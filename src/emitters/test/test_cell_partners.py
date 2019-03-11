import unittest

from ..cell_partners import *


class TestTowerData(unittest.TestCase):

    def test_generate_tower_docs(self):
        for i in generate_tower_docs():
            self.assertEqual(len(i), 21)
            break


if __name__ == '__main__':
    unittest.main()
