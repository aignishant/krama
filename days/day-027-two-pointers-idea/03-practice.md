---
day: 27
track: practice
title: "Practice — Two pointers: the idea"
status: written
---

# Day 027 · Practice

**DSA topic:** Two pointers: the idea
**System design topic:** SQL you must know for interviews

---

## Code these, in this order

Four problems where two indices replace a nested loop. **For every one, state the elimination argument
out loud before writing code** — the sentence that says why discarding a value is safe. If you cannot
produce it, you have a remembered move rather than an understood one.

Before each one, ask:

1. Is the input sorted? If not, can I sort it, and what does that cost me?
2. Which of the three shapes — opposite ends, same direction, fast and slow?
3. What does each move eliminate, and why is that safe?
4. Is it `left < right` or `left <= right`, and why?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Two Sum II — Input Array Is Sorted | LeetCode 167 (Medium) | The base case, and whether you notice it wants **1-indexed** positions. |
| 2 | Container With Most Water | LeetCode 11 (Medium) | A *different* elimination argument. Moving the taller line is the wrong move, and you should be able to say why in one sentence. |
| 3 | 3Sum | LeetCode 15 (Medium) | That it is not three pointers. Fix one, two-pointer the rest — and the duplicate-skipping is most of the work. |
| 4 | Trapping Rain Water | LeetCode 42 (Hard) | The two-pointer version, after you have written the prefix-max one. The argument here is genuinely subtle and worth the hour. |

### On problem 1, prove it to yourself

Before coding, take `[2, 7, 11, 15]` with target 18 and say each step out loud including the reason:

```
2 + 15 = 17 < 18  ->  move left, because ...
7 + 15 = 22 > 18  ->  move right, because ...
7 + 11 = 18       ->  found
```

Fill in both "because" clauses without looking. Then run your solution on `[3, 2, 4]` with target 6
and explain why it returns nothing.

### On problem 2, get the rule wrong on purpose

Write the version that moves the **taller** line and run it on `[1,8,6,2,5,4,8,3,7]`. You should get 8
instead of 49. Then say, in one sentence, why moving the taller line can never help.

The sentence you want is about which of the two lines determines the depth, and what happens to the
width.

### On problem 3, do the duplicates properly

Solve it, then test on `[0,0,0,0]` and on `[-2,0,0,2,2]`. Both are duplicate-heavy on purpose.

Then answer:

1. Why must you sort first, given the problem does not ask for sorted output?
2. Where exactly do the three duplicate-skips go — the outer element, `left`, and `right`?
3. What is the total cost, and why is it not `O(n³)`?
4. Why does no three-pointer version exist?

### The three-shapes drill

For each problem, name the shape — **opposite ends**, **same direction**, or **fast and slow** — in
under five seconds:

1. Check whether a string is a palindrome.
2. Move all zeros to the end.
3. Find whether a linked list has a cycle.
4. Find two numbers in a sorted array that sum to a target.
5. Remove duplicates from a sorted array in place.
6. Find the middle node of a linked list in one pass.
7. Merge two sorted arrays into the first, in place.
8. Longest substring without repeating characters.

Number 7 is opposite-ends in a disguise — say which end and why. Number 8 is a window, which is the
same-direction shape with the pair treated as a range.

### The elimination drill

This is the exercise that matters most today. For each, write the one sentence that justifies the
move:

1. Two-sum sorted, total too small → move `left`. Why is `nums[left]` finished?
2. Two-sum sorted, total too large → move `right`. Why?
3. Container with most water → move the shorter line. Why can the taller one never help?
4. Trapping rain water → move whichever side has the smaller wall. Why is that side's answer already
   determined?

Number 4 is the hardest and it is worth the effort. The answer involves knowing that the *other*
side's wall is at least as tall, so it cannot be the limiting factor.

### The measurement drill

Run this and read the ratio column.

```python
import time

def two_pointer(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target: return [left, right]
        if s < target: left += 1
        else: right -= 1
    return []

def brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target: return [i, j]
    return []

for n in (1000, 5000, 10000):
    arr = [2 * i for i in range(n)]      # all even
    target = 1                            # odd, so no pair exists
    s = time.perf_counter(); two_pointer(arr, target); t1 = time.perf_counter() - s
    s = time.perf_counter(); brute(arr, target);       t2 = time.perf_counter() - s
    print(f"n={n:>6}  {t1:.6f}s  {t2:.4f}s  ratio {t2/t1:>7.0f}x")
```

Then answer:

1. Why is the target chosen to be impossible?
2. The ratio roughly doubles each time `n` doubles. What does that tell you, and why is it not
   constant?
3. Predict the two times at `n = 100,000` before running it.

### The sorted-or-not drill

For each, say whether you would use two pointers or a hash map, and why:

1. Sorted array, return positions in that array.
2. Unsorted array, return original positions.
3. Unsorted array, return the two values, memory is very tight.
4. Sorted array, but you must not modify it and cannot allocate.
5. A stream of numbers arriving one at a time.

Number 5 is the one that rules out two pointers entirely — say why.

### The SQL drill

Write each query without looking anything up. Tables: `customers(id, name, city)`,
`orders(id, customer_id, amount, status, created_at)`.

1. All orders over ₹5,000, newest first.
2. The number of orders per customer.
3. The number of *completed* orders per customer, only for customers with more than three.
4. The top five customers by total completed spend, with their names.
5. Customers who have never placed an order.
6. The average order value per city.
7. How many distinct customers ordered in the last 30 days.
8. The three most recent orders for each customer.

Number 8 needs a window function. Numbers 3 and 6 need you to decide `WHERE` versus `HAVING`
correctly.

### The execution-order drill

Answer without running anything:

1. Why does `SELECT SUM(amount) AS total FROM orders WHERE total > 100` fail?
2. Why does `ORDER BY total DESC` work in the same query?
3. Why can `WHERE` not contain `SUM(amount)`?
4. What is the difference between `COUNT(*)` and `COUNT(discount_code)`?
5. `WHERE status <> 'cancelled'` — does it return rows where status is `NULL`? Why?
6. Two customers have the same total. Why might `LIMIT 5` return different rows on different runs?

### The slow-query drill

You run `EXPLAIN ANALYZE` and see:

```
Seq Scan on orders  (cost=0.00..18334.00 rows=1 width=64)
                    (actual time=0.021..112.4 rows=3 loops=1)
  Filter: (customer_id = 4217)
  Rows Removed by Filter: 999997
```

Say, in order: what this is telling you, what you would do, what you would expect to see afterwards,
and roughly what the new time would be.

Then say two other things you look for in a plan besides `Seq Scan`.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Can you do better than the nested loop?*
   Ask whether it is sorted. State the brute force and its cost. Name the shape. **Give the
   elimination argument before the code.** Then the pair-table picture — each move deletes a row or a
   column, and there are only `n` of each. Finish with the hash-map alternative and when you would
   prefer it.

2. *Write a query for the top five customers by total spend.*
   Two clarifying questions first. Say the shape before the syntax. Explain why the status filter is
   in `WHERE` and not `HAVING`, and that it changes the answer rather than just the speed. Mention the
   tie-breaker and the excluded-customers point unprompted. Offer the index.

3. *Why is it safe to move the left pointer when the sum is too small?*
   This is the whole day. Smallest value still in play, already paired with the largest available, so
   that is its best case — if the best case falls short, nothing works, so discard it and every pair
   containing it. And say what the argument depends on: sortedness.

---

## Before you move on

- [ ] I ask "is it sorted?" before considering two pointers.
- [ ] I state the elimination argument out loud before writing the move.
- [ ] I can draw the pair table and show what one move deletes.
- [ ] I know the three shapes and can classify a problem into one in five seconds.
- [ ] I write `left < right` for pair problems and can say why not `<=`.
- [ ] I can give the two-pointers-versus-hash-map comparison as a table, not a preference.
- [ ] I can write the top-five query in two minutes without looking anything up.
- [ ] I can state the execution order and the three things it explains.
- [ ] I know `WHERE` filters rows and `HAVING` filters groups, and that the choice changes the answer.
- [ ] I can redraw the pair-table diagram and the clause-order diagram from memory, in whatever tool I
      like.
