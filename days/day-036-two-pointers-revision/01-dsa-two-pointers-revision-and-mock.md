---
day: 36
track: dsa
title: "Two pointers revision and mock round"
phase: "Two pointers and sliding window"
status: written
---

# Day 036 · DSA — Two pointers revision and mock round

**After today you can:** You can solve two unseen pointer or window problems cold.

**The interviewer asks it as:** *Two problems, no hints, talk as you go.*

---

## 1. What this is, and why they ask it

Days 27 to 35 built the pointer-and-window toolkit: the two-pointers idea, opposite ends, read and
write, fast and slow, the fixed window, the variable window, the window with a map, the counting
window, and yesterday's routing checklist that chooses among them. Today is the third mock round,
and it has a different job from [day 018](../day-018-arrays-revision/README.md)'s process and
[day 026](../day-026-strings-revision/README.md)'s recognition.

Today is about **execution under match conditions**. You know the six beats. You know the routing
questions. The remaining question is whether they still run when the problem is unseen, the clock is
on, and someone is watching — because knowledge that evaporates under pressure scores the same as
knowledge you never had. This phase is also the single most-asked family at product companies: a
majority of screening-round mediums are pointer or window problems, so this is the mock most worth
doing honestly.

The two problems in §5 are deliberately ones no lesson has solved. Route them yourself before
reading the transcripts.

---

## 2. The story

Tuesday and Thursday evenings, the community hall becomes a badminton court, and coach Sebastian
runs the junior group from six to eight.

For the first hour it is drills, and in drills his best student is unbeatable. Drop shots into a
hoop, twenty out of twenty. Serves onto a coin. Footwork ladders faster than anyone. Her name is
Divya, she is thirteen, and until October she had never won a match that mattered.

Sebastian watched her lose one in the district round and saw exactly what he expected to see. Every
stroke she owned in the drills was still there — but between strokes, where a match actually
happens, everything went. She chose the wrong shot when the rally got long. She rushed her serve
after losing a point. At nine points down she started playing shots she had never practised at all,
as if the drills belonged to a different girl.

So he changed Thursdays. The second hour is now nothing but practice matches, with scoring, with an
umpire, with her parents allowed to sit and watch — because an audience changes the body, and she
had never once practised being watched. And he gave her a rule for the gap between points, the only
part of a match nobody drills. Before every serve she must say her plan in her head in one short
sentence — serve wide, then attack the backhand. Not a paragraph. One sentence, every point, no
exceptions, even at match point, *especially* at match point.

The first three Thursdays were ugly. She lost to boys she beat in every drill, and cried once in
the car. The fourth Thursday she stopped rushing. By December the sentence had become automatic —
plan, serve, play — and in January she won the district under-fourteens, beating the same girl from
October in straight games.

The strokes did not improve between October and January. The strokes were never the problem.

---

## 3. The idea in plain English

Divya's drills are days 27 to 35. Today is Thursday's second hour — full matches, scored, watched.
And her one-sentence rule between points is exactly yesterday's routing sentence said before every
problem: the piece of match play that must be drilled until pressure cannot remove it.

### The phase, on one table

Nine days compressed. Each row is a tool, its invariant — the sentence that makes it correct — and
its tell.

| Tool | The invariant to say | The tell | Day |
|---|---|---|---|
| Opposite ends | any answer lies between `left` and `right`; each move discards only proven-impossible pairs | sorted + pairs | [028](../day-028-opposite-ends/README.md) |
| Read and write | `items[0:write]` is finished and correct; `write <= read` always | compact in place | [029](../day-029-read-write-pointer/README.md) |
| Fast and slow | the gap shrinks by exactly one per step inside a loop | cycle, middle, O(1) | [030](../day-030-fast-and-slow/README.md) |
| Fixed window | when `i` enters, `i - k` leaves; add and subtract, never recompute | "of length k" | [031](../day-031-fixed-window/README.md) |
| Variable window | neither edge ever moves backwards; ~2n moves | "longest", "shortest" | [032](../day-032-variable-window/README.md) |
| Window + map | the map means *what is in the window now* — hence `del` at zero | condition on counts | [033](../day-033-window-with-a-map/README.md) |
| Counting window | after the shrink, `right - left + 1` valid subarrays end here | "how many" | [034](../day-034-at-most-k/README.md) |

Under pressure you will not re-derive these. You will either say the invariant from memory or write
code you cannot defend. That is what today's two matches test.

### What pressure actually removes, and the counter-habit

Watching candidates fail mock rounds shows the same three losses, in order:

**The routing minute goes first.** The heart speeds up, the hands want to type, and the checklist
gets skipped — the exact skill [day 035](../day-035-choosing-the-pattern/README.md) built. The
counter is Divya's rule: one routing sentence, out loud, before any code, no exceptions. It costs
thirty seconds and it is the thing being scored.

**Edge cases go second.** The empty input, the single element, the all-same input — known cold on a
calm day, forgotten at minute thirty. The counter is a fixed list run at a fixed time: after the
code compiles in your head, before you declare done, the same five inputs from
[day 026](../day-026-strings-revision/README.md), every time, as a ritual rather than a decision.

**Honesty goes third.** Stuck candidates go quiet, and quiet is the one unrecoverable state — the
interviewer cannot help, cannot score the thinking, cannot even tell it is happening. The counter:
narrate the stuck. *"I have the window but my condition isn't monotonic — let me check what breaks
it."* Saying you are stuck, with specifics, reads as method; silence reads as absence.

### How to run today's mock

Same protocol as [day 026](../day-026-strings-revision/README.md). Set a timer for thirty-five
minutes per problem. Stand up, talk continuously, no notes, no lesson files open. Route out loud,
name the invariant, write the code in one pass, then run the five test inputs by voice. Only then
read the transcript in §5 and score yourself against it — not on whether the code matches, but on
whether the *sentences before the code* match.

---

## 4. The picture

The whole phase as one corridor, with yesterday's desk at the front:

```
                       the routing desk (035)
                                |
        +-----------------------+----------------------+
        |                                               |
   pointer side                                    window side
        |                                               |
  +-----+---------+--------+                +-----------+-----------+
  |               |        |                |           |           |
opposite       read +   fast +          fixed        variable    counting
ends (028)     write    slow            (031)        (032/033)   (034)
               (029)    (030)                           |
                                                  shape A: minimise
                                                  shape B: maximise
        exits:  "subsequence" -> 024    negatives in a sum -> 037/038
                "indices" + unsorted -> hash map (021)
```

**What to notice:** seven rooms, three exits. A mock is passed as much by walking *out* of the
corridor at the right moment as by picking the right room in it.

The match ritual, as the clock you run today:

```
 min 0-2     read twice; ask the contract questions (alphabet? negatives? empty?)
 min 2-3     ROUTE OUT LOUD: one sentence, pattern + shape + invariant
 min 3-5     example by hand; state brute force and its cost
 min 5-20    code, narrating; invariant said before each loop
 min 20-25   the five test inputs, by voice, including the empty one
 min 25-35   follow-ups, cost argument, the honest "what I'd check with more time"
```

**What to notice:** the code gets fifteen of thirty-five minutes. Candidates who type at minute one
spend those fifteen minutes twice.

---

## 5. The code, built step by step

Two problems, worked as transcripts. Route each yourself before reading on.

### Match one — Container With Most Water

> *"You are given heights of vertical lines at positions 0 to n−1. Pick two lines; together with
> the x-axis they hold water. Return the largest area you can trap. `[1,8,6,2,5,4,8,3,7]` → 49."*
> — LeetCode 11.

**Beat 1, clarify.** *"Area is distance between the lines times the shorter height? And the lines
between don't matter?"* Yes and yes. *"Can heights be zero?"* They can — area just comes out zero.

**Beat 2, route out loud.** *"The answer is about a pair of positions, not a contiguous run — so
pointer side, not a window. It isn't sorted, but I don't need sortedness for a pair chosen by
position: I need an argument for discarding pairs. Widest pair first, then move inward — opposite
ends, if I can find the discard argument."*

**Beat 3, brute force.** *"Every pair: n²/2 areas, O(n²). Fine to name, not to write."*

**Beat 4, the invariant — the whole question.** *"Start at the outermost pair. The area is width
times the shorter line. Now: moving the **taller** line inward can never help — the width shrinks,
and the height is still capped by the same shorter line. So every pair using the current shorter
line at this width or less is already beaten, and I can discard the shorter line entirely. That is
the opposite-ends move: each step throws away a whole set of pairs that are proven no better."*

That paragraph is [day 028](../day-028-opposite-ends/README.md)'s row-and-column deletion argument
with area instead of a target sum. Producing it — not the code — is what the problem is for.

**Beat 5, code.**

```python
left, right = 0, len(height) - 1
best = 0
while left < right:
    width = right - left
    if height[left] < height[right]:
        best = max(best, width * height[left])
        left += 1
    else:
        best = max(best, width * height[right])
        right -= 1
```

*"Record the area this pair makes, then discard the shorter line. Ties: moving either is safe —
both are capped by the same height — so the `else` taking the right one is fine."*

**Beat 6, test.** `[1,8,6,2,5,4,8,3,7]` → 49 — the pair of 8s... no: width 7 × height 7, the 8 at
index 1 and the 7 at the end. Say the winning pair out loud, that is the point of testing by hand.
`[1,1]` → 1. `[4,3,2,1,4]` → 16, the two ends. `[1,2,1]` → 2. Single element → loop never runs, 0.

### Match two — Number of Substrings Containing All Three Characters

> *"Given a string of only a, b and c, count the substrings that contain at least one of each.
> `"abcabc"` → 10."* — LeetCode 1358.

**Beat 1, clarify.** *"Exactly the letters a, b, c, nothing else? Count substrings, so positions
matter — the same text at two places counts twice?"* Yes.

**Beat 2, route out loud.** *"Substrings — contiguous, window side. 'Count', not 'longest' — a
counting window, day 034. But the condition is 'contains all three', an **at least**, where day 034
counted **at most** — so the counting line lands differently, and I want to re-derive it rather
than paste it."*

Saying that a memorised line does not fit, before it bites, is the mark of the invariant being real.

**Beat 3, the re-derivation.** *"For at-most conditions, validity survives *shortening*, so I count
windows ending at `right` that start at or after `left`. For at-least conditions it is the mirror:
validity survives *lengthening* — if `s[left..right]` contains all three, then any start *earlier*
than `left` also works. So: shrink the window while it is still valid, walking `left` past every
start that works, and then `left` itself is the count of valid starts — positions 0 to `left - 1` —
for this `right`. Add `left`, not `right - left + 1`."*

**Beat 5, code.**

```python
count: defaultdict[str, int] = defaultdict(int)
left = 0
total = 0
for ch in s:
    count[ch] += 1
    while len(count) == 3:          # still valid: keep shrinking
        count[s[left]] -= 1
        if count[s[left]] == 0:
            del count[s[left]]      # len(count) is the condition -> del, as always
        left += 1
    total += left                   # starts 0 .. left-1 were all valid
```

*"The shrink loop deliberately overshoots — it stops only when the window is invalid again — which
is exactly what makes `left` equal the number of valid starts. And the `del` at zero is
load-bearing for the same reason as ever: `len(count)` is the condition."*

**Beat 6, test.** `"abcabc"` → 10, and check the first hit by hand: at the first `c`, `left` walks
to 1, adding 1 — the substring `"abc"`. `"aaacb"` → 3. `"abc"` → 1. `"aab"` → 0 — no `c`, the
while never fires, total stays 0. Empty string → 0.

### The complete solutions

```python
from collections import defaultdict


def max_area(height: list[int]) -> int:
    """LeetCode 11. Opposite ends: discard the shorter line — moving the taller
    one can only shrink width under the same height cap."""
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        width = right - left
        if height[left] < height[right]:
            best = max(best, width * height[left])
            left += 1
        else:
            best = max(best, width * height[right])
            right -= 1
    return best


def number_of_substrings(s: str) -> int:
    """LeetCode 1358. At-least counting: shrink while VALID, then add left —
    every start before left works for this right."""
    count: defaultdict[str, int] = defaultdict(int)
    left = 0
    total = 0
    for ch in s:
        count[ch] += 1
        while len(count) == 3:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        total += left
    return total


if __name__ == "__main__":
    print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))   # 49
    print(max_area([1, 1]))                        # 1
    print(max_area([4, 3, 2, 1, 4]))               # 16
    print(max_area([1, 2, 1]))                     # 2

    print(number_of_substrings("abcabc"))          # 10
    print(number_of_substrings("aaacb"))           # 3
    print(number_of_substrings("abc"))             # 1
    print(number_of_substrings("aab"))             # 0
```

---

## 6. What it costs

### Match one

Each iteration retires one line — `left` up or `right` down — and they start `n - 1` apart, so
exactly `n - 1` iterations of constant work. **O(n) time, O(1) space.** Against the brute force's
`n²/2` pairs: at `n = 100,000`, five billion areas against a hundred thousand steps.

### Match two

The standard two-edges count: the loop body runs `n` times, and `left` advances at most `n` times
across the whole run — at most `2n` moves, constant map work each (the map holds at most three
keys). **O(n) time, O(1) space** — the alphabet is fixed at three, so even the map is constant.

### The cost that is actually being examined today

Neither problem's asymptotics are the test — everything in this corridor is `O(n)`, as
[day 035](../day-035-choosing-the-pattern/README.md) said. What the mock measures is the **argument
per move**: why discarding the shorter line is safe, why `left` equals the count of valid starts.
An `O(n)` loop you cannot defend scores like a guess, because the follow-up — *"why is that
correct?"* — arrives every single time.

---

## 7. The traps

### The near-miss: moving the taller line

The plausible-but-backwards version of match one:

```python
if height[left] > height[right]:
    left += 1          # moving the TALLER side
else:
    right -= 1
```

```
8
```

On `[1,8,6,2,5,4,8,3,7]` it returns 8 instead of 49. It walks straight past the winning pair,
because it keeps the short line — the binding constraint — and discards the tall one that cost
nothing. The fix is the argument, not the sign: the shorter line caps every pair it could ever form
at this width or less, so the shorter line is the one with nothing left to offer.

### The near-miss: yesterday's counting line in today's problem

Paste [day 034](../day-034-at-most-k/README.md)'s line into match two:

```python
while len(count) == 3:
    ...shrink...
total += right - left + 1        # at-most line in an at-least problem
```

```
11
```

Eleven, not ten — and the wrongness is instructive: after shrinking *while valid*, the window is
invalid, so `right - left + 1` counts the substrings ending here that do **not** contain all three.
It computes the exact complement: 21 total substrings of `"abcabc"` minus the 10 good ones. The
counting line is not a formula to paste; it is the answer to *"which starts are valid for this
right?"* — asked fresh each time. At-most: starts at or after `left`. At-least: starts before
`left`.

### The real error: the empty-input reflex, again

Match one with a careless initial:

```python
left, right = 0, len(height) - 1
print(height[left])
```

On `height = []`:

```
Traceback (most recent call last):
  File "day36.py", line 2, in <module>
    print(height[left])
IndexError: list index out of range
```

The loop version survives (`while 0 < -1` never runs) — but any code that touches `height[0]`
before the loop dies on empty input. The five test inputs exist precisely because at minute thirty
you will not *think* of the empty case; you will only *run the ritual* — which is why it is a
ritual.

### The mock-round trap: the silent stall

Not a code bug, and it fails more mocks than any code bug: sixty seconds of silence while stuck.
There is always a legal sentence available — the invariant you are trying to prove, the input that
is bothering you, the two candidate rooms you are torn between. *"I want opposite ends but I
haven't justified discarding a line yet — let me test the discard on a three-element example"* is
progress the interviewer can score. Silence is not. If you catch yourself quiet during today's
timer, that — not the code — is the thing to repeat next Thursday.

---

## 8. In the interview

### How it gets asked

- *"Let's do a couple of problems."* — the screening round itself; this phase supplies most of its
  mediums.
- *"Talk me through your approach before you code."* — an explicit request for the routing
  sentence and the invariant; candidates who code first are stopped and asked again.
- *"Why is that correct?"* — the invariant question, arriving mid-code, on schedule.
- *"That works — can you do it without the extra memory?"* — the pointer-side upgrade question:
  hash map to opposite ends, stack to backwards pointers.

### What to say out loud, in the first ninety seconds

The compressed match ritual — this is the script, for any problem in the family:

1. **The two contract questions this family always needs.** *"Can values be negative? Can the input
   be empty?"* — one kills windows-over-sums, the other kills careless initials.
2. **The routing sentence.** *"Contiguous and counting, so a counting window"* — or wherever the
   five questions land, said as one breath.
3. **The invariant, before any code.** *"Each move discards only pairs that are proven no better"* /
   *"every start before left is valid"* — the sentence you will be asked to defend later, volunteered
   now.
4. **Brute force and target.** *"Pairs at O(n²); the pointer argument gives O(n)."*
5. **The test list, promised.** *"I'll finish with empty, single, all-same, all-different, and the
   adversarial one."* Saying it early means you cannot forget it late.

### The follow-ups

**"Why is discarding the shorter line safe? Convince me."**
Fix the current pair: left line height 3, right line height 8, width 10 — area 30, capped by the 3.
Every other pair that still uses the left line has width at most 9 and height still at most 3 — the
shorter line caps the height whatever partner it gets — so all of those pairs are at most 27:
strictly worse than what I already recorded. The left line's future is exhausted, and I discard it.
The taller line makes no such promise: a still-taller partner inside could pair with it for a bigger
area, so it must stay. That is the same shape of argument as the pair-sum walk from day 028 — each
move deletes a set of candidates that have been *proven* beaten, never merely guessed — and it is
why meeting in the middle having recorded the best along the way is a proof, not a heuristic.

**"Your counting answer added `left`, but yesterday you added `right - left + 1`. Which is right?"**
Both — for different conditions, and the difference is which direction validity survives. An
at-most condition survives shortening: if the window is valid, every later start also gives a valid
window, so after shrinking to the tightest valid window I count starts from `left` to `right` —
`right - left + 1`. An at-least condition survives lengthening: if `s[left..right]` contains all
three letters, every *earlier* start does too, so I shrink while still valid, overshooting to the
first invalid start, and the valid starts are 0 to `left - 1` — exactly `left` of them. Pasting one
formula into the other problem computes the complement — 11 instead of 10 on `"abcabc"`, which is
21 total substrings minus the 10 good ones. The habit that protects me is asking "which starts are
valid for this right?" fresh, every time, rather than remembering a line.

**"You're three minutes in and stuck between two approaches. What do you do?"**
Say so, with the specifics: name both rooms and the missing piece — "this is either opposite ends
or a window; what decides it is whether the answer is about a pair or a run, and the phrase
'substring' settles it — window." If it does not settle in one sentence, I take the smallest example
that could distinguish them and run both intuitions on it by hand for sixty seconds; a
three-element input usually kills one of the two. What I do not do is pick silently and start
typing, because a wrong room discovered at minute twenty is unrecoverable, and because the
interviewer scores the deciding process — which only exists for them if it happens out loud.

### A model answer

The first two minutes of match two, as one continuous piece — compare your recording against it:

> "Count the substrings containing at least one a, one b and one c. Substrings — contiguous, so
> window side. Count, not longest — so a counting window. But my counting line from at-most
> problems assumes validity survives shortening, and here it's the opposite: containing all three
> survives *lengthening*. So I'll re-derive: for each right edge, if the window from `left` still
> contains all three, every earlier start works too. I'll shrink while the window is still valid,
> and then the number of valid starts for this right is exactly `left`. I add `left` each step.
>
> The window carries a three-key count map, and since my loop condition is `len(count) == 3`, I
> must delete keys at zero or the length lies. Both edges only move forward — at most 2n moves —
> so O(n) time, O(1) space, the map never holds more than three keys.
>
> Before I code: empty string gives 0, a string missing one letter gives 0 — the while never fires
> and left stays 0 — and `"abc"` should give exactly 1. Those are my first three tests. Writing it
> now."

---

## 9. Recall card

- **The invariant is the answer.** Seven tools, seven sentences — say the sentence before the code,
  every time; a loop you cannot defend scores as a guess.
- **Container: discard the shorter line** — it caps every pair it could still form at smaller
  width. Moving the taller line returns 8 where 49 exists.
- **Counting has two directions.** At-most survives shortening → add `right - left + 1`. At-least
  survives lengthening → shrink while valid, add `left`. The wrong one computes the complement.
- **Pressure eats, in order: the routing minute, the edge cases, the narration.** Counter each with
  a ritual — one sentence before code, five inputs by voice, stuck-narration instead of silence.
- **Everything here is O(n) and the interviewer knows it.** The score lives in the sentences
  between the lines of code.
