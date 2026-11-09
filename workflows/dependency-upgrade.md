# Playbook: dependency-upgrade

## Khi nào áp dụng
- Nâng phiên bản thư viện, framework, runtime.
- Có cảnh báo lỗ hổng hoặc phiên bản sắp hết hỗ trợ.

## Cỡ mặc định
M.

## Chuỗi
0. `/team:intake` → team-leader → `intake.md`.
1. `/team:research` → researcher → `research.md`: changelog, thay đổi phá vỡ, đường di trú, nguồn chính thức.
2. `/team:plan` → tech-lead → `plan.md`, `tasks.md` (một task cho mỗi thay đổi phá vỡ).
3. `/team:build` → tech-lead → dev, reviewer; lockfile chỉ đổi qua `cmd.install`.
4. `/team:verify` (đầy đủ) → qa → `acceptance.md`: `cmd.test`, `cmd.lint`, `cmd.typecheck`, `cmd.build`.
5. `/team:pr` → tech-lead → PR riêng cho lần nâng cấp.

## Cổng
G3, G4.

## Điểm dừng
- Thay đổi phá vỡ cần đổi API công khai của dự án: dừng, báo người.

## Tiêu chí xong
- Mọi thay đổi phá vỡ trong `research.md` đã có task tick; verify đầy đủ xanh.

## Lỗi thường gặp
- Nâng nhiều thư viện lớn trong một PR.
- Sửa tay lockfile.

## Playbook liên quan
`spike`, `refactor`.
