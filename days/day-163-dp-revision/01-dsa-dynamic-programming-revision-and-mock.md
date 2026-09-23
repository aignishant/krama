---
day: 163
track: dsa
title: "Dynamic programming revision and mock round"
phase: "Dynamic programming"
status: written
---

# Dynamic programming revision and mock round

## 1. What this is, and why they ask it

Twenty days of dynamic programming end here. **This is not new material — it is the day you find out what you
actually have.**

The lesson has two halves. **The first is a compression**: every shape, every recurrence, every trap, on one
page, in the form you would need it under pressure. **The second is a mock round** — three problems with a
clock, and a scoring rubric that tells you what an interviewer is actually watching.

They ask you to do this — implicitly, by making DP a third of the interview loop — because **recall under
pressure is a different skill from understanding at leisure.** You have written all eight shapes. **The
question is whether, with an interviewer watching and eight minutes gone, you can produce the state definition
for the one in front of you.**

**The honest thing about this day is that it will show you gaps**, and that is what it is for. **A gap found
today is twenty minutes of revision; the same gap found in an interview is the interview.**

The other reason this day matters is the rubric. **Candidates consistently misjudge what is being scored.**
They optimise for finishing the code and are marked on whether they stated the state, checked the complexity,
handled the edge cases, and noticed the follow-up. **Knowing what is measured changes what you do with your
forty-five minutes**, and that is worth more than another problem solved.

By the end of this lesson you have the whole subject on one page, three timed problems attempted honestly,
and a specific list of what to revise before your next interview.

---

## 2. The story

The exam was in eleven days and Nandini had done everything she was supposed to do, which was the problem.

**She had read all of it.** Every chapter, twice, and the notes were beautiful — colour-coded, tabbed, with
little arrows joining the parts that belonged together. Her mother, who had not been to college, thought they were the most impressive thing she had
ever seen.

**And on the Tuesday she sat down with a past exam and could not start the first question.**

Not because she did not know it. **She knew it perfectly well, and she found that out an hour later when she
looked at the answer and thought "oh, obviously".** She had known it and she had not been able to *reach* it.

Her cousin, who had done this two years earlier and failed and then passed, told her the thing that actually
helped.

**"Stop reading. You are not short of material. You are short of retrieval."**

And then he made her do something she hated.

**He took the notes away.** Physically. Put them in another room. And he asked her questions out of the past
paper, one at a time, with a clock, **and made her answer out loud with nothing in front of her.**

**The first evening was awful.** She got about a third of them and she was slow and she knew she was slow, and
twice she said something confidently that was wrong.

**But she found out exactly which third she did not have.**

Which was the point, and it was six topics out of forty, and they were not the ones she would have guessed.
**They were the ones she had read most recently, because she had confused "I just read this" with "I know
this".**

The second evening was better and the fourth was fine.

**And the thing her cousin said at the end, which she repeated to her own students for the next twenty
years:**

**"Reading tells you what you have seen. Only being asked tells you what you have."**

---

## 3. The idea in plain English

Nandini's cousin is right, and this section is the notes-in-the-other-room version: **everything, compressed,
so you can check what you can produce rather than what you recognise.**

**The whole subject in one paragraph.**

**Dynamic programming is: find a state that completely describes a situation, write a recurrence for it in
terms of smaller states, and compute each state once.** Everything else — the shapes, the fill orders, the
space collapses — is mechanics that follow from those three things.

**The recognition procedure, from yesterday, in five lines.**

```
1. SIGNALS      max/min/count/possible? small set of choices?
                exponential naive? constraint small?
2. TEST         optimal substructure AND overlapping subproblems
3. SHAPE        what do I need to know to decide the next step?
4. STATE        say it as a full sentence
5. COUNT        states x work, against ~10^7
```

**The eight shapes, with their canonical problems and costs.**

```
  shape                state              example              cost
  ---------------------------------------------------------------------
  1-D, bounded look    dp[i]              climbing stairs      O(n), O(1) space
  1-D + resource       dp[i][cap]         knapsack             O(n*W)
  1-D + mode           dp[i][mode]        buy/sell stock       O(n*m)
  two sequences        dp[i][j]           edit distance        O(n*m)
  grid                 dp[r][c]           unique paths         O(r*c), O(c) space
  interval             dp[i][j] one seq   burst balloons       O(n^3), O(n^2) space
  tree                 recursion          diameter             O(n), O(depth)
  bitmask              dp[mask]           TSP                  O(2^n * n^2)
```

**The recurrences worth having in memory, exactly.**

```
knapsack 0/1       dp[c] = max(dp[c], dp[c-w] + v)      c DESCENDING
knapsack unbounded dp[c] = max(dp[c], dp[c-w] + v)      c ASCENDING
coin change (min)  dp[t] = min(dp[t], dp[t-coin] + 1)   ASCENDING, dp[0]=0, rest inf
coin change (ways) dp[t] += dp[t-coin]                  coins OUTSIDE = combinations
LIS                dp[i] = 1 + max(dp[j]) for j<i, nums[j]<nums[i]; answer max(dp)
LCS                match: dp[i-1][j-1]+1; else max(dp[i-1][j], dp[i][j-1])
edit distance      match: dp[i-1][j-1];   else 1 + min(diag, up, left)
                   base cases are i and j, NOT zeros
grid paths         dp[c] += dp[c-1]                     one row
palindrome         dp[i][j] = s[i]==s[j] and dp[i+1][j-1]   fill by LENGTH
interval           dp[i][j] = best over k of dp[i][k] + dp[k+1][j] + join
stock              not_holding = max(nh, h + price); holding = max(h, nh - price)
tree               children first, then combine
TSP                dp[mask|1<<n][n] = dp[mask][last] + dist[last][n]
```

**Every trap from the month, in one list.** These are the ones that produce **wrong answers with no error**,
which is the only kind that matters.

```
  1.  wrong loop DIRECTION (0/1 vs unbounded)       -> different problem, no error
  2.  wrong loop NESTING (combinations vs perms)    -> different question, no error
  3.  incomplete STATE (LIS, stock)                 -> plausible wrong number
  4.  dp[-1] instead of max(dp) (LIS, maximal sq)   -> too small
  5.  zero base cases in edit distance              -> far too small
  6.  +1 on a match in edit distance                -> distance to itself non-zero
  7.  no clamp on negative children (tree path sum) -> forced through losses
  8.  best = 0 instead of -inf                      -> returns the empty path
  9.  fill order in interval DP                     -> too CHEAP, harder to spot
  10. record vs return in tree DP                   -> grows with the tree
  11. transaction counted on both halves            -> halves the limit
  12. missing the trip home in TSP                  -> the open-path answer
  13. k >= n/2 shortcut omitted                     -> MemoryError
  14. one row where a dependency is to the right    -> wrong generation
  15. missing row[0] = i after collapsing           -> too small
```

**Fifteen bugs, and not one of them raises an exception.** That list is the single most useful thing in this
lesson.

**The three questions asked after every DP solution, and the answers.**

**"What is the complexity?"** — states times work per state, said as a product, **plus the space, plus what
the space collapses to.**

**"Can you reduce the space?"** — the rule from day 161: **keep what the recurrence reads.** And **"no, because
it reads many rows" is a correct answer** for interval DP.

**"Can you do better?"** — sometimes yes and usually no, and **knowing which is the answer.** Coin change has a
BFS formulation; palindromic substrings has Manacher's; the assignment problem has the Hungarian algorithm;
**travelling salesman does not, because it is NP-hard.**

**Now the rubric, which is the part candidates get wrong.**

**What interviewers actually score, roughly in order of weight:**

```
  1. Did you state the STATE, in words, before coding?          heavily
  2. Did you check the complexity, unprompted?                  heavily
  3. Is the recurrence correct?                                 heavily
  4. Did you handle the base cases and edge cases?              moderately
  5. Did you communicate while thinking?                        moderately
  6. Did the code run?                                          less than you think
  7. Did you find the optimal solution first try?               barely
```

**Two things on that list surprise people.**

**"Did the code run" is item six.** A candidate with a correct state, a correct recurrence, stated complexity
and one syntax error scores far above a candidate with working code and no explanation. **The code is
evidence of the thinking, not the thing being measured.**

**And "first try" barely counts at all.** Proposing brute force, computing its cost, identifying the overlap
and improving it **is the expected path** — it demonstrates the reasoning, where jumping straight to the answer
demonstrates only recall.

**The time budget for a forty-five minute round:**

```
  0-3    clarify: constraints, edge cases, what the output is
  3-6    brute force, out loud, with its cost
  6-10   recognise DP: signals, test, shape, STATE AS A SENTENCE
 10-13   recurrence and base cases, on the board, before any code
 13-30   write it — memoised first
 30-35   trace one small example by hand
 35-40   complexity, space reduction, edge cases
 40-45   follow-ups
```

**The first ten minutes contain no code**, and that is deliberate. **Candidates who start coding at minute
four spend minutes twenty to thirty-five discovering their state was wrong.**

---

## 4. The picture

The subject on one page:

```
                        IS IT DP?
        signals -> test -> shape -> state -> count
                            |
        +-------------------+-------------------+
        |          |          |         |       |
      1-D       2-D        interval   tree   bitmask
        |          |          |         |       |
   dp[i]     dp[i][j]    dp[i][j]   recurse  dp[mask]
   dp[i][cap]  (two seqs   (one seq,          dp[mask][last]
   dp[i][mode]  or a grid)  split at k)
        |          |          |         |       |
        +-------------------+-------------------+
                            |
              recurrence + base cases
                            |
                    MEMOISE (fill order free)
                            |
                    tabulate if asked
                            |
                    collapse space if asked
```

The fill orders, all of them, in one place:

```
  shape        loop order                  why
  ---------------------------------------------------------------
  1-D          i ascending                 reads i-1, i-2
  knapsack     capacity DESCENDING (0/1)   must read the PREVIOUS row
               capacity ASCENDING (unbdd)  may read the CURRENT row
  2-D grid     rows then columns           reads above and left
  interval     LENGTH outermost            reads STRICTLY SHORTER ranges
  palindrome   LENGTH outermost            reads dp[i+1][j-1]
  tree         post-order (recursion)      children before parent
  bitmask      mask ascending              adding a bit increases the int

  THREE of these are non-obvious, and all three produce
  wrong answers with no error.
```

The space collapses, all of them:

```
  reads                    keep                    example
  ---------------------------------------------------------------
  dp[i-1], dp[i-2]         2 variables             fibonacci
  the previous row         1 row                   grid paths
  previous row + diagonal  1 row + 1 variable      edit distance
  previous row to the      2 rows (NOT one)        min falling path
    RIGHT
  many rows                NOTHING — say so        interval DP

  and ALWAYS: reconstruction needs the full table.
  Both? Hirschberg's: 2x time, linear space.
```

The fifteen silent bugs, as a checklist:

```
  BEFORE SUBMITTING, CHECK:

  [ ] loop direction — did I say why, out loud?
  [ ] loop nesting — combinations or permutations?
  [ ] is the state COMPLETE? (can I decide the next step from it alone?)
  [ ] is the answer dp[last] or max(dp)?
  [ ] base cases — are they zeros, or something else?
  [ ] is a "match" free, or does it cost one?
  [ ] negatives — do I need a clamp, and is my initial best -inf?
  [ ] interval DP — is LENGTH the outer loop?
  [ ] tree DP — what do I RECORD and what do I RETURN?
  [ ] counted resource — is it consumed in exactly ONE place?
  [ ] TSP — did I add the trip home?
  [ ] huge k — is there a shortcut for when the limit cannot bind?
  [ ] collapsed row — are the base cases re-established each row?

  NONE of these raise an exception.
```

The interview clock:

```
   0    5    10   15   20   25   30   35   40   45
   |----|----|----|----|----|----|----|----|----|
   [clarify]
        [brute force + cost]
             [DP: signals, shape, STATE]
                  [recurrence + base cases]
                       [============ code ============]
                                                [trace]
                                                     [cost, space, edges]
                                                          [follow-ups]

   NO CODE BEFORE MINUTE THIRTEEN.

   Candidates who start coding at minute 4 spend minutes 20-35
   discovering their state was wrong — and then have no time left.
```

---

## 5. The code, built step by step

### Mock problem one, warm-up: fifteen minutes

> *You are given an array of house values along a circular street — the first and last houses are adjacent.
> You may not rob two adjacent houses. Return the maximum you can take.*

**Diagnose before reading further.** Signals, shape, state, count. Then look:

```python
def rob_circular(nums: list[int]) -> int:
    """House robber, but the street is a circle."""
    if len(nums) == 1:
        return nums[0]

    def rob_line(values: list[int]) -> int:
        take, skip = 0, 0
        for v in values:
            take, skip = skip + v, max(take, skip)
        return max(take, skip)

    # the circle: either house 0 is excluded, or the last one is.
    return max(rob_line(nums[1:]), rob_line(nums[:-1]))
```

**The insight is that the circular constraint reduces to two linear problems.** House zero and the last house
cannot both be taken, **so either exclude the first or exclude the last, and take the better.**

**That reduction is the whole difficulty**, and it is a pattern worth naming: **when a constraint couples two
ends, try splitting into cases that break the coupling.**

**Cost: `O(n)` time, `O(1)` space, two passes.**

### Mock problem two, the main one: twenty-five minutes

> *Given a string `s` and a dictionary of words, return the minimum number of extra characters left over if
> you break `s` optimally into dictionary words. Characters not part of any word count as extra.*

```python
def min_extra_char(s: str, dictionary: list[str]) -> int:
    """dp[i] = the fewest leftover characters in the first i characters."""
    words = set(dictionary)
    n = len(s)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + 1                 # treat s[i-1] as leftover
        for j in range(i):
            if s[j:i] in words:
                dp[i] = min(dp[i], dp[j])     # s[j:i] is a word: no cost
    return dp[n]
```

**The state as a sentence: `dp[i]` is the minimum number of leftover characters in the first `i` characters of
`s`.**

**The default is `dp[i-1] + 1`** — this character is left over — **and then any word ending here gives an
alternative.**

**Two things worth saying out loud.** **The answer is `dp[n]`, not `min(dp)`**, because the state covers the
whole prefix rather than "ending at". **And `s[j:i] in words` is `O(i-j)` for the slice**, so the true cost is
`O(n³)` rather than `O(n²)` — **which a trie fixes, and which is the natural follow-up.**

### The follow-up, if asked

```python
class TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_word = False


def min_extra_char_trie(s: str, dictionary: list[str]) -> int:
    root = TrieNode()
    for word in dictionary:
        node = root
        for ch in reversed(word):             # REVERSED: the scan walks leftwards
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    n = len(s)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + 1
        node = root
        for j in range(i - 1, -1, -1):        # extend leftwards through the trie
            ch = s[j]
            if ch not in node.children:
                break                          # no word can start here — stop
            node = node.children[ch]
            if node.is_word:
                dp[i] = min(dp[i], dp[j])
    return dp[n]
```

**The trie holds the words REVERSED**, and that is the detail to get right: the scan fixes the *end* position
`i` and walks leftwards, **so it sees each candidate word back to front.**

**And the `break` is the whole saving**: once the characters stop forming any word's suffix, **no longer
suffix can either**, so the inner loop stops early instead of running to zero.

**`O(n × L)` where `L` is the longest word**, rather than `O(n³)`.

### Mock problem three, the hard one: twenty minutes

> *Given an integer array, partition it into contiguous subarrays of length at most `k`. Each subarray's
> values all become the maximum in that subarray. Return the largest sum of the array after partitioning.*

```python
def max_sum_after_partitioning(arr: list[int], k: int) -> int:
    """dp[i] = the best sum for the first i elements."""
    n = len(arr)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        best_in_window = 0
        for length in range(1, min(k, i) + 1):        # the LAST group's length
            best_in_window = max(best_in_window, arr[i - length])
            dp[i] = max(dp[i], dp[i - length] + best_in_window * length)
    return dp[n]
```

**The decision is the length of the last group**, which is the recurring trick in partition problems: **do not
ask where the first cut goes; ask how long the last piece is.**

**`best_in_window` is maintained as the window grows leftwards**, which avoids recomputing the maximum — **and
that is the difference between `O(n·k)` and `O(n·k²)`.**

**Cost: `O(n × k)` time, `O(n)` space.**

### The self-scoring harness

```python
import time
from dataclasses import dataclass, field


@dataclass
class Attempt:
    name: str
    minutes_to_state: float
    minutes_total: float
    stated_complexity: bool
    handled_edges: bool
    correct_first_run: bool
    notes: str = ""

    def score(self) -> int:
        """The rubric, weighted the way interviewers actually weight it."""
        points = 0
        points += 30 if self.minutes_to_state <= 10 else 10
        points += 25 if self.stated_complexity else 0
        points += 25 if self.correct_first_run else 15    # partial credit
        points += 10 if self.handled_edges else 0
        points += 10 if self.minutes_total <= 25 else 0
        return points


def report(attempts: list[Attempt]) -> None:
    print(f"{'problem':32} {'to state':>9} {'total':>7} {'score':>6}")
    for a in attempts:
        print(f"{a.name:32} {a.minutes_to_state:>7.1f}m "
              f"{a.minutes_total:>6.1f}m {a.score():>6}/100")
        if a.notes:
            print(f"    -> {a.notes}")
    average = sum(a.score() for a in attempts) / len(attempts)
    print(f"\naverage {average:.0f}/100")
    if average >= 80:
        print("  -> ready. Keep the pace and do timed sets weekly.")
    elif average >= 60:
        print("  -> close. The gap is usually SPEED TO THE STATE.")
    else:
        print("  -> revise the shapes. Redo the state sentences from memory.")
```

**Fill this in honestly after each attempt.** The score is not the point; **`minutes_to_state` is the point**,
because it is the number that predicts everything else.

### The verification habit

```python
def check_against_brute_force(fast, slow, generate, trials: int = 500) -> None:
    """The single most valuable five minutes after writing a DP."""
    import random
    for _ in range(trials):
        case = generate(random)
        expected, actual = slow(*case), fast(*case)
        if expected != actual:
            print(f"MISMATCH on {case}: brute {expected}, dp {actual}")
            return
    print(f"agreed on {trials} random cases")
```

**Random testing against a slow, obviously-correct brute force catches every one of the fifteen silent bugs.**
It costs five minutes, **and it is the only reliable defence against a wrong answer that raises no error.**

### The complete solution

```python
"""DP revision: three mock problems, the rubric, and the verification habit."""

import random
from dataclasses import dataclass


# ---------- mock 1: house robber on a circle ----------

def rob_circular(nums: list[int]) -> int:
    """Circular constraint -> two linear problems. O(n) time, O(1) space."""
    if len(nums) == 1:
        return nums[0]

    def rob_line(values: list[int]) -> int:
        take, skip = 0, 0
        for v in values:
            take, skip = skip + v, max(take, skip)
        return max(take, skip)

    return max(rob_line(nums[1:]), rob_line(nums[:-1]))


def rob_circular_brute(nums: list[int]) -> int:
    n = len(nums)
    if n == 1:
        return nums[0]
    best = 0
    for mask in range(1 << n):
        ok = True
        for i in range(n):
            if (mask >> i) & 1 and (mask >> ((i + 1) % n)) & 1:
                ok = False
                break
        if ok:
            best = max(best, sum(nums[i] for i in range(n) if (mask >> i) & 1))
    return best


# ---------- mock 2: minimum extra characters ----------

def min_extra_char(s: str, dictionary: list[str]) -> int:
    """dp[i] = fewest leftover characters in the first i characters."""
    words = set(dictionary)
    n = len(s)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + 1                 # this character is leftover
        for j in range(i):
            if s[j:i] in words:
                dp[i] = min(dp[i], dp[j])
    return dp[n]


class TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_word = False


def min_extra_char_trie(s: str, dictionary: list[str]) -> int:
    """O(n * longest_word) instead of O(n^3). The break is the saving."""
    root = TrieNode()
    for word in dictionary:
        node = root
        for ch in reversed(word):             # REVERSED: the scan walks leftwards
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    n = len(s)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + 1
        node = root
        for j in range(i - 1, -1, -1):
            ch = s[j]
            if ch not in node.children:
                break
            node = node.children[ch]
            if node.is_word:
                dp[i] = min(dp[i], dp[j])
    return dp[n]


# ---------- mock 3: partition array for maximum sum ----------

def max_sum_after_partitioning(arr: list[int], k: int) -> int:
    """The decision is the LENGTH OF THE LAST GROUP. O(n*k)."""
    n = len(arr)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        best_in_window = 0
        for length in range(1, min(k, i) + 1):
            best_in_window = max(best_in_window, arr[i - length])
            dp[i] = max(dp[i], dp[i - length] + best_in_window * length)
    return dp[n]


def max_sum_brute(arr: list[int], k: int) -> int:
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def best(i: int) -> int:
        if i == len(arr):
            return 0
        return max(
            max(arr[i:i + length]) * length + best(i + length)
            for length in range(1, min(k, len(arr) - i) + 1)
        )

    return best(0)


# ---------- the rubric ----------

@dataclass
class Attempt:
    name: str
    minutes_to_state: float
    minutes_total: float
    stated_complexity: bool
    handled_edges: bool
    correct_first_run: bool
    notes: str = ""

    def score(self) -> int:
        points = 0
        points += 30 if self.minutes_to_state <= 10 else 10
        points += 25 if self.stated_complexity else 0
        points += 25 if self.correct_first_run else 15
        points += 10 if self.handled_edges else 0
        points += 10 if self.minutes_total <= 25 else 0
        return points


def report(attempts: list[Attempt]) -> None:
    print(f"\n{'problem':34} {'to state':>9} {'total':>8} {'score':>8}")
    for a in attempts:
        print(f"{a.name:34} {a.minutes_to_state:>7.1f}m "
              f"{a.minutes_total:>7.1f}m {a.score():>6}/100")
        if a.notes:
            print(f"    -> {a.notes}")
    average = sum(a.score() for a in attempts) / len(attempts)
    print(f"\naverage {average:.0f}/100")
    if average >= 80:
        print("  -> ready. Keep the pace; do a timed set weekly.")
    elif average >= 60:
        print("  -> close. The gap is usually SPEED TO THE STATE.")
    else:
        print("  -> revise the shapes; redo the state sentences from memory.")


def check_against_brute_force(fast, slow, generate, trials: int = 300) -> None:
    """Five minutes that catches every one of the fifteen silent bugs."""
    for _ in range(trials):
        case = generate(random)
        if slow(*case) != fast(*case):
            print(f"  MISMATCH on {case}: brute {slow(*case)}, dp {fast(*case)}")
            return
    print(f"  agreed on {trials} random cases")


if __name__ == "__main__":
    print("MOCK 1 — house robber on a circle")
    print("  [2,3,2]    ->", rob_circular([2, 3, 2]))
    print("  [1,2,3,1]  ->", rob_circular([1, 2, 3, 1]))
    print("  [1,2,3]    ->", rob_circular([1, 2, 3]))
    check_against_brute_force(
        rob_circular, rob_circular_brute,
        lambda r: ([r.randint(0, 20) for _ in range(r.randint(1, 10))],))

    print("\nMOCK 2 — minimum extra characters")
    print('  "leetscode", [leet,code,leetcode] ->',
          min_extra_char("leetscode", ["leet", "code", "leetcode"]))
    print('  "sayhelloworld", [hello,world]    ->',
          min_extra_char("sayhelloworld", ["hello", "world"]))
    print("  trie version agrees              :",
          min_extra_char_trie("leetscode", ["leet", "code", "leetcode"]),
          min_extra_char_trie("sayhelloworld", ["hello", "world"]))

    print("\nMOCK 3 — partition array for maximum sum")
    print("  [1,15,7,9,2,5,10], k=3 ->", max_sum_after_partitioning(
        [1, 15, 7, 9, 2, 5, 10], 3))
    print("  [1,4,1,5,7,3,6,1,9,9,3], k=4 ->", max_sum_after_partitioning(
        [1, 4, 1, 5, 7, 3, 6, 1, 9, 9, 3], 4))
    check_against_brute_force(
        max_sum_after_partitioning, max_sum_brute,
        lambda r: ([r.randint(1, 30) for _ in range(r.randint(1, 12))],
                   r.randint(1, 4)))

    report([
        Attempt("robber on a circle", 4.0, 12.0, True, True, True),
        Attempt("minimum extra characters", 11.0, 24.0, True, True, True,
                "spotted the O(n^3) slice cost — good; state took 11 minutes"),
        Attempt("partition for maximum sum", 14.0, 31.0, True, False, False,
                "slow to the state: took too long to see the LAST GROUP idea"),
    ])
```

Run it and you get:

```
MOCK 1 — house robber on a circle
  [2,3,2]    -> 3
  [1,2,3,1]  -> 4
  [1,2,3]    -> 3
  agreed on 300 random cases

MOCK 2 — minimum extra characters
  "leetscode", [leet,code,leetcode] -> 1
  "sayhelloworld", [hello,world]    -> 3
  trie version agrees              : 1 3

MOCK 3 — partition array for maximum sum
  [1,15,7,9,2,5,10], k=3 -> 84
  [1,4,1,5,7,3,6,1,9,9,3], k=4 -> 83
  agreed on 300 random cases

problem                             to state    total    score
robber on a circle                     4.0m    12.0m    100/100
minimum extra characters              11.0m    24.0m     80/100
    -> spotted the O(n^3) slice cost — good; state took 11 minutes
partition for maximum sum             14.0m    31.0m     50/100
    -> slow to the state: took too long to see the LAST GROUP idea

average 77/100
  -> close. The gap is usually SPEED TO THE STATE.
```

**The two `agreed on 300 random cases` lines are the habit worth taking away.** Both DP solutions were checked
against a slow, obviously-correct version on hundreds of random inputs — **which is the only defence against
the fifteen bugs that raise no exception.**

**And the score report is the honest part.** One problem clean, and **two where the state took more than ten
minutes** — which is the pattern the rubric is designed to expose. **The diagnosis is specific: not "revise
DP", but "the last-group decomposition in partition problems", which is twenty minutes of work rather than a
week.**

---

## 6. What it costs

**The three mock problems, by complexity:**

```
  robber on a circle        O(n) time, O(1) space, two passes
  minimum extra characters  O(n^3) naive (the slice is O(n))
                            O(n * L) with a trie, L = longest word
  partition for max sum     O(n * k) time, O(n) space
```

**The middle one is worth dwelling on**, because the hidden cost is the kind interviewers probe:

```
  for i in 1..n:            n
    for j in 0..i:            n
      s[j:i] in words           the SLICE is O(i-j), then the hash is O(len)
                                -> O(n) per check

  total: O(n^3), not O(n^2)

  n = 50 (the LeetCode constraint):  125,000 — fine
  n = 5,000:                          10^11 — impossible

  the trie version: O(n * L) where L is the longest word
  n = 5,000, L = 20:  100,000. Instant.
```

**Noticing that a string slice inside two loops makes it cubic is a real signal**, and it is the difference
between "it passes" and "I know what it costs".

**The revision material itself, measured:**

```
  eight shapes
  ~13 recurrences worth memorising
  ~7 fill orders, 3 of them non-obvious
  ~5 space collapses
  15 silent bugs

  -> about 50 discrete facts

at 30 seconds each to recite from memory: ~25 minutes for a full pass
-> a complete self-test the evening before an interview is
   ONE PASS, and it is worth doing
```

**Fifty facts and twenty-five minutes** is the useful framing: **this is a memorisable body of knowledge, not
an unbounded one.**

**The time budget, and where it actually goes wrong:**

```
  a candidate who starts coding at minute 4:
    4-20   writing
    20-30  discovering the state is wrong
    30-40  rewriting
    40-45  no time for complexity, edges or follow-ups
    -> scores on item 6 only

  a candidate who starts coding at minute 13:
    13-30  writing, from a correct state
    30-35  tracing an example
    35-45  complexity, space, edges, follow-ups
    -> scores on items 1, 2, 3, 4, 5 AND 6

  the nine "wasted" minutes at the start BUY the last fifteen.
```

**Random verification, costed:**

```
  writing a brute force for a small n:     ~5 minutes
  300 random trials:                       < 1 second

  what it catches: all fifteen silent bugs
  what it costs in an interview:           you would not run it there,
                                           but the HABIT of thinking
                                           "what would brute force say
                                           on [2,3,2]?" is free
```

**And the practice-to-interview ratio, honestly:**

```
  problems solved this month:          ~120
  distinct SHAPES:                     8
  distinct RECURRENCES:                ~13

-> the 120 problems were practice at RETRIEVING the 13.
   Which is why re-solving problems you have already seen has
   sharply diminishing returns, and why timed retrieval from
   memory does not.
```

---

## 7. The traps

**Reading instead of retrieving.** Nandini's mistake, and it is the one that matters today.

```
  reading a solution:      "yes, obviously"     -> recognition
  producing it from blank: "..."                -> recall

  These feel similar and are completely different skills.
  Only the second one is what an interview tests.
```

**The fix is to close everything and produce the state sentence out loud**, which is uncomfortable and is the
whole point of this day.

**Optimising for finishing the code.**

```python
>>> # a candidate who writes working code and says nothing:
>>> #   scores on item 6 of 7
>>> # a candidate who states the state, the recurrence, the complexity,
>>> #   and leaves one syntax error:
>>> #   scores on items 1, 2, 3, 5
```

**The code is evidence of the thinking, not the thing measured.** Silent correct code scores below explained
almost-correct code, **consistently, and candidates find this hard to believe.**

**Jumping to the optimal solution.**

```
  "This is longest increasing subsequence, here is the O(n log n)
   solution" — typed in ninety seconds

  -> demonstrates recall
  -> demonstrates NOTHING about how you would handle a problem
     you have not seen

  the expected path: brute force, its cost, the overlap, the table,
  then the improvement. It takes longer and it scores higher.
```

**Not stating the complexity unprompted.**

```
  being asked "what is the complexity?" costs you the point
  for having noticed
  -> say it as you finish, every time:
     "n times W states, constant work each, so O(nW) time and
      O(W) space after the collapse"
```

**Skipping the trace.**

```
  five minutes tracing dp on a 4-element input catches:
    wrong base cases, off-by-one, wrong loop direction,
    wrong answer cell

  candidates skip it because they are behind on time —
  and it is the cheapest bug-finding available
```

**Treating this day as reading.**

```
  reading this lesson:                 ~20 minutes, feels productive
  doing the three mocks with a clock:  ~60 minutes, feels bad

  only one of those tells you anything.
```

**And the specific failure this day exists to prevent:**

```
  "I know dynamic programming"        <- based on having solved 120 problems
  "I can produce the state definition
   for an unseen problem in under
   ten minutes"                       <- the thing actually required

  the gap between those two is what the mock round measures.
```

**Revising the wrong thing.**

```
  after a bad mock, the instinct is "revise DP"
  -> too broad to act on

  the useful version is what the score report gives:
    "slow to the state on partition problems"
    "forgot the loop direction reason"
    "did not check the state count"

  three specific gaps, twenty minutes each.
```

---

## 8. In the interview

### How it gets asked

- Any of the twenty days' problems, with no warning about which.
- *"How would you approach this?"* — before any code.
- *"What is your state?"* — the question that exposes everything.
- *"What is the complexity?"* — which you should have said already.
- *"Can you reduce the space?"* — the universal follow-up.
- *"Can you do better?"* — sometimes yes, usually no, and knowing which is the answer.

### The first ninety seconds

> **This is the template for any DP problem, and it is the thing to rehearse until it is automatic.**
>
> "Let me make sure I have the problem. **The input is an array of up to a thousand integers, the output is a
> single number, and values can be negative** — I would want to confirm that last one, because it affects the
> base case.
>
> **The brute force is to try every subset, which is `2^n`** — at a thousand elements that is not happening, so
> there is something better.
>
> **This looks like dynamic programming, for three reasons.** It asks for a maximum. **There is a small set of
> choices at each element — take it or skip it.** And the naive recursion branches two ways per element with
> the same subproblems appearing under different branches, **which is overlap, so a table pays for itself.**
>
> **The constraint of a thousand suggests a quadratic solution is acceptable**, which is consistent.
>
> **Now the state. The question I ask is: what do I need to know to decide about the next element?** Here it is
> where I am and how much capacity remains — **so the state is `dp[i][c]`: the best value using the first `i`
> items with `c` capacity left.**
>
> **Completeness check: given only `i` and `c`, can I decide what happens next?** Yes.
>
> **And the count: a thousand times the capacity, with constant work each.** If the capacity is up to ten
> thousand, that is ten million operations — **at the edge of comfortable in Python, fine in a compiled
> language.** If it were up to a billion, this approach would not exist and I would say so.
>
> **The recurrence: for each item, either skip it — `dp[i-1][c]` — or take it if it fits — `dp[i-1][c-w] + v`.
> Take the better.** Base case: zero items gives zero value.
>
> **I will write it memoised first**, because then the fill order cannot be wrong, **and convert it to a table
> if you want the space reduced — which collapses to one row, iterating capacity downwards so each item is used
> once.**
>
> **That is about two minutes and no code yet, which is deliberate** — I would rather find out now that the
> state is wrong than at minute thirty."

### The follow-ups

**"What is your state, and why is it enough?"**

> "The state as a sentence first: **`dp[i][c]` is the maximum value obtainable using the first `i` items with
> `c` capacity remaining.**
>
> **If I cannot finish that sentence, I do not have a state**, and writing code before I can is how twenty
> minutes disappear.
>
> **Then the completeness check, which is the part that catches the expensive mistakes: given only the values
> in the state, can I decide what happens next — without knowing anything about how I got here?**
>
> Here, yes. Knowing which item I am on and how much capacity is left is enough to decide about item `i`.
>
> **When the answer is no, the state is incomplete, and it fails silently.** That is the worst failure mode in
> the whole subject, because you can write code from an incomplete state and it runs and it produces plausible
> numbers.
>
> **The example I keep in mind is longest increasing subsequence.** The natural state — 'the longest increasing
> subsequence in the first `i` elements' — **cannot express the recurrence**, because when element `i` arrives
> I know a length but not what that subsequence ended on. **The fix is to redefine: 'ending exactly at `i`'**,
> which carries the ending value in the definition.
>
> **And notice the fix cost nothing** — still `n` cells. **Trying to redefine before adding a dimension is
> worth thirty seconds**, because adding a dimension multiplies the state space and redefining is often free.
>
> **Then the third thing, which is arithmetic: states times work per state, against about ten million.**
> Python does roughly ten million simple operations a second, C about a billion. **If the product is much
> above that, either the state has a dimension it does not need, or this is not DP.**
>
> **Those three steps — sentence, completeness, count — take ninety seconds, and they are what I do before any
> code.**"

**"Can you reduce the space?"**

> "The rule is: **look at which cells the recurrence reads, and keep only those.**
>
> **Here it reads the previous row only, so one row suffices** — `O(W)` instead of `O(nW)`. At a thousand items
> and ten thousand capacity that is ten thousand cells instead of ten million.
>
> **And the loop direction matters, which I would say while writing it.** Iterating capacity **downwards**
> guarantees that `dp[c-w]` still holds the previous row's value, **so each item is used once.** Iterating
> upwards would let it be reused — **which is the unbounded knapsack, a correct algorithm for a different
> problem, with no error to distinguish them.**
>
> **The general version of the rule covers everything I have written this month.** Reading `dp[i-1]` and
> `dp[i-2]` means two variables. Reading a previous row means one row. **Reading the previous row plus the
> diagonal — edit distance — means one row plus one saved variable**, because the diagonal is overwritten
> before you need it.
>
> **And there are two cases where the answer is no**, which I would give rather than attempt something that
> does not work. **Interval DP reads many rows at once**, so no subset of rows suffices — the full table has to
> be live. **And a recurrence that reads the previous row to the *right***, like minimum falling path sum,
> **needs two arrays**, because an in-place update has already overwritten it.
>
> **What every collapse costs is the reconstruction.** The array has been overwritten, so there is no history
> to walk back through. **I can have the value in linear space or the path in quadratic space.**
>
> **If you want both, that is Hirschberg's algorithm** — divide and conquer on the middle row, using the
> linear-space pass forwards and backwards to find where the optimal path crosses, then recursing on the two
> halves. **Exactly twice the time, linear space, and it gives the path.** I would look it up rather than write
> it from memory."

**"Can you do better than this complexity?"**

> "Sometimes, and knowing which case I am in is the real answer — so let me go through what I would check.
>
> **First: is there a closed form?** Counting problems often collapse. **Grid paths is a binomial coefficient**
> — `O(1)` space against a full table. If the problem is about counting arrangements, that is worth thirty
> seconds before building anything.
>
> **Second: is greedy actually correct?** If I can prove the local choice is safe, one pass beats a table.
> **The test is to try to construct a counter-example**, and if I fail, I look for an exchange argument.
>
> **Third: is there a better algorithm for this specific problem?** Several of the classics have one.
> **Longest increasing subsequence is `O(n log n)` with the tails array**, not `O(n²)`. **Palindromic
> substrings has Manacher's, which is linear.** **The assignment problem has the Hungarian algorithm at
> `O(n³)`, where bitmask DP is exponential** — and I would volunteer that one rather than let it be pointed
> out.
>
> **Fourth: can the constants come down?** A trie instead of repeated string slicing turned one of these from
> `O(n³)` to `O(n × L)`. **That is not an asymptotic improvement in the state count — it is the work per
> state**, and it is often where the real saving is.
>
> **And fifth: sometimes the honest answer is no, and saying so is correct.** **Travelling salesman is
> NP-hard**, so bitmask DP at `O(2ⁿ · n²)` is the best known exact algorithm — Held-Karp, from 1962, and
> nothing better has been found. **What exists instead is heuristics and approximation**, and offering those
> is the right answer rather than pretending an improvement exists.
>
> **The shape of the answer I want to give is: here are the four things I checked, here is which one applies,
> and here is why the others do not.** That is more useful than either 'no' or a half-remembered
> optimisation."

### The model answer

*"Take forty-five minutes. Here is the problem: given a string and a dictionary of words, break the string into
dictionary words so as to leave the fewest characters unused. Return that count."*

> **Minutes 0–3, clarifying.**
>
> "**A few questions.** Can words be reused — is the dictionary a multiset or a set? Can words overlap, or is
> this a strict partition into non-overlapping pieces? **What are the sizes — the string length and the number
> of words?** And are the words all lowercase?
>
> **Taking it as: a set, reusable, non-overlapping pieces, string up to fifty characters, up to fifty words of
> up to fifty characters each.**
>
> **Let me check my understanding with an example.** `"leetscode"` with `["leet", "code", "leetcode"]` — I take
> `leet` at positions 0 to 3 and `code` at 5 to 8, **leaving the `s` at position 4 unused, so the answer is
> one.**
>
> **Minutes 3–6, brute force.**
>
> **The naive approach is: at every position, either skip this character as unused, or try every word that
> starts here.** That branches, so it is exponential — roughly `2ⁿ` in the worst case. At fifty characters
> that is `10¹⁵`, so there is something better.
>
> **Minutes 6–10, recognising it.**
>
> **Four signals.** It asks for a **minimum**. There is a **small set of choices** at each position — skip, or
> take one of the words ending here. **The naive recursion is exponential.** And the constraint is small.
>
> **The test: does the same subproblem recur?** Yes — 'the best for the first `i` characters' is reached by
> many different prefixes. **Overlap, so a table pays for itself.**
>
> **The shape: what do I need to know to decide the next step?** Just how far along the string I am — **the
> characters before that point do not affect what I can do next, only how much waste I have accumulated.**
> **So it is one-dimensional.**
>
> **The state: `dp[i]` is the minimum number of leftover characters in the first `i` characters of the
> string.**
>
> **Completeness: given only `i` and that value, can I decide about the next character?** Yes.
>
> **Count: `n` states, and the work per state is scanning back over previous positions — so `O(n²)` states
> times work.** At fifty characters that is 2,500. Trivial.
>
> **Minutes 10–13, the recurrence.**
>
> **The default is that character `i-1` is leftover: `dp[i] = dp[i-1] + 1`.**
>
> **Then for every earlier position `j`, if the substring from `j` to `i` is a word, I could have used it —
> and then the leftover count is just `dp[j]`, because the word costs nothing.** Take the minimum.
>
> **Base case: `dp[0] = 0`** — no characters, no waste. **Answer: `dp[n]`**, not the minimum over the array,
> because the state covers the whole prefix rather than 'ending at'.
>
> **Minutes 13–30, writing it.** *(writes the loop version)*
>
> **Minutes 30–35, tracing.**
>
> **Let me walk `"leetscode"` by hand.** `dp[4]` is zero, because `leet` is a word covering positions 0 to 3.
> `dp[5]` is one — the `s` is leftover and no word ends at position 5. **`dp[9]` is one, via `dp[5]` plus
> `code`.** Which matches the expected answer.
>
> **Minutes 35–40, cost and edges.**
>
> **And here is something I want to flag about the complexity, because it is easy to state wrongly.** The loops
> are `O(n²)`, **but `s[j:i]` builds a new string, which is `O(i-j)`** — so the real cost is `O(n³)`, not
> `O(n²)`. At fifty characters that is 125,000 and completely fine, **but I would not want to claim `O(n²)`
> when it is not.**
>
> **Space is `O(n)` for the table plus the word set. No collapse is available** — the recurrence reads `dp[j]`
> for every earlier `j`, so the whole array has to be live.
>
> **Edge cases: an empty string gives zero. A string with no matching words gives its own length. And a word
> longer than the string is simply never matched** — no special handling needed, which is worth confirming
> rather than assuming.
>
> **Minutes 40–45, the follow-up, which I would raise myself.**
>
> **If the string were five thousand characters rather than fifty, the cubic version would be `10¹¹` and would
> not finish.** The fix is a **trie of the dictionary**: for each ending position, walk backwards through the
> trie one character at a time. **When the characters stop forming any word's suffix, break out — because no
> longer suffix can match either.**
>
> **That is `O(n × L)` where `L` is the longest word — a hundred thousand operations at `n = 5,000` instead of
> `10¹¹`** — and it removes the string slicing entirely, which was where the hidden cost was.
>
> **If you would like, I can write that version.**"

---

## 9. Recall card

**DP in one sentence: find a state that completely describes a situation, write a recurrence over smaller
states, compute each once.** Everything else is mechanics.

**Eight shapes:** `dp[i]` / `dp[i][cap]` / `dp[i][mode]` / `dp[i][j]` two sequences / `dp[r][c]` grid /
`dp[i][j]` interval / recursion for trees / `dp[mask]`. **The one question that picks the shape: what do I need
to know to decide the next step?**

**Three non-obvious fill orders, all silent when wrong:** knapsack **descending** for 0/1 and **ascending** for
unbounded; interval DP by **increasing length**; tree DP **post-order** (free, from the recursion).

**Fifteen bugs that raise no exception** — loop direction, loop nesting, incomplete state, `dp[-1]` vs
`max(dp)`, zero base cases in edit distance, `+1` on a match, no clamp on negatives, `best = 0` not `-inf`,
interval fill order, record-vs-return in trees, a resource counted twice, the missing trip home, the missing
`k ≥ n/2` shortcut, a dependency to the right, and the missing `row[0] = i` after collapsing. **Random testing
against a brute force catches all fifteen in five minutes.**

**The rubric, in weight order: state stated before coding, complexity given unprompted, recurrence correct,
edge cases, communication — and only then whether the code ran.** "Finished it first try" barely counts.
**No code before minute thirteen**: the nine minutes at the start buy the last fifteen.

**Say the state as a full SENTENCE, run the completeness check, count states × work against ~10⁷** — ninety
seconds, before anything else. **Then memoise** (the fill order cannot be wrong), tabulate and collapse only if
asked. **And reading is not retrieval**: close everything and produce it out loud, because that is the only
thing that tells you what you actually have.
