#!python3

import time
from scapy.all import *

def run(env):

    conf.iface = env.interface
    conf.ipv6_enabled = False

    pkt = Ether()/IP(dst="1.2.3.4",ttl=64)/UDP(sport=53)/DNS(rd=1, qd=DNSQR(qname='password is ' + env.nextpass + ' '))

    while True:
        sendp(pkt)
        time.sleep(1)
