import pandas as pd
from pipeline.base import PipelineStep

class ReadCSVStep(PipelineStep):
    def __init__(self, filepath):
        self.filepath = filepath

    def process(self, data=None):
        print(f"Reading CSV from: {self.filepath}")
        return pd.read_csv(self.filepath)

class FilterStep(PipelineStep):
    def __init__(self, column, condition_fn):
        self.column = column
        self.condition_fn = condition_fn

    def process(self, data):
        print(f"Filtering on column: {self.column}")
        return data[data[self.column].apply(self.condition_fn)]
