# Sources, citation, confidence

## Source ranking
| Rank | Source | Used for |
|---|---|---|
| 1 | Official docs for the exact version (reference, guide) | every claim about an API, configuration, limit |
| 2 | Changelog, release notes, migration guide, the project's official blog | changes between versions, deprecations |
| 3 | Standards (RFC, W3C, MDN) | protocols, formats, browsers |
| 4 | Compatibility tables, the official issue tracker (confirmed bug status) | known bugs, supported platforms |
| — | Personal blogs, community Q&A, AI summaries, memory | only to find direction; never the source of a claim |

## How to cite
- The full URL to the page/section (anchor), with `(accessed YYYY-MM-DD)`.
- A claim that is hard to find or contentious: quote one short sentence verbatim.
- A claim with no source found: write `UNVERIFIED` right after the sentence; list them at the end of the answer section.
- Two conflicting sources: record both, say which one applies to the version in use and why.

## Confidence
| Level | When |
|---|---|
| high | a rank 1–2 source for the exact version answers directly; the POC (if any) confirms it |
| medium | a rank 1–2 source but for a different minor version, or inferred from two sources |
| low | only rank 3–4, has `UNVERIFIED`, or the version could not be determined |

## `--upgrade` table template
| Breaking change | Source | Affected files (Explore) | Migration step | Risk |
|---|---|---|---|---|
| `connect()` drops the `timeout` parameter | <URL#breaking> | src/db/pool.py:12, src/jobs/sync.py:40 | use `options.timeout` | low |

Each row is the size of one 2–5 minute task; a row that is too big → split it.

## `--integration` table template
| Item | Value | Source |
|---|---|---|
| Authentication | OAuth2 client credentials, 1-hour token | <URL> |
| Rate limit | 100 requests/minute/key; exceeded → 429 + `Retry-After` | <URL> |
| Idempotency | `Idempotency-Key` header, kept 24 hours | <URL> |
| Sandbox | yes, data reset daily | <URL> |
| Errors | JSON `{code, message}`; 5xx should be retried with backoff | <URL> |
| Pagination | cursor | <URL> |
| Recommended timeout | 10 seconds | <URL> or `UNVERIFIED` |
