from pylamarck.production import NullarySearchOperation, UnarySearchOperation

import numpy as np
import random


class RandomUniformSearch(NullarySearchOperation):
    def __init__(self, ai, bi):
        self._ai = ai
        self._bi = bi

    def __call__(self):
        return np.array([random.uniform(self._ai[i], self._bi[i]) for i in range(len(self._ai))])


class BoxCond:
    def __init__(self, ai, bi):
        self._ai = ai
        self._bi = bi

    def __call__(self, x):
        return all([self._ai[i] <= x[i] <= self._bi[i] for i in range(len(x))])


class GaussianRn:
    def __init__(self, n, mu, sigma):
        self._n = n
        self._mu = mu
        self._sigma = sigma

    def __call__(self):
        return np.array([random.gauss(self._mu, self._sigma) for _ in range(self._n)])


class RandomAdditiveMutation(UnarySearchOperation):
    def __init__(self, cond, rng):
        self._cond = cond
        self._rng = rng

    def __call__(self, parent):
        pg = parent.g
        new = pg + self._rng()
        while not self._cond(new):
            new = self._rng()

        return new
