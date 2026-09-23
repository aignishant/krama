---
day: 87
track: practice
title: "Practice — Recursion: the leap of faith"
status: written
---

# Day 087 · Practice

**DSA topic:** Recursion: the leap of faith
**System design topic:** Design a food delivery order flow

---

## Code these, in this order

One rule for the whole set: **answer the three questions out loud before typing.** What is the smallest
input I can answer without asking anybody? What is a smaller version of the same problem? What one step
turns that answer into mine? If you cannot say all three, you are not ready to write the function.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Fibonacci Number | LeetCode 509 (Easy) | The classic, and whether you notice it is exponential before being told. |
| 2 | Reverse String | LeetCode 344 (Easy) | Recursion with two indices instead of slicing, in O(1) extra space. |
| 3 | Pow(x, n) | LeetCode 50 (Medium) | Halving instead of decrementing, negative exponents, and calling the recursion **once**. |
| 4 | Merge Two Sorted Lists | LeetCode 21 (Easy) | You solved this iteratively on day 084. Now do it recursively and compare the two. |

### On problem 1, measure before you optimise

Write the naive version. Time `fib(30)`, then `fib(32)`, then `fib(34)`. Write the three numbers down
and say what the ratio between them tells you. Then add `@cache` and time `fib(100)`.

### On problem 2, do not slice

The obvious recursive reverse allocates a new string per call. Write it with two indices moving toward
each other instead, and say what you changed the complexity from and to.

### On problem 3, count your recursive calls

Write the version that calls `fast_power` twice for the even case. Time it against the version that
calls it once and stores the result. Explain the difference in one sentence about branching.

### On problem 4, compare honestly

Write both. Say which you would ship and why, in terms of stack depth on a hundred-thousand-node list.

---

### The three-questions drill

For each, state the base case, the smaller problem and the one step — out loud, before coding:

1. Sum a list of numbers.
2. Count the nodes in a linked list.
3. Reverse a string.
4. Raise a number to a power.
5. Check whether a string is a palindrome.
6. Find the maximum of a list.
7. Count the digits in a positive integer.
8. Flatten a nested list of lists.

Two of the eight have a base case that is *not* "empty". Name them.

### The leap-of-faith drill

1. Write `total` and then, without running it, say why it is correct — using the three checks rather
   than a trace.
2. Try to trace `total([1,2,3,4])` four levels deep in your head. Notice how it feels.
3. State the three conditions that replace tracing.
4. Say, in one sentence, what treating the recursive call as a library function buys you.

### The base-case drill

1. Write a function with no base case. Quote the error.
2. Write one whose base case is present but unreachable — step by two towards `== 0`. Quote the error
   and say why it is harder to diagnose.
3. Fix it two ways: by changing the guard, and by changing the step. Say which is the real fix.
4. State both halves of the termination condition in one sentence.

### The one-call-versus-two drill

1. Draw the call tree for `total([1,2,3])`.
2. Draw the call tree for `fib(5)`.
3. Count the nodes in each.
4. State the complexity of each and say what in the *body* predicts it.
5. Give a third example of each kind.

### The break-it drill

Trigger each and record the exact output or error text:

1. Omit the base case.
2. Put the base case *after* the recursive call.
3. Forget to `return` the recursive call. Quote the error one level up.
4. Slice in the recursive call and time it at n = 2000 against the index version.
5. Call the recursion twice in `fast_power`'s even branch and time it.
6. Use a mutable default argument and call the function twice.
7. Run a depth-5000 recursion. Quote the error.
8. Raise the recursion limit to a million and run it again. Describe what happens.

### The cost drill

1. State the time complexity of `total`, `power`, `fast_power` and `fib`, and where each comes from.
2. State the *space* of each, and explain why `fib` is O(n) space despite 2ⁿ calls.
3. Quote Python's recursion limit and the input size at which a linear-depth recursion dies.
4. Say why `sys.setrecursionlimit` is not a fix.
5. Give the rule about log-depth versus linear-depth recursion in one sentence.

### The conversion drill

1. Write `total` as a loop.
2. Write `fib` as a loop.
3. Write binary search as a loop.
4. For each, say whether the loop is better and why.
5. Say when you would choose recursion, and give two problems where the loop version is clearly worse.

---

### The actors drill

1. List the eight order states.
2. For each transition, name the actor.
3. For each transition where the actor is not the platform, give a timeout and what happens when it
   fires.
4. Say which transitions have no timeout and defend each one.
5. State the general rule in one sentence.

### The timeout drill

1. Compute the auto-cancellations per day at 2M orders and a 5 percent no-response rate.
2. Say what must happen on each one — list four things.
3. Say why a metric is one of them.
4. Describe the sweeper: the query, the batch, and the clause that lets several run at once.
5. Say what you would alert on, and why that alert matters more than most.
6. Say why lazy expiry works for a cinema seat and not here.

### The snapshot drill

1. Write `OrderItem` and mark the fields that are copies rather than references.
2. Say what goes wrong without the snapshot, concretely.
3. Compute the orders per day touching a changed menu item.
4. Say why the subtotal, delivery fee and tax are stored separately from the total.
5. Name two other lessons in this course with the same immutability rule.

### The cancellation drill

For each, say whether cancellation is allowed, the refund, and the reason in the customer's language:

1. Customer, order placed, restaurant has not responded.
2. Customer, order accepted, food not started.
3. Customer, food being prepared.
4. Customer, partner has collected the food.
5. Restaurant, after accepting.
6. System, after ninety seconds with no restaurant response.

Say what shape this logic takes in code, and why it is not a boolean on the order.

### The assignment drill

1. State the three options for when to assign a partner.
2. Compute the wasted partner-hours per day for the earliest option.
3. State the cost of the latest option in minutes per order.
4. State the middle option as a formula.
5. Say what that formula turns the problem into, and why you would name it as a separate system.

### The estimation drill

Compute each, showing the multiplication:

1. Peak orders per second, given 40 percent of 2M orders in two hours.
2. State transitions per day and per second at peak.
3. Storage per day for orders, items and transitions.
4. The fraction of storage that is transition history, and what you would do about it.
5. The annual support cost of not snapshotting prices.

### The pattern-choice drill

1. Say why this design uses a transition table and an enum rather than a class per state.
2. Say what would make you switch to classes.
3. Name the lesson where a class per state was the right answer, and what was different there.
4. State the general gate in one sentence.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Solve this recursively. What is the base case?*
   The three questions answered in order before any code, the leap of faith named, the base case
   written first, both halves of termination, the index-not-slice point, and both complexities with the
   stack limit stated as a real limit.

2. *Design the order flow for a food delivery app.*
   Ask the restaurant-timeout question first, the states with an actor on every arrow, the timeout
   column with the hundred-thousand-a-day number, one sweeper with a rules table, the price snapshot
   with its dispute arithmetic, cancellation as a question asked of the state, and the assignment trade
   with both costs.

3. *Write Fibonacci recursively. What is its complexity?*
   Two recursive calls per level so about 2ⁿ, the measured numbers, memoisation turning 331 million
   calls into 41, the loop as what you would ship, and the general rule about counting calls in the
   body.

---

## Before you move on

- [ ] I answer the three questions out loud before writing any recursive function.
- [ ] I can state the three checks that replace tracing.
- [ ] I write the base case first, at the top, every time.
- [ ] I can state both halves of the termination condition.
- [ ] I built an unreachable base case on purpose and can say why it is the harder bug.
- [ ] I can predict a recursion's complexity by counting the calls in the body.
- [ ] I timed `fib(30)`, `fib(32)` and `fib(34)` and can say what the ratio means.
- [ ] I added `@cache` and can say what it changed and what it is the foundation of.
- [ ] I never slice in a recursive call, and I can say what it costs.
- [ ] I can quote the recursion limit and the input size where it bites.
- [ ] I can say why raising the limit is not a fix.
- [ ] I can name every actor on every order transition.
- [ ] I can give the auto-cancellation number and the four things that must happen.
- [ ] I can describe the sweeper, including the clause that lets several run at once.
- [ ] I can explain the price snapshot with its arithmetic.
- [ ] I can give all three partner-assignment options with their costs.
- [ ] I answered all three questions above out loud.
