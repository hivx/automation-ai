# Playbook: spike

## Khi nào áp dụng
- Chưa biết làm được không, cách nào tốt hơn, giá bao nhiêu.
- Cần thử nhanh trước khi cam kết một feature.

## Cỡ mặc định
S.

## Chuỗi
0. `/team:intake` → team-leader → `intake.md` (câu hỏi cần trả lời, hạn thời gian).
1. `/team:research` → researcher → `research.md`; POC trong worktree nếu cần, xóa sau đó.
2. Lưu cache → `docs/team/research/<topic>@<version>.md`.
3. [Đề xuất ADR → nháp trong `research.md`: khi kết quả dẫn tới một quyết định kiến trúc.]

## Cổng
Không.

## Điểm dừng
- Hết hạn thời gian mà chưa có câu trả lời: báo kết quả dở dang.

## Tiêu chí xong
- Câu hỏi có câu trả lời kèm nguồn và độ tin cậy; không code POC nào còn trong nhánh làm việc.

## Lỗi thường gặp
- Biến POC thành code thật.
- Spike không có câu hỏi rõ.

## Playbook liên quan
`new-feature`, `dependency-upgrade`.
