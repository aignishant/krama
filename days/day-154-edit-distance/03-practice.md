---
day: 154
track: practice
title: "Practice — Edit distance"
status: written
---

# Day 154 · Practice

**DSA topic:** Edit distance
**System design topic:** Design Twitter

---

## Code these, in this order

One rule for the whole set: **write the base-case loops before the recurrence, and write the name of each
branch as a comment on the line.** The base cases are not zeros here, and the delete/insert confusion is
invisible to every test that checks only the number.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Edit Distance | LeetCode 72 (Medium) | Three branches, named, and the non-zero base cases. |
| 2 | One Edit Distance | LeetCode 161 (Medium) | Where the table is overkill and two pointers win. |
| 3 | Delete Operation for Two Strings | LeetCode 583 (Medium) | Edit distance with replace removed. |
| 4 | Minimum ASCII Delete Sum | LeetCode 712 (Medium) | Weighted costs, and what happens to the base cases. |
| 5 | Regular Expression Matching | LeetCode 10 (Hard) | The same table shape with a different move set. |
| 6 | Wildcard Matching | LeetCode 44 (Hard) | The same again, and where greedy beats the table. |

### On problem 1, leave the base cases out

Allocate the table as all zeros and skip both base-case loops. Run on `"horse"` / `"ros"` and record the
answer. **Say why it is too small and why a small wrong number is worse than a crash.**

### On problem 1, add one on a match

Change the match branch to `dp[i-1][j-1] + 1`. Run `edit_distance("abc", "abc")` and record the result.
**Say what that number claims, in words.**

### On problem 1, swap delete and insert

Swap the two branches. Run on five random string pairs and record whether any answer changes. **Then write the
reconstruction and run it.** Say exactly where the bug becomes visible, and why no distance test could have
caught it.

### On problem 1, reconstruct with `and` instead of `or`

Write the walk-back with `while i > 0 and j > 0`. Run it on `""` → `"abc"` and record the script. **Say what
was lost and why.**

### On problem 1, collapse to two rows

Write it, then deliberately leave `current` as `[0] * (m+1)` instead of `[i] + [0] * m`. Run on `"horse"` /
`"ros"` and record the answer. **Say which base case you just deleted.**

### On problem 4, generalise carefully

Convert your uniform-cost version to weighted. **Note what happens to the two base-case loops** — write down
what they become and why. Then say what property of the distance you have just lost.

### On problems 5 and 6, keep the state and change the moves

Before coding either, write `dp[i][j]` as a sentence. Then list the moves available at each cell. **Notice the
state is identical to edit distance and only the move set changed.**

### Then the fuzzy-search drill

Build a list of ten thousand words. Time: (a) computing full edit distance against all of them; (b) adding the
length filter; (c) adding the row-minimum early exit. Record all three. **Then say what a BK-tree or a trie
would change, and by roughly how much.**

---

### The base-case drill

1. Give both base cases and say what each means in words.
2. Say why they are not zeros, and where that habit comes from.
3. Say what the answer looks like when they are missing.
4. Say what they become when the costs are weighted.

### The branch drill

1. Name all three operations and give the cell each reads.
2. For each, say which index moves and why.
3. State the rule in one sentence.
4. Say what the match branch does and what it does not do.
5. Say why swapping delete and insert passes every distance test.

### The reconstruction drill

1. Say where the walk-back starts and stops.
2. Give the four cases in order.
3. Say why the loop condition is `or`.
4. Say what the branch order decides.
5. Say what reconstruction costs in time and in space.

### The variants drill

1. Damerau-Levenshtein: the extra operation, the condition, and why it matters.
2. Weighted: what changes and what property is lost.
3. Delete-only: the formula in terms of LCS.
4. Banded: what it is for and when it is valid.

### The fuzzy-search drill

1. Compute the cost of comparing one query against 100,000 words.
2. Give the two cheap filters and roughly what each saves.
3. Explain a BK-tree in two sentences.
4. Explain the trie approach in two sentences.
5. Say which you would pick for a search box and why.
6. Say what you would rank the survivors by, and why not distance alone.

### The break-it drill

Trigger each and record the exact output or error:

1. Missing base cases.
2. `+ 1` in the match branch.
3. Swapped delete and insert, checked only by distance.
4. `while i > 0 and j > 0` in the walk-back.
5. Missing `[i]` in the collapsed version's row start.
6. Two 100,000-character strings.
7. Two Unicode strings that look identical.

Six of the seven give no error at all. Name them.

---

### The scoping drill

1. Give your in-scope and out-of-scope lists.
2. Say why saying the out list matters.
3. Say what you would cut first if given ten minutes.

### The timeline drill

1. Compute the read-to-write ratio and say what it justifies.
2. Say how the user timeline is built and why nothing clever is needed.
3. Say why the home timeline cannot be a query.
4. Say what the Snowflake id buys you, in three separate ways.
5. Give the Redis structure, the cap, and what the score is.

### The celebrity drill

1. Do the 100-million-follower fan-out arithmetic.
2. Compute the size of that follower id list.
3. Say what that size implies about the graph service's API.
4. Describe the hybrid and why the read-side merge is cheap.
5. Describe the partial-fanout refinement.

### The graph drill

1. Say which two questions the graph must answer.
2. Give both sharding options and what each makes fast and slow.
3. Say what you do and what it costs.
4. Say what the consistency cost is, concretely.

### The search drill

1. Say why the timeline index cannot serve search.
2. Describe an inverted index in one sentence.
3. Say how a two-term query is answered.
4. Say why you bound the posting lists.
5. Say why shard by time and not by term.
6. Say why indexing is asynchronous, and what the alternative would cost.

### The trending drill

1. Say what ranking by raw count produces.
2. State what trending actually measures.
3. Say why the baseline must be seasonal.
4. Explain a count-min sketch, including why `min`.
5. Give the memory comparison against exact counting.
6. Say the property that makes sketches the right choice, not just a smaller one.
7. Say what the sketch does *not* give you, and what you keep alongside it.

### The sizing drill

1. Give storage for tweets, timelines, graph and search index.
2. Say which is the smallest and why that is surprising.
3. Give the read-path latency breakdown.
4. Compute the cache size for 48 hours of tweets.
5. Say what moving the hit rate from 90% to 95% does.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the minimum number of edits to turn one string into the other.*
   The state, the non-zero base cases with their meanings, the free match, all three branches named with the
   index rule, and the complexity.

2. *Now show me the actual edits.*
   The walk-back with its four cases, the `or` condition and what it saves, the tie-break, and where the
   swapped-branch bug finally becomes visible.

3. *Design Twitter.*
   The scope, the 100:1 ratio, both timelines and why they differ, the celebrity arithmetic including the
   800 MB, and why search and trending need different structures.

---

## Before you move on

- [ ] I write the base-case loops first, and they are not zeros.
- [ ] I know what each base case means in words.
- [ ] I know a match is free, with no `+1`.
- [ ] I can name all three branches and which index each moves.
- [ ] I can state the index rule in one sentence.
- [ ] I know why swapping delete and insert passes every distance test.
- [ ] I can reconstruct with the four cases.
- [ ] I know the loop condition is `or` and what `and` loses.
- [ ] I know the branch order picks among equal-cost scripts.
- [ ] I can collapse to two rows, including the row-start base case.
- [ ] I know the collapse gives up reconstruction.
- [ ] I can generalise to weighted costs, including the base cases.
- [ ] I know weighted costs break symmetry, and why that matters.
- [ ] I know what Damerau adds and why spell-checkers use it.
- [ ] I can give time and space, and where the table stops being viable.
- [ ] I know a spell-checker does not call this 100,000 times.
- [ ] I can give both cheap filters and explain a BK-tree or a pruning trie.
- [ ] I would rank suggestions by frequency, not distance alone.
- [ ] I can scope Twitter out loud, in and out.
- [ ] I can compute the read-to-write ratio.
- [ ] I know the user timeline is a plain query.
- [ ] I know why the home timeline cannot be one.
- [ ] I can give three things the Snowflake id buys.
- [ ] I can do the 100-million-follower arithmetic, both numbers.
- [ ] I know why that forces a streaming cursor in the graph API.
- [ ] I can give both graph sharding options and say what I do.
- [ ] I know why search needs a separate inverted index.
- [ ] I know why it shards by time and is asynchronous.
- [ ] I know trending measures change, not volume, and why the baseline is seasonal.
- [ ] I can explain a count-min sketch and why sketches merge.
- [ ] I answered all three questions above out loud.
