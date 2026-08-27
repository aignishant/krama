---
day: 28
track: practice
title: "Practice — Opposite ends: pair sums on a sorted array"
status: written
---

# Day 028 · Practice

**DSA topic:** Opposite ends: pair sums on a sorted array
**System design topic:** Joins, drawn

---

## Code these, in this order

Four problems on one skeleton. **For every one, state the completeness argument before writing code** —
not just why a move is safe, but why nothing is missed when the indices meet.

Before each one, ask:

1. Is it sorted? If not, what does sorting cost, and does it destroy anything I need?
2. `left < right` or `left <= right` — am I forming pairs, or filling positions?
3. What do I do on a hit: return, or record and move **both**?
4. Are duplicates possible, and does the problem want distinct values or distinct positions?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Two Sum II — Input Array Is Sorted | LeetCode 167 (Medium) | The skeleton, the completeness argument, and that the output is **1-indexed**. |
| 2 | Squares of a Sorted Array | LeetCode 977 (Easy) | Writing from the **back**, and `left <= right` rather than `<`. The `O(n)` answer versus the `O(n log n)` one-liner. |
| 3 | 3Sum | LeetCode 15 (Medium) | Fix one, two-pointer the rest — and three duplicate guards in three different places. |
| 4 | 3Sum Closest | LeetCode 16 (Medium) | The same skeleton tracking a best-so-far. Note that you can no longer stop early on a mismatch. |

### On problem 1, produce the proof

Before coding, write out the three sentences of the invariant argument:

1. What is true at the start?
2. Why is it still true after advancing `left`? (One sentence, and it must mention sortedness.)
3. Therefore, what does it mean when the indices meet with nothing found?

Then run your solution on `[3, 2, 4]` with target 6 and explain the empty result in terms of which
sentence stopped being true.

### On problem 2, do it both ways and time it

Write `sorted(x*x for x in nums)` first. Say its cost. Then write the two-pointer version.

Then answer:

1. Why can you not fill the output from the front?
2. Why is the loop `left <= right` here when it was `left < right` yesterday?
3. On `[-1, 0, 1]`, what does the `<` version return, and why does it look almost right?
4. At `n = 1,000,000`, roughly how many operations does each version do?

### On problem 3, break it three ways

Solve it, then delete each duplicate guard in turn and find the input that exposes it.

```python
three_sum([-1, 0, 1, 2, -1, -4])     # guard 1 missing -> which triple repeats?
three_sum([-2, 0, 0, 2, 2])          # guards 2 and 3 -> which triple repeats?
three_sum([0, 0, 0, 0])              # all three at once
```

Then say, for each guard, in one sentence: what repetition does it prevent, and why can the other two
guards not do its job?

### On problem 4, notice what changed

3Sum Closest looks like 3Sum and one thing is different: you cannot stop scanning when the sum is
wrong, because a wrong sum might still be the closest one. Say what that means for:

1. Where the `best` update goes relative to the comparison.
2. Whether you can still `break` out early, and on what condition.
3. Whether the duplicate guards are needed at all here. (They are not — say why.)

### The completeness drill

For each, give the one sentence that justifies discarding, and name what would break if the input were
unsorted:

1. Two-sum, total too small → advance `left`.
2. Two-sum, total too large → retreat `right`.
3. Count pairs at most `k` → `count += right - left`, then advance `left`.
4. Sorted squares → take the larger absolute value and write it at the back.

Number 3 is the one worth extra thought: why is it `right - left` and not `right - left + 1`?

### The variant drill

Take the nine-line skeleton and adapt it, without looking at the lesson, for each of these:

1. Return **all** distinct pairs summing to the target.
2. Return **how many** index pairs sum to at most the target.
3. Return the pair whose sum is **closest** to the target.
4. Return **true/false** only — does any pair sum to the target?
5. Given two sorted arrays, find one element from each summing to the target.

Number 5 is the one that changes shape: say where the two indices start and which way each moves, and
why the argument still holds.

### The row-count drill

Two tables:

```
  customers                     orders
  +----+------+                 +----+-------------+
  | id | name |                 | id | customer_id |
  +----+------+                 +----+-------------+
  | 1  | Asha |                 | 10 | 1           |
  | 2  | Ravi |                 | 11 | 1           |
  | 3  | Nita |                 | 12 | 2           |
  | 4  | Sam  |                 | 13 | NULL        |
  +----+------+                 +----+-------------+
```

Give the row count for each, from memory, in under thirty seconds total:

1. `INNER JOIN`
2. `LEFT JOIN`
3. `RIGHT JOIN`
4. `FULL OUTER JOIN`
5. `CROSS JOIN`
6. `LEFT JOIN`, then `WHERE o.id IS NOT NULL`
7. `LEFT JOIN`, then `GROUP BY c.id` with `COUNT(*)` — what does Nita get?
8. The same with `COUNT(o.id)` — what does Nita get?

Numbers 7 and 8 must differ. If they do not, re-read §3.

### The fan-out drill

`orders` has 10,000 rows with an average total of ₹2,000. `order_items` has 40,000 rows — four per
order on average.

1. What does `SELECT SUM(o.total) FROM orders o` give?
2. What does `SELECT SUM(o.total) FROM orders o JOIN order_items i ON i.order_id = o.id` give?
3. Why, in one sentence?
4. Write the corrected version.
5. If the average were 1.3 items per order instead of 4, why would this bug be *more* dangerous?

### The ON-versus-WHERE drill

Predict the row count of each against the four-customer example, then say which is the bug:

```sql
-- A
SELECT c.name, o.id FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NOT NULL;

-- B
SELECT c.name, o.id FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id AND o.id > 11;

-- C
SELECT c.name, o.id FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id > 11;
```

B and C differ by moving one condition. Say what each returns and which one silently stopped being a
left join.

### The join-algorithm drill

Answer each in one or two sentences:

1. Name the three join algorithms and say when each is chosen.
2. Which one is the two-pointer walk in disguise?
3. What happens to a nested loop join when the right side's join column is not indexed?
4. What happens to a hash join when the build side does not fit in `work_mem`?
5. 10,000 customers against 1,000,000 orders — comparisons with and without an index?
6. In `EXPLAIN`, what does a large gap between estimated and actual rows usually mean?

### The anti-join drill

Write "customers who have never ordered" three ways. Then say:

1. Which is usually fastest, and why?
2. Which one returns **nothing at all** if `orders.customer_id` contains a single `NULL`, and why?
3. Why is that the nastiest of the three bugs?

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find two numbers in a sorted array that add up to the target.*
   Confirm sortedness and the index base. Brute force and its cost. The move rules **with their
   reasons**. Then the invariant, in three sentences, unprompted — that is what today is for. Then
   `O(n)` / `O(1)` and the unsorted alternative.

2. *What is the difference between an inner join and a left join?*
   Define by what happens to unmatched rows, then give the four row counts from a concrete example.
   Raise fan-out before being asked. Name the `COUNT(*)` trap and the `ON`-versus-`WHERE` trap.

3. *How do you know your two-pointer scan didn't miss a pair?*
   The invariant, stated precisely, and the single place sortedness is used. Finish with what happens
   to the argument on unsorted input — it returns nothing, with no error, which is the dangerous kind
   of wrong.

---

## Before you move on

- [ ] I can state the invariant in three sentences without preparation.
- [ ] I know the exactly one place sortedness is used in the argument.
- [ ] On a hit I move **both** indices, then skip repeats of both values.
- [ ] I can say what each of 3Sum's three duplicate guards prevents, with its input.
- [ ] I check the index base before writing the return statement.
- [ ] I choose `<` or `<=` from what the problem is covering, not from habit.
- [ ] I can give the four join row counts from a small example in under thirty seconds.
- [ ] I raise fan-out before being asked, and can quantify the double-counting bug.
- [ ] I know `COUNT(o.id)` from `COUNT(*)`, and `ON` from `WHERE`, on an outer join.
- [ ] I can redraw the elimination diagram and the four-join diagram from memory, in whatever tool I
      like.
