# Reference design — Stampede control

This is an author-written answer to [the assignment](README.md#assignment), not learner
evidence. Read [CONCEPTS.md](CONCEPTS.md) first. Use this within the existing 30-minute
SD budget for guided reading or comparison after an independent attempt.
[DESIGN.md](DESIGN.md) remains your practice file; its TODOs belong to you.

## Assumptions and requirement

Consider one public, non-security-sensitive link at 1,000 requests/s. Assume origin lookup
takes 100 ms, there are eight application processes, and a response may use a source snapshot
up to 15 seconds old. Origin reads are authoritative. Values must not be served past domain
expiry. These are assumed requirements and workload figures, not observed performance.

## Comparison and chosen request path

| Technique | Applied here | Limitation |
| --- | --- | --- |
| Per-process single-flight | one in-progress load per key per process | up to eight loads across eight processes |
| TTL jitter | fresh period sampled from 8..10 seconds | spreads different keys, not this single key's concurrent requests |
| Stale-while-revalidate | serve until snapshot age reaches 15 seconds while one refresh runs | requires product tolerance; no use after hard expiry |

Choose all three for complementary reasons. Store read_started_at with the payload and
conservatively compute age from that timestamp; publication delay consumes age budget rather
than resetting it. A trusted consistent clock basis and expiry checks across all processes
are requirements; allow a safety margin for clock uncertainty in implementation. A fresh
deadline is 8..10 seconds after read start and stale_until is 15 seconds after read start.
Discard results arriving after their applicable deadline; never refresh the age by cache hits.

The request checks existence, domain validity, and age. Fresh values return immediately.
Eligible stale values return immediately and trigger one coalesced refresh. An absent or
too-old value joins the pending load with a 200 ms request wait cap. The loader itself has
a 150 ms deadline. Successful refresh publishes only an acceptable current result; failed
refresh wakes waiters, clears the pending registry, and applies bounded retry backoff.
After hard expiry, a failed load returns a controlled error, not another stale response.

## Load calculation and decision

Without sharing, 1,000 requests/s * 0.1 s = approximately 100 requests arrive during a load
and may each start origin work. Local coalescing reduces this to at most one overlapping
load per key per process in normal operation, hence up to eight across the fleet. This is
not a global once-only guarantee. Assume that eight concurrent lookups fit the origin budget;
cap aggregate origin concurrency separately to account for many distinct missing keys.

For the current assumption, per-process coordination is the simpler decision. A global lease
is an alternative when eight duplicate loads are too expensive. It needs acquisition timeouts,
bounded lease lifetime, owner tokens, safe release, and protection from late former owners
overwriting newer results. Recheck the cache after acquiring the lease. Coordination cost
must be justified against the actual origin load saved.

## Failure walkthrough

At snapshot age 11 seconds, the value is stale but allowed. One process starts refresh and
its followers share work while stale responses continue. The origin stalls; at 150 ms the
loader fails, releases its registry slot, and schedules bounded backoff. At age 15 seconds,
the old value becomes ineligible even if the origin is still down. Requests can wait at most
their remaining 200 ms cap, then receive an error. A waiter that disconnects does not cancel
the shared loader for everyone. No error path may retain an unresolved pending result forever.

## Self-review

Test simultaneous misses across all eight processes, loader exceptions, cancellation, late
completion, stale-boundary equality, and restart. Record origin load count, followers per
leader, waiter latency, rejected late fills, and maximum age served. The Python demonstration
models a fixed arrival schedule but does not test synchronization or clocks. The remaining
risks are shared-cache publication races and clock uncertainty; reuse the Day 37 version/age
analysis instead of assuming coalescing provides consistency.

## Reading and practice

This is one defensible answer under the stated assumptions. Reading it does not complete
SD-39. Record your own decision, help used, and evidence in [DESIGN.md](DESIGN.md).
The [concept lesson](CONCEPTS.md#the-source-behind-it) links the verified primary sources.
