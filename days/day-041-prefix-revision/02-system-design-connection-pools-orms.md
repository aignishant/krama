---
day: 41
track: system-design
title: "Connection pools, ORMs, and the N+1 query"
phase: "Databases from zero"
status: written
---

# Day 041 · System Design — Connection pools, ORMs, and the N+1 query

**After today you can:** You can spot an N+1 query in code and fix it.

**The interviewer asks it as:** *Your page makes 200 database calls per request. What happened?*

---

## 1. What this is, and why they ask it

Today closes the database phase where most real slowness actually lives: not in the database, but
in **how applications talk to it**. Three ideas, one lesson. A **connection pool** keeps a set of
opened database connections and lends them out, because opening one is expensive and every
request needs one. An **ORM** (object-relational mapper — Django's models, SQLAlchemy, Hibernate)
translates between objects in code and rows in tables, writing the SQL for you. And the **N+1
query** is the classic disease at their intersection: one query for a list, then one *more* query
per item — 1 + N round trips where 2 queries would do — usually emitted invisibly by the ORM.

Interviewers love the hub question because it is a real incident, not a puzzle: every working
engineer has met the page that makes two hundred calls. The passing answer diagnoses from the
symptom (identical queries differing only in an id), names the cause (lazy loading in a loop),
fixes it with the ORM's own tools (eager loading), and knows the pool arithmetic underneath. It
is the most directly job-like question in the whole phase.

---

## 2. The story

The first time Suresh cooked for his in-laws, the meal was fine and the afternoon was a farce,
and his wife still tells the story.

He had decided on five dishes and started confidently at noon. Ten minutes in, no mustard seeds —
chappals on, down three floors, to the corner shop, back up. Started the dal. No tamarind.
Chappals on, down again. The third trip was coriander, the fourth was curd, and when he went down
the fifth time — matchsticks — the shopkeeper's boy laughed openly and asked whether he was
buying the shop item by item.

Each trip was short. Seven or eight minutes, door to door. That was precisely the poison: no
single trip felt bad enough to stop and think, so the afternoon leaked away four hundred rupees
of time in eight-minute instalments. Five dishes, eleven trips. The cooking itself took less
time than the stairs.

His mother-in-law, who has cooked for forty years and has opinions, delivered the verdict at
dinner, kindly. The problem was not his cooking, she said. The problem was that he decided what
he needed one ingredient at a time, at the moment he needed it. She plans differently: read all
five recipes *first*, write one list, make one trip. Everything on the counter before the first
flame.

And she added the detail Suresh thinks about most. In her building, the shop sends a delivery
boy who knows her flat — but even so, she said, you do not send him eleven times. The boy is
quick, but every trip is still the stairs, the road, the queue at the counter. The stairs do
not get shorter because the boy is fast.

The next family lunch, Suresh read the recipes the night before, made the list on his phone,
and went down once. His father-in-law, who notices things, remarked that the food arrived hot
and the cook arrived calm — and that both, in his experience, tend to happen together.

---

## 3. The idea in plain English

Suresh's eleven trips are the N+1 query. The stairs are the network round trip. His
mother-in-law's read-all-recipes-first is eager loading. And the delivery boy who is quick but
still climbs the stairs is the milliseconds that fooled everyone: **short trips, many times, is
still slow.**

### The N+1 query, mechanically

The page lists 50 blog posts with their authors. The code reads naturally:

```python
posts = Post.objects.all()[:50]          # query 1: the list
for post in posts:
    print(post.author.name)              # queries 2..51: one per post
```

The ORM fetched the posts. Each `post.author` is a *different table*, not yet loaded — so the
ORM, helpfully and silently, fetches it **on first touch**. That is **lazy loading**: the
ingredient bought at the moment it is needed. In a loop, lazy loading becomes 1 + N queries —
the list, plus one per item. Nothing errors. Every query is fast. The page is slow, and
[day 032](../day-032-variable-window/README.md) already warned that this cause **never appears
in a query plan** — every individual query planned perfectly.

### Why 200 fast queries make a slow page

Each query pays the stairs before it pays the query:

```
per call: network round trip ~0.5 ms + parse/plan ~0.2 ms + the query ~0.3 ms
200 calls ≈ 200 ms — sequentially, because each result decides nothing;
the loop just hasn't asked for the next one yet
2 calls   ≈   2 ms for the same data
```

The database is innocent — it answered 200 easy questions quickly. The *shape of the
conversation* is the disease, and that is why the fix lives in the application.

### The fix: read the recipes first

Every ORM has eager loading — the one-trip list, in two flavours:

- **Join it in** — one query bringing posts and authors together: Django's
  `select_related("author")`, SQLAlchemy's `joinedload` — right for to-one relationships
  ([day 028](../day-028-opposite-ends/README.md)'s joins doing what joins are for).
- **Batch it in** — two queries: the posts, then *all* needed authors in one
  `WHERE id IN (...)`: Django's `prefetch_related`, SQLAlchemy's `selectinload` — right for
  to-many relationships, where a join would duplicate rows
  ([day 028](../day-028-opposite-ends/README.md)'s row-multiplication warning).

Two queries instead of fifty-one. The loop code does not change — only the first line declares
what the loop will need.

### The connection pool: the delivery boy on retainer

Under all of this, every query needs a **connection** — and opening one is genuinely expensive:
TCP, then TLS ([day 006](../day-006-python-strings-dicts-sets/README.md)'s handshake),
authentication, and in Postgres a **whole operating-system process** per connection
([day 008](../day-008-reading-a-problem/README.md)'s processes, ~5–10 MB each). Five to ten
milliseconds and real memory, per opening. No sane application opens one per query, or even per
request: a **pool** opens, say, 20 connections at startup, lends one per request, takes it back
at the end. Borrowing from the pool costs microseconds. When the fleet of application servers
grows past what the database can host — `max_connections` defaults to 100 — a shared pooler in
front (**PgBouncer**) multiplexes thousands of application connections onto tens of real ones.

---

## 4. The picture

The two conversations, drawn to scale:

```
 N+1 (lazy loading in a loop)              EAGER (batched)

 app                      db               app                      db
  |---- posts? ----------->|                |---- posts? ----------->|
  |<--- 50 posts ----------|                |<--- 50 posts ----------|
  |---- author 7? -------->|                |---- authors IN (7,     |
  |<--- row ---------------|                |     12, 41, ...)? ---->|
  |---- author 12? ------->|                |<--- 34 rows -----------|
  |<--- row ---------------|                |
  |     ... 48 more ...    |               2 round trips  ≈ 2 ms
  |                        |
 51 round trips ≈ 50+ ms — each fast,
 and the total is the stairs × 51
```

**What to notice:** the right side sends *the same information* in two envelopes. Nothing about
the data changed — only the shape of the conversation.

The pool, and why it exists:

```
 open a fresh connection:            borrow from the pool:
   TCP handshake      ~0.2 ms          take a lease     ~0.01 ms
   TLS handshake      ~1-2 ms          run queries
   auth + fork a      ~2-5 ms          return the lease
   process (5-10 MB)
   ≈ 5-10 ms + memory, PER OPEN      the 20 connections were opened
                                     once, at application startup

 500 app instances × 20 pooled each = 10,000 wanted connections
 Postgres max_connections = 100     -> PgBouncer in front:
 10,000 app-side ----> [PgBouncer] ----> 50 real connections
```

**What to notice:** the pool solves the *per-request* cost; PgBouncer solves the *fleet* cost.
They are the same idea at two levels — never pay the stairs when a lease will do.

---

## 5. How it actually works

### What an ORM actually does

It maps classes to tables and objects to rows, tracks what you touch, and emits SQL. The
translation is honest work — parameterised queries, escaping, migrations — and the danger is
exactly its convenience: **the code stops looking like round trips.** `post.author.name` reads
like a field access and costs a query. The engineer's job is not to abandon the ORM but to know
what it emits — every serious ORM will show you (`django-debug-toolbar`, SQLAlchemy's `echo`,
Rails' log), and the habit of glancing at the emitted SQL for any new page is the cheapest
performance practice in the industry.

### The N+1 signature, in the wild

In the query log or APM trace, the fingerprint is unmistakable:

```
SELECT ... FROM posts ORDER BY created_at LIMIT 50;
SELECT ... FROM users WHERE id = 7;
SELECT ... FROM users WHERE id = 12;
SELECT ... FROM users WHERE id = 41;
   ... 47 more, identical but for the id ...
```

Many identical statements differing only in a bound value, inside one request.
`pg_stat_statements` — [day 032](../day-032-variable-window/README.md)'s tool — shows the same
truth aggregated: a trivial query with an enormous *call count*, ranked high by total time.
Diagnosis is reading, not cleverness.

### Eager loading, precisely

Django: `Post.objects.select_related("author")` adds a SQL `JOIN` — one query, right for
foreign keys pointing *to one*. `Post.objects.prefetch_related("comments")` runs the second
query with `WHERE post_id IN (...)` and stitches in memory — right for *to many*, avoiding
join row-multiplication. SQLAlchemy mirrors them as `joinedload` and `selectinload`. Rails:
`includes`. The deeper rule outlives every framework: **declare the shape of the read before
the loop starts** — the recipes before the shopping.

### Pool sizing, and the counterintuitive truth

Bigger pools are not faster. The database does useful work on roughly as many things as it has
cores; beyond that, extra connections are queue positions with memory costs
([day 008](../day-008-reading-a-problem/README.md)'s context-switching, plus a process apiece in
Postgres). The standard starting point (HikariCP's guidance) is around
`cores × 2 + effective_spindle_count` — for an 8-core database, a pool near 20, not 200. When
requests wait for a lease, the pool is not too small until the database is idle — check *its*
CPU first; a bigger pool in front of a saturated database only lengthens the queue,
[day 035](../day-035-choosing-the-pattern/README.md)'s arithmetic again.

### PgBouncer's price

PgBouncer in **transaction mode** lends a real connection per transaction, which is how 10,000
app connections fit on 50 real ones — but between transactions you have no fixed connection, so
**session state breaks**: session-level prepared statements, `SET` parameters, advisory locks
held across transactions. Most ORMs have a compatible mode; the interview point is knowing the
trade exists: the multiplexing is bought by giving up per-session state.

---

## 6. The numbers

### The hub incident, priced

```
page renders 50 posts + author + comment count, lazily:
  1 + 50 + 50 = 101 queries × ~1 ms round trip ≈ 100+ ms in the database
  conversation alone — before rendering anything

eagerly: 3 queries (posts; authors IN; counts grouped) ≈ 3-5 ms
                                        ~25-30× on one code change
```

### What N+1 does to the database fleet

```
that page at 200 req/s:
  lazy : 200 × 101 =  20,200 queries/s   -> the database's capacity spent
  eager: 200 × 3   =     600 queries/s      on stairs, not on work
```

The same server that "needs sharding" at twenty thousand queries a second is idling at six
hundred — **most "we outgrew Postgres" stories are conversation-shape stories**, which is why
this lesson sits at the end of the phase, before the scaling chapters can be blamed.

### Connection arithmetic

```
open-per-request at 200 req/s: 200 × ~5 ms opening = 1 full second of
   handshake work per second, plus 200 process forks — the database
   spends itself on greetings
pooled: 20 connections opened once; lease cost ~0.01 ms — noise

fleet: 500 instances × 20 = 10,000 wanted vs max_connections 100
   -> PgBouncer: 10,000 app-side on ~50 real; memory saved ≈
      9,950 × ~7 MB ≈ 70 GB of process overhead that never exists
```

### The pool-size sanity check

```
8-core database, queries averaging 5 ms:
  one connection ≈ 200 queries/s; ~16-20 busy connections saturate the cores
  a pool of 200 adds: 180 queue positions + 180 processes × 7 MB ≈ 1.3 GB
  and zero extra throughput
```

---

## 7. The trade-offs

### The ORM bargain

Kept: productivity, safety (parameterised SQL by default), migrations, and code the whole team
reads. Paid: the SQL becomes invisible, and invisible SQL breeds N+1s, accidental huge fetches
(`SELECT *` of a row with a megabyte column), and queries no index can love. The senior position
is neither worship nor abandonment: **use the ORM, read its output** — and drop to hand-written
SQL for the five queries per system that are actually hot, which every ORM allows. I would not
ban the ORM to prevent N+1s; I would turn on query logging in development and fail the test
suite on query-count regressions — the guard rail that scales.

### Eager loading is not "always"

Eager-load what the code path *will* use; eagerly fetching everything is its own disease —
hauling comment bodies for a page that shows counts, joining five tables for two fields.
The declaration-before-the-loop rule cuts both ways: declare what you need, and only that.
**I would not `select_related` speculatively** — I would let the query log tell me what each
page touches.

### Pool and pooler

A per-instance pool is non-negotiable — open-per-request is never right. PgBouncer earns its
place only when the fleet's connection count threatens `max_connections`: it is one more moving
part ([day 040](../day-040-2d-prefix-sums/README.md)'s operational bill) and its transaction
mode taxes session state. **I would not add PgBouncer at ten app instances** — arithmetic
first: instances × pool size against the database's comfortable connection count.

### The honest sentence

> The database phase ends where it began on [day 025](../day-025-pattern-matching/README.md):
> the database keeps its promises. When the page is slow with two hundred fast queries in it,
> the promise-breaker is the conversation — and the fix is one line that reads the recipes
> before the shopping.

---

## 8. In the interview

### How it gets asked

- *"Your page makes 200 database calls per request. What happened?"* — the hub incident;
  diagnose, name, fix.
- *"What is an N+1 query?"* — the definition form; give the loop, the signature, both fixes.
- *"Why do we need a connection pool?"* — the opening-cost arithmetic, and Postgres's
  process-per-connection.
- *"The app has 500 instances — what happens to the database's connections?"* — the fleet form:
  the multiplication, `max_connections`, PgBouncer and its transaction-mode trade.
- *"ORMs: good or bad?"* — the maturity probe; the answer is a bargain, not a side.

### What to say out loud, in the first ninety seconds

1. **Diagnose from the shape.** *"Two hundred calls in one request is almost certainly N+1: one
   query for a list, then one per item — I'd confirm in the query log by looking for identical
   statements differing only in an id."*
2. **Name the mechanism.** *"The ORM lazy-loads relations on first touch; touched in a loop,
   that's a round trip per element — each query fast, the sum slow, and none of it visible in a
   query plan."*
3. **Fix it in one line.** *"Eager-load what the loop needs: a join for to-one
   (`select_related`), a batched `IN` query for to-many (`prefetch_related`) — two or three
   queries total, a 25× on this page."*
4. **Add the guard rail.** *"Then keep it fixed: query logging in development and a test that
   fails when a page's query count jumps."*
5. **Check the floor underneath.** *"And I'd confirm connections are pooled — opening is 5–10 ms
   and a whole Postgres process; at fleet scale that's PgBouncer arithmetic."*

### The follow-ups

**"Each query takes one millisecond. Why is the page slow at all?"**
Because the two hundred milliseconds are sequential and none of them is the database working.
Each call pays the stairs — network round trip, parse, plan — before the query proper, and the
loop issues call 41 only after call 40 returns, since the code touches `post.author` one
iteration at a time; nothing overlaps. So the request spends ~200 ms mostly *in transit*, while
the database itself would happily have answered one `IN` query in three. That is also why this
disease hides from every database-side tool: the plan for each statement is perfect, and
`EXPLAIN` has nothing to confess — day 032 listed N+1 as one of the two slownesses that never
appear in a plan. The general principle, worth saying because it transfers to every remote call
in system design: **latency is paid per conversation turn, not per byte** — the fix is always to
change the shape of the conversation, fewer and fatter turns, whether the far side is Postgres,
Redis, or a microservice.

**"How would you catch N+1s before production, structurally?"**
Three layers, cheapest first. In development: query visibility on by default —
django-debug-toolbar or SQLAlchemy's echo — so the number sits in the developer's face while
the page is being built; most N+1s die here, free. In CI: assert query counts on key
endpoints — Django's `assertNumQueries`, or a test middleware that fails a page whose count
jumps from 4 to 104 — which converts the regression from a production incident into a red
build. In production: APM traces (the waterfall of 51 identical spans is unmistakable) and
`pg_stat_statements` sorted by call count — a trivial statement with millions of calls is an
N+1 broadcasting its location. What I would not rely on is code review alone: the whole
character of the bug is that the code reads innocently — `post.author.name` — and the reviewer
sees a field access, not a query. The structural fixes work because they measure the emitted
conversation, not the source's appearance.

**"When would you route around the ORM entirely?"**
For the handful of queries where the SQL is the design. Reports and analytics — multi-way
joins, window functions, grouping — where the ORM's rendition is either impossible or
unreadable; hot-path statements worth hand-tuning against the plan, day 032 style; bulk
operations, where a million ORM object instantiations lose to one
`INSERT ... SELECT` or `COPY` by two orders of magnitude; and anything needing database-side
arithmetic under concurrency — day 033's `SET balance = balance - 5000` — where object-think
(read, mutate, save) is precisely the lost-update anti-pattern. Every mature ORM has the
escape hatch (`raw()`, `text()`) and using it is not defeat; the codebase ends up ~95% ORM for
shape and safety, 5% SQL where SQL is the better language. The signal I watch for in either
direction: ORM contortions three method-calls deep trying to express a join — write the SQL;
or hand-written SQL doing what `select_related` would have done — use the tool.

### A model answer

> "Two hundred calls per request is the N+1 signature: one query fetched a list, and then the
> loop touched a lazy relation per item — the ORM emits a fresh query on each first touch. I'd
> confirm in thirty seconds from the query log or an APM trace: it'll show the same statement
> repeated with only the id changing.
>
> Why it's slow when every query is a millisecond: the cost is the round trip, not the query,
> and the loop pays it sequentially — two hundred turns of conversation for data that fits in
> two. The database side looks healthy throughout, which is why EXPLAIN finds nothing; this is
> one of the slownesses that never appears in a plan.
>
> The fix is to declare the read's shape before the loop: for a to-one relation like the
> author, a join — select_related in Django, joinedload in SQLAlchemy — and for to-many like
> comments, a batched IN query — prefetch_related or selectinload. That page goes from 101
> queries to 2 or 3, and at 200 requests a second the database drops from twenty thousand
> queries a second to six hundred — which is often the difference between 'we need to shard'
> and 'we're fine'.
>
> Then two guard rails so it stays fixed: query counts visible in development, and a CI
> assertion on key endpoints' query counts so a regression fails the build instead of shipping.
>
> And I'd check the layer underneath while I'm there: connections must come from a pool —
> opening one is five to ten milliseconds and a whole Postgres process, so per-request opening
> is a self-inflicted outage — sized around cores-times-two, not in the hundreds; and if we're
> running hundreds of app instances, the multiplication against max_connections says whether
> PgBouncer belongs in front, with its transaction-mode trade on session state."

---

## 9. Recall card

- **N+1 = one query for the list + one per item**, emitted by lazy loading in a loop. Signature:
  identical statements differing only in an id. Invisible to EXPLAIN — day 032's warning.
- **Latency is paid per conversation turn:** 101 × 1 ms sequential beats the database at
  nothing; 2–3 eager queries carry the same data. Fix: declare the read before the loop —
  join for to-one (`select_related`), batched `IN` for to-many (`prefetch_related`).
- **Guard rails, not vigilance:** query counts visible in dev, `assertNumQueries` in CI,
  `pg_stat_statements` by call count in production.
- **Pool always:** opening = TCP + TLS + auth + a Postgres process (~5–10 ms, ~7 MB). Size near
  cores × 2 — bigger pools are queue positions, not throughput.
- **Fleet arithmetic:** instances × pool vs `max_connections` → PgBouncer multiplexes
  (transaction mode trades away session state). Most "outgrew Postgres" stories are
  conversation-shape stories.
