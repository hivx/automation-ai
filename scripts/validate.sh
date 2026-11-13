#!/usr/bin/env bash
# validate.sh — static checks of the automation-ai kit (plugin `team`).
# Dependencies: bash, python3 (stdlib only), jq. Optional: claude (runs `claude plugin validate`).
# Usage: scripts/validate.sh [--strict]
#   --strict  treat WARN as FAIL (on since P4).
# Output: one line per problem `<file>: FAIL|WARN: <problem>`; non-zero exit code when there is a FAIL.

set -euo pipefail

# ---- Configuration (edit here, not the logic below) ----
SKILL_DESC_PREFIX="Use when"                       # skill descriptions (English, P9)
DESC_MAX_CHARS=500
AGENT_DESC_PREFIX="Delegate when"                  # agent descriptions (English, P9)
AGENT_DESC_MAX_CHARS=300
# Skill/agent quality bar (words, headings, rationalization/red-flag/verification counts): scripts/skill-budgets.txt,
# scripts/skill-sections.txt, scripts/agent-sections.txt — checked by scripts/kit-metrics.py --check (section 6c).
ALLOWED_TOOLS_FILE="scripts/allowed-tools.txt"
SKILL_HEADING_EXEMPT="handbook using-team"         # preloaded skills need no argument-hint
HUMAN_ONLY_SKILLS="release"  # merge, tag, deploy stay with the human; every other skill is callable by Claude (ADJ-28, ADJ-35)
FORK_SKILLS="analyze=analyst research=researcher architect=architect design=designer plan=tech-lead build=tech-lead verify=qa asbuilt=writer clean=maintainer ci=devops retro=coach pr=tech-lead audit-kit=coach"
WORKFLOW_HEADINGS="## When it applies|## Default size|## Chain|## Gates|## Stop points|## Done criteria|## Common mistakes|## Related playbooks"
PLAYBOOKS="takeover new-project new-feature change-request bug-fix quick hotfix refactor dependency-upgrade data-migration integration ci-fix docs-only client-docs release spike retro"
BATCH_FLOWS="build-all-tasks verify-all weekly-retro clean-sweep"
PLAYBOOK_WORDS=300
BATCH_WORDS=400
PENDING_PATHS_FILE="scripts/pending-paths.txt"     # paths a later step creates; emptied in P5
PATH_SCAN="agents skills workflows handbook docs templates profiles README.md CLAUDE.md"
STACK_CMD_BLACKLIST="pytest|npm test|npm run|yarn|pnpm|go test|mvn|gradle|bench |flutter test|cargo test|dotnet test"
STACK_CMD_SCAN_DIRS="agents skills hooks scripts"  # where hard-coded stack commands are forbidden
STACK_CMD_EXEMPT="scripts/validate.sh scripts/detect-stack.sh scripts/tests/"  # lists of manifest names/test cases, not commands that run
# Where to look for /team:<x> and agents/<role>.md references
REF_SCAN_PATHS="agents skills workflows hooks scripts handbook profiles templates evals docs README.md CLAUDE.md SPEC.md CHANGELOG.md"

STRICT=0
for arg in "$@"; do
  case "$arg" in
    --strict) STRICT=1 ;;
    -h|--help) sed -n '2,6p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "validate.sh: unknown argument: $arg" >&2; exit 64 ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

for dep in python3 jq; do
  command -v "$dep" >/dev/null 2>&1 || { echo "validate.sh: missing dependency: $dep" >&2; exit 69; }
done

REPORT="$(mktemp)"
PYCACHE="$(mktemp -d)"
trap 'rm -rf "$REPORT" "$PYCACHE"' EXIT

fail() { echo "$1: FAIL: $2" >>"$REPORT"; }
warn() { echo "$1: WARN: $2" >>"$REPORT"; }

# ---- 1. JSON parse + required manifest fields ----
while IFS= read -r -d '' f; do
  f="${f#./}"
  jq empty "$f" >/dev/null 2>&1 || fail "$f" "invalid JSON"
done < <(find . -path ./.git -prune -o -name '*.json' -type f -print0)

PLUGIN=.claude-plugin/plugin.json
MARKET=.claude-plugin/marketplace.json
if [[ -f $PLUGIN ]]; then
  for key in name version description; do
    jq -e --arg k "$key" '.[$k] | type == "string" and length > 0' "$PLUGIN" >/dev/null 2>&1 \
      || fail "$PLUGIN" "missing string field '$key'"
  done
  jq -e '.author.name | type == "string"' "$PLUGIN" >/dev/null 2>&1 || fail "$PLUGIN" "missing author.name"
  [[ "$(jq -r '.name' "$PLUGIN" 2>/dev/null)" == "team" ]] || fail "$PLUGIN" "name must be 'team'"
else
  fail "$PLUGIN" "missing"
fi
if [[ -f $MARKET ]]; then
  jq -e '.name | type == "string"' "$MARKET" >/dev/null 2>&1 || fail "$MARKET" "missing name"
  jq -e '.owner.name | type == "string"' "$MARKET" >/dev/null 2>&1 || fail "$MARKET" "missing owner.name"
  jq -e '.plugins | type == "array" and length > 0' "$MARKET" >/dev/null 2>&1 || fail "$MARKET" "plugins must be a non-empty array"
  jq -e 'all(.plugins[]?; (.name | type == "string") and (.source != null))' "$MARKET" >/dev/null 2>&1 \
    || fail "$MARKET" "every plugin entry needs name and source"
  jq -e 'any(.plugins[]?; .name == "team" and .source == "./")' "$MARKET" >/dev/null 2>&1 \
    || fail "$MARKET" "needs plugin entry {name: team, source: ./}"
else
  fail "$MARKET" "missing"
fi

# ---- 2–6. Frontmatter, word budgets, @file, stack commands, references (python stdlib) ----
SKILL_DESC_PREFIX="$SKILL_DESC_PREFIX" DESC_MAX_CHARS="$DESC_MAX_CHARS" \
AGENT_DESC_PREFIX="$AGENT_DESC_PREFIX" AGENT_DESC_MAX_CHARS="$AGENT_DESC_MAX_CHARS" \
ALLOWED_TOOLS_FILE="$ALLOWED_TOOLS_FILE" STACK_CMD_BLACKLIST="$STACK_CMD_BLACKLIST" \
STACK_CMD_SCAN_DIRS="$STACK_CMD_SCAN_DIRS" STACK_CMD_EXEMPT="$STACK_CMD_EXEMPT" REF_SCAN_PATHS="$REF_SCAN_PATHS" \
python3 -I - >>"$REPORT" <<'PY'
import os, re, pathlib

env = os.environ
PREFIX = env["SKILL_DESC_PREFIX"]
DESC_MAX = int(env["DESC_MAX_CHARS"])
def _hmap():
    p = pathlib.Path("scripts/heading-map.txt")
    if not p.is_file() or "\ntransition: on" not in "\n" + p.read_text(encoding="utf-8"):
        return {}
    return {x.encode("ascii").decode("unicode_escape"): y for x, y in (l.split(" = ", 1) for l in p.read_text(encoding="utf-8").splitlines() if " = " in l and not l.startswith("# "))}
HMAP = _hmap()
ALT = {v.split(":", 1)[1]: k.split(":", 1)[1] for k, v in HMAP.items() if k.startswith("prefix:")}
def pfx(desc, want):
    return desc.startswith(want) or (want in ALT and desc.startswith(ALT[want]))

SELF = "scripts/validate.sh"
TEXT_EXT = {".md", ".sh", ".py", ".json", ".yml", ".yaml", ".tmpl", ".txt", ""}

def out(kind, f, msg):
    print(f"{f}: {kind}: {msg}")

def read(p):
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None

def frontmatter(text):
    """Minimal YAML frontmatter reader: top-level `key: value` plus block scalars."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, text
    data, key = {}, None
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val in (">", "|", ">-", "|-", ">+", "|+"):
                val = ""
            elif len(val) >= 2 and val[0] == val[-1] and val[0] in "'\"":
                val = val[1:-1]
            data[key] = val
        elif key and line.startswith((" ", "\t")):
            data[key] = (data[key] + " " + line.strip()).strip()
    return data, "\n".join(lines[end + 1:])

def files_under(paths):
    for p in paths:
        p = pathlib.Path(p)
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.name != ".gitkeep" and f.suffix in TEXT_EXT:
                    yield f

# 2. frontmatter of agents and skills
try:
    ALLOWED_TOOLS = {l.strip() for l in open(env["ALLOWED_TOOLS_FILE"], encoding="utf-8")
                     if l.strip() and not l.startswith("#")}
except OSError:
    ALLOWED_TOOLS = set()
    out("FAIL", env["ALLOWED_TOOLS_FILE"], "missing tool allowlist")
docs = []
for f in sorted(pathlib.Path("agents").glob("*.md")):
    docs.append(("agent", f, f.stem))
skills_dir = pathlib.Path("skills")
for d in sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []:
    sk = d / "SKILL.md"
    if sk.is_file():
        docs.append(("skill", sk, d.name))
    else:
        out("WARN", str(d), "SKILL.md missing (folder still empty)")

for kind, f, expected in docs:
    text = read(f)
    if text is None:
        out("FAIL", str(f), "not UTF-8 text"); continue
    fm, body = frontmatter(text)
    if fm is None:
        out("FAIL", str(f), "missing YAML frontmatter"); continue
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not name:
        out("FAIL", str(f), "frontmatter lacks name")
    elif name != expected:
        out("FAIL", str(f), f"name '{name}' must equal '{expected}'")
    if not desc:
        out("FAIL", str(f), "frontmatter lacks description")
    else:
        if len(desc) > DESC_MAX:
            out("FAIL", str(f), f"description is {len(desc)} chars (max {DESC_MAX})")
        if kind == "skill" and not pfx(desc, PREFIX):
            out("FAIL", str(f), f"description must start with '{PREFIX}'")
    if kind == "agent":
        if desc and not pfx(desc, env["AGENT_DESC_PREFIX"]):
            out("FAIL", str(f), f"description must start with '{env['AGENT_DESC_PREFIX']}'")
        if len(desc) > int(env["AGENT_DESC_MAX_CHARS"]):
            out("FAIL", str(f), f"description is {len(desc)} chars (max {env['AGENT_DESC_MAX_CHARS']})")
        tools = [x.strip() for x in fm.get("tools", "").split(",") if x.strip()]
        if not tools:
            out("FAIL", str(f), "tools must be listed explicitly")
        for tool in tools:
            if tool not in ALLOWED_TOOLS:
                out("FAIL", str(f), f"tool '{tool}' not in {env['ALLOWED_TOOLS_FILE']}")
        print(f"{f}: INFO: body {len(body.split())} words")

# 3. no @file includes in skills/agents
inc = re.compile(r"^\s*@(?:[~.]?/|[\w.-]+/|[\w-]+\.[A-Za-z0-9]+\b)")
for f in files_under(["agents", "skills"]):
    text = read(f) or ""
    for n, line in enumerate(text.split("\n"), 1):
        if inc.match(line):
            out("FAIL", f"{f}:{n}", "@file include is forbidden")

# 4. hard-coded stack commands
terms = [t for t in env["STACK_CMD_BLACKLIST"].split("|") if t]
pat = re.compile("|".join(
    r"(?<![\w-])" + re.escape(t.rstrip()) + (r"(?=\s)" if t.endswith(" ") else r"(?![\w-])")
    for t in terms))
exempt = env.get("STACK_CMD_EXEMPT", "").split()
for f in files_under(env["STACK_CMD_SCAN_DIRS"].split()):
    if any(str(f) == e or (e.endswith("/") and str(f).startswith(e)) for e in exempt):
        continue
    text = read(f) or ""
    for n, line in enumerate(text.split("\n"), 1):
        m = pat.search(line)
        if m:
            out("FAIL", f"{f}:{n}", f"hard-coded stack command '{m.group(0)}' (use a cmd.* profile slot)")

# 5. cross references
skill_names = {d.name for d in skills_dir.iterdir() if d.is_dir()} if skills_dir.is_dir() else set()
agents_dir = pathlib.Path("agents")
agent_files = {f.stem for f in agents_dir.glob("*.md")} if agents_dir.is_dir() else set()
cmd_ref = re.compile(r"/team:([a-z][a-z0-9-]*)")
agent_ref = re.compile(r"agents/([a-z][a-z0-9-]*)\.md")
for f in files_under(env["REF_SCAN_PATHS"].split()):
    if str(f) == SELF:
        continue
    text = read(f) or ""
    for n, line in enumerate(text.split("\n"), 1):
        for m in cmd_ref.finditer(line):
            x = m.group(1)
            if x not in skill_names:
                out("FAIL", f"{f}:{n}", f"/team:{x} has no skills/{x}/ folder")
            elif not (skills_dir / x / "SKILL.md").is_file():
                pass  # folder exists but still empty: reported once above as WARN
        if str(f).startswith(("skills/", "workflows/")):
            for m in agent_ref.finditer(line):
                x = m.group(1)
                if x not in agent_files:
                    kind = "WARN" if not agent_files else "FAIL"
                    out(kind, f"{f}:{n}", f"agents/{x}.md does not exist")
PY

# ---- 6b. P4 checks: skill structure, workflows, kit path references ----
SKILL_HEADING_EXEMPT="$SKILL_HEADING_EXEMPT" HUMAN_ONLY_SKILLS="$HUMAN_ONLY_SKILLS" \
FORK_SKILLS="$FORK_SKILLS" WORKFLOW_HEADINGS="$WORKFLOW_HEADINGS" PLAYBOOK_WORDS="$PLAYBOOK_WORDS" \
BATCH_WORDS="$BATCH_WORDS" PLAYBOOKS="$PLAYBOOKS" BATCH_FLOWS="$BATCH_FLOWS" ALLOWED_TOOLS_FILE="$ALLOWED_TOOLS_FILE" \
PENDING_PATHS_FILE="$PENDING_PATHS_FILE" PATH_SCAN="$PATH_SCAN" \
python3 -I - >>"$REPORT" <<'PY'
import os, re, pathlib

def _hmap():
    p = pathlib.Path("scripts/heading-map.txt")
    if not p.is_file() or "\ntransition: on" not in "\n" + p.read_text(encoding="utf-8"):
        return {}
    return {x.encode("ascii").decode("unicode_escape"): y for x, y in (l.split(" = ", 1) for l in p.read_text(encoding="utf-8").splitlines() if " = " in l and not l.startswith("# "))}
HMAP = _hmap()
env = os.environ

def out(kind, f, msg):
    print(f"{f}: {kind}: {msg}")

def split_fm(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, text
    fm = {}
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            v = m.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
                v = v[1:-1]
            fm[m.group(1)] = v
    return fm, "\n".join(lines[end + 1:])

tools_ok = {l.strip() for l in open(env["ALLOWED_TOOLS_FILE"], encoding="utf-8")
            if l.strip() and not l.startswith("#")}
exempt = set(env["SKILL_HEADING_EXEMPT"].split())
human = set(env["HUMAN_ONLY_SKILLS"].split())
forks = dict(p.split("=") for p in env["FORK_SKILLS"].split())
agents = {p.stem for p in pathlib.Path("agents").glob("*.md")}

for sk in sorted(pathlib.Path("skills").glob("*/SKILL.md")):
    name = sk.parent.name
    fm, body = split_fm(sk.read_text(encoding="utf-8"))
    if name not in exempt:
        if not fm.get("argument-hint"):
            out("FAIL", str(sk), "missing argument-hint")
    for entry in re.findall(r"[A-Za-z]+(?:\([^)]*\))?", fm.get("allowed-tools", "")):
        tool = entry.split("(", 1)[0]
        if tool not in tools_ok:
            out("FAIL", str(sk), f"allowed-tools entry '{entry}' uses unknown tool")
        elif tool == "Bash" and (entry == "Bash" or entry in ("Bash(*)", "Bash( *)")):
            out("FAIL", str(sk), "allowed-tools must not grant bare Bash")
    dmi = fm.get("disable-model-invocation") == "true"
    if name in human and not dmi:
        out("FAIL", str(sk), "human-only skill needs disable-model-invocation: true")
    if name not in human and dmi:
        out("FAIL", str(sk), "disable-model-invocation: true but skill is not in HUMAN_ONLY_SKILLS")
    if fm.get("context") == "fork" or name in forks:
        agent = fm.get("agent", "")
        if fm.get("context") != "fork":
            out("FAIL", str(sk), "must set context: fork")
        if name in forks and agent != f"team:{forks[name]}":
            out("FAIL", str(sk), f"agent must be team:{forks[name]} (got '{agent}')")
        if not agent.startswith("team:") or agent.split(":", 1)[1] not in agents:
            out("FAIL", str(sk), f"agent '{agent}' must be team:<existing agent> (bare names fall back silently)")
    for ref in re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([A-Za-z0-9_./-]+)", body):
        if not (sk.parent / ref).is_file():
            out("FAIL", str(sk), f"${{CLAUDE_SKILL_DIR}}/{ref} does not exist")

wh = env["WORKFLOW_HEADINGS"].split("|")
for kind, names, budget in (("playbook", env["PLAYBOOKS"].split(), int(env["PLAYBOOK_WORDS"])),
                            ("batch", env["BATCH_FLOWS"].split(), int(env["BATCH_WORDS"]))):
    base = pathlib.Path("workflows") / ("batch" if kind == "batch" else "")
    for n in names:
        f = base / f"{n}.md"
        if not f.is_file():
            out("FAIL", str(f), f"{kind} missing")
            continue
        text = f.read_text(encoding="utf-8")
        heads = [HMAP.get(l.strip(), l.strip()) for l in text.split("\n") if l.startswith("## ")]
        if heads != wh:
            out("FAIL", str(f), "headings must be exactly, in order: " + " / ".join(wh))
        words = len("\n".join(text.split("\n")[1:]).split())
        if words > budget:
            out("FAIL", str(f), f"{words} words (budget {budget})")

pending = set()
pf = pathlib.Path(env["PENDING_PATHS_FILE"])
if pf.is_file():
    pending = {l.strip() for l in pf.read_text(encoding="utf-8").split("\n") if l.strip() and not l.startswith("#")}
for p in sorted(pending):
    if pathlib.Path(p).exists():
        out("FAIL", str(pf), f"{p} now exists; remove it from the pending list")
prefix = re.compile(r'(<kit>/|\$\{CLAUDE_PLUGIN_ROOT\}/|\$\(cat \.team/plugin_root\)/)')
ref = re.compile(r"(?<![\w./<>$(-])((?:scripts|templates|handbook|workflows|profiles|hooks|agents|skills)/[A-Za-z0-9_./-]*[A-Za-z0-9_-]\.(?:sh|py|md|json|jsonl|yml|yaml|tmpl|txt))\b")
seen_missing = {}
targets = []
for t in env["PATH_SCAN"].split():
    p = pathlib.Path(t)
    targets += [p] if p.is_file() else [x for x in sorted(p.rglob("*")) if x.is_file() and x.suffix in (".md", ".json", ".yml", ".tmpl")]
HISTORICAL = ("docs/acceptance/", "docs/requirements/")  # historical records, never rewritten
for f in targets:
    if str(f).startswith(HISTORICAL):
        continue
    for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
        for m in ref.finditer(prefix.sub("", line)):
            path = m.group(1)
            if not pathlib.Path(path).exists() and path not in pending:
                seen_missing.setdefault(path, f"{f}:{n}")
for path, where in sorted(seen_missing.items()):
    out("FAIL", where, f"kit path {path} does not exist (add to {env['PENDING_PATHS_FILE']} only if a later step creates it)")
PY

# ---- 6c. quality bar (P7): every skill/agent at the bar unless listed in scripts/quality-backlog.txt ----
if [[ -f scripts/kit-metrics.py ]]; then
  while IFS= read -r line; do
    [[ -n $line ]] && echo "${line%%: *}: FAIL: quality ${line#*: }" >>"$REPORT"
  done < <(python3 -I scripts/kit-metrics.py --check 2>&1 || true)
  if [[ -f scripts/quality-backlog.txt ]]; then
    while IFS= read -r item; do
      [[ -z $item || $item == \#* ]] && continue
      echo "scripts/quality-backlog.txt: INFO: $item not yet at the quality bar (later round)" >>"$REPORT"
    done < scripts/quality-backlog.txt
  fi
fi

# ---- 7. bash -n / py_compile ----
shopt -s nullglob
for f in scripts/*.sh scripts/tests/*.sh; do
  bash -n "$f" 2>/dev/null || fail "$f" "bash -n syntax error"
done
for f in scripts/*.py; do
  PYTHONPYCACHEPREFIX="$PYCACHE" python3 -m py_compile "$f" 2>/dev/null || fail "$f" "py_compile error"
done

# ---- 8. hooks/hooks.json ----
HOOKS=hooks/hooks.json
if [[ -f $HOOKS ]]; then
  if jq -e '.hooks | type == "object"' "$HOOKS" >/dev/null 2>&1; then
    while IFS= read -r cmd; do
      while IFS= read -r rel; do
        [[ -z $rel ]] && continue
        if [[ ! -f $rel ]]; then fail "$HOOKS" "referenced script missing: $rel"
        elif [[ ! -x $rel ]]; then fail "$HOOKS" "referenced script not executable: $rel"
        fi
      done < <(grep -oE '\$\{?CLAUDE_PLUGIN_ROOT\}?/[A-Za-z0-9_./-]+' <<<"$cmd" | sed -E 's#^\$\{?CLAUDE_PLUGIN_ROOT\}?/##')
    done < <(jq -r '.. | objects | select(.type? == "command") | .command' "$HOOKS")
  else
    fail "$HOOKS" "must be JSON with a top-level 'hooks' object"
  fi
fi

# ---- 9. handbook/STD-short.md must equal freshly generated output ----
GEN=scripts/gen-handbook-short.py
SHORT=handbook/STD-short.md
if [[ -f handbook/STD.md && -f $GEN ]]; then
  if gen_out="$(python3 -I "$GEN" --stdout 2>&1)"; then
    if [[ ! -f $SHORT ]]; then
      fail "$SHORT" "missing; run $GEN"
    elif ! diff -q <(printf '%s\n' "$gen_out") "$SHORT" >/dev/null; then
      fail "$SHORT" "stale or edited by hand; run $GEN"
    fi
  else
    fail "handbook/STD.md" "generator failed: $(tr '\n' ' ' <<<"$gen_out")"
  fi
fi

# ---- 9b. docs/02-team.md role table must match agents/*.md frontmatter ----
if [[ -f scripts/gen-team-table.py ]] && compgen -G "agents/*.md" >/dev/null; then
  python3 -I scripts/gen-team-table.py --check \
    || fail "docs/02-team.md" "role table out of sync; run scripts/gen-team-table.py"
fi

# ---- 9c. generated guides (skills/README.md, want-x-type-y.md, decision-tree.md) ----
if [[ -f scripts/gen-guides.py ]]; then
  while IFS= read -r line; do
    [[ -n $line ]] && echo "${line%%: *}: FAIL: ${line#*: }" >>"$REPORT"
  done < <(python3 -I scripts/gen-guides.py --check 2>&1 || true)
fi

# ---- 9d. owner guide (GUIDE-VI.md): generated blocks fresh, vi-strings.json complete (P9) ----
if [[ -f scripts/gen-vi-guide.py ]]; then
  while IFS= read -r line; do
    [[ -n $line ]] && echo "scripts/gen-vi-guide.py: FAIL: ${line#gen-vi-guide: }" >>"$REPORT"
  done < <(python3 -I scripts/gen-vi-guide.py --check 2>&1 || true)
fi

# ---- 9e. language zones and anchors (P9): no translated anchor, no Vietnamese prose outside the allowlist ----
if [[ -f scripts/check-lang.py ]]; then
  while IFS= read -r line; do
    [[ $line == FAIL* ]] && echo "${line#FAIL }" | sed 's/^\(anchor\|zone\): \([^:]*\):/\2: FAIL: \1:/' >>"$REPORT"
  done < <(python3 -I scripts/check-lang.py 2>&1 || true)
fi

# ---- 10. profiles and config template against their schemas ----
check_schema() { # check_schema <schema> <file>...
  local schema=$1; shift
  [[ -f $schema ]] || { fail "$schema" "schema missing"; return; }
  (( $# )) || return 0
  local line
  while IFS= read -r line; do
    [[ -n $line ]] && echo "${line%%: *}: FAIL: schema ${line#*: }" >>"$REPORT"
  done < <(python3 -I scripts/check-profile.py "$schema" "$@" || true)
}
if [[ -f scripts/check-profile.py ]]; then
  check_schema templates/schemas/profile.schema.json profiles/*.json
  [[ -f templates/project/team/config.json ]] \
    && check_schema templates/schemas/config.schema.json templates/project/team/config.json
fi

# ---- 10b. test suite (--strict only) ----
if (( STRICT )) && [[ -x scripts/tests/run-all.sh ]]; then
  if ! tests_out="$(bash scripts/tests/run-all.sh 2>&1)"; then
    fail "scripts/tests/run-all.sh" "tests failed: $(grep -E 'FAIL|failed|Error' <<<"$tests_out" | head -n 3 | tr '\n' ' ')"
  fi
fi

# ---- 10c. cross-reference audit (--strict only) ----
if (( STRICT )) && [[ -f scripts/audit-xref.py ]]; then
  while IFS= read -r line; do
    [[ -n $line && $line != audit-xref:* ]] && echo "${line%%: *}: FAIL: xref ${line#*: }" >>"$REPORT"
  done < <(python3 -I scripts/audit-xref.py 2>&1 || true)
fi

# ---- 11. official validator (optional, only if the claude CLI is installed) ----
if command -v claude >/dev/null 2>&1; then
  if ! out="$(claude plugin validate . 2>&1)"; then
    fail ".claude-plugin" "claude plugin validate failed: $(tail -n 3 <<<"$out" | tr '\n' ' ')"
  fi
fi

# ---- Summary ----
sort -u -o "$REPORT" "$REPORT"
[[ -s $REPORT ]] && cat "$REPORT"
FAILS=$(grep -c ': FAIL: ' "$REPORT" || true)
WARNS=$(grep -c ': WARN: ' "$REPORT" || true)
if (( STRICT )); then FAILS=$((FAILS + WARNS)); fi
echo "validate: ${FAILS} fail, ${WARNS} warn (strict=${STRICT})"
(( FAILS == 0 ))
