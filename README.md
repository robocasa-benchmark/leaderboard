# RoboCasa Benchmark Leaderboard 🏆

This repository hosts the official RoboCasa365 leaderboard. It tracks multi-task policy learning performance on RoboCasa365 and is open to community submissions via pull requests.

We analyze multi-task learning through three RoboCasa365 splits — **Atomic-Seen**, **Composite-Seen**, and **Composite-Unseen** — and report average task success rate (in %) for each. This accounts for a total of 50 target tasks being evaluated. These evaluation splits and target datasets are explained in further detail in our [documentation](https://robocasa.ai/docs/build/html/datasets/datasets_overview.html).

There are two submission types, evaluated on the same tasks and splits and ranked together on one [leaderboard](https://robocasa.ai/leaderboard.html):

| Submission | What it ranks | Submission folder |
|---|---|---|
| **Standard** | Policies you train | `submissions/standard/` |
| **Agentic** | A new model or a novel agentic harness built around a base policy | `submissions/agentic/` |

To add your results, export a JSON file in the format for your submission type (below) and open a pull request that adds it to that type's submission folder. PRs are labeled `standard` or `agentic` automatically based on the folder. Please give us up to 10 days to evaluate your model upon submission. After verification, results will be displayed on our main [website](https://robocasa.ai/leaderboard.html).

## Standard submissions

> [!NOTE]
> For models that cannot be released open-source (`"open_source": "no"`), you must grant the RoboCasa team private access to your model checkpoint and evaluation code so we can verify results on our benchmark. You can give private access to your model checkpoint on Hugging Face and evaluation code on GitHub by granting access to @sepnasiriany. We will only accept closed source models for legitimate proprietary reasons and we expect your model to eventually be open sourced.

### Submission requirements

1. **Novel model.** A submission must be a distinct model: a new architecture, training recipe, or data approach. A short fine-tune, LoRA adapter, or minor post-training run on an existing entry is not a new submission.
2. **Novelty in the model or the data.** A new architecture qualifies, and so does an established architecture trained on a new pretraining dataset or data mixture. Side outputs the policy never uses at test time do not count as the novelty.
3. **Show a real improvement.** If you build on someone else's base model, demonstrate a measurable success-rate gain from your contribution. A delta within noise of the base is the same model.
4. **Attribute your base.** If your submission wraps or extends another team's checkpoint, say so clearly: which parts are frozen, which you trained, and how much data you used.
5. **Paper or writeup.** Publish a paper or commit to a release timeline. Unexplained leaderboard numbers aren't reproducible science. We require an arXiv abstract link for the paper.

### Submission template

Each submission is a single JSON file added to `submissions/standard/` with this structure:

```json
{
  "model_name": "<string>",
  "submitter": "<team or organization name>",
  "model_type": "<string> (ie. VLA)",
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
  "training_config": {
    "batch_size": "<integer>",
    "num_training_steps": "<integer>"
  },
  "notes": "<optional free text>"
}
```

> [!NOTE]
> For any field where the information is unavailable or not applicable, write `"N/A"`.
> `model_type` is one of `VLA` (vision-language-action model), `WAM` (world action model that jointly predicts future frames and actions), `VLA + WM` (a VLA paired with a separate world model), `Visuomotor` (no language or VLM backbone), or `Other`.
> The current default `robocasa_version` is `1.0.1` until a new update is announced.
> `code_url`, `commit_hash`, and `checkpoint_url` are required when `"open_source": "yes"`; with `"open_source": "no"` they may be omitted.

Here’s a sample JSON: [gr00t_n1.5_2026_05_19.json](https://github.com/robocasa-benchmark/leaderboard/blob/main/submissions/standard/gr00t_n1.5_2026_05_19.json)

## Agentic submissions

Agentic submissions go in `submissions/agentic/`. Please start the PR title with `[AGENTIC]`.

### Submission requirements

1. **Novelty.** Either a new model or a novel agentic harness framework. Using an existing model with an existing coding agent for basic steering does not qualify.
2. **Base policy.** Name, HF repo and commit, and license. No weight edits.
3. **Scope.** Policy observations only (no privileged simulator state). No ground-truth success signal during an episode. Cross-episode memory must be disclosed.
4. **Reproducibility.** Public repo, pinned dependencies, and one-prompt setup. For closed-API planners: provider, model ID, settings, and a test key with enough quota for one full eval. For closed-source code or checkpoints, grant access on GitHub to [@Abhiram824](https://github.com/Abhiram824) and on Hugging Face to [Abhi03](https://huggingface.co/Abhi03).
5. **Verification.** An arXiv or preprint link. We re-run the full eval, and our numbers are the ones posted.

### Submission template

Each submission is a single JSON file added to `submissions/agentic/` with this structure:

```json
{
  "model_name": "<string>",
  "submitter": "<team or organization name>",
  "model_type": "<type of the base policy: VLA | WAM | VLA + WM | Visuomotor | Other>",
  "date": "<YYYY-MM-DD>",
  "robocasa_version": "<string, default '1.0.1'>",
  "atomic_seen_success": <number 0–100>,
  "composite_seen_success": <number 0–100>,
  "composite_unseen_success": <number 0–100>,
  "base_policy": "<name of the policy the agent runs>",
  "code_url": "<URL>",
  "commit_hash": "<git commit hash>",
  "checkpoint_url": "<URL of the policy checkpoint the agent runs>",
  "paper_link": "<arXiv or preprint URL>",
  "open_source": "yes",
  "training_config": {
    "batch_size": "<integer>",
    "num_training_steps": "<integer>"
  },
  "notes": "<base policy license, planner provider and model ID if closed-API, and whether cross-episode memory is used>"
}
```

> [!NOTE]
> `checkpoint_url` is required when `"open_source": "yes"`. `training_config` is optional; include it if you trained or finetuned a model.
> `model_type` uses the same options as standard submissions and describes the base policy; the website shows agentic entries as `Agent + <model_type>`.

### Private information

Everything in the pull request is public. Never put API keys or other credentials in your PR. After opening the PR, email [robocasa@googlegroups.com](mailto:robocasa@googlegroups.com) with:

- A link to your PR.
- Your API key for any closed-API planner, with enough quota for one full eval.
- For closed-source code or checkpoints, confirmation that access was granted on GitHub to [@Abhiram824](https://github.com/Abhiram824) and on Hugging Face to [Abhi03](https://huggingface.co/Abhi03).

## Model icon

To show a logo next to your model on the leaderboard, add a square image (256px or larger; `.png` or `.svg`) to the `icons/` folder in the same pull request, named after your submission JSON file. For example, `submissions/standard/my-model_2026_09_01.json` pairs with `icons/my-model_2026_09_01.png`. Without an icon, the leaderboard shows a letter tile with your model's initial. This works the same for both submission types.

## Questions

If you have any questions about the benchmark or the submission process, reach out at [robocasa@googlegroups.com](mailto:robocasa@googlegroups.com).
