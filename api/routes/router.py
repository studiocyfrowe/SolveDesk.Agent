from fastapi import APIRouter, Depends
from api.requests.agent_request import AgentRequest
from api.controllers.diagnose_controller import DiagnoseController
from api.dependencies import get_diagnose_controller

router = APIRouter()

@router.post("/diagnose")
def diagnose(
    request: AgentRequest,
    controller: DiagnoseController = Depends(get_diagnose_controller)
):
    return controller.diagnose(request.problem)