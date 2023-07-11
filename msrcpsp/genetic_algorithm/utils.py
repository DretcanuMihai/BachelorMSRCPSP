import copy

from msrcpsp.genetic_algorithm.representation import GAProjectPlan
from msrcpsp.project_context import DetailedProjectContext
from msrcpsp.project_plan import BasicProjectPlan


class ProjectException(Exception):
    pass


def transform_priorities_to_orders(priorities: list[int], project_context: DetailedProjectContext) -> list[int]:
    project_nr_activities = project_context.nr_activities
    project_activities = project_context.activities
    orders = []
    priorities = priorities[:]  # create a copy such that we don't destroy the list from the outside
    priorities_index = 0
    while len(orders) != project_nr_activities:
        prioritized_activity = priorities[priorities_index]
        if len(project_activities[prioritized_activity].predecessors.difference(orders)) == 0:
            orders.append(prioritized_activity)
            priorities.pop(priorities_index)
            priorities_index = 0
        else:
            priorities_index += 1
            if priorities_index == len(priorities):
                raise ProjectException("Error: current activities have circular dependencies - check the following"
                                       " activities: " + str(priorities) + ";")
    return orders


def calculate_primitive_orders_representation_end_times(orders: list[int], assignments: list[dict[int, set[int]]],
                                                        project_context: DetailedProjectContext) -> list[int]:
    project_activities = project_context.activities
    project_nr_activities = project_context.nr_activities
    project_nr_resources = project_context.nr_resources

    activities_end_time = [0 for _ in range(project_nr_activities)]  # the time at which the activities ended
    resources_refresh_time = [0 for _ in range(project_nr_resources)]  # the time at which the resource becomes
    # available again
    for activity_id in orders:
        resources_assigned_for_skill = assignments[activity_id]
        activity = project_activities[activity_id]

        duration = activity.duration
        predecessors = activity.predecessors
        assigned_resources = []
        for required_skill in resources_assigned_for_skill:
            for resource in resources_assigned_for_skill[required_skill]:
                assigned_resources.append(resource)

        predecessors_max_end_time = max([activities_end_time[ind] for ind in predecessors], default=0)
        resources_max_refresh_time = max([resources_refresh_time[ind] for ind in assigned_resources], default=0)
        activity_end_time = max([predecessors_max_end_time, resources_max_refresh_time]) + duration
        activities_end_time[activity_id] = activity_end_time
        for resource in assigned_resources:
            resources_refresh_time[resource] = activity_end_time
    return activities_end_time


def transform_orders_to_solution(plan: GAProjectPlan, project_context: DetailedProjectContext) -> BasicProjectPlan:
    return transform_primitive_orders_and_assignments_to_solution(plan.activities, plan.assignments, project_context)


def transform_priorities_to_solution(plan: GAProjectPlan,
                                     project_context: DetailedProjectContext) -> BasicProjectPlan:
    orders = transform_priorities_to_orders(plan.activities, project_context)
    return transform_primitive_orders_and_assignments_to_solution(orders, plan.assignments, project_context)


# transforms an order list and an assignments list into a project plan
def transform_primitive_orders_and_assignments_to_solution(orders: list[int], assignments: list[dict[int, set[int]]],
                                                           project_context: DetailedProjectContext) -> BasicProjectPlan:
    project_activities = project_context.activities
    project_nr_activities = project_context.nr_activities
    project_plan = BasicProjectPlan()
    activities_end_time = calculate_primitive_orders_representation_end_times(orders, assignments, project_context)
    project_plan.activities_start_times = [activities_end_time[i] - project_activities[i].duration
                                           for i in range(project_nr_activities)]
    project_plan.assignments = copy.deepcopy(assignments)  # deep copy such that the actual list is not affected
    return project_plan
