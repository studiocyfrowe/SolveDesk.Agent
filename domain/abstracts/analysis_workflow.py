from abc import ABC, abstractmethod

class AnalysisWorkflow(ABC):
    @abstractmethod
    def execute(self):
        pass