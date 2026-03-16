import json

class DiagnoseWorkflow:
    def __init__(self, planner, executor, summarizer):
        self.planner = planner
        self.executor = executor
        self.summarizer = summarizer

    def execute_workflow(self, problem):
        plan = self.planner.create_plan(problem)

        if not plan:
            yield {
                "type": "error",
                "content": "Planner returned empty plan"
            }
            return

        yield {
            "type": "plan",
            "content": plan
        }

        results = []

        for step in plan:
            result = self.executor.execute_plan(step)
            results.append(result)

            yield {
                "type": "observation",
                "content": result
            }

        summary = self.summarizer.get_summarize(problem, results)

        yield {
            "type": "summary",
            "content": summary
        }