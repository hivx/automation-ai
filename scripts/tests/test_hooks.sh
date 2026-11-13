#!/usr/bin/env bash
# test_hooks.sh — feeds fake hook JSON to protect.sh, check-git.sh, role-policy.sh, stop-check.sh and checks the exit codes.
set -uo pipefail
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
pass=0; failn=0
check() { # check <name> <expected code> <script> <json> [--root dir]
  local name=$1 want=$2 script=$3 json=$4; shift 4
  local got err
  err="$(CLAUDE_PROJECT_DIR="$T/p" bash "$KIT/scripts/$script" "$@" <<<"$json" 2>&1 >/dev/null)"; got=$?
  if [[ $got == "$want" ]]; then pass=$((pass + 1)); echo "ok   $name (exit $got)";
  else failn=$((failn + 1)); echo "FAIL $name: want $want got $got — ${err:0:200}"; fi
}
mkdir -p "$T/p/.team" "$T/p/src" "$T/p/tests" "$T/p/docs/team/features/FEAT-001"
cd "$T/p" && git init -q -b main && git -c user.name=t -c user.email=t@t commit -q --allow-empty -m init && git switch -q -c team/FEAT-001-x
cp "$KIT/profiles/python.json" .team/profile.json
jq '.enforcement = "block"' "$KIT/templates/project/team/config.json" > .team/config.json  # the checks below test the block mode
echo 'x = 1' > src/existing.py
P="$T/p"
w() { jq -nc --arg t "$1" --arg f "$2" '{hook_event_name:"PreToolUse", tool_name:$t, tool_input:{file_path:$f}}'; }
b() { jq -nc --arg c "$1" --arg cwd "$P" --arg a "${2:-}" '{hook_event_name:"PreToolUse", tool_name:"Bash", cwd:$cwd, tool_input:{command:$c}} + (if $a == "" then {} else {agent_type:$a} end)'; }

# protect.sh
check "protect: .env blocked"                    2 protect.sh "$(w Edit "$P/.env")"
check "protect: lockfile blocked"                2 protect.sh "$(w Write "$P/poetry.lock")"
check "protect: .git blocked"                    2 protect.sh "$(w Write "$P/.git/config")"
check "protect: settings.json blocked"           2 protect.sh "$(w Write "$P/.claude/settings.json")"
check "protect: new file outside roots blocked"  2 protect.sh "$(w Write "$P/random/new.py")"
check "protect: new file in src allowed"         0 protect.sh "$(w Write "$P/src/new.py")"
check "protect: editing existing file allowed"   0 protect.sh "$(w Edit "$P/src/existing.py")"
check "protect: .team/profile.json blocked"     2 protect.sh "$(w Edit "$P/.team/profile.json")"
check "protect: .team/current.json allowed"     0 protect.sh "$(w Write "$P/.team/current.json")"
check "protect: docs/team always allowed"        0 protect.sh "$(w Write "$P/docs/team/features/FEAT-001/spec.md")"
check "protect: new file in worktree/tests allowed" 0 protect.sh "$(w Write "$P/.claude/worktrees/agent-x/tests/test_new.py")"
check "protect: worktree/.env blocked"         2 protect.sh "$(w Write "$P/.claude/worktrees/agent-x/.env")"
check "protect: worktree/random blocked"       2 protect.sh "$(w Write "$P/.claude/worktrees/agent-x/random/x.py")"
check "protect: outside the project allowed"     0 protect.sh "$(w Write "/tmp/elsewhere.txt")"
check "protect: new root CHANGELOG.md allowed"   0 protect.sh "$(w Write "$P/CHANGELOG.md")"

# check-git.sh
check "git: push origin main blocked"            2 check-git.sh "$(b 'git push origin main')"
check "git: commit with Co-Authored-By blocked (STD-GIT-8)" 2 check-git.sh "$(b $'git commit -m "feat(x): add y (FEAT-001)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"')"
check "git: heredoc commit with co-authored-by blocked" 2 check-git.sh "$(b $'git commit -m "$(cat <<\'EOF\'\nfix(x): z (BUG-001)\n\nco-authored-by: Someone <a@b.c>\nEOF\n)"')"
check "git: plain commit allowed"                0 check-git.sh "$(b 'git commit -m "feat(x): add y (FEAT-001)"')"
check "gh: PR body with Generated with Claude Code blocked" 2 check-git.sh "$(b $'gh pr create --title t --body "Why\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)"')"
check "gh: PR without attribution allowed"       0 check-git.sh "$(b 'gh pr create --title t --body "Why: x"')"
check "git: push HEAD:main blocked"              2 check-git.sh "$(b 'git push origin HEAD:main')"
check "git: push team/x allowed"                 0 check-git.sh "$(b 'git push -u origin team/FEAT-001-x')"
check "git: push without refspec on team/* allowed" 0 check-git.sh "$(b 'git push')"
check "git: push feature/y blocked (team/* only)" 2 check-git.sh "$(b 'git push origin feature/y')"
check "git: push --force blocked"                2 check-git.sh "$(b 'git push --force origin team/FEAT-001-x')"
check "git: push -f blocked"                     2 check-git.sh "$(b 'git push -fu origin team/FEAT-001-x')"
check "git: push +refspec blocked"               2 check-git.sh "$(b 'git push origin +team/FEAT-001-x')"
check "git: push --delete blocked"               2 check-git.sh "$(b 'git push origin --delete team/old')"
check "git: push --tags allowed"                 0 check-git.sh "$(b 'git push origin --tags')"
check "git: commit --no-verify blocked"          2 check-git.sh "$(b 'git commit --no-verify -m "feat(x): y (FEAT-001)"')"
check "git: commit -n blocked"                   2 check-git.sh "$(b 'git commit -n -m "x"')"
check "git: badly formatted commit only warns"   0 check-git.sh "$(b 'git commit -m "update stuff"')"
check "git: compound && push main blocked"       2 check-git.sh "$(b 'git add . && git push origin main')"
check "git: -c core.hooksPath blocked"         2 check-git.sh "$(b 'git -c core.hooksPath=/dev/null commit -m x')"
check "git: -c alias.x=!cmd blocked"           2 check-git.sh "$(b "git -c alias.x='!rm -rf .' x")"
check "git: valid -c user.name allowed"        0 check-git.sh "$(b 'git -c user.name=A log -1')"
check "git: filter-branch blocked"               2 check-git.sh "$(b 'git filter-branch --tree-filter x HEAD')"
git switch -q main
check "git: reset --hard on main blocked"        2 check-git.sh "$(b 'git reset --hard HEAD~1')"
check "git: rebase -i on main blocked"           2 check-git.sh "$(b 'git rebase -i HEAD~2')"
git switch -q team/FEAT-001-x
check "git: reset --hard on team/* allowed"      0 check-git.sh "$(b 'git reset --hard HEAD')"

# role-policy.sh
rw() { jq -nc --arg t "$1" --arg f "$2" --arg a "$3" '{tool_name:$t, agent_type:$a, tool_input:{file_path:$f}}'; }
ag() { jq -nc --arg s "$1" --arg a "$2" '{tool_name:"Agent", agent_type:$a, tool_input:{subagent_type:$s, prompt:"x"}}'; }
check "role: team-leader writes docs/team allowed" 0 role-policy.sh "$(rw Write "$P/docs/team/journal/FEAT-001.md" team:team-leader)"
check "role: team-leader writes src blocked"     2 role-policy.sh "$(rw Write "$P/src/new.py" team:team-leader)"
check "role: dev writes src allowed"             0 role-policy.sh "$(rw Write "$P/src/new.py" team:dev)"
check "role: reviewer writes src blocked"        2 role-policy.sh "$(rw Edit "$P/src/existing.py" team:reviewer)"
check "role: reviewer writes memory allowed"     0 role-policy.sh "$(rw Write "$P/.claude/agent-memory/reviewer/notes.md" team:reviewer)"
check "role: team-leader read-only bash allowed" 0 role-policy.sh "$(b 'git log --oneline | head -n 5' team:team-leader)"
check "role: reviewer git worktree list allowed" 0 role-policy.sh "$(b 'git worktree list' team:reviewer)"
check "role: reviewer git worktree add blocked" 2 role-policy.sh "$(b 'git worktree add x' team:reviewer)"
check "role: tech-lead cd then git allowed"    0 role-policy.sh "$(b 'cd src && git status' team:tech-lead)"
check "role: reviewer \$(...) blocked"            2 role-policy.sh "$(b 'echo $(touch x)' team:reviewer)"
check "role: reviewer python3 -c blocked"        2 role-policy.sh "$(b 'python3 -c "open(1)"' team:reviewer)"
check "role: reviewer git -c pager blocked"      2 role-policy.sh "$(b 'git -c core.pager=sh log' team:reviewer)"
check "role: reviewer awk blocked"               2 role-policy.sh "$(b 'awk "BEGIN{system(1)}"' team:reviewer)"
check "role: tech-lead calls dev (no prefix) allowed" 0 role-policy.sh "$(ag dev team:tech-lead)"
check "role: tech-lead (local) calls dev allowed" 0 role-policy.sh "$(ag dev tech-lead)"
check "role: tech-lead team.py via plugin_root allowed" 0 role-policy.sh "$(b 'python3 "$(cat .team/plugin_root)/scripts/team.py" status FEAT-001' team:tech-lead)"
check "role: reviewer other \$(cat) blocked"      2 role-policy.sh "$(b 'cat $(cat .env)' team:reviewer)"
check "role: team-leader rm blocked"             2 role-policy.sh "$(b 'rm -rf src' team:team-leader)"
check "role: team-leader redirect into src blocked" 2 role-policy.sh "$(b 'echo x > src/a.py' team:team-leader)"
check "role: team-leader jq >> feedback allowed" 0 role-policy.sh "$(b 'jq -nc {} >> docs/team/metrics/feedback.jsonl' team:team-leader)"
check "role: qa runs any check command allowed"  0 role-policy.sh "$(b 'python3 -c "print(1)"' team:qa)"
check "role: tech-lead runs cmd.test allowed"    0 role-policy.sh "$(b 'pytest -q tests/test_x.py' team:tech-lead)"
check "role: tech-lead curl blocked"             2 role-policy.sh "$(b 'curl https://example.com' team:tech-lead)"
# cmd.* values with several segments (`cd ../.. && bench …`): each segment is allowed on its own
jq '.cmd.migrate="cd ../.. && bench --site s1 migrate"' .team/profile.json > .team/p && mv .team/p .team/profile.json
check "role: tech-lead runs segment of multi-part cmd allowed" 0 role-policy.sh "$(b 'bench --site s1 migrate' team:tech-lead)"
check "role: tech-lead runs whole multi-part cmd allowed" 0 role-policy.sh "$(b 'cd ../.. && bench --site s1 migrate' team:tech-lead)"
check "role: tech-lead other bench command blocked" 2 role-policy.sh "$(b 'bench --site s1 drop-site s1' team:tech-lead)"
jq '.cmd.migrate="alembic upgrade head"' .team/profile.json > .team/p && mv .team/p .team/profile.json
check "role: tech-lead calls team:dev allowed"   0 role-policy.sh "$(ag team:dev team:tech-lead)"
check "role: tech-lead calls team:qa blocked"    2 role-policy.sh "$(ag team:qa team:tech-lead)"
check "role: analyst calls Explore allowed"      0 role-policy.sh "$(ag Explore team:analyst)"
check "role: dev calls an agent blocked"         2 role-policy.sh "$(ag Explore team:dev)"
# v0.6.0: writer keeps the project block of CLAUDE.md; every role may run the check
check "role: writer edits CLAUDE.md allowed"     0 role-policy.sh "$(rw Edit "$P/CLAUDE.md" team:writer)"
check "role: writer edits src blocked"           2 role-policy.sh "$(rw Edit "$P/src/existing.py" team:writer)"
check "role: team-leader edits CLAUDE.md outside onboard blocked" 2 role-policy.sh "$(rw Edit "$P/CLAUDE.md" team:team-leader)"
check "role: writer runs check-claude-md allowed" 0 role-policy.sh "$(b "python3 $KIT/scripts/check-claude-md.py" team:writer)"
check "role: coach runs check-claude-md allowed" 0 role-policy.sh "$(b "python3 $KIT/scripts/check-claude-md.py --root ." team:coach)"
# K-39: read-only must not write or run commands
check "role: reviewer sed e cmd blocked"         2 role-policy.sh "$(b "sed '1e touch x' src/existing.py" team:reviewer)"
check "role: reviewer sed w file blocked"        2 role-policy.sh "$(b "sed -n 'w out.txt' src/existing.py" team:reviewer)"
check "role: reviewer sed s///e blocked"         2 role-policy.sh "$(b "sed 's/x/id/e' src/existing.py" team:reviewer)"
check "role: reviewer sed -n 1,20p allowed"      0 role-policy.sh "$(b "sed -n '1,20p' docs/workflows.md" team:reviewer)"
check "role: reviewer sed s/a/b/g allowed"       0 role-policy.sh "$(b "sed 's/x/y/g' src/existing.py" team:reviewer)"
check "role: reviewer sort -o blocked"           2 role-policy.sh "$(b 'sort -o src/a.py src/existing.py' team:reviewer)"
check "role: reviewer uniq IN OUT blocked"       2 role-policy.sh "$(b 'uniq src/existing.py src/b.py' team:reviewer)"
check "role: reviewer tree -o blocked"           2 role-policy.sh "$(b 'tree -o src/t.txt' team:reviewer)"
check "role: reviewer rg --pre blocked"          2 role-policy.sh "$(b 'rg --pre ./x foo' team:reviewer)"
check "role: reviewer >&file blocked"            2 role-policy.sh "$(b 'echo x >&src/a.py' team:reviewer)"
check "role: reviewer <> file blocked"           2 role-policy.sh "$(b 'cat <> src/a.py' team:reviewer)"
check "role: reviewer 2>&1 allowed"              0 role-policy.sh "$(b 'git log -1 2>&1 | head -n 3' team:reviewer)"
check "role: reviewer mkdir blocked"             2 role-policy.sh "$(b 'mkdir src/x' team:reviewer)"
# K-40: kit scripts are matched by path
check "role: reviewer kit team.py allowed"       0 role-policy.sh "$(b "python3 $KIT/scripts/team.py status" team:reviewer)"
check "role: reviewer foreign team.py blocked"   2 role-policy.sh "$(b 'python3 /tmp/x/scripts/team.py status' team:reviewer)"
check "role: reviewer foreign validate.sh blocked" 2 role-policy.sh "$(b 'bash ./validate.sh' team:reviewer)"
check "role: reviewer log-run.sh (writes) blocked" 2 role-policy.sh "$(b "bash $KIT/scripts/log-run.sh --skill x" team:reviewer)"
check "role: team-leader log-run.sh allowed"     0 role-policy.sh "$(b "bash $KIT/scripts/log-run.sh --skill x" team:team-leader)"
check "role: team-leader log-run --root blocked" 2 role-policy.sh "$(b "bash $KIT/scripts/log-run.sh --root /tmp --skill x" team:team-leader)"
# K-24: shell commands writing forbidden areas (every role, bash: any included)
check "protect-bash: dev echo > .env blocked"    2 protect.sh "$(b 'echo X=1 > .env' team:dev)"
check "protect-bash: dev sed -i lockfile blocked" 2 protect.sh "$(b "sed -i 's/a/b/' poetry.lock" team:dev)"
check "protect-bash: dev cp into .env blocked"   2 protect.sh "$(b 'cp /tmp/x .env' team:dev)"
check "protect-bash: dev rm .env blocked"        2 protect.sh "$(b 'rm -f .env' team:dev)"
check "protect-bash: dev tee profile blocked"    2 protect.sh "$(b 'echo {} | tee .team/profile.json' team:dev)"
check "protect-bash: dev mv .git/x blocked"      2 protect.sh "$(b 'mv a .git/config' team:dev)"
check "protect-bash: cd then write .env blocked" 2 protect.sh "$(b 'cd src && echo x > ../.env' team:dev)"
check "protect-bash: dev writes src allowed"     0 protect.sh "$(b 'echo x > src/a.py && cp src/a.py src/b.py' team:dev)"
check "protect-bash: rm -rf build allowed"       0 protect.sh "$(b 'rm -rf build dist' team:dev)"
check "protect-bash: 2>/dev/null allowed"        0 protect.sh "$(b 'ls 2>/dev/null' team:dev)"
check "role: researcher writes POC in worktree allowed" 0 role-policy.sh "$(rw Write "$P/.claude/worktrees/poc-x/src/poc.py" team:researcher)"
check "role: researcher writes main-tree src blocked" 2 role-policy.sh "$(rw Write "$P/src/poc.py" team:researcher)"
check "role: researcher writes research.md allowed" 0 role-policy.sh "$(rw Write "$P/docs/team/features/FEAT-001/research.md" team:researcher)"
check "role: reviewer team.py scorecard blocked" 2 role-policy.sh "$(b "python3 $KIT/scripts/team.py scorecard" team:reviewer)"
mkdir -p "$P/.claude/agents"; printf -- '---\nname: ui-spec\n---\n<!-- team: temp, created 2026-11-10, need: x -->\n' > "$P/.claude/agents/ui-spec.md"
check "role: temp agent curl blocked"             2 role-policy.sh "$(b 'curl https://x' ui-spec)"
check "role: temp agent calls dev blocked"        2 role-policy.sh "$(ag dev ui-spec)"
check "role: temp agent runs cmd.test allowed"    0 role-policy.sh "$(b 'pytest -q tests/test_x.py' ui-spec)"
check "role: coach team.py scorecard allowed"    0 role-policy.sh "$(b "python3 $KIT/scripts/team.py scorecard" team:coach)"
echo '{"feature":"","stage":"onboard"}' > "$P/.team/current.json"
check "role: onboard cp from kit/templates allowed" 0 role-policy.sh "$(b "cp $KIT/templates/project/gitignore.tmpl .gitignore.new" team:team-leader)"
check "role: onboard cp from elsewhere blocked (K-26)" 2 role-policy.sh "$(b 'cp /etc/passwd docs/x' team:team-leader)"
echo '{"feature":"","stage":"idle"}' > "$P/.team/current.json"
check "role: outside onboard cp from kit blocked" 2 role-policy.sh "$(b "cp $KIT/templates/project/gitignore.tmpl .gitignore.new" team:team-leader)"
# audit-kit round 2 (K-75): env prefixes, abbreviated long options, cd before redirection, malformed input blocks
check "role: coach GIT_EXTERNAL_DIFF= blocked"    2 role-policy.sh "$(b 'GIT_EXTERNAL_DIFF=x git diff' team:coach)"
check "role: coach BASH_ENV= kit script blocked"   2 role-policy.sh "$(b "BASH_ENV=docs/team/retro/x.sh bash $KIT/scripts/check-structure.sh" team:coach)"
check "role: coach LC_ALL=C grep allowed"          0 role-policy.sh "$(b 'LC_ALL=C grep -n x src/existing.py' team:coach)"
check "role: coach git grep --open-files-in-pager blocked" 2 role-policy.sh "$(b 'git grep --open-files-in-pager=x foo' team:coach)"
check "role: coach sort -uo blocked"               2 role-policy.sh "$(b 'sort -uo out.txt in.txt' team:coach)"
check "role: coach sort --compress-program blocked" 2 role-policy.sh "$(b 'sort --compress-program=x in.txt' team:coach)"
check "role: coach sed --in=.bak blocked"          2 role-policy.sh "$(b 'sed --in=.bak s/a/b/ f.txt' team:coach)"
check "role: coach cd then > docs/team blocked"    2 role-policy.sh "$(b 'cd src && echo x > docs/team/retro/a.md' team:coach)"
check "role: coach writes docs/team/retro allowed" 0 role-policy.sh "$(b 'echo x > docs/team/retro/a.md' team:coach)"
check "role: date -Iseconds allowed"               0 role-policy.sh "$(b 'date -Iseconds' team:reviewer)"
check "role: malformed JSON blocked"               2 role-policy.sh '{not json'
check "protect-bash: sort -o .env blocked"         2 protect.sh "$(b 'sort -o .env in.txt' team:dev)"
check "protect-bash: sort -uo profile blocked"     2 protect.sh "$(b 'sort -uo .team/profile.json in.txt' team:dev)"
check "protect-bash: sed --in=.bak .env blocked"   2 protect.sh "$(b 'sed --in=.bak s/a/b/ .env' team:dev)"
check "role: session without agent_type allowed" 0 role-policy.sh "$(jq -nc '{tool_name:"Bash", tool_input:{command:"rm -rf x"}}')"

# stop-check.sh
check "stop: stop_hook_active allows stop"       0 stop-check.sh '{"hook_event_name":"Stop","stop_hook_active":true}'
check "stop: no active-build allows stop"        0 stop-check.sh "$(jq -nc --arg c "$P" '{hook_event_name:"Stop",stop_hook_active:false,cwd:$c}')"
jq '.cmd.lint="false" | .cmd.typecheck=""' .team/profile.json > .team/p && mv .team/p .team/profile.json
touch .team/active-build; echo 'y = 2' > src/changed.py
check "stop: build with red lint blocked"        2 stop-check.sh "$(jq -nc --arg c "$P" '{hook_event_name:"Stop",stop_hook_active:false,cwd:$c}')"
jq '.cmd.lint="true"' .team/profile.json > .team/p && mv .team/p .team/profile.json
check "stop: clean build allows stop"            0 stop-check.sh "$(jq -nc --arg c "$P" '{hook_event_name:"Stop",stop_hook_active:false,cwd:$c}')"
rm .team/active-build
echo '{"feature":"FEAT-001","stage":"research"}' > .team/current.json
printf '# Research\n\n## Sources\n(none yet)\n' > docs/team/features/FEAT-001/research.md
check "stop: research without URL blocked"       2 stop-check.sh '{"hook_event_name":"Stop","stop_hook_active":false}'
printf '# Research\n\n## Sources\n- https://docs.python.org/3/ (2026-11-09)\n' > docs/team/features/FEAT-001/research.md
check "stop: research with Sources allows stop"  0 stop-check.sh '{"hook_event_name":"Stop","stop_hook_active":false}'

# parallel waves: per-feature build flag; researcher's feature comes from its transcript, not current.json
jq '.cmd.lint="false"' .team/profile.json > .team/p && mv .team/p .team/profile.json
touch .team/active-build-FEAT-009
check "stop: per-feature active-build-<ID> runs the build checks" 2 stop-check.sh "$(jq -nc --arg c "$P" '{hook_event_name:"SubagentStop",stop_hook_active:false,cwd:$c,agent_type:"team:dev"}')"
rm .team/active-build-FEAT-009; jq '.cmd.lint="true"' .team/profile.json > .team/p && mv .team/p .team/profile.json
echo '{"feature":"FEAT-002","stage":"analyze"}' > .team/current.json
mkdir -p docs/team/features/FEAT-003; printf '# Research

## Sources
(none yet)
' > docs/team/features/FEAT-003/research.md
printf '%s\n' '{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Write","input":{"file_path":"docs/team/features/FEAT-003/research.md"}}]}}' > "$P/.team/tr.jsonl"
rs() { jq -nc --arg t "$P/.team/tr.jsonl" '{hook_event_name:"SubagentStop",stop_hook_active:false,agent_type:"team:researcher",agent_transcript_path:$t}'; }
check "stop: parallel researcher, its feature (transcript) lacks URL → blocked" 2 stop-check.sh "$(rs)"
printf '# Research

## Sources
- https://docs.python.org/3/ (2026-11-11)
' > docs/team/features/FEAT-003/research.md
check "stop: parallel researcher, its feature has Sources → allowed" 0 stop-check.sh "$(rs)"
check "role: tech-lead touch .team/active-build-<ID> allowed" 0 role-policy.sh "$(b 'touch .team/active-build-FEAT-003' team:tech-lead)"
check "role: tech-lead rm -f .team/active-build-<ID> allowed" 0 role-policy.sh "$(b 'rm -f .team/active-build-FEAT-003' team:tech-lead)"
rm -f "$P/.team/tr.jsonl"

# session-start.sh never creates .team/ in a repo nobody took over; refreshes plugin_root in a team project
mkdir -p "$T/other" && (cd "$T/other" && git init -q -b main)
ss() { (cd "$1" && CLAUDE_PROJECT_DIR="$1" CLAUDE_PLUGIN_ROOT="$KIT" bash "$KIT/scripts/session-start.sh" <<<'{"source":"startup","session_id":"s1"}'); }
out="$(ss "$T/other")"
if [[ ! -e $T/other/.team && $out == *"not onboarded"* ]]; then pass=$((pass + 1)); echo "ok   session-start: no .team/ in a foreign repo";
else failn=$((failn + 1)); echo "FAIL session-start: created .team/ in a foreign repo or no hint"; fi
rm -f "$P/.team/plugin_root"; ss "$P" >/dev/null
if [[ $(cat "$P/.team/plugin_root" 2>/dev/null) == "$KIT" ]]; then pass=$((pass + 1)); echo "ok   session-start: plugin_root refreshed in a team project";
else failn=$((failn + 1)); echo "FAIL session-start: plugin_root not written in a team project"; fi

check "role-policy: team-leader K=\$(cat .team/plugin_root); team.py status is read-only" 0 role-policy.sh "$(b 'K=$(cat .team/plugin_root); python3 "$K/scripts/team.py" status' team:team-leader)"
check "role-policy: team-leader git reflog is read-only" 0 role-policy.sh "$(b 'git reflog -5' team:team-leader)"
check "role-policy: team-leader ps is read-only"         0 role-policy.sh "$(b 'ps -eo pid,cmd' team:team-leader)"
check "role-policy: team-leader other substitution still flagged (block mode)" 2 role-policy.sh "$(b 'echo $(rm -rf x)' team:team-leader)"
# default "warn" mode: the same violations only remind (exit 0 + additionalContext / systemMessage)
jq '.enforcement = "warn"' .team/config.json > .team/c.tmp && mv .team/c.tmp .team/config.json
check "warn mode: push origin main runs, reminded"       0 check-git.sh "$(b 'git push origin main')"
check "warn mode: edit .team/profile.json runs"           0 protect.sh "$(w Edit "$P/.team/profile.json")"
check "warn mode: rm of protected path runs"             0 protect.sh "$(b 'rm .claude/settings.json')"
check "warn mode: team-leader non-read-only Bash runs"    0 role-policy.sh "$(b 'python3 -c "print(1)"' team:team-leader)"
out="$(CLAUDE_PROJECT_DIR="$P" bash "$KIT/scripts/check-git.sh" <<<"$(b 'git push origin main')" 2>/dev/null)"
if jq -e '.hookSpecificOutput.additionalContext | test("RULE \\(reminder")' <<<"$out" >/dev/null; then pass=$((pass + 1)); echo "ok   warn mode: reminder reaches Claude as additionalContext";
else failn=$((failn + 1)); echo "FAIL warn mode: no additionalContext reminder — $out"; fi
jq 'del(.enforcement)' .team/config.json > .team/c.tmp && mv .team/c.tmp .team/config.json
check "no enforcement key = warn: push origin main runs" 0 check-git.sh "$(b 'git push origin main')"
jq '.enforcement = "block"' .team/config.json > .team/c.tmp && mv .team/c.tmp .team/config.json

echo "test_hooks: $pass passed, $failn failed"
(( failn == 0 ))
