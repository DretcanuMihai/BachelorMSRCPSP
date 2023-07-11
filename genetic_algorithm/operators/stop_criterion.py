from typing import Union

from genetic_algorithm.implementation import GeneticAlgorithm
from genetic_algorithm.general import MAXIMIZING_PROBLEM


# generates a function that with each call increases the current generation number
# when called, if the current generation didn't reach the specified limit, it returns true, otherwise false
def create_generational_stop_criterion(nr_generations: int):
    def should_stop(genetic_algorithm: GeneticAlgorithm) -> bool:
        return genetic_algorithm.get_nr_generations() >= nr_generations

    return should_stop


# generates a function that represents a timed stop criterion
# when first called, it starts said timer.
# when called, it returns true if the specified duration elapsed, false otherwise
def create_timed_stop_criterion(duration: float):
    def should_stop(genetic_algorithm: GeneticAlgorithm) -> bool:
        return genetic_algorithm.get_elapsed_time() >= duration

    return should_stop


# generates a function that represents a convergence stop criterion
# when called, it checks if the best member of the population reached the specified fitness
def create_fitness_stop_criterion(fitness: Union[int, float]):
    def should_stop(genetic_algorithm: GeneticAlgorithm) -> bool:
        population = genetic_algorithm.get_population()
        problem_type = genetic_algorithm.get_problem_type()
        f1 = population[0].fitness
        if problem_type is MAXIMIZING_PROBLEM:
            return f1 >= fitness
        else:
            return f1 <= fitness

    return should_stop
