"""
Aggregate submissions/*.json into Jekyll data for robocasa-web (leaderboard.html).

By default, if ../robocasa-web exists (sibling of this repo), writes:
  robocasa-web/_data/robocasa365_leaderboard.yml
Otherwise writes:
  website/robocasa365_leaderboard.yml
Use --output PATH to override.

`updated_at` in the YAML is the UTC calendar date when this script runs (sync/build time),
not the latest submission JSON `date` field.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

# Static copy on the site (see leaderboard.html "How we evaluate").
BENCHMARK_META = {
    "benchmark_name": "Multi-Task Learning",
    "metric_label": "Average task success rate",
    "evaluation_split": "Pretrain scenes",
    "benchmark_tasks": 50,
    "split_counts": {
        "atomic_seen": 18,
        "composite_seen": 16,
        "composite_unseen": 16,
    },
}

# Display names / table keys for known baseline model_name values; others use fallbacks.
MODEL_DISPLAY = {
    "pi0": {
        "name": "π0",
        "short_name": "pi0",
        "family": "OpenPI",
        "color": "#10b981",
    },
    "pi0.5": {
        "name": "π0.5",
        "short_name": "pi0.5",
        "family": "OpenPI",
        "color": "#f59e0b",
    },
    "dp": {
        "name": "Diffusion Policy",
        "short_name": "DP",
        "family": "Diffusion",
        "color": "#3b82f6",
    },
    "gr00t_n1.5": {
        "name": "GR00T N1.5",
        "short_name": "GR00T",
        "family": "VLA",
        "color": "#8b5cf6",
    },
}


def _default_output_path(repo_root: Path) -> Path:
    sibling = repo_root.parent / "robocasa-web" / "_data" / "robocasa365_leaderboard.yml"
    if sibling.parent.is_dir():
        return sibling
    return repo_root / "website" / "robocasa365_leaderboard.yml"


def _policy_row(data: dict, rank: int) -> dict:
    mid = data["model_name"]
    disp = MODEL_DISPLAY.get(mid, {})
    name = disp.get("name") or data["policy_family"]
    short_name = disp.get("short_name") or mid
    family = disp.get("family") or data["policy_family"]
    color = disp.get("color", "#64748b")

    return {
        "rank": rank,
        "name": name,
        "short_name": short_name,
        "family": family,
        "color": color,
        "score": float(data["overall_success"]),
        "atomic_seen": float(data["atomic_seen_success"]),
        "composite_seen": float(data["composite_seen_success"]),
        "composite_unseen": float(data["composite_unseen_success"]),
        "code_url": data["code_url"],
        "checkpoint_url": data["checkpoint_url"],
    }


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output YAML path (default: sibling robocasa-web/_data/... or website/...)",
    )
    args = parser.parse_args()
    out_path = args.output or _default_output_path(repo_root)

    submissions_dir = repo_root / "submissions"
    rows: list[dict] = []

    for file_path in sorted(submissions_dir.glob("*.json")):
        data = json.loads(file_path.read_text(encoding="utf-8"))
        rows.append(data)

    rows.sort(key=lambda x: float(x["overall_success"]), reverse=True)

    policies = [_policy_row(data, rank) for rank, data in enumerate(rows, start=1)]

    # When the YAML was generated (sync / local build), not max submission date.
    updated_at = datetime.now(timezone.utc).strftime("%m/%d/%Y")

    payload = {
        "updated_at": updated_at,
        **BENCHMARK_META,
        "policies": policies,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        # Quote date so YAML parsers don't treat it as a date literal.
        f.write(f'updated_at: "{updated_at}"\n')
        yaml.dump(
            {k: v for k, v in payload.items() if k != "updated_at"},
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=120,
        )

    print(f"Wrote {len(policies)} policies to {out_path}")


if __name__ == "__main__":
    main()
