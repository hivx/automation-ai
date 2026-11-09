# Message commit — ví dụ

| Xấu | Vì sao | Tốt |
|---|---|---|
| `fix` | Không loại phạm vi, không mã, không nghĩa | `fix(otp): reject codes older than 5 minutes (FEAT-012)` |
| `update stuff (FEAT-012)` | "update" không nói gì | `refactor(report): extract row formatter (FEAT-012)` |
| `feat: add csv` | Thiếu scope và mã | `feat(report): add to_csv export (FEAT-001)` |
| `WIP` | Không phải điểm lưu | Commit khi xanh, message đầy đủ |
| `feat(api): add endpoint and refactor db and fix typo (FEAT-3)` | Ba ý trong một commit | Ba commit |

## Thân message (khi thay đổi không tầm thường)
```
fix(otp): reject codes older than 5 minutes (FEAT-012)

Expired codes were accepted because the comparison used the issue time
instead of the verify time. Covers AC-2.
```

## Tách commit
1. `test` + code của một hành vi → một commit `feat`/`fix`.
2. Đổi tên/di chuyển thuần → `refactor`.
3. Định dạng thuần trên file trong touchpoints → `chore` (hoặc đi cùng commit của file đó nếu formatter ép).
4. Tài liệu → `docs`.
