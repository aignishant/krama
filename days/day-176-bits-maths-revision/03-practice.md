---
day: 176
track: practice
title: "Practice — Bits and maths mock, and cost"
status: written
---

# Day 176 · Practice

**DSA topic:** Bits and maths revision and mock round
**System design topic:** Cost: the constraint nobody mentions

---

## Code these, in this order

**This is a mock round, so the rule is different today.** Set a clock. **Twenty minutes for a medium, thirty
for a hard.** Talk out loud the whole time, even alone, even feeling foolish. **And before you write a single
line, say the recognition sentence** — the one that names which of the twelve tools this is. **If you cannot
say it, do not start typing; go back and read the constraints again.**

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Bitwise AND of Numbers Range | LeetCode 201 (Medium) | That a range of numbers shares a binary prefix. |
| 2 | Single Number II | LeetCode 137 (Medium) | Noticing that pairing fails, and counting modulo three. |
| 3 | Closest Prime Numbers in Range | LeetCode 2523 (Medium) | Per group, not per number — plus one fact about prime gaps. |
| 4 | Count Ways to Make Array With Product | LeetCode 1735 (Hard) | The capstone: sieve, factorise, stars and bars, modular inverse. |

### The rules for the round

**Read the constraints first, out loud, before the problem statement.** Say what they forbid.

**Then say the recognition sentence.** One sentence, naming the structure. *"ANDing a range keeps only the
common prefix."* *"A product is decided independently per prime, so I multiply the counts."*

**Then state the plan and the cost, before writing.** Time and space.

**Then write it.** No running it until you have read it back once yourself.

**Then test four inputs: zero, one, two, and something negative or degenerate.**

### Score yourself honestly

```
   For each problem, tick what actually happened:

   [ ] I read the constraints before the problem
   [ ] I said the recognition sentence before writing
   [ ] The sentence was right
   [ ] I stated the cost before writing
   [ ] The first version was correct
   [ ] I found my own bug, before running it
   [ ] I tested 0, 1, 2 and a degenerate case

   4 problems x 7 = 28 ticks.

   22+   you are ready for this phase in an interview.
   15-21 the tools are there and the recognition is not.
         Re-read the trigger table until the middle column
         arrives before you finish the left one.
   <15   go back and re-solve days 171-175's problems
         with the clock off. Speed is not the issue yet.
```

### On problem 1, notice what the constraints forbid

`right` can be 2,147,483,647. **Say out loud, before anything else, what that rules out.** Then say what is
left: the answer can only depend on the two endpoints.

### On problem 1 again, check the boundary

Run it on `left == right`. **Then change `while right > left` to `while right >= left` and record what
happens** for every input.

### On problem 2, write the slow one on purpose

Write the column-counting version even though the state machine exists. **Then write the state machine and
time both on a list of thirty thousand.** Record the ratio. **Then say which one you would write in an
interview and why the answer is not the fast one.**

### On problem 3, find the early exit yourself

Solve it without the early exit first. **Count how many primes the scan examines on `[1, 1000000]`.** Then work
out for yourself why a gap of two cannot be beaten, add the exit, and count again. Record both numbers.

### On problem 4, say the sentence before anything

Do not write code until you can say, in one breath, **why the primes are independent and what stars and bars is
doing.** Then check `n = 2, k = 6` by hand — there should be four arrays — before you trust anything.

### Then the trigger-table drill

Cover the middle column. **Read each trigger and name the tool and the justifying sentence.** Do it until
nothing takes more than three seconds.

### Then the silent-failure drill

Write out all five failures that produce a wrong number with no error. **For each, give the input that exposes
it and the one-line fix.**

### Then the bill drill

Price the system in the lesson from memory: **compute, egress, cross-zone, observability, database.** Get to a
total. Then give the cost per daily active user and per thousand requests.

### Then the surprise drill

Compute what it costs to store 30 TB for a month, and what it costs to send it out once. **Say the ratio.**
Then compute the cross-zone bill from eight internal calls at twenty kilobytes, and say why it is invisible.

### Then the cut-it-in-half drill

Give the optimisation list in order. **For each step, say roughly what it saves and what it costs you.** Then
say which step most teams start at, and why that is the wrong end.

---

### The recognition drill

1. Give five triggers and the tool each one names.
2. Give the four questions of the thirty-second procedure, in order.
3. Say which question is highest value and why.
4. Name the three tools that are secretly one idea, and give the idea.

### The bits drill

1. Give both core moves and what each one is for.
2. Give the power-of-two test with its guard.
3. Give the subset enumeration and the value of `n` at which it stops.
4. Give the submask loop and its cost against the naive one.

### The XOR drill

1. Give the three facts.
2. One loner, two loners, three copies: the method for each.
3. Say what a set bit in `a ^ b` means.
4. Give the range-XOR period and the four cases.

### The number-theory drill

1. Say why testing to the square root is enough.
2. Give the sieve, including where it starts and where it stops.
3. Give Euclid and the one-sentence reason.
4. Give fast power and its step count for `10^9`.
5. Give Fermat's inverse and both preconditions.

### The counting drill

1. Give the two questions and the four formulas.
2. Say why you never compute a factorial.
3. Give the multiplicative form and its order of operations.
4. Give the three-lookup modular form and the walk-down trick.
5. Give stars and bars, and one problem it solves in disguise.

### The line-items drill

1. Name the four line items that dominate a bill.
2. Name the fifth that is not on the bill.
3. Say which is usually the largest at scale, and why that surprises people.
4. Say what fraction compute typically is.

### The transfer drill

1. Give the four transfer prices.
2. Compare the cost of storing 30 TB with sending it out once.
3. Compute the cross-zone bill from stated internal traffic.
4. Give the fix, and say why collapsing to one zone is the wrong fix.

### The purchasing drill

1. Give the four ways to buy compute and the discount for each.
2. Say what you commit to and what you never commit to.
3. Say what spot is right for and wrong for, with examples.
4. Say where serverless wins and where it loses.

### The optimisation drill

1. Give the seven steps in order.
2. Say which two are free.
3. Compute the saving from switching non-production off outside working hours.
4. Say which step teams start at, and why that is wrong.
5. Say when cost optimisation is itself a bad investment.

### The visibility drill

1. Say what tagging buys and how it is enforced.
2. Say what the "untagged" row usually contains.
3. Give the difference between showback and chargeback.
4. Say why a cost bug runs for a month, and the alert that catches it in a day.
5. Say where the cheapest place to see a price is.

### The break-it drill

For each, say what happens and whether anything reports it:

1. `while right >= left` in the range-AND loop.
2. Plain XOR on a list where values appear three times.
3. Breaking on the first prime pair found rather than the closest.
4. Factorial tables sized to `n` rather than `e + n − 1`.
5. A log level left at DEBUG in production for a month.
6. A three-year commitment on a six-month-old product.
7. A database primary running on spot capacity.
8. Millions of tiny objects moved into deep archive.
9. An untagged resource created by a test that never cleaned up.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Two problems, no hints, talk as you go.*
   Read the constraints, say what they forbid, say the recognition sentence, state the plan and the cost, then
   write. Practise the shape, not the answer.

2. *How do you approach a bits or maths problem you have not seen?*
   Which of the twelve rather than what is this; constraints first; per number or per group; does anything
   shrink structurally; does the answer need dividing.

3. *What does this system cost to run per month?*
   The four line items with real multiplication, the two lines that appear on no diagram, the total, cost per
   user, and the two changes you would make.

---

## Before you move on

- [ ] I read constraints before I read the problem.
- [ ] I can name the tool for any trigger in the table within three seconds.
- [ ] I say the recognition sentence out loud before writing.
- [ ] I know the three tools that are secretly one idea.
- [ ] I scored myself on the four mock problems honestly.
- [ ] I know which of 0, 1, 2 and a negative breaks each tool.
- [ ] I can list the five silent failures with the input that exposes each.
- [ ] I know `while n: n &= n-1` hangs on a negative, and why hanging is worse.
- [ ] I would write the explainable version and mention the clever one.
- [ ] I can name the four line items and the fifth that is off the bill.
- [ ] I know observability is often the largest single line.
- [ ] I know egress is ~$0.09/GB and cross-zone is ~$0.01/GB each way.
- [ ] I can say why serving is four times more expensive than storing.
- [ ] I can compute the cross-zone bill from internal call volume.
- [ ] I know zone-aware routing is the fix, not collapsing to one zone.
- [ ] I can give the four ways to buy compute with their discounts.
- [ ] I know to commit to the floor and never to the peak.
- [ ] I know what spot is right for and wrong for.
- [ ] I can give the seven optimisation steps in order.
- [ ] I know the first two are free and often the biggest.
- [ ] I can compute the non-production idle saving.
- [ ] I know what tagging buys and how it has to be enforced.
- [ ] I know a cost bug pages nobody, and the alert that fixes that.
- [ ] I can give cost per user and per thousand requests for a stated system.
- [ ] I know to ask what an hour of downtime costs before buying a nine.
- [ ] I answered all three questions above out loud.
