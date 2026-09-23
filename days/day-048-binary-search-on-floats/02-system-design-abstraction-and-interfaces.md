---
day: 48
track: system-design
title: "Abstraction and interfaces"
phase: "Object-oriented design"
status: written
---

# Day 048 · System design — Abstraction and interfaces

**After today you can:** You can design to an interface so a swap of implementation touches one line.

**The interviewer asks it as:** *How would you make it easy to swap the payment provider later?*

---

## 1. What this is, and why they ask it

An **interface** is a list of operations with no implementation behind them — the shape of a
capability, written down. **Abstraction** is the act of deciding what that list should be: naming
*what* something does and deliberately saying nothing about *how*. A `PaymentGateway` interface says
"you can charge and you can refund"; it does not say Razorpay, it does not say HTTP, and it does not
say what a card token looks like.

They ask the payment-provider question because it is the cleanest test of whether a candidate can
draw a boundary. Everybody knows the words. The differences show up in three specific places: whether
the interface is written in *your* vocabulary or the vendor's, whether the concrete class is chosen
inside the code that uses it or handed in from outside, and whether the candidate can say honestly
when *not* to do this. It also arrives in real work constantly — swapping a payment provider, moving
uploads from disk to S3, replacing one search engine with another — and the difference between a
one-line change and a two-week change is a decision somebody made a year earlier.

---

## 2. The story

Chandran has run a tea shop near the college gate in Thrissur for twenty-two years. Two stoves going
from six in the morning, and he gets through about two gas cylinders a week.

In the monsoon two years ago his usual supplier went to pieces. Deliveries that were promised on
Tuesday came on Friday, and twice they did not come at all, and on one of those days he shut at
eleven in the morning with forty people still coming.

He changed suppliers on the Saturday. It took him one phone call and about ten minutes when the new
man arrived.

Ten minutes, because the neck of a cylinder is the same whoever fills it. The regulator that sits on
top is the same fitting, the rubber tube from the regulator to his stove is the same, and the stove
does not know or care what is written on the side of the cylinder. He unscrewed one, screwed on the
other, checked for a smell, and lit the front burner. Twenty-two years and he has changed supplier
four times, and it has never once meant touching the stove.

The shop two doors down is a smarter place, glass front, and they put in an imported cooking range
about four years ago. Beautiful machine. It came with its own fitting, its own tube, and a
recommendation to use one particular supplier's cylinders, and the man who installed it plumbed it in
that way because that is what the box said.

They cannot change supplier. Not easily. The last time they tried, they were quoted a figure for
re-fitting the whole line that was more than a month's gas, so they paid the higher rate instead and
they are still paying it. The owner told Chandran, quite ruefully, that the range was the best thing
he ever bought and the fitting was the worst decision he ever made, and they were the same purchase.

There is one thing Chandran gives up, and he knows about it. The big commercial cylinders that hotels
use run at a different setting and would burn hotter than his stoves ever do. His fitting cannot
carry that. He decided a long time ago that hotter is not what a tea shop needs — but it is a real
thing he cannot have, and it is the price of the fitting that lets him change his mind about
everything else in ten minutes.

---

## 3. The idea in plain English

The regulator fitting is the interface. Chandran's stove is your application code. The suppliers are
the implementations. The imported range is what happens when code depends on a concrete vendor. And
the commercial cylinder he cannot use is the honest cost of a standard fitting, which §7 makes
explicit.

### The shape of it

Three pieces, always:

```python
from typing import Protocol

class PaymentGateway(Protocol):                   # 1. the fitting: what, not how
    def charge(self, amount: Money, token: str) -> ChargeResult: ...
    def refund(self, charge_id: str, amount: Money) -> RefundResult: ...
```

```python
class RazorpayGateway:                            # 2. one supplier
    def charge(self, amount: Money, token: str) -> ChargeResult:
        ...                                       # HTTP, retries, their error codes

class StripeGateway:                              # another supplier
    def charge(self, amount: Money, token: str) -> ChargeResult:
        ...
```

```python
class Checkout:                                   # 3. the stove: knows only the fitting
    def __init__(self, gateway: PaymentGateway) -> None:
        self._gateway = gateway                   # handed in, not chosen here

    def pay(self, order: Order, token: str) -> None:
        result = self._gateway.charge(order.total, token)
        ...
```

`Checkout` contains the word "Razorpay" exactly zero times. That is the property to check, and it is
checkable with `grep`.

### The part everyone gets wrong: who chooses

Here is the same code with one thing changed, and it undoes everything:

```python
class Checkout:
    def __init__(self) -> None:
        self._gateway = RazorpayGateway()         # <-- chosen INSIDE
```

Now `Checkout` names a concrete class, so `Checkout` depends on Razorpay, so swapping the provider
means editing `Checkout` — and every test of `Checkout` makes a real network call. The interface
bought nothing.

Passing the dependency in from outside is called **dependency injection**, and stripped of the
ceremony it means: *the thing that uses a capability does not choose which implementation it gets;
whoever builds it does.*

```python
# one place in the whole program, at start-up
gateway = StripeGateway(api_key=settings.STRIPE_KEY)     # <-- the one line that changes
checkout = Checkout(gateway)
```

That is the answer to the interviewer's question, and it is one line.

There is a deeper name for the shape, which you will meet properly in the SOLID phase from
[day 055](../day-055-quickselect/README.md): **depend on abstractions, not on concretions.** Say the
plain version instead — *the code that uses a thing should name the capability, not the vendor.*

### The leaky abstraction

This is where good answers separate from great ones. An interface can be present in form and useless
in substance:

```python
class PaymentGateway(Protocol):
    def charge(self, intent: stripe.PaymentIntent) -> stripe.Charge: ...
```

The fitting is bolted to one supplier's shape. Any other implementation has to construct a Stripe
object to satisfy it, and `Checkout` now imports `stripe` to build the argument. The interface exists
and the coupling is unchanged.

**The rule: the interface speaks your vocabulary, not the vendor's.** Define your own small types —
`Money`, `ChargeResult`, `PaymentError` — and let each implementation translate at its own edge. The
translation is real work and it is exactly the work you are paying for.

The leak has three usual forms, and all three are worth being able to name:

- **Types.** Vendor classes in the signature, as above.
- **Errors.** `except stripe.CardError` appearing in your business logic. Each implementation must
  catch its own exceptions and raise yours.
- **Semantics.** A method called `capture()` because Stripe has authorise-then-capture, when your
  application only ever charges once. You have modelled their workflow, not yours.

### Interfaces in Python: three ways

```python
# 1. duck typing -- nothing declared at all
def pay(gateway, amount): gateway.charge(amount)
```

Works. Nothing checks that `gateway` has `charge` until the call runs.

```python
# 2. abstract base class -- inheritance, checked at construction
from abc import ABC, abstractmethod
class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: Money, token: str) -> ChargeResult: ...
```

A subclass missing `charge` cannot be instantiated: `TypeError: Can't instantiate abstract class`.
Good when you also want to share a little default behaviour, and when you want the failure to be
loud.

```python
# 3. Protocol -- structural, checked by a type checker, no inheritance
from typing import Protocol
class PaymentGateway(Protocol):
    def charge(self, amount: Money, token: str) -> ChargeResult: ...
```

Any class with a matching `charge` satisfies it, with no import and no base class. `mypy` verifies it
before the program runs. This is the modern default, and it has one property that matters for
third-party code: **you can write a Protocol for a class you do not own**, which an abstract base
class cannot do.

### Keep the interface small

A `PaymentGateway` with fourteen methods forces every implementation to stub the nine it does not
support, and each stub is a lie waiting to be called. Two or three methods per interface is normal;
if half the implementers raise `NotImplementedError` on half the methods, the interface is two
interfaces. That instinct has a name too — interface segregation — and it arrives on
[day 059](../day-059-sorting-revision/README.md).

### The test that stops you over-doing it

Before writing an interface, ask: **can I name the second implementation?**

```
PaymentGateway     -> Razorpay and Stripe, both real. Interface.
FileStorage        -> local disk and S3, both real. Interface.
OrderRepository    -> Postgres and... an in-memory fake for tests. Counts, and it is
                      the commonest legitimate "second implementation".
InvoiceNumberer    -> there is one way to number an invoice. No interface.
```

An in-memory fake for tests is a genuine second implementation, and it is the one people forget. If
your only justification is "we might swap it one day", that is speculation, and
[day 043](../day-043-binary-search-without-bugs/README.md)'s warning applies: an interface with one
implementation is a layer with no payoff.

---

## 4. The picture

The fitting, and the code:

```
     CHANDRAN'S SHOP                        YOUR APPLICATION

        [ stove ]                              [ Checkout ]
            |                                       |
     rubber tube (fixed)                  depends on PaymentGateway
            |                                       |
   +--- REGULATOR FITTING ---+          +---- interface: charge / refund ----+
   |     (the standard)      |          |     in YOUR vocabulary             |
   +-------------------------+          +------------------------------------+
        |        |        |                  |          |            |
   supplier   supplier  supplier         Razorpay    Stripe    FakeGateway
      A          B         C                                   (for tests)

  changing supplier: unscrew,        changing provider: one line where
  screw on, 10 minutes               the object is constructed
```

**What to notice:** the fitting is in the middle and belongs to *neither* side. It is not the stove's
and it is not the supplier's. An interface written in the vendor's types has quietly moved the
fitting onto the supplier, which is the imported range two doors down.

Where the dependency points, before and after:

```
 BAD                                    GOOD

 Checkout ---------> RazorpayGateway    Checkout -------> PaymentGateway
   (imports it, constructs it)                                  ^
                                                                |
                                                        RazorpayGateway
                                                        StripeGateway
                                                        FakeGateway

 the arrow goes from your code          the arrows go from the vendors
 to the vendor                          to your interface

 -> swapping means editing Checkout     -> swapping means one line at start-up
 -> testing means a network call        -> testing means passing a fake
```

**What to notice:** the arrows reversed. Before, your code pointed at a vendor; after, three vendors
point at a thing you own. That reversal is the whole of "depend on abstractions".

---

## 5. How it actually works

### The wiring, in full

```python
# gateways/base.py -- yours, and nothing vendor-shaped in it
@dataclass(frozen=True)
class ChargeResult:
    charge_id: str
    succeeded: bool
    failure_reason: str | None = None

class PaymentError(Exception): ...
class CardDeclined(PaymentError): ...

class PaymentGateway(Protocol):
    def charge(self, amount: Money, token: str) -> ChargeResult: ...
    def refund(self, charge_id: str, amount: Money) -> ChargeResult: ...
```

```python
# gateways/razorpay.py -- the translation lives HERE, at the edge
class RazorpayGateway:
    def charge(self, amount: Money, token: str) -> ChargeResult:
        try:
            r = self._client.payment.capture(token, int(amount.paise))
        except razorpay.errors.BadRequestError as exc:
            if exc.code == "CARD_DECLINED":
                raise CardDeclined(str(exc)) from exc      # THEIR error -> YOURS
            raise PaymentError(str(exc)) from exc
        return ChargeResult(charge_id=r["id"], succeeded=r["status"] == "captured")
```

Three translations happen in that method, and all three are the point: their units (paise as an int),
their errors (`BadRequestError` becomes `CardDeclined`), and their vocabulary (`capture` becomes
`charge`). Every one of them would otherwise leak into your business logic.

```python
# app.py -- the composition root: the one place that names concrete classes
def build_checkout(settings) -> Checkout:
    gateway = {
        "razorpay": lambda: RazorpayGateway(settings.RAZORPAY_KEY),
        "stripe":   lambda: StripeGateway(settings.STRIPE_KEY),
        "fake":     FakeGateway,
    }[settings.PAYMENT_PROVIDER]()
    return Checkout(gateway)
```

That function is called the **composition root**. Every concrete class in the program is named here
and nowhere else, and "swap the provider" becomes a change to one configuration value.

### The interfaces you already depend on

- **Python's DB-API (PEP 249).** `psycopg`, `mysqlclient` and `sqlite3` all expose `connect`,
  `cursor`, `execute`, `fetchall`. Code written against it moves between databases without changing,
  and this is exactly why SQLAlchemy can support eight backends.
- **File-like objects.** `open()`, `io.StringIO`, `gzip.open`, a socket — all support `read` and
  `write`, so `json.load(f)` accepts any of them. No base class enforces it; it is duck typing
  standardised by convention.
- **Django's `Storage`.** `FileSystemStorage` and `S3Boto3Storage` implement `save`, `open`, `url`,
  `delete`. Moving uploads to S3 is `DEFAULT_FILE_STORAGE = "..."` in settings.
- **`logging.Handler`.** One `emit` method, and every destination in the ecosystem behind it.
- **JDBC in Java, and Kubernetes' CSI** for storage drivers — the same idea at the scale of a whole
  industry: a standard fitting so that vendors compete behind it.

### Testing, which is the payoff nobody mentions in the question

```python
class FakeGateway:
    def __init__(self) -> None:
        self.charges: list[tuple[Money, str]] = []
        self.next_result = ChargeResult("fake_1", succeeded=True)

    def charge(self, amount: Money, token: str) -> ChargeResult:
        self.charges.append((amount, token))
        return self.next_result
```

```python
def test_declined_card_leaves_order_unpaid():
    gateway = FakeGateway()
    gateway.next_result = ChargeResult("", succeeded=False, failure_reason="declined")
    checkout = Checkout(gateway)
    ...
```

Testing a declined card against a real provider means a sandbox account, a magic card number, network
access, and a test that fails when their sandbox is down. With the fake it is two lines and runs in
microseconds. **In practice this is the reason most interfaces earn their keep**, and it is the second
implementation that always exists.

---

## 6. The numbers

### The cost of a swap, counted in files

```
concrete dependency (Checkout constructs RazorpayGateway):
    every file that constructs a Checkout            ~6-15 files
    every test that mocks the gateway                ~20-40 tests
    every place that catches razorpay.errors.*       ~5-10 files
    error-handling semantics scattered               unknown until grep
                                                    -----
                                                     ~30-60 edits, over 1-2 weeks

interface + injection:
    write StripeGateway implementing 2 methods       1 new file, ~80 lines
    change the composition root                      1 line
                                                    -----
                                                     1 new file, 1 line
```

That is the number to quote. **Thirty to sixty edits against one new file and one line**, and the
first version's edits are all in code that currently works.

### The grep test

A one-command health check you can name in an interview:

```
grep -rn "razorpay\|stripe" src/ --include=*.py | grep -v "src/gateways/"

    a healthy codebase:   0 results
    a leaky one:          every result is a place the swap will break
```

Run it on the imports too. If `stripe` is imported outside the adapter directory, the abstraction has
a hole in it at that line.

### Test speed, which compounds

```
40 checkout tests against a provider sandbox:
    ~400 ms each (network round trip + their latency)  = 16 seconds
    plus flakiness: ~2% failure rate from their side   = 1 failed run in every few

40 checkout tests against FakeGateway:
    ~0.2 ms each                                       = 8 milliseconds
    flakiness: 0

2,000x faster, and deterministic.
```

### The cost of building the abstraction

Be honest about this side too:

```
the interface + one adapter + one fake:
    interface + your own types      ~40 lines
    the adapter (translation)       ~80 lines
    the fake                        ~25 lines
                                    ---------
                                    ~145 lines, half a day

worth it when: a second implementation exists or is near-certain, OR the tests need a fake.
not worth it when: one implementation, no test need, no named second candidate.
```

---

## 7. The trade-offs

### An abstraction against direct use

Every interface is a layer: one more file to open when reading, one more indirection when debugging.
*I would not put an interface in front of something with exactly one implementation and no test
need.* The trigger is the second implementation — and an in-memory fake for tests counts as one, which
is why so many repositories legitimately get an interface on day one.

### A common interface against each provider's best features

This is Chandran's commercial cylinder, and it is the trade-off candidates most often miss. An
interface can only expose what all its implementations can do. Stripe has authorise-then-capture;
Razorpay's flow differs; a fitting that spans both offers neither in full. *I would not force a
single interface over two providers whose models genuinely differ* — I would either narrow the
interface to the part that really is common and let the rest be provider-specific code behind a
feature check, or accept two interfaces. Pretending they are the same is how you get a `capture()`
method that means two different things.

### A leaky interface against the translation work

Writing your own `Money`, `ChargeResult` and error types is real work, and using the vendor's types is
free today. *I would not put a vendor type in an interface signature*, because the moment it is there
the interface has stopped being yours and the swap is back to being a two-week job. The translation
at the adapter's edge is the price of the fitting.

### Hiding against debuggability

A good abstraction hides the provider — including its error messages, its retry behaviour and its
rate limits. *I would not swallow provider detail entirely*: I would keep the original exception as
the cause (`raise CardDeclined(...) from exc`) and log the provider's request id, so an on-call
engineer can still find the transaction in the vendor's dashboard. An abstraction that makes
production incidents harder to diagnose has been drawn too tightly.

### The honest sentence

> An interface is not free and it is not automatically good. It is a bet that this capability will
> have more than one implementation, and the way to check the bet is to name the second one out loud.
> If you can, draw the boundary in your own vocabulary and put every vendor word behind it. If you
> cannot, write the concrete class and wait.

---

## 8. In the interview

### How it gets asked

- *"How would you make it easy to swap the payment provider later?"* — the direct form, and the answer
  ends with "one line at start-up".
- *"We store uploads on disk. How would you move to S3 without a rewrite?"* — the same question about
  files, and Django's `Storage` is the reference answer.
- *"How do you test this without calling the real API?"* — the same idea approached from testing,
  which is usually the honest reason the interface exists.
- *"What's the difference between abstraction and encapsulation?"* — the vocabulary version.
  Encapsulation hides *data* from callers; abstraction hides *how* behind a named capability.

### What to say out loud, in the first ninety seconds

1. **Name the capability, not the vendor.** *"I'd define a `PaymentGateway` interface with two
   methods — charge and refund — and my code would depend on that, never on Razorpay directly."*
2. **Say the vocabulary rule immediately.** *"Crucially, the interface is in my vocabulary, not
   theirs. My own `Money` type, my own `ChargeResult`, my own `PaymentError` hierarchy. No vendor
   class ever appears in a signature."*
3. **Say who chooses.** *"`Checkout` doesn't construct a gateway — it takes one in its constructor. The
   concrete class is named in exactly one place, at start-up. That's the line that changes when we
   swap."*
4. **Say where the translation lives.** *"Each adapter translates at its own edge: their error codes
   into my exceptions, their units into my `Money`. That translation is the work I'm paying for, and
   it's what stops their model leaking in."*
5. **Give the number.** *"Concretely: swapping goes from thirty-odd edits across the codebase to one
   new file and one line."*
6. **Name the cost, unprompted.** *"The trade is that the interface can only expose what both
   providers do. If one has authorise-then-capture and the other doesn't, I'd rather narrow the
   interface than fake a shared model."*

### The follow-ups

**"How do you stop the abstraction leaking?"**
Three specific ways, and I'd check all three because they fail independently. First, types: no vendor
class in any signature. If `charge` takes a `stripe.PaymentIntent`, then every other implementation
has to construct a Stripe object to satisfy the interface, and my `Checkout` imports `stripe` to build
the argument — the interface exists and the coupling is untouched. So I define `Money`,
`ChargeResult` and a `PaymentError` hierarchy of my own. Second, errors: `except stripe.CardError`
must never appear in business logic. Each adapter catches its provider's exceptions and re-raises
mine, keeping the original as `__cause__` so the stack trace still helps on-call. Third, semantics: I
would not add a `capture()` method just because one provider distinguishes authorise from capture — a
method that means two different things behind two adapters is worse than no method. The check I'd
actually run is a grep: search the source for the provider's name outside the adapter directory, and
if it returns anything, that line is where the swap will break. A healthy codebase returns nothing.

**"Isn't this over-engineering when you only have one provider?"**
It can be, and I would apply a test rather than a rule: can I name the second implementation? For a
payment gateway I usually can, and not because of vendor risk — the second implementation is the fake
I need for tests. Testing a declined card, a timeout and a partial refund against a real sandbox means
network access, magic card numbers, and a suite that fails when their sandbox is down. With a fake
it's two lines per case and runs in microseconds — forty tests going from sixteen seconds and flaky to
eight milliseconds and deterministic. That alone usually justifies the roughly 145 lines of interface,
adapter and fake. Where I would *not* do it is a capability with one implementation and no test need —
an invoice numberer, a slug generator. And I'd be honest that if my only argument is "we might swap it
one day", that is speculation, and I'd write the concrete class and extract the interface when the
second implementation actually arrives, which is a mechanical refactor rather than a rewrite.

**"What if the two providers genuinely work differently — one has authorise-then-capture and the other
doesn't?"**
Then I stop pretending they are the same, because an interface that spans two different models ends up
offering neither properly. There are three honest options and I'd pick between them explicitly. One:
narrow the interface to what is genuinely common — `charge` and `refund` — and treat
authorise-then-capture as a capability that lives outside it, reached through a separate, optional
protocol that only some adapters satisfy, with a check before use. Two: widen the interface to the
richer model and make the simpler provider's adapter emulate it — authorise becomes a no-op that
records intent, capture does the real charge. That works only if the emulation is honest; if a failure
can happen at capture time on one provider and not the other, the emulation is a lie and I would not
ship it. Three: accept that these are two interfaces for two different kinds of provider, and let the
application choose at a higher level. What decides it is whether my *application* needs the richer
model. If checkout only ever charges once, option one is right and the extra capability is not my
problem. This is the same trade Chandran makes with his gas fitting: the standard fitting cannot carry
the hotter commercial cylinder, and that is a real thing given up in exchange for being able to change
supplier in ten minutes.

### A model answer

> "The goal is that swapping the provider is a configuration change, not a code change, and there are
> three things that get me there.
>
> First, I define the capability in my own vocabulary. A `PaymentGateway` interface — a Protocol in
> Python — with two methods: `charge(amount: Money, token: str) -> ChargeResult` and `refund`. My own
> `Money` type, my own `ChargeResult`, my own `PaymentError` and `CardDeclined` exceptions. No vendor
> class ever appears in a signature, because the moment it does the interface belongs to that vendor
> rather than to me.
>
> Second, each provider gets an adapter that implements it, and the adapter is where all the
> translation happens: their units into my `Money`, their error codes into my exceptions, their
> workflow vocabulary into mine. That translation is the actual work, and doing it at the edge is what
> stops their model spreading into my business logic. I'd keep the original exception as the cause so
> the vendor's request id is still in the trace when something goes wrong at 3am.
>
> Third, and this is where most designs fail — `Checkout` does not construct a gateway. It takes one
> in its constructor. The concrete class is named in exactly one place, a composition root at
> start-up, which reads the provider from settings. That's the one line that changes.
>
> ```python
> class Checkout:
>     def __init__(self, gateway: PaymentGateway) -> None:
>         self._gateway = gateway
> ```
>
> The check I'd run to prove it worked: grep the source for the provider's name outside the adapter
> directory. If that returns nothing, the swap is one file and one line. If it returns anything, every
> hit is a place the swap will break — and in a codebase where `Checkout` constructs the gateway
> itself, that's typically thirty to sixty edits across a week or two.
>
> The reason I'd do this even with one provider is the fake. A `FakeGateway` is the second
> implementation, and it turns forty checkout tests from sixteen flaky seconds against a sandbox into
> eight deterministic milliseconds, including cases like a declined card that are genuinely awkward to
> trigger for real.
>
> And the cost, since there is one: the interface can only offer what all the implementations can do.
> If one provider has authorise-then-capture and the other doesn't, I'd narrow the interface to what's
> genuinely common rather than fake a shared model — and if my application ever really needs the
> richer flow, that's a deliberate decision to make then, not something to paper over now."

---

## 9. Recall card

- **Interface = the capability, in *your* vocabulary.** Your `Money`, your `ChargeResult`, your
  exceptions. A vendor type in a signature means the interface belongs to the vendor and bought
  nothing.
- **The user must not choose the implementation.** `Checkout(gateway)`, never
  `self._gateway = RazorpayGateway()`. Concrete classes are named once, in a composition root — that
  is the one line that changes.
- **The adapter translates at its own edge:** their units → your types, their errors → your
  exceptions (`raise CardDeclined(...) from exc`), their workflow words → yours. Three leak types:
  types, errors, semantics.
- **The test before writing one: can you name the second implementation?** An in-memory **fake for
  tests** counts, and is usually the real reason — 40 tests from 16 flaky seconds to 8 deterministic
  milliseconds.
- **Numbers and the check:** swap cost 30-60 edits → 1 file + 1 line;
  `grep -rn "stripe" src/ --exclude-dir=gateways` should return nothing. **The cost:** an interface
  offers only what *all* implementations can do — narrow it honestly rather than fake a shared model.
