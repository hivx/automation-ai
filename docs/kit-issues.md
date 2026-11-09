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
| K-10 | minor | mở | feedback | Skill `feedback` nối `feedback.jsonl` bằng `jq >>`; ở `-p` có thể bị từ chối như K-04. | v0.2: `log-run.sh --feedback` ghi dòng góp ý. |
| K-11 | blocker | đã sửa | team.py | `- [x] **T1 — …**` (T in đậm) không được tính là task tick → status kẹt ở `planned`, team-leader không đi tiếp. | Regex task chấp nhận `*`, `_`, `` ` `` trước mã task; thêm ca thử. |
| K-12 | major | đã sửa | team-leader | team-leader vẫn ghi `current.json` và journal bằng `printf` trong Bash → bị từ chối ở `-p`; journal thiếu dòng. | Thân agent ghi rõ "(Write)" ở bước 4 và 7. |
| K-13 | major | đã sửa | role-policy | Lệnh chỉ-đọc bị chặn: reviewer `git worktree list`, `git ls-tree`; tech-lead `cd <worktree>`. | Thêm `cd` và git `ls-tree`, `for-each-ref`, `show-ref`, `worktree list` vào danh sách chỉ-đọc; ca thử. |
| K-14 | major | đã sửa | dev / worktree | Vòng sửa: dev mới nằm ở worktree khác, cố trỏ git vào worktree cũ → Claude Code từ chối. | dev bước 1: vòng sửa thì `git switch` nhánh task trong worktree của mình. |
| K-15 | major | mở | build / max_agents_per_feature | Cỡ S dùng 2 dev + 2 reviewer (1 vòng sửa) + analyst + tech-lead + qa > trần S = 3; SPEC nói cỡ S "verify tự động, không qa riêng" nhưng skill `verify` luôn fork sang qa. | v0.2: định nghĩa trần là số VAI khác nhau, không tính lần gọi lại trong vòng sửa; cỡ S verify chạy trong tech-lead. |
| K-16 | minor | mở | team-leader | Đọc `gates` trong config và nghĩ G1 áp cho cỡ S dù `team.py` báo READY. | Đã thêm cột "Cổng áp dụng" vào `team.py status`; theo dõi ở vòng sau. |
| K-17 | minor | đã sửa | gitignore.tmpl | `.claude/worktrees/` của subagent hiện là file untracked. | Thêm vào `gitignore.tmpl`. |
