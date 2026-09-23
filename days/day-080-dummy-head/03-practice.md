---
day: 80
track: practice
title: "Practice — The dummy head trick"
status: written
---

# Day 080 · Practice

**DSA topic:** The dummy head trick
**System design topic:** Design an ATM

---

## Code these, in this order

One rule for the whole set: **the moment you type `dummy = Node(0, head)`, type `return dummy.next`
as well** — before the loop, before anything. Half the bugs in this technique are a `return head` that
was written on autopilot at the end.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Remove Linked List Elements | LeetCode 203 (Easy) | The guard form. `[7,7,7,1,7]` for the leading run, `[1,7,7,2]` for the advance rule. |
| 2 | Merge Two Sorted Lists | LeetCode 21 (Easy) | The builder form, and attaching the remainder wholesale instead of node by node. |
| 3 | Remove Nth Node From End of List | LeetCode 19 (Medium) | Where the dummy does real work: the head case *and* landing on the predecessor. |
| 4 | Remove Duplicates from Sorted List II | LeetCode 82 (Medium) | A head that is part of a duplicate run, so no `if` can save you. |

### On problem 1, run the four inputs before you submit

`[7,7,7,1,7]`, `[7,7,7]`, `[1,7,7,2]`, `[]`. The first tests the leading run, the second tests
returning an empty list, the third tests the advance rule and has nothing to do with the head, and the
fourth is the one people skip. Any solution that passes all four is almost certainly right.

### On problem 2, attach the remainder in one line

When one list runs out, do not keep looping. `tail.next = a if a is not None else b` attaches the
whole remaining chain in one assignment, because it is already sorted and already linked. Say out loud
why that is correct.

### On problem 3, do it without the dummy first

Write the version with a gap of `n + 1` and an explicit head check. Count the lines and the branches.
Then write the dummy version and count again. Say what the dummy did *twice* here.

### On problem 4, find the input that beats an `if`

Construct an input where the head, the second node and the third node are all part of the same
duplicate run. Then say why a single `if` on the head cannot handle it and a `while` on the head is
still worse than a dummy.

---

### The two-forms drill

1. Write the guard form and say which constructor argument matters.
2. Write the builder form and say which cursor exists only because of it.
3. Say the single sentence that describes what both forms have in common.
4. Give three problems that need the guard form and three that need the builder form.
5. Give two problems where a dummy would be pure noise, and say what they have in common.

### The return drill

1. Write `remove_elements` returning `head` instead of `dummy.next`.
2. Run it on `[7, 7, 1]` with target 7 and write down what comes back.
3. Explain, in terms of what `head` refers to, why nothing raised.
4. Say the habit that prevents it.

### The advance drill

1. Write the loop that advances `previous` in both branches.
2. Run it on `[1, 7, 7, 2]` and write down the output.
3. Explain what `previous.next` is immediately after an unlink.
4. Say why this bug survives adding a dummy node.
5. Construct the shortest input that exposes it.

### The break-it drill

Trigger each and record the exact output or error text:

1. `return head` instead of `return dummy.next`, on `[7, 7, 1]`.
2. Advance `previous` unconditionally, on `[1, 7, 7, 2]`.
3. Walk `dummy` itself instead of a separate cursor. Print the result.
4. Create the dummy inside the loop. Say what it costs and why the output is still right.
5. Write `dummy = Node(0)` when you meant `Node(0, head)`. Run any input.
6. In `partition`, omit `more.next = None`. Print the result and describe what happens.
7. In `merge_two_sorted`, use `<` instead of `<=`. Say what property you lost, and construct an input
   where it is visible.

### The counting drill

For `remove_elements`, both versions:

1. Count the lines, the loops, the head-specific branches, and the places `head` is referenced.
2. Do the same for the dummy version.
3. Say which of the two head branches in the naive version handles `[7,7,7,1]` and which handles
   `[7,7,7]`.
4. State the extra space of the dummy version, precisely.

### The recognition drill

For each, say whether you would use a dummy, which form, and why:

1. Remove every node equal to a value.
2. Count the nodes.
3. Merge two sorted lists.
4. Find the middle node.
5. Remove the nth node from the end.
6. Detect a cycle.
7. Partition around a value.
8. Reverse the list.
9. Swap every pair of adjacent nodes.
10. Sum all the values.

Four of the ten need no dummy. Say the one-sentence rule that rejects all four.

### The build-it drill

From an empty file, without looking, write `remove_elements`, `merge_two_sorted`,
`remove_nth_from_end` and `partition`. Then run each on: the empty list, a one-element list, a list
where every element matches, and a list where none does. Any function that fails one of those four is
the one to rewrite.

---

### The state-machine drill

Draw the ATM state machine from memory, then answer:

1. Which state has no cancel transition, and why is that physical rather than a design choice?
2. Which state does every failure path have to be able to reach?
3. What happens after three wrong PIN attempts, and which state is that?
4. Name the state that exists only because a customer may walk away.
5. Why does the base state class refuse everything by default?

### The ordering drill

1. Write the three steps of a withdrawal in order.
2. Say what fails, and what is lost, if the order is dispense-then-debit.
3. Compute the daily unrecoverable loss under that ordering at 5,000 ATMs, 200 transactions a day,
   0.5 percent failure and ₹3,000 average.
4. Say what the customer experiences under the correct ordering, and how long it lasts.
5. Say which regulator rule exists because of exactly this failure.

### The failure-table drill

For each, say what the machine does, what the bank does, and what reconciliation sees:

1. The network dies before authorisation.
2. The network dies after the debit, before dispensing.
3. The notes jam halfway through dispensing.
4. The confirmation message is lost after a successful dispense.
5. The customer does not take the presented notes.
6. The power fails between the journal write and the dispense.
7. The ATM retries an authorisation it already got an answer to.

One of the seven is the case where the bank must **not** reverse. Name it and say what stops it.

### The dispenser drill

1. Write the greedy planner.
2. Find an amount and a cassette state where greedy fails but a solution exists. Prove it by hand.
3. Write the bounded search.
4. State its worst-case size for four denominations and forty notes each, and how long it actually
   takes.
5. Say the rule about when the plan is computed, and what goes wrong if you dispense as you go.
6. Compute the notes needed for ₹3,000 with the ₹500 cassette empty, and say what that does to the
   maximum withdrawal at a 40-note cap.

### The estimation drill

Compute each, showing the multiplication:

1. Total cash capacity for the loadout in the lesson.
2. Days between replenishments at 200 withdrawals of ₹3,000.
3. Incomplete transactions per ATM per day, and for a bank with 5,000 ATMs.
4. Time to dispense 8 notes and 15 notes at 4 notes a second.
5. The end-of-day reconciliation identity: what three quantities must balance?

### The security drill

1. Where is the PIN verified, and where is it encrypted?
2. What does the ATM store about the PIN?
3. What does the ATM track that is PIN-related, and why?
4. Say what is wrong with the answer "the ATM checks the PIN against the chip on the card".

### The testability drill

1. Say why `BankClient` is an interface, in terms of what you cannot otherwise test.
2. List the five behaviours your fake bank must be able to produce on demand.
3. Write the assertions for the "timeout after debit" test: what should the journal contain, what
   should the cassettes contain, what should be queued?
4. Say why testing the happy path here is nearly worthless.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Remove all nodes with a given value, including at the head.*
   The head having no predecessor and being a *run* rather than a single case, the dummy in one line,
   `return dummy.next` with the silent failure named, the advance-only-when-you-keep rule stated as
   separate from the dummy, O(n) and O(1), and the four inputs you would run.

2. *Design an ATM. What happens if the network dies mid-withdrawal?*
   The three parts, the failure-rate estimate that justifies a pipeline, debit-then-dispense with the
   asymmetry and the crore-a-day comparison, timeout meaning unknown rather than no, the journal
   written before acting, the STAN making retries idempotent, auto-reversal and end-of-day
   reconciliation, and the fact that dispense must never be retried.

3. *Why not just handle the head with an `if`?*
   Because it is a run, not a single node, so it is a `while`; plus a second branch for the
   everything-deleted case; and the dummy takes the count to zero rather than making it smaller.

---

## Before you move on

- [ ] I write `return dummy.next` at the same moment I write the dummy.
- [ ] I can state the advance-only-when-you-keep rule and why it is independent of the dummy.
- [ ] I ran all four inputs on `remove_elements` and know what each one tests.
- [ ] I returned `head` on purpose and saw the silent wrong answer.
- [ ] I can write both the guard form and the builder form from memory.
- [ ] I omitted `more.next = None` in `partition` and saw the cycle.
- [ ] I wrote `remove_nth_from_end` both with and without a dummy and counted the branches.
- [ ] I can name four problems where a dummy would be noise, and the rule that rejects them.
- [ ] I can draw the ATM state machine and say why `Dispensing` has no cancel.
- [ ] I can state the three withdrawal steps and defend the order with the loss comparison.
- [ ] I can say what a timeout means and what the machine does in response.
- [ ] I can name the one failure case where the bank must not reverse.
- [ ] I found a cassette state where greedy fails and a solution exists.
- [ ] I can say where the PIN is verified and what the ATM stores.
- [ ] I can list the five behaviours a fake bank must produce for testing.
- [ ] I answered all three questions above out loud.
