<!-- GENERATED — do not edit; run scripts/gen-handbook-short.py -->
# STD-short — short version of handbook/STD.md

## Level 2–3 rules (level in parentheses)
- STD-STRUCT-1 (3) Create new files only under the directories in `structure.allowed_new_file_roots`.
- STD-STRUCT-2 (2) Put source code in `structure.src` and tests in `structure.tests` (or next to the code when the value is `colocated`).
- STD-STRUCT-3 (2) Follow the existing module layout; do not create a parallel directory or layer for the same purpose.
- STD-STRUCT-4 (3) Do not edit inside `.git/`, build-output directories or vendored directories.
- STD-STRUCT-5 (2) Keep one main responsibility per file; split a file when it carries two unrelated purposes.
- STD-STRUCT-6 (3) Run the structure check before finishing a build task.
- STD-STRUCT-7 (2) Put utility scripts in `structure.scripts` and configuration files in the `structure.config` locations.
- STD-NAME-1 (2) Name files according to `naming.file`.
- STD-NAME-2 (2) Name classes/types, functions and constants according to `naming.class`, `naming.function`, `naming.constant`.
- STD-NAME-3 (3) Name test files according to `naming.test_file`.
- STD-NAME-4 (3) Name branches `team/<ID>-<slug>`.
- STD-NAME-5 (3) Write commit messages as `type(scope): description (<ID>)`.
- STD-NAME-6 (2) Use names that state the business meaning; no abbreviations outside `docs/team/glossary.md`.
- STD-NAME-7 (2) Keep one naming convention within a module; do not mix two conventions.
- STD-STYLE-1 (3) Format every edited file with the profile's formatter.
- STD-STYLE-2 (3) Leave `cmd.lint` clean before committing.
- STD-STYLE-3 (3) Leave `cmd.typecheck` clean when the profile has that slot.
- STD-STYLE-4 (2) Follow the existing style of the file being edited; no mass style changes in a feature PR.
- STD-STYLE-5 (2) Leave no dead code, commented-out code or debug logging in the diff.
- STD-STYLE-7 (2) Do not disable a lint/typecheck rule in place without a reason written right next to it.
- STD-DESIGN-1 (2) Edit only within the task's touchpoints; if an edit outside them is needed, stop and report `DESIGN_CONFLICT`.
- STD-DESIGN-2 (2) Follow the approved architecture and ADRs; changing the architecture requires a new ADR.
- STD-DESIGN-3 (2) Keep public API contracts backward compatible; a breaking change needs a new version and a migration guide.
- STD-DESIGN-4 (2) Reuse existing logic instead of duplicating it.
- STD-DESIGN-5 (2) Choose the simplest solution that meets the spec; add no features or extension points that were not requested.
- STD-DESIGN-6 (2) Keep dependencies between modules one-directional; create no dependency cycles.
- STD-DESIGN-7 (2) Read environment-dependent values from configuration; do not hard-code them.
- STD-TEST-1 (2) Write a failing test before changing code (mandatory for bug fixes) and paste the red output.
- STD-TEST-2 (2) Cover every acceptance criterion with at least one automated test or one check step that has output.
- STD-TEST-3 (3) Run `cmd.test_one` for changed tests before finishing a task and `cmd.test` before merging.
- STD-TEST-4 (3) Do not use skip, xfail or only to get green — a violation is a blocker.
- STD-TEST-5 (2) Do not change an assertion to match wrong behavior; change a test only when the spec changes.
- STD-TEST-6 (2) Write tests that are independent and repeatable: no dependence on run order, wall-clock time or external networks.
- STD-TEST-7 (2) Record a flaky test in `docs/team/debt.md` and fix it; do not disable it.
- STD-TEST-8 (2) Test edge cases and error paths, not only the happy path.
- STD-ERR-1 (2) Do not swallow errors; every catch must handle the error, add context and rethrow, or state clearly why it is ignored.
- STD-ERR-2 (2) Validate input at system boundaries (API, form, file, message).
- STD-ERR-3 (2) Do not expose internal details (stack traces, queries, paths) in error messages shown to users.
- STD-ERR-4 (2) Log errors with enough context to trace them (request ID, entity) and log no sensitive data.
- STD-ERR-5 (2) Call external services with a timeout, a bounded number of retries and idempotent operations when retrying.
- STD-ERR-6 (2) Fail immediately at startup when configuration is missing or invalid; do not continue on implicit defaults.
- STD-ERR-7 (2) Run multi-step data operations in a transaction or with a compensating step.
- STD-GIT-1 (2) One task, one small PR; when the task is merged into the feature branch, the task is a separate commit that can be reviewed on its own.
- STD-GIT-2 (2) Keep commits small and atomic; every commit builds and passes the tests.
- STD-GIT-3 (3) Push only `team/*` branches.
- STD-GIT-4 (3) Do not force-push and do not rewrite pushed history.
- STD-GIT-5 (2) Do not commit generated files, build output or machine-specific files; list them in the ignore file.
- STD-GIT-6 (2) Update from `config.base_branch` before opening a PR; resolve conflicts without losing other people's changes.
- STD-GIT-7 (2) Write a PR description covering: why, what changed, how it was verified, the feature/task ID.
- STD-GIT-8 (3) No AI attribution in commits or PRs: no `Co-Authored-By:` trailer, no "Generated with Claude Code" line.
- STD-CI-1 (3) Run the profile's lint, typecheck and tests on every PR.
- STD-CI-2 (3) Do not merge while CI is red.
- STD-CI-3 (2) Do not delete, disable or loosen a check step to make CI green.
- STD-CI-5 (2) Take secrets from the CI platform's secret store; never write secrets in workflow files.
- STD-CI-6 (3) Every prod deploy needs one human approver.
- STD-CI-7 (2) Pin runner and tool versions so the pipeline is repeatable.
- STD-DOC-1 (2) Have a design before the work and an As-Built after it (part of the DoD).
- STD-DOC-2 (2) Update the README or user documentation in the same PR when user-visible behavior changes.
- STD-DOC-3 (2) Add a CHANGELOG entry for every released change.
- STD-DOC-4 (2) Record every architecture decision as an ADR with context, options and consequences.
- STD-DOC-7 (2) Describe the inputs, outputs and errors of every public API.
- STD-SEC-1 (3) Do not commit secrets and do not touch `protected_paths`.
- STD-SEC-2 (3) Do not read `.env*` files or secret files; use the environment variables provided.
- STD-SEC-3 (2) Parameterize or escape every query and command built from external data.
- STD-SEC-4 (2) Check authentication and authorization server-side for every operation on protected data.
- STD-SEC-6 (2) Do not write passwords, tokens or personal data into logs, artifacts or the journal.
- STD-SEC-7 (2) Encrypt sensitive data in transit and at rest as the spec requires.
- STD-DEP-1 (2) Record the reason for every new dependency in the design or PR (license, maintenance, size).
- STD-DEP-2 (3) Do not edit lockfiles by hand; update them only through `cmd.install` or the package manager.
- STD-DEP-3 (2) Do not add a library for a job under 50 lines of code.
- STD-DEP-4 (2) Pin dependency versions the way the ecosystem does; no floating versions for prod.
- STD-DEP-5 (2) Do not add dependencies with known critical vulnerabilities or incompatible licenses.
- STD-DEP-6 (2) Upgrade major dependencies in a separate PR, after reading the changelog for breaking changes.
- STD-OPS-1 (2) Have a tested rollback plan for every deployed change.
- STD-OPS-2 (2) Write reversible migrations and test both the up and the down direction.
- STD-OPS-3 (2) Dry-run data migrations on a copy and reconcile record counts before the real run.
- STD-OPS-4 (3) Run a smoke test after every deploy.
- STD-OPS-5 (2) Add enough logs or metrics to know the new feature works correctly in prod.
- STD-OPS-7 (3) Do not let agents operate directly on prod data or infrastructure.

## Review checklist (10)
1. The diff does exactly and fully what the task's spec and criteria ask, nothing extra (STD-DESIGN-5, STD-TEST-2).
2. Edits stay within the touchpoints; new files are in the right place (STD-DESIGN-1, STD-STRUCT-1, STD-STRUCT-2).
3. A failing test came first; tests cover edges and error paths; no skip/xfail/only (STD-TEST-1, STD-TEST-8, STD-TEST-4).
4. No test was changed to match wrong behavior; tests are independent and repeatable (STD-TEST-5, STD-TEST-6).
5. Errors are handled; input is validated at boundaries; external calls have timeouts (STD-ERR-1, STD-ERR-2, STD-ERR-5).
6. No secrets, no injection, authorization in place, no sensitive data exposed (STD-SEC-1, STD-SEC-3, STD-SEC-4, STD-SEC-6).
7. API and data contracts stay compatible, or come with a reversible migration (STD-DESIGN-3, STD-OPS-2).
8. Names, structure and style follow the profile; no dead code (STD-NAME-1, STD-NAME-2, STD-STYLE-4, STD-STYLE-5).
9. New dependencies have a reason and are worth it (STD-DEP-1, STD-DEP-3, STD-DEP-5).
10. Commits, branch and PR follow the standard; documentation travels with the change (STD-NAME-4, STD-NAME-5, STD-GIT-1, STD-DOC-2).

## Acceptance checklist (6)
1. Each acceptance criterion: run the real command, paste the output, conclude pass or fail (STD-TEST-2).
2. `cmd.test`, `cmd.lint`, `cmd.typecheck` are green on the feature branch (STD-TEST-3, STD-STYLE-2, STD-STYLE-3).
3. The diff adds none of the test-skip markers in `test.skip_markers` (STD-TEST-4).
4. Migrations run up then down successfully; reconciled data matches (STD-OPS-2, STD-OPS-3).
5. The build part of the DoD is complete (tests, code, docs edited in the task); As-Built, CHANGELOG and user documentation are the job of `/team:asbuilt` after G4 — record the owner and the check command, `/team:release` checks again (STD-DOC-1, STD-DOC-2, STD-DOC-3).
6. The diff does not touch `protected_paths` and contains no secrets (STD-SEC-1).

## Finding format
One line per finding:
`severity | STD | file:line | description | fix`
- `severity` ∈ `blocker` (blocks the merge), `major` (must be fixed in this task), `minor`.
- List only blockers and majors. Fold every minor into one final line: `minor | — | — | <n> small points: ... | dev's call`.
- Each finding has exactly one STD code; without a code it is not a finding.
