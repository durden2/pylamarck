from unittest import TestCase
from pylamarck.individual import IndividualFactory
from pylamarck.spaces.euclidean.production import DiscreteRecombination,\
    IntermediateRecombination


class TestDiscreteRecombination(TestCase):
    def test(self):
        dr = DiscreteRecombination()
        ind_fac = IndividualFactory(lambda x: 0.0)
        parents = [ind_fac.create_individual([0.0, 1.0]),
                   ind_fac.create_individual([1.0, 2.0]),
                   ind_fac.create_individual([2.0, 3.0])]
        result = dr(parents)
        self.assertIn(result[0], [0.0, 1.0, 2.0])
        self.assertIn(result[1], [1.0, 2.0, 3.0])


class TestIntermediateRecombination(TestCase):
    def test(self):
        dr = IntermediateRecombination()
        ind_fac = IndividualFactory(lambda x: 0.0)
        parents = [ind_fac.create_individual([0.0, 1.0]),
                   ind_fac.create_individual([1.0, 2.0]),
                   ind_fac.create_individual([2.0, 3.0])]
        result = dr(parents)
        self.assertEqual(result[0], 1.0)
        self.assertEqual(result[1], 2.0)
