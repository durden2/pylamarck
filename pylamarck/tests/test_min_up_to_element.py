from unittest import TestCase
from pylamarck.logging import min_up_to_element


class TestMinUpToElement(TestCase):
    def test_min_up_to_element(self):
        l = [10.0, 9.0, 11.0, 8.0, 14.0, 15.0, 2.0]
        l_expected = [10.0, 9.0, 9.0, 8.0, 8.0, 8.0, 2.0]
        l_received = min_up_to_element(l)
        self.assertListEqual(l_expected, l_received)
