import matplotlib.pyplot as plt
import pandas
from pandas import DataFrame

from input_utils.read_project_context import read_project_context_from_file

ORDER_ACCURATE_RUN = {
    1: 2,
    2: 2,
    3: 1,
    4: 1,
    5: 8,
    6: 2,
    7: 3,
    8: 3,
    9: 4,
    10: 2
}

PRIORITY_ACCURATE_RUN = {
    1: 1,
    2: 1,
    3: 2,
    4: 3,
    5: 5,
    6: 2,
    7: 6,
    8: 6,
    9: 9,
    10: 1
}

BEST_FITNESS = "Best Fitness"
AVERAGE_FITNESS = "Average Fitness"
ELAPSED_TIME = "Elapsed Time"
GENERATION_NUMBER = "Generation Number"

SDGNT = "SDGNT"  # standard deviation generation numbers table
FCT = "FCT"  # fitness comparison table
GNBF = "GNBF"
GNAF = "GNAF"
ETBF = "ETBF"
ETAF = "ETAF"
ETGN = "ETGN"

ORDER_REPRESENTATION = "Order"
PRIORITY_REPRESENTATION = "Priority"
TARGET_VALUE = "Target Value"
TEST_CASE = "Test Case"

NR_TEST_CASES = 10
NR_RUNS = 10

MODE = GNBF


def generate_standard_deviation_generation_number_table():
    all_results = {TEST_CASE: [], ORDER_REPRESENTATION: [], PRIORITY_REPRESENTATION: []}
    for case_index in range(1, NR_TEST_CASES + 1):
        all_results[TEST_CASE].append("Case " + str(case_index))
        for representation in [ORDER_REPRESENTATION, PRIORITY_REPRESENTATION]:
            nr_of_generations_list = []
            for run_index in range(1, NR_RUNS + 1):
                report_data = pandas.read_csv("../../data/reports/case" + str(case_index) + "/" + representation.lower()
                                              + "/run" + str(run_index) + ".csv")
                nr_of_generations_list.append(len(report_data))
            mean_value = sum(nr_of_generations_list) / NR_RUNS
            std_deviation = (sum([(mean_value - nr_gens) ** 2 for nr_gens in nr_of_generations_list]) / NR_RUNS) ** (
                    1 / 2)
            all_results[representation].append(str(mean_value) + "+/-" + str(std_deviation))
    results_dataframe = DataFrame.from_dict(all_results)
    results_dataframe.to_csv("../../data/reports/std_gen_table.csv")


def generate_fitness_table():
    all_results = {TEST_CASE: [], TARGET_VALUE: []}
    for value_field in [BEST_FITNESS, AVERAGE_FITNESS]:
        for representation in [ORDER_REPRESENTATION, PRIORITY_REPRESENTATION]:
            all_results[representation + " " + value_field] = []
    for case_index in range(1, NR_TEST_CASES + 1):
        all_results[TEST_CASE].append("Case " + str(case_index))
        case_filename = "../../data/problem_input_data/converted/case" + str(case_index) + ".txt"
        project_context = read_project_context_from_file(case_filename)
        all_results[TARGET_VALUE].append(project_context.deadline)
        for value_field in [BEST_FITNESS, AVERAGE_FITNESS]:
            for representation in [ORDER_REPRESENTATION, PRIORITY_REPRESENTATION]:
                if representation == ORDER_REPRESENTATION:
                    run_index = ORDER_ACCURATE_RUN[case_index]
                else:
                    run_index = PRIORITY_ACCURATE_RUN[case_index]
                report_data = pandas.read_csv("../../data/reports/case" + str(case_index) + "/" + representation.lower()
                                              + "/run" + str(run_index) + ".csv")
                report_value = report_data.iloc[-1][value_field]
                all_results[representation + " " + value_field].append(report_value)
    results_dataframe = DataFrame.from_dict(all_results)
    results_dataframe.to_csv("../../data/reports/fitness_table.csv")


def plot_single_report_data(report_data, representation, x_label, y_label):
    plt.plot(report_data[x_label], report_data[y_label], label=representation)


def plot_reports_data(case_index, report_order_data, report_priority_data, x_label, y_label, deadline_value=None):
    plt.title(y_label + " By " + x_label + " Comparison Case " + str(case_index))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plot_single_report_data(report_order_data, ORDER_REPRESENTATION, x_label, y_label)
    plot_single_report_data(report_priority_data, PRIORITY_REPRESENTATION, x_label, y_label)
    if deadline_value is not None:
        plt.axhline(y=deadline_value, color='r', linestyle='-', label="Deadline")
    plt.legend()
    plt.show()


def plot_comparison_for_case(comparison_type, case_index, order_run_index, priority_run_index):
    order_data = pandas.read_csv("../../data/reports/case" + str(case_index) + "/order/run"
                                 + str(order_run_index) + ".csv")
    priority_data = pandas.read_csv("../../data/reports/case" + str(case_index) + "/priority/run"
                                    + str(priority_run_index) + ".csv")
    filename = "../../data/problem_input_data/converted/case" + str(case_index) + ".txt"
    project_context = read_project_context_from_file(filename)
    deadline = project_context.deadline
    if comparison_type == GNBF:
        plot_reports_data(case_index, order_data, priority_data, GENERATION_NUMBER, BEST_FITNESS, deadline)
    elif comparison_type == GNAF:
        plot_reports_data(case_index, order_data, priority_data, GENERATION_NUMBER, AVERAGE_FITNESS, deadline)
    elif comparison_type == ETBF:
        plot_reports_data(case_index, order_data, priority_data, ELAPSED_TIME, BEST_FITNESS, deadline)
    elif comparison_type == ETAF:
        # it's fuzzy
        plot_reports_data(case_index, order_data, priority_data, ELAPSED_TIME, AVERAGE_FITNESS, deadline)
    elif comparison_type == ETGN:
        plot_reports_data(case_index, order_data, priority_data, ELAPSED_TIME, GENERATION_NUMBER)


def plot_all_accurate_comparisons(comparison_type):
    for index in range(1, NR_TEST_CASES + 1):
        plot_comparison_for_case(comparison_type, index, ORDER_ACCURATE_RUN[index], PRIORITY_ACCURATE_RUN[index])


if MODE == SDGNT:
    generate_standard_deviation_generation_number_table()
elif MODE == FCT:
    generate_fitness_table()
else:
    plot_all_accurate_comparisons(MODE)
