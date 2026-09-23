# Reference design — Invalidation race

This is an author-written answer to [the assignment](README.md#assignment), not learner
evidence. Read [CONCEPTS.md](CONCEPTS.md) first. Use this within the existing 30-minute
SD budget for guided reading or comparison after an independent attempt.
[DESIGN.md](DESIGN.md) remains your practice file; its TODOs belong to you.

## Assumptions and requirement

We cache editable public link destinations. The primary database is authoritative; a source
lookup sees committed data at its read point. Assume this display/redirect route tolerates
at most 5.2 seconds of old destination visibility after commit. Security revocation uses a
separate authoritative path. These are design assumptions, not measurements.

Choose cache TTL T=5 seconds from fill and loader deadline D=0.2 seconds from starting the
source read through publication. Reject a loader result that cannot publish within D. Cache
hits never extend expiry. All readers enforce expiry; no downstream cache extends this bound.
The bound also assumes no lagging replica and no stale local fallback layer.

## Interleaving and calculation

| Step | Reader R | Writer W | Source/cache |
| --- | --- | --- | --- |
| 1 | cache miss, snapshots v4 | | DB v4; cache absent |
| 2 | waits before publishing | commits v5 | DB v5; cache absent |
| 3 | still waiting | deletes cache key | DB v5; cache absent |
| 4 | publishes saved v4 | write already acknowledged | DB v5; cache v4 |
| 5 | another request reads v4 | | stale answer |

Invalidation did execute successfully. Its weakness is that it cannot retract a snapshot
already held by R. If R began before the commit, its permitted remaining publication delay
after commit is at most D. Its fill can live for another T. Thus the conditional worst-case
window is D+T=0.2 s+5 s=5.2 s. If R exceeds D, discard its result and do not fill or return
that old snapshot. A new read may retry within its request budget or return a controlled error.

## Decision and alternative

Adopt bounded staleness with commit-then-delete and fixed TTL. Invalidation reduces typical
stale exposure; expiry and capped fills provide the stated fallback bound even if deletion
fails. Reads after successful expiry consult the source. Cache outages bypass only under
an origin concurrency limit, so loss of the cache cannot create unlimited database work.

For a stronger alternative, retain a per-key minimum version and atomically reject older
publications. The writer raises the barrier when publishing its committed version. A stale
reader holding v4 cannot fill over a v5 barrier. Keep the barrier independently of value
eviction, with retention longer than all permitted in-flight reads. A restart must rebuild
or conservatively gate fills until the barrier is trustworthy. Acknowledging the database
commit before the barrier update still leaves a gap; versions alone do not create a
transaction across the database and cache. I would use authoritative reads for a strict
read-after-write requirement until that coordination protocol is fully specified and tested.

## Failure walkthrough

R reads v4 just before W commits v5. R resumes 150 ms after commit and fills v4. That entry
can remain eligible for five seconds from fill, so readers may see v4 until 5.15 seconds
after commit, within the assumed 5.2-second allowance. An R resuming after its 200 ms deadline
must be rejected. If the implementation merely times out the client but lets the background
loader publish later, the bound is lost. Recovery therefore includes suppressing late results,
not just returning a timeout. The source record is never overwritten by a cache fill.

## Self-review

The unresolved implementation detail is enforcing deadline validation together with publication
so a paused publisher cannot validate early and publish arbitrarily late. That needs an atomic
or server-enforced operation, or an expiry mechanism tied to the original read deadline.
Until verified, 5.2 seconds is a design requirement, not a demonstrated production guarantee.
I would pause a loader after its read, commit a write, force invalidation failure, resume the
loader before and after its deadline, and inspect every response age. Track stale-version hits,
late-fill rejections, and invalidation lag. The concept's Python schedule reproduces logical
ordering only; it does not run these distributed tests.

## Reading and practice

This is one defensible answer under the stated assumptions. Reading it does not complete
SD-37. Record your own decision, help used, and evidence in [DESIGN.md](DESIGN.md).
The [concept lesson](CONCEPTS.md#the-source-behind-it) links the verified primary sources.
