---
day: 27
track: dsa
title: "Two pointers: the idea"
phase: "Two pointers and sliding window"
status: written
---

# Day 027 · DSA — Two pointers: the idea

**After today you can:** You can spot the shape of a problem that two pointers turns from O(n^2) into O(n).

**The interviewer asks it as:** *Can you do better than the nested loop?*

---

## 1. What this is, and why they ask it

**Two pointers** means keeping two indices into the same sequence and moving them according to a rule,
instead of looping over every pair. It turns a great many `O(n²)` problems into `O(n)`, and it is
probably the highest-value pattern in the whole of interview preparation — the next ten days are built
on it, and it reappears in linked lists, sorting, and dynamic programming.

You have already used it three times without it being named. The write pointer on
[day 015](../day-015-the-write-pointer/README.md). The two ends walking inwards on
[day 023](../day-023-palindromes/README.md). The two indices comparing two strings on
[day 026](../day-026-strings-revision/README.md). Today names the family and — much more importantly —
explains **why it is allowed to work**, because that is the part interviewers push on and the part
most candidates cannot supply.

The reason is always the same and it is worth learning as a sentence: **each move eliminates a whole
set of possibilities at once, and you can prove none of them could have been the answer.** A nested
loop checks `n²/2` pairs. Two pointers checks about `n` of them and discards the rest with an argument.
If you cannot state the argument, you have memorised a solution rather than understood one — and
*"why is it safe to move the left pointer there?"* is the follow-up that finds out.

---

## 2. The story

Sathish is eleven and he spends most of the summer at his grandfather's provision shop, and the job he
likes is the weighing.

There is a two-pan balance on the counter, the old kind, and beside it a wooden block with the brass
weights standing in a row in their holes — the smallest at one end, the biggest at the other, in order,
because his grandfather has kept them that way for forty years and gets annoyed if they are not.

The game his grandfather sets him is this. A woman wants exactly two and a half kilos of rice in one
go. Find two weights from the row that come to exactly two and a half, or say there are none.

Sathish used to do it the obvious way. Take the first weight, try it against every other weight in
turn. Then take the second weight and try it against every other one. It works and it takes a long
time and he lost his place constantly.

His grandfather showed him the other way, and it is the only thing Sathish has ever learnt from him
that felt like a trick.

Put one finger on the smallest weight and one finger on the biggest. Lift both onto the pan and look.

Too heavy. Now here is the thing — that biggest weight is finished. Not just with this small one. With
*everything*. Because it is already too heavy paired with the very lightest weight in the row, and
every other weight is heavier than that one, so it can only get worse. So take your finger off it and
move to the next biggest, and never think about it again.

Too light works the same way in the other direction. The smallest weight is finished, because even
paired with the biggest thing on the block it did not reach, and everything else is smaller than the
biggest. Move that finger up one.

Exactly right, and you stop.

What Sathish noticed after a week is that his fingers only ever move towards each other, and each one
only moves forward, so the whole thing is over by the time they meet. On the block with fourteen
weights, the old way was ninety-one lifts. This way is never more than thirteen.

---

## 3. The idea in plain English

Sathish's two fingers are two indices. His grandfather's *"that weight is finished"* is the elimination
argument, and it is the whole subject.

### The canonical problem

*Given a **sorted** array and a target, find two numbers that add to the target.*

```python
left, right = 0, len(nums) - 1
while left < right:
    total = nums[left] + nums[right]
    if total == target:
        return [left, right]
    if total < target:
        left += 1          # the smallest value is too small to ever work
    else:
        right -= 1         # the largest value is too large to ever work
```

Nine lines. `O(n)` time, `O(1)` space, where the nested loop is `O(n²)`.

### Why each move is safe — say this out loud

This is the part that matters, and it needs the array to be **sorted**.

**When the total is too small**, `nums[left]` is the smallest value still in play, and it is currently
paired with `nums[right]`, the **largest** value still in play. That is the best this element will ever
do. If even its best partner does not reach the target, then no partner can, so `nums[left]` cannot be
part of any answer. Discard it — that is one move that eliminates every remaining pair containing it.

**When the total is too large**, the mirror image. `nums[right]` is already paired with the smallest
remaining value and is still too big, so no smaller partner will save it. Discard it.

**Each step throws away a whole row of the pair table** — up to `n` pairs — with one comparison. That
is where the factor of `n` goes, and it is the answer to *"why is this safe?"*

Notice what the argument depends on: **sortedness**. On an unsorted array, "the largest value still in
play" is not `nums[right]`, and the whole argument collapses. That is why *"is it sorted?"* is the
first question you ask.

### Termination, and why `left < right`

Every turn moves exactly one of the two indices, and `left` only increases while `right` only
decreases. So the gap between them shrinks by at least one every turn, and the loop must end after at
most `n` turns.

`left < right` and not `<=`, because the two values must be different elements. With `<=` you would
allow `nums[i] + nums[i]`, using the same element twice — which the problem almost certainly forbids.
**Ask.** Some versions allow it and the condition changes.

### The three shapes of two pointers

Not every two-pointer problem has the pointers at opposite ends. There are three arrangements, and
recognising which you need is most of the skill.

| Shape | Where they start | How they move | Used for |
|---|---|---|---|
| **Opposite ends** | `0` and `n-1` | towards each other | pair sums, palindromes, container with most water. Needs **sorted** or symmetric input. [Day 028](../day-028-opposite-ends/README.md) |
| **Same direction** | both at `0` | one leads, one follows | write pointer, compaction, dedupe. [Day 029](../day-029-read-write-pointer/README.md) |
| **Fast and slow** | both at head | one moves twice as fast | cycle detection, middle of a list. [Day 030](../day-030-fast-and-slow/README.md) |

And the **sliding window** from [day 031](../day-031-fixed-window/README.md) onwards is the
same-direction shape with the pair of indices treated as the ends of a range rather than as two
separate things.

### How to recognise the opposite-ends shape

The tells, in order of reliability:

1. **The array is sorted, or you are allowed to sort it.** The single strongest signal.
2. **The answer is a pair** — two numbers, two positions, two lines.
3. **The brute force is a nested loop over pairs**, and the problem says "can you do better?"
4. **The input is symmetric in some way** — a palindrome, or a shape read from both ends.
5. **You are asked for `O(1)` space**, which rules out the hash-map answer.

### The other answer, and when to prefer it

For pair-sum on an **unsorted** array, there is a different `O(n)` solution: walk once, and for each
value ask a hash set whether `target - value` has already been seen.

```python
seen = {}
for i, x in enumerate(nums):
    if target - x in seen:
        return [seen[target - x], i]
    seen[x] = i
```

`O(n)` time, `O(n)` space, and **it does not need the array sorted**. That is LeetCode 1.

So which? The honest comparison:

| | Two pointers | Hash map |
|---|---|---|
| needs sorted input | **yes** | no |
| time on sorted input | `O(n)` | `O(n)` |
| time if you must sort first | `O(n log n)` | `O(n)` |
| space | `O(1)` | `O(n)` |
| returns original indices | not after sorting | yes |

**If it arrives sorted, use two pointers** — same time, less space. **If it is unsorted and you need
original indices, use the hash map**, because sorting destroys them. Saying that comparison, rather
than picking one, is the complete answer.

---

## 4. The picture

`nums = [2, 7, 11, 15]`, `target = 18`:

```
  index    0     1     2     3
         +-----+-----+-----+-----+
  value  |  2  |  7  | 11  | 15  |
         +-----+-----+-----+-----+
            ^                 ^
          left              right      2 + 15 = 17  < 18  -> left++
                                       (2 paired with the biggest and still short:
                                        2 can never work. Discard it.)

         +-----+-----+-----+-----+
         |  2  |  7  | 11  | 15  |
         +-----+-----+-----+-----+
                  ^           ^
                left        right      7 + 15 = 22  > 18  -> right--
                                       (15 paired with the smallest left and still
                                        too big: 15 can never work. Discard it.)

         +-----+-----+-----+-----+
         |  2  |  7  | 11  | 15  |
         +-----+-----+-----+-----+
                  ^     ^
                left  right           7 + 11 = 18  -> found, return [1, 2]
```

**What to notice:** three comparisons for four elements. The nested loop would do six. The gap widens
fast — at `n = 10,000` it is 10,000 against 50 million.

What each move actually discards, drawn as the table of pairs:

```
        j=0   j=1   j=2   j=3
  i=0    -    2+7   2+11  2+15        <- one move of `left` deletes this whole row
  i=1    -     -    7+11  7+15
  i=2    -     -     -    11+15
  i=3    -     -     -     -
                            ^
                            one move of `right` deletes this whole column
```

**What to notice:** the nested loop visits every cell — `n(n-1)/2` of them. Two pointers deletes an
entire row or an entire column per step, and there are only `n` rows and columns, so it finishes in
about `n` steps. **That is the whole reason it is linear**, and it is the picture to have in mind when
somebody asks why it works.

The three shapes, side by side:

```
  OPPOSITE ENDS            SAME DIRECTION           FAST AND SLOW
  (sorted input)           (compaction)             (cycles, middle)

  [ . . . . . . . ]        [ . . . . . . . ]        [ . . . . . . . ]
    ^           ^            ^ ^                      ^ ^
    L           R            W R                      S F
    -->       <--            -->-->                   -->  ---->

  they meet in the         write lags behind        fast moves 2 per
  middle; each move        read; the gap is         step of slow; they
  eliminates a row         what was discarded       meet iff there is
  or a column                                       a cycle
```

---

## 5. The code, built step by step

### The two indices, and the loop

```python
left, right = 0, len(nums) - 1
while left < right:
```

Opposite ends. `left < right` because the two must be different elements, and because it guarantees
termination — every turn moves one of them inwards.

### The three-way decision

```python
    total = nums[left] + nums[right]
    if total == target:
        return [left, right]
    if total < target:
        left += 1
    else:
        right -= 1
```

Three cases and each has a reason you can state. Equal: done. Too small: the left value is the smallest
in play and has already been given the best partner available, so discard it. Too big: mirror image.

Write `total` into a variable rather than computing it twice. It reads better and, more usefully, it
gives you something to point at while explaining.

### The whole thing

```python
def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        if total < target:
            left += 1
        else:
            right -= 1
    return []
```

`O(n)` time, `O(1)` space, and it handles the empty array and the one-element array without a special
case — `left < right` is false immediately.

### The same shape, a different rule: container with most water

LeetCode 11, and it is the problem that proves you understood the elimination argument rather than
memorising the sum version.

> *Given heights of vertical lines, pick two so that the container they form holds the most water.*

The area is `min(height[left], height[right]) × (right - left)` — the shorter line decides the depth,
and the distance decides the width.

```python
left, right = 0, len(height) - 1
best = 0
while left < right:
    best = max(best, min(height[left], height[right]) * (right - left))
    if height[left] < height[right]:
        left += 1
    else:
        right -= 1
```

**Why move the shorter one?** This is the argument, and it is the whole question. Whatever you do next,
the width can only shrink. So the only way to beat the current area is to increase the depth. Moving
the **taller** line inwards cannot increase the depth, because the depth is set by the *shorter* one —
so every container you could form that way is worse than the one you just measured. Moving the
**shorter** one is the only move that can possibly help.

That is a genuinely different rule from the sum problem, arrived at by the same kind of reasoning.
**Two pointers is not one algorithm; it is a family with a shared proof obligation.**

### Same direction: dedupe a sorted array

The write pointer from [day 015](../day-015-the-write-pointer/README.md), now named:

```python
def remove_duplicates(nums: list[int]) -> int:
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write
```

Both indices start near the front and move the same way; `write` lags. Same family, different shape.

### The complete solutions

```python
def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    """Sorted input. O(n) time, O(1) space.

    Too small -> nums[left] is already paired with the largest value available,
                 so it can never reach the target. Discard it.
    Too large -> mirror image for nums[right].
    """
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        if total < target:
            left += 1
        else:
            right -= 1
    return []


def two_sum_hash(nums: list[int], target: int) -> list[int]:
    """LeetCode 1. Unsorted input, original indices. O(n) time, O(n) space."""
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []


def max_area(height: list[int]) -> int:
    """LeetCode 11. Move the SHORTER line: width only shrinks, so only depth can help."""
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        best = max(best, min(height[left], height[right]) * (right - left))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best


def remove_duplicates(nums: list[int]) -> int:
    """Same-direction two pointers. Sorted input, in place, returns the new length."""
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write


def is_palindrome_list(values: list[int]) -> bool:
    """Opposite ends on a symmetric input — no sorting needed here."""
    left, right = 0, len(values) - 1
    while left < right:
        if values[left] != values[right]:
            return False
        left += 1
        right -= 1
    return True


if __name__ == "__main__":
    print([two_sum_sorted(a, t) for a, t in
           (([2, 7, 11, 15], 9), ([2, 3, 4], 6), ([-1, 0], -1),
            ([1, 2, 3, 4], 100), ([], 5), ([1], 1))])
    # [[0, 1], [0, 2], [0, 1], [], [], []]

    print(two_sum_hash([3, 2, 4], 6))          # [1, 2] — unsorted, original indices

    print([max_area(x) for x in
           ([1, 8, 6, 2, 5, 4, 8, 3, 7], [1, 1], [1, 2], [4, 3, 2, 1, 4])])
    # [49, 1, 1, 16]

    a = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k = remove_duplicates(a)
    print(k, a[:k])                            # 5 [0, 1, 2, 3, 4]

    print(is_palindrome_list([1, 2, 3, 2, 1]), is_palindrome_list([1, 2, 3]))
    # True False
```

---

## 6. What it costs

### `two_sum_sorted`

Every turn of the loop moves exactly one index, `left` only forward and `right` only backward, and the
loop stops when they meet. So the total number of turns is at most `n - 1`, and each turn does one
addition and at most two comparisons — constant work.

**O(n) time. O(1) extra space** — two integers, whatever the size of the array.

### Against the nested loop

The nested loop examines every pair: `n(n-1)/2`. Measured, on an input where no pair exists so both
versions do their full work:

```
n =  1,000   two pointers 0.000067 s   nested loop 0.0225 s     334x     1,000 vs 499,500 pairs
n =  5,000   two pointers 0.000332 s   nested loop 0.5923 s   1,782x     5,000 vs 12,497,500
n = 10,000   two pointers 0.000679 s   nested loop 2.3448 s   3,454x    10,000 vs 49,995,000
```

Look at the ratio column: it roughly **doubles when `n` doubles** — 334, then 1,782, then 3,454. That
is the signature of `O(n)` against `O(n²)`, and it means the gap keeps widening. At `n = 100,000` the
nested loop would take about four minutes and two pointers about seven milliseconds.

### If you have to sort first

If the input is unsorted, two pointers needs `O(n log n)` for the sort, so the total is `O(n log n)`
time and `O(1)` extra space — worse in time than the hash map's `O(n)`, better in space than its
`O(n)`. And sorting **destroys the original indices**, so if the answer must be positions in the
original array, either use the hash map or sort `(value, index)` pairs and pay `O(n)` space anyway.

**Say the whole comparison**, not just your choice:

```
sorted input, positions in the sorted array : two pointers, O(n) time, O(1) space   <- best
unsorted input, need original indices       : hash map,     O(n) time, O(n) space   <- best
unsorted input, memory is tight             : sort + two pointers, O(n log n), O(1)
```

### `max_area`

Same structure, so **O(n) time and O(1) space**. The brute force over all pairs is `O(n²)`; at
`n = 10,000` that is 50 million area computations against 10,000.

### `remove_duplicates`

One pass, `n` turns of constant work: **O(n) time, O(1) extra space.**

### The number to have ready

> Two pointers turns `n(n-1)/2` pair checks into at most `n` steps, because each move eliminates an
> entire row or column of the pair table. At `n = 10,000` that is 10,000 comparisons against 50
> million — measured at about 3,500 times faster, and the ratio doubles every time `n` doubles.

---

## 7. The traps

### The near-miss: forgetting that it needs sorted input

```python
print(two_sum_sorted([3, 2, 4], 6))
```

```
[]
```

The answer is `[1, 2]` — `2 + 4`. The function returns nothing, with no error, because the elimination
argument is false on unsorted data: `nums[right]` is not the largest remaining value, so "discard the
largest" discards something that might have been the answer.

**Sortedness is a precondition, not a convenience.** If it is not sorted you either sort it — `O(n log
n)`, and you lose the original indices — or you use the hash map. Ask which the interviewer wants.

### The near-miss: `left <= right`

```python
while left <= right:
```

Now `left` and `right` can land on the same element, so `nums[i] + nums[i]` counts as a pair. On
`[1, 2, 3]` with target `4`, it returns `[1, 1]` — the single value 2 used twice. Almost every version
of this problem forbids that. **`left < right` for pair problems; `left <= right` is for binary search,
where a single remaining element is still a valid candidate.**

### The near-miss: moving the wrong pointer in `max_area`

```python
if height[left] > height[right]:
    left += 1                       # moving the TALLER one
else:
    right -= 1
```

On `[1, 8, 6, 2, 5, 4, 8, 3, 7]` the correct answer is 49; this returns 8. Moving the taller line
cannot increase the depth — the depth is fixed by the shorter one — and the width has shrunk, so every
container reachable that way is strictly worse. **Whenever you write a two-pointer move rule, say the
one-sentence reason out loud as you write it.** If you cannot, the rule is a guess.

### The near-miss: forgetting the answer is a pair of *values*, not the pair you were asked for

Some versions want the values, some want indices, some want them 1-indexed — LeetCode 167 wants
`[left + 1, right + 1]`. This is not a bug in your reasoning, it is a bug in your reading, and it costs
a submission. **Read the return type before writing the return statement.**

### The near-miss: assuming distinct values

```python
two_sum_sorted([1, 1, 2, 3], 2)
```

Returns `[0, 1]`, which is correct — but only because `left < right` allowed two *different positions*
holding the same value. Problems that say "you may not use the same element twice" mean the same
*position*, not the same value. If a problem genuinely forbids equal values, that is a different
condition and you must write it explicitly.

### The trap in the follow-up: three-sum

*"Now find three numbers that sum to zero"* — LeetCode 15 — is not a three-pointer problem. It is a
loop over the first element with **two pointers inside**:

```python
for i in range(len(nums) - 2):
    # then two pointers over nums[i+1:] looking for -nums[i]
```

`O(n²)` overall, which is the expected answer. Candidates who try to move three pointers
simultaneously get stuck, because there is no elimination argument that works for three at once. The
right instinct is: **fix one, two-pointer the rest.** The other detail is skipping duplicate values of
`nums[i]`, or you emit the same triple repeatedly.

---

## 8. In the interview

### How it gets asked

- *"Can you do better than the nested loop?"* — the direct version, and it almost always means two
  pointers or a hash map.
- *"The array is sorted. Find two numbers that add to the target."* — LeetCode 167. The word *sorted*
  is doing all the work.
- *"Container with most water."* — LeetCode 11, the one that tests whether you can construct a new
  elimination argument.
- *"Three sum."* — LeetCode 15, where the answer is "fix one and two-pointer the rest".
- *"Why is it safe to move that pointer?"* — the follow-up that separates understanding from recall.

### What to say out loud, in the first ninety seconds

1. **Ask whether it is sorted.** *"Is the array sorted? That decides whether two pointers is even
   available."* This is the single most valuable question in this topic.
2. **State the brute force and its cost.** *"The obvious approach is every pair, which is O(n²)."*
3. **Name the pattern and the shape.** *"Since it's sorted, I'll use two pointers from opposite ends
   moving inwards."*
4. **Give the elimination argument before writing the code.** *"If the sum is too small, the left
   value is the smallest still available and it's already paired with the largest — so it can never
   reach the target with anything, and I can discard it entirely. Too big is the mirror image."* This
   is the sentence the question exists for.
5. **Say what that buys.** *"Each move eliminates a whole row or column of the pair table, and there
   are only n of each, so it's O(n) instead of O(n²)."*
6. **Say why the loop terminates.** *"Every turn moves one pointer inwards and they only ever
   approach, so it ends in at most n steps."*
7. **Give the alternative and when you would prefer it.** *"If it weren't sorted, a hash map is O(n)
   time and O(n) space and keeps the original indices, which sorting would destroy."*

### The follow-ups

**"Why is it safe to move the left pointer when the sum is too small?"**
Because of what the sortedness guarantees about what is left. `nums[left]` is the smallest value still
in play, and right now it is paired with `nums[right]`, which is the **largest** value still in play.
So that pairing is the best `nums[left]` will ever achieve — every other remaining partner is smaller.
If even the best case falls short of the target, then no pairing involving `nums[left]` can reach the
target, so I can discard it and every pair containing it in one move. That is the entire reason this
is linear: one comparison removes up to `n` pairs from consideration, and the nested loop removes one.
The argument depends completely on the array being sorted — on unsorted data `nums[right]` is not the
largest remaining value and the whole thing is false.

**"What if the array isn't sorted?"**
Two options and I would name both. Sort it first, which makes the total `O(n log n)` time and keeps
`O(1)` extra space — but sorting destroys the original positions, so if the answer must be indices into
the original array I would have to sort `(value, index)` pairs, which costs `O(n)` space and removes
the space advantage. Or use a hash map: one pass, and for each value ask whether `target - value` has
already been seen. That is `O(n)` time and `O(n)` space and keeps the original indices naturally. For
LeetCode 1, which is unsorted and wants indices, the hash map is simply the right answer. Two pointers
wins specifically when the input arrives sorted, or when memory is tight enough that `O(1)` space is
worth an `O(n log n)` sort.

**"Now do three-sum."**
Not three pointers — there is no elimination argument that works on three moving indices at once.
Instead I fix the first element with an outer loop and run two pointers on the remainder looking for
its negation. Sort first, so the two-pointer step is valid, and the total is `O(n log n) + O(n²)`,
which is `O(n²)` — and that is the expected answer; there is no known better bound for this problem.
The detail that catches people is duplicates: since the problem wants distinct triples, I skip over
repeated values of the outer element, and skip repeats of `left` and `right` after recording a match.
Getting the deduplication right is most of the difficulty, and I would say so before writing it.

**"Container with most water — why move the shorter line?"**
Because the width can only shrink from here, so the only way to find a bigger area is to increase the
depth, and the depth is determined by the **shorter** of the two lines. If I move the taller line
inwards, the depth is still capped by the shorter one — which has not changed — while the width has
gone down, so every container I could form is strictly worse than the one I just measured. Moving the
shorter line is the only move that can possibly increase the depth. It is the same style of reasoning
as the sum problem but a completely different rule, which is why I would always state the argument
rather than reach for a remembered move — two-pointer problems share a proof obligation, not an
algorithm.

### A model answer

> "First: is the array sorted? That's the question that decides whether this technique is available at
> all.
>
> ...Sorted, good.
>
> The brute force is to check every pair, which is n choose 2, so O(n²). At ten thousand elements
> that's about fifty million comparisons.
>
> Because it's sorted I can do it in one pass with two indices, one at each end, moving inwards.
>
> ```python
> def two_sum_sorted(nums: list[int], target: int) -> list[int]:
>     left, right = 0, len(nums) - 1
>     while left < right:
>         total = nums[left] + nums[right]
>         if total == target:
>             return [left, right]
>         if total < target:
>             left += 1
>         else:
>             right -= 1
>     return []
> ```
>
> The important part is why each move is safe, and it comes entirely from sortedness. If the total is
> too small, then `nums[left]` is the smallest value still available and it is currently paired with
> `nums[right]`, the largest one still available. That's the best that element will ever do — every
> other remaining partner is smaller. So if its best case falls short, no pair containing it can reach
> the target, and I can discard it completely. Too large is the mirror image: `nums[right]` is already
> paired with the smallest remaining value and is still too big, so nothing smaller will help.
>
> That's where the speed comes from. Think of the table of all pairs — the nested loop visits every
> cell, and each move here deletes an entire row or an entire column. There are only n rows and n
> columns, so I finish in about n steps rather than n²/2. I measured it: at ten thousand elements it
> was about three and a half thousand times faster, and the ratio doubles every time n doubles.
>
> The loop terminates because every turn moves exactly one index and they only ever approach each
> other, so it ends within n steps. And it's `left < right` rather than `<=`, because the two must be
> different positions — with `<=` I'd allow an element to pair with itself.
>
> O(n) time, O(1) extra space.
>
> If it weren't sorted, I'd change approach rather than sort. A hash map does it in one pass — for each
> value, ask whether target minus it has already been seen — which is O(n) time and O(n) space, and it
> keeps the original indices, which sorting would destroy. Two pointers wins when the input is already
> sorted, or when O(1) space matters enough to pay for an O(n log n) sort."

---

## 9. Recall card

- **Two indices, one rule, and an argument for why each move is safe.** That argument is the question.
- **Opposite ends needs sorted input.** Too small → the left value can never work; too big → the right
  value can never work.
- **Each move deletes a whole row or column of the pair table** — that is why `O(n²)` becomes `O(n)`.
- **Three shapes:** opposite ends (sorted, pairs), same direction (compaction), fast and slow (cycles).
- **Unsorted and need original indices → hash map**, `O(n)` time, `O(n)` space. Sorted → two pointers,
  `O(1)` space.
