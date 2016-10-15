import os
import sys
import unittest

from codetype import (
    identify,
    remove_inline_ignore
)

sys.path.insert(0, os.path.abspath("."))
CONTENT_DIR = os.path.join("test", "content")
LANG_DIR = os.path.join("test", "lang")


class CodeTypeTestCase(unittest.TestCase):
    """Tests for codetype's utility functions.
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
            "var += 1 # This is a comments": ["var += 1", ["#"]],
            "foo # This is a nested -- comment": ["foo", ["#"]],
            "bar // another nested # comment": ["bar", ["//"]],
            "baz /* block-style inline */": ["baz", ["/*"]],
            "main() -- comment": ["main()", ["--"]],
            "baz {- block-style inline -}": ["baz", ["{-"]],
            'baz {- "block-style" inline -}': ["baz", ["{-"]],
            '"baz" {- "block-style" inline -}': ["", ["{-", '"']],
            "'baz' // {- block-style inline -}": ["", ["//", "'"]],
            '# the queue." (http://en)': ["", ["#"]],
            "# see http://docs.python.org/l#st": ["", ["#"]],
            "#--": ["", ["#"]],
            "print('foo', 'bar') # print!": ["print(, )", ["#", "'"]],
            "'''foo'''": ["", ["'''"]],
            'print("baz", \'foo\', "fo") // foo {- "block-style" # in -}': [
                "print(, , )", ["//", '"', "'"]
            ],
            "# FIRST LEARN ABOUT LISTS --": ["", ["#"]],
            '"git [ -- version]\n"': ["", ['"']],
            "## programmatically": ["", ["#"]],
            'printf("%s text", foo)': ["printf(, foo)", ['"']],
            'set the_phone_number to "424-354-3548"': [
                "set the_phone_number to", ['"']
            ],
            "(*    //   *  This *)": ["", ["(*"]],
            "'the `blank=True`'": ["", ["'"]],
            '"#{dir}/Payload/*.app"': ["", ['"']]
        }
        for case, output in cases.items():
            line, chars = remove_inline_ignore(case)
            try:
                self.assertCountEqual(chars, output[1])
            except AttributeError:
                self.assertItemsEqual(chars, output[1])
            self.assertEqual(line.strip(), output[0])

if __name__ == "__main__":
    unittest.main()
