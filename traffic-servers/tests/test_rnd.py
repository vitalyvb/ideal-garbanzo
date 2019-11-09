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


    def test_random_fake_pass(self):
        env = TstEnv()
        r = Rnd(env)

        p = r.random_fake_pass()
        self.assertEqual(len(env.nextpass), len(p))

        p = [r.random_fake_pass() for x in range(100)]
        self.assertEqual(len(p), 100)
