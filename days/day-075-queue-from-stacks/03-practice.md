---
day: 75
track: practice
title: "Practice — A queue from two stacks, and a stack from queues"
status: written
---

# Day 075 · Practice

**DSA topic:** A queue from two stacks, and a stack from queues
**System design topic:** Template method and iterator

---

## Code these, in this order

One rule for the whole set: **never say "O(1)" without saying which kind.** Worst case for one call,
or amortised across a sequence. If you cannot say which you mean, you do not yet know the answer.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Implement Stack using Queues | LeetCode 225 (Easy) | Choosing which operation pays, and noticing there is no amortised saving here. |
| 2 | Implement Queue using Stacks | LeetCode 232 (Easy) | The pour-only-when-empty rule, and the amortised argument on demand. |
| 3 | Design Front Middle Back Queue | LeetCode 1670 (Medium) | Two deques kept balanced — the same "two containers, one invariant" habit. |
| 4 | Max Stack | LeetCode 716 (Hard) | Two structures cooperating under one interface, and the honest cost of the expensive operation. |

### On problem 1, do both versions

Write costly-push-with-one-queue, then cheap-push-with-two-queues. Say which you would submit and
why, and then say what the total cost of n pushes is in each. Neither answer is "amortised O(1)", and
being able to say *why not* is the point of the exercise.

### On problem 2, write the test that finds the bug

Do not test by enqueuing everything and then dequeuing everything — that sequence passes even with
the pour rule broken. Write the interleaved test: `enqueue 1, enqueue 2, dequeue, enqueue 3,
dequeue`. Then write the random-sequence check against a real `deque` and run it two thousand times.

### On problem 3, name the invariant before coding

Two deques, front half and back half. Say out loud what must be true after every operation — the
sizes differ by at most one — and where you have to rebalance. Then write it.

### On problem 4, be honest about the cost

There is a version with O(1) push and O(n) `pop_max`, and a much harder one with a doubly linked list
and a sorted structure. Write the simple one, state its costs plainly, and say what you would need to
make `pop_max` logarithmic.

---

### The amortised drill

Say each answer out loud, five times:

1. What is the cost of a single `dequeue` in the worst case?
2. What is the cost amortised, and what does "amortised" mean in one sentence?
3. Count the operations one element experiences across its entire life. Say the number.
4. What single fact makes that count a bound rather than a hope?
5. What is the difference between amortised and average-case?
6. Give one situation where amortised O(1) is not good enough, and say what you would use instead.

### The pour-rule drill

1. Write the sequence that breaks a queue whose `_pour` has no emptiness guard. Say what it returns
   and what it should return.
2. Say why no exception is raised.
3. Explain, in terms of the pile on Basava's counter, what has physically gone wrong.
4. Write the invariant sentence: what does `outbox` hold, what does `inbox` hold, and how do you read
   the whole queue front to back?

### The break-it drill

Trigger each and record the actual output or error:

1. Remove the `if not self._outbox` guard from `_pour`. Run the interleaved sequence.
2. Write `is_empty` as `not self._outbox` and loop `while not q.is_empty()`. Count what you lose.
3. Write `peek` without calling `_pour`. Run `enqueue(1); peek()` and quote the error.
4. In the one-queue stack, rotate `len(queue)` times instead of `len(queue) - 1`. Push 1 and 2, then
   pop. Say what structure you accidentally built.
5. In the two-queue stack, reallocate the spare queue instead of swapping. Say what it costs at ten
   thousand pops.
6. Pour on every dequeue unconditionally. Say both things that are now wrong — the correctness and
   the complexity.

### The counting drill

1. For n enqueues followed by n dequeues, count every push and pop. State the total.
2. For n alternating enqueue/dequeue pairs, count the same. State the total.
3. For n pushes into the one-queue stack, count the rotations. State the total and the complexity.
4. Say in one sentence why the queue-from-stacks gets an amortised saving and the stack-from-queues
   does not.
5. At n = 10,000, quote both totals.

### The recognition drill

For each, say whether the amortised argument applies, and give the one-way fact that makes it work
if it does:

1. `list.append` in Python.
2. `dequeue` in the two-stack queue.
3. The `while` loop inside a monotonic stack.
4. `push` in the one-queue stack.
5. Rehashing a dictionary when the load factor is exceeded.
6. The pour in a queue that pours unconditionally.
7. Popping from a monotonic deque.

Two of the seven have no amortised saving. Name them and say what they have in common.

---

### The template-method refactor drill

You have three report classes of roughly 120 lines each, about 96 lines of which are near-identical.

1. List the steps and mark each one fixed or varying.
2. Write the template method. Say which method must never be overridden and how you would enforce it
   in Java, in C#, and in Python.
3. Write the two abstract steps with `@abstractmethod`. Then instantiate a subclass that forgets one
   and quote the exact error.
4. Add one hook. Say what makes it a hook rather than an abstract step.
5. Add a fourth report. Count the lines.
6. Now suppose delivery must also vary — email, S3, SFTP. Draw what happens to the hierarchy, count
   the classes, and say what you would switch to.

### The Hollywood drill

For each, name what the framework calls and what you write:

1. `unittest.TestCase`
2. Django's `ListView`
3. A servlet's `doGet`
4. Spring's `JdbcTemplate`
5. An Airflow operator
6. An Android `Activity`

Then say the one sentence that describes what all six have in common, and what it means for who owns
the control flow.

### The iterator drill

1. Write `Countdown` as two classes — the collection and the position. Loop over one instance twice
   and confirm both loops work.
2. Merge them into one class so `__iter__` returns `self`. Loop twice. Say what the second loop
   produces and why.
3. Rewrite the whole thing as a four-line generator.
4. Write a generator that pages a table with keyset pagination.
5. Iterate it once to count and again to sum. Write down the second number and explain it.
6. Add a type hint that would have warned the caller.

### The memory drill

1. Compute the memory for 10 million rows at 200 bytes, loaded into a list.
2. Compute it for pages of 1,000. State the ratio.
3. Say what the failure looks like in a 512 MB container, including what appears in the application
   log.
4. Compute the total row reads to page through 10 million rows with `OFFSET` at 1,000 per page.
5. Compute it with keyset pagination.
6. State the ratio and say why the code change is almost nothing.

### The which-pattern drill

For each, say template method, strategy, iterator, or none:

1. Three reports differing only in grouping and rendering.
2. A pricing rule that differs by country and is chosen at run time.
3. Walking a directory tree without loading it all.
4. `setUp` running before every test.
5. Returning a very large query result from an API.
6. Three sorting orders the caller picks between.
7. A fixed six-step onboarding flow where step four differs by customer type.

Two of the seven are strategy, and the deciding question is the same for both. Say it.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Implement a queue using only stacks. What is the amortised cost?*
   The reversal trick, the two roles, the pour-only-when-empty rule stated as a rule with the failing
   sequence, both complexities given before being asked, the four-touches count with the never-goes-
   backwards fact, and the amortised-versus-average distinction.

2. *Three report types share 80 percent of their logic. Structure it.*
   The steps split into fixed and varying first, the template that owns the order, abstract steps
   versus hooks, the edit-count argument rather than the line-count argument, the iterator change for
   memory with both numbers, and the named condition under which you would abandon inheritance for
   composition.

3. *Pop can move n elements. How is that O(1)?*
   The count over an element's whole life, the one-way fact, the concrete thousand-element example,
   and the honest caveat about p99 latency.

---

## Before you move on

- [ ] I can state the reversal trick in one sentence.
- [ ] I can say the pour rule and the exact sequence that breaks without it.
- [ ] I wrote the interleaved test and the random-sequence check against a real queue.
- [ ] I can give the four-touches count without hesitating.
- [ ] I can define amortised without using the word "average".
- [ ] I can name a situation where amortised O(1) is not good enough.
- [ ] I wrote both stack-from-queue versions and can say the total cost of n pushes.
- [ ] I can say why the amortised saving does not transfer to the stack-from-queues.
- [ ] I made `is_empty` check one stack and saw the queue lose its contents.
- [ ] I split the report steps into fixed and varying before naming any pattern.
- [ ] I quoted the `TypeError` from forgetting an abstract method.
- [ ] I can say the difference between a hook and an abstract step.
- [ ] I can give the edit-count argument, not just the line-count one.
- [ ] I wrote a one-shot generator bug and saw the second pass return zero.
- [ ] I can quote 2 GB against 200 KB, and 5 × 10¹⁰ against 10⁷ row reads.
- [ ] I can name the condition that would make me abandon the template for composition.
- [ ] I answered all three questions above out loud.
