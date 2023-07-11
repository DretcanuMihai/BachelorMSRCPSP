class MsrcpspFileException(Exception):
    pass


# skips the specified amount of lines from a source file
def skip_lines(source_file, nr_lines: int) -> None:
    for i in range(nr_lines):
        source_file.readline()
