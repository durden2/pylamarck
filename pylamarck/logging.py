import time
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import math


class EvaluationLogger:
    def __init__(self, label):
        self.evals = []
        self.label = label

    def push(self, args, f):
        self.evals.append((args, f, time.time()))


def logme(logger):
    def logger_decorator(function):
        def wrapper(*args, **kwargs):
            f = function(*args, **kwargs)
            logger.push(args, f)
            return f

        return wrapper

    return logger_decorator


def bresenham(n, m):
    return [i * n // m + n // (2 * m) for i in range(m)]


def convergence_demo2d(logs, f, mincoord, maxcoord, contour_logspace=True, contour_levels=30, xminf_=None,
                       resample_evals_to=200):
    xmin = mincoord[0]
    xmax = maxcoord[1]
    ymin = mincoord[0]
    ymax = maxcoord[1]

    xstep = (xmax - xmin) / 200
    ystep = (ymax - ymin) / 200

    x, y = np.meshgrid(np.arange(xmin, xmax + xstep, xstep), np.arange(ymin, ymax + ystep, ystep))
    z = f(np.array([x, y]))

    fig, ax = plt.subplots(figsize=(14, 9))
    if contour_logspace:
        ax.contour(x, y, z, levels=np.logspace(0.0, 5.0, contour_levels), norm=LogNorm(), cmap=plt.cm.jet)
    else:
        ax.contour(x, y, z, levels=np.linspace(np.min(z), np.max(z), contour_levels), cmap=plt.cm.jet)

    for log in logs:
        its = bresenham(len(log.evals), resample_evals_to)
        evals = [log.evals[i] for i in its]
        ax.plot([ev[0][0][0] for ev in evals], [ev[0][0][1] for ev in evals], label=log.label)

    if xminf_ is not None:
        ax.plot(*xminf_, 'o', markersize=5)

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.legend()

    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))
    plt.show()


def min_up_to_element(l):
    ret = [l[0]]
    mval = l[0]
    for i in range(1, len(l)):
        if l[i] < mval:
            mval = l[i]
        ret.append(mval)
    return ret


def goal_val_plot(logs, xtimestep='step', mintoi=True, fmin=None, plot_logarithm=True):
    fig, ax = plt.subplots(figsize=(14, 9))
    if fmin is None:
        absminfx = min(min(ev[1] for ev in log.evals) for log in logs)
    else:
        absminfx = fmin

    for log in logs:
        if plot_logarithm:
            vals_y = [math.log10(ev[1] - absminfx + 1) for ev in log.evals]
        else:
            vals_y = [ev[1] - absminfx for ev in log.evals]

        if mintoi:
            vals_y = min_up_to_element(vals_y)
        if xtimestep == 'step':
            vals_x = list(range(len(vals_y)))
        elif xtimestep == 'time':
            t0 = log.evals[0][2]
            vals_x = [ev[2] - t0 for ev in log.evals]
        else:
            raise Exception("wrong xtimestep")

        ax.plot(vals_x, vals_y,
                label=log.label, linestyle='-')

    ax.set_xlabel(xtimestep)
    if plot_logarithm:
        ax.set_ylabel('$\log_{10}(f(x)-f_{min}+1)$')
    else:
        ax.set_ylabel('$f(x)-f_{min}$')

    ax.legend(loc='upper left')
    plt.show()
