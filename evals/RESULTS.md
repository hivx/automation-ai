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

## Round 2 — P7 vòng 2 (2026-11-10, Claude Code 2.1.319)

BEFORE = `pre-p7-round2` (= v0.2.1) qua `EVAL_KIT=<worktree của tag>`; AFTER = cây hiện tại (v0.3.0). Cùng dự án mẫu (`eval-project`: FEAT-001 đã accepted, chờ G4), cùng `run-eval.sh`, chế độ with-skill. Kịch bản đã sửa TRƯỚC khi chạy: make-skill s1 (check phân biệt), asbuilt s1 (mới).

| Kịch bản | BEFORE | AFTER | Chi phí B → A | Ghi chú |
|---|---|---|---|---|
| using-team s1 (5 check) | 5/5 | lần 1: 2/5 → sửa K-70 → lần 2: 3/5 → sửa K-73 → lần 3: **5/5** | $1.71 → $0.14 / $0.17 / $1.76 | Hai file liên quan (intake, team-leader) GIỐNG nhau ở hai bản lúc chạy lần 1: khác biệt là dao động giữa các lần chạy, lộ ra hai lỗi thật của kit. Lần 1: intake chỉ người gọi được (`disable-model-invocation`) mà using-team trỏ tới nó → team-leader dừng, bắt người gõ lệnh (K-70). Lần 2: intake chạy, rồi dừng in `/team:analyze` vì "in lệnh tiếp theo" mơ hồ (K-73). Lần 3: intake → analyze → build (dev + reviewer), như BEFORE. |
| verify s1 (4 check) | 4/4 | **4/4** | $0.90 → $1.05 | Tương đương. |
| make-skill s1 (6 check) | 0/6 | 0/6 | $0.33 → $0.16 | Không kết luận được. BEFORE: mọi lần ghi `.claude/skills/**` bị Claude Code từ chối ở `-p` (K-72, thử 4 dạng `--allowedTools`, đều từ chối). AFTER: từ chối ĐÚNG theo hợp đồng mới — nhu cầu không có bằng chứng (chỉ một export CSV, không task lặp); không ghi file nào. Nhánh "tạo skill" chỉ thử được ở phiên tương tác. |
| asbuilt s1 (7 check, chấm lại) | 6/7 | **7/7** | $0.23 → $0.30 | Check CHANGELOG ban đầu trỏ nhầm `CHANGELOG.md` ở gốc (dự án dùng `docs/CHANGELOG.md`) và check `^## Đổi gì` thêm SAU khi chạy; cả hai thư mục làm việc được chấm lại. BEFORE: `pr-body.md` có 3/4 tiêu đề mà `/team:pr` grep (thiếu "Đổi gì"), không có mục nợ sau G4. AFTER: 4/4 tiêu đề, `## Nợ sau G4` 3/3 đóng, bảng 17 dòng so từng tiêu chí/touchpoint. |

Ghi chú trung thực:
- Không eval nào xấu đi sau khi sửa; lần chạy xấu (using-team lần 1, 2) có nguyên nhân, có sửa (K-70, K-73) và chạy lại.
- Chi phí using-team AFTER lần 3 ≈ BEFORE: cùng chuỗi vai.
- make-skill cần một kịch bản có bằng chứng thật (task lặp) và phiên tương tác; ghi ở backlog vòng sau.
