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
        grouped: Optional[DataFrame] = None
    ) -> list[str]:
        issues = []

        if grouped is None or grouped.empty:
            return issues

        mean_usage = grouped["used_percent_mean"].mean()
        max_usage = grouped["used_percent_max"].max()

        high_usage_processes = (grouped["used_percent_mean"] > 70).sum()
        total_processes = len(grouped)

        if mean_usage > 90:
            issues.append("Critical: CPU usage is extremely high across processes")
        elif mean_usage > 80:
            issues.append("Warning: Sustained high CPU usage across processes")

        if max_usage > 95:
            issues.append("Critical: CPU spike detected (process near 100%)")
        elif max_usage > 85:
            issues.append("Warning: Single process reached high CPU usage")

        if total_processes > 0:
            ratio = high_usage_processes / total_processes

            if ratio > 0.5:
                issues.append("CPU load is distributed across many processes")
            elif high_usage_processes == 1:
                issues.append("CPU load concentrated in a single process")

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