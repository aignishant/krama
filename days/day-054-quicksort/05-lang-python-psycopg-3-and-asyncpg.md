---
day: 54
track: lang-python
title: "psycopg 3 and asyncpg, and a connection pool"
theme: "Databases II: Postgres and connection pools"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 054 · Python — psycopg 3 and asyncpg, and a connection pool

**Today's theme:** Databases II: Postgres and connection pools

**After today you can:** You can talk to a real Postgres from each language and say why a pool exists.

**The interviewer asks it as:** *Why do you need a connection pool?*

---

## 1. What this is, and why it matters

Postgres is a database server: a separate process, usually on another machine, that many
programs talk to at once over TCP. `psycopg` is the Python driver, `psycopg_pool` keeps a set
of open connections ready to hand out, and `asyncpg` is the driver you use inside the `asyncio`
code from [day 45](../day-045-rotated-array-search/README.md). Everything from yesterday
carries over: statements, parameters, transactions; what is new is that a connection is now an
expensive thing on the far end of a network, and the pool is how you stop paying for it on every
request.

At work, the pool is the piece of a service that decides how it behaves under load, and its two
numbers, the size and the timeout, are the ones you tune first when a database is struggling. In
interviews, "why do you need a connection pool" is asked to see if you know what a connection
costs, and the follow-up, "what size", is asked to see if you know it is not "as many as
possible".

## 2. The story

Sudha manages a bank branch with four counters. Behind each counter sits a teller, and a teller
is not something you conjure up: it takes twenty minutes in the morning to unlock the drawer,
count the float, log into the terminal, and put the name plate out. Nobody does that per
customer.

Customers come to Sudha's desk first and take a token. If a counter is free, she sends them
straight over. If all four are busy, they sit and wait, in order, and the moment a counter
clears, the next token is called. The tellers stay at their counters all day; the customers are
the ones who come and go.

Her predecessor ran it the other way. Whenever a customer arrived, a teller was fetched from the
back office, sat down, unlocked the drawer, served that one customer, locked up, and went back.
Every customer waited twenty minutes before anyone looked at them, and on a busy morning the
back office had eleven people setting up drawers while the queue reached the door. Then the
head office set a limit, eight tellers per branch, and the ninth customer was simply turned
away.

Two things Sudha watches for. A customer who gets to a counter and then wanders off to take a
phone call, leaving the teller sitting there, holding that counter, while the queue grows; she
now gives people a fixed time and calls the next token if they leave. And the number four
itself. She tried eight once, and it was slower, because there is one cash safe at the back
and eight tellers queued for it. Four keeps the safe busy and the counters moving. The right
number is not "as many as fit".

## 3. The idea in plain English

The teller is a **connection**. Opening one to Postgres is a TCP handshake from
[day 47](../day-047-minimise-the-maximum/README.md), a TLS exchange, an authentication round
trip, and on the server side a whole process forked to serve it, with its own memory. Tens of
milliseconds and a few megabytes, per connection. Doing that per request is the predecessor's
branch.

The four counters are a **connection pool**: a fixed set of connections opened once and lent
out. `ConnectionPool(conninfo, min_size=2, max_size=4)` opens two at start and never more than
four. `with pool.connection() as conn:` is taking a token: it hands you a free connection, or
waits until one is free, and returns it to the pool when the block ends. Returning it is the
part people forget.

The head office limit is Postgres's `max_connections`, one hundred by default. Every process
that connects counts against it, and the hundred-and-first gets refused with `too many clients
already`. A service that opens a connection per request under load hits that limit and takes
every other service down with it.

The customer who wanders off is a **leaked connection**: code that took one from the pool and
did not give it back, because an exception skipped the return or because a long computation
happened while holding it. The pool has a `timeout`; a caller that waits longer than that for a
free connection gets a `PoolTimeout`, and that error is the signal that something is holding
counters.

The number four is the **pool size**, and Sudha's cash safe is the database's disk and CPU. More
connections than the database can serve at once do not add throughput; they add queueing
inside the database, where it is harder to see. A starting rule is a small multiple of the
database machine's cores, shared across every process that connects.

Placeholders change: psycopg uses `%s`, not `?`, and asyncpg uses `$1`, `$2`. `RETURNING id`
gives you the new row's id in the same statement, instead of a separate `lastrowid`.

## 4. The picture

```mermaid
flowchart LR
    R1[request 1] -->|with pool.connection| P
    R2[request 2] -->|with pool.connection| P
    R3[request 3] -->|with pool.connection| P
    R4[request 4] -->|with pool.connection| P
    R5[request 5] -->|waits, up to timeout| P
    P[pool: 4 connections] -->|conn 1| DB[(Postgres)]
    P -->|conn 2| DB
    P -->|conn 3| DB
    P -->|conn 4| DB
```

Notice that request 5 waits at the pool, not at the database. That is the point: the pool is
where the queue forms, and a queue you can see and time is a queue you can size.

## 5. The code, built step by step

You need a Postgres to talk to. The quickest is a container:

```bash
docker run --name pg -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=app -p 5432:5432 -d postgres:16
python -m pip install "psycopg[binary]" psycopg_pool
```

The connection string comes from the environment, as on
[day 51](../day-051-why-sorting-matters/README.md), because it has the password in it.

The pool.

```python
import os
import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

DSN = os.environ["DATABASE_URL"]   # postgresql://postgres:secret@localhost:5432/app

pool = ConnectionPool(DSN, min_size=2, max_size=4, timeout=5, kwargs={"row_factory": dict_row}, open=False)
```

`min_size` connections are opened when the pool opens; `max_size` is the ceiling; `timeout` is
how long a caller waits for a free one before `PoolTimeout`. `kwargs` are passed to every
`psycopg.connect`, so every connection returns rows as dicts. `open=False` means it opens when
you say, in `main`, not at import time.

The schema.

```python
def create_schema() -> None:
    with pool.connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                city TEXT NOT NULL,
                balance INTEGER NOT NULL DEFAULT 0
            )
        """)
```

`SERIAL` is Postgres's auto-incrementing integer. `pool.connection()` lends a connection, and
the `with` returns it and commits, or rolls back on an exception, exactly like yesterday's `with
conn:`.

Insert and read, with `%s` and `RETURNING`.

```python
def add_user(name: str, city: str) -> int:
    with pool.connection() as conn:
        row = conn.execute("INSERT INTO users (name, city) VALUES (%s, %s) RETURNING id", (name, city)).fetchone()
        return row["id"]


def find_by_name(name: str) -> dict | None:
    with pool.connection() as conn:
        return conn.execute("SELECT id, name, city, balance FROM users WHERE name = %s", (name,)).fetchone()
```

`%s` is the placeholder, for every type, and the values are a tuple as before. It looks like
old-style string formatting and is not: the driver sends the values separately. `RETURNING id`
makes the insert return a row, so `fetchone` gives the id.

The transfer, as a transaction on one connection.

```python
def transfer(from_id: int, to_id: int, amount: int) -> None:
    with pool.connection() as conn:
        conn.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, from_id))
        row = conn.execute("SELECT balance FROM users WHERE id = %s", (from_id,)).fetchone()
        if row["balance"] < 0:
            raise ValueError("insufficient balance")
        conn.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, to_id))
```

Both updates go through the same `conn`, inside the same `with`, so they are one transaction. A
transaction cannot span two connections, which is why the transfer takes the connection once at
the top and not per statement.

Seeing the pool wait.

```python
def hold(seconds: float) -> None:
    with pool.connection() as conn:
        conn.execute("SELECT pg_sleep(%s)", (seconds,))
```

`pg_sleep` makes the database hold the connection busy. The main program runs five of these at
once on threads, with a pool of four, and times them.

```python
def main() -> None:
    pool.open()
    create_schema()
    meera = add_user("Meera", "Pune")
    arjun = add_user("Arjun", "Delhi")
    with pool.connection() as conn:
        conn.execute("UPDATE users SET balance = 100 WHERE id = %s", (meera,))
    print("inserted ids:", meera, arjun)
    print("found:", find_by_name("Meera"))
    transfer(meera, arjun, 30)
    try:
        transfer(meera, arjun, 500)
    except ValueError as err:
        print("transfer refused:", err)

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as workers:
        for _ in range(5):
            workers.submit(hold, 1.0)
    print(f"five 1-second holds on a pool of 4 took {time.perf_counter() - start:.1f}s")
    print("pool stats:", {k: pool.get_stats()[k] for k in ("pool_size", "requests_waiting", "requests_num")})
    pool.close()
```

Run it:

```bash
DATABASE_URL=postgresql://postgres:secret@localhost:5432/app python main.py
```

```text
inserted ids: 1 2
found: {'id': 1, 'name': 'Meera', 'city': 'Pune', 'balance': 100}
transfer refused: insufficient balance
five 1-second holds on a pool of 4 took 2.0s
pool stats: {'pool_size': 4, 'requests_waiting': 0, 'requests_num': 10}
```

The fourth line is the picture: four holds ran together, the fifth waited for a counter, two
seconds in all. `requests_num` is how many times a connection was lent out.

**The same thing with asyncpg.** Inside an `asyncio` service the driver is `asyncpg`, which has
its own pool and its own placeholders:

```python
import asyncpg

async def main() -> None:
    pool = await asyncpg.create_pool(DSN, min_size=2, max_size=4)
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, name FROM users WHERE name = $1", "Meera")
        print(dict(row))
    await pool.close()
```

`$1`, `$2` instead of `%s`; `fetchrow`, `fetch` and `execute` are all awaited; `pool.acquire()`
is the token. Transactions are `async with conn.transaction():`. The pool arithmetic is
identical, and so is the leak.

Here is the whole program in one piece, `main.py`:

```python
import os
import time
from concurrent.futures import ThreadPoolExecutor

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

DSN = os.environ["DATABASE_URL"]

pool = ConnectionPool(DSN, min_size=2, max_size=4, timeout=5, kwargs={"row_factory": dict_row}, open=False)


def create_schema() -> None:
    with pool.connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                city TEXT NOT NULL,
                balance INTEGER NOT NULL DEFAULT 0
            )
        """)


def add_user(name: str, city: str) -> int:
    with pool.connection() as conn:
        row = conn.execute("INSERT INTO users (name, city) VALUES (%s, %s) RETURNING id", (name, city)).fetchone()
        return row["id"]


def find_by_name(name: str) -> dict | None:
    with pool.connection() as conn:
        return conn.execute("SELECT id, name, city, balance FROM users WHERE name = %s", (name,)).fetchone()


def transfer(from_id: int, to_id: int, amount: int) -> None:
    with pool.connection() as conn:
        conn.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, from_id))
        row = conn.execute("SELECT balance FROM users WHERE id = %s", (from_id,)).fetchone()
        if row["balance"] < 0:
            raise ValueError("insufficient balance")
        conn.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, to_id))


def hold(seconds: float) -> None:
    with pool.connection() as conn:
        conn.execute("SELECT pg_sleep(%s)", (seconds,))


def main() -> None:
    pool.open()
    create_schema()
    meera = add_user("Meera", "Pune")
    arjun = add_user("Arjun", "Delhi")
    with pool.connection() as conn:
        conn.execute("UPDATE users SET balance = 100 WHERE id = %s", (meera,))
    print("inserted ids:", meera, arjun)
    print("found:", find_by_name("Meera"))
    transfer(meera, arjun, 30)
    try:
        transfer(meera, arjun, 500)
    except ValueError as err:
        print("transfer refused:", err)

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as workers:
        for _ in range(5):
            workers.submit(hold, 1.0)
    print(f"five 1-second holds on a pool of 4 took {time.perf_counter() - start:.1f}s")
    print("pool stats:", {k: pool.get_stats()[k] for k in ("pool_size", "requests_waiting", "requests_num")})
    pool.close()


if __name__ == "__main__":
    main()
```

## 6. How the other two languages do it

**Go**

```go
cfg, _ := pgxpool.ParseConfig(dsn)
cfg.MaxConns = 4
pool, err := pgxpool.NewWithConfig(ctx, cfg)
err = pool.QueryRow(ctx, "SELECT id FROM users WHERE name = $1", name).Scan(&id)
```

`pgxpool` is the pool and the query interface in one: `pool.QueryRow` borrows a connection,
runs the statement, and returns it. Every call takes a context, so a caller waiting on an
exhausted pool can be given a deadline.

**C++**

```cpp
Pool pool(dsn, 4);                       // a class you write: vector, mutex, condition_variable
auto lease = pool.acquire();             // blocks until one is free; destructor returns it
pqxx::work tx(*lease);
auto row = tx.exec_params1("SELECT id FROM users WHERE name = $1", name);
tx.commit();
```

libpqxx has connections and transactions and no pool, so the pool is the day 32 mutex and
condition variable around a vector of connections, with an RAII lease that returns the
connection on destruction.

**The difference that matters:** Python's `with pool.connection()` returns the connection on
every path out, including an exception, because it is a context manager. Go returns it when
`rows.Close` or `Scan` finishes, and a forgotten `Close` leaks it silently. C++ returns it when
the lease object dies, which is the one you wrote. All three leak if a long computation runs
inside the borrow; the Python version just makes the borrow's edges visible as indentation.

## 7. The traps

**The near-miss: a connection per request.**

```python
def find_by_name(name: str) -> dict | None:
    with psycopg.connect(DSN, row_factory=dict_row) as conn:
        return conn.execute("SELECT ... WHERE name = %s", (name,)).fetchone()
```

It works, it is correct, and it is Sudha's predecessor. Each call pays the handshake and the
server-side fork. Under load, Postgres answers:

```text
psycopg.OperationalError: connection failed: FATAL:  sorry, too many clients already
```

and so does every other service sharing that database.

**Holding a connection while doing something slow.**

```python
with pool.connection() as conn:
    user = conn.execute("SELECT ...").fetchone()
    send_email(user)            # two seconds, connection held for nothing
```

The counter is held while the customer takes a phone call. With four such calls in flight, the
fifth request waits, and after `timeout`:

```text
psycopg_pool.PoolTimeout: couldn't get a connection after 5.00 sec
```

Borrow, query, return, then do the slow thing.

**A transaction across two borrows.**

```python
with pool.connection() as conn:
    conn.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, from_id))
with pool.connection() as conn:
    conn.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, to_id))
```

Two connections, two transactions, and a crash between them loses the money. One borrow for the
whole transfer.

**`?` from yesterday.**

```text
psycopg.ProgrammingError: query parameters are not supported for this query: the query contains a '?' placeholder
```

psycopg wants `%s`; asyncpg wants `$1`. Same idea, different spelling, and the driver tells you.

**Running it twice.**

```text
psycopg.errors.UniqueViolation: duplicate key value violates unique constraint "users_name_key"
DETAIL:  Key (name)=(Meera) already exists.
```

Postgres names the constraint and the key. `except psycopg.errors.UniqueViolation` is the
[day 50](../day-050-binary-search-revision/README.md) 409.

**No table.**

```text
psycopg.errors.UndefinedTable: relation "users" does not exist
LINE 1: SELECT id, name, city, balance FROM users WHERE name = 'Meera'
                                            ^
```

Postgres says "relation"; it means table. Usually the wrong database in the DSN.

**Nobody home.**

```text
psycopg.OperationalError: connection failed: connection to server at "127.0.0.1", port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
```

The container is not up, or the port is not published.

## 8. Say it out loud

**How it gets asked**

- Why do you need a connection pool?
- What does opening a database connection cost?
- How big should the pool be?
- What happens when the pool is exhausted, and what does that tell you?

**The ninety-second script**

A database connection is expensive on both ends: a TCP handshake, a TLS exchange and an
authentication round trip on the way in, and on the Postgres side a forked process with its own
memory for as long as it lives. Tens of milliseconds and megabytes, per connection. A service
that opens one per request pays that latency on every call, and under load it hits Postgres's
`max_connections`, at which point every service sharing that database starts getting refused.
A pool opens a fixed set of connections once, at start-up, and lends them out: borrow, run the
statements, return. Requests beyond the pool's size queue at the pool, where the wait is visible
and has a timeout, instead of inside the database. The size is not "as many as possible": more
connections than the database can serve concurrently just move the queue inside Postgres. A
small multiple of the database's cores, shared across all the processes that connect, is the
starting point, and the pool's wait time is the number you watch to adjust it. The one thing
that breaks it is holding a borrowed connection while doing something slow that is not a query,
so the borrow is as short as the transaction and no shorter.

**The follow-ups**

- **Why does a transaction have to stay on one connection?** *A transaction is state inside the
  server process behind that connection. Another connection is another process with no idea
  the first one has an open transaction. Borrow once for the whole transaction.*
- **Pool per process, or shared?** *Per process, and the sum across processes has to fit under
  `max_connections`. Ten workers with a pool of ten each is a hundred, which is the default
  ceiling exactly, with nothing left for a migration or a human. That is what an external pooler
  like PgBouncer is for.*
- **What does a pool timeout mean at 3am?** *Either the database is slow, so every borrow is
  long, or some code path is holding connections while doing something else. The pool's
  `requests_waiting` and the database's active query list tell you which.*

**A model answer**

"Because a connection is a handshake, a TLS exchange, authentication, and a forked server
process, and because Postgres caps how many it will hold. A pool opens a fixed set once and
lends them out, so a request pays nothing to start talking and the queue forms at the pool,
where I can see and bound it. In Python, `psycopg_pool.ConnectionPool` with `min_size`,
`max_size` and `timeout`, and `with pool.connection()` so the return is automatic. Size is a
small multiple of the database's cores across all processes, not a large number; more than the
database can serve concurrently only hides the queue inside it."

## 9. Recall card

- A connection is a handshake, TLS, auth, and a forked server process; Postgres caps them at `max_connections`. Never one per request.
- `ConnectionPool(DSN, min_size=, max_size=, timeout=)`; `with pool.connection() as conn:` borrows and returns on every path out.
- Borrow only as long as the transaction; a slow thing inside the borrow holds a counter, and the fifth caller gets `PoolTimeout`.
- Placeholders are `%s` in psycopg and `$1` in asyncpg; `RETURNING id` replaces `lastrowid`.
- Size is a small multiple of the database's cores across all processes; watch the pool's wait time, not its size.
