---
day: 75
track: dsa
title: "A queue from two stacks, and a stack from queues"
phase: "Stacks and queues"
status: written
---

# Day 075 · DSA — A queue from two stacks, and a stack from queues

**After today you can:** You can build one from the other and give the amortised cost honestly.

**The interviewer asks it as:** *Implement a queue using only stacks. What is the amortised cost?*

---

## 1. What this is, and why they ask it

You are allowed one operation at one end — push and pop from the top of a stack — and you have to
produce first-in-first-out behaviour. The trick is that **pouring one stack into another reverses the
order**, so two stacks give you both ends. Then the same question is asked backwards: build a stack
using only queues.

The code is short. The interview is not about the code. It is about the sentence *"pop is O(n) in the
worst case and O(1) amortised"*, and about being able to prove that claim by counting how many times
a single element can be touched across its whole life. This is the first problem in the course where
**amortised** is the answer rather than a footnote.

They ask it because it separates people who have memorised complexities from people who can derive
them. It is LeetCode 232 and 225, it turns up in phone screens constantly, and the follow-up is
always the same: *"but pop can be O(n) — so how can you call it O(1)?"* If you can answer that
calmly, with a count rather than a claim, the question is over.

---

## 2. The story

Basava's shop opens at six, and the first thing he does, before the shutters are even fully up, is
sort out the milk.

The milk comes in soft packets and it goes bad, so the rule is simple and unbreakable: the oldest
packet in the shop has to be the next one sold. If a packet from Tuesday is still there on Friday,
that is money thrown away, and he learned that lesson expensively in his first year.

The trouble is the fridge. It is a narrow upright thing with one deep shelf, and packets go in from
the front and come out from the front. Whatever he put in last is what his hand reaches first. The
delivery boy comes at half past six and again at four, and both times the new packets go in at the
front — because that is the only place they can go.

So the packets he needs to sell are always at the back, behind everything newer, and he cannot get at
them.

What he does is this. Every morning he takes the packets out of the fridge one at a time and stacks
them on the counter beside the till. The one that comes out first goes down first, the next one on
top of it, and so on. By the time the fridge is empty, the pile on the counter is the other way round
— the oldest packet, the one that was right at the back, is now sitting on top where he can pick it
up.

Then he sells from the counter pile, top down, and every packet he hands over is the oldest one in
the shop. New deliveries go straight into the fridge, at the front, where they belong.

When the counter pile runs out, he empties the fridge onto the counter again, and it comes out
reversed again, oldest on top.

The one rule he is absolutely strict about, and he told his nephew off twice about this in one week,
is that he never adds to the counter pile while there is still something on it. If the fridge gets
poured onto a half-finished counter pile, the newer packets end up sitting on top of older ones and
he starts selling them in the wrong order. Empty the counter completely, then pour. Never before.

His nephew thinks the pouring is a waste of time — twenty packets moved at once, standing there at
half past six. Basava's answer is that every single packet gets picked up exactly twice in its life:
once going into the fridge, once coming out onto the counter. Twenty at a time looks like a lot of
work. Spread over the whole day, it is two touches a packet.

---

## 3. The idea in plain English

The fridge is a **stack**: last in, first out. So is the counter pile. Two stacks, and the only clever
thing in the whole design is that **pouring one stack into another reverses the order**, which turns
LIFO into FIFO.

### The two stacks

- **`inbox`** — the fridge. Everything you `enqueue` goes here, on top.
- **`outbox`** — the counter pile. Everything you `dequeue` comes from here, off the top.

`enqueue` is one line: push onto `inbox`.

`dequeue` is two: if `outbox` is empty, pour the whole of `inbox` into it; then pop `outbox`.

```python
    def dequeue(self):
        if not self._outbox:                  # only when empty. This is the rule.
            while self._inbox:
                self._outbox.append(self._inbox.pop())    # pouring reverses
        return self._outbox.pop()
```

Read the `while` as Basava emptying the fridge onto the counter. The first packet out of the fridge
is the newest, so it goes to the bottom of the counter pile; the last one out is the oldest, so it
ends on top. Reversal, for free, as a side effect of moving things.

### The rule that makes it correct

**Pour only when `outbox` is empty.** This is not an optimisation. It is what makes the queue a
queue.

If you pour while three packets are still on the counter, the freshly poured ones land on top of
them, and the next thing you sell is newer than something still underneath. In code: `enqueue(1)`,
`enqueue(2)`, `dequeue()` — which pours and returns 1 — then `enqueue(3)`, and now a pour with a
non-empty outbox puts 3 above 2, so the next dequeue returns 3 instead of 2. The order is wrong and
nothing raises an error.

The invariant to say out loud: **`outbox` holds the oldest elements, in the order they will leave;
`inbox` holds the newest, upside down. The whole queue, front to back, is `outbox` reversed followed
by `inbox`.**

### Amortised, and what the word actually means

One `dequeue` can be expensive. If a thousand elements are sitting in `inbox` and `outbox` is empty,
that dequeue moves all thousand. That is O(n) for a single operation, and you should say so plainly
rather than hide it.

Now count over the whole life of one element:

```
 push onto inbox         1 operation
 pop off inbox           1 operation   (during a pour)
 push onto outbox        1 operation   (during the same pour)
 pop off outbox          1 operation
 ------------------------------------
 total, for its whole life:  4
```

**Four operations per element, whatever order the calls come in.** So `n` enqueues and `n` dequeues
cost at most `4n` operations in total, which is O(1) each on average. That is what **amortised O(1)**
means: not "usually fast", but "the total across any sequence is bounded, so the cost per operation
averages to a constant".

The key fact holding it up: **an element moves from `inbox` to `outbox` exactly once.** It can never
go back. That is the same one-way argument as the monotonic stack of
[day 071](../day-071-monotonic-stack/README.md) and it is the same argument that makes `list.append`
amortised O(1), from [day 005](../day-005-python-lists-and-tuples/README.md).

**Amortised is not average-case.** Average-case is about which inputs are likely. Amortised makes no
assumption about the input at all: it is a guarantee about any sequence of operations, including the
worst one an adversary could pick. Saying that distinction correctly is worth a lot in the follow-up.

### Where amortised is not good enough

If this queue sits behind a request that must answer in five milliseconds, an occasional operation
that moves a hundred thousand elements is a latency spike, and "amortised O(1)" is no comfort to the
one request that hit it. Real-time systems care about the worst single operation, not the average.
Say this if asked — it shows you know that complexity is not the only thing that matters.

### Now backwards: a stack from queues

A queue only lets you take from the front, so to get the *last* thing in you must rotate everything
else past it. You choose which operation pays.

**Costly push, cheap pop** — usually the right answer:

```python
    def push(self, value):
        self._queue.append(value)
        for _ in range(len(self._queue) - 1):
            self._queue.append(self._queue.popleft())   # rotate the older ones behind
```

After the rotation, the newest element is at the front, so `pop` is just `popleft` — O(1). Push is
O(n). One queue is enough.

**Costly pop, cheap push** is the mirror: append on push, and on pop move `n − 1` elements to a second
queue and return the last one.

And unlike the queue-from-stacks, **there is no amortised trick here.** Every push does `n − 1`
rotations, every time; there is no "each element moves once" argument, because the same elements
rotate on every single push. This asymmetry is the interesting observation of the day: **two stacks
make a genuinely efficient queue, but queues do not make an efficient stack.** Being able to say
*why* — one direction has a one-way flow, the other repeats work — is the strongest thing you can
say about this pair of problems.

---

## 4. The picture

`enqueue(1)`, `enqueue(2)`, `enqueue(3)`, then `dequeue()`.

```
 after three enqueues            during the pour              after the pour
 ------------------             -------------                --------------
  inbox      outbox              inbox    outbox               inbox   outbox
  +---+      (empty)             +---+    +---+                (empty) +---+
  | 3 | <- top                   | 2 |    | 3 |                        | 1 | <- top
  +---+                          +---+    +---+                        +---+
  | 2 |                          | 1 |                                 | 2 |
  +---+                          +---+                                 +---+
  | 1 |                                                                | 3 |
  +---+                                                                +---+

  order in:  1, 2, 3            3 moved first,               1 is on top:
                                so it lands at the           dequeue returns 1
                                bottom of outbox             — correct FIFO
```

What to notice: nothing was sorted and nothing was searched. The reversal is a **side effect of
moving a stack one item at a time into another stack**, and that side effect is the entire algorithm.

Now the rule, drawn as the thing that goes wrong:

```
 CORRECT: pour only when outbox is empty

   enqueue 1,2 -> dequeue (pours, returns 1) -> enqueue 3 -> dequeue
   outbox holds [2] (2 on top); inbox holds [3]
   dequeue does NOT pour, because outbox is not empty      -> returns 2  correct

 WRONG: pour whenever inbox is non-empty

   same sequence, but the pour happens anyway
   outbox becomes [2] with 3 pushed on top
   +---+
   | 3 | <- top    dequeue returns 3
   +---+
   | 2 |           ...but 2 arrived first. Order broken, no error raised.
   +---+
```

And the whole queue, read as one line, so the invariant is visible:

```
   front                                                   back
     |                                                       |
     v                                                       v
   [ outbox top ... outbox bottom ][ inbox bottom ... inbox top ]
     oldest                                              newest
```

---

## 5. The code, built step by step

### Step 1 — enqueue is trivial

```python
    def enqueue(self, value: int) -> None:
        self._inbox.append(value)
```

O(1), always, no conditions. Every element enters the same way.

### Step 2 — the pour, in its own method

```python
    def _pour(self) -> None:
        """Move everything from inbox to outbox, reversing the order."""
        if not self._outbox:                       # ONLY when empty
            while self._inbox:
                self._outbox.append(self._inbox.pop())
```

Putting the emptiness check *inside* the helper is deliberate: now `dequeue` and `peek` both call
`_pour()` unconditionally and cannot get the rule wrong independently. Two call sites, one place
where the rule lives.

### Step 3 — dequeue and peek

```python
    def dequeue(self) -> int:
        self._pour()
        if not self._outbox:
            raise IndexError("dequeue from an empty queue")
        return self._outbox.pop()

    def peek(self) -> int:
        self._pour()
        if not self._outbox:
            raise IndexError("peek at an empty queue")
        return self._outbox[-1]
```

`peek` must pour too. Forgetting that is a real bug: `enqueue(1); peek()` would look at an empty
`outbox` while the element sits in `inbox`.

### Step 4 — emptiness and size

```python
    def is_empty(self) -> bool:
        return not self._inbox and not self._outbox      # BOTH must be empty

    def __len__(self) -> int:
        return len(self._inbox) + len(self._outbox)
```

Checking only one of the two is the second-most-common bug in this problem, and it produces a queue
that reports itself empty while holding a thousand elements.

### Step 5 — the stack from one queue

```python
    def push(self, value: int) -> None:
        self._queue.append(value)
        for _ in range(len(self._queue) - 1):
            self._queue.append(self._queue.popleft())
```

Append the newcomer at the back, then move every *other* element from the front to the back. After
`len - 1` rotations the newcomer is at the front, and everything else is behind it in the original
stack order.

Trace `push(1); push(2); push(3)`:

```
 push 1:  [1]                          0 rotations
 push 2:  [1,2] -> rotate 1 -> [2,1]   1 rotation
 push 3:  [2,1,3] -> rotate 2 -> [3,2,1]
 pop -> popleft -> 3.  Correct LIFO.
```

### The complete solution

```python
from collections import deque


class QueueFromStacks:
    """A FIFO queue built from two LIFO stacks.

    Pouring one stack into another reverses the order, which is the entire
    trick. `inbox` takes every arrival; `outbox` serves every departure.

    THE RULE: pour only when outbox is empty. Pouring onto a non-empty outbox
    puts newer elements above older ones and silently breaks FIFO order.

    Cost: enqueue O(1) always. dequeue O(n) worst case, O(1) AMORTISED, because
    each element is touched exactly four times in its whole life — pushed to
    inbox, popped from inbox, pushed to outbox, popped from outbox — and can
    never move backwards.
    """

    def __init__(self) -> None:
        self._inbox: list[int] = []          # arrivals, newest on top
        self._outbox: list[int] = []         # departures, oldest on top

    def enqueue(self, value: int) -> None:
        self._inbox.append(value)

    def dequeue(self) -> int:
        self._pour()
        if not self._outbox:
            raise IndexError("dequeue from an empty queue")
        return self._outbox.pop()

    def peek(self) -> int:
        self._pour()
        if not self._outbox:
            raise IndexError("peek at an empty queue")
        return self._outbox[-1]

    def is_empty(self) -> bool:
        return not self._inbox and not self._outbox      # both, not either

    def __len__(self) -> int:
        return len(self._inbox) + len(self._outbox)

    def _pour(self) -> None:
        if not self._outbox:                             # the rule, in one place
            while self._inbox:
                self._outbox.append(self._inbox.pop())


class StackFromOneQueue:
    """A LIFO stack built from a single FIFO queue: costly push, cheap pop.

    push rotates the older elements behind the newcomer, so the newest element
    is always at the front of the queue and pop is a plain popleft.

    Cost: push O(n) EVERY time — there is no amortised saving here, because the
    same elements rotate again on the next push. pop, top and empty are O(1).
    """

    def __init__(self) -> None:
        self._queue: deque[int] = deque()

    def push(self, value: int) -> None:
        self._queue.append(value)
        for _ in range(len(self._queue) - 1):
            self._queue.append(self._queue.popleft())    # older ones go behind

    def pop(self) -> int:
        if not self._queue:
            raise IndexError("pop from an empty stack")
        return self._queue.popleft()

    def top(self) -> int:
        if not self._queue:
            raise IndexError("top of an empty stack")
        return self._queue[0]

    def is_empty(self) -> bool:
        return not self._queue

    def __len__(self) -> int:
        return len(self._queue)


class StackFromTwoQueues:
    """The mirror: cheap push, costly pop.

    push appends. pop moves n-1 elements to a second queue, returns the last
    one, and swaps the two queues. Worth knowing so you can say which operation
    you chose to make expensive, and why.
    """

    def __init__(self) -> None:
        self._main: deque[int] = deque()
        self._spare: deque[int] = deque()

    def push(self, value: int) -> None:
        self._main.append(value)                         # O(1)

    def pop(self) -> int:
        if not self._main:
            raise IndexError("pop from an empty stack")
        while len(self._main) > 1:
            self._spare.append(self._main.popleft())
        value = self._main.popleft()
        self._main, self._spare = self._spare, self._main   # swap, do not copy
        return value

    def is_empty(self) -> bool:
        return not self._main


if __name__ == "__main__":
    q = QueueFromStacks()
    q.enqueue(1)
    q.enqueue(2)
    print(q.dequeue())                 # 1   (this call pours)
    q.enqueue(3)
    print(q.dequeue())                 # 2   (this call must NOT pour)
    print(q.dequeue())                 # 3   (this one pours again)
    print(q.is_empty())                # True
    try:
        q.dequeue()
    except IndexError as error:
        print(f"IndexError: {error}")  # IndexError: dequeue from an empty queue

    s = StackFromOneQueue()
    for value in (1, 2, 3):
        s.push(value)
    print(s.pop(), s.pop(), s.pop())   # 3 2 1

    t = StackFromTwoQueues()
    for value in (1, 2, 3):
        t.push(value)
    print(t.pop(), t.pop(), t.pop())   # 3 2 1

    # The two must behave identically to the real thing, on any sequence.
    import random
    from collections import deque as real_queue

    for _ in range(2000):
        mine, reference = QueueFromStacks(), real_queue()
        for _ in range(30):
            if reference and random.random() < 0.4:
                assert mine.dequeue() == reference.popleft()
            else:
                value = random.randint(0, 99)
                mine.enqueue(value)
                reference.append(value)
        assert len(mine) == len(reference)
    print("queue-from-stacks agreed with a real queue on 2000 random sequences")
```

The random sequence check at the end is the one that catches the pour-when-not-empty bug, because
that bug only shows up on an interleaving of enqueues and dequeues. A test that enqueues everything
and then dequeues everything will never find it.

---

## 6. What it costs

### The queue from two stacks

```
 enqueue   O(1)   always. One push.
 dequeue   O(n)   worst case — the pour moves everything in inbox
           O(1)   amortised
 peek      same as dequeue
 is_empty  O(1)
 space     O(n)   total across both stacks
```

The amortised argument, counted rather than asserted:

```
 one element's whole life:
   pushed onto inbox      1
   popped off inbox       1     (during a pour)
   pushed onto outbox     1     (during the same pour)
   popped off outbox      1
   ------------------------
   total                  4     — and it can never go back to inbox

 n enqueues + n dequeues  <=  4n operations  ->  O(1) amortised each
```

Concretely: enqueue a thousand elements, then dequeue a thousand. The first dequeue does a thousand
moves; the next 999 do none. Total work is 2,000 pushes and 2,000 pops for 2,000 operations — two
operations each, on average, even though one call did a thousand.

**The worst single operation is still O(n)**, and you should say both numbers. "Amortised O(1), worst
case O(n) for one call" is a complete answer; "O(1)" alone is a claim you will be asked to defend.

### The stack from queues

```
 push      O(n)   EVERY time
 pop       O(1)
 top       O(1)
 space     O(n)
```

There is deliberately no "amortised" line here. On a sequence of `n` pushes:

```
 push 1: 0 rotations
 push 2: 1 rotation
 push 3: 2 rotations
 ...
 push n: n-1 rotations
 ---------------------------
 total:  n(n-1)/2 rotations  ->  O(n^2) for n pushes  ->  O(n) each, not amortised down
```

At n = 10,000 pushes that is about fifty million rotations. Compare with the queue-from-stacks, where
n enqueues and n dequeues cost 4n = 40,000 operations. **Same-looking problem, thousand-fold
difference in behaviour**, and the reason is in one sentence: in the two-stack queue each element
moves between the stacks once and never returns; in the stack-from-queue the same elements rotate
again on every push.

### Compared with the real thing

```
 collections.deque:  enqueue O(1), dequeue O(1), worst case O(1)
 two stacks:         enqueue O(1), dequeue O(1) amortised, O(n) worst case
```

If you are allowed a real queue, use one. This construction exists as an exercise, and in one
genuine setting: some purely functional languages build queues exactly this way, because two
immutable lists are cheap to build and a "reverse the front list when the back runs out" is the same
amortised argument.

---

## 7. The traps

### Trap 1 — pouring when `outbox` is not empty

```python
    def _pour(self) -> None:
        while self._inbox:                     # no `if not self._outbox` guard
            self._outbox.append(self._inbox.pop())
```

No error. No crash. Wrong order, silently. The sequence that exposes it:

```
 enqueue(1); enqueue(2); dequeue() -> 1        outbox now holds [2]
 enqueue(3); dequeue()             -> 3        WRONG. Should be 2.
```

3 was poured on top of 2. This is the bug the random-sequence test exists to catch, and it will never
show up if you test by enqueuing everything first and then dequeuing everything.

### Trap 2 — `is_empty` checking one stack

```python
    def is_empty(self) -> bool:
        return not self._outbox                # WRONG
```

After `enqueue(1)` the element is in `inbox` and `outbox` is empty, so this reports an empty queue
holding one element. Any caller looping `while not queue.is_empty()` exits immediately and drops
everything. Check both.

### Trap 3 — `peek` that forgets to pour

```python
    def peek(self) -> int:
        return self._outbox[-1]                # no _pour()
```

```
IndexError: list index out of range
```

Fires on `enqueue(1); peek()`. `dequeue` and `peek` need exactly the same preparation, which is the
argument for putting the pour in its own method that both call.

### Trap 4 — pouring on every dequeue "to be safe"

```python
    def dequeue(self) -> int:
        while self._inbox:                     # unconditional
            self._outbox.append(self._inbox.pop())
        return self._outbox.pop()
```

This is trap 1 in a friendlier disguise — it is trap 1 whenever `outbox` is non-empty. It also
destroys the amortised bound even when it happens to be correct, because elements move repeatedly.

### Trap 5 — claiming O(1) without the qualifier

Saying "dequeue is O(1)" and stopping. The interviewer will say "but the pour moves n elements", and
now you are defending rather than explaining. Say it first, in full: **"O(n) for one call in the
worst case, O(1) amortised, because each element crosses from inbox to outbox exactly once and can
never go back."**

### Trap 6 — confusing amortised with average

"On average it is fast" is not the claim. Average-case reasoning assumes something about which inputs
arrive. Amortised assumes nothing: it bounds the **total** cost of *any* sequence of operations,
including the worst one someone could design on purpose. Get this distinction right and it is
noticeable.

### Trap 7 — rotating the wrong number of times in the stack-from-queue

```python
        for _ in range(len(self._queue)):      # should be len - 1
            self._queue.append(self._queue.popleft())
```

One rotation too many puts the newcomer back at the *end*, which turns your stack into a queue.
`push(1); push(2); pop()` returns 1 instead of 2. Compute `len` *after* appending the newcomer, and
rotate one fewer than that.

### Trap 8 — copying instead of swapping in the two-queue stack

```python
        self._main = self._spare
        self._spare = deque()                  # allocates a new queue every pop
```

Correct but wasteful: it discards and reallocates on every pop. Swap the two names instead —
`self._main, self._spare = self._spare, self._main` — which is one tuple assignment and no
allocation.

---

## 8. In the interview

### How it gets asked

- The direct version: *"Implement a queue using only stacks. What is the cost of each operation?"*
  LeetCode 232. The follow-up is guaranteed: *"pop can be O(n), so how is that O(1)?"*
- The reverse: *"Now implement a stack using only queues."* LeetCode 225, usually as a five-minute
  add-on.
- The theory version: *"Explain amortised complexity using an example."* This problem and Python's
  list growth are the two standard answers.
- The comparison: *"You have two implementations of a stack from queues — costly push or costly pop.
  Which do you choose?"*

### What to say out loud, in the first ninety seconds

1. **Name the trick immediately.** "A stack gives me last-in-first-out. If I pour one stack into
   another, the order reverses. So two stacks give me first-in-first-out."
2. **Name the two roles.** "One stack takes every arrival — call it `inbox`. The other serves every
   departure — `outbox`. Enqueue always pushes to `inbox`; dequeue always pops from `outbox`."
3. **State the rule as a rule, not a detail.** "The correctness condition is that I only pour when
   `outbox` is empty. Pouring onto a non-empty `outbox` puts newer elements above older ones, and
   nothing raises an error — it just returns the wrong element."
4. **Give both complexities before being asked.** "Enqueue is O(1) always. Dequeue is O(n) for a
   single call in the worst case, and O(1) amortised."
5. **Prove the amortised claim by counting.** "Each element is touched exactly four times in its
   entire life: pushed onto `inbox`, popped off `inbox`, pushed onto `outbox`, popped off `outbox`.
   It can never move backwards. So n enqueues and n dequeues cost at most 4n operations, whatever
   order the calls come in."
6. **Then write the code**, which is about fifteen lines.

### The follow-ups

**"Dequeue can move n elements. How is that O(1)?"**
"It is not, for a single call — that call is genuinely O(n) and I would say so. The claim is about
any sequence of calls. An element enters `inbox` once, crosses to `outbox` once, and leaves once; it
can never go back. So the total work across n enqueues and n dequeues is bounded by about 4n
operations, which averages to a constant each. Concretely: enqueue a thousand and then dequeue a
thousand — the first dequeue does a thousand moves and the next 999 do none, so it is two operations
per element overall."

**"What is the difference between amortised and average-case?"**
"Average-case makes an assumption about the distribution of inputs — it says 'on typical data this is
fast'. Amortised makes no assumption at all: it bounds the total cost of any sequence, including one
an adversary picks deliberately. There is no input to this queue that makes it worse than 4n. That is
a stronger guarantee, and it is why the same word is used for Python's list growth."

**"Is amortised good enough in production?"**
"It depends entirely on whether you care about the worst single operation. For total throughput, yes.
For a service with a p99 latency target, a dequeue that occasionally moves a hundred thousand
elements is a visible spike, and the average is no comfort to the request that hit it. In a real-time
or low-latency system I would use a structure with a worst-case bound — `collections.deque` here —
and keep this construction for the interview and for functional languages where it is genuinely
idiomatic."

**"Now build a stack from queues."**
"One queue is enough if I make push expensive: append the new element, then rotate the other `n − 1`
elements from the front to the back, so the newcomer ends up at the front. Then pop is a plain
`popleft`, O(1). The mirror is cheap push and costly pop with two queues. I would pick costly push if
pops are more frequent, which they usually are, and it uses one queue instead of two."

**"Does the same amortised argument apply to the stack from queues?"**
"No, and that is the interesting asymmetry. In the two-stack queue, an element crosses once and never
returns, so the work is bounded in total. In the stack from queues, every push rotates *all* the
existing elements again — the same elements move over and over. So n pushes cost n(n−1)/2 rotations,
which is quadratic; there is no amortised saving. Two stacks make a good queue, but queues do not
make a good stack."

**"Why would anyone build a queue this way?"**
"In an interview, to test whether I can count operations. In real code, almost never — I would use a
deque. The one genuine setting is purely functional programming, where you cannot mutate: a queue is
represented as a front list and a reversed back list, and when the front runs out you reverse the
back onto it. That is exactly this structure and exactly this amortised argument."

### A model answer

Asked: *implement a queue using only stacks, and tell me the amortised cost.*

> "The whole idea is one observation: a stack is last-in-first-out, and if I pour one stack into
> another by popping and pushing, the order comes out reversed. So two stacks give me both ends.
>
> I will keep two. `inbox` receives every arrival — enqueue is just a push, O(1), no conditions.
> `outbox` serves every departure — dequeue pops from it. When `outbox` runs out, I pour the whole of
> `inbox` into it, which reverses `inbox`, so the oldest element ends up on top of `outbox` where I
> can take it.
>
> The correctness condition, which I would write as a comment because it is easy to get wrong, is that
> I pour **only** when `outbox` is empty. If I pour onto a non-empty `outbox`, the newer elements land
> on top of older ones and I start returning things out of order — and nothing raises an error, the
> queue just quietly lies. The sequence that exposes it is enqueue 1, enqueue 2, dequeue, enqueue 3,
> dequeue: the second dequeue should give 2 and gives 3.
>
> A couple of small things that follow from having two stacks: `is_empty` must check both, or a queue
> holding one element in `inbox` reports itself empty. And `peek` needs the same pour as `dequeue`, so
> I put the pour in one private method that both call, rather than trusting myself to remember it
> twice.
>
> On cost. Enqueue is O(1) always. A single dequeue is O(n) in the worst case, and I would say that
> plainly rather than have you find it. But it is O(1) amortised, and here is the count that proves
> it. Over its whole life, one element is touched exactly four times: pushed onto `inbox`, popped off
> `inbox`, pushed onto `outbox`, popped off `outbox`. And it can never move backwards — once it is in
> `outbox` it only leaves. So n enqueues and n dequeues cost at most 4n operations, whatever order the
> calls arrive in. Enqueue a thousand and dequeue a thousand: the first dequeue moves a thousand
> elements and the next 999 move none.
>
> That is stronger than an average-case claim, which is worth being precise about. Average-case would
> assume something about typical inputs. Amortised assumes nothing — there is no sequence of calls,
> adversarial or otherwise, that costs more than about 4n.
>
> The one place I would not be satisfied with it is a latency-sensitive service. A dequeue that
> occasionally moves a hundred thousand elements is a p99 spike, and 'amortised' is no comfort to the
> request that hit it. There I would want a worst-case bound, which is what `collections.deque` gives
> me.
>
> If you want the reverse — a stack from queues — one queue is enough, with an expensive push: append
> the newcomer, then rotate the other n−1 elements from front to back so the newcomer is at the front,
> and pop becomes a plain `popleft`. What is worth noticing is that the amortised argument does *not*
> transfer. Every push rotates all the existing elements again, so n pushes cost about n²/2
> rotations. Two stacks make a genuinely efficient queue; queues do not make an efficient stack, and
> the difference is whether elements move once or move repeatedly."

---

## 9. Recall card

- **Pouring one stack into another reverses the order** — that single side effect turns two LIFO
  stacks into a FIFO queue. `inbox` takes every arrival (**enqueue is O(1), always**); `outbox` serves
  every departure.
- **The correctness rule: pour ONLY when `outbox` is empty.** Pouring onto a non-empty `outbox` puts
  newer elements above older ones and **fails silently** — `enqueue 1, 2 · dequeue · enqueue 3 ·
  dequeue` returns **3 instead of 2**. Put the guard inside one `_pour()` that both `dequeue` and
  `peek` call. `is_empty` must check **both** stacks.
- **Say both numbers: dequeue is O(n) for one call, O(1) amortised.** The proof is a count, not a
  claim: each element is touched exactly **4 times** in its life — inbox push, inbox pop, outbox push,
  outbox pop — and **can never move backwards**, so n enqueues + n dequeues ≤ **4n** operations.
- **Amortised is not average-case.** Average-case assumes something about the inputs; amortised bounds
  the **total cost of any sequence**, including an adversarial one. But it says nothing about a single
  call, so it is the wrong guarantee for a **p99 latency target** — there you want `deque`.
- **The asymmetry is the real lesson: two stacks make a good queue; queues do not make a good stack.**
  A one-queue stack rotates `len − 1` on **every** push, so n pushes cost **n(n−1)/2** — no amortised
  saving, because the same elements move again and again. Rotate `len − 1`, not `len`, or your stack
  becomes a queue.
