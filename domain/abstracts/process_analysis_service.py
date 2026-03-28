from abc import ABC, abstractmethod
from pandas import DataFrame

class ProcessAnalysisService(ABC):
    @abstractmethod
    def load_process_data(self) -> DataFrame:
        pass

    @abstractmethod
    def analyze_top_processes(self, df: DataFrame) -> DataFrame:
        pass

    @abstractmethod
    def detect_issues(self, top_processes: DataFrame, grouped: DataFrame, df: DataFrame) -> list[str]:
        pass

    @abstractmethod
    def build_llm_payload(self, top_processes: DataFrame, df: DataFrame, issues: list) -> dict:
        pass