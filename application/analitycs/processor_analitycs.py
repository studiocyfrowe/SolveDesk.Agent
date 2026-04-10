from pandas import DataFrame
from domain.abstracts.base_analysis_service import BaseAnalysisService
from typing import Optional

class ProcessorAnalitycs(BaseAnalysisService):
    def __init__(self, loader):
        self.loader = loader

    def load_data(self):
        query = """SELECT 
            StationName, 
            TotalGB, 
            UsedGB, 
            FreeGB, 
            UsedPercent, 
            LastScan
        FROM MemoryRamScans
        ORDER BY LastScan DESC"""

        loaded_data = self.loader.read_data(query)
        return loaded_data
    
    def analyze(self, df: DataFrame) -> DataFrame:
        grouped = df.groupby('StationName').agg({
            "UsedPercent": ['mean', 'max']
        })

        grouped = grouped.reset_index()
        grouped.columns = ['StationName', 'used_percent_mean', 'used_percent_max']

        return grouped
    
    def detect(
        self,
        top_processes: Optional[DataFrame] = None,
        grouped: Optional[DataFrame] = None,
        df: Optional[DataFrame] = None
    ) -> list[str]:
        issues = []

        if grouped["used_percent_mean"].mean() > 80:
            issues.append("Sustained high CPU usage across processes")

        if grouped["used_percent_max"].max() > 80:
            issues.append("Single process reached very high CPU usage (possible CPU spike)")

        return issues
    
    def build_llm_payload(
        self,
        top_processes: Optional[DataFrame] = None,
        df: Optional[DataFrame] = None,
        issues: Optional[list] = None
    ) -> dict:
        payload = {
            "processor_scan": {
                "processor_used_percent_mean": round(df["used_percent_mean"].mean(), 2),
                "processor_used_percent_max": round(df["used_percent_max"].max(), 2)
            },
            "issues": issues
        }

        return payload