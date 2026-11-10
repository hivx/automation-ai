# Playbook: ci-fix

## When it applies
- The CI pipeline is red on the main branch or on a PR that does not touch the related parts.
- A CI workflow needs fixing or a new step.

## Default size
S.

## Chain
0. `/team:intake` → team-leader → `intake.md`.
1. `/team:ci fix` → devops: diagnose, CLASSIFY first per STD-CI-4 (code / flaky test / environment / configuration / dependency).
2. A real defect in the code → switch to `bug-fix`. Anything else → devops fixes CI.
3. `/team:pr` → tech-lead → a SEPARATE PR for the CI change; `docs/team/ci.md` is updated.

## Gates
No dedicated gate; the PR is reviewed under the repo's rules.

## Stop points
- A real defect in the code; missing permissions or secrets.

## Done criteria
- CI is green on the fix PR; the classification and log excerpt are recorded in `docs/team/ci.md`.

## Common mistakes
- Disabling the test step to get green.
- Re-running repeatedly instead of classifying.

## Related playbooks
`bug-fix`, `release`.
