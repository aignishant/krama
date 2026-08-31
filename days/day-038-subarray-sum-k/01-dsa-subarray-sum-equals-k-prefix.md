---
day: 38
track: dsa
title: "Subarray sum equals K: prefix plus hash map"
phase: "Prefix sums"
status: written
---

# Day 038 · DSA — Subarray sum equals K: prefix plus hash map

**After today you can:** You can count subarrays with a given sum in one pass, including the negative-number case.

**The interviewer asks it as:** *Count the subarrays whose sum equals k.*

---

## 1. What this is, and why they ask it

Count the subarrays that sum to exactly `k`, in one pass, on an array that may contain negative
numbers. The tool is yesterday's running total plus
[day 021](../day-021-frequency-maps/README.md)'s frequency map: walk the array carrying the prefix
sum, and at each step ask the map *how many earlier prefixes equal this one minus k* — because each
such earlier moment marks the start of a subarray ending here with sum exactly `k`.

This is LeetCode 560, one of the most-asked mediums at product companies, and it is asked as a
**trap with a pedigree**. The problem looks exactly like the window problems of days 32 to 34 — and
windows are illegal here, because negatives destroy monotonicity, the debt
[day 032](../day-032-variable-window/README.md) recorded and [day 034](../day-034-at-most-k/README.md)
renewed. Interviewers watch for one specific moment: do you ask about negative numbers before
choosing the tool? Today pays that debt, and the same three-line pattern then solves a whole family
— equal 0s and 1s, sums divisible by k, and their cousins.

---

## 2. The story

Deepa's bank app shows two columns: each credit or debit, and next to it the balance after it. She
scrolls it the way other people scroll photos — month-end discipline, she calls it.

Her brother started it, with an accusation. Somewhere in March, he said, that badminton kit plus
the shoes plus whatever else — you dropped exactly five thousand in one stretch, I am sure of it.
Find the stretch.

The obvious way is miserable. Pick a starting entry, add every amount from there forward, see if
any stopping point gives five thousand, move the start one down, do it again. Forty entries in
March. She tried it for two starts and gave up.

Then she stopped looking at the amounts column and looked only at the balances. If some stretch of
entries cost exactly five thousand net, then the balance at the end of that stretch is exactly five
thousand less than the balance just before it began. That is not clever, she thought — that is just
what a balance is.

So the question flips. Standing at any entry, balance showing 41,200, she does not add anything.
She asks: **was there an earlier moment when the balance showed 46,200?** If yes — there is her
stretch, ending right here. If the balance showed 46,200 at *three* earlier moments, that is three
different stretches, all ending here, all costing exactly five thousand.

And the three-moments case is real, not a technicality — her balance climbs on payday and falls all
month, so the same figure comes around again and again. Money goes up and down; that is exactly why
the same balance repeats, and exactly why she counts moments rather than remembering one.

One scroll, top to bottom. At each entry she asks her one question about the balances she has
already passed, keeps a rough tally of how often each balance has appeared, and moves on. By the
bottom of March she had found it — two stretches, actually, which cost her brother an apology and
her a coffee.

The first moment she almost missed: a stretch that starts at the very top of the month. Its
"balance just before" is the balance March *opened* with — a moment with no entry attached. She had
to remember the opening balance counted too.

---

## 3. The idea in plain English

Deepa's balance column is yesterday's prefix sum. Her one question — *how often has
balance-minus-5000 appeared before?* — is the whole algorithm. And her opening balance is the
sentinel again, wearing new clothes.

### The flip

Yesterday established: sum of `nums[i..j]` = `prefix[j + 1] - prefix[i]` — after the end minus
before the start. So a subarray ending at position `j` sums to `k` exactly when

```
prefix_before_its_start  =  prefix_here - k
```

Walk left to right carrying `running`, the prefix so far. At each element, the subarrays that end
here and sum to `k` correspond **one for one** with the earlier moments whose prefix equalled
`running - k`. Do not search for them — that is Deepa adding from every start. **Count them as you
go**: keep a map from prefix value to how many times it has occurred, ask the map, then record the
current prefix.

```python
count += seen[running - k]     # how many valid starts end a subarray here
seen[running] += 1             # this moment is a future "earlier moment"
```

The order matters and §7 has the input that punishes getting it wrong: ask first, record after,
or a subarray of length zero sneaks in when `k = 0`.

### The opening balance: `seen[0] = 1`

A subarray that starts at index 0 has "the prefix before its start" equal to 0 — the sum of
nothing, yesterday's sentinel. That moment happened — before the walk began — so the map starts as
`{0: 1}`, not empty. Forget it and every subarray touching the left edge goes uncounted: on
`[1, 2, 3]` with `k = 3` you get 1 instead of 2, silently missing `[1, 2]`. This is the
single most common bug in this problem, and it is Deepa's opening balance, exactly.

### Why this beats the window — and when the window is still better

Negatives are no problem here, because nothing is assumed about direction: the map does not care
whether prefixes climb or fall, it only counts what appeared, and Deepa's balance falling and
rising is why the same value repeats and why occurrences are *counted*, not just remembered.

But say the comparison properly, because it is a favourite follow-up. With all-positive values and
a question like "longest at most k", the window is still the better tool — `O(1)` space against the
map's `O(n)`. The map earns its space exactly when **negatives** are possible or the question is
**exactly** — the two places monotonicity fails. This is [day 035](../day-035-choosing-the-pattern/README.md)'s
routing question 4 getting its full answer.

### The same trick in costumes

Two transformations turn famous problems into this one:

**Contiguous Array** — LeetCode 525: longest subarray with equal 0s and 1s. Recast each 0 as −1;
now "equal 0s and 1s" means **sum zero**. Because it asks *longest*, not *how many*, the map stores
each prefix's **first** index instead of a count — the earliest occurrence gives the longest
stretch — and is never overwritten.

**Subarrays Divisible by K** — LeetCode 974: count subarrays whose sum is divisible by `k`. A
stretch is divisible by `k` when the prefixes at its two ends leave the **same remainder** — so
carry `running % k` and count matching remainders. Python's `%` always returns a non-negative
remainder for positive `k` (`-7 % 5 == 3`), so negatives cost nothing here; in Java or C++ the
remainder keeps the sign and needs `(r % k + k) % k` — worth one sentence if the interview is not
in Python.

One pattern, three problems: **carry a running quantity, and ask a map about the past.** What
varies is the quantity (sum, recast sum, remainder) and what the map stores (count, or first
index).

---

## 4. The picture

The one-pass count on `[3, 4, 7, 2, -3, 1, 4, 2]`, `k = 7` — answer 4:

```
 index      0     1     2     3     4     5     6     7
          +-----+-----+-----+-----+-----+-----+-----+-----+
 nums     |  3  |  4  |  7  |  2  | -3  |  1  |  4  |  2  |
          +-----+-----+-----+-----+-----+-----+-----+-----+

 step  running  ask seen[running-7]        found          seen afterwards
 ----  -------  --------------------       ------------   -------------------------
 (start)                                                  {0:1}
   0      3     seen[-4] = 0                              {0:1, 3:1}
   1      7     seen[0]  = 1   [3,4]       1st            {0:1, 3:1, 7:1}
   2     14     seen[7]  = 1   [7]         2nd            {..., 14:1}
   3     16     seen[9]  = 0                              {..., 16:1}
   4     13     seen[6]  = 0                              {..., 13:1}
   5     14     seen[7]  = 1   [2,-3,1,4]… no: [7,2,-3,1] 3rd   {..., 14:2}
   6     18     seen[11] = 0                              {..., 18:1}
   7     20     seen[13] = 1   [-3,1,4,2]… no: [1,4,2]…   4th   {..., 20:1}
```

**What to notice, three things.** The very first hit uses the `{0: 1}` sentinel — subarray `[3, 4]`
starts at the left edge. At step 5, `running` returns to 14 — the negative at index 4 pulled it back
down — and the map now holds `14: 2`: revisited values are why occurrences are counted. And the
negative number caused no special handling anywhere.

Same balance, two moments — the picture of why counting matters:

```
 running:  3    7    14    16    13    14    18    20
                      ^                ^
                      +--- same value --+
                      the stretch between sums to 0 —
                      and BOTH moments serve as valid starts
                      for later subarrays summing to k
```

**What to notice:** a repeated prefix value means some stretch in between summed to zero — only
possible with negatives, and exactly the case windows cannot navigate.

---

## 5. The code, built step by step

### The core

```python
seen: defaultdict[int, int] = defaultdict(int)
seen[0] = 1                     # the opening balance: prefix before index 0
running = 0
count = 0
```

Four names. `seen[0] = 1` is the line that separates this from a wrong answer on day one.

```python
for x in nums:
    running += x
    count += seen[running - k]      # ask about the past first
    seen[running] += 1              # then file the present
```

Three lines of loop. `seen[running - k]` on a `defaultdict` returns 0 for never-seen values —
harmless here, and the read-creates-key quirk from [day 021](../day-021-frequency-maps/README.md)
does not bite because inserting `running - k` with count 0 never changes a future answer. (With a
plain dict you would write `seen.get(running - k, 0)` — §7 shows the crash if you forget.)

### Contiguous array: first index, not count

```python
first: dict[int, int] = {0: -1}     # sum 0 exists before index 0
running = 0
best = 0
for i, x in enumerate(nums):
    running += 1 if x == 1 else -1
    if running in first:
        best = max(best, i - first[running])
    else:
        first[running] = i          # only the FIRST occurrence — never overwrite
```

Two changes, both forced by "longest": the map stores the earliest index of each prefix value
(`{0: -1}` is the sentinel in index form — the moment before index 0), and an existing entry is
**never overwritten**, because a later duplicate could only shorten the stretch. §7 shows the
overwriting version producing a confident wrong answer.

### Divisible by k: remainders

```python
seen: defaultdict[int, int] = defaultdict(int)
seen[0] = 1
running = 0
count = 0
for x in nums:
    running = (running + x) % k
    count += seen[running]          # same remainder = divisible stretch between
    seen[running] += 1
```

The ask changes from `seen[running - k]` to `seen[running]` — equal remainders, rather than a fixed
difference. Everything else is the same machine.

### The complete solutions

```python
from collections import defaultdict


def subarray_sum(nums: list[int], k: int) -> int:
    """LeetCode 560. Count subarrays summing to k; negatives welcome."""
    seen: defaultdict[int, int] = defaultdict(int)
    seen[0] = 1                          # prefix 0 exists before the walk starts
    running = 0
    count = 0
    for x in nums:
        running += x
        count += seen[running - k]       # ask first...
        seen[running] += 1               # ...record after (k = 0 depends on this)
    return count


def find_max_length(nums: list[int]) -> int:
    """LeetCode 525. Longest subarray with equal 0s and 1s: recast 0 as -1,
    then longest stretch with sum 0 — map stores FIRST index of each prefix."""
    first: dict[int, int] = {0: -1}
    running = 0
    best = 0
    for i, x in enumerate(nums):
        running += 1 if x == 1 else -1
        if running in first:
            best = max(best, i - first[running])
        else:
            first[running] = i           # never overwrite: earliest = longest
    return best


def subarrays_div_by_k(nums: list[int], k: int) -> int:
    """LeetCode 974. Same remainder at both ends = divisible stretch between.
    Python's % is already non-negative for k > 0."""
    seen: defaultdict[int, int] = defaultdict(int)
    seen[0] = 1
    running = 0
    count = 0
    for x in nums:
        running = (running + x) % k
        count += seen[running]
        seen[running] += 1
    return count


if __name__ == "__main__":
    print(subarray_sum([1, 1, 1], 2))                  # 2
    print(subarray_sum([1, 2, 3], 3))                  # 2
    print(subarray_sum([1, -1, 1, 1], 2))              # 2 — needs the negatives
    print(subarray_sum([-1, -1, 1], 0))                # 1
    print(subarray_sum([3, 4, 7, 2, -3, 1, 4, 2], 7))  # 4 — the walk in §4

    print(find_max_length([0, 1]))                     # 2
    print(find_max_length([0, 1, 0]))                  # 2
    print(find_max_length([0, 0, 1, 0, 0, 0, 1, 1]))   # 6

    print(subarrays_div_by_k([4, 5, 0, -2, -3, 1], 5)) # 7
    print(subarrays_div_by_k([5], 9))                  # 0
```

---

## 6. What it costs

### The count, out loud

One loop over `n` elements. Each iteration: one addition, one map read, one map write — all `O(1)`
on average, [day 021](../day-021-frequency-maps/README.md)'s deal. **O(n) time.** The map holds at
most one entry per distinct prefix value — up to `n + 1` of them. **O(n) extra space.**

### Against the alternatives

```
n = 20,000, k = 0, worst case:

all starts × all ends, summing each stretch afresh : ~n³/6  ≈ 1.3 × 10¹²  ops
all starts × all ends, running sum per start       : ~n²/2  ≈ 2 × 10⁸     ops
prefix + map                                       : ~3n    ≈ 6 × 10⁴     ops
```

The `O(n²)` version is the one interviewers actually see written — it passes small tests and dies
on large ones. Name it as the honest brute force, then leave it.

### The space is the price of the negatives

Yesterday's window solved its problems in `O(1)` space; today costs `O(n)`. That is not
carelessness — it is the exact price of dropping monotonicity. When values can go both ways, any
earlier moment might matter, so some record of *all* of them must be kept. **Say the trade in the
interview:** windows when monotonic and `O(1)` space matters; prefix-plus-map when negatives or
"exactly" appear, at `O(n)` space.

### The number to have ready

> One pass, constant map work per element: O(n) time, O(n) space for the prefix counts. The
> running-sum brute force is O(n²) — two hundred million operations at twenty thousand elements
> against sixty thousand.

---

## 7. The traps

### The near-miss: the missing opening balance

Start the map empty instead of `{0: 1}`:

```python
seen = defaultdict(int)          # no seen[0] = 1
...
print(subarray_sum_noinit([1, 2, 3], 3))
```

```
1
```

The answer is 2: `[1, 2]` and `[3]`. The version without the sentinel finds only `[3]` — every
subarray starting at index 0 needs an "earlier moment with prefix 0", and that moment was never
filed. Wrong by a little, on most inputs, with no error: the worst kind. **`seen[0] = 1` is the
first line after the imports, every time.**

### The real error: `get` forgotten on a plain dict

Swap the `defaultdict` for a plain dict and keep the bracket read:

```python
seen = {0: 1}
...
count += seen[running - k]
```

```
Traceback (most recent call last):
  File "day38.py", line 8, in <module>
    count += seen[running - k]
             ~~~~^^^^^^^^^^^^^
KeyError: -1
```

First element 1, `k = 2`, and `seen[-1]` has never been filed. With a plain dict the read must be
`seen.get(running - k, 0)`. Either spelling is fine in an interview — mixing them is not.

### The near-miss: recording before asking

Swap the two loop lines and run `k = 0`:

```python
seen[running] += 1               # record first — wrong order
count += seen[running - k]       # k = 0: this now counts the CURRENT moment
```

With `k = 0`, `seen[running - 0]` includes the entry you just filed — the empty subarray from this
moment to itself — and every position overcounts by one. On `[-1, -1, 1]` with `k = 0` it answers 4
instead of 1. **Ask about the past, then file the present.** The order encodes "earlier moment",
and `k = 0` is the input that checks you meant it.

### The near-miss: overwriting the first index in Contiguous Array

```python
if running in first:
    best = max(best, i - first[running])
first[running] = i               # overwrites every time
```

```
4
```

On `[0, 0, 1, 0, 0, 0, 1, 1]` the true answer is 6; the overwriting version says 4. Each overwrite
drags the stored index rightward, shortening every stretch measured against it. For *counting*
problems you add occurrences; for *longest* problems you keep the *first* index untouched. Which
map you are keeping — count or first-index — is a sentence to say before coding, because the two
bodies differ by one line and answer different questions.

### The misroute, formally retired

The window version of this problem — grow right, shrink left while the sum exceeds `k` — returns
plausible answers on all-positive tests and wrong ones the moment a negative appears: shrinking can
*raise* the sum, so the shrink loop discards subarrays it never examined.
[Day 032](../day-032-variable-window/README.md) showed the failure; today names the resolution.
**"Can values be negative?" is the first question this problem statement should trigger** — asked
aloud, before any tool is chosen. If no: windows remain legal and cheaper for at-most/longest
forms. If yes, or if the word is "exactly": today's map.

### The contract corner: `k = 0` and empty subarrays

Two clarifications worth fifteen seconds: do empty subarrays count (universally no, and the
ask-then-record order enforces it), and can `k` be negative (yes — nothing in the machine cares,
`seen[running - k]` is just a different lookup). Saying the second unprompted signals the machine
is understood, not memorised.

---

## 8. In the interview

### How it gets asked

- *"Count the subarrays whose sum equals k."* — LeetCode 560, verbatim.
- *"Longest subarray with equal numbers of 0s and 1s."* — LeetCode 525; the recast-and-sum-zero
  costume.
- *"Count the subarrays whose sum is divisible by k."* — LeetCode 974; the remainder costume.
- *"Is there a subarray summing to k?"* — the existence version: same machine, return on first hit.
- And the escalation path: you solve a window problem, and the interviewer adds *"now the values
  can be negative"* — the sentence that hands over from days 32–34 to today.

### What to say out loud, in the first ninety seconds

1. **Ask the routing question.** *"Can the values be negative?"* — and say why: *"negatives break
   the sliding window's monotonicity, so they decide my tool."*
2. **Name the brute force honestly.** *"Every start with a running sum is O(n²) — correct, and too
   slow at scale."*
3. **State the flip.** *"A subarray ending here sums to k exactly when some earlier prefix equals
   the current prefix minus k — so I count earlier prefixes with a frequency map instead of
   re-summing."*
4. **Flag the two load-bearing details.** *"The map starts as {0: 1} — the prefix before the array
   — or I miss every subarray touching the left edge. And I ask the map before recording the
   current prefix, or k = 0 counts empty subarrays."*
5. **Give the costs, both sides.** *"O(n) time, O(n) space — the space is the price of negatives;
   with all-positive values and an at-most question I'd be back to an O(1)-space window."*

### The follow-ups

**"Why exactly does the sliding window fail here?"**
The window's shrink logic is licensed by monotonicity: growing the window must push the sum one way
and shrinking must push it the other, so that "too big" is a state shrinking always repairs and
never overshoots reversibly. With negatives, both directions are broken — extending the window can
shrink the sum, and shrinking it can grow the sum — so when the window discards a start position,
it has not *proven* anything about that start: a later extension might have brought the sum back to
k. Concretely, on `[1, -1, 1, 1]` with k = 2, a window that shrinks past index 0 on seeing the sum
reach 2 throws away the start of `[1, -1, 1, 1]`, which also sums to 2. The map version never
discards: every prefix stays counted forever, which is exactly why it costs O(n) space — the fair
price of making no directional assumption at all.

**"Now make it the *longest* subarray with sum k, not the count."**
Same machine, different map contract. I still walk with the running prefix and still ask about
`running - k`, but the map now stores the **first index** at which each prefix value occurred,
because for length I want the match that is furthest left: `best = max(best, i - first[running - k])`
when present. Two details change with it. The sentinel becomes `{0: -1}` — index form, the moment
before the array — so a stretch from the very start measures correctly as `i - (-1) = i + 1`. And I
never overwrite an existing entry: a later occurrence of the same prefix could only produce shorter
stretches, so the earliest one is the only one worth keeping. That is exactly Contiguous Array —
LeetCode 525 — after recasting 0s as −1s; count-maps for "how many", first-index-maps for
"longest", and saying which contract the map carries is the difference between the two problems.

**"What if the array is enormous — streaming, can't hold it in memory?"**
The algorithm is already one forward pass that never revisits elements, so it runs on a stream
as-is: I keep the running sum and the map, and each arriving value costs O(1). What grows is the
map — one entry per distinct prefix value, unbounded in general. Whether that is a problem depends
on structure I would ask about: if values are integers in a modest range, prefix values are bounded
and so is the map; for the divisible-by-k variant the map is at most k entries — O(k), fully
streaming-safe; for arbitrary values, an adversarial stream makes every prefix distinct and the map
grows linearly, and no exact algorithm can avoid that, because any forgotten prefix could be the
partner of a future element. So: time is stream-friendly, space is the honest constraint, and the
divisible variant is the one that streams perfectly.

### A model answer

> "First question: can the values be negative? ...Yes — then a sliding window is off the table,
> because shrinking no longer reliably reduces the sum, and I'd be discarding starts I've proven
> nothing about. I'll use prefix sums with a frequency map instead.
>
> The idea: the sum of a subarray is the prefix at its end minus the prefix before its start. So a
> subarray ending at the current position sums to k exactly when some earlier prefix equals my
> current prefix minus k. Instead of searching for those, I count them as I walk — a map from
> prefix value to how many times it has occurred.
>
> ```python
> def subarray_sum(nums, k):
>     seen = defaultdict(int)
>     seen[0] = 1
>     running = count = 0
>     for x in nums:
>         running += x
>         count += seen[running - k]
>         seen[running] += 1
>     return count
> ```
>
> Two lines carry the correctness. `seen[0] = 1` — the prefix before the array exists, or every
> subarray starting at index 0 goes missing; on [1,2,3] with k = 3 the answer drops from 2 to 1.
> And I ask the map *before* recording the current prefix — otherwise k = 0 counts each position's
> empty subarray.
>
> Cost: one pass, O(1) map work per element — O(n) time, O(n) space. The space is the honest price
> of negatives: since sums can come back down, any earlier moment may matter, so all of them stay
> counted. With all-positive values and an at-most question I'd use the O(1)-space window instead.
>
> And the pattern generalises: recast 0s as −1s and 'equal 0s and 1s' becomes sum zero; carry the
> remainder instead of the sum and 'divisible by k' becomes matching remainders. Same machine,
> different quantity."

---

## 9. Recall card

- **A subarray ending here sums to k ⇔ some earlier prefix equals `running - k`.** Count earlier
  prefixes with a map; never re-sum.
- **`seen[0] = 1` first, always** — the prefix before the array. Without it, every left-edge
  subarray is silently missed.
- **Ask, then record.** `count += seen[running - k]` before `seen[running] += 1` — `k = 0` is the
  input that checks the order.
- **Count-map for "how many"; first-index map (never overwritten, sentinel `{0: -1}`) for
  "longest".** Recast 0→−1 gives equal-0s-and-1s; remainders give divisible-by-k.
- **O(n) time, O(n) space — the space is the price of negatives.** All positive + at-most →
  yesterday's O(1) window instead. Ask "can values be negative?" before choosing.
