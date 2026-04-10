import json

class Planner:
    def __init__(self, model, registry):
        self.model = model
        self.registry = registry

    def create_plan(self, problem):
        tools = json.dumps(self.registry.describe_tools(), indent=2)

        prompt = f"""
            Jesteś plannerem diagnostyki IT.

            Problem użytkownika:
            {problem}

            Dostępne narzędzia:
            {tools}

            Twoim zadaniem jest:
            1. Dokładnie opisać problem użytkownika (na podstawie podanego opisu).
            2. Wypisać obserwowane objawy.
            3. Nie podawaj żadnych rekomendacji ani rozwiązań.
            4. Na końcu wskaż, które narzędzia mogą zostać użyte do dalszej diagnostyki (tylko z listy dostępnych narzędzi).

            Zwróć wynik w formacie JSON:

            {{
                "plan": [
                    "tool_name"
                ]
            }}

            Używaj tylko dostępnych narzędzi.
        """

        response = self.model.call_model(prompt)

        print("\nPLANNER RESPONSE:")
        print(response)

        try:
            plan = json.loads(response)["plan"]

        except:
            print("Planner JSON error, fallback plan.")
            plan = ["check_cpu_usage", "top_processes"]

        return plan