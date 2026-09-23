---
day: 69
track: practice
title: "Practice — Balanced brackets and the parsing family"
status: written
---

# Day 069 · Practice

**DSA topic:** Balanced brackets and the parsing family
**System design topic:** Decorator

---

## Code these, in this order

One rule for the whole set: **name the three failure modes out loud before writing any of them.**
Wrong type on top, closer with nothing open, something still open at the end. Every problem below
fails in one of those three ways, and saying them first is what stops you discovering them from a
failing test.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Valid Parentheses | LeetCode 20 (Easy) | All three failures, and whether you map closer→opener or the wrong way round. |
| 2 | Minimum Add to Make Parentheses Valid | LeetCode 921 (Medium) | Two counters instead of a stack — whether you noticed the stack was not needed. |
| 3 | Evaluate Reverse Polish Notation | LeetCode 150 (Medium) | Operand order, which only `-` and `/` expose. |
| 4 | Decode String | LeetCode 394 (Medium) | Pushing a *context*, multi-digit counts, and which side of the concatenation goes where. |

### On problem 1, break it three ways on purpose

Write it without the emptiness check and run `"]"`. Write it without the end-of-string check and run
`"((("`. Write it with the map keyed by opener and see how awkward the lookup becomes. Then fix all
three and say which one you would have shipped.

### On problem 2, notice the stack disappeared

You do not need one. Two integers do it in O(1) space, because with a single bracket type you never
need to remember *which* bracket is open. Say out loud what would have to change for the stack to
come back.

### On problem 3, find the operand-order bug

Write `left = stack.pop()` first, then `right`. Test with `["2","1","+","3","*"]` — it passes.
Then test `["4","13","5","/","+"]` — it fails. Say why `+` and `*` hid it.

### On problem 4, test `"12[a]"` before anything else

If you get `"aa"` instead of twelve a's, your digit accumulation is `int(character)` instead of
`number * 10 + int(character)`. Then test `"a2[b]"` to check the concatenation side.

### The three-failures drill

For each input, say which of the three failure modes it triggers, or that it is valid:

1. `"()"`
2. `"([)]"`
3. `"())"`
4. `"(()"`
5. `""`
6. `"]"`
7. `"({[]})"`
8. `")("`
9. `"((("`
10. `"{[()]}"`

Then say which single input you would use to test each of the three checks, and why one-character
inputs are the most valuable tests here.

### The counting drill

1. Write the counting version for one bracket type. What is its space complexity?
2. Find an input with **three** bracket types where the counts all match and the string is invalid.
3. Would three separate counters fix it? Give the input that defeats them too.
4. State in one sentence what counting throws away.
5. Say when you would offer the counting version in an interview.

### The context drill

For each problem, say what gets pushed on the opener and what happens on the closer:

1. Valid parentheses.
2. Decode String.
3. Basic Calculator (`"1 + (2 - (3 + 4))"`).
4. Reverse Polish notation.
5. A compiler reporting "unmatched `{` opened at line 41".
6. Validating XML with named tags.

Number 5 pushes one thing more than number 1 does. What, and what does it buy the user?

### The complexity drill

1. What is the time complexity of `is_balanced`? Count the loop.
2. What is its worst-case space, and what input causes it?
3. What is its best-case space, and what input causes it?
4. What is the time complexity of `decode_string`? Be careful — say it in terms of the right thing.
5. Give an input to `decode_string` that is 13 characters long and produces 1,000 characters.
6. Say the one sentence that explains why a `pop` inside a `for` loop is still linear.

### The decorator-versus-inheritance drill

You have a `PriceService` and want logging, caching, retry and timing.

1. How many subclasses would inheritance need to cover every combination?
2. How many classes does the decorator approach need?
3. Write out three of the subclass names to see the problem.
4. Which logic would be duplicated across the subclasses?
5. How many classes and edits does a fifth feature cost in each approach?
6. Write the composition line for logged + cached + timed, without retry.

### The ordering drill

For each pair, say what each ordering does differently and which you would choose:

1. `Cached(Logged(real))` versus `Logged(Cached(real))`
2. `Retry(Timeout(real))` versus `Timeout(Retry(real))`
3. `Auth(Cached(real))` versus `Cached(Auth(real))`
4. `RateLimit(Retry(real))` versus `Retry(RateLimit(real))`
5. `Metrics(Cached(real))` versus `Cached(Metrics(real))`

One of the five is not a preference — it is a security bug. Name it and say exactly what goes wrong.

### The measurement drill

Build a real four-layer stack and measure it:

1. Time a bare method call.
2. Time it through one decorator.
3. Time it through four.
4. Compute the per-layer overhead.
5. Now put a 2 ms sleep in the real method and recompute the overhead as a percentage.
6. Say the condition under which the overhead matters, with a number.

### The Python-syntax drill

1. Write a `@timed` decorator without `functools.wraps`. Print the decorated function's `__name__`
   and `__doc__`.
2. Add `@wraps` and print them again.
3. Name two real tools that break when `__name__` is wrong.
4. Say the one thing the `@` syntax cannot do that an object decorator can.
5. Write a composition that caches in production and does not cache in tests. Could you do it with
   `@lru_cache`?

### The forwarding drill

You have an interface with 15 methods and a decorator that only changes one.

1. Write it the explicit way. How many forwarding methods?
2. Write it with `__getattr__`.
3. What do you lose by using `__getattr__`?
4. What happens when a sixteenth method is added, in each version?
5. Say which you would choose for a library, and which for application code.

### The four-wrappers drill, again

Now that you have seen both, sort these into adapter, decorator, facade or proxy, and say the
distinguishing question you used:

1. `BufferedReader(new InputStreamReader(new FileInputStream(f)))`
2. `psycopg` presenting the DB-API
3. Django's `MIDDLEWARE` list
4. An ORM's lazy-loading object
5. `requests.get(url)`
6. `functools.lru_cache`
7. nginx in front of your app
8. A class adding retry around a service, same interface

Two of the eight have identical structure and different intent. Name them and give the test that
tells them apart.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Check whether the brackets in this string are balanced.*
   The three failure modes named before any code, the invariant, why counting fails with the
   `"([)]"` example, the clarifying question about other characters, and both space cases.

2. *Add logging and caching to this service without changing its code.*
   The defining property, the `2ⁿ` versus `n` arithmetic, the composition line read out loud, the
   ordering point volunteered with its numbers, and the Python-syntax distinction.

3. *Does the order of your decorators matter?*
   Yes, with the cache-and-logger example and the 600-versus-4,000 number, retry versus timeout, and
   the auth case that is a security bug rather than a preference.

---

## Before you move on

- [ ] I can name the three bracket failure modes from memory, in order.
- [ ] I broke the code three separate ways and know which input exposes each.
- [ ] I can give an input where the counts match and the string is invalid.
- [ ] I wrote the O(1)-space version and can say exactly why it only works for one bracket type.
- [ ] I found the RPN operand-order bug myself, using an input where `-` or `/` exposes it.
- [ ] I tested `"12[a]"` and `"a2[b]"` on Decode String.
- [ ] I can state Decode String's complexity in terms of the output, and give the 13-in/1000-out input.
- [ ] I can quote the `2ⁿ` versus `n` arithmetic for decorators.
- [ ] I can give three concrete ordering pairs and say what changes in each.
- [ ] I know which decorator ordering is a security bug and why.
- [ ] I measured the per-layer overhead myself and can say when it matters.
- [ ] I answered all three questions above out loud.
