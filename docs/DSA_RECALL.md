# DSA — quick recall

Use this file to refresh topics you have already studied, without opening a problem, writing
code, or running tests. Read the matching day card and stop when the idea is familiar again.
The linked lesson is available only if you want more explanation.

Cards describe authored lessons, not completed study. Use the latest event for each DSA day in
[track progress](TRACK_PROGRESS.csv) to select completed topics; missing entries mean completion
has not been recorded. Day 001 is the first available card. New cards are added as future days
are taught; this is not a summary of all 168 planned days.

## Index

| Day | Topic | Jump |
| --- | --- | --- |
| 001 | Counting, invariants, frequencies, and cumulative counts | [Recall card](#day-001-counting-and-reusing-counts) |

## Day 001: Counting and reusing counts

**Core idea:** retain only the information needed by the answer. Counting turns each predicate
result into a contribution: yes adds 1; no adds 0. Repeated values remain separate occurrences.

**Why it works:** after k items, the counter equals the number qualifying among those k items.
It starts at zero, survives both match and non-match updates, and becomes the full answer when
all items have been processed. The proof is initialization → maintenance → termination.

| Situation | Mechanism | Cost under the unit-cost model |
| --- | --- | --- |
| One exact count query | Scan, updating one counter | O(n) time, O(1) auxiliary space |
| q independent queries, direct baseline | Rescan for each query | O(nq) time, O(1) auxiliary space excluding output |
| Many queries over U small integer values | Build frequencies and cumulative counts | O(n + U + q) time, O(U) auxiliary space excluding output |

**The insight behind the optimization:** equal query values need the same answer. A frequency
table retains multiplicity once. `below[v]` totals frequencies strictly before v; save the
running total before adding the current bucket. This reuses computation across queries.

**Tiny memory anchor:** for `[3, 1, 3, 0, 5]`, exactly two occurrences are below 3: 1 and 0.
The two 3s contribute nothing to a strict-lower query about 3. Looking up answers using the
original input order preserves the relationship between each position and its result.

**Common mistakes:** reset the count on a non-match; return after the first match; remove
duplicates with a set; include the current bucket in a strict comparison; confuse sorted order
with required output order. A frequency table needs a suitable domain and must reflect current data.

**Distinction to keep:** “equal to one target” returns one count; “smaller than each value”
returns a count per position. The latter has O(n) output space. O(U) is small only when U is small.

[Full scan explanation](../days/day-001-count-target-values/dsa_count-target-values/CONCEPTS.md) ·
[Reusing counts](../days/day-001-count-target-values/dsa_count-target-values/FREQUENCY_COUNTS.md) ·
[Your Day 1 notes](../days/day-001-count-target-values/dsa_count-target-values/NOTES.md)

---

[Python recall](LANG_RECALL.md) · [System design recall](SD_RECALL.md) · [Study workflow](STUDY_WORKFLOW.md)
