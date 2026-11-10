# Chạy headless

## Cờ bắt buộc
| Cờ | Vì sao |
|---|---|
| `--agent team:team-leader` | team-leader là cửa duy nhất, kể cả không người trông (ADJ-01) |
| `--permission-mode dontAsk` | không ai trả lời hộp thoại quyền |
| `--allowedTools "<từ permissions.allow>"` | thư mục chưa được tin (CI, máy mới) bỏ qua `permissions.allow` của dự án (K-06) |
| `--max-turns`, `--max-budget-usd` | trần cứng; chạm trần thì dừng, không chạy tiếp |
| `--output-format json` | đọc `subtype`, `total_cost_usd`, `result` |
| lệnh có `--decide` | không hỏi được người; câu hỏi lớn → `WAITING_FOR_ANSWER` |
Không dùng `--bare` khi có sửa file: nó tắt mọi hook, kể cả hook của plugin (ADJ-03). `--bare` chỉ cho báo cáo chỉ-đọc như `/team:status`.

Danh sách `--allowedTools`:
```
jq -r '["Read","Grep","Glob","Edit","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json
```
Giai đoạn không sửa code (verify, retro): bỏ `Edit` khỏi mảng đầu.

## Mẫu theo giai đoạn
| Việc | Lệnh | Trần gợi ý |
|---|---|---|
| Build hết task | `/team:build <ID> --decide` | lấy từ trung vị `measure.py` × 1,5; không có số liệu → bắt đầu thấp, đọc JSON rồi tăng |
| Nghiệm thu | `/team:verify <ID>` | như trên |
| Retro định kỳ | `/team:retro --decide` | như trên |
| Dọn một loại nợ | `/team:clean <loại> --decide` | như trên |

## Đọc kết quả
- `subtype: success` + `team.py status <ID>` để biết giai đoạn thật (đừng tin chữ trong `result`).
- `subtype` báo hết lượt/ngân sách → việc dở; `/team:session load` ở phiên sau.
- Trạng thái chờ người (`WAITING_FOR_APPROVAL`, `WAITING_FOR_ANSWER`) là kết thúc bình thường, không phải lỗi.
- Ghi `total_cost_usd` vào journal của feature.
