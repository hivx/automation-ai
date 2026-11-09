# Ngân sách các tầng quét

| Tầng | Đọc gì | Ngân sách | Trả lời câu nào | Dừng khi |
|---|---|---|---|---|
| T0 | Cây thư mục, manifest, `git log --stat`, tag, issue/PR mở, CHANGELOG (chỉ tên và số liệu) | ≈ 0 token nội dung; ≤ 10 lệnh | Đã tới đâu (sơ bộ) | Đủ để biết stack, nhịp commit, vùng nóng |
| T1 | README, `docs/`, ADR, CLAUDE.md, spec/plan | ≤ 15 tài liệu; mục lục trước | Làm gì (theo lời tài liệu) | Có mô tả tính năng chính |
| T2 | Module chính + vùng nóng: tính năng ↔ code/test, TODO/FIXME, test skip, nhánh chưa gộp, migration chưa chạy | ≤ 10 module, qua Explore | Đã tới đâu (thật), việc tiếp theo | Không mâu thuẫn mới |
| T3 | Đọc sâu từng module | Chỉ khi T2 mâu thuẫn, module không tài liệu, hoặc `--full` | Làm rõ mâu thuẫn | Mâu thuẫn được giải thích |

## Repo nhỏ
Repo < 30 file được theo dõi: T2 được đọc file trực tiếp thay vì Explore; ghi rõ "đọc trực tiếp, < 30 file" trong bảng Đã quét. T3 vẫn chỉ chạy khi có mâu thuẫn hoặc `--full`.

## AI-readiness — điều cần xét
- CLAUDE.md hiện có: số dòng, nội dung, độ cũ, mâu thuẫn với code.
- `.claude/`, plugin, MCP, AGENTS.md: giữ / cắt / viết lại.
- Kết luận một trong ba: `ready` / `adjust profile` / `clean first`.

## Phụ lục sức khỏe trong assessment.md
Build/test có chạy được (lệnh đề xuất), lint, coverage nếu có số liệu, phụ thuộc lỗi thời/CVE, secret lộ, test chập chờn.
