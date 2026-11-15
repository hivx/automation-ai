Feature: <ID>
Stage: plan
Author-agent: tech-lead
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# Tasks <ID>

Each task is one vertical slice: one behavior with its tests, ≤ 5 files, about 15–30 minutes of work; ≤ 4 lines per task. Only task lines, ticks and one `baseline:` line live here (no progress logs). Two tasks that share a file depend on each other. Append `BLOCKED: <reason>` to the end of the line when a task is blocked.

- [ ] T1 — <title> — files: <path/to/file, ...> — test: <test file> — depends: —
- [ ] T2 — <title> — files: <...> — test: <...> — depends: T1
