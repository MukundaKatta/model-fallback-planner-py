# model-fallback-planner-py

Plan model fallback chains from capability, cost, and health data. Pure Python, zero deps. Python port of [`@mukundakatta/model-fallback-planner`](https://www.npmjs.com/package/@mukundakatta/model-fallback-planner).

```bash
pip install model-fallback-planner-py
```

```python
from model_fallback_planner import plan_fallbacks, choose_fallback

models = [
    {"name": "claude-sonnet", "capabilities": ["chat", "tools"], "cost": 3, "priority": 5, "healthy": True},
    {"name": "claude-haiku", "capabilities": ["chat", "tools"], "cost": 1, "priority": 3, "healthy": True},
    {"name": "gpt-5", "capabilities": ["chat"], "cost": 5, "priority": 8, "healthy": True},
]

choose_fallback(models, capabilities=["tools"], max_cost=4)
# FallbackChoice(model={...claude-sonnet...}, chain=[...claude-sonnet, claude-haiku])
```

## License

MIT
