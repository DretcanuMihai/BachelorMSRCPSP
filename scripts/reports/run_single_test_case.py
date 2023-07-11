import sys
from typing import IO, Union

from genetic_algorithm.implementation import GeneticAlgorithm, STOP_CRITERION
from input_utils.read_project_context import read_project_context_from_file
from msrcpsp.genetic_algorithm.builder import create_ga_args
from msrcpsp.project_context import transform_basic_project_context_to_detailed_project_context


def __create_report_function(file_handle: IO):
    file_handle.write("Generation Number,Elapsed Time,Best Fitness,Average Fitness\n")

    def report(generation_number: int, elapsed_time: float, best_fitness: Union[float, int],
               average_fitness: Union[float, int]):
        file_handle.write(str(generation_number) + "," + str(elapsed_time) + "," + str(best_fitness) + "," +
                          str(average_fitness) + "\n")
        return

    return report


def __wrap_stop_criterion_with_report(stop_criterion_function, report_function):
    def should_stop(genetic_algorithm: GeneticAlgorithm):
        elapsed_time = genetic_algorithm.get_elapsed_time()
        del_should_stop = stop_criterion_function(genetic_algorithm)

        if not del_should_stop:
            generation_number = genetic_algorithm.get_nr_generations()
            population = genetic_algorithm.get_population()
            fitness_values = [candidate.fitness for candidate in population]
            best_fitness = fitness_values[0]
            average_fitness = sum(fitness_values) / len(fitness_values)
            report_function(generation_number, elapsed_time, best_fitness, average_fitness)

        return del_should_stop

    return should_stop


def execute_case(case_file_name: str, report_file_name: str, representation: str):
    project_context = transform_basic_project_context_to_detailed_project_context(
        read_project_context_from_file(case_file_name))

    report_file_handle = open(report_file_name, "w")
    file_report_function = __create_report_function(report_file_handle)

    ga_args = create_ga_args(project_context=project_context,
                             representation=representation)
    ga_args[STOP_CRITERION] = __wrap_stop_criterion_with_report(ga_args[STOP_CRITERION], file_report_function)

    ga = GeneticAlgorithm.create_from_args(ga_args)
    ga.run()
    report_file_handle.close()


# this module should only be called from command line or similar methods
# arguments: the name of the case file, the name of the output type, the used representation
if __name__ == "__main__":
    arg_case_file_name = sys.argv[1]
    arg_report_file_name = sys.argv[2]
    arg_representation = sys.argv[3]
    execute_case(arg_case_file_name, arg_report_file_name, arg_representation)
