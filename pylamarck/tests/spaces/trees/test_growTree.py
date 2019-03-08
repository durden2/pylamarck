from unittest import TestCase
from pylamarck.spaces.trees.production import GrowTree
from pylamarck.spaces.trees.test_functions_symreg import SymbolicNodeGenerator
import random


class TestGrowTree(TestCase):
    def test(self):
        random.seed(42)
        sng = SymbolicNodeGenerator(['x'], [])
        max_depth = 2
        grower = GrowTree(max_depth, 'float', sng)
        tree = grower()
        self.assertTrue(tree.get_tag() == 'float')
        self.assertTrue(tree.get_depth() <= max_depth)
        self.assertIsInstance(tree.evaluate({'x': 0.0}), float)
