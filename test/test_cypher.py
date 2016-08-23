import os
import sys
import unittest

from cypher import (
    identify,
    remove_inline_ignore,
    extract_content
)

sys.path.insert(0, os.path.abspath("."))
CONTENT_DIR = os.path.join("test", "content")
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
                    self.assertEqual(
                        known, computed,
                        msg="{0} != {1} ({2})".format(known, computed, f)
                    )
            print("Tested {} {} files.".format(count, known))

    def test_remove_inline_ignore(self):
        cases = {
            "var += 1 # This is a comments": ["var += 1", "#", False],
            "foo # This is a nested -- comment": ["foo", "#", False],
            "bar // another nested # comment": ["bar", "//", False],
            "baz /* block-style inline */": ["baz", "/*", False],
            "main() -- comment": ["main()", "--", False],
            "baz {- block-style inline -}": ["baz", "{-", False],
            "baz {- block-style 'inline' -}": ["baz", "{-", False],
            'baz {- "block-style" inline -}': ["baz", "{-", False],
            '"baz" {- "block-style" inline -}': ['"baz"', "{-", 1],
            "'baz' // {- block-style inline -}": ["'baz'", "//", 1],
            '# the queue." (http://en)': ['', "#", False],
            '# see http://docs.python.org/l#st': ['', '#', False],
            '#--': ['', '#', False],
            "print('foo', 'bar') # print!": ["print('foo', 'bar')", "#", 2],
            "'''foo'''": ['', "'''", False]
        }
        for case, output in cases.items():
            removed, char, idx, string_count = remove_inline_ignore(case)
            self.assertEqual(char, output[1])
            self.assertEqual(removed.strip(), output[0])
            self.assertEqual(string_count, output[2])

    def test_extract_content(self):
        cases = {
            'case1.txt': [{'r#"'}, [7, 0, 2, 0]],
            'case2.txt': [{"'''"}, [1, 0, 4, 0]]
        }
        for case, output in cases.items():
            path = os.path.join(CONTENT_DIR, case)
            content, comments, counts = extract_content(path, True)
            self.assertEqual(comments, output[0])
            self.assertEqual(counts, output[1])


if __name__ == "__main__":
    unittest.main()
