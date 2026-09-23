---
day: 65
track: dsa
title: "Hashing your own objects"
phase: "Hashing: maps and sets"
status: written
---

# Day 065 · DSA — Hashing your own objects

**After today you can:** You can make a custom class usable as a dictionary key without subtle bugs.

**The interviewer asks it as:** *Why did putting this object in a set not deduplicate it?*

---

## 1. What this is, and why they ask it

Everything you have put in a set or used as a dictionary key so far has been a number, a string or a
tuple — things Python already knows how to hash. Today you write a class of your own and put it in a
set. It will not work the way you expect, and the reason is a **contract** with exactly two rules
that every language enforces the same way: **if two objects are equal, their hashes must be equal**,
and **a key's hash must never change while it is in the table**.

They ask it because it is a bug you can watch happen. The interviewer creates two objects that are
obviously the same order, puts both in a set, and the set has two elements in it. Or they put one in
and then change a field and it becomes unfindable — `obj in d` returns `False`, with no error, while
the object is sitting inside the dictionary. Both of those are three lines of setup and both catch
out people who have used hash maps for years without ever asking what a key really has to be.

It is also where the interview crosses from data structures into design. `__eq__` is you deciding
what "the same" means for your domain — two orders with the same id, or two orders with every field
matching? — and `__hash__` has to agree with whatever you decided. Getting that pair right is the
same skill as designing a grouping key in [day 064](../day-064-grouping/README.md), and interviewers
know it.

---

## 2. The story

Nagaraj has taken in washing on the same corner in Rajajinagar for twenty-six years. Two rooms, and a
long steel rail along one wall with a hundred and forty hooks on it.

When his son took over the counter, he did it the way that seemed obvious. A bundle comes in, you
hang it on the next empty hook, and you tell the person their hook number. Nothing was ever lost.

What it did instead was stranger. Mrs Fernandes came in on a Monday, again on a Thursday and again
the following Tuesday, and by the end of the month she had four bundles on four hooks in four
different parts of the rail. To the shop these were four unrelated things, because they arrived as
four separate bundles. When she rang to ask whether her blue sari had come back, the only answer was
to walk the whole rail.

Nagaraj came back and changed it in an afternoon. The hook is not the next free one any more. The
hook is decided by the phone number — the last two digits tell you which hook, and that is that. Same
person, same hook, every time, no matter how many times they come.

Now when Mrs Fernandes rings, he does not walk anything. Her number ends 31, so he goes to hook 31,
and everything of hers is there together.

There is one thing he is careful about, and he learned it the hard way in about the second month.

A regular customer changed her phone number. She told him, and he was pleased to be told, and he
updated it in his phone. What neither of them thought about was the bundle already hanging on hook
14 — hung there because her old number ended 14. Her new number ended 62. Three days later she came
to collect, he went to hook 62, and there was nothing there. Her clothes were eleven feet away on a
hook that, as far as the shop's rule was concerned, had nothing to do with her. He found them
eventually, by going through the rail the old way, which took forty minutes.

His rule since then is short. The number the hook is chosen from does not change while the bundle is
hanging. If somebody changes their number, the bundle comes off the rail first and goes back on
afterwards.

---

## 3. The idea in plain English

The rail is a **hash table**. The hook is the **bucket**. The rule "last two digits of the phone
number" is the **hash function**, and it is computed **from the value of the thing**, not from which
physical bundle it happens to be.

The son's version — next free hook — is what Python does by default with your classes, and it is why
your set has two elements in it when you expected one.

### Why two identical objects are two different things

```python
class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id = order_id

a = Order("A-1")
b = Order("A-1")

a == b            # False
len({a, b})       # 2
```

By default, Python gives every object an `__eq__` that means "is this literally the same object in
memory?" and a `__hash__` derived from its memory address. Two `Order("A-1")` objects live at two
addresses, so they are unequal and they hash differently. The set is behaving perfectly; it just does
not know that you consider them the same order.

**This is the answer to the interview question.** "It did not deduplicate because the class does not
define `__eq__` and `__hash__`, so Python compared identity, not value."

### The contract

Two rules. Every language has them; Java writes them as `equals` and `hashCode`.

> **Rule 1: if `a == b`, then `hash(a) == hash(b)`.**
>
> **Rule 2: an object's hash must not change while it is a key.**

Rule 1 is one-directional. Two unequal objects are *allowed* to share a hash — that is just a
collision, which [day 061](../day-061-collisions/README.md) says is normal and costs time, not
correctness. What is not allowed is the reverse: two equal objects with different hashes. Then the
lookup goes to the wrong hook and never finds the thing, and nothing raises.

Rule 2 is Mrs Fernandes's neighbour. The bundle is fine, the shop is fine, and the two have lost
track of each other.

### Writing the pair

```python
class Order:
    def __init__(self, order_id: str, customer: str) -> None:
        self.order_id = order_id
        self.customer = customer

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id

    def __hash__(self) -> int:
        return hash(self.order_id)
```

Three things to notice, and each one is a question an interviewer might ask.

**`isinstance` and `NotImplemented`.** Returning `NotImplemented` — not `False` — lets Python try the
other object's `__eq__` before giving up. `Order("A-1") == "A-1"` then correctly gives `False`
instead of raising.

**The same fields in both.** `__eq__` uses `order_id`; `__hash__` uses `order_id`. If `__eq__`
compared both fields and `__hash__` used only one, that would still be legal — equal objects would
still hash the same. The other way round is the bug.

**Hash a tuple when there are several fields.** `hash((self.first, self.last))` — do not add them or
combine them by hand. The tuple's own hash mixes them properly, and it is one line.

### The thing that catches everybody

Defining `__eq__` and nothing else makes your class **unhashable**:

```python
>>> class Q:
...     def __init__(self, n): self.n = n
...     def __eq__(self, other): return self.n == other.n
...
>>> {Q("a")}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'Q'
```

Python sets `__hash__ = None` the moment you define `__eq__`. It is being deliberately strict: you
have just told it that equality means something new, and the inherited identity hash would now break
rule 1. Rather than let you have a silent bug, it takes hashing away until you define it. **This is
Python protecting you, and saying so out loud in an interview is a good line.**

### Dataclasses, and the three settings

Most of the time you will not write any of this by hand.

```python
from dataclasses import dataclass

@dataclass                       # eq=True by default -> __hash__ = None
class R:
    n: str

{R("a")}                         # TypeError: unhashable type: 'R'
```

A plain `@dataclass` generates `__eq__` comparing all fields, and therefore sets `__hash__` to
`None`, for exactly the reason above. Three ways out:

```python
@dataclass(frozen=True)          # immutable -> gets __eq__ AND __hash__
class Point:
    x: int
    y: int

@dataclass(eq=False)             # keeps identity equality and identity hash
class Node:
    value: int

@dataclass(unsafe_hash=True)     # generates __hash__ on a mutable class.
class Risky:                     # The name is a warning, not decoration.
    value: int
```

`frozen=True` is the one to reach for, and it is the right default for anything you intend to use as
a key. It gives you both methods, and it makes rule 2 impossible to break because the fields cannot
be reassigned.

### `NamedTuple` — the answer when you want no ceremony

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

{Point(1, 2), Point(1, 2)}       # {Point(x=1, y=2)} — one element
```

A `NamedTuple` is a tuple, so it is hashable and immutable for free, compares by value, and prints
nicely. For coordinates, pairs and small value objects in an interview, this is two lines and no
explanation needed.

### What to hash on

The same judgement as designing a grouping key.

- **Hash on identity fields, not on everything.** An `Order` with an `order_id` should hash on the
  id. Whether the delivery address changed does not make it a different order.
- **Hash on fields that never change.** This is rule 2 in practice. An id, a timestamp of creation, a
  natural key — never a status, a count, or a list.
- **Never hash on a mutable container.** `hash(self.items)` where `items` is a list raises. Use
  `tuple(self.items)`, and only if the list genuinely never changes.
- **Cheap is important.** `__hash__` runs on every single lookup. Hashing a field that is a
  hundred-kilobyte string means every dictionary operation reads a hundred kilobytes.

---

## 4. The picture

The same two objects, before and after the pair is defined.

```
 WITHOUT __eq__ / __hash__          (Python uses the memory address)

   a = Order("A-1")  at 0x7f3a01  ->  hash 0x7f3a01 % 8  ->  hook 1
   b = Order("A-1")  at 0x7f3b90  ->  hash 0x7f3b90 % 8  ->  hook 6

   hook:  0    1     2    3    4    5    6     7
        +----+-----+----+----+----+----+-----+----+
        |    |  a  |    |    |    |    |  b  |    |     len(set) == 2
        +----+-----+----+----+----+----+-----+----+


 WITH __eq__ / __hash__ on order_id (Python uses the value)

   a = Order("A-1")  ->  hash("A-1") % 8  ->  hook 3
   b = Order("A-1")  ->  hash("A-1") % 8  ->  hook 3, then a == b -> replace

   hook:  0    1    2     3     4    5    6    7
        +----+----+----+-----+----+----+----+----+
        |    |    |    |  a  |    |    |    |    |     len(set) == 1
        +----+----+----+-----+----+----+----+----+
```

What to notice: nothing about the set changed. The set was always going to put the object where the
hash said. All that changed is what the hash is computed *from* — the address, or the value.

Now rule 2, drawn. This is the bug you cannot see:

```
 step 1   d[order] = "paid"      hash("A-1") % 8 = 3
          hook:  3 -> [ order ]

 step 2   order.order_id = "A-2"     the object is still on hook 3

 step 3   order in d ?           hash("A-2") % 8 = 6
          hook:  6 -> empty      ->  False

 hook:  0    1    2     3      4    5     6      7
      +----+----+----+------+----+----+-------+----+
      |    |    |    |order |    |    | empty |    |
      +----+----+----+------+----+----+-------+----+
                        ^                ^
                  it is here      we look here
```

`len(d)` still says 1. Iterating the dictionary still yields the order. Asking for it returns
`False`. No exception anywhere. That is the worst failure mode a data structure has, and it is why
rule 2 exists.

---

## 5. The code, built step by step

### Step 1 — watch it fail

```python
class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id = order_id

print(len({Order("A-1"), Order("A-1")}))    # 2
print(Order("A-1") == Order("A-1"))         # False
```

Run this before you fix anything. The two lines of output are the whole interview question.

### Step 2 — add `__eq__` alone, and watch it fail differently

```python
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id
```

```python
>>> {Order("A-1")}
TypeError: unhashable type: 'Order'
```

Equality now works and hashing is gone. Say why: defining `__eq__` sets `__hash__` to `None`, because
the inherited address-based hash would now break rule 1.

### Step 3 — add `__hash__` on the same field

```python
    def __hash__(self) -> int:
        return hash(self.order_id)
```

```python
>>> len({Order("A-1"), Order("A-1")})
1
```

One field, one `hash()` call, and the whole thing works. When there are several fields, put them in a
tuple:

```python
    def __hash__(self) -> int:
        return hash((self.order_id, self.customer))
```

### Step 4 — make rule 2 impossible to break

The version above still lets somebody write `order.order_id = "A-2"` while it sits in a dictionary.
Freeze it:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Order:
    order_id: str
    customer: str
```

Four lines, both methods generated, and assignment now raises:

```python
>>> order = Order("A-1", "fernandes")
>>> order.order_id = "A-2"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
dataclasses.FrozenInstanceError: cannot assign to field 'order_id'
```

An error at the moment of the mistake, instead of a silent wrong answer later. That is the trade
`frozen=True` buys, and it is the sentence to say.

### Step 5 — when the identity is one field but equality is all of them

Real domains often want: two orders are the same order if the ids match, whatever else differs. A
frozen dataclass compares every field, which is not that. Write it by hand:

```python
@dataclass(frozen=True, eq=False)      # keep frozen; write our own equality
class Order:
    order_id: str
    customer: str
    total_paise: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id

    def __hash__(self) -> int:
        return hash(self.order_id)
```

Now two orders with the same id and different totals are equal and hash together, which is what the
business means by "the same order". `eq=False` stops the dataclass generating an `__eq__` that would
override yours, and it also stops it blanking `__hash__`.

### The complete solution

```python
from dataclasses import dataclass, FrozenInstanceError
from typing import NamedTuple


@dataclass(frozen=True)
class Point:
    """The default choice for a value object used as a key.

    frozen=True gives __eq__ and __hash__ over all fields, and makes rule 2
    unbreakable because the fields cannot be reassigned.
    """
    x: int
    y: int


class Cell(NamedTuple):
    """The no-ceremony version: a tuple, so hashable and immutable for free."""
    row: int
    column: int


@dataclass(frozen=True, eq=False)
class Order:
    """Identity is the id alone; the other fields are data about it."""
    order_id: str
    customer: str
    total_paise: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id

    def __hash__(self) -> int:
        return hash(self.order_id)


class Mutable:
    """The hand-written pair, for when a dataclass is not available.
    Note that nothing here stops rule 2 being broken."""

    def __init__(self, key: str, payload: str) -> None:
        self.key = key
        self.payload = payload

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Mutable):
            return NotImplemented
        return self.key == other.key

    def __hash__(self) -> int:
        return hash(self.key)

    def __repr__(self) -> str:
        return f"Mutable({self.key!r}, {self.payload!r})"


if __name__ == "__main__":
    print(len({Point(1, 2), Point(1, 2)}))            # 1
    print(len({Cell(0, 0), Cell(0, 0), Cell(0, 1)}))  # 2

    a = Order("A-1", "fernandes", 45000)
    b = Order("A-1", "fernandes", 99999)
    print(a == b, len({a, b}))                        # True 1

    try:
        Point(1, 2).x = 5
    except FrozenInstanceError as error:
        print(type(error).__name__, error)
        # FrozenInstanceError cannot assign to field 'x'

    # Rule 2, broken on purpose, so you can see the silence.
    lookup = {Mutable("A-1", "paid"): "receipt-9"}
    key = next(iter(lookup))
    key.key = "A-2"
    print(key in lookup, len(lookup), list(lookup))
    # False 1 [Mutable('A-2', 'paid')]
```

Read that last line of output twice. The dictionary contains the key. `len` says one. Asking for it
says `False`.

---

## 6. What it costs

### What `__hash__` costs, per operation

`__hash__` runs on every insert, every lookup, every `in`. Not once — every time. So its cost is
multiplied by the number of dictionary operations in your whole program.

```
 hash(self.order_id)                 reads a ~10-char string   ~ 40 ns
 hash((self.a, self.b, self.c))      builds a 3-tuple, hashes  ~ 120 ns
 hash(self.description)              reads a 100 KB string     ~ 8,000 ns
 hash(tuple(self.items))             builds a 10,000-list      ~ 200,000 ns
```

That last one is the disaster. Building a tuple from a ten-thousand-element list on every lookup
turns an O(1) dictionary into something that reads ten thousand elements per operation. A million
lookups is 10<sup>10</sup> element reads. **Hash the id, not the contents.**

Python does cache the hash of a `str` after computing it once, which is why string keys are fast. It
does not cache yours.

### What a bad `__hash__` costs

Suppose you write this, because it seems reasonable:

```python
    def __hash__(self) -> int:
        return hash(self.customer)      # thousands of orders per customer
```

It satisfies rule 1 only if `__eq__` also uses just `customer` — but suppose `__eq__` uses
`order_id`. Then two unequal orders share a hash, which is legal, and everything still works. It just
gets slow, in the way [day 061](../day-061-collisions/README.md) described:

```
 100,000 orders, 500 customers
 -> average chain length 100,000 / 500 = 200
 -> a lookup compares ~200 keys instead of ~1
 -> 100,000 lookups: 20,000,000 comparisons instead of 100,000
```

Two hundred times slower, with no error and no wrong answers. This is the difference between an O(1)
map and an O(n) one, produced by one plausible line.

And the extreme version, `return 1`, is legal and turns the dictionary into a list: building it is
O(n²), which at n = 20,000 is 400,000,000 comparisons.

### What the fixes cost

```
 @dataclass(frozen=True)     0 extra lines beyond the class, ~0 runtime cost
 NamedTuple                  0 extra lines, and slightly FASTER than a dataclass
                             because tuple hashing is implemented in C
 hand-written pair           ~8 lines, and the risk of getting rule 1 wrong
```

There is no performance argument for writing the pair by hand. Write it by hand only when equality
means something the generated version does not.

---

## 7. The traps

### Trap 1 — `__eq__` without `__hash__`

```python
>>> class Q:
...     def __init__(self, n): self.n = n
...     def __eq__(self, other): return self.n == other.n
...
>>> {Q("a")}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'Q'
>>> Q.__hash__ is None
True
```

The fix is to add `__hash__`, not to delete `__eq__`. And note what the error does *not* say — it
does not mention `__eq__` at all, so the connection is not obvious the first time.

### Trap 2 — the plain `@dataclass` is unhashable

```python
>>> from dataclasses import dataclass
>>> @dataclass
... class R:
...     n: str
...
>>> {R("a")}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'R'
```

Exactly the same cause — the generated `__eq__` blanks `__hash__` — and it surprises people much more
because they did not write an `__eq__`. `frozen=True` is the fix.

### Trap 3 — mutating a key while it is in the table

This is the one with no error at all, so it is the one worth doing yourself once:

```python
>>> lookup = {Mutable("A-1", "paid"): "receipt-9"}
>>> key = next(iter(lookup))
>>> key.key = "A-2"
>>> key in lookup
False
>>> len(lookup)
1
>>> list(lookup)
[Mutable('A-2', 'paid')]
```

The object is in there. `len` counts it. Iterating yields it. `in` says no. Nothing raises, nothing
logs, and the only symptom is that some record has quietly stopped being found.

`frozen=True` makes this impossible, which is the entire argument for it.

### Trap 4 — `unsafe_hash=True` used to shut the error up

```python
@dataclass(unsafe_hash=True)
class Risky:
    value: int
```

This generates a `__hash__` on a mutable class. It compiles, the `TypeError` goes away, and you have
just re-enabled trap 3. The keyword is called `unsafe_hash` because the authors wanted you to have to
type the word "unsafe". If you find yourself reaching for it, the question is why the object is
mutable.

### Trap 5 — `__eq__` that raises on a different type

```python
    def __eq__(self, other):
        return self.n == other.n        # no isinstance check
```

```python
>>> Q("a") == "a"
AttributeError: 'str' object has no attribute 'n'
```

Equality should never raise. Anything can be compared to anything in Python — including by `in`,
which compares your object against whatever is in the container. Guard with `isinstance` and return
`NotImplemented`.

### Trap 6 — hashing on a field that is a list

```python
    def __hash__(self):
        return hash(self.items)         # items is a list
```

```
TypeError: unhashable type: 'list'
```

`tuple(self.items)` fixes the error and introduces two new problems: it is O(len(items)) on every
lookup, and if the list ever changes you are back in trap 3. If a collection is really part of the
identity, use a `frozenset` or a `tuple` field from the start and never a list.

### Trap 7 — inheritance breaking symmetry

```python
@dataclass(frozen=True)
class Point:
    x: int
    y: int

@dataclass(frozen=True)
class Point3D(Point):
    z: int
```

`Point(1, 2) == Point3D(1, 2, 3)` is `False`, and `Point3D(1, 2, 3) == Point(1, 2)` is `False` too,
because the dataclass `__eq__` compares `other.__class__ is self.__class__`. That is symmetric and
correct. But a hand-written `isinstance`-based `__eq__` is *not* symmetric under inheritance — the
parent would accept the child and the child would reject the parent, so `a == b` and `b == a` could
disagree, and a set would then behave differently depending on insertion order. Prefer exact-class
comparison when inheritance is in play, and say why.

---

## 8. In the interview

### How it gets asked

- The demonstration: *"I put these two objects in a set and got two elements. Why?"* Three lines on
  the screen, and the whole answer is identity versus value equality.
- The contract: *"What is the relationship between `equals` and `hashCode`?"* — the Java phrasing,
  asked at every company that hires Java engineers, and the expected answer is rule 1 plus the fact
  that the converse does not hold.
- The bug hunt: *"This object is in the map but `containsKey` returns false. What happened?"* Rule 2,
  every time.
- The design version: *"Make this class usable as a dictionary key."* Where the real question is
  *which fields*, not *which methods*.

### What to say out loud, in the first ninety seconds

1. **Name the default before you fix it.** "By default Python compares objects by identity, not by
   value, and the default hash comes from the memory address. So two objects with identical fields
   are two different keys, and the set is right."
2. **State the contract as two rules.** "Equal objects must have equal hashes; unequal objects may
   share a hash and that is just a collision. And the hash must not change while the object is a key."
3. **Say which fields, and why.** "Identity here is the order id. The customer name and the total are
   data about the order, not what makes it that order. So both methods use the id."
4. **Say the immutability point without being asked.** "I would make it frozen, so the field cannot
   be reassigned while it is a key. That converts a silent wrong answer into an error at the moment
   of the mistake."
5. **Then write four lines.** `@dataclass(frozen=True)` and the fields.

### The follow-ups

**"Can two unequal objects have the same hash?"**
"Yes, and they must be allowed to — there are more possible values than hash values, so collisions
are unavoidable. A collision costs time, not correctness: the table compares with `__eq__` after
finding the bucket. What is forbidden is the reverse, two equal objects with different hashes,
because then the lookup goes to the wrong bucket and finds nothing, silently."

**"What happens if I mutate a key?"**
"The object stays in the bucket it was placed in, but lookups now compute a different bucket, so it
becomes unreachable. `len` still counts it and iteration still yields it — `in` just returns `False`.
No exception. That is why I freeze anything used as a key."

**"Why does defining `__eq__` remove hashing?"**
"Because Python knows the inherited hash is now wrong. You have redefined equality by value while the
hash is still by address, which breaks rule 1 immediately. Rather than let that be a silent bug, it
sets `__hash__` to `None` so you get a `TypeError` the first time you try. Java does not do this,
which is exactly why 'always override `hashCode` when you override `equals`' is such a well-worn
piece of Java advice."

**"What would you hash on for a large object?"**
"The identity fields, and cheap ones. `__hash__` runs on every lookup, so hashing a hundred-kilobyte
description field means every dictionary operation reads a hundred kilobytes. And I would never hash
a mutable collection — building a tuple from a ten-thousand-element list on every lookup turns an
O(1) map into something that reads ten thousand items per operation."

**"How is this the same as yesterday's grouping key?"**
"It is the same question. `__eq__` decides what makes two objects the same, and a grouping key
decides what makes two items belong in the same pile. Both fail the same two ways — too coarse and
things merge that should not, too fine and one thing splits into many. `__hash__` just has to agree
with whatever `__eq__` decided."

### A model answer

Asked: *why did putting this object in a set not deduplicate it?*

> "Because the class does not define `__eq__` and `__hash__`, so Python is using its defaults, and
> the defaults are about identity rather than value. The default `__eq__` asks 'is this literally the
> same object in memory', and the default hash comes from the address. Two `Order('A-1')` objects are
> at two addresses, so they are unequal and they hash to different buckets. The set is behaving
> correctly — it does not know that I consider them the same order.
>
> To fix it I have to define both, and they have to agree, because the contract is that equal objects
> must have equal hashes. The converse is not required — two unequal objects sharing a hash is just a
> collision, which costs a comparison and not correctness.
>
> The design question is which fields. Here the identity of an order is its id; the customer and the
> total are facts about the order rather than what makes it that order. So `__eq__` compares ids and
> `__hash__` hashes the id. If several fields made up the identity I would hash a tuple of them and
> let the tuple do the mixing.
>
> There is a second rule that matters more than people expect: the hash must not change while the
> object is a key. If I put an order in a dictionary and then reassign its id, the object stays in
> the bucket it was filed under, but every lookup computes a different bucket. So `in` returns False
> while `len` still counts it and iteration still yields it, with no exception at all. That is the
> worst failure a data structure has.
>
> So in practice I would write `@dataclass(frozen=True)` and list the fields. That generates both
> methods and makes the second rule unbreakable, because assignment raises `FrozenInstanceError`
> instead of quietly corrupting the table. For a small pair like a coordinate I would use a
> `NamedTuple`, which is hashable and immutable for free and is slightly faster because tuple hashing
> is in C.
>
> And one thing I would flag: a plain `@dataclass` is unhashable, because the generated `__eq__`
> causes Python to set `__hash__` to `None`. There is an `unsafe_hash=True` option that makes the
> error go away, and I would avoid it — it re-enables exactly the mutation bug, and the keyword is
> named 'unsafe' on purpose."

---

## 9. Recall card

- **The default is identity, not value.** No `__eq__`/`__hash__` means Python compares memory
  addresses, so `len({Order("A-1"), Order("A-1")}) == 2`. That one sentence is the whole interview
  question.
- **Two rules. `a == b` ⇒ `hash(a) == hash(b)`, and the hash must not change while the object is a
  key.** The converse of rule 1 is *not* required — unequal objects sharing a hash is a collision,
  which costs time, never correctness.
- **Breaking rule 2 is silent.** Mutate a key in place and `x in d` is `False` while `len(d)` is 1
  and iteration still yields it. No exception, ever. `@dataclass(frozen=True)` makes it impossible —
  `FrozenInstanceError` at the moment of the mistake instead of a wrong answer later.
- **Defining `__eq__` sets `__hash__ = None`,** so a plain `@dataclass` raises `TypeError:
  unhashable type`. Fixes: `frozen=True` (the default choice) · `NamedTuple` (free, and faster —
  tuple hashing is C) · `eq=False` to keep identity · `unsafe_hash=True` **never**, it just
  re-enables the bug.
- **Hash the identity fields, cheaply.** `__hash__` runs on *every* lookup: a 100 KB field is 8 µs
  per operation; `tuple(self.items)` on a 10,000-list is 200 µs. And a too-coarse hash (customer
  instead of order id) gives 200-long chains — 200× slower with no error. Combine fields with
  `hash((a, b))`, and always guard `__eq__` with `isinstance` returning `NotImplemented`.
