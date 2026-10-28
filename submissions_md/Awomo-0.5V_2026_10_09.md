## Submission details

- Model name: Awomo-0.5V
- Model type: WAM
- Submitter: Awomo-WAM Team
- Date evaluated: 10/09/2026
- RoboCasa version: 1.0.1
- Atomic-Seen success: 85.0
- Composite-Seen success: 60.4
- Composite-Unseen success: 39.4
- Code URL: [https://github.com/Awomo-WestlakeDI/Awomo-0.5/tree/main/eval_robocasa365](https://github.com/Awomo-WestlakeDI/Awomo-0.5/tree/main/eval_robocasa365)
- Checkpoint URL: [https://huggingface.co/Auwomo/Awomo-0.5V-RoboCasa365](https://huggingface.co/Auwomo/Awomo-0.5V-RoboCasa365)
- Commit hash: 1145c18afd13a3876c6740f098bd734f5e35617a
- Open Source: yes
- PR: [https://github.com/robocasa-benchmark/leaderboard/pull/28](https://github.com/robocasa-benchmark/leaderboard/pull/28)
- Batch size: 512
- Number of training steps: 40,000
- Notes: Awomo-0.5V (Awomo-0.5-Video) is a video-based world-action model built on pretrained Wan2.2. It combines task instructions, video observations, and proprioception to jointly predict future video and action sequences, using a causal transformer with cached visual context. Supervised fine-tuning (SFT) used only RoboCasa365 Human300, with a global batch size of 512 for 40,000 steps. No Target50 data, target scenes, or target assets were used in training. Evaluation used RoboCasa 1.0.1, split=pretrain, replan=16, 16 denoising steps, and 30 trials per task. Results contain 938 successes over 1,500 episodes: Atomic-Seen 459/540, Composite-Seen 290/480, and Composite-Unseen 189/480. Code, checkpoint, and reproduction instructions are publicly available. A technical report is planned for October 2026.
