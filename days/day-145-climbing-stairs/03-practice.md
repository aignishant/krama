---
day: 145
track: practice
title: "Practice — Climbing stairs and the one-dimensional habit"
status: written
---

# Day 145 · Practice

**DSA topic:** Climbing stairs and the one-dimensional habit
**System design topic:** How to run a high-level design interview: the forty-five-minute script

---

## Code these, in this order

One rule for the whole set, and it is the only rule this phase needs: **write two comment lines before any
code.** The first is `# dp[i] = ` finished as a full English sentence. The second is the last-move
enumeration — "to be here, my last move was either ___ or ___". Everything else follows from those two.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Climbing Stairs | LeetCode 70 (Easy) | The habit, on the simplest possible case. |
| 2 | House Robber | LeetCode 198 (Medium) | A genuine choice, and the base case `max(m[0], m[1])`. |
| 3 | Maximum Subarray | LeetCode 53 (Medium) | "Ending exactly at i" — so the answer is `max(dp)`. |
| 4 | Min Cost Climbing Stairs | LeetCode 746 (Easy) | The answer is past the end of the array. |
| 5 | Decode Ways | LeetCode 91 (Medium) | Two moves, five conditions — the conditions are the problem. |
| 6 | Word Break | LeetCode 139 (Medium) | An enumeration of length `n`, and how to bound it. |
| 7 | House Robber II | LeetCode 213 (Medium) | A circle: run the linear version twice and take the max. |

### On every problem, write the two comment lines first

Then check them. For problem 3, your sentence must contain "ending exactly at", or the recurrence will be
wrong in a way that passes small tests. For problem 4, your sentence must make it obvious that the top is one
step past the last index.

### On problem 3, test all-negative input first

Write the test before the solution: `max_subarray([-3, -1, -7])` must return `-1`. Then write the solution.
Initialising the running best to `0` passes every other test and fails this one, and it is the hidden case.

### On problem 5, enumerate the zero cases before coding

Write down what each of these should return, by hand: `"0"`, `"06"`, `"10"`, `"100"`, `"226"`, `"1111"`. Then
write the solution and check all six. **A '0' can only ever be the second digit of a 10 or a 20**, and every
wrong answer to this problem comes from that.

### On problem 6, measure the bound

Solve it with `for j in range(i)` and again with `for j in range(max(0, i - longest_word), i)`. Time both on a
10,000-character string with a dictionary whose longest word is 20. Two numbers, and the ratio should be
around 500.

### Then the operator drill

Take problems 1, 2 and 6 and write down, for each: the state sentence, the last-move enumeration, the
combining operator (`+`, `max`, or `any`), and the initial value of the table. **Notice that the operator and
the initial value always agree** — `+` with 0, `max` with negative infinity or the first element, `any` with
`False`.

### Then the space drill

For each of problems 1 to 5, reduce to `O(1)` and say what window you kept. For problem 3, notice that you
need *two* variables rather than one, and say why.

For problem 6, say why it does not collapse.

---

### The habit drill

1. State the question in one sentence.
2. Apply it to stairs, house robber and maximum subarray, out loud.
3. Say what makes an enumeration "short and backwards-pointing", and why that means one dimension.
4. Say what the enumeration length does to the complexity.

### The state drill

1. Give the state sentence for all seven problems above.
2. For each, say where the answer lives and why.
3. Give the three places an answer can live, and the sentence that tells you which.
4. Give the test for whether a state is complete.
5. Say what the symptom is when a state needs a second dimension.

### The base-case drill

1. Say how to derive the base cases from the recurrence rather than from intuition.
2. Do it for `dp[i] = dp[i-1] + dp[i-2]` and for a three-step version.
3. Give house robber's `dp[1]` and justify it from the state sentence.
4. Say what a wrong base case looks like — the symptom, not the fix.

### The operator drill

1. Name the three combining operators and the problem type each belongs to.
2. Give the matching initial value for each.
3. Give one problem of each type from the list above.

### The costs drill

1. Give the general formula.
2. Give the cost of all seven problems above and say which term differs.
3. Say what bounding word break's enumeration buys, with the arithmetic.
4. Say why the substring construction makes word break worse than it looks, and the fix.

### The break-it drill

Trigger each and record the exact output or error:

1. `return dp[n-1]` when the state means "ending exactly at i".
2. `best_overall = 0` on all-negative input.
3. House robber with `dp[1] = money[1]`.
4. `dp = [0] * n` when the recurrence indexes to `n`.
5. Any of them on an empty or single-element input.
6. Word break with an unbounded `j` range, on a 10,000-character string.
7. A one-dimensional table on a problem whose answer also depends on a remaining budget.

---

### The script drill

1. Name the six phases with their minute allocations.
2. Say the goal of each in one sentence.
3. Say what fraction of the time is setup and what fraction is being marked.
4. Say what you do at minute 25 if the deep dive has not started.

### The requirements drill

1. Give the four or five questions you would ask on any prompt.
2. Say why the exclusions matter as much as the inclusions.
3. Say what makes a question worth asking, and what makes one a waste.
4. State the scope back for "design Twitter", including what is out.

### The estimation drill

1. Give the four-step chain.
2. Memorise and recite: seconds in a day, 1M/day per second, 1B/day per second, peak multiplier.
3. Do the full Twitter estimate out loud, ending with the decision sentence.
4. Do the full Instagram estimate, ending with why the CDN is a cost decision.
5. Give per-machine capacity for a web server, Redis, Postgres, Kafka and WebSockets.
6. Give bytes per record for a post, a user row, a photo, a video minute, a log line, a metric point.

### The design drill

1. Say what phase 4 should feel like, and why.
2. Say what "trace one write and one read" catches.
3. Give the four things a deep dive must cover.
4. Say which of the four is most often missing.
5. Give the four wrap-up sentences.

### The failure-modes drill

1. Name the four ways candidates lose this round.
2. For each, say what it looks like on the timeline.
3. Say which one is the most common and what the fix is.
4. Say what narrating the clock signals to an interviewer.

### The hard-moments drill

1. Give the three responses to an interruption.
2. Give the phrasing for reorienting after being pulled deep early.
3. Give the phrasing for not knowing something.
4. Give the phrasing for disagreeing.
5. Say what to do with five minutes left and an unfinished deep dive.

### The failure drill

For each, say what happens and what you would do:

1. The interviewer says "skip requirements, just design it."
2. The interviewer says "you're spending too long on estimation."
3. You are at minute 40 and have not started the deep dive.
4. You realise at minute 30 that you misunderstood the requirement.
5. You are asked something you genuinely do not know.
6. The interviewer disagrees with a choice you made.
7. The prompt is a system you have never heard of.

Two of the seven are recoverable in under a minute. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *How many ways to climb `n` stairs taking one or two steps?*
   The last-move question producing the recurrence, the state sentence, base cases derived from the
   recurrence, where the answer lives, the cost, and the space collapse.

2. *What does `dp[i]` represent?*
   The full sentence, why similar-looking states differ, the completeness test, and the symptom that means you
   need a second dimension.

3. *Design Twitter. You have forty-five minutes. Begin.*
   The opening ninety seconds only: the framing sentence, four questions, the scope stated back with
   exclusions, and the move into sizing with a reason.

---

## Before you move on

- [ ] I write the state sentence and the last-move enumeration before any code.
- [ ] I can apply the last-move question to three different problems out loud.
- [ ] I derive base cases from the recurrence, not from the pattern.
- [ ] I know the three places an answer can live and how to tell which.
- [ ] I know "ending exactly at i" means `max(dp)`.
- [ ] I know the three combining operators and their matching initial values.
- [ ] I test all-negative input on maximum-subarray-shaped problems.
- [ ] I can enumerate the five zero cases in decode ways.
- [ ] I know how to bound word break's enumeration and what it buys.
- [ ] I know why word break does not collapse to `O(1)` space.
- [ ] I know the symptom that means the state needs a second dimension.
- [ ] I can name the six phases with their minutes.
- [ ] I can give the four or five requirements questions.
- [ ] I state exclusions explicitly.
- [ ] I can do the four-step estimation chain from memory.
- [ ] I end phase 2 with a decision sentence, not just numbers.
- [ ] I know phase 4 should be boring, and why.
- [ ] I trace one write and one read out loud.
- [ ] I offer a choice at the start of the deep dive.
- [ ] I cover mechanism, numbers, failure mode and the rejected alternative.
- [ ] I can give the four wrap-up sentences.
- [ ] I can name the four ways to lose the round.
- [ ] I narrate the clock at least once.
- [ ] I know the three responses to an interruption.
- [ ] I know the phrasing for not knowing something.
- [ ] I know what to do with five minutes left mid-deep-dive.
- [ ] I have the universal opening sentence ready.
- [ ] I answered all three questions above out loud.
