from unittest import TestCase
from pylamarck.algorithms.tabu_search import TabuSearch, SimpleTabuSearchNeighbourhood
from pylamarck.spaces.bits.production import RandomBitSequence
from pylamarck.production import ConstantSearch
from pylamarck.spaces.bits.test_functions_bits import MaxSAT, sat_neighbourhood
from pylamarck.termination import MaxSteps
import random


class TestTabuSearch(TestCase):
    def test(self):
        n_vars = 5
        n_conj = 4
        n_disj = 3
        nso_rand = RandomBitSequence(n_vars)
        random.seed(42)

        msat = MaxSAT(n_vars, n_conj, n_disj)
        tabu_max_len = 30  # the result is very sensitive to this parameter
        neighbourhood_search = SimpleTabuSearchNeighbourhood(sat_neighbourhood)
        search = TabuSearch(nso_rand,
                            neighbourhood_search,
                            MaxSteps(100),
                            tabu_max_len)
        xts = search.solve(msat)
        self.assertTrue(len(xts.g) == n_vars)
