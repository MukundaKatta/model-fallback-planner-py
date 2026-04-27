from model_fallback_planner import plan_fallbacks, choose_fallback


MODELS = [
    {"name": "claude-sonnet", "capabilities": ["chat", "tools"], "cost": 3, "priority": 5, "healthy": True},
    {"name": "claude-haiku", "capabilities": ["chat", "tools"], "cost": 1, "priority": 3, "healthy": True},
    {"name": "gpt-5", "capabilities": ["chat"], "cost": 5, "priority": 8, "healthy": True},
    {"name": "broken", "capabilities": ["chat"], "cost": 0, "priority": 100, "healthy": False},
]


def test_no_filters_returns_all_healthy_sorted():
    chain = plan_fallbacks(MODELS)
    assert chain[0]["name"] == "gpt-5"  # highest priority
    assert "broken" not in [m["name"] for m in chain]


def test_filters_by_capability():
    chain = plan_fallbacks(MODELS, capabilities=["tools"])
    names = [m["name"] for m in chain]
    assert "gpt-5" not in names
    assert "claude-sonnet" in names


def test_filters_by_max_cost():
    chain = plan_fallbacks(MODELS, max_cost=2)
    names = [m["name"] for m in chain]
    assert names == ["claude-haiku"]


def test_choose_fallback_returns_chain():
    res = choose_fallback(MODELS, capabilities=["tools"])
    assert res.model["name"] in ("claude-sonnet", "claude-haiku")
    assert len(res.chain) >= 1


def test_no_match_returns_none():
    res = choose_fallback(MODELS, capabilities=["vision-pro-9000"])
    assert res.model is None
    assert res.chain == []


def test_priority_orders_chain():
    a = {"name": "a", "capabilities": [], "cost": 0, "priority": 1}
    b = {"name": "b", "capabilities": [], "cost": 0, "priority": 5}
    chain = plan_fallbacks([a, b])
    assert [m["name"] for m in chain] == ["b", "a"]


def test_cost_breaks_priority_tie():
    a = {"name": "a", "capabilities": [], "cost": 5, "priority": 3}
    b = {"name": "b", "capabilities": [], "cost": 1, "priority": 3}
    chain = plan_fallbacks([a, b])
    assert [m["name"] for m in chain] == ["b", "a"]


def test_unhealthy_excluded():
    chain = plan_fallbacks([
        {"name": "ok", "capabilities": [], "cost": 0, "priority": 1, "healthy": True},
        {"name": "bad", "capabilities": [], "cost": 0, "priority": 99, "healthy": False},
    ])
    assert [m["name"] for m in chain] == ["ok"]
