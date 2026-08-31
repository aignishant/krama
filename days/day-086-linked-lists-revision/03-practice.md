---
day: 86
track: practice
title: "Practice — Linked lists revision and mock round"
status: written
---

# Day 086 · Practice

**DSA topic:** Linked lists revision and mock round
**System design topic:** Design BookMyShow

---

## Code these, in this order

One rule for the whole set: **diagnose before you repair.** Say which two or three techniques the
problem is made of, out loud, before typing anything. If you cannot name them, name the O(n)-space
baseline instead and improve from there.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Odd Even Linked List | LeetCode 328 (Medium) | Two builder chains at once, and terminating both — the simplest composite. |
| 2 | Copy List with Random Pointer | LeetCode 138 (Medium) | The map baseline, then the interleaving trick, and restoring the original. |
| 3 | Reorder List | LeetCode 143 (Medium) | Runner + reverse + interleave. Three techniques, no new idea. |
| 4 | Sort List | LeetCode 148 (Medium) | First middle, the cut, and the quicksort question you will be asked. |

### On every one, run the six questions first

Can the first node change? Do I need a position I cannot count to? Might it not end? Am I turning
arrows around? Am I combining or ordering? Do I already hold the node? Thirty seconds, out loud, before
the first keystroke.

### On problem 1, count your terminations

Two chains being built means two `next = None`s at the end, and forgetting either one builds a cycle.
Print the result; if it never returns, you found it.

### On problem 2, do both versions

The map version first, because it is the honest baseline and you should always say it. Then the
interleaving version, and then check that the *original* list still has its `next` and `random`
pointers exactly as they were.

### On problem 4, prepare the answer before you are asked

"Why merge sort and not quicksort?" is coming. Two sentences: no random access for the partition, and
merging lists needs no scratch space where merging arrays does.

---

### The six-questions drill

For each problem, name the technique or techniques in under ten seconds:

1. Remove every node with value 7.
2. Return the middle node.
3. Is this list a palindrome, in O(1) space?
4. Does this list have a cycle, and where does it start?
5. Reverse the nodes in groups of three.
6. Merge k sorted lists.
7. Design an LRU cache.
8. Remove the 3rd node from the end.
9. Reorder the list into first, last, second, second-last.
10. Copy a list with random pointers.
11. Flatten a multilevel doubly linked list.
12. Sort a linked list.

Four of the twelve need two or more techniques. Name them and their parts.

### The five-sentences drill

Say each aloud, five times, then use each in a sentence about a specific problem:

1. To change the list at position k, stand at k−1.
2. Save the next node before you overwrite the pointer.
3. Return `dummy.next`, never `head`.
4. Insertion is O(1) *given the node*.
5. Advance only when you keep.

### The error-message drill

For each error, name at least two distinct causes from this phase:

1. `AttributeError: 'NoneType' object has no attribute 'next'`
2. `RecursionError: maximum recursion depth exceeded`
3. `TypeError: '<' not supported between instances of 'Node' and 'Node'`
4. No error at all — the program hangs.

The fourth has three causes. Name all three.

### The break-it drill, phase-wide

Trigger each and record the exact output or error text:

1. Overwrite `current.next` before saving it, in a reversal. Run `[1,2,3]`.
2. Return `head` after a reversal.
3. Discard the return value of a function that changes the head.
4. Handle a run of leading matches with an `if` instead of a dummy. Run `[7,7,7,1]`.
5. Advance after a deletion. Run `[1,7,7,2]`.
6. Split at the second middle in a merge sort. Run `[1,2]`.
7. Omit the cut in a split. Run anything.
8. Return the meeting point as a cycle start. Run a list that is entirely one cycle, then one with a
   tail.
9. Update one direction only in a doubly linked list, then walk backwards.
10. Leave a built list unterminated. Print it.

### The mock round

Set a timer for forty-five minutes. Pick two problems you have never seen from the linked-list tag.
Solve both out loud. Then mark every place where you:

- wrote code before naming the techniques,
- assigned a pointer before drawing what it should point at,
- skipped the empty, one-node or two-node case,
- mutated the caller's list without saying so.

Those four marks are the practice list. The problems were the excuse.

### The read-only drill

For each, say whether the operation is allowed to modify the input, and what you would do if not:

1. Reverse the list.
2. Check whether it is a palindrome.
3. Detect a cycle.
4. Find the middle.
5. Copy a list with random pointers.
6. Sort the list.

Two of the six are commonly implemented in a way that damages the input while returning the right
answer. Name them.

---

### The two-things drill

1. Say why a seat is two classes, in one sentence.
2. List three fields for each class.
3. Say which one the seat map queries and which one you lock.
4. Say what goes wrong if you lock the other one.
5. Name two other domains from this course with the same split.

### The race drill

1. Write the check-then-act version and describe the interleaving that breaks it.
2. Write the conditional `UPDATE` that fixes it.
3. Say what the affected row count means, in both cases.
4. Compute the collisions per second at 3,000 attempts, a 2 ms window and 200 seats.
5. Say why this is the same pattern as the parking spot and the shipped order.

### The all-or-nothing drill

1. Write the four-seat claim as one statement.
2. Write it as four statements and describe the failure with two concurrent users.
3. Say what the affected count must equal, and what happens otherwise.
4. Say when lock ordering matters and what it prevents.

### The expiry drill

1. Describe lazy expiry and where the condition lives.
2. Describe the sweeper approach.
3. Say which one correctness depends on, and why that is the better choice.
4. Say what the sweeper is still for.
5. Choose a hold duration and defend it with two numbers.

### The payment drill

1. Write the confirming update with its conditional clause.
2. Delete the clause and describe the worst-case failure in the whole system.
3. Say what happens when the confirm affects zero rows.
4. Say which earlier lesson this failure is a copy of.

### The scale drill

Compute each, showing the multiplication:

1. ShowSeat rows per day, and bytes.
2. Reads and writes per second on a blockbuster's seat map.
3. The read-to-write ratio, normal and at peak.
4. The size of every seat map in the country, in cache.
5. Dead inventory at a 20 percent abandonment rate with a ten-minute hold.

Then say which number tells you to cache the map, and which tells you that sharding will not help.

### The trade-off drill

For each, give the trade in one sentence and say which side you would pick:

1. Lock in the database versus lock in Redis.
2. Five-minute hold versus fifteen-minute hold.
3. Cached seat map versus always-fresh seat map.
4. Sweeper-based expiry versus lazy expiry.
5. Sharding by show versus a virtual waiting room.

One of the five has an answer that is wrong in both directions until you add a qualifier. Name it.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Two problems, no hints, talk as you go.*
   Run the six trigger questions on an unseen problem, name the techniques it is made of, draw the
   pointers, code narrating the two rules that matter, trace the degenerate case, and give the
   complexity with the counting and the space including whether you mutated the input.

2. *Design BookMyShow. Two users click the same seat at the same moment.*
   The `Seat`/`ShowSeat` split first with the one-sentence payoff, the three states with both arrows
   out of LOCKED, the conditional claim as one statement with the row-count check and the collisions
   number, all-or-nothing, lazy expiry, the conditional confirm with the automatic refund, and cache
   the map but never the claim.

3. *Why a linked list rather than an array?*
   O(1) insertion and deletion **given the node**, the LRU case where a hash map hands you the node,
   the front-insertion measurement, and the honest costs — six times the memory and twice the traversal
   time.

---

## Before you move on

- [ ] I can name all six trigger questions and apply them in ten seconds.
- [ ] I can say the five sentences without hesitating.
- [ ] I can give two causes for each of the four failure signatures.
- [ ] I triggered all ten phase traps and recorded the exact output.
- [ ] I ran a timed forty-five-minute mock on two unseen problems, out loud.
- [ ] I marked the four failure types in my own recording.
- [ ] I always ask whether I may modify the input list.
- [ ] I wrote both versions of the random-pointer copy and confirmed the original survived.
- [ ] I can say why a seat is two classes and what breaks if it is one.
- [ ] I can write the conditional claim and say what the row count means.
- [ ] I can compute the double-sold seats per second for the naive version.
- [ ] I can explain lazy expiry and why correctness should not depend on a scheduler.
- [ ] I can write the conditional confirm and name the failure it prevents.
- [ ] I can say which number justifies caching the map and which says sharding will not help.
- [ ] I can defend a ten-minute hold with two numbers.
- [ ] I answered all three questions above out loud.
