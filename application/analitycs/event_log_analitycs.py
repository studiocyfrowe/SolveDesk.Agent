from domain.abstracts.base_analysis_service import BaseAnalysisService
import pandas as pd

class EventLogAnalitycs(BaseAnalysisService):
    def __init__(self, collector):
        self.collector = collector

    def load_data(self, hostname: str) -> pd.DataFrame:
        data = self.collector.collect_data(hostname=hostname)

        if data is None:
            raise ValueError("Collector returned None")

        if len(data) == 0:
            raise ValueError("Collector returned empty data")

        return pd.DataFrame(data)
    
    def analyze(self, df) -> pd.DataFrame:
        log_report_df = pd.pivot_table(
            data=df,
            index=['EventCode', 'Message'],
            values=['Message'],
            aggfunc=['count'],
            sort=True
        )

        log_report_df.reset_index()
        log_report_df.columns = ['count']
        log_report_df = log_report_df.sort_values(by='count', ascending=False).head()
        log_report_df = log_report_df.reset_index()
        
        return log_report_df