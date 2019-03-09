from unittest import TestCase
from pylamarck.spaces.permutations.test_functions_tsp import ReversePartMove
from pylamarck.individual import Individual


class TestReversePartMove(TestCase):
    def test(self):
        rpm = ReversePartMove(1, 2)
        rpm_r = rpm.reverse()
        self.assertEqual(rpm.i, rpm_r.i)
        self.assertEqual(rpm.j, rpm_r.j)

        self.assertTrue(rpm.conflicts(rpm))

        ind = Individual([0, 1, 2], [0, 1, 2], 0.0)
        ind_moved = rpm.make_move(ind)
        self.assertEqual(ind.g[0], ind_moved[0])
        self.assertEqual(ind.g[1], ind_moved[2])
        self.assertEqual(ind.g[2], ind_moved[1])
