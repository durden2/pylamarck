from unittest import TestCase
from pylamarck.spaces.permutations.production import PermutationSingleSwap
from pylamarck.individual import Individual


class TestPermutationSingleSwap(TestCase):
    def test(self):
        pss = PermutationSingleSwap(2)
        g = [1, 2]
        permuted = pss(Individual(g, g, 0.0))
        self.assertEqual(permuted, [2, 1])
