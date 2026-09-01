---
day: 124
track: practice
title: "Practice — Tries revision and mock round"
status: written
---

# Day 124 · Practice

**DSA topic:** Tries revision and mock round
**System design topic:** Failure detection, heartbeats, and timeouts

---

## Code these, in this order

This is a closing day, so the rule is different: **write every one of these from an empty file, with the
lesson closed.** If you have to look something up, finish the problem, then write that template out three
times from memory before starting the next one.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Implement Trie (Prefix Tree) | LeetCode 208 (Medium) | The walk, and the one condition between `search` and `starts_with`. |
| 2 | Design Add and Search Words Data Structure | LeetCode 211 (Medium) | The branching walk, and the base case that must not be `True`. |
| 3 | Word Break | LeetCode 139 (Medium) | Trie plus memo — mock problem 1, timed. |
| 4 | Stream of Characters | LeetCode 1032 (Hard) | The reversed trie — mock problem 2, timed. |
| 5 | Maximum XOR of Two Numbers in an Array | LeetCode 421 (Medium) | A trie over *bits*, not letters. The shape nobody expects. |

### Problem 5 is the one to do properly

Nothing in this phase mentioned numbers, and this is a trie problem. Insert each number as its 32 bits, most
significant first. Then for each number, walk the trie choosing the *opposite* bit at every level, because
the opposite bit is what maximises XOR at that position.

Write down, in one sentence, why greedily taking the opposite bit at the highest position is correct. If you
cannot, that is the thing to fix — the structure is easy and the argument is the interview.

### Run the mock round properly

Twenty minutes each for problems 3 and 4, with a timer, standing up, talking the whole time. Record yourself
if you can bear to. Then listen back for three things:

1. Did you name the recognition reason before writing any code?
2. Did you say the cost out loud without being asked?
3. When you got stuck, did you keep talking, or go quiet?

The third one is the one that fails interviews.

### Then the negative drill

Take five problems you have solved with a trie and, for each, write one line saying what you would use
instead if the trie were banned, and what it would cost. Two of them have a better non-trie answer than you
expect.

---

### The recognition drill

1. State the recognition question in one line, all three parts.
2. Say what each of the three parts throws out.
3. Name the four shapes and give a problem for each.
4. Say the signal for shape 4 in one sentence.
5. Give four situations where the answer is "not a trie".

### The templates drill

Write each from an empty file, timed:

1. Node, insert, `_walk`, `search`, `starts_with`. Target: three minutes.
2. `delete` with the pruning rule. Target: five minutes.
3. `search_pattern` with wildcards. Target: three minutes.
4. `suggest` with gather-and-rank. Target: four minutes.
5. `find_words` on a grid. Target: seven minutes.

### The costs drill

1. Give the cost of every operation in the table, from memory.
2. Say the sentence about what none of them depend on.
3. Give the wildcard cost and say what matters more than the number of dots.
4. Give the two `suggest` costs and say which is worse on a short prefix.
5. Say what is *not* in Word Search II's time complexity, and why that is the whole point.

### The memory drill

1. Compute node count for 100,000 English words, worst case and realistic.
2. Compute the trie's memory and the set's memory, and give the ratio.
3. Name the three ways to cut memory, in order of what they buy.
4. Say what a radix trie collapses and roughly how much it saves on English.

### The five-bugs drill

For each of the five, say the symptom before you say the fix:

1. `search` without `is_end`.
2. Pruning a node that ends a word.
3. Wildcard base case returning `True`.
4. The grid cell never restored.
5. A trie where a set would do.

Four of the five produce no error message. Name which one does.

---

### The impossibility drill

1. Name the four things that produce "stopped answering".
2. Say why no better monitoring separates them.
3. Define false positive and false negative in this context.
4. Say which one a shorter timeout increases and which it decreases.

### The numbers drill

1. Give the detection-time formula and compute it for 1 s and 3 misses.
2. Quote the detection time for Kubernetes liveness defaults and ALB defaults.
3. Compute failed requests from a dead machine at 10,000 QPS over 20 machines, at 30 s and at 5 s.
4. Compute false evictions per day for a 1 s timeout with a 0.1% overrun rate, across 20 machines.
5. Convert those evictions into lost machine-hours at a 20-second cold start.
6. Compare all-to-all and SWIM message rates on 1,000 nodes.
7. Compute gossip propagation time at one round per second on 1,000 nodes.

### The tuning drill

1. Describe the method for picking a timeout from a latency distribution.
2. Say why p999 alone is not enough, and what else you look at.
3. Say what you would measure to find out whether your timeout is too tight.
4. Give the ratio that tells you that, in one sentence.

### The probes drill

1. State the difference between liveness and readiness in one line each.
2. Say what a liveness probe is allowed to check, and the rule behind it.
3. Explain the fleet-wide restart incident from first principles.
4. Say why even readiness should usually not fail hard on a shared dependency.

### The gossip drill

1. Say why all-to-all heartbeating fails at a thousand nodes, with the arithmetic.
2. Describe one SWIM round.
3. Explain the indirect probe and exactly which false positive it removes.
4. Say what gossip gives up in exchange, and how long that window is.

### The fencing drill

1. Describe the scenario where a node comes back after being declared dead.
2. Explain a fencing token in three sentences.
3. Say where the token is checked, and why it must be there rather than in the caller.
4. Say what STONITH is and when you would reach for it.
5. Give the one-sentence version of why fencing beats a better detector.

### The failure drill

For each, say what happens and what you would build:

1. A 2.5-second garbage-collection pause with a 1-second timeout.
2. A liveness probe that checks the database, during a database blip.
3. One bad network link between two nodes in a ten-node cluster.
4. A single central monitor, and the monitor dies.
5. A node evicted, its work reassigned, and the node returns.
6. A thousand-node cluster using all-to-all heartbeats.
7. A cluster where 90% of ejected instances come back healthy within a minute.

Two of the seven are tuning problems and five are design problems. Sort them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Here is a dictionary and a string with no spaces. Can it be split into words?*
   The recognition reason first — repeated prefix questions over a fixed list — then why a set is worse, then
   the trie walk with memoisation, the early exit as the trie earning its keep, and the cost.

2. *Why did you pick a trie here?*
   Prefixes not exact matches; repeated queries against a stable set; `O(L)` independent of `n`. Then the
   memory cost with the number, and the two alternatives you considered.

3. *How do you know a server has died?*
   You do not — four indistinguishable causes. Then suspicion rather than truth, the two errors priced,
   detection time as a formula and a number, the timeout chosen from a distribution, and fencing as the reason
   it does not have to be right.

---

## Before you move on

- [ ] I can state the recognition question in one line.
- [ ] I can name the four shapes and give a problem for each.
- [ ] I can say the signal for shape 4 without hesitating.
- [ ] I can name four cases where a trie is the wrong answer.
- [ ] I wrote all five templates from an empty file.
- [ ] I can give every operation's cost from memory.
- [ ] I can say what none of the basic operations depend on.
- [ ] I can do the memory arithmetic for trie versus set.
- [ ] I know what a radix trie collapses and why it helps.
- [ ] I can name the five bugs and their symptoms.
- [ ] I know which four of the five are silent.
- [ ] I solved the bit-trie problem and can justify the greedy choice.
- [ ] I ran both mock problems timed and out loud.
- [ ] I kept talking when I was stuck.
- [ ] I can name the four causes of "stopped answering".
- [ ] I can define both error types and say which way the timeout moves them.
- [ ] I can give the detection-time formula and three real systems' numbers.
- [ ] I can compute failed requests from a slow detection.
- [ ] I can compute lost capacity from an over-tight timeout.
- [ ] I can describe how to pick a timeout from a distribution.
- [ ] I know the difference between liveness and readiness and the rule behind it.
- [ ] I can explain the fleet-wide restart incident.
- [ ] I can describe a SWIM round and the indirect probe.
- [ ] I can give the message-rate arithmetic for gossip versus all-to-all.
- [ ] I can explain a fencing token and where it is checked.
- [ ] I can say in one sentence why fencing beats a better detector.
- [ ] I answered all three questions above out loud.
