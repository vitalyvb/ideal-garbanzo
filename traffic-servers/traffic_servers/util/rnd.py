#!python3

import random
import string


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


class Rnd:
    def __init__(self, env):
        self.env = env

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

    def random_port(self):
        return random.randint(1025, 32767)

    def random_loport(self):
        return random.randint(120, 1023)

    def random_hiport(self):
        return random.randint(32768, 65535)

    def random_fake_pass(self):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.sample(chars, len(self.env.nextpass)))

