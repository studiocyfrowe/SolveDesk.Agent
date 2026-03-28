from pandas import DataFrame
from domain.abstracts.process_analysis_service import ProcessAnalysisService

class TopProcessesAnalitycs(ProcessAnalysisService):
    def __init__(self, loader):
        self.loader = loader

    def load_process_data(self) -> DataFrame:
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
    

    def analyze_top_processes(self, df: DataFrame) -> DataFrame:
        grouped = df.groupby('ProcessName').agg({
            "MemoryUsageMB": ['mean', 'max']
        })

        grouped.columns = ['ram_mean', 'ram_max']
        grouped.reset_index()

        top_processes = grouped.sort_values(
            by=['ram_mean', 'ram_max'],
            ascending=[False, False]
        ).head()

        return top_processes, grouped
    

    def detect_issues(self, top_processes: DataFrame, grouped: DataFrame, df: DataFrame) -> list[str]:
        issues = []
        if top_processes.iloc[0]['ram_mean'] > 50:
            issues.append('Single process dominates CPU')

        if df['CpuUsagePercent'].mean() > 80:
            issues.append('High overall CPU usage')

        if grouped['ram_max'].max() > 2000:
            issues.append('Possible memory leak')

        return issues
    

    def build_llm_payload(self, top_processes: DataFrame, df: DataFrame, issues: list) -> dict:
        payload = {
            'top_processes': top_processes.to_dict(orient='records'),
            'system': {
                'ram_avg': df['MemoryUsageMB'].mean().round(2)
            },
            'issues': issues
        }

        return payload


