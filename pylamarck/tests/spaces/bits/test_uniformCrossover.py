from unittest import TestCase
from pylamarck.spaces.bits.production import UniformCrossover
from pylamarck.individual import Individual


class TestUniformCrossover(TestCase):
    def test(self):
        g1 = [1, 0, 1]
        g2 = [0, 0, 0]
        uc = UniformCrossover()
        crossed = uc(Individual(g1, g1, 0.0), Individual(g2, g2, 0.0))
        for i in range(len(g1)):
            self.assertIn(crossed[i], [g1[i], g2[i]])
