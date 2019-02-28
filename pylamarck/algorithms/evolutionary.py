from .algorithm import SearchAlgorithm
from pylamarck.individual import IndividualFactory
import numpy as np


class BestIndividualSelector:
    def __call__(self, previous_best, population):
        raise NotImplementedError


class SimpleBestIndividualSelector(BestIndividualSelector):
    def __call__(self, previous_best, population):
        new_best = previous_best
        for ind in population:
            if ind < new_best:
                new_best = ind
        return new_best


class Evaluator:
    def __call__(self, ind):
        raise NotImplementedError


class ObjectiveEvaluator(Evaluator):
    def __call__(self, ind):
        return ind.y


class Selector:
    def __call__(self, population_with_fitness):
        raise NotImplementedError


class RouletteWheel(Selector):
    def __init__(self, num_of_selected, with_replacement=True):
        self.num_of_selected = num_of_selected
        self.with_replacement = with_replacement

    def __call__(self, population_with_fitness):
        sum_fitness = sum(x[1] for x in population_with_fitness)
        probabilities = [x[1]/sum_fitness for x in population_with_fitness]
        return list(np.random.choice(population_with_fitness,
                                     self.num_of_selected,
                                     p=probabilities,
                                     replace=self.with_replacement))


class TournamentSelection(Selector):
    def __init__(self, k, mps):
        """

        :param k: number of contestants for each slot
        :param mps: number of slots (mating pool size)
        """
        self.k = k
        self.mps = mps

    def __call__(self, population_with_fitness):
        ret = []
        for i in range(self.mps):
            pop_num = len(population_with_fitness)
            selected_indices = np.random.choice(range(pop_num), self.k,
                                                replace=False)
            tournament = [population_with_fitness[i] for i in selected_indices]
            ret.append(min(tournament, key=lambda j: j[1]))
        return ret


class TruncationSelection(Selector):
    def __init__(self, mps):
        """

        :param mps: mating pool size
        """
        self.mps = mps

    def __call__(self, population_with_fitness):
        return sorted(population_with_fitness, key=lambda x: x[1])[:self.mps]


class Reproducer:
    def __call__(self, mate_pool):
        raise NotImplementedError


class RandomReproducer(Reproducer):
    def __init__(self, offspring_size, uso, bso, probability_mutation,
                 preserve_parents):
        """

        :param offspring_size:
        :param uso: unary search operator (for mutation)
        :param bso: binary search operator (for crossover
        :param probability_mutation: probability of mutation
        :param preserve_parents: if true, parents are appended to offspring
        """
        self.offspring_size = offspring_size
        self.uso = uso
        self.bso = bso
        self.probability_mutation = probability_mutation
        self.preserve_parents = preserve_parents

    def __call__(self, mate_pool):
        if self.preserve_parents:
            offspring = [parent[0].g for parent in mate_pool]
        else:
            offspring = []

        mate_pool_size = len(mate_pool)
        for i in range(self.offspring_size):
            if np.random.random() < self.probability_mutation:
                parent_id = np.random.choice(range(mate_pool_size))
                selected_individual = mate_pool[parent_id][0]
                offspring.append(self.uso(selected_individual))
            else:
                parent_ids = np.random.choice(range(mate_pool_size), 2,
                                              replace=False)
                parents = (mate_pool[parent_ids[0]][0],\
                          mate_pool[parent_ids[1]][0])
                offspring.append(self.bso(parents[0], parents[1]))
        return offspring


class Evolutionary(SearchAlgorithm):
    def __init__(self, nso, reproducer, selector, term, n0,
                 evaluator=ObjectiveEvaluator(), gpm=lambda x: x,
                 best_individual_selector=SimpleBestIndividualSelector()):
        """

        :param nso: nullary search operator (for getting initial population)
        :param reproducer: unary search operator (for mutation)
        :param selector: binary search operator (for reproduction)
        :param term: termination criterion
        :param n0: size of initial pool
        :param evaluator: calculates fitness
        :param gpm: genome phenome mapping
        :param best_individual_selector: a callable object for selecting new
                best individual
        """
        self.nso = nso
        self.evaluator = evaluator
        self.reproducer = reproducer
        self.selector = selector
        self.term = term
        self.n0 = n0
        self.gpm = gpm
        self.best_individual_selector = best_individual_selector

    def solve(self, f):
        ind_fac = IndividualFactory(self.gpm, f)
        epoch = 0
        genotypes = self.nso.create_many(self.n0)
        best_ind = ind_fac.create_individual(genotypes[0], epoch=epoch)
        self.term.initialize()

        while not self.term.should_terminate():
            # gpm and evaluation
            population = [ind_fac.create_individual(rg, epoch=epoch)
                          for rg in genotypes]
            # selecting new best individual
            best_ind = self.best_individual_selector(best_ind, population)
            # fitness assignment
            population_with_fitness = [(ind, self.evaluator(ind))
                                       for ind in population]
            # selection
            mate_pool = self.selector(population_with_fitness)
            # reproduction
            genotypes = self.reproducer(mate_pool)
            epoch += 1

        return best_ind
