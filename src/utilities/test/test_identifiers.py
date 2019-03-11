import unittest
import re

from ..identifiers import *


class TestIdentifierUtilities(unittest.TestCase):

    def test_generate_mac_address_random(self):
        mac = generate_mac_address()
        self.assertRegex(mac, '^([0-9a-f]{2}:){5}[0-9a-f]{2}$')

    def test_generate_mac_address_oui(self):
        oui = 'ab:ab:ab'
        mac = generate_mac_address(oui)
        self.assertRegex(mac, '^' + oui + ':([0-9a-f]{2}:){2}[0-9a-f]{2}$')

    def test_generate_mac_address_ordinal(self):
        mac = generate_mac_address(ordinal=116)
        self.assertEqual(mac, '00:00:00:00:00:74')

    def test_generate_mac_address_oui_and_ordinal(self):
        oui = 'ab:ab:ab'
        mac = generate_mac_address(oui, 116)
        self.assertEqual(mac, oui + ':00:00:74')


if __name__ == '__main__':
    unittest.main()
