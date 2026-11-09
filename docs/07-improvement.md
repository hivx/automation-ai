# 07 — Tự cải tiến

Nguồn chuẩn: `SPEC.md` §9 (Journal & self-improvement, Temp skills). Skill liên quan: `/team:retro`, `/team:feedback`, `/team:audit-kit`, `/team:make-skill`, `/team:make-agent`.

## Journal (định tính)
`docs/team/journal/<feature>.md`. Sau mỗi lần bàn giao, team-leader hoặc tech-lead viết 3–5 dòng:
- giao cho ai, việc gì;
- kết quả, thời gian / số vòng;
- nhận xét về agent/skill: tốt / chậm / sai + nguyên nhân sơ bộ;
- ý tưởng cải tiến.

Mẫu: `templates/artifacts/journal-entry.md`. Trần: `journal.max_lines_per_entry` trong config.

## Scorecard (định lượng)
Mỗi agent/skill: số lần gọi, số lượt, thời gian, rework/bị từ chối, vi phạm STD gây ra, token (từ log cục bộ của Claude Code), số lần người phải can thiệp. So với trung vị của việc cùng cỡ. Hook SubagentStop ghi vào `docs/team/metrics/`.

`scripts/measure.py` chạy định kỳ, không dùng LLM: điểm hiệu quả, xu hướng, bất thường, xếp hạng cần chú ý → đưa cho coach và journal. Góp ý của người: `docs/team/metrics/feedback.jsonl`; báo động sau 2 lần vượt ngưỡng. Chỉ số gọi thừa: số agent gọi mỗi feature so với `max_agents_per_feature`.

## Vòng của coach
1. Đọc scorecard + journal → tìm điểm nghẽn.
2. Chẩn đoán 5 nguyên nhân, có bằng chứng: prompt · model/effort · đầu vào (lỗi từ khâu trước) · profile/config · cỡ task.
3. Viết đề xuất vào `docs/team/proposals/`: diff dạng overlay (`# Overlay from retro <date>: <reason>`, có phiên bản) + eval trước/sau.
4. Người duyệt → canary trên N việc cỡ S.
5. Giữ / rollback / thay / bỏ.

coach không tự áp thay đổi và không sửa bản gốc của kit.

## Skill và agent tạm
Chỉ tạo khi cần, không tạo sẵn lúc cài.
1. Ở intake/plan, team-leader thấy task cần chuyên môn kit chưa có, hoặc sẽ lặp lại.
2. Kiểm tra cái đã có: kit, `.claude/skills/` của dự án, plugin.
3. Giao `/team:make-skill` (researcher gom mẫu và docs trong repo trước nếu cần).
4. Skill nằm ở `.claude/skills/<tên>/`: mục đích, khi nào dùng, vào/ra, các bước, tool, mẫu tham khảo, tiêu chí xong, 1–2 ca thử; nhãn `temp`; ghi vào `docs/team/skills-registry.md`.
5. Giao cho subagent kiểu "dùng /<tên> cho bước X"; dùng ngay; ghi journal.
6. Theo dõi: `temp` → `project` (ổn định, người duyệt) → đề xuất đưa vào kit (≥ 2 dự án) hoặc `retired` (30 ngày không dùng). Có trần số skill tạm đang hoạt động.

`/team:make-agent` theo cùng vòng đời. Lỗi của chính kit ghi vào `docs/team/kit-issues.md`.

## Script đo
| Việc | Lệnh |
|---|---|
| Ghi một lần chạy agent | tự động: hook SubagentStop → `scripts/scorecard.sh` |
| Ghi kết quả một giai đoạn | `scripts/log-run.sh --skill <x> --result <y>` (skill `run` gọi) |
| Gộp theo agent/skill/cỡ | `python3 scripts/team.py metrics`; ghi `docs/team/metrics/scorecard.json` bằng `team.py scorecard` |
| Điểm hiệu quả, xu hướng, bất thường, xếp hạng | `python3 scripts/measure.py [--since <date>] [--logs ~/.claude/projects/<slug>/] [--json]` |

Trọng số của điểm hiệu quả nằm ở đầu `scripts/measure.py` (`WEIGHTS`). Test: `scripts/tests/test_measure.py`.
