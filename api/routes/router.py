from fastapi import APIRouter, Depends
from api.requests.agent_request import AgentRequest
from api.controllers.diagnose_controller import DiagnoseController
from api.controllers.statistics_controller import StatisticsController
from api.dependencies import get_diagnose_controller, get_stats_controller

router = APIRouter()

@router.post("/diagnose")
def diagnose(
    request: AgentRequest,
    controller: DiagnoseController = Depends(get_diagnose_controller)
):
    return controller.diagnose(request.problem)

@router.get("/stats/cpu")
def get_cpu_stats(
    controller: StatisticsController = Depends(get_stats_controller)
):
    return controller.get_cpu_data()