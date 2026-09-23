---
day: 42
track: practice
title: "Practice — Binary search: the idea and the invariant"
status: written
---

# Day 042 · Practice

**DSA topic:** Binary search: the idea and the invariant
**System design topic:** Database revision and interview questions

---

## Code these, in this order

Today is the first day of a new phase, so the rule is different from a mock day: **write the loop
from memory before you look at §5, every single time.** Four problems, and the fourth is deliberately
not an array search.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Binary Search | LeetCode 704 (Easy) | The template itself: `<=`, `middle + 1`, `middle - 1`, and `-1` as a conclusion. |
| 2 | Search Insert Position | LeetCode 35 (Easy) | Whether you noticed where `low` ends up when the target is absent. |
| 3 | Guess Number Higher or Lower | LeetCode 374 (Easy) | Binary search with no array at all — the space is a range of numbers. |
| 4 | Valid Perfect Square | LeetCode 367 (Easy) | The first sight of searching an answer range instead of data. |

### On problem 1, say the invariant before you type

Out loud, in one sentence: *if the target is anywhere, its index is between low and high inclusive.*
Then write the five lines. Then run the three inputs that catch beginner versions — `[]` with any
target, `[7]` with 7, `[7]` with 8. If any of them surprised you, rewrite the loop rather than
patching it.

### On problem 2, do not add a new loop

The whole answer is one word different from problem 1. When the loop ends without a match, `low` is
already sitting at the insertion point — trace it by hand on `[1, 3, 5, 6]` with target 2 and watch
where `low` finishes. Change `return -1` to `return low`, and say why that is correct rather than
lucky: the invariant guarantees everything left of `low` is smaller and everything from `low` on is
larger.

### On problem 3, notice there is nothing to index

The search space is the numbers 1 to n, not cells in memory. Same two variables, same halving, same
termination. This is the bridge to [day 046](../day-046-binary-search-on-the-answer/README.md), and
if it feels like the same problem, that is the point. Use `low + (high - low) // 2` here — n goes up
to 2³¹ − 1, and the problem exists partly to make the overflow point.

### On problem 4, name the monotone thing

Before coding, say what is sorted. It is not the input — the input is one number. It is the sequence
of squares `1, 4, 9, 16, …`, which never goes down, and that is the only property binary search
needs. Search `low = 1` to `high = num` and compare `middle * middle` against `num`.

### The off-by-one drill

Break your own working solution four ways, one at a time, and predict the symptom before you run it:

1. `while low < high` — which two inputs fail, and does it crash or lie?
2. `low = middle` instead of `low = middle + 1` — crash, wrong answer, or hang?
3. `high = len(nums)` instead of `len(nums) - 1` — paste the exact traceback.
4. Feed it `[5, 2, 9, 1, 7]` looking for 9 — what does it return, and why is that not a bug in the
   function?

Being able to predict the symptom is worth more than being able to fix it.

### The counting drill

Answer in under ten seconds each, no calculator: comparisons needed for 1,000 elements; 1,000,000;
1,000,000,000. Then the sentence that generates all three without memorising any of them.

### The database phase-closing drill

The database phase ends today. Run Nasreen's six questions on a product you have not seen written
about here — pick a hostel room-booking system — and speak the answer in under four minutes,
standing:

1. The access paths, three of them, as questions and not entities.
2. One number, multiplied out.
3. The one invariant that must never be false.
4. The tables, keys and two indexes, each index named with its query.
5. What happens when two people book the same room in the same second, and which of the three fixes
   you pick.
6. The trigger that would change your mind, with a number in it.

Then say the diagnosis order for a slow page — and remember which two causes never appear in a query
plan.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Search a sorted array. Why is it O(log n)?*
   The invariant first, then the code as sentences, then the halving count — n, n/2, n/4 — and the
   line about every doubling costing one more comparison.

2. *Design and defend the database layer for an unseen product.*
   The six questions in order, ending on the trigger. If you reach for a product name before
   question five, start again.

3. *Your binary search returns −1 for a value that is definitely in the list. What are the two
   possible causes?*
   The input was not sorted, or the loop used `<` and never looked at the last remaining cell. Say
   which one produces which symptom, and the clarifying question that prevents the first.

---

## Before you move on

- [ ] I wrote binary search from memory, with no reference, and it handled `[]`, `[7]` found, and
      `[7]` absent.
- [ ] I can state the invariant in one sentence, and say which line of the code preserves it.
- [ ] I predicted the symptom of all four deliberate breakages before running them.
- [ ] I can give the comparison count for a thousand, a million and a billion without pausing.
- [ ] I ran the six database questions on the hostel booking system in under four minutes.
- [ ] I answered all three questions above out loud.
