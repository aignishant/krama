---
day: 59
track: practice
title: "Practice — Sorting revision and mock round"
status: written
---

# Day 059 · Practice

**DSA topic:** Sorting revision and mock round
**System design topic:** Dependency inversion

---

## Code these, in this order

One rule for the whole set, and it is the only rule today: **run it as a mock.** Set a timer, talk out
loud the entire time, and do not stop when you get something wrong. Twenty minutes per problem,
including the clarifying questions and the out-loud testing. If nobody is available to sit with you,
record yourself — the point is that the words leave your mouth.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Meeting Rooms II | LeetCode 253 (Medium) | That "sort by what?" is the whole question — and this one wants two separate sorted lists. |
| 2 | Top K Frequent Words | LeetCode 692 (Medium) | Choosing between sort, heap and quickselect, and defending the choice with arithmetic. |
| 3 | Maximum Gap | LeetCode 164 (Hard) | A linear-time requirement, so the comparison sorts are all excluded by the constraints. |
| 4 | Merge Intervals | LeetCode 56 (Medium) | The phase's cleanest "the sort is the algorithm" — and which field you sort on. |

### The rules for all four

1. **Three minutes of clarifying first**, out loud, before a line of code. Size, key type, range,
   nearly sorted, can you modify the input, does it fit in memory.
2. **State the approach and its cost before writing.** *"Brute force is O(n²), that's X operations at
   this size. Sorting makes it O(n log n) because [reason]. I'll do that."*
3. **Narrate while writing.** Say the invariant. Flag the error-prone lines as you reach them.
4. **Test out loud on five inputs**: empty, one element, all equal, already sorted, reverse sorted.
5. **Answer the follow-up you know is coming** before it is asked: what if it is a stream, what if
   the values are bounded, what if you only need the top k.

### On problem 1, the sort choice is the interview

There are three defensible solutions — the two-list sweep, the min-heap of end times, and the
difference-array sweep from [day 039](../day-039-difference-arrays/README.md). Solve it one way, then
say the other two out loud with their costs and say which you would defend and why.

### On problem 2, do the arithmetic before choosing

`n` distinct words, want the top `k` by count, ties broken alphabetically. Say all three costs out
loud — `O(n log n)` full sort, `O(n log k)` heap, `O(n)` quickselect — then say which you would use
and what makes the choice. Watch the tie-break: it is a two-key ordering, and one of them goes
descending.

### On problem 3, let the constraint pick the algorithm

The problem demands linear time, which rules out every comparison sort by definition. Say that out
loud as the first sentence. Then find the pigeonhole argument before coding: with `n` values and
`n − 1` buckets, the largest gap must span two different buckets, so only each bucket's minimum and
maximum matter.

### On problem 4, say the key before you type it

Sort by start, not by end, and be able to say what sorting by end would solve instead. Then break it
deliberately: sort by `iv[1]` and run it on `[[1, 4], [0, 2], [3, 5]]` to get a plausible wrong answer
with no error.

### The phase-recall drill

Two minutes each, no reference, code that runs:

1. `insertion_sort`, with the guard in the right order and the strict comparison.
2. `merge`, with both `extend` lines and the `<=`.
3. `merge_sort`, with the base case that covers empty.
4. `partition`, with a random pivot, and say its invariant.
5. `quicksort`, recursing into the smaller side.
6. `quickselect`, iterative, with the correct target index for the k-th largest.
7. `counting_sort`, stable, with the running totals and the backwards placement.

### The decision drill

For each, say what you would use and give the cost. Fifteen seconds each:

1. Sort a million integers between 0 and 100.
2. Sort a million arbitrary integers in Python.
3. Find the 5th largest of a million values.
4. Find the top 100 of a billion values arriving one at a time.
5. Sort ten million records by a 32-bit integer id.
6. Sort a linked list of 100,000 nodes.
7. Sort 30 elements inside a tight loop.
8. Sort a nearly-sorted log file of two million lines.
9. Find whether any value appears twice in a million values.
10. Sort a list of records by department, then by name descending.

### The arithmetic drill

Answer with numbers, in under ten seconds each:

1. `n log n` against `n²` at a million elements. Both numbers and the ratio.
2. Why quickselect is `O(n)`, in one line of algebra.
3. Comparisons for merge sort, quicksort and heapsort at a million elements.
4. Counting sort's operation count and memory for a million values in `0..100`.
5. Counting sort's memory for three values with a maximum of two billion.
6. `sorted()` in C against a hand-written merge sort in Python, at a million elements.
7. Timsort on already-sorted against random input, two million integers.

### The trap drill

Trigger each one, read the output, and say the fix in one sentence:

1. Quicksort with a last-element pivot on `list(range(5000))`.
2. Quicksort with `<=` in the partition on `[7] * 3000`.
3. Quicksort recursing on `p` instead of `p - 1`.
4. Merge sort with only one `extend`.
5. Merge sort with `if len(nums) == 1` called on `[]`.
6. Counting sort with a maximum of two billion.
7. `kth_largest` with `k` as the target index.
8. `reverse=True` on a tuple key.
9. `-p.name` in a key function.
10. `nums.sort()[:3]`.

### The dependency-inversion drill

Here is the module. Do not refactor it yet.

```python
# billing/invoicer.py
import boto3
import psycopg
import weasyprint
from sendgrid import SendGridAPIClient

class Invoicer:
    def issue(self, customer_id: int, month: str) -> str:
        conn = psycopg.connect(os.environ["DATABASE_URL"])
        with conn.cursor() as cur:
            cur.execute("SELECT sku, qty, unit_paise FROM usage WHERE cust=%s AND month=%s",
                        (customer_id, month))
            rows = cur.fetchall()
        subtotal = sum(r[1] * r[2] for r in rows)
        total = int(subtotal * 1.18)
        pdf = weasyprint.HTML(string=render("invoice.html", rows=rows, total=total)).write_pdf()
        key = f"invoices/{customer_id}/{month}.pdf"
        boto3.client("s3").put_object(Bucket="invoices", Key=key, Body=pdf)
        SendGridAPIClient(os.environ["SG_KEY"]).send(...)
        return key
```

1. Run the grep in your head: which external packages does the business logic depend on? Count them.
2. Which lines are the actual business rule? There are two. Point at them.
3. List the operations the policy needs from each mechanism — not what the library offers, what this
   code uses.
4. Write the ports. Which package do they live in, and why does that matter?
5. What types appear in the port signatures? Make sure none of them is a vendor type.
6. Write one adapter fully, including the translation at its edge — their rows to your objects, their
   errors to your exceptions.
7. Write the composition root.
8. Give the two commands that prove the inversion is real.
9. Write the test for "an eighteen percent tax is applied", and count the lines of setup before and
   after.
10. Now argue against yourself: give one scenario where this refactor would be the wrong call.

### The injection-versus-inversion drill

For each, say whether it is injection, inversion, both, or neither:

1. `def __init__(self): self.db = psycopg.connect(...)`
2. `def __init__(self, conn: psycopg.Connection): self.db = conn`
3. `def __init__(self, orders: OrderRepository): self._orders = orders`, with `OrderRepository`
   defined in `persistence/`.
4. `def __init__(self, orders: OrderRepository): self._orders = orders`, with `OrderRepository`
   defined in `orders/ports.py`.
5. Django calling your view function when a request arrives.
6. A pytest fixture supplying an in-memory repository to a test.

### The where-does-the-interface-live drill

For each, say which package the interface belongs in and give the one-line reason:

1. `OrderRepository`, used by `orders/service.py`, implemented by Postgres.
2. `PaymentGateway`, used by `checkout/`, implemented by Razorpay and a fake.
3. `Clock`, used by `subscriptions/`, implemented by the system clock and a fixed clock.
4. `EmailSender`, used by three different modules.
5. `Serializer`, defined by a third-party library you are using.
6. `Comparable`, in a language's standard library.

Two of those six are cases where you do *not* own the interface. Name them and say what follows.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Two problems, no hints, talk as you go.*
   Run the full script on an unseen problem: three minutes of clarifying, the approach and cost
   before coding, narration while writing, five test inputs out loud, and the follow-up answered
   before it is asked.

2. *Your service imports the MySQL driver directly. What is wrong with that?*
   The direction of the arrow, the three harms, where the interface lives and why that is the half
   people skip, the adapter as a translator, and the grep that proves it.

3. *Which sorting algorithm would you actually use, and why?*
   `sorted()` and the honest reason, then the five cases where you would do something else, ending on
   "pick two of guaranteed, in place, stable".

---

## Before you move on

- [ ] I ran all four problems as timed mocks, talking out loud, without stopping when I was wrong.
- [ ] I asked clarifying questions about the *data* before coding, every time.
- [ ] I stated the approach and its cost before writing a line, every time.
- [ ] I can write all seven reference implementations from memory in under two minutes each.
- [ ] I triggered all ten traps and can give the one-sentence fix for each.
- [ ] I can answer the decision drill's ten scenarios without hesitating.
- [ ] I refactored `Invoicer` and can give both commands that prove the inversion is real.
- [ ] I can state the difference between dependency injection and dependency inversion in one
      sentence.
- [ ] I answered all three questions above out loud.
