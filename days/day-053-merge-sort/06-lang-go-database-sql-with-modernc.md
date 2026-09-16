---
day: 53
track: lang-go
title: "database/sql with modernc sqlite, prepared statements, and Scan"
theme: "Databases I: SQLite"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 053 · Go — database/sql with modernc sqlite, prepared statements, and Scan

**Today's theme:** Databases I: SQLite

**After today you can:** You can create a table, insert, query and update from each language, safely with parameters.

**The interviewer asks it as:** *What is SQL injection, and how do parameters stop it?*

---

## 1. What this is, and why it matters

`database/sql` is Go's standard interface to any relational database: `Open`, `Exec` for
statements that change things, `QueryRow` and `Query` for statements that return rows, `Scan`
to read a row's columns into variables, and `Begin`, `Commit`, `Rollback` for transactions. The
actual database is a **driver** you import for its side effect; today's is `modernc.org/sqlite`,
a pure-Go SQLite that needs no C compiler. Swap the import and the connection string and the
same code talks to Postgres on [day 54](../day-054-quicksort/README.md).

At work, every Go service that touches a database goes through this interface, whether directly
or under a query builder, so the shapes you learn today are the shapes you will read every day.
In interviews, the question in the header has the same answer in every language; the Go
follow-up is usually about `rows.Close` and what a forgotten one does to a connection pool.

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
customer with every word of that as their name, finds nobody, and sends the slip back.

The hatch has one more rule, about the slips themselves. When the back room finishes with a
slip, it comes back through the hatch and Nazneen files it. There are only so many slips in the
pad. On a bad Saturday she stopped filing, slips piled up on the back-room side, and by four
o'clock the pad was empty and nobody could order anything, because every slip was sitting in the
back, finished, waiting for someone to bring it home.

And the till rule: two packets paid for means two packets handed over, or the money goes back
and both packets go back on the shelf. Never one.

## 3. The idea in plain English

The stock book is the **database**, and `sql.Open("sqlite", "users.db")` gives you a `*sql.DB`,
which is not one connection but a **pool** of them, opened as needed and reused, the way the
HTTP client from [day 47](../day-047-minimise-the-maximum/README.md) pools sockets. `Open` does
not touch the file; `db.Ping()` does, and is the way to find out at start-up that the path is
wrong.

A slip through the hatch is a **statement**. `db.Exec(sql, args...)` for `INSERT`, `UPDATE`,
`CREATE`; it returns a result with `LastInsertId` and `RowsAffected`. `db.QueryRow(sql, args...)`
for a statement that returns one row; `db.Query` for many.

The printed boxes are **parameters**: a `?` in the SQL for each value, and the values as extra
arguments to `Exec` or `Query`. The text and the values reach the database separately, and a
value can never be parsed as SQL, whatever characters it holds. Building the text with
`fmt.Sprintf` is the blank slip, and section 7 shows the attack.

**Scan** is reading the boxes of a returned row into Go variables: `row.Scan(&id, &name)`, one
pointer per selected column, in order. A `QueryRow` that matched nothing returns `sql.ErrNoRows`
from `Scan`, which you check with `errors.Is`.

The slips that must come home are `rows.Close()`. `db.Query` returns a `*sql.Rows` that holds
one connection from the pool until you have read to the end or called `Close`. `defer
rows.Close()` on the line after the error check, every time, or the pool runs dry the way the
pad did.

A **prepared statement**, `db.Prepare(sql)`, parses the SQL once and returns a `*sql.Stmt` you
can execute many times with different arguments. It is the printed slip kept in a drawer,
ready. Useful in a loop; the plain `Exec` with arguments is parameterised just the same.

The till rule is a **transaction**: `tx, err := db.Begin()`, then `tx.Exec` for each step,
`tx.Commit()` at the end, and `defer tx.Rollback()` right after `Begin` so that any early return
undoes everything. `Rollback` after a successful `Commit` is a harmless no-op, which is what
makes the defer safe.

## 4. The picture

```text
  the blank slip (Sprintf)                  the printed slip (parameters)

  "SELECT id FROM users WHERE name = '"     "SELECT id FROM users WHERE name = ?"
     + name + "'"                                                            |
  name = x' OR '1'='1                       args: "x' OR '1'='1"
  -> SELECT id FROM users                   -> compare the whole string to name
     WHERE name = 'x' OR '1'='1'            -> sql.ErrNoRows
  -> every row
```

Notice that the statement text on the right never changes between calls. The database parses it
once, then binds whatever the value is, quotation marks included, as a name.

## 5. The code, built step by step

Fetch the driver once:

```bash
go mod init users && go get modernc.org/sqlite
```

Opening the pool and declaring the table.

```go
import (
	"database/sql"
	_ "modernc.org/sqlite"
)

db, err := sql.Open("sqlite", "users.db")
if err != nil {
	return err
}
defer db.Close()
if err := db.Ping(); err != nil {
	return err
}
```

The blank import runs the driver's `init`, which registers the name `"sqlite"`. `Open` with a
name nobody registered is the first trap in section 7.

```go
const schema = `
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    balance INTEGER NOT NULL DEFAULT 0
)`

if _, err := db.Exec(schema); err != nil {
	return err
}
```

Inserting, with parameters.

```go
func addUser(db *sql.DB, name, city string) (int64, error) {
	res, err := db.Exec("INSERT INTO users (name, city) VALUES (?, ?)", name, city)
	if err != nil {
		return 0, err
	}
	return res.LastInsertId()
}
```

Two `?`, two arguments. `LastInsertId` is the id SQLite assigned.

Reading one row, and many.

```go
type User struct {
	ID      int64
	Name    string
	City    string
	Balance int
}

func findByName(db *sql.DB, name string) (*User, error) {
	var u User
	err := db.QueryRow("SELECT id, name, city, balance FROM users WHERE name = ?", name).
		Scan(&u.ID, &u.Name, &u.City, &u.Balance)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &u, nil
}
```

Four columns selected, four pointers to `Scan`, in the same order. `ErrNoRows` is "no such
user", an ordinary answer, so it becomes `nil, nil`.

```go
func listUsers(db *sql.DB) ([]User, error) {
	rows, err := db.Query("SELECT id, name, city, balance FROM users ORDER BY id")
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var users []User
	for rows.Next() {
		var u User
		if err := rows.Scan(&u.ID, &u.Name, &u.City, &u.Balance); err != nil {
			return nil, err
		}
		users = append(users, u)
	}
	return users, rows.Err()
}
```

`defer rows.Close()` is the slip coming home. `rows.Next()` advances; `rows.Err()` after the loop
reports a failure that ended it early, which `Next` returning `false` cannot tell you on its own.

A transfer, as one transaction.

```go
func transfer(db *sql.DB, from, to int64, amount int) error {
	tx, err := db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()
	if _, err := tx.Exec("UPDATE users SET balance = balance - ? WHERE id = ?", amount, from); err != nil {
		return err
	}
	var balance int
	if err := tx.QueryRow("SELECT balance FROM users WHERE id = ?", from).Scan(&balance); err != nil {
		return err
	}
	if balance < 0 {
		return errors.New("insufficient balance")
	}
	if _, err := tx.Exec("UPDATE users SET balance = balance + ? WHERE id = ?", amount, to); err != nil {
		return err
	}
	return tx.Commit()
}
```

`defer tx.Rollback()` right after `Begin`. Every `return err` and the `insufficient balance`
return leave through the defer, which undoes the subtraction. The happy path ends in `Commit`,
after which the deferred `Rollback` does nothing.

Run it:

```bash
go run main.go
```

```text
inserted ids: 1 2
found: {1 Meera Pune 100}
parameterised: <nil>
transfer refused: insufficient balance
Meera 70
Arjun 30
```

`parameterised: <nil>` is the long-named man being sent away: no user has that whole string as
a name. The same lookup with `fmt.Sprintf` returns Arjun and Meera both; section 7 shows it.

Here is the whole program in one piece, `main.go`:

```go
package main

import (
	"database/sql"
	"errors"
	"fmt"
	"os"

	_ "modernc.org/sqlite"
)

const schema = `
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    balance INTEGER NOT NULL DEFAULT 0
)`

type User struct {
	ID      int64
	Name    string
	City    string
	Balance int
}

func addUser(db *sql.DB, name, city string) (int64, error) {
	res, err := db.Exec("INSERT INTO users (name, city) VALUES (?, ?)", name, city)
	if err != nil {
		return 0, err
	}
	return res.LastInsertId()
}

func findByName(db *sql.DB, name string) (*User, error) {
	var u User
	err := db.QueryRow("SELECT id, name, city, balance FROM users WHERE name = ?", name).
		Scan(&u.ID, &u.Name, &u.City, &u.Balance)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	return &u, nil
}

func listUsers(db *sql.DB) ([]User, error) {
	rows, err := db.Query("SELECT id, name, city, balance FROM users ORDER BY id")
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var users []User
	for rows.Next() {
		var u User
		if err := rows.Scan(&u.ID, &u.Name, &u.City, &u.Balance); err != nil {
			return nil, err
		}
		users = append(users, u)
	}
	return users, rows.Err()
}

func transfer(db *sql.DB, from, to int64, amount int) error {
	tx, err := db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()
	if _, err := tx.Exec("UPDATE users SET balance = balance - ? WHERE id = ?", amount, from); err != nil {
		return err
	}
	var balance int
	if err := tx.QueryRow("SELECT balance FROM users WHERE id = ?", from).Scan(&balance); err != nil {
		return err
	}
	if balance < 0 {
		return errors.New("insufficient balance")
	}
	if _, err := tx.Exec("UPDATE users SET balance = balance + ? WHERE id = ?", amount, to); err != nil {
		return err
	}
	return tx.Commit()
}

func run() error {
	db, err := sql.Open("sqlite", "users.db")
	if err != nil {
		return err
	}
	defer db.Close()
	if err := db.Ping(); err != nil {
		return err
	}
	if _, err := db.Exec(schema); err != nil {
		return err
	}

	meera, err := addUser(db, "Meera", "Pune")
	if err != nil {
		return err
	}
	arjun, err := addUser(db, "Arjun", "Delhi")
	if err != nil {
		return err
	}
	if _, err := db.Exec("UPDATE users SET balance = 100 WHERE id = ?", meera); err != nil {
		return err
	}
	fmt.Println("inserted ids:", meera, arjun)

	found, err := findByName(db, "Meera")
	if err != nil {
		return err
	}
	fmt.Println("found:", *found)

	evil := "x' OR '1'='1"
	suspicious, err := findByName(db, evil)
	if err != nil {
		return err
	}
	fmt.Println("parameterised:", suspicious)

	if err := transfer(db, meera, arjun, 30); err != nil {
		return err
	}
	if err := transfer(db, meera, arjun, 500); err != nil {
		fmt.Println("transfer refused:", err)
	}
	users, err := listUsers(db)
	if err != nil {
		return err
	}
	for _, u := range users {
		fmt.Println(u.Name, u.Balance)
	}
	return nil
}

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
```

## 6. How the other two languages do it

**Python**

```python
with conn:
    conn.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, from_id))
    row = conn.execute("SELECT balance FROM users WHERE id = ?", (from_id,)).fetchone()
    if row["balance"] < 0:
        raise ValueError("insufficient balance")
```

The transaction is a `with` block: commit when it ends, rollback when it raises. Rows are
read by column name and there is no `Scan`, no `Close`, and no pool to run dry, because one
connection is one connection.

**C++**

```cpp
Statement stmt(db, "SELECT balance FROM users WHERE id = ?");
stmt.bind(1, from_id);
if (stmt.step()) balance = stmt.column_int(0);
```

The same prepare, bind, step as Go's `QueryRow` and `Scan`, with the finalise in a destructor.
The transaction is a class whose destructor rolls back unless `commit()` ran.

**The difference that matters:** Go is the only one where a query holds a connection from a
pool until you let go of it. Python's `sqlite3` has one connection and C++'s wrapper owns the
statement; neither can leak a connection by forgetting to read to the end. In Go, `db.Query`
without `defer rows.Close()` works perfectly in a test, and in production the pool is empty
after a few hundred requests and every query waits forever.

## 7. The traps

**The near-miss: `Sprintf`.**

```go
query := fmt.Sprintf("SELECT id, name FROM users WHERE name = '%s'", name)
rows, err := db.Query(query)
```

With `name = "x' OR '1'='1"`, this returns every user. There is no error and `go vet` is silent,
because the compiler cannot know the string will reach a database. The `?` and the extra
argument are the fix, and the practice sheet has you run both against the same file.

**Forgetting the driver import.**

```go
db, err := sql.Open("sqlite", "users.db")
```

```text
sql: unknown driver "sqlite" (forgotten import?)
```

The `_ "modernc.org/sqlite"` line is what registers the name. The error message says so.

**Forgetting `rows.Close()`.** No error, ever, in a small program. In a server, after the pool's
connections are all held by finished-but-unclosed `Rows`:

```text
database is locked
```

or every query hanging with no message at all. `defer rows.Close()` on the line after
`if err != nil`, without exception.

**Wrong number of `Scan` targets.**

```go
db.QueryRow("SELECT id, name FROM users WHERE id = ?", 1).Scan(&id)
```

```text
sql: expected 2 destination arguments in Scan, not 1
```

**`ErrNoRows` treated as a failure.**

```go
if err := row.Scan(&u.ID); err != nil {
	return nil, err   // a missing user is now a 500
}
```

```text
sql: no rows in result set
```

`errors.Is(err, sql.ErrNoRows)` first, and decide what "not found" means to the caller.

**Running it twice.** The `UNIQUE` on `name` fires, in the driver's words:

```text
constraint failed: UNIQUE constraint failed: users.name (2067)
```

**A transaction without the deferred rollback.** An early `return err` between `Begin` and
`Commit` leaves the transaction open on a connection that goes back to the pool still holding
it. The next user of that connection is inside somebody else's half-finished transfer.
`defer tx.Rollback()` immediately after `Begin`, always.

## 8. Say it out loud

**How it gets asked**

- What is SQL injection, and how do parameters stop it?
- What does `sql.Open` actually open?
- What goes wrong if you forget `rows.Close()`?
- How do you write a transaction in Go so an early return cannot leave it open?

**The ninety-second script**

SQL injection is user input pasted into SQL text, so that a quotation mark in the input ends the
string early and the rest runs as SQL: `x' OR '1'='1` turns a lookup into "everything". Parameters
stop it because the statement text and the values travel to the database separately; the text
has a `?` per value, the values are extra arguments, the database parses the text first and binds
the values as data afterwards, so a value cannot become part of the statement. That is a
complete defence, not a filter. In Go that is `db.Exec` or `db.Query` with `?` and arguments, never
`Sprintf`. `sql.Open` returns a pool, not a connection, and does not touch the database until
`Ping`. A `Query` holds one pooled connection until `rows.Close`, so `defer rows.Close()` goes on
the line after the error check or the pool runs dry in production. A transaction is `Begin`,
`defer tx.Rollback()` immediately, the statements on `tx`, then `Commit`; the deferred rollback
makes every early return safe and is a no-op after a commit.

**The follow-ups**

- **When would you use `Prepare`?** *In a loop that runs the same statement thousands of times,
  to parse it once. For a handler that runs it once per request, plain `Exec` with arguments is
  just as safe and simpler; `database/sql` caches prepared statements per connection anyway.*
- **What about a column name from the user?** *Not a parameter; `?` binds values only. Check it
  against a fixed allowed list and then build the text. The list is the defence there.*
- **How do you set pool limits?** *`db.SetMaxOpenConns`, `SetMaxIdleConns`, and
  `SetConnMaxLifetime`. For SQLite, one writer means `SetMaxOpenConns(1)` for a write-heavy
  program is honest; [day 54](../day-054-quicksort/README.md) is where the numbers matter.*

**A model answer**

"Injection is input pasted into SQL text becoming SQL. Parameters keep text and values on
separate channels, bound after parsing, so a value cannot be a statement. In Go: `?` and
arguments, never `Sprintf`; `sql.Open` is a pool; `defer rows.Close()` after every `Query` or the
pool drains; `errors.Is(err, sql.ErrNoRows)` for not found; and `Begin`, `defer tx.Rollback()`,
statements, `Commit`, so an early return cannot leave a transaction on a pooled connection."

## 9. Recall card

- Injection: input pasted into SQL text. Parameters: `?` in the text, values as arguments, bound after parsing; never `Sprintf`.
- `sql.Open` is a pool and touches nothing; `db.Ping` checks; the driver is a blank import, or `unknown driver "sqlite"`.
- `QueryRow(...).Scan(&a, &b)` one pointer per column; `errors.Is(err, sql.ErrNoRows)` is "not found".
- `rows, err := db.Query(...)`, then `defer rows.Close()` on the next line, `rows.Next()`, `rows.Scan`, `rows.Err()`.
- `tx, _ := db.Begin()`, `defer tx.Rollback()` at once, statements on `tx`, `tx.Commit()` last.
