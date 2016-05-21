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
    \.\.\.|
    \(\)|
    [.@!?;:&\{\}\[\]\\#\/\|%\$`\*]
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
    sig = compute_signature(src, is_file=is_file)
    if sig == -1:
        return sig

    for f in os.listdir(SIG_PATH):
        lang = f.split(".")[0]
        if not lang:
            continue
        ksig = read_signature(lang)
        results[lang] = compare_signatures(sig, ksig)

    if verbose:
        return results
    else:
        return max(results, key=results.get)


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

    if is_file:
        text = open(src)
    else:
        text = StringIO(src)

    for line in text:
        line = line.lstrip()
        if not line or any(line.startswith(c) for c in COMMENTS):
            continue
        for c in INLINE_COMMENTS:
            if c in line:
                line = line[:line.find(c)]
        line = re.sub(STRING_RE, '', line)
        extr = re.findall(EXTRACT_RE, line, re.VERBOSE)
        parts.extend([s for s in extr if s in filtered or not filtered])
        lines += 1

    text.close()
    return parts, lines


def compare_signatures(unknown, known):
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
    lines = 0
    parts = []
    words = set(get_lang_data(lang))
    if not os.path.isdir(src):
        sparts, slines = get_parts(src, is_file=is_file, filtered=words)
        parts.extend(sparts)
        lines += slines
    else:
        for subdir, dirs, files in os.walk(src):
            for f in files:
                if ext and not any(f.endswith(e) for e in ext):
                    continue
                sparts, slines = get_parts(
                    os.path.join(subdir, f),
                    is_file=is_file,
                    filtered=words
                )
                parts.extend(sparts)
                lines += slines

    if not parts:
        return -1
    signature = Counter(parts)
    for key in signature:
        signature[key] /= lines
    return signature


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
        return d
    with open(os.path.join(DATA_PATH, lang + ".json")) as jdata:
        d = json.load(jdata)
    return sum([d[s] for s in d.keys()], [])


def write_signature(src, lang, ext, is_file=True):
    """Write a signature for `src`.

    Args:
        `src` (str): Either a string or a file path.
        `lang` (str): The name of the language.
        `ext` (list): A list of file extensions associated with `lang`.
        `is_file` (bool): `True` if `src` is a file.
    """
    data = compute_signature(src, lang=lang, ext=ext, is_file=is_file)
    with open(os.path.join(SIG_PATH, lang + ".json"), "w+") as sig:
        json.dump(data, sig, indent=4, sort_keys=True)
