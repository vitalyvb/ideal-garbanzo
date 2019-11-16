#!python3

import asyncio
from scapy.all import Ether, IP, UDP, conf, L2Socket
from ...util.rnd import Rnd, FakeFlows, NoIPs
from ..level02 import AUTH_SERVER_ADDR


def generator(flow):
    return Ether() / IP(dst=flow.dip, src=flow.sip, ttl=64) / UDP(sport=flow.sp, dport=flow.dp) / (' ' + flow.pwd)


async def run_fake(env, sock):
    flows = FakeFlows(env.rnd, generator, count=30)

    await flows.iterate(sock.send, pps=10)


async def run_real(env, sock):
    flows = FakeFlows(env.rnd, generator, count=9)

    dst = AUTH_SERVER_ADDR
    p1 = env.rnd.random_port()
    p2 = env.rnd.random_port()

    pkt_silent = Ether() / IP(dst=dst, ttl=64) / UDP(sport=p1, dport=p2) / (' ' + env.nextpass)

    i = 0
    while True:
        if i % 10 == 0:
            sock.send(pkt_silent)
        else:
            flow = flows.get_random()
            sock.send(flow.get_data())
        await asyncio.sleep(1.0 / (len(flows) + 1))
        i += 1


def run(env):

    conf.iface = env.interface
    conf.ipv6_enabled = False

    env.rnd = Rnd(env, filter=NoIPs([AUTH_SERVER_ADDR]))

    # no rx
    eth0 = L2Socket(iface=env.interfaces[0], filter="proto 254", promisc=False)
    eth1 = L2Socket(iface=env.interfaces[1], filter="proto 254", promisc=False)

    async def runner():
        await asyncio.gather(
            run_fake(env, eth0),
            run_real(env, eth1),
        )

    asyncio.run(runner())
