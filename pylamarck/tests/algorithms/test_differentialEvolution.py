from unittest import TestCase
from pylamarck.algorithms.differential_evolution import DifferentialEvolution
from pylamarck.termination import MaxSteps
from pylamarck.spaces.euclidean.production import DifferentialRecombination,\
    BoxConstraint
from pylamarck.spaces.euclidean.production import RandomUniformSearch
import random


class TestDifferentialEvolution(TestCase):
    def test(self):
        random.seed(42)
        box_constr = BoxConstraint([-2.0, -2.0], [2.0, 2.0])
        strength = 0.2
        tso = DifferentialRecombination(strength, box_constr.get_fixer())
        nso = RandomUniformSearch(box_constr.ai, box_constr.bi)
        search = DifferentialEvolution(nso=nso,
                                       n0=5,
                                       tso=tso,
                                       term=MaxSteps(100))

        def f(t):
            return (t[0] - 0.25) ** 2

        x = search.solve(f)
        self.assertAlmostEqual(x.g[0], 0.25, places=2)
