# Mẫu tin bàn giao trong vòng build

## Trạng thái dev (dòng đầu tin trả)
| Trạng thái | Nghĩa | tech-lead làm |
|---|---|---|
| DONE | Xong, có đỏ rồi xanh, lint sạch | Kiểm bằng chứng → gói review |
| DONE_WITH_CONCERNS | Xong nhưng có lo ngại | Lo ngại về tính đúng/phạm vi → giải quyết trước review |
| NEEDS_CONTEXT | Thiếu thông tin để làm đúng | Bổ sung, gọi lại (không gửi lại tin cũ) |
| BLOCKED | Thử nhiều lần vẫn không qua | Đổi một điều; sau max_attempts → dừng |
| DESIGN_CONFLICT | Phải sửa ngoài touchpoints / đổi hợp đồng | Dừng, báo team-leader |

## Gọi dev (lần đầu)
```
Task FEAT-012 T3 — Từ chối mã OTP hết hạn
Tiêu chí: AC-2 (mã quá 5 phút trả 401)
Touchpoints: src/auth/otp.py, tests/auth/test_otp.py — CHỈ sửa trong touchpoints
Test: cmd.test_one với {file}=tests/auth/test_otp.py
Nhánh: team/FEAT-012-task-3 (tạo từ team/FEAT-012)
Ràng buộc chung: docs/team/features/FEAT-012/plan.md#ràng-buộc-chung
Báo cáo chi tiết: docs/team/features/FEAT-012/dev-T3.md; tin trả ≤ 10 dòng, dòng đầu là trạng thái
```

## Gọi reviewer
```
Review FEAT-012 T3 — chấm theo Review checklist (10)
Gói review: docs/team/features/FEAT-012/review-pkg-T3.md (BASE 9f8e7d..a1b2c3d)
Thiết kế: docs/team/features/FEAT-012/design.md (mục 7, 8)
Tiêu chí task: AC-2
Trả: phán quyết + phát hiện `severity | STD | file:line | description | fix` + mục "không kiểm chứng được từ diff"
```

## Vòng sửa
```
Sửa FEAT-012 T3 vòng 2/3
Phát hiện (nguyên văn): docs/team/features/FEAT-012/review-03.md#vòng-1
Trong worktree của bạn: git switch team/FEAT-012-task-3 (không trỏ git vào worktree khác)
Báo cáo sửa: phát hiện → thay đổi → test phủ → lệnh + đầu ra
```
Xem lại có phạm vi: reviewer nhận `FIX_BASE..HEAD` và danh sách phát hiện cũ; trả `ADDRESSED`/`NOT ADDRESSED` từng mục.

## Dòng tiến độ trong tasks.md (để chạy tiếp sau khi nén)
```
- [ ] T3 — … — files: … — test: … — depends: T2
  - tiến độ: BASE=9f8e7d · dev gọi lần 1 · review vòng 1 request-changes · vòng 2 …
```
