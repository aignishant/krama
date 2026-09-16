---
day: 55
track: lang-python
title: "SQLAlchemy 2.0 and Alembic"
theme: "Databases III: migrations and ORMs"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 055 · Python — SQLAlchemy 2.0 and Alembic

**Today's theme:** Databases III: migrations and ORMs

**After today you can:** You can evolve a schema safely in each language and say what an ORM buys and costs.

**The interviewer asks it as:** *ORM or raw SQL? Defend your answer.*

---

## 1. What this is, and why it matters

An ORM, an object-relational mapper, lets you describe a table as a Python class and work with
rows as objects: `session.add(user)` instead of an `INSERT`, `user.orders` instead of a `SELECT`.
SQLAlchemy is the ORM most Python services use. A migration tool records every change to the
schema as a numbered, ordered file, so the database on your laptop, in the tests, and in
production all get there by the same steps; Alembic is SQLAlchemy's. The two together are how a
schema changes over months without anyone running `ALTER TABLE` by hand on a live database.

At work, the ORM is what you read every day and the migrations are what you are most afraid of,
because a bad one runs against production data. In interviews, "ORM or raw SQL, defend your
answer" is a favourite because there is no single right answer, and the good response names what
each one buys and what it costs, with the N+1 query as the cost you can demonstrate.

## 2. The story

Farida's bakery has one binder of recipes, and every baker works from it. The binder is not
edited in place. When the almond cake needs less sugar, nobody reaches in and scribbles over the
old amount, because then a baker who is mid-bake would see a number change under their hands, and
nobody could say what the recipe was last Tuesday.

Instead there is a pad of change slips by the binder. Each slip is numbered, in order, and says
two things: what to change, and how to undo it. "Slip 14: almond cake, sugar from 200 grams to
160. To undo: back to 200." A slip is applied to the binder once, and then it is filed. A new
bakery that opens across town gets a fresh empty binder and the whole stack of slips, applied in
order, one to fourteen, and ends up with exactly the binder Farida has. Not a photocopy of hers,
which might be smudged; the same binder, built the same way.

Because the slips are numbered and in order, everyone knows which slips a given kitchen has
applied. The new branch is "up to slip 14". If Farida writes slip 15 today, the branch is behind
by one, and catching up means applying slip 15, nothing else.

The binder is a convenience. Every baker could instead be handed the raw list of instructions
each morning, and for a simple loaf that would be faster and clearer. But for the wedding cake,
with its layers and fillings, the binder's structure, one page per component, cross-references
between them, saves real confusion. And there is one trap the binder hides. A baker making ten
small cakes, if they walk to the store cupboard for each cake's almonds separately, makes ten
trips when one trip with a list would have done. The binder does not stop them; it just makes the
ten trips feel as natural as one, because each looks like a small, reasonable thing.

## 3. The idea in plain English

The binder is the **ORM's models**. A class with typed attributes maps to a table:
`class User(Base)` with `id`, `name`, `city` becomes the `users` table with those columns.
SQLAlchemy 2.0 writes them as `Mapped[int]` and `mapped_column(...)`, and a **relationship**,
`orders: Mapped[list["Order"]]`, is the cross-reference to another table, so `user.orders` reads
the rows of `orders` that point back to this user.

A **session** is a workspace: `with Session(engine) as session`. You add objects to it, change
their attributes, and `session.commit()` writes every change as the right SQL in one
transaction. Reading is `session.scalars(select(User))`. You do not write `INSERT`, `UPDATE`, or
the `WHERE` by hand; you change the object and commit.

The change slips are **migrations**, and Alembic is the pad. `alembic revision --autogenerate`
compares your models to the current database and writes a numbered file with an `upgrade`
function, the change, and a `downgrade` function, the undo. `alembic upgrade head` applies every
slip the database has not seen, in order. A fresh database plus the whole stack of migrations
equals the schema your models describe, built the same way everywhere.

"Which slips has this kitchen applied" is the **version**: Alembic keeps a tiny table,
`alembic_version`, holding the id of the last migration applied, so it knows exactly which files
to run and which to skip.

The store-cupboard trap is the **N+1 query**. `for u in users: sum(o.amount for o in u.orders)`
looks like one loop. But `u.orders` is lazy: the first time you touch it, SQLAlchemy runs a
`SELECT` for that user's orders. Ten users is one query for the users plus ten for their orders,
eleven where two would do. `selectinload(User.orders)` tells SQLAlchemy to fetch all the orders
in one extra query up front. The ORM did not cause the trips; it made ten trips look like one
loop.

## 4. The picture

```text
  models.py (the binder)          migrations (the change slips)         database

  class User(Base)          slip 1: create users, create orders   ->  users, orders
    id, name, city                                                     (version: slip 1)
    orders -> Order         slip 2: add users.age                 ->  users.age added
                                                                       (version: slip 2)

  alembic upgrade head:  apply every slip after the recorded version, in order.
  a fresh db + slips 1..2  ==  the schema the models describe.
```

```text
  N+1 (lazy)                            batched (selectinload)

  SELECT ... FROM users                 SELECT ... FROM users
  SELECT ... FROM orders WHERE user_id=1   SELECT ... FROM orders WHERE user_id IN (1, 2, ...)
  SELECT ... FROM orders WHERE user_id=2   (one query for all users' orders)
  ... one per user
```

Notice the left column has one query per user and the right column has two queries total. With
a thousand users that is a thousand and one against two.

## 5. The code, built step by step

Install both:

```bash
python -m pip install sqlalchemy alembic
```

The models, in `models.py`.

```python
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    city: Mapped[str] = mapped_column(String(50))
    age: Mapped[int | None]
    orders: Mapped[list["Order"]] = relationship(back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[int]
    user: Mapped[User] = relationship(back_populates="orders")
```

`Mapped[int]` is a non-null column; `Mapped[int | None]` is nullable. `unique=True` and
`ForeignKey` become the constraints from [day 53](../day-053-merge-sort/README.md). The two
`relationship` calls with `back_populates` are the two ends of one link: `user.orders` and
`order.user` stay in step.

Setting up Alembic, once.

```bash
alembic init migrations
```

Then two edits: in `alembic.ini`, `sqlalchemy.url = sqlite:///app.db`; in `migrations/env.py`,
`from models import Base` and `target_metadata = Base.metadata`, so autogenerate can see your
models.

The first migration.

```bash
alembic revision --autogenerate -m "create users and orders"
```

```text
INFO  [alembic.autogenerate.compare.tables] Detected added table 'users'
INFO  [alembic.autogenerate.compare.tables] Detected added table 'orders'
Generating .../versions/61f1c34b0a44_create_users_and_orders.py ...  done
```

The generated file's `upgrade` is the change slip:

```python
def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('city', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'))
    op.create_table('orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'))
```

Apply it:

```bash
alembic upgrade head
```

```text
INFO  [alembic.runtime.migration] Running upgrade  -> 61f1c34b0a44, create users and orders
```

Now change the model, adding `age`, and generate a second slip. Alembic sees only the
difference:

```bash
alembic revision --autogenerate -m "add age to users"
```

```text
INFO  [alembic.autogenerate.compare.tables] Detected added column 'users.age'
```

```python
def upgrade() -> None:
    op.add_column('users', sa.Column('age', sa.Integer(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'age')
```

`alembic upgrade head` applies it; `alembic history` shows the ordered stack:

```text
61f1c34b0a44 -> 413ba32d8c8f (head), add age to users
<base> -> 61f1c34b0a44, create users and orders
```

The ORM program, `main.py`.

```python
engine = create_engine("sqlite:///app.db", echo="--echo" in sys.argv)


def seed(session: Session) -> None:
    if session.scalar(select(User).where(User.name == "Meera")):
        return
    meera = User(name="Meera", city="Pune", age=31)
    meera.orders = [Order(amount=250), Order(amount=120)]
    session.add_all([meera, User(name="Arjun", city="Delhi", age=30, orders=[Order(amount=999)])])
    session.commit()
```

`meera.orders = [...]` and the commit insert the user and the orders and set the foreign keys,
all as the right SQL, because the relationship knows how they connect. No `INSERT` is written by
hand.

Finding and changing.

```python
with Session(engine) as session:
    meera = session.scalar(select(User).where(User.name == "Meera"))
    print("found:", meera.name, meera.city, meera.age, [o.amount for o in meera.orders])
    meera.city = "Mumbai"
    session.commit()
```

`meera.city = "Mumbai"` then `commit()` is the whole update; SQLAlchemy notices the changed
attribute and issues the `UPDATE`. Run it:

```bash
python main.py
```

```text
found: Meera Pune 31 [250, 120]
lazy: {'Meera': 370, 'Arjun': 999}
eager: {'Meera': 370, 'Arjun': 999}
```

Both totals are right; the difference is how many queries each took, which `--echo` reveals.

The N+1, shown.

```python
def totals_lazy(session: Session) -> dict[str, int]:
    users = session.scalars(select(User)).all()
    return {u.name: sum(o.amount for o in u.orders) for u in users}


def totals_eager(session: Session) -> dict[str, int]:
    users = session.scalars(select(User).options(selectinload(User.orders))).all()
    return {u.name: sum(o.amount for o in u.orders) for u in users}
```

`python main.py --echo` prints the SQL. The lazy version, with two users:

```text
SELECT users.id, users.name, users.city, users.age FROM users
SELECT orders.id, orders.user_id, orders.amount FROM orders WHERE orders.user_id = ?
SELECT orders.id, orders.user_id, orders.amount FROM orders WHERE orders.user_id = ?
```

One for the users, one per user for their orders: three. The eager version:

```text
SELECT users.id, users.name, users.city, users.age FROM users
SELECT orders.user_id, orders.id, orders.amount FROM orders WHERE orders.user_id IN (?, ?)
```

Two, and it stays two at a thousand users. Same result, same code shape in the loop, one option
on the query.

Here is the whole program in one piece, `main.py` (with `models.py` beside it and the
migrations applied):

```python
import sys

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, selectinload

from models import Order, User

engine = create_engine("sqlite:///app.db", echo="--echo" in sys.argv)


def seed(session: Session) -> None:
    if session.scalar(select(User).where(User.name == "Meera")):
        return
    meera = User(name="Meera", city="Pune", age=31)
    meera.orders = [Order(amount=250), Order(amount=120)]
    arjun = User(name="Arjun", city="Delhi", age=30, orders=[Order(amount=999)])
    session.add_all([meera, arjun])
    session.commit()


def totals_lazy(session: Session) -> dict[str, int]:
    users = session.scalars(select(User)).all()
    return {u.name: sum(o.amount for o in u.orders) for u in users}


def totals_eager(session: Session) -> dict[str, int]:
    users = session.scalars(select(User).options(selectinload(User.orders))).all()
    return {u.name: sum(o.amount for o in u.orders) for u in users}


def main() -> None:
    with Session(engine) as session:
        seed(session)
        meera = session.scalar(select(User).where(User.name == "Meera"))
        print("found:", meera.name, meera.city, meera.age, [o.amount for o in meera.orders])
        meera.city = "Mumbai"
        session.commit()
        print("lazy:", totals_lazy(session))
        print("eager:", totals_eager(session))


if __name__ == "__main__":
    main()
```

## 6. How the other two languages do it

**Go**

```go
// query.sql, checked in:
//   -- name: GetUser :one
//   SELECT id, name, city, age FROM users WHERE name = $1;
user, err := queries.GetUser(ctx, "Meera")   // generated, typed
```

Go's common choice is `sqlc`: you write the SQL, a tool generates typed Go functions from it,
and migrations are separate files run by `golang-migrate`. There is no lazy loading and so no
N+1 by accident, because every query is one you wrote.

**C++**

```cpp
// 001_create.up.sql, run by a migration runner you write:
//   CREATE TABLE users (...);
auto rows = tx.exec_params("SELECT id, name, city, age FROM users WHERE name = $1", name);
```

C++ has no mainstream ORM in this course; you write the SQL against libpqxx from
[day 54](../day-054-quicksort/README.md), and the migration runner is a loop that applies
numbered `.sql` files it has not recorded yet, which the practice sheet has you build.

**The difference that matters:** Python's ORM writes the SQL for you, which is why
`user.orders` in a loop can silently become N+1; the query you did not write is the query you
did not count. sqlc and raw libpqxx make every query visible, so the N+1 is impossible to write
without seeing it, at the cost of writing every query by hand. The migration idea, numbered
ordered files with a recorded version, is identical in all three; only the ORM part differs.

## 7. The traps

**The near-miss: the N+1 in a loop.** The lazy `totals` above is correct and, at scale, slow.
The tell is in the `--echo` output: a `SELECT ... FROM orders WHERE user_id = ?` repeated, once
per user. It never appears in a two-user test's result, only in production's latency.
`selectinload` on the query is the fix, and reading your own SQL log is how you catch it.

**Editing a migration that has run.** Change `413ba32d8c8f` after it is applied in production and
the fresh databases get the new version while production has the old, and they have diverged
with the same version id. Migrations are append-only, like the ledgers in this repository: a
mistake gets a new migration that corrects it, never an edit to the old one.

**A model change with no migration.** Add `age` to the model, run the program without
`alembic revision` and `upgrade`, and:

```text
sqlite3.OperationalError: no such column: users.age
```

The model and the database disagree. `alembic check` catches this in CI:

```text
No new upgrade operations detected.
```

means they agree; anything else means someone changed a model without a migration.

**Using an object after its session closes.**

```python
with Session(engine) as session:
    meera = session.scalar(select(User).where(User.name == "Meera"))
print(meera.orders)     # outside the with
```

```text
sqlalchemy.orm.exc.DetachedInstanceError: Parent instance <User> is not bound to a Session; lazy load operation of attribute 'orders' cannot proceed
```

`orders` was never loaded, and now there is no session to load it. Load what you need inside the
session, with `selectinload`, or keep the session open while you use the object.

**Autogenerate does not see everything.** It detects tables and columns well, and misses some
changes: a column rename looks like a drop plus an add, and a `CHECK` constraint or a data
change it cannot infer. Read every generated migration before applying it; the `-- please
adjust!` comment Alembic writes is not decoration.

**A downgrade that loses data.** `downgrade` for "add a column" is `drop_column`, which throws
the column's data away. Downgrades are for un-applying a migration in development; in production
a mistake is usually fixed by a new forward migration, not by going back, precisely because back
can mean delete.

## 8. Say it out loud

**How it gets asked**

- ORM or raw SQL? Defend your answer.
- What is the N+1 query problem, and how do you find it?
- How do you change a database schema without breaking production?
- What does a migration's downgrade do, and when do you not use it?

**The ninety-second script**

An ORM maps tables to classes, so I work with objects and it writes the SQL: `session.add`,
`user.city = "Mumbai"`, `commit`. It buys speed on the common cases and keeps the schema in one
place as models. It costs visibility: the query I did not write is the query I forget to count,
and the classic example is the N+1, where a loop over users touching `user.orders` runs one
query for the users and one more per user for their orders. I find it by reading the ORM's SQL
log, and I fix it with eager loading, `selectinload`, which fetches all the children in one
extra query. So my answer is: ORM for the ordinary create-read-update-delete that is most of a
service, raw SQL for the few complex reads where I want to see and shape the query. Schema
changes go through migrations: numbered, ordered files with an upgrade and a downgrade, applied
by a tool that records which the database has, so a fresh database and the full stack reach the
same schema everywhere. Migrations are append-only; a mistake is a new migration, never an edit
to one that has run, and a downgrade is a development tool because for "add a column" it means
drop the column and its data.

**The follow-ups**

- **When is the ORM clearly wrong?** *A reporting query with several joins, a window function,
  or a bulk update of a million rows. The ORM's version is slower and harder to read than the
  SQL, and it may load a million objects into memory. That is raw SQL, or a `text()` query.*
- **How do you deploy a migration safely?** *Make it backward-compatible so the old code still
  runs against the new schema: add a nullable column, deploy the migration, deploy the code that
  uses it, then in a later migration make it non-null. Never a migration and the code that needs
  it in the same instant.*
- **Does the ORM stop SQL injection?** *Yes, because it parameterises for you, which is most of
  why people trust it. The escape hatch, a raw `text()` with an f-string in it, is exactly as
  injectable as [day 53](../day-053-merge-sort/README.md)'s f-string.*

**A model answer**

"ORM for ordinary CRUD, because it writes correct parameterised SQL and keeps the schema as
models; raw SQL for complex reads and bulk writes, because there I want to see the query. The
ORM's cost is the query you did not write, the N+1: a loop over users touching `user.orders` is
one query plus one per user, which I catch in the SQL log and fix with `selectinload`. Schema
changes are Alembic migrations, numbered and ordered, upgrade and downgrade, with a recorded
version so every database gets there by the same steps. Append-only, and downgrades are for
development because they can drop data."

## 9. Recall card

- ORM maps tables to classes; `session.add`, attribute change, `commit` write the SQL. Buys speed on CRUD, costs query visibility.
- N+1: a loop touching `user.orders` runs one query plus one per user; read the SQL log to find it, `selectinload` to fix it.
- Migrations are numbered ordered files with `upgrade`/`downgrade`; `alembic revision --autogenerate`, `alembic upgrade head`; a version table records progress.
- Append-only: never edit an applied migration; a mistake is a new one. Downgrade can drop data, so it is a development tool.
- `DetachedInstanceError` means using an object after its session closed; `no such column` means a model changed without a migration, which `alembic check` catches.
