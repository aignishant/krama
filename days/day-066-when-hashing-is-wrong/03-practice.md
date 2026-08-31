---
day: 66
track: practice
title: "Practice — When a hash map is the wrong answer"
status: written
---

# Day 066 · Practice

**DSA topic:** When a hash map is the wrong answer
**System design topic:** Builder

---

## Code these, in this order

One rule for the whole set: **solve each one with a hash map first, then take the map away.** Writing
the easy answer and then removing it is exactly the interview shape, and doing it in that order here
is what makes it available to you under pressure.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Two Sum II — Input Array Is Sorted | LeetCode 167 (Medium) | Whether you notice the word "sorted" and drop the map for two pointers. |
| 2 | Find All Numbers Disappeared in an Array | LeetCode 448 (Easy) | The marking trick, without the cleaning pass to complicate it. |
| 3 | Find the Duplicate Number | LeetCode 287 (Medium) | O(1) space with the input read-only — so marking is banned too. |
| 4 | First Missing Positive | LeetCode 41 (Hard) | The bound nobody gives you, and the `-abs` line. |

### On problem 1, say what "sorted" bought you

Write the hash-map version, state its space, then write two pointers. Then answer out loud: what
would you do if the array were *not* sorted and O(1) space were still required? Say both the cost of
sorting it yourself and whether you are allowed to.

### On problem 3, notice the constraint that kills your first two answers

The array is read-only *and* space is O(1), so neither the set nor the marking trick is available.
The intended answer is Floyd's cycle detection from
[day 030](../day-030-fast-and-slow/README.md), treating values as pointers. Say out loud why the
values being in `1..n` is what makes the array a valid function to walk.

### On problem 4, run `[1, 1]` before you submit

Write the marking line as `-numbers[v-1]` first. Run `[1, 1]`. Get `1` instead of `2`. Then change it
to `-abs(numbers[v-1])` and run it again. Do this once and you will never write it wrong.

### The three-cases drill

For each problem, say which of the three cases applies — space taken away, small dense keys, or order
needed — and what you would use instead of a map:

1. "Find the duplicate, O(1) space."
2. "Count the letters in a string of a million characters."
3. "Which orders were placed between these two timestamps?"
4. "What is the third-largest score?"
5. "The values are all between 1 and n. Find the missing one."
6. "Return the elements in ascending order of frequency."
7. "Is this ASCII string made of unique characters, in O(1) space?"
8. "Which key comes immediately after 'kumar' alphabetically?"

Two of the eight need *two* structures, not one. Name them and say which two.

### The space drill

Measure each on a million small integers, then tabulate:

1. `sys.getsizeof(list(range(1_000_000)))`
2. `sys.getsizeof(set(range(1_000_000)))`
3. `sys.getsizeof({i: 1 for i in range(1_000_000)})`

Then answer: why is the set roughly four times the list? Name the three reasons, and say which of
them a plain list does not pay.

### The small-n drill

Time a million membership tests against a set and against a list, at n = 4, 8, 16, 64, 256, 1024.

1. Tabulate the ratio at each size.
2. Where does the set become clearly worth it?
3. Now add the cost of *building* the set to the comparison. Where is the break-even now?
4. State the rule of thumb you would actually use in an interview, and say it is a rule of thumb.

### The direct-addressing drill

For each, say whether direct addressing is appropriate and why:

1. Counting lowercase English letters.
2. Counting arbitrary Unicode characters.
3. Counting HTTP status codes seen in a log.
4. Counting user ids seen in a log, where ids are random 64-bit integers.
5. Counting values known to be between 1 and n, where n is the array length.
6. Counting ages of people, 0 to 120.

Two of the six would allocate absurd amounts of memory. Say how much, with arithmetic.

### The marking drill

Using `[4, 3, 2, 7, 8, 2, 3, 1]`:

1. Run the marking pass by hand and write out the array after every step.
2. Which slots are still positive at the end? What does that mean?
3. Now do it with `-x` instead of `-abs(x)` and find the step where it goes wrong.
4. Reconstruct the original array from the marked one. What information was preserved, and where?
5. Say what would break if the array contained a zero, and what the cleaning pass does about it.
6. Say what would break if the array contained `10**9`, and what the cleaning pass does about it.

### The ask-first drill

For each, say what question you would ask the interviewer before writing anything, and what you would
do for each possible answer:

1. You want to sort the input in place.
2. You want to mark inside the input with sign bits.
3. You want to return the result in the original order.
4. You want to assume all values are positive.
5. You want to assume the values fit in a machine integer.

One of these five questions is worth asking in almost every array problem. Which, and why?

### The twelve-parameter drill

Here is the constructor:

```python
class Cake:
    def __init__(self, weight_kg, flavour, eggless, finish, message,
                 photo, delivery, delivery_time, tier_count, colour,
                 candles, note):
        ...
```

1. Write out one realistic call, positionally. Count how many arguments a reader must look up.
2. How many of the twelve are optional? How many combinations is that?
3. Find the data clumps. How many parameters collapse into value objects, and into what?
4. Rewrite it as a frozen, keyword-only dataclass with defaults. Count the lines.
5. Write two cross-field rules that no setter could enforce, and put them in `__post_init__`.
6. Now write the fluent builder version. Count the lines.
7. State what the builder buys over the dataclass here, honestly. If the answer is nothing, say so.
8. Name the compile-time guarantee the builder gave up.

### The builder-or-not drill

For each, say whether you would write a builder in Python, and give the deciding reason:

1. A `Point` with `x` and `y`.
2. An HTTP request with a URL, method, ten optional headers, a body and a timeout.
3. An object assembled from three different callbacks as a file is parsed.
4. A configuration where premium users get two extra steps and free users do not.
5. An `Order` used in sixty tests, each of which cares about two fields.
6. A `Cake` with twelve fields, all required.
7. A `Report` whose assembly takes four seconds and should happen once.

Two of the seven are "no" for the same reason. Name it.

### The test-data-builder drill

Write a test that needs an `Order` with a `Customer`, an `Address` and three `OrderLine`s, where the
test only cares that the order is already paid.

1. Write the setup without a builder. Count the lines.
2. Count how many of those lines the test actually cares about.
3. Write a test data builder with sensible defaults.
4. Rewrite the setup with it. Count the lines again.
5. Now add a thirteenth field to `Order`. How many files change in each version?
6. Say which of those two numbers would actually persuade a team, and why.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *You used a hash map. Could you do it in O(1) space instead?*
   What the map was buying, the three replacements named before one is chosen, the "may I modify the
   input" question asked out loud, and the bound found and stated before any code is written.

2. *This constructor takes twelve parameters. Fix it.*
   The value-object question first, then what is actually wrong with twelve, then the Python answer
   (frozen keyword-only dataclass) before the pattern answer, then the four cases where you would
   still build one, then the compile-time guarantee you gave up.

3. *When would you not use a hash map?*
   The three cases with an example each, plus the three smaller reasons — memory, tiny n, and
   adversarial keys — and the sentence about O(1) being an average rather than a bound.

---

## Before you move on

- [ ] I solved at least two problems with a map first and then removed it.
- [ ] I ran `[1, 1]` through First Missing Positive with `-x` and watched it return the wrong answer.
- [ ] I can state why the answer is bounded by n + 1, in one sentence, without hesitating.
- [ ] I asked "may I modify the input?" out loud before every in-place solution today.
- [ ] I measured list, set and dict memory on a million integers and can quote all three.
- [ ] I found the small-n break-even myself, including the cost of building the set.
- [ ] I can name the three ordering questions a hash map cannot answer, and what to use instead.
- [ ] I found the data clumps in the twelve-parameter constructor before reaching for a pattern.
- [ ] I wrote both the dataclass and the builder version and can say honestly what the builder added.
- [ ] I can name the compile-time guarantee Builder gives up, and the four cases where it is worth it.
- [ ] I answered all three questions above out loud.
