---
day: 70
track: practice
title: "Practice — Min stack, and stacks that carry extra state"
status: written
---

# Day 070 · Practice

**DSA topic:** Min stack, and stacks that carry extra state
**System design topic:** Facade and proxy

---

## Code these, in this order

One rule for the whole set: **say the observation before writing the code.** "A stack only changes at
the top, so the answer before a push is the answer after the matching pop." Every problem below is
that sentence with a different aggregate in it, and saying it first turns four problems into one.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Min Stack | LeetCode 155 (Medium) | The observation, and the `<=` duplicate trap in the two-stack variant. |
| 2 | Max Stack | LeetCode 716 (Hard) | One comparison flipped — until `popMax` is asked for, and then it is a different problem. |
| 3 | Design a Stack With Increment Operation | LeetCode 1381 (Medium) | Lazy increments carried per element: the same idea with a different aggregate. |
| 4 | Maximum Frequency Stack | LeetCode 895 (Hard) | Extra state that is a map of stacks. The senior version of today. |

### On problem 1, write both versions and break one

Write the pairs version first. Then write the two-stack version with `<` and run `push(3)`,
`push(3)`, `pop()`, `get_min()`. Read the exact error. Change one character and run it again.

### On problem 2, notice where the technique stops

`push`, `pop`, `top` and `peekMax` are today's idea with `max` instead of `min`. Then `popMax` — remove
the maximum from anywhere in the stack — is not, because it changes the middle. Say out loud why
today's trick cannot help, and what structure you would reach for instead.

### On problem 3, find the aggregate

The increment applies to the bottom `k` elements. Doing it eagerly is O(k). Say what you would store
per element so that `pop` applies the right total in O(1), and why that is still the same technique.

### On problem 4, say what is being carried

Not a number this time. Say out loud what the extra state is, and why a stack per frequency is the
right shape rather than one stack of pairs.

### The observation drill

Say each of these out loud, then check it:

1. Why does `pop` need no work at all in the pairs version?
2. What property of a stack makes that true, that a queue does not have?
3. Where did the cost of `get_min` go? It did not disappear.
4. What would break if you kept a single `self._min` variable and nothing else?
5. Why can the same trick not give you the median?

### The duplicate drill

Using the two-stack version:

1. Write it with `<`. Run `push(3)`, `push(3)`, `pop()`, `get_min()`. Quote the exact output.
2. Now with three elements underneath, so it returns a wrong answer instead of raising. Construct
   that input.
3. Change `<` to `<=`. Trace the min stack after each of the four operations.
4. Say why the matching `pop` must use `==` and not `<=`.
5. Say what the pairs version does about this problem, and why.

### The space drill

For each input, say how many entries the optimised two-stack version holds in its min stack:

1. `[1, 2, 3, 4, 5]`
2. `[5, 4, 3, 2, 1]`
3. `[3, 3, 3, 3, 3]`
4. `[5, 1, 5, 1, 5]`
5. A random permutation of 1 to 1000

Then state the best case and the worst case as multiples of n, and say whether you would describe the
optimisation as saving memory.

### The aggregate drill

For each, say whether today's technique works, and give the reason:

1. Minimum
2. Maximum
3. Sum
4. Count of elements
5. Product
6. Average
7. Median
8. Most frequent element
9. Second smallest
10. Range (max minus min)

Three of the ten do not work. Name the property they all fail, in one sentence. For number 6, say
what you would actually store.

### The encoded-trick drill

1. Implement the O(1)-extra-space version with `2 * value - min`.
2. Prove to yourself that the encoded value is always strictly less than the new minimum.
3. Show that `2 * min - stored` recovers the previous minimum.
4. What does `top()` have to do differently?
5. In Java with `int`, find two values where `2 * value - min` overflows.
6. Say whether you would write this in an interview, and under what condition.

### The four-wrappers drill, final version

Sort each into adapter, decorator, facade or proxy. Say which of the two separating questions you
used first.

1. `requests.get(url)`
2. nginx in front of your application
3. `functools.lru_cache`
4. `psycopg` presenting the DB-API
5. An ORM's lazy `order.customer`
6. A gRPC client stub
7. A class adding retry around a service, same interface
8. `CheckoutFacade.checkout(cart, user)`
9. `io.TextIOWrapper`
10. Spring's `@Transactional` wrapper

Two of the ten have identical structure and different intent. Name them, give the test that
separates them, and say why it is honest to admit the structures are the same.

### The checkout drill

You have six services: inventory, pricing, payments, orders, shipping, notifications.

1. Write the facade method with the six calls in the correct order.
2. For each ordering constraint, write the one-line comment saying what breaks if it is violated.
3. Count the coupling edges with nine callers, with and without the facade.
4. Payment succeeds and order creation fails. Write what the facade does.
5. The client retries. What stops the customer being charged twice?
6. Somebody asks you to add "apply an 18% tax for Indian customers" to the facade. Say no, and say
   where it goes instead.
7. Reporting wants to query orders directly. Allow it or forbid it? Defend your answer.

### The gateway drill

A mobile home screen needs data from six services.

1. Six sequential calls at a 120 ms mobile round trip. Total?
2. Six parallel calls. Total, and what else does the client pay six times?
3. One gateway call, fanning out inside the data centre at a 1 ms round trip. Total?
4. Payload: 40 KB of six raw responses versus a shaped response. Estimate the shaped size.
5. Web and mobile want different shapes. One gateway or two? Name the pattern.
6. What does the gateway now become a single point of, and what would you do about it?

### The proxy-hazard drill

For each, say which kind of proxy it is and what goes wrong because it is invisible:

1. A loop over 100 orders touching `order.customer`.
2. A gRPC stub call inside a tight loop.
3. A `@Transactional` method called from another method of the same class.
4. A caching proxy in front of a permission check.
5. A CDN serving a page that has just been updated.

Then, for numbers 1 and 3, write the exact fix in one line each.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Design a stack that returns its minimum in constant time.*
   The naive cost first, the observation stated before any code, the pairs version, the two-stack
   variant with its `<=` trap volunteered, the space cost, and the O(1)-space trick mentioned with
   its overflow caveat.

2. *Your checkout touches six services. How do you expose it to the client?*
   The facade with what it actually removes (ordering and failure policy), the compensation and
   idempotency answer, the two rules, the coupling-edge arithmetic, and the jump to API gateway with
   the 720 ms versus 125 ms number.

3. *What is the difference between a facade and a proxy?*
   New-and-simpler over many versus same-over-one controlling access, the two separating questions,
   and the honest admission that proxy and decorator are structurally identical.

---

## Before you move on

- [ ] I can state the observation — why `pop` does no work — in one sentence, from memory.
- [ ] I broke the two-stack version with `<` and know the exact input and output.
- [ ] I can say the best-case and worst-case size of the optimised min stack.
- [ ] I can name three aggregates this technique cannot carry, and the property they fail.
- [ ] I wrote the max stack and the sum stack and saw that only one line changed.
- [ ] I know why `popMax` is not the same problem.
- [ ] I can sort all four wrapping patterns using the two separating questions.
- [ ] I wrote the checkout facade with the ordering comments and answered the failure question.
- [ ] I can quote the coupling-edge arithmetic and the mobile round-trip arithmetic.
- [ ] I can name the two rules that stop a facade becoming a god object.
- [ ] I can explain why `@Transactional` does nothing on self-invocation.
- [ ] I answered all three questions above out loud.
