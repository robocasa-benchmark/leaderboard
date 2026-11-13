## Submission details

- Model name: HexaShell 1.5
- Submitter: HexaFuture
- Model type: Other
- Date evaluated: 10/31/2026
- RoboCasa version: 1.0.1
- Atomic-Seen success: 91.1
- Composite-Seen success: 85.0
- Composite-Unseen success: 80.0
- Code URL: [https://github.com/HexaFuture/HexaShell](https://github.com/HexaFuture/HexaShell)
- Commit hash: 10e11ef3ee83258b157c23f688d64c139933a221
- Paper link: [https://arxiv.org/abs/2610.23479](https://arxiv.org/abs/2610.23479)
- Open Source: yes
- PR: [https://github.com/robocasa-benchmark/leaderboard/pull/39](https://github.com/robocasa-benchmark/leaderboard/pull/39)
- Notes: Author-run results, pending official verification. Not the official target50 protocol: RoboCasa 1.0.1, the 50 target tasks in pretraining kitchens, on the pretrain50 split taken from HexaShell-Casa (50 fixed pretraining kitchens, seed s in kitchen s % 50), test seeds 20-49, 30 episodes per task, 1500 in all. Atomic-Seen 492/540 (91.1%), Composite-Seen 408/480 (85.0%), Composite-Unseen 384/480 (80.0%), weighted overall 85.6. The official target50 run (50 tasks x 50 episodes) has not been done yet. Planner: gpt-6-astra (closed API), reasoning_effort xhigh, max_tokens 8192, streamed, through an OpenAI-compatible chat endpoint. The endpoint and a test key will be sent by email. With the same code at reasoning_effort high (the repository default): 88.5 / 79.8 / 76.7 (1229/1500). Observations: the three RGB-D cameras (left, right, wrist, 512x512), their camera parameters, proprioception, the instruction and the step budget. The robot's own pixels are masked using the renderer's segmentation of the robot's own parts. No other simulator state is used. Motions are planned by the harness (IK) and executed at 20 Hz with the official 12-dim action. An episode ends at the first step at which RoboCasa's _check_success() holds, or at the official horizon. The model gets no further request after that, so it never acts on the verdict. There are also limits of 40 replies for an atomic task, 100 for a composite one, and 2 h per episode. Cross-episode memory: per-task skill notes, fixed text, one per task for all 50 tasks. They were written from our own runs on pretrain50 seeds 0-9 and checked on seeds 10-19. Because there is a note for every task, the Composite-Unseen tasks are not zero-shot for this agent. Nothing is learned or updated during evaluation. The code and a writeup will be open-sourced at the code_url within two weeks.
