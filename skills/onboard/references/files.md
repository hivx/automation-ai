# Files onboard creates and how they are merged

| Target file | Source | Write mode |
|---|---|---|
| `.team/profile.json` | `docs/team/profile-proposal.md` or `<kit>/profiles/<stack>.json` | Create; already present → ask before replacing |
| `.team/config.json` | `<kit>/templates/project/team/config.json` | Create (includes `output_language`, default `vi`; the owner may set `en`); already present → keep it, add only missing keys (`jq -s '.[0] * .[1]'`, the project's copy wins) |
| `CLAUDE.md` team block | `<kit>/templates/project/CLAUDE.md.tmpl` | Insert/replace the block between `<!-- team:start -->` and `<!-- team:end -->`; ≤ 25 lines, at the end |
| `CLAUDE.md` project block | `<kit>/templates/artifacts/claude-md.md` (or `vi/`), filled from the takeover reports and the profile | Between `<!-- project:start -->` and `<!-- project:end -->`, above the team block; present → skip; an old CLAUDE.md is adopted into it (one reason row per cut or corrected line in `onboarding.md`); ≤ 150 lines; `scripts/check-claude-md.py` → 0 problems |
| `.claude/settings.json` | `<kit>/templates/project/claude/settings.json.tmpl` | `render.py --json --merge-into`: existing values win; arrays are unioned, duplicates dropped |
| `.claude/settings.local.json` | `<kit>/templates/project/claude/settings.local.json.tmpl` | As above; holds `Read(//<kit>/**)` for this machine only (not committed) |
| `.claude/rules/*.md` | `<kit>/templates/project/claude/rules/*.tmpl` | Never overwrite an existing file |
| `.github/workflows/team-ci.yml`, `team-feature.yml` | `<kit>/templates/project/github/workflows/` | Only when `ci.provider` = `github` |
| `.github/PULL_REQUEST_TEMPLATE.md`, `ISSUE_TEMPLATE/team-feature.yml`, `CODEOWNERS` | `<kit>/templates/project/github/` | Never overwrite |
| `.gitignore` | `<kit>/templates/project/gitignore.tmpl` | Add the missing lines |

`permissions.allow` is built from every non-empty `cmd.*` slot (as `Bash(<command> *)`) plus safe git. `permissions.deny`: pushing to protected branches, force-push, `rm -rf`, `Edit` on the `protected_paths`, `Read(.env*)`. `Read(//<kit>/**)` lives in `settings.local.json` because the kit path differs from machine to machine.
