---
name: takeover
description: Dùng khi đội nhận một repo đã có code mà chưa có .team/profile.json, hoặc người hỏi dự án này làm gì, đã tới đâu, việc tiếp theo là gì.
argument-hint: "[--full]"
disable-model-invocation: true
allowed-tools: Read Glob Bash(bash *) Bash(git log *) Bash(git branch *) Bash(git tag *) Bash(ls *) Bash(cat *) Bash(jq *) Bash(gh issue list *) Bash(gh pr list *)
---

## Mục đích
Trả lời ba câu: dự án LÀM GÌ, ĐÃ TỚI ĐÂU, VIỆC TIẾP THEO — chỉ quét và báo cáo, không sửa gì.

## Đầu vào
- `$ARGUMENTS`: rỗng, hoặc `--full` để luôn chạy T3.
- Repo hiện tại. `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
- Không có `.team/profile.json` (có rồi → dùng `/team:status`).
- `git status` sạch hoặc người đồng ý quét trên bản đang có.

## Các bước
Ngân sách từng tầng: `${CLAUDE_SKILL_DIR}/references/tiers.md`. Tầng sau chỉ chạy khi tầng trước chưa trả lời được.
1. **T0 — siêu dữ liệu, không đọc nội dung file** (Bash): `bash "<kit>/scripts/detect-stack.sh" --deep`; `git log --stat` (vùng nóng, nhịp, tác giả); `git tag`; `gh issue list`, `gh pr list` khi `gh` có. Ghi kết luận "đã tới đâu" sơ bộ.
2. **T1 — tài liệu** (Read): ≤ 15 tài liệu, đọc mục lục trước, chỉ đọc thân khi liên quan; ghi ngày cập nhật. → "làm gì" theo lời tài liệu.
3. **T2 — đối chiếu lấy mẫu** (Agent → Explore): ≤ 10 module (module chính + vùng nóng): tính năng tài liệu nói có code/test không; TODO/FIXME; test bị skip; nhánh chưa gộp; migration chưa chạy.
4. **T3 — đọc sâu** (Explore theo module): chỉ khi T2 thấy mâu thuẫn, có module không tài liệu, hoặc `--full`.
5. Kiểm sức khỏe: build/test có chạy được không — chỉ ĐỀ XUẤT lệnh, không chạy lệnh cài đặt.
6. Viết 5 báo cáo từ `<kit>/templates/artifacts/`: `assessment.md` (xương sống = 3 câu; phụ lục stack & sức khỏe, quy ước đo từ code), `ai-readiness.md`, `profile-proposal.md` (bằng chứng cho từng khe), `debt.md` (chặn / nên / để sau), `open-questions.md` (≤ 10).
7. Mỗi báo cáo có mục `## Đã quét / Chưa quét / Độ tin cậy`.
8. Cache kết luận T0–T1 vào `docs/team/explore/`.
9. Ghi journal: `docs/team/journal/takeover.md`.

## Đầu ra
- `docs/team/assessment.md`, `docs/team/ai-readiness.md`, `docs/team/profile-proposal.md`, `docs/team/debt.md`, `docs/team/open-questions.md`, `docs/team/explore/`.
- `.team/current.json` {feature: "takeover", stage: "G0"}.

## Tiêu chí xong
- Đủ 5 file, mỗi file có mục đã quét / chưa quét / độ tin cậy.
- `git status` cho thấy chỉ `docs/team/**` thay đổi — dán đầu ra.

## Dấu hiệu sai
- "Đọc hết repo cho chắc" → theo tầng và ngân sách.
- "README nói có, coi như có" → đối chiếu code ở T2.
- "Tiện sửa luôn lỗi nhỏ thấy được" → ghi `debt.md`, không sửa.
- "Chạy cài phụ thuộc để thử build" → chỉ đề xuất.

## Lệnh tiếp theo
In: "Đọc `docs/team/ai-readiness.md`, trả lời `open-questions.md`, thêm `Approved-by: <tên> <YYYY-MM-DD>` lên đầu `ai-readiness.md`, rồi chạy `/team:onboard`."
