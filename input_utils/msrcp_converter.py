from input_utils.utils import skip_lines, MsrcpspFileException


# this function converts a file from msrcp format to my own specified format (see problem_input_data folder for
# specified formats)
def convert(source_file_name: str, destination_file_name: str) -> None:
    result = ""
    try:
        with open(source_file_name, "r") as source_file:
            # Convert the Project Module
            skip_lines(source_file, 1)
            line = source_file.readline()
            nr_activities, nr_resources, nr_skill_types, _ = [int(elem) for elem in line.split()]
            result += "Nr. Activities|Nr. Resources|Nr. Skills Types\n"
            result += str(nr_activities) + "\t" + str(nr_resources) + "\t" + str(nr_skill_types) + "\n"
            skip_lines(source_file, 1)
            result += "Deadline\n"
            result += source_file.readline()
            skip_lines(source_file, 3)

            result += "Activities\n"
            result += "Duration|Nr. Successors|Successors\n"
            for i in range(nr_activities):
                result += source_file.readline()
            skip_lines(source_file, 2)

            # Convert the Workforce Module
            result += "Resources Skill Mastery\n"
            for i in range(nr_resources):
                result += source_file.readline()
            skip_lines(source_file, 2)

            # Convert the Workforce Module with Skill Levels
            skip_lines(source_file, nr_resources + 2)

            # Convert the Skill Requirements Module
            result += "Activities Skill Requirements\n"
            for i in range(nr_activities):
                line = source_file.readline()
                result += line
            skip_lines(source_file, 2)
            # The rest is not concerned
    except ValueError:
        raise MsrcpspFileException("Error: source file might not respect format;")
    except Exception:
        raise MsrcpspFileException("Error: couldn't work with the source file;")
    try:
        with open(destination_file_name, "w") as destination_file:
            destination_file.write(result)
            destination_file.close()
    except Exception:
        raise MsrcpspFileException("Error: couldn't work with the destination file;")
