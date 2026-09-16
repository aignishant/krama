---
day: 52
track: lang-cpp
title: "spdlog: sinks, levels, and formatting"
theme: "Logging that helps at 3am"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 052 · C++ — spdlog: sinks, levels, and formatting

**Today's theme:** Logging that helps at 3am

**After today you can:** You can emit structured logs with request IDs in each language and grep them.

**The interviewer asks it as:** *What do you log, and what must you never log?*

---

## 1. What this is, and why it matters

C++ has no logging in its standard library, and spdlog is the one nearly everyone uses: a
logger writes to one or more **sinks**, a sink is a destination such as standard output or a
rotating file, each logger has a level threshold, and a **pattern** string decides what every
line looks like. spdlog formats messages with `{}` placeholders, and it is fast enough that
people leave `debug` lines in hot paths and switch them on when needed.

At work, spdlog is in most C++ services and a great many tools, and the shape you learn today,
one JSON object per line with a request id, is what the log aggregator expects from every
language. In interviews, "what do you log, and what must you never log" has one answer across
languages; the C++ follow-up is "how is that JSON, when spdlog only formats strings", and the
honest answer is that you build the object yourself.

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

The book itself is not the only copy. Every line Ravi writes, he also writes on a carbon sheet
underneath, and the carbon copies go to the owner's office once a week, where nobody reads them
unless there is a dispute. And the F lines, the phone-the-manager ones, he also writes on the
whiteboard by the door, so the morning shift sees them before they have sat down. Same line,
three places, chosen by how urgent it is.

There are things Ravi never writes anywhere: not in the book, not on the carbon, not on the
board. The reason is where they live: on the desk, open, where the day staff, the cleaners and
sometimes a guest waiting for a taxi can see it. Card numbers never go in. The code to a room
safe never goes in. A passport number never goes in. Those are in the locked drawer, and the book
says "see folder 214".

## 3. The idea in plain English

The incident book, the carbon copy and the whiteboard are **sinks**: destinations a logger
writes to. `spdlog::sinks::stdout_sink_mt` is standard output; `basic_file_sink_mt` is a file;
`rotating_file_sink_mt` is a file that starts a new one at a size limit. A logger can have
several sinks, and each sink can have its own threshold, so the whiteboard sink takes only
`critical` while the book takes everything from `info` up. The `_mt` suffix means multi-threaded:
safe to call from several threads at once, which the server from
[day 48](../day-048-binary-search-on-floats/README.md) needs.

Ravi's letters are **levels**: `trace`, `debug`, `info`, `warn`, `err`, `critical`. A logger's
`set_level` is the threshold; calls below it return almost immediately. `spdlog::level::from_str`
turns a setting from [day 51](../day-051-why-sorting-matters/README.md) into a level.

The five things in the same order are the **pattern**: a string of `%` codes that spdlog fills
in per line, `%Y-%m-%dT%H:%M:%S` for the time, `%l` for the level name, `%n` for the logger name,
`%v` for the message. Today the pattern is written so that the whole line is a JSON object,
and the message, `%v`, is the fields.

spdlog has no idea what a field is. It formats a string with `{}` placeholders and writes it. So
**structured logging** here is a small helper: build a nlohmann object from
[day 40](../day-040-2d-prefix-sums/README.md) with the message and the facts, `dump()` it, and
pass the result as `%v`. nlohmann escapes quotation marks and newlines in values, which is the
part you must not do by hand.

The folder number is the **request id**, held in a `thread_local std::string`: one variable
per thread, set at the top of each request on the worker thread that serves it, read by the
helper on every line. `thread_local` is correct as long as one request stays on one thread,
which is true for cpp-httplib and false for anything that hands work to a pool.

What Ravi never writes is the **never-log list**: passwords, tokens and API keys, card numbers,
full request bodies, and personal data beyond an id.

## 4. The picture

```text
                       +---> stdout sink  (info and up)      the book
  logger "users" ------+---> file sink    (debug and up)     the carbon copy
                       +---> stderr sink  (critical only)    the whiteboard

  one call:  log_json(logger, info, {{"msg","user created"},{"user_id",2}})
  one line:  {"ts":"2026-09-16T21:39:07","level":"info","logger":"users","request_id":"1a89bf92","msg":"user created","user_id":2}
```

Notice that one call fans out to whichever sinks accept that level, each with its own
threshold, and that the JSON is assembled from two halves: the pattern provides the first four
fields and `%v` provides the rest.

## 5. The code, built step by step

Install spdlog through your package manager, `libspdlog-dev` on Debian and Ubuntu, `spdlog` on
Homebrew and vcpkg; it depends on the `fmt` library, which comes with it.

The request id and the helper.

```cpp
#include <spdlog/spdlog.h>
#include <spdlog/sinks/basic_file_sink.h>
#include <spdlog/sinks/stdout_sinks.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

thread_local std::string request_id = "-";

void log_json(spdlog::logger& logger, spdlog::level::level_enum level, json fields) {
    fields["request_id"] = request_id;
    const std::string body = fields.dump();
    logger.log(level, "{}", body.substr(1, body.size() - 2));
}
```

`logger.log(level, fmt, args...)` is the general form behind `info`, `warn` and the rest. The
`substr` strips the outer braces from `{"msg":...}` so the pattern can supply the opening brace
and the first fields. The `"{}"` is important: passing `body` directly as the format string
would make any `{` inside a value a formatting error.

The logger with two sinks and the pattern.

```cpp
std::shared_ptr<spdlog::logger> make_logger(const std::string& level_name) {
    auto console = std::make_shared<spdlog::sinks::stdout_sink_mt>();
    auto file = std::make_shared<spdlog::sinks::basic_file_sink_mt>("users.log", true);
    file->set_level(spdlog::level::debug);
    auto logger = std::make_shared<spdlog::logger>("users", spdlog::sinks_init_list{console, file});
    logger->set_pattern(R"({"ts":"%Y-%m-%dT%H:%M:%S","level":"%l","logger":"%n",%v})");
    logger->set_level(spdlog::level::from_str(level_name));
    console->set_level(spdlog::level::from_str(level_name));
    return logger;
}
```

Two sinks, made as shared pointers, handed to the logger in an initialiser list. The file sink
takes `debug` and up always; the console takes whatever the setting says; the logger's own level
is the outer gate. The pattern is a raw string from [day 42](../day-042-binary-search-idea/README.md)
so the quotation marks need no escaping, and it ends with `,%v}` so the helper's fields close the
object.

Writing lines.

```cpp
int create_user(spdlog::logger& log, const std::string& name, const std::string& password) {
    log_json(log, spdlog::level::debug, {{"msg", "validating input"}, {"name_len", name.size()}});
    if (name.empty()) {
        log_json(log, spdlog::level::warn, {{"msg", "rejected create: blank name"}});
        throw std::invalid_argument("name must not be blank");
    }
    const int user_id = 2;
    log_json(log, spdlog::level::info, {{"msg", "user created"}, {"user_id", user_id}, {"user_name", name}});
    return user_id;
}
```

Constant message, facts as fields. `password` arrives and is never mentioned. The `(void)password;`
in the full program below is how you tell the compiler that is deliberate, so `-Wextra` stays
quiet.

The request wrapper.

```cpp
void handle(spdlog::logger& log, const std::string& name, const std::string& password) {
    request_id = make_request_id();
    const auto start = std::chrono::steady_clock::now();
    try {
        create_user(log, name, password);
    } catch (const std::exception& e) {
        log_json(log, spdlog::level::err, {{"msg", "create failed"}, {"err", e.what()}});
    }
    const auto elapsed = std::chrono::steady_clock::now() - start;
    log_json(log, spdlog::level::info, {{"msg", "request done"},
        {"ms", std::chrono::duration_cast<std::chrono::microseconds>(elapsed).count() / 1000.0}});
}
```

Set the `thread_local` once at the top; every line below carries it. The catch turns the
exception into an `err` line with its message; C++ has no cheap stack trace to attach, which is
one reason the message and the request id matter more here. The done line runs either way.

Build and run:

```bash
g++ -Wall -Wextra -std=c++20 main.cpp -lspdlog -lfmt -o app
./app
```

```text
{"ts":"2026-09-16T21:39:07","level":"info","logger":"users","request_id":"00000001","msg":"user created","user_id":2,"user_name":"Arjun"}
{"ts":"2026-09-16T21:39:07","level":"info","logger":"users","ms":0.031,"msg":"request done","request_id":"00000001"}
{"ts":"2026-09-16T21:39:07","level":"warning","logger":"users","msg":"rejected create: blank name","request_id":"00000002"}
{"ts":"2026-09-16T21:39:07","level":"error","logger":"users","err":"name must not be blank","msg":"create failed","request_id":"00000002"}
{"ts":"2026-09-16T21:39:07","level":"info","logger":"users","ms":0.012,"msg":"request done","request_id":"00000002"}
```

The fields inside each line are alphabetical, because nlohmann sorts keys; the pattern's four
come first because the pattern put them there. `users.log` has the same lines plus the `debug`
one with `"name_len":5`, because the file sink's threshold is lower. If your package manager's
spdlog is header-only, drop `-lspdlog -lfmt` and add `-DSPDLOG_HEADER_ONLY`.

And the reason it is JSON. Every error and its request id, with `jq` if you have it:

```bash
./app | grep '"level":"error"' | jq -r '.request_id + " " + .err'
```

```text
00000002 name must not be blank
```

Then `grep 00000002 users.log` gives every line of that request, including the `debug` one that
never reached the console.

Here is the whole program in one piece, `main.cpp`:

```cpp
#include <spdlog/spdlog.h>
#include <spdlog/sinks/basic_file_sink.h>
#include <spdlog/sinks/stdout_sinks.h>
#include <nlohmann/json.hpp>

#include <atomic>
#include <chrono>
#include <iomanip>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>

using json = nlohmann::json;

thread_local std::string request_id = "-";

std::string make_request_id() {
    static std::atomic<unsigned> counter{0};
    std::ostringstream out;
    out << std::hex << std::setw(8) << std::setfill('0') << ++counter;
    return out.str();
}

void log_json(spdlog::logger& logger, spdlog::level::level_enum level, json fields) {
    fields["request_id"] = request_id;
    const std::string body = fields.dump();
    logger.log(level, "{}", body.substr(1, body.size() - 2));
}

std::shared_ptr<spdlog::logger> make_logger(const std::string& level_name) {
    auto console = std::make_shared<spdlog::sinks::stdout_sink_mt>();
    auto file = std::make_shared<spdlog::sinks::basic_file_sink_mt>("users.log", true);
    file->set_level(spdlog::level::debug);
    auto logger = std::make_shared<spdlog::logger>("users", spdlog::sinks_init_list{console, file});
    logger->set_pattern(R"({"ts":"%Y-%m-%dT%H:%M:%S","level":"%l","logger":"%n",%v})");
    logger->set_level(spdlog::level::from_str(level_name));
    console->set_level(spdlog::level::from_str(level_name));
    return logger;
}

int create_user(spdlog::logger& log, const std::string& name, const std::string& password) {
    (void)password;  // received, never logged
    log_json(log, spdlog::level::debug, {{"msg", "validating input"}, {"name_len", name.size()}});
    if (name.empty()) {
        log_json(log, spdlog::level::warn, {{"msg", "rejected create: blank name"}});
        throw std::invalid_argument("name must not be blank");
    }
    const int user_id = 2;
    log_json(log, spdlog::level::info, {{"msg", "user created"}, {"user_id", user_id}, {"user_name", name}});
    return user_id;
}

void handle(spdlog::logger& log, const std::string& name, const std::string& password) {
    request_id = make_request_id();
    const auto start = std::chrono::steady_clock::now();
    try {
        create_user(log, name, password);
    } catch (const std::exception& e) {
        log_json(log, spdlog::level::err, {{"msg", "create failed"}, {"err", e.what()}});
    }
    const auto elapsed = std::chrono::steady_clock::now() - start;
    log_json(log, spdlog::level::info, {{"msg", "request done"},
        {"ms", std::chrono::duration_cast<std::chrono::microseconds>(elapsed).count() / 1000.0}});
}

int main(int argc, char** argv) {
    auto logger = make_logger(argc > 1 ? argv[1] : "info");
    handle(*logger, "Arjun", "hunter2");
    handle(*logger, "", "hunter2");
    logger->flush();
    return 0;
}
```

The `flush()` at the end matters: spdlog buffers file writes, and a process that exits without
flushing can lose the last lines, which are the ones you wanted.

## 6. How the other two languages do it

**Python**

```python
log.info("user created", extra={"user_id": 2, "user_name": name})
# -> {"ts": ..., "level": "INFO", "logger": "users", "msg": "user created", "request_id": ..., "user_id": 2, "user_name": "Arjun"}
```

The formatter turns `extra` into fields; the call site never sees JSON. The request id is a
`ContextVar`, which follows an async task rather than a thread.

**Go**

```go
log := base.With("request_id", requestID)
log.Info("user created", "user_id", 2, "user_name", name)
```

The JSON handler turns pairs into fields, and the request id rides on the logger object that
`With` returned.

**The difference that matters:** Python and Go have a notion of a field built into the logger;
spdlog has a notion of a formatted line. So the JSON object is yours to build, with nlohmann
doing the escaping, and the request id is a `thread_local` rather than something the logger
carries. The moment your server hands a request to another thread, the Python and Go versions
still know which request it is and the C++ one prints `-`.

## 7. The traps

**The near-miss: the password as a field.**

```cpp
log_json(log, spdlog::level::info, {{"msg", "user created"}, {"user_id", user_id}, {"password", password}});
```

```text
{"ts":"...","level":"info","logger":"users","msg":"user created","password":"hunter2","request_id":"00000001","user_id":2}
```

Into the console, the file, and the aggregator, for as long as retention lasts. The same for
`{"body", req.body}` and `{"headers", ...}`.

**Formatting the JSON by hand.**

```cpp
log.info(R"("msg":"user created","user_name":"{}")", name);
```

Works until `name` is `Ar"jun`, and then the line is not JSON and the aggregator drops it, or
`name` is `{oops}` and spdlog throws a format error. nlohmann's `dump()` escapes both; that is
why the helper exists.

**The message as the format string.**

```cpp
logger.log(level, body);          // body contains "{"
```

```text
terminate called after throwing an instance of 'fmt::v10::format_error'
  what():  invalid format string
```

Always `"{}"` with the text as the argument, never the text as the format string.

**A thread pool between the request and the log.** Hand the create to a worker from
[day 35](../day-035-choosing-the-pattern/README.md) and its lines say `"request_id":"-"`,
because `thread_local` is per thread and the worker's copy was never set. Pass the id into the
job, or pass a logger-like object that carries it, the way Go's `With` does.

**Forgetting `flush` at exit.** The last `error` line of a crashing process is the one you need,
and it is the one still in the buffer. `logger->flush()` in the shutdown path, and
`spdlog::flush_on(spdlog::level::err)` so error lines are never buffered.

**Every sink at `debug`.** A file sink at `debug` on a busy server writes gigabytes a day. The
file sink in this lesson is at `debug` so the lesson can show it; in production the file and
the console usually share a threshold, and `debug` is switched on for one logger, for one
hour, by the setting.

**Two loggers with the same name.** `spdlog::stdout_logger_mt("users")` twice:

```text
terminate called after throwing an instance of 'spdlog::spdlog_ex'
  what():  logger with name 'users' already exists
```

The factory functions register by name. Make the logger once and pass it, or `spdlog::get("users")`.

## 8. Say it out loud

**How it gets asked**

- What do you log, and what must you never log?
- spdlog formats strings. How do you get structured logs out of it?
- Where does the request id live in a C++ server, and when does that break?
- What are sinks for?

**The ninety-second script**

Never: passwords, tokens and API keys, card numbers, full request or response bodies, and
personal data beyond an identifier, because logs live for months in places many people and
systems can read. Always: time, level, logger name, a constant message, the request id, and the
facts as fields. With spdlog, structure is mine to build: a small helper takes a nlohmann object
of fields, adds the request id, dumps it, and passes it as the `{}` argument, and the pattern
supplies the timestamp, level and name so the whole line is one JSON object. nlohmann does the
escaping, which is why I never format JSON with `{}` placeholders by hand. The request id is a
`thread_local` set at the top of the request on the worker thread, which is right for a server
that keeps one request on one thread and wrong the moment work moves to a pool, where the id has
to travel with the job. Sinks are destinations with their own thresholds: console at `info`, a
rotating file at `debug`, and I flush on `err` so an error line is never lost in a buffer.

**The follow-ups**

- **How do you switch on debug in production?** *The logger's level is a setting; an admin
  endpoint calls `set_level(spdlog::level::debug)` on the named logger, for a while, then sets it
  back. spdlog's levels are atomic, so that is safe from another thread.*
- **Why not just log to a file?** *A container's log collector reads standard output. The file
  sink is for a process on a machine you own, and then it is a rotating sink with a size cap,
  because a plain file grows until the disk is full.*
- **How do you get a stack trace on an error?** *Not for free. C++23 has `std::stacktrace`, and
  some platforms have backtrace libraries; in most services the answer is the error message, the
  request id, and enough `debug` lines before the failure to reconstruct it.*

**A model answer**

"Time, level, logger, constant message, request id, and facts as fields, one JSON object per
line. Never a secret, a body, or personal data past an id. In spdlog: a `log_json` helper that
builds a nlohmann object, adds the `thread_local` request id, and passes `dump()` as the `{}`
argument, with a pattern that opens the object and supplies `ts`, `level` and `logger`. Two
sinks with their own thresholds, `flush_on(err)`, and a `flush()` at shutdown. The thing to say
unprompted: `thread_local` breaks when a request crosses threads, and then the id travels with
the job."

## 9. Recall card

- Never log: passwords, tokens, keys, card numbers, bodies, personal data past an id. Always: `ts`, `level`, `logger`, constant `msg`, `request_id`, facts as fields.
- spdlog formats lines, not fields: `log_json` builds a nlohmann object and passes `dump()` as the `{}` argument; the pattern opens the JSON object.
- Sinks are destinations with their own thresholds; `_mt` sinks are thread-safe; `flush_on(err)` and `flush()` at exit.
- `thread_local std::string request_id`, set per request on its worker thread; it prints `-` the moment work crosses threads.
- Never use the message as the format string; a `{` in it throws `fmt::format_error`. Never hand-format JSON with `{}`.
