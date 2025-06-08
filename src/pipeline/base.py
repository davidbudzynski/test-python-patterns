from abc import ABC, abstractmethod

class PipelineStep(ABC):
    @abstractmethod
    def process(self, data):
        pass

class Pipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, step: PipelineStep):
        self.steps.append(step)

    def run(self):
        data = None
        for step in self.steps:
            data = step.process(data)
        return data
