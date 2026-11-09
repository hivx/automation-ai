---
name: feedback
description: Dùng khi người hoặc một vai muốn ghi nhận xét về một agent hay skill của đội: tốt, chậm, sai, khó dùng.
argument-hint: "<agent|skill> <1-5> \"<nhận xét>\" [<ID>]"
allowed-tools: Bash(jq *) Bash(cat *) Bash(date *) Bash(mkdir *) Bash(tail *)
---

## Mục đích
Ghi một dòng góp ý có cấu trúc để coach đo.

## Đầu vào
`$ARGUMENTS`: đối tượng (`agent:<tên>` hoặc `skill:<tên>`), điểm 1–5, nhận xét, mã feature (tùy chọn).

## Điều kiện trước
Thư mục `docs/team/metrics/` có (không có → `mkdir -p`).

## Các bước
1. Kiểm đối tượng tồn tại trong `agents/` hoặc `skills/` của kit hay `.claude/` của dự án.
2. Lấy `feature`, `stage` từ `.team/current.json` nếu không truyền.
3. Thêm một dòng (Bash, jq), `from` = `human` hoặc tên vai:
   ```
   jq -nc --arg ts "$(date -Iseconds)" --arg from "<from>" --arg about "<agent|skill>:<tên>" \
     --arg feature "<ID>" --arg stage "<stage>" --argjson score <1-5> --arg note "<nhận xét>" \
     '{ts:$ts,from:$from,about:$about,feature:$feature,stage:$stage,score:$score,note:$note}' \
     >> docs/team/metrics/feedback.jsonl
   ```
4. Đọc lại dòng cuối (`tail -n 1`) để kiểm JSON hợp lệ bằng `jq`.
5. Điểm ≤ 2 → nhắc: hai lần vượt ngưỡng cho cùng đối tượng sẽ kích hoạt retro.

## Đầu ra
`docs/team/metrics/feedback.jsonl` thêm một dòng.

## Tiêu chí xong
`jq` đọc được dòng cuối — dán đầu ra.

## Dấu hiệu sai
- "Sửa luôn agent theo góp ý" → chỉ ghi; coach xử lý.
- "Viết lại cả file" → chỉ nối thêm.
- "Bỏ điểm vì khó chọn" → điểm bắt buộc.

## Lệnh tiếp theo
In: "Đã ghi. Xem tổng hợp bằng `/team:retro` khi đến kỳ."
