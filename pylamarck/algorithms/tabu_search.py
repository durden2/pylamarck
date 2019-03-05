from pylamarck.algorithms.algorithm import SearchAlgorithm
from pylamarck.individual import IndividualFactory


class TabuSearch(SearchAlgorithm):
    def __init__(self, nso, neghbourhood_search, term, tabu_max_len,
                 gpm=lambda x: x):
        """

        :param nso: nullary search operator
        :param neghbourhood_search: neighbourhood search operation
        :param term: termination criterion
        :param tabu_max_len: max length of the tabu list
        :param gpm: genome phenome mapping
        """
        self.nso = nso
        self.neghbourhood_search = neghbourhood_search
        self.term = term
        self.tabu_max_len = tabu_max_len
        self.gpm = gpm

    def solve(self, f):

        ind_fac = IndividualFactory(f, self.gpm)
        best_ind = cur_ind = ind_fac.create_individual(self.nso())
        self.term.initialize()
        tabu = []
        n_search = self.neghbourhood_search

        while not self.term.should_terminate() and cur_ind is not None:
            new_ind, new_move = n_search.get_move(tabu, cur_ind,
                                                  best_ind, ind_fac)

            cur_ind = new_ind
            if cur_ind is not None:
                if cur_ind.lt_goal(best_ind):
                    best_ind = cur_ind
                tabu.append(new_move.reverse())
                if len(tabu) > self.tabu_max_len:
                    del tabu[0]

        return best_ind


class TabuSearchNeighbourhood:
    def get_move(self, tabu_list, cur_ind, best_ind, ind_fac):
        raise NotImplementedError


class SimpleTabuSearchNeighbourhood(TabuSearchNeighbourhood):
    def __init__(self, neighbours):
        self.neighbours = neighbours

    def get_move(self, tabu_list, cur_ind, best_ind, ind_fac):
        new_ind = None
        new_move = None
        for move in self.neighbours(cur_ind):
            test_ind = ind_fac.create_individual(move.make_move(cur_ind))
            disallowed = any(tabu_move.conflicts(move)
                             for tabu_move in tabu_list)
            if (not disallowed and
                (new_ind is None or test_ind.lt_goal(new_ind)))\
                    or test_ind.lt_goal(best_ind):
                new_ind = test_ind
                new_move = move
        return new_ind, new_move


class TabuMove:
    def conflicts(self, other):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    def make_move(self, ind):
        raise NotImplementedError
