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

## Round 1 — P7 (2026-11-09, Claude Code 2.1.319)

BEFORE = `pre-p7-round1` (= v0.1.0) chạy qua `EVAL_KIT=<worktree của tag>`; AFTER = cây hiện tại. Cùng dự án mẫu, cùng kịch bản, cùng `run-eval.sh`, chế độ with-skill; chỉ kit khác nhau.

| Kịch bản | BEFORE | AFTER | Chi phí B → A | Khác biệt thật |
|---|---|---|---|---|
| using-team s1 (3 check gốc) | 3/3 | 3/3 | $0.36 → $1.57 | — |
| using-team s1 (+2 check mới, chấm lại trên cùng thư mục làm việc) | 3/5 — FAIL `spec.md`, FAIL `review-*.md` | **5/5** | — | BEFORE: team-leader giao thẳng dev, bỏ analyze và reviewer, rồi tự đọc diff (trái hợp đồng). AFTER: analyze → `/team:build` (tech-lead → dev + reviewer), `review-01.md`, journal đếm "2/3 vai". Chi phí cao hơn là phần review mà v0.1.0 bỏ qua (K-34, K-15). |
| verify s1 | 4/4 (80 dòng, 8 dòng bảng) | 4/4 (72 dòng, 6 dòng bảng) | $0.94 → $0.87 | Tương đương; AFTER rẻ hơn 8%. |
| analyze s1 | 4/4 (115 dòng) | 4/4 (88 dòng) | $0.68 → $0.83 | Tương đương; spec AFTER ngắn hơn, cùng số tiêu chí. |

Ghi chú trung thực:
- Hai check mới của using-team s1 được thêm SAU khi chạy và chấm lại trên thư mục làm việc đã lưu của cả hai lần chạy; các check gốc không phân biệt được hai bản (K-33). Từ vòng sau, kịch bản dùng 5 check.
- Không eval nào xấu đi theo check; chi phí using-team tăng có giải thích (quy trình đúng hơn), không phải hồi quy.
- `num_turns` của phiên chính là 0–2 vì việc chạy trong subagent fork; không dùng để so.
