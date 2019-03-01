from unittest import TestCase
from pylamarck.algorithms.hill_climbing import HillClimbing
from pylamarck.termination import MaxSteps
from pylamarck.spaces.euclidean.production import RandomAdditiveMutation,\
    BoxCond, GaussianRn
from pylamarck.production import ConstantSearch
import random


class TestHillClimbing(TestCase):
    def test(self):
        random.seed(42)
        ram = RandomAdditiveMutation(GaussianRn(2, 0.1),
                                     cond=BoxCond([-2.0, -2.0], [2.0, 2.0]))
        search = HillClimbing(ConstantSearch([-1.0, 1.0]), ram, MaxSteps(100))
        x = search.solve(lambda t: (t[0] - 0.25) ** 2)
        self.assertAlmostEqual(x.g[0], 0.25, places=2)
