---
day: 50
track: lang-go
title: "Decoding request bodies, validation, and writing error responses"
theme: "Designing a JSON API"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 050 · Go — Decoding request bodies, validation, and writing error responses

**Today's theme:** Designing a JSON API

**After today you can:** You can build a CRUD endpoint set with proper status codes and error bodies, in each language.

**The interviewer asks it as:** *What should a 400 response body look like?*

---

## 1. What this is, and why it matters

In Go the standard library decodes JSON into a struct and stops there. Whether a field was
present, whether a string is blank, whether an age is 200: none of that is checked, because
`encoding/json` has no idea what your rules are. Today you write the three pieces that a JSON API
needs on top of it: a decoder set up to refuse what it should refuse, a `validate` function that
returns every problem at once, and one `writeError` that produces the same error body for every
failure in the service.

At work, these three functions are in every Go service you will read, usually in a file called
`errors.go` or `respond.go`, and the quality of a codebase is visible in whether they exist or
whether every handler builds its own JSON by hand. In interviews, "what should a 400 response
body look like" is answered the same way in every language; the Go follow-up is "and how do you
tell a missing field from an empty one", which has a real answer you will meet in section 7.

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

One more habit is Farida's own. The form has a box for "declared value". Some people leave it
empty, and some write a zero. Those are not the same parcel. An empty box means they forgot, and
she asks; a zero means they are sending a gift with no value, and she does not. For a long time
the form could not tell the two apart, and she had to ask everyone. Now the box has a small
"none" tick next to it, and the difference is on the form itself.

## 3. The idea in plain English

The printed slip is the **error body**, one shape for every failure:
`{"error": {"code": ..., "message": ..., "fields": [...]}}`. In Go that is two structs, `apiError`
and `fieldError`, with `json` tags from [day 40](../day-040-2d-prefix-sums/README.md), and one
function, `writeError`, that fills them and encodes them. Every handler calls it; no handler
builds error JSON by hand.

The five fixed words are **status codes** chosen by kind of outcome: `200` for a read or a
replace, `201` for a create, `204` for a delete with no body, `400` for a body that fails the
rules, `404` when the path names something that is not there, `409` when the body is fine but the
state says no, `500` for our fault. Go has no framework opinion about 400 versus 422; this lesson
uses 400.

Checking the whole form is a **validate** function that returns a slice of field errors. Every
rule is an `if` that appends. The handler calls it once and, if the slice is not empty, writes a
400 with the whole slice as `fields`. Returning at the first failure is the thing the manager
told Farida to stop doing.

The decoder's refusals are two settings. `decoder.DisallowUnknownFields()` makes a body with a
field the struct does not have a decode error, so a caller who misspells `city` as `town` hears
about it. `http.MaxBytesReader(w, r.Body, 1<<20)` caps the body at a megabyte, so a caller cannot
send a gigabyte and have you read it into memory.

The empty box and the zero are the **zero value** problem. A missing `"age"` decodes to `0`, and
so does `"age": 0`. To tell them apart you declare the field as a pointer, `*int`: `nil` means the
box was empty, and a non-nil pointer to `0` means they wrote zero. That is the small "none" tick,
and it is the answer to the interview follow-up.

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

Notice that the error rows differ only in `code`, and only the validation row has `fields`.
`writeError` takes the status, the code, the message and an optional slice, and that table is
its whole job.

## 5. The code, built step by step

The two shapes and the store.

```go
type UserIn struct {
	Name string `json:"name"`
	City string `json:"city"`
	Age  *int   `json:"age"`
}

type User struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
	City string `json:"city"`
	Age  int    `json:"age"`
}

var users = map[int]User{1: {ID: 1, Name: "Meera", City: "Pune", Age: 31}}
```

`UserIn` is the form; `User` is the receipt. `Age` is `*int` on the way in so that a missing age is
`nil` and not `0`, and a plain `int` on the way out because a stored user always has one.

The error shape, and the one function that writes it.

```go
type fieldError struct {
	Field   string `json:"field"`
	Message string `json:"message"`
}

type apiError struct {
	Code    string       `json:"code"`
	Message string       `json:"message"`
	Fields  []fieldError `json:"fields,omitempty"`
}

func writeError(w http.ResponseWriter, status int, code, message string, fields []fieldError) {
	writeJSON(w, status, map[string]apiError{"error": {Code: code, Message: message, Fields: fields}})
}
```

`omitempty` from day 40 drops `fields` when the slice is nil, so a 404 body has no empty list in
it. `writeJSON` is yesterday's helper: header, status, encode.

The rules, all of them, in one function.

```go
func validate(in UserIn) []fieldError {
	var errs []fieldError
	if name := strings.TrimSpace(in.Name); name == "" {
		errs = append(errs, fieldError{"name", "must not be blank"})
	} else if len(name) > 50 {
		errs = append(errs, fieldError{"name", "must be 50 characters or fewer"})
	}
	if strings.TrimSpace(in.City) == "" {
		errs = append(errs, fieldError{"city", "must not be blank"})
	}
	if in.Age == nil {
		errs = append(errs, fieldError{"age", "is required"})
	} else if *in.Age < 0 || *in.Age > 150 {
		errs = append(errs, fieldError{"age", "must be between 0 and 150"})
	}
	return errs
}
```

No early return. A body with a blank name and an age of 200 gets two entries. The `nil` check on
`Age` is the "required" rule, and it is only possible because the field is a pointer.

Decoding, with the refusals switched on.

```go
func decode(w http.ResponseWriter, r *http.Request, into any) error {
	r.Body = http.MaxBytesReader(w, r.Body, 1<<20)
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	return decoder.Decode(into)
}
```

Three lines that every handler with a body will call. `1<<20` is one megabyte. The decoder
returns an error for a body that is not JSON, a wrong type, an unknown field, or one that is too
big, and the handler turns any of those into a 400.

The create handler, using all three.

```go
func createUser(w http.ResponseWriter, r *http.Request) {
	var in UserIn
	if err := decode(w, r, &in); err != nil {
		writeError(w, http.StatusBadRequest, "bad_request", "body is not valid JSON: "+err.Error(), nil)
		return
	}
	if errs := validate(in); len(errs) > 0 {
		writeError(w, http.StatusBadRequest, "validation_error", "request body is invalid", errs)
		return
	}
	for _, u := range users {
		if u.Name == strings.TrimSpace(in.Name) {
			writeError(w, http.StatusConflict, "conflict", "a user named "+u.Name+" already exists", nil)
			return
		}
	}
	user := User{ID: len(users) + 1, Name: strings.TrimSpace(in.Name), City: strings.TrimSpace(in.City), Age: *in.Age}
	users[user.ID] = user
	writeJSON(w, http.StatusCreated, user)
}
```

Decode, validate, check state, store, 201. Four outcomes, four exits, and every error goes
through `writeError`. `*in.Age` is safe here because `validate` returned no errors, so `Age` is
not `nil`.

Get, replace and delete, sharing a lookup.

```go
func lookup(w http.ResponseWriter, r *http.Request) (User, bool) {
	id, err := strconv.Atoi(r.PathValue("id"))
	if err != nil {
		writeError(w, http.StatusBadRequest, "bad_request", "id must be a number", nil)
		return User{}, false
	}
	user, ok := users[id]
	if !ok {
		writeError(w, http.StatusNotFound, "not_found", "no user with id "+r.PathValue("id"), nil)
		return User{}, false
	}
	return user, true
}
```

`lookup` writes the error itself and returns `false`, so each handler is one `if !ok { return }`.

```go
func deleteUser(w http.ResponseWriter, r *http.Request) {
	user, ok := lookup(w, r)
	if !ok {
		return
	}
	delete(users, user.ID)
	w.WriteHeader(http.StatusNoContent)
}
```

A 204 is `WriteHeader` and nothing else; no `writeJSON`, no body.

Run it and send the parcels:

```bash
go run main.go
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
{"error":{"code":"validation_error","message":"request body is invalid","fields":[{"field":"name","message":"must not be blank"},{"field":"city","message":"must not be blank"},{"field":"age","message":"must be between 0 and 150"}]}}

HTTP/1.1 201 Created
{"id":2,"name":"Arjun","city":"Delhi","age":30}

HTTP/1.1 409 Conflict
{"error":{"code":"conflict","message":"a user named Arjun already exists"}}

HTTP/1.1 404 Not Found
{"error":{"code":"not_found","message":"no user with id 99"}}

HTTP/1.1 204 No Content
```

Three problems on one slip, then each outcome with its own status and the same outer shape.

Here is the whole program in one piece, `main.go`:

```go
package main

import (
	"encoding/json"
	"log"
	"net/http"
	"sort"
	"strconv"
	"strings"
)

type UserIn struct {
	Name string `json:"name"`
	City string `json:"city"`
	Age  *int   `json:"age"`
}

type User struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
	City string `json:"city"`
	Age  int    `json:"age"`
}

type fieldError struct {
	Field   string `json:"field"`
	Message string `json:"message"`
}

type apiError struct {
	Code    string       `json:"code"`
	Message string       `json:"message"`
	Fields  []fieldError `json:"fields,omitempty"`
}

var users = map[int]User{1: {ID: 1, Name: "Meera", City: "Pune", Age: 31}}

func writeJSON(w http.ResponseWriter, status int, value any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(value); err != nil {
		log.Println("encode:", err)
	}
}

func writeError(w http.ResponseWriter, status int, code, message string, fields []fieldError) {
	writeJSON(w, status, map[string]apiError{"error": {Code: code, Message: message, Fields: fields}})
}

func decode(w http.ResponseWriter, r *http.Request, into any) error {
	r.Body = http.MaxBytesReader(w, r.Body, 1<<20)
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	return decoder.Decode(into)
}

func validate(in UserIn) []fieldError {
	var errs []fieldError
	if name := strings.TrimSpace(in.Name); name == "" {
		errs = append(errs, fieldError{"name", "must not be blank"})
	} else if len(name) > 50 {
		errs = append(errs, fieldError{"name", "must be 50 characters or fewer"})
	}
	if strings.TrimSpace(in.City) == "" {
		errs = append(errs, fieldError{"city", "must not be blank"})
	}
	if in.Age == nil {
		errs = append(errs, fieldError{"age", "is required"})
	} else if *in.Age < 0 || *in.Age > 150 {
		errs = append(errs, fieldError{"age", "must be between 0 and 150"})
	}
	return errs
}

func lookup(w http.ResponseWriter, r *http.Request) (User, bool) {
	id, err := strconv.Atoi(r.PathValue("id"))
	if err != nil {
		writeError(w, http.StatusBadRequest, "bad_request", "id must be a number", nil)
		return User{}, false
	}
	user, ok := users[id]
	if !ok {
		writeError(w, http.StatusNotFound, "not_found", "no user with id "+r.PathValue("id"), nil)
		return User{}, false
	}
	return user, true
}

func listUsers(w http.ResponseWriter, r *http.Request) {
	all := make([]User, 0, len(users))
	for _, u := range users {
		all = append(all, u)
	}
	sort.Slice(all, func(i, j int) bool { return all[i].ID < all[j].ID })
	writeJSON(w, http.StatusOK, all)
}

func getUser(w http.ResponseWriter, r *http.Request) {
	user, ok := lookup(w, r)
	if !ok {
		return
	}
	writeJSON(w, http.StatusOK, user)
}

func createUser(w http.ResponseWriter, r *http.Request) {
	var in UserIn
	if err := decode(w, r, &in); err != nil {
		writeError(w, http.StatusBadRequest, "bad_request", "body is not valid JSON: "+err.Error(), nil)
		return
	}
	if errs := validate(in); len(errs) > 0 {
		writeError(w, http.StatusBadRequest, "validation_error", "request body is invalid", errs)
		return
	}
	for _, u := range users {
		if u.Name == strings.TrimSpace(in.Name) {
			writeError(w, http.StatusConflict, "conflict", "a user named "+u.Name+" already exists", nil)
			return
		}
	}
	user := User{ID: len(users) + 1, Name: strings.TrimSpace(in.Name), City: strings.TrimSpace(in.City), Age: *in.Age}
	users[user.ID] = user
	writeJSON(w, http.StatusCreated, user)
}

func replaceUser(w http.ResponseWriter, r *http.Request) {
	user, ok := lookup(w, r)
	if !ok {
		return
	}
	var in UserIn
	if err := decode(w, r, &in); err != nil {
		writeError(w, http.StatusBadRequest, "bad_request", "body is not valid JSON: "+err.Error(), nil)
		return
	}
	if errs := validate(in); len(errs) > 0 {
		writeError(w, http.StatusBadRequest, "validation_error", "request body is invalid", errs)
		return
	}
	user = User{ID: user.ID, Name: strings.TrimSpace(in.Name), City: strings.TrimSpace(in.City), Age: *in.Age}
	users[user.ID] = user
	writeJSON(w, http.StatusOK, user)
}

func deleteUser(w http.ResponseWriter, r *http.Request) {
	user, ok := lookup(w, r)
	if !ok {
		return
	}
	delete(users, user.ID)
	w.WriteHeader(http.StatusNoContent)
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /users", listUsers)
	mux.HandleFunc("GET /users/{id}", getUser)
	mux.HandleFunc("POST /users", createUser)
	mux.HandleFunc("PUT /users/{id}", replaceUser)
	mux.HandleFunc("DELETE /users/{id}", deleteUser)
	log.Println("listening on 127.0.0.1:8000")
	log.Fatal(http.ListenAndServe("127.0.0.1:8000", mux))
}
```

The map is still unguarded; the mutex from the day 48 practice belongs here too.

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

The rules are on the model and the list of failures is built for you; the handler only reshapes
it. A missing field and a present one are different because pydantic knows which keys it saw.

**C++**

```cpp
if (!body.contains("age")) errs.push_back({"age", "is required"});
else if (!body["age"].is_number_integer()) errs.push_back({"age", "must be an integer"});
else if (body["age"] < 0 || body["age"] > 150) errs.push_back({"age", "must be between 0 and 150"});
```

The same appending style as Go, with `contains` answering the missing-versus-zero question
directly, because the JSON object is still a JSON object when you check it.

**The difference that matters:** Go is the only one of the three where decoding erases the
difference between a field that was absent and a field that was zero. Python's model and C++'s
`json` object both still know. In Go you get that knowledge back only by declaring the field as a
pointer, and every "required integer" in a Go API is a `*int` for exactly this reason.

## 7. The traps

**The near-miss: `Age int` instead of `*int`.**

```go
type UserIn struct {
	Name string `json:"name"`
	City string `json:"city"`
	Age  int    `json:"age"`
}
```

POST `{"name":"Arjun","city":"Delhi"}` with no age. `validate` sees `Age == 0`, which is between
0 and 150, and the user is created aged zero:

```text
HTTP/1.1 201 Created
{"id":2,"name":"Arjun","city":"Delhi","age":0}
```

No error anywhere. The pointer is the only way to ask "was it there".

**An unknown field, with and without the setting.** POST `{"name":"Zed","city":"Goa","age":20,"town":"x"}`.
Without `DisallowUnknownFields`, a 201 and `town` is silently dropped. With it:

```text
HTTP/1.1 400 Bad Request
{"error":{"code":"bad_request","message":"body is not valid JSON: json: unknown field \"town\""}}
```

**Wrong type.** `"age": "thirty"`:

```text
json: cannot unmarshal string into Go struct field UserIn.age of type int
```

**Body too big.** Send two megabytes:

```text
http: request body too large
```

`MaxBytesReader` also closes the connection, so the caller cannot keep sending.

**Returning at the first validation failure.**

```go
if strings.TrimSpace(in.Name) == "" {
	writeError(w, 400, "validation_error", "name must not be blank", nil)
	return
}
if in.Age == nil { ... }
```

A body with both problems reports one, the caller fixes it, sends again, and gets the other.
Collect a slice.

**A body on the 204.** `writeJSON(w, http.StatusNoContent, map[string]bool{"deleted": true})`:

```text
http: request method or response status code does not allow body
```

That line appears in the server log, and the body is dropped. `WriteHeader(204)` alone.

## 8. Say it out loud

**How it gets asked**

- What should a 400 response body look like?
- How do you tell a missing field from a zero in Go?
- Which status codes does your API use, and when?
- Where do the validation rules live?

**The ninety-second script**

A fixed shape under one `error` key: a `code` from a short fixed list that a program can switch
on, a `message` a person can read, and for validation failures a `fields` list, one entry per
problem, naming the field and what was wrong with it. The same outer shape for every error in the
service, so a caller writes one reader, and every problem reported at once so they fix the form
in one round trip. In Go that is an `apiError` struct with `omitempty` on `fields`, and a single
`writeError` that every handler calls. Rules live in a `validate` function that appends to a
slice and never returns early. Before it, the decoder has `DisallowUnknownFields` and a
`MaxBytesReader` so a misspelled key is a 400 and a huge body is refused. Required numbers are
pointer fields, because after decoding a missing `age` and `"age": 0` are both `0` unless the
field is a `*int`, where missing is `nil`. Status codes by outcome: 201 create, 204 delete, 404
missing, 409 conflict, 400 invalid, 500 only when it is my fault.

**The follow-ups**

- **Why not a validation library?** *There are good ones that read struct tags, and in a large
  service I would use one. The hand-written version is fifteen lines, has no magic, and I can
  explain every rule in it; the library is the same slice of field errors with the rules moved
  into tags.*
- **What about a 500? What does the caller see?** *`{"error": {"code": "internal", "message":
  "something went wrong", "request_id": ...}}` and nothing else. The panic or the SQL error is in
  my log against that id. A recover middleware from [day 49](../day-049-peak-finding/README.md)
  writes it.*
- **PUT versus PATCH?** *PUT replaces the whole record and takes a full body, so the same
  `validate` applies. PATCH changes some fields, so every field is optional and the pointer trick
  is how you tell "leave it alone" from "set it to empty".*

**A model answer**

"`{"error": {"code": "validation_error", "message": "request body is invalid", "fields": [{"field":
"age", "message": "is required"}]}}`, the same outer shape for 404 and 409 without `fields`. In Go,
one `writeError`, one `validate` that returns a slice, a decoder with `DisallowUnknownFields` and
`MaxBytesReader`, and `*int` for required numbers so I can tell missing from zero. Codes by
outcome: 201, 204, 400, 404, 409, 500."

## 9. Recall card

- One `writeError(w, status, code, message, fields)`; `apiError` has a `Fields []fieldError` tagged `fields,omitempty` so a 404 body carries no empty list.
- `validate` appends every problem to a slice and never returns early; the handler writes 400 with the slice.
- `decoder.DisallowUnknownFields()` and `http.MaxBytesReader(w, r.Body, 1<<20)` before `Decode`.
- Missing and zero decode the same; a required number is `*int`, and `nil` means missing.
- 201 create, 204 delete (`WriteHeader` only), 404 path missing, 409 conflict, 400 invalid body, 500 my fault.
