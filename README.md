## Submission template

Each submission is a single JSON file added to `submissions/` with this structure: :

```json
{
  "model_name": "<string, e.g. 'pi0.5'>",
  "benchmark_track": "<string, e.g. 'RoboCasa365-main'>",
  "policy_family": "<string, e.g. 'openpi' | 'gr00t' | 'diffusion_policy' | 'other'>",
  "date": "<YYYY-MM-DD, e.g. '2026-04-02'>",
  "submission_source": "external",
  "robocasa_version": "<string, e.g. '1.0.0'>",
  "atomic_success": <number 0–100>,
  "composite_seen_success": <number 0–100>,
  "composite_unseen_success": <number 0–100>,
  "overall_success": <number 0–100>,
  "code_url": "<URL>",
  "commit_hash": "<git commit hash>",
  "checkpoint_url": "<URL>",
  "notes": "<optional free text>"
}
```

> [!NOTE]
> For any field where the information is unavailable or not applicable, use `"N/A"`.

Here’s a sample JSON: [dp_2026_04_02.json](https://github.com/robocasa-benchmark/leaderboard/blob/main/dp_2026_04_02.json)