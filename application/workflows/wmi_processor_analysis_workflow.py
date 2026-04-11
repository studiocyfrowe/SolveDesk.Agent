from domain.abstracts.analysis_workflow import AnalysisWorkflow as BaseAnalysisWorkflow

class WMIProcessorAnalysisWorkflow(BaseAnalysisWorkflow):
    def __init__(self, processor_analysis, logger=None):
        self.processor_analysis = processor_analysis
        self.logger = logger

    def execute(self):
        try:
            loaded_data = self.processor_analysis.load_data(hostname='localhost')
            if loaded_data is None or len(loaded_data) == 0:
                raise ValueError('No data loaded from source')

            result = self.processor_analysis.analyze(df=loaded_data)
            if result is None:
                raise ValueError("Analyze returned None")

            detected_issues = self.processor_analysis.detect(
                top_processes=result
            )
            if detected_issues is None:
                raise ValueError("Detect returned None")

            result = self.processor_analysis.build_llm_payload(
                df=result,
                issues=detected_issues
            )
            if result is None:
                raise ValueError("build_llm_payload returned None")
            
            return result
        
        except Exception as e:
            raise ValueError('Process Analysis Workflow failed', e)