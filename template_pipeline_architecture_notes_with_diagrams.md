
Template + Pipeline Architecture for Flexible Model Transformations

Goal  
Design a scalable, modular app that:  
- Loads global configuration  
- Reads model data  
- Applies one of many template-specific transformations (30+ possible)  
- Outputs a result based on structured, reusable processing logic  

---

High-Level Components  

1. Global Settings  
- JSON or config file loaded at runtime  
- Contains:  
  - Which template to run ("template": "sales_summary")  
  - Where to load/save data ("model_path", "output_path")  
  - Additional settings for template and pipeline behavior  

---

2. Model Data  
- Loaded early using pandas or similar  
- Passed as input into the selected template and pipeline  

---

3. PipelineStep  
- Small, composable units of transformation logic  
- Each step is a class with a `run(data, settings)` method  
- Configurable using parameters passed at initialization  

Example:

```python
class FilterByColumnValueStep(PipelineStep):
    def run(self, data, settings):
        column = self.params["column"]
        value = self.params["value"]
        return data[data[column] == value]
```

---

Introducing the TemplatePipeline Abstraction  

Instead of hardcoding pipeline steps in each template, extract them into reusable pipeline classes.  

Why This Helps  
- Reduces duplication by grouping common logic for similar templates  
- Enables reuse of pipeline structures across templates (e.g. sales templates, engagement templates)  
- Allows separation of concerns: templates handle high-level config, pipelines handle step composition  
- Supports pipeline-specific settings separate from template settings  

---

4. TemplatePipeline (New Class)  

Base class:

```python
class TemplatePipeline(ABC):
    def __init__(self, data: pd.DataFrame, pipeline_settings: dict):
        self.data = data
        self.pipeline_settings = pipeline_settings

    @abstractmethod
    def build_pipeline(self) -> list:
        pass

    def run(self) -> pd.DataFrame:
        result = self.data.copy()
        for step in self.build_pipeline():
            result = step.run(result, self.pipeline_settings)
        return result
```

Example shared pipeline:

```python
class SalesPipeline(TemplatePipeline):
    def build_pipeline(self):
        return [
            NormalizeColumnsStep(casing="lower"),
            FilterByColumnValueStep(column="region", value=self.pipeline_settings.get("region")),
            GroupAndAggregateStep(group_by="region", agg_col="sales"),
        ]
```

---

5. Template  

- Represents the entry point for a particular transformation configuration  
- Holds raw model data and high-level settings  
- Delegates execution to a TemplatePipeline instance  

Example:

```python
class SalesSummaryTemplate(Template):
    def __init__(self, raw_data: pd.DataFrame, settings: dict):
        self.raw_data = raw_data
        self.settings = settings

    def run_pipeline(self):
        pipeline_settings = self.settings.get("pipeline_settings", {})
        pipeline = SalesPipeline(self.raw_data, pipeline_settings)
        return pipeline.run()
```

---

6. TemplateFactory  

- Selects the correct Template subclass based on a name  
- Instantiates the template with model data and template-specific settings  

Example:

```python
class TemplateFactory:
    templates = {
        "sales_summary": SalesSummaryTemplate,
        "user_engagement": UserEngagementTemplate,
        # Add other templates here
    }

    @classmethod
    def create(cls, name: str, model_data: pd.DataFrame, settings: dict):
        if name not in cls.templates:
            raise ValueError(f"Unknown template: {name}")
        return cls.templates[name](model_data, settings)
```

---

# Suggested Folder Structure

```
project_root/
│
├── config/
│   └── settings.json           # Global settings file
│
├── data/
│   ├── raw/                    # Raw model data files
│   └── processed/              # Output data after transformations
│
├── pipelines/                  # PipelineStep implementations and pipelines
│   ├── steps.py                # PipelineStep base classes and implementations
│   ├── base_pipeline.py        # TemplatePipeline base class
│   └── sales_pipeline.py       # Example pipeline subclass
│
├── templates/                  # Template classes and factories
│   ├── base_template.py        # Template base class
│   ├── sales_template.py       # SalesSummaryTemplate and others
│   └── template_factory.py     # Factory to create templates
│
├── main.py                    # Application entry point: loads settings, data, runs pipeline
└── requirements.txt           # Dependencies
```

---

# Architecture Flow Diagram (simplified ASCII)

```
+------------------+
| Load Global       |
| Settings (JSON)   |
+---------+--------+
          |
          v
+------------------+
| Load Model Data  |
+---------+--------+
          |
          v
+-------------------------+
| TemplateFactory         |
| - Selects Template      |
+---------+--------------+
          |
          v
+--------------------------+
| Template (e.g. Sales)    |
| - Holds raw data & config|
+---------+---------------+
          |
          v
+---------------------------+
| TemplatePipeline          |
| - Builds list of Steps    |
+---------+-----------------+
          |
          v
+---------------------------+
| PipelineStep 1, 2, 3...   |
| - Each transforms data    |
+---------------------------+
          |
          v
+---------------------------+
| Output transformed data   |
+---------------------------+
```

---

# Summary:  
- Settings are loaded globally and passed down  
- Model data is loaded once and passed to templates  
- Templates hold high-level config and delegate to pipelines  
- Pipelines hold reusable sequences of steps  
- Steps are small, testable units of transformation logic  
- This layered architecture enables maximum flexibility, reusability, and scalability  

---

Let me know if you want me to help build example step implementations or a full minimal working prototype!
