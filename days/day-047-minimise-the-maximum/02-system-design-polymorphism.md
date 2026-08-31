---
day: 47
track: system-design
title: "Polymorphism"
phase: "Object-oriented design"
status: written
---

# Day 047 · System design — Polymorphism

**After today you can:** You can explain polymorphism with code, not with a dictionary definition.

**The interviewer asks it as:** *What is polymorphism? Show me, do not tell me.*

---

## 1. What this is, and why they ask it

**Polymorphism** means one call site behaving differently depending on which object is at the other
end of it. You write `spot.can_fit(vehicle)` once. There are four kinds of spot, each with its own
answer, and the line that calls it never learns which kind it has. The caller sends a message; the
object decides what the message means.

They ask you to show it rather than define it because the definition is memorised everywhere and
understood in about half those places. "Many forms" is not an answer. What the interviewer wants is
the before-and-after: a chain of `if type == ...` branches, and the same code with the branches gone,
and a clear statement of what that bought — which is that adding a fifth kind of thing means writing
one new class and editing nothing. That is also why this question sits in the middle of design rounds
rather than in a quiz: every extensibility follow-up you will be asked in the next five days is
answered with polymorphism.

---

## 2. The story

Sarojini has been headmistress of a school in Vellore for eleven years, and the thing she is proudest
of is not a result.

When she took over, there were nine sections and a fire drill that took nineteen minutes. The way it
worked was that she walked. Bell at ten forty, and she started at the far end of the corridor and put
her head into each room: *you go down the back stairs, wait at the gate; you go through the hall,
you're closest; you two switch off the gas taps before anyone moves.* Nine rooms, one at a time, and
the little ones at the far end stood there for eleven minutes before anybody told them anything.

Two things went wrong with it, and the second one is why she changed it.

The first was that it was slow, which everyone could see.

The second was that in her third year a new pre-primary section opened in the annexe, and at the
drill in August she did her round of nine rooms and went back to her office, and those twenty-two
children sat where they were, because nobody had come to tell them. Not one person had done anything
wrong. She had a list of rooms in her head and the list was a year old.

So now there is a bell. One long ring, held for five seconds, at the announced time.

And the point of it — the thing she explains to every new teacher — is that the bell does not say
anything. It does not say *use the back stairs*. It says *now*, and each room already knows what
*now* means for that room. The little ones line up in twos and hold hands and go with their teacher.
The middle school walks itself down to the ground without being led. The science room switches off
the burners first, which takes forty seconds, and then goes. The office staff take the register
box and the keys. The annexe, whenever a new one opens, is told once, on the day it opens, what it
does when the bell goes.

Sarojini does not know, on the day of a drill, how many sections there are. She does not need to. She
rings the bell.

Four minutes and ten seconds, last February, with fourteen sections.

---

## 3. The idea in plain English

The bell is a method call. Each section is a class with its own version of "what to do now". And the
head teacher's old round of nine rooms is the `if/elif` chain — the thing polymorphism deletes.

### The before, and the after

Here is a parking lot deciding whether a vehicle fits a spot, written the way most people write it
first:

```python
def can_fit(spot, vehicle) -> bool:
    if vehicle.kind == "bike":
        return spot.size in ("bike", "compact", "large")
    elif vehicle.kind == "car":
        return spot.size in ("compact", "large")
    elif vehicle.kind == "truck":
        return spot.size == "large"
    raise ValueError(f"unknown vehicle kind {vehicle.kind}")
```

It works. Now add electric vehicles, which fit any spot that has a charger. You edit this function.
Then somebody adds pricing, which needs the same branches; then the display board, which needs them
again. The rule about what fits where is now in three places, and the fourth developer will add a
fifth kind and update two of them.

Here it is polymorphically:

```python
class Vehicle:
    def fits(self, spot: "Spot") -> bool:
        raise NotImplementedError

class Bike(Vehicle):
    def fits(self, spot): return spot.size in ("bike", "compact", "large")

class Car(Vehicle):
    def fits(self, spot): return spot.size in ("compact", "large")

class Truck(Vehicle):
    def fits(self, spot): return spot.size == "large"
```

and the caller becomes one line with no branches in it at all:

```python
if vehicle.fits(spot):
    ...
```

**That line is the whole idea.** It does not know how many kinds of vehicle exist. Adding electric
vehicles is a new class and no edit to any existing one, exactly like Sarojini telling the annexe
once, on the day it opens.

### The two names, and the one that matters

Textbooks split polymorphism in two:

- **Compile-time polymorphism**, or **overloading**: several methods with the same name and different
  argument types, and the compiler picks. Java has it; **Python does not**. In Python a second `def`
  with the same name simply replaces the first. Say this if asked — it is a common trip-up, and the
  Python answers are default arguments, `*args`, or `functools.singledispatch`.
- **Runtime polymorphism**, or **overriding**: a subclass replaces a parent's method, and which one
  runs is decided by the object at run time. This is the one interviews mean, and it is the one that
  removes branches.

### Duck typing: Python does not need a common parent

In Java, polymorphism requires a shared type — the objects must implement the same interface or
extend the same class. In Python they do not:

```python
class SlackNotifier:
    def send(self, message: str) -> None: ...

class EmailNotifier:
    def send(self, message: str) -> None: ...

for notifier in notifiers:        # no common base class anywhere
    notifier.send("build failed")
```

This is **duck typing**: if it has a `send` method that takes a string, it is a notifier. Python
looks the method up on the object at the moment of the call and does not care about its ancestry.

That freedom is real and it has one cost: nothing tells you at write time that a class forgot to
implement `send`, so you find out when the call happens. Two ways to get the check back without
giving up the freedom:

```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...
```

An **abstract base class** cannot be instantiated if an abstract method is missing — the error arrives
at construction rather than at the call. Or:

```python
from typing import Protocol

class Notifier(Protocol):
    def send(self, message: str) -> None: ...
```

A **Protocol** is a structural type: any class with a matching `send` satisfies it, with no
inheritance at all, and a type checker verifies it before the program runs. Protocol is duck typing
that a tool can check, and it is the modern Python answer.

### Where the branches are allowed to stay

Polymorphism is not the answer to every `if`. The honest rule:

- **Branching on a *type* that will grow** — vehicle kinds, payment methods, export formats, spot
  sizes — is what polymorphism is for.
- **Branching on a *value* or a state that will not grow** — `if amount > 1000`, `if status ==
  "CANCELLED"` — is just a condition, and turning it into three classes makes the code worse.

The test: *am I going to add a new branch to this `if` when a new kind of thing appears?* If yes, it
should be a method. If the branch list is closed and small — the days of the week, the four suits in
a pack — a `match` statement in one place is clearer than four classes.

### What it costs the reader

There is a genuine downside and interviewers respect you for naming it. With an `if/elif`, all four
behaviours are visible in one screen. With polymorphism they are in four files, and answering "what
happens for a truck?" means finding the truck class. You have traded *seeing all cases at once* for
*adding a case without touching anything*. That trade is usually right, and it is a trade.

---

## 4. The picture

The bell, and the call:

```
                    ONE MESSAGE                          ONE CALL SITE
                         |                                     |
                      [ bell ]                       vehicle.fits(spot)
                         |                                     |
       +---------+-------+-------+---------+       +-------+---+---+-------+
       |         |               |         |       |       |       |       |
   pre-primary  middle       science    office    Bike    Car    Truck  ElectricCar
       |         |               |         |       |       |       |       |
  line up in   walk to       burners    take     any    compact  large   any spot
  twos, go     the ground    off, then  the      spot   or       only    with a
  with teacher on their own  go         keys     size   large            charger
                                                                          ^
                                             added later. Nothing above changed.
```

**What to notice:** the top of both diagrams is one thing. The width at the bottom can grow forever
without the top being edited — that is the entire payoff.

The refactor, drawn as what happens when a fifth kind arrives:

```
 WITH BRANCHES                          WITH POLYMORPHISM

 can_fit()      -> edit                 class ElectricCar(Vehicle)   -> NEW file
 price_for()    -> edit                     def fits(self, spot)
 display_text() -> edit                     def price(self, hours)
 SpotSize enum  -> edit                     def display_text(self)
 the report     -> edit
                                        register it where vehicles
 5 edits to WORKING code                are constructed  -> 1 line

                                        1 new file, 1 line changed
```

**What to notice:** the units are edits to code that currently works. Each of those five is a chance
to break parking for ordinary cars; the one new file cannot break anything, because nothing depends
on it yet.

---

## 5. How it actually works

### The lookup, in Python

When Python evaluates `vehicle.fits(spot)` it looks up `fits` on the object's own dictionary, then on
its class, then up the method resolution order, and calls the first one it finds with `vehicle` as
the first argument. Nothing is decided in advance. That is why a `Truck` created a millisecond ago
runs `Truck.fits` even though the calling code was written before `Truck` existed.

In Java the mechanism is a **virtual method table** — each object points to its class's table of
method addresses, and the call is an indirect jump through it. Different machinery, identical
consequence, and worth one sentence if the interviewer's language is Java.

### The special methods you already use

Python's built-in functions are polymorphism you have been relying on since
[day 005](../day-005-python-lists-and-tuples/README.md):

```python
len(x)          -> x.__len__()
str(x)          -> x.__str__()
x + y           -> x.__add__(y)
for i in x      -> x.__iter__()
x[3]            -> x.__getitem__(3)
```

`len` works on a list, a string, a dict, a set and on any class you write that defines `__len__`. The
`len` function contains no branches on type at all. That is exactly the shape you are being asked to
demonstrate, and pointing at it is a strong answer: *"the standard library's `len` is polymorphic —
it calls `__len__` on whatever it is given, and my class joins that set by defining one method."*

### Real designs built on it

- **Python's `logging.Handler`** — `StreamHandler`, `FileHandler`, `RotatingFileHandler`,
  `SMTPHandler`. `Logger` calls `handler.emit(record)` and knows nothing else. Adding a handler that
  posts to Slack requires zero changes to the logging module.
- **File-like objects.** `open()`, `io.StringIO`, `gzip.open` and a network socket all support
  `.read()` and `.write()`, so `json.load(f)` works on all of them. There is no `File` base class
  enforcing this — it is duck typing, at the scale of an entire ecosystem.
- **Django's storage backends.** `FileSystemStorage` and `S3Storage` both implement `save`, `open`
  and `url`, so moving uploads to S3 is a settings line.
- **Payment gateways.** `RazorpayGateway`, `StripeGateway`, `PayPalGateway` behind one `charge`
  method. The checkout flow has no idea which one it has, which is what makes adding a gateway a
  contained change rather than a release.
- **`sorted(items, key=...)`** — the comparison behaviour is supplied by the caller. Same idea,
  arriving as a function instead of an object, and it is the seam you will meet as strategy on
  [day 058](../day-058-custom-comparators/README.md).

### The refactoring, step by step

Turning a type switch into polymorphism is a mechanical recipe, and being able to run it out loud is
worth a lot in a design round.

1. **Find the switch.** Look for `if x.kind ==` or `isinstance` chains. Look for *two* of them on the
   same set of types — that is the strongest signal, because the duplication is the actual cost.
2. **Name the question the switch is answering.** "Does this fit?" "What does it cost?" That name
   becomes the method.
3. **Create the base declaration** — an abstract method or a Protocol.
4. **Move each branch body into its own class**, unchanged.
5. **Replace the switch with the call.**
6. **Delete the type tag.** If `vehicle.kind` is no longer read anywhere, remove it. Leaving it means
   somebody will write a new switch on it next year.

Step six is the one people skip, and it is the one that makes the refactoring stick.

---

## 6. The numbers

### The cost of adding a kind

```
a system with 3 vehicle types and 4 places that branch on type
    (allocation, pricing, display, the daily report)

add a 4th type, with branches:
    4 files edited, all of them currently working
    each edit is a chance to break the 3 existing types
    the branch somebody forgets fails at run time, in production

add a 4th type, polymorphically:
    1 new class implementing 4 methods
    1 line where vehicles are constructed
    a missing method fails at CONSTRUCTION with an abstract-class error,
    or before running at all if a Protocol and a type checker are used
```

**Four edits to working code against one new file.** And the failure moves from run time in
production to construction time in development, which is the more valuable half of the change.

### The branch-count multiplication

```
kinds x places-that-branch = branches to maintain

3 kinds x 4 places  = 12 branches
5 kinds x 4 places  = 20 branches
5 kinds x 7 places  = 35 branches

polymorphic:  5 classes x 4 methods = 20 methods, but each one lives with its own kind,
              and adding a 6th kind touches 0 of the existing 20.
```

The count is similar; the *coupling* is not. Twenty branches spread over four files must all be
edited together. Twenty methods in five files are edited one file at a time.

### Runtime cost

```
direct function call                       ~40-60 ns
polymorphic method call (Python)           ~60-80 ns
Java virtual call                          ~1-2 ns   (often inlined away entirely)

10,000 polymorphic calls in one request:   ~0.7 ms
one database round trip:                   ~1 ms
```

The dispatch is free at any scale a web request cares about. If a candidate argues against
polymorphism on speed, they are optimising the wrong four orders of magnitude — say so.

### When the switch is genuinely cheaper

```
a closed set that will never grow (7 days, 4 suits, 3 HTTP verbs you support):
    match statement in ONE place    : 1 file,  ~10 lines
    a class per case                : 7 files, ~70 lines, and a factory

-> for a closed set, the switch wins on every measure that matters.
```

---

## 7. The trade-offs

### Seeing all the cases against adding a case cheaply

An `if/elif` shows every behaviour on one screen; polymorphism scatters them across files. *I would
not use polymorphism for a set of cases that is closed and small*, because then I am paying the
scatter and getting nothing — nobody is ever adding a fifth day to the week. The moment the set can
grow, the trade flips, because a growing set means repeated edits to working code.

### Polymorphism against a `match` statement

Python 3.10's `match` is genuinely good for closed sets and for dispatching on *shape* rather than on
type. *I would not turn three `match` arms into three classes unless the arms are going to multiply* —
and I would say the trigger out loud: the second place in the codebase that switches on the same set
is the moment to refactor, because that is when the duplication starts costing.

### Duck typing against explicit contracts

Duck typing is flexible and gives you no warning when a class forgets a method. *I would not rely on
bare duck typing across a module boundary* — inside one file it is fine; across a plugin interface I
want a Protocol or an abstract base class, so a missing method is an error at construction or at type
check rather than at three in the morning.

### Adding behaviour against adding types

This is the trade-off nobody mentions and it is worth knowing. Polymorphism makes adding a **new
type** cheap and adding a **new operation** expensive — a new operation means a new method on every
existing class. A switch statement is the exact opposite: adding an operation is one new function,
adding a type edits everything. *I would choose based on which axis actually grows.* Vehicle kinds
grow; the operations on them are fairly stable, so polymorphism wins. If instead the types were fixed
and the operations kept multiplying, the honest answer is a visitor-style arrangement or plain
functions, and saying that is a strong signal.

### The honest sentence

> Polymorphism is not about "many forms". It is a bet that the list of kinds will grow and the list of
> operations will not. Make that bet where it is true, and adding a kind is a new file; make it where
> it is false, and every new operation touches every class you own.

---

## 8. In the interview

### How it gets asked

- *"What is polymorphism? Show me, don't tell me."* — the direct form, and the answer is a
  before-and-after with a type switch removed.
- *"Refactor this."* — handed a function with an `isinstance` chain in it. Same answer, applied.
- *"How would you support a new payment provider?"* — polymorphism arriving as a design question,
  which is how it usually appears in an LLD round.
- *"What's the difference between overloading and overriding?"* — the vocabulary check, where the
  useful extra sentence is that Python has no overloading.

### What to say out loud, in the first ninety seconds

1. **Refuse the definition, offer the demonstration.** *"Let me show it with the code rather than
   define it. Here's the version with a type switch, and here's the same thing with the switch
   gone."*
2. **Write the switch first.** Four lines of `if vehicle.kind ==`. Then say what is wrong with it:
   *"the rule about what fits where is going to appear in pricing and in the display too, so it'll be
   in three places and someone will update two."*
3. **Write the polymorphic version**, and point at the call site: *"the caller is now one line with no
   branches, and it doesn't know how many kinds of vehicle exist."*
4. **State the payoff in units of edits.** *"Adding electric vehicles is one new class and one line
   where vehicles are constructed — against four edits to code that currently works."*
5. **Name the cost, unprompted.** *"What I've given up is seeing all four behaviours on one screen.
   That trade is right when the list of kinds grows, and wrong when it's closed — I wouldn't do this
   for the days of the week."*

### The follow-ups

**"Python has no interfaces and no `private`. Does polymorphism even mean anything here?"**
It means more here, not less, because Python does not require a shared base class at all. If an object
has a `send` method taking a string, it works everywhere a notifier is expected — that is duck typing,
and the standard library is built on it. File-like objects are the clearest example: `open()`,
`io.StringIO`, `gzip.open` and a socket all support `read` and `write`, there is no `File` base class
anywhere enforcing that, and `json.load` works with all of them. What Python gives up is the
write-time guarantee: nothing tells you a class forgot `send` until the call happens. So I'd say what
I actually do about that, because that is the real question. Inside one module, plain duck typing.
Across a boundary where other people plug things in, an abstract base class, so that a missing method
raises at construction rather than at use — you cannot instantiate an ABC with an unimplemented
abstract method. Or, better in modern code, a `typing.Protocol`, which is structural — any class with
a matching `send` satisfies it, with no inheritance — and which a type checker verifies before the
program runs. Protocol is duck typing that a tool can check, and it is the answer I would give.

**"When is an if/else actually better?"**
When the set of cases is closed and small, and I would give the test rather than a rule. The question
is whether I will be adding a branch to this `if` when a new kind of thing appears. Days of the week,
the four suits in a pack, the three HTTP methods a particular endpoint supports — those sets do not
grow, and turning them into seven classes plus a factory costs seventy lines to replace ten and gains
nothing. Branching on a *value* or a *state* is also usually fine: `if amount > 1000` is a business
condition, not a type, and modelling large amounts as a subclass would be strange. The second signal
I watch for is duplication rather than size: one switch in one place is a switch, but the *same*
switch appearing in a second place is the point where the cost starts, because now the two can
disagree. So my trigger for refactoring is not "there are more than three branches", it is "this is
the second function that branches on the same set of types". And I'd mention the deeper trade-off:
polymorphism makes adding types cheap and adding operations expensive, while a switch is the opposite,
so the right choice depends on which axis actually grows in this system.

**"You've replaced four branches with four classes. Isn't that the same amount of code, just spread
out?"**
Roughly the same number of lines, yes, and a genuinely different coupling, which is what actually
costs money. With four branches in four functions — allocation, pricing, display, the report — adding
a fifth vehicle type means editing four files that currently work, and all four edits have to land
together or the system is inconsistent: a vehicle that can park but cannot be priced. Each of those
edits is a chance to break the four existing types, and the one somebody forgets fails at run time in
production, with no error at write time. With polymorphism, adding a type is one new file
implementing four methods, and it cannot break anything that exists because nothing existing refers to
it. If I forget a method, an abstract base class stops me at construction, or a type checker stops me
before the program runs at all. So the count of lines is similar; what changed is that the change is
*local* and the failure moved from production to development. That is the whole argument, and I'd
also concede the other side honestly: I have lost the ability to see all four behaviours on one
screen, and if I ever needed to add a *fifth operation* rather than a fifth type, I would now be
editing five classes instead of writing one function.

### A model answer

> "Let me show it rather than define it.
>
> Here's the version people write first — a parking lot deciding whether a vehicle fits a spot:
>
> ```python
> def can_fit(spot, vehicle) -> bool:
>     if vehicle.kind == "bike":
>         return spot.size in ("bike", "compact", "large")
>     elif vehicle.kind == "car":
>         return spot.size in ("compact", "large")
>     elif vehicle.kind == "truck":
>         return spot.size == "large"
> ```
>
> It works today. The problem is that the same three-way branch is going to appear in pricing, in the
> display board and in the daily report — so the rule lives in four places, and when someone adds
> electric vehicles they'll update three of them.
>
> Polymorphically, each kind owns its own answer:
>
> ```python
> class Bike(Vehicle):
>     def fits(self, spot): return spot.size in ("bike", "compact", "large")
>
> class Car(Vehicle):
>     def fits(self, spot): return spot.size in ("compact", "large")
>
> class Truck(Vehicle):
>     def fits(self, spot): return spot.size == "large"
> ```
>
> and the caller is one line: `if vehicle.fits(spot):`. That line doesn't know how many kinds of
> vehicle exist, and it never has to.
>
> The payoff in units that matter: adding electric vehicles is one new class and one line where
> vehicles are constructed, against four edits to code that currently works — and each of those four
> is a chance to break parking for ordinary cars. The failure also moves: if I forget a method, an
> abstract base class stops me at construction, rather than a missing branch failing in production.
>
> In Python I'd note two things. There's no overloading — a second `def` with the same name just
> replaces the first — so when people say 'compile-time polymorphism' that's Java, and the Python
> answers are default arguments or `functools.singledispatch`. And Python doesn't need a common base
> class at all: duck typing means anything with a `fits` method works. I'd still declare a Protocol or
> an abstract base for anything crossing a module boundary, so a missing method is caught before run
> time.
>
> And the cost, since there is one: I've given up seeing all four behaviours on one screen. That's the
> right trade when the list of kinds grows. For a closed set — days of the week, the four suits — I'd
> keep a single `match` statement, because seven classes and a factory to replace ten lines is worse."

---

## 9. Recall card

- **Show it, never define it:** an `if vehicle.kind == ...` chain, then the same thing as
  `vehicle.fits(spot)` with no branches. The caller never learns how many kinds exist.
- **The payoff in edits:** a new kind is 1 new file + 1 wiring line, against 4 edits to *working* code
  — and a missing method fails at construction (ABC) or before running (Protocol) instead of in
  production.
- **Python has no overloading** (a second `def` replaces the first) — only overriding, plus
  `singledispatch`. And it needs no common base: **duck typing**, made checkable by
  `typing.Protocol` or enforced at construction by an `ABC`.
- **The refactor is mechanical:** find the switch → name the question it answers → declare the
  abstract method → move each branch into its class → replace the switch with the call → **delete the
  type tag**, or someone rebuilds the switch.
- **Keep the `if` when the set is closed** (days, suits) or you are branching on a *value*. The
  trigger to refactor is the *second* place switching on the same types. Polymorphism makes new
  **types** cheap and new **operations** expensive — choose by which axis grows.
