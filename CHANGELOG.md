# Changelog

Mọi thay đổi đáng kể của bộ kit được ghi ở đây.
Định dạng theo [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), phiên bản theo [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
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
