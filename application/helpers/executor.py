class Executor:
    def __init__(self, registry):
        self.registry = registry

    def execute_plan(self, plan):
        tool = self.registry.execute(plan)

        if not tool:
            return {
                "tool": plan,
                "result": f"Tool {plan} not found"
            }

        return {
            "tool": plan,
            "result": tool
        }