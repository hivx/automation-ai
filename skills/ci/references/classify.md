# Classifying a red CI run (STD-CI-4)

| Kind | Signs in the log | Evidence needed before concluding | Action | Do not |
|---|---|---|---|---|
| code | a failing assertion, an exception in project code, a type/lint error in a file just changed | run the matching `cmd.*` slot locally on the same SHA → same failure | hand back to team-leader: `/team:intake --type bug` | fix the code, edit the test |
| flaky test | timeouts, ordering, a busy network port; the same test red one time and green the next | same SHA: red → one rerun (`gh run rerun <id> --failed`) → green | a `debt.md` row (test name, both run-ids, count); tell team-leader | disable the test, add retries to the test, rerun many times |
| environment | runner out of disk, API quota, DNS, an external service down | the diff changes nothing related; the failure is outside the project's steps | wait/rerun once; if it recurs → change the runner/setup step on a separate PR | change code |
| configuration | wrong YAML, wrong action version, `ci.setup` out of line with the profile, a missing environment variable | read the workflow file + profile; point to the wrong line | fix the workflow on `team/ci-<slug>` | loosen a check step |
| dependency | a package fails to resolve, the lockfile disagrees with the manifest, a new upstream release is broken | compare lockfile with manifest; the upstream changelog | `cmd.install` on a separate branch; caused by a new release → playbook dependency-upgrade | hand-edit the lockfile |

## Order for reading the log
1. Which job went red first (`--json jobs`), and which step.
2. The first error line in that step (skip the trailing "exit code 1", "Process completed" lines).
3. The SHA and branch; does it match an earlier red run on the base branch (`gh run list --branch <base> --limit 5`)?

## Failures already on the base branch
The base branch is red with the same failure too → it is not caused by the PR. State "already red on `<base>` since run <id>"; the kind is still one of the five above; the PR under review is not blocked by this failure, but the human must be told.
