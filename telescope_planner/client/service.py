import requests
from fastapi.encoders import jsonable_encoder

from input_utils import msrcp_converter, read_project_context
from input_utils.utils import MsrcpspFileException
from msrcpsp.project_context import BasicProjectContext
from msrcpsp.project_plan import DetailedProjectPlan
from telescope_planner.client.utils import ServiceException
from telescope_planner.commons.dto import ProjectPlanDTO, ProjectPlanningRequestDTO, ErrorDTO
from telescope_planner.commons.dto_utils import transform_basic_project_context_to_project_context_dto, \
    transform_project_plan_dto_to_detailed_project_plan


class Service:
    def __init__(self, server_name: str, server_port: str, root_path: str = "."):
        self.__server_name = server_name
        self.__server_port = server_port
        self.__root_path = root_path
        self.__api_url = "http://" + server_name + ":" + server_port

    def __add_root_path_to_filename(self, filename: str) -> str:
        return self.__root_path + "/" + filename

    def convert_from_msrcp(self, source_filename: str, destination_filename: str):
        try:
            source_filename = self.__add_root_path_to_filename(source_filename)
            destination_filename = self.__add_root_path_to_filename(destination_filename)
            msrcp_converter.convert(source_filename, destination_filename)
        except MsrcpspFileException as e:
            raise ServiceException(str(e))

    def generate_plan(self, source_filename: str, destination_filename: str, time_limit_as_string: str):
        time_limit = self.__convert_string_time_limit(time_limit_as_string)
        project_context = self.__get_project_context_from_file(source_filename)
        detailed_plan = self.__generate_plan_for_context(project_context, time_limit)
        self.__write_plan_to_file(detailed_plan, destination_filename)

    def __convert_string_time_limit(self, time_limit_as_string: str) -> float:
        try:
            time_limit = float(time_limit_as_string)
            if time_limit < 1:
                raise ValueError()
        except Exception:
            raise ServiceException("Error: Time limit should be a positive real number;")
        return time_limit

    def __get_project_context_from_file(self, source_filename) -> BasicProjectContext:
        source_filename = self.__add_root_path_to_filename(source_filename)
        try:
            project_context = read_project_context.read_project_context_from_file(source_filename)
        except MsrcpspFileException as e:
            raise ServiceException(str(e))
        return project_context

    def __generate_plan_for_context(self, project_context: BasicProjectContext, time_limit: float) \
            -> DetailedProjectPlan:
        api_endpoint = self.__api_url + "/plans"

        project_context_dto = transform_basic_project_context_to_project_context_dto(project_context)
        request_dto = ProjectPlanningRequestDTO(time_limit=time_limit,
                                                project_context=project_context_dto)

        response = requests.post(api_endpoint, json=jsonable_encoder(request_dto))
        if response.status_code == 400:
            api_error_messages = (ErrorDTO.parse_raw(response.text)).detail
            error_message = ""
            for api_error_message in api_error_messages:
                error_message += api_error_message + "\n"
            error_message = error_message[:-1]
            raise ServiceException(error_message)
        elif response.status_code != 201:
            raise ServiceException("Error: communication with server failed;")

        plan_dto = ProjectPlanDTO.parse_raw(response.text)
        return transform_project_plan_dto_to_detailed_project_plan(plan_dto)

    def __write_plan_to_file(self, plan: DetailedProjectPlan, destination_filename: str):
        destination_filename = self.__add_root_path_to_filename(destination_filename)
        try:
            destination_file = open(destination_filename, "w")
            destination_file.write(str(plan))
            destination_file.close()
        except Exception:
            raise ServiceException("Error: couldn't work with the destination file;")
