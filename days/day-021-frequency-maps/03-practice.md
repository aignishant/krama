---
day: 21
track: practice
title: "Practice — Character counting and frequency maps"
status: written
---

# Day 021 · Practice

**DSA topic:** Character counting and frequency maps
**System design topic:** GraphQL versus REST

---

## Code these, in this order

Four problems where the answer is *build a count, then look at it*. The skill being trained is
recognising that in the first five seconds, so before you write anything, say out loud which phrase
in the problem statement told you.

Before each one, ask:

1. Do I need **how many**, or only **whether**? (Counter or set.)
2. What is the alphabet? Can I use 26 slots, or do I need a dictionary?
3. How many passes does this need, and can it be done in one?
4. What is the answer for the empty input?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Ransom Note | LeetCode 383 (Easy) | Counter subtraction, and whether you notice that "can I build A from B" is a counting question and not a searching one. |
| 2 | First Unique Character in a String | LeetCode 387 (Easy) | Two passes, and being able to say why one pass is impossible. |
| 3 | Sort Characters By Frequency | LeetCode 451 (Medium) | `most_common`, then building the output with `join` — not `+=`. Two lessons meeting. |
| 4 | Find All Anagrams in a String | LeetCode 438 (Medium) | A count that **moves**: add the entering character, remove the leaving one. This is the sliding window of [day 033](../day-033-window-with-a-map/README.md) arriving early. |

### On problem 1, do it three ways

Solve it with `Counter` subtraction, then with a plain dictionary and an explicit check, then with a
26-element array. Time all three on a large input. Then say which you would write in an interview and
why — and note that the answer is the `Counter` one, with the others available if asked.

### On problem 2, argue with yourself

Spend five minutes genuinely trying to solve it in one pass before reading anything. Then write down
the exact reason it cannot be done. The sentence you want is about *when the information becomes
available*, not about cleverness.

Then look up the stream version — "first non-repeating character so far, after each character" — and
work out why that one **can** be done incrementally, and what extra structure it needs.

### On problem 4, build the moving count by hand

Do not jump to the solution. Take `s = "cbaebabacd"` and `p = "abc"` and, for each window of length
3, say out loud what the count looks like and whether it matches the count of `p`. Then notice you
are recomputing the whole count each time, which is `O(n × k)`.

Then find the improvement: when the window slides one step, only two characters change. Decrement the
one leaving, increment the one arriving. Say the cost of that version before you code it.

### The three-ways drill

Write the character count for `"hello"` three ways from memory, in under sixty seconds:

```python
# 1. plain dict
# 2. defaultdict
# 3. Counter
```

Then run this and explain each result:

```python
counts = {}
for ch in "hello":
    counts[ch] += 1
```

```python
from collections import defaultdict
counts = defaultdict(int)
counts["a"] += 1
if counts["z"] == 0:
    pass
print(dict(counts))
```

```python
from collections import Counter
c = Counter("hello")
print(c["z"], dict(c))
```

The second one has a surprise in it. Name it.

### The silent-bug drill

Predict the output before running:

```python
def counts26(s):
    arr = [0] * 26
    for ch in s:
        arr[ord(ch) - ord("a")] += 1
    return arr

print(counts26("Hello"))
```

Most people predict an `IndexError`. Say what actually happens and why, then say which position the
capital `H` was counted into and how you would work that out without running it. Then fix the
function two different ways.

### The pattern-recognition drill

For each phrase, say in under three seconds which structure you reach for — **counter**, **set**,
**sorted**, or **moving counter** — and why:

1. "the most common word in this document"
2. "does this array contain any duplicates"
3. "are these two strings anagrams"
4. "the first character that appears exactly once"
5. "how many distinct characters"
6. "the longest substring with at most two distinct characters"
7. "can this note be built from these letters"
8. "which element appears more than n/2 times"

Numbers 2 and 5 want a set, not a counter. Number 6 is a window. Number 8 has a famous `O(1)`-space
answer worth looking up after you have given the counting one.

### The cost drill

State time **and** space for each, counting out loud rather than naming a class:

1. `Counter(s)` on a string of length n.
2. The two-pass first-unique solution.
3. The naive `s.count(ch)` inside a loop.
4. A 26-element array count on a string of length n.
5. `len(set(s))`.

For number 4, say why the space is `O(1)` and not `O(26)`, and be able to defend it.

### The GraphQL drill

Answer each in one or two sentences, out loud:

1. What are the two specific problems GraphQL was built to solve? Give an example of each.
2. What does a GraphQL response shape have to do with the request shape?
3. What is the single biggest thing you give up, and roughly what does it cost in server load?
4. What is the N+1 problem in GraphQL, and what fixes it?
5. Why is depth limiting not optional?
6. Why does a GraphQL server return `200` even when the query failed?
7. Name two large companies using GraphQL and two deliberately staying with REST, and say why the
   second group is right for their case.
8. What is the cheap middle option, and why might you try it first?

### The arithmetic drill

From memory, in under two minutes:

- Three REST calls at 120 ms each, sequentially and in parallel, against one GraphQL call.
- 11 KB of REST responses where 2 KB is rendered — what is saved per screen, and per million loads?
- 420 requests a second, 80% cacheable, 90% CDN hit rate — origin load with REST, and with GraphQL.
- 50 orders each needing a customer — queries with and without DataLoader.
- A social graph averaging 200 friends, three levels of nesting — how many nodes?

Then say the sentence those numbers buy you: *"the caching loss is bigger than the payload saving."*

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the first non-repeating character in a string.*
   Clarify index-or-character and the alphabet. Name the `O(n²)` version. State the two-pass
   structure, and — before being asked — say why one pass is impossible. Give `O(n)` time and the
   space answer that depends on the alphabet.

2. *When would you choose GraphQL over REST?*
   Name the two problems it solves, then immediately name what it costs, with the caching number.
   Then give a **condition**, not a preference. Finish with the `?fields=` middle path.

3. *Here is a string of a billion characters that will not fit in memory. Find the first character
   that appears exactly once.*
   The counter is bounded by the alphabet, not the length, so pass one streams in constant memory.
   Then the interesting half: how do you avoid a second pass over the data? (Record first positions.)

---

## Before you move on

- [ ] I hear "how many times" and reach for a counter without thinking about it.
- [ ] I use a set when the question is "whether", not "how many".
- [ ] I can write the count three ways, and I know why plain `counts[ch] += 1` raises.
- [ ] I can say why first-unique needs two passes, and that two passes is still `O(n)`.
- [ ] I state the alphabet assumption out loud before using `ord(ch) - ord("a")`.
- [ ] I can name GraphQL's two problems solved and its four real costs.
- [ ] I know what DataLoader is for and can say the 51-versus-2 number.
- [ ] I answer "GraphQL or REST" with a condition, never a preference.
- [ ] I can redraw the both-ways round-trip diagram from memory, in whatever tool I like.
