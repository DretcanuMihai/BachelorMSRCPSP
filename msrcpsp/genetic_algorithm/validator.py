from msrcpsp.genetic_algorithm.representation import GAProjectPlan
from msrcpsp.genetic_algorithm.utils import transform_priorities_to_orders
from msrcpsp.project_context import DetailedProjectContext


class SchedulingException(Exception):
    pass


def create_validator_function(activities_validator_function, assignments_validator_function):
    def validate(plan: GAProjectPlan, project_context: DetailedProjectContext):
        activities_validator_function(plan.activities, project_context)
        assignments_validator_function(plan.assignments, project_context)

    return validate


def validate_activities(activities: list[int], project_context: DetailedProjectContext):
    project_nr_activities = project_context.nr_activities
    all_activities = set(range(project_nr_activities))
    unique_activities = set(activities)
    if len(activities) != project_nr_activities:
        raise SchedulingException("ACTIVITIES ERROR: THEY DON'T HAVE ENOUGH ELEMENTS")
    if unique_activities != all_activities:
        raise SchedulingException("ACTIVITIES ERROR: THEY AREN'T A PERMUTATION")


def validate_orders(orders: list[int], project_context: DetailedProjectContext):
    validate_activities(orders, project_context)
    reformed_orders = transform_priorities_to_orders(orders, project_context)
    if reformed_orders != orders:
        raise SchedulingException("ORDERS ERROR: NOT ACTUALLY AN ORDER LIST")


def validate_priorities(priorities: list[int], project_context: DetailedProjectContext):
    validate_activities(priorities, project_context)


def create_assignments_validator_function(single_assignment_validator_function):
    def validate(assignments: list[dict[int, set[int]]], project_context: DetailedProjectContext):
        project_nr_activities = project_context.nr_activities
        project_activities = project_context.activities
        if len(assignments) != project_nr_activities:
            raise SchedulingException("ASSIGNMENTS ERROR: THEY DON'T CONTAIN ENOUGH ELEMENTS")
        for activity_id in range(project_nr_activities):
            single_assignment_validator_function(assignments[activity_id],
                                                 project_activities[activity_id].required_units_of_skill,
                                                 project_context)

    return validate


def create_single_assignment_validator_function():
    def validate_skill_assignments(skill_type: int, required_skill_amount: int, assigned_resources: set[int],
                                   project_context: DetailedProjectContext):
        resources_mastering_skill = project_context.resources_mastering_skill
        if len(assigned_resources) != required_skill_amount:
            raise SchedulingException("ASSIGNMENT ERROR: NOT ENOUGH RESOURCES ASSIGNED FOR SKILL")
        for resource in assigned_resources:
            if resource not in resources_mastering_skill[skill_type]:
                raise SchedulingException("ASSIGNMENT ERROR: SOME RESOURCES ASSIGNED DON'T MASTER THE NEEDED SKILL")

    def validate_resources_assigned_once(assignment: dict[int, set[int]]):
        unique_assigned_resources = set()
        total_resources = 0
        for skill_type in assignment.keys():
            unique_assigned_resources = unique_assigned_resources.union(assignment[skill_type])
            total_resources += len(assignment[skill_type])
        if len(unique_assigned_resources) != total_resources:
            raise SchedulingException("ASSIGNMENT ERROR: SOME RESOURCES ARE ASSIGNED TWICE")

    def validate(assignment: dict[int, set[int]], skill_requirements: dict[int, int],
                 project_context: DetailedProjectContext):
        if set(assignment.keys()) != set(skill_requirements.keys()):
            raise SchedulingException("ASSIGNMENT ERROR: THE SKILLS DON'T MATCH WHAT'S REQUIRED")
        for skill_type in assignment.keys():
            validate_skill_assignments(skill_type, skill_requirements[skill_type], assignment[skill_type],
                                       project_context)
        validate_resources_assigned_once(assignment)

    return validate
