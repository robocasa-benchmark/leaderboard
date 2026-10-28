## Submission details

- Model name: Awomo-0.5I
- Submitter: Awomo-WAM Team
- Date evaluated: 10/09/2026
- RoboCasa version: 1.0.1
- Atomic-Seen success: 86.5
- Composite-Seen success: 58.8
- Composite-Unseen success: 45.2
- Code URL: [https://github.com/Awomo-WestlakeDI/Awomo-0.5/tree/main/eval_robocasa365](https://github.com/Awomo-WestlakeDI/Awomo-0.5/tree/main/eval_robocasa365)
- Checkpoint URL: [https://huggingface.co/Auwomo/Awomo-0.5I-RoboCasa365](https://huggingface.co/Auwomo/Awomo-0.5I-RoboCasa365)
- Commit hash: 1145c18afd13a3876c6740f098bd734f5e35617a
- Open Source: yes
- PR: [https://github.com/robocasa-benchmark/leaderboard/pull/27](https://github.com/robocasa-benchmark/leaderboard/pull/27)
- Batch size: 512
- Number of training steps: 60,000
- Notes: Awomo-0.5I (Awomo-0.5-Image) integrates a LoRA-adapted Qwen3-VL conditioner with a shared world-action DiT. The policy combines task instructions, current and historical visual observations, and proprioception to jointly predict future-image latents and 16-step action sequences. Historical observations provide both vision-language context and visual memory. Built on pretrained foundation models, the model underwent supervised fine-tuning (SFT) using only RoboCasa365 Human300, with a global batch size of 512 for 60,000 steps. No Target50 data, target scenes, or target assets were used in training. Evaluation used RoboCasa 1.0.1, split=pretrain, replan=16, 16 denoising steps, and 30 trials per task. Results contain 966 successes over 1,500 episodes: Atomic-Seen 467/540, Composite-Seen 282/480, and Composite-Unseen 217/480. Code, checkpoint, and reproduction instructions are publicly available. A technical report is planned for October 2026.
