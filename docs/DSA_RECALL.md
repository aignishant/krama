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
| 002 | First maximum and dominance | [Recall card](#day-002-first-maximum-and-dominance) |
| 003 | Stable compaction | [Recall card](#day-003-stable-compaction) |
| 004 | Reverse a segment | [Recall card](#day-004-reverse-a-segment) |
| 005 | Merge sorted arrays | [Recall card](#day-005-merge-sorted-arrays) |

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

## Day 002: First maximum and dominance

**Idea and cue:** when one best position is needed, retain a candidate index instead of sorting.
Initialize from a real element after handling empty input. Replace only on a strict improvement
to preserve the earliest tie. Zero is not a safe initial best value for arbitrary integers.

**Why it works:** the candidate is the earliest maximum of the processed prefix. Larger values
replace it; equal or smaller values cannot improve that answer. After the scan the prefix is
the whole input. O(n) time, O(1) auxiliary space, constant output space.

**Memory anchor:** `[4, 9, 6, 9]` keeps index 1. Changing `>` to `>=` instead keeps index 3.

**Online variation:** finding the largest does not prove it doubles every competitor. Verify
all other indices in a second pass, or retain the second-largest value. Two linear passes are
still O(n). `[1, 10, 5]` passes dominance; `[1, 10, 6]` fails.

**Trap and tradeoff:** don't compare a candidate with itself or discard the tie policy.
Two-largest state saves a pass but adds proof obligations; it does not improve the time class.
The online problem assumes a unique maximum; local practice permits ties and empty input.

[Full lesson](../days/day-002-find-the-first-maximum/dsa_find-the-first-maximum/CONCEPTS.md) ·
[Dominance](../days/day-002-find-the-first-maximum/dsa_find-the-first-maximum/DOMINANCE.md) ·
[Your notes](../days/day-002-find-the-first-maximum/dsa_find-the-first-maximum/NOTES.md)

## Day 003: Stable compaction

**Idea and cue:** filter inside an existing array while preserving retained items' order.
Read examines each position; write names the next slot in the retained prefix. Retain an item
by placing it at write and advancing write. Fill the stale tail with the required marker afterwards.

**Why it works:** the valid prefix is exactly the retained part of the already-read input,
in order. Since write never exceeds read, a write cannot destroy unread future data.
One read pass plus tail cleanup costs O(n) time and O(1) auxiliary space.

**Memory anchor:** `[0, 4, 0, 2]` becomes `[4, 2, 0, 0]`. The prefix is meaningful before the
tail is. An end-swap can put 2 before 4 and violate stability.

**Trap and tradeoff:** negative numbers are retained too; forgetting tail cleanup leaves stale
values. A separate output list is simpler but uses O(n) storage. Returning an equal new list
does not fulfill a mutation contract. Check order, identity, and length independently.

[Full lesson](../days/day-003-stable-compaction/dsa_stable-compaction/CONCEPTS.md) ·
[Your notes](../days/day-003-stable-compaction/dsa_stable-compaction/NOTES.md)

## Day 004: Reverse a segment

**Idea and cue:** reversal pairs original position i with L+R−i in an inclusive interval.
Swap the working endpoints and move inward. Everything finalized outside those pointers is
already correct; everything outside the original interval stays unchanged.

**Why it works:** every swap puts two mirrored values in their final positions. The unfinished
interval shrinks by two. Stop when the pointers meet or cross; an odd middle item maps to itself.
For k=R−L+1, floor(k/2) swaps use O(k) time and O(1) extra space.

**Memory anchor:** reverse indices 1..3 of `[X, A, B, C, Y]` to get `[X, C, B, A, Y]`.

**Trap and tradeoff:** sequential overwrites lose a value; save it or use a proper swap.
Swapping every mirrored pair twice undoes the result. A reversed slice uses O(k) memory.
Reversing twice is a useful extra property, but a no-op also passes it, so check expected output.
The local task requires a valid nonempty range; online practice reverses the whole character array.

[Full lesson](../days/day-004-reverse-a-segment/dsa_reverse-a-segment/CONCEPTS.md) ·
[Your notes](../days/day-004-reverse-a-segment/dsa_reverse-a-segment/NOTES.md)

---

## Day 005: Merge sorted arrays

**Idea and cue:** two inputs already ordered by the same key expose their smallest remaining
values at their heads. Compare those heads, emit one occurrence, and advance only its source.
Once one side ends, emit the remaining tail of the other side.

**Why it works:** each head bounds its own suffix, so the smaller head is smallest overall.
The output stays sorted and contains exactly the consumed prefixes. Equal heads represent two
occurrences; neither may disappear. Take from the first input on ties for a stable forward merge.

**Memory anchor:** `[2, 8]` and `[3]` produce `[2, 3]` before cleanup; the remaining 8 must follow.
O(n+m) time, O(1) auxiliary state excluding the required O(n+m) new output. Temporary slices
add storage; repeated front deletion can add quadratic shifting work.

**Online variation:** when the destination has spare tail capacity, choose the larger unread
tail and fill backward. With i and j naming unread tails, destination k=i+j+1 lies beyond i
while incoming items remain. This protects unread destination data. Leave the destination
prefix alone if incoming data ends first; copy remaining incoming data if the other side ends.

**Trap and tradeoff:** logical lengths distinguish valid zeros from placeholders. Online,
mutate the destination; locally, return a new list, including when one input is empty. A new
output simplifies ownership but costs space. Backward merging saves allocation only under
the promised buffer-capacity and non-overlap assumptions.

[Full lesson](../days/day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/CONCEPTS.md) ·
[Backward merging](../days/day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/BACKWARD_MERGE.md) ·
[Your notes](../days/day-005-merge-sorted-arrays/dsa_merge-sorted-arrays/NOTES.md)

---

[Python recall](LANG_RECALL.md) · [System design recall](SD_RECALL.md) · [Study workflow](STUDY_WORKFLOW.md)
