from application.tools.diagnose_service import DiagnoseService
from application.tools.lumos_loader import LumosLoader
from application.helpers.model_calling import ModelCalling
from application.helpers.tool_registry import ToolRegistry
from application.helpers.executor import Executor
from application.helpers.planner import Planner
from application.helpers.summarizer import Summarizer
from fastapi import Depends
from application.workflows.diagnose_workflow import DiagnoseWorkflow
from api.controllers.diagnose_controller import DiagnoseController
from api.controllers.statistics_controller import StatisticsController

URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"


def get_model_calling():
    return ModelCalling(MODEL_NAME, URL)

def get_diagnose_service():
    return DiagnoseService()

def get_lumos_loader():
    return LumosLoader()

def get_tool_registry(
    service: DiagnoseService = Depends(get_diagnose_service),
    lumos_loader: LumosLoader = Depends(get_lumos_loader)
):
    registry = ToolRegistry()

    registry.register(
        "check_cpu_usage",
        lumos_loader.fetch_cpu_scan,
        "Check current CPU usage"
    )

    registry.register(
        "check_ram_usage",
        lumos_loader.fetch_memory_ram_scan,
        "Check RAM usage"
    )

    registry.register(
        "check_disk_space",
        service.check_disk_space,
        "Check disk free space"
    )

    registry.register(
        "top_processes",
        lumos_loader.fetch_processes_scan,
        "Show top CPU consuming processes"
    )

    return registry


def get_planner(
    model_calling: ModelCalling = Depends(get_model_calling),
    registry: ToolRegistry = Depends(get_tool_registry)
):
    return Planner(model=model_calling, registry=registry)

def get_executor(
    registry: ToolRegistry = Depends(get_tool_registry)
):
    return Executor(registry=registry)

def get_summarizer(
    model_calling: ModelCalling = Depends(get_model_calling)
):
    return Summarizer(model_calling=model_calling)

def get_workflow(
    planner: Planner = Depends(get_planner),
    executor: Executor = Depends(get_executor),
    summarizer: Summarizer = Depends(get_summarizer)
):
    return DiagnoseWorkflow(
        planner=planner,
        executor=executor,
        summarizer=summarizer
    )

def get_diagnose_controller(
    workflow: DiagnoseWorkflow = Depends(get_workflow)
):
    return DiagnoseController(workflow=workflow)

def get_stats_controller(
    loader: LumosLoader = Depends(get_lumos_loader)
):
    return StatisticsController(loader=loader)
    