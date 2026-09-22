# Reference design — Cursor pagination for links

This is the author's answer to the [actual assignment](README.md#assignment). Use it before
guided practice or after an independent attempt. [DESIGN.md](DESIGN.md) remains your work.
All rows and timings below are hypothetical; the executed ordering model is in [CONCEPTS.md](CONCEPTS.md).

## Assumptions and required behavior

An authenticated owner lists only their links, newest first. Creation time is server-assigned
UTC and immutable; link_id is unique, immutable, and totally ordered. Timestamps may tie.
This is a live listing: a refresh sees newer rows, while continuation does not promise a
snapshot. Page size defaults to 20 rows and is bounded to 1–100 rows as a chosen resource cap.
The small example uses 2 rows per page. These are policy choices, not measured optimal values.

## Contract and requested artifact

`GET /v1/links?limit=2` returns `items` and `next_cursor`. Each item contains link_id,
created_at, destination_url, and expires_at. A missing continuation is JSON null. The cursor
encodes a version, the last returned (created_at, link_id), the owner/filter scope, and an
expiry. Choose a signed opaque token valid for 15 minutes to bound stale format support;
this is a chosen traversal limit. Reject malformed, expired, or mismatched tokens with a
400 response and a stable error code. Recheck authentication and owner scope on every page.
Allow limit to vary within bounds because it does not change the ordering or filters.

Use the following query shape after validating a cursor:

```sql
SELECT link_id, created_at, destination_url, expires_at
FROM links
WHERE owner_id = :authenticated_owner
  AND (created_at, link_id) < (:last_created_at, :last_link_id)
ORDER BY created_at DESC, link_id DESC
LIMIT :limit_plus_one;
```

**Line by line:** This is a parameterized design sketch, not executed SQL; colon parameters
stand for driver-bound values. Owner scope comes from authentication. Tuple comparison handles
the time tie using ID and excludes the last returned row. ORDER BY must match that comparison.
Fetch one extra row to detect continuation, but set the token to the last row actually returned.
The first-page query omits the boundary predicate. A proposed index is
`(owner_id, created_at DESC, link_id DESC)`; confirm its plan with representative data later.

| Step | Newest-first rows or result |
| --- | --- |
| Initial keys | (12:00,9), (12:00,8), (11:59,7), (11:58,6) |
| First page | IDs 9,8; cursor=(12:00,8) |
| Concurrent insertion | New ID 10 at 12:01 sorts before both returned rows |
| Second page | Keys strictly below (12:00,8): IDs 7,6 |
| Offset alternative | Skipping two rows now repeats ID 8 |

Times share one hypothetical UTC date. ID 8 at the same time as ID 9 is why time alone is
insufficient. Cursor `(12:00)` with strict time comparison would skip remaining tied rows.

## Decision and defended alternative

Choose keyset continuation: unchanged rows already returned cannot satisfy the strict lower
bound. The cursor remains useful even if its referenced row is deleted because the key is in
the token. Offset pagination is simpler for small static lists and supports numbered page
jumps; accept it if that is the actual requirement. A snapshot export is a separate alternative
when all pages must reflect one instant, with database/storage lifetime costs this listing avoids.

## Failure walkthrough and response

A client changes the owner field in its token. Signature validation rejects the tampering;
even a valid token from a different account fails scope matching. Authorization always remains
in the query. A link's ordering key changing between pages could move it across the boundary
and produce a repeat or omission, so creation time and ID cannot be edited. Destination edits
may appear between pages under this live contract. Backdated inserts below the boundary can
appear later; new rows above it wait for refresh. None of these behaviors establishes a snapshot.

## Cost and self-review

The extra fetched row adds at most one row of query output per page. At the maximum limit,
fetch 101 rows and return at most 100. Seek-style execution may approach O(log N + page_size)
with the proposed index; this is a plan expectation, not a benchmark. Verify equal timestamps,
an insertion, deletion of the boundary row, the final partial page, and invalid tokens in an
implementation. The artifact meets the ordered-cursor and concurrent-insertion requirements.
Remaining limits: no arbitrary page number, no snapshot, and no measured index performance.

Source: [PostgreSQL 18 — LIMIT and OFFSET](https://www.postgresql.org/docs/18/queries-limit.html),
checked 2026-09-22. Cursor policy and examples are authored design decisions.
