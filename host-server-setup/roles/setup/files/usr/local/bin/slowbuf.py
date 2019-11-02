#!/usr/bin/env python3

import sys
import time

TIME = 0.6

data = sys.stdin.read(1024*1024)
lines = data.splitlines()
start = time.monotonic()
step = TIME / len(lines)
i = 0
for l in lines:
    print(l)
    i += 1

    offs = step*i - (time.monotonic()-start)
    if offs > 0:
        time.sleep(offs)
