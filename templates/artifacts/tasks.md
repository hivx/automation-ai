Feature: <ID>
Stage: plan
Author-agent: tech-lead
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Tasks <ID>

Each task is one vertical slice: 1–4 criteria end to end, roughly 100–400 changed lines with their tests, ≤ 6 files; at most 6 tasks at size M, 12 at size L; ≤ 4 lines per task. Append `[risk]` to a task touching authorization or secrets, a migration or schema, money or data deletion, a contract used outside the feature, or shared state: every task is tested and reviewed in its round's checkpoint; a task that depends on a `[risk]` task waits for that review. Only task lines, ticks and one `baseline:` line live here (no progress logs). Two tasks that share a file depend on each other. Append `BLOCKED: <reason>` to the end of the line when a task is blocked.

- [ ] T1 — <title> — files: <path/to/file, ...> — test: <test file> — depends: —
- [ ] T2 — <title> — files: <...> — test: <...> — depends: T1 [risk]
