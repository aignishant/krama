---
day: 22
track: practice
title: "Practice — Anagrams: the sorting versus counting choice"
status: written
---

# Day 022 · Practice

**DSA topic:** Anagrams: the sorting versus counting choice
**System design topic:** gRPC and when binary protocols win

---

## Code these, in this order

Four problems built on one idea: **find a canonical form, then compare or group by it.** For every
one of them, say out loud what your canonical form is before writing a line.

Before each one, ask:

1. What is my canonical form, and why is it identical for exactly the things that should match?
2. Is my key hashable? (A list is not.)
3. Does the length check help, and is anything else relying on it?
4. Case, spaces, Unicode — what did I assume, and did I say so?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Valid Anagram | LeetCode 242 (Easy) | Two solutions with different complexities, offered unprompted. The one-liner alone is an incomplete answer. |
| 2 | Group Anagrams | LeetCode 49 (Medium) | The canonical form as a dictionary key, and knowing that a list cannot be one. |
| 3 | Find All Anagrams in a String | LeetCode 438 (Medium) | A count that slides. Recomputing per window is `O(n·k)`; updating two entries per step is `O(n)`. |
| 4 | Group Shifted Strings | LeetCode 249 (Medium) | Inventing a canonical form yourself. `abc` and `bcd` are the same "shape" — what key captures that? This is the real skill. |

### On problem 1, produce both

Write `sorted(a) == sorted(b)` first, state `O(k log k)`, and then say *"but I can do better"* without
being asked. Write the counting version. Then write the single-array version that increments for `a`
and decrements for `b`, and answer:

1. Why can it return early the moment a count goes negative?
2. Why does that early exit need the length check to be correct?
3. Run it on `("aab", "ab")` with the length check removed. What comes back, and why?

### On problem 2, break your own key

Write the grouping solution with `groups[sorted(word)].append(word)` — with `sorted` and no `join` —
and run it. Read the error. Say the reason in one sentence, using the word *hashable*.

Then write the count-key version and confirm both produce the same groups on
`["eat","tea","tan","ate","nat","bat"]`.

Then test both on `[]` and on `[""]`. One of those is easy to get wrong.

### On problem 4, design the key before you code

`["abc","bcd","xyz","az","ba","a","z"]` groups into `[["abc","bcd","xyz"],["az","ba"],["a","z"]]`,
because each of those can be shifted into the others.

Do not look anything up. Spend ten minutes deciding what a canonical form for "same shape" is. Say
your candidate out loud, then find the input that breaks it. The wrap-around at `z` is where most
first attempts fail.

This is the most valuable exercise on this page, because inventing a canonical form is the skill the
whole day is about, and [day 064](../day-064-grouping/README.md) is entirely built on it.

### The set-versus-counter drill

Predict, then run:

```python
print(set("aacc") == set("ccac"))
print(sorted("aacc") == sorted("ccac"))
print(sorted("aab") == sorted("abb"))
```

Then say in one sentence what a set throws away that a count keeps, and why that makes it the wrong
structure for this problem but the right one for "how many distinct characters".

### The measurement drill

Run this and read the numbers before you decide what to ship.

```python
from collections import defaultdict
import random, string, time

random.seed(1)

def g_sort(words):
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())

def g_count(words):
    groups = defaultdict(list)
    for w in words:
        key = [0] * 26
        for ch in w:
            key[ord(ch) - ord("a")] += 1
        groups[tuple(key)].append(w)
    return list(groups.values())

for k in (10, 100, 1000, 5000):
    words = ["".join(random.choices(string.ascii_lowercase, k=k)) for _ in range(2000)]
    row = [f"k={k:>5}"]
    for f in (g_sort, g_count):
        s = time.perf_counter(); f(words)
        row.append(f"{f.__name__} {time.perf_counter()-s:.4f}s")
    print("  ".join(row))
```

Then answer:

1. At `k = 100`, which is faster? Is that what the complexity said would happen?
2. At what word length does the `O(k)` version start to win?
3. Explain the gap. (One is compiled C, the other is interpreted Python.)
4. Which would you ship for ordinary words, and which would you *say* in an interview?

Questions 3 and 4 have different answers, and being comfortable with that is the point.

### The canonical-form drill

For each, name a canonical form in under ten seconds:

1. Two strings are anagrams.
2. Two words are the same ignoring case.
3. Two phone numbers are the same, written differently (`+91 98765 43210`, `09876543210`).
4. Two points are on the same line through the origin.
5. Two lists contain the same elements regardless of order **and** duplicates matter.
6. Two binary trees have the same shape and values.
7. Two strings are shifts of each other (`abc`, `bcd`).

Numbers 4 and 6 are the ones to think about; both come back much later in the course.

### The gRPC drill

Answer each in one or two sentences, out loud:

1. What three things does gRPC change compared with REST + JSON over HTTP/1.1?
2. Which of those three do engineers actually feel every day, and why?
3. What is a field tag in a `.proto` file, and what may you never do to one?
4. Name the four call shapes gRPC supports. Which one does REST have?
5. What is deadline propagation, and what goes wrong without it?
6. Why can a browser not call a gRPC service directly?
7. Why does gRPC break an ordinary layer-4 load balancer, and what are the two fixes?
8. Draw the boundary: which traffic in a system is gRPC, and which is REST?

### The arithmetic drill

From memory, in under two minutes:

- A four-field message as JSON versus protobuf — the two sizes and the ratio.
- With headers: a REST call versus a gRPC call, total bytes.
- At 100,000 calls a second — traffic per day, both ways, and the difference.
- JSON parse at 10 µs versus protobuf at 2 µs, decoded on both sides — cores at 100,000 calls/second.
- A cold HTTPS handshake at 3 round trips of 0.5 ms, against work of 2 ms — what fraction of the
  latency is setup?

Then say the sentence those numbers buy you: *"at a thousand calls a second none of this is
measurable, and the price is a build step and losing `curl`."*

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Are these two strings anagrams? Now group a list of words into anagram groups.*
   Ask the contract questions. Name the canonical-form idea before either solution. Give the
   one-liner, then improve it unprompted. For grouping, say explicitly that there is no comparison
   between words — a dictionary turns `O(n²·k)` into one pass. Finish with which you would ship.

2. *Why would a company use gRPC between its own services?*
   Three changes, ranked by what matters. One number. Streaming and deadlines. Then draw the
   boundary — inside gRPC, edge REST — and name debuggability as the cost, unprompted.

3. *Given ten thousand words, find any two that are anagrams of each other.*
   The trap is the nested loop. Say what the naive version costs, then the dictionary version, then
   what changes if this has to run on a million words across several machines. (The key is a pure
   function of the word, so sharding by key needs no merge step.)

---

## Before you move on

- [ ] I say the words "canonical form" when I see this family of problem.
- [ ] I offer two solutions with different complexities, unprompted.
- [ ] I know a dictionary key must be hashable, and I reach for `tuple` or `"".join` automatically.
- [ ] I never use a set where multiplicities matter, and I can name the input that proves it.
- [ ] I write the length check and can say what depends on it.
- [ ] I can name gRPC's three changes and rank them by what engineers actually feel.
- [ ] I can say why field tags may never be renumbered.
- [ ] I answer "gRPC or REST" by drawing the boundary, not by picking a winner.
- [ ] I can redraw the inside-versus-edge diagram from memory, in whatever tool I like.
