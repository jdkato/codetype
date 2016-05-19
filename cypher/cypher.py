import argparse
from .util import identify

parser = argparse.ArgumentParser(
    prog="cypher",
    description="A source code identification tool."
)
parser.add_argument(
    "src",
    nargs=1,
    help="Path to unknown source code."
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Return all scores."
)
parser.add_argument(
    "-f",
    "--file",
    action="store_true",
    help="Indicates the the source is being passed as a file."
)
args = vars(parser.parse_args())


def main():
    if not args["src"][0]:
        print("foo")
    result = identify(
        args["src"][0],
        is_file=args["file"],
        verbose=args["verbose"]
    )
    print(args["src"][0])
    if result < 0:
        return -1
    else:
        print(result)
        return 0
