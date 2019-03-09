from pylamarck.algorithms.algorithm import SearchAlgorithm
from pylamarck.individual import IndividualFactory
import random
import math
import matplotlib.pyplot as plt


class SimulatedAnnealing(SearchAlgorithm):
    def __init__(self, nso, uso, term, temperature_schedule, gpm=lambda x: x):
        """

        :param nso: nullary search operator
        :param uso: unary search operator
        :param term: termination criterion
        :param temperature_schedule:
        :param gpm: genome phenome mapping
        """
        self.nso = nso
        self.uso = uso
        self.term = term
        self.temperature_schedule = temperature_schedule
        self.gpm = gpm

    def solve(self, f):
        time = 1

        ind_fac = IndividualFactory(f, self.gpm)
        cur_ind = ind_fac.create_individual(self.nso())
        self.term.initialize()
        best_ind = cur_ind

        while not self.term.should_terminate():
            new_ind = ind_fac.create_individual(self.uso(cur_ind))
            delta_e = new_ind.y - cur_ind.y
            if delta_e < 0:
                cur_ind = new_ind
                if new_ind.lt_goal(best_ind):
                    best_ind = new_ind
            else:
                temperature = self.temperature_schedule(time)
                # we need to check if temperature is greater than 0
                # to avoid division by zero in the second condition
                if temperature > 1e-10 and random.uniform(0.0, 1.0) < \
                        math.exp(-delta_e/temperature):
                    cur_ind = new_ind

            time += 1
        return best_ind


class LogarithmicSchedule:
    def __init__(self, init_temp):
        self.init_temp = init_temp

    def __call__(self, time):
        if time < 3:
            return self.init_temp
        else:
            return self.init_temp / math.log(time)


class ExponentialSchedule:
    def __init__(self, init_temp, epsilon):
        self.init_temp = init_temp
        self.epsilon = epsilon

    def __call__(self, time):
        return self.init_temp * (1.0 - self.epsilon)**time


class PolynomialSchedule:
    def __init__(self, init_temp, alpha, t_max):
        self.init_temp = init_temp
        self.alpha = alpha
        self.t_max = t_max

    def __call__(self, time):
        return self.init_temp * (max(0.0, 1 - (time/self.t_max)))**self.alpha


def temperature_schedule_plot(schedules, t_max):
    fig, ax = plt.subplots(figsize=(14, 9))

    for schedule in schedules:
        x_range = range(1, t_max)
        values_y = list(map(schedule["schedule"], x_range))

        ax.plot(list(x_range), values_y,
                label=schedule["label"], linestyle='-')

    ax.set_xlabel("time")
    ax.set_ylabel("temperature")
    ax.legend(loc='upper left')
    plt.show()
