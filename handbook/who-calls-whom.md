# Who calls whom

## Matrix
Row = caller, column = callee. ✓ = may call; — = may not.

| caller ↓ / callee → | team-leader | tech-lead | coach | analyst | researcher | architect | designer | dev | reviewer | qa | writer | maintainer | devops | Explore |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| team-leader | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| tech-lead | — | — | — | — | — | — | — | ✓ | ✓ | — | — | — | — | ✓ |
| coach | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| analyst | — | — | — | — | — | — | — | — | — | — | — | — | — | ✓ |
| researcher | — | — | — | — | — | — | — | — | — | — | — | — | — | ✓ |
| architect | — | — | — | — | — | — | — | — | — | — | — | — | — | ✓ |
| designer | — | — | — | — | — | — | — | — | — | — | — | — | — | ✓ |
| dev | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| reviewer | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| qa | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| writer | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| maintainer | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| devops | — | — | — | — | — | — | — | — | — | — | — | — | — | — |

- Only team-leader and tech-lead call other roles. Other roles may call only `Explore`, and only when they have the `Agent` tool.
- team-leader calls `dev` directly only for playbook quick (one trivial change, ADJ-36); every other size, S included, goes through `/team:build` (tech-lead → dev + reviewer, K-34). A question calls nobody: team-leader answers it.
- Temp agents (`/team:make-agent`) are called only by team-leader; the hook applies the `_temp` role (read-only Bash + basic git + `cmd.*`, may call only Explore).
- Nobody calls team-leader: it is the main session and the only door to the human.
- The matrix is enforced by the role-policy hook (STD level 3), not just written down.
- Maximum depth: main session (team-leader) → tech-lead → dev/reviewer → Explore.

## Handoff
Handoff = ONE FILE + a self-contained message of ≤ 10 lines. The receiver does NOT see the sender's conversation, so the message must be enough to do the work without asking back.

A handoff message always has:
1. The feature/task ID.
2. The path of the input file (artifact).
3. A one-sentence goal.
4. Done criteria.
5. Limits (paths that may be edited, things that must not be done).

A return message always has:
1. The result / verdict.
2. The path of the output file.
3. Evidence (output of the commands run).
4. What is still missing, what the risks are.

### Required fields per direction
| Direction | Required fields |
|---|---|
| tech-lead → dev | task ID; acceptance criteria; touchpoints; `cmd.test_one`; branch; the sentence "edit only within the touchpoints" |
| team-leader → dev (quick) | the same, with branch `team/<ID>` from `base_branch` |
| dev → tech-lead | files changed; tests run with real output; what is still missing |
| tech-lead → reviewer | diff (commit or branch); `design.md`; task criteria; the sentence "grade against the Review checklist (10)" |
| reviewer → tech-lead | verdict approve / request-changes / design-defect; findings in the STD format |
| team-leader → qa | `spec.md` (DoD); feature branch; the sentence "grade against the Acceptance checklist (6)" |
| qa → team-leader | verdict accepted / rework / design-defect; `acceptance.md` with real output |
| any role → team-leader when the human must be asked | status `NEEDS_ANSWER`; file holding the question (2–4 options, recommendation, consequences) |

## Reason for calling
Each time a role is called, the caller writes ONE sentence of reason in `docs/team/journal/<feature>.md` before the call, e.g. "Calling researcher because the spec needs a digital-signature library the project does not have yet." No reason, no call.
