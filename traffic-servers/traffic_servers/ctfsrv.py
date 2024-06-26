#!python3

import argparse
import logging
import importlib


class Env:
    def __init__(self, args):
        self._args = args
        self.params = args.parameters
        self.verbose = args.verbose
        self.interfaces = args.interfaces.split(",")
        self.interface = self.interfaces[0]
        self.nextpass = open(args.nextpwfile, "r").read(1024).strip()


def setup_logging(args):
    level = logging.INFO
    if args.verbose > 0:
        level = logging.DEBUG
    logging.basicConfig(level=level)
    logging.debug("Command line: {}".format(args))


def list_runners():
    from . import levels

    for m in levels._submodules:
        print(m)


def runner(args):
    if args.generator == "list":
        return list_runners()

    name = ".levels.{}".format(args.generator)
    try:
        gen = importlib.import_module(name, __package__)
    except ModuleNotFoundError as e:
        if e.name != name:
            raise
        logging.error("Generator '{}' not found, use 'list' to list available generators.".format(args.generator))
        return

    return gen.run(Env(args))


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="count", default=0)
    parser.add_argument("-i", "--interfaces", help="set working interfaces",
                        required=True)
    parser.add_argument("-n", "--nextpwfile", help="file with the password for the next level",
                        required=True)
    parser.add_argument("generator", help="generator name to run")

    parser.add_argument('parameters', help="parameter to pass to the generator",
                        nargs=argparse.REMAINDER)

    args = parser.parse_args()
    setup_logging(args)
    return runner(args)


if __name__ == '__main__':
    main()
