---
day: 72
track: practice
title: "Practice — Largest rectangle in a histogram"
status: written
---

# Day 072 · Practice

**DSA topic:** Largest rectangle in a histogram
**System design topic:** Observer

---

## Code these, in this order

One rule for the whole set: **before writing the loop, say the width formula as a sentence.** "Both
boundaries are the shorter bars themselves, and neither of them is inside the span, so the width is
`right - left - 1`." If you cannot say that sentence, do not write the loop yet.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Sum of Subarray Minimums | LeetCode 907 (Medium) | The same two boundaries, used to *count* spans instead of measuring one. Forces the width formula into your hands. |
| 2 | Largest Rectangle in Histogram | LeetCode 84 (Hard) | Today's problem. The reduction, the one-pass pop, and the sentinel. |
| 3 | Trapping Rain Water | LeetCode 42 (Hard) | The same stack accumulating as it pops — and the two-pointer solution that beats it on space. |
| 4 | Maximal Rectangle | LeetCode 85 (Hard) | Recognising that each row of a binary grid is a histogram. Almost no new code. |

### On problem 1, do it the slow way first

Write the O(n²) version that finds the minimum of every subarray. Run it on an array of 2,000 random
values and time it. Then write the boundary version and time that. Say out loud why the boundaries
turn "minimum of every subarray" into "how many subarrays does each element win", and where the
duplicate-handling has to be asymmetric — one side strict, one side not — or you double-count.

### On problem 2, get the width wrong on purpose

1. Write it with `width = index - left` and run `[2, 1, 5, 6, 2, 3]`. Write down what it returns.
2. Fix it to `index - left - 1` and run it again.
3. Say in one sentence why the `- 1` is there, without using the words "off by one".

### On problem 3, solve it twice

Once with the monotonic stack, popping and adding the water trapped above the popped bar. Once with
two pointers from [day 030](../day-030-fast-and-slow/README.md), moving the smaller side
inward. Then say which one you would write in an interview and why — the answer involves the words
"O(1) space".

### On problem 4, count before you code

Before writing anything, say the complexity out loud: rows × columns to build the heights, plus one
O(columns) histogram solve per row. State the total. It sounds much worse than it is, and saying the
number first is how you stop the interviewer thinking you have not noticed.

---

### The reduction drill

Say the argument out loud, five times, until it comes without effort:

1. Why are there infinitely many candidate rectangles as the problem is stated?
2. What is the claim that cuts it down to `n`?
3. Prove it in one sentence. (Start with "suppose the top edge were below every bar it spans".)
4. Given that claim, what is the exact question you now ask about each bar?
5. Name the two things you need per bar, and what each defaults to when there is none.

### The width drill

For `heights = [2, 1, 5, 6, 2, 3]`, compute by hand, for every index:

1. `left[i]` — the index of the nearest strictly shorter bar to the left, or −1.
2. `right[i]` — the index of the nearest strictly shorter bar to the right, or 6.
3. The width, and the area.
4. Which index wins, and by how much over the runner-up.

Then check your six areas against `largest_rectangle_two_pass`. Any disagreement is a boundary
definition you have wrong, not an arithmetic slip.

### The trace drill

Run `[2, 1, 5, 6, 2, 3]` in your head with a sentinel at the end, writing the stack contents after
every step. Then answer without looking:

1. At which index does one arrival pop two bars?
2. What is the width computed for the bar of height 2 at index 4, and why is it not 2?
3. How many bars does the sentinel pop?
4. What would the function return with no sentinel and no drain loop?

### The break-it drill

Trigger each and record what actually happens — the output, or the exact error text:

1. Remove `stack and` from the `while` condition. Quote the error and the input that causes it.
2. Write `left = stack[-1]` with no `if stack else -1`. Quote the error.
3. Use `index - stack.pop()` as the width. Run `[2, 1, 5, 6, 2, 3]`, then run `[4, 3]`. Explain why
   the first one is the dangerous result.
4. Remove the sentinel. Run `[2, 2]`, then `[1, 2, 3, 4, 5]`, then `[2, 1, 5, 6, 2, 3]`. Say why the
   third one makes this bug so hard to catch.
5. Change `>` to `>=`. Confirm the answer is still right, then say which duplicate carries the full
   span in each version.
6. Push before popping instead of after. Say what the bar compares itself against.

### The random-cross-check drill

Write the O(n²) brute force, then run both on two thousand random arrays of length 0 to 12 with
values 0 to 9, asserting they agree. Then break one thing from the drill above and watch the
assertion fire on a four-element input. Say out loud why small random inputs catch this bug class
faster than large ones.

### The recognition drill

For each, say whether the histogram stack is the tool, and if so what plays the part of "height":

1. The largest square of 1s in a binary grid.
2. The largest rectangle of 1s in a binary grid.
3. How much rain water is trapped between bars.
4. The sum of the minimums of every subarray.
5. The maximum area of a container formed by two vertical lines.
6. For each day, how many days until a warmer one.
7. The largest rectangle under a skyline where bars have different widths.

Two of the seven are not stack problems at all. Name them and say what they are instead.

---

### The observer-refactor drill

Here is the function:

```python
def place_order(order: Order) -> str:
    order_id = store.save(order)
    smtp.send_confirmation(order)
    warehouse.reserve(order.items)
    billing.generate_invoice(order)
    loyalty.award(order.user_id, order.total_paise)
    analytics.record("order_placed", order_id)
    return order_id
```

1. List every module this function now depends on.
2. Name three specific things that go wrong when the sixth reaction is added.
3. Write the observer interface. One method. Say why one and not five.
4. Write the event class, and say why it is frozen.
5. Write `attach`, `detach` and `_notify`, with all three of the details from §5 in place.
6. Write the composition root.
7. Add a sixth listener. Count the files edited and the existing tests that must re-run, both ways.
8. Now make it publish to a broker instead. Quote both latency totals.

### The failure drill

For each, say what the customer sees and what you would add:

1. The analytics recorder throws, and there is no try/except.
2. The analytics recorder throws, there is a try/except, and no logging.
3. The email service is down for one hour, with in-process observers.
4. The email service is down for one hour, with Kafka.
5. An observer detaches itself while being notified, and you iterate the list directly.
6. An observer mutates the event before the next observer sees it.
7. A short-lived request object subscribes and is never detached.

### The do-not-do-it drill

For each, say whether you would use Observer, and give the deciding question:

1. Two things happen on order placement, both core to ordering.
2. Five things happen, and one of them must run before another.
3. Five things happen, and either all five succeed or the order must be cancelled.
4. One listener, today, with no second one in sight.
5. The subject needs to know whether the order is fraudulent before saving it.
6. Cache invalidation when any row in a table changes.
7. Six teams each want to react to checkout, on their own deployment schedule.

Two of the seven are "no" for the same reason. Name it. One is a "yes" only in the broker form — say
which and why.

### The already-used-it drill

For each, name the subject, the observer, and whether a missed notification is lost forever:

1. `button.addEventListener("click", handler)`
2. Django's `post_save.connect(...)`
3. Redis `SUBSCRIBE orders`
4. A Kafka consumer group reading `orders.placed`
5. Postgres `LISTEN order_placed`
6. Stripe calling your `/webhooks/stripe` endpoint
7. React's `useEffect` with a dependency array

Three of the seven lose the message if the listener is not there at the moment it fires. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the largest rectangle in the histogram.*
   The reduction first — why the top edge must rest on a bar — then the per-bar question, the two
   boundaries with their defaults, the width formula said as a sentence, the one-pass fold with both
   boundaries known at the moment of the pop, the sentinel, and the counting argument for O(n).

2. *When an order is placed, five things must happen. Design that.*
   The shape named before the pattern, the concrete coupling problem in terms of imports and
   re-tested tests, the one-method interface with an immutable event, save-then-notify, wiring in the
   composition root, and then the two separate decisions — per-listener failure handling, and 365 ms
   synchronous against 27 ms through a broker.

3. *Why is the top edge of the best rectangle always level with some bar?*
   Suppose it is not; raise it; it still fits and it is bigger. Then say what that buys you — `n`
   candidates instead of infinitely many — and what the per-bar question becomes.

---

## Before you move on

- [ ] I can state the reduction claim and prove it in one sentence.
- [ ] I can say the width formula as a sentence, without the words "off by one".
- [ ] I computed `left`, `right`, width and area by hand for all six bars of `[2, 1, 5, 6, 2, 3]`.
- [ ] I wrote the two-array version and the one-pass version, and they agree on random inputs.
- [ ] I broke the width on purpose and know what `[4, 3]` returns under the popped-index bug.
- [ ] I removed the sentinel and saw `[1, 2, 3, 4, 5]` return 0.
- [ ] I can explain why equal heights are safe, and which duplicate carries the full span.
- [ ] I solved maximal rectangle and can state its complexity before writing it.
- [ ] I can give the counting argument for O(n) without softening it.
- [ ] I refactored `place_order` to observers and counted the files edited for a sixth listener.
- [ ] I can name the three implementation details in `_notify` and what each one prevents.
- [ ] I can quote both latency totals, synchronous and through a broker.
- [ ] I can say the honest concession: the pattern buys decoupling, not speed.
- [ ] I answered all three questions above out loud.
