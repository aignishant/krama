---
day: 76
track: practice
title: "Practice — LRU cache: the structure interviewers love"
status: written
---

# Day 076 · Practice

**DSA topic:** LRU cache: the structure interviewers love
**System design topic:** Design patterns revision and interview questions

---

## Code these, in this order

One rule for the whole set: **before writing a line, say which structure answers which question.**
"The map answers *where is it*; the list answers *which is oldest*." If you cannot say that sentence,
you will merge the two and lose an hour.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Design HashMap | LeetCode 706 (Easy) | Buckets and chaining, so that "the map is O(1)" is something you have built rather than assumed. |
| 2 | LRU Cache | LeetCode 146 (Medium) | Today's problem. Two structures, sentinels, and the fact that `get` is a write. |
| 3 | Design Browser History | LeetCode 1472 (Medium) | The same doubly linked list, with a cursor instead of an eviction rule. |
| 4 | LFU Cache | LeetCode 460 (Hard) | A third structure and a `min_frequency` counter, and why it stays O(1). |

### On problem 2, write the sentinels first

Do not write `get` or `put` until the fake head and tail exist and `_unlink` and `_push_front` are
both four lines with no `if` in them. If either helper needs a null check, the sentinels are wrong.

### On problem 3, notice what changed

Browser history is a doubly linked list with no map and no eviction — the cursor moves rather than
the nodes. Say in one sentence what problem 2 needed a hash map for, and why this one does not.

### On problem 4, find the O(1) argument

The hard part is not the code, it is why `min_frequency` can be maintained in constant time. Say out
loud: when does it increase, when does it reset, and why can it only ever increase by exactly one.

---

### The why-two-structures drill

Answer each without looking:

1. What does a hash map alone fail at, and what is the cost of patching it?
2. What does a list alone fail at, and what are the two separate costs?
3. What exactly does the map map to, and why not to the value?
4. Why must the list be doubly linked? Give the two-assignment answer.
5. What would you have to do if you were forced to use a singly linked list?
6. Which end holds the most recently used, and which operations touch each end?

### The get-is-a-write drill

1. Implement `get` without the reordering.
2. Run `put(1,1); put(2,2); get(1); put(3,3); get(2)` on both versions. Write both outputs.
3. Say why the broken version returns correct *values* from every `get`.
4. Say what the symptom looks like in production rather than in a test.
5. Write the shortest test that distinguishes the two.

### The both-structures drill

1. Delete the `del self._map[oldest.key]` line.
2. Run 2,000 random operations and print `len(self._map)` at the end. Say what has happened.
3. Then `get` an evicted key and print `keys_most_recent_first()`. Describe the corruption.
4. Now remove the key field from `Node` and try to write the eviction. Say what you would be forced
   to do instead and what it costs.

### The break-it drill

Trigger each and record the output or the exact error text:

1. Remove the sentinels and write `_unlink` with null checks. Count the branches you needed.
2. Then run it on a cache holding exactly one node and quote the error you get when you forget one.
3. Treat an existing key as a new insert in `put`. Run `put(1,1); put(1,2); put(2,2); put(3,3)` with
   capacity 2 and describe the state of both structures.
4. In `_push_front`, set `self._head.next = node` first. Say what you lose.
5. Set capacity to 0 with no guard. Trace what `put` does.
6. Set capacity to 1 and run `put(1,1); put(2,2); get(1)`. State the expected answer.

### The cost drill

1. Count the pointer writes in `get` and in `put`. State both.
2. State the space complexity, and say why it is not O(n).
3. Compute the per-entry memory with and without `__slots__`, and the total for 100,000 entries.
4. Compute the average read time at a 90 percent hit rate with a 1 µs cache and a 100 µs database.
   Then at 50 percent. State both speed-ups.
5. Say which single number you would measure before increasing the capacity.

### The follow-ups drill

Answer each in three sentences:

1. Why does the node store the key?
2. Why not a singly linked list?
3. Is `get` a mutation?
4. Is this thread-safe, and what are the two fixes?
5. How would you make it LFU?
6. What would you use in production, and how does Redis differ from this?

---

### The axis-of-change drill

For each prompt, say the axis of change in four words or fewer, then the pattern, then the cost, then
the condition under which you would use no pattern:

1. Nine payment providers in one `if` chain.
2. An order that moves through six stages with different rules at each.
3. Five things that must happen when a user signs up.
4. Three report formats sharing a fixed four-step pipeline.
5. A legacy library whose method names are wrong for your codebase.
6. A settings object with eighteen optional fields, three of which are mutually exclusive.
7. Expense approval with limits at four levels.
8. An action the user must be able to undo.
9. Retry, logging and metrics that should wrap any of several senders.
10. A very large query result returned from an API.

Two of the ten are the same pattern for different reasons. Say which and why.

### The look-alike drill

Give the one-sentence distinguisher for each pair, then write six lines of code where the difference
is visible:

1. Strategy and State.
2. Strategy and Template Method.
3. Decorator and Proxy.
4. Decorator and Adapter.
5. Adapter and Facade.
6. Observer and Chain of Responsibility.
7. Command and Strategy.
8. Factory and Builder.

For pair 3, write the version where the two are genuinely indistinguishable and say what decides it.

### The no-pattern drill

For each, say whether you would use a pattern, and give the deciding question:

1. Two tax rates that differ only by a number.
2. Two tax rules with genuinely different shapes.
3. Seven weekdays with different opening hours.
4. Three log destinations, with a fourth expected next quarter.
5. The first time a second variation has appeared.
6. Four suits in a deck of cards.
7. A retry policy each customer configures for themselves.
8. Three subclasses that share ten lines.

Three of the eight are "no" for the same reason. Name it in one sentence.

### The Python drill

Write both versions and count the lines:

1. Strategy as classes, and as a dictionary of functions.
2. Command without undo as a class, and as `functools.partial`.
3. Singleton as a class with `__new__`, and as a module.
4. Iterator as two classes, and as a generator.
5. Decorator as a wrapper class, and with the `@` syntax.

Then say, for each, what the class version buys that the short version does not — and be honest when
the answer is "nothing".

### The regret drill

Prepare a real answer to *"tell me about a pattern you introduced and later removed"*. Write it out
in five sentences: what you built, why it seemed right, what the actual variation turned out to be,
what the removal diff looked like, and what test you now apply instead. If you have no real example
yet, build one deliberately this week — introduce Strategy for two things that differ only by a
constant, live with it for a day, and remove it.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Design an LRU cache with O(1) get and put.*
   The O(1)-eviction requirement that forces two structures, each single structure rejected with its
   cost, the map pointing into the doubly linked list, why doubly, `get` is a write, the key stored on
   the node, sentinels as a deliberate decision, and the space bound with a number.

2. *Which pattern fits here, and what would you lose by using it?*
   The axis of change named before any pattern, the check for a second axis, the naive version and
   what specifically breaks, the pattern with what it makes flat rather than cheap, the cost in hops
   and in run-time failure, and the condition that would make you write the `if` instead.

3. *How is that different from Strategy?*
   State, Template Method, Command and Decorator, one sentence each, plus the line of code in which
   the difference is visible.

---

## Before you move on

- [ ] I can say which structure answers which question, in one sentence.
- [ ] I can give the two-assignment reason for the list being doubly linked.
- [ ] I wrote the sentinels first and neither helper contains an `if`.
- [ ] I broke `get` so it does not reorder and saw the eviction go wrong while values stayed right.
- [ ] I deleted the map removal and watched both structures disagree.
- [ ] I can explain why the node stores its own key.
- [ ] I tested capacity 0 and capacity 1.
- [ ] I can quote the per-entry memory and the total for 100,000 entries.
- [ ] I can give the hit-rate arithmetic for 90 percent and 50 percent.
- [ ] I can answer "is it thread-safe" with both fixes.
- [ ] I named the axis of change before the pattern on all ten prompts.
- [ ] I can give all eight look-alike distinguishers without hesitating.
- [ ] I can say the break-even numbers and the rule of three.
- [ ] I can name three patterns I have already used without knowing it.
- [ ] I have a real answer ready for "a pattern you removed".
- [ ] I answered all three questions above out loud.
