from unittest import TestCase
from pylamarck.individual import Individual
from pylamarck.algorithms.evolutionary import RouletteWheel,\
    TournamentSelection, TruncationSelection, ParentReplacementSelection,\
    PopulationTracker


class TestSelector(TestCase):
    def test(self):
        population = [Individual([0], [0], 0.0, fitness=0.0),
                      Individual([1], [1], 0.0, fitness=0.0),
                      Individual([2], [2], 0.0, fitness=0.0),
                      Individual([3], [3], 0.0, fitness=0.0),
                      Individual([4], [4], 0.0, fitness=0.0)]
        universal_parent = Individual([-1], [-1], 0.0, fitness=0.0)
        for ind in population:
            ind.reproduction_auxiliary = universal_parent

        selectors = [RouletteWheel(2),
                     TournamentSelection(2, 3),
                     TruncationSelection(3),
                     ParentReplacementSelection(),
                     PopulationTracker(RouletteWheel(2))]

        for s in selectors:
            selected = s(population)
            for ind in selected:
                self.assertIsInstance(ind, Individual)
