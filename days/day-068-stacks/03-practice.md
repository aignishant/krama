---
day: 68
track: practice
title: "Practice — Stacks: last in, first out"
status: written
---

# Day 068 · Practice

**DSA topic:** Stacks: last in, first out
**System design topic:** Adapter

---

## Code these, in this order

One rule for the whole set: **say the sentence before you write the loop.** *"The stack holds the
most recent ___ that has not yet been resolved."* Fill in the blank out loud. If you cannot, you have
not understood the problem yet, and the code will not save you.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Remove All Adjacent Duplicates In String | LeetCode 1047 (Easy) | The cancel-with-the-top pattern, and the `if stack and ...` guard. |
| 2 | Baseball Game | LeetCode 682 (Easy) | Reading a specification carefully while the stack part stays trivial. |
| 3 | Simplify Path | LeetCode 71 (Medium) | Real edge cases: `/../` at the root, `//`, and `"..."` being a legal name. |
| 4 | Backspace String Compare | LeetCode 844 (Easy) | Write it with a stack, then do it again in O(1) space with two pointers from the right. |

### On problem 1, break the guard on purpose

Write `if stack[-1] == character` without `if stack and`. Run it on `"a"`. Read the exact error. Then
fix it and say why the check has to be part of the same condition rather than a separate `if` above.

### On problem 3, test the four inputs that matter

`"/../"`, `"/home//foo/"`, `"/a/./b/../../c/"` and `"/..."`. The last one is the trap: three dots is
a legal directory name, so `part.startswith("..")` is wrong and `part == ".."` is right.

### On problem 4, do it twice

The stack version is six lines and O(n) space. Then the interviewer says "O(1) space", and the answer
is two pointers walking from the right, counting backspaces. Write both, and say which you would
offer first and why.

### The which-end drill

1. Time a million `append` + `pop` pairs.
2. Time a hundred thousand `insert(0, x)` + `pop(0)` pairs on a ten-thousand-element list.
3. Compute the ratio, and note that number 2 did ten times fewer operations.
4. Say why `insert(0, x)` is O(n) in one sentence, in terms of what has to move.
5. Now do the same with `collections.deque`. What changes, and why?
6. Say when you would choose `deque` over `list` for a stack.

### The recognition drill

For each problem, fill in the sentence *"the stack holds the most recent ___ not yet resolved"*, or
say that a stack is not the right structure:

1. Check whether brackets are balanced.
2. Implement browser back.
3. Implement browser forward as well.
4. Evaluate `3 + 4 * 2` respecting precedence.
5. Return the elements in the order they arrived.
6. Find the next greater element to the right of every element.
7. Undo the last five actions.
8. Serve customers in the order they queued.
9. Convert a recursive tree traversal to an iterative one.
10. Find the k most frequent words.

Three of the ten are not stack problems. Name them and say what each one wants instead.

### The empty-stack drill

Trigger each and quote the exact error:

1. `[].pop()`
2. `[][-1]`
3. `collections.deque().pop()`
4. `Stack().pop()` on your own class with no guard.

Then rewrite your `Stack.pop` and `Stack.peek` so the message mentions a stack rather than a list, and
say why that matters to a caller.

### The call-stack drill

1. Write `def r(n): return r(n + 1)` and call it. Quote the exact error and the default limit.
2. Raise the limit with `sys.setrecursionlimit(100000)` and try again. What happens, and why is that
   worse than the exception?
3. Write a recursive function that sums a list, then rewrite it with an explicit stack.
4. Say what the explicit-stack version is limited by instead.
5. Answer out loud: *"this tree is a million nodes deep — will your recursive solution work?"*

### The build-a-stack drill

1. Write `Stack` with `push`, `pop`, `peek`, `is_empty` and `__len__`.
2. Write `peek` as pop-then-push. Say two things wrong with it.
3. Now implement it over a **fixed-size** array. What does `push` have to do when it is full?
4. Implement doubling on overflow. Say why that makes push amortised O(1) and show the
   `8 + 16 + 32 + ...` sum.
5. Say what a linked-list implementation would change — which bound gets stronger, and what gets
   worse.
6. Say which one every standard library actually uses, and why.

### The counting-argument drill

For each, say why the code is O(n) despite having a loop inside a loop, or a pop inside a loop:

1. `remove_adjacent_duplicates`
2. `simplify_path`
3. A `while stack and stack[-1] < current: stack.pop()` inside a `for`.

The sentence is the same for all three. Say it exactly, and say what it would take to make one of
them genuinely quadratic.

### The adapter drill

Here is the vendor SDK you cannot edit:

```python
# vendor_sdk.py
class SmsVendor:
    def push_message(self, to_e164: str, body: str,
                     sender_id: str, unicode_flag: int) -> dict:
        """returns {"msg_id": "...", "state": "QUEUED"|"REJECTED", "cost_micros": 1200}"""
```

And here is what your code wants:

```python
class SmsSender(Protocol):
    def send(self, message: Message) -> Receipt: ...
```

1. Write the adapter.
2. Name every one of the four translations you performed, with the specific line that does each.
3. Their cost is in micro-rupees; yours is `Money` in paise. Write the conversion and say what breaks
   if you get it wrong.
4. Their `"REJECTED"` should become an exception in your vocabulary. Which one, and why not just
   return it?
5. Write a fake `SmsSender` for tests. Does it contain anything vendor-shaped? If yes, go back to
   step 1.
6. Say which package the `SmsSender` protocol lives in, and why the other option looks identical on a
   diagram.
7. Run the grep that proves the dependency was inverted. Write it out.

### The half-adapter drill

Here is an adapter that only did half the job:

```python
class StripeGateway:
    def charge(self, order: Order) -> dict:
        return self._client.create_charge(amount_cents=order.total_cents,
                                          source_token=order.token)
```

1. Name the three translations it skipped.
2. Write out a call site that uses it. What does the caller now know about Stripe?
3. Count how many call sites would change when you swap providers, given this adapter.
4. Say what the fake for this interface would have to look like.
5. Fix it, and say what the fake looks like now.

### The four-wrappers drill

For each, say which of adapter, decorator, facade or proxy it is, and give the one-sentence reason:

1. `functools.lru_cache` around a function.
2. `psycopg` presenting the DB-API interface.
3. `requests.get(url)`.
4. nginx in front of your application.
5. `io.TextIOWrapper` around a binary stream.
6. An ORM object that fires a query the first time you touch a field.
7. A class that adds logging around every method of a service, same interface.
8. `java.util.Arrays.asList()`.

One of the eight is also a Liskov violation shipped in a standard library. Name it and say why.

### The swap drill

You are moving from provider A to provider B.

1. Without an adapter: run a grep for the vendor name in a real project you have. How many
   references, in how many files?
2. With an adapter: how many files are added, and how many lines edited?
3. Describe how you would send 5% of traffic to B while keeping 95% on A. Which pattern from
   [day 065](../day-065-hashing-custom-objects/README.md) does the routing?
4. Name two things the adapter does *not* make the same between A and B.
5. Say the honest sentence about what an adapter buys and what it does not.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Implement a stack. What operations must be O(1)?*
   The restriction first and why it causes the O(1), the three operations, "a list is a stack" with
   the which-end warning and its number, amortised push explained in one sentence, and the two
   alternatives with the reason you would not use one of them.

2. *You must integrate a third-party SDK with a different interface. How?*
   Three parties named, the interface written before reading their docs, where it lives and whose
   vocabulary it uses, the four translations with the units emphasised, the fake-based test for
   whether it is real, and the honest limit.

3. *Why is a `while stack: pop()` inside a `for` loop still O(n)?*
   Each element pushed at most once and popped at most once, so the total pops are bounded by the
   total pushes — and what it would take to break that.

---

## Before you move on

- [ ] I can say the recognition sentence — "the most recent ___ not yet resolved" — from memory.
- [ ] I timed `append`/`pop` against `insert(0)`/`pop(0)` and can quote the ratio.
- [ ] I triggered `IndexError: pop from empty list` and know where the guard belongs.
- [ ] I found the `"..."` case in Simplify Path myself.
- [ ] I wrote `Stack` from scratch, including the fixed-size and doubling version.
- [ ] I can explain amortised O(1) push with the `8 + 16 + 32 + ...` sum.
- [ ] I hit `RecursionError` and can say why raising the limit is not a fix.
- [ ] I wrote a real adapter and named all four translations with the line that does each.
- [ ] I wrote the fake and confirmed it contains nothing vendor-shaped.
- [ ] I can separate adapter, decorator, facade and proxy in one sentence each.
- [ ] I answered all three questions above out loud.
