# Reference design — Negative caching

This is an author-written answer to [the assignment](README.md#assignment), not learner
evidence. Read [CONCEPTS.md](CONCEPTS.md) first. Use this within the existing 30-minute
SD budget for guided reading or comparison after an independent attempt.
[DESIGN.md](DESIGN.md) remains your practice file; its TODOs belong to you.

## Assumptions and requirement

Assume a tenant-scoped link lookup where a confirmed missing code is frequently retried.
The source database is authoritative. A newly created code may remain invisible for at most
2.1 seconds under a fallback policy; the creator's immediate confirmation reads the source
directly. A negative fill must finish within 100 ms, and its TTL is 2 seconds without extension
on hits. All numbers are proposed choices. Infrastructure errors are not evidence of absence.

## Cache representation and lifecycle

Use a key containing tenant ID, canonical code, and any visibility scope affecting the answer.
Authenticate before protected lookup. If permission-dependent absence cannot be shared safely,
do not put it in this cache. Store a tagged NOT_FOUND marker with an expiry, distinct from
FOUND(payload) and from no cache entry. The cache never stores a timeout as NOT_FOUND.

| Source result | Cache action | Caller outcome |
| --- | --- | --- |
| object exists | store positive under its own policy | return authorized object |
| authoritative absence | store NOT_FOUND for 2 s | return the API's missing-object response |
| timeout or connection error | no negative fill | bounded retry or temporary failure |
| create commits | delete negative entry after commit | next miss reads source |

Let negative loader deadline D=0.1 s and TTL T=2 s. If an absence snapshot predates creation
but fills afterward, its latest permitted fill is D after commit and its lifetime adds T.
The fallback visibility lag is therefore at most D+T=2.1 s, conditional on atomic deadline
enforcement, authoritative reads, and no longer-lived downstream negative cache. For a stronger
read-after-create promise, bypass or use a coordinated version barrier as in Day 37.

## Decision and capacity calculation

Choose short negative caching plus creation invalidation and same-key coalescing within each
process. For one coordinator, one missing key at 2,000 requests/s produces about 4,000 requests
per two-second TTL window but roughly one reload per window in steady state. With multiple
independent coordinators, account for duplicate boundary loads rather than claiming exactly one.
Requests arriving after expiry may briefly wait for the next authoritative result.

Bound negative cache memory to 10,000 entries. With an assumed 128 bytes per marker including
key and overhead, this is 1,280,000 bytes, about 1.22 MiB. Measure real overhead and enforce a
byte limit too. Random unique-code traffic bypasses the benefit and can churn entries; rate
limit queries and consider admission only after repeated misses. Never let missing-key noise
evict all useful positive entries without a deliberate shared-budget decision.

The simplest alternative is no negative caching: every lookup remains immediately consistent
with its authoritative read but costs source capacity. I would choose that for rare misses
or when even a 2.1-second false negative is unacceptable. A longer TTL saves more work while
extending creation visibility lag, so it needs a different requirement.

## Failure walkthrough

R reads absence for K and pauses. W creates K, commits, and deletes the negative entry. R
resumes within 100 ms and installs an old NOT_FOUND marker. Other callers may receive missing
responses until expiry; the creator's direct confirmation succeeds. If the loader resumes
after its deadline, discard it. Independently, a source timeout must return a temporary
failure; caching it as absence would hide existing objects throughout an outage and afterward.
Recovery clears any incorrectly classified entries and fixes error classification at the loader.

## Self-review

Test the creation race, tenants sharing the same code string, real empty payloads, expiry
boundary equality, timeouts, and high-cardinality invalid traffic. Measure false-negative
reports, source reads avoided, negative-entry bytes, and loader delays. Confirm intermediary
HTTP caching cannot prolong the error beyond the internal bound. The Python model establishes
tag separation only; no deployed cache, authorization boundary, or rate limit was tested.

## Reading and practice

This is one defensible answer under the stated assumptions. Reading it does not complete
SD-40. Record your own decision, help used, and evidence in [DESIGN.md](DESIGN.md).
The [concept lesson](CONCEPTS.md#the-source-behind-it) links the verified primary sources.
