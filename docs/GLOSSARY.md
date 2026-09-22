# Glossary — Krama

Append-only. One row per term, defined **once**, with the part that introduced it.

This file exists because 168 days is long enough that day 3 is forgotten by day 66. Its
real job is not to be read front to back; it is to be **checked before defining anything**, so
that a term is never defined twice, slightly differently, in two places. Two nearly-identical
definitions are worse than one bad definition, because the reader cannot tell which is current.

Before you define a term in a day document, search this file. If it is here, link the part that
introduced it instead of redefining it.

| Term | Plain-language definition | Introduced in | Also called |
| ---- | ------------------------- | ------------- | ----------- |
| Contract | Allowed inputs, required results, and permitted side effects. | [Day 1 DSA](../days/day-001-count-target-values/dsa_count-target-values/CONCEPTS.md) | Input/output contract |
| Loop invariant | A statement that remains true at a specified point in each iteration. | [Day 1 DSA](../days/day-001-count-target-values/dsa_count-target-values/CONCEPTS.md) | Invariant |
| Baseline | A straightforward correct approach used for comparison. | [Day 1 DSA](../days/day-001-count-target-values/dsa_count-target-values/CONCEPTS.md) | Reference approach |
| Auxiliary space | Working memory beyond the supplied input and required output. | [Day 1 DSA](../days/day-001-count-target-values/dsa_count-target-values/CONCEPTS.md) | Extra space |
| Functional requirement | An action and its observable outcome under stated conditions. | [Day 1 SD](../days/day-001-count-target-values/sd_functional-scope/CONCEPTS.md) | Required behavior |
| Exclusion | Behavior the current version deliberately does not promise. | [Day 1 SD](../days/day-001-count-target-values/sd_functional-scope/CONCEPTS.md) | Out of scope |
| Assumption | A statement accepted temporarily for reasoning that still needs confirmation. | [Day 1 SD](../days/day-001-count-target-values/sd_functional-scope/CONCEPTS.md) | Design assumption |
| Success criterion | A measurable condition for deciding whether a stated outcome has been achieved. | [Day 1 SD](../days/day-001-count-target-values/sd_functional-scope/CONCEPTS.md) | Acceptance criterion |
| Identity | Whether references designate the same object. | [Day 1 Python](../days/day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md) | Object identity |
| Equality | Whether values compare equal under their type's comparison rules. | [Day 1 Python](../days/day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md) | Value equality |
| Aliasing | Multiple references reaching the same object. | [Day 1 Python](../days/day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md) | Shared reference |
| Mutation | Changing an existing object's state. | [Day 1 Python](../days/day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md) | In-place change |
| Rebinding | Changing which object a name refers to. | [Day 1 Python](../days/day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md) | Name reassignment |
| Predicate | A condition with a yes/no result that determines whether an item qualifies. | [Day 1 DSA](../days/day-001-count-target-values/dsa_count-target-values/CONCEPTS.md) | Boolean condition |
| Frequency table | A summary retaining how often each value occurs. | [Day 1 DSA](../days/day-001-count-target-values/dsa_count-target-values/FREQUENCY_COUNTS.md) | Histogram |
| Cumulative count | A sum of frequencies across a stated value boundary. | [Day 1 DSA](../days/day-001-count-target-values/dsa_count-target-values/FREQUENCY_COUNTS.md) | Prefix count |
| Stable compaction | Packing retained items into a prefix without changing their relative order. | [Day 3 DSA](../days/day-003-stable-compaction/dsa_stable-compaction/CONCEPTS.md) | Stable filtering |
| Closed interval | A range including both endpoints; indices L through R contain R−L+1 positions. | [Day 4 DSA](../days/day-004-reverse-a-segment/dsa_reverse-a-segment/CONCEPTS.md) | Inclusive interval |
| Shallow copy | A new outer container holding references to the original children. | [Day 2 Python](../days/day-002-find-the-first-maximum/lang_shallow-and-deep-copies/CONCEPTS.md) | Outer copy |
| Hash collision | Different keys producing the same hash value; equality still distinguishes them. | [Day 4 Python](../days/day-004-reverse-a-segment/lang_hash-and-equality/CONCEPTS.md) | Collision |
| SLI | A measured service-quality indicator with a defined population and boundary. | [Day 2 SD](../days/day-002-find-the-first-maximum/sd_quality-requirements/CONCEPTS.md) | Service level indicator |
| SLO | A target for a service level indicator. | [Day 2 SD](../days/day-002-find-the-first-maximum/sd_quality-requirements/CONCEPTS.md) | Service level objective |
| QPS | Queries or requests per second at a named service boundary. | [Day 3 SD](../days/day-003-stable-compaction/sd_traffic-estimates/CONCEPTS.md) | Request rate |
| Retention | How long records remain stored. | [Day 4 SD](../days/day-004-reverse-a-segment/sd_storage-estimates/CONCEPTS.md) | Retention period |
| Replication factor | The total count of live copies, including the original. | [Day 4 SD](../days/day-004-reverse-a-segment/sd_storage-estimates/CONCEPTS.md) | Total copies |
| Headroom | Spare provisioned capacity for operations and growth. | [Day 4 SD](../days/day-004-reverse-a-segment/sd_storage-estimates/CONCEPTS.md) | Capacity reserve |
| Nondecreasing order | Each value is at least the preceding value; equal neighbors are allowed. | [Day 5 DSA](../days/day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/CONCEPTS.md) | Ascending order with ties |
| Logical length | The number of meaningful entries, excluding spare capacity. | [Day 5 DSA](../days/day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/BACKWARD_MERGE.md) | Valid length |
| Latency budget | An allocation of an end-to-end time target among request-path components. | [Day 5 SD](../days/day-005-merge-sorted-arrays/sd_latency-budgets/CONCEPTS.md) | Time allocation |
| Critical path | The dependency path that determines when a response can finish. | [Day 5 SD](../days/day-005-merge-sorted-arrays/sd_latency-budgets/CONCEPTS.md) | Completion path |
| Sentinel | A distinguished object representing a state such as an omitted value. | [Day 5 Python](../days/day-005-merge-sorted-arrays/lang_truth-and-sentinels/CONCEPTS.md) | Absence marker |
| Frequency bucket | A collection of values sharing one occurrence count. | [Day 9 DSA](../days/day-009-frequency-ranking/dsa_frequency-ranking/CONCEPTS.md) | Count bucket |
| Closure | A function retaining access to bindings from an enclosing function scope. | [Day 9 Python](../days/day-009-frequency-ranking/lang_closure-binding/CONCEPTS.md) | Enclosing state |
| Free variable | A name used inside a function but bound outside its local scope. | [Day 9 Python](../days/day-009-frequency-ranking/lang_closure-binding/CONCEPTS.md) | Nonlocal reference |
| Safe method | An HTTP method whose requested semantics do not ask for a state change. | [Day 9 SD](../days/day-009-frequency-ranking/sd_http-methods/CONCEPTS.md) | Read semantics |
| Idempotency | Repetition having the same intended effect as one operation. | [Day 9 SD](../days/day-009-frequency-ranking/sd_http-methods/CONCEPTS.md) | Repeat-effect semantics |
| Complement | The other value required to satisfy a target equation. | [Day 10 DSA](../days/day-010-pair-sum-indices/dsa_pair-sum-indices/CONCEPTS.md) | Needed partner |
| Lexicographic order | Compare the first unequal corresponding components; an equal proper prefix sorts first. | [Day 10 DSA](../days/day-010-pair-sum-indices/dsa_pair-sum-indices/CONCEPTS.md) | Dictionary order |
| Nonlocal rebinding | Assigning an existing binding in the nearest applicable enclosing function scope. | [Day 10 Python](../days/day-010-pair-sum-indices/lang_nonlocal-state/CONCEPTS.md) | nonlocal |
| Replay record | Stored operation identity, request, and result used to answer matching retries. | [Day 10 SD](../days/day-010-pair-sum-indices/sd_idempotency-semantics/CONCEPTS.md) | Deduplication record |
| Canonical key | A common representation equal exactly for items considered equivalent. | [Day 11 DSA](../days/day-011-group-anagrams/dsa_group-anagrams/CONCEPTS.md) | Canonical representation |
| Decorator | A callable that receives a function and returns its replacement at definition time. | [Day 11 Python](../days/day-011-group-anagrams/lang_decorator-metadata/CONCEPTS.md) | Function decorator |
| Connection pool | A bounded collection of reusable connections with a checkout policy. | [Day 11 SD](../days/day-011-group-anagrams/sd_connection-budgets/CONCEPTS.md) | Resource pool |
| Prefix sum | A total over an initial segment, with its boundary convention stated explicitly. | [Day 12 DSA](../days/day-012-range-sums/dsa_range-sums/CONCEPTS.md) | Cumulative sum |
| Decorator factory | A callable accepting configuration and returning a decorator. | [Day 12 Python](../days/day-012-range-sums/lang_decorator-arguments/CONCEPTS.md) | Configurable decorator |
| Deadline | The point after which an operation's result is no longer timely. | [Day 12 SD](../days/day-012-range-sums/sd_timeout-propagation/CONCEPTS.md) | Request expiry |
| Cancellation | A cooperative signal to stop work whose result is no longer wanted. | [Day 12 SD](../days/day-012-range-sums/sd_timeout-propagation/CONCEPTS.md) | Stop request |

## Days 13–16 additions

| Term | Meaning | Introduction | Related phrase |
| --- | --- | --- | --- |
| Prefix frequency | The number of earlier prefix boundaries with a given cumulative total. | [Day 13 dsa](../days/day-013-count-target-subarrays/dsa_count-target-subarrays/CONCEPTS.md) | Multiplicity of boundaries |
| Partial application | A callable specialized by storing some arguments for later invocation. | [Day 13 lang](../days/day-013-count-target-subarrays/lang_partial-application/CONCEPTS.md) | functools.partial |
| Cursor pagination | Continuing a listing from an ordered boundary rather than a row offset. | [Day 13 sd](../days/day-013-count-target-subarrays/sd_pagination/CONCEPTS.md) | Keyset continuation |
| Two-pointer elimination | Discarding an endpoint after proving it cannot participate in a remaining answer. | [Day 15 dsa](../days/day-015-sorted-pair-existence/dsa_sorted-pair-existence/CONCEPTS.md) | Sorted pair scan |
| Iterator | A traversal object returning itself from iter and producing values until permanent exhaustion. | [Day 15 lang](../days/day-015-sorted-pair-existence/lang_iterator-protocol/CONCEPTS.md) | Consumable cursor |
| Entity identity | A stable key distinguishing one domain object from another despite equal or changed attributes. | [Day 15 sd](../days/day-015-sorted-pair-existence/sd_domain-model/CONCEPTS.md) | Domain key |
| Generator suspension | Preserving a generator frame at yield until the next advancement. | [Day 16 lang](../days/day-016-unique-triples/lang_generator-laziness/CONCEPTS.md) | Lazy resumption |
| API contract | The declared accepted inputs, observable outcomes, errors, and semantics of an interface. | [Day 16 sd](../days/day-016-unique-triples/sd_api-contract/CONCEPTS.md) | Request/response agreement |

## Days 17–20 additions

| Term | Meaning | Introduction | Related phrase |
| --- | --- | --- | --- |
| Stateless worker | A replaceable process whose local state is not authoritative for later requests. | [Day 17 sd](../days/day-017-container-capacity/sd_stateless-workers/CONCEPTS.md) | External state |
| Generator closure | Explicitly ending a suspended generator and unwinding entered cleanup scopes. | [Day 17 lang](../days/day-017-container-capacity/lang_generator-cleanup/CONCEPTS.md) | close |
| Sliding window | A contiguous range whose boundaries advance while its summary is maintained. | [Day 18 dsa](../days/day-018-fixed-window-maximum-sum/dsa_fixed-window-maximum-sum/CONCEPTS.md) | Moving interval |
| Yield delegation | Forwarding a child iterator through yield from and capturing its terminal return value. | [Day 18 lang](../days/day-018-fixed-window-maximum-sum/lang_yield-delegation/CONCEPTS.md) | Subgenerator delegation |
| Durable handoff | Acceptance of work by storage that survives the stated producer failure model. | [Day 18 sd](../days/day-018-fixed-window-maximum-sum/sd_sync-versus-async/CONCEPTS.md) | Persistent enqueue |
| Tolerant reader | A response consumer that reads required fields while permitting documented unknown additions. | [Day 19 sd](../days/day-019-longest-distinct-substring/sd_compatibility/CONCEPTS.md) | Additive response compatibility |
| Pull pipeline | Composed stages whose upstream advancement is driven by downstream requests. | [Day 20 lang](../days/day-020-minimum-positive-window/lang_streaming-pipeline/CONCEPTS.md) | Demand-driven iteration |
| Modular monolith | One deployable application with explicit internal module interfaces and data ownership. | [Day 20 sd](../days/day-020-minimum-positive-window/sd_modular-monolith/CONCEPTS.md) | Internal service boundaries |
