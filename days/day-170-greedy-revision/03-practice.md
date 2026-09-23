---
day: 170
track: practice
title: "Practice — Greedy revision and the mock round"
status: written
---

# Day 170 · Practice

**DSA topic:** Greedy and intervals revision and mock round
**System design topic:** High-level design revision and full mock

---

## Code these, in this order

One rule for the whole set, and it is the rule of the phase: **before you write a line, say the four questions
out loud.** Can I name the best-looking choice in one sentence? Can I break it in thirty seconds? Can I state
the exchange argument concretely? If not, is it DP? **Solving one of these silently and correctly is worth
less than solving it out loud and getting it wrong.**

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Non-overlapping Intervals | LeetCode 435 (Medium) | The sort key, and "remove fewest" = "keep most". |
| 2 | Minimum Number of Arrows to Burst Balloons | LeetCode 452 (Medium) | The same greedy in disguise — do you see it? |
| 3 | Course Schedule III | LeetCode 630 (Hard) | Greedy with an undo, and why the longest. |
| 4 | Minimum Number of Refueling Stops | LeetCode 871 (Hard) | Regret greedy — deferring the choice to hindsight. |
| 5 | IPO | LeetCode 502 (Hard) | Two heaps, and a greedy that needs both orderings. |
| 6 | Candy | LeetCode 135 (Hard) | Two greedy passes, and why one pass cannot work. |

### On problem 1, use the wrong sort key on purpose

Sort by start instead of end. Run on `[[1,100],[11,22],[1,11],[2,12]]` and record the answer against the
correct one. **Then run it on `[[1,2],[2,3],[3,4]]` and note that it agrees.** Say in one sentence why that
combination is the trap of the whole phase.

### On problem 2, notice it is problem 1

Solve it. **Then say precisely which words in the two problem statements differ**, and why the greedy is
identical. Check the tie-break — do balloons touching at a point count as overlapping? **Say what changes if
you get it backwards.**

### On problem 3, find the counter-example first

Before writing anything, find a three-course input where take-if-it-fits gives the wrong answer. **Write it
down and say what the correct answer is.** Only then write the heap version.

Then flip `>` to `>=` in the overrun check. **Run it on your counter-example and record what happens.**

### On problem 3, sort by duration instead

Keep the heap and change only the sort key. Run on `[[1,5],[2,10],[6,8]]`. **Record both answers**, and say
why sorting by deadline is the one that can be justified.

### On problem 4, change `<=` to `<`

One character in the inner loop. Run on `target 100, start 10, stations [[10,60],[20,30],[30,30],[60,40]]` and
record what it returns. **Say why that particular wrong answer is more dangerous than a crash.**

### On problem 4, prove the two loops are linear

They look nested. **Say why they are not**, in one sentence about the pointer. Then instrument it: count the
total inner-loop iterations for `n = 10,000` and check it is `n`, not `n²`.

### On problem 5, name the two orderings

There is an ordering you sort by and an ordering you pop by, **and they are different fields.** Say which is
which and why one heap cannot do both.

### On problem 6, try one pass

Attempt it with a single left-to-right pass. **Find the input where it fails and say what information the
first pass cannot have.** Then write the two-pass version.

### Then the verification drill

For every problem above, write a brute force and check the greedy on a few hundred small random inputs. **Say
for each one why your brute force is small enough to be an oracle** — give the input size where it stops being
usable.

### Then the mock drill

Set a clock. Fifteen minutes for one unseen greedy problem, talking the whole time. Score yourself on four
things: did you say the decision procedure out loud, did you name and justify the sort key, did you try a
counter-example, did you give the cost unprompted. **Three out of four is a pass.**

---

### The decision-procedure drill

1. Give the four questions in order.
2. Say what each one rules out.
3. Say what you do when question two succeeds.
4. Say why "greedy fails, here is the input" is a correct answer.
5. Give the rule for when greedy survives, in one sentence.

### The exchange-argument drill

1. State it in thirty seconds for activity selection.
2. Say what the swap is, concretely.
3. Say what the middle clause must establish.
4. Say what it means if you cannot fill that clause in.
5. Say how the induction finishes it.

### The sort-key drill

1. Give all six rows of the table from memory.
2. Give the rule underneath all of them.
3. Say which family needs no sort at all, and why.
4. Give the input where by-start and by-end disagree, with both answers.
5. Say why the wrong key is silent.

### The middle-ground drill

1. Name both families and their tell.
2. Give the Course Schedule III argument for undoing the longest.
3. Say what regret greedy defers, and until when.
4. Say why `fuel` doubles as a position.
5. Say when you would still fall back to DP.

### The break-it drill

For each, say what happens and whether anything reports it:

1. Sorting intervals by start instead of end.
2. Sorting courses by duration instead of deadline.
3. `>=` instead of `>` in the overrun check.
4. `<` instead of `<=` in the refuelling loop.
5. Pushing `+duration` instead of `-duration`.
6. No guard on an empty interval list.

---

### The clock drill

1. Give the six blocks with their minute ranges.
2. Say what each block produces.
3. Say what the most common failure is, and what it signals.
4. Say which block candidates skip, and why that is the expensive one.

### The four-questions drill

1. Give all four.
2. Say which is the most decision-relevant, and name four things it decides.
3. Give the three read:write regimes and what each implies.
4. Say why asking what you are *not* building is not laziness.

### The estimation drill

1. Give the four steps of the ladder.
2. Say what you round 86,400 to, and why.
3. Work the photo-sharing example end to end.
4. Give the one sentence that is the actual output.
5. Say what you do when the arithmetic comes out small.

### The numbers drill

1. Give per-second rates for 1M/day and 1B/day.
2. Give one database's write rate and one cache node's read rate.
3. Give memory, SSD and disk access times as a ratio.
4. Give the cross-continent round trip and say what is special about it.

### The mock drill

1. State the exam platform's two systems and why they are separate.
2. Give the naive paper-delivery arithmetic and the pre-positioned version.
3. Give the ratio between them and state the general rule.
4. Compute the autosave write rate and the per-shard rate.
5. Say why the end-of-exam spike is not a spike, with both numbers.
6. Give three things that break, and what you would measure.

### The seniority drill

1. Name the three habits and give an example of each.
2. Say why volunteering a weakness needs the mitigation ready.
3. Say what "interesting, but what about X" means.
4. Say what confident invention costs you.
5. Say when the framework itself is the wrong tool.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *How do you decide whether greedy works?*
   The four questions in order, the exchange argument stated concretely, the two middle-ground families with
   their tell, and the rule for when greedy survives.

2. *Which sort key, and why?*
   The rule underneath the table, all six rows, the family that needs no sort, and the input where by-start
   and by-end disagree.

3. *Design a system you have never seen. Forty-five minutes.*
   The six blocks, the four opening questions, the estimation ladder ending in one sentence, offering two deep
   dives, and volunteering what breaks.

---

## Before you move on

- [ ] I can give the four questions of the decision procedure, in order.
- [ ] I can state the exchange argument concretely in thirty seconds.
- [ ] I know what it means when I cannot fill in the swap clause.
- [ ] I know "greedy fails, here is the input" is a correct answer.
- [ ] I can give the rule for when greedy survives and when it dies.
- [ ] I can recall all six rows of the sort-key table.
- [ ] I can give the rule underneath the table in one sentence.
- [ ] I know reachability needs no sort, and why.
- [ ] I know the input where by-start and by-end disagree, with both answers.
- [ ] I know the wrong sort key is silent and passes tidy examples.
- [ ] I can name both middle-ground families and their tell.
- [ ] I can justify undoing the longest in Course Schedule III.
- [ ] I know what regret greedy defers, and until when.
- [ ] I know `fuel` doubles as a position, and why.
- [ ] I checked every greedy I wrote against a brute force.
- [ ] I know where each brute force stops being usable.
- [ ] I scored myself on the four mock criteria and got three of four.
- [ ] I can give the six blocks of the clock with their minutes.
- [ ] I know the most common failure is drawing boxes in minute two.
- [ ] I can give the four opening questions.
- [ ] I know the read:write ratio decides four things, and can name them.
- [ ] I can give the three read:write regimes and what each implies.
- [ ] I can work the estimation ladder and end with one sentence.
- [ ] I round 86,400 to 100,000 out loud.
- [ ] I know what to say when the arithmetic comes out small.
- [ ] I know the per-second rates, database and cache rates, and access times.
- [ ] I know the cross-continent round trip and why it is unfixable.
- [ ] I can give the pre-position-and-release-a-key rule with its ratio.
- [ ] I can say why the end-of-exam spike is not a spike, with numbers.
- [ ] I can name the three habits that read as senior.
- [ ] I know what "interesting, but what about X" means and what to do.
- [ ] I answered all three questions above out loud.
