from .algorithm import SearchAlgorithm
from pylamarck.individual import IndividualFactory


class RandomSampling(SearchAlgorithm):
    def __init__(self, nso, term, gpm=lambda x: x):
        """

        :param nso: nullary search operator
        :param term: termination criterion
        :param gpm: genome phenome mapping
        """
        self.nso = nso
        self.term = term
        self.gpm = gpm

    def solve(self, f):
        ind_fac = IndividualFactory(self.gpm, f)
        best_ind = ind_fac.create_individual(self.nso())
        self.term.initialize()

        while not self.term.should_terminate():
            new_ind = ind_fac.create_individual(self.nso())
            if new_ind < best_ind:
                best_ind = new_ind
        return best_ind
