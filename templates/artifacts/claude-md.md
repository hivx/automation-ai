<!-- project:start -->
# <fill: project name>
<!-- Kept by the team: /team:onboard writes this block, /team:asbuilt keeps it true after each feature, /team:retro reports drift. Facts only, each checkable in the repo; no history, no plans. Budget: 150 lines (scripts/check-claude-md.py). -->

<fill: 2–4 sentences: what the system does, for whom, and its main parts — taken from assessment.md or spec.md>

## Commands
| Purpose | Command |
|---|---|
| <fill: one row per non-empty cmd.* slot: install, run, test, test one file, lint, format, typecheck, build, migrate> | `<fill: the cmd.* value, copied>` |

## Layout
- `<fill: path>/` — <fill: what lives there; one line per area an agent must know before editing>

## Domain terms
- <fill: term> — <fill: meaning in this codebase, where it lives>

## Conventions
- <fill: a rule the code follows that no linter enforces, with one example path>

## Gotchas
- <fill: symptom → cause → what to do (source: review-NN, defects.md or a rework round)>

## Where to look
- <fill: path of the architecture, ADRs, API or domain docs>
<!-- project:end -->
