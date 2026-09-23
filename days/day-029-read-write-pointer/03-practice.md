---
day: 29
track: practice
title: "Practice — Same direction: the read pointer and the write pointer"
status: written
---

# Day 029 · Practice

**DSA topic:** Same direction: the read pointer and the write pointer
**System design topic:** Normalisation and when to break it

---

## Code these, in this order

Four problems on the same-direction skeleton, chosen so that each one uses a different sub-shape.
**Before writing any of them, say which sub-shape it is**: filter, compare-against-what-you-kept,
partition by swapping, or walk from the back.

Before each one, ask:

1. In place? Do I return a count, or is the array itself checked?
2. Does the relative order of the survivors matter? Of the discarded group?
3. Am I comparing against the current element, or against something I already kept?
4. What happens on the empty input, and on one element?

| # | Problem | Source | Sub-shape, and what it is really testing |
|---|---|---|---|
| 1 | Remove Duplicates from Sorted Array | LeetCode 26 (Easy) | Compare-against-what-you-kept. `nums[write - 1]`, and the empty guard that silently returns 1 without it. |
| 2 | Remove Duplicates from Sorted Array II | LeetCode 80 (Medium) | The same, at `write - 2`. Should be a one-character change. If it is a rewrite, problem 1 compared against the wrong thing. |
| 3 | Sort Colors | LeetCode 75 (Medium) | Partition, three pointers. The whole question is why `mid` advances on a 0 and not on a 2. |
| 4 | Backspace String Compare | LeetCode 844 (Easy) | Walk from the back. Easy with `O(n)` space; the question is the `O(1)` version. |

### On problem 1, find the silent bug

Write it, then delete the empty guard and run it on `[]`.

```python
def remove_duplicates(nums):
    write = 1                       # no empty check
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write

print(remove_duplicates([]))
```

It returns `1`, with no exception. Say why the loop never runs, why `nums[write - 1]` is therefore
never evaluated, and why that makes this worse than a crash.

### On problems 1 and 2, prove the habit

Solve problem 1 comparing against `nums[write - 1]`. Then solve problem 2 by changing **one
character**.

Then write the deliberately wrong version and find the input that catches it:

```python
def keep_at_most_two(nums):
    write = 0
    for read in range(len(nums)):
        if write < 2 or nums[read] != nums[read - 2]:      # read, not write
            nums[write] = nums[read]
            write += 1
    return write

a = [1, 1, 1, 2, 2, 3]
k = keep_at_most_two(a)
print(k, a[:k])          # 4 [1, 1, 2, 3]   — a 2 has been LOST
```

Then check that it gives the *right* answer on `[1, 1, 1, 1, 2, 3]`. That is the point: the wrong
version passes the input you would naturally try.

Then generalise to `keep_at_most_k` and confirm `k = 1` reproduces problem 1.

### On problem 3, break it and find the input yourself

Write the version that advances `mid` after swapping in a 2. Then, without looking anything up, find
an input of length 3 that it gets wrong.

```python
elif nums[mid] == 2:
    nums[mid], nums[high] = nums[high], nums[mid]
    high -= 1
    mid += 1              # the bug
```

Try `[2, 0, 1]` first. It works — which is why this bug survives. Now try `[1, 2, 0]` and `[2, 1, 2]`.

Then answer:

1. Why is advancing `mid` **correct** in the `0` branch and **wrong** in the `2` branch?
2. Why is the loop `mid <= high` and not `mid < high`?
3. Why does the loop terminate, given that `mid` sometimes stands still?
4. What are the four regions of the array, and what is true of each?

### On problem 4, do it twice

Write the easy version — build both strings with a list and `join`, then compare. State its cost.

Then write the `O(1)`-space version walking backwards with a skip count, and answer:

1. Why can you not decide, going forwards, whether a character survives?
2. Why can you, going backwards?
3. What goes wrong if you use `zip` instead of `zip_longest`? Give an input.
4. Where else have you seen "go in the direction where the answer is already determined"?

### The invariant drill

For each, state the invariant in one sentence and say what it makes safe:

1. The filter skeleton — `write` and `read`.
2. Dedupe — what does `items[0:write]` hold at any moment?
3. Sort Colors — name the four regions and what is true of each.
4. Merge sorted arrays from the back ([day 018](../day-018-arrays-revision/README.md)) — why can the
   write index never collide?

### The stability drill

Run this and predict the output first:

```python
def partition_even_odd(nums):
    write = 0
    for read in range(len(nums)):
        if nums[read] % 2 == 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
    return write

a = [3, 1, 2, 4]
print(partition_even_odd(a), a)
```

Then answer:

1. Which group kept its order, and which did not? Why?
2. When would that matter, and when would it not?
3. If both groups must keep their order, what does that cost you?
4. Which of the copy version and the swap version does more writes, and on what kind of input?

### The sub-shape drill

Classify each in under five seconds, and name the comparison:

1. Move all zeros to the end.
2. Remove every occurrence of a value.
3. Remove duplicates from a sorted array.
4. Keep each value at most three times.
5. Sort an array of 0s, 1s and 2s.
6. Partition an array around a pivot.
7. Compare two strings with backspaces.
8. Merge a sorted array into the tail of another.
9. String compression, `aabcccccaaa` to `a2b1c5a3`.

Numbers 6 and 5 are the same shape at different widths. Numbers 7 and 8 both run backwards, for the
same reason.

### The cost drill

State time and space, counting out loud, for each:

1. The filter skeleton.
2. `keep_at_most_k`.
3. Sort Colors.
4. Backspace compare, both versions.
5. Removing duplicates with `del nums[i]` inside a loop.

For number 5, give the number of element moves at `n = 100,000` and compare it with number 1.

### The normalisation drill

Here is a table somebody actually wrote. Normalise it to 3NF, saying which form each fix satisfies:

```
  bookings
  +----+-----------+--------------+---------------+-----------+---------+-----------+
  | id | guest_name| guest_email  | guest_city    | room_nums | nights  | room_type |
  +----+-----------+--------------+---------------+-----------+---------+-----------+
  | 1  | Asha      | asha@x.com   | Coimbatore    | "12, 14"  | 3       | "AC, AC"  |
  | 2  | Ravi      | ravi@x.com   | Erode         | "7"       | 1       | "Non-AC"  |
  +----+-----------+--------------+---------------+-----------+---------+-----------+
```

Then answer:

1. Which column breaks 1NF, and what does that make impossible?
2. Once you have a `booking_rooms` table keyed on `(booking_id, room_num)`, which column breaks 2NF?
3. Which column depends on another non-key column, breaking 3NF?
4. Which column should stay duplicated on purpose, and why is it not a violation?

Number 4 is the rate charged per night. Say why it must be stored on the booking.

### The denormalisation drill

For each, say **normalise** or **denormalise**, and give the deciding number or reason:

1. A post's comment count, read 3,700 times a second and written 3.5 times a second.
2. A customer's current address, needed on every order display.
3. The price a customer paid, shown on an old invoice.
4. A user's display name, shown on every one of their 10,000 comments.
5. A daily revenue total for a dashboard that would otherwise scan 50 million rows.
6. An order's total, derivable by summing its items.

Numbers 3 and 6 are interesting for opposite reasons. Say why.

### The three-parts drill

Any denormalised copy has three parts. For a post's `comment_count`, write out all three:

1. The copy itself — what column, what type?
2. What maintains it — name three options and pick one, with a reason.
3. What detects drift — write the reconciliation query, and say what it should log.

If you cannot write part 3, say out loud what you would do instead.

### The slow-page drill

*"This page does eight joins and it's slow. Do you denormalise?"*

Say the three things you would check **before** touching the schema, and for each one say what the fix
would be. Then say when you would actually reach for denormalisation, and what you would build
alongside it.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Remove duplicates in place and return the new length.*
   Contract questions. Name the shape. State the invariant — `write` never overtakes `read` — and say
   what it makes safe. Say you compare against `nums[write - 1]` and **why that specific choice**.
   Finish with `O(n)`/`O(1)`, and what `write` means at the end.

2. *When would you deliberately duplicate data across tables?*
   3NF in one sentence, the three anomalies by name, then your default. Then the exception with the
   ratio: 265 to 1, four cores against 3.5 writes a second. Distinguish the snapshot from the copy.
   Finish with the reconciliation job, unprompted.

3. *Sort an array of 0s, 1s and 2s in one pass.*
   Four regions, three pointers. The whole answer is why `mid` advances on a 0 and not on a 2 — what
   is known about the value coming back from each end. Then termination, then `O(n)`/`O(1)`, then
   mention counting sort and why the problem forbids it.

---

## Before you move on

- [ ] I can state the `write <= read` invariant and say exactly what it makes safe.
- [ ] I compare against `items[write - 1]`, not `items[read - 1]`, without thinking about it.
- [ ] I can turn dedupe into keep-at-most-`k` by changing one character.
- [ ] I write the empty guard on anything that pre-keeps element 0.
- [ ] I know the copy version is stable and the swap version is not, and can show it.
- [ ] I can say why `mid` does not advance on a 2, and name an input that proves it.
- [ ] I can define 3NF in one sentence and name all three anomalies.
- [ ] I decide denormalisation with a read-to-write ratio, not with taste.
- [ ] I can tell a snapshot from a copy, and I never denormalise without a reconciliation job.
- [ ] I can redraw the read/write gap diagram and the four-regions diagram from memory, in whatever
      tool I like.
