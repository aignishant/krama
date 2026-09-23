---
day: 46
track: practice
title: "Practice — Binary search on the answer"
status: written
---

# Day 046 · Practice

**DSA topic:** Binary search on the answer
**System design topic:** Inheritance and its costs

---

## Code these, in this order

For every one of these, **write the three things down before the loop**: the answer range with a
reason for each end, the `works(x)` function, and the sentence saying why it is monotone. The search
loop is then copied unchanged from the previous problem.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Koko Eating Bananas | LeetCode 875 (Medium) | The friendliest entry: bounds of 1 to max, and ceiling division. |
| 2 | Capacity To Ship Packages Within D Days | LeetCode 1011 (Medium) | Bounds of `max` to `sum`, and the day counter starting at one. |
| 3 | Split Array Largest Sum | LeetCode 410 (Hard) | That a problem which reads like dynamic programming is this instead. |
| 4 | Minimum Number of Days to Make m Bouquets | LeetCode 1482 (Medium) | A feasibility check with a run-length rule inside it. |

### On problem 1, get the bounds right and say why

`lo = 1`, not 0 — a speed of zero never finishes, and in code it raises
`ZeroDivisionError: integer division or modulo by zero`. `hi = max(piles)` — at that speed every pile
takes exactly one hour, so `len(piles)` hours, which is the fastest anything can be. Prove to
yourself that no bigger `hi` helps by checking `hours_needed(max(piles))` equals `hours_needed(10**9)`.

Then get the ceiling right: `(pile + k - 1) // k`, because a part-eaten pile still costs a whole
hour. Check it on `pile = 7, k = 3`: three hours, not two.

### On problem 2, test the counter

Write `days_needed` on its own and check three things before the search exists: `[1,2,3,4,5]` with
capacity 5 gives 4, with capacity 15 gives 1, and with capacity 100 gives 1. Then deliberately change
`days` to start at 0 and re-run all three — you get 3, 0 and 0. Say the one-line reason.

### On problem 3, notice what changed

Nothing. Rename `capacity` to `limit` and `days` to `parts`, and the code is character-for-character
problem 2. Do problem 3 without looking at problem 2, then diff them. If they differ anywhere except
the names, one of them is wrong.

### On problem 4, the check has structure inside it

The feasibility check is not a running total this time — it counts *runs* of consecutive bloomed
flowers of length `k`. Write it separately and test it before searching. Then handle the impossible
case: if `m * k > len(bloomDay)` there is no answer at all, and that is the one problem in this set
with a genuine not-found branch. Say why the others do not have one.

### The three-things drill

For each phrasing, produce the answer range with a reason for each end, the `works` function in one
sentence, and the monotonicity sentence — under sixty seconds each, out loud:

1. Smallest ship capacity to clear packages in d days.
2. Slowest eating speed to finish piles in h hours.
3. Smallest largest-part-sum when splitting into k contiguous parts.
4. Largest minimum distance when placing c cows in n stalls.
5. Smallest number of days until m bouquets of k adjacent flowers can be made.

Number 4 is the maximisation form. Say which of the two routes you would take and why.

### The bounds drill

For each, say whether the bounds are correct, wasteful, or broken — and what the symptom is:

1. `lo, hi = 0, sum(weights)` for ship capacity.
2. `lo, hi = 1, max(piles)` for eating speed.
3. `lo, hi = max(weights), max(weights) * len(weights) // 2` for ship capacity.
4. `lo, hi = 1, 10**18` for eating speed.
5. `lo, hi = min(nums), sum(nums)` for split-array largest sum.

For the broken ones, say what the function returns and why no exception is raised.

### The monotonicity drill

For each phrasing, say monotone or not — and if not, why binary search on the answer is the wrong
tool:

1. "The smallest capacity such that it takes **at most** d days."
2. "The smallest k such that **exactly** k groups can be formed."
3. "The smallest number of workers such that the total wage bill is under ₹X, where extra workers cut
   overtime."
4. "The largest minimum gap between any two chosen positions."
5. "The smallest window size such that every value appears **at least** twice."

### The hierarchy audit

Take this and answer five questions about it:

```python
class Employee:
    def pay(self): ...
    def annual_review(self): ...

class Manager(Employee):
    def approve_leave(self, request): ...

class Contractor(Employee):
    def annual_review(self):
        raise NotImplementedError("contractors have no annual review")
```

1. Which of the three named failures does `Contractor` demonstrate? Give the exact symptom a caller
   will show.
2. What does a function written as `for e in employees: e.annual_review()` do, and whose fault is it?
3. Rewrite it so the problem cannot exist. There is more than one right answer — give two.
4. Now add a second axis: employees are either on-site or remote, and that changes how expenses are
   claimed. How many classes does a pure inheritance model need? How many with composition?
5. Which of the four "inheritance is right here" cases from the lesson does none of this resemble,
   and why?

### The is-a drill

For each, say subclass or compose, and give the one-sentence reason:

1. `SavingsAccount` and `Account`.
2. `Stack` and `List`.
3. `Car` and `Engine`.
4. `PaymentDeclined` and `PaymentError`.
5. `ElectricCar` and `Car`, in a system that also varies by size and by ownership model.
6. `Square` and `Rectangle`, where both are immutable.

Number 6 has a different answer from the mutable version. Say what changed.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the smallest capacity that lets you ship all packages within d days.*
   The sentence shape, the bounds with a reason for each end, the greedy check with its counter
   starting at one, the monotonicity sentence, and the two-part cost.

2. *When does inheritance become a problem?*
   The three named failures with an example each, then the four places it is genuinely right and the
   property they share.

3. *Why is your feasibility check monotone? Prove it.*
   The induction argument for the shipping case — more capacity means at least as many packages
   loaded each day, so it can never finish later — and then name a phrasing where it fails.

---

## Before you move on

- [ ] For all four problems I wrote the range, the check and the monotonicity sentence before the
      loop.
- [ ] My search loop is character-identical across problems 2 and 3.
- [ ] I can say why there is no not-found case in three of the four, and why problem 4 has one.
- [ ] I sorted all five bounds in the drill and named the symptom of each broken one.
- [ ] I can name the three inheritance failures with an example each, unprompted.
- [ ] I did the hierarchy audit including the two-axis class count, both ways.
- [ ] I answered all three questions above out loud.
