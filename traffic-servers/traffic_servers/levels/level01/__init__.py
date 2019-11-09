#!python3

import time
from scapy.all import Ether, IP, UDP, conf, L2Socket


def run(env):

    conf.iface = env.interface
    conf.ipv6_enabled = False

    pkt_verbose = Ether() / IP(dst="1.2.3.4", ttl=64) / UDP(sport=5554, dport=5553) / ('Next level password is ' + env.nextpass + ' ')
    pkt_silent = Ether() / IP(dst="1.2.3.4", ttl=64) / UDP(sport=5554, dport=5553) / env.nextpass

    # no rx
    sock = L2Socket(iface=conf.iface, filter="proto 254", promisc=False)
    i = 0

    while True:
        sock.send(pkt_verbose if i % 16 == 0 else pkt_silent)
        time.sleep(1)
        i += 1
