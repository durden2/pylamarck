from unittest import TestCase
from pylamarck.spaces.bits.production import UniformCrossover,\
    MultiPointCrossover, BitFlips
from pylamarck.individual import Individual


class TestUniformCrossover(TestCase):
    def test(self):
        g1 = [True, False, True]
        g2 = [False, False, False]
        uc = UniformCrossover()
        crossed = uc(Individual(g1, g1, 0.0), Individual(g2, g2, 0.0))
        for i in range(len(g1)):
            self.assertIn(crossed[i], [g1[i], g2[i]])


class TestMultiPointCrossover(TestCase):
    def test(self):
        g1 = [True, False, True]
        g2 = [False, False, False]
        mpx = MultiPointCrossover(1)
        crossed = mpx(Individual(g1, g1, 0.0), Individual(g2, g2, 0.0))
        for i in range(len(g1)):
            self.assertIn(crossed[i], [g1[i], g2[i]])


class TestBitFlips(TestCase):
    def test(self):
        g1 = [True, False, True, False, True, True, False]
        for num_flips in range(4):
            for can_repeat in [True, False]:
                uso = BitFlips(num_flips, can_repeat=can_repeat)
                mutated = uso(Individual(g1, g1, 0.0))
                flipped = 0
                for i in range(len(g1)):
                    if mutated[i] != g1[i]:
                        flipped += 1
                if can_repeat:
                    self.assertTrue(flipped <= num_flips)
                else:
                    self.assertEqual(num_flips, flipped)
