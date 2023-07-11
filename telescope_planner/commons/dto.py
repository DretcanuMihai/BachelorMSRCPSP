from pydantic import BaseModel


class ProjectContextActivityDTO(BaseModel):
    duration: int
    successors: set[int]
    skill_requirements: dict[int, int]


class ProjectContextResourceDTO(BaseModel):
    skills: set[int]


class ProjectContextDTO(BaseModel):
    nr_skills: int
    resources: list[ProjectContextResourceDTO]
    activities: list[ProjectContextActivityDTO]


class ProjectPlanningRequestDTO(BaseModel):
    project_context: ProjectContextDTO
    time_limit: float


class ProjectPlanActivityDTO(BaseModel):
    start_time: int
    duration: int
    end_time: int
    resources_assigned_for_skill: dict[int, set[int]]


class ProjectPlanResourceDTO(BaseModel):
    skill_used_in_activity: dict[int, int]


class ProjectPlanDTO(BaseModel):
    activities: list[ProjectPlanActivityDTO]
    resources: list[ProjectPlanResourceDTO]


class ErrorDTO(BaseModel):
    detail: list[str]
