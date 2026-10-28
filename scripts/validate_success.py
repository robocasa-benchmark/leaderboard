import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


# Each leaderboard validates its own folder against its own schema.
BOARDS = [
    ("standard", "submissions", "submission.schema.json"),
    ("agentic", "submissions/agentic", "agentic_submission.schema.json"),
]


def main():
    repo_root = Path(__file__).resolve().parents[1]
    has_errors = False
    for board, folder, schema_name in BOARDS:
        print(f"== {board} ({folder}/)")
        if not validate_board(repo_root / folder, repo_root / "schemas" / schema_name):
            has_errors = True

    if has_errors:
        sys.exit(1)

    print("\nAll submission files are valid.")


def validate_board(submissions_dir: Path, schema_path: Path) -> bool:
    if not schema_path.exists():
        print(f"Error: schema file not found at {schema_path}")
        return False

    if not submissions_dir.exists():
        print(f"Error: submissions directory not found at {submissions_dir}")
        return False

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error reading schema file: {e}")
        return False

    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
    except Exception as e:
        print(f"Error: invalid JSON schema: {e}")
        return False

    submission_files = sorted(submissions_dir.glob("*.json"))

    if not submission_files:
        print("No submission JSON files found.")
        return True

    has_errors = False

    for file_path in submission_files:
        try:
            submission = json.loads(file_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[FAIL] {file_path.name}: invalid JSON ({e})")
            has_errors = True
            continue

        errors = sorted(validator.iter_errors(submission), key=lambda e: list(e.path))

        if errors:
            has_errors = True
            print(f"[FAIL] {file_path.name}")
            for error in errors:
                path = ".".join(str(x) for x in error.path)
                if path:
                    print(f"  - {path}: {error.message}")
                else:
                    print(f"  - {error.message}")
        else:
            print(f"[OK]   {file_path.name}")

    return not has_errors


if __name__ == "__main__":
    main()