#!python3

_submodules = []

for _x in range(1, 30):
    try:
        _n = "level{:02d}".format(_x)
        __import__("{}.{}".format(__name__, _n), globals=globals(), fromlist=(_n,))
        _submodules.append(_n)
    except ModuleNotFoundError:
        break;

del _x
del _n
