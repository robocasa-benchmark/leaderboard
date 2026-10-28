## Submission details

- Model name: LY-GWM-RoboCasa
- Submitter: SEIN-LYGWM
- Model type: VLA + WM
- Date evaluated: 09/24/2026
- RoboCasa version: 1.0.1
- Atomic-Seen success: 48.3
- Composite-Seen success: 16.3
- Composite-Unseen success: 3.1
- Code URL: [https://github.com/SEIN-LYGWM/LY-GWM-RoboCasa-Human300-eval](https://github.com/SEIN-LYGWM/LY-GWM-RoboCasa-Human300-eval)
- Checkpoint URL: [https://huggingface.co/lygwm-review/LY-GWM-RoboCasa-Human300/tree/180883d9af9ee02edc3c53fe20babdc7658d1127](https://huggingface.co/lygwm-review/LY-GWM-RoboCasa-Human300/tree/180883d9af9ee02edc3c53fe20babdc7658d1127)
- Commit hash: 79b247c854df116614d9ec5db29406c329a18603
- Paper link: [https://arxiv.org/abs/2610.23274](https://arxiv.org/abs/2610.23274)
- Open Source: yes
- PR: [https://github.com/robocasa-benchmark/leaderboard/pull/19](https://github.com/robocasa-benchmark/leaderboard/pull/19)
- Batch size: 128
- Number of training steps: 120,000
- Notes: S42: RoboCasa 1.0.1, split=pretrain, 50 tasks x 50 episodes, 207/2500 successes (8.28%). R5 fine-tuned GR00T-N1.5 generates four candidates; frozen W5 LY-GWM predicts future features/state; a separate S38 binary state-reward head selects the maximum logit. The scorer is not a goal-conditioned value function. The previous 200/2500 submission is superseded by this S42 submission and is not evidence of LY-GWM-based action selection; the current submission uses S42's 207/2500 result and its corresponding public code, weights and evaluation records. S42 passed revised INTERNAL acceptance: after the run, nonzero action-bound counts became diagnostic-only; original zero-bound acceptance failed. 1822 affected episodes include 149 successful episodes; all 2500 remain in the denominator. No new rollouts were performed by the revised collector. Historical S31 was 181/2500 (7.24%); the +1.04 percentage-point difference is descriptive, without a causal or significance claim; S31 contemporaneous weight-shard hashes are unavailable. Historical full raw action traces are not bundled; recorded audit reports and trace hashes are supplied. New-machine reviewer entrypoints have CPU/static checks only, not a completed GPU reproduction. The local public-checkpoint versus official-reference performance gap remains unresolved. Source and inference weights are public subject to preserved component terms. Official acceptance is for the maintainers to determine.
