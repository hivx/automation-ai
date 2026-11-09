# Khi có sự cố

## Hook chặn
Dấu hiệu: Claude báo một thao tác bị chặn, kèm lý do từ hook.
1. Đọc lý do. Hook là luật (P3), không tìm cách lách.
2. Sửa file bảo vệ (`protected_paths`) → người tự sửa, hoặc đổi profile nếu đường dẫn bị khai nhầm.
3. Tạo file ngoài `allowed_new_file_roots` → chọn chỗ đúng, hoặc thêm thư mục vào danh sách (người duyệt).
4. Push nhánh bảo vệ / force-push → chỉ push nhánh `team/*`; mở PR.
5. Vai làm việc ngoài phạm vi (role-policy) → giao đúng vai.
6. Hook sai thật → `/team:feedback "<mô tả>"`; lỗi kit ghi vào `docs/team/kit-issues.md`.

## Cổng kẹt
Dấu hiệu: `/team:status` báo `WAITING_FOR_APPROVAL` dù bạn nghĩ đã duyệt.
1. Kiểm tra dòng `Approved-by: <tên> <YYYY-MM-DD>` nằm ở ĐẦU đúng artifact (G5: `Approved-by-prod:`).
2. Kiểm tra người duyệt có trong `approvers` của cổng đó (`.team/config.json`).
3. Duyệt qua issue: bình luận đúng `@claude approve Gn`.
4. Không muốn cổng này nữa → đặt `false` trong `gates`. Không xóa artifact.

## CI đỏ
1. `/team:ci` — devops phân loại nguyên nhân TRƯỚC: code, test chập chờn, môi trường, cấu hình CI, phụ thuộc.
2. Sửa trên PR riêng (playbook ci-fix). Không bao giờ xóa bước test để cho xanh.
3. Test chập chờn → ghi vào `debt.md`, không đánh dấu skip.

## Ngữ cảnh đầy
Dấu hiệu: cảnh báo vượt `context_warn_pct`, hoặc Claude bắt đầu quên.
1. `/team:session` để ghi bàn giao (≤ 40 dòng).
2. `/compact` hoặc mở phiên mới — trạng thái nằm trên đĩa, `/team:status` đưa bạn về đúng chỗ.
3. Một feature mỗi phiên. Việc đọc code lớn → để `Explore` làm.

## Vượt ngân sách hoặc vòng sửa
`feature_budget_usd` hoặc `max_rework` vượt → đội dừng và báo. Xem `journal/<feature>.md`, quyết định: chia nhỏ task, đổi cỡ, hay nâng giới hạn.
