# Changelog

Mọi thay đổi đáng kể của bộ kit được ghi ở đây.
Định dạng theo [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), phiên bản theo [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-11-09

Bản dùng được đầu tiên của plugin `team`. Đã chạy end-to-end trên dự án mẫu: takeover → G0 → onboard → một feature cỡ S (analyze → build → verify, dừng ở G4) → retro.

### Bộ kit gồm
- 13 agent (`agents/`), 26 skill (`skills/`), 16 playbook + 4 batch workflow (`workflows/`).
- Hook cho 8 sự kiện qua 9 script (`hooks/hooks.json`, `hooks/role-policy.json`); tổng 25 script bash/python3 stdlib trong `scripts/`.
- Sổ tay `handbook/STD.md`: 12 mảng, 86 quy tắc, checklist review (10) và nghiệm thu (6); `STD-short.md` sinh tự động.
- 6 profile (`_template`, python, node-ts, go, java-maven, flutter), 3 schema, 25 template artifact, 15 template dự án (CLAUDE.md, settings, rules, GitHub/GitLab CI, PR/issue, CODEOWNERS, gitignore).
- Test: 62 ca hook, 23 ca `team.py status`, 9 unit test `measure.py`; `validate.sh --strict` (gồm `audit-xref.py`) chạy trong CI.
- Eval cho 8 skill kỷ luật (`evals/`, `run-eval.sh`); kết quả trong `evals/RESULTS.md`.

### Hạn chế đã biết
- Mở (major): K-06 headless ở thư mục chưa được tin phải truyền `--allowedTools`; K-15 định nghĩa `max_agents_per_feature` và verify cỡ S; K-24 Bash của vai `bash: any` không qua `protect.sh`. Chi tiết và minor: `docs/kit-issues.md`.
- Ngôn ngữ văn xuôi là tiếng Việt; ngân sách chữ đếm theo âm tiết nên thân skill/agent còn ngắn (P7 sẽ nâng).
- Phạm vi v2 theo SPEC: GitLab CI đầy đủ (hiện là khung), scorecard nâng cao, canary tự động, đưa skill tạm lên kit, cấu hình MCP mẫu.

### Đã sửa khi chạy end-to-end (P6)
- Blocker: K-01 `cmd.test_one` sai chỗ thay (schema bắt `{file}`), K-02 cổng theo cỡ, K-03 quyền đọc kit lần đầu, K-11 task in đậm không được tính.
- Major: K-04/K-12 ghi file bằng Write, K-05 CHANGELOG ở gốc, K-13 lệnh chỉ-đọc bị chặn nhầm, K-14 worktree vòng sửa, K-20 eval ghi trong thư mục plugin, K-21..K-23 lỗ hổng chỉ-đọc, matcher cài cục bộ, vùng luôn-cho-ghi quá rộng.

### Added (P1–P5)
- Khung repo: manifest plugin `team` và marketplace `automation-ai`.
- `scripts/validate.sh` (kiểm tĩnh, `--strict`) và `scripts/install-local.sh` (cài cục bộ).
- `SPEC.md`, `README.md`, `CLAUDE.md`, tài liệu `docs/` và `docs/guides/`.
- CI `validate.yml` (tạm `continue-on-error` tới P4).
- Sổ tay kỹ thuật `handbook/STD.md` (12 mảng, 86 quy tắc, 2 checklist) và bản rút gọn sinh tự động `STD-short.md`.
- Phụ lục `tool-selection.md`, `tool-map.md`, `who-calls-whom.md`.
- Schema `profile.schema.json`, `config.schema.json`; `scripts/check-profile.py`; `scripts/gen-handbook-short.py`.
- Profile mẫu: `_template`, `python`, `node-ts`, `go`, `java-maven`, `flutter`; config mặc định `templates/project/team/config.json`.
- `validate.sh` kiểm bản rút gọn cũ/sửa tay và kiểm profile/config theo schema.
- 13 agent trong `agents/` (hợp đồng 8 mục, ≤ 350 từ) và skill `handbook`, `using-team`.
- `scripts/gen-team-table.py` sinh bảng vai trong `docs/02-team.md`; `scripts/allowed-tools.txt`.
- `validate.sh` kiểm agent: tiền tố mô tả, tool trong allowlist, 8 tiêu đề đúng thứ tự, ngân sách chữ, bảng vai đồng bộ.
- 16 playbook, `workflows/README.md` (bảng tín hiệu → playbook) và 4 batch workflow.
- 24 skill còn lại; `skills/README.md`, `docs/guides/want-x-type-y.md`, `docs/guides/decision-tree.md` sinh bằng `scripts/gen-guides.py`.
- Khe config mới `limits.max_temp_skills` (mặc định 5).
- `validate.sh --strict` bắt buộc trong CI; kiểm cấu trúc skill/playbook, `agent: team:<vai>`, đường dẫn kit (`scripts/pending-paths.txt`).
- Hook `hooks/hooks.json` + `hooks/role-policy.json`; script `lib.sh`, `teamlib.py`, `protect.sh`, `check-git.sh`, `role-policy.sh`, `format.sh`, `stop-check.sh`, `check-structure.sh`, `session-start.sh`, `handoff.sh`, `log-session.sh`, `scorecard.sh`, `log-run.sh`, `detect-stack.sh`, `explore-cache.sh`, `render.py`, `team.py`, `measure.py`.
- 22 template artifact, `stage-result.json`, template dự án (CLAUDE.md, settings, rules, GitHub/GitLab CI, PR/issue, CODEOWNERS, gitignore).
- Test `scripts/tests/` (hook, team.py status, measure.py) chạy trong `validate.sh --strict` và CI.
- `install-local.sh` nối hook và bỏ tiền tố plugin khi cài cục bộ.
