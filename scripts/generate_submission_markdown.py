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
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
GITHUB_REPO_URL = "https://github.com/robocasa-benchmark/leaderboard"


def _fmt_steps(value: Any) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def _is_na(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().upper() in {"", "N/A", "NA"}
    return False


def _fmt_field(label: str, value: Any) -> str:
    return f"- {label}: {value}"


def _append_field(lines: list[str], label: str, value: Any) -> None:
    if _is_na(value):
        return
    lines.append(_fmt_field(label, value))


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


# Manual override for the PR link shown in markdown (not part of the submission
# JSON / schema). Normally the PR is auto-detected from git history (see
# `_pr_url_from_git`); only add an entry here to pin or correct a link.
SUBMISSION_PR_URLS: dict[str, str] = {}


def _pr_url_from_git(filename: str) -> str | None:
    """Best-effort: find the PR that merged a submission JSON into main.

    Looks up the commit that first added `submissions/<filename>`, then finds the
    `Merge pull request #N` commit that brought it onto the current branch and
    returns the PR URL. Returns None if it can't be determined (e.g. the file was
    committed directly to main, or git history isn't available).
    """
    rel_path = f"submissions/{filename}"

    def _git(*args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout

    try:
        # Walk main's first-parent line only: a PR merge shows the file as Added
        # on the merge commit ("Merge pull request #N ..."), and a squash merge
        # shows it on a commit whose subject ends with "(#N)". The oldest (last)
        # such commit is where the file first reached main. Files committed
        # directly to main have no PR number -> no PR link.
        adds = _git(
            "log", "--first-parent", "--diff-filter=A", "--format=%s", "--", rel_path
        ).splitlines()
        if not adds:
            return None
        subject = adds[-1]
        match = re.search(r"#(\d+)", subject)
        if match:
            return f"{GITHUB_REPO_URL}/pull/{match.group(1)}"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None
    return None


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
        _append_field(lines, "Submission JSON filename", filename)
    _append_field(lines, "Model name", data.get("model_name"))
    _append_field(lines, "Policy family", data.get("policy_family"))
    if not _is_na(data.get("date")):
        _append_field(lines, "Date evaluated", _fmt_date_mmddyyyy(data.get("date")))
    _append_field(lines, "Submission source", data.get("submission_source"))
    _append_field(lines, "RoboCasa version", data.get("robocasa_version"))
    _append_field(lines, "Atomic-Seen success", data.get("atomic_seen_success"))
    _append_field(lines, "Composite-Seen success", data.get("composite_seen_success"))
    _append_field(lines, "Composite-Unseen success", data.get("composite_unseen_success"))

    code_url = data.get("code_url")
    is_open_source = data.get("open_source") != "no"
    if is_open_source:
        if not _is_na(code_url):
            lines.append(_fmt_field("Code URL", f"[{code_url}]({code_url})"))

        checkpoint_url = data.get("checkpoint_url")
        if not _is_na(checkpoint_url):
            lines.append(_fmt_field("Checkpoint URL", f"[{checkpoint_url}]({checkpoint_url})"))

    commit_hash = data.get("commit_hash")
    if not _is_na(commit_hash):
        _append_field(lines, "Commit hash", commit_hash)

    paper_link = data.get("paper_link")
    if not _is_na(paper_link):
        lines.append(_fmt_field("Paper link", f"[{paper_link}]({paper_link})"))

    _append_field(lines, "Open Source", data.get("open_source"))

    pr_url = SUBMISSION_PR_URLS.get(filename) or _pr_url_from_git(filename)
    if pr_url:
        lines.append(_fmt_field("PR", f"[{pr_url}]({pr_url})"))

    wandb = data.get("wandb")
    if not _is_na(wandb):
        lines.append(_fmt_field("W&B", f"[{wandb}]({wandb})"))

    training_cfg = data.get("training_config")
    if isinstance(training_cfg, dict):
        batch_size = training_cfg.get("batch_size")
        num_training_steps = training_cfg.get("num_training_steps")
        if not _is_na(batch_size):
            _append_field(lines, "Batch size", batch_size)
        if not _is_na(num_training_steps):
            _append_field(lines, "Number of training steps", _fmt_steps(num_training_steps))

    notes = data.get("notes")
    if not _is_na(notes):
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
