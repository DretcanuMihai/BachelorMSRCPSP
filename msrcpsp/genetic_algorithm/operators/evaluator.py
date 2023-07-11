from msrcpsp.genetic_algorithm.representation import GAProjectPlan
from msrcpsp.genetic_algorithm.utils import calculate_primitive_orders_representation_end_times, \
    transform_priorities_to_orders
from msrcpsp.project_context import DetailedProjectContext


def evaluate_orders_representation(individual: GAProjectPlan, project_context: DetailedProjectContext) -> int:
    return max(calculate_primitive_orders_representation_end_times(individual.activities, individual.assignments,
                                                                   project_context))


def evaluate_priorities_representation(individual: GAProjectPlan, project_context: DetailedProjectContext) -> int:
    resource_assignments = individual.assignments
    priorities = individual.activities
    orders = transform_priorities_to_orders(priorities, project_context)
    return max(calculate_primitive_orders_representation_end_times(orders, resource_assignments, project_context))
