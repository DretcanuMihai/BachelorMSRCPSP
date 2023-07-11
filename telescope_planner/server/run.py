import uvicorn
from fastapi import FastAPI, HTTPException

from msrcpsp.genetic_algorithm.utils import ProjectException
from msrcpsp.project_context import transform_basic_project_context_to_detailed_project_context
from telescope_planner.commons.dto_utils import transform_project_context_dto_to_basic_project_context, \
    transform_detailed_project_plan_to_project_plan_dto
from telescope_planner.commons.dto import ProjectPlanningRequestDTO, ProjectPlanDTO
from telescope_planner.server.service import Service
from telescope_planner.server.validator import Validator

# application components
validator = Validator()
service = Service()
app = FastAPI()


@app.post("/plans", status_code=201)
async def create_plan(planning_request: ProjectPlanningRequestDTO) -> ProjectPlanDTO:
    errors = validator.validate(planning_request)
    if len(errors) != 0:
        raise HTTPException(status_code=400, detail=errors)
    project_context = transform_project_context_dto_to_basic_project_context(planning_request.project_context)
    project_context = transform_basic_project_context_to_detailed_project_context(project_context)
    try:
        detailed_plan = service.generate_project_plan(project_context, planning_request.time_limit)
    except ProjectException as e:
        raise HTTPException(status_code=400, detail=[str(e)])
    return transform_detailed_project_plan_to_project_plan_dto(detailed_plan)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
