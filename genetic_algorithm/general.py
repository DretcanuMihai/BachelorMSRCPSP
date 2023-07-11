from typing import Union

MAXIMIZING_PROBLEM = object()
MINIMIZING_PROBLEM = object()


class Candidate:
    def __init__(self, representation, fitness: Union[int, float]):
        self.representation = representation
        self.fitness: Union[int, float] = fitness
