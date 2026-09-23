---
day: 56
track: practice
title: "Practice — Counting sort, radix sort, and bucket sort"
status: written
---

# Day 056 · Practice

**DSA topic:** Counting sort, radix sort, and bucket sort
**System design topic:** Open for extension, closed for modification

---

## Code these, in this order

One rule for the whole set: **before writing anything, say what you know about the keys** — are they
integers, what is the range, and what is `k` compared with `n`. If you cannot answer that, you cannot
use today's sorts, and saying so is the right answer.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Sort Colors | LeetCode 75 (Medium) | Counting sort with `k = 3` — and whether you notice it is the same problem as the Dutch flag. |
| 2 | Maximum Gap | LeetCode 164 (Hard) | The classic bucket-sort problem: `O(n)` is required, and the pigeonhole argument is the whole trick. |
| 3 | Sort an Array | LeetCode 912 (Medium) | The range is −50,000 to 50,000. Counting sort is genuinely the best answer, and spotting that is the point. |
| 4 | H-Index | LeetCode 274 (Medium) | Counting sort in disguise — citations above `n` can all be bucketed together. |

### On problem 1, write both and compare

Write the counting version (count 0s, 1s, 2s, then overwrite) and the one-pass three-region version.
Both are `O(n)`. Say out loud which one the interviewer wants and why — the answer is about passes
over the data, not about complexity.

### On problem 2, find the pigeonhole argument first

Do not code until you can say this out loud: *if `n` values are spread over a range, and you make
`n − 1` buckets, then the largest gap must be between two values in different buckets, so you only
need each bucket's minimum and maximum and never what is inside them.* That sentence is the problem.
Then say why the bucket count is `n − 1` and not `n`.

### On problem 3, use the constraint

The constraints say `-50000 <= nums[i] <= 50000`. That is `k = 100,001` for up to 50,000 elements.
Write the counting sort with the `- min` shift, submit it, and compare the runtime with `sorted()`.
Then answer honestly: which was faster in Python, and why does that not change the asymptotic answer?

### On problem 4, notice the cap

Citations can be enormous, so a naive counting sort would need a huge table — but any paper with more
than `n` citations counts the same as one with exactly `n`. Say out loud what that does to `k`, and
why the resulting solution is `O(n)`.

### The counting-sort drill

Write `counting_sort` from memory, then verify:

1. `counting_sort([3, 1, 4, 1, 5, 1, 4], 5)`.
2. `counting_sort([], 5)` — does it return, or does it raise?
3. `counting_sort([2, 2, 2], 2)`.
4. `counting_sort_range([-3, 7, -1, 0, 7])` — what is `k` here?
5. Sort `[(2, "first"), (1, "x"), (2, "second"), (1, "y")]` by key and check that `"first"` still
   comes before `"second"`.

For number 5, then change `reversed(nums)` to `nums` and run it again. Record what changed and say
why nothing raised.

### The k-versus-n drill

For each, say whether counting sort is the right choice, and give the operation count and the memory:

1. A million exam marks, 0 to 100.
2. A million ages, 0 to 120.
3. A thousand timestamps in milliseconds since 1970.
4. Ten million product IDs, 1 to 50,000.
5. Fifty values between 0 and one billion.
6. A million floating-point temperatures between −40 and 55.

Two of those six should make you say "MemoryError", and one should make you say "not an integer".

### The radix drill

1. Trace `radix_sort([329, 457, 657, 839, 436, 720, 355])` by hand, writing the list after each pass.
2. In pass 2, find the pair whose order was decided by pass 1, and say which pair it is.
3. Replace the per-digit sort with one that reverses equal keys. Run it and paste the wrong output.
4. How many passes for values up to 999,999 in base 10? In base 256?
5. Why does radix sort go least-significant digit first? What happens if you go the other way?
6. Sort `["cat", "act", "tab"]` with radix sort. What changes for strings?

### The break-it drill

Introduce each, run it, and read the result:

1. `counting_sort([1, 5, 2_000_000_000], 2_000_000_000)`. Paste the error.
2. `counting_sort([3, -1, 2], 3)`. Paste the error, then explain why a *different* negative value
   might not raise at all.
3. Bucket sort with `* n` instead of `* (n - 1)` in the index. Paste the error.
4. Bucket sort on `[0.5] * 9999 + [0.99]`. Time it, and time `sorted()` on the same list.
5. Counting sort placing forwards with start positions, tested on `(key, tag)` pairs.

### The theory drill

Answer out loud, in under fifteen seconds each:

1. Why can no comparison sort beat `O(n log n)`?
2. How do today's three get around that, and what do they give up?
3. What exactly is `k` in `O(n + k)`?
4. Why does radix sort require a stable inner sort?
5. What is bucket sort's worst case, and what causes it?
6. Which of today's three sorts in place? (Trick question.)

### The open/closed drill

Here is the function. Do not rewrite it yet.

```python
def export(report: Report, fmt: str) -> bytes:
    if fmt == "csv":
        rows = [",".join(str(c) for c in r) for r in report.rows]
        return "\n".join(rows).encode()
    elif fmt == "json":
        return json.dumps({"rows": report.rows}).encode()
    elif fmt == "xlsx":
        wb = openpyxl.Workbook()
        for r in report.rows:
            wb.active.append(r)
        return save_to_bytes(wb)
    elif fmt == "pdf":
        html = render_template("report.html", rows=report.rows)
        return weasyprint.HTML(string=html).write_pdf()
    raise ValueError(f"unknown format {fmt}")
```

1. What question is this chain answering? Write that sentence — it is your interface method.
2. Declare the interface. Two methods at most.
3. Move each branch into its own class. Do them one at a time.
4. Write the closed calling code, and say why it will never change again for this reason.
5. Write the wiring, and say exactly which line changes when a new format arrives.
6. Now count: files touched, existing tests re-run, and lines of existing code read — before and
   after.
7. Add an XML exporter. Time yourself. Then say what adding the *twelfth* format would cost under
   each design.
8. Argue the other side: give one scenario where leaving this function alone is the correct
   engineering decision.

### The should-I-build-it drill

For each, say whether you would create a plug point, and name the second implementation — or say
plainly that you cannot:

1. Discount types in an online shop, one new one per month.
2. Days of the week.
3. GST rates by product category.
4. Payment providers.
5. T-shirt sizes.
6. Notification channels (email, SMS, push).
7. The four suits in a deck of cards.
8. Export formats, where only CSV has ever been requested.

Three of those eight are traps. Name them.

### The platform drill

For each, say what the stable core is, what the published contract is, and what arrives from outside:

1. `sorted(key=...)`.
2. Django middleware.
3. pytest plugins.
4. Payment provider webhooks.
5. VS Code extensions.
6. Python's `functools.singledispatch`.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Sort a million integers in the range 0 to 100. Can you beat n log n?*
   Ask about the keys, name why the limit does not apply, give `O(n + k)` with `k` explained, and
   volunteer the MemoryError condition before being asked.

2. *A new discount type arrives every month. How do you design for that?*
   Ask whether it is data or behaviour, name the question the branch answers, show the interface and
   the closed class, give the edit count, and concede where the change moved to.

3. *Why does radix sort need a stable sort?*
   The 457-and-657 example, what an unstable pass destroys, and why the failure is silent.

---

## Before you move on

- [ ] I wrote counting sort from memory, stable, with the running totals and the backwards placement.
- [ ] I broke stability by placing forwards and can say why nothing raised.
- [ ] I triggered the MemoryError and can state the `k`-is-the-range rule in one sentence.
- [ ] I can name the two bad cases for bucket sort and quote the 2,500× number.
- [ ] I traced radix sort by hand and can point at the pair whose order came from the previous pass.
- [ ] I refactored the exporter and can give the before-and-after edit counts.
- [ ] I can name three variations where a plug point would be a mistake, and say why for each.
- [ ] I answered all three questions above out loud.
