---
day: 34
track: system-design
title: "Isolation levels and the anomalies they allow"
phase: "Databases from zero"
status: written
---

# Day 034 · System Design — Isolation levels and the anomalies they allow

**After today you can:** You can name dirty read, non-repeatable read and phantom read, and which level stops each.

**The interviewer asks it as:** *What isolation level would you use, and what anomaly are you accepting?*

---

## 1. What this is, and why they ask it

Yesterday established that isolation is the only ACID letter with a dial. Today is the dial. There are
four standard **isolation levels** — read uncommitted, read committed, repeatable read, serialisable —
and each weaker level permits specific, named **anomalies**: ways concurrent transactions can see
things that a one-at-a-time world could never show them. Choosing a level is choosing which anomalies
you are prepared to handle yourself.

This is a favourite interview question because it has a memorisable table on the surface and real
understanding underneath, and the two are easy to tell apart. Anyone can recite "repeatable read stops
non-repeatable reads". The candidate who gets hired can describe each anomaly as a story with two
transactions in it, say what their database's default actually permits, and answer the hub question —
*which level, and what are you accepting?* — with a decision rather than a definition. It appears in
backend interviews at every product company, usually right after ACID, and the follow-up about
**write skew** is where senior candidates are separated from the table-reciters.

---

## 2. The story

Kavita caters weddings, and the part of the job that has nothing to do with cooking is the guest
count. The count lives in the family's phone chat, and the family will not stop touching it.

Three things have gone wrong often enough that she has names for them.

The first she calls the taken-back number. Two years ago, a groom's uncle typed that ninety extra
people were coming from Nagpur, and Kavita saw it and ordered two more vats of oil. An hour later he
deleted the message — it was the wrong chat, the ninety people were for a different function. The
order was already placed. She had acted on something that was never actually true.

The second is the number that will not sit still. On a Thursday she checked the chat at ten in the
morning — 240 guests — and planned the plates. At noon she checked again to plan the sweets, and it
said 265. Same job, same day, two answers. Nothing was wrong, exactly. The family had every right to
change it. But her plates and her sweets were now planned for two different weddings.

The third is the count that grows while you are counting. She once went through the chat adding up
the out-of-town guests, got 38, and went through again to be sure — 41. Three new names had arrived
between her first pass and her second, typed in by an aunt while Kavita was still counting.

Her fix, these days, is a rule. At noon on the day she plans, she takes a screenshot of the list and
works only from the screenshot. The chat can boil all it likes; her plates, sweets and seating all
come from one frozen moment, so they at least agree with each other. Anything typed after noon goes
into the next day's screenshot.

And for the last hour before the wedding, she asks the family to stop editing altogether. They
grumble. It is the only way the seating chart and the reality in the hall come out the same.

---

## 3. The idea in plain English

Kavita's three disasters are the three read anomalies, in the official order. Her screenshot and her
stop-editing hour are two isolation levels. All that changes in the technical version is that the
family chat is a table, and Kavita and the family are **concurrent transactions**.

### The three read anomalies

**Dirty read** — the taken-back number. A transaction reads data that another transaction has written
but **not yet committed**. If the writer rolls back, the reader acted on a value that officially never
existed. Kavita bought oil for ninety guests who were never coming.

**Non-repeatable read** — the number that will not sit still. A transaction reads the same row twice
and gets different values, because another transaction **committed a change** in between. Both reads
saw committed truth; they just saw different days of it. Plates for 240, sweets for 265.

**Phantom read** — the count that grows while you are counting. A transaction runs the same *search*
twice — "all out-of-town guests" — and the second run returns **rows that did not exist the first
time**. The difference from a non-repeatable read is worth being able to say: non-repeatable is an
existing row *changing*; a phantom is a *new row appearing* that matches your condition.

And from yesterday, the fourth horseman, which is a write anomaly rather than a read one: the **lost
update** — two transactions read the same value, both compute, both write, one overwrites the other.
Keep it in the set, because interviewers do.

### The four levels, and what each one buys

Each level is defined by which anomalies it forbids:

| Level | Dirty read | Non-repeatable read | Phantom read |
|---|---|---|---|
| **Read uncommitted** | allowed | allowed | allowed |
| **Read committed** | stopped | allowed | allowed |
| **Repeatable read** | stopped | stopped | allowed by the standard |
| **Serialisable** | stopped | stopped | stopped |

**Read uncommitted** is the no-rules chat: you can see half-typed messages. Almost nothing runs here.

**Read committed** — Postgres's default — promises only that you never see uncommitted work. Every
statement sees the freshest committed truth, which is precisely why two statements in one transaction
can disagree: truth moved between them. This is Kavita checking the live chat twice.

**Repeatable read** is the screenshot. The transaction takes a **snapshot** at its first read and
every statement in it sees that snapshot, however long it runs. Internally consistent, possibly
slightly stale.

**Serialisable** is the stop-editing hour. The database guarantees the outcome is the same as if the
transactions had run one at a time, in some order — and anything that cannot be made to look serial
is **aborted** and must retry.

### The screenshot has a hole in it

Here is the subtlety the follow-up questions live in. Repeatable read gives every transaction a
consistent *picture*, but two transactions can each act on their own picture and produce a combined
result no serial order could ever create. The classic is **write skew**: two rows, an invariant
across both, and two transactions that each check the invariant on their snapshot, then write to
*different* rows. Each write is fine alone; together they break the rule. Snapshots cannot catch it,
because neither transaction touched the row the other wrote. Only serialisable — which watches what
you *read*, not just what you wrote — stops it. §5 has the worked example.

---

## 4. The picture

The three anomalies, as timelines. Time runs left to right; each line is one transaction.

```
 DIRTY READ (stopped by: read committed and above)

 T1:  BEGIN -- UPDATE stock = 0 ----------------- ROLLBACK
 T2:                   SELECT stock -> 0
                       ^ read a value that was never committed:
                         T2 refuses an order it could have taken


 NON-REPEATABLE READ (stopped by: repeatable read and above)

 T1:  ------------- UPDATE price = 120; COMMIT
 T2:  BEGIN -- SELECT price -> 100 ------------- SELECT price -> 120 -- COMMIT
              ^ both reads saw committed data,      ^ same row, same
                just from different moments           transaction, new answer


 PHANTOM READ (stopped by: serialisable; in Postgres, by repeatable read too)

 T1:  ------------------- INSERT guest ('Pune'); COMMIT
 T2:  BEGIN -- COUNT guests in Pune -> 8 ------- COUNT guests in Pune -> 9
              ^ no existing row changed:            ^ a NEW row appeared
                the SET of matching rows grew         inside one transaction
```

**What to notice:** in all three, every individual read is perfectly reasonable. The anomaly is only
visible when you compare two moments — which is exactly why code that "worked in testing", where
nothing ran concurrently, produces these in production.

The levels, as how much of the chat Kavita is looking at:

```
 read uncommitted   the live chat, half-typed messages included
 read committed     the live chat, sent messages only     <- Postgres default
 repeatable read    the noon screenshot
 serialisable       the screenshot, plus nobody may edit
                    anything you LOOKED AT until you finish
```

---

## 5. How it actually works

### Snapshots, not locks: MVCC does the reading

Postgres, and InnoDB under MySQL, deliver read isolation with **multi-version concurrency control**
from [day 033](../day-033-window-with-a-map/README.md): writers create new row versions rather than
overwriting, so readers never block writers. The difference between the two everyday levels is only
**when the snapshot is taken**:

- **Read committed:** a fresh snapshot per *statement*. Each statement sees everything committed
  before it started. Hence non-repeatable reads between statements.
- **Repeatable read:** one snapshot per *transaction*, taken at the first read. Every statement sees
  it. In Postgres this snapshot also makes phantoms impossible — the second `COUNT` cannot see rows
  committed after the snapshot — so **Postgres repeatable read is stronger than the standard
  requires**. The standard's table says "phantoms allowed"; Postgres's implementation says no.

Two Postgres quirks worth stating in an interview. First, `READ UNCOMMITTED` exists as a keyword but
**behaves as read committed** — Postgres never shows uncommitted data to anyone. Second, MySQL's
InnoDB defaults to repeatable read, not read committed, so "what is the default?" has a
per-database answer.

### What repeatable read does on a write conflict

Snapshots handle reads. When two repeatable-read transactions **update the same row**, the second
waits for the first to commit, and then Postgres refuses to apply a write on top of data that changed
under the snapshot:

```
ERROR:  could not serialize access due to concurrent update
```

The application must catch this and **retry the whole transaction**. That error is not a bug — it is
repeatable read doing its job, and it is how repeatable read stops lost updates that read committed
would allow through silently.

### Write skew: the anomaly the snapshot cannot see

The canonical example: a hospital roster requires **at least one doctor on call**. Alice and Bob are
both on call. Both try to go off duty at the same moment, at repeatable read:

```
 invariant: at least one row must have on_call = true

 T1 (Alice): count on-call doctors -> 2   [her snapshot]
 T2 (Bob):   count on-call doctors -> 2   [his snapshot]
 T1: UPDATE alice SET on_call = false;  COMMIT   -- fine: 2 -> 1
 T2: UPDATE bob   SET on_call = false;  COMMIT   -- fine on HIS snapshot: 2 -> 1

 result: zero doctors on call. No serial order could produce this.
```

No error is raised, because the transactions wrote to **different rows** — the concurrent-update
check never fires. Each decision was valid on its own snapshot; the combination is invalid. The same
shape hides in "book the seat if it is free", "spend if the balance across accounts stays positive",
"claim the username if unused" — any **check-then-act across rows**.

### Serialisable: how the database catches it

Postgres's serialisable level is **serialisable snapshot isolation (SSI)**: repeatable read plus
tracking of read/write **dependencies** between concurrent transactions. When it detects a pattern
that could not occur in any serial order — Alice read what Bob wrote around, and Bob read what Alice
wrote around — it aborts one of them:

```
ERROR:  could not serialize access due to read/write dependencies among transactions
HINT:  The transaction might succeed if retried.
```

The hint is literal: **serialisable code must run inside a retry loop.** That is the real cost of the
level — not slow reads, but a background abort rate that your application has to absorb. SQL Server
and older systems instead take **range locks** at serialisable, blocking writers that would create
phantoms; same guarantee, different price — waiting instead of retrying.

### The targeted alternative: lock exactly what you check

You rarely raise the level globally. At read committed, you can buy just the strength you need:

```sql
SELECT * FROM doctors WHERE on_call = true FOR UPDATE;
```

`FOR UPDATE` locks the rows you read, so Bob's identical `SELECT` waits until Alice commits — then
sees one doctor and refuses. This converts the write skew into a wait. It works when you can name the
rows to lock; it cannot protect a *count of rows that do not exist yet*, which is where serialisable
or a separate constraint-carrying row comes in. Tomorrow — locking and deadlocks — is entirely about
this tool and its failure mode.

---

## 6. The numbers

### The price of each step up

Read committed to repeatable read is nearly free on reads — same MVCC machinery, one snapshot instead
of many. The costs appear as aborts and as bloat:

```
repeatable read, two writers on the same row:
  loser gets "could not serialize access due to concurrent update"
  cost = one full transaction retry

serialisable, measured on TPC-C-like workloads (the Postgres SSI paper):
  low contention  : ~5-10% throughput below repeatable read
  high contention : abort rates climb into double digits, and
                    every abort is a retry your app must perform
```

### What a retry rate does to capacity

```
1,000 transactions/second at serialisable
3% abort rate            -> 30 retries/second
each retry repeats ~5 ms of work -> 150 ms of extra work per second  (0.15 cores)

but at 20% aborts on a hot row:
200 retries/s, some aborting AGAIN on retry
-> effective throughput can fall by a third while CPU stays busy
```

The multiplication to say out loud: **abort rate × retry cost is a tax on every write**, and it grows
with contention, not with data size. Serialisable on a low-contention workload is cheap. Serialisable
on one hot counter row is a retry storm.

### The cost of check-then-act done wrong, for scale

```
seat-booking site, 2,000 bookings/minute at peak, read committed, no locks:
check-seat-free -> act window of ~10 ms per booking
two requests for the same seat inside 10 ms = a double booking

popular concert, 500 requests hit one seat in the first second:
window overlap is a certainty, not a risk -- every hot seat double-books
```

That is why "we will just check first" fails precisely when the product succeeds.

### The snapshot you hold open

A repeatable-read transaction holds its snapshot for its whole life, so
[day 033](../day-033-window-with-a-map/README.md)'s bloat arithmetic applies with a sharper edge:

```
a 30-minute repeatable-read report on a database taking 5,000 updates/second:
  5,000 × 1,800 s = 9,000,000 dead row versions VACUUM cannot reclaim
  at ~100 bytes each ≈ 900 MB of bloat, from one report
```

Long reports at repeatable read are fine — that is what the level is for — but they are a scheduled
cost, not a free lunch. Run them on a replica when they grow.

---

## 7. The trade-offs

### Choose per transaction, not per database

The level is a property of each transaction (`BEGIN ISOLATION LEVEL SERIALIZABLE`), and the strong
move in an interview is to refuse the global question. Payments and inventory adjustments:
serialisable, or read committed with `FOR UPDATE`, inside a retry loop. Reports and exports:
repeatable read, so every table in the report agrees with every other. Everything else: the default,
with the arithmetic done in SQL — `SET balance = balance - 5000` — so lost updates cannot happen.

### Read committed plus discipline, or serialisable plus retries

Most production systems run read committed and handle the anomalies that matter **explicitly**:
database-side arithmetic, `FOR UPDATE` on check-then-act, unique constraints to kill duplicate
inserts. That is more code and more thinking, and it is fast and predictable. Serialisable replaces
all that thinking with one guarantee and one obligation — **every transaction must be retryable** —
which means no side effects inside transactions (no emails, no HTTP calls: yesterday's rule with a
second reason now).

### I would not use it if...

**I would not use serialisable if** the workload concentrates writes on a few hot rows and I cannot
afford retry storms — a like-counter, a stock ticker. I would use database-side arithmetic there,
which needs no isolation at all. **I would not stay at read committed if** the money path contains a
check-then-act across rows — that is write skew territory, and "it passed the tests" means only that
the tests did not run concurrently. **I would not use repeatable read for a quick single-statement
read** — a lone `SELECT` at read committed is already a consistent snapshot of one moment; the level
buys nothing there.

### The honest sentence

> Most teams run Postgres at read committed and never change it, and the ones that get away with it
> are the ones that know *which* anomalies they are accepting and where. The level is not a safety
> setting you turn up; it is a contract about which failures are yours to prevent.

---

## 8. In the interview

### How it gets asked

- *"What isolation level would you use, and what anomaly are you accepting?"* — the hub question, and
  it wants a decision with reasons, not the table.
- *"What is the difference between a non-repeatable read and a phantom read?"* — the classic
  discriminator; existing row changing versus new row appearing.
- *"Your default is read committed. What can still go wrong?"* — lost updates, non-repeatable reads,
  phantoms, write skew: everything except dirty reads.
- *"Two transactions each check a condition and then write, and the invariant breaks anyway. What
  happened?"* — write skew, being described to see if you can name it.

### What to say out loud, in the first ninety seconds

1. **Frame the dial.** *"Isolation comes in four levels, and each weaker level admits specific named
   anomalies in exchange for concurrency — so the question is which anomalies this workload can
   tolerate."*
2. **Name the anomalies as one-liners.** *"Dirty read: seeing uncommitted work. Non-repeatable read:
   the same row answering differently twice. Phantom: new rows appearing between two runs of the
   same search. And the write-side one: the lost update."*
3. **State the defaults.** *"Postgres defaults to read committed — no dirty reads, everything else
   possible. MySQL's InnoDB defaults to repeatable read."*
4. **Give the decision rule.** *"I choose per transaction: read committed plus SQL-side arithmetic
   for ordinary writes, repeatable read for multi-statement reports, and serialisable — in a retry
   loop — for check-then-act invariants that span rows."*
5. **Show the depth card early.** *"The subtle failure is write skew: two transactions check an
   invariant on their own snapshots and write different rows, so no conflict is detected — snapshot
   levels can't see it; serialisable can."*

### The follow-ups

**"Explain write skew, and why repeatable read does not stop it."**
Write skew is two transactions reading an overlapping set of rows, each validating an invariant
against its snapshot, then writing to *different* rows so that the combined result violates the
invariant. The on-call roster is the standard example: two doctors, a rule that one must stay on
call, and both go off duty simultaneously — each saw two on-call doctors in its snapshot, each
reduced the count to one, and reality went to zero. Repeatable read cannot stop it because its
machinery detects conflicting writes to the *same* row, and here there are none; the conflict is
between what one transaction *read* and what the other *wrote*. Serialisable — SSI in Postgres —
tracks exactly those read/write dependencies and aborts one transaction. The lightweight alternative
at lower levels is to make the reads conflict deliberately: `SELECT ... FOR UPDATE` on the rows you
checked, so the second transaction waits and then re-checks against the new truth.

**"You are at read committed. How do you prevent a lost update?"**
Four tools, in the order I would reach for them. First, do the arithmetic in the database —
`UPDATE accounts SET balance = balance - 5000` — because the read and the write become one atomic
statement under a row lock, and the anomaly is impossible. Second, if the logic must live in the
application, `SELECT ... FOR UPDATE` to lock the row across the read-think-write gap. Third,
optimistic locking: carry a version column, write with
`UPDATE ... SET version = version + 1 WHERE id = ? AND version = ?`, and treat zero affected rows as
"someone got there first — reload and retry"; that is the right tool when contention is rare and you
would rather not hold locks. Fourth, raise that transaction to repeatable read and let
`could not serialize access due to concurrent update` force the retry. What I would not do is read,
compute in code, and write back with no guard — that is the lost update, and it fails silently.

**"Does Postgres actually match the standard's table?"**
No, in three ways worth knowing. `READ UNCOMMITTED` is accepted syntax but behaves as read committed
— Postgres never exposes uncommitted rows, because MVCC always has a committed version to show
instead. Repeatable read is stronger than the standard requires: the standard permits phantoms at
that level, but a Postgres snapshot covers the whole transaction, so phantoms cannot occur either.
And serialisable is implemented as serialisable snapshot isolation — optimistic detection and abort —
rather than the range-locking the standard's authors had in mind, so its cost appears as retries, not
as blocking. The general lesson is that the standard defines levels by which anomalies they *forbid*,
and implementations are free to forbid more — so the answer to "what does repeatable read allow?" is
per-engine, and saying that is itself a good signal.

### A model answer

> "I'd pick the level per transaction, not for the database, and I'll say what I'm accepting in each
> case.
>
> For ordinary writes I'd stay at Postgres's default, read committed, and keep the arithmetic in
> SQL — `balance = balance - 5000` — so lost updates can't happen at any level. What I'm accepting is
> non-repeatable reads and phantoms inside multi-statement transactions, which for short writes
> touching one entity never bite.
>
> For anything shaped like check-then-act — book the seat if free, go off call if someone else is
> still on — read committed is not enough even with careful code, because of write skew: two
> transactions validate an invariant on their own views and write different rows, so nothing
> conflicts and the invariant still breaks. There I either lock what I check with
> `SELECT ... FOR UPDATE`, or run serialisable with a retry loop around the transaction, since
> Postgres enforces it optimistically and aborts losers with a serialization error. I'm accepting a
> retry rate, so those transactions must be side-effect-free — no emails from inside a transaction.
>
> For long reports I'd use repeatable read: one snapshot for the whole run, so every number in the
> report agrees with every other. I'm accepting staleness of a few minutes and the bloat cost of
> holding a snapshot open, which is why heavy reports belong on a replica.
>
> And if you asked me the difference between the read anomalies: a non-repeatable read is an existing
> row changing between two reads; a phantom is a new row appearing in a repeated search; a dirty read
> is seeing data that was never committed at all — which Postgres never allows at any level."

---

## 9. Recall card

- **Three read anomalies, in strength order:** dirty read (uncommitted data), non-repeatable read
  (same row, two answers), phantom (new rows appear in a repeated search). Plus the write one: the
  lost update.
- **The levels forbid them cumulatively:** read committed kills dirty; repeatable read kills
  non-repeatable; serialisable kills phantoms — and write skew.
- **Postgres: default read committed; repeatable read = one snapshot per transaction** and stops
  phantoms too; serialisable = SSI, aborts losers — **retry loop required**.
- **Write skew:** two snapshots, an invariant across rows, writes to *different* rows — no conflict
  fires. Fix with `FOR UPDATE` on what you checked, or serialisable.
- **Choose per transaction:** default + SQL arithmetic for writes, repeatable read for reports,
  serialisable (retried) for check-then-act. Say what you are accepting.
