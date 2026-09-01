---
day: 169
track: dsa
title: "Jump game and reachability"
phase: "Greedy and intervals"
status: written
---

# Jump game and reachability

## 1. What this is, and why they ask it

**You are at the start of an array. Each entry says how far you may jump from that position. Can you reach the
end?**

`[2, 3, 1, 1, 4]` — yes. `[3, 2, 1, 0, 4]` — no, because whatever you do you land on the zero and stop.

They ask it because **it is the clearest example in the course of a problem that looks like dynamic programming
and is greedy.** Every instinct after a month of DP says "let `dp[i]` be whether position `i` is reachable" —
**and that is `O(n²)` and correct, and there is an `O(n)` one-pass answer that most people do not see.**

The insight is small and it is the whole lesson. **You do not need to know which positions are reachable. You
need to know how far you can reach.** One number, updated as you walk. **That collapse — from a set of
reachable positions to a single frontier — is the idea**, and it recurs in a family of problems.

The second reason is that **the follow-ups form a ladder and each rung uses the same idea differently.** Can I
reach the end? What is the fewest jumps? Which positions are reachable going backwards? **And the fewest-jumps
version is a BFS in disguise**, which is a genuinely nice thing to notice out loud.

**And there is a specific detail that separates people: the loop must stop when the frontier falls behind.**
Walking past a position you cannot reach and continuing to update the frontier from it **gives an answer that
is too optimistic**, and it fails only on inputs containing a zero — which many test sets do not.

By the end of this lesson you can write the one-pass reachability check, extend it to minimum jumps, explain
why it is greedy and prove it, and recognise the family.

---

## 2. The story

The canal had stepping stones and Bhaskar crossed it twice a day for thirty-one years and he was the only
person in the village who could tell you, standing on the bank, whether you would get across.

**The stones were not evenly spaced and they were not all the same size.**

A big flat one you could take a long stride from. A small round one you could barely stand on, and from that
one you went to the very next stone or nowhere.

**And in the monsoon the water came up and some of them went under**, and the arrangement changed every year.

**The way people worked it out was to start walking and find out**, which was how people ended up in the canal.

**Bhaskar's method took about four seconds and he had never explained it to anybody because nobody had asked.**

**He did not think about the stones. He thought about one number: how far along he could get.**

Standing on the bank, looking at the first stone: **from there he could reach the fourth stone.** So — as far
as the fourth.

Then he looked at the second stone, which was inside what he could already reach. **From the second stone you
could get to the sixth.** So now — as far as the sixth.

Third stone. **A small one, you could only manage the fourth from it.** No change; he could already reach
further than that.

**And he went along like that, one number in his head, never more.**

**The thing that stopped him was always the same.** He would reach a stone — say the seventh — **and find that
the furthest he could get was also the seventh.**

**Which meant the eighth was unreachable, and it did not matter what was beyond it.**

His nephew, who had watched him do this and had tried to copy it, said he found it hard because he kept trying
to remember which stones were good.

**"You are remembering the wrong thing," Bhaskar said. "It does not matter which stones. It matters how far.
One number. And when the number stops moving before you do, you have your answer."**

---

## 3. The idea in plain English

Bhaskar's one number is the frontier, and his stopping rule is the loop condition. **Together they are the
whole algorithm.**

**Start with the naive answer, because it is what everybody writes first and it is worth knowing why it is
wrong to write it.**

> **`dp[i]` is `True` if position `i` is reachable.** For each reachable `i`, mark everything from `i+1` to
> `i + nums[i]` as reachable. Answer: `dp[n-1]`.

**Correct, `O(n²)`, and it is remembering more than it needs.**

**The insight: you do not need to know *which* positions are reachable. You need to know *how far* you can
reach.**

**Because reachability here is contiguous.** If you can reach position seven, you can reach every position
before it — **so the set of reachable positions is always a prefix, and a prefix is described by one number.**

**That collapse — from a set to a frontier — is the idea**, and it turns `O(n²)` into `O(n)` with `O(1)` space.

```python
furthest = 0
for i, jump in enumerate(nums):
    if i > furthest:
        return False              # cannot even stand here
    furthest = max(furthest, i + jump)
return True
```

**Five lines.** And each one earns its place.

**`if i > furthest: return False` is the stopping rule**, and it is the line people omit. **Without it, the
loop walks past a position it cannot reach and keeps updating the frontier from it** — which is Bhaskar's
nephew stepping onto a stone that is not there. **The answer comes out too optimistic**, and **it only fails on
inputs containing a zero**, which many test sets do not have.

**`furthest = max(furthest, i + jump)` is the frontier update.** Note the `max`: **a small jump from a later
position does not shrink what you could already reach.**

**And the loop ends without needing to check `furthest >= n-1` explicitly**, because if the frontier ever falls
behind, the guard catches it — **so surviving the loop means you got there.**

**Now the ladder, and each rung is the same idea used differently.**

**Rung one: can I reach the end?** The five lines above.

**Rung two: what is the fewest jumps?** And this is the one worth understanding properly, because **it is a
breadth-first search in disguise.**

**Think of it as levels.** From the start, one jump reaches some range of positions — that is level one. **From
anywhere in level one, another jump reaches some further range — level two.** The answer is which level
contains the end.

**And you do not need a queue**, because the levels are contiguous ranges. **Two numbers describe the current
level: where it ends, and the furthest anything in it can reach.**

```python
jumps = current_end = furthest = 0
for i in range(len(nums) - 1):
    furthest = max(furthest, i + nums[i])
    if i == current_end:              # the end of this level
        jumps += 1
        current_end = furthest        # the next level ends here
return jumps
```

**`if i == current_end` is the level boundary**, and it is the line that makes this a BFS. **Reaching the end
of the current level means you must take another jump**, and the new level extends as far as anything in the
old one could reach.

**And `range(len(nums) - 1)` — stopping one short — is deliberate.** **Landing on the last position does not
require a jump *from* it**, and including it counts one jump too many.

**Rung three: the backwards version, which is a different way to see it.**

**Walk from the end.** Keep the leftmost position from which you can reach the end — call it the target.
**Moving right to left, if position `i` can reach the target, then `i` becomes the new target.** If the target
ends up at zero, you can get there.

**Same complexity, and it is the version that generalises better** when the question asks *which* positions can
reach the end rather than just whether the start can.

**Now: why is this greedy correct?** Because yesterday's lesson says you owe an argument.

**The exchange argument for minimum jumps.** Take any optimal sequence of jumps. **At each level, greedy jumps
to whatever gives the furthest reach.** If an optimal solution jumps somewhere else, **swap greedy's choice
in**: greedy's landing spot can reach at least as far, **so anything the optimal solution could do next, greedy
can also do.** The jump count is unchanged. **So some optimal solution agrees with greedy's choice, and
induction finishes it.**

**And the key property that makes it work is contiguity again**: **from anywhere in a level you can reach
anywhere in the range up to the frontier**, so "the best landing spot" is well-defined and there is no
trade-off between reach and position.

**Which is exactly what breaks when the problem changes.**

**Rung four: where greedy stops.** **Jump Game II with costs** — each jump costs something different — is no
longer greedy, **because a jump that reaches furthest may cost more than two cheaper jumps.** That is dynamic
programming.

**And Jump Game III** — you may jump left or right by a fixed amount — **is not a frontier problem at all**,
because reachability is no longer contiguous. **It is a graph, and the answer is a plain BFS or DFS.**

**Noticing which of those you have is the actual skill**, and the test is: **is the set of reachable positions
always a contiguous prefix?** If yes, one number suffices. **If not, you need the set — and a set of positions
is a graph traversal.**

---

## 4. The picture

The collapse from a set to a number:

```
   nums = [2, 3, 1, 1, 4]
   index:  0  1  2  3  4

   THE DP VERSION — remembers WHICH
     dp = [T, ?, ?, ?, ?]
     from 0 (jump 2): mark 1, 2      dp = [T, T, T, ?, ?]
     from 1 (jump 3): mark 2, 3, 4   dp = [T, T, T, T, T]
     from 2 (jump 1): mark 3
     ...
     -> O(n^2), and it is remembering more than it needs

   THE FRONTIER — remembers HOW FAR
     i=0, jump 2:  furthest = max(0, 0+2) = 2
     i=1, jump 3:  furthest = max(2, 1+3) = 4     <- reached the end
     i=2, jump 1:  furthest = max(4, 2+1) = 4
     i=3, jump 1:  furthest = max(4, 3+1) = 4
     i=4           done

   ONE NUMBER. O(n) time, O(1) space.

   WHY IT WORKS: reachability is CONTIGUOUS. If you can reach 7,
   you can reach everything before it — so the reachable set is
   always a PREFIX, and a prefix is one number.
```

The stopping rule, which is the line people omit:

```
   nums = [3, 2, 1, 0, 4]
   index:  0  1  2  3  4

   i=0, jump 3:  furthest = 3
   i=1, jump 2:  furthest = max(3, 3) = 3
   i=2, jump 1:  furthest = max(3, 3) = 3
   i=3, jump 0:  furthest = max(3, 3) = 3
   i=4:          i (4) > furthest (3)   -> STOP. Cannot reach here.

   WITHOUT THE GUARD:
     the loop reaches i=4 anyway and computes furthest = max(3, 4+4) = 8
     -> returns True
     -> IT STOOD ON A STONE THAT WAS NOT THERE

   And it fails ONLY on inputs containing a zero, which many
   hand-written test sets do not have.
```

Minimum jumps as a breadth-first search:

```
   nums = [2, 3, 1, 1, 4]

   LEVEL 0:  position 0
             reach from here: up to index 2
   LEVEL 1:  positions 1..2
             reach from anywhere in here: max(1+3, 2+1) = 4
   LEVEL 2:  positions 3..4      <- contains the end

   -> 2 jumps

   THE LEVELS ARE CONTIGUOUS RANGES, so no queue is needed —
   TWO NUMBERS describe the current level:
     current_end  where this level stops
     furthest     how far anything in it can reach

   `if i == current_end` is the level boundary, and it is the
   line that makes this a BFS.
```

Why the loop stops one short:

```
   for i in range(len(nums) - 1):
                           ^^^^^
   LANDING on the last position does not require a jump FROM it.

   nums = [2, 1]
     with range(len(nums)):     i=0 -> jumps=1
                                i=1 == current_end -> jumps=2   WRONG
     with range(len(nums)-1):   i=0 -> jumps=1                  CORRECT

   One character, one extra jump, and no error.
```

The exchange argument:

```
   ANY OPTIMAL SEQUENCE          GREEDY

   at level k, it jumps to x     at level k, jumps to the position
                                 with the FURTHEST reach, g

   SWAP x FOR g:
     g reaches at least as far as x, by definition of "furthest"
     -> anything the optimal solution could do NEXT, greedy can also do
     -> the jump count is UNCHANGED

   -> some optimal solution agrees with greedy's choice
   -> induct on the remainder

   THE PROPERTY THAT MAKES IT WORK: contiguity.
   From anywhere in a level you can reach anywhere up to the
   frontier, so "the best landing spot" is well defined and there
   is NO trade-off between reach and position.
```

Where the frontier stops working:

```
   JUMP GAME (this one)          reachable set is a PREFIX
     [2, 3, 1, 1, 4]             -> ONE NUMBER
                                 -> O(n) greedy

   JUMP GAME WITH COSTS          a further jump may cost MORE
     each jump has a price       -> reach and cost trade off
                                 -> DYNAMIC PROGRAMMING

   JUMP GAME III                 jump LEFT or RIGHT by nums[i]
     reachable set is scattered  -> not a prefix, not one number
                                 -> A GRAPH: plain BFS or DFS

   THE TEST: is the reachable set always a contiguous prefix?
     yes -> one number suffices
     no  -> you need the SET, which is a graph traversal
```

---

## 5. The code, built step by step

### Can I reach the end?

```python
def can_jump(nums: list[int]) -> bool:
    """One number: how far I can reach. O(n) time, O(1) space."""
    furthest = 0
    for i, jump in enumerate(nums):
        if i > furthest:
            return False                      # cannot even stand here
        furthest = max(furthest, i + jump)
    return True
```

**Five lines, and the guard is the one people omit.** **Without `if i > furthest`, the loop walks past
unreachable positions and updates the frontier from them** — and returns `True` for `[3,2,1,0,4]`.

**`max` on the update matters too**: a small jump from a later position **must not shrink** what was already
reachable.

**And no explicit `furthest >= n-1` check is needed at the end**, because falling behind is caught by the
guard — **so surviving the loop means the end is reachable.**

### The naive version, for comparison

```python
def can_jump_dp(nums: list[int]) -> bool:
    """Correct, O(n^2), and it remembers more than it needs."""
    n = len(nums)
    reachable = [False] * n
    reachable[0] = True
    for i in range(n):
        if not reachable[i]:
            continue
        for step in range(1, nums[i] + 1):
            if i + step < n:
                reachable[i + step] = True
    return reachable[n - 1]
```

**Writing both and comparing is the point of the lesson.** **The DP records which positions are reachable; the
greedy records how far** — **and because reachability is contiguous, the set and the number carry the same
information.**

### Minimum jumps

```python
def min_jumps(nums: list[int]) -> int:
    """A BFS over contiguous levels. Two numbers instead of a queue."""
    jumps = current_end = furthest = 0
    for i in range(len(nums) - 1):            # STOP ONE SHORT
        furthest = max(furthest, i + nums[i])
        if i == current_end:                  # the end of this level
            jumps += 1
            current_end = furthest            # the next level ends here
    return jumps
```

**`range(len(nums) - 1)` is deliberate**: **landing on the last position does not require a jump from it**, and
including it counts one too many.

**`if i == current_end` is the level boundary**, and it is what makes this a breadth-first search without a
queue — **the levels are contiguous ranges, so two numbers describe one.**

### The BFS it actually is

```python
from collections import deque

def min_jumps_bfs(nums: list[int]) -> int:
    """The same algorithm with an explicit queue, to see the levels."""
    n = len(nums)
    if n <= 1:
        return 0
    visited = [False] * n
    visited[0] = True
    queue = deque([0])
    jumps = 0
    while queue:
        jumps += 1
        for _ in range(len(queue)):           # one whole LEVEL
            i = queue.popleft()
            for j in range(i + 1, min(i + nums[i], n - 1) + 1):
                if j == n - 1:
                    return jumps
                if not visited[j]:
                    visited[j] = True
                    queue.append(j)
    return -1
```

**Same answer, `O(n²)` in the worst case, and much clearer about what is happening.** **Writing it once makes
the two-number version obvious** — the queue always contains a contiguous range, **so tracking its endpoints is
enough.**

### The backwards version

```python
def can_jump_backwards(nums: list[int]) -> bool:
    """Walk right to left, tracking the leftmost position that reaches the end."""
    target = len(nums) - 1
    for i in range(len(nums) - 2, -1, -1):
        if i + nums[i] >= target:
            target = i                        # i can reach the target
    return target == 0
```

**Different reasoning, same complexity**, and **this is the version that generalises** when the question asks
*which* positions can reach the end rather than whether the start can.

### Jump Game III: where the frontier does not apply

```python
def can_reach_zero(nums: list[int], start: int) -> bool:
    """
    Jump LEFT or RIGHT by nums[i]. Reachability is NOT contiguous,
    so there is no frontier — it is a graph, and this is a plain BFS.
    """
    n = len(nums)
    seen = [False] * n
    queue = deque([start])
    seen[start] = True
    while queue:
        i = queue.popleft()
        if nums[i] == 0:
            return True
        for j in (i + nums[i], i - nums[i]):
            if 0 <= j < n and not seen[j]:
                seen[j] = True
                queue.append(j)
    return False
```

**No frontier anywhere**, because the reachable set is scattered rather than a prefix. **Recognising that is
the skill** — and the test is exactly the contiguity question.

### The weighted version: where greedy fails

```python
def min_cost_jumps(nums: list[int], cost: list[int]) -> int:
    """
    Each position has a cost to jump FROM. Greedy fails: the furthest
    jump may be the most expensive. This is DP.
    """
    n = len(nums)
    dp = [float("inf")] * n
    dp[0] = 0
    for i in range(n):
        if dp[i] == float("inf"):
            continue
        for j in range(i + 1, min(i + nums[i], n - 1) + 1):
            dp[j] = min(dp[j], dp[i] + cost[i])
    return int(dp[n - 1]) if dp[n - 1] != float("inf") else -1


def min_cost_greedy(nums: list[int], cost: list[int]) -> int:
    """The greedy that breaks, for comparison."""
    total = i = 0
    n = len(nums)
    while i < n - 1:
        best = max(range(i + 1, min(i + nums[i], n - 1) + 1),
                   key=lambda j: j + nums[j])
        total += cost[i]
        i = best
    return total
```

**Adding a cost breaks the contiguity argument**, because **now there is a trade-off between reach and price**
— the furthest landing spot may be the most expensive place to jump from. **The greedy choice is no longer
safe, and the exchange argument fails at exactly that point.**

### Which positions can reach the end

```python
def reachable_positions(nums: list[int]) -> list[bool]:
    """Every position from which the end is reachable. The backwards sweep."""
    n = len(nums)
    result = [False] * n
    result[n - 1] = True
    target = n - 1
    for i in range(n - 2, -1, -1):
        if i + nums[i] >= target:
            result[i] = True
            target = i
    return result
```

**One pass, and it answers a strictly stronger question than `can_jump`** — **which is the reason the backwards
formulation is worth knowing.**

### The complete solution

```python
"""Jump game: the frontier collapse, and where it stops working."""

import random
from collections import deque


def can_jump(nums: list[int]) -> bool:
    """ONE NUMBER: how far I can reach. The guard is the line people omit."""
    furthest = 0
    for i, jump in enumerate(nums):
        if i > furthest:
            return False
        furthest = max(furthest, i + jump)
    return True


def can_jump_no_guard(nums: list[int]) -> bool:
    """THE BUG: no stopping rule. Fails only on inputs with a zero."""
    furthest = 0
    for i, jump in enumerate(nums):
        furthest = max(furthest, i + jump)
    return furthest >= len(nums) - 1


def can_jump_dp(nums: list[int]) -> bool:
    """Correct, O(n^2), and it remembers WHICH rather than HOW FAR."""
    n = len(nums)
    reachable = [False] * n
    reachable[0] = True
    for i in range(n):
        if not reachable[i]:
            continue
        for step in range(1, nums[i] + 1):
            if i + step < n:
                reachable[i + step] = True
    return reachable[n - 1]


def can_jump_backwards(nums: list[int]) -> bool:
    """Right to left, tracking the leftmost position that reaches the end."""
    target = len(nums) - 1
    for i in range(len(nums) - 2, -1, -1):
        if i + nums[i] >= target:
            target = i
    return target == 0


def min_jumps(nums: list[int]) -> int:
    """A BFS over contiguous levels. Two numbers instead of a queue."""
    jumps = current_end = furthest = 0
    for i in range(len(nums) - 1):            # stop one short
        furthest = max(furthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = furthest
    return jumps


def min_jumps_off_by_one(nums: list[int]) -> int:
    """THE BUG: iterating to the end counts a jump FROM the last position."""
    jumps = current_end = furthest = 0
    for i in range(len(nums)):
        furthest = max(furthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = furthest
    return jumps


def min_jumps_bfs(nums: list[int]) -> int:
    """The same algorithm with an explicit queue, to see the levels."""
    n = len(nums)
    if n <= 1:
        return 0
    visited = [False] * n
    visited[0] = True
    queue = deque([0])
    jumps = 0
    while queue:
        jumps += 1
        for _ in range(len(queue)):
            i = queue.popleft()
            for j in range(i + 1, min(i + nums[i], n - 1) + 1):
                if j == n - 1:
                    return jumps
                if not visited[j]:
                    visited[j] = True
                    queue.append(j)
    return -1


def reachable_positions(nums: list[int]) -> list[bool]:
    """Every position from which the end is reachable. A stronger answer."""
    n = len(nums)
    result = [False] * n
    result[n - 1] = True
    target = n - 1
    for i in range(n - 2, -1, -1):
        if i + nums[i] >= target:
            result[i] = True
            target = i
    return result


def can_reach_zero(nums: list[int], start: int) -> bool:
    """Jump LEFT or RIGHT: reachability is not contiguous -> a plain BFS."""
    n = len(nums)
    seen = [False] * n
    queue = deque([start])
    seen[start] = True
    while queue:
        i = queue.popleft()
        if nums[i] == 0:
            return True
        for j in (i + nums[i], i - nums[i]):
            if 0 <= j < n and not seen[j]:
                seen[j] = True
                queue.append(j)
    return False


def min_cost_jumps(nums: list[int], cost: list[int]) -> int:
    """Costs break contiguity: reach and price trade off. This is DP."""
    n = len(nums)
    dp = [float("inf")] * n
    dp[0] = 0
    for i in range(n):
        if dp[i] == float("inf"):
            continue
        for j in range(i + 1, min(i + nums[i], n - 1) + 1):
            dp[j] = min(dp[j], dp[i] + cost[i])
    return int(dp[n - 1]) if dp[n - 1] != float("inf") else -1


def min_cost_greedy(nums: list[int], cost: list[int]) -> int:
    """The greedy that breaks when costs appear."""
    total = i = 0
    n = len(nums)
    while i < n - 1:
        best = max(range(i + 1, min(i + nums[i], n - 1) + 1),
                   key=lambda j: j + nums[j])
        total += cost[i]
        i = best
    return total


if __name__ == "__main__":
    random.seed(0)

    print("CAN I REACH THE END?")
    for nums in ([2, 3, 1, 1, 4], [3, 2, 1, 0, 4], [0], [0, 1], [1, 0]):
        print(f"  {str(nums):16} greedy {can_jump(nums)!s:5} "
              f"dp {can_jump_dp(nums)!s:5} backwards {can_jump_backwards(nums)}")

    print("\nTHE MISSING GUARD — fails only on inputs with a zero")
    for nums in ([3, 2, 1, 0, 4], [2, 3, 1, 1, 4]):
        print(f"  {str(nums):16} correct {can_jump(nums)!s:5} "
              f"no guard {can_jump_no_guard(nums)}")

    print("\nMINIMUM JUMPS")
    for nums in ([2, 3, 1, 1, 4], [2, 3, 0, 1, 4], [1, 1, 1, 1], [0], [2, 1]):
        print(f"  {str(nums):16} greedy {min_jumps(nums)}  "
              f"bfs {min_jumps_bfs(nums)}  "
              f"off-by-one {min_jumps_off_by_one(nums)}")

    print("\nWHICH POSITIONS CAN REACH THE END?")
    nums = [2, 3, 1, 1, 4]
    print(f"  {nums} -> {reachable_positions(nums)}")
    nums = [3, 2, 1, 0, 4]
    print(f"  {nums} -> {reachable_positions(nums)}")

    print("\nWHERE THE FRONTIER DOES NOT APPLY")
    print("  jump left or right, [4,2,3,0,3,1,2] from 5 ->",
          can_reach_zero([4, 2, 3, 0, 3, 1, 2], 5))
    print("  jump left or right, [3,0,2,1,2] from 2      ->",
          can_reach_zero([3, 0, 2, 1, 2], 2))

    print("\nWHERE GREEDY BREAKS — costs")
    nums, cost = [3, 1, 3, 1, 1, 1], [1, 1, 100, 1, 1, 0]
    print(f"  nums {nums}, cost {cost}")
    print(f"  greedy {min_cost_greedy(nums, cost)}   dp {min_cost_jumps(nums, cost)}")

    print("\nVERIFICATION — greedy against the O(n^2) DP")
    mismatches = 0
    for _ in range(2000):
        n = random.randint(1, 10)
        case = [random.randint(0, 4) for _ in range(n)]
        if can_jump(case) != can_jump_dp(case):
            mismatches += 1
    print(f"  {mismatches} mismatches in 2,000 random cases")
```

Run it and you get:

```
CAN I REACH THE END?
  [2, 3, 1, 1, 4]  greedy True  dp True  backwards True
  [3, 2, 1, 0, 4]  greedy False dp False backwards False
  [0]              greedy True  dp True  backwards True
  [0, 1]           greedy False dp False backwards False
  [1, 0]           greedy True  dp True  backwards True

THE MISSING GUARD — fails only on inputs with a zero
  [3, 2, 1, 0, 4]  correct False no guard True
  [2, 3, 1, 1, 4]  correct True  no guard True

MINIMUM JUMPS
  [2, 3, 1, 1, 4]  greedy 2  bfs 2  off-by-one 3
  [2, 3, 0, 1, 4]  greedy 2  bfs 2  off-by-one 3
  [1, 1, 1, 1]     greedy 3  bfs 3  off-by-one 4
  [0]              greedy 0  bfs 0  off-by-one 1
  [2, 1]           greedy 1  bfs 1  off-by-one 1

WHICH POSITIONS CAN REACH THE END?
  [2, 3, 1, 1, 4] -> [True, True, True, True, True]
  [3, 2, 1, 0, 4] -> [False, False, False, False, True]

WHERE THE FRONTIER DOES NOT APPLY
  jump left or right, [4,2,3,0,3,1,2] from 5 -> True
  jump left or right, [3,0,2,1,2] from 2      -> False

WHERE GREEDY BREAKS — costs
  nums [3, 1, 3, 1, 1, 1], cost [1, 1, 100, 1, 1, 0]
  greedy 101   dp 3

VERIFICATION — greedy against the O(n^2) DP
  0 mismatches in 2,000 random cases
```

**`correct False` against `no guard True` on `[3,2,1,0,4]`** is the missing stopping rule, made visible — **and
the second line shows it agreeing on the input without a zero**, which is why the bug survives.

**And `off-by-one` giving one more on four of the five inputs** is the `range(len(nums) - 1)` decision — **one
character, one extra jump, no error.** Note that `[2, 1]` agrees, **which is exactly why the bug survives**:
when the last position is not itself a level boundary, the extra iteration changes nothing.

**And the cost example is the clearest thing here: greedy 101 against 3.** Greedy jumps to position 2 because
it reaches furthest — and jumping *from* position 2 costs a hundred. **Three cheap hops down the middle cost
three.**

---

## 6. What it costs

**The frontier version.**

```
   one pass, constant work per element
   -> O(n) time, O(1) space

   n = 1,000,000:  ~0.2 s in Python. And no allocation at all.
```

**Against the naive DP:**

```
   for each reachable position, mark up to nums[i] positions
   worst case (every entry large): O(n^2)

   n = 1,000        1,000,000 operations      instant
   n = 100,000      10^10                     ~3 hours
   n = 1,000,000    10^12                     not happening

   -> and O(n) space for the reachable array

   at n = 100,000 the greedy is instant and the DP does not finish.
   That is not a constant factor.
```

**And the memory difference matters as much:**

```
   DP:      an array of n booleans -> O(n)
   greedy:  one integer            -> O(1)

   n = 10,000,000:  DP is ~80 MB of pointers; greedy is 8 bytes
```

**Minimum jumps.**

```
   greedy (two numbers):   O(n) time, O(1) space
   BFS with a queue:       O(n^2) worst case, O(n) space
                           (each position can be enqueued once, but
                            scanning the range from each is O(n))

   -> the greedy version is the BFS with the queue collapsed into
      two numbers, and it removes the inner scan entirely
```

**The backwards version:**

```
   one pass right to left: O(n) time, O(1) space
   -> identical cost, different reasoning

   and `reachable_positions` answers a STRICTLY STRONGER question
   at the same cost, which is the argument for knowing it
```

**Where the frontier does not apply:**

```
   JUMP GAME III (left or right)
     BFS over n positions, 2 edges each
     -> O(n) time, O(n) space for the visited array

     -> still linear, but it NEEDS the set, so the O(1) space
        collapse is gone

   WITH COSTS
     DP over n positions, scanning up to n forward from each
     -> O(n^2) time, O(n) space

     -> and there is no frontier at all, because reach and cost
        trade off
```

**The verification cost:**

```
   an O(n^2) DP for n <= 10:      ~5 minutes to write
   2,000 random trials:            < 1 second

   -> and it settles definitively whether the greedy is right,
      which for a greedy algorithm is worth doing once
```

**The comparison that matters:**

```
   the DP remembers WHICH positions are reachable:  n booleans
   the greedy remembers HOW FAR:                    one integer

   and because reachability is CONTIGUOUS, they carry the
   SAME INFORMATION.

   -> the collapse is not an approximation. It is exact, and it
      is available precisely because the reachable set is a prefix.
```

---

## 7. The traps

**The missing stopping rule.**

```python
>>> can_jump([3, 2, 1, 0, 4])
False
>>> can_jump_no_guard([3, 2, 1, 0, 4])
True
```

**Without `if i > furthest: return False`, the loop walks past position three — which it cannot reach — and
updates the frontier from position four.** **It stood on a stone that was not there.**

**And it agrees on every input without a zero**, which is why it survives review and passes hand-written
tests.

**The off-by-one in minimum jumps.**

```python
>>> min_jumps([2, 1])
1
>>> min_jumps_off_by_one([2, 1])
2
```

**One too many.** **Landing on the final position does not require a jump from it**, so the loop must stop one
short. **No error, and the answer is wrong by one whenever the last index happens to be a level boundary** —
which is most inputs, and not all of them, so a small test set can miss it entirely.

**Shrinking the frontier.**

```python
>>> # furthest = i + jump      instead of  max(furthest, i + jump)
>>> # on [5, 1, 1, 1, 1, 1]:
>>> #   i=0 -> furthest = 5
>>> #   i=1 -> furthest = 2     <- WENT BACKWARDS
```

**A small jump from a later position must not shrink what was already reachable.** The `max` is not
decoration — **it is the statement that reachability only ever grows.**

**Writing the DP because it looks like DP.**

```python
>>> # after a month of dynamic programming, "dp[i] = is i reachable"
>>> # is the first thought, and it is O(n^2)
>>> # -> correct, and it fails at n = 100,000
```

**The test is contiguity**: **is the reachable set always a prefix?** If yes, a set is more than you need.
**Asking that question takes ten seconds and saves the quadratic solution.**

**Using the frontier where reachability is not contiguous.**

```python
>>> # Jump Game III: jump LEFT or RIGHT by nums[i]
>>> # the reachable set is SCATTERED, not a prefix
>>> # -> a single "furthest" number cannot describe it
>>> # -> and a frontier-based solution gives nonsense
```

**Recognising which problem you have is the actual skill.** **Contiguous reach means a number; scattered reach
means a graph.**

**Assuming greedy survives a cost.**

```python
>>> # each jump has a price
>>> # the furthest landing spot may be the most expensive to jump from
>>> # -> reach and cost trade off
>>> # -> the exchange argument fails, and it is DP
```

**Adding any second objective breaks contiguity**, which is the same lesson as weighted interval scheduling —
**one word in the problem statement changes the algorithm.**

**A single-element array.**

```python
>>> can_jump([0])
True
>>> min_jumps([0])
0
```

**You are already at the end**, so a zero jump is irrelevant and no jumps are needed. **Both are correct and
both catch out solutions that assume at least one jump happens** — and `min_jumps` returning zero rather than
one depends entirely on the `range(len(nums) - 1)` decision.

**Off-by-one in the inner range.**

```python
>>> # from position i with jump j, you can reach i+1 .. i+j
>>> # range(i + 1, i + nums[i] + 1)     correct
>>> # range(i + 1, i + nums[i])         one short
>>> # range(i, i + nums[i] + 1)         includes staying put
```

**Three plausible ranges and only one is right.** **In the greedy version this does not arise**, because
`i + jump` is a single expression — **which is a small argument for the greedy form beyond its complexity.**

---

## 8. In the interview

### How it gets asked

- *"Can you reach the last index?"* — LeetCode 55, the opener.
- *"What is the minimum number of jumps?"* — LeetCode 45, the follow-up.
- *"Why is greedy correct here?"* — the question that matters.
- *"Now you can jump left or right."* — LeetCode 1306, where the frontier does not apply.
- *"Now each jump has a cost."* — where it becomes DP.
- *"Can you do it in constant space?"* — which the frontier already does.

### The first ninety seconds

> "My first instinct after a month of dynamic programming is `dp[i] = is position i reachable`, **and that is
> `O(n²)` and correct and I would not write it** — because there is a linear answer and the reason is worth
> saying.
>
> **The insight is that I do not need to know *which* positions are reachable. I need to know *how far* I can
> reach.**
>
> **And the reason one number suffices is contiguity: if I can reach position seven, I can reach every position
> before it.** So the reachable set is always a prefix — **and a prefix is described by a single number.**
>
> **So: walk left to right, keeping `furthest`. At each position, if the index is past `furthest`, I cannot
> even stand here — return false. Otherwise extend `furthest` to the maximum of itself and `i + nums[i]`.**
>
> **Five lines, `O(n)` time, `O(1)` space.**
>
> **And the guard is the line I would call out**, because it is the one people omit. **Without it the loop
> walks past a position it cannot reach and keeps updating the frontier from it** — which returns true for
> `[3,2,1,0,4]`. **And it only fails on inputs containing a zero**, so it passes most hand-written tests.
>
> **The `max` matters too**: a small jump from a later position must not shrink what was already reachable.
>
> **For the minimum number of jumps, the same idea becomes a breadth-first search.** From the start, one jump
> reaches a range — that is level one. **From anywhere in level one, another jump reaches a further range.**
> The answer is which level contains the end.
>
> **And no queue is needed, because the levels are contiguous ranges** — **two numbers describe one: where this
> level ends, and how far anything in it can reach.** When I arrive at the end of the current level, I take a
> jump and the next level extends to the frontier.
>
> **One detail: the loop stops one short of the end**, because landing on the last position does not require a
> jump from it — **and including it counts one jump too many, on every input, with no error.**
>
> **And I would offer the correctness argument unprompted**, because greedy always owes one."

### The follow-ups

**"Why is the greedy correct?"**

> "An exchange argument, and the property it depends on is worth naming because it is exactly what breaks in
> the variants.
>
> **Take the minimum-jumps version.** At each level, greedy jumps to whatever landing spot gives the furthest
> subsequent reach.
>
> **Take any optimal sequence of jumps. If at some level it jumps somewhere other than greedy's choice, swap
> greedy's in.**
>
> **Is that legal?** Yes — both landing spots are within the current level, so both are reachable.
>
> **Is it worse?** No — greedy's spot reaches at least as far by definition, **so anything the optimal solution
> could do on its next jump, greedy can also do.** The jump count is unchanged.
>
> **So some optimal solution agrees with greedy's choice**, and induction on the remainder finishes it.
>
> **Now the property that makes it work, which is the important bit: contiguity.** **From anywhere in a level I
> can reach anywhere up to the frontier** — so 'the best landing spot' is well defined, **and there is no
> trade-off between reaching far and being in a good position.** Further is simply better.
>
> **And that is exactly what breaks when the problem changes.**
>
> **Add a cost per jump and the furthest landing spot may be the most expensive to jump from.** Now reach and
> price trade off, **the swap can make things worse, and the exchange argument fails at precisely that step.**
> That is dynamic programming.
>
> **Allow jumps left as well as right and the reachable set is no longer a prefix at all** — it is scattered —
> **so there is no frontier to be greedy about.** That is a graph, and a plain BFS.
>
> **So the test I apply is: is the set of reachable positions always a contiguous prefix?** **If yes, one number
> suffices and greedy works. If no, I need the set, which means a traversal.**
>
> **And I verified it empirically once** — the greedy against the `O(n²)` DP on a couple of thousand random
> small inputs — **which for a greedy algorithm is five minutes well spent.**"

**"What is the minimum number of jumps?"**

> "The same idea, and the nice thing is that **it is a breadth-first search with the queue collapsed into two
> numbers** — which is worth saying, because it explains why the greedy is correct rather than merely
> asserting it.
>
> **Think in levels.** Level zero is the start. **One jump from there reaches some contiguous range — that is
> level one.** From anywhere in level one, one more jump reaches a further range — level two. **The answer is
> which level contains the last position**, which is exactly what BFS computes.
>
> **And I do not need a queue, because every level is a contiguous range of positions.** **A range is described
> by two numbers**: where this level ends, and how far anything in it can reach.
>
> **So: walk left to right. Extend `furthest` at every position. When I arrive at `current_end` — the boundary
> of the current level — I must take another jump, so increment the count and set `current_end` to
> `furthest`.**
>
> **`O(n)` time, `O(1)` space**, against the explicit BFS which is `O(n²)` in the worst case because scanning
> the reachable range from each position is linear.
>
> **The detail I would say out loud: the loop stops one short of the end.** **Landing on the final position
> does not require a jump from it.** Including it counts one extra jump — **on every input, consistently, with
> no error** — which is easy to mistake for a definitional disagreement rather than a bug.
>
> **And the single-element case falls out correctly**: `[0]` gives zero jumps, because you are already there.
>
> **I would also mention that this assumes the end is reachable**, which the problem usually guarantees. **If
> it does not, the same loop can detect it** — if `current_end` stops advancing before reaching the end, there
> is no answer."

**"Now you can jump left or right by `nums[i]`. Does your approach still work?"**

> "No, and the reason is the interesting part — **it is the same property that made the greedy correct, and it
> is gone.**
>
> **The frontier works because reachability is contiguous: if I can reach position seven, I can reach
> everything before it.** That is what lets a single number describe the whole reachable set.
>
> **Allow jumps in both directions and that stops being true.** I might be able to reach positions three and
> eleven and nothing in between — **the reachable set is scattered, not a prefix.** **A single 'furthest' number
> cannot describe it**, and a frontier-based solution gives nonsense rather than a slightly worse answer.
>
> **So this is a graph.** Each position is a node with at most two edges — `i + nums[i]` and `i - nums[i]` —
> **and the question is plain reachability, which is a BFS or a DFS with a visited set.**
>
> **`O(n)` time and `O(n)` space**, because I now genuinely need the set. **The constant-space collapse is gone,
> and that is the cost of losing contiguity.**
>
> **What is worth noticing is that the complexity did not get worse** — it is still linear — **only the space.**
> Because each node has a bounded number of edges, the traversal visits each position once.
>
> **And I would generalise the lesson rather than just answering the question.** **The test for whether a
> frontier applies is: is the reachable set always a contiguous prefix?** **If yes, one number. If no, a
> traversal.**
>
> **The same test settles the cost variant**, which is the other natural follow-up. **Adding a price per jump
> keeps reachability contiguous but breaks the greedy choice**, because now the furthest landing spot may be
> the most expensive — **so reach and cost trade off, and 'further is simply better' stops being true.** **That
> one is dynamic programming**, not a graph.
>
> **Three variants, three different techniques, and the question that separates them is about contiguity and
> trade-offs rather than about the code.**"

### The model answer

*"A delivery drone flies along a straight route with charging pads at fixed points. At each pad, the amount of
charge available tells you how many pads further you can fly before needing to land again. Given the charge at
each pad, can the drone reach the last one — and if so, what is the fewest landings?"*

> "Two questions, and **they are the same idea used twice**, so let me establish the shape once and then answer
> both.
>
> **My first instinct is dynamic programming — 'is pad `i` reachable' — and I would not write it**, because it
> is `O(n²)` and there is a linear answer.
>
> **The insight is that I do not need to know which pads are reachable. I need to know how far I can get.**
>
> **And that works because reachability here is contiguous**: if the drone can reach pad seven, it can reach
> every pad before it — **it can always land early.** **So the reachable set is always a prefix, and a prefix is
> one number.**
>
> **I would confirm that assumption explicitly**, because it is the thing the whole approach depends on: **can
> the drone land at any pad within range, or must it fly the full distance its charge allows?** **If it must
> fly the maximum, reachability is not contiguous and this becomes a graph.**
>
> **Question one, assuming it can land early: one pass with a single number.** Walk the pads left to right
> keeping `furthest`. **At each pad, if its index is beyond `furthest`, the drone cannot get here — return
> false.** Otherwise extend `furthest` to the maximum of itself and `i + charge[i]`.
>
> **`O(n)` time, `O(1)` space, and the guard is the important line** — without it the loop reasons from a pad
> the drone never reached, **and a pad with zero charge stops it in reality and not in the code.**
>
> **Question two — the fewest landings — is the same idea as a breadth-first search over levels.** From the
> start, one flight reaches a contiguous range of pads. From anywhere in that range, another flight reaches
> further. **The answer is which level contains the last pad.**
>
> **And the levels are contiguous, so two numbers describe one** — where this level ends and how far anything
> in it can reach. **When I arrive at the level boundary, that is another landing.**
>
> **The loop stops one short of the end**, because arriving at the final pad does not require taking off from
> it.
>
> **Both are `O(n)` and constant space**, so a route with a million pads is a fraction of a second.
>
> **Now three things about the domain that I would raise, because the textbook version hides them.**
>
> **First, the charge probably is not an integer number of pads.** It is a distance, and the pads are at
> irregular positions. **That does not change the algorithm** — the frontier becomes a distance rather than an
> index, and I advance through the pads while their position is within it — **but it does mean working in
> distances, and I would want to know the units.**
>
> **Second, wind and payload change the range**, so the charge-to-distance conversion is not fixed. **The
> algorithm still applies with a conservative estimate**, and I would want a safety margin as an explicit
> parameter rather than baked into the numbers.
>
> **And third, the question that would change the algorithm: is there a cost to landing?** Time, battery wear,
> a fee at the pad. **If landings have different costs, greedy breaks** — the furthest pad may be the most
> expensive place to land — **and it becomes dynamic programming.** **Fewest landings and cheapest route are
> different problems**, and I would want to know which one is actually wanted before committing to the greedy
> answer."

---

## 9. Recall card

**This looks like DP and is greedy.** The naive `dp[i] = is position i reachable` is `O(n²)` and correct and
**remembers more than it needs.** **The insight: you do not need to know WHICH positions are reachable, only
HOW FAR you can reach** — one number.

**It works because reachability is CONTIGUOUS**: reach position 7 and you reach everything before it, **so the
reachable set is always a prefix and a prefix is one number.** `O(n)` time, `O(1)` space.

**The stopping rule is the line people omit:** `if i > furthest: return False`. Without it the loop walks past
an unreachable position **and updates the frontier from it** — returning `True` for `[3,2,1,0,4]`. **It fails
only on inputs containing a zero**, which is why it survives. **And the update must be `max(furthest, i+jump)`**
— reachability only ever grows.

**Minimum jumps is a BFS with the queue collapsed into two numbers**, because the levels are contiguous
ranges: `current_end` (where this level stops) and `furthest` (how far anything in it reaches). **`if i ==
current_end` is the level boundary.** **The loop stops ONE SHORT** — landing on the last position needs no jump
from it — **and including it is exactly one too many on every input, with no error.**

**The exchange argument:** greedy jumps to the spot with the furthest reach; swapping it into any optimal
sequence is legal (both are in the current level) and no worse (it reaches at least as far), **so anything the
optimum could do next, greedy can too.** **The property it depends on is contiguity — "further is simply
better", with no trade-off.**

**The test for which technique you have: is the reachable set always a contiguous prefix?** **Yes → one number,
greedy.** **Jump left OR right → scattered, not a prefix → a graph, plain BFS, and the `O(1)` space is gone.**
**Add a cost per jump → contiguity survives but "further is better" does not, because reach and price trade
off → dynamic programming.**
