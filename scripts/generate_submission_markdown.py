"""
Generate Markdown summaries from submission JSON files.

By default, reads:
  submissions/*.json
and writes:
  submissions_md/<same-name>.md
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def _fmt_steps(value: Any) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def _fmt_field(label: str, value: Any) -> str:
    return f"- {label}: {value}"


_GITHUB_USER_RE = re.compile(r"@([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,38}))")
_URL_RE = re.compile(r"(?<!\]\()https?://\S+")


def _linkify_notes(notes: str) -> str:
    """Turn @handles and bare URLs into Markdown links for GitHub rendering."""
    text = _GITHUB_USER_RE.sub(
        lambda m: f"[@{m.group(1)}](https://github.com/{m.group(1)})", notes
    )

    def _link_url(match: re.Match[str]) -> str:
        raw = match.group(0)
        url = raw.rstrip(".,;:!?)")
        suffix = raw[len(url) :]
        return f"[{url}]({url}){suffix}"

    return _URL_RE.sub(_link_url, text)


# PR URLs for markdown only (not part of submission JSON / schema).
SUBMISSION_PR_URLS: dict[str, str] = {
    "gwp01_2026_05_11.json": "https://github.com/robocasa-benchmark/leaderboard/pull/1",
    "rldx-1_2026_05_20.json": "https://github.com/robocasa-benchmark/leaderboard/pull/3",
    "worlddreamer_2026_06_20.json": "https://github.com/robocasa-benchmark/leaderboard/pull/5",
}


def _fmt_date_mmddyyyy(value: Any) -> str:
    if not value:
        return "N/A"
    try:
        dt = datetime.strptime(str(value), "%Y-%m-%d")
        return dt.strftime("%m/%d/%Y")
    except ValueError:
        return str(value)


def render_submission_fields(
    data: dict[str, Any],
    filename: str,
    *,
    include_filename: bool = False,
) -> list[str]:
    lines: list[str] = []
    if include_filename:
        lines.append(_fmt_field("Submission JSON filename", filename))
    lines.append(_fmt_field("Model name", data.get("model_name", "N/A")))
    lines.append(_fmt_field("Policy family", data.get("policy_family", "N/A")))
    lines.append(_fmt_field("Date evaluated", _fmt_date_mmddyyyy(data.get("date"))))
    lines.append(_fmt_field("Submission source", data.get("submission_source", "N/A")))
    lines.append(_fmt_field("RoboCasa version", data.get("robocasa_version", "N/A")))
    lines.append(_fmt_field("Atomic-Seen success", data.get("atomic_seen_success", "N/A")))
    lines.append(_fmt_field("Composite-Seen success", data.get("composite_seen_success", "N/A")))
    lines.append(
        _fmt_field("Composite-Unseen success", data.get("composite_unseen_success", "N/A"))
    )

    code_url = data.get("code_url")
    if code_url:
        lines.append(_fmt_field("Code URL", f"[{code_url}]({code_url})"))
    else:
        lines.append(_fmt_field("Code URL", "N/A"))

    lines.append(_fmt_field("Commit hash", data.get("commit_hash", "N/A")))

    checkpoint_url = data.get("checkpoint_url")
    if checkpoint_url:
        lines.append(_fmt_field("Checkpoint URL", f"[{checkpoint_url}]({checkpoint_url})"))
    else:
        lines.append(_fmt_field("Checkpoint URL", "N/A"))

    pr_url = SUBMISSION_PR_URLS.get(filename)
    if pr_url:
        lines.append(_fmt_field("PR", f"[{pr_url}]({pr_url})"))

    wandb = data.get("wandb")
    if wandb:
        lines.append(_fmt_field("W&B", f"[{wandb}]({wandb})"))

    training_cfg = data.get("training_config")
    if isinstance(training_cfg, dict):
        batch_size = training_cfg.get("batch_size")
        num_training_steps = training_cfg.get("num_training_steps")
        if batch_size is not None:
            lines.append(_fmt_field("Batch size", batch_size))
        if num_training_steps is not None:
            lines.append(_fmt_field("Number of training steps", _fmt_steps(num_training_steps)))

    notes = data.get("notes")
    if notes:
        lines.append(_fmt_field("Notes", _linkify_notes(str(notes))))

    return lines


def render_submission_markdown(data: dict[str, Any], filename: str) -> str:
    lines = ["## Submission details", ""]
    lines.extend(render_submission_fields(data, filename))
    lines.append("")
    return "\n".join(lines)


def render_pr_submission_comment(
    data: dict[str, Any], filename: str
) -> str:
    lines = [
        "<!-- robocasa-submission-summary -->",
        "### Submission summary (auto-generated)",
        "",
        f"_From `{filename}`. Edit the JSON in this PR to update this summary._",
        "",
    ]
    lines.extend(render_submission_fields(data, filename, include_filename=True))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--submissions-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "submissions",
        help="Directory containing submission JSON files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "submissions_md",
        help="Directory where markdown summaries will be written.",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    generated = 0

    for json_path in sorted(args.submissions_dir.glob("*.json")):
        with json_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        md_text = render_submission_markdown(payload, json_path.name)
        output_path = args.output_dir / f"{json_path.stem}.md"
        with output_path.open("w", encoding="utf-8") as f:
            f.write(md_text)
        generated += 1

    print(f"Generated {generated} markdown files in {args.output_dir}")


if __name__ == "__main__":
    main()
