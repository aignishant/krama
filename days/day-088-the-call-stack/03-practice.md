---
day: 88
track: practice
title: "Practice — The call stack, drawn"
status: written
---

# Day 088 · Practice

**DSA topic:** The call stack, drawn
**System design topic:** Design a ride-hailing booking flow

---

## Code these, in this order

One rule for the whole set: **before optimising or converting anything, say which number you are
worried about — total calls or maximum depth.** They are different questions and the fixes are
different.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Binary Tree Inorder Traversal | LeetCode 94 (Easy) | Write it recursively, then iteratively. This is the conversion where the work happens *after* the calls. |
| 2 | Maximum Depth of Binary Tree | LeetCode 104 (Easy) | Depth as a value *and* depth as a cost — and the degenerate tree that kills the recursive version. |
| 3 | Climbing Stairs | LeetCode 70 (Easy) | Naive recursion, count the calls, then memoise. Fibonacci wearing a hat. |
| 4 | Flatten Nested List Iterator | LeetCode 341 (Medium) | An explicit stack because the depth is attacker-controlled — the practical reason for the conversion. |

### On problem 1, write both and count the lines

The recursive version is four lines. The iterative one needs a stack of nodes and a way to remember
whether you have already scheduled a node's children. Count both, and say what the extra lines are
storing.

### On problem 2, build the tree that breaks it

Insert 5,000 sorted values into an unbalanced binary search tree, then call the recursive version.
Quote the error. Then call the iterative one on the same tree.

### On problem 3, instrument before you memoise

Add a global counter. Run `n = 10`, `20`, `30` and write the three call counts down. Then memoise and
run the same three. Say what the ratio is at `n = 30`.

### On problem 4, say why iteration is not optional here

The nesting depth comes from the input. Say what that means if the input comes from outside your
system, and name the class of vulnerability.

---

### The frame drill

1. Name the three things a stack frame holds.
2. Draw the stack for `factorial(4)` at its deepest point, with what each frame is waiting for.
3. Say which frames are suspended and what they are suspended in the middle of.
4. Say in which phase the arithmetic happens, and why that determines the space cost.

### The tree-versus-stack drill

1. Draw the recursion tree for `fib(5)` and count the nodes.
2. Draw the stack at three different moments during that run.
3. State the maximum depth.
4. Instrument `fib` to count both and run it for n = 5, 10, 20. Write down six numbers.
5. State the sentence that separates the two, in seven words or fewer.
6. Give one function that is cheap in time and expensive in space, and one that is the reverse.

### The tracing drill

1. Add a `depth` parameter to a recursive function and indent the prints.
2. Run it on the smallest input that shows the shape.
3. Now run it on `fib(25)` with the prints still in. Describe what happens and what you learned about
   where to trace.
4. Use `len(inspect.stack())` to confirm the depth matches your drawing.

### The limit drill

1. Print `sys.getrecursionlimit()`.
2. Write the function that finds the deepest actually reachable depth. Run it from a script and from a
   bare prompt and write both numbers.
3. Explain the gap between the two.
4. Run a linear-depth recursion on a 5,000-element list. Quote the error.
5. Raise the limit to a million and run it again. Describe exactly what happens and what you lose.

### The traceback drill

1. Trigger a `RecursionError` and read the traceback.
2. Say which end is the most recent call, and how that differs from C or Java.
3. Say what "previous line repeated N times" tells you.
4. Given a traceback, list the three possible causes and how you would tell them apart.

### The conversion drill

1. Convert a pre-order traversal to an explicit stack. Count the lines.
2. Convert a post-order traversal — where the work happens after the children — and count again.
3. Name what the extra state is storing, in terms of what the machine was doing for you.
4. Say when the conversion is mechanical and when it is not.
5. Convert a linear recursion to a plain loop and say why no stack was needed at all.

### The tail-call drill

1. Rewrite a linear recursion in tail form with an accumulator.
2. Run it on a 5,000-element list. Quote the error.
3. Say what a language with tail-call elimination would have done.
4. Say why Python does not do it, and what was traded for what.

### The degenerate-input drill

1. Build a balanced tree of 100,000 nodes and run the recursive count. Note the depth.
2. Build a degenerate tree of 5,000 nodes and run the same function. Quote the error.
3. State, in one sentence, whose property the depth is.
4. Give three real sources of degenerate input.
5. Say what it means when the depth can be chosen by an attacker.

---

### The two-systems drill

1. Compute the location writes per second and the trip writes per second.
2. State the ratio.
3. State the durability requirement of each.
4. Say where each one is stored and why.
5. Compute the total size of the live location state and say what that makes possible.

### The offer-lock drill

1. Say what an offer to a driver *is*, in one sentence, and name the two earlier lessons with the same
   shape.
2. Write the conditional claim.
3. Say what zero rows affected means and what the matcher does next.
4. Say why the `tried` set matters.
5. Say what must happen the instant a driver accepts, and compute what it costs to forget.

### The batching drill

1. Compute the expected number of offers for sequential matching at a 60 percent acceptance rate.
2. Compute the time to match at eight seconds per offer.
3. Compute the probability that at least one of three accepts.
4. Compute the expected time to match when batching three.
5. State the cost of batching in the drivers' terms.
6. Say which you would ship and what you would tune it against.

### The location drill

1. Say why separate latitude and longitude indexes cannot answer "within 3 km".
2. Explain geohashing in two sentences.
3. Describe the edge problem and the fix.
4. Compute how many cells a 3 km query reads at precision 6.
5. Say what the staleness TTL is for, and what happens without it.
6. Say why ranking by distance is worse than ranking by ETA, with an example.

### The fare drill

1. Write the frozen quote and mark which field matters most.
2. Compute the overcharge when surge moves 1.4× to 2.0× on a ₹250 fare.
3. Say what that number is an argument about — and it is not pricing.
4. Name two earlier lessons with the same immutability rule.
5. Say what freezing the quote transfers to the platform, and how real platforms handle it.

### The state-and-timeout drill

For each transition, name the actor, the timeout, and what happens when it passes:

1. REQUESTED → MATCHING
2. MATCHING → ASSIGNED
3. MATCHING → no driver
4. ASSIGNED → ARRIVING
5. ARRIVED → IN_PROGRESS
6. IN_PROGRESS → COMPLETED

Then compute how many "no driver" outcomes there are per day, and say what that number makes it.

### The cancellation drill

For each, state the fee and the reason in the user's language:

1. Rider cancels before a driver is assigned.
2. Rider cancels after assignment.
3. Rider does not appear after the driver has arrived.
4. Driver cancels after accepting.
5. The system fails to match.

Say what is *counted* rather than charged, and why that is a design consequence.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Trace this recursion. What is on the stack at the deepest point?*
   What a frame holds, the two phases with the arithmetic on the way back up, the deepest point drawn
   with what each frame is waiting for, the tree-versus-stack distinction with the measured `fib(20)`
   numbers, the real limit, and the conversion with its honest caveat.

2. *Design the booking flow for a cab app.*
   Split it into the location firehose and the trip records with the ratio, the offer as a lock with a
   conditional claim, sequential versus batched with both times, releasing losers immediately with its
   cost, geohashing with the edge problem, ranking by ETA, and the frozen surge with the 43 percent
   arithmetic.

3. *How many calls does `fib(20)` make and how much stack does it use?*
   21,891 and 20, why they diverge, and the seven-word sentence that separates time from space.

---

## Before you move on

- [ ] I can name the three things in a stack frame.
- [ ] I can draw the stack at the deepest point with what each frame is waiting for.
- [ ] I can say in which phase the work happens and why that is the space cost.
- [ ] I instrumented `fib` and can quote calls and depth for n = 5, 10 and 20.
- [ ] I can state the time-versus-space sentence in one line.
- [ ] I traced a recursion with indentation and know to use the smallest input.
- [ ] I measured the real reachable depth and can explain why it is not 1,000.
- [ ] I raised the recursion limit on purpose and saw what it costs.
- [ ] I can read a Python traceback from the correct end.
- [ ] I converted both a pre-order and a post-order traversal and can say what the extra state is.
- [ ] I wrote a tail-recursive function and confirmed it dies at the same depth.
- [ ] I built a degenerate tree and killed the recursive version on it.
- [ ] I can compute the location-to-trip write ratio and say where each is stored.
- [ ] I can write the driver claim and say what zero rows means.
- [ ] I can compute both matching times and say what releasing losers late costs.
- [ ] I can explain the geohash edge problem and the nine-cell query.
- [ ] I can give the surge arithmetic and say what it is an argument about.
- [ ] I answered all three questions above out loud.
