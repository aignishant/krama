---
day: 55
track: lang-cpp
title: "Raw SQL with a migration runner you write yourself"
theme: "Databases III: migrations and ORMs"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 055 · C++ — Raw SQL with a migration runner you write yourself

**Today's theme:** Databases III: migrations and ORMs

**After today you can:** You can evolve a schema safely in each language and say what an ORM buys and costs.

**The interviewer asks it as:** *ORM or raw SQL? Defend your answer.*

---

## 1. What this is, and why it matters

C++ has no mainstream ORM, so the answer to "ORM or raw SQL" is decided for you: raw SQL, through
libpqxx from [day 54](../day-054-quicksort/README.md). What you do not get for free is
migrations, so today you write the runner: a folder of numbered `.sql` files, a small table that
records which have run, and a loop that applies the ones that have not, inside a transaction, in
order. It is thirty lines, and writing it once shows you exactly what Alembic and golang-migrate
do behind their commands.

At work, a C++ service's data layer is hand-written SQL and a migration runner very like today's,
or an in-house wrapper over one. In interviews, "ORM or raw SQL, defend your answer" from a C++
candidate is a chance to say that the language made the choice, and then to show that the part
people fear about raw SQL, evolving the schema safely, is a small, understandable amount of code
rather than magic.

## 2. The story

Farida's bakery has one binder of recipes, and every baker works from it. The binder is not
edited in place. When the almond cake needs less sugar, nobody reaches in and scribbles over the
old amount, because then a baker who is mid-bake would see a number change under their hands, and
nobody could say what the recipe was last Tuesday.

Instead there is a pad of change slips by the binder. Each slip is numbered, in order, and says
what to change. "Slip 14: almond cake, sugar from 200 grams to 160." A slip is applied to the
binder once, and then it is filed. A new bakery that opens across town gets a fresh empty binder
and the whole stack of slips, applied in order, one to fourteen, and ends up with exactly the
binder Farida has.

At Farida's branch there is no printed pad; she made the system herself, out of a cheap notebook
and a spike for filed slips. The notebook has one line per slip applied: "slip 1, done", "slip 2,
done". When a new stack of slips arrives, whoever is setting up reads the notebook to see the
last line, then applies every slip after that number, adds a line to the notebook for each, and
spikes the slip. If the electricity goes out halfway through applying a slip, the rule is that a
half-applied slip does not count: the notebook line goes in only when the whole slip is done, so
next time they start that slip again from the top rather than from the middle.

Her cousin, who keeps recipe cards instead of a cross-referenced binder, has the same notebook and
the same spike. The recipes themselves are more work to write out longhand on cards. But the
change-slip system, the notebook, the numbers, the "half does not count" rule, is identical,
because that part was never about how the recipes are stored.

## 3. The idea in plain English

The recipes on cards are your **raw SQL**: statements written by hand and run through libpqxx.
There is no object graph, no lazy loading, so the ORM's N+1 cannot happen by accident; the price
is that every query is a string you write and check. `tx.exec_params("SELECT ... WHERE name =
$1", name)` is the whole of it, and it is [day 54](../day-054-quicksort/README.md).

The change slips are **migrations**: numbered `.sql` files in a folder, `001_create.sql`,
`002_add_age.sql`. Each is a slip. They are applied in order and never edited once applied.

The notebook is the **version table**, `schema_migrations`, a table with one row per applied
migration's number. The **runner** reads the largest number in it, lists the files with a larger
number, and applies each: run the file's SQL, insert its number into the table, all inside one
transaction, so "half does not count" is the transaction from
[day 53](../day-053-merge-sort/README.md). If applying a file fails or the power goes out, the
transaction rolls back, the number is not recorded, and the next run starts that file from the
top.

"Which slips has this kitchen applied" is a `SELECT max(version) FROM schema_migrations`. Running
the runner on a fresh database applies every file, one upward; running it on an up-to-date one
applies nothing.

The ORM's convenience, `user.orders`, is the thing you do without. Fetching a user's orders is a
query you write; batching many users' orders is an `= ANY($1)` query you write. The buy of raw
SQL is total visibility, every query in front of you; the cost is that you write and maintain all
of it, including the runner.

## 4. The picture

```text
  migrations/ (the slips)         schema_migrations (the notebook)      database

  001_create.sql            row: version = 1                      ->  users, orders
  002_add_age.sql           row: version = 2                      ->  users.age added

  runner:
    applied = SELECT COALESCE(max(version), 0) FROM schema_migrations
    for each file with number > applied, in order:
        BEGIN
        run the file's SQL
        INSERT version                                <- both, or neither
        COMMIT
```

Notice the `BEGIN`/`COMMIT` around each file. That single transaction is what makes a
half-applied migration impossible: the schema change and the recorded version commit together or
not at all.

## 5. The code, built step by step

libpqxx from day 54, and a `<filesystem>` walk from
[day 44](../day-044-first-and-last-occurrence/README.md) to find the files.

The migration files, by hand. `migrations/001_create.sql`:

```sql
CREATE TABLE users (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL
);
CREATE TABLE orders (
    id      SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    amount  INTEGER NOT NULL
);
```

`migrations/002_add_age.sql`:

```sql
ALTER TABLE users ADD COLUMN age INTEGER;
```

The runner. First, make sure the notebook exists.

```cpp
void ensure_version_table(pqxx::connection& conn) {
    pqxx::work tx(conn);
    tx.exec("CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY)");
    tx.commit();
}
```

Read the last applied number.

```cpp
int current_version(pqxx::connection& conn) {
    pqxx::work tx(conn);
    return tx.query_value<int>("SELECT COALESCE(max(version), 0) FROM schema_migrations");
}
```

`query_value<int>` returns a single scalar; `COALESCE(max(version), 0)` gives 0 on an empty
table, so a fresh database is "at version 0".

List the files in order, with their numbers.

```cpp
std::map<int, std::filesystem::path> list_migrations(const std::filesystem::path& dir) {
    std::map<int, std::filesystem::path> files;   // std::map keeps them sorted by key
    for (const auto& entry : std::filesystem::directory_iterator(dir)) {
        if (entry.path().extension() != ".sql") continue;
        const std::string name = entry.path().filename().string();
        const int number = std::stoi(name.substr(0, name.find('_')));
        files[number] = entry.path();
    }
    return files;
}
```

`std::map` from [day 7](../day-007-space-complexity/README.md) is sorted by key, so iterating it
gives the files in numeric order. The number is the digits before the first underscore.

Apply the pending ones, each in its own transaction.

```cpp
void migrate(pqxx::connection& conn, const std::filesystem::path& dir) {
    ensure_version_table(conn);
    const int applied = current_version(conn);
    for (const auto& [number, path] : list_migrations(dir)) {
        if (number <= applied) continue;
        std::ifstream file(path);
        const std::string sql((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
        pqxx::work tx(conn);
        tx.exec(sql);
        tx.exec_params("INSERT INTO schema_migrations (version) VALUES ($1)", number);
        tx.commit();
        std::cout << "applied " << path.filename().string() << '\n';
    }
}
```

The whole idea is in the last five lines: read the file, run its SQL, record its number, commit,
all in one `pqxx::work`. If `tx.exec(sql)` throws, the `work` is destroyed without `commit`, the
schema change and the version insert both roll back, and the next run retries this file. "Half
does not count."

The data code, raw SQL, no ORM.

```cpp
int add_user(Pool& pool, const std::string& name, const std::string& city, std::optional<int> age) {
    auto lease = pool.acquire();
    pqxx::work tx(*lease);
    pqxx::row row = age
        ? tx.exec_params1("INSERT INTO users (name, city, age) VALUES ($1, $2, $3) RETURNING id", name, city, *age)
        : tx.exec_params1("INSERT INTO users (name, city) VALUES ($1, $2) RETURNING id", name, city);
    tx.commit();
    return row["id"].as<int>();
}
```

Totals without an N+1: fetch every order in one query and group in C++.

```cpp
std::map<int, int> totals_by_user(Pool& pool) {
    auto lease = pool.acquire();
    pqxx::work tx(*lease);
    std::map<int, int> totals;
    for (const auto& row : tx.exec("SELECT user_id, amount FROM orders")) {
        totals[row["user_id"].as<int>()] += row["amount"].as<int>();
    }
    return totals;
}
```

One `SELECT` for all orders, summed in a map. There is no `user.orders` to trip over, because
there is no ORM; the query is right there, and it is one query.

Run the migrations, then the program:

```bash
g++ -Wall -Wextra -std=c++20 main.cpp -lpqxx -lpq -o app
DATABASE_URL=postgresql://postgres:secret@localhost:5432/app ./app
```

```text
applied 001_create.sql
applied 002_add_age.sql
created: 1 2
totals: 1 -> 370, 2 -> 999
```

Run it a second time and the migrations say nothing, because `current_version` is now 2 and no
file has a higher number:

```text
created: 3 4
totals: 1 -> 370, 2 -> 999, 3 -> 370, 4 -> 999
```

Here is the runner in one piece, `migrate.hpp` (the data functions above sit alongside it and
`main` calls `migrate(conn, "migrations")` before using the pool):

```cpp
#pragma once
#include <pqxx/pqxx>

#include <filesystem>
#include <fstream>
#include <iostream>
#include <iterator>
#include <map>
#include <string>

inline void ensure_version_table(pqxx::connection& conn) {
    pqxx::work tx(conn);
    tx.exec("CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY)");
    tx.commit();
}

inline int current_version(pqxx::connection& conn) {
    pqxx::work tx(conn);
    return tx.query_value<int>("SELECT COALESCE(max(version), 0) FROM schema_migrations");
}

inline std::map<int, std::filesystem::path> list_migrations(const std::filesystem::path& dir) {
    std::map<int, std::filesystem::path> files;
    for (const auto& entry : std::filesystem::directory_iterator(dir)) {
        if (entry.path().extension() != ".sql") continue;
        const std::string name = entry.path().filename().string();
        files[std::stoi(name.substr(0, name.find('_')))] = entry.path();
    }
    return files;
}

inline void migrate(pqxx::connection& conn, const std::filesystem::path& dir) {
    ensure_version_table(conn);
    const int applied = current_version(conn);
    for (const auto& [number, path] : list_migrations(dir)) {
        if (number <= applied) continue;
        std::ifstream file(path);
        const std::string sql((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
        pqxx::work tx(conn);
        tx.exec(sql);
        tx.exec_params("INSERT INTO schema_migrations (version) VALUES ($1)", number);
        tx.commit();
        std::cout << "applied " << path.filename().string() << '\n';
    }
}
```

## 6. How the other two languages do it

**Python**

```python
class User(Base):
    orders: Mapped[list["Order"]] = relationship(back_populates="user")

for u in session.scalars(select(User)):
    total = sum(o.amount for o in u.orders)   # lazy: one query per user
```

The ORM writes the SQL and gives you `u.orders`, convenient and the home of the N+1. Alembic is
the migration runner, so you do not write one.

**Go**

```go
// query.sql, checked in:  -- name: OrdersForUsers :many
//   SELECT * FROM orders WHERE user_id = ANY($1::int[]);
orders, err := queries.OrdersForUsers(ctx, ids)   // generated, one query
```

sqlc generates typed functions from SQL you write; golang-migrate is the runner. No object graph,
so no accidental N+1, and the migration runner is a tool, not code you wrote.

**The difference that matters:** C++ is the only one where you write the migration runner
yourself, and doing so shows that Alembic and golang-migrate are not magic: a version table, a
sorted list of files, a loop, and a transaction per file. The N+1 story is the same as sqlc's,
one query you write rather than one the ORM hides, and the migration story is the same as
everyone's, numbered files and a recorded version, except that here the twenty lines that record
the version are on the screen in front of you.

## 7. The traps

**The near-miss: the runner without a transaction.**

```cpp
tx.exec(sql);
tx.commit();                                  // schema change committed
// power fails here
tx2.exec_params("INSERT INTO schema_migrations ...", number);   // never runs
```

Two separate transactions: the schema change commits, then the version insert is a separate
step. If anything happens between them, the change is applied but not recorded, and the next run
applies it again, `ALTER TABLE ... ADD COLUMN age` a second time:

```text
ERROR:  column "age" of relation "users" already exists
```

The schema change and the version insert must be in one `pqxx::work`, so they commit together.

**Editing an applied migration.** Change `002_add_age.sql` after production ran it: fresh
databases get the new content at version 2, production has the old at version 2, and they have
diverged under the same number. Append `003` to correct it; never edit an applied file.

**Files that do not sort numerically.** `10_add_index.sql` next to `2_add_age.sql`, compared as
strings, puts `10` before `2`. That is why the number is parsed with `std::stoi` and the map is
keyed by `int`, and why real tools zero-pad: `0002`, `0010`. Sorting filenames as text is the
classic migration-order bug.

**A SQL error mid-file.** A migration with two statements where the second fails:

```text
ERROR:  syntax error at or near "TABEL"
LINE 1: CREATE TABEL orders ...
```

Because the whole file runs in one `pqxx::work`, the first statement rolls back too, and the
version is not recorded. Fix the file and re-run; nothing was half-applied.

**Re-running on a partly-migrated database by hand.** Someone runs `001_create.sql` manually,
then the runner: `current_version` is still 0, so the runner runs `001` again and
`CREATE TABLE users` fails with "already exists". The lesson: apply migrations only through the
runner, so the version table always reflects reality.

**No N+1 here, but no lazy convenience either.** Forgetting that there is no `user.orders` and
writing a loop that queries per user is possible, exactly as in sqlc, and just as visible:

```cpp
for (const auto& user : users) {
    auto orders = tx.exec_params("SELECT amount FROM orders WHERE user_id = $1", user.id);  // per user
}
```

One `SELECT ... WHERE user_id = ANY($1)` instead, and the difference is in your code where you
can see it.

## 8. Say it out loud

**How it gets asked**

- ORM or raw SQL? Defend your answer.
- How does a migration tool actually work?
- What makes a half-applied migration impossible?
- Does raw SQL mean you get N+1, or avoid it?

**The ninety-second script**

C++ has no mainstream ORM, so it is raw SQL through libpqxx, and the trade is total visibility
for more code: there is no object graph and no lazy loading, so the N+1 cannot happen by
accident, but every query is a string I write and check. The part people fear, evolving the
schema, is a runner I write in about thirty lines, and writing it shows that Alembic and
golang-migrate are the same thing: a `schema_migrations` table recording the last applied
number, a folder of numbered `.sql` files, and a loop that reads the version, lists the files
with a higher number in order, and for each one runs its SQL and inserts its number in a single
transaction. That transaction is what makes a half-applied migration impossible: the schema
change and the recorded version commit together or roll back together, so a failure mid-migration
leaves the database exactly where it was and the next run retries that file from the top.
Migrations are append-only and numbers are zero-padded so they sort correctly. So my answer is:
in C++ raw SQL is the only real option, and it is fine, because the two things people worry
about, injection and migrations, are a parameter and a small runner.

**The follow-ups**

- **Why one transaction per file and not one for all of them?** *Some DDL, like adding an index
  concurrently in Postgres, cannot run inside a transaction, and one giant transaction holds
  locks for the whole run. Per file is the common choice: each migration is atomic, and a
  failure stops the run at a known version.*
- **How do you handle down migrations?** *A second file per number, or a `-- +down` section the
  runner splits on. In practice production rarely runs down; a mistake is a new forward
  migration, because down for "add a column" drops data.*
- **Is hand-written SQL not more injectable than an ORM?** *No: the injection defence is
  parameters, `$1`, which libpqxx gives me exactly as the ORM does. The migration SQL has no user
  input in it at all; it is DDL I wrote. The query SQL is parameterised. Neither pastes user
  input into text.*

**A model answer**

"In C++ it is raw SQL through libpqxx, because there is no mainstream ORM. That means no
accidental N+1, since there is no lazy `user.orders`, at the cost of writing every query.
Migrations I write a runner for: a `schema_migrations` version table, numbered zero-padded `.sql`
files, and a loop that applies each pending file's SQL and records its number in one transaction,
so half-applied is impossible. It is thirty lines, and it is exactly what Alembic and
golang-migrate do. Append-only, and down migrations are for development because they can drop
data."

## 9. Recall card

- C++ has no mainstream ORM: raw SQL through libpqxx. No lazy loading, so no accidental N+1; batch with `WHERE id = ANY($1)`, written on purpose.
- Migration runner: a `schema_migrations` version table, numbered `.sql` files, apply each pending one's SQL and its version number in one `pqxx::work`.
- The single transaction per file is what makes half-applied impossible: schema change and version commit together or roll back together.
- Zero-pad the numbers so they sort as integers; append-only, never edit an applied file; apply only through the runner.
- The runner is what Alembic and golang-migrate do; writing it shows the tools are a version table, a sorted file list, a loop, and a transaction.
