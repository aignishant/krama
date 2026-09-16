---
day: 8
track: lang-python
title: "class, __init__, methods, and dataclasses"
theme: "Modelling a thing"
phase: "Languages: every language, every basic"
status: written
---

# Day 008 · Python — class, __init__, methods, and dataclasses

**Today's theme:** Modelling a thing

**After today you can:** You can model a bank account in each language with data and behaviour together, and say what is public.

**The interviewer asks it as:** *What is the difference between a struct and a class?*

---

## 1. What this is, and why it matters

A class is a blueprint for a thing that has some data and some actions that belong with that data: an account has a holder and a balance, and it can be deposited into and withdrawn from. In Python you write the blueprint with `class`, set up each new thing in `__init__`, and write the actions as methods whose first parameter, `self`, is the thing itself. Python has no real "private": everything is reachable, and a leading underscore is a polite request not to touch.

At work, almost every named thing in a codebase is a class: a user, an order, a connection, a request. Interviewers ask "what is `self`", "what is the difference between a class attribute and an instance attribute", and "what does `@dataclass` give you", and, from the heading, "what is the difference between a struct and a class", which in Python has the answer "there is no struct, and here is how a class plays both parts".

## 2. The story

Sunita runs a tiffin service from her kitchen. Forty customers, one hot lunch each, delivered by eleven. She used to keep everything in her head. At forty it stopped fitting.

So she sat down one Sunday and worked out what she actually needs to know about each customer. A name. A delivery address. How much money they have paid in advance. That is it. Every customer is those three things, and nothing else about them matters to the business.

Then she worked out what happens to a customer. They top up, usually five hundred or a thousand at a time, and the balance goes up. Every day a tiffin goes out, and the balance goes down by eighty. If a balance would go below zero, the tiffin does not go out; she sends a message instead. And once a month she tells each customer their balance.

Those are the only four things that ever happen. Top up, deduct a tiffin, refuse if there is not enough, and report. Nobody ever does anything else to a customer's account. Sunita wrote the four things on a note in her phone and has not changed the note in two years.

Here is the part that took her longest to decide. Her customers can ask their balance any time, and she tells them straight away. But they cannot change it. Not even the ones she has known for ten years. Mr Rao once asked her to just write down a thousand and he would pay her on Friday. She said no. The number changes when money arrives or a tiffin leaves, and by no other route, ever. That rule is what makes the number trustworthy. If anyone could reach in and change it, she would have to check it every time she read it.

When a new customer joins, Sunita does the same three things every time: gets the name, gets the address, takes the first payment. Nobody starts without all three. A customer with no address is not a customer yet.

And when she describes a customer to her daughter, she says it the same way every time: "Rao, Flat 4B, four hundred and twenty left." Name, address, balance. The description is part of the thing.

## 3. The idea in plain English

A **class** is a blueprint: it says what data every thing of this kind has and what actions it supports. `class Account:` starts one. Each thing made from the blueprint is an **object** or an **instance**: Mr Rao's account is one instance, Mrs Iyer's is another, and both were made from the same class.

The data lives in **attributes**, names attached to each instance: `holder`, `address`, `balance`. The actions are **methods**, functions defined inside the class. A method's first parameter is always `self`, which is the instance the method was called on. When you write `rao.deposit(500)`, Python calls `deposit(rao, 500)`; `self` is `rao`. That is how `deposit` knows which balance to change.

`__init__` is the method that runs when a new instance is made. It is Sunita's three steps for a new customer: it takes the name, the address and the opening amount, and stores each one on `self`. `Account("Rao", "Flat 4B", 500)` calls `__init__` with those values and hands back the finished instance. Names with double underscores on both sides are called **dunder** methods and Python calls them for you at particular moments.

`__repr__` is another dunder: it returns the text Python shows when you print the instance. "Rao, Flat 4B, four hundred and twenty left." Without it, printing an account shows `<__main__.Account object at 0x7f...>`, which tells you nothing.

Now, what is **public**. In Python, everything is. Any code can read or write `rao.balance`. The convention is that a name starting with one underscore, `_balance`, is **internal**: you may see it, but touching it from outside is your fault when it breaks. To give customers a way to read the balance without a way to write it, you add a **property**, a method decorated with `@property` that is read like an attribute: `rao.balance` calls it, and `rao.balance = 1000` fails. That is Sunita saying no to Mr Rao.

A **dataclass** is a shortcut for classes that are mostly data. Put `@dataclass` above the class, list the attributes with type hints, and Python writes `__init__`, `__repr__` and `==` for you. When there are no rules to enforce, a dataclass is the right amount of code.

## 4. The picture

```
 class Account          the blueprint, written once

   __init__(self, holder, address, opening)    the three steps for a new customer
   deposit(self, amount)
   charge_tiffin(self)  → True or False
   balance  (property, read-only)
   __repr__(self)

 rao = Account("Rao", "Flat 4B", 500)          one instance
 ┌──────────────────────────────┐
 │ holder    "Rao"              │
 │ address   "Flat 4B"          │
 │ _balance  500                │  ◄── internal; read through .balance, never written directly
 └──────────────────────────────┘

 iyer = Account("Iyer", "Flat 2A", 1000)       another instance, same blueprint
 ┌──────────────────────────────┐
 │ holder    "Iyer"             │
 │ address   "Flat 2A"          │
 │ _balance  1000               │
 └──────────────────────────────┘

 rao.deposit(500)   →   deposit(rao, 500)   →   rao._balance = 1000
```

*Notice that the methods are written once, in the class, and the data is separate per instance. Notice how `self` in `deposit` is whichever instance sat before the dot.*

## 5. The code, built step by step

Start `tiffin.py` in a `day08` folder. The blueprint and its `__init__`.

```python
class Account:
    def __init__(self, holder: str, address: str, opening: int) -> None:
        self.holder = holder
        self.address = address
        self._balance = opening
```

Four spaces in for the method, eight for its body. `self.holder = holder` attaches the value to this instance. `_balance` has the underscore because nothing outside the class should write it. `-> None` because `__init__` returns nothing; the instance is returned by the class call, not by `__init__`.

The actions.

```python
    def deposit(self, amount: int) -> None:
        self._balance += amount

    def charge_tiffin(self, price: int = 80) -> bool:
        if self._balance < price:
            return False
        self._balance -= price
        return True
```

`+=` adds to the existing value. `charge_tiffin` returns whether the tiffin went out. Both methods reach the balance through `self`, and nothing else in the program ever needs to.

The read-only view.

```python
    @property
    def balance(self) -> int:
        return self._balance

    def __repr__(self) -> str:
        return f"Account({self.holder!r}, {self.address!r}, balance={self._balance})"
```

`@property` sits on the line above the method and turns `account.balance` into a call to it, with no brackets. `!r` inside an f-string shows the value with its quotes, so the repr reads like the code that would make it.

Using it.

```python
rao = Account("Rao", "Flat 4B", 500)
rao.deposit(500)
print(rao)
print(rao.charge_tiffin(), rao.balance)
```

```
Account('Rao', 'Flat 4B', balance=1000)
True 920
```

And Sunita's rule, enforced.

```python
rao.balance = 5000
```

```
Traceback (most recent call last):
  File "/home/you/day08/tiffin.py", line 28, in <module>
    rao.balance = 5000
    ^^^^^^^^^^^
AttributeError: property 'balance' of 'Account' object has no setter
```

Readable, not writable. Note the honesty: `rao._balance = 5000` would still work. Python trusts you. The property makes the accidental case fail and leaves the deliberate case possible.

A dataclass, for the thing with no rules.

```python
from dataclasses import dataclass


@dataclass
class Delivery:
    holder: str
    address: str
    tiffins: int = 1


d = Delivery("Rao", "Flat 4B")
print(d)
print(d == Delivery("Rao", "Flat 4B", 1))
```

```
Delivery(holder='Rao', address='Flat 4B', tiffins=1)
True
```

No `__init__`, no `__repr__`, no `==` written by you; all three exist. A delivery is three values and no rules, so it is a dataclass. An account has a rule about who may change the balance, so it is a full class.

Here is the run and output for the complete program.

```bash
python3 tiffin.py
```

```
Account('Rao', 'Flat 4B', balance=1000)
tiffin sent: True, balance now 920
tiffin sent: True, balance now 840
Account('Iyer', 'Flat 2A', balance=60)
tiffin sent: False, balance now 60
cannot set balance directly: property 'balance' of 'Account' object has no setter
Delivery(holder='Rao', address='Flat 4B', tiffins=1)
same delivery? True
```

And the complete file.

```python
# tiffin.py — day 8, a class with data, behaviour, and one rule
# Run:  python3 tiffin.py
from dataclasses import dataclass


class Account:
    """One customer's prepaid balance. The balance changes only through deposit and charge."""

    def __init__(self, holder: str, address: str, opening: int) -> None:
        self.holder = holder
        self.address = address
        self._balance = opening

    def deposit(self, amount: int) -> None:
        self._balance += amount

    def charge_tiffin(self, price: int = 80) -> bool:
        if self._balance < price:
            return False
        self._balance -= price
        return True

    @property
    def balance(self) -> int:
        return self._balance

    def __repr__(self) -> str:
        return f"Account({self.holder!r}, {self.address!r}, balance={self._balance})"


@dataclass
class Delivery:
    """Three values and no rules, so a dataclass."""

    holder: str
    address: str
    tiffins: int = 1


rao = Account("Rao", "Flat 4B", 500)
rao.deposit(500)
print(rao)
for _ in range(2):
    print(f"tiffin sent: {rao.charge_tiffin()}, balance now {rao.balance}")

iyer = Account("Iyer", "Flat 2A", 60)
print(iyer)
print(f"tiffin sent: {iyer.charge_tiffin()}, balance now {iyer.balance}")

try:
    rao.balance = 5000
except AttributeError as error:
    print(f"cannot set balance directly: {error}")

d = Delivery("Rao", "Flat 4B")
print(d)
print(f"same delivery? {d == Delivery('Rao', 'Flat 4B', 1)}")
```

The `try`/`except` lines catch the failure so the program can continue and print it; day 9 is all about them. Today, read them as "attempt this, and if it fails, run this instead".

## 6. How the other two languages do it

Go, where the data is a struct, the methods are attached from outside, and public means a capital letter:

```go
type Account struct {
	Holder  string
	Address string
	balance int // lowercase: unreachable outside this package
}

func (a *Account) Deposit(amount int) { a.balance += amount }
func (a *Account) Balance() int      { return a.balance }
```

C++, where `class` and `struct` are the same thing with a different default, and `private:` is enforced by the compiler:

```cpp
class Account {
public:
    Account(std::string holder, std::string address, int opening);
    void deposit(int amount);
    int balance() const { return balance_; }
private:
    std::string holder_;
    std::string address_;
    int balance_;
};
```

The one line of difference that matters: **Python's privacy is a naming convention; Go's and C++'s are enforced by the compiler.** `rao._balance = 5000` runs in Python. `a.balance = 5000` from another package does not compile in Go, and `a.balance_ = 5000` from outside the class does not compile in C++. The second difference is where the methods live: Python and C++ write them inside the class body; Go writes them as separate functions with a receiver, and the struct itself is only data. That is Go's answer to "struct or class": the struct is the data, and the methods are a separate decision.

## 7. The traps

**The real error: forgetting `self`.** Write a method like a plain function.

```python
class Account:
    def deposit(amount: int) -> None:
        ...

rao.deposit(500)
```

```
Traceback (most recent call last):
  File "/home/you/day08/tiffin.py", line 5, in <module>
    rao.deposit(500)
TypeError: Account.deposit() takes 1 positional argument but 2 were given
```

Two arguments were given: `rao` and `500`. The method only declared room for one. Whenever you see "takes N positional arguments but N+1 were given" on a method, `self` is missing.

**The near-miss: the shared class attribute.** Put a list on the class instead of in `__init__`.

```python
class Account:
    history = []

    def __init__(self, holder: str) -> None:
        self.holder = holder

    def deposit(self, amount: int) -> None:
        self.history.append(amount)

rao = Account("Rao")
iyer = Account("Iyer")
rao.deposit(500)
print(iyer.history)
```

```
[500]
```

Mrs Iyer never deposited anything. `history` was created once, on the class, and every instance shares it, exactly like day 5's mutable default. Anything that belongs to one instance goes in `__init__` as `self.history = []`.

**The real error: a mutable default in a dataclass.** Python refuses the same mistake there.

```python
@dataclass
class Customer:
    holder: str
    orders: list[int] = []
```

```
ValueError: mutable default <class 'list'> for field orders is not allowed: use default_factory
```

The fix is `orders: list[int] = field(default_factory=list)`, with `field` imported from `dataclasses`. A dataclass catching this for you is a good reason to use one.

## 8. Say it out loud

**How it gets asked**

- "What is `self`, and why do you have to write it?"
- "What is the difference between a struct and a class?"
- "What does `@dataclass` generate, and when would you not use it?"

**What to say out loud, the first ninety seconds**

"A Python class bundles data and the methods that operate on it. `__init__` runs when an instance is created and stores the initial attributes on `self`, which is the instance itself; every method takes `self` explicitly as its first parameter, and `obj.method(x)` is sugar for `Class.method(obj, x)`. Attributes set on `self` belong to that instance; names defined directly in the class body are class attributes shared by every instance, which is a bug when the value is mutable.

Python has no struct; a class serves both roles. When a thing is only data, `@dataclass` generates `__init__`, `__repr__` and `__eq__` from the annotated fields. When a thing has invariants, like a balance that must only change through deposit and charge, I write a full class, keep the field as `_balance`, and expose a read-only `@property`. Privacy is convention: a leading underscore says internal, and nothing stops a caller who insists. Go and C++ enforce it; Python documents it."

**The follow-ups**

1. *"What is the difference between `__repr__` and `__str__`?"* — `__repr__` is for programmers and should look like the code that makes the object; `__str__` is for users. `print` uses `__str__` and falls back to `__repr__`, so defining only `__repr__` covers both.
2. *"How do you make a dataclass immutable?"* — `@dataclass(frozen=True)`. Assignment to a field then raises, and the instance becomes hashable, so it can be a dict key.
3. *"What does double underscore, `__balance`, do?"* — Name mangling: Python renames it to `_Account__balance` to avoid clashes in subclasses. It is still reachable under that name; it is not privacy either.

**A model answer**

"`class` defines a type whose instances carry per-object attributes, assigned on `self` in `__init__`, and whose behaviour lives in methods that receive the instance as their explicit first argument. Class-body assignments are shared class attributes, so mutable ones like lists must go on `self`. Encapsulation is by convention: `_name` marks internal state, `@property` gives read-only access, and `__name` merely mangles. `@dataclass` synthesises `__init__`, `__repr__` and `__eq__` from annotated fields, rejects mutable defaults in favour of `default_factory`, and with `frozen=True` gives immutability and hashing. There is no separate struct: dataclasses play that role, and a hand-written class is for types with invariants to enforce."

## 9. Recall card

- `class Account:` with `def __init__(self, ...)` storing `self.field = value`; every method takes `self` first, and `obj.m(x)` is `Account.m(obj, x)`.
- Missing `self` gives `takes 1 positional argument but 2 were given`; a list in the class body is shared by every instance.
- `_balance` is convention, not enforcement; `@property` makes `obj.balance` readable and `obj.balance = x` an `AttributeError`.
- `__repr__` returns the text `print` shows; write it to look like the constructor call.
- `@dataclass` writes `__init__`, `__repr__`, `==` from annotated fields; use `field(default_factory=list)` for mutable defaults; `frozen=True` for immutable.
