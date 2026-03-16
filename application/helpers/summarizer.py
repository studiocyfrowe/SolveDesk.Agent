import json

class Summarizer:
    def __init__(self, model_calling):
        self.model_calling = model_calling

    def get_summarize(self, problem, results):
        prompt = f"""
            Jesteś asystentem administratora IT.
            Problem użytkownika:
            {problem}

            Wyniki diagnostyki:

            {json.dumps(results, indent=2)}

            Podsumuj przyczynę problemu dla informatyka.
        """

        response = self.model_calling.call_model(prompt)

        return response

