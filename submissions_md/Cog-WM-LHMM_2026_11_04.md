## Submission details

- Model name: Cog-WM LHMM
- Submitter: lidingebkernel-bit
- Model type: VLA
- Date evaluated: 11/04/2026
- RoboCasa version: 1.0.1
- Atomic-Seen success: 87.3
- Composite-Seen success: 65.38
- Composite-Unseen success: 40.0
- Commit hash: 1f7abf6c7b919111b1b56dbab73a473d9be9d640
- Open Source: no
- PR: [https://github.com/robocasa-benchmark/leaderboard/pull/41](https://github.com/robocasa-benchmark/leaderboard/pull/41)
- Batch size: 512
- Number of training steps: 56,849
- Notes: Agentic system: frozen Cog-WM LHMM policy with the Cog-Harness planner and memory system; 1629/2500 successes (65.16%) on RoboCasa365 target50, pretrain scenes, native horizons and scoring. Base policy license: Apache-2.0; HF revision: 54c6b3062791b645e98f3c3ab684766f46dcd80e. Planner: OpenAI gpt-6-astra, medium reasoning, Codex CLI 0.153.4. Disclosed frozen task-scoped experience is reused across episodes; working memory resets each episode with no writeback. Live task-progress predicates and object ground-truth coordinates are excluded; native depth and terminal-only feedback are retained. Reviewer access, planner quota and paper link remain to be finalized.
