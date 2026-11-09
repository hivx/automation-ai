# Vấn đề của bộ kit (v0.1.0)

Nguồn: chạy end-to-end P6 trên dự án mẫu `sample-existing` (Python, 24 commit), `/team:audit-kit` trên chính repo kit, và `scripts/audit-xref.py`. Mức: **blocker** (đã sửa trong v0.1.0) · **major** · **minor**. Major/minor còn mở là backlog v0.2.

| ID | Mức | Trạng thái | Nơi | Hiện tượng | Xử lý |
|---|---|---|---|---|---|
| K-01 | blocker | đã sửa | takeover → profile-proposal | Đề xuất `cmd.test_one` với chỗ thay `{module}` và khe bịa `cmd.test_all`; onboard ghi nguyên vào profile; `stop-check.sh` chỉ thay `{file}` nên mọi task build sẽ bị chặn. | Schema bắt `cmd.test_one`/`cmd.format` chứa `{file}` (`check-profile.py` thêm `pattern`); template profile-proposal liệt kê đúng tên khe và luật `{file}`. Chạy lại takeover + onboard: `python3 -m unittest {file}`, profile hợp lệ. |
| K-02 | blocker | đã sửa | run | Việc cỡ S dừng ở G1 dù ADJ-09 bỏ G1 cho cỡ S: team-leader tự đọc `gates` trong config thay vì tin `team.py`. | Skill `run`: cổng CHỈ theo đầu ra `team.py`. |
| K-03 | blocker | đã sửa (P5) | onboard lần đầu | Phiên chưa có settings không đọc được thư mục kit. | `takeover`, `onboard` có `Read Glob` trong `allowed-tools`; `Read(//<kit>/**)` vào `settings.local.json`. |
| K-04 | major | đã sửa | handbook / headless | Ghi `current.json`, journal bằng chuyển hướng Bash bị từ chối ở `-p`; journal thiếu dòng cho lần gọi analyst. | Handbook: ghi file bằng Write/Edit; build ghi `diff.patch` bằng Write. |
| K-05 | major | đã sửa | protect.sh | Tạo `CHANGELOG.md` ở gốc bị chặn khi `.` không thuộc `allowed_new_file_roots`, trong khi DoD đòi CHANGELOG. | `protect.sh` luôn cho tạo `CHANGELOG.md` ở gốc; thêm ca thử. |
| K-06 | major | mở | headless / CI | Thư mục chưa được tin (workspace trust) thì `-p` bỏ qua `permissions.allow` của dự án; phải truyền `--allowedTools`. | v0.2: batch workflow và `team-feature.yml` sinh `--allowedTools` từ profile; tài liệu `08-channels.md` đã ghi. |
| K-07 | minor | đã sửa | takeover | Repo 11 file: T2 đọc trực tiếp, không qua Explore (có ghi lý do). | `tiers.md`: repo < 30 file được đọc trực tiếp ở T2, ghi rõ trong bảng tầng. |
| K-08 | minor | mở | takeover | Đếm sai số dòng CLAUDE.md (116 thay vì 120). | v0.2: `detect-stack.sh` báo số dòng CLAUDE.md/AGENTS.md (máy đếm, không phải LLM). |
| K-09 | minor | mở | onboard | AI-readiness `clean-first` nhưng onboard vẫn chạy khi G0 đã duyệt, chỉ nhắc viết lại CLAUDE.md ở việc tay. | v0.2: onboard đòi xác nhận riêng khi verdict là `clean-first`. |
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
| K-24 | major | mở | hooks.json | `protect.sh` không gắn vào Bash: vai `bash: any` (dev, maintainer, devops, qa) sửa được `protected_paths` bằng shell (`>`, `tee`, `cp`, `sed -i`). | v0.2: kiểm đích ghi của Bash cho mọi vai. |
| K-25 | minor | mở | 18 skill | `Bash(python3 *)` trong `allowed-tools` cho phép mọi `python3 -c`. | v0.2: thu hẹp về đúng script của kit. |
| K-26 | minor | mở | onboard | Ngoại lệ onboard cho `cp *` không kiểm vùng cấm. | v0.2: chỉ cho chép từ `<kit>/templates/`. |
| K-27 | minor | mở | coach.md / audit-kit / role-policy | Danh sách ghi của coach lệch giữa ba nơi; coach dừng khi thiếu `runs.jsonl` trong khi audit-kit vẫn cho chạy kiểm tĩnh. | v0.2: đồng bộ (sẽ làm khi viết lại coach ở P7). |
| K-28 | minor | mở | docs/01-process.md / team-feature.yml | Nhãn `team:decide`, `team:size:*` được nhắc trong docs nhưng workflow không đọc. | v0.2: workflow truyền nhãn vào prompt. |
| K-29 | minor | đã sửa | teamlib.py | So khớp `cmd.*` không có ranh giới từ (`pytest` khớp `pytestfoo`). | Đòi khoảng trắng sau tiền tố. |
| K-30 | minor | mở | hooks.json | Hook format không áp cho NotebookEdit. | v0.2: thêm hoặc ghi là cố ý. |
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
| K-38 | minor | mở | coach / retro | Retro tạo 2 đề xuất (asbuilt, config-max-agents) dựa trên một feature; độ tin cậy thấp nhưng vẫn hợp lệ theo luật mới. | Theo dõi ở vòng sau khi có ≥ 2 feature. |

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
| K-39 | major | mở | teamlib.py `is_readonly` / role-policy.json | Chỉ-đọc vẫn lọt: `sed 'e cmd'`, `sed 'w f'`, `sort -o f`, `uniq IN OUT`, `tree -o f`, `rg --pre cmd`; chuyển hướng `>&`, `<>` không được nhận; `mkdir` trong danh sách chỉ-đọc. | v0.2.x: chặn từng dạng, bỏ `mkdir`, ca thử cho mỗi dạng. |
| K-40 | major | mở | teamlib.py `readonly_scripts` | So theo tên file, không theo đường dẫn: `validate.sh`/`team.py` ở thư mục bất kỳ đều được coi là chỉ-đọc; `log-run.sh`, `validate.sh` có ghi file. | v0.2.x: so đường dẫn tuyệt đối dưới `<kit>/scripts/`; tách script có ghi. |
| K-41 | major | đã sửa (v0.2.1) | check-git.sh / teamlib.py | `git -c core.hooksPath=/dev/null commit` bỏ qua hook commit; `git -c alias.x='!cmd'` chạy shell tùy ý. | Chặn `-c` với `alias.*`, `core.hooksPath`, `core.sshCommand`, `core.pager`, `core.editor`, `core.fsmonitor`, `diff.external`, `credential.helper`, và `--exec-path`; 3 ca thử. Thu hẹp `git *` trong allow-list: vòng sau. |
| K-42 | major | đã sửa (v0.2.1) | skills/takeover | `allowed-tools` còn `Bash(bash *)` (phiên chính không có `agent_type` nên role-policy không áp). | Thu hẹp về `Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/{detect-stack,explore-cache}.sh *)`. |
| K-43 | minor | mở | coach.md / audit-kit / role-policy | K-27 còn: danh sách ghi của coach lệch ba nơi; lần chạy này gặp đúng xung đột. | Vòng 2 viết lại coach + audit-kit. |
| K-44 | minor | mở | skills/audit-kit | Chạy audit-kit ngay trong repo kit (`<kit>` = gốc dự án) thì báo cáo không ghi được về đúng chỗ. | Nhận dạng trường hợp này, in hướng dẫn chép vào `docs/kit-issues.md`. |
| K-45 | minor | mở | docs/01-process.md | Ghi "cỡ S verify tự động" trong khi verify luôn fork qa (đúng với định nghĩa trần mới). | Sửa văn bản ở vòng 2. |
Cũng được audit nhắc lại (đã có): K-24, K-06, K-30, K-28.
