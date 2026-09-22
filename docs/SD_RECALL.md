# System design — quick recall

Use this file to revisit concepts you have already studied without producing another design,
diagram, or exercise. Each card provides the decision framework, its rationale, and its limits.
Open a full lesson only if the short reminder is insufficient.

Cards represent authored material. To choose completed topics, use each day's latest `sd`
event in [track progress](TRACK_PROGRESS.csv). Missing entries do not mean completed. Day 001
is the first available card; future taught days will extend this file in day order.

## Index

| Day | Topic | Jump |
| --- | --- | --- |
| 001 | Functional scope and observable outcomes | [Recall card](#day-001-functional-scope) |
| 002 | Quality requirements | [Recall card](#day-002-quality-requirements) |
| 003 | Traffic estimates | [Recall card](#day-003-traffic-estimates) |
| 004 | Storage estimates | [Recall card](#day-004-storage-estimates) |
| 005 | Latency budgets | [Recall card](#day-005-latency-budgets) |
| 006 | Single-node baseline | [Recall card](#day-006-single-node-baseline) |
| 007 | Week 1 design review | [Recall card](#day-007-week-1-design-review) |
| 008 | Request journey | [Recall card](#day-008-request-journey) |

## Day 001: Functional scope

**Core idea:** agree on what the user can accomplish before choosing how to build it.

**Reusable shape:** given a condition, an actor supplies an input; the service produces an
observable result. A named failure has a defined alternative outcome.

| Term | Keep this distinction |
| --- | --- |
| Functional requirement | The action and observable outcome |
| Quality requirement | A property of that behavior, such as delay or availability |
| Implementation choice | How the behavior is built; “use a database” is not a user action |
| Assumption | A premise still needing confirmation |
| Exclusion | Behavior this version does not promise |
| Success criterion | A defined scenario/population, measurement, and target |

**Memory anchor:** “Item created” is insufficient if the user cannot retrieve the item.
Returning an identifier repairs the response shape, but testing the full promise requires
retrieving the saved item too. One passing fixture does not prove the whole service works.

**Link-shortener boundary:** browser → shortener → redirect → browser → destination.
A correct redirect does not guarantee that the destination is healthy. Define which outcome
your success measure covers and what happens for a code that cannot be resolved.

**Why it helps:** two readers can agree on an acceptance scenario before committing to
infrastructure. A scope memo retains user decisions and postpones choices that lack a requirement.
The cost is clarification now; the benefit is fewer incompatible expectations later.

**Common mistakes:** start with architecture; use untestable words such as “fast”; omit
exclusions; present assumed traffic as measured traffic; count destination failures against an
undefined shortener guarantee. Compare one alternative and state what evidence would change the decision.

[Full explanation](../days/day-001-count-target-values/sd_functional-scope/CONCEPTS.md) ·
[Complete reference](../days/day-001-count-target-values/sd_functional-scope/REFERENCE_DESIGN.md) ·
[Your Day 1 memo](../days/day-001-count-target-values/sd_functional-scope/DESIGN.md)

---

## Day 002: Quality requirements

**Idea and cue:** replace words such as fast and reliable with a population, measurement
boundary, window, and threshold. The measured indicator is an SLI; its target is an SLO.

**Mechanism:** distinguish availability (successful eligible requests), latency (duration),
durability (retention of acknowledged data), and freshness (visibility delay after change).
Name timeouts and exclusions. Targets are assumptions until observations establish results.

**Why it works:** two reviewers can apply the same event definitions and agree on a result.
A fast stale answer can pass latency but fail freshness; temporary unavailability need not
mean permanent data loss.

**Memory anchor:** nine 10 ms requests and one 910 ms request average 100 ms, while nearest-rank
p95 is 910 ms. An average can hide a user-visible tail.

**Tradeoff and trap:** finer measurements cost collection and storage effort. Stricter freshness
can reduce cache usefulness. Do not average local percentiles into a supposed global percentile
or mistake gateway timing for the whole client experience.

[Full lesson](../days/day-002-find-the-first-maximum/sd_quality-requirements/CONCEPTS.md) ·
[Complete reference](../days/day-002-find-the-first-maximum/sd_quality-requirements/REFERENCE_DESIGN.md) ·
[Your memo](../days/day-002-find-the-first-maximum/sd_quality-requirements/DESIGN.md)

## Day 003: Traffic estimates

**Idea and cue:** turn a proposed user workload into request rates before discussing capacity.
Daily active users × actions/user × requests/action gives daily requests. Divide by 86,400
seconds for the average of a modeled 24-hour day; derive peaks from a separate concentration scenario.

**Why it works:** units cancel visibly, and the model exposes which assumption drives each
number. Retain population, frequency, boundary, interval, and peak assumptions rather than one
unexplained rate. Changing any input gives a sensitivity case.

**Memory anchor:** 1,440,000 daily reads average about 16.67 QPS; putting 25% into one hour
gives 100 QPS for that hour. These are illustrative assumptions, not measured traffic.

**Tradeoff and trap:** an average hides bursts, users are not simultaneous requests, and an
hourly rate is not QPS. API rate and database rate differ with caching, fan-out, and retries.
Equal QPS can consume different resources. Use measurements of the request mix and resource
cost before deriving server count; the estimate is a starting model, not a benchmark.

[Full lesson](../days/day-003-stable-compaction/sd_traffic-estimates/CONCEPTS.md) ·
[Complete reference](../days/day-003-stable-compaction/sd_traffic-estimates/REFERENCE_DESIGN.md) ·
[Your memo](../days/day-003-stable-compaction/sd_traffic-estimates/DESIGN.md)

## Day 004: Storage estimates

**Idea and cue:** estimate retained records before provisioning disk. Raw bytes = new records
per day × retained days × bytes per record. Then add named overheads and count total copies.

**Mechanism and reason:** if every live copy contains both data and indexes, occupied bytes
are `(raw + indexes) × total copies`. Required capacity at utilization u is occupied/u.
Each term names a layer so you can detect omissions and double counting.

**Memory anchor:** assumed 2.88 GB raw + 0.72 GB indexes gives 3.60 GB per copy; three copies
occupy 10.80 GB; 75% maximum use requires 14.40 GB capacity.

**Tradeoff and trap:** replication factor three means three total copies. Decimal GB and binary
GiB differ. Reads do not automatically create records. Backups, logs, temporary rewrites, and
delayed deletion need explicit allowances; generic headroom does not prove they fit. Shorter
retention saves storage at a product cost. Replicas can repeat an accidental deletion, so
replication and independently retained recovery copies serve different needs.

[Full lesson](../days/day-004-reverse-a-segment/sd_storage-estimates/CONCEPTS.md) ·
[Complete reference](../days/day-004-reverse-a-segment/sd_storage-estimates/REFERENCE_DESIGN.md) ·
[Your memo](../days/day-004-reverse-a-segment/sd_storage-estimates/DESIGN.md)

---

## Day 005: Latency budgets

**Idea and cue:** when a whole interaction has a latency target, allocate time along its
actual dependency path. Name the measurement boundary, request population, and component
boundaries before choosing numbers. An allocation is a planning assumption, not a measurement.

**Mechanism and reason:** nonoverlapping serial durations add for one request. Parallel work
requires tracing the path that determines completion. Measure complete-request durations to
verify the end-to-end percentile. Component p95 values may describe different slow requests,
so their sum is not generally end-to-end p95.

**Memory anchor:** across 20 synthetic requests, one stage is 100 ms once and 10 ms otherwise;
another is slow on a different request. Each nearest-rank p95 is 10 ms, but the paired totals
have p95 110 ms. Adding the two 10 ms percentiles misses the tail.

**Tradeoff and trap:** reserve margin and account for queueing, network travel, and client work.
Do not add a storage span to an inclusive app span that already contains it. Finer tracing
costs collection and analysis effort. Caching may improve latency at a freshness cost. Parallel
calls, retries, and per-stage timeouts can change the critical path; a passing toy fixture
does not validate a production target.

[Full lesson](../days/day-005-merge-sorted-arrays/sd_latency-budgets/CONCEPTS.md) ·
[Complete reference](../days/day-005-merge-sorted-arrays/sd_latency-budgets/REFERENCE_DESIGN.md) ·
[Your memo](../days/day-005-merge-sorted-arrays/sd_latency-budgets/DESIGN.md)

---

## Day 006: Single-node baseline

**Cue and mechanism:** start with a traceable browser → service → database path. Identify
the authoritative mapping, commit before acknowledging creation, and resolve codes through
that same truth. The browser follows the redirect to the destination.

**Why it works:** each operation has an explicit state owner and success boundary. Logical
boxes may share one host and therefore one outage. Measure a bottleneck hypothesis against
queue time, database latency, resource utilization, and end-to-end latency before adding capacity.

**Memory anchor:** 4 ms per operation gives an ideal serialized ceiling of 250 operations/s.
At 200 requests/s, two calls per request demand 400 operations/s. Adding app workers cannot
raise that modeled database ceiling. Real costs require measurement. A backup supports recovery,
not live availability; a lost create response can leave a committed effect and an uncertain client.

[Full lesson](../days/day-006-best-single-trade/sd_single-node-baseline/CONCEPTS.md) ·
[Complete reference](../days/day-006-best-single-trade/sd_single-node-baseline/REFERENCE_DESIGN.md) ·
[Your memo](../days/day-006-best-single-trade/sd_single-node-baseline/DESIGN.md)

## Day 007: Week 1 design review

**Cue and mechanism:** revise the weakest assumption or boundary in an earlier memo. Connect
requirement → assumption → artifact → decision → failure, then defend one alternative.
Changing one input exposes sensitivity without replacing the whole architecture.

**Why it works:** explicit units, state ownership, and acknowledgment boundaries make a
decision falsifiable. Extra capacity costs money and operations; changing retention or readiness
changes the product promise. Label estimates separately from observations.

**Memory anchor:** 18.25 GB of raw annual mappings becomes 36.5 GB under an assumed 2× overhead,
so a 20 GB allocation fails that model. In the reference, moving acknowledgment after commit
repairs the promise that acknowledged mappings survive a service-process restart. Lost responses
still leave uncertain outcomes. Read the reference after a cold attempt; this card is not a gate.

[Repair lesson](../days/day-007-week-1-review/sd_week-1-design-review/CONCEPTS.md) ·
[Complete reference](../days/day-007-week-1-review/sd_week-1-design-review/REFERENCE_DESIGN.md) ·
[Your memo](../days/day-007-week-1-review/sd_week-1-design-review/DESIGN.md)

## Day 008: Request journey

**Cue and mechanism:** expand a browser arrow into DNS, connection establishment, TLS, HTTP
request, and response. For a redirect, the browser then contacts the destination, resolving
and connecting as needed. The lesson assumes a cold TCP/TLS 1.3 path without early data.

**Why it works:** prerequisites locate failure boundaries. DNS identifies a host endpoint,
not a short-code mapping. TLS failure can prevent any application request. A correct redirect
does not prove the destination loaded. Server processing measures only part of browser delay.

**Memory anchor:** assumed 20 ms DNS + 40 TCP + 40 TLS + 40 transit + 10 app totals 150 ms
to a redirect, versus 50 ms on a usable warm connection in that model. These are synthetic
durations, not percentiles or benchmarks. Reuse saves setup but retains connection resources;
another origin may need another connection. HTTP/3 requires a different transport trace.

[Full lesson](../days/day-008-first-repeated-value/sd_request-journey/CONCEPTS.md) ·
[Complete reference](../days/day-008-first-repeated-value/sd_request-journey/REFERENCE_DESIGN.md) ·
[Your memo](../days/day-008-first-repeated-value/sd_request-journey/DESIGN.md)

---

[DSA recall](DSA_RECALL.md) · [Python recall](LANG_RECALL.md) · [Study workflow](STUDY_WORKFLOW.md)
