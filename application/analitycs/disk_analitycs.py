from domain.abstracts.base_analysis_service import BaseAnalysisService
from domain.issues.disk_issues import DiskIssuesEnum
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
        df: Optional[pd.DataFrame] = None
    ) -> list[str]:
        issues = []

        if df is None or df.empty:
            return issues

        df = df.copy()
        df["diff"] = df["max"] - df["min"]

        worst = df.sort_values(by="diff", ascending=False).iloc[0]
        diff = worst["diff"]

        if diff > 5:
            issues.append(DiskIssuesEnum.HIGH_INCREASE)
        elif diff > 2.5:
            issues.append(DiskIssuesEnum.MEDIUM_INCREASE)
        elif diff > 1:
            issues.append(DiskIssuesEnum.SMALL_INCREASE)

        return issues
    
    def build_llm_payload(self, top_processes = None, df = None, issues = None):
        payload = {
            "disk_scan": {
                "disk_usage_max": round(df["max"].mean(), 2),
                "disk_usage_min": round(df["min"].max(), 2),
                "disk_usage_mean": round(df["mean"].max(), 2)
            },
            "issues": issues
        }

        return payload