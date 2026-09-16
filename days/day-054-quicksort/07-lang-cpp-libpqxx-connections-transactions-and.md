---
day: 54
track: lang-cpp
title: "libpqxx: connections, transactions, and prepared statements"
theme: "Databases II: Postgres and connection pools"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 054 · C++ — libpqxx: connections, transactions, and prepared statements

**Today's theme:** Databases II: Postgres and connection pools

**After today you can:** You can talk to a real Postgres from each language and say why a pool exists.

**The interviewer asks it as:** *Why do you need a connection pool?*

---

## 1. What this is, and why it matters

libpqxx is the C++ library for Postgres: `pqxx::connection` opens one, `pqxx::work` is a
transaction on it, `exec_params` runs a statement with `$1` placeholders and returns a
`pqxx::result` you index like a table, and `commit()` makes it permanent. Every failure is an
exception with a Postgres error message inside. What libpqxx does not have is a pool, so today
you write one: a fixed set of connections, a mutex and a condition variable from
[day 32](../day-032-variable-window/README.md), and a lease object that returns the connection
when it goes out of scope.

At work, the pool you write today is the one in most C++ services, give or take a feature, and
writing it once is how you understand what every other language's pool is doing for you. In
interviews, "why do you need a connection pool" is the same question everywhere; the C++
follow-up is "how would you implement one", and you will have.

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

There was no token machine when Sudha arrived; she built the system herself with a box of
numbered discs and a bell. A customer takes a disc from the box. When a teller finishes, they
ring the bell, and the customer holding the lowest disc walks up and drops it back in the box
on the way. If the box is empty, the customer waits by it until a disc comes back. Nobody keeps
a disc in their pocket after they are served; the disc goes back in the box the moment they turn
from the counter, and everyone knows it, because a disc in a pocket is a counter nobody can use.

## 3. The idea in plain English

The teller is a **connection**, `pqxx::connection conn(dsn)`: a TCP handshake from
[day 47](../day-047-minimise-the-maximum/README.md), TLS, an authentication round trip, and a
forked process on the Postgres side. Tens of milliseconds and megabytes each. The head office
limit is `max_connections`, one hundred by default across every client.

The box of discs is the **pool** you write. It holds a `std::vector` of connections opened once
in its constructor, a `std::mutex` guarding the vector, and a `std::condition_variable` that
is the bell. `acquire()` locks, waits on the condition variable until the vector is not empty,
takes one, and returns it wrapped in a **lease**. The lease is the disc: an object whose
destructor puts the connection back and rings the bell. A lease held across a slow operation is
the disc in the pocket, and it is the whole failure mode of pools in one sentence.

`acquire(timeout)` uses `wait_for` on the condition variable, so a caller waits at most that
long and then gets an exception, rather than queueing forever. That is the token with a time on
it.

A **transaction** is `pqxx::work tx(conn)`: it begins when constructed and, if destroyed
without `commit()`, rolls back. That is the `Transaction` class from
[day 53](../day-053-merge-sort/README.md), built in. `tx.exec_params(sql, args...)` runs a
statement with `$1`, `$2` placeholders and returns a `pqxx::result`; `exec_params1` is the same
and insists on exactly one row. A row is indexed by column name, `row["id"].as<int>()`.

A **prepared statement**, `conn.prepare("find", sql)` then `tx.exec_prepared("find", name)`,
parses the SQL once per connection and runs it by name. It belongs to the connection, so a pool
prepares it on every connection at start-up.

Errors are exceptions: `pqxx::unique_violation`, `pqxx::undefined_table`,
`pqxx::broken_connection`, all under `pqxx::sql_error` and `std::exception`, each carrying the
server's message in `what()`.

## 4. The picture

```text
   Pool pool(dsn, 4)                  connections: [c1] [c2] [c3] [c4]     (the box)
                                      mutex + condition_variable            (the bell)

   thread A:  auto lease = pool.acquire();   -> takes c1, box: [c2] [c3] [c4]
   thread B:  auto lease = pool.acquire();   -> takes c2, box: [c3] [c4]
   thread C:  ...                            -> takes c3
   thread D:  ...                            -> takes c4, box: []
   thread E:  auto lease = pool.acquire();   -> waits on the condition variable
   thread A:  } // lease destroyed           -> c1 back in the box, notify_one
   thread E:                                 -> wakes, takes c1
```

Notice that thread E did nothing but wait, and that A's closing brace is what woke it. No
thread ever opened a connection after start-up.

## 5. The code, built step by step

A Postgres to talk to, and the library: `libpqxx-dev` on Debian and Ubuntu, `libpqxx` on
Homebrew and vcpkg.

```bash
docker run --name pg -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=app -p 5432:5432 -d postgres:16
```

The lease.

```cpp
class Pool;

class Lease {
public:
    Lease(Pool& pool, std::unique_ptr<pqxx::connection> conn) : pool_(pool), conn_(std::move(conn)) {}
    ~Lease();
    Lease(const Lease&) = delete;
    Lease& operator=(const Lease&) = delete;
    pqxx::connection& operator*() { return *conn_; }
private:
    Pool& pool_;
    std::unique_ptr<pqxx::connection> conn_;
};
```

A lease owns one connection for its lifetime, cannot be copied, and its destructor, defined
after `Pool` below, gives the connection back. `operator*` lets you write `*lease` where a
`pqxx::connection&` is wanted.

The pool.

```cpp
class Pool {
public:
    Pool(const std::string& dsn, std::size_t size) {
        for (std::size_t i = 0; i < size; ++i) {
            free_.push_back(std::make_unique<pqxx::connection>(dsn));
        }
    }

    Lease acquire(std::chrono::milliseconds timeout = std::chrono::seconds(5)) {
        std::unique_lock<std::mutex> lock(mutex_);
        if (!bell_.wait_for(lock, timeout, [this] { return !free_.empty(); })) {
            throw std::runtime_error("pool: no connection free within timeout");
        }
        auto conn = std::move(free_.back());
        free_.pop_back();
        return Lease(*this, std::move(conn));
    }

    void give_back(std::unique_ptr<pqxx::connection> conn) {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            free_.push_back(std::move(conn));
        }
        bell_.notify_one();
    }

private:
    std::mutex mutex_;
    std::condition_variable bell_;
    std::vector<std::unique_ptr<pqxx::connection>> free_;
};

Lease::~Lease() {
    if (conn_) pool_.give_back(std::move(conn_));
}
```

The constructor opens every connection up front; a `Pool` that exists is ready. `acquire` is
the day 32 pattern: `unique_lock`, `wait_for` with a predicate, which handles spurious wake-ups
and the timeout in one call, then take from the vector. `give_back` pushes under the lock and
rings the bell after releasing it. The lease destructor is the only caller of `give_back`,
which is why a connection cannot be leaked by forgetting: there is nothing to forget.

Using a lease.

```cpp
int add_user(Pool& pool, const std::string& name, const std::string& city) {
    auto lease = pool.acquire();
    pqxx::work tx(*lease);
    const pqxx::row row = tx.exec_params1("INSERT INTO users (name, city) VALUES ($1, $2) RETURNING id", name, city);
    tx.commit();
    return row["id"].as<int>();
}
```

Take a disc, open a transaction on that connection, run one statement, commit, and the lease
returns the connection at the closing brace. `exec_params1` returns the single row, and
`as<int>()` converts the column.

Reading, with a prepared statement.

```cpp
std::optional<User> find_by_name(Pool& pool, const std::string& name) {
    auto lease = pool.acquire();
    pqxx::work tx(*lease);
    const pqxx::result rows = tx.exec_prepared("find_by_name", name);
    if (rows.empty()) return std::nullopt;
    const pqxx::row r = rows[0];
    return User{r["id"].as<int>(), r["name"].as<std::string>(), r["city"].as<std::string>(), r["balance"].as<int>()};
}
```

`exec_prepared` runs a statement prepared earlier by name. The pool's constructor is where
that happens, `conn->prepare("find_by_name", "SELECT id, name, city, balance FROM users WHERE name = $1")`
on each connection, so every disc knows the statement. A read-only transaction still needs the
`work` object; libpqxx runs every statement inside one.

The transfer.

```cpp
void transfer(Pool& pool, int from, int to, int amount) {
    auto lease = pool.acquire();
    pqxx::work tx(*lease);
    tx.exec_params("UPDATE users SET balance = balance - $1 WHERE id = $2", amount, from);
    const int balance = tx.exec_params1("SELECT balance FROM users WHERE id = $1", from)["balance"].as<int>();
    if (balance < 0) throw std::runtime_error("insufficient balance");
    tx.exec_params("UPDATE users SET balance = balance + $1 WHERE id = $2", amount, to);
    tx.commit();
}
```

One lease, one `work`, two updates. The throw leaves through `tx`'s destructor, which rolls
back, and then through `lease`'s, which returns the connection. Two destructors, in the right
order, with no code at the throw site.

Seeing the pool wait.

```cpp
void hold(Pool& pool, double seconds) {
    auto lease = pool.acquire();
    pqxx::work tx(*lease);
    tx.exec_params("SELECT pg_sleep($1)", seconds);
    tx.commit();
}
```

`main` runs five of these on five threads with a pool of four and times them.

Build and run:

```bash
g++ -Wall -Wextra -std=c++20 main.cpp -lpqxx -lpq -o app
DATABASE_URL=postgresql://postgres:secret@localhost:5432/app ./app
```

```text
inserted ids: 1 2
found: Meera Pune 100
transfer refused: insufficient balance
five 1-second holds on a pool of 4 took 2.0s
```

Four holds ran together and the fifth waited by the box. Give `acquire` a timeout shorter than
a second on the fifth and it throws `pool: no connection free within timeout` instead of
waiting, which is the token with a time on it.

Here is the whole program in one piece, `main.cpp`:

```cpp
#include <pqxx/pqxx>

#include <chrono>
#include <condition_variable>
#include <cstdlib>
#include <iostream>
#include <memory>
#include <mutex>
#include <optional>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

class Pool;

class Lease {
public:
    Lease(Pool& pool, std::unique_ptr<pqxx::connection> conn) : pool_(pool), conn_(std::move(conn)) {}
    ~Lease();
    Lease(const Lease&) = delete;
    Lease& operator=(const Lease&) = delete;
    Lease(Lease&&) = default;
    pqxx::connection& operator*() { return *conn_; }
private:
    Pool& pool_;
    std::unique_ptr<pqxx::connection> conn_;
};

class Pool {
public:
    Pool(const std::string& dsn, std::size_t size) {
        for (std::size_t i = 0; i < size; ++i) {
            auto conn = std::make_unique<pqxx::connection>(dsn);
            conn->prepare("find_by_name", "SELECT id, name, city, balance FROM users WHERE name = $1");
            free_.push_back(std::move(conn));
        }
    }

    Lease acquire(std::chrono::milliseconds timeout = std::chrono::seconds(5)) {
        std::unique_lock<std::mutex> lock(mutex_);
        if (!bell_.wait_for(lock, timeout, [this] { return !free_.empty(); })) {
            throw std::runtime_error("pool: no connection free within timeout");
        }
        auto conn = std::move(free_.back());
        free_.pop_back();
        return Lease(*this, std::move(conn));
    }

    void give_back(std::unique_ptr<pqxx::connection> conn) {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            free_.push_back(std::move(conn));
        }
        bell_.notify_one();
    }

private:
    std::mutex mutex_;
    std::condition_variable bell_;
    std::vector<std::unique_ptr<pqxx::connection>> free_;
};

Lease::~Lease() {
    if (conn_) pool_.give_back(std::move(conn_));
}

struct User {
    int id;
    std::string name;
    std::string city;
    int balance;
};

void create_schema(Pool& pool) {
    auto lease = pool.acquire();
    pqxx::work tx(*lease);
    tx.exec("CREATE TABLE IF NOT EXISTS users ("
            "id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE, "
            "city TEXT NOT NULL, balance INTEGER NOT NULL DEFAULT 0)");
    tx.commit();
}

int add_user(Pool& pool, const std::string& name, const std::string& city) {
    auto lease = pool.acquire();
    pqxx::work tx(*lease);
    const pqxx::row row = tx.exec_params1("INSERT INTO users (name, city) VALUES ($1, $2) RETURNING id", name, city);
    tx.commit();
    return row["id"].as<int>();
}

std::optional<User> find_by_name(Pool& pool, const std::string& name) {
    auto lease = pool.acquire();
    pqxx::work tx(*lease);
    const pqxx::result rows = tx.exec_prepared("find_by_name", name);
    if (rows.empty()) return std::nullopt;
    const pqxx::row r = rows[0];
    return User{r["id"].as<int>(), r["name"].as<std::string>(), r["city"].as<std::string>(), r["balance"].as<int>()};
}

void transfer(Pool& pool, int from, int to, int amount) {
    auto lease = pool.acquire();
    pqxx::work tx(*lease);
    tx.exec_params("UPDATE users SET balance = balance - $1 WHERE id = $2", amount, from);
    const int balance = tx.exec_params1("SELECT balance FROM users WHERE id = $1", from)["balance"].as<int>();
    if (balance < 0) throw std::runtime_error("insufficient balance");
    tx.exec_params("UPDATE users SET balance = balance + $1 WHERE id = $2", amount, to);
    tx.commit();
}

void hold(Pool& pool, double seconds) {
    auto lease = pool.acquire();
    pqxx::work tx(*lease);
    tx.exec_params("SELECT pg_sleep($1)", seconds);
    tx.commit();
}

int main() {
    const char* dsn = std::getenv("DATABASE_URL");
    if (dsn == nullptr) {
        std::cerr << "DATABASE_URL is not set\n";
        return 1;
    }
    try {
        // The table must exist before the pool prepares its statement against it.
        {
            Pool bootstrap(dsn, 1);
            create_schema(bootstrap);
        }
        Pool pool(dsn, 4);

        const int meera = add_user(pool, "Meera", "Pune");
        const int arjun = add_user(pool, "Arjun", "Delhi");
        {
            auto lease = pool.acquire();
            pqxx::work tx(*lease);
            tx.exec_params("UPDATE users SET balance = 100 WHERE id = $1", meera);
            tx.commit();
        }
        std::cout << "inserted ids: " << meera << ' ' << arjun << '\n';
        if (auto u = find_by_name(pool, "Meera")) {
            std::cout << "found: " << u->name << ' ' << u->city << ' ' << u->balance << '\n';
        }

        transfer(pool, meera, arjun, 30);
        try {
            transfer(pool, meera, arjun, 500);
        } catch (const std::runtime_error& e) {
            std::cout << "transfer refused: " << e.what() << '\n';
        }

        const auto start = std::chrono::steady_clock::now();
        std::vector<std::jthread> threads;
        for (int i = 0; i < 5; ++i) threads.emplace_back([&pool] { hold(pool, 1.0); });
        threads.clear();
        const auto elapsed = std::chrono::steady_clock::now() - start;
        std::cout << "five 1-second holds on a pool of 4 took "
                  << std::chrono::duration<double>(elapsed).count() << "s\n";
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
    return 0;
}
```

Wait: `prepare` against a table that does not exist yet fails, which is why `main` creates the
schema through a one-connection bootstrap pool before opening the real one. In a service the
schema is a migration that ran before the process started, which is
[day 55](../day-055-quickselect/README.md).

## 6. How the other two languages do it

**Python**

```python
pool = ConnectionPool(DSN, min_size=2, max_size=4, timeout=5)
with pool.connection() as conn:
    conn.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, from_id))
```

The pool is a library; the `with` is the lease. Same size, same timeout, same rule about the
borrow being as short as the transaction.

**Go**

```go
tx, err := pool.Begin(ctx)
defer tx.Rollback(ctx)
_, err = tx.Exec(ctx, "UPDATE users SET balance = balance - $1 WHERE id = $2", amount, from)
err = tx.Commit(ctx)
```

`pgxpool` is the pool; `Begin` is the lease and `Commit` or the deferred `Rollback` returns it.
The context bounds the wait and can cancel the running query.

**The difference that matters:** in C++ you can read the pool, all forty lines of it, and every
other language's pool is doing the same thing behind a nicer name. The mutex is why two threads
cannot take the same connection; the condition variable is why a waiting thread sleeps instead
of spinning; the lease destructor is why a leak is impossible rather than unlikely. When a
Python or Go pool "times out", it is `wait_for` returning `false`.

## 7. The traps

**The near-miss: a connection per call.**

```cpp
int add_user(const std::string& dsn, const std::string& name, const std::string& city) {
    pqxx::connection conn(dsn);        // handshake, TLS, auth, fork, every call
    pqxx::work tx(conn);
    ...
```

Correct, and the predecessor's branch. Under load Postgres refuses:

```text
connection to server at "127.0.0.1", port 5432 failed: FATAL:  sorry, too many clients already
```

**A lease in the pocket.**

```cpp
auto lease = pool.acquire();
auto user = find_user(*lease, id);
send_email(user);                  // two seconds, disc in pocket
```

With four such calls in flight, the fifth `acquire` waits, and after the timeout:

```text
pool: no connection free within timeout
```

Take the lease, run the transaction, let the lease die, then send the email.

**`give_back` under the lock while notifying.** The lesson notifies after the `lock_guard`'s
scope closes. Notifying while holding the lock is not wrong, but the woken thread immediately
blocks on the mutex you still hold, which is a wasted context switch on every return.

**`wait` without the predicate.**

```cpp
bell_.wait(lock);                  // no predicate
auto conn = std::move(free_.back());
```

Condition variables can wake spuriously, and two waiters can both wake on one `notify_one`
under some implementations. The second one pops from an empty vector, which is undefined
behaviour and in practice a crash. The predicate form re-checks; it is the only form to use.

**Forgetting `commit()`.**

```cpp
pqxx::work tx(*lease);
tx.exec_params("INSERT INTO users ...", name, city);
// no tx.commit()
```

No error. The transaction rolls back when `tx` is destroyed and the row was never inserted.
libpqxx does this on purpose, so that an exception cannot half-commit; the cost is that the
happy path must say `commit()` out loud.

**`?` from SQLite.**

```text
ERROR:  syntax error at or near "?"
LINE 1: SELECT id FROM users WHERE name = ?
                                          ^
```

Postgres wants `$1`. libpqxx throws `pqxx::syntax_error` with that text.

**Running it twice.**

```text
ERROR:  duplicate key value violates unique constraint "users_name_key"
DETAIL:  Key (name)=(Meera) already exists.
```

That is `pqxx::unique_violation`; catch it by type for the day 50 409.

**Nobody home.**

```text
connection to server at "127.0.0.1", port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
```

`pqxx::broken_connection`, thrown from the `pqxx::connection` constructor, which in the lesson
means from the pool's constructor at start-up, which is where you want it.

## 8. Say it out loud

**How it gets asked**

- Why do you need a connection pool?
- How would you implement one?
- What stops two threads getting the same connection?
- What happens if a caller holds a connection and forgets to return it?

**The ninety-second script**

A connection is a TCP handshake, a TLS exchange, an authentication round trip and a forked
process on the Postgres side, so tens of milliseconds and megabytes each, and Postgres caps them
at `max_connections` across every client. Opening one per request pays that on every call and,
under load, hits the cap. A pool opens a fixed set once and lends them out. In C++ I write it:
a vector of connections opened in the constructor, a mutex around the vector so two threads
cannot take the same one, a condition variable so a thread that finds the vector empty sleeps
until a return wakes it, and `wait_for` with a predicate so the wait has a timeout and spurious
wake-ups are re-checked. `acquire` returns a lease, an object that owns the connection and whose
destructor puts it back and notifies. The lease is what makes a leak impossible: the connection
returns when the lease dies, on every path out, including an exception. The one thing that
breaks it is holding the lease across something slow that is not the transaction. Size is a
small multiple of the database's cores across every process, not a large number.

**The follow-ups**

- **Why a condition variable and not a sleep loop?** *A loop that sleeps ten milliseconds and
  retries burns CPU and adds up to ten milliseconds of latency per wait. `wait_for` sleeps
  until notified and wakes at once when a connection returns.*
- **What if a connection breaks while in the pool?** *`pqxx::connection::is_open()` on
  acquire, and reconnect if it is not; or catch `pqxx::broken_connection` in the caller and
  retry once with a fresh lease. The lesson's pool does not, and the practice sheet asks for it.*
- **How do prepared statements interact with the pool?** *They belong to a connection, so the
  pool prepares them on each connection at start-up. Preparing inside a request works too, but
  then every connection re-prepares the first time it sees each statement.*

**A model answer**

"A connection is a handshake, TLS, auth and a server process, capped by `max_connections`, so
one per request is both slow and self-limiting. A pool: `std::vector` of `pqxx::connection`
opened in the constructor, `std::mutex`, `std::condition_variable`, `acquire` does `wait_for`
with a predicate and pops one, returns a `Lease` whose destructor pushes it back and
`notify_one`s. `pqxx::work` on the leased connection for the transaction, `commit()` out loud
or it rolls back. Never hold the lease across anything but the transaction."

## 9. Recall card

- A connection is a handshake, TLS, auth and a forked server process, capped by `max_connections`; the pool opens `size` of them once.
- Pool = `std::vector<std::unique_ptr<pqxx::connection>>` + `std::mutex` + `std::condition_variable`; `acquire` is `wait_for(lock, timeout, predicate)` then pop.
- `Lease` owns the connection; its destructor gives it back and notifies. No lease across anything slower than the transaction.
- `pqxx::work tx(conn)`, `tx.exec_params(sql, args...)` with `$1`, `exec_params1` for one row, `row["id"].as<int>()`, and `tx.commit()` or it rolls back.
- `conn.prepare(name, sql)` per connection at start-up; `tx.exec_prepared(name, args...)`. Errors are `pqxx::unique_violation`, `pqxx::broken_connection`, under `std::exception`.
