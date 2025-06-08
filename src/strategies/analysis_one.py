from strategies.base import AnalysisStrategy
from pipeline.base import Pipeline
from pipeline.steps import ReadCSVStep, FilterStep
from factory.strategy_factory import StrategyFactory

@StrategyFactory.register("analysis_one")
class AnalysisOneStrategy(AnalysisStrategy):
    def __init__(self, filepath, column, condition_fn):
        self.pipeline = Pipeline()
        self.pipeline.add_step(ReadCSVStep(filepath))
        self.pipeline.add_step(FilterStep(column, condition_fn))

    def execute(self):
        print("Running AnalysisOneStrategy...")
        return self.pipeline.run()
