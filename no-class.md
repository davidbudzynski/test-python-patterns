```python
import pandas as pd

# === Shared pipeline steps ===

def read_csv(filepath):
    return pd.read_csv(filepath)

def filter_by_column(data, column, condition_fn):
    return data[data[column].apply(condition_fn)]

def filter_by_salary(data, threshold):
    return data[data["salary"] > threshold]

def top_n_rows(data, n):
    return data.head(n)

# === Strategies ===

def analysis_one(filepath, column, condition_fn):
    data = read_csv(filepath)
    return filter_by_column(data, column, condition_fn)

def analysis_two(filepath):
    data = read_csv(filepath)
    return filter_by_salary(data, 60000)

def analysis_three(filepath, n):
    data = read_csv(filepath)
    return top_n_rows(data, n)

def analysis_four(filepath):
    data = read_csv(filepath)
    return data.sort_values(by="age")

def analysis_five(filepath):
    data = read_csv(filepath)
    return data.groupby("age").mean()

# === Strategy Registry ===

strategy_registry = {
    "analysis_one": analysis_one,
    "analysis_two": analysis_two,
    "analysis_three": analysis_three,
    "analysis_four": analysis_four,
    "analysis_five": analysis_five,
}

# === Strategy Parameters (per run) ===

strategy_params = {
    "analysis_one": {
        "filepath": "data.csv",
        "column": "age",
        "condition_fn": lambda x: x > 30,
    },
    "analysis_two": {
        "filepath": "data.csv",
    },
    "analysis_three": {
        "filepath": "data.csv",
        "n": 2,
    },
    "analysis_four": {
        "filepath": "data.csv",
    },
    "analysis_five": {
        "filepath": "data.csv",
    },
}

# === Main ===

def main():
    # Create test CSV
    with open("data.csv", "w") as f:
        f.write("name,age,salary\nAlice,25,50000\nBob,35,60000\nCarol,45,70000\nDan,55,80000\n")

    strategy_name = "analysis_one"  # <- Just change this string!

    if strategy_name not in strategy_registry:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    strategy_fn = strategy_registry[strategy_name]
    params = strategy_params[strategy_name]

    result = strategy_fn(**params)

    print("\nResult:")
    print(result)

if __name__ == "__main__":
    main()

```

Strategy file example :
```python
from io import read_csv
from cleaning import filter_by_column

def analysis_one(filepath, column, condition_fn):
    data = read_csv(filepath)
    return filter_by_column(data, column, condition_fn)

```

`src/strategies/init.py`

```python
from .analysis_one import analysis_one
from .analysis_two import analysis_two

strategy_registry = {
    "analysis_one": analysis_one,
    "analysis_two": analysis_two,
}

```

in main.py 

```
from strategies import strategy_registry

strategy_name = "analysis_one"
params = { ... }
result = strategy_registry[strategy_name](**params)
```

Bash to generate modular structure:

```bash
#!/bin/bash

# Create directories
mkdir -p src/strategies

# Create src/io.py
cat > src/io.py << EOF
import pandas as pd

def read_csv(filepath):
    print(f"Reading CSV from {filepath}")
    return pd.read_csv(filepath)
EOF

# Create src/cleaning.py
cat > src/cleaning.py << EOF
def filter_by_column(data, column, condition_fn):
    print(f"Filtering data where {column} meets condition")
    return data[data[column].apply(condition_fn)]

def filter_by_salary(data, threshold=60000):
    print(f"Filtering where salary > {threshold}")
    return data[data["salary"] > threshold]
EOF

# Create src/strategies/analysis_one.py
cat > src/strategies/analysis_one.py << EOF
from io import read_csv
from cleaning import filter_by_column

def analysis_one(filepath, column, condition_fn):
    data = read_csv(filepath)
    return filter_by_column(data, column, condition_fn)
EOF

# Create src/strategies/analysis_two.py
cat > src/strategies/analysis_two.py << EOF
from io import read_csv
from cleaning import filter_by_salary

def analysis_two(filepath):
    data = read_csv(filepath)
    return filter_by_salary(data)
EOF

# Create src/strategies/__init__.py
cat > src/strategies/__init__.py << EOF
from .analysis_one import analysis_one
from .analysis_two import analysis_two

strategy_registry = {
    "analysis_one": analysis_one,
    "analysis_two": analysis_two,
}
EOF

# Create src/main.py
cat > src/main.py << EOF
from strategies import strategy_registry

def main():
    filepath = "data.csv"
    with open(filepath, "w") as f:
        f.write("name,age,salary\\nAlice,25,50000\\nBob,35,60000\\nCarol,45,70000\\n")

    strategy_name = "analysis_one"

    if strategy_name not in strategy_registry:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    if strategy_name == "analysis_one":
        params = {
            "filepath": filepath,
            "column": "age",
            "condition_fn": lambda x: x > 30,
        }
    else:
        params = {"filepath": filepath}

    result = strategy_registry[strategy_name](**params)

    print("\\nResult:")
    print(result)

if __name__ == "__main__":
    main()
EOF

echo "✅ Project structure created. Run it with: python3 src/main.py"

```
