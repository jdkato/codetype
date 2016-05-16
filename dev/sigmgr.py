import subprocess
import os
import shutil

LANG_INFO = {
    "Python": {"repo": "https://github.com/django/django.git", "ext": [".py"]},
    "Ruby": {"repo": "https://github.com/rails/rails.git", "ext": [".rb"]},
    "C": {"repo": "https://github.com/git/git.git", "ext": [".c"]},
    "C++": {"repo": "https://github.com/apple/swift.git", "ext": [".cc", ".cpp"]},
    "R": {"repo": "https://github.com/rstudio/shiny.git", "ext": [".r", ".R"]},
    "Haskell": {"repo": "https://github.com/haskell/cabal.git", "ext": [".hs"]},
    "JavaScript": {"repo": "https://github.com/mbostock/d3.git", "ext": [".js"]},
    "C#": {"repo": "https://github.com/NancyFx/Nancy.git", "ext": [".cs"]}
}
TEMP_DIR = os.path.join(os.getcwd(), "cypher", "temp")


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
            computed = indentifier(src=p, is_file=1)
            if computed == lang:
                identified += 1
            elif computed == -1:
                file_count -= 1
                print("Insufficient information {}!".format(p))
            else:
                print("Incorrectly identified ({}) {}!".format(computed, p))
    c = identified / file_count if file_count else 1
    print("Correct = {} ({} / {})".format(round(c, 3), identified, file_count))


def run(lang, is_test, indentifier=None, writer=None):
    """
    """
    info = LANG_INFO.get(lang)
    if info is None:
        print("Language {0} not found.".format(lang))
        return
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        
    os.makedirs(TEMP_DIR)
    (out, error) = subprocess.Popen(
        ["git", "clone", info["repo"]],
        cwd=TEMP_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()

    src_dir = os.path.join(TEMP_DIR, info["repo"].split("/")[-1].split(".")[0])
    if is_test and identifier:
        test_sig(src_dir, lang, info["ext"], indentifier)
    elif is_test:
        print("Please specify an identifier.")
    elif writer:
        writer(src_dir, lang=lang, ext=info["ext"], is_file=1)
    else:
        print("Please specify a writer.")
        
    shutil.rmtree(TEMP_DIR)
