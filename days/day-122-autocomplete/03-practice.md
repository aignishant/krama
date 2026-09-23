---
day: 122
track: practice
title: "Practice — Autocomplete and word dictionaries"
status: written
---

# Day 122 · Practice

**DSA topic:** Autocomplete and word dictionaries
**System design topic:** Idempotency and exactly-once delivery

---

## Code these, in this order

One rule for the whole set: **write the tie-break rule at the top of the file before you write anything
else.** Higher weight first, alphabetically smaller second. Every problem below has a hidden test that
depends on it, and every one of them fails silently rather than loudly when you get it wrong.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Search Suggestions System | LeetCode 1268 (Medium) | Walk, gather, rank — the version you write first. |
| 2 | Longest Word in Dictionary | LeetCode 720 (Medium) | Traversal that stops the moment a node is not a whole word. |
| 3 | Design Search Autocomplete System | LeetCode 642 (Hard) | Weights, the `#` terminator, and state carried between calls. |
| 4 | Top K Frequent Words | LeetCode 692 (Medium) | The same tie rule, without a trie, so you can see it alone. |
| 5 | Replace Words | LeetCode 648 (Medium) | Stopping at the *first* whole word on the path, not the deepest. |

### On problem 1, solve it twice

Once with a trie, once by sorting the product list and using `bisect` to find the block of names sharing the
prefix. Record how many lines each takes. Then say out loud which one you would write in an interview and
why — the honest answer is not always the trie.

### On problem 3, the `#` is the whole problem

Record what your solution does when `#` arrives and the typed sentence is one that already exists, and when
it is brand new. Then break it deliberately: reset the current sentence *before* storing it instead of after,
and record which test fails.

### On problem 5, count the visits

Solve it once by checking every dictionary word against every sentence word, and once with a trie that stops
at the first root. Count how many character comparisons each version makes on a 1,000-word dictionary. Two
numbers, said out loud.

### Then build the precomputed version

Take your problem 1 solution and add a `top` list to every node, maintained on insert. Then:

1. Time 10,000 calls to `suggest("a")` on a 100,000-word dictionary, both versions. Two numbers.
2. Measure the memory of both with `sys.getsizeof` walked over the trie, or `tracemalloc`. Two numbers.
3. Delete the most popular word and print the root's `top` list. Say why it is now wrong.

---

### The two-versions drill

1. Say what `suggest` costs in version one, with every term named.
2. Say what it costs in version two, and what `add` costs in exchange.
3. Give the crossover: at what read-to-write ratio does version two stop being worth it?
4. Say why the first keystroke is the expensive one.

### The ranking drill

1. State the tie rule in one line.
2. Say what happens to your output if you sort on weight alone.
3. Write the sort key from memory, and say what the minus sign is doing.
4. Say why `nsmallest` with negated weights is correct and `nlargest` without them is not.

### The collect drill

1. Write `_collect` from memory.
2. Say why the check on the current node comes before the loop.
3. Say what `so_far` is and what breaks if you start it as an empty string.
4. Rewrite it with an explicit stack, no recursion.

### The precomputation drill

1. Say which nodes an insert has to update, and why no others.
2. Write `_offer` from memory, including the line that removes the old entry.
3. Say what `suggest("")` returns and why it is free.
4. Say what depth you would stop storing front rows at, and why.

### The staleness drill

1. Say why a deletion cannot be repaired locally.
2. Give the three answers, in the order you would offer them.
3. Say which one real systems use.
4. Say what "swap it in atomically" means in one sentence.

### The break-it drill

Trigger each and record the exact output or error:

1. `_collect` that checks the child instead of the current node, asked for `car`.
2. `suggest("")` on a 100,000-word dictionary, with no special case.
3. A heap holding `(weight, node)` tuples where two weights are equal.
4. `_collect` on a key of 2,000 characters.
5. `_offer` without the line that removes the existing entry, after `add("car")` twice.
6. `_collect` called with an empty `so_far` instead of the prefix.

---

### The definition drill

1. Define idempotent in one sentence, with one example of each kind.
2. Say what a timeout actually tells you, and name the three cases.
3. Say which of the three cases costs money, and why it is invisible to the caller.
4. Define at-most-once, at-least-once and exactly-once in one line each.

### The key drill

1. Say who generates the idempotency key, and when.
2. Say what goes wrong if the receiver generates it.
3. Say what goes wrong if the client generates a fresh one per HTTP attempt.
4. Give the one-sentence rule you would put in the API documentation.

### The ordering drill

1. State the three steps of the insert-before-work sequence.
2. Say what breaks if you do the work first.
3. Say what the unique constraint is doing that your code cannot.
4. Say what you return for `IN_PROGRESS`, and why you cannot return the response.

### The exactly-once drill

1. Say in two sentences why exactly-once delivery is impossible.
2. Say what exactly-once effect is, and how you build it.
3. Say exactly what Kafka's transactions do guarantee, and where that guarantee stops.
4. Say what makes a read-process-write pipeline into a single store genuinely exactly-once.

### The natural-idempotency drill

1. Give the absolute and relative versions of a balance update, and say which is safe.
2. Write the state-machine `UPDATE` that is idempotent by construction.
3. Say why `PUT` needs no key and `POST` does.
4. Say what a conditional write buys you over a dedup table.

### The numbers drill

1. Compute ambiguous requests per day at ten million payments and a 0.1% timeout rate.
2. Compute the daily rupee cost of double charges from those, showing every step.
3. Size the dedup store: bytes per key, per day, at a 24-hour retention.
4. Compute the retry amplification for three tiers retrying three times.
5. Size Kafka's dedup window at 50,000 messages a second over five minutes.

### The trade-offs drill

1. Say what you give up by adding a dedup store, in latency and in load.
2. Say what happens when the dedup store is down, and which way you fail for payments.
3. Say why the dedup store cannot be eventually consistent.
4. Say what idempotency does *not* protect, with two examples.
5. Name the situation where the whole mechanism is dead weight.

### The failure drill

For each, say what happens and what you would build:

1. The bank charges the card and the reply is lost.
2. Two retries arrive at two machines four milliseconds apart.
3. A client sends the same key with a different amount.
4. A mobile app replays a queued request 30 hours later.
5. A consumer processes a message and crashes before committing its offset.
6. The dedup store returns "not found" from a stale replica.
7. The retry succeeds, but the first attempt also completes ten seconds later.

Two of the seven are not fixed by an idempotency key at all. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Design autocomplete for a search box.*
   Trie plus prefix walk, the traversal version with its cost, the number that makes you change it, the
   precomputed top-`k` with its memory arithmetic, and the offline rebuild — offered before the interviewer
   asks about deletion.

2. *The payment request timed out. Is it safe to retry?*
   Not as it stands, and say why: three indistinguishable cases, one of which already took the money. Then
   the idempotency key, insert-before-work with a unique constraint, the three branches including
   `IN_PROGRESS`, and the retention window as a number.

3. *How do you guarantee exactly-once processing?*
   Reject the premise in one sentence, give the reason — the last message can always be lost — then
   at-least-once plus idempotent handlers, what Kafka actually promises, and the one case that is genuinely
   exactly-once because only one store is involved.

---

## Before you move on

- [ ] I can walk to a prefix and gather every completion below it.
- [ ] I can state the tie rule without hesitating.
- [ ] I know `_collect` must check the node it starts on.
- [ ] I know what `so_far` is for and what breaks without it.
- [ ] I can give the cost of the traversal version with every term named.
- [ ] I can say why the first keystroke is the expensive one.
- [ ] I can write `_offer` from memory, including the removal line.
- [ ] I know which nodes an insert must update, and why no others.
- [ ] I can size the memory of the precomputed version out loud.
- [ ] I know the precomputed list is a cache, and deletion is invalidation.
- [ ] I can name the three answers to deletion, and which one production uses.
- [ ] I know what an empty prefix should return.
- [ ] I rewrote `_collect` without recursion.
- [ ] I can define idempotent and give one example of each kind.
- [ ] I can name the three cases a timeout hides.
- [ ] I know the key is the client's, generated once, reused on retries.
- [ ] I can state the insert-before-work order and say what breaks if reversed.
- [ ] I know what the unique constraint is doing for me.
- [ ] I know what to return for a request still in flight.
- [ ] I can say in two sentences why exactly-once delivery is impossible.
- [ ] I can say what Kafka's transactions guarantee, and where that stops.
- [ ] I can name four ways to make an operation naturally idempotent.
- [ ] I can compute the daily cost of double charges from a timeout rate.
- [ ] I can size a dedup store per day at a given volume.
- [ ] I know why the dedup store must be strongly consistent.
- [ ] I know which way I fail when the dedup store is down, and why.
- [ ] I can name two things idempotency does not protect.
- [ ] I answered all three questions above out loud.
