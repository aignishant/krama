---
day: 64
track: practice
title: "Practice — Grouping: the key-design skill"
status: written
---

# Day 064 · Practice

**DSA topic:** Grouping: the key-design skill
**System design topic:** Singleton

---

## Code these, in this order

One rule for the whole set: **say the belonging rule in words before you write the key.** "Two items
go in the same group when ___." If you cannot finish that sentence, you are not ready to write the
line, and every one of these problems is failed in that sentence rather than in the loop.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Group Anagrams | LeetCode 49 (Medium) | The standard vehicle. Whether you can defend the key, not whether you can write a `defaultdict`. |
| 2 | Find Duplicate File in System | LeetCode 609 (Medium) | Grouping by content rather than by name, and the cheap-key-first idea. |
| 3 | Group Shifted Strings | LeetCode 249 (Medium) | A key you have to invent, with a wrap-around case that most people miss. |
| 4 | Valid Sudoku | LeetCode 36 (Medium) | Three groupings at once, and the `(r // 3, c // 3)` key. |

### On problem 1, write it twice and time it

Once with `"".join(sorted(word))`, once with `tuple(counts of 26)`. Time both on 10,000 words of
length 10, then on 10,000 words of length 200. Say which won each time and why, and find the
crossover length yourself.

### On problem 2, order your keys by cost

Do not hash two million files. Group by size first, because two files of different sizes cannot be
equal and the size is free. Then hash only inside the groups that have more than one member. Then say
what you would do about a digest collision, and why "compare the bytes" is a real answer rather than
paranoia.

### On problem 3, find the wrap-around case before you submit

Your key is the gaps between consecutive letters. Test `"az"` and `"ba"`. If they are not grouped
together, you have forgotten `% 26`. Then say what happens to a one-character string, and why the
answer is correct rather than a bug.

### On problem 4, notice you already know the key

Rows, columns and boxes are three groupings of the same 81 cells. Write all three keys, then say why
one pass with three sets beats three passes.

### The key-design drill

For each of these, write the belonging sentence first, then the key, then run both tests on it:

1. Group words that are anagrams.
2. Group words that are anagrams, case-insensitively.
3. Group points that lie on the same line through the origin.
4. Group timestamps into hours.
5. Group people into age bands of ten years.
6. Group strings by their set of distinct characters.
7. Group numbers by their remainder when divided by 7.
8. Group employees by department and location.

Two of those eight have a key that is too coarse if you write the obvious thing. Find them, and give
the input that proves it.

### The too-coarse / too-fine drill

Each of these keys is wrong for grouping anagrams. Say which failure it is, and give the two words
that prove it:

1. `len(word)`
2. `frozenset(word)`
3. `word`
4. `(len(word), word[0])`
5. `sum(ord(c) for c in word)`
6. `tuple(sorted(set(word)))`

Number 5 is the interesting one — it is a real hash function and it is too coarse. Give a collision.

### The mechanics drill

Build the same grouping four ways and say when you would use each:

1. `defaultdict(list)`
2. `dict.setdefault(k, []).append(x)`
3. A plain `dict` with an explicit `if k not in groups`
4. `itertools.groupby`

Then, for 4, run it on the unsorted anagram list and count the groups. Run it on `sorted(words)` and
count again. Run it on `sorted(words, key=key)` and count again. Explain all three numbers.

### The break-it drill

Trigger each, read the exact output, and give the fix in one sentence:

1. Return `counts` (a list) as the key instead of `tuple(counts)`.
2. Use `itertools.groupby` on unsorted input.
3. Use `itertools.groupby` on input sorted by the item rather than by the key.
4. Check `if groups[k]:` on a `defaultdict(list)`, then print `len(groups)` and the output list.
5. Group anagrams with `frozenset(word)` and test on `"aab"` and `"abb"`.
6. Group shifted strings without `% 26` and test on `"az"` and `"ba"`.

### The singleton implementation drill

Write each version, then say what is wrong with it:

1. The naive check-then-create, and describe the race on a timeline.
2. Eager creation at import time.
3. A lock around the whole accessor.
4. Double-checked locking.
5. Overriding `__new__` — then set a field in `__init__`, call the class twice, and print the field.
6. A module-level object.
7. `@functools.cache` on a factory function.

Number 5 has a bug that produces no error. Say exactly what it is and what it would look like in
production.

### The singleton critique drill

For each situation, say whether a singleton is defensible, and give the deciding question:

1. A database connection pool.
2. An in-memory cache of user permissions.
3. A logging configuration read once at startup.
4. A rate limiter allowing 100 requests per second.
5. A stateless helper that formats currency.
6. Application settings, in a service that will soon be multi-tenant.
7. A metrics registry.
8. A clock, used by code that needs testing.

Two of the eight are defensible for the same reason, and two are indefensible for the same reason.
Name both reasons.

### The multi-process drill

Answer each with arithmetic:

1. A service runs 8 Gunicorn workers in 4 containers. How many instances of your singleton exist?
2. It is a 500 MB cache. What is your real memory requirement per node, and per deployment?
3. It is a rate limiter set to 100 requests per second. What is the actual system-wide limit?
4. Two of those caches disagree about a user's permissions. Describe the bug a user would report.
5. Where should the state have lived instead, and what does that cost?

### The replacement drill

Take this class and remove the singleton without removing the uniqueness:

```python
class ConnectionPool:
    _instance = None

    @classmethod
    def get_instance(cls) -> "ConnectionPool":
        if cls._instance is None:
            cls._instance = ConnectionPool()
        return cls._instance


class OrderService:
    def place(self, order):
        pool = ConnectionPool.get_instance()
        ...
```

1. Rewrite it so exactly one pool still exists, created in one place.
2. Count the lines you added.
3. Write the test for `OrderService.place` before and after. Count the setup lines in each.
4. Say what `OrderService.__init__`'s signature now tells a reader that it did not before.
5. Say which principle from [day 059](../day-059-sorting-revision/README.md) this satisfies, and
   which one the original violated.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Group these strings into anagram groups. What is your key?*
   The belonging sentence first, the key derived from it, both correctness tests run out loud, then
   the four-line loop, then the cost with n and k named — and the counting alternative with its real
   crossover rather than a recited O(k).

2. *Implement a thread-safe singleton. Now tell me why I should not use it.*
   The two claims separated, the race described on a timeline, the three fixes with their costs,
   the Java memory-model footnote, what you would actually write in Python — and then the criticism
   volunteered, ending on injection at the composition root.

3. *Why is `itertools.groupby` the wrong tool here?*
   Adjacent runs only, the three different counts you get on unsorted, item-sorted and key-sorted
   input, and the O(n log n) you would pay for a job the dictionary does in O(n).

---

## Before you move on

- [ ] I said the belonging sentence out loud before writing every key today.
- [ ] I ran both tests — too coarse and too fine — on at least three different keys.
- [ ] I timed the sorted key against the count key at k = 10 and k = 200, and found the crossover.
- [ ] I broke grouping with an unhashable key and read the exact error.
- [ ] I ran `groupby` three ways and can explain all three group counts.
- [ ] I proved that reading a missing key from a `defaultdict(list)` adds an empty group to my output.
- [ ] I wrote double-checked locking and can say why Java's version was broken until Java 5.
- [ ] I found the `__new__` bug by setting a field in `__init__` and calling the class twice.
- [ ] I can compute how many singletons exist across 4 containers of 8 workers, and what that breaks.
- [ ] I rewrote a singleton as an injected dependency and counted the test setup lines both ways.
- [ ] I answered all three questions above out loud.
