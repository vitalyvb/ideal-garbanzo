#!python3

import random
import string


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

    def random_fake_pass(self):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.sample(chars, len(self.env.nextpass)))

