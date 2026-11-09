---
name: clean
description: Dùng khi cần dọn dẹp không đổi hành vi một loại nợ: code chết, đặt tên, cấu trúc, phụ thuộc thừa, test mồ côi hoặc đơn giản hóa.
argument-hint: "<dead-code|naming|structure|deps|tests|simplify> [<đường dẫn>] [--decide]"
context: fork
agent: team:maintainer
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git *)
---

## Mục đích
Một loại dọn dẹp, có bằng chứng hành vi không đổi.

## Đầu vào
- `$ARGUMENTS`: loại (`dead-code` | `naming` | `structure` | `deps` | `tests` | `simplify`), phạm vi đường dẫn.
- `docs/team/debt.md`, `design.md` (playbook refactor), `.team/profile.json`.

## Điều kiện trước
Đúng MỘT loại; G2b đã duyệt khi bật. Kiểm: `python3 "$(cat .team/plugin_root)/scripts/team.py" status`.

## Các bước
1. Ghi `.team/current.json` {feature, stage: "clean", agent: "maintainer", started_at}.
2. Tạo nhánh `team/<ID>-clean-<kind>` từ `config.base_branch` (git).
3. Chạy `cmd.test` TRƯỚC; lưu số test và kết quả.
4. Dọn đúng loại đã chọn:
   - `dead-code`: chứng minh không còn ai gọi (Grep) trước khi xóa.
   - `naming`: theo `naming.*`; đổi mọi chỗ gọi.
   - `structure`: theo `structure.*`; chỉ di chuyển, không sửa logic.
   - `deps`: gỡ phụ thuộc không dùng qua trình quản lý gói, không sửa tay lockfile.
   - `tests`: test mồ côi chỉ xóa khi chứng minh không phủ hành vi nào.
   - `simplify`: bỏ nhánh chết, gộp trùng; deprecation có đường thay thế và hạn gỡ; log/metric không chứa dữ liệu nhạy cảm.
5. Chạy `cmd.test` SAU; số test và kết quả phải bằng trước (trừ test mồ côi đã chứng minh).
6. `cmd.lint`, `cmd.typecheck` sạch.
7. Commit bằng `/team:commit`; cập nhật `docs/team/debt.md`.

## Đầu ra
- Commit trên `team/<ID>-clean-<kind>`; `docs/team/debt.md`.
- Tin trả ≤ 10 dòng: loại, file đổi, đầu ra test trước và sau, nợ còn lại.

## Tiêu chí xong
- Hai đầu ra `cmd.test` (trước/sau) được dán và giống nhau.
- Diff chỉ có một loại dọn dẹp.

## Dấu hiệu sai
- "Tiện sửa một bug" → ghi `debt.md`.
- "Đổi tên khỏi chạy test" → chạy trước và sau.
- "Hai loại một PR cho đỡ" → tách.

## Lệnh tiếp theo
`/team:verify <ID>` (playbook refactor) hoặc `/team:pr <ID>`.
