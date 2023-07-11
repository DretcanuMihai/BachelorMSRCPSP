from input_utils.utils import skip_lines, MsrcpspFileException
from msrcpsp.project_context import BasicProjectContext


# reads the information of the problem from a specified file
def read_project_context_from_file(source_filename: str) -> BasicProjectContext:
    try:
        with open(source_filename, "r") as source_file:
            problem_details = BasicProjectContext()

            # general details
            skip_lines(source_file, 1)
            line = source_file.readline()
            [nr_activities, nr_resources, nr_skill_types] = [int(elem) for elem in line.split()]
            problem_details.nr_activities = nr_activities
            problem_details.nr_resources = nr_resources
            problem_details.nr_skill_types = nr_skill_types

            # deadline
            skip_lines(source_file, 1)
            line = source_file.readline()
            deadline = int(line)
            problem_details.deadline = deadline

            # activities details
            skip_lines(source_file, 2)
            for _ in range(nr_activities):
                line = source_file.readline()
                line_as_ints = [int(elem) for elem in line.split()]
                problem_details.activities_durations.append(line_as_ints[0])
                problem_details.activities_successors.append(set([elem - 1 for elem in line_as_ints[2:]]))

            # resources details
            skip_lines(source_file, 1)
            for _ in range(nr_resources):
                problem_details.resource_skills.append(set())
                line = source_file.readline()
                line_as_ints = [int(elem) for elem in line.split()]
                for skill_index in range(nr_skill_types):
                    if line_as_ints[skill_index] == 1:
                        problem_details.resource_skills[-1].add(skill_index)

            # activities skill requirements
            skip_lines(source_file, 1)
            for activity_index in range(nr_activities):
                problem_details.activities_skills_requirements.append({})
                line = source_file.readline()
                line_as_ints = [int(elem) for elem in line.split()]
                for skill_index in range(nr_skill_types):
                    if line_as_ints[skill_index] != 0:
                        problem_details.activities_skills_requirements[activity_index][skill_index] = line_as_ints[
                            skill_index]

            source_file.close()
            return problem_details
    except ValueError:
        raise MsrcpspFileException("Error: source file might not respect format;")
    except Exception:
        raise MsrcpspFileException("Error: couldn't work with the source file;")
