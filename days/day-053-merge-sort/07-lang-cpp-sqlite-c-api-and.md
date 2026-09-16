---
day: 53
track: lang-cpp
title: "SQLite C API and a thin RAII wrapper"
theme: "Databases I: SQLite"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 053 · C++ — SQLite C API and a thin RAII wrapper

**Today's theme:** Databases I: SQLite

**After today you can:** You can create a table, insert, query and update from each language, safely with parameters.

**The interviewer asks it as:** *What is SQL injection, and how do parameters stop it?*

---

## 1. What this is, and why it matters

SQLite is written in C and its API is C: `sqlite3_open` gives you a `sqlite3*`,
`sqlite3_prepare_v2` turns SQL text into a `sqlite3_stmt*`, `sqlite3_bind_*` fills the `?`
placeholders, `sqlite3_step` runs it one row at a time, and `sqlite3_finalize` and
`sqlite3_close` free what you opened. Every one of those returns an error code you must check,
and every opened thing must be closed on every path out of the function. Today you wrap that in
two small classes whose destructors do the closing, which is RAII from
[day 13](../day-013-reverse-and-rotate/README.md) doing exactly the job it was invented for.

At work, this is the shape of every C library you will ever use from C++: a handle, a set of
functions on it, a cleanup function, and a wrapper you write so the cleanup cannot be
forgotten. In interviews, the question in the header has one answer in every language; the C++
follow-up is "what happens to the statement if an exception is thrown between prepare and
finalize", and the wrapper is the answer.

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

The printed slips are numbered, and each one must come back and be filed, even the ones that
were sent back, even the ones that were half-written when the phone rang and the customer
walked off. For a while, Nazneen filed them when she remembered, and the ones she forgot lay
under the counter until the end of the month, when the count did not match. So the owner put a
tray by the hatch, and the rule became: a slip is torn off the pad, and the moment Nazneen is
done with it, however she is done with it, it goes in the tray. Not "when convenient". The
moment.

And the till rule: two packets paid for means two packets handed over, or the money goes back
and both packets go back on the shelf. Never one.

## 3. The idea in plain English

The stock book is the **database**, a `sqlite3*` from `sqlite3_open`. The slip is a **prepared
statement**, a `sqlite3_stmt*` from `sqlite3_prepare_v2`: the SQL text parsed once, with a slot
for each `?`. Filling the boxes is **binding**: `sqlite3_bind_text(stmt, 1, value, -1,
SQLITE_TRANSIENT)` puts a string into slot 1, `sqlite3_bind_int` puts an integer. The slots
are numbered from one. Passing the slip through is `sqlite3_step`, which returns `SQLITE_ROW`
when there is a row to read and `SQLITE_DONE` when there are no more. Reading a row's boxes is
`sqlite3_column_int(stmt, 0)` and `sqlite3_column_text(stmt, 1)`, numbered from zero.

The printed boxes are what stop **SQL injection**: the text goes to `prepare`, the values go to
`bind`, and by the time a value arrives the statement has already been parsed, so no value can
ever be read as SQL. Building the text with `+` is the blank slip, and the practice sheet has you
run both.

The tray by the hatch is **RAII**. `sqlite3_finalize(stmt)` must run on every path out: after
the last row, after an error, and after an exception thrown by something else in the function.
A class whose destructor calls it is the tray, because destructors run on every path out
including the exceptional one. Today's wrapper is two classes: `Database`, which owns the
`sqlite3*` and closes it, and `Statement`, which owns a `sqlite3_stmt*` and finalises it. Each
holds its pointer in a `std::unique_ptr` with a custom deleter, the same trick as the `CURL*`
on [day 45](../day-045-rotated-array-search/README.md).

The till rule is a **transaction**: `BEGIN`, the statements, `COMMIT`; or `ROLLBACK` if anything
fails. A third class, `Transaction`, runs `BEGIN` in its constructor and `ROLLBACK` in its
destructor unless `commit()` was called, so an exception between the two updates undoes the
first one without any code at the throw site.

Error text comes from `sqlite3_errmsg(db)`, a string owned by the database that says what went
wrong last. The wrapper turns a non-`SQLITE_OK` return into a thrown `std::runtime_error`
carrying that text, so the rest of the program never checks return codes by hand.

## 4. The picture

```text
  Database db("users.db");            sqlite3_open ........... sqlite3_close   (destructor)
  {
    Transaction tx(db);               BEGIN .................. ROLLBACK        (destructor, unless commit)
    Statement s(db, "UPDATE ... ?");  sqlite3_prepare_v2 ..... sqlite3_finalize (destructor)
    s.bind(1, amount);                sqlite3_bind_int
    s.step();                         sqlite3_step -> SQLITE_DONE
    ...
    tx.commit();                      COMMIT
  }                                   <- everything on the right column runs here, in reverse order
```

Notice that the right-hand column has a closing call for every opening call, and that none of
them appear in the left-hand column. The scope's closing brace is where they run.

## 5. The code, built step by step

Link against the system library: `libsqlite3-dev` on Debian and Ubuntu, `sqlite` on Homebrew,
`sqlite3` on vcpkg.

The database wrapper.

```cpp
#include <sqlite3.h>

class Database {
public:
    explicit Database(const std::string& path) : db_(nullptr, sqlite3_close) {
        sqlite3* raw = nullptr;
        if (sqlite3_open(path.c_str(), &raw) != SQLITE_OK) {
            std::string why = raw ? sqlite3_errmsg(raw) : "out of memory";
            sqlite3_close(raw);
            throw std::runtime_error("open " + path + ": " + why);
        }
        db_.reset(raw);
    }
    sqlite3* raw() const { return db_.get(); }
    void exec(const std::string& sql);
private:
    std::unique_ptr<sqlite3, decltype(&sqlite3_close)> db_;
};
```

`sqlite3_open` writes the handle through a pointer-to-pointer; the `unique_ptr` with
`sqlite3_close` as its deleter takes it from there. The constructor throws on failure, so a
`Database` that exists is open.

`exec` for statements with no parameters and no rows.

```cpp
void Database::exec(const std::string& sql) {
    char* error = nullptr;
    if (sqlite3_exec(db_.get(), sql.c_str(), nullptr, nullptr, &error) != SQLITE_OK) {
        std::string why = error;
        sqlite3_free(error);
        throw std::runtime_error(why);
    }
}
```

`sqlite3_exec` is for `CREATE TABLE`, `BEGIN`, `COMMIT`: text with no values in it. The error
string it hands back is allocated by SQLite and must be `sqlite3_free`d, which is one more
cleanup the wrapper hides.

The statement wrapper.

```cpp
class Statement {
public:
    Statement(Database& db, const std::string& sql) : db_(db.raw()), stmt_(nullptr, sqlite3_finalize) {
        sqlite3_stmt* raw = nullptr;
        if (sqlite3_prepare_v2(db_, sql.c_str(), -1, &raw, nullptr) != SQLITE_OK) {
            throw std::runtime_error(std::string("prepare: ") + sqlite3_errmsg(db_));
        }
        stmt_.reset(raw);
    }
    Statement& bind(int slot, int value) {
        check(sqlite3_bind_int(stmt_.get(), slot, value));
        return *this;
    }
    Statement& bind(int slot, const std::string& value) {
        check(sqlite3_bind_text(stmt_.get(), slot, value.c_str(), -1, SQLITE_TRANSIENT));
        return *this;
    }
    bool step() {
        const int rc = sqlite3_step(stmt_.get());
        if (rc == SQLITE_ROW) return true;
        if (rc == SQLITE_DONE) return false;
        throw std::runtime_error(std::string("step: ") + sqlite3_errmsg(db_));
    }
    int column_int(int index) const { return sqlite3_column_int(stmt_.get(), index); }
    std::string column_text(int index) const {
        const unsigned char* text = sqlite3_column_text(stmt_.get(), index);
        return text ? reinterpret_cast<const char*>(text) : "";
    }
private:
    void check(int rc) const {
        if (rc != SQLITE_OK) throw std::runtime_error(std::string("bind: ") + sqlite3_errmsg(db_));
    }
    sqlite3* db_;
    std::unique_ptr<sqlite3_stmt, decltype(&sqlite3_finalize)> stmt_;
};
```

`bind` returns `*this` so calls chain. `SQLITE_TRANSIENT` tells SQLite to copy the string,
because the `std::string` may be gone by the time the statement runs. `step` turns the three
outcomes into `true`, `false` and a throw. `column_text` returns `const unsigned char*` from the
C API, which is why the cast is there, and it can be null for a `NULL` column.

The transaction wrapper.

```cpp
class Transaction {
public:
    explicit Transaction(Database& db) : db_(db) { db_.exec("BEGIN"); }
    void commit() { db_.exec("COMMIT"); committed_ = true; }
    ~Transaction() {
        if (!committed_) {
            try { db_.exec("ROLLBACK"); } catch (...) {}
        }
    }
private:
    Database& db_;
    bool committed_ = false;
};
```

`BEGIN` on construction, `ROLLBACK` on destruction unless `commit()` ran. The `try` in the
destructor is because a destructor must not throw, from
[day 13](../day-013-reverse-and-rotate/README.md).

Using all three.

```cpp
int add_user(Database& db, const std::string& name, const std::string& city) {
    Statement(db, "INSERT INTO users (name, city) VALUES (?, ?)").bind(1, name).bind(2, city).step();
    return static_cast<int>(sqlite3_last_insert_rowid(db.raw()));
}

void transfer(Database& db, int from, int to, int amount) {
    Transaction tx(db);
    Statement(db, "UPDATE users SET balance = balance - ? WHERE id = ?").bind(1, amount).bind(2, from).step();
    Statement check(db, "SELECT balance FROM users WHERE id = ?");
    check.bind(1, from);
    if (check.step() && check.column_int(0) < 0) throw std::runtime_error("insufficient balance");
    Statement(db, "UPDATE users SET balance = balance + ? WHERE id = ?").bind(1, amount).bind(2, to).step();
    tx.commit();
}
```

A temporary `Statement` is prepared, bound, stepped, and finalised at the end of the full
expression. In `transfer`, the throw leaves the function through `tx`'s destructor, which rolls
back the subtraction.

Build and run:

```bash
g++ -Wall -Wextra -std=c++20 main.cpp -lsqlite3 -o app
./app
```

```text
inserted ids: 1 2
found: Meera Pune 100
parameterised: no such user
transfer refused: insufficient balance
Meera 70
Arjun 30
```

`parameterised: no such user` is the long-named man sent away. The same lookup with the text
built by `+` returns every row; section 7 shows it.

Here is the whole program in one piece, `main.cpp`:

```cpp
#include <sqlite3.h>

#include <iostream>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string>

class Database {
public:
    explicit Database(const std::string& path) : db_(nullptr, sqlite3_close) {
        sqlite3* raw = nullptr;
        if (sqlite3_open(path.c_str(), &raw) != SQLITE_OK) {
            std::string why = raw ? sqlite3_errmsg(raw) : "out of memory";
            sqlite3_close(raw);
            throw std::runtime_error("open " + path + ": " + why);
        }
        db_.reset(raw);
    }
    sqlite3* raw() const { return db_.get(); }
    void exec(const std::string& sql) {
        char* error = nullptr;
        if (sqlite3_exec(db_.get(), sql.c_str(), nullptr, nullptr, &error) != SQLITE_OK) {
            std::string why = error;
            sqlite3_free(error);
            throw std::runtime_error(why);
        }
    }
private:
    std::unique_ptr<sqlite3, decltype(&sqlite3_close)> db_;
};

class Statement {
public:
    Statement(Database& db, const std::string& sql) : db_(db.raw()), stmt_(nullptr, sqlite3_finalize) {
        sqlite3_stmt* raw = nullptr;
        if (sqlite3_prepare_v2(db_, sql.c_str(), -1, &raw, nullptr) != SQLITE_OK) {
            throw std::runtime_error(std::string("prepare: ") + sqlite3_errmsg(db_));
        }
        stmt_.reset(raw);
    }
    Statement& bind(int slot, int value) {
        check(sqlite3_bind_int(stmt_.get(), slot, value));
        return *this;
    }
    Statement& bind(int slot, const std::string& value) {
        check(sqlite3_bind_text(stmt_.get(), slot, value.c_str(), -1, SQLITE_TRANSIENT));
        return *this;
    }
    bool step() {
        const int rc = sqlite3_step(stmt_.get());
        if (rc == SQLITE_ROW) return true;
        if (rc == SQLITE_DONE) return false;
        throw std::runtime_error(std::string("step: ") + sqlite3_errmsg(db_));
    }
    int column_int(int index) const { return sqlite3_column_int(stmt_.get(), index); }
    std::string column_text(int index) const {
        const unsigned char* text = sqlite3_column_text(stmt_.get(), index);
        return text ? reinterpret_cast<const char*>(text) : "";
    }
private:
    void check(int rc) const {
        if (rc != SQLITE_OK) throw std::runtime_error(std::string("bind: ") + sqlite3_errmsg(db_));
    }
    sqlite3* db_;
    std::unique_ptr<sqlite3_stmt, decltype(&sqlite3_finalize)> stmt_;
};

class Transaction {
public:
    explicit Transaction(Database& db) : db_(db) { db_.exec("BEGIN"); }
    void commit() { db_.exec("COMMIT"); committed_ = true; }
    ~Transaction() {
        if (!committed_) {
            try { db_.exec("ROLLBACK"); } catch (...) {}
        }
    }
private:
    Database& db_;
    bool committed_ = false;
};

struct User {
    int id;
    std::string name;
    std::string city;
    int balance;
};

int add_user(Database& db, const std::string& name, const std::string& city) {
    Statement(db, "INSERT INTO users (name, city) VALUES (?, ?)").bind(1, name).bind(2, city).step();
    return static_cast<int>(sqlite3_last_insert_rowid(db.raw()));
}

std::optional<User> find_by_name(Database& db, const std::string& name) {
    Statement stmt(db, "SELECT id, name, city, balance FROM users WHERE name = ?");
    stmt.bind(1, name);
    if (!stmt.step()) return std::nullopt;
    return User{stmt.column_int(0), stmt.column_text(1), stmt.column_text(2), stmt.column_int(3)};
}

void transfer(Database& db, int from, int to, int amount) {
    Transaction tx(db);
    Statement(db, "UPDATE users SET balance = balance - ? WHERE id = ?").bind(1, amount).bind(2, from).step();
    Statement check(db, "SELECT balance FROM users WHERE id = ?");
    check.bind(1, from);
    if (check.step() && check.column_int(0) < 0) throw std::runtime_error("insufficient balance");
    Statement(db, "UPDATE users SET balance = balance + ? WHERE id = ?").bind(1, amount).bind(2, to).step();
    tx.commit();
}

int main() {
    try {
        Database db("users.db");
        db.exec("PRAGMA foreign_keys = ON");
        db.exec("CREATE TABLE IF NOT EXISTS users ("
                "id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, "
                "city TEXT NOT NULL, balance INTEGER NOT NULL DEFAULT 0)");

        const int meera = add_user(db, "Meera", "Pune");
        const int arjun = add_user(db, "Arjun", "Delhi");
        Statement(db, "UPDATE users SET balance = 100 WHERE id = ?").bind(1, meera).step();
        std::cout << "inserted ids: " << meera << ' ' << arjun << '\n';

        if (auto u = find_by_name(db, "Meera")) {
            std::cout << "found: " << u->name << ' ' << u->city << ' ' << u->balance << '\n';
        }
        const std::string evil = "x' OR '1'='1";
        std::cout << "parameterised: " << (find_by_name(db, evil) ? "found" : "no such user") << '\n';

        transfer(db, meera, arjun, 30);
        try {
            transfer(db, meera, arjun, 500);
        } catch (const std::runtime_error& e) {
            std::cout << "transfer refused: " << e.what() << '\n';
        }
        Statement all(db, "SELECT name, balance FROM users ORDER BY id");
        while (all.step()) {
            std::cout << all.column_text(0) << ' ' << all.column_int(1) << '\n';
        }
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
    return 0;
}
```

## 6. How the other two languages do it

**Python**

```python
with conn:
    conn.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, from_id))
    if conn.execute("SELECT balance FROM users WHERE id = ?", (from_id,)).fetchone()["balance"] < 0:
        raise ValueError("insufficient balance")
```

Prepare, bind, step and finalise are all inside `execute`, and the transaction is the `with`
block. The driver did the wrapping for you.

**Go**

```go
tx, err := db.Begin()
defer tx.Rollback()
_, err = tx.Exec("UPDATE users SET balance = balance - ? WHERE id = ?", amount, from)
err = tx.Commit()
```

The same three-class shape, with `defer` instead of a destructor: `Rollback` is scheduled the
moment `Begin` succeeds and is a no-op after `Commit`.

**The difference that matters:** C++ is the only one where you can see the C API, and the only
one where you wrote the cleanup yourself. The `Statement` destructor and the `Transaction`
destructor are the whole reason an exception in the middle of `transfer` does not leak a
statement and does not leave half a transfer committed. Python's `with` and Go's `defer` are the
same idea with the language doing the bookkeeping; in C++ the bookkeeping is a class you can
read.

## 7. The traps

**The near-miss: building the text.**

```cpp
Statement stmt(db, "SELECT id, name FROM users WHERE name = '" + name + "'");
```

With `name = "x' OR '1'='1"` this returns every user, no error, no warning. `prepare` sees a
perfectly valid statement, because the value is already part of it. Two `?` and two `bind`
calls, and the same input finds nobody.

**Binding a temporary without `SQLITE_TRANSIENT`.**

```cpp
sqlite3_bind_text(stmt, 1, (name + "!").c_str(), -1, SQLITE_STATIC);
```

`SQLITE_STATIC` promises the string outlives the statement. The temporary dies at the end of
the line, `step` reads freed memory, and the row gets garbage or the process gets a
segmentation fault, sometimes. `SQLITE_TRANSIENT` makes SQLite copy it.

**Slots from one, columns from zero.** `bind(0, name)`:

```text
bind: column index out of range
```

Bind slots start at 1. `column_int(0)` is the first selected column. This is the C API's own
inconsistency and every wrapper inherits it.

**Running it twice.**

```text
step: UNIQUE constraint failed: users.name
```

The wrapper's `step` threw with `sqlite3_errmsg`'s text. Catch it where a duplicate is a real
possibility, and answer 409.

**A table that is not there.**

```text
prepare: no such table: users
```

Almost always the wrong path to the file, or the `CREATE TABLE` not run on this connection's
file.

**Forgetting to link.** Build without `-lsqlite3`:

```text
/usr/bin/ld: /tmp/ccXyZ.o: in function `Database::Database(std::string const&)':
main.cpp:(.text+0x3c): undefined reference to `sqlite3_open'
collect2: error: ld returned 1 exit status
```

**No wrapper at all.** A `sqlite3_stmt*` prepared at the top of a function and finalised at the
bottom, with a `return` or a `throw` in between, is a leak that SQLite reports only at close:

```text
unable to close due to unfinalized statements or unfinished backups
```

That is `sqlite3_close` returning `SQLITE_BUSY`, and the wrapper is why you will not see it.

## 8. Say it out loud

**How it gets asked**

- What is SQL injection, and how do parameters stop it?
- Why wrap the C API? What does the wrapper actually guarantee?
- What happens to a prepared statement if an exception is thrown before `finalize`?
- How do you make a transaction exception-safe in C++?

**The ninety-second script**

SQL injection is user input pasted into the SQL text, so that a quotation mark in the input
ends the string and the rest runs as SQL; `x' OR '1'='1` turns a lookup into "everything".
Parameters stop it because the text goes to `sqlite3_prepare_v2` and the values go to
`sqlite3_bind_*` afterwards: the statement is parsed before any value exists, so a value can
never become part of it. It is a complete defence, not escaping. In C++ the API is C, so every
open has a close and every prepare has a finalize, and an exception between them leaks the
statement and, at `sqlite3_close`, fails with "unfinalized statements". So I wrap the `sqlite3*`
and the `sqlite3_stmt*` in classes holding a `unique_ptr` with the C cleanup function as the
deleter; the destructor runs on every path out, including a throw. The transaction is a third
class: `BEGIN` in the constructor, `ROLLBACK` in the destructor unless `commit()` was called, so
a throw between two updates rolls back the first. Errors come from `sqlite3_errmsg` and the
wrapper throws them, so the rest of the code never checks return codes.

**The follow-ups**

- **Why `SQLITE_TRANSIENT` and not `SQLITE_STATIC`?** *`STATIC` promises the buffer outlives
  the statement; with a `std::string` argument that promise is one temporary away from being
  false. `TRANSIENT` copies, which costs a few bytes and cannot be wrong.*
- **Is a `Statement` reusable?** *Yes: `sqlite3_reset` and `sqlite3_clear_bindings` put it back
  to the start with the same parsed SQL, which is the prepared-statement advantage in a loop.
  The wrapper in the lesson makes a fresh one per use for simplicity; the practice sheet adds
  `reset`.*
- **What about threads?** *One connection per thread, or a mutex around one connection. SQLite
  can be built to allow sharing, but the default mode and the simple rule is that a `sqlite3*`
  is not passed between threads.*

**A model answer**

"Injection is input pasted into SQL text becoming SQL. Parameters go through `bind` after
`prepare` has parsed the text, so they cannot. In C++: a `Database` class owning `sqlite3*`
with `sqlite3_close` as the `unique_ptr` deleter, a `Statement` class owning `sqlite3_stmt*` with
`sqlite3_finalize`, a `Transaction` class with `BEGIN` in the constructor and `ROLLBACK` in the
destructor unless committed. `SQLITE_TRANSIENT` on every string bind, slots from one, columns
from zero, and `sqlite3_errmsg` thrown as a `runtime_error`."

## 9. Recall card

- Injection: input pasted into SQL text. Parameters: text to `prepare`, values to `bind`, parsed before bound; never build the text with `+`.
- `Database` owns `sqlite3*` (deleter `sqlite3_close`); `Statement` owns `sqlite3_stmt*` (deleter `sqlite3_finalize`); destructors run on every path out.
- `bind` slots start at 1, `column_*` at 0; `SQLITE_TRANSIENT` on every string bind.
- `step` returns `SQLITE_ROW`, `SQLITE_DONE`, or an error; `sqlite3_errmsg(db)` is the text; throw it.
- `Transaction`: `BEGIN` in the constructor, `ROLLBACK` in the destructor unless `commit()`; a throw between updates undoes the first.
