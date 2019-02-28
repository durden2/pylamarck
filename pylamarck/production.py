import random
import numpy as np


class SearchOperation:
    def __call__(self, *args):
        raise NotImplementedError


class NullarySearchOperation(SearchOperation):
    def __call__(self):
        """
        Create a random element of the search space.
        """
        raise NotImplementedError

    def create_many(self, n):
        """
        Create a random elements of the search space.
        :param n: how many elements should be generated
        """
        return np.array([self() for _ in range(n)])


class RandomSequenceSearch(NullarySearchOperation):
    def __init__(self, container):
        self.container = container

    def __call__(self):
        return random.choice(self.container)


class SequentialSearch(NullarySearchOperation):
    def __init__(self, container):
        self.it = iter(container)

    def __call__(self):
        return next(self.it)


class ConstantSearch(NullarySearchOperation):
    def __init__(self, x0):
        self.x0 = x0

    def __call__(self):
        return self.x0


class UnarySearchOperation(SearchOperation):
    def __call__(self, parent):
        """
        Create a random element of the search space.
        :param parent: instance to mutate
        """
        raise NotImplementedError


class BinarySearchOperation(SearchOperation):
    def __call__(self, parent_1, parent_2):
        raise NotImplementedError


class PostSearchOperationWrapper(SearchOperation):
    def __init__(self, wrapped_operator, transformation):
        self.wrapped_operator = wrapped_operator
        self.transformation = transformation

    def __call__(self, *args):
        original_result = self.wrapped_operator(*args)
        return self.transformation(original_result)
