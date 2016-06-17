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
            "var += 1 # This is a comments": "var += 1",
            "foo # This is a nested -- comment": "foo",
            "bar // another nested # comment": "bar",
            "baz /* block-style inline */": "baz",
            "main() -- comment": "main()",
            "baz {- block-style inline -}": "baz",
        }
        for case, output in cases.items():
            removed = remove_inline_comment(case)[0].strip()
            self.assertEqual(removed, output)


if __name__ == "__main__":
    unittest.main()
