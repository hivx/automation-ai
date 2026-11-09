---
name: feedback
description: Dùng khi người hoặc một vai muốn ghi nhận xét về một agent hay skill của đội: tốt, chậm, sai, khó dùng.
argument-hint: "<agent|skill> <1-5> \"<nhận xét>\" [<ID>]"
allowed-tools: Bash(jq *) Bash(cat *) Bash(date *) Bash(mkdir *) Bash(tail *)
---

# Ghi góp ý

## Tổng quan
Ghi một dòng góp ý có cấu trúc về một agent hay skill để coach đo. `$ARGUMENTS`: đối tượng (`agent:<tên>` hoặc `skill:<tên>`), điểm 1–5, nhận xét, mã feature (tùy chọn).

## Quy trình
1. Kiểm đối tượng tồn tại trong `agents/`/`skills/` của kit hoặc `.claude/` của dự án; không có → báo, dừng.
2. Lấy `feature`, `stage` từ `.team/current.json` nếu không truyền.
3. Đọc `docs/team/metrics/feedback.jsonl` (có thể chưa có), rồi Write lại file với một dòng JSON mới ở cuối:
   `{"ts": "<ISO>", "from": "<human|vai>", "about": "<agent|skill>:<tên>", "feature": "<ID>", "stage": "<stage>", "score": <1-5>, "note": "<nhận xét>"}`.
4. Kiểm dòng cuối hợp lệ: `tail -n 1 docs/team/metrics/feedback.jsonl | jq .`.
5. Điểm ≤ 2 → nhắc: hai lần vượt ngưỡng cho cùng đối tượng sẽ kích hoạt `/team:retro`.

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Sửa luôn agent theo góp ý" | Chỉ ghi; coach chẩn đoán, người duyệt. |
| "Nối nhanh bằng `jq >>`" | Write; headless từ chối chuyển hướng. |
| "Viết lại cả file cho sạch" | Giữ mọi dòng cũ, chỉ thêm một dòng. |
| "Bỏ điểm vì khó chọn" | Điểm bắt buộc 1–5. |
| "Ghi chung chung 'chậm'" | Nêu việc, feature, stage cụ thể. |
| "Góp ý về dự án, không về đội" | Chỉ về agent/skill; lỗi dự án vào `debt.md`. |

## Kiểm chứng
- `jq` đọc được dòng cuối — dán đầu ra.
- Số dòng file tăng đúng 1 (`wc -l` trước/sau).
