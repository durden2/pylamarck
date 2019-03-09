from unittest import TestCase
from pylamarck.spaces.permutations.test_functions_tsp import\
    tsp_swap_neighbourhood, visualize, RandomCities
from pylamarck.individual import Individual
import matplotlib.pyplot as plt


class TestTspSwapNeighbourhood(TestCase):
    def test(self):
        ind = Individual([0, 1, 2], [0, 1, 2], 0.0)
        neighbourhood = tsp_swap_neighbourhood(ind)
        for neighbour in neighbourhood:
            self.assertNotEqual(neighbour.i, neighbour.j)


class TestVisualize(TestCase):
    def test(self):
        # let's at least make sure it doesn't error
        n = 5
        cities = RandomCities(n)
        plt.close('all')
        visualize(cities,
                  [{"label": "Random sampling", "perm": list(range(n))}],
                  show_plot=False)
        self.assertTrue(True)
