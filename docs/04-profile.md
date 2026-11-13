# 04 — The project profile (`.team/profile.json`)

The profile holds everything that is specific to the stack. Agents, skills and hooks only name SLOTS; they never contain commands. The file is committed.

| File | Purpose |
|---|---|
| `templates/schemas/profile.schema.json` | Schema (JSON Schema draft-07) of the profile |
| `templates/schemas/config.schema.json` | Schema of `.team/config.json` |
| `templates/project/team/config.json` | Default config copied into the project at onboard |
| `profiles/_template.json` | Every slot, empty values, `notes` explaining each slot |
| `profiles/python.json`, `node-ts.json`, `go.json`, `java-maven.json`, `flutter.json` | Sensible per-stack defaults; uncertain values are flagged in `notes` |
| `scripts/check-profile.py` | Checks a file against a schema: `scripts/check-profile.py <schema> <file>...` |

`/team:takeover` proposes a profile with evidence for every slot (`docs/team/profile-proposal.md`); `/team:onboard` writes the file after the human approves G0.

**Config slot `output_language`** (in `.team/config.json`, not in the profile): enum `vi|en`, default `vi`. It sets the prose language of the artifacts the team writes in `docs/team/` (spec, design, plan, review, acceptance, As-Built…); templates come from `templates/artifacts/vi/` when it is `vi` and that file exists, otherwise from `templates/artifacts/`. Machine-read anchors never translate, whatever the value: `Approved-by:`, `## Definition of Done`, `Verdict: …`, statuses, task lines, STD codes, IDs (full list: `scripts/anchors.txt`).

## The slots
| Slot | Meaning | Example (illustration, Python project) |
|---|---|---|
| `stack` | Name of the main stack | `"python"` |
| `language[]` | Languages used in the repo | `["python", "sql"]` |
| `cmd.install` | Install dependencies | `"pip install -e .[dev]"` |
| `cmd.build` | Build | `"python -m build"` |
| `cmd.test` | The whole test suite | `"pytest -q"` |
| `cmd.test_one` | **Required.** Run the tests of one file; `{file}` is the placeholder | `"pytest -q {file}"` |
| `cmd.lint` | Lint | `"ruff check ."` |
| `cmd.typecheck` | Type check | `"mypy src"` |
| `cmd.format` | Format one file | `"ruff format {file}"` |
| `cmd.run` | Run the application | `"python -m app"` |
| `cmd.migrate` | Run migrations | `"alembic upgrade head"` |
| `formatters_by_ext{}` | Formatter per file extension, applied after every edit | `{".py": "ruff format {file}"}` |
| `structure.src` | Source directory | `"src"` |
| `structure.tests` | Test directory, or `"colocated"` | `"tests"` |
| `structure.docs`, `structure.scripts`, `structure.config[]` | Where docs, scripts and config live | `"docs"`, `"scripts"`, `["pyproject.toml"]` |
| `structure.allowed_new_file_roots[]` | CLOSED list of places where new files may be created | `["src", "tests", "docs"]` |
| `naming.file`, `class`, `function`, `constant`, `test_file` | Naming conventions | `"snake_case"`, `"PascalCase"`, `"test_{name}.py"` |
| `naming.branch` | Branch pattern | `"team/{id}-{slug}"` |
| `test.skip_markers[]` | Test-skip markers that must not be used to make things green | `["@pytest.mark.skip", "xfail"]` |
| `test.shared_state` | `true` when test runs share one database, site or service, so two full suites at once interfere; the build then runs the full `cmd.test` only after each serial merge, never inside a parallel wave | `true` (Frappe/ERPNext site, one shared dev DB) |
| `protected_paths[]` | No agent may edit these: secrets, lockfiles, vendored libraries, prod config | `[".env*", "poetry.lock", "vendor/**"]` |
| `ci.provider`, `ci.runner`, `ci.setup[]` | CI platform | `"github"`, `"ubuntu-latest"` |
| `deploy.staging`, `deploy.smoke`, `deploy.prod_requires_reviewer` | Staging deploy command, smoke test; prod always needs a human | `true` |
| `ui` | The project has a user interface (turns on qa with Playwright) | `false` |
| `tracker` | Where issues are managed | `"github"` |
| `plugins.required[]`, `plugins.recommended[]` | Plugins needed / recommended; onboard only prints the install commands | — |
| `notes` | Slot → one-line note; flags uncertain values | `{"cmd.migrate": "Unverified: ..."}` |
| `packages` | Monorepo: directory → partial profile override | `{"web": {"stack": "node-ts"}}` |

## Rules
- `cmd.test_one` is required. Every command runs from the repo root.
- `{file}` is the only placeholder.
- `allowed_new_file_roots` is a closed list: outside it, the hook flags file creation (a stop with `enforcement: "block"`).
- Monorepo: root profile + `packages` overrides per directory.
- Enums: `ci.provider` and `tracker` ∈ `github|gitlab|none`; `deploy.prod_requires_reviewer` accepts only `true`; `output_language` (config) ∈ `vi|en`.
- Do not add new slots yourself; propose them through `/team:feedback`. The schema has `additionalProperties: false`, so unknown slots are reported as errors.

## Adding a profile for a new stack
1. Copy `profiles/_template.json` to `profiles/<stack>.json` (English name, kebab-case).
2. Fill in every slot; leave slots that do not apply empty. Uncertain commands → record them in `notes`.
3. Add the language's official LSP plugin (if any) to `plugins.recommended`.
4. Run `scripts/check-profile.py templates/schemas/profile.schema.json profiles/<stack>.json`, then `scripts/validate.sh`.
