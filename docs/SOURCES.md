# Source ledger — Krama

Append-only. **Never invent a citation** (plan §11.4.1, rule 5). Every primary source a document
teaches or cites gets a row here, and the row is written **only after the record was opened
live** and the title copied from it rather than from memory.

This is the strictest of the three verification rules because it fails the most quietly. A wrong
version pin breaks the next install. A plausible identifier attached to the wrong title survives
for years, gets copied into other people's notes, and is never caught.

**Cite by title and identifier, never by author.** The identifier resolves to exactly one
document, and it is what a reader types.

Accepted identifier forms: `arXiv:2401.12345` · `doi:10.1145/3597503` · `RFC 9110` ·
`ISO/IEC 9899:2018` · `spec:<name>-<revision>`. Anything citation-shaped that matches none of
these is rejected by `python granth.py depth`.

| Identifier | Exact title | Year | URL | Record checked | Taught on | Cited by |
| ---------- | ----------- | ---- | --- | -------------- | --------- | -------- |

| spec:python-3.12-library | The Python Standard Library | rolling | https://docs.python.org/3.12/library/index.html | 2026-09-18 | assigned reference | Python track |
| spec:python-data-model | 3. Data model | rolling | https://docs.python.org/3/reference/datamodel.html | 2026-09-18 | assigned reference | Python track; compare version before using new behavior |
| spec:algorithms-2020 | Introduction to Algorithms | 2020 | https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ | 2026-09-18 | assigned reference | DSA track |
| RFC 9110 | HTTP Semantics | 2022 | https://www.rfc-editor.org/rfc/rfc9110.html | 2026-09-18 | assigned reference | SD weeks 1–3 |
| spec:postgres-concurrency | Chapter 13. Concurrency Control | rolling | https://www.postgresql.org/docs/current/mvcc.html | 2026-09-18 | assigned reference | SD database and transaction sessions |
| spec:consensus-paper | In Search of an Understandable Consensus Algorithm | 2014 | https://raft.github.io/raft.pdf | 2026-09-18 | assigned reference | SD coordination sessions |
| spec:sre-book | Site Reliability Engineering — Table of Contents | rolling | https://sre.google/sre-book/table-of-contents/ | 2026-09-18 | assigned reference | SD reliability and operations |

These landing pages/records were opened live. Individual linked chapters are assigned readings,
not claims of a fresh verification of every interface. Recheck the exact versioned page before
each lab. Case-study workloads and service targets are hypothetical design inputs.

## LeetCode interview-practice references — 2026-09-19

The official [Top Interview 150](https://leetcode.com/studyplan/top-interview-150/) and
[LeetCode 75](https://leetcode.com/studyplan/leetcode-75/) pages were opened during this update.
Individual official problem-page records, difficulty observations and access status are in
[leetcode_sources.json](leetcode_sources.json); course assignments are in [LEETCODE_INDEX.md](LEETCODE_INDEX.md).
These are pattern-based recommendations, not verified employer-frequency data. No paid problem
statement was reproduced; the two subscription-gated companions retain free local alternatives.

The base Jump Game URL timed out; its [official description page](https://leetcode.com/problems/jump-game/description/)
was successfully checked on 2026-09-19, confirming problem 55 and Medium difficulty.

## Day 1 teaching expansion — 2026-09-19

The following official pages were opened live for the Day 1 teaching documents. Python author
demonstrations were executed locally on Python 3.12.10. The HTTP example is a synthetic response
fixture, not a network test. No learner completion or online acceptance is implied.

| Identifier | Exact title | Year | URL | Record checked | Taught on | Cited by |
| --- | --- | --- | --- | --- | --- | --- |
| spec:python-3.12-data-model | 3. Data model | rolling, version 3.12 | https://docs.python.org/3.12/reference/datamodel.html | 2026-09-19 | Day 1 Python | lang_identity-and-equality/CONCEPTS.md |
| spec:python-3.12-expressions | 6. Expressions | rolling, version 3.12 | https://docs.python.org/3.12/reference/expressions.html | 2026-09-19 | Day 1 Python | lang_identity-and-equality/CONCEPTS.md |
| spec:python-3.12-copy | copy — Shallow and deep copy operations | rolling, version 3.12 | https://docs.python.org/3.12/library/copy.html | 2026-09-19 | Day 1 optional Python follow-up | lang_identity-and-equality/CONCEPTS.md |
| RFC 9110 | HTTP Semantics | 2022 | https://www.rfc-editor.org/rfc/rfc9110.html | 2026-09-19 | Day 1 scope and redirect trace | sd_functional-scope/CONCEPTS.md |
| spec:leetcode-1365 | How Many Numbers Are Smaller Than the Current Number | rolling | https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/ | 2026-09-19 | Day 1 DSA companion | dsa_count-target-values/LEETCODE.md |

## Day 1 explanation and recall update — 2026-09-22

Reopened the following primary pages for the extended explanations and recall cards. The
inventory frequency trace is an original derivation. Source checks are not learner evidence.

| Identifier | Exact title | Year | URL | Record checked | Taught on | Cited by |
| --- | --- | --- | --- | --- | --- | --- |
| spec:leetcode-1365 | How Many Numbers Are Smaller Than the Current Number | rolling | https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/ | 2026-09-22 | Day 1 bounded counting domain | dsa_count-target-values/FREQUENCY_COUNTS.md |
| spec:python-3.12-data-model | 3. Data model | rolling, version 3.12 | https://docs.python.org/3.12/reference/datamodel.html | 2026-09-22 | Day 1 identity and ownership | lang_identity-and-equality/CONCEPTS.md |
| spec:python-3.12-expressions | 6. Expressions | rolling, version 3.12 | https://docs.python.org/3.12/reference/expressions.html | 2026-09-22 | Day 1 comparison semantics | lang_identity-and-equality/CONCEPTS.md |
| RFC 9110 | HTTP Semantics | 2022 | https://www.rfc-editor.org/rfc/rfc9110.html | 2026-09-22 | Day 1 redirect boundaries | sd_functional-scope/CONCEPTS.md |

## Days 2–4 teaching expansion — 2026-09-22

The official pages below were opened live for the expanded explanations and online contract
comparisons. All 11 Python teaching blocks across the ten new documents were executed on
Python 3.12.10; printed results matched their embedded transcripts, including deliberate
failure observations and repairs. Runs used isolated teaching fixtures, never learner files.
The design workloads, target values, and overhead factors are hypothetical inputs. Storage
arithmetic and worked traces are original derivations, not measured infrastructure behavior.

| Identifier | Exact title | Year | URL | Record checked | Taught on | Cited by |
| --- | --- | --- | --- | --- | --- | --- |
| spec:python-3.12-copy | copy — Shallow and deep copy operations | rolling, version 3.12 | https://docs.python.org/3.12/library/copy.html | 2026-09-22 | Day 2 ownership and copying | lang_shallow-and-deep-copies/CONCEPTS.md |
| spec:python-3.12-defaults | 4. More Control Flow Tools | rolling, version 3.12 | https://docs.python.org/3.12/tutorial/controlflow.html#default-argument-values | 2026-09-22 | Day 3 default evaluation | lang_mutable-defaults/CONCEPTS.md |
| spec:python-3.12-data-model | 3. Data model | rolling, version 3.12 | https://docs.python.org/3.12/reference/datamodel.html#object.__hash__ | 2026-09-22 | Day 4 equality and hash obligations | lang_hash-and-equality/CONCEPTS.md |
| spec:python-3.12-builtins | Built-in Types | rolling, version 3.12 | https://docs.python.org/3.12/library/stdtypes.html#sequence-types-list-tuple-range | 2026-09-22 | Days 2–4 list, dictionary, and sequence interface checks | DSA and Python teaching demonstrations |
| spec:sre-slos | Service Level Objectives | 2016 | https://sre.google/sre-book/service-level-objectives/ | 2026-09-22 | Day 2 measurable quality targets | sd_quality-requirements/CONCEPTS.md |
| spec:sre-overload | Handling Overload | 2016 | https://sre.google/sre-book/handling-overload/ | 2026-09-22 | Day 3 limits of QPS as a capacity measure | sd_traffic-estimates/CONCEPTS.md |
| spec:leetcode-747 | Largest Number At Least Twice of Others | rolling | https://leetcode.com/problems/largest-number-at-least-twice-of-others/ | 2026-09-22 | Day 2 dominance contract | dsa_find-the-first-maximum/DOMINANCE.md and LEETCODE.md |
| spec:leetcode-283 | Move Zeroes | rolling | https://leetcode.com/problems/move-zeroes/ | 2026-09-22 | Day 3 stable in-place ordering | dsa_stable-compaction/CONCEPTS.md and LEETCODE.md |
| spec:leetcode-344 | Reverse String | rolling | https://leetcode.com/problems/reverse-string/ | 2026-09-22 | Day 4 whole-array online variation | dsa_reverse-a-segment/CONCEPTS.md and LEETCODE.md |

## Day 5 teaching expansion — 2026-09-22

Opened these official pages live for Day 005. Executed all four Python teaching blocks on
Python 3.12.10 and compared actual output with the embedded transcripts, including the
deliberate failures and repairs. The paired-request latency dataset and allocation are
original synthetic fixtures, not production measurements. Learner files were not executed
or filled in, and these checks do not establish learner completion or online acceptance.

| Identifier | Exact title | Year | URL | Record checked | Taught on | Cited by |
| --- | --- | --- | --- | --- | --- | --- |
| spec:leetcode-88 | Merge Sorted Array | rolling | https://leetcode.com/problems/merge-sorted-array/ | 2026-09-22 | Day 5 logical lengths and destination mutation | dsa_merge-sorted-arrays/BACKWARD_MERGE.md and LEETCODE.md |
| spec:python-3.12-builtins | Built-in Types | rolling, version 3.12 | https://docs.python.org/3.12/library/stdtypes.html#truth-value-testing | 2026-09-22 | Day 5 truth testing, Boolean operators, and mapping lookup | lang_truth-and-sentinels/CONCEPTS.md |
| spec:python-3.12-expressions | 6. Expressions | rolling, version 3.12 | https://docs.python.org/3.12/reference/expressions.html#is | 2026-09-22 | Day 5 identity-tested markers | lang_truth-and-sentinels/CONCEPTS.md |
| spec:sre-slos | Service Level Objectives | 2016 | https://sre.google/sre-book/service-level-objectives/ | 2026-09-22 | Day 5 latency distributions and target boundaries | sd_latency-budgets/CONCEPTS.md |

## Days 6–8 teaching expansion — 2026-09-22

The following official pages were opened live. All nine new Python teaching blocks were run
on Python 3.12.10; their actual output was inserted into the lessons, including deliberate
failures and repairs. System-design timings, workloads, capacity figures, and failure
walkthroughs are hypothetical. The executed calculations are not network traces, database
benchmarks, crash tests, or learner evidence. Day 7 reviews existing sources and mechanisms;
its reference is for comparison after the cold attempt.

| Identifier | Exact title | Year | URL | Record checked | Taught on | Cited by |
| --- | --- | --- | --- | --- | --- | --- |
| spec:leetcode-121 | Best Time to Buy and Sell Stock | rolling | https://leetcode.com/problems/best-time-to-buy-and-sell-stock/ | 2026-09-22 | Day 6 ordered trade contract | dsa_best-single-trade/CONCEPTS.md and LEETCODE.md |
| spec:leetcode-217 | Contains Duplicate | rolling | https://leetcode.com/problems/contains-duplicate/ | 2026-09-22 | Day 8 Boolean versus encounter-order contract | dsa_first-repeated-value/CONCEPTS.md and LEETCODE.md |
| spec:leetcode-1365 | How Many Numbers Are Smaller Than the Current Number | rolling | https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/ | 2026-09-22 | Day 7 review of Day 1 | dsa_week-1-dsa-review/CONCEPTS.md |
| spec:leetcode-88 | Merge Sorted Array | rolling | https://leetcode.com/problems/merge-sorted-array/ | 2026-09-22 | Day 7 review of Day 5 | dsa_week-1-dsa-review/CONCEPTS.md |
| spec:python-3.12-data-structures | 5. Data Structures | rolling, version 3.12 | https://docs.python.org/3.12/tutorial/datastructures.html | 2026-09-22 | Day 6 mutation and Day 7 ownership review | lang_mutation-contracts/CONCEPTS.md and lang_week-1-python-review/CONCEPTS.md |
| spec:python-3.12-special-parameters | 4. More Control Flow Tools | rolling, version 3.12 | https://docs.python.org/3.12/tutorial/controlflow.html#special-parameters | 2026-09-22 | Day 8 parameter categories | lang_argument-binding/CONCEPTS.md |
| spec:python-3.12-expressions | 6. Expressions | rolling, version 3.12 | https://docs.python.org/3.12/reference/expressions.html#calls | 2026-09-22 | Day 8 argument binding | lang_argument-binding/CONCEPTS.md |
| spec:python-3.12-builtins | Built-in Types | rolling, version 3.12 | https://docs.python.org/3.12/library/stdtypes.html#set-types-set-frozenset | 2026-09-22 | Day 8 set membership | dsa_first-repeated-value/CONCEPTS.md |
| spec:sre-overload | Handling Overload | 2016 | https://sre.google/sre-book/handling-overload/ | 2026-09-22 | Days 6–7 workload-dependent limits | sd_single-node-baseline and sd_week-1-design-review teaching |
| RFC 1034 | DOMAIN NAMES - CONCEPTS AND FACILITIES | 1987 | https://www.rfc-editor.org/rfc/rfc1034.html | 2026-09-22 | Day 8 name resolution | sd_request-journey/CONCEPTS.md and REFERENCE_DESIGN.md |
| RFC 9293 | Transmission Control Protocol (TCP) | 2022 | https://www.rfc-editor.org/rfc/rfc9293.html | 2026-09-22 | Day 8 connection establishment | sd_request-journey/CONCEPTS.md and REFERENCE_DESIGN.md |
| RFC 8446 | The Transport Layer Security (TLS) Protocol Version 1.3 | 2018 | https://www.rfc-editor.org/rfc/rfc8446.html | 2026-09-22 | Day 8 secure handshake | sd_request-journey/CONCEPTS.md and REFERENCE_DESIGN.md |
| RFC 9110 | HTTP Semantics | 2022 | https://www.rfc-editor.org/rfc/rfc9110.html | 2026-09-22 | Days 6 and 8 redirect boundaries | sd_single-node-baseline/REFERENCE_DESIGN.md and sd_request-journey teaching |

## Days 9–12 teaching expansion — 2026-09-22

Opened the following official records live for the four-day expansion. Executed all twelve
new Python teaching blocks on Python 3.12.10 and inserted their actual output, including the
deliberate failures and repaired checks. SD workloads, limits, timelines, API policies, and
failure walkthroughs are hypothetical. The local models are not HTTP integration tests,
database crash tests, load measurements, or cancellation tests. No learner solution, lab,
personal evidence, or completion ledger was changed. No online acceptance is claimed.

| Identifier | Exact title | Year | URL | Record checked | Taught on | Cited by |
| --- | --- | --- | --- | --- | --- | --- |
| spec:leetcode-347 | Top K Frequent Elements | rolling | https://leetcode.com/problems/top-k-frequent-elements/ | 2026-09-22 | Day 9 top-k contract and follow-up | dsa_frequency-ranking/CONCEPTS.md and LEETCODE.md |
| spec:leetcode-1 | Two Sum | rolling | https://leetcode.com/problems/two-sum/ | 2026-09-22 | Day 10 unique online solution versus local ordering | dsa_pair-sum-indices/CONCEPTS.md and LEETCODE.md |
| spec:leetcode-49 | Group Anagrams | rolling | https://leetcode.com/problems/group-anagrams/ | 2026-09-22 | Day 11 alphabet and output ordering | dsa_group-anagrams/CONCEPTS.md and LEETCODE.md |
| spec:leetcode-303 | Range Sum Query - Immutable | rolling | https://leetcode.com/problems/range-sum-query-immutable/ | 2026-09-22 | Day 12 constructor and inclusive query interface | dsa_range-sums/CONCEPTS.md and LEETCODE.md |
| spec:python-3.12-programming-faq | Programming FAQ | rolling, version 3.12 | https://docs.python.org/3.12/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result | 2026-09-22 | Day 9 delayed callback lookup | lang_closure-binding/CONCEPTS.md |
| spec:python-3.12-simple-statements | 7. Simple statements | rolling, version 3.12 | https://docs.python.org/3.12/reference/simple_stmts.html#the-nonlocal-statement | 2026-09-22 | Day 10 nonlocal binding | lang_nonlocal-state/CONCEPTS.md |
| spec:python-3.12-functools | functools — Higher-order functions and operations on callable objects | rolling, version 3.12 | https://docs.python.org/3.12/library/functools.html#functools.wraps | 2026-09-22 | Day 11 wraps; reused Day 12 | lang_decorator-metadata/CONCEPTS.md |
| spec:python-3.12-inspect | inspect — Inspect live objects | rolling, version 3.12 | https://docs.python.org/3.12/library/inspect.html#inspect.signature | 2026-09-22 | Day 11 signature inspection | lang_decorator-metadata/CONCEPTS.md |
| spec:python-3.12-compound-statements | 8. Compound statements | rolling, version 3.12 | https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions | 2026-09-22 | Day 12 decorator application | lang_decorator-arguments/CONCEPTS.md |
| RFC 9110 | HTTP Semantics | 2022 | https://www.rfc-editor.org/rfc/rfc9110.html | 2026-09-22 | Days 9–10 method and effect semantics | sd_http-methods and sd_idempotency-semantics teaching |
| RFC 9111 | HTTP Caching | 2022 | https://www.rfc-editor.org/rfc/rfc9111.html | 2026-09-22 | Day 9 explicit cache directives | sd_http-methods/CONCEPTS.md and REFERENCE_DESIGN.md |
| spec:postgresql-16-connections | 20.3. Connections and Authentication | rolling, version 16 | https://www.postgresql.org/docs/16/runtime-config-connection.html | 2026-09-22 | Day 11 connection limits and reserved slots | sd_connection-budgets/CONCEPTS.md and REFERENCE_DESIGN.md |
| spec:grpc-deadlines | Deadlines | rolling | https://grpc.io/docs/guides/deadlines/ | 2026-09-22 | Day 12 remaining-time propagation | sd_timeout-propagation/CONCEPTS.md and REFERENCE_DESIGN.md |
| spec:grpc-cancellation | Cancellation | rolling | https://grpc.io/docs/guides/cancellation/ | 2026-09-22 | Day 12 cooperative handler cancellation | sd_timeout-propagation/CONCEPTS.md and REFERENCE_DESIGN.md |


## Days 13–16 teaching checks — 2026-09-22

Public pages below were opened on this date. Examples in CONCEPTS.md were executed locally;
SQL, HTTP exchanges, and service timelines in references are explicitly design sketches.

| Identifier | Title | Version/year | URL | Checked | Used for |
| --- | --- | --- | --- | --- | --- |
| spec:leetcode-560 | Subarray Sum Equals K | live problem | https://leetcode.com/problems/subarray-sum-equals-k/ | 2026-09-22 | Day 13 nonempty signed subarray count |
| spec:leetcode-217 | Contains Duplicate | live problem | https://leetcode.com/problems/contains-duplicate/ | 2026-09-22 | Day 14 boolean versus first-repeat contract |
| spec:leetcode-303 | Range Sum Query - Immutable | live problem | https://leetcode.com/problems/range-sum-query-immutable/ | 2026-09-22 | Day 14 inclusive queries and NumArray interface |
| spec:leetcode-167 | Two Sum II - Input Array Is Sorted | live problem | https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/ | 2026-09-22 | Day 15 one-based indices and unique solution |
| spec:leetcode-15 | 3Sum | live problem | https://leetcode.com/problems/3sum/ | 2026-09-22 | Day 16 distinct indices, unique triples, arbitrary order |
| spec:python-312-partial | functools — Higher-order functions and operations on callable objects | 3.12 | https://docs.python.org/3.12/library/functools.html#functools.partial | 2026-09-22 | Day 13 argument storage and keyword override |
| spec:python-312-faq-closures | Programming FAQ | 3.12 | https://docs.python.org/3.12/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result | 2026-09-22 | Day 14 closure lookup versus default capture |
| spec:python-312-iterators | Built-in Types — Iterator Types | 3.12 | https://docs.python.org/3.12/library/stdtypes.html#iterator-types | 2026-09-22 | Day 15 permanent exhaustion |
| spec:python-312-yield | Expressions — Yield expressions | 3.12 | https://docs.python.org/3.12/reference/expressions.html#yield-expressions | 2026-09-22 | Day 16 suspended body and resumption |
| spec:postgresql-18-limit | 7.6. LIMIT and OFFSET | 18 | https://www.postgresql.org/docs/18/queries-limit.html | 2026-09-22 | Days 13–14 ordered pagination and skipped-row work |
| spec:postgresql-18-constraints | 5.5. Constraints | 18 | https://www.postgresql.org/docs/18/ddl-constraints.html | 2026-09-22 | Day 15 primary, unique and foreign keys |
| RFC 9110 | HTTP Semantics | 2022 | https://www.rfc-editor.org/rfc/rfc9110.html | 2026-09-22 | Day 16 methods and response status semantics |
| RFC 3339 | Date and Time on the Internet: Timestamps | 2002 | https://www.rfc-editor.org/rfc/rfc3339.html | 2026-09-22 | Day 16 explicit timezone offset and timestamp subset |

## Days 17–20 teaching checks — 2026-09-22

Official pages below were opened for the named claims. Python examples were executed locally;
service diagrams, thresholds, and timelines are hypothetical designs. The Python web pages
track the 3.12 maintenance series; executable evidence records the installed interpreter.

| Identifier | Exact title | Version/year | URL | Checked | Use |
| --- | --- | --- | --- | --- | --- |
| LeetCode 11 | Container With Most Water | Live problem | https://leetcode.com/problems/container-with-most-water/ | 2026-09-22 | Day 17 area and nonnegative-height contract |
| LeetCode 643 | Maximum Average Subarray I | Live problem | https://leetcode.com/problems/maximum-average-subarray-i/ | 2026-09-22 | Day 18 average versus local sum, fixed positive k |
| LeetCode 3 | Longest Substring Without Repeating Characters | Live problem | https://leetcode.com/problems/longest-substring-without-repeating-characters/ | 2026-09-22 | Day 19 contiguous substring and empty input |
| LeetCode 209 | Minimum Size Subarray Sum | Live problem | https://leetcode.com/problems/minimum-size-subarray-sum/ | 2026-09-22 | Day 20 positive input and no-answer result |
| Python expressions | 6. Expressions | 3.12 | https://docs.python.org/3.12/reference/expressions.html | 2026-09-22 | Generator close, membership consumption, generator-expression timing |
| Python contextlib | contextlib — Utilities for with-statement contexts | 3.12 | https://docs.python.org/3.12/library/contextlib.html | 2026-09-22 | Day 17 consumer-owned closing scope |
| PEP 380 | Syntax for Delegating to a Subgenerator | 2009 | https://peps.python.org/pep-0380/ | 2026-09-22 | Day 18 yield from and StopIteration.value |
| Python itertools | itertools — Functions creating iterators for efficient looping | 3.12 | https://docs.python.org/3.12/library/itertools.html | 2026-09-22 | Days 19–20 tee buffering and iterator composition |
| Twelve-Factor VI | The Twelve-Factor App — VI. Processes | Live page | https://12factor.net/processes | 2026-09-22 | Day 17 replaceable processes and backing state |
| Azure async pattern | Asynchronous Request-Reply pattern | Live page | https://learn.microsoft.com/en-us/azure/architecture/patterns/asynchronous-request-reply | 2026-09-22 | Day 18 acceptance versus completion; adapted to internal analytics |
| AIP-180 | Backwards compatibility | Live guidance | https://google.aip.dev/180 | 2026-09-22 | Day 19 wire and semantic compatibility, additive changes |
| Azure architecture | Microservices architecture style | Live page | https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices | 2026-09-22 | Day 20 independent scaling and distributed-system complexity |

The async pattern page redirected from /patterns/async-request-reply to the canonical address
recorded above. These sources support technical semantics; no source claims that the authored
service numbers were measured or that a problem occurs at a particular employer.

## Days 25–28 teaching checks — 2026-09-23

Official pages below were opened live for the named claims. Examples and proofs are original
teaching material. Python output records the installed 3.12.10 interpreter; Python web
documentation follows the 3.12 maintenance series. PostgreSQL designs were not executed.

| Identifier | Exact title | Version/year | URL | Checked | Use |
| --- | --- | --- | --- | --- | --- |
| LeetCode 69 | Sqrt(x) | Live problem | https://leetcode.com/problems/sqrtx/ | 2026-09-23 | Day 25 floor root and operation restrictions |
| LeetCode 1011 | Capacity To Ship Packages Within D Days | Live problem | https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/ | 2026-09-23 | Days 26 and 28 order and deadline contract |
| LeetCode 4 | Median of Two Sorted Arrays | Live problem | https://leetcode.com/problems/median-of-two-sorted-arrays/ | 2026-09-23 | Day 27 median and runtime contract |
| LeetCode 35 | Search Insert Position | Live problem | https://leetcode.com/problems/search-insert-position/ | 2026-09-23 | Day 28 existing review companion |
| Python data model | 3. Data model | 3.12 | https://docs.python.org/3.12/reference/datamodel.html | 2026-09-23 | Days 25–28 subscription, callable objects, special-method dispatch |
| Python functions | Built-in Functions | 3.12 | https://docs.python.org/3.12/library/functions.html | 2026-09-23 | Day 25 slice descriptor |
| Python inspect | inspect — Inspect live objects | 3.12 | https://docs.python.org/3.12/library/inspect.html | 2026-09-23 | Day 26 named closure inspection |
| Python compound statements | 8. Compound statements | 3.12 | https://docs.python.org/3.12/reference/compound_stmts.html | 2026-09-23 | Day 27 with entry, exit, and suppression |
| Python sqlite3 | sqlite3 — DB-API 2.0 interface for SQLite databases | 3.12 | https://docs.python.org/3.12/library/sqlite3.html | 2026-09-23 | Day 25 local rollback demonstration |
| PostgreSQL transactions | 3.4. Transactions | 18 | https://www.postgresql.org/docs/18/tutorial-transactions.html | 2026-09-23 | Day 25 transaction boundary |
| PostgreSQL isolation | 13.2. Transaction Isolation | 18 | https://www.postgresql.org/docs/18/transaction-iso.html | 2026-09-23 | Days 26–28 isolation and retry semantics |
| PostgreSQL update | UPDATE | 18 | https://www.postgresql.org/docs/18/sql-update.html | 2026-09-23 | Days 25–28 conditional update and returned rows |
| RFC 9110 | HTTP Semantics | 2022 | https://www.rfc-editor.org/rfc/rfc9110.html | 2026-09-23 | Days 27–28 If-Match preconditions |

Days 21–24 already contained authored teaching files at the start of this expansion. Their
navigation and recall cards were connected here; their historical source-check dates were
not relabeled as new live verification.

## Days 29–36 teaching checks — 2026-09-23

Opened the official pages below for the listed semantics. Algorithm proofs, hand traces,
design decisions, and numeric scenarios are original teaching material. Python demonstrations
ran on the installed 3.12.10 interpreter; online Python documentation is the 3.12 maintenance
series. No storage engine, cache service, or concurrent database was deployed or benchmarked.

| Identifier | Exact title and URL | Version/year | Checked | Use |
| --- | --- | --- | --- | --- |
| LeetCode 912 | [Sort an Array](https://leetcode.com/problems/sort-an-array/) | Live problem | 2026-09-23 | Days 29/35 numeric sorting and built-in-sort restriction |
| LeetCode 56 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Live problem | 2026-09-23 | Day 30 touching closed endpoints |
| LeetCode 57 | [Insert Interval](https://leetcode.com/problems/insert-interval/) | Live problem | 2026-09-23 | Day 31 sorted disjoint input and insertion |
| LeetCode 2406 | [Divide Intervals Into Minimum Number of Groups](https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups/) | Live problem | 2026-09-23 | Day 32 closed intervals versus local half-open meetings |
| LeetCode 215 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Live problem | 2026-09-23 | Days 33/35 largest versus smallest rank; duplicates count |
| LeetCode 493 | [Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) | Live problem | 2026-09-23 | Day 34 doubled-right-value predicate |
| LeetCode 206 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Live problem | 2026-09-23 | Day 36 node-head interface versus local serialization |
| Python sorting | [Sorting Techniques](https://docs.python.org/3.12/howto/sorting.html) | 3.12 | 2026-09-23 | Day 29 stable built-in oracle and key-based ordering |
| Python descriptors | [Descriptor Guide](https://docs.python.org/3.12/howto/descriptor.html) | 3.12 | 2026-09-23 | Days 29–32 precedence, properties, field descriptors, bound methods |
| Python data model | [3. Data model](https://docs.python.org/3.12/reference/datamodel.html) | 3.12 | 2026-09-23 | Days 29–35 attribute lookup, inheritance, slots |
| Python builtins | [Built-in Functions](https://docs.python.org/3.12/library/functions.html#super) | 3.12 | 2026-09-23 | Day 33 cooperative super and actual-instance MRO |
| Python sys | [sys — System-specific parameters and functions](https://docs.python.org/3.12/library/sys.html#sys.getsizeof) | 3.12 | 2026-09-23 | Day 34 shallow object-size measurement boundary |
| Python dataclasses | [dataclasses — Data Classes](https://docs.python.org/3.12/library/dataclasses.html) | 3.12 | 2026-09-23 | Day 36 field factories and mutable-default rejection |
| PostgreSQL B-tree | [65.1. B-Tree Indexes](https://www.postgresql.org/docs/18/btree.html) | 18 | 2026-09-23 | Day 29 ordered-index context; split drawing is a generic model |
| PostgreSQL multicolumn | [11.3. Multicolumn Indexes](https://www.postgresql.org/docs/18/indexes-multicolumn.html) | 18 | 2026-09-23 | Days 31/34 equality-prefix ordered access |
| RocksDB introduction | [Getting started](https://rocksdb.org/docs/getting-started.html) | Live documentation | 2026-09-23 | Day 30 WAL, memtable, immutable file components |
| RocksDB compaction | [Leveled Compaction](https://github.com/facebook/rocksdb/wiki/Leveled-Compaction) | Live documentation | 2026-09-23 | Day 30 maintenance and read/write/space tradeoffs |
| DynamoDB key design | [Best practices for designing and using partition keys effectively in DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html) | Live documentation | 2026-09-23 | Days 32/34/35 request skew; example capacities are assumptions |
| DynamoDB TTL | [Working with expired items and time to live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ttl-expired-items.html) | Live documentation | 2026-09-23 | Days 33/35 filtering expired items while cleanup is pending |
| Azure cache pattern | [Cache-Aside Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside) | Live documentation | 2026-09-23 | Day 36 miss loading, invalidation, and consistency limitations |

The PostgreSQL 18 B-tree implementation subpage could not be retrieved during source checks.
No claim of checking its split/recovery details is made; Day 29 labels its split as a simplified
generic model and leaves engine-specific recovery verification as a next step. Tombstone
retention durations, freshness targets, capacities, and request deadlines elsewhere are stated
design assumptions, not vendor limits or measured production observations.
