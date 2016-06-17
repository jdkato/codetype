import argparse
import sys
import unittest

from cypher.util import (
    identify,
    write_signature as sig_writer
)
from dev.sigmgr import run

parser = argparse.ArgumentParser()
parser.add_argument(
    "script",
    nargs=1,
    help="sigmgr|test"
)
parser.add_argument(
    "-t",
    "--test",
    action="store_true"
)
parser.add_argument(
    "lang",
    nargs="?"
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Return all scores."
)

args = vars(parser.parse_args())
script = args["script"][0]
if script == "sigmgr":
    if args["test"]:
        run(lang=args["lang"], is_test=1, identifier=identify)
    elif args["lang"]:
        run(lang=args["lang"], is_test=0, writer=sig_writer)
elif script == "test":
    unittest.TextTestRunner().run(unittest.TestLoader().discover("."))
elif script == "cypher":
    r = identify(args["lang"], verbose=args["verbose"])
    print(r)
else:
    print("{0} not recognized!".format(script))
sys.exit(0)
