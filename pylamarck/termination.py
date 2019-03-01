import time


class TerminationCriterion:
    def initialize(self):
        pass

    def should_terminate(self) -> bool:
        raise NotImplementedError

    def __or__(self, other):
        return OrTermination([self, other])


class OrTermination(TerminationCriterion):
    def __init__(self, tcs):
        self.tcs = tcs

    def initialize(self):
        for tc in self.tcs:
            tc.initialize()

    def should_terminate(self):
        return any([tc.should_terminate() for tc in self.tcs])


class MaxSteps(TerminationCriterion):
    def __init__(self, max_steps):
        self._remaining = self._max_steps = max_steps

    def initialize(self):
        self._remaining = self._max_steps

    def should_terminate(self):
        self._remaining -= 1
        return self._remaining <= 0


class Infinite(TerminationCriterion):
    def should_terminate(self):
        return False


class TimeLimit(TerminationCriterion):
    def __init__(self, max_seconds):
        self._max_seconds = max_seconds
        self._t0 = time.time()

    def initialize(self):
        self._t0 = time.time()

    def should_terminate(self):
        t1 = time.time()
        return t1 - self._t0 > self._max_seconds


class EpochCallback(TerminationCriterion):
    def __init__(self, functions_to_call):
        """

        :param functions_to_call: functions called at the beginning of
            each epoch.
        """
        self._functions_to_call = functions_to_call

    def initialize(self):
        pass

    def should_terminate(self):
        for f in self._functions_to_call:
            f()
        return False
