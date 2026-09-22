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
