from unittest import TestCase
from pylamarck.production import SequentialSearch


class TestSequentialSearch(TestCase):
    def test(self):
        sequence = [1, 2, 3]
        seq_search = SequentialSearch(sequence)
        for i in range(len(sequence)):
            self.assertEqual(seq_search(), sequence[i])
