---
name: retro
description: Dùng khi đến kỳ nhìn lại, sau feature nhiều rework, khi góp ý vượt ngưỡng hai lần, hoặc scorecard có bất thường.
argument-hint: "[--since <YYYY-MM-DD>] [--decide]"
disable-model-invocation: true
context: fork
agent: team:coach
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(jq *) Bash(ls *)
---

## Mục đích
Tìm điểm nghẽn có bằng chứng và đề xuất sửa agent/skill an toàn, chờ người duyệt.

## Đầu vào
- `$ARGUMENTS`: mốc thời gian (`--since`), `--decide` khi chạy định kỳ.
- `docs/team/metrics/*` (gồm `feedback.jsonl`, `scorecard.json`), `docs/team/journal/*`. `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
Có ít nhất một dòng trong `docs/team/metrics/runs.jsonl` hoặc `feedback.jsonl` sau mốc.

## Các bước
1. Ghi `.team/current.json` {feature: "retro", stage: "retro", agent: "coach", started_at}.
2. `python3 "<kit>/scripts/measure.py" --since <date>` (Bash): điểm hiệu quả, xu hướng, bất thường, xếp hạng cần chú ý.
3. Đọc journal của các feature trong kỳ; gắn mỗi điểm nghẽn với số liệu + dòng journal.
4. Chọn ≤ 3 điểm nghẽn. Chẩn đoán 5 nguyên nhân: prompt · model/effort · đầu vào · profile/config · cỡ task.
5. Mỗi đề xuất: `docs/team/proposals/<date>/<agent-or-skill>.md` (mẫu `<kit>/templates/artifacts/proposal.md`) gồm bằng chứng, bảng 5 nguyên nhân, nội dung ĐẦY ĐỦ file overlay (dòng đầu `# Overlay from retro <date>: <reason>`, phiên bản), eval (baseline vs có thay đổi, ≥ 3 kịch bản), canary (N việc cỡ S, tiêu chí giữ/rollback/thay/bỏ), cách rollback.
6. Quy tắc STD mức 1 vi phạm ≥ 2 lần → đề xuất nâng mức.
7. Gọi thừa agent: so số agent mỗi feature với `limits.max_agents_per_feature`.
8. `docs/team/retro/<date>.md` từ `<kit>/templates/artifacts/retro.md`.

## Đầu ra
- `docs/team/retro/<date>.md`, `docs/team/proposals/<date>/*.md`.
- Tin trả ≤ 10 dòng: điểm nghẽn, đề xuất, quyết định người cần đưa.

## Tiêu chí xong
- Mỗi đề xuất đủ 6 phần, số liệu dẫn nguồn; dán đầu ra `measure.py`.

## Dấu hiệu sai
- "Sửa luôn agent" → chỉ đề xuất.
- "Một lần chậm là đủ" → cần ≥ 2 lần hoặc xu hướng.
- "Bỏ eval" → không eval, không đề xuất.

## Lệnh tiếp theo
In: "Đọc `docs/team/retro/<date>.md`; duyệt từng đề xuất bằng `Approved-by:` trong file đề xuất."
