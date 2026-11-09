---
name: plan
description: Dùng khi feature đã có spec và design được duyệt và cần chia thành task 2–5 phút có touchpoints, hoặc khi change-request cần chèn task mới (--insert).
argument-hint: "<ID> [--insert]"
context: fork
agent: team:tech-lead
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git branch *)
---

## Mục đích
Viết `plan.md` và `tasks.md` để dev làm từng task không cần hỏi lại.

## Đầu vào
- `$ARGUMENTS`: mã `<ID>`; `--insert` khi có amendment.
- `spec.md`, `design.md`, `arch-impact.md` nếu có; `.team/config.json` (`limits.max_parallel_dev`). `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
Cổng trước (G1, G2, G2b khi bật) đã duyệt. Kiểm: `python3 "$(cat .team/plugin_root)/scripts/team.py" status <ID>`.

## Các bước
1. Ghi `.team/current.json` {feature, stage: "plan", agent: "tech-lead", started_at}.
2. `plan.md` từ `<kit>/templates/artifacts/plan.md`: thứ tự, rủi ro, nhánh `team/<ID>`.
3. `tasks.md` từ `<kit>/templates/artifacts/tasks.md`; mỗi task một dòng, 2–5 phút:
   `- [ ] T<N> — <tên> — files: <touchpoints> — test: <file test> — depends: <T… hoặc —>`; tiêu chí trích spec ghi dòng con.
4. Cỡ L: T1 là walking skeleton chạy đầu-cuối.
5. Kiểm: mọi touchpoint trong `design.md` thuộc ít nhất một task; task nào > 5 phút thì chia.
6. Đánh dấu nhóm song song: hai task chung file → phụ thuộc nhau.
7. `--insert`: thêm task mới sau task cuối đã tick; task bị amendment ảnh hưởng ghi `[affected]`.
8. Tạo nhánh `team/<ID>` từ `config.base_branch` nếu chưa có (git).

## Đầu ra
- `docs/team/features/<ID>/plan.md`, `tasks.md`; nhánh `team/<ID>`.
- Tin trả ≤ 10 dòng: số task, nhóm song song, rủi ro, cổng G3.

## Tiêu chí xong
- Mỗi task có touchpoints, test file, tiêu chí; không task nào thiếu.
- Dán bảng touchpoint → task.

## Dấu hiệu sai
- "Task 'làm phần backend'" → chia tới 2–5 phút với file cụ thể.
- "Song song cho nhanh dù chung file" → nối phụ thuộc.
- "Bỏ walking skeleton" → cỡ L bắt buộc.

## Lệnh tiếp theo
"Duyệt `plan.md` (G3) rồi `/team:build <ID>`" hoặc `/team:run <ID>`.
