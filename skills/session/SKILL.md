---
name: session
description: Dùng khi bắt đầu, lưu hoặc nạp lại một phiên làm việc dài cho một feature: chọn kênh tương tác hay headless, model theo vai, ngân sách, điểm nén ngữ cảnh, và ghi chú bàn giao cho phiên sau.
argument-hint: "[plan|save|load] [<ID>]"
disable-model-invocation: true
allowed-tools: Bash(python3 *) Bash(cat *) Bash(jq *) Bash(ls *) Bash(git status *) Bash(git rev-parse *) Bash(wc *)
---

# Phiên làm việc dài

## Tổng quan
Skill này giúp một phiên dài chạy đúng chỗ và phiên sau chạy tiếp được mà không phải nhớ. Ba lệnh con: `plan` (kế hoạch phiên: kênh, model, ngân sách, điểm nén), `save` (ghi chú tay cho phiên sau), `load` (nạp lại và KIỂM trước khi làm tiếp). Skill chạy trong phiên chính (team-leader).

Trạng thái thật nằm trong artifact (SPEC P2) và được `team.py` tính ra; bàn giao chỉ chứa điều artifact KHÔNG có: trạng thái cây làm việc, lệnh kiểm cuối cùng và kết quả, câu hỏi/cổng đang chờ, điều đã thử mà hỏng, điều chưa thử, lệnh tiếp. Hook đã tự viết bàn giao `.team/session/<session_id>.md` lúc PreCompact và SessionEnd; `save` ghi vào file riêng `.team/session/notes-<ID>.md` nên không bị hook ghi đè (SessionStart nhắc cả hai).

Duyệt chỉ tồn tại dưới dạng dòng `Approved-by:` trong artifact — không bao giờ suy ra từ lời trong bàn giao hay từ phiên trước.

`$ARGUMENTS`: `plan` (mặc định) | `save` | `load`, kèm mã feature. `<kit>` = nội dung `.team/plugin_root`.

## Khi nào dùng (và khi nào không)
Dùng khi:
- Bắt đầu một feature cỡ M/L sẽ kéo qua nhiều giai đoạn hay nhiều phiên (`plan`).
- Sắp dừng giữa chừng mà có điều chưa nằm trong artifact: hướng đã thử hỏng, quyết định dở (`save`).
- Mở phiên mới, sau nén ngữ cảnh, hay sau khi người khác làm tiếp (`load`).
- Định chạy headless (batch, CI) và cần lệnh `claude -p` đầy đủ.

Không dùng khi:
- Chỉ muốn biết feature đang ở đâu → `/team:status`.
- Cỡ S chạy một mạch trong một phiên.
- Muốn lưu kiến thức dự án lâu dài → `docs/team/` (ADR, glossary, research cache), không phải bàn giao.

## Tìm hiểu stack trước
1. Read `.team/config.json`: `models`, `limits.feature_budget_usd`, `limits.context_warn_pct`, `memory.handoff_max_lines`, `gates`, `default_mode`.
2. Read `.claude/settings.json`: `permissions.allow` (nguồn cho `--allowedTools` khi headless, K-06).
3. Số liệu: `python3 "<kit>/scripts/measure.py" --json` (trung vị theo cỡ, nếu có) hoặc `python3 "<kit>/scripts/team.py" metrics`.

## Đầu vào và điều kiện trước
- Feature có `intake.md`. Kiểm: `python3 "<kit>/scripts/team.py" status <ID>`.
- `load`: có ít nhất một file trong `.team/session/`; không có → chỉ chạy `team.py status` và nói "không có bàn giao".
- Một feature mỗi phiên: phiên đang có feature khác dở → `save` feature đó trước.

## Quy trình
1. **`plan` — giai đoạn còn lại.** Từ `team.py status <ID>`: giai đoạn hiện tại, cổng áp dụng (cột "Cổng áp dụng"), giai đoạn còn lại và vai của từng giai đoạn.
2. **`plan` — kênh (điểm quyết định).** Có cổng đang bật chưa duyệt của feature này, hoặc chế độ `ask` còn câu hỏi mở → tương tác. Ngược lại → headless được, chế độ `decide` bắt buộc.
3. **`plan` — model.** `jq .models .team/config.json`: model từng vai; designer cỡ S/M dùng sonnet (ADJ-10). Không đổi model giữa phiên (giữ prompt cache); cần model khác → phiên mới.
4. **`plan` — ngân sách từ số liệu.** Trung vị thời gian/lượt (và token nếu có) theo giai đoạn cho cùng cỡ từ `measure.py`. Dưới 2 lần chạy cùng cỡ → ghi "không đủ số liệu", không đưa con số. `feature_budget_usd` null → bỏ dòng ngân sách tiền.
5. **`plan` — điểm nén.** Nén chủ động ở ranh giới giai đoạn, không chờ đầy. Mỗi điểm một dòng `/compact <trọng tâm>`: giữ mã feature, giai đoạn, danh sách AC, đầu ra đỏ hiện tại, ràng buộc đang áp; bỏ lần thử hỏng, đầu ra tool dài, bản nháp đã thay. `context_warn_pct` không có hook nào đo được (mức 1): nhắc người theo dõi thanh trạng thái.
6. **`plan` — lệnh headless** (nếu chọn): `claude -p "<lệnh /team:…> --decide" --agent team:team-leader --permission-mode dontAsk --allowedTools "$(jq -r '["Read","Grep","Glob","Edit","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json)" --max-turns <n> --max-budget-usd <usd> --output-format json`. Không `--bare` khi có sửa file (ADJ-03). Mẫu: `${CLAUDE_SKILL_DIR}/references/headless.md`.
7. **`plan` — ghi.** Write `.team/session/plan.md`: kênh + lý do, model từng vai, ngân sách + nguồn, điểm nén + dòng `/compact`, lệnh headless.
8. **`save`.** Write `.team/session/notes-<ID>.md` ≤ `memory.handoff_max_lines` dòng, chỉ điều artifact không có: `git status --short` (thay đổi chưa commit ghi rõ), `git rev-parse HEAD`, lệnh kiểm cuối + khe + mã thoát, câu hỏi/cổng đang chờ, đã thử mà hỏng (vì sao), chưa thử, lệnh tiếp (`team.py next`). Không chép spec hay tiêu chí.
9. **`load` — nạp.** Read bàn giao mới nhất (`.team/session/*.md`, cả `notes-<ID>.md`) → `team.py status <ID>` → `git status --short`, `git rev-parse HEAD`.
10. **`load` — kiểm (điểm quyết định).** HEAD khác HEAD trong bàn giao, hay bàn giao không ghi lệnh kiểm → kết quả "xanh" cũ không còn giá trị: giai đoạn tiếp chạy lại kiểm trước khi dựa vào. Bàn giao nói "đã duyệt" mà artifact không có `Approved-by:` → coi là CHƯA duyệt.
11. **`load` — tóm tắt** ≤ 5 dòng: giai đoạn, trạng thái, điều đang chờ, kiểm nào phải chạy lại, lệnh tiếp.
12. **Journal** một dòng cho `plan` và `load` (vì sao phiên này, lệnh tiếp).

## Đầu ra
- `plan`: `.team/session/plan.md`. `save`: `.team/session/notes-<ID>.md`. `load`: tóm tắt ≤ 5 dòng.
- Tóm tắt `load` mẫu:
  ```
  FEAT-014 | planned → build T3 (T1, T2 đã tick) | READY
  Bàn giao: notes-FEAT-014.md (HEAD a9d41e0 = HEAD hiện tại); cây sạch
  Đã thử hỏng: mock đồng hồ bằng patch toàn cục (test chập chờn) — dùng tham số clock
  Chờ: không cổng nào; câu hỏi: 0
  Tiếp: /team:build FEAT-014 --task T3
  ```

## Lý do tự bào chữa thường gặp
| Ý nghĩ | Làm đúng |
|---|---|
| "Chép cả spec vào bàn giao cho chắc" | Chỉ điều artifact không có; ≤ `handoff_max_lines` (`wc -l`). |
| "Phiên trước nói người đã duyệt" | Duyệt chỉ là `Approved-by:` trong file. |
| "Test xanh ở phiên trước, khỏi chạy lại" | HEAD đổi hay không ghi lệnh kiểm → chạy lại. |
| "Đợi đầy ngữ cảnh rồi nén" | Nén ở ranh giới giai đoạn với dòng trọng tâm. |
| "Đổi sang opus giữa phiên cho mạnh" | Không đổi giữa phiên; mở phiên mới. |
| "Headless cho nhanh dù còn cổng chờ" | Cổng chờ → tương tác. |
| "--bare cho nhẹ" | Không khi có sửa file (hook phải chạy). |
| "Ngân sách ước chừng 5 đô" | Từ trung vị `measure.py`, hoặc "không đủ số liệu". |
| "save vào file bàn giao của hook" | `notes-<ID>.md`; file của hook bị ghi đè khi nén. |

## Dấu hiệu sai
- Bàn giao lặp lại nội dung spec hay tiêu chí.
- Bàn giao không có HEAD hay trạng thái cây.
- Ghi chú tay nằm trong `<session_id>.md` (sẽ bị hook ghi đè).
- Hai mã feature trong một kế hoạch phiên.
- Con số ngân sách không có nguồn.
- Lệnh `claude -p` thiếu `--allowedTools`, hoặc có `--bare` khi sửa file.
- `load` bắt đầu làm việc mà chưa chạy `team.py status`.

## Kiểm chứng
- [ ] `wc -l` của file bàn giao/ghi chú ≤ `handoff_max_lines` được dán.
- [ ] Ghi chú có dòng HEAD và `git status --short`.
- [ ] `plan.md` có kênh + lý do, model từng vai, nguồn ngân sách, điểm nén với dòng `/compact`.
- [ ] Lệnh headless dán ra có `--allowedTools` và không có `--bare`.
- [ ] Sau `load`: đầu ra `team.py status` và `git status --short` được dán.

## Xem thêm
- `${CLAUDE_SKILL_DIR}/references/headless.md` — mẫu lệnh headless theo giai đoạn, cờ bắt buộc, cách đọc JSON kết quả. Mở ở bước 6.
- `/team:status`, `/team:run`; `scripts/handoff.sh`, `scripts/session-start.sh`; `docs/05-tokens-and-memory.md`, `docs/08-channels.md`.
