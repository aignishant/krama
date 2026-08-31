---
day: 51
track: practice
title: "Practice — Why sorting matters more than any single sorting algorithm"
status: written
---

# Day 051 · Practice

**DSA topic:** Why sorting matters more than any single sorting algorithm
**System design topic:** Modelling a real domain

---

## Code these, in this order

One rule for the whole set: **before writing anything, say out loud whether sorting helps, which of
the four payoffs you want, and what the cost becomes.** On one of these four the answer is no, and
spotting which is the point.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Minimum Absolute Difference | LeetCode 1200 (Easy) | The purest form: closest-in-value becomes adjacent-after-sorting. |
| 2 | Merge Intervals | LeetCode 56 (Medium) | That the sort *is* the algorithm, and which field you sort on. |
| 3 | 3Sum | LeetCode 15 (Medium) | One sort buying two things — the two-pointer sweep and easy duplicate skipping. |
| 4 | Two Sum | LeetCode 1 (Easy) | The trap: sorting is slower here *and* destroys the answer. |

### On problem 1, say the proof before the code

*If two values are the closest pair, nothing lies between them in value — so after sorting, nothing
lies between them in position either.* Then two lines. Then state the cost both ways: n(n−1)/2 against
n log n + n, and the ratio at a million.

### On problem 2, get the key right and prove it matters

Sort by **start**, then one pass. Then deliberately sort by `iv[1]` instead and run it on
`[[1, 4], [0, 2], [3, 5]]` — you get a plausible wrong answer with no error. Say the difference: merge
by start, pack the most non-overlapping meetings by end. When the sort is the algorithm, the key is
the algorithm.

### On problem 3, notice the sort is doing two jobs

Write it, then find both payoffs in your own code: the two-pointer sweep needs order, and the
duplicate-skipping `while` loops need equal values to be adjacent. Say "one sort, two payoffs" out
loud — that is why the O(n log n) is almost never the thing you regret.

### On problem 4, write the wrong version first

Write the sort-plus-two-pointers version. Run it on `[3, 2, 4]` with target 6 and read the answer:
`[0, 2]`, which are positions in the *sorted* list, not the input. No exception. Then write the
dictionary version, say it is O(n) rather than O(n log n), and say the second reason it is better —
it never had the indices to lose.

### The four-payoffs drill

For each problem, name which of the four things sorting buys — equal-adjacent, near-adjacent, binary
search / early exit, or a correct greedy order:

1. Are there any duplicates?
2. What is the smallest difference between any two values?
3. How many values lie between 10 and 44?
4. Merge overlapping intervals.
5. Group anagrams together.
6. What is the maximum number of non-overlapping meetings?

Two of these have a better non-sorting answer. Name them and say what it is.

### The don't-sort drill

For each, say whether to sort — and if not, what instead, with the cost:

1. Find the ten largest of a million values.
2. Find whether any value appears twice.
3. Find the indices of two values summing to a target.
4. Find the median of a stream that will not fit in memory.
5. Answer a thousand "how many values in [a, b]" queries on a fixed array.
6. Find the two closest values.

### The arithmetic drill

Answer with numbers, in under ten seconds each:

1. Comparisons to sort a million elements.
2. Comparisons to compare every pair of a million elements.
3. The ratio between those two.
4. Operations for the ten largest of a million: full sort, heap, quickselect.
5. The break-even query count for "sort once and binary search" against "scan every time" at
   n = 100,000.

### The Python drill

Say what each does, and which is right for which situation:

1. `nums.sort()` versus `sorted(nums)` — return value, space, and what happens to the caller's list.
2. `key=lambda p: (p.city, -p.age)` — what order, and why the minus sign is needed rather than
   `reverse=True`.
3. Two-pass sorting by city then name — which pass goes first, and what property makes it work.
4. `sorted((value, i) for i, value in enumerate(nums))` — what problem does this solve.
5. `sorted([3, "1", 2])` — paste the exact error.
6. How many times is `key` called for a list of n elements?

### The modelling drill

Set a timer for fifteen minutes and model this out loud, running the six steps in order:

> *A gym sells memberships. A member books classes; each class has a trainer, a room and a capacity. A
> member can cancel up to two hours before a class and the slot goes back on sale. Members on a
> monthly plan can book unlimited classes; members on a ten-class pack lose a credit per booking, and
> a cancellation returns it.*

1. Nouns and verbs, in the gym's words. Then three questions that would change the model.
2. Entities against value objects, with the "would I care which one I got" test applied to at least
   two.
3. The noun that is not in the paragraph. Name it, and say exactly what has nowhere to live without
   it.
4. Three invariants, as sentences.
5. The aggregate roots, and what is referenced by id from outside — with the invariant that justifies
   each boundary.
6. Where the cancellation rule goes, and the one-sentence reason. Then where the credit rule goes, and
   whether it is the same object.

Then answer the extension you know is coming: *"now a class can be booked by a member on behalf of a
guest."* Say what changes and what does not.

### The vocabulary drill

Define each in one sentence, then give one example from the gym model:

1. Entity.
2. Value object.
3. Aggregate root.
4. Repository — and how many you would have for the gym.
5. Domain service — and why it is the last resort.
6. Ubiquitous language.
7. Bounded context — and where one would appear in a gym chain.

### The missing-noun drill

For each requirement, name the class that is not in the sentence, and say what has nowhere to live
without it:

1. "Members borrow books."
2. "A customer books a seat for a show."
3. "A vehicle parks in a spot and pays on exit."
4. "Parcels travel between hubs and each movement is recorded."
5. "Employees claim expenses, which a manager approves."
6. "A patient sees a doctor and is prescribed medicines."

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Would sorting first make this problem easier?*
   The question, the payoff you want, the class arithmetic with real numbers, and the three checks
   that would make the answer no.

2. *Here are the requirements. Model it.*
   The six steps in order on the gym, ending on where one specific rule lives and why. If you reach
   for a service before step three, start again.

3. *You sorted. Justify the extra n log n.*
   Half a trillion against twenty-one million, the class-change test, and the counter-example where
   sorting makes it twenty times worse for the same answer.

---

## Before you move on

- [ ] I said the sort decision out loud before coding on all four problems.
- [ ] I broke Merge Intervals by sorting on the wrong field and can say which key each problem wants.
- [ ] I wrote the sorted Two Sum, read the wrong indices, and can say both reasons the dict is better.
- [ ] I can give the four payoffs and the four times not to sort, unprompted.
- [ ] I can quote the closest-pair arithmetic and the ratio.
- [ ] I ran the gym modelling drill in fifteen minutes, including the missing noun and the aggregate
      boundaries.
- [ ] I can define entity, value object, aggregate root, repository and ubiquitous language in one
      sentence each.
- [ ] I answered all three questions above out loud.
