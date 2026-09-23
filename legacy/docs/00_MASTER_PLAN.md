---
plan: krama
version: "v1.1.0"
days: 168
tracks: 3
ids: 504
phases: 24
---

# Krama — master course plan

## 1 · Outcome and assumptions

Krama means sequence: steady practice in three independently usable tracks. The assumed goal
is strong software-engineering and product-company interview readiness, including the user's
Google goal. Focus on unfamiliar problems, clear reasoning, correctness, complexity and follow-ups.
LeetCode assignments are pattern practice, not claims about an employer's current question bank.
Python assumes five years of practical experience; DSA and design start with a diagnostic foundation.
Duration is 168 study days, or 24 weeks at seven sessions per week. At six sessions per week it
takes 28 calendar weeks. The count is an initial recommendation, not a user-specified deadline.

The deliverable is a complete daily assignment course and practice workspace. Deep eleven-section
Granth chapters are not prewritten. Official references supply further teaching; daily exercises
have explicit outcomes, and DSA includes original self-contained problem statements and examples.
504 IDs identify session outcomes, including assessments; they are not 504 unrelated concepts.

## 2 · Principles

Study tracks independently and in their own order. Write a hypothesis before code. Start with a
simple correct baseline, then explain the improvement. Record failed attempts. Leave exercises
unsolved until you do them. Every test must be capable of detecting a real mistake. Cite actual
sources, distinguish assumptions from observations, and keep algorithmic complexity separate from
runtime measurements. Completion means evidence and explanation, not merely reading a page.

## 3 · Portfolio

DSA: tested solutions, complexity arguments, counterexamples, a mistake log and cold re-solves.
System design: short decision memos, sequence/component diagrams and case studies ending in a
defensible design portfolio. Python: focused experiments and a tiny local job runner, with tests
for cleanup, concurrency and failure paths. No cloud deployment or paid platform is required.

## 4 · Daily budget and overload policy

| Track | Daily cap | Session allocation |
| --- | --- | --- |
| dsa | 60 minutes | 5 recall + 10 concept/trace + 30 core attempt + 10 tests/explanation + 5 log |
| sd | 30 minutes | 5 recall + 10 reference/concept + 12 one design deliverable + 3 critique |
| lang | 15 minutes | 3 predict + 8 experiment + 4 explain/test |

For DSA, use the LeetCode companion as the main attempt when its pattern matches. The local
exercise provides a warm-up, a free fallback, or a contract variation for review. Do not require
both implementations within the same hour. An online solve needs actual submission evidence and
a contract comparison; local tests check only the local contract. See [interview practice](INTERVIEW_PREP.md)
and the [complete LeetCode index](LEETCODE_INDEX.md).

Total: 105 minutes daily. Across 168 sessions the budget is 168 DSA hours, 84 design hours and
42 Python hours. Optional exercises replace spare time; they never add mandatory time. Hard DSA
sessions may use the whole attempt window for deriving a baseline and invariant. Mark partial,
then use review time to finish; do not label an unfinished exercise mastered. If more than two
core problems remain unresolved at a weekly gate, pause that track's new topics and use additional
calendar sessions. Other tracks can continue. The 168-day map is a sequence, not a deadline.

## 5 · Environment and sources

Local Python observed: 3.12.10; scripts use only the standard library. Tooling requires Python
3.11+; core experiments target 3.12. Newer interpreter topics require reading version notes and
are not claimed to run on 3.12. Use PowerShell from the repository root. No package installation
is needed to begin. See [sources](SOURCES.md), [pins](PINS.md) and [provenance](PROVENANCE.md).

## 6 · Tracks

<!-- granth:tracks:start -->
| Track | Prefix | Count | Thread |
| --- | --- | --- | --- |
| Data structures and algorithms | DSA | 168 | Correctness, implementation, complexity and cold practice |
| System design | SD | 168 | Requirements, scale, data, failures and tradeoffs |
| Advanced Python | PY | 168 | Semantics, maintainability, runtime behavior and production code |
<!-- granth:tracks:end -->

## 7 · Weekly phases

Each phase has six topic sessions and a seventh review. Pass each track separately. A DSA gate
requires two cold re-solves with tests and explanations; SD requires a revised design artifact
and one failure walkthrough; Python requires a bug reproduction/fix and a spoken explanation.

<!-- granth:phases:start -->
| Phase | Days | Theme | Gate |
| --- | --- | --- | --- |
| 1 | 1-7 | Cost, invariants and arrays / Requirements and estimation / Object semantics | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 2 | 8-14 | Hashing and prefix sums / Networking and HTTP / Functions and scope | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 3 | 15-21 | Two pointers and sliding windows / Service boundaries and API design / Iteration and generators | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 4 | 22-28 | Binary search and ordered answers / Relational storage and indexes / Data model protocols | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 5 | 29-35 | Sorting, intervals and selection / Storage engine tradeoffs / Classes and descriptors | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 6 | 36-42 | Linked lists and pointer invariants / Caching and content delivery / Data classes and modeling | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 7 | 43-49 | Stacks, queues and monotone structures / Load balancing and partitioning / Typing foundations for experienced developers | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 8 | 50-56 | Recursion and backtracking / Replication and consistency / Advanced typing and API contracts | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 9 | 57-63 | Binary trees and search trees / Queues and event processing / Exceptions and resource lifetime | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 10 | 64-70 | Heaps, tries and tree construction / Reliability patterns / Testing and debugging | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 11 | 71-77 | Graph traversal and dependencies / Distributed coordination / Collections and algorithms in Python | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 12 | 78-84 | Weighted graphs and connectivity / Observability and operations / Functional tools and caching | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 13 | 85-91 | Greedy choices and exchange arguments / Security and tenancy / Async fundamentals | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 14 | 92-98 | Dynamic programming foundations / URL shortener case study / Async reliability | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 15 | 99-105 | Dynamic programming on grids and strings / Feed case study / Threads and processes | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 16 | 106-112 | Knapsack and advanced DP states / Chat case study / Profiling and memory | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 17 | 113-119 | Bits, arithmetic and range structures / Upload and media case study / Files, text and data boundaries | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 18 | 120-126 | String algorithms and pattern matching / Search and notifications case studies / Persistence and safe I/O | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 19 | 127-133 | Advanced graph and tree practice / Payments and reservations case study / Modules, imports and packaging | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 20 | 134-140 | Data structure design and tradeoffs / Analytics and stream processing / Production Python service code | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 21 | 141-147 | Mixed pattern selection I / Multi-region and advanced tradeoffs / Internals and version-aware Python | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 22 | 148-154 | Mixed pattern selection II / Low-level design and maintainability / Code review and refactoring | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 23 | 155-161 | Mock interviews and weak-area repair / Design interviews and critique / Python interview drills | Two cold DSA re-solves; one SD defense; one Python regression test. |
| 24 | 162-168 | Capstone and retention / Final design portfolio / Python capstone and retention | Two cold DSA re-solves; one SD defense; one Python regression test. |
<!-- granth:phases:end -->

## 8 · Complete day map

The third column assigns IDs; each ID belongs to exactly one day.

<!-- granth:day-map:start -->

### Phase 1 — Cost, invariants and arrays

| Day | Title | IDs assigned |
| --- | --- | --- |
| 1 | DSA: Count target values; SD: Functional scope; Python: Identity and equality | DSA-01, SD-01, PY-01 |
| 2 | DSA: Find the first maximum; SD: Quality requirements; Python: Shallow and deep copies | DSA-02, SD-02, PY-02 |
| 3 | DSA: Stable compaction; SD: Traffic estimates; Python: Mutable defaults | DSA-03, SD-03, PY-03 |
| 4 | DSA: Reverse a segment; SD: Storage estimates; Python: Hash and equality | DSA-04, SD-04, PY-04 |
| 5 | DSA: Merge sorted arrays; SD: Latency budgets; Python: Truth and sentinels | DSA-05, SD-05, PY-05 |
| 6 | DSA: Best single trade; SD: Single-node baseline; Python: Mutation contracts | DSA-06, SD-06, PY-06 |
| 7 | DSA: Week 1 DSA review; SD: Week 1 design review; Python: Week 1 Python review | DSA-07, SD-07, PY-07 |

### Phase 2 — Hashing and prefix sums

| Day | Title | IDs assigned |
| --- | --- | --- |
| 8 | DSA: First repeated value; SD: Request journey; Python: Argument binding | DSA-08, SD-08, PY-08 |
| 9 | DSA: Frequency ranking; SD: HTTP methods; Python: Closure binding | DSA-09, SD-09, PY-09 |
| 10 | DSA: Pair sum indices; SD: Idempotency semantics; Python: Nonlocal state | DSA-10, SD-10, PY-10 |
| 11 | DSA: Group anagrams; SD: Connection budgets; Python: Decorator metadata | DSA-11, SD-11, PY-11 |
| 12 | DSA: Range sums; SD: Timeout propagation; Python: Decorator arguments | DSA-12, SD-12, PY-12 |
| 13 | DSA: Count target subarrays; SD: Pagination; Python: Partial application | DSA-13, SD-13, PY-13 |
| 14 | DSA: Week 2 DSA review; SD: Week 2 design review; Python: Week 2 Python review | DSA-14, SD-14, PY-14 |

### Phase 3 — Two pointers and sliding windows

| Day | Title | IDs assigned |
| --- | --- | --- |
| 15 | DSA: Sorted pair existence; SD: Domain model; Python: Iterator protocol | DSA-15, SD-15, PY-15 |
| 16 | DSA: Unique triples; SD: API contract; Python: Generator laziness | DSA-16, SD-16, PY-16 |
| 17 | DSA: Container capacity; SD: Stateless workers; Python: Generator cleanup | DSA-17, SD-17, PY-17 |
| 18 | DSA: Fixed window maximum sum; SD: Sync versus async; Python: Yield delegation | DSA-18, SD-18, PY-18 |
| 19 | DSA: Longest distinct substring; SD: Compatibility; Python: Iterator consumption | DSA-19, SD-19, PY-19 |
| 20 | DSA: Minimum positive window; SD: Modular monolith; Python: Streaming pipeline | DSA-20, SD-20, PY-20 |
| 21 | DSA: Week 3 DSA review; SD: Week 3 design review; Python: Week 3 Python review | DSA-21, SD-21, PY-21 |

### Phase 4 — Binary search and ordered answers

| Day | Title | IDs assigned |
| --- | --- | --- |
| 22 | DSA: Lower bound; SD: Schema constraints; Python: Representations | DSA-22, SD-22, PY-22 |
| 23 | DSA: Target range; SD: Index selection; Python: Rich comparison | DSA-23, SD-23, PY-23 |
| 24 | DSA: Rotated search; SD: Query plans; Python: Container protocol | DSA-24, SD-24, PY-24 |
| 25 | DSA: Integer square root; SD: Transactions; Python: Indexing and slicing | DSA-25, SD-25, PY-25 |
| 26 | DSA: Minimum shipping capacity; SD: Isolation anomalies; Python: Callable instances | DSA-26, SD-26, PY-26 |
| 27 | DSA: Median of two arrays; SD: Optimistic concurrency; Python: Context managers | DSA-27, SD-27, PY-27 |
| 28 | DSA: Week 4 DSA review; SD: Week 4 design review; Python: Week 4 Python review | DSA-28, SD-28, PY-28 |

### Phase 5 — Sorting, intervals and selection

| Day | Title | IDs assigned |
| --- | --- | --- |
| 29 | DSA: Stable record sorting; SD: Tree indexes; Python: Attribute lookup | DSA-29, SD-29, PY-29 |
| 30 | DSA: Merge overlapping intervals; SD: Log structured storage; Python: Properties | DSA-30, SD-30, PY-30 |
| 31 | DSA: Insert an interval; SD: Access-pattern modeling; Python: Descriptors | DSA-31, SD-31, PY-31 |
| 32 | DSA: Minimum meeting rooms; SD: Hot partitions; Python: Method binding | DSA-32, SD-32, PY-32 |
| 33 | DSA: Kth smallest; SD: TTL and deletion; Python: Inheritance and super | DSA-33, SD-33, PY-33 |
| 34 | DSA: Count inversions; SD: Storage decision memo; Python: Slots | DSA-34, SD-34, PY-34 |
| 35 | DSA: Week 5 DSA review; SD: Week 5 design review; Python: Week 5 Python review | DSA-35, SD-35, PY-35 |

### Phase 6 — Linked lists and pointer invariants

| Day | Title | IDs assigned |
| --- | --- | --- |
| 36 | DSA: Reverse a linked list; SD: Cache aside; Python: Dataclass defaults | DSA-36, SD-36, PY-36 |
| 37 | DSA: Middle node; SD: Invalidation race; Python: Frozen models | DSA-37, SD-37, PY-37 |
| 38 | DSA: Cycle entry; SD: TTL and eviction; Python: Ordering and hashing | DSA-38, SD-38, PY-38 |
| 39 | DSA: Merge linked lists; SD: Stampede control; Python: Enums | DSA-39, SD-39, PY-39 |
| 40 | DSA: Remove from end; SD: Negative caching; Python: Composition | DSA-40, SD-40, PY-40 |
| 41 | DSA: Least recently used cache; SD: CDN behavior; Python: Model boundary | DSA-41, SD-41, PY-41 |
| 42 | DSA: Week 6 DSA review; SD: Week 6 design review; Python: Week 6 Python review | DSA-42, SD-42, PY-42 |

### Phase 7 — Stacks, queues and monotone structures

| Day | Title | IDs assigned |
| --- | --- | --- |
| 43 | DSA: Balanced delimiters; SD: Balancing policies; Python: Annotations at runtime | DSA-43, SD-43, PY-43 |
| 44 | DSA: Queue from stacks; SD: Health checks; Python: Optional and narrowing | DSA-44, SD-44, PY-44 |
| 45 | DSA: Minimum stack; SD: Horizontal scaling; Python: Typed dictionaries | DSA-45, SD-45, PY-45 |
| 46 | DSA: Warmer days; SD: Partition keys; Python: Protocols | DSA-46, SD-46, PY-46 |
| 47 | DSA: Largest histogram rectangle; SD: Consistent placement; Python: Generics | DSA-47, SD-47, PY-47 |
| 48 | DSA: Sliding window maxima; SD: Resharding; Python: Overloads | DSA-48, SD-48, PY-48 |
| 49 | DSA: Week 7 DSA review; SD: Week 7 design review; Python: Week 7 Python review | DSA-49, SD-49, PY-49 |

### Phase 8 — Recursion and backtracking

| Day | Title | IDs assigned |
| --- | --- | --- |
| 50 | DSA: Enumerate subsets; SD: Leader replication; Python: Callable signatures | DSA-50, SD-50, PY-50 |
| 51 | DSA: Enumerate permutations; SD: Read-your-writes; Python: Variance reasoning | DSA-51, SD-51, PY-51 |
| 52 | DSA: Combination sum; SD: Consistency models; Python: Literal states | DSA-52, SD-52, PY-52 |
| 53 | DSA: Balanced parentheses; SD: Quorum reasoning; Python: Type guards | DSA-53, SD-53, PY-53 |
| 54 | DSA: Word search; SD: Network partitions; Python: NewType | DSA-54, SD-54, PY-54 |
| 55 | DSA: Nonattacking queens; SD: Failover; Python: Typing debt | DSA-55, SD-55, PY-55 |
| 56 | DSA: Week 8 DSA review; SD: Week 8 design review; Python: Week 8 Python review | DSA-56, SD-56, PY-56 |

### Phase 9 — Binary trees and search trees

| Day | Title | IDs assigned |
| --- | --- | --- |
| 57 | DSA: Tree depth; SD: Queue fundamentals; Python: Exception chaining | DSA-57, SD-57, PY-57 |
| 58 | DSA: Level order; SD: Delivery semantics; Python: Exception boundaries | DSA-58, SD-58, PY-58 |
| 59 | DSA: Validate search tree; SD: Consumer idempotency; Python: Finally behavior | DSA-59, SD-59, PY-59 |
| 60 | DSA: Kth tree value; SD: Ordering; Python: Contextlib | DSA-60, SD-60, PY-60 |
| 61 | DSA: Tree diameter; SD: Backpressure; Python: ExitStack | DSA-61, SD-61, PY-61 |
| 62 | DSA: Lowest shared ancestor; SD: Poison messages; Python: Exception groups | DSA-62, SD-62, PY-62 |
| 63 | DSA: Week 9 DSA review; SD: Week 9 design review; Python: Week 9 Python review | DSA-63, SD-63, PY-63 |

### Phase 10 — Heaps, tries and tree construction

| Day | Title | IDs assigned |
| --- | --- | --- |
| 64 | DSA: K largest stream values; SD: Retry budgets; Python: Unittest subtests | DSA-64, SD-64, PY-64 |
| 65 | DSA: Merge sorted streams; SD: Backoff and jitter; Python: Test doubles | DSA-65, SD-65, PY-65 |
| 66 | DSA: Running median; SD: Circuit breakers; Python: Mock boundaries | DSA-66, SD-66, PY-66 |
| 67 | DSA: Prefix dictionary; SD: Bulkheads; Python: Property checks | DSA-67, SD-67, PY-67 |
| 68 | DSA: Tree reconstruction; SD: Rate limiting; Python: Metamorphic tests | DSA-68, SD-68, PY-68 |
| 69 | DSA: Tree codec round trip; SD: Graceful degradation; Python: Debugging workflow | DSA-69, SD-69, PY-69 |
| 70 | DSA: Week 10 DSA review; SD: Week 10 design review; Python: Week 10 Python review | DSA-70, SD-70, PY-70 |

### Phase 11 — Graph traversal and dependencies

| Day | Title | IDs assigned |
| --- | --- | --- |
| 71 | DSA: Reachability; SD: Logical ordering; Python: Deque behavior | DSA-71, SD-71, PY-71 |
| 72 | DSA: Unweighted distance; SD: Consensus purpose; Python: Counter algebra | DSA-72, SD-72, PY-72 |
| 73 | DSA: Island count; SD: Leader terms; Python: Default dictionaries | DSA-73, SD-73, PY-73 |
| 74 | DSA: Dependency order; SD: Distributed locks; Python: Heap ordering | DSA-74, SD-74, PY-74 |
| 75 | DSA: Two-color graph; SD: Unique identifiers; Python: Bisect contracts | DSA-75, SD-75, PY-75 |
| 76 | DSA: Multi-source spread; SD: Cross-service transactions; Python: Sorting keys | DSA-76, SD-76, PY-76 |
| 77 | DSA: Week 11 DSA review; SD: Week 11 design review; Python: Week 11 Python review | DSA-77, SD-77, PY-77 |

### Phase 12 — Weighted graphs and connectivity

| Day | Title | IDs assigned |
| --- | --- | --- |
| 78 | DSA: Nonnegative shortest paths; SD: SLIs and SLOs; Python: Itertools grouping | DSA-78, SD-78, PY-78 |
| 79 | DSA: Negative edge paths; SD: Error budgets; Python: Iterator duplication | DSA-79, SD-79, PY-79 |
| 80 | DSA: Disjoint set queries; SD: Logs metrics traces; Python: Bounded iteration | DSA-80, SD-80, PY-80 |
| 81 | DSA: Minimum spanning cost; SD: Tail latency; Python: Function caching | DSA-81, SD-81, PY-81 |
| 82 | DSA: Strong components; SD: Capacity and cost; Python: Cache invalidation | DSA-82, SD-82, PY-82 |
| 83 | DSA: Critical edges; SD: Incident review; Python: Dispatch | DSA-83, SD-83, PY-83 |
| 84 | DSA: Week 12 DSA review; SD: Week 12 design review; Python: Week 12 Python review | DSA-84, SD-84, PY-84 |

### Phase 13 — Greedy choices and exchange arguments

| Day | Title | IDs assigned |
| --- | --- | --- |
| 85 | DSA: Maximum compatible meetings; SD: Trust boundaries; Python: Coroutine lifecycle | DSA-85, SD-85, PY-85 |
| 86 | DSA: Reach the end; SD: Authentication and authorization; Python: Blocking the loop | DSA-86, SD-86, PY-86 |
| 87 | DSA: Minimum jumps; SD: Abuse prevention; Python: Concurrent tasks | DSA-87, SD-87, PY-87 |
| 88 | DSA: Circular fuel route; SD: Secret handling; Python: Cancellation | DSA-88, SD-88, PY-88 |
| 89 | DSA: Task cooldown length; SD: Tenant isolation; Python: Timeout scopes | DSA-89, SD-89, PY-89 |
| 90 | DSA: Optimal merge cost; SD: Retention and audit; Python: Async context managers | DSA-90, SD-90, PY-90 |
| 91 | DSA: Week 13 DSA review; SD: Week 13 design review; Python: Week 13 Python review | DSA-91, SD-91, PY-91 |

### Phase 14 — Dynamic programming foundations

| Day | Title | IDs assigned |
| --- | --- | --- |
| 92 | DSA: Climbing steps; SD: Shortener requirements; Python: Bounded concurrency | DSA-92, SD-92, PY-92 |
| 93 | DSA: Nonadjacent loot; SD: Shortener API and data; Python: Async queues | DSA-93, SD-93, PY-93 |
| 94 | DSA: Minimum coins; SD: Shortener capacity; Python: Task failure | DSA-94, SD-94, PY-94 |
| 95 | DSA: Coin combinations; SD: Shortener architecture; Python: Context variables | DSA-95, SD-95, PY-95 |
| 96 | DSA: Increasing subsequence; SD: Shortener deep dive; Python: Offloading blocking work | DSA-96, SD-96, PY-96 |
| 97 | DSA: Decode digits; SD: Shortener failure review; Python: Async shutdown | DSA-97, SD-97, PY-97 |
| 98 | DSA: Week 14 DSA review; SD: Week 14 design review; Python: Week 14 Python review | DSA-98, SD-98, PY-98 |

### Phase 15 — Dynamic programming on grids and strings

| Day | Title | IDs assigned |
| --- | --- | --- |
| 99 | DSA: Grid path count; SD: Feed requirements; Python: Thread ownership | DSA-99, SD-99, PY-99 |
| 100 | DSA: Minimum grid path; SD: Feed API and data; Python: Condition signaling | DSA-100, SD-100, PY-100 |
| 101 | DSA: Common subsequence length; SD: Feed capacity; Python: Thread pools | DSA-101, SD-101, PY-101 |
| 102 | DSA: Edit distance; SD: Feed architecture; Python: Process pools | DSA-102, SD-102, PY-102 |
| 103 | DSA: Longest palindrome length; SD: Feed deep dive; Python: Serialization cost | DSA-103, SD-103, PY-103 |
| 104 | DSA: Word segmentation; SD: Feed failure review; Python: GIL boundaries | DSA-104, SD-104, PY-104 |
| 105 | DSA: Week 15 DSA review; SD: Week 15 design review; Python: Week 15 Python review | DSA-105, SD-105, PY-105 |

### Phase 16 — Knapsack and advanced DP states

| Day | Title | IDs assigned |
| --- | --- | --- |
| 106 | DSA: Zero-one knapsack; SD: Chat requirements; Python: Measurement design | DSA-106, SD-106, PY-106 |
| 107 | DSA: Equal partition; SD: Chat API and data; Python: CPU profiles | DSA-107, SD-107, PY-107 |
| 108 | DSA: Signed target count; SD: Chat connections; Python: Allocation tracing | DSA-108, SD-108, PY-108 |
| 109 | DSA: Weighted scheduling; SD: Chat architecture; Python: Reference cycles | DSA-109, SD-109, PY-109 |
| 110 | DSA: Matrix chain cost; SD: Chat deep dive; Python: Weak references | DSA-110, SD-110, PY-110 |
| 111 | DSA: Visit every city; SD: Chat failure review; Python: Optimization memo | DSA-111, SD-111, PY-111 |
| 112 | DSA: Week 16 DSA review; SD: Week 16 design review; Python: Week 16 Python review | DSA-112, SD-112, PY-112 |

### Phase 17 — Bits, arithmetic and range structures

| Day | Title | IDs assigned |
| --- | --- | --- |
| 113 | DSA: Single unmatched value; SD: Upload requirements; Python: Path handling | DSA-113, SD-113, PY-113 |
| 114 | DSA: Set bit counts; SD: Upload API and metadata; Python: Unicode normalization | DSA-114, SD-114, PY-114 |
| 115 | DSA: Modular power; SD: Upload capacity; Python: Binary interfaces | DSA-115, SD-115, PY-115 |
| 116 | DSA: Primes below a bound; SD: Upload architecture; Python: JSON boundaries | DSA-116, SD-116, PY-116 |
| 117 | DSA: Mutable range sums; SD: Upload deep dive; Python: Decimal arithmetic | DSA-117, SD-117, PY-117 |
| 118 | DSA: Mutable range minima; SD: Upload failure review; Python: Timezone handling | DSA-118, SD-118, PY-118 |
| 119 | DSA: Week 17 DSA review; SD: Week 17 design review; Python: Week 17 Python review | DSA-119, SD-119, PY-119 |

### Phase 18 — String algorithms and pattern matching

| Day | Title | IDs assigned |
| --- | --- | --- |
| 120 | DSA: Normalize text units; SD: Search requirements; Python: SQLite transactions | DSA-120, SD-120, PY-120 |
| 121 | DSA: Prefix border lengths; SD: Search indexing; Python: CSV streaming | DSA-121, SD-121, PY-121 |
| 122 | DSA: Find all pattern matches; SD: Search query path; Python: Atomic replacement | DSA-122, SD-122, PY-122 |
| 123 | DSA: Rolling hash matching; SD: Notification requirements; Python: Subprocess contracts | DSA-123, SD-123, PY-123 |
| 124 | DSA: Smallest covering window; SD: Notification architecture; Python: Untrusted serialization | DSA-124, SD-124, PY-124 |
| 125 | DSA: Dictionary wildcard search; SD: Notification failure review; Python: Resource limits | DSA-125, SD-125, PY-125 |
| 126 | DSA: Week 18 DSA review; SD: Week 18 design review; Python: Week 18 Python review | DSA-126, SD-126, PY-126 |

### Phase 19 — Advanced graph and tree practice

| Day | Title | IDs assigned |
| --- | --- | --- |
| 127 | DSA: Longest DAG path; SD: Reservation invariants; Python: Import execution | DSA-127, SD-127, PY-127 |
| 128 | DSA: Minimum effort grid route; SD: Reservation data; Python: Circular imports | DSA-128, SD-128, PY-128 |
| 129 | DSA: Redundant undirected edge; SD: Payment idempotency; Python: Entry points | DSA-129, SD-129, PY-129 |
| 130 | DSA: Subtree sizes; SD: Transactional outbox; Python: Package layout | DSA-130, SD-130, PY-130 |
| 131 | DSA: Tree distance sums; SD: Compensation workflow; Python: Environment isolation | DSA-131, SD-131, PY-131 |
| 132 | DSA: Bipartite matching; SD: Reconciliation; Python: Dependency policy | DSA-132, SD-132, PY-132 |
| 133 | DSA: Week 19 DSA review; SD: Week 19 design review; Python: Week 19 Python review | DSA-133, SD-133, PY-133 |

### Phase 20 — Data structure design and tradeoffs

| Day | Title | IDs assigned |
| --- | --- | --- |
| 134 | DSA: Time-indexed values; SD: Analytics requirements; Python: Structured logs | DSA-134, SD-134, PY-134 |
| 135 | DSA: Frequency stack; SD: Event time; Python: Configuration | DSA-135, SD-135, PY-135 |
| 136 | DSA: Least frequently used cache; SD: Aggregation windows; Python: Retry wrapper | DSA-136, SD-136, PY-136 |
| 137 | DSA: Order statistic stream; SD: Partitioned aggregation; Python: Idempotent handler | DSA-137, SD-137, PY-137 |
| 138 | DSA: Expiring counter; SD: Approximate answers; Python: Shutdown hooks | DSA-138, SD-138, PY-138 |
| 139 | DSA: Autocomplete ranking; SD: Replay and rebuild; Python: Error taxonomy | DSA-139, SD-139, PY-139 |
| 140 | DSA: Week 20 DSA review; SD: Week 20 design review; Python: Week 20 Python review | DSA-140, SD-140, PY-140 |

### Phase 21 — Mixed pattern selection I

| Day | Title | IDs assigned |
| --- | --- | --- |
| 141 | DSA: Product except self; SD: Regional topology; Python: Bytecode inspection | DSA-141, SD-141, PY-141 |
| 142 | DSA: Longest consecutive run; SD: Recovery objectives; Python: Object sizes | DSA-142, SD-142, PY-142 |
| 143 | DSA: Trapped rainwater; SD: Conflict resolution; Python: Name resolution | DSA-143, SD-143, PY-143 |
| 144 | DSA: Top frequent words; SD: Data placement; Python: Special method lookup | DSA-144, SD-144, PY-144 |
| 145 | DSA: Rotated minimum with duplicates; SD: Disaster recovery drill; Python: Version compatibility | DSA-145, SD-145, PY-145 |
| 146 | DSA: Find duplicate without mutation; SD: Migration strategy; Python: Implementation portability | DSA-146, SD-146, PY-146 |
| 147 | DSA: Week 21 DSA review; SD: Week 21 design review; Python: Week 21 Python review | DSA-147, SD-147, PY-147 |

### Phase 22 — Mixed pattern selection II

| Day | Title | IDs assigned |
| --- | --- | --- |
| 148 | DSA: Interleaved strings; SD: Responsibilities; Python: API simplification | DSA-148, SD-148, PY-148 |
| 149 | DSA: Course completion time; SD: State machines; Python: Hidden state | DSA-149, SD-149, PY-149 |
| 150 | DSA: Maximum path sum; SD: Dependency inversion; Python: Mutable ownership review | DSA-150, SD-150, PY-150 |
| 151 | DSA: Smallest missing positive; SD: Concurrency contracts; Python: Concurrency review | DSA-151, SD-151, PY-151 |
| 152 | DSA: Shortest subarray with negatives; SD: Extensibility; Python: Typing review | DSA-152, SD-152, PY-152 |
| 153 | DSA: Minimum interval for queries; SD: Design review; Python: Performance review | DSA-153, SD-153, PY-153 |
| 154 | DSA: Week 22 DSA review; SD: Week 22 design review; Python: Week 22 Python review | DSA-154, SD-154, PY-154 |

### Phase 23 — Mock interviews and weak-area repair

| Day | Title | IDs assigned |
| --- | --- | --- |
| 155 | DSA: Mock arrays; SD: Mock requirements round; Python: Semantics drill | DSA-155, SD-155, PY-155 |
| 156 | DSA: Mock search; SD: Mock architecture round; Python: Protocol drill | DSA-156, SD-156, PY-156 |
| 157 | DSA: Mock graph; SD: Mock deep dive; Python: Typing drill | DSA-157, SD-157, PY-157 |
| 158 | DSA: Mock DP; SD: Mock alternative; Python: Concurrency drill | DSA-158, SD-158, PY-158 |
| 159 | DSA: Mock heap; SD: Critique round; Python: Debugging drill | DSA-159, SD-159, PY-159 |
| 160 | DSA: Mock backtracking; SD: Repair round; Python: Review drill | DSA-160, SD-160, PY-160 |
| 161 | DSA: Week 23 DSA review; SD: Week 23 design review; Python: Week 23 Python review | DSA-161, SD-161, PY-161 |

### Phase 24 — Capstone and retention

| Day | Title | IDs assigned |
| --- | --- | --- |
| 162 | DSA: Routing capstone; SD: Capstone brief; Python: Capstone interface | DSA-162, SD-162, PY-162 |
| 163 | DSA: Scheduling capstone; SD: Capstone architecture; Python: Capstone generator | DSA-163, SD-163, PY-163 |
| 164 | DSA: Search capstone; SD: Capstone consistency; Python: Capstone execution | DSA-164, SD-164, PY-164 |
| 165 | DSA: Range capstone; SD: Capstone resilience; Python: Capstone tests | DSA-165, SD-165, PY-165 |
| 166 | DSA: Counterexample capstone; SD: Capstone tradeoffs; Python: Capstone profile | DSA-166, SD-166, PY-166 |
| 167 | DSA: Final independent problem; SD: Final defense; Python: Final explanation | DSA-167, SD-167, PY-167 |
| 168 | DSA: Week 24 DSA review; SD: Week 24 design review; Python: Week 24 Python review | DSA-168, SD-168, PY-168 |
<!-- granth:day-map:end -->

## 9 · Assessment and retention

DSA scores each of correctness, explanation, complexity and test quality from 0 to 2. Pass a
weekly gate at 6/8 or above with correctness=2, including at least one cold solve without hints.
Design scores requirements, data/API, scale and failure tradeoffs from 0 to 2; pass at 6/8 with
no unexplained source of truth. Python passes when you can predict, run, explain and test one
subtle behavior without copying an answer. Scores are diagnostic, not employment guarantees.

Recall prior work at study-day offsets +1, +7 and +21. Daily links list candidates: choose one
for the five-minute recall budget; use weekly review for full re-solves. Missed reviews become
a queue, not three additional mandatory problems. After day 168, use the review queue for
four further weekly retention sessions; these are optional maintenance beyond this plan.

## 10 · Progress and traceability

[TRACK_PROGRESS.csv](TRACK_PROGRESS.csv) is an append-only event ledger: day, track, status,
date, evidence and notes. Status is not-started, partial, needs-review or complete; the latest
row for each pair is current. `python course.py status` shows independent next sessions.
[PROGRESS.md](PROGRESS.md) records a whole day only after all three tracks pass. No study
completion is prefilled. Generated Granth indexes are a plan/authoring view, not the independent
study ledger. A hub-only status is expected for guided assignments without deep chapters.

## 11 · Adapted day contract

Each day contains exactly three topic-named subject folders: dsa_<topic>/, sd_<topic>/ and
lang_<topic>/, plus an orienting LESSON.md and CHECKLIST.md. Actual paths live in sessions.json;
CLI aliases remain dsa, sd and lang. The day-1 folders are dsa_count-target-values,
sd_functional-scope and lang_identity-and-equality.
DSA has README.md, PRACTICE.md, HINTS.md, LEETCODE.md, solution.py, cases.json, test_solution.py and NOTES.md.
Review days point to explicit earlier core problems and have their own replacement solve target.
SD has a bounded assignment, design-response template and checklist. Python has a focused lab
assignment, unsolved lab.py and notes. Each subject can be opened without reading the other two.

Every expanded SD day also includes an author-written `REFERENCE_DESIGN.md`: a complete response
to the day's actual task with assumptions, the requested artifact or calculation, a decision,
an alternative, a failure walkthrough, and a self-review. The assistant writes that reference;
the learner fills `TODO(me)` in `DESIGN.md` as personal practice. Preserve existing practice
content. A concept lesson alone is no longer sufficient to declare an SD day fully expanded.
Days 001–040 include references; remaining planned days receive them when expanded.

Choose guided reading (concepts → reference → own attempt) or independent practice (concepts
→ own attempt → reference comparison). Record help used. Reading a reference is available
without completing practice, but does not count as learner completion. Weekly cold reviews
still start without answers. Use the existing 30-minute reference/practice/critique windows,
not another mandatory design. See [the SD method](SD_DESIGN_GUIDE.md#who-fills-the-todos) and
[ADR-0003](adr/ADR-0003-system-design-reference-and-practice.md).

A complete practice session includes understanding the contract, a baseline, an independent
attempt, boundary tests, a complexity argument and a failure note. Provided example fixtures are
smoke checks, not exhaustive correctness proofs. Add your own cases and a small brute-force oracle
where feasible. Solutions intentionally raise NotImplementedError until you implement them.

Full teaching chapters may later be written within each subject folder, one idea per document,
with motivation, mechanism, real failure evidence and production implications. Consult the
vendored Granth contract for that expansion. Never disguise assignment briefs as full chapters.
Use `python course.py check` for this format. Upstream `granth.py depth` cannot validate it;
its no-clock/parts-folder assumptions remain unchanged in the preserved upstream code.

## 12 · Teaching and practice style

Teach the topic before presenting its practice route. Every subject README starts with a
linked navigation section explaining what to read, what to try, how to verify, and where to
record evidence. For an expanded day, CONCEPTS.md is the first teaching entry point: explain
the underlying idea, how to recognize it, why it works, its assumptions and costs, a worked
example, and a readiness check before the learner opens the problem. Teach general techniques
openly; reserve problem-specific rescue hints for after an independent attempt. Follow
[the teaching workflow](TEACHING_WORKFLOW.md) for every future day expansion. Existing future
briefs may link a clearly labeled preparation guide until their full topic lesson is written.

Maintain three common files for recall without a new exercise: [DSA](DSA_RECALL.md),
[Python](LANG_RECALL.md), and [system design](SD_RECALL.md). Add a compact day card when its
teaching material is expanded, link it from the subject README, and let readers select the
topics they have already studied using their independent track progress. Summary availability
does not imply completion. This optional reading mode does not replace weekly cold assessments.

Use plain language and explicit contracts. Explain why a pattern applies before writing code.
Draw state or data flow where it clarifies an invariant. Keep hints separate and staged. No solved
learner reps. Name actual observed failures; never fabricate a traceback or benchmark. Python
does not repeat beginner syntax, loops or basic function lessons. State CPython-specific behavior
as such. Advanced and optional work must fit spare time or a later review session.

## 13 · Amendments

2026-09-18: v1.0.0 adopted with the user's timing/layout overriding upstream defaults; see
[ADR-0001](adr/ADR-0001-the-plan-as-adopted.md). Scope, sequencing or layout changes require an
append-only decision and changelog entry before renumbering. No automatic commit is part of study.

2026-09-19: v1.1.0 adds topic-named subject folders and LeetCode interview assignments under
[ADR-0002](adr/ADR-0002-topic-folders-and-interview-practice.md). The 168-day order and IDs are unchanged.
