Feature: <ID>
Stage: any
Author-agent: team-leader
Date: <YYYY-MM-DD>
Approved-by:
<!-- Cổng: người duyệt điền dòng trên `Approved-by: <tên> <YYYY-MM-DD>`. Không có cổng thì để trống. -->

# Skill và agent tạm của dự án

Trần đang hoạt động (skill + agent `temp`): `limits.max_temp_skills`. `temp` không dùng 30 ngày → `retired`; ổn định và người duyệt → `project`; `project` dùng ở ≥ 2 dự án → đề xuất đưa lên kit.
team-leader cập nhật `last used` và `runs` trong cùng lần ghi journal khi giao việc dùng skill/agent; retro rà và đề xuất đổi trạng thái.

| name | loại skill/agent | trạng thái temp/project/retired | nhu cầu (bằng chứng) | created | last used | runs | model (agent) | ca thử |
|---|---|---|---|---|---|---|---|---|
| <tên> | skill | temp | <một câu> (<journal/review dẫn tới>) | <YYYY-MM-DD> | <YYYY-MM-DD> | 0 | — | .claude/skills/<tên>/references/tests.md |
