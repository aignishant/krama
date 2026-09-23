---
day: 29
track: dsa
title: "Same direction: the read pointer and the write pointer"
phase: "Two pointers and sliding window"
status: written
---

# Day 029 · DSA — Same direction: the read pointer and the write pointer

**After today you can:** You can remove duplicates from a sorted array in place, in one pass.

**The interviewer asks it as:** *Remove duplicates in place and return the new length.*

---

## 1. What this is, and why they ask it

The second of the three two-pointer shapes. Yesterday both indices started at opposite ends and moved
towards each other. Today **both start at the front and move the same way**, one leading and one
lagging, and the gap between them is what has been thrown away.

You met the basic version on [day 015](../day-015-the-write-pointer/README.md) as in-place compaction.
Today it becomes a family, and the family is larger than most people realise:

- **Filter** — keep some elements, drop others. Move zeros, remove a value, remove duplicates.
- **Compare against what you kept** — dedupe, keep-at-most-`k`. The lagging index is not just a
  destination, it is a *record of your decisions*, and you read back from it.
- **Partition by swapping** — separate a list into groups in one pass. Sort Colors, quickselect's
  partition step, and the partition inside quicksort.
- **Walking from the back with a skip count** — backspace string compare, and merging into the end of
  an array.

Interviewers ask the dedupe version constantly because it is a five-minute problem with two real
follow-ups: *"now allow each value at most twice"*, which tests whether you compared against the right
thing, and *"does your solution preserve the order of the survivors?"*, which tests whether you know
the difference between the copy version and the swap version. Most candidates write one of them and do
not know the other exists.

This shape is also the engine inside quicksort on [day 054](../day-054-quicksort/README.md) and
quickselect on [day 055](../day-055-quickselect/README.md), so getting it into your hands now pays
twice.

---

## 2. The story

The godown near the railway siding at Sanathnagar takes in rice by the lorry-load, and Karim has been
the man who checks it for nine years.

A lorry came in on Tuesday with sixty sacks, loaded in one long row down the bed, and eleven of them
had got wet somewhere between there and here — you can tell by the colour along the bottom seam and by
the weight, and Karim can tell without picking a sack up.

The wet ones have to come out and the dry ones have to end up stacked from the front of the bed,
because the lorry is going on to a second godown and the load has to sit forward or it rides badly.

What Karim does not do is unload all sixty and put them back. He works inside the lorry, and he keeps
two things in his head.

The first is where he has got to — which sack he is looking at now. That starts at the front and moves
down the row, one sack at a time, and it never goes back.

The second is where the next good sack has to go. That also starts at the front. And here is the whole
thing: it only moves when he actually puts a sack down.

The first three sacks are dry. He looks at each one, puts it where it already is, and both of the
things in his head move along together — no gap. The fourth is wet. He steps past it, and now the two
have come apart: the place-where-the-next-good-sack-goes is standing on the wet fourth sack, and he is
looking at the fifth.

Fifth is dry, so he drags it back onto the fourth's position, and the placing spot moves to five while
he moves to six.

From then on the gap is exactly the number of wet sacks he has walked past, and it only ever grows.
The placing spot never gets ahead of him, which is the reason he can drag a sack backwards without
worrying — whatever was sitting there, he has already looked at it and already decided.

By the end of the row he is standing at the tailboard and the placing spot is eleven sacks behind him,
and that number is the answer to the only question the office actually asks: forty-nine good, eleven
wet.

---

## 3. The idea in plain English

Karim's *where I have got to* is `read`. His *where the next good one goes* is `write`. And the rule
that makes it safe — the placing spot never gets ahead of him — is the invariant.

### The skeleton

```python
write = 0
for read in range(len(items)):
    if keep(items[read]):
        items[write] = items[read]
        write += 1
return write
```

Five lines, and every variant today is this with a different `keep`.

### The invariant, stated properly

> **`write <= read` at every moment**, and everything in `items[0:write]` is finished and correct.

Both start at 0, so it holds initially. `write` only increases in the same step where `read` increases,
and `read` also increases in steps where `write` does not — so `write` can never overtake. That is why
`items[write] = items[read]` is safe: position `write` is either the same position you are reading, or
one that `read` has already passed and already decided about.

**Say that sentence in the interview.** It is what makes the whole family obviously correct rather than
apparently reckless.

### What `write` means when the loop ends

Three useful things, and which one you return depends on the question:

- **`write` is the count of kept elements.**
- **`items[0:write]`** is the answer, in the original relative order.
- **`items[write:]`** is leftovers — stale values `read` has already passed.

You cannot shrink a fixed-size array, so the convention is to **return `write` as the new length** and
let the caller ignore the rest. That is what LeetCode 26, 27 and 80 all want, and it confuses people
the first time: nothing is deleted, the count is the answer.

### The three sub-shapes

**Shape one: filter.** `keep` looks only at the current element.

```python
if items[read] != 0:              # move zeros
if items[read] != target:         # remove a value
```

**Shape two: compare against what you kept.** `keep` looks *back* at `items[write - 1]`. This is the
one that matters, and it is what makes dedupe work.

```python
if items[read] != items[write - 1]:       # remove duplicates from a sorted array
if write < 2 or items[read] != items[write - 2]:   # allow each value at most twice
```

**`items[write - 1]`, not `items[read - 1]`.** `read - 1` is the element you last *looked at*;
`write - 1` is the element you last *kept*. On a sorted array with no gaps they coincide, so the wrong
version passes — and then the "at most twice" follow-up needs a rewrite instead of a one-character
change. Comparing against what you kept is the habit that generalises.

The generalisation is worth seeing, because it is the follow-up:

```python
def keep_at_most_k(nums: list[int], k: int) -> int:
    write = 0
    for x in nums:
        if write < k or x != nums[write - k]:
            nums[write] = x
            write += 1
    return write
```

*Is this value different from the one I kept `k` places ago?* If it is, then fewer than `k` copies of
it have been kept, so this one may stay. `write < k` lets the first `k` through unconditionally. One
function, and `k = 1` and `k = 2` are LeetCode 26 and 80.

**Shape three: partition by swapping.** Instead of copying forward and leaving stale values behind,
**exchange**:

```python
if items[read] != 0:
    items[write], items[read] = items[read], items[write]
    write += 1
```

Now the discarded elements are pushed to the back rather than overwritten, so nothing is lost. That
matters when you need both groups, which is what partitioning is.

### Stable or not — the follow-up people miss

The **copy** version preserves the relative order of the survivors. The **swap** version preserves the
order of the *kept* group but scrambles the discarded group:

```python
partition_even_odd([3, 1, 2, 4])    # -> [2, 4, 3, 1]
```

The evens came out `2, 4` — original order. The odds came out `3, 1` — reversed, because `3` was
swapped to the back early. An algorithm that keeps relative order is **stable**, from
[day 015](../day-015-the-write-pointer/README.md).

**Ask which the problem wants.** If it only cares about the kept group, either works. If it needs both
groups in order, the swap version is wrong and you need extra space.

### Three pointers: the Dutch national flag

*Sort an array of 0s, 1s and 2s in one pass* — LeetCode 75 — is the same idea with three indices:

```python
low, mid, high = 0, 0, len(nums) - 1
while mid <= high:
    if nums[mid] == 0:
        nums[low], nums[mid] = nums[mid], nums[low]
        low += 1
        mid += 1
    elif nums[mid] == 2:
        nums[mid], nums[high] = nums[high], nums[mid]
        high -= 1                       # note: mid does NOT advance
    else:
        mid += 1
```

The array is kept in four regions: `[0, low)` all 0s, `[low, mid)` all 1s, `[mid, high]` unexamined,
`(high, end]` all 2s.

**The detail that catches everyone:** on a 2, `mid` does not advance. The value swapped in from `high`
has never been looked at, so it must be examined. On a 0 it is safe to advance both, because whatever
comes back from `low` is already known to be a 1 — `low` never passes anything but 1s.

`while mid <= high`, not `<`, because the element at `high` is still unexamined.

### Walking from the back

Some problems in this family run backwards, and the tell is that **information is destroyed as you go
forward but preserved going back**. Backspace string compare is the standard one: `"ab#c"` and
`"ad#c"` are equal, because `#` deletes the character before it.

Going forwards you cannot tell whether a character will survive — a `#` might arrive later. Going
backwards you can, because you have already seen all the deletions that could affect it:

```python
skip = 0
for i in range(len(s) - 1, -1, -1):
    if s[i] == "#":
        skip += 1
    elif skip:
        skip -= 1                       # this character is deleted
    else:
        yield s[i]                      # this character survives
```

Same idea as [day 018](../day-018-arrays-revision/README.md)'s merge-from-the-back: **go in the
direction where the answer is already determined.**

---

## 4. The picture

`[0, 1, 0, 3, 12]`, removing zeros, with `w` and `r`:

```
  start        0    1    2    3    4
             +----+----+----+----+----+
             |  0 |  1 |  0 |  3 | 12 |
             +----+----+----+----+----+
               ^
              w,r     0 is dropped. Only r moves. The gap opens.

             +----+----+----+----+----+
             |  0 |  1 |  0 |  3 | 12 |
             +----+----+----+----+----+
               ^    ^
               w    r     1 is kept: copy to w, then both move.

             +----+----+----+----+----+
             |  1 |  1 |  0 |  3 | 12 |
             +----+----+----+----+----+
                    ^    ^
                    w    r     position 1 still says 1 — a stale leftover,
                               already read, never read again. This is fine.

  end        +----+----+----+----+----+
             |  1 |  3 | 12 |  3 | 12 |
             +----+----+----+----+----+
               |----------|  |-------|
                  kept        leftovers
                             ^
                           w = 3 kept, r - w = 2 discarded
```

**What to notice:** the gap only grows, and it grows by exactly one per discard. `write` is the count
of keepers and `read - write` is the count of discards — both facts fall out for free.

Dedupe, showing why you compare against `write - 1`:

```
  nums   0    0    1    1    1    2
         w=1                              keep position 0 unconditionally
         r=1: nums[1]=0 == nums[w-1]=0    -> duplicate, skip
         r=2: nums[2]=1 != nums[w-1]=0    -> keep. nums[1]=1, w=2
         r=3: nums[3]=1 == nums[w-1]=1    -> duplicate, skip
         r=4: nums[4]=1 == nums[w-1]=1    -> duplicate, skip
         r=5: nums[5]=2 != nums[w-1]=1    -> keep. nums[2]=2, w=3

  result [0, 1, 2, ...]  length 3
                  ^
          nums[w-1] is always "the last thing I decided to keep",
          which is exactly the question a dedupe needs to ask.
```

The Dutch national flag, as four regions:

```
   [ 0 0 0 | 1 1 1 | ? ? ? ? ? | 2 2 2 ]
            ^       ^         ^
           low     mid       high

   all 0s   all 1s  unexamined   all 2s
   [0,low)  [low,mid)  [mid,high]  (high,end]

   nums[mid] == 0 : swap with low, low++, mid++   (the swapped-in value is a known 1)
   nums[mid] == 1 : mid++
   nums[mid] == 2 : swap with high, high--        (mid does NOT move — unexamined value)
```

**What to notice:** the `?` region shrinks by one every turn, from one end or the other, so the loop
runs at most `n` times even though `mid` sometimes stands still. That is the termination argument.

---

## 5. The code, built step by step

### Dedupe a sorted array

```python
if not nums:
    return 0
write = 1
```

`write` starts at 1 because position 0 is always kept — there is nothing before it to duplicate. That
also means `nums[write - 1]` is valid from the first comparison. The empty guard exists because
`write = 1` on an empty array would report a length of 1.

```python
for read in range(1, len(nums)):
    if nums[read] != nums[write - 1]:
        nums[write] = nums[read]
        write += 1
return write
```

`read` starts at 1 too, for the same reason. Say the comparison out loud as you write it: *"is this
different from the last value I kept?"*

### At most `k` copies

```python
def keep_at_most_k(nums: list[int], k: int) -> int:
    write = 0
    for x in nums:
        if write < k or x != nums[write - k]:
            nums[write] = x
            write += 1
    return write
```

`write < k` waves the first `k` through. Then `x != nums[write - k]` asks *is this different from the
one I kept `k` places ago?* — if it is, at most `k - 1` copies of it are already kept.

Note this iterates the values directly rather than by index, which is safe because the write position
is always at or behind the read position, so `x` was captured before any overwrite could reach it.

### The swap version, and why you might want it

```python
write = 0
for read in range(len(nums)):
    if nums[read] != 0:
        nums[write], nums[read] = nums[read], nums[write]
        write += 1
```

Exchange instead of copy, so the zeros are pushed to the back rather than overwritten and no second
pass is needed. Costs two writes per keeper instead of one, so on a mostly-non-zero array the copy
version does about half the writes — the comparison from
[day 015](../day-015-the-write-pointer/README.md).

The reason to reach for it here is **partitioning**: when you want both groups, not just one.

### Sort Colors

```python
low, mid, high = 0, 0, len(nums) - 1
while mid <= high:
```

`mid <= high` because `nums[high]` is still unexamined.

```python
    if nums[mid] == 0:
        nums[low], nums[mid] = nums[mid], nums[low]
        low += 1
        mid += 1
```

Swap the 0 down to the `low` boundary. **Both advance**, and the reason is worth saying: whatever comes
back from `low` is a value the `low` boundary had already classified, and everything in `[low, mid)` is
a 1 — so the swapped-in value is a known 1 and needs no re-examination.

```python
    elif nums[mid] == 2:
        nums[mid], nums[high] = nums[high], nums[mid]
        high -= 1
```

**`mid` does not move.** The value that came back from `high` is from the unexamined region and has
never been looked at. Advancing `mid` here is the single most common bug in this problem, and it fails
on `[1, 2, 0]` and on `[2, 1, 2]` — try both.

```python
    else:
        mid += 1
```

### Backspace compare, from the back

```python
def gen(x: str):
    skip = 0
    for i in range(len(x) - 1, -1, -1):
        if x[i] == "#":
            skip += 1
        elif skip:
            skip -= 1
        else:
            yield x[i]
```

A generator yielding the surviving characters in reverse. Then compare two of them lazily:

```python
from itertools import zip_longest
return all(a == b for a, b in zip_longest(gen(s), gen(t)))
```

`zip_longest` pads the shorter one with `None`, so different lengths correctly compare unequal —
`zip` would stop at the shorter and wrongly report equal.

`O(n + m)` time and `O(1)` extra space, against the obvious approach of building both strings, which is
`O(n + m)` space. **That space difference is the whole reason the problem is posed.**

### The complete solutions

```python
from itertools import zip_longest


def remove_duplicates(nums: list[int]) -> int:
    """LeetCode 26. Sorted input, in place. Returns the count of distinct values."""
    if not nums:
        return 0
    write = 1                                  # position 0 is always kept
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:      # compare with what was KEPT, not read
            nums[write] = nums[read]
            write += 1
    return write


def keep_at_most_k(nums: list[int], k: int) -> int:
    """LeetCode 80 generalised. Sorted input. k=1 is LeetCode 26, k=2 is LeetCode 80."""
    write = 0
    for x in nums:
        if write < k or x != nums[write - k]:  # differs from the one kept k places back
            nums[write] = x
            write += 1
    return write


def move_zeroes(nums: list[int]) -> None:
    """Swap version: one pass, no tail fill, and the zeros end up at the back."""
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1


def partition_even_odd(nums: list[int]) -> int:
    """Evens to the front. Returns where the odds start.

    NOT stable for the discarded group: [3,1,2,4] -> [2,4,3,1], odds reversed.
    """
    write = 0
    for read in range(len(nums)):
        if nums[read] % 2 == 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
    return write


def sort_colors(nums: list[int]) -> None:
    """LeetCode 75. Dutch national flag, one pass, O(1) space.

    [0,low) = 0s, [low,mid) = 1s, [mid,high] = unexamined, (high,end] = 2s
    """
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:                         # <=, because nums[high] is unexamined
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1                           # swapped-in value is a known 1
        elif nums[mid] == 2:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1                          # mid does NOT move: unexamined value
        else:
            mid += 1


def backspace_compare(s: str, t: str) -> bool:
    """LeetCode 844. O(1) extra space by walking backwards with a skip count."""
    def surviving(x: str):
        skip = 0
        for i in range(len(x) - 1, -1, -1):
            if x[i] == "#":
                skip += 1
            elif skip:
                skip -= 1
            else:
                yield x[i]

    return all(a == b for a, b in zip_longest(surviving(s), surviving(t)))


if __name__ == "__main__":
    for case in ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], [1, 1, 2], [1], [], [1, 2, 3]):
        a = list(case)
        k = remove_duplicates(a)
        print(case, "->", k, a[:k])
    # [0,0,1,1,1,2,2,3,3,4] -> 5 [0, 1, 2, 3, 4]

    a = [1, 1, 1, 2, 2, 3]
    k = keep_at_most_k(a, 2)
    print(k, a[:k])                            # 5 [1, 1, 2, 2, 3]

    b = [0, 1, 0, 3, 12]
    move_zeroes(b)
    print(b)                                   # [1, 3, 12, 0, 0]

    c = [3, 1, 2, 4]
    print(partition_even_odd(c), c)            # 2 [2, 4, 3, 1]  <- odds reversed

    for case in ([2, 0, 2, 1, 1, 0], [2, 0, 1], [0], []):
        d = list(case)
        sort_colors(d)
        print(case, "->", d)
    # [2,0,2,1,1,0] -> [0, 0, 1, 1, 2, 2]

    print([backspace_compare(x, y) for x, y in
           (("ab#c", "ad#c"), ("ab##", "c#d#"), ("a#c", "b"), ("", ""), ("a##c", "#a#c"))])
    # [True, True, False, True, True]
```

---

## 6. What it costs

### `remove_duplicates` and the filter family

The loop runs `len(nums) - 1` times — once per position — and each turn does one comparison and at most
one assignment and one increment. Constant work per turn.

**O(n) time. O(1) extra space** — `read` and `write` are two integers whatever the array size.

Against the obvious alternative of building a new list: also `O(n)` time, but `O(n)` extra space. And
against deleting in place with `del nums[i]`, which is `O(n²)`, because each delete shifts everything
after it — the shifting cost from [day 011](../day-011-insert-and-delete/README.md).

At `n = 100,000`:

```
write pointer : 100,000 comparisons
delete-in-place : ~5,000,000,000 element moves
```

### `keep_at_most_k`

Identical structure: one pass, constant work per element. **O(n) time, O(1) space**, for any `k`.

### `sort_colors`

Each turn of the loop either advances `mid` or decreases `high`, and the unexamined region
`[mid, high]` therefore shrinks by exactly one every turn. Starting at size `n`, the loop runs at most
`n` times.

**O(n) time, O(1) space — and one pass.** The obvious alternative is counting sort: one pass to count
the 0s, 1s and 2s, a second pass to write them back. Also `O(n)` and `O(1)`, and perfectly acceptable —
**but the problem explicitly asks for one pass**, and the reason is that a real version of this may be
sorting objects by a key rather than integers, where you cannot regenerate the values from a count.
Mention the counting solution, then give the one-pass one.

### `backspace_compare`

Each generator visits each character exactly once, so **O(n + m) time**. The generators hold one integer
each and yield lazily, so **O(1) extra space** beyond the inputs.

The straightforward version — build both strings with a list and `join`, then compare — is the same
`O(n + m)` time but `O(n + m)` space. On a very large input that is the difference between constant
memory and a full second copy, and it is the entire point of the question. **Write the simple one
first, then offer this.**

### Copy versus swap, counted

On `[1, 2, 3, 4]` with no zeros to remove:

```
copy version : 4 self-copies, then a 0-length tail loop      = 4 writes
swap version : 4 self-swaps                                  = 8 writes
```

On `[0, 0, 0, 1]`:

```
copy version : 1 copy + 3 tail fills                         = 4 writes
swap version : 1 swap                                        = 2 writes
```

Neither dominates. **Mostly-discarded favours swap; mostly-kept favours copy**, and both are `O(n)`.

### The number to have ready

> The write pointer is one pass, `O(n)` time and `O(1)` extra space, and it replaces either an `O(n)`
> allocation or an `O(n²)` sequence of deletes. At a hundred thousand elements that is 100,000
> operations against five billion.

---

## 7. The traps

### The near-miss: comparing against `read - 1`

```python
if nums[read] != nums[read - 1]:      # works on LeetCode 26, wrong in general
```

On a plain sorted dedupe this gives the right answer, because you never skip a value that could come
back. It breaks the moment the rule involves *how many you kept*:

```python
def keep_at_most_two(nums):
    write = 0
    for read in range(len(nums)):
        if write < 2 or nums[read] != nums[read - 2]:     # read - 2, not write - 2
            nums[write] = nums[read]
            write += 1
    return write

a = [1, 1, 1, 2, 2, 3]
k = keep_at_most_two(a)
print(k, a[:k])
```

```
4 [1, 1, 2, 3]
```

The answer is `5` and `[1, 1, 2, 2, 3]` — one of the 2s has been **dropped**. `nums[read - 2]` looks at
the *input* two positions back, but by this point the write pointer has already overwritten that
position, so the comparison is against a value that is no longer what it was. `nums[write - 2]` reads
back from the output, which is the only thing that reflects your actual decisions.

Note that it gives the right answer on `[1, 1, 1, 1, 2, 3]`, which is exactly the kind of input people
test with. **Compare against what you kept.**

### The real error: forgetting the empty guard

```python
def remove_duplicates(nums):
    write = 1                          # no empty check
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write

print(remove_duplicates([]))
```

```
1
```

No exception — it reports a length of 1 for an empty array, which is a silent wrong answer rather than
a crash. The loop never runs, so `nums[write - 1]` is never evaluated and the bug hides. **Any solution
that pre-keeps element 0 needs an empty guard.**

### The near-miss: advancing `mid` after swapping a 2 in Sort Colors

```python
elif nums[mid] == 2:
    nums[mid], nums[high] = nums[high], nums[mid]
    high -= 1
    mid += 1                           # WRONG
```

```python
nums = [1, 2, 0]
sort_colors(nums)
print(nums)
```

```
[1, 0, 2]
```

Not sorted. The value swapped in from `high` came from the unexamined region and was never looked at —
here the `0` arrived at `mid` and was walked straight past. `[2, 1, 2]` is worse still: it comes back
completely unchanged. Contrast with the `0` branch, where advancing
`mid` **is** correct, because everything in `[low, mid)` is a 1, so the value coming back from `low` is
a known 1.

**Two swaps, two different rules, and the reason is what is known about the region you swapped with.**

### The near-miss: assuming the swap version is stable

```python
partition_even_odd([3, 1, 2, 4])      # -> [2, 4, 3, 1]
```

The evens keep their order; the odds come out reversed. If the problem says "preserve the relative
order of both groups", this is wrong and no in-place `O(1)`-space solution exists — you need `O(n)`
extra space, or a stable partition algorithm that is considerably more work. **Ask whether order
matters, and for which group.**

### The near-miss: `zip` instead of `zip_longest`

```python
return all(a == b for a, b in zip(surviving(s), surviving(t)))
print(backspace_compare("a#c", "b"))
```

`zip` stops at the shorter sequence, so a string that is a prefix of the other compares **equal**. Here
`"a#c"` reduces to `"c"` and `"b"` stays `"b"`, so it happens to be caught — but `"ac"` against `"c"`
would wrongly return `True`. `zip_longest` pads with `None`, which never equals a character.

### The near-miss: forgetting the tail

The copy version leaves stale values after `write`. If the problem wants zeros at the end — LeetCode
283 — you must fill them:

```python
for i in range(write, len(nums)):
    nums[i] = 0
```

Skip it and the front is right and the back is rubbish, and a test that checks only `result[:3]`
passes. **Always compare the whole array.**

---

## 8. In the interview

### How it gets asked

- *"Remove duplicates from a sorted array in place and return the new length."* — LeetCode 26. Then
  *"now allow each value at most twice"*, which is LeetCode 80 and the real question.
- *"Move all zeros to the end."* — LeetCode 283, and the stability follow-up.
- *"Sort an array of 0s, 1s and 2s in a single pass."* — LeetCode 75. The counting solution is
  two passes, so they want the flag.
- *"Compare two strings with backspaces, in O(1) space."* — LeetCode 844, where the space constraint
  forces the backwards walk.

### What to say out loud, in the first ninety seconds

1. **Pin the contract.** *"In place, so I cannot allocate a second array? And do I return the count, or
   is the array itself checked? And does the relative order of the survivors have to be preserved?"*
2. **Name the shape.** *"Two indices moving the same way — a read index that visits every position, and
   a write index that says where the next kept element goes."*
3. **State the invariant, because it is why it is safe.** *"The write index never overtakes the read
   index, so anything I overwrite has already been read and decided. That is what makes writing into
   the array I am reading from safe."*
4. **Say what the comparison is against.** *"For dedupe I compare against `nums[write - 1]` — the last
   value I kept — rather than `nums[read - 1]`, which is the last value I looked at. On this problem
   they coincide, but the habit is what makes the at-most-twice follow-up a one-character change."*
5. **Say what `write` means at the end.** *"When the loop ends, `write` is the number of elements kept,
   and everything from there on is stale leftovers."*
6. **Give the cost.** *"O(n) time, one pass, O(1) extra space."*
7. **Name what you are not doing.** *"I'm not deleting in place — each delete shifts everything after
   it, so that would be O(n²)."*

### The follow-ups

**"Now allow each value to appear at most twice."**
One character, if I compared against the right thing. The condition becomes `nums[read] != nums[write -
2]` with `write < 2` letting the first two through unconditionally — *is this value different from the
one I kept two places ago?* If it is, then at most one copy is already kept and this one may stay.
Generalise the 2 to a `k` and the same five lines solve "at most k times", which is the version I would
actually write since it costs nothing. This is only a one-character change because the original
compared against `nums[write - 1]`; a solution built on `nums[read - 1]` needs restructuring, because
`read - 2` looks at the input two positions back, and by that point the input has been overwritten by
earlier writes.

**"Does your solution preserve the order of the elements?"**
The copy version does — survivors come out in their original relative order, so it is stable. The swap
version preserves the order of the kept group but reverses or scrambles the discarded group, because
elements get swapped backwards from wherever the write index happens to be. `[3,1,2,4]` partitioned by
evens gives `[2,4,3,1]`: evens in order, odds reversed. So which one I use depends on whether anything
downstream cares about the second group. If both groups must keep their order and I am not allowed
extra space, there is no simple `O(n)` `O(1)` answer — stable in-place partition exists but is
considerably more involved, and I would say so rather than pretend the swap version does it.

**"Sort colours in one pass — why does `mid` not advance when you swap a 2?"**
Because the value that comes back from `high` is from the unexamined region and I have never looked at
it. If I advance `mid`, I walk past a value I have not classified — on `[2,0,1]` a `0` gets swapped to
`mid` and skipped, and the result is `[1,0,2]`, unsorted. The contrast with the `0` branch is the
interesting part: there, advancing `mid` **is** correct, because everything between `low` and `mid` is
known to be a 1, so the value swapped back from `low` is a known 1 and needs no re-examination. Two
swaps, two rules, and the difference is entirely about what is already known about the region on the
other end of the swap. Termination is easy either way: every turn either advances `mid` or lowers
`high`, so the unexamined region shrinks by one each time.

**"Do the backspace comparison in O(1) space."**
Walk both strings backwards with a skip counter. Forwards you cannot decide whether a character
survives, because a `#` might arrive later; backwards you can, because you have already seen every
deletion that could affect it. So: scan right to left, increment `skip` on a `#`, decrement it and
discard the character when `skip` is positive, otherwise the character survives. Comparing two such
walks lazily — as generators — gives `O(n + m)` time and `O(1)` extra space, against the obvious
build-both-strings approach which is the same time but `O(n + m)` space. The detail to be careful about
is the end: I need `zip_longest` rather than `zip`, or a string that is a suffix of the other compares
equal because `zip` stops at the shorter one.

### A model answer

> "Three clarifications. In place, so no second array? Do I return the new length, or will you check
> the array? And does the order of the survivors matter?
>
> ...In place, return the length, order preserved. Good.
>
> I'll use two indices moving in the same direction. A read index visits every position from left to
> right. A write index says where the next element I keep should go. Because the array is sorted,
> duplicates are adjacent, so 'have I seen this before?' reduces to 'is it the same as the last thing
> I kept?'
>
> ```python
> def remove_duplicates(nums: list[int]) -> int:
>     if not nums:
>         return 0
>     write = 1
>     for read in range(1, len(nums)):
>         if nums[read] != nums[write - 1]:
>             nums[write] = nums[read]
>             write += 1
>     return write
> ```
>
> Three things worth calling out.
>
> `write` starts at 1 because position 0 is always kept — nothing precedes it — which also makes
> `nums[write - 1]` valid on the first comparison. And that is why I need the empty guard: without it,
> an empty array returns a length of 1, silently, because the loop never runs and the bug never
> surfaces.
>
> I compare against `nums[write - 1]`, not `nums[read - 1]`. On this problem they happen to agree, but
> `write - 1` is the last value I *kept* and `read - 1` is the last value I *looked at* — and that
> distinction is what makes the at-most-twice follow-up a one-character change to `write - 2` rather
> than a rewrite.
>
> The property that makes overwriting safe is that the write index never overtakes the read index. Both
> start at 0; `write` only increases in steps where `read` also increases, and `read` sometimes
> increases alone. So every position I write to is either the one I am reading or one I have already
> passed and already decided about.
>
> That is one pass, O(n) time and O(1) extra space. When the loop ends, `write` is the count of
> distinct values, and everything from `write` onwards is stale leftovers, which the caller ignores.
>
> The version I deliberately avoided is deleting duplicates in place — each `del` shifts everything
> after it, so that is O(n²): about five billion element moves on a hundred thousand elements, against
> a hundred thousand comparisons here."

---

## 9. Recall card

- **Both indices move forward.** `read` visits everything; `write` advances only on a keep. The gap is
  what you discarded.
- **The invariant: `write <= read`**, so overwriting is always safe — and `items[0:write]` is finished
  and correct.
- **Compare against `items[write - 1]`, not `items[read - 1]`** — what you kept, not what you saw. That
  makes `k`-duplicates a one-character change.
- **Copy is stable; swap is not** for the discarded group. `[3,1,2,4]` → `[2,4,3,1]`.
- **Sort Colors: on a 2, `mid` does not advance** — the value from `high` is unexamined. On a 0 it does,
  because the value from `low` is a known 1.
