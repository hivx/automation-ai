---
name: retro
description: Dùng khi đến kỳ nhìn lại, sau feature nhiều rework, khi góp ý vượt ngưỡng hai lần, hoặc scorecard có bất thường, để tìm điểm nghẽn của đội có bằng chứng và đề xuất sửa agent/skill chờ người duyệt.
argument-hint: "[--since <YYYY-MM-DD>] [--decide]"
disable-model-invocation: true
context: fork
agent: team:coach
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(jq *) Bash(ls *)
---

# Nhìn lại có bằng chứng

## Tổng quan
Skill này tìm tối đa ba điểm nghẽn của ĐỘI — agent, skill, cấu hình — có số liệu và journal làm bằng chứng, chẩn đoán theo 5 nguyên nhân (prompt · model/effort · đầu vào · profile/config · cỡ task), và viết đề xuất sửa an toàn: overlay đầy đủ + eval + canary + cách rollback, chờ người duyệt. Skill chạy trong ngữ cảnh `coach` (fork): Bash chỉ đọc, không gọi vai nào, không tự áp thay đổi. coach THIẾT KẾ eval nhưng không chạy được; người hoặc người bảo trì kit chạy `evals/run-eval.sh`.

Mọi phát hiện có nguồn (dòng jsonl, dòng journal, `file:line`); không có nguồn thì bỏ. Báo cáo phải phân biệt "đã kiểm và sạch" với "không kiểm được". Không đổ lỗi cho agent: đích luôn là một trong 5 nguyên nhân.

`$ARGUMENTS`: `--since <YYYY-MM-DD>` (mặc định từ retro trước, hoặc 14 ngày); `--decide` khi chạy định kỳ không người trông. `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- Đến kỳ (batch `weekly-retro`), hoặc kết thúc một mốc phát hành.
- Feature vượt `limits.max_rework`; `feedback.jsonl` vượt ngưỡng hai lần; `measure.py` báo bất thường.
- Cần đánh giá canary của một đề xuất đã áp (giữ / rollback / thay / bỏ).

Không dùng khi:
- Muốn tìm lỗi của chính bộ kit (hook lách được, tên lệch) → `/team:audit-kit`.
- Muốn sửa ngay một agent/skill → không có đường tắt: đề xuất ở đây, người duyệt.
- Chưa có lượt chạy nào sau mốc → chạy việc trước.

## Tìm hiểu stack trước
1. Read `.team/config.json`: `limits.max_agents_per_feature`, `limits.max_rework`, `limits.max_temp_skills`, `models`, `memory.*`.
2. Nguồn số liệu: `docs/team/metrics/runs.jsonl`, `feedback.jsonl`, `scorecard.json`, `sessions.jsonl`; journal `docs/team/journal/*.md`; retro và đề xuất trước `docs/team/retro/`, `docs/team/proposals/`; `docs/team/skills-registry.md`.
3. `python3 "<kit>/scripts/measure.py" --help`: chỉ số có sẵn. Trường `result` của scorecard đoán từ chữ trong tin cuối (K-18) → số liệu dựa trên nó gắn "độ tin cậy thấp". Token chỉ có khi chạy với `--logs`; không thì ghi "không đo".

## Đầu vào và điều kiện trước
- Có ít nhất một dòng trong `runs.jsonl` hoặc `feedback.jsonl` sau mốc. Không có → `NEEDS_CONTEXT` (thiếu số liệu), không viết retro rỗng.
- Kiểm: `python3 "<kit>/scripts/team.py" status` (feature nào trong kỳ, cỡ gì).

## Quy trình
1. **Ghi vị trí và khung.** Write `.team/current.json` {feature: "retro", stage: "retro", agent: "coach", started_at}. Write khung `docs/team/retro/<date>.md` từ `<kit>/templates/artifacts/retro.md` ngay; đã có (chạy lại) → đọc, đối chiếu với số liệu hiện tại (số liệu mới thắng), điền tiếp từ mục trống đầu tiên.
2. **Kê nguồn.** Mỗi nguồn: số dòng trong kỳ, feature nào. Nguồn thiếu → dòng "không kiểm: thiếu <nguồn>" và thu hẹp kết luận.
3. **Định lượng.** `python3 "<kit>/scripts/measure.py" --since <date>`; dán đầu ra: điểm hiệu quả, xu hướng, bất thường, xếp hạng cần chú ý. Làm mới `scorecard.json` khi cần: `python3 "<kit>/scripts/team.py" scorecard`.
4. **Theo dõi retro trước.** Với từng đề xuất cũ trong `docs/team/proposals/*/`: đã duyệt chưa (`Approved-by:`), canary đã chạy chưa (journal của việc cỡ S), kết quả giữ/rollback/thay/bỏ — có nguồn; không tìm thấy → "không tìm thấy bằng chứng" (khác "chưa làm").
5. **Định tính.** Đọc journal các feature trong kỳ; gắn mỗi điểm nghẽn ứng viên với dòng số liệu + dòng journal. Phát hiện từ Explore hay agent khác coi là chưa kiểm: mở lại nguồn gốc trước khi dựa vào.
6. **Luật mẫu tối thiểu (điểm quyết định, K-38).** Đề xuất chỉ khi ≥ 2 lần trên ≥ 2 feature, hoặc xu hướng/bất thường của `measure.py` trên ≥ 3 lượt cùng đối tượng và cỡ. Ít hơn — kể cả một lần vượt trần config — vào `## Theo dõi`, không có file đề xuất. Mỗi đề xuất ghi số feature, số lượt, độ tin cậy.
7. **Chọn ≤ 3 điểm nghẽn.** Mỗi điểm hai quyết định: lần này (đề xuất / hoãn — theo dõi / chấp nhận, ghi để retro sau không nêu lại) và phòng ngừa (nguyên nhân nào trong 5).
8. **Chẩn đoán 5 nguyên nhân.** Bảng: mỗi ô dẫn nguồn hoặc "không rõ". Đầu vào và cỡ task thường là nguyên nhân thật; đừng mặc định là prompt.
9. **Đề xuất.** Write `docs/team/proposals/<date>/<agent-or-skill>.md` từ `<kit>/templates/artifacts/proposal.md`: bằng chứng, bảng 5 nguyên nhân, nội dung ĐẦY ĐỦ file overlay (dòng đầu `# Overlay from retro <date>: <reason>`, phiên bản), dạng sửa khớp loại lỗi (bảng tự bào chữa cho bỏ bước, ô mẫu cho thiếu phần, công thức cho sai hình dạng, luật theo điều kiện quan sát được), eval, canary, rollback. Chi tiết eval và canary: `${CLAUDE_SKILL_DIR}/references/proposal-eval.md`.
10. **Eval phân biệt được.** ≥ 3 kịch bản theo định dạng `evals/<skill>/scenarios.md`; ít nhất một check bản hiện tại TRƯỢT và bản đề xuất qua; một kịch bản đối chứng không đổi; check qua ở cả hai bản bị ghi "không phân biệt". Nói rõ ai chạy (`evals/run-eval.sh`, người/người bảo trì kit).
11. **Kiểm tra chéo cấu hình.** Gọi thừa: số VAI team-leader tự gọi mỗi feature (kể cả skill fork; không tính dev/reviewer do tech-lead gọi, K-15) so với `max_agents_per_feature[cỡ]`. Quy tắc STD mức 1 vi phạm ≥ 2 lần → đề xuất nâng mức.
12. **Rà registry.** Từ `skills-registry.md`: `temp` không dùng > 30 ngày → đề xuất `retired`; `temp` ổn định → `project` (người duyệt); số `temp` so với `max_temp_skills`. coach không ghi registry: đây là đề xuất cho team-leader.
13. **Giả định (`--decide`).** Ghi mọi giả định (kỳ chọn, feature tính, nhãn độ tin cậy) vào mục `## Giả định`.
14. **Hoàn tất** `docs/team/retro/<date>.md`; memory: kết luận có ngày, không dữ liệu nhạy cảm; trả team-leader ≤ 10 dòng, dòng đầu `coach -> team-leader | retro <date> | <N> đề xuất, <M> theo dõi`.

## Đầu ra
- `docs/team/retro/<date>.md`; `docs/team/proposals/<date>/*.md`; memory của coach.
- Tin trả mẫu:
  ```
  coach -> team-leader | retro 2026-11-16 | 1 đề xuất, 2 theo dõi
  measure.py --since 2026-11-09: 14 lượt; bất thường: reviewer turns 2,6 MAD (cỡ M)
  Điểm nghẽn: reviewer chạm maxTurns 3/5 lần trên FEAT-021, FEAT-024 (journal FEAT-021 dòng 4)
  Nguyên nhân: đầu vào (design.md thiếu touchpoints) — không phải prompt
  Đề xuất: proposals/2026-11-16/designer.md (overlay v2, 3 kịch bản, 1 check bản hiện tại trượt; canary 3 việc S)
  Theo dõi: analyst chậm 1 lần (FEAT-024); vượt max_agents S 1 lần (FEAT-022)
  Retro trước: config-max-agents không tìm thấy Approved-by. Tiếp: người đọc retro/2026-11-16.md
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Một feature chậm là đủ để đề xuất" | ≥ 2 lần hoặc xu hướng; ít hơn → theo dõi (K-38). |
| "Sửa luôn file agent cho nhanh" | Đề xuất overlay; người duyệt. |
| "Eval chỉ cần đường thuận" | ≥ 3 kịch bản, có check bản hiện tại trượt, có đối chứng. |
| "Thiếu token/log thì bỏ qua" | Ghi "không đo", thu hẹp kết luận. |
| "Đề xuất cũ chắc đã áp" | Tìm `Approved-by` và canary; không có → "không tìm thấy bằng chứng". |
| "Nguyên nhân là prompt" | Điền đủ 5 ô có nguồn; đầu vào và cỡ hay là thủ phạm. |
| "Thêm chữ PHẢI vào skill là xong" | Chọn dạng sửa theo loại lỗi. |
| "Kết quả scorecard là chuẩn" | `result` đoán từ chữ; gắn nhãn độ tin cậy. |
| "Chạy eval cho chắc" | Không chạy được; viết kịch bản và nói ai chạy. |

## Dấu hiệu sai
- Đề xuất không có số feature, số lượt, độ tin cậy.
- Ô bằng chứng không có đường dẫn hay số dòng nguồn.
- Đề xuất < 3 kịch bản eval, hoặc không có check bản hiện tại trượt.
- Overlay thiếu dòng `# Overlay from retro <date>: <reason>` hoặc phiên bản.
- coach ghi ngoài `docs/team/retro/**`, `docs/team/proposals/**`, `.team/current.json`, `scorecard.json`, memory.
- Hơn 3 điểm nghẽn; không có mục theo dõi retro trước.
- Retro không dán đầu ra `measure.py`.

## Kiểm chứng
- [ ] Đầu ra `measure.py --since …` được dán.
- [ ] `ls docs/team/proposals/<date>/` khớp danh sách đề xuất trong retro.
- [ ] Mỗi đề xuất có dòng overlay, bảng 5 nguyên nhân có nguồn, ≥ 3 kịch bản eval, canary, rollback.
- [ ] Bảng theo dõi retro trước và bảng gọi thừa (với cách đếm K-15) có trong retro.
- [ ] Bảng nguồn cho thấy nguồn nào đã kiểm, nguồn nào thiếu.

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/proposal-eval.md` — mẫu eval phân biệt được, canary, tiêu chí giữ/rollback/thay/bỏ. Mở ở bước 9–10.
- Agent `coach`; `<kit>/templates/artifacts/{retro,proposal}.md`; `scripts/measure.py`.
- `/team:audit-kit` (lỗi của kit); `workflows/retro.md`, `workflows/batch/weekly-retro.md`; `docs/07-improvement.md`.
