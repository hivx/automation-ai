# Baseline — commit không có skill

Chạy kịch bản trên bản sao dự án với một bản sao kit đã BỎ thư mục `skills/commit`; đầu vào là câu tự nhiên ("Baseline input" trong `../scenarios.md`), không có lệnh `/team:commit`.

```bash
evals/run-eval.sh commit <n> --project <dự-án-mẫu> --mode baseline
```
Script tự tạo bản sao kit (tar loại `skills/commit`), chạy `claude -p --plugin-dir <bản sao> --max-turns/--max-budget-usd` theo `evals/config.json`, lưu vào `evals/commit/out/<ngày>/s<n>-baseline/`.
