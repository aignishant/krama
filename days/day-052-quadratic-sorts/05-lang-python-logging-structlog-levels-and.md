---
day: 52
track: lang-python
title: "logging, structlog, levels, and JSON output"
theme: "Logging that helps at 3am"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 052 · Python — logging, structlog, levels, and JSON output

**Today's theme:** Logging that helps at 3am

**After today you can:** You can emit structured logs with request IDs in each language and grep them.

**The interviewer asks it as:** *What do you log, and what must you never log?*

---

## 1. What this is, and why it matters

A log is the record a program leaves of what it did, written for a person who was not there,
usually at three in the morning, usually in a hurry. Python's standard `logging` module gives you
a logger per module, five levels of importance, and a formatter that decides what each line looks
like. Today the formatter writes one JSON object per line, every line carries the request id from
[day 49](../day-049-peak-finding/README.md), and the extra facts about an event go in named
fields rather than inside the sentence, so the line can be searched by a machine and read by a
person.

At work, logs are the only witness to most incidents; the difference between a ten-minute fix
and a four-hour one is whether the log line says which user and which request, or just "error".
In interviews, "what do you log, and what must you never log" is asked because the second half
has a short, absolute answer that a surprising number of people get wrong, and because the first
half shows whether you have ever been the person reading the log.

## 2. The story

Ravi works the night desk at a forty-room hotel, ten at night to six in the morning. On the desk
is the incident book. Every night shift writes in it, and every morning the manager, Shalini,
reads it before she does anything else.

In Ravi's first month his entries looked like this: "Around midnight something happened with a
guest, sorted it." Shalini read that, asked him what happened, and he could not remember which
guest. That was the last entry of that kind he wrote.

Now every line has the same five things, in the same order. The time, to the minute. The room
number. What happened, in plain words. How serious, marked with one of four letters in the
margin: N for a note, W for something to watch, E for a problem that needed fixing, and F for
the kind of thing you phone the manager about at night. And the folder number, so anyone can
pull the guest's file from the cabinet without asking. "02:14 · Room 214 · guest reported no hot
water, plumber called, fixed 02:50 · E · folder 214."

The letters matter because Shalini does not read every line. On a normal morning she reads only
the E and F lines, and glances at the W ones. On the morning after a bad night she reads all of
it. The N lines exist for that second kind of morning, and nobody expects them to be read most
days.

There are things Ravi never writes in the book, and the reason is where the book lives: on the
desk, open, where the day staff, the cleaners and sometimes a guest waiting for a taxi can see
it. Card numbers never go in. The code to a room safe never goes in. A guest's passport number
never goes in. Those are in the locked drawer, in the folder, and the book says "see folder 214".
Once, a new hire copied a card number into the book to save walking to the cabinet, and it took
Shalini a week to be sure nobody had photographed the page.

## 3. The idea in plain English

The incident book is the **log**, and each line is a **record**. `logging.getLogger("users")`
gives you a logger named after the part of the program writing, so the line says who wrote it.

Ravi's four letters are **levels**: `DEBUG` for the N lines that are only read on a bad morning,
`INFO` for the ordinary "this happened", `WARNING` for something to watch, `ERROR` for a problem
that needed handling, and `CRITICAL` for the phone-the-manager kind. A logger has a threshold,
and lines below it are not written at all; running at `INFO` means the `DEBUG` lines cost almost
nothing and are switched on with one setting when the bad night comes.

The five things in the same order are **structured logging**: instead of one sentence with the
facts buried in it, a line is a set of named fields. The **formatter** decides the shape; today's
writes a JSON object per line, with `ts`, `level`, `logger`, `msg`, `request_id`, and whatever
extra fields the call added. A machine can filter on `level` and a person can still read `msg`.

The folder number is the **request id**. Every line written while handling one request carries
the same id, so `grep` on that id gives you the whole story of that request in order. A
`ContextVar` from the standard library holds it: set once at the start of a request, readable by
any logger call on that request without being passed through every function. A `ContextVar` is
like a global that is separate per request, which is what an async server needs.

The extra facts, `user_id`, `ms`, go in `extra={...}`, a dict of fields that the formatter
attaches to the line. They are not in the message string, so the message stays the same for
every occurrence and can be searched for as a phrase.

`log.exception(...)` is the E line with the plumber's report attached: it writes an `ERROR` and
adds the traceback as a field, so the stack is in the same JSON line as the request id.

What Ravi never writes is the **never-log list**: passwords, tokens and API keys, card numbers,
the full request body, and personal data beyond an id. The log lives where many people and
systems can read it and it is kept for months. "See folder 214" is logging the user id, not the
user.

## 4. The picture

```text
{"ts": "2026-09-16T21:39:07", "level": "INFO",  "logger": "users", "msg": "user created", "request_id": "1a89bf92", "user_id": 2, "user_name": "Arjun"}
{"ts": "2026-09-16T21:39:07", "level": "INFO",  "logger": "users", "msg": "request done", "request_id": "1a89bf92", "ms": 0.2}
{"ts": "2026-09-16T21:39:07", "level": "WARNING", "logger": "users", "msg": "rejected create: blank name", "request_id": "e155afe0"}
{"ts": "2026-09-16T21:39:07", "level": "ERROR", "logger": "users", "msg": "create failed", "request_id": "e155afe0", "exc": "Traceback ..."}
  ^time                       ^letter          ^who              ^what                          ^folder number            ^the facts
```

Notice that the two lines with `e155afe0` tell one story, and that `password` appears nowhere
even though `create_user` received one.

## 5. The code, built step by step

The request id, and the formatter.

```python
request_id: ContextVar[str] = ContextVar("request_id", default="-")

STANDARD = set(vars(logging.LogRecord("", 0, "", 0, "", (), None))) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        line = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "request_id": request_id.get(),
        }
        line.update({key: value for key, value in vars(record).items() if key not in STANDARD})
        if record.exc_info:
            line["exc"] = self.formatException(record.exc_info)
        return json.dumps(line)
```

A `LogRecord` carries the standard fields and any `extra` ones as attributes. `STANDARD` is the
set of names a blank record has, so the comprehension picks out only the fields you added.
`getMessage()` applies any `%s` arguments. `exc_info` is set by `log.exception`, and
`formatException` renders the traceback as text.

Wiring it to the root logger.

```python
def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
```

A **handler** is where lines go, here standard output, which is where a container expects them.
The root logger is the parent of every named logger, so one handler on it catches all of them.
`setLevel(level)` is the threshold, and it is a setting from
[day 51](../day-051-why-sorting-matters/README.md), not a constant.

Writing lines.

```python
log = logging.getLogger("users")


def create_user(name: str, password: str) -> int:
    log.debug("validating input", extra={"name_len": len(name)})
    if not name:
        log.warning("rejected create: blank name")
        raise ValueError("name must not be blank")
    user_id = 2
    log.info("user created", extra={"user_id": user_id, "user_name": name})
    return user_id
```

One logger per module, named. The message is a constant phrase; the facts are in `extra`. The
function receives `password` and logs nothing about it, not its length, not whether it was
empty. That is not an accident, and the practice sheet has you prove it.

The request wrapper.

```python
def handle(name: str, password: str) -> None:
    request_id.set(uuid.uuid4().hex[:8])
    start = time.perf_counter()
    try:
        create_user(name, password)
    except ValueError:
        log.exception("create failed")
    finally:
        log.info("request done", extra={"ms": round((time.perf_counter() - start) * 1000, 1)})
```

`request_id.set(...)` once, at the top; every line under it carries the id without being told.
`log.exception` inside `except` writes an `ERROR` with the traceback attached. The `finally`
guarantees a "request done" line with the duration, success or not, which is the line you grep
for when someone says "it was slow".

Run it:

```bash
python main.py
```

```text
{"ts": "2026-09-16T21:39:07", "level": "INFO", "logger": "users", "msg": "user created", "request_id": "1a89bf92", "user_id": 2, "user_name": "Arjun"}
{"ts": "2026-09-16T21:39:07", "level": "INFO", "logger": "users", "msg": "request done", "request_id": "1a89bf92", "ms": 0.2}
{"ts": "2026-09-16T21:39:07", "level": "WARNING", "logger": "users", "msg": "rejected create: blank name", "request_id": "e155afe0"}
{"ts": "2026-09-16T21:39:07", "level": "ERROR", "logger": "users", "msg": "create failed", "request_id": "e155afe0", "exc": "Traceback (most recent call last):\n  File \"main.py\", line 54, in handle\n    create_user(name, password)\n  File \"main.py\", line 44, in create_user\n    raise ValueError(\"name must not be blank\")\nValueError: name must not be blank"}
{"ts": "2026-09-16T21:39:07", "level": "INFO", "logger": "users", "msg": "request done", "request_id": "e155afe0", "ms": 2.9}
```

Five lines, two request ids, no `DEBUG` line because the threshold is `INFO`. Run it again with
the threshold lowered and the N line appears:

```bash
python main.py DEBUG
```

```text
{"ts": "2026-09-16T21:39:07", "level": "DEBUG", "logger": "users", "msg": "validating input", "request_id": "c8c41a8a", "name_len": 5}
```

And this is why it is JSON. Find every error and pull out its request id and the last line of
its traceback, with nothing but the standard library:

```bash
python main.py | grep '"level": "ERROR"' | python -c "import sys, json; [print(json.loads(l)['request_id'], json.loads(l)['exc'].splitlines()[-1]) for l in sys.stdin]"
```

```text
7a5b0a29 ValueError: name must not be blank
```

Then `grep 7a5b0a29` gives you every line of that request, in order. That is the three-in-the-
morning workflow, and the whole lesson exists so it takes one minute.

**The same thing with structlog.** `structlog` is the third-party library built around this
idea; the call site is the same shape with the fields as keyword arguments:

```python
import structlog

structlog.configure(processors=[structlog.processors.add_log_level, structlog.processors.TimeStamper(fmt="iso"), structlog.processors.JSONRenderer()])
log = structlog.get_logger("users")
log.info("user created", user_id=2, user_name="Arjun")
```

It binds context with `log.bind(request_id=...)` instead of a `ContextVar`, and it renders JSON
by default. The standard library version above is what you fall back to when you cannot add a
dependency, and everything in it maps onto structlog one to one.

Here is the whole program in one piece, `main.py`:

```python
import json
import logging
import sys
import time
import uuid
from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar("request_id", default="-")

STANDARD = set(vars(logging.LogRecord("", 0, "", 0, "", (), None))) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        line = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "request_id": request_id.get(),
        }
        line.update({key: value for key, value in vars(record).items() if key not in STANDARD})
        if record.exc_info:
            line["exc"] = self.formatException(record.exc_info)
        return json.dumps(line)


def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)


log = logging.getLogger("users")


def create_user(name: str, password: str) -> int:
    log.debug("validating input", extra={"name_len": len(name)})
    if not name:
        log.warning("rejected create: blank name")
        raise ValueError("name must not be blank")
    user_id = 2
    log.info("user created", extra={"user_id": user_id, "user_name": name})
    return user_id


def handle(name: str, password: str) -> None:
    request_id.set(uuid.uuid4().hex[:8])
    start = time.perf_counter()
    try:
        create_user(name, password)
    except ValueError:
        log.exception("create failed")
    finally:
        log.info("request done", extra={"ms": round((time.perf_counter() - start) * 1000, 1)})


if __name__ == "__main__":
    setup_logging(sys.argv[1] if len(sys.argv) > 1 else "INFO")
    handle("Arjun", "hunter2")
    handle("", "hunter2")
```

## 6. How the other two languages do it

**Go**

```go
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
reqLog := logger.With("request_id", requestID)
reqLog.Info("user created", "user_id", 2, "user_name", name)
reqLog.Error("create failed", "err", err)
```

`log/slog` is in the standard library and JSON is one handler away. Fields are alternating key,
value arguments, and the request id is bound once with `With` and carried by the returned
logger rather than by a context variable.

**C++**

```cpp
auto logger = spdlog::stdout_logger_mt("users");
logger->set_pattern(R"({"ts":"%Y-%m-%dT%H:%M:%S","level":"%l","logger":"%n","msg":"%v"})");
logger->info(R"("request_id":"{}","user_id":{},"user_name":"{}")", request_id, 2, name);
```

spdlog formats a pattern per line and the message with `{}` placeholders; there is no native
notion of fields, so JSON is a pattern you write and a message you shape, or a small helper that
builds the object with nlohmann.

**The difference that matters:** Python and Go both know what a field is; C++ with spdlog knows
what a line is. In Python `extra={"user_id": 2}` becomes `"user_id": 2` in the JSON without any
help; in Go `"user_id", 2` does the same; in spdlog you are formatting a string and it is your
job to make sure the result is still valid JSON when `name` contains a quotation mark.

## 7. The traps

**The near-miss: the password in the log.** It is one keystroke away:

```python
log.info("user created", extra={"user_id": user_id, "user_name": name, "password": password})
```

```text
{"ts": "...", "level": "INFO", "logger": "users", "msg": "user created", "request_id": "1a89bf92", "user_id": 2, "user_name": "Arjun", "password": "hunter2"}
```

That line is now in a file, a log aggregator, a backup, and the terminal history of whoever
tailed it, for as long as the retention policy says. There is no undo. The same applies to
`extra={"body": request.json()}` and to `log.info(f"login {headers}")`.

**A field name that collides with the record.**

```python
log.info("user created", extra={"name": name})
```

```text
KeyError: "Attempt to overwrite 'name' in LogRecord"
```

`name`, `msg`, `args`, `levelname` and the other standard attributes belong to the record.
Prefix yours: `user_name`.

**Logging before setup.**

```python
import logging
logging.info("starting")      # nothing appears
logging.warning("shown %s", 42)
```

```text
WARNING:root:shown 42
```

The root logger's default threshold is `WARNING`, and the default handler writes plain text.
Call `setup_logging` before the first line you care about.

**Facts inside the sentence.**

```python
log.info(f"user {user_id} created in {ms}ms")
```

It reads fine. It cannot be grouped, because every occurrence is a different string, and it
cannot be filtered on `ms > 500` without a regular expression. Constant message, facts in
`extra`.

**`print` instead of logging.** It works, it has no level, no timestamp, no request id, and it
cannot be turned off. Every `print` in a service is a `log.debug` that nobody can silence.

**`log.error` in an `except` block.** It writes the message and drops the traceback.
`log.exception` is `log.error` with `exc_info=True`, and the stack is the reason you were logging.

## 8. Say it out loud

**How it gets asked**

- What do you log, and what must you never log?
- Why structured logs? What is wrong with a sentence?
- How do you find everything that happened during one request?
- What are the levels for, and which one do you run at in production?

**The ninety-second script**

Never: passwords, tokens and API keys, card numbers, full request or response bodies, and
personal data beyond an identifier. Logs live for months in places many people and systems can
read, so a secret in a log is a leak that has already happened. Always: a timestamp, a level, the
logger name, a constant message, a request id, and the facts of the event as named fields, such
as the user id, the duration, and the outcome. Structured, one JSON object per line, because a
machine filters on fields and a person still reads `msg`. The request id is set once at the top
of each request in a context variable and every line carries it, so one `grep` on the id gives
the whole story of one request in order. Levels are a threshold: production runs at `INFO`,
`DEBUG` lines are written in the code and switched on by a setting when something is wrong.
Errors are logged with `log.exception` so the traceback lands in the same line as the request
id. And every request ends with a "done" line carrying its duration, because "it was slow" is the
most common complaint and that line answers it.

**The follow-ups**

- **What about logging a user's email for support?** *An id, and a way for support to look up
  the email from the id in a system with access control. The log is not that system.*
- **How much is too much?** *Every request gets a start-or-done line and every error gets a
  line. Loops over a thousand items do not get a line per item at `INFO`; that is `DEBUG`, or a
  summary line with a count. If the log is too noisy to read, it is not a log.*
- **What is a request id for across services?** *Reuse the incoming `X-Request-ID` from
  [day 49](../day-049-peak-finding/README.md) instead of making a new one, pass it on every
  outgoing call, and one id follows the request through every service's log.*

**A model answer**

"Log a timestamp, level, logger name, a constant message, the request id, and the facts as
fields; user id, duration, outcome. One JSON object per line. Never a password, token, card
number, request body, or personal data past an id, because logs are kept for months where many
things can read them. In Python that is a `JsonFormatter` on the root logger, a `ContextVar` for
the request id set at the top of each request, `extra={}` for fields, `log.exception` in
`except`, and a `finally` that logs the duration. Threshold `INFO` in production, `DEBUG` by
setting when it matters."

## 9. Recall card

- Never log: passwords, tokens, keys, card numbers, full bodies, personal data past an id. Logs are kept for months, readable by many.
- Always log: `ts`, `level`, `logger`, constant `msg`, `request_id`, and the facts as fields in `extra={}`; one JSON object per line.
- `ContextVar` for the request id, set once per request; every line carries it; `grep` on it is the whole story.
- `log.exception` in `except`, not `log.error`; a `finally` that logs `ms`. Production at `INFO`, `DEBUG` by setting.
- `extra` keys must not collide with `name`, `msg`, `args`; the root default is `WARNING` until `setup_logging` runs.
