import matplotlib.pyplot as plt
from pylamarck.algorithms.tabu_search import TabuMove
from copy import copy
import math
import random


class City:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name


class RandomCities:
    def __init__(self, n, rand_min=-100.0, rand_max=100.0):
        def get_coord():
            return random.uniform(rand_min, rand_max)

        self._cities = [City(get_coord(), get_coord(), f"C-{i}")
                        for i in range(n)]

    def dist(self, i, j):
        return math.sqrt((self._cities[i].x - self._cities[j].x)**2 +
                         (self._cities[i].y - self._cities[j].y)**2)

    def __call__(self, perm):
        dist = 0.0
        for i in range(len(perm)):
            dist += self.dist(perm[i], perm[(i+1) % len(perm)])

        return dist


def visualize(pc, orders, show_plot=True):

    coords = [(c.x, c.y) for c in pc._cities]

    plt.axes().set_aspect('equal', 'datalim')
    for order in orders:
        x_coords = [coords[i][0] for i in order["perm"]]
        x_coords.append(x_coords[0])
        y_coords = [coords[i][1] for i in order["perm"]]
        y_coords.append(y_coords[0])

        plt.plot(x_coords, y_coords, label=order["label"], linestyle='-.')

    # plot city names
    for i in range(len(pc._cities)):
        plt.text(coords[i][0], coords[i][1], pc._cities[i].name)

    plt.legend(loc='lower left')
    if show_plot:
        plt.show()
    return plt


class SwapElementsMove(TabuMove):
    def __init__(self, i, j):
        """

        :param i: first element to swap
        :param j: second element to swap
        """
        self.i = i
        self.j = j

    def conflicts(self, other):
        return self.i == other.i and self.j == other.j

    def reverse(self):
        return self

    def make_move(self, ind):
        g = copy(ind.g)
        t = g[self.i]
        g[self.i] = g[self.j]
        g[self.j] = t
        return g


def tsp_swap_neighbourhood(x):
    n = len(x.g)
    return [SwapElementsMove(i, j)
            for i in range(n)
            for j in range(n) if i != j]


class ReversePartMove(TabuMove):
    def __init__(self, i, j):
        """

        :param i: index of the first element of reversed sequence
        :param j: index of the last element of reversed sequence
        """
        self.i = i
        self.j = j

    def conflicts(self, other):
        return self.i == other.i and self.j == other.j

    def reverse(self):
        return self

    def make_move(self, ind):
        g = ind.g[:self.i]
        g += reversed(ind.g[self.i:self.j+1])
        g += ind.g[self.j+1:]
        return g


def tsp_reverse_neighbourhood(x):
    n = len(x.g)
    return [ReversePartMove(i, j) for i in range(n-1) for j in range(i+1, n-1)]
