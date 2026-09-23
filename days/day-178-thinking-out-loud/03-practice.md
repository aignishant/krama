---
day: 178
track: practice
title: "Practice — Thinking out loud, and the design framework"
status: written
---

# Day 178 · Practice

**DSA topic:** How to think out loud in a coding round
**System design topic:** The system design interview framework, memorised

---

## Code these, in this order

**Today the code is not the exercise. The talking is.** For every problem below, **record yourself** — a phone
is fine — **and solve it out loud from the first second to the last.** Then listen back. **That is the drill,
and it is uncomfortable, and it is the single most effective hour in this whole course.**

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Longest Consecutive Sequence | LeetCode 128 (Medium) | The full arc: brute force, its cost, the one-line fix, and why it is linear. |
| 2 | Product of Array Except Self | LeetCode 238 (Medium) | Clarifying the constraint — no division, O(1) extra — before writing. |
| 3 | Merge Intervals | LeetCode 56 (Medium) | Stating the sort key and its reason before touching the loop. |
| 4 | Word Break | LeetCode 139 (Medium) | Naming the state out loud before writing the DP. |

### The rule for all four

**Say every one of these, in this order, before you write a line:**

```
   1. restate the problem in your own words
   2. the four questions: how big, weird inputs, what to
      return when there is no answer, may I modify the input
   3. work the given example by hand, aloud
   4. the brute force AND its cost
   5. the better idea AND its cost
   6. "shall I write that?"
```

**Then code, narrating decisions.** **Then test by saying values.** **Then state the complexity unprompted.**

### Then listen back, with this checklist

```
   [ ] Did I restate before doing anything?
   [ ] Did I ask all four questions?
   [ ] Did I work an example by hand?
   [ ] Did I say a brute force before the clever answer?
   [ ] Did I state a cost before writing?
   [ ] Was there any silence longer than 30 seconds?
   [ ] Was I narrating DECISIONS or keystrokes?
   [ ] Did I test by saying actual values?
   [ ] Did I state the complexity without being asked?
   [ ] Did I say "this is easy" or "it should work"?

   Score the first four problems, then do four more and
   score again. The gap between the two scores is the
   only measure that matters here.
```

### On problem 1, count the steps

Instrument both versions and **record the inner-step counts for a single run of 10, 100, 1,000 and 5,000
consecutive numbers.** Then say the ratio out loud, and say why the guarded version is genuinely linear despite
the nested loop.

### On problem 2, let the constraint choose

The problem forbids division and asks for O(1) extra space. **Say what each of those rules out, before you
think about the answer.** Then say what is left.

### On problem 4, say the state first

Do not write anything until you can say, in one sentence: *"`ok[i]` means the first `i` characters can be
broken into dictionary words."* **If the sentence does not come, the loop will be wrong in a way that is very
hard to find.**

### Then the silence drill

Solve any problem with a timer visible. **Every time you go quiet, note the timestamp.** Add up the silent
seconds. **Anything over thirty seconds in one stretch is a gap the interviewer would have felt.**

### Then the stuck drill

Pick a problem genuinely above your level. **When you get stuck, say the three-part sentence out loud** — what
I know, what is blocking me, what I am about to try. **Record it.** Then listen back and ask whether somebody
listening could have helped you from that sentence alone.

### Then the hint drill

Have somebody give you a hint mid-problem, or read one from a solution. **Practise repeating it back in your
own words before acting on it.** Notice the urge to say "yes, but I was going to..." and do not.

### Then the framework drill

Take any well-known product and run the six beats out loud with a clock. **Five, five, five, five, ten,
fifteen.** Stop at each boundary whether or not you are finished. **Getting to the deep dive with fifteen
minutes left is the whole exercise.**

### Then the estimation drill

From memory: **100 million daily active users, twenty reads and 0.2 writes each per day.** Get to reads per
second, writes per second, the ratio, storage per day and per year, and bandwidth. **Then say what the ratio
implies.** Do it in under three minutes.

### Then the numbers drill

Recite from memory: memory read, SSD read, same-zone network, cross-region network. One machine's requests per
second, one Postgres instance's writes per second, one Redis instance's operations per second. **Then use them
to answer "do I need to shard?" for 700 writes a second.**

### Then the weakness drill

Take a design you have already produced. **Name its single weakest point and the failure that would have no
obvious symptom.** Then say the metric you would alert on.

---

### The script drill

1. Give the seven things you say before writing a line.
2. Say why the brute force goes first even when you know the answer.
3. Give the sentence that hands control back to the interviewer.
4. Say what "shall I write that?" buys you.

### The questions drill

1. Give the four questions that apply to every problem.
2. For each, say what the answer would change.
3. Give two problem-specific questions for a string problem and two for a graph problem.
4. Say what "n is up to a hundred thousand" has just told you.

### The narration drill

1. Give three examples of narrating a decision.
2. Give one example of narrating a keystroke, and say why it is worse than silence.
3. Give the sentence to use when you need ten quiet seconds.
4. Say the silence limit.

### The stuck drill

1. Give the three moves.
2. Give the three-part sentence, in order.
3. Say why that sentence is the most valuable thing to say when stuck.
4. Say how to take a hint, and the two words never to say.

### The testing drill

1. Say what a test is, and what it is not.
2. Give the five inputs you always check.
3. Say which one finds your own bugs most often, and why.
4. Say what finding your own bug does to the score.

### The grading drill

1. Name the four axes.
2. Say which two you control completely.
3. Explain why "almost finished, communicated well" can beat "finished, silent".
4. Say what to do at minute 25 with nothing working.

### The six-beats drill

1. Name all six, in order, with their minutes.
2. For each, say what it hands to the next one.
3. Give the opening sentence that announces the plan.
4. Say why beats one to five are deliberately shallow.
5. Name the two classic failures and say what the framework prevents.

### The requirements drill

1. Give both halves and say which candidates forget.
2. Say why naming exclusions matters.
3. List the six non-functional questions.
4. Say which one shapes the architecture most, and why.

### The estimation drill

1. Give the seven steps, in order.
2. Do the worked example from 100M DAU to reads and writes per second.
3. Give the ratio and the three decisions it makes.
4. Compute photo storage per day and per year.
5. Compute the feed table's size, and say what caps it.
6. Give the bandwidth, and say what that argues for.

### The numbers drill

1. Give the four latency figures.
2. Give the four throughput figures.
3. Give the four size figures.
4. Use two of them to make a sharding decision in one sentence.

### The closing drill

1. Name the six items on the closing checklist.
2. Say why naming your own design's weakness is worth the most.
3. Give an example of a failure with no natural symptom, and the metric for it.

### The break-it drill

For each, say what happens and how it is scored:

1. Writing code in minute one.
2. Two minutes of silence in the middle of a round.
3. Narrating keystrokes.
4. "No, because..." after a hint.
5. "This is easy."
6. "I think that's right" instead of a trace.
7. Asking no clarifying questions.
8. Reciting a memorised solution without justifying it.
9. Forty minutes of boxes with no numbers.
10. Thirty minutes on the cache before agreeing the requirements.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Talk me through your approach before you write any code.*
   Restate, the four questions, an example by hand, the brute force with its cost, the better idea with its
   cost, and hand back control.

2. *You've been quiet. What are you thinking?*
   The three-part sentence: what I know, what is blocking me, what I am about to try — said so precisely that
   somebody could hand you exactly the right hint.

3. *Design something. Show me your process, not just your answer.*
   The six beats with their minutes, why the order is fixed, an estimation with "so…" after every number, the
   deep dive offered as a choice, and the closing checklist including one honest weakness.

---

## Before you move on

- [ ] I have recorded myself solving a problem out loud and listened back.
- [ ] I restate the problem before doing anything else.
- [ ] I ask all four questions every time, even when I can guess.
- [ ] I know what "n up to 100,000" has already told me.
- [ ] I work a small example by hand, aloud, before proposing anything.
- [ ] I say the brute force and its cost before the clever answer.
- [ ] I state a cost before writing, not after being asked.
- [ ] I hand control back with "shall I write that?"
- [ ] I narrate decisions, never keystrokes.
- [ ] I never go silent for more than thirty seconds.
- [ ] I can give the three moves for being stuck.
- [ ] I can say what I know, what is blocking, and what I will try.
- [ ] I repeat hints back in my own words and never say "no, because".
- [ ] I test by saying values, not by asserting.
- [ ] I test the thing I was unsure about while writing.
- [ ] I know finding my own bug is a positive.
- [ ] I know the four grading axes and which two I fully control.
- [ ] I know what to say at minute 25 with nothing working.
- [ ] I can name the six design beats with their minutes.
- [ ] I can say what each beat hands to the next.
- [ ] I announce the plan in the first fifteen seconds.
- [ ] I give both halves of requirements and name the exclusions.
- [ ] I push on the consistency question.
- [ ] I can go from 100M DAU to reads, writes, storage and bandwidth in three minutes.
- [ ] I follow every number with "so…".
- [ ] I know the latency, throughput and size reference numbers.
- [ ] I can make a sharding decision from two of them in one sentence.
- [ ] I design the data model from access patterns.
- [ ] I walk the read path and the write path out loud.
- [ ] I offer the deep dive as a choice.
- [ ] I close with monitoring, SLO, security, cost, failure and one honest weakness.
- [ ] I answered all three questions above out loud.
