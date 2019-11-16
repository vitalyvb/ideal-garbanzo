#!python3

import asyncio
import random
import unittest
import socket

from env import *

from traffic_servers.util.rnd import *

class TestRnd(unittest.TestCase):

    def test_random_ip(self):
        r = Rnd(TstEnv())
        for x in range(100):
            x = socket.inet_aton(r.random_ip())

    def test_random_ip_from(self):
        base = "55.55.55.0"
        basen = struct.unpack("!I", socket.inet_aton(base))[0]
        r = Rnd(TstEnv())
        for x in range(100):

            ip = r.random_ip_from(base, 50)

            x = struct.unpack("!I", socket.inet_aton(ip))[0]
            self.assertGreaterEqual(x, basen, "{} out of range of {} + {}".format(ip, base, 50))
            self.assertLessEqual(x, basen+50, "{} out of range of {} + {}".format(ip, base, 50))


    def test_random_port(self):
        r = Rnd(TstEnv())
        for x in range(100):
            x = r.random_port()
            self.assertGreater(x, 0)
            self.assertLess(x, 65536)

    def test_random_ip_filter(self):
        base = "10.0.0.0"
        cnt = 65535
        basen = struct.unpack("!I", socket.inet_aton(base))[0]
        r = Rnd(TstEnv(), NoIPs([(base, cnt)]))
        for x in range(100):
            ip = r.random_ip()
            #ip = "9.255.255.255" # pass
            #ip = "10.0.0.0" # fail
            #ip = "10.0.255.255" # fail
            #ip = "10.1.0.0" # pass
            x = struct.unpack("!I", socket.inet_aton(ip))[0]

            self.assertTrue((x < basen) or (x > basen+cnt), "{} hit range of {} + {}".format(ip, base, cnt))

    def test_random_port_filter(self):
        exclude = set(range(0, 65536))-set(range(0, 65536, 2))
        r = Rnd(TstEnv(), NoPorts(list(exclude)))
        for x in range(20):
            x = r.random_port()
            self.assertEqual(x%2, 0)

    def test_random_port_filter(self):
        exclude = set(range(0, 65536))-set(range(0, 65536, 2))
        r = Rnd(TstEnv(), NoIPsPorts([], list(exclude)))
        for x in range(20):
            x = r.random_port()
            self.assertEqual(x%2, 0)

    def test_random_fake_pass(self):
        env = TstEnv()
        r = Rnd(env)

        p = r.random_fake_pass()
        self.assertEqual(len(env.nextpass), len(p))

        p = [r.random_fake_pass() for x in range(100)]
        self.assertEqual(len(p), 100)
