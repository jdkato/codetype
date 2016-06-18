import os
import sys
import unittest

from cypher.util import (
    identify,
    remove_inline_comment
)

sys.path.insert(0, os.path.abspath("."))
LANG_DIR = os.path.join("test", "lang")


class CypherTestCase(unittest.TestCase):
    """Tests for cypher's utility functions.
    """
    def test_identify(self):
        for subdir, dirs, files in os.walk(LANG_DIR):
            known = os.path.basename(subdir)
            if known == "lang":
                continue
            count = 0
            for f in files:
                if f.endswith(".txt"):
                    count += 1
                    computed = identify(os.path.join(subdir, f))
                    self.assertEqual(known, computed)
            print("Tested {} {} files.".format(count, known))

    def test_remove_inline_comment(self):
        cases = {
            "var += 1 # This is a comments": ["var += 1", "#", False],
            "foo # This is a nested -- comment": ["foo", "#", False],
            "bar // another nested # comment": ["bar", "//", False],
            "baz /* block-style inline */": ["baz", "/*", False],
            "main() -- comment": ["main()", "--", False],
            "baz {- block-style inline -}": ["baz", "{-", False],
            "baz {- block-style 'inline' -}": ["baz", "{-", False],
            'baz {- "block-style" inline -}': ["baz", "{-", False],
            '"baz" {- "block-style" inline -}': ['"baz"', "{-", True],
            "'baz' // {- block-style inline -}": ["'baz'", "//", True],
        }
        for case, output in cases.items():
            removed, char, string_found = remove_inline_comment(case)
            self.assertEqual(removed.strip(), output[0])
            self.assertEqual(char, output[1])
            self.assertEqual(string_found, output[2])


if __name__ == "__main__":
    unittest.main()
