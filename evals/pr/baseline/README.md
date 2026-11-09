# Baseline — pr không có skill

Chạy kịch bản trên bản sao dự án với một bản sao kit đã BỎ thư mục `skills/pr`; đầu vào là câu tự nhiên ("Baseline input" trong `../scenarios.md`), không có lệnh `/team:pr`.

```bash
evals/run-eval.sh pr <n> --project <dự-án-mẫu> --mode baseline
```
Script tự tạo bản sao kit (tar loại `skills/pr`), chạy `claude -p --plugin-dir <bản sao> --max-turns/--max-budget-usd` theo `evals/config.json`, lưu vào `evals/pr/out/<ngày>/s<n>-baseline/`.
