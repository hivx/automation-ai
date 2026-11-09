---
name: release
description: Dùng khi feature đã accepted và duyệt G4, cần merge, gắn tag, đưa lên staging rồi prod khi người đã duyệt G5.
argument-hint: "<ID> [staging|prod]"
disable-model-invocation: true
allowed-tools: Bash(python3 *) Bash(cat *) Bash(gh pr checks *) Bash(gh pr view *)
---

## Mục đích
Đưa feature đã nghiệm thu lên môi trường, không bao giờ lên prod khi thiếu duyệt của người.

## Đầu vào
- `$ARGUMENTS`: mã `<ID>`; `staging` (mặc định) hoặc `prod`.
- `acceptance.md`, `asbuilt.md`, `pr-body.md`, `.team/profile.json` (`deploy.*`). `<kit>` = nội dung `.team/plugin_root`.

## Điều kiện trước
- `team.py status <ID>` báo `verified` và G4 đã duyệt: `python3 "$(cat .team/plugin_root)/scripts/team.py" status <ID>`.
- CI xanh trên PR: `gh pr checks`.
- `asbuilt.md` có. Thiếu một điều → dừng, in điều thiếu.

## Các bước
1. Ghi `.team/current.json` {feature, stage: "release", agent: "devops", started_at}; journal một câu lý do.
2. Gọi devops (Agent, `team:devops`), mục tiêu `deploy-staging`:
   1. Merge PR đã đủ duyệt theo luật bảo vệ nhánh (không ép merge).
   2. Gắn tag phiên bản; CHANGELOG chuyển mục `[Unreleased]` sang phiên bản.
   3. `deploy.staging` → `deploy.smoke`; dán đầu ra.
3. Báo người làm UAT trên staging.
4. `prod`: kiểm khối header (20 dòng đầu) của `asbuilt.md` có `Approved-by-prod: <tên> <YYYY-MM-DD>`. KHÔNG có → dừng, in hướng dẫn duyệt G5.
5. Có duyệt → gọi devops, mục tiêu `deploy-prod`: lệnh rollback đã kiểm trước; deploy; `deploy.smoke`.
6. Smoke prod đỏ → devops đề xuất rollback ngay, báo người.
7. Xanh → thêm dòng `Released: <tag> <YYYY-MM-DD>` vào `asbuilt.md`.

## Đầu ra
- Tag; `CHANGELOG.md`; dòng `Released:` trong `docs/team/features/<ID>/asbuilt.md`; journal.

## Tiêu chí xong
- Đầu ra smoke staging (và prod khi lên prod) được dán; có dòng `Released:`.

## Dấu hiệu sai
- "Gấp, lên prod trước rồi duyệt" → dừng chờ `Approved-by-prod:`.
- "Smoke đỏ nhẹ, cứ giữ" → đề xuất rollback.
- "Ép merge cho kịp" → theo luật nhánh.
- "UAT bỏ qua lần này" → người quyết, không phải đội.

## Lệnh tiếp theo
Staging xong: "UAT, rồi thêm `Approved-by-prod:` vào `asbuilt.md` và chạy `/team:release <ID> prod`". Prod xong: `/team:status`.
