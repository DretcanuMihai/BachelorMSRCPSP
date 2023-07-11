from genetic_algorithm.operators.stop_criterion import create_timed_stop_criterion, \
    create_generational_stop_criterion, create_fitness_stop_criterion
from msrcpsp.project_context import transform_basic_project_context_to_detailed_project_context
from input_utils.read_project_context import read_project_context_from_file
from msrcpsp.genetic_algorithm.builder import create_ga
from msrcpsp.genetic_algorithm.representation import PRIORITY_REPRESENTATION, ORDER_REPRESENTATION

# problem input
filename = "../../data/problem_input_data/converted/case2.txt"
project_context = transform_basic_project_context_to_detailed_project_context(read_project_context_from_file(filename))

# stop criteria definition
timed_stop_criterion = create_timed_stop_criterion(3)
generational_stop_criterion = create_generational_stop_criterion(100)
fitness_stop_criterion = create_fitness_stop_criterion(project_context.deadline)

# arguments
representation = PRIORITY_REPRESENTATION
stop_criterion = timed_stop_criterion

ga = create_ga(project_context=project_context,
               representation=representation,
               should_validate_candidates=True,
               stop_criterion=stop_criterion)
ga.run()

print("GOOD" if ga.get_population()[0].fitness <= project_context.deadline else "BAD")
print("Normal Deadline " + str(project_context.deadline))
print("Time " + str(ga.get_elapsed_time()))
print("Generation " + str(ga.get_nr_generations()))
for elem in ga.get_population()[0:1]:
    print(str(elem.fitness) + " " + str(elem.representation) + "\n")
