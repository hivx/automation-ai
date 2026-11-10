# Vấn đề của bộ kit (v0.1.0)

Nguồn: chạy end-to-end P6 trên dự án mẫu `sample-existing` (Python, 24 commit), `/team:audit-kit` trên chính repo kit, và `scripts/audit-xref.py`. Mức: **blocker** (đã sửa trong v0.1.0) · **major** · **minor**. Major/minor còn mở là backlog v0.2.

| ID | Mức | Trạng thái | Nơi | Hiện tượng | Xử lý |
|---|---|---|---|---|---|
| K-01 | blocker | đã sửa | takeover → profile-proposal | Đề xuất `cmd.test_one` với chỗ thay `{module}` và khe bịa `cmd.test_all`; onboard ghi nguyên vào profile; `stop-check.sh` chỉ thay `{file}` nên mọi task build sẽ bị chặn. | Schema bắt `cmd.test_one`/`cmd.format` chứa `{file}` (`check-profile.py` thêm `pattern`); template profile-proposal liệt kê đúng tên khe và luật `{file}`. Chạy lại takeover + onboard: `python3 -m unittest {file}`, profile hợp lệ. |
| K-02 | blocker | đã sửa | run | Việc cỡ S dừng ở G1 dù ADJ-09 bỏ G1 cho cỡ S: team-leader tự đọc `gates` trong config thay vì tin `team.py`. | Skill `run`: cổng CHỈ theo đầu ra `team.py`. |
| K-03 | blocker | đã sửa (P5) | onboard lần đầu | Phiên chưa có settings không đọc được thư mục kit. | `takeover`, `onboard` có `Read Glob` trong `allowed-tools`; `Read(//<kit>/**)` vào `settings.local.json`. |
| K-04 | major | đã sửa | handbook / headless | Ghi `current.json`, journal bằng chuyển hướng Bash bị từ chối ở `-p`; journal thiếu dòng cho lần gọi analyst. | Handbook: ghi file bằng Write/Edit; build ghi `diff.patch` bằng Write. |
| K-05 | major | đã sửa | protect.sh | Tạo `CHANGELOG.md` ở gốc bị chặn khi `.` không thuộc `allowed_new_file_roots`, trong khi DoD đòi CHANGELOG. | `protect.sh` luôn cho tạo `CHANGELOG.md` ở gốc; thêm ca thử. |
| K-06 | major | đã sửa (vòng 2) | headless / CI | Thư mục chưa được tin (workspace trust) thì `-p` bỏ qua `permissions.allow` của dự án; phải truyền `--allowedTools`. | Batch workflow, `team-feature.yml`, `weekly-retro` và `docs/08-channels.md` sinh `--allowedTools` từ `permissions.allow` của `.claude/settings.json` (jq), nên không chép tay lệnh stack. |
| K-07 | minor | đã sửa | takeover | Repo 11 file: T2 đọc trực tiếp, không qua Explore (có ghi lý do). | `tiers.md`: repo < 30 file được đọc trực tiếp ở T2, ghi rõ trong bảng tầng. |
| K-08 | minor | đã sửa (vòng 2) | takeover | Đếm sai số dòng CLAUDE.md (116 thay vì 120). | `detect-stack.sh` in `ai_files` (số dòng CLAUDE.md, AGENTS.md, .claude/CLAUDE.md, CLAUDE.local.md do máy đếm); takeover lấy số từ đó. |
| K-09 | minor | đã sửa (vòng 2) | onboard | AI-readiness `clean-first` nhưng onboard vẫn chạy khi G0 đã duyệt, chỉ nhắc viết lại CLAUDE.md ở việc tay. | onboard đọc dòng `Verdict:` của ai-readiness: `clean-first` → dừng trước mọi ghi, hỏi xác nhận riêng hoặc chạy lại với `--accept-clean-first`; luôn đóng `stage: idle`. |
| K-10 | minor | đã sửa (P7) | feedback | Skill `feedback` nối `feedback.jsonl` bằng `jq >>`; ở `-p` có thể bị từ chối như K-04. | v0.2: `log-run.sh --feedback` ghi dòng góp ý. |
| K-11 | blocker | đã sửa | team.py | `- [x] **T1 — …**` (T in đậm) không được tính là task tick → status kẹt ở `planned`, team-leader không đi tiếp. | Regex task chấp nhận `*`, `_`, `` ` `` trước mã task; thêm ca thử. |
| K-12 | major | đã sửa | team-leader | team-leader vẫn ghi `current.json` và journal bằng `printf` trong Bash → bị từ chối ở `-p`; journal thiếu dòng. | Thân agent ghi rõ "(Write)" ở bước 4 và 7. |
| K-13 | major | đã sửa | role-policy | Lệnh chỉ-đọc bị chặn: reviewer `git worktree list`, `git ls-tree`; tech-lead `cd <worktree>`. | Thêm `cd` và git `ls-tree`, `for-each-ref`, `show-ref`, `worktree list` vào danh sách chỉ-đọc; ca thử. |
| K-14 | major | đã sửa | dev / worktree | Vòng sửa: dev mới nằm ở worktree khác, cố trỏ git vào worktree cũ → Claude Code từ chối. | dev bước 1: vòng sửa thì `git switch` nhánh task trong worktree của mình. |
| K-15 | major | đã sửa (P7) | build / max_agents_per_feature | Cỡ S dùng 2 dev + 2 reviewer (1 vòng sửa) + analyst + tech-lead + qa > trần S = 3; SPEC nói cỡ S "verify tự động, không qa riêng" nhưng skill `verify` luôn fork sang qa. | P7: trần = số VAI khác nhau team-leader tự gọi (kể cả skill fork), không tính dev/reviewer do tech-lead gọi và lần gọi lại; cỡ S = analyst, tech-lead, qa = 3. qa vẫn nghiệm thu cỡ S (bước kiểm tự động thu gọn). |
| K-16 | minor | đã sửa (P7) | team-leader | Đọc `gates` trong config và nghĩ G1 áp cho cỡ S dù `team.py` báo READY. | Đã thêm cột "Cổng áp dụng" vào `team.py status`; theo dõi ở vòng sau. |
| K-17 | minor | đã sửa | gitignore.tmpl | `.claude/worktrees/` của subagent hiện là file untracked. | Thêm vào `gitignore.tmpl`. |
| K-18 | minor | mở | scorecard.sh | `result` đoán từ chữ trong tin cuối: dev ghi `DESIGN_CONFLICT`, Explore ghi `approve` chỉ vì có từ đó. | v0.2: vai trả dòng JSON theo `stage-result.json`; scorecard đọc trường `verdict`. |
| K-19 | minor | đã sửa (P7) | team-leader | Có feature chờ G4 thì team-leader từ chối nhận yêu cầu mới (cổng chặn feature, không chặn cả đội). | v0.2: ghi rõ trong team-leader/intake: cổng chỉ chặn feature của nó. |
| K-20 | major | đã sửa | evals/run-eval.sh | Bản sao dự án nằm trong thư mục kit (plugin) → Claude Code từ chối ghi ("sensitive file"); kết quả with-skill vô giá trị. | Bản sao chuyển ra `$EVAL_WORK_ROOT` ngoài kit; chạy lại. |

## Từ `/team:audit-kit` chạy trên chính kit (2026-11-09, coach, $1.48)
Kết quả: 7 cao, 7 trung bình, 5 thấp. Báo cáo không ghi được vào repo kit (cùng nguyên nhân K-20: thư mục plugin), nên được chép vào đây.

| ID | Mức | Trạng thái | Nơi | Hiện tượng | Xử lý |
|---|---|---|---|---|---|
| K-21 | major | đã sửa | teamlib.py (chỉ-đọc) | `$(…)`, backtick, `python3 -c`, `bash -c`, `git -c core.pager=…`, `git diff --output`, `awk system()`, `sed --in-place`, `find -fprint` lọt qua kiểm chỉ-đọc. | Chặn các dạng đó cho vai chỉ-đọc; bỏ `awk` khỏi danh sách; ca thử. |
| K-22 | major | đã sửa | hooks.json / teamlib.py | Cài cục bộ bỏ tiền tố `team:` nhưng matcher SubagentStop và kiểm Agent vẫn đòi tiền tố → stop-check không chạy cho dev; tech-lead bị chặn gọi `dev`. | Matcher `^(team:)?(dev\|maintainer\|researcher)$`; chuẩn hóa `subagent_type`; ca thử. |
| K-23 | major | đã sửa | protect.sh | `.team/*`, `.claude/*` luôn cho ghi → dev sửa được `profile.json` (đổi lệnh test mà stop-check chạy). | Chỉ cho `docs/team/**`, `.team/**` trừ profile/config (chỉ lúc onboard), `.claude/{agent-memory,skills,agents,rules}/**`; ca thử. |
| K-24 | major | đã sửa (vòng 2) | hooks.json | `protect.sh` không gắn vào Bash: vai `bash: any` (dev, maintainer, devops, qa) sửa được `protected_paths` bằng shell (`>`, `tee`, `cp`, `sed -i`). | `protect.sh` gắn thêm vào PreToolUse Bash cho mọi vai và phiên chính: `teamlib.protect_bash` nhận đích ghi của chuyển hướng, `tee`, `rm`/`touch`/`truncate`/`mkdir`, `mv` (cả nguồn), `cp`/`install`/`ln`, `sed -i`, `chmod`, `dd of=`; chặn `.git/`, settings, profile/config (ngoài onboard), `protected_paths`. Không thấy được ghi bên trong script khác hay đường dẫn chứa biến shell (ghi trong `docs/06-install.md`); 10 ca thử. |
| K-25 | minor | mở | 18 skill | `Bash(python3 *)` trong `allowed-tools` cho phép mọi `python3 -c`. | v0.2: thu hẹp về đúng script của kit. |
| K-26 | minor | đã sửa (vòng 2) | onboard | Ngoại lệ onboard cho `cp *` không kiểm vùng cấm. | Ngoại lệ onboard đổi `cp *` thành `cp-from-kit-templates`: mọi nguồn phải nằm dưới `<kit>/templates/`; 3 ca thử. |
| K-27 | minor | đã sửa (vòng 2) | coach.md / audit-kit / role-policy | Danh sách ghi của coach lệch giữa ba nơi; coach dừng khi thiếu `runs.jsonl` trong khi audit-kit vẫn cho chạy kiểm tĩnh. | Một danh sách ghi của coach trong `agents/coach.md` = `role-policy.json` (ADJ-23); audit-kit chạy kiểm tĩnh khi thiếu số liệu, retro thì dừng (đầu vào theo chế độ ở mục 2 của coach). |
| K-28 | minor | đã sửa (vòng 2) | docs/01-process.md / team-feature.yml | Nhãn `team:decide`, `team:size:*` được nhắc trong docs nhưng workflow không đọc. | `team-feature.yml` đưa danh sách nhãn vào prompt: `team:size:*` → `--size`, `team:decide` → `--decide`. |
| K-29 | minor | đã sửa | teamlib.py | So khớp `cmd.*` không có ranh giới từ (`pytest` khớp `pytestfoo`). | Đòi khoảng trắng sau tiền tố. |
| K-30 | minor | đã sửa (vòng 2) | hooks.json | Hook format không áp cho NotebookEdit. | PostToolUse `format.sh` áp cả NotebookEdit (đọc `notebook_path`). |
| K-31 | minor | đã sửa | evals/config.json | `Bash(bash *)` ≈ Bash không giới hạn. | Thay bằng `Bash(bash <kit>/scripts/*)` do run-eval thêm. |

## Từ eval và kiểm cài đặt (2026-11-09)
| ID | Mức | Trạng thái | Nơi | Hiện tượng | Xử lý |
|---|---|---|---|---|---|
| K-32 | major | đã sửa | install-local.sh | Cài cục bộ bỏ tiền tố → skill thành `/status`, `/run`, `/verify`, `/feedback`, trùng tên lệnh/skill có sẵn của Claude Code. | Skill cục bộ đổi thành `team-<tên>`; `team.py` in `/team-<tên>` khi kit nằm ở `.claude/team-kit`. |
| K-33 | minor | đã sửa (P7) | evals/using-team | Kịch bản 1 không phân biệt baseline/with-skill (check quá hẹp hoặc quá yếu). | P7: viết lại kịch bản và check. |
| K-34 | major | đã sửa (P7) | team-leader / build | Cỡ S: team-leader gọi thẳng dev, không qua `/team:build` → không có reviewer (vi phạm "luôn review"). | P7: team-leader cỡ S vẫn gọi `/team:build` (1 dev + reviewer). |

## Vòng 1 P7 — chạy lại end-to-end (2026-11-09)
Đã đóng nhờ viết lại skill/agent: K-10 (feedback ghi bằng Write), K-15 (trần vai = số vai khác nhau team-leader tự gọi; cỡ S: analyst, tech-lead, qa = 3), K-16/K-19 (cổng chỉ theo `team.py`, chỉ chặn feature của nó), K-33 (kịch bản using-team s1 có 5 check), K-34 (cỡ S qua `/team:build` có reviewer — xác nhận trong eval và end-to-end).

| ID | Mức | Trạng thái | Nơi | Hiện tượng | Xử lý |
|---|---|---|---|---|---|
| K-35 | blocker | đã sửa | handbook Acceptance checklist #5, verify, qa, spec template | qa trả `rework` dù 5/5 tiêu chí đạt vì DoD đòi As-Built, CHANGELOG, tài liệu người dùng — những thứ `/team:asbuilt` chỉ viết SAU G4. Vòng lặp không thoát được. | Checklist #5: phần DoD của build; phần sau G4 ghi chủ, `/team:release` kiểm lại; release thêm điều kiện CHANGELOG + tài liệu. Chạy lại verify trên mẫu. |
| K-36 | blocker | đã sửa | protect.sh / teamlib.relpath | Sau K-23, file MỚI trong worktree của dev (`.claude/worktrees/<n>/…`) bị chặn như nằm ngoài allowed roots (dev không ghi được báo cáo; file test mới cũng sẽ bị chặn). | Đường dẫn trong worktree được xét tương đối với worktree; 3 ca thử. |
| K-37 | blocker | đã sửa | teamlib role-policy (K-21) | Chặn `$(…)` cho vai chỉ-đọc cũng chặn lệnh của chính skill: `python3 "$(cat .team/plugin_root)/scripts/team.py" status`. | Chỉ thay đúng dạng `$(cat .team/plugin_root)` bằng đường dẫn kit; mọi thay thế khác vẫn bị chặn; 2 ca thử. |
| K-38 | minor | đã sửa (vòng 2) | coach / retro | Retro tạo 2 đề xuất (asbuilt, config-max-agents) dựa trên một feature; độ tin cậy thấp nhưng vẫn hợp lệ theo luật mới. | Luật mẫu tối thiểu trong retro/coach: ≥ 2 lần trên ≥ 2 feature, hoặc xu hướng ≥ 3 lượt → đề xuất; ít hơn (kể cả một lần vượt trần config) → mục `## Theo dõi`. Đề xuất ghi số feature, số lượt, độ tin cậy. |

### So sánh với lần chạy P6 (cùng dự án mẫu, cùng yêu cầu)
| Chỉ số | P6 (v0.1.0) | P7 vòng 1 | Ghi chú |
|---|---|---|---|
| Số lần `/team:run` để tới verify | 3 (2 lần dừng sai: G1 cỡ S; task in đậm) | 1 | K-02, K-11 không tái diễn |
| Dòng journal FEAT-001 | 4 (thiếu dòng analyst) | 6 (mỗi lần gọi có lý do trước) | Một số trường nhận xét còn "—" khi chưa có kết quả |
| Vai team-leader tự gọi / trần S | 5 vai, journal ghi sai "3" | 3 / 3 (analyst, tech-lead, qa) | Định nghĩa đếm mới (K-15) |
| Vòng rework | 1 | 0 (reviewer approve vòng 1) | — |
| Hook chặn nhầm | 3 (qa `python3 -c`, reviewer `git worktree list`, tech-lead `cd`) | 2 (K-36, K-37 — đều do sửa an toàn ở P6) → đã sửa | Ca thử mới chặn tái diễn |
| Phán quyết verify | accepted | rework (K-35) → sửa → chạy lại: `Verdict: accepted`, dừng ở G4 ($1.25) | Checklist #5 đạt với cách viết mới |
| Chi phí intake→verify | ≈ $3.9 (3 lần run) | $3.29 (intake $0.26 + run $3.03) | — |

## Từ `/team:audit-kit` trên v0.2.0 (2026-11-09, coach, $0.94)
11 vấn đề (4 cao, 3 trung bình, 4 thấp); không lệch tên, không cặp luật mâu thuẫn mới. Báo cáo không ghi được vào repo kit (như K-20), chép vào đây.

| ID | Mức | Trạng thái | Nơi | Hiện tượng | Xử lý |
|---|---|---|---|---|---|
| K-39 | major | đã sửa (vòng 2) | teamlib.py `is_readonly` / role-policy.json | Chỉ-đọc vẫn lọt: `sed 'e cmd'`, `sed 'w f'`, `sort -o f`, `uniq IN OUT`, `tree -o f`, `rg --pre cmd`; chuyển hướng `>&`, `<>` không được nhận; `mkdir` trong danh sách chỉ-đọc. | `is_readonly`: chặn `sed` có lệnh `e`/`w`/`W` hay cờ `s///e|w` và `-f`; `sort -o`, `uniq IN OUT`, `tree -o`, `rg --pre`, `date -s`, `file -C`; chuyển hướng `>&file`, `<>`; bỏ `mkdir` khỏi danh sách chỉ-đọc; 13 ca thử. |
| K-40 | major | đã sửa (vòng 2) | teamlib.py `readonly_scripts` | So theo tên file, không theo đường dẫn: `validate.sh`/`team.py` ở thư mục bất kỳ đều được coi là chỉ-đọc; `log-run.sh`, `validate.sh` có ghi file. | `readonly_scripts` thành bảng tên → đích ghi; script phải nằm đúng `<kit>/scripts/` (realpath, kit = thư mục của teamlib hoặc `.team/plugin_root`). `log-run.sh` và `team.py scorecard` chỉ chạy được khi vai được ghi `docs/team/metrics/**`; cấm `--root`; bỏ `gen-guides.py` (ghi docs của kit); 6 ca thử. |
| K-41 | major | đã sửa (v0.2.1) | check-git.sh / teamlib.py | `git -c core.hooksPath=/dev/null commit` bỏ qua hook commit; `git -c alias.x='!cmd'` chạy shell tùy ý. | Chặn `-c` với `alias.*`, `core.hooksPath`, `core.sshCommand`, `core.pager`, `core.editor`, `core.fsmonitor`, `diff.external`, `credential.helper`, và `--exec-path`; 3 ca thử. Thu hẹp `git *` trong allow-list: vòng sau. |
| K-42 | major | đã sửa (v0.2.1) | skills/takeover | `allowed-tools` còn `Bash(bash *)` (phiên chính không có `agent_type` nên role-policy không áp). | Thu hẹp về `Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/{detect-stack,explore-cache}.sh *)`. |
| K-43 | minor | đã sửa (vòng 2) | coach.md / audit-kit / role-policy | K-27 còn: danh sách ghi của coach lệch ba nơi; lần chạy này gặp đúng xung đột. | Như K-27; `team.py scorecard` chỉ chạy được khi vai được ghi `docs/team/metrics/scorecard.json`. |
| K-44 | minor | đã sửa (vòng 2) | skills/audit-kit | Chạy audit-kit ngay trong repo kit (`<kit>` = gốc dự án) thì báo cáo không ghi được về đúng chỗ. | audit-kit: `<kit>` trùng gốc dự án hoặc chứa nó → không ghi file, in các dòng theo cột của `docs/kit-issues.md`; template kit-issues dùng cùng cột và mức blocker/major/minor. |
| K-45 | minor | đã sửa (vòng 2) | docs/01-process.md | Ghi "cỡ S verify tự động" trong khi verify luôn fork qa (đúng với định nghĩa trần mới). | `docs/01-process.md`: cỡ S verify do qa, bước kiểm thu gọn, tính trong trần 3 vai. |
Cũng được audit nhắc lại (đã có): K-24, K-06, K-30, K-28.

## Vòng 2 P7 — đọc tham khảo và viết lại 21 mục (2026-11-10)
Tìm khi đọc tham khảo (`docs/research/kit-audit-round2.md`) và khi viết lại; mọi mục dưới đây có bằng chứng từ code hoặc lần chạy, không chỉ từ tài liệu.

| ID | Mức | Trạng thái | Nơi | Hiện tượng | Xử lý |
|---|---|---|---|---|---|
| K-46 | blocker | đã sửa | skills/architect, team.py | Chế độ `system` chỉ viết `docs/team/architecture.md`; `team.py` đọc cổng G2 của feature từ `arch-impact.md` → `approved(None)` sai → feature kẹt `WAITING_FOR_APPROVAL G2` mãi. | Chế độ `system` viết thêm `arch-impact.md` ngắn của feature (mục `## Chế độ system`), mang dòng duyệt G2. |
| K-47 | blocker | đã sửa | team.py | Playbook không có analyze (bug-fix, hotfix, refactor, dependency-upgrade, spike, ci-fix, docs-only) không bao giờ qua `specified`; refactor không có `tasks.md` nên không bao giờ `built` → `/team:verify` không chạy được. | `NO_SPEC_PLAYBOOKS`, `NO_PLAN_PLAYBOOKS` (ADJ-26); `/team:clean` ghi `tasks.md` T1 tick; 6 ca thử. |
| K-48 | major | đã sửa | role-policy (researcher) | POC "trong worktree" (SPEC §3) không làm được: researcher chỉ được ghi `docs/team/**`, đường dẫn trong worktree bị quy về cây chính. | `worktree_write` cho researcher: ghi mọi file trong `.claude/worktrees/<n>/` (ADJ-25); 3 ca thử. |
| K-49 | major | đã sửa | teamlib.role_policy | Agent tạm (make-agent) không có trong role-policy → không giới hạn đường dẫn, Bash, agent. | Vai `_temp` áp cho agent có dấu `team: temp`: Bash chỉ-đọc + git cơ bản + `cmd.*`, chỉ gọi Explore; 3 ca thử. make-agent cấm `permissionMode`/`hooks`/`mcpServers`. |
| K-50 | major | đã sửa | skills/session, handoff.sh | `session save` và hook PreCompact/SessionEnd ghi cùng `.team/session/<id>.md` → ghi chú tay bị ghi đè. | `save` ghi `notes-<ID>.md`; `session-start.sh` nhắc cả hai. |
| K-51 | minor | đã sửa | docs/05-tokens-and-memory.md | Ghi "hook SessionStart cảnh báo vượt `context_warn_pct`" nhưng không script nào đọc khe đó. | Sửa tài liệu: mức 1, session plan đặt điểm nén; không hook nào đo được % ngữ cảnh. |
| K-52 | major | đã sửa | analyst, architect, designer, writer | Không có Bash mà skill của họ chạy `team.py status`, `explore-cache.sh`; eval analyze s1 (2026-11-09) cho thấy analyst bỏ bước và không ghi `current.json` dù được phép. | Thêm `Bash` (role-policy giữ chỉ-đọc, ADJ-27); mục 1 của agent nêu đúng danh sách ghi. |
| K-53 | major | mở | profile.schema / release / devops | Không có khe cho lệnh deploy prod và rollback, nhưng release, devops, STD-OPS-1 cần chúng. | Tạm: lệnh nằm ở `docs/team/ci.md` mục Deploy, viết qua `/team:ci deploy-script` có PR (ADJ-24). Đề xuất khe mới (`deploy.prod`, `deploy.rollback`) cho người quyết — SPEC §13 cấm bịa khe. |
| K-54 | minor | đã sửa | ci, devops, ci-fix, ci.md | STD-CI-4 có 5 loại; skill/agent/playbook/template dùng 4 loại khác tên. | Thống nhất 5 loại STD-CI-4 ở mọi nơi. |
| K-55 | minor | đã sửa | team-ci.yml / ci | Đầu file "sửa profile rồi chạy lại onboard" mâu thuẫn `ci setup/add-stage`. | Đầu file mới: sinh bởi onboard hoặc `ci setup`; thêm bước qua `/team:ci add-stage` (PR riêng). |
| K-56 | major | đã sửa (vòng 2) | team-ci.yml | Khe `cmd.*` rỗng sinh bước `run: true` → xanh mà không kiểm. | Mẫu `team-ci.yml`: khe rỗng sinh `echo "::warning::cmd.<khe> chưa cấu hình …"` (cảnh báo hiện trên CI, không im lặng); ci/devops ghi "chưa cấu hình" trong `ci.md`. |
| K-57 | minor | đã sửa | batch/weekly-retro.md | Trỏ `team-ci.yml` cho bước cài plugin (không có ở đó); hai khóa `claude_args` trùng. | Cài plugin như `team-feature.yml`; một `claude_args` có `--allowedTools`. |
| K-58 | minor | đã sửa | clean / maintainer / verify | Nhánh `team/<ID>-clean-<kind>` (skill) khác `team/<ID>-<slug>` (agent), còn verify checkout `team/<ID>`. | Thống nhất `team/<ID>`; maintainer nhả nhánh (`git switch --detach`) cho qa. |
| K-59 | major | đã sửa | audit-kit | Kiểm "skill không dùng" sai: dòng SubagentStop có `skill: null`. | Kiểm D1 ghép skill fork với agent + stage; skill không ghi số liệu → "không có dữ liệu". |
| K-60 | minor | đã sửa | asbuilt / pr / mẫu PR | `pr` grep "bốn tiêu đề" chưa được định nghĩa; mẫu PR gộp ba ý vào một tiêu đề. | Mẫu PR: `## Feature`, `## Vì sao`, `## Đổi gì`, `## Cách kiểm`; pr grep đúng bốn tiêu đề. |
| K-61 | minor | đã sửa | release / asbuilt template | Ai viết dòng `Released:` lệch giữa skill và mẫu. | devops viết sau smoke prod xanh (cả hai nơi). |
| K-62 | minor | mở | role-policy (writer) | writer chỉ được ghi `docs/**` trong khi profile có khe `structure.docs` (P4). | writer dừng và báo khi `structure.docs` khác `docs/`; đọc khe trong teamlib ở vòng sau. |
| K-63 | minor | đã sửa | evals/make-skill | Kịch bản ghi "8 mục" và chỉ kiểm "file tồn tại". | Chuẩn skill tạm = 8 nội dung SPEC §9, 300–1.000 chữ; check phân biệt (evidence, ca từ chối). |
| K-64 | minor | đã sửa | make-agent | Ca thử `.claude/agents/<name>.tests.md` có thể bị nạp như agent. | Chuyển sang `docs/team/agents/<name>.tests.md`. |
| K-65 | minor | mở | role-policy (devops) | devops `write: *`, `bash: any` rộng hơn hợp đồng (SPEC §3 `Bash(gh, ci)`). | Agent nêu danh sách ghi; thu hẹp role-policy khi teamlib đọc được khe `structure.scripts`. |
| K-66 | minor | đã sửa | templates/artifacts/design.md | Bảng touchpoints có cột `task` → designer chia task thay tech-lead. | Cột "ghi chú" (vì sao chạm). |
| K-67 | minor | đã sửa | agents/writer | Đòi `acceptance.md` cả khi playbook docs-only/client-docs (không có nghiệm thu). | Đầu vào theo chế độ. |
| K-68 | minor | đã sửa | agents/researcher | Đòi `spec.md` trong khi dependency-upgrade, spike, integration đi từ intake. | Chấp nhận `intake.md` cho các playbook đó. |
| K-69 | minor | đã sửa | scripts/gen-guides.py | Ví dụ tin trả có dấu backtick lẻ trong mục Đầu ra làm bảng "muốn X gõ Y" sinh rác. | Bỏ khối code và không cho khớp qua dòng. |
| K-70 | major | đã sửa | skills/intake, using-team | `using-team` và team-leader đưa yêu cầu thô vào `/team:intake`, nhưng intake có `disable-model-invocation: true` → team-leader lúc tự làm intake (eval BEFORE), lúc dừng bắt người gõ lệnh (eval AFTER vòng 2: 2/5). | Bỏ `disable-model-invocation` khỏi intake (chỉ ghi `intake.md`, journal, `current.json`); SPEC §3: team-leader làm intake. |
| K-71 | minor | đã sửa | 16 skill/agent | End-to-end vòng 2: `bash "$(cat .team/plugin_root)/scripts/log-run.sh" …` bị Claude Code đòi duyệt ở `-p` (lệnh thay thế = "nhiều thao tác"), không phải do hook; số liệu build/verify không được ghi. | Skill/agent gõ `"<kit>/scripts/…"` với `<kit>` là đường dẫn đọc từ `.team/plugin_root`; handbook nói rõ. role-policy vẫn nhận dạng cũ (K-37). |
| K-72 | major | mở (giới hạn Claude Code, đã ghi) | make-skill, make-agent, evals/make-skill | Ở `-p`, ghi vào `.claude/skills/**` luôn bị từ chối, kể cả với `--allowedTools "Write(.claude/skills/**)"`, `Edit(...)`, `Edit` (thử 4 dạng, 2026-11-10). Eval make-skill s1 không chạy được nhánh tạo skill. | Hai skill nói rõ: chỉ tạo ở phiên tương tác (người duyệt lần ghi); headless thì in nội dung cho người tạo. Eval nhánh tạo phải chạy tay ở phiên tương tác. |
| K-73 | major | đã sửa | agents/team-leader, skills/intake | Eval using-team s1 (vòng 2, sau K-70): team-leader làm intake rồi dừng, in `/team:analyze` (3/5); lần chạy BEFORE thì đi hết chuỗi (5/5). Câu "in lệnh tiếp theo" ở intake bước 9 và team-leader bước 11 để mô hình tự chọn dừng hay đi tiếp. | team-leader bước 11: `READY` → đi tiếp như `/team:run --until-blocked`; chỉ dừng ở cổng, câu hỏi, chặn, trần, hoặc khi người gõ đúng một lệnh. intake bước 9 phân biệt người gõ lệnh và team-leader nhận yêu cầu thô. |

## Từ `/team:audit-kit` trong end-to-end vòng 2 (2026-11-10, coach, $2.21)
coach chạy trên dự án mẫu (kit ngoài gốc dự án → K-44 cho ghi file), làm tới S13 thì hết 40 lượt mà chưa viết báo cáo; các phát hiện dưới đây lấy từ bản ghi phiên (lệnh + đầu ra của coach) và được tái hiện bằng ca thử.

| ID | Mức | Trạng thái | Nơi | Hiện tượng | Xử lý |
|---|---|---|---|---|---|
| K-74 | major | đã sửa | skills/audit-kit | 17 kiểm không vừa 40 lượt; báo cáo viết một lần ở cuối nên hết lượt là mất hết. | Bước 2a: khung kit-issues trước, ghi sau mỗi nhóm kiểm, chạy lại làm tiếp kiểm "chưa chạy". |
| K-75 | major | đã sửa | teamlib.py (chỉ-đọc, chuyển hướng, lỗi) | Vẫn lọt với vai chỉ-đọc: tiền tố `GIT_EXTERNAL_DIFF=`, `GIT_CONFIG_*`, `BASH_ENV=`; `git grep --open-files-in-pager`; `sort -uo`, `sort --compress-program`; `sed --in=` (tên dài viết tắt của GNU); `cd src && echo x > docs/team/…` (đích chuyển hướng tính từ gốc, không theo `cd`); JSON hook hỏng hay thiếu `role-policy.json` → cho qua. `protect-bash` bỏ sót `sort -o` và `sed --in=`. | Tiền tố env chỉ cho danh sách an toàn (`LC_ALL`, `TZ`…), cấm `sudo`; chặn tên dài viết tắt (`--i…` của sed, `--o…`/`--com…` của sort, `--s…` của date, `--c…` của file) và cụm cờ ngắn có `o`; đích chuyển hướng tính theo `cd`; JSON hỏng hay thiếu luật → chặn (mã 2); `protect-bash` nhận đích `sort -o`; 14 ca thử. |
| K-76 | minor | mở | profiles/*.json | Không profile nào đưa cấu hình lint/typecheck/test hay workflow CI vào `protected_paths` → vai `bash: any` có thể nới cổng bằng cách sửa cấu hình. | Vòng sau: thêm mẫu thường gặp vào profile mẫu, cân nhắc devops cần sửa workflow (qua PR). |
| K-77 | minor | mở | role-policy (qa) | qa `bash: any` trong khi SPEC §3 không cho qa Write/Edit. | Giữ (qa cần chạy lệnh kiểm tùy ý); hợp đồng qa cấm sửa code/test; xem lại khi teamlib phân biệt được lệnh ghi. |
| K-78 | minor | đã sửa | SPEC §4 / docs/01-process.md | SPEC ghi cỡ S "verify (automated, no separate qa)"; kit cho qa nghiệm thu cỡ S mà không có ADJ. | ADJ-29. |
| K-79 | minor | mở | settings.json.tmpl / CI | Script bash của kit chỉ được cho phép trong `settings.local.json` (đường dẫn kit khác máy) → `--allowedTools` ở CI không gồm `bash <kit>/scripts/*` (`log-run.sh`). | Vòng sau: cho phép theo mẫu tên script, hoặc dùng `python3`/`team.py` cho ghi số liệu. |
| K-80 | minor | mở | skills/onboard | Trong phiên onboard, `cp` từ `<kit>/templates/` bị Claude Code đòi quyền ("sensitive file") dù kit là nguồn; onboard phải Write tay nội dung mẫu (A-01 của lần chạy). | Vòng sau: dùng `render.py --out` cho mọi mẫu (cả file không có `{{…}}`). |

### End-to-end vòng 2 so với vòng 1 (dự án mẫu mới `sample-e2e3`, cùng yêu cầu "Implement the feature the README promises", cỡ S, decide)
| Chỉ số | P7 vòng 1 (v0.2.0) | P7 vòng 2 (v0.3.0) | Ghi chú |
|---|---|---|---|
| Onboard với AI-readiness `clean-first` | chạy luôn (K-09) | dừng trước mọi ghi, nêu việc dọn; chạy lại với `--accept-clean-first` | K-09 đóng |
| Playbook do intake chọn | new-feature (FEAT-001) | bug-fix (BUG-001: README hứa, code thiếu — có lý do + phương án khác) | đi qua chuỗi không spec/plan → kiểm K-47 trên thực tế: `built` → `verified` |
| Số lần `/team:run` tới verify | 1 (+1 chạy lại verify sau K-35) | 1 | — |
| Dòng journal | 6 | 10 | mỗi lần gọi có lý do trước |
| Vai team-leader tự gọi / trần S | 3 / 3 | 2 / 3 (tech-lead, qa) | bug-fix không có analyze |
| Vòng rework | 0 | 1 (reviewer đòi đầu ra đỏ rồi xanh trong gói review) | đúng luật STD-TEST-1 |
| Hook chặn nhầm | 2 (K-36, K-37) | 0 — các chặn đều đúng (coach `for`, biến `$K` không giải được, tech-lead ghi file bằng `{ echo …}`); 1 lần Claude Code đòi duyệt `$(cat …)` (K-71, đã sửa) | — |
| Phán quyết verify | rework (K-35) → accepted | accepted lần đầu (7/7 tiêu chí), dừng ở G4 | — |
| Retro | 2 đề xuất từ 1 feature (K-38) | 0 đề xuất, 4 mục theo dõi (luật mẫu tối thiểu) | K-38 đóng |
| Audit-kit | 11 phát hiện | hết lượt ở S13 trước khi ghi (K-74); 7 phát hiện mới lấy từ bản ghi (K-75..K-80) | sửa K-74, K-75 trong vòng |
| Chi phí | intake→verify $3.29 | intake $0.20 + run $2.25 = $2.45; cả chuỗi $6.50 | — |


## Nghiệm thu theo tài liệu yêu cầu (2026-11-10, v0.3.0) — FAIL và PARTIAL
Phán quyết: TỪ CHỐI (`docs/acceptance/acceptance-2026-11-10.md`). Mỗi dòng một yêu cầu; bằng chứng đầy đủ trong `docs/acceptance/traceability-2026-11-10.md`.

- REQ-A2-2 (must, PARTIAL): Không tự deploy production khi cổng bật — Chỉ là hướng dẫn + team.py; không hook nào chặn lệnh deploy prod; role-policy devops `"write":["*"],"bash":"any"`
- REQ-A3-6 (must, PARTIAL): Việc nhỏ team-leader tự xử hoặc giao MỘT agent duy nhất — Cỡ S = analyst + tech-lead + qa (+dev, reviewer): theo ADJ-29/K-15, khác "một agent duy nhất"
- REQ-A3-9 (must, PARTIAL): Không lách cổng đang bật (điều không được sai phải là máy) — Tự duyệt cổng chỉ bị cấm bằng lời (team-leader.md:61); máy không chặn
- REQ-A4-6 (must, PARTIAL): Coach đầy đủ từ bản 1: đo bằng thuật toán, chẩn đoán 5 nguyên nhân, đề xuất có diff + eval, canary cỡ S; áp d… — Đề xuất là toàn văn overlay, không có diff; coach không chạy được eval (retro SKILL.md:15)
- REQ-B1-2 (must, PARTIAL): team-leader tools = Read, Grep, Glob, Bash(đọc), Agent, TaskCreate/Update, AskUserQuestion, Write(docs/team/*… — Thiếu TaskCreate/Update (ADJ-07), thêm Skill (ADJ-11); vùng ghi rộng hơn docs/team/**
- REQ-B1-4 (must, PARTIAL): team-leader: được làm (intake, playbook & cỡ, hỏi/quyết, gọi có lý do, giữ cổng, leo thang, journal, điều phố… — Thân không nói nâng/hạ cỡ giữa chừng (chỉ ở docs/01-process.md:33); skill tạm chỉ qua using-team/SKILL.md:18
- REQ-B1-5 (must, PARTIAL): tech-lead tools = Read, Grep, Glob, Bash(git, test), Agent, Edit(docs/team/**) — Thêm Write, Skill (ADJ-11); Bash giới hạn đúng tinh thần (git + cmd.*), thêm gh pr
- REQ-B1-8 (must, PARTIAL): coach tools = Read, Grep, Glob, Bash(đọc), Write(retro/**, proposals) — Thêm Skill và memory; vùng ghi mở rộng theo ADJ-23
- REQ-B1-11 (must, PARTIAL): analyst tools = Read, Grep, Glob, Agent(Explore), AskUserQuestion, Write(docs/team/**) — Bỏ AskUserQuestion (ADJ-01), thêm Bash (ADJ-27) và Skill; giới hạn Explore do hook giữ
- REQ-B1-14 (must, PARTIAL): researcher tools = Read, Grep, Glob, Bash, WebFetch, WebSearch, Agent, Write(docs/team/**) — Thêm Skill; Bash bị hẹp hơn bảng; ghi worktree POC (ADJ-25)
- REQ-B1-17 (must, PARTIAL): architect tools = Read, Grep, Glob, Agent, Write(docs/team/**) — Thêm Bash (ADJ-27) và Skill
- REQ-B1-20 (must, PARTIAL): designer tools = Read, Grep, Glob, Agent, Write(docs/team/**) — Thêm Bash (ADJ-27) và Skill
- REQ-B1-21 (must, PARTIAL): designer opus / high (sonnet cỡ S/M) / 40 — Không có bước nào (team-leader, using-team, design) truyền model sonnet: cỡ S/M vẫn chạy opus
- REQ-B1-23 (must, PARTIAL): dev tools = Read, Edit, Write, Grep, Glob, Bash — Chỉ thêm Skill (ADJ-11); isolation: worktree
- REQ-B1-26 (must, PARTIAL): reviewer tools = Read, Grep, Glob, Bash(đọc); memory: project — Chỉ thêm Skill; test_hooks.sh:77-108 nhiều ca chặn lệnh ghi của reviewer
- REQ-B1-29 (must, PARTIAL): qa tools = Read, Grep, Glob, Bash; memory: project — Thêm Write, Skill (ADJ-11); bash any nên lệnh shell có thể sửa code (chỉ văn bản cấm)
- REQ-B1-32 (must, PARTIAL): writer tools = Read, Grep, Glob, Write(docs/**, CHANGELOG) — Thêm Bash (ADJ-27), Skill; README thêm hợp lý vì có trong "Được làm"
- REQ-B1-35 (must, PARTIAL): maintainer tools = Read, Edit, Write, Grep, Glob, Bash — Chỉ thêm Skill (ADJ-11)
- REQ-B1-38 (must, PARTIAL): devops tools = Read, Edit, Write, Grep, Glob, Bash(gh, ci) — Giới hạn Bash(gh, ci) không được máy thực thi; "chỉ sửa workflow CI" chỉ là văn bản
- REQ-B1-40 (must, PARTIAL): devops: dựng CI/CD, chẩn đoán đỏ (phân loại trước), script deploy/rollback/smoke, docs/team/ci.md / không xoá… — Thân tốt (838 chữ, 7 dòng); việc cấm deploy prod chỉ là văn bản, hook không chặn
- REQ-B2-3 (should, PARTIAL): Ma trận ai gọi ai viết rõ và nhất quán — Mâu thuẫn nội bộ; hook không chặn đường team-leader→dev
- REQ-B2-6 (must, PARTIAL): dev → tech-lead: file đã sửa, test kèm output thật, gì còn thiếu — Trường "còn thiếu gì" không nằm trong hợp đồng của dev
- REQ-B3-2 (must, PARTIAL): haiku cho triage / việc cơ học — Chỉ Explore có sẵn dùng haiku; không có đường haiku nào trong kit
- REQ-B3-5 (must, FAIL): Ghi đè models trong config có hiệu lực — Khóa trang trí: đổi config không đổi model nào
- REQ-C1-1 (must, PARTIAL): Tiếp nhận dự án: `/team:takeover`, team-leader (+Explore, researcher), 5 artifact assessment/ai-readiness/pro… — researcher không có vai nào trong skill (chỉ Explore); G0 không có trong team.py nên `/team:status` không hiện "chờ G0".
- REQ-C1-10 (must, PARTIAL): Phát hành: `/team:asbuilt`, `/team:pr`, `/team:release`; writer, tech-lead, devops; asbuilt/CHANGELOG/PR/depl… — G5 chỉ do skill/agent giữ (LLM); máy (team.py, hook) không chặn `Released:` khi thiếu duyệt prod.
- REQ-C1-11 (must, PARTIAL): Vận hành: `/team:intake --type bug`, `/team:clean`, `/team:ci`, `/team:retro`; team-leader, maintainer, devop… — clean/ci/retro có fork đúng vai; defects.md không có mẫu và không skill nào tạo.
- REQ-C3-1 (must, PARTIAL): S: diff một câu, ≤ 3 file, không đổi schema/API; intake → analyze rút gọn bỏ G1 → build 1 dev → verify tự độn… — Lệch tài liệu theo ADJ-29 (S vẫn fork qa); playbook new-feature/bug-fix vẫn ghi "không gọi qa riêng" → lệch nội bộ.
- REQ-C3-3 (must, PARTIAL): L: nhiều module, NFR mới, > 5 ngày; đủ 9 giai đoạn; kiến trúc bắt buộc; task đầu walking skeleton — Kiến trúc chỉ "bắt buộc" trong next_cmd; trạng thái cho đi qua và bỏ luôn G2; research cũng bị bỏ ở L (team.py:205).
- REQ-C3-6 (must, PARTIAL): Nâng/hạ cỡ giữa chừng ghi lý do vào `intake.md` — agents/team-leader.md không có bước áp dụng đổi cỡ và ghi vào intake.md; chỉ có chỗ trống trong mẫu.
- REQ-C4-6 (must, PARTIAL): Mục nhỏ → ghi `## Giả định tự quyết` — Đúng hành vi, sai tên tiêu đề so với tài liệu (S3 trong docs/acceptance/spec-vs-requirements.md).
- REQ-C4-10 (must, PARTIAL): Trong CI: câu hỏi → comment issue theo mẫu, label `team:needs-answer`, dừng `WAITING_FOR_ANSWER` — CI mặc định decide (chỉ ask khi có nhãn team:ask) nên đường hỏi trong CI hiếm khi chạy; live UNVERIFIED.
- REQ-C5-10 (must, FAIL): Hành vi: feature cỡ S chạy analyze → build (dev worktree, test hỏng trước, reviewer, finding có mã STD) → ver… — Nguyên nhân: REQ-E1-9
- REQ-C6-5 (must, PARTIAL): Dừng khi vượt `feature_budget_usd` — Không chỗ nào ghi chi phí theo feature, nên điều kiện không đo được; chỉ batch có `--max-budget-usd`.
- REQ-C7-4 (must, PARTIAL): Quét 4 tầng → báo cáo 3 câu → G0 → onboard; cỡ L; cổng G0 — Cỡ lệch (tài liệu: L).
- REQ-C7-6 (must, PARTIAL): intake → analyze → [research] → design → plan → build → verify → asbuilt → pr → release; M; G1, G3, G4 — Cỡ mặc định không phải M; dòng verify mâu thuẫn ADJ-29/verify skill.
- REQ-C7-7 (must, PARTIAL): analyze --amend → architect (impact) → plan (chèn) → build…; M; G1, G3 — team.py dẫn sang design, không sang architect impact rồi plan --insert như playbook; cổng thêm G2, G4.
- REQ-C7-8 (must, PARTIAL): intake(bug) → test fail trước → build (1 task) → verify → pr; S; G4 nếu M — G4 áp cả ở cỡ S (tài liệu: chỉ khi M); intake không tạo defects.md như bước 0 ghi.
- REQ-C7-9 (must, PARTIAL): intake(hotfix) → build tối thiểu từ prod → verify nhanh → pr → release prod (người duyệt) → bug-fix đầy đủ sa… — Tài liệu chỉ có G5; repo chặn thêm ở G4.
- REQ-C7-13 (must, FAIL): research (API, auth, giới hạn) → architect (impact) → design (contract, retry, idempotent) → plan → build → v… — team.py:89 thiếu integration trong NO_SPEC_PLAYBOOKS: không có spec.md thì kẹt ở intaken, `/team:run` lặp research.
- REQ-C7-16 (must, PARTIAL): analyze (đối tượng, phạm vi) → writer → review nội dung → pr; S/M; G1 rút gọn — Cỡ S mặc định làm mất G1 và team.py dẫn sang build thay vì writer (kiểm cỡ S ở team.py:203 trước client-docs ở :207).
- REQ-C8-14 (must, PARTIAL): Ghi rõ đã quét gì / chưa / độ tin cậy — Theo mẫu thì bước kiểm "grep -c 'Đã quét' ... mỗi file ≥ 1" của chính skill sẽ trượt.
- REQ-D1-3 (must, PARTIAL): Quy tắc ghi mức 3 thật sự do máy chặn — docs/03-handbook.md:39 tự đặt luật "mức 3 phải có hook thật"; 5 quy tắc vi phạm luật đó
- REQ-D1-4 (must, PARTIAL): Quy tắc mức 1 vi phạm ≥ 2 lần → coach đề xuất nâng mức — Không có cách đếm vi phạm theo từng mã/mức; một dòng, không phương pháp
- REQ-D2-2 (must, PARTIAL): STRUCT: file mới trong allowed_new_file_roots; test theo quy ước; không commit file sinh bởi tool; artifact đ… — Thiếu "artifact đúng tên"; "file sinh bởi tool" nằm ở GIT
- REQ-D2-3 (must, PARTIAL): NAME: theo profile + codebase; tên nói ý định; nhánh team/<ID>-<slug>; commit type(scope): mô tả (<ID>); test… — NAME-3 chỉ là tên file test
- REQ-D2-4 (must, PARTIAL): STYLE: formatter quyết; linter là luật; hàm ≤ 50 dòng, ≤ 4 tham số; không code chết; TODO có ID; comment nói … — Thiếu giới hạn hàm 50 dòng / 4 tham số và TODO có ID
- REQ-D2-5 (must, PARTIAL): DESIGN: phụ thuộc đi vào từ ngoài; không sửa thư viện bên thứ ba; không global state ẩn; đổi API/schema có de… — Thiếu "phụ thuộc vào từ ngoài" (DI) và "không global state ẩn"
- REQ-D2-6 (must, PARTIAL): TEST: fail trước (bug bắt buộc); một hành vi một test; không mock cái đang kiểm; không skip/xfail/only (block… — Thiếu "một hành vi một test", "không mock cái đang kiểm"; "mỗi task có test" chỉ gián tiếp
- REQ-D2-7 (must, PARTIAL): ERR: không nuốt exception; thông điệp hành động được; log có ngữ cảnh không bí mật; validate ở biên — "Lỗi có thông điệp hành động được" không có thành quy tắc
- REQ-D2-8 (must, PARTIAL): GIT: một task một PR nhỏ theo template; chỉ push team/*; không force-push; squash merge; commit không chứa fi… — Thiếu squash merge
- REQ-D2-9 (must, PARTIAL): CI: lint → typecheck → test → build → staging → smoke; đỏ không merge; prod cần người; không bí mật trong fil… — Thứ tự đủ 6 bước và "job có timeout" không là quy tắc STD; chỉ có trong template
- REQ-D2-12 (must, PARTIAL): DEP: ưu tiên thư viện đã có; pin + lockfile; không thêm thư viện cho việc < 50 dòng — Thiếu "ưu tiên thư viện đã có" thành quy tắc riêng
- REQ-D2-17 (must, PARTIAL): Hai checklist "dùng nguyên văn" — Mẫu PR là bản diễn lại, không nguyên văn, viết hai lần
- REQ-D2-18 (must, PARTIAL): Finding = mức / STD / file:line / mô tả / cách sửa; chỉ blocker/major; minor gộp 1 dòng — Định dạng chuẩn đúng; agent thêm cột thứ 6 và viết dòng minor khác mẫu
- REQ-D4-2 (must, PARTIAL): docs/ chỉ gồm tổng quan, cách cài, bản đồ việc → skill, lý do thiết kế; không viết tri thức hai lần — Tri thức quy trình chỉ có ở docs/ và nhiều đoạn viết hai lần
- REQ-E1-2 (must, PARTIAL): `test_one` bắt buộc — Khóa bắt buộc nhưng chuỗi rỗng vẫn qua; profiles/_template.json có test_one rỗng; build/handbook chỉ dừng bằng chữ
- REQ-E1-3 (must, PARTIAL): `{file}` là placeholder DUY NHẤT — Không cấm placeholder khác; stop-check chỉ thay `{file}` nên `{path}` sẽ lọt nguyên văn
- REQ-E1-4 (must, PARTIAL): protected_paths luôn có bí mật, lockfile, vendored, cấu hình prod — Mẫu tốt nhưng không có kiểm máy; teamlib.py:22 mặc định chỉ `.env`,`.env.*` khi thiếu profile; `.git/**` được nối thêm …
- REQ-E1-5 (must, PARTIAL): allowed_new_file_roots là danh sách đóng (doc gồm src, tests, docs, scripts, .github, .claude, .team) — Profiles bỏ `.github/` khỏi roots (doc có); onboard chỉ chạy được vì ghi qua `render.py`/`cp` bằng Bash mà hook không t…
- REQ-E1-7 (must, PARTIAL): Monorepo: profile gốc + `packages` ghi đè theo thư mục — Khai được nhưng không script/hook nào áp ghi đè theo thư mục
- REQ-E1-9 (must, FAIL): Hành vi: profile do takeover đề xuất và onboard ghi phải dùng được với script của kit (`naming.test_file` the… — Cùng lớp với K-01; schema không bắt mẫu
- REQ-E1-10 (must, PARTIAL): Hành vi: protected_paths của profile onboard có bí mật (`.env*`, thư mục secrets), lockfile, vendored, cấu hì… — Dự án mẫu không có lockfile/vendored
- REQ-E2-3 (must, FAIL): protected_branches = main, master, develop, release — Thiếu `develop`; `release` thành `release/*`
- REQ-E2-6 (must, FAIL): approvers mỗi cổng `["@owner"]` — Rỗng = không kiểm tên (release/SKILL.md:55 chỉ kiểm khi không rỗng)
- REQ-E4-2 (must, PARTIAL): deny: push nhánh bảo vệ, force-push, rm -rf, Edit protected_paths, Read .env* — Không có deny cho push nhánh bảo vệ; việc đó chỉ do hook check-git.sh chặn
- REQ-E4-4 (should, FAIL): `~/.claude/settings.json`: autoMemoryEnabled, plugin cá nhân — Không có hướng dẫn nào nói bật auto memory
- REQ-E4-5 (must, PARTIAL): Permission mode: plan ở phân tích/kiến trúc, acceptEdits ở build, dontAsk + allowlist ở CI/headless — Phần lớn chỉ có trong docs; plugin agent bỏ qua permissionMode
- REQ-E5-5 (should, PARTIAL): Theo nhu cầu: Playwright MCP (qa, ui), docs MCP (researcher), Sentry/Slack (devops, team-leader), tracker (in… — intake chỉ dùng gh
- REQ-E5-6 (should, PARTIAL): Không cài plugin trùng (superpowers, commit-commands, pr-review-toolkit), ẩn bằng skillOverrides; superpowers… — Thiếu câu về plugin-dev
- REQ-E5-7 (must, PARTIAL): Rule theo path nói khi nào dùng tool nào; skill nêu tool từng bước; agent chỉ tool của vai — Bảng tool có nhưng không gắn theo path
- REQ-F1-7 (must, PARTIAL): Mệnh lệnh: MỌI agent kiểm playbook/skill trước khi làm — Lệch "mọi agent"
- REQ-F1-8 (must, PARTIAL): Chấm artifact, gắn agent/skill → feedback.jsonl; mọi vai trò và người — reviewer/qa/coach không dùng được
- REQ-F1-18 (must, PARTIAL): Điều kiện → PR → CI → merge → staging → smoke → prod (G5); tech-lead, devops — Đủ quy trình; vai điều phối là team-leader chứ không phải tech-lead
- REQ-F1-28 (must, PARTIAL): description không tóm tắt quy trình — 2/26 kể chuỗi bước
- REQ-F1-30 (must, PARTIAL): Mỗi bước có checkpoint và điều kiện thoát — Có điều kiện dừng rải rác, không đều theo bước
- REQ-F1-31 (must, PARTIAL): Bảng anti-rationalization + red flags — 6 skill nạp thường xuyên không có red flags
- REQ-F1-33 (must, FAIL): Ngân sách chữ: skill hay nạp < 200 từ, khác < 500 — Repo theo P7 (CLAUDE.md luật 6), gấp 2–5 lần trần của tài liệu
- REQ-F1-35 (must, FAIL): Mỗi skill có eval baseline → with-skill trước khi phát hành — 17 skill không có eval; build, commit, pr, takeover chỉ có README chưa chạy
- REQ-F2-5 (must, FAIL): Hành vi: yêu cầu cần chuyên môn lặp ("6 màn hình CRUD giống nhau") → team-leader điều phối `/team:make-skill`… — team-leader coi là new-feature M, dừng G1
- REQ-F3-5 (must, PARTIAL): Phải có `## Nguồn` có URL — Hành vi có, nhưng tiêu đề là `## Sources` chứ không phải `## Nguồn`
- REQ-F5-1 (must, PARTIAL): Nạp lười, Explore, một phiên một feature, cảnh báo > context_warn_pct — Không có cảnh báo tự động
- REQ-F5-4 (must, PARTIAL): Dùng lại ≥ 2 hoặc đắt; kết luận không quá trình; ngày/version; trần kích thước và số file — Trần số file không được áp
- REQ-F5-5 (should, PARTIAL): Coach dọn định kỳ; prompt cache: prefix ổn định, không đổi model giữa phiên, fan-out cùng model/tool — Việc dọn memory/cache của coach không có trong agent hay skill
- REQ-F5-6 (must, PARTIAL): Hành vi: PreCompact/SessionEnd ghi `.team/session/<id>.md` ≤ handoff_max_lines, chỉ thông tin ngoài artifact;… — Nội dung bàn giao mỏng
- REQ-F6-2 (must, PARTIAL): gọi, turn, thời gian, rework/bác, STD vi phạm, token (log local), lần người can thiệp; so trung vị cùng cỡ — Không ai ghi std_violations/human_interventions vào runs.jsonl → luôn 0
- REQ-F6-4 (must, PARTIAL): Feedback tại chỗ; cảnh báo khi vượt ngưỡng 2 lần — Cảnh báo chỉ bằng chữ; 3 vai không ghi được feedback
- REQ-F6-6 (should, PARTIAL): Overlay header `# Overlay từ retro <date>: <lý do>` + version — Có header + version nhưng chữ là tiếng Anh, khác tài liệu
- REQ-F6-8 (must, PARTIAL): Số đo gọi thừa: agent/feature theo cỡ so max_agents_per_feature; retro định kỳ, kit-issues, audit-kit — Không có số đo tính bằng máy; retro/audit-kit có
- REQ-F6-9 (must, PARTIAL): Hành vi: `/team:retro` ra `retro/<date>.md` với ≥ 1 đề xuất có diff + eval + canary; không sửa agent/skill; d… — Định dạng đề xuất chưa kiểm được trên thực tế
- REQ-F6-10 (must, PARTIAL): Hành vi: lần chạy ghi `runs.jsonl` và `scorecard.json` — —
- REQ-G1-4 (must, PARTIAL): workflows/ 16 playbook + `lot/` (3–4 workflow kịch bản hoá) — Tên `batch/` theo SPEC.md:108, khác `lot/` của tài liệu
- REQ-G1-10 (must, PARTIAL): docs/00-tong-quan.md … 08-kenh-kich-hoat.md và docs/huong-dan/ (bat-dau-5-phut, muon-gi-go-gi, cay-quyet-dinh… — Nội dung khớp 1–1 nhưng tên tiếng Anh: theo A5 và SPEC.md:168, trái G1
- REQ-H1-3 (must, PARTIAL): Scheduled task: retro, clean-sweep định kỳ; webhook sau deploy → smoke; chỉ decide — Không có cơ chế/mẫu webhook sau deploy → smoke
- REQ-H1-4 (must, PARTIAL): Headless `claude -p` với `--bare --max-turns --max-budget-usd --output-format json`; bắt buộc decide — Lệch có chủ đích theo ADJ-03 (--bare tắt hook)
- REQ-H1-5 (must, PARTIAL): Projects (cloud): nhiều feature song song, duyệt ở "Waiting on you", hỏi trong thread — Không mô tả cách duyệt hay hỏi trong thread
- REQ-H3-1 (must, PARTIAL): Cú pháp Claude Code đổi: bắt tra docs + xác nhận phiên bản; phụ lục cú pháp dự phòng — Không kiểm phiên bản lúc chạy; phụ lục cú pháp chỉ trong automation-ai_prompts.md:217 (chưa track)
- REQ-H3-3 (must, PARTIAL): Khó kiểm hành vi: repo mẫu ở P6; evals skill kỷ luật; canary cỡ S — Repo mẫu không nằm trong kit; kết quả eval là lời khai chưa chạy lại
- REQ-H3-7 (must, PARTIAL): Memory tràn: tiêu chí đáng lưu; trần; coach dọn — Khóa explore_cache_max_files là cấu hình chết; coach chỉ dọn memory của chính mình, không dọn cache explore/research
- REQ-H3-8 (must, FAIL): Định danh tiếng Việt làm script lỗi: quy định ngôn ngữ; validate kiểm — Quy định có (CLAUDE.md luật 4) nhưng validate không kiểm ngôn ngữ định danh; key bị bắt chỉ nhờ additionalProperties
- REQ-I-3 (should, PARTIAL): Viết skill như TDD: baseline không skill → ghi lý do viện nguyên văn → skill tối thiểu → chạy lại; `evals/` — Không lưu lý do viện nguyên văn từ baseline; make-skill:13 mô tả cách viết kiểu kiểm thử
- REQ-I-5 (must, FAIL): Ngân sách chữ 200/500 — CHANGELOG.md:69 "Bỏ ngân sách cũ 200/500 chữ" (chuẩn P7); không có ADJ ghi điều này; cũng lệch SPEC.md:143
- REQ-J-5 (must, PARTIAL): Coach đầy đủ; evals cho skill kỷ luật; hướng dẫn người dùng; GitHub Actions template — Một phần do coach (REQ-A4-6)
- REQ-J-6 (should, PARTIAL): GitLab CI để bản 2 (không làm ở bản 1) — Lan phạm vi nhỏ: khung 15 dòng đã phát hành, có đánh dấu v2; tracker/ci enum có gitlab
