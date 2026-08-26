---
day: 14
track: practice
title: "Practice — Max, min, second largest: the single-pass habit"
status: written
---

# Day 014 · Practice

**DSA topic:** Max, min, second largest: the single-pass habit
**System design topic:** Fundamentals revision and interview questions

---

## Code these, in this order

Four problems that all have a one-line sorting solution and a better one-pass solution. Write
the sorting version first if it helps you see the answer — then delete it and write the pass.

Before each one, say out loud:

1. How many trackers do I need, and what does each one hold?
2. What do they start as? (Never `0`.)
3. Does "largest" here mean by position or by distinct value?
4. What happens on an empty input, and on a one-element input?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Maximum Product of Two Elements in an Array | LeetCode 1464 (Easy) | The two largest, in one pass. The sorting answer is one line; write the two-tracker version and see that it is barely longer. |
| 2 | Third Maximum Number | LeetCode 414 (Easy) | Three trackers, **and** the distinct-value contract — the statement says third *distinct* maximum, and if there isn't one you return the maximum instead. Read it twice. |
| 3 | Maximum Product of Three Numbers | LeetCode 628 (Medium) | Five trackers: the three largest **and the two smallest**. Two large negatives multiply to a large positive, which is the whole trap. |
| 4 | Kth Largest Element in an Array | LeetCode 215 (Medium) | Where trackers stop working. Solve it three ways — sort, min-heap of size k, quickselect — and be able to say when each is the right choice. |

### On problem 2, do this properly

- Write it with three trackers before looking at any solution.
- Then test it on `[2, 2, 3, 1]`, `[1, 2]`, `[1, 1, 1]` and `[5, 2, 4, 1, 3, 6, 0]`.
- Then answer: which of those four inputs breaks a version that forgets `x != first`?
- Then answer: which of them breaks a version that has no third branch at all?

### On problem 3, notice the negatives

`[-10, -10, 1, 3, 2]` has answer 300, not 6. Say why out loud before coding. Then decide how
many trackers that means, and write them.

The lazy version — `sorted(nums)` then compare `nums[-1]*nums[-2]*nums[-3]` against
`nums[0]*nums[1]*nums[-1]` — is correct and `O(n log n)`. Write it, then write the `O(n)`
five-tracker version, then say which you would ship and why. (There is a real answer: for a
small `n` the sorted version is clearer and fast enough; for a stream it is impossible.)

### On problem 4, do all three

- **Sort and index**: `O(n log n)`, two lines. Always correct, sometimes right.
- **Min-heap of size k**: push each element, pop when the heap exceeds `k`. `O(n log k)` time,
  `O(k)` space. Best when `k` is small and `n` is huge, or when the data is a stream.
- **Quickselect**: partition around a pivot, recurse into one side only. `O(n)` average,
  `O(n²)` worst case unless you randomise the pivot.

Then say out loud which one you would use if `k = 3` and `n = 10⁹` arriving over a network, and
why the other two are not options.

### The contract drill

For each phrase, say what you would ask the interviewer before writing any code:

1. "Find the second largest element."
2. "Find the second highest salary."
3. "Find the top three scores."
4. "Find the largest and smallest in one pass."

Every one of them has an ambiguity. Name it in under five seconds.

### The bug drill

Predict the output of each, then run them:

```python
def largest(items):
    best = 0
    for x in items:
        if x > best:
            best = x
    return best

print(largest([-7, -2, -9]))
```

```python
def second(items):
    first = second_ = float("-inf")
    for x in items:
        if x > first:
            first = x
            second_ = first
    return second_

print(second([3, 9, 1, 7]))
```

```python
def second(items):
    first = second_ = float("-inf")
    for x in items:
        if x > first:
            first, second_ = x, first
    return second_

print(second([10, 1, 2]))
print(second([1, 2, 10]))
```

For the third one, explain in a sentence why the two calls disagree, and why that makes the bug
so hard to catch by testing.

### The fundamentals drill

This is the real work of today. Ten questions, and the rule is: **say the whole answer out loud
before you read anything.** Being wrong out loud is the exercise.

1. What happens when you type google.com and press Enter?
2. What is the difference between a client and a server?
3. How does the browser find the server for google.com?
4. TCP or UDP for a live video call, and why?
5. Describe an HTTP request. What is in the headers, what is in the body?
6. What does HTTPS protect you from, and what does it not?
7. What happens inside the server between the request arriving and the response leaving?
8. What is the difference between a process and a thread?
9. How much slower is a disk read than a memory read?
10. How does your code end up running on a server, and what is a container?

Mark each one **said it / knew it but could not say it / did not know it**. Only the first
category counts. Anything in the other two goes on tomorrow's list, not today's — a question
you failed at yesterday is worth several you got right ten minutes ago.

### The numbers drill

Produce these from memory, in under a minute, with no looking:

- The five levels of the latency ladder, in order, with an order of magnitude each.
- The port numbers for HTTP, HTTPS, SSH, Postgres and Redis.
- What 401, 403, 404, 429, 502 and 504 each mean.
- How many round trips happen before the first byte of your request is sent on a cold HTTPS
  connection, and what each one is for.
- 50 million daily users × 20 requests each — what is that in requests per second, average and
  peak?

### The one to draw

Draw the days 1–13 journey — name, address, connection, request, process, operating system,
hardware, and back — in whatever tool you like, from memory, with no notes open. Then check it
against §4 and mark what you left out. What you leave out twice is what to revise.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the second largest element without sorting.*
   Ask the `[5, 5, 3]` question first. Then give the two branches, name why the old best has to
   slide down, and finish with `O(n)` time and `O(1)` space.

2. *Pick any topic from days 1 to 13 and answer it with no preparation.*
   Have someone pick, or pick at random. Use the three-part shape: one-sentence answer, then the
   mechanism, then the trade-off. Ninety seconds, then stop.

3. *How much slower is a disk read than a memory read, and what does that mean for a system you
   are designing?*
   Give the ratio, then the ladder, then one design consequence — why a cache hit is worth
   three orders of magnitude, and why one extra network hop can cost more than any amount of
   code tuning.

---

## Before you move on

- [ ] I ask what "second largest" means before writing a line of code.
- [ ] I never initialise a tracker to `0`, and I can say what happens if I do.
- [ ] I write `first, second = x, first` as one statement, and I know why.
- [ ] I test every second-largest solution with the largest element **first** in the list.
- [ ] I can say all ten fundamentals answers out loud, in ninety seconds each, with no notes.
- [ ] I can produce the latency ladder and the round-trip count from memory.
