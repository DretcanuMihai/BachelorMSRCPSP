import os
import subprocess

from msrcpsp.genetic_algorithm.representation import PRIORITY_REPRESENTATION, ORDER_REPRESENTATION


def __create_dir_if_not_exists(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


nr_testcases = 10
nr_runs = 10
for case_index in range(1, nr_testcases + 1):
    print("Case " + str(case_index))

    case_file_name = "../../data/problem_input_data/converted/case" + str(case_index) + ".txt"
    report_dir_name = "../../data/reports/case" + str(case_index)
    __create_dir_if_not_exists(report_dir_name)

    for representation in [ORDER_REPRESENTATION, PRIORITY_REPRESENTATION]:
        if representation == ORDER_REPRESENTATION:
            representation_str = "order"
        else:
            representation_str = "priority"
        print("\tRepresentation " + representation_str)

        representation_dir_name = report_dir_name + "/" + representation_str
        __create_dir_if_not_exists(representation_dir_name)

        for run_number in range(1, nr_runs + 1):
            print("\t\tRun Number " + str(run_number))
            report_file_name = representation_dir_name + "/run" + str(run_number) + ".csv"
            subprocess.run(["python", "run_single_test_case.py", case_file_name, report_file_name, representation])
