from unittest import TestCase
from pylamarck.spaces.euclidean.test_functions_rn import fsphere, frastrigin,\
    frosenn, fbeale, fhimmelblau, feggholder


class TestFunctionsRn(TestCase):
    def test(self):
        self.assertAlmostEqual(fsphere([0.0, 0.0]), 0.0)
        self.assertAlmostEqual(frastrigin([0.0, 0.0]), 0.0)
        self.assertAlmostEqual(frosenn([1.0, 1.0]), 0.0)
        self.assertAlmostEqual(fbeale([3.0, 0.5]), 0.0)
        self.assertAlmostEqual(fhimmelblau([3.0, 2.0]), 0.0)
        self.assertAlmostEqual(feggholder([512.0, 404.2319]), 1000.0-959.6407,
                               places=4)
