import subprocess
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
        "repo": "https://github.com/apple/swift.git",
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
    }
}
RESULTS = os.path.join(os.getcwd(), "test", "results.json")
TEMP_DIR = os.path.join(os.getcwd(), "dev", "repos")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


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
    """
    """
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
            computed = indentifier(src=p)
            if computed == lang:
                identified += 1
            elif computed == -1:
                file_count -= 1
                print("Insufficient information {}!".format(p))
            else:
                print("Incorrectly identified ({}) {}!".format(computed, p))
    c = round(identified / file_count if file_count else 1, 3)
    print("Correct = {} ({} / {})".format(c, identified, file_count))
    store_result(lang, c)


def clone_and_clean(repo, src_dir, ext):
    (out, error) = subprocess.Popen(
        ["git", "clone", repo],
        cwd=TEMP_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()

    for subdir, dirs, files in os.walk(src_dir):
        for f in files:
            if any(f.endswith(e) for e in ext):
                continue
            os.remove(os.path.join(subdir, f))


def run(lang, is_test, identifier=None, writer=None):
    """
    """
    test_all = False
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
                test_sig(src_dir, lang, info["ext"], identifier)
        else:
            test_sig(src_dir, lang, info["ext"], identifier)
    elif is_test:
        print("Please specify an identifier.")
        return -1
    elif writer:
        writer(src_dir, lang=lang, ext=info["ext"], is_file=1)
    else:
        print("Please specify a writer.")
        return -1
    return 0
