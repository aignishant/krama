---
day: 79
track: practice
title: "Practice — Traversal, insertion, and deletion"
status: written
---

# Day 079 · Practice

**DSA topic:** Traversal, insertion, and deletion
**System design topic:** Design an elevator system

---

## Code these, in this order

One rule for the whole set: **say "stand at k−1, act on k" before every single operation.** If your
walk loop runs `range(index)` when it should run `range(index - 1)`, you will delete the wrong node
and the tests will pass on three inputs out of four.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Middle of the Linked List | LeetCode 876 (Easy) | The plain traversal loop, and whether you can state the two-answer ambiguity for even lengths before coding. |
| 2 | Design Linked List | LeetCode 707 (Medium) | Every boundary at once: index 0, index size, index out of range, empty list, single element. |
| 3 | Remove Linked List Elements | LeetCode 203 (Easy) | Look-one-ahead, consecutive matches, and the leading run that makes the head case a *loop*, not an `if`. |
| 4 | Insert into a Sorted Circular Linked List | LeetCode 708 (Medium) | The walk that has no `None` to stop it, and the all-equal-values case that hangs. |

### On problem 2, write the six boundary tests first

`addAtIndex(0, x)` on an empty list. `addAtIndex(size, x)`. `addAtIndex(size + 1, x)`.
`deleteAtIndex(0)` on a one-element list. `deleteAtIndex(size - 1)`. `deleteAtIndex(size)`. Write
those, watch them fail, then implement.

### On problem 3, break it on `[7, 7, 7]`

Write the loop that advances `previous` after every iteration, including after a deletion. Run it on
`[7, 7, 7]` with `val = 7` and write down what comes out. Then say in one sentence why you must not
advance after removing.

### On problem 4, find the input that hangs

A circular list has no `None`, so your loop needs a different stopping condition. Run it on a list
where every value is the same and the insert value is different. If it hangs, you have found the case
the problem exists for.

---

### The rule drill

Answer each without looking:

1. State the rule that generates traversal, insertion and deletion, in one sentence.
2. Why can you not unlink a node you are holding?
3. How many steps do you walk to delete index `k`?
4. Write the deletion in one assignment.
5. Write the insertion in one assignment, and say which half is built first and why.
6. Name the three boundary cases and say what makes each one different.

### The bounds drill

1. How many valid positions does insertion have on a list of length `n`?
2. How many does deletion have?
3. Write both bounds checks and say which uses `>` and which uses `>=`.
4. What must happen before any dereference, and what is the error text if it does not?
5. Which single character separates a working `insert_at(size, x)` from one that raises?

### The head-case drill

1. Write `delete_at(0)` for a bare function taking a head and returning something.
2. Call it and discard the return value. Print the list. Explain the result in terms of how Python
   passes arguments.
3. Now write it as a method on a class. Say what changed and why the bug is no longer available.
4. Write `delete_at(0)` on a one-element list and say which two pieces of bookkeeping must change.

### The bookkeeping drill

1. Add `_size` to a bare linked list and list every method that must update it.
2. Add `_tail` and list every method that must update it.
3. Name the one deletion that must move the tail *backwards*, and say why it is O(n) anyway.
4. Write `_check` with three assertions. Say what each one catches.
5. Delete the tail update from `delete_at`, then append and print. Describe what you see, and note
   that there is no error.

### The break-it drill

Trigger each and record the exact output or error text:

1. Walk `range(index)` instead of `range(index - 1)` in `delete_at`. Run it on `[7, 3, 9, 4, 8]` with
   `k = 2` and say which value disappeared.
2. Call `_node_at(index - 1)` with `index = 0` and no head case. Quote the error, or describe the
   silent wrong behaviour if you did not guard.
3. Use `>=` instead of `>` on the insert bound and call `insert_at(size, x)`. Quote the error.
4. Write `while previous.next.value != target` with the target absent. Quote the error.
5. Assign `previous.next = new` before `new.next = previous.next`. Traverse and describe the failure.
6. Delete the only node without clearing `_tail`, then append twice. Print the list.
7. Forget `self._size -= 1` in `delete_at`, then call `value_at(size - 1)`. Describe what happens.

### The quadratic drill

1. Write `append` without a tail reference.
2. Build a list of 100,000 elements with it and time it.
3. Add the tail reference and time it again.
4. State both complexities and the arithmetic for the slow one.
5. Say which other operation in this class has the same shape of hidden cost.

### The comparison drill

For each operation, give the complexity for a linked list and a Python list, and say which wins:

1. Insert at the front.
2. Delete at the front.
3. Insert at the end.
4. Delete at the end.
5. Insert in the middle at a known index.
6. Access by index.
7. Length.

For number 5, both are O(n). Say what each one is actually spending its time on, and which is faster
in practice.

---

### The two-decisions drill

1. State the two scheduling decisions in an elevator system, and say which is system-level and which
   is per-car.
2. Say what a hall call carries that a car request does not.
3. Say why that difference means the system, not the car, chooses for a hall call.
4. Give one sentence for why merging the two decisions is the standard mistake.

### The algorithm drill

Take a car on floor 1 with pending stops at 2, 9, 3, 8, 4 in that arrival order.

1. Compute the total floors travelled under first-come-first-served.
2. Compute it under nearest-first.
3. Compute it under LOOK.
4. Convert all three to seconds at two seconds a floor.
5. Construct a request stream where nearest-first starves floor 9, and say how long it waits.
6. Say why LOOK cannot starve, structurally rather than with a timeout.
7. Name the strict variant that runs to the very top before turning, and one other system that uses
   the same algorithm.

### The two-sets drill

1. Say why a car keeps `up_stops` and `down_stops` rather than one set.
2. Give a concrete floor that appears in both and explain what it means.
3. Write `next_stop` for the going-up case in four lines.
4. Write the turn condition, and say what floor you go to when you turn.
5. Say how `press_floor` decides which set to use, and name the one case where that inference is
   wrong.

### The estimation drill

Compute each from scratch, showing the multiplication:

1. Round-trip time in up-peak: ten floors, six stops, express return.
2. People per hour for three cars.
3. Demand in people per hour for 400 arrivals in 30 minutes.
4. Headroom, as a percentage.
5. Average wait, and whether it is acceptable.
6. Total system state in bytes.

Then say which number tells you "there is nothing to scale here" and which tells you whether to buy a
fourth lift.

### The dispatch drill

1. Write the score function with its three cases.
2. Explain the `approaching` expression in one sentence, including why multiplying by the direction
   value works for both directions.
3. Say what the penalties are and, honestly, where their values come from.
4. Write the zoned dispatcher and say why it needs a fallback.
5. Say why the dispatcher gets an interface and the stop ordering does not.

### The failure drill

For each, say what happens and what you would add:

1. Five people on floor 4 press "up".
2. A car is full and a hall call arrives on a floor it is passing.
3. A car is full and one of its own passengers wants floor 7.
4. Car 1 is assigned a call on floor 5, then car 2 becomes idle on floor 4.
5. A car stops responding entirely.
6. The fire alarm goes off.
7. Someone presses floor 3 from inside while the car is at floor 3 with the doors open.

Two of the seven are legal or safety requirements rather than optimisations. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Delete the node at position k. What if it is the head?*
   The stand-at-k−1 rule and why you cannot reach backwards, the one-assignment unlink, the head as a
   *different* operation rather than a harder one, returning the new head and why the bug is silent,
   the different bounds for insertion and deletion, and the size and tail bookkeeping with the stale
   tail named.

2. *Design an elevator system for a ten-storey building with three lifts.*
   The two scheduling decisions separated first, the estimate before the classes, the two stop sets,
   LOOK justified against FCFS and nearest-first with floor counts and the word starvation, dispatch
   behind an interface with two implementations, and idempotent hall calls raised unprompted.

3. *What is wrong with always sending the nearest lift?*
   Starvation, with the concrete request stream that causes it, why it shows up as the top floor
   complaining, and how LOOK removes it structurally rather than with a timeout.

---

## Before you move on

- [ ] I can state the stand-at-k−1 rule and say why reaching backwards is impossible.
- [ ] I can write deletion and insertion each as one assignment, in the right order.
- [ ] I know the three boundary cases and what makes each different.
- [ ] I can say why insertion allows `size + 1` positions and deletion allows `size`.
- [ ] I discarded a return value from a head-changing function and saw nothing happen.
- [ ] I wrote `_check` and used it to catch a stale tail.
- [ ] I deleted the tail update and watched an appended value vanish with no error.
- [ ] I timed 100,000 appends with and without a tail reference.
- [ ] I can give the linked-list-versus-array table from memory.
- [ ] I can separate the two elevator scheduling decisions in one sentence each.
- [ ] I computed FCFS, nearest-first and LOOK travel for the same five stops.
- [ ] I can construct the starvation stream and explain why LOOK is immune.
- [ ] I can explain why the car keeps two stop sets, with a floor that is in both.
- [ ] I did the up-peak estimate and can say whether three lifts are enough and by how much.
- [ ] I can say why the dispatcher has an interface and the stop ordering does not.
- [ ] I answered all three questions above out loud.
