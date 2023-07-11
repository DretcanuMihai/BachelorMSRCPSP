from genetic_algorithm.operators.stop_criterion import create_timed_stop_criterion
from msrcpsp.genetic_algorithm.builder import create_ga
from msrcpsp.genetic_algorithm.representation import PRIORITY_REPRESENTATION, ORDER_REPRESENTATION
from msrcpsp.genetic_algorithm.utils import transform_orders_to_solution, transform_priorities_to_solution
from msrcpsp.project_context import DetailedProjectContext
from msrcpsp.project_plan import DetailedProjectPlan, transform_basic_plan_to_detailed_plan


class Service:

    def generate_project_plan(self, project_context: DetailedProjectContext, time_limit: float) \
            -> DetailedProjectPlan:
        # some projects work better with other representations. we can add a method to determine which representation
        # would work better, if such analysis can be done
        representation = ORDER_REPRESENTATION
        genetic_algorithm = create_ga(project_context=project_context,
                                      representation=representation,
                                      stop_criterion=create_timed_stop_criterion(time_limit))
        genetic_algorithm.run()
        best_solution_representation = genetic_algorithm.get_population()[0].representation
        if representation == PRIORITY_REPRESENTATION:
            basic_plan = transform_orders_to_solution(best_solution_representation, project_context)
        else:
            basic_plan = transform_priorities_to_solution(best_solution_representation, project_context)
        return transform_basic_plan_to_detailed_plan(basic_plan, project_context)
