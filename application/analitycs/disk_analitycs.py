from domain.abstracts.base_analysis_service import BaseAnalysisService
import pandas as pd
from typing import Optional

class DiskAnalitycs(BaseAnalysisService):
    def __init__(self, collector):
        self.collector = collector

    def load_data(self, hostname: str):
        data = self.collector.collect_data(hostname=hostname)

        if data is None:
            raise ValueError("Collector returned None")

        if len(data) == 0:
            raise ValueError("Collector returned empty data")

        return pd.DataFrame(data)
    
    def analyze(self, df) -> pd.DataFrame:
        df['FreePercentage'] = (df['FreeSpace'].astype('float') / df['Size'].astype('float')) * 100

        df = df.groupby('SystemName').agg({
            "FreePercentage": ['min', 'max', 'mean']
        }).reset_index()

        df.columns = ['SystemName', 'min', 'max', 'mean']
        df = df.sort_values(
            by=['min', 'max', 'mean'],
            ascending=[False, False, False])
        
        return df
    
    def detect(
        self,
        top_processes: Optional[pd.DataFrame] = None,
        grouped: Optional[pd.DataFrame] = None,
        df: Optional[pd.DataFrame] = None
    ) -> list[str]:
        issues = []
        if (df.iloc[0]['max'] - df.iloc[0]['min']) > 1:
            issues.append('There was a small increase in disk involvement')

        if (df.iloc[0]['max'] - df.iloc[0]['min']) > 2.5:
            issues.append('There was a medium increase in disk involvement')

        if (df.iloc[0]['max'] - df.iloc[0]['min']) > 5:
            issues.append('There was a large increase in disk involvement')

        return issues
    
    def build_llm_payload(self, top_processes = None, df = None, issues = None):
        payload = {
            "disk_csan": {
                "disk_usage_max": round(df["max"].mean(), 2),
                "disk_usage_min": round(df["min"].max(), 2),
                "disk_usage_mean": round(df["mean"].max(), 2)
            },
            "issues": issues
        }

        return payload