#!python3

import asyncio
import random
from scapy.all import Ether, IP, UDP, conf, L2Socket, Raw, RandBin, RandString
from ...util.rnd import Rnd, FakeFlows, NoIPsPorts


AUTH_SERVER_ADDR_MIN = "172.31.7.2"
AUTH_SERVER_ADDR_COUNT = 250
AUTH_SERVER_PORT_MIN = 5200
AUTH_SERVER_PORT_MAX = 5700
AUTH_SERVER_PORT_COUNT = AUTH_SERVER_PORT_MAX - AUTH_SERVER_PORT_MIN


def generator1(flow):
    return Ether() / IP(dst=flow.dip, src=flow.sip, ttl=64) / UDP(sport=flow.sp, dport=flow.dp) / (' ' + flow.pwd)


async def run_fake(env, sock):
    flows = FakeFlows(env.rnd, generator1, count=40)

    await flows.iterate(sock.send, pps=5)


def generator2(flow):
    gen = random.choice([RandBin, RandString])
    return Ether() / IP(dst=flow.dip, src=flow.sip, ttl=64) / UDP(sport=flow.sp, dport=flow.dp) / Raw(gen(size=random.randint(50, 1000)))


async def run_fake2(env, sock):
    flows = FakeFlows(env.rnd, generator2, count=40)

    await flows.iterate(sock.send, pps=5)


async def run_fake3(env, sock):
    def generator(flow):
        if random.choice([False, True]):
            flow.dip = env.rnd3.random_ip_from(AUTH_SERVER_ADDR_MIN, AUTH_SERVER_ADDR_COUNT)
        else:
            flow.dp = env.rnd2.random_port_from(AUTH_SERVER_PORT_MIN, AUTH_SERVER_PORT_COUNT)
        gen = random.choice([generator1, generator2])
        return gen(flow)

    flows = FakeFlows(env.rnd, generator, count=50)

    await flows.iterate(sock.send, pps=15)


async def run_real(env, sock):
    dst = env.rnd.random_ip()
    pkt_silent = Ether() / IP(dst=dst, src=env.addr, ttl=64) / UDP(sport=env.port, dport=env.port) / (' ' + env.nextpass)

    while True:
        sock.send(pkt_silent)
        await asyncio.sleep(5.0)


def run(env):

    conf.iface = env.interface
    conf.ipv6_enabled = False

    trnd = Rnd(env)
    env.addr = trnd.random_ip_from(AUTH_SERVER_ADDR_MIN, AUTH_SERVER_ADDR_COUNT)
    env.port = trnd.random_port_from(AUTH_SERVER_PORT_MIN, AUTH_SERVER_PORT_COUNT)

    noips = [(AUTH_SERVER_ADDR_MIN, AUTH_SERVER_ADDR_COUNT)]
    noports = list(range(AUTH_SERVER_PORT_MIN, AUTH_SERVER_PORT_MAX + 1))
    env.rnd = Rnd(env, filter=NoIPsPorts(noips, noports))

    env.rnd2 = Rnd(env, filter=NoIPsPorts(noips, [env.port]))
    env.rnd3 = Rnd(env, filter=NoIPsPorts([env.addr], noports))

    # no rx
    eth0 = L2Socket(iface=env.interface, filter="proto 254", promisc=False)

    async def runner():
        await asyncio.gather(
            run_fake(env, eth0),
            run_fake2(env, eth0),
            run_fake3(env, eth0),
            run_real(env, eth0),
        )

    asyncio.run(runner())
