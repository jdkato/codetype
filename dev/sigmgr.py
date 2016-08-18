import subprocess
import time
import json
import os

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
        "repo": "https://github.com/getlantern/lantern.git",
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
    }
}
RESULTS = os.path.join(os.getcwd(), "dev", "results.json")
TEMP_DIR = os.path.join(os.getcwd(), "dev", "repos")
LOG_DIR = os.path.join(os.getcwd(), "dev", "logs")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def store_result(lang, new):
    """
    """
    with open(RESULTS) as jdata:
        d = json.load(jdata)
    old = d.get(lang, 0)
    print("{0}: diff = {1}".format(lang, round(new - old, 3)))
    d[lang] = new
    with open(RESULTS, "w+") as results:
        json.dump(d, results, indent=4, sort_keys=True)


def test_sig(src_dir, lang, ext, indentifier):
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
            computed = indentifier(src=p)
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
    return sum(times) / len(times)


def clone_and_clean(repo, src_dir, ext):
    subprocess.Popen(
        ["git", "clone", repo],
        cwd=TEMP_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()

    for subdir, _, files in os.walk(src_dir):
        for f in files:
            if any(f.endswith(e) for e in ext):
                continue
            os.remove(os.path.join(subdir, f))


def run(lang, is_test, identifier=None, writer=None):
    """
    """
    test_all = False
    times = []
    if not lang:
        test_all = True
    else:
        info = LANG_INFO.get(lang)
        src_dir = os.path.join(
            TEMP_DIR, info["repo"].split("/")[-1].split(".")[0]
        )
        if not os.path.exists(os.path.join(TEMP_DIR, src_dir)):
            clone_and_clean(info["repo"], src_dir, info["ext"])

    if is_test and identifier:
        if test_all:
            for lang, info in LANG_INFO.items():
                src_dir = os.path.join(
                    TEMP_DIR, info["repo"].split("/")[-1].split(".")[0]
                )
                times.append(test_sig(src_dir, lang, info["ext"], identifier))
        else:
            times.append(test_sig(src_dir, lang, info["ext"], identifier))
        print("Avg. time per file: {}".format(sum(times) / len(times)))
    elif is_test:
        print("Please specify an identifier.")
        return -1
    elif writer:
        writer(src_dir, lang=lang, ext=info["ext"], is_file=1)
    else:
        print("Please specify a writer.")
        return -1
    return 0
