"""Weighted overall success for the 50-task multi-task benchmark (18 + 16 + 16 tasks)."""

from __future__ import annotations

# Matches leaderboard split_counts: atomic_seen, composite_seen, composite_unseen.
WEIGHT_ATOMIC_SEEN = 18
WEIGHT_COMPOSITE_SEEN = 16
WEIGHT_COMPOSITE_UNSEEN = 16
TOTAL_WEIGHT = WEIGHT_ATOMIC_SEEN + WEIGHT_COMPOSITE_SEEN + WEIGHT_COMPOSITE_UNSEEN  # 50


def compute_overall_success(
    atomic_seen_success: float,
    composite_seen_success: float,
    composite_unseen_success: float,
) -> float:
    """
    Task-weighted mean success (percent), rounded to one decimal place
    (same convention as prior hand-entered overall_success values).
    """
    raw = (
        WEIGHT_ATOMIC_SEEN * atomic_seen_success
        + WEIGHT_COMPOSITE_SEEN * composite_seen_success
        + WEIGHT_COMPOSITE_UNSEEN * composite_unseen_success
    ) / TOTAL_WEIGHT
    return round(raw, 1)
