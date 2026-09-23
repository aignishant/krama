# Reference design — Cache aside

This is the assistant's completed answer to the [assignment](README.md#assignment).
[DESIGN.md](DESIGN.md) remains your personal practice. Assumed scenarios are not production observations.

## Assumptions and source of truth

The database owns code, destination, active, expires_at, and version. The cache is disposable.
For this initial read-heavy example, destinations are immutable and early revocation is outside
the serving contract; logical expiry is enforced on every hit. If editable destinations or
immediate revocation are required, the freshness policy must be strengthened before deployment.
For an absent code choose 404; for an expired known code choose 410; a database timeout on a miss
returns a retryable 503. These are proposed API choices, not captured HTTP responses.

## Request artifact

```text
GET code -> bounded cache read
             |
             +-- valid hit -> check active/expiry -> redirect
             |
             +-- miss/error -> bounded source read
                                 |
                                 +-- timeout/failure -> 503
                                 +-- absent -> 404
                                 +-- expired -> 410
                                 +-- valid -> best-effort cache fill -> redirect
```

A cached active=false or expired payload never redirects. Treat an unusable expired candidate
as a source lookup if the response needs authoritative 404 versus 410 classification. Never
turn a cache error into a conclusive missing-code result. A cache-fill failure after a valid
database result is recorded but does not cancel the redirect.

## Four required traces

| Trace | Source interaction | User result | Evidence to record in a real test |
| --- | --- | --- | --- |
| valid hit | none | redirect | hit and deadline check |
| miss, source valid | one bounded read | redirect; fill attempted | source read and fill outcome |
| miss, source failure | failed read | 503 | timeout/error classification |
| miss, source valid, fill fails | successful read | redirect | separate fill-error metric |

For a hypothetical 100 ms internal request budget, allocate 5 ms to cache lookup, 60 ms to
source read on a miss, 5 ms to best-effort fill, and 30 ms to handler/serialization/headroom.
The sum is 100 ms. These are proposed deadlines, not observed latency percentiles. Abort or
skip optional fill when the remaining deadline cannot cover it. Never retry each component
indefinitely inside that budget. Cap aggregate source concurrency during cache failure.

## Decision, freshness, and alternative

Use cache-aside because repeated immutable reads can avoid source work without making the
cache authoritative. A direct-database baseline is simpler and preferable if measured load
does not need caching. A read-through cache relocates loading responsibility but does not
remove failure or freshness decisions. Record hit rate, source QPS, and tail latency before
claiming benefit.

Cache lifetime must not exceed remaining link lifetime; payload deadline checks remain mandatory.
If edits are introduced, update the database then invalidate. That alone is not strict coherence:
a reader fetching v1 before a writer commits v2 can fill v1 after invalidation. Limit fill age
and design version-aware coordination or authoritative validation for the required freshness.
Do not claim that a TTL measured from a late fill automatically bounds staleness from commit.

## Failure walkthrough

Cache connectivity fails across workers. Every request would fall through to storage, potentially
overloading it. Use bounded cache waits, coalescing for popular keys, source admission limits,
and retryable failure for excess work. A successful database result still serves if its fill
fails. A database timeout is never negative-cached as absence. During total source outage,
already valid immutable cache hits can serve until their deadlines; misses fail explicitly.

## Self-review

All four assigned paths have distinct outcomes and the database is the source of truth.
Remaining uncertainty is measured source capacity, cache benefit, and whether real product
requirements permit immutable destinations and no early revocation. Next inject cache-read,
source-read, and cache-write failures independently, verify status distinctions, then run a
cache-outage load test. The lesson's Python branch model passed; no deployed service was tested.


## Sources and comparison

[Cache-Aside Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside) explains loading on a miss and the consistency tradeoff. Failure responses and numeric budgets here are proposed application choices.
Checked 2026-09-23. See [the concept lesson](CONCEPTS.md) for the worked mechanism and
executed teaching model, and [the source ledger](../../../docs/SOURCES.md) for provenance.
