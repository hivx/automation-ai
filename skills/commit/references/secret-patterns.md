# Patterns for scanning the staged part for secrets

Run on `git diff --staged` (added lines only, starting with `+`). Any hit → stop; record `file:line`, NEVER copy the value.

| Pattern (regex, case-insensitive) | Catches |
|---|---|
| `(password|passwd|pwd)\s*[:=]\s*['"][^'"]{4,}` | Hard-coded passwords |
| `(secret|token|api[_-]?key|access[_-]?key)\s*[:=]\s*['"][^'"]{8,}` | Keys, tokens |
| `-----BEGIN [A-Z ]*PRIVATE KEY-----` | Private keys |
| `AKIA[0-9A-Z]{16}` | AWS-style access keys |
| `gh[pousr]_[A-Za-z0-9]{30,}` | GitHub tokens |
| `xox[baprs]-[A-Za-z0-9-]{10,}` | Slack tokens |
| `://[^/\s:@]+:[^/\s@]+@` | Passwords in URLs |

Example command: `git diff --staged | grep -nE '^\+' | grep -iE '<pattern>'`.
False positives (sample values in tests, examples in docs) → record the reason in the report; never turn the scan off.
