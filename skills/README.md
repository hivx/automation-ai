<!-- GENERATED — do not edit; run scripts/gen-guides.py -->
# Skills của plugin `team`

Mỗi thư mục là một lệnh `/team:<tên>`. Cài cục bộ thì gõ `/team-<tên>`.

| Skill | Ai gọi | Vai chạy | Artifact |
|---|---|---|---|
| [`analyze`](analyze/SKILL.md) | cả hai | analyst | `docs/team/features/<ID>/spec.md`, `<kit>/templates/artifacts/spec.md`, `docs/team/features/<ID>/questions.md` |
| [`architect`](architect/SKILL.md) | cả hai | architect | `docs/team/architecture.md`, `docs/team/features/<ID>/arch-impact.md`, `docs/team/adr/ADR-NNN.md` |
| [`asbuilt`](asbuilt/SKILL.md) | cả hai | writer | `docs/team/features/<ID>/asbuilt.md`, `pr-body.md`, `CHANGELOG.md` |
| [`audit-kit`](audit-kit/SKILL.md) | người | coach | `docs/team/kit-issues.md` |
| [`build`](build/SKILL.md) | cả hai | tech-lead | `team/<ID>`, `docs/team/features/<ID>/tasks.md`, `review-NN.md` |
| [`ci`](ci/SKILL.md) | người | devops | `team/ci-<slug>`, `docs/team/ci.md` |
| [`clean`](clean/SKILL.md) | cả hai | maintainer | `team/<ID>-clean-<kind>`, `docs/team/debt.md` |
| [`commit`](commit/SKILL.md) | cả hai | dev, maintainer | `team/<ID>-…`, `dev -> tech-lead \| FEAT-012 T3 \| DONE
  Commit: a1b2c3d fix(otp): reject expired code (FEAT-012)
  File: src/auth/otp.py, tests/auth/test_otp.py (đúng touchpoints)
  Test: <cmd.test_one tests/auth/test_otp.py> → 6 passed; lint: exit 0
  Quét staged: skip marker 0, secret 0
  Thấy nhưng không chạm: src/auth/session.py:88 nuốt lỗi (ghi debt, không sửa)` |
| [`design`](design/SKILL.md) | cả hai | designer | `docs/team/features/<ID>/design.md` |
| [`feedback`](feedback/SKILL.md) | cả hai | team-leader | — |
| [`handbook`](handbook/SKILL.md) | Claude | mọi vai (nạp sẵn) | — |
| [`intake`](intake/SKILL.md) | người | team-leader | — |
| [`make-agent`](make-agent/SKILL.md) | cả hai | team-leader | `.claude/agents/<name>.md`, `.claude/agents/<name>.tests.md` |
| [`make-skill`](make-skill/SKILL.md) | cả hai | team-leader | `.claude/skills/<name>/SKILL.md`, `.claude/skills/<name>/references/tests.md`, `docs/team/skills-registry.md` |
| [`onboard`](onboard/SKILL.md) | người | team-leader | `.team/profile.json`, `.team/config.json`, `CLAUDE.md` |
| [`plan`](plan/SKILL.md) | cả hai | tech-lead | `docs/team/features/<ID>/plan.md`, `<kit>/templates/artifacts/plan.md`, `docs/team/features/<ID>/tasks.md` |
| [`pr`](pr/SKILL.md) | cả hai | tech-lead | `docs/team/journal/<ID>.md`, `tech-lead -> team-leader \| FEAT-012 \| DONE
  PR: https://github.com/<owner>/<repo>/pull/42 — head team/FEAT-012 → base main
  cmd.test trên đầu nhánh sau rebase: exit 0, "Ran 42 tests … OK"
  Kiểm CI: pending. Không merge (chờ người duyệt).
  Bình luận: 0 mở
  Tiếp: người review PR; sau merge chạy /team:release FEAT-012` |
| [`release`](release/SKILL.md) | người | team-leader | `CHANGELOG.md`, `docs/team/features/<ID>/asbuilt.md` |
| [`research`](research/SKILL.md) | cả hai | researcher | `docs/team/features/<ID>/research.md`, `docs/team/research/<topic>@<version>.md` |
| [`retro`](retro/SKILL.md) | người | coach | `docs/team/retro/<date>.md`, `docs/team/proposals/<date>/*.md` |
| [`run`](run/SKILL.md) | người | team-leader | — |
| [`session`](session/SKILL.md) | người | team-leader | `.team/session/plan.md`, `.team/session/<id>.md` |
| [`status`](status/SKILL.md) | cả hai | team-leader | — |
| [`takeover`](takeover/SKILL.md) | người | team-leader | `docs/team/assessment.md`, `docs/team/ai-readiness.md`, `docs/team/profile-proposal.md` |
| [`using-team`](using-team/SKILL.md) | cả hai | team-leader, tech-lead (nạp sẵn) | — |
| [`verify`](verify/SKILL.md) | cả hai | qa | `docs/team/features/<ID>/acceptance.md`, `<kit>/templates/artifacts/acceptance.md`, `.team/current.json` |
