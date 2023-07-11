from random import Random

from genetic_algorithm.general import MINIMIZING_PROBLEM
from genetic_algorithm.implementation import GeneticAlgorithm, create_genetic_algorithm_args
from genetic_algorithm.operators.mutator import create_probabilistic_mutator_function
from genetic_algorithm.operators.replacer import replace_steady_state
from genetic_algorithm.operators.selector import create_tournament_selector_function
from genetic_algorithm.operators.stop_criterion import create_timed_stop_criterion
from msrcpsp.genetic_algorithm.operators.crossover import cross_activities, cross_assignments, create_crossover_function
from msrcpsp.genetic_algorithm.operators.evaluator import evaluate_orders_representation, \
    evaluate_priorities_representation
from msrcpsp.genetic_algorithm.operators.generator import create_assignments_generator_function, \
    nc_generate_single_assignment, generate_orders, generate_priorities, create_generator_function
from msrcpsp.genetic_algorithm.operators.mutator import create_mutator_function, mutate_orders, mutate_priorities, \
    create_assignments_mutator_function
from msrcpsp.genetic_algorithm.representation import ORDER_REPRESENTATION, GAProjectPlan
from msrcpsp.genetic_algorithm.validator import create_validator_function, \
    create_assignments_validator_function, create_single_assignment_validator_function, validate_priorities, \
    validate_orders
from msrcpsp.project_context import DetailedProjectContext

BEST_SEED = 101  # seed with the best results


def create_ga(project_context: DetailedProjectContext,
              representation: str = ORDER_REPRESENTATION,
              should_validate_candidates: bool = False,
              population_size: int = 100,
              reproductions_per_generation: int = 45,
              random_seed: int = BEST_SEED,
              stop_criterion=create_timed_stop_criterion(60),
              selector_function=create_tournament_selector_function(2, 2),
              activities_mutation_probability: float = 0.1,
              assignments_mutation_probability: float = 0.25,
              replacer_function=replace_steady_state) -> GeneticAlgorithm:
    args = create_ga_args(project_context,
                          representation,
                          should_validate_candidates,
                          population_size,
                          reproductions_per_generation,
                          random_seed,
                          stop_criterion,
                          selector_function,
                          activities_mutation_probability,
                          assignments_mutation_probability,
                          replacer_function)
    return GeneticAlgorithm.create_from_args(args)


def create_ga_args(project_context: DetailedProjectContext,
                   representation: str = ORDER_REPRESENTATION,
                   should_validate_individuals: bool = False,
                   population_size: int = 300,
                   reproductions_per_generation: int = 145,
                   random_seed: int = BEST_SEED,
                   stop_criterion=create_timed_stop_criterion(60),
                   selector_function=create_tournament_selector_function(2, 2),
                   activities_mutation_probability: float = 0.1,
                   assignments_mutation_probability: float = 0.25,
                   replacer_function=replace_steady_state) -> dict:
    # generator
    generator_function = __create_generator_function(representation)

    # evaluator
    evaluator_function = __create_evaluator_function(representation)

    # crossover operators
    crossover_function = __create_crossover_function(representation)

    # mutators
    mutator_function = __create_mutator_function(representation, activities_mutation_probability,
                                                 assignments_mutation_probability)

    if should_validate_individuals:
        validator_function = __create_validator_function(representation)
        generator_function = __wrap_generator_with_validate(generator_function, validator_function)
        crossover_function = __wrap_crossover_with_validate(crossover_function, validator_function)
        mutator_function = __wrap_mutator_with_validate(mutator_function, validator_function)

    args = create_genetic_algorithm_args(
        problem_type=MINIMIZING_PROBLEM,
        population_size=population_size,
        reproductions_per_generation=reproductions_per_generation,
        random=Random(random_seed),
        context=project_context,
        generator_function=generator_function,
        evaluator_function=evaluator_function,
        stop_criterion=stop_criterion,
        selector_function=selector_function,
        crossover_function=crossover_function,
        mutator_function=mutator_function,
        replacer_function=replacer_function
    )
    return args


def __create_generator_function(representation):
    if representation == ORDER_REPRESENTATION:
        activities_generator_function = generate_orders
    else:
        activities_generator_function = generate_priorities
    assignments_generator_function = create_assignments_generator_function(nc_generate_single_assignment)
    generator_function = create_generator_function(activities_generator_function, assignments_generator_function)
    return generator_function


def __create_evaluator_function(representation):
    if representation == ORDER_REPRESENTATION:
        evaluator_function = evaluate_orders_representation
    else:
        evaluator_function = evaluate_priorities_representation
    return evaluator_function


def __create_crossover_function(representation):
    activities_crossover_function = cross_activities
    assignments_crossover_function = cross_assignments
    crossover_function = create_crossover_function(activities_crossover_function,
                                                   assignments_crossover_function)
    return crossover_function


def __create_mutator_function(representation, activities_mutation_probability, assignments_mutation_probability):
    if representation == ORDER_REPRESENTATION:
        activities_mutator_function = mutate_orders
    else:
        activities_mutator_function = mutate_priorities
    activities_mutator_function = create_probabilistic_mutator_function(
        activities_mutator_function,
        activities_mutation_probability
    )
    assignments_mutator_function = create_assignments_mutator_function(nc_generate_single_assignment)
    assignments_mutator_function = create_probabilistic_mutator_function(
        assignments_mutator_function,
        assignments_mutation_probability
    )
    mutator_function = create_mutator_function(activities_mutator_function, assignments_mutator_function)
    return mutator_function


def __create_validator_function(representation):
    if representation == ORDER_REPRESENTATION:
        activities_validator_function = validate_orders
    else:
        activities_validator_function = validate_priorities
    single_assignment_validator_function = create_single_assignment_validator_function()
    assignments_validator_function = create_assignments_validator_function(single_assignment_validator_function)
    validator_function = create_validator_function(activities_validator_function, assignments_validator_function)
    return validator_function


def __wrap_generator_with_validate(generator_function, validator_function):
    def generate_and_validate(random: Random, project_context: DetailedProjectContext) -> GAProjectPlan:
        result = generator_function(random, project_context)
        validator_function(result, project_context)
        return result

    return generate_and_validate


def __wrap_crossover_with_validate(crossover_function, validator_function):
    def cross_and_validate(parents: list[GAProjectPlan], random: Random, project_context: DetailedProjectContext) \
            -> list[GAProjectPlan]:
        result = crossover_function(parents, random, project_context)
        for elem in result:
            validator_function(elem, project_context)
        return result

    return cross_and_validate


def __wrap_mutator_with_validate(mutator_function, validator_function):
    def mutate_and_validate(individual: GAProjectPlan, random: Random, project_context: DetailedProjectContext) \
            -> GAProjectPlan:
        result = mutator_function(individual, random, project_context)
        validator_function(result, project_context)
        return result

    return mutate_and_validate
