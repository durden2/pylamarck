from pylamarck.algorithms.evolutionary import Evolutionary,\
    TruncationSelection, RandomReproducer, ObjectiveEvaluator,\
    BestIndividualSelectorSN
from pylamarck.algorithms.algorithm import SearchAlgorithm
from pylamarck.production import BinarySearchOperation
from pylamarck.termination import EpochCallback


class EvolutionStrategy(SearchAlgorithm):
    def __init__(self, mu_param, lambda_param, mode, nso, uso, term,
                 evaluator=ObjectiveEvaluator(), gpm=lambda x: x):
        """

        :param mu_param:
        :param lambda_param:
        :param mode: either "(mu, lambda)" or "(mu+lambda)"
        :param nso: nullary search operator
        :param uso: unary search operator (for mutation)
        :param term: termination condition
        :param evaluator: calculates fitness
        :param gpm: genome phenome mapping
        """
        self.mu_param = mu_param
        self.lambda_param = lambda_param
        if mode in ["(mu, lambda)", "(mu+lambda)"]:
            self.mode = mode
        else:
            raise Exception("mode must be either (mu, lambda) or (mu+lambda)")

        if mode == "(mu, lambda)":
            preserve_parents = False
        else:
            preserve_parents = True
        reproducer = RandomReproducer(lambda_param,
                                      uso,
                                      BinarySearchOperation(),
                                      1.01,
                                      preserve_parents)

        self.search = Evolutionary(nso=nso,
                                   reproducer=reproducer,
                                   selector=TruncationSelection(mu_param),
                                   term=term,
                                   n0=self.mu_param,
                                   evaluator=evaluator,
                                   gpm=gpm)

    def solve(self, f):
        return self.search.solve(f)


class AdaptiveEvolutionStrategy(SearchAlgorithm):
    def __init__(self, mu_param, lambda_param, mode, nso, uso, term,
                 evaluator=ObjectiveEvaluator(), gpm=lambda x: x):
        """

        :param mu_param:
        :param lambda_param:
        :param mode: either "(mu, lambda)" or "(mu+lambda)"
        :param nso: nullary search operator
        :param uso: unary search operator (for mutation)
        :param term: termination condition
        :param evaluator: calculates fitness
        :param gpm: genome phenome mapping
        """
        self.mu_param = mu_param
        self.lambda_param = lambda_param
        if mode in ["(mu, lambda)", "(mu+lambda)"]:
            self.mode = mode
        else:
            raise Exception("mode must be either (mu, lambda) or (mu+lambda)")

        if mode == "(mu, lambda)":
            preserve_parents = False
        else:
            preserve_parents = True
        reproducer = RandomReproducer(lambda_param,
                                      uso,
                                      BinarySearchOperation(),
                                      1.01,
                                      preserve_parents)

        epoch_callback = EpochCallback([lambda: uso.new_epoch()])

        def best_ind_listener(old_best_ind, new_best_ind):
            uso.new_best_individual(old_best_ind, new_best_ind)
        best_ind_selector = \
            BestIndividualSelectorSN(listener=best_ind_listener)

        self.search = Evolutionary(nso=nso,
                                   reproducer=reproducer,
                                   selector=TruncationSelection(mu_param),
                                   term=term | epoch_callback,
                                   n0=self.mu_param,
                                   evaluator=evaluator,
                                   gpm=gpm,
                                   best_individual_selector=best_ind_selector)

    def solve(self, f):
        return self.search.solve(f)

