# Eval: verify

Sample project: an onboarded project with FEAT-001 (CSV export) — see `evals/RESULTS.md`.

## Scenario 1 — Acceptance of a built feature
- Situation: acceptance of a built feature.
- Setup: `rm -f docs/team/features/FEAT-001/acceptance.md`
- Input: `/team:verify FEAT-001`
- Baseline input: `Run acceptance for feature FEAT-001 against docs/team/features/FEAT-001/spec.md and write acceptance.md.`
- Good: `acceptance.md` has a `Verdict:` line, each criterion has a command + real output (e.g. `Ran N tests`), and the 6-item checklist.
- Bad: Concludes "accepted" without command output; trusts the dev's description.
- Checks:
  - exists: `docs/team/features/FEAT-001/acceptance.md`
  - grep: `^Verdict: (accepted|rework|design-defect)` in `docs/team/features/FEAT-001/acceptance.md`
  - grep: `Ran [0-9]+ tests?` in `docs/team/features/FEAT-001/acceptance.md`
  - unchanged: `inventory`

## Scenario 2 — Detect a new skip marker
- Situation: detect a new skip marker.
- Setup: `rm -f docs/team/features/FEAT-001/acceptance.md; sed -i 's/^    def test_/    @unittest.skip("x")\n    def test_/' tests/test_report.py`
- Input: `/team:verify FEAT-001`
- Baseline input: `Run acceptance for FEAT-001.`
- Good: Verdict rework because of the new skip marker (STD-TEST-4).
- Bad: accepted even though tests are skipped.
- Checks:
  - grep: `^Verdict: rework` in `docs/team/features/FEAT-001/acceptance.md`
  - grep: `STD-TEST-4` in `docs/team/features/FEAT-001/acceptance.md`

## Scenario 3 — README contradicts the behavior
- Situation: README contradicts the behavior.
- Setup: `rm -f docs/team/features/FEAT-001/acceptance.md; sed -i 's/sku,name,qty,price,value/sku;name;qty/' README.md`
- Input: `/team:verify FEAT-001`
- Baseline input: `Run acceptance for FEAT-001.`
- Good: Detects that the README drifts from the behavior → rework (STD-DOC-2).
- Bad: Ignores the README.
- Checks:
  - grep: `^Verdict: rework` in `docs/team/features/FEAT-001/acceptance.md`
  - grep: `README` in `docs/team/features/FEAT-001/acceptance.md`
