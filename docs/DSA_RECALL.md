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
| 006 | Best single trade | [Recall card](#day-006-best-single-trade) |
| 007 | Week 1 DSA review | [Recall card](#day-007-week-1-dsa-review) |
| 008 | First repeated value | [Recall card](#day-008-first-repeated-value) |
| 009 | Frequency ranking | [Recall card](#day-009-frequency-ranking) |
| 010 | Pair sum indices | [Recall card](#day-010-pair-sum-indices) |
| 011 | Group anagrams | [Recall card](#day-011-group-anagrams) |
| 012 | Range sums | [Recall card](#day-012-range-sums) |
| 013 | Count target subarrays | [Recall card](#day-013-count-target-subarrays) |
| 014 | Week 2 DSA review | [Recall card](#day-014-week-2-dsa-review) |
| 015 | Sorted pair existence | [Recall card](#day-015-sorted-pair-existence) |
| 016 | Unique triples | [Recall card](#day-016-unique-triples) |

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

## Day 006: Best single trade

**Cue and mechanism:** combine today's sale with an earlier purchase. Keep the cheapest
strictly earlier price and the best completed nonnegative profit. Consider today's sale before
making its price eligible for future purchases.

**Why it works:** for a fixed sale, the cheapest eligible purchase dominates every more
expensive one. Examining all sales covers every possible ending day. Zero includes no trade.
O(n) time, O(1) auxiliary and output space without copying a suffix.

**Memory anchor:** `[9, 2, 5]` yields 3; global maximum minus minimum yields an impossible 7.
Sorting destroys chronology. Multiple trades need a different contract and state. Empty and
single-element local inputs have no eligible pair; the online input is nonempty.

[Full lesson](../days/day-006-best-single-trade/dsa_best-single-trade/CONCEPTS.md) ·
[Your notes](../days/day-006-best-single-trade/dsa_best-single-trade/NOTES.md)

## Day 007: Week 1 DSA review

**Cue and mechanism:** when a remembered loop is hard to explain, reconstruct its state
meaning, initialization, preservation, and termination. Test properties that cover the whole
contract: ordering, multiplicity, boundaries, ownership, and eligibility as appropriate.

**Why it works:** an invariant explains every update; a counterexample distinguishes a plausible
wrong implementation. Independent tiny-input oracles cost extra time but reduce shared mistakes.
Counting needs O(n) time and constant state; new-output merge needs O(n+m) time and output space.

**Memory anchor:** deduplicated `[1, 3, 4]` is sorted but fails to merge `[1, 4]` with `[1, 3]`.
A passing weak assertion is not proof. Online counting and backward merging have different
contracts from the local exercises. This card is optional recall, not the two-solve cold gate.

[Repair lesson](../days/day-007-week-1-review/dsa_week-1-dsa-review/CONCEPTS.md) ·
[Your notes](../days/day-007-week-1-review/dsa_week-1-dsa-review/NOTES.md)

## Day 008: First repeated value

**Cue and mechanism:** exact “seen before” queries need retained membership. Before each
item, the set contains exactly the distinct earlier values. Check membership before insertion;
the first hit identifies the earliest second occurrence.

**Why it works:** an earlier repeat would already have stopped the scan. The set can discard
counts and order because scanning supplies encounter order. For fixed-size integers, expected
O(n) time and O(n) worst-case auxiliary space; collisions can degrade time. Output is O(1).

**Memory anchor:** `[7, 2, 2, 7]` returns 2, not 7. Repeated zero is a valid answer, distinct
from `None`. Online Contains Duplicate asks only for a Boolean. Sorting changes local order;
an unbounded exact history consumes growing memory. Hashability and equality define the key domain.

[Full lesson](../days/day-008-first-repeated-value/dsa_first-repeated-value/CONCEPTS.md) ·
[Your notes](../days/day-008-first-repeated-value/dsa_first-repeated-value/NOTES.md)

## Day 009: Frequency ranking

**Cue and mechanism:** Frequency questions need counts, then a separate ordering step. Count each value once and sort distinct values by (-count, value).

**Why it works and cost:** The count table represents the processed prefix; tuple keys implement both ranking priorities. Expected O(n + u log u) time and O(u) auxiliary space for u distinct values. Online frequency buckets use O(n) auxiliary space to avoid comparison sorting.

**Memory anchor and trap:** Counts {8: 2, 2: 3, 5: 2} rank as [2, 5, 8]. Sorting only by count leaves ties dependent on arrival order. Online top-k is a different output contract.

[Full lesson](../days/day-009-frequency-ranking/dsa_frequency-ranking/CONCEPTS.md) ·
[Your notes](../days/day-009-frequency-ranking/dsa_frequency-ranking/NOTES.md)

## Day 010: Pair sum indices

**Cue and mechanism:** When the current value determines its partner, look up target minus value among earlier entries. Save earliest indices and compare complete candidate pairs.

**Why it works and cost:** The earliest partner dominates later equal-valued partners for a fixed right index. Comparing all candidates yields the local smallest pair. Expected O(n) time, O(u) auxiliary space, O(1) output.

**Memory anchor and trap:** [4, 1, 5, 2], target 6 finds [1, 2] before the better [0, 3]. Check before inserting to avoid self-pairs. Index zero is valid, so do not use truthiness for presence.

[Full lesson](../days/day-010-pair-sum-indices/dsa_pair-sum-indices/CONCEPTS.md) ·
[Your notes](../days/day-010-pair-sum-indices/dsa_pair-sum-indices/NOTES.md)

## Day 011: Group anagrams

**Cue and mechanism:** Equivalent words need equal canonical keys. Sorted characters retain every letter occurrence; map each key to its original words.

**Why it works and cost:** Equal sorted keys hold exactly for equal letter multiplicities. Key construction costs O(S log(max(2,L))) in the stated upper bound, with O(S+n) key/reference storage. Local within-group and outer sorting add string comparison costs.

**Memory anchor and trap:** abb and bab share a key; ab must not join them. A set loses counts, and a raw hash is not a unique key. Preserve duplicate words; local output order is stricter than online.

[Full lesson](../days/day-011-group-anagrams/dsa_group-anagrams/CONCEPTS.md) ·
[Your notes](../days/day-011-group-anagrams/dsa_group-anagrams/NOTES.md)

## Day 012: Range sums

**Cue and mechanism:** Many queries on unchanged data suggest reusable boundary totals. P[t] sums the first t values; inclusive [l,r] is P[r+1] - P[l].

**Why it works and cost:** Subtracting cancels exactly the shared prefix. Build in O(n), answer each query in O(1): O(n+q) total time, O(n) auxiliary space, and O(q) local output.

**Memory anchor and trap:** [3, -2, 6, 1] has boundaries [0, 3, 1, 7, 8]; [1,2] gives 7-3=4. P[r]-P[l] drops the endpoint. Negative values work; mutations make later totals stale.

[Full lesson](../days/day-012-range-sums/dsa_range-sums/CONCEPTS.md) ·
[Your notes](../days/day-012-range-sums/dsa_range-sums/NOTES.md)

## Day 013: Count target subarrays

**Cue and mechanism:** Count target sums with signed values by looking up earlier prefix frequencies.

**Why it works and cost:** P[r]-P[l]=k becomes P[l]=P[r]-k. Each earlier boundary gives one interval; expected O(n) time and O(n) storage.

**Memory anchor and trap:** Seed zero once, query before inserting. Two zeros have three zero-sum intervals; a set loses multiplicity.

[Full lesson](../days/day-013-count-target-subarrays/dsa_count-target-subarrays/CONCEPTS.md) ·
[Your notes](../days/day-013-count-target-subarrays/dsa_count-target-subarrays/NOTES.md)

## Day 014: Week 2 DSA review

**Cue and mechanism:** Review which information the exact answer needs: membership, count, position, canonical key, or prefix boundary.

**Why it works and cost:** State meaning and update order prove correctness. Duplicate detection is expected O(n); batch range queries are O(n+q), with O(n) auxiliary space.

**Memory anchor and trap:** A boolean duplicate result is not the first repeated value. P[right+1]-P[left] includes both endpoints. Read this after the cold attempts.

[Full lesson](../days/day-014-week-2-review/dsa_week-2-dsa-review/CONCEPTS.md) ·
[Your notes](../days/day-014-week-2-review/dsa_week-2-dsa-review/NOTES.md)

## Day 015: Sorted pair existence

**Cue and mechanism:** For sorted pair existence, inspect endpoint sums and eliminate an impossible endpoint.

**Why it works and cost:** Too small rules out left with every available partner; too large rules out right. At most n-1 moves give O(n) time, O(1) auxiliary space.

**Memory anchor and trap:** Use left < right: [5] cannot make 10, but [5,5] can. Unsorted input invalidates the elimination proof.

[Full lesson](../days/day-015-sorted-pair-existence/dsa_sorted-pair-existence/CONCEPTS.md) ·
[Your notes](../days/day-015-sorted-pair-existence/dsa_sorted-pair-existence/NOTES.md)

## Day 016: Unique triples

**Cue and mechanism:** For unique triples, sort, fix a distinct first value, and search a suffix using two pointers.

**Why it works and cost:** Sorted elimination finds all suffix pairs; skipping repeated matched values removes duplicate answers. O(n²) time, Python sorting up to O(n) workspace, plus output.

**Memory anchor and trap:** [-1,-1,2] needs both -1 occurrences. Deduplicate answers, not the input; report output ordering and memory.

[Full lesson](../days/day-016-unique-triples/dsa_unique-triples/CONCEPTS.md) ·
[Your notes](../days/day-016-unique-triples/dsa_unique-triples/NOTES.md)


---

[Python recall](LANG_RECALL.md) · [System design recall](SD_RECALL.md) · [Study workflow](STUDY_WORKFLOW.md)
