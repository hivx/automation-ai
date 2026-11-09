# Baseline — verify không có skill

Chạy kịch bản trên bản sao dự án với một bản sao kit đã BỎ thư mục `skills/verify`; đầu vào là câu tự nhiên ("Baseline input" trong `../scenarios.md`), không có lệnh `/team:verify`.

```bash
evals/run-eval.sh verify <n> --project <dự-án-mẫu> --mode baseline
```
Script tự tạo bản sao kit (tar loại `skills/verify`), chạy `claude -p --plugin-dir <bản sao> --max-turns/--max-budget-usd` theo `evals/config.json`, lưu vào `evals/verify/out/<ngày>/s<n>-baseline/`.
