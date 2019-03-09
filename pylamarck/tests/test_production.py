from unittest import TestCase
from pylamarck.production import SearchOperation, UnarySearchOperation,\
    BinarySearchOperation


class TestSearchOperation(TestCase):
    def test(self):
        so = SearchOperation()
        self.assertRaises(NotImplementedError, so)
        self.assertIsNone(so.new_generation())
        self.assertIsNone(so.new_best_individual(None, None))


class TestUnarySearchOperation(TestCase):
    def test(self):
        uso = UnarySearchOperation()
        self.assertRaises(NotImplementedError, uso, None)


class TestBinarySearchOperation(TestCase):
    def test(self):
        bso = BinarySearchOperation()
        self.assertRaises(NotImplementedError, bso, None, None)
