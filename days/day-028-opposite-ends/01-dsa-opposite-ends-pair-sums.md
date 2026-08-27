---
day: 28
track: dsa
title: "Opposite ends: pair sums on a sorted array"
phase: "Two pointers and sliding window"
status: written
---

# Day 028 · DSA — Opposite ends: pair sums on a sorted array

**After today you can:** You can find a pair summing to a target in O(n) and argue that you miss nothing.

**The interviewer asks it as:** *Find two numbers in a sorted array that add up to the target.*

---

## 1. What this is, and why they ask it

Yesterday introduced two pointers and the elimination argument. Today is the same technique used
properly, and the emphasis moves to the harder half: **proving you have not missed anything**.

That distinction matters more than it sounds. Yesterday's argument said *why each individual move is
safe*. Today's says *why, when the two indices meet and you have found nothing, there is genuinely
nothing to find* — even though you examined about `n` pairs out of `n(n-1)/2`. Those are different
claims, and the second is the one an interviewer probes with *"how do you know you didn't skip the
answer?"*

The technique also stops being one problem today. The same two-indices-from-opposite-ends shape solves
*find one pair*, *find all pairs*, *find the closest pair*, *count the pairs*, *three-sum*, and *sorted
squares* — six recognisably different questions with the same skeleton and different move rules. Being
able to adapt the skeleton rather than recall six solutions is what the day is for.

`3Sum` (LeetCode 15) in particular is one of the most-asked medium problems anywhere, and its real
difficulty is not the algorithm — it is producing distinct triples without duplicates, which is §7.

---

## 2. The story

Bashir has been painting houses for twenty-six years and the part he is most careful about is not the
painting.

A flat in the new block near the water tank needs its front room done, and he has worked out that it
will take twelve litres — two coats, and he has measured the walls twice because he always does. The
shop at the corner sells the same paint in tins of one, two, four, five, ten and twenty litres, and
they stand on the shelf in that order, smallest on the left.

He wants exactly twelve, and he wants it in exactly two tins. Not three, because the third opening is
where colour differences show, and not one big tin with waste left over, because the owner is paying
for what is opened.

So he stands in front of the shelf and puts one hand on the one-litre and the other on the twenty.

Twenty-one. Too much. And here he does not just move on — he says the thing he always says, which is
that the twenty is finished. It is already sitting with the smallest tin on the shelf and it is still
over, so there is nothing on that shelf that will bring it down to twelve. Never mind about pairing it
with the four or the five; those are bigger than the one, so they are worse.

Hand off the twenty, on to the ten.

One and ten is eleven. Not enough. So now the one-litre tin is finished, for the mirror reason — it is
sitting with the biggest thing left and still falling short, and everything else on that shelf is
smaller than the ten.

Hand off the one, on to the two. Two and ten is twelve, and he is done.

The bit that took him years to be comfortable with is the other outcome. Some days the number does not
come out — the owner wants exactly thirteen and there is no pair on that shelf that makes thirteen.
Bashir's hands meet in the middle and he turns round and tells the man, flatly, that it cannot be done
in two tins. He does not go back and check the combinations he skipped, and he is not being lazy.
Every pair he did not try had one tin in it that he had already proved could not work with anything.

---

## 3. The idea in plain English

Bashir's two hands are `left` and `right`. Him being willing to say *"it cannot be done"* without going
back is the completeness argument, and it is what today exists to install.

### The skeleton

```python
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

Nine lines, and every variant today changes only what happens in those three branches.

### The property that holds all the way through

Say this sentence and the rest follows:

> **At every moment, if a valid pair exists anywhere in the array, both of its elements lie between
> `left` and `right` inclusive.**

That is called an **invariant** — something true before the loop starts, still true after every turn,
and therefore true when the loop ends.

**True at the start**, because `left` and `right` are the two ends and everything is between them.

**Still true after a move.** Suppose the total is too small and we advance `left`. The only pairs we
lose are the ones containing `nums[left]`. Every one of those pairs is `nums[left] + something`, where
`something` is at most `nums[right]` — because the array is sorted and `nums[right]` is the largest
value still in range. So every lost pair sums to at most `nums[left] + nums[right]`, which we just
measured and found **less than the target**. None of them could have been the answer. The same argument
mirrored covers advancing `right`.

**Therefore, when the loop ends** with `left` and `right` having met, the range between them is empty,
so by the invariant no valid pair exists anywhere. Returning "not found" is not a guess.

That is the whole proof, and it is three sentences. **Interviewers ask for it, and almost nobody has
it ready.**

### Why sortedness is load-bearing

The step "every `something` is at most `nums[right]`" is the only place sortedness is used — and it is
used to eliminate an entire row of pairs at once. On an unsorted array it is false, so nothing about
the argument survives. That is why *"is it sorted?"* is the first question, every time.

### The six variants, and what changes

The skeleton stays. Only the branches move.

| Problem | On `==` | On `<` | On `>` |
|---|---|---|---|
| **find one pair** | return | `left += 1` | `right -= 1` |
| **find all pairs** | record, then move **both**, then skip duplicates | `left += 1` | `right -= 1` |
| **count pairs ≤ target** | — | add `right - left`, then `left += 1` | `right -= 1` |
| **closest pair** | return | update best, `left += 1` | update best, `right -= 1` |
| **3Sum** | record, move both, skip duplicates | `left += 1` | `right -= 1` |
| **sorted squares** | — | compare magnitudes, write from the **back** | |

Two of those deserve unpacking.

### Finding *all* pairs, and the duplicate problem

On a hit you must move **both** indices. Moving only one gives you the same pair again — `nums[left]`
is unchanged and its partner requirement is unchanged, so nothing has progressed.

Then you must skip repeats:

```python
if total == target:
    out.append((nums[left], nums[right]))
    left += 1
    right -= 1
    while left < right and nums[left] == nums[left - 1]:
        left += 1
    while left < right and nums[right] == nums[right + 1]:
        right -= 1
```

On `[1, 1, 2, 2, 3, 3, 4, 4]` with target 5, the distinct pairs are `(1,4)` and `(2,3)`. Without the
two skip loops you get `(1,4)` twice and `(2,3)` twice. **Ask whether the interviewer wants distinct
pairs or all index pairs** — they are different questions and the second is a counting problem.

### Counting pairs, which is the neat one

*"How many pairs sum to at most the target?"* When `nums[left] + nums[right] <= target`, then
**every** element between `left` and `right` also works with `nums[left]`, because they are all at most
`nums[right]`. So that single comparison contributes `right - left` pairs at once:

```python
if nums[left] + nums[right] <= target:
    count += right - left
    left += 1
else:
    right -= 1
```

That is the same "one move settles a whole row" idea, used to *count* rather than to *discard*. It is
the seed of the `right - left + 1` counting trick that runs through the window problems on
[day 034](../day-034-at-most-k/README.md).

### 3Sum: fix one, two-pointer the rest

There is no three-pointer version, because no elimination argument works on three moving indices at
once. So:

1. **Sort** the array.
2. **Loop** over the first element, `i`.
3. **Two-pointer** the range `i+1 .. n-1` looking for `-nums[i]`.

`O(n log n) + O(n²)` = `O(n²)`, which is the expected answer. The difficulty is entirely duplicates,
and there are three separate places to handle them — §7.

### Sorted squares: opposite ends, writing backwards

*"Given a sorted array that may contain negatives, return the squares in sorted order."*

`[-4, -1, 0, 3, 10]` squares to `[16, 1, 0, 9, 100]`, which is not sorted. But the **largest square is
always at one end or the other**, because the largest magnitude is. So compare magnitudes at the two
ends, take the bigger, and **write it into the output from the back**.

That is opposite-ends two pointers combined with the write-from-the-back idea from
[day 018](../day-018-arrays-revision/README.md), and it is `O(n)` where sorting the squares would be
`O(n log n)`.

Note `while left <= right` here, not `<`. The single middle element still has to be written, because
this variant is about covering every position rather than about forming pairs of distinct elements.
**The loop condition follows from what the problem is counting**, not from habit.

---

## 4. The picture

The invariant, drawn. The shaded region is where a valid pair could still be:

```
  start          [ 1  2  4  5  10  20 ]      target 12
                   ^                ^
                   L                R        1 + 20 = 21 > 12

  everything eliminated by moving R:
                 [ 1  2  4  5  10 ][20]      every pair containing 20 sums to
                                    xxxx     at least 1 + 20 = 21 > 12

  after R--      [ 1  2  4  5  10 ]
                   ^            ^
                   L            R            1 + 10 = 11 < 12

  everything eliminated by moving L:
                 [1][ 2  4  5  10 ]          every pair containing 1 sums to
                  xx                         at most 1 + 10 = 11 < 12

  after L++      [ 2  4  5  10 ]
                   ^         ^
                   L         R               2 + 10 = 12  ->  found
```

**What to notice:** each `xxxx` block is a whole set of pairs discarded by one comparison, and the
reason is written next to it. When the two hands meet with nothing found, the un-eliminated region is
empty — which is the completeness argument made visual.

The pair table, showing coverage:

```
        1     2     4     5    10    20
   1    -   1+2   1+4   1+5  1+10  1+20   <-- one L++ deletes this entire row
   2    -     -   2+4   2+5  2+10  2+20
   4    -     -     -   4+5  4+10  4+20
   5    -     -     -     -  5+10  5+20
  10    -     -     -     -     -  10+20
  20    -     -     -     -     -     -
                                      ^
                              one R-- deletes this entire column

   15 pairs in the table.  The two-pointer walk touched 3 of them
   and eliminated the other 12 with an argument.
```

**What to notice:** 3 examined, 12 eliminated, 0 missed. At `n = 10,000` it is 10,000 examined and
about 50 million eliminated.

Sorted squares, where the writing goes backwards:

```
  input   [ -4  -1   0   3  10 ]     output  [ _  _  _  _  _ ]
             ^              ^                              ^
             L              R                            write

  |−4| = 4, |10| = 10  ->  10 wins   output  [ _  _  _  _ 100 ]   R--, write--
  |−4| = 4, | 3| = 3   ->   4 wins   output  [ _  _  _ 16 100 ]   L++, write--
  |−1| = 1, | 3| = 3   ->   3 wins   output  [ _  _  9 16 100 ]   R--, write--
  |−1| = 1, | 0| = 0   ->   1 wins   output  [ _  1  9 16 100 ]   L++, write--
  L == R on the 0                    output  [ 0  1  9 16 100 ]
```

**What to notice:** the write index moves backwards from the end, because the **largest** value is the
one you can identify first. Filling forwards would need the smallest, which is in the middle and is
exactly the thing you do not know.

---

## 5. The code, built step by step

### The base case, with the 1-indexing trap

LeetCode 167 wants positions numbered from 1, not 0.

```python
def two_sum_ii(nums: list[int], target: int) -> list[int]:
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left + 1, right + 1]      # the problem is 1-indexed
        if total < target:
            left += 1
        else:
            right -= 1
    return []
```

The `+ 1`s are the only difference from yesterday's version and they are worth a sentence in the
interview — *"this one is 1-indexed, so I'll adjust on the way out."* Reading the return format before
writing the return statement is a habit worth having.

### All distinct pairs

The move on a hit is the interesting part.

```python
if total == target:
    out.append((nums[left], nums[right]))
    left += 1
    right -= 1
```

**Both**, because moving one leaves the other looking for the same partner value and you emit the same
pair again.

```python
    while left < right and nums[left] == nums[left - 1]:
        left += 1
    while left < right and nums[right] == nums[right + 1]:
        right -= 1
```

Then skip past repeats of the two values you just used. `nums[left - 1]` is the value you just
consumed, so this walks forward while the value is unchanged. Both loops keep the `left < right` guard,
for the same reason the palindrome skip loops did on
[day 023](../day-023-palindromes/README.md) — a block of identical values could otherwise run an index
off the end.

### Counting pairs at or under a target

```python
count = 0
left, right = 0, len(nums) - 1
while left < right:
    if nums[left] + nums[right] <= target:
        count += right - left          # all of nums[left+1..right] also work with nums[left]
        left += 1
    else:
        right -= 1
```

`right - left` and not `right - left + 1`, because `nums[left]` cannot pair with itself. Say the
justification while you write it: *"if the largest partner works, every smaller partner works too, so I
can count them all at once."*

### 3Sum, and the three duplicate guards

```python
nums = sorted(nums)
for i in range(len(nums) - 2):
    if i > 0 and nums[i] == nums[i - 1]:
        continue                       # guard 1: same first element as last time
    if nums[i] > 0:
        break                          # optimisation: sorted, so no three positives sum to 0
```

Guard 1 is the one people forget. Without it, `[-1, -1, 0, 1]` produces the triple `[-1, 0, 1]` twice.

```python
    left, right = i + 1, len(nums) - 1
    while left < right:
        total = nums[i] + nums[left] + nums[right]
        if total == 0:
            out.append([nums[i], nums[left], nums[right]])
            left += 1
            right -= 1
            while left < right and nums[left] == nums[left - 1]:
                left += 1              # guard 2
            while left < right and nums[right] == nums[right + 1]:
                right -= 1             # guard 3
        elif total < 0:
            left += 1
        else:
            right -= 1
```

Three guards in three different places, for three different repetitions. **Being able to say what each
one prevents, with the input it prevents it on, is the whole of this question.**

### Sorted squares

```python
n = len(nums)
out = [0] * n
left, right, write = 0, n - 1, n - 1
while left <= right:
    a, b = abs(nums[left]), abs(nums[right])
    if a > b:
        out[write] = a * a
        left += 1
    else:
        out[write] = b * b
        right -= 1
    write -= 1
```

`left <= right`, because every position must be filled including the middle one. And the write index
starts at the end, because the value you can identify with certainty is the **largest**.

### The complete solutions

```python
def two_sum_ii(nums: list[int], target: int) -> list[int]:
    """LeetCode 167. Sorted input, 1-INDEXED output. O(n) time, O(1) space."""
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            left += 1
        else:
            right -= 1
    return []


def all_pairs(nums: list[int], target: int) -> list[tuple[int, int]]:
    """Every DISTINCT pair of values summing to target. Sorted input."""
    out: list[tuple[int, int]] = []
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            out.append((nums[left], nums[right]))
            left += 1
            right -= 1                                   # move BOTH, or you re-emit
            while left < right and nums[left] == nums[left - 1]:
                left += 1
            while left < right and nums[right] == nums[right + 1]:
                right -= 1
        elif total < target:
            left += 1
        else:
            right -= 1
    return out


def count_pairs_at_most(nums: list[int], target: int) -> int:
    """How many index pairs (i < j) have nums[i] + nums[j] <= target. Sorted input."""
    count = 0
    left, right = 0, len(nums) - 1
    while left < right:
        if nums[left] + nums[right] <= target:
            count += right - left      # every partner between left+1 and right also works
            left += 1
        else:
            right -= 1
    return count


def three_sum(nums: list[int]) -> list[list[int]]:
    """LeetCode 15. Distinct triples summing to zero. O(n^2) after an O(n log n) sort."""
    nums = sorted(nums)
    out: list[list[int]] = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue                                     # guard 1: repeated first element
        if nums[i] > 0:
            break                                        # sorted: no three positives sum to 0
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                out.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1                            # guard 2
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1                           # guard 3
            elif total < 0:
                left += 1
            else:
                right -= 1
    return out


def three_sum_closest(nums: list[int], target: int) -> int:
    """LeetCode 16. The triple sum nearest to target. Same skeleton, tracking a best."""
    nums = sorted(nums)
    best = nums[0] + nums[1] + nums[2]
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if abs(total - target) < abs(best - target):
                best = total
            if total == target:
                return total
            if total < target:
                left += 1
            else:
                right -= 1
    return best


def sorted_squares(nums: list[int]) -> list[int]:
    """LeetCode 977. Sorted input with negatives. O(n) by writing from the BACK."""
    n = len(nums)
    out = [0] * n
    left, right, write = 0, n - 1, n - 1
    while left <= right:               # <=, because every position must be filled
        a, b = abs(nums[left]), abs(nums[right])
        if a > b:
            out[write] = a * a
            left += 1
        else:
            out[write] = b * b
            right -= 1
        write -= 1
    return out


if __name__ == "__main__":
    print([two_sum_ii(a, t) for a, t in (([2, 7, 11, 15], 9), ([2, 3, 4], 6), ([-1, 0], -1))])
    # [[1, 2], [1, 3], [1, 2]]

    print(all_pairs([1, 1, 2, 2, 3, 3, 4, 4], 5))    # [(1, 4), (2, 3)]
    print(all_pairs([0, 0, 0, 0], 0))                # [(0, 0)]
    print(all_pairs([1, 2, 3, 4, 5], 6))             # [(1, 5), (2, 4)]

    print(count_pairs_at_most([1, 2, 3, 4], 5))      # 4  -> (1,2)(1,3)(1,4)(2,3)

    print(three_sum([-1, 0, 1, 2, -1, -4]))          # [[-1, -1, 2], [-1, 0, 1]]
    print(three_sum([0, 0, 0, 0]))                   # [[0, 0, 0]]
    print(three_sum([0, 1, 1]))                      # []

    print(three_sum_closest([-1, 2, 1, -4], 1))      # 2

    print(sorted_squares([-4, -1, 0, 3, 10]))        # [0, 1, 9, 16, 100]
    print(sorted_squares([-7, -3, 2, 3, 11]))        # [4, 9, 9, 49, 121]
```

---

## 6. What it costs

### The base case

Every turn moves exactly one index, `left` only forward and `right` only backward, and they start `n-1`
apart. So the loop runs at most `n - 1` times, each turn doing one addition and at most two
comparisons.

**O(n) time. O(1) extra space.**

Against the nested loop's `n(n-1)/2` pair checks, measured on inputs where no pair exists:

```
n =  1,000   two pointers 0.000067 s   nested loop 0.0225 s      334x
n =  5,000   two pointers 0.000332 s   nested loop 0.5923 s    1,782x
n = 10,000   two pointers 0.000679 s   nested loop 2.3448 s    3,454x
```

The ratio doubling with `n` is the `O(n)`-versus-`O(n²)` signature.

### `all_pairs` and `count_pairs_at_most`

Same structure, so still **O(n) time**. The duplicate-skip loops do not change that: they only ever
move `left` forward and `right` backward, so across the whole run the two indices still travel at most
`n` positions in total. **Nested `while` loops do not imply `O(n²)` — count the travel, not the
nesting.**

`all_pairs` is `O(k)` extra space for `k` output pairs; `count_pairs_at_most` is `O(1)`.

### `three_sum`

Sorting is `O(n log n)`. The outer loop runs `n - 2` times and each inner two-pointer scan is `O(n)`,
so the scanning is `O(n²)`, which dominates.

**O(n²) time.** Space is `O(1)` beyond the output if you may sort in place, or `O(n)` if you must copy
first — and `O(k)` for the `k` triples returned.

Concretely, at `n = 3,000`:

```
brute force, all triples : 3,000 choose 3 ≈ 4.5 billion    — not runnable
sort + two pointers      : ~9 million inner steps          — a few seconds in Python
```

**There is no known sub-quadratic algorithm for 3Sum**, and saying so is a better answer than
searching for one. It is a well-studied problem, and `O(n²)` is the expected bound.

### `sorted_squares`

One pass, `n` writes: **O(n) time**, `O(n)` for the output and `O(1)` beyond it.

The obvious alternative — square everything, then sort — is `O(n log n)`. At `n = 1,000,000` that is
about 20 million comparisons against 1 million steps, so roughly 20×. Worth mentioning as the
one-liner you are choosing not to use.

### The number to have ready

> Two pointers examines about `n` pairs and eliminates the other `n(n-1)/2 − n` with an argument. On
> `[1,2,4,5,10,20]` that is 3 pairs examined out of 15. At `n = 10,000` it is 10,000 out of 50 million,
> measured at about 3,500× faster.

---

## 7. The traps

### The near-miss: moving only one index on a hit

```python
if total == target:
    out.append((nums[left], nums[right]))
    left += 1                          # right not moved
```

On `[1, 2, 3, 4]` with target 5 this finds `(1,4)`, then advances to `2 + 4 = 6`, which is too big, so
`right` drops to 3 and it finds `(2,3)`. It happens to work here. Now try `[1, 1, 4, 4]` with target 5:
you get `(1,4)`, then `left` moves to the second 1, and `1 + 4 = 5` again — the same pair of *values*
emitted twice.

**On a hit, both indices must move**, because the pair is consumed. Then the skip loops handle repeats.

### The near-miss: forgetting duplicate skipping in 3Sum

```python
for i in range(len(nums) - 2):
    # no guard on nums[i] == nums[i-1]
    ...

print(three_sum([-1, 0, 1, 2, -1, -4]))
```

```
[[-1, -1, 2], [-1, 0, 1], [-1, 0, 1]]
```

`[-1, 0, 1]` appears twice, because after sorting there are two `-1`s and the outer loop runs the same
two-pointer scan for each. The problem asks for **distinct** triples.

Three separate guards are needed and they are not interchangeable:

- **Guard 1**, on the outer element: `if i > 0 and nums[i] == nums[i-1]: continue`.
- **Guards 2 and 3**, after a hit, skipping repeats of `left` and `right`.

The input that finds a missing guard 1 is `[-1,0,1,2,-1,-4]`. The input for guards 2 and 3 is
`[-2,0,0,2,2]`. Test with both.

### The near-miss: not sorting before 3Sum

The two-pointer scan inside 3Sum requires the sub-array to be sorted, for exactly the reason from §3.
Skip the sort and it silently returns incomplete results — no error, just missing triples. And the
duplicate guards also depend on sortedness, because they assume equal values are adjacent.

### The near-miss: 0-indexed output on a 1-indexed problem

LeetCode 167 wants `[1, 2]` for the first two elements. Returning `[0, 1]` is a wrong answer for
completely correct code, and it costs a submission. **Read the return format before writing the
return.**

### The near-miss: `left < right` in sorted squares

```python
while left < right:                    # should be <=
```

The middle element is never written, so `sorted_squares([-1, 0, 1])` returns `[1, 0, 1]` — position 1
keeps its initial `0` by accident, which happens to look plausible. On `[-4, -1, 0, 3, 10]` you get
`[0, 1, 9, 16, 100]`, still correct by luck because the middle value is 0.

**The loop condition depends on what you are covering.** Pair problems want `<` because the two must be
distinct elements. Position-filling problems want `<=` because every position needs a value. Say which
one you are doing.

### The near-miss: assuming the input is sorted when it is not

```python
print(all_pairs([3, 1, 4, 2], 5))
```

```
[]
```

There are two pairs summing to 5. Nothing is found and nothing errors, because the elimination
argument is false on unsorted input. **Sortedness is a precondition.** If the problem does not
guarantee it, sort — and then say what that costs, and that it destroys original indices.

### The contract corner: distinct values or distinct positions?

*"Find all pairs summing to the target"* is ambiguous. On `[1, 1, 4, 4]` with target 5:

- **Distinct value pairs:** one answer, `(1, 4)`.
- **Distinct index pairs:** four answers — each of the two 1s with each of the two 4s.

The second is a **counting** problem and two pointers with skip loops gives the wrong answer for it;
you multiply the run lengths instead. Ask which one is wanted.

---

## 8. In the interview

### How it gets asked

- *"Find two numbers in a sorted array that add up to the target."* — LeetCode 167. Check the indexing.
- *"How do you know you haven't missed a pair?"* — the completeness question, and the reason today
  exists.
- *"Now find all such pairs."* — where duplicate handling appears.
- *"3Sum."* — LeetCode 15, and the duplicates are the question.
- *"Square a sorted array containing negatives, keeping it sorted."* — LeetCode 977, the
  write-from-the-back variant.

### What to say out loud, in the first ninety seconds

1. **Confirm sortedness and the return format.** *"It's sorted — good. And do you want indices or
   values, and are indices 0-based or 1-based?"*
2. **State the brute force and its cost.** *"Every pair is O(n²)."*
3. **Name the shape.** *"Two indices at opposite ends, moving inwards."*
4. **Give the move rules with the reason attached.** *"Too small, advance left: that value is paired
   with the largest available and still short, so it can't work with anything. Too large, retreat
   right, by the mirror argument."*
5. **Give the completeness argument, unprompted.** *"The property that holds throughout is that any
   valid pair lies between the two indices. Each move only discards pairs I've just proved can't
   reach the target. So when they meet with nothing found, there genuinely is nothing."*
6. **Give the cost and the space.** *"O(n) time, O(1) space."*
7. **Say what would change your approach.** *"If it weren't sorted I'd use a hash map — O(n) time,
   O(n) space, and it keeps the original indices."*

### The follow-ups

**"How do you know you haven't skipped the answer?"**
Because of an invariant I can state precisely: at every point in the loop, if a valid pair exists
anywhere in the array, both of its elements are between `left` and `right`. It is true at the start
because those are the two ends. It stays true across a move: when I advance `left` because the sum was
too small, the only pairs I lose are those containing `nums[left]`, and every one of them sums to at
most `nums[left] + nums[right]` — since the array is sorted, `nums[right]` is the largest partner
available — which I just measured as below the target. So every discarded pair was already known to
fall short. The mirror argument covers retreating `right`. Therefore when the two meet, the range
between them is empty, and by the invariant no valid pair exists. That is a proof rather than a
hope, and the one place it uses sortedness is the claim that `nums[right]` is the largest remaining
partner.

**"Now return all the pairs, not just one."**
Two changes. On a hit I move **both** indices rather than one, because the pair is consumed — moving
only `left` leaves `right` on the same value and I would emit the same pair again on the next equal
element. Then I skip forward over repeats of both values I just used, so `[1,1,2,2,3,3,4,4]` with
target 5 gives `(1,4)` and `(2,3)` once each rather than twice. Before writing any of that I would ask
what "all pairs" means: distinct pairs of **values**, or distinct pairs of **positions**. On
`[1,1,4,4]` the first has one answer and the second has four, and the second is really a counting
problem — I would multiply the lengths of the two runs rather than emitting pairs. It is a genuine
ambiguity and worth three seconds.

**"3Sum. And why can't you use three pointers?"**
Because there is no elimination argument for three simultaneously moving indices — with two, "too
small" identifies exactly one element that can be discarded, and with three, a sum being too small
tells you nothing about which of the three to move. So the structure is: sort, then fix the first
element with an outer loop, then run two pointers on the remainder looking for its negation. That is
`O(n log n)` for the sort plus `O(n²)` for the scanning, so `O(n²)` overall, and there is no known
sub-quadratic algorithm for this problem. The real difficulty is duplicates, and there are three
separate guards in three places: skip a repeated outer element, and after recording a triple, skip
repeated values at both `left` and `right`. Each one prevents a different repetition, and I would name
the input that catches each.

**"Square a sorted array with negatives, keeping it sorted, in O(n)."**
Squaring destroys the order because a large negative squares to a large positive. But the **largest**
square is always at one end or the other, since the largest magnitude is at one end. So I use two
indices at the ends, compare the absolute values, take the bigger, square it, and write it into the
output starting from the **back**. Then move whichever index I consumed. Writing backwards is the key
move — I can identify the largest remaining value with certainty at each step, and the smallest is
somewhere in the middle where the sign changes, which is exactly the thing I do not know. `O(n)` time
against `O(n log n)` for square-then-sort, which at a million elements is about 20 times fewer
operations. And the loop is `left <= right` here, not `<`, because every output position must be
filled including the middle one.

### A model answer

> "First: it's sorted, and do you want the indices or the values? And if indices, 0-based or 1-based?
>
> ...Indices, 1-based. Noted — I'll adjust on the way out.
>
> The brute force checks every pair, which is n choose 2, so O(n²). Because it's sorted I can do it in
> one pass with two indices, one at each end, moving inwards.
>
> ```python
> def two_sum(nums: list[int], target: int) -> list[int]:
>     left, right = 0, len(nums) - 1
>     while left < right:
>         total = nums[left] + nums[right]
>         if total == target:
>             return [left + 1, right + 1]
>         if total < target:
>             left += 1
>         else:
>             right -= 1
>     return []
> ```
>
> The move rules each have a reason. If the sum is too small, `nums[left]` is the smallest value still
> available and it's currently paired with the largest one available — that's its best case, so if it
> falls short, no pair containing it can reach the target, and I discard it. Too large is the mirror
> argument on `nums[right]`.
>
> The part I'd want to be explicit about is why this doesn't miss anything, because that's the
> interesting claim. The invariant is: at every moment, if a valid pair exists anywhere, both of its
> elements are between `left` and `right`. True at the start, since those are the ends. Preserved by
> each move, because the pairs I discard are exactly the ones I've just proved fall on the wrong side
> of the target. So when the indices meet with nothing found, the remaining range is empty and there
> genuinely is no such pair — that's a proof, not an assumption.
>
> Sortedness is used in exactly one place: the claim that `nums[right]` is the largest partner still
> available. That's why the whole thing collapses on unsorted input — it returns nothing, with no
> error, which is the dangerous kind of wrong.
>
> Cost: at most n−1 turns, each doing constant work, so O(n) time and O(1) extra space. Against the
> nested loop that's about 3,500 times faster at ten thousand elements, and the gap doubles every time
> n doubles.
>
> Edge cases: fewer than two elements, where the loop never runs and I return empty; and equal values,
> where `left < right` correctly allows two different positions holding the same number. If the array
> weren't sorted I'd switch to a hash map — same O(n) time, O(n) space, and it preserves the original
> indices, which sorting would destroy."

---

## 9. Recall card

- **The invariant:** any valid pair lies between `left` and `right`. Each move discards only pairs
  already proved impossible — so meeting with nothing found is a **proof**, not a guess.
- **Sortedness is used once:** `nums[right]` is the largest remaining partner. That is the whole
  dependency.
- **On a hit, move both indices**, then skip repeats of both values. Otherwise you emit the same pair
  twice.
- **3Sum = sort, fix one, two-pointer the rest.** `O(n²)`, three duplicate guards in three places.
- **`left < right` for pairs; `left <= right` when filling positions**, as in sorted squares, where you
  write from the back.
