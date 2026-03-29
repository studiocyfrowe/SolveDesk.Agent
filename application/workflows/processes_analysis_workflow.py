from domain.abstracts.analysis_workflow import AnalysisWorkflow as BaseAnalysisWorkflow

class ProcessesAnalysisWorkflow(BaseAnalysisWorkflow):
    def __init__(self, process_analysis, logger=None):
        self.process_analysis = process_analysis
        self.logger = logger

    def execute(self):
        try:
            loaded_data = self.process_analysis.load_data()
            if loaded_data is None or len(loaded_data) == 0:
                raise ValueError('No data loaded from source')

            top_processes, grouped = self.process_analysis.analyze(loaded_data)
            detected_issues = self.process_analysis.detect(
                top_processes, 
                grouped, 
                loaded_data
            )

            result = self.process_analysis.build_llm_payload(
                top_processes, 
                loaded_data,
                detected_issues
            )

            return result
        
        except Exception as e:
            raise ValueError('Process Analysis Workflow failed', e)