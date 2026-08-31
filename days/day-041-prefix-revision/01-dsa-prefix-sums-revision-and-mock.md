---
day: 41
track: dsa
title: "Prefix sums revision and mock round"
phase: "Prefix sums"
status: written
---

# Day 041 · DSA — Prefix sums revision and mock round

**After today you can:** You can recognise a prefix-sum problem from the question alone.

**The interviewer asks it as:** *Two problems, no hints, talk as you go.*

---

## 1. What this is, and why they ask it

Days 37 to 40 built the precompute family: the prefix array and its sentinel, prefix-plus-map for
exact sums with negatives, the difference array for cheap range updates, and the 2D table with
inclusion-exclusion. Four tools, one instinct — **spend a pass now so questions cost nothing
later** — and one shared border with the window family, patrolled by a single question about
negative numbers.

Today is the phase's mock, and its skill is the one the hub names: **recognition from the
question alone.** The window phase's tells were loud — "longest", "substring". This family's
tells are quieter: *many queries*, *fixed data*, *exactly*, *negatives allowed*, *range updates*,
*rectangle*. Interviewers rarely say "use prefix sums"; they describe a situation whose shape you
must hear. The two problems in §5 are unseen, chosen because their surfaces point away from the
tools that solve them — route them yourself, on the clock, before reading the transcripts.

---

## 2. The story

The mock board exam was in November, and Rekha, who has taught Class 10 mathematics for
seventeen years, watched her best student walk out of it with a face like a burnt chapati.

Pranav. Ninety-eight in every class test. He had answered the paper in order, from question one,
like a man eating a thali left to right without looking at the plate. Question four was a
monster — he gave it twenty-five minutes and got it, too — and then did the last three questions,
worth eighteen easy marks, in a panicked scrawl in nine minutes. Sixty-one.

The Monday after, she taught the lesson she teaches every batch, and it has nothing to do with
mathematics. Take the first five minutes, she said, and do not solve anything. Read the whole
paper with a pencil in your hand, and against every question, write one word. Not the answer —
the **chapter**. This one is mensuration. This one is quadratic. This one *looks* like
trigonometry but the triangle is a red herring — it is similar-triangles dressed up.

The class groaned. Five minutes, madam, gone, and nothing written.

Then she did her demonstration, the one that convinces every batch. She put a question on the
board and gave them ten seconds — not to solve it, only to name the chapter. Most got it. Then
she asked: now that you know the chapter, how much of the method do you already know? Nearly all
of it, someone said. The chapter *is* the method, she said. What costs you twenty-five minutes is
not solving — it is solving inside the wrong chapter, or discovering the right one at minute
twenty.

Pranav sat the December mock with his pencil and his five minutes. Named every question's
chapter, did the eighteen easy marks first, saw through the dressed-up question because naming
it was now a separate act from answering it. Ninety-one.

She tells them one more thing, every year. The examiners do not write the chapter's name on the
question. That is not cruelty. Naming the chapter **is** the examination.

---

## 3. The idea in plain English

Rekha's chapter-naming is today's whole skill: recognition is a separate act from solving, done
first, with its own five minutes. Her dressed-up trigonometry question is §5's second problem.
And "the chapter is the method" is exactly true here — name the tool and the code is lines you
already own.

### The phase, on one table

| Tool | The tell in the question | The invariant to say | Day |
|---|---|---|---|
| Prefix array | many range-sum queries, data fixed | sentinel 0; *after the end minus before the start* | [037](../day-037-prefix-sums/README.md) |
| Prefix + map | "exactly k", negatives possible, counting or longest | `seen[0] = 1`; ask the map, then record | [038](../day-038-subarray-sum-k/README.md) |
| Difference array | many range *updates*, report at the end | two marks per update; settle once; inclusive → `r + 1` | [039](../day-039-difference-arrays/README.md) |
| 2D prefix | rectangle sums, block sums | zero frame; big − two strips + corner | [040](../day-040-2d-prefix-sums/README.md) |

And the border post, staffed by one question: **"can the values be negative?"** All positive and
at-most/longest → the window family keeps the case at `O(1)` space. Negatives, or "exactly" →
this family takes it, at `O(n)` space, and saying the handover out loud is worth marks by itself.

### The five bugs of the phase, as a pre-flight list

Every lesson this week ended in the same handful of failure shapes. Before declaring any
prefix-family solution done, run the list:

1. **The sentinel** — `initial=0`, `seen[0] = 1`, `{0: -1}`, the zero frame. Is the
   before-anything moment represented?
2. **The order** — ask the map, *then* record. (`k = 0` is the checking input.)
3. **The boundary** — inclusive or exclusive end? Minus at `r + 1` or `r`? Last meal, or last
   night?
4. **The map's contract** — count-map for "how many", first-index map (never overwritten) for
   "longest". Which am I keeping, and did I say so?
5. **The negative index** — can any subscript reach −1? Python will not crash; it will lie.

### Running today's mock

The protocol is [day 036](../day-036-two-pointers-revision/README.md)'s, with one addition:
thirty-five minutes a problem, standing, talking, nothing open — and **Rekha's pencil minute
comes first**: before any solving, say the chapter. Which of the four tools, or the window
family, or neither — and what tell decided it. Then the invariant, then code, then the five test
inputs by voice, then the pre-flight list. Score yourself on the transcripts afterwards — on the
naming, before the code.

---

## 4. The picture

The phase as one desk, with its border crossing:

```
                      "ranges, sums, subarrays, updates..."
                                    |
                     Q: reads, or updates, or both?
              +---------------------+---------------------+
            reads                 updates              both, mixed
              |                     |                     |
      Q: 1D or rectangles?    difference array       Fenwick/segment
        |            |        (039) — marks,         tree — NAME them,
       1D        2D prefix    settle once            O(log n), later
        |         (040)
  Q: "exactly k" or negatives?
        |                  |
       no                 yes
        |                  |
  Q: all positive?    prefix + map (038)
        |                  seen[0]=1, ask-then-record
   window family
   keeps it (032-034)     many fixed queries, no target?
   O(1) space              -> plain prefix array (037)
```

**What to notice:** two exits again — the window border and the log-n trees — and both are
*named*, not solved. Knowing where the family ends is part of knowing the family.

The mock clock, with Rekha's minute marked:

```
 min 0-2    read twice; contract questions (negatives? ends inclusive? updates?)
 min 2-3    NAME THE CHAPTER, out loud: tool + the tell that chose it
 min 3-5    example by hand; brute force named with its cost
 min 5-20   code, narrating; invariant before each loop
 min 20-25  five test inputs by voice; then the five-bug pre-flight list
 min 25-35  follow-ups; the escalation names (Fenwick, segment tree)
```

---

## 5. The code, built step by step

Two problems, worked as transcripts. Neither says "prefix" anywhere on its surface.

### Match one — Product of Array Except Self

> *"Return an array where answer[i] is the product of every element except nums[i]. No division.
> O(n)."* — LeetCode 238.

**Beat 1, clarify.** *"Zeros allowed? Negatives? And division is banned even for the no-zero
case?"* Yes, yes, yes — and the division ban is the routing hint in disguise.

**Beat 2, name the chapter.** *"Products, not sums — but the shape is day 037's: answer[i] is
*everything before i* times *everything after i*. Those are a prefix and a suffix. The chapter is
prefix precompute, with multiplication as the running operation."*

Saying *why division is banned* seals the naming: division is the subtraction of products —
`total / nums[i]` is the 1D prefix trick run through an inverse — and zero has no inverse. §7 has
the crash. The ban forces the two-directions form instead.

**Beat 5, code — two sweeps, one output array.**

```python
answer = [1] * n
before = 1
for i in range(n):
    answer[i] = before      # product of everything left of i
    before *= nums[i]
```

*"First sweep: answer[i] gets the running product of everything before i — the prefix, written
directly into the output. `before` starts at 1, the empty product — the sentinel again, in
multiplicative clothing."*

```python
after = 1
for i in range(n - 1, -1, -1):
    answer[i] *= after      # times the product of everything right of i
    after *= nums[i]
```

*"Second sweep, from the right: multiply in the running product of everything after i. Same
idea, mirrored — and because `after` rides in one variable, the suffix array never exists:
O(1) extra space beyond the output."*

**Beat 6, test.** `[1,2,3,4]` → `[24,12,8,6]`. One zero: `[-1,1,0,-3,3]` → `[0,0,9,0,0]` — say
*why* index 2 alone is non-zero. Two zeros: `[0,0]` → `[0,0]` — every position sees a zero on
some side. Single element → `[1]`, the empty product, and worth saying before running.

### Match two — Continuous Subarray Sum

> *"Does the array contain a subarray of length at least two whose sum is a multiple of k?"* —
> LeetCode 523.

**Beat 1, clarify.** *"Is zero a multiple of k? So `[0, 0]` is True for any k?"* Yes — the
contract corner that decides two test cases. *"Values non-negative? k positive?"* Say the
questions even when the constraints answer them.

**Beat 2, name the chapter — through the disguise.** *"'Sum is a multiple of k' is day 038's
remainder costume: two prefixes with the **same remainder** mod k bracket a stretch summing to a
multiple of k. And it asks *does one exist of length ≥ 2* — an existence-with-length question, so
the map stores **first index** per remainder, day 038's longest-contract, not the count."*

**Beat 5, code.**

```python
first = {0: -1}             # remainder 0 before the array — index sentinel
running = 0
for i, x in enumerate(nums):
    running = (running + x) % k
    if running in first:
        if i - first[running] >= 2:
            return True     # stretch from first[running]+1 .. i, length >= 2
    else:
        first[running] = i
return False
```

*"Three familiar pieces: the sentinel `{0: -1}` so a qualifying stretch from index 0 measures
correctly; first-index-never-overwritten, because an *earlier* match can only make the stretch
longer; and the length check `i - first[running] >= 2`. Note what the `else` protects: a repeat
remainder that fails the length check must NOT update the map — §7 shows the input that punishes
that."*

**Beat 6, test.** `[23,2,4,6,7], 6` → True (`[2,4]`). `[23,2,6,4,7], 13` → False. `[0,0], 1` →
True — the contract corner. `[5,0,0,0], 3` → True. `[6], 6` → False — length one is not enough.

### The complete solutions

```python
def product_except_self(nums: list[int]) -> list[int]:
    """LeetCode 238. Prefix and suffix products, two sweeps, no division."""
    n = len(nums)
    answer = [1] * n
    before = 1
    for i in range(n):
        answer[i] = before           # product of nums[0..i-1]
        before *= nums[i]
    after = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= after           # times product of nums[i+1..]
        after *= nums[i]
    return answer


def check_subarray_sum(nums: list[int], k: int) -> bool:
    """LeetCode 523. Same remainder twice = multiple-of-k stretch between;
    first-index map + the length-2 rule."""
    first: dict[int, int] = {0: -1}
    running = 0
    for i, x in enumerate(nums):
        running = (running + x) % k
        if running in first:
            if i - first[running] >= 2:
                return True
        else:
            first[running] = i       # first occurrence only — never overwrite
    return False


if __name__ == "__main__":
    print(product_except_self([1, 2, 3, 4]))        # [24, 12, 8, 6]
    print(product_except_self([-1, 1, 0, -3, 3]))   # [0, 0, 9, 0, 0]
    print(product_except_self([0, 0]))              # [0, 0]

    print(check_subarray_sum([23, 2, 4, 6, 7], 6))  # True
    print(check_subarray_sum([23, 2, 6, 4, 7], 13)) # False
    print(check_subarray_sum([0, 0], 1))            # True — 0 is a multiple
    print(check_subarray_sum([5, 0, 0, 0], 3))      # True
    print(check_subarray_sum([6], 6))               # False — length 1
```

---

## 6. What it costs

### Match one

Two sweeps of `n` iterations, one multiplication and one write each — `2n` operations. **O(n)
time.** Extra space beyond the output: two running variables — **O(1)**, and saying "beyond the
output" is the precise phrasing the follow-up fishes for.

### Match two

One sweep, one modulo and one map operation per element. **O(n) time, O(min(n, k)) space** — at
most `k` distinct remainders can exist, so the map is bounded by `k` regardless of `n`. That
sharper bound is [day 038](../day-038-subarray-sum-k/README.md)'s streaming observation made
concrete, and producing it unprompted is a small flag of ownership.

### The phase's costs, one line each

```
prefix array (037):  O(n) build, O(1)/query, O(n) space — data must hold still
prefix + map (038):  O(n) time, O(n) space — the space buys the negatives
difference (039):    O(1)/update + O(n) settle — no reads before settling
2D prefix (040):     O(rows·cols) build, O(1)/rectangle — four lookups
```

Four tools, one sentence of cost each — recitable in twenty seconds, and worth having at that
speed.

---

## 7. The traps

### The real error: division as the shortcut

The banned version of match one, on the input with a zero:

```python
total = 1
for x in nums:
    total *= x
print([total // x for x in nums])
```

```
Traceback (most recent call last):
  File "day41.py", line 4, in <module>
    print([total // x for x in nums])
ZeroDivisionError: integer division or modulo by zero
```

And patching the zero cases breeds a three-branch swamp (no zeros, one zero, two-plus zeros)
that is longer than the honest two sweeps. The ban is not arbitrary: division is the inverse
that products do not always have — the same reason [day 039](../day-039-difference-arrays/README.md)'s
multiplicative difference array needed invertibility. One principle, surfacing twice.

### The near-miss: the overwritten first index

Move the map write out of the `else` in match two:

```python
if running in first and i - first[running] >= 2:
    return True
first[running] = i          # overwrites on every step
```

```
bad:  False      # on [5, 0, 0, 0], k = 3 — answer is True
bad2: False      # on [0, 0],       k = 1 — answer is True
```

Each repeat remainder that fails the length check now *drags the stored index forward*, so the
gap can never reach 2. `[5, 0, 0, 0]`: remainder 2 repeats at every index, the stored index
shadows `i` one step behind, and a True instance is walked straight past.
[Day 038](../day-038-subarray-sum-k/README.md)'s rule, now with an existence check attached:
**first index means first, forever.**

### The near-miss: the forgotten length rule

Return True on any repeated remainder and `[6], 6` comes back True — the single element 6, sum
6, "length at least two" violated. The subarray between two equal prefixes at indices
`first[r]` and `i` has length `i - first[r]`; the rule is `>= 2`, and deriving that length —
rather than guessing `> 1` versus `>= 1` — is ten seconds of boundary arithmetic that prevents
the bug class entirely. *(And the index sentinel `{0: -1}` makes the derivation uniform for
stretches from the start: `i - (-1) = i + 1` elements.)*

### The contract corner: zero is a multiple

`[0, 0]` with any `k` is True — sum 0 = 0 × k. Candidates who never asked "is zero a multiple?"
lose this case, and it is on every judge's test list precisely because the maths and the
instinct disagree. Contract questions are free; this one is two test cases.

### The mock trap, repeated on purpose

The silent stall from [day 036](../day-036-two-pointers-revision/README.md) has a phase-specific
variant: the candidate who recognises *nothing* and starts writing nested loops to stay busy.
The recovery sentence exists here too: *"the surface says products, but the shape is
everything-before times everything-after — let me check whether the prefix idea transfers."*
Naming a *candidate* chapter, even tentatively, restarts the round; busy hands do not.

---

## 8. In the interview

### How it gets asked

- *"Let's do two problems."* — the screening round; this phase supplies the quieter mediums.
- *"Product of the array except self, no division."* — the transfer test: does your prefix
  instinct survive a change of operation?
- *"Does a subarray of length ≥ 2 sum to a multiple of k?"* — the disguise test: remainder
  thinking under a divisibility costume.
- *"Now the updates arrive between the queries."* — the escalation, every time this family
  appears: name Fenwick and segment trees, O(log n), and stop.

### What to say out loud, in the first ninety seconds

Rekha's pencil minute, as a script:

1. **The contract questions.** *"Negatives possible? Ends inclusive? Is zero a multiple? Can the
   data change between queries?"* — four questions, ten seconds each, and two of them are
   routing questions in disguise.
2. **The chapter, named with its tell.** *"Everything-before times everything-after — prefix
   shape with multiplication"* / *"multiple of k means equal remainders — prefix-plus-map in the
   remainder costume."*
3. **The map's contract, if there is a map.** *"Existence with a length rule, so first-index,
   never overwritten, sentinel {0: -1}."*
4. **The brute force, priced.** *"Every pair of ends is O(n²); the prefix idea makes it one or
   two passes."*
5. **The pre-flight promise.** *"Before I call it done I'll check the sentinel, the ask-record
   order, the boundary, the map contract, and any index that can reach −1."*

### The follow-ups

**"Why exactly is division banned in Product Except Self?"**
Because division is the trick's inverse operation, and the inverse does not always exist. The
one-pass fantasy is: total product, then `total / nums[i]` per position — which is the prefix
family's subtraction, transplanted to products. Subtraction always works, which is why range
sums never faced this; division fails at zero, and floats add precision rot besides. One zero
in the array makes the total 0 and every quotient meaningless — the crash is immediate — and
handling it by cases (no zeros, one zero, more) yields three code paths, each wrong somewhere
under pressure. The two-sweep form sidesteps inverses entirely: build the left products
forward, ride the right products backward, multiply — every position pays two multiplications
and no position ever divides. It is the same lesson day 039 taught about multiplicative range
updates: the boundary-mark and running-total tricks are theorems about invertible operations,
and when the inverse goes missing, you restructure the computation instead of forcing it.

**"Your remainder solution — why store the first index and not the count, like in 560?"**
Because the two problems ask different questions of the same walk, and the map's contract
follows the question. LeetCode 560 asks *how many* subarrays — every earlier matching prefix is
one more answer, so the map must remember multiplicities: a count. This problem asks *does one
exist with length at least two* — a single sufficiently-old match settles it, and the oldest
match is the most likely to satisfy the length rule, so the map keeps each remainder's first
index and never updates it: any later occurrence is strictly worse. The same fork appeared on
day 038 between 560 and longest-subarray-with-sum-k. And the overwrite bug is the fork ignored:
refresh the index on every repeat and the stored position shadows the current one, the gap
never reaches two, and `[5,0,0,0]` with k = 3 returns False against a plain True. Saying
"count-map for how-many, frozen first-index for longest-or-exists" before coding is the
one-sentence vaccine.

**"Updates now arrive between the range-sum queries. Sketch your options."**
Three, in cost order, and the ratio between updates and queries picks one. Rare updates: keep
the prefix array and rebuild on write — O(n) per update, O(1) per query, unbeatable when writes
are once-a-day. Mixed traffic: a Fenwick tree — the prefix idea stored as a tree of partial
sums, giving O(log n) point-update and O(log n) prefix-query; range sums stay
two-prefix-subtraction; it is ~20 lines and the standard answer. Range *updates* with range
queries, or operations beyond sums: a segment tree with lazy propagation — heavier, more
general, O(log n) both ways. I would name all three with those costs, say the workload decides,
and be honest that under interview time I can produce a Fenwick tree while a lazy segment tree
is a design conversation — both structures get their full treatment later in this course, and
at this point in a round the *naming with costs* is usually what was being tested.

### A model answer

The pencil minute of match two, continuous and verbatim — compare your recording against it:

> "Subarray of length at least two whose sum is a multiple of k. Two contract questions first:
> is zero a multiple of k — I'll assume yes, so [0,0] is True — and are values non-negative?
> Either way, 'multiple of k' is the tell: a stretch sums to a multiple of k exactly when the
> prefixes at its two ends leave the same remainder mod k. So this is the prefix-plus-map
> family in its remainder costume, from day 038.
>
> It asks for existence with a length rule, not a count — so the map stores each remainder's
> first index, never overwritten, because an earlier match only makes the stretch longer. The
> sentinel is remainder 0 at index −1, so a qualifying stretch from the very start measures
> correctly. The stretch between indices first[r] and i has length i − first[r], so the test is
> i − first[r] ≥ 2 — I derived that rather than guessing the sign.
>
> One subtlety I'll flag before coding: when a repeated remainder fails the length check, I must
> NOT update the map — updating drags the first index forward and can walk straight past a true
> answer; [5,0,0,0] with k 3 is the input that catches it.
>
> Brute force is every pair of ends at O(n²). This is one pass, O(n) time, and the map holds at
> most k remainders, so O(min(n, k)) space. Tests before I run anything: the two examples,
> [0,0] True, [6] with k 6 False for the length rule, [5,0,0,0] True for the no-overwrite
> rule."

---

## 9. Recall card

- **Name the chapter before solving — it is a separate act.** The tells: many queries / exactly /
  negatives / range updates / rectangle — and the tool names itself.
- **The border question is "can values be negative?"** All-positive at-most stays with windows at
  O(1) space; negatives or "exactly" cross to prefix-plus-map at O(n).
- **Pre-flight, every time:** sentinel · ask-then-record · boundary (r vs r+1) · map contract
  (count vs frozen first-index) · any index that can reach −1.
- **Two transfer lessons:** products = prefix idea minus the inverse (no division — restructure
  as two sweeps); multiple-of-k = equal remainders, map bounded by k.
- **The escalation names, with costs:** rebuild-if-rare; Fenwick tree O(log n) point-update;
  segment tree + lazy for range-update-range-query. Name, price, stop.
