# RoboCasa Benchmark Leaderboard 🏆

This repository hosts the official RoboCasa365 leaderboard and JSON submission files. It tracks multi-task policy learning performance on RoboCasa365 and is open to community submissions via pull requests.

We analyze multi-task learning through three RoboCasa365 splits — **Atomic-Seen**, **Composite-Seen**, and **Composite-Unseen** — and report average task success rate (in %) for each. This accounts for a total of 50 target tasks being evaluated. These evaluation splits and target datasets are explained in further detail in our [documentation](https://robocasa.ai/docs/build/html/datasets/datasets_overview.html#target-datasets).

To add your results, export a JSON file in the format below and open a pull request that adds it to the `submissions/` directory.

## Submission template

Each submission is a single JSON file added to `submissions/` with this structure: :

```json
{
  "model_name": "<string>",
  "policy_family": "<string>",
  "date": "<YYYY-MM-DD, e.g. '2026-04-02'>",
  "submission_source": "external",
  "robocasa_version": "<string, e.g. '1.0.0'>",
  "atomic_seen_success": <number 0–100>,
  "composite_seen_success": <number 0–100>,
  "composite_unseen_success": <number 0–100>,
  "code_url": "<URL>",
  "commit_hash": "<git commit hash>",
  "checkpoint_url": "<URL>",
  "notes": "<optional free text>"
}
```

> [!NOTE]
> For any field where the information is unavailable or not applicable, write `"N/A"` and explain the reason in the "notes" field.

**Overall score on the website** is not part of the JSON. It is computed as a task-weighted mean of the three splits (18 Atomic-Seen + 16 Composite-Seen + 16 Composite-Unseen = 50 tasks), each rounded to one decimal:  
`(18×atomic_seen_success + 16×composite_seen_success + 16×composite_unseen_success) / 50`.

Here’s a sample JSON: [dp_2026_04_02.json](https://github.com/robocasa-benchmark/leaderboard/blob/main/submissions/dp_2026_04_02.json)