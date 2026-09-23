# Reference design — TTL and eviction

This is an author-written answer to [the assignment](README.md#assignment), not learner
evidence. Read [CONCEPTS.md](CONCEPTS.md) first. Use this within the existing 30-minute
SD budget for guided reading or comparison after an independent attempt.
[DESIGN.md](DESIGN.md) remains your practice file; its TODOs belong to you.

## Assumptions and requirement

Assume public link metadata tolerates a cache residence TTL of at most 60 seconds; source-read
delay must be budgeted separately as in Day 37. The cache is disposable, and the origin can
admit 500 reloads/s for this workload. A warmup fills 20,000 popular keys at once. All figures
are hypothetical planning inputs. Domain-expired or revoked links require their own checks.

## Expiration and capacity artifact

| Concern | Policy | Reason |
| --- | --- | --- |
| Freshness | fixed per-fill TTL uniformly chosen from 45 to 60 s | never exceeds the residence limit; spreads expiry |
| Hits | do not reset TTL | popularity must not keep an old value alive indefinitely |
| Memory | reserve 128 MiB total; plan 96 MiB for entries | leave 32 MiB headroom for overhead not covered by the entry estimate |
| Victims | all-key LRU as an initial policy | remove cold entries even if still fresh |
| Expired reads | check deadline before serving | logical expiry must not wait for physical cleanup |

Assume measured later, but currently estimated, entry footprint is 1 KiB including key and
per-entry overhead. The 96 MiB entry budget fits about 98,304 entries because
96 * 1,048,576 bytes / 1,024 bytes = 98,304. This is a sizing estimate, not a guaranteed
Redis process limit. Allocator overhead and buffers require measurement before deployment.
The toy two-entry example in CONCEPTS separates eviction of a fresh B from expiry of a popular A.

## Simultaneous-expiration calculation

With fixed 60-second TTL after the warmup, all 20,000 keys expire together. If all are requested
immediately and each reload occurs once, 20,000 / 500 = 40 seconds of admitted origin work
is required. Queuing that much work would violate most request deadlines; requests should
be shed or served through an explicitly permitted stale policy rather than wait indefinitely.

Jitter spreads expected first reloads over 15 seconds, but 20,000 / 15 is about 1,333 reloads/s,
still above the assumed 500/s origin budget. Randomization also provides no strict peak bound.
Therefore jitter alone is insufficient for this workload. Limit admitted origin work, avoid
synchronized full warmups, and use Day 39's coalescing and bounded stale refresh where allowed.
Same-key bursts need coalescing even when different keys expire at different times.

## Decision and alternative

Select fixed maximum freshness plus independent LRU eviction, with downward jitter and a bounded
reload budget. Cache misses remain correct regardless of which key was evicted. Compare LFU
if stable popular keys are repeatedly displaced by scans; compare a separate negative-entry
budget if missing-key traffic competes with real data. More memory may reduce capacity misses
but cannot repair freshness expiration. A longer TTL would reduce reload frequency but violates
the stated residence bound, so changing it requires changing the requirement first.

## Failure walkthrough

A deployment preloads every popular key using the same TTL and causes a reload wave one minute
later. Admission stops excess origin work; callers receive an allowed stale answer or a bounded
error according to policy. Recovery staggers warmup and refresh, retains independent eviction,
and monitors demand while returning toward normal traffic. If stale service is forbidden,
choose controlled errors over silently extending TTL. No cache entry becomes authoritative.

## Self-review

Measure actual bytes per entry and process memory, expiry-caused misses versus evictions,
origin admission rate, and request latency through warmup and total cache loss. The 500/s
assumption needs a load test, and the 45..60-second range needs production-like access traces.
Validate engine-specific eviction behavior; the concept uses exact toy LRU while real policies
can approximate recency. Neither memory estimates nor the arithmetic constitute a benchmark.

## Reading and practice

This is one defensible answer under the stated assumptions. Reading it does not complete
SD-38. Record your own decision, help used, and evidence in [DESIGN.md](DESIGN.md).
The [concept lesson](CONCEPTS.md#the-source-behind-it) links the verified primary sources.
