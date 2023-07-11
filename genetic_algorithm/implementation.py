import time

from genetic_algorithm.general import MINIMIZING_PROBLEM, Candidate

PROBLEM_TYPE = "problem_type"
POPULATION_SIZE = "initial_population_size"
REPRODUCTIONS_PER_GENERATION = "reproductions_per_generation"
RANDOM = "random"
CONTEXT = "context"
GENERATOR_FUNCTION = "generator_fun"
EVALUATOR_FUNCTION = "evaluator_fun"
STOP_CRITERION = "stop_criterion_fun"
SELECTOR_FUNCTION = "selector_fun"
CROSSOVER_FUNCTION = "crossover_fun"
MUTATOR_FUNCTION = "mutator_fun"
REPLACER_FUNCTION = "replacer_fun"

# Documentation and
# nc means non-conforming - that means that the method doesn't respect arguments constraints
# the functions should not modify the state of their input arguments, the only exception being Random objects
# __Context__ -> an entity that represents the extra needed data for the problem - can be any type, even none
# __Representation__ -> an entity that represents the chosen representation - also called individual
# __ProblemType__ -> MAXIMIZING_PROBLEM or MINIMIZING_PROBLEM
SAMPLE_ARGS = {
    PROBLEM_TYPE: None,  # either MAXIMIZING_PROBLEM or MINIMIZING_PROBLEM, depending on problem
    POPULATION_SIZE: None,  # the size of the initial population
    REPRODUCTIONS_PER_GENERATION: None,  # the number of reproductions that should be done per generation
    RANDOM: None,  # the random number generator used
    CONTEXT: None,  # the context of the problem - it can be any data type
    GENERATOR_FUNCTION: None,  # generate(Random,__Context__) : __Representation__
    # generates a valid solution representation
    EVALUATOR_FUNCTION: None,  # evaluate(__Representation__,__Context__): number
    # calculates the fitness of the representation
    STOP_CRITERION: None,  # should_stop(GeneticAlgorithm):boolean
    # it returns true if the stop criterion for an algorithm is reached, or false otherwise
    SELECTOR_FUNCTION: None,  # select(list[Candidate],Random,__ProblemType__): list[Candidate]
    # randomly selects some candidates from a pool sorted from best to worst
    CROSSOVER_FUNCTION: None,  # cross(list[__Representation__],Random,__Context__): list[__Representation__]
    # crosses some representations and returns the offsprings
    MUTATOR_FUNCTION: None,  # mutate(__Representation__,Random,__Context__): __Representation__
    # mutates a given representation
    REPLACER_FUNCTION: None  # replace(list[Candidate],list[Candidate],Random,__ProblemType__): list[Candidate] np
    # the first list represents the current population. the second list are the current offsprings. both lists
    # are sorted best to worst. the function returns the candidates that form the new generation.
}


# creates a dictionary of arguments like the sample dictionary
def create_genetic_algorithm_args(problem_type,
                                  population_size,
                                  reproductions_per_generation,
                                  random,
                                  context,
                                  generator_function,
                                  evaluator_function,
                                  stop_criterion,
                                  selector_function,
                                  crossover_function,
                                  mutator_function,
                                  replacer_function):
    return {
        PROBLEM_TYPE: problem_type,
        POPULATION_SIZE: population_size,
        REPRODUCTIONS_PER_GENERATION: reproductions_per_generation,
        RANDOM: random,
        CONTEXT: context,
        GENERATOR_FUNCTION: generator_function,
        EVALUATOR_FUNCTION: evaluator_function,
        STOP_CRITERION: stop_criterion,
        SELECTOR_FUNCTION: selector_function,
        CROSSOVER_FUNCTION: crossover_function,
        MUTATOR_FUNCTION: mutator_function,
        REPLACER_FUNCTION: replacer_function
    }


class GeneticAlgorithm:

    def __init__(self,
                 problem_type,
                 population_size,
                 reproductions_per_generation,
                 random,
                 context,
                 generator_function,
                 evaluator_function,
                 stop_criterion,
                 selector_function,
                 crossover_function,
                 mutator_function,
                 replacer_function):
        self.__population = []
        self.__nr_generations = 0
        self.__start_time = 0
        self.__problem_type = problem_type
        self.__sort_reversed = True
        if self.__problem_type is MINIMIZING_PROBLEM:
            self.__sort_reversed = False
        self.__population_size = population_size
        self.__reproductions_per_generation = reproductions_per_generation
        self.__random = random
        self.__context = context
        self.__generate = generator_function
        self.__evaluate = evaluator_function
        self.__should_stop = stop_criterion
        self.__select = selector_function
        self.__cross = crossover_function
        self.__mutate = mutator_function
        self.__replace = replacer_function

    def get_population(self):
        return self.__population

    def get_nr_generations(self):
        return self.__nr_generations

    def get_start_time(self):
        return self.__start_time

    def get_elapsed_time(self):
        return time.time() - self.__start_time

    def get_problem_type(self):
        return self.__problem_type

    def run(self):
        self.generate_initial_population()
        while not self.__should_stop(self):
            self.advance_to_next_generation()

    def generate_initial_population(self):
        self.__start_time = time.time()
        self.__population = [self.__generate(self.__random, self.__context) for _ in range(self.__population_size)]
        self.__population = self.__evaluate_and_rank_individuals(self.__population)
        self.__nr_generations = 0

    def advance_to_next_generation(self):
        current_offsprings = []
        for i in range(self.__reproductions_per_generation):
            selected_candidates = self.__select(self.__population, self.__random, self.__problem_type)
            individuals = [parent.representation for parent in selected_candidates]
            offsprings = self.__cross(individuals, self.__random, self.__context)
            offsprings = [self.__mutate(offspring, self.__random, self.__context) for offspring in offsprings]
            current_offsprings = current_offsprings + offsprings
        offspring_candidates = self.__evaluate_and_rank_individuals(current_offsprings)
        self.__population = self.__replace(self.__population, offspring_candidates, self.__random, self.__problem_type)
        self.__population = sorted(self.__population, key=(lambda c: c.fitness), reverse=self.__sort_reversed)
        self.__nr_generations += 1

    def __evaluate_and_rank_individuals(self, individuals):
        candidates = [Candidate(elem, self.__evaluate(elem, self.__context)) for elem in individuals]
        candidates = sorted(candidates, key=(lambda c: c.fitness), reverse=self.__sort_reversed)
        return candidates

    @staticmethod
    def create_from_args(args: dict):
        problem_type = args[PROBLEM_TYPE]
        population_size = args[POPULATION_SIZE]
        reproductions_per_generation = args[REPRODUCTIONS_PER_GENERATION]
        random = args[RANDOM]
        context = args[CONTEXT]
        generator_function = args[GENERATOR_FUNCTION]
        evaluator_function = args[EVALUATOR_FUNCTION]
        stop_criterion = args[STOP_CRITERION]
        selector_function = args[SELECTOR_FUNCTION]
        crossover_function = args[CROSSOVER_FUNCTION]
        mutator_function = args[MUTATOR_FUNCTION]
        replacer_function = args[REPLACER_FUNCTION]

        return GeneticAlgorithm(
            problem_type=problem_type,
            population_size=population_size,
            reproductions_per_generation=reproductions_per_generation,
            random=random,
            context=context,
            generator_function=generator_function,
            evaluator_function=evaluator_function,
            stop_criterion=stop_criterion,
            selector_function=selector_function,
            crossover_function=crossover_function,
            mutator_function=mutator_function,
            replacer_function=replacer_function
        )
