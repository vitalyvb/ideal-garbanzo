#!python3

import asyncio
import unittest
from scapy.all import Ether, IP, UDP, conf, L2Socket


async def run_fake(env, sock):
    pass


async def run_real(env, sock):
    pkt_verbose = Ether() / IP(dst="1.2.3.4", ttl=64) / UDP(sport=5554, dport=5553) / ('Next level password is ' + env.nextpass + ' ')
    pkt_silent = Ether() / IP(dst="1.2.3.4", ttl=64) / UDP(sport=5554, dport=5553) / env.nextpass

    i = 0
    while True:
        sock.send(pkt_verbose if i % 25 == 0 else pkt_silent)
        await asyncio.sleep(1)
        i += 1


def run(env):

    conf.iface = env.interface
    conf.ipv6_enabled = False

    # no rx
    eth0 = L2Socket(iface=env.interfaces[0], filter="proto 254", promisc=False)
    eth1 = L2Socket(iface=env.interfaces[1], filter="proto 254", promisc=False)

    async def runner():
        await asyncio.gather(
            run_fake(env, eth0),
            run_real(env, eth1),
        )

    asyncio.run(runner())
