from unittest import TestCase
from pylamarck.spaces.trees.test_functions_symreg import \
    UnivariateRegressionProblem, SymbolicNode, SymbolicNodeGenerator
from pylamarck.spaces.trees.production import GrowTree, NodeSingleSwap
from pylamarck.termination import MaxSteps
from pylamarck.algorithms.evolution_strategies import EvolutionStrategy
import math
import numpy as np
import random


class TestUnivariateRegressionProblem(TestCase):
    def test(self):
        def f(x):
            return math.exp(x)
        xs = np.linspace(0.0, 1.0, 50)
        ys = np.array([f(x) for x in xs])
        unireg = UnivariateRegressionProblem(xs, ys)
        expr = SymbolicNode('real',
                            ['real'],
                            math.exp,
                            'exp',
                            [SymbolicNode('real',
                                          [],
                                          lambda variables: variables['x'],
                                          'x')])

        self.assertAlmostEqual(expr.evaluate({'x': 0.0}), 1.0)
        self.assertAlmostEqual(unireg(expr), 0.0)
        self.assertEqual(expr.get_tag(), 'real')
        self.assertEqual(expr.get_child_tag(0), 'real')
        self.assertEqual(expr.get_child(0).get_tag(), 'real')
        self.assertEqual(expr.num_children(), 1)
        self.assertEqual(expr.print_expression(), 'exp(x)')
        expr.child_nodes[0] = None
        self.assertIsNone(expr.get_child(0))

    def test2(self):
        def f(x):
            return math.exp(x)+math.sin(x)
        xs = np.linspace(0.0, 1.0, 50)
        ys = np.array([f(x) for x in xs])
        unireg = UnivariateRegressionProblem(xs, ys)

        random.seed(42)
        rand_node = SymbolicNodeGenerator(['x'], [])
        mutation = NodeSingleSwap(rand_node)
        nso = GrowTree(3, 'float', rand_node)
        es1 = EvolutionStrategy(mu_param=50,
                                lambda_param=50,
                                mode="(mu+lambda)",
                                nso=nso,
                                uso=mutation,
                                term=MaxSteps(20))
        expr = es1.solve(unireg)
        self.assertTrue(expr.y < 5.0)


