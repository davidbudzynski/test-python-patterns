class StrategyFactory:
    _registry = {}

    @classmethod
    def register(cls, name):
        def inner(strategy_cls):
            cls._registry[name] = strategy_cls
            return strategy_cls
        return inner

    @classmethod
    def create(cls, name, *args, **kwargs):
        strategy_cls = cls._registry.get(name)
        if not strategy_cls:
            raise ValueError(f"Unknown strategy: {name}")
        return strategy_cls(*args, **kwargs)
