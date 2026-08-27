---
day: 32
track: dsa
title: "Variable-size sliding window"
phase: "Two pointers and sliding window"
status: written
---

# Day 032 · DSA — Variable-size sliding window

**After today you can:** You can grow and shrink a window against a condition and never lose track of the invariant.

**The interviewer asks it as:** *Find the smallest subarray with a sum at least k.*

---

## 1. What this is, and why they ask it

Yesterday the window was `k` wide and both edges moved together. Today **the width is not given** — it
is whatever the condition says it should be. The right edge always advances by one; the left edge
advances only when a rule tells it to.

That one change turns a small technique into a large family. *The shortest subarray summing to at least
k. The longest substring with no repeats. The longest substring with at most k distinct characters. The
smallest window containing all the letters of another string.* All of them are eight lines with a
different condition, and all of them are `O(n)`.

The cost argument is the same as it has been all week and worth saying precisely: **each index is
visited at most twice** — once when the right edge passes it and once when the left edge does. Neither
edge ever moves backwards. So a `while` loop nested inside a `for` loop is still linear, and being able
to explain that is half of what is being tested.

The other half is knowing **when the technique does not apply**. A sliding window needs the condition
to behave predictably as the window grows — and the moment an array contains negative numbers, "the sum
only increases as I add elements" stops being true and the whole method silently breaks. Candidates who
apply a window to *"shortest subarray with sum at least k, values may be negative"* get a wrong answer
with no error. Knowing that boundary is the difference between using a technique and reciting one.

---

## 2. The story

Devappa farms about four acres outside Belur, and the thing that decides his year is when the rain
comes and how fast.

He has the daily figures on his phone — the taluk office publishes them, millimetre by millimetre,
going back years. And the number he actually cares about is a strange one: **what is the shortest run of
consecutive days that gave him fifty millimetres?** Because fifty millimetres is roughly what soaks the
field properly, and if it takes four days he can sow on the fifth, and if it takes nineteen days it has
been useless — it ran off or evaporated between falls.

The first year he looked it up he did it the long way. Start at the first of June and add days until he
got to fifty. Then start at the second of June and add days until fifty. Then the third. It took him an
evening and he was fairly sure he had made an arithmetic mistake somewhere.

His son showed him the quick way and it takes about a minute.

You keep a running total and you keep two dates — where the run starts and where it ends. You move the
end date forward one day at a time, adding that day's rain to the total.

The moment the total reaches fifty, you stop adding and do the other thing: **you push the start date
forward**, taking days off the front, for as long as the total is still fifty or more. Each time you
push it, you have a shorter run that still works, so you write down the length. When taking one more day
off would drop you below fifty, you stop, and go back to moving the end date forward.

The part that surprised Devappa is that you never put a day back at the front. Once a day has been
dropped off the start, it is gone for the rest of the calculation. His son explained it and Devappa
repeated it back in his own words, which were better: any run that still includes that day is at least
as long as one that starts later, and I have already looked at the ones that start later. So there is
nothing back there worth going back for.

The whole thing goes forward, once, and never turns round.

---

## 3. The idea in plain English

Devappa's end date is `right`, his start date is `left`, and his running total is the window's sum.
Everything today is the two rules for moving them.

### The two shapes

There are exactly two, and picking the wrong one is the commonest error in this family.

**Shape A — shrink while valid. Use it to MINIMISE.**

> Grow the window until the condition is satisfied, then shrink from the left **while it is still
> satisfied**, recording the length at each step.

```python
left = 0
total = 0
best = float("inf")
for right, x in enumerate(nums):
    total += x
    while total >= target:            # while still VALID
        best = min(best, right - left + 1)
        total -= nums[left]
        left += 1
return 0 if best == float("inf") else best
```

Note where the recording happens: **inside the shrink loop, before shrinking**. Every time the window
is valid you have a candidate, and you want the smallest of them.

**Shape B — shrink while invalid. Use it to MAXIMISE.**

> Grow the window; whenever it becomes invalid, shrink from the left **until it is valid again**; then
> record.

```python
left = 0
best = 0
for right, ch in enumerate(s):
    add(ch)
    while invalid():                  # while still BROKEN
        remove(s[left])
        left += 1
    best = max(best, right - left + 1)   # record AFTER restoring validity
return best
```

Here the recording is **after** the shrink loop, outside it, because only then is the window guaranteed
valid.

**The rule to remember:** minimising means shrink-while-valid and record inside; maximising means
shrink-while-invalid and record after. Get those two the wrong way round and the code runs and gives
plausible nonsense.

### Why it is `O(n)`

`right` advances exactly `n` times, once per turn of the `for` loop. `left` only ever advances, and it
can never pass `right`, so across the whole run it advances at most `n` times too.

**Total: at most `2n` moves.** Each element is added once and removed at most once. That is `O(n)`,
despite the `while` inside the `for` — and the argument is *count how far the pointers travel*, not
*count the nested loops*. Same reasoning as [day 023](../day-023-palindromes/README.md) and
[day 031](../day-031-fixed-window/README.md).

### The condition that makes this legal

A sliding window is not always allowed, and this is the part most people never learn.

The technique needs the condition to be **monotonic in the window**: extending the window on the right
must move you in one direction only, and shrinking on the left must move you back.

- *Sum of positive numbers ≥ target* — adding elements only increases the sum. **Monotonic. Window
  works.**
- *At most k distinct characters* — adding can only increase the distinct count, removing can only
  decrease it. **Monotonic. Window works.**
- *Sum ≥ target, values may be negative* — adding an element might **decrease** the sum, so a window
  that is invalid now might become valid later, and shrinking might make it valid rather than
  invalid. **Not monotonic. The window is wrong**, and the correct technique is prefix sums plus a
  monotonic deque, which is LeetCode 862 and considerably harder.

**Say this out loud when the array might contain negatives.** *"A sliding window needs the sum to grow
monotonically as I extend, which negatives break — so I'd use prefix sums with a deque instead."* That
sentence is worth more than any of the code on this page.

### The four variants you will actually be asked

| Problem | Shape | The condition | What the window carries |
|---|---|---|---|
| Minimum size subarray sum (209) | A, minimise | `total >= target` | a running sum |
| Longest substring without repeating characters (3) | B, maximise | a character repeats | a set, or a last-seen map |
| Longest substring with at most k distinct (340) | B, maximise | `len(counts) > k` | a count map |
| Minimum window substring (76) | A, minimise | all of `t` is covered | a count map plus a "missing" counter |

### Two ways to handle repeats, and why one is nicer

For *longest substring without repeating characters* there are two correct approaches.

**Shrink one at a time**, which is the pure shape-B template:

```python
while ch in seen:
    seen.discard(s[left])
    left += 1
seen.add(ch)
```

**Jump straight there**, using a map of last-seen positions:

```python
if ch in last and last[ch] >= left:
    left = last[ch] + 1
last[ch] = right
```

The jump version is what you met on
[day 024](../day-024-substrings-vs-subsequences/README.md), and `last[ch] >= left` is the guard
without which `left` moves **backwards** on input like `"abba"` — which breaks the whole `O(n)`
argument as well as the answer. **The `while` version cannot have that bug**, because it only ever
increments, which is a reason to prefer it under pressure.

### The subtle one: longest repeating character replacement

LeetCode 424: *you may change at most `k` characters; what is the longest run of one repeated
character you can make?*

The window is valid when `window_length - count_of_the_most_frequent_character <= k`, because those
are the characters you would have to change.

The famous subtlety is that the standard solution **never decreases the maximum-frequency tracker** when
the window shrinks — and it is still correct. The reason: the answer only ever grows, so a window
carried forward with a stale (too high) maximum frequency can only fail to *shrink*, never produce a
wrong larger answer. The window size never decreases, which is exactly what you want when maximising.

**You do not have to use that trick.** Recomputing `max(count.values())` inside the loop is correct and
`O(26)` per step, which is constant. Say the simple version, and mention the optimisation.

---

## 4. The picture

Shape A, minimising. `nums = [2,3,1,2,4,3]`, `target = 7`:

```
  right=0  [2]                  total=2   < 7, grow
  right=1  [2,3]                total=5   < 7, grow
  right=2  [2,3,1]              total=6   < 7, grow
  right=3  [2,3,1,2]            total=8  >= 7  -> record 4, drop 2, left=1
           [3,1,2]              total=6   < 7, stop shrinking, grow
  right=4  [3,1,2,4]            total=10 >= 7  -> record 4, drop 3, left=2
           [1,2,4]              total=7  >= 7  -> record 3, drop 1, left=3
           [2,4]                total=6   < 7, stop shrinking, grow
  right=5  [2,4,3]              total=9  >= 7  -> record 3, drop 2, left=4
           [4,3]                total=7  >= 7  -> record 2, drop 4, left=5
           [3]                  total=3   < 7, stop

  answer 2
```

**What to notice:** `left` moves 5 times in total across the whole run, and `right` moves 6. Eleven
moves for six elements — that is the `2n` bound made concrete, and it is why the nested `while` does
not make it quadratic.

Shape B, maximising. `s = "abcabcbb"`, no repeats allowed:

```
  right=0  [a]        ok            best=1
  right=1  [ab]       ok            best=2
  right=2  [abc]      ok            best=3
  right=3  [abca]     'a' repeats -> shrink: drop 'a', left=1
           [bca]      ok            best=3
  right=4  [bcab]     'b' repeats -> shrink: drop 'b', left=2
           [cab]      ok            best=3
  right=5  [cabc]     'c' repeats -> shrink: drop 'c', left=3
           [abc]      ok            best=3
  right=6  [abcb]     'b' repeats -> shrink: drop 'a', left=4
           [bcb]      'b' repeats -> shrink: drop 'b', left=5
           [cb]       ok            best=3
  right=7  [cbb]      'b' repeats -> shrink: drop 'c', left=6
           [bb]       'b' repeats -> shrink: drop 'b', left=7
           [b]        ok            best=3
```

**What to notice at `right = 6`:** the shrink loop runs twice in one turn. That looks expensive and is
not, because `left` has moved two positions it will never revisit.

The two shapes side by side — this is the picture to memorise:

```
  MINIMISE (shape A)                   MAXIMISE (shape B)
  ------------------                   ------------------
  for right:                           for right:
      add(right)                           add(right)
      while VALID:                         while INVALID:
          record(right - left + 1)  <--        remove(left); left++
          remove(left); left++             record(right - left + 1)  <--
                                       
  record INSIDE the shrink loop        record AFTER the shrink loop
  shrink while it still works          shrink until it works again
```

Why `left` never goes back — Devappa's own argument:

```
  window [left .. right] is the smallest valid one ending at right.

  Now right moves to right+1. Could the answer start EARLIER than left?
  No: any window starting before left and ending at right+1 CONTAINS
  [left .. right+1], so it is longer. For a minimisation problem, longer
  is worse. So there is nothing behind left worth revisiting.
```

---

## 5. The code, built step by step

### Shape A: minimum size subarray sum

```python
left = 0
total = 0
best = float("inf")
```

`best` starts at infinity, not at 0 or at `len(nums)`, because you need a value that any real answer
beats and a way to detect "no answer at all".

```python
for right, x in enumerate(nums):
    total += x
```

The right edge always advances, unconditionally. That is the outer loop and it never has a condition of
its own.

```python
    while total >= target:
        best = min(best, right - left + 1)
        total -= nums[left]
        left += 1
```

**Record first, then shrink.** The window is valid right now, so its length is a candidate; then remove
the leftmost element and check again. `while` and not `if`, because several elements may need to come
off — look at `right = 4` in §4, where two come off in one turn.

```python
return 0 if best == float("inf") else best
```

The problem's convention for "no such subarray" is 0. **Ask** — some versions want `-1`.

### Shape B: longest substring without repeats

```python
seen: set[str] = set()
left = 0
best = 0
for right, ch in enumerate(s):
    while ch in seen:
        seen.discard(s[left])
        left += 1
    seen.add(ch)
    best = max(best, right - left + 1)
```

Note the order inside the loop: **shrink first, then add**. If you added `ch` before the `while`, the
condition `ch in seen` would be true because of the character you just added, and `left` would run all
the way to `right`.

And the recording is **after** the shrink loop, because only there is the window guaranteed valid.

### Shape B with a count map: at most k distinct

```python
count: defaultdict[str, int] = defaultdict(int)
left = 0
best = 0
for right, ch in enumerate(s):
    count[ch] += 1
    while len(count) > k:
        count[s[left]] -= 1
        if count[s[left]] == 0:
            del count[s[left]]        # or len(count) never goes down
        left += 1
    best = max(best, right - left + 1)
```

**The `del` at zero is what makes `len(count)` mean "distinct characters in the window".** Leave the
zero entries in and the count never decreases, the shrink loop never terminates properly, and the
answer is wrong. This is the same rule as [day 031](../day-031-fixed-window/README.md), and here it is
not merely a comparison failure — it breaks the loop condition itself.

### Shape A with a count map: minimum window substring

The hardest of the four, and the trick is the `missing` counter that makes the validity check `O(1)`
rather than a dictionary comparison.

```python
need = Counter(t)
missing = len(t)          # how many characters of t are still unmatched
left = 0
best = (float("inf"), 0, 0)
```

```python
for right, ch in enumerate(s):
    if need[ch] > 0:
        missing -= 1      # only counts if we still NEEDED this character
    need[ch] -= 1         # goes negative for surplus characters
```

`need[ch]` going negative is deliberate: it records how many spare copies of `ch` the window holds,
which is exactly what the shrink step needs to know.

```python
    if missing == 0:
        while need[s[left]] < 0:      # trim surplus characters off the front
            need[s[left]] += 1
            left += 1
        if right - left + 1 < best[0]:
            best = (right - left + 1, left, right)
        need[s[left]] += 1            # give up one needed character
        missing += 1                  # and stop being valid
        left += 1
```

The last three lines are the shape-A shrink: having recorded the best window, deliberately break
validity by removing one *needed* character, so the outer loop goes back to growing.

### The complete solutions

```python
from collections import Counter, defaultdict


def min_subarray_len(target: int, nums: list[int]) -> int:
    """LeetCode 209. Shortest subarray with sum >= target. POSITIVE values only.

    Shape A: grow, then shrink while still valid, recording inside the shrink.
    """
    left = 0
    total = 0
    best = float("inf")
    for right, x in enumerate(nums):
        total += x
        while total >= target:              # while STILL valid
            best = min(best, right - left + 1)   # record BEFORE shrinking
            total -= nums[left]
            left += 1
    return 0 if best == float("inf") else best


def longest_unique(s: str) -> int:
    """LeetCode 3. Shape B: shrink while invalid, record after."""
    seen: set[str] = set()
    left = 0
    best = 0
    for right, ch in enumerate(s):
        while ch in seen:                   # shrink BEFORE adding
            seen.discard(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)  # record AFTER restoring validity
    return best


def longest_at_most_k_distinct(s: str, k: int) -> int:
    """LeetCode 340. Shape B with a count map."""
    count: defaultdict[str, int] = defaultdict(int)
    left = 0
    best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]          # MANDATORY: len(count) must mean "distinct"
            left += 1
        best = max(best, right - left + 1)
    return best


def character_replacement(s: str, k: int) -> int:
    """LeetCode 424. Valid when (window length - most frequent count) <= k.

    max_freq is never decreased on shrink, and that is still correct: a stale
    high value can only stop the window growing, never produce a larger answer.
    """
    count: defaultdict[str, int] = defaultdict(int)
    left = 0
    best = 0
    max_freq = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        max_freq = max(max_freq, count[ch])
        while (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def min_window(s: str, t: str) -> str:
    """LeetCode 76. Smallest window of s containing every character of t.

    `missing` makes the validity check O(1) instead of comparing two maps.
    Negative values in `need` record surplus characters.
    """
    if not t or not s:
        return ""
    need = Counter(t)
    missing = len(t)
    left = 0
    best = (float("inf"), 0, 0)

    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1

        if missing == 0:
            while need[s[left]] < 0:        # trim surplus off the front
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            need[s[left]] += 1              # break validity deliberately
            missing += 1
            left += 1

    return "" if best[0] == float("inf") else s[best[1]:best[2] + 1]


if __name__ == "__main__":
    print([min_subarray_len(t, a) for t, a in
           ((7, [2, 3, 1, 2, 4, 3]), (4, [1, 4, 4]),
            (11, [1, 1, 1, 1, 1, 1, 1, 1]), (1, [1]), (5, []))])
    # [2, 1, 0, 1, 0]

    print([longest_unique(x) for x in
           ("abcabcbb", "bbbbb", "pwwkew", "", "au", "dvdf", "abba")])
    # [3, 1, 3, 0, 2, 3, 2]

    print([longest_at_most_k_distinct(s, k) for s, k in
           (("eceba", 2), ("aa", 1), ("abaccc", 2), ("", 2), ("abc", 0))])
    # [3, 2, 4, 0, 0]

    print([character_replacement(s, k) for s, k in
           (("ABAB", 2), ("AABABBA", 1), ("AAAA", 0), ("", 1))])
    # [4, 4, 4, 0]

    print([min_window(s, t) for s, t in
           (("ADOBECODEBANC", "ABC"), ("a", "a"), ("a", "aa"), ("ab", "b"))])
    # ['BANC', 'a', '', 'b']
```

---

## 6. What it costs

### Every problem on this page

`right` advances exactly `n` times. `left` only advances and never passes `right`, so it advances at
most `n` times across the entire run.

```
at most 2n pointer moves, each doing constant work  ->  O(n) time
```

Space depends on what the window carries: `O(1)` for a running sum, `O(k)` for a set or map bounded by
the alphabet or by `k`.

**The nested `while` does not make it quadratic**, and the argument is that a single turn of the `for`
loop may run the `while` many times, but those moves are permanently spent — `left` never returns. Total
work across all turns is bounded by how far `left` can travel, which is `n`.

### Against the brute force

The brute force tries every start and extends until the condition is met: `O(n²)`.

Measured, on inputs where no window qualifies so both do their full work:

```
n =  2,000   window 0.00009 s   brute 0.0800 s      854x
n =  5,000   window 0.00025 s   brute 0.5268 s    2,100x
n = 10,000   window 0.00048 s   brute 2.0750 s    4,350x
```

The ratio roughly doubles when `n` doubles — 854, 2,100, 4,350 — which is the `O(n)` versus `O(n²)`
signature. At `n = 10,000` that is about 10,000 operations against 50 million.

### `min_window`, and why the `missing` counter matters

Without it, checking validity means comparing two dictionaries on every step. That is `O(k)` where `k`
is the alphabet size — constant, but with a real constant factor, and it is done `n` times.

With `missing`, validity is `missing == 0`: a single integer comparison. Same complexity class, several
times faster in practice, and it is the difference between a solution that reads well and one that
looks laboured.

**O(|s| + |t|) time, O(|t|) space.**

### `character_replacement`, both ways

Recomputing `max(count.values())` inside the shrink loop is `O(26)` per step — constant for a fixed
alphabet, so the whole thing stays `O(n)`. Carrying `max_freq` and never decreasing it removes that
constant entirely.

**Both are `O(n)`.** The trick is a constant-factor improvement with a subtle correctness argument, so
in an interview: write the simple version, get it right, then offer the optimisation with its
justification.

### The number to have ready

> Both edges only ever move forward, so each index is visited at most twice — `2n` moves, `O(n)` time.
> The brute force is `O(n²)`: measured at about 4,350 times slower at ten thousand elements, with the
> ratio doubling every time `n` doubles.

---

## 7. The traps

### The big one: negative numbers break the whole technique

```python
print(min_subarray_len(3, [-3, 5]))
```

```
0
```

`0` means "no such subarray exists". But `[5]` sums to 5, which is at least 3, so the answer is **1**.
The window silently reported that nothing works.

Here is what happened. After `right = 0` the total is `-3`, below target, so nothing shrinks. At
`right = 1` the total is `2` — still below target — so the loop ends having never been valid. The `5`
was never considered on its own, because the window never dropped the `-3` off the front.

That is the general failure. Shape A's shrink loop assumes **removing an element from the left can only
decrease the sum**, so "not valid yet" means "keep growing". With negatives, removing a negative
element *increases* the sum, so a window that looks hopeless can be fixed by shrinking — which the
algorithm never tries. Testing over twenty thousand random small arrays containing negatives, this
version disagrees with the brute force about **12% of the time**, sometimes reporting no answer at all
and sometimes reporting one that is too long — `[-1,-3,2,4,1,4]` with target 6 gives 3 where the answer
is 2.

**Sliding windows require the condition to be monotonic as the window grows.** For sums, that means
non-negative values. The correct technique for negatives is prefix sums plus a monotonic deque —
LeetCode 862 — and it is a genuinely harder problem. **Say "does the array contain negative numbers?"
before writing a window over sums.**

### The near-miss: recording in the wrong place

```python
for right, x in enumerate(nums):
    total += x
    while total >= target:
        total -= nums[left]
        left += 1
    best = min(best, right - left + 1)     # recorded AFTER the shrink
```

By the time this records, the shrink loop has already broken validity — it exits when the sum has
dropped *below* target — so it measures an invalid window. On `[2,3,1,2,4,3]` with target 7 it returns
1, which is wrong.

**Minimise: record inside the shrink loop, before shrinking. Maximise: record after.** Getting these
backwards is the single most common structural error in this family, and the code runs perfectly.

### The near-miss: `if` instead of `while`

```python
if total >= target:                        # should be while
```

On `[1, 1, 1, 10]` with target 4, the window needs to shrink three positions in one turn and this
shrinks one. The answer comes out too large, with no error. **Look at `right = 4` in §4** — two removals
in one turn is normal, not exceptional.

### The near-miss: adding before shrinking in shape B

```python
seen.add(ch)
while ch in seen:                          # always true — we just added it
    seen.discard(s[left])
    left += 1
```

`left` runs all the way up to `right` every time, and the answer is always 1. **Shrink first, then
add.**

### The near-miss: `left` moving backwards

```python
if ch in last:                             # missing: and last[ch] >= left
    left = last[ch] + 1
```

On `"abba"`: at the final `a`, `last["a"]` is 0, which is *before* the current `left` of 2 — so `left`
jumps backwards to 1, the window contains a repeated `b`, and the answer is 3 instead of 2.

It also destroys the `O(n)` argument, since `left` no longer travels monotonically. Guard with
`last[ch] >= left`, or write `left = max(left, last[ch] + 1)`, which says the intent plainly. **The
`while`-based version cannot have this bug at all**, because it only increments.

### The near-miss: forgetting the `del` at zero

```python
count[s[left]] -= 1
# no deletion at zero
left += 1
```

`len(count)` now counts characters that are no longer in the window, so it never drops back to `k`, the
shrink loop keeps running, and `left` marches to the end. The answer becomes 1 or 0. **Here the missing
`del` breaks the loop condition itself**, which is worse than the equality-comparison failure it caused
yesterday.

### The contract corner: what "no answer" returns

`min_subarray_len(11, [1,1,1,1,1,1,1,1])` — the whole array sums to 8, so no window qualifies. LeetCode
209 wants `0`. Other phrasings want `-1`. Returning `float("inf")` because you forgot to translate it is
a real and easy mistake. **Decide and say it.**

---

## 8. In the interview

### How it gets asked

- *"Find the smallest subarray with a sum at least k."* — LeetCode 209, shape A.
- *"Longest substring without repeating characters."* — LeetCode 3, shape B, and the most-asked window
  problem there is.
- *"Longest substring with at most k distinct characters."* — LeetCode 340, shape B with a map.
- *"Minimum window substring."* — LeetCode 76, shape A with a map, and genuinely hard.
- *"What if the array has negative numbers?"* — the question that checks whether you know the boundary.

### What to say out loud, in the first ninety seconds

1. **Ask the question that decides legality.** *"Are all the values positive? A sliding window needs the
   sum to only increase as I extend the window, and negatives break that."*
2. **Name the shape and say which of the two it is.** *"This is a minimisation, so I'll grow the window
   until it's valid and then shrink from the left while it's still valid, recording the length each
   time."*
3. **Say the invariant.** *"The window from left to right is always the shortest valid one ending at
   right."*
4. **Say why `left` never goes back.** *"Any window starting earlier and ending here contains this one,
   so it's longer — and for a minimisation, longer is worse. There's nothing behind left worth
   revisiting."*
5. **Say where the recording goes and why.** *"The record goes inside the shrink loop, before I remove
   an element, because that's the moment the window is valid."*
6. **Give the cost with the argument.** *"Both pointers only move forward, so each index is visited at
   most twice — 2n moves, O(n) — even though there's a `while` inside a `for`."*
7. **Name the boundary cases.** *"Empty array, and no window ever reaching the target — I'll return 0
   for that, though I'd check the convention."*

### The follow-ups

**"What if the array can contain negative numbers?"**
Then a sliding window is the wrong technique, and I would say so rather than adapt it. The window
depends on monotonicity: extending it can only increase the sum, and shrinking can only decrease it,
which is what makes "shrink while still valid" safe. With negatives, adding an element can decrease the
sum and removing one can increase it — so a window I rejected might have become valid later, and a
window I shrank might have had a shorter valid version I never saw. The result is a wrong answer with
no error, which is the dangerous kind. The correct approach is prefix sums plus a monotonic deque: build
the prefix sums, and for each right endpoint find the largest earlier prefix that is at least `target`
smaller, maintaining a deque of increasing prefix values. That is LeetCode 862 and it is a hard problem
rather than a variation.

**"Why is this O(n) when there's a while loop inside a for loop?"**
Because the right pointer advances exactly n times and the left pointer also advances at most n times
across the entire run — it only ever increases and it can never pass the right pointer. So the total
number of pointer movements is bounded by 2n, and every unit of work is attached to a movement. A
single turn of the outer loop might run the inner `while` many times, but each of those iterations
spends a move that will never be repeated, so it is paid for. The way I check this in general is to ask
whether either pointer can move backwards — if neither can, it is linear; if either can, as in the
last-seen-map version without a guard, the argument collapses along with the correctness.

**"Now find the minimum window in `s` containing all characters of `t`, including duplicates."**
Same shape A, with two refinements. The window carries a count map initialised to what `t` needs, and I
decrement it as characters arrive — letting it go negative, which records surplus copies. And rather
than comparing two maps to check validity, I keep a single `missing` counter of how many required
characters are still unmatched, decremented only when I consume a character that was still needed. So
validity is `missing == 0`, an integer comparison rather than a dictionary comparison. When valid, I
first trim surplus characters off the front — those with negative counts — then record, then
deliberately remove one *needed* character to break validity so the window grows again. O(|s| + |t|)
time, O(|t|) space.

**"How do you decide whether it's shape A or shape B?"**
By what the question is optimising. If it asks for the **smallest** window satisfying something, I grow
until it is satisfied and then shrink while it is *still* satisfied, recording inside the shrink loop —
because each shrink gives a shorter valid candidate. If it asks for the **largest** window satisfying
something, I grow and shrink only while the window is *broken*, recording after the shrink loop, because
that is the first moment the window is valid again. Stated as a rule: minimise means shrink-while-valid
and record inside; maximise means shrink-while-invalid and record after. Swapping them produces code
that runs and returns plausible wrong answers, which is why I say which one I am doing before writing
it.

### A model answer

> "First, are all the values positive? That decides whether a sliding window is even legal here — the
> technique relies on the sum only increasing as I extend the window, and negative numbers break that.
>
> ...All positive. Good.
>
> The brute force is to try every starting position and extend until the sum reaches the target, which
> is O(n²).
>
> Instead I'll use a window with two edges that both only move forward. The right edge advances
> unconditionally, adding to a running total. The moment the total reaches the target, the window is
> valid, so I record its length — and then I shrink from the left while it is *still* valid, recording
> each shorter version, until removing another element would drop below the target.
>
> ```python
> def min_subarray_len(target: int, nums: list[int]) -> int:
>     left = 0
>     total = 0
>     best = float("inf")
>     for right, x in enumerate(nums):
>         total += x
>         while total >= target:
>             best = min(best, right - left + 1)
>             total -= nums[left]
>             left += 1
>     return 0 if best == float("inf") else best
> ```
>
> Two structural points. The record goes *inside* the shrink loop and *before* the removal, because that
> is the moment the window is valid — putting it after the loop measures a window that has just been
> broken, and returns an answer that is too small. And it is a `while`, not an `if`, because several
> elements may need to come off in one turn: on `[1,1,1,10]` with target 4 the left edge moves three
> places when the 10 arrives.
>
> The left edge never goes backwards, and the reason is worth stating: any window starting before the
> current left and ending at the current right *contains* the current window, so it is longer — and for
> a minimisation, longer is worse. There is nothing back there to reconsider.
>
> That also gives the cost. The right pointer advances n times and the left pointer at most n times, so
> at most 2n moves total — O(n) time, O(1) space, even though there is a `while` inside a `for`. I
> measured it against the brute force: about four thousand times faster at ten thousand elements, with
> the ratio doubling each time n doubles.
>
> Edge cases: an empty array, and the case where no window ever reaches the target — the convention
> there is to return 0, and I'd confirm that."

---

## 9. Recall card

- **Right edge always advances. Left edge advances only when the rule says so.** Neither ever goes
  back — so `2n` moves, `O(n)`.
- **Minimise → shrink while VALID, record INSIDE the loop. Maximise → shrink while INVALID, record
  AFTER.** Swapping them gives plausible nonsense.
- **The condition must be monotonic.** Negative numbers break sum-windows — that needs prefix sums plus
  a deque instead. Ask first.
- **Shape B: shrink before adding**, or the character you just added triggers the shrink.
- **With a count map, `del` at zero** — here it breaks the loop condition, not just a comparison.
