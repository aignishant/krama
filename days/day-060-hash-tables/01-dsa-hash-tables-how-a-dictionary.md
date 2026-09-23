---
day: 60
track: dsa
title: "Hash tables: how a dictionary finds anything instantly"
phase: "Hashing: maps and sets"
status: written
---

# Day 060 · DSA — Hash tables: how a dictionary finds anything instantly

**After today you can:** You can explain hashing, buckets and O(1) average lookup with a drawing.

**The interviewer asks it as:** *How does a hash map work internally?*

---

## 1. What this is, and why they ask it

A **hash table** finds a value by a key without searching. Instead of looking through the data, it
takes the key, runs it through a function that turns it into a number, and uses that number as a
position — so it goes straight to where the value must be. That is what a Python `dict` is, and what
a `set` is, and it is why `"apple" in d` takes the same time whether the dictionary holds ten items
or ten million.

They ask "how does a hash map work internally" more often than any other data-structure question,
because it is the one whose *inside* everybody has used and almost nobody has looked at. A good
answer has four parts — the hash function, the bucket, the collision, and the resize — and each one
has a follow-up waiting behind it. It is also the structure that makes half the earlier phases work:
the `O(n)` Two Sum from [day 051](../day-051-why-sorting-matters/README.md), the frequency maps from
[day 021](../day-021-frequency-maps/README.md), the "subarray sum equals K" trick from
[day 038](../day-038-subarray-sum-k/README.md) — all of them were paying for a dictionary lookup and
calling it free. Today is where you find out what you were actually buying.

---

## 2. The story

The hostel at the college in Manipal has four hundred boys and one shoe rack in the porch, and
whether that rack works or not depends entirely on a rule somebody wrote on a board in 2009.

Before the rule, the rack was a heap. You came back at eleven at night, you put your shoes down
wherever there was a gap, and in the morning you looked for them. Finding your own shoes took two
minutes on a good day and much longer if somebody had shoved them behind something, and every single
morning four hundred boys did that at the same time.

The warden then was a man called Mr Shenoy, and his first attempt was reasonable and did not work.
He divided the rack into twenty-six sections, one per letter, and said: your shoes go in the section
for the first letter of your name.

It half worked. Nobody had to search the whole rack any more, which was a real improvement. But the
S section had about sixty pairs in it, because of all the Sandeeps and Sureshs and Shivas, and the Q
section had nothing in it for four years. Boys whose names began with S were still standing there
digging through sixty pairs while a boy called Zubin walked up to an empty shelf and was gone in three
seconds.

So in 2009 they changed the rule to the one still painted on the board. Take the first letter of your
name, take the last digit of your room number, and that pair tells you your slot. Two hundred and
sixty slots.

The difference was immediate and it is not really about the number of slots. It is that room numbers
spread out evenly across the hostel, so the boys got scattered across the slots instead of piling up
at the popular letters. Most slots have one or two pairs. The worst has five.

Nobody searches. You walk in, you already know your slot before you get to the rack, and you look at
one or two pairs instead of four hundred.

Two things still happen. Occasionally two boys land on the same slot — same first letter, same last
digit — and then there are two pairs there and you glance at both, which takes a second. And when the
hostel took in a new block and the numbers went up to five hundred and forty, the slots got crowded,
so over one weekend they built a second rack, repainted the rule with more slots, and every single boy
had to move his shoes to a new place. That weekend was a nuisance. It has happened twice in sixteen
years.

---

## 3. The idea in plain English

The rack is a hash table. The rule painted on the board is the **hash function**. A slot is a
**bucket**. Two boys landing in the same slot is a **collision**. And the weekend they rebuilt the
rack is a **resize**.

### The problem it solves

Finding a value in a list of `n` items means looking at them one at a time — `O(n)`, from
[day 012](../day-012-linear-search/README.md). Sorting first buys you `O(log n)` with binary search,
but only if the data stays sorted and only if the keys have an order.

A hash table does something different. It does not search at all. It **computes** where the item must
be, and goes there.

```python
d = {"apple": 3, "banana": 7}
d["apple"]        # does not look through anything. It calculates.
```

### The three parts

**One: the hash function.** A function that turns any key into an integer.

```python
hash("apple")      # 4159254339421612417   (a different number each run -- see §7)
hash(42)           # 42
hash((1, 2))       # -3550055125485641917
```

A hash function must be three things:

- **Deterministic** — the same key must give the same number every time, within one run of the
  program. Otherwise you could never find anything again.
- **Uniform** — different keys should spread out across the whole range of numbers. Mr Shenoy's first
  rule failed here: it was deterministic and fast, but it piled everyone onto S.
- **Fast** — it runs on every single lookup, so it must be cheap.

**Two: the bucket.** The hash is far too large to be a position, so you take the remainder:

```
 bucket = hash(key) % number_of_buckets
```

```python
hash("apple") % 8      # some number from 0 to 7 -- that is the slot
```

That is the whole mechanism. Key → number → remainder → position. Nothing is searched.

**Three: the collision.** Two different keys can land in the same bucket, either because they hash to
the same number or — far more often — because two different numbers have the same remainder. That is
not a bug and it is not avoidable; with more possible keys than buckets, it is guaranteed.

The standard fix is **chaining**: each bucket holds a small list of the `(key, value)` pairs that
landed there, and a lookup checks the two or three entries in that one bucket. Two pairs of shoes in
one slot.

Note what this means for correctness: **you must store the key, not just the value.** Otherwise you
cannot tell which of the two entries in the bucket is yours. That is the detail beginners miss.

### Why it is `O(1)` on average and `O(n)` in the worst case

If the hash function spreads keys evenly and there are roughly as many buckets as items, each bucket
holds about one entry, so a lookup is: compute a hash, take a remainder, check one or two entries.
That is **constant time — it does not depend on `n` at all.**

If the hash function is bad and everything lands in one bucket, a lookup checks all `n` entries, and
you have written a linked list with extra steps. That is **`O(n)`**, and it is why "what is the worst
case of a hash map" is a real interview question with a real answer.

The number that controls this is the **load factor**: the number of items divided by the number of
buckets.

```
 load factor = items / buckets

 0.25  ->  most buckets empty; lots of wasted memory
 0.66  ->  Python's dict resizes at about here
 1.0   ->  about one item per bucket on average
 5.0   ->  five per bucket; every lookup checks five things. Still O(1), but 5x slower.
```

### The resize, and why it is still `O(1)` on average

When the load factor gets too high, the table allocates a bigger array — usually double — and
**rehashes every key into it**, because `hash(key) % 8` and `hash(key) % 16` are different numbers.
That single operation is `O(n)`: the weekend the hostel rebuilt the rack.

But it happens rarely, and it happens less often as the table grows. Doubling means that inserting
`n` items causes resizes at 1, 2, 4, 8, … items, and the total copying work is
`1 + 2 + 4 + … + n ≈ 2n` — that halving-series sum again, from
[day 055](../day-055-quickselect/README.md). Spread over `n` insertions, that is a constant amount of
work each.

That is called **amortised `O(1)`**, a term you met on [day 005](../day-005-python-lists-and-tuples/README.md)
for list `append`: most operations are cheap, a rare one is expensive, and the average over a long
run is constant. It is worth saying the word and then explaining it, because saying it alone sounds
memorised.

### What Python actually does

Python's `dict` is a hash table with two Python-specific things worth knowing:

**It uses open addressing, not chaining.** On a collision, instead of keeping a list in the bucket, it
probes for another empty slot using a sequence derived from the hash. That is
[day 061](../day-061-collisions/README.md)'s subject.

**It is compact and insertion-ordered.** Since Python 3.7, iterating a dict gives you keys in the
order they were inserted, and that is a language guarantee rather than an accident. It comes from
storing entries in a dense array with a separate small index array pointing into it — which also
makes a dict about a third smaller than it used to be.

### What can be a key

A key must be **hashable**, which in practice means immutable:

```python
d[("a", 1)] = "fine"      # a tuple is hashable
d[["a", 1]] = "boom"      # a list is not
```

The reason is exactly the rack: your shoes are found by a rule computed from your name. If you could
change your name after putting the shoes down, nobody — including you — could find them again. An
object whose hash can change is unfindable in the table it is sitting in.

That is why `__hash__` must be built from fields that never change, and why defining `__eq__` without
`__hash__` makes Python set `__hash__` to `None`
([day 052](../day-052-quadratic-sorts/README.md)).

### The costs, all of them

```
 lookup   d[key]           O(1) average, O(n) worst
 insert   d[key] = v       O(1) amortised average, O(n) worst
 delete   del d[key]       O(1) average, O(n) worst
 in       key in d         O(1) average  -- checks KEYS, not values
 len      len(d)           O(1) -- stored, not counted
 iterate  for k in d       O(n), in insertion order

 value in d.values()       O(n)  <- the one that catches people
 space                     O(n), with a constant of about 2-3x the raw data
```

---

## 4. The picture

The rack, before and after the rule:

```
 NO RULE — a heap. Finding your shoes means looking at all 400.

   [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ] ...
      searching:  O(n)


 RULE 1 — first letter only. Deterministic and fast, but NOT UNIFORM.

   A: [][]                        2 pairs
   ...
   S: [][][][][][][][][][][]...  60 pairs   <- the Sandeeps, Sureshs, Shivas
   ...
   Q:                             0 pairs   <- four years empty
   Z: []                          1 pair

      lookup for an S:  60 checks.   lookup for a Z: 1 check.
      Same structure, 60x difference. That is a BAD HASH FUNCTION.


 RULE 2 — first letter AND last digit of the room number. 260 slots.

   A0:[]  A1:[][] A2:[]  ...
   S0:[][] S1:[] S2:[][] S3:[] S4:[][] ...   the 60 S's spread over 10 slots
   ...
      lookup: 1 or 2 checks, for everybody.   That is O(1).
```

**What to notice:** the number of slots is not what fixed it. Rule 1 had twenty-six slots and rule 2
has two hundred and sixty, but the real change is that the room number *spreads people out*. A hash
function that is deterministic and fast but not uniform gives you the worst case on the most common
keys.

The mechanism, drawn:

```
        key                hash function          bucket array (8 buckets)
   +-----------+          +-------------+        +---+
   |  "apple"  |  ----->  | hash()      |  --->  | 0 |  -> [ ]
   +-----------+          | 4159254339  |        +---+
                          | ...421612417|        | 1 |  -> [ ("apple", 3) ]
                          +-------------+        +---+     ^
                                 |               | 2 |  -> [ ]        the KEY is stored
                                 |               +---+                too -- or you could
                                 v               | 3 |  -> [ ("banana", 7), ("grape", 2) ]
                          % 8  = 1               +---+                     ^^^^^^^^^^^^
                                                 | 4 |  -> [ ]        a COLLISION: two keys,
                                                 +---+                one bucket. Check both.
                                                 | 5 |  -> [ ("fig", 9) ]
                                                 +---+
                                                 | 6 |  -> [ ]
                                                 +---+
                                                 | 7 |  -> [ ("kiwi", 1) ]
                                                 +---+

  d["apple"]:   hash it (fast) -> take % 8 -> go to bucket 1 -> compare the key -> return 3.
                Three steps. NOTHING was searched.
```

**What to notice:** bucket 3 holds two entries, so a lookup there compares two keys instead of one.
That is a collision, and it costs one extra comparison — not a re-search of the table. And notice the
key is stored alongside the value: without it you could not tell "banana" from "grape" once they
share a bucket.

The resize:

```
 8 buckets, 6 items -> load factor 0.75, too high

 BEFORE            AFTER doubling to 16 buckets
   bucket = h % 8      bucket = h % 16          <- the SAME key moves!

   "apple"  -> 1       "apple"  -> 9
   "banana" -> 3       "banana" -> 3
   "grape"  -> 3       "grape"  -> 11           <- the collision is resolved for free
   "fig"    -> 5       "fig"    -> 13
   "kiwi"   -> 7       "kiwi"   -> 7

 Every key must be REHASHED and moved: O(n) for that one insert.

 But doubling means it happens at 1, 2, 4, 8, 16 ... items:
   total copying over n inserts = 1 + 2 + 4 + ... + n  ~ 2n
   spread over n inserts        = ~2 per insert = O(1) AMORTISED
```

**What to notice:** `hash(key) % 8` and `hash(key) % 16` are different, so nothing can stay where it
is — the rack really does have to be rebuilt completely. And notice the halving series again: the
same `1 + 2 + 4 + … = 2n` argument that made quickselect linear.

---

## 5. The code, built step by step

### A hash table from scratch, with chaining

Building it is the fastest way to be able to explain it. Start with the buckets:

```python
class HashMap:
    def __init__(self, capacity: int = 8) -> None:
        self._capacity = capacity
        self._size = 0
        self._buckets: list[list[tuple]] = [[] for _ in range(capacity)]
```

A list of lists. Each inner list is one bucket and will hold the `(key, value)` pairs that land
there. Note `[[] for _ in range(capacity)]` and not `[[]] * capacity` — the second makes eight
references to *one* list, which is a genuinely nasty bug.

Now the one line that does all the work:

```python
    def _bucket_index(self, key) -> int:
        return hash(key) % self._capacity
```

That is the hash table. Everything else is bookkeeping.

### Lookup

```python
    def get(self, key, default=None):
        for existing_key, value in self._buckets[self._bucket_index(key)]:
            if existing_key == key:              # compare the KEY -- collisions exist
                return value
        return default
```

One bucket, then a short scan inside it. The `existing_key == key` comparison is why the key has to
be stored. And note both `hash` and `==` are used: hashing finds the bucket, equality finds the
entry. That is why **equal objects must have equal hashes** — if `a == b` but `hash(a) != hash(b)`,
they land in different buckets and the table thinks they are different keys.

### Insert, with the update case

```python
    def put(self, key, value) -> None:
        bucket = self._buckets[self._bucket_index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)          # update in place
                return
        bucket.append((key, value))
        self._size += 1
        if self._size / self._capacity > 0.75:    # the load factor
            self._resize()
```

The loop before the append is what makes `d[k] = 1; d[k] = 2` leave one entry rather than two.
Forgetting it is the commonest bug when people write this from scratch.

### The resize

```python
    def _resize(self) -> None:
        old = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for bucket in old:
            for key, value in bucket:
                self.put(key, value)              # rehash: % has a new divisor
```

Every key is re-inserted, because the bucket index depends on the capacity. This is `O(n)` and it is
the operation the amortised argument is about.

### Delete

```python
    def delete(self, key) -> None:
        bucket = self._buckets[self._bucket_index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket.pop(i)
                self._size -= 1
                return
        raise KeyError(key)
```

With chaining, deletion is genuinely simple — remove it from the list. With open addressing it is
much harder, and that is one of the trade-offs on
[day 061](../day-061-collisions/README.md).

### The complete file

```python
"""A hash table with chaining, and the dictionary patterns it makes possible."""

from collections import Counter, defaultdict


class HashMap:
    """A dict, built from scratch. Chaining for collisions, doubling on resize.

    get/put/delete: O(1) average, O(n) worst case (everything in one bucket).
    Space: O(n).
    """

    def __init__(self, capacity: int = 8) -> None:
        self._capacity = capacity
        self._size = 0
        self._buckets: list[list[tuple]] = [[] for _ in range(capacity)]

    def _bucket_index(self, key) -> int:
        return hash(key) % self._capacity        # THE line. Key -> number -> position.

    def put(self, key, value) -> None:
        bucket = self._buckets[self._bucket_index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size / self._capacity > 0.75:
            self._resize()

    def get(self, key, default=None):
        for existing_key, value in self._buckets[self._bucket_index(key)]:
            if existing_key == key:
                return value
        return default

    def delete(self, key) -> None:
        bucket = self._buckets[self._bucket_index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket.pop(i)
                self._size -= 1
                return
        raise KeyError(key)

    def _resize(self) -> None:
        old = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for bucket in old:
            for key, value in bucket:
                self.put(key, value)

    def __contains__(self, key) -> bool:
        return any(k == key for k, _ in self._buckets[self._bucket_index(key)])

    def __len__(self) -> int:
        return self._size

    def load_factor(self) -> float:
        return self._size / self._capacity

    def bucket_sizes(self) -> list[int]:
        """For seeing the distribution -- a good hash gives mostly 0s, 1s and 2s."""
        return [len(b) for b in self._buckets]


def two_sum(nums: list[int], target: int) -> list[int]:
    """The reason hash maps matter. O(n) instead of O(n^2), and it keeps the indices."""
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []


def first_non_repeating(text: str) -> str | None:
    """Two passes, both O(n). Dict insertion order gives 'first' for free (3.7+)."""
    counts = Counter(text)
    for ch in text:
        if counts[ch] == 1:
            return ch
    return None


def group_anagrams(words: list[str]) -> list[list[str]]:
    """A hash map keyed on a computed signature. The key does not have to be the data."""
    groups: dict[tuple, list[str]] = defaultdict(list)
    for word in words:
        signature = tuple(sorted(word))          # a tuple is hashable; a list is not
        groups[signature].append(word)
    return list(groups.values())


if __name__ == "__main__":
    m = HashMap()
    for i, fruit in enumerate(["apple", "banana", "grape", "fig", "kiwi"]):
        m.put(fruit, i)
    print(len(m), m.get("grape"), m.get("mango", -1))     # 5 2 -1
    print("apple" in m, "mango" in m)                     # True False

    m.put("apple", 99)                                    # update, not insert
    print(len(m), m.get("apple"))                         # 5 99

    m.delete("apple")
    print(len(m), m.get("apple", "gone"))                 # 4 gone

    # watch the resize happen
    big = HashMap(capacity=4)
    for i in range(20):
        big.put(f"key{i}", i)
        print(f"{len(big):3} items, {big._capacity:3} buckets, "
              f"load {big.load_factor():.2f}")
    # 1 items, 4 buckets ... resizes at 4, 8, 16, 32 buckets

    print(sorted(big.bucket_sizes(), reverse=True)[:5])   # mostly 1s and 2s

    # a BAD hash function, to see the failure
    class BadKey:
        def __init__(self, name: str) -> None:
            self.name = name
        def __hash__(self) -> int:
            return 1                                      # everything in one bucket
        def __eq__(self, other) -> bool:
            return isinstance(other, BadKey) and self.name == other.name

    bad = HashMap()
    for i in range(200):
        bad.put(BadKey(f"n{i}"), i)
    print(max(bad.bucket_sizes()))                        # 200 -- one bucket has everything
    # every lookup is now O(n). Same structure, same code, 200x slower.

    print(two_sum([2, 7, 11, 15], 9))                     # [0, 1]
    print(first_non_repeating("swiss"))                   # w
    print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

---

## 6. What it costs

### The lookup, counted

```
 d[key], with a good hash and load factor around 0.66:

   1. hash(key)                    ~constant (for a short string, ~20 ns in C)
   2. % capacity                   1 operation
   3. index into the array         1 operation
   4. compare keys in the bucket   ~1.3 comparisons on average at load 0.66
                                   -------
                                   about 4 operations, INDEPENDENT of n
```

Independent of `n` is the whole point. At ten items and at ten million items, the same four steps.

### Against the alternatives

```
 finding one value among n = 1,000,000

   list, linear scan          500,000 comparisons on average       O(n)
   sorted list, bisect             20 comparisons                  O(log n)
   dict                             1 hash + ~1.3 comparisons      O(1)

 and for 1,000 lookups:
   list      500,000,000 comparisons
   bisect         20,000
   dict            2,300
```

The gap against the sorted list is smaller than people expect — twenty against one is not the
headline. The headline is that the dict needs no sort, no order on the keys, and no maintenance when
you insert.

### The load factor, priced

```
 average comparisons per lookup, with chaining:

   load 0.25   ->  ~1.1
   load 0.5    ->  ~1.25
   load 0.75   ->  ~1.4      <- typical resize threshold
   load 1.0    ->  ~1.5
   load 2.0    ->  ~2.0
   load 10.0   ->  ~6.0      -- still "O(1)", and six times slower

 memory, for n = 1,000,000 entries:
   load 0.25   ->  4,000,000 buckets   -- 4x the buckets you need
   load 0.75   ->  1,333,333 buckets
```

Load factor is the time-against-memory dial, and 0.66 to 0.75 is where almost every implementation
sets it.

### The resize, and the amortised argument

```
 inserting n items into a table that doubles from 8:

   resize at 8 items    : copy 8
   resize at 16         : copy 16
   resize at 32         : copy 32
   ...
   resize at n/2        : copy n/2
                          --------
   total copying        = 8 + 16 + ... + n/2 ~ n

 total work for n inserts = n (the inserts) + n (the copying) = 2n
 per insert               = 2 operations = O(1) AMORTISED

 BUT: one individual insert can take O(n).
      At a million items, one unlucky insert copies a million entries.
      That is a latency spike, and it matters in a real-time path.
```

Say both halves. "Amortised O(1)" is the average; the tail latency is real, and it is why some
systems pre-size their maps or use incremental rehashing — Redis rehashes a few buckets per operation
rather than all at once, precisely to avoid the spike.

### Memory

```
 a Python dict with 1,000,000 short string keys and integer values:

   the raw data (keys + values)          ~ 60 MB
   the dict structure                    ~ 80 MB
                                         --------
   total                                 ~ 140 MB, about 2.3x the data

 a list of the same 1,000,000 values     ~ 40 MB

 The dict costs roughly 3x a list. That is the price of O(1) lookup.
```

### The worst case, made concrete

```
 200 keys, all hashing to the same bucket:

   lookup : 200 comparisons instead of ~1.3
   insert : 200 comparisons
   n keys : O(n) per operation, O(n^2) to build the table

 With n = 100,000 that is 5,000,000,000 comparisons to fill a dict
 that should have taken 100,000.
```

That is not theoretical. Before 2012 it was a real denial-of-service technique: send a web form with
thousands of parameter names crafted to collide, and the server's parameter dictionary turns
quadratic. The fix is in §7.

---

## 7. The traps

### The real error: an unhashable key

```python
d = {}
d[["a", "b"]] = 1
```

```
Traceback (most recent call last):
  File "day60.py", line 2, in <module>
    d[["a", "b"]] = 1
    ~^^^^^^^^^^^^
TypeError: unhashable type: 'list'
```

A list can change, so its hash could change, so it could never be found again. Use a tuple. The same
error appears with sets, dicts and any object defining `__eq__` without `__hash__`:

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

{Point(1, 2): "here"}
```

```
TypeError: unhashable type: 'Point'
```

`@dataclass` generates `__eq__`, so Python sets `__hash__` to `None` deliberately. Fix it with
`@dataclass(frozen=True)`.

### The trap that produces no error: mutating a key after insertion

```python
class Tag:
    def __init__(self, name): self.name = name
    def __hash__(self): return hash(self.name)      # hashes on a MUTABLE field
    def __eq__(self, other): return self.name == other.name

t = Tag("draft")
d = {t: "my document"}
print(t in d)          # True

t.name = "published"   # the hash has now changed
print(t in d)          # ???
```

```
True
False
```

The object is sitting in the dictionary and cannot be found — including by itself. It hashes to a
different bucket now, so the lookup goes to the wrong slot and finds nothing. Nothing raises, and the
entry is unreachable and un-deletable except by iterating.

**Hash on fields that never change.** This is the rack rule: if you can change your name after
leaving your shoes, nobody can find them.

### The real error: changing a dict while iterating it

```python
d = {"a": 1, "b": 2, "c": 3}
for key in d:
    if d[key] == 2:
        del d[key]
```

```
Traceback (most recent call last):
  File "day60.py", line 2, in <module>
    for key in d:
RuntimeError: dictionary changed size during iteration
```

The iterator holds a position into the internal array; a delete or an insert can move entries or
trigger a resize, so the position becomes meaningless. Python detects it and raises rather than
giving you nonsense. The fix is to iterate a copy of the keys — `for key in list(d)` — or to build a
new dict.

### The trap: `in` checks keys, not values

```python
d = {"apple": 3}
print("apple" in d)        # True   -- O(1)
print(3 in d)              # False  -- 3 is a VALUE, not a key
print(3 in d.values())     # True   -- and this is O(n)!
```

`d.values()` has no hash structure behind it, so searching it is a linear scan. If you need to look
up by value, you need a second dictionary keyed the other way — and then you have to keep both in
step.

### The trap: assuming `O(1)` always

```python
class Everything:
    def __hash__(self): return 0
    def __eq__(self, other): return isinstance(other, Everything)
```

Every instance lands in one bucket. Insert `n` of them and the dictionary is a list: each insert
compares against everything already there, so building it is `O(n²)`. This is the shape of the
hash-collision denial-of-service attack, and the defence in Python is **hash randomisation**:

```bash
python -c "print(hash('apple'))"
python -c "print(hash('apple'))"
```

```
-8395723518259234171
5731011213473296981
```

Different on every run. Python seeds string hashing with a random value at start-up (since 3.3, on by
default), so an attacker cannot precompute colliding keys. Two consequences to remember: **never
persist a Python hash value to disk or across processes**, and **never rely on dict iteration order
matching hash order** — the insertion-order guarantee is a separate mechanism and it does hold.

### The trap: `KeyError` in production

```python
counts = {}
counts["apple"] += 1
```

```
Traceback (most recent call last):
  File "day60.py", line 2, in <module>
    counts["apple"] += 1
    ~~~~~~^^^^^^^^^
KeyError: 'apple'
```

Three idiomatic fixes, and knowing which to use matters:

```python
counts[key] = counts.get(key, 0) + 1        # explicit, works for any dict
counts = defaultdict(int); counts[key] += 1  # cleaner, but ANY read creates the key
counts = Counter(items)                      # best when you are counting
```

The `defaultdict` caveat is worth knowing: reading a missing key inserts it, so
`if d[k] == 0` silently grows the dictionary.

### The trap: equal objects with unequal hashes

```python
class Bad:
    def __init__(self, v): self.v = v
    def __eq__(self, other): return self.v == other.v
    def __hash__(self): return id(self)          # different for every instance

d = {Bad(1): "x"}
print(Bad(1) in d)
```

```
False
```

The two objects are equal, and the dictionary cannot find one from the other, because they hash to
different buckets so the equality check never happens. **The contract is one-directional and
absolute: if `a == b`, then `hash(a)` must equal `hash(b)`.** The reverse is allowed — unequal
objects may share a hash, which is just a collision.

---

## 8. In the interview

### How it gets asked

- *"How does a hash map work internally?"* — the direct form, and the answer has four parts: hash
  function, bucket, collision, resize.
- *"Why is lookup O(1)? Is it always?"* — the follow-up that separates people. Average yes, worst
  case no, and be able to say when.
- *"Implement a hash map."* — LeetCode 706. Chaining is the version to write.
- *"What can be a key, and why?"* — hashable, meaning effectively immutable, and the reason is the
  find-it-again argument.
- *"What happens when it gets full?"* — resize, rehash, and the amortised argument with the doubling
  sum.
- *"Dict or a sorted list?"* — the comparison question. Order, range queries and memory decide it.

### What to say out loud, in the first ninety seconds

1. **Give the one-sentence mechanism first.** *"It doesn't search — it computes. You run the key
   through a hash function to get an integer, take that modulo the number of buckets, and that is the
   position."*
2. **Name the three requirements on the hash.** *"Deterministic, so you can find it again. Uniform,
   so keys spread across buckets. Fast, because it runs on every operation."*
3. **Bring up collisions before being asked.** *"Two keys can land in the same bucket — that's
   guaranteed, since there are more possible keys than buckets. With chaining, each bucket holds a
   short list, and a lookup checks the two or three entries there. Which is why the key has to be
   stored, not just the value."*
4. **Give the complexity with both cases.** *"O(1) average, because with a good hash each bucket
   holds about one entry. O(n) worst case, if everything lands in one bucket — then it's a linked
   list with extra steps."*
5. **Volunteer the resize.** *"When the load factor passes about 0.66, it doubles the table and
   rehashes everything, because `hash % 8` and `hash % 16` differ. That one insert is O(n), but
   doubling means the total copying over n inserts is about 2n, so it's amortised O(1) — with a real
   latency spike on the unlucky insert."*

### The follow-ups

**"Why is it O(1)? Is it always?"**
It is O(1) *on average*, and no, not always, and the distinction is the whole question. The average
case rests on two assumptions. The first is that the hash function distributes keys roughly uniformly
across buckets — that is the part a hash function has to earn, and a deterministic, fast hash that
piles everything onto a few buckets is a real failure mode. The second is that the number of buckets
grows with the number of items, which the resize does; if the table never grew, the load factor would
rise with `n` and every lookup would get slower. Given both, each bucket holds about one entry, so a
lookup is hash, modulo, index, and about one and a third key comparisons — four operations that do
not depend on `n` at all. The worst case is that every key lands in the same bucket, and then a
lookup compares against all `n` entries, so operations are O(n) and building the table is O(n²).
That is not hypothetical: before 2012 it was a real denial-of-service technique, where an attacker
sent a web form with thousands of crafted parameter names that all collided, and the server's
parameter dictionary went quadratic. The defence is hash randomisation — Python seeds string hashing
with a random value per process, so `hash('apple')` genuinely differs between runs, which means you
must never persist a hash value or rely on it across processes.

**"What happens when the table gets full?"**
It resizes, and the interesting part is why that is still cheap on average. When the load factor —
items divided by buckets — passes a threshold, typically around two-thirds, the table allocates a new
array of double the size and reinserts every existing key into it. Reinserting is not optional and it
is not a copy: the bucket index is `hash(key) % capacity`, so changing the capacity changes where
every key belongs. That single insert is therefore O(n). What makes it acceptable is the doubling.
Resizes happen at 8, 16, 32, 64 items and so on, so over `n` insertions the total copying is
`8 + 16 + ... + n/2`, which sums to about `n` — the same halving-series argument as elsewhere. Total
work for `n` inserts is about `2n`, so each insert costs a constant on average, which is what
amortised O(1) means. I would add the caveat, because it matters in practice: the average is fine and
the tail is not. At a million items, one unlucky insert copies a million entries, and if that lands
in a request path it is a visible latency spike. Systems that care about that either pre-size the map
when they know the count, or rehash incrementally — Redis moves a few buckets per operation instead
of doing it all at once.

**"What can be a key, and why?"**
Anything hashable, which in practice means effectively immutable — numbers, strings, tuples of
hashable things, frozensets, and your own objects if you define `__hash__`. Lists, dicts and sets
cannot be keys. The reason is the find-it-again argument: the table stores an entry at a position
computed from the key's hash, so if the hash can change after insertion, the entry becomes
unreachable. The demonstration is unpleasant — take an object that hashes on a mutable field, put it
in a dict, then change that field, and `obj in d` returns `False` for an object that is physically
sitting in the dictionary. It cannot be found and it cannot be deleted by key, and nothing raises.
So the rule is that `__hash__` must be computed from fields that never change — the identity of an
entity, not its status. That is also why Python sets `__hash__` to `None` when you define `__eq__`
without it: it refuses to guess. And there is a second half to the contract that is absolute: if two
objects are equal, they must have the same hash. If they do not, the table looks in different buckets
and never even runs the equality check, so an object equal to your key will not find it. The reverse
is fine — unequal objects sharing a hash is just a collision, which the table already handles.

### A model answer

> "The key idea is that it doesn't search at all — it computes where the value must be. You take the
> key, run it through a hash function that turns it into an integer, take that integer modulo the
> number of buckets, and that's the position in an array. One calculation, then a direct index. That's
> why it doesn't matter whether the map holds ten items or ten million.
>
> The hash function has to be three things. Deterministic, or you'd never find anything again. Fast,
> because it runs on every operation. And uniform — spreading keys evenly across buckets — and that
> last one is what people underestimate. A hash that's deterministic and fast but piles everything
> onto a few buckets gives you the worst case on your most common keys.
>
> Collisions are guaranteed, because there are more possible keys than buckets — even a perfect hash
> function has to share a remainder. The standard fix is chaining: each bucket holds a short list of
> `(key, value)` pairs, and a lookup checks the two or three entries in that one bucket. That's why
> the key is stored alongside the value — with two entries in a bucket you need the key to tell them
> apart. Python actually uses open addressing rather than chaining, probing for another slot instead
> of keeping a list, but the idea is the same.
>
> Complexity is O(1) average and O(n) worst case. Average, because with a good hash and a load factor
> around two-thirds each bucket holds about one entry, so a lookup is a hash, a modulo, an index, and
> about one comparison — four operations regardless of n. Worst case, if everything lands in one
> bucket, a lookup compares against all n entries and you've written a linked list with extra steps.
>
> When the load factor passes the threshold it resizes: allocate double the buckets and reinsert every
> key, because `hash % 8` and `hash % 16` are different positions. That insert is O(n), but doubling
> means resizes happen at 8, 16, 32 items, so the total copying over n inserts is about n and each
> insert costs a constant on average — amortised O(1). I'd flag the caveat, though: the average is
> fine and the tail isn't. One unlucky insert at a million items copies a million entries, and Redis
> for example rehashes incrementally specifically to avoid that spike.
>
> One last thing: keys must be hashable, which effectively means immutable, because if the hash can
> change after insertion the entry becomes unfindable — including by the object itself."

---

## 9. Recall card

- **It does not search, it computes:** `bucket = hash(key) % capacity`, then a direct index. That one
  line is the whole structure. A hash function must be **deterministic** (find it again), **uniform**
  (spread the keys), and **fast** (it runs on every operation) — and Mr Shenoy's first-letter rule
  failed only on uniformity.
- **Collisions are guaranteed** (more keys than buckets). **Chaining** = each bucket holds a short
  list, so a lookup checks 1-2 entries — which is why the **key is stored alongside the value**.
  Python uses **open addressing** instead ([day 061](../day-061-collisions/README.md)).
- **O(1) average, O(n) worst case.** Average = 4 operations independent of n, resting on a uniform
  hash *and* the table growing. Worst = everything in one bucket: n comparisons per operation, O(n²)
  to build — the real hash-DoS attack, defended by Python's per-process **hash randomisation** (so
  never persist a hash).
- **Resize when the load factor passes ~0.66:** double the buckets and **rehash everything**, because
  `% 8` and `% 16` differ. That insert is O(n), but 8+16+32+…+n/2 ≈ n, so it is **amortised O(1)** —
  with a real tail-latency spike on the unlucky insert.
- **Keys must be hashable = effectively immutable.** Hash on fields that **never change**, or the
  entry becomes unfindable while sitting in the table (`obj in d` → `False`, no error). And the
  absolute contract: **`a == b` implies `hash(a) == hash(b)`.** `@dataclass` without `frozen=True`
  sets `__hash__` to `None`; `d.values()` search is **O(n)**; deleting while iterating raises
  `RuntimeError: dictionary changed size during iteration`.
