from domain.abstracts.base_analysis_service import BaseAnalysisService
import pandas as pd
from typing import Optional
from domain.issues.ram_issues import RamIssuesEnum

class RAMAnalitycs(BaseAnalysisService):
    def __init__(self, collector):
        self.collector = collector

    def load_data(self, hostname: str):
        data = self.collector.collect_data(hostname=hostname)

        if data is None:
            raise ValueError("Collector returned None")

        if len(data) == 0:
            raise ValueError("Collector returned empty data")

        return pd.DataFrame(data)
    
    def analyze(self, df: pd.DataFrame) -> pd.DataFrame:
        if isinstance(df, list):
            df = pd.DataFrame(df)
            
        grouped = df.groupby('DeviceName').agg({
            "Free_MB": ['mean', 'max', 'min'],
            "Used_MB": ['mean', 'max', 'min'],
            "Used_Percentage": ['mean', 'max', 'min']
        })

        grouped = grouped.reset_index()
        grouped.columns = ['DeviceCaption', 'free_mean', 'free_max', 'free_min', 'used_mean', 'used_max', 'used_min', 'used_percentage_mean', 'used_percentage_max', 'used_percentage_min']

        result = grouped.sort_values(
            by=['free_mean', 'free_max', 'free_min', 'used_mean', 'used_max', 'used_min', 'used_percentage_mean', 'used_percentage_max', 'used_percentage_min'],
            ascending=[False, False, False, False, False, False, False, False, False]
        ).head()

        return result
    
    def detect(
        self,
        df: Optional[pd.DataFrame] = None
    ) -> list[str]:
        issues = []

        if df is None or df.empty:
            return issues

        row = df.sort_values(by="used_percentage_max", ascending=False).iloc[0]

        diff = row['used_percentage_max'] - row['used_percentage_min']
        max_usage = row['used_percentage_max']
        mean_usage = row['used_percentage_mean']

        if diff > 5:
            issues.append(RamIssuesEnum.HIGH_INCREASE)
        elif diff > 2.5:
            issues.append(RamIssuesEnum.MEDIUM_INCREASE)
        elif diff > 1:
            issues.append(RamIssuesEnum.SMALL_INCREASE)

        if mean_usage > 85:
            issues.append(RamIssuesEnum.HIGH_USAGE)

        if max_usage > 90:
            issues.append(RamIssuesEnum.MEMORY_PRESSURE)

        if max_usage > 95:
            issues.append(RamIssuesEnum.LOW_AVAILABLE_MEMORY)

        return issues
        
    def build_llm_payload(self, top_processes = None, df = None, issues = None):
        payload = {
            "ram_scan": {
                "ram_usage_max": f"{round(df['used_percentage_max'].mean(), 2)}%",
                "ram_usage_min": f"{round(df['used_percentage_min'].max(), 2)}%",
                "ram_usage_mean": f"{round(df['used_percentage_mean'].max(), 2)}%"
            },
            "issues": issues
        }

        return payload