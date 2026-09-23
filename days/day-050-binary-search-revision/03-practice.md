---
day: 50
track: practice
title: "Practice — Binary search revision and mock round"
status: written
---

# Day 050 · Practice

**DSA topic:** Binary search revision and mock round
**System design topic:** Class diagrams and the UML you will actually draw

---

## Code these, in this order

A mock, so the protocol rules: **twenty-five minutes a problem, standing, talking the whole time,
nothing open — and Yesudas's two seconds first.** Name the chapter and the tell before you solve
anything, and score yourself on the naming separately from the code.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Find First and Last Position of Element in Sorted Array | LeetCode 34 (Medium) | The warm-up: two bounds, and whether find-then-walk still tempts you. |
| 2 | Search in Rotated Sorted Array | LeetCode 33 (Medium) | Discarding on a range, and the `<=` in the sortedness test, cold. |
| 3 | Koko Eating Bananas | LeetCode 875 (Medium) | Whether the answer-space instinct fires without the word "capacity" in it. |
| 4 | Split Array Largest Sum | LeetCode 410 (Hard) | The phase's summit, re-derived a week later, with the DP named and rejected. |

### On problem 1, respect the warm-up

Two template calls, one character apart, and the guard in the right order. If it takes more than ten
minutes, the phase needs re-reading rather than more problems. Then run `[8] * 200000` with target 8
and confirm you did not write a walk.

### On problem 2, say the sentence before the code

*At least one half is properly sorted, because there is exactly one break point and one point cannot
be in two halves.* Then write it. Then run the un-rotated array, the break-at-the-end array, and the
single-element array. A special case for any of those means the real bug is still there.

### On problem 3, notice there is no capacity in sight

The word "capacity" does not appear and the shape is identical. The tell is "the minimum k such that
it can be finished in h hours". Bound it at 1 to `max(piles)` — say why the lower bound is not 0 and
what it raises. Ceiling division: `(pile + k - 1) // k`, checked by hand on `pile = 7, k = 3`.

### On problem 4, name the DP and reject it with numbers

Before writing the search, say: *"there's a dynamic-programming solution at O(n²k) — a thousand
elements and fifty parts is fifty million operations and a fifty-thousand-cell table, against about
thirty thousand operations and three integers here."* Then write the binary search. Then diff it
against your LeetCode 1011 solution from day 046 — if they differ anywhere except the names, one of
them is wrong.

### The two-second drill

Ten phrasings. Name the chapter and the tell in under ten seconds each, out loud, no code:

1. Answer 100,000 range-sum queries on a fixed array.
2. Find the index of a target in a sorted array with duplicates.
3. Find the minimum in an array that was sorted and then rotated.
4. Find any element greater than both its neighbours.
5. Find the smallest divisor such that the sum of the divisions is at most a threshold.
6. Find the largest minimum distance when placing c items in n stalls.
7. Find the median of two sorted arrays.
8. Find the maximum of an unsorted array.
9. Find the smallest k such that exactly k groups can be formed.
10. Find the cube root to six decimal places.

Numbers 1, 8 and 9 are not binary search. Say what each of them is instead, and why.

### The pre-flight drill

Say the five bugs of the phase from memory, each with the input that catches it:

1. The convention blend — which two things must never be mixed, and what are the two symptoms?
2. `hi = mid - 1` — when is it right and when does it throw away the answer?
3. Discarding on one comparison — which day introduced the need for a proof, and what is the input?
4. A range that misses the answer — name two problems where it happens, and the one-line habit that
   catches it.
5. A meaningless `lo` — what does it raise, and what is the general rule?

### The one-loop drill

Write `first_true` from memory, then express each of these as a question passed to it — one line
each, no new loops:

1. The first index whose value is at least the target.
2. The last index holding the target.
3. How many values lie in `[a, b]`.
4. The smallest capacity shipping everything in d days.
5. The largest gap at which c items can still be placed.
6. The minimum of a rotated array.
7. A peak.

### The cost drill

Answer in under five seconds each, with numbers not letters:

1. Comparisons for a plain search at a million.
2. Comparisons for first-and-last at a million.
3. Worst case for a rotated search with duplicates at a million.
4. Operations for a search-on-answer with n = 50,000 and a range of 25 million.
5. Peak versus maximum on an unsorted array of a million.
6. Space, for every tool in the phase.

### The four-minute diagram drill

Set a timer for four minutes and draw the class diagram for a **library** — the model you built on
[day 044](../day-044-first-and-last-occurrence/README.md) — in whatever tool you like, talking the
whole time. Then score it:

- [ ] Six to nine boxes, no more.
- [ ] A multiplicity on every relationship line.
- [ ] Hollow triangle for inheritance, dashed for implements, used consistently.
- [ ] Between a third and a half of the boxes have no fields or methods at all.
- [ ] No getters, no constructors, no `created_at`.
- [ ] Nothing crosses anything: spine down the middle, hierarchies at the sides, interface at an edge.
- [ ] I said a design decision out loud for at least three of the boxes.
- [ ] I said what I left out, unprompted.

Then draw the same thing again in Mermaid and check it renders.

### The wrong-diagram drill

For each request, say which diagram it wants — class, sequence, or neither — and why:

1. "Show me how these fit together."
2. "Walk me through what happens when a book is returned late."
3. "What are your classes?"
4. "How does the fee get calculated, and who calls whom?"
5. "Draw the deployment."

### The symbol drill

From memory, and then check:

1. The five Mermaid arrow forms and what each means.
2. The four multiplicities you actually use.
3. What a filled diamond means, what a hollow one means, and the one sentence you would say instead of
   drawing either.
4. How many boxes are readable from where the interviewer sits, and what you do at fifteen.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Two problems, no hints, talk as you go.*
   Run the recognition minute out loud on problem 4 as if it were unseen: chapter, precondition,
   range, question, return meaning — then the invariant and the predicted cost, before any code.

2. *Draw the class diagram for what you just described.*
   The plan sentence, the central class with its reason, the spine with multiplicities, one design
   decision narrated, the interface with its second implementation, and what you left out.

3. *How do you decide in ten seconds whether a problem is binary search at all?*
   The first question is not "is it sorted?" — it is "what is the answer?" Say both branches, the
   precondition for each, and the three exits.

---

## Before you move on

- [ ] I did all four problems standing, talking, with the naming scored separately.
- [ ] I named all ten phrasings in the two-second drill, including the three that are not binary
      search.
- [ ] I can recite the five pre-flight bugs with their checking inputs.
- [ ] I wrote `first_true` from memory and expressed all seven problems as questions to it.
- [ ] I can give every cost in the phase as a number, not a letter.
- [ ] I drew the library diagram in four minutes and it passed all eight checks.
- [ ] I can produce the five Mermaid arrow forms and the four multiplicities from memory.
- [ ] I answered all three questions above out loud.
