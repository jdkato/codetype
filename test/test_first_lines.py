import os
import sys
import re
import json
import unittest

from codecs import getdecoder

sys.path.insert(0, os.path.abspath("."))
REGEXP_DIR = os.path.join("test", "lang", "regexp")


class FirstLinesTestCase(unittest.TestCase):
    """Tests for codetype's utility functions.
    """
    def test_identify(self):
        unicode_escape = getdecoder("unicode_escape")
        for test in os.listdir(REGEXP_DIR):
            if test.endswith(".json"):
                with open(os.path.join(REGEXP_DIR, test)) as data_file:
                    data = json.load(data_file)
                for key in data:
                    regexp = unicode_escape(key)[0]
                    accepted = data[key]["accepted"]
                    unaccepted = data[key]["unaccepted"]
                    for s in accepted:
                        self.assertTrue(
                            re.search(regexp, s),
                            msg="'{0}' does not match '{1}'".format(regexp, s)
                        )
                    for s in unaccepted:
                        self.assertFalse(
                            re.search(regexp, s),
                            msg="'{0}' matches '{1}'".format(regexp, s)
                        )

if __name__ == "__main__":
    unittest.main()
