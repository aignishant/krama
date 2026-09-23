---
day: 77
track: dsa
title: "Stacks and queues revision and mock round"
phase: "Stacks and queues"
status: written
---

# Day 077 · DSA — Stacks and queues revision and mock round

**After today you can:** You can solve two unseen stack or queue problems cold.

**The interviewer asks it as:** *Two problems, no hints, talk as you go.*

---

## 1. What this is, and why they ask it

Ten days ago a stack was a list you could only touch at one end. Since then you have built balanced
bracket checkers, a min stack, monotonic stacks, the largest rectangle in a histogram, a ring-buffer
queue, a monotonic deque, a queue from two stacks and an LRU cache. Today is not new material. Today
is **recognition under time pressure**, which is a different skill and the one actually being tested.

The mock round is two problems in forty-five minutes, spoken aloud, with no hints. What is being
scored is not whether the code compiles. It is whether you say *"the stack holds the elements whose
answer is not yet known"* before you write a loop, whether you give the amortised argument before
being challenged, and whether you notice that a question about "the last k seconds" is a queue
question.

They run this round because a candidate who has memorised eight solutions and one who has understood
one idea look identical on the easy problems and completely different on an unfamiliar one. This day
is about being the second kind.

---

## 2. The story

Nithya failed her driving test the first time and she still thinks it was unfair.

She had been driving for three years by then — her father's car, mostly on the ring road, and every
Sunday to her grandmother's place forty minutes away. She was, by any reasonable measure, a
competent driver.

The test lasted eleven minutes. The examiner sat beside her with a small tablet and said almost
nothing. Start the car. Left at the junction. Pull over here. Reverse into that gap. Right at the
lights. Back to the centre. He did not raise his voice once and he did not ask her a single question
about driving.

She failed on four points. She had not looked over her right shoulder before moving off. She had not
checked the mirror before slowing down. She had signalled after she had already started turning. And
on the reverse she had done the whole thing correctly and beautifully while looking only at the
screen on the dashboard.

She argued about it in the car park, which nobody has ever won. The car had gone exactly where she
wanted it, every time, without a single scrape. That, she said, is driving.

Her instructor, when she rang him, was kind but not on her side. He said something she repeated to
her sister that evening. He said: the man cannot see what you know. He can only see what you do. You
looked in the mirror on the road every Sunday for three years and you did not look in it once in
front of him, because when you are nervous you do the thing and you skip the showing.

So the second time she narrated the whole drive. Out loud, the entire eleven minutes. Checking the
mirror. Right shoulder. Signalling now. Gear down for the junction. Nothing to my left, going.

She said afterwards that it felt ridiculous and that the examiner must have thought she was mad. He
did not. He ticked things off, said "that was fine", and gave her the pass.

The driving was identical both times. She is sure of that. What changed was that the second time,
someone else could tell.

---

## 3. The idea in plain English

The mock round is the driving test. The interviewer cannot see what you know. They can only see what
you say. Everything below is a thing to **say**, in order, before or while you write.

### The recognition procedure, in the order to run it

Run this on any problem in the phase, in under sixty seconds.

**1. Does the problem mention "most recent", "last", "innermost", "matching", or "undo"?**
→ Stack. The recognition sentence is: *reach for a stack when you need the most recent thing not yet
resolved.*

**2. Does it mention "in order", "first", "oldest", "levels", "shortest path", or "the last k
seconds"?**
→ Queue. FIFO is what makes level-by-level and shortest-path-in-an-unweighted-graph work.

**3. Does it ask, for every element, about the nearest element on one side satisfying a
comparison?**
→ Monotonic stack. Next greater, next smaller, previous greater, previous smaller — four variants
from two knobs.

**4. Does it ask for an aggregate over a window that slides?**
→ Monotonic deque if the aggregate is max or min. A running sum if it is a sum. Two heaps if it is a
median.

**5. Does it need both "find this key fast" and "find the oldest fast"?**
→ Two structures: a hash map plus a doubly linked list. One structure will not do it.

**6. Does it ask you to build one structure out of another?**
→ Two stacks make a queue with an amortised argument. Queues make a stack without one.

### The five sentences that carry the whole phase

If you remember nothing else, these are what you say out loud.

1. **"The stack holds the things whose answer is not yet known."** True of brackets, of monotonic
   stacks, of the histogram, of the calculator family. Say what your stack holds *before* writing the
   loop, every single time.
2. **"Each element is pushed once and popped at most once, so it is O(n) — the inner loop is bounded
   in total, not per iteration."** This is the complexity defence for half the phase. Say it before
   being challenged.
3. **"The front of a Python list is the expensive end."** `pop(0)` and `insert(0, x)` are O(n).
   Measured: 10.2 seconds against 0.0034 for 100,000 elements.
4. **"Store indices, not values."** Because the follow-up always wants a distance or a width, and a
   value cannot give you one.
5. **"Amortised O(1) means the total across any sequence is bounded — it is not average-case, and it
   is not a promise about any single call."**

### The one-page comparison

| Structure | Add | Remove | Look | Use it when |
|---|---|---|---|---|
| `list` as a stack | `append` O(1) | `pop()` O(1) | `[-1]` | Most recent unresolved thing |
| `list` as a queue | `append` O(1) | **`pop(0)` O(n)** | `[0]` | **Never** |
| `deque` | `append`/`appendleft` O(1) | `pop`/`popleft` O(1) | `[0]`, `[-1]` | Any queue; both ends |
| Ring buffer | O(1) | O(1) | O(1) | Fixed capacity, no allocation |
| Monotonic stack | O(1) amortised | O(1) amortised | `[-1]` | Nearest greater/smaller |
| Monotonic deque | O(1) amortised | O(1) amortised | `[0]` | Window max or min |
| Two stacks as a queue | O(1) | O(1) amortised, O(n) worst | O(1) amortised | Only when asked |
| Map + doubly linked list | O(1) | O(1) | O(1) | LRU: key lookup *and* recency |

### What the round is actually scoring

Four things, in this order of weight:

1. **Did you say what the structure holds, before coding?** More than anything else, this is what
   distinguishes understanding from recall.
2. **Did you give the complexity with the counting, not just the letter?** "O(n) because each element
   is pushed once and popped at most once" beats "O(n)".
3. **Did you handle the empty case?** `while stack and ...` is the single most common missing guard in
   this phase.
4. **Did you name the trade-off you chose?** Ring buffer versus deque, exact LRU versus approximate,
   `<` versus `<=`. Choosing is fine. Choosing silently is not.

---

## 4. The picture

The phase on one page. Every problem you have met, grouped by the sentence that triggers it.

```
 "the most recent thing not yet resolved"          -> STACK
   +-- unmatched opener                            -> balanced brackets
   +-- the value before this one                   -> min stack (carry the aggregate)
   +-- the element whose answer is unknown         -> monotonic stack
   |     +-- answer is a VALUE                     -> next greater element
   |     +-- answer is a DISTANCE                  -> daily temperatures
   |     +-- answer is a WIDTH between boundaries  -> largest rectangle
   +-- the context I am leaving                    -> decode string, RPN, calculator

 "in the order they arrived"                       -> QUEUE
   +-- fixed capacity, no allocation               -> ring buffer
   +-- one level at a time                         -> level-order traversal, BFS
   +-- the last k seconds                          -> sliding window of timestamps
   +-- both ends needed                            -> DEQUE
         +-- max or min over a sliding window      -> monotonic deque

 "lookup fast AND oldest fast"                     -> MAP + DOUBLY LINKED LIST
   +-- evict the least recently used               -> LRU cache
   +-- evict the least frequently used             -> LFU: a third structure

 "build X out of only Y"                           -> TRANSFORMATION
   +-- queue from two stacks                       -> amortised O(1); pour when empty
   +-- stack from queues                           -> O(n) push, NO amortised saving
```

What to notice: the left-hand column has only four entries. **Four trigger sentences cover ten days.**
That is the compression you are aiming for — not ten memorised solutions, four questions you ask
yourself.

And the diagram that answers "is it linear?", because it will be asked twice:

```
 for element in n elements:          <- runs exactly n times: n pushes
     while <condition>:              <- only ever POPS
         pop()

 pushes across the whole run:  exactly n
 pops   across the whole run:  at most  n   (nothing that leaves ever returns)
 -----------------------------------------------
 total operations:             <= 2n   ->  O(n)

 One iteration may pop 100,000 elements. That iteration has consumed
 all the pops the rest of the run was going to do.
```

---

## 5. The code, built step by step

Two problems, worked the way you would work them in the room — the talking first, then the code.

### Problem one: *"You are given a list of daily stock prices. For each day, report how many consecutive days up to and including today had a price less than or equal to today's price."*

**What to say first, before writing anything.**

"Let me restate it: for day `i`, I want the length of the longest run ending at `i` where every price
is at most `prices[i]`. So really I am looking for the nearest earlier day with a *strictly greater*
price — everything after that day and up to today qualifies. That is 'previous greater element', which
is a monotonic stack."

"Brute force: for each day walk backwards until I find a bigger price. That is O(n²) — five billion
comparisons at a hundred thousand days."

"The stack will hold the days whose price has not yet been beaten. When today's price is at least the
price on top, that day can never be the answer for any future day either, because today is later and
at least as large — so I pop it, and I take its span with me."

**Then the code, in fragments.**

```python
    stack: list[tuple[int, int]] = []      # (price, span) for unbeaten days
    spans: list[int] = []
```

The stack holds pairs, not just prices, and that is the trick: **when I pop a day, I absorb its span
into mine**, so I never re-walk the days it already covered.

```python
    for price in prices:
        span = 1                           # today always counts
        while stack and stack[-1][0] <= price:
            span += stack.pop()[1]         # absorb the span of everything I beat
        stack.append((price, span))
        spans.append(span)
```

Five lines. Say the invariant out loud while writing: *the stack is strictly decreasing by price from
bottom to top, and each entry carries how many days it accounts for.*

**Then the complexity, unprompted.** "Each day is pushed exactly once and popped at most once, so at
most 2n stack operations across the whole run — O(n) time, O(n) space in the worst case of strictly
increasing prices, where nothing is ever popped."

**Then the edge cases, out loud.** "Equal prices: the problem says 'less than or equal', so I pop on
`<=`, which means an equal earlier day is absorbed. If it had said 'strictly less', I would use `<`.
That is a one-character difference and I would confirm it with you."

### Problem two: *"Implement `allow(user_id, timestamp) -> bool`. A user may make at most 100 requests in any rolling 60-second window."*

**What to say first.**

"'Any rolling 60-second window' is the giveaway — that is a queue of timestamps per user. I keep the
timestamps of that user's recent requests, drop the ones older than 60 seconds from the front, and
then the count is just the length."

"Front removals and back additions, both O(1), so a `deque`. If I used a list and `pop(0)` this would
be O(n) per eviction, which at a hundred requests a user is not fatal but is a bad habit and I would
not do it."

"One thing I want to flag before coding: this grows without bound if I keep a deque per user for ever.
So I would ask whether we need exact windows or approximate — and if memory matters, the standard
production answer is a counter per fixed window, or a token bucket, both of which are O(1) memory per
user. I will write the exact one, since that is what was asked."

**Then the code.**

```python
from collections import defaultdict, deque

class RateLimiter:
    def __init__(self, limit: int = 100, window_seconds: int = 60) -> None:
        self._limit = limit
        self._window = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)
```

`defaultdict(deque)` so a first-time user does not need a special case.

```python
    def allow(self, user_id: str, timestamp: float) -> bool:
        hits = self._hits[user_id]
        cutoff = timestamp - self._window
        while hits and hits[0] <= cutoff:      # expire from the FRONT
            hits.popleft()
```

The `while` here — not an `if` — because unlike the sliding-window maximum, several timestamps can
expire between two calls. Saying why you chose `while` over `if` is exactly the kind of remark that
gets noticed.

```python
        if len(hits) >= self._limit:
            return False                        # rejected: do NOT record it
        hits.append(timestamp)
        return True
```

**The subtle line is `return False` before `append`.** A rejected request must not be recorded, or a
user who keeps hammering the endpoint never escapes the window — every rejection extends their own
ban. Say that out loud; it is the bug the interviewer is watching for.

**Then the complexity.** "Amortised O(1) per call: each timestamp is appended once and popped once,
so `n` calls cost at most `2n` deque operations. Memory is O(limit) per active user — a hundred
floats, about 900 bytes with the deque overhead — so a million active users is roughly 900 MB, which
is the number that would make me move to a token bucket."

### The reference implementations, for revision

```python
from collections import defaultdict, deque


def stock_spans(prices: list[int]) -> list[int]:
    """For each day, the number of consecutive days up to and including today
    with a price <= today's price.

    A monotonic stack of (price, span). Popping absorbs the popped day's span,
    which is why no day is ever re-examined. O(n) time, O(n) space.
    """
    stack: list[tuple[int, int]] = []       # (price, span), prices decreasing
    spans: list[int] = []

    for price in prices:
        span = 1
        while stack and stack[-1][0] <= price:
            span += stack.pop()[1]          # absorb, do not re-walk
        stack.append((price, span))
        spans.append(span)

    return spans


class RateLimiter:
    """At most `limit` requests per user in any rolling `window_seconds`.

    One deque of timestamps per user. Expire from the front, count the rest.
    A REJECTED request is not recorded, or a hammering client never recovers.
    Amortised O(1) per call; O(limit) memory per active user.
    """

    def __init__(self, limit: int = 100, window_seconds: float = 60.0) -> None:
        self._limit = limit
        self._window = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, user_id: str, timestamp: float) -> bool:
        hits = self._hits[user_id]
        cutoff = timestamp - self._window
        while hits and hits[0] <= cutoff:
            hits.popleft()
        if len(hits) >= self._limit:
            return False
        hits.append(timestamp)
        return True

    def forget_idle(self, now: float) -> int:
        """Drop users with no recent activity. Without this, memory grows for
        ever — which is the honest weakness of the exact-window approach."""
        stale = [user for user, hits in self._hits.items()
                 if not hits or hits[-1] <= now - self._window]
        for user in stale:
            del self._hits[user]
        return len(stale)


def is_balanced(text: str) -> bool:
    """The phase in six lines. The stack holds the openers not yet closed."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for character in text:
        if character in "([{":
            stack.append(character)
        elif character in pairs:
            if not stack or stack.pop() != pairs[character]:
                return False
    return not stack                        # non-empty at the end is a failure


def next_greater(numbers: list[int]) -> list[int]:
    """The base monotonic stack. Indices, because the follow-up wants a distance."""
    answer = [-1] * len(numbers)
    stack: list[int] = []
    for index, value in enumerate(numbers):
        while stack and numbers[stack[-1]] < value:
            answer[stack.pop()] = value
        stack.append(index)
    return answer


def max_sliding_window(numbers: list[int], k: int) -> list[int]:
    """Monotonic deque. Expire the front, crush the back, append, then record."""
    if k <= 0 or not numbers:
        return []
    window: deque[int] = deque()
    answers: list[int] = []
    for index, value in enumerate(numbers):
        if window and window[0] <= index - k:
            window.popleft()
        while window and numbers[window[-1]] <= value:
            window.pop()
        window.append(index)
        if index >= k - 1:
            answers.append(numbers[window[0]])
    return answers


if __name__ == "__main__":
    print(stock_spans([100, 80, 60, 70, 60, 75, 85]))   # [1, 1, 1, 2, 1, 4, 6]
    print(stock_spans([1, 2, 3, 4]))                    # [1, 2, 3, 4]
    print(stock_spans([4, 3, 2, 1]))                    # [1, 1, 1, 1]
    print(stock_spans([5, 5, 5]))                       # [1, 2, 3]

    limiter = RateLimiter(limit=3, window_seconds=10)
    print([limiter.allow("u1", t) for t in (0, 1, 2, 3, 11)])
    # [True, True, True, False, True]

    print(is_balanced("({[]})"), is_balanced("([)]"), is_balanced("(("))
    # True False False
    print(next_greater([2, 1, 2, 4, 3]))                # [4, 2, 4, -1, -1]
    print(max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))
    # [3, 3, 5, 5, 6, 7]
```

---

## 6. What it costs

### The whole phase, priced at n = 1,000,000

```
 balanced brackets              O(n) time,  O(n) space worst case
 min stack                      O(1) per operation, 2n space
 monotonic stack                <= 2n operations,   O(n) space worst case
 largest rectangle              <= 2n+2 operations, O(n) space
 ring-buffer queue              O(1) per operation, O(capacity) space
 monotonic deque (window max)   <= 2n operations,   O(k) space
 queue from two stacks          4n operations total, O(n) space
 LRU cache                      ~6 writes per get, ~10 per put, O(capacity) space
```

Every single line is linear or constant. That is the shape of the phase: **stacks and queues turn
quadratic problems linear, and the mechanism is always that each element is handled a fixed number of
times.**

### The four arithmetic facts to have ready

```
 1. list.pop(0) draining 100,000 elements     10.203 s
    deque.popleft draining the same            0.0034 s      ~3,000x

 2. n -> 2n on list.pop(0):  10.20 s -> 39.74 s               3.9x  = quadratic

 3. sliding window max, n=200,000, k=1,000
      brute force  1.984 s | heap 0.092 s | deque 0.050 s     40x and 1.8x

 4. monotonic stack vs brute force at n=100,000
      5 x 10^9 comparisons vs 2 x 10^5 operations             ~25,000x
```

Quoting one real measurement is worth more than three complexity classes, because anybody can say
"O(n²) is slower".

### Space, side by side

```
 stack / deque of indices        O(n) worst, O(1) best   — name both inputs
 monotonic deque                 O(k), independent of n  — the streaming argument
 ring buffer                     O(capacity), fixed      — no allocation at all
 LRU cache                       O(capacity), ~190 B/entry in Python
 min stack (pairs)               2n
 min stack (O(1) extra)          n, but it overflows in fixed-width languages
```

### The complexity claim that gets probed

Three of them, and the probe is always the same shape:

- *"There is a loop inside a loop."* → n pushes, each element popped at most once, ≤ 2n operations.
- *"Pop can move n elements."* → four touches per element over its whole life, and it never goes
  backwards.
- *"You loop 2n times for the circular version."* → still n pushes and n pops; the constant is two.

All three are the same argument. **Count the operations across the run, not the nesting.**

---

## 7. The traps

The complete list for the phase. Each one has cost somebody an interview.

### `pop(0)` and `insert(0, x)`

O(n), silently. The correct answers are `deque.popleft()` and `deque.appendleft()`. If you write
`pop(0)` in a queue problem, the interviewer stops listening to the rest.

### A missing `while stack and ...`

```
IndexError: pop from an empty list
IndexError: list index out of range
IndexError: pop from an empty deque
```

Three phrasings of one bug. The emptiness check must be the **first** half of the `and`, because `and`
short-circuits.

### Storing values instead of indices

Works until the follow-up asks for a distance or a width, then cannot be patched. Store indices;
write `numbers[stack[-1]]` when you need the value.

### Building the answer by appending as you pop

The elements never popped simply go missing and your output is shorter than the input. **Pre-fill the
answer array with the default and write into it by index.**

### Forgetting the leftovers

Whatever is still in the stack at the end has no answer. Either pre-fill the default, or push a
sentinel that forces everything out. Without it, `largest_rectangle([1,2,3,4,5])` returns 0.

### `<` versus `<=`

`next_greater([2,2,3])` gives `[3,3,-1]` with `<` and `[2,3,-1]` with `<=`. Both are correct
programs; only one answers the question. Read the problem for the word "strictly", and ask if it is
not there.

### The width off-by-one

`width = index - left - 1`, because both boundaries are the shorter bars and neither is inside the
span. `index - left` returns 15 instead of 10 on the standard input.

### `head == tail` meaning both empty and full

Keep an explicit `_size` counter. And never loop on `while head < tail` — it breaks the moment the
tail wraps.

### Reading a ring buffer in slot order

Wrong order as soon as `tail < head`. Walk `(head + i) % capacity` for `i` in `range(size)`.

### Not clearing the dequeued slot

`self._items[self._head] = None`. Without it the queue holds every object it has ever seen alive, and
a job runner leaks gigabytes.

### `is_empty` checking one of two structures

In the two-stack queue, `not self._outbox` reports a queue holding a thousand elements as empty. Check
both.

### Pouring onto a non-empty outbox

No error, wrong order. `enqueue 1, 2 · dequeue · enqueue 3 · dequeue` returns 3 instead of 2. Pour
**only** when the outbox is empty.

### Rotating `len` times instead of `len - 1`

Turns your stack from queues into a queue. `push(1); push(2); pop()` returns 1.

### `get` that does not reorder, in an LRU cache

Every returned value is right; every eviction is wrong. A read is a use.

### Evicting from the list but not the map

The map grows for ever and a later `get` resurrects a node that is not in the list. **Every change
touches both structures.**

### No key stored on the LRU node

Eviction then cannot delete the map entry without scanning. Store the key.

### No sentinels in linked-list code

```
AttributeError: 'NoneType' object has no attribute 'next'
```

Two fake nodes remove six branches and this error with them.

### The expiry comparison in a sliding window

`window[0] <= index - k`, derived from "the window ending at `index` starts at `index - k + 1`". With
`<` it is right on most inputs and wrong on `[8, 3, 2]` with k = 2.

### Recording before the window is full

`if index >= k - 1`. Without it you return `n` answers instead of `n - k + 1`.

### Recording a rejected request in a rate limiter

The user's window never empties and they are banned for ever. Return before appending.

### Quoting amortised as if it were worst case

"O(1)" alone invites the challenge. Say "O(1) amortised, O(n) for a single call", and say which one
matters for a p99 latency target.

### Using `queue.Queue` in a coding round

Correct, and about 48× slower, because it locks on every operation. Name it only when the question is
about threads.

---

## 8. In the interview

### How it gets asked

- The plain mock: *"Two problems, forty-five minutes, talk as you go."*
- The disguised stack: *"Evaluate this expression"*, *"decode this string"*, *"simplify this file
  path"*, *"remove k digits to make the smallest number"*.
- The disguised queue: *"how many requests in the last minute"*, *"print the tree level by level"*,
  *"how many minutes until every orange has rotted"*.
- The design-a-structure question: *"design a data structure with O(1) insert, delete and get
  random"*, or an LRU cache.
- The follow-up that is really the question: *"is that not quadratic?"*

### The script, minute by minute, for a 45-minute round

**Minutes 0–3 — restate and clarify.** Say the problem back in your own words. Ask about the three
things that always matter in this phase: duplicates and whether comparisons are strict; the size of
`n`; and what to return when the input is empty. Write the two or three examples they give you, plus
one you invent that is degenerate.

**Minutes 3–6 — brute force, with a number, then reject it.** "For each element I would walk
backwards, which is n squared over two — five billion at a hundred thousand elements." Never skip
this. It establishes the baseline that makes your improvement measurable.

**Minutes 6–10 — the observation, not the algorithm.** This is the part that is scored. "When a bigger
element arrives, everything smaller before it is worthless for ever." Or: "the last k seconds is a
queue of timestamps." Say what the structure will hold, in one sentence, before writing anything.

**Minutes 10–25 — code, narrating.** Write the emptiness guard as you write the `while`. Say "indices,
not values, because the follow-up wants a distance". Say "expire, crush, append, record" as you write
those four lines.

**Minutes 25–30 — trace one example out loud.** Pick the degenerate one you invented. This catches
the off-by-one before the interviewer finds it, and finding your own bug reads far better than having
it pointed out.

**Minutes 30–35 — complexity, with the counting.** "n pushes, each element popped at most once, so at
most 2n operations — the inner loop is bounded in total, not per iteration." Then space, with the
worst-case input named.

**Minutes 35–45 — the second problem**, at double speed, because the pattern-recognition is now warm.

If you have five minutes left over, offer the cross-check: "I would normally run this against a brute
force on small random inputs, because the off-by-one in the width is easy to miss."

### The follow-ups

**"There is a loop inside a loop. Is that not O(n²)?"**
"No — count operations rather than nesting. Every element is pushed exactly once by the outer loop
and popped at most once, because once it leaves the stack it never returns. So the total is at most
2n across the whole run, however unevenly it falls. One iteration might pop a hundred thousand
elements; that iteration has used up all the pops the rest of the run was going to do."

**"Why a deque rather than a list?"**
"Because I need to remove from the front, and the front of a list is the expensive end — removing
element zero shifts every remaining element one slot left, so it is O(n) and draining is O(n²). I
measured it once: a hundred thousand elements took ten seconds with `pop(0)` and three milliseconds
with `deque.popleft`, and doubling the input quadrupled the time, which is the quadratic signature."

**"Can you do it with less space?"**
Depends on the problem, and the honest answers differ. "For window maximum, no — O(k) is already
independent of n, and there is a block-partition trick that is also O(n). For the min stack, yes:
push `2*value - min` and recover with arithmetic, but it overflows in fixed-width languages, so I
would mention it and not write it. For a rate limiter, yes: a token bucket is O(1) per user instead
of O(limit)."

**"What if the data is a stream and never ends?"**
"That favours the deque solutions, because their space is O(k) rather than O(n) — a sixty-second
window over a billion events holds sixty entries. What breaks is anything that needs the whole array
up front, like the two-pass histogram version. And I would watch the index counter, which grows
without bound in a long-running process."

**"Is this thread-safe?"**
"No. `deque.append` and `popleft` happen to be atomic in CPython, so a single-producer,
single-consumer deque is safe by accident, but I would not rely on that. Anything with two structures
— the LRU cache — is definitely not: two threads interleaving pointer updates can corrupt the list
with no exception raised. One lock, or shard by key hash to reduce contention."

**"Which of these would you actually use in production?"**
"`collections.deque` for every queue. `OrderedDict` or `functools.lru_cache` instead of hand-writing
an LRU. A ring buffer only when the capacity is fixed and allocation matters, like a metrics buffer.
The two-stack queue essentially never, outside functional languages. And Redis with an LRU eviction
policy when the cache has to be shared between processes."

### A model answer

Asked: *for each day, report how many consecutive days up to and including today had a price at most
today's price.*

> "Let me restate it to check I have it. For day `i`, I want the length of the longest run ending at
> `i` in which every price is at most `prices[i]`. Two things I would confirm: 'at most' means an
> equal earlier price counts, yes? And today itself always counts, so the smallest answer is 1.
>
> The brute force is: from each day walk backwards while the prices are at most today's. That is
> n squared over two in the worst case — an increasing sequence — which is five billion comparisons
> at a hundred thousand days. So I want a single pass.
>
> Here is the observation. The run ending today stops at the first earlier day with a *strictly
> greater* price. So what I actually need is the previous greater element, which is a monotonic
> stack.
>
> And there is a second observation that makes it cheap. When I pop a day because today's price beats
> it, that day can never be the answer for any future day either — any future day that could have
> reached it also reaches today, and today is at least as large. So popping is permanent, and I can
> absorb the popped day's span into mine rather than walking those days again. That is why the stack
> holds pairs: a price and the number of days that price accounts for.
>
> So: for each price, start a span of one. While the stack is non-empty and the price on top is at
> most today's, pop it and add its span to mine. Then push my price with my span, and record the
> span. Five lines. The stack ends up strictly decreasing by price from the bottom up, and I did not
> sort it — anything that would have broken the order was popped.
>
> On complexity: each day is pushed exactly once and popped at most once, so at most 2n stack
> operations across the whole run. O(n) time. The inner `while` looks quadratic and is not — it is
> bounded in total, not per iteration. Space is O(n) in the worst case, which is a strictly
> increasing price sequence where nothing is ever popped, and O(1) on a strictly decreasing one where
> every day pops the previous.
>
> Two things I would check before I called it done. The `<=` in the pop condition is where 'at most'
> lives — if the problem had said 'strictly less than today', that becomes `<`, and it changes the
> answer on equal prices: `[5, 5, 5]` gives spans of 1, 2, 3 with `<=` and 1, 1, 1 with `<`. And the
> empty input returns an empty list, which the loop handles without a special case.
>
> If you want, I would normally check this against the O(n²) version on a few hundred small random
> arrays — the span-absorbing line is the kind of thing that is easy to get subtly wrong and easy to
> verify."

---

## 9. Recall card

- **Four trigger sentences cover the whole phase.** *"The most recent thing not yet resolved"* →
  **stack**. *"In the order they arrived / the last k seconds / one level at a time"* → **queue**.
  *"For every element, the nearest one on a side satisfying a comparison"* → **monotonic stack**.
  *"Lookup fast AND oldest fast"* → **map + doubly linked list**.
- **Say what the structure holds before you write the loop.** "The stack holds the elements whose
  answer is not yet known." That one sentence is what the round is scoring — the driving test cannot
  see what you know, only what you say.
- **The complexity defence, said before it is challenged: n pushes, each element popped at most once,
  ≤ 2n operations — bounded in total, not per iteration.** And its cousin for the two-stack queue:
  **four touches per element, never backwards**, so amortised O(1) — *which is not average-case and
  is not a promise about one call.*
- **The four measurements to quote.** `pop(0)` 10.2 s vs `deque.popleft` 0.0034 s at 100,000
  (~3,000×) · n → 2n gave **3.9×**, the quadratic signature · window max at n = 200,000, k = 1,000:
  brute **1.98 s**, heap **0.092 s**, deque **0.050 s** · monotonic stack vs brute force ~**25,000×**.
- **The traps that end rounds:** `pop(0)` · a missing `while stack and` · values instead of indices ·
  appending the answer instead of writing by index · forgetting the leftovers · `<` vs `<=` ·
  `width = right − left − 1` · `head == tail` needing a size counter · pouring onto a non-empty outbox
  · `get` that does not reorder · removing from one structure and not the other · recording a
  *rejected* request in a rate limiter.
