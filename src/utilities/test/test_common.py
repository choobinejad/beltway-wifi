import unittest

from ..common import *


class TestCommonUtilities(unittest.TestCase):

    def test_frange_step_size(self):
        self.assertEqual(
            len(list(frange(0, 1, .01))),
            100
        )

    def test_frange_nonpositive(self):
        l = list(frange(-1, 1, .01))
        self.assertEqual(l[0], -1)
        self.assertEqual(l[-1], 0.99)

    def test_progress_bar(self):
        p = progress(50, 100, status='test_status', visual=False)
        self.assertEqual(
            p,
            '[==================================================--------------------------------------------------]'
            ' 50.0% ...test_status\r'
        )


if __name__ == '__main__':
    unittest.main()
