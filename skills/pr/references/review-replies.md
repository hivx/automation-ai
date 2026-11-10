# Replying to review comments

## Classification table (build it before creating any task)
| # | Comment (summary) | Checked against | Class | Grounds | Action |
|---|---|---|---|---|---|
| 1 | `to_csv` does not escape commas | code `report.py:12`, AC-1 | agree | STD-ERR-2 | task T5 |
| 2 | "Should add a full metrics endpoint" | Grep: nothing uses it | disagree | STD-DESIGN-5, spec non-goal | reply |
| 3 | "This part looks odd" | — | needs clarification | — | ask back |

## Reply templates
- Agree, fixed: `Fixed in a1b2c3d: commas and double quotes in names are now escaped (STD-ERR-2); test tests/test_report.py::test_csv_quotes.`
- Disagree: `Not changed: spec FEAT-012 lists metrics as a non-goal and nothing uses it (searched "metrics" in src/). Per STD-DESIGN-5 the team does not add what was not requested. If it is needed, open a new intake.`
- Needs clarification: `Is "this part looks odd" about the column order or the number format? The team is waiting for the answer before fixing the other comments, since they may be related.`
- Pushed back wrongly: `I was wrong above: the empty-name case does happen (the new test is red). Fixed in d4e5f6a.`

## Do not use
- "You're absolutely right!", "Thanks for the great feedback" — they carry no information.
- Marking threads resolved in bulk without replying.
- Promising a fix without a task.
