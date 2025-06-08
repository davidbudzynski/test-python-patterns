## Overview

This design integrates three design patterns to build a flexible and maintainable system for reading settings, processing model data, and applying various output templates with configurable transformation pipelines.

- **Factory Pattern:** Selects and creates the appropriate Template based on configuration or input.
- **Strategy Pattern (Templates):** Each Template encapsulates a distinct data transformation strategy.
- **Pipeline Pattern:** Defines a sequence of small transformation steps that process data sequentially.
