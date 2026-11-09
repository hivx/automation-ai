# Playbook: new-project

## Khi nào áp dụng
- Repo rỗng hoặc chỉ có README.
- Người mô tả một hệ thống cần dựng từ đầu.

## Cỡ mặc định
L.

## Chuỗi
1. `/team:onboard --new` → team-leader → `.team/`, `.claude/`, `docs/team/`.
2. `/team:intake --size L` → team-leader → `intake.md`.
3. `/team:analyze` → analyst → `spec.md` (có DoD, NFR).
4. `/team:research` → researcher → `research.md`.
5. `/team:architect` → architect → `docs/team/architecture.md`, `docs/team/adr/ADR-NNN.md`.
6. `/team:design` → designer → `design.md`.
7. `/team:plan` → tech-lead → `plan.md`, `tasks.md`; task 1 là walking skeleton.
8. `/team:build` → tech-lead → dev, reviewer → commit, `review-NN.md`.
9. `/team:verify` → qa → `acceptance.md`.
10. `/team:asbuilt` → writer → `asbuilt.md`, CHANGELOG.
11. `/team:pr` → tech-lead → PR.
12. `/team:release` → devops → staging, rồi prod khi có `Approved-by-prod:`.

## Cổng
G1 (spec), G2 (kiến trúc), G2b nếu bật, G3 (plan), G4 (nghiệm thu), G5 (prod) — người duyệt theo `approvers` trong config.

## Điểm dừng
- Mỗi cổng bật.
- Walking skeleton không chạy được đầu-cuối: dừng trước task 2.

## Tiêu chí xong
- Walking skeleton chạy đầu-cuối; mọi tiêu chí trong `acceptance.md` đạt; CI xanh; staging smoke xanh.

## Lỗi thường gặp
- Bỏ walking skeleton, xây từng tầng riêng.
- Chọn công nghệ trước khi có NFR.
- Kiến trúc cho nhu cầu chưa có.

## Playbook liên quan
`new-feature`, `integration`, `release`.
