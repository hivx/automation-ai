Feature: <ID>
Stage: retro
Author-agent: coach
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

# Retro <YYYY-MM-DD>

- Kỳ: <từ> → <đến>; feature: <danh sách>
- Lệnh: `measure.py --since <date>` (đầu ra bên dưới)

## Xếp hạng cần chú ý
<bảng từ measure.py>

## Điểm nghẽn (≤ 3)
| # | Đối tượng | Bằng chứng (số liệu + dòng journal) |
|---|---|---|

## Chẩn đoán 5 nguyên nhân
| Điểm nghẽn | prompt | model/effort | đầu vào | profile/config | cỡ task | Kết luận |
|---|---|---|---|---|---|---|

## Đề xuất
- `docs/team/proposals/<date>/<agent-or-skill>.md` — <tóm tắt>; chờ người duyệt

## Gọi thừa agent
<số agent mỗi feature so với max_agents_per_feature>

## CLAUDE.md
<!-- Đầu ra `check-claude-md.py`, rồi mỗi sự thật dự án cần thêm, sửa hoặc bỏ một dòng, kèm nguồn. /team:asbuilt (writer) áp các dòng này vào khối project. -->
- `check-claude-md.py`: <dòng tổng kết>
- add | fix | remove: <dòng nguyên văn> — mục <tên> — nguồn: <dòng journal / review-NN / defects>
