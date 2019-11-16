#!python3

import asyncio
import random
from scapy.all import Ether, IP, UDP, conf, L2Socket, Raw, RandBin
from ...util.rnd import Rnd, FakeFlows, NoIPsPorts
from ..level02 import AUTH_SERVER_ADDR


AUTH_SERVER_PORT = 6236


async def run_fake(env, sock):
    def generator(flow):
        return Ether() / IP(dst=flow.dip, src=flow.sip, ttl=64) / UDP(sport=flow.sp, dport=flow.dp) / (' ' + flow.pwd)

    flows = FakeFlows(env.rnd, generator, count=30)

    await flows.iterate(sock.send, pps=10)


async def run_fake2(env, sock):
    def generator(flow):
        return Ether() / IP(dst=flow.dip, src=flow.sip, ttl=64) / UDP(sport=flow.sp, dport=flow.dp) / Raw(RandBin(size=random.randint(50, 1000)))

    flows = FakeFlows(env.rnd, generator, count=40)

    await flows.iterate(sock.send, pps=15)


async def run_real(env, sock):
    dst = AUTH_SERVER_ADDR
    p1 = AUTH_SERVER_PORT
    p2 = AUTH_SERVER_PORT

    pkt_silent = Ether() / IP(dst=dst, ttl=64) / UDP(sport=p1, dport=p2) / (' ' + env.nextpass)

    while True:
        sock.send(pkt_silent)
        await asyncio.sleep(3.0)


def run(env):

    conf.iface = env.interface
    conf.ipv6_enabled = False

    env.rnd = Rnd(env, filter=NoIPsPorts([AUTH_SERVER_ADDR], [AUTH_SERVER_PORT]))

    # no rx
    eth0 = L2Socket(iface=env.interface, filter="proto 254", promisc=False)

    async def runner():
        await asyncio.gather(
            run_fake(env, eth0),
            run_fake2(env, eth0),
            run_real(env, eth0),
        )

    asyncio.run(runner())
