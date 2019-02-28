from unittest import TestCase
from pylamarck.algorithms.exhaustive_search import ExhaustiveSearchBasic


class TestExhaustiveSearchBasic(TestCase):
    def test(self):
        xs = [3, 2, 1]
        esb = ExhaustiveSearchBasic(xs)
        x_min = esb.solve(lambda x: x)
        self.assertEqual(x_min, 1)
