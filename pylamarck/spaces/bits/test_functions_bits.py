import random
from pylamarck.algorithms.tabu_search import TabuMove
from copy import copy
import numpy as np


class MaxSAT:
    def __init__(self, n_vars, n_conj, n_disj):
        self.formula = []
        for i in range(n_conj):
            cur_disj = []
            for j in range(n_disj):
                cur_disj.append((random.randint(0, n_vars-1),
                                 random.choice([True, False])))
            self.formula.append(cur_disj)

    def check(self, x):
        result = True
        for clause in self.formula:
            cc = False
            for i, neg in clause:
                if neg:
                    cc = cc or not x[i]
                else:
                    cc = cc or x[i]
            result = result and cc
        return result

    def __call__(self, x):
        """
        Return number of not satisfied clauses.
        :param x: values of boolean variables
        :return:
        """
        result = len(self.formula)
        for clause in self.formula:
            cc = False
            for i, neg in clause:
                if neg:
                    cc = cc or not x[i]
                else:
                    cc = cc or x[i]
            if not cc:
                result -= 1
        return result

    def print(self):
        bit_str = ""
        for ci, clause in enumerate(self.formula):
            bit_str += "("
            for i, neg in clause:
                if neg:
                    bit_str += "-x[{}] ".format(i)
                else:
                    bit_str += "x[{}] ".format(i)
            if ci == len(self.formula)-1:
                bit_str += ")"
            else:
                bit_str += ") and "
        return bit_str


class BitFlipMove(TabuMove):
    def __init__(self, k):
        """

        :param k: bit to flip
        """
        self.k = k

    def conflicts(self, other):
        return self.k == other.k

    def reverse(self):
        return self

    def make_move(self, ind):
        g = copy(ind.g)
        g[self.k] = not g[self.k]
        return g


def sat_neighbourhood(x):
    n = len(x.g)
    return [BitFlipMove(k) for k in range(n)]


class Knapsack:
    def __init__(self,
                 min_weight=100,
                 max_weight=1500,
                 number_of_products=50,
                 knapsack_size=10000,
                 min_value=10,
                 max_value=1000):
        self.knapsack_size = knapsack_size
        self.weights = np.random.randint(min_weight, max_weight,
                                         number_of_products)
        self.values = np.random.randint(min_value, max_value,
                                        number_of_products)
        self.number_of_products = number_of_products

    def __call__(self, x):
        return sum(x[i]*self.values[i] for i in range(len(x)))

    def get_weight(self, x):
        return sum(x[i]*self.weight[i] for i in range(len(x)))

    def repair(self, x):
        x_repaired = copy(x)
        value_to_weight_sorted_indices =\
            sorted(range(len(x)),
                   key=lambda k: self.values[k]/self.weights[k])

        for i in value_to_weight_sorted_indices:
            if self.get_weight(x_repaired) <= self.knapsack_size:
                break
            if x[i] == 1:
                x[i] = 0
        return x_repaired
