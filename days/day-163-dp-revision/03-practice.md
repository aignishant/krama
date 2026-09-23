---
day: 163
track: practice
title: "Practice — Dynamic programming revision and mock round"
status: written
---

# Day 163 · Practice

**DSA topic:** Dynamic programming revision and mock round
**System design topic:** Design an e-commerce system

---

## Code these, in this order

Today's rule is different: **use a clock, and score yourself honestly.** Twenty-five minutes each, no notes,
no looking anything up. **Write down `minutes_to_state` for every one of them** — that number is what this
whole day is measuring, and it predicts everything else.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | House Robber III | LeetCode 337 (Medium) | Tree DP under a clock, and the `(take, skip)` state. |
| 2 | Extra Characters in a String | LeetCode 2707 (Medium) | 1-D DP, and noticing the hidden cubic cost. |
| 3 | Partition Array for Maximum Sum | LeetCode 1043 (Medium) | The last-group decomposition. |
| 4 | Best Time to Buy and Sell Stock IV | LeetCode 188 (Hard) | Three dimensions, and the `k ≥ n/2` shortcut. |
| 5 | Burst Balloons | LeetCode 312 (Hard) | Interval DP, and the last-not-first inversion. |
| 6 | Minimum Cost to Cut a Stick | LeetCode 1547 (Hard) | Interval DP you have not seen, from the shape alone. |

### On all six, run the clock and record five numbers

For each: **minutes to a stated state, minutes total, whether you gave the complexity unprompted, whether you
handled the edge cases, whether it ran first time.** Score them with the rubric.

**Then look at the pattern rather than the average.** Three of the six slow to the state means something
different from three of the six failing to run.

### On problem 2, find the hidden cost

After solving it, work out the true complexity including the string slice. **Say whether it is `O(n²)` or
`O(n³)`**, and what constraint makes it fine. Then implement the trie version and **note which direction the
trie has to store the words in**, and why.

### On problem 4, check the shortcut before writing

Read the constraints. Compute the table size for the largest `k`. **Say what fails and at what point.** Then
write the shortcut condition and justify the `n/2`.

### On problem 6, use the shape alone

You have not seen this problem. **Do not look it up.** Work through the diagnostic: signals, test, shape,
state, count. **Note the moment you recognise it as interval DP**, and what gave it away.

Then find the padding trick — **the cuts array needs sentinels at both ends** — and say why, in one sentence.

### Then the fifteen-bugs drill

Take one solved problem and **deliberately introduce each of the fifteen silent bugs**, one at a time. For
each, record: what the answer becomes, and whether any test you would naturally write would catch it.

**Count how many your natural tests miss.** That number is why the random-verification habit exists.

### Then the verification drill

For two of the six problems, write a brute-force version and check the DP against it on three hundred random
inputs. **Time how long writing the brute force took.** Compare that with how long you spent debugging.

### Then the recall drill

Close everything. Out loud, from memory:

1. The eight shapes with their states.
2. The thirteen recurrences.
3. The three non-obvious fill orders.
4. The five space collapses.

**Record which ones you could not produce.** Those are your revision list, and there will be fewer than you
expect.

---

### The compression drill

1. State DP in one sentence.
2. Give the five-step recognition procedure.
3. Give the eight shapes and one example each.
4. Give the constraint-to-complexity table.

### The recurrence drill

Write each from memory, with its loop direction and base case:

1. 0/1 knapsack, one row.
2. Unbounded knapsack, one row.
3. Coin change, minimum.
4. Coin change, count combinations.
5. Longest increasing subsequence.
6. Longest common subsequence.
7. Edit distance.
8. Grid paths, one row.
9. Palindrome table.
10. Interval DP skeleton.
11. Stock, two states.
12. Tree DP skeleton.
13. TSP.

### The silent-bugs drill

Give all fifteen from memory. For each, say what the wrong answer looks like — **too big, too small, or a
different correct answer to a different question.**

### The rubric drill

1. Give the seven scored items in weight order.
2. Say which two surprise people, and why.
3. Give the forty-five-minute budget.
4. Say what the first ten minutes buy.
5. Say what a candidate who codes at minute four loses.

### The follow-ups drill

For each, give a two-sentence answer:

1. What is the complexity?
2. Can you reduce the space?
3. Can you do better?
4. What is your state, and why is it enough?
5. What happens on an empty input?

### The self-diagnosis drill

After scoring the six problems:

1. Say what your average was.
2. Say which of the five rubric items you lost most points on.
3. Name three specific gaps, not "revise DP".
4. Estimate the revision time for each. (It should be twenty minutes, not a week.)

---

### The split drill

1. Give both halves with volumes and requirements.
2. Give the ratio and say what it implies.
3. Say what store each half wants, and why the instinct is wrong for one of them.

### The inventory drill

1. Describe the read-then-write race, step by step.
2. Say why it never appears in testing.
3. Give all three correct fixes and when each is right.
4. Say why you check the row count and not the new value.
5. Describe the three stock states.
6. Say what the TTL prevents and what message never arrives.
7. Compute what the missing expiry job costs per day.

### The payment drill

1. Say where the idempotency key comes from and what the near-miss mistake is.
2. Give the two-phase sequence and why that order.
3. Say what a void costs and what a refund costs.
4. Compute the annual fee difference at 1% refunds.
5. Say what happens when the timeout came after the charge succeeded.
6. Name the two mechanisms that resolve that.

### The saga drill

1. Say why a distributed transaction is not available.
2. Give the state machine and three compensations.
3. Say why the compensations are not symmetric.
4. Say what the transition table prevents.
5. Describe the outbox and what it prevents.
6. Say what it implies about consumers.

### The flash-sale drill

1. Say what breaks and what does not.
2. Give the row throughput and compute the queueing time.
3. Give the three mitigations in order.
4. Give the cost of sharding, precisely.
5. Say what you would change about reservations.
6. Say what the honest framing of "sold out" is.

### The sizing drill

1. Compute the read-to-write ratio.
2. Compute the order storage per year.
3. Compute the payment fees per day.
4. Compare infrastructure with payment fees.
5. Give the latency budget and name the dominating component.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Walk me through how you approach any DP problem.*
   The five-step recognition, the state as a sentence, the completeness check, the count, and then the coding
   order — with the time budget.

2. *What are the mistakes that produce wrong answers with no error?*
   As many of the fifteen as you can, grouped by what the wrong answer looks like, and the habit that catches
   all of them.

3. *Design an e-commerce checkout.*
   The 2,000:1 split, the read-then-write race and its fix, the three stock states with the TTL, two-phase
   payment with the void-versus-refund argument, and the saga with its outbox.

---

## Before you move on

- [ ] I timed all six problems and recorded `minutes_to_state`.
- [ ] I scored myself with the rubric, honestly.
- [ ] I named three specific gaps, not "revise DP".
- [ ] I can state DP in one sentence.
- [ ] I can give the five-step recognition procedure.
- [ ] I can give the eight shapes and their states.
- [ ] I can give the constraint-to-complexity table.
- [ ] I can write all thirteen recurrences from memory.
- [ ] I know the three non-obvious fill orders.
- [ ] I know the five space collapses, including the two that are "no".
- [ ] I can list the fifteen silent bugs.
- [ ] I know which produce too-big and which too-small answers.
- [ ] I have the random-verification habit.
- [ ] I know the rubric's seven items in weight order.
- [ ] I know why "did the code run" is item six.
- [ ] I know the forty-five-minute budget and write no code before minute thirteen.
- [ ] I say the complexity unprompted.
- [ ] I can answer all five standard follow-ups in two sentences each.
- [ ] I can give the e-commerce read-to-write ratio and what it implies.
- [ ] I can describe the read-then-write race step by step.
- [ ] I know all three correct inventory fixes and when each applies.
- [ ] I know why you check the row count, not the new value.
- [ ] I can describe the three stock states and the TTL's job.
- [ ] I can compute what a missing expiry job costs.
- [ ] I know where the idempotency key comes from and the near-miss mistake.
- [ ] I can give the two-phase sequence and justify the order with fees.
- [ ] I know what to do when a timeout hides a successful charge.
- [ ] I can explain the saga, its compensations, and the outbox.
- [ ] I know what breaks in a flash sale and the three mitigations.
- [ ] I know the cost of sharding a counter.
- [ ] I answered all three questions above out loud.
