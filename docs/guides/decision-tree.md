<!-- GENERATED — do not edit; run scripts/gen-guides.py -->
# Which playbook

team-leader chooses at `/team:intake`: read from the top, the first matching row wins; size comes after.
Source: `workflows/README.md`. Each playbook's skill chain, gates and stop points live in the playbook file.

| Signal | Playbook | Default size |
|---|---|---|
| Repo has code the team has never worked on (no `.team/profile.json` yet) | [takeover](../../workflows/takeover.md) | — |
| Empty repo, building a system from scratch | [new-project](../../workflows/new-project.md) | L |
| Production is broken and needs a fix now | [hotfix](../../workflows/hotfix.md) | S |
| Trivial change: a text, a config value, one obvious line; ≤ 2 files; no schema/API/security change | [quick](../../workflows/quick.md) | S |
| Behavior differs from the spec, reproducible, not urgent | [bug-fix](../../workflows/bug-fix.md) | S |
| CI pipeline is red or a CI workflow needs fixing | [ci-fix](../../workflows/ci-fix.md) | S |
| Change to the requirements of a feature that passed G1 | [change-request](../../workflows/change-request.md) | M |
| Connecting to an external API/service | [integration](../../workflows/integration.md) | M |
| Converting or loading data between schemas/systems | [data-migration](../../workflows/data-migration.md) | M |
| Upgrading a library, framework or runtime version | [dependency-upgrade](../../workflows/dependency-upgrade.md) | M |
| Cleaning up code without changing behavior | [refactor](../../workflows/refactor.md) | M |
| Technical docs or README only | [docs-only](../../workflows/docs-only.md) | S |
| Docs for clients/end users | [client-docs](../../workflows/client-docs.md) | S |
| Unknown whether it can be done, needs a trial | [spike](../../workflows/spike.md) | S |
| Packaging an accepted feature and shipping it to an environment | [release](../../workflows/release.md) | — |
| Looking back at how the team works | [retro](../../workflows/retro.md) | — |
| New behavior for a running system (every other case) | [new-feature](../../workflows/new-feature.md) | from intake |

Unattended runs: `workflows/batch/` (build-all-tasks, verify-all, weekly-retro, clean-sweep).
