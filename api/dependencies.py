from fastapi import Depends
from api.controllers.diagnose_controller import DiagnoseController
from api.controllers.statistics_controller import StatisticsController
from domain.loaders.lumos_loader import LumosLoader
from domain.loaders.wmi_loader import WmiLoader
from domain.collectors.cpu_collector import CPUCollector
from domain.collectors.disk_collector import DiskCollector
from domain.collectors.ram_collector import RAMCollector
from domain.collectors.processes_collector import ProcessesCollector
from domain.collectors.event_log_collector import EventLogCollector
from application.helpers.model_calling import ModelCalling
from application.helpers.tool_registry import ToolRegistry
from application.helpers.executor import Executor
from application.helpers.planner import Planner
from application.helpers.summarizer import Summarizer
from application.analitycs.top_processes_analitycs import TopProcessesAnalitycs
from application.analitycs.wmi_processor import WmiProcessor
from application.analitycs.processor_analitycs import ProcessorAnalitycs
from application.analitycs.disk_analitycs import DiskAnalitycs
from application.analitycs.ram_analitycs import RAMAnalitycs
from application.workflows.disk_workflow import DiskWorkflow
from application.workflows.ram_workflow import RAMWorkflow
from application.workflows.diagnose_workflow import DiagnoseWorkflow
from application.workflows.processor_workflow import ProcessorWorkflow
from application.workflows.processes_analysis_workflow import ProcessesAnalysisWorkflow
from application.workflows.wmi_processor_analysis_workflow import WMIProcessorAnalysisWorkflow

URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"

# --- MODEL CALLING

def get_model_calling():
    return ModelCalling(MODEL_NAME, URL)

# --- LOADERS

def get_lumos_loader():
    return LumosLoader()

def get_wmi_loader():
    return WmiLoader()

# --- COLLECTORS

def get_cpu_collector():
    return CPUCollector()

def get_disk_collector():
    return DiskCollector()

def get_ram_collector():
    return RAMCollector()

def get_processes_collector():
    return ProcessesCollector()

def get_event_log_collector():
    return EventLogCollector()

# --- ANALITYCS

def get_ram_analitycs(
    collector: WmiLoader = Depends(get_ram_collector)
):
    return RAMAnalitycs(collector=collector)

def get_wmi_processor_analitycs(
    collector: WmiLoader = Depends(get_cpu_collector)
):
    return WmiProcessor(collector=collector)

def get_disk_analitycs(
    collector: WmiLoader = Depends(get_disk_collector)
):
    return DiskAnalitycs(collector=collector)

def get_top_processes_analitycs(
    collector: WmiLoader = Depends(get_processes_collector)
):
    return TopProcessesAnalitycs(collector=collector)

def get_processes_analitycs(
    loader: LumosLoader = Depends(get_lumos_loader)
):
    return ProcessorAnalitycs(loader=loader)

# --- WORKFLOWS

def get_ram_workflow(
    ram_analysis: RAMAnalitycs = Depends(get_ram_analitycs)
):
    return RAMWorkflow(ram_analysis=ram_analysis)

def get_disk_workflow(
    disk_analysis: DiskAnalitycs = Depends(get_disk_analitycs)
):
    return DiskWorkflow(disk_analysis=disk_analysis)

def get_processor_workflow(
    processor_analysis: ProcessorAnalitycs = Depends(get_processes_analitycs)
):
    return ProcessorWorkflow(processor_analysis=processor_analysis)

def get_processes_analysis_workflow(
    process_analysis: TopProcessesAnalitycs = Depends(get_top_processes_analitycs)
):
    return ProcessesAnalysisWorkflow(process_analysis=process_analysis)

def get_wmi_processes_analysis_workflow(
    processor_analysis: WmiProcessor = Depends(get_wmi_processor_analitycs)
):
    return WMIProcessorAnalysisWorkflow(processor_analysis=processor_analysis)

# --- TOOLS

def get_tool_registry(
    processes_workflow: ProcessesAnalysisWorkflow = Depends(get_processes_analysis_workflow),
    wmi_processor_workflow: WMIProcessorAnalysisWorkflow = Depends(get_wmi_processes_analysis_workflow),
    disk_workflow: DiskWorkflow = Depends(get_disk_workflow),
    ram_workflow: RAMWorkflow = Depends(get_ram_workflow)
):
    registry = ToolRegistry()

    registry.register(
        "top_processes",
        processes_workflow.execute,
        "Show top CPU consuming processes"
    )

    registry.register(
        "processor_usage",
        wmi_processor_workflow.execute,
        "Show percentage usage of Processor CPU"
    )

    registry.register(
        "disk_usage",
        disk_workflow.execute,
        "Show percentage usage of hard disk"
    )

    registry.register(
        "ram_workflow",
        ram_workflow.execute,
        "Show percentage usage of RAM"
    )

    return registry


# --- PLANNER, EXECUTOR, SUMMARIZER

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

# --- CONTROLLERS

def get_diagnose_controller(
    workflow: DiagnoseWorkflow = Depends(get_workflow)
):
    return DiagnoseController(workflow=workflow)

def get_stats_controller(
    loader: LumosLoader = Depends(get_lumos_loader)
):
    return StatisticsController(loader=loader)
    