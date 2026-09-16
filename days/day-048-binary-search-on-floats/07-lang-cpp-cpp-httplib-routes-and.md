---
day: 48
track: lang-cpp
title: "cpp-httplib: routes and handlers"
theme: "HTTP servers"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 048 · C++ — cpp-httplib: routes and handlers

**Today's theme:** HTTP servers

**After today you can:** You can serve a JSON endpoint on a port in each language and hit it with curl.

**The interviewer asks it as:** *Walk me through how your server handles one request.*

---

## 1. What this is, and why it matters

C++ has no HTTP server in its standard library, and the lightest one people reach for is
cpp-httplib: a single header, `httplib.h`, that gives you a `httplib::Server`, a method per HTTP
verb to register a route, and a lambda per route that receives a `Request` and fills in a
`Response`. Under it is the same socket, bind, listen and accept you wrote on
[day 46](../day-046-binary-search-on-the-answer/README.md), with a thread pool serving
connections.

At work, a C++ service that needs a health endpoint, a metrics page or a small JSON API usually
does it with this or with a heavier framework built the same way. In interviews the question is
the same as in the other two languages, and the C++ answer has one extra step worth saying out
loud: which thread your handler is running on, and what that means for anything it touches.

## 2. The story

Rekha runs the front desk at a small dental clinic on the second floor of a shopping complex. The
clinic opens at nine. Before that, the door is locked and anyone who climbs the stairs finds a
closed shutter and goes back down. At nine she unlocks it, switches on the light over the desk,
and from then on she is the first person anyone meets.

A man comes in holding a folded slip. Rekha does not guess what he wants. She asks. "Are you here
to see someone, or are you here to register?" If he is here to see a doctor, she asks which one.
Dr Iyer is in room two, Dr Bhat is in room three. If he asks for a Dr Menon, she says, without
looking anything up, "there is no Dr Menon here", and that is the end of it. He does not get sent
to a room to find out for himself.

A woman comes in to register as a new patient. Rekha hands her the form: name, phone number,
date of birth. The woman fills in her name and hands it back. Rekha looks at it for two seconds
and hands it straight back. "Phone number, please." She does not carry a half-filled form to the
back office and let them discover the gap an hour later. Nobody behind the desk ever sees a form
with something missing, because Rekha does not let one through.

When a form is complete, Rekha writes the new patient's number on it, files it, and gives the
woman a small printed card with exactly three things on it: her number, her name, and the
clinic's phone line. The same card, every time.

On busy mornings Rekha is not alone. There are four of her, four chairs behind one long desk,
and whoever is free takes the next person through the door. It works, until two of them reach
for the same patient file at the same moment. So the file cabinet has one key on a hook, and you
take the key before you open the drawer and hang it back when you are done. Nobody argues about it, because
the one time they skipped it two patients ended up with the same number.

At six the light goes off and the shutter comes down. A boy who arrives at ten past six knocks
twice and leaves.

## 3. The idea in plain English

The unlocked door with the light on is `svr.listen("127.0.0.1", 8000)`. It is the `socket`,
`bind`, `listen` and `accept` loop from [day 46](../day-046-binary-search-on-the-answer/README.md),
done for you, and it blocks for as long as the server runs. It returns `false` if it could not
bind.

"Which doctor?" is the **route table**. `svr.Get(path, handler)` and `svr.Post(path, handler)`
each add one row: a method, a path pattern, and a function to call. A path of `/users/:id` has a
**path parameter**: whatever sits in the `:id` position is captured, as a string, into
`req.path_params`.

The function is a **handler**, a lambda that takes `const httplib::Request&` and
`httplib::Response&`. The request carries `req.method`, `req.path`, and `req.body` as a
`std::string`. The response is two things you set: `res.status`, an `int`, and the body through
`res.set_content(text, content_type)`.

"There is no Dr Menon here" is `res.status = 404` and a JSON body you build with nlohmann from
[day 40](../day-040-2d-prefix-sums/README.md). Nothing builds it for you.

The registration form is `json::parse(req.body)`. That throws if the body is not JSON, so it goes
in a `try`. It does not know that `city` is required; `body.contains("city")` is a question you
ask, and "phone number, please" is an `if` you write.

The four chairs are the **thread pool**. cpp-httplib serves each connection on a worker thread, so
two handlers can run at the same instant. The key on the hook is a `std::mutex` from
[day 31](../day-031-fixed-window/README.md) around the map of users, taken with a `std::lock_guard`
so it is released however the handler leaves.

## 4. The picture

```mermaid
sequenceDiagram
    participant C as curl
    participant L as svr.listen (accept loop)
    participant W as worker thread
    participant H as POST /users lambda
    C->>L: POST /users {"name": "Arjun", "city": "Delhi"}
    L->>W: hand the connection to a free worker
    W->>W: parse request, match "POST /users"
    W->>H: handler(req, res)
    H->>H: json::parse(req.body)? contains("city")? lock the map
    H->>H: res.status = 201; res.set_content(...)
    H->>W: return
    W->>C: HTTP/1.1 201 Created
```

Notice the worker thread. The accept loop hands the connection off and goes straight back to
accepting, the way Arjun went back to the door on day 46. Your lambda runs on the worker, next to
other lambdas on other workers.

## 5. The code, built step by step

cpp-httplib is a single header. Install it through your package manager, `libcpp-httplib-dev`
on Debian and Ubuntu, `cpp-httplib` on Homebrew and vcpkg, or download `httplib.h` and put it
next to `main.cpp`. nlohmann/json is the same as on day 40.

The includes, the store, and its key.

```cpp
#include <httplib.h>
#include <nlohmann/json.hpp>

#include <iostream>
#include <map>
#include <mutex>
#include <string>

using json = nlohmann::json;

std::map<int, json> users = {{1, {{"id", 1}, {"name", "Meera"}, {"city", "Pune"}}}};
std::mutex users_mutex;
```

A `std::map` of id to JSON object stands in for a database until
[day 53](../day-053-merge-sort/README.md). The mutex sits next to it, because it will be read and
written from several worker threads at once.

A helper to answer with JSON, because every route needs one.

```cpp
void reply(httplib::Response& res, int status, const json& body) {
    res.status = status;
    res.set_content(body.dump(), "application/json");
}
```

`set_content` takes the body text and the content type. The status is a plain `int` field.

The GET route.

```cpp
svr.Get("/users/:id", [](const httplib::Request& req, httplib::Response& res) {
    int id = 0;
    try {
        id = std::stoi(req.path_params.at("id"));
    } catch (const std::invalid_argument&) {
        return reply(res, 400, {{"error", "id must be a number"}});
    }
    std::lock_guard<std::mutex> lock(users_mutex);
    auto it = users.find(id);
    if (it == users.end()) return reply(res, 404, {{"error", "no such user"}});
    reply(res, 200, it->second);
});
```

`req.path_params.at("id")` is the captured string, `"1"` or `"abc"`. `std::stoi` throws
`std::invalid_argument` on `"abc"`, and that becomes a 400. The `lock_guard` holds the key for the
rest of the lambda, and `find` on the map is the 404.

The POST route.

```cpp
svr.Post("/users", [](const httplib::Request& req, httplib::Response& res) {
    json body;
    try {
        body = json::parse(req.body);
    } catch (const json::parse_error&) {
        return reply(res, 400, {{"error", "body is not JSON"}});
    }
    if (!body.contains("name") || !body.contains("city")) {
        return reply(res, 400, {{"error", "name and city are required"}});
    }
    std::lock_guard<std::mutex> lock(users_mutex);
    int id = static_cast<int>(users.size()) + 1;
    users[id] = {{"id", id}, {"name", body["name"]}, {"city", body["city"]}};
    reply(res, 201, users[id]);
});
```

Parse, check the fields, take the key, write, answer 201. The new object is built from the two
fields you checked, not by copying `body`, so a caller who sends `"id": 1` does not overwrite
Meera.

Listening.

```cpp
int main() {
    httplib::Server svr;
    // ... the two routes above ...
    std::cout << "listening on 127.0.0.1:8000\n";
    if (!svr.listen("127.0.0.1", 8000)) {
        std::cerr << "could not bind 127.0.0.1:8000\n";
        return 1;
    }
    return 0;
}
```

`listen` blocks. It returns `false` if the port could not be bound, which is the one error it
reports; there is no `errno` message from it, so the line after it is yours.

Build and run:

```bash
g++ -Wall -Wextra -std=c++20 main.cpp -o server
./server
```

```text
listening on 127.0.0.1:8000
```

In a second terminal:

```bash
curl -i http://127.0.0.1:8000/users/1
curl -i http://127.0.0.1:8000/users/99
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"Arjun","city":"Delhi"}' http://127.0.0.1:8000/users
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"Arjun"}' http://127.0.0.1:8000/users
```

The status lines and bodies, one pair per command:

```text
HTTP/1.1 200 OK
{"city":"Pune","id":1,"name":"Meera"}

HTTP/1.1 404 Not Found
{"error":"no such user"}

HTTP/1.1 201 Created
{"city":"Delhi","id":2,"name":"Arjun"}

HTTP/1.1 400 Bad Request
{"error":"name and city are required"}
```

The keys are alphabetical because nlohmann's `dump` sorts them. The server's terminal prints
nothing per request; a logger is [day 49](../day-049-peak-finding/README.md).

Here is the whole program in one piece, `main.cpp`:

```cpp
#include <httplib.h>
#include <nlohmann/json.hpp>

#include <iostream>
#include <map>
#include <mutex>
#include <stdexcept>
#include <string>

using json = nlohmann::json;

std::map<int, json> users = {{1, {{"id", 1}, {"name", "Meera"}, {"city", "Pune"}}}};
std::mutex users_mutex;

void reply(httplib::Response& res, int status, const json& body) {
    res.status = status;
    res.set_content(body.dump(), "application/json");
}

int main() {
    httplib::Server svr;

    svr.Get("/users/:id", [](const httplib::Request& req, httplib::Response& res) {
        int id = 0;
        try {
            id = std::stoi(req.path_params.at("id"));
        } catch (const std::invalid_argument&) {
            return reply(res, 400, {{"error", "id must be a number"}});
        }
        std::lock_guard<std::mutex> lock(users_mutex);
        auto it = users.find(id);
        if (it == users.end()) return reply(res, 404, {{"error", "no such user"}});
        reply(res, 200, it->second);
    });

    svr.Post("/users", [](const httplib::Request& req, httplib::Response& res) {
        json body;
        try {
            body = json::parse(req.body);
        } catch (const json::parse_error&) {
            return reply(res, 400, {{"error", "body is not JSON"}});
        }
        if (!body.contains("name") || !body.contains("city")) {
            return reply(res, 400, {{"error", "name and city are required"}});
        }
        std::lock_guard<std::mutex> lock(users_mutex);
        int id = static_cast<int>(users.size()) + 1;
        users[id] = {{"id", id}, {"name", body["name"]}, {"city", body["city"]}};
        reply(res, 201, users[id]);
    });

    std::cout << "listening on 127.0.0.1:8000\n";
    if (!svr.listen("127.0.0.1", 8000)) {
        std::cerr << "could not bind 127.0.0.1:8000\n";
        return 1;
    }
    return 0;
}
```

## 6. How the other two languages do it

**Python**

```python
@app.post("/users", response_model=UserOut, status_code=201)
def create_user(body: UserIn) -> UserOut:
    new_id = max(users) + 1
    users[new_id] = UserOut(id=new_id, name=body.name, city=body.city)
    return users[new_id]
```

The parse, the field check and the status are all in the decorator and the type hint. A missing
`city` is a 422 with the field named, and the function never runs.

**Go**

```go
var body User
if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
	writeJSON(w, http.StatusBadRequest, map[string]string{"error": "body is not JSON"})
	return
}
if body.Name == "" || body.City == "" { /* 400 */ }
```

The same three steps as C++, with a `nil` error instead of a caught exception, and a zero-value
string instead of a missing key.

**The difference that matters:** in C++ your handler is on a worker thread, and the library does
not say so loudly. FastAPI runs plain `def` routes on a thread pool too, but the map you touch in
Python is protected by the interpreter's own lock; Go's handlers are goroutines and the race
detector will tell you. In cpp-httplib the shared map with no mutex compiles, runs, and passes
every single-client test, and corrupts itself the first time two requests land together.

## 7. The traps

**The near-miss: no mutex.** Delete `users_mutex` and the two `lock_guard` lines. Everything in
section 5 still works, because `curl` sends one request at a time. Send fifty POSTs at once:

```bash
seq 50 | xargs -P 10 -I{} curl -s -o /dev/null -X POST -H "Content-Type: application/json" -d '{"name":"u{}","city":"x"}' http://127.0.0.1:8000/users
```

Two workers read `users.size()` as 7 at the same moment, both write id 8, and one user is gone.
Or the map's internal tree is rebalanced by two threads at once and the process dies:

```text
Segmentation fault (core dumped)
```

No compiler warning, no error message, and it may take a hundred runs to happen once.

**A path parameter that is not an int.** `curl http://127.0.0.1:8000/users/abc` without the
`try`:

```text
terminate called after throwing an instance of 'std::invalid_argument'
  what():  stoi
```

The whole server exits, taking every other connection with it. Every `stoi` on caller input is
inside a `try`.

**A body that is not JSON.** `-d 'hello'` without the `try` around `parse`:

```text
terminate called after throwing an instance of 'nlohmann::json_abi_v3_11_3::detail::parse_error'
  what():  [json.exception.parse_error.101] parse error at line 1, column 1: syntax error while parsing value - invalid literal; last read: 'h'
```

Same lesson. An uncaught exception in a handler is the process ending, not a 500.

**The port is taken.** Start it twice:

```text
listening on 127.0.0.1:8000
could not bind 127.0.0.1:8000
```

That second line is yours; `listen` only returned `false`. Print something, or you will stare at a
server that exited with no message.

**`set_content` with one argument.**

```cpp
res.set_content(body.dump());
```

```text
main.cpp:17:9: error: no matching function for call to 'httplib::Response::set_content(std::string)'
```

The content type is not optional. Without `"application/json"` a caller like yesterday's
`httpx` will refuse to parse the body.

**Forgetting `:` in the route.** `svr.Get("/users/id", ...)` matches the literal path
`/users/id` and nothing else; `/users/1` gets an empty 404 and `path_params` is never filled.

## 8. Say it out loud

**How it gets asked**

- Walk me through how your server handles one request.
- Which thread is your handler running on?
- What happens if your handler throws?
- Why did the process die under load when it worked fine with curl?

**The ninety-second script**

`svr.listen` binds the port and runs an accept loop. Each accepted connection goes to a worker
thread from a pool, and the accept loop goes straight back to accepting. The worker parses the
request line and headers, and matches the method and path against the route table; `/users/:id`
captures the id as a string into `path_params`. It calls my lambda with the request and an empty
response. In the lambda I convert the id inside a `try`, because `stoi` throws on bad input and an
uncaught exception ends the process. For a POST I `json::parse` the body inside a `try` for the
same reason, and check the required fields with `contains`, because the parser does not know what
is required. I take a `lock_guard` on the mutex before touching the map, because another worker
may be in the same lambda. I set `res.status` and `set_content` with the JSON and its content
type. The lambda returns, the worker writes the response, and serves the next request on that
connection or closes it.

**The follow-ups**

- **How many worker threads, and what if they are all busy?** *cpp-httplib defaults to a pool of
  a few threads, eight on most builds, set through `new_task_queue`. When all are busy, accepted
  connections wait in the queue; if my handlers block on a slow database, the whole server stalls,
  which is why handlers should be short.*
- **What does the caller see on an exception?** *By default the connection drops, because the
  process is gone. cpp-httplib has `set_exception_handler` to turn a caught exception into a 500,
  and I set one, but I still wrap the calls I know can throw so I can answer with the right 400.*
- **How do you stop it?** *`svr.stop()` from another thread, typically a signal handler, makes
  `listen` return. In-flight handlers finish, then the pool joins.*

**A model answer**

"Bind and listen, accept loop, worker thread per connection from a pool. The worker parses,
matches method and path, captures `:id`, and calls my lambda. In the lambda: `stoi` and
`json::parse` in `try` blocks because a throw ends the process, `contains` for required fields
because the parser does not know them, a `lock_guard` on the shared map because I am on a worker
next to other workers, then status and `set_content` with the content type. Every error branch
returns after `reply`. The near-miss is the missing mutex: fine under curl, a segfault under
load."

## 9. Recall card

- `httplib::Server svr; svr.Get("/users/:id", lambda); svr.Post("/users", lambda); svr.listen("127.0.0.1", 8000)` blocks and returns `false` if it cannot bind.
- A handler is `(const httplib::Request& req, httplib::Response& res)`; `req.path_params.at("id")`, `req.body`, `res.status`, `res.set_content(text, "application/json")`.
- Handlers run on worker threads. Shared state gets a `std::mutex` and a `std::lock_guard`, or it segfaults under load.
- `std::stoi` and `json::parse` throw; an uncaught throw in a handler ends the process. `try` around both.
- `contains("city")` is the required-field check; nothing checks it for you. Every error branch is `return reply(res, 4xx, ...)`.
