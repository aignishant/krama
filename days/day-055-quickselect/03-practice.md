---
day: 55
track: practice
title: "Practice — Quickselect: finding the Kth largest without sorting"
status: written
---

# Day 055 · Practice

**DSA topic:** Quickselect: finding the Kth largest without sorting
**System design topic:** Single responsibility

---

## Code these, in this order

One rule for the whole set: **say the target index out loud before you write anything**, and check it
against `k = 1` and `k = n`. The off-by-one is the bug that actually costs people this question.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Kth Largest Element in an Array | LeetCode 215 (Medium) | The whole lesson. And whether your version survives an input of identical values. |
| 2 | Top K Frequent Elements | LeetCode 347 (Medium) | Quickselect on a derived key — you select on counts, not on the values themselves. |
| 3 | K Closest Points to Origin | LeetCode 973 (Medium) | That you never need the actual distance, only something that orders the same way. |
| 4 | Kth Largest Element in a Stream | LeetCode 703 (Easy) | The boundary: quickselect cannot be used at all, and knowing why is the answer. |

### On problem 1, write all three answers

1. `sorted(nums)[-k]`. Submit it. Note the runtime.
2. `heapq.nlargest(k, nums)[-1]`. Submit it. Note the runtime.
3. Quickselect with a two-way partition and a random pivot. Submit it.
4. Now build `[7] * 200000 + [9]` locally and run your two-way version on it. Record what happens.
5. Switch to the three-way partition and run the same input.

Then say out loud which of the three you would offer first in an interview, and why the answer is
"the sort, for five seconds, and then the better one".

### On problem 2, notice the two-step shape

You need the counts first, then the top `k` of the counts. Say out loud which step dominates the
cost, and what the complexity is if you use quickselect on the count pairs rather than sorting them.

### On problem 3, drop the square root

The point that gets missed: you never need the actual distance, only a value that orders the same
way, so `x² + y²` is enough. Say why that matters — it removes a floating-point operation per element
and removes a source of precision error. Then use quickselect on that key.

### On problem 4, say why quickselect is unavailable

The class receives values one at a time forever. Write the heap solution, then answer out loud: what
exactly does quickselect need that a stream cannot provide? There are two answers, and both matter.

### The index drill

Say each answer in under five seconds, with no code:

1. `n = 10`, k-th largest, `k = 1`. Target index?
2. `n = 10`, k-th largest, `k = 10`. Target index?
3. `n = 10`, k-th smallest, `k = 1`. Target index?
4. `n = 6`, second largest of `[3, 2, 1, 5, 6, 4]`. Target index, then the value.
5. `n = 7`, the median. Target index?
6. `n = 8`, the median. Which two indices, and what do you do with them?

### The partition-trace drill

By hand, with no code, for `nums = [3, 2, 1, 5, 6, 4]` and target index 4:

1. Suppose the random pivot is `4`. Where does it land, and which side survives?
2. How many elements are discarded on that first pass?
3. Suppose instead the pivot is `6`. Where does it land, and which side survives now?
4. Suppose the pivot is `1`. How many elements are eliminated?
5. In the worst possible sequence of pivot choices, how many passes does this take?

### The complexity drill

Answer out loud, in under fifteen seconds each:

1. Why is quickselect `O(n)` when quicksort is `O(n log n)`? Give the sum.
2. Prove that `1 + 1/2 + 1/4 + ... = 2` in one line.
3. What is the worst case, and what input causes it?
4. What does randomising the pivot change, exactly?
5. Which bad case does randomising *not* fix, and what does?
6. What is the space cost of the iterative version, and why can it be iterative?

### The break-it drill

Introduce each bug, run it, and read the result:

1. Pass `k` as the target instead of `len(nums) - k`. Run on `[3, 2, 1, 5, 6, 4]` with `k = 2` and
   read the wrong answer.
2. Recurse into both sides. Check that it still returns the right answer, then say what the
   complexity became.
3. Use a fixed last-element pivot on `list(range(50000))` with `k = 1`.
4. Two-way partition on 200,000 identical values.
5. Forget to copy the input, then print the caller's list afterwards.

### The alternatives drill

For each situation, name the right approach and give its cost:

1. The 10th largest of a million values in memory.
2. The 500,000th largest of a million values in memory.
3. The 10th largest of a billion values arriving one at a time.
4. The median of an array you must not modify.
5. The top 10, where you need them in order.
6. The top 10, where the order does not matter.

### The SRP drill

Here is the class. Do not rewrite it yet.

```python
class ReportGenerator:
    def __init__(self, user_id: int) -> None:
        self.user = db.fetch_user(user_id)
        self.conn = psycopg.connect(os.environ["DB"])
        self.smtp = smtplib.SMTP(os.environ["SMTP"])

    def monthly_report(self, month: date) -> None:
        rows = self.conn.execute("SELECT ... WHERE user_id = %s", (self.user.id,))
        total = sum(r["amount"] for r in rows)
        tax = total * 0.18
        html = f"<h1>{self.user.name}</h1><p>Total: {total}, tax: {tax}</p>"
        pdf = weasyprint.HTML(string=html).write_pdf()
        self.conn.execute("INSERT INTO reports ...", (self.user.id, month, pdf))
        self.smtp.sendmail("reports@x.in", self.user.email, "Your report is ready")
        analytics.track("report_generated", {"user": self.user.id})
```

1. List every method-sized concern in `monthly_report`, and name the **stakeholder** for each. Not
   the topic — the person or team.
2. How many distinct reasons to change does this class have? Say the number.
3. Which imports would you expect in each file after the split? Write the list.
4. Which piece of behaviour should **stay** with the data rather than moving out, and why?
5. Do the split. Five or six classes, and one sentence of responsibility for each with no "and" in
   it.
6. Which class did you extract first, and why that one?
7. Write the test for "eighteen percent tax is applied to the total" and count the lines of setup
   before and after.
8. Now argue the other side: name one reason this split could be a mistake in a small codebase.

### The stakeholder drill

For each class, say how many reasons to change it has and name them:

1. `Matrix` with `multiply`, `transpose`, `invert`, `determinant`, `to_string`.
2. `User` with `full_name`, `is_admin`, `save`, `send_password_reset`.
3. `CsvParser` with `parse`, `validate_row`, `write_to_database`.
4. `Order` with `total`, `add_line`, `is_valid`, `cancel`.
5. `PlaceOrder` with one `execute` method calling five collaborators.
6. `DateRange` with `nights`, `overlaps`, `days`.

Two of those six are fine as they are. Name them and defend it.

### The naming drill

Each of these class names hides a responsibility problem. Say what the class is probably doing, and
what you would call the pieces:

1. `OrderManager`
2. `DataProcessor`
3. `UserUtils`
4. `ApplicationHelper`
5. `CommonService`
6. `FileHandler`

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the Kth largest element. Can you beat O(n log n)?*
   The baseline, the target index checked at both ends, the one-sided recursion, the halving sum, and
   the honest "expected" caveat with both bad cases and both fixes.

2. *This class is 800 lines. What is wrong with it?*
   Reject the line count, name the stakeholders method by method, give the concrete coupling failure,
   say what stays with the data, and name the resulting classes with no "and" in any sentence.

3. *The data is a stream of a billion numbers. Now what?*
   Why quickselect is unavailable, the heap of size k with its two costs, and what you would do if
   `k` were also enormous.

---

## Before you move on

- [ ] I wrote quickselect from memory, iteratively, and it handled `k = 1` and `k = n` correctly.
- [ ] I ran the two-way version on 200,000 identical values and can say why randomising did not help.
- [ ] I can prove `n + n/2 + n/4 + ... = 2n` in one line, out loud.
- [ ] I can say what "expected O(n)" promises and what it does not.
- [ ] I named the stakeholder for every concern in `ReportGenerator` and gave the number.
- [ ] I can say which behaviour stays with the data and why moving everything out is a mistake.
- [ ] I can describe the over-splitting failure and give its cost in files and wiring lines.
- [ ] I answered all three questions above out loud.
