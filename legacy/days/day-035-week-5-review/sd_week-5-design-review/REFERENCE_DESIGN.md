# Reference design — Week 5 design review

This is the assistant's completed answer to the [assignment](README.md#assignment).
[DESIGN.md](DESIGN.md) remains your personal practice. Assumed scenarios are not production observations.

## Cold review first

Attempt your own weakest decision from Days 29–34 before opening this answer. This reference
chooses Day 33 expiration as an illustrative weak decision; it does not identify your weakness.
Use the existing 30-minute gate and record help from this comparison.

## Original decision and exposed gap

Original memo: “The cleanup worker deletes expired links, so redirects can return any stored
row.” Assume expires_at=100 seconds, cleanup at 150, and a read at 120. That read would return
expired content. The statement coupled user-visible correctness to a maintenance schedule with
no punctuality guarantee. The missing invariant was explicit eligibility at the serving boundary.

## Revised artifact

```text
request(code)
  -> authorized serving path
  -> candidate from cache or database
  -> active and now < expires_at?   (no expiry is a separate allowed state)
        yes -> redirect
        no  -> absent/expired response

cleanup -> reclaim expired storage asynchronously
delete propagation -> retain newer deletion state until stale copies are fenced/repaired
```

The database remains the source of truth; cache copies carry expires_at and version. At 99
the hypothetical active link is eligible, at 100 and 120 it is not. Cleanup delay affects
storage occupancy. Explicit revocation before expiry needs its own cache freshness or source
validation rule; this expiry predicate alone does not solve stale active flags.

## Alternative and tradeoff defense

Synchronous physical deletion at the deadline can reclaim primary storage sooner but requires
reliable scheduling, retry handling, and load control. It still does not eliminate cached or
restored copies. Read-time eligibility plus asynchronous cleanup is therefore the chosen repair
for this requirement. Strong immediate revocation could instead require authoritative checks on
each read, sacrificing some cache benefit and availability during source failure.

## Failure walkthrough

The cleanup worker stops at time 90. The row and cache copy remain present through 120.
Both serving paths reject the candidate after the deadline. On worker recovery, cleanup
reclaims eligible data without changing the already-correct user result. If a replica returns
old pre-delete data, tombstone retention and stale-replica fencing from Day 33 prevent resurrection.
Clock disagreement can still cause inconsistent boundary decisions, so a defined clock policy
and a measured skew bound are prerequisites to a strict real-world expiry promise.

## Self-review and next verification

Requirements: explicit serving deadline. Data/API: source ownership and cached expiry fields.
Scale: cleanup backlog costs storage; eligibility checks add per-read work. Failure: delayed
cleanup and stale replicas have separate handling. This covers the review's revision, alternative,
and failure walkthrough. Next test boundary reads with cleanup disabled, a retained cache entry,
and a stale replica; also measure clock skew. The Python trace is an observed abstract model,
not evidence that these integration checks passed. Score your own artifact 0–2 in each design
category and require 6/8 with the source of truth explained before recording completion.


## Sources and comparison

The primary references for repair are [partition-key design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) and [expired-item behavior](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ttl-expired-items.html).
Checked 2026-09-23. See [the concept lesson](CONCEPTS.md) for the worked mechanism and
executed teaching model, and [the source ledger](../../../docs/SOURCES.md) for provenance.
