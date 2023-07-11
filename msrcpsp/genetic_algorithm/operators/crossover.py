from random import Random

from genetic_algorithm.operators.crossover import cross_permutations_one_point, cross_lists_uniform
from msrcpsp.genetic_algorithm.representation import GAProjectPlan
from msrcpsp.project_context import DetailedProjectContext


def create_crossover_function(activities_crossover_function,
                              assignments_crossover_function):
    def cross(parents: list[GAProjectPlan], random: Random, project_context: DetailedProjectContext) -> \
            list[GAProjectPlan]:
        parent1 = parents[0]
        parent2 = parents[1]
        offspring1 = GAProjectPlan()
        offspring2 = GAProjectPlan()
        [offspring1.activities, offspring2.activities] = \
            activities_crossover_function([parent1.activities, parent2.activities], random, project_context)
        [offspring1.assignments, offspring2.assignments] = \
            assignments_crossover_function([parent1.assignments, parent2.assignments], random, project_context)
        return [offspring1, offspring2]

    return cross


def cross_activities(activities: list[list[int]], random: Random, project_context: DetailedProjectContext) \
        -> list[list[int]]:
    return cross_permutations_one_point(activities, random)


def cross_assignments(assignments: list[list[dict[int, set[int]]]], random: Random,
                      project_context: DetailedProjectContext) -> list[list[dict[int, set[int]]]]:
    return cross_lists_uniform(assignments, random)
