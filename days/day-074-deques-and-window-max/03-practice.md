---
day: 74
track: practice
title: "Practice — Deques and the sliding-window maximum"
status: written
---

# Day 074 · Practice

**DSA topic:** Deques and the sliding-window maximum
**System design topic:** Command and chain of responsibility

---

## Code these, in this order

One rule for the whole set: **before writing the loop, say what the deque holds and in what order.**
"Indices of elements that could still be the maximum of some future window, values falling from
front to back." If you cannot say that sentence, you are using the deque as scratch space.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Moving Average from Data Stream | LeetCode 346 (Easy) | The plain deque: add at the back, expire at the front, keep a running total. No monotonicity yet. |
| 2 | Sliding Window Maximum | LeetCode 239 (Hard) | Today's problem. The delete-for-ever observation, both removals, and the O(n) defence. |
| 3 | Longest Continuous Subarray With Absolute Diff ≤ Limit | LeetCode 1438 (Medium) | Two deques at once, and a window that shrinks rather than slides. |
| 4 | Shortest Subarray with Sum at Least K | LeetCode 862 (Hard) | A monotonic deque over prefix sums, with negatives — the case where a plain sliding window is simply wrong. |

### On problem 1, notice what is missing

There is no monotonic anything here. It is a queue with a running sum. Write it, then say in one
sentence what problem 2 needs that this one does not — and why that need is what forces both ends.

### On problem 2, write the brute force first and time it

Write the one-line `max(numbers[i:i+k])` version. Run it on 200,000 elements with k = 1,000 and time
it. Then time the deque version. Write both numbers down. You will quote them for years.

### On problem 3, run two deques side by side

1. Write it with only the max deque and see which cases fail.
2. Add the min deque.
3. Print both deques at every step for `[8, 2, 4, 7]`, `limit = 4`, and watch the left edge move.
4. Say why the window here *shrinks* rather than slides by exactly one, and what that changes about
   the expiry check.

### On problem 4, find out why the easy approach fails

1. Write the ordinary two-pointer sliding window for "shortest subarray with sum at least K" and run
   it on `[2, -1, 2]` with `K = 3`.
2. Say exactly which assumption of the sliding window the negative number broke.
3. Then build prefix sums and run a monotonic deque over them, and say what the deque now holds.

---

### The observation drill

Say it out loud, five times, until it is automatic:

1. What happens to every earlier smaller element when a bigger one arrives, and why "for ever"?
2. Why does that argument need the words "because the new one is later"?
3. What exactly is left in the deque, described as a property rather than as code?
4. Why is it in falling order without anything sorting it?
5. Name the two removals and the different reason for each.

### The trace drill

Trace `[1, 3, -1, -3, 5, 3, 6, 7]` with k = 3, writing the deque contents after every step. Then
answer without looking:

1. At which index do both removals happen in the same step?
2. What is the largest the deque ever gets, and why is that smaller than k here?
3. Which input of length 8 would make the deque hold all 3 allowed indices at every step?
4. Which input would make it hold exactly one at every step?

### The break-it drill

Trigger each and record the actual output or error text:

1. Store values instead of indices. Get as far as the front expiry and say what you cannot write.
2. Remove `window and` from the `while` condition. Quote the exact error.
3. Drop the `if index >= k - 1` guard. Run the standard input and count the answers.
4. Change the expiry to `window[0] < index - k`. Run `[1, 3, -1, -3, 5, 3, 6, 7]` with k = 3 — it is
   *right*. Then run `[8, 3, 2]` with k = 2 and say what it returns and why.
5. Do the front expiry *after* appending and recording. Say which answer becomes stale.
6. Use a plain list with `pop(0)` instead of a deque. Time it at n = 200,000, k = 1,000.
7. Change `<=` to `<` on the back removal. Confirm it is still correct, then say what changed about
   the deque's size on `[5, 5, 5, 5, 5]`.

### The heap-comparison drill

1. Write the lazy-deletion heap version.
2. Time both at n = 200,000, k = 1,000. Write down the ratio.
3. Say the one-sentence conceptual difference between them, the one with "write time" and "read
   time" in it.
4. State both space complexities and say why one is O(k) and the other O(n).
5. Say what you would do if you blanked on the deque version under pressure.

### The recognition drill

For each, say whether a monotonic deque is the tool, and if so what it holds:

1. The maximum of every window of size k.
2. The average of the last k readings.
3. The longest window where max − min ≤ limit.
4. The next greater element for every item.
5. The maximum score when you may jump at most k steps forward.
6. The shortest subarray with sum at least K, with negatives allowed.
7. The number of requests in the last second, for a rate limiter.
8. The median of every window of size k.

One of the eight needs a completely different structure. Name it and say what.

---

### The undo drill

Build it and then attack it:

1. Write `InsertText` with `execute` and `undo`.
2. Write `DeleteText`. Say which line makes undo possible and what happens without it.
3. Write `History` with both stacks.
4. Do three edits, undo twice, then do a new edit. Print the redo stack. Explain the result.
5. Remove the `self._redo.clear()` line and repeat step 4. Say exactly what redo now does to the
   document.
6. Write `MacroCommand`. Undo it with the children in the original order and describe the damage.
7. Add a depth cap. Say why you drop the oldest and not the newest.

### The memory drill

1. Compute the snapshot cost for a 1 MB document at 500 levels of undo.
2. Compute the command cost for the same history.
3. State the ratio.
4. Describe the mixed strategy, and say how many operations a 500-step undo costs under it.
5. Say which of the two you would pick for a drawing app whose entire state is 4 KB, and why.

### The cannot-undo drill

For each, say whether it belongs on the undo stack, and what you would do instead if not:

1. Typing a character.
2. Deleting a paragraph.
3. Sending an email.
4. Charging a card.
5. Renaming a file on disk.
6. Posting a comment that others may have already read.
7. Generating a new document id.

Two of the seven can only be *compensated*, not undone. Name the difference in one sentence.

### The chain drill

Build the expense-approval chain with limits of ₹1,000, ₹10,000 and ₹1,00,000.

1. Write the base handler with the three cases in it.
2. Run ₹800, ₹9,000, ₹80,000 and ₹9,00,000. Say what happens to the last one by default.
3. Fix the last case deliberately. Say what you chose and why.
4. Insert a vice-president between manager and director. Count the files edited.
5. Log which handler terminated each request, and say why that log exists.

### The middleware drill

Given this pipeline: request id, logging, CORS, session load, authentication, rate limit, CSRF,
compression.

1. Add up the per-request overhead from the lesson's numbers.
2. Compute the CPU cost per second at 5,000 requests per second.
3. Reorder it for cheapest-rejection-first and say what moved and why.
4. Say what breaks if authorisation runs before authentication.
5. Say which handler must be outermost so that failures anywhere are still recorded.

### The which-pattern drill

For each, say Command, chain of responsibility, Observer, or none:

1. Ctrl+Z in an editor.
2. Five things must happen when an order is placed.
3. A request passes through auth, rate limiting and logging.
4. A slow job runs in the background when a button is clicked.
5. An expense needs approval at the right level.
6. The write-ahead log in a database.
7. A click event travelling up from a button to the body.
8. A new pricing rule per country.

One of the eight is Strategy from [day 071](../day-071-monotonic-stack/README.md). Name it. Two are
Command for the same reason — say the reason.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the maximum in every window of size k.*
   The brute force with a number, the delete-for-ever observation stated before any structure, what
   survives and why it is ordered without sorting, the two removals at two ends with their two
   different reasons, indices-not-values, the record guard, the O(n) counting argument, and O(k)
   space with the heap named and rejected.

2. *Design undo and redo for a text editor.*
   The move from calling to creating, the four things an object buys, the snapshot number killed with
   the command number, the two stacks with the redo-clearing rule, delete as the interesting command,
   macros with reversed undo, the depth cap, and the two boundaries — repeatable `execute`, and two
   users needing OT or CRDTs.

3. *There is a `while` inside the `for`. Is that not O(n·k)?*
   n appends total, each index removed at most once, so ≤ 2n operations — bounded in total, not per
   iteration — plus the example where one arrival crushes a thousand elements and why that costs
   nothing.

---

## Before you move on

- [ ] I can state the delete-for-ever observation and say why "for ever" is justified.
- [ ] I can name both removals and give the different reason for each.
- [ ] I can say why this needs a deque rather than a stack or a queue.
- [ ] I traced the standard input and know where both removals happen in one step.
- [ ] I measured the brute force, the heap and the deque, and can quote all three numbers.
- [ ] I know what `[8, 3, 2]` with k = 2 returns under the off-by-one expiry.
- [ ] I dropped the record guard and counted the wrong number of answers.
- [ ] I can state the space as O(k) and name the worst-case and best-case inputs.
- [ ] I wrote the two-deque version for max − min ≤ limit.
- [ ] I built `InsertText`, `DeleteText`, `History` and `MacroCommand`.
- [ ] I removed the redo-clearing line and saw what redo did to the document.
- [ ] I can quote the 500 MB against 0.5 MB comparison and explain the thousandfold.
- [ ] I can name two actions that can only be compensated, not undone.
- [ ] I built the approval chain and decided deliberately what happens at the end of it.
- [ ] I can say the cheapest-rejection-first rule and what it saves under attack.
- [ ] I answered all three questions above out loud.
