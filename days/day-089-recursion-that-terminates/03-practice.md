---
day: 89
track: practice
title: "Practice — Writing a recursive function that terminates"
status: written
---

# Day 089 · Practice

**DSA topic:** Writing a recursive function that terminates
**System design topic:** Design a rate limiter, at the object level

---

## Code these, in this order

One rule for the whole set: **write the measure as a comment before the base case.** One line naming
what shrinks, by how much, and what its floor is. If you cannot write it, you do not yet know that the
function ends.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Greatest Common Divisor of Strings | LeetCode 1071 (Easy) | Euclid's shape, where the obvious argument is not the measure. |
| 2 | Number of Islands | LeetCode 200 (Medium) | A grid with no natural measure — the visited marking *is* the termination argument. |
| 3 | Unique Paths | LeetCode 62 (Medium) | A measure that is a combination of two arguments, and the call count it predicts. |
| 4 | Sqrt(x) | LeetCode 69 (Easy), then the float version | An integer measure that terminates, then a float one that needs an epsilon. |

### On problem 1, say the measure before the code

It is not the first argument. Say which one shrinks and why it must, and only then write the three
lines.

### On problem 2, break it deliberately

Write the flood fill without marking cells visited. Run it on a two-by-two grid of land. Quote the
error. Then move the marking to *after* the recursive calls instead of before, and run it again — say
why that fails too.

### On problem 3, count the calls

Instrument the naive recursion. Run it for a 3×3, 5×5 and 10×10 grid and write the three counts down.
Say what the measure predicts, and then memoise and count again.

### On problem 4, do both versions

The integer version terminates because the interval is an integer range. The float version does not,
because a halving interval never reaches zero. Write both, and say exactly what you had to add.

---

### The three-conditions drill

State all three from memory, then apply them to each function:

1. `total(numbers, start)`
2. `power(base, n)` with `n - 1`
3. `power(base, n)` with `n - 2`
4. `gcd(a, b)`
5. `paths(row, col)`
6. `bisect_root(low, high)` with no epsilon
7. A depth-first search on a graph with a cycle, with no visited set

For each, say which condition fails, or say that all three hold.

### The name-the-measure drill

For each, name the measure in one phrase and say by how much it drops:

1. Summing a list by index.
2. Reversing a string by slicing.
3. Binary search on an integer range.
4. Merge sort.
5. Euclid's algorithm.
6. Counting grid paths.
7. Flood fill on a grid.
8. Ackermann.

Two of the eight have a measure that is not a single argument. Name them and say what the measure is.

### The failure drill

Write each of the three failures, run it, and quote the error:

1. The measure never moves.
2. The measure steps over the bound.
3. The measure decreases and never reaches the floor.

For the second one, "fix" it by widening the guard to `<= 0` and say precisely what you have now got
instead of a crash.

### The graph drill

1. Write a traversal of a cyclic graph with no visited set. Quote the error.
2. Add the set and say what measure you have just created.
3. Move `seen.add` to after the loop instead of before. Run it and explain the result.
4. Change `seen=None` to `seen=set()` as a default. Call the function twice on different graphs and
   describe what the second call returns.
5. Say in one sentence why a tree does not need the set, and what property it has that a graph lacks.

### The float drill

1. Write a bisection with `if low == high` as its base case. Run it.
2. Add an absolute epsilon and run it again. Count the calls.
3. Compute the number of halvings needed for an epsilon of 1e-9 and of 1e-15 on the interval [0, 2].
4. Try an absolute epsilon on an interval around 1e12 and describe what happens.
5. Add a depth guard as a second, independent bound and say why two reasons to stop is cheap.

### The mutual-recursion drill

1. Write `is_even` and `is_odd`.
2. Say what the measure is and around what it decreases.
3. Break one leg so it does not decrement. Run it and quote the error.
4. Say why each function looks correct in isolation.
5. State the general rule about cycles in the call graph.

### The measure-predicts-complexity drill

For each, use the measure to state the complexity, then verify by counting calls:

1. Drops by 1, one call per level.
2. Halves, one call per level.
3. Drops by 1, two calls per level.
4. `paths(row, col)`, where the measure is `row + col` and there are two calls per level.

Then run `paths(10, 10)` with a counter and check your prediction.

### The honesty drill

1. Write the Collatz step function.
2. Say whether it terminates and what is actually known.
3. Add an explicit limit and raise. Say why that is the honest thing to do.
4. State, in one sentence, why "it worked on the inputs I tried" is not a termination argument.

---

### The interface drill

1. Write the `Decision` dataclass and say why it is not a boolean.
2. Say why `now` is a parameter.
3. Say why the key is an opaque string, and what that separates.
4. Name the two HTTP headers this makes possible and what a client does with each.

### The boundary drill

1. Implement the fixed window limiter.
2. Allow 100 requests at t = 59.9 and 100 more at t = 60.1. Print how many were allowed and over what
   span.
3. State the effective worst-case rate as a multiple of the configured limit.
4. Say why the boundary being *predictable* makes it worse than being merely wrong.
5. Name a case where fixed window is still the right choice.

### The memory drill

Compute each, showing the multiplication, for 1,000,000 active keys:

1. Fixed window.
2. Sliding counter.
3. Token bucket.
4. Sliding log at a limit of 100 per minute.
5. Sliding log at a limit of 10,000 per hour.

Then say which number rules the sliding log out, and what property of it causes that.

### The token-bucket drill

1. Implement it with lazy refill.
2. Express "100 per minute sustained, bursts of up to 20" as a rate and a capacity.
3. Compute the tokens available after 12 seconds of silence.
4. Compute `retry_after` on an empty bucket.
5. Say what a new key's bucket should start at, and defend the choice.
6. Say which single property no other algorithm here can express.

### The distributed drill

1. Write the naive Redis fixed window as two commands.
2. Describe exactly what happens if the process dies between them, and what the symptom looks like.
3. Say why a `GET`, compute, `SET` token bucket in application code is wrong under concurrency.
4. Write the Lua script version and say what makes it safe.
5. Say how you would choose the TTL, and why it is derived rather than guessed.

### The operations drill

1. Compute the added latency per request for a Redis round trip, and its percentage on a 20 ms and a
   2 ms endpoint.
2. Describe the two-tier mitigation and what it gives up.
3. Say what should happen when the store is unreachable, and defend it.
4. Say what the default behaviour of an unhandled exception is, and why that matters here.
5. Name one case where the opposite choice is correct.

### The choose-the-algorithm drill

For each, name the algorithm and the deciding reason:

1. 1,000 API calls per day, for billing.
2. Five login attempts per hour per account.
3. 100 requests per minute per API key on a public API, ten servers.
4. Calls to a payment provider that permits exactly 10 per second.
5. A page load that legitimately makes 15 requests at once.
6. Password reset emails, one per day per account.

Two of the six want the exact algorithm for the same reason. Name it.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Why does your recursion terminate?*
   The measure named first, all three conditions, the argument that actually shrinks (and in Euclid, the
   one that does not), the combination case, the graph case where the visited set *creates* the
   measure, and the float case where you supply the floor.

2. *Implement a rate limiter. Which algorithm, and why?*
   The interface and its two decisions, fixed window with its boundary demonstrated, the sliding log's
   memory arithmetic, token bucket as the default with the two independent knobs and the lazy refill,
   the `INCR`/`EXPIRE` race, and fail-open.

3. *What is wrong with counting requests per minute and resetting?*
   The boundary burst with the exact numbers, why predictability makes it worse, and the one case where
   it is still right.

---

## Before you move on

- [ ] I write the measure as a comment before writing the base case.
- [ ] I can state all three termination conditions from memory.
- [ ] I can name the measure for eight different functions, including two that are combinations.
- [ ] I know why `b` is Euclid's measure and `a` is not.
- [ ] I wrote all three failure modes and quoted the errors.
- [ ] I know what widening a guard to `<= 0` gives me instead of a crash.
- [ ] I broke a graph traversal by removing the visited set, and by marking too late.
- [ ] I used a mutable default as an accumulator and saw the second call misbehave.
- [ ] I can say why a tree needs no visited set and a graph does.
- [ ] I added an epsilon and a depth guard to a float recursion.
- [ ] I can use the measure to predict complexity, and verified it by counting calls.
- [ ] I can say why "it worked on my inputs" is not a termination argument.
- [ ] I demonstrated the fixed-window boundary burst with real numbers.
- [ ] I can give the memory arithmetic for all four algorithms at a million keys.
- [ ] I can express a rate and a burst as two independent token-bucket knobs.
- [ ] I can describe the `INCR`/`EXPIRE` race and its symptom.
- [ ] I can defend fail-open, and name the case where the opposite is right.
- [ ] I answered all three questions above out loud.
