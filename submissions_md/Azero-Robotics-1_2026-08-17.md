## Submission details

- Model name: Azero-Robotics-1
- Submitter: [GitHub: yuxin101](https://github.com/robocasa-benchmark/leaderboard/pull/11)
- Date evaluated: 08/17/2026
- Submission source: external
- RoboCasa version: 1.0.1
- Atomic-Seen success: 30.3
- Composite-Seen success: 3.8
- Composite-Unseen success: 1.6
- Commit hash: 82ccf2b164ed604185599e490c968048ec5b4ee2
- Open Source: no
- PR: [https://github.com/robocasa-benchmark/leaderboard/pull/11](https://github.com/robocasa-benchmark/leaderboard/pull/11)
- W&B: [https://wandb.ai/yuxin-soundai-soundai/robocasa365/runs/7711y2ka](https://wandb.ai/yuxin-soundai-soundai/robocasa365/runs/7711y2ka)
- Batch size: 128
- Number of training steps: 120,000
- Notes: Azero-Robotics-1 is initialized from the publicly released NVIDIA GR00T-N1.5-3B checkpoint and retrained under the official RoboCasa365 multi-task learning protocol using pretrain_human300. Results are from a completed 50-task formal eval run. The reported training_config.batch_size is the global batch size (128), corresponding to a per-GPU batch size of 16 over 8 GPUs. Code and checkpoint are hosted as linked above, and private verification access can be granted to the RoboCasa team if needed.
