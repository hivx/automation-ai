---
name: design
description: Dùng khi spec đã duyệt cần thiết kế chi tiết (dữ liệu, API, luồng, quyền, migration, touchpoints, test plan) trước khi lập kế hoạch, hoặc refactor cần bản thiết kế ngắn.
argument-hint: "<ID> [--short]"
context: fork
agent: team:designer
background: false
allowed-tools: Bash(python3 *) Bash(cat *)
---

## Mục đích
Viết `design.md` đủ cụ thể để tech-lead chia task không cần đoán.

## Đầu vào
- `$ARGUMENTS`: mã `<ID>`; `--short` cho refactor (chỉ mục 1, 7, 8 + cách chứng minh hành vi không đổi).
- `spec.md`; `architecture.md` hoặc `arch-impact.md` (cỡ L); `.team/profile.json`. `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
G1 đã duyệt (khi bật); G2 đã duyệt khi có kiến trúc. Kiểm: `python3 "$(cat .team/plugin_root)/scripts/team.py" status <ID>`.

## Các bước
1. Ghi `.team/current.json` {feature, stage: "design", agent: "designer", started_at}.
2. Đọc `structure.*`, `naming.*` trong profile; gọi Explore tìm file, dữ liệu, API sẽ bị chạm.
3. Viết `design.md` từ `<kit>/templates/artifacts/design.md`, 8 mục theo thứ tự:
   1. Bối cảnh; 2. Mô hình dữ liệu; 3. API/hợp đồng; 4. Luồng; 5. Quyền; 6. Migration và rollback; 7. Touchpoints (đường dẫn cụ thể, ghi "mới" hay "sửa"); 8. Test plan ánh xạ từng tiêu chí.
4. Kiểm: file "mới" nằm trong `structure.allowed_new_file_roots`; không touchpoint nào trong `protected_paths`.
5. Kiểm: mỗi tiêu chí trong `spec.md` có ≥ 1 dòng test plan.
6. Hợp đồng công khai đổi → phiên bản mới + hướng dẫn di trú.

## Đầu ra
- `docs/team/features/<ID>/design.md`.
- Tin trả ≤ 10 dòng: số touchpoints, đổi dữ liệu/API, migration có không, cổng G2b.

## Tiêu chí xong
- Đủ 8 mục (hoặc 3 mục khi `--short`); bảng tiêu chí → test đầy đủ được dán.

## Dấu hiệu sai
- "Dev tự tìm file" → ghi đường dẫn.
- "Khỏi rollback" → luôn có.
- "Luật nghiệp vụ chắc là vậy" → trả câu hỏi về team-leader.

## Lệnh tiếp theo
G2b bật: "Duyệt `design.md` rồi `/team:plan <ID>`"; không: `/team:plan <ID>`.
