from pylamarck.production import NullarySearchOperation,\
    UnarySearchOperation, SearchOperation
from pylamarck.individual import Constraint
from pylamarck.algorithms.evolutionary import Reproducer

import numpy as np
import random
import copy


class RandomUniformSearch(NullarySearchOperation):
    def __init__(self, ai, bi):
        self._ai = ai
        self._bi = bi

    def __call__(self):
        return np.array([random.uniform(self._ai[i], self._bi[i])
                         for i in range(len(self._ai))])


class BoxConstraint(Constraint):
    def __init__(self, ai, bi):
        self.ai = ai
        self.bi = bi

    def check(self, x):
        return all([self.ai[i] <= x[i] <= self.bi[i]
                    for i in range(len(x))])

    def fix(self, x):
        return np.clip(x, self.ai, self.bi)


class GaussianRn(NullarySearchOperation):
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

    def new_generation(self):
        if isinstance(self._rng, SearchOperation):
            self._rng.new_generation()

    def new_best_individual(self, old_best, new_best):
        if isinstance(self._rng, SearchOperation):
            self._rng.new_best_individual(old_best, new_best)


class GaussianESMutation(NullarySearchOperation):
    """
    Rng for gaussian mutation for evolutionary strategies.
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
        self._t = 1  # generation
        self._s = 0  # successful update counter

    def __call__(self):
        return np.array([random.gauss(self._mu, self._sigma)
                         for _ in range(self._n)])

    def new_generation(self):
        if self._t % self._update_period == 0:
            if self._s / self._update_period < self._update_threshold:
                self._sigma *= self._a
            else:
                self._sigma /= self._a
        self._t += 1

    def new_best_individual(self, old_best, new_best):
        self._s += 1


class DiscreteRecombination(SearchOperation):
    def __call__(self, parents):
        new_g = copy.copy(parents[0].g)
        n_parents = len(parents)
        for i in range(len(new_g)):
            new_g[i] = parents[random.randint(0, n_parents-1)].g[i]
        return new_g


class IntermediateRecombination(SearchOperation):
    def __call__(self, parents):
        new_g = copy.copy(parents[0].g)
        n_parents = len(parents)
        for i in range(len(new_g)):
            parent_values = [parents[k].g[i] for k in range(n_parents)]
            new_g[i] = np.mean(parent_values)
        return new_g


class DifferentialRecombination(SearchOperation):
    def __init__(self, strength, fix_genotype=lambda x: x):
        """

        :param strength: coefficient of difference term
        :param fix_genotype: function
        """
        self._strength = strength
        self._fix_genotype = fix_genotype

    def __call__(self, parents):
        new_g = [parents[2].g[i] +
                 self._strength * (parents[0].g[i] - parents[1].g[i])
                 for i in range(len(parents[2].g))]
        return self._fix_genotype(new_g)


class DEReproducer(Reproducer):
    """
    Reproducer for differential evolution.
    """
    def __init__(self, recombination):
        """

        :param recombination: ternary recombination operator
            main parent is passed as the third one
        """
        self._recombination = recombination

    def __call__(self, mate_pool, ind_fac, generation):
        offspring = []
        mate_pool_size = len(mate_pool)
        for i, ind_i in enumerate(mate_pool):
            range_without_i = list(filter(lambda x: x != i,
                                          range(mate_pool_size)))
            j, k = np.random.choice(range_without_i,
                                    2,
                                    replace=False)
            new_g = self._recombination([mate_pool[j],
                                         mate_pool[k],
                                         mate_pool[i]])
            new_ind =\
                ind_fac.create_individual(new_g,
                                          generation=generation,
                                          reproduction_auxiliary=mate_pool[i])
            offspring.append(new_ind)

        return offspring


class RandomKeysGPM:
    """
    Random Keys genome-phenome mapping
    """
    def __init__(self, n, s=None):
        self.n = n
        if s is None:
            self.s = list(range(n))
        else:
            self.s = s

    def __call__(self, g):
        el = sorted(zip(g, self.s), key=lambda x: x[0])
        return [e[1] for e in el]
