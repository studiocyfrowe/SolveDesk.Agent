from abc import ABC, abstractmethod
from pandas import DataFrame
from typing import Optional

class BaseAnalysisService(ABC):
    @abstractmethod
    def load_data(self) -> DataFrame:
        pass

    @abstractmethod
    def analyze(self, df: DataFrame) -> DataFrame:
        pass

    @abstractmethod
    def detect(
        self,
        top_processes: Optional[DataFrame] = None,
        grouped: Optional[DataFrame] = None,
        df: Optional[DataFrame] = None
    ) -> list[str]:
        pass

    @abstractmethod
    def build_llm_payload(
        self,
        top_processes: Optional[DataFrame] = None,
        df: Optional[DataFrame] = None,
        issues: Optional[list] = None
    ) -> dict:
        pass