from unittest import TestCase
from pylamarck.individual import IndividualFactory
from pylamarck.spaces.bits.test_functions_bits import Knapsack
from pylamarck.spaces.bits.production import RandomBitSequence
from pylamarck.algorithms.evolutionary import ObjectiveEvaluator


class TestEvolutionary(TestCase):
    def test(self):
        knapsack_f = Knapsack()
        ind_fac = IndividualFactory(lambda x: x, knapsack_f)
        nso = RandomBitSequence(knapsack_f.number_of_products)
        population = [ind_fac.create_individual(g) for g in nso.create_many(10)]
        evaluator = ObjectiveEvaluator()
        population_with_fitness = [(ind, evaluator(ind)) for ind in population]
        self.assertEqual(population_with_fitness[0][1], population[0].y)
