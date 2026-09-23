---
day: 90
track: practice
title: "Practice — Recursion on arrays and strings"
status: written
---

# Day 090 · Practice

**DSA topic:** Recursion on arrays and strings
**System design topic:** Design an in-memory cache with eviction

---

## Code these, in this order

One rule for the whole set: **an index, never a slice.** If your recursive call contains `[1:]` or
`[:-1]`, stop and rewrite it with a position. The function will still be correct and it will be a
different complexity class.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Reverse String | LeetCode 344 (Easy) | Two indices in place, and the `>=` base case that even lengths need. |
| 2 | Valid Palindrome | LeetCode 125 (Easy) | The same shape with characters to skip — where the indices move by different amounts. |
| 3 | Fibonacci Number | LeetCode 509 (Easy) | Loop to recursion to memoised recursion, and the call counts for all three. |
| 4 | Flatten Nested List Iterator | LeetCode 341 (Medium) | The case where recursion genuinely wins: depth is the nesting, not the length. |

### On problem 1, write the base case last

Write the swap and the recursive call first, then ask "when do I stop?" and *derive* `low >= high`
rather than remembering it. Then test `"abba"` and `"abcba"` — one of them is the reason it is `>=`.

### On problem 2, notice the indices move unevenly

Skipping non-alphanumeric characters means `low` may advance several times before a comparison. Say
what that does to the measure, and confirm it still strictly decreases.

### On problem 3, count the calls three ways

Instrument the naive recursion, the memoised one, and the loop. Run all three at n = 30 and write down
the three call counts and the three times.

### On problem 4, say why this one is different

Compare the depth of the recursion against the length of the input, and say why the iterative version
needs an explicit stack while the array versions needed nothing.

---

### The slice-versus-index drill

1. Write `total` with a slice and with an index.
2. Time both at n = 900 and write down the ratio.
3. Compute the number of element copies each performs, and state both complexities.
4. Say why the slicing version raises no error and gives the right answer.
5. Do the same for a string version and say why strings are worse.

### The two-index drill

1. Write the palindrome check with `low == high` as its base case.
2. Run it on `"abcba"`. Then run it on `"abba"`. Quote what happens.
3. Trace the index pairs for both inputs and say exactly where they diverge.
4. State the measure and say by how much it drops.
5. Say which of day 089's three termination conditions the `==` version fails.

### The conversion drill

For each loop, name the three parts and write the recursion:

1. Sum a list.
2. Find the maximum.
3. Count occurrences of a value.
4. Build a reversed copy.
5. Check whether a list is sorted.

Then convert two of the recursions back to loops, and say what you did with the accumulator.

### The helper-pattern drill

1. Write `is_palindrome(text, low=0, high=-1)` with the bookkeeping in the signature.
2. List three things wrong with that signature.
3. Rewrite it with a private inner helper.
4. Say what the inner function closes over and what that saves on every call.

### The break-it drill

Trigger each and record the exact output or error text:

1. Slice in the recursive call and time it against the index version.
2. Use `==` instead of `>=` in a two-index base case, on an even-length input.
3. Build a string with `+` inside a recursion at n = 5,000 and time it.
4. Use a mutable default as an accumulator and call the function twice.
5. Run a shrink-by-one recursion on 100,000 elements. Quote the error.
6. Run a split-in-half recursion on the same input. Say what the depth was.

### The two-shapes drill

1. Write a shrink-by-one recursion and a split-in-half recursion over the same array.
2. State the depth of each in terms of n.
3. Run both on 100,000 elements and record which survives.
4. Count the total calls each makes.
5. Say when divide and conquer is an improvement and when it is a demonstration.

### The string drill

1. Write a recursive reverse using slicing and concatenation.
2. Count the character copies for n = 10,000.
3. Rewrite it collecting into a list and joining once.
4. Rewrite it again working on a `list(text)` in place with two indices.
5. State the complexity of all three, and say which you would ship.

### The judgement drill

For each, say whether you would use recursion or a loop, and why in one sentence:

1. Sum a flat list.
2. Reverse a string.
3. Flatten an arbitrarily nested list.
4. Merge sort an array.
5. Walk a directory tree.
6. Find the maximum of an array.
7. Binary search a sorted array.

Two of the seven are the cases where recursion genuinely wins. Name what they have in common.

---

### The three-mechanisms drill

1. Define eviction, expiry and invalidation in one sentence each.
2. Give an example of an entry that is expired and still resident.
3. Give an example of an entry evicted while perfectly fresh.
4. Describe the bug that comes from merging eviction and expiry.
5. Say which of the three is about correctness and which is about capacity.

### The policy drill

1. Write the `EvictionPolicy` interface with its four methods.
2. Implement LRU using an `OrderedDict` and name the two O(1) operations.
3. Implement Random and state its hit rate relative to LRU.
4. State plain LFU's structural weakness and the two standard fixes.
5. Apply the interface gate: name all four implementations and say why the interface is justified here
   more clearly than in most examples.
6. Say what `Entry` must *not* contain, and why.

### The expiry drill

1. Implement lazy expiry on read. Say why an expired hit must count as a miss.
2. Say precisely what lazy expiry leaks and why.
3. Implement the sampled sweep with Redis's adaptive rule.
4. Say why sampling alone is wasteful.
5. Compute how long an unread expired entry survives, given 20 keys sampled 10 times a second out of
   100,000.
6. Contrast this with the food-delivery timeout from day 087 and say why one needs a sweeper for
   correctness and the other does not.

### The stampede drill

1. Compute the concurrent identical queries for a key at 5,000 req/s with a 200 ms load.
2. Say what actually breaks, and why it is not the hot key.
3. Write single-flight with a per-key lock.
4. Say why the lock must be per key and not global.
5. Say why the re-check inside the lock is essential, and what happens without it.
6. Compute the effect of TTL jitter on 1,000 keys loaded together with a 600 s TTL.
7. Describe `stale-while-revalidate` and say what it trades.

### The sizing drill

Compute each, showing the multiplication:

1. Memory for 100,000 entries of 2 KB, including entry, dict and LRU overhead.
2. The overhead as a percentage of the data.
3. The same overhead percentage for 200-byte values.
4. Memory for 100,000 entries of 2 MB.
5. Average read time at hit rates of 99, 95, 90 and 50 percent, given 100 µs and 1 µs.

Then say which number tells you to count bytes instead of entries, and which tells you where to stop
adding capacity.

### The threading drill

1. Say what one global lock does to a cache doing a million gets a second.
2. Describe sharding and what it costs.
3. Say why the single-flight locks are a separate matter.
4. Say what happens to a waiter if the loader hangs, and what you would add.

### The would-you-ship-it drill

For each, say what you would actually use and why:

1. Memoising a pure function in one process, no TTL.
2. A per-request cache within one request's lifetime.
3. A hot config value read a million times a second.
4. A shared cache across ten servers.
5. A cache in front of a database where staleness is unacceptable.

One of the five needs no cache at all. Name it and say what it needs instead.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Reverse a string recursively. Now do it without extra space.*
   The shape named first, the index-not-slice rule with its complexity consequence, two indices with
   the `>=` base case and *why*, the private helper, both costs including the honest note that
   recursion is never O(1) space, and what you would ship.

2. *Design an in-memory cache. Now make the eviction policy swappable.*
   The three mechanisms separated with the expired-and-resident sentence, `Entry` with no policy state,
   the four-implementation interface, lazy plus sampled expiry with why each alone fails, the stampede
   with its arithmetic and single-flight with the re-check, TTL jitter, and the hit rate as the only
   tunable number.

3. *A very popular key expires. What happens?*
   The 5,000 × 0.2 arithmetic, why the damage lands on unrelated queries, single-flight with a per-key
   lock and the inner re-check, and jitter as the one-line prevention.

---

## Before you move on

- [ ] I never slice in a recursive call, and I measured the ratio myself.
- [ ] I can derive `low >= high` rather than remember it, and say why `==` fails.
- [ ] I can convert a loop to a recursion by naming its three parts.
- [ ] I use a private helper so the public signature has no bookkeeping.
- [ ] I built a recursive string with `+` and measured how bad it is.
- [ ] I know which recursion shape survives 100,000 elements and which does not.
- [ ] I can say when divide and conquer is an improvement rather than a demonstration.
- [ ] I can name the two cases where recursion genuinely beats a loop.
- [ ] I can define eviction, expiry and invalidation and give an example of each mismatch.
- [ ] I can say what `Entry` must not contain and why.
- [ ] I implemented LRU and Random and can quote their relative hit rates.
- [ ] I can state plain LFU's weakness and both fixes.
- [ ] I can explain why lazy expiry leaks and why sampling alone is wasteful.
- [ ] I can compute the stampede numbers and write single-flight correctly.
- [ ] I can say why the re-check inside the lock is essential.
- [ ] I can give the hit-rate table and say where the value falls off a cliff.
- [ ] I answered all three questions above out loud.
