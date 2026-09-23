---
day: 12
track: practice
title: "Practice — Searching an array: linear search, done properly"
status: written
---

# Day 012 · Practice

**DSA topic:** Searching an array: linear search, done properly
**System design topic:** How your code becomes a running service

---

## Code these, in this order

Four problems that are all one scan. The scanning is trivial; the **contract** is the
exercise — what you return, which occurrence you return, and what happens when there is
nothing to return.

For each problem, before writing anything:

1. Say what you return when the target is absent.
2. Say which occurrence you return if there are several.
3. Say what happens on an empty input.
4. Then write it, and confirm the empty case works with no special-case guard.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Search Insert Position | LeetCode 35 (Easy) | The "not found" answer is not `-1` here — it is where the value *would* go, which is a different contract entirely. Read the statement twice. |
| 2 | Find Numbers with Even Number of Digits | LeetCode 1295 (Easy) | Search by a **condition**, not by equality. This is the case binary search cannot handle, and the reason linear search survives. |
| 3 | Find All Numbers Disappeared in an Array | LeetCode 448 (Easy) | "Find all", not "find first" — so no early exit is possible. The naive version searches for each candidate and is `O(n²)`; a set makes it `O(n)`. |
| 4 | First Bad Version | LeetCode 278 (Easy) | Deliberately the counter-example. The linear scan is correct and too slow, and the problem exists to make you notice the property that allows something better. Solve it linearly first, then see why. |

### On problem 4, do this properly

- Write the linear version. It is correct. Submit it and see what happens.
- Then answer: what property of the input made a faster solution possible?
- Then say what that property is worth: at `n = 10⁹`, how many checks does the linear
  version need, and how many does halving need?
- This is [day 042](../day-042-binary-search-idea/README.md) arriving early, and it is worth
  meeting it here as "the thing linear search cannot do".

### The contract drill

For each of these, say the three answers out loud — absent, duplicates, empty:

1. "Find the index of the target."
2. "Find the largest element."
3. "Find the first element greater than 100."
4. "Find how many times the target appears."

Then check yourself against one rule: **could the caller confuse your 'not found' answer with a
real answer?** If yes, the contract is wrong.

### The falsy drill

Predict the output of this before running it:

```python
def find(items, target):
    for i, x in enumerate(items):
        if x == target:
            return i
    return None

items = [7, 3, 9]
if find(items, 7):
    print("found")
else:
    print("not found")
```

Then explain the bug in one sentence, fix it, and say which five Python values are falsy.

### The break-even drill

An array of one million elements, searched `k` times. Work these out with the arithmetic
shown:

- The cost of `k` linear searches.
- The cost of building a hash set once, then `k` lookups.
- The cost of sorting once, then `k` binary searches.
- The `k` at which the hash set overtakes linear search.
- The `k` at which sorting overtakes linear search.

### The one to try in a terminal

If you have a project with a Dockerfile, run `docker build .` twice in a row and compare the
times. If you do not, read any `Dockerfile` you can find and answer two questions: which lines
would invalidate the layer cache when you change one line of source code, and is there
anything in it that should have been an environment variable instead.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *Find the index of a target. What do you return if it is not there?*
   Ask the contract question first. Then give the code, say where the fallback return goes and
   why, give best/average/worst, and note why absence is always the worst case.

2. *How does the code you wrote end up running on a server?*
   Give the eight links in order. Get to health checks and rollback without being asked, then
   volunteer the migration caveat.

3. *Something is broken in production right after a deploy. What do you do?*
   Give the first action, the reason with the two timings compared, and the one thing you check
   before doing it.

---

## Before you move on

- [ ] I ask what to return for "not found" before writing a search.
- [ ] I know why `-1` is riskier in Python than in Java, and what I would use instead.
- [ ] I never write `if result:` when `0` is a valid answer.
- [ ] I can say why absence is always the worst case, in one sentence.
- [ ] I can name the eight links from commit to serving traffic, and say which one cannot be
      rolled back.
