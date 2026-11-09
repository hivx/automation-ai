# Ai gọi ai

## Ma trận
Hàng = người gọi, cột = người được gọi. ✓ = được gọi; — = không.

| người gọi ↓ / được gọi → | team-leader | tech-lead | coach | analyst | researcher | architect | designer | dev | reviewer | qa | writer | maintainer | devops | Explore |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| team-leader | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| tech-lead | — | — | — | — | — | — | — | ✓ | ✓ | — | — | — | — | ✓ |
| coach | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| analyst | — | — | — | — | — | — | — | — | — | — | — | — | — | ✓ |
| researcher | — | — | — | — | — | — | — | — | — | — | — | — | — | ✓ |
| architect | — | — | — | — | — | — | — | — | — | — | — | — | — | ✓ |
| designer | — | — | — | — | — | — | — | — | — | — | — | — | — | ✓ |
| dev | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| reviewer | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| qa | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| writer | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| maintainer | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| devops | — | — | — | — | — | — | — | — | — | — | — | — | — | — |

- Chỉ team-leader và tech-lead gọi vai khác. Vai khác chỉ được gọi `Explore` khi có tool `Agent`.
- team-leader gọi thẳng `dev` chỉ cho việc cỡ S một task; còn lại qua tech-lead.
- Không ai gọi team-leader: nó là phiên chính và là cửa duy nhất với người.
- Ma trận do hook role-policy thực thi (STD mức 3), không chỉ là văn bản.
- Độ sâu tối đa: phiên chính (team-leader) → tech-lead → dev/reviewer → Explore.

## Bàn giao
Bàn giao = MỘT FILE + một tin nhắn tự đủ ≤ 10 dòng. Người nhận KHÔNG thấy hội thoại của người gửi, nên tin nhắn phải đủ để làm mà không hỏi lại.

Tin nhắn giao việc luôn có:
1. Mã feature/task.
2. Đường dẫn file đầu vào (artifact).
3. Mục tiêu một câu.
4. Tiêu chí xong.
5. Giới hạn (đường dẫn được sửa, điều không được làm).

Tin nhắn trả việc luôn có:
1. Kết quả / phán quyết.
2. Đường dẫn file đầu ra.
3. Bằng chứng (đầu ra lệnh đã chạy).
4. Còn thiếu gì, rủi ro gì.

### Trường bắt buộc theo chiều
| Chiều | Trường bắt buộc |
|---|---|
| tech-lead → dev | mã task; tiêu chí nghiệm thu; touchpoints; `cmd.test_one`; nhánh; câu "chỉ sửa trong touchpoints" |
| dev → tech-lead | file đã đổi; test đã chạy kèm đầu ra thật; còn thiếu gì |
| tech-lead → reviewer | diff (commit hoặc nhánh); `design.md`; tiêu chí task; câu "chấm theo Review checklist (10)" |
| reviewer → tech-lead | phán quyết approve / request-changes / design-defect; phát hiện theo định dạng STD |
| team-leader → qa | `spec.md` (DoD); nhánh feature; câu "chấm theo Acceptance checklist (6)" |
| qa → team-leader | phán quyết accepted / rework / design-defect; `acceptance.md` có đầu ra thật |
| vai bất kỳ → team-leader khi cần hỏi người | trạng thái `NEEDS_ANSWER`; file chứa câu hỏi (2–4 lựa chọn, khuyến nghị, hậu quả) |

## Lý do gọi
Mỗi lần gọi một vai, người gọi ghi MỘT câu lý do vào `docs/team/journal/<feature>.md` trước khi gọi, ví dụ: "Gọi researcher vì spec cần thư viện ký số chưa có trong dự án." Không có lý do thì không gọi.
