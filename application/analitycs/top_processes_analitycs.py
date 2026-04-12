from pandas import DataFrame
from domain.abstracts.base_analysis_service import BaseAnalysisService
from typing import Optional
import pandas as pd

class TopProcessesAnalitycs(BaseAnalysisService):
    def __init__(self, collector):
        self.collector = collector

    def load_data(self, hostname: str):
        data = self.collector.collect_data(hostname=hostname)

        if data is None:
            raise ValueError("Collector returned None")

        if len(data) == 0:
            raise ValueError("Collector returned empty data")

        return pd.DataFrame(data)
    

    def analyze(self, df: DataFrame) -> tuple[DataFrame, DataFrame]:
        df = df.copy()

        df["CreationDate"] = pd.to_datetime(
            df["CreationDate"].str[:14],
            format="%Y%m%d%H%M%S",
            errors="coerce"
        )

        grouped = df.groupby('ProcessName').agg(
            working_set_mean=('WorkingSet_MB', 'mean'),
            working_set_max=('WorkingSet_MB', 'max'),
            thread_mean=('ThreadCount', 'mean'),
            thread_max=('ThreadCount', 'max'),
            handle_mean=('HandleCount', 'mean'),
            handle_max=('HandleCount', 'max')
        ).reset_index()

        top_processes = grouped.sort_values(
            by=['working_set_mean', 'working_set_max'],
            ascending=[False, False]
        ).head(5)

        return top_processes, grouped
    

    def detect(
        self,
        top_processes: Optional[DataFrame] = None,
        grouped: Optional[DataFrame] = None,
        df: Optional[DataFrame] = None
    ) -> list[str]:

        issues = []

        if top_processes is None or top_processes.empty:
            return issues

        if grouped is None or grouped.empty:
            return issues

        top = top_processes.iloc[0]

        if top['working_set_mean'] > 500:  # MB
            issues.append("Single process consumes high amount of RAM")

        if top['working_set_max'] > 2000:
            issues.append("Single process reached very high RAM usage")

        if grouped['working_set_mean'].mean() > 400:
            issues.append("Overall memory usage across processes is high")

        if grouped['thread_max'].max() > 300:
            issues.append("Process with unusually high number of threads detected")

        if grouped['handle_max'].max() > 10000:
            issues.append("High number of handles detected (possible resource leak)")

        return issues
    

    def build_llm_payload(
        self,
        top_processes: Optional[DataFrame] = None,
        df: Optional[DataFrame] = None,
        issues: Optional[list] = None
    ) -> dict:
        if top_processes is None:
            top_processes = pd.DataFrame()

        if df is None:
            df = pd.DataFrame()

        ram_avg = None
        cpu_avg = None

        if not df.empty:
            if 'MemoryUsageMB' in df.columns:
                ram_avg = float(round(df['MemoryUsageMB'].mean(), 2))

            if 'CpuUsagePercent' in df.columns:
                cpu_avg = float(round(df['CpuUsagePercent'].mean(), 2))

        payload = {
            'top_processes': top_processes.to_dict(orient='records'),
            'system': {
                'ram_avg': ram_avg,
                'cpu_avg': cpu_avg
            },
            'issues': issues or []
        }

        return payload


