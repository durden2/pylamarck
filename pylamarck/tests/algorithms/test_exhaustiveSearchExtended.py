from unittest import TestCase
from pylamarck.algorithms.exhaustive_search import ExhaustiveSearchExtended


class TestExhaustiveSearchExtended(TestCase):
    def test(self):
        xs = [0, 3, 2, 1]
        esb = ExhaustiveSearchExtended(xs, lambda t: -t)
        x_min = esb.solve(lambda x: x)
        self.assertEqual(x_min.g, 3)
        self.assertEqual(x_min.p, -3)
        self.assertEqual(x_min.y, -3)
