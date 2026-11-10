# Playbook: release

## When it applies
- One or more features are accepted and need to be packaged and shipped to an environment.

## Default size
Not applicable.

## Chain
1. `/team:asbuilt` → writer → release notes, CHANGELOG entry.
2. `/team:release` → devops: merge the approved PR → tag.
3. `deploy.staging` → `deploy.smoke` (devops).
4. UAT: the human checks on staging.
5. Prod: only when `Approved-by-prod:` is present; then `deploy.smoke`; write the `Released:` mark into `asbuilt.md`.

## Gates
G4 (already accepted), G5 is always a human.

## Stop points
- CI is not green; the staging smoke test is red; `Approved-by-prod:` is not present yet.
- The prod smoke test is red: propose a rollback immediately.

## Done criteria
- The tag exists; staging and prod smoke tests are green with their output pasted; the `Released:` mark exists.

## Common mistakes
- Deploying to prod before UAT is done.
- No tested rollback command.

## Related playbooks
`hotfix`, `data-migration`.
