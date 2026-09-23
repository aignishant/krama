---
day: 60
track: practice
title: "Practice — Hash tables: how a dictionary finds anything instantly"
status: written
---

# Day 060 · Practice

**DSA topic:** Hash tables: how a dictionary finds anything instantly
**System design topic:** DRY, KISS, and YAGNI

---

## Code these, in this order

One rule for the whole set: **say what the key is and what the value is before you write anything.**
Half the difficulty of hash-map problems is choosing the key, and it is a decision you can state in
one sentence.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Design HashMap | LeetCode 706 (Easy) | Whether you can actually build one — buckets, collisions, and storing the key. |
| 2 | Two Sum | LeetCode 1 (Easy) | The canonical `O(n²)` → `O(n)` trade, and that the dict keeps the indices. |
| 3 | Group Anagrams | LeetCode 49 (Medium) | That the key can be *computed*, and that it must be hashable — a tuple, not a list. |
| 4 | First Unique Character in a String | LeetCode 387 (Easy) | Two passes, and Python's insertion-order guarantee doing real work. |

### On problem 1, build it with chaining

Do not use a `dict` inside. Use a list of lists, `hash(key) % capacity`, and store `(key, value)`
pairs. Then answer three things out loud: why the key is stored and not just the value, what happens
when you `put` a key that already exists, and when you would resize.

Then add the resize and print the load factor after every insert so you can watch it happen.

### On problem 2, say both costs before coding

Nested loops is `O(n²)` — five hundred billion operations at a million elements. The dict is `O(n)`
with `O(n)` space. Say both, then say the second reason the dict wins here: sorting would destroy the
indices the problem asks for.

### On problem 3, get the key right

`sorted(word)` returns a list, and a list cannot be a key. Try it, paste the `TypeError`, then fix it
with `tuple(sorted(word))`. Then say out loud why lists are unhashable, using the shoe-rack argument.

Then find a second valid key — a 26-length count tuple — and say which is better and at what word
length the answer changes.

### On problem 4, notice what you are relying on

Your solution almost certainly relies on dict iteration following insertion order. Say out loud
whether that is a guarantee or an accident, and from which Python version.

### The build-it drill

Write `HashMap` from memory, then check each:

1. `put` then `get` returns the value.
2. `put` the same key twice leaves one entry, not two.
3. `get` on a missing key returns the default rather than raising.
4. `delete` on a missing key raises `KeyError`.
5. Insert twenty items into a table starting at capacity four, and print capacity and load factor
   after each. How many resizes?
6. Print `bucket_sizes()` after inserting a hundred string keys. What is the maximum, and what would
   you expect?

### The bad-hash drill

1. Write a key class whose `__hash__` always returns 1.
2. Insert two hundred of them into your `HashMap` and print `max(bucket_sizes())`.
3. Time a lookup against a table with two hundred normal keys.
4. State the complexity of building the table in each case.
5. Say what real-world attack this is, and what Python does to prevent it.
6. Run `python -c "print(hash('apple'))"` twice. What do you see, and what two rules follow from it?

### The contract drill

For each, say whether it breaks the hash contract, and what the visible symptom is:

1. `__eq__` defined, `__hash__` not defined.
2. `__hash__` returning `id(self)` while `__eq__` compares a field.
3. `__hash__` computed from a field that changes.
4. `__hash__` returning a constant.
5. `__eq__` that returns `True` for objects with different hashes.
6. A frozen dataclass used as a key.

### The break-it drill

Trigger each, read the output, and say the fix:

1. `d[["a", "b"]] = 1` — paste the error.
2. A non-frozen `@dataclass` used as a dict key — paste the error.
3. An object whose hash field is mutated after insertion — what does `obj in d` return, and does
   anything raise?
4. `del d[key]` inside `for key in d:` — paste the error and give two fixes.
5. `3 in d` where 3 is a value — what does it return, and what is the cost of the version that
   works?
6. `counts["apple"] += 1` on an empty dict — paste the error and give three idiomatic fixes.

### The costs drill

Answer out loud, in under fifteen seconds each:

1. Why is lookup `O(1)`? Name the two assumptions it rests on.
2. What is the worst case, and what causes it?
3. What is the load factor, and where do implementations set it?
4. Why is insert `O(1)` amortised rather than `O(1)`? Give the sum.
5. What does one unlucky insert cost at a million items, and who cares?
6. How much memory does a dict cost compared with a list of the same values?
7. Why must a key be immutable?
8. What is the cost of `value in d.values()`?

### The DRY drill

For each pair, say whether it is real duplication or coincidental, name the fact if there is one, and
say what you would do:

1. `total = subtotal * 1.18` in three files.
2. `validate_customer_signup` and `validate_admin_signup`, identical today, owned by different teams.
3. Two API handlers that both parse a date from a query parameter the same way.
4. The retry logic in the payment client and in the email client, both "three attempts, exponential
   backoff".
5. A `Customer` class in the billing module and a `Customer` class in the support module.
6. The same twelve-line test setup in eight test functions.
7. Two report renderers that both open a file, write a header, write rows, and close.
8. The regex for a valid GST number, in the signup form and in the invoice generator.

Three of those eight are real duplication. Name them.

### The wrong-abstraction drill

Take the merged validator with five flags:

```python
def validate_signup(data, is_admin=False, min_password=8,
                    require_mfa=False, allow_plus_addressing=True):
    ...
```

1. Describe what this function does in one sentence, with no "and" and no "or". Can you?
2. How many distinct behaviours does it have? Count the flag combinations that are actually used.
3. Which callers pass which flags? What does that tell you about what the flags really encode?
4. Split it back into two functions. What is duplicated afterwards, and is that duplication real or
   coincidental?
5. Is there a genuine shared fact inside it? Extract that and only that.
6. Estimate the time for the split, and compare it with the twenty-four lines saved by the original
   merge.

### The YAGNI drill

For each, say whether you would build it now or wait, and give the reason:

1. Multi-currency support in a product selling only in India.
2. A `tenant_id` column on every table, in a single-tenant product that might go multi-tenant.
3. An audit trail of who changed what.
4. A plugin system for report formats, where two formats exist and both live in your repository.
5. A caching layer, before anything has been measured.
6. Database migrations, on day one of a project.
7. A `v2` API path with nothing behind it.
8. An interface over the payment gateway, when there is one gateway and no test fake.

Three of those eight should be built now. Name them and say what makes them different.

### The KISS drill

For each pair, say which you would choose and what specifically would have to be true for the other
one to win:

1. A dict of functions against a plugin registry with entry-point discovery.
2. A cron job against a message queue, for a task that runs nightly.
3. A single Postgres table against a separate service, for a feature with four fields.
4. A 40-line function with no cleverness against a 12-line one built from three generics.
5. A config file against a hard-coded constant, for something nobody has ever changed.
6. A monolith against microservices, for a team of four.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *How does a hash map work internally?*
   The compute-don't-search sentence, the three requirements on the hash function, collisions and why
   the key is stored, `O(1)` average against `O(n)` worst, and the resize with the amortised
   argument.

2. *Is this duplication worth removing?*
   Ask the question back, state DRY in terms of knowledge, give the would-they-always-change-together
   test and the who-owns-it test, describe the flag-accumulation failure, and give the asymmetry
   number.

3. *Why must a dictionary key be immutable?*
   The find-it-again argument, the demonstration where `obj in d` returns `False` for an object
   sitting in the dict, and the `a == b` implies `hash(a) == hash(b)` contract.

---

## Before you move on

- [ ] I built a working `HashMap` with chaining and resizing from memory.
- [ ] I can say why the key is stored alongside the value, without being prompted.
- [ ] I made a hash function that always returns 1 and watched every lookup become `O(n)`.
- [ ] I can give the amortised argument for the resize, including the doubling sum.
- [ ] I mutated a key after insertion and confirmed the entry became unfindable with no error.
- [ ] I can classify the eight duplication cases and name the three that are real.
- [ ] I can describe the flag-accumulation failure with its timeline and its cost.
- [ ] I answered all three questions above out loud.
