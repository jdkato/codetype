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

TEMP_DIR = os.path.join(os.getcwd(), "cypher", "temp")
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)
lang = vars(parser.parse_args())["lang"]
if lang == "Python":
    repo = "https://github.com/django/django.git"
    ext = [".py"]
elif lang == "Ruby":
    repo = "https://github.com/Homebrew/legacy-homebrew.git"
    ext = [".rb"]
elif lang == "C":
    repo = "https://github.com/git/git.git"
    ext = [".c", ".h"]
elif lang == "C++":
    repo = "https://github.com/apple/swift.git"
    ext = [".cpp", ".cc", ".h"]
elif lang == "R":
    repo = "https://github.com/rstudio/shiny.git"
    ext = [".R", ".r"]
elif lang == "Haskell":
    repo = "https://github.com/haskell/cabal.git"
    ext = [".hs"]
else:
    print("{} not found.".format(lang))
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
write_signature(src_dir, lang=lang, ext=ext, is_file=1)
shutil.rmtree(TEMP_DIR)
