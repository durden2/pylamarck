from unittest import TestCase
from pylamarck.logging import convergence_demo2d, EvaluationLogger,\
    goal_val_plot
from scipy.optimize import rosen


class TestConvergenceDemo2d(TestCase):
    def test(self):
        # let's at least make sure it doesn't error
        el_test = EvaluationLogger("Test logger")
        for i in range(50):
            arg = [0.0, 0.0]
            el_test.push([arg], rosen(arg))

        min_coord = [-3, -3]
        max_coord = [3, 3]
        convergence_demo2d([el_test], rosen, min_coord, max_coord,
                           resample_evals_to=25, show_plot=False)
        self.assertTrue(True)

        goal_val_plot([el_test], mintoi=True, xtimestep='time',
                      fmin=0, plot_logarithm=False, show_plot=False)
        self.assertTrue(True)
