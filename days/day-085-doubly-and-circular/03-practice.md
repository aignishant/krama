---
day: 85
track: practice
title: "Practice — Doubly and circular linked lists"
status: written
---

# Day 085 · Practice

**DSA topic:** Doubly and circular linked lists
**System design topic:** Design Splitwise

---

## Code these, in this order

One rule for the whole set: **after every operation, walk the list both ways and compare.** A doubly
linked list can be correct forwards and broken backwards, and nothing else will tell you.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Design Linked List | LeetCode 707 (Medium) | Do it doubly this time. Every boundary, twice as many pointers. |
| 2 | Design Browser History | LeetCode 1472 (Medium) | A cursor in a doubly linked list, and truncating the forward chain on a new visit. |
| 3 | Flatten a Multilevel Doubly Linked List | LeetCode 430 (Medium) | Splicing a whole sublist in, with both directions maintained at three joints. |
| 4 | LRU Cache | LeetCode 146 (Medium) | Build it again, and this time say the one-sentence justification before writing a line. |

### On problem 1, write `_check` before anything else

Walk forwards collecting values, walk backwards collecting values, assert one is the reverse of the
other and that the length matches the stored size. Then call it after every single operation in your
tests. It will find bugs you would otherwise spend an hour on.

### On problem 2, notice what the `prev` pointer is for

Back and forward are the two directions. Then answer: when the user visits a new page after going
back, what happens to everything ahead of the cursor, and which pointer has to change?

### On problem 3, count the joints

Splicing a child list in means three places where links must be fixed, and each needs both directions.
Draw all six assignments before writing any of them.

### On problem 4, say the sentence first

"The map gives me the node in O(1); unlinking must also be O(1), and reaching the predecessor from a
node is exactly what `prev` buys." Say it, then write the code.

---

### The one-thing drill

1. State, in one sentence, the only operation the second pointer buys.
2. Write the two assignments that remove a node.
3. State the same operation's cost in a singly linked list, and why.
4. Give the LRU number: capacity 100,000, cost per read, both ways.
5. State the general rule about when a doubly linked list is worth it.

### The ordering drill

1. Write the four insertion assignments in the correct order.
2. Write them in the wrong order and trace what `fresh.next` ends up being.
3. Say the habit that makes the ordering bug impossible.
4. Rewrite `insert` to take both neighbours as parameters and say why that helps.

### The half-correct drill

1. Write a removal that updates only the forward links.
2. Iterate forwards and print. Confirm it looks right.
3. Print `len`. Confirm it looks right.
4. Now walk backwards and describe what you find.
5. Say why this failure mode does not exist in a singly linked list.
6. Write `_check` and confirm it catches it.

### The break-it drill

Trigger each and record the exact output or error text:

1. Remove a node with only one direction updated, then `pop_back`.
2. Insert with `left.next = fresh` written first.
3. Remove the first node with no sentinels. Quote the error.
4. Traverse a circular list with `while node is not None`.
5. Iterate a circular list without skipping the sentinel. Describe the extra element.
6. Remove a node and leave its `prev` and `next` set, then walk from it.
7. Call `remove(5)` where 5 is a value rather than a node. Say what the O(1) guarantee actually
   requires.

### The circular drill

1. Draw a circular doubly linked list with one sentinel.
2. Write the emptiness test.
3. Write `sentinel.next` and `sentinel.prev` in words.
4. Say how many `None`s appear in the structure, and what that buys.
5. Write a correct traversal and say what makes it terminate.

### The Josephus drill

1. Simulate n = 7, k = 3 by hand and write the elimination order.
2. Run your implementation and confirm the survivor.
3. State the simulation's time and space.
4. Write the closed-form recurrence and say its time and space.
5. Say which you would give in an interview and why you would mention both.

### The cost drill

1. Bytes per node, singly and doubly, with `__slots__`.
2. The percentage overhead, and the absolute at 10 million nodes.
3. Writes per removal and per insertion, both structures.
4. Name the cost that does not appear in any table.
5. Name three cases where you would *not* use a doubly linked list.

### The real-world drill

For each, say what structure it is and what the second pointer buys:

1. `collections.deque`
2. `OrderedDict`
3. The Linux kernel's `list_head`
4. A browser's back and forward buttons
5. A music player on repeat
6. An LRU cache

---

### The money drill

1. Say why money is never a float, in one sentence about binary.
2. Split ₹1,000 three ways in paise and show the remainder.
3. Write the deterministic assignment and say why determinism matters.
4. Write the assertion and say what it prevents.
5. Compute the platform-wide leak at 50 million expenses.

### The ledger drill

1. Write the ledger entries for "Sandeep pays ₹11,400 for a room shared equally by 6".
2. Confirm they sum to zero and say why that matters.
3. Say what is stored and what is derived, and which one wins in a disagreement.
4. Say why the balance is materialised anyway, with the millisecond figure.
5. Describe the reconciliation job in one sentence.

### The simplification drill

Given balances Sandeep +9,500, Meera +1,800, Ravi +50, Anjali −2,300, Vinod −4,600, Kiran −4,450:

1. Confirm they sum to zero.
2. Run the greedy by hand and write out every settlement.
3. Count them and compare with `k − 1`.
4. Count the possible pairs for six people.
5. Say why every payment zeroes at least one person.
6. Construct a balance set where a zero-sum subset exists, and say what the optimal is.
7. State what problem finding the true minimum reduces to, and its complexity.

### The provenance drill

1. State Vinod's complaint in one sentence.
2. Say whether it is a bug, and defend the answer.
3. Say what the design consequence is — what simplification must produce, and what it must not touch.
4. Say why real Splitwise makes it a setting.

### The concurrency drill

1. Write the wrong balance update as read-modify-write in application code.
2. Describe what two concurrent expenses do to it.
3. Write the correct SQL.
4. Say why the ledger being the source of truth limits the damage.
5. Describe how you would handle an *edit* to an existing expense, and why not an update.

### The estimation drill

Compute each, showing the multiplication:

1. Possible pairs for 6, 20 and 50 people, and the settlement bound for each.
2. Total storage for 10M users, 50M expenses and 250M ledger entries.
3. Time to derive one balance for a group with 8 members and 400 expenses.
4. The same for a home screen showing 12 groups.
5. The simplifier's complexity, and the operation count at k = 50.

Then say which single number tells you this is not a scale problem.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Why does an LRU cache use a doubly linked list?*
   The one operation the second pointer buys, the two assignments, the singly linked cost and why,
   the capacity-100,000 comparison, sentinels at both ends, and the honest cost including the
   half-correct failure mode.

2. *Design Splitwise. How do you minimise the number of transactions?*
   Integer paise and the remainder rule with its assertion, the immutable ledger with entries summing
   to zero, balances derived then materialised then reconciled, netting each person, the greedy with
   two heaps, the `k − 1` bound with *why*, the NP-hardness caveat, and provenance as a setting.

3. *Is your debt simplification optimal?*
   At most k−1 and achieved in one pass; not minimal, because zero-sum subsets could be separated;
   that is set-partition and NP-hard; and the practical position on why you would not pay exponential
   time for one payment.

---

## Before you move on

- [ ] I can state the one operation the second pointer buys, in one sentence.
- [ ] I wrote `_check` and used it to catch a one-direction removal.
- [ ] I can write the four insertion assignments in the right order and say why.
- [ ] I traversed a circular list with `while node is not None` and saw it hang.
- [ ] I can state the LRU justification with the capacity-100,000 numbers.
- [ ] I can name three cases where I would not use a doubly linked list.
- [ ] I implemented Josephus by simulation and know the closed form exists.
- [ ] I can say why money is never a float, in terms of binary.
- [ ] I can split ₹1,000 three ways and say where the last paisa goes and why deterministically.
- [ ] I can write the assertion and say what it prevents platform-wide.
- [ ] I can write ledger entries that sum to zero and say why that matters.
- [ ] I ran the greedy by hand on the six-person example and got five settlements.
- [ ] I can say why every payment zeroes at least one person.
- [ ] I can name the NP-hard problem the true minimum reduces to.
- [ ] I can defend "provenance loss is a setting, not a bug".
- [ ] I can write the correct concurrent balance update in SQL.
- [ ] I answered all three questions above out loud.
