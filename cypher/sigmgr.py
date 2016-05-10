#!/usr/bin/env python
import argparse
import subprocess
import os
import shutil
import sys

from util import write_signature, identify

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
    ext = [".c"]
elif args["lang"] == "C++":
    repo = "https://github.com/apple/swift.git"
    ext = [".cpp", ".cc"]
elif args["lang"] == "R":
    repo = "https://github.com/rstudio/shiny.git"
    ext = [".R", ".r"]
elif args["lang"] == "Haskell":
    repo = "https://github.com/haskell/cabal.git"
    ext = [".hs"]
elif args["lang"] == "JavaScript":
    repo = "https://github.com/facebook/react.git"
    ext = [".js"]
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
print(src_dir)
if args["test"]:
    file_count = 0.0
    identified = 0.0
    for subdir, dirs, files in os.walk(src_dir):
        for f in files:
            p = os.path.join(subdir, f)
            if ext and not any(f.endswith(e) for e in ext):
                continue
            if os.stat(p).st_size == 0:
                continue
            file_count += 1
            computed = identify(src=p, is_file=1)
            if computed == args["lang"]:
                identified += 1
            elif computed == -1:
                file_count -= 1
                print("Insufficient information {}!".format(p))
            else:
                print("Incorrectly identified ({}) {}!".format(computed, p))
    c = identified / file_count if file_count else 1
    print("Correct = {} ({} / {})".format(round(c, 3), identified, file_count))
else:
    write_signature(src_dir, lang=args["lang"], ext=ext, is_file=1)
shutil.rmtree(TEMP_DIR)
