from unittest import TestCase
from pylamarck.algorithms.simulated_annealing import SimulatedAnnealing, ExponentialSchedule, LogarithmicSchedule, \
    PolynomialSchedule
from pylamarck.termination import MaxSteps, TimeLimit
from pylamarck.production import ConstantSearch
from pylamarck.spaces.bits.production import BitFlips
from pylamarck.spaces.bits.test_functions_bits import MaxSAT


class TestSimulatedAnnealing(TestCase):
    def test(self):
        n_vars = 10
        max_time = 1
        max_steps = 1000
        nso_const = ConstantSearch([True for _ in range(n_vars)])
        uso = BitFlips(2)

        schedules = [{"label": "exponential", "schedule": ExponentialSchedule(1.0, 0.05)},
                     {"label": "logarithmic", "schedule": LogarithmicSchedule(1.0)},
                     {"label": "polynomial", "schedule": PolynomialSchedule(1.0, 2, 500)}]
        msat = MaxSAT(n_vars, 5, 3)
        for s in schedules:

            search = SimulatedAnnealing(nso_const, uso, TimeLimit(max_time) | MaxSteps(max_steps), s["schedule"])
            xsa = search.solve(msat)
            self.assertTrue(msat(xsa.g) <= msat(nso_const()))
