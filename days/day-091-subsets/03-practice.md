---
day: 91
track: practice
title: "Practice — Subsets: the include-or-exclude tree"
status: written
---

# Day 091 · Practice

**DSA topic:** Subsets: the include-or-exclude tree
**System design topic:** Design a logging framework

---

## Code these, in this order

One rule for the whole set: **say "copy" out loud as you type `current[:]`.** The single most common
backtracking bug appends the working list itself, and the result is uniformly wrong with no error at
all.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Subsets | LeetCode 78 (Medium) | The tree, choose-recurse-un-choose, and the copy. |
| 2 | Subsets II | LeetCode 90 (Medium) | Sorting first, and `i > start` rather than `i > 0`. |
| 3 | Combinations | LeetCode 77 (Medium) | The same tree with a cap, and the first real pruning. |
| 4 | Letter Combinations of a Phone Number | LeetCode 17 (Medium) | The same shape where the branching factor is 3 or 4 rather than 2. |

### On problem 1, run the broken version first

Write it with `result.append(current)` and print the output. Eight empty lists. Then fix it and say, in
one sentence, why every entry was the same object.

### On problem 2, test `[2, 2]` before anything else

The right answer has three subsets. Write the version with `i > 0` and confirm it gives two. Then fix
the condition and say what `i > start` means in terms of the tree.

### On problem 3, add the prune and measure it

Write it without the "not enough elements left" check, then with it. Count the calls both ways for
choosing 8 from 20 and write both numbers down.

### On problem 4, notice what changed

The branching factor is no longer two. Say what stayed exactly the same, and what the complexity became
in terms of the digits.

---

### The size drill

1. Say why there are exactly 2ⁿ subsets, in one sentence about decisions.
2. Compute the count for n = 10, 20, 25 and 30.
3. Say why no algorithm can be faster, and what that sentence prevents in an interview.
4. Given a problem that says `n ≤ 20`, say what that constraint is telling you.

### The pattern drill

1. Write the three lines of choose-recurse-un-choose from memory.
2. Say what the `pop` is for, and what happens if you leave it out — including whether it raises.
3. Draw the decision tree for `[1, 2, 3]` and label every leaf.
4. Count the leaves, the nodes and the depth.
5. Say which of those three is the time and which is the space.

### The copy drill

1. Write the version that appends the list instead of a copy.
2. Print the result for `[1, 2, 3]` and describe exactly what you see.
3. Explain why every entry is empty at the end.
4. Name three ways to make the copy.
5. Say why this bug produces no error.

### The two-arrangements drill

1. Write the version where only the leaves are subsets.
2. Write the version where every node is a subset.
3. Confirm they produce the same set of answers.
4. Say which one generalises, and give two problems it generalises to.

### The other-formulations drill

1. Write the iterative doubling version in two lines.
2. Say what happens if you seed it with `[]` instead of `[[]]`.
3. Write the bitmask version.
4. Say what `mask = 5` means for a three-element array.
5. State the limit of the bitmask approach and say why it never matters here.
6. Say which version you would write in an interview, and why it is not the shortest one.

### The duplicates drill

1. Sort, then write the skip with `i > start`.
2. Run it on `[1, 2, 2]` and count the distinct subsets against the number of decision paths.
3. Change the condition to `i > 0` and run `[2, 2]`. Say which subset disappeared and why.
4. Remove the sort and run `[2, 1, 2]`. Say why nothing gets skipped.
5. Write the filter-at-the-end version and say what it costs on `[2] * 20`.

### The break-it drill

Trigger each and record the exact output:

1. `result.append(current)` without the copy.
2. Omit the `pop`.
3. `i > 0` instead of `i > start`, on `[2, 2]`.
4. Forget to sort before de-duplicating.
5. Seed the iterative version with `[]`.
6. Compare your recursive output against the iterative one without sorting either. Explain the
   mismatch.

### The generalisation drill

For each, say what changes from the subsets template and what stays the same:

1. Combinations of size k.
2. Permutations.
3. Combination sum, where numbers may be reused.
4. N-Queens.
5. Word search on a grid.

Name the one thing that all five share, and the one thing that makes the last two "backtracking"
rather than "enumeration".

---

### The two-interfaces drill

1. Name the two interfaces and what each one decides.
2. Say how many classes you need for 4 destinations and 3 formats, kept separate and combined.
3. Write the `Handler` interface and one implementation.
4. Say what else a handler carries besides the formatter, and what that enables.
5. Answer the prompt — "how do I add a destination?" — in one sentence.

### The hot-path drill

1. Write the `log` method with the level check in the right place.
2. Say why the check must be the first statement.
3. Write the same log call two ways — f-string and deferred — and say what executes in each.
4. Compute the CPU cost per second for 200,000 calls at 80 percent suppressed, for a cheap f-string and
   an expensive one.
5. Say what the API's shape has to be for deferral to be possible at all.
6. Write the guard for a genuinely expensive argument.

### The hierarchy drill

1. Draw four loggers in a tree.
2. Say what "effective level" means and how it is computed.
3. Describe what happens to a record logged at the deepest node.
4. Say how this differs from a plain chain of responsibility.
5. Say what one line of configuration you would write to debug one subsystem.
6. Say what `propagate = False` does and when you would use it.

### The structured drill

1. Write the same event as a sentence and as a record.
2. Write the query "failed Razorpay payments over ₹10,000 last Tuesday" against each.
3. State the storage cost difference as a percentage.
4. Say what structured logging decouples, beyond queryability.
5. Say what the highest-value field in any log line is and why.

### The async drill

1. Compute the I/O time per second for synchronous network writes at 40,000 lines a second.
2. Write the queue handler with a bounded queue.
3. Say why it must drop rather than block.
4. Say what must accompany every drop.
5. Compute the buffer in milliseconds for a 10,000-record queue at 40,000 records a second.
6. Say what is lost on a crash and name the two mitigations.

### The volume drill

Compute each, showing the multiplication:

1. Log calls per second at 10,000 req/s and 20 statements each.
2. Bytes and terabytes per day at DEBUG, INFO and WARNING.
3. Lines per day, and how many belong to one request.
4. Storage saved by sampling one noisy event at 1 percent.
5. The rupee cost per month of the DEBUG option at ₹2 per GB.

### The failure drill

For each, say what happens and what you would add:

1. The disk fills.
2. A value cannot be serialised to JSON.
3. The network collector hangs for one second.
4. The process is killed by the OOM killer.
5. A library configures the root logger.
6. A user-supplied string containing `${...}` is logged.
7. A request body is logged at DEBUG in production.

Two of the seven are security problems rather than reliability problems. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Generate all subsets of this array.*
   The 2ⁿ size stated first and why nothing can beat it, the decision tree described before any code,
   choose-recurse-un-choose with what the pop is for, the copy flagged before you write it, both
   complexities kept separate, and the iterative alternative offered with a reason for choosing the
   recursive one.

2. *Design a logging library. How do I add a new destination?*
   One class and one line, because `Handler` and `Formatter` are separate — then the part that matters:
   the level check first with the eight-cores arithmetic, the hierarchy and what it buys, structured
   records with a correlation id and the seventeen-billion number, and the bounded queue with its drop
   policy and crash loss.

3. *What does a suppressed `debug` call cost?*
   One integer comparison if the API allows deferral, and eight seconds of CPU per second if it does
   not — with the reason arguments are evaluated before the call.

---

## Before you move on

- [ ] I can say why there are 2ⁿ subsets and why nothing can be faster.
- [ ] I can write choose-recurse-un-choose without thinking, and say what the pop is for.
- [ ] I ran the no-copy version and can explain the eight empty lists.
- [ ] I can draw the decision tree and say which count is time and which is space.
- [ ] I wrote all three formulations and know which one generalises.
- [ ] I can state what happens if the iterative version is seeded with `[]`.
- [ ] I can write the duplicate skip and explain `i > start` versus `i > 0`.
- [ ] I tested `[2, 2]` and know which subset the wrong condition loses.
- [ ] I can say why pruning beats filtering, with the `[2] * 20` example.
- [ ] I can name what changes for combinations, permutations and N-Queens.
- [ ] I can answer "how do I add a destination" in one sentence.
- [ ] I can say why `Handler` and `Formatter` are separate, with the N × M argument.
- [ ] I can compute the cost of suppressed f-strings at 200,000 calls a second.
- [ ] I can explain why the API takes a template and arguments.
- [ ] I can describe the hierarchy, effective level and propagation.
- [ ] I can state the correlation id's value with the lines-per-day number.
- [ ] I can defend dropping over blocking, and say what must accompany a drop.
- [ ] I answered all three questions above out loud.
