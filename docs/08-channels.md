# 08 — Kênh làm việc

Nguồn chuẩn: `SPEC.md` §11. Điều chỉnh: ADJ-01, ADJ-03.

| Kênh | Hỏi người bằng | Chế độ | Ghi chú |
|---|---|---|---|
| CLI / Desktop / IDE | `AskUserQuestion` trong phiên chính (team-leader) | `ask` hoặc `decide` | Kênh chính hằng ngày |
| GitHub Actions | Bình luận issue + nhãn `team:needs-answer` | `ask` hoặc `decide` | Dùng `anthropics/claude-code-action@v1` |
| Tác vụ định kỳ | Không hỏi | chỉ `decide` | retro, clean-sweep, smoke sau deploy |
| Headless `claude -p` | Không hỏi | chỉ `decide` | Xem bên dưới |
| Projects (đám mây) | Như CLI | tùy | Chạy nhiều feature song song |

## GitHub Actions
- Nhãn `team:intake` trên issue → tiếp nhận; `team:run` → chạy tiếp tới cổng kế.
- Duyệt cổng bằng bình luận `@claude approve Gn`.
- Câu hỏi được đăng thành bình luận theo mẫu `templates/artifacts/question-comment.md`; job dừng với `WAITING_FOR_ANSWER`.
- Workflow mẫu: `templates/project/github/workflows/team-ci.yml`, `team-feature.yml`.

## Headless
Lệnh cho việc có sửa file (cần hook):
```
claude -p "<lệnh /team:...>" \
  --permission-mode dontAsk --allowedTools "<allowlist tối thiểu>" \
  --max-turns <n> --max-budget-usd <usd> --output-format json
```
- KHÔNG dùng `--bare` cho việc có sửa file: `--bare` tắt mọi hook, kể cả hook của plugin, nên luật máy không chạy (ADJ-03).
- `--bare` chỉ cho báo cáo chỉ đọc như `/team:status`; khi đó nạp plugin bằng `--plugin-dir` và đặt `ANTHROPIC_API_KEY`.
- Chế độ `decide` bắt buộc. Kết quả đọc từ JSON đầu ra, đối chiếu `templates/schemas/stage-result.json`.

## Tác vụ định kỳ
Playbook batch trong `workflows/batch/`: `build-all-tasks`, `verify-all`, `weekly-retro`, `clean-sweep`. Chạy ở chế độ `decide`; chạm cổng đang bật thì dừng và báo.
