# Baseline — analyze không có skill

Chạy kịch bản trên bản sao dự án với một bản sao kit đã BỎ thư mục `skills/analyze`; đầu vào là câu tự nhiên ("Baseline input" trong `../scenarios.md`), không có lệnh `/team:analyze`.

```bash
evals/run-eval.sh analyze <n> --project <dự-án-mẫu> --mode baseline
```
Script tự tạo bản sao kit (tar loại `skills/analyze`), chạy `claude -p --plugin-dir <bản sao> --max-turns/--max-budget-usd` theo `evals/config.json`, lưu vào `evals/analyze/out/<ngày>/s<n>-baseline/`.
