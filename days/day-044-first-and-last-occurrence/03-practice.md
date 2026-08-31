---
day: 44
track: practice
title: "Practice — First and last occurrence"
status: written
---

# Day 044 · Practice

**DSA topic:** First and last occurrence
**System design topic:** Classes and objects

---

## Code these, in this order

Same rule as yesterday: **one template, two calls, no `- 1` inside any loop.** If you catch yourself
writing a `while` that walks one step at a time, stop — that is the trap this day exists for.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Find First and Last Position of Element in Sorted Array | LeetCode 34 (Medium) | The two bounds, and whether you resist find-then-walk. |
| 2 | Number of Occurrences / Count of an element | Standard (`bisect` warm-up) | That the count is one subtraction, and zero needs no special case. |
| 3 | Kth Missing Positive Number | LeetCode 1539 (Easy) | A boundary question where the array is not what you search on. |
| 4 | Find K Closest Elements | LeetCode 658 (Medium) | The bound as a *starting point* for a window, not as the answer itself. |

### On problem 1, run the three inputs that decide it

Before you look at anything else: `[]` with any target, `[1]` with target 1, and `[8] * 200000` with
target 8. Time the last one against a find-then-walk version you write deliberately. Say the ratio
out loud. That number — roughly seven thousand times — is the reason the question exists.

### On problem 2, do not write a loop

`upper_bound(nums, x) - lower_bound(nums, x)`. One line. Then check it on a value that is absent and
confirm you got 0 without an `if`. Then check it on an empty list. If either needed a special case,
your bounds are wrong, not your subtraction.

### On problem 3, name the monotone question first

The array holds present numbers; you are asked about missing ones. The bridge is that at index `i`,
the count of missing numbers below `nums[i]` is `nums[i] - (i + 1)`, and that count never goes down.
Say that sentence before writing anything. Then the question is
`missing_count(i) >= k` and the template does the rest — this is the first problem where the monotone
quantity is *computed* rather than read.

### On problem 4, the bound is the start of the work

`lower_bound` tells you where `x` belongs; the answer is a window of size `k` around it. Two ways:
expand outward with two pointers from that position ([day 028](../day-028-opposite-ends/README.md)),
or binary search directly on the *window's left edge*. Do the first, then read about the second and
say why it is `O(log(n - k))` instead of `O(log n + k)`.

### The walk-cost drill

Answer without running anything:

1. `[8] * 1_000_000`, target 8 — how many operations does find-then-walk do?
2. Same array, two bounds — how many?
3. What is `k` in `O(log n + k)`, and what is the worst case for `k`?
4. On which single input do the two approaches cost the same?

### The guard drill

For each, say what happens — a crash with a named exception, a silent wrong answer, or a correct
answer:

1. `lower_bound(nums, 99)` on a five-element array, then `nums[first]`.
2. `lower_bound` then `upper_bound - 1` with no equality check, target absent but in range.
3. `upper_bound - 1` computed before the validity check, target absent.
4. Two bounds run on `[("Asha", 31), ("Bala", 24)]` sorted by name, asking about age.

### The free-answers drill

From the two bounds alone, in one line each, no extra loops:

1. How many values are strictly less than `x`.
2. How many are less than or equal to `x`.
3. How many lie in `[a, b]` inclusive.
4. Whether `x` is present.
5. The slice containing exactly the copies of `x`.

### The modelling drill

Take this paragraph and produce a model out loud in four minutes:

> *A cinema has several screens. A show is a film on one screen at one time. Customers book seats for
> a show. A booking can be cancelled up to an hour before the show, and the seats go back on sale.*

1. Nouns underlined, verbs underlined.
2. Which nouns are **not** classes, and why.
3. The class that is **not** in the paragraph but that your model needs.
4. One sentence of responsibility per class, no "and" allowed in any of them.
5. Where the cancellation rule goes, and the one-sentence reason.
6. Which classes define `__eq__`, on which field, and which deliberately do not.

### The anaemic-model drill

For each, say whether it is a real class or a dictionary wearing a class's clothes, and if it is the
latter, name the rule that would fix it:

1. `class Seat: def __init__(self, row, number): ...` with only getters.
2. `class Booking:` with `cancel()` that checks the hour rule.
3. `class BookingService:` holding every rule about bookings, with `Booking` holding only fields.
4. `class Money:` frozen, with `add()` that refuses to add different currencies.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the first and last position of a target in a sorted array.*
   The contiguous-run observation, the two questions one character apart, the guard in the right
   order, and the pre-empted shortcut with its cost in terms of `k`.

2. *Model a library. What are your classes?*
   Nouns and verbs, the `Book`/`Copy` split with its reason, the `Loan` class that was not in the
   paragraph, and one rule placed with a justification.

3. *Where would you put this rule, and why?*
   Pick any rule from the cinema drill. The answer is always "on the class that owns the data the
   rule reads" — say it in those words, then name what breaks if it goes elsewhere.

---

## Before you move on

- [ ] I solved LeetCode 34 with two template calls and no walking loop anywhere.
- [ ] I timed find-then-walk against two bounds on a million identical values and can quote the ratio.
- [ ] I can state the guard as two halves, in order, and say what each half prevents.
- [ ] I gave all five free answers from the two bounds without adding a loop.
- [ ] I ran the cinema modelling drill in four minutes, including the missing class.
- [ ] I can tell an anaemic model from a real one and name the rule that fixes it.
- [ ] I answered all three questions above out loud.
