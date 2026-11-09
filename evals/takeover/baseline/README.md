# Baseline — takeover không có skill

Chạy kịch bản trên bản sao dự án với một bản sao kit đã BỎ thư mục `skills/takeover`; đầu vào là câu tự nhiên ("Baseline input" trong `../scenarios.md`), không có lệnh `/team:takeover`.

```bash
evals/run-eval.sh takeover <n> --project <dự-án-mẫu> --mode baseline
```
Script tự tạo bản sao kit (tar loại `skills/takeover`), chạy `claude -p --plugin-dir <bản sao> --max-turns/--max-budget-usd` theo `evals/config.json`, lưu vào `evals/takeover/out/<ngày>/s<n>-baseline/`.
