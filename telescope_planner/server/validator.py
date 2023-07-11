from telescope_planner.commons.dto import ProjectContextDTO, ProjectPlanningRequestDTO


class Validator:

    def __init__(self,
                 time_limit_upperbound=60,
                 activities_number_upperbound=40,
                 skill_number_upperbound=10,
                 resources_number_upperbound=20,
                 activity_duration_upperbound=366,
                 skill_amount_needed_upperbound=10):
        self.__time_limit_upperbound = time_limit_upperbound
        self.__activities_number_upperbound = activities_number_upperbound
        self.__skill_number_upperbound = skill_number_upperbound
        self.__resources_number_upperbound = resources_number_upperbound
        self.__activity_duration_upperbound = activity_duration_upperbound
        self.__skill_amount_needed_upperbound = skill_amount_needed_upperbound

    def validate(self, planning_request: ProjectPlanningRequestDTO) -> list[str]:
        errors = []
        errors += self.__validate_time_limit(planning_request.time_limit)
        errors += self.__validate_project_context(planning_request.project_context)
        return errors

    def __validate_time_limit(self, time_limit) -> list[str]:
        errors = []
        if time_limit < 1 or time_limit > self.__time_limit_upperbound:
            errors.append(
                "Error: time limit should be between 1 and " + str(self.__time_limit_upperbound) + " seconds;")
        return errors

    def __validate_project_context(self, project_context: ProjectContextDTO) -> list[str]:
        errors = []
        nr_activities = len(project_context.activities)
        nr_skills = project_context.nr_skills
        nr_resources = len(project_context.resources)

        if nr_activities < 1 or nr_activities > self.__activities_number_upperbound:
            errors.append("Error: project number of activities should be between 1 and " +
                          str(self.__activities_number_upperbound) + ";")
        if nr_skills < 0 or nr_skills > self.__skill_number_upperbound:
            errors.append("Error: project number of skills should be between 0 and "
                          + str(self.__skill_number_upperbound) + ";")
        if nr_resources < 0 or nr_resources > self.__resources_number_upperbound:
            errors.append("Error: project number of resources should be between 0 and "
                          + str(self.__resources_number_upperbound) + ";")
        if len(errors) > 0:
            return errors

        skills = set([elem for elem in range(nr_skills)])
        activities = set([elem for elem in range(nr_activities)])

        for index, activity in enumerate(project_context.activities):
            if activity.duration < 0 or activity.duration > self.__activity_duration_upperbound:
                errors.append("Error: activity " + str(index) + " duration must be between 0 and " +
                              str(self.__activity_duration_upperbound) + ";")
            if not activity.successors.issubset(activities) or index in activity.successors:
                errors.append("Error: activity " + str(index) + " has invalid dependencies;")
            skills_required = set(activity.skill_requirements.keys())
            if not skills_required.issubset(skills):
                errors.append("Error: activity " + str(index) + " has invalid skills required;")
            else:
                for skill in skills_required:
                    amount_needed = activity.skill_requirements[skill]
                    if amount_needed < 1 or amount_needed > self.__skill_amount_needed_upperbound:
                        errors.append("Error: activity " + str(index) + " should have a required skill amount for " +
                                      str(skill) + " between 1 and " + str(self.__skill_amount_needed_upperbound) + ";")

        for index, resource in enumerate(project_context.resources):
            if not resource.skills.issubset(skills):
                errors.append("Error: resource " + str(index) + " masters invalid skills;")

        return errors
