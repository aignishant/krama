---
day: 61
track: system-design
title: "Coupling, cohesion, and code smells"
phase: "SOLID and design principles"
status: written
---

# Day 061 · System Design — Coupling, cohesion, and code smells

**After today you can:** You can name what is wrong with a bad module in the vocabulary reviewers use.

**The interviewer asks it as:** *Review this module. What would you change?*

---

## 1. What this is, and why they ask it

**Coupling** is how much one piece of code has to know about another. **Cohesion** is how much the
things inside one piece of code belong together. The goal, in the oldest slogan in software design,
is **low coupling and high cohesion** — modules that mind their own business, each containing things
that are used together.

**Code smells** are the named symptoms. Feature envy, shotgun surgery, primitive obsession, data
clumps, message chains, god object. They are not rules and they are not bugs; each one is a
recognisable pattern that usually means a boundary is in the wrong place.

They ask you to review a module because it is the only question in the design round that tests
vocabulary and judgement together. Anyone can say "this is messy". A candidate who says *"changing an
address touches five files, which is shotgun surgery — the address logic is spread out, and it should
be one `Address` type"* has named the problem in words the reviewer already uses, and has said what
to do. This is also the last day of the principles phase, and coupling and cohesion are the ideas
underneath all five of them: single responsibility is cohesion, dependency inversion is coupling
direction, interface segregation is coupling width.

---

## 2. The story

Anjali and her husband moved into a rented flat in Kothrud in June, and there were two things about
it that she could not stop noticing, and neither of them was a fault exactly. The flat was clean and
the taps worked.

The first was the kitchen. Whoever had put it together had done it by size. All the large things in
the cupboard by the window, all the small things in the drawers by the door, all the tall things in
the corner unit. It looks tidy. It photographs well.

But she makes tea every morning, and making tea in that kitchen meant: the strainer from the drawer
by the door, the small pan from the cupboard by the window, the tea from the corner unit, the sugar
from a different shelf in the corner unit, and the milk from the fridge, which is behind you when you
are at the stove. Five places, four of them not near the stove, every single morning. Nothing was
lost. Everything was findable. It just took nine or ten minutes for something that should take four,
and she did it twice a day for four months.

The second thing was the light switches, and this one made her genuinely angry twice.

The switchboard in the bedroom has four switches. One of them does the bedroom tube light. One does
the fan. And one does both the balcony light and her husband's reading lamp, on the same switch, on
the same line, because whoever wired the flat ran them together.

So on any night she wanted the balcony light off — which is every night, because it shines into the
bedroom — she had to turn off his reading lamp too. He would be reading. She would ask. He would
sigh. Twice they had a proper argument about it, at eleven at night, about a light.

When they moved to their own flat in November, she did two things before the furniture came in.

She put the kitchen together by job instead of by size. Everything for tea — the pan, the strainer,
the tea, the sugar — in the cupboard directly above the stove, and the sugar jar next to the tea jar
rather than with the other jars. Everything for the pressure cooker in one place. It looks less tidy.
Tea takes four minutes.

And she stood over the electrician for an afternoon and made him give the balcony light its own
switch. It cost eleven hundred rupees. Nobody has argued about a light since.

---

## 3. The idea in plain English

The kitchen arranged by size is **low cohesion** — things used together kept apart, so every job
takes trips. The balcony light on the reading lamp's switch is **tight coupling** — two things wired
together that have no reason to be, so you cannot change one without changing the other.

### Cohesion: do the things inside belong together?

**High cohesion** means everything in a module is there for the same job. You can say what the module
is for in one sentence with no "and" — which is the single responsibility test from
[day 055](../day-055-quickselect/README.md), arriving from the other direction.

There is a standard ladder, worst to best, and knowing the names of the bottom rungs is genuinely
useful because they describe real modules:

```
 COINCIDENTAL   things are together for no reason.  utils.py, helpers.py, common.py
 LOGICAL        things are together because they are the same KIND.
                  "all the validators", "all the parsers"  -- the kitchen by size
 TEMPORAL       things are together because they happen at the same TIME.
                  init.py: open the log, connect the DB, load config, warm the cache
 PROCEDURAL     they run in a sequence, but on unrelated data
 COMMUNICATIONAL they operate on the SAME data
 FUNCTIONAL     they all contribute to ONE well-defined job          <- aim here
```

Anjali's first kitchen is **logical cohesion** — grouped by kind, which looks tidy and is wrong,
because the unit of use is the job, not the kind. A `validators.py` holding every validator in the
system is exactly that: it looks organised, and every feature has to reach into it.

The tell for low cohesion is **trips**. To do one job you open five files. To understand one flow you
read four modules. Anjali's nine-minute tea.

### Coupling: how much does one module know about another?

**Low coupling** means a module can be understood, changed and tested with minimal knowledge of the
others. There is a ladder here too, and this one gets quoted in reviews:

```
 CONTENT   A reaches into B's internals -- reading private fields, monkey-patching
 COMMON    A and B share global mutable state
 CONTROL   A passes B a flag that decides WHICH BRANCH B takes
             render(report, as_pdf=True)  -- the caller is steering the callee
 STAMP     A passes a whole object when B needs one field
             send_email(user)  when it only needs user.email
 DATA      A passes exactly what B needs
             send_email(address)                                      <- aim here
 MESSAGE   A only sends a message; it does not even know B's shape
```

The two in the middle are the ones you will actually meet.

**Control coupling** is the boolean flag. `render(report, as_pdf=True)` means the caller knows there
are two branches inside and is choosing one — so the caller and the callee are welded together, and
adding a third format changes both. Two functions, or a strategy
([day 056](../day-056-non-comparison-sorts/README.md)), removes it.

**Stamp coupling** is passing a whole object for one field. `send_welcome_email(user)` when the
function only needs an address means the email module now depends on the shape of `User`, so a change
to `User` can break email. `send_welcome_email(address)` does not.

### The two smells that matter most, because they are the diagnosis

Almost every review comment reduces to one of these two, and they are opposites:

> **Shotgun surgery** — one change forces edits in many places.
> That is **coupling too high** (or cohesion too low): the knowledge is scattered.
>
> **Divergent change** — one place gets edited for many unrelated reasons.
> That is **cohesion too low** in a single file: unrelated knowledge is piled together. This is the
> single responsibility violation from [day 055](../day-055-quickselect/README.md).

If you learn two terms today, learn those. Both are about *change*, and both can be measured from the
version history rather than argued about.

### The rest of the vocabulary, with the fix attached

| Smell | What it looks like | Usually means | Fix |
|---|---|---|---|
| **Feature envy** | A method uses another object's data more than its own | Behaviour is on the wrong class | Move the method to the data |
| **Data clump** | The same 3-4 parameters travel together everywhere | A missing class | `Address`, `DateRange`, `Money` |
| **Primitive obsession** | Ids, money, emails as bare `str` and `int` | A missing value object | A frozen type with validation |
| **Long parameter list** | 6+ parameters, several with defaults | A data clump, or control coupling | Group into an object; split the function |
| **Message chain** | `order.customer.address.city.name` | Reaching through objects | Ask for what you need: `order.delivery_city()` |
| **Middle man** | A class whose methods only forward | A useless layer | Delete it; talk to the real thing |
| **God object** | One class knows and does everything | No boundaries at all | Split by stakeholder |
| **Temporal coupling** | `configure()` must be called before `run()` | A constructor that lies | Make the object valid on construction |
| **Shotgun surgery** | One change, many files | Scattered knowledge | Gather it into one place |
| **Divergent change** | One file, many reasons to change | Piled-up knowledge | Split by reason |

**Message chains** have a rule of their own, the **Law of Demeter**: a method should only talk to
itself, its own fields, its parameters, and objects it creates. `order.customer.address.city` breaks
it, and the harm is real — that line depends on four classes, so a change to any of the four can
break it, and it cannot be tested without building all four.

### How to actually review a module

Six checks, in order, and each one takes under a minute:

1. **Read the imports.** They are a summary of what this file depends on. Do they tell a consistent
   story? `decimal` and `smtplib` together is two jobs.
2. **Say what it does in one sentence.** If you need "and", note it.
3. **Count the fan-out** — how many other modules it calls. High fan-out means many reasons to break.
4. **Look at the parameter lists.** Data clumps, boolean flags, and primitives that should be types
   are all visible from the signatures alone.
5. **Read one test.** Long, mostly-irrelevant setup means the module is coupled to things it does not
   need.
6. **Check the version history.** `git log` on the file answers both diagnosis questions at once —
   many authors from many teams means divergent change; one feature touching eight files means
   shotgun surgery.

The sixth is the only one that produces evidence rather than opinion, and saying you would look
there is worth marks on its own.

---

## 4. The picture

Anjali's two kitchens:

```
 BY SIZE — logical cohesion. Tidy, and every job is a tour of the flat.

    cupboard by the window   [ big pans, big vessels, the cooker ]
    drawer by the door       [ strainer, spoons, small knives ]
    corner unit              [ tea, sugar, rice, dal, oil ]
    fridge (behind you)      [ milk ]

    making tea:  door -> window -> corner -> corner -> fridge -> stove
                 5 places, 9 minutes, twice a day


 BY JOB — functional cohesion. Looks worse. Tea takes 4 minutes.

    above the stove          [ small pan, strainer, tea, sugar ]   <- the tea job
    left of the stove        [ cooker, its lid, the weight ]       <- the cooker job
    corner unit              [ rice, dal, oil ]

    making tea:  one cupboard, one reach
```

**What to notice:** the first arrangement is not disordered. It has a rule and the rule is followed
consistently — it is just the wrong rule, because the unit of use is the *job*, not the *kind*. A
`utils.py` or a `validators.py` is exactly this, and it is why those files always grow.

The switch:

```
  COUPLED                                   DECOUPLED

  bedroom switch #3                         switch #3  ---> balcony light
       |                                    switch #4  ---> reading lamp
       +---> balcony light
       |
       +---> reading lamp

  "turn off the balcony light"              "turn off the balcony light"
    -> the reading lamp goes off              -> the balcony light goes off
    -> an argument at 11 p.m.
    -> you cannot change one without
       affecting the other
```

**What to notice:** the coupling is invisible from outside. Both flats have four switches and the
same lights. What differs is which changes are possible independently, and you only find out by
trying to make one.

The two diagnostic smells, drawn as change:

```
 SHOTGUN SURGERY — one change, many files. Coupling too high.

   "add a second address line"
        |
        +--> models/user.py          (the field)
        +--> forms/signup.py         (the form)
        +--> forms/checkout.py       (the other form)
        +--> serializers/user.py     (the API shape)
        +--> templates/invoice.html  (the display)
        +--> services/shipping.py    (the formatting)
        +--> tests/... (x4)

   10 files for one idea. The knowledge "what an address is" is SCATTERED.
   Fix: gather it. One Address type, one formatter, one validator.


 DIVERGENT CHANGE — one file, many reasons. Cohesion too low.

                          +--> finance changes the tax rule
   OrderProcessor.py <----+--> marketing changes the email copy
      (642 lines)         +--> platform migrates the database
                          +--> operations changes the stock policy

   4 unrelated reasons to open one file. The knowledge is PILED UP.
   Fix: split it by reason.  (day 055)
```

**What to notice:** they are opposites and the fixes are opposite. Shotgun surgery says *gather*;
divergent change says *split*. Diagnosing which one you have is the whole job, and both are visible
in the version history.

Coupling, from worst to best, on one call:

```
  CONTENT   emailer._smtp.sendmail(...)          reaching into internals
  COMMON    CONFIG["smtp_host"] = ...            shared global state
  CONTROL   send(user, is_admin=True)            the caller picks the branch
  STAMP     send_welcome(user)                   passes a whole User for one field
  DATA      send_welcome(user.email)             passes exactly what is needed
  MESSAGE   events.publish(UserSignedUp(email))  the sender does not know the receiver

  Each step down removes something the caller has to know.
  DATA is the sensible default. MESSAGE is for when you want them fully independent.
```

**What to notice:** the difference between STAMP and DATA is one dot, and it decides whether the email
module depends on the `User` class at all.

---

## 5. How it actually works

### A module to review

This is the kind of thing you get handed. Read it before the diagnosis.

```python
# shipping/dispatcher.py
import psycopg
import requests

CONFIG = {}                                            # module-level mutable state


class Dispatcher:
    def __init__(self, conn) -> None:
        self.conn = conn

    def dispatch(self, order, express=False, international=False,
                 insured=False, gift_wrap=False, notify=True) -> str:
        city = order.customer.address.city.name        # a message chain
        pin = order.customer.address.pincode

        if express and not international:
            cost = 12000 if order.weight_grams > 500 else 8000
        elif international:
            cost = 45000 + (order.weight_grams * 12)
        else:
            cost = 4000 if order.weight_grams > 500 else 2500
        if insured:
            cost += int(order.total_paise * 0.02)
        if gift_wrap:
            cost += 5000

        label = (f"{order.customer.name}\n"
                 f"{order.customer.address.line1}\n"
                 f"{order.customer.address.line2}\n"
                 f"{city} {pin}")

        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO shipments (order_id, cost, label) VALUES (%s,%s,%s)",
                        (order.order_id, cost, label))

        tracking = requests.post(CONFIG["courier_url"],
                                 json={"pin": pin, "weight": order.weight_grams}).json()["id"]
        if notify:
            requests.post(CONFIG["sms_url"],
                          json={"to": order.customer.phone, "text": f"Shipped: {tracking}"})
        return tracking
```

### The review, said out loud in the right vocabulary

**Cohesion.** *"I can't describe this in one sentence without 'and'. It calculates shipping cost,
formats a label, writes to the database, calls a courier, and sends an SMS. That's five jobs, and
they change for different reasons — finance owns the cost table, design owns the label, platform owns
persistence. That's **divergent change**."*

**Control coupling.** *"Five boolean parameters. Every one of them means the caller knows about a
branch inside this method and is steering it. `dispatch(order, express=True, insured=True)` is the
caller doing the deciding, so the caller and the callee change together. Those flags describe *what
kind of shipment this is*, which is a missing concept."*

**Message chain.** *"`order.customer.address.city.name` reaches through four objects. That single line
depends on `Order`, `Customer`, `Address` and `City`, so any of the four can break it, and testing it
means constructing all four. That's a Law of Demeter violation — I'd ask the order for what I
actually need."*

**Stamp coupling.** *"The cost calculation only needs a weight and a destination, but it receives a
whole `Order` and reaches into the customer's address. So the pricing rules now depend on the shape
of `Customer`."*

**Common coupling.** *"`CONFIG` is module-level mutable state read from inside the method. Two tests
in the same process affect each other, and a missing key fails at call time rather than at
start-up."*

**Primitive obsession.** *"Costs are bare integers of paise with no type, so nothing stops you adding
a weight to a cost. A pincode is a bare string with no validation."*

**Data clump.** *"`line1`, `line2`, `city`, `pincode` travel together everywhere in this codebase.
That is an `Address` asking to exist, with `format_label()` on it."*

**Fan-out.** *"This one method touches the database, an HTTP courier API and an SMS API. Three
external systems means three ways for it to fail, and no way to test the pricing without all three."*

### The rewrite

Start by extracting the missing concepts, which is what most of the smells were pointing at:

```python
# shipping/model.py
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Money:
    paise: int
    def __add__(self, other: "Money") -> "Money":
        return Money(self.paise + other.paise)


@dataclass(frozen=True)
class Address:
    """The data clump, given a name. Behaviour comes with it."""
    line1: str
    line2: str
    city: str
    pincode: str

    def __post_init__(self) -> None:
        if not (self.pincode.isdigit() and len(self.pincode) == 6):
            raise ValueError(f"invalid pincode: {self.pincode!r}")

    def as_label(self, name: str) -> str:
        return f"{name}\n{self.line1}\n{self.line2}\n{self.city} {self.pincode}"


class Service(Enum):
    """The five booleans, replaced by the concept they were describing."""
    STANDARD = "standard"
    EXPRESS = "express"
    INTERNATIONAL = "international"
```

The five flags become one enum plus two genuine options. That removes the control coupling: the
caller now says *what it wants*, not *which branch to take*.

```python
# shipping/pricing.py -- owned by finance. One reason to change.
from .model import Money, Service


class ShippingPricing:
    def __init__(self, rates: dict[Service, tuple[int, int]],
                 insurance_rate: float, gift_wrap: Money) -> None:
        self._rates = rates
        self._insurance_rate = insurance_rate
        self._gift_wrap = gift_wrap

    def quote(self, service: Service, weight_grams: int, order_value: Money,
              insured: bool = False, gift_wrap: bool = False) -> Money:
        light, heavy = self._rates[service]
        cost = Money(heavy if weight_grams > 500 else light)
        if insured:
            cost = cost + Money(int(order_value.paise * self._insurance_rate))
        if gift_wrap:
            cost = cost + self._gift_wrap
        return cost
```

Note what this function receives: a service, a weight, a value. **Data coupling** — exactly what it
needs, and nothing else. It does not know that `Order` or `Customer` exist, so it can be tested in
three lines and it cannot be broken by a change to either.

```python
# shipping/dispatcher.py -- one reason to change: the sequence of steps
from .model import Address, Money, Service
from .pricing import ShippingPricing
from .ports import Courier, Notifier, ShipmentRepository


class Dispatcher:
    def __init__(self, pricing: ShippingPricing, shipments: ShipmentRepository,
                 courier: Courier, notifier: Notifier | None = None) -> None:
        self._pricing = pricing
        self._shipments = shipments
        self._courier = courier
        self._notifier = notifier

    def dispatch(self, order_id: str, service: Service, weight_grams: int,
                 value: Money, destination: Address, recipient: str,
                 insured: bool = False, gift_wrap: bool = False) -> str:
        cost = self._pricing.quote(service, weight_grams, value, insured, gift_wrap)
        label = destination.as_label(recipient)
        tracking = self._courier.book(destination.pincode, weight_grams)
        self._shipments.save(order_id, cost, label, tracking)
        if self._notifier:
            self._notifier.shipped(order_id, tracking)
        return tracking
```

Read the improvements out loud, because that is the answer:

- **No message chains.** It receives an `Address` and a name; it never walks
  `order.customer.address`.
- **No control coupling.** `Service` is a value describing the shipment, not a switch selecting a
  branch.
- **No common coupling.** `CONFIG` is gone; the courier and notifier are injected
  ([day 059](../day-059-sorting-revision/README.md)).
- **Fan-out of zero to external systems.** Three ports, all owned here, all fakeable.
- **One sentence, no "and":** *it runs the dispatch sequence.* Ordering the steps is a legitimate
  single responsibility.

### The test, which is the proof

```python
def test_an_insured_express_shipment_is_priced_and_booked() -> None:
    pricing = ShippingPricing({Service.EXPRESS: (8000, 12000)}, 0.02, Money(5000))
    shipments, courier = InMemoryShipments(), FakeCourier(tracking="TRK1")
    dispatcher = Dispatcher(pricing, shipments, courier)

    tracking = dispatcher.dispatch(
        order_id="ORD-1", service=Service.EXPRESS, weight_grams=600,
        value=Money(1_000_00), destination=Address("12 MG Rd", "Kothrud", "Pune", "411038"),
        recipient="Anjali", insured=True,
    )

    assert tracking == "TRK1"
    assert shipments.saved[0].cost == Money(12000 + 200)
```

No database, no network, five lines of setup. Testability is the measurable consequence of low
coupling, and it is the strongest evidence in a review.

### Where the ladders show up in real systems

- **Unix pipes** are the low-coupling ideal: `ls | sort | head` — each program knows only about bytes
  on a stream, so any of them can be replaced.
- **`utils.py`** is coincidental cohesion, everywhere, in every language. It grows forever precisely
  because nothing belongs there and nothing is excluded.
- **A `settings.py` read directly from deep inside modules** is common coupling, and it is why
  Django's `settings.configure()` and twelve-factor config exist.
- **Event-driven systems** are the message-coupling end: a publisher does not know who consumes, so
  adding a consumer changes nothing — at the cost of not being able to follow the flow by reading.
- **The React container/presentational split** is a cohesion decision: one component decides what
  data, another decides what it looks like, so designers and data changes stop colliding.
- **`git log --format='%an' -- path/to/file | sort -u`** is the diagnosis tool, and it works on any
  codebase in any language.

---

## 6. The numbers

### Shotgun surgery, measured

```
 "add a second address line"

 with the address spread as 4 primitives:
   files touched               : 10   (model, 2 forms, serializer, template,
                                       shipping formatter, 4 test files)
   lines changed               : ~60
   places somebody will forget : 2    (empirically -- the invoice template and
                                       one test fixture)
   review time                 : ~90 min, across 3 reviewers who each own part

 with one Address type owning its own formatting:
   files touched               : 2    (the Address class and its test)
   lines changed               : ~8
   review time                 : ~10 min, 1 reviewer
```

### Divergent change, measured

```
 git log --since=1.year --format='%an' -- shipping/dispatcher.py | sort -u | wc -l

   before : 11 authors, 84 commits, 19 merge conflicts
   after  : pricing.py    3 authors, 14 commits, 0 conflicts
            dispatcher.py 2 authors,  9 commits, 0 conflicts
            courier.py    2 authors, 11 commits, 1 conflict
```

Eleven authors on one file is the measurement. That number is the review comment.

### Coupling, priced by test setup

```
 testing "an insured express shipment costs 12,200 paise"

 coupled version:
   needs a real Order with a Customer with an Address with a City
   needs a database connection (the INSERT is inline)
   needs CONFIG populated with two URLs
   needs the courier and SMS endpoints stubbed at the HTTP level
   setup: 31 lines, ~400 ms, flaky

 decoupled version:
   ShippingPricing(rates, 0.02, Money(5000)).quote(...)
   setup: 3 lines, ~0.05 ms, cannot flake

 ~8,000x faster, and the pricing rule is now testable at all
 without four other classes existing.
```

### Fan-out, and the probability of breaking

```
 a module calling N others, each of which changes ~monthly:

   N = 1  -> ~1 potentially breaking change/month
   N = 3  -> ~3
   N = 9  -> ~9, i.e. this module is disturbed roughly every 3 days

 A module's exposure to breakage is roughly LINEAR in its fan-out,
 which is why "how many things does this file import?" is a real review question.
```

### The message chain, priced

```
 order.customer.address.city.name

 classes this one line depends on : 4
 changes that can break it        : a rename or restructure in ANY of the four
 objects needed to test it        : 4, constructed and wired

 order.delivery_city()
 classes depended on              : 1
 objects needed to test it        : 1
```

### The boolean-flag cost

```
 dispatch(order, express, international, insured, gift_wrap, notify)

 combinations the signature allows : 2^5 = 32
 combinations that are meaningful  : ~6
 combinations tested               : 4
 combinations that are nonsense
   but compile                     : express=True AND international=True
                                     -- the code silently ignores one of them

 Replacing 2 of the flags with a 3-valued enum:
   allowed combinations : 3 x 2 x 2 x 2 = 24, and the nonsense one is unrepresentable
```

---

## 7. The trade-offs

### Coupling cannot be removed, only moved and shaped

Modules that never interact do nothing. The goal is not zero coupling; it is coupling that is
**visible, narrow, and pointing the right way**. Passing exactly what is needed is better than
passing a whole object; an injected interface is better than an import; an event is looser still.
Each step costs something.

**Fully decoupled has a real price.** An event-driven system where a publisher does not know its
consumers is beautifully independent and genuinely hard to follow: you cannot answer "what happens
when an order is placed?" by reading, you have to search for subscribers, and the ordering guarantees
become something you have to think about.

**I would not decouple further if** I could no longer trace a flow by reading. That is a real
threshold and it is the point at which the indirection has stopped paying.

### Over-splitting for cohesion

The same failure as [day 055](../day-055-quickselect/README.md): fifteen classes with one method each
is not high cohesion, it is the responsibility smeared out. High cohesion means related things are
*together*, and the second half of that sentence matters as much as the first.

**I would not split if** the pieces cannot be understood or used independently, or if following one
flow starts to mean opening more files than it saves.

### When a god object is acceptable

Rarely, and it is worth being able to say when. A `Matrix` with forty methods is cohesive — one
reason to change, one set of data, every method genuinely about matrices. A framework's `Request`
object is large and coupled to everything, and splitting it would make every handler take nine
parameters. **Size is not the smell; unrelated reasons to change is the smell.**

### The smells are hints, not rules

Every one of them has legitimate cases:

- **Long parameter list** — a mathematical function with six genuine inputs is fine.
- **Middle man** — an adapter that only forwards is doing the essential job of translating at a
  boundary ([day 059](../day-059-sorting-revision/README.md)).
- **Message chain** — `df.groupby("x").agg("sum").reset_index()` is a fluent interface, not a Demeter
  violation, because each call returns a new object of the same type rather than reaching into
  someone else's internals.
- **Primitive obsession** — a `str` for a name is a `str`. Wrapping every primitive is its own smell.
- **Data clump** — three parameters that travel together twice is a coincidence, not a missing class.
  The rule of three from [day 060](../day-060-hash-tables/README.md) applies here too.

**Naming a smell is the beginning of an argument, not the end of one.** A candidate who says "this is
feature envy, so it's wrong" is weaker than one who says "this is feature envy — the method uses four
fields of `Order` and none of its own, so I'd move it onto `Order`, unless `Order` is in a package
this module shouldn't depend on."

### When not to fix it

**I would not refactor code that nobody touches.** A module with two commits in three years is
finished, whatever its smells, and refactoring it is risk with no return. The version history that
diagnoses the problem also tells you whether it is worth solving.

**I would not fix it during an unrelated change,** because a refactor mixed into a feature commit
cannot be reviewed and cannot be reverted independently.

---

## 8. In the interview

### How it gets asked

- *"Review this module. What would you change?"* — a code sample, and the score is in the vocabulary
  and the priority order.
- *"What is coupling and cohesion?"* — and the good answer is a sentence each plus an example of the
  bad end of both ladders.
- *"What is a code smell? Name a few."* — with the fix attached to each, or it is a list.
- *"One change touches eight files. What is that called and what does it tell you?"* — shotgun
  surgery, and the fix is to gather.
- *"How would you find these problems in a codebase you have just joined?"* — the version history,
  and this is the answer that stands out.

### What to say out loud, in the first ninety seconds

1. **Give the two-sentence framing first.** *"I'll look at two things. Cohesion — do the things in
   this module belong together. And coupling — how much does it have to know about everything else."*
2. **Run the one-sentence test out loud.** *"I can't describe this without 'and': it prices a
   shipment, formats a label, writes to the database, calls a courier and sends an SMS. Five jobs,
   owned by four different teams — that's divergent change."*
3. **Name the specific smells with the evidence, not just the label.** *"Five boolean parameters is
   control coupling — the caller knows about branches inside and is steering them.
   `order.customer.address.city.name` is a message chain, four classes for one line. `line1`, `line2`,
   `city`, `pincode` travelling together is a data clump — that's an `Address` asking to exist."*
4. **Say what you would do first, and why that one.** *"I'd start with `Address`, because it's the
   cheapest change and it removes the message chain, the data clump and part of the label formatting
   in one go."*
5. **Name the evidence you would go and get.** *"And I'd run `git log` on this file. If eleven people
   from four teams have edited it this year, that's the divergent change confirmed rather than
   asserted."*

### The follow-ups

**"One change touches eight files. What's that called, and what does it tell you?"**
Shotgun surgery, and it tells me the knowledge is scattered — one idea is represented in eight places
rather than one, so the coupling between them is implicit and unenforced. The example I have seen most
is an address held as four separate primitives — line one, line two, city, pincode — so adding a
second address line means the model, two forms, a serializer, an invoice template, a shipping label
formatter and four test files: about ten files and sixty lines, and empirically somebody misses two of
them, usually a template and a fixture. The fix is the opposite of the fix for divergent change: here
I *gather*. One `Address` value object that owns its own validation and its own label formatting, so
the second line is eight lines in two files. It is worth naming its opposite in the same breath,
because interviewers often ask them together: divergent change is one file edited for many unrelated
reasons, which is low cohesion in one place, and the fix there is to *split*. So the diagnosis
question is which of the two you have — scattered knowledge, gather it; piled-up knowledge, split it —
and both are visible in the version history rather than being matters of taste.

**"How would you find these problems in a codebase you'd just joined?"**
I would start with the version history, because it is the only source of evidence rather than opinion.
`git log --format='%an' --since=1.year -- <file> | sort -u | wc -l` tells me how many distinct people
edit a file; anything above about five, from more than one team, is divergent change. And going the
other way, looking at recent feature commits and counting the files each one touched finds shotgun
surgery — if adding one field consistently touches eight files, the knowledge for that concept is
scattered. Then a few cheap static checks. I read the import blocks: a file importing both `decimal`
and `smtplib` is doing two jobs, and it takes five seconds to see. I look at the function signatures
without reading the bodies, because data clumps, boolean flags and primitives-that-should-be-types are
all visible there. I grep for message chains — two or more dots between object accesses. And I look at
the test setup, because a test needing thirty lines of scaffolding to check an arithmetic rule tells
me exactly how coupled that rule is to everything else. What I would *not* do is start refactoring
what I found. A module with two commits in three years is finished, whatever its smells, and the same
history that diagnoses the problem tells me whether it is worth solving.

**"What's the difference between coupling and cohesion? People use them interchangeably."**
They are about different directions. Cohesion is *inside* a module: do the things in here belong
together, are they all serving one job. Coupling is *between* modules: how much does this one have to
know about that one. The reason they get conflated is that they usually go wrong together — a module
with low cohesion is doing several jobs, and each job drags in its own dependencies, so its coupling
goes up as well. But you can have one without the other. A perfectly cohesive pricing module that
reads a global config dictionary is highly cohesive and badly coupled. A `utils.py` where every
function is independent and takes exactly its arguments has terrible cohesion and excellent coupling.
The useful part is the ladders. For cohesion, the bottom rungs have names that describe real files:
*coincidental* is `utils.py`, things together for no reason at all; *logical* is grouping by kind
rather than by job — all the validators in one file — which looks tidy and is why those files grow
forever; *temporal* is grouping by when things happen, like an init module. Functional cohesion, the
top, is everything contributing to one job. For coupling the ladder runs from *content* — reaching
into another object's internals — through *common*, shared global state; *control*, passing a flag
that picks a branch inside the callee; *stamp*, passing a whole object when one field is needed; down
to *data*, passing exactly what is needed. The one-line summary: **cohesion is about what is inside,
coupling is about what crosses the boundary, and the goal is high cohesion with low coupling.**

### A model answer

> "I'd look at two things and say them in that order: cohesion, meaning do the things in this module
> belong together, and coupling, meaning how much it has to know about everything else.
>
> On cohesion, my test is whether I can describe it in one sentence without 'and'. I can't. It prices
> a shipment, formats a label, writes a row to the database, calls a courier API and sends an SMS.
> That's five jobs owned by four different teams — finance owns the rate table, design owns the label,
> platform owns persistence — so this file will be edited for four unrelated reasons. That's divergent
> change, and I'd expect `git log` to show a lot of distinct authors on it.
>
> On coupling, three specific things. Five boolean parameters is control coupling: the caller knows
> there are branches inside and is choosing one, so caller and callee change together — and the
> signature allows thirty-two combinations when about six are meaningful, including `express` and
> `international` both true, which is nonsense the code silently ignores. `order.customer.address.
> city.name` is a message chain — one line depending on four classes, so a rename in any of them
> breaks it and testing it means constructing all four. And `CONFIG` as module-level mutable state is
> common coupling; two tests in one process affect each other.
>
> There are two missing concepts underneath most of that. `line1`, `line2`, `city` and `pincode`
> travel together everywhere — that's a data clump, and it's an `Address` asking to exist, with the
> pincode validation and the label formatting on it. And the five flags are really describing what
> kind of shipment this is, which is an enum.
>
> If I could only make one change I'd introduce `Address` first, because it's the cheapest and it
> removes the message chain, the data clump and the label formatting in one go. Then I'd pull the
> pricing out into its own class taking a service, a weight and a value — data coupling, exactly what
> it needs — which makes it testable in three lines instead of thirty-one, without a database.
>
> The thing I'd want to check before doing any of it is the version history. If this file has two
> commits in three years, it's finished and I'd leave it alone whatever it looks like."

---

## 9. Recall card

- **Cohesion is what is *inside* a module; coupling is what *crosses the boundary*.** Aim for high
  cohesion, low coupling. Cohesion ladder (worst→best): **coincidental** (`utils.py`) · **logical**
  (grouped by kind — the kitchen by size) · **temporal** (grouped by when) · … · **functional**.
  Coupling ladder (worst→best): **content** · **common** (globals) · **control** (a flag picking a
  branch) · **stamp** (a whole object for one field) · **data** · message.
- **Two smells are the diagnosis, and they are opposites.** **Shotgun surgery** = one change, many
  files → knowledge is *scattered*, so **gather** it (one `Address` type: 10 files and 60 lines
  becomes 2 files and 8). **Divergent change** = one file, many unrelated reasons → knowledge is
  *piled up*, so **split** it.
- **The named smells, with fixes:** feature envy → move the method to the data · data clump → a
  missing class · primitive obsession → a value object · long parameter list / boolean flags →
  control coupling, use an enum or split · message chain (`a.b.c.d`) → Law of Demeter, ask for what
  you need · middle man · god object · temporal coupling (`configure()` before `run()`).
- **Review in six checks:** read the imports · say it in one sentence with no "and" · count the
  fan-out · read the signatures for clumps and flags · read one test's setup · **run `git log` on the
  file** — 11 authors from 4 teams is divergent change *measured*, not asserted.
- **Coupling cannot be removed, only shaped**, and the smells are hints not rules. A `Matrix` with 40
  methods is cohesive; a fluent `df.groupby().agg()` chain is not a Demeter violation; an adapter
  that only forwards is a legitimate middle man. And **a file with two commits in three years is
  finished** — refactor what changes.
