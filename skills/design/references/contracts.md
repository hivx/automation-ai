# Contracts, idempotency, migration, test plan

## The contract of an entry point
| Part | What to record |
|---|---|
| Input | fields, types, required/optional, limits; where it is validated (boundary) |
| Output | fields, types, ordering (if meaningful), default values |
| Errors | code + condition + message, in the project's shared error style |
| Version | unchanged / additive (compatible) / new (breaking) + migration guide |

Observable behavior (error codes, message text, result ordering, defaults) is contract even if nobody wrote it down — someone will depend on it. Changing it = changing the contract.

Order of preference when a change is needed: add an optional field → add a new entry point → a new version. Never change the meaning of an existing field.

## Idempotency (outbound calls, or inbound calls that get retried)
1. The key is derived from business intent (for example order ID + action), not generated anew for each attempt.
2. Claim atomically: a unique constraint on the key; never "read to see if it exists, then insert".
3. Same key, different payload → an explicit error (never silently return the old result).
4. An in-flight duplicate: pick one — reject, wait, or return "processing".
5. Keep the key longer than the caller's longest retry path.
6. Three-state outcome: success / failure / unknown (timeout) — "unknown" must have a way to reconcile.

## Batched migration
| Item | What to record |
|---|---|
| Expected numbers | row count before, row count after, how they are counted |
| Up | the steps; large table → batches of N rows, with a safe stopping point |
| Down | the reverse steps; data lost on the way down must be stated and needs a human approval |
| Reconciliation | a query comparing counts/totals after each direction |
| Cutover | the deploy order of code and migration (expand → migrate → contract when changing a schema in use) |
| Rollback | trigger conditions, success criteria |

## Test-plan row template
| Criterion | Test | Kind | Error/boundary path |
|---|---|---|---|
| AC-1 exports CSV with a header | tests/test_export.py::test_header_row | unit | — |
| AC-2 empty inventory | tests/test_export.py::test_empty_inventory | unit | boundary: 0 rows |
| AC-3 name containing a comma | tests/test_export.py::test_quote_comma | unit | error: special character |
| NFR-1 10,000 rows < 2 s | tests/perf/test_export_perf.py::test_10k | integration | boundary |

The Test column is `file::name` per `naming.test_file`; the command that runs it is `cmd.test_one` with `{file}`, never a typed stack command.
