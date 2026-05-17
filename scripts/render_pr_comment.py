"""
Render a PR comment body summarizing submission JSON file(s) in a pull request.

Usage:
  python scripts/render_pr_comment.py path/to/submissions/foo.json
  python scripts/render_pr_comment.py   # no files: prints a helpful message
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from generate_submission_markdown import render_pr_submission_comment

COMMENT_TAG = "robocasa-submission-summary"


def _no_json_message() -> str:
    return "\n".join(
        [
            f"<!-- {COMMENT_TAG} -->",
            "### Submission summary (auto-generated)",
            "",
            "No `submissions/*.json` file was found in this PR. Add your submission JSON under `submissions/`.",
            "",
        ]
    )


def _multiple_json_message(filenames: list[str]) -> str:
    listed = ", ".join(f"`{name}`" for name in filenames)
    return "\n".join(
        [
            f"<!-- {COMMENT_TAG} -->",
            "### Submission summary (auto-generated)",
            "",
            f"Multiple submission JSON files were changed in this PR ({listed}). "
            "Please include exactly one submission per PR.",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "json_files",
        nargs="*",
        help="Submission JSON paths changed in the PR (e.g. submissions/foo.json).",
    )
    args = parser.parse_args()

    paths = [Path(p) for p in args.json_files if p.endswith(".json")]
    paths = [p for p in paths if "submissions" in p.parts]

    if not paths:
        sys.stdout.write(_no_json_message())
        return

    if len(paths) > 1:
        sys.stdout.write(_multiple_json_message([p.name for p in paths]))
        return

    json_path = paths[0]
    with json_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    sys.stdout.write(render_pr_submission_comment(payload, json_path.name))


if __name__ == "__main__":
    main()
