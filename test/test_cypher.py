import os
import sys
import unittest

from cypher.util import identify

sys.path.insert(0, os.path.abspath("."))
LANG_DIR = os.path.join("test", "lang")


class CypherTestCase(unittest.TestCase):
    """
    """
    def test_identify(self):
        """
        """
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


if __name__ == "__main__":
    unittest.main()
