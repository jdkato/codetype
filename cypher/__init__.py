# coding: utf-8
import codecs
import io
import math
import os
import re
import sys

from collections import Counter
PY2 = sys.version_info <= (3,)
if PY2:
    from cStringIO import StringIO
else:
    from io import StringIO

import msgpack

from .re_globals import (
    EXTRACT_RE,
    STRING_RE,
    BLOCK_IGNORES,
    INLINE_COMMENTS,
    INLINE_STRINGS,
    INLINE_EXCEPTIONS,
    FILE_TERMINATORS
)

__version__ = "1.0.0"
FILE_PATH = os.path.dirname(os.path.realpath(__file__))
SIG_PATH = os.path.join(FILE_PATH, "signatures")


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
    summary = summarize_text(src, is_file=os.path.isfile(src))
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
        if all(r in ksig.get("ignores") for r in summary["ignores"]):
            filtered[0][lang] = results[lang]
        for regex in ksig.get("first_line", []):
            decoded = codecs.getdecoder("unicode_escape")(regex)[0]
            if re.search(decoded, first_line):
                filtered[1][lang] = results[lang]

    results = parse_filtered(filtered, results)
    if verbose:
        return results
    else:
        return max(results, key=results.get)


def parse_filtered(filtered, results):
    """Return the most refined version of results as possible.

    Args:
        filtered (list): A list of two dictionaries with results filtered by
            ignore and first line matches, respectively.
        results (dict): A dictionary with language names as keys and their
            scores as values.

    Returns:
        dict: Either `results` or one of the filtered dictionaries.

    Examples:
        >>> filtered = [{'Python': 4, 'Ruby': 4}, {'Python': 4, 'Perl': 3}]
        >>> results = {'Python': 4, 'Ruby': 4, 'Perl': 3}
        >>> parse_filtered(filtered, results)
        {'Python': 4}
        >>>
    """
    d = {}
    if all(f for f in filtered):
        for lang in [x for x in filtered[0] if x in filtered[1]]:
            d[lang] = filtered[0][lang]
        if not d:
            filtered[0].update(filtered[1])
            d = filtered[0]
    else:
        d = filtered[0] or filtered[1]
    return d or results


def remove_strings(line):
    """Remove strings from line.

    Args:
        lines (str): A line of text.

    Returns:
        (str, list): `line` with its strings removed, if any were present, and
            a list containing the characters removed.

    Examples:
        >>> remove_strings('print("Hello, world!")')
        ('print()', ['"'])
        >>> remove_strings('print("Hello", \'world\')')
        ('print(, )', ['"', "'"])
    """
    char_to_pos = {}
    chars = []
    for c, regex in INLINE_STRINGS.items():
        expt = any(re.search(r, line) for r in INLINE_EXCEPTIONS.get(c, []))
        if not expt and re.search(regex, line):
            char_to_pos[c] = line.find(c)

    for c in sorted(char_to_pos, key=char_to_pos.get):
        regex = INLINE_STRINGS.get(c)
        if re.search(regex, line):
            line = re.sub(regex, "", line)
            chars.append(c)
    return line, chars


def remove_comment(line):
    """Remove comments from line.

    Args:
        lines (str): A line of text.

    Returns:
        (str, str): `line` with its comments removed, if any were present, and
            the character removed.

    Examples:
        >>> remove_comment('print("Hello") # this is a comment')
        ('print("Hello")', '#')
        >>> remove_comment('printf("Hello") // # another')
        ('printf("Hello")', '//')
    """
    char_to_pos = {}
    char = None
    wos_line = line
    for r in INLINE_STRINGS.values():
        if re.search(r, line):
            wos_line = re.sub(r, "", line)

    for c, regex in INLINE_COMMENTS.items():
        if line.count(c) > 1:
            line = line[:line.rfind(c)].strip()
        expt = any(re.search(r, line) for r in INLINE_EXCEPTIONS.get(c, []))
        if not expt and re.search(regex, line) and re.search(regex, wos_line):
            char_to_pos[c] = line.find(c)

    if char_to_pos:
        char = min(char_to_pos, key=char_to_pos.get)
        line = line[:line.find(char)].strip()
    return line, char


def remove_inline_ignore(line):
    """Return line without comments and strings.
    """
    line, comment_char = remove_comment(line)
    line, strings = remove_strings(line)
    if comment_char:
        strings.append(comment_char)
    return line.strip(), strings


def summarize_text(src, is_file=False, filtered=None):
    """Return all non-comment and non-string content in src.
    """
    lines = 0.0
    toks, ignores = [], []
    skip, regex, first = None, None, None
    text = io.open(src, errors="ignore") if is_file else StringIO(src)
    for line in text:
        if any(re.search(r, line) for r in FILE_TERMINATORS):
            break
        skip = True
        for c, r in BLOCK_IGNORES.items():
            if not regex and re.search(r[0], line):
                is_comment = re.search(INLINE_COMMENTS.get(c, r"$^"), line)
                is_string = re.search(STRING_RE, line)
                is_inline = re.search(INLINE_STRINGS.get(c, r"$^"), line)
                if not is_comment and not is_string and not is_inline:
                    # We've found the start of a block ignore.
                    regex = r[1]
                    ignores.append(c)
                    break
            elif regex and re.search(regex, line):
                # We've found the end of a block ignore.
                regex = None
                break
        else:
            skip = regex

        if skip or not line.strip():
            # We're either in a block ignore or the line is blank.
            continue

        line, chars = remove_inline_ignore(line)
        ignores.extend(chars)
        if line:
            lines += 1
            if lines == 1:
                first = line
            extr = re.findall(EXTRACT_RE, line, re.VERBOSE)
            toks.extend([s for s in extr if not filtered or s in filtered])

    text.close()
    return {
        "tokens": toks, "lines": lines, "first_line": first,
        "ignores": set(ignores)
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
        if k in ["first_line", "ignores"]:
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
    """Compute a 'signature' using `lang_data`.

    Args:
        lang_data (dict): A dictionary containing the extracted tokens, the
            text's first line, a list of ignored characters and, if provided,
            the language's flags and unique tokens.

    Returns:
        dict: The computed signature.
    """
    tokens = lang_data.get("tokens")
    if not tokens:
        return {}

    lines = lang_data.get("lines", 1)
    signature = Counter(tokens)
    for key in signature:
        signature[key] /= lines

    signature["first_line"] = lang_data.get("first_line")
    signature["unique"] = lang_data.get("unique", [])
    signature["ignores"] = lang_data.get("ignores")
    signature["flags"] = lang_data.get("flags", [])
    return signature


def read_signature(lang):
    """Load an existing signature.

    Args:
        lang (str): The name of the existing signature.
    """
    with open(os.path.join(SIG_PATH, lang + ".bin"), "rb") as sig:
        return msgpack.load(sig, encoding="utf-8")
