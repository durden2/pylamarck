from pylamarck.production import NullarySearchOperation,\
    UnarySearchOperation, SearchOperation

import numpy as np
import random


class RandomUniformSearch(NullarySearchOperation):
    def __init__(self, ai, bi):
        self._ai = ai
        self._bi = bi

    def __call__(self):
        return np.array([random.uniform(self._ai[i], self._bi[i])
                         for i in range(len(self._ai))])


class BoxCond:
    def __init__(self, ai, bi):
        self._ai = ai
        self._bi = bi

    def __call__(self, x):
        return all([self._ai[i] <= x[i] <= self._bi[i]
                    for i in range(len(x))])


class GaussianRn(UnarySearchOperation):
    def __init__(self, n, sigma, mu=0.0):
        self._n = n
        self._mu = mu
        self._sigma = sigma

    def __call__(self):
        return np.array([random.gauss(self._mu, self._sigma)
                         for _ in range(self._n)])


class RandomAdditiveMutation(UnarySearchOperation):
    def __init__(self, rng, cond=lambda x: True):
        """

        :param rng:
        :param cond: condition for repeating randomization
        """
        self._cond = cond
        self._rng = rng

    def __call__(self, parent):
        pg = parent.g
        new = pg + self._rng()
        while not self._cond(new):
            new = self._rng()

        return new

    def new_epoch(self):
        if isinstance(self._rng, SearchOperation):
            self._rng.new_epoch()

    def new_best_individual(self, old_best, new_best):
        if isinstance(self._rng, SearchOperation):
            self._rng.new_best_individual(old_best, new_best)


class GaussianESMutation(UnarySearchOperation):
    """
    Gaussian mutation for evolutionary strategies.
    """
    def __init__(self, n, sigma, a, update_period,
                 update_threshold=0.2,
                 mu=0.0):
        """

        :param n: number of variables in the genome
        :param sigma: standard deviation of gaussian
        :param a: modification factor for standard deviation updating
        :param update_period: update period
        :param update_threshold: determines when sigma should be increased
            and when decreased
        :param mu: mean of gaussian
        """
        self._n = n
        self._mu = mu
        self._initial_sigma = sigma
        self._sigma = sigma
        self._a = a
        self._update_period = update_period
        self._update_threshold = update_threshold
        self._t = 1  # epoch
        self._s = 0  # successful update counter

    def __call__(self):
        return np.array([random.gauss(self._mu, self._sigma)
                         for _ in range(self._n)])

    def new_epoch(self):
        if self._t % self._update_period == 0:
            if self._s / self._update_period < self._update_threshold:
                self._sigma *= self._a
            else:
                self._sigma /= self._a
        self._t += 1

    def new_best_individual(self, old_best, new_best):
        self._s += 1
