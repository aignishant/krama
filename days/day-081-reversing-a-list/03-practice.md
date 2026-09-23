---
day: 81
track: practice
title: "Practice — Reversing a linked list"
status: written
---

# Day 081 · Practice

**DSA topic:** Reversing a linked list
**System design topic:** Design a vending machine

---

## Code these, in this order

One rule for the whole set: **say "save, turn, previous up, current up" before you write the loop,
every time.** Until those four words arrive without thinking, you are not finished with this day.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Reverse Linked List | LeetCode 206 (Easy) | The three-pointer dance, iteratively and recursively, with the stack cost volunteered. |
| 2 | Palindrome Linked List | LeetCode 234 (Easy) | Reversal as a *tool*: find the middle, reverse half, compare — and restore it afterwards. |
| 3 | Reverse Linked List II | LeetCode 92 (Medium) | Capturing the sublist's future tail before you start, plus both reattachments. |
| 4 | Reverse Nodes in k-Group | LeetCode 25 (Hard) | Counting before reversing, and the three-way reattachment per group. |

### On problem 1, write it blind

Close the lesson. Write the iterative version from memory. Then write the recursive one. Then, without
running them, predict the output for `[]`, `[1]` and `[1, 2]`. Then run them.

### On problem 2, restore what you broke

The O(1)-space solution reverses the second half of the caller's list. Leaving it reversed is a real
bug — you have mutated data you were only asked to inspect. Reverse it back before returning, and say
out loud why that matters even though the tests pass either way.

### On problem 3, capture before you reverse

Write it once *without* capturing the node at position `left` first. Get to the reattachment and find
you cannot name the node you need. That two minutes of being stuck is worth more than reading about
it.

### On problem 4, count first on purpose

Write the version that reverses first and then discovers the group was short. Watch yourself have to
un-reverse it. Then move the count to the front and compare the two.

---

### The four-lines drill

Say each answer out loud, five times:

1. What are the four lines, in order, as a four-word phrase?
2. What exactly is lost if you swap lines 1 and 2? Give the output for `[1, 2, 3]`.
3. Why does `previous` start as `None`, and what two jobs does that do?
4. What do you return, and what would returning `head` give you?
5. Why is the loop condition `current is not None` and not `current.next is not None`?
6. State the time and space, and count the assignments.

### The recursion drill

1. Write the base case and say why it covers two inputs.
2. State what you are *trusting* the recursive call to have done.
3. Explain what `head.next` points at when the call returns, in one sentence.
4. Write the two lines that do the work, and say what each achieves.
5. Delete `head.next = None` and run it. Describe the failure precisely.
6. State the space complexity and the exact error text at 5,000 nodes.
7. Say why `sys.setrecursionlimit` is not a fix.

### The break-it drill

Trigger each and record the exact output or error text:

1. Overwrite `current.next` before saving it. Run `[1, 2, 3]`.
2. Return `head` instead of `previous`. Run `[1, 2, 3, 4]`.
3. Loop on `current.next is not None`. Run `[1, 2, 3]`.
4. Omit `head.next = None` in the recursive version, then print the result.
5. In `reverse_between`, capture `tail_of_reversed` after the reversal instead of before. Describe
   what you actually captured.
6. In `reverse_k_group`, drop the count check. Run `[1, 2, 3]` with k = 5.
7. In `reverse_k_group`, forget to move `group_before` at the end of a group. Describe the loop.

### The escalation drill

1. Reverse the whole list.
2. Reverse positions 2 to 4 of a five-element list, by hand on the diagram, naming every pointer
   change.
3. Reverse in groups of 2, then 3, then 5, on `[1, 2, 3, 4, 5]`. Write all three outputs before
   running.
4. For each of the three escalations, say which part is "the same four lines" and which part is new.

### The application drill

1. Write `is_palindrome` in O(1) space using reversal.
2. Say which two other techniques it needs, and which day each came from.
3. Restore the list before returning, and say why.
4. Write "add two numbers given most-significant-digit-first" using reversal, and say what the
   alternative would be if you were forbidden to mutate the inputs.

### The space drill

1. Write the O(n)-space version using a Python list.
2. State exactly what it allocates for a million nodes, in megabytes.
3. State what the in-place version allocates.
4. Say the sentence you would use if you chose the O(n) version deliberately.

---

### The ordering drill

1. State the rule that decides the order of money and goods, in one sentence.
2. Apply it to the ATM and say which act goes first, and why.
3. Apply it to the vending machine and say which act goes last, and why.
4. Say why those two answers are the same principle rather than two memorised cases.
5. Describe what goes wrong in a vending machine that dispenses first, with a concrete amount.

### The state-machine drill

Draw the four states from memory, then answer:

1. Name the three transitions that leave `Collecting` and return to it, and say why none is a failure.
2. Which transition must be legal at any moment before dispensing, and what does it return?
3. Which state can fail *after* commitment, and what are the two things you do?
4. Why does the base state class refuse everything?

### The change drill

Given a coin box of ₹10 × 0, ₹5 × 2, ₹2 × 3, ₹1 × 0 and an escrow of one ₹20 note and one ₹10 coin:

1. Can the machine sell a ₹22 item? Show the working.
2. Can it sell a ₹25 item? Show the working.
3. What does that pair prove about the "exact change only" indicator?
4. Find a change amount where greedy fails and a solution exists.
5. Say why the escrow coins must be counted as available change, and what is lost if they are not.

### The escrow drill

1. Describe the escrow model and the immediate model in one sentence each.
2. Say what a cancel returns under each.
3. Say which one gives more change-making ability, and which one real machines use.
4. Give the reason real machines choose the one they do, in terms of power failure.

### The estimation drill

Compute each, showing the multiplication:

1. Items in the machine and days of stock at 120 sales a day.
2. Days of stock for a top-3 slot at 40 percent of sales across three slots.
3. Change paid out per day at 60 percent of customers averaging ₹8.
4. Days until the float runs out, given ₹800 loaded.
5. The gap between those two lifetimes, and what you would do about it.
6. Total machine state in kilobytes.

Then say which number tells you to report per-slot levels and which tells you to change the pricing.

### The failure drill

For each, say what the machine does and what the customer sees:

1. Sold out, money already inserted.
2. Not enough money inserted.
3. Cannot make change for the selected item.
4. Cancel pressed with ₹40 inserted.
5. The motor jams after commitment.
6. Power fails while coins are in escrow.
7. The same slot jams a second time.

Two of the seven leave the machine in `Collecting`. Name them and say why that is right.

### The cashless drill

1. Say what changes in the ordering when payment is by card or UPI.
2. Say which three components stop mattering.
3. Say which failure mode you have just imported, and from which lesson.
4. Say what you would add to handle it.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Reverse a linked list. Now do it in groups of k.*
   What is actually changing, the hazard on line 2 stated before writing, the four lines as a phrase,
   why `previous` starts as `None`, returning `previous`, the complexities — then k-groups: count
   first, reverse exactly k, three reattachments, O(2n) and O(1).

2. *Design a vending machine. Handle exact change and refunds.*
   Three parts and one customer at a time, the four states with the three refusals that stay in
   `Collecting`, escrow and what cancel returns, verify-change-before-dispensing with the
   reversible-first principle and the ATM connection, greedy-then-search, the motor jam, and the float
   arithmetic.

3. *Do you dispense the item or the change first?*
   Neither — verify first. Then the general rule, the ATM comparison, and the concrete failure if you
   get it backwards.

---

## Before you move on

- [ ] I can say the four lines as a four-word phrase without thinking.
- [ ] I can state what is lost by swapping lines 1 and 2, with the output.
- [ ] I know why `previous` starts as `None` and what two jobs that does.
- [ ] I returned `head` on purpose and saw the one-element list.
- [ ] I wrote the recursive version blind and can explain both magic lines.
- [ ] I deleted `head.next = None` and saw the cycle.
- [ ] I can quote the `RecursionError` and say why raising the limit is not a fix.
- [ ] I wrote `reverse_between` and got stuck once by not capturing the tail first.
- [ ] I wrote `reverse_k_group` with the count check in the wrong place, then fixed it.
- [ ] I used reversal to solve palindrome in O(1) space, and restored the list.
- [ ] I can state the reversible-first rule and apply it to both the ATM and the vending machine.
- [ ] I can name the three refusals that stay in `Collecting` and say why none is a failure.
- [ ] I worked the ₹22-versus-₹25 example and can say what it proves about the lamp.
- [ ] I can explain escrow and why real machines use it.
- [ ] I computed the stock lifetime and the float lifetime and can quote the gap.
- [ ] I answered all three questions above out loud.
