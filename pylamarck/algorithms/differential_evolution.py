from pylamarck.algorithms.evolutionary import Evolutionary,\
    ObjectiveEvaluator, ParentReplacementSelection, Selector
from pylamarck.algorithms.algorithm import SearchAlgorithm
from pylamarck.spaces.euclidean.production import DEReproducer


class DifferentialEvolution(SearchAlgorithm):
    def __init__(self, nso, n0, tso, term,
                 evaluator=ObjectiveEvaluator(),
                 selector=ParentReplacementSelection(),
                 gpm=lambda x: x):
        """

        :param nso: nullary search operator
        :param n0: size of initial population
        :param tso: ternary search operator (for recombination)
        :param term: termination condition
        :param evaluator: calculates fitness
        :param gpm: genome phenome mapping
        """
        reproducer = DEReproducer(tso)

        self.search = Evolutionary(nso=nso,
                                   reproducer=reproducer,
                                   selector=selector,
                                   term=term,
                                   n0=n0,
                                   evaluator=evaluator,
                                   gpm=gpm)

    def solve(self, f):
        return self.search.solve(f)
