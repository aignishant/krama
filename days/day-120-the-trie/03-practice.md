---
day: 120
track: practice
title: "Practice — The trie: a tree of characters"
status: written
---

# Day 120 · Practice

**DSA topic:** The trie: a tree of characters
**System design topic:** Distributed transactions and two-phase commit

---

## Code these, in this order

One rule for the whole set: **write the node class from memory before you look at anything.** Two fields.
If you cannot produce those two lines cold, nothing else in this topic will come.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Implement Trie (Prefix Tree) | LeetCode 208 (Medium) | The node, insert, and `search` vs `startsWith`. |
| 2 | Longest Common Prefix | LeetCode 14 (Easy) | Whether you know a trie is *overkill* here. |
| 3 | Longest Word in Dictionary | LeetCode 720 (Medium) | Every prefix must also be a word — `is_end` used as a real condition. |
| 4 | Replace Words | LeetCode 648 (Medium) | Stopping the walk at the first `is_end`. |
| 5 | Map Sum Pairs | LeetCode 677 (Medium) | The `words_below` augmentation, with sums instead of counts. |

### On problem 1, write the two one-liners side by side

`search` and `startsWith`, adjacent, and say aloud the single condition that differs. Then insert `"card"`
only and check `search("car")`, `startsWith("car")`. Record both.

### On problem 2, solve it twice

Once with a trie, once with a plain vertical scan. Compare line counts and memory. Say which you would write
in an interview and why. This problem is here to teach you when *not* to use today's structure.

### On problem 3, notice what `is_end` is doing

The condition is that every prefix of the answer is also a word. Say why that makes this a trie problem
rather than a sorting problem, and what would change if the condition were dropped.

### On problem 5, add the augmentation

Store a running value at every node on the insert path. Then handle the update case — inserting the same key
twice with different values — and record what breaks if you only add rather than adjust by the difference.

### Measure the memory yourself

Build a trie over an English word list and over the same number of random 10-character strings. Print
`node_count()` for both, and the character totals. Two ratios. Keep them; they are the argument you will
make in the interview.

---

### The structure drill

1. Write `TrieNode` from memory. Two fields.
2. Say what a node does *not* contain, and why that matters.
3. Say where the letter actually lives.
4. Say what the root represents.

### The path drill

1. State "the path is the key" and explain it in two sentences.
2. Given a trie of `car, card, cat, do`, list every node and say which are words.
3. Say how many nodes exist and how many characters were stored.
4. Say why a node cannot report its own prefix.

### The two-flags drill

1. State the two independent questions a node answers.
2. For `card` stored alone, give `is_end` and children for the node at `car`.
3. For `car` and `card` both stored, give the same.
4. State the one thing that is always true about leaves.
5. Say which bug appears if you check `is_end` in `starts_with`, and which if you omit it in `search`.

### The complexity drill

1. Give the cost of insert, search, prefix-exists and collect.
2. Say what is missing from all four, and why that is unusual.
3. Compare a prefix query against a hash set and a sorted array at n = 1,000,000.
4. Say which of the three you would pick for a static word list, and why.

### The memory drill

1. Say how many nodes a trie creates, in terms of prefixes.
2. Give a realistic bytes-per-node figure for Python and say where it goes.
3. Compute the memory for 100,000 English words and compare with a set.
4. Compute it for 1,000,000 UUIDs and give the ratio.
5. State the rule for when a trie is worth its memory.

### The alternatives drill

1. Describe a radix tree and give the typical node reduction.
2. Describe a DAWG and say what it cannot do.
3. Say what a ternary search tree trades.
4. Say which one a router uses and why.

### The variants drill

1. Compare the dict node and the array-of-26 node on three axes.
2. Say which you would use in Python and which in C++, with reasons.
3. Say what breaks in the array version with uppercase input, and what breaks with accented input.
4. Say what `words_below` buys and how many lines it costs.

### The break-it drill

Trigger each and record the exact output or error:

1. `insert` with the final `is_end = True` line removed, then any `search`.
2. `search("car")` with only `"card"` stored.
3. `starts_with` written with the `is_end` check included.
4. `ord('A') - ord('a')` used as a list index.
5. `ord('é') - ord('a')` used as a list index.
6. A recursive collect over a key 2,000 characters long.
7. `words_with_prefix("")` on a full dictionary.
8. Accessing `node.word` on a plain `TrieNode`.

---

### The problem drill

1. State what a distributed transaction is, in one sentence.
2. Say why a single-machine transaction cannot be extended to two machines.
3. Give the concrete two-database failure that motivates the whole lesson.

### The protocol drill

1. Name the two roles.
2. Describe phase one, including what the participant does before voting.
3. Say what a `yes` vote commits the participant to.
4. Say why the vote must be fsynced before it is sent.
5. Describe phase two and say how much say participants have in it.
6. Name the exact moment the transaction becomes real.

### The blocking drill

1. Describe the failure that defines 2PC, step by step with timings.
2. Say why a stuck participant cannot commit.
3. Say why it cannot abort.
4. Say why asking the other participants does not help.
5. State the theorem in one sentence.
6. Say what actually resolves it in production.

### The asymmetry drill

1. Say what a participant in doubt must do.
2. Say what a coordinator in doubt does, and which way it decides.
3. Explain why that is safe and not arbitrary.
4. Say what `presumed abort` saves.

### The comparison drill

1. Give four differences between 2PC and consensus.
2. Say which needs a majority and which needs unanimity.
3. Say which gets more reliable as machines are added, and which gets less.
4. Describe the modern combination of the two and name two systems that use it.

### The numbers drill

1. Break a 2PC transaction into its steps with timings and count the fsyncs.
2. Say what dominates in one data centre.
3. Compute cross-region latency and say which participant sets it.
4. Compute availability for 2, 3, 5 and 10 participants at 99.9% each.
5. Compare with a five-node Raft cluster.
6. Give the lock window in both cases and the throughput consequence on a hot row.

### The trade-offs drill

1. Give four situations where 2PC is the right answer.
2. Give five where it is not.
3. State the real objection to 2PC in microservices, and say why it is not speed.
4. Fill in the six-row alternatives table.
5. Say what the first question about any distributed transaction should be.
6. Say what 2PC does *not* give you, in terms of ACID letters.

### The variants drill

1. Describe three-phase commit in two sentences.
2. Say what it fixes and what it does not.
3. Say why "worse than blocking" is the right criticism of it.
4. Say what `XA` is and give the Postgres commands.
5. Give the Postgres default for `max_prepared_transactions` and say what it signals.

### The failure drill

For each, say what happens and what you would do:

1. A participant votes yes, then loses power.
2. The coordinator writes COMMIT, then loses power before sending anything.
3. The coordinator loses power after collecting votes but before writing the decision.
4. One of five participants is unreachable during phase one.
5. A prepared transaction is found holding locks on a production table with no coordinator alive.
6. A reservation is created, the follow-up write fails, and the compensating action also fails.

Two of the six are not fixed by anything inside 2PC. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Implement a trie, and tell me why not just use a hash set.*
   The prefix query as the reason the structure exists, the path being the key with no word in any node,
   the two fields, `search` versus `startsWith` as one differing condition, `O(L)` with no `n`, and the
   memory cost stated honestly with the random-key case.

2. *Two databases, one transaction. How?*
   The problem, both phases with the promise and the fsync, the decision point named, the blocking failure
   in full, the lock-window and availability arithmetic, and where you would go instead.

3. *What happens if the coordinator dies?*
   The in-doubt window, why the participants cannot decide, the asymmetry between participant and
   coordinator recovery, and the Raft-replicated-coordinator fix.

---

## Before you move on

- [ ] I can write `TrieNode` from memory, two fields.
- [ ] I can say what a node does not contain and where the letter lives.
- [ ] I can state "the path is the key" and explain it.
- [ ] I can write `insert` including the final `is_end` line.
- [ ] I can write `search` and `starts_with` and name the one differing condition.
- [ ] I know that existence and word-ness are separate facts.
- [ ] I know the one thing that is always true about leaves.
- [ ] I know all four operations are `O(L)` with no `n`.
- [ ] I can name the three things a hash set cannot do.
- [ ] I can give the memory arithmetic for English words and for random keys.
- [ ] I know the rule for when a trie is worth its memory.
- [ ] I know a sorted array is the real competitor, and where the trie beats it.
- [ ] I can describe a radix tree and a DAWG.
- [ ] I know `words_below` and what it buys.
- [ ] I know a trie does prefixes, not substrings.
- [ ] I can describe both phases of 2PC precisely.
- [ ] I know a `yes` vote is an irrevocable promise and must be fsynced first.
- [ ] I can name the exact moment the transaction becomes real.
- [ ] I can describe the blocking failure without notes.
- [ ] I can state why no protocol avoids it under partitions.
- [ ] I know the participant/coordinator recovery asymmetry.
- [ ] I can give the availability product and compare it with Raft.
- [ ] I can give the lock-window argument with throughput numbers.
- [ ] I know 2PC gives atomicity but not isolation.
- [ ] I know the real objection in microservices is coupling.
- [ ] I know 3PC exists, what it fixes, and why nobody uses it.
- [ ] I would ask why the data is distributed before designing anything.
- [ ] I answered all three questions above out loud.
