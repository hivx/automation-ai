# Các kiểm của audit-kit

| Kiểm | Cách làm | Ngưỡng báo |
|---|---|---|
| Skill không dùng | `jq` đếm `runs.jsonl` theo `skill`; so với danh sách `skills/*/` của kit và `.claude/skills/` | 0 lần trong 30 ngày |
| Agent chạm trần | `jq` lọc `runs.jsonl` có `turns >= maxTurns` theo `agent` | ≥ 2 lần |
| Chỉ dẫn mâu thuẫn | Grep cùng một danh từ (vd. "push", "skip", "migration") đi kèm "luôn"/"bắt buộc" ở file này và "không"/"cấm" ở file khác | Mọi cặp tìm được |
| Lệch tên | Grep `/team:<x>` và `agents/<x>.md` trong `docs/`; đối chiếu thư mục | Mọi tên không tồn tại |
| Hook có thể lách | Đọc `hooks/hooks.json`: matcher PreToolUse phải gồm `Edit`, `Write`, `NotebookEdit` cho bảo vệ file; `Bash` cho git | Thiếu tool |
| allowed-tools quá rộng | Grep `allowed-tools:` có `Bash` trần, `Bash(*)`, `Bash(rm *)`, `Bash(sudo *)` | Mọi dòng |
| Skill tạm chưa đăng ký | So `.claude/skills/*/` với `docs/team/skills-registry.md` | Mọi skill thiếu |
| Skill tạm quá hạn | `skills-registry.md`: trạng thái `temp` không dùng 30 ngày | Mọi skill |
