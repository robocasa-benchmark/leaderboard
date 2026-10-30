## Submission details

- Model name: Meituan-Robotics-0
- Submitter: Meituan Robotics
- Model type: VLA
- Date evaluated: 10/24/2026
- RoboCasa version: 1.0.1
- Atomic-Seen success: 77.3
- Composite-Seen success: 57.8
- Composite-Unseen success: 27.1
- Open Source: no
- PR: [https://github.com/robocasa-benchmark/leaderboard/pull/37](https://github.com/robocasa-benchmark/leaderboard/pull/37)
- Batch size: 256
- Number of training steps: 200,000
- Notes: Author-run results for the 200,000-step Meituan-Robotics-0 checkpoint, pending official verification. Initialized from a pretrained MR0 policy. RoboCasa adaptation used pretrain_human300 (300 tasks, 100 human demonstrations per task), four RGB/state observations at offsets [-6,-4,-2,0], 640x320 images, a 50-step action horizon, and mode-balanced action loss. Both the VLM and action head were fine-tuned; effective batch size was 256. Evaluated on RoboCasa 1.0.1 in pretraining kitchens with the official target50 protocol: 50 tasks x 50 episodes, execution horizon 16, and 10 denoising steps. Atomic-Seen: 711/900 (79.00%); Composite-Seen: 432/800 (54.00%); Composite-Unseen: 218/800 (27.25%); overall: 1361/2500 (54.44%). Private evaluation-code and checkpoint access invitations have been issued to sepnasiriany. The paper/writeup is planned for November 2026; the arXiv link is not yet available. The model is temporarily closed-source while a related component is prepared for release. Code and checkpoint will be open-sourced after that component is released.
