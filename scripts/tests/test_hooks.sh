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
check "git: -c core.hooksPath bị chặn"         2 check-git.sh "$(b 'git -c core.hooksPath=/dev/null commit -m x')"
check "git: -c alias.x=!cmd bị chặn"           2 check-git.sh "$(b "git -c alias.x='!rm -rf .' x")"
check "git: -c user.name hợp lệ qua"           0 check-git.sh "$(b 'git -c user.name=A log -1')"
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
# K-39: chỉ-đọc không được ghi/chạy lệnh
check "role: reviewer sed e cmd bị chặn"         2 role-policy.sh "$(b "sed '1e touch x' src/existing.py" team:reviewer)"
check "role: reviewer sed w file bị chặn"        2 role-policy.sh "$(b "sed -n 'w out.txt' src/existing.py" team:reviewer)"
check "role: reviewer sed s///e bị chặn"         2 role-policy.sh "$(b "sed 's/x/id/e' src/existing.py" team:reviewer)"
check "role: reviewer sed -n 1,20p qua"          0 role-policy.sh "$(b "sed -n '1,20p' docs/workflows.md" team:reviewer)"
check "role: reviewer sed s/a/b/g qua"           0 role-policy.sh "$(b "sed 's/x/y/g' src/existing.py" team:reviewer)"
check "role: reviewer sort -o bị chặn"           2 role-policy.sh "$(b 'sort -o src/a.py src/existing.py' team:reviewer)"
check "role: reviewer uniq IN OUT bị chặn"       2 role-policy.sh "$(b 'uniq src/existing.py src/b.py' team:reviewer)"
check "role: reviewer tree -o bị chặn"           2 role-policy.sh "$(b 'tree -o src/t.txt' team:reviewer)"
check "role: reviewer rg --pre bị chặn"          2 role-policy.sh "$(b 'rg --pre ./x foo' team:reviewer)"
check "role: reviewer >&file bị chặn"            2 role-policy.sh "$(b 'echo x >&src/a.py' team:reviewer)"
check "role: reviewer <> file bị chặn"           2 role-policy.sh "$(b 'cat <> src/a.py' team:reviewer)"
check "role: reviewer 2>&1 qua"                  0 role-policy.sh "$(b 'git log -1 2>&1 | head -n 3' team:reviewer)"
check "role: reviewer mkdir bị chặn"             2 role-policy.sh "$(b 'mkdir src/x' team:reviewer)"
# K-40: script của kit so theo đường dẫn
check "role: reviewer team.py của kit qua"       0 role-policy.sh "$(b "python3 $KIT/scripts/team.py status" team:reviewer)"
check "role: reviewer team.py lạ bị chặn"        2 role-policy.sh "$(b 'python3 /tmp/x/scripts/team.py status' team:reviewer)"
check "role: reviewer validate.sh lạ bị chặn"    2 role-policy.sh "$(b 'bash ./validate.sh' team:reviewer)"
check "role: reviewer log-run.sh (ghi) bị chặn"  2 role-policy.sh "$(b "bash $KIT/scripts/log-run.sh --skill x" team:reviewer)"
check "role: team-leader log-run.sh qua"         0 role-policy.sh "$(b "bash $KIT/scripts/log-run.sh --skill x" team:team-leader)"
check "role: team-leader log-run --root chặn"    2 role-policy.sh "$(b "bash $KIT/scripts/log-run.sh --root /tmp --skill x" team:team-leader)"
# K-24: lệnh shell ghi vùng cấm (mọi vai, cả bash: any)
check "protect-bash: dev echo > .env chặn"       2 protect.sh "$(b 'echo X=1 > .env' team:dev)"
check "protect-bash: dev sed -i lockfile chặn"   2 protect.sh "$(b "sed -i 's/a/b/' poetry.lock" team:dev)"
check "protect-bash: dev cp vào .env chặn"       2 protect.sh "$(b 'cp /tmp/x .env' team:dev)"
check "protect-bash: dev rm .env chặn"           2 protect.sh "$(b 'rm -f .env' team:dev)"
check "protect-bash: dev tee profile chặn"       2 protect.sh "$(b 'echo {} | tee .team/profile.json' team:dev)"
check "protect-bash: dev mv .git/x chặn"         2 protect.sh "$(b 'mv a .git/config' team:dev)"
check "protect-bash: cd rồi ghi .env chặn"       2 protect.sh "$(b 'cd src && echo x > ../.env' team:dev)"
check "protect-bash: dev ghi src qua"            0 protect.sh "$(b 'echo x > src/a.py && cp src/a.py src/b.py' team:dev)"
check "protect-bash: rm -rf build qua"           0 protect.sh "$(b 'rm -rf build dist' team:dev)"
check "protect-bash: 2>/dev/null qua"            0 protect.sh "$(b 'ls 2>/dev/null' team:dev)"
check "role: researcher ghi POC trong worktree qua" 0 role-policy.sh "$(rw Write "$P/.claude/worktrees/poc-x/src/poc.py" team:researcher)"
check "role: researcher ghi src cây chính chặn"  2 role-policy.sh "$(rw Write "$P/src/poc.py" team:researcher)"
check "role: researcher ghi research.md qua"     0 role-policy.sh "$(rw Write "$P/docs/team/features/FEAT-001/research.md" team:researcher)"
check "role: reviewer team.py scorecard chặn"    2 role-policy.sh "$(b "python3 $KIT/scripts/team.py scorecard" team:reviewer)"
mkdir -p "$P/.claude/agents"; printf -- '---\nname: ui-spec\n---\n<!-- team: temp, created 2026-11-10, need: x -->\n' > "$P/.claude/agents/ui-spec.md"
check "role: agent tạm curl bị chặn"              2 role-policy.sh "$(b 'curl https://x' ui-spec)"
check "role: agent tạm gọi dev bị chặn"           2 role-policy.sh "$(ag dev ui-spec)"
check "role: agent tạm chạy cmd.test qua"         0 role-policy.sh "$(b 'pytest -q tests/test_x.py' ui-spec)"
check "role: coach team.py scorecard qua"        0 role-policy.sh "$(b "python3 $KIT/scripts/team.py scorecard" team:coach)"
echo '{"feature":"","stage":"onboard"}' > "$P/.team/current.json"
check "role: onboard cp từ kit/templates qua"    0 role-policy.sh "$(b "cp $KIT/templates/project/gitignore.tmpl .gitignore.new" team:team-leader)"
check "role: onboard cp từ chỗ khác chặn (K-26)" 2 role-policy.sh "$(b 'cp /etc/passwd docs/x' team:team-leader)"
echo '{"feature":"","stage":"idle"}' > "$P/.team/current.json"
check "role: ngoài onboard cp từ kit chặn"      2 role-policy.sh "$(b "cp $KIT/templates/project/gitignore.tmpl .gitignore.new" team:team-leader)"
# audit-kit vòng 2 (K-75): tiền tố env, tên dài viết tắt, cd trước chuyển hướng, hỏng thì chặn
check "role: coach GIT_EXTERNAL_DIFF= chặn"       2 role-policy.sh "$(b 'GIT_EXTERNAL_DIFF=x git diff' team:coach)"
check "role: coach BASH_ENV= script kit chặn"      2 role-policy.sh "$(b "BASH_ENV=docs/team/retro/x.sh bash $KIT/scripts/check-structure.sh" team:coach)"
check "role: coach LC_ALL=C grep qua"              0 role-policy.sh "$(b 'LC_ALL=C grep -n x src/existing.py' team:coach)"
check "role: coach git grep --open-files-in-pager chặn" 2 role-policy.sh "$(b 'git grep --open-files-in-pager=x foo' team:coach)"
check "role: coach sort -uo chặn"                  2 role-policy.sh "$(b 'sort -uo out.txt in.txt' team:coach)"
check "role: coach sort --compress-program chặn"   2 role-policy.sh "$(b 'sort --compress-program=x in.txt' team:coach)"
check "role: coach sed --in=.bak chặn"             2 role-policy.sh "$(b 'sed --in=.bak s/a/b/ f.txt' team:coach)"
check "role: coach cd rồi > docs/team chặn"        2 role-policy.sh "$(b 'cd src && echo x > docs/team/retro/a.md' team:coach)"
check "role: coach ghi docs/team/retro qua"        0 role-policy.sh "$(b 'echo x > docs/team/retro/a.md' team:coach)"
check "role: date -Iseconds qua"                   0 role-policy.sh "$(b 'date -Iseconds' team:reviewer)"
check "role: JSON hỏng thì chặn"                   2 role-policy.sh '{not json'
check "protect-bash: sort -o .env chặn"            2 protect.sh "$(b 'sort -o .env in.txt' team:dev)"
check "protect-bash: sort -uo profile chặn"        2 protect.sh "$(b 'sort -uo .team/profile.json in.txt' team:dev)"
check "protect-bash: sed --in=.bak .env chặn"      2 protect.sh "$(b 'sed --in=.bak s/a/b/ .env' team:dev)"
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
