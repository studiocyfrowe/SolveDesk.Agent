from pandas import DataFrame
import wmi
from typing import Optional
from domain.abstracts.base_analysis_service import BaseAnalysisService
import pandas as pd

class WmiProcessor(BaseAnalysisService):
    def __init__(self, collector):
        self.collector = collector

    def load_data(self, hostname: str):
        data = self.collector.collect_data(hostname=hostname)

        if data is None:
            raise ValueError("Collector returned None")

        if len(data) == 0:
            raise ValueError("Collector returned empty data")

        return pd.DataFrame(data)
    
    def analyze(self, df: DataFrame):
        if isinstance(df, list):
            df = pd.DataFrame(df)
            
        grouped = df.groupby('Caption').agg({
            "LoadPercentage": ['mean', 'max']
        })

        grouped = grouped.reset_index()
        grouped.columns = ['ProcessorCaption', 'cpu_mean', 'cpu_max']

        result = grouped.sort_values(
            by=['cpu_mean', 'cpu_max'],
            ascending=[False, False]
        ).head()

        return result
    
    def detect(
        self,
        top_processes: Optional[DataFrame] = None,
        grouped: Optional[DataFrame] = None,
        df: Optional[DataFrame] = None
    ) -> list[str]:
        issues = []

        if top_processes["cpu_mean"].mean() > 80:
            issues.append("Sustained high CPU usage across processes")

        if top_processes["cpu_max"].max() > 80:
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
                    "processor_used_percent_mean": float(round(df["cpu_mean"].mean(), 2)),
                    "processor_used_percent_max": float(round(df["cpu_max"].max(), 2))
                },
                "issues": issues
            }

            return payload