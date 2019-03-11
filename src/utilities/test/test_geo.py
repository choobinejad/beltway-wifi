import unittest

from ..geo import *


class TestGeoUtilities(unittest.TestCase):

    def test_bad_gateway_polygon(self):
        # The whole story currently relies on this!
        self.assertEqual(
            bad_gateway_polygon,
            [
                [-77.045190, 39.004399], [-77.034190, 39.005399], [-77.003890, 39.000199],
                [-77.018490, 38.983399], [-77.047990, 38.986099], [-77.045190, 39.004399]
            ]
        )


if __name__ == '__main__':
    unittest.main()
