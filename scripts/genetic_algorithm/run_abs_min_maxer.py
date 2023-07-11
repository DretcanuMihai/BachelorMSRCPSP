from random import Random

from genetic_algorithm.general import MAXIMIZING_PROBLEM
from genetic_algorithm.implementation import GeneticAlgorithm, create_genetic_algorithm_args
from genetic_algorithm.operators.crossover import cross_permutations_one_point
from genetic_algorithm.operators.generator import create_permutations_generator_function
from genetic_algorithm.operators.mutator import mutate_permutations_by_interchange
from genetic_algorithm.operators.replacer import replace_steady_state
from genetic_algorithm.operators.selector import create_tournament_selector_function
from genetic_algorithm.operators.stop_criterion import create_timed_stop_criterion

random = Random(2300)
n = 10
values = [i * 10 for i in range(n)]


def evaluate(p, context=None):
    p = [p_elem for p_elem in p]
    result = abs(values[p[0]] - values[p[-1]])
    for i in range(len(p) - 1):
        result += abs(values[p[i]] - values[p[i + 1]])
    return result


args = create_genetic_algorithm_args(
    problem_type=MAXIMIZING_PROBLEM,
    population_size=n // 2,
    reproductions_per_generation=2,
    random=random,
    context=None,
    generator_function=create_permutations_generator_function(n),
    evaluator_function=evaluate,
    stop_criterion=create_timed_stop_criterion(2),
    selector_function=create_tournament_selector_function(2, 4),
    crossover_function=cross_permutations_one_point,
    mutator_function=mutate_permutations_by_interchange,
    replacer_function=replace_steady_state
)

ga = GeneticAlgorithm.create_from_args(args)
ga.run()

for elem in ga.get_population()[0:5]:
    print(str(elem.fitness) + " " + str(elem.representation) + "\n")
