---
day: 179
track: practice
title: "Practice — The full mock, coding and design"
status: written
---

# Day 179 · Practice

**DSA topic:** Full mock: two problems, forty-five minutes
**System design topic:** Full mock: one high-level design, one low-level design

---

## Code these, in this order

**Today is not practice. Today is the round.** **Set a clock, start it, and do not stop it for anything.**

**The rules, and breaking any one of them means you practised something else:**

```
   [ ] a visible clock: 20 minutes, then 25 minutes
   [ ] talking out loud from the first second
   [ ] NO running the code. Not once.
   [ ] NO looking anything up
   [ ] NO pausing
   [ ] recorded
   [ ] scored immediately, honestly
```

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Task Scheduler | LeetCode 621 (Medium) | Simulating first, then noticing the structure — and saying the sentence between them. |
| 2 | Count of Smaller Numbers After Self | LeetCode 315 (Hard) | Recognising merge sort doing an unfamiliar job. |

### Then, after the round, and only then

**Score both problems on the rubric before you look at any solution.**

```
   PROBLEM SOLVING  0-4      CODING       0-4
   COMMUNICATION    0-4      TESTING      0-4

   16 per problem, 32 total.

   26+   ready. Book the interview.
   20-25 mediums are fine; the hard one needs more rooms.
   14-19 the knowledge is there and the performance is not.
         Four more mocks before anything else.
   <14   go back to the phase that fell over, clock off.
```

### Then diagnose, which is the actual exercise

**Decide which of these four it was. They have different fixes and only one of them is "solve more problems".**

```
   RECOGNITION    the shape did not arrive in two minutes
                  -> day 177's index, not more problems
   ARTICULATION   knew it, could not narrate while writing
                  -> more recorded mocks. Repetition only.
   IMPLEMENTATION had the approach, the code came out wrong
                  -> the seven templates from memory
   COMPOSURE      froze, rushed, or did not start problem 2
                  -> more rooms
```

### On problem 1, write both versions

Write the counting formula, then the heap simulation. **Check them against each other on the examples,
including `n = 0` and a single task.** Say out loud why `most − 1` and not `most`.

### On problem 2, break it on purpose

Change `<=` to `<` in the merge comparison. **Run it on `[-1, -1]` and record both answers.** Say why one
character changed the meaning, and why only duplicates expose it.

### Then do a second mock, tomorrow, with two fresh problems

**One medium, one hard, both unseen.** **Score it.** **The gap between the two scores is the only measurement
in this lesson that matters.**

### Then run the design loop

**Two forty-five minute rounds, back to back, with sixty seconds between them.**

**Round 1, high level: design a video streaming service.** Six beats, on the clock.

**Round 2, low level: design an expense-sharing app.** Six different beats, and **have somebody ask you an
extension question at minute thirty** — percentage splits, multiple payers, or multiple currencies.

### On the reset, do all four steps

Stand up. **One sentence about round one.** **One thing to change.** **And say out loud which round you are
about to be in.** **Notice how strong the urge is to skip the fourth one.**

### Then the wrong-framework drill

Have somebody give you a design question without telling you which kind it is. **Say, in the first minute,
which round you think it is and why.** Then check.

### Then the estimation drill

From memory: 100 million viewers, five videos a day, ten minutes each, two megabits a second. **Get to
petabytes a day and dollars a day of direct egress.** Then say what that single number decides.

### Then the extension drill

Take your expense-sharing class model. **Add percentage splits.** Count how many existing files you had to
edit. **Zero is the target.** Then add multiple payers and count again.

### Then the rounding drill

Split ten rupees three ways with two-decimal precision. **Record what the shares sum to.** Say where the
missing paisa goes and who decides. Then say why the amount is a `Decimal` and not a float.

---

### The rules drill

1. Give all seven mock rules.
2. Say which one people break most, and why breaking it wastes the mock.
3. Say what to say instead of looking something up.
4. Say why the mock is recorded.

### The clock drill

1. Give the minute-by-minute shape of a twenty-minute problem.
2. Say what fraction of it is coding.
3. Give the three clock decisions and the sentence for each.
4. Say what to do at minute nineteen, unfinished.

### The reset drill

1. Give all four steps.
2. Say which one people skip and why it matters most.
3. Say what carrying the first problem in produces.
4. Give the potter's sentence.

### The rubric drill

1. Name the four axes and what a 4 looks like on each.
2. Give the four score bands and the action for each.
3. Say why scoring yourself kindly is worthless.

### The diagnosis drill

1. Name the four failure modes.
2. Give the fix for each.
3. Say which one "solve fifty more problems" actually helps.

### The problem-one drill

1. State the formula and justify every term.
2. Say why `most − 1` and not `most`, with the input that proves it.
3. Say what the `max()` is for, with an example.
4. Give both costs, formula and simulation.

### The problem-two drill

1. Say what the brute force repeats.
2. State the counting rule during the merge, in one sentence.
3. Say why positions must travel with values.
4. Say what `<=` versus `<` changes, and which input exposes it.
5. Give the cost and the space.

### The two-rounds drill

1. Give both sets of six beats.
2. Say what each round's output is.
3. Say what each round's classic failure looks like.
4. Say which beat is the whole low-level round, and why.

### The streaming drill

1. Compute delivered petabytes a day, and the direct egress cost.
2. Say what that number decides, in one sentence.
3. Say why uploads use a pre-signed URL.
4. Give the chunked transcoding argument and its three costs.
5. Name the metric you would alert on, and why there is no alternative.

### The expense drill

1. Give the entities and what each one knows.
2. Say why balances are derived rather than stored.
3. Give the invariant and say where it is enforced.
4. Give the strategy interface and say what adding a variant costs.
5. Say how you justify the pattern without over-engineering.
6. Give the rounding rule and the type of money.

### The break-it drill

For each, say what happens and how it is scored:

1. Running the code during a mock.
2. Looking up the heap API mid-problem.
3. Going straight into problem two without standing up.
4. Silence for the last four minutes of an unfinished problem.
5. Optimising before anything works.
6. `most * (cooldown + 1) + ties` on a single task.
7. `<` instead of `<=` in the merge, on `[-1, -1]`.
8. Doing capacity estimation for a low-level design question.
9. A switch statement over split types, when a fourth type arrives.
10. Storing balances instead of deriving them, when an old expense is edited.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *One medium, one hard. The clock is running.*
   The shape of each problem — restate, clarify, example, brute force with cost, better idea with cost, hand
   back, code, trace, complexity — plus the two clock rules and the reset.

2. *How do you get better at this, specifically?*
   The four failure modes, the different fix for each, the score bands, and why the default response only
   helps with one of the four.

3. *Two design rounds, back to back. Begin.*
   Both sets of six beats, why the orders differ, the number that decides the streaming architecture, the
   extension question as the whole low-level round, and the four-step reset.

---

## Before you move on

- [ ] I ran a real mock: clock visible, out loud, no running the code.
- [ ] I recorded it and listened back.
- [ ] I scored it on the rubric, honestly, before looking at any solution.
- [ ] I diagnosed which of the four failure modes it was.
- [ ] I know the different fix for each of the four.
- [ ] I know the minute-by-minute shape of a twenty-minute problem.
- [ ] I know coding is less than half of it.
- [ ] I can give the three clock decisions and their sentences.
- [ ] I describe the missing piece rather than going silent.
- [ ] I stood up between problems and named the change.
- [ ] I can state the Task Scheduler formula and justify every term.
- [ ] I know why `most − 1`, and the input that proves it.
- [ ] I can state the merge-sort counting rule in one sentence.
- [ ] I know what `<=` versus `<` changes, and which input exposes it.
- [ ] I can give both sets of six design beats.
- [ ] I know which beat is the whole low-level round.
- [ ] I say out loud which kind of design round I am in.
- [ ] I can compute 75 petabytes a day and say what it decides.
- [ ] I know why uploads use a pre-signed URL.
- [ ] I can argue for chunked transcoding and name its three costs.
- [ ] I know which metric fails silently in that pipeline.
- [ ] I can give the expense-app entities and the invariant.
- [ ] I know why balances are derived, not stored.
- [ ] I can add a split type without editing anything.
- [ ] I can justify the strategy pattern from a signal, not by habit.
- [ ] I know where the missing paisa goes, and why money is a `Decimal`.
- [ ] I close every design with failure, monitoring and one honest weakness.
- [ ] I answered all three questions above out loud.
