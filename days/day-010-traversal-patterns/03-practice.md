---
day: 10
track: practice
title: "Practice — Traversal: the loop patterns you will reuse forever"
status: written
---

# Day 010 · Practice

**DSA topic:** Traversal: the loop patterns you will reuse forever
**System design topic:** Latency numbers every engineer should know

---

## Code these, in this order

Four problems, one per traversal pattern. The code in each is short; the loop bound is the
whole exercise.

For each problem, **before writing the loop**:

1. Say the largest index the body will touch.
2. Say the bound that follows from it, out loud, with the arithmetic.
3. Say how many iterations that gives for an array of 7.
4. Then write it, and check the empty and single-element cases without adding a special case.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Monotonic Array | LeetCode 896 (Easy) | The adjacent-pairs bound, exactly. `range(n - 1)` because the body reaches `i + 1`, and it must return `True` for a one-element array without a guard. |
| 2 | Maximum Average Subarray I | LeetCode 643 (Easy) | The fixed window. The slicing version is `O(n × k)` and passes; the running-total version is `O(n)`. Write the slow one first, then fix it, and say what changed. |
| 3 | Reverse String | LeetCode 344 (Easy) | Two pointers from the ends. `while left < right`, and the loop naturally handles both odd and even lengths without a special case. |
| 4 | Remove Element | LeetCode 27 (Easy) | The trap from §7 — deleting while iterating forwards. Write the `remove()`-in-a-loop version, watch it skip elements, then write the write-pointer version. |

### On problem 2, do this properly

- Write it with `sum(nums[i:i+k])` inside the loop. Submit it. Note the runtime.
- Work out the complexity: `n` up to 10⁵ and `k` up to `n` means how many operations?
- Rewrite with a running total: add `nums[i]`, subtract `nums[i - k]`.
- Submit again and compare the runtimes.
- Then answer out loud: **why does the running total not work for a sliding-window
  maximum?**

### The bounds drill

Answer these six from memory, with the arithmetic, in under ninety seconds:

- The body touches `items[i]`. What is the bound, and how many iterations for `n = 7`?
- The body touches `items[i + 1]`. Same two questions.
- The body touches `items[i + 2]`. Same two questions.
- A window of `k = 4` over `n = 10`. How many windows, and where does the last one start?
- Walking backwards over `n = 7` — write the `range(...)` exactly.
- Two pointers from the ends of `n = 7`. How many iterations before they meet?

### The trap drill

Type this and predict the output **before** running it:

```python
items = [1, 2, 2, 3, 2, 4]
for x in items:
    if x == 2:
        items.remove(x)
print(items)
```

Then explain, in one sentence, why one `2` survived. Then write two versions that give the
right answer — one that builds a new list, one that walks backwards — and say what each costs
in space.

### The latency drill

Say these from memory, in under a minute:

- Main memory reference, in nanoseconds.
- SSD random read, in microseconds.
- Round trip within a data centre, in milliseconds.
- Round trip across the world, in milliseconds.
- 1 Gbps, converted to megabytes per second.
- How many requests per second a million requests a day works out to.

Then use them: a request has a 40 ms user network leg, a 1 ms parse, a 5 ms database query
and a 2 ms render. What is the total, which leg dominates, and what single change would help
most?

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *Iterate over every adjacent pair in the array.*
   State the bound and its reason before writing it. Give the pair count for `n = 7`. Say what
   happens for an empty list without adding a guard.

2. *Roughly how long is a network round trip to a data centre on another continent?*
   Give the range, then the physics, then the neighbouring numbers, then the design
   consequence.

3. *Our p99 is 200 ms and our p50 is 20 ms. Is that a problem?*
   Do the fan-out multiplication out loud, then say what you would investigate, then name two
   techniques that limit the damage.

---

## Before you move on

- [ ] I derive loop bounds from the largest index the body touches, not from memory.
- [ ] I can say why `n` items have `n − 1` adjacent pairs, and why a window of `k` gives
      `n − k + 1`.
- [ ] I know the three reasons to iterate backwards.
- [ ] I never delete from a list while iterating forwards over it.
- [ ] I can quote seven latency numbers cold and use them to size a request in legs.
