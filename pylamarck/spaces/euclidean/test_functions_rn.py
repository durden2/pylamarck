
import numpy as np


def fbeale(x):
    """
    Beale function
    :param x:
    :return:
    """
    return (1.5 - x[0] + x[0]*x[1])**2 + (2.25 - x[0] + x[0]*x[1]**2)**2 + (2.625 - x[0] + x[0]*x[1]**3)**2


def fhimmelblau(x):
    """
    Himmelblau function
    :param x:
    :return:
    """
    return (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 - 7)**2


def feggholder(x):
    """
    Eggholder function
    :param x:
    :return:
    """
    return -(x[1]+47.0)*np.sin(np.sqrt(np.fabs(x[0]/2.0 + x[1] + 47.0))) -\
           x[0]*np.sin(np.sqrt(np.fabs(x[0] - (x[1] + 47.0)))) + 1000.0


def fsphere(x):
    """
    Sphere function
    :param x:
    :return:
    """
    return sum(t*t for t in x)


def frosenn(x):
    """
    Multidimensional Rosenbrock function
    :param x:
    :return:
    """
    return sum([100*(x[i+1]-x[i]**2)**2 + (1-x[i])**2 for i in range(len(x)-1)])
