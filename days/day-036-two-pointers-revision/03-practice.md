---
day: 36
track: practice
title: "Practice — Two pointers revision and mock round"
status: written
---

# Day 036 · Practice

**DSA topic:** Two pointers revision and mock round
**System design topic:** NoSQL: what it actually means

---

## Code these, in this order

Today is a mock, so the protocol matters more than the list. **Thirty-five minutes per problem, a
timer, standing, talking continuously, nothing open.** Route out loud, say the invariant, code in
one pass, run the five test inputs by voice. Score yourself afterwards against §5 of the lesson —
on the sentences before the code, not the code.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Container With Most Water | LeetCode 11 (Medium) | Whether you can *produce* the discard argument — moving the taller line can never help. |
| 2 | Number of Substrings Containing All Three Characters | LeetCode 1358 (Medium) | Re-deriving the counting line for an at-least condition instead of pasting yesterday's. |
| 3 | 3Sum Closest | LeetCode 16 (Medium) | Opposite ends inside a fixed outer loop, unseen variant — tracking nearest instead of equal. |
| 4 | Minimum Window Substring | LeetCode 76 (Hard) | The phase's summit, revisited cold: shape A with a need map and a missing counter. |

Problems 3 and 4 have no transcript in the lesson. That is deliberate — they are the second match
of each pair, done truly unseen.

### On problem 1, argue before you move

Before writing the loop, say the discard argument to the wall: the shorter line caps every pair it
could still form at this width or less, so it is spent. Then break it on purpose — move the taller
line instead — and run `[1,8,6,2,5,4,8,3,7]`. You get 8, not 49. Say which pair the broken version
walked past.

### On problem 2, derive the counting line fresh

Ask the question aloud before coding: *for this right edge, which starts are valid?* If the window
still contains all three after shrinking, the valid starts are everything before `left` — so add
`left`. Then paste yesterday's `right - left + 1` instead and run `"abcabc"`: you get 11, the exact
complement (21 total substrings minus the 10 good ones). Explain why it counts the bad ones.

### On problem 3, name the composition

This is [day 028](../day-028-opposite-ends/README.md)'s 3Sum skeleton with one change. Say what
stays (sort, fix one, walk two) and what changes (record the nearest sum instead of hunting an
exact one — no duplicate-skipping needed, and the update is an `abs` comparison). Test with
`([-1, 2, 1, -4], 1)` → 2.

### On problem 4, respect the summit

If it takes the full thirty-five minutes, that is the honest result. The pieces you own already:
shape A (shrink while valid, record inside), a `need` map, and the `missing` counter that makes
validity O(1). Test on `("ADOBECODEBANC", "ABC")` → `"BANC"` and `("a", "aa")` → `""`.

### The invariant drill

One sentence each, from memory, under five seconds — the sentence that makes the tool correct:

1. Opposite ends.
2. Read and write.
3. Fast and slow.
4. Fixed window.
5. Variable window.
6. Window with a map.
7. Counting window, at-most.
8. Counting window, at-least.

### The stall drill

Practise the recovery sentence. For each stuck-state, say the narration that keeps the round alive:

1. Torn between two rooms.
2. The invariant will not come.
3. A test input just failed and you do not know why.

### The slogan-repair drill

Each sentence below is the failing answer. Say the passing version out loud:

1. "NoSQL is faster."
2. "NoSQL scales better."
3. "MongoDB is schemaless."
4. "We should use NoSQL because we have a lot of data."

### The families drill

For each need, name the family and one product, in under five seconds:

1. Session tokens looked up by id, sub-millisecond.
2. A product page read as one unit, fields varying by category.
3. A million sensor readings a second, queried by device and time.
4. "Friends of friends who bought this."
5. Money moving between two accounts, atomically.

### The arithmetic drill

From memory, in under two minutes:

- A billion events a day — writes per second, and which side of one Postgres node that lands on.
- An author's name embedded in 40,000 documents — the storage cost, the rename cost, and which one
  matters.
- Four sequential round trips at 1 ms against one joined query — the gap, and why it is an
  application bug rather than a database law.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Why is it always safe to move the pointer at the shorter line?*
   The capping argument, a concrete pair with numbers, and the connection to day 028 — each move
   discards only pairs proven beaten, so the walk is a proof.

2. *What is the difference between SQL and NoSQL?*
   Arranged for questions against arranged for serving. The trade in both directions, the four
   families with a product each, where the scaling claim is honestly true, and the relational
   default.

3. *You counted subarrays two different ways this week. When is it `right - left + 1` and when is
   it `left`?*
   At-most survives shortening; at-least survives lengthening. Which starts are valid each time,
   and what the wrong choice computes on `"abcabc"`.

---

## Before you move on

- [ ] I did both mock problems standing, timed, talking — and scored the sentences, not the code.
- [ ] I can say all eight invariants from the drill without looking.
- [ ] I narrated at least one stuck moment instead of going quiet.
- [ ] I can repair all four NoSQL slogans into trade-offs.
- [ ] I can name the family and a product for all five needs in the drill.
- [ ] I know which scale honestly needs NoSQL, with the events-per-day arithmetic.
- [ ] I answered all three questions above out loud.
