---
day: 60
track: lang-python
title: "FastAPI plus Postgres plus Redis"
theme: "Mini project 4: a URL shortener API"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 060 · Python — FastAPI plus Postgres plus Redis

**Today's theme:** Mini project 4: a URL shortener API

**After today you can:** You can build, test, containerise, and demo the same REST service in all three languages.

**The interviewer asks it as:** *Design and build a URL shortener. Now explain every choice.*

---

## 1. What this is, and why it matters

A URL shortener takes a long address, hands back a short code, and later turns the code back
into the address with a redirect. It is two routes, one table, and one cache, which is why it is
the standard first system design question and the standard "build something real" take-home.
Today you assemble it from the last twelve days: FastAPI routes and pydantic validation from
[days 48](../day-048-binary-search-on-floats/README.md) and [50](../day-050-binary-search-revision/README.md),
a psycopg connection pool from [day 54](../day-054-quicksort/README.md), cache-aside on Redis
from [day 56](../day-056-non-comparison-sorts/README.md), tests from
[day 58](../day-058-custom-comparators/README.md), and the image from
[day 59](../day-059-sorting-revision/README.md).

At work this is the shape of most small services: an API in front of a database with a cache
beside it. In interviews, the build question is "make it work", and the design question that
follows is "now explain every choice", and today you make choices you can explain.

## 2. The story

The wedding hall has a cloakroom, and Nandini is running it. Guests arrive in December coats,
heavy wool things with long scarves and gloves stuffed in the pockets, and nobody wants to sit
through a three-hour ceremony wrapped in one. So they hand the coat across the counter, and
Nandini hands back a small brass token with a number stamped on it. The token fits in a palm.
The coat does not.

Behind the counter is a long rail with numbered hooks, and a ledger where she writes the number
and a description: "214, grey wool, red scarf". The ledger is the thing that matters. If the
tokens got mixed up, the ledger would sort it out; if the ledger got lost, a room full of coats
would become a room full of arguments.

By nine o'clock she has learned something. Perhaps a dozen guests keep coming back, out to the
car, in again, out for a phone call. She does not open the ledger for them any more. She knows
that 214 is the grey wool with the red scarf, that 231 is the long camel one, and she reaches
for the hook before the token has fully left the guest's hand. For anyone else she looks it up.
The ledger is never wrong; her head is just faster, for the few she has seen lately.

Once, at the start, she stamped two tokens with the same number. The second guest got a token,
she went to write it in the ledger, and the line for that number was already filled. She did
not write over it. She apologised, took a fresh token with a different number, and started
again. Nobody got the wrong coat. And when a guest turns up with a token she has never issued,
a 900 when she only has tokens to 400, she does not go hunting along the rail; she says, kindly,
that it is not one of hers.

## 3. The idea in plain English

The coat is the long URL and the brass token is the **short code**: seven characters from the
sixty-two letters and digits, chosen at random with `secrets.choice`. Sixty-two to the power
seven is about three and a half trillion, so two guests getting the same token is rare, and
when it happens the ledger catches it.

The ledger is the Postgres table `links(code PRIMARY KEY, url)`. `PRIMARY KEY` is the
"line already filled" rule: a second insert with the same code fails with `UniqueViolation`,
and the service does what Nandini did, rolls back and tries a fresh code. Never overwrite.

Nandini's memory is Redis, used cache-aside exactly as on day 56: on a redirect, `GET link:<code>`
first; on a miss, read the table, `SET` with a one-hour expiry, return. Redis being down is
Nandini having a headache: slower, never wrong, because the ledger is still there.

The two routes are the two sides of the counter. `POST /links` takes a coat and returns a token,
a 201 with the code. `GET /{code}` takes a token and returns the coat, which on the web is a
**302 redirect**: a response whose `Location` header is the long URL, which the browser follows
by itself. A token she never issued is a 404.

Everything else is what the last twelve days built: a pool of connections opened once at
start-up, pydantic checking that the URL is actually a URL, tests with the database and cache
replaced, and a Dockerfile so the whole thing runs with one command.

## 4. The picture

```mermaid
sequenceDiagram
    participant C as client
    participant A as FastAPI
    participant R as Redis
    participant P as Postgres
    C->>A: POST /links {"url": long}
    A->>P: INSERT (code, url)
    P-->>A: ok (or UniqueViolation: retry with a new code)
    A-->>C: 201 {"code": "kX3pQ9a"}
    C->>A: GET /kX3pQ9a
    A->>R: GET link:kX3pQ9a
    R-->>A: nil (miss)
    A->>P: SELECT url WHERE code
    P-->>A: long
    A->>R: SET link:kX3pQ9a long EX 3600
    A-->>C: 302 Location: long
    C->>A: GET /kX3pQ9a (again)
    A->>R: GET link:kX3pQ9a
    R-->>A: long (hit)
    A-->>C: 302 Location: long
```

Notice the create path never touches Redis, and the second redirect never touches Postgres.
Reads are the common case, so the cache sits on the read path only.

## 5. The code, built step by step

Dependencies:

```bash
uv init --name shortener --no-readme
uv add fastapi "uvicorn[standard]" "psycopg[binary,pool]" redis
uv add --dev pytest respx httpx
```

`app.py`, top to bottom. Settings from the environment, as on
[day 51](../day-051-why-sorting-matters/README.md): the two URLs must be set, and the process
refuses to start without them.

```python
import os
import secrets
import string
from collections.abc import Iterator
from contextlib import asynccontextmanager

import psycopg
import redis
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from psycopg_pool import ConnectionPool
from pydantic import BaseModel, HttpUrl

ALPHABET = string.ascii_letters + string.digits
DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.environ["REDIS_URL"]
```

The pool and the cache client, created once. `open=False` so the pool connects at start-up, in
the lifespan, not at import, which is what lets the tests import the module without a database.

```python
pool = ConnectionPool(DATABASE_URL, min_size=1, max_size=4, open=False)
cache = redis.Redis.from_url(REDIS_URL, decode_responses=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS links (
    code TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
)"""
```

The lifespan opens the pool and creates the table; `yield` is the running service; after it, the
pool closes.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open()
    with pool.connection() as conn:
        conn.execute(SCHEMA)
    yield
    pool.close()


app = FastAPI(lifespan=lifespan)
```

The dependency for a connection, so the tests can override it, and the token maker.

```python
def get_conn() -> Iterator[psycopg.Connection]:
    with pool.connection() as conn:
        yield conn


def new_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(7))
```

`secrets`, not `random`: codes must be unguessable, or someone can enumerate every link anyone
has ever shortened.

Create. pydantic's `HttpUrl` rejects anything that is not an `http` or `https` URL with a 422
before the function runs. Three attempts at a code; a collision rolls back and retries.

```python
class LinkIn(BaseModel):
    url: HttpUrl


@app.post("/links", status_code=201)
def create(link: LinkIn, conn: psycopg.Connection = Depends(get_conn)) -> dict[str, str]:
    url = str(link.url)
    for _ in range(3):
        code = new_code()
        try:
            conn.execute("INSERT INTO links (code, url) VALUES (%s, %s)", (code, url))
            conn.commit()
            return {"code": code, "url": url}
        except psycopg.errors.UniqueViolation:
            conn.rollback()
    raise HTTPException(500, detail={"code": "no_code", "message": "could not allocate a code"})
```

`rollback()` is required: after a failed statement, Postgres refuses every further command on
that transaction until it is rolled back.

The lookup, cache-aside. Redis failures are caught and fall through; the function never lets a
cache problem become a 500.

```python
def lookup(code: str, conn: psycopg.Connection) -> str | None:
    key = f"link:{code}"
    try:
        if (cached := cache.get(key)) is not None:
            return cached
    except redis.RedisError:
        pass
    row = conn.execute("SELECT url FROM links WHERE code = %s", (code,)).fetchone()
    if row is None:
        return None
    try:
        cache.set(key, row[0], ex=3600)
    except redis.RedisError:
        pass
    return row[0]
```

Redirect. `RedirectResponse` with 302 sets `Location` and the browser does the rest.

```python
@app.get("/{code}")
def follow(code: str, conn: psycopg.Connection = Depends(get_conn)) -> RedirectResponse:
    url = lookup(code, conn)
    if url is None:
        raise HTTPException(404, detail={"code": "not_found", "message": f"no link {code}"})
    return RedirectResponse(url, status_code=302)
```

Run it against local services and demo:

```bash
DATABASE_URL=postgresql://postgres:secret@127.0.0.1:5432/shortener \
REDIS_URL=redis://127.0.0.1:6379/0 \
python -m uvicorn app:app --port 8000
```

```bash
curl -s -X POST http://127.0.0.1:8000/links \
  -H 'content-type: application/json' \
  -d '{"url":"https://example.com/a/very/long/path?with=query&and=more"}'
curl -i http://127.0.0.1:8000/kX3pQ9a
curl -i http://127.0.0.1:8000/nothere
```

```text
{"code":"kX3pQ9a","url":"https://example.com/a/very/long/path?with=query&and=more"}
HTTP/1.1 302 Found
location: https://example.com/a/very/long/path?with=query&and=more
content-length: 0

HTTP/1.1 404 Not Found
content-type: application/json
{"detail":{"code":"not_found","message":"no link nothere"}}
```

The complete `app.py`:

```python
import os
import secrets
import string
from collections.abc import Iterator
from contextlib import asynccontextmanager

import psycopg
import redis
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from psycopg_pool import ConnectionPool
from pydantic import BaseModel, HttpUrl

ALPHABET = string.ascii_letters + string.digits
DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.environ["REDIS_URL"]

pool = ConnectionPool(DATABASE_URL, min_size=1, max_size=4, open=False)
cache = redis.Redis.from_url(REDIS_URL, decode_responses=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS links (
    code TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
)"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open()
    with pool.connection() as conn:
        conn.execute(SCHEMA)
    yield
    pool.close()


app = FastAPI(lifespan=lifespan)


def get_conn() -> Iterator[psycopg.Connection]:
    with pool.connection() as conn:
        yield conn


def new_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(7))


class LinkIn(BaseModel):
    url: HttpUrl


@app.post("/links", status_code=201)
def create(link: LinkIn, conn: psycopg.Connection = Depends(get_conn)) -> dict[str, str]:
    url = str(link.url)
    for _ in range(3):
        code = new_code()
        try:
            conn.execute("INSERT INTO links (code, url) VALUES (%s, %s)", (code, url))
            conn.commit()
            return {"code": code, "url": url}
        except psycopg.errors.UniqueViolation:
            conn.rollback()
    raise HTTPException(500, detail={"code": "no_code", "message": "could not allocate a code"})


def lookup(code: str, conn: psycopg.Connection) -> str | None:
    key = f"link:{code}"
    try:
        if (cached := cache.get(key)) is not None:
            return cached
    except redis.RedisError:
        pass
    row = conn.execute("SELECT url FROM links WHERE code = %s", (code,)).fetchone()
    if row is None:
        return None
    try:
        cache.set(key, row[0], ex=3600)
    except redis.RedisError:
        pass
    return row[0]


@app.get("/{code}")
def follow(code: str, conn: psycopg.Connection = Depends(get_conn)) -> RedirectResponse:
    url = lookup(code, conn)
    if url is None:
        raise HTTPException(404, detail={"code": "not_found", "message": f"no link {code}"})
    return RedirectResponse(url, status_code=302)
```

The Dockerfile is day 59's, unchanged except the command. The practice sheet carries the
compose file that starts Postgres, Redis, and this image together.

## 6. How the other two languages do it

**Go**

```go
_, err := s.pool.Exec(ctx, "INSERT INTO links (code, url) VALUES ($1, $2)", code, in.URL)
var pgErr *pgconn.PgError
if errors.As(err, &pgErr) && pgErr.Code == "23505" {
	continue // collision: try another code
}
http.Redirect(w, r, longURL, http.StatusFound)
```

The same three attempts, but the collision is a SQLSTATE string compared by hand, and the URL
is validated with `url.ParseRequestURI` and a scheme check, because there is no `HttpUrl`.

**C++**

```cpp
try {
    pqxx::work tx(conn);
    tx.exec_params("INSERT INTO links (code, url) VALUES ($1, $2)", code, url);
    tx.commit();
} catch (const pqxx::unique_violation&) { continue; }
res.set_redirect(long_url, 302);
```

libpqxx maps the violation to a typed exception, which is closer to Python; the transaction
object rolls back on its own when it is destroyed without `commit`.

**The difference that matters:** Python is the only one of the three where the URL check is a
type annotation. `HttpUrl` on the model means a bad URL is a 422 with the field named before
your function runs; in Go and C++ you write the parse, the scheme check, and the error response
yourself, and the first version usually forgets one of `ftp://`, an empty host, or a missing
scheme.

## 7. The traps

**The near-miss: retrying without `rollback()`.** Catch `UniqueViolation` and loop straight
round to the next `INSERT`:

```text
psycopg.errors.InFailedSqlTransaction: current transaction is aborted, commands ignored until end of transaction block
```

A failed statement poisons the transaction. Roll back, then retry.

**`random` instead of `secrets`.** The codes come out fine and the tests pass. But
`random` is predictable from a few outputs, so someone can compute every code you will ever
issue and walk through everyone's links. `secrets.choice` for anything a stranger must not guess.

**Caching the miss the wrong way.** `cache.set(key, "")` for a code that does not exist, to save
the database from repeated 404s, and then `if cached:` treats the empty string as a miss and
reads the database anyway. If you cache misses, use a sentinel you check for by identity, and
give it a short expiry.

**A cache with no expiry.** `cache.set(key, url)` without `ex=` and Redis fills with every link
ever followed. Every key gets a TTL, as on day 56.

**`GET /{code}` swallowing every other route.** `/{code}` matches `/health`, `/docs`, and
`/links` on GET. Declare the specific routes before it, or give the redirect its own prefix
such as `/r/{code}`. FastAPI matches in declaration order.

**Testing against the real Postgres.** The day 58 pattern works here: override `get_conn` with a
connection to a throwaway database, and replace `cache` with a fake that has `get` and `set`.
SQLite will not do this time; `TIMESTAMPTZ` and `%s` placeholders are Postgres. A test database
in the compose file, created and dropped per run, is the honest fixture.

## 8. Say it out loud

**How it gets asked**

- Design and build a URL shortener. Now explain every choice.
- How do you generate the short code, and what happens on a collision?
- Where does the cache go, and what happens when Redis is down?
- Why 302 and not 301?

**The ninety-second script**

Two routes. `POST /links` validates the URL with pydantic's `HttpUrl`, generates a seven-character
code from sixty-two letters and digits with `secrets`, and inserts it into a Postgres table whose
`code` column is the primary key; a collision raises `UniqueViolation`, I roll back and retry
with a fresh code, three times, then give up with a 500 that in practice never fires because the
space is three trillion. `GET /{code}` is cache-aside: `GET link:<code>` on Redis, on a miss
`SELECT` from Postgres and `SET` with a one-hour expiry, then a 302 with `Location` set to the
long URL. Redis errors are caught and fall through to Postgres, so the cache being down is slower,
never wrong. Connections come from a psycopg pool opened in the lifespan, so the tests can import
the app without a database and override `get_conn`. It ships in the day 59 image and runs with
compose next to Postgres and Redis. The choices I would defend: random codes over sequential
ones so links cannot be enumerated, a primary key over a check-then-insert so two requests
cannot race, and 302 over 301 so the redirect is not cached forever by browsers and I can
change or delete a link later.

**The follow-ups**

- **Why not hash the URL to get the code?** *Then the same URL always gets the same code, which
  is a feature for some products and a leak for others: anyone can check whether a given URL has
  been shortened. Random codes plus a unique constraint are simpler and private; if
  deduplication is wanted, add an index on `url` and look it up first.*
- **How would this scale to a billion links?** *The read path is already cache-first; the next
  step is read replicas for Postgres behind the cache, and then sharding the table by code
  prefix. The write path is a single insert and does not need to change until much later. That
  is the system design lesson of [day 60](README.md) meeting the code.*
- **What is missing from this for production?** *Rate limiting on create, an owner on each link,
  a delete route that also `DEL`s the cache key, click counting on a queue rather than in the
  redirect path, and the logs and request ids from day 52.*

**A model answer**

"Create validates with `HttpUrl`, generates a seven-character `secrets` code, inserts with the
code as primary key, and on `UniqueViolation` rolls back and retries. Redirect is cache-aside:
Redis `GET`, on a miss Postgres `SELECT` and Redis `SET` with a one-hour TTL, then a 302 with
`Location`. Redis failures fall through. Pool opened in the lifespan; tests override `get_conn`.
Random codes so links cannot be enumerated, a constraint instead of a check so two creates cannot
race, 302 not 301 so the mapping can change."

## 9. Recall card

- Two routes: `POST /links` → 201 `{"code", "url"}`; `GET /{code}` → `RedirectResponse(url, status_code=302)` or 404. Declare specific routes before the catch-all.
- Code: seven of `string.ascii_letters + string.digits` via `secrets.choice`; `code TEXT PRIMARY KEY`; on `psycopg.errors.UniqueViolation`, `conn.rollback()` then retry, three times.
- Cache-aside on the read path only: `cache.get(f"link:{code}")`, miss → `SELECT`, `cache.set(key, url, ex=3600)`; every `redis.RedisError` is caught and falls through.
- `ConnectionPool(DATABASE_URL, open=False)` opened in the lifespan with `CREATE TABLE IF NOT EXISTS`; `get_conn` yields from `pool.connection()` so tests can override it.
- `HttpUrl` on the request model is the URL check; 302 not 301 so the mapping can change; random not sequential so links cannot be enumerated.
