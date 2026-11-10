<!-- GENERATED — do not edit; run scripts/gen-guides.py -->
# Skills of the `team` plugin

Each folder is a `/team:<name>` command. With a local install, type `/team-<name>`.

| Skill | Invoked by | Runs as role | Artifacts |
|---|---|---|---|
| [`analyze`](analyze/SKILL.md) | both | analyst | `docs/team/features/<ID>/spec.md`, `<kit>/templates/artifacts/spec.md`, `docs/team/features/<ID>/questions.md` |
| [`architect`](architect/SKILL.md) | both | architect | `docs/team/architecture.md`, `docs/team/features/<ID>/arch-impact.md`, `arch-impact.md` |
| [`asbuilt`](asbuilt/SKILL.md) | both | writer | `docs/team/features/<ID>/asbuilt.md`, `docs/team/features/<ID>/pr-body.md`, `CHANGELOG.md` |
| [`audit-kit`](audit-kit/SKILL.md) | human | coach | `docs/team/kit-issues.md` |
| [`build`](build/SKILL.md) | both | tech-lead | `team/<ID>`, `docs/team/features/<ID>/tasks.md`, `review-NN.md` |
| [`ci`](ci/SKILL.md) | human | devops | `team/ci-<slug>`, `docs/team/ci.md`, `debt.md` |
| [`clean`](clean/SKILL.md) | both | maintainer | `team/<ID>`, `docs/team/features/<ID>/tasks.md`, `docs/team/debt.md` |
| [`commit`](commit/SKILL.md) | both | dev, maintainer | `team/<ID>-…` |
| [`design`](design/SKILL.md) | both | designer | `docs/team/features/<ID>/design.md`, `questions.md` |
| [`feedback`](feedback/SKILL.md) | both | team-leader | — |
| [`handbook`](handbook/SKILL.md) | Claude | every role (preloaded) | — |
| [`intake`](intake/SKILL.md) | both | team-leader | — |
| [`make-agent`](make-agent/SKILL.md) | both | team-leader | `.claude/agents/<name>.md`, `docs/team/agents/<name>.tests.md`, `docs/team/skills-registry.md` |
| [`make-skill`](make-skill/SKILL.md) | both | team-leader | `.claude/skills/<name>/SKILL.md`, `.claude/skills/<name>/references/tests.md`, `docs/team/skills-registry.md` |
| [`onboard`](onboard/SKILL.md) | human | team-leader | `.team/profile.json`, `.team/config.json`, `CLAUDE.md` |
| [`plan`](plan/SKILL.md) | both | tech-lead | `docs/team/features/<ID>/plan.md`, `<kit>/templates/artifacts/plan.md`, `docs/team/features/<ID>/tasks.md` |
| [`pr`](pr/SKILL.md) | both | tech-lead | `docs/team/journal/<ID>.md` |
| [`release`](release/SKILL.md) | human | team-leader | `CHANGELOG.md`, `docs/team/features/<ID>/asbuilt.md` |
| [`research`](research/SKILL.md) | both | researcher | `docs/team/features/<ID>/research.md`, `docs/team/research/<topic>@<version>.md` |
| [`retro`](retro/SKILL.md) | human | coach | `docs/team/retro/<date>.md`, `docs/team/proposals/<date>/*.md` |
| [`run`](run/SKILL.md) | human | team-leader | — |
| [`session`](session/SKILL.md) | human | team-leader | `.team/session/plan.md`, `.team/session/notes-<ID>.md` |
| [`status`](status/SKILL.md) | both | team-leader | — |
| [`takeover`](takeover/SKILL.md) | human | team-leader | `docs/team/assessment.md`, `docs/team/ai-readiness.md`, `docs/team/profile-proposal.md` |
| [`using-team`](using-team/SKILL.md) | both | team-leader, tech-lead (preloaded) | — |
| [`verify`](verify/SKILL.md) | both | qa | `docs/team/features/<ID>/acceptance.md`, `<kit>/templates/artifacts/acceptance.md`, `.team/current.json` |
