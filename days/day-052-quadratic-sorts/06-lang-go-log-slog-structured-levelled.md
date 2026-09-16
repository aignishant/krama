---
day: 52
track: lang-go
title: "log/slog: structured, levelled, and with context"
theme: "Logging that helps at 3am"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 052 · Go — log/slog: structured, levelled, and with context

**Today's theme:** Logging that helps at 3am

**After today you can:** You can emit structured logs with request IDs in each language and grep them.

**The interviewer asks it as:** *What do you log, and what must you never log?*

---

## 1. What this is, and why it matters

`log/slog` is the structured logger in Go's standard library. A `slog.Logger` writes records
through a handler, and `slog.NewJSONHandler` writes one JSON object per line; every call takes a
constant message and then key-value pairs, which become fields. `logger.With("request_id", id)`
returns a logger that adds that field to every line, and that logger travels with the request,
usually in the `context.Context` from [day 36](../day-036-two-pointers-revision/README.md).

At work, `slog` replaced the older `log` package and a dozen third-party loggers in most Go
services, because it is standard and JSON is one line to switch on. In interviews, "what do you
log, and what must you never log" has one answer across languages; the Go-flavoured follow-up is
"how does the request id get to a function three calls deep", and the answer is the logger in the
context.

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
pull the guest's file from the cabinet without asking.

The letters matter because Shalini does not read every line. On a normal morning she reads only
the E and F lines. On the morning after a bad night she reads all of it.

When a problem takes several people, the folder number is what ties them together. Ravi writes
"02:14 · 214 · no hot water · E · folder 214", then phones the plumber and hands him a slip with
the folder number on it. The plumber writes his own line when he is done, with the same folder
number. The kitchen, if they were asked to send tea up, write theirs. In the morning Shalini
pulls every line that says 214 and has the whole night, in order, from three different hands,
without asking anyone.

There are things Ravi never writes in the book, and the reason is where the book lives: on the
desk, open, where the day staff, the cleaners and sometimes a guest waiting for a taxi can see
it. Card numbers never go in. The code to a room safe never goes in. A passport number never goes
in. Those are in the locked drawer, and the book says "see folder 214".

## 3. The idea in plain English

The incident book is the **log**. `slog.New(handler)` makes a logger, and the **handler** decides
where lines go and what they look like; `slog.NewJSONHandler(os.Stdout, opts)` writes one JSON
object per line to standard output.

Ravi's letters are **levels**: `slog.LevelDebug`, `LevelInfo`, `LevelWarn`, `LevelError`. The
handler has a threshold in its options, and records below it are dropped before they are
formatted, so `Debug` lines in production cost nearly nothing. A `slog.LevelVar` is a threshold
you can change while the program runs, which is how the bad-night switch works without a
restart.

The five things in the same order are **structured logging**. `logger.Info("user created",
"user_id", 2, "user_name", name)` is a constant message followed by alternating keys and values;
the handler writes each pair as a JSON field. The message never changes between occurrences, so
it can be grouped and searched as a phrase.

The slip with the folder number is `logger.With("request_id", id)`: it returns a new logger that
carries that field on every line it writes. Handing that logger to the plumber is putting it in
the **context**: `context.WithValue(ctx, key, logger)` at the top of the request, and a small
`fromContext(ctx)` that any function three calls deep uses to get the request's logger back. The
function never receives the id as a parameter; it receives the logger that already knows it.

`logger.Error("create failed", "err", err)` is the E line: an error value becomes a field with
its message. A duration passed as a `time.Duration` is written in a readable form.

What Ravi never writes is the **never-log list**: passwords, tokens and API keys, card numbers,
full request bodies, and personal data beyond an id. "See folder 214" is logging the user id, not
the user.

## 4. The picture

```text
{"time":"2026-09-16T21:39:07.412+05:30","level":"INFO","msg":"user created","request_id":"1a89bf92","user_id":2,"user_name":"Arjun"}
{"time":"2026-09-16T21:39:07.412+05:30","level":"INFO","msg":"request done","request_id":"1a89bf92","ms":0.2}
{"time":"2026-09-16T21:39:07.413+05:30","level":"WARN","msg":"rejected create: blank name","request_id":"e155afe0"}
{"time":"2026-09-16T21:39:07.413+05:30","level":"ERROR","msg":"create failed","request_id":"e155afe0","err":"name must not be blank"}
  ^time                                  ^letter        ^what                       ^folder number             ^the facts
```

Notice that `request_id` is on every line without any call naming it, because the logger that
wrote them was made with `With`. And notice no `password` field, though `createUser` received
one.

## 5. The code, built step by step

The logger, and the switchable threshold.

```go
var level = new(slog.LevelVar)

func newLogger() *slog.Logger {
	level.Set(slog.LevelInfo)
	return slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: level}))
}
```

`slog.LevelVar` satisfies the `Leveler` the handler wants and can be `Set` later, from a signal
handler or an admin endpoint, to `slog.LevelDebug` on the bad night.

The logger in the context.

```go
type ctxKey struct{}

func withLogger(ctx context.Context, logger *slog.Logger) context.Context {
	return context.WithValue(ctx, ctxKey{}, logger)
}

func fromContext(ctx context.Context) *slog.Logger {
	if logger, ok := ctx.Value(ctxKey{}).(*slog.Logger); ok {
		return logger
	}
	return slog.Default()
}
```

`ctxKey` is an unexported struct type, so no other package can collide with it, from
[day 49](../day-049-peak-finding/README.md). `fromContext` falls back to the default logger
rather than returning `nil`, so a function called outside a request still logs.

Writing lines, three calls deep.

```go
func createUser(ctx context.Context, name, password string) (int, error) {
	log := fromContext(ctx)
	log.Debug("validating input", "name_len", len(name))
	if name == "" {
		log.Warn("rejected create: blank name")
		return 0, errors.New("name must not be blank")
	}
	userID := 2
	log.Info("user created", "user_id", userID, "user_name", name)
	return userID, nil
}
```

The function takes `ctx` first, as every function that waits or logs should, and gets its logger
from it. The message is constant; the facts are pairs. `password` is received and never
mentioned.

The request wrapper.

```go
func handle(base *slog.Logger, name, password string) {
	requestID := fmt.Sprintf("%08x", rand.Uint32())
	log := base.With("request_id", requestID)
	ctx := withLogger(context.Background(), log)
	start := time.Now()
	if _, err := createUser(ctx, name, password); err != nil {
		log.Error("create failed", "err", err)
	}
	log.Info("request done", "ms", float64(time.Since(start).Microseconds())/1000)
}
```

`With` once, into the context once, and every line below carries the id. `"err", err` makes the
error's message a field. The final line always runs, with the duration.

Run it:

```bash
go run main.go
```

```text
{"time":"2026-09-16T21:39:07.412391+05:30","level":"INFO","msg":"user created","request_id":"1a89bf92","user_id":2,"user_name":"Arjun"}
{"time":"2026-09-16T21:39:07.412512+05:30","level":"INFO","msg":"request done","request_id":"1a89bf92","ms":0.121}
{"time":"2026-09-16T21:39:07.412530+05:30","level":"WARN","msg":"rejected create: blank name","request_id":"e155afe0"}
{"time":"2026-09-16T21:39:07.412541+05:30","level":"ERROR","msg":"create failed","request_id":"e155afe0","err":"name must not be blank"}
{"time":"2026-09-16T21:39:07.412548+05:30","level":"INFO","msg":"request done","request_id":"e155afe0","ms":0.018}
```

No `DEBUG` line, because the threshold is `INFO`. Set `level.Set(slog.LevelDebug)` and it
appears with `"name_len":5`.

And the reason it is JSON. Every error, with its request id, using the `jq` tool if you have it
or a five-line Go program if you do not:

```bash
go run main.go | grep '"level":"ERROR"' | jq -r '.request_id + " " + .err'
```

```text
e155afe0 name must not be blank
```

Then `grep e155afe0` gives every line of that request in order, from every function that
touched it.

Here is the whole program in one piece, `main.go`:

```go
package main

import (
	"context"
	"errors"
	"fmt"
	"log/slog"
	"math/rand/v2"
	"os"
	"time"
)

var level = new(slog.LevelVar)

func newLogger() *slog.Logger {
	level.Set(slog.LevelInfo)
	return slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: level}))
}

type ctxKey struct{}

func withLogger(ctx context.Context, logger *slog.Logger) context.Context {
	return context.WithValue(ctx, ctxKey{}, logger)
}

func fromContext(ctx context.Context) *slog.Logger {
	if logger, ok := ctx.Value(ctxKey{}).(*slog.Logger); ok {
		return logger
	}
	return slog.Default()
}

func createUser(ctx context.Context, name, password string) (int, error) {
	log := fromContext(ctx)
	log.Debug("validating input", "name_len", len(name))
	if name == "" {
		log.Warn("rejected create: blank name")
		return 0, errors.New("name must not be blank")
	}
	userID := 2
	log.Info("user created", "user_id", userID, "user_name", name)
	return userID, nil
}

func handle(base *slog.Logger, name, password string) {
	requestID := fmt.Sprintf("%08x", rand.Uint32())
	log := base.With("request_id", requestID)
	ctx := withLogger(context.Background(), log)
	start := time.Now()
	if _, err := createUser(ctx, name, password); err != nil {
		log.Error("create failed", "err", err)
	}
	log.Info("request done", "ms", float64(time.Since(start).Microseconds())/1000)
}

func main() {
	logger := newLogger()
	if len(os.Args) > 1 && os.Args[1] == "debug" {
		level.Set(slog.LevelDebug)
	}
	handle(logger, "Arjun", "hunter2")
	handle(logger, "", "hunter2")
}
```

In a server, `handle` is the logging middleware from [day 49](../day-049-peak-finding/README.md):
it makes the request logger, puts it in `r.Context()` with `r.WithContext`, and every handler
does `fromContext(r.Context())`.

## 6. How the other two languages do it

**Python**

```python
request_id: ContextVar[str] = ContextVar("request_id", default="-")
request_id.set(uuid.uuid4().hex[:8])          # once, at the top of the request
log.info("user created", extra={"user_id": 2, "user_name": name})
```

The request id lives in a context variable that the formatter reads on every line; the call
site never mentions it. Fields are a dict rather than alternating arguments.

**C++**

```cpp
thread_local std::string request_id;
log_json(logger, spdlog::level::info, {{"msg", "user created"}, {"user_id", 2}, {"user_name", name}});
```

spdlog formats strings, so JSON fields are a helper that builds a nlohmann object, and the
request id is a `thread_local` because each request runs on one worker thread.

**The difference that matters:** Go is the only one where the request id rides on the logger
object rather than on the thread or task. `With` returns a new logger, and that logger goes into
the context, so two goroutines handling two requests each hold their own. Python's `ContextVar`
and C++'s `thread_local` do the same job by different means, and the C++ one is wrong the moment
a request hops threads.

## 7. The traps

**The near-miss: the password as a field.**

```go
log.Info("user created", "user_id", userID, "user_name", name, "password", password)
```

```text
{"time":"...","level":"INFO","msg":"user created","request_id":"1a89bf92","user_id":2,"user_name":"Arjun","password":"hunter2"}
```

No warning, no error, and the line is now in every place logs go. The same for
`"body", string(bodyBytes)` and for `"headers", r.Header`, which carries the API key.

**An odd number of arguments.**

```go
log.Info("user created", "user_id", userID, "user_name")
```

```text
{"time":"...","level":"INFO","msg":"user created","user_id":2,"!BADKEY":"user_name"}
```

It does not panic. The handler writes `!BADKEY` and moves on, and you find it in the log a week
later. `go vet` reports it at build time; run `go vet` in CI.

**Facts in the message.**

```go
log.Info(fmt.Sprintf("user %d created in %v", userID, elapsed))
```

Valid, and unsearchable: every occurrence is a different `msg`, and `elapsed` cannot be
compared. Constant message, facts as pairs.

**`log.Printf` from the old package.** It writes plain text to standard error with no level and
no fields, and it does not know about the request id. Mixing it with `slog` gives a log that is
half JSON. `slog.SetDefault(logger)` routes the old package's calls through the new handler,
which is the migration step.

**Passing the id instead of the logger.** `createUser(ctx, requestID, name, ...)` and
`slog.Info("...", "request_id", requestID, ...)` in every call works and is what people do when
they have not met `With`. Every function grows a parameter and every call site can forget it.
The logger in the context carries it for free.

**Logging the error and returning it.**

```go
if err != nil {
	log.Error("lookup failed", "err", err)
	return err
}
```

The caller also logs it, and its caller, and one failure is four `ERROR` lines. Log at the place
that handles the error, once; wrap it with `%w` on the way up.

## 8. Say it out loud

**How it gets asked**

- What do you log, and what must you never log?
- How does the request id reach a function three calls deep?
- Why JSON and not a readable line?
- How do you turn on debug logging in production without restarting?

**The ninety-second script**

Never: passwords, tokens and API keys, card numbers, full request or response bodies, and
personal data beyond an identifier, because logs are kept for months in places many people and
systems can read, and a secret written there has already leaked. Always: time, level, a constant
message, the request id, and the facts of the event as fields, such as user id, duration and
outcome. In Go that is `slog` with a JSON handler on standard output. At the top of each request
I make a logger with `With("request_id", id)` and put it in the context; any function down the
call chain takes a context and gets its logger from it, so the id is on every line without being
passed as a parameter. Errors are a field, `"err", err`, logged once at the place that handles
them. Every request ends with a done line and its duration. The threshold is a `LevelVar` set to
`INFO`, and an admin endpoint or a signal sets it to `DEBUG` when something is wrong, without a
restart.

**The follow-ups**

- **Why not put the request id in the context and read it in each call?** *That is also fine,
  and a custom handler can read it from `ctx` when you use the `InfoContext` methods. Putting the
  whole logger in the context means the fields travel together, and a function can add its own
  `With` for its callees.*
- **How much is too much?** *One line per request, one per error, summaries for loops. If the
  three-in-the-morning reader has to scroll past a thousand `DEBUG` lines to find the error, the
  `DEBUG` lines were at the wrong level.*
- **What about the `time` field's precision?** *The JSON handler writes nanoseconds and a zone.
  I keep it; log lines from different services are ordered by it, and clock skew between
  machines is the thing that makes that hard, not the format.*

**A model answer**

"Log time, level, constant message, request id, and the facts as fields. Never a secret, a body,
or personal data past an id. In Go, `slog.New(slog.NewJSONHandler(os.Stdout, opts))`, a
`LevelVar` threshold, `With("request_id", id)` once per request, the logger in the context so
`fromContext(ctx)` gives it back anywhere, `"err", err` for failures, a done line with `ms`, and
`go vet` in CI to catch the odd-argument `!BADKEY` before it ships."

## 9. Recall card

- Never log: passwords, tokens, keys, card numbers, bodies, personal data past an id. Always: time, level, constant `msg`, `request_id`, facts as fields.
- `slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: level}))`; `level` is a `*slog.LevelVar` you can `Set` at runtime.
- `base.With("request_id", id)` once per request; put that logger in the context; `fromContext(ctx)` three calls deep.
- Pairs are `"key", value`; an odd count writes `!BADKEY`, and `go vet` catches it.
- `"err", err` for errors, logged once where handled; a done line with the duration on every request.
