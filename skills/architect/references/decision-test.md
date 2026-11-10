# Architecture threshold test

A decision is settled at the architecture level (as an ADR) when all three conditions hold:
1. **Can diverge:** two independently built parts (two tasks, two devs, two features) could choose differently.
2. **Not obvious:** a competent builder would not pick the same thing unless told.
3. **Real trade-off:** each option has a measurable cost (performance, money, complexity, reversibility).

Missing one → not an ADR. Record it under `## Left to the designer` with the reason ("only one module uses it", "the project already has a convention").

## Examples
| Candidate | 1 | 2 | 3 | Conclusion |
|---|---|---|---|---|
| Who may write the `invoices` table | yes (billing and notify) | no | yes | ADR: only billing writes; notify listens to an event |
| API error format | yes | yes if the project has none yet | low | the project already has `{code, message}` → follow the convention, no ADR |
| Queue or synchronous call when sending email | yes | yes | yes (latency vs complexity) | ADR |
| Field name `created_at` or `createdAt` | yes | no (follows `naming.*`) | no | left to the designer |
| Redis cache "for speed later" | — | — | — | no NFR → dropped (STD-DESIGN-5) |

## Checkable constraints
Every ADR has at least one line reviewer can check on a diff:
- "Only `src/billing/**` writes the invoices table" → grep for write statements in other modules.
- "Every outbound call goes through `src/clients/` and has a timeout" → grep HTTP client imports outside that directory.
- "No module under `src/domain/` imports `src/api/`" → dependency direction.

A vague constraint ("code must be clean", "easy to extend") is not a constraint.

## Dimensions to sweep
| Dimension | Question |
|---|---|
| Environments and deploy | How many environments? Which deploy units? Are the commands in `deploy.*`/`docs/team/ci.md`? |
| Data ownership | One owning module per entity? Who only reads? |
| State write paths | Written synchronously, through events, or by jobs? Ordering and duplicates? |
| Errors, logs, configuration | One error style? Logs with context and no sensitive data? Where is configuration read? |
| Authentication, authorization | Where is it checked (server side)? Who grants permissions? |
| External integration | Timeout, retry, idempotency (from research `--integration`) |

Every dimension ends with one of: **decided** (cite the ADR), **left to the designer** (reason), **open question** (goes to `questions.md`, or `## Assumptions decided by the team` in decide mode).
