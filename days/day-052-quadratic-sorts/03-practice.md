---
day: 52
track: practice
title: "Practice — Bubble, selection and insertion sort, and what each one teaches"
status: written
---

# Day 052 · Practice

**DSA topic:** Bubble, selection and insertion sort, and what each one teaches
**System design topic:** Common object-oriented interview questions

**Theme:** Logging that helps at 3am

---

## Code these, in this order

One rule for the whole set: **write the sort from memory before you look at anything.** All three are
under ten lines, and the only way to know you have them is to produce them cold.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Sort an Array | LeetCode 912 (Medium) | Whether your hand-written sort survives 50,000 elements — insertion sort will time out, and noticing that is the point. |
| 2 | Insertion Sort List | LeetCode 147 (Medium) | The insertion idea without the ability to shift — you have to relink instead. |
| 3 | Sort Colors | LeetCode 75 (Medium) | That a selection-sort instinct is wrong here, and one pass with three regions is right. |
| 4 | Height Checker | LeetCode 1051 (Easy) | Counting how far the input is from sorted — the exact quantity insertion sort is sensitive to. |

### On problem 1, submit the slow one first

Write `insertion_sort` and submit it. Read the verdict:

```
Time Limit Exceeded
```

Then submit `sorted(nums)`. Say out loud what changed: `n²` at n = 50,000 is 1,250,000,000
comparisons; `n log n` is about 800,000. That is the difference between a timeout and forty
milliseconds, and it is the reason you call a library sort for real data.

### On problem 2, notice what you cannot do

A linked list has no shifting. You cannot move everything one place right to open a gap, because
there is no "one place right" — you can only relink. So the insertion walk becomes: find the last
node whose value is not greater, then point around. Say out loud which property of insertion sort
survives that change (it still grows a sorted prefix) and which does not (it can no longer walk
*backwards*, so you scan forward from the head each time).

### On problem 3, resist selection sort

Sort Colors is three distinct values. The selection-sort instinct — find all the zeros, then all the
ones — is two passes and `O(n)` but it is not what the problem wants. Write the counting version
first, then the one-pass Dutch-flag version with three regions, and say which of the two you would
offer in an interview and why.

### On problem 4, connect it to the cost

Height Checker asks how many positions differ between the input and its sorted version. Solve it,
then answer this: is that number the same as the number of shifts insertion sort would perform? Run
the shift counter from §5 of the lesson on the same input and find out. It is not the same, and being
able to say why — one counts *misplaced elements*, the other counts *inversions* — is a genuinely
good answer to "how nearly sorted is nearly sorted".

### The write-from-memory drill

Set a timer. Two minutes each, no reference, and the code must run:

1. `bubble_sort`, with the early-stop flag and the shrinking inner range.
2. `selection_sort`, tracking the position of the smallest.
3. `insertion_sort`, with the guard condition in the right order.

Then, for each one you wrote, answer without looking: what is the best case, what is the worst case,
how many swaps, and is it stable?

### The break-it drill

Introduce each bug on purpose, run it, and read the output:

1. In bubble sort, change the inner range to `range(len(nums))`. Paste the exact error.
2. In insertion sort, swap the two conditions to `while nums[i] > value and i >= 0`. Run it on
   `[2, 3, 1]`. What comes out, and why is there no error?
3. In insertion sort, change `>` to `>=`. Sort `[("a", 2), ("b", 1), ("c", 2)]` by the number and say
   what changed about `a` and `c`.
4. In selection sort, write `smallest = nums[i]` instead of `smallest = i`. Run it on `[5, 1, 4]`,
   then on `[2, 0, 1]`, and explain why one raises and one does not.
5. Remove the `swapped` flag from bubble sort. What is the best case now?

### The adaptive drill

Count shifts with the counter from the lesson, and say the number before you run it:

1. `list(range(1000))` — already sorted.
2. `list(range(1000, 0, -1))` — exactly reversed.
3. `list(range(1000))` with elements 100 and 103 swapped.
4. `list(range(1000))` with the last element moved to the front.
5. A list of 1,000 identical values.

Then say which of those five is the case that makes insertion sort worth using in production, and
which one is the case people wrongly assume is fast.

### The arithmetic drill

Answer with numbers, in under ten seconds each:

1. Comparisons for selection sort at n = 1,000.
2. Element writes for selection sort at n = 1,000.
3. Element writes for bubble sort on reversed input at n = 1,000.
4. Comparisons for insertion sort on already-sorted input at n = 1,000.
5. Roughly where the crossover with merge sort sits, and what Python's Timsort uses.

### The rapid-fire drill

Twelve questions, forty-five seconds each, answered out loud in three beats — definition, situation,
cost. Time yourself, and stop when the third beat is done:

1. What are the four pillars of OOP?
2. Abstract class or interface — which and why?
3. Encapsulation or abstraction — what is the difference?
4. Overloading or overriding? Does Python have both?
5. Composition or inheritance? Give the numbers.
6. What is polymorphism? Give an example from your own code.
7. `==` or `is`?
8. If I define `__eq__`, what else must I define, and why?
9. Static method, class method, or instance method?
10. What is the diamond problem, and how does Python answer it?
11. Shallow copy or deep copy?
12. Can you have an abstract class with no abstract methods? Should you?

Mark yourself out of three on each. Anything scoring one is a definition with nothing behind it.

### The Python-mechanics drill

Run each, then explain the output before you read it:

1. Define a class with two methods of the same name and call the first one.
2. Subclass an `ABC` without implementing an abstract method, then construct it. Paste the error.
3. Write a class that satisfies a `Protocol` without importing it, and type-check it.
4. Build the A/B/C/D diamond and print `D.__mro__`. Explain why `super()` inside `B` reaches `C`.
5. `@dataclass(eq=True)` without `frozen=True`, then call `hash()` on an instance. Paste the error.
6. `copy.copy` a dict containing a list, mutate the inner list, and print both.

---

## Build these, in all three languages

*Three exercises, easiest first. Each one says what it is really testing. Every
exercise is done three times: once in Python, once in Go, once in C++.*

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | One request, one grep | Whether every line of one request carries the same id, three calls deep, with no id parameter anywhere. |
| 2 | The secret scan | Turning "never log a password" into a check you can run, not a rule you remember. |
| 3 | Wire it into the server | Replacing the day 49 print-style log line with the structured logger, request id and all. |

All three start from the lesson's program. Keep the output as JSON lines; the point of every
exercise is that a machine can read them.

### 1. One request, one grep

Add a third function under `create_user`, `send_welcome(user_id)`, that logs one `info` line and
is called by `create_user`. Do not pass the request id to it. Run the program, pick the first
request id from the output, and `grep` it: you must get exactly four lines, in order, from
`create_user`, `send_welcome`, and the wrapper, and the `DEBUG` one when the threshold is
lowered. Then, in C++, move the call to `send_welcome` onto a `std::thread` and join it, and
show the line that now says `"request_id":"-"`; fix it by passing the id into the thread. Done
means four lines per request id in all three languages, and the C++ break-and-fix pasted.

### 2. The secret scan

Write a tiny scanner, in any one language, that reads JSON log lines from standard input and
exits non-zero if any line has a key named `password`, `token`, `authorization`, `api_key`,
`card`, or `body`, printing the offending line's request id and key. Run each of the three
programs through it: all must pass. Then add a `password` field to each program's "user
created" line on purpose, run the scanner again, and paste the three failures. Then remove the
field. Done means the scanner exists, all three pass, and the three deliberate failures were
caught.

### 3. Wire it into the server

Take the day 49 server in each language and replace its `print`-style log line with today's
structured logger: the middleware, the wrapper or the hook sets the request id and logs the done
line with method, path, status and `ms`; every route logs through the same logger; the level
comes from the day 51 settings. Send the four requests from day 49 and paste the four JSON lines.
Then `grep` the 401's request id and show that the auth refusal and the done line share it. Done
means four JSON lines per language, no `print`, and the level switchable from a setting.

## Say these out loud

### DSA and system design

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Write insertion sort. When would you actually use it?*
   The code with no off-by-one, the invariant, the guard-order reason, and the three real cases —
   small inputs, nearly-sorted input, and values arriving one at a time.

2. *What is the difference between an abstract class and an interface?*
   Definition, the "is a kind of" against "is able to" rule, one situation for each, and the
   one-slot cost. Then the Python mechanisms for both.

3. *You have three O(n²) sorts. Why does anyone distinguish them?*
   Comparisons against writes with the numbers, best cases, adaptivity, and stability — ending on
   the one case where selection sort genuinely wins.

### Languages

*Three questions from today. Answer each in two minutes, standing up, no notes.*

1. What do you log, and what must you never log?
   The never list with the reason it is absolute; the always list, field by field; one JSON
   object per line; the request id; the done line with a duration; and the level you run at in
   production and how you lower it.
2. How does the request id reach a function three calls deep in each language?
   A `ContextVar`, a logger in the `context.Context`, a `thread_local`; and the case where each
   one breaks or does not: an async task, a goroutine, a thread pool.
3. Why is the message a constant string and the facts fields?
   Grouping, filtering on a value, and the `f`-string or `Sprintf` line that reads well and
   cannot be searched. Give the `ms > 500` example.

## Before you move on

- [ ] I wrote all three sorts from memory in under two minutes each, and they ran.
- [ ] I introduced the guard-order bug, ran it on `[2, 3, 1]`, and can say why there is no error.
- [ ] I can quote the write counts at n = 1,000: bubble 1,498,500 · insertion 500,499 · selection
      2,997.
- [ ] I can name the three situations where insertion sort is the right answer, unprompted.
- [ ] I submitted insertion sort to LeetCode 912, got the timeout, and can say the arithmetic behind
      it.
- [ ] I answered all twelve rapid-fire questions in three beats each, inside forty-five seconds.
- [ ] I can draw the abstract-class-against-interface diagram in any tool and say which triangle is
      which.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] The three lesson programs print five JSON lines with two request ids, and no `DEBUG` line until the level is lowered.
- [ ] Exercise 1 gives four lines per request id in all three, and I have the C++ `"-"` line and its fix.
- [ ] Exercise 2's scanner catches the three deliberate password fields and passes the clean programs.
- [ ] Exercise 3's servers log four JSON lines for the four day 49 requests, and the 401 shares an id with its done line.
- [ ] I can say the never-log list without pausing, and the reason it is absolute.
- [ ] I can say why spdlog needs a helper for fields, and what `!BADKEY` and `Attempt to overwrite 'name'` each mean.
