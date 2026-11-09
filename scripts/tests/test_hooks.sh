#!/usr/bin/env bash
# test_hooks.sh — đưa JSON hook giả vào protect.sh, check-git.sh, role-policy.sh, stop-check.sh và kiểm mã thoát.
set -uo pipefail
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
pass=0; failn=0
check() { # check <tên> <mã mong đợi> <script> <json> [--root dir]
  local name=$1 want=$2 script=$3 json=$4; shift 4
  local got err
  err="$(CLAUDE_PROJECT_DIR="$T/p" bash "$KIT/scripts/$script" "$@" <<<"$json" 2>&1 >/dev/null)"; got=$?
  if [[ $got == "$want" ]]; then pass=$((pass + 1)); echo "ok   $name (exit $got)";
  else failn=$((failn + 1)); echo "FAIL $name: want $want got $got — ${err:0:200}"; fi
}
mkdir -p "$T/p/.team" "$T/p/src" "$T/p/tests" "$T/p/docs/team/features/FEAT-001"
cd "$T/p" && git init -q -b main && git -c user.name=t -c user.email=t@t commit -q --allow-empty -m init && git switch -q -c team/FEAT-001-x
cp "$KIT/profiles/python.json" .team/profile.json
cp "$KIT/templates/project/team/config.json" .team/config.json
echo 'x = 1' > src/existing.py
P="$T/p"
w() { jq -nc --arg t "$1" --arg f "$2" '{hook_event_name:"PreToolUse", tool_name:$t, tool_input:{file_path:$f}}'; }
b() { jq -nc --arg c "$1" --arg cwd "$P" --arg a "${2:-}" '{hook_event_name:"PreToolUse", tool_name:"Bash", cwd:$cwd, tool_input:{command:$c}} + (if $a == "" then {} else {agent_type:$a} end)'; }

# protect.sh
check "protect: .env bị chặn"                    2 protect.sh "$(w Edit "$P/.env")"
check "protect: lockfile bị chặn"                2 protect.sh "$(w Write "$P/poetry.lock")"
check "protect: .git bị chặn"                    2 protect.sh "$(w Write "$P/.git/config")"
check "protect: settings.json bị chặn"           2 protect.sh "$(w Write "$P/.claude/settings.json")"
check "protect: file mới ngoài roots bị chặn"    2 protect.sh "$(w Write "$P/random/new.py")"
check "protect: file mới trong src cho qua"      0 protect.sh "$(w Write "$P/src/new.py")"
check "protect: sửa file có sẵn cho qua"         0 protect.sh "$(w Edit "$P/src/existing.py")"
check "protect: .team/profile.json bị chặn"     2 protect.sh "$(w Edit "$P/.team/profile.json")"
check "protect: .team/current.json cho qua"     0 protect.sh "$(w Write "$P/.team/current.json")"
check "protect: docs/team luôn cho qua"          0 protect.sh "$(w Write "$P/docs/team/features/FEAT-001/spec.md")"
check "protect: file mới trong worktree/tests qua" 0 protect.sh "$(w Write "$P/.claude/worktrees/agent-x/tests/test_new.py")"
check "protect: worktree/.env bị chặn"         2 protect.sh "$(w Write "$P/.claude/worktrees/agent-x/.env")"
check "protect: worktree/random bị chặn"       2 protect.sh "$(w Write "$P/.claude/worktrees/agent-x/random/x.py")"
check "protect: ngoài dự án cho qua"             0 protect.sh "$(w Write "/tmp/elsewhere.txt")"
check "protect: CHANGELOG.md mới ở gốc cho qua"  0 protect.sh "$(w Write "$P/CHANGELOG.md")"

# check-git.sh
check "git: push origin main bị chặn"            2 check-git.sh "$(b 'git push origin main')"
check "git: push HEAD:main bị chặn"              2 check-git.sh "$(b 'git push origin HEAD:main')"
check "git: push team/x cho qua"                 0 check-git.sh "$(b 'git push -u origin team/FEAT-001-x')"
check "git: push không refspec trên team/* qua"  0 check-git.sh "$(b 'git push')"
check "git: push feature/y bị chặn (chỉ team/*)" 2 check-git.sh "$(b 'git push origin feature/y')"
check "git: push --force bị chặn"                2 check-git.sh "$(b 'git push --force origin team/FEAT-001-x')"
check "git: push -f bị chặn"                     2 check-git.sh "$(b 'git push -fu origin team/FEAT-001-x')"
check "git: push +refspec bị chặn"               2 check-git.sh "$(b 'git push origin +team/FEAT-001-x')"
check "git: push --delete bị chặn"               2 check-git.sh "$(b 'git push origin --delete team/old')"
check "git: push --tags cho qua"                 0 check-git.sh "$(b 'git push origin --tags')"
check "git: commit --no-verify bị chặn"          2 check-git.sh "$(b 'git commit --no-verify -m "feat(x): y (FEAT-001)"')"
check "git: commit -n bị chặn"                   2 check-git.sh "$(b 'git commit -n -m "x"')"
check "git: commit sai định dạng chỉ cảnh báo"   0 check-git.sh "$(b 'git commit -m "update stuff"')"
check "git: lệnh ghép && push main bị chặn"      2 check-git.sh "$(b 'git add . && git push origin main')"
check "git: filter-branch bị chặn"               2 check-git.sh "$(b 'git filter-branch --tree-filter x HEAD')"
git switch -q main
check "git: reset --hard trên main bị chặn"      2 check-git.sh "$(b 'git reset --hard HEAD~1')"
check "git: rebase -i trên main bị chặn"         2 check-git.sh "$(b 'git rebase -i HEAD~2')"
git switch -q team/FEAT-001-x
check "git: reset --hard trên team/* cho qua"    0 check-git.sh "$(b 'git reset --hard HEAD')"

# role-policy.sh
rw() { jq -nc --arg t "$1" --arg f "$2" --arg a "$3" '{tool_name:$t, agent_type:$a, tool_input:{file_path:$f}}'; }
ag() { jq -nc --arg s "$1" --arg a "$2" '{tool_name:"Agent", agent_type:$a, tool_input:{subagent_type:$s, prompt:"x"}}'; }
check "role: team-leader ghi docs/team qua"      0 role-policy.sh "$(rw Write "$P/docs/team/journal/FEAT-001.md" team:team-leader)"
check "role: team-leader ghi src bị chặn"        2 role-policy.sh "$(rw Write "$P/src/new.py" team:team-leader)"
check "role: dev ghi src qua"                    0 role-policy.sh "$(rw Write "$P/src/new.py" team:dev)"
check "role: reviewer ghi src bị chặn"           2 role-policy.sh "$(rw Edit "$P/src/existing.py" team:reviewer)"
check "role: reviewer ghi memory qua"            0 role-policy.sh "$(rw Write "$P/.claude/agent-memory/reviewer/notes.md" team:reviewer)"
check "role: team-leader bash chỉ-đọc qua"       0 role-policy.sh "$(b 'git log --oneline | head -n 5' team:team-leader)"
check "role: reviewer git worktree list qua"    0 role-policy.sh "$(b 'git worktree list' team:reviewer)"
check "role: reviewer git worktree add chặn"    2 role-policy.sh "$(b 'git worktree add x' team:reviewer)"
check "role: tech-lead cd rồi git qua"          0 role-policy.sh "$(b 'cd src && git status' team:tech-lead)"
check "role: reviewer \$(...) bị chặn"            2 role-policy.sh "$(b 'echo $(touch x)' team:reviewer)"
check "role: reviewer python3 -c bị chặn"        2 role-policy.sh "$(b 'python3 -c "open(1)"' team:reviewer)"
check "role: reviewer git -c pager bị chặn"      2 role-policy.sh "$(b 'git -c core.pager=sh log' team:reviewer)"
check "role: reviewer awk bị chặn"               2 role-policy.sh "$(b 'awk "BEGIN{system(1)}"' team:reviewer)"
check "role: tech-lead gọi dev (không tiền tố) qua" 0 role-policy.sh "$(ag dev team:tech-lead)"
check "role: tech-lead (cục bộ) gọi dev qua"     0 role-policy.sh "$(ag dev tech-lead)"
check "role: tech-lead team.py qua plugin_root"  0 role-policy.sh "$(b 'python3 "$(cat .team/plugin_root)/scripts/team.py" status FEAT-001' team:tech-lead)"
check "role: reviewer \$(cat khác) bị chặn"       2 role-policy.sh "$(b 'cat $(cat .env)' team:reviewer)"
check "role: team-leader rm bị chặn"             2 role-policy.sh "$(b 'rm -rf src' team:team-leader)"
check "role: team-leader chuyển hướng ra src chặn" 2 role-policy.sh "$(b 'echo x > src/a.py' team:team-leader)"
check "role: team-leader jq >> feedback qua"     0 role-policy.sh "$(b 'jq -nc {} >> docs/team/metrics/feedback.jsonl' team:team-leader)"
check "role: qa chạy lệnh kiểm tùy ý qua"        0 role-policy.sh "$(b 'python3 -c "print(1)"' team:qa)"
check "role: tech-lead chạy cmd.test qua"        0 role-policy.sh "$(b 'pytest -q tests/test_x.py' team:tech-lead)"
check "role: tech-lead curl bị chặn"             2 role-policy.sh "$(b 'curl https://example.com' team:tech-lead)"
check "role: tech-lead gọi team:dev qua"         0 role-policy.sh "$(ag team:dev team:tech-lead)"
check "role: tech-lead gọi team:qa bị chặn"      2 role-policy.sh "$(ag team:qa team:tech-lead)"
check "role: analyst gọi Explore qua"            0 role-policy.sh "$(ag Explore team:analyst)"
check "role: dev gọi agent bị chặn"              2 role-policy.sh "$(ag Explore team:dev)"
check "role: phiên không có agent_type qua"      0 role-policy.sh "$(jq -nc '{tool_name:"Bash", tool_input:{command:"rm -rf x"}}')"

# stop-check.sh
check "stop: stop_hook_active cho dừng"          0 stop-check.sh '{"hook_event_name":"Stop","stop_hook_active":true}'
check "stop: không active-build cho dừng"        0 stop-check.sh "$(jq -nc --arg c "$P" '{hook_event_name:"Stop",stop_hook_active:false,cwd:$c}')"
jq '.cmd.lint="false" | .cmd.typecheck=""' .team/profile.json > .team/p && mv .team/p .team/profile.json
touch .team/active-build; echo 'y = 2' > src/changed.py
check "stop: build có lint đỏ bị chặn"           2 stop-check.sh "$(jq -nc --arg c "$P" '{hook_event_name:"Stop",stop_hook_active:false,cwd:$c}')"
jq '.cmd.lint="true"' .team/profile.json > .team/p && mv .team/p .team/profile.json
check "stop: build sạch cho dừng"                0 stop-check.sh "$(jq -nc --arg c "$P" '{hook_event_name:"Stop",stop_hook_active:false,cwd:$c}')"
rm .team/active-build
echo '{"feature":"FEAT-001","stage":"research"}' > .team/current.json
printf '# Research\n\n## Sources\n(chưa có)\n' > docs/team/features/FEAT-001/research.md
check "stop: research thiếu URL bị chặn"         2 stop-check.sh '{"hook_event_name":"Stop","stop_hook_active":false}'
printf '# Research\n\n## Sources\n- https://docs.python.org/3/ (2026-11-09)\n' > docs/team/features/FEAT-001/research.md
check "stop: research có Sources cho dừng"       0 stop-check.sh '{"hook_event_name":"Stop","stop_hook_active":false}'

echo "test_hooks: $pass passed, $failn failed"
(( failn == 0 ))
