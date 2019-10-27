#!python3

import argparse
import logging


def setup_logging(args):
    level = logging.INFO
    if args.verbose > 0:
        level = logging.DEBUG
    logging.basicConfig(level=level)
    logging.debug("Command line: {}".format(args))


def list_runners():
    import levels

    for m in levels._submodules:
        print(m)


def runner(args):
    if args.generator == "list":
        return list_runners()

    try:
        gen = __import__("levels.{}".format(args.generator), globals=globals(), fromlist=(args.generator,))
    except ModuleNotFoundError:
        logging.error("Generator '{}' not found, use 'list' to list available generators.".format(args.generator))
        return

    return gen.run(args)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="count", default=0)
    parser.add_argument("-i", "--interface", help="set a working interface",
                        required=True)
    parser.add_argument("generator", help="generator name to run")

    parser.add_argument('parameters', help="parameter to pass to the generator",
                        nargs=argparse.REMAINDER)

    args = parser.parse_args()
    setup_logging(args)
    return runner(args)


if __name__ == '__main__':
    main()
