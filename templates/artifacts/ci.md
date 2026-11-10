Feature: <ID>
Stage: ci
Author-agent: devops
Date: <YYYY-MM-DD>
Approved-by:
<!-- Gate: the approver fills in the line above as `Approved-by: <name> <YYYY-MM-DD>`. Leave it empty when there is no gate. -->

# CI/CD

## Pipeline
| Workflow | Trigger | Steps | Runner |
|---|---|---|---|

## Incident history
| Date | Run | STD-CI-4 class (code / flaky test / environment / config / dependency) | Log excerpt | Fix | PR |
|---|---|---|---|---|---|

## Deploy
- Staging: `deploy.staging` → `deploy.smoke`
- Prod: only with `Approved-by-prod:`; rollback: <verified command>
