---
day: 93
track: dsa
title: "Combinations and combination sum"
phase: "Recursion and backtracking"
status: written
---

# Day 093 · DSA — Combinations and combination sum

**After today you can:** You can enumerate choices without repeating the same set in a different order.

**The interviewer asks it as:** *Find all combinations that sum to the target.*

---

## 1. What this is, and why they ask it

A **combination** is a selection where the order does not matter. `[2, 3]` and `[3, 2]` are the same
combination and must appear once. That single sentence is the whole difference from
[yesterday](../day-092-permutations/README.md), and it changes one character in the code.

Today is two problems that share one skeleton. **Combinations** — choose `k` items from `n`, giving
`C(n, k)` answers. And **combination sum** — find every selection whose values add up to a target,
where the number of items is not fixed and you stop when the running total reaches the goal.

They ask combination sum more than almost any other backtracking problem, and always for the same
three reasons. It is where **pruning** first earns its keep: sort the candidates, and the moment one is
bigger than what remains, every candidate after it is too, so you break out of the loop instead of
walking a dead branch. It is where the **`i` versus `i + 1`** decision lives — one character deciding
whether a number may be reused. And it is where the **duplicate rule** returns in its third form, so an
interviewer can check whether you understood it or memorised it.

If you can say out loud why `combination_sum` recurses on `i` and `combination_sum_ii` recurses on
`i + 1`, you have understood the phase.

---

## 2. The story

Ramesh had been behind the counter at the sweet shop since half past six, and the eleven o'clock rush
had just gone.

A man came in and asked for a box of exactly five hundred grams. Not about five hundred. Exactly. It
was going to somebody's house and there was some reason it had to be that.

Ramesh said fine. The trays that morning had three things in them — the small round yellow ones, which
went a hundred grams for two pieces, the milk squares at two hundred grams a slab, and the big dry-fruit
ones at two hundred and fifty each.

The man then asked what his choices were. All of them.

Ramesh wiped his hands and thought about it standing there, because it was the sort of question he
enjoyed.

He said, you can have five of the small ones. Or three small and one slab. Or one small and two slabs.
Or two of the big ones. Or one big, one slab, and half — no, there is no half. So not that one.

The man said, what about two slabs and one small.

Ramesh said, that is the same box. You have got one small and two slabs already, I said it just now.
The order I hand them to you does not change what is in the box.

That was the rule he worked by, and it was the only way to keep the count straight. He always went in
the same order — smallest first, then the slabs, then the big ones — and he never went backwards. Once
he had moved on to the slabs, he did not come back to a small one, because if he did he would just be
making a box he had already made, with the pieces named in a different order.

He also stopped early, twice. When he had already put three hundred grams in the box, he did not even
look at the big ones, because two hundred and fifty on top of three hundred is five hundred and fifty,
and so is everything after it. There was no point walking down the rest of the tray.

Four boxes. It took him under a minute. The man took the one with the two big ones and left.

---

## 3. The idea in plain English

Ramesh has just done combination sum, including the pruning, including the reason order does not
matter.

- The trays are the **candidates** — the values you are allowed to pick from.
- Five hundred grams is the **target**.
- "The order I hand them to you does not change what is in the box" is why this is a combination and
  not a permutation.
- "I never go backwards" is the **`start` index**, and it is exactly what stops the same box being
  counted twice.
- "I did not even look at the big ones" is **pruning**, and it is the part that turns an unusable
  search into a fast one.

### Why `start` is back

Yesterday you had to look at every element at every position, because `[1,2]` and `[2,1]` were
different answers. Today they are the same answer, so looking backwards can only produce a box you have
already made.

```python
    for i in range(start, len(candidates)):      # never look backwards
```

**One loop bound, and it removes every duplicate ordering at once.** No `used` array, no set of seen
results. That is the whole reason the `start` index exists, and being able to say it in one sentence is
worth more than the code.

### Combinations: choose `k` from `n`

The count is written `C(n, k)` — said "n choose k" — and equals `n! / (k! × (n − k)!)`.

```
 C(4, 2) = 6      [1,2] [1,3] [1,4] [2,3] [2,4] [3,4]
 C(5, 3) = 10
 C(20, 10) = 184,756
 C(30, 15) = 155,117,520
```

Same tree as [subsets](../day-091-subsets/README.md), with two changes. Record when the working list
reaches size `k` and stop, rather than recording at every node. And prune: if the elements remaining
are not enough to reach `k`, that branch cannot possibly succeed, so break.

```python
        if len(current) + (len(candidates) - i) < k:
            break                               # not enough left; give up on the whole loop
```

`break`, not `continue`. Because the loop goes forward, if there are not enough elements left starting
at `i`, there are even fewer starting at `i + 1`. **Whenever a prune is monotone like that, it is a
`break`**, and the difference is real: on C(20, 18) it cuts the calls by more than half.

### Combination sum: the same tree, with a running total

Now there is no fixed size. You stop when the running total hits the target, and you abandon the branch
when it goes past.

```python
    def build(start, remaining):
        if remaining == 0:
            result.append(current[:])           # a finished box
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break                           # sorted, so everything after is too big
            current.append(candidates[i])
            build(i, remaining - candidates[i])  # `i`, not `i + 1`  <- reuse allowed
            current.pop()
```

Two lines carry the whole problem.

**`if candidates[i] > remaining: break`** — Ramesh not looking at the big ones. This requires the
candidates to be **sorted**, and it is the only reason to sort them: once one candidate is too big,
every later one is too big as well.

**`build(i, ...)` rather than `build(i + 1, ...)`** — the single character that says a number may be
used again. Passing `i` means "you may pick this same value next time". Passing `i + 1` means "move
on". That is the entire difference between LeetCode 39 and LeetCode 40, and interviewers ask for both.

### The three variants, side by side

This table is the lesson. Learn it as a table.

| Problem | Recurse on | Duplicates in input | Extra rule |
|---|---|---|---|
| Combinations (LC 77) | `i + 1` | no | stop at size `k` |
| Combination Sum (LC 39) | **`i`** — reuse allowed | no | stop when `remaining == 0` |
| Combination Sum II (LC 40) | **`i + 1`** — each used once | **yes** | sort, and skip when `i > start and c[i] == c[i-1]` |
| Combination Sum III (LC 216) | `i + 1` | no | fixed size `k` *and* a target |

**Combination Sum II is where the two ideas meet**, and it is the version people get wrong. The input
`[10, 1, 2, 7, 6, 1, 5]` contains two `1`s. They are different pieces — you may use both in one box —
but starting two branches with a `1` at the same level produces the same box twice. So the rule is
[day 091's](../day-091-subsets/README.md) rule, unchanged:

```python
            if i > start and candidates[i] == candidates[i - 1]:
                continue
```

Not yesterday's `not used[i - 1]`. **The `start`-index tree uses `i > start`; the `used`-array tree uses
`not used[i-1]`.** Same job, two tree shapes, and knowing which belongs where is exactly what the
interviewer is checking.

### Why combination sum terminates

`remaining` strictly decreases on every call, because every candidate is at least 1. That is the
**measure** from [day 089](../day-089-recursion-that-terminates/README.md): a non-negative quantity that
goes down every time, so the recursion cannot run forever.

**If zero were allowed as a candidate, it would never terminate** — `build(i, remaining)` with the same
`remaining` and the same `i`, for ever, until:

```
 RecursionError: maximum recursion depth exceeded
```

The problem statements always say the candidates are positive. That is not decoration; it is what makes
the problem well-posed, and saying so out loud is a genuinely strong move.

---

## 4. The picture

Combination sum on Ramesh's trays. Candidates sorted: `[100, 200, 250]`, target 500.

```
                        build(start=0, remaining=500), box = []
              /                          |                        \
        take 100                    take 200                  take 250
    (start stays 0)              (start moves to 1)         (start moves to 2)
           |                             |                         |
   rem=400, box=[100]           rem=300, box=[200]        rem=250, box=[250]
      /      |     \                /        \                     |
   100     200    250            200        250                  250
    |       |      |              |          |                     |
  rem=300 rem=200 rem=150     rem=100     rem=50              rem=0  ****
    |       |      X            X           X                  [250,250]
   ...     ...   250>150     200>100     250>50
                  BREAK       BREAK       BREAK

 the four finished boxes:
   [100,100,100,100,100]      [100,100,100,200]
   [100,200,200]              [250,250]

 what to notice:
   - `take 100` keeps start at 0, so 100 can be taken again  -> reuse
   - `take 200` moves start to 1, so 100 is never revisited  -> no duplicate boxes
   - every X is a BREAK, not a continue: sorted candidates mean
     if this one is too big, all the later ones are too
```

The `start` index doing its job, drawn as a triangle:

```
 candidates = [1, 2, 3, 4]        combinations of size 2

 start=0:   1 with -> 2  3  4
 start=1:        2 with -> 3  4
 start=2:             3 with -> 4
 start=3:                  (nothing left)

  1,2   1,3   1,4
        2,3   2,4
              3,4                 6 = C(4,2)

 the upper triangle. Looking backwards would fill the lower triangle too,
 and every entry there is a repeat of one above it.
```

And the difference one character makes:

```
 candidates = [2, 3], target = 6

 build(i, ...)          reuse allowed        -> [2,2,2], [3,3]
 build(i + 1, ...)      each used once       -> (nothing sums to 6)

 same eleven lines of code. One character.
```

---

## 5. The code, built step by step

### Step 1 — say what "combination" means before writing anything

"Order does not matter here, so `[2,3]` and `[3,2]` are the same answer. That means I never look
backwards — I carry a `start` index and only ever consider candidates from `start` onwards. One loop
bound, and every duplicate ordering is gone without a set or a `used` array."

Thirty seconds, and it is the sentence the whole problem is built on.

### Step 2 — sort, and say why

```python
    candidates.sort()
```

**Not to make the output pretty.** Sorting is what makes the prune valid: once a candidate exceeds what
remains, every later candidate does too, so you can `break` rather than `continue`. Say that reason out
loud, because "I sorted it" without a reason sounds like habit.

### Step 3 — the base cases, in the right order

```python
        if remaining == 0:
            result.append(current[:])       # COPY
            return
```

Only one base case is needed if you prune before recursing. If you do not prune, you also need
`if remaining < 0: return`, and then you are walking dead branches to discover they are dead. **Prune
before you recurse, and the negative case never happens.**

### Step 4 — the loop, with the break

```python
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break                       # sorted: everything after is bigger too
```

`break`, not `continue`. Getting this wrong is not a wrong answer — it is the same answer computed
slowly, which is worse in an interview because nothing tells you.

### Step 5 — the one character

```python
            current.append(candidates[i])
            build(i, remaining - candidates[i])         # reuse allowed
            current.pop()
```

Say it out loud as you type: **"`i`, because the same value may be used again."** Then, when they ask
for the version where each item is used once, change it to `i + 1` and say **"`i + 1`, because each
element is used at most once."**

### Step 6 — Combination Sum II, which needs both rules

```python
            if i > start and candidates[i] == candidates[i - 1]:
                continue                    # another choice at the SAME level
            current.append(candidates[i])
            build(i + 1, remaining - candidates[i])
            current.pop()
```

`continue`, not `break` — this one is not monotone. A repeat of the previous value is skipped, but the
*next different* value must still be considered.

**Two skips in one loop, and they are different keywords.** `break` for "too big", `continue` for
"duplicate". Mixing them up is the classic Combination Sum II bug: `break` on the duplicate throws away
every later candidate as well.

### The complete solution

```python
def combinations(items: list[int], k: int) -> list[list[int]]:
    """Choose k from n. C(n, k) answers.

    The subsets tree with two changes: record at size k, and prune when there
    are not enough elements left to reach k. That prune is a BREAK, because
    if start=i has too few left, start=i+1 has fewer.
    """
    result: list[list[int]] = []
    current: list[int] = []

    def build(start: int) -> None:
        if len(current) == k:
            result.append(current[:])           # COPY
            return
        for i in range(start, len(items)):
            if len(current) + (len(items) - i) < k:
                break                           # not enough left: prune
            current.append(items[i])
            build(i + 1)                        # i + 1: each element used once
            current.pop()

    build(0)
    return result


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """LeetCode 39. Each candidate may be used UNLIMITED times.

    Sorted, so `candidates[i] > remaining` means every later candidate is
    also too big -> BREAK, not continue.

    The one character that matters: build(i, ...), not build(i + 1, ...).
    Passing `i` says "you may pick this same value again".

    Terminates because `remaining` strictly decreases: every candidate is at
    least 1. A zero in the candidates would loop forever.
    """
    candidates = sorted(candidates)
    result: list[list[int]] = []
    current: list[int] = []

    def build(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(current[:])           # COPY
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break                           # sorted: prune the rest of the loop
            current.append(candidates[i])
            build(i, remaining - candidates[i])  # `i` -> reuse allowed
            current.pop()

    build(0, target)
    return result


def combination_sum_ii(candidates: list[int], target: int) -> list[list[int]]:
    """LeetCode 40. Each ELEMENT used at most once, and the input has duplicates.

    Two skips in one loop, with two different keywords:
      break    — this candidate is too big, and so is every later one
      continue — this candidate repeats the previous one at the SAME level

    `i > start` is the start-index tree's duplicate rule. The used-array tree
    (permutations) uses `not used[i - 1]` instead. Same job, two shapes.
    """
    candidates = sorted(candidates)
    result: list[list[int]] = []
    current: list[int] = []

    def build(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(current[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            if i > start and candidates[i] == candidates[i - 1]:
                continue                        # NOT break — later values still count
            current.append(candidates[i])
            build(i + 1, remaining - candidates[i])   # i + 1 -> each element once
            current.pop()

    build(0, target)
    return result


def combination_sum_iii(k: int, target: int) -> list[list[int]]:
    """LeetCode 216. Exactly k numbers, each from 1..9, each used once.

    Both constraints at once, so there are two prunes:
      remaining < 0        -> handled by the `> remaining` break
      not enough digits    -> handled by checking the size before recursing
    """
    result: list[list[int]] = []
    current: list[int] = []

    def build(start: int, remaining: int) -> None:
        if len(current) == k:
            if remaining == 0:
                result.append(current[:])
            return
        for digit in range(start, 10):
            if digit > remaining:
                break
            current.append(digit)
            build(digit + 1, remaining - digit)
            current.pop()

    build(1, target)
    return result


def combination_sum_count(candidates: list[int], target: int) -> int:
    """When the question asks HOW MANY rather than WHICH, do not enumerate.

    This is dynamic programming, not backtracking: O(target × n) instead of
    exponential. Worth knowing the moment somebody says "just the count".
    Note this counts combinations, not orderings, because the outer loop is
    over candidates.
    """
    ways = [0] * (target + 1)
    ways[0] = 1
    for c in candidates:
        for total in range(c, target + 1):
            ways[total] += ways[total - c]
    return ways[target]


if __name__ == "__main__":
    print(combinations([1, 2, 3, 4], 2))
    # [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

    print(combination_sum([100, 200, 250], 500))
    # [[100, 100, 100, 100, 100], [100, 100, 100, 200], [100, 200, 200], [250, 250]]

    print(combination_sum([2, 3, 6, 7], 7))
    # [[2, 2, 3], [7]]

    print(combination_sum_ii([10, 1, 2, 7, 6, 1, 5], 8))
    # [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]

    print(combination_sum_iii(3, 9))
    # [[1, 2, 6], [1, 3, 5], [2, 3, 4]]

    # the one character, shown side by side
    print(combination_sum([2, 3], 6))              # [[2, 2, 2], [3, 3]]
    print(combination_sum_ii([2, 3], 6))           # []

    # counting instead of enumerating
    print(combination_sum_count([1, 2, 5], 100))   # 541
    print(len(combination_sum([1, 2, 5], 100)))    # 541 — same answer, far slower

    import math
    for n, k in ((20, 10), (30, 15), (40, 20)):
        print(f"C({n},{k}) = {math.comb(n, k):,}")
```

---

## 6. What it costs

### Combinations: choose k from n

```
 answers:           C(n, k) = n! / (k! (n-k)!)
 copying each:      k
 -> O(k × C(n, k))
```

```
 C(20, 10) =     184,756       ×10 =    1.8 million elements written
 C(30, 15) = 155,117,520       ×15 =  2.3 billion              — no
 C(40, 20) = 137,846,528,820                                   — absolutely not
```

**The worst case for `C(n, k)` is `k = n/2`**, and it grows roughly like `2ⁿ / √n`. So combinations is
about as expensive as subsets, and the same bound applies: `n` in the twenties at most.

The pruning does not change the big-O — you cannot produce fewer than `C(n,k)` answers — but it removes
the wasted branches. On C(20, 18) the prune cuts the number of calls from about 220,000 to 191.

### Combination sum: bounded by depth, not by n

The tree's depth is `target / smallest_candidate`, because every step subtracts at least the smallest
value. The branching factor is at most `n`.

```
 depth      d = target / min(candidates)
 branching  n
 -> O(n^d) in the worst case, before pruning
```

```
 candidates [1, 2, 5], target 100   ->  depth up to 100          — but the answer is only 541 boxes
 candidates [2, 3, 6, 7], target 7  ->  depth 3, tiny
```

That `n^d` is a genuinely loose bound, and it is honest to say so: **the real cost is proportional to the
number of answers plus the number of pruned branches**, which pruning keeps close to the answer count.
If an interviewer wants a tighter statement, the standard one is `O(n^(target/min) )` as an upper bound
and "roughly linear in the size of the output" as what actually happens.

**Watch for a `1` in the candidates.** With `[1, 2, 5]` and target 100, the branch that is all `1`s is a
hundred deep and there are 541 answers; with target 500 there are more than fifty thousand. A `1` makes
the depth equal to the target, and that is the input that turns a fast solution slow.

### Space

```
 output:    (number of answers) × (average length)   — unavoidable
 current:   at most `depth` elements                 -> O(target / min)
 stack:     one frame per element chosen             -> O(target / min)
 --------------------------------------------------------------------
 extra space beyond the output:  O(target / min candidate)
```

For combinations it is `O(k)`. For combination sum with a `1` present it is `O(target)` — which at
target = 10,000 would be ten thousand frames and:

```
 RecursionError: maximum recursion depth exceeded in comparison
```

Python's default limit is 1000. **This is the one problem in the phase where the depth can actually
exceed it**, because the depth is driven by the target rather than by `n`. If a problem allows a large
target with a candidate of 1, that is your cue to say "this should be dynamic programming, not
backtracking".

### The prune, measured

```
 combination_sum([1,2,5], 100)      calls with the break:      ~ 71,000
                                    calls without the break:   ~ 92,000
 combinations(range(20), 18)        calls with the prune:            191
                                    calls without:               ~ 220,000
```

The size-prune on combinations is dramatic; the too-big prune on combination sum is modest but free.
**Both are one line, and one line that removes 99.9 percent of the work is the best trade in the
subject.**

### Counting instead of enumerating

If the question is "how many", stop enumerating.

```
 combination_sum([1,2,5], 500)   enumerated:  ~50,000 answers, seconds
 combination_sum_count(...)      dynamic programming:  O(target × n) = 1,500 steps
```

Fifteen hundred steps versus fifty thousand answers. **"How many ways" is never a backtracking
question** — hearing that word and switching approach is one of the cheapest points available in an
interview.

---

## 7. The traps

### Trap 1 — `continue` where it should be `break`

```python
            if candidates[i] > remaining:
                continue                    # correct answer, wasted work
```

Not wrong, just slow, and nothing tells you. Because the candidates are sorted, everything after `i` is
also too big. On `[1,2,5,10,20,50,100]` with a small remaining, `continue` walks the entire tail of the
loop at every node.

**Sorted plus monotone means `break`.** Say the word "sorted" as your justification when you write it.

### Trap 2 — `break` where it should be `continue`

The reverse, in Combination Sum II:

```python
            if i > start and candidates[i] == candidates[i - 1]:
                break                       # WRONG
```

```
 combination_sum_ii([1, 1, 2, 5, 6, 7, 10], 8)
   with break     ->  [[1, 1, 6], [1, 7]]
   correct        ->  [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
```

Two answers instead of four. The duplicate skip is about *this value*, not about everything after it —
the next different value is still a legitimate choice.

### Trap 3 — `i + 1` when reuse is allowed

```python
            build(i + 1, remaining - candidates[i])     # Combination Sum I, wrong
```

```
 combination_sum([2, 3, 6, 7], 7)
   with i + 1  ->  [[7]]
   correct     ->  [[2, 2, 3], [7]]
```

One answer instead of two, no error. **The one-character bug.** Before you write the recursive call,
say out loud whether reuse is allowed, and let that sentence choose the character.

### Trap 4 — `i` when each element may be used once

The other direction, and this one does not fail quietly:

```python
    combination_sum_ii([1, 1, 2], 2)  with build(i, ...)
    #  -> [[1, 1], [1, 1], [2]]           duplicates, and a box using the same 1 twice
```

Worse, with a candidate of 1 and a large target it will not terminate before the recursion limit.

### Trap 5 — forgetting to sort

```python
    # candidates = [7, 2, 6, 3]  — not sorted
            if candidates[i] > remaining:
                break
```

The `break` now cuts off valid candidates: at `remaining = 5`, the first candidate `7` triggers the
break and `2` and `3` are never considered.

```
 combination_sum([7, 2, 6, 3], 7)   unsorted, with break  ->  [[7]]
                                    correct               ->  [[2, 2, 3], [7]]
```

**The sort is not cosmetic — the `break` is invalid without it.** And the duplicate rule needs it too,
because it compares adjacent elements.

### Trap 6 — `i > 0` instead of `i > start`

The same trap as [day 091](../day-091-subsets/README.md), in its third outfit.

```
 combination_sum_ii([1, 1, 6], 8)
   with i > 0   ->  []                 the [1,1,6] box is lost entirely
   correct      ->  [[1, 1, 6]]
```

`i > 0` blocks the second `1` even when it is legitimately following the first *inside the same box*.
`i > start` blocks it only when it is another *first choice at the same level*.

### Trap 7 — a candidate of zero

```python
    combination_sum([0, 1], 3)
```

```
 RecursionError: maximum recursion depth exceeded
```

`build(i, remaining - 0)` calls itself with identical arguments, for ever. The measure never decreases.
LeetCode guarantees positive candidates; **saying that guarantee out loud, and saying what breaks
without it, is a strong move**, because it shows you know why the problem is well-posed.

### Trap 8 — deep recursion on a large target

```python
    combination_sum([1, 2, 5], 5000)
```

```
 RecursionError: maximum recursion depth exceeded in comparison
```

Depth is `target / min(candidates)` = 5000, and Python's limit is 1000. Unlike everything else in this
phase, **the depth here is not bounded by `n`**. If the target is large, the answer is dynamic
programming.

### Trap 9 — enumerating when they asked how many

```python
    len(combination_sum([1, 2, 5], 500))      # correct, and ~50,000 answers built
```

The count is a `O(target × n)` loop over an array. Building fifty thousand lists to call `len` on them
is the difference between one millisecond and several seconds — and at target 5000 it is the difference
between working and not.

---

## 8. In the interview

### How it gets asked

- The base: *"Find all unique combinations that sum to the target. Numbers may be reused."* LeetCode 39.
- The follow-up, always: *"Now each number may be used only once, and the input has duplicates."*
  LeetCode 40.
- The fixed-size one: *"All combinations of k numbers from 1 to 9 that add to n."* LeetCode 216.
- The plain one: *"All combinations of k elements from n."* LeetCode 77.
- The switch: *"Just tell me how many there are."* — which is not this problem at all.

### What to say out loud, in the first ninety seconds

1. **Define combination against permutation.** "Order does not matter, so `[2,3]` and `[3,2]` are the
   same answer. That means I carry a `start` index and never look backwards — one loop bound removes
   every duplicate ordering, with no set and no `used` array."
2. **Sort, and give the reason.** "I sort the candidates so that when one exceeds what remains, I know
   every later one does too and I can `break` out of the loop rather than continue."
3. **Say the reuse decision before writing the call.** "Numbers may be reused, so I recurse on `i`, not
   `i + 1`. That single character is the whole difference between this and the version where each
   element is used once."
4. **Say why it terminates.** "The remaining target strictly decreases every call because all candidates
   are positive, so the recursion has to bottom out. If zero were allowed it would loop for ever."
5. **Flag the copy.** "I append a copy when `remaining` hits zero, because the working list is mutated
   throughout."
6. **Give the honest complexity.** "Depth is target over the smallest candidate; branching is `n`. The
   loose bound is `O(n^(target/min))`, and in practice the pruning keeps it close to the size of the
   output. Extra space is the depth, which is `target / min` — and that is the one thing here not
   bounded by `n`, so a large target with a candidate of `1` would blow the stack."

### The follow-ups

**"Now each number may be used only once, and the input has duplicates."**
"Two changes and they are separate. First, recurse on `i + 1` instead of `i`, so each element is
consumed. Second, sort the input and skip a candidate that equals the previous one when `i > start` —
meaning it is another *first* choice at this level, which would start a branch identical to one I have
already walked. The important detail is that this skip is a `continue`, while the too-big check is a
`break`. Two skips, two different keywords, in the same loop. If you `break` on the duplicate you throw
away every later value as well, and on `[1,1,2,5,6,7,10]` with target 8 you get two answers instead of
four."

**"Why `i > start` and not `not used[i-1]`, which is what you used for permutations?"**
"Because they are two different tree shapes doing the same job. In the permutations tree I look at every
element at every level, so 'have I already used this one' needs a `used` array, and the duplicate rule
has to ask whether the twin is currently placed. Here the `start` index already guarantees I only move
forwards, so the only way to make the same box twice is to start two branches with equal values *at the
same level* — and `i > start` is exactly the test for that. Same idea, different bookkeeping."

**"What is the complexity?"**
"Honestly, a loose bound. The tree depth is target divided by the smallest candidate, and the branching
factor is at most `n`, so `O(n^(target/min))` is an upper bound. What actually happens is much better,
because the sorted `break` cuts off branches as soon as the running total gets close — the real cost
tracks the number of answers. Extra space is the depth, `O(target/min)`, plus the working list. I would
also flag that this is the one problem in the phase where depth is not bounded by `n`: with a candidate
of 1 and a target of 5000 you get a `RecursionError`, and at that point the right answer is dynamic
programming rather than backtracking."

**"Just tell me how many combinations there are."**
"Then I would not enumerate at all. Counting is a one-dimensional dynamic programming array: `ways[0] =
1`, then for each candidate, for each total from that candidate up to the target, add `ways[total −
candidate]`. That is `O(target × n)` — for target 500 and three candidates, fifteen hundred steps
instead of fifty thousand lists. The loop order matters: candidates on the outside counts
*combinations*; totals on the outside would count *orderings*, which is a different question."

**"What if the same combination can be reached by different paths — how do you know the output has no
duplicates?"**
"Because of the `start` index, not because of any filtering. Every box is generated in exactly one
order — non-decreasing — so there is exactly one path to it. That is the invariant worth stating: the
answer set is the set of non-decreasing sequences that hit the target. It is also why I never need to
de-duplicate the result, which matters, since `set()` on a list of lists raises `TypeError: unhashable
type: 'list'`."

**"Can you prune more aggressively?"**
"Yes, for the fixed-size ones. For choose-k I check whether the elements remaining are enough to reach
`k` and `break` if not — on choosing 18 from 20 that takes the call count from about 220,000 down to
191. For combination sum, if the candidates are sorted you can also precompute suffix sums and cut a
branch when everything left cannot reach the remaining target. Both are one line, and one line that
removes most of the tree is the best trade available."

### A model answer

Asked: *find all unique combinations that sum to the target; numbers may be reused.*

> "First the word 'combination'. Order does not matter, so `[2,3]` and `[3,2]` are the same answer and
> must appear once. That decides the structure straight away: I carry a **`start` index** and never look
> backwards. One loop bound, and every duplicate ordering disappears — I do not need a `used` array like
> permutations, and I do not need to de-duplicate at the end. The invariant is that every combination is
> generated in non-decreasing order, so there is exactly one path to each one.
>
> Then I sort the candidates, and the reason is not tidiness. Sorting means that once a candidate is
> bigger than what remains, every later candidate is too — so I can **`break`** out of the loop instead
> of continuing through the rest of it. Without the sort the `break` would be wrong and would drop valid
> answers.
>
> The recursion carries two things: `start`, and `remaining`. When `remaining` hits zero I record a
> **copy** of the working list. In the loop, for each candidate from `start` onwards: break if it is
> bigger than `remaining`, otherwise append it, recurse, and pop.
>
> The one character that matters is the argument to the recursive call. Since numbers may be reused, I
> recurse on **`i`**, not `i + 1` — 'you may pick this same value again'. If you tell me each element may
> be used once, that single character changes, and I would also add the duplicate skip: sort, and
> `continue` when this candidate equals the previous one and `i > start`. Note those are two different
> keywords in the same loop — `break` for too big, `continue` for duplicate — and swapping them is the
> classic bug.
>
> It terminates because `remaining` strictly decreases on every call: all the candidates are positive.
> That guarantee is doing real work — a zero in the candidate list would recurse with identical
> arguments for ever and end in a `RecursionError`.
>
> On cost, I will be honest that the bound is loose. Depth is target over the smallest candidate,
> branching is at most `n`, so `n^(target/min)` is an upper bound and the pruning keeps the real work
> close to the size of the output. Extra space is the depth. And I would flag one thing: unlike
> everything else in this family, the depth here is driven by the **target**, not by `n`. With a
> candidate of 1 and a target of five thousand, this recursion exceeds Python's limit — and at that
> point the question is probably 'how many', which is a `O(target × n)` dynamic programming array and
> not this at all."

---

## 9. Recall card

- **Combination = order does not matter, so carry a `start` index and never look backwards.** One loop
  bound removes every duplicate ordering — no `used` array, no de-duplication. The invariant: every
  answer is generated in **non-decreasing order**, so there is exactly one path to it.
- **Sort, then `break` when `candidates[i] > remaining`** — valid only because it is sorted, and the
  sort is therefore not cosmetic. Unsorted, the `break` drops real answers: `[7,2,6,3]` target 7 gives
  `[[7]]` instead of `[[2,2,3],[7]]`.
- **The one character: `build(i, …)` allows reuse; `build(i + 1, …)` uses each element once.** Say which
  one aloud before typing it. `i + 1` on Combination Sum I gives `[[7]]` instead of `[[2,2,3],[7]]`,
  with no error.
- **Combination Sum II has TWO skips with TWO keywords**: `break` for too big, `continue` for
  `i > start and c[i] == c[i-1]`. `break` on the duplicate loses every later value — four answers become
  two. And it is **`i > start` here**, versus **`not used[i-1]`** in the permutations tree: same job, two
  tree shapes.
- **Depth is `target / smallest candidate`, not `n`** — the only problem in the phase where the stack
  can actually overflow (`RecursionError` at target 5000 with a candidate of 1), and a **zero candidate
  never terminates** because the measure stops decreasing. **"How many" is never backtracking**: it is
  `ways[t] += ways[t-c]`, O(target × n) — 1,500 steps instead of 50,000 lists.
