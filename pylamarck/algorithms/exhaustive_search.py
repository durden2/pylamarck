from .algorithm import SearchAlgorithm
from pylamarck.individual import IndividualFactory


class ExhaustiveSearchBasic(SearchAlgorithm):
    def __init__(self, xs):
        self.xs = xs

    def solve(self, f):
        cxs = iter(self.xs)
        best_x = next(cxs)
        for x in cxs:
            if f(x) < f(best_x):
                best_x = x
        return best_x


class ExhaustiveSearchExtended(SearchAlgorithm):
    def __init__(self, xs, gpm):
        self.xs = xs
        self.gpm = gpm

    def solve(self, f):
        ind_fac = IndividualFactory(f, self.gpm)
        cxs = iter(self.xs)
        best_ind = ind_fac.create_individual(next(cxs))
        for x in cxs:
            new_ind = ind_fac.create_individual(x)
            if new_ind < best_ind:
                best_ind = new_ind
        return best_ind
