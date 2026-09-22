---
day: 19
part: "1.1"
title: "Repair a window until every character is distinct"
ids: [DSA-19]
level: working
prerequisites: ["Day 8 sets; contiguous strings"]
failure: true
---

# Repair a window until every character is distinct

Core reading: explanation, worked trace, and readiness. The production section offers optional
depth for another sitting; keep the existing track budget and record partial work honestly.

## One-line answer

Extend right, remove from left until the incoming character is absent, then record the longest valid window.

## The story

You highlight text with no repeated character. A new character repeats one already inside
the highlight; deleting the whole highlight wastes a suffix that is still useful.

## The idea in plain language

Recognize a longest contiguous range whose validity can be restored by removing a prefix.
Here valid means each Unicode code point occurs at most once. A substring is contiguous;
a subsequence can skip positions and is a different problem. Python string iteration exposes
code points, not bytes or user-perceived grapheme clusters. No normalization is requested.

Retain left, the active set of characters, and best length. A repeat means shrink until that
specific older occurrence leaves, then insert the incoming character. Retaining unrelated
suffix characters is exactly what a restart-from-empty strategy fails to do.

## Why Krama needs it

This develops DSA-19 for the [Week 3 review](../../day-021-week-3-review/LESSON.md).
The tracks remain independent; use only this subject's prerequisites.

## The source behind it

[Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/),
LeetCode 3, returns a length and includes empty strings. The local contract explicitly counts
Unicode code points; compare the official input domain before submitting. Checked 2026-09-22; details are in the [source ledger](../../../docs/SOURCES.md).
The trace and counterexample below are original teaching examples.

## The mechanism

### Worked trace

Trace "abba" using an active set.

| Incoming index/character | Repair before insertion | Active substring | Best |
| --- | --- | --- | --- |
| 0 / a | none | a | 1 |
| 1 / b | none | ab | 2 |
| 2 / b | remove a, then old b | b | 2 |
| 3 / a | none | ba | 2 |

After each insertion, the set equals the characters at indices left..right, each once.
The chosen left is the earliest valid start for this right endpoint: the older occurrence
of the incoming character forces all earlier starts to fail. Any prefix discarded earlier
remains unusable for a later extension unless its cause leaves, which the advancing left
already accounts for. Thus right-left+1 is the longest valid suffix ending here. Taking
the maximum over all right endpoints covers the global optimum.

Each character enters once and leaves at most once. With expected constant-time set operations,
total time is O(n), despite the inner while loop; active storage is O(k) for maximum window
size k. A useful alternative stores last-seen positions: left=max(left,last[ch]+1) for a
seen character, then update last[ch]. The max prevents moving backward. That alternative can
retain O(u) entries for all distinct input code points, even after they leave the window.

## When it breaks

Run this separate teaching demonstration before implementing your own exercise.

```python
text = "abba"
last, left, wrong = {}, 0, 0
for right, char in enumerate(text):
    if char in last:
        left = last[char] + 1  # wrong: can move backward
    last[char] = right
    wrong = max(wrong, right - left + 1)
oracle = max((j - i for i in range(len(text) + 1)
              for j in range(i, len(text) + 1)
              if len(set(text[i:j])) == j - i), default=0)
print("backward-left result:", wrong, "oracle:", oracle)
try:
    assert wrong == oracle, "left moved backward into an invalid window"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert max(2, 0 + 1) == 2  # at the final a: current left=2, previous a index=0
```

**Line by line:** The wrong last-seen version treats an old occurrence outside the active range as a reason
to move left backward. The exhaustive substring oracle counts only distinct-character ranges.
The final assertion illustrates the nondecreasing-left guard, not a full optimized solution.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
backward-left result: 3 oracle: 2
AssertionError: left moved backward into an invalid window
```

**Line by line:** These are the actual printed observations, including the deliberately caught
assertion or exception. A caught failure documents the wrong assumption; later assertions check
the repair on the stated example, not on every possible input.

## In production

Decide whether the product means code points, normalized text, or grapheme clusters before
changing the algorithm. Returning the actual substring also needs tie policy and saved bounds;
slicing every candidate can destroy the intended cost. Expected hash performance is an explicit
assumption. A fixed small alphabet can use a table, but arbitrary Unicode cannot assume 26 slots.

## Check yourself

### Readiness before practice

1. At the second b in "abba", why is one removal insufficient?
2. What goes wrong if last-seen positions move left backward?
3. Why is total shrinking linear rather than quadratic?
4. Which representation retains only active characters, and which retains historical ones?

Use [README.md](README.md) for the assignment and evidence route. Reading does not complete study.
