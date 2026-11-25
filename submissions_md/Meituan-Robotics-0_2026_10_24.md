## Submission details

- Model name: Meituan-Robotics-0
- Submitter: Meituan Robotics
- Model type: VLA
- Date evaluated: 10/24/2026
- RoboCasa version: 1.0.1
- Atomic-Seen success: 77.3
- Composite-Seen success: 57.8
- Composite-Unseen success: 27.1
- Code URL: [https://github.com/linglingxiansen/robocasa365-eval](https://github.com/linglingxiansen/robocasa365-eval)
- Checkpoint URL: [https://huggingface.co/MeituanRobotics/Meituan-Robotics-0-RoboCasa365/tree/8a3f69a65600c4ba0fbe340ba934438140f44d2d](https://huggingface.co/MeituanRobotics/Meituan-Robotics-0-RoboCasa365/tree/8a3f69a65600c4ba0fbe340ba934438140f44d2d)
- Commit hash: 380232d22cbf94da7f33e58c172b9a4d10c33706
- Paper link: [https://arxiv.org/abs/2611.08577](https://arxiv.org/abs/2611.08577)
- Open Source: yes
- PR: [https://github.com/robocasa-benchmark/leaderboard/pull/37](https://github.com/robocasa-benchmark/leaderboard/pull/37)
- Batch size: 256
- Number of training steps: 200,000
- Notes: The published 200,000-step checkpoint is the checkpoint reproduced by the RoboCasa team in PR #37. Initialized from a pretrained MR0 policy. RoboCasa adaptation used pretrain_human300 (300 tasks, 100 human demonstrations per task), four RGB/state observations at offsets [-6,-4,-2,0], 640x320 images, a 50-step action horizon, and mode-balanced action loss. Both the VLM and action head were fine-tuned with an effective batch size of 256. Evaluation used RoboCasa 1.0.1 in pretraining kitchens with the official target50 protocol, 50 episodes per task, an execution horizon of 16, and 10 denoising steps. The public Meituan-Robotics-0 project links to the matching RoboCasa365 evaluation code.
