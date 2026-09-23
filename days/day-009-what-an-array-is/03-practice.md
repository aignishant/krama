---
day: 9
track: practice
title: "Practice — What an array really is in memory"
status: written
---

# Day 009 · Practice

**DSA topic:** What an array really is in memory
**System design topic:** CPU, RAM, and disk: the speed hierarchy

---

## Code these, in this order

Four problems that all rest on one fact: you may reach any position of an array directly, and
it costs the same wherever you reach. Each one uses that differently.

For each problem:

1. Say which positions you need to reach, and in what order.
2. State whether you are walking forwards, backwards, or jumping — and whether the order
   could be made sequential.
3. Solve it, then state the time and extra space.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Build Array from Permutation | LeetCode 1920 (Easy) | The purest possible use of `O(1)` indexing: `nums[nums[i]]` is two direct reaches, not a search. If indexing were `O(n)` this problem would not exist. |
| 2 | Concatenation of Array | LeetCode 1929 (Easy) | Position arithmetic. `ans[i]` and `ans[i + n]` are both computed, both direct, both the same cost. |
| 3 | Richest Customer Wealth | LeetCode 1672 (Easy) | A 2D list is a list of references to lists. Row-by-row is the natural order and also the cache-friendly one — notice that they agree. |
| 4 | Find Pivot Index | LeetCode 724 (Easy) | Two passes over the same array, both sequential. The naive version recomputes a sum inside the loop and is `O(n²)`; spotting that is the exercise. |

### On problem 3, do this properly

After solving it, write the column-major version — the one that loops over columns on the
outside and rows on the inside — producing the same answer. Time both on a grid of about
2,000 × 2,000.

They are both `O(rows × cols)` and they will not take the same time. Say out loud why, using
the words "cache line".

### The address drill

Answer these from memory, with the arithmetic shown, in under a minute:

- An array of 4-byte integers starts at address 2000. Where is `items[12]`?
- An array of 8-byte values starts at address 5000. Where is `items[1000]`?
- Why does the answer to either take the same time as finding `items[0]`?
- What breaks if one element in the middle is 6 bytes instead of 4?
- A Python list of 1,000,000 integers — how much memory, roughly, and where does it go?

### The measurement drill

Run the complete program from §5 of the lesson. Then change one thing: make the shuffled test
use a list of 100,000 elements instead of 4,000,000, and run it again.

The ratio between ordered and shuffled should shrink dramatically. Explain why in one
sentence. (The answer involves the size of L3 cache from the system design lesson.)

### The numbers to have cold

Say these six out loud without looking:

- RAM read, in nanoseconds.
- SSD read, in microseconds.
- Spinning-disk seek, in milliseconds.
- How many times slower SSD is than RAM.
- How many times slower a disk seek is than RAM.
- A cache line, in bytes.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *Why is array indexing O(1)?*
   Give the formula with real addresses. Then name the requirement that makes it work. Then
   derive why front insertion is `O(n)` from the same fact.

2. *How much slower is a disk read than a memory read?*
   Give the absolute numbers, then the ratios, then the human scale. Then say what follows
   from it about caching.

3. *Two loops read the same million elements and one is five times slower. Why?*
   One sentence on cache lines, one on the RAM-versus-cache gap, one on why Big-O is still
   right.

---

## Before you move on

- [ ] I can write `address = base + i × element_size` from memory and put real numbers in it.
- [ ] I can say the three requirements that make the formula work.
- [ ] I know that a Python list stores references, and roughly what a million integers costs.
- [ ] I can order register, L1, RAM, SSD, HDD and network by speed, with numbers.
- [ ] I can explain why a 90% cache hit rate is a worse position than it sounds.
