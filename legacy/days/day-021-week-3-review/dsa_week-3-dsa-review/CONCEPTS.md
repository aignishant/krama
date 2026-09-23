---
day: 21
part: "1.1"
title: "Recover the proof before the pattern"
ids: [DSA-21]
level: working
prerequisites: ["Days 15–20 two pointers and windows"]
failure: true
---

# Recover the proof before the pattern

Start with the cold assignment in [README.md](README.md). Open this repair lesson only
after the attempt, or record the explanation as help.

Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Choose a pointer move by the candidates it safely eliminates, and state the input assumption that permits it.

## The story

A memorized two-pointer template can pass one example and fail as soon as negatives or repeated characters appear. Review tests whether you can recover the reason for each move from a blank page.

## The idea in plain language

A cold attempt uses no lesson, hint, or prior implementation. Afterward, repair the first
missing reasoning step. An invariant is a statement preserved by every update; a counterexample
is one valid input that disproves a claim. For sorted pairs, endpoint ordering rules out a
whole set of partners. For distinct substrings, the retained window contains no repeated code
point. For a positive threshold window, positivity justifies stopping after the sum falls short.
These are different proofs even though all use moving indices.

## Why Krama needs it

This develops DSA-21 in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

Use the six original lessons linked below for their verified sources; this review introduces no new algorithm contract.
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

Keep the scheduled 5 minutes recall + two 20-minute attempts + 10 critique + 5 logging.
Re-solve Day 15 and Day 19 from blank code; an unresolved hard problem may replace the second.
The local Day 21 fixture checks only Day 19's substring contract. Day 15's local result is a
boolean, while its online companion returns one-based indices. Use the original Day 15
fixtures for that re-solve. Score correctness/explanation/complexity/tests 0–2 each; pass at
6/8 with correctness=2 and at least one hint-free solve. Reading this repair is help.

| Repair topic | Mechanism to reconstruct | Original lesson |
| --- | --- | --- |
| Sorted pairs | Too small eliminates left; too large eliminates right | [Day 15](../../day-015-sorted-pair-existence/dsa_sorted-pair-existence/CONCEPTS.md) |
| Unique triples | Fix one value, search suffix, skip duplicate answers | [Day 16](../../day-016-unique-triples/dsa_unique-triples/CONCEPTS.md) |
| Container capacity | A shorter endpoint limits all narrower pairs retaining it | [Day 17](../../day-017-container-capacity/dsa_container-capacity/CONCEPTS.md) |
| Fixed window | Subtract departure, add arrival | [Day 18](../../day-018-fixed-window-maximum-sum/dsa_fixed-window-maximum-sum/CONCEPTS.md) |
| Distinct substring | Repair repetition without moving left backward | [Day 19](../../day-019-longest-distinct-substring/dsa_longest-distinct-substring/CONCEPTS.md) |
| Positive threshold | Record and shrink repeatedly while qualifying | [Day 20](../../day-020-minimum-positive-window/dsa_minimum-positive-window/CONCEPTS.md) |

Repair trace for `abba`: after a, left=0 and best=1; after b, best=2. The second b moves
left to 2. The final a was last seen at 0, outside the active window. Left stays 2, and the
best remains 2. Assigning left=previous+1 without a maximum moves it backward to 1 and
incorrectly counts `bba`. The active-set approach uses expected O(n) time, O(k) storage for
the largest active window; a last-seen map instead stores up to O(u) distinct code points.
Sorted pair elimination uses O(n) time and O(1) auxiliary space. Nested rescanning can
erase these bounds; justify total pointer moves, not merely the number of loops.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
def distinct_length(text, guard):
    last = {}
    left = best = 0
    for right, char in enumerate(text):
        if char in last:
            candidate = last[char] + 1
            left = max(left, candidate) if guard else candidate
        last[char] = right
        best = max(best, right - left + 1)
    return best

wrong = distinct_length('abba', False)
fixed = distinct_length('abba', True)
print('backward boundary:', wrong, 'monotone boundary:', fixed)
assert wrong == 3 and fixed == 2
assert distinct_length('', True) == 0
```

**Line by line:** The map records historical positions. The guard controls whether old history can undo a later boundary. Both versions run on the same counterexample; the assertions distinguish them and include empty input.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
backward boundary: 3 monotone boundary: 2
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

Use the smallest failing input to repair one claim, then rerun independent boundaries.
Do not call a code-point result a grapheme-cluster count. Record actual help and remaining
uncertainty; memorizing the demonstrated function is not a cold re-solve.

## Check yourself

### Readiness before practice

1. Why does moving left backward invalidate the substring invariant?
2. What sorted-pair candidates are discarded when the endpoint sum is too small?
3. Why do negative values invalidate the positive-window stopping rule?
4. Which contract and fixtures belong to each of the two review attempts?

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.
