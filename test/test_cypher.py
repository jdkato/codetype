import os
import sys
import unittest

from cypher.util import identify, extract_content

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
            if known != "lang":
                print("Testing {} ...".format(known))
            for f in files:
                if f.endswith(".txt"):
                    computed = identify(os.path.join(subdir, f))
                    self.assertEqual(known, computed)
                    
    def test_extract_content(self):
        """
        """
        cases = {
            "print('I am a string')": "print()",
            "cout << 'I am another string' << endl;": "cout <<  << endl;",
            "print('foo')  # Inline comment": "print()",
            "printf('%d', 2) // Inline comment": "printf(, 2)",
            "test += 1": "test += 1"
        }
        for line, output in cases.items():
            self.assertEqual(output, extract_content(line))
            


if __name__ == "__main__":
    unittest.main()
