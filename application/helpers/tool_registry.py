class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, func, description=""):
        self.tools[name] = {
            "func": func,
            "description": description
        }

    def execute(self, name, args=None):
        if name not in self.tools:
            return f"Tool {name} not found"

        if args is None:
            args = {}

        try:
            return self.tools[name]["func"](**args)
        except Exception as e:
            return f"Tool error: {str(e)}"

    def list_tools(self):
        return list(self.tools.keys())

    def describe_tools(self):
        tools = []

        for name, tool in self.tools.items():

            tools.append({
                "name": name,
                "description": tool["description"]
            })

        return tools