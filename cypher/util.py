import codecs
import json
import re
import os
import io
import math

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from collections import Counter

EXTRACT_RE = r"""
    [\w]+\(?|
    ::| # C++, Haskell, Ruby, R, PHP
    =>| # C#, Rust, PHP
    <<(?!-)| # C++
    >>|
    :\n| # Python
    <-| # Haskell, R
    ->| # Haskell, Rust, PHP
    !!| # Haskell
    <<-| # R
    {-| # Haskell
    :=| # Go
    <%| # Ruby
    ===| # PHP
    !==| # PHP
    \s\.\s| # PHP
    &&| # PHP
    =~| # Perl
    \#if| # C#
    \[\]|
    \.\.\.|
    \.\.|
    \(\)|
    [~.@!?;:&\{\}\[\]\\#\/\|%\$`\*\)\(]
"""
STRING_RE = r"([\"\'])(?:(?=(\\?))\2.)*?\1"
BLOCK_COMMENTS = {
    r"^\/\*.*$": r"^.*\*\/$",
    r"^[\'\"]{3}.*$": r"^.*[\'\"]{3}$",
    r"^{-.*$": r"^.*-}$",
    r"^=.*$": r"^=.*$"
}
INLINE_COMMENTS = {
    "#": r"(?<!{-)#[^include|-].*(?!-})",
    "//": r"//.*",
    "--": r"--.*",
    "/*": r"/\*.*\*/",
    "{-": r"{-.*-}"
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
    limited_results = {}
    is_file = os.path.isfile(src)
    summary = get_tokens(src, is_file=is_file)
    sig = compute_signature(
        summary["tokens"], summary["lines"], summary["first_line"]
    )
    if not sig:
        return -1

    first_line = sig.get("first_line", [])
    for f in os.listdir(SIG_PATH):
        lang = f.split(".")[0]
        if not lang:
            continue
        ksig = read_signature(lang)
        results[lang] = compare_signatures(sig, ksig, summary["lines"])
        for regex in ksig.get("first_line", []):
            decoded = codecs.getdecoder("unicode_escape")(regex)[0]
            if re.match(decoded, first_line) or re.search(decoded, first_line):
                limited_results[lang] = results[lang]

    # print(first_line, limited_results)
    results = limited_results if limited_results else results
    if verbose:
        return {
            "results": results,
            "inline-comments": summary["inline_count"],
            "block-comments": summary["block_count"],
            "lines": summary["lines"]
        }
    else:
        return max(results, key=results.get)


def extract_content(src, is_file):
    """Return all non-comment and non-string content in src.
    """
    content = ""
    skip = regex = None
    count = inline = block = 0
    text = io.open(src, errors="ignore") if is_file else StringIO(src)

    for line in text:
        if count > 0:
            line = re.sub(STRING_RE, "", line)
        # Remove any inline comments.
        for c, r in INLINE_COMMENTS.items():
            if re.search(r, line):
                line = line[:line.find(c)] + "\n"
                inline += 1
                break

        skip = True
        for start, end in BLOCK_COMMENTS.items():
            if not regex and re.match(start, line):
                if start == end or not re.match(end, line):
                    # We've found the start of a multi-line comment.
                    regex = end
                    block += 1
                    break
            elif regex and re.match(regex, line):
                # We've found the end of a multi-line comment.
                regex = None
                break
        else:
            skip = regex

        if skip or not line.strip():
            # We're either in a multi-line comment or the line is blank.
            continue
        if line.strip():
            count += 1
            content += line

    text.close()
    return content, inline, block


def get_tokens(src, is_file=False, filtered=[]):
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
    content, inline, block = extract_content(src, is_file)
    text = StringIO(content)

    for line in text:
        if not line.strip():
            continue
        lines += 1
        if lines == 1:
            first_line = line.strip()
        extr = re.findall(EXTRACT_RE, line, re.VERBOSE)
        tokens.extend([s for s in extr if s in filtered or not filtered])

    text.close()
    return {
        "tokens": tokens,
        "lines": lines,
        "first_line": first_line,
        "inline_count": inline,
        "block_count": block
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
    for k, v in known.items():
        if k == "first_line":
            continue
        elif k == "unique":
            found += sum([2.5 if keyword in unknown else 0 for keyword in v])
        else:
            test_value = unknown.get(k)
            if test_value:
                total += math.fabs(v - test_value)
                found += 1
            elif v > 0.10:
                total += 1
                found -= 1
    return found / total


def compute_signature(tokens, lines, first_line, unique=None):
    """
    """
    if not tokens:
        return {}
    signature = Counter(tokens)
    for key in signature:
        signature[key] /= lines
    signature["first_line"] = first_line
    signature["unique"] = unique
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
    d = []
    if lang is None:
        return d, None

    with open(os.path.join(DATA_PATH, lang + ".json")) as jdata:
        d = json.load(jdata)
    tokens = sum([d.get(s, []) for s in d.keys()], [])
    return set(tokens), d.get("first_line"), d.get("unique", [])


def write_signature(src, lang, ext, is_file=True):
    """Write a signature for src.

    Args:
        src (str): A path to a directory.
        lang (str): The name of the language.
        ext (list): A list of file extensions associated with lang.
        is_file (bool): True if src is a file.
    """
    known, first_line, unique = get_lang_data(lang)
    tokens = []
    lines = 0.0

    for subdir, _, files in os.walk(src):
        for f in files:
            if ext and not any(f.endswith(e) for e in ext):
                continue
            summary = get_tokens(
                os.path.join(subdir, f),
                is_file=is_file,
                filtered=known
            )
            tokens.extend(summary["tokens"])
            lines += summary["lines"]

    data = compute_signature(tokens, lines, first_line, unique)
    with open(os.path.join(SIG_PATH, lang + ".json"), "w+") as sig:
        json.dump(data, sig, indent=4, sort_keys=True)
