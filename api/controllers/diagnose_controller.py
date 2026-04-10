import json
import traceback
from fastapi.responses import StreamingResponse

class DiagnoseController:
    def __init__(self, workflow):
        self.workflow = workflow

    def diagnose(self, problem):
        def event_stream():
            try:
                for event in self.workflow.execute_workflow(problem):
                    yield json.dumps(event) + "\n"

            except Exception as e:
                error_trace = traceback.format_exc()
                yield json.dumps({
                    "type": "error",
                    "message": str(e),
                    "details": error_trace
                }) + "\n"
        
        return StreamingResponse(
            event_stream(),
            media_type="application/json"
        )