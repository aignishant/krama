---
day: 35
track: dsa
title: "Choosing between two pointers and a window, under pressure"
phase: "Two pointers and sliding window"
status: written
---

# Day 035 · DSA — Choosing between two pointers and a window, under pressure

**After today you can:** You can look at a new problem and pick the right pattern in under a minute.

**The interviewer asks it as:** *You have thirty seconds. What pattern does this problem want?*

---

## 1. What this is, and why they ask it

Days 27 to 34 gave you six tools: opposite ends, read and write, fast and slow, the fixed window, the
variable window, and the counting window. Today teaches the skill that sits above all six —
**routing**. Given a problem you have never seen, you ask a fixed sequence of short questions, and
the answers land you on one tool before you have written a line.

No interviewer asks "please choose a pattern" out loud, but every interviewer scores it. The first
two minutes of a coding round are a routing test wearing a problem's clothes: candidates who route
correctly spend twenty-five minutes on code they already know; candidates who route wrongly discover
it at minute twenty, with nothing left to salvage. The questions in this lesson are the same ones
[day 026](../day-026-strings-revision/README.md) built for strings, extended to cover the pointer and
window families — and they are meant to be drilled until they run in under a minute, out loud.

---

## 2. The story

The out-patient queue at the district hospital starts forming before the gates open, and by eight
o'clock there are sixty people on the benches. Sister Philomena sits at the front desk, and she has
been sitting there for fourteen years.

She asks every person the same three questions, in the same order, and she needs about fifteen
seconds per person. Where is the trouble? How long has it been there? Is there fever with it? Then
she writes a room number on a slip of their token and calls the next person. Chest and breathing go
left to Room 2. Anything with fever goes straight back to Room 5. Old aches, longer than a month, go
upstairs. Cuts and swellings go to the dressing room. Anything that fits nowhere goes to Room 1,
the general physician, who can handle whatever walks in.

A trainee sat beside her in June, and the queue nearly died of it. The trainee listened to each
person's whole account — the uncle who had the same thing, what the first medicine was, what the
neighbour said — and tried to work out what was actually wrong with them. Twelve minutes for the
second person. The benches filled and the shouting started.

Philomena told her the thing she tells every trainee. You are not here to find out what is wrong.
The doctor finds out what is wrong, in the room, with time and instruments. You are here to find out
**which room**. Those are different jobs, and the second one only needs three answers.

And the order of the questions matters, she said. Fever first would be a waste — most people say no,
and you have learnt almost nothing. Where-is-the-trouble first cuts the whole building in half.

The trainee learnt it inside a week. The queue moves again. Sixty people, three questions each, and
by half past eight every one of them is sitting outside the right door — none of them treated yet,
every one of them in the right place to be.

---

## 3. The idea in plain English

Philomena's desk is the first two minutes of the interview. The rooms are the six patterns. Her three
fixed questions are the routing checklist below — and her deepest rule carries over whole: **routing
is a different job from solving.** You are not looking for the answer; you are looking for the door.

### The routing checklist

Ask these in order. Each answer eliminates rooms.

**Question 1 — is the answer about a contiguous run?**
Look for *subarray*, *substring*, *consecutive*, *run of*. Contiguous — from
[day 024](../day-024-substrings-vs-subsequences/README.md) — sends you to the **window side**.
Pairs, rearrangement in place, or cycles send you to the **pointer side**. This is
where-is-the-trouble: one question, half the building gone.

**Question 2 (window side) — fixed size or best size?**
"Every window of size k", "any k consecutive" → the **fixed window**,
[day 031](../day-031-fixed-window/README.md). "Longest", "shortest", "at most", "how many" → keep
going.

**Question 3 (window side) — best, or how many?**
"Longest" or "shortest" → the **variable window**,
[day 032](../day-032-variable-window/README.md), and immediately say which shape: minimise shrinks
while valid and records inside; maximise shrinks while invalid and records after. "How many" or
"count" → the **counting window** and the at-most trick,
[day 034](../day-034-at-most-k/README.md), and the line is `total += right - left + 1`.

**Question 4 (window side) — is the condition monotonic?**
The window's licence, from [day 032](../day-032-variable-window/README.md): growing must only push
the condition one way. A sum over values that can be **negative** is not monotonic — the window is
the wrong room, and the case goes to prefix sums, which arrive on
[day 037](../day-037-prefix-sums/README.md). Asking "can the values be negative?" out loud is
routing done where the interviewer can hear it.

**Question 5 (pointer side) — which of the three shapes?**
From [day 027](../day-027-two-pointers-idea/README.md): **sorted input and a pair to find** →
opposite ends, [day 028](../day-028-opposite-ends/README.md). **Keep some elements, discard others,
in place** → read and write, [day 029](../day-029-read-write-pointer/README.md). **A cycle, a
middle, or "no extra space" on something linked** → fast and slow,
[day 030](../day-030-fast-and-slow/README.md). And the escape: **unsorted, and the answer needs the
original indices** → not a pointer problem at all — a hash map, from
[day 021](../day-021-frequency-maps/README.md), because sorting would destroy the very thing you
must return.

### The tells, on one table

| The problem says | The room | Day |
|---|---|---|
| "longest substring such that..." | variable window, shape B | [032](../day-032-variable-window/README.md) |
| "smallest subarray with..." | variable window, shape A | [032](../day-032-variable-window/README.md) |
| "count the subarrays with..." | counting window, at-most trick | [034](../day-034-at-most-k/README.md) |
| "exactly k" | two at-most passes, subtract | [034](../day-034-at-most-k/README.md) |
| "maximum sum of any k consecutive" | fixed window | [031](../day-031-fixed-window/README.md) |
| "sorted array, find a pair" | opposite ends | [028](../day-028-opposite-ends/README.md) |
| "remove / move / compact in place" | read and write | [029](../day-029-read-write-pointer/README.md) |
| "cycle", "middle", "linked, O(1) space" | fast and slow | [030](../day-030-fast-and-slow/README.md) |
| "return the indices", unsorted | hash map, not pointers | [021](../day-021-frequency-maps/README.md) |
| "subsequence" | not this family at all | [024](../day-024-substrings-vs-subsequences/README.md) |
| sums that can go negative | prefix sums, not a window | [037](../day-037-prefix-sums/README.md) |

The last two rows are Philomena's Room 1 — the cases that fit nowhere on this desk, and knowing they
fit nowhere **is** the routing. Saying "this is a subsequence question, so none of my window tools
apply" is a correct and impressive answer.

### Routing is said out loud

The checklist is worthless run silently, because the interviewer cannot score what they cannot hear.
The sentence to practise is one breath long: *"The word subarray means contiguous, it says longest,
and the condition is a count of zeros which only grows as the window grows — so this is a variable
window, maximise shape, shrink while invalid, record after."* That sentence, before any code, is the
first ninety seconds done properly.

---

## 4. The picture

The desk, as a shape you can run in under a minute:

```
                     read the problem
                            |
              Q1: contiguous run involved?
              ("subarray", "substring", "consecutive")
                    |                    |
                   yes                   no
                    |                    |
         Q2: window size fixed?    Q5: which pointer shape?
            |            |              |
           yes           no        sorted + pair ......... opposite ends (028)
            |            |         keep/discard in place .. read + write  (029)
       fixed window   Q3: best     cycle / middle / O(1) .. fast + slow   (030)
          (031)       or count?    unsorted + indices ..... HASH MAP      (021)
                        |     |
                   longest/   "how many"
                   shortest       |
                        |     counting window,
                  variable    at-most trick (034)
                  window
                  (032)
                        |
              Q4: condition monotonic?
                    |         |
                   yes        no  (negatives in a sum)
                    |         |
                 proceed   PREFIX SUMS (037) — not a window
```

**What to notice:** two of the leaves are not rooms on this corridor at all. The checklist exists as
much to route you *away* from these patterns as toward them — the hash-map leaf and the prefix-sums
leaf are where wrong-pattern disasters are averted.

The cost of routing badly, drawn on the interview clock:

```
   0 min    5 min                    25 min              40 min
   |--------|------------------------|-------------------|
   read +   code the right pattern   test, fix, discuss  done
   route
                THE PLANNED ROUND

   0 min    5 min                20 min        40 min
   |--------|--------------------|-------------|
   read,    code the WRONG       realise it     rewrite from zero,
   no route pattern              cannot work    out of time
                THE UNROUTED ROUND
```

**What to notice:** the failure is not slower code — it is that the discovery arrives at minute
twenty, when there is no time left to spend the lesson it teaches.

---

## 5. The code, built step by step

Three problems, worked as routing transcripts. Read them for the questions asked before the code, not
for the code.

### Problem one — Merge Sorted Array

> *"You are given two sorted arrays. The first has empty space at its end, exactly enough to hold the
> second. Merge the second into the first, in place, keeping sorted order."* — LeetCode 88.

**Route it.** No "subarray", no condition on a run — Q1 says pointer side. Two sorted inputs walked
position by position, and an in-place destination — this is the two-indices family, one per array,
plus a write position, from [day 029](../day-029-read-write-pointer/README.md).

**Then the twist that makes it worth asking.** Writing from the front overwrites values of `nums1`
that have not been read yet. The free space is at the **back** — so walk everything backwards,
largest first, and the write position can never catch up with the unread data.

```python
write = m + n - 1
i = m - 1          # last real value in nums1
j = n - 1          # last value in nums2
```

Three positions, all starting at ends. `write` fills the array from the back; `i` and `j` point at
the largest unread value of each source.

```python
while j >= 0:
    if i >= 0 and nums1[i] > nums2[j]:
        nums1[write] = nums1[i]
        i -= 1
    else:
        nums1[write] = nums2[j]
        j -= 1
    write -= 1
```

The loop runs while `nums2` has anything left — if `nums2` is exhausted, the rest of `nums1` is
already in place. The `i >= 0` guard matters: without it, `nums1[i]` with `i = -1` reads the *last*
element — Python's negative indexing, silently wrong, from
[day 021](../day-021-frequency-maps/README.md). §7 shows the damage.

### Problem two — Longest Subarray of 1's After Deleting One Element

> *"Delete exactly one element. Return the length of the longest run of 1s in what remains."* —
> LeetCode 1493.

**Route it.** "Subarray" — Q1 says window. No fixed k — Q2 says variable. "Longest" — Q3 says shape
B: shrink while invalid, record after. The condition: a window is workable if it contains **at most
one zero** — deleting that zero leaves all 1s. Zeros only accumulate as the window grows, so Q4
passes. The window carries one integer, `zeros` — the collapsed map from
[day 033](../day-033-window-with-a-map/README.md).

```python
left = zeros = best = 0
for right, x in enumerate(nums):
    if x == 0:
        zeros += 1
    while zeros > 1:
        if nums[left] == 0:
            zeros -= 1
        left += 1
    best = max(best, right - left)
```

One line differs from the standard shape: `right - left`, not `right - left + 1`, because exactly one
element **must** be deleted — the answer is the window minus its sacrificial element. That handles
the all-ones input for free: `[1, 1, 1]` gives 2, because you delete a 1 you would rather keep.

### Problem three — Maximum Sum of Distinct Subarrays of Length K

> *"Return the maximum sum over all subarrays of length k whose elements are all distinct; 0 if none
> exists."* — LeetCode 2461.

**Route it.** "Subarrays of length k" — Q1 window, Q2 **fixed**: this is
[day 031](../day-031-fixed-window/README.md)'s shape, not yesterday's. The window carries two things:
a running sum (slides by add-and-subtract) and a count map (to test distinctness). "All k distinct"
is `len(count) == k`.

```python
count: defaultdict[int, int] = defaultdict(int)
window_sum = 0
best = 0
for i, x in enumerate(nums):
    count[x] += 1
    window_sum += x
    if i >= k:
        out = nums[i - k]
        count[out] -= 1
        if count[out] == 0:
            del count[out]
        window_sum -= out
    if i >= k - 1 and len(count) == k:
        best = max(best, window_sum)
```

When `i` enters, `i - k` leaves — the fixed-window rhythm — and the `del` at zero is mandatory
because `len(count)` is the test, [day 033](../day-033-window-with-a-map/README.md)'s rule applying
inside [day 031](../day-031-fixed-window/README.md)'s shape. Two patterns composed, which is exactly
why interviewers like this one.

### The complete solutions

```python
from collections import defaultdict


def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    """LeetCode 88. Overlapping destination: write from the free end, backwards."""
    write = m + n - 1
    i, j = m - 1, n - 1
    while j >= 0:                            # nums2 exhausted -> rest already in place
        if i >= 0 and nums1[i] > nums2[j]:   # i >= 0 guard: -1 would wrap silently
            nums1[write] = nums1[i]
            i -= 1
        else:
            nums1[write] = nums2[j]
            j -= 1
        write -= 1


def longest_subarray(nums: list[int]) -> int:
    """LeetCode 1493. At most one zero in the window; one element must go."""
    left = zeros = best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > 1:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left)       # window minus the deleted element
    return best


def maximum_subarray_sum(nums: list[int], k: int) -> int:
    """LeetCode 2461. Fixed window carrying a sum AND a map."""
    count: defaultdict[int, int] = defaultdict(int)
    window_sum = 0
    best = 0
    for i, x in enumerate(nums):
        count[x] += 1
        window_sum += x
        if i >= k:                           # i enters, i - k leaves
            out = nums[i - k]
            count[out] -= 1
            if count[out] == 0:
                del count[out]               # len(count) is the test: del is mandatory
            window_sum -= out
        if i >= k - 1 and len(count) == k:
            best = max(best, window_sum)
    return best


if __name__ == "__main__":
    a = [1, 2, 3, 0, 0, 0]
    merge(a, 3, [2, 5, 6], 3)
    print(a)                                              # [1, 2, 2, 3, 5, 6]
    b = [0]
    merge(b, 0, [1], 1)
    print(b)                                              # [1]

    print(longest_subarray([1, 1, 0, 1]))                 # 3
    print(longest_subarray([0, 1, 1, 1, 0, 1, 1, 0, 1]))  # 5
    print(longest_subarray([1, 1, 1]))                    # 2 — must delete a 1

    print(maximum_subarray_sum([1, 5, 4, 2, 9, 9, 9], 3)) # 15
    print(maximum_subarray_sum([4, 4, 4], 3))             # 0 — no distinct window
```

---

## 6. What it costs

### The three solutions, counted

**Merge:** every iteration writes one cell and retires one source element; there are `m + n` cells.
**O(m + n)** time, **O(1)** extra space — the point of merging backwards is precisely that no
temporary array is needed.

**Longest subarray of 1s:** `right` advances `n` times, `left` at most `n` times, neither moves
back — the `2n` argument from [day 032](../day-032-variable-window/README.md). **O(n)** time,
**O(1)** space.

**Distinct k-sum:** one pass, each step doing constant map work; the map holds at most `k` entries.
**O(n)** time, **O(k)** space.

### The cost that matters today: the wrong room

The routing checklist is five questions and costs under a minute. Compare what it buys:

```
45-minute round, well routed:
   ~2 min reading + routing, ~20 min code, ~15 min tests and follow-ups

45-minute round, routed wrong and discovered at minute 20:
   20 min sunk + ~5 min accepting it + 20 min to re-route, re-code, re-test
   = a rushed solution or none, in the same round, with the same knowledge
```

One minute of questions against twenty minutes of loss — a 20× return, and it is the only
complexity argument in this course measured in interview minutes rather than operations.

### The number to have ready

> Every tool in this family is `O(n)` — the whole reason the family exists — with space `O(1)` for
> pure pointers and `O(k)` when the window carries a map. So the differentiator in the round is not
> asymptotics; it is choosing the right `O(n)` tool in the first minute.

---

## 7. The traps

### The near-miss: merging from the front

The instinct is to write the merged order starting at index 0:

```python
c = [1, 2, 3, 0, 0, 0]
merge_front(c, 3, [2, 5, 6], 3)
print(c)
```

```
[1, 2, 2, 5, 6, 0]
```

The 3 is gone — overwritten by the incoming 2 before it was ever read, and every value after it is
wrong. **When source and destination share memory, write into the free end.** Here the free space is
at the back, so the merge runs backwards, largest first.

### The near-miss: the missing `i >= 0` guard

Drop the guard from the backwards merge and run `nums1 = [2, 0]`, `m = 1`, `nums2 = [1]`:

```python
if nums1[i] > nums2[j]:        # i is -1 here
```

```
[2, 2]
```

No crash. `nums1[-1]` reads the **last** element — Python's negative indexing, the same silent wrap
as [day 021](../day-021-frequency-maps/README.md)'s `ord` trap — and the 1 never gets placed. The
expected answer is `[1, 2]`. An index that can go negative must be guarded *before* it is used, not
after.

### The real error: the unguarded pop

Route Backspace String Compare (LeetCode 844) to a stack — a fine first answer — and feed it a
string that starts with deletes:

```python
stack = []
for ch in "##a":
    if ch == "#":
        stack.pop()
    else:
        stack.append(ch)
```

```
Traceback (most recent call last):
  File "day35.py", line 5, in <module>
    stack.pop()
IndexError: pop from empty list
```

A backspace with nothing before it must do nothing: `if stack: stack.pop()`. And the follow-up —
*"now do it in O(1) space"* — is the routing question again: walk both strings **backwards** with a
pointer each, counting skips, because a backspace's effect runs right to left.

### The misroute: "subsequence" through the window door

*Longest increasing subsequence* contains the word "longest", and a window will happily produce an
answer to it — the wrong answer. In `[5, 1, 2]` the longest increasing subsequence is `[1, 2]`,
which is contiguous only by luck; in `[1, 9, 2, 3]` it is `[1, 2, 3]`, which no window can hold,
because a window is a contiguous run and a subsequence may skip. **"Longest" routes you nowhere until
you have answered Q1.** Subsequence questions belong to later tools
([day 024](../day-024-substrings-vs-subsequences/README.md) drew the line; dynamic programming picks
them up much later in the course).

### The misroute: sorting away the answer

*Two Sum* returns **indices**, and the array is unsorted. Sort it to use opposite ends and the
pointers find a correct *pair of values* — at positions in the sorted copy that mean nothing in the
original:

```
nums = [3, 2, 4], target = 6
sorted -> [2, 3, 4]; pointers find 2 + 4, positions 0 and 2
answer returned: (0, 2) -> in the ORIGINAL array that is values 3 and 4 = 7
```

Correct answer: positions 1 and 2. If the answer is made of indices, sorting destroys it — the tell
that routes to a hash map. (Sorting a *copy* and mapping back is possible, but it is `O(n log n)` and
fiddly against the map's clean `O(n)` — [day 027](../day-027-two-pointers-idea/README.md)'s rule.)

### The misroute: negatives through the window door

One line of yesterday repeated, because it is the most expensive misroute in the family:
`shortest subarray with sum at least k` over values that may be negative is **not** a window problem
— `[-3, 5]` with target 3 defeats the shrink logic, from
[day 032](../day-032-variable-window/README.md). Ask "can values be negative?" before the window
leaves your mouth. If yes: prefix sums, arriving [day 037](../day-037-prefix-sums/README.md).

---

## 8. In the interview

### How it gets asked

- Never directly. The routing happens inside every problem from this family — the interviewer just
  says *"Merge these two sorted arrays in place"* or *"Longest run of 1s if you may delete one
  element"* and watches your first two minutes.
- The pressure version: you finish one problem and get *"okay, quick one"* — a second problem with
  fifteen minutes left, where routing speed is openly the thing being measured.
- The trap version: a problem whose surface words point to the wrong room — "longest" on a
  subsequence, "indices" on a sortable array — checking whether you route on words or on structure.

### What to say out loud, in the first ninety seconds

This section *is* the script today. Run the checklist audibly:

1. **Q1, contiguity.** *"It says subarray, so contiguous — window side."* Or: *"pairs in a sorted
   array, in place — pointer side."*
2. **Q2/Q3, the shape.** *"No fixed k, and it says longest — variable window, maximise shape: shrink
   while invalid, record after."* Or: *"count — so I accumulate `right - left + 1`, and 'exactly'
   means two at-most passes."*
3. **Q4, the licence.** *"The condition is a count of zeros, which only grows as the window grows —
   monotonic, so the window is legal. If these could be negative-weighted I'd switch to prefix
   sums."*
4. **The carry.** *"The window carries one integer — the zero count — so O(1) space."*
5. **Only now, code.** *"Brute force is every subarray at O(n²); the window gives O(n). Writing
   it."*

### The follow-ups

**"Why do you merge from the back?"**
Because the destination and one source are the same array, and the free space sits at the end.
Merging forwards writes the smallest values into `nums1[0], nums1[1], ...` — cells that still hold
unread values of `nums1`, so the write destroys data before the read reaches it; on
`[1,2,3,0,0,0]` and `[2,5,6]` the 3 is overwritten and the result is wrong with no error. Walking
backwards, largest first, writes only into cells that are either free space or already read —
`write` starts at `m + n - 1` and `i` at `m - 1`, and `write` can never overtake `i`, because
exactly `j + 1` of the cells between them are reserved for `nums2`'s remaining values. Same
comparisons, same cost, and the overlap problem vanishes. The general rule: when source and
destination overlap, write from the end where the free space is — it is the back here for the same
reason the write pointer ran forwards in remove-duplicates, where the free space opens at the front.

**"You picked a window in ten seconds. What would make you abandon it?"**
Three discoveries, and I try to force all three before coding. First, contiguity failing — if
clarification reveals the answer may skip elements, it is a subsequence question and no window
applies. Second, monotonicity failing — if the condition can improve *and* worsen as the window
grows, the shrink logic has no licence; the concrete case is a sum over values that can be negative,
where `[-3, 5]` style inputs break the invariant, and the correct move is prefix sums. Third, the
answer's shape failing — if the problem wants original indices and my plan involved sorting, I have
destroyed the answer to make the tool fit, and a hash map was the right room. All three are cheap
questions before code and expensive discoveries after, which is exactly why the checklist runs
first.

**"Two problems, fifteen minutes. How do you spend them?"**
Ninety seconds routing both, out loud, before solving either — because routing is cheap and
misrouting is the only real risk at this time scale. Then the one I am surest of first, coded
straight from the pattern skeleton with the two or three standard tests — empty, single element,
all-same — not a full test sweep. Then the second, and if I am short of time on it I state the route,
the invariant and the cost, and write the skeleton honestly rather than rushing opaque code: "this
is a maximise window over the zero count, record after the shrink, O(n)" earns most of the marks
even half-typed. What I never do is start typing the first problem in the first thirty seconds —
at this pace a wrong room is unrecoverable, so the routing minute matters more, not less.

### A model answer

*"Longest run of 1s if you may delete exactly one element"* — the first ninety seconds, verbatim:

> "Subarray of the original — so contiguous, a window question, not a subsequence one. It says
> longest, so a variable window, maximise shape: grow the right edge, shrink from the left only
> while the window is invalid, record after the shrink.
>
> What makes a window workable? At most one zero inside it — I delete that zero and the rest are 1s.
> Zeros only accumulate as the window grows, so the condition is monotonic and the window is legal.
> The window carries a single integer, the zero count — no map needed, values are only 0 or 1.
>
> One edge case before I write it: all ones. I must still delete something, so the answer is the
> window length minus one — which suggests recording `right - left` rather than the usual
> `right - left + 1`, and then the all-ones case needs no special branch at all.
>
> Brute force is every subarray at O(n²); the window is O(n), both pointers only move forward.
> Writing it now — eight lines."

Then the eight lines from §5, and the tests `[1,1,0,1] → 3`, `[1,1,1] → 2`, `[0] → 0` — spoken
before they are run.

---

## 9. Recall card

- **Route before solving, out loud.** Q1 contiguous? Q2 fixed k? Q3 best or count? Q4 monotonic?
  Q5 which pointer shape? Under a minute, every problem.
- **Words route wrong; structure routes right.** "Longest" on a subsequence is no window;
  "indices" plus sorting destroys the answer — hash map.
- **Two leaves lead out of the family:** negatives in a sum → prefix sums
  ([day 037](../day-037-prefix-sums/README.md)); "subsequence" → not this corridor at all.
- **Overlapping source and destination → write from the free end** — merge sorted arrays runs
  backwards, and `i >= 0` guards the wrap to `nums1[-1]`.
- **Everything here is O(n).** The differentiator is the first minute, not the asymptotics — one
  minute of routing against twenty minutes of misroute.
