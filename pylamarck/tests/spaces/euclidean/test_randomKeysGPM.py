from unittest import TestCase
from pylamarck.spaces.euclidean.production import RandomKeysGPM


class TestRandomKeysGPM(TestCase):
    def test1(self):
        rk1 = RandomKeysGPM(4)
        result = rk1([0.2, 0.1, 5.0, 4.0])
        self.assertListEqual(result, [1, 0, 3, 2])

        rk2 = RandomKeysGPM(4, ['a', 'b', 'c', 'd'])
        result = rk2([0.2, 0.1, 5.0, 4.0])
        self.assertListEqual(result, ['b', 'a', 'd', 'c'])
