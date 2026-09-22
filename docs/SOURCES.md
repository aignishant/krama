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
