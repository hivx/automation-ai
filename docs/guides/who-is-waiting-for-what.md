# Who is waiting for what — reading `/team:status`

`/team:status` computes the position from the artifacts in `docs/team/features/<ID>/`; it does not read a stored pointer. The result answers three things: which stage the feature is in, who holds the ball, and the next command.

## How the stage is computed
| Artifact present | Status |
|---|---|
| `intake.md` | intaken |
| `spec.md` with DoD | specified |
| `research.md` | researched |
| `arch-impact.md` or a reference to `architecture.md` | architected |
| `design.md` | designed |
| `plan.md` + `tasks.md` | planned |
| every task ticked | built |
| `acceptance.md` with verdict accepted | verified |
| `asbuilt.md` + the Released mark | released |

An enabled gate that is not approved blocks every status after it.

## Who is waiting
| Status reports | Who must act | What to do |
|---|---|---|
| `WAITING_FOR_APPROVAL Gn` | The human | Read the named artifact, add `Approved-by:` (or `@claude approve Gn`), then `/team:run` |
| `WAITING_FOR_ANSWER` | The human | Answer the questions (in the session or as an issue comment), then `/team:run` |
| `BLOCKED` | The human or tech-lead | Read the reason; fix the cause; run the printed resume command |
| `DESIGN_CONFLICT` / `design-defect` | designer/architect, the human re-approves | Fix `design.md`, re-approve the related gate |
| `IN_PROGRESS <agent>` | The team | Wait, or `/team:session` to see the handoff |
| `READY` | The human | Type the next command that was printed |

Every stop always states: the reason, which piece of work, who does what, and the command to resume. If one of the four is missing, report it with `/team:feedback`.
