# Kết quả eval

Cách chạy: `evals/run-eval.sh <skill> <n> --project <dự án mẫu>`; cấu hình `evals/config.json` (model sonnet cho phiên chính, `--max-turns 40`, `--max-budget-usd 2.0`; agent con dùng model trong frontmatter). Dự án mẫu: bản sao `sample-existing` sau P6 (FEAT-001 đã verify, chờ G4). Chi phí là `total_cost_usd` Claude Code in ra.

## Round 0 — v0.1.0 (2026-11-09, Claude Code 2.1.319)

| Skill / kịch bản | Chế độ | Kết quả | Lượt | Chi phí | Ghi chú |
|---|---|---|---|---|---|
| verify s1 | baseline (bỏ `skills/verify`) | 3/4 — FAIL `^Verdict:` | 7 | $0.89 | Có `acceptance.md` và đầu ra `Ran N tests`, nhưng không có dòng `Verdict:` → `team.py` không nhận giai đoạn verified. |
| verify s1 | with-skill | **4/4** | 0* | $0.69 | `Verdict: accepted`, đầu ra lệnh thật, không sửa code. |
| using-team s1 | baseline (bỏ `skills/using-team`) | 2/3 — FAIL grep OUTPUT | 15 | $0.34 | Tạo FEAT-002 intake.md, giao thẳng dev; không review. |
| using-team s1 | with-skill | 2/3 — FAIL grep OUTPUT | 2 | $0.31 | Như baseline. Không phân biệt được hai chế độ. |

\* `num_turns` của phiên chính; công việc chạy trong subagent fork nên không tính vào đây.

Kết luận:
- `verify`: skill tạo khác biệt đo được (dòng `Verdict:` mà máy đọc được).
- `using-team` s1: **không kết luận được.** Check grep OUTPUT quá hẹp (cả hai chế độ đều nêu FEAT-002 nhưng không viết `/team:intake`); check `unchanged inventory` yếu vì dev commit trong worktree. Agent team-leader vẫn mang các luật của using-team trong thân agent nên baseline gần giống. Viết lại kịch bản ở vòng sau (K-33).
- Cả hai chế độ của using-team đều cho dev làm cỡ S mà không có reviewer → K-34.

Lần chạy đầu (cùng ngày) bị loại: bản sao dự án nằm trong thư mục plugin nên mọi lệnh ghi bị từ chối ở chế độ with-skill (K-20). Đã sửa `run-eval.sh` và chạy lại; bảng trên là lần chạy lại.

Các kịch bản khác (analyze, build, commit, pr, takeover, make-skill; s2–s3 của verify, using-team) chưa chạy; lệnh xem bằng `--dry-run`.
