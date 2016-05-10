import argparse
import os

parser = argparse.ArgumentParser(
    prog="cypher",
    description="A source code identification tool."
)
parser.add_argument(
    "src",
    nargs="?",
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


def identify(src, is_file=False, verbose=False):
    """Attempt to identify the language which `src` is written in.

    Args:
        src (str): Either a string or a file path.
        is_file (bool): `True` if `src` is a file.
        verbose (bool): `True` if verbose output is to be used.

    Returns:
        (str|dict): A string specifying the computed language if `verbose` is
            `False`. Otherwise a dictionary with all tested languages as keys
            and their computed scores as values.
    """
    return None


def main():
    print(identify(args["src"], is_file=args["file"], verbose=args["verbose"]))
