from unittest import TestCase
from pylamarck.algorithms.random_walk import RandomWalk
from pylamarck.spaces.euclidean.production import RandomAdditiveMutation,\
    GaussianRn
from pylamarck.production import ConstantSearch
import random
from pylamarck.termination import MaxSteps
from pylamarck.logging import EvaluationLogger, logme
import numpy as np


class TestRandomWalk(TestCase):
    def test(self):
        nso = ConstantSearch(np.array([1.0, 2.0]))
        sigma = 0.05
        uso = RandomAdditiveMutation(GaussianRn(2, sigma))
        term = MaxSteps(50)
        rw = RandomWalk(nso, uso, term)
        random.seed(42)
        el = EvaluationLogger("test_fun")
        fun = logme(el)(lambda x: x[0]**2 + x[1]**2)
        rw.solve(fun)
        for i in range(len(el.evals)-1):
            diff = el.evals[i][0][0] - el.evals[i+1][0][0]
            self.assertTrue(np.linalg.norm(diff) < 6*sigma)
