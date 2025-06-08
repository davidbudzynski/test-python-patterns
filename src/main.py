import importlib
import pkgutil
from factory.strategy_factory import StrategyFactory

def import_all_strategies():
    import strategies  # package must exist with __init__.py
    for _, module_name, _ in pkgutil.iter_modules(strategies.__path__):
        importlib.import_module(f"strategies.{module_name}")


def age_greater_than_30(x):
    return x > 30

def main():
    import_all_strategies()
    # Create dummy CSV
    with open("data.csv", "w") as f:
        f.write("name,age,salary\nAlice,25,50000\nBob,35,60000\nCarol,45,70000\n")

    strategy_name = "analysis_one"
    filepath = "data.csv"
    column = "age"
    condition_fn = age_greater_than_30

    strategy = StrategyFactory.create(strategy_name, filepath, column, condition_fn)
    result = strategy.execute()

    print("Final Result:")
    print(result)

if __name__ == "__main__":
    main()
