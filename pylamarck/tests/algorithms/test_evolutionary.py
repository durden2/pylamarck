from unittest import TestCase
from pylamarck.individual import IndividualFactory
from pylamarck.spaces.bits.test_functions_bits import Knapsack
from pylamarck.spaces.bits.production import RandomBitSequence
from pylamarck.algorithms.evolutionary import ObjectiveEvaluator,\
    RouletteWheel, TournamentSelection


class TestEvolutionary(TestCase):
    def test(self):
        knapsack_f = Knapsack()
        ind_fac = IndividualFactory(knapsack_f)
        nso = RandomBitSequence(knapsack_f.number_of_products)
        population = [ind_fac.create_individual(g)
                      for g in nso.create_many(10)]
        evaluator = ObjectiveEvaluator()
        for ind in population:
            evaluator(ind)

        self.assertEqual(population[0].fitness, population[0].y)

        num_to_select = 3
        rw_selector = RouletteWheel(num_to_select)
        selected = rw_selector(population)
        self.assertEqual(len(selected), num_to_select)

        ts_selector = TournamentSelection(4, num_to_select)
        selected = ts_selector(population)
        self.assertEqual(len(selected), num_to_select)
