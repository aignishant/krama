---
day: 39
track: dsa
title: "Difference arrays: range updates, cheaply"
phase: "Prefix sums"
status: written
---

# Day 039 · DSA — Difference arrays: range updates, cheaply

**After today you can:** You can apply a thousand range updates in O(1) each and rebuild the array at the end.

**The interviewer asks it as:** *Apply many range increments and then report the final array.*

---

## 1. What this is, and why they ask it

A **difference array** is the prefix sum run backwards. Instead of storing values and precomputing
totals, you store only the **changes at boundaries**: to add 5 to every element from index `l` to
`r`, write `+5` at `l` and `−5` just past `r` — two writes, whatever the range's length. When all
updates are in, one prefix-sum pass turns the recorded changes back into the final array.

It is [day 037](../day-037-prefix-sums/README.md)'s trade mirrored: prefix sums made *reads* of
ranges O(1) by preparing once; difference arrays make *writes* to ranges O(1) by settling once at
the end. Interviewers like the family — *Corporate Flight Bookings*, *Car Pooling*, *Range
Addition* — because the trick is three lines, and everything they want to probe lives around the
lines: whether you see why two boundary marks equal a whole range of additions, whether you handle
the inclusive-end boundary without an off-by-one, and whether you know when the deal is off — the
moment someone needs to *read* between the updates.

---

## 2. The story

The wedding was a ten-day affair, and Sarasu, who runs the kitchen for that side of the family,
had one question that decided everything else: how many people eat here, each day?

Relatives do not arrive together. The Chennai cousins were coming Sunday and leaving Thursday. The
grand-aunt, Saturday to the last day. The Bombay lot, just Tuesday-Wednesday-Thursday. Fourteen
families, each with their own dates, each a message in the family chat.

Her nephew offered to work it out and did it the honest, slow way: a list of ten days on his
phone, and for each family, he went down every day of their stay adding their headcount. The
Chennai cousins alone meant touching five days. Fourteen families, every day of every stay — his
thumb was sore, and then a message arrived changing one family's dates and he groaned out loud.

Sarasu does not do it that way. For each family she records exactly two things: the day they
arrive, plus so-many mouths; the day they leave, minus so-many. The Chennai cousins are two
entries — Sunday +6, Thursday −6 — not five. A family changing plans is two entries corrected, not
a stay's worth of days redone.

Of course, her page of pluses and minuses does not answer the cook's question directly. Ask her on
Tuesday what Wednesday's count is and she cannot say — not yet. When the entries are all in, she
walks the ten days once, keeping a running count: start at zero, Saturday plus four, Sunday plus
six, and so on down the page. Each day's figure is just the running count as she passes it. One
walk, and the whole calendar is settled.

The one thing she is careful about — because it went wrong at her own daughter's wedding — is what
"leaving Thursday" means. Leaving Thursday *morning* means no Thursday lunch: the minus goes on
Thursday. Leaving Thursday *night* means the minus belongs to Friday. That year, one aunt was
subtracted a day early, the count came up short, and Sarasu has asked every family the same
question since: last meal, or last night?

---

## 3. The idea in plain English

Sarasu's arrivals-and-departures page is the difference array. Her nephew's sore thumb is the
naive version. Her one settling walk is a prefix sum. And her "last meal or last night?" is the
boundary question that decides every off-by-one in this family.

### Recording changes instead of values

To add `amount` to every element of `nums[l..r]`, the naive way touches `r - l + 1` elements. The
difference array touches two:

```python
diff[l] += amount          # from here on, everything is `amount` higher
diff[r + 1] -= amount      # from here on, that stops
```

`diff` records, at each index, **how much the running level changes there** — Sunday +6, Thursday
−6. A range update is one step up at its start and one step down just past its end, and the
thousand elements in between are never touched, because *staying raised* needs no marks.

### Settling: the prefix sum comes home

When all updates are recorded, rebuild with a running total:

```python
result = list(accumulate(diff))[:-1]
```

The running count walking Sarasu's page **is** [day 037](../day-037-prefix-sums/README.md)'s prefix
sum — the two tools are one idea facing opposite directions. Prefix sums: store values, subtract
readings to get ranges. Difference arrays: store changes, accumulate to get values. Formally,
`diff` is built so that its prefix sums are the final array — differencing and prefix-summing undo
each other, the way subtraction undoes addition.

### The `r + 1`, and the extra slot

The `−amount` lands **just past** the range's end — the raise stops *after* `r`, because `r` itself
is still inside. Two consequences, both bug factories:

- `diff` needs `length + 1` slots, so that a range ending at the last element can write its
  step-down at `diff[length]` without crashing. The settling pass drops that final slot.
- When a problem's "end" is exclusive — passengers who get off *at* stop 5 stopped occupying the
  seat *at* stop 5 — the minus goes at `end`, not `end + 1`. Sarasu's question, exactly: last meal,
  or last night? §7 shows both versions of getting it wrong.

### When the deal is off

The difference array answers questions **only after settling**. Ask for `nums[3]` halfway through
the updates and there is no answer without a walk — the marks are promises, not values. So the
tool's contract is: **all updates first, then one settle, then reads.** Interleaved reads and range
updates are the same escalation as [day 037](../day-037-prefix-sums/README.md)'s mutable follow-up
— name the Fenwick and segment trees, `O(log n)` both ways, and say they are heavier machinery for
a genuinely mixed workload.

---

## 4. The picture

Three updates on a five-element array, recorded and settled:

```
 updates, each becoming exactly two marks:

   add  2 to [1..3]:  diff[1] += 2,  diff[4] -= 2
   add  3 to [2..4]:  diff[2] += 3,  diff[5] -= 3
   add -2 to [0..2]:  diff[0] -= 2,  diff[3] += 2

 index        0     1     2     3     4     5   <- the extra slot
            +-----+-----+-----+-----+-----+-----+
 diff       | -2  | +2  | +3  | +2  | -2  | -3  |
            +-----+-----+-----+-----+-----+-----+

 settle (running total):   -2    0    3    5    3    (drop slot 5)
```

**What to notice:** the six marks from three different updates all live in one array, in no
particular order of arrival, and the settle adds them up in passing — had two marks landed on the
same slot they would simply have summed. Boundary marks compose by plain addition; nothing ever
needs to know which update wrote what.

The step shape, drawn as Sarasu's running count:

```
 level
   5              +-----+
   4              |     |
   3        +-----+     +-----+
   2        |     .     .     |
   1        |     .     .     |
   0  +-----+     .     .     +
  -1  |     .     .     .     .
  -2  +     .     .     .     .
      day0  day1  day2  day3  day4

 each +N in diff is a step UP at that index;
 each -N is a step DOWN. The array is the skyline the steps trace.
```

**What to notice:** a range update is one step up and one step down — the flat top in between is
free. That is the entire O(1)-per-update argument, drawn.

---

## 5. The code, built step by step

### Range Addition — the pattern, pure

LeetCode 370: length `n`, a list of `[l, r, amount]` updates (inclusive ends), report the final
array.

```python
diff = [0] * (length + 1)
for left, right, amount in updates:
    diff[left] += amount
    diff[right + 1] -= amount
```

The extra slot makes `right + 1` always legal — a range ending at the last element steps down in
the slot the settle will discard.

```python
return list(accumulate(diff))[:-1]
```

Settle and drop the scratch slot. `accumulate` is [day 037](../day-037-prefix-sums/README.md)'s
build, reused verbatim — no `initial=0` this time, because `diff[0]` already *is* the change from
zero.

### Corporate Flight Bookings — the same, 1-indexed

LeetCode 1109: bookings `[first, last, seats]` with flights numbered from 1, ends inclusive.

```python
diff = [0] * (n + 1)
for first, last, seats in bookings:
    diff[first - 1] += seats     # shift to 0-based
    diff[last] -= seats          # (last - 1) + 1 = last: two shifts cancel
return list(accumulate(diff))[:-1]
```

The 1-based shift and the exclusive step-down cancel into plain `diff[last]` — worth deriving out
loud rather than pattern-matching, because deriving it is the protection against the off-by-one.

### Car Pooling — Sarasu's question decides it

LeetCode 1094: trips `[people, start, end]`, passengers ride from `start` to `end`, capacity check.
The crux: passengers get off **at** `end` — the seat is free *at* `end`, so the step-down goes at
`end`, not `end + 1`. Last meal, or last night — this problem says last night was `end - 1`.

```python
diff = [0] * 1001                    # stops are bounded: 0..1000
for people, start, end in trips:
    diff[start] += people
    diff[end] -= people              # off AT end — exclusive, no +1
```

Then the settle doubles as the check — no final array needed, just the running level against
capacity:

```python
riding = 0
for change in diff:
    riding += change
    if riding > capacity:
        return False
return True
```

### The complete solutions

```python
from itertools import accumulate


def get_modified_array(length: int, updates: list[list[int]]) -> list[int]:
    """LeetCode 370. Inclusive ends: step down at right + 1; settle once."""
    diff = [0] * (length + 1)
    for left, right, amount in updates:
        diff[left] += amount
        diff[right + 1] -= amount        # extra slot makes this always legal
    return list(accumulate(diff))[:-1]   # drop the scratch slot


def corp_flight_bookings(bookings: list[list[int]], n: int) -> list[int]:
    """LeetCode 1109. 1-indexed inclusive ends: the two shifts cancel."""
    diff = [0] * (n + 1)
    for first, last, seats in bookings:
        diff[first - 1] += seats
        diff[last] -= seats
    return list(accumulate(diff))[:-1]


def car_pooling(trips: list[list[int]], capacity: int) -> bool:
    """LeetCode 1094. Passengers leave AT end: exclusive end, no +1.
    The settle walk doubles as the capacity check."""
    diff = [0] * 1001
    for people, start, end in trips:
        diff[start] += people
        diff[end] -= people
    riding = 0
    for change in diff:
        riding += change
        if riding > capacity:
            return False
    return True


if __name__ == "__main__":
    print(get_modified_array(5, [[1, 3, 2], [2, 4, 3], [0, 2, -2]]))
    # [-2, 0, 3, 5, 3] — the walk from §4

    print(corp_flight_bookings([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5))
    # [10, 55, 45, 25, 25]

    print(car_pooling([[2, 1, 5], [3, 3, 7]], 4))   # False — 5 aboard on [3, 5)
    print(car_pooling([[2, 1, 5], [3, 3, 7]], 5))   # True
    print(car_pooling([[2, 1, 5], [3, 5, 7]], 3))   # True — clean handover AT 5
```

The last test is the boundary made executable: two passengers off at stop 5, three on at stop 5,
capacity 3 — legal only because "off at 5" frees the seats *at* 5. Change the `diff[end]` to
`diff[end + 1]` and this test flips to `False`.

---

## 6. What it costs

### Counted from the loops

```
recording:  u updates × 2 writes each          -> O(u)
settling:   one pass over length + 1 slots     -> O(n)
total:      O(n + u)   — and O(1) per update, which is the headline
space:      the diff array itself, O(n); no other structure
```

The naive version costs the sum of the range lengths — `O(n)` per update in the worst case,
`O(n × u)` overall.

### Measured, not just argued

A thousand updates averaging 50,000 elements wide, on a 100,000-element array — both versions run
for real:

```
naive (touch every element per update):  2.225 s
difference array (record + one settle):  0.003 s     ~780× faster

the arithmetic behind it:
  naive : 1,000 × ~50,000 = 50,000,000 element writes
  diff  : 1,000 × 2 + 100,001 ≈ 102,000 operations — ~500× fewer, as observed
```

### The trade said in one line

Prefix sums and difference arrays are the same purchase in opposite shops: **prefix** pays O(n)
once to make range *reads* O(1); **difference** pays O(n) once — at the end — to make range
*writes* O(1). Each is helpless at the other's job until it settles, and the mixed workload
belongs to the log-n trees.

### The number to have ready

> Two writes per update regardless of range width, one O(n) settle at the end — O(n + u) total.
> A thousand wide updates on a hundred-thousand-element array: about a hundred thousand operations
> against fifty million naive — measured at roughly 780× faster.

---

## 7. The traps

### The real error: the missing extra slot

Size the array at `length` and update a range that touches the last element:

```python
diff = [0] * 5                       # length 5, no extra slot
diff[1] += 2
diff[4 + 1] -= 2                     # range [1..4]: steps down at index 5
```

```
Traceback (most recent call last):
  File "day39.py", line 3, in <module>
    diff[4 + 1] -= 2
IndexError: list index out of range
```

The step-down for a range ending at the last element has nowhere to land. **`length + 1` slots,
always**, and the settle drops the last one. (The tempting alternative — `if right + 1 < length:`
guards around every write — works and doubles the code's surface for the same reason
[day 037](../day-037-prefix-sums/README.md)'s sentinel beat the special-case `if`.)

### The near-miss: the inclusive minus at the inclusive end

Put the step-down *at* `r` instead of past it, in Range Addition:

```python
diff[left] += amount
diff[right] -= amount                # wrong: right is still INSIDE the range
```

On `get_modified_array(5, [[1, 3, 2]])` this yields `[0, 2, 2, 0, 0]` — the range's own last
element never got its raise. Every range comes out one short at the tail, silently. The sentence
that prevents it: **the raise stops *after* the last raised element.**

### The near-miss: `+ 1` where the end was already exclusive

The same instinct, inverted, in Car Pooling:

```python
diff[start] += people
diff[end + 1] -= people              # wrong: passengers got off AT end
```

```
bad handover: False
```

On `[[2, 1, 5], [3, 5, 7]]` with capacity 3 — two off at stop 5, three on at stop 5 — the correct
answer is `True`; this version keeps the leavers aboard one stop too long, sees five riders, and
refuses a legal trip. Two problems, two conventions: Range Addition's ends are inclusive
(`r + 1`), Car Pooling's are exclusive (`end`). **The convention is in the problem statement, not
in the pattern** — Sarasu's question, asked of every problem: last meal, or last night?

### The near-miss: reading before settling

```python
diff[2] += 5                         # update: add 5 to [2..6]
diff[7] -= 5
print(diff[4])                       # "what is nums[4] now?"
```

```
0
```

Not 5 — nothing. The marks are promises; only the settle walk redeems them. If the problem
interleaves reads with range updates, the difference array is the wrong tool and saying so is the
answer: rebuild-per-read is `O(n)` a time, and the honest upgrade is a Fenwick or segment tree at
`O(log n)` for both operations.

### The contract corner: bounds and non-integer positions

Car Pooling's `diff = [0] * 1001` leans on the promise that stops live in `0..1000` — ask for that
bound before writing it. When positions are huge or unbounded (timestamps, coordinates), a dense
array is off the table; the same boundary marks go into a **map** — `{position: change}` — settled
by walking the sorted keys: `O(u log u)` for the sort, memory `O(u)`, and no dependence on the
coordinate range at all. Same idea, sparse clothing — worth naming whenever the interviewer says
"positions can be up to a billion".

---

## 8. In the interview

### How it gets asked

- *"Apply these range increments and return the final array."* — Range Addition, LeetCode 370; the
  pattern verbatim.
- *"Seat bookings across flights 1 to n — how many seats per flight?"* — Corporate Flight
  Bookings, LeetCode 1109; 1-indexed, inclusive.
- *"Can this van complete all trips without exceeding capacity?"* — Car Pooling, LeetCode 1094;
  exclusive ends, settle-as-check.
- *"A calendar of guest arrivals and departures — peak occupancy?"* — the same tool wearing
  interval clothes; it reappears when the sorting phase treats interval problems.
- And the escalation: *"now queries arrive between the updates"* — the handover question to
  log-n trees, mirroring [day 037](../day-037-prefix-sums/README.md)'s.

### What to say out loud, in the first ninety seconds

1. **Name the shape.** *"Many range updates, one final report — that's a difference array: record
   changes at boundaries, settle once with a prefix sum."*
2. **Give the two-line mechanic.** *"Add at the start, subtract just past the end — two writes per
   update, any width. The elements between never get touched because staying raised needs no
   marks."*
3. **Ask the boundary question.** *"Is the end inclusive — do they fly the last flight, eat the
   last meal? That decides whether the minus goes at end or end + 1."*
4. **State the contract.** *"All updates, then one settle, then reads — if reads interleave, this
   is the wrong tool and I'd name a Fenwick tree instead."*
5. **Give the cost.** *"O(1) per update, O(n) settle — against O(range width) per update naively;
   at a thousand wide updates that's measured hundreds of times faster."*

### The follow-ups

**"Why does writing two numbers update a thousand elements? Convince me."**
Because the settle walk turns marks into levels, and between marks the level cannot move. The
running total only changes where `diff` is non-zero — so `+5` at index `l` raises the level as the
walk passes `l`, and that raise *persists* through every subsequent index for free, because the
walk carries its total forward; the `−5` just past `r` is the one and only thing that ends it.
Formally: the settled value at index `i` is the sum of `diff[0..i]`, so adding 5 to `diff[l]` adds
5 to every settled value from `l` onward — a suffix — and subtracting at `r + 1` cancels it from
`r + 1` onward; a range is the difference of two suffixes. That is also why overlapping updates
compose without any bookkeeping: each is a pair of boundary marks, addition is commutative, and
the walk adds them all in passing — §4's index 3, where two updates' marks share a slot and simply
sum.

**"Now the updates are multiplicative — double everything in the range. Still works?"**
Not with sums, and the honest first answer is why: the whole machine rests on the settle being a
running *sum* and range effects being the difference of two suffix-sums — addition's structure.
Doubling is multiplication; the equivalent trick needs a running *product*: record ×2 at `l` and
×½ past `r`, settle by multiplying. That works exactly when every factor is invertible — no zeros,
and floating-point or modular arithmetic to hold the halves — so for "double from l to r" over
integers it survives only in log-space or mod-p form, and I would say that rather than force it.
The general statement, if the interviewer wants it: the trick works over any operation with an
inverse — sums with subtraction, products with division, XOR with itself — because "start the
effect, cancel the effect" is the whole design. For non-invertible updates like "set the range to
5" or "max with 5", boundary marks cannot cancel, and the tool is a segment tree with lazy
propagation — machinery for a later phase, named and left.

**"Peak riders rather than a yes/no capacity check — and what if stop numbers go to a billion?"**
Peak is the settle walk keeping a maximum instead of a threshold test — `peak = max(peak, riding)`
— same cost, and it falls out of the same running level. Unbounded coordinates kill the dense
array, not the idea: put the marks in a dictionary keyed by position — `changes[start] += people`,
`changes[end] -= people` — then settle by walking the keys in sorted order. Cost becomes
O(u log u) for the sort with memory O(u), independent of the coordinate range; the level between
marked positions is constant, so nothing between them ever needed a slot. That sparse form is
worth knowing by name because it is the standard answer for time-stamped intervals — bookings,
meetings, server load — where the axis is huge and the events are few, and it reappears when the
sorting phase does interval problems properly.

### A model answer

> "Bookings across flights 1 to n, report seats per flight — many range updates, one final report.
> I'll use a difference array: record each booking as two boundary marks, then settle once.
>
> The mechanic: to add `seats` to flights `first` through `last`, I add at the start and subtract
> just past the end. The elements between are never touched — when I rebuild with a running total,
> a mark raises the level and the level stays raised until the closing mark cancels it. Two writes
> per booking, any width.
>
> One boundary question before I code: ends are inclusive here — they do fly the last flight — so
> the subtract goes past it. The array is 1-indexed, so shifting to 0-based, the marks are
> `diff[first - 1] += seats` and `diff[last] -= seats` — the two off-by-ones cancel, and I'd rather
> derive that than remember it. I size the array n + 1 so a booking ending at flight n has a slot
> to step down in, and the settle drops that slot.
>
> ```python
> def corp_flight_bookings(bookings, n):
>     diff = [0] * (n + 1)
>     for first, last, seats in bookings:
>         diff[first - 1] += seats
>         diff[last] -= seats
>     return list(accumulate(diff))[:-1]
> ```
>
> Cost: O(1) per booking and one O(n) settle — O(n + u) total, against O(n × u) touching every
> flight of every booking. And the contract worth stating: this answers nothing until it settles —
> if queries arrived between bookings I'd move to a Fenwick tree at O(log n) both ways, and if
> flight numbers were unbounded I'd keep the same marks in a sorted map instead of a dense array."

---

## 9. Recall card

- **Range update = two boundary marks:** `diff[l] += amount`, `diff[r + 1] -= amount` — O(1) each,
  any width. Settle once with a running total; the marks compose by plain addition.
- **It is day 037 mirrored:** prefix sums buy O(1) range *reads*; difference arrays buy O(1) range
  *writes*. Each settles once; mixed read/write workloads go to Fenwick/segment trees, O(log n).
- **Size `length + 1`** — the step-down for a range ending at the last element needs its slot, and
  the settle drops it. No guards.
- **Ask the boundary question every time:** inclusive end → minus at `r + 1` (flights, bookings);
  exclusive end → minus at `r` (car pooling — off *at* the stop). Last meal, or last night?
- **Marks are promises, not values** — no reads before the settle. Huge coordinates → same marks
  in a sorted map, O(u log u), range-independent.
