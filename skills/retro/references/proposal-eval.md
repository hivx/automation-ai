# Eval và canary cho một đề xuất

## Eval phân biệt được
Định dạng giống `evals/<skill>/scenarios.md` để `evals/run-eval.sh` chạy được:
```markdown
## Scenario 1 — <tình huống đã gây điểm nghẽn>
- Situation: <dẫn journal/runs.jsonl>
- Input: `<lệnh /team:… với bản đề xuất>`
- Baseline input: `<cùng lệnh>`  (BEFORE = kit hiện tại, AFTER = kit + overlay)
- Good: <kết quả mong đợi>
- Bad: <điều đã xảy ra>
- Checks:
  - grep: `<regex>` in `<file|OUTPUT>`
  - exists: `<path>`
```
Luật:
- ≥ 3 kịch bản: tình huống gốc, một biến thể, một đối chứng (việc mà bản hiện tại đã làm đúng — phải vẫn đúng).
- Ít nhất một check bản hiện tại TRƯỢT và bản đề xuất QUA. Check qua ở cả hai bản ghi "không phân biệt" — không tính là bằng chứng.
- Check về nội dung, không chỉ "file tồn tại" (file rỗng cũng tồn tại).
- Đổi câu chữ (prompt): ≥ 3 lần chạy mỗi bản; độ dao động là một chỉ số.
- coach không chạy eval (Bash chỉ đọc): ghi "người chạy: <người hoặc người bảo trì kit>", lệnh `EVAL_KIT=<kit có overlay> evals/run-eval.sh <skill> <n> --project <dự án mẫu>`.

## Canary
| Mục | Ghi gì |
|---|---|
| Phạm vi | N việc cỡ S kế tiếp (N = 3 mặc định; độ tin cậy thấp → 2 và theo dõi sát) |
| Đo | chỉ số của điểm nghẽn (lượt, rework, thời gian) qua `measure.py --since <ngày áp>` so trung vị đường nền cùng cỡ |
| Giữ | chỉ số tốt hơn đường nền và không chỉ số nào xấu hơn quá 1 MAD |
| Rollback | chỉ số xấu hơn đường nền, hoặc một việc canary hỏng vì thay đổi |
| Thay | tốt ở chỉ số mục tiêu nhưng xấu ở chỉ số khác → đề xuất bản khác |
| Bỏ | không khác biệt sau N việc → gỡ overlay (đơn giản hơn là tốt hơn) |
| Rollback thế nào | xóa file overlay (đường dẫn), hoặc khôi phục bản trước (phiên bản ghi trong dòng đầu) |

Retro kế tiếp đọc kết quả canary ở bước "theo dõi retro trước" và ghi khuyến nghị; người quyết.
