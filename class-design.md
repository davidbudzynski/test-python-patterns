# Design Summary: Combining Strategy, Pipeline, and Factory Patterns for Model Data Processing

## Overview

This design integrates three design patterns to build a flexible and maintainable system for reading settings, processing model data, and applying various output templates with configurable transformation pipelines.

- **Factory Pattern:** Selects and creates the appropriate Template based on configuration or input.
- **Strategy Pattern (Templates):** Each Template encapsulates a distinct data transformation strategy.
- **Pipeline Pattern:** Defines a sequence of small transformation steps that process data sequentially.

---

## Components

### 1. PipelineStep (Abstract Base Class)

- Defines a standard interface for all transformation steps.
- Requires implementation of a `run(data)` method.
- Examples include filtering data, selecting columns, or aggregating results.

### 2. Pipeline

- Contains an ordered list of `PipelineStep` instances.
- Executes steps sequentially, passing data output from one step to the next.

### 3. Template (Strategy)

- Represents a specific transformation strategy.
- Holds raw model data and settings.
- Defines its own pipeline configuration internally by specifying which steps to use and in what order.
- Executes the pipeline and returns the processed output.

### 4. TemplateFactory

- Responsible for creating Template instances based on a template identifier.
- Abstracts template instantiation details from the main application logic.

---

## How It Works Together

1. The main application reads settings and model data.
2. The `TemplateFactory` creates an instance of the required Template.
3. The Template internally builds its pipeline by specifying the pipeline steps.
4. The Template runs the pipeline on the model data.
5. The output is returned for further use or display.

---

## Example Code

```python
from abc import ABC, abstractmethod

# Abstract PipelineStep
class PipelineStep(ABC):
    @abstractmethod
    def run(self, data):
        pass

# Concrete pipeline steps
class FilterStep(PipelineStep):
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def run(self, data):
        return data[data[self.column] == self.value]

class SelectColumnsStep(PipelineStep):
    def __init__(self, columns):
        self.columns = columns

    def run(self, data):
        return data[self.columns]

# Pipeline that runs steps sequentially
class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self, data):
        for step in self.steps:
            data = step.run(data)
        return data

# Base Template (Strategy)
class BaseTemplate(ABC):
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings

    @abstractmethod
    def build_pipeline(self):
        pass

    def run(self):
        pipeline = self.build_pipeline()
        return pipeline.run(self.data)

# Concrete Template example
class SalesSummaryTemplate(BaseTemplate):
    def build_pipeline(self):
        steps = [
            FilterStep("region", self.settings.get("region")),
            SelectColumnsStep(["product", "sales"])
        ]
        return Pipeline(steps)

# Factory to instantiate templates
class TemplateFactory:
    templates = {
        "sales_summary": SalesSummaryTemplate,
        # Add more template mappings here
    }

    @classmethod
    def create(cls, name, data, settings):
        if name not in cls.templates:
            raise ValueError(f"Unknown template: {name}")
        return cls.templates[name](data, settings)

# Usage example
if __name__ == "__main__":
    import pandas as pd

    model_data = pd.DataFrame({
        "region": ["East", "West", "East"],
        "sales": [100, 200, 150],
        "product": ["A", "B", "A"]
    })

    config = {"region": "East"}

    template = TemplateFactory.create("sales_summary", model_data, config)
    result = template.run()
    print(result)

## Directory structure
```bash
/project_root
    /templates
        __init__.py
        base_template.py
        sales_summary.py
        other_templates.py
    /pipeline_steps
        __init__.py
        filter_step.py
        select_columns_step.py
        aggregation_step.py
    /factories
        __init__.py
        template_factory.py
    main.py
    config.yaml

```

## Diagram

```mermaid
flowchart LR
    TF[TemplateFactory] --> T[Template]
    T --> P[Pipeline]
    T -->|configures| PS[Pipeline Steps]
    PS --> DT[Data Transformations]
