---
day: 61
track: dsa
title: "Collisions, and why a hash map can turn slow"
phase: "Hashing: maps and sets"
status: written
---

# Day 061 · DSA — Collisions, and why a hash map can turn slow

**After today you can:** You can describe chaining and open addressing, and the worst case of each.

**The interviewer asks it as:** *What is the worst-case complexity of a hash map lookup? When does it happen?*

---

## 1. What this is, and why they ask it

A **collision** is two different keys landing in the same bucket. It is not a bug and it is not
avoidable — there are always more possible keys than buckets, so some of them must share. Yesterday
you met the idea; today is about the two strategies for handling it, **chaining** and **open
addressing**, and about what happens to a hash map when collisions stop being occasional.

They ask it because the honest answer to "what is a hash map's complexity" is `O(1)` average and
`O(n)` worst, and everybody can say the first half. The interview is in the second: when does the
worst case actually happen, what does it look like, and what do real implementations do about it. The
answers are specific and interesting — Python probes rather than chains, Java converts a long chain
into a tree, deletion under open addressing needs a marker that is not "empty", and there was a real
denial-of-service class of attack built on exactly this that changed how every major language hashes
strings. This is also the day the `O(1)` you have been assuming since
[day 021](../day-021-frequency-maps/README.md) gets its conditions stated.

---

## 2. The story

Vinod has been the watchman at a complex of a hundred and twenty flats in Kondapur for nine years,
and the thing he actually spends his evenings on is cars.

There are eighty-four bays and a hundred and twenty flats, so it was never going to be one each. The
rule the association came up with is on a board by the gate: your bay is the last two digits of your
flat number, and if somebody is already in it, you take the next free one along, and keep going.
Simple enough that nobody has to be told twice.

For the first few years it worked well. Most people found their own bay empty and parked and went up.

What went wrong went wrong slowly.

Around bay forty, several flats' numbers happened to land close together, and once forty, forty-one
and forty-two were taken, a man arriving for forty-one took forty-three, which meant the man for
forty-three took forty-four, and so on. The run grew. By last year the stretch from forty to
fifty-two was solid every evening, and a man who should have parked at forty-one was walking to
fifty-three. Nobody planned that. Each individual person had followed the rule exactly.

Then came the part Vinod actually had to solve.

When somebody's car has to be moved — a lorry needs to get in, or two cars are blocking each other —
he has to find the owner. So he walks from their bay along the row, and if he reaches an empty bay he
stops, because under the rule an empty bay means nobody went past it.

In 2021 the family in flat forty-one sold their car. Bay forty-one stood empty. And a man from flat
thirty-eight, who years earlier had walked past a full forty-one and parked at forty-seven, became
completely unfindable — Vinod would start at thirty-eight, walk three bays, reach the empty
forty-one, conclude nobody had gone past, and stop. The car was there. The rule said it could not be.

The fix was a plastic cone. When a bay empties permanently, a cone goes in it, and a cone means:
somebody used to be here, keep walking. Not empty. Vacated.

That worked, and then the cones became their own problem. After two years there were eleven of them,
and walking from bay thirty-eight past eleven cones to find a car took as long as when the row had
been full — because a cone slows you down exactly as much as a parked car does, and unlike a parked
car it is not holding anybody.

So one Sunday in 2023 they cleared the whole car park, took every cone away, and started again from
an empty row.

---

## 3. The idea in plain English

Vinod's car park is **open addressing** with **linear probing**. The solid run from forty to
fifty-two is **clustering**. The unfindable car is why deletion is hard. The cone is a **tombstone**.
And the Sunday they cleared everything is a **rehash**.

### Why collisions are guaranteed

Two separate reasons, and both are worth being able to say.

**One: there are more keys than buckets.** A dictionary with eight buckets can hold any of infinitely
many strings, so keys must share buckets. Even a perfect hash function must map some pair to the same
remainder.

**Two: collisions arrive far sooner than people expect.** With `b` buckets and `n` keys, the chance
that no two collide falls very fast. This is the shape of the birthday problem: in a room of
twenty-three people, there is about a fifty percent chance two share a birthday, even though there
are three hundred and sixty-five days.

```
 buckets = 365, keys = 23   ->  ~50% chance of at least one collision
 buckets = 1,000, keys = 38 ->  ~50%
 buckets = 1,000,000, keys = 1,178 -> ~50%
```

A million buckets and only about twelve hundred keys, and it is a coin flip. **Collision handling is
not an edge case; it is the normal operating condition.**

### Strategy one: chaining

Each bucket holds a small collection — a list — of the entries that landed there. A lookup finds the
bucket and scans that short list.

```
 bucket 3 -> [ ("banana", 7) , ("grape", 2) , ("melon", 4) ]
```

- **Lookup cost:** one bucket, then `1 + load factor` comparisons on average.
- **Deletion:** easy. Remove it from the list. Nothing else is affected.
- **Load factor above 1 is fine.** With sixteen buckets and forty keys, each chain is about two and a
  half long, and it still works.
- **The cost:** every entry needs a pointer, so memory is higher, and following pointers is bad for
  the processor's memory cache — the entries in a chain are scattered rather than adjacent.
- **The worst case:** every key in one bucket, so the map is a list and every operation is `O(n)`.

**Java's improvement, which gets asked about:** since Java 8, when a chain in `HashMap` reaches eight
entries and the table is large enough, that chain is converted into a balanced tree, so the worst
case for that bucket becomes `O(log n)` rather than `O(n)`. It is a real, shippable answer to the
attack priced in §6, and a good thing to know.

### Strategy two: open addressing

There are no lists. Every entry lives directly in the array, and when a bucket is taken you **probe**
— look at another slot by a rule — until you find a free one. Vinod's rule.

**Linear probing:** try `h`, then `h+1`, `h+2`, `h+3`, wrapping round.

```
 insert "grape", hash % 8 = 3
   slot 3 taken by "banana" -> try 4
   slot 4 free -> put it there

 lookup "grape"
   slot 3: "banana"? no, keep going
   slot 4: "grape"? yes.

 lookup "melon", hash % 8 = 3
   slot 3: "banana"? no
   slot 4: "grape"?  no
   slot 5: EMPTY     -> stop. "melon" is not in the map.
```

That last line is the rule that makes lookups terminate: **an empty slot means the search is over.**
Nothing could have been placed past it, because insertion would have stopped there too.

- **Lookup cost:** rises sharply with the load factor, because of clustering.
- **Memory:** better than chaining. No pointers, and the entries are adjacent in memory, so the
  processor's cache works for you — which is why it is usually faster in practice at sensible load
  factors.
- **Load factor must stay below 1**, obviously, and in practice below about 0.7.
- **Deletion is hard**, and that is the interesting part.

### Clustering: why linear probing degrades

Once a run of consecutive slots is full, it grows faster than it should. Any key that hashes anywhere
inside the run has to walk to the end of it and lands just past it — which makes the run one longer,
which makes it catch more keys. This is **primary clustering**, and it is Vinod's stretch from forty
to fifty-two.

```
 load factor    average probes for a successful lookup (linear probing)
   0.25          1.2
   0.50          1.5
   0.75          2.5
   0.90          5.5
   0.95         10.5
   0.99         50.5
```

Look at the shape. From 0.5 to 0.75 it merely doubles; from 0.9 to 0.99 it multiplies by nine. **A
hash map does not slow down gradually; it falls off a cliff**, and the cliff is why implementations
resize at around 0.66 rather than waiting until the table is nearly full.

The fixes for clustering:

- **Quadratic probing:** try `h+1`, `h+4`, `h+9`, `h+16`. The jumps spread keys out so runs do not
  merge. It removes primary clustering but keys with the *same* initial hash still follow the same
  path — **secondary clustering**.
- **Double hashing:** the step size itself comes from a second hash of the key, so two keys that
  start in the same slot walk away in different directions. This is the best of the three, and it is
  what Python does, in its own form.

### Deletion under open addressing, and the tombstone

You cannot simply empty a slot. Vinod's unfindable car is the exact failure:

```
 "banana" at 3, "grape" probed past it to 4.

 delete "banana" and blank slot 3:

   lookup "grape": hash % 8 = 3
     slot 3: EMPTY -> stop. "grape" not found.

 The entry is sitting at slot 4 and is now unreachable.
```

The fix is a third state. A slot is **empty**, **occupied**, or **deleted** — a marker meaning
"something was here; keep probing". That marker is a **tombstone**, and it is the cone.

```
 lookup : a tombstone means KEEP GOING (it is not the end of the probe)
 insert : a tombstone may be REUSED (it is a free slot)
```

And then the cones accumulate. A tombstone costs a lookup exactly as much as a real entry and holds
nothing, so a table with heavy insert-and-delete traffic slowly fills with markers and lookups get
slower while the map appears to be shrinking. The fix is to count tombstones and **rehash when there
are too many** — the Sunday they cleared the car park.

That is a genuinely good detail to volunteer: *"a hash map with a lot of deletions has to rehash even
though it is not growing."*

### What Python actually does

`dict` and `set` use **open addressing** with a probe sequence that is neither linear nor purely
quadratic:

```
 perturb = hash(key)
 slot    = hash(key) % capacity
 repeat: slot = (5 * slot + 1 + perturb) % capacity
         perturb >>= 5
```

The `perturb` value carries the *high* bits of the hash, which the initial `% capacity` threw away —
so two keys whose hashes agree in the low bits still separate quickly. That is double hashing in
spirit, and it is why Python's dict behaves well without needing chains.

Python also uses tombstones — a `DKIX_DUMMY` marker — and rehashes on resize, which cleans them up.

### The worst case, stated properly

```
 all n keys hash to the same bucket:

   chaining        : one chain of n. Lookup O(n). Building the map O(n^2).
   open addressing : one long probe run. Same.
   Java 8+         : the chain becomes a tree. Lookup O(log n). Building O(n log n).
```

Three ways this happens in real life:

1. **A bad hash function** — one written by hand that uses too little of the key, such as only the
   first character or only the length.
2. **A pathological key set** — integer keys whose values are all multiples of the capacity, so
   `key % capacity` is always the same. Sequential integer keys are usually *good*, but keys stepping
   by exactly the table size are the worst possible input.
3. **An adversary choosing the keys.** This is the real one, and it is §7.

---

## 4. The picture

Linear probing, and how a cluster forms:

```
 capacity 8. Rule: try h, then h+1, h+2 ... wrapping.

 slot     0     1     2     3     4     5     6     7
        +-----+-----+-----+-----+-----+-----+-----+-----+
 start  |     |     |     |     |     |     |     |     |
        +-----+-----+-----+-----+-----+-----+-----+-----+

 insert "banana" (h=3)
        |     |     |     | ban |     |     |     |     |     1 probe

 insert "grape"  (h=3)  -> 3 taken, try 4
        |     |     |     | ban | gra |     |     |     |     2 probes

 insert "melon"  (h=4)  -> 4 taken, try 5
        |     |     |     | ban | gra | mel |     |     |     2 probes

 insert "fig"    (h=3)  -> 3,4,5 taken, try 6
        |     |     |     | ban | gra | mel | fig |     |     4 probes
                            \_______________________/
                              a CLUSTER of 4.

  Any new key hashing to 3, 4, 5 or 6 must walk to the END of the run
  and lands at 7 -- making the run LONGER, so it catches MORE keys.
  That is primary clustering, and it feeds itself.
```

**What to notice:** the probe count went 1, 2, 2, 4. Nothing was done wrong; the rule was followed
exactly each time. Clusters are an emergent property of linear probing, not a mistake.

Why deletion needs a tombstone:

```
 state:   slot 3 = "banana"(h=3),  slot 4 = "grape"(h=3, probed past 3)

 WRONG -- blank the slot:
        +-----+-----+-----+-----+-----+
        |     |     |     |     | gra |
        +-----+-----+-----+-----+-----+
        lookup "grape": h=3 -> slot 3 is EMPTY -> "not found"
        The entry is at slot 4 and is UNREACHABLE. No error. Ever.

 RIGHT -- leave a tombstone:
        +-----+-----+-----+-----+-----+
        |     |     |     |  X  | gra |          X = "was here, keep going"
        +-----+-----+-----+-----+-----+
        lookup "grape": h=3 -> slot 3 is a tombstone -> keep probing
                             -> slot 4 = "grape". Found.
        insert "kiwi" (h=3): a tombstone is a free slot -> reuse it.

 AND THEN: tombstones cost a probe each and hold nothing.
        +-----+-----+-----+-----+-----+-----+-----+-----+
        |  X  |  X  |  X  | ban |  X  |  X  | gra |  X  |
        +-----+-----+-----+-----+-----+-----+-----+-----+
        2 real entries, 6 cones. Lookups are as slow as a full table.
        -> REHASH, even though the map is nearly empty.
```

**What to notice:** the last box. A hash map that is shrinking can need a rehash, which is the
opposite of what everybody assumes. Deletions do not make it faster.

The cliff:

```
  average probes per lookup (linear probing, successful)

   50 |                                                    *
      |
   40 |
      |
   30 |
      |
   20 |
      |                                              *
   10 |                                        *
      |                          *      *
    0 +---*-----*-----*-----*---------------------------------
        .25   .50   .60   .75    .85   .90   .95   .99
                                  load factor
                    |
              resize HERE (~0.66), long before the cliff
```

**What to notice:** it is flat and then it is vertical. There is no useful warning region, which is
why every implementation resizes at a fixed load factor rather than reacting to slowness.

Chaining against open addressing:

```
                        CHAINING                 OPEN ADDRESSING
  collision handling    a list in the bucket      probe for another slot
  load factor           can exceed 1              must stay < 1; resize at ~0.66
  memory                +1 pointer per entry      no pointers, denser
  cache behaviour       poor (scattered)          good (adjacent slots)
  deletion              trivial: remove it        needs TOMBSTONES
  worst case            O(n)  (O(log n) in Java 8+ via treeification)
  used by               Java HashMap, most        Python dict/set, Go maps,
                        textbooks                 C++ open-addressing tables
```

**What to notice:** the deletion row and the cache row are the trade. Open addressing is faster in
practice because of memory locality, and it pays for that with tombstones.

---

## 5. The code, built step by step

### Making a collision happen on purpose

You cannot reason about collisions until you have caused one:

```python
class Colliding:
    """Every instance hashes to the same bucket. Equality still distinguishes them."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __hash__(self) -> int:
        return 42                                  # the same for every instance

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Colliding) and self.name == other.name

    def __repr__(self) -> str:
        return f"Colliding({self.name!r})"
```

```python
d = {Colliding(f"k{i}"): i for i in range(5)}
print(len(d))                    # 5 -- all five are present and distinct
print(d[Colliding("k3")])        # 3 -- and findable
```

Five entries, one bucket, and the dictionary is still **correct**. That is the first thing to say
about collisions: they cost time, never correctness — as long as `__eq__` distinguishes the keys.

### Open addressing with linear probing

Build the table with three states, because that is the whole lesson:

```python
_EMPTY = object()       # never used
_TOMBSTONE = object()   # was used, then deleted -- KEEP PROBING
```

```python
class OpenAddressed:
    def __init__(self, capacity: int = 8) -> None:
        self._capacity = capacity
        self._keys: list = [_EMPTY] * capacity
        self._values: list = [None] * capacity
        self._size = 0           # real entries
        self._used = 0           # real entries + tombstones
```

Two counters, and the difference between them is the whole tombstone problem. `_size` is what `len()`
reports; `_used` is what decides when to resize.

The probe, which is the heart of it:

```python
    def _probe(self, key) -> tuple[int, bool]:
        """Return (slot, found). Walks until the key, or the first EMPTY slot."""
        slot = hash(key) % self._capacity
        first_tombstone = -1
        for _ in range(self._capacity):
            entry = self._keys[slot]
            if entry is _EMPTY:
                return (first_tombstone if first_tombstone >= 0 else slot), False
            if entry is _TOMBSTONE:
                if first_tombstone < 0:
                    first_tombstone = slot        # remember it: insert can reuse it
            elif entry == key:
                return slot, True
            slot = (slot + 1) % self._capacity    # linear probing, wrapping
        return (first_tombstone if first_tombstone >= 0 else -1), False
```

Three things to say about this while writing it. `_EMPTY` ends the search — nothing could have been
placed beyond it. `_TOMBSTONE` does **not** end the search, but it is remembered so an insert can
reuse the first one it passed. And `(slot + 1) % capacity` wraps, so the probe never runs off the
end.

Insert:

```python
    def put(self, key, value) -> None:
        slot, found = self._probe(key)
        if found:
            self._values[slot] = value            # update in place
            return
        if self._keys[slot] is _EMPTY:
            self._used += 1                       # a fresh slot consumed
        self._keys[slot] = key
        self._values[slot] = value
        self._size += 1
        if self._used * 3 >= self._capacity * 2:  # load factor 2/3, counting tombstones
            self._resize()
```

`self._used`, not `self._size`, drives the resize. That is the fix for cone accumulation: a table
full of tombstones triggers a rehash even though it holds almost nothing.

Delete:

```python
    def delete(self, key) -> None:
        slot, found = self._probe(key)
        if not found:
            raise KeyError(key)
        self._keys[slot] = _TOMBSTONE             # NOT _EMPTY -- that breaks lookups
        self._values[slot] = None
        self._size -= 1                           # _used is unchanged: the slot is still spent
```

One line and one comment, and they are the point of the whole lesson.

Resize, which also sweeps the cones away:

```python
    def _resize(self) -> None:
        old_keys, old_values = self._keys, self._values
        self._capacity *= 2
        self._keys = [_EMPTY] * self._capacity
        self._values = [None] * self._capacity
        self._size = self._used = 0
        for key, value in zip(old_keys, old_values):
            if key is not _EMPTY and key is not _TOMBSTONE:
                self.put(key, value)              # tombstones are simply not copied
```

### Measuring the damage

The only way to believe the numbers is to produce them:

```python
def average_probes(table: "OpenAddressed", keys: list) -> float:
    total = 0
    for key in keys:
        slot = hash(key) % table._capacity
        probes = 1
        while table._keys[slot] is not _EMPTY and table._keys[slot] != key:
            slot = (slot + 1) % table._capacity
            probes += 1
        total += probes
    return total / len(keys)
```

### The complete file

```python
"""Collisions: linear probing, tombstones, clustering, and where O(1) stops being true."""

_EMPTY = object()
_TOMBSTONE = object()


class OpenAddressed:
    """A hash map with open addressing and linear probing.

    Three slot states: EMPTY (search ends), OCCUPIED, TOMBSTONE (keep probing).
    Resizes on `used` -- entries PLUS tombstones -- so heavy deletion also rehashes.
    """

    def __init__(self, capacity: int = 8) -> None:
        self._capacity = capacity
        self._keys: list = [_EMPTY] * capacity
        self._values: list = [None] * capacity
        self._size = 0
        self._used = 0

    def _probe(self, key) -> tuple[int, bool]:
        slot = hash(key) % self._capacity
        first_tombstone = -1
        for _ in range(self._capacity):
            entry = self._keys[slot]
            if entry is _EMPTY:
                return (first_tombstone if first_tombstone >= 0 else slot), False
            if entry is _TOMBSTONE:
                if first_tombstone < 0:
                    first_tombstone = slot
            elif entry == key:
                return slot, True
            slot = (slot + 1) % self._capacity
        return (first_tombstone if first_tombstone >= 0 else -1), False

    def put(self, key, value) -> None:
        slot, found = self._probe(key)
        if found:
            self._values[slot] = value
            return
        if self._keys[slot] is _EMPTY:
            self._used += 1
        self._keys[slot] = key
        self._values[slot] = value
        self._size += 1
        if self._used * 3 >= self._capacity * 2:
            self._resize()

    def get(self, key, default=None):
        slot, found = self._probe(key)
        return self._values[slot] if found else default

    def delete(self, key) -> None:
        slot, found = self._probe(key)
        if not found:
            raise KeyError(key)
        self._keys[slot] = _TOMBSTONE            # NOT _EMPTY
        self._values[slot] = None
        self._size -= 1

    def _resize(self) -> None:
        old_keys, old_values = self._keys, self._values
        self._capacity *= 2
        self._keys = [_EMPTY] * self._capacity
        self._values = [None] * self._capacity
        self._size = self._used = 0
        for key, value in zip(old_keys, old_values):
            if key is not _EMPTY and key is not _TOMBSTONE:
                self.put(key, value)

    def __len__(self) -> int:
        return self._size

    def tombstones(self) -> int:
        return sum(1 for k in self._keys if k is _TOMBSTONE)

    def probes_for(self, key) -> int:
        slot, probes = hash(key) % self._capacity, 1
        while self._keys[slot] is not _EMPTY and self._keys[slot] != key:
            slot = (slot + 1) % self._capacity
            probes += 1
        return probes


class BrokenDelete(OpenAddressed):
    """Deletion done wrong, so you can watch an entry become unreachable."""

    def delete(self, key) -> None:
        slot, found = self._probe(key)
        if not found:
            raise KeyError(key)
        self._keys[slot] = _EMPTY                # <-- the bug
        self._values[slot] = None
        self._size -= 1


class Colliding:
    """Every instance shares one bucket. Correct, and O(n)."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __hash__(self) -> int:
        return 42

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Colliding) and self.name == other.name

    def __repr__(self) -> str:
        return f"Colliding({self.name!r})"


if __name__ == "__main__":
    # 1. collisions cost time, never correctness
    d = {Colliding(f"k{i}"): i for i in range(5)}
    print(len(d), d[Colliding("k3")])                 # 5 3

    # 2. the deletion bug, made visible
    broken = BrokenDelete(capacity=8)
    a, b = Colliding("a"), Colliding("b")             # both hash to 42 % 8 = 2
    broken.put(a, 1)
    broken.put(b, 2)                                  # probes past a, lands at 3
    print(broken.get(b))                              # 2
    broken.delete(a)                                  # blanks slot 2
    print(broken.get(b, "UNREACHABLE"))               # UNREACHABLE  <- no error!
    print(len(broken))                                # 1 -- it thinks b is still there

    fixed = OpenAddressed(capacity=8)
    fixed.put(a, 1)
    fixed.put(b, 2)
    fixed.delete(a)
    print(fixed.get(b, "UNREACHABLE"))                # 2  -- the tombstone saved it

    # 3. clustering, measured -- fill directly, so no resize hides the effect
    for target_load in (0.25, 0.5, 0.75, 0.9):
        t = OpenAddressed(capacity=4096)
        chosen = [f"k{i}" for i in range(int(4096 * target_load))]
        for k in chosen:
            slot = hash(k) % t._capacity
            while t._keys[slot] is not _EMPTY:
                slot = (slot + 1) % t._capacity
            t._keys[slot] = k
        avg = sum(t.probes_for(k) for k in chosen) / len(chosen)
        print(f"load {target_load:.2f}  ->  {avg:.2f} probes per lookup")
    # load 0.25 -> ~1.2 / 0.50 -> ~1.5 / 0.75 -> ~2.5 / 0.90 -> ~5.5

    # 4. tombstones accumulating
    t = OpenAddressed(capacity=64)
    for i in range(20):
        t.put(f"x{i}", i)
    for i in range(18):
        t.delete(f"x{i}")
    print(len(t), t.tombstones())                     # 2 18 -- 2 entries, 18 cones

    # 5. Python randomises string hashing every run
    print(hash("apple"))    # a different number in every process
```

---

## 6. What it costs

### The average, by load factor

```
 successful lookup, average number of probes

 load     chaining          linear probing      double hashing
  0.25    1.13              1.17                1.15
  0.50    1.25              1.50                1.39
  0.66    1.33              2.00                1.66
  0.75    1.38              2.50                1.85
  0.90    1.45              5.50                2.56
  0.95    1.48             10.50                3.15
  0.99    1.50             50.50                4.65
```

Two readings. **Chaining degrades gently and linear probing falls off a cliff** — and yet open
addressing is what most modern implementations use, because at a load factor of 0.66 the difference
is two probes against one and a third, and those two probes are on *adjacent memory*, which the
processor's cache handles far better than following two pointers. The theory favours chaining; the
hardware favours probing.

### The worst case, priced

```
 n = 100,000 keys, all colliding into one bucket:

   building the map  : 1 + 2 + 3 + ... + n = n(n-1)/2 = 5,000,000,000 comparisons
   one lookup        : 100,000 comparisons
   vs a good hash    : 1 lookup ~1.3 comparisons

 76,000x slower per lookup, with identical code and identical data volume.
```

### The tombstone problem, priced

```
 capacity 1,024, workload: insert 600, delete 590, insert 590 more...

   after a while : ~10 live entries, ~600 tombstones
   load factor by SIZE   : 0.01   -- "the map is nearly empty"
   load factor by USED   : 0.60   -- what lookups actually experience
   average probes        : ~2.5, on a map holding ten things

 Resize on `used`, not on `size`, or a shrinking map gets slower.
```

### Java's treeification, priced

```
 a bucket with 1,000 colliding entries:

   plain chain        : 1,000 comparisons per lookup
   red-black tree     : log2(1000) ~ 10 comparisons

 100x, and it turns a denial-of-service attack into a slowdown.
 Java converts a chain to a tree at 8 entries (and back at 6).
```

### The attack, with real numbers

```
 Hash-flooding, roughly as demonstrated in 2011:

   send an HTTP POST with 20,000 form fields whose names all collide
   the server builds a dict of the parameters:
     normal keys : 20,000 inserts x ~1 comparison   =    20,000 operations
     colliding   : 20,000 x 20,000 / 2              = 200,000,000 operations
   -> ~1 second of pure CPU, from a request of a few hundred kilobytes

   a handful of such requests per second saturates a core.
   Affected: PHP, Java, Python, Ruby, ASP.NET, node.js -- all of them.
```

The fix, adopted almost everywhere: **randomise the hash per process**, so the attacker cannot
precompute colliding keys. Python does this for strings and bytes by default since 3.3, seeded at
start-up (`PYTHONHASHSEED` can pin it, for reproducible tests only). Many languages went further and
adopted **SipHash**, a keyed hash designed to be unpredictable without a secret.

### Memory

```
 1,000,000 entries

 chaining        : array of 1,000,000 pointers  +  1,000,000 nodes
                   each node = key + value + next pointer  ~ 56 bytes
                   total ~ 64 MB

 open addressing : one array, 1,000,000 / 0.66 = 1,515,000 slots
                   each slot = key + value  ~ 32 bytes
                   total ~ 48 MB, and contiguous
```

---

## 7. The traps

### The real failure: deleting by blanking the slot

```python
broken = BrokenDelete(capacity=8)
a, b = Colliding("a"), Colliding("b")     # both land in the same slot
broken.put(a, 1)
broken.put(b, 2)                          # probes past a
print(broken.get(b))
broken.delete(a)
print(broken.get(b, "UNREACHABLE"))
print(len(broken))
```

```
2
UNREACHABLE
1
```

The entry is physically in the array, the map reports a length of 1, and the value cannot be
retrieved by its key. **No exception, ever.** This is the single most important thing to know about
open addressing, and it is why the tombstone exists.

### The trap: resizing on `size` instead of `used`

```python
if self._size * 3 >= self._capacity * 2:      # <-- wrong counter
```

A workload that inserts and deletes in equal measure keeps `_size` low forever, so no resize is ever
triggered, and the table fills with tombstones until every lookup walks half the array. The map looks
empty and behaves as though it were full. Count tombstones towards the resize.

### The real error: mutating a key so it lands in the wrong bucket

```python
class Tag:
    def __init__(self, name): self.name = name
    def __hash__(self): return hash(self.name)
    def __eq__(self, other): return self.name == other.name

t = Tag("draft")
d = {t: "doc"}
t.name = "published"
print(t in d, len(d))
```

```
False 1
```

The entry is in the map and unreachable by any key, including the object that created it. Same
failure as a wrong deletion, from the other direction. **Hash on fields that never change.**

### The trap: a hash function using too little of the key

```python
class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id = order_id                # "ORD-2026-000123"
    def __hash__(self) -> int:
        return hash(self.order_id[:4])          # <-- "ORD-" for every single order
    def __eq__(self, other) -> bool:
        return self.order_id == other.order_id
```

Deterministic, fast, and every order in the system lands in one bucket. Nothing raises; the map is
correct and quadratic. **A hash must use the parts of the key that actually vary.** The safe default
in Python is to hash a tuple of the identifying fields:

```python
    def __hash__(self) -> int:
        return hash((self.order_id,))
```

### The trap: integer keys that step by the capacity

```python
d = {}
for i in range(0, 1_000_000, 8):     # every key is a multiple of 8
    d[i] = i
```

`hash(n) == n` for small integers in Python, so with a capacity that is a power of two, keys stepping
by eight all share the low bits. Python's probe sequence mixes in the *high* bits precisely to
survive this, but a hand-written table with `hash(key) % capacity` and linear probing degrades badly.
**Sequential integers are fine; integers with a stride equal to the table size are the worst case.**

### The trap: relying on a hash value across runs or processes

```bash
python -c "print(hash('apple'))"
python -c "print(hash('apple'))"
```

```
-8395723518259234171
5731011213473296981
```

String hashing is seeded randomly per process. **Never persist a Python hash to disk, never send one
over the network, never use one as a database key, and never write a test that asserts a specific
hash value.** If you need a stable digest, use `hashlib` — `hashlib.sha256(s.encode()).hexdigest()` —
which is deterministic across runs and machines.

### The trap: assuming a set makes duplicate detection safe against an adversary

```python
def has_duplicates(items: list) -> bool:
    return len(set(items)) != len(items)
```

`O(n)` on normal input, `O(n²)` if the caller supplies items crafted to collide. If `items` comes
from a request body and the objects are user-controlled with a custom `__hash__`, this is a
denial-of-service vector. For untrusted input, either use built-in types (which are hash-randomised)
or bound the input size.

---

## 8. In the interview

### How it gets asked

- *"What is the worst-case complexity of a hash map lookup? When does it happen?"* — the direct form.
  `O(n)`, and the three causes.
- *"How do you handle collisions?"* — chaining and open addressing, with the trade between them.
- *"How would you delete from an open-addressed table?"* — the tombstone question, and the best answer
  starts by showing what goes wrong without one.
- *"Why does a hash map get slow before it gets full?"* — clustering, and the load-factor cliff.
- *"Why does Python's `hash('a')` change between runs?"* — hash randomisation, and the attack behind
  it.
- *"Your dictionary lookups got slow in production. Diagnose it."* — the open-ended version, and the
  answer is a checklist.

### What to say out loud, in the first ninety seconds

1. **Answer both halves immediately.** *"O(1) average, O(n) worst case. The worst case is when every
   key lands in the same bucket, and then the map is a linked list with extra steps."*
2. **Say collisions are normal, not exceptional.** *"Collisions are guaranteed — more possible keys
   than buckets. And they arrive early: with a million buckets, about twelve hundred keys gives you a
   fifty percent chance of one. It's the birthday problem."*
3. **Give the two strategies and the trade.** *"Chaining puts a list in each bucket — deletion is
   trivial and the load factor can exceed one. Open addressing probes for another slot — denser, much
   better cache behaviour, and that's why Python and Go use it, but deletion needs tombstones."*
4. **Volunteer the tombstone before being asked.** *"With probing you can't blank a deleted slot,
   because a lookup stops at the first empty one — so an entry that probed past it becomes
   unreachable, with no error. You leave a marker meaning 'keep going'."*
5. **Name the three real causes of the worst case.** *"A hand-written hash using too little of the
   key. Keys whose values step by exactly the table size. And an adversary choosing the keys — which
   was a real DoS class in 2011, and is why Python randomises string hashing per process."*

### The follow-ups

**"How would you implement deletion in an open-addressed table?"**
I would start by saying what goes wrong with the obvious version, because that is the whole question.
A lookup probes from the key's home slot and stops at the first empty slot, because under the
insertion rule nothing could have been placed past an empty one. So if I delete an entry by blanking
its slot, any entry that probed *past* that slot during insertion becomes unreachable — the lookup
walks to the newly emptied slot, sees empty, and reports not found. The entry is physically in the
array, `len()` still counts it, and nothing raises. So a slot needs three states rather than two:
empty, occupied, and deleted. The deleted marker is called a tombstone, and it means "something was
here, keep probing". A lookup treats it as occupied and continues; an insert treats it as free and
may reuse it, though it should remember the *first* tombstone it passed and keep probing to check the
key is not already present further along — otherwise you get two entries for one key. The second half
of the answer is that tombstones then become their own problem: each one costs a probe and holds
nothing, so a workload with heavy insertion and deletion fills the table with markers while the map
appears to be shrinking, and lookups get slower. The fix is to track two counters — live entries, and
entries plus tombstones — and to trigger the resize on the second one. That means a hash map that is
shrinking can still need a rehash, which surprises people and is the correct behaviour.

**"Why does a hash map get slow before the table is full?"**
Because of clustering, and it is specific to probing. With linear probing, once a run of consecutive
slots is occupied, any key hashing anywhere inside that run has to walk to the end of it and lands
just past — which makes the run one longer, which makes it catch more keys. It feeds itself. That is
primary clustering, and the effect on lookup cost is not gradual: the average number of probes for a
successful lookup goes roughly 1.5 at load 0.5, 2.5 at 0.75, 5.5 at 0.9, 10.5 at 0.95, and about 50
at 0.99. It is flat and then vertical, with no useful warning region — which is exactly why every
implementation resizes at a fixed load factor around two-thirds rather than waiting to notice
slowness. There are two standard mitigations. Quadratic probing jumps by 1, 4, 9, 16 so runs do not
merge, which removes primary clustering, though keys with the same starting slot still follow the
same path — secondary clustering. Double hashing derives the step size from a second hash of the key,
so two keys starting in the same slot walk off in different directions, and that is the best of the
three. Python does something in that spirit: its probe sequence mixes in the high bits of the hash
that the initial modulo threw away, so keys agreeing in the low bits still separate quickly.

**"Why does `hash('apple')` give a different answer every time I run Python?"**
Because string hashing is seeded with a random value at interpreter start-up, and that is a security
feature rather than an accident. The attack it defends against is hash flooding. Around 2011 it was
demonstrated against essentially every web stack — PHP, Java, Python, Ruby, ASP.NET, node — and the
mechanism is simple: the server puts request parameters into a hash map, so an attacker sends a form
with twenty thousand field names crafted to hash to the same bucket. Insertion then degrades to
quadratic, so twenty thousand parameters cost two hundred million comparisons instead of twenty
thousand — about a second of CPU for a request of a few hundred kilobytes, and a handful per second
saturates a core. Randomising the seed per process means the attacker cannot precompute a colliding
set, because they do not know the seed; several languages went further and adopted SipHash, a keyed
hash designed to be unpredictable. Two practical consequences follow and both matter. You must never
persist a Python hash value, send it over a network, use it as a database key, or assert on it in a
test, because it is only stable within one process — if you need a stable digest, that is `hashlib`.
And it does not affect dictionary iteration order, because Python's insertion-order guarantee is a
separate mechanism and it does hold across runs. Java took a different route to the same problem: it
converts a chain of eight or more entries into a balanced tree, so a flooded bucket degrades to
O(log n) rather than O(n).

### A model answer

> "O(1) on average, O(n) in the worst case, and the worst case is when every key ends up in the same
> bucket — at which point the map is a linked list with extra steps and building it is O(n²).
>
> The thing I'd say first is that collisions themselves are normal rather than exceptional. There are
> always more possible keys than buckets, so some must share, and they arrive much earlier than people
> expect — it's the birthday problem, so with a million buckets you have about a fifty percent chance
> of a collision by around twelve hundred keys. Collision handling is the operating condition, not an
> edge case. And collisions only ever cost time, never correctness, provided equality distinguishes the
> keys.
>
> There are two strategies. Chaining keeps a small list in each bucket, so lookup checks one bucket and
> scans a short list. Deletion is trivial and the load factor can go above one. Open addressing has no
> lists — on a collision it probes for another slot by a rule. It's denser, and because the slots are
> adjacent in memory the processor's cache works for you, which is why it's usually faster in practice
> and why Python and Go both use it. What it costs is deletion.
>
> That's the part worth showing rather than stating. A lookup probes from the home slot and stops at
> the first empty slot, because nothing could have been placed past one. So if I delete by blanking a
> slot, an entry that probed past it during insertion becomes unreachable — it's sitting in the array,
> `len()` still counts it, and the lookup reports not found with no error. So slots need three states,
> and the third is a tombstone meaning 'keep probing'. Then tombstones become their own problem,
> because each one costs a probe and holds nothing — so I'd count live entries and entries-plus-
> tombstones separately and resize on the second. Which means a shrinking map can need a rehash.
>
> On when the worst case actually happens: three ways. A hand-written hash that uses too little of the
> key — I've seen one that hashed the first four characters of an order id, and every order started
> 'ORD-'. Integer keys stepping by exactly the table size. And an adversary choosing the keys, which
> was a real denial-of-service class in 2011 — twenty thousand colliding form fields turning twenty
> thousand operations into two hundred million. That's why Python randomises string hashing per
> process, and why you must never persist a Python hash value."

---

## 9. Recall card

- **Collisions are guaranteed and normal** — more keys than buckets, and they arrive early
  (birthday problem: 10⁶ buckets, ~1,178 keys → 50%). They cost **time, never correctness**, as long
  as `__eq__` distinguishes the keys.
- **Chaining**: a list per bucket. Deletion trivial, load factor may exceed 1, degrades *gently*
  (~1.5 probes even at load 0.99), but scattered memory. **Java 8+ turns a chain of 8 into a tree** →
  O(log n). **Open addressing**: probe for another slot. Denser, cache-friendly — what **Python and
  Go** use — and it falls off a **cliff** (1.5 probes at load 0.5 → 2.5 at 0.75 → 10.5 at 0.95 → ~50
  at 0.99), which is why everyone resizes at ~0.66.
- **You cannot delete by blanking a slot.** A lookup stops at the first EMPTY slot, so anything that
  probed past becomes **unreachable with no error** while `len()` still counts it. Use a
  **tombstone** — empty / occupied / deleted — which lookups skip and inserts may reuse.
- **Tombstones then accumulate**: each costs a probe and holds nothing, so **resize on
  `entries + tombstones`, not on `len`** — a *shrinking* map can need a rehash.
- **Three real causes of O(n):** a hash using too little of the key (`hash(order_id[:4])`) · integer
  keys stepping by exactly the capacity · **an adversary** — 20,000 colliding form fields turned
  20,000 operations into 200,000,000 in the 2011 hash-flooding attacks. Hence Python's per-process
  **hash randomisation**: never persist, transmit, or assert on a `hash()` value — use `hashlib`.
