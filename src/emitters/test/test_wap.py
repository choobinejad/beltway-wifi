import unittest

from ..wap import *


class TestWapCreation(unittest.TestCase):

    def test_generate_wap_points(self):
        x = list(generate_wap_points())
        # Ensure method of wap point generation has not changed significantly
        self.assertEqual(x[0], (1, [-77.3, 38.7]))
        self.assertEqual(x[-1], (22378, [-76.80199, 39.099]))
        self.assertEqual(len(x), 22378)

    def test_generate_wap_docs(self):
        x = list(generate_wap_docs())
        # Ensure method of generating wap records has not changed significantly
        self.assertEqual(len(x), 22378)
        self.assertEqual(len(x[0]), 9)


if __name__ == '__main__':
    unittest.main()
