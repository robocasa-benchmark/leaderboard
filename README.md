# RoboCasa Benchmark Leaderboard 🏆

This repository hosts the official RoboCasa365 leaderboard. It tracks multi-task policy learning performance on RoboCasa365 and is open to community submissions via pull requests.

We analyze multi-task learning through three RoboCasa365 splits — **Atomic-Seen**, **Composite-Seen**, and **Composite-Unseen** — and report average task success rate (in %) for each. This accounts for a total of 50 target tasks being evaluated. These evaluation splits and target datasets are explained in further detail in our [documentation](https://robocasa.ai/docs/build/html/datasets/datasets_overview.html).

To add your results, export a JSON file in the format below and open a pull request that adds it to the `submissions/` directory. The results will be displayed on our main [website](https://robocasa.ai/leaderboard.html).

> [!NOTE]
> For models that cannot be released open-source (`"open_source": "no"`), you must grant the RoboCasa team private access to your model checkpoint and evaluation code so we can verify results on our benchmark. You can give private access to your model checkpoint on Hugging Face and evaluation code on GitHub by granting access to @sepnasiriany. We will only accept closed source models for legitimate proprietary reasons and we expect your model to eventually be open sourced.

## Submission requirements

1. **Novel model.** A submission must be a distinct model: a new architecture, training recipe, or data approach. A short fine-tune, LoRA adapter, or minor post-training run on an existing entry is not a new submission.
2. **Novelty must show up at inference.** Contributions that only run during training (regularizers, auxiliary losses) or that compute side outputs the policy never uses do not count. The mechanism you claim credit for must be part of what the model does at test time.
3. **Show a real improvement.** If you build on someone else's base model, demonstrate a measurable success-rate gain from your contribution. A delta within noise of the base is the same model.
4. **Attribute your base.** If your submission wraps or extends another team's checkpoint, say so clearly: which parts are frozen, which you trained, and how much data you used.
5. **Paper or writeup.** Publish a paper, tech report, or blog post, or commit to a release timeline. Unexplained leaderboard numbers aren't reproducible science.

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
> `code_url`, `commit_hash`, and `checkpoint_url` are required when `"open_source": "yes"`; with `"open_source": "no"` they may be omitted.

Here’s a sample JSON: [gr00t_n1.5_2026_05_19.json](https://github.com/robocasa-benchmark/leaderboard/blob/main/submissions/gr00t_n1.5_2026_05_19.json)

### Model icon (optional)

To show a logo next to your model on the leaderboard, add a square image (256px or larger; `.png` or `.svg`) to the `icons/` folder in the same pull request, named after your submission JSON file. For example, `submissions/my-model_2026_09_01.json` pairs with `icons/my-model_2026_09_01.png`. Without an icon, the leaderboard shows a letter tile with your model's initial.

When your submission includes an icon, the leaderboard derives a matching hover highlight color for your model's name from the logo automatically. To pick it yourself, set the optional `"accent"` field in your submission JSON (a hex color such as `"#76b900"`); an explicit accent always wins.
