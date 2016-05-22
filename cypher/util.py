import json
import re
import os
import math

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from collections import Counter

EXTRACT_RE = r"""
    [\w]+\(?|
    ::|
    =>|
    <<(?!-)|
    :\n|
    <-|
    ->|
    !!|
    <<-|
    {-|
    :=|
    <%|
    \[\]|
    \.\.\.|
    \(\)|
    [.@!?;:&\{\}\[\]\\#\/\|%\$`\*\)\(]
"""
STRING_RE = r"([\"\'])(?:(?=(\\?))\2.)*?\1"
COMMENTS = ["/", "//", "-", "#", "*"]
INLINE_COMMENTS = ["//", "#", "--"]
FILE_PATH = os.path.dirname(os.path.realpath(__file__))
SIG_PATH = os.path.join(FILE_PATH, "signatures")
DATA_PATH = os.path.join(FILE_PATH, "data")


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
    results = {}
    ksigs = {}
    limited_results = {}
    sig, lines = compute_signature(src, is_file=is_file)
    if not sig:
        return -1

    for f in os.listdir(SIG_PATH):
        lang = f.split(".")[0]
        if not lang:
            continue
        ksig = read_signature(lang)
        results[lang] = compare_signatures(sig, ksig, lines)
        ksigs[lang] = ksig

    fl = sig.get("first_line")
    print(fl)
    for lang, ksig in ksigs.items():
        kfl = ksig.get("first_line")
        if any(l in fl for l in kfl):
            limited_results[lang] = results[lang]

    print(limited_results if limited_results else None)
    results = limited_results if limited_results else results
    if verbose:
        return results
    else:
        return max(results, key=results.get)


def extract_content(line):
    """Attempt to ignore comments and strings.
    """
    line = line.lstrip()
    if not line or any(line.startswith(c) for c in COMMENTS):
        if "#include" not in line:  # FIXME: Use patterns instead?
            return None
    line = re.sub(STRING_RE, '', line).strip()
    for c in INLINE_COMMENTS:
        if c in line and "#include" not in line:
            line = line[:line.find(c)]
    return line


def get_parts(src, is_file=False, filtered=[]):
    """Attempt to extract all non-string and non-comment content from `src`.

    Args:
        `src` (str): Either a string or a file path.
        `is_file` (bool): `True` if `src` is a file.
        `filtered` (list): A list of words to keep (others will be ignored).

    Returns:
     (list, int): The list of extracted content and the total number of lines
        examined.
    """
    lines = 0.0
    parts = []
    first_line = None

    if is_file:
        text = open(src)
    else:
        text = StringIO(src)

    for line in text:
        line = extract_content(line)
        if not line:
            continue
        lines += 1
        if lines == 1.0:
            first_line = line
        extr = re.findall(EXTRACT_RE, line, re.VERBOSE)
        parts.extend([s for s in extr if s in filtered or not filtered])

    text.close()
    return parts, lines, first_line


def compare_signatures(unknown, known, lines):
    """Compare two signatures using only the keys in `known`.

    Args:
        `unknown` (dict): A signature for an unknown language.
        `known` (dict): A signature for a known language.

    Returns:
        float: A score indicating how closely `unknown` resembled `known`
    """
    total = 1.0
    found = 0.0
    for k, v in known.items():
        if k == "first_line":
            continue
        test_value = unknown.get(k)
        if test_value:
            total += math.fabs(v - test_value)
            found += 1
        elif v > 0.10:
            total += 1
            found -= 1
    return found / total


def compute_signature(src, lang=None, ext=[], is_file=False):
    """Compute a signature for `src`.

    Args:
        `src` (str): Either a string or a file path.
        `is_file` (bool): `True` if `src` is a file.
        `lang` (str): The name of the language `src` is written in.
        `ext` (list): A list of file extensions associated with `lang`.

    Returns:
     dict: A dictionary with words as keys and their frequency per line as
        values in `src`.
    """
    words, first_line = get_lang_data(lang)
    if not os.path.isdir(src):
        parts, lines, sfirst = get_parts(src, is_file=is_file, filtered=words)
    else:
        parts = []
        lines = 0.0
        for subdir, dirs, files in os.walk(src):
            for f in files:
                if ext and not any(f.endswith(e) for e in ext):
                    continue
                sparts, slines, sfirst = get_parts(
                    os.path.join(subdir, f),
                    is_file=is_file,
                    filtered=set(words)
                )
                parts.extend(sparts)
                lines += slines
    if not parts:
        return {}, 0

    signature = Counter(parts)
    for key in signature:
        signature[key] /= lines

    if lang:
        signature["first_line"] = first_line
    else:
        signature["first_line"] = sfirst
    return signature, lines


def read_signature(lang):
    """Load an existing signature.

    Args:
        `lang` (str): The name of the existing signature.
    """
    with open(os.path.join(SIG_PATH, lang + ".json")) as sig:
        return json.load(sig)


def get_lang_data(lang):
    """Load existing data on `lang`.

    Args:
        `lang` (str): The name of the language.

    Returns:
        list: A list of all keywords associated with `lang`.
    """
    d = []
    if lang is None:
        return d, None
    with open(os.path.join(DATA_PATH, lang + ".json")) as jdata:
        d = json.load(jdata)

    words = sum([d.get(s, []) for s in d.keys()], [])
    return set(words), d.get("first")


def write_signature(src, lang, ext, is_file=True):
    """Write a signature for `src`.

    Args:
        `src` (str): Either a string or a file path.
        `lang` (str): The name of the language.
        `ext` (list): A list of file extensions associated with `lang`.
        `is_file` (bool): `True` if `src` is a file.
    """
    data, _ = compute_signature(src, lang=lang, ext=ext, is_file=is_file)
    with open(os.path.join(SIG_PATH, lang + ".json"), "w+") as sig:
        json.dump(data, sig, indent=4, sort_keys=True)
