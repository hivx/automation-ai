---
name: audit-kit
description: Dùng khi cần kiểm toán chính bộ kit team đang chạy trong dự án: hook có thể bị lách, quyền quá rộng, chỉ dẫn mâu thuẫn, tên lệch, skill không dùng, agent chạm trần lượt.
argument-hint: "[--since <YYYY-MM-DD>]"
disable-model-invocation: true
context: fork
agent: team:coach
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(jq *) Bash(ls *)
---

# Kiểm toán bộ kit

## Tổng quan
Skill này tìm lỗi của BỘ KIT — agent, skill, hook, script, template — không phải lỗi của dự án, và ghi mỗi lỗi kèm bằng chứng vào `docs/team/kit-issues.md` để người báo lên repo `automation-ai`. Skill chạy trong ngữ cảnh `coach` (fork): Bash chỉ đọc, không gọi vai nào, không sửa file của kit. Một lỗi tìm được là một dòng; sửa là việc của người bảo trì kit.

Góc nhìn: luật máy (hook, permission, script) là luật; mọi chỗ luật máy có thể bị lách, mở khi lỗi, hay nói một đằng làm một nẻo là lỗi nặng hơn văn bản sai. "0 vấn đề" chỉ có nghĩa khi mỗi kiểm ghi rõ phạm vi đã kiểm; kiểm không chạy được thì ghi "bỏ qua: <lý do>", không im lặng.

`$ARGUMENTS`: `--since <YYYY-MM-DD>` cho các kiểm theo số liệu (mặc định 30 ngày). `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- Định kỳ (cùng nhịp retro), hoặc sau khi nâng phiên bản kit.
- Hook chặn nhầm hay để lọt một lần; agent làm trái luật mà không bị chặn.
- `/team:retro` thấy nguyên nhân nằm ở kit (prompt, hook, template) chứ không ở dự án.

Không dùng khi:
- Muốn tìm nợ kỹ thuật của dự án → `debt.md`, `/team:clean`.
- Muốn đề xuất sửa một agent/skill dựa trên số liệu hiệu quả → `/team:retro` (đề xuất có eval, canary).
- Muốn sửa luôn lỗi kit → không ở đây; báo lên repo kit.

## Tìm hiểu stack trước
1. Read `.team/plugin_root` → `<kit>`; `realpath` của `<kit>` và của gốc dự án.
2. Read `<kit>/hooks/hooks.json`, `<kit>/hooks/role-policy.json`, `<kit>/templates/schemas/profile.schema.json`.
3. Glob `<kit>/agents/*.md`, `<kit>/skills/*/SKILL.md`, `.claude/skills/*/SKILL.md`, `.claude/agents/*.md`; Read `docs/team/skills-registry.md`.
4. Số liệu: `docs/team/metrics/runs.jsonl` (có hay không, bao nhiêu dòng từ mốc).
5. Danh sách vấn đề đã biết: `<kit>/docs/kit-issues.md` nếu đọc được (để chống trùng).

## Đầu vào và điều kiện trước
- Kit đọc được tại `<kit>`; không đọc được → `BLOCKED`, nêu đường dẫn.
- Không có `runs.jsonl`: VẪN chạy kiểm tĩnh; các kiểm theo số liệu ghi "bỏ qua: không có dữ liệu". Thiếu số liệu không phải lý do dừng (khác retro).
- Nơi ghi (K-44): `<kit>` trùng gốc dự án, hoặc gốc dự án nằm trong `<kit>` (đang chạy trong chính repo kit) → KHÔNG ghi `docs/team/kit-issues.md`; in các dòng ra tin trả theo cột của `docs/kit-issues.md` và nói "chép vào docs/kit-issues.md".

## Quy trình
1. **Ghi vị trí.** Write `.team/current.json` {feature: "audit-kit", stage: "audit", agent: "coach", started_at}.
2. **Quyết nơi ghi** theo điều kiện K-44 ở trên; ghi kết luận vào đầu báo cáo.
2a. **Khung trước, ghi dần (K-74).** Write `docs/team/kit-issues.md` từ mẫu ngay: bảng phạm vi có đủ S1–S14, D1–D3 với trạng thái "chưa chạy". Sau mỗi nhóm 3–4 kiểm, Edit thêm dòng vấn đề và cập nhật phạm vi. 17 kiểm không vừa một lần chạy 40 lượt: hết lượt giữa chừng thì file vẫn giữ kết quả tới đó; chạy lại → đọc bảng phạm vi, làm tiếp các kiểm "chưa chạy". Mỗi kiểm tối đa vài lệnh; thử nhiều dạng lệnh thì gộp vào một lệnh, không một lệnh mỗi dạng.
3. **Kiểm tĩnh S1–S14** theo `${CLAUDE_SKILL_DIR}/references/checks.md`, lần lượt. Mỗi kiểm: lệnh hoặc file đã đọc → kết quả → dòng phạm vi (`đã kiểm: N file / bỏ qua: lý do`).
4. **Ưu tiên luật máy.** Với hook (S2, S3, S4): đọc code của script, không chỉ đọc tài liệu. Một hook "có" nhưng matcher thiếu tool hay mở khi lỗi là lỗi, dù tài liệu nói đã chặn.
5. **Danh sách ghi của vai (S5).** So ba nơi cho từng vai: `role-policy.json`, câu "chỉ ghi …" trong agent, SPEC §3 + ADJ. Lệch → một dòng, dán ba trích dẫn.
6. **Kiểm theo số liệu D1–D3** khi có `runs.jsonl`: dùng `jq` đọc; ghi rõ dữ liệu nào không có (skill không ghi số liệu ≠ skill không dùng; `result` đoán từ chữ).
7. **Phân mức.** blocker = làm quy trình kẹt hay kết quả sai không ai biết; major = lách được luật máy, quyền rộng hơn hợp đồng; minor = lệch tên, tài liệu, mô tả. Mỗi mức kèm một câu lý do.
8. **Chống trùng.** So với `<kit>/docs/kit-issues.md`: trùng → "đã có (K-xx)" kèm bằng chứng mới; mới → "mới".
9. **Bằng chứng mỗi dòng.** `file:line` hoặc lệnh + đầu ra. Không có bằng chứng → không ghi dòng đó.
10. **Viết.** Write `docs/team/kit-issues.md` từ `<kit>/templates/artifacts/kit-issues.md` (cột `ID | Mức | Trạng thái | Nơi | Hiện tượng | Đề xuất` và bảng phạm vi), hoặc in ra tin trả nếu K-44.
11. **Kiểm cuối.** `git status --short`: chỉ `docs/team/kit-issues.md`, `.team/current.json` (và memory của coach) đổi. Số dòng theo mức trong tin trả = trong file.
12. **Trả** team-leader ≤ 10 dòng, dòng đầu `coach -> team-leader | audit-kit <date> | <N> vấn đề`.

## Đầu ra
- `docs/team/kit-issues.md` (hoặc các dòng trong tin trả khi chạy trong repo kit).
- Tin trả mẫu:
  ```
  coach -> team-leader | audit-kit 2026-11-16 | 5 vấn đề (0 blocker, 2 major, 3 minor)
  File: docs/team/kit-issues.md (14 kiểm tĩnh; 3 kiểm số liệu: 2 chạy, 1 bỏ qua — không có dữ liệu skill)
  Major: A-01 role-policy cho `uniq IN OUT` (teamlib.py:398, mới); A-02 clean-sweep thiếu cmd.* trong --allowedTools (đã có K-06)
  Minor: A-03 mô tả skill `foo` 540 ký tự; A-04 coach ghi lệch ba nơi (đã có K-43); A-05 docs nhắc một lệnh skill không có thư mục skills/
  Phạm vi: 13 agent, 26 skill, 2 skill tạm, 9 hook
  Người cần làm: báo A-01, A-05 lên repo automation-ai
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Không có runs.jsonl thì bỏ" | Chạy kiểm tĩnh; kiểm số liệu ghi "không có dữ liệu". |
| "Hook có rồi nên đã được thi hành" | Đọc matcher, mã thoát, đường lỗi của script. |
| "Đây là lỗi dự án, ghi luôn" | Chỉ lỗi kit; lỗi dự án qua team-leader vào `debt.md`. |
| "Tìm ra lỗi hook, sửa luôn" | coach không sửa file kit (SPEC §3). |
| "jq không ra gì, vậy 0 skill thừa" | Dữ liệu rỗng không phải sạch; ghi phạm vi. |
| "Lỗi này lần trước đã báo, bỏ qua" | Ghi "đã có (K-xx)" với bằng chứng mới. |
| "Chạy validate.sh cho nhanh" | Script đó ghi file; chỉ dùng lệnh chỉ-đọc. |
| "Ghi kit-issues ngay trong repo kit" | K-44: in ra tin trả để người chép. |
| "Viết báo cáo một lần ở cuối" | Khung trước, ghi sau mỗi nhóm; hết lượt vẫn còn kết quả (K-74). |

## Dấu hiệu sai
- Dòng vấn đề không có `file:line` hay lệnh + đầu ra.
- Mức không kèm lý do; mức không thuộc blocker/major/minor.
- Một dòng nói về code của dự án.
- "0 vấn đề" mà không có bảng phạm vi.
- coach ghi file ngoài danh sách ghi của mình, hoặc chạy script có ghi.
- Ghi `docs/team/kit-issues.md` khi đang chạy trong repo kit.

## Kiểm chứng
- [ ] Mỗi kiểm S1–S14, D1–D3 có lệnh + kết quả, hoặc "bỏ qua: lý do".
- [ ] Mỗi dòng vấn đề có `file:line` hoặc lệnh + đầu ra.
- [ ] Nơi ghi (file hay tin trả) được nêu và đúng điều kiện K-44.
- [ ] Số vấn đề theo mức trong tin trả bằng số dòng trong file.
- [ ] `git status --short` chỉ có file trong vùng ghi của coach.

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/checks.md` — 14 kiểm tĩnh, 3 kiểm số liệu, cách chống trùng. Mở ở bước 3 và 6.
- Agent `coach`; `<kit>/templates/artifacts/kit-issues.md`.
- `/team:retro` (đề xuất sửa có eval); `handbook/tool-selection.md` (điều gì phải là luật máy).
- `handbook/STD.md`: STD-SEC-1, STD-SEC-5, STD-SEC-8.
