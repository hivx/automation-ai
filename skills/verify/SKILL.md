---
name: verify
description: Dùng khi mọi task của feature đã tick và cần nghiệm thu độc lập từng tiêu chí bằng lệnh chạy thật trước khi phát hành.
argument-hint: "<ID>"
context: fork
agent: team:qa
background: false
allowed-tools: Bash(python3 *) Bash(cat *) Bash(git *)
---

## Mục đích
Ra phán quyết `accepted` / `rework` / `design-defect` có đầu ra thật.

## Đầu vào
- `$ARGUMENTS`: mã `<ID>`.
- `spec.md` (tiêu chí, DoD), `design.md` (test plan), nhánh `team/<ID>`, `.team/profile.json`. `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
Mọi task trong `tasks.md` đã tick. Kiểm: `python3 "$(cat .team/plugin_root)/scripts/team.py" status <ID>` báo `built`.

## Các bước
1. Ghi `.team/current.json` {feature, stage: "verify", agent: "qa", started_at}.
2. Checkout `team/<ID>` (git).
3. Mỗi tiêu chí: chạy lệnh kiểm (test plan / khe `cmd.*`), dán đầu ra thật, kết luận đạt/không.
4. Chạy `cmd.test`, `cmd.lint`, `cmd.typecheck`; dán đầu ra.
5. Grep diff với `config.base_branch` tìm mọi dấu trong `test.skip_markers`.
6. Có migration: `cmd.migrate` lên → xuống → lên; đối soát dữ liệu.
7. `ui: true`: Playwright MCP nếu có; không có → xin người ảnh chụp, ghi rõ.
8. Cỡ S: chỉ bước 3–5 (kiểm tự động); bỏ 6–7 khi không áp dụng.
9. DoD: As-Built (nếu đã có), README khớp hành vi, CHANGELOG.
10. Chấm Acceptance checklist (6); viết `acceptance.md` từ `<kit>/templates/artifacts/acceptance.md`, dòng `Verdict: accepted|rework|design-defect`.

## Đầu ra
- `docs/team/features/<ID>/acceptance.md`.
- Tin trả ≤ 10 dòng: phán quyết, tiêu chí trượt, file, cổng G4.

## Tiêu chí xong
- Mọi tiêu chí có lệnh + đầu ra thật; đủ 6 mục checklist; có dòng `Verdict:`.

## Dấu hiệu sai
- "CI xanh rồi" → vẫn chạy lại.
- "Hiển nhiên đạt" → chạy và dán.
- "Bỏ migration xuống" → vẫn chạy.
- "Lỗi ở thiết kế nhưng code đúng thiết kế" → `design-defect`.

## Lệnh tiếp theo
`accepted`: "Duyệt `acceptance.md` (G4) rồi `/team:asbuilt <ID>`". `rework`: `/team:build <ID> --task T<N>`. `design-defect`: `/team:design <ID>`.
