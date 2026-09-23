---
day: 49
track: practice
title: "Practice — Peak finding, and searching data that is structured but not sorted"
status: written
---

# Day 049 · Practice

**DSA topic:** Peak finding, and searching data that is structured but not sorted
**System design topic:** Composition over inheritance

---

## Code these, in this order

One rule today: **for every problem, say the invariant and the discard proof out loud before writing a
line.** These problems have no target and no monotone question — the proof is all you have, and if you
cannot state it you are guessing.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Peak Index in a Mountain Array | LeetCode 852 (Medium) | The rule, with the answer guaranteed unique so nothing can distract you. |
| 2 | Find Peak Element | LeetCode 162 (Medium) | The same code with the guarantee removed — and whether you accept a non-unique answer. |
| 3 | Find Minimum in Rotated Sorted Array | LeetCode 153 (Medium) | The mirror: a valley. Re-derive it as local structure, not as a rotation trick. |
| 4 | Find a Peak Element II | LeetCode 1901 (Medium) | The 2D version, and whether you search columns and take each column's maximum row. |

### On problem 1, do the proof first

Before typing: *if it rises to the right of the middle, either it climbs to the end — and the last
element beats the imaginary negative infinity beyond it — or it turns over somewhere, and the turning
point is a peak. Either way a peak exists to the right.* Then write four lines. Then confirm the
guarantee that makes the answer unique changes nothing about the code.

### On problem 2, resist checking your answer against the maximum

Run it on `[1, 3, 2, 4, 7, 9, 5, 6, 2]`. It returns index 7, value 6 — and 9 is in the array. That is
correct. Write the `is_peak` helper from §5 and use it to check your answers, rather than comparing
against `max(nums)`. If you find yourself wanting the maximum, say out loud why that is O(n) and
cannot be beaten.

### On problem 3, do not look at day 045

Re-derive it as a valley: the minimum is the one element smaller than both neighbours, with the
wrap-around counted. Compare `nums[mid]` against `nums[hi]`, and say why comparing against `nums[lo]`
returns the maximum on an un-rotated array. Then notice you have written today's code with one
comparison flipped.

### On problem 4, get the axis right

Search over the **columns**, and inside each candidate column take the row holding that column's
largest value. That element already beats its up and down neighbours for free, which is what collapses
the problem back to one dimension. Write the version that scans the *row* instead and see it fail —
then say precisely why the discard is not justified in that version.

### The proof drill

Say each out loud, in under thirty seconds:

1. Why does every array have at least one peak?
2. Why does "it rises to the right" guarantee a peak to the right? Name the two cases and the fact
   that rules out a third.
3. Why is `hi = mid` and not `hi = mid - 1` in the falling branch?
4. Why is `mid + 1` always a valid index?
5. Why is the loop condition strictly `<`?

### The breakage drill

Produce each failure yourself and record what happens — a crash with a named exception, a silent wrong
answer, or a hang:

1. `while lo <= hi` with `hi = mid`, on `[1, 2, 3]`.
2. `hi = mid - 1` in the falling branch, on `[1, 2, 1, 3, 5, 6, 4]`.
3. Comparing with `nums[mid - 1]` instead of `nums[mid + 1]`, on `[1, 2]`.
4. `[1, 2, 2, 2, 1]` on the correct solution — what does it return, and is it a peak?

Number 4 is not a bug in your code. Say whose problem it is and what you would have asked for.

### The sortedness drill

For each, say whether binary search applies, and what the discard proof is:

1. A sorted array, find a target.
2. A rotated sorted array, find a target.
3. An unsorted array, find any peak.
4. An unsorted array, find the maximum.
5. An unsorted array of distinct values, find the third largest.
6. A monotone yes-or-no question over a range of capacities.

Two of these six have no discard proof. Name them and say what the cost is instead.

### The hierarchy refactor drill

Take this and rework it out loud in five minutes:

```python
class Notification: ...
class EmailNotification(Notification): ...
class SmsNotification(Notification): ...
class UrgentEmailNotification(EmailNotification): ...
class UrgentSmsNotification(SmsNotification): ...
class ScheduledEmailNotification(EmailNotification): ...
class ScheduledSmsNotification(SmsNotification): ...
```

1. Name the axes. How many are there, and what is the tell in the class names?
2. Which axis is the identity and which are things the object *has*?
3. Name each extracted component as a capability, not as a variant.
4. Count the classes now, and after adding a third channel, and after adding a fourth delivery
   timing.
5. Name the duplication that exists in the current version and where it goes.
6. Write the construction line for an urgent SMS.
7. Say what you gave up.

### The count drill

Fill in the table from memory, then check it:

```
axes                              inheritance      composition
3 channels                        ?                ?
3 channels x 3 timings            ?                ?
3 x 3 x 2 (with attachment)       ?                ?
adding a 4th channel              ? new classes    ? new classes
```

### The still-inheritance drill

For each, say compose or inherit, with the one-sentence reason:

1. `CardDeclined` and `PaymentError`.
2. `ElectricCar` and `Car`, in a system that also varies by size.
3. `JsonFormatter` and `logging.Formatter`.
4. `PremiumSubscriber` and `Subscriber`, where the difference is a discount rate.
5. `RetryingHttpClient` and `HttpClient`.
6. `TimestampMixin` on four unrelated model classes.

Say the one property shared by every "inherit" answer.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find a peak element in O(log n).*
   Deal with the sortedness objection first, confirm the two conventions, state that an answer always
   exists, give the rule with its proof in one breath, and close on the peak-versus-maximum contrast.

2. *Refactor this class hierarchy. Why is your version better?*
   Name the axes from the class names, pick the identity, name the capability, give the count both
   ways, name the duplication removed, and concede the cost.

3. *Why does binary search work here? There is no order.*
   The general statement — binary search needs a discard proof, not sortedness — then this problem's
   proof, then two other days where the proof was something else.

---

## Before you move on

- [ ] I stated the discard proof before writing code on all four problems.
- [ ] I checked my peak answers with `is_peak`, not against `max(nums)`.
- [ ] I produced all four breakages and can say which is a crash, which is silent, and which hangs.
- [ ] I can say why finding the maximum is O(n) and cannot be beaten.
- [ ] I refactored the notification hierarchy and gave the class count for four axes both ways.
- [ ] I can name the property shared by every case where inheritance is still right.
- [ ] I answered all three questions above out loud.
