---
day: 65
track: practice
title: "Practice — Hashing your own objects"
status: written
---

# Day 065 · Practice

**DSA topic:** Hashing your own objects
**System design topic:** Factory and abstract factory

---

## Code these, in this order

One rule for the whole set: **before writing `__eq__`, say out loud which fields make two of these
the same thing.** That sentence is the design decision. `__hash__` is then obliged to agree with it,
and the code writes itself.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Number of Boomerangs | LeetCode 447 (Medium) | A tuple as a key, and noticing that the natural key is a distance rather than a point. |
| 2 | Max Points on a Line | LeetCode 149 (Hard) | Designing a key for "same line" — the reduced-fraction slope, and why floats are the wrong key. |
| 3 | Insert Delete GetRandom O(1) | LeetCode 380 (Medium) | Objects as keys with a positional value, and deletion done right. |
| 4 | Design a HashMap keyed on your own class | Write it yourself | Rule 1 and rule 2 by hand: your table must call `__hash__` and then `__eq__`. |

### On problem 2, resist the float

The obvious key for a line's slope is `(y2 - y1) / (x2 - x1)`. That is a float, and two lines that
are mathematically the same can produce two different floats. Use the reduced fraction — divide both
differences by their GCD and normalise the sign — and say out loud why a tuple of two integers is a
safe key and a float is not.

### On problem 4, break both rules on purpose

Write a small open-addressed table that stores your own objects. Then:

1. Insert an object, mutate the field its hash uses, and try to find it. Confirm nothing raises.
2. Write an `__eq__` that ignores a field `__hash__` uses. Confirm it still works, and say why.
3. Write a `__hash__` that ignores a field `__eq__` uses. Find the input that loses an entry.

Number 3 is the only one of the three that is a real violation. Say which rule, and in which
direction.

### The identity-versus-value drill

For each, predict `len(...)` before you run it, then run it:

1. `{Order("A-1"), Order("A-1")}` with no `__eq__` or `__hash__`.
2. The same, with `__eq__` only.
3. The same, with both.
4. `{Point(1, 2), Point(1, 2)}` with `@dataclass`.
5. The same with `@dataclass(frozen=True)`.
6. The same with `@dataclass(eq=False)`.
7. `{Cell(0, 0), Cell(0, 0)}` with `NamedTuple`.

Two of those seven raise rather than returning a number. Name them and quote the exact error.

### The contract drill

For each pair of methods, say whether it is legal, and if not, which rule it breaks and what goes
wrong:

1. `__eq__` on `id`; `__hash__` on `id`.
2. `__eq__` on `id`; `__hash__` on `(id, customer)`.
3. `__eq__` on `(id, customer)`; `__hash__` on `id`.
4. `__eq__` on `id`; `__hash__` returning `1` always.
5. `__eq__` on `id`; `__hash__` returning `id(self)`.
6. `__eq__` defined; `__hash__` not defined.

Two of the six are legal but slow. Say how slow, with a number, for 100,000 objects.

### The silent-failure drill

Reproduce this exactly, and write down every line of output:

1. Put an object in a dictionary as a key.
2. Mutate the field its `__hash__` uses.
3. Print `key in lookup`.
4. Print `len(lookup)`.
5. Print `list(lookup)`.
6. Print `lookup.get(key)`.
7. Try to `del lookup[key]`.

Then say, in one sentence, why this is worse than an exception, and what single change makes it
impossible.

### The frozen drill

1. Make a `@dataclass(frozen=True)` and try to assign to a field. Quote the exact error.
2. Put a mutable list inside a frozen dataclass and mutate the list. Does it raise? Is the object
   still findable? Explain.
3. Change the list field to a `tuple` and repeat.
4. Say what `frozen=True` actually guarantees and what it does not.

Step 2 is the one people are surprised by. Say precisely what frozen means.

### The cost drill

Time 100,000 dictionary lookups where `__hash__` is each of the following:

1. `hash(self.order_id)` — a 10-character string.
2. `hash((self.a, self.b, self.c))`.
3. `hash(self.description)` — a 100 KB string.
4. `hash(tuple(self.items))` — a 10,000-element list.
5. `return 1`.

Then, for number 5, build a dictionary of 20,000 such objects and time that. Compute the number of
comparisons and name the complexity.

### The factory-distinction drill

For each, say which of the three it is — simple factory, factory method, or abstract factory — and
give the reason in one sentence:

1. `logging.getLogger("app.orders")`
2. `sqlalchemy.create_engine("postgresql://...")`
3. A `Dialog` base class whose subclasses override `create_button()`.
4. A `UiFactory` with `create_button`, `create_checkbox` and `create_menu`.
5. `datetime.fromisoformat("2026-08-31")`
6. `boto3.session.client("s3")`
7. A `TestInfrastructure` object handing out an in-memory database, an in-memory object store and a
   fake payment client.
8. `Calendar.getInstance()`

One of the eight is not really a factory at all in the sense we mean. Which, and why is its name
misleading?

### The build-it drill

Take this code and refactor it:

```python
# orders/checkout.py
if user.prefers_sms:
    sender = SmsSender(api_key=settings.TWILIO_KEY)
else:
    sender = EmailSender(host=settings.SMTP_HOST)
sender.send(message)
```

1. Count how many other files would contain this same branch in a real system.
2. Write the `Sender` protocol.
3. Write the registry factory. Count its lines.
4. Add a fourth channel. Count the files you edited.
5. Convert it to a decorator registry. Add a fifth channel. Count again.
6. Run `grep -rn "twilio" orders/` before and after, and say what the result proves.
7. Name the cost you just accepted, and the two ways to mitigate it.

### The abstract-factory grid drill

You have four families (Windows, Mac, Linux, Web) and three product types (button, checkbox, menu).

1. How many product classes exist?
2. Add a fifth family. How many files added, how many edited?
3. Add a fourth product type. How many files added, how many edited?
4. State the asymmetry in one sentence.
5. Give one real situation where the asymmetry is acceptable, and one where it is not.
6. Name a family from your own experience where mixing members would be a genuine bug.

### The do-not-build-it drill

For each, say whether you would write a factory, and give the deciding question:

1. One implementation, no test double, trivial constructor.
2. One implementation, but the constructor needs three secrets from config.
3. Three implementations chosen by a value from the database.
4. Three tax rates that differ only by a number.
5. Two implementations, one of which exists only for tests.
6. A class that will be swapped when the vendor contract expires next year.

Two of the six are "no" for the same reason and two are "yes" for the same reason. Name both reasons.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Why did putting this object in a set not deduplicate it?*
   Identity versus value, the two rules of the contract with the one-directionality of rule 1, which
   fields you would choose and why, and `frozen=True` volunteered as the way to make rule 2
   unbreakable.

2. *How do you create the right notification object for each channel?*
   The three meanings of "factory" separated in the first sentence, the pain named with a number of
   call sites, the registry written, the three things that moved out of the business logic, and the
   run-time-typo cost accepted with its mitigation.

3. *What happens if I mutate a key while it is in a dictionary?*
   The object stays in its old bucket, lookups compute a new one, `in` is False while `len` counts it
   and iteration yields it, no exception at all — and the one-word fix.

---

## Before you move on

- [ ] I watched `len({Order("A-1"), Order("A-1")})` print 2 before I fixed anything.
- [ ] I triggered `TypeError: unhashable type` from `__eq__` alone and from a plain `@dataclass`.
- [ ] I can state both rules of the contract and say which direction rule 1 does *not* go.
- [ ] I mutated a key in place and confirmed `in` is False while `len` is 1 and no error is raised.
- [ ] I know what `frozen=True` guarantees, and what it does not guarantee about a list field.
- [ ] I measured the cost of a `__hash__` that builds a tuple from a 10,000-element list.
- [ ] I can separate simple factory, factory method and abstract factory in one sentence each.
- [ ] I wrote the registry factory and can say the three things it moved out of the business logic.
- [ ] I can state the abstract-factory row/column asymmetry with numbers.
- [ ] I can name two situations where I would deliberately not write a factory.
- [ ] I answered all three questions above out loud.
