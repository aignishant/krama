---
day: 33
track: system-design
title: "Transactions and ACID"
phase: "Databases from zero"
status: written
---

# Day 033 · System Design — Transactions and ACID

**After today you can:** You can explain each of the four ACID letters with a bank-transfer example.

**The interviewer asks it as:** *What does ACID stand for, and why does it matter?*

---

## 1. What this is, and why they ask it

A **transaction** is a group of database operations treated as one indivisible unit. Either all of them
take effect, or none of them do. You mark the boundaries yourself:

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 5000 WHERE id = 1;
  UPDATE accounts SET balance = balance + 5000 WHERE id = 2;
COMMIT;
```

Two statements, one transaction. If the process dies between them, neither happens. If another
connection looks while it is in progress, it sees neither.

**ACID** names the four guarantees a transaction gives you:

- **Atomicity** — all of it, or none of it.
- **Consistency** — the database's own rules are never violated.
- **Isolation** — concurrent transactions do not see each other's unfinished work.
- **Durability** — once it says committed, it survives a crash.

Interviewers ask this constantly, and it is one of the questions most often answered badly — not
because people cannot recite the four words, but because reciting is all they do. The answer that
lands names each letter, gives the **specific failure it prevents**, and says **what mechanism
delivers it**. And the most revealing follow-up is *"which of the four is the interesting one?"*, where
the answer is isolation, because it is the only one that is not simply on or off — it comes in levels,
which is [day 034](../day-034-at-most-k/README.md).

You have already met three of the four mechanisms. The write-ahead log from
[day 025](../day-025-pattern-matching/README.md) delivers atomicity and durability. Constraints from
[day 026](../day-026-strings-revision/README.md) deliver consistency. Today ties them together and
adds isolation.

---

## 2. The story

Sudhir decided to sell his scooter in March, and the man who wanted it was a stranger who had answered
the advertisement — perfectly pleasant, from two towns away, and completely unknown.

The problem they had is old and obvious. Sudhir was not going to hand over the keys and the papers and
then wait to see whether the money arrived. And the buyer was not going to hand over sixty-two thousand
rupees and then wait to see whether the papers turned up. Neither of them was being difficult. Each of
them was simply not prepared to be the one who went first.

What they did was go to a man who does vehicle transfers near the RTO, on a Tuesday morning, both of
them.

That man's whole job is that nothing happens until everything can happen. He took the papers from
Sudhir and put them on his side of the desk. He watched the buyer make the transfer on his phone and
waited for Sudhir's message to come. He checked the insurance was current and that there was no loan
outstanding on the vehicle, because a transfer with a loan on it is not a thing he is allowed to do.
And only when all of that was in front of him did he do the actual transfer — and then it was done,
all of it, in about four minutes.

Sudhir asked him what happens if something goes wrong in the middle. He said: then nothing has
happened. If the money does not come, he gives the papers back and everyone goes home and the scooter
is still Sudhir's. There is no state of affairs where the buyer owns half a scooter, or where the money
has moved and the papers have not.

And the third thing, which Sudhir only appreciated later. While it was going on, if somebody else had
rung him about the scooter, the honest answer was still that it was his. It did not become
half-sold. Right up to the moment it was done, it was one thing; after that moment, it was the other.

The papers came ten days later and the entry is in the government's records, and Sudhir says that is
the part he actually paid for. Not the four minutes. The fact that it is written down somewhere that
does not depend on anybody remembering.

---

## 3. The idea in plain English

The man at the RTO is the database. Everything he insisted on is one of the four letters.

### A — Atomicity: all of it, or none of it

*"There is no state of affairs where the money has moved and the papers have not."*

A transaction is indivisible. If any part fails — a constraint violation, a deadlock, the process being
killed — everything done so far is **rolled back**, and it is as though the transaction never ran.

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 5000 WHERE id = 1;
  -- process dies here
  UPDATE accounts SET balance = balance + 5000 WHERE id = 2;
COMMIT;
```

Without atomicity, ₹5,000 has vanished. With it, nothing happened at all.

**The mechanism is the write-ahead log.** Before changing anything, the database appends a record of
what it intends to do. On restart it reads the log: transactions that reached `COMMIT` are replayed,
and those that did not are undone. The word to use is **rollback**, and it is not a special error path
— it is the normal machinery.

### C — Consistency: the rules are never broken

*"He checked there was no loan outstanding, because a transfer with a loan on it is not a thing he is
allowed to do."*

A transaction moves the database from one valid state to another valid state. Every constraint you
declared — `NOT NULL`, `UNIQUE`, `CHECK`, foreign keys, from
[day 026](../day-026-strings-revision/README.md) — holds before and after. If a statement would break
one, the transaction fails and rolls back.

```sql
balance NUMERIC NOT NULL CHECK (balance >= 0)
```

Now a transfer that would overdraw an account cannot commit, whatever the application code believes.

**C is the odd letter out**, and saying so is a genuinely good signal. Atomicity, isolation and
durability are things the database *does*. Consistency is largely something **you** define — the
database enforces the rules you declared, and it has no opinion about rules you did not declare. Many
people argue the C is in the acronym mostly because ACID is a better word than AID.

### I — Isolation: nobody sees your half-finished work

*"If somebody else had rung him about the scooter, the honest answer was still that it was his."*

Concurrent transactions must not observe each other's intermediate states. Between the two `UPDATE`s
above, ₹5,000 genuinely does not exist in either account — and **no other transaction may ever see
that.**

The strongest form is **serialisable**: the result is as if the transactions had run one after another,
in some order. That is expensive, so real databases offer weaker levels that permit specific anomalies
in exchange for speed. Postgres defaults to **read committed**, which prevents dirty reads and permits
several other things.

**Isolation is the interesting letter**, because it is the only one with a dial. That dial —
and the four anomalies it trades against — is tomorrow's lesson.

### D — Durability: once committed, it stays committed

*"It is written down somewhere that does not depend on anybody remembering."*

When `COMMIT` returns successfully, the data survives a power cut, a kernel panic or a process kill. It
is not "probably written soon"; it is written.

**The mechanism is `fsync` on the write-ahead log.** The change is appended to the log and the operating
system is told to force it to physical storage *before* the commit is acknowledged. The actual data
pages are written later, in the background — because the log is written sequentially, which from
[day 025](../day-025-pattern-matching/README.md) is far faster than the random writes the data pages
would need.

That single design makes commits both **safe and fast**, which is a rare combination and the reason
write-ahead logging is in every serious database.

### The four, as one table

| Letter | Prevents | Mechanism | Failure without it |
|---|---|---|---|
| **Atomicity** | half-done work | write-ahead log, rollback | ₹5,000 vanishes mid-transfer |
| **Consistency** | invalid data | constraints, checked at commit | a negative balance is stored |
| **Isolation** | seeing others' unfinished work | locking, MVCC | a report totals money that is mid-flight |
| **Durability** | losing committed work | `fsync` on the log | the payment is confirmed and then lost |

### What a transaction is *not*

Two clarifications that come up:

**A transaction is not a lock on the whole database.** Two transactions touching different rows run in
parallel. Only conflicting access is serialised.

**A transaction is not free.** Holding one open takes resources, holds locks, and — under Postgres's
MVCC — prevents old row versions from being cleaned up. **A long-running transaction is one of the
classic production problems**: an idle-in-transaction connection can block `VACUUM` across the whole
database and cause table bloat that has nothing to do with the query it ran.

---

## 4. The picture

The transfer, with and without atomicity:

```
   WITHOUT a transaction                    WITH a transaction
   ---------------------                    ------------------
   UPDATE a: 10000 -> 5000    [written]     BEGIN
                                              UPDATE a: 10000 -> 5000  [in the log]
        *** process killed ***                     *** process killed ***
                                            (no COMMIT was reached)
   UPDATE b: never runs
                                            on restart: replay the log,
   state: a = 5000, b = 3000                find no COMMIT for this
          total 8000                        transaction, UNDO it
          ₹5,000 has vanished
                                            state: a = 10000, b = 3000
                                                   total 13000  — unchanged
```

**What to notice:** the left column has no error message anywhere. The money is simply gone, and the
only way anyone finds out is a reconciliation weeks later.

Where each letter acts, on one timeline:

```
   BEGIN
     |
     |  UPDATE accounts SET balance = balance - 5000 WHERE id = 1;
     |     -> appended to the write-ahead log         [ A, D ]
     |     -> row locked / new version created        [ I ]
     |     -> CHECK (balance >= 0) evaluated          [ C ]
     |
     |  UPDATE accounts SET balance = balance + 5000 WHERE id = 2;
     |     ... same four things ...
     |
     |  <-- other transactions see NEITHER update     [ I ]
     |
   COMMIT
     |  -> fsync the log to physical storage          [ D ]
     |  -> only THEN report success                   [ D ]
     |  -> now other transactions see BOTH            [ I ]
     v
   data pages written to disk later, in the background
```

**What to notice:** the `fsync` happens *before* `COMMIT` returns, and the data pages are written after.
That ordering is the whole of durability, and reversing it — reporting success first — is what "fast
but loses data on power failure" means.

The write-ahead log, and why it is fast as well as safe:

```
   the data pages that need changing:        the log:
   +----+   +----+   +----+   +----+         +--------------------------------+
   |page|   |page|   |page|   |page|         | txn 88: a -= 5000              |
   |1092|   | 47 |   |8801|   | 312|         | txn 88: b += 5000              |
   +----+   +----+   +----+   +----+         | txn 88: COMMIT                 |
      ^        ^        ^        ^           +--------------------------------+
      scattered: 4 RANDOM writes                        one SEQUENTIAL append

   random 8 KB writes to SSD : ~15,000/second
   sequential writes to SSD  : ~60,000 8 KB writes/second

   So: append to the log, fsync THAT, report success.
       Write the scattered pages later, lazily, batched.
```

---

## 5. How it actually works

### Writing one

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 5000 WHERE id = 1;
  UPDATE accounts SET balance = balance + 5000 WHERE id = 2;
  INSERT INTO transfers (from_id, to_id, amount) VALUES (1, 2, 5000);
COMMIT;
```

Three statements, one unit. Note the third: the audit record is inside the transaction, so there can
never be a transfer row without the balance changes or the reverse.

Two rules worth stating:

**Do the arithmetic in the database, not in your application.** `SET balance = balance - 5000` is one
atomic operation. Reading the balance, subtracting in Python and writing it back is a **lost update** —
two concurrent transfers each read 10,000, each write 5,000, and one transfer vanishes. That is
[day 025](../day-025-pattern-matching/README.md)'s lost update, and a transaction alone does not
prevent it at Postgres's default isolation level.

**Keep transactions short.** No network calls to third parties inside one, no waiting for user input,
no sleeping. Every held lock is a queue behind you.

### What actually happens on `COMMIT`

1. All the changes are already in the write-ahead log buffer in memory.
2. `fsync` — the operating system is told to force the log to physical storage and to wait until it has
   happened.
3. Only now is `COMMIT` reported as successful.
4. The modified data pages are written from the buffer pool to their real locations later, at a
   checkpoint.

Step 2 is the expensive one — it is a physical write barrier, and it is why commit latency is roughly
one disk sync. **Group commit** amortises it: many transactions committing at nearly the same moment
share one `fsync`, so throughput can be far higher than one commit per sync.

`synchronous_commit = off` in Postgres skips the wait — commits return before the log is durable. That
makes writes dramatically faster and means a power failure can lose the last fraction of a second of
committed transactions. **It is a real, deliberate setting for data where that is acceptable**, and
knowing it exists, and what exactly it trades, is a good signal.

### `ROLLBACK`, and how it happens without you

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 5000 WHERE id = 1;
  UPDATE accounts SET balance = balance - 999999 WHERE id = 2;  -- violates CHECK
COMMIT;
```

The second statement raises, the transaction is aborted, and **the first update is undone too**. In
Postgres, once a statement errors inside a transaction, every subsequent statement fails with *current
transaction is aborted* until you `ROLLBACK` — which surprises people the first time and is exactly
the guarantee working.

**Savepoints** allow partial rollback when you genuinely want it:

```sql
BEGIN;
  INSERT INTO orders ...;
  SAVEPOINT after_order;
  INSERT INTO notifications ...;     -- if this fails, keep the order
  ROLLBACK TO after_order;
COMMIT;
```

Use them sparingly; they are usually a sign the transaction is doing two jobs.

### MVCC, and why readers do not block

Postgres, Oracle and MySQL's InnoDB use **multi-version concurrency control**. An `UPDATE` does not
overwrite the row — it writes a **new version** and marks the old one as valid up to this transaction's
id. Each transaction sees the versions that were committed when it started.

The consequences are worth knowing:

- **Readers never block writers, and writers never block readers.** That is the single biggest reason
  these databases perform well under mixed load.
- **Two writers to the same row still conflict** — the second waits for the first to commit or roll
  back.
- **Old versions accumulate** and must be cleaned up, which is `VACUUM`. A long-running transaction
  holds back the cleanup horizon for the *whole database*, which is why an idle-in-transaction
  connection can bloat tables it never touched.

### Distributed transactions, and why they are avoided

A transaction across two databases needs **two-phase commit**: a coordinator asks everyone to prepare,
and if all say yes, tells everyone to commit.

It works and it is avoided, because if the coordinator dies between the two phases, every participant
is left holding locks and unable to decide. In a microservice architecture the usual answer is the
**saga** pattern — a sequence of local transactions, each with a compensating action to undo it — which
gives you eventual consistency and explicit undo instead of atomicity. Sagas arrive later in the
course; naming them here is enough.

### Which stores give you this

**Full ACID:** PostgreSQL, MySQL with InnoDB, Oracle, SQL Server, SQLite.

**ACID within a limit:** MongoDB has multi-document transactions since 4.0 but they are discouraged at
scale. DynamoDB has transactions across up to 100 items. Cassandra has none across partitions —
lightweight transactions are a single-partition compare-and-set.

**Redis** has `MULTI`/`EXEC`, which is atomic in the sense that commands are not interleaved — but there
is **no rollback**: if one command in the block fails, the others still apply. It is worth being precise
about that, because people call it a transaction and it is not an ACID one.

---

## 6. The numbers

### What a commit costs

```
fsync to SSD          ≈ 0.5 - 1 ms
fsync to spinning disk ≈ 5 - 10 ms

so, naively, one commit per fsync:
   SSD  : ~1,000 - 2,000 commits/second
   HDD  : ~100 - 200 commits/second
```

With **group commit**, transactions arriving within the same window share one `fsync`:

```
100 transactions sharing one 1 ms fsync -> effective 100,000 commits/second
```

Which is why real throughput on a single Postgres instance is tens of thousands of small transactions a
second and not one thousand. **That gap between the naive figure and the real one is the thing to be
able to explain.**

### `synchronous_commit = off`

```
on  : commit waits for fsync   -> ~1 ms latency, zero data loss
off : commit returns first     -> ~0.05 ms latency, up to ~600 ms of committed
                                  transactions lost on a power failure
```

**About 20× faster writes**, in exchange for a bounded window of loss. Right for analytics ingestion or
click tracking; wrong for payments.

### Transaction size

```
1,000 rows, one transaction each  : 1,000 commits × 1 ms fsync  = 1,000 ms
1,000 rows, one transaction total : 1 commit                    ≈    15 ms
                                                                  about 60x
```

**Batching writes into one transaction is one of the largest easy wins there is**, and it is the answer
to "the import is slow".

But there is an opposite limit:

```
1,000,000 rows in one transaction:
  - holds locks for the whole duration
  - the entire change must be undoable, so undo information grows
  - one failure at row 999,999 discards everything
  - blocks VACUUM for the whole database while it runs
```

**Batch in chunks of a few thousand**, not one row and not a million.

### The cost of a long transaction

```
a transaction left open for 4 hours:
  - VACUUM cannot remove any row version created in those 4 hours,
    ANYWHERE in the database
  - a table taking 10,000 updates/second for 4 hours accumulates
    144,000,000 dead row versions
  - at ~100 bytes each: ~14 GB of bloat from ONE idle connection
```

That number is worth carrying, because "an idle-in-transaction connection bloated the database" sounds
implausible until you multiply it out.

### Lock waiting

```
transaction A holds a row lock for 100 ms
99 other transactions want the same row

serialised: 99 × 100 ms = 9.9 seconds for the last one
```

Which is why "keep transactions short" is a throughput statement, not tidiness. **Never put an HTTP
call to a payment provider inside a transaction** — you have just made every other writer wait for a
third party's latency.

---

## 7. The trade-offs

### Durability against write latency

`synchronous_commit = on` is roughly 20× slower and loses nothing. `off` is fast and can lose a
fraction of a second of acknowledged commits on power loss. There is a middle setting, `remote_write`,
which waits for a replica to have received the log but not necessarily flushed it.

**Choose by what the data is.** Payments, orders and anything a person will complain about: `on`.
Metrics, clickstream, cache warming: `off` is defensible and the speed is real.

### Transaction size

Too small and you pay an `fsync` per row — 60× slower on a bulk import. Too large and you hold locks
for minutes, generate huge undo, block `VACUUM` and lose everything if the last row fails. **A few
thousand rows per transaction is the usual sweet spot**, and the shape of that curve is worth knowing.

### Isolation strength against concurrency

Stronger isolation means more locking or more aborted transactions, and therefore less throughput.
Serialisable is correct and slow; read committed is fast and permits anomalies you must think about.
**That is tomorrow's entire lesson**, and the honest position is that most applications run at read
committed and handle the specific anomalies that matter to them explicitly.

### ACID against distributed scale

Two-phase commit across services is technically possible and operationally miserable — a coordinator
failure leaves participants stuck holding locks. Sagas replace atomicity with compensating actions:
each step commits locally and has a defined undo. **You give up "all or nothing" and get "eventually
all, or eventually undone", with the undo written by you.**

### The sentence that separates candidates

> **I would not put a call to an external service inside a transaction.** The transaction holds locks
> for its entire lifetime, so a payment provider having a slow afternoon becomes every other writer in
> my system waiting on their latency — and a transaction open for hours stops `VACUUM` reclaiming dead
> rows across the whole database, which is how one idle connection bloats tables it never touched. The
> pattern I would use instead is to commit the local state first, then make the external call outside
> the transaction, and reconcile with an idempotency key — which is
> [day 018](../day-018-arrays-revision/README.md)'s answer arriving here for a different reason.

---

## 8. In the interview

### How it gets asked

- *"What does ACID stand for?"* — the definition, and the answer that lands attaches a failure and a
  mechanism to each letter.
- *"Walk me through a bank transfer."* — the canonical example. Two updates, one transaction.
- *"Which of the four is the interesting one?"* — isolation, because it has levels.
- *"How does the database actually guarantee durability?"* — the write-ahead log and `fsync`.
- *"Two users transfer money at the same time. What goes wrong?"* — the lost update, which a transaction
  alone does not prevent at the default isolation level.

### What to say out loud, in the first ninety seconds

1. **Define a transaction before the acronym.** *"A transaction is a group of operations treated as one
   indivisible unit — all of them take effect or none do."*
2. **Give each letter with a failure attached.** *"Atomicity: the transfer can't leave money debited and
   not credited. Consistency: it can't leave a negative balance if I declared that constraint.
   Isolation: nobody else sees the moment when the money is in neither account. Durability: once commit
   returns, a power cut can't undo it."*
3. **Name the mechanism for each.** *"Atomicity and durability both come from the write-ahead log —
   append the intent, fsync it, and only then report success. Consistency is the constraints I
   declared. Isolation is locking, or MVCC."*
4. **Say which letter is odd.** *"Consistency is arguably the odd one out — the other three are things
   the database does, and consistency is mostly rules I define and it enforces."*
5. **Say which is interesting.** *"Isolation is the one worth talking about, because it's the only one
   with a dial. The others are on or off; isolation has levels, and each level permits specific
   anomalies."*
6. **Give the practical rule.** *"And in practice the thing that matters most is keeping transactions
   short — no external calls inside one, because you're holding locks the whole time."*

### The follow-ups

**"How does the database actually guarantee durability?"**
With a write-ahead log. Before changing any data page, it appends a description of the change to a log
file, and on `COMMIT` it calls `fsync` to force that log to physical storage and waits for the operating
system to confirm — only then does the commit return successfully. The actual data pages are written
later, in the background at a checkpoint. That ordering is the whole guarantee: if the machine loses
power, the log is replayed on restart, transactions that reached commit are reapplied and those that did
not are undone. The design is also *faster*, not just safer, because the log is written sequentially
while the data pages are scattered — roughly four times the throughput on an SSD — and because many
transactions committing at once can share a single `fsync`, which is called group commit and is why a
single instance does tens of thousands of commits a second rather than the thousand you would get from
one `fsync` each.

**"Which of the four letters is the most interesting, and why?"**
Isolation, because it is the only one that comes in degrees. Atomicity, durability and consistency are
essentially on or off — a database either rolls back partial work or it does not. Isolation has levels,
because full serialisability is expensive, so databases offer weaker ones that permit specific,
named anomalies in exchange for concurrency: dirty reads, non-repeatable reads, phantom reads, and lost
updates. Postgres defaults to read committed, which prevents dirty reads and permits the rest. So
choosing an isolation level is a real design decision with real consequences, and the anomalies it
allows are things you then have to handle in the application — typically with explicit locking, or by
doing the arithmetic in the database rather than in application code.

**"Two users transfer money from the same account at the same time. What happens?"**
It depends entirely on how the update is written, and this is where a transaction alone is not enough.
If I write `UPDATE accounts SET balance = balance - 5000 WHERE id = 1`, the database performs the
arithmetic itself under a row lock, so the two transfers serialise and both are applied correctly. If
instead the application reads the balance, subtracts in code, and writes the result back, then at
Postgres's default read-committed level both transactions can read 10,000, both compute 5,000, and both
write it — one transfer disappears with no error. That is a lost update, and being inside a transaction
does not prevent it. The fixes are to do the arithmetic in the SQL, to take an explicit lock with
`SELECT ... FOR UPDATE`, to use optimistic locking with a version column, or to raise the isolation
level to repeatable read so the second transaction is aborted and can retry.

**"Why not just use transactions everywhere, across services too?"**
Because across a network the guarantee gets very expensive. Within one database it is nearly free —
locks are local and the coordinator is the database itself. Across two databases you need two-phase
commit: a coordinator asks every participant to prepare, and if all agree, tells them to commit. The
problem is the window between the two phases — if the coordinator dies there, every participant is
holding locks and cannot decide on its own whether to commit or abort, so it blocks, potentially
indefinitely. In practice most systems avoid it and use sagas instead: a sequence of local transactions,
each with a compensating action that undoes it. You trade atomicity for eventual consistency plus
explicit undo logic that you have to write and test — and you accept that there are moments when the
system is visibly half-done, which the business has to be able to tolerate.

### A model answer

> "A transaction is a group of database operations treated as one indivisible unit — all of them happen
> or none do — and ACID names the four guarantees it gives you. The clearest example is a bank transfer,
> which is two updates: subtract from one account, add to the other.
>
> **Atomicity** is that there is no state where the money has left one account and not arrived in the
> other. If the process dies between the two updates, the whole thing is rolled back and it is as if
> nothing ran. The mechanism is the write-ahead log: on restart the database replays the log, reapplies
> anything that reached commit, and undoes anything that did not.
>
> **Consistency** is that the database's own rules hold before and after. If I declared `CHECK (balance
> >= 0)`, a transfer that would overdraw the account cannot commit, regardless of what the application
> code thinks. I'd add that C is arguably the odd letter out — the other three are things the database
> does for you, and consistency is mostly rules you define and it enforces.
>
> **Isolation** is that no other transaction sees the moment in the middle when the ₹5,000 is in neither
> account. A report running concurrently either sees both updates or neither, never one.
>
> **Durability** is that once `COMMIT` returns, a power cut cannot undo it. The mechanism is that the
> log is `fsync`ed to physical storage *before* the commit is acknowledged — the data pages themselves
> are written later in the background, which is both safer and faster, because the log is a sequential
> append while the data pages are scattered.
>
> If you asked which of the four is worth talking about, I'd say isolation, because it's the only one
> with a dial. The others are on or off. Isolation has levels — read committed, repeatable read,
> serialisable — and each weaker level permits specific anomalies in exchange for concurrency, which
> becomes something you have to handle deliberately.
>
> And the practical thing I'd add: keep transactions short. They hold locks for their whole lifetime, so
> an external HTTP call inside one makes every other writer wait on a third party's latency — and a
> transaction left open for hours prevents `VACUUM` from cleaning up dead row versions across the entire
> database, which is how a single idle connection ends up bloating tables it never touched."

---

## 9. Recall card

- **A transaction is one indivisible unit.** `BEGIN` … `COMMIT`, and all of it or none of it.
- **A**tomicity and **D**urability both come from the **write-ahead log**: append the intent, `fsync`,
  *then* report success.
- **C**onsistency is the constraints you declared — the odd letter out, since you define it and the
  database enforces it.
- **I**solation is the interesting one, because it is the only one with **levels** — that is
  [day 034](../day-034-at-most-k/README.md).
- **Keep transactions short.** No external calls inside one; batch bulk writes in thousands, not one at
  a time and not a million.
