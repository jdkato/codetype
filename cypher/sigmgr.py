#!/usr/bin/env python
import argparse
import subprocess
import os
import shutil
import sys

from util import write_signature

parser = argparse.ArgumentParser()
parser.add_argument(
    "lang",
    nargs="?",
    help="Language name"
)
parser.add_argument(
    "-t",
    "--test",
    action="store_true",
    help="Run base test"
)

TEMP_DIR = os.path.join(os.getcwd(), "cypher", "temp")
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)

args = vars(parser.parse_args())
if args["lang"] == "Python":
    repo = "https://github.com/django/django.git"
    ext = [".py"]
elif args["lang"] == "Ruby":
    repo = "https://github.com/Homebrew/legacy-homebrew.git"
    ext = [".rb"]
elif args["lang"] == "C":
    repo = "https://github.com/git/git.git"
    ext = [".c", ".h"]
elif args["lang"] == "C++":
    repo = "https://github.com/apple/swift.git"
    ext = [".cpp", ".cc", ".h"]
elif args["lang"] == "R":
    repo = "https://github.com/rstudio/shiny.git"
    ext = [".R", ".r"]
elif args["lang"] == "Haskell":
    repo = "https://github.com/haskell/cabal.git"
    ext = [".hs"]
else:
    print("{} not found.".format(args["lang"]))
    sys.exit(0)

os.makedirs(TEMP_DIR)
pro = subprocess.Popen(
    ["git", "clone", repo],
    cwd=TEMP_DIR,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
(out, error) = pro.communicate()

src_dir = os.path.join(TEMP_DIR, repo.split("/")[-1].split(".")[0])
if args["test"]:
    pass
else:
    write_signature(src_dir, lang=args["lang"], ext=ext, is_file=1)
shutil.rmtree(TEMP_DIR)
