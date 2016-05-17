import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument(
    "script",
    nargs="?",
    const="cypher",
    type=str,
    help="cypher|mkdocs|sigmgr"
)

if __name__ == "__main__":
    from cypher.cypher import main
    sys.exit(main())
