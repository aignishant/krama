---
day: 97
track: practice
title: "Practice — Recursion and backtracking revision and mock round"
status: written
---

# Day 097 · Practice

**DSA topic:** Recursion and backtracking revision and mock round
**System design topic:** What scale actually means, in numbers

---

## Code these, in this order

This is a mock round, so treat it like one. **Set a timer for twenty-five minutes per problem, talk out
loud the whole time, and do not look at anything.** If you cannot name which of the four templates it is
within thirty seconds, that is the thing to practise, not the code.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Palindrome Partitioning | LeetCode 131 (Medium) | Recognising the `start`-index tree from a string problem, and pruning before descending. |
| 2 | Restore IP Addresses | LeetCode 93 (Medium) | Two prunes, both `break`, and a fixed piece count. |
| 3 | Combination Sum II | LeetCode 40 (Medium) | Both skips with the right keyword each, cold. |
| 4 | Word Search | LeetCode 79 (Medium) | Path versus region, said before any code is written. |

### Before each problem, say the four things

Out loud, timed, before typing:

1. The constraint bound, and what it implies.
2. The output size, and that nothing can beat it.
3. Order matters or not — so which tree.
4. Reuse allowed or not — so `i` or `i + 1`.

If those four take more than forty seconds, do them again on the next problem until they do not.

### On problem 1, add the table afterwards

Solve it with the inline palindrome check, then again with the pre-computed table. Say what factor came
off the per-node cost, and what did not change.

### On problem 2, justify both `break`s

Neither is obvious. For each, say the monotonicity that makes `break` correct rather than `continue`.

### On problem 3, write both skips before the loop body

Write the two guard lines first, with the right keyword each, then fill in the rest. Then swap the
keywords and record both kinds of damage.

### On problem 4, say the word first

Say "path" or "region" out loud before typing. Then write it, and afterwards say what the answer would
have been had you said the other word.

---

### The two-questions drill

1. State both questions from memory.
2. Give the four combinations and the template each one names.
3. For each template, name two problems that use it.
4. Take five problems you have never seen and classify each in under ten seconds.

### The template drill

1. Write all four templates from memory, in under six minutes total.
2. Say what is identical across all four.
3. Say what changes between templates 1 and 2, character by character.
4. Say what template 4 does not need, and why.

### The five-rules drill

1. Name the five rules that survive the phase.
2. For each, give the specific wrong output it prevents.
3. Say which of the five is silent in every case.
4. Say which one removes a question from the interview entirely.

### The duplicate drill

1. Write both duplicate conditions.
2. Say the one English sentence they both mean.
3. Say which tree shape each belongs to, and why the bookkeeping differs.
4. Use the wrong one in each tree and record what you lose.
5. Say what both of them require to have happened first.

### The keyword drill

1. State the rule for `break` versus `continue` in one sentence.
2. Give two examples of each from the phase.
3. Swap them in Combination Sum II and record the output.
4. Swap them in Combination Sum and say what changed — and what did not.

### The complexity drill

Fill this in from memory, then check it:

| problem | answers | time | extra space |
|---|---|---|---|
| subsets | | | |
| permutations | | | |
| combinations C(n,k) | | | |
| combination sum | | | |
| word search | | | |
| N-Queens | | | |

Then say the sentence that is true of the whole right-hand column.

### The bound-reading drill

For each constraint, say which template the problem probably wants:

1. `1 <= n <= 6`
2. `1 <= n <= 20`
3. `1 <= n <= 16` on a string
4. `1 <= target <= 500`, candidates as small as 1
5. `1 <= n <= 10^5`

The last one is the important one. Say what it rules out.

### The break-it drill

Trigger each, record the exact output or error, and say which rule it violates:

1. `result.append(current)` in any template.
2. `used[i] = False` omitted.
3. `i` instead of `i + 1` in Combination Sum II.
4. `i > 0` instead of `i > start`.
5. `continue` instead of `break` on the too-big check — and time it.
6. Combination sum with a target of 5,000 and a candidate of 1.
7. `set(list_of_lists)`.

### The mock drill

Take two problems you have never seen, from the list below, and do them under a timer with no
references. Talk the whole time.

- Generate Parentheses (LeetCode 22)
- Letter Case Permutation (LeetCode 784)
- Combination Sum III (LeetCode 216)
- Beautiful Arrangement (LeetCode 526)
- Additive Number (LeetCode 306)

Afterwards, write down: how long the first minute took, whether you named the template before coding,
and whether you said the output size out loud.

---

### The conversion drill

Compute each in your head, then check:

1. 50 million requests a day, in QPS.
2. 3 billion a day, in QPS.
3. 800 QPS, in requests per day.
4. 5 million DAU × 40 actions, average and peak QPS.
5. 2 KB × 500 million records, in TB.

### The ladder drill

1. Draw the conversion ladder from users to peak QPS from memory.
2. Say what number goes on each arrow, and where you would ask a question instead of assuming.
3. Say which side of the ladder gives you servers and which gives you storage.
4. Say what you must multiply storage by, and why.

### The capacity drill

State from memory:

1. QPS for one application server, doing real work.
2. Simple indexed reads per second for one relational database.
3. Writes per second for the same.
4. Operations per second for one Redis instance.
5. Bandwidth of one machine's network link.

Then size a system at 6,000 peak QPS with a 50:1 read ratio and say how many of each you need.

### The latency drill

1. Write the six latency figures in order.
2. State the memory-to-SSD ratio and the SSD-to-across-the-world ratio.
3. Compute the pure-distance round trip for Mumbai to New York and show the working.
4. Say what that number means for the design, and what it rules out.
5. Say why p99 is quoted rather than the average, using the hundred-requests-per-page argument.

### The photo-app drill

Reproduce the whole worked example for 100 million DAU, out loud, in under three minutes:

1. Feed loads per day, average QPS, peak QPS.
2. Image requests per second at peak, and where they must be served from.
3. Uploads per day and write QPS.
4. The read:write ratio and what it implies.
5. Media storage per day and per year, with replication.
6. Metadata storage per year, and where it goes.
7. Peak outbound bandwidth, and what that number is really telling you.

### The peak-shape drill

For each product, give the peak factor and say whether it is a machine-count problem or an architecture
problem:

1. A global messaging app.
2. An Indian food-delivery app on a Friday evening.
3. Ticket sales for a concert.
4. A university publishing results at 10 a.m.
5. A live cricket match.

### The misleading-estimate drill

For each, say what the naive estimate misses:

1. A celebrity with 50 million followers posts once.
2. A chat app with a million idle users.
3. A system that has run for three years.
4. A cache sized assuming every key is equally likely.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Two problems, no hints, talk as you go.*
   For each: the bound read aloud, the output size stated, the two questions answered so the template is
   named, the pattern with the copy flagged, the prune placed before the descent, and both complexities
   given separately.

2. *This app has ten million users. What is the read QPS?*
   The daily-active assumption named, actions per user reasoned about rather than guessed, the division
   with the rounding admitted, the peak factor with the question about scheduled events, the read:write
   split, and then the comparison against what one machine actually does.

3. *Which of the four templates would you write for a problem you have never seen?*
   The two questions, the four answers, and the sentence about what is identical in all four.

---

## Before you move on

- [ ] I can state the two questions and the four templates they choose between.
- [ ] I can write all four templates from memory in under six minutes.
- [ ] I can name the five rules and the wrong output each one prevents.
- [ ] I can write both duplicate conditions and say the one sentence they share.
- [ ] I can state the `break` versus `continue` rule and give two examples of each.
- [ ] I filled in the complexity table from memory and got the space column right.
- [ ] I can read a constraint bound and name the expected template.
- [ ] I know the only problem in the phase that can overflow the stack, and why.
- [ ] I did two unseen problems under a timer and named the template in the first thirty seconds.
- [ ] I can convert any daily figure to QPS in my head.
- [ ] I can draw the conversion ladder and say what goes on every arrow.
- [ ] I know what one app server, one database and one Redis instance can do.
- [ ] I can give the six latency figures and the two ratios.
- [ ] I can compute the Mumbai–New York round trip and say what it rules out.
- [ ] I can do the photo-app estimate out loud in under three minutes.
- [ ] I can tell a machine-count peak from an architecture peak.
- [ ] I answered all three questions above out loud.
