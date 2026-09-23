---
day: 73
track: practice
title: "Practice — Queues: first in, first out"
status: written
---

# Day 073 · Practice

**DSA topic:** Queues: first in, first out
**System design topic:** State

---

## Code these, in this order

One rule for the whole set: **never write `pop(0)` again.** If your fingers type it, stop, delete the
line, and say out loud why it is O(n) before you type the replacement.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Number of Recent Calls | LeetCode 933 (Easy) | The simplest real queue: things expire from the front while new ones arrive at the back. |
| 2 | Design Circular Queue | LeetCode 622 (Medium) | The ring buffer, and specifically whether you can tell full from empty. |
| 3 | Binary Tree Level Order Traversal | LeetCode 102 (Medium) | The `for _ in range(len(queue))` trick that separates one level from the next. |
| 4 | Rotting Oranges | LeetCode 994 (Medium) | Multi-source BFS on a grid, where the queue's FIFO order *is* the passage of time. |

### On problem 1, measure it

Solve it once with a list and `pop(0)`, once with a `deque`. Then run 100,000 calls through each and
time both. Write down the two numbers. This is the measurement you will quote in an interview for the
rest of your life, so take it yourself once.

### On problem 2, break full-versus-empty on purpose

1. Implement it with `is_empty` as `head == tail` and no size counter.
2. Fill it to capacity, then call `is_empty`. Write down what it says.
3. Add the size counter and run the same sequence.
4. Now implement the other fix — waste one slot — and say what the usable capacity became.

### On problem 3, look at the one line that matters

`for _ in range(len(queue))` is evaluated once, before the loop body starts adding children. Change it
to `while queue:` and watch the levels merge into one list. Say in one sentence why capturing the
length first is what separates level 2 from level 3.

### On problem 4, say why FIFO is load-bearing

Replace the queue with a stack and run it. The answer will be wrong. Explain, in one sentence, what
property of FIFO makes the number of rounds come out equal to the number of minutes.

---

### The cost drill

Answer each without looking:

1. Why is `list.pop(0)` O(n)? Answer in terms of memory layout, not in terms of "it is slow".
2. Why is `list.append` O(1) but `list.insert(0, x)` O(n)?
3. What is the total cost of draining an n-element list queue with `pop(0)`?
4. What did n = 100,000 and n = 200,000 measure at, and what does the ratio between them prove?
5. What is `collections.deque` internally, and why does that make both ends cheap?
6. When is `queue.Queue` the right answer, and roughly what does it cost when it is not?

### The ring drill

Start with a capacity-5 ring, empty. Apply this sequence and write down `head`, `tail`, `size` and
the slot contents after every single step:

```
 enqueue A, B, C, D, dequeue, dequeue, enqueue E, F, G, dequeue, enqueue H
```

Then answer:

1. At which step does `tail` wrap around?
2. At which step is `tail` less than `head`, and is the queue still valid?
3. Read the queue in order using `(head + i) % capacity` and check it against your working.
4. What happens on the next enqueue, and what are the three reasonable behaviours?

### The break-it drill

Trigger each and record the actual output or error text:

1. `dequeue` from an empty ring with no size check. Quote the error.
2. `dequeue` from an empty `deque`. Quote the error.
3. Implement `is_empty` as `head == tail`, fill the buffer, and call it.
4. Loop with `while head < tail` on a wrapped ring. Say what it reports.
5. Print the ring with `[x for x in items if x is not None]` after a wrap. Compare with the correct
   order.
6. Remove the `items[head] = None` line, push a million large objects through, and watch the memory.
7. Grow the buffer by copying slot-by-slot instead of unrolling from `head`. Find the input where the
   order comes out wrong.

### The when-is-it-a-queue drill

For each, say whether the tool is a stack, a queue, a deque, or none of the three:

1. Undo in a text editor.
2. Print a tree level by level.
3. The shortest path in an unweighted grid.
4. Matching brackets.
5. The maximum of every window of size k.
6. Jobs waiting for a worker, oldest first.
7. The back button in a browser.
8. Requests in the last one second, for a rate limiter.
9. The next greater element for every item.
10. Cards dealt from the top of a shuffled deck.

Two of the ten need both ends. Name them.

---

### The state-machine drill

Draw the order machine from memory — six states, every legal arrow — then answer:

1. How many `(state, event)` pairs exist, how many are legal, and what percentage is refused?
2. Which single arrow goes backwards, and why does a design that forbids backwards arrows break?
3. Which state's `cancel` does extra work, and what is it?
4. Which two states have no outgoing arrows at all?

### The refactor drill

Here is the method, and it has five siblings that look exactly like it:

```python
def cancel(self) -> None:
    if self.status == "placed":
        self.status = "cancelled"
    elif self.status == "paid":
        refund(self.payment_id)
        self.status = "cancelled"
    elif self.status == "shipped":
        raise ValueError("cannot cancel a shipped order")
    elif self.status == "delivered":
        raise ValueError("cannot cancel a delivered order")
```

1. Count the branches across all six methods, and say what adding a seventh state costs.
2. Write the base state class, and say why every method refuses by default.
3. Write `PlacedState` and `PaidState`. Count the lines.
4. Write `Order.cancel`. Count the lines.
5. Add a `Returned` state. Count the files edited, both ways.
6. Now write the same machine as a `(state, event) → state` dictionary. Count those lines too.
7. Say which of the two you would ship for *this* problem, and give the deciding question.

### The state-versus-strategy drill

1. Write a two-implementation Strategy — two pricing rules, chosen by the caller.
2. Write a two-state State machine — draft that promotes itself to submitted.
3. Show both class diagrams. Say what is identical.
4. Point at the one arrow that exists in only one of them.
5. Say the one-sentence rule that tells them apart.
6. Given only an implementation file, name the single line of code that tells you which pattern it is.

### The concurrency drill

Two workers pick up the same paid order at the same instant and both call `ship`.

1. Say exactly what each worker does, step by step, and what the end result is.
2. Say why the state pattern cannot prevent it.
3. Write the conditional `UPDATE` that does prevent it.
4. Say what the worker must do when the update reports zero rows.
5. Give the alternative using a row lock, and say what it costs.
6. Say which you would choose for 500 shipments a second, and why.

### The already-used-it drill

For each, name the states you know and say who owns the transition:

1. A TCP connection.
2. A Stripe `PaymentIntent`.
3. A Kubernetes pod.
4. A pull request on GitHub.
5. An order on any food delivery app.
6. A `Promise` in JavaScript.

One of the six can never go backwards under any circumstance. Name it and say why that matters.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Implement a queue. Why not just use a list and `pop(0)`?*
   FIFO defined by its restriction, the four operations at O(1), the memory-layout reason `pop(0)` is
   O(n), the measured numbers and the doubling test, the head-marker fix and why it leaks, the ring
   buffer with both markers wrapping, the full-versus-empty subtlety flagged before it is asked, and
   `collections.deque` in production but never `queue.Queue`.

2. *Model an order that moves through placed, paid, shipped and delivered.*
   The states and arrows drawn first, the size of the grid and how much of it is illegal, one class
   per state behind one interface with refusal as the default, the one-line delegation and what it
   buys you, the Strategy distinction, persistence as a checked string column, and the conditional
   update for two workers racing.

3. *There is a `while` loop and a queue. Is that not O(n²)?*
   Each element is enqueued once and dequeued once, so the loop body runs `n` times in total, and
   each operation is O(1) because nothing shifts. Then say what would make it O(n²) — `pop(0)` — and
   what that costs at n = 100,000.

---

## Before you move on

- [ ] I can say the four queue operations and their costs without pausing.
- [ ] I can explain why `pop(0)` is O(n) in terms of memory layout.
- [ ] I measured `pop(0)` against `deque.popleft` myself and can quote both numbers.
- [ ] I ran the doubling test and can say what 3.9× proves.
- [ ] I implemented the ring buffer with wraparound and a size counter.
- [ ] I broke full-versus-empty on purpose and saw a full buffer report itself empty.
- [ ] I know why the dequeued slot must be set to `None`.
- [ ] I can write level-order traversal and explain the `range(len(queue))` line.
- [ ] I drew the order state machine from memory, with the backwards arrow.
- [ ] I can say how many of the thirty combinations are legal, and why refusal is the default.
- [ ] I can state the State-versus-Strategy rule in one sentence and point at the telling line.
- [ ] I can write the conditional UPDATE and say what zero rows updated means.
- [ ] I can say the honest concession: the branching moved into method dispatch, it did not vanish.
- [ ] I answered all three questions above out loud.
