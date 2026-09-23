---
day: 162
track: practice
title: "Practice — Recognising dynamic programming"
status: written
---

# Day 162 · Practice

**DSA topic:** Recognising dynamic programming
**System design topic:** Design Google Maps

---

## Code these, in this order

Today the rule is different from every other day: **do not solve these first. Diagnose all six, out loud,
before writing a line of code.** Signals, test, shape, state as a sentence, state count. Ninety seconds each.
Write down your six diagnoses, and only then start coding.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Jump Game II | LeetCode 45 (Medium) | Looks like DP, and greedy is better. |
| 2 | Decode Ways | LeetCode 91 (Medium) | One dimension, and a validity condition. |
| 3 | Longest Increasing Subsequence | LeetCode 300 (Medium) | The incomplete state, caught before coding. |
| 4 | Word Break | LeetCode 139 (Medium) | Position plus a dictionary — which dimension is real? |
| 5 | Combination Sum | LeetCode 39 (Medium) | "List all" — backtracking, not DP. |
| 6 | Super Egg Drop | LeetCode 887 (Hard) | Two dimensions, and a constraint that rules out the obvious one. |

### On all six, write the diagnosis first

For each, write down five things before coding: **which signals fired, whether overlap exists, which shape,
the state as a full sentence, and the state count.** Then code it. **Then compare your diagnosis with what you
actually needed.**

**Count how many you got right first time.** That number is the thing this lesson is trying to improve.

### On problem 1, try to break greedy and fail

Spend a real thirty seconds looking for a counter-example to "jump to whichever reachable position takes you
furthest". Record what you tried. **Then look up why it works**, and say in one sentence what property makes
the greedy choice safe.

### On problem 3, catch the incomplete state before coding

Write "dp[i] is the longest increasing subsequence in the first i elements" and then try to write the
recurrence. **Record the exact sentence you cannot finish.** Then redefine and note that the state count did
not change.

### On problem 4, question the second dimension

Your first instinct may be `dp[i][word]`. Write the state count for that against `dp[i]`. **Say what the
dictionary actually is in the recurrence** — a dimension, or just the set of choices?

### On problem 5, notice it is not DP at all

Compute the number of results for a realistic input. **Say why no table helps**, and what changes if the
question becomes "how many combinations" instead.

### On problem 6, let the constraint choose

Read the constraints before the statement. `k ≤ 100`, `n ≤ 10,000`. Compute the size of `dp[eggs][floors]` and
the work per state for the obvious recurrence. **Say whether it fits**, then find the reformulation that does.

### Then the counter-example drill

For each of these, spend thirty seconds trying to break greedy, and record what you find:

1. Coin change with `[1, 2, 5]`.
2. Coin change with `[1, 5, 7]`.
3. Interval scheduling by earliest end time.
4. Fractional knapsack by value per kilo.
5. 0/1 knapsack by value per kilo.
6. House robber, taking the largest value first.

**Three break and three do not.** Say which, and for the three that hold, say what the argument would be.

### Then the audit drill

For eight problems you have solved this month, write the state count and the work per state, and compare
against ten million. **Find the two that are closest to the line** and say what constraint makes them fit.

---

### The signals drill

1. Name all four signals.
2. Give the words that indicate signal one, and the counter-words.
3. Say what signal two rules out.
4. Give the constraint table from memory.
5. Say why every row of it lands near the same number.

### The test drill

1. State both halves of the test.
2. Say which half separates DP from divide and conquer.
3. Give the practical way to check overlap.
4. Say what a broken substructure actually means, and what the fix is.
5. Give the two call-count figures that make it concrete.

### The shape drill

Give the state for each, from memory:

1. Position with a bounded lookback.
2. Position plus a resource.
3. Position plus a mode.
4. Two independent sequences.
5. A grid.
6. A range and how it splits.
7. A subtree.
8. A set, `n ≤ 20`.

Then say the one question that produces all eight.

### The not-DP drill

1. Give four cases where it is not DP.
2. For each, say what it is instead.
3. Say how you test for each.
4. Give the constraint-based fifth case.

### The order drill

1. Give the six steps in order.
2. Say how long the first three take and what they prevent.
3. Say why you write it memoised first.
4. Say what you would do only if asked.

### The break-it drill

For each, say what goes wrong and whether anything reports it:

1. DP where greedy is provably safe.
2. DP where a closed form exists.
3. Not checking the state count.
4. An incomplete state.
5. "Count" solved as "list".
6. Memoising divide and conquer.
7. A two-dimensional table when `n = 10⁵`.

---

### The scoping drill

1. Give your in and out lists.
2. Say why search in particular is out.
3. Say which of the three sub-systems you would go deep on.

### The Dijkstra drill

1. Give the graph size and say what that means for the data.
2. Say what Dijkstra explores and why.
3. Give the node count and the time for a 600 km route.
4. Compute the machine count at peak.
5. Give what bidirectional and A\* each buy, and why neither is enough.
6. Say how the question changes as a result.

### The hierarchy drill

1. State the observation about road networks.
2. Describe contraction in two sentences.
3. Say what the shortcut condition is and what it prevents.
4. Describe the query and its one crucial restriction.
5. Give the node count and the query time.
6. Give the preprocessing cost and what it replaces.

### The traffic drill

1. Say exactly why preprocessing and traffic conflict.
2. Give the two-phase split and what changes in each.
3. Say why that split works, in one sentence about what traffic changes.
4. Describe the live overlay and why it is affordable.
5. Say what happens with stale readings.
6. Say what hysteresis is for.

### The telemetry drill

1. Compute the reports per second and per day.
2. Say what map matching is and why it is hard.
3. Say why median and not mean.
4. Give both jobs the contributor threshold does.
5. Compute the size of the live speed state.
6. Say which data in this system is the most sensitive.

### The ETA drill

1. Say why adding current speeds is wrong.
2. Give the line that fixes it.
3. Say what output you would return, and why.

### The tiles drill

1. Give the tile count per zoom level.
2. Compute it at z=12 and z=20.
3. Give the pre-render strategy and why it works.
4. Give the raster-versus-vector comparison, both factors.
5. Say what fraction of the bill tiles are.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *How would you approach this problem?*
   The four signals, the two-part test, the shape decision tree, the state as a sentence, and the state count
   — in ninety seconds, for a problem you have not seen.

2. *Is it dynamic programming or greedy?*
   The counter-example test with a real example, what you say when you find one and what you say when you do
   not, and the three other cases where it is not DP.

3. *Design Google Maps.*
   Why Dijkstra is off by four orders of magnitude, contraction hierarchies and the upward-only query, the
   two-phase split for traffic, and where the traffic data comes from.

---

## Before you move on

- [ ] I can name all four signals from memory.
- [ ] I read the constraints before the problem statement.
- [ ] I know the constraint table and why every row lands near 10⁷.
- [ ] I can state both halves of the test.
- [ ] I know overlap is what separates DP from divide and conquer.
- [ ] I can check overlap by sketching two levels.
- [ ] I know a broken substructure means an incomplete state.
- [ ] I can give all eight shapes and the question that produces them.
- [ ] I state the state as a full sentence before coding.
- [ ] I run the completeness check.
- [ ] I count states × work against ten million.
- [ ] I write it memoised first, and know why.
- [ ] I can name four cases where it is not DP.
- [ ] I spend thirty seconds trying to break greedy.
- [ ] I know what to say when I find a counter-example and when I do not.
- [ ] I check for a closed form on counting problems.
- [ ] I know "list all" is backtracking and "how many" is DP.
- [ ] I diagnosed all six practice problems before coding.
- [ ] I can say why Dijkstra fails, with the node count and the machine count.
- [ ] I know what bidirectional and A\* each buy.
- [ ] I can describe contraction hierarchies and the shortcut condition.
- [ ] I know the query only moves upwards, and what that buys.
- [ ] I can give the preprocessing cost and what it replaces.
- [ ] I know exactly why traffic conflicts with preprocessing.
- [ ] I can give the two-phase split and why it works.
- [ ] I know where the traffic data comes from and its volume.
- [ ] I know what map matching is and why it is hard.
- [ ] I know why the contributor threshold is also the privacy guarantee.
- [ ] I know why an ETA advances the clock as it walks the route.
- [ ] I know routing is about 2% of the bill.
- [ ] I answered all three questions above out loud.
