from unittest import TestCase
from pylamarck.spaces.euclidean.production import DifferentialRecombination
from pylamarck.individual import IndividualFactory


class TestDifferentialRecombination(TestCase):
    def test(self):
        ind_fac = IndividualFactory(lambda x: 0.0)
        g1 = [1.0, 2.0, 3.0]
        g2 = [2.0, 3.0, 4.0]
        g3 = [-1.0, -1.0, -2.0]
        strength = 0.5
        dr = DifferentialRecombination(strength)
        offspring = dr([ind_fac.create_individual(g1),
                        ind_fac.create_individual(g2),
                        ind_fac.create_individual(g3)])
        self.assertListEqual(offspring, [-1.5, -1.5, -2.5])

