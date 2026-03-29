from abc import ABC, abstractmethod
from pandas import DataFrame

class BaseAnalysisService(ABC):
    @abstractmethod
    def load_data(self) -> DataFrame:
        pass

    @abstractmethod
    def analyze(self, df: DataFrame) -> DataFrame:
        pass

    @abstractmethod
    def detect(self, top_processes: DataFrame, grouped: DataFrame, df: DataFrame) -> list[str]:
        pass

    @abstractmethod
    def build_llm_payload(self, top_processes: DataFrame, df: DataFrame, issues: list) -> dict:
        pass