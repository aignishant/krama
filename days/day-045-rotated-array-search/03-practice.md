---
day: 45
track: practice
title: "Practice — Search in a rotated sorted array"
status: written
---

# Day 045 · Practice

**DSA topic:** Search in a rotated sorted array
**System design topic:** Encapsulation

---

## Code these, in this order

Do the minimum before the search. Finding the break point is the easier half of the idea, and it
makes the harder half obvious.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Find Minimum in Rotated Sorted Array | LeetCode 153 (Medium) | The break point, and comparing against `nums[high]` rather than `nums[low]`. |
| 2 | Search in Rotated Sorted Array | LeetCode 33 (Medium) | Discarding on a *range* instead of a single comparison. |
| 3 | Search in Rotated Sorted Array II | LeetCode 81 (Medium) | Whether you can say "O(n) worst case" and explain why it is unavoidable. |
| 4 | Find Minimum in Rotated Sorted Array II | LeetCode 154 (Hard) | The same duplicate problem on the cleaner cousin — and the one-line guard. |

### On problem 1, break your own solution first

Write the version that compares `nums[mid]` against `nums[low]` and run it on `[1, 2, 3, 4, 5]`. It
returns 5. Say why in one sentence before you fix it: on an un-rotated array every middle is bigger
than the first element, so `low` marches to the end. Then write the `nums[high]` version and confirm
the same input gives 1.

### On problem 2, say the sentence before the code

Out loud: *at least one half is properly sorted, because there is exactly one break point and one
point cannot be in two halves.* Then write it. Then run the three inputs that decide correctness — an
un-rotated array, a break at the very last position, and a single-element array. If you needed a
special case for any of them, delete it and find the real bug.

### On problem 3, do not patch — understand

Before writing the duplicate version, hold `[3, 1, 3, 3, 3]` and `[3, 3, 3, 1, 3]` side by side and
check what `nums[0]`, `nums[2]` and `nums[4]` say in each. They are identical. That is the proof that
no comparison can decide, and it is what you say in the interview rather than "duplicates make it
slower". Then add the one-line guard and time it on `[1] * 100000 + [2]`.

### On problem 4, notice what the guard becomes

Here the guard is `high -= 1` alone, not `low += 1; high -= 1`. Work out why: when
`nums[mid] == nums[high]`, you cannot rule out the middle, but you can safely discard *one* copy of
the value at the right end, because if it were the unique minimum the middle would equal it anyway.
This is the hardest reasoning in the phase; if it does not land in ten minutes, write the O(n) scan,
say it is O(n), and come back to it.

### The which-half drill

For each array and midpoint, say which half is sorted and how you know, in under five seconds each:

1. `[4, 5, 6, 7, 0, 1, 2]`, mid = 3.
2. `[6, 7, 0, 1, 2, 4, 5]`, mid = 3.
3. `[1, 2, 3, 4, 5, 6, 7]`, mid = 3.
4. `[2, 1]`, mid = 0.
5. `[5]`, mid = 0.

Numbers 3, 4 and 5 are the ones that catch people. Say which comparison operator each depends on.

### The discard-proof drill

For each, say whether the discard is justified and give the reason as a range statement:

1. Left half sorted, runs 240 to 330, target 88 — discard which half?
2. Right half sorted, runs 1 to 239, target 300 — discard which half?
3. Left half sorted, runs 4 to 7, target 7 — careful, where is `mid`?
4. Right half sorted, runs 0 to 2, target 0 — careful, where is `mid`?

Cases 3 and 4 are about whether `mid` is inside or outside your interval. Say which boundary is
inclusive on each side and why.

### The encapsulation audit

Take this class and list every way a caller can break it. There are at least four:

```python
class Cart:
    MAX_ITEMS = 20

    def __init__(self):
        self.items = []
        self.total = 0

    def add(self, item, price):
        if len(self.items) < self.MAX_ITEMS:
            self.items.append(item)
            self.total += price
```

1. Name the invariants the class is trying to hold — there are two.
2. Name four distinct ways a caller breaks one of them without any exception being raised.
3. Rewrite it so none of the four is possible, and say which change fixes which.
4. Then answer: should `total` be stored at all, or computed? Give the trade-off in one sentence.

### The getter drill

For each, say whether a getter is right, or whether a behaviour method is missing — and if the
latter, name the method:

1. `order.get_total()`, used to print a receipt.
2. `order.get_status()`, used as `if order.get_status() == "PENDING": order.set_status("PAID")`.
3. `account.get_balance()`, used to display on a statement.
4. `account.get_balance()`, used as `if account.get_balance() >= amount: ...`.
5. `cart.get_items()`, used to render the list in the checkout view.
6. `cart.get_items()`, used as `cart.get_items().append(x)`.

Say the one-line test that decides all six.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Search a rotated sorted array in O(log n).*
   The one-break-point structure, the "at least one half is sorted" fact, the range-based discard, the
   `<=` in the sortedness test, and the duplicates clarifying question.

2. *Why make a field private if you are going to add a getter anyway?*
   The invariant, the call-site multiplication with a number, and then the real answer — that the
   getter is often also wrong and the behaviour is what should be exposed.

3. *Your rotated search returns −1 for a value that is in the array. Where is the bug?*
   Two candidates: a plain `nums[mid] < target` comparison instead of a range check, or `<` instead of
   `<=` in the sortedness test. Say which input exposes each.

---

## Before you move on

- [ ] I wrote find-minimum comparing against `nums[high]` and can say what breaks with `nums[low]`.
- [ ] I solved LeetCode 33 with no special case for the un-rotated array.
- [ ] I can hold up `[3, 1, 3, 3, 3]` and `[3, 3, 3, 1, 3]` and explain why duplicates force O(n).
- [ ] I answered all five which-half drills, including the one-element case.
- [ ] I found at least four ways to break the `Cart` class and fixed each one.
- [ ] I can state the one-line test that decides whether a getter or a method is right.
- [ ] I answered all three questions above out loud.
