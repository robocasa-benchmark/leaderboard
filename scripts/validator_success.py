import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def main():
    repo_root = Path(__file__).resolve().parents[1]
    schema_path = repo_root / "schemas" / "submission.schema.json"
    submissions_dir = repo_root / "submissions"

    if not schema_path.exists():
        print(f"Error: schema file not found at {schema_path}")
        sys.exit(1)

    if not submissions_dir.exists():
        print(f"Error: submissions directory not found at {submissions_dir}")
        sys.exit(1)

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error reading schema file: {e}")
        sys.exit(1)

    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
    except Exception as e:
        print(f"Error: invalid JSON schema: {e}")
        sys.exit(1)

    submission_files = sorted(submissions_dir.glob("*.json"))

    if not submission_files:
        print("No submission JSON files found.")
        return

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

    if has_errors:
        sys.exit(1)

    print("\nAll submission files are valid.")


if __name__ == "__main__":
    main()