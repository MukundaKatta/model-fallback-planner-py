"""model_fallback_planner -- plan model fallback chains from capability, cost, health."""

from dataclasses import dataclass
from typing import Any, Iterable, Optional


@dataclass(frozen=True)
class FallbackChoice:
    model: Optional[dict]
    chain: list[dict]


def plan_fallbacks(
    models: Iterable[dict],
    *,
    capabilities: Optional[Iterable[str]] = None,
    max_cost: float = float("inf"),
) -> list[dict]:
    """Filter + rank candidate models for a request.

    Filters out: missing required capability, over budget, or `healthy=False`.
    Sorts by `priority` desc, then `cost` asc.
    """
    caps = list(capabilities or [])

    def passes(m: dict) -> bool:
        if not isinstance(m, dict):
            return False
        m_caps = m.get("capabilities") or []
        if any(c not in m_caps for c in caps):
            return False
        if float(m.get("cost") or 0) > max_cost:
            return False
        if m.get("healthy") is False:
            return False
        return True

    return sorted(
        (m for m in models if passes(m)),
        key=lambda m: (-(m.get("priority") or 0), m.get("cost") or 0),
    )


def choose_fallback(
    models: Iterable[dict],
    *,
    capabilities: Optional[Iterable[str]] = None,
    max_cost: float = float("inf"),
) -> FallbackChoice:
    """Plan the chain and return the head model + the full chain."""
    chain = plan_fallbacks(models, capabilities=capabilities, max_cost=max_cost)
    return FallbackChoice(model=chain[0] if chain else None, chain=chain)


__version__ = "0.1.0"
__all__ = ["plan_fallbacks", "choose_fallback", "FallbackChoice"]
