from random import Random

from genetic_algorithm.operators.mutator import mutate_permutations_by_interchange
from msrcpsp.genetic_algorithm.representation import GAProjectPlan
from msrcpsp.project_context import DetailedProjectContext


def create_mutator_function(activities_mutator_function, assignments_mutator_function):
    def mutate(individual: GAProjectPlan, random: Random, project_context: DetailedProjectContext) -> GAProjectPlan:
        result = GAProjectPlan()
        result.activities = activities_mutator_function(individual.activities, random, project_context)
        result.assignments = assignments_mutator_function(individual.assignments, random, project_context)
        return result

    return mutate


# Let S=[A1,A2,....,An] be the current order. this mutation chooses a random activity Ak.
# the newly generated order will have the activities [A1,A2,...,Ak-1,Ak+1,...,An] in the this order, and Ak
# "floats" somewhere such that the order remains available.
def mutate_orders(orders: list[int], random: Random, project_context: DetailedProjectContext) -> list[int]:
    project_nr_activities = project_context.nr_activities
    project_activities = project_context.activities
    orders = orders[:]  # we create a copy such that we don't modify the original list
    k = random.randint(0, project_nr_activities - 1)
    activity = orders[k]

    lb = k
    while lb > 0:
        if orders[lb - 1] in project_activities[activity].predecessors:
            break
        lb -= 1

    ub = k
    while ub < project_nr_activities - 1:
        if orders[ub + 1] in project_activities[activity].successors:
            break
        ub += 1

    if lb != ub:
        new_k = random.randint(lb, ub)
        while new_k == k:
            new_k = random.randint(lb, ub)

        step = 1
        if new_k < k:
            step = -1

        while k != new_k:
            orders[k], orders[k + step] = orders[k + step], orders[k]
            k = k + step
    return orders


def mutate_priorities(priorities: list[int], random: Random, project_context: DetailedProjectContext) -> list[int]:
    return mutate_permutations_by_interchange(priorities, random)


def create_assignments_mutator_function(single_assignment_generator_function):
    def mutate(assignments: list[dict[int, set[int]]], random: Random, project_context: DetailedProjectContext) \
            -> list[dict[int, set[int]]]:
        project_nr_activities = project_context.nr_activities
        project_activities = project_context.activities
        assignments = assignments[:]  # we create a copy such that we don't affect the original list
        activity_id = random.randint(0, project_nr_activities - 1)

        skill_requirements = project_activities[activity_id].required_units_of_skill
        assignments[activity_id] = single_assignment_generator_function(skill_requirements, random, project_context)
        return assignments

    return mutate
