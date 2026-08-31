---
day: 91
track: system-design
title: "Design a logging framework"
phase: "Low-level design case studies"
status: written
---

# Day 091 · System design — Design a logging framework

**After today you can:** You can design log levels, appenders and formatters as replaceable parts.

**The interviewer asks it as:** *Design a logging library. How do I add a new destination?*

---

## 1. What this is, and why they ask it

A logging framework takes a message from anywhere in a program and gets it to zero or more
destinations — a file, the console, a network collector — in a chosen format, if it is important
enough to bother with.

The question in the prompt is the easy half: adding a destination should be **one class and one line
of configuration**, and that is a `Handler` interface with an obvious set of implementations.

The half that decides whether the design is any good is the word **"if"**. A logging call that produces
nothing must cost almost nothing, because there are hundreds of thousands of them a second and most of
them are switched off. That single requirement drives the most important API decision in the whole
library: **the level check must happen before the message is built**, which is why
`logger.debug("user %s failed", user_id)` is right and `logger.debug(f"user {user_id} failed")` is
wrong — the f-string is evaluated whether or not anybody wants it.

They ask it because everybody uses logging and almost nobody has looked at how it works, because
"where it goes" and "what it looks like" being two separate interfaces is a clean example of
orthogonal design, and because the follow-ups — asynchronous writing, what happens on a crash, and how
you find one request among a billion lines — are real operational problems with real answers.

---

## 2. The story

Kumar has run security at the tyre factory since 2011, forty-one people across three shifts.

The rule when he joined was that everything went to the manager. Every gate entry, every vehicle,
every visitor, every torch that needed a new battery. The manager's phone rang about sixty times a
night, and by the third month he had simply stopped answering it, which meant the four calls that
mattered did not get through either.

What they have now is three levels, and Kumar can recite them.

Routine things go into the shift record and nobody is disturbed. A vehicle in at 2:40, out at 3:15.
Nobody reads it, most nights. It is there for the mornings when somebody asks.

Things that are unusual but not dangerous go to the shift manager on the intercom. A lorry arriving
without paperwork. A man at the gate saying he is from the electricity office.

And then the siren, which Kumar has sounded four times in fourteen years.

The part he has had to teach every new supervisor is a different thing, and he had to tell Ravi three
times.

Ravi joined last year. He is careful and he writes beautifully, and he was spending fifteen minutes at
the end of every round composing a full account of what had happened — times, names, vehicle numbers,
the state of the lights on the east side — and then reading all of it into the shift record, where
nobody would ever look at it.

Kumar's objection was not that the record is useless. It was that Ravi was doing the writing *first*
and finding out afterwards that nobody wanted it. **Ask what level a thing is before you spend fifteen
minutes describing it.** Routine gets one line. If somebody is going to act on it, then take the time
and write it properly.

The other change was who keeps the record. The gate has its own now, and the loading bay has its own,
and both also feed up into the factory record. So when there was a problem at the loading bay in
March, Kumar could say "turn everything up at the loading bay" and read every detail from there,
without wading through four weeks of routine gate entries to find it.

---

## 3. The idea in plain English

Kumar's three levels are **log levels**. Ravi writing before checking is the **lazy formatting**
problem, and it is the most expensive mistake in logging. And the gate having its own record that also
feeds upward is the **logger hierarchy**.

### The pieces, and why there are four of them

- **`Logger`** — what your code calls. Named, hierarchical: `app.payments.stripe`.
- **`LogRecord`** — one event: level, message, arguments, timestamp, logger name, and the context
  around it.
- **`Handler`** *(interface)* — **where** it goes. Console, file, rotating file, network, database.
- **`Formatter`** *(interface)* — **what it looks like**. Plain text, JSON, one line, multi-line.
- **`Filter`** *(optional interface)* — a last say on whether this particular record passes.

**`Handler` and `Formatter` are separate on purpose**, and that separation is the answer to "how do I
add a destination". They vary independently: you may want JSON to a file and plain text to the
console, or the same format to three destinations. Combining them gives you `JsonFileHandler`,
`TextFileHandler`, `JsonNetworkHandler` and so on — **N × M classes instead of N + M.**

Adding a destination is then exactly one class implementing one method, plus one line of wiring. That
is the whole answer to the prompt, and it takes ten seconds to say.

### Levels, and the one that matters

```
 DEBUG      what I need when I am debugging this   — off in production
 INFO       normal, notable events                 — on
 WARNING    something is odd but handled           — on
 ERROR      an operation failed                    — on, and someone should see it
 CRITICAL   the process cannot continue            — on, and it wakes somebody up
```

Kumar's shift record, intercom and siren, with two extra gradations.

A level is just an integer, so "is this enabled?" is one comparison. That cheapness is the point, and
it leads directly to the important part.

### The expensive mistake: building a message nobody wants

```python
    logger.debug(f"processing order {order.id} for {user.name}: {order.to_dict()}")
```

The f-string is evaluated **before** `debug` is called. Python has no choice — arguments are evaluated
first. So `order.to_dict()` runs, a string is built, and *then* the logger looks at the level and
throws it all away.

```python
    logger.debug("processing order %s for %s: %s", order.id, user.name, order.to_dict)
```

Now the formatting is deferred: the logger checks the level first, and only if the record will actually
be emitted does it do the `%` substitution. The arguments are still evaluated — `order.to_dict` is
passed as a *function*, not called — which is the trick for genuinely expensive values.

**Ravi writing his fifteen-minute account before asking whether anyone wanted it.**

The numbers in §6 make this concrete, and they are startling: with an expensive argument, suppressed
debug logging can burn several cores doing nothing at all.

And when the argument is genuinely costly to compute even lazily:

```python
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("state: %s", expensive_dump())
```

Ugly, and correct, and worth doing in the three places per system where it matters.

### The hierarchy, which is what makes logging usable in production

Loggers are named with dots and form a tree:

```
 root
 └── app
     ├── app.payments
     │   └── app.payments.stripe
     └── app.orders
```

A record logged to `app.payments.stripe` is offered to that logger's handlers, then **propagates
upward** to `app.payments`, then `app`, then the root — each of which may have its own handlers and its
own level.

That is [day 074](../day-074-deques-and-window-max/README.md)'s chain of responsibility, with one
difference worth naming: **in a chain, the first able handler stops the walk; here every level gets
it.** So it is a chain in structure and a broadcast in behaviour, unless somebody sets
`propagate = False` to cut it — which is the `stopPropagation` of the logging world.

Why it matters: you can raise the volume on **one subsystem** without drowning in everything else.
`app.payments.stripe` at DEBUG, everything else at INFO, one line of configuration, no code change,
no redeploy if the configuration is reloadable. Kumar turning everything up at the loading bay.

### Structured logging, because grep does not scale

```python
    logger.info("payment failed for order %s", order_id)                   # a sentence
    logger.info("payment_failed", order_id=order_id, amount=amount,
                provider="razorpay", attempt=2)                            # a record
```

The first is readable by a person and useless to a machine: finding "all failed payments over ₹10,000
for Razorpay last Tuesday" means regular expressions over terabytes. The second is a dictionary, so
the same question is a query.

**Log events, not sentences.** The message becomes a stable event name and everything variable becomes
a field — which also means the message text can be changed without breaking every dashboard built on
it.

### Context, and the field that matters most

One request produces twenty log lines from ten different modules, and in a system doing ten thousand
requests a second those two hundred thousand lines a second are interleaved. Without a shared
identifier, reconstructing one request is impossible.

So every record carries a **correlation id** — generated at the edge, stored in a context variable, and
attached automatically by the framework rather than passed through every function signature.

```python
    request_id = ContextVar("request_id")     # per-task, not per-thread; asyncio-safe
```

**This is the single most valuable field in a log line**, and it costs one middleware and one
`ContextVar`. Without it, logs are a stream of unrelated sentences.

### Asynchronous writing, and what it trades

A synchronous handler writes on the calling thread. If the destination is a file that is fine; if it is
a network collector, a slow collector now makes your request handler slow, and a hung one hangs it.

So real systems put a **queue** between the logger and the handler: the caller appends and returns, and
a background thread drains it. That decouples the application from the destination, and it introduces
two genuine costs:

- **Loss on crash.** Anything still in the queue when the process dies is gone — which is exactly the
  moment you most want the logs. Mitigate by flushing on shutdown and by writing CRITICAL synchronously.
- **A bounded queue must drop.** If the consumer cannot keep up, you either block the application
  (which is what you were avoiding) or discard records. Dropping is usually right, and **it must be
  counted and reported**, or you are silently missing data.

**Blocking is a correctness disaster and dropping is a data problem.** Choose dropping, count the
drops, and alert on them.

---

## 4. The picture

The two orthogonal interfaces, which is the answer to the prompt:

```
                        +---------------+
   logger.info(...) --> |    Logger     |  level check FIRST
                        +---------------+
                                |  (only if enabled)
                                v
                        +---------------+
                        |   LogRecord   |  level, message, args, time, name, context
                        +---------------+
                                |
              +-----------------+-----------------+
              v                 v                 v
        ConsoleHandler    RotatingFile      NetworkHandler     <- WHERE
              |                 |                 |
        TextFormatter     JsonFormatter     JsonFormatter      <- WHAT IT LOOKS LIKE

   two interfaces, N + M classes.
   combined, it would be N x M: JsonFileHandler, TextFileHandler, JsonNetworkHandler, ...
```

The hierarchy and propagation:

```
   app.payments.stripe   level DEBUG   handlers: [file]
            |  propagate
            v
   app.payments          level INFO    handlers: []
            |  propagate
            v
   app                   level INFO    handlers: [console]
            |  propagate
            v
   root                  level WARNING handlers: [network]

   a DEBUG record from app.payments.stripe:
     - passes that logger's level (DEBUG)     -> written to the file
     - propagates up; app's console handler has its own level check
     - reaches root; the network handler decides for itself

   turn one subsystem up without touching anything else — one line of config.
   `propagate = False` on any node cuts the chain there.
```

And the expensive mistake, drawn as what actually executes:

```
 logger.debug(f"order {order.id}: {order.to_dict()}")

   1. order.to_dict()      <- RUNS. Always. Even at INFO level.
   2. build the string     <- RUNS
   3. call debug()
   4. check the level      <- "not enabled"
   5. discard everything from steps 1 and 2

 logger.debug("order %s: %s", order.id, order.to_dict)

   1. call debug() with a function reference   <- nothing is computed
   2. check the level -> not enabled -> RETURN
   ---------------------------------------------
   steps 1 and 2 of the first version never happen
```

---

## 5. How it actually works

### Move 1 · Clarify (minutes 0–5)

> **"Library for other people, or the logging inside one service?"** — A library, so the API and the
> extension points matter more than the destinations.
> **"Structured or free text?"** — Structured, and I would push for it, because grep does not scale.
> **"How much volume?"** — This decides synchronous versus asynchronous and whether sampling is needed.
> **"Must a log line ever be guaranteed to survive a crash?"** — Because that decides whether anything
> is written synchronously.

> "I will assume one process with several threads, that destinations may be slow, and that we want to
> be able to change levels without redeploying. I am not designing the collector, the storage or the
> query layer."

### Move 2 · The nouns (minutes 5–10)

- **`Level`** — an `IntEnum`, so comparison is one integer comparison.
- **`LogRecord`** — frozen: level, event, fields, timestamp, logger name, context.
- **`Logger`** — named, hierarchical, holds a level and a list of handlers.
- **`Handler`** *(interface)* — where. Console, file, rotating file, network, null.
- **`Formatter`** *(interface)* — what it looks like. Text, JSON.
- **`Filter`** *(interface)* — an optional final say, for sampling and rate limiting.
- **`LogManager`** — the registry of loggers, so `get_logger("a.b")` returns the same object each time.

Seven, three interfaces — and all three pass the gate, because "console and file", "text and JSON",
and "sample and rate-limit" are each two real implementations somebody wants.

### Move 3 · The hot path, where the level check comes first

```python
class Logger:
    def log(self, level: Level, event: str, *args, **fields) -> None:
        if level < self._effective_level():        # THE FIRST THING. One int comparison.
            return
        record = LogRecord(
            level=level, event=event, args=args, fields=fields,
            timestamp=time.time(), logger=self._name,
            context=dict(_context.get({})),        # correlation id, user id, ...
        )
        self._dispatch(record)
```

**The level check is the first statement in the method**, and everything expensive — building the
record, reading the context, formatting — is after it. A suppressed call is one comparison and a
return.

```python
    def debug(self, event: str, *args, **fields) -> None:
        self.log(Level.DEBUG, event, *args, **fields)
```

And the API is `debug(event, *args)` rather than `debug(message)` **precisely so that callers can defer
formatting**. The signature is the mechanism: if the only parameter were a finished string, there would
be no way for a caller to avoid building it.

### Move 4 · The effective level and propagation

```python
    def _effective_level(self) -> Level:
        """Walk up the hierarchy until a level is explicitly set."""
        logger = self
        while logger is not None:
            if logger._level is not None:
                return logger._level
            logger = logger._parent
        return Level.WARNING                       # the root default
```

Inheriting the level rather than copying it is what makes "set `app` to DEBUG" affect every logger
underneath without touching them.

```python
    def _dispatch(self, record: LogRecord) -> None:
        logger = self
        while logger is not None:
            for handler in logger._handlers:
                if handler.level <= record.level and handler.passes_filters(record):
                    handler.emit(record)           # EVERY level gets it, not just the first
            if not logger._propagate:
                break                              # stopPropagation
            logger = logger._parent
```

Point at the difference from a plain chain of responsibility: **every ancestor's handlers run, not just
the first that can.** It is a chain in structure and a broadcast in behaviour, and `propagate = False`
is the escape.

Each handler also has **its own level**, which is what lets a file capture DEBUG while the console
shows only WARNING from the same logger.

### Move 5 · The two interfaces

```python
class Formatter(Protocol):
    def format(self, record: LogRecord) -> str: ...


class JsonFormatter:
    def format(self, record: LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.timestamp, UTC).isoformat(),
            "level": record.level.name,
            "logger": record.logger,
            "event": record.event,
            **record.context,                      # correlation id and friends
            **record.fields,
        }
        return json.dumps(payload, default=str)     # default=str: never raise on a bad value
```

`default=str` is a small, real decision: **a logger must never raise.** A value that will not serialise
should degrade to its `repr`, not take down the request it was describing.

```python
class Handler:
    def __init__(self, formatter: Formatter, level: Level = Level.DEBUG) -> None:
        self.formatter, self.level = formatter, level
        self._filters: list[Filter] = []

    def emit(self, record: LogRecord) -> None:
        raise NotImplementedError


class FileHandler(Handler):
    def emit(self, record: LogRecord) -> None:
        try:
            self._stream.write(self.formatter.format(record) + "\n")
        except Exception:
            _handle_internal_error()               # never propagate to the caller
```

**Adding a destination is this class with one method.** That is the answer to the prompt, and the
`try` is the second half of "a logger must never raise": a full disk must not turn into an exception
in unrelated business code.

### Move 6 · Asynchronous emission

```python
class QueueHandler(Handler):
    """Hand off to a background thread so a slow destination cannot slow the caller.

    Bounded, and it DROPS rather than blocks — blocking would reintroduce
    exactly the coupling this exists to remove. Drops are counted, because a
    silent drop is worse than a slow log.
    """

    def __init__(self, target: Handler, capacity: int = 10_000) -> None:
        self._queue: queue.Queue[LogRecord] = queue.Queue(maxsize=capacity)
        self._dropped = 0
        threading.Thread(target=self._drain, args=(target,), daemon=True).start()

    def emit(self, record: LogRecord) -> None:
        try:
            self._queue.put_nowait(record)
        except queue.Full:
            self._dropped += 1                     # counted and reported, never silent
```

And the two mitigations, stated together: **flush on shutdown**, and **write CRITICAL synchronously**,
because the records you most want are the ones written just before the process died.

### Move 7 · Sampling, for the line that fires a million times

```python
class SampleFilter:
    """Keep 1 in N of a noisy event. Applied per event name, not globally —
    you want all the errors and one percent of the cache hits."""

    def __init__(self, rate: float) -> None:
        self._rate = rate

    def passes(self, record: LogRecord) -> bool:
        if record.level >= Level.ERROR:
            return True                            # never sample away an error
        return random.random() < self._rate
```

The `level >= ERROR` line is the important one. Sampling that discards errors is a way of losing
exactly the information you were collecting logs for.

### Real systems

- **Python's `logging`** is this design: hierarchical dotted loggers, propagation, handlers and
  formatters as separate objects, per-handler levels, and `logging.QueueHandler` for the async case.
  The `%`-style deferred formatting exists for the reason in §3, which is why linters warn about
  f-strings in log calls.
- **Log4j / Logback / SLF4J** in Java use the same shapes with different names — *appenders* instead of
  handlers, *layouts* instead of formatters — and Logback's `AsyncAppender` is the queue handler,
  including the drop-on-full behaviour.
- **structlog** and **Zap** (Go) are the structured-first versions: the log call takes an event name and
  key–value pairs, and formatting is a pipeline of processors.
- **OpenTelemetry** standardises the context propagation — the trace and span ids that make the
  correlation id work across services rather than just within one.
- **Log4Shell (CVE-2021-44228)** is the cautionary tale: Log4j interpolated `${...}` expressions inside
  *log messages*, so logging a user-supplied string could execute code. The lesson is one line —
  **never interpret user data as a template** — and it belongs in any answer about formatting.

---

## 6. The numbers

### The cost of a log call that produces nothing

```
 10,000 requests/second × 20 log statements each  =  200,000 log calls/second
 of which ~80% are DEBUG and switched off         =  160,000 suppressed calls/second
```

```
 suppressed call, level check only         ~0.05 µs   ->  160,000 × 0.05 µs =   8 ms/s
 suppressed call, f-string already built   ~0.50 µs   ->                       80 ms/s
 suppressed call, f-string with a
   json.dumps of a real object  ~50 µs                ->                    8,000 ms/s
```

**Eight seconds of CPU per second — eight cores — spent building strings that are thrown away.** That
is the whole argument for deferred formatting, and it is a number rather than a principle. The first
row is what you get by checking the level first; the third is what you get from an f-string with an
expensive argument.

### Volume and disk

```
 200,000 log calls/second, ~200 B per line
 at DEBUG (everything):  200,000 × 200 B  =  40 MB/s  =  3.4 TB/day
 at INFO (20% of lines):  40,000 × 200 B  =   8 MB/s  =  690 GB/day
 at WARNING (1%):          2,000 × 200 B  =  0.4 MB/s =   35 GB/day
```

**Three and a half terabytes a day at DEBUG.** That is why DEBUG is off in production, why sampling
exists, and why "just log everything and search later" is not a plan. And at a typical ₹2 per GB per
month for hot log storage, the DEBUG option is roughly ₹2 lakh a month in storage alone.

### Why writes must be buffered, and asynchronous

```
 an fsync to disk:            ~5 ms
 a buffered write to a file:  ~1 µs
 a network write to a collector: ~0.5 ms, and it can hang

 at 40,000 lines/second:
   fsync per line:     40,000 × 5 ms   = 200 seconds of I/O per second — impossible
   buffered:           40,000 × 1 µs   = 40 ms/s — fine
   network, synchronous: 40,000 × 0.5 ms = 20 seconds per second — impossible
```

**Synchronous network logging is arithmetically impossible at this volume**, which is why the queue is
not an optimisation. And the queue's size is a time budget:

```
 queue of 10,000 records at 40,000 records/second  =  250 ms of buffer
 a collector stalling for 1 second  ->  30,000 records dropped
```

Two hundred and fifty milliseconds of tolerance. That number is what you tune, and it is why drops
must be counted: a one-second collector hiccup silently loses thirty thousand records unless somebody
is watching the counter.

### Finding one request

```
 200,000 lines/second × 86,400 s  =  17,280,000,000 lines/day
 one request produces ~20 of them
```

**Seventeen billion lines a day, and the twenty you want are scattered through it.** Grep is not a
plan; the correlation id is. With it, "show me this request" is an indexed lookup. Without it, it is
impossible — and this is why the correlation id is the highest-value field in the record.

### Structured versus text, for the same query

```
 "failed Razorpay payments over ₹10,000 last Tuesday"

 free text:   regex over ~700 GB of that day's INFO lines
 structured:  a query on indexed fields — event, provider, amount
```

The storage cost of JSON is roughly 30–50 percent more bytes per line than plain text. **That is the
trade: about 40 percent more disk to make the data queryable at all.**

### Sampling, priced

```
 one very noisy event: cache_hit, 100,000/second
 unsampled:              100,000 × 200 B  =  20 MB/s  =  1.7 TB/day
 sampled at 1%:            1,000 × 200 B  = 0.2 MB/s  =   17 GB/day
```

**A hundredfold reduction on one event name**, with the statistics preserved as long as you record the
sampling rate in the line — so a consumer can multiply back up. And errors are never sampled.

---

## 7. The trade-offs

### What this design gives up

**Asynchronous logging loses records exactly when you need them.** A crash discards whatever is in the
queue, and that is the last few hundred milliseconds before the failure — the most valuable logs in the
system. Flushing on shutdown handles a graceful exit and does nothing for a segmentation fault or an
OOM kill. Writing CRITICAL synchronously is the usual compromise: the volume is tiny and the value is
enormous.

**A bounded queue drops, and dropping is invisible unless you make it visible.** A counter and an alert
are not optional. The alternative — an unbounded queue — converts a slow collector into an
out-of-memory kill, which is strictly worse.

**Deferred formatting makes the API worse.** `logger.info("order %s", id)` is uglier than an f-string
and easier to get wrong — a mismatched placeholder count is a runtime error inside the logger, in the
error path, which is the worst possible place. Structured logging with keyword fields is nicer, and
the reason the `%`-style survives is that it is what defers the work. A linter rule catching f-strings
in log calls is worth more than any amount of documentation.

**A logger must never raise, which means it swallows its own errors.** A full disk, an unserialisable
value, a broken network handler — none of them may propagate into business code. So logging failures
are themselves invisible unless there is an internal error counter and a fallback destination. "The
logs stopped" is a genuinely common incident with no log line explaining it.

**The hierarchy is global mutable state.** Loggers are registered in a process-wide manager, so tests
interfere with each other and a library that configures the root logger breaks its host application.
The rule — **libraries add handlers to nothing and configure nothing; applications configure the
root** — exists because that mistake is so common.

**Structured logging costs discipline.** The moment somebody writes `logger.info(f"paid {amount}")`
instead of an event name and fields, that line is invisible to every dashboard. Consistency has to be
enforced by review or by a linter, because the framework cannot tell.

### "I would change this design if..."

- **...records must never be lost.** Then write synchronously to a local file and let a separate agent
  ship it — the file is the durable buffer, and the process never waits on a network.
- **...volume exceeds what a queue can absorb.** Then sample at the source, per event name, and record
  the rate in the line so consumers can scale it back up.
- **...several services must be correlated.** Then the correlation id becomes a propagated trace
  context — OpenTelemetry — and logging becomes one signal among traces and metrics rather than the
  only one.
- **...the destination is genuinely fast and local.** Then skip the queue: a buffered file write is a
  microsecond, and a queue adds a thread, a hand-off and a loss mode for no benefit.

### The honest concession

The part the prompt asks about — adding a destination — is the easy part, and it is one interface with
one method. The parts that decide whether the library is any good are the level check coming first,
the correlation id, and the queue's drop policy. Those are all *performance and operations* decisions
rather than object-oriented ones, and a design answer that produces a beautiful class diagram and
never mentions that a suppressed f-string can burn eight cores has answered a different question from
the one that matters in production.

---

## 8. In the interview

### How it gets asked

- The prompt: *"Design a logging library. How would I add a new destination?"*
- The performance probe, which is the real question: *"What does a `debug` call cost when debug
  logging is off?"*
- The operational probe: *"Logging to a network collector is slowing down our requests. What do you
  do?"*
- The scale probe: *"How do you find all the log lines for one request among a billion?"*
- The API probe: *"Why does Python's logging use `%s` and arguments instead of f-strings?"*

### The timed script

**Minutes 0–5 · Clarify.** A library or one service's logging? Structured or text? What volume? Must
any line be guaranteed to survive a crash?

**Minutes 5–12 · The four pieces**, with `Handler` and `Formatter` kept separate and the N × M
argument. Answer the prompt's question directly and early: adding a destination is one class, one
method, one line of wiring.

**Minutes 12–20 · The hot path**, and this is where to spend the time. The level check first, deferred
formatting, and the arithmetic — eight cores burned on suppressed f-strings with expensive arguments.

**Minutes 20–28 · The hierarchy and propagation**, and what it buys: turning one subsystem up without
touching anything else.

**Minutes 28–34 · Structured logging and the correlation id**, with the seventeen-billion-lines number.

**Minutes 34–40 · Asynchronous emission**, the drop policy, the loss-on-crash trade, and CRITICAL
written synchronously.

### The follow-ups

**"How do I add a new destination?"**
"One class implementing `Handler`, with a single `emit` method, plus one line of configuration
attaching it to a logger. Nothing else changes — and it is one class rather than several because
`Handler` and `Formatter` are deliberately separate interfaces: *where* it goes and *what it looks
like* vary independently. If they were combined you would need a class per combination —
`JsonFileHandler`, `TextFileHandler`, `JsonNetworkHandler` — so N × M classes instead of N + M. The
handler also carries its own level, which is what lets a file capture DEBUG while the console shows
only warnings from the same logger."

**"What does a `debug` call cost when debug is off?"**
"It should be one integer comparison and a return — about fifty nanoseconds — and the API is designed
around making that possible. Which is why `logger.debug(\"user %s failed\", user_id)` is right and
`logger.debug(f\"user {user_id} failed\")` is wrong: arguments are evaluated before the call, so the
f-string is built whether or not anybody wants it. With an expensive argument the difference is
dramatic. At ten thousand requests a second with twenty log statements each, and eighty percent of them
suppressed, an f-string that serialises an object at fifty microseconds costs **eight seconds of CPU
per second** — eight cores producing strings that are immediately discarded. The deferred version costs
about eight milliseconds a second."

**"Logging to a network collector is slowing down our requests."**
"Put a bounded queue between the logger and the handler: the caller appends and returns, and a
background thread drains it. Synchronous network logging is arithmetically impossible anyway — at
forty thousand lines a second and half a millisecond per write, that is twenty seconds of I/O per
second. The queue introduces two costs I would name explicitly. It must **drop** when full rather than
block, because blocking reintroduces exactly the coupling it exists to remove — and the drops must be
counted and alerted on, or you silently lose thirty thousand records every time the collector hiccups
for a second. And anything still queued when the process dies is lost, which is precisely the moment
you want it. So: flush on shutdown, and write CRITICAL synchronously, because the volume is tiny and
the value is enormous."

**"How do you find all the lines for one request?"**
"A correlation id on every record, generated at the edge, stored in a `ContextVar`, and attached
automatically by the framework rather than passed through every function signature. The arithmetic
makes the case: two hundred thousand lines a second is seventeen billion a day, and one request
produces about twenty of them, interleaved with everything else. With the id it is an indexed lookup;
without it, it is not a hard problem, it is an impossible one. I would use a `ContextVar` rather than a
thread-local so it works with async code, and across services the id becomes a propagated trace
context."

**"Why structured logging?"**
"Because a sentence is readable by a person and useless to a machine. 'Failed Razorpay payments over
ten thousand rupees last Tuesday' is a regular expression over hundreds of gigabytes if the lines are
prose, and an indexed query if they are records with an event name and typed fields. It costs about
thirty to fifty percent more bytes per line for the JSON, which is the trade: forty percent more disk
to make the data queryable at all. It also decouples the log text from the dashboards — you can reword
a message without breaking every alert built on it, because the alert matches an event name."

**"What happens if the logging itself fails?"**
"It must not propagate. A full disk or an unserialisable value cannot be allowed to throw an exception
inside unrelated business code, so every handler wraps its emit in a `try` and the JSON formatter falls
back to `repr` rather than raising. The consequence, and it is a real one, is that logging failures are
themselves invisible — so there has to be an internal error counter and ideally a fallback destination.
'The logs stopped' is a common incident with, by construction, no log line explaining it."

**"Any security concerns?"**
"Two. First, never interpolate user data as a *template* — that is Log4Shell: Log4j evaluated `${...}`
expressions inside log messages, so logging a user-supplied string could execute code. User data is a
value, never a format string. Second, logs are where secrets leak: a request body dumped at DEBUG
contains passwords and card numbers, and it is now in a system with much weaker access control than
the database. I would add a redaction filter for known sensitive field names and treat the log store as
production data, not as a convenience."

### A model answer

Asked: *design a logging library. How would I add a new destination?*

> "Let me answer the direct question first and then spend the time on the part I think decides whether
> the library is any good.
>
> Adding a destination is one class implementing a `Handler` interface with a single `emit` method, plus
> one line of configuration attaching it to a logger. That is deliberately small, and it is small
> because `Handler` and `Formatter` are two separate interfaces — *where* a record goes and *what it
> looks like* vary independently, so you can send JSON to a file and plain text to the console. If they
> were one interface you would need a class per combination, N × M instead of N + M.
>
> Now the part that matters more. There are four pieces: a `Logger` that code calls, a `LogRecord`
> describing one event, handlers, and formatters. And the single most important design decision is that
> **the level check is the first statement in the logging call**, before anything is built.
>
> The reason is that most logging calls produce nothing. At ten thousand requests a second with twenty
> log statements each, that is two hundred thousand calls a second and perhaps eighty percent of them
> are debug and switched off. A suppressed call should cost one integer comparison — about fifty
> nanoseconds.
>
> This is why the API takes a message *template* and arguments rather than a finished string. Arguments
> are evaluated before the call, so an f-string is built whether or not anybody wants it. If that
> f-string serialises an object — say fifty microseconds — then a hundred and sixty thousand suppressed
> calls a second is **eight seconds of CPU per second**. Eight cores, producing strings that are
> immediately discarded. That number is the whole argument for the awkward `%s` API, and it is why
> linters warn about f-strings in log calls.
>
> Loggers are hierarchical and dotted — `app.payments.stripe` — and a record propagates upward through
> its ancestors, each of which has its own handlers and its own level. That is what makes logging usable
> in production: you can turn `app.payments` up to DEBUG and leave everything else at INFO, in one line
> of configuration, with no code change. It is structurally a chain of responsibility with one
> difference — every ancestor gets the record, not just the first — and `propagate = False` cuts it.
>
> Two more things I would insist on. **Structured records rather than sentences**, because at seventeen
> billion lines a day 'failed Razorpay payments over ten thousand rupees' has to be a query, not a
> regular expression. And a **correlation id** on every record, from a context variable, attached by the
> framework — one request produces twenty lines scattered through two hundred thousand a second, and
> without a shared id, reconstructing it is impossible rather than merely hard.
>
> Finally, emission goes through a bounded queue to a background thread, because synchronous network
> logging at forty thousand lines a second would need twenty seconds of I/O per second. The queue drops
> rather than blocks when full — blocking would reintroduce the coupling it exists to remove — and the
> drops are counted and alerted on. The honest cost is that a crash loses whatever is queued, which is
> exactly the logs you want, so CRITICAL is written synchronously and everything is flushed on
> shutdown."

---

## 9. Recall card

- **`Handler` (WHERE) and `Formatter` (WHAT IT LOOKS LIKE) are separate interfaces, and that is the
  answer to the prompt**: adding a destination is **one class, one method, one line of wiring**.
  Combined, you would need a class per combination — **N × M instead of N + M**. Each handler carries
  its **own level**, so a file can capture DEBUG while the console shows only warnings.
- **The level check must be the FIRST statement, and the API exists to make deferred formatting
  possible.** `logger.debug("user %s", uid)` defers; `logger.debug(f"user {uid}")` **always builds the
  string**. At 200,000 calls/s with 80% suppressed and an expensive argument, that is **8 seconds of
  CPU per second — eight cores — discarded**, against ~8 ms/s done properly.
- **Dotted hierarchical loggers with upward propagation let you turn one subsystem up in one line of
  config.** Structurally a chain of responsibility, but **every ancestor gets the record**, not just the
  first — `propagate = False` cuts it.
- **Log events, not sentences, and carry a correlation id.** 200,000 lines/s is **17 billion a day**,
  and one request's 20 lines are scattered through it — with the id it is an indexed lookup, without it
  it is impossible. Use a **`ContextVar`** (async-safe), attached by the framework, never threaded
  through signatures. JSON costs ~40% more bytes and makes the data queryable at all.
- **Emit through a BOUNDED queue on a background thread — synchronous network logging is
  arithmetically impossible** (40,000 lines/s × 0.5 ms = 20 s of I/O per second). It must **drop, not
  block**, and **count the drops** (a 1 s collector stall loses ~30,000 records). A crash loses the
  queue — the logs you most want — so **flush on shutdown and write CRITICAL synchronously**. And **a
  logger must never raise**: wrap every emit, fall back to `repr`, and **never interpret user data as a
  template** (Log4Shell).
