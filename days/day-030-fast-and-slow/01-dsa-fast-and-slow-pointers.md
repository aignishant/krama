---
day: 30
track: dsa
title: "Fast and slow pointers"
phase: "Two pointers and sliding window"
status: written
---

# Day 030 · DSA — Fast and slow pointers

**After today you can:** You can find the middle of a sequence in one pass and detect a loop in it.

**The interviewer asks it as:** *Find the middle element in a single pass.*

---

## 1. What this is, and why they ask it

The third of the three two-pointer shapes. Both indices start at the same place and move in the same
direction, but **at different speeds** — one step at a time for the slow one, two for the fast one.

That single arrangement answers two apparently unrelated questions.

**Where is the middle?** When the fast index reaches the end, it has taken twice as many steps, so the
slow index is exactly halfway. One pass, no length needed in advance — which matters enormously for
anything you can only walk forwards through.

**Is there a loop?** On a straight path the fast one pulls away and you never see it again. If the path
bends back on itself, the fast one comes round and catches the slow one from behind. **That catching
is the proof**, and it needs no memory of where you have been.

The technique is **Floyd's cycle detection**, universally called *tortoise and hare*. It is asked
constantly, in three costumes: on linked lists from [day 083](../day-083-cycle-detection/README.md),
on arrays that encode a function — *Find the Duplicate Number*, LeetCode 287 — and on number sequences
— *Happy Number*, LeetCode 202. The costume changes and the six lines do not.

The reason interviewers like it is that the obvious solution to cycle detection is a hash set of
everything seen, which is `O(n)` space, and Floyd's is `O(1)`. **A candidate who produces the set
version and then says "but I can do it in constant space" has answered the question**; one who only
knows the set has not.

---

## 2. The story

There is a walking path all the way round the lake at the back of Girish's colony, and he does it every
morning at ten past six, four rounds, about an hour.

His neighbour Mani runs it. Not fast, but properly, and roughly twice Girish's speed.

They start together at the gate most mornings and they talk for the first thirty seconds and then Mani
goes on ahead. What Girish noticed in his first week — and it delighted him, in the way small
regularities do — is that Mani comes past him again. From behind. Every eleven minutes or so, without
fail, there is the sound of Mani's shoes coming up behind him and a hand on his shoulder as he goes by.

The path is a loop, so that is what happens. Mani gets further and further ahead, and then the ahead
becomes behind, and he arrives from the other side.

Girish said something to him about it once and Mani, who thinks about these things, said the useful
part back: on a loop, if one man goes twice as fast as another, he will always catch him. He cannot
not. He gains steadily on him, and there is nowhere for the slow man to escape to.

The other thing happened in October, when the council dug up the far side for a drain and made the
path an out-and-back — down to the far corner and turn round and come back. That morning Mani never
came up behind him at all. Girish saw him coming the other way, waved, and that was that. A straight
path out and a straight path back, and the faster man simply gets to the end and returns; he never
laps anybody, because there is no lap.

There is one more thing they do, and it is the reason they still start together. Girish's wife drops
them at the gate and comes back for them. So when Mani finishes his round and reaches the gate again,
he tells her where Girish is — and he is always at the same place, right across the water, exactly
halfway. Twice the speed, twice the distance, so when one of them is at the end the other is at the
middle. She has stopped asking.

---

## 3. The idea in plain English

Girish is `slow`, moving one step at a time. Mani is `fast`, moving two. Everything today comes from
that and from one fact: **if there is a loop, the fast one must catch the slow one.**

### Finding the middle

```python
slow = fast = 0
while fast + 1 < len(items):
    slow += 1
    fast += 2
return slow
```

`fast` covers two positions for every one of `slow`'s. When `fast` can go no further, it has travelled
about `n` and `slow` has travelled about `n/2` — so `slow` is at the middle.

**Why this is worth doing on an array at all**, where you could just use `len(items) // 2`: because the
same six lines work on a structure you can only walk forwards through and whose length you do not know.
That is a linked list, and it is why this is the standard answer to *"find the middle of a linked list
in one pass"*. On an array it is a demonstration; on a list it is the only sensible method.

**The contract question:** on an even-length sequence there are two middles. `[1,2,3,4]` — is it `2` or
`3`? The loop above gives the **second** one, index 2, which is the LeetCode 876 convention. Ask.
Changing the loop condition to `while fast + 2 < len(items)` gives the first. **Say which one you are
returning and why.**

### Detecting a loop

Now the same two speeds, on something that might bend back:

```python
slow = fast = start
while True:
    slow = step(slow)
    fast = step(step(fast))
    if slow == fast:
        return True          # they met: there is a cycle
```

On a path with an end you never get here — the fast one runs off the end and you stop. On a loop, they
meet.

### Why the meeting must happen — this is the question

Interviewers ask *"why are you sure they meet?"* and the answer is short and worth having exactly.

Once **both** are inside the loop, look at the gap between them, measured the way round the loop from
`fast` to `slow`. Every step, `slow` advances 1 and `fast` advances 2, so **the gap shrinks by exactly
1 per step**.

A quantity that starts at some value less than the loop length and decreases by exactly one each step
must reach zero. And because it decreases by exactly one, **it cannot jump over zero** — there is no
way for the fast one to step past the slow one without landing on it.

So they meet, in at most one loop-length of steps after both are inside. That is the whole proof, and
"the gap shrinks by exactly one, so it cannot skip zero" is the sentence to say.

**The reason the fast one moves at 2 and not 3** is precisely this. At speed 3 the gap shrinks by 2 per
step, so it can go from 1 to −1 and step straight past. It still works out on a single loop for other
reasons, but the argument stops being one line — and the second phase below breaks. Use 2.

### Where the loop starts — Floyd's second phase

Detecting a loop is often not enough; you want the node where it begins. There is a small piece of
arithmetic that gives it, and it looks like magic until you see it once.

Let `μ` be the distance from the start to where the loop begins, and `λ` the loop's length.

When the two meet, `slow` has walked `d` steps and `fast` has walked `2d`. Both are on the loop, and
`fast` has gone round some whole number of extra loops, so:

```
2d - d = k·λ        →      d = k·λ
```

**The slow one has walked a whole number of loop-lengths.** Now, `slow` is `d − μ` steps into the loop.
If you start a fresh index at the beginning and move both one step at a time, then after `μ` steps the
fresh one is at the loop entry, and `slow` has moved `μ` further — reaching `d − μ + μ = d = k·λ` steps
into the loop, which is the loop entry again.

So:

```python
slow = start                     # reset one index to the beginning
while slow != fast:
    slow = step(slow)
    fast = step(fast)            # BOTH at speed 1 now
return slow                      # the loop entry
```

**Both move one step at a time in the second phase.** Leaving `fast` on two steps is the standard bug
and it gives a wrong answer with no error.

### The loop's length

Once they have met, stand still and walk one of them round until it comes back:

```python
length = 1
cur = step(meeting_point)
while cur != meeting_point:
    cur = step(cur)
    length += 1
```

### Arrays as paths: the trick that makes this apply everywhere

An array of numbers where every value is a valid index **is a path**. From position `i`, the next
position is `nums[i]`. Follow it and you are walking.

```
nums = [1, 3, 4, 2, 2]

0 -> nums[0]=1 -> nums[1]=3 -> nums[3]=2 -> nums[2]=4 -> nums[4]=2 -> nums[2]=4 -> ...
                                            ^                         ^
                                            the loop:  2 -> 4 -> 2 -> 4 ...
```

*Find the Duplicate Number*, LeetCode 287: `n + 1` values in the range `1..n`, exactly one repeated.
Because a value is repeated, **two different positions point at the same place**, which is exactly what
creates a loop — and the entry to that loop is the duplicated value. So Floyd's algorithm finds it in
`O(n)` time and `O(1)` space, without modifying the array and without a hash set.

That problem is famous precisely because those three constraints together rule out every obvious
approach: sorting modifies, a set costs space, and counting costs space.

The same trick applies to any **repeated function**. *Happy Number*: repeatedly replace `n` by the sum
of the squares of its digits. Either you reach 1, or you loop forever — and "loops forever" is exactly
what tortoise and hare detects, with two integers of memory.

---

## 4. The picture

The shape a path with a loop makes, and why it is called a **rho**:

```
   start
     |
     v
   ()---()---()---()          the tail: mu = 4 steps
                    \
                     v
                    ()---()
                    ^       \                the loop: lambda = 5
                     \       v
                      ()<---()
                        the rho shape:  a tail, then a circle
```

**What to notice:** the fast index gets into the circle first and goes round; the slow one arrives
later. Once both are on the circle there is no exit, which is why the meeting is forced.

The gap closing, step by step, with `λ = 5`:

```
   step   slow at   fast at   gap (fast -> slow, round the loop)
   ----   -------   -------   --------------------------------
     0       A         C           3
     1       B         E           2       gap shrinks by exactly 1
     2       C         B           1
     3       D         D           0   <-- they meet

   The gap goes 3, 2, 1, 0. It decreases by exactly one each step,
   so it CANNOT step over zero. That is the whole proof.
```

Finding the middle:

```
   index    0    1    2    3    4
          +----+----+----+----+----+
          |    |    |    |    |    |
          +----+----+----+----+----+
   start   s,f
   step 1       s         f
   step 2            s         f        fast + 1 = 5, not < 5, so stop
                     ^
                   slow = 2, the middle of 5

   even length, n = 4:
   start   s,f
   step 1       s         f
   step 2            s         (fast would be 4)   -> stop, slow = 2
                     ^
              the SECOND of the two middles
```

The array-as-a-path view, for `[1, 3, 4, 2, 2]`:

```
  index:  0    1    2    3    4
  value:  1    3    4    2    2

  walk:   0 -> 1 -> 3 -> 2 -> 4 -> 2 -> 4 -> 2 -> ...
          |---- tail ----|    |--- loop ---|
                mu = 3          lambda = 2

  Two positions (2 and 4) both hold the value 2, so two arrows point at
  index 2 — and that is exactly what makes a loop. The loop entry is 2,
  which is the duplicated value.
```

**What to notice:** the duplicate is not found by comparing values at all. It is found by noticing that
the path joins, and the join point *is* the duplicate. That reframing is the whole insight of LeetCode
287.

---

## 5. The code, built step by step

### The middle

```python
def middle_index(items: list[int]) -> int:
    if not items:
        return -1
    slow = fast = 0
    while fast + 1 < len(items):
        slow += 1
        fast += 2
    return slow
```

`fast + 1 < len(items)` asks *can fast take two more steps?* If it can, take them; otherwise stop.

For a linked list, where you cannot ask for a length, the same shape reads:

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
return slow
```

**`fast and fast.next`, in that order.** Python's `and` short-circuits, so if `fast` is `None` the
second test is never evaluated. Reverse them and you get `AttributeError: 'NoneType' object has no
attribute 'next'` on any even-length list. Linked lists arrive properly on
[day 078](../day-078-nodes-and-links/README.md); the ordering rule is worth carrying now.

### Cycle detection

```python
def has_cycle(step, start):
    slow = fast = start
    while True:
        slow = step(slow)
        fast = step(step(fast))
        if slow == fast:
            return True
```

For a structure that can end, you need the escape:

```python
while fast and fast.next:
    ...
return False        # fast ran off the end: no cycle
```

For a **function** that never ends — happy numbers, `nums[i]` where every value is a valid index —
there is nothing to run off, so `while True` is correct and the loop is guaranteed to terminate by the
gap argument.

### Where the loop begins

```python
    # phase 1: find a meeting point
    slow = fast = start
    while True:
        slow = step(slow)
        fast = step(step(fast))
        if slow == fast:
            break

    # phase 2: reset one to the start, then move BOTH at speed 1
    slow = start
    while slow != fast:
        slow = step(slow)
        fast = step(fast)
    return slow
```

Two things that are easy to get wrong and are the whole of this half:

**Reset `slow`, not `fast`.** It does not matter which name you reset as long as one goes back to the
start and one stays at the meeting point — but be deliberate, because swapping them by accident gives
a wrong answer with no error.

**Both move one step in phase two.** The arithmetic in §3 depends on it.

### Find the Duplicate Number

```python
def find_duplicate(nums: list[int]) -> int:
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
```

Note the starting point: `nums[0]`, which is one step in from index 0. Starting both at `0` works too
as long as you are consistent about taking the first step before the first comparison — otherwise
`slow == fast` is true immediately and you exit at once. **This off-by-one is the commonest way to get
this problem wrong**, and the tell is that it returns the value at index 0.

### Happy Number

```python
def is_happy(n: int) -> bool:
    def next_value(x: int) -> int:
        total = 0
        while x:
            x, digit = divmod(x, 10)
            total += digit * digit
        return total

    slow = fast = n
    while True:
        slow = next_value(slow)
        fast = next_value(next_value(fast))
        if slow == fast:
            return slow == 1
```

The sequence either reaches 1 — which is itself a loop of length one, since `1 → 1` — or enters a
different loop. So the two always meet, and **what they meet on is the answer**: 1 means happy,
anything else means not.

### The complete solutions

```python
def middle_index(items: list[int]) -> int:
    """Index of the middle. On even lengths, the SECOND middle (LeetCode 876 convention)."""
    if not items:
        return -1
    slow = fast = 0
    while fast + 1 < len(items):        # can fast take two more steps?
        slow += 1
        fast += 2
    return slow


def has_cycle(step, start):
    """Floyd's cycle detection on any repeated function. O(1) space."""
    slow = fast = start
    while True:
        slow = step(slow)
        fast = step(step(fast))
        if slow == fast:
            return True


def cycle_start_and_length(step, start) -> tuple[object, int]:
    """The entry point of the loop, and its length."""
    slow = fast = start
    while True:                          # phase 1: meet somewhere inside the loop
        slow = step(slow)
        fast = step(step(fast))
        if slow == fast:
            break

    length = 1                           # phase 2a: walk one all the way round
    cur = step(slow)
    while cur != slow:
        cur = step(cur)
        length += 1

    slow = start                         # phase 2b: reset one, BOTH at speed 1
    while slow != fast:
        slow = step(slow)
        fast = step(fast)
    return slow, length


def find_duplicate(nums: list[int]) -> int:
    """LeetCode 287. n+1 values in 1..n, one repeated. O(n) time, O(1) space,
    without sorting and without modifying the array.

    nums is a path: from i you go to nums[i]. A repeated value means two
    positions point at the same place, which makes a loop — and the loop
    entry IS the duplicate.
    """
    slow = fast = nums[0]                # one step in, so the first comparison is meaningful
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:                  # both at speed 1
        slow = nums[slow]
        fast = nums[fast]
    return slow


def is_happy(n: int) -> bool:
    """LeetCode 202. Repeatedly sum the squares of the digits. Loops or reaches 1."""
    def next_value(x: int) -> int:
        total = 0
        while x:
            x, digit = divmod(x, 10)
            total += digit * digit
        return total

    slow = fast = n
    while True:
        slow = next_value(slow)
        fast = next_value(next_value(fast))
        if slow == fast:
            return slow == 1             # 1 is itself a loop of length 1


if __name__ == "__main__":
    for case in ([1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6]):
        i = middle_index(case)
        print(case, "-> index", i, "value", case[i])
    # [1,2,3,4] -> index 2 value 3      <- the SECOND middle

    for case in ([1, 3, 4, 2, 2], [3, 1, 3, 4, 2], [1, 1], [1, 1, 2],
                 [2, 2, 2, 2, 2], [1, 4, 6, 6, 6, 6, 3, 2, 5]):
        print(case, "-> duplicate", find_duplicate(list(case)))
    # [1,3,4,2,2] -> 2   [3,1,3,4,2] -> 3   [1,4,6,6,6,6,3,2,5] -> 6

    print([(n, is_happy(n)) for n in (19, 2, 1, 7, 4, 100)])
    # [(19, True), (2, False), (1, True), (7, True), (4, False), (100, True)]
```

---

## 6. What it costs

### Finding the middle

`fast` advances by 2 each turn and stops near `n`, so the loop runs about `n/2` times, each doing
constant work. **O(n) time, O(1) space** — two integers.

Against the obvious alternative on a linked list — walk it once to count, then walk half of it again —
that is `2n` steps against `1.5n`. Same complexity; the reason to prefer one pass is that **on a stream
you cannot walk it twice**, which is the honest answer when asked why it matters.

### Cycle detection

Let `μ` be the tail length and `λ` the loop length.

**Phase 1.** `slow` reaches the loop after `μ` steps. From there the gap closes by one per step, and
the gap is less than `λ`, so they meet within `λ` more. Total at most `μ + λ` iterations, and
`μ + λ ≤ n`. **O(n) time.**

**Phase 2a**, the length: one walk round the loop, `λ` steps.
**Phase 2b**, the entry: `μ` steps.

**Total O(n) time, O(1) space** — a fixed number of variables regardless of the input size.

### Against the hash-set version

```python
seen = set()
while node:
    if node in seen: return True
    seen.add(node)
    node = node.next
```

Also `O(n)` time, and **`O(n)` space**. On ten million nodes:

```
hash set : 10,000,000 entries × ~50 bytes ≈ 500 MB
Floyd    : two variables                  ≈ 16 bytes
```

**That is the entire reason Floyd's algorithm is worth knowing.** Write the set version first, state its
cost, then offer the constant-space one — that sequence is the complete answer.

### `find_duplicate`, and why the constraints matter

The problem forbids modifying the array and asks for constant space, which rules out:

```
sort then scan          : O(n log n), and it MODIFIES the array
a hash set              : O(n) time, O(n) space
counting array          : O(n) time, O(n) space
marking values negative : O(n) time, O(1) space — but MODIFIES the array
binary search on value  : O(n log n) time, O(1) space, no modification
Floyd                   : O(n) time, O(1) space, no modification    <- the intended answer
```

That table is worth having, because a good answer walks down it. The binary-search-on-value approach
is a genuine alternative and worth naming: count how many values are `≤ mid`; if that count exceeds
`mid`, the duplicate is in the lower half.

### `is_happy`

The sequence of digit-square-sums drops quickly and then stays small: for any number below 1,000, the
next value is at most `9² × 3 = 243`. So the reachable set is tiny and both `μ` and `λ` are small
constants — in practice under a dozen steps. **Effectively O(log n) time** to reduce the original
number, then constant, and **O(1) space**.

### The number to have ready

> Floyd's is `O(n)` time and `O(1)` space, against `O(n)` space for the hash-set version — 16 bytes
> against 500 MB on ten million nodes. The meeting is guaranteed because the gap shrinks by exactly one
> per step and therefore cannot skip zero.

---

## 7. The traps

### The real error: testing `fast.next` before `fast`

```python
while fast.next and fast:
    slow = slow.next
    fast = fast.next.next
```

```
AttributeError: 'NoneType' object has no attribute 'next'
```

On any even-length list, `fast` becomes `None` and the first half of the condition dereferences it.
`and` evaluates left to right and short-circuits, so **`fast` must be tested first**:
`while fast and fast.next`. The ordering is doing real work, not stylistic.

### The near-miss: exiting immediately

```python
def find_duplicate(nums):
    slow = fast = 0                # both at index 0, no first step
    while slow != fast:            # false immediately!
        ...
```

`slow == fast` is true before anything moves, so the loop never runs. The `while True` / `break`
structure exists precisely to force **one step before the first comparison**. If you prefer a
condition-first loop, you must offset the starting positions:

```python
slow, fast = nums[0], nums[nums[0]]
while slow != fast:
    slow = nums[slow]
    fast = nums[nums[fast]]
```

Both forms are correct; mixing them is not.

### The near-miss: leaving `fast` at double speed in phase two

```python
slow = start
while slow != fast:
    slow = step(slow)
    fast = step(step(fast))        # still doubling — WRONG
return slow
```

Returns a point inside the loop that is not the entry, with no error. The derivation in §3 requires
both to move one step at a time — that is what makes the fresh index and `slow` meet exactly at the
entry.

### The near-miss: the even-length middle

```python
print(middle_index([1, 2, 3, 4]))     # 2, the value 3
```

Is that right? It depends on the problem. LeetCode 876 wants the second middle; a "split the list in
half" problem usually wants the **first**, so that the halves are equal. Changing `fast + 1 <` to
`fast + 2 <` gives the first. **This is a contract question, and getting it wrong costs a submission
for otherwise perfect code.**

### The near-miss: assuming a cycle exists

```python
def has_cycle(step, start):
    slow = fast = start
    while True:
        slow = step(slow)
        fast = step(step(fast))
        if slow == fast:
            return True
```

On a structure with an end, this never returns `False` — it runs off the end, or loops forever. For
anything finite you need the escape condition. `while True` is only correct for a **total function**
where every value maps to another valid value, which is true of happy numbers and of an array where
every entry is a valid index, and false of a linked list.

### The near-miss: speed 3

```python
fast = step(step(step(fast)))
```

The gap now shrinks by 2 per step, so it can go from 1 to −1 and jump over zero. It happens to still
work in many cases for other reasons, but the one-line proof is gone and the phase-two arithmetic is
wrong. **There is no benefit and a real cost. Use 2.**

### The contract corner: what "middle" means for length 1 and 2

`[1]` — the middle is index 0. `[1, 2]` — index 1 under this convention, index 0 under the other. Both
are single-line answers and both are easy to get wrong by not thinking about them. Test them.

---

## 8. In the interview

### How it gets asked

- *"Find the middle element in a single pass."* — usually about a linked list, where the single-pass
  constraint is the whole point.
- *"Does this linked list have a cycle?"* — LeetCode 141, then *"find where it starts"*, which is
  LeetCode 142 and the interesting half.
- *"Find the duplicate number without modifying the array and in constant space."* — LeetCode 287. The
  constraints are the question.
- *"Is this a happy number?"* — LeetCode 202, where "does it loop?" is the whole problem.

### What to say out loud, in the first ninety seconds

1. **Name the technique.** *"Two indices at different speeds — Floyd's, tortoise and hare. Slow moves
   one step, fast moves two."*
2. **Say what the speeds buy.** *"For the middle: when fast reaches the end it has gone twice as far, so
   slow is halfway. For cycles: on a straight path fast pulls away, but on a loop it comes round and
   catches slow from behind."*
3. **Give the obvious solution and its cost first.** *"The straightforward way to detect a cycle is a
   hash set of everything visited — O(n) time and O(n) space."*
4. **Then offer the improvement.** *"Floyd's does it in O(1) space, which on ten million nodes is two
   variables instead of half a gigabyte."*
5. **Give the meeting proof, unprompted.** *"They must meet, because once both are in the loop the gap
   closes by exactly one per step — and since it changes by exactly one it can't skip over zero."*
6. **Ask the contract question for the middle.** *"On an even-length input there are two middles — do
   you want the first or the second?"*
7. **Flag the short-circuit if it is a linked list.** *"The condition is `fast and fast.next`, in that
   order, or it dereferences None on an even-length list."*

### The follow-ups

**"Why are you sure the fast pointer catches the slow one?"**
Once both are inside the loop, consider the gap from fast to slow measured the way round the loop. Each
step, slow advances one and fast advances two, so the gap decreases by exactly one. It starts at some
value smaller than the loop length and decreases by one every step, so it must reach zero — and
because it changes by exactly one, it cannot step over zero and miss. So they land on the same point.
The bound falls out too: slow enters the loop after μ steps, and they meet within λ more, so it is at
most μ + λ iterations, which is at most n. That is also why the fast pointer moves at two and not
three: at three the gap shrinks by two per step, so it can go from 1 to −1 and jump the meeting, and
the one-line argument is gone.

**"Now find where the cycle starts."**
There is a short derivation. Let μ be the distance from the start to the loop entry and λ the loop
length. When they meet, slow has taken d steps and fast has taken 2d, and since both are on the loop,
fast has covered a whole number of extra loops — so 2d − d = kλ, meaning d is a multiple of λ. Now
reset one index to the start and move **both** one step at a time. After μ steps the reset one is at the
loop entry, and the other has advanced μ from a position that was d − μ into the loop, putting it at d
steps in — which is a multiple of λ, so it is at the entry too. They meet exactly at the loop start.
The two things people get wrong are resetting the wrong one and leaving the fast pointer at double
speed in the second phase; both give a wrong answer with no error.

**"Find the duplicate number in an array of n+1 values from 1 to n, without modifying it and in O(1)
space."**
The reframing is the whole answer: treat the array as a path where from index `i` you move to index
`nums[i]`. Since every value is between 1 and n, every step lands on a valid index, so the walk never
ends — which means it must eventually repeat, so there is a cycle. And because one value appears twice,
two different positions point at the same index, and that convergence is exactly where the cycle
begins. So the entry point of the cycle is the duplicated value, and Floyd's finds it in O(n) time and
O(1) space. It is worth saying why the alternatives are ruled out: sorting modifies the array, a hash
set or a counting array is O(n) space, and marking values negative modifies it. The one other
legitimate answer is binary search on the value range — count how many entries are at most mid, and if
that exceeds mid the duplicate is below — which is O(n log n) time and O(1) space.

**"How does this apply to a happy number?"**
Repeatedly replacing a number by the sum of the squares of its digits is just a function applied over
and over, so the sequence is a path exactly like the array case. Either it reaches 1 — and 1 maps to
itself, so that is a loop of length one — or it enters some other loop. Since the values are bounded —
anything under a thousand maps to at most 243 — the sequence cannot escape to infinity, so a loop is
guaranteed. Run tortoise and hare, and when they meet, look at what they met on: 1 means happy,
anything else means not. That is O(1) space, against the obvious solution of keeping a set of every
value seen. The set version is perfectly acceptable here because the reachable set is tiny, so I would
mention that the space saving is a demonstration rather than a necessity on this particular problem.

### A model answer

> "First a contract question, since this is a linked list: on an even-length list there are two
> middles — do you want the first or the second?
>
> ...The second. Fine.
>
> The naive approach is two passes: walk the list to count the nodes, then walk half of it again. That
> is O(n) and correct, and it needs the list twice.
>
> One pass uses two pointers at different speeds. Slow advances one node, fast advances two. When fast
> reaches the end it has travelled twice as far, so slow is exactly at the middle.
>
> ```python
> slow = fast = head
> while fast and fast.next:
>     slow = slow.next
>     fast = fast.next.next
> return slow
> ```
>
> The condition has to be `fast and fast.next` in that order. Python's `and` short-circuits, so if
> `fast` is None the second test is never evaluated — reverse them and you get an AttributeError on
> every even-length list. And this particular loop condition is what gives the second middle; stopping
> one step earlier gives the first.
>
> O(n) time and O(1) space. The reason one pass matters rather than two isn't the constant factor —
> it's that on a stream, or anything you can only traverse once, there is no second pass available.
>
> The same two speeds answer a different question, which is whether the list has a cycle. On a straight
> list, fast reaches the end and you stop. If there's a cycle, fast comes round and catches slow from
> behind, and that meeting is the proof.
>
> The reason it must meet is worth stating: once both pointers are inside the cycle, the gap between
> them closes by exactly one node per step, because slow moves one and fast moves two. A quantity that
> decreases by exactly one each step must hit zero, and it can't jump over zero. So they meet within one
> cycle-length.
>
> The obvious alternative is a hash set of visited nodes — same O(n) time, but O(n) space. On ten
> million nodes that's roughly half a gigabyte against two variables, and that gap is the entire reason
> the technique is worth knowing.
>
> If you also want where the cycle starts, there's a second phase: reset one pointer to the head and
> move both one step at a time. They meet at the cycle entry, and the arithmetic is that when they first
> met, slow had walked a whole number of cycle-lengths."

---

## 9. Recall card

- **Slow moves 1, fast moves 2.** When fast ends, slow is at the **middle**. If they ever meet, there is
  a **cycle**.
- **Why they must meet:** once both are in the loop the gap shrinks by **exactly one** per step, so it
  cannot skip zero. That is why fast moves 2, not 3.
- **Cycle start:** reset one to the beginning, then move **both at speed 1**. They meet at the entry.
- **`while fast and fast.next`** — that order, or you dereference `None` on an even-length list.
- **An array where every value is a valid index is a path.** A repeated value makes a loop, and the
  loop entry is the duplicate — `O(n)` time, `O(1)` space, no modification.
