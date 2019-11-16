#!python3

import asyncio
import random
import string
import socket
import struct


class FakeFlow:
    def __init__(self, rnd, generator):
        self.sip = rnd.random_ip()
        self.dip = rnd.random_ip()
        self.sp = rnd.random_port()
        self.dp = rnd.random_port()
        self.pwd = rnd.random_fake_pass()
        self.generator = generator
        self._data = None

    def get_data(self):
        if self._data is None:
            self._data = self.generator(self)
        return self._data


class FakeFlows:
    def __init__(self, rnd, generator, count=10):
        self.flows = [FakeFlow(rnd, generator) for x in range(count)]

    def get_random(self):
        return random.choice(self.flows)

    def __len__(self):
        return len(self.flows)

    async def iterate(self, send, pps=10):
        slp = 1.0 / pps
        while True:
            flow = self.get_random()
            send(flow.get_data())
            await asyncio.sleep(slp)


class FilterBase:
    def check_ip(self, ip):
        return True

    def check_port(self, port):
        return True


class NoIPs(FilterBase):
    def __init__(self, ips):
        addrs = []
        for ip in ips:
            if isinstance(ip, type((0,))):
                addrs.extend(self._addr_expand(ip[0], ip[1]))
            else:
                addrs.append(ip)

        self.ips = set(addrs)

    def _addr_expand(self, from_addr, count):
        rep = socket.inet_aton(from_addr)
        ipn = struct.unpack("!I", rep)[0]
        for i in range(count + 1):
            yield struct.pack("!I", ipn + i)

    def check_ip(self, ip):
        return ip not in self.ips


class NoPorts(FilterBase):
    def __init__(self, ports):
        self.ports = set(ports)

    def check_port(self, port):
        return port not in self.ports


class NoIPsPorts(NoIPs, NoPorts):
    def __init__(self, ips, ports):
        NoIPs.__init__(self, ips)
        NoPorts.__init__(self, ports)


class Rnd:
    def __init__(self, env, filter=None):
        self.env = env
        self.flt = FilterBase() if filter is None else filter

    def filterby(what):
        def check(self, *a, **kw):
            flt = self.flt
            return getattr(flt, "check_{}".format(what))(*a, **kw)

        def mkflt(f):
            def g(self, *a, **kw):
                v = f(self, *a, **kw)
                while not check(self, v):
                    v = f(self, *a, **kw)
                return v
            g.__name__ = f.__name__
            return g
        return mkflt

    @filterby("ip")
    def random_ip(self):
        def first():
            while True:
                r = random.randint(1, 239)
                if r in [127, 169]:
                    continue
                break
            return r

        return "{}.{}.{}.{}".format(first(),
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(1, 254))

    @filterby("ip")
    def random_ip_from(self, from_addr, count):
        rep = socket.inet_aton(from_addr)
        ipn = struct.unpack("!I", rep)[0]
        ipn += random.randint(0, count)
        rep = struct.pack("!I", ipn)
        return socket.inet_ntoa(rep)

    @filterby("port")
    def random_port_from(self, from_port, count):
        return random.randint(from_port, from_port + count)

    @filterby("port")
    def random_port(self):
        return random.randint(1025, 32767)

    @filterby("port")
    def random_loport(self):
        return random.randint(120, 1023)

    @filterby("port")
    def random_hiport(self):
        return random.randint(32768, 65535)

    def random_fake_pass(self):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.sample(chars, len(self.env.nextpass)))

