from random import Random
from typing import Union

from genetic_algorithm.operators.generator import nc_generate_permutation
from msrcpsp.genetic_algorithm.utils import ProjectException
from msrcpsp.genetic_algorithm.representation import GAProjectPlan
from msrcpsp.project_context import DetailedProjectContext


# the generated function doesn't need an input when called
def create_generator_function(activities_generator_function, assignments_generator_function):
    def generate(random: Random, project_context: DetailedProjectContext) -> GAProjectPlan:
        project_plan = GAProjectPlan()
        project_plan.activities = activities_generator_function(random, project_context)
        project_plan.assignments = assignments_generator_function(random, project_context)
        return project_plan

    return generate


def generate_orders(random: Random, project_context: DetailedProjectContext) -> list[int]:
    project_nr_activities = project_context.nr_activities
    project_activities = project_context.activities
    orders = []

    unfeasible_activities = set([elem for elem in range(project_nr_activities)])
    feasible_activities = set()

    predecessors = [set(project_activities[i].predecessors) for i in range(project_nr_activities)]
    successors = [set(project_activities[i].successors) for i in range(project_nr_activities)]

    while len(orders) != project_nr_activities:
        new_feasible_activities = set()
        for activity in unfeasible_activities:
            if len(predecessors[activity]) == 0:
                new_feasible_activities.add(activity)

        feasible_activities = feasible_activities.union(new_feasible_activities)
        unfeasible_activities = unfeasible_activities.difference(new_feasible_activities)

        choice_pool = list(feasible_activities)
        if len(choice_pool) == 0:
            raise ProjectException("Error: current activities have circular dependencies - check the following"
                                   " activities: " + str(list(unfeasible_activities)) + ";")
        chosen_activity = random.choice(choice_pool)
        orders.append(chosen_activity)

        feasible_activities.remove(chosen_activity)
        for successor in successors[chosen_activity]:
            predecessors[successor].remove(chosen_activity)
        for predecessor in predecessors[chosen_activity]:
            successors[predecessor].remove(chosen_activity)
    return orders


def generate_priorities(random: Random, project_context: DetailedProjectContext) -> list[int]:
    return nc_generate_permutation(random, project_context.nr_activities)


def create_assignments_generator_function(single_assignment_generator_function):
    def generate(random: Random, project_context: DetailedProjectContext) -> list[dict[int, set[int]]]:
        project_nr_activities = project_context.nr_activities
        project_activities = project_context.activities
        assignments = []
        for activity_id in range(project_nr_activities):
            assignments.append(
                single_assignment_generator_function(project_activities[activity_id].required_units_of_skill, random,
                                                     project_context))
        return assignments

    return generate


def nc_generate_single_assignment(skill_requirements: dict[int, int],
                                  random: Random,
                                  project_context: DetailedProjectContext) -> dict[int, set[int]]:
    skill_requirements_as_list = []
    for skill in sorted(skill_requirements.keys()):
        for _ in range(skill_requirements[skill]):
            skill_requirements_as_list.append(skill)
    random.shuffle(skill_requirements_as_list)  # to give each skill the chance to be prioritised
    all_resources = set([i for i in range(project_context.nr_resources)])
    resources_mastering_skill = project_context.resources_mastering_skill

    def backtracking_resource_assignments(current_available_resources: set[int],
                                          current_requirement_index: int) -> Union[list[int], None]:
        if current_requirement_index == len(skill_requirements_as_list):
            return []
        current_required_skill = skill_requirements_as_list[current_requirement_index]
        feasible_resources = current_available_resources.intersection(
            resources_mastering_skill[current_required_skill])
        feasible_resources = list(feasible_resources)
        random.shuffle(feasible_resources)
        for feasible_resource in feasible_resources:
            next_available_resources = current_available_resources.difference([feasible_resource])
            next_resource_assignments = backtracking_resource_assignments(next_available_resources,
                                                                          current_requirement_index + 1)
            if next_resource_assignments is not None:
                return [feasible_resource] + next_resource_assignments
        return None

    resource_assignments = backtracking_resource_assignments(all_resources, 0)
    if resource_assignments is None:
        raise ProjectException("Error: workforce can't satisfy the following combination of skill requirements: "
                               + str(skill_requirements) + ";")

    final_resource_assignments: dict[int, set[int]] = {}
    for skill in sorted(skill_requirements.keys()):
        final_resource_assignments[skill] = set()
    for skill, assigned_resource in zip(skill_requirements_as_list, resource_assignments):
        final_resource_assignments[skill].add(assigned_resource)
    return final_resource_assignments
