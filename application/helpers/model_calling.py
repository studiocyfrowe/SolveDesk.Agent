import requests

class ModelCalling():
    def __init__(self, model_name, url):
        self.model_name = model_name
        self.url = url

    def call_model(self, prompt):
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }

        r = requests.post(self.url, json=payload)

        return r.json()["message"]["content"]