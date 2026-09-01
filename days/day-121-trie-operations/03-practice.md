---
day: 121
track: practice
title: "Practice — Insert, search, and prefix search"
status: written
---

# Day 121 · Practice

**DSA topic:** Insert, search, and prefix search
**System design topic:** The saga pattern

---

## Code these, in this order

One rule for the whole set: **write the four delete cases as tests before you write delete.** Absent word,
word that is a prefix of another, word that extends another, word alone on its branch. If your four
assertions on `node_count()` are wrong, the implementation will be too.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Implement Trie (Prefix Tree) | LeetCode 208 (Medium) | `search` vs `startsWith` — one condition apart. |
| 2 | Design Add and Search Words Data Structure | LeetCode 211 (Medium) | Wildcards: a walk becomes a DFS. |
| 3 | Replace Words | LeetCode 648 (Medium) | Stopping at the *first* `is_end`, not the last. |
| 4 | Word Search II | LeetCode 212 (Hard) | Pruning a grid search with a trie — the real payoff. |
| 5 | Word Break | LeetCode 139 (Medium) | The trie replacing the set lookup, plus memoisation. |

### Delete is not on LeetCode. Write it anyway.

Add `delete` to your problem 1 solution and test all four cases by asserting `node_count()` after each.
The five numbers from the lesson are 9, 9, 8, 7, 5. If you get different ones, find out why before moving
on — this is the one operation an interviewer will ask for and no online judge will check.

### On problem 2, break the base case deliberately

Change `return node.is_end` to `return True` and record what `search("ca")` returns when only `"cat"` is
stored. Then change the wildcard loop to `return self._match(...)` inside the loop and record which
patterns start failing.

### On problem 4, measure the pruning

Solve it once with a plain word list and once with a trie. Count how many grid cells each version visits.
Two numbers. Say why the trie version can abandon a path several characters early.

### On problem 5, say why a trie helps at all

A hash set already gives `O(1)` lookup here. State what the trie buys you and be honest if the answer is
"not much" for the standard version — then say which variant makes it worth it.

---

### The three-operations drill

1. Write the shared walk from memory.
2. Write insert, search and `starts_with` on top of it.
3. Say the single condition that differs between the last two.
4. Say what makes insert idempotent, and what breaks that.

### The delete-rule drill

1. State the pruning rule in one line, both conditions.
2. Say what each condition means in terms of who is using the node.
3. Say why it must be evaluated bottom-up.
4. Say what the recursive delete's return value means, in words.

### The four-cases drill

1. Name all four cases with an example each.
2. For each, say how many nodes are removed.
3. Say which two are mirror images and which one breaks naive implementations.
4. Give the five `node_count()` values from the lesson's run.

### The delete-implementation drill

1. Write the recursive version from memory.
2. Write the iterative version from memory.
3. Point at the line in the iterative version that is the pruning rule.
4. Say why the `del` must come before the prunability check.
5. Say why the two-pass version is the one to write in an interview.

### The wildcard drill

1. Say what changes when a `.` appears — walk to what?
2. Write `_match` from memory.
3. Say what the base case must return, and what happens if it returns `True`.
4. Say what goes wrong if the loop returns instead of continuing.
5. Give the worst-case complexity and then the practical correction.

### The wildcard-cost drill

1. Give the branch counts for `cat`, `c.t`, `.at`, `..t` on an English trie.
2. Say why the practical number is far below `26^w`.
3. Compare `c...` with `...t` and say why they differ by ten times.
4. Give the free optimisation for fixed-length patterns.
5. Say what a reversed second trie would buy, and what it costs.

### The completions drill

1. Say what `completions("")` returns without a limit.
2. Write the bounded version with an explicit stack.
3. Say why the stack pushes in reverse alphabetical order.
4. Say how the design changes if "top" means most popular rather than alphabetical.

### The break-it drill

Trigger each and record the exact output or error:

1. Delete `"car"` from `{car, card}` with the `is_end` check missing from the prune rule.
2. `_delete` called directly on a word that is not present.
3. The prunability check placed before the `del`.
4. `search_pattern("ca")` with a base case of `return True`.
5. The wildcard loop written with `return` instead of `if ...: return True`.
6. A recursive delete on a 2,000-character key.
7. `completions("")` on a 100,000-word trie.
8. Removing children from a dict while iterating over it.

---

### The definition drill

1. Define a saga in one sentence.
2. Say what a compensating transaction is.
3. State the difference between compensation and rollback, with the payment example.
4. Say which step you start compensating from when step 4 fails, and why.

### The ordering drill

1. State the ordering rule for saga steps.
2. Say why it is counter-intuitive.
3. Give three examples of steps that cannot be compensated.
4. Say what you do with a step that truly cannot be undone.

### The two-styles drill

1. Describe choreography and orchestration in two sentences each.
2. Give the step-count rule and the reason behind it.
3. State the strongest argument against choreography.
4. State the two costs of an orchestrator.
5. Say what makes an orchestrator different from a function that calls four services.

### The isolation drill

1. Say what a saga gives up beyond atomicity.
2. Name the three hazards and give a scenario for each.
3. Name the four countermeasures and say what each catches.
4. Give the commutative-update example, both the safe and unsafe forms.
5. Say plainly what none of the countermeasures can fix.

### The production-rules drill

1. State the three rules that make sagas work.
2. Say why every step needs an idempotency key, and where it is checked.
3. Say what happens to a compensation that keeps failing.
4. Explain why the expiry job is the most important part of the design.
5. Say what the expiry interval equals, in terms of consistency.

### The outbox drill

1. State the problem the outbox solves.
2. Give both wrong orderings and say what each loses.
3. Write the SQL.
4. Say why events can be published twice and why that is acceptable.
5. Say what property that requirement forces on every consumer.

### The numbers drill

1. Break a four-step saga into its latency components.
2. Say what dominates, and by how much.
3. Compare saga and 2PC on latency and on hot-row throughput.
4. Give the availability figures for both.
5. List the inconsistency windows for five failure scenarios.
6. Compute the monthly refund cost for a million orders at two percent.
7. Size the orchestrator's state and its history.

### The trade-offs drill

1. Fill in the nine-row saga-versus-2PC table.
2. Say where each one's complexity lives, and why that matters.
3. Give five situations where a saga is the wrong choice.
4. Say which loss people underestimate, and why it is worse than the other.
5. Say what a team must have in place before running sagas in production.

### The failure drill

For each, say what happens and what you would build:

1. Payment succeeds, shipping fails, and the refund call times out.
2. A message is redelivered and the card is charged twice.
3. The orchestrator restarts mid-saga.
4. An event is published but the database write was rolled back.
5. A customer sees an item as out of stock during a 300 ms window and leaves.
6. A compensation lands in the dead-letter queue at 3 a.m.
7. Two sagas update the same balance and one compensates.

Two of the seven are not fixed by better retry logic. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Implement a trie, then delete a word from it.*
   The shared walk and the three one-liners, then the pruning rule with both conditions, why it is
   bottom-up, and all four cases with the prefix case named as the one that breaks naive code.

2. *Order service and payment service, separate databases. Keep them consistent.*
   2PC rejected for three named reasons, the saga described, compensation-is-not-rollback stated plainly,
   orchestration chosen with the reason, and both losses — eventual atomicity and no isolation — admitted
   before being asked.

3. *What if the compensation fails?*
   Retry forever with backoff, idempotent, dead-letter and alert — then the real answer: design so a lost
   compensation is survivable, with the expiry job and the window it defines.

---

## Before you move on

- [ ] I can write the shared walk and all three operations on top of it.
- [ ] I can name the one condition separating `search` from `starts_with`.
- [ ] I can state the pruning rule with both conditions.
- [ ] I can say why delete must be bottom-up.
- [ ] I can name all four delete cases and how many nodes each removes.
- [ ] I know that deleting `car` must not remove `card`.
- [ ] I wrote delete recursively and iteratively.
- [ ] I know the `del` comes before the prunability check.
- [ ] I know delete is `O(L)`, not `O(n)`.
- [ ] I can write the wildcard match from memory.
- [ ] I know the base case returns `is_end`, never `True`.
- [ ] I can give the worst case and the practical correction for wildcards.
- [ ] I know why wildcard position matters more than wildcard count.
- [ ] My completions take a limit and stop early.
- [ ] I know when to use the iterative delete.
- [ ] I can define a saga and a compensating transaction.
- [ ] I can say why compensation is not rollback, with an example.
- [ ] I know irreversible steps go last, and why.
- [ ] I can choose between choreography and orchestration with a reason.
- [ ] I know an orchestrator must write state durably before every call.
- [ ] I can name the three isolation hazards and the four countermeasures.
- [ ] I can say what none of the countermeasures fix.
- [ ] I know every step and every compensation must be idempotent.
- [ ] I know a failed compensation is an incident, not a retry.
- [ ] I know the expiry job is the safety net and defines the worst-case window.
- [ ] I can describe the outbox pattern and write the SQL.
- [ ] I know sagas win on contention, not latency.
- [ ] I can give the operational cost of compensating at scale.
- [ ] I know five situations where a saga is the wrong choice.
- [ ] I answered all three questions above out loud.
