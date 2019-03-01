from unittest import TestCase
from pylamarck.spaces.permutations.test_functions_tsp import SwapElementsMove
from pylamarck.spaces.permutations.production import RandomPermutation
from pylamarck.individual import Individual


class TestSwapElementsMove(TestCase):
    def test_conflicts(self):
        sem12 = SwapElementsMove(1, 2)
        sem13 = SwapElementsMove(1, 3)
        self.assertTrue(sem12.conflicts(sem12))
        self.assertTrue(sem13.conflicts(sem13))
        self.assertFalse(sem12.conflicts(sem13))
        self.assertFalse(sem13.conflicts(sem12))

    def test_reverse(self):
        sem12 = SwapElementsMove(1, 2)
        sem21 = sem12.reverse()
        self.assertEqual(sem12, sem21)

    def test_make_move(self):
        sem12 = SwapElementsMove(1, 2)
        perm_gen = RandomPermutation(10)
        perm = perm_gen()
        ind = Individual(perm, perm, 0.0)
        perm_act = sem12.make_move(ind)
        ind2 = Individual(perm_act, perm_act, 0.0)
        perm_act_rev = sem12.reverse().make_move(ind2)
        self.assertListEqual(perm, perm_act_rev)
