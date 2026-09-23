---
day: 63
track: dsa
title: "Counting with dictionaries"
phase: "Hashing: maps and sets"
status: written
---

# Day 063 · DSA — Counting with dictionaries

**After today you can:** You can build, update and query frequency maps without KeyError.

**The interviewer asks it as:** *Find the top k most frequent elements.*

---

## 1. What this is, and why they ask it

A **frequency map** is a dictionary whose keys are the things you are counting and whose values are
how many times each one appeared. You build it in one pass over the data, bumping a number as you go.
It is the second half of the set: a set remembers *whether* you have seen something, a frequency map
remembers *how many times*.

They ask it because counting is the most common single step in the whole of interview coding. Top k
frequent elements, valid anagram, first non-repeating character, majority element, ransom note,
longest substring with at most k distinct characters — all of them start with the same three lines.
An interviewer who gives you one of those is not testing whether you can count. They are testing
whether the counting is automatic enough that you have thought left over for the part that is
actually hard, which is usually what you do with the counts afterwards.

There is a second thing being tested, and it is more specific. Once you have counts, "give me the top
k" has three different answers with three different complexities — sort them, use a heap, or bucket
them — and knowing all three, and when each wins, is a very reliable way to turn a medium question
into a good conversation.

---

## 2. The story

Shobha has been sending lunch boxes to four offices near the flyover in Malleswaram for six years.
Forty-one people, six days a week, and she cooks everything herself between five and nine in the
morning.

The orders arrive on her phone from about half past nine the night before. They come in one at a
time, in no particular order, and they are all one line — bisi bele bath, curd rice, two lemon rice,
chapati and palya, curd rice again. By eleven at night there are forty-one of them.

For the first year she used to read the whole lot of them over and over. Once through for the curd
rice. Then back to the top and once through again to count the lemon rice. Then again for the
chapati. Four dishes, four times through forty-one messages, and if she lost her place she started
that dish again. It took nearly half an hour and she got it wrong twice, which meant somebody at an
office got a box with the wrong thing in it and rang her about it.

Her son fixed it in about a minute, with a whiteboard and a marker on the kitchen wall.

Now she goes through the messages exactly once, from the top. She reads one, finds that dish on the
board, and adds one to the number next to it. Reads the next, adds one. When a dish comes up that is
not on the board at all — somebody asks for pulao, which nobody has asked for in two months — she
writes the name on the board with a one next to it, and carries on. That is the only moment she has
to stop and think.

By the end of the messages every dish has its total, and she has read each message once. Eleven minutes
instead of half an hour, and she has not got it wrong since.

The bit her son was pleased about is that it does not get worse. When the fifth office joined and it
went from forty-one boxes to sixty-three, it took a bit longer, but only a bit — sixty-three messages
instead of forty-one. The old way would have got worse four times over, because she was reading the
whole lot of messages once for every dish.

---

## 3. The idea in plain English

The whiteboard is a **dictionary**. Each dish name is a **key** and the number next to it is the
**value**. Going through the messages once and bumping a number is building a **frequency map**, also
called a **count map** or a **counter** — all three names mean the same thing and interviewers use
all three.

The old way — reading everything once per dish — is the nested loop. With `n` messages and `m`
distinct dishes it is `n × m` reads. The whiteboard way is `n` reads and `n` bumps, whatever `m` is.

And the moment Shobha has to stop and think — a dish that is not on the board yet — is the **missing
key**, which is the one part of this that goes wrong in code.

### The three lines

```python
counts: dict[str, int] = {}
for dish in orders:
    counts[dish] = counts.get(dish, 0) + 1
```

`counts.get(dish, 0)` means: give me the current count, or 0 if this dish is not on the board yet.
Add one. Store it back. Those three lines handle both cases — the dish that is already there and the
dish that is not — without an `if`.

### Why not just `counts[dish] += 1`?

Because that is the missing-key problem, and it is the error you will actually hit:

```python
>>> counts = {}
>>> counts["pulao"] += 1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'pulao'
```

`counts["pulao"] += 1` means *read the value, add one, write it back*, and the read fails because
there is nothing to read. Python is not being awkward: on a fresh board there is no number next to
pulao to add one to.

### The four ways, and when to use each

You will see all four in other people's code, so you need to read all four. You only need to write
one.

**One — the explicit `if`.** Verbose, but nothing is hidden.

```python
if dish in counts:
    counts[dish] += 1
else:
    counts[dish] = 1
```

**Two — `.get` with a default.** The one to write in an interview when you want no imports.

```python
counts[dish] = counts.get(dish, 0) + 1
```

**Three — `defaultdict(int)`.** A dictionary that invents a zero the first time you touch a key.

```python
from collections import defaultdict
counts = defaultdict(int)
for dish in orders:
    counts[dish] += 1        # no KeyError — the missing key is born as 0
```

**Four — `Counter`.** The whole loop, in one line.

```python
from collections import Counter
counts = Counter(orders)     # Counter({'curd rice': 12, 'lemon rice': 9, ...})
```

`Counter` is a dictionary subclass, so everything you know about dictionaries still works on it. In
an interview, write `Counter` and then say "if you would rather see the loop, it is three lines" —
that shows you know the library without hiding behind it.

### What `Counter` gives you beyond counting

```python
c = Counter("aabbbc")
c["z"]                # 0  — a missing key is 0, not a KeyError
c.most_common(2)      # [('b', 3), ('a', 2)]  — sorted by count, descending
c.most_common()       # everything, descending
list(c.elements())    # ['a','a','b','b','b','c']  — back to the original multiset
Counter("aabbc") - Counter("abz")   # Counter({'a': 1, 'b': 1, 'c': 1})
```

Two of those are worth pausing on.

`c["z"]` returning `0` is convenient and it is a trap. On a plain dictionary a typo raises
`KeyError` and you find it immediately. On a `Counter` a typo silently returns 0 and your answer is
quietly wrong.

`Counter - Counter` drops zero and negative counts, which is exactly what you want for questions like
"can I build this word from these letters" and exactly not what you want if you were expecting
arithmetic. `Counter("ab") - Counter("abz")` is `Counter()` — the `z` does not appear as `-1`.

### Counting by something derived from the element

This is the step that turns counting into a technique rather than a chore. The key does not have to
be the element. It can be anything you compute from it.

```python
Counter(len(word) for word in words)          # how many words of each length
Counter(word[0] for word in words)            # how many words start with each letter
Counter("".join(sorted(w)) for w in words)    # how many words share each letter-multiset
```

That third one is the anagram key, and it is [day 064](../day-064-grouping/README.md)'s entire
subject. Choosing the key *is* the problem, in a very large number of questions.

### Getting the top k out

Once you have counts, "the k most frequent" has three answers.

- **Sort everything.** `sorted(counts.items(), key=lambda kv: -kv[1])[:k]`. Simple, O(m log m).
- **A heap.** `counts.most_common(k)` uses one internally: O(m log k). Better when k is small and m
  is large.
- **Bucket by count.** Because a count can never exceed `n`, you can make a list of `n + 1` buckets
  and drop each key into the bucket for its count, then read the buckets from the top. O(n + m) — no
  logarithm at all.

All three are correct. Which one you offer, and whether you can say why, is the question.

---

## 4. The picture

The frequency map being built, one element at a time. The input is a stream of dish codes.

```
 orders:   C   L   C   B   C   L   P
           |   |   |   |   |   |   |
 step 1    C:1
 step 2    C:1  L:1
 step 3    C:2  L:1
 step 4    C:2  L:1  B:1
 step 5    C:3  L:1  B:1
 step 6    C:3  L:2  B:1
 step 7    C:3  L:2  B:1  P:1     <- P is new: the missing-key moment
```

Notice steps 3, 5 and 6. Those are the cheap ones — the key exists, so it is a read and a write, no
decision. Steps 1, 2, 4 and 7 are the ones where the key had to be created. **`counts.get(k, 0)`
makes those two cases look identical in the code**, which is the whole reason to write it that way.

Now the bucket trick for top k, drawn on the finished counts `{C:3, L:2, B:1, P:1}` with n = 7:

```
 count:     0     1        2      3      4      5      6      7
          +----+--------+------+------+------+------+------+------+
 bucket   | [] | [B,P]  | [L]  | [C]  |  []  |  []  |  []  |  []  |
          +----+--------+------+------+------+------+------+------+
                                  ^
                          walk from the right,
                          collect until you have k
```

What to notice: there are exactly `n + 1` buckets, because no element can appear more than `n` times.
That bound is why this is O(n) and not O(n log n) — you never sort anything, you just walk a list you
already know the length of.

---

## 5. The code, built step by step

Three small ones to get the shape into your fingers, then the real question.

### Step 1 — is this an anagram?

```python
from collections import Counter

def is_anagram(first: str, second: str) -> bool:
    return Counter(first) == Counter(second)
```

Two strings are anagrams if their letter counts match. `Counter.__eq__` compares the dictionaries, so
this is one line and it is O(n). Worth saying: the sorting answer, `sorted(first) == sorted(second)`,
is also one line and is O(n log n). Counting wins on time; sorting wins on space when the alphabet is
huge. Mention both — this is a
[day 022](../day-022-anagrams/README.md) question and the interviewer expects the comparison.

### Step 2 — the first character that does not repeat

```python
def first_unique(text: str) -> str | None:
    counts = Counter(text)
    for character in text:          # walk the ORIGINAL, not the counter
        if counts[character] == 1:
            return character
    return None
```

Two passes, and the second one matters. You must walk the original string, not the dictionary,
because the question asks for the *first* such character and only the original knows the order. This
is the single commonest mistake in this problem.

### Step 3 — the majority element

```python
def majority(numbers: list[int]) -> int:
    counts = Counter(numbers)
    return counts.most_common(1)[0][0]
```

`most_common(1)` returns a list of one `(value, count)` pair, so the indexing is `[0][0]`. It is
ugly and it is correct. If the interviewer then says "O(1) space", the answer is the Boyer-Moore
voting algorithm, and you should say so even if you do not write it: keep one candidate and one
count, increment on a match, decrement otherwise, and the survivor is the majority.

### Step 4 — top k frequent elements

Given `[1, 1, 1, 2, 2, 3]` and `k = 2`, return `[1, 2]`. This is LeetCode 347, and the interesting
part is that there are three answers.

Start the same way, always:

```python
counts = Counter(numbers)      # O(n)
```

**Answer A — sort the counts.**

```python
ordered = sorted(counts, key=counts.get, reverse=True)
return ordered[:k]
```

`m` distinct values, so O(m log m). Perfectly acceptable, and the one to write first if you are
short of time. Say the complexity as you write it.

**Answer B — a heap of size k.**

```python
import heapq
return heapq.nlargest(k, counts, key=counts.get)
```

O(m log k). When k is 10 and m is a million, log k is about 3 and log m is about 20, so this is
roughly seven times less comparison work. This is what `most_common(k)` does internally.

**Answer C — bucket by count.** The one that beats the log entirely.

```python
buckets: list[list[int]] = [[] for _ in range(len(numbers) + 1)]
for value, count in counts.items():
    buckets[count].append(value)
```

Bucket `i` holds every value that appeared exactly `i` times. There are `n + 1` buckets because no
value can appear more than `n` times. Now read from the right:

```python
result: list[int] = []
for count in range(len(buckets) - 1, 0, -1):
    for value in buckets[count]:
        result.append(value)
        if len(result) == k:
            return result
```

The `if len(result) == k` check has to be inside the inner loop, not after it. A single bucket can
hold more values than you need — if every value appears once and k is 3, bucket 1 holds all of them.

### The complete solution

```python
from collections import Counter
import heapq


def top_k_frequent(numbers: list[int], k: int) -> list[int]:
    """The k most frequent values, in O(n) time using bucket counting.

    Bucket i holds every value that appeared exactly i times. There are n + 1
    buckets because no value can appear more than n times, so no sort is needed.
    """
    counts = Counter(numbers)

    buckets: list[list[int]] = [[] for _ in range(len(numbers) + 1)]
    for value, count in counts.items():
        buckets[count].append(value)

    result: list[int] = []
    for count in range(len(buckets) - 1, 0, -1):
        for value in buckets[count]:
            result.append(value)
            if len(result) == k:      # must be inside: one bucket can hold many
                return result
    return result


def top_k_frequent_heap(numbers: list[int], k: int) -> list[int]:
    """The same answer in O(m log k), where m is the number of distinct values."""
    counts = Counter(numbers)
    return heapq.nlargest(k, counts, key=counts.get)


def count_manually(items: list[str]) -> dict[str, int]:
    """The three-line version, for when the interviewer says 'no imports'."""
    counts: dict[str, int] = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def is_anagram(first: str, second: str) -> bool:
    """O(n) by counting. The sorting answer is O(n log n)."""
    return Counter(first) == Counter(second)


def first_unique(text: str) -> str | None:
    """The first non-repeating character. Walk the original for the order."""
    counts = Counter(text)
    for character in text:
        if counts[character] == 1:
            return character
    return None


if __name__ == "__main__":
    print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))        # [1, 2]
    print(top_k_frequent([7], 1))                        # [7]
    print(top_k_frequent([4, 5, 6], 3))                  # [4, 5, 6] in some order
    print(top_k_frequent_heap([1, 1, 1, 2, 2, 3], 2))    # [1, 2]
    print(count_manually(["curd", "lemon", "curd"]))     # {'curd': 2, 'lemon': 1}
    print(is_anagram("listen", "silent"))                # True
    print(first_unique("swiss"))                         # 'w'
```

---

## 6. What it costs

### Building the map

The loop runs once per element: `n` iterations. Each does one hash, one lookup and one store — all
O(1) on average. So building the frequency map is **O(n) time**.

Space is **O(m) extra**, where `m` is the number of *distinct* values. That distinction matters and
interviewers push on it. Counting a million log lines that only ever contain 12 different status
codes costs 12 entries, not a million.

### What Shobha's old method cost

Four dishes, forty-one messages: `4 × 41 = 164` reads. In general `m × n`. With m = 200 distinct
words and n = 100,000 words that is `20,000,000` reads against `100,000` for the one-pass version —
**200 times more work**, and the ratio grows with the number of distinct values.

You will meet this written as `list.count()` inside a loop, which is the same mistake:

```python
for word in words:
    if words.count(word) == 1:      # this scans the whole list, every time
        return word
```

`words.count(word)` is O(n) and it is inside an O(n) loop, so that is O(n²). It looks like two lines
of clean code. It is fifty million operations at n = 10,000.

### The three top-k answers, counted

Let `n` be the number of elements and `m` the number of distinct values, so `m ≤ n`.

```
 counting        O(n)          every approach pays this
 A: sort         O(m log m)    then slice k
 B: heap         O(m log k)    keep only k in the heap
 C: buckets      O(n + m)      n+1 buckets, walk them once
```

Put numbers on it. With `n = 1,000,000`, `m = 100,000` and `k = 10`:

```
 A: 100,000 x log2(100,000) = 100,000 x 17 = 1,700,000 comparisons
 B: 100,000 x log2(10)      = 100,000 x 3.3 =  330,000 comparisons
 C: 1,000,000 + 100,000     =              1,100,000 simple steps, no comparisons
```

B does the least comparison work. C does no comparisons at all but allocates a list of a million and
one entries, which is why it is not always the winner in practice: when `n` is enormous and `m` is
tiny, C's bucket list is mostly empty and B is better. **Say that out loud.** "Bucket sort is O(n)
but it allocates n + 1 buckets, so if n is a billion and there are only 12 distinct values I would
use the heap" is a much stronger answer than reciting that one is linear.

### Space for each

```
 A: O(m)        the sorted list of distinct values
 B: O(m + k)    the counts, plus the heap
 C: O(n + m)    the bucket list is the expensive part
```

---

## 7. The traps

### Trap 1 — the missing key

```python
>>> counts = {}
>>> counts["pulao"] += 1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'pulao'
```

The three fixes, in order of how often you should use them: `counts.get(k, 0) + 1`,
`defaultdict(int)`, `Counter`. What you should not do is wrap it in a `try`/`except KeyError` — it
works, and it reads as though you did not know the alternatives.

### Trap 2 — `defaultdict` creates keys when you only meant to look

This one is genuinely surprising, and it produces wrong answers rather than errors.

```python
>>> from collections import defaultdict
>>> counts = defaultdict(int)
>>> counts["x"] += 1
>>> "zzz" in counts          # asking with `in` is safe
False
>>> counts["zzz"]            # but READING it creates it
0
>>> dict(counts)
{'x': 1, 'zzz': 0}
>>> len(counts)
2
```

Reading a missing key from a `defaultdict` **inserts** it. So `len(counts)` is now wrong, iterating
gives you a key that never appeared in the data, and a later `if counts["zzz"]` has silently changed
your dictionary. If you are going to read keys that might be absent, use `counts.get("zzz", 0)` or a
plain `dict`, and check membership with `in`, never by indexing.

### Trap 3 — `Counter` returns 0 for anything, including your typos

```python
>>> c = Counter("aabbbc")
>>> c["b"]
3
>>> c["bb"]      # typo
0
>>> c["z"]
0
```

No error, ever. This is helpful right up to the moment it hides a bug. When the count of something
that definitely exists comes back as 0, suspect the key before you suspect the logic.

### Trap 4 — walking the counter instead of the original

```python
def first_unique_wrong(text: str) -> str | None:
    counts = Counter(text)
    for character in counts:            # <- wrong: this is insertion order of
        if counts[character] == 1:      #    DISTINCT characters, not the string
            return character
    return None
```

On most inputs this returns the right answer, because a `Counter` iterates in first-seen order. It
breaks on `"aabbc"`: the distinct order is `a, b, c`, and the answer is `c` either way. Try
`"loveleetcode"` and it still works. It fails only when the first *distinct* character with count 1
is not the first *positional* character with count 1 — and since `Counter` preserves first-seen
order, that is actually never for this specific problem. **That is exactly why it is dangerous.** It
is right by accident, it stops being right the moment somebody sorts the counter or switches to a
plain dict built in a different order, and you cannot explain why it works. Walk the original.

### Trap 5 — `list.count()` inside a loop

```python
for word in words:
    if words.count(word) == 1:
        return word
```

Two clean-looking lines that are O(n²). `words.count(word)` walks the entire list every time. With
20,000 words that is 400,000,000 comparisons and takes several seconds; the `Counter` version is
0.003 seconds. Same output, same readability, different complexity — this is the counting version of
the `seen = []` trap from [day 062](../day-062-sets/README.md).

### Trap 6 — changing the dictionary while iterating it

```python
>>> d = {"a": 1, "b": 2}
>>> for key in d:
...     d[key + "!"] = 1
...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: dictionary changed size during iteration
```

Iterate over `list(d)` or `list(d.items())` if you must change the dictionary inside the loop.
Changing a *value* for an existing key is fine; adding or deleting keys is not.

### Trap 7 — `Counter` arithmetic drops what you might have wanted

```python
>>> Counter("aabbc") - Counter("abz")
Counter({'a': 1, 'b': 1, 'c': 1})
```

The `z` is gone, not `-1`. Subtraction keeps only positive counts. If you need the negatives, use
`c.subtract(other)`, which mutates in place and does keep them. And `sum(Counter(x) for x in ...)`
raises, because `sum` starts at the integer 0:

```
TypeError: unsupported operand type(s) for +: 'int' and 'Counter'
```

The fix is `sum(counters, Counter())` or, better, one `Counter` you `update()` in a loop.

---

## 8. In the interview

### How it gets asked

- *"Given an integer array and an integer k, return the k most frequent elements. Your algorithm's
  time complexity must be better than O(n log n)."* The complexity constraint is the whole question —
  it rules out sorting the counts and pushes you to the heap or the buckets.
- *"Find the first non-repeating character in a string."* Sounds easier. The trap is the second pass.
- *"Are these two strings anagrams?"* The warm-up, and the follow-up is always "what if they are
  Unicode" or "what if the strings are a gigabyte".
- The vague version: *"I have a log file with a hundred million lines. Which endpoint is slowest most
  often?"* No complexity stated, and now you have to notice that the distinct count is small and the
  total count is huge, which changes which top-k answer wins.

### What to say out loud, in the first ninety seconds

1. **Separate the two halves.** "There are two parts here: counting, and then selecting the top k.
   Counting is O(n) with a hash map and there is no way around it — I have to look at every element
   at least once. So the interesting question is the selection."
2. **Name the size that actually matters.** "Let me call n the number of elements and m the number of
   distinct values. m is at most n and is usually much smaller. The selection cost is in terms of m,
   not n."
3. **Offer all three, with their costs.** "Sorting the counts is O(m log m). A heap of size k is
   O(m log k). Bucketing by count is O(n + m) with no comparisons at all."
4. **Pick one and say why.** "I will write the bucket version because you asked for better than
   n log n, and it is the only one with no logarithm. If m were tiny and n enormous I would prefer
   the heap, because the bucket list is n + 1 long regardless."
5. **Ask the one clarifying question.** "If there are ties at the k-th position, is any valid answer
   acceptable?" It almost always is, and asking shows you noticed.

### The follow-ups

**"Why is bucket counting O(n) when sorting is O(n log n)? Have you not beaten the sorting bound?"**
"No, because I am not sorting by comparison. The bound of n log n applies to comparison sorts. Here I
know something extra — a count is an integer between 1 and n — so I can index by it directly instead
of comparing. That is the same reason counting sort is linear
([day 056](../day-056-non-comparison-sorts/README.md)). The price is the memory for the buckets."

**"What if the input does not fit in memory?"**
"Then the map does not fit either, and I would count in chunks and merge. Each machine counts its
shard and produces a partial `Counter`; then I merge the partials by adding them. Counting is
associative, which is exactly why this is the canonical MapReduce example. For approximate answers on
a stream, Count-Min Sketch gives frequencies in fixed memory with a bounded overestimate."

**"Can you do it in O(1) extra space?"**
"Not for top k in general — I have to remember the counts somewhere, and there can be n distinct
values. For the specific case of the *majority* element, yes: Boyer-Moore voting keeps one candidate
and one counter, so it is O(1) space and one pass. It only works because the majority is defined as
strictly more than half."

**"You used `Counter`. Write it without imports."**
Write the three-line `.get(k, 0) + 1` loop immediately. Have this ready — it is asked often enough
that fumbling it undoes the impression the rest of the answer made.

### A model answer

Asked: *given an array of integers and a number k, return the k most frequent elements, faster than
O(n log n).*

> "This is two problems. First count, then select.
>
> Counting has to be O(n) because I must see every element, and a hash map makes each element cost
> constant time. I will call the number of distinct values m — that is at most n, and usually far
> less.
>
> For the selection there are three options. I can sort the m counts, which is O(m log m). I can push
> them through a heap of size k, which is O(m log k) — better when k is small. Or I can bucket them:
> because a count is an integer between 1 and n, I can make n plus one buckets and drop each value
> into the bucket for its count, then read buckets from the highest down until I have k. That is
> O(n + m) and involves no comparisons at all.
>
> You have asked for better than n log n, so I will write the bucket version. The reason it beats the
> comparison bound is that I am not comparing — I know the counts are small integers, so I can index
> by them, which is the same trick as counting sort.
>
> The cost I am paying is memory: the bucket list is n plus one entries whether or not I need them.
> If I knew n was a billion and there were only twelve distinct values, I would use the heap instead,
> because allocating a billion buckets to hold twelve values would be absurd.
>
> One detail in the code: the check for whether I have collected k elements has to be inside the
> inner loop, not after it, because one bucket can hold more values than I need. If every value
> appears exactly once, bucket one holds all of them.
>
> Edge cases: k equal to the number of distinct values returns everything. Ties at the k-th position
> — I will return any valid set unless you want a specific tie-break."

---

## 9. Recall card

- **Three lines, and know all four spellings:** `counts[x] = counts.get(x, 0) + 1` · the explicit
  `if` · `defaultdict(int)` · `Counter(items)`. Building it is **O(n) time, O(m) extra space**, where
  m is the number of *distinct* values — not n.
- **`counts[x] += 1` on a missing key raises `KeyError`.** And `defaultdict` **creates the key when
  you merely read it**, so `len()` silently grows; `Counter` returns `0` for anything, so typos never
  raise. Check membership with `in`, never by indexing.
- **Top k has three answers:** sort `O(m log m)` · heap `O(m log k)` · bucket by count `O(n + m)`.
  At n = 10⁶, m = 10⁵, k = 10 that is 1.7M vs 330K vs 1.1M. **Buckets beat the n log n bound because
  they do not compare** — a count is an integer in 1..n, so you index by it.
- **Say the trade, not just the winner:** buckets allocate `n + 1` slots regardless, so with n huge
  and m tiny the heap wins. And the `len(result) == k` check goes *inside* the inner loop.
- **Two O(n²) traps that look clean:** `words.count(word)` inside a loop (400M ops at n = 20,000),
  and walking the counter instead of the original string for a "first such" question. Real errors:
  `KeyError`, `RuntimeError: dictionary changed size during iteration`, and `TypeError: unsupported
  operand type(s) for +: 'int' and 'Counter'` from `sum()`.
