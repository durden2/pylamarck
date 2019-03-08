
class Individual:
    def __init__(self, g, p, y, generation=None, reproduction_auxiliary=None,
                 fitness=None):
        self.g = g
        self.p = p
        self.y = y
        self.generation = generation
        self.reproduction_auxiliary = reproduction_auxiliary
        self.fitness = fitness

    def lt_goal(self, other):
        return self.y < other.y

    def lt_fitness(self, other):
        return self.fitness < other.fitness

    def __str__(self):
        str_desc = "Individual: g = {}, p = {}, y = {}, generation = {}, " \
                   "reproduction_auxiliary = {}, fitness = {}"
        return str_desc.format(self.g,
                               self.p,
                               self.y,
                               self.generation,
                               self.reproduction_auxiliary,
                               self.fitness)


class IndividualFactory:
    def __init__(self, f, gpm=lambda x: x):
        self.f = f
        self.gpm = gpm

    def create_individual(self, g, generation=None, reproduction_auxiliary=None):
        p = self.gpm(g)
        y = self.f(p)
        return Individual(g,
                          p,
                          y,
                          generation=generation,
                          reproduction_auxiliary=reproduction_auxiliary)


class Constraint:
    def check(self, genotype):
        raise NotImplementedError

    def get_checker(self):
        return lambda g: self.check(g)

    def fix(self, genotype):
        raise NotImplementedError

    def get_fixer(self):
        return lambda g: self.fix(g)
