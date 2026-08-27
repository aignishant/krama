---
day: 33
track: dsa
title: "Window plus hash map: the longest-substring family"
phase: "Two pointers and sliding window"
status: written
---

# Day 033 · DSA — Window plus hash map: the longest-substring family

**After today you can:** You can solve longest substring without repeating characters and its five cousins.

**The interviewer asks it as:** *Find the length of the longest substring without repeating characters.*

---

## 1. What this is, and why they ask it

Yesterday's window carried a running **sum**. Today it carries a **map** — a count of what is inside it
— and that single change unlocks the largest family of window problems there is.

The map answers questions a sum cannot:

- **How many distinct things are in the window?** `len(count)`.
- **How many of this particular thing?** `count[x]`.
- **What is the most frequent thing?** the largest value.
- **Does the window contain everything I need?** compare against a required map.

Every problem below is the same eight-line skeleton with one of those four questions as its condition.
*Longest substring without repeats. Longest with at most k distinct. Longest after replacing k
characters. Longest run of 1s after flipping k zeros. Fruit into baskets. Permutation in a string.*
Six recognisably different questions, one shape.

Interviewers ask the first of them — LeetCode 3 — more than almost any other problem in existence. It
is the standard medium warm-up at every product company. The reason it works as a filter is that the
brute force is obviously `O(n²)` or worse, the window solution is obviously better once seen, and there
is one specific bug — `left` moving backwards — that separates people who understand the invariant from
people who have memorised a shape.

---

## 2. The story

Kamesh drives a share-auto on the road that runs from the bypass junction down to the hospital, and
the way it works is that people stand along it and he picks them up as he goes.

The thing that decides whether a trip is worth doing is destinations. He will run a trip with **two**
destinations. Not three. Three means he is going down two side lanes and coming back out, and the
fifteen minutes that costs him is fifteen minutes not on the main road picking people up, and by the
time he is back the whole road has been taken by somebody else.

So on a Saturday morning, standing at the junction and looking down the road at the people waiting, the
question in his head is: **what is the longest stretch of this road I can serve in one trip?**

He works it forwards. He starts at the top of the road and walks down it in his head, taking people as
he goes and keeping a little tally — not just *which* places they are going to, but *how many* people
for each place, because that turns out to matter.

Hospital, hospital, market. Two places, fine, keep going. Hospital again — three for hospital, one for
market, still two places. Then somebody for the college, and that is a third place, so this stretch has
gone too far.

Now he does the other thing: he starts dropping people from the **front** of the stretch — the ones
nearest the junction — until he is back to two destinations.

And here is where the tally earns its place. He drops the first person, who was going to the hospital,
and that does **not** get him back to two destinations, because there are still two more hospital
people further down. He has to keep dropping until the *last* hospital person is gone. Only when the
count for a place reaches zero does that place actually leave his list.

He said once that he used to keep only the names of the places and not the numbers, and he kept getting
it wrong — crossing a place off his list while there was still somebody in the auto going there.

By the time he has walked the whole road in his head, he knows the longest stretch he can take, and he
starts the engine.

---

## 3. The idea in plain English

Kamesh's stretch of road is the window. His tally is the **map**. And his rule that a place only leaves
the list when its count reaches zero is the single most important detail in this entire family.

### The skeleton

```python
count = defaultdict(int)
left = 0
best = 0
for right, ch in enumerate(s):
    count[ch] += 1                     # the entering element
    while invalid(count):              # shape B from day 032
        count[s[left]] -= 1            # the leaving element
        if count[s[left]] == 0:
            del count[s[left]]         # THE line
        left += 1
    best = max(best, right - left + 1)
return best
```

Eight lines. Everything today is a different `invalid()`.

### The `del` at zero, and why it is not optional

`len(count)` is supposed to mean *how many distinct characters are in the window right now*. If you
decrement a count to zero and leave the key in the dictionary, `len(count)` still counts it — so it
never goes back down, the shrink loop never terminates properly, and `left` marches all the way to
`right`.

That is Kamesh crossing a place off his list while somebody in the auto is still going there — except
the code makes the opposite mistake, keeping a place on the list after everybody going there has got
out.

**Decrement, then delete at zero.** Say it as one action.

There is a Python subtlety worth knowing: with `defaultdict(int)`, merely *reading* `count[x]` for a
missing key **creates it** with value 0 — from [day 021](../day-021-frequency-maps/README.md). So
`if count[s[left]] == 0` after the decrement is safe, because the key definitely exists, but a stray
`if count[some_other_char] == 0` elsewhere silently inserts a key and corrupts `len(count)`. Use
`x in count` to test membership.

### The six problems, and the one line that differs

| Problem | The condition for **invalid** | What the map holds |
|---|---|---|
| Longest without repeating (3) | `count[ch] > 1` | character → count |
| Longest with at most k distinct (340) | `len(count) > k` | character → count |
| Fruit into baskets (904) | `len(count) > 2` | fruit type → count |
| Longest repeating replacement (424) | `window_len - max_freq > k` | character → count |
| Max consecutive ones III (1004) | `zeros > k` | just a counter, not a map |
| Permutation in string (567) | fixed window; compare maps | character → count |

**That table is the day.** Learn the skeleton once and the six problems are one line each.

Notice the fifth row. When there are only two kinds of thing — 0 and 1 — you do not need a map at all,
just an integer. **Recognising when the map collapses to a counter is worth saying**, because it is
simpler and faster and shows you understand what the map was for.

### Two ways to shrink, and which to write

**One at a time** — the pure template, and it cannot go wrong:

```python
while count[ch] > 1:
    count[s[left]] -= 1
    left += 1
```

**Jump straight there** — using a last-seen map, from
[day 024](../day-024-substrings-vs-subsequences/README.md):

```python
if ch in last and last[ch] >= left:
    left = last[ch] + 1
last[ch] = right
```

The jump version is fewer operations, and it has a bug waiting in it. **`last[ch] >= left` is
mandatory**: without it, a character last seen *before* the window began drags `left` backwards.

On `"abba"`: at the final `a`, `last["a"]` is 0, which is behind the current `left` of 2, so `left`
jumps back to 1 — the window now contains two `b`s and the answer comes out 3 instead of 2. It also
destroys the `O(n)` argument, because `left` is no longer monotonic.

**Write the `while` version under pressure.** It is one line longer and it cannot have this bug, because
it only ever increments. Offer the jump version afterwards as an optimisation, with the guard.

### The subtle one: longest repeating character replacement

LeetCode 424: *you may change at most `k` characters; what is the longest run of a single repeated
character you can produce?*

Inside any window, the characters you would have to change are all of them except the most frequent
one. So:

```
invalid  when  (right - left + 1) - max_freq > k
```

Now the famous part. The standard solution **never decreases `max_freq`** when the window shrinks, and
it is still correct. The argument:

- `best` only ever increases, and the window length never decreases — when the window becomes invalid,
  `left` advances by exactly as much as `right` did, so the window slides rather than shrinking.
- A stale, too-high `max_freq` makes the condition *easier* to satisfy, so the window can only fail to
  shrink when it should have.
- But a window that is too long is never *recorded* as an improvement, because the recorded value can
  only grow when a genuinely valid longer window appears.

**You do not need this trick.** Recomputing `max(count.values())` is `O(26)` per step — constant for a
bounded alphabet, so the whole thing is still `O(n)`. Write the honest version, get it right, and offer
the optimisation with its justification. That reads far better than a memorised trick you cannot
defend.

### The fixed-size cousin

*Permutation in String* — LeetCode 567 — asks whether **any** window of length `len(s1)` is an anagram
of `s1`. The window size is fixed, so this is [day 031](../day-031-fixed-window/README.md)'s shape with
a map inside: build the first window, then slide, adding one and removing one, comparing maps each
step.

Comparing two `Counter`s of at most 26 keys is constant work, so it stays `O(n)`. And the `del` at zero
is mandatory again, for a different reason: `Counter({'a': 1, 'b': 0})` does not equal
`Counter({'a': 1})`, so a leftover zero makes every comparison fail forever.

---

## 4. The picture

`"abcabcbb"`, no repeats allowed, with the map shown:

```
  right ch   count after adding      action                left  window   best
  ----- ---  --------------------    ------------------    ----  -------  ----
    0   a    {a:1}                   ok                     0    "a"       1
    1   b    {a:1,b:1}               ok                     0    "ab"      2
    2   c    {a:1,b:1,c:1}           ok                     0    "abc"     3
    3   a    {a:2,b:1,c:1}           a>1 -> drop 'a'        1    "bca"     3
             {a:1,b:1,c:1}           ok
    4   b    {a:1,b:2,c:1}           b>1 -> drop 'b'        2    "cab"     3
             {a:1,b:1,c:1}           ok
    5   c    {a:1,b:1,c:2}           c>1 -> drop 'c'        3    "abc"     3
             {a:1,b:1,c:1}           ok
    6   b    {a:1,b:2,c:1}           b>1 -> drop 'a'        4
             {b:2,c:1}               b>1 -> drop 'b'        5    "cb"      3
             {b:1,c:1}               ok
    7   b    {b:2,c:1}               b>1 -> drop 'c'        6
             {b:2}                   b>1 -> drop 'b'        7    "b"       3
             {b:1}                   ok

  answer 3
```

**What to notice at `right = 6`:** the shrink loop runs twice and the map loses the key `a` entirely,
because its count hit zero. If the `del` were missing, `{a:0, b:1, c:1}` would still have `len == 3`,
which matters enormously for the at-most-k-distinct variant.

The `del`-at-zero rule, made visible:

```
   WITH the del                        WITHOUT the del
   window "bca", drop 'b'              window "bca", drop 'b'
   {a:1,b:1,c:1} -> {a:1,c:1}          {a:1,b:1,c:1} -> {a:1,b:0,c:1}
   len = 2   correct                   len = 3   WRONG

   For "at most 2 distinct", the left version stops shrinking here
   and the right version keeps going until left reaches right.
```

Why `left` must never move backwards, on `"abba"`:

```
  index    0    1    2    3
  char     a    b    b    a

  right=3, ch='a', last['a'] = 0

  WITH the guard (last[ch] >= left):     WITHOUT it:
     left is currently 2                    left = last['a'] + 1 = 1
     last['a'] = 0, and 0 >= 2 is FALSE     window = s[1..3] = "bba"
     so left stays at 2                     -> contains two b's!
     window = s[2..3] = "ba"   correct      -> answer 3, should be 2
```

---

## 5. The code, built step by step

### The base case, the safe way

```python
count: defaultdict[str, int] = defaultdict(int)
left = 0
best = 0
for right, ch in enumerate(s):
    count[ch] += 1
    while count[ch] > 1:
        count[s[left]] -= 1
        if count[s[left]] == 0:
            del count[s[left]]
        left += 1
    best = max(best, right - left + 1)
```

*Add the entering character. While it now appears twice, drop characters off the front. Then record.*

The condition is `count[ch] > 1` and not `len(count) < right - left + 1`, because the first says
directly what is wrong — **this specific character repeats** — and shrinking is guaranteed to fix it,
since the only way to remove the duplicate is to pass its earlier occurrence.

### The base case, the fast way

```python
last: dict[str, int] = {}
left = 0
best = 0
for right, ch in enumerate(s):
    if ch in last and last[ch] >= left:
        left = last[ch] + 1
    last[ch] = right
    best = max(best, right - left + 1)
```

Fewer operations, and `last[ch] >= left` is load-bearing. An equivalent and clearer way to write the
same guard:

```python
left = max(left, last.get(ch, -1) + 1)
```

That says *left never goes backwards* in the code itself, which is better than relying on the reader to
notice the comparison.

### At most k distinct

Only the condition changes:

```python
while len(count) > k:
    count[s[left]] -= 1
    if count[s[left]] == 0:
        del count[s[left]]
    left += 1
```

`len(count) > k` is where the `del` earns its keep: without it `len(count)` counts characters that have
left, so it never falls back to `k` and the loop runs until `left == right`.

**Guard `k = 0`** — the answer is 0, and the loop handles it, but say it aloud.

### Max consecutive ones, where the map collapses

```python
zeros = 0
left = 0
best = 0
for right, x in enumerate(nums):
    if x == 0:
        zeros += 1
    while zeros > k:
        if nums[left] == 0:
            zeros -= 1
        left += 1
    best = max(best, right - left + 1)
```

Two kinds of value, so one integer replaces the whole map. **Noticing that is worth mentioning** — it
is the same algorithm with the data structure simplified because the alphabet is size two.

### Longest repeating character replacement

```python
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
```

Note there is no `del` here, because nothing depends on `len(count)` — the condition uses `max_freq`
and the window length. **The `del` is needed exactly when `len(count)` is part of the condition**, and
saying that shows you know why the rule exists rather than applying it superstitiously.

### Permutation in string: fixed window plus map

```python
if len(s1) > len(s2):
    return False
need = Counter(s1)
window = Counter(s2[:len(s1)])
if window == need:
    return True

for i in range(len(s1), len(s2)):
    window[s2[i]] += 1
    left_char = s2[i - len(s1)]
    window[left_char] -= 1
    if window[left_char] == 0:
        del window[left_char]
    if window == need:
        return True
return False
```

Fixed size, so both edges move together — `i` enters, `i - len(s1)` leaves, exactly
[day 031](../day-031-fixed-window/README.md). And the `del` is mandatory again, because
`Counter` equality is affected by zero entries.

### The complete solutions

```python
from collections import Counter, defaultdict


def longest_unique(s: str) -> int:
    """LeetCode 3. The safe version: shrink one at a time, so left cannot go back."""
    count: defaultdict[str, int] = defaultdict(int)
    left = 0
    best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while count[ch] > 1:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best


def longest_unique_jump(s: str) -> int:
    """The same, jumping straight to the new left. max() makes the guard explicit."""
    last: dict[str, int] = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        left = max(left, last.get(ch, -1) + 1)   # left NEVER goes backwards
        last[ch] = right
        best = max(best, right - left + 1)
    return best


def longest_k_distinct(s: str, k: int) -> int:
    """LeetCode 340. len(count) must mean 'distinct in the window' — hence the del."""
    count: defaultdict[str, int] = defaultdict(int)
    left = 0
    best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best


def longest_ones(nums: list[int], k: int) -> int:
    """LeetCode 1004. Two kinds of value, so the map collapses to one integer."""
    zeros = 0
    left = 0
    best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def character_replacement(s: str, k: int) -> int:
    """LeetCode 424. No del needed: the condition uses max_freq, not len(count)."""
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


def check_inclusion(s1: str, s2: str) -> bool:
    """LeetCode 567. FIXED window plus a map — day 031's shape, not day 032's."""
    if len(s1) > len(s2):
        return False
    need = Counter(s1)
    window = Counter(s2[:len(s1)])
    if window == need:
        return True

    for i in range(len(s1), len(s2)):
        window[s2[i]] += 1
        left_char = s2[i - len(s1)]
        window[left_char] -= 1
        if window[left_char] == 0:
            del window[left_char]        # zero entries break Counter equality
        if window == need:
            return True
    return False


if __name__ == "__main__":
    cases = ("abcabcbb", "bbbbb", "pwwkew", "", "au", "dvdf", "abba", " ")
    print([longest_unique(x) for x in cases])        # [3, 1, 3, 0, 2, 3, 2, 1]
    print([longest_unique_jump(x) for x in cases])   # identical

    print([longest_k_distinct(s, k) for s, k in
           (("eceba", 2), ("aa", 1), ("abaccc", 2), ("", 2), ("abc", 0),
            ("abcadcacacaca", 3))])
    # [3, 2, 4, 0, 0, 11]

    print([longest_ones(a, k) for a, k in
           (([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2), ([0, 0, 1, 1, 1, 0, 0], 0),
            ([0], 1), ([1], 0))])
    # [6, 3, 1, 1]

    print([character_replacement(s, k) for s, k in
           (("ABAB", 2), ("AABABBA", 1), ("AAAA", 0), ("", 1), ("ABBB", 2))])
    # [4, 4, 4, 0, 4]

    print([check_inclusion(a, b) for a, b in
           (("ab", "eidbaooo"), ("ab", "eidboaoo"), ("a", "a"), ("adc", "dcda"))])
    # [True, False, True, True]
```

---

## 6. What it costs

### Every problem on this page

`right` advances exactly `n` times. `left` only advances and never passes `right`, so at most `n` times
across the whole run. Each move does a constant number of dictionary operations, which are `O(1)` on
average.

**O(n) time**, and the argument is the same as
[day 032](../day-032-variable-window/README.md): count how far the pointers travel, not how the loops
are nested.

**Space: O(min(n, alphabet))** — one entry per distinct character currently in the window. For
lowercase English that is at most 26, so `O(1)`; for arbitrary Unicode it is bounded by `n`.

**Say the space bound carefully.** "O(k) where k is the alphabet size" is the precise answer, and
"O(1) because the alphabet is bounded at 26" is the right thing to say when the problem promises
lowercase letters.

### Against the brute force

Checking every substring for repeats: `n²/2` substrings, each checked in `O(k)`:

```
n = 1,000    brute ≈ 500,000 substring checks × up to 1,000 chars = 500,000,000 ops
             window ≈ 2,000 pointer moves
```

At `n = 100,000` the brute force is roughly `10¹⁵` operations and the window is 200,000.

### `character_replacement`, both versions

```
recompute max(count.values()) : O(26) per step  ->  26n operations
carry max_freq                : O(1) per step   ->  n operations
```

Both are `O(n)`. The trick is a constant-factor improvement of about 26×, which is real but not a
complexity change. **Say that when you offer it**, so it is clear you are not confusing an optimisation
with an asymptotic improvement.

### `check_inclusion`

One `Counter` comparison per position. Two `Counter`s of at most 26 keys compare in constant time, so:

```
n comparisons × O(26) = O(26n) = O(n)
```

There is a further optimisation — carry a `matches` counter of how many characters have exactly the
right count, updated as the two edges move — which makes each step genuinely `O(1)`. Worth naming; not
worth writing unless asked.

### The number to have ready

> One pass, both pointers forward only, so `O(n)` time and `O(k)` space where `k` is the alphabet size —
> `O(1)` for lowercase English. The brute force checks every substring, which at a thousand characters
> is 500 million operations against 2,000.

---

## 7. The traps

### The near-miss: forgetting the `del` at zero

```python
count[s[left]] -= 1
# no deletion
left += 1

print(longest_k_distinct("eceba", 2))
```

```
1
```

The answer is 3 (`"ece"`). Once any character's count hits zero, `len(count)` still includes it, so the
shrink loop's condition `len(count) > k` never becomes false again and `left` marches up to `right`.
The result collapses to 1.

**The `del` is needed exactly when `len(count)` is part of the condition.** In
`character_replacement` it is not, and there is no `del` there — knowing *why* rather than doing it
everywhere is the mark of understanding it.

### The near-miss: `left` moving backwards

```python
if ch in last:                          # missing: and last[ch] >= left
    left = last[ch] + 1
```

On `"abba"` this returns 3 instead of 2, and the mechanism is in §4's diagram: at the final `a`, the
last-seen position 0 is behind the current window, so `left` jumps backwards and the window swallows a
repeated `b`.

Two fixes, and the second is better because it states the intent:

```python
if ch in last and last[ch] >= left:
    left = last[ch] + 1
# or
left = max(left, last.get(ch, -1) + 1)
```

**And the `while`-shrink version cannot have this bug at all**, which is a reason to prefer it when you
are being watched.

### The near-miss: adding before shrinking

```python
count[ch] += 1
seen.add(ch)
while ch in seen:                       # always true — you just added it
```

If you use a set and add before checking, the condition is trivially true and `left` runs to `right`,
so every answer is 1. With a counter and `count[ch] > 1` this does not arise, which is another small
reason to prefer the counter.

### The real error: `defaultdict` inserting on read

```python
count = defaultdict(int)
if count[ch] == 0:                      # this INSERTS ch with value 0
    ...
print(len(count))                       # now includes characters never seen
```

Reading a missing key from a `defaultdict` creates it — from
[day 021](../day-021-frequency-maps/README.md). That silently corrupts `len(count)`, which is exactly
the quantity the shrink loop depends on. **Test membership with `ch in count`, never by reading the
value.**

### The near-miss: recording inside the shrink loop

```python
while len(count) > k:
    best = max(best, right - left + 1)   # WRONG PLACE
    count[s[left]] -= 1
    left += 1
```

This is [day 032](../day-032-variable-window/README.md)'s shape-A placement applied to a shape-B
problem. It records the window while it is still **invalid** — too many distinct characters — so the
answer comes out too large. **Maximise: record after the shrink loop. Minimise: record inside it.**

### The contract corner: what counts as a character

`" "` is a valid input to LeetCode 3, and the answer is 1. So are digits, symbols and Unicode. If you
reached for a 26-element array instead of a map, `ord(' ') - ord('a')` is negative and — from
[day 021](../day-021-frequency-maps/README.md) — a negative index does not raise, it reads from the
end. **Ask about the alphabet before choosing the structure.**

### The subtle one: defending `max_freq`

If an interviewer asks *"why don't you decrease `max_freq` when the window shrinks?"* and you cannot
answer, the honest move is to say so and switch to recomputing it. A wrong justification is worse than
the extra 26 operations. The correct argument is in §3, and it turns on the window never actually
shrinking — only sliding.

---

## 8. In the interview

### How it gets asked

- *"Longest substring without repeating characters."* — LeetCode 3, the most-asked medium there is.
- *"Longest substring with at most k distinct characters."* — LeetCode 340, and *fruit into baskets*
  (904) is the same problem with `k = 2`.
- *"Longest run of 1s if you can flip at most k zeros."* — LeetCode 1004, where the map collapses to a
  counter.
- *"Longest substring you can make uniform by changing k characters."* — LeetCode 424, the subtle one.
- *"Does s2 contain a permutation of s1?"* — LeetCode 567, a **fixed** window with a map.

### What to say out loud, in the first ninety seconds

1. **Ask about the alphabet.** *"Lowercase English only, or arbitrary characters? That decides whether
   I use a 26-element array or a map, and it changes the space bound I quote."*
2. **State the brute force and its cost.** *"Checking every substring for repeats is O(n²) at best."*
3. **Name the shape and which one it is.** *"This is a maximisation, so: grow the window, and shrink
   from the left only while it's invalid, recording after the shrink."*
4. **Say what the window carries and what the condition is.** *"The window carries a count map, and
   it's invalid when the character I just added appears twice."*
5. **Flag the `del` and say why.** *"When I decrement a count to zero I delete the key, because
   `len(count)` has to mean 'distinct characters currently in the window'."*
6. **Say why `left` never moves backwards.** *"Both pointers only advance, so each index is visited at
   most twice — that's the O(n) argument, and it's also why I'd rather shrink one step at a time than
   jump, since jumping can move `left` backwards on input like `abba` if the guard is missing."*
7. **Give the costs.** *"O(n) time; O(k) space for the map, which is O(1) for a bounded alphabet."*

### The follow-ups

**"Can you do it without shrinking one character at a time?"**
Yes — keep a map of the last position each character was seen, and when a repeat arrives, jump `left`
straight past that earlier occurrence instead of walking there. It is fewer operations. The thing to be
careful about is that the jump must never move `left` backwards: if the character was last seen
*before* the current window began, its recorded position is behind `left`, and assigning
`left = last[ch] + 1` unconditionally moves the window's start backwards. On `"abba"` that gives 3
instead of 2, because the window ends up containing two `b`s. The fix is either a guard,
`last[ch] >= left`, or writing it as `left = max(left, last[ch] + 1)`, which I prefer because it states
the invariant in the code. Under time pressure I would write the one-step-at-a-time version, since it
only ever increments and cannot have this bug at all.

**"Now: at most k distinct characters."**
Only the condition changes — invalid becomes `len(count) > k`. But that change makes one line load-
bearing that was optional before: when I decrement a character's count to zero I must delete the key,
because `len(count)` is now the thing the loop tests. Leave a zero entry behind and `len(count)` counts
characters that have already left the window, so it never drops back to `k`, the shrink loop keeps
running, and `left` walks all the way to `right` — the answer collapses to 1 with no error. On
`"eceba"` with k of 2 you get 1 instead of 3. It is worth noticing that *fruit into baskets* is exactly
this problem with `k = 2`, and that if there were only two possible values I would drop the map entirely
and keep a single counter.

**"Why doesn't `max_freq` need to decrease in the character-replacement problem?"**
Because the window never actually shrinks — it slides. When the window becomes invalid, `left` advances
by one for the one step `right` advanced, so the length stays the same rather than dropping. A stale,
too-high `max_freq` makes the validity test easier to pass, so the only thing it can do is fail to
shrink a window that should have shrunk — and since the recorded answer only improves when a genuinely
longer window appears, that never produces a larger wrong answer. I would add that I do not need the
trick: recomputing `max(count.values())` is `O(26)` per step, so constant for a bounded alphabet and
still `O(n)` overall. I would write that version first and offer this one as a constant-factor
optimisation with the argument attached, because a trick I cannot defend is worse than 26 extra
operations.

**"What if the string is Unicode, or extremely long?"**
The map handles Unicode with no change, which is the main reason to prefer it over a 26-element array —
that array silently misbehaves on anything outside `a`–`z`, because `ord(ch) - ord('a')` goes negative
and Python indexes from the end rather than raising. The space bound becomes `O(min(n, alphabet))`
rather than `O(1)`. For an extremely long input the algorithm is already one pass and the map only ever
holds what is currently inside the window, so memory is bounded by the window's distinct-character
count rather than by the input length — which means it works on a stream, provided you can buffer the
window itself. What I would watch is slicing: never take `s[left:right+1]` inside the loop to inspect
the window, because that copies and turns a linear algorithm into a quadratic one silently.

### A model answer

> "First, what's the alphabet? Lowercase English, or could it be arbitrary characters including spaces
> and Unicode? That decides whether I use a fixed 26-element array or a dictionary, and it changes the
> space bound I'd quote.
>
> ...Arbitrary. Then a map.
>
> The brute force checks every substring for repeats, which is O(n²) at best and worse if you rebuild a
> set each time. Instead I'll use a sliding window with a count of what's inside it.
>
> This is a maximisation, so the shape is: grow the window on the right unconditionally, and shrink from
> the left only while the window is invalid — then record after the shrink, because that's the first
> moment it's valid again.
>
> ```python
> def longest_unique(s: str) -> int:
>     count = defaultdict(int)
>     left = 0
>     best = 0
>     for right, ch in enumerate(s):
>         count[ch] += 1
>         while count[ch] > 1:
>             count[s[left]] -= 1
>             if count[s[left]] == 0:
>                 del count[s[left]]
>             left += 1
>         best = max(best, right - left + 1)
>     return best
> ```
>
> The condition is `count[ch] > 1` — the character I just added now appears twice — and shrinking is
> guaranteed to fix it, because the only way to remove the duplicate is to pass its earlier occurrence.
>
> The `del` when a count reaches zero matters. Here it's tidiness, but the moment the condition involves
> `len(count)` — as it does for the at-most-k-distinct version — it becomes essential, because
> `len(count)` has to mean 'distinct characters currently in the window'. Leave zero entries behind and
> the shrink loop never terminates properly.
>
> Cost: the right pointer advances n times, the left pointer at most n times, and neither ever moves
> backwards — so at most 2n moves, each doing constant dictionary work. O(n) time, and O(k) space where
> k is the alphabet size, bounded by n.
>
> There's a faster variant that jumps `left` straight past the previous occurrence using a last-seen
> map, and it has a specific bug worth mentioning: if the character was last seen before the window
> started, jumping unconditionally moves `left` *backwards*. On `abba` that returns 3 instead of 2. The
> fix is `left = max(left, last[ch] + 1)`. I'd write the one-step version under time pressure, because
> it only ever increments and can't have that bug."

---

## 9. Recall card

- **The window carries a map**, and the condition is a property of the map: `len(count)`, `count[x]`,
  the maximum value, or a comparison against a needed map.
- **`del` at zero — mandatory whenever `len(count)` is in the condition**, or the shrink loop never
  ends.
- **Maximise: shrink while invalid, record after.** Six problems, one skeleton, one line different.
- **`left` must never move backwards.** Guard the jump with `max(left, last[ch] + 1)`, or shrink one
  step at a time and the bug cannot exist.
- **`O(n)` time, `O(k)` space** where `k` is the alphabet. When there are only two kinds of value, the
  map collapses to one integer.
