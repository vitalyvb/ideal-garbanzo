#!python3

import time
from scapy.all import Ether, IP, UDP, conf, L2Socket
from ...util.rnd import Rnd


def run(env):

    conf.iface = env.interface
    conf.ipv6_enabled = False

    rnd = Rnd(env)

    dst = rnd.random_ip()
    p1 = rnd.random_port()
    p2 = rnd.random_port()

    pkt_verbose = Ether() / IP(dst=dst, ttl=64) / UDP(sport=p1, dport=p2) / ('Next level password is ' + env.nextpass + ' ')
    pkt_silent = Ether() / IP(dst=dst, ttl=64) / UDP(sport=p1, dport=p2) / (' ' + env.nextpass)

    # no rx
    sock = L2Socket(iface=conf.iface, filter="proto 254", promisc=False)
    i = 0

    while True:
        sock.send(pkt_verbose if i % 16 == 0 else pkt_silent)
        time.sleep(1)
        i += 1
