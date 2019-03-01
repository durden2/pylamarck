from unittest import TestCase
from pylamarck.algorithms.evolution_strategies import EvolutionStrategy,\
    AdaptiveEvolutionStrategy
from pylamarck.production import ConstantSearch
from pylamarck.spaces.euclidean.production import RandomAdditiveMutation,\
    GaussianRn, GaussianESMutation
from pylamarck.termination import MaxSteps
import random


class TestEvolutionStrategy(TestCase):
    def test(self):
        mutation1 = RandomAdditiveMutation(GaussianRn(2, 1.0))
        random.seed(42)
        nso = ConstantSearch([1.0, 2.0])
        es1 = EvolutionStrategy(mu_param=1,
                                lambda_param=1,
                                mode="(mu+lambda)",
                                nso=nso,
                                uso=mutation1,
                                term=MaxSteps(100))

        mutation2 = RandomAdditiveMutation(GaussianESMutation(2, 1.0, 1.0, 5))
        es2 = AdaptiveEvolutionStrategy(mu_param=1,
                                        lambda_param=1,
                                        mode="(mu+lambda)",
                                        nso=nso,
                                        uso=mutation2,
                                        term=MaxSteps(100))

        def f(x):
            return x[0]**2 + x[1]**2

        x1 = es1.solve(f)
        random.seed(42)
        x2 = es2.solve(f)
        self.assertAlmostEqual(x1.g[0], x2.g[0])
        self.assertAlmostEqual(x1.g[1], x2.g[1])
