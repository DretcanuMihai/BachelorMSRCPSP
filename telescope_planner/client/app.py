from telescope_planner.client.utils import ServiceException
from telescope_planner.client.service import Service


class App:

    def __init__(self, service: Service):
        self.__service = service
        self.__running = False
        self.__commands_dict = self.__get_commands_dict()

    def __show_menu(self):
        print("0. 'menu' - shows the available commands")
        print("1. 'convert_from_msrcp' - converts a file from 'msrcp' to the valid format")
        print("2. 'generate_plan' - generates a plan for a valid file")
        print("3. 'exit' - exists the program")

    def __convert_from_msrcp(self):
        print("Enter the name of the source file;")
        source_filename = input(">")
        print("Enter the name of the destination file;")
        destination_filename = input(">")
        self.__service.convert_from_msrcp(source_filename, destination_filename)
        print("File converted;")

    def __generate_plan(self):
        print("Enter the name of the source file;")
        source_filename = input(">")
        print("Enter the name of the destination file;")
        destination_filename = input(">")
        print("Enter the time limit in seconds;")
        time_limit_as_string = input(">")
        self.__service.generate_plan(source_filename, destination_filename, time_limit_as_string)
        print("Plan generated;")

    def __stop_running(self):
        self.__running = False

    def __get_commands_dict(self):
        commands_dict = {
            "menu": self.__show_menu,
            "convert_from_msrcp": self.__convert_from_msrcp,
            "generate_plan": self.__generate_plan,
            "exit": self.__stop_running
        }
        return commands_dict

    def run(self):
        self.__running = True
        print("Telescope Planner client started; Type 'menu' to see available commands;")
        while self.__running:
            command = input(">>>")
            if command in self.__commands_dict:
                try:
                    self.__commands_dict[command]()
                except ServiceException as e:
                    print(str(e))
                except Exception:
                    print("Error: An unexpected internal error occurred;")
            else:
                print("Invalid command; Use 'menu' to see available commands;")
        print("Telescope Planner client stopped;")
