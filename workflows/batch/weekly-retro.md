# Batch: weekly-retro

## When it applies
- Every week, when there is at least one new feature or new feedback that week.

## Default size
Not applicable.

## Chain
`decide` mode is mandatory; no `--bare`.
1. `/team:retro --decide` → coach → `docs/team/retro/<date>.md`, `docs/team/proposals/<date>/`.

```yaml
on:
  schedule:
    - cron: "0 1 * * 1"   # 08:00 Monday, Vietnam time
jobs:
  retro:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - id: tools   # K-06: the runner ignores permissions.allow; pass it again with --allowedTools
        run: echo "list=$(jq -r '["Read","Grep","Glob","Write","Agent","Skill"] + (.permissions.allow // []) | join(",")' .claude/settings.json)" >> "$GITHUB_OUTPUT"
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          plugin_marketplaces: "https://github.com/<owner>/automation-ai.git"
          plugins: "team@automation-ai"
          claude_args: "--max-turns 60 --max-budget-usd 5 --allowedTools '${{ steps.tools.outputs.list }}'"
          prompt: "/team:retro --decide"
```
Plugin installation and job permissions: as in `templates/project/github/workflows/team-feature.yml`. The results (`docs/team/retro/`, `proposals/`) are committed to branch `team/retro-<date>` and a PR is opened by hand or by a `gh pr create` step added to the job.

## Gates
Proposals are only notes awaiting approval; nothing is applied.

## Stop points
- Missing metrics; the budget runs out.

## Done criteria
On Monday morning the human reads `docs/team/retro/<date>.md` and each proposal file, then approves or drops them.

## Common mistakes
- Applying an overlay automatically in the scheduled job.

## Related playbooks
`retro`.
