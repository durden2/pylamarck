from pylamarck.production import NullarySearchOperation, UnarySearchOperation

import numpy as np
import random
from copy import copy


class RandomPermutation(NullarySearchOperation):
    def __init__(self, n):
        self._n = n

    def __call__(self):
        return list(np.random.permutation(self._n))


class PermutationSingleSwap(UnarySearchOperation):
    def __init__(self, n):
        self._n = n

    def __call__(self, parent):
        pg = copy(parent.g)
        i = random.randint(0, self._n-1)
        j = random.randint(0, self._n-1)
        while i == j:
            j = random.randint(0, self._n-1)

        t = pg[i]
        pg[i] = pg[j]
        pg[j] = t

        return pg
