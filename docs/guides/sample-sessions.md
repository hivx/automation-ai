# Phiên mẫu (rút gọn từ lần chạy thật)

Ba phiên dưới đây rút từ lần chạy end-to-end ngày 2026-11-09 (Claude Code 2.1.319) trên dự án mẫu `sample-existing`: thư viện Python `inventory` 3 module, 24 commit, README hứa `to_csv` nhưng code chưa có, một test bị skip, CLAUDE.md cũ 120 dòng. Chỉ giữ lệnh, quyết định và phán quyết; bỏ chi tiết gọi tool. Chi phí là con số Claude Code in ra.

## 1. Ngày đầu trên dự án có sẵn (takeover → G0 → onboard)

```
người> /team:takeover
team-leader: T0 detect-stack.sh --deep (24 commit, 3 tác giả, 1 dấu skip, 1 TODO)
             T1 README, CLAUDE.md, Makefile, .env.example (4 tài liệu)
             T2 đọc trực tiếp, < 30 file (11 file theo dõi)
             T3 không chạy: mâu thuẫn đã giải thích ở T2
  → docs/team/assessment.md      Làm gì: thư viện tồn kho 3 module.
                                 Tới đâu: README hứa to_csv — code không có (grep: 0);
                                          test_remove_unknown_sku bị skip ("flaky on CI", repo không có CI).
                                 Tiếp theo: viết lại CLAUDE.md; cài to_csv hoặc bỏ khỏi README; ...
  → ai-readiness.md  Verdict: clean-first — CLAUDE.md mô tả app Django không tồn tại → Viết lại
  → profile-proposal.md  cmd.test = make test; cmd.test_one = python3 -m unittest {file}; cmd.lint = make lint
  (35 lượt, $0.27; không file nguồn nào bị sửa)
người> (thêm "Approved-by: Miyano 2026-11-09" vào ai-readiness.md)
người> /team:onboard
team-leader: profile + config (check-profile: hợp lệ); CLAUDE.md: chèn khối 16 dòng, 120 dòng cũ giữ nguyên;
             .claude/settings.json (agent team:team-leader), settings.local.json (Read kit), 4 rule;
             make lint → 0; make test → "Ran 4 tests … OK (skipped=1)"
             Việc tay: viết lại CLAUDE.md; điền approvers; cài security-guidance (chỉ in lệnh)
  (57 lượt, $0.38)
```

## 2. Tính năng cỡ S (intake → run → verify, dừng ở G4)

```
người> /team:intake "Implement the feature the README promises" --size S --decide
team-leader: FEAT-001 · playbook new-feature · cỡ S · decide
             lý do: README.md dòng 8 hứa to_csv, grep "csv" trong inventory/ = 0      ($0.19)
người> /team:run FEAT-001 --until-blocked
  analyst  → spec.md: 5 tiêu chí AC-1..AC-5, mỗi cái có lệnh kiểm; DoD gồm CHANGELOG   (SPECIFIED)
  tech-lead → tasks.md: T1 to_csv + test + README + CHANGELOG
    dev (worktree)   test hỏng trước → to_csv → make test xanh → commit "feat(report): add to_csv (FEAT-001)"
    reviewer         request-changes: price âm rất nhỏ in "-0.00" (major)
    dev (vòng sửa)   "fix(report): normalise negative zero in to_csv (FEAT-001)"
    reviewer         approve → review-01.md; gộp vào team/FEAT-001; make test: 11 tests OK (skipped=1)
  qa       → acceptance.md: "Ran 8 tests … OK"; make test "Ran 11 tests"; make lint 0
             Verdict: accepted
team-leader: dừng — WAITING_FOR_APPROVAL G4_uat (docs/team/features/FEAT-001/acceptance.md)
```

Nhật ký `docs/team/journal/FEAT-001.md`:
```
- 2026-11-09 intake → team-leader | new-feature, S, decide | intake.md | — | good | README hứa to_csv nhưng code chưa có; cỡ S do người ép
- 2026-11-09 build → tech-lead | skill team:build (playbook new-feature, S) | tasks.md 1 task | — | good | không có design.md vì cỡ S
- 2026-11-09 verify → qa | xong | acceptance.md | — | good | accepted; dừng ở G4
```

Lỗi của kit lộ ra trong phiên này (đã sửa trong v0.1.0): status kẹt ở `planned` vì `- [x] **T1**` in đậm (K-11); team-leader dừng ở G1 dù cỡ S bỏ G1 (K-02); ghi journal bằng `printf` bị từ chối (K-12). Xem `docs/kit-issues.md`.

## 3. Nhìn lại (retro)

```
người> /team:retro --decide
coach: measure.py --since 2026-11-09 → hạng 1 cần chú ý: team:tech-lead (420 s, 46 lượt, cỡ S)
       Điểm nghẽn: FEAT-001 cỡ S gọi 5 vai / 8 lượt > trần max_agents_per_feature.S = 3;
                   journal ghi sai "agents 3 trong giới hạn"
       Chẩn đoán: config (trần 3 < chuỗi tối thiểu 5 vai) + prompt (team-leader không có cách đếm)
  → docs/team/retro/2026-11-09.md
  → docs/team/proposals/2026-11-09/team-leader.md: overlay rule "ngân sách agent", eval 5 kịch bản,
    canary 3 việc cỡ S, rollback; chờ người duyệt
  (agents/ và skills/ của kit không đổi — kiểm bằng sha256)
```
