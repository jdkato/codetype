import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument(
    "script",
    nargs=1,
    help="mddocs|sigmgr|test"
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

args = vars(parser.parse_args())
script = args["script"][0]
if not script:
    from cypher.cypher import main
    sys.exit(main())
elif script == "sigmgr":
    from dev.sigmgr import run
    if args["test"] and args["lang"]:
        from cypher.util import identify
        sys.exit(run(lang=args["lang"], is_test=1, identifier=identify))
    elif args["lang"]:
        from cypher.util import write_signature as sig_writer
        sys.exit(run(lang=args["lang"], is_test=0, writer=sig_writer))
elif script == "test":
    import unittest
    suite = unittest.TestLoader().discover(".")
    run = unittest.TextTestRunner().run(suite)
sys.exit(0)
