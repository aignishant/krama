---
day: 33
track: practice
title: "Practice — Window plus hash map: the longest-substring family"
status: written
---

# Day 033 · Practice

**DSA topic:** Window plus hash map: the longest-substring family
**System design topic:** Transactions and ACID

---

## Code these, in this order

Four problems, all the same eight-line skeleton with a different condition. **Before writing a line of
any of them, say the condition out loud** — what the map holds, and what makes the window invalid.
That sentence is the problem; the rest is typing.

Before each one, ask:

1. What does the map hold, and is it a map at all — or does it collapse to one integer?
2. What is the invalid condition, in one sentence?
3. Does the condition use `len(count)`? If yes, the `del` at zero is mandatory — say why.
4. Maximise, so: shrink while invalid, record after. Say it before you type it.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Longest Substring Without Repeating Characters | LeetCode 3 (Medium) | The skeleton itself, and whether `left` can ever move backwards. |
| 2 | Fruit Into Baskets | LeetCode 904 (Medium) | Recognising "at most 2 distinct" through a story about fruit. |
| 3 | Max Consecutive Ones III | LeetCode 1004 (Medium) | Noticing the map collapses to a single counter when the alphabet is size two. |
| 4 | Longest Repeating Character Replacement | LeetCode 424 (Medium) | The `window_len - max_freq > k` condition, and defending the `max_freq` optimisation. |

### On problem 1, break it both ways

Write the `while`-shrink version and get it passing. Then write the jump version with a last-seen map,
and delete the `last[ch] >= left` guard. Run both on `"abba"`. The broken one returns 3 instead of 2.

Then answer, out loud:

1. At which index did `left` move backwards, and what did the window contain afterwards?
2. Why can the `while` version never have this bug?
3. Why does `left` moving backwards also destroy the `O(n)` argument?

### On problem 2, forget the `del` on purpose

Write it correctly first — it is "longest with at most 2 distinct" wearing a costume. Confirm
`[1,2,1]` gives 3 and `[1,2,3,2,2]` gives 4.

Then remove the `del` at zero and run `[1,2,3,2,2]` again. Watch the answer collapse. Say exactly
which quantity `len(count)` stopped meaning, and finish the sentence: *"the `del` is mandatory exactly
when..."*

### On problem 3, say the simplification before you use it

Before coding, say: *"two kinds of value, so the map collapses to one integer counting zeros."* Then
write it with just `zeros`, no dictionary. Confirm `([1,1,1,0,0,0,1,1,1,1,0], 2)` gives 6.

Then say what the invalid condition would have been with a full map, and why the integer version is
the same algorithm.

### On problem 4, write the honest version first

Write it recomputing `max(count.values())` in the condition. Confirm `("AABABBA", 1)` gives 4. State
the cost, and why `O(26)` per step is still `O(n)`.

Only then write the version that carries `max_freq` and never decreases it, and answer the question
that actually gets asked: why is a stale, too-high `max_freq` safe? The argument is in §3 of the
lesson — say it without looking, in three sentences.

### The condition drill

For each, give the invalid condition and what the window carries, in under five seconds:

1. Longest substring without repeating characters.
2. Longest substring with at most k distinct characters.
3. Fruit into baskets.
4. Longest run of 1s after flipping at most k zeros.
5. Longest substring you can make uniform by changing k characters.
6. Does s2 contain a permutation of s1?

Number 6 is the odd one out — say why it is day 031's shape, not day 032's.

### The ACID drill

Say the table from memory: for each letter — the failure it prevents, and the mechanism that
delivers it. Four letters, eight facts, under a minute.

Then the two one-liners an interviewer listens for:

1. Which letter is the odd one out, and why?
2. Which letter is the interesting one, and why?

### The commit-timeline drill

Say what happens on `COMMIT`, in order: where the changes already are, what gets `fsync`ed, when
success is reported, and when the data pages are actually written. Then say why that ordering is both
the safety and the speed.

### The arithmetic drill

From memory, in under two minutes:

- One `fsync` at 1 ms — naive commits per second, and what group commit does to that number.
- 1,000 rows inserted one transaction each, against one transaction total. Roughly how long each?
- A transaction left open 4 hours on a table taking 10,000 updates a second — how many dead row
  versions pile up, and what does that do to the database?
- `synchronous_commit = off` — how much faster, and what exactly can be lost?

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the length of the longest substring without repeating characters.*
   Ask about the alphabet first. Name the shape and where the recording goes. Say why the `del` at
   zero matters, why `left` never moves backwards, and finish with the `O(n)` argument.

2. *What does ACID stand for, and why does it matter?*
   Each letter with a failure attached and a mechanism named. Then the two follow-up one-liners: the
   odd letter, and the interesting letter.

3. *Two users transfer money from the same account at the same time. What can go wrong, and how do
   you stop it?*
   The lost update, why being inside a transaction does not prevent it at read committed, and two
   fixes — arithmetic in the SQL, or `SELECT ... FOR UPDATE`.

---

## Before you move on

- [ ] I say the invalid condition in one sentence before writing any window-plus-map problem.
- [ ] I `del` at zero whenever `len(count)` is in the condition, and I can say why.
- [ ] I can name the input where a missing `last[ch] >= left` guard makes `left` go backwards.
- [ ] I notice when the map collapses to one integer, and I say so.
- [ ] I can give each ACID letter with a failure and a mechanism, from memory.
- [ ] I can say what happens on `COMMIT`, in order, including where the `fsync` sits.
- [ ] I answered all three questions above out loud.
