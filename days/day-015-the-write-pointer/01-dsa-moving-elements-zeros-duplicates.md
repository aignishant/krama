---
day: 15
track: dsa
title: "Moving elements: zeros, duplicates, and the write pointer"
phase: "Arrays"
status: written
---

# Day 015 · DSA — Moving elements: zeros, duplicates, and the write pointer

**After today you can:** You can compact an array in place with a read index and a write index.

**The interviewer asks it as:** *Move all zeros to the end while keeping the order of the other elements.*

---

## 1. What this is, and why they ask it

Some questions ask you to throw things out of a list and keep the rest packed together at the
front. Remove the zeros. Remove every copy of the number 3. Remove the duplicates. In every one
of them you walk the list once with **two counters instead of one**: a *read* counter that visits
every position, and a *write* counter that only moves when you decide to keep something.

That is the whole technique, and it has a name: the **write pointer**, sometimes called in-place
compaction. The read counter runs ahead. The write counter lags behind. The gap between them is
exactly how many elements you have thrown away so far.

Interviewers like this family because the obvious answers are both wrong in an interesting way.
Building a new list is easy but uses extra memory, and the question usually says *in place* to
forbid it. Deleting from the middle of the list as you go is worse: it is slow, and it silently
skips elements, and §7 shows exactly how. The write pointer is the answer that is fast, uses no
extra memory, and keeps the surviving elements in their original order.

This is a phone-screen staple — LeetCode 283, 27 and 26 are three of the most-asked easy problems
anywhere — and it is the direct ancestor of the two-pointer work that starts on
[day 027](../day-027-two-pointers-idea/README.md) and the read-write pointer day,
[day 029](../day-029-read-write-pointer/README.md). Learn it properly now and four later weeks
get easier.

---

## 2. The story

Padma keeps her books on a long shelf in the passage outside the bedrooms, standing in the order
she means to read them. Thirty places, and for years it was full enough that nothing fell over.

Over the last few months she has lent four of them out. Her sister took two, a neighbour took one,
and one went to her son's friend and has not come back. Where each book used to stand there is now
a gap, and the books on either side have started to lean into it. On Sunday morning she comes out
with her tea and finds two of them lying flat.

So she fixes it, and the way she fixes it is worth watching.

She does not take everything off the shelf. She stands at the left-hand end and puts her left hand
on the first place. Her right hand goes on the same place. Book there, so both hands move one to
the right. Book there again, both hands move again. On the fourth place there is nothing, so her
left hand stops and stays where it is, and only her right hand carries on.

Her right hand finds the next book two places along. She lifts it out, stands it in the place her
left hand is holding, and moves her left hand one to the right. Her right hand carries on from
where it had got to.

From then on her two hands are apart, and the distance between them is exactly the number of gaps
she has walked past. Every time her right hand finds a book, that book goes back to where her left
hand is and her left hand moves on one. Every time her right hand finds nothing, only her right
hand moves.

When her right hand runs off the end of the shelf, every book is standing packed against the
left-hand side, in the order they were in before, and all the empty space is in one block at the
right.

Then she counts what is left over at that end. Four empty places, which is exactly how many books
are out with people. She types the four names into her phone so she knows whom to ask.

---

## 3. The idea in plain English

Padma's shelf is an **array** — the fixed row of numbered boxes you met on
[day 009](../day-009-what-an-array-is/README.md). Her two hands are two variables holding
positions in it. Everything else follows from one rule about those hands.

### The two counters, and the one rule

Call the right hand `read` and the left hand `write`.

- `read` visits **every** position from left to right. It never skips and never stops early.
- `write` says **where the next kept element goes**. It moves only when you actually keep
  something.

The rule is: **`write` never runs ahead of `read`.** It starts equal to `read` and falls further
behind with every element you discard. That is why you can safely overwrite position `write` —
whatever used to be there has already been read and either kept or discarded. You are never
destroying data you still need. This is the sentence to say out loud in an interview, and it is
the reason the whole pattern is safe.

### What "in place" means, and why they ask for it

**In place** means you change the original list itself rather than building a new one, using only
a constant amount of extra memory — a few variables, no second list. You met the term on
[day 007](../day-007-space-complexity/README.md). Here it means two integer variables, whether
the list has 5 elements or 5 million.

The tempting non-answer is one line:

```python
kept = [x for x in items if x != 0]
```

That is correct, readable, and what you would write in real code if you were allowed a new list.
It is also `O(n)` extra space, and when the question says *in place*, it is precisely the answer
being ruled out.

### What "keeping the order" means

The surviving elements must come out in the same relative order they went in. If the input is
`[0, 1, 0, 3, 12]`, the answer is `[1, 3, 12, 0, 0]` — 1 before 3 before 12, exactly as before.
An answer of `[12, 3, 1, 0, 0]` has the right contents and is wrong.

An algorithm that preserves relative order like this is called **stable**. The word comes back on
[day 057](../day-057-stability-and-pythons-sort/README.md) when you meet stable sorting, and it
means the same thing there.

There is a faster-looking trick for this problem: whenever you meet a zero, swap it with the last
element and shrink the range. That does fewer writes, and it is the right answer to *some*
questions — but it scrambles the order, so it is the wrong answer to this one. Knowing which
question you are being asked is half the marks.

### Two phases, or one

Once `read` has run off the end, `write` holds a number with a clear meaning: **how many elements
you kept**. Positions `0` to `write - 1` are the survivors. Positions `write` to the end are
leftovers — old values that are still sitting there, already copied to their new homes.

What you do with that tail depends on the question:

- *Move the zeros to the end* — overwrite the tail with zeros. That is Padma noticing the four
  empty places at the right-hand end.
- *Remove all instances of a value* — you cannot shrink a fixed-size array, so you return `write`
  as the new length and the caller ignores everything past it. This is exactly what LeetCode 27
  and 26 ask for, and it confuses people the first time. Nothing is deleted. The count is the
  answer.

---

## 4. The picture

Padma's shelf, mid-walk. `w` is the left hand, `r` is the right hand.

```
 start           0    1    2    3    4
               +----+----+----+----+----+
               |  0 |  1 |  0 |  3 | 12 |
               +----+----+----+----+----+
                 ^
                w,r          both hands on position 0
```

`items[0]` is 0, so it is discarded. Only `r` moves.

```
                 0    1    2    3    4
               +----+----+----+----+----+
               |  0 |  1 |  0 |  3 | 12 |
               +----+----+----+----+----+
                 ^    ^
                 w    r      the hands have separated: one zero passed
```

`items[1]` is 1, so it is kept. It is copied to position `w`, then both hands move.

```
                 0    1    2    3    4
               +----+----+----+----+----+
               |  1 |  1 |  0 |  3 | 12 |
               +----+----+----+----+----+
                      ^    ^
                      w    r
```

Notice position 1 still says 1. That is the **leftover** — a stale copy that `r` has already
passed, so nobody will ever read it again. Beginners find this alarming. It is fine, and it is
the whole reason the pattern is safe.

Carry on to the end, keeping 3 and 12:

```
 after the loop  0    1    2    3    4
               +----+----+----+----+----+
               |  1 |  3 | 12 |  3 | 12 |
               +----+----+----+----+----+
                 |------------| |--------|
                    the kept     leftovers
                                ^
                                w = 3, so three elements were kept
```

Then fill from `w` to the end with zeros:

```
 finished        0    1    2    3    4
               +----+----+----+----+----+
               |  1 |  3 | 12 |  0 |  0 |
               +----+----+----+----+----+
```

**What to notice:** the gap between `w` and `r` only ever grows, and it grows by exactly one each
time you discard something. At the end, `r - w` is the number of zeros and `w` is the number of
non-zeros. Both facts drop out for free.

---

## 5. The code, built step by step

### The loop, in five lines

```python
write = 0
for read in range(len(items)):
    if items[read] != 0:
        items[write] = items[read]
        write += 1
```

Read it as English: *walk every position; if this one is worth keeping, put it at the write
position and move the write position on.* Five lines, and it is the entire pattern.

After this loop, `items[0:write]` holds the non-zero values in their original order, and `write`
holds how many there were. Run it on `[0, 1, 0, 3, 12]` and the list is now `[1, 3, 12, 3, 12]`.
Which is not the answer yet.

### The second phase: clear the tail

```python
for i in range(write, len(items)):
    items[i] = 0
```

`range(write, len(items))` covers exactly the leftover positions and nothing else. If nothing was
discarded, `write == len(items)` and this loop runs zero times, which is the correct behaviour
rather than a special case you have to test for.

Put the two together and you have LeetCode 283 solved.

### Why the copy is safe, one more time

The line that worries people is `items[write] = items[read]`. It writes into the same list you
are reading from. It is safe because `write <= read` always holds:

- Both start at 0, so they start equal.
- `write` only increases in the same step where `read` increases.
- `read` also increases in steps where `write` does not.

So `write` can never overtake `read`. When `write == read` the line copies a value onto itself,
which is harmless. When `write < read`, it overwrites a position `read` has already gone past.

### The swap version, which needs no second phase

```python
write = 0
for read in range(len(items)):
    if items[read] != 0:
        items[write], items[read] = items[read], items[write]
        write += 1
```

Instead of copying the non-zero forward and leaving a stale value behind, this **exchanges** it
with whatever is at `write` — which, if the two positions differ, is guaranteed to be a zero. The
zeros get pushed to the back as a side effect and the tail cleans itself. One pass, no second
loop.

Remember the tuple-swap from [day 013](../day-013-reverse-and-rotate/README.md): the whole
right-hand side is evaluated before anything is assigned, so this is a genuine exchange and not
two assignments that clobber each other.

Which of the two should you write? Say both exist. The copy-then-fill version generalises to
every question in this family; the swap version is specific to *move the discarded thing to the
end*, and it does more writes when the array is mostly non-zero, because it writes twice per kept
element instead of once. Interviewers are happy with either as long as you can say that sentence.

### Changing the test changes the problem

The only thing that varies across this whole family is the `if`. Everything else is identical.

```python
if items[read] != 0:                # move zeros to the end
if items[read] != target:           # remove every copy of `target`
if items[read] != items[write - 1]: # remove duplicates from a sorted list
```

That third one deserves a look. On a **sorted** list every duplicate sits next to its twin, so
"have I seen this before?" collapses to "is it the same as the last thing I kept?" — and the last
thing you kept is at `write - 1`. That is why it needs `write` to start at 1, with position 0
kept unconditionally:

```python
write = 1
for read in range(1, len(items)):
    if items[read] != items[write - 1]:
        items[write] = items[read]
        write += 1
```

Comparing against `items[write - 1]` and not against `items[read - 1]` is the detail that
matters. `read - 1` is the previous element you *looked at*; `write - 1` is the previous element
you *kept*. On a sorted list with no gaps they happen to agree, but the habit of comparing
against what you kept is what makes the "at most twice" variant below fall out in one line.

### The complete solutions

All five, ready to run.

```python
def move_zeroes(items: list[int]) -> None:
    """LeetCode 283. Move every 0 to the end, in place, keeping the order of the rest."""
    write = 0
    for read in range(len(items)):
        if items[read] != 0:
            items[write] = items[read]   # safe: write <= read, always
            write += 1
    for i in range(write, len(items)):   # the leftovers become zeros
        items[i] = 0


def move_zeroes_swap(items: list[int]) -> None:
    """The same thing in one pass. items[write] is a zero whenever write != read."""
    write = 0
    for read in range(len(items)):
        if items[read] != 0:
            items[write], items[read] = items[read], items[write]
            write += 1


def remove_value(items: list[int], target: int) -> int:
    """LeetCode 27. Returns the new length; items[:length] holds the survivors."""
    write = 0
    for read in range(len(items)):
        if items[read] != target:
            items[write] = items[read]
            write += 1
    return write


def remove_duplicates(items: list[int]) -> int:
    """LeetCode 26. items must be sorted. Returns the count of distinct values."""
    if not items:                        # write starts at 1, so guard the empty case
        return 0
    write = 1
    for read in range(1, len(items)):
        if items[read] != items[write - 1]:
            items[write] = items[read]
            write += 1
    return write


def remove_duplicates_twice(items: list[int]) -> int:
    """LeetCode 80. Sorted input; keep each value at most twice."""
    write = 0
    for x in items:
        if write < 2 or x != items[write - 2]:
            items[write] = x
            write += 1
    return write


if __name__ == "__main__":
    a = [0, 1, 0, 3, 12]
    move_zeroes(a)
    print(a)                                          # [1, 3, 12, 0, 0]

    b = [0, 1, 0, 3, 12]
    move_zeroes_swap(b)
    print(b)                                          # [1, 3, 12, 0, 0]

    c = [3, 2, 2, 3]
    k = remove_value(c, 3)
    print(k, c[:k])                                   # 2 [2, 2]

    d = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k = remove_duplicates(d)
    print(k, d[:k])                                   # 5 [0, 1, 2, 3, 4]

    e = [1, 1, 1, 2, 2, 3]
    k = remove_duplicates_twice(e)
    print(k, e[:k])                                   # 5 [1, 1, 2, 2, 3]
```

Look at `remove_duplicates_twice` for a moment. The test `x != items[write - 2]` asks *is this
value different from the one I kept two places ago?* If it is, this is at most the second copy and
it may stay. `write < 2` covers the first two elements, which are always allowed. Change the 2 to
a `k` and you have "keep each value at most k times" — the same five lines.

---

## 6. What it costs

### `move_zeroes`, the copy version

The first loop runs `len(items)` times — call it `n` — because `range(len(items))` visits every
position exactly once, whatever the values are. Each turn does one comparison, and at most one
assignment and one increment. That is a fixed, small amount of work, so the first loop is `n`
turns of constant work.

The second loop runs from `write` to `n`. If the list has `z` zeros in it, then `write` finished
at `n - z`, so the second loop runs `z` times. The worst case is an all-zeros list, where `z = n`.

Total: `n + z` turns, and `z` is at most `n`, so at most `2n`. Constant factors are dropped, so
this is **O(n) time**.

Space: `write`, `read` and `i` are three integers. Three integers whether the list has 5 elements
or 5 million. That is **O(1) extra space**. The list itself takes `O(n)`, but it was the input, so
you do not count it — the phrase to use is *O(1) extra space*, and saying "extra" is what shows
you know the difference.

### `move_zeroes_swap`

One loop, `n` turns, so **O(n) time** and **O(1) extra space** as well. The difference is in the
constant factor, not the class. Count the writes on `[1, 2, 3, 4]`, which has no zeros at all:

- Copy version: 4 copies, and each is a copy onto itself, since `write == read` throughout. Then
  the tail loop runs zero times. **4 writes.**
- Swap version: 4 swaps, and a swap is two writes. **8 writes.**

Now count on `[0, 0, 0, 1]`:

- Copy version: 1 copy, then 3 zero-fills. **4 writes.**
- Swap version: 1 swap. **2 writes.**

So neither is uniformly better. Mostly-zeros favours the swap, mostly-non-zeros favours the copy,
and both are `O(n)`. If an interviewer pushes on this, that is the honest answer, and the honest
answer is the one they want.

### What you are being compared against

The list-comprehension version — `[x for x in items if x != 0]` — is also `O(n)` time, but it is
`O(n)` extra space. The delete-as-you-go version in §7 is `O(n²)` time, because each `del` or
`remove` shifts everything after it down by one, which is the `O(n)` shifting cost you counted on
[day 011](../day-011-insert-and-delete/README.md). On a list of 100,000 zeros that is around five
billion moves, and it will not finish while the interviewer is watching.

---

## 7. The traps

### The near-miss: deleting while you loop

This is the version almost everybody writes first, and it looks completely reasonable.

```python
items = [0, 1, 0, 3, 12]
for x in items:
    if x == 0:
        items.remove(x)
print(items)
```

Predict the output before reading on. Most people say `[1, 3, 12]`, because both zeros are
removed. Run it:

```
[1, 3, 12]
```

It is right. Now run the same code on `[0, 0, 1]`:

```
[0, 1]
```

One of the zeros survived. Here is why. The loop keeps an internal counter of where it is. It
starts at position 0, finds a zero, and removes it — which slides every later element down one
place, so the zero that was at position 1 is now at position 0. The loop then moves its counter to
position 1, which now holds the 1. **The second zero was moved to a place the loop had already
been past, so it is never looked at.** Deleting from a list while looping over it skips exactly
the elements that follow a deletion.

This is a bug that passes its first test and fails in production, which is the worst kind. Never
delete from a list while iterating over it.

### The real error: the same idea with a counted loop

Try to fix it by looping over positions instead:

```python
nums = [1, 0, 0, 0]
for i in range(len(nums)):
    if nums[i] == 0:
        del nums[i]
print(nums)
```

```
Traceback (most recent call last):
  File "t2.py", line 3, in <module>
    if nums[i] == 0:
       ~~~~^^^
IndexError: list index out of range
```

`range(len(nums))` is worked out **once**, at the start, from the original length of 4. So `i`
still goes 0, 1, 2, 3 even though the list has shrunk to length 1 by then. The crash is actually
good news; the `remove` version's silent wrong answer is far more dangerous.

### The near-miss: forgetting the second phase

```python
def move_zeroes(items):
    write = 0
    for read in range(len(items)):
        if items[read] != 0:
            items[write] = items[read]
            write += 1
    return items

print(move_zeroes([0, 1, 0, 3, 12]))
```

```
[1, 3, 12, 3, 12]
```

The front is perfect and the back is rubbish. Those trailing `3, 12` are the leftovers from §4 —
stale copies that were never cleaned up. The tell is that the answer has the right length and the
right beginning, so a test that only checks `result[:3]` passes. Always compare the whole list.

### The near-miss: comparing against the wrong neighbour

In `remove_duplicates`, this looks equivalent and is not:

```python
if items[read] != items[read - 1]:   # wrong on the general problem
```

On a sorted list it gives the same answer, because you never skip a value. On an unsorted list, or
on the "at most twice" variant, it falls apart immediately, because `read - 1` may be an element
you discarded. Compare against **what you kept**, at `write - 1`, and the habit transfers.

### The one-character trap: forgetting to advance `write`

Leave out `write += 1` and every kept element lands on top of the last one. `[1, 2, 3]` becomes
`[3, 2, 3]` and `write` stays 0, so the function reports that it kept nothing. There is no error
message. This is why you say the rule out loud while writing the line: *keep it, then move the
write position on.*

---

## 8. In the interview

### How it gets asked

- *"Move all zeros to the end of the array while keeping the relative order of the non-zero
  elements. Do it in place."* — LeetCode 283, and the most common phrasing of all.
- *"Remove all instances of a given value from the array in place and return the new length."* —
  LeetCode 27. The words *return the new length* are the part people miss.
- *"This array is sorted. Remove the duplicates in place."* — LeetCode 26, and its harder sibling
  LeetCode 80, *allow each element at most twice*.
- *"Given an array, keep only the elements that pass some test, without allocating."* — the vague
  version. It is the same five lines with a different `if`.

### What to say out loud, in the first ninety seconds

1. **Pin the contract.** *"Two things before I start: does in place mean I cannot allocate a
   second array, and does the relative order of the surviving elements have to be preserved?"*
   Those two answers together decide which of three solutions is correct, so asking is not
   stalling.
2. **Name the pattern.** *"I'll use two indices over the same array — a read index that visits
   every position and a write index that says where the next kept element goes."*
3. **State the rule, because it is the reason it works.** *"The write index never overtakes the
   read index, so anything I overwrite has already been read. That is what makes writing into the
   array I am reading from safe."*
4. **Say what the write index means at the end.** *"When the loop ends, the write index is the
   number of elements I kept, and everything from there to the end is leftovers."*
5. **Say what you do about the tail.** *"For move-zeros I fill the tail with zeros in a second
   loop. For remove-element I just return the count, because you cannot shrink a fixed-size
   array."*
6. **Give the costs.** *"O(n) time — every position visited once, plus at most n more for the
   tail — and O(1) extra space, just two integers."*
7. **Name the thing you are not doing.** *"I am not deleting from the array as I go. Each delete
   shifts everything after it, so that is O(n²), and looping while deleting also skips elements."*

### The follow-ups

**"Can you do it without the second loop?"**
Yes — swap instead of copy. When the write index is behind the read index, whatever sits at the
write index is guaranteed to be a zero, because zeros are the only thing I have skipped past. So
exchanging the non-zero at the read index with the value at the write index moves the non-zero
forward and pushes the zero back in the same step, and the tail cleans itself. It is still `O(n)`
and `O(1)`. The trade is in the constant factor: the swap does two writes per kept element, so on
an array with very few zeros the copy-then-fill version does about half the writes. On an array
that is mostly zeros the swap version wins. I would mention both and pick the copy version by
default, because it generalises to remove-element and remove-duplicates unchanged.

**"What if the order didn't have to be preserved?"**
Then there is a cheaper answer. Keep an index at the end of the array; whenever the read index
finds a zero, swap it with the element at the end index and move the end index inwards, without
advancing the read index — you have to re-examine the value you just pulled in, because it might
also be a zero. That does one swap per zero rather than one write per non-zero, so on an array
with a handful of zeros it does a handful of writes instead of `n`. The output order is scrambled,
which is exactly why the original question forbids it. This is the same idea as LeetCode 27's
optimal solution.

**"Now the array is sorted and you want the duplicates gone. What changes?"**
Only the condition. On a sorted array all copies of a value are adjacent, so "have I seen this
already?" becomes "is it equal to the last value I kept?", which lives at `write - 1`. I keep
position 0 unconditionally, start the write index at 1, and start reading from 1. Same `O(n)` and
`O(1)`. If the array were *not* sorted I could not do it in `O(1)` space — I would need a set of
what I have seen, which is `O(n)` extra space, or I would sort first and lose the original order.

**"Make it keep each value at most twice."**
Compare against `items[write - 2]` instead of `items[write - 1]`, and let the first two elements
through unconditionally. If the current value differs from the one I kept two positions ago, then
at most one copy of it has been kept so far, so this one is allowed. Generalise the 2 to a `k` and
the same five lines solve "at most k times" — that is the version I would actually write, since it
costs nothing.

### A model answer

> "Two clarifications first. Does 'in place' rule out allocating a second array, and does the
> order of the non-zero elements have to be preserved?
>
> ...Right, in place and order preserved.
>
> Then I will use two indices walking the same array. A read index visits every position from left
> to right. A write index says where the next element I keep should go. Both start at zero.
>
> For each position, if the value is non-zero I copy it to the write index and advance the write
> index. If it is zero I do nothing, so the write index falls one further behind. The key property
> is that the write index never overtakes the read index — so every position I overwrite is one
> the read index has already passed, and I am never destroying a value I still need.
>
> When the loop ends, the write index equals the number of non-zero elements, and everything from
> there to the end is a stale leftover. So a second loop fills that range with zeros.
>
> ```python
> def move_zeroes(items: list[int]) -> None:
>     write = 0
>     for read in range(len(items)):
>         if items[read] != 0:
>             items[write] = items[read]
>             write += 1
>     for i in range(write, len(items)):
>         items[i] = 0
> ```
>
> On `[0, 1, 0, 3, 12]`: the 0 is skipped, 1 goes to position 0, the next 0 is skipped, 3 goes to
> position 1, 12 goes to position 2. The write index is 3, so positions 3 and 4 get zeroed, giving
> `[1, 3, 12, 0, 0]`.
>
> That is O(n) time — every position visited once, plus at most n more for the tail — and O(1)
> extra space, since it is two integers regardless of the array size.
>
> The version I deliberately avoided is deleting the zeros as I walk. Each delete shifts every
> later element down one, so that is O(n²), and if you delete while looping you also skip the
> element straight after each deletion, which gives a wrong answer rather than a slow one.
>
> If you want it in a single pass I can swap instead of copy, since the value at the write index
> is always a zero when the two indices differ. And if the order did not matter there is a cheaper
> version that swaps zeros with the last element instead."

---

## 9. Recall card

- **Two indices, one array.** `read` visits every position; `write` moves only when you keep one.
- **The rule:** `write <= read` always, so overwriting `items[write]` can never lose data.
- **At the end** `write` is the number kept; `items[write:]` is leftovers — zero it, or return
  `write` as the new length.
- **Only the `if` changes** across the family: `!= 0`, `!= target`, `!= items[write - 1]`,
  `!= items[write - 2]`.
- **O(n) time, O(1) extra space.** Never delete inside a loop — `O(n²)`, and it skips elements.
