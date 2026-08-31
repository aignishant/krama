---
day: 82
track: practice
title: "Practice — Finding the middle, and the runner technique"
status: written
---

# Day 082 · Practice

**DSA topic:** Finding the middle, and the runner technique
**System design topic:** Design a library management system

---

## Code these, in this order

One rule for the whole set: **before writing the loop, say which runner variant you need — different
speeds, or a fixed gap.** They solve different problems and mixing them up wastes five minutes you do
not have.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Middle of the Linked List | LeetCode 876 (Easy) | The two-guard loop condition, and whether you raise the even-length ambiguity before being told. |
| 2 | Remove Nth Node From End of List | LeetCode 19 (Medium) | The fixed gap, the dummy putting `slow` on the predecessor, and `n` larger than the list. |
| 3 | Palindrome Linked List | LeetCode 234 (Easy) | Three techniques in one, and restoring the caller's list afterwards. |
| 4 | Reorder List | LeetCode 143 (Medium) | Split, reverse, interleave — and the interleave loop's terminating condition. |

### On problem 1, ask the question out loud first

"On an even-length list there are two middles — which do you want?" Then write the version they asked
for, and afterwards write the other one and confirm both by running `[1,2,3,4]`.

### On problem 2, do the arithmetic without the dummy once

Write it with `slow = head` and a gap of `n + 1`, and handle the head separately. Count the branches.
Then write the dummy version. Say the two distinct jobs the dummy did.

### On problem 3, print the list after returning

Every test that only checks the boolean passes whether or not you restored the list. Add a print of
the original list after the call and make it match the input. That is the actual requirement.

### On problem 4, write the interleave slowly

The loop that weaves two half-lists together is four assignments and it is easy to build a cycle. Draw
the pointers for `[1,2,3]` and `[5,4]` before writing, and check the last node points at `None`.

---

### The two-variants drill

1. State both runner variants in one sentence each.
2. For each, say what is true when the fast pointer stops.
3. Give two problems solved by the speed variant and two by the gap variant.
4. Say which variant tomorrow's cycle detection uses, and what changes about the conclusion.

### The condition drill

1. Write the middle loop condition and say what each half protects against.
2. Swap the two halves and run it on `[1,2,3,4]`. Quote the error.
3. Write the other condition and say which middle it gives.
4. Run both on `[1,2,3,4]` and on `[1,2,3,4,5]`. Write all four answers down.
5. Say which one a merge sort needs, and what happens if you use the other.

### The gap drill

1. Write the opening walk with its bounds check.
2. Remove the check and run it with `n` larger than the list. Quote the error.
3. Say the two reasonable behaviours for that case and pick one.
4. Explain why the gap never changes once the second loop starts.
5. Say where `slow` must start if you want the predecessor, and why.

### The break-it drill

Trigger each and record the exact output or error text:

1. Loop condition in the wrong order. Run `[1,2,3,4]`.
2. Use the second middle to split for a merge sort. Run `[1,2]` and describe the failure.
3. Forget `middle.next = None` in the split. Print both halves.
4. Start `slow` at the head instead of the dummy in `remove_nth_from_end`. Run `[1,2,3,4,5]` with
   n = 2 and say which node actually disappeared.
5. Skip the restore in `is_palindrome`. Print the original list afterwards.
6. In `reorder`, forget to terminate the woven list. Describe the failure.

### The complexity-honesty drill

1. Count the pointer moves for the one-pass middle.
2. Count them for the two-pass version.
3. State both complexities.
4. Say, in one sentence, what one pass actually buys — and what it does not.
5. Say what makes one traversal genuinely better than two on a linked list specifically.

### The composition drill

Write `reorder` from scratch using only functions you already have, then answer:

1. Which day did each of the three pieces come from?
2. Which middle does the split need, and why?
3. What is the terminating condition of the interleave, and why is it the shorter half?
4. Confirm the final node points at `None` and say how you checked.

---

### The modelling drill

1. Say, in one sentence, why "a book" needs two classes.
2. List four fields that belong on the title and four that belong on the copy.
3. Say which class a reservation points at, and which a loan points at.
4. Give three questions the split answers cleanly that a merged class cannot.
5. Name three other domains with the same title-versus-instance split.

### The responsibility drill

For each candidate home for the late-fee rule, give the one-sentence rejection:

1. `Book`
2. `BookItem`
3. `Member`
4. `Loan`
5. `LendingService`

Then state where it does belong, and name the two constructor dependencies that prove it.

### The anaemic-model drill

1. List four methods that belong on `Loan`.
2. List two that do not, and say why.
3. State the boundary as a single sentence containing `days_overdue` and `rupees_owed`.
4. Say what would make `Loan` genuinely anaemic, and why this version is not.

### The policy drill

1. Write the `FinePolicy` interface.
2. Write the standard implementation, including the closed-days handling.
3. Write the festival amnesty as a *wrapper* rather than a branch. Name the pattern.
4. Apply the interface gate to both `FinePolicy` and `LendingPolicy` and say what a second
   implementation is for each.
5. Say when you would move these from classes to a configuration table, and why.

### The reservation drill

1. Say which class the queue is attached to and why.
2. Walk through what happens when a copy is returned and someone is waiting.
3. Say why `HELD` must be a separate state from both available and loaned.
4. Say what goes wrong with no hold expiry.
5. Compute the wait for position 40 in a queue for a title with 6 copies and a 14-day loan.
6. Compute the copy-days lost per year to uncollected holds at a 20 percent no-show rate.

### The estimation drill

Compute each, showing the multiplication:

1. Total memory for titles, copies and members.
2. Loan history growth per year.
3. Operations per second across loans, returns and searches.
4. Annual fine revenue at 15 percent late, 4 days average, ₹2 a day.
5. The fine on a book forgotten for three years, uncapped, against the book's cost.
6. The percentage of days the library is closed, and the overcharge on a four-day overdue.

Then say which two numbers you would quote in the first ten minutes of the interview, and why.

### The concurrency drill

1. Name the two-step operation that races when two members want the last copy.
2. Write the conditional update that fixes it.
3. Say what zero rows updated means and what the member sees.
4. Say why this is the same pattern as the parking spot and the shipped order.
5. Say roughly how often it will fire at this system's traffic, and why you build it anyway.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Remove the Nth node from the end in one pass.*
   The two-pass baseline named and set aside, the gap variant with the invariant in one sentence, the
   dummy doing two jobs, the bounds check on the opening walk, the honest complexity claim, and the
   three inputs you would run.

2. *Design a library system. Who owns the rule about late fees?*
   The title-versus-copy split stated first with the one-sentence payoff, each wrong home for the fine
   rule rejected with a reason, `FinePolicy` with its two telling dependencies, the
   `days_overdue`/`rupees_owed` boundary, the closed-days and uncapped-fine numbers, and the hold
   state with its expiry.

3. *Why not just put `calculate_fine()` on the `Loan` class?*
   The four things it would need that are not on the loan, all of which change without any loan
   changing, and the constructor test that makes it concrete.

---

## Before you move on

- [ ] I can state both runner variants and what is true when the fast pointer stops.
- [ ] I can write the middle's loop condition and say what each half protects against.
- [ ] I ran both conditions on `[1,2,3,4]` and know which middle each gives.
- [ ] I know which middle a merge sort needs and what happens with the other one.
- [ ] I forgot the cut on purpose and saw two halves that were really one list.
- [ ] I wrote `remove_nth_from_end` without the dummy and counted the extra branches.
- [ ] I can say what one pass actually buys, without overclaiming.
- [ ] I wrote the palindrome check and confirmed the list was unchanged afterwards.
- [ ] I can say in one sentence why a book needs two classes.
- [ ] I can reject all four wrong homes for the fine rule, each with a reason.
- [ ] I can name the two constructor dependencies that prove the policy split.
- [ ] I can state the `days_overdue` / `rupees_owed` boundary.
- [ ] I wrote the amnesty as a wrapper and named the pattern.
- [ ] I can explain the `HELD` state and what breaks without a hold expiry.
- [ ] I can quote the closed-days percentage and the uncapped-fine arithmetic.
- [ ] I answered all three questions above out loud.
