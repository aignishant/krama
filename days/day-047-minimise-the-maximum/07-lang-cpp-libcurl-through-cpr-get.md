---
day: 47
track: lang-cpp
title: "libcurl through cpr: GET, POST, headers, timeouts"
theme: "HTTP clients"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 047 · C++ — libcurl through cpr: GET, POST, headers, timeouts

**Today's theme:** HTTP clients

**After today you can:** You can call a JSON API with a timeout in each language and handle a 500.

**The interviewer asks it as:** *What goes wrong if you create a new HTTP client for every request?*

---

## 1. What this is, and why it matters

C++ has no HTTP client in its standard library. The one almost everyone uses is libcurl, which
you drove by hand on [day 45](../day-045-rotated-array-search/README.md) with `curl_easy_setopt`
and a write callback. `cpr` is a thin C++ wrapper over libcurl that turns those twelve lines into
one: `cpr::Get(cpr::Url{...})` returns a `cpr::Response` with the status code, the body, and an
error field already filled in. A `cpr::Session` is the same thing kept alive between calls, so the
connection underneath is reused.

At work, this is how a C++ service calls anything over HTTP, from a metrics endpoint to a payment
gateway. In interviews the question in the header is asked directly, and the C++ follow-up is
about ownership: who owns the connection, and what happens to it when the wrapper goes out of
scope. The story is the same as in Python and Go; the way the library tells you about failure is
not.

## 2. The story

Sunita runs a tailoring shop on the ground floor of her building. Every blouse needs buttons, and
the buttons come from Rafiq's wholesale shop on the other side of town, forty minutes away by auto.

In her first month she does it the obvious way. She runs out of blue buttons, pulls the shutter
half down, walks to the corner, flags an auto, haggles over the fare, rides across town, buys one
packet, rides back, and opens up again. Two hours gone. The next day, the same again. By the end of the month she has spent more
time in autos than at the machine.

Her neighbour, who has run a shop for twenty years, watches this for a week and then says the
obvious thing. "Why do you go? Call him."

So Sunita saves Rafiq's number in her phone. Now, when she needs buttons, she calls. The first
few seconds of every call are the same: "Rafiq, it's Sunita from the tailoring shop, I'm calling
about buttons." He knows who she is and what kind of thing she wants before she says another word.
Then she either asks a question, "do you have the dark green in stock", or she places an order,
"send me six packets of the dark green". A question and an order are different kinds of call.

Two more habits come with the phone. If Rafiq does not pick up in a minute, she hangs up and
tries again after lunch. And she has learnt to hear the difference between two kinds of
bad news. Sometimes the line is dead, and she knows nothing at all about whether Rafiq is open.
Sometimes Rafiq picks up and says, "the shutter is jammed, I can't get to the shelves, call back
in an hour". That second one is not a failed call. It is a perfectly good call that carried bad
news, and she plans around it.

After every call she checks two things in her head, always in the same order. Did the call go
through at all? And if it did, what did he actually say? She never lets herself skip the first
question, because on the days the line is dead there is no second answer to hear, only silence
that is easy to mistake for a yes.

## 3. The idea in plain English

The auto ride is a new TCP connection: the three-message handshake from
[day 4](../day-004-the-growth-curves/README.md), and for `https` an encryption exchange on top,
each a round trip of thirty milliseconds across a city or two hundred across an ocean. A fresh
connection per request pays that every time.

The saved number is a **session**, `cpr::Session`. Underneath it is one libcurl easy handle, the
same `CURL*` you cleaned up with `curl_easy_cleanup` on
[day 45](../day-045-rotated-array-search/README.md), and libcurl keeps the connection from the
last request open inside that handle so the next request to the same server can skip the
handshake. That is the **connection reuse** the interview question is about. The free functions
`cpr::Get` and `cpr::Post` build a session, use it once, and destroy it, so they are the auto ride
with a nicer name.

"It's Sunita, calling about buttons" is the **headers**, named lines sent before the body of every
request: `User-Agent` says who is calling and `Accept` says what kind of reply you can read. In
cpr they are a `cpr::Header`, a map from name to value, and set once on the session they go out
with every request.

The question is a **GET**, a request with no body that asks for something; the order is a
**POST**, a request that sends a body, here JSON from [day 40](../day-040-2d-prefix-sums/README.md)
built with nlohmann, and usually changes what the server holds.

Hanging up after a minute is the **timeout**, `cpr::Timeout`, which is libcurl's
`CURLOPT_TIMEOUT_MS` from day 45 under a type. It caps the whole request.

The two questions Sunita asks after every call are the two fields of a `cpr::Response`. Did the
call go through is `r.error`: a dead line, refused or timed out, sets `r.error.code` to something
other than `OK` and leaves `r.status_code` at zero. What did he say is `r.status_code`: a jammed
shutter is a **500**, a real response with a real body in `r.text`, and `r.error` is not set for it
at all. cpr never throws. It never returns a second value. It fills in both fields and hands you
the response, and you check them in that order, every time.

## 4. The picture

```text
cpr::Response r = session.Get();

   +----------------+-------------+--------------------------+
   | r.error.code   | status_code | what happened            |
   +----------------+-------------+--------------------------+
   | OK             | 200         | the call worked          |
   | OK             | 404         | reply: no such user      |
   | OK             | 500         | reply: server is broken  |   <- not an error to cpr
   | OPERATION_     |   0         | dead line: gave up       |
   |   TIMEDOUT     |             |   waiting                |
   | CONNECTION_    |   0         | dead line: nobody home   |
   |   FAILURE      |             |                          |
   +----------------+-------------+--------------------------+
```

Notice that the 500 row has `OK` in the error column. Notice also that the two dead-line rows have
a status of zero, which is why checking `status_code == 200` alone is not enough: zero is not
200, so it fails, but you would not know why.

## 5. The code, built step by step

Every call goes to the fixture in [the practice sheet](03-practice.md). Save it as `fixture.py`,
run `python fixture.py` in a separate terminal, and leave it running. It prints one line per
request with the port the request came from, and that port is how you will see reuse.

Install cpr and nlohmann/json through your package manager: on Debian and Ubuntu they are
`libcpr-dev` and `nlohmann-json3-dev`, on Homebrew `cpr` and `nlohmann-json`, on vcpkg `cpr` and
`nlohmann-json`. The build line is at the end.

The session first. This is the saved phone number.

```cpp
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;
const std::string base = "http://127.0.0.1:8090";

cpr::Session session;
session.SetTimeout(cpr::Timeout{std::chrono::milliseconds{2000}});
session.SetHeader(cpr::Header{{"User-Agent", "krama-day47"}, {"Accept", "application/json"}});
```

`cpr::Session` is a class with a `Set...` method per option. The timeout and the headers are set
once and stay set for every request through this session. `cpr::Header` is built from pairs, the
same brace-initialised map you know from [day 7](../day-007-space-complexity/README.md).

A GET, with the two checks in order.

```cpp
std::optional<json> get_user(cpr::Session& session, int id) {
    session.SetUrl(cpr::Url{base + "/users/" + std::to_string(id)});
    cpr::Response r = session.Get();
    if (r.error) {
        throw std::runtime_error("GET /users failed: " + r.error.message);
    }
    if (r.status_code == 404) return std::nullopt;
    if (r.status_code != 200) {
        throw std::runtime_error("GET /users: status " + std::to_string(r.status_code));
    }
    return json::parse(r.text);
}
```

`SetUrl` changes the address; everything else on the session stays. `session.Get()` performs the
request and returns the response. `r.error` converts to `true` when the call did not go through,
and `r.error.message` is libcurl's own sentence about why. Only after that do you look at
`status_code`. A 404 is an ordinary answer here, so it becomes `std::nullopt` from the
`std::optional` of [day 23](../day-023-palindromes/README.md). Anything else that is not 200
is an error you raise yourself, because cpr will not. Then, and only then, `json::parse(r.text)`.

A POST with a JSON body.

```cpp
json create_user(cpr::Session& session, const std::string& name, const std::string& city) {
    session.SetUrl(cpr::Url{base + "/users"});
    session.UpdateHeader(cpr::Header{{"Content-Type", "application/json"}});
    session.SetBody(cpr::Body{json{{"name", name}, {"city", city}}.dump()});
    cpr::Response r = session.Post();
    if (r.error) throw std::runtime_error("POST /users failed: " + r.error.message);
    if (r.status_code != 201) {
        throw std::runtime_error("POST /users: status " + std::to_string(r.status_code));
    }
    return json::parse(r.text);
}
```

`json{...}.dump()` is day 40's serialiser, giving a `std::string`, which `cpr::Body` wraps.
`UpdateHeader` adds one header to the ones already set without replacing them; `SetHeader` would
have thrown away `User-Agent` and `Accept`. The `Content-Type` is not set for you, and the fixture
answers `415` without it.

The two kinds of bad news, told apart.

```cpp
session.SetUrl(cpr::Url{base + "/fail"});
cpr::Response r = session.Get();
if (!r.error && r.status_code == 500) {
    std::cout << "server error: 500 " << json::parse(r.text)["error"].get<std::string>() << '\n';
}

session.SetUrl(cpr::Url{base + "/slow"});
r = session.Get();
if (r.error.code == cpr::ErrorCode::OPERATION_TIMEDOUT) {
    std::cout << "gave up waiting on /slow after 2 seconds\n";
}
```

The 500 arrives with `r.error` clear and a body you can parse. The timeout arrives with
`r.error.code == cpr::ErrorCode::OPERATION_TIMEDOUT`, `r.status_code == 0`, and an empty `r.text`.
Two different fields for two different kinds of bad news.

Save as `main.cpp` and build:

```bash
g++ -Wall -Wextra -std=c++20 main.cpp -lcpr -lcurl -o client
./client
```

If you would rather use CMake from [day 44](../day-044-first-and-last-occurrence/README.md), the
target is `cpr::cpr`: `find_package(cpr CONFIG REQUIRED)` and
`target_link_libraries(client PRIVATE cpr::cpr nlohmann_json::nlohmann_json)`.

With the fixture up it prints:

```text
user 1: Meera from Pune
user 99: not found
created id 2 -> {"city":"Delhi","id":2,"name":"Arjun"}
server error: 500 database down
gave up waiting on /slow after 2 seconds
```

The keys in the created line are alphabetical because nlohmann's `dump` sorts them. The fixture's
terminal:

```text
GET  /users/1 from port 51702
GET  /users/99 from port 51702
POST /users from port 51702
GET  /fail from port 51702
GET  /slow from port 51702
```

One port, five requests. The session's one handle dialled once.

Here is the whole program in one piece, `main.cpp`:

```cpp
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>

#include <chrono>
#include <iostream>
#include <optional>
#include <stdexcept>
#include <string>

using json = nlohmann::json;

const std::string base = "http://127.0.0.1:8090";

std::optional<json> get_user(cpr::Session& session, int id) {
    session.SetUrl(cpr::Url{base + "/users/" + std::to_string(id)});
    cpr::Response r = session.Get();
    if (r.error) {
        throw std::runtime_error("GET /users failed: " + r.error.message);
    }
    if (r.status_code == 404) return std::nullopt;
    if (r.status_code != 200) {
        throw std::runtime_error("GET /users: status " + std::to_string(r.status_code));
    }
    return json::parse(r.text);
}

json create_user(cpr::Session& session, const std::string& name, const std::string& city) {
    session.SetUrl(cpr::Url{base + "/users"});
    session.UpdateHeader(cpr::Header{{"Content-Type", "application/json"}});
    session.SetBody(cpr::Body{json{{"name", name}, {"city", city}}.dump()});
    cpr::Response r = session.Post();
    if (r.error) throw std::runtime_error("POST /users failed: " + r.error.message);
    if (r.status_code != 201) {
        throw std::runtime_error("POST /users: status " + std::to_string(r.status_code));
    }
    return json::parse(r.text);
}

int main() {
    cpr::Session session;
    session.SetTimeout(cpr::Timeout{std::chrono::milliseconds{2000}});
    session.SetHeader(cpr::Header{{"User-Agent", "krama-day47"}, {"Accept", "application/json"}});

    try {
        const auto user = get_user(session, 1);
        std::cout << "user 1: " << (*user)["name"].get<std::string>() << " from "
                  << (*user)["city"].get<std::string>() << '\n';

        if (!get_user(session, 99)) std::cout << "user 99: not found\n";

        const json created = create_user(session, "Arjun", "Delhi");
        std::cout << "created id " << created["id"].get<int>() << " -> " << created.dump() << '\n';
    } catch (const std::runtime_error& err) {
        std::cerr << err.what() << '\n';
        return 1;
    }

    session.SetUrl(cpr::Url{base + "/fail"});
    cpr::Response r = session.Get();
    if (!r.error && r.status_code == 500) {
        std::cout << "server error: 500 " << json::parse(r.text)["error"].get<std::string>() << '\n';
    }

    session.SetUrl(cpr::Url{base + "/slow"});
    r = session.Get();
    if (r.error.code == cpr::ErrorCode::OPERATION_TIMEDOUT) {
        std::cout << "gave up waiting on /slow after 2 seconds\n";
    } else if (r.error) {
        std::cerr << "GET /slow failed: " << r.error.message << '\n';
    }
    return 0;
}
```

## 6. How the other two languages do it

**Python**

```python
with httpx.Client(base_url=BASE, timeout=2.0, headers=headers) as client:
    try:
        response = client.get("/users/1")     # dead line raises here
        response.raise_for_status()           # 500 raises here, if you ask
        return response.json()
    except httpx.HTTPError as err:
        ...
```

One `httpx.Client`. A dead line is an exception thrown by the call itself; a 500 is a normal
response until `raise_for_status` turns it into an exception too.

**Go**

```go
client := &http.Client{Timeout: 2 * time.Second}
resp, err := client.Get(base + "/users/1")
if err != nil {
	return nil, err // dead line
}
defer resp.Body.Close()
if resp.StatusCode != http.StatusOK { /* jammed shutter */ }
```

One `http.Client`. A dead line is the second return value; a 500 is `resp` with `err == nil`, and
the body is a stream you must close.

**The difference that matters:** cpr is the only one of the three where a dead line is neither
thrown nor returned. It is a field, `r.error`, sitting next to `r.status_code` on a response that
looks exactly like a successful one. A Python habit of wrapping the call in `try`, or a Go habit
of checking a second value, catches nothing here, and a timed-out request walks straight into your
`status_code != 200` branch with a status of zero and no explanation.

## 7. The traps

**The near-miss: the free function.** This is the auto ride, and it reads beautifully.

```cpp
for (int i = 0; i < 3; ++i) {
    cpr::Response r = cpr::Get(cpr::Url{base + "/users/1"}, cpr::Timeout{2000});
    std::cout << json::parse(r.text)["name"].get<std::string>() << '\n';
}
```

It prints `Meera` three times. The fixture shows the truth:

```text
GET  /users/1 from port 51703
GET  /users/1 from port 51704
GET  /users/1 from port 51705
```

Each `cpr::Get` builds a `cpr::Session`, performs one request, and destroys it, and the libcurl
handle with its open connection goes with it. Three handshakes for three identical calls. Nothing
in the output says so.

**Checking the status before the error.** The order matters.

```cpp
cpr::Response r = session.Get();
if (r.status_code != 200) {
    std::cerr << "status " << r.status_code << '\n';   // prints: status 0
    return 1;
}
```

On a timeout this prints `status 0` and exits, and you spend an hour looking for a server that
returns status zero. Check `r.error` first; its message would have said:

```text
Operation timed out after 2008 milliseconds with 0 bytes received
```

That is libcurl's own sentence, in `r.error.message`, with `r.error.code` equal to
`cpr::ErrorCode::OPERATION_TIMEDOUT`.

**Nobody home.** Point the session at a port with no server:

```text
Failed to connect to 127.0.0.1 port 9999 after 2026 ms: Could not connect to server
```

`r.error.code` is `cpr::ErrorCode::CONNECTION_FAILURE`. The millisecond count varies by machine
and is near zero on Linux. It is the [day 46](../day-046-binary-search-on-the-answer/README.md)
`connection refused`, seen from the client.

**Parsing a body that is not JSON.** A proxy in front of the server answers with an HTML
maintenance page and a 200, and `json::parse(r.text)` throws:

```text
terminate called after throwing an instance of 'nlohmann::json_abi_v3_11_3::detail::parse_error'
  what():  [json.exception.parse_error.101] parse error at line 1, column 1: syntax error while parsing value - invalid literal; last read: '<'
```

Check `r.header["content-type"]` before parsing, or catch `json::parse_error` and log the first
hundred characters of `r.text`.

**Comparing the status to a string.** `status_code` is a `long`:

```cpp
if (r.status_code == "200") { ... }
```

```text
main.cpp:18:23: error: ISO C++ forbids comparison between pointer and integer [-fpermissive]
```

**Forgetting to link.** Build with the header found but the library not named:

```text
/usr/bin/ld: /tmp/ccA1b2C3.o: in function `main':
main.cpp:(.text+0x4a): undefined reference to `cpr::Session::Session()'
collect2: error: ld returned 1 exit status
```

`#include <cpr/cpr.h>` finds the declarations; `-lcpr` finds the code. You need both, and with
`-lcurl` after it, because cpr itself calls libcurl.

## 8. Say it out loud

**How it gets asked**

- What goes wrong if you create a new HTTP client for every request?
- In C++, what owns the connection, and when is it closed?
- The downstream returns a 500. What does cpr give you?
- How do you tell a timeout from a 500 with cpr?

**The ninety-second script**

A new client per request means a new TCP connection per request: a handshake, plus the TLS
exchange on HTTPS, before any data moves, which is one to three round trips of thirty to two
hundred milliseconds on every call. In C++ with cpr, that is exactly what the free functions
`cpr::Get` and `cpr::Post` do: each one builds a session, runs one request, and destroys the
session and the libcurl handle inside it, connection and all. So I keep one `cpr::Session` alive
for the life of the program, or one per downstream service, with the timeout and the common
headers set once. Its libcurl handle keeps the connection open between requests, so the second
call to the same host skips the handshake. Then, on every response, two checks in order. First
`r.error`, because a dead line, refused or timed out, is not thrown and not returned, it is a
field on the response, with `status_code` left at zero. Second `r.status_code`, because a 500 is
a normal response with `r.error` clear, and cpr will never treat it as a failure for me.

**The follow-ups**

- **Who owns the connection?** *The `CURL*` easy handle inside the session, which the session
  owns and cleans up in its destructor, RAII as on
  [day 13](../day-013-reverse-and-rotate/README.md). While the session lives, libcurl keeps the last
  connection open inside that handle. Destroy the session and the connection closes with it.*
- **Is a session safe to share between threads?** *No. One easy handle may be used by one thread
  at a time, as on day 45. I give each worker its own session, or keep a small pool of sessions
  behind a mutex, and never let two threads call `Get` on the same one.*
- **What do you do on a 500?** *Retry a GET, with a short growing wait between attempts and a cap
  on the count. Not a POST that creates something, unless the server takes a key that makes a
  repeat harmless. After the last attempt I raise or return an error with the status in it.*

**A model answer**

"One `cpr::Session` per process or per downstream, with `SetTimeout` and `SetHeader` done once,
and `SetUrl` per call. It wraps one libcurl handle, and the handle keeps the connection alive
between calls, so I am not paying a handshake per request the way `cpr::Get` does. On every
response I check `r.error` first, because a timeout or a refused connection is a field, not an
exception, and it leaves `status_code` at zero. Then I check `status_code`, because a 500 comes
back with no error set and a body I can read out of `r.text`."

## 9. Recall card

- One `cpr::Session` kept alive; `cpr::Get(...)` and `cpr::Post(...)` build and destroy a session, and its connection, every call.
- `SetTimeout`, `SetHeader` once; `SetUrl`, `SetBody`, `UpdateHeader` per call; `Get()` or `Post()` returns a `cpr::Response`.
- Check `r.error` first: a dead line sets `r.error.code` and leaves `status_code` at 0. Then check `status_code`: a 500 has `r.error` clear.
- `OPERATION_TIMEDOUT` is the timeout; `CONNECTION_FAILURE` is nobody home; `r.error.message` is libcurl's sentence.
- Link with `-lcpr -lcurl`; `#include <cpr/cpr.h>` alone ends in `undefined reference to cpr::Session::Session()`.
