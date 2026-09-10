# RoboCasa Benchmark Leaderboard 🏆

This repository hosts the official RoboCasa365 leaderboard. It tracks multi-task policy learning performance on RoboCasa365 and is open to community submissions via pull requests.

We analyze multi-task learning through three RoboCasa365 splits — **Atomic-Seen**, **Composite-Seen**, and **Composite-Unseen** — and report average task success rate (in %) for each. This accounts for a total of 50 target tasks being evaluated. These evaluation splits and target datasets are explained in further detail in our [documentation](https://robocasa.ai/docs/build/html/datasets/datasets_overview.html).

To add your results, export a JSON file in the format below and open a pull request that adds it to the `submissions/` directory. The results will be displayed on our main [website](https://robocasa.ai/leaderboard.html).

> [!NOTE]
> For models that cannot be released open-source (`"open_source": "no"`), you must grant the RoboCasa team private access to your model checkpoint and evaluation code so we can verify results on our benchmark. You can give private access to your model checkpoint on Hugging Face and evaluation code on GitHub by granting access to @sepnasiriany.

## Submission template

Each submission is a single JSON file added to `submissions/` with this structure: :

```json
{
  "model_name": "<string>",
  "submitter": "<team or organization name>",
  "date": "<YYYY-MM-DD, e.g. '2026-04-02'>",
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

### Model icon (optional)

To show a logo next to your model on the leaderboard, add a square image (256px or larger; `.png` or `.svg`) to the `icons/` folder in the same pull request, named after your submission JSON file. For example, `submissions/my-model_2026_09_01.json` pairs with `icons/my-model_2026_09_01.png`. Without an icon, the leaderboard shows a letter tile with your model's initial.

The optional `"accent"` field (a hex color such as `"#76b900"`, typically your logo's primary color) sets the hover highlight color of your model's name on the leaderboard.

Here’s a sample JSON: [gr00t_n1.5_2026_05_19.json](https://github.com/robocasa-benchmark/leaderboard/blob/main/submissions/gr00t_n1.5_2026_05_19.json)
