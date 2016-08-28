import subprocess
import time
import json
import sys
import os

import msgpack

sys.path.append(os.path.abspath("../cypher"))

from cypher import (
    identify,
    compute_signature,
    summarize_text,
    SIG_PATH
)

LANG_INFO = {
    "Python": {
        "repo": "https://github.com/django/django.git",
        "ext": [".py"]
    },
    "Ruby": {
        "repo": "https://github.com/rails/rails.git",
        "ext": [".rb"]
    },
    "C": {
        "repo": "https://github.com/git/git.git",
        "ext": [".c"]
    },
    "C++": {
        "repo": "https://github.com/electron/electron.git",
        "ext": [".cc", ".cpp"]
    },
    "R": {
        "repo": "https://github.com/rstudio/shiny.git",
        "ext": [".r", ".R"]
    },
    "Haskell": {
        "repo": "https://github.com/haskell/cabal.git",
        "ext": [".hs"]
    },
    "C#": {
        "repo": "https://github.com/NancyFx/Nancy.git",
        "ext": [".cs"]
    },
    "Java": {
        "repo": "https://github.com/spring-projects/spring-framework.git",
        "ext": [".java"]
    },
    "Go": {
        "repo": "https://github.com/docker/docker.git",
        "ext": [".go"]
    },
    "Rust": {
        "repo": "https://github.com/rust-lang/cargo.git",
        "ext": [".rs"]
    },
    "PHP": {
        "repo": "https://github.com/WordPress/WordPress.git",
        "ext": [".php"]
    },
    "Perl": {
        "repo": "https://github.com/kraih/mojo.git",
        "ext": [".pm"]
    },
    "Objective-C": {
        "repo": "https://github.com/adium/adium.git",
        "ext": [".m"]
    },
    "Lua": {
        "repo": "https://github.com/Mashape/kong.git",
        "ext": [".lua"]
    },
    "Scala": {
        "repo": "https://github.com/paypal/squbs.git",
        "ext": [".scala"]
    },
    "D": {
        "repo": "https://github.com/dlang/phobos.git",
        "ext": [".d"]
    },
    "AppleScript": {
        "repo": "https://github.com/Zettt/LaunchBar-Scripts.git",
        "ext": [".applescript"]
    },
    "Julia": {
        "repo": "https://github.com/BioJulia/Bio.jl.git",
        "ext": [".jl"]
    },
    "OCaml": {
        "repo": "https://github.com/coq/coq.git",
        "ext": [".ml", ".mli"]
    },
    "JavaScript": {
        "repo": "https://github.com/vuejs/vue.git",
        "ext": [".js"]
    },
    "Swift": {
        "repo": "https://github.com/eBay/NMessenger",
        "ext": [".swift"]
    }
}
DIR_PATH = os.path.join(os.getcwd(), "dev")
RESULTS = os.path.join(DIR_PATH, "results.json")
TEMP_DIR = os.path.join(DIR_PATH, "repos")
LOG_DIR = os.path.join(DIR_PATH, "logs")
DATA_PATH = os.path.join(DIR_PATH, "data")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def store_result(lang, new):
    with open(RESULTS) as jdata:
        d = json.load(jdata)
    old = d.get(lang, 0)
    print("{0}: diff (from last run) = {1}".format(lang, round(new - old, 3)))
    d[lang] = new
    with open(RESULTS, "w+") as results:
        json.dump(d, results, indent=4, sort_keys=True)


def test_sig(src_dir, lang, ext):
    log = open(os.path.join(LOG_DIR, lang + ".txt"), "w+")
    file_count = 0.0
    identified = 0.0
    times = []
    for subdir, _, files in os.walk(src_dir):
        for f in files:
            p = os.path.join(subdir, f)
            sp = p.split("repos")[1]
            if not os.path.exists(p):
                continue
            if ext and not any(f.endswith(e) for e in ext):
                continue
            if os.stat(p).st_size == 0:
                continue
            file_count += 1
            start_time = time.time()
            computed = identify(src=p)
            times.append(time.time() - start_time)
            if computed == lang:
                identified += 1
            elif computed == -1:
                file_count -= 1
                log.write("Insufficient information {}!\n".format(sp))
            else:
                log.write("Incorrect: ({}) {}!\n".format(computed, sp))
    log.close()
    c = round(identified / file_count if file_count else 1, 3)
    store_result(lang, c)
    print("{}: Correct = {} ({} / {})".format(lang, c, identified, file_count))
    return sum(times) / len(times), file_count, c


def clone_and_clean(repo, src_dir, ext):
    subprocess.Popen(
        ["git", "clone", repo],
        cwd=TEMP_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()

    for subdir, _, files in os.walk(src_dir):
        for f in files:
            path = os.path.join(subdir, f)
            if any(f.endswith(e) for e in ext) and os.path.exists(path):
                continue
            os.remove(path)


def get_lang_data(lang):
    d = {}
    tokens = []
    if lang is None:
        return d, None, None, None

    with open(os.path.join(DATA_PATH, lang + ".json")) as jdata:
        d = json.load(jdata)

    for k, v in d.items():
        if k not in ["ignores", "first_line"]:
            tokens.extend(v)
    tokens = set(tokens)

    return tokens, d


def write_signature(src, lang, ext, is_file=True):
    known, lang_data = get_lang_data(lang)
    tokens = []
    lines = 0.0

    for subdir, _, files in os.walk(src):
        for f in files:
            if ext and not any(f.endswith(e) for e in ext):
                continue
            summary = summarize_text(
                os.path.join(subdir, f),
                is_file=is_file,
                filtered=known
            )
            tokens.extend(summary["tokens"])
            lines += summary["lines"]

    lang_data["tokens"] = tokens
    lang_data["lines"] = lines
    data = compute_signature(lang_data)
    with open(os.path.join(SIG_PATH, lang + ".bin"), "wb") as sig:
        msgpack.dump(data, sig, use_bin_type=True)


def run(lang, is_test):
    times = []
    files = 0
    correct = []
    if is_test:
        for lang, info in LANG_INFO.items():
            print("Testing {}...".format(lang))
            src_dir = os.path.join(
                TEMP_DIR, info["repo"].split("/")[-1].split(".git")[0]
            )
            if not os.path.exists(os.path.join(TEMP_DIR, src_dir)):
                clone_and_clean(info["repo"], src_dir, info["ext"])
            timed, count, percentage = test_sig(src_dir, lang, info["ext"])
            times.append(timed)
            files += count
            correct.append(percentage)
        print("# of files: {}".format(files))
        print("Time per file: {}s".format(round(sum(times) / len(times), 3)))
        print("Accuracy: {}".format(round(sum(correct) / len(LANG_INFO), 3)))
    else:
        info = LANG_INFO.get(lang)
        src_dir = os.path.join(
            TEMP_DIR, info["repo"].split("/")[-1].split(".git")[0]
        )
        if not os.path.exists(os.path.join(TEMP_DIR, src_dir)):
            clone_and_clean(info["repo"], src_dir, info["ext"])
        write_signature(src_dir, lang=lang, ext=info["ext"], is_file=1)
    return 0
