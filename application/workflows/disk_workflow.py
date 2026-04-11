from domain.abstracts.analysis_workflow import AnalysisWorkflow as BaseAnalysisWorkflow

class DiskWorkflow(BaseAnalysisWorkflow):
    def __init__(self, disk_analysis, logger=None):
        self.disk_analysis = disk_analysis
        self.logger = logger

    def execute(self):
        try:
            loaded_data = self.disk_analysis.load_data(hostname='localhost')
            if loaded_data is None or len(loaded_data) == 0:
                raise ValueError('No data loaded from source')

            grouped = self.disk_analysis.analyze(df=loaded_data)
            if grouped is None:
                raise ValueError("Analyze returned None")

            detected_issues = self.disk_analysis.detect(
                df=grouped
            )
            if detected_issues is None:
                raise ValueError("Detect returned None")

            result = self.disk_analysis.build_llm_payload(
                df=grouped,
                issues=detected_issues
            )
            if result is None:
                raise ValueError("build_llm_payload returned None")
            
            return result
        
        except Exception as e:
            raise ValueError('Process Analysis Workflow failed', e)