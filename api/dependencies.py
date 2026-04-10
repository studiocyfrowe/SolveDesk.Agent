from application.tools.diagnose_service import DiagnoseService
from domain.loaders.lumos_loader import LumosLoader
from domain.loaders.wmi_loader import WmiLoader
from application.helpers.model_calling import ModelCalling
from application.helpers.tool_registry import ToolRegistry
from application.helpers.executor import Executor
from application.helpers.planner import Planner
from application.helpers.summarizer import Summarizer
from fastapi import Depends
from application.workflows.diagnose_workflow import DiagnoseWorkflow
from application.workflows.processor_workflow import ProcessorWorkflow
from api.controllers.diagnose_controller import DiagnoseController
from api.controllers.statistics_controller import StatisticsController
from application.analitycs.top_processes_analitycs import TopProcessesAnalitycs
from application.analitycs.wmi_processor import WmiProcessor
from application.analitycs.processor_analitycs import ProcessorAnalitycs
from application.workflows.processes_analysis_workflow import ProcessesAnalysisWorkflow

URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"


def get_model_calling():
    return ModelCalling(MODEL_NAME, URL)

def get_lumos_loader():
    return LumosLoader()

def get_wmi_loader():
    return WmiLoader('localhost')

def get_wmi_processor_analitycs(
    loader: WmiLoader = Depends(get_wmi_loader)
):
    return WmiProcessor(loader=loader)

def get_top_processes_analitycs(
    loader: LumosLoader = Depends(get_lumos_loader)
):
    return TopProcessesAnalitycs(loader=loader)

def get_processes_analitycs(
    loader: LumosLoader = Depends(get_lumos_loader)
):
    return ProcessorAnalitycs(loader=loader)

def get_processor_workflow(
    processor_analysis: ProcessorAnalitycs = Depends(get_processes_analitycs)
):
    return ProcessorWorkflow(processor_analysis=processor_analysis)

def get_processes_analysis_workflow(
    process_analysis: TopProcessesAnalitycs = Depends(get_top_processes_analitycs)
):
    return ProcessesAnalysisWorkflow(process_analysis=process_analysis)

def get_tool_registry(
    processes_workflow: ProcessesAnalysisWorkflow = Depends(get_processes_analysis_workflow),
    processor_workflow: ProcessorWorkflow = Depends(get_processor_workflow)
):
    registry = ToolRegistry()

    registry.register(
        "top_processes",
        processes_workflow.execute,
        "Show top CPU consuming processes"
    )

    registry.register(
        "processor_usage",
        processor_workflow.execute,
        "Show percentage usage of Processor CPU"
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
    