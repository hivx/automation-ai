# Playbooks — pick by signal

team-leader uses this table in `/team:intake`: look at the KIND of work first (first matching row wins, top to bottom), and only then set size S/M/L. `scripts/gen-guides.py` reads the table between the two markers below to generate `docs/guides/decision-tree.md`.

<!-- playbook-table:start -->
| Signal | Playbook | Default size |
|---|---|---|
| Repo has code the team has never worked on (no `.team/profile.json` yet) | [takeover](takeover.md) | — |
| Empty repo, building a system from scratch | [new-project](new-project.md) | L |
| Production is broken and needs a fix now | [hotfix](hotfix.md) | S |
| Trivial change: a text, a config value, one obvious line; ≤ 2 files; no schema/API/security change | [quick](quick.md) | S |
| Behavior differs from the spec, reproducible, not urgent | [bug-fix](bug-fix.md) | S |
| CI pipeline is red or a CI workflow needs fixing | [ci-fix](ci-fix.md) | S |
| Change to the requirements of a feature that passed G1 | [change-request](change-request.md) | M |
| Connecting to an external API/service | [integration](integration.md) | M |
| Converting or loading data between schemas/systems | [data-migration](data-migration.md) | M |
| Upgrading a library, framework or runtime version | [dependency-upgrade](dependency-upgrade.md) | M |
| Cleaning up code without changing behavior | [refactor](refactor.md) | M |
| Technical docs or README only | [docs-only](docs-only.md) | S |
| Docs for clients/end users | [client-docs](client-docs.md) | S |
| Unknown whether it can be done, needs a trial | [spike](spike.md) | S |
| Packaging an accepted feature and shipping it to an environment | [release](release.md) | — |
| Looking back at how the team works | [retro](retro.md) | — |
| New behavior for a running system (every other case) | [new-feature](new-feature.md) | from intake |
<!-- playbook-table:end -->

## Right-size the team (ADJ-36)
Call only the roles the work needs. A question, an explanation or a status check is answered by team-leader directly: no intake, no ID, no agent (at most Explore, one call per question, in one message). quick = 1 dev. Size S = tech-lead with 1 dev + 1 reviewer; acceptance runs inside build (no qa) and there is no As-Built. research, architect, design and plan run only when their signal is there (size, playbook, open technical questions).

## Sizing
- **S**: the diff fits in one sentence; ≤ 3 files; no schema/API change.
- **M**: one module; data or API change; 1–5 person-days.
- **L**: several modules; new NFRs; > 5 person-days.
The human forces a size with `--size` or a `team:size:*` label.

## Unattended runs (`batch/`)
| File | Use when |
|---|---|
| [batch/build-all-tasks.md](batch/build-all-tasks.md) | Plan passed G3; build every task overnight |
| [batch/verify-all.md](batch/verify-all.md) | Re-run acceptance for every feature in the built state |
| [batch/weekly-retro.md](batch/weekly-retro.md) | Recurring weekly retro |
| [batch/clean-sweep.md](batch/clean-sweep.md) | Clean up one kind of debt from `debt.md` |
