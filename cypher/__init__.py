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
    BLOCK_IGNORES,
    INLINE_IGNORES,
    INLINE_STRING,
    INLINE_EXCEPTIONS,
    EXTRACT_RE,
    FILE_TERMINATORS
)

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
        return results
    else:
        return max(results, key=results.get)


def parse_filtered(filtered, results):
    """
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


def remove_inline_ignore(line):
    """
    """
    comments = {}
    without_string = re.sub(INLINE_STRING, "", line)
    char = idx = None

    for c, tup in INLINE_IGNORES.items():
        r = tup[0]
        if re.search(r, line) and re.search(r, without_string):
            if line.count(c) > 1:
                line = line.rsplit(c, 1)[0]
            exceptions = INLINE_EXCEPTIONS.get(c, [])
            if not any(re.search(p, line) for p in exceptions):
                comments[c] = line.find(c)
                idx = tup[1]

    if comments:
        char = min(comments, key=comments.get)
        line = line[:line.find(char)].strip() + "\n"

    return line, char, idx, len(re.findall(INLINE_STRING, line))


def extract_content(src, is_file):
    """Return all non-comment and non-string content in src.
    """
    content = ""
    comments = set()
    skip = regex = idx = None
    counts = [0] * 4  # [lines, inline, string, block]

    text = io.open(src, errors="ignore") if is_file else StringIO(src)
    for line in text:
        stripped = line.strip()
        if any(re.search(r, stripped) for r in FILE_TERMINATORS):
            break
        skip = True
        for c, r in BLOCK_IGNORES.items():
            if not regex and re.match(r[0], stripped):
                if not re.match(INLINE_IGNORES.get(c, r"$^")[0], stripped):
                    # We've found the start of a multi-line comment.
                    regex = r[1]
                    idx = r[2]
                    comments.add(c)
                    break
            elif regex and re.match(regex, stripped):
                # We've found the end of a multi-line comment.
                counts[idx] += 1
                regex = None
                break
        else:
            skip = regex

        if skip or not stripped:
            # We're either in a multi-line comment or the line is blank.
            continue

        line, char, idx, string_count = remove_inline_ignore(line)
        if char:
            comments.add(char)
            counts[idx] += 1
        counts[2] += string_count

        if counts[0] > 0:
            line = re.sub(INLINE_STRING, "", line)
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
    if PY2:
        text = StringIO(content.encode("utf-8"))
    else:
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
    if not tokens:
        return {}

    lines = lang_data.get("lines", 1)
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
    with open(os.path.join(SIG_PATH, lang + ".bin"), "rb") as sig:
        return msgpack.load(sig, encoding="utf-8")
