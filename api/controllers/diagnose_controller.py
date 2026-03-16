import json
from fastapi.responses import StreamingResponse

class DiagnoseController:
    def __init__(self, workflow):
        self.workflow = workflow

    def diagnose(self, problem):
        def event_stream():
            for event in self.workflow.execute_workflow(problem):
                yield json.dumps(event) + "\n"
        
        return StreamingResponse(
            event_stream(),
            media_type="application/json"
        )

    