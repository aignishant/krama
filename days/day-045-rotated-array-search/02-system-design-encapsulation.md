---
day: 45
track: system-design
title: "Encapsulation"
phase: "Object-oriented design"
status: written
---

# Day 045 · System design — Encapsulation

**After today you can:** You can say why public fields are a design bug, with a concrete failure.

**The interviewer asks it as:** *Why make a field private if you are going to add a getter anyway?*

---

## 1. What this is, and why they ask it

**Encapsulation** means an object keeps its own data to itself and lets the outside world act on it
only through methods it chose to offer. The data is not hidden to be mysterious. It is hidden so that
every change to it passes through code the object controls, which means the object can guarantee
something is always true about itself — and no caller, anywhere, can break that guarantee.

They ask it with the getter question because that question is a trap, and it is asked on purpose. The
weak answer is "so you can add validation later" or "it's good practice", both of which suggest the
candidate has learnt a rule without the reason. The strong answer is that a getter is usually a
failure too, and the real goal is that the object should be asked to *do* things rather than asked
for its internals. Encapsulation is also the load-bearing idea under every remaining day of this
phase: inheritance, polymorphism and composition are all ways of arranging encapsulated things, and
none of them help if every object's insides are public.

---

## 2. The story

Vinod's medical shop is on the corner opposite the bus stop, and it opens at half past eight.

It is a small place. There is a glass counter at the front with the everyday things behind it —
paracetamol, bandage rolls, a basket of throat lozenges — and behind that, four wooden shelves going
up to the ceiling, packed tight, floor to top.

You cannot go behind the counter. Nobody can. There is a wooden flap at one end that lifts, and in
nineteen years Vinod has lifted it for exactly two people: his brother, and the man who comes to
service the cold cabinet.

Customers have asked. A schoolteacher who comes every month once told him, quite kindly, that it
would be faster if she just went and got her own. And she was right, on that particular afternoon, in
that particular way. Vinod said no anyway, and he could not really explain why at the time.

He can now, because he has watched what happens when the rule slips.

The shelves are not arranged in any way a customer could work out. They are arranged the way he
remembers them, which is partly by kind, partly by how fast they move, and partly by where a box
happens to fit. He can put his hand on any of six hundred things without looking. One person putting
one strip back on the wrong shelf costs him twenty minutes, three days later, with a queue at the
counter.

The cold cabinet is worse. Some things must stay cold, and they do not say so on the front of the
box in a way that means anything to somebody who does not already know. He has had a boy hand him a
box off the wrong shelf that had been sitting out since morning, and the only honest thing to do with
it was throw it away.

And then there is the thing that matters most, which is that some medicines he will not hand over
without seeing the doctor's slip. If people take their own, that check does not happen. It does not
happen *sometimes*, and it does not happen *usually* — it simply stops existing, because the counter
was the only place it ever happened.

So there is one way in and it is him. Tell him what you need. He will get it, check what needs
checking, and put it in your hand.

---

## 3. The idea in plain English

Vinod's shelves are the object's data. The counter is its public interface. The prescription check is
an **invariant** — a rule about the object that must always hold — and the reason the flap stays down
is that an invariant enforced in one place is enforced, and an invariant enforced at every call site
is enforced nowhere.

### The invariant is the point

Start with the rule, not with the keyword. Take a bank account:

> **The balance is never negative.**

That sentence is the invariant. Now compare two designs.

```python
# Public data. The rule lives at every call site.
class Account:
    def __init__(self, balance: int) -> None:
        self.balance = balance

# somewhere in the withdrawal screen
if account.balance >= amount:
    account.balance -= amount
```

```python
# Encapsulated. The rule lives in one place, and there is no way round it.
class Account:
    def __init__(self, balance: int) -> None:
        self._balance = balance

    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
```

The first version is not wrong today. It is wrong in eight months, when the third call site — a batch
job, a refund path, an admin tool — writes `account.balance -= amount` without the check, and the
balance goes negative in production. There is no way to prevent that, because the field is public and
Python will happily assign to it.

The second version has one door. You cannot make a negative balance through it. That is the whole of
encapsulation, and everything else is mechanics.

### Why a getter is usually still a failure

Now the interviewer's question. Suppose you make the field private and add a getter:

```python
class Account:
    def get_balance(self) -> int:
        return self._balance
```

Have you gained anything? A little: reads are now channelled, so you could log them, or compute the
value instead of storing it. But if the caller then writes

```python
if account.get_balance() >= amount:
    account.set_balance(account.get_balance() - amount)
```

you have rebuilt the public field with extra typing. The rule is back at the call site. The getter
plus setter pair is public data wearing a coat.

The real answer to the question is: **do not add the getter — add the behaviour.** The caller does
not want the balance. The caller wants to withdraw money. `account.withdraw(amount)` puts the
decision inside the object, where the rule lives.

That principle has a name worth knowing: **Tell, Don't Ask.** Tell the object to do something; do not
ask it for its data so you can decide on its behalf. In an interview, saying "I'd rather expose
`withdraw` than `balance`, because the rule about withdrawing belongs to the account" answers the
getter question completely.

Getters are still legitimate when the value is genuinely something the outside world needs to *see* —
a balance printed on a statement, an order's total on a receipt. The test is whether the caller is
going to read the value and then make a decision the object should have made.

### How Python actually does it

Python has no `private` keyword. It has conventions and one mechanism.

```python
class Account:
    def __init__(self) -> None:
        self.balance = 0        # public: part of the promise
        self._ledger = []       # single underscore: internal, do not touch
        self.__key = "abc"      # double underscore: name-mangled to _Account__key
```

- **One underscore** is a convention. It means "this is not part of the interface; if you use it and
  it changes, that is on you". Nothing enforces it. Every linter and every reviewer respects it.
- **Two underscores** triggers **name mangling**: inside the class the attribute is rewritten as
  `_Account__key`, so a subclass defining its own `__key` does not collide. It is not a security
  feature — `obj._Account__key` still works — and it is meant for avoiding accidental clashes in
  inheritance, not for privacy.

Python's own phrase for this is that we are all consenting adults. The convention is the fence; the
language does not build a wall. In Java or C++ `private` is enforced by the compiler, which is why
the same design intent looks stronger there. **The intent is identical in both languages, and the
intent is what the interview is about.**

### Properties: changing your mind without changing callers

Sometimes you genuinely want an attribute-looking read, with control behind it:

```python
class Account:
    @property
    def balance(self) -> int:
        return self._balance          # callers write account.balance, and cannot assign
```

With no setter defined, `account.balance = 500` raises `AttributeError`. So reads look natural and
writes are impossible, which is often exactly the shape you want. Properties also let you start with
a stored field and later replace it with a computation — `total` as a stored number today, a sum over
line items tomorrow — without a single caller changing.

### The leak nobody notices: handing out your insides

This is the mistake that survives all the underscores:

```python
class Order:
    def __init__(self) -> None:
        self._items: list[str] = []

    def get_items(self) -> list[str]:
        return self._items            # <-- hands out the real list
```

```python
order.get_items().append("free laptop")     # no method was called on Order at all
```

The list is a **reference**, not a copy. Returning it hands the caller the object's internals with
full write access, and every rule `Order` might have about items — a maximum count, a price recalc —
is bypassed silently. There was never a moment to check anything.

Three fixes, cheapest first:

```python
    def items(self) -> tuple[str, ...]:
        return tuple(self._items)         # a copy, and immutable

    def items(self) -> Iterator[str]:
        return iter(self._items)          # read-only walk, no copy

    def add_item(self, item: str) -> None:
        if len(self._items) >= 20:
            raise ValueError("cart is full")
        self._items.append(item)          # better still: no getter, just the behaviour
```

The same trap applies to dictionaries, sets, dates in mutable form, and any object you return that
the caller can mutate. **Returning a mutable internal is the same as making the field public**, and
it is worth saying that sentence in an interview because most candidates only think about the
attribute.

---

## 4. The picture

The shop, and the object, side by side:

```
        THE SHOP                              THE OBJECT

   +----------------------+            +--------------------------+
   |  shelves, cold       |            |  _balance                |
   |  cabinet, six        |  private   |  _ledger                 |
   |  hundred boxes       |            |  _overdraft_limit        |
   +----------------------+            +--------------------------+
   ========= counter =======           ======= public methods =====
   | ask for what you need |            | deposit(amount)          |
   | he checks the slip    |  public    | withdraw(amount)         |
   | he hands it over      |            | balance  (read-only)     |
   +----------------------+            +--------------------------+
            ^                                       ^
        customers                              calling code

   the flap stays down       <->        no public attribute, no setter,
                                        no mutable internal handed out
```

**What to notice:** the counter is narrow on purpose. Every rule the shop has — the cold chain, the
prescription, the arrangement of the shelves — is enforceable only because there is exactly one way
in.

Where the leak happens, drawn:

```
   caller                       Order object
     |                        +------------------+
     | get_items()            |  _items -------> [ "rice", "dal" ]   (one list, in memory)
     |----------------------->|                  |
     |<-----------------------|  returns the SAME reference
     |   .append("laptop")    |
     |------------------------------------------> [ "rice", "dal", "laptop" ]
                                                    ^
                              Order never ran a single line of its own code
```

**What to notice:** no method on `Order` was called during the mutation. Every check `Order` owns was
skipped, and nothing anywhere reports an error. The underscore on `_items` did not help at all,
because the reference escaped.

---

## 5. How it actually works

### What the language gives you, and what it does not

```
Java / C++     private, protected, public enforced at compile time.
               Reflection can still break it, deliberately and visibly.

Python         no enforcement. _name is a convention; __name is mangled to
               _Class__name to avoid subclass collisions, not to hide.
               @property gives a read that looks like an attribute.
               __slots__ prevents new attributes being added from outside.

JavaScript     #field is genuinely private since ES2022, enforced at runtime.
```

The design intent is identical everywhere. Only the enforcement differs, and interviewers are testing
the intent, so "Python doesn't have private" is never an answer — it is at most half a sentence
before you say what you do instead.

### The products you already use

- **Python's `datetime.date`** exposes `.year`, `.month` and `.day` as read-only properties, and the
  object is immutable. You cannot construct 30 February through any door, because the only door is
  the constructor and it validates. That is encapsulation used to make an invalid object
  unrepresentable.
- **`collections.Counter`** and `dict` keep their hash table entirely internal. You can never corrupt
  the bucket array from outside, which is why the O(1) guarantee from
  [day 021](../day-021-frequency-maps/README.md) is a guarantee and not a hope.
- **Java's `ArrayList`** keeps `size` and the backing array private. Making `size` public would let
  any caller set it to 100 on a list of three elements, and the next `get` reads uninitialised
  memory. The class's entire correctness rests on nobody being able to do that.
- **`java.lang.String` and Python's `str`** are immutable, which is encapsulation taken to its
  limit — you met the consequences on [day 019](../day-019-what-a-string-is/README.md). An immutable
  object needs no defensive copies, is safe to share between threads, and can be safely hashed.
- **Stripe's SDK** does not let you assign `intent.status = "succeeded"`. Status changes only through
  operations the server authorised, because a client that can write the field can lie about payment.

### Designing the interface: the order to do it in

1. **Write the invariants first, as sentences.** "The balance is never negative." "A spot holds at
   most one vehicle." "The total equals the sum of the lines." Two or three per class.
2. **For each invariant, name every operation that could break it.** Those operations become methods.
3. **Make everything else private.** Not "make everything private then add getters" — start closed,
   and open only what an operation needs.
4. **Check what you return.** Any mutable object handed out is a hole. Copy it, wrap it, or replace
   the getter with behaviour.
5. **Re-read the method list and ask: could a caller assemble a broken object out of these?** If yes,
   an operation is missing a check or an operation should not exist.

### What "breaking encapsulation" looks like in a real codebase

```python
if order.status == "PENDING" and order.items and order.customer.tier == "GOLD":
    order.status = "PRIORITY"
```

Three objects' internals read, one written, and the rule about what makes an order priority now lives
in a screen. Find that same rule written slightly differently in two other files and you have the
classic bug where an order is priority on one page and not on another. The fix is a method —
`order.promote_if_eligible(customer)` — and the reason to say it out loud in an interview is that
this is what the failure actually looks like in production. Not a security breach. A quiet
disagreement between two files.

---

## 6. The numbers

### The invariant, counted in call sites

```
"balance never negative", enforced at the call site:
    withdrawal screen        1
    ATM path                 1
    scheduled standing order 1
    admin refund tool        1
    the data-fix script      1  (the one nobody remembers)
                            ---
                             5 copies of one rule

after one year and two new features:      7-9 copies
probability all of them are correct:      the product of each being right

the same rule inside Account.withdraw():  1. Always 1, whatever ships next year.
```

### What encapsulation costs at runtime

```
direct attribute read      obj.x            ~20-30 ns
property read              obj.x  (@property) ~90-150 ns   -- roughly 4x
method call                obj.get_x()      ~60-80 ns

a request that does 1,000 property reads:  ~0.1 ms
the same request's single database round trip: ~1 ms

so the entire encapsulation overhead is ~10% of ONE query.
```

The conclusion to say out loud: **the cost is real, it is nanoseconds, and it is dominated by the
first input/output call in the request.** Optimise round trips, not property access.

### Defensive copying, priced

```
returning tuple(self._items) on a 20-item list:   ~400 ns, 20 pointer copies
returning iter(self._items):                       ~50 ns, no copy at all
returning self._items:                              ~0 ns, and a hole in the class

a cart page rendering 50 orders x 20 items:
    copies:  50 x 400 ns = 20 microseconds
```

Twenty microseconds against a page budget of 200 milliseconds. The copy is free in any sense that
matters. The exception, and it is a real one: copying a list of a million elements on every access
inside a loop is `O(n)` per call — there, return an iterator or expose the behaviour instead.

### `__slots__`, from [day 044](../day-044-first-and-last-occurrence/README.md)

```
__slots__ = ("_balance", "_ledger")
    - removes the per-instance dict:  ~184 bytes -> ~64 bytes
    - AND blocks obj.blance = 100 (the typo) with an AttributeError
```

The second effect is the encapsulation one and it is underrated: without `__slots__`, a typo in an
assignment silently creates a new attribute and the real one never changes.

---

## 7. The trade-offs

### Hiding against convenience

Every private field is one thing callers cannot do without asking you to add a method. On a small
script that is friction with no payoff. *I would not encapsulate a throwaway data-holder that crosses
one boundary and dies* — a parsed row on its way into a list is fine as a dataclass with public
fields, or as a `NamedTuple` where immutability does the job for free.

### Immutability against churn

A frozen object cannot be corrupted, needs no defensive copies and is safe to hash and share. It also
means every change allocates. *I would freeze value objects — `Money`, `DateRange`, `Coordinate` —
and leave entities mutable*, exactly as [day 044](../day-044-first-and-last-occurrence/README.md) put
it. Freezing an `Order` that changes state ten times in its life turns every transition into a new
object and a new identity, which is worse, not safer.

### Encapsulation against frameworks that want your fields

ORMs, serialisers and dataclass-to-JSON converters all want to read every attribute, and most reach
past the underscore to do it. *I would not fight the framework at the boundary* — I would keep the
rich, encapsulated object in the domain layer and convert to a plain dictionary or a schema object at
the edge, so that the framework sees a flat structure and the rules stay in one place. That
conversion layer is annoying and it is the price of having rules at all.

### Getters against behaviour

*I would not add a getter for a value the caller is only going to use to make a decision about my
object.* That decision belongs to me. I would add a getter for a value the caller genuinely needs to
display, report, or hand to something else. The test is the next line of the caller's code: if it is
an `if`, the getter is wrong and a method is missing.

### The honest sentence

> Encapsulation is not about stopping malicious code. It is about making sure that in two years,
> when someone adds the seventh way to withdraw money, the rule about not going negative is somewhere
> they cannot avoid.

---

## 8. In the interview

### How it gets asked

- *"Why make a field private if you're going to add a getter anyway?"* — the trap, and the answer is
  that the getter is often also a mistake.
- *"What's wrong with this class?"* — shown a class with public fields, and expected to name the
  invariant that nothing protects.
- *"Where do you put the validation?"* — inside a larger design round. The answer is "on the object
  that owns the data being validated", and then you point at the method.
- *"Python doesn't have private. So does encapsulation matter here?"* — a genuine question that
  sounds like a gotcha, and the answer is about intent and conventions, plus `@property` and the
  returned-reference trap.

### What to say out loud, in the first ninety seconds

1. **Lead with the invariant, not the keyword.** *"The rule here is that the balance is never
   negative. Encapsulation is how I make that rule impossible to break rather than merely
   documented."*
2. **Name the failure concretely.** *"With a public field, the rule has to be repeated at every call
   site. Right now there are three; in a year there are seven, and the one somebody forgets is the
   one that ships."*
3. **Answer the getter trap directly.** *"A getter alone doesn't fix it — `get` then `set` is a
   public field with extra typing. What I actually want is `withdraw(amount)`, so the decision
   happens inside the object. Tell, don't ask."*
4. **Mention the leak.** *"And I'd check what the class returns. Handing back the internal list means
   a caller can append to it without any of my code running — that's a public field by another
   route."*
5. **Say what Python gives you.** *"Python won't enforce it: underscore is a convention, double
   underscore is name mangling for inheritance, and `@property` gives a read-only attribute-shaped
   access. The intent is the same as `private` in Java; only the enforcement differs."*

### The follow-ups

**"Give me a concrete bug that a public field causes and a private one prevents."**
A cart with a maximum of twenty items. With `cart.items` public, the checkout page appends through
the object's own `add_item` and the limit is respected — but the bulk-reorder feature, written a year
later by someone else, does `cart.items.extend(previous_order.items)` because it is one line and it
works. Now a cart holds sixty items, the packing system that assumed twenty overflows its label
layout, and the failure surfaces three systems downstream with nothing in the logs pointing back at
the cart. There is no exception at the moment the rule breaks, which is what makes it expensive: the
bug and its symptom are in different services. With the list private and only `add_item` exposed, the
bulk path has to call the same method twenty times and gets a clear `ValueError` on the twenty-first,
at the right place, in the right stack trace. What I want to draw out is that the value of
encapsulation is not that it prevents the write — it is that it moves the error to where somebody can
understand it.

**"You made the list private, but you still return it from `get_items`. Is that safe?"**
No, and this is the mistake that survives the underscore. Returning `self._items` hands the caller
the same list object my class is holding, so `order.get_items().append(...)` mutates my state
directly, without a single line of my code running. Underscore is a naming convention, not a barrier
around the object it names. There are three fixes and they trade off differently. Returning
`tuple(self._items)` gives an immutable snapshot and costs a copy — about four hundred nanoseconds on
twenty items, which is nothing, but is O(n) if the collection is large and the call is in a loop.
Returning `iter(self._items)` gives a read-only walk with no copy, and is the right choice for large
collections, though the caller can still be surprised if the underlying list changes mid-iteration.
And the best option is usually to delete the getter — if the caller only wants a count, expose
`item_count`; if they want to add, expose `add_item`. The general rule I'd state: any mutable object
you return is part of your public interface, whether you meant it to be or not. That applies to
lists, dicts, sets, and any of your own entities you hand out.

**"Python has no `private`. Doesn't that make all of this decoration?"**
No, and there are two separate reasons. The first is that enforcement was never the point.
Encapsulation is a statement about where a rule lives, and a rule that lives in one method is
enforced by the fact that all the sensible paths go through that method — the compiler was only ever
a reminder. In practice, a leading underscore is respected by every reviewer, every linter, and every
IDE's autocomplete, which is most of the value. The second reason is that Python does give you real
tools, they are just different ones. `@property` with no setter makes assignment raise
`AttributeError` at runtime, which is genuine enforcement. `@dataclass(frozen=True)` makes an object
immutable, so the invariant holds by construction and no defensive copy is ever needed. `__slots__`
blocks new attributes being created from outside, which catches the typo case. And double-underscore
name mangling exists for a narrower purpose that is worth being accurate about — it prevents a
subclass accidentally colliding with a base class's attribute, which matters from
[tomorrow](../day-046-binary-search-on-the-answer/README.md) when inheritance arrives. What I would
never say in an interview is "Python doesn't have private, so I use public fields" — the design
intent is language-independent, and that is what is being scored.

### A model answer

> "Let me answer that with the rule rather than the keyword, because the keyword is the part that
> doesn't matter.
>
> Say the rule is: an account balance is never negative. If `balance` is public, that rule has to be
> written at every place that takes money out. Today that's the withdrawal screen. In a year it's the
> withdrawal screen, the standing-order job, the refund tool and a data-fix script — and the one
> somebody forgets is the one that puts a negative balance in production, with no error at the moment
> it happens.
>
> So I make the field private and expose `withdraw(amount)`, which checks and then subtracts. Now
> there is exactly one door and the rule is behind it, and there is no way to write a negative
> balance through the interface at all.
>
> On your actual question — the getter doesn't buy me that. If I expose `get_balance` and
> `set_balance`, the caller writes `if get_balance() >= amount: set_balance(get_balance() - amount)`
> and the rule is back at the call site. That's a public field with more typing. What I want is not a
> getter at all: I want the behaviour. Tell the object to withdraw; don't ask it for its balance and
> decide on its behalf.
>
> I'd still expose a read-only `balance` if something genuinely needs to display it — a statement, a
> receipt. In Python that's `@property` with no setter, so `account.balance` reads naturally and
> `account.balance = 500` raises `AttributeError`. The test I apply is: what's the caller's next
> line? If it's an `if`, the getter is wrong and a method is missing.
>
> The other thing I'd check is what the class hands out. If `get_items` returns the internal list, a
> caller can append to it and none of my code runs — the underscore didn't protect the object, only
> the name. So I'd return a tuple, or an iterator for a large collection, or better, expose
> `add_item` and delete the getter.
>
> And the cost of all this is nanoseconds. A property read is maybe four times a direct attribute
> read, which is about a hundred nanoseconds, against a millisecond for one database round trip. It's
> not a performance conversation."

---

## 9. Recall card

- **Start from the invariant, not the keyword:** "balance never negative", "a spot holds one
  vehicle". Encapsulation makes the rule *impossible to break* instead of merely documented.
- **The failure is call-site multiplication.** One rule at 5-9 call sites, and the forgotten one
  ships. Inside one method it is 1 place, forever — and the error lands where somebody can read it.
- **The getter answer: don't add the getter, add the behaviour.** `get`+`set` is a public field with
  more typing. Tell, Don't Ask. A getter is fine only when the caller *displays* the value — if their
  next line is an `if`, a method is missing.
- **Returning a mutable internal is a public field by another route.** `get_items().append(...)` runs
  none of your code. Return a tuple, an iterator, or nothing at all.
- **Python: `_` is convention, `__` is name mangling for subclass collisions, `@property` without a
  setter is real enforcement, `frozen=True` and `__slots__` help.** The intent is identical to Java's
  `private`; only the enforcement differs, and intent is what is scored.
