# encoding=utf8
import codecs
import io
import json
import math
import os
import re
import sys

from collections import Counter

try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except NameError:
    pass

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

__all__ = ["identify"]

EXTRACT_RE = r"""
    [@|#]?[\w]+\(?|
    \+\+| # Scala
    :::| # Scala
    ::~| # C++
    ::| # C++, Haskell, Ruby, R, PHP
    =>| # C#, Rust, PHP
    <<(?!-)| # C++
    >>| # C++
    :\n| # Python
    <-| # Haskell, R
    ->| # Haskell, Rust, PHP
    !!| # Haskell
    <<-| # R
    {-| # Haskell
    :=| # Go
    <%| # Ruby
    %w| # Ruby
    ===| # PHP
    !==| # PHP
    \s\.\s| # PHP, Perl
    &&| # PHP
    =~| # Perl
    ~=| # Lua
    !\(| # Rust
    \[\]| # Java
    \.\.\.| # R
    \.\.| # Haskell
    \(\)| # Haskell
    \$_| # PHP
    \#\[| # Rust
    [~.@!?;:&\{\}\[\]\\#\/\|%\$`\*\)\(-,+]
"""
STRING_RE = r"([\"\'])(?:(?=(\\?))\2.)*?\1"
BLOCK_COMMENTS = {
    "/*": [r"^\/\*.*$", r"^.*\*\/$"],
    "/+": [r"^\/\+.*$", r"^.*\+\/$"],
    "'''": [r"^[\']{3}.*$", r"^.*[\']{3}$"],
    '"""': [r"^[\"]{3}.*$", r"^.*[\"]{3}$"],
    "{-": [r"^{-.*$", r"^.*-}$"],
    "=": [r"^=.*$", r"^=.*$"],
    "--[[": [r"^-{2,}\[{1,3}(.*)?$", r"^-{2,}\]{1,3}(.*)?$"]
}
INLINE_COMMENTS = {
    "#": r"(?<!{-)#(?!-}|include|!|define|if|el|endif|import).*",
    "//": r"\/\/.*",
    "--": r"(?<!\w)--.*",
    "/*": r"/\*.*\*/",
    "/+": r"/\+.*\+/",
    "{-": r"{-.*-}",
    "'''": r"^'{3}.*'{3}$",
    '"""': r'^"{3}.*"{3}$'
}
FILE_PATH = os.path.dirname(os.path.realpath(__file__))
SIG_PATH = os.path.join(FILE_PATH, "signatures")
DATA_PATH = os.path.join(FILE_PATH, "data")


def identify(src, verbose=False):
    """Attempt to identify the language which src is written in.
    Args:
        src (str): Either a string or a file path.
        verbose (bool): True if verbose output is to be used.
    Returns:
        (str|dict): A string specifying the computed language if verbose is
            False. Otherwise a dictionary with all tested languages as keys
            and their computed scores as values.
    """
    results = {}
    filtered = [{}, {}]
    summary = get_text_summary(src, is_file=os.path.isfile(src))
    sig = compute_signature(summary)
    if not sig:
        return -1

    first_line = sig.get("first_line", [])
    for f in os.listdir(SIG_PATH):
        lang = f.split(".")[0]
        if not lang:
            continue
        ksig = read_signature(lang)
        results[lang] = compare_signatures(sig, ksig, summary["lines"])
        if all(r in ksig.get("comments") for r in summary["comments"]):
            filtered[0][lang] = results[lang]
        for regex in ksig.get("first_line", []):
            decoded = codecs.getdecoder("unicode_escape")(regex)[0]
            if re.search(decoded, first_line):
                filtered[1][lang] = results[lang]

    results = parse_filtered(filtered, results)
    if verbose:
        return {
            "results": results, "block_count": summary["counts"][3],
            "inline_count": summary["counts"][1],
            "string_count": summary["counts"][2]
        }
    else:
        return max(results, key=results.get)


def parse_filtered(filtered, results):
    """
    """
    if all(f for f in filtered):
        d = {}
        for lang in [x for x in filtered[0] if x in filtered[1]]:
            d[lang] = filtered[0][lang]
    else:
        d = filtered[0] or filtered[1]
    return d or results


def remove_inline_comment(line):
    """
    """
    comments = {}
    without_string = re.sub(STRING_RE, "", line)
    char = False

    for c, r in INLINE_COMMENTS.items():
        if re.search(r, line) and re.search(r, without_string):
            comments[c] = line.find(c)

    if comments:
        char = min(comments, key=comments.get)
        line = line[:line.find(char)].strip() + "\n"
        without_string = re.sub(STRING_RE, "", line)

    return line, char, line != without_string


def extract_content(src, is_file):
    """Return all non-comment and non-string content in src.
    """
    content = ""
    comments = set()
    skip = regex = None
    counts = [0] * 4

    try:
        text = io.open(src, errors="ignore") if is_file else StringIO(src)
    except IOError:
        print("IOError: {}".format(src))
        return content, comments, counts

    for line in text:
        skip = True
        for c, r in BLOCK_COMMENTS.items():
            if not regex and re.match(r[0], line.strip()):
                if not re.match(INLINE_COMMENTS.get(c, r"^$"), line.strip()):
                    # We've found the start of a multi-line comment.
                    regex = r[1]
                    comments.add(c)
                    break
            elif regex and re.match(regex, line.strip()):
                # We've found the end of a multi-line comment.
                counts[3] += 1
                regex = None
                break
        else:
            skip = regex

        if skip or not line.strip():
            # We're either in a multi-line comment or the line is blank.
            continue

        line, char, string_found = remove_inline_comment(line)
        if char:
            comments.add(char)
        counts[1] += int(bool(char))
        counts[2] += int(bool(string_found))

        if counts[0] > 0:
            line = re.sub(STRING_RE, "", line)
        if line.strip():
            counts[0] += 1
            content += line

    text.close()
    return content, comments, counts


def get_text_summary(src, is_file=False, filtered=None):
    """Extract all tokens from src.
    Args:
        src (str): Either a string or a file path.
        is_file (bool): True if src is a file.
        filtered (list): A list of strings indicating tokens to look for in
            src. If provided, any tokens not in filtered will be ignored.
    Returns:
        (tuple): (tokens, lines, first_line).
    """
    lines = 0.0
    tokens = []
    first_line = None
    content, comments, counts = extract_content(src, is_file)

    text = StringIO(content)
    for line in text:
        if not line.strip():
            continue
        lines += 1
        if lines == 1:
            first_line = line.strip()
        extr = re.findall(EXTRACT_RE, line, re.VERBOSE)
        tokens.extend([s for s in extr if not filtered or s in filtered])
    text.close()

    return {
        "tokens": tokens, "lines": lines, "first_line": first_line,
        "counts": counts, "comments": comments
    }


def compare_signatures(unknown, known, lines):
    """Compare two signatures using only the keys in known.
    Args:
        unknown (dict): A signature for an unknown language.
        known (dict): A signature for a known language.
    Returns:
        float: A score indicating how closely unknown resembled known.
    """
    total = 1.0
    found = 0.0
    mult = 2 if lines < 15 else 1

    for k, v in known.items():
        if k in ["first_line", "comments"]:
            continue
        elif k == "unique":
            inc = 4 * mult
            found += sum([inc if token in unknown else 0 for token in v])
        elif k == "flags":
            found -= sum([4 if token in unknown else 0 for token in v])
        else:
            test_value = unknown.get(k)
            if test_value:
                total += math.fabs(v - test_value)
                found += 1
            elif v > 0.10:
                total += 1
                found -= 1

    return round(found / total, 3)


def compute_signature(lang_data):
    """
    """
    tokens = lang_data.get("tokens")
    lines = lang_data.get("lines")
    if not tokens:
        return {}
    signature = Counter(tokens)
    for key in signature:
        signature[key] /= lines
    signature["first_line"] = lang_data.get("first_line")
    signature["unique"] = lang_data.get("unique", [])
    signature["comments"] = lang_data.get("comments")
    signature["flags"] = lang_data.get("flags", [])
    return signature


def read_signature(lang):
    """Load an existing signature.
    Args:
        lang (str): The name of the existing signature.
    """
    with open(os.path.join(SIG_PATH, lang + ".json")) as sig:
        return json.load(sig)


def get_lang_data(lang):
    """Load existing data on lang.
    Args:
        lang (str): The name of the language.
    Returns:
        list: A list of all keywords associated with lang.
    """
    d = {}
    tokens = []
    if lang is None:
        return d, None, None, None

    with open(os.path.join(DATA_PATH, lang + ".json")) as jdata:
        d = json.load(jdata)

    for k, v in d.items():
        if k not in ["comments", "first_line"]:
            tokens.extend(v)
    tokens = set(tokens)

    return tokens, d


def write_signature(src, lang, ext, is_file=True):
    """Write a signature for src.
    Args:
        src (str): A path to a directory.
        lang (str): The name of the language.
        ext (list): A list of file extensions associated with lang.
        is_file (bool): True if src is a file.
    """
    known, lang_data = get_lang_data(lang)
    tokens = []
    lines = 0.0

    for subdir, _, files in os.walk(src):
        for f in files:
            if ext and not any(f.endswith(e) for e in ext):
                continue
            summary = get_text_summary(
                os.path.join(subdir, f),
                is_file=is_file,
                filtered=known
            )
            tokens.extend(summary["tokens"])
            lines += summary["lines"]

    lang_data["tokens"] = tokens
    lang_data["lines"] = lines
    data = compute_signature(lang_data)
    with open(os.path.join(SIG_PATH, lang + ".json"), "w+") as sig:
        json.dump(data, sig, indent=4, sort_keys=True)
