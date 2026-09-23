---
day: 165
track: practice
title: "Practice — Proving a greedy choice, simply"
status: written
---

# Day 165 · Practice

**DSA topic:** Proving a greedy choice, simply
**System design topic:** Design a ticket booking system

---

## Code these, in this order

One rule for the whole set: **write the exchange argument as a docstring before you write the function body.**
If you cannot write it, you do not know the algorithm is correct — and you find that out in two minutes rather
than in an interview.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Minimum Number of Arrows to Burst Balloons | LeetCode 452 (Medium) | The same exchange as activity selection, in disguise. |
| 2 | Queue Reconstruction by Height | LeetCode 406 (Medium) | A greedy whose argument is genuinely subtle. |
| 3 | Task Scheduler | LeetCode 621 (Medium) | Greedy plus a formula, and why the formula is right. |
| 4 | Course Schedule III | LeetCode 630 (Hard) | An exchange with an undo — greedy that reconsiders. |
| 5 | Minimum Cost to Connect Sticks | LeetCode 1167 (Medium) | Huffman, under a different name. |
| 6 | Job Sequencing with Deadlines | classic — write it yourself | The full argument, including where it breaks. |

### On all six, write the argument first

For each, before coding: **state the greedy rule, then write the exchange argument as three sentences** — take
any optimal solution, swap the greedy choice in, show it is still legal and no worse.

**Record which ones you could not complete.** Those are the ones where you were about to guess.

### On problem 1, notice it is the same problem

Before solving it, say in one sentence why bursting balloons with arrows is activity selection. **Then check
whether your exchange argument transfers word for word.** It should.

### On problem 2, find the argument that is actually hard

The greedy here — sort by height descending, then insert each person at the index of their `k` value — **is
correct and the reason is not obvious.** Spend five minutes trying to construct the exchange argument before
looking anything up. **Write down where you got stuck**, because that is the point of the exercise.

### On problem 3, prove the formula rather than the loop

The answer is a closed form based on the most frequent task. **Say why that formula is a lower bound**, and
then say why it is achievable. **Two separate arguments** — and most explanations give only the first.

### On problem 4, find the undo

This greedy takes courses and then **removes one it already took** when a better option appears. **Say what
makes that still a greedy algorithm**, and construct the exchange argument for the removal step specifically.

### On problem 6, break it deliberately

Solve it for unit-duration jobs. **Then change the problem so jobs take different amounts of time** and try to
construct the same argument. **Find the exact sentence that stops working**, and build the counter-example it
describes.

### Then the argument-completion drill

For each of these, write the exchange argument or say why it fails:

1. Activity selection by end time.
2. Activity selection by start time.
3. Fractional knapsack by ratio.
4. 0/1 knapsack by ratio.
5. Shortest job first.
6. Longest job first.
7. Huffman: merge the two rarest.
8. Coin change: take the largest coin.

**Four have arguments and four have counter-examples.** For the four that fail, **say where the argument breaks
before constructing the input**, and check that the input matches the failure.

### Then the empirical drill

Write a brute force for activity selection at `n ≤ 8`. For every random instance where the optimal solution
does not contain the earliest finisher, **try every possible single swap and record whether one works.**

**Run four hundred instances.** Any failure means the exchange argument is wrong.

---

### The claim drill

1. State exactly what greedy needs to establish.
2. Say why it is "an" optimal solution rather than "the".
3. Say why the weaker claim is easier to prove.
4. Say what makes the induction work.

### The exchange drill

1. Give the three steps.
2. Name the two halves of step three.
3. Say which half is usually omitted.
4. Give the argument for activity selection, in full.
5. Compress it to one sentence.

### The adjacent-swap drill

1. Say why it is the easiest form.
2. Give it for shortest job first.
3. Say exactly what the saving equals.
4. Say when you should look for this form first.

### The stays-ahead drill

1. State it in two sentences.
2. Give it for activity selection.
3. Say what it needs that exchange does not.
4. Name a problem where it does not apply, and why.

### The failed-proof drill

1. Say what a failed proof gives you.
2. Give the exact sentence where 0/1 knapsack breaks.
3. Build the counter-example from that sentence.
4. Say why the fractional version survives the same argument.
5. Say what changes in the problem statement between them.

### The what-to-say drill

1. Give the thirty-second, three-sentence version.
2. Say what you say when you cannot fill in the blanks.
3. Say why that is a good answer rather than a concession.
4. Say what over-formalising looks like and why it costs you.

---

### The difference drill

1. Give the two properties that make tickets unlike ordinary stock.
2. Say why there is no oversell recovery.
3. Say why a counter does not work.
4. Say what predictability buys you.

### The hold drill

1. Give the three seat states.
2. Say why the hold must be atomic, and give both correct forms.
3. Say what the TTL prevents and what message never arrives.
4. Say why release must be a script, and what bug it prevents.
5. Describe the group-booking deadlock and the one-word fix.
6. Say why a partial acquisition must roll back.

### The spike drill

1. Compute the ordinary rate and the sale-opening rate.
2. Say why retries make the failure worse than it first appears.
3. Give the three layers in order.
4. Say why the visible position matters, and what it prevents.
5. Say what randomised admission removes, and what it costs.
6. Say what "reject early" controls and what it cannot.
7. Name the risk the waiting room introduces.

### The seat-map drill

1. Say why a stale map is correct rather than a compromise.
2. Say where the authoritative check happens.
3. Compute polling versus pushing, both figures.
4. Say what the real cost of pushing is.

### The TTL drill

1. Give both directions of the trade.
2. Say what 3-D Secure does to the arithmetic.
3. State the asymmetry between overselling and underselling.
4. Say which way the number drifts, and why.
5. Name the two metrics you would put on a dashboard.
6. Give two mechanisms that soften the trade.

### The bots drill

1. Say why bots are first-class here.
2. Name five defences.
3. Say which is most effective and how it is defeated.
4. Say where the challenge belongs and why.
5. State the realistic goal honestly.

### The sizing drill

1. Compute the durable write rate at sell-out.
2. Say where the difficulty actually is.
3. Compute the hold storage.
4. Say what the WebSocket connection count costs.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Why does your greedy choice work?*
   The claim in its weak form, the three-step exchange, both halves of step three, and the activity-selection
   argument compressed to one sentence.

2. *What if you cannot prove it?*
   What a failed proof tells you, the exact sentence where 0/1 knapsack breaks, the counter-example it
   describes, and what you say to the interviewer.

3. *Design a ticket booking system.*
   Why tickets are unlike stock, the atomic hold with its TTL, the three spike layers, why a stale seat map is
   correct, and the TTL trade with its asymmetry.

---

## Before you move on

- [ ] I can state exactly what greedy needs to establish.
- [ ] I know why "an" optimal solution rather than "the".
- [ ] I can give the three-step exchange argument.
- [ ] I always show both halves: still legal, and no worse.
- [ ] I know which half people omit.
- [ ] I can give the activity-selection argument in full and in one sentence.
- [ ] I look for the adjacent-swap form first, and know why.
- [ ] I can give the shortest-job-first argument and its exact saving.
- [ ] I can state "greedy stays ahead" and say when to use it.
- [ ] I know a failed proof names the counter-example.
- [ ] I can give the sentence where 0/1 knapsack breaks.
- [ ] I can build the counter-example from that sentence.
- [ ] I know why the fractional version survives.
- [ ] I can give the thirty-second version, unprompted.
- [ ] I know what to say when I cannot complete the argument.
- [ ] I know why that is a good answer.
- [ ] I wrote the argument as a docstring for all six problems.
- [ ] I can say what makes tickets unlike ordinary inventory.
- [ ] I know why there is no oversell recovery.
- [ ] I can give the three seat states and both atomic hold forms.
- [ ] I know why release must be a script.
- [ ] I know the group-booking deadlock and its one-word fix.
- [ ] I can compute the ordinary rate and the spike rate.
- [ ] I know why retries make the spike worse than it appears.
- [ ] I can name the three spike layers and what each does.
- [ ] I know why a visible queue position matters.
- [ ] I know why a stale seat map is correct.
- [ ] I can compute polling versus pushing.
- [ ] I can state the TTL trade and its asymmetry.
- [ ] I know the realistic goal for bot defence.
- [ ] I answered all three questions above out loud.
