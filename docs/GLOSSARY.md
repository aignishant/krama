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
