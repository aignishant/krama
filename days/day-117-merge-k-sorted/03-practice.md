---
day: 117
track: practice
title: "Practice — Merging K sorted lists"
status: written
---

# Day 117 · Practice

**DSA topic:** Merging K sorted lists
**System design topic:** Quorums: why R plus W must exceed N

---

## Code these, in this order

One rule for the whole set: **say the invariant before writing** — *each list is sorted, so the overall
smallest must be at the front of some list, and the heap holds all `k` fronts.* That sentence is the
correctness proof and it takes ten seconds.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Merge Two Sorted Lists | LeetCode 21 (Easy) | The primitive the tournament is built from. |
| 2 | Merge k Sorted Lists | LeetCode 23 (Hard) | The heap of `k` fronts, and both `O(n log k)` solutions. |
| 3 | Kth Smallest Element in a Sorted Matrix | LeetCode 378 (Medium) | A k-way merge that stops after `k` pops. |
| 4 | Smallest Range Covering Elements from K Lists | LeetCode 632 (Hard) | The same heap plus one extra variable. |

### On problem 2, write all four approaches

Heap, tournament, sequential pairwise, and concatenate-and-sort. Time all four at n = 100,000 with k = 100.
Record four numbers and say which two are `O(n log k)`.

### On problem 2 again, break the tuple

Push `(node.val, node)` with two nodes of equal value and record the exact `TypeError`. Then say what the
natural tie-breaker is here and why it is free.

### On problem 3, notice what changes

Say what makes this a k-way merge, what `k` is, and why stopping after `k` pops changes the complexity from
`O(n log rows)` to `O(k log rows)`.

### On problem 4, say what you added

Compare it line by line with problem 2. Say exactly which variable is new and why advancing the minimum is
the only move that can shrink the range.

---

### The invariant drill

1. State the invariant in one sentence.
2. Give the one-sentence proof.
3. Say what would break it if a list were not sorted.
4. Say why this makes the heap size `k` rather than `n`.

### The complexity drill

1. Derive `O(n log k)` from the pops and the heap size.
2. Compute the comparison counts at n = 1,000,000 for k = 2, 10, 100 and 10,000.
3. Say at what `k` the heap stops being worth it, and what to do instead.
4. State the space complexity and say why it is the more important number.

### The four-approaches drill

1. Name all four and give time, space, streaming and whether each uses the sortedness.
2. Identify the two at `O(n log k)`.
3. Say which one is the trap and why it looks correct.
4. Say which one throws away the only interesting property of the input.

### The tournament drill

1. Describe it in two sentences.
2. Say why it is `O(n log k)`, in terms of rounds and work per round.
3. Give three advantages over the heap.
4. Give its disadvantage, and the input type that removes it.
5. Say when you would choose it.

### The tuple drill

1. Write the heap entry from memory and name all three fields.
2. Say what each field is for.
3. Say which field doubles as the tie-breaker and why it is always safe here.
4. Construct the `TypeError` you get without it.

### The external-sort drill

1. Describe both passes of an external merge sort.
2. Say which pass is today's algorithm.
3. Say what is held in memory during that pass.
4. Say why merge is the disk world's sort and quicksort is memory's.
5. Name two production systems that do this.

### The break-it drill

Trigger each and record the exact output or error:

1. A heap containing all `n` items instead of `k`.
2. No `if lst` guard when building the initial heap, with `[[], [1,2]]`.
3. `(node.val, node)` with two equal values.
4. Advancing list 0 instead of the list the value came from.
5. Pushing without the bound check when a list is exhausted.
6. Sequential pairwise merging, timed at k = 100.
7. Returning a list rather than yielding, on input larger than memory.

---

### The inequality drill

1. State the rule and give the one-sentence pigeonhole proof.
2. For `N = 5`, list every `(W, R)` pair that satisfies it with `W + R = N + 1`.
3. Compute the overlap size formula and apply it to two configurations.
4. Construct a concrete miss for `N = 5, W = 2, R = 2`.

### The versioning drill

1. Say why the overlap is useless without versions.
2. Compare timestamps against vector clocks on three axes.
3. Say what last-write-wins does under clock skew.
4. Say which question is more consequential than choosing `R` and `W`.

### The configuration drill

1. Give the default for `N = 3` and for `N = 5`.
2. Give a read-heavy configuration and a write-heavy one.
3. Say what `W = 1, R = 1` gives you and what it gives up.
4. Say why even values of `N` buy nothing.

### The availability drill

Compute, at 99.9% per replica:

1. `N=3, W=1`, `N=3, W=2`, `N=3, W=3`, `N=5, W=3`.
2. The ratio between `W=2` and `W=3` for `N=3`.
3. Say which configuration is worse than a single machine, and by how much.

### The latency drill

1. Given replica responses of 2, 3, 5, 40 and 200 ms, give the latency for `W = 1` through `W = 5`.
2. State the general rule in one sentence.
3. Say why this is the underrated reason quorums exist.
4. Compute the cross-region cost and name the setting that avoids it.

### The not-linearizable drill

1. State what `R + W > N` actually guarantees.
2. Describe all three holes with a concrete scenario each.
3. Say what you need instead for a genuine total order.
4. Name the Cassandra feature that provides it and its cost.

### The sloppy-quorum drill

1. Define strict and sloppy.
2. Say what sloppy gains and what it suspends.
3. Say which systems default to it and why.
4. Say when the guarantee is restored.

### The healing drill

1. Name all three mechanisms.
2. For each, say what triggers it and which keys it reaches.
3. Say which one fixes cold keys and why nothing else does.
4. Say what the trust register's equivalent of read repair was.

### The failure drill

For each, say what happens and what you would configure:

1. One of five replicas is permanently slow but not down.
2. A client writes to two of three replicas and then crashes.
3. Two clients write different values to overlapping quorums simultaneously.
4. A read repairs A and B; the next read touches C, D and E.
5. Two of three replicas acknowledging a write are in the same rack, which loses power.
6. A global quorum is configured across two regions.

Two of the six are not fixed by adjusting `R` and `W`. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Merge k sorted lists efficiently.*
   The invariant stated as the proof, the heap holding `k` and not `n` with the complexity derived from it,
   the tuple's three fields with the free tie-breaker, the tournament offered as the second `O(n log k)`,
   the sequential trap named, and external sorting as the real use.

2. *You have five replicas. What R and W would you pick?*
   Three and three with the pigeonhole proof, versioning named as the necessary second half, `W = N`
   rejected with the availability arithmetic, the tail-latency argument, and the admission that a quorum is
   not linearizability.

3. *Is a quorum linearizable?*
   No, what it actually guarantees, all three holes with a scenario each, and what you need instead.

---

## Before you move on

- [ ] I can state the merge invariant and its one-sentence proof.
- [ ] I can derive `O(n log k)` from the heap size.
- [ ] I know why `O(k)` space matters more than the time bound.
- [ ] I can name all four approaches and identify the trap.
- [ ] I can describe the tournament and say when I would choose it.
- [ ] I write the three-field tuple by habit and know why the index is a free tie-breaker.
- [ ] I skip empty lists when building the initial heap.
- [ ] I can describe both passes of an external merge sort.
- [ ] I can adapt the merge to smallest-range and to a sorted matrix.
- [ ] I can state `R + W > N` and give the pigeonhole proof.
- [ ] I can construct a concrete miss when the inequality fails.
- [ ] I always mention versioning as the necessary second half.
- [ ] I can compute availability for four configurations and spot the one worse than a single machine.
- [ ] I can give the tail-latency argument with numbers.
- [ ] I know that a quorum is not linearizability, and all three reasons.
- [ ] I can define a sloppy quorum and say what it suspends.
- [ ] I can name all three healing mechanisms and which keys each reaches.
- [ ] I know what `LOCAL_QUORUM` is for and what it costs.
- [ ] I answered all three questions above out loud.
