---
day: 158
track: practice
title: "Practice — Interval DP"
status: written
---

# Day 158 · Practice

**DSA topic:** Interval DP
**System design topic:** Design YouTube

---

## Code these, in this order

One rule for the whole set: **write the three loops — length, start, split — before you write anything
inside them.** Every problem here has the same skeleton, and the only real decisions are what `k` means and
what joining costs.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Matrix Chain Multiplication | classic — write it yourself | The skeleton, and the three dimension indices. |
| 2 | Burst Balloons | LeetCode 312 (Hard) | The last-not-first inversion, and the inclusive `k`. |
| 3 | Minimum Score Triangulation of Polygon | LeetCode 1039 (Medium) | The same shape once more, so it stops feeling special. |
| 4 | Stone Game | LeetCode 877 (Medium) | Two players, and the minus sign that handles both. |
| 5 | Palindrome Partitioning II | LeetCode 132 (Hard) | An interval table feeding a one-dimensional DP. |
| 6 | Remove Boxes | LeetCode 546 (Hard) | Where two dimensions are not enough. |

### On problem 1, fill it row by row and watch it lie

Write the natural `for i, for j` loops. Run on `dims = [10, 100, 5, 50]` and record the answer. Then run on
`[40, 20, 30, 10, 30]` and record that against the correct 26,000.

**One passes and one does not.** Say which direction the error goes, and why that direction is harder to
notice.

### On problem 1, get the dimensions wrong

Use `dims[i] * dims[k] * dims[j]` instead of `dims[i] * dims[k+1] * dims[j+1]`. Record what happens. **Say why
there is no error**, then derive the correct three indices out loud from the `dims` convention.

### On problem 2, try thinking "first"

Write the recurrence for "burst `k` first" and try to justify it in one sentence. **Find the sentence you
cannot finish.** Then write the "last" version and say what changed about the two halves.

### On problem 2, use `range(i, j)` for `k`

Run it on `[3, 1, 5, 8]` and record the answer against 167. **Say what `k` means in this problem and why the
range must be inclusive**, and how that differs from problem 1.

### On problem 2, remove the padding

Run without the sentinel 1s and record what happens at `i = 0`. **Say why Python does not raise**, and what
value it actually used.

### On problem 2, write it memoised

Write the `lru_cache` version. Confirm it agrees. Time both at `n = 200`. **Say what you paid and what you
bought.**

### On problem 4, remove the minus sign

Write `max(piles[i] + dp[i+1][j], piles[j] + dp[i][j-1])`. Run on `[3, 7, 2, 3]` and record it. **Say what the
minus sign is doing**, in one sentence about whose turn it is.

### On problem 6, find where two dimensions fail

Try `dp[i][j]` alone. Say what information about the boxes to the left of `i` you need and cannot express.
**Then say what the third dimension is.**

### Then the skeleton drill

Write the three-loop skeleton from memory. Then instantiate it for problems 1, 2 and 3 without looking at your
earlier code. **Target two minutes each once the skeleton is down.**

---

### The shape drill

1. State the interval DP state in one sentence.
2. Say what distinguishes it from LCS's two-index state.
3. Give the general recurrence.
4. Say what the three loops are and their order.
5. Give the time and space.

### The fill-order drill

1. Say which two cells the recurrence reads and why they are shorter.
2. Say what the natural order reads instead, and what a zero means there.
3. Say which direction the error goes and why that is worse.
4. Give the second correct order.
5. Say why you would write it memoised instead.

### The inversion drill

1. Say what goes wrong with "burst first", precisely.
2. Say what "burst last" fixes, and about which values.
3. Give the recurrence.
4. Name two other problems that use the same inversion.
5. Say what phrasing in a problem statement should make you try it.

### The k-meaning drill

1. Say what `k` is in matrix chain and what the loop bound is.
2. Say what `k` is in burst balloons and what the loop bound is.
3. Say what goes wrong if you swap them.
4. Say why there is no error either way.

### The space drill

1. Say why there is no one-row collapse here.
2. Say what you can save instead, and by how much.
3. Say what reconstruction costs.
4. Say what actually limits you first, time or space, with numbers.

### The break-it drill

Trigger each and record the exact output or error:

1. Row-by-row fill on a five-matrix chain.
2. `dims[i] * dims[k] * dims[j]`.
3. `range(i, j)` for `k` in burst balloons.
4. No padding in burst balloons.
5. `dp[i][j]` initialised to 0 while minimising.
6. `n = 5,000` with the cubic loops.
7. Stone game without the minus sign.

Six of the seven give no error at all. Name them.

---

### The scoping drill

1. Give your in and out lists.
2. Say why recommendations in particular is out.
3. Say which of the three hard sub-systems you would go deep on first.

### The upload drill

1. Say what is the same as a photo pipeline and what is new.
2. Say why resumable uploads are required here and not there.
3. Give the chunk size and justify it in both directions.

### The transcoding drill

1. Give the compute rule and the daily CPU-hours.
2. Explain chunking and give the wall-time comparison.
3. Say why segments must be cut at keyframes, and what happens otherwise.
4. Say why the worker must be idempotent, and why it matters more here.
5. Give two other optimisations and what each avoids.

### The streaming drill

1. Say who decides the quality, and why that is unusual.
2. Describe the player's loop in three steps.
3. Say why it starts low, with the latency numbers.
4. Say what a segment is, architecturally, and why that matters for the CDN.
5. Give the segment-length trade in both directions.
6. Give the cost argument for adaptive bitrate.

### The storage drill

1. Compute bytes per hour of video and the annual total.
2. Give the untiered and tiered monthly costs.
3. Say what you tier by, and why not age.
4. Say what breaks without a fast restore path.
5. Say why the original is kept, and what re-encoding a rendition costs.
6. Say what CMAF saves.

### The delivery drill

1. Compute daily egress from the watch hours.
2. Give the commercial CDN bill.
3. Say what you do instead at this scale, and roughly where the break-even is.
4. Say what serving everything at 1080p would cost.

### The counting drill

1. Say what a view is, and why that definition matters.
2. Give the two counting paths and what each is for.
3. Say why counts sometimes go down.
4. Compute views per second at this scale.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the cheapest way to multiply a chain of matrices.*
   The range state, the recurrence over splits, the three loops with why length is outermost, the join cost
   derived from the convention, the complexity, and why there is no space collapse.

2. *Burst balloons.*
   Why "first" fails, why "last" works, the recurrence, the padding, the inclusive `k`, and why you would
   write it memoised.

3. *Design YouTube, and tell me what it costs.*
   The scope, chunked transcoding with the keyframe constraint, adaptive bitrate with the client deciding,
   storage tiered by popularity, and the ranked bill.

---

## Before you move on

- [ ] I can state the interval DP state and its recurrence.
- [ ] I write the three loops with length outermost, every time.
- [ ] I can say why the natural order fails and which direction it errs.
- [ ] I know a small test can pass with the wrong fill order.
- [ ] I can give the matrix chain join cost and derive its indices.
- [ ] I can reconstruct the parenthesisation with a split table.
- [ ] I can say why "burst first" leaves the subproblems entangled.
- [ ] I can say what "burst last" fixes, about which values.
- [ ] I know `k` is a split in one problem and a member in the other.
- [ ] I know the loop bounds differ, and that neither errors.
- [ ] I pad burst balloons, and know what negative indexing would do.
- [ ] I can write the memoised version and say why I prefer it.
- [ ] I know there is no space collapse, and why.
- [ ] I know what limits me first, time or space, with numbers.
- [ ] I know the constraint on `n` signals a cubic solution.
- [ ] I can do stone game and explain the minus sign.
- [ ] I can name three other problems with this shape.
- [ ] I can scope YouTube out loud, in and out.
- [ ] I know why uploads must be resumable here.
- [ ] I can give the transcoding compute rule and the daily total.
- [ ] I can explain chunking and give the wall-time comparison.
- [ ] I know why segments are cut at keyframes.
- [ ] I know why the transcode worker must be idempotent.
- [ ] I can describe the player's adaptive loop.
- [ ] I know why it starts at a low quality, with numbers.
- [ ] I know a segment is a static file and why that matters.
- [ ] I can give the segment-length trade.
- [ ] I can compute storage per year and both tiering costs.
- [ ] I know why we tier by popularity and why the restore path matters.
- [ ] I can give the delivery bill and say what you build instead.
- [ ] I answered all three questions above out loud.
