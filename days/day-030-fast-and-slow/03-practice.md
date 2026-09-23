---
day: 30
track: practice
title: "Practice — Fast and slow pointers"
status: written
---

# Day 030 · Practice

**DSA topic:** Fast and slow pointers
**System design topic:** Indexes: how a database finds a row fast

---

## Code these, in this order

Four problems that are the same six lines in four costumes. **Before each one, say which costume it is
and what the "path" is** — what plays the role of "the next node".

Before each one, ask:

1. What is the step function? From here, where do I go next?
2. Can the path end, or does it go forever? That decides the loop condition.
3. Do I need only *whether* there is a loop, or *where* it starts?
4. What is the naive solution and what does it cost in space?

| # | Problem | Source | The costume, and what it is really testing |
|---|---|---|---|
| 1 | Middle of the Linked List | LeetCode 876 (Easy) | Two speeds, one pass. The condition order `fast and fast.next`, and which of the two middles. |
| 2 | Linked List Cycle | LeetCode 141 (Easy) | Detection. Give the hash-set answer with its space cost, then Floyd's. |
| 3 | Happy Number | LeetCode 202 (Easy) | The path is a function on integers. Note what the meeting **value** tells you. |
| 4 | Find the Duplicate Number | LeetCode 287 (Medium) | The path is `i → nums[i]`. The three constraints rule out every obvious approach, and the loop entry *is* the answer. |

### On problem 1, decide the convention first

Run your solution on `[1]`, `[1,2]`, `[1,2,3]`, `[1,2,3,4]`. Then answer:

1. Which of the two middles does your loop return on even lengths?
2. What single change gives the other one?
3. Which does LeetCode 876 want?
4. If you were splitting a list into two halves for a merge sort, which would you want and why?

Then deliberately reverse the condition to `while fast.next and fast` and run it on `[1,2]`. Read the
exact error and say why the order matters.

### On problem 2, write both and compare

Write the hash-set version first. State its cost out loud: `O(n)` time, `O(n)` space. Then write
Floyd's and state its cost.

Then produce the number that justifies it: at 10 million nodes, how much memory does each use? That
comparison is the reason the technique exists, and it is what you say in the interview.

### On problem 4, work out why the obvious answers are banned

The problem says: `n+1` values in the range `1..n`, one repeated, **do not modify the array**, use
**constant space**. For each of these, say which constraint rules it out:

1. Sort, then scan for adjacent equals.
2. A hash set of values seen.
3. A counting array of size `n+1`.
4. Negate `nums[abs(x)]` as a marker.
5. Binary search on the value range, counting how many are `≤ mid`.
6. Floyd's.

Number 5 is not ruled out — say its cost and why it is a legitimate second answer.

Then explain, in two sentences, why a repeated value creates a loop and why the loop's entry point is
the duplicate.

### The proof drill

Say each of these out loud, without looking:

1. Why must the fast pointer catch the slow one if there is a loop? (The answer is about a quantity
   that changes by exactly one.)
2. Why does the fast pointer move at 2 and not 3?
3. In the second phase, why do **both** pointers move at speed 1?
4. Why, when they first meet, has the slow pointer walked a whole number of loop-lengths?
5. What is the total number of steps, in terms of `μ` and `λ`?

Number 1 is the one you will actually be asked. Number 4 is the one that makes number 3 make sense.

### The break-it drill

Run each and say what goes wrong:

```python
# A
def find_duplicate(nums):
    slow = fast = 0
    while slow != fast:              # condition checked before any step
        slow = nums[slow]
        fast = nums[nums[fast]]
    return slow
```

```python
# B  (phase two)
slow = start
while slow != fast:
    slow = step(slow)
    fast = step(step(fast))          # still doubling
return slow
```

```python
# C
while fast.next and fast:
    ...
```

A exits immediately. B returns a point inside the loop that is not the entry, with no error. C raises.
Say which of the three is most dangerous and why.

### The costume drill

For each, say what the "path" is — what the step function does — and whether the path can end:

1. A linked list with a cycle.
2. `nums[i]` where every value is a valid index.
3. Sum of the squares of the digits.
4. A function that maps each user to the person who referred them.
5. Repeatedly halving a number and rounding down.

Number 5 is the one where there is always a loop, and a boring one. Say what it is.

### The middle-versus-length drill

Answer without running anything:

1. Two passes — count, then walk half — versus one pass with two speeds. Same complexity. Give the
   real reason to prefer one pass.
2. On an array, why would you ever use this instead of `len(items) // 2`?
3. What structure makes this technique not merely nicer but necessary?

### The index drill

Answer each in one or two sentences, out loud:

1. What is an index, physically, and why is it shallow?
2. Fanout of 500 — how many levels for ten million rows? For sixty billion?
3. Name five query shapes an index on one column can serve. Name one it cannot.
4. Why does `WHERE YEAR(created_at) = 2026` not use an index on `created_at`? Rewrite it.
5. An index on `(a, b)` — which of `a`, `b`, and `a AND b` does it serve?
6. What is a covering index, and what does `SELECT *` do to it?
7. At roughly what fraction of the table does a sequential scan beat an index scan, and why?
8. What does every extra index cost, in writes and in storage?
9. What does `CREATE INDEX CONCURRENTLY` buy you, and what does it cost?
10. Name three reasons a query is slow that are **not** a missing index.

Number 10 is the one that makes the difference in an interview.

### The plan-reading drill

For each plan fragment, say the diagnosis and the fix:

```
Seq Scan on orders  (actual time=0.021..112.4 rows=3 loops=1)
  Filter: (customer_id = 4217)
  Rows Removed by Filter: 999997
```

```
Seq Scan on users  (cost=... rows=1 width=...) (actual rows=480000 loops=1)
```

```
Sort  (actual time=...)  Sort Method: external merge  Disk: 52000kB
```

```
Index Scan using orders_pkey on orders (actual rows=1 loops=61)
```

The last one has `loops=61`. Say what that almost certainly means and where you would look for it.

### The arithmetic drill

From memory, in under two minutes:

- 1,000,000 rows at 200 bytes — table size, pages, and time for a sequential scan.
- The same lookup through a three-level B-tree — page reads and time. The ratio.
- Fanout 500 — rows covered at depths 2, 3 and 4.
- A table with eight indexes — writes per insert, and the rough slowdown.
- One index on a bigint column over a million rows — its size, and as a percentage of the table.
- The selectivity crossover — what fraction, and why random beats sequential below it.

### The design drill

You are given this table and these three queries. Decide the minimum set of indexes, and justify each.

```sql
CREATE TABLE orders (
    id           BIGSERIAL PRIMARY KEY,
    customer_id  BIGINT NOT NULL REFERENCES customers(id),
    status       TEXT   NOT NULL,          -- 'pending', 'shipped', 'delivered', 'cancelled'
    total        NUMERIC(12,2) NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL
);
```

1. `SELECT * FROM orders WHERE customer_id = ? ORDER BY created_at DESC LIMIT 20;`
2. `SELECT id, total FROM orders WHERE status = 'pending' ORDER BY created_at;`
3. `SELECT customer_id, SUM(total) FROM orders WHERE created_at >= ? GROUP BY customer_id;`

Then answer: which of your indexes is redundant with another? Which query would benefit from a
**partial** index, and why? And which one could be made an index-only scan, and what would you have to
change?

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the middle element in a single pass.*
   Ask which middle. Give the two-pass version and its cost. Then two speeds, and the reason one pass
   matters — not the constant factor, but that a stream has no second pass. Name the `fast and
   fast.next` ordering.

2. *This query is slow. How do you find out why, and what do you do about it?*
   Measure first. Say what you read in the plan and in what order. Then the six causes, at least three
   of which are not missing indexes. Then the B-tree explanation with the fanout number, then the cost
   of the index, then `CONCURRENTLY`.

3. *Why are you sure the fast pointer catches the slow one?*
   The gap shrinks by exactly one per step, so it cannot skip zero. Then the bound, `μ + λ`. Then why
   speed 3 breaks the argument. Ninety seconds.

---

## Before you move on

- [ ] I can state, in one sentence, why the two pointers must meet.
- [ ] I write `while fast and fast.next` in that order without thinking.
- [ ] I ask which of the two middles before writing the loop.
- [ ] I give the hash-set solution and its space cost before offering Floyd's.
- [ ] I can explain why a repeated value in an index-valued array creates a loop.
- [ ] In phase two I reset one pointer and move **both** at speed 1.
- [ ] I say "`EXPLAIN ANALYZE` first" before "add an index".
- [ ] I can name three causes of a slow query that are not a missing index.
- [ ] I know the left-prefix rule and can say why `(a, b)` does not serve `b`.
- [ ] I can quantify the write cost of an index, and I mention `CONCURRENTLY` unprompted.
- [ ] I can redraw the rho diagram and the B-tree fanout diagram from memory, in whatever tool I like.
