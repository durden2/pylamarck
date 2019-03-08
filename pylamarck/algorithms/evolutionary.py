from .algorithm import SearchAlgorithm
from pylamarck.individual import IndividualFactory
import numpy as np
import copy


class BestIndividualSelector:
    def __call__(self, previous_best, population):
        raise NotImplementedError


class SimpleBestIndividualSelector(BestIndividualSelector):
    def __call__(self, previous_best, population):
        if previous_best is None:
            new_best = population[0]
        else:
            new_best = previous_best

        for ind in population:
            if ind.lt_goal(new_best):
                new_best = ind
        return new_best


class BestIndividualSelectorSN(BestIndividualSelector):
    """
    Selector of the best individual with notification of successful
    update of the best individual.
    """
    def __init__(self, listener, per_population=True):
        """

        :param listener: function to call when a better best individual
            is found. Two arguments are passed: the old best individual and
            the new best individual.
        :param per_population: if true, listener is called once per
            selection from the entire population. If false, listener
            is called each time a better individual is found.
        """
        self._listener = listener
        self._per_population = per_population

    def __call__(self, previous_best, population):
        if previous_best is None:
            new_best = population[0]
        else:
            new_best = previous_best

        better_ind_found = False
        for ind in population:
            if ind.lt_goal(new_best):
                if not self._per_population:
                    self._listener(new_best, ind)
                new_best = ind
                better_ind_found = True

        if better_ind_found and self._per_population:
            self._listener(previous_best, new_best)

        return new_best


class Evaluator:
    def __call__(self, ind):
        raise NotImplementedError


class ObjectiveEvaluator(Evaluator):
    def __call__(self, ind):
        ind.fitness = ind.y
        return ind.fitness


class Selector:
    def __call__(self, population_with_fitness):
        raise NotImplementedError


class PopulationTracker(Selector):
    def __init__(self, wrapped_selector, post_wrapped=True):
        self.wrapped_selector = wrapped_selector
        self.history = []
        self.post_wrapped = post_wrapped

    def __call__(self, population_with_fitness):
        selected = self.wrapped_selector(population_with_fitness)
        if self.post_wrapped:
            self.history.append(selected)
        else:
            self.history.append(population_with_fitness)

        return selected


class RouletteWheel(Selector):
    def __init__(self, num_of_selected, with_replacement=True):
        self.num_of_selected = num_of_selected
        self.with_replacement = with_replacement

    def __call__(self, population):
        pop_num = len(population)
        sum_fitness = sum(x.fitness for x in population)
        if np.isclose(sum_fitness, 0.0):
            probabilities = [1.0/pop_num for _ in population]
        else:
            probabilities = [x.fitness/sum_fitness
                             for x in population]

        selected_indices = np.random.choice(range(pop_num),
                                            self.num_of_selected,
                                            p=probabilities,
                                            replace=self.with_replacement)
        return [population[i] for i in selected_indices]


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
            ret.append(min(tournament, key=lambda j: j.fitness))
        return ret


class TruncationSelection(Selector):
    def __init__(self, mps):
        """

        :param mps: mating pool size
        """
        self.mps = mps

    def __call__(self, population_with_fitness):
        sel_with_fitness = sorted(population_with_fitness,
                                  key=lambda x: x.fitness)[:self.mps]
        return list(sel_with_fitness)


class ParentReplacementSelection(Selector):
    def __call__(self, population_with_fitness):
        offspring = []
        for ind in population_with_fitness:
            if ind.reproduction_auxiliary is None or\
                    ind.lt_fitness(ind.reproduction_auxiliary):
                ind.reproduction_auxiliary = None
                offspring.append(ind)
            else:
                offspring.append(ind.reproduction_auxiliary)
        return offspring


class Reproducer:
    def __call__(self, mate_pool, ind_fac, generation):
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

    def __call__(self, mate_pool, ind_fac, generation):
        if self.preserve_parents:
            offspring = copy.copy(mate_pool)
        else:
            offspring = []

        mate_pool_size = len(mate_pool)
        for i in range(self.offspring_size):
            if np.random.random() < self.probability_mutation:
                parent_id = np.random.choice(range(mate_pool_size))
                selected_individual = mate_pool[parent_id]

                new_genotype = self.uso(selected_individual)
            else:
                parent_ids = np.random.choice(range(mate_pool_size), 2,
                                              replace=False)
                parents = (mate_pool[parent_ids[0]],
                           mate_pool[parent_ids[1]])
                new_genotype = self.bso(parents[0], parents[1])
            new_ind = ind_fac.create_individual(new_genotype,
                                                generation=generation)
            offspring.append(new_ind)
        return offspring


class Evolutionary(SearchAlgorithm):
    def __init__(self, nso, reproducer, selector, term, n0,
                 evaluator=ObjectiveEvaluator(),
                 gpm=lambda x: x,
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
        ind_fac = IndividualFactory(f, self.gpm)
        generation = 0
        population = [ind_fac.create_individual(rg, generation=generation)
                      for rg in self.nso.create_many(self.n0)]
        best_ind = None
        self.term.initialize()

        while not self.term.should_terminate():
            # selecting new best individual
            best_ind = self.best_individual_selector(best_ind, population)
            # fitness assignment
            for ind in population:
                self.evaluator(ind)

            # selection
            mate_pool = self.selector(population)
            generation += 1
            # reproduction
            # gpm and evaluation
            population = self.reproducer(mate_pool, ind_fac, generation)

        return best_ind
