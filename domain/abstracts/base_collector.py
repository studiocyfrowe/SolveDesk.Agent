from abc import ABC, abstractmethod

class BaseCollector(ABC):
    @abstractmethod
    def collect_data(self):
        pass