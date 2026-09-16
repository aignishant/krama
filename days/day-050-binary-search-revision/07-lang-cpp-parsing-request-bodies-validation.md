---
day: 50
track: lang-cpp
title: "Parsing request bodies, validation, and consistent error shapes"
theme: "Designing a JSON API"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 050 · C++ — Parsing request bodies, validation, and consistent error shapes

**Today's theme:** Designing a JSON API

**After today you can:** You can build a CRUD endpoint set with proper status codes and error bodies, in each language.

**The interviewer asks it as:** *What should a 400 response body look like?*

---

## 1. What this is, and why it matters

In C++ with cpp-httplib and nlohmann/json, a request body arrives as a string, `json::parse`
turns it into a tree, and from there every question is yours: is the key there, is it the right
type, is the value in range. Today you write the three pieces a JSON API is made of: a `parse`
step that turns a bad body into a 400 instead of a crash, a `validate` function that returns every
problem at once, and one `error` function that produces the same body for every failure. Then
the five CRUD routes, each a few lines, because the three pieces do the work.

At work, this is the file in every C++ service that decides whether other teams like calling it.
In interviews, "what should a 400 response body look like" has the same answer in every language;
the C++ twist is that nlohmann makes the wrong thing easy, because `body["age"]` on a missing key
does not fail, it creates the key.

## 2. The story

Farida works the parcel counter at a courier office near the railway station. Two hundred people
a day put a parcel and a form on her counter, and about thirty of them get the parcel back.

In her first month, she handed parcels back with a sentence. "This won't do." "Fix the address."
"Too heavy." People argued, or came back with the same form and a different mistake, or stood
there asking which line she meant. The queue behind them grew.

Her manager gave her a pad of printed slips. Every slip has the same three boxes. The first says
what kind of problem it is, in one of five fixed words: incomplete, unreadable, too heavy, not
allowed, or our fault. The second says which line of the form, by its number. The third says what
to do about it. Farida ticks and fills, tears the slip off, and hands it over with the parcel.
Nobody argues with a slip. They read it, fix the one thing, and come back.

She also stopped mixing outcomes. A parcel that is accepted gets a receipt with a tracking number,
and nothing else. A parcel for a town the company does not deliver to gets a slip that says
"not allowed", not a receipt with a note on the back.

The other thing the manager insisted on: Farida checks the whole form before saying anything. If
the address is missing and the phone number has letters in it, the slip says both. A customer
who fixes one and comes back to be told about the other is a customer who does not come back a
third time.

There is one mistake Farida made exactly once. A form came in with the "declared value" box empty,
and instead of asking, she wrote a zero in it herself so the form would look complete, and passed
it through. The parcel was lost, and the customer had wanted to declare it at twenty thousand.
Now, when a box is empty, she does not fill it. She looks, she sees that it is empty, and she
says so on the slip. Looking is not the same as touching.

## 3. The idea in plain English

The printed slip is the **error body**: `{"error": {"code": ..., "message": ..., "fields": [...]}}`.
In C++ it is one function, `error(res, status, code, message, fields)`, that builds the JSON and
sets the status and content type. Every route calls it. No route builds error JSON inline.

The five fixed words are **status codes**, by kind of outcome: `200` read or replace, `201`
create, `204` delete with no body, `400` body fails the rules, `404` path names something absent,
`409` body fine but state says no, `500` our fault.

Checking the whole form is a **validate** function that returns a `std::vector` of field errors.
Each rule is an `if` that pushes back. The route calls it once, and if the vector is not empty,
answers 400 with the whole vector. No early return inside `validate`.

Looking without touching is the difference between `body.contains("age")` and `body["age"]`.
On a non-const `json`, `operator[]` with a missing key **inserts a null** at that key and returns
it, which is Farida writing a zero in the empty box. On a `const json&` there is nothing to
insert into, so the same call is undefined behaviour, an assertion in a debug build and garbage
in a release one. `contains` looks; `at` looks and throws if absent; `operator[]` touches. `validate` takes
the body by `const&`, and uses `contains` and `at`, and never `[]`.

Type questions are `is_string()`, `is_number_integer()`, `is_boolean()`. A JSON object has no
schema until you ask these, so each field gets three checks in order: is it there, is it the
right type, is the value acceptable. The `else if` chain stops after the first failure **for that
field**, because "must be an integer" and "must be between 0 and 150" about the same value is
noise; the vector still collects across fields.

The five routes are **CRUD**: create, read, update, delete, over `/users`.

## 4. The picture

```text
outcome                         status   body
---------------------------------------------------------------------------
read one, found                  200     {"id": 1, "name": ..., ...}
created                          201     the created thing, with its id
replaced                         200     the replaced thing
deleted                          204     (nothing)
path names something missing     404     {"error": {"code": "not_found", "message": ...}}
body fails a rule                400     {"error": {"code": "validation_error",
                                                    "message": ..., "fields": [...]}}
body fine, state says no         409     {"error": {"code": "conflict", "message": ...}}
our fault                        500     {"error": {"code": "internal", "message": ...}}
```

Notice that the error rows share everything but `code`, and `fields` appears on one of them. The
`error` function has an optional last parameter for exactly that row.

## 5. The code, built step by step

Start from day 49's `main.cpp`, keeping `reply`, the mutex, and the `timed` wrapper if you like.

The error shape, in one function.

```cpp
struct FieldError {
    std::string field;
    std::string message;
};

void error(httplib::Response& res, int status, const std::string& code, const std::string& message,
           const std::vector<FieldError>& fields = {}) {
    json body = {{"error", {{"code", code}, {"message", message}}}};
    if (!fields.empty()) {
        json list = json::array();
        for (const auto& f : fields) list.push_back({{"field", f.field}, {"message", f.message}});
        body["error"]["fields"] = list;
    }
    reply(res, status, body);
}
```

A default argument of an empty vector means a 404 calls it with four arguments and a validation
failure with five. `json::array()` makes an empty list explicitly; without it, an empty
`json` is `null`.

The rules, all of them.

```cpp
std::string trimmed(const json& value) {
    std::string s = value.get<std::string>();
    const auto first = s.find_first_not_of(' ');
    if (first == std::string::npos) return "";
    return s.substr(first, s.find_last_not_of(' ') - first + 1);
}

std::vector<FieldError> validate(const json& body) {
    std::vector<FieldError> errs;
    for (const char* key : {"name", "city"}) {
        if (!body.contains(key)) errs.push_back({key, "is required"});
        else if (!body.at(key).is_string()) errs.push_back({key, "must be a string"});
        else if (trimmed(body.at(key)).empty()) errs.push_back({key, "must not be blank"});
        else if (trimmed(body.at(key)).size() > 50) errs.push_back({key, "must be 50 characters or fewer"});
    }
    if (!body.contains("age")) errs.push_back({"age", "is required"});
    else if (!body.at("age").is_number_integer()) errs.push_back({"age", "must be an integer"});
    else if (body.at("age") < 0 || body.at("age") > 150) errs.push_back({"age", "must be between 0 and 150"});
    return errs;
}
```

`const json& body`, `contains`, `at`. Never `[]`. The `for` over two keys is the same three
checks for `name` and `city` without writing them twice. `body.at("age") < 0` works because
nlohmann compares a number-valued `json` with an `int`.

Parsing, with the crash turned into a 400.

```cpp
bool parse_body(const httplib::Request& req, httplib::Response& res, json& out) {
    if (req.body.size() > 1 << 20) {
        error(res, 413, "too_large", "body must be under 1 MB");
        return false;
    }
    try {
        out = json::parse(req.body);
    } catch (const json::parse_error& e) {
        error(res, 400, "bad_request", std::string("body is not valid JSON: ") + e.what());
        return false;
    }
    if (!out.is_object()) {
        error(res, 400, "bad_request", "body must be a JSON object");
        return false;
    }
    return true;
}
```

Three refusals: too big, not JSON, JSON but not an object, because `[1, 2]` parses fine and then
`contains` on an array is `false` for everything, which would make every field "required". The
function writes the error itself and returns `false`, so the route is one `if`.

The create route, using all three.

```cpp
svr.Post("/users", [](const httplib::Request& req, httplib::Response& res) {
    json body;
    if (!parse_body(req, res, body)) return;
    if (auto errs = validate(body); !errs.empty()) {
        return error(res, 400, "validation_error", "request body is invalid", errs);
    }
    const std::string name = trimmed(body.at("name"));
    std::lock_guard<std::mutex> lock(users_mutex);
    for (const auto& [id, u] : users) {
        if (u.at("name") == name) return error(res, 409, "conflict", "a user named " + name + " already exists");
    }
    int id = static_cast<int>(users.size()) + 1;
    users[id] = {{"id", id}, {"name", name}, {"city", trimmed(body.at("city"))}, {"age", body.at("age")}};
    reply(res, 201, users[id]);
});
```

Parse, validate, check state, store, 201. The `if (auto errs = ...; !errs.empty())` is the
C++17 if-with-initialiser, keeping `errs` scoped to the check. The structured binding over the
map is from [day 5](../day-005-python-lists-and-tuples/README.md).

A lookup the read, replace and delete routes share.

```cpp
std::optional<int> lookup(const httplib::Request& req, httplib::Response& res) {
    int id = std::stoi(req.matches[1]);
    if (!users.contains(id)) {
        error(res, 404, "not_found", "no user with id " + std::to_string(id));
        return std::nullopt;
    }
    return id;
}
```

Call it with the mutex already held. It writes the 404 itself and returns `nullopt`, so each route
is `auto id = lookup(req, res); if (!id) return;`.

```cpp
svr.Delete(R"(/users/(\d+))", [](const httplib::Request& req, httplib::Response& res) {
    std::lock_guard<std::mutex> lock(users_mutex);
    auto id = lookup(req, res);
    if (!id) return;
    users.erase(*id);
    res.status = 204;
});
```

A 204 is `res.status = 204` and no `set_content`. cpp-httplib sends an empty body.

Build, run, and send the parcels:

```bash
g++ -Wall -Wextra -std=c++20 main.cpp -o server
./server
```

```bash
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"  ","age":200}' http://127.0.0.1:8000/users
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"Arjun","city":"Delhi","age":30}' http://127.0.0.1:8000/users
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"Arjun","city":"Delhi","age":30}' http://127.0.0.1:8000/users
curl -i http://127.0.0.1:8000/users/99
curl -i -X DELETE http://127.0.0.1:8000/users/2
```

```text
HTTP/1.1 400 Bad Request
{"error":{"code":"validation_error","fields":[{"field":"name","message":"must not be blank"},{"field":"city","message":"is required"},{"field":"age","message":"must be between 0 and 150"}],"message":"request body is invalid"}}

HTTP/1.1 201 Created
{"age":30,"city":"Delhi","id":2,"name":"Arjun"}

HTTP/1.1 409 Conflict
{"error":{"code":"conflict","message":"a user named Arjun already exists"}}

HTTP/1.1 404 Not Found
{"error":{"code":"not_found","message":"no user with id 99"}}

HTTP/1.1 204 No Content
```

The keys come out alphabetical, so `fields` sits before `message`; the shape is the same and a
caller reading by key does not care.

Here is the whole program in one piece, `main.cpp`:

```cpp
#include <httplib.h>
#include <nlohmann/json.hpp>

#include <iostream>
#include <map>
#include <mutex>
#include <optional>
#include <string>
#include <vector>

using json = nlohmann::json;

std::map<int, json> users = {{1, {{"id", 1}, {"name", "Meera"}, {"city", "Pune"}, {"age", 31}}}};
std::mutex users_mutex;

struct FieldError {
    std::string field;
    std::string message;
};

void reply(httplib::Response& res, int status, const json& body) {
    res.status = status;
    res.set_content(body.dump(), "application/json");
}

void error(httplib::Response& res, int status, const std::string& code, const std::string& message,
           const std::vector<FieldError>& fields = {}) {
    json body = {{"error", {{"code", code}, {"message", message}}}};
    if (!fields.empty()) {
        json list = json::array();
        for (const auto& f : fields) list.push_back({{"field", f.field}, {"message", f.message}});
        body["error"]["fields"] = list;
    }
    reply(res, status, body);
}

std::string trimmed(const json& value) {
    std::string s = value.get<std::string>();
    const auto first = s.find_first_not_of(' ');
    if (first == std::string::npos) return "";
    return s.substr(first, s.find_last_not_of(' ') - first + 1);
}

std::vector<FieldError> validate(const json& body) {
    std::vector<FieldError> errs;
    for (const char* key : {"name", "city"}) {
        if (!body.contains(key)) errs.push_back({key, "is required"});
        else if (!body.at(key).is_string()) errs.push_back({key, "must be a string"});
        else if (trimmed(body.at(key)).empty()) errs.push_back({key, "must not be blank"});
        else if (trimmed(body.at(key)).size() > 50) errs.push_back({key, "must be 50 characters or fewer"});
    }
    if (!body.contains("age")) errs.push_back({"age", "is required"});
    else if (!body.at("age").is_number_integer()) errs.push_back({"age", "must be an integer"});
    else if (body.at("age") < 0 || body.at("age") > 150) errs.push_back({"age", "must be between 0 and 150"});
    return errs;
}

bool parse_body(const httplib::Request& req, httplib::Response& res, json& out) {
    if (req.body.size() > 1 << 20) {
        error(res, 413, "too_large", "body must be under 1 MB");
        return false;
    }
    try {
        out = json::parse(req.body);
    } catch (const json::parse_error& e) {
        error(res, 400, "bad_request", std::string("body is not valid JSON: ") + e.what());
        return false;
    }
    if (!out.is_object()) {
        error(res, 400, "bad_request", "body must be a JSON object");
        return false;
    }
    return true;
}

// Call with users_mutex held.
std::optional<int> lookup(const httplib::Request& req, httplib::Response& res) {
    int id = std::stoi(req.matches[1]);
    if (!users.contains(id)) {
        error(res, 404, "not_found", "no user with id " + std::to_string(id));
        return std::nullopt;
    }
    return id;
}

json user_from(int id, const json& body) {
    return {{"id", id}, {"name", trimmed(body.at("name"))}, {"city", trimmed(body.at("city"))}, {"age", body.at("age")}};
}

int main() {
    httplib::Server svr;

    svr.Get("/users", [](const httplib::Request&, httplib::Response& res) {
        std::lock_guard<std::mutex> lock(users_mutex);
        json all = json::array();
        for (const auto& [id, u] : users) all.push_back(u);
        reply(res, 200, all);
    });

    svr.Get(R"(/users/(\d{1,9}))", [](const httplib::Request& req, httplib::Response& res) {
        std::lock_guard<std::mutex> lock(users_mutex);
        auto id = lookup(req, res);
        if (!id) return;
        reply(res, 200, users[*id]);
    });

    svr.Post("/users", [](const httplib::Request& req, httplib::Response& res) {
        json body;
        if (!parse_body(req, res, body)) return;
        if (auto errs = validate(body); !errs.empty()) {
            return error(res, 400, "validation_error", "request body is invalid", errs);
        }
        const std::string name = trimmed(body.at("name"));
        std::lock_guard<std::mutex> lock(users_mutex);
        for (const auto& [id, u] : users) {
            if (u.at("name") == name) return error(res, 409, "conflict", "a user named " + name + " already exists");
        }
        int id = static_cast<int>(users.size()) + 1;
        users[id] = user_from(id, body);
        reply(res, 201, users[id]);
    });

    svr.Put(R"(/users/(\d{1,9}))", [](const httplib::Request& req, httplib::Response& res) {
        json body;
        if (!parse_body(req, res, body)) return;
        if (auto errs = validate(body); !errs.empty()) {
            return error(res, 400, "validation_error", "request body is invalid", errs);
        }
        std::lock_guard<std::mutex> lock(users_mutex);
        auto id = lookup(req, res);
        if (!id) return;
        users[*id] = user_from(*id, body);
        reply(res, 200, users[*id]);
    });

    svr.Delete(R"(/users/(\d{1,9}))", [](const httplib::Request& req, httplib::Response& res) {
        std::lock_guard<std::mutex> lock(users_mutex);
        auto id = lookup(req, res);
        if (!id) return;
        users.erase(*id);
        res.status = 204;
    });

    std::cout << "listening on 127.0.0.1:8000\n";
    if (!svr.listen("127.0.0.1", 8000)) {
        std::cerr << "could not bind 127.0.0.1:8000\n";
        return 1;
    }
    return 0;
}
```

The `\d{1,9}` in the patterns is day 49's trap closed: nine digits always fit in an `int`, so
`stoi` cannot throw `out_of_range`.

## 6. How the other two languages do it

**Python**

```python
class UserIn(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0, le=150)

@app.exception_handler(RequestValidationError)
async def on_validation_error(request, exc):
    fields = [{"field": ..., "message": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=422, content=error_body("validation_error", ..., fields))
```

The rules are declarations on the model, the failures are collected for you, and the handler
only reshapes the list into your body.

**Go**

```go
type UserIn struct {
	Name string `json:"name"`
	Age  *int   `json:"age"`
}
if in.Age == nil { errs = append(errs, fieldError{"age", "is required"}) }
```

The same appending style as C++, but the "is it there" question has to be asked of a pointer,
because decoding into a struct already threw away the difference between missing and zero.

**The difference that matters:** C++ keeps the body as a JSON tree until you choose to read a
field, so "is it there" is `contains` and "is it a string" is `is_string()`, both free. The cost
is that the tree is mutable, and `body["age"]` on a missing key does not fail, it creates a
`null` at `"age"` and returns it. Go cannot insert a field by looking at it and Python's model
is frozen once built; C++ is the one language where the act of checking can change what you are
checking.

## 7. The traps

**The near-miss: `[]` in `validate`.**

```cpp
std::vector<FieldError> validate(json& body) {           // not const
    std::vector<FieldError> errs;
    if (body["age"].is_null()) errs.push_back({"age", "is required"});
    // ...
```

It compiles, and it reports the missing age correctly. It also inserted `"age": null` into the
body. Anything after `validate` that does `body.contains("age")` now says `true`, and a later
`body.at("age").get<int>()` on that null throws:

```text
terminate called after throwing an instance of 'nlohmann::json_abi_v3_11_3::detail::type_error'
  what():  [json.exception.type_error.302] type must be number, but is null
```

The process is gone. `const json&`, `contains`, `at`.

**`at` on a missing key, outside a check.** `body.at("name")` when there is no name:

```text
terminate called after throwing an instance of 'nlohmann::json_abi_v3_11_3::detail::out_of_range'
  what():  [json.exception.out_of_range.403] key 'name' not found
```

Fine inside `validate` after `contains`; fatal in a route that skipped validation.

**A body that is JSON but not an object.** `-d '[1,2,3]'` without the `is_object()` check makes
every `contains` false, so the slip says all three fields are required, which is true and
useless. With the check, the caller is told the body must be an object.

**Stopping at the first field.** `return error(...)` inside `validate` instead of `push_back`
reports one problem per round trip. The vector exists so the slip is complete.

**Forgetting `json::array()`.**

```cpp
json list;                       // null
for (...) list.push_back(...);   // works: push_back on null makes an array
body["error"]["fields"] = list;  // but with zero fields, this is null, not []
```

The lesson uses `json::array()` so an empty list is `[]`; the `if (!fields.empty())` guard means
it never matters here, and it will the first time someone removes the guard.

**`res.status = 204` with a body.** Add `set_content` after it and cpp-httplib sends the body
anyway, and a strict client like yesterday's `httpx` raises on it. A 204 has no body, ever.

## 8. Say it out loud

**How it gets asked**

- What should a 400 response body look like?
- How do you check whether a field is present without breaking the body?
- Which status codes does your API use, and when?
- What happens to your server when the body is not JSON?

**The ninety-second script**

A fixed shape under one `error` key: a `code` from a short fixed list a program can switch on, a
`message` a person can read, and for validation failures a `fields` list with one entry per
problem, naming the field and what was wrong. The same outer shape for every error in the
service, every problem reported at once, and never the caller's sensitive input echoed back. In
C++ that is one `error` function every route calls, and a `validate` that takes the body by
`const&` and pushes every failure into a vector. Each field gets three questions in order, is it
there with `contains`, is it the right type with `is_string` or `is_number_integer`, is the value
acceptable, and I read with `at`, never `[]`, because `[]` on a mutable body inserts a null where
the key was missing. Before validation, `json::parse` sits in a `try` so a bad body is a 400 and
not a dead process, and I check `is_object` and size. Codes by outcome: 201 create, 204 delete
with no body, 404 missing, 409 conflict, 400 invalid, 413 too large, 500 only when it is my
fault.

**The follow-ups**

- **Why `const json&` and not `json`?** *Copying the tree on every call is wasteful, and more
  importantly a `const` body cannot have a null inserted into it, so `validate` cannot change
  what it is checking. It also forces me to write `contains` and `at`, because `[]` on a const
  body with a missing key is undefined behaviour and I do not want that line in my code at all.*
- **Where does a 500 come from, and what does the caller see?** *An exception I did not catch.
  cpp-httplib's `set_exception_handler` turns it into a response instead of ending the process,
  and I write `{"error": {"code": "internal", "message": "something went wrong"}}` with a request
  id, and log the `what()` against that id.*
- **Would you use a schema library instead?** *For a large API, yes, a JSON Schema validator
  turns `validate` into a document. For a service with five routes, the hand-written version is
  thirty lines I can read, and either way the error body shape is my decision, not the
  library's.*

**A model answer**

"`{"error": {"code": "validation_error", "message": "request body is invalid", "fields": [{"field":
"age", "message": "is required"}]}}`, same outer shape for 404 and 409 without `fields`. One
`error` function, one `validate` returning a vector, `const json&` with `contains` and `at` so
checking never inserts, `parse` in a `try` so bad input is a 400 and not a crash, `is_object` and
a size cap before that. Codes by outcome: 201, 204, 400, 404, 409, 413, 500."

## 9. Recall card

- One `error(res, status, code, message, fields = {})`; every route calls it, none builds error JSON inline.
- `validate(const json&)` returns a `std::vector<FieldError>`; per field: `contains`, then `is_string()`/`is_number_integer()`, then range; never `return` early.
- `[]` on a mutable `json` inserts a null for a missing key. `contains` looks, `at` throws, `const&` protects.
- `json::parse` in a `try`, then `is_object()`, then a size cap; a throw in a handler ends the process.
- 201 create, 204 delete (`res.status` only, no `set_content`), 404 missing, 409 conflict, 400 invalid, 413 too large.
