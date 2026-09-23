---
day: 92
track: practice
title: "Practice — Permutations"
status: written
---

# Day 092 · Practice

**DSA topic:** Permutations
**System design topic:** Design a notification service

---

## Code these, in this order

One rule for the whole set: **count the branching out loud before you write anything.** `n`, then
`n − 1`, then `n − 2`. If you catch yourself saying "exponential", stop and count again — `n!` is worse
than `2ⁿ`, and the interviewer can hear the difference.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Permutations | LeetCode 46 (Medium) | The `used` list replacing `start`, and two un-chooses for two chooses. |
| 2 | Letter Case Permutation | LeetCode 784 (Medium) | The same tree where the branching factor is 1 or 2 depending on the character. |
| 3 | Permutations II | LeetCode 47 (Medium) | `not used[i - 1]` — the hardest single line in the phase. |
| 4 | Beautiful Arrangement | LeetCode 526 (Medium) | Permutations with a validity check before recursing, which is what pruning buys. |

### On problem 1, break it deliberately first

Write it with `used[i] = True` and no matching `used[i] = False`. Run it on `[1, 2, 3]` and record what
comes out. Then say, in one sentence, why one answer appears instead of six.

### On problem 2, notice what the branching factor did

A digit branches once. A letter branches twice. Say what the total count is for a string with `k`
letters and `m` digits, and say why it is `2ᵏ` rather than anything factorial.

### On problem 3, test `[1, 1]` before anything else

The right answer has exactly one permutation. Write the version with only
`items[i] == items[i-1]` and confirm it returns an empty list. Then add `and not used[i - 1]` and say
out loud what the added clause means about the tree.

### On problem 4, count the calls with and without the check

Move the divisibility check from the base case to just before the recursive call. Run n = 12 both ways
and record both call counts. That gap is the whole argument for pruning.

---

### The size drill

1. Say why there are exactly `n!` permutations, counting the positions out loud.
2. Compute `n!` for n = 8, 10, 12 and 13.
3. Put `2ⁿ` and `n!` side by side for n = 5, 10, 15 and 20.
4. Say at which `n` factorial overtakes exponential.
5. Given a problem that bounds `n` at 8, say which of the two it is asking for and why you know.

### The `start` drill

1. Say why `range(start, n)` is correct for subsets.
2. Say why it is wrong for permutations, using `[1,2]` and `[2,1]`.
3. Name the two things that can replace it.
4. Say which one you would write in an interview, and give the reason that is about duplicates.

### The un-choose drill

1. Write the five-line block from memory: choose, choose, recurse, un-choose, un-choose.
2. Say which two lines are the chooses and which two are the un-chooses.
3. Remove `used[i] = False` and run `[1, 2, 3]`. Record the output.
4. Explain why the result is one permutation and not, say, three.
5. Say why this failure produces no error.

### The copy drill

1. Write the version that appends `current` instead of `current[:]`.
2. Run it on `[1, 2, 3]` and describe exactly what you see.
3. Do the same for the swap version with `result.append(items)` and say why every entry reads `[1,2,3]`.
4. Name three ways to take the copy.

### The swap drill

1. Write the in-place version from memory.
2. Say what the bar means: what is true of everything before `first`, and everything from `first` on.
3. Say why the loop starts at `first` and not at `first + 1`.
4. Remove the second swap and run `[1, 2, 3]`. Record the output.
5. Confirm the input list is unchanged after a correct run, and say why that matters to a caller.
6. State the extra space for this version and for the `used` version, separately.

### The duplicates drill

1. Sort, then write the skip with `and not used[i - 1]`.
2. Say the condition's meaning as an English sentence about twins.
3. Say the rule in one line: among equal elements, use them in which order?
4. Run `[1, 1, 2]` and count distinct answers against decision paths.
5. Remove the sort, run `[2, 1, 1]`, and say why nothing gets skipped.
6. Run `permutations_swap([1, 1, 2])` and say why the adjacency rule cannot rescue it.
7. Compute the distinct count for `[1, 1, 2, 2]` from `4! / (2! × 2!)`.

### The break-it drill

Trigger each and record the exact output:

1. `used[i] = False` omitted.
2. `result.append(current)` without the copy.
3. `and not used[i - 1]` omitted, on `[1, 1]`.
4. The sort omitted, on `[2, 1, 1]`.
5. The second swap omitted in the in-place version.
6. `set(permutations([1, 1, 2]))` — record the traceback line for line.

### The cost drill

1. State the time complexity and say where each factor comes from.
2. State the extra space, separately from the output.
3. Compute the number of tree nodes at n = 10 and the stack depth at n = 10.
4. Say which of those two numbers is the time and which is the space.
5. Estimate the memory for the full result at n = 10 and say what you would do instead.

---

### The five-decisions drill

1. Name the five decisions the notification service makes, in order.
2. Say what goes wrong if preferences are checked after the render rather than before.
3. State the one rule about what callers pass in, and give the two consequences of breaking it.
4. Say what `SUPPRESSED` records that dropping the message would not.

### The two-interfaces drill

1. Name both interfaces and what each one decides.
2. Answer "now add WhatsApp" in one sentence, naming exactly what changes.
3. Write the `Channel` interface and one implementation.
4. Say which field of `SendResult` people forget, and what it costs to get it wrong.
5. Give four event types and the retry policy each one deserves, with the reason for the password reset.

### The duplicate-delivery drill

1. Name the three ways a user ends up with the same email three times.
2. Say what a compare-and-set on the status does, and write the `UPDATE` statement.
3. Say where the idempotency key comes from and what enforces it.
4. Say why exactly-once delivery to a third party is not achievable, in one sentence.

### The retry drill

1. Write `ExponentialBackoff.next_delay` and say what `None` means.
2. Say what jitter is for, and what happens to a recovering provider without it.
3. Say when you would add a circuit breaker and what it does while it is open.
4. Say why a permanently-bad phone number must not be retried, in money.

### The numbers drill

Compute each, showing the multiplication:

1. Notifications per day and per second at 10M users and 5 per user per day.
2. Peak provider calls per second at 3× average and 1.8 channels per event.
3. Delivery log size per day and per year at 300 bytes a row.
4. The monthly SMS bill at 5 percent of volume and ₹0.15 a message.
5. The saving from moving a fifth of those users to push.

### The failure drill

For each, say what happens and what you would add:

1. The SMS provider is down for two minutes.
2. The worker crashes after calling the provider but before writing `SENT`.
3. A user unsubscribes while a marketing message is already on the queue.
4. Ten million broadcast messages are enqueued at 9 a.m.
5. A template change is deployed, and support asks what was sent last Tuesday.
6. Two events for one user must arrive in order, and the first one retries.

Two of the six are not fixable inside this design as drawn. Name them and say what you would build
instead.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Generate all permutations. Now handle duplicate values.*
   The `n!` counted out position by position rather than named, why `start` no longer works, the `used`
   list with two chooses and two un-chooses, the copy flagged before you write it, both complexities
   kept separate, and then the duplicate rule as an English sentence about twins — plus the reason it is
   not subsets' `i > start`.

2. *Design a notification service that supports email, SMS and push.*
   The boundary first, then the one rule about events versus messages, the five decisions in order, both
   interfaces with the reason there are two, at-least-once delivery and the compare-and-set, and the
   numbers — 50M a day, 3,000 provider calls a second at peak, ₹11M a month of SMS.

3. *Now add WhatsApp. What changes?*
   One class, one registration line, one template per event, one preference value — and nothing in the
   dispatcher. Then say what the answer would have been if the dispatcher had an `if channel ==` in it.

---

## Before you move on

- [ ] I can count `n!` out loud position by position, without saying "exponential".
- [ ] I can put `2ⁿ` and `n!` side by side and say where factorial overtakes.
- [ ] I can say why `start` works for subsets and fails for permutations.
- [ ] I wrote the five-line block from memory, with both un-chooses.
- [ ] I ran the version without `used[i] = False` and can explain the single answer.
- [ ] I can write the swap version and say what the second swap is for.
- [ ] I can write the duplicate rule and say what `not used[i - 1]` means about twins.
- [ ] I tested `[1, 1]` with the wrong condition and know what it returns.
- [ ] I can state time and extra space separately, with the node count and the depth at n = 10.
- [ ] I can say what I would do instead of building the whole result at n = 10.
- [ ] I can name the five decisions the notification service makes, in order.
- [ ] I can answer "now add WhatsApp" in one sentence.
- [ ] I can say why there are two interfaces and not one.
- [ ] I can explain at-least-once delivery and write the compare-and-set.
- [ ] I can produce the volume, storage and SMS-cost numbers with the multiplication shown.
- [ ] I can say what breaks when ten million broadcast messages hit the same queue.
- [ ] I answered all three questions above out loud.
