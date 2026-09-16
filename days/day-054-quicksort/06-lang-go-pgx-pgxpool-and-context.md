---
day: 54
track: lang-go
title: "pgx, pgxpool, and context-aware queries"
theme: "Databases II: Postgres and connection pools"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 054 · Go — pgx, pgxpool, and context-aware queries

**Today's theme:** Databases II: Postgres and connection pools

**After today you can:** You can talk to a real Postgres from each language and say why a pool exists.

**The interviewer asks it as:** *Why do you need a connection pool?*

---

## 1. What this is, and why it matters

`pgx` is the Postgres driver most Go services use, and `pgxpool` is its pool: `pgxpool.New`
opens a set of connections and gives you back an object with `QueryRow`, `Query`, `Exec` and
`Begin` on it, each of which borrows a connection, uses it, and returns it. Every call takes a
`context.Context` from [day 36](../day-036-two-pointers-revision/README.md) as its first
argument, so a query can be cancelled and a wait for a free connection can be bounded. Yesterday's
`database/sql` still works with Postgres; `pgx` is what you use when you want the pool and the
Postgres-specific types without the generic layer.

At work, the pool's `MaxConns` and the context's deadline are the two knobs that decide what a
Go service does when the database slows down: queue politely, or fall over. In interviews, "why
do you need a connection pool" is answered the same way in every language; the Go follow-up is
about `ctx`, and what a query does when the request that asked for it has already gone.

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

Sudha added one thing her predecessor never had. Every token has a time on it. A customer who
has waited past that time is not called; Sudha tells them the branch is too busy and asks them
to come back, rather than letting the queue grow past the door. And a customer who leaves the
queue, because their bus is here, hands the token back on the way out, so a counter is not held
for someone who has already gone. The tellers know to look up, see the empty chair, and call
the next number.

## 3. The idea in plain English

The teller is a **connection**: a TCP handshake from
[day 47](../day-047-minimise-the-maximum/README.md), a TLS exchange, an authentication round
trip, and a forked process on the Postgres side with its own memory. Tens of milliseconds and
megabytes each. The four counters are the **pool**, `pgxpool.New(ctx, dsn)`: a fixed set opened
once and lent out. `pool.QueryRow(ctx, sql, args...)` takes a token, runs the statement on a
free connection, and returns it. `pool.Acquire(ctx)` takes a token and gives you the connection
itself, for when several statements must share one, and `conn.Release()` hands it back.

The head office limit is Postgres's `max_connections`, one hundred by default, counted across
every process that connects. `MaxConns` on the pool config is your branch's share of it.

The time on the token is the **context**. `ctx, cancel := context.WithTimeout(ctx, 2*time.Second)`
bounds the whole call: waiting for a free connection and running the query. If the deadline
passes while waiting, the call returns `context.DeadlineExceeded` instead of queueing forever.
Handing the token back on the way out is cancellation: in a server, `r.Context()` is cancelled
when the client disconnects, and a query given that context is cancelled on the Postgres side
too, so a counter is not held for a caller who has gone.

Placeholders are `$1`, `$2`, numbered, not `?`. `RETURNING id` gives you the new row's id from
the insert. `pgx.ErrNoRows` is "not found" from `Scan`, and a Postgres error is a `*pgconn.PgError`
whose `Code` is the five-character SQLSTATE, `23505` for a unique violation.

## 4. The picture

```mermaid
flowchart LR
    R1[handler 1] -->|QueryRow ctx| P
    R2[handler 2] -->|QueryRow ctx| P
    R3[handler 3] -->|QueryRow ctx| P
    R4[handler 4] -->|QueryRow ctx| P
    R5[handler 5] -->|waits until ctx deadline| P
    P[pgxpool MaxConns=4] -->|conn 1| DB[(Postgres)]
    P -->|conn 2| DB
    P -->|conn 3| DB
    P -->|conn 4| DB
```

Notice that handler 5 waits at the pool with a deadline on its token. When the deadline passes
it gets an error and can answer 503, instead of holding a goroutine and a client forever.

## 5. The code, built step by step

A Postgres to talk to, and the module:

```bash
docker run --name pg -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=app -p 5432:5432 -d postgres:16
go mod init users && go get github.com/jackc/pgx/v5
```

The pool, from a config.

```go
cfg, err := pgxpool.ParseConfig(os.Getenv("DATABASE_URL"))
if err != nil {
	return err
}
cfg.MaxConns = 4
cfg.MinConns = 2
pool, err := pgxpool.NewWithConfig(ctx, cfg)
if err != nil {
	return err
}
defer pool.Close()
if err := pool.Ping(ctx); err != nil {
	return err
}
```

`ParseConfig` reads the DSN, `MaxConns` and `MinConns` are the counters, and `Ping` is the
start-up check that the database is really there. The DSN comes from the environment because it
carries the password, as on [day 51](../day-051-why-sorting-matters/README.md).

Insert and read, with `$1` and `RETURNING`.

```go
func addUser(ctx context.Context, pool *pgxpool.Pool, name, city string) (int, error) {
	var id int
	err := pool.QueryRow(ctx, "INSERT INTO users (name, city) VALUES ($1, $2) RETURNING id", name, city).Scan(&id)
	return id, err
}

func findByName(ctx context.Context, pool *pgxpool.Pool, name string) (*User, error) {
	var u User
	err := pool.QueryRow(ctx, "SELECT id, name, city, balance FROM users WHERE name = $1", name).
		Scan(&u.ID, &u.Name, &u.City, &u.Balance)
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &u, nil
}
```

`pool.QueryRow` borrows and returns inside the call; `Scan` is the same as yesterday, and the
`RETURNING` makes the insert a one-row query, so the id comes back through `Scan` too.

The transfer, as a transaction on one borrowed connection.

```go
func transfer(ctx context.Context, pool *pgxpool.Pool, from, to, amount int) error {
	tx, err := pool.Begin(ctx)
	if err != nil {
		return err
	}
	defer tx.Rollback(ctx)
	if _, err := tx.Exec(ctx, "UPDATE users SET balance = balance - $1 WHERE id = $2", amount, from); err != nil {
		return err
	}
	var balance int
	if err := tx.QueryRow(ctx, "SELECT balance FROM users WHERE id = $1", from).Scan(&balance); err != nil {
		return err
	}
	if balance < 0 {
		return errors.New("insufficient balance")
	}
	if _, err := tx.Exec(ctx, "UPDATE users SET balance = balance + $1 WHERE id = $2", amount, to); err != nil {
		return err
	}
	return tx.Commit(ctx)
}
```

`pool.Begin` borrows one connection for the whole transaction; `Commit` or the deferred
`Rollback` returns it. Every statement takes `ctx`, so a cancelled request rolls the transfer
back and frees the counter.

Seeing the pool wait, and the deadline.

```go
func hold(ctx context.Context, pool *pgxpool.Pool, seconds float64) error {
	_, err := pool.Exec(ctx, "SELECT pg_sleep($1)", seconds)
	return err
}
```

`main` runs five of these at once with `MaxConns = 4` and a two-second deadline on the fifth's
context.

```go
start := time.Now()
var wg sync.WaitGroup
for i := 0; i < 5; i++ {
	wg.Add(1)
	go func() {
		defer wg.Done()
		if err := hold(ctx, pool, 1.0); err != nil {
			fmt.Println("hold:", err)
		}
	}()
}
wg.Wait()
fmt.Printf("five 1-second holds on a pool of 4 took %.1fs\n", time.Since(start).Seconds())
```

Run it:

```bash
DATABASE_URL=postgresql://postgres:secret@localhost:5432/app go run main.go
```

```text
inserted ids: 1 2
found: {1 Meera Pune 100}
transfer refused: insufficient balance
five 1-second holds on a pool of 4 took 2.0s
pool: total=4 acquired=0 idle=4
```

Four holds ran together, the fifth waited for a counter. Now give each hold a deadline,
`context.WithTimeout(ctx, 1500*time.Millisecond)`, and the fifth does not get to finish:

```text
hold: timeout: context deadline exceeded
five 1-second holds on a pool of 4 took 1.5s
```

The fifth got a counter at the one-second mark, ran for half a second, and at its deadline `pgx`
cancelled the query on the Postgres side and returned. That is the token with a time on it: the
caller got an error it can turn into a 503, the connection went straight back to the pool, and
nothing sat past the deadline. Make the deadline shorter than one second and the fifth never
gets a counter at all; the error is then a plain `context deadline exceeded` from the wait.

Here is the whole program in one piece, `main.go`:

```go
package main

import (
	"context"
	"errors"
	"fmt"
	"os"
	"sync"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

const schema = `
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    balance INTEGER NOT NULL DEFAULT 0
)`

type User struct {
	ID      int
	Name    string
	City    string
	Balance int
}

func addUser(ctx context.Context, pool *pgxpool.Pool, name, city string) (int, error) {
	var id int
	err := pool.QueryRow(ctx, "INSERT INTO users (name, city) VALUES ($1, $2) RETURNING id", name, city).Scan(&id)
	return id, err
}

func findByName(ctx context.Context, pool *pgxpool.Pool, name string) (*User, error) {
	var u User
	err := pool.QueryRow(ctx, "SELECT id, name, city, balance FROM users WHERE name = $1", name).
		Scan(&u.ID, &u.Name, &u.City, &u.Balance)
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &u, nil
}

func transfer(ctx context.Context, pool *pgxpool.Pool, from, to, amount int) error {
	tx, err := pool.Begin(ctx)
	if err != nil {
		return err
	}
	defer tx.Rollback(ctx)
	if _, err := tx.Exec(ctx, "UPDATE users SET balance = balance - $1 WHERE id = $2", amount, from); err != nil {
		return err
	}
	var balance int
	if err := tx.QueryRow(ctx, "SELECT balance FROM users WHERE id = $1", from).Scan(&balance); err != nil {
		return err
	}
	if balance < 0 {
		return errors.New("insufficient balance")
	}
	if _, err := tx.Exec(ctx, "UPDATE users SET balance = balance + $1 WHERE id = $2", amount, to); err != nil {
		return err
	}
	return tx.Commit(ctx)
}

func hold(ctx context.Context, pool *pgxpool.Pool, seconds float64) error {
	_, err := pool.Exec(ctx, "SELECT pg_sleep($1)", seconds)
	return err
}

func run(ctx context.Context) error {
	cfg, err := pgxpool.ParseConfig(os.Getenv("DATABASE_URL"))
	if err != nil {
		return err
	}
	cfg.MaxConns = 4
	cfg.MinConns = 2
	pool, err := pgxpool.NewWithConfig(ctx, cfg)
	if err != nil {
		return err
	}
	defer pool.Close()
	if err := pool.Ping(ctx); err != nil {
		return err
	}
	if _, err := pool.Exec(ctx, schema); err != nil {
		return err
	}

	meera, err := addUser(ctx, pool, "Meera", "Pune")
	if err != nil {
		return err
	}
	arjun, err := addUser(ctx, pool, "Arjun", "Delhi")
	if err != nil {
		return err
	}
	if _, err := pool.Exec(ctx, "UPDATE users SET balance = 100 WHERE id = $1", meera); err != nil {
		return err
	}
	fmt.Println("inserted ids:", meera, arjun)

	found, err := findByName(ctx, pool, "Meera")
	if err != nil {
		return err
	}
	fmt.Println("found:", *found)

	if err := transfer(ctx, pool, meera, arjun, 30); err != nil {
		return err
	}
	if err := transfer(ctx, pool, meera, arjun, 500); err != nil {
		fmt.Println("transfer refused:", err)
	}

	start := time.Now()
	var wg sync.WaitGroup
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if err := hold(ctx, pool, 1.0); err != nil {
				fmt.Println("hold:", err)
			}
		}()
	}
	wg.Wait()
	fmt.Printf("five 1-second holds on a pool of 4 took %.1fs\n", time.Since(start).Seconds())
	stat := pool.Stat()
	fmt.Printf("pool: total=%d acquired=%d idle=%d\n", stat.TotalConns(), stat.AcquiredConns(), stat.IdleConns())
	return nil
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	if err := run(ctx); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
```

## 6. How the other two languages do it

**Python**

```python
pool = ConnectionPool(DSN, min_size=2, max_size=4, timeout=5)
with pool.connection() as conn:
    row = conn.execute("SELECT id FROM users WHERE name = %s", (name,)).fetchone()
```

The pool's `timeout` is the token's time; there is no context, so a cancelled request cannot
cancel its query. The `with` returns the connection on every path out.

**C++**

```cpp
Pool pool(dsn, 4);
auto lease = pool.acquire(std::chrono::seconds(2));   // throws if none free in time
pqxx::work tx(*lease);
auto row = tx.exec_params1("SELECT id FROM users WHERE name = $1", name);
```

The pool is a class you write with a mutex and a condition variable, and `acquire` with a
deadline is `wait_for` on the condition variable. The lease returns the connection in its
destructor.

**The difference that matters:** Go's `ctx` reaches all the way to the database. When a client
disconnects, `r.Context()` is cancelled, `pgx` sends a cancel to Postgres, the running query
stops, the transaction rolls back and the connection goes back to the pool. Python's
`psycopg_pool` and a hand-written C++ pool bound the wait for a connection, but a query that is
already running on behalf of a caller who has gone runs to completion, holding the counter.
That is why every `pgx` call takes a context, and why passing `context.Background()` from a
handler is the wrong thing.

## 7. The traps

**The near-miss: `pgx.Connect` in a handler.**

```go
conn, err := pgx.Connect(ctx, dsn)
defer conn.Close(ctx)
```

A single connection, opened per request. Correct, and Sudha's predecessor. Under load:

```text
failed to connect to `host=localhost user=postgres database=app`: server error (FATAL: sorry, too many clients already (SQLSTATE 53300))
```

**`context.Background()` in a handler.** The query runs to the end after the client has gone,
and so does the transaction. Use `r.Context()`, and derive a timeout from it when the query
should not be allowed to take longer than the caller will wait.

**Acquire without Release.**

```go
conn, err := pool.Acquire(ctx)
rows, err := conn.Query(ctx, "SELECT ...")
// no conn.Release()
```

No error. The pool's `AcquiredConns` climbs by one per call, and after `MaxConns` calls every
`QueryRow` in the process waits until its context expires:

```text
context deadline exceeded
```

`defer conn.Release()` on the line after `Acquire`, or use `pool.QueryRow` and let it borrow and
return for you.

**`?` from SQLite.**

```text
ERROR: syntax error at or near "?" (SQLSTATE 42601)
```

Postgres wants `$1`. The SQLSTATE at the end is how `pgx` reports every server error; `42601` is
"syntax error".

**Running it twice.**

```text
ERROR: duplicate key value violates unique constraint "users_name_key" (SQLSTATE 23505)
```

To turn that into a 409 rather than a 500:

```go
var pgErr *pgconn.PgError
if errors.As(err, &pgErr) && pgErr.Code == "23505" { /* conflict */ }
```

**No table.**

```text
ERROR: relation "users" does not exist (SQLSTATE 42P01)
```

**Nobody home.**

```text
failed to connect to `host=localhost user=postgres database=app`: dial error (dial tcp 127.0.0.1:5432: connect: connection refused)
```

The container is not up, or the port is not published.

**Forgetting `rows.Close()`.** Same as yesterday, and worse: the connection stays acquired from
the pool, and after `MaxConns` such leaks the service is dead. `defer rows.Close()` on the next
line, every time.

## 8. Say it out loud

**How it gets asked**

- Why do you need a connection pool?
- What does the context do on a database call?
- How big should the pool be?
- What happens when the pool is exhausted, and what do you return to the caller?

**The ninety-second script**

A connection is a TCP handshake, a TLS exchange, an authentication round trip, and a forked
process on the Postgres side with its own memory, so tens of milliseconds and megabytes per
connection, and Postgres caps them at `max_connections` across every client. A service that
connects per request pays that on every call and, under load, hits the cap and takes every
other service down with it. A pool opens a fixed set once and lends them out, so a request pays
nothing to start and the queue forms at the pool, where it is visible and bounded. In Go that
is `pgxpool` with `MaxConns`, and every call takes a context: the context bounds how long a
caller waits for a free connection, and it reaches the database, so a client that disconnects
cancels its query and frees the connection. When the pool is exhausted, a call returns
`context.DeadlineExceeded` and I answer 503, rather than holding the goroutine. The size is a
small multiple of the database's cores across all my processes, not a large number; more than
the database can serve at once only moves the queue inside Postgres, where I cannot see it.

**The follow-ups**

- **`pgx` or `database/sql`?** *`database/sql` with the `pgx` stdlib adapter if the code must
  stay database-agnostic; `pgx` directly for the pool, the context on every call, and Postgres
  types like arrays and JSONB without conversion. Both are parameterised; both leak on a
  forgotten `rows.Close`.*
- **How do you turn a cancelled query into the right response?** *`errors.Is(err,
  context.Canceled)` means the client went away, so nothing to send; `context.DeadlineExceeded`
  means my own timeout fired, so 503 or 504 with a request id in the log.*
- **What about ten replicas of the service?** *Ten pools of four is forty connections, and
  they all count against the same `max_connections`. That sum is the number to plan, and
  PgBouncer in front of Postgres is how you let it exceed what Postgres itself can hold.*

**A model answer**

"A connection is a handshake, TLS, auth and a server process, capped by `max_connections`.
`pgxpool` opens `MaxConns` once and lends them: `pool.QueryRow(ctx, ...)` borrows and returns
inside the call, `pool.Begin(ctx)` borrows one for the whole transaction with `defer
tx.Rollback(ctx)`. The context bounds the wait and cancels the query when the caller is gone.
Exhaustion is `context.DeadlineExceeded`, which becomes a 503. Size is a small multiple of the
database's cores, summed across every replica."

## 9. Recall card

- A connection is a handshake, TLS, auth and a forked server process, capped by `max_connections`; never `pgx.Connect` per request.
- `pgxpool.ParseConfig(dsn)`, set `MaxConns`, `pgxpool.NewWithConfig(ctx, cfg)`, `pool.Ping(ctx)`; `pool.QueryRow(ctx, ...)` borrows and returns.
- `pool.Begin(ctx)`, `defer tx.Rollback(ctx)`, statements on `tx`, `tx.Commit(ctx)`; one connection for the whole transaction.
- Every call takes `ctx`; a handler passes `r.Context()`, so a gone client cancels the query and frees the counter. Exhaustion is `context.DeadlineExceeded`.
- Placeholders are `$1`; errors carry a SQLSTATE, `23505` is the unique violation, read with `errors.As(err, &pgErr)`.
