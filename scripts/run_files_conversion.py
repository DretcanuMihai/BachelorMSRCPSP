from input_utils import msrcp_converter

nr_testcases = 10
for index in range(1, nr_testcases + 1):
    msrcp_converter.convert("../data/problem_input_data/original/MSLIB_Set2_" + str(index) + ".msrcp",
                            "../data/problem_input_data/converted/case" + str(index) + ".txt")
