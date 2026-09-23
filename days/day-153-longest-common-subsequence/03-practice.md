---
day: 153
track: practice
title: "Practice — Longest common subsequence"
status: written
---

# Day 153 · Practice

**DSA topic:** Longest common subsequence
**System design topic:** Design a news feed

---

## Code these, in this order

One rule for the whole set: **write `dp[i][j] uses a[i-1] and b[j-1]` as a comment at the top before you write
the loops.** Every problem here is a two-dimensional prefix-length table, and the off-by-one is the only thing
that will cost you time.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Longest Common Subsequence | LeetCode 1143 (Medium) | The two-dimensional state and both branches. |
| 2 | Longest Palindromic Subsequence | LeetCode 516 (Medium) | The `LCS(s, reversed(s))` reduction. |
| 3 | Delete Operation for Two Strings | LeetCode 583 (Medium) | `n + m - 2·LCS`, in one line. |
| 4 | Shortest Common Supersequence | LeetCode 1092 (Hard) | Reconstruction, not just the length. |
| 5 | Uncrossed Lines | LeetCode 1035 (Medium) | LCS with the strings replaced by number arrays. |
| 6 | Longest Common Substring | classic — write it yourself | The two lines that differ, and where the answer lives. |

### On problem 1, write the off-by-one wrong on purpose

Use `a[i]` and `b[j]` instead of `a[i-1]` and `b[j-1]`. Run on `"abcde"` and `"ace"` and record what happens.
Then try it on two strings where it does *not* raise. **Say why the version that raises is the lucky case.**

### On problem 1, loop from 0

Change both loops to start at 0 and see what you have to add to make it work. **Then say in one sentence what
starting at 1 buys you.**

### On problem 1, print the table

Print the whole `dp` grid for `"abcde"` / `"ace"`. Read one interior cell out loud as a full sentence
containing "the first `i` characters". **Then check that sentence is true by hand.**

### On problem 1, collapse to two rows and then try to reconstruct

Write the two-row version and confirm it agrees. Then attempt to walk back through it. **Say what stops you, in
one sentence**, and say what you would use if you needed both linear space and the string.

### On problem 4, reconstruct rather than count

You need the actual supersequence, so you need the full table. Walk back and emit: on a match, one character;
on a mismatch, the character from whichever side you move from. **Check your output contains both inputs as
subsequences.**

### On problem 6, find both differences

Start from your LCS code and change exactly two things. Run both on `"abcdef"` and `"abzdef"` and record both
answers. **Name the two changes and say which one is the sneaky bug.**

### Then the diff drill

Implement `diff` on two lists of lines using your reconstruction. Run it on two versions of a real file of
yours. Then compute how many cells the table has for two 5,000-line files, and say what Git does instead and
why it gets faster as the files get more similar.

---

### The state drill

1. State it as a full sentence.
2. Say why prefix lengths and not indices.
3. Say what `i = 0` means and what it buys.
4. Say which character `i` refers to, and write it down.

### The recurrence drill

1. Give the match case and say what it means in words.
2. Give the mismatch case and say why there are two options.
3. Say why you cannot tell which to skip.
4. Say where the answer is, and why it is the last cell here but not in LIS.

### The reconstruction drill

1. Say where the walk-back starts and where it stops.
2. Give the three moves and what each means.
3. Say what the tie-break decides.
4. Say what it costs in time and in space.
5. Name the algorithm for linear-space reconstruction.

### The substring drill

1. Give both answers for `"abcdef"` / `"abzdef"`.
2. Say what the mismatch case becomes and why.
3. Say where the answer lives and why.
4. Say which of the two changes is easier to forget.
5. Say what better algorithm exists for the substring version.

### The family drill

Give each as a one-liner and say why it works:

1. Shortest common supersequence length.
2. Minimum deletions to make two strings equal.
3. Longest palindromic subsequence.
4. Minimum insertions to make a string a palindrome.

### The break-it drill

Trigger each and record the exact output or error:

1. `a[i]` instead of `a[i-1]`.
2. Loops starting at 0 without a guard.
3. Substring code returning `dp[n][m]`.
4. Subsequence code returning the table maximum.
5. Reconstruction after the two-row collapse.
6. A table for two 20,000-character strings.
7. An empty string as one input.

Four of the seven give no error at all. Name them.

---

### The fan-out drill

1. Compute the read-to-write ratio and say what it justifies.
2. Give both strategies with their write cost, read cost and read latency.
3. Say which wins and why, in one sentence with numbers.
4. Say exactly where it breaks.

### The celebrity drill

1. Do the 50-million-follower arithmetic.
2. Say what happens to everyone else's posts during those minutes.
3. Describe the hybrid in three sentences.
4. Say why the read-side merge is cheap, using the asymmetry.
5. Say what the threshold is and what kind of number it is.
6. Describe the partial-fanout refinement.

### The storage drill

1. Say what a feed entry contains and what it deliberately does not.
2. Compute both totals at 300M users, ids versus content.
3. Say what the cap is and what happens without it.
4. Say what happens when a user scrolls past the cap.
5. Name the Redis structure and the two commands.

### The pagination drill

1. Show how offset pagination produces duplicates, with post numbers.
2. Say what a cursor contains and why it needs both fields.
3. Say what ranking adds to the problem.
4. Say what the session id is for.
5. Say why the cursor should be opaque.
6. Say why you over-fetch.

### The read-path drill

1. Give the six steps in order with rough timings.
2. Say what hydration is and why it must be batched.
3. Compute batched versus unbatched round trips.
4. Say what the cache hit rate does to database load at this scale.

### The corrections drill

1. Say what deleting a post properly would cost.
2. Say what you do instead and why it is free.
3. Say what it costs, precisely.
4. Say why blocking is the exception.
5. State the general principle in one sentence.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the longest common subsequence of two strings.*
   The state as a sentence, why prefix lengths, both branches with their meanings, where the answer is, and
   the complexity with the space collapse and its cost.

2. *How is that different from longest common substring, and how would you write `diff`?*
   The two changed lines, where each answer lives, LCS as unchanged lines, and why Git uses Myers.

3. *Design a news feed.*
   The read-to-write ratio, both fan-out strategies with numbers, the celebrity arithmetic, the hybrid, ids
   not content, and cursor pagination.

---

## Before you move on

- [ ] I can state the LCS state as a full sentence.
- [ ] I know why prefix lengths beat indices.
- [ ] I write `a[i-1]`, and I know why.
- [ ] I start my loops at 1 and know what that buys.
- [ ] I can give both branches and what each means in words.
- [ ] I know the answer is `dp[n][m]` here and not in LIS.
- [ ] I can reconstruct with the three moves.
- [ ] I know the tie-break decides which valid LCS I get.
- [ ] I can collapse to two rows, with the swap.
- [ ] I know the collapse gives up reconstruction, and can name Hirschberg.
- [ ] I can give both substring differences.
- [ ] I know the substring answer is the table maximum.
- [ ] I can give the four derived one-liners.
- [ ] I know LCS on lines is `diff`.
- [ ] I know what Myers does and why it gets faster on similar files.
- [ ] I can give time and space, and where the table stops being viable.
- [ ] I can compute the feed read-to-write ratio.
- [ ] I can give both fan-out strategies with their costs.
- [ ] I can do the 50-million-follower arithmetic.
- [ ] I can describe the hybrid and the read-side merge.
- [ ] I know why the merge is cheap, via the asymmetry.
- [ ] I know feeds store ids, and both storage totals.
- [ ] I know the cap and what happens past it.
- [ ] I can name the Redis structure and its two commands.
- [ ] I can show how offsets produce duplicates.
- [ ] I know what a cursor contains and why both fields.
- [ ] I know why ranking needs a session id in the cursor.
- [ ] I know hydration must be batched, with the numbers.
- [ ] I know deletes are filtered at read, and why blocking is the exception.
- [ ] I can say when I would not build any of this.
- [ ] I answered all three questions above out loud.
