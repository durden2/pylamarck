from unittest import TestCase
from pylamarck.algorithms.random_sampling import RandomSampling
from pylamarck.termination import MaxSteps
from pylamarck.production import RandomSequenceSearch


class TestRandomSampling(TestCase):
    def test(self):
        search = RandomSampling(RandomSequenceSearch(range(10)), MaxSteps(20))
        x = search.solve(lambda i: (i - 5) ** 2)
        self.assertIn(x.g, range(10))
