---
day: 78
track: practice
title: "Practice — Nodes and links: pointers without pointers"
status: written
---

# Day 078 · Practice

**DSA topic:** Nodes and links: pointers without pointers
**System design topic:** Design a parking lot

---

## Code these, in this order

One rule for the whole set: **draw the pointers before you write the assignment.** Two boxes, an
arrow, and what the arrow should point at afterwards. Every bug in this phase is an assignment made
before its picture existed.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Delete Node in a Linked List | LeetCode 237 (Medium) | Whether you notice the tail is impossible, and whether you say so before being asked. |
| 2 | Remove Linked List Elements | LeetCode 203 (Easy) | The head as a special case — the exact ugliness day 080 removes. |
| 3 | Design Linked List | LeetCode 707 (Medium) | Every operation in one class, including the index arithmetic that everybody gets wrong once. |
| 4 | Convert Binary Number in a Linked List to Integer | LeetCode 1290 (Easy) | The traversal loop, clean, with an accumulator. Warm-up for the whole phase. |

### On problem 1, say the precondition out loud

Before writing anything: "this is impossible for the tail, because there is no successor whose value
I can steal." Then write it. An interviewer who has to point that out has learned something different
about you than one who hears it first.

### On problem 2, count your special cases

Write it without a dummy head and count how many `if`s exist purely because the first element is
different. Then write down what those `if`s have in common. You will delete all of them on
[day 080](../day-080-dummy-head/README.md), and it lands much harder if you have felt them.

### On problem 3, test the boundaries first

`addAtIndex(0, x)` on an empty list. `addAtIndex(size, x)` — legal, appends. `addAtIndex(size+1, x)` —
illegal, does nothing. `deleteAtIndex` on the head, the tail, and out of range. Write those six tests
before the implementation.

### On problem 4, keep it to one variable

`total = total * 2 + node.value`. No list, no string, no reversal. If you built an intermediate list,
say out loud what you traded — O(n) space for a line of clarity — and whether it was worth it.

---

### The memory-picture drill

Answer without looking:

1. How does a runtime find `numbers[500]` in a Python list? Give the arithmetic.
2. How does it find the 500th node of a linked list? Say why the arithmetic is unavailable.
3. What does a Python variable actually hold?
4. Show two names referring to the same node, then mutate through one and read through the other.
5. Explain cache locality in three sentences, without the word "fast".
6. Why is `Node` with `__slots__` 48 bytes and without it over 300?

### The trade-off drill

For each, say array or linked list, and give the one-sentence reason:

1. Access the 10,000th element.
2. Insert at the front, a million times.
3. Delete a node you were handed by a hash map.
4. Sum every element.
5. Store ten million small integers in as little memory as possible.
6. A queue where both ends are used.
7. The recency order inside an LRU cache.
8. Binary search over sorted data.

Two of the eight are the *only* honest wins for a linked list. Name them.

### The qualifier drill

Say the full, honest complexity for each, with the qualifier included:

1. Insert into a linked list.
2. Delete from a linked list.
3. Insert into an array.
4. Delete from an array at a known position.
5. Find the length.
6. Access by index.

For 1 and 2, any answer that does not contain the words "given the node" is wrong.

### The break-it drill

Trigger each and record the exact output or error text:

1. Walk the list using the `head` parameter itself, then try to use `head` afterwards.
2. Write `node.next = new_node` before `new_node.next = node.next`. Then traverse. Describe what
   happens and how long it takes to happen.
3. Write `while node.next.value != target` on a list where the target is absent. Quote the error.
4. Delete the first element with a loop that starts at `head.next`. Print the list.
5. Call `push_front(head, 5)` and discard the return value. Print the list.
6. Set `last.next = head` and call `to_values`. Describe the failure.
7. Call `delete_this_node` on the tail. Quote the error, then say why the operation is impossible in
   principle rather than merely unimplemented.

### The measurement drill

Reproduce all four on your own machine and write the numbers down:

1. Summing a million-element list against a million-node chain. State the ratio.
2. 100,000 `list.insert(0, x)` against 100,000 front pushes onto a chain. State the ratio.
3. `sys.getsizeof` on a `Node` with and without `__slots__`.
4. Bytes per element in a Python list of a million integers.

Then say which of the four is an asymptotic difference and which three are constant factors.

### The build-it drill

Write, from an empty file and without looking:

1. `Node`.
2. `from_values` and `to_values`.
3. `length`, `value_at`, `find`.
4. `push_front`, `insert_after`, `delete_after`.
5. `delete_value`, including the head case.

Then run every one of them on the empty list, a one-element list, and a two-element list. Three of
the nine functions have a bug on at least one of those. Find them.

---

### The script drill

Run the six moves on the parking lot, out loud, in forty minutes, with a timer. Then check yourself:

1. Did you announce the shape in the first thirty seconds?
2. Were all four clarifying questions ones whose answers change the design?
3. Did you state scope exclusions?
4. Did you do the estimate *before* the class diagram, and did it change any decision?
5. Did you say version one and what breaks it, before showing the interface?
6. Did you write two implementations, or one?
7. Did you raise concurrency yourself, with a number?

### The estimation drill

Compute each from scratch, showing the multiplication:

1. Memory for 1,000 spots, 5 floors, 1,000 tickets and 1,000 vehicles.
2. Vehicles per day at a three-hour average stay over a sixteen-hour day.
3. Events per second, average and at a peak of twenty times average.
4. The worst-case allocation scan in microseconds, at 1,000 spots and at 50,000.
5. The collision rate per day from a 151-microsecond window at four arrivals a second.
6. The rupee cost of a one-minute billing error on every ticket, per year.

Then say which single number told you "one lock is enough" and which told you "at fifty thousand
spots, stop scanning".

### The policy-versus-bookkeeping drill

For each, say whether it belongs in `Floor`, in `Spot`, in `ParkingLot`, or in a policy class:

1. Which spots of exactly this size are free.
2. Whether a car may use a bus bay.
3. Whether this spot currently holds a vehicle.
4. How much a three-hour stay costs.
5. Whether the first fifteen minutes are free.
6. Which floor a vehicle should be sent to.
7. Whether a spot is already occupied when you try to claim it.
8. What the display board shows.

Two of the eight are the classic mistakes — rules put into bookkeeping classes. Name them.

### The extension drill

For each new requirement, say which classes change and how many:

1. Electric-vehicle charging bays.
2. Monthly pass holders who get reserved bays.
3. A second entrance on the other side of the building.
4. Sunday rates that are double.
5. Reservations made a day in advance.
6. Spots that are wide but low, suitable for cars but not vans.
7. A lost ticket.

Two of the seven cannot be absorbed by this design without changing its shape. Name them and say what
shape they need instead.

### The concurrency drill

1. Write the two-step operation that races, with both steps named.
2. State the window in microseconds and the collisions per day.
3. Write the single-process fix, and say where the lock goes and why not around each step.
4. Write the cross-process fix as SQL.
5. Say what `Spot.assign` raising achieves that the lock does not.
6. Say what changes if you shard the lock per floor, and what new hazard that introduces.

### The over-engineering drill

Add `ParkingLotFactory`, `AbstractTicketBuilder`, an observer per event, and a
`SpotAllocationStrategyRegistryProvider` to your design. Then:

1. Count classes, files and hops from "a car arrives" to "a spot is chosen".
2. Apply the interface gate to every interface you now have and delete the ones that fail.
3. Write the one sentence you would say if an interviewer asked "is this over-engineered?"

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *What is a linked list, and when is it better than an array?*
   The contiguous-versus-scattered difference and the arithmetic it enables, both consequences, the
   "given the node" qualifier said explicitly, the four honest wins with the LRU cache first, and the
   two costs with real numbers — six times the memory, twice the traversal time, and cache locality
   as the reason.

2. *Design a parking lot. Multiple floors, multiple vehicle types.*
   The shape announced, four clarifying questions, the estimate that justifies one lock and no
   database, seven classes with one-line responsibilities, version one and what breaks it, the
   allocation interface with two implementations, the fallback rule placed in policy not bookkeeping,
   and the race raised with a number.

3. *Delete a node given only that node.*
   Copy the successor's value, unlink the successor, say that it is impossible for the tail and why,
   and note that it breaks any outside reference to the successor.

---

## Before you move on

- [ ] I can explain how an array finds element `i`, and why a linked list cannot.
- [ ] I can say what a Python variable holds, and demonstrate two names for one node.
- [ ] I never state linked-list insertion complexity without the words "given the node".
- [ ] I can name the four honest cases for a linked list, LRU cache first.
- [ ] I reproduced all four measurements myself and know which are constant factors.
- [ ] I triggered the wrong-order relink and watched a node point at itself.
- [ ] I discarded a `push_front` return value and saw nothing happen, with no error.
- [ ] I wrote all nine functions from scratch and tested them on lists of length 0, 1 and 2.
- [ ] I counted the head special cases in `delete_value` and can say what they have in common.
- [ ] I ran the full six-move script on the parking lot against a timer.
- [ ] I did the estimate before the diagram and can say which decisions it changed.
- [ ] I can sort eight rules into bookkeeping and policy without hesitating.
- [ ] I can say which two extensions this design cannot absorb, and what they need instead.
- [ ] I can state the race, the window, the collisions per day, and both fixes.
- [ ] I answered all three questions above out loud.
