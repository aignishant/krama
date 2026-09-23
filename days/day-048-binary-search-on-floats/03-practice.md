---
day: 48
track: practice
title: "Practice — Binary search on floats, and the epsilon question"
status: written
---

# Day 048 · Practice

**DSA topic:** Binary search on floats, and the epsilon question
**System design topic:** Abstraction and interfaces

---

## Code these, in this order

One rule: **before writing any float loop, say out loud what stops it.** If the answer is not "a fixed
count" or "a relative epsilon", stop and pick one.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Sqrt(x) | LeetCode 69 (Easy) | Whether you notice the answer is an integer and stay in integers. |
| 2 | Square root to six decimal places | Standard follow-up to LC 69 | The stopping rule, and the `max(1.0, x)` bound. |
| 3 | Pow(x, n) | LeetCode 50 (Medium) | Not binary search on the answer — binary *exponentiation*. Know the difference. |
| 4 | Minimize Max Distance to Gas Station | LeetCode 774 (Hard) | The full float search: an expensive check, so the iteration count is a real decision. |

### On problem 1, do not touch a float

The answer is an integer, so search integers: the largest `m` with `m * m <= x`. Python's ints are
exact at any size, so there is no rounding to reason about. Remember the ceiling midpoint —
`(lo + hi + 1) // 2` — because this is the last-True form; write it with the floor midpoint first,
watch it hang, kill it, then fix it. Then run it on `10**18` and confirm the answer is exact.

### On problem 2, break it three ways before you fix it

Write the working version. Then produce all three failures deliberately and collect the evidence:

1. `while lo < hi` — run it, kill it with Ctrl-C, paste the `KeyboardInterrupt`.
2. `while hi - lo > 1e-9` with `x = 1e18` — run it, kill it, and say what number makes it
   unreachable.
3. `hi = x` instead of `hi = max(1.0, x)` — run it on `0.25` and read the wrong answer.

Then write the hundred-iteration version and check all four inputs pass.

### On problem 3, notice this is a different animal

LeetCode 50 is not binary search on the answer. It is exponentiation by squaring: `x^n` is
`(x^(n//2))²`, with an extra `x` when `n` is odd. It is `O(log n)` for the same reason binary search
is — halving — but nothing is being searched. Being able to say why it is in the same complexity class
and a different pattern is the point of including it here. Handle negative `n`, and say what
`x^(-2³¹)` does about overflow.

### On problem 4, size the iteration count from the requirement

The check here is an `O(n)` pass, so a hundred iterations is a hundred passes and the count stops
being free. Work out the number: the answer needs about 10⁻⁶ precision, the range is up to 10⁸, so
`log₂(10⁸ / 10⁻⁶) = log₂(10¹⁴)` ≈ 47. Use 50, not 100, and say the arithmetic out loud. Then say why
you would still not switch to an epsilon loop to save the iterations.

### The stopping-rule drill

For each, say what happens — converges, hangs, or converges to the wrong precision:

1. `while lo < hi` on floats.
2. `while hi - lo > 1e-9`, answer near 3.
3. `while hi - lo > 1e-9`, answer near 10¹⁵.
4. `while hi - lo > 1e-9 * max(1.0, lo)`, answer near 10¹⁵.
5. `for _ in range(100)`, answer near 10¹⁵.
6. `for _ in range(20)`, answer near 3, six decimals wanted.

### The precision drill

Answer from memory, no calculator:

1. How many significant decimal digits does a 64-bit double hold?
2. What is the smallest step between representable doubles near 1.0? Near 10¹⁵?
3. How many halvings does it take to shrink a range of 10 to below 10⁻⁹?
4. By what factor does a hundred halvings shrink any range?
5. Why is `0.1 + 0.2 == 0.3` False?

### The integer-first drill

For each, say whether you would search integers or floats, and why:

1. The floor of the square root of `x`.
2. The square root to six decimal places.
3. The smallest ship capacity, weights in whole kilos.
4. The minimum time in seconds, answers to the millisecond.
5. A price, in rupees and paise.

Number 5 has a specific right answer that is neither. Say what it is and why money is not a float.

### The swap-the-provider drill

Take this and rework it out loud in five minutes:

```python
import stripe

class Checkout:
    def __init__(self):
        self.client = stripe.Client(api_key=settings.STRIPE_KEY)

    def pay(self, order, token):
        try:
            intent = self.client.PaymentIntent.create(
                amount=int(order.total * 100), currency="inr", payment_method=token
            )
        except stripe.error.CardError as e:
            order.mark_failed(e.user_message)
            return
        order.mark_paid(intent.id)
```

1. Name the three leaks — a type leak, an error leak, and a semantics leak. Point at the exact lines.
2. Write the interface. It has two methods and no vendor word in it.
3. Say who constructs the gateway now, and where.
4. Write the `FakeGateway` and the test for a declined card.
5. Count the edits to add Razorpay, before and after.
6. Write the grep command that proves the abstraction holds, and say what a healthy result looks like.

### The name-the-second drill

For each, say whether you would write an interface, and name the second implementation — or say there
is not one:

1. A payment gateway.
2. A slug generator that turns a title into a URL fragment.
3. A file store for user uploads.
4. An order repository.
5. An invoice numbering scheme.
6. A search index.

Two of these have "an in-memory fake for tests" as their honest second implementation. Say which, and
whether that is enough on its own.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the square root of a number to six decimal places, without the library call.*
   The integer-or-float clarifying question, the `max(1.0, x)` bound with its reason, what changes on
   floats, the fixed count and why you prefer it, and the input that kills the absolute epsilon.

2. *How would you make it easy to swap the payment provider later?*
   The interface in your vocabulary, the injection, the translation at the adapter's edge, the number
   (30-60 edits against one line), and the cost you accepted.

3. *When does your loop stop, and why is that the right condition?*
   The three candidates, what each does on a large answer, and the sentence about a hundred halvings
   shrinking any range past double precision.

---

## Before you move on

- [ ] I solved LeetCode 69 entirely in integers, with the ceiling midpoint, and it is exact at 10¹⁸.
- [ ] I made a float loop hang three separate ways and collected the evidence for each.
- [ ] I can state the double-precision numbers — 15-17 digits, ~2.2e-16 near 1, ~0.125 near 10¹⁵.
- [ ] I sized the iteration count for LeetCode 774 from the required precision, with the arithmetic.
- [ ] I found all three leaks in the `Checkout` class and named each by kind.
- [ ] I wrote the grep command and can say what a healthy result is.
- [ ] I answered all three questions above out loud.
