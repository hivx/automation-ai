# 03 — Sổ tay kỹ thuật

Nội dung chuẩn nằm ở `handbook/`:
- `handbook/STD.md` — bản đầy đủ: 12 mảng, mã `STD-<AREA>-n`, checklist review (10 mục) và nghiệm thu (6 mục).
- `handbook/STD-short.md` — bản rút gọn, SINH bằng `scripts/gen-handbook-short.py`, nạp sẵn vào agent qua skill `handbook`. Không sửa tay.
- `handbook/tool-selection.md` — chọn hook, script, rule, skill hay agent.
- `handbook/tool-map.md` — việc → tool ưu tiên → tool dự phòng.
- `handbook/who-calls-whom.md` — quan hệ gọi giữa các vai.

## Ba mức thực thi
| Mức | Ai thực thi | Ví dụ |
|---|---|---|
| 3 | Máy chặn | formatter/linter, hook, `permissions.deny`, CI, branch protection |
| 2 | Agent kiểm | checklist của reviewer/qa, phát hiện có mã STD |
| 1 | Văn bản | CLAUDE.md, rule, handbook |

Quy tắc mức 1 bị vi phạm ≥ 2 lần → coach đề xuất nâng mức.

## Mười hai mảng
`STRUCT` cấu trúc · `NAME` đặt tên · `STYLE` phong cách · `DESIGN` thiết kế · `TEST` kiểm thử · `ERR` xử lý lỗi · `GIT` git · `CI` tích hợp liên tục · `DOC` tài liệu · `SEC` bảo mật · `DEP` phụ thuộc · `OPS` vận hành.

Nguyên tắc bất biến nằm trong handbook. Chi tiết theo stack lấy từ khe profile (`cmd.*`, `structure.*`, `naming.*`, `test.skip_markers`, `protected_paths`, `ci.*`, `deploy.*`), xem `docs/04-profile.md`.

## Định dạng phát hiện
`severity | STD code | file:line | description | fix` — chỉ liệt kê blocker/major; minor gộp một dòng.

## Mở rộng
**Thêm một quy tắc**
1. Mở `handbook/STD.md`, vào mảng phù hợp, lấy số trống TIẾP THEO (không chèn giữa, không dùng lại số cũ).
2. Viết một dòng: `mã | câu mệnh lệnh | mức | thực thi bởi | khe profile hoặc —`.
3. Mức 3 thì phải có hook/script/CI thật thực thi nó; chưa có thì ghi mức 2 hoặc 1.
4. Chạy `scripts/gen-handbook-short.py` để sinh lại `handbook/STD-short.md`.
5. Chạy `scripts/validate.sh`: bản rút gọn cũ hoặc bị sửa tay sẽ FAIL.

**Bỏ một quy tắc:** giữ dòng, thêm `(deprecated → STD-X-m)`, hạ mức về 1.

**Nâng mức:** coach đề xuất khi một quy tắc mức 1 bị vi phạm ≥ 2 lần (`docs/07-improvement.md`).

Chọn cơ chế thực thi theo `handbook/tool-selection.md`; công cụ cho từng việc theo `handbook/tool-map.md`.
