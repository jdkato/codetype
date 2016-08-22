import argparse
import sys
import unittest

from cypher import identify
from dev import run

parser = argparse.ArgumentParser()
parser.add_argument(
    "script",
    nargs=1,
    help="dev|test"
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
if script == "dev":
    if args["test"]:
        run(lang=args["lang"], is_test=1)
    elif args["lang"]:
        run(lang=args["lang"], is_test=0)
elif script == "test":
    unittest.TextTestRunner().run(unittest.TestLoader().discover("."))
elif script == "cypher":
    print(identify(args["lang"], verbose=args["verbose"]))
else:
    print("{0} not recognized!".format(script))
sys.exit(0)
