# Reference design — Revise the pagination decision

Read this only **after your cold review attempt**. The [assignment](README.md#assignment)
asks for your weakest decision from Days 8–13. The author cannot infer that weakness, so this
complete worked review selects pagination as an explicit example. Your [DESIGN.md](DESIGN.md)
can legitimately revise another prior decision.

## Selected decision and assumptions

Hypothetical old memo: list an owner's links newest-first using page numbers, two rows per
page, and OFFSET. Product requirement: ordinary sequential navigation must not repeat an
unchanged link merely because another link was created. Creation time and ID are immutable,
ID is unique, and pages are live rather than a consistent export. The old memo did not connect
its pagination choice to the concurrent-insertion requirement. This is an authored example,
not a claim about a learner's previous work or a production incident.

## Failure that motivates the revision

| Request/event | Visible descending keys | Result |
| --- | --- | --- |
| Page 1 | (12:00,8), (12:00,7), (11:59,6), (11:58,5) | Return 8,7 |
| Another create | Prepend (12:01,9) | Positions shift |
| Page 2 with OFFSET 2 | 9,8,7,6,5 | Return 7,6; ID 7 repeats |

All times use a common hypothetical UTC date. A page contains 2 rows, so the old second page
skips exactly 2 current rows, not 2 rows from the previous view. That is the violated assumption.

## Revised artifact

```text
Authenticated owner -> GET /links?limit=2
Service -> query owner scope, ORDER BY created_at DESC, link_id DESC, fetch 3
Service -> return first 2 rows + signed cursor(last returned time, ID, scope, version)
Client -> GET /links?limit=2&cursor=...
Service -> validate token and owner; query keys strictly below saved pair; fetch 3
Service -> return first 2 rows + next cursor, or null if no lookahead row
```

The 3-row fetch equals requested size 2 plus one lookahead. The last returned key (12:00,7)
is the continuation; the lookahead key is not. The revised second page returns IDs 6,5 even
after insertion. Tie-breaking by ID avoids losing a same-time row. The query always derives
owner scope from authentication and checks token scope against it. Use the bounded sizes,
cursor expiry, and index proposal in [Day 13's reference](../../day-013-count-target-subarrays/sd_pagination/REFERENCE_DESIGN.md).

## Decision, alternative, and tradeoff

Keep cursor continuation because it meets sequential no-repeat behavior for unchanged keys.
Defend OFFSET when a small mostly static administrative list needs direct jumps to numbered
pages and accepts movement between requests. If the requirement is instead a reproducible
export, select a snapshot-based design; a stable boundary alone cannot guarantee all rows
as of one instant. Snapshot lifetime and retained data then become explicit costs.

## Revised failure walkthrough

Delete the boundary row after page one. Continuation still works because its saved pair is
a value, not a database lookup of that row. Change a destination: later pages may show the new
value under live semantics. Change creation time: the correctness argument fails, so forbid
that edit. Tampered cursor: reject before querying; valid token from another owner: reject
scope mismatch, with owner filtering still enforced. Token expiry requires a fresh traversal;
the client must not merge the restarted list as though it were the old continuation.

## Self-review and evidence

The revision includes the old decision, a violated requirement, a new request flow, a defended
alternative, and residual failure modes. The [concept lesson](CONCEPTS.md#when-it-breaks)
contains an executed in-memory insertion test. The timeline above is hypothetical; SQL query
plans, signing, concurrent clients, and server behavior have not been executed. Proposed
implementation checks include ties, insertions, deletion, owner isolation, and cursor expiry.
This is one defensible review within the existing 30-minute session, not a second mandatory
design. A learner should critique their own selected artifact and record help separately.

Source: [PostgreSQL 18 — LIMIT and OFFSET](https://www.postgresql.org/docs/18/queries-limit.html),
checked 2026-09-22; [Day 13 explanation](../../day-013-count-target-subarrays/sd_pagination/CONCEPTS.md).
