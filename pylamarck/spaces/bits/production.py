from pylamarck.production import NullarySearchOperation,\
    UnarySearchOperation, BinarySearchOperation

import random
from copy import copy
import numpy as np


class RandomBitSequence(NullarySearchOperation):
    def __init__(self, n):
        self._n = n

    def __call__(self):
        return [random.choice([True, False]) for _ in range(self._n)]


class BitFlips(UnarySearchOperation):
    def __init__(self, n, can_repeat=True):
        self._n = n
        self._can_repeat = can_repeat

    def __call__(self, parent):
        pg = copy(parent.g)
        if self._can_repeat:
            for _ in range(self._n):
                i = random.choice(range(len(pg)))
                pg[i] = not pg[i]
        else:
            used = []
            while len(used) < self._n:
                i = random.choice(range(len(pg)))
                if i not in used:
                    pg[i] = not pg[i]
                    used.append(i)

        return pg


class MultiPointCrossover(BinarySearchOperation):
    def __init__(self, k):
        """

        :param k: number of split points used in crossover
        """
        self.k = k

    def __call__(self, parent_1, parent_2):
        parent_1_g = parent_1.g
        parent_2_g = parent_2.g
        n = len(parent_1_g)
        split_points = list(sorted(np.random.choice(range(1, n-1), self.k,
                                                    replace=False)))
        parents = (parent_1_g, parent_2_g)
        parent_ids = [0 for _ in range(n)]
        sp_i = 0
        b = 0
        for t in range(n):
            if sp_i < self.k and t == split_points[sp_i]:
                b = 1-b
                sp_i += 1
            parent_ids[t] = b
        new_genotype = [parents[pid][i] for (i, pid) in enumerate(parent_ids)]
        return new_genotype


class UniformCrossover(BinarySearchOperation):
    def __call__(self, parent_1, parent_2):
        parent_1_g = parent_1.g
        parent_2_g = parent_2.g
        n = len(parent_1_g)
        parents = (parent_1_g, parent_2_g)
        parent_ids = [random.randint(0, 1) for _ in range(n)]
        new_genotype = [parents[pid][i] for (i, pid) in enumerate(parent_ids)]
        return new_genotype
