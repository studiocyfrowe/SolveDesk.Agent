from pandas import DataFrame
import wmi
from domain.abstracts.base_analysis_service import BaseAnalysisService

class WmiProcessor(BaseAnalysisService):
    def __init__(self, loader):
        self.loader = loader

    def load_data(self):
        return super().load_data()
    
    def analyze(self, df):
        return super().analyze(df)
    
    def detect(self, top_processes = None, grouped = None, df = None):
        return super().detect(top_processes, grouped, df)
    
    def build_llm_payload(self, top_processes = None, df = None, issues = None):
        return super().build_llm_payload(top_processes, df, issues)