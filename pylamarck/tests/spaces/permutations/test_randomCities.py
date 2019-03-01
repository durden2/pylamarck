from unittest import TestCase
from pylamarck.spaces.permutations.test_functions_tsp import RandomCities
from pylamarck.spaces.permutations.production import RandomPermutation


class TestRandomCities(TestCase):
    def test(self):
        n = 10
        rand_min = -30.0
        rand_max = 30.0
        rc = RandomCities(n=n, rand_min=rand_min, rand_max=rand_max)
        self.assertEqual(len(rc._cities), n)
        for i in range(n):
            self.assertAlmostEqual(rc.dist(i, i), 0.0)
        random_perm = RandomPermutation(n)
        self.assertTrue(rc(random_perm()) >= 0.0)
