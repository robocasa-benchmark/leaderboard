# RoboCasa Benchmark Leaderboard 🏆

This repository hosts the official RoboCasa365 leaderboard. It tracks multi-task policy learning performance on RoboCasa365 and is open to community submissions via pull requests.

We analyze multi-task learning through three RoboCasa365 splits — **Atomic-Seen**, **Composite-Seen**, and **Composite-Unseen** — and report average task success rate (in %) for each. This accounts for a total of 50 target tasks being evaluated. These evaluation splits and target datasets are explained in further detail in our [documentation](https://robocasa.ai/docs/build/html/datasets/datasets_overview.html).

To add your results, export a JSON file in the format below and open a pull request that adds it to the `submissions/` directory. The results will be displayed on our main [website](https://robocasa.ai/leaderboard.html).

> [!NOTE]
> For models that cannot be released open-source (`"open_source": "no"`), you must grant the RoboCasa team private access to your model checkpoint and evaluation code so we can verify results on our benchmark.

## Submission template

Each submission is a single JSON file added to `submissions/` with this structure: :

```json
{
  "model_name": "<string>",
  "policy_family": "<string>",
  "date": "<YYYY-MM-DD, e.g. '2026-04-02'>",
  "submission_source": "external",
  "robocasa_version": "<string, default '1.0.1'>",
  "atomic_seen_success": <number 0–100>,
  "composite_seen_success": <number 0–100>,
  "composite_unseen_success": <number 0–100>,
  "code_url": "<URL>",
  "commit_hash": "<git commit hash>",
  "checkpoint_url": "<URL>",
  "paper_link": "<URL>",
  "open_source": "yes",
  "wandb": "<wandb run or project URL/reference>",
  "training_config": {
    "batch_size": "<integer>",
    "num_training_steps": "<integer>"
  },
  "notes": "<optional free text>"
}
```

> [!NOTE]
> For any field where the information is unavailable or not applicable, write `"N/A"` and explain the reason in the "notes" field.
> The current default `robocasa_version` is `1.0.1` until a new update is announced.

Here’s a sample JSON: [gr00t_n1.5_2026_05_19.json](https://github.com/robocasa-benchmark/leaderboard/blob/main/submissions/gr00t_n1.5_2026_05_19.json)
