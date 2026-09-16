---
day: 50
track: lang-python
title: "Pydantic models, validation errors, and status codes"
theme: "Designing a JSON API"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 050 · Python — Pydantic models, validation errors, and status codes

**Today's theme:** Designing a JSON API

**After today you can:** You can build a CRUD endpoint set with proper status codes and error bodies, in each language.

**The interviewer asks it as:** *What should a 400 response body look like?*

---

## 1. What this is, and why it matters

A JSON API is a set of routes that agree with each other: the same shape for every error, the
same status code for the same kind of outcome, and rules on the input that are checked once, at
the door. In FastAPI the rules live on the pydantic model as `Field` constraints and validators,
the status codes are declared on the route, and one exception handler turns every validation
failure into the one error shape you chose.

At work, the error body is the part of your API that other teams read most, because it is what
they see when their code is wrong. In interviews, "what should a 400 response body look like" is
asked to find out whether you have ever been on the calling side of a bad one. The answer is
short and specific, and this lesson builds it.

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
"not allowed", not a receipt with a note on the back. And on the day the weighing scale broke,
every parcel got an "our fault" slip that said "come back after two", so nobody thought they had
filled the form wrong.

The other thing the manager insisted on: Farida checks the whole form before saying anything. If
the address is missing and the phone number has letters in it, the slip says both. A customer
who fixes one and comes back to be told about the other is a customer who does not come back a
third time.

The back office has never once seen a form with a line missing. They only see forms Farida
passed, which is why they are fast.

## 3. The idea in plain English

The printed slip is the **error body**: one JSON shape for every failure, so a caller writes one
piece of code to read it. Today's shape is `{"error": {"code": ..., "message": ..., "fields": [...]}}`.
The `code` is one of a few fixed words a program can switch on; the `message` is a sentence a
person can read; `fields` is the list of what was wrong with which part of the input, present only
when the problem was the input.

The five fixed words map onto **status codes**, the three-digit number on the status line, chosen
by kind of outcome and not by feeling. Today's set: `200` for a successful read or replace, `201`
when a POST created something, `204` for a successful delete with no body, `404` when the thing
named in the path does not exist, `409` when the request is fine but conflicts with what is
already there, `422` when the body failed validation, and `500` for "our fault". FastAPI uses
`422` for validation rather than `400`; the interview answer is the body shape, and the number is
the convention of the framework you are in.

The form's rules are **constraints** on the model: `Field(min_length=1, max_length=50)` on a
string, `Field(ge=0, le=150)` on an int. A **validator**, `@field_validator("name")`, is a rule
you write yourself, such as "strip whitespace and refuse a blank". They run before your route,
and they run all of them, so the slip lists every problem at once.

Checking the whole form before speaking is what pydantic does by default: it collects every
failure in the body and reports them together as a list, each with a `loc`, the path to the field,
and a `msg`.

The one place that prints slips is an **exception handler**: `@app.exception_handler(RequestValidationError)`
catches every validation failure in the whole app and turns pydantic's list into your shape. A
second handler for `HTTPException` does the same for the 404s and 409s your routes raise, so the
shape is the same whether the failure was the input or the state.

The five routes, `GET /users`, `GET /users/{id}`, `POST /users`, `PUT /users/{id}`,
`DELETE /users/{id}`, are **CRUD**: create, read, update, delete. Every resource in every API
you will meet has some subset of these.

## 4. The picture

```text
outcome                         status   body
---------------------------------------------------------------------------
read one, found                  200     {"id": 1, "name": ..., ...}
created                          201     the created thing, with its id
replaced                         200     the replaced thing
deleted                          204     (nothing)
path names something missing     404     {"error": {"code": "not_found", "message": ...}}
input fails a rule               422     {"error": {"code": "validation_error",
                                                    "message": ..., "fields": [...]}}
input fine, state says no        409     {"error": {"code": "conflict", "message": ...}}
our fault                        500     {"error": {"code": "internal", "message": ...}}
```

Notice that every error row has the same outer shape and only the success rows differ. A caller
checks `status >= 400`, reads `error.code`, and is done.

## 5. The code, built step by step

Start from a fresh `main.py` with the usual `pip install fastapi uvicorn`.

The model with its rules.

```python
class UserIn(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    city: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0, le=150)

    @field_validator("name", "city")
    @classmethod
    def strip_and_check(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value
```

`Field` carries the constraints; `ge` and `le` are "greater or equal" and "less or equal". The
validator runs on both named fields, strips them, and refuses a string of spaces, which
`min_length=1` alone would let through. A validator that raises `ValueError` becomes one entry in
the failure list; one that returns a value replaces the field with it.

The output model, and the store.

```python
class UserOut(UserIn):
    id: int


users: dict[int, UserOut] = {1: UserOut(id=1, name="Meera", city="Pune", age=31)}
```

`UserOut` inherits the three fields and adds `id`. The caller cannot set `id` on a `UserIn`
because it is not there.

The error shape, in one function.

```python
def error_body(code: str, message: str, fields: list[dict[str, str]] | None = None) -> dict:
    body: dict = {"error": {"code": code, "message": message}}
    if fields:
        body["error"]["fields"] = fields
    return body
```

Every error in the app goes through this. Change the shape here and it changes everywhere.

The two handlers, the slip printer.

```python
@app.exception_handler(RequestValidationError)
async def on_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    fields = [{"field": ".".join(str(p) for p in e["loc"][1:]), "message": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=422, content=error_body("validation_error", "request body is invalid", fields))


@app.exception_handler(HTTPException)
async def on_http_error(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=error_body(exc.detail["code"], exc.detail["message"]))
```

`exc.errors()` is pydantic's list. Each entry's `loc` is a tuple like `("body", "city")`; the
`[1:]` drops `"body"`, and the join handles nested fields like `address.pin`. The second handler
expects routes to raise `HTTPException` with a dict as `detail`, carrying `code` and `message`,
so the 404s and 409s come out in the same shape.

A helper the routes share, and the five routes.

```python
def find(user_id: int) -> UserOut:
    if user_id not in users:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": f"no user with id {user_id}"})
    return users[user_id]


@app.get("/users", response_model=list[UserOut])
def list_users() -> list[UserOut]:
    return sorted(users.values(), key=lambda u: u.id)


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int) -> UserOut:
    return find(user_id)
```

```python
@app.post("/users", response_model=UserOut, status_code=201)
def create_user(body: UserIn) -> UserOut:
    if any(u.name == body.name for u in users.values()):
        raise HTTPException(status_code=409, detail={"code": "conflict", "message": f"a user named {body.name} already exists"})
    new_id = max(users, default=0) + 1
    users[new_id] = UserOut(id=new_id, **body.model_dump())
    return users[new_id]


@app.put("/users/{user_id}", response_model=UserOut)
def replace_user(user_id: int, body: UserIn) -> UserOut:
    find(user_id)
    users[user_id] = UserOut(id=user_id, **body.model_dump())
    return users[user_id]


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int) -> Response:
    find(user_id)
    del users[user_id]
    return Response(status_code=204)
```

The 409 is a rule that needs the store, so it lives in the route and not the model. `PUT`
replaces the whole record, so it takes a full `UserIn` and answers 200 with the result. `DELETE`
answers 204 and an empty `Response`, because a body on a 204 is a protocol error. Deleting twice
is a 404 the second time; the practice sheet argues about that.

Run it and send the parcels:

```bash
python -m uvicorn main:app --port 8000
```

```bash
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"  ","age":200}' http://127.0.0.1:8000/users
```

```text
HTTP/1.1 422 Unprocessable Entity
{"error":{"code":"validation_error","message":"request body is invalid","fields":[{"field":"name","message":"Value error, must not be blank"},{"field":"city","message":"Field required"},{"field":"age","message":"Input should be less than or equal to 150"}]}}
```

Three problems, one slip. Then the happy path, the conflict, and the rest:

```bash
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"Arjun","city":"Delhi","age":30}' http://127.0.0.1:8000/users
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"Arjun","city":"Delhi","age":30}' http://127.0.0.1:8000/users
curl -i http://127.0.0.1:8000/users/99
curl -i -X DELETE http://127.0.0.1:8000/users/2
curl -i -X DELETE http://127.0.0.1:8000/users/2
```

```text
HTTP/1.1 201 Created
{"name":"Arjun","city":"Delhi","age":30,"id":2}

HTTP/1.1 409 Conflict
{"error":{"code":"conflict","message":"a user named Arjun already exists"}}

HTTP/1.1 404 Not Found
{"error":{"code":"not_found","message":"no user with id 99"}}

HTTP/1.1 204 No Content

HTTP/1.1 404 Not Found
{"error":{"code":"not_found","message":"no user with id 2"}}
```

Here is the whole program in one piece, `main.py`:

```python
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

app = FastAPI()


class UserIn(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    city: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0, le=150)

    @field_validator("name", "city")
    @classmethod
    def strip_and_check(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class UserOut(UserIn):
    id: int


users: dict[int, UserOut] = {1: UserOut(id=1, name="Meera", city="Pune", age=31)}


def error_body(code: str, message: str, fields: list[dict[str, str]] | None = None) -> dict:
    body: dict = {"error": {"code": code, "message": message}}
    if fields:
        body["error"]["fields"] = fields
    return body


@app.exception_handler(RequestValidationError)
async def on_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    fields = [{"field": ".".join(str(p) for p in e["loc"][1:]), "message": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=422, content=error_body("validation_error", "request body is invalid", fields))


@app.exception_handler(HTTPException)
async def on_http_error(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=error_body(exc.detail["code"], exc.detail["message"]))


def find(user_id: int) -> UserOut:
    if user_id not in users:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": f"no user with id {user_id}"})
    return users[user_id]


@app.get("/users", response_model=list[UserOut])
def list_users() -> list[UserOut]:
    return sorted(users.values(), key=lambda u: u.id)


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int) -> UserOut:
    return find(user_id)


@app.post("/users", response_model=UserOut, status_code=201)
def create_user(body: UserIn) -> UserOut:
    if any(u.name == body.name for u in users.values()):
        raise HTTPException(status_code=409, detail={"code": "conflict", "message": f"a user named {body.name} already exists"})
    new_id = max(users, default=0) + 1
    users[new_id] = UserOut(id=new_id, **body.model_dump())
    return users[new_id]


@app.put("/users/{user_id}", response_model=UserOut)
def replace_user(user_id: int, body: UserIn) -> UserOut:
    find(user_id)
    users[user_id] = UserOut(id=user_id, **body.model_dump())
    return users[user_id]


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int) -> Response:
    find(user_id)
    del users[user_id]
    return Response(status_code=204)
```

## 6. How the other two languages do it

**Go**

```go
func validate(u UserIn) []FieldError {
	var errs []FieldError
	if strings.TrimSpace(u.Name) == "" { errs = append(errs, FieldError{"name", "must not be blank"}) }
	if u.Age < 0 || u.Age > 150 { errs = append(errs, FieldError{"age", "must be between 0 and 150"}) }
	return errs
}
if errs := validate(body); len(errs) > 0 {
	writeError(w, 400, "validation_error", "request body is invalid", errs)
	return
}
```

Every rule is an `if` that appends to a slice, and the slice becomes `fields`. Nothing runs
before the handler; the handler calls `validate` itself.

**C++**

```cpp
std::vector<FieldError> validate(const json& body) {
    std::vector<FieldError> errs;
    if (!body.contains("name") || !body["name"].is_string()) errs.push_back({"name", "must be a string"});
    else if (trim(body["name"]).empty()) errs.push_back({"name", "must not be blank"});
    // ...
    return errs;
}
```

The same shape as Go, with one extra question per field: is it there, and is it the right type,
because a JSON object does not have a schema until you check it.

**The difference that matters:** FastAPI checks types and constraints and collects every failure
before the route, from the model alone; Go and C++ check nothing until the handler asks, and the
"report all problems at once" behaviour is a slice you remember to keep appending to instead of
returning at the first `if`. The error body shape is a decision in all three; only Python gives
you the list for free.

## 7. The traps

**The near-miss: extra fields are ignored.** Send `"id": 1` on a POST:

```bash
curl -i -X POST -H "Content-Type: application/json" -d '{"name":"Zed","city":"Goa","age":20,"id":1}' http://127.0.0.1:8000/users
```

```text
HTTP/1.1 201 Created
{"name":"Zed","city":"Goa","age":20,"id":2}
```

No error, and the `id` was silently dropped. That is safe here, because the model does not have
the field, but a caller who misspells `city` as `town` gets a 422 for the missing `city` and no
mention that `town` was ignored. `model_config = ConfigDict(extra="forbid")` on the model turns
an unknown field into a 422 that names it.

**The default validation body.** Without the handler, the same bad parcel gets:

```text
{"detail":[{"type":"missing","loc":["body","city"],"msg":"Field required","input":{"name":"  ","age":200}}]}
```

It is useful and it is a different shape from every other error in your API, and it echoes the
caller's input back, which for a password field is a leak. The handler exists to make it match.

**A dict `detail` on the wrong handler.** Raise `HTTPException(status_code=404, detail="no user")`
with a string, and the handler above does `exc.detail["code"]`:

```text
TypeError: string indices must be integers, not 'str'
```

The caller gets a 500 for what should have been a 404. Every `HTTPException` in this app carries
a dict, or the handler checks `isinstance(exc.detail, dict)`.

**A body on a 204.** Return `{"deleted": True}` from the delete route with `status_code=204`:

```text
RuntimeError: Response content longer than Content-Length
```

A 204 promises no body. Return `Response(status_code=204)` and nothing else.

**Validation that stops at the first problem.** A validator that raises on the first bad field
it sees, for the whole model, sends the customer back three times. Field validators run per
field, and pydantic collects them; keep the checks per field so the slip is complete.

## 8. Say it out loud

**How it gets asked**

- What should a 400 response body look like?
- Which status codes does your API use, and when?
- Where does validation happen, and does the caller see every problem or just the first?
- How do you keep every error in the API the same shape?

**The ninety-second script**

An error body has a fixed outer shape, one object under an `error` key, with a machine-readable
`code` from a short fixed list, a human-readable `message`, and, for validation failures, a
`fields` list where each entry names the field and says what was wrong with it. Every error in
the API uses that shape, whether it is a 404, a 409 or a validation failure, so the caller writes
one reader. Validation reports every problem at once, not the first one, so the caller fixes the
form in one round trip. It never echoes back sensitive input. Status codes are by kind of outcome:
200 for a read or replace, 201 for a create, 204 for a delete, 404 when the path names something
that does not exist, 409 when the input is valid but conflicts with current state, 422 in FastAPI
for a body that fails validation, and 500 only when it is my fault. In FastAPI the rules are
`Field` constraints and validators on the model, and two exception handlers produce the shape,
so no route builds an error body by hand.

**The follow-ups**

- **400 or 422 for validation?** *Either, consistently. FastAPI's default is 422, "understood the
  request, cannot process it"; many APIs use 400. What matters is that it is one number and the
  body shape is the same.*
- **Should a repeated DELETE be 404 or 204?** *404 is honest about state: the thing is not there
  now. 204 is idempotent-friendly: the caller wanted it gone and it is gone. I pick one, document
  it, and lean towards 204 when callers retry, so a retry after a lost response does not look
  like a failure.*
- **What do you never put in an error body?** *Stack traces, SQL, internal hostnames, and the
  caller's own sensitive input. A 500 says "internal error" and a request id; the detail is in my
  logs against that id.*

**A model answer**

"`{"error": {"code": "validation_error", "message": "request body is invalid", "fields": [{"field": "city",
"message": "Field required"}]}}`. Fixed shape, a code a program can switch on, a message a person
can read, and every field problem in one list so the caller fixes them in one go. Same shape for
404s and 409s, minus `fields`. In FastAPI that is `Field` constraints on the model, a
`RequestValidationError` handler that maps pydantic's list to my shape, and an `HTTPException`
handler for the rest. Status codes by outcome: 201 create, 204 delete, 404 missing, 409 conflict,
422 invalid, 500 my fault."

## 9. Recall card

- One error shape: `{"error": {"code", "message", "fields"?}}`; fixed codes, readable message, every field problem at once, never echo secrets.
- Codes by outcome: 200 read/replace, 201 create, 204 delete (no body), 404 path missing, 409 conflict, 422 invalid body, 500 my fault.
- Rules on the model: `Field(min_length=, ge=, le=)` and `@field_validator`; they run before the route and collect all failures.
- `@app.exception_handler(RequestValidationError)` and `(HTTPException)` produce the shape in one place; routes raise `HTTPException(detail={"code", "message"})`.
- `ConfigDict(extra="forbid")` to reject unknown fields; `Response(status_code=204)` for a delete; a repeated delete is a decision you document.
