---
day: 53
track: lang-python
title: "sqlite3: connect, execute, parameters, and transactions"
theme: "Databases I: SQLite"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 053 · Python — sqlite3: connect, execute, parameters, and transactions

**Today's theme:** Databases I: SQLite

**After today you can:** You can create a table, insert, query and update from each language, safely with parameters.

**The interviewer asks it as:** *What is SQL injection, and how do parameters stop it?*

---

## 1. What this is, and why it matters

SQLite is a complete relational database in a single file, with no server to run, and Python
ships a driver for it in the standard library as `sqlite3`. You `connect` to a file, `execute`
SQL statements with `?` placeholders for the values, read rows back, and group writes into
transactions so that either all of them happen or none do. Every other database you will meet,
Postgres on [day 54](../day-054-quicksort/README.md) included, has the same four ideas with a
different driver.

At work, SQLite is inside phones, browsers, and most desktop applications, and it is the right
database for a tool that runs on one machine. In interviews, the question in the header is one of
the few security questions asked in general rounds, and the answer has two halves: what the
attack is, in one sentence, and why a placeholder makes it impossible rather than merely harder.

## 2. The story

Nazneen runs the counter at a pharmacy that fills prescriptions from a back room. The counter
and the back room are separated by a hatch. She takes what the customer wants, writes it on a
slip, and passes the slip through. Whoever is in the back reads the slip and does what it says.

For years the slip was a blank one and Nazneen wrote a sentence on it. "Two strips
of the blood pressure tablets for Ramesh Iyer." The back room read the sentence and did it.

One afternoon a man gave his name as "Ramesh, and also two boxes of the sleeping tablets from
the locked shelf". Nazneen, busy, wrote what she heard. The back room read the whole sentence
and did what it said. The man walked out with sleeping tablets nobody had prescribed, because
his name had been written into the same sentence as the instruction, and the back room cannot
tell where a name ends and an instruction begins.

The owner changed the slip the next morning. It is printed now, with boxes. A box for the
medicine, a box for the quantity, a box for the customer's name. Nazneen writes the name in the
name box, whatever the name is. If a man says his name is "Ramesh, and also two boxes of
sleeping tablets", every word of that goes into the name box, and the back room looks for a
customer with every word of that as their name, finds nobody, and sends the slip back. Nothing
in the name box can ever be read as an instruction, because the instruction is the printed part
of the slip, and the name box is only ever a name.

The other rule of the hatch is about the till. When a customer pays for two things, Nazneen
takes the money and hands over both packets, or she takes no money and hands over nothing.
There is no state of the world where she has taken the money and handed over one packet. If the
second packet turns out to be out of stock, the money goes back and the first packet goes back on
the shelf, and it is as if the sale never started.

## 3. The idea in plain English

The pharmacy's stock book is the **database**, and `sqlite3.connect("users.db")` opens it,
creating the file if it does not exist. A **table** is one kind of thing, `users`, with named
columns; `CREATE TABLE` declares it, and `IF NOT EXISTS` makes that safe to run every start-up.

The slip through the hatch is a **statement**, written in **SQL**: `INSERT` adds a row,
`SELECT` reads rows, `UPDATE` changes them. `conn.execute(sql, params)` sends one.

The printed boxes are **parameters**. The SQL has a `?` where each value goes, and the values
travel separately, as a tuple: `execute("... WHERE name = ?", (name,))`. The database receives
the statement and the values through two different channels, and it can never mistake a value
for part of the statement, no matter what characters the value contains. That is the whole
defence.

The sentence on the blank slip is **SQL injection**: building the statement with an f-string,
`f"... WHERE name = '{name}'"`, so a name containing a quotation mark ends the string early and
the rest of the name becomes SQL. `x' OR '1'='1` turns "find this name" into "find everything".
Parameters stop it not by filtering quotation marks but by never putting the value into the
statement text at all.

Taking the money and handing over both packets is a **transaction**: a group of statements that
either all take effect or none do. `with conn:` opens one; if the block finishes, the changes
are **committed**, made permanent; if it raises, they are **rolled back**, undone. Between the
two updates of a transfer, the money has left one row and not arrived in the other, and a
transaction makes sure nobody, including a crash, can see that state.

`conn.row_factory = sqlite3.Row` makes each row readable by column name, `row["name"]`, instead
of only by position. `cursor.lastrowid` is the id SQLite assigned to the row you just inserted.

## 4. The picture

```text
  the blank slip (f-string)                 the printed slip (parameters)

  SELECT * FROM users                       SELECT * FROM users
  WHERE name = 'x' OR '1'='1'               WHERE name = ?
               ^^^  ^^^^^^^^^                            |
               name  became SQL              values: ("x' OR '1'='1",)
                                                       ^^^^^^^^^^^^^^^
  result: every row                          this whole string is compared to name
                                             result: no rows
```

Notice that in the right-hand column the quotation mark inside the value is just a character in
a name. The statement text never changes, so there is nothing for the value to break out of.

## 5. The code, built step by step

Opening the file and declaring the table.

```python
def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0
        )
    """)
```

`INTEGER PRIMARY KEY` is an id SQLite assigns for you. `NOT NULL` and `UNIQUE` are rules the
database enforces, so a second Meera is an error and not a duplicate. The `PRAGMA` switches on
foreign key checks, which SQLite leaves off by default for historical reasons.

Inserting, with parameters.

```python
def add_user(conn: sqlite3.Connection, name: str, city: str) -> int:
    with conn:
        cursor = conn.execute("INSERT INTO users (name, city) VALUES (?, ?)", (name, city))
    return cursor.lastrowid
```

Two `?`, a tuple of two. The `with conn:` commits when the block ends. Without it the insert sits
in an open transaction until something commits it, and another connection cannot see it.

Reading, with a parameter.

```python
def find_by_name(conn: sqlite3.Connection, name: str) -> list[sqlite3.Row]:
    return conn.execute("SELECT id, name, city, balance FROM users WHERE name = ?", (name,)).fetchall()
```

`(name,)` with the comma is a one-element tuple. `(name)` without it is just the string, and
section 7 shows what happens then. `fetchall` returns every matching row; `fetchone` returns the
first or `None`.

A transfer, as one transaction.

```python
def transfer(conn: sqlite3.Connection, from_id: int, to_id: int, amount: int) -> None:
    with conn:
        conn.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, from_id))
        row = conn.execute("SELECT balance FROM users WHERE id = ?", (from_id,)).fetchone()
        if row["balance"] < 0:
            raise ValueError("insufficient balance")
        conn.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, to_id))
```

Subtract, check, add. If the check raises, the `with` rolls back the subtraction and the row is
as it was. If the process dies between the two updates, SQLite rolls back on the next open. There
is no moment when the money is gone from one row and not in the other that anyone can observe.

Save as `main.py` and run:

```bash
python main.py
```

```text
inserted ids: 1 2
found: {'id': 1, 'name': 'Meera', 'city': 'Pune', 'balance': 100}
parameterised: []
transfer refused: insufficient balance
Meera 70
Arjun 30
```

The `parameterised: []` line is the man with the long name being sent away. The same search
with an f-string, run against the same file:

```python
name = "x' OR '1'='1"
conn.execute(f"SELECT id, name FROM users WHERE name = '{name}'").fetchall()
```

```text
[{'id': 2, 'name': 'Arjun'}, {'id': 1, 'name': 'Meera'}]
```

Every row. That is the attack, in one line, and the placeholder version returned nothing from
the identical input.

Here is the whole program in one piece, `main.py`:

```python
import sqlite3
from pathlib import Path

DB = Path("users.db")


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0
        )
    """)


def add_user(conn: sqlite3.Connection, name: str, city: str) -> int:
    with conn:
        cursor = conn.execute("INSERT INTO users (name, city) VALUES (?, ?)", (name, city))
    return cursor.lastrowid


def find_by_name(conn: sqlite3.Connection, name: str) -> list[sqlite3.Row]:
    return conn.execute("SELECT id, name, city, balance FROM users WHERE name = ?", (name,)).fetchall()


def transfer(conn: sqlite3.Connection, from_id: int, to_id: int, amount: int) -> None:
    with conn:
        conn.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, from_id))
        row = conn.execute("SELECT balance FROM users WHERE id = ?", (from_id,)).fetchone()
        if row["balance"] < 0:
            raise ValueError("insufficient balance")
        conn.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, to_id))


def main() -> None:
    conn = connect()
    create_schema(conn)
    meera = add_user(conn, "Meera", "Pune")
    arjun = add_user(conn, "Arjun", "Delhi")
    with conn:
        conn.execute("UPDATE users SET balance = 100 WHERE id = ?", (meera,))
    print("inserted ids:", meera, arjun)

    for row in find_by_name(conn, "Meera"):
        print("found:", dict(row))

    evil = "x' OR '1'='1"
    print("parameterised:", [dict(r) for r in find_by_name(conn, evil)])

    transfer(conn, meera, arjun, 30)
    try:
        transfer(conn, meera, arjun, 500)
    except ValueError as err:
        print("transfer refused:", err)
    for row in conn.execute("SELECT name, balance FROM users ORDER BY id"):
        print(row["name"], row["balance"])


if __name__ == "__main__":
    main()
```

Run it a second time and it fails, because Meera already exists; section 7 has the message, and
the practice sheet has you make the program safe to re-run.

## 6. How the other two languages do it

**Go**

```go
db, err := sql.Open("sqlite", "users.db")
res, err := db.Exec("INSERT INTO users (name, city) VALUES (?, ?)", name, city)
var balance int
err = db.QueryRow("SELECT balance FROM users WHERE id = ?", id).Scan(&balance)
tx, err := db.Begin(); tx.Exec(...); tx.Exec(...); err = tx.Commit()
```

`database/sql` is the standard interface and the driver is a separate import. Parameters are
extra arguments, rows are read with `Scan` into variables, and a transaction is an explicit
`Begin`, `Commit` and a deferred `Rollback`.

**C++**

```cpp
sqlite3_stmt* stmt = nullptr;
sqlite3_prepare_v2(db, "INSERT INTO users (name, city) VALUES (?, ?)", -1, &stmt, nullptr);
sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);
sqlite3_bind_text(stmt, 2, city.c_str(), -1, SQLITE_TRANSIENT);
sqlite3_step(stmt);
sqlite3_finalize(stmt);
```

The C API: prepare a statement, bind each `?` by number, step it, finalise it. The parameters
are the same idea; the ceremony around them is what a RAII wrapper hides.

**The difference that matters:** Python's `with conn:` is the only one of the three that ties
commit and rollback to a block, so a raised exception rolls back without any code at the raise
site. In Go you `defer tx.Rollback()` and `Commit` at the end; in C++ you write a `Transaction`
class whose destructor rolls back unless `commit()` was called. Forget either, and an exception
leaves a transaction open with half the transfer done.

## 7. The traps

**The near-miss: the f-string.**

```python
conn.execute(f"SELECT id FROM users WHERE name = '{name}'")
```

It works for `Meera`. It returns everything for `x' OR '1'='1`. And for `x'; DROP TABLE users; --`
Python's driver happens to save you:

```text
sqlite3.ProgrammingError: You can only execute one statement at a time.
```

That is a safety net, not a defence; `executescript` has no such limit, other databases have no
such limit, and the `OR '1'='1'` form is a single statement. The placeholder is the defence.

**A string where a tuple was wanted.**

```python
conn.execute("INSERT INTO t VALUES (?)", ("Meera"))
```

```text
sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 5 supplied.
```

`("Meera")` is the string `"Meera"`, five characters, and the driver tried to bind each one.
`("Meera",)` with the comma.

**Running it twice.**

```text
sqlite3.IntegrityError: UNIQUE constraint failed: users.name
```

The `UNIQUE` on `name` did its job. Catch `IntegrityError` and answer 409, from
[day 50](../day-050-binary-search-revision/README.md), or use `INSERT OR IGNORE` when a repeat is
harmless.

**A table that is not there.**

```text
sqlite3.OperationalError: no such table: users
```

Usually `connect` pointed at a different file than you thought: a relative path resolved from
another working directory, or `:memory:`, which is a fresh empty database every time.

**Forgetting `row_factory`.** Rows come back as plain tuples:

```text
TypeError: tuple indices must be integers or slices, not str
```

`row["name"]` needs `conn.row_factory = sqlite3.Row`, set once on the connection.

**Two writers at once.**

```text
sqlite3.OperationalError: database is locked
```

SQLite allows one writer at a time. A second connection that tries to write while a transaction
is open waits for `timeout` seconds, five by default, and then raises this. It is not a bug in
SQLite; it is the signal that two processes are writing to one file, and that is the moment to
read [day 54](../day-054-quicksort/README.md).

**Foreign keys off.** `INSERT INTO orders (user_id) VALUES (99)` with no user 99 succeeds
silently unless `PRAGMA foreign_keys = ON` ran on that connection. With it:

```text
sqlite3.IntegrityError: FOREIGN KEY constraint failed
```

## 8. Say it out loud

**How it gets asked**

- What is SQL injection, and how do parameters stop it?
- What is a transaction, and when do you need one?
- Why SQLite, and when would you move off it?
- What does `database is locked` mean?

**The ninety-second script**

SQL injection is building a query by pasting user input into the SQL text, so that input
containing a quotation mark ends the string early and the rest of the input runs as SQL: a name
of `x' OR '1'='1` turns a lookup into "return everything", and a semicolon can append a `DROP
TABLE`. Parameters stop it because the SQL text and the values travel to the database
separately: the text has a `?` where each value goes, the values go as a tuple, and the database
binds them as data after it has already parsed the statement. There is no escaping and no
filtering, so there is nothing to get wrong; a value can never become part of the statement. In
Python that is `conn.execute("... WHERE name = ?", (name,))`, never an f-string. A transaction
groups writes so all of them commit or none do; `with conn:` commits on success and rolls back
on an exception, which is what a transfer between two rows needs. SQLite is one file with one
writer at a time, right for one machine, and `database is locked` is the sign you have outgrown
it.

**The follow-ups**

- **Can parameters be used for a table or column name?** *No. A `?` is a value. A column name
  chosen by the user has to be checked against a fixed list of allowed names and then pasted in,
  and that is the one place string building is unavoidable, so the allowed list is the defence.*
- **What about an ORM?** *It builds parameterised queries for you, which is most of the point of
  it, and [day 55](../day-055-quickselect/README.md) is about what else it buys and costs. A
  `raw()` or `text()` escape hatch in an ORM is exactly as injectable as an f-string.*
- **How do you test the transfer's rollback?** *Make the second update fail, deliberately, and
  assert the first row's balance is unchanged afterwards. A test that only checks the happy path
  has not tested the transaction.*

**A model answer**

"Injection is user input pasted into SQL text so that it becomes SQL. Parameters send the text
and the values on separate channels, so a value is bound as data after parsing and can never be
read as a statement; that is why it is a complete defence and escaping is not. `execute(sql,
(value,))` with the comma. Transactions with `with conn:` so a failed second update rolls back
the first. SQLite until two processes need to write, then Postgres."

## 9. Recall card

- Injection: user input pasted into SQL text; `x' OR '1'='1` returns everything. Parameters send text and values separately; the value can never become SQL.
- `conn.execute("... WHERE name = ?", (name,))`; the tuple needs its comma, or `Incorrect number of bindings`.
- `with conn:` is a transaction: commit on success, rollback on exception. A transfer is two updates inside one.
- `row_factory = sqlite3.Row` for `row["name"]`; `PRAGMA foreign_keys = ON` per connection; `UNIQUE` failures are `IntegrityError`.
- One writer at a time; `database is locked` means two processes are writing, and that is the day 54 signal.
