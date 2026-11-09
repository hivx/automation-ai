# 01 — Quy trình

Nguồn chuẩn: `SPEC.md` §4–§5. Trang này là bản đọc nhanh cho người. Điều chỉnh: `docs/00-overview.md` (ADJ-09).

## Chín giai đoạn và cổng
Artifact nằm ở `docs/team/features/<ID>/` trừ khi ghi khác.

| # | Giai đoạn | Lệnh | Vai | Artifact | Cổng mặc định |
|---|---|---|---|---|---|
| G0 | Tiếp nhận dự án | `/team:takeover` | team-leader (+Explore, researcher) | `docs/team/assessment.md`, `ai-readiness.md`, ... | G0 bật với dự án có sẵn |
| 0 | Tiếp nhận yêu cầu | `/team:intake` | team-leader | `intake.md` | — |
| 1 | Phân tích | `/team:analyze` | analyst | `spec.md` (có DoD) | G1 bật |
| 2 | Nghiên cứu | `/team:research` | researcher | `research.md` + cache `docs/team/research/` | — |
| 3 | Kiến trúc | `/team:architect` | architect | `docs/team/architecture.md` hoặc `arch-impact.md`, `adr/` | G2 bật |
| 4 | Thiết kế chi tiết | `/team:design` | designer | `design.md` | G2b tắt |
| 5 | Lập kế hoạch | `/team:plan` | tech-lead | `plan.md`, `tasks.md` | G3 bật |
| 6 | Xây dựng | `/team:build` | tech-lead → dev, reviewer | code, commit, `review-NN.md` | — |
| 7 | Nghiệm thu | `/team:verify` | qa | `acceptance.md` | G4 bật |
| 8 | Phát hành | `/team:asbuilt`, `/team:pr`, `/team:release` | writer, tech-lead, devops | `asbuilt.md`, CHANGELOG, PR | G5 luôn là người |
| 9 | Vận hành | `/team:intake --type bug`, `/team:clean`, `/team:ci`, `/team:retro` | team-leader, maintainer, devops, coach | `defects.md`, `debt.md`, `retro/` | — |

**Duyệt cổng:** thêm dòng `Approved-by: <tên> <YYYY-MM-DD>` lên đầu artifact (G5 dùng `Approved-by-prod:`), hoặc bình luận `@claude approve Gn` trên issue. Cổng đặt `false` trong `.team/config.json` thì không chặn.

**Trạng thái được tính, không lưu:** `/team:status` đọc artifact và cho biết feature đang ở đâu. Một cổng đang bật mà chưa duyệt sẽ chặn mọi giai đoạn sau, kể cả khi artifact sau đã có.

## Cỡ việc
| Cỡ | Dấu hiệu | Chuỗi |
|---|---|---|
| S | Mô tả diff bằng một câu; ≤ 3 file; không đổi schema/API | intake → analyze ngắn → build (1 dev) → verify tự động → release |
| M | Một module; đổi dữ liệu hoặc API; 1–5 người-ngày | intake → analyze → [research] → design → plan → build → verify → release |
| L | Nhiều module; NFR mới; > 5 người-ngày | đủ 9 giai đoạn; kiến trúc bắt buộc; task đầu là walking skeleton |

team-leader định cỡ ở intake. Ép cỡ bằng `--size S|M|L` hoặc nhãn `team:size:*`. Đổi cỡ giữa chừng được ghi lý do vào `intake.md`.

## Hỏi hay tự quyết
- **`ask` (mặc định):** chỉ hỏi điều chưa rõ mà hậu quả LỚN hoặc KHÔNG ĐẢO NGƯỢC được (xóa/di trú dữ liệu, đổi API công khai, đổi luật nghiệp vụ, chi phí). Tối đa 5 câu/vòng, 2 vòng; mỗi câu 2–4 lựa chọn, có khuyến nghị và hậu quả. Việc nhỏ ghi vào `## Assumptions decided by the team`.
- **`decide`:** không hỏi; mọi quyết định ghi: chọn gì / vì sao / phương án khác / sửa thế nào nếu sai. Bật bằng `--decide`, nhãn `team:decide` hoặc `default_mode`.
- **Trong CI:** câu hỏi thành bình luận issue + nhãn `team:needs-answer`, dừng với `WAITING_FOR_ANSWER`.
- Chỉ phiên chính (team-leader) hỏi người; vai khác trả câu hỏi về cho team-leader (ADJ-01).

## Vòng xây dựng
1. tech-lead chọn task chưa bị chặn trong `tasks.md`.
2. dev (worktree riêng): viết test hỏng trước → làm → `cmd.test_one` → `cmd.lint` → commit.
3. reviewer (ngữ cảnh mới): tầng 1 khớp spec → tầng 2 chất lượng; phát hiện có mã STD.
4. dev sửa blocker/major (≤ `max_rework` vòng).
5. tech-lead tick task, viết `review-NN.md`, gộp vào `team/<ID>`, chạy `cmd.test`.
6. Hết task → `/team:verify`.

Task dài 2–5 phút, có đường dẫn file cụ thể. Hai task chạm cùng file không chạy song song. Không ai nói "xong" khi chưa dán đầu ra.

## Dừng và leo thang
Đội dừng khi: task BLOCKED sau `max_attempts`; vượt `max_rework`; gặp `DESIGN_CONFLICT` hoặc phán quyết design-defect; cổng bật chưa duyệt; vượt `feature_budget_usd`; chạm `protected_paths`; hai vòng sửa cùng một lỗi.
Mỗi lần dừng nói rõ: lý do, việc nào, ai phải làm gì, lệnh để chạy tiếp. Xử lý: `docs/guides/incidents.md`.

## Playbook
16 playbook trong `workflows/`, chọn theo loại việc rồi theo cỡ: xem `docs/guides/decision-tree.md`.
