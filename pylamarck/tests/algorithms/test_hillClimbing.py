from unittest import TestCase
from pylamarck.algorithms.hill_climbing import HillClimbing
from pylamarck.termination import MaxSteps
from pylamarck.spaces.euclidean.production import RandomAdditiveMutation,\
    BoxConstraint, GaussianRn
from pylamarck.production import ConstantSearch
import random


class TestHillClimbing(TestCase):
    def test(self):
        random.seed(42)
        box_constr = BoxConstraint([-2.0, -2.0], [2.0, 2.0])
        ram = RandomAdditiveMutation(GaussianRn(2, 0.1),
                                     cond=box_constr.get_checker())
        search = HillClimbing(ConstantSearch([-1.0, 1.0]), ram, MaxSteps(100))
        x = search.solve(lambda t: (t[0] - 0.25) ** 2)
        self.assertAlmostEqual(x.g[0], 0.25, places=2)
