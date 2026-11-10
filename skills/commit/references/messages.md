# Commit messages — examples

| Bad | Why | Good |
|---|---|---|
| `fix` | No scope, no ID, no meaning | `fix(otp): reject codes older than 5 minutes (FEAT-012)` |
| `update stuff (FEAT-012)` | "update" says nothing | `refactor(report): extract row formatter (FEAT-012)` |
| `feat: add csv` | Missing scope and ID | `feat(report): add to_csv export (FEAT-001)` |
| `WIP` | Not a save point | Commit when green, with a full message |
| `feat(api): add endpoint and refactor db and fix typo (FEAT-3)` | Three intents in one commit | Three commits |

## Message body (for a non-trivial change)
```
fix(otp): reject codes older than 5 minutes (FEAT-012)

Expired codes were accepted because the comparison used the issue time
instead of the verify time. Covers AC-2.
```

## Splitting commits
1. `test` + code of one behavior → one `feat`/`fix` commit.
2. Pure rename/move → `refactor`.
3. Pure formatting on touchpoint files → `chore` (or with that file's commit if the formatter forces it).
4. Docs → `docs`.
