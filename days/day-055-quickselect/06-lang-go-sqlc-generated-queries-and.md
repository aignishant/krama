---
day: 55
track: lang-go
title: "sqlc generated queries and golang-migrate"
theme: "Databases III: migrations and ORMs"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 055 · Go — sqlc generated queries and golang-migrate

**Today's theme:** Databases III: migrations and ORMs

**After today you can:** You can evolve a schema safely in each language and say what an ORM buys and costs.

**The interviewer asks it as:** *ORM or raw SQL? Defend your answer.*

---

## 1. What this is, and why it matters

Go's common answer to "ORM or raw SQL" is neither: `sqlc`. You write the SQL in a `.sql` file,
annotate each query with a name and a shape, and `sqlc generate` reads your schema and your
queries and writes typed Go functions, `GetUser(ctx, name) (User, error)`, that run exactly the
SQL you wrote. Migrations are separate, numbered `.sql` files applied by `golang-migrate`. There
is no object graph, no lazy loading, and so no N+1 by accident, because every query is one you
wrote and can see.

At work, this is the shape of a great many Go services, and the reason people choose it is
exactly the trade-off in the interview question: they want the safety and speed of generated,
typed code without the ORM's habit of running queries you did not ask for. In interviews, "ORM
or raw SQL, defend your answer" in Go is a chance to say that Go's ecosystem largely picked a
third option, and why.

## 2. The story

Farida's bakery has one binder of recipes, and every baker works from it. The binder is not
edited in place. When the almond cake needs less sugar, nobody reaches in and scribbles over the
old amount, because then a baker who is mid-bake would see a number change under their hands, and
nobody could say what the recipe was last Tuesday.

Instead there is a pad of change slips by the binder. Each slip is numbered, in order, and says
two things: what to change, and how to undo it. "Slip 14: almond cake, sugar from 200 grams to
160. To undo: back to 200." A slip is applied to the binder once, and then it is filed. A new
bakery that opens across town gets a fresh empty binder and the whole stack of slips, applied in
order, one to fourteen, and ends up with exactly the binder Farida has.

Because the slips are numbered and in order, everyone knows which slips a given kitchen has
applied. The new branch is "up to slip 14". If Farida writes slip 15 today, the branch is behind
by one, and catching up means applying slip 15, nothing else.

There is a second binder in this bakery that Farida's cousin runs differently. He does not keep
recipes as pages; he keeps a stack of recipe cards, one per dish, each card the exact list of
steps in his own hand. Nothing is inferred, nothing is cross-referenced, and there is never a
surprise trip to the store cupboard, because every trip is written on the card in front of him.
It is more cards to write, and more to keep in step when the flour supplier changes. But he can
hold up any card and tell you precisely what it does, which is not always true of Farida's
cross-referenced pages.

## 3. The idea in plain English

The cousin's recipe cards are **sqlc**. You write the SQL, one query per card, in a `.sql` file:

```sql
-- name: GetUser :one
SELECT id, name, city, age FROM users WHERE name = $1;
```

The `-- name: GetUser :one` comment is the annotation: the function's name, and that it returns
one row. `sqlc generate` reads your schema, checks the query against it, and writes a typed Go
`GetUser(ctx, name) (User, error)`. If the query names a column that does not exist, generation
fails, not runtime. There is no `user.orders` that quietly runs a query; to get a user's orders
you write and name a query that does, so the trip to the store cupboard is always on the card.

The change slips are **migrations**, numbered `.sql` file pairs: `000001_create.up.sql` with the
change, `000001_create.down.sql` with the undo. `golang-migrate` applies every `up` the database
has not seen, in order, and records progress in a `schema_migrations` table, exactly Alembic's
idea in files you write by hand.

"Which slips has this kitchen applied" is the version in `schema_migrations`. `migrate up` runs
the pending ones; `migrate down 1` un-applies the last, running its `down` file.

The ORM's N+1 does not happen here, because there is no lazy attribute to trip over. Fetching
users and their orders is a query you write, either a join or an `IN` list, and its cost is
visible in the SQL because you are looking at the SQL. The buy is that you write more of it; the
save is that you never run a query you did not mean to.

## 4. The picture

```text
  query.sql (the recipe cards)        migrations (the change slips)        database

  -- name: GetUser :one        000001_create.up.sql   -> users, orders
  SELECT ... WHERE name = $1                                (schema_migrations: 1)
  -- name: ListUsers :many     000002_add_age.up.sql  -> users.age added
  SELECT ... FROM users                                    (schema_migrations: 2)

  sqlc generate  ->  typed Go: GetUser(ctx, name) (User, error), checked against the schema
  migrate up     ->  apply every .up.sql after the recorded version, in order
```

Notice that the queries are checked against the schema at generate time, so a column that a
migration has not added yet is a build error, not a 3am one.

## 5. The code, built step by step

Two tools:

```bash
go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest
go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest
```

The migrations, written by hand. `migrations/000001_create.up.sql`:

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

and its `000001_create.down.sql`:

```sql
DROP TABLE orders;
DROP TABLE users;
```

The second slip, `000002_add_age.up.sql` and `.down.sql`:

```sql
ALTER TABLE users ADD COLUMN age INTEGER;
```

```sql
ALTER TABLE users DROP COLUMN age;
```

Apply them:

```bash
migrate -path migrations -database "$DATABASE_URL" up
```

```text
1/u create (12.3ms)
2/u add_age (4.1ms)
```

The queries, in `query.sql`.

```sql
-- name: CreateUser :one
INSERT INTO users (name, city, age) VALUES ($1, $2, $3) RETURNING *;

-- name: GetUser :one
SELECT * FROM users WHERE name = $1;

-- name: ListUsers :many
SELECT * FROM users ORDER BY id;

-- name: OrdersForUsers :many
SELECT * FROM orders WHERE user_id = ANY($1::int[]);
```

`OrdersForUsers` takes an array of ids, so all the orders come back in one query: the batched
version, written on purpose, because there is no lazy loading to do it wrong.

`sqlc.yaml` points at the schema and the queries:

```yaml
version: "2"
sql:
  - engine: "postgresql"
    schema: "migrations"
    queries: "query.sql"
    gen:
      go:
        package: "db"
        out: "db"
```

Generate:

```bash
sqlc generate
```

It writes `db/models.go` with a `User` struct and `db/query.sql.go` with the typed functions. If
`query.sql` selected a column the schema lacks:

```text
# package db
query.sql:2:8: column "aeg" does not exist
```

That is a build-time error from a typo, which an ORM would give you at runtime.

Using the generated code.

```go
queries := db.New(pool)   // pool is the pgxpool from day 54

meera, err := queries.CreateUser(ctx, db.CreateUserParams{Name: "Meera", City: "Pune", Age: pgtype.Int4{Int32: 31, Valid: true}})
if err != nil {
	return err
}

users, err := queries.ListUsers(ctx)
if err != nil {
	return err
}
ids := make([]int32, len(users))
for i, u := range users {
	ids[i] = u.ID
}
orders, err := queries.OrdersForUsers(ctx, ids)   // one query for all
if err != nil {
	return err
}
```

`CreateUser` returns a typed `User`; the nullable `age` is a `pgtype.Int4` with a `Valid` flag,
which is Go's honest way of saying a column can be null, the same problem as
[day 50](../day-050-binary-search-revision/README.md)'s `*int`. Totals are computed by grouping
`orders` by `user_id` in Go, having fetched them in the one `OrdersForUsers` call. There is no
loop that queries; the query happened once, up front, because you wrote it that way.

Run it:

```bash
DATABASE_URL=postgresql://postgres:secret@localhost:5432/app go run .
```

```text
created: {1 Meera Pune {31 true}}
users: 2
totals: map[Arjun:999 Meera:370]
```

The whole flow: hand-written migrations applied by `golang-migrate`, hand-written queries turned
into typed functions by `sqlc`, and every query visible in `query.sql`.

Here is the complete `query.sql`, which with the migrations and `sqlc.yaml` above is the whole
data layer:

```sql
-- name: CreateUser :one
INSERT INTO users (name, city, age) VALUES ($1, $2, $3) RETURNING *;

-- name: GetUser :one
SELECT * FROM users WHERE name = $1;

-- name: ListUsers :many
SELECT * FROM users ORDER BY id;

-- name: CreateOrder :one
INSERT INTO orders (user_id, amount) VALUES ($1, $2) RETURNING *;

-- name: OrdersForUsers :many
SELECT * FROM orders WHERE user_id = ANY($1::int[]);
```

## 6. How the other two languages do it

**Python**

```python
class User(Base):
    orders: Mapped[list["Order"]] = relationship(back_populates="user")

for u in session.scalars(select(User)):
    total = sum(o.amount for o in u.orders)   # lazy: one query per user
```

The ORM gives you `u.orders` as an attribute, which is convenient and is exactly where the N+1
hides. SQLAlchemy writes the SQL; sqlc makes you write it.

**C++**

```cpp
auto rows = tx.exec_params("SELECT id, name, city, age FROM users WHERE name = $1", name);
```

Raw libpqxx from [day 54](../day-054-quicksort/README.md), with a migration runner you write.
No generation and no ORM: every query is a string you check yourself, which sqlc automates the
checking of.

**The difference that matters:** SQLAlchemy generates the SQL from your objects, so you can run
a query without writing one, N+1 included. sqlc generates the Go from your SQL, so you cannot
run a query without writing it, and it is checked against the schema before the program builds.
Same destination, typed access to the database, from opposite ends: Python trusts the ORM and
watches the SQL log, Go writes the SQL and trusts the generator.

## 7. The traps

**The near-miss: the N+1, rebuilt by hand.** sqlc does not cause N+1, but you can still write
it:

```go
users, _ := queries.ListUsers(ctx)
for _, u := range users {
	orders, _ := queries.OrdersForUser(ctx, u.ID)   // one query per user
	// ...
}
```

That is a query per iteration, the same eleven-for-ten as the ORM, except here it is in plain
sight in your own loop. The `OrdersForUsers(ctx, ids)` array query is the fix, and the point is
that the fix and the mistake are both visible in your code, not the ORM's.

**Editing an applied migration.** Change `000002_add_age.up.sql` after production ran it and
fresh databases get the new version while production has the old, both recorded as version 2.
Migrations are append-only; write `000003` to correct it.

**A dirty migration.** If a migration fails halfway, `golang-migrate` marks the version dirty
and refuses to continue:

```text
error: Dirty database version 2. Fix and force version.
```

You fix the database by hand, then `migrate force 1` to set the version back to the last good
one, then re-run. The dirty flag is there so a half-applied migration cannot be silently built
on.

**Regenerating against the wrong schema.** `sqlc generate` reads the schema from the
`migrations` folder, not from the live database. If you add a column in a migration but a query
uses it before you list that migration in the schema path, generation fails with `column does
not exist`. The fix is that the migration files are the source of truth for both `migrate` and
`sqlc`.

**Nullable columns.** `age INTEGER` with no `NOT NULL` generates `pgtype.Int4`, not `int32`.
Treating it as a plain int:

```text
cannot use meera.Age (variable of type pgtype.Int4) as int32 value in argument
```

The `.Valid` flag is the missing-versus-zero distinction, and the compiler makes you handle it.

**Forgetting to regenerate.** Change `query.sql`, forget `sqlc generate`, and the Go code calls
the old function signature. It compiles against the stale generated file and runs the old query.
`sqlc generate` in the build, and the generated files committed, so a reviewer sees them change.

## 8. Say it out loud

**How it gets asked**

- ORM or raw SQL? Defend your answer.
- What is the N+1 problem, and does sqlc have it?
- How do you change a schema safely?
- Why generate code from SQL instead of using an ORM?

**The ninety-second script**

In Go the common answer is a third option, sqlc: I write the SQL, annotate each query with a
name and whether it returns one row or many, and a generator produces typed Go functions that
run exactly that SQL, checked against the schema at build time. It buys the safety and
convenience of typed access without the ORM's habit of running queries I did not write, which is
where the N+1 lives: an ORM lets a loop touch `user.orders` and quietly runs a query per user,
while sqlc has no lazy attribute, so fetching orders is a query I write, usually an array or a
join, and its cost is visible because I am looking at the SQL. The cost of sqlc is that I write
more SQL and must regenerate when it changes. Migrations are separate: numbered up and down
`.sql` files applied by golang-migrate, which records the version in a table, so a fresh database
and the full stack reach the same schema. Append-only, and a failed migration is marked dirty so
nothing builds on a half-applied change. So: sqlc for a Go service where I want every query
visible, an ORM in an ecosystem built around one, raw SQL for the rare query neither handles
well.

**The follow-ups**

- **Why not just an ORM in Go?** *There are ORMs in Go, like GORM, and they have the same N+1
  and the same convenience. The Go community leans to sqlc because the language's culture favours
  explicit over magic, and a generated typed function checked at build time fits that better
  than a runtime object graph.*
- **How do you deploy a migration safely?** *Backward-compatible steps: add a nullable column,
  deploy the migration, deploy the code, then a later migration tightens it. Never the migration
  and the code that requires it in the same instant.*
- **What stops SQL injection here?** *The generated functions use parameters, `$1`, because you
  wrote them that way. sqlc will not generate a function from a query with string concatenation
  in it, because you cannot express that in a `.sql` file; the placeholder is the only way.*

**A model answer**

"In Go I reach for sqlc: I write the SQL, it generates typed functions checked against the schema
at build time. It gives me typed access without the ORM's N+1, because there is no lazy
attribute, so every query is one I wrote and can see in `query.sql`. The cost is writing the SQL
and regenerating. Migrations are golang-migrate: numbered up and down files, a recorded version,
append-only, dirty-flagged on failure. ORM for an ecosystem built on one and watch the SQL log;
sqlc for Go; raw SQL for the query neither does well."

## 9. Recall card

- sqlc: write SQL with `-- name: X :one/:many`, generate typed Go checked against the schema; a bad column is a build error.
- No lazy loading, so no accidental N+1; batch with an array query, `WHERE id = ANY($1::int[])`, written on purpose.
- Migrations are numbered `.up.sql`/`.down.sql` applied by golang-migrate; a `schema_migrations` table records the version.
- Append-only; a failed migration is marked dirty and blocks further ones until `migrate force`.
- Nullable columns generate `pgtype.Int4` with a `Valid` flag; the compiler makes you handle missing-versus-zero.
