---
day: 77
track: practice
title: "Practice — Stacks and queues revision and mock round"
status: written
---

# Day 077 · Practice

**DSA topic:** Stacks and queues revision and mock round
**System design topic:** How to run a low-level design interview: the forty-minute script

---

## Code these, in this order

One rule for the whole set: **solve each one out loud, standing up, on a clock.** Twenty-five minutes
each, narrating. If you go silent for more than fifteen seconds, that is the thing to fix, not the
code.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Simplify Path | LeetCode 71 (Medium) | Recognising a stack in a problem that never says "stack", and the `..` versus `...` trap. |
| 2 | Basic Calculator II | LeetCode 227 (Medium) | The stack holding "the context I am leaving", and precedence without recursion. |
| 3 | Remove K Digits | LeetCode 402 (Medium) | A monotonic stack used for construction rather than for lookup, plus three edge cases. |
| 4 | Design Hit Counter | LeetCode 362 (Medium) | "The last 300 seconds" as a queue, and the follow-up about a very large hit rate. |

### On every one of these, run the script

Restate. Ask about duplicates, `n`, and the empty input. State the brute force with a number. Say
what the structure holds *before* the loop. Trace a degenerate example. Give the complexity with the
counting. Do this even alone in your room — especially alone in your room.

### On problem 1, find the traps yourself

Before running it, list every input you think will break your solution. `"/../"`, `"/home//foo/"`,
`"/a/./b/../../c/"`, `"/..."`. Then run them. The `"..."` one is the classic: it is a legal directory
name, and `startswith("..")` treats it as a parent.

### On problem 3, say what the stack holds

It is not "elements whose answer is unknown" this time. It is "the answer so far, kept as small as
possible". Say that sentence, then handle the three edge cases: `k` not fully used at the end, leading
zeros, and an empty result.

### On problem 4, do the follow-up honestly

"What if there are hundreds of hits per second?" The exact queue holds every timestamp. Say what you
would keep instead, and what precision you are giving up to get O(1) memory.

---

### The recognition drill

For each, say in five seconds which of the four trigger sentences applies, and name the structure:

1. Whether a string of brackets is balanced.
2. The maximum in every window of size k.
3. How many days until a warmer temperature.
4. Print a tree level by level.
5. Get the minimum of a stack in O(1).
6. The number of requests in the last 300 seconds.
7. The largest rectangle in a histogram.
8. The shortest path in an unweighted grid.
9. Evaluate an expression with brackets.
10. A cache that evicts the least recently used entry.
11. Decode `3[a2[c]]`.
12. Implement a queue with only stacks.

Then group all twelve under the four trigger sentences and say which sentence covers the most.

### The say-it-first drill

For each, write the single sentence you would say *before* writing any loop:

1. Balanced brackets.
2. Next greater element.
3. Largest rectangle in a histogram.
4. Sliding-window maximum.
5. Min stack.
6. LRU cache.
7. Queue from two stacks.
8. Rate limiter over a rolling window.

Every sentence should start with "the stack holds", "the deque holds", "the map answers … and the
list answers …", or "each element is touched …".

### The complexity-defence drill

Say each answer out loud, five times, until it is automatic:

1. "There is a loop inside a loop. Is that not O(n²)?"
2. "Pop can move n elements. How is that O(1)?"
3. "You loop 2n times for the circular version."
4. "Your rate limiter has a `while` inside `allow`."
5. "Your LRU `put` calls three helper methods."

Each answer must contain a count, not an assertion.

### The number-recall drill

Quote each from memory, then check:

1. `list.pop(0)` versus `deque.popleft`, draining 100,000 elements.
2. What happened when n doubled from 100,000 to 200,000, and what that proves.
3. Brute force, heap and deque for sliding-window maximum at n = 200,000, k = 1,000.
4. Monotonic stack against brute force at n = 100,000.
5. `queue.Queue` against `deque` in a single thread.
6. Bytes per entry in a Python LRU cache, and the total for 100,000 entries.

### The break-it drill, phase-wide

Trigger each and record the exact error text or the wrong output:

1. `pop(0)` in a queue solution, timed at n = 200,000.
2. A `while` condition with no `stack and`.
3. `is_empty` checking one of the two stacks.
4. Pouring onto a non-empty outbox.
5. `head == tail` used as "empty" on a full ring buffer.
6. `width = index - left` in the histogram.
7. An LRU `get` that does not reorder.
8. Removing from the list but not the map.
9. Recording a rejected request in the rate limiter.
10. `window[0] < index - k` on `[8, 3, 2]` with k = 2.

### The mock round

Set a timer for forty-five minutes. Pick two problems you have never seen from the stack-and-queue
tag on LeetCode. Solve both out loud, recording yourself if you can bear it. Then, listening back,
mark every place where you:

- wrote code before saying what the structure held,
- said a complexity without counting,
- went quiet for more than fifteen seconds,
- fixed a bug the interviewer would have found first.

Those four marks are your actual practice list. The problems were only the excuse.

---

### The script drill

Run all six moves, out loud, on each of these, in eight minutes each. Do not write code — only speak.

1. Design a parking lot.
2. Design a vending machine.
3. Design a library management system.
4. Design a deck of cards.

For each, say: the four clarifying questions, the scope exclusions, the nouns with one-line
responsibilities, and — most importantly — **the one interesting part**.

### The interesting-part drill

For each prompt, name the single place where the design is actually decided, and the second
implementation you would show:

1. Parking lot.
2. Elevator system.
3. ATM.
4. Vending machine.
5. Library management.
6. Tic-tac-toe.
7. Splitwise.
8. BookMyShow.
9. Food delivery.
10. Ride hailing.
11. Rate limiter.
12. In-memory cache.
13. Logging framework.

Two of the thirteen have a state machine as their interesting part. Name them, and say what you would
draw before the class diagram in those two cases.

### The interface-gate drill

For each proposed interface, say whether you would build it, and name the second implementation or
admit you cannot:

1. `SpotAllocation` in a parking lot.
2. `TicketFactory` in a parking lot.
3. `PricingPolicy` in a parking lot.
4. `VehicleRepository` in a parking lot.
5. `ShuffleStrategy` in a deck of cards.
6. `EvictionPolicy` in a cache.
7. `WinCondition` in tic-tac-toe.
8. `Formatter` in a logging framework.

Three of the eight fail the gate. Name them and say the one-sentence rule that rejects them.

### The concurrency drill

For each, describe the two-step operation, the size of the window between the steps, the failure it
produces, and both fixes:

1. Two cars at the barrier, one free spot.
2. Two users clicking the same seat.
3. Two workers shipping the same order.
4. Two threads calling `get` on the same LRU cache.
5. Two customers taking the last item from a vending machine.

For each, say whether a lock or a conditional update is the better answer, and why.

### The over-engineering drill

Take your parking lot design and deliberately ruin it. Add `ParkingLotFactory`,
`AbstractTicketBuilder`, `SpotAllocationStrategyRegistryProvider` and an observer for every event.
Then:

1. Count the classes and the files.
2. Count the hops from "a car arrives" to "a spot is chosen".
3. Write the sentence a reviewer would write on this pull request.
4. Delete everything that fails the interface gate and count what is left.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Two problems, no hints, talk as you go.*
   Run the whole script on an unseen stack problem: restate, clarify three things, brute force with a
   number, the observation before the structure, what the structure holds, the code narrated, a
   traced degenerate example, and the complexity with the counting.

2. *Design a parking lot. You have forty minutes. Begin.*
   The shape announced in the first thirty seconds, four clarifying questions whose answers change
   the design, assumptions and scope exclusions, nouns with one-line responsibilities, version one
   and what breaks it, the interface with two implementations, and concurrency raised before it is
   asked.

3. *There is a loop inside a loop. Is that not O(n²)?*
   n pushes total, each element popped at most once, ≤ 2n operations, bounded in total not per
   iteration, plus the example where one iteration pops a hundred thousand elements and why it costs
   nothing.

---

## Before you move on

- [ ] I can name all four trigger sentences and classify twelve problems with them.
- [ ] I can say what the structure holds, in one sentence, for eight different problems.
- [ ] I can give all five complexity defences with a count rather than an assertion.
- [ ] I can quote six real measurements from the phase from memory.
- [ ] I triggered all ten phase traps and recorded the exact error text.
- [ ] I ran a timed forty-five-minute mock on two unseen problems, out loud.
- [ ] I listened back and marked the four failure types.
- [ ] I can name the six moves of the LLD script and their minute budgets.
- [ ] I ran the script out loud on four different prompts.
- [ ] I can name the interesting part of thirteen standard prompts.
- [ ] I can state the interface gate and apply it to eight proposed interfaces.
- [ ] I can raise concurrency unprompted, with a window size and both fixes.
- [ ] I over-engineered a design on purpose and can say exactly what a reviewer would object to.
- [ ] I answered all three questions above out loud.
