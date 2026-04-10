from pandas import DataFrame
from domain.abstracts.base_analysis_service import BaseAnalysisService
from typing import Optional

class TopProcessesAnalitycs(BaseAnalysisService):
    def __init__(self, loader):
        self.loader = loader

    def load_data(self) -> DataFrame:
        query = """SELECT 
            MachineGuid, 
            ProcessId, 
            ProcessName, 
            MemoryUsageMB, 
            CpuUsagePercent, 
            StartTime, 
            LastScan
        FROM Processes"""

        loaded_data = self.loader.read_data(query)
        return loaded_data
    

    def analyze(self, df: DataFrame) -> DataFrame:
        grouped = df.groupby('ProcessName').agg({
            "MemoryUsageMB": ['mean', 'max'],
            "CpuUsagePercent": ['mean', 'max']
        })

        grouped = grouped.reset_index()
        grouped.columns = ['ProcessName', 'ram_mean', 'ram_max', 'cpu_mean', 'cpu_max']

        top_processes = grouped.sort_values(
            by=['ram_mean', 'ram_max', 'cpu_mean', 'cpu_max'],
            ascending=[False, False, False, False]
        ).head()

        return top_processes, grouped
    

    def detect(
        self,
        top_processes: Optional[DataFrame] = None,
        grouped: Optional[DataFrame] = None,
        df: Optional[DataFrame] = None
    ) -> list[str]:
        issues = []
        if top_processes.iloc[0]['ram_mean'] > 50:
            issues.append('Single process dominates CPU')

        if df['CpuUsagePercent'].mean() > 80:
            issues.append('High overall CPU usage')

        if grouped['ram_max'].max() > 2000:
            issues.append('Possible memory leak')

        return issues
    

    def build_llm_payload(
        self,
        top_processes: Optional[DataFrame] = None,
        df: Optional[DataFrame] = None,
        issues: Optional[list] = None
    ) -> dict:
        payload = {
            'top_processes': top_processes.to_dict(orient='records'),
            'system': {
                'ram_avg': df['MemoryUsageMB'].mean().round(2),
                "cpu_avg": df["CpuUsagePercent"].mean().round(2)
            },
            'issues': issues
        }

        return payload


