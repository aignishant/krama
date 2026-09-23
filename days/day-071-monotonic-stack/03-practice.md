---
day: 71
track: practice
title: "Practice — Monotonic stack: the next greater element"
status: written
---

# Day 071 · Practice

**DSA topic:** Monotonic stack: the next greater element
**System design topic:** Strategy

---

## Code these, in this order

One rule for the whole set: **before writing the loop, say what the stack holds.** "The stack holds
the indices of elements whose answer is not yet known." If you cannot say that sentence about your
stack, you are using it as a scratch space and the code will drift.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Next Greater Element I | LeetCode 496 (Easy) | The base pattern, plus a map from value to answer for the lookup half. |
| 2 | Daily Temperatures | LeetCode 739 (Medium) | The distance variant — which is why the stack must hold indices. |
| 3 | Next Greater Element II | LeetCode 503 (Medium) | Circular: `2n` steps, and pushing only on the first pass. |
| 4 | Online Stock Span | LeetCode 901 (Medium) | Previous-greater, arriving one element at a time rather than as an array. |

### On problem 2, try it with values first

Write the stack holding values instead of indices. Get to the line where you need `index - previous`
and find you cannot write it. Then switch to indices and say out loud why this is the default.

### On problem 3, break the second pass on purpose

Push on both passes. Run `[1, 2, 1]` and see what comes out. Then add `if step < n` and run it again.
Say in one sentence why the second pass must only answer, never ask.

### On problem 4, notice what changed

The elements arrive one at a time and you must answer immediately. Say what that does to the stack —
and what it does not do to the counting argument.

### The complexity-defence drill

Say this out loud, five times, until it is automatic:

1. How many pushes happen across the whole run?
2. How many pops can happen across the whole run, and why?
3. What is the total number of stack operations?
4. What do you say to "there is a loop inside a loop, so it is O(n²)"?
5. Give an input where one iteration pops n − 1 elements, and explain why that is fine.

### The four-variants drill

For `[4, 2, 5, 1, 3]`, compute all four by hand, then write all four and check:

1. Next greater to the right.
2. Next smaller to the right.
3. Previous greater to the left.
4. Previous smaller to the left.

Then, for each, say which direction you walked and which way the comparison pointed, and what
direction the stack ended up ordered in.

### The strictness drill

1. Run `next_greater([2, 2, 3])` with `<`. Write down the answer.
2. Run it with `<=`. Write down the answer.
3. Explain the difference in one sentence.
4. For each of these phrasings, say whether you would use `<` or `<=`:
   - "the next greater element"
   - "the next day that is at least as warm"
   - "the first later element strictly larger"
   - "the span of days up to and including today with price ≤ today's"
5. Say what question you would ask the interviewer if the phrasing were ambiguous.

### The break-it drill

Trigger each and say what happens:

1. Remove `stack and` from the `while` condition. Quote the exact error and the input that causes it.
2. Push before popping instead of after. Run `[2, 2, 3]` with `<=` and explain the output.
3. Store values instead of indices, then try to write Daily Temperatures.
4. Build the answer by appending as you pop, instead of pre-filling and writing by index. Run
   `[5, 4, 3]` and count the length of your output.
5. Push on both passes of the circular version.
6. Use `>` when you wanted next-greater. Run `[4, 2, 5, 1]` and say which variant you accidentally
   wrote.

### The recognition drill

For each, say whether it is a monotonic-stack problem, and if so which variant:

1. For each day, how many days until a warmer one.
2. For each element, the nearest smaller element to its left.
3. The k most frequent elements.
4. The largest rectangle in a histogram.
5. How much rain water is trapped between the bars.
6. Whether the brackets are balanced.
7. For each stock price, how many consecutive earlier days had a price ≤ today's.
8. The minimum of the stack in O(1).
9. Remove k digits to make the smallest possible number.
10. The next greater element in a circular array.

Two of the ten are stack problems but *not* monotonic-stack problems. Name them and say what the
difference is.

### The strategy-refactor drill

Here is the function:

```python
def price(order: Order, country: str) -> Decimal:
    if country == "IN":
        base = order.subtotal * Decimal("1.18")
        if order.subtotal > 5000:
            base -= Decimal("100")
        return base
    elif country == "AE":
        return order.subtotal * Decimal("1.05")
    elif country == "GB":
        return order.subtotal * Decimal("1.20") - order.loyalty_credit
    raise ValueError(country)
```

1. Name the axis of change, in three words.
2. List four specific things wrong with this, none of which is "it is ugly".
3. Write the protocol.
4. Write the three implementations.
5. Write the selection, and say why it must not live in `Checkout`.
6. Write the same thing as a dictionary of functions. Count the lines both ways.
7. Add a fourth market to each version. Count files edited and tests re-run.
8. Write the test for the UK rule, before and after. Count the lines.
9. Say what you gained, honestly, including what did *not* happen to the `if`.

### The do-not-do-it drill

For each, say whether you would use Strategy, and give the deciding question:

1. Three countries whose only difference is the tax rate.
2. Three countries with genuinely different rule shapes.
3. Two sorting orders for a report.
4. Seven weekdays with different opening hours.
5. Compression: gzip versus zstd versus lz4.
6. A retry policy each customer configures for themselves.
7. The first time a second variant has appeared.
8. Three payment providers with different SDKs.

One of the eight is really an adapter question, not a strategy question. Name it and say why. Two are
"no" for the same reason — name it.

### The look-alikes drill

1. Write a small State machine — a `Draft` order that moves itself to `Submitted`, which moves itself
   to `Shipped`.
2. Write the same thing as Strategy, with the client choosing.
3. Say which one you wrote by looking only at the implementations. What is the tell?
4. Write a Template Method version of "load, transform, save" where the transform varies.
5. Rewrite it as Strategy.
6. Name three things the Strategy version can do that the Template Method version cannot.

### The already-used-it drill

For each, say what the strategy is and what the interface is:

1. `sorted(items, key=lambda x: x.age)`
2. `hashlib.new("sha256")`
3. nginx's `least_conn;`
4. `functools.lru_cache(maxsize=128)`
5. `tenacity.retry(wait=wait_exponential())`
6. Django's `PASSWORD_HASHERS` setting
7. `defaultdict(list)`

One of the seven is a decorator rather than a strategy. Name it and say why the distinction holds.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *For every element, find the next greater element to its right.*
   The brute force with a number, the observation that popping *is* answering, what the stack holds,
   indices-not-values with the reason, and the complexity defence pre-empted rather than defended.

2. *The pricing rule changes per country. How do you structure that?*
   The axis named first, four specific problems with the chain in edit counts, the interface, the
   selection kept separate and why, the Python function version with its line count, and the honest
   concession about where the `if` went.

3. *There is a loop inside a loop. Is that not O(n²)?*
   n pushes total, each element popped at most once, so ≤ 2n operations — bounded in total, not per
   iteration — and the example where one iteration pops n − 1 and why it costs nothing.

---

## Before you move on

- [ ] I can say what the stack holds, in one sentence, without hesitating.
- [ ] I can give the complexity defence confidently, without softening it.
- [ ] I wrote all four variants and can generate any of them from the two knobs.
- [ ] I know what `<` versus `<=` does on `[2, 2, 3]` and which phrasings need which.
- [ ] I tried storing values and hit the wall on Daily Temperatures.
- [ ] I broke the circular version by pushing on both passes and saw the wrong output.
- [ ] I can name two stack problems that are not monotonic-stack problems.
- [ ] I refactored the pricing function and counted files edited for a fourth market, both ways.
- [ ] I wrote the dictionary-of-functions version and can quote both line counts.
- [ ] I can say the honest sentence about where the `if` actually went.
- [ ] I can name the test that separates "behaviour differs" from "only a value differs".
- [ ] I answered all three questions above out loud.
