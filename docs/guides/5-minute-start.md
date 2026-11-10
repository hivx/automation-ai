# Start in 5 minutes

1. **Install** (inside Claude Code):
   ```
   /plugin marketplace add hivx/automation-ai
   /plugin install team@automation-ai
   ```
2. **Open the project**: `cd <project> && claude`.
3. **Does the project already have code?**
   - Yes: `/team:takeover`. Read `docs/team/assessment.md` and `docs/team/ai-readiness.md`. Add `Approved-by: <name> <YYYY-MM-DD>` at the top of `ai-readiness.md`.
   - No (empty repo): skip this step.
4. **Configure the team**: `/team:onboard` (empty repo: `/team:onboard --new`). Check `.team/profile.json`, especially `cmd.test_one`. Artifacts are written in Vietnamese by default; set `"output_language": "en"` in `.team/config.json` for English.
5. **Hand over the first piece of work**: `/team:intake "Add a CSV export button to the order list"`.
6. **Follow along**: `/team:status`. When the team stops at a gate, read the artifact it names, add the `Approved-by:` line, then `/team:run`.

Want the team to run without asking: `/team:intake --decide "<request>"`. Want to turn a gate off entirely: set it to `false` in `.team/config.json → gates`; "fully automatic" = every gate `false` except `G5_prod`, plus `default_mode: "decide"`.

Next: `want-x-type-y.md`, `decision-tree.md`.
