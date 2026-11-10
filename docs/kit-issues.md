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

