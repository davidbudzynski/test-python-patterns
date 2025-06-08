from abc import ABC, abstractmethod

class AnalysisStrategy(ABC):
    @abstractmethod
    def execute(self):
        pass
