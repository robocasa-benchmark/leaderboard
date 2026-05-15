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
from typing import Any

import yaml

from weighted_overall import compute_overall_success

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
        "note": "Evaluated with 2/3 shorter horizon",
    },
    # Keep note mapping when model_name is stored as a literal display name.
    "GR00T N1.5": {
        "note": "Evaluated with 2/3 shorter horizon",
    },
}
SUBMISSION_MD_BASE_URL = "https://github.com/robocasa-benchmark/leaderboard/blob/main/submissions_md"


def _default_output_path(repo_root: Path) -> Path:
    sibling = repo_root.parent / "robocasa-web" / "_data" / "robocasa365_leaderboard.yml"
    if sibling.parent.is_dir():
        return sibling
    return repo_root / "website" / "robocasa365_leaderboard.yml"


def _load_existing_policies(out_path: Path) -> list[dict[str, Any]]:
    if not out_path.exists():
        return []
    try:
        with out_path.open("r", encoding="utf-8") as f:
            payload = yaml.safe_load(f) or {}
    except Exception:
        return []
    policies = payload.get("policies", [])
    return policies if isinstance(policies, list) else []


def _policy_match_key(policy: dict[str, Any]) -> tuple[str, str] | None:
    """
    Match generated rows to existing rows by stable identity.

    Preference order:
      1) checkpoint_url
      2) code_url
      3) name (fallback for legacy rows)
    """
    checkpoint_url = policy.get("checkpoint_url")
    if checkpoint_url:
        return ("checkpoint_url", str(checkpoint_url))
    code_url = policy.get("code_url")
    if code_url:
        return ("code_url", str(code_url))
    name = policy.get("name")
    if name:
        return ("name", str(name))
    return None


def _merge_existing_fields(
    generated: dict[str, Any], existing: dict[str, Any]
) -> dict[str, Any]:
    """
    Keep metadata from existing rows (e.g. notes/flags) while letting generated
    values win for freshly computed fields.
    """
    merged = dict(generated)
    # Preserve curated presentation metadata when a row already exists.
    preserve_existing_keys = {"name", "short_name", "family", "color", "note"}

    for key, value in existing.items():
        if key not in merged:
            merged[key] = value
        elif merged[key] is None and value is not None:
            merged[key] = value
        elif key in preserve_existing_keys and value not in (None, ""):
            merged[key] = value
    return merged


def _policy_row(data: dict, rank: int) -> dict:
    mid = data["model_name"]
    disp = MODEL_DISPLAY.get(mid, {})
    name = disp.get("name") or data["model_name"] or data["policy_family"]
    short_name = disp.get("short_name") or mid
    family = disp.get("family") or data["policy_family"]
    color = disp.get("color", "#64748b")

    a = float(data["atomic_seen_success"])
    cs = float(data["composite_seen_success"])
    cu = float(data["composite_unseen_success"])
    overall = compute_overall_success(a, cs, cu)
    training_cfg = data.get("training_config", {})
    if not isinstance(training_cfg, dict):
        training_cfg = {}

    training_config_out: dict[str, Any] = {}
    if training_cfg.get("batch_size") is not None:
        training_config_out["batch_size"] = int(training_cfg["batch_size"])
    if training_cfg.get("num_training_steps") is not None:
        num_training_steps = int(training_cfg["num_training_steps"])
        training_config_out["num_training_steps"] = num_training_steps
        training_config_out["num_training_steps_display"] = f"{num_training_steps:,}"

    return {
        "rank": rank,
        "name": name,
        "short_name": short_name,
        "family": family,
        "color": color,
        "score": overall,
        "atomic_seen": a,
        "composite_seen": cs,
        "composite_unseen": cu,
        "training_config": training_config_out,
        "note": disp.get("note"),
        "submission_url": f"{SUBMISSION_MD_BASE_URL}/{Path(data['_submission_filename']).stem}.md",
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
    existing_policies = _load_existing_policies(out_path)
    existing_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for policy in existing_policies:
        if isinstance(policy, dict):
            key = _policy_match_key(policy)
            if key is not None:
                existing_by_key[key] = policy

    submissions_dir = repo_root / "submissions"
    rows: list[dict] = []

    for file_path in sorted(submissions_dir.glob("*.json")):
        data = json.loads(file_path.read_text(encoding="utf-8"))
        data["_submission_filename"] = file_path.name
        rows.append(data)

    def _sort_key(row: dict) -> float:
        return compute_overall_success(
            float(row["atomic_seen_success"]),
            float(row["composite_seen_success"]),
            float(row["composite_unseen_success"]),
        )

    rows.sort(key=_sort_key, reverse=True)

    generated_policies = [_policy_row(data, rank) for rank, data in enumerate(rows, start=1)]
    policies: list[dict] = []
    for policy in generated_policies:
        key = _policy_match_key(policy)
        existing = existing_by_key.get(key) if key is not None else None
        if existing is not None:
            policies.append(_merge_existing_fields(policy, existing))
        else:
            policies.append(policy)

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
