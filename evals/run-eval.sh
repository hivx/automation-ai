#!/usr/bin/env bash
# run-eval.sh — run one eval scenario of a discipline skill in two modes: baseline (without the skill) and with-skill.
# Usage: evals/run-eval.sh <skill> <n> [--project DIR] [--mode both|baseline|with-skill] [--dry-run]
#   --project  onboarded sample project (default: "project" in evals/config.json, or $EVAL_PROJECT).
#   Each mode runs on a COPY of the project; the baseline kit is a copy without the skills/<skill> folder.
#   model, max_turns, max_budget_usd and allowed_tools come from evals/config.json. EVAL_KIT=<kit dir> runs another kit version.
#   Results: evals/<skill>/out/<YYYY-MM-DD>/s<n>-<mode>/{result.json,stderr.txt,output.txt,workdir.txt}; prints PASS/FAIL per check.
#   The project copy lives OUTSIDE the kit: $EVAL_WORK_ROOT (default $TMPDIR/team-evals) — Claude Code refuses writes inside a plugin folder.
# Scenario format (evals/<skill>/scenarios.md): "## Scenario <n> — …", the lines "- Setup: `…`",
#   "- Input: `…`", "- Baseline input: `…`", and under "- Checks:" the lines
#   "grep: `<regex>` in `<file|OUTPUT>`", "absent: `<regex>` in `<file|OUTPUT>`", "exists: `<path>`", "unchanged: `<path>`".
set -uo pipefail
[[ ${1:-} == --help || ${1:-} == -h || $# -lt 2 ]] && { sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; exit 0; }
EVALS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; KIT="${EVAL_KIT:-$(dirname "$EVALS")}"  # EVAL_KIT: run with another kit version (before/after comparison)
skill=$1; n=$2; shift 2
mode=both; dry=0; project="${EVAL_PROJECT:-$(jq -r '.project // ""' "$EVALS/config.json")}"
while (( $# )); do case "$1" in --project) project="$2"; shift 2 ;; --mode) mode="$2"; shift 2 ;; --dry-run) dry=1; shift ;; *) shift ;; esac; done
[[ -f $EVALS/$skill/scenarios.md ]] || { echo "run-eval: no evals/$skill/scenarios.md" >&2; exit 64; }
cfg() { jq -r ".$1" "$EVALS/config.json"; }
parse() { python3 -I - "$EVALS/$skill/scenarios.md" "$n" <<'PY'
import json, re, sys
text = open(sys.argv[1], encoding="utf-8").read()
m = re.search(rf"^## Scenario {sys.argv[2]}\b.*?(?=^## Scenario |\Z)", text, re.S | re.M)
if not m:
    sys.exit(f"scenario {sys.argv[2]} not found")
block = m.group(0)
get = lambda k: (re.search(rf"^- {k}: `(.+)`\s*$", block, re.M) or [None, ""])[1]
checks = re.findall(r"^\s+- (grep|absent): `(.+?)` in `(.+?)`\s*$|^\s+- (exists|unchanged): `(.+?)`\s*$", block, re.M)
out = [{"kind": c[0], "pattern": c[1], "target": c[2]} if c[0] else {"kind": c[3], "pattern": c[4], "target": "-"} for c in checks]
print(json.dumps({"setup": get("Setup"), "input": get("Input"), "baseline": get("Baseline input") or get("Input"), "checks": out}))
PY
}
spec="$(parse)" || exit 64
day="$(date +%F)"
modes=(); [[ $mode == both || $mode == baseline ]] && modes+=(baseline); [[ $mode == both || $mode == with-skill ]] && modes+=(with-skill)
for m in "${modes[@]}"; do
  tag="${EVAL_TAG:+-$EVAL_TAG}"; out="$EVALS/$skill/out/$day/s$n-$m$tag"; work="${EVAL_WORK_ROOT:-${TMPDIR:-/tmp}/team-evals}/$skill/$day/s$n-$m$tag"; prompt="$(jq -r "if \"$m\" == \"baseline\" then .baseline else .input end" <<<"$spec")"
  kitdir="$KIT"; [[ $m == baseline ]] && kitdir="$work.kit"
  cmd=(claude -p --plugin-dir "$kitdir" --model "$(cfg model)" --permission-mode acceptEdits "--allowedTools=$(cfg allowed_tools),Read(/$kitdir/**),Bash(bash $kitdir/scripts/*),Bash(bash \"$kitdir/scripts/*)"
       --max-turns "$(cfg max_turns)" --max-budget-usd "$(cfg max_budget_usd)" --output-format json "$prompt")
  echo "== $skill s$n [$m]"
  if (( dry )); then
    echo "  workdir: cp -a <project> $work"; [[ $m == baseline ]] && echo "  kit: copy of $KIT without skills/$skill"
    [[ -n $(jq -r .setup <<<"$spec") ]] && echo "  setup: $(jq -r .setup <<<"$spec")"
    printf '  run:'; printf ' %q' "${cmd[@]}"; echo
    jq -r '.checks[] | "  check: \(.kind) \(.pattern) \(.target)"' <<<"$spec"; continue
  fi
  [[ -d $project ]] || { echo "run-eval: invalid --project: '$project'" >&2; exit 64; }
  rm -rf "$out" "$work" "$work.kit"; mkdir -p "$out" "$(dirname "$work")"; cp -a "$project" "$work"; echo "$work" >"$out/workdir.txt"
  if [[ $m == baseline ]]; then mkdir -p "$work.kit"; (cd "$KIT" && tar --exclude="./skills/$skill" --exclude=./evals --exclude=./.git -cf - .) | tar -xf - -C "$work.kit"; fi
  echo "$kitdir" >"$work/.team/plugin_root" 2>/dev/null || true
  setup="$(jq -r .setup <<<"$spec")"; [[ -n $setup ]] && (cd "$work" && bash -c "$setup")
  (cd "$work" && timeout 1800 "${cmd[@]}" </dev/null >"$out/result.json" 2>"$out/stderr.txt")
  jq -r '.result // ""' "$out/result.json" >"$out/output.txt" 2>/dev/null
  pass=0; fail=0
  while IFS=$'\t' read -r kind pat target; do
    ok=0; f="$work/$target"; [[ $target == OUTPUT ]] && f="$out/output.txt"
    case $kind in
      grep) cat $f 2>/dev/null | grep -qiE -- "$pat" && ok=1 ;;
      absent) cat $f 2>/dev/null | grep -qiE -- "$pat" || ok=1 ;;
      exists) compgen -G "$work/$pat" >/dev/null && ok=1 ;;
      unchanged) (cd "$work" && git diff --quiet HEAD -- "$pat" && [[ -z $(git ls-files --others --exclude-standard -- "$pat") ]]) && ok=1 ;;
    esac
    if (( ok )); then pass=$((pass + 1)); echo "  PASS $kind $pat ${target}"; else fail=$((fail + 1)); echo "  FAIL $kind $pat ${target}"; fi
  done < <(jq -r '.checks[] | [.kind, .pattern, .target] | @tsv' <<<"$spec")
  cost="$(jq -r '.total_cost_usd // "?"' "$out/result.json" 2>/dev/null)"
  echo "  result: $pass pass, $fail fail, cost \$$cost → $out"
done
