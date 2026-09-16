---
day: 50
track: practice
title: "Practice — Binary search revision and mock round"
status: written
---

# Day 050 · Practice

**DSA topic:** Binary search revision and mock round
**System design topic:** Class diagrams and the UML you will actually draw

**Theme:** Designing a JSON API

---

## Code these, in this order

A mock, so the protocol rules: **twenty-five minutes a problem, standing, talking the whole time,
nothing open — and Yesudas's two seconds first.** Name the chapter and the tell before you solve
anything, and score yourself on the naming separately from the code.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Find First and Last Position of Element in Sorted Array | LeetCode 34 (Medium) | The warm-up: two bounds, and whether find-then-walk still tempts you. |
| 2 | Search in Rotated Sorted Array | LeetCode 33 (Medium) | Discarding on a range, and the `<=` in the sortedness test, cold. |
| 3 | Koko Eating Bananas | LeetCode 875 (Medium) | Whether the answer-space instinct fires without the word "capacity" in it. |
| 4 | Split Array Largest Sum | LeetCode 410 (Hard) | The phase's summit, re-derived a week later, with the DP named and rejected. |

### On problem 1, respect the warm-up

Two template calls, one character apart, and the guard in the right order. If it takes more than ten
minutes, the phase needs re-reading rather than more problems. Then run `[8] * 200000` with target 8
and confirm you did not write a walk.

### On problem 2, say the sentence before the code

*At least one half is properly sorted, because there is exactly one break point and one point cannot
be in two halves.* Then write it. Then run the un-rotated array, the break-at-the-end array, and the
single-element array. A special case for any of those means the real bug is still there.

### On problem 3, notice there is no capacity in sight

The word "capacity" does not appear and the shape is identical. The tell is "the minimum k such that
it can be finished in h hours". Bound it at 1 to `max(piles)` — say why the lower bound is not 0 and
what it raises. Ceiling division: `(pile + k - 1) // k`, checked by hand on `pile = 7, k = 3`.

### On problem 4, name the DP and reject it with numbers

Before writing the search, say: *"there's a dynamic-programming solution at O(n²k) — a thousand
elements and fifty parts is fifty million operations and a fifty-thousand-cell table, against about
thirty thousand operations and three integers here."* Then write the binary search. Then diff it
against your LeetCode 1011 solution from day 046 — if they differ anywhere except the names, one of
them is wrong.

### The two-second drill

Ten phrasings. Name the chapter and the tell in under ten seconds each, out loud, no code:

1. Answer 100,000 range-sum queries on a fixed array.
2. Find the index of a target in a sorted array with duplicates.
3. Find the minimum in an array that was sorted and then rotated.
4. Find any element greater than both its neighbours.
5. Find the smallest divisor such that the sum of the divisions is at most a threshold.
6. Find the largest minimum distance when placing c items in n stalls.
7. Find the median of two sorted arrays.
8. Find the maximum of an unsorted array.
9. Find the smallest k such that exactly k groups can be formed.
10. Find the cube root to six decimal places.

Numbers 1, 8 and 9 are not binary search. Say what each of them is instead, and why.

### The pre-flight drill

Say the five bugs of the phase from memory, each with the input that catches it:

1. The convention blend — which two things must never be mixed, and what are the two symptoms?
2. `hi = mid - 1` — when is it right and when does it throw away the answer?
3. Discarding on one comparison — which day introduced the need for a proof, and what is the input?
4. A range that misses the answer — name two problems where it happens, and the one-line habit that
   catches it.
5. A meaningless `lo` — what does it raise, and what is the general rule?

### The one-loop drill

Write `first_true` from memory, then express each of these as a question passed to it — one line
each, no new loops:

1. The first index whose value is at least the target.
2. The last index holding the target.
3. How many values lie in `[a, b]`.
4. The smallest capacity shipping everything in d days.
5. The largest gap at which c items can still be placed.
6. The minimum of a rotated array.
7. A peak.

### The cost drill

Answer in under five seconds each, with numbers not letters:

1. Comparisons for a plain search at a million.
2. Comparisons for first-and-last at a million.
3. Worst case for a rotated search with duplicates at a million.
4. Operations for a search-on-answer with n = 50,000 and a range of 25 million.
5. Peak versus maximum on an unsorted array of a million.
6. Space, for every tool in the phase.

### The four-minute diagram drill

Set a timer for four minutes and draw the class diagram for a **library** — the model you built on
[day 044](../day-044-first-and-last-occurrence/README.md) — in whatever tool you like, talking the
whole time. Then score it:

- [ ] Six to nine boxes, no more.
- [ ] A multiplicity on every relationship line.
- [ ] Hollow triangle for inheritance, dashed for implements, used consistently.
- [ ] Between a third and a half of the boxes have no fields or methods at all.
- [ ] No getters, no constructors, no `created_at`.
- [ ] Nothing crosses anything: spine down the middle, hierarchies at the sides, interface at an edge.
- [ ] I said a design decision out loud for at least three of the boxes.
- [ ] I said what I left out, unprompted.

Then draw the same thing again in Mermaid and check it renders.

### The wrong-diagram drill

For each request, say which diagram it wants — class, sequence, or neither — and why:

1. "Show me how these fit together."
2. "Walk me through what happens when a book is returned late."
3. "What are your classes?"
4. "How does the fee get calculated, and who calls whom?"
5. "Draw the deployment."

### The symbol drill

From memory, and then check:

1. The five Mermaid arrow forms and what each means.
2. The four multiplicities you actually use.
3. What a filled diamond means, what a hollow one means, and the one sentence you would say instead of
   drawing either.
4. How many boxes are readable from where the interviewer sits, and what you do at fifteen.

---

## Build these, in all three languages

*Three exercises, easiest first. Each one says what it is really testing. Every
exercise is done three times: once in Python, once in Go, once in C++.*

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Twelve parcels, twelve slips | Whether every failure in the API comes out in one shape, with every problem listed at once. |
| 2 | Missing is not zero | Telling an absent field from an empty one, in the language where decoding erases the difference. |
| 3 | A PATCH that leaves things alone | Optional fields, partial updates, and what "not sent" means for each field type. |

Every exercise starts from the lesson's server. Use `curl -i` so the status line is visible, and
keep the twelve commands from exercise 1 in a file; you will run them again on every later day
that touches this server.

### 1. Twelve parcels, twelve slips

Write a script of twelve `curl` commands: a good create, a blank name, a missing city, an age of
200, an age of `"thirty"`, a body of `hello`, a body of `[1,2,3]`, an unknown field `town`, a
duplicate name, a get of id 99, a delete of id 2 twice, and a PUT with a missing field. Run it
against each server and paste all twelve status lines and bodies into a comment. Every error
body must have the same outer shape, `error.code` must be one of your fixed words, and the
blank-name-plus-bad-age case must list both problems. In Python, add
`model_config = ConfigDict(extra="forbid")` and show the `town` case change from 201 to 422. Done
means twelve pasted responses per language and no error body that breaks the shape.

### 2. Missing is not zero

Add an optional field, `newsletter: bool`, that defaults to `false` when absent and must be a
boolean when present. Then prove, with three requests each, that absent, `false` and `true`
are handled: absent stores `false`, `false` stores `false`, `"yes"` is a validation error naming
the field. In Go this is `*bool` and a `nil` check; in Python it is `bool = False`; in C++ it is
`contains` then `is_boolean()`. Then, in a comment on the Go version, explain in two sentences
what would go wrong with `Newsletter bool` and a rule of "newsletter is required". Done means
the nine responses pasted per language and the Go comment written.

### 3. A PATCH that leaves things alone

Add `PATCH /users/{id}` that changes only the fields present in the body: `{"city": "Goa"}` changes
the city and nothing else, `{}` changes nothing and answers 200 with the unchanged user, and
`{"age": 200}` is a validation error. In Python every field of a `UserPatch` model is
`str | None = None` and you apply `model_dump(exclude_unset=True)`; in Go every field is a
pointer; in C++ you walk the keys that are present. Then answer the hard case in a comment: how
does a caller clear an optional string field, and how does your API tell "set to empty" from
"not sent"? Done means the three PATCH cases give 200, 200, 400 in all three languages, and the
comment answers the clearing question.

## Say these out loud

### DSA and system design

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Two problems, no hints, talk as you go.*
   Run the recognition minute out loud on problem 4 as if it were unseen: chapter, precondition,
   range, question, return meaning — then the invariant and the predicted cost, before any code.

2. *Draw the class diagram for what you just described.*
   The plan sentence, the central class with its reason, the spine with multiplicities, one design
   decision narrated, the interface with its second implementation, and what you left out.

3. *How do you decide in ten seconds whether a problem is binary search at all?*
   The first question is not "is it sorted?" — it is "what is the answer?" Say both branches, the
   precondition for each, and the three exits.

### Languages

*Three questions from today. Answer each in two minutes, standing up, no notes.*

1. What should a 400 response body look like?
   The fixed outer shape, the machine code and the human message, the `fields` list with every
   problem at once, never echoing secrets, and the same shape for 404 and 409. Then say the one
   line of code in each language that makes it impossible to build a different one.
2. How do you tell a missing field from an empty one in each language?
   Pydantic knows which keys it saw; nlohmann's `contains`; Go's `*int` and `nil`. Then the
   near-miss in each: extras ignored by default, `[]` inserting a null, and `Age int` decoding a
   missing age as zero.
3. Walk me through the status code for each CRUD outcome, and defend the two that people argue
   about.
   200, 201, 204, 400 or 422, 404, 409, 500, and then: a repeated DELETE, and validation as 400
   versus 422. Give your choice and the reason, and say what matters more than the number.

## Before you move on

- [ ] I did all four problems standing, talking, with the naming scored separately.
- [ ] I named all ten phrasings in the two-second drill, including the three that are not binary
      search.
- [ ] I can recite the five pre-flight bugs with their checking inputs.
- [ ] I wrote `first_true` from memory and expressed all seven problems as questions to it.
- [ ] I can give every cost in the phase as a number, not a letter.
- [ ] I drew the library diagram in four minutes and it passed all eight checks.
- [ ] I can produce the five Mermaid arrow forms and the four multiplicities from memory.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] The three lesson servers give the same five status lines for the five commands in section 5, with one error shape.
- [ ] Exercise 1 has twelve responses pasted per language and every error body keeps the shape.
- [ ] Exercise 2 handles absent, `false`, `true` and `"yes"` correctly in all three, and my Go comment explains the zero-value trap.
- [ ] Exercise 3's PATCH gives 200, 200, 400 in all three, and my comment says how a caller clears a field.
- [ ] I can write the `writeError` and `validate` shapes from memory in Go, and name the two decoder settings.
- [ ] I can say why `validate` takes `const json&` in C++, and what `[]` does on a missing key.
