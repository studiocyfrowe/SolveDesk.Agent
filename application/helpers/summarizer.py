import json

class Summarizer:
    def __init__(self, model_calling):
        self.model_calling = model_calling

    def get_summarize(self, problem, results):
        prompt = f"""
            You are an IT administrator assistant.
            User problem:

            {problem}

            Diagnostic results:

            {json.dumps(results, indent=2)}

            Summarize the cause of the problem for the IT specialist.

        """

        response = self.model_calling.call_model(prompt)

        return response

