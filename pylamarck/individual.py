
class Individual:
    def __init__(self, g, p, y, epoch=None):
        self.g = g
        self.p = p
        self.y = y
        self.epoch = epoch

    def __lt__(self, other):
        return self.y < other.y

    def __str__(self):
        return "Individual: g = {}, p = {}, y = {}".format(self.g, self.p, self.y)


class IndividualFactory:
    def __init__(self, gpm, f):
        self.gpm = gpm
        self.f = f

    def create_individual(self, g, epoch=None):
        p = self.gpm(g)
        y = self.f(p)
        return Individual(g, p, y, epoch=epoch)
