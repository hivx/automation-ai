# Playbook: retro

## Khi nào áp dụng
- Định kỳ (xem `batch/weekly-retro.md`), hoặc sau feature có nhiều rework.
- Góp ý vượt ngưỡng hai lần; scorecard có bất thường.

## Cỡ mặc định
Không áp dụng.

## Chuỗi
1. `/team:retro` → coach: `measure.py` → journal → điểm nghẽn → chẩn đoán 5 nguyên nhân.
2. coach → `docs/team/proposals/<date>/<agent-or-skill>.md`: overlay + eval trước/sau.
3. Người duyệt đề xuất.
4. Canary trên N việc cỡ S; coach so với baseline.
5. Giữ / rollback / thay / bỏ — người quyết.

## Cổng
Người duyệt mỗi đề xuất trước canary và trước khi giữ.

## Điểm dừng
- Thiếu số liệu; canary xấu hơn baseline.

## Tiêu chí xong
- `docs/team/retro/<date>.md` có; mỗi đề xuất có bằng chứng, eval, canary, rollback; quyết định của người được ghi.

## Lỗi thường gặp
- Sửa agent ngay khi thấy một lần chậm.
- Không có baseline để so.

## Playbook liên quan
`batch/weekly-retro.md`.
