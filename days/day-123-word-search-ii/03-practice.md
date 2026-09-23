---
day: 123
track: practice
title: "Practice — Tries in interviews: word search II"
status: written
---

# Day 123 · Practice

**DSA topic:** Tries in interviews: word search II
**System design topic:** Clocks, ordering, and why time is a lie

---

## Code these, in this order

One rule for the whole set: **write the mark line and the restore line in the same keystroke.** Type
`board[r][c] = "#"`, then immediately type `board[r][c] = character` two lines below it, then fill in the
loop between them. Every other bug in these problems announces itself. That one does not.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Word Search | LeetCode 79 (Medium) | Backtracking on a grid, one word, restore on the way out. |
| 2 | Word Search II | LeetCode 212 (Hard) | Moving the word list *inside* the walk. The whole lesson. |
| 3 | Word Break II | LeetCode 140 (Hard) | A trie plus memoised backtracking, without a grid. |
| 4 | Concatenated Words | LeetCode 472 (Hard) | Searching a trie from inside a trie walk. |
| 5 | Stream of Characters | LeetCode 1032 (Hard) | The reversed trie — the trick nobody sees the first time. |

### On problem 2, write the slow version first and time it

Solve it once by calling your problem 1 solution in a loop over the words. Run it on a 12 × 12 grid with
3,000 words and record how long it takes, or record that you gave up waiting. Then write the trie version and
record that number. Two numbers, and the ratio between them is the answer to "why a trie".

### On problem 2, remove each pruning and measure

Three runs on the same input:

1. Full solution.
2. Without `child.word = None` after a find.
3. Without the node deletion at the end.

Record the runtime and the output length for each. Version 2 has a wrong output as well as a slow one; say
which and why.

### On problem 2, build the adversarial input yourself

A 12 × 12 grid of nothing but `a`, and words `["a"*k for k in range(1, 11)]`. Run all three versions above on
it. This is the case the judge uses to fail solutions that have a trie but no node deletion.

### On problem 5, say why the trie is reversed

Write down, in one sentence, what is being stored and why storing the words forwards does not work when
characters arrive one at a time and you must answer after each one.

---

### The two-walks drill

1. Say what two things move together during the search, and what happens when one cannot move.
2. Say what `node.children.get(character)` returning `None` means in words.
3. Say why the word list is inside the walk and not outside it.
4. Give the naive cost and the trie cost, and name the factor that disappears.

### The node drill

1. Say why the node stores the word rather than a boolean.
2. Say what that saves on every step of every path.
3. Say what setting `word = None` after a find does — both effects.
4. Say when the node-deletion pruning fires, and what it buys.

### The backtracking drill

1. Write the mark-loop-restore block from memory.
2. Say what the output looks like when the restore is missing — not what error, what output.
3. Say why `#` is a safe marker and what would not be.
4. Give the non-mutating alternative and its cost.

### The cost drill

1. Derive `M × N × 4 × 3^(L−1)` out loud, saying where the 4 and the 3 come from.
2. Put the LeetCode limits in and produce the two numbers.
3. Say why the bound is loose, and what the real cost is bounded by.
4. Give the space cost, separating the trie from the call stack.

### The break-it drill

Trigger each and record the exact output or error:

1. The restore line removed, on a grid where two answers share a cell.
2. `child.word = None` removed, on a 2 × 2 grid of `a` with the word `aa`.
3. The word loop left on the outside, on the 3,000-word input.
4. A trie built from 2,000-character strings, searched recursively.
5. `explore` called without the bounds check.
6. The node deletion placed *before* the restore line instead of after.

---

### The clock drill

1. Say how far an unsynchronised clock drifts in a day, and show the arithmetic.
2. Give NTP's realistic skew in one data centre and across regions.
3. Say two things NTP cannot give you, beyond a smaller number.
4. Say what a leap smear is and why Google built one.

### The two-clocks drill

1. Name the two clocks on every machine and what each is for.
2. Say what `time.time()` does that `time.monotonic()` does not.
3. Give three places where using the wrong one is a correctness bug.
4. Describe the rate-limiter symptom and trace it back to the cause.

### The happens-before drill

1. State the three rules of happens-before, without mentioning a clock.
2. Define concurrent, and say what it does *not* mean.
3. Say why "Deepak saw the kettle was warm" settles an order that two clocks could not.
4. Give an example from a real system of each of the three rules.

### The Lamport drill

1. Write the update rule from memory, both on an event and on receipt.
2. State exactly what it guarantees, in one direction.
3. Say what it does not guarantee, and why that matters.
4. Say how you turn it into a total order, and what the tie-break is.

### The vector-clock drill

1. Write the update rule from memory.
2. Give the comparison procedure and its three outcomes.
3. Work through the `[1,0,0]` versus `[0,0,1]` example out loud.
4. Say what a vector clock tells you that it does not tell you.
5. Give the metadata size at 10 nodes and at 500 nodes.

### The numbers drill

1. Compute how many writes fall inside a 50 ms skew window at 10,000 writes a second.
2. Compute the daily conflict count at 1,000 writes a second and a 0.5% conflict rate.
3. Compare metadata for Lamport, HLC, and vectors at 10 and 500 nodes, on a 200-byte value.
4. Compute the storage cost of 500-node vectors on a billion values.
5. Compute Spanner's commit-wait cost and its effect on hot-row throughput.

### The trade-offs drill

1. Say what last-write-wins costs and when it is the right choice.
2. Say what vector clocks cost and where they stop scaling.
3. Say what an HLC gives you and the one thing it does not.
4. Say what TrueTime buys and what you pay, in milliseconds and in hardware.
5. Give the design move that makes this entire topic disappear, and when it is available.

### The failure drill

For each, say what happens and what you would build:

1. A phone edits offline for four hours and then syncs.
2. Two nodes write the same key 30 ms apart with 50 ms of skew, under last-write-wins.
3. NTP steps a clock back 200 ms during a duration measurement.
4. A lock lease is measured on the wall clock and the clock jumps forward.
5. A 500-node cluster tries to attach vector clocks to every value.
6. Two users concurrently rename the same document.
7. An event log is sorted by timestamp during an incident review.

Two of the seven are not fixed by any clock, however good. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find all dictionary words in this letter grid.*
   Backtracking plus a trie, the sentence about `W` leaving the multiplication, the two positions moving
   together, storing the word on the node, both prunings, the cost, and the restore-the-cell bug named before
   you write it.

2. *Two events have the same timestamp. Which happened first?*
   You cannot tell, and why — skew against event gap, with a number. Then happens-before, then Lamport with
   its one-directional guarantee, then vector clocks for detecting concurrency.

3. *Two replicas disagree about a key's value. Resolve it.*
   The three metadata cases, last-write-wins named as data loss with the Cassandra example, vector-clock
   comparison with its three outcomes, and merging as a product decision rather than a storage one.

---

## Before you move on

- [ ] I can say in one sentence why a trie beats searching each word.
- [ ] I know which factor leaves the multiplication, and by how much on the LeetCode limits.
- [ ] I can write the two-positions-moving-together search from memory.
- [ ] I know why the node stores the word and not a boolean.
- [ ] I know both effects of clearing the word after a find.
- [ ] I know when node deletion fires and which test case it saves.
- [ ] I write the restore line at the same time as the mark line.
- [ ] I know the restore bug produces missing words, not an error.
- [ ] I can derive the cost formula and say where the 4 and the 3 come from.
- [ ] I can give the non-mutating alternative and its price.
- [ ] I built the all-`a` adversarial grid and ran it.
- [ ] I can say what NTP achieves and what it cannot give me.
- [ ] I can name the two clocks and what each is for.
- [ ] I can give three bugs caused by using the wall clock for durations.
- [ ] I can state happens-before in three rules with no clock in them.
- [ ] I can define concurrent and say what it does not mean.
- [ ] I can write the Lamport update rule and state its one guarantee.
- [ ] I know why a Lamport clock cannot detect conflicts.
- [ ] I can write the vector clock rule and the three comparison outcomes.
- [ ] I can give vector metadata sizes at 10 and 500 nodes.
- [ ] I know last-write-wins loses data and that it is Cassandra's default.
- [ ] I can say what an HLC gives me and the one thing it does not.
- [ ] I can quote TrueTime's epsilon and the commit-wait cost.
- [ ] I know the single-owner move that makes this problem disappear.
- [ ] I answered all three questions above out loud.
