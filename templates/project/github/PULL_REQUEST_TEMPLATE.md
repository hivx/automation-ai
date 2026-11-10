## Feature
- ID: <!-- FEAT-NNN / BUG-NNN / CHG-NNN -->
- Design: `docs/team/features/<ID>/design.md`
- As-Built: `docs/team/features/<ID>/asbuilt.md`
- Acceptance: `docs/team/features/<ID>/acceptance.md` — Verdict: <!-- accepted / rework / design-defect -->

## Why
<!-- the problem or need, one or two sentences; link spec.md -->

## What changed
<!-- behavior and main files; if it differs from the design, link asbuilt.md -->

## How verified
<!-- commands run and their output (exit code), taken from acceptance.md -->

## Review checklist (handbook/STD.md)
- [ ] 1. Implements the spec correctly and completely, nothing extra (STD-DESIGN-5, STD-TEST-2)
- [ ] 2. Only within touchpoints; new files in the right place (STD-DESIGN-1, STD-STRUCT-1, STD-STRUCT-2)
- [ ] 3. Failing test first; edges and errors covered; no skip/xfail/only (STD-TEST-1, STD-TEST-8, STD-TEST-4)
- [ ] 4. Tests not changed to match wrong behavior; tests independent (STD-TEST-5, STD-TEST-6)
- [ ] 5. Errors handled; input validated; external calls have timeouts (STD-ERR-1, STD-ERR-2, STD-ERR-5)
- [ ] 6. No secrets, no injection, authorization in place (STD-SEC-1, STD-SEC-3, STD-SEC-4, STD-SEC-6)
- [ ] 7. Contracts compatible or migration reversible (STD-DESIGN-3, STD-OPS-2)
- [ ] 8. Naming, structure, style per the profile; no dead code (STD-NAME-1, STD-NAME-2, STD-STYLE-4, STD-STYLE-5)
- [ ] 9. New dependencies are justified (STD-DEP-1, STD-DEP-3, STD-DEP-5)
- [ ] 10. Commits, branch and PR follow the standard; docs come along (STD-NAME-4, STD-NAME-5, STD-GIT-1, STD-DOC-2)
