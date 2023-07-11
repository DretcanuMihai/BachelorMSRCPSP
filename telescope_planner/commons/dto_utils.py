from msrcpsp.project_context import BasicProjectContext
from msrcpsp.project_plan import DetailedProjectPlan, DetailedProjectPlanActivity, DetailedProjectPlanResource
from telescope_planner.commons.dto import ProjectContextDTO, ProjectContextResourceDTO, ProjectContextActivityDTO
from telescope_planner.commons.dto import ProjectPlanDTO, ProjectPlanActivityDTO, ProjectPlanResourceDTO


def transform_project_context_dto_to_basic_project_context(project_context_dto: ProjectContextDTO) \
        -> BasicProjectContext:
    basic_project_context = BasicProjectContext()
    basic_project_context.nr_activities = len(project_context_dto.activities)
    basic_project_context.nr_resources = len(project_context_dto.resources)
    basic_project_context.nr_skill_types = project_context_dto.nr_skills

    for activity in project_context_dto.activities:
        basic_project_context.activities_durations.append(activity.duration)
        basic_project_context.activities_successors.append(activity.successors)
        basic_project_context.activities_skills_requirements.append(activity.skill_requirements)

    for resource in project_context_dto.resources:
        basic_project_context.resource_skills.append(resource.skills)
    return basic_project_context


def transform_basic_project_context_to_project_context_dto(basic_project_context: BasicProjectContext) \
        -> ProjectContextDTO:
    nr_skills = basic_project_context.nr_skill_types
    resources = []
    activities = []

    for resource in range(basic_project_context.nr_resources):
        skills = basic_project_context.resource_skills[resource]
        resources.append(ProjectContextResourceDTO(skills=skills))

    for activity in range(basic_project_context.nr_activities):
        duration = basic_project_context.activities_durations[activity]
        successors = basic_project_context.activities_successors[activity]
        skill_requirements = basic_project_context.activities_skills_requirements[activity]
        activities.append(ProjectContextActivityDTO(duration=duration,
                                                    successors=successors,
                                                    skill_requirements=skill_requirements))
    return ProjectContextDTO(nr_skills=nr_skills, activities=activities, resources=resources)


def transform_detailed_project_plan_to_project_plan_dto(detailed_plan: DetailedProjectPlan) \
        -> ProjectPlanDTO:
    activities = []
    for activity in detailed_plan.activities:
        activity_dto = ProjectPlanActivityDTO(start_time=activity.start_time,
                                              duration=activity.duration,
                                              end_time=activity.end_time,
                                              resources_assigned_for_skill=activity.resources_assigned_for_skill)
        activities.append(activity_dto)

    resources = []
    for resource in detailed_plan.resources:
        resource_dto = ProjectPlanResourceDTO(skill_used_in_activity=resource.skill_used_in_activity)
        resources.append(resource_dto)

    return ProjectPlanDTO(activities=activities, resources=resources)


def transform_project_plan_dto_to_detailed_project_plan(project_plan_dto: ProjectPlanDTO) -> DetailedProjectPlan:
    detailed_plan = DetailedProjectPlan()

    for activity in range(len(project_plan_dto.activities)):
        detailed_activity = DetailedProjectPlanActivity()
        detailed_activity.start_time = project_plan_dto.activities[activity].start_time
        detailed_activity.duration = project_plan_dto.activities[activity].duration
        detailed_activity.end_time = project_plan_dto.activities[activity].end_time
        detailed_activity.resources_assigned_for_skill = \
            project_plan_dto.activities[activity].resources_assigned_for_skill
        detailed_plan.activities.append(detailed_activity)

    for resource in range(len(project_plan_dto.resources)):
        detailed_resource = DetailedProjectPlanResource()
        detailed_resource.skill_used_in_activity = project_plan_dto.resources[resource].skill_used_in_activity
        detailed_plan.resources.append(detailed_resource)

    return detailed_plan
