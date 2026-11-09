---
name: pr
description: Dùng khi nhánh feature hoặc nhánh sửa CI đã sẵn sàng cần mở hay cập nhật pull request, hoặc cần trả lời bình luận review của người.
argument-hint: "<ID> [create|update|reply]"
context: fork
agent: team:tech-lead
background: false
allowed-tools: Bash(gh pr *) Bash(git fetch *) Bash(git rebase *) Bash(git push *) Bash(git log *) Bash(git status *) Bash(cat *)
---

## Mục đích
PR đúng nội dung, đúng nhánh, không bao giờ tự merge vượt luật duyệt.

## Đầu vào
- `$ARGUMENTS`: mã `<ID>` (hoặc `ci-<slug>`); `create` (mặc định), `update`, `reply`.
- `docs/team/features/<ID>/pr-body.md` (writer), `.team/config.json` (`base_branch`).

## Điều kiện trước
- Nhánh `team/<ID>` có commit; `cmd.test` xanh trên nhánh.
- `gh auth status` thành công. Không có `gh` → in nội dung PR để người tự tạo.

## Các bước
1. Ghi `.team/current.json` {feature, stage: "pr", agent: "tech-lead", started_at}.
2. `git fetch`; rebase `team/<ID>` lên `config.base_branch`; xung đột → giải mà không mất thay đổi của người khác, chạy lại `cmd.test`.
3. Push CHỈ nhánh `team/*`; không force-push dưới mọi dạng (hook `check-git.sh` chặn). Rebase làm lệch remote → push nhánh mới `team/<ID>-r<n>`.
4. `create`: `gh pr create --base <base_branch> --head team/<ID> --body-file pr-body.md`; tiêu đề theo định dạng commit.
5. `update`: `gh pr edit --body-file`.
6. `reply`: đọc bình luận (`gh pr view --comments`); mỗi bình luận trả lời dẫn mã STD hoặc mục `design.md`; đồng ý → task sửa mới cho dev; không đồng ý → nêu lý do, để người quyết.
7. Playbook docs-only: `gh pr merge --auto` (vẫn theo luật nhánh). Còn lại: KHÔNG merge.

## Đầu ra
- PR mở/cập nhật; đường dẫn PR trong journal.
- Tin trả ≤ 10 dòng: URL PR, trạng thái kiểm, bình luận còn mở.

## Tiêu chí xong
- `gh pr view --json url,state,headRefName` được dán; head là `team/*`.

## Dấu hiệu sai
- "Merge luôn cho nhanh" → chỉ người hoặc luật auto-merge.
- "Force-push cho sạch" → không.
- "Bình luận sai, bỏ qua" → trả lời có căn cứ.

## Lệnh tiếp theo
`/team:release <ID>` sau khi PR được duyệt; hoặc chờ review của người.
