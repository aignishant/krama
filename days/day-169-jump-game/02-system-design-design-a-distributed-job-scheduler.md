---
day: 169
track: system-design
title: "Design a distributed job scheduler"
phase: "High-level design case studies"
status: written
---

# Design a distributed job scheduler

## 1. What this is, and why they ask it

A job scheduler runs work at a specified time. **"Send this email at 09:00 tomorrow." "Run this report every
night at two." "Retry this webhook in five minutes."**

They ask it because **it is the infrastructure every company builds and almost nobody gets right the first
time**, and because the difficulties are not where people expect them.

**The scheduling is easy.** A sorted structure keyed by run time, and a loop that pulls whatever is due. **That
part is twenty lines.**

**What is hard is everything about failure.** A worker picks up a job and dies halfway through — **is the job
lost, or run twice?** A job runs for six hours — **how do you know it is still alive rather than stuck?** A
scheduler instance is partitioned from the network but still running — **does another instance take over, and
do they both then run everything?**

**And the second hard thing is that "exactly once" is not available and the honest design says so.** You get
at-least-once with idempotent jobs, or at-most-once with the risk of loss. **Choosing which, per job, and
saying why, is the interview.**

**The third is a scale detail that catches people: a hundred million jobs all scheduled for 09:00.** Everything
in the system is fine until the thundering herd at the top of the hour, **and the fix is jitter, which is one
line and is never in the first design.**

By the end of this lesson you can design the store and the polling loop, handle leases and worker death,
support recurring jobs, avoid the herd, and say precisely what delivery guarantee you are offering.

---

## 2. The story

The hospital had a diary on the counter of the nurses' station and everything that had to happen at a
particular time was written in it.

**Injections at six. Dressings at ten. The dialysis lot at two.**

And for eleven years the system was that whoever was on duty read the diary, **and the trouble was never the
reading.**

**The first trouble was the handover.**

Because a nurse would look at ten o'clock, see four dressings, start the first one — **and go off shift.** And
the next nurse would look at ten o'clock, see four dressings, and start the first one.

**Which was done. And bed eleven got two dressings and bed fourteen got none.**

**The fix was a pencil tick, and it took an argument to introduce.** You ticked the line **when you started**,
not when you finished, **and you wrote your initials.**

Then the second trouble, which took a year.

**A nurse ticked a line, started, and was called to something else and did not come back.** And the tick said
somebody was doing it, **so nobody else did**, and at four o'clock in the afternoon somebody noticed.

**The rule they added was a time next to the tick.** If your initials had been against a line for more than an
hour, **anybody could rub it out and take it.**

Which caused the third trouble almost immediately, **because some things genuinely took two hours**, and the
nurse doing them would come back to find somebody else halfway through.

**So the tick had to be renewed.** You came back to the station, and you moved the time along, **and that
meant you were still on it.**

**And the fourth thing was the one nobody planned for.**

Because eleven years of "everything at six, everything at ten, everything at two" meant that at six o'clock
there were nineteen things to do and at seven o'clock there were none.

**The ward sister who fixed it did not change the medicine.** She changed the diary. **She wrote things at
five past, and ten past, and quarter past** — the same medicines, the same intervals, **spread across the
hour.**

**"It was never that we had too much work," she said. "It was that we had written it all down at the same
time."**

---

## 3. The idea in plain English

The nurses' diary is the job store, the tick is a lease, the time next to it is the lease expiry, renewing it
is the heartbeat, and the ward sister's fix is jitter. **Those five things are the design.**

**Start with the model, because the vocabulary matters.**

```
   JOB          what to run, and with what arguments
   SCHEDULE     when: once at a time, or a repeating rule
   RUN          one attempt at executing a job
   LEASE        a claim on a run, held by one worker, with an expiry
```

**A job is not a run.** A daily report is one job and three hundred and sixty-five runs a year — **and
conflating them is the modelling mistake that makes recurring jobs painful later.**

**Now the store, which is a sorted structure keyed by time.**

**"What is due?" is the only query that matters**, so the schema is built around it:

```sql
CREATE TABLE runs (
    id           BIGINT PRIMARY KEY,
    job_id       BIGINT NOT NULL,
    run_at       TIMESTAMPTZ NOT NULL,
    state        TEXT NOT NULL,        -- pending, leased, done, failed
    lease_until  TIMESTAMPTZ,
    attempt      INT NOT NULL DEFAULT 0
);
CREATE INDEX ON runs (state, run_at);
```

**One index on `(state, run_at)` and the whole scheduling problem is a range query** — `WHERE state = 'pending'
AND run_at <= now()`.

**And a relational database is genuinely the right answer here for most systems**, because the volume is
modest and you need transactions.

**Now claiming work, which is where the correctness is.**

**Two workers must not run the same job.** A `SELECT` followed by an `UPDATE` is a race — **both see it
pending, both claim it.**

**The claim must be one atomic operation:**

```sql
UPDATE runs
   SET state = 'leased', lease_until = now() + interval '60 seconds',
       worker = %(me)s, attempt = attempt + 1
 WHERE id IN (
     SELECT id FROM runs
      WHERE state = 'pending' AND run_at <= now()
      ORDER BY run_at
      LIMIT 10
      FOR UPDATE SKIP LOCKED          -- the important part
 )
RETURNING *;
```

**`FOR UPDATE SKIP LOCKED` is the line that makes this scale.** Without it, ten workers polling simultaneously
**all block on the same rows** and the throughput is that of one worker. **With it, each worker takes rows
nobody else has locked and moves on** — no coordination, no contention.

**Then the lease, which is the nurses' tick with a time on it.**

**A worker that dies mid-job must not hold the job forever.** So the claim carries an expiry, **and an expired
lease means the run is available again.**

**And the renewal is what handles long jobs.** A worker running a six-hour job **extends its lease
periodically** — a heartbeat — so the job is not stolen while it is genuinely progressing.

**Which produces the fundamental trade, and it is worth stating precisely:**

```
   SHORT LEASE   dead workers are detected fast
                 a slow-but-alive worker gets its job STOLEN and it runs TWICE

   LONG LEASE    slow workers are safe
                 a dead worker's job sits idle for the whole lease
```

**And there is no setting that avoids both**, because **you cannot distinguish a dead worker from a slow one
over a network.** That is the same failure-detection result that made presence hard in chat, applied to
work instead of people.

**So the honest answer is: heartbeat to make the lease short *and* safe**, and accept that a worker partitioned
from the database will have its job taken while still running it.

**Which brings the delivery guarantee, and this is the thing to be precise about.**

**Exactly-once execution is not available.** The worker can finish the work and die before recording that it
did. **You cannot make "do the thing" and "record that I did the thing" atomic when the thing is an external
side effect.**

**So there are two honest choices, per job:**

**At-least-once** — mark the run complete *after* the work. **A crash between them means it runs again.**
**This is the default, and it requires the job to be idempotent.**

**At-most-once** — mark it complete *before* the work. **A crash means it never runs.** Correct for anything
where a duplicate is worse than a miss, and rare.

**And "make the job idempotent" is the actual answer**, exactly as it was for payments and notifications: **an
idempotency key derived from `(job_id, scheduled_time)`**, checked by whatever the job touches.

**Then recurring jobs, where the modelling matters.**

**Do not store "every day at 09:00" as a single row you keep updating.** **Store the *rule* on the job, and
materialise the next run as its own row** — created when the previous one completes.

**Two properties follow, and both are worth having.** **A history**: every past run is a row, with its
outcome. **And no drift**: the next run is computed from the schedule, not from when the last one finished.

**And the awkward question: what if a run is late — do you catch up?** A nightly report that was missed for
three days: **run it three times, or once?** **There is no default answer**, and the honest design makes it a
per-job policy with a "do not run more than N missed occurrences" bound.

**Then the herd, which is the ward sister's problem.**

**Everybody schedules things at the top of the hour.** Nine o'clock, midnight, the start of the month. **A
hundred million jobs at 09:00:00 is a spike that no amount of capacity planning survives**, because the average
rate is fine and the instantaneous rate is not.

**Two fixes, both trivial.** **Jitter**: spread each job by a random offset within an acceptable window —
**"at 09:00" becomes "between 09:00 and 09:05"**, which is almost always acceptable and removes the spike
entirely. **And rate-limited dispatch**: the scheduler pulls at a bounded rate regardless of how much is due,
so the backlog drains smoothly instead of arriving at once.

**Finally, the scaling shape, which is not what people expect.**

**The scheduler is small.** Even a hundred million scheduled jobs a day is about a thousand a second —
**an ordinary database workload.** The polling loop is a query every second.

**The workers are where the capacity is**, and they scale horizontally because `SKIP LOCKED` means they need
no coordination at all.

**And the one thing that does need care at very large scale is the poll itself**, because every scheduler
instance querying the same index every second is contention on one hot range. **Partitioning the run table by
time bucket, or sharding by job id, removes it** — and at most realistic scales it is not needed.

---

## 4. The picture

Job, schedule, run — three things, not one:

```
   JOB  "send the weekly report"
        + SCHEDULE "every Monday at 09:00"
        |
        +--> RUN  2026-08-31 09:00   state: done      attempt 1
        +--> RUN  2026-09-07 09:00   state: done      attempt 2 (retried)
        +--> RUN  2026-09-14 09:00   state: pending   <- materialised
                                                         when the last
                                                         one completed

   ONE job, MANY runs.

   Conflating them — one row you keep updating — costs you the
   history AND makes retries impossible to model.
```

Claiming work without a race:

```
   BROKEN — select then update

     worker A: SELECT ... WHERE state='pending'  -> job 42
     worker B: SELECT ... WHERE state='pending'  -> job 42     <- both see it
     worker A: UPDATE 42 SET state='leased'
     worker B: UPDATE 42 SET state='leased'
     -> BOTH RUN JOB 42

   CORRECT — one atomic statement

     UPDATE runs SET state='leased', lease_until=now()+60s, worker=me
      WHERE id IN (SELECT id FROM runs
                    WHERE state='pending' AND run_at <= now()
                    ORDER BY run_at LIMIT 10
                    FOR UPDATE SKIP LOCKED)
     RETURNING *

   `SKIP LOCKED` IS WHAT MAKES IT SCALE:
     without it, 10 workers all BLOCK on the same rows
       -> throughput of ONE worker
     with it, each takes rows nobody else holds
       -> no coordination at all, workers scale horizontally
```

The lease, and the trade with no good setting:

```
   worker claims job 42, lease_until = now + 60s
        |
        +-- finishes in 10s     -> mark done, lease irrelevant
        |
        +-- still working at 50s -> HEARTBEAT: extend the lease
        |
        +-- dies at 20s          -> at 60s the lease EXPIRES
                                    -> another worker claims it
                                    -> the job runs (again)

   THE TRADE:

     SHORT LEASE (10s)     dead workers detected fast
                           a slow-but-alive worker gets its job STOLEN
                           -> the job runs TWICE

     LONG LEASE (1 hour)   slow workers are safe
                           a dead worker's job sits idle for an hour

   AND THERE IS NO SETTING THAT AVOIDS BOTH, because you cannot
   distinguish a DEAD worker from a SLOW one over a network.

   The mitigation is the HEARTBEAT: short leases, renewed while
   genuinely working.
```

Why exactly-once is not available:

```
   do the work                    mark it done
   ------------                   ------------
        |                              |
        +-- crash HERE ----------------+

   the side effect HAPPENED and the record does NOT exist

   AT-LEAST-ONCE:  mark done AFTER the work
                   crash -> it runs AGAIN
                   -> requires the job to be IDEMPOTENT
                   -> THE DEFAULT

   AT-MOST-ONCE:   mark done BEFORE the work
                   crash -> it NEVER runs
                   -> correct only when a duplicate is worse
                      than a miss

   "EXACTLY ONCE" would need the side effect and the record to be
   ATOMIC — and the side effect is in somebody else's system.

   -> the real answer is: at-least-once + an idempotency key
      derived from (job_id, scheduled_time)
```

The thundering herd, and the one-line fix:

```
   WITHOUT JITTER

   jobs due:    09:00:00  ################################  100,000,000
                09:00:01
                09:00:02
                ...
                09:04:59

   -> the average rate is fine; the INSTANTANEOUS rate is not
   -> every worker wakes, the database is hammered, everything
      times out, and the retries make it worse


   WITH JITTER (spread over 5 minutes)

   09:00:00  ####
   09:00:30  ####
   09:01:00  ####      ~333,000 per second, evenly
   ...
   09:04:30  ####

   ONE LINE:  run_at = scheduled + random(0, jitter_window)

   "It was never that we had too much work. It was that we had
    written it all down at the same time."
```

Where the capacity actually is:

```
   THE SCHEDULER                  THE WORKERS

   100,000,000 jobs/day           the actual work: sending emails,
   = ~1,200/second                generating reports, calling webhooks
   one indexed range query
   per second                     -> seconds to hours each
                                  -> THIS is where the machines are
   -> AN ORDINARY DATABASE
      WORKLOAD                    -> and they scale horizontally,
                                     because SKIP LOCKED means they
   -> the scheduling is NOT          need no coordination
      the hard part
```

---

## 5. How it actually works

### The schema

```sql
CREATE TABLE jobs (
    id        BIGINT PRIMARY KEY,
    payload   JSONB NOT NULL,
    schedule  TEXT,                     -- a cron expression, or NULL for one-off
    max_attempts INT NOT NULL DEFAULT 3,
    jitter_seconds INT NOT NULL DEFAULT 0
);

CREATE TABLE runs (
    id           BIGINT PRIMARY KEY,
    job_id       BIGINT NOT NULL REFERENCES jobs(id),
    run_at       TIMESTAMPTZ NOT NULL,
    state        TEXT NOT NULL,         -- pending, leased, done, failed
    lease_until  TIMESTAMPTZ,
    worker       TEXT,
    attempt      INT NOT NULL DEFAULT 0,
    UNIQUE (job_id, run_at)             -- one run per job per scheduled time
);

CREATE INDEX ON runs (state, run_at) WHERE state IN ('pending', 'leased');
```

**`UNIQUE (job_id, run_at)` is the line that prevents duplicate scheduling** — two scheduler instances both
materialising the next run of a recurring job **cannot both succeed.**

**And the partial index — only `pending` and `leased`** — keeps it small: **completed runs are the vast
majority of the table and are never queried by the polling loop.**

### Claiming work

```python
LEASE_SECONDS = 60

def claim(worker_id: str, batch: int = 10) -> list[dict]:
    """One atomic statement. SKIP LOCKED is what makes workers scale."""
    return db.query("""
        UPDATE runs
           SET state = 'leased',
               lease_until = now() + interval '%(lease)s seconds',
               worker = %(worker)s,
               attempt = attempt + 1
         WHERE id IN (
             SELECT id FROM runs
              WHERE state = 'pending' AND run_at <= now()
              ORDER BY run_at
              LIMIT %(batch)s
              FOR UPDATE SKIP LOCKED
         )
        RETURNING id, job_id, attempt
    """, {"lease": LEASE_SECONDS, "worker": worker_id, "batch": batch})
```

**`FOR UPDATE SKIP LOCKED` is the whole scaling story.** Without it, **ten workers polling at the same moment
all queue behind the same rows** and the system's throughput is one worker's. **With it, each takes what nobody
else holds.**

**`attempt = attempt + 1` on the claim rather than on completion** matters: **a worker that dies has already
consumed an attempt**, which is what stops an infinitely-crashing job retrying forever.

**And `ORDER BY run_at` inside the subquery makes it fair** — the oldest due work goes first, so a backlog
drains in order rather than starving old jobs.

### The lease heartbeat

```python
def heartbeat(run_id: int, worker_id: str) -> bool:
    """Extend the lease while genuinely working. Returns False if it was stolen."""
    rows = db.execute("""
        UPDATE runs
           SET lease_until = now() + interval '%(lease)s seconds'
         WHERE id = %(id)s AND worker = %(worker)s AND state = 'leased'
    """, {"lease": LEASE_SECONDS, "id": run_id, "worker": worker_id})
    return rows == 1
```

**`AND worker = %(worker)s` is what makes this safe.** If the lease expired and another worker took the run,
**this update affects zero rows and returns `False`** — **and the original worker must then stop**, because
somebody else is now running it.

**A heartbeat that does not check ownership will happily extend a lease it no longer holds**, and then two
workers both believe they own the run.

### Executing a run

```python
def execute(run: dict, worker_id: str) -> None:
    job = job_store.get(run["job_id"])
    idempotency_key = f"job:{run['job_id']}:{run['run_at']}"

    stop = threading.Event()
    threading.Thread(target=_heartbeat_loop,
                     args=(run["id"], worker_id, stop), daemon=True).start()
    try:
        handler(job["payload"], idempotency_key=idempotency_key)
        complete(run["id"], worker_id, "done")           # AFTER the work
    except Exception as error:
        if run["attempt"] >= job["max_attempts"]:
            complete(run["id"], worker_id, "failed", str(error))
        else:
            reschedule(run["id"], worker_id, backoff(run["attempt"]))
    finally:
        stop.set()
```

**`complete` after the work is what makes this at-least-once.** **A crash between the two means the run
executes again** — which is why the idempotency key is passed to the handler.

**And the key is derived from `(job_id, run_at)`**, not generated per attempt: **a retry must carry the same
key**, or deduplication downstream does nothing.

**The heartbeat runs on its own thread** because the work is blocking, **and `finally: stop.set()` guarantees
it stops** even when the handler throws.

### Reclaiming expired leases

```python
def reclaim_expired() -> int:
    """A dead worker's lease lapses and the run becomes available again."""
    return db.execute("""
        UPDATE runs
           SET state = 'pending', worker = NULL, lease_until = NULL
         WHERE state = 'leased' AND lease_until < now()
    """)
```

**This is the only thing that recovers from a dead worker**, and it needs no failure detection — **the absence
of a heartbeat is the signal**, exactly as with presence and distributed locks.

**And it must be idempotent and safe to run from several scheduler instances**, which the conditional `WHERE`
makes it: **a run already reclaimed by another instance no longer matches.**

### Recurring jobs

```python
from croniter import croniter

def materialise_next(job_id: int, after: datetime) -> None:
    """Compute the next run from the SCHEDULE, not from when the last finished."""
    job = job_store.get(job_id)
    if not job["schedule"]:
        return
    next_at = croniter(job["schedule"], after).get_next(datetime)
    if job["jitter_seconds"]:
        next_at += timedelta(seconds=random.randint(0, job["jitter_seconds"]))
    db.execute("""
        INSERT INTO runs (id, job_id, run_at, state)
        VALUES (%(id)s, %(job)s, %(at)s, 'pending')
        ON CONFLICT (job_id, run_at) DO NOTHING
    """, {"id": snowflake.next_id(), "job": job_id, "at": next_at})
```

**`croniter(schedule, after)` computes from the *schedule*, not from now** — **so a job that ran late does not
drift.** A daily job delayed by twenty minutes still runs at nine tomorrow, not at nine twenty.

**And `ON CONFLICT DO NOTHING` against the unique constraint** means **two scheduler instances materialising
the same next run is harmless** — one wins, the other is a no-op.

### Jitter, which is one line

```python
def schedule_with_jitter(job_id: int, at: datetime, window_seconds: int) -> datetime:
    """'At 09:00' becomes 'between 09:00 and 09:05'."""
    return at + timedelta(seconds=random.randint(0, window_seconds))
```

**One line, and it removes the entire thundering-herd problem** — which is why it is worth naming as a design
decision rather than a detail.

**The window is a product question**: "send at nine" usually tolerates five minutes; **"expire this token at
nine" does not**, so jitter is per job and defaults to zero.

### Missed runs, which need a policy

```python
CATCH_UP_LIMIT = 3

def handle_missed(job_id: int, now: datetime) -> list[datetime]:
    """
    A nightly job missed for three days: run it three times, or once?
    There is no default answer. Make it a per-job policy.
    """
    job = job_store.get(job_id)
    policy = job.get("catch_up", "skip")
    missed = list(missed_occurrences(job["schedule"], job["last_run"], now))
    if policy == "skip":
        return missed[-1:]                    # only the most recent
    if policy == "all":
        return missed[-CATCH_UP_LIMIT:]       # bounded, or an outage floods
    return []                                 # "none": drop them
```

**The bound on `all` is not optional.** **A job that was down for a week with an hourly schedule would
otherwise materialise a hundred and sixty-eight runs at once** — a self-inflicted herd, at exactly the moment
the system is recovering.

### Backoff for retries

```python
def backoff(attempt: int) -> int:
    """Exponential, capped, with jitter — the same rule as everywhere else."""
    base = min(2 ** attempt, 3600)
    return base + random.randint(0, base // 2)
```

**Jitter here for the same reason as in scheduling**: **without it, a hundred jobs that failed together retry
together**, and the failure repeats.

### The scheduler loop

```python
def scheduler_loop(worker_id: str) -> None:
    while True:
        runs = claim(worker_id, batch=10)
        if not runs:
            time.sleep(1)                     # nothing due
            continue
        for run in runs:
            execute(run, worker_id)
```

**Polling once a second is genuinely fine** for almost every scheduler, **and it is much simpler than anything
event-driven.** **Sub-second precision is a requirement worth questioning** — very few scheduled jobs need it,
and it changes the design substantially.

### The real systems

```
PostgreSQL          the job store; SELECT ... FOR UPDATE SKIP LOCKED
                    is the standard queue pattern and is genuinely good
Quartz              the Java scheduler; clustered mode uses row locks
Airflow             DAG-oriented; the scheduler/executor split is the
                    same shape, with dependencies added
Temporal / Cadence  durable execution — the workflow's state is
                    persisted, so a crash resumes mid-function
Sidekiq / Celery    queue-backed workers, Redis or a broker
cron                one machine, no coordination, no history —
                    and correct for a great many cases
```

**Temporal is worth naming as the different approach**: instead of making jobs idempotent, **it persists the
execution state so a crashed job resumes where it stopped** — which changes the guarantee genuinely rather
than working around it.

---

## 6. The numbers

**Scale.**

```
100,000,000 scheduled jobs/day
= ~1,200/second average

but the distribution is NOT uniform:
  ~40% are scheduled on the hour
  ~15% at midnight
  -> the instantaneous rate at 09:00:00 could be MILLIONS

-> the average is comfortable; the SPIKE is the whole problem
```

**The scheduler's own load.**

```
polling every second, 10 scheduler instances:
  10 queries/second, each an indexed range scan

the pending set at any moment (with jitter, steady state):
  ~1,200/second x a few seconds of lag = ~5,000 rows

-> a trivial database workload
-> THE SCHEDULING IS NOT THE HARD PART
```

**Storage.**

```
run row: ~200 bytes
100,000,000 runs/day = 20 GB/day

with 90-day retention: 1.8 TB
+ replicas: 5.4 TB

-> and the PARTIAL INDEX on (state, run_at) covers only pending
   and leased rows — a few thousand at a time — rather than
   9 billion completed ones
```

**That partial index is the difference between a usable table and an unusable one**, and it is one `WHERE`
clause.

**The herd, quantified.**

```
100,000,000 jobs, 40% on the hour = 40,000,000 at 09:00:00

WITHOUT JITTER:
  the claim query returns whatever it can, but every worker polls
  simultaneously; the database sees 10 concurrent range scans over
  40,000,000 matching rows
  -> the query slows from ~1 ms to seconds
  -> workers time out, retry, and make it worse

WITH 5 MINUTES OF JITTER:
  40,000,000 / 300 seconds = ~133,000/second, evenly

  at 10 jobs per claim and ~50 ms per job:
    each worker does ~200 jobs/second
    -> ~700 workers, steadily

-> ONE LINE turns an unbounded spike into a flat 133,000/second
```

**Lease settings.**

```
LEASE = 10 seconds, no heartbeat:
  any job taking > 10 s gets stolen and runs twice
  -> unusable for anything real

LEASE = 1 hour, no heartbeat:
  a dead worker's job sits idle for up to an hour
  -> unacceptable latency for a retry

LEASE = 60 seconds WITH a 20-second heartbeat:
  dead worker detected in <= 60 s
  a 6-hour job renews 1,080 times and is never stolen
  heartbeat load: 700 workers / 20 s = 35 updates/second

-> 35 writes a second buys correct behaviour for both cases.
   That is the argument for heartbeating rather than tuning
   the lease.
```

**Worker capacity, which is where the machines are.**

```
job duration varies enormously:
  send an email        ~100 ms
  call a webhook       ~500 ms (external!)
  generate a report    ~30 s to minutes

at 1,200 jobs/second average and ~200 ms mean:
  1,200 x 0.2 = 240 concurrent jobs
  at 50 concurrent per worker (I/O bound): ~5 workers

at the jittered peak of 133,000/second:
  133,000 x 0.2 = 26,600 concurrent
  -> ~530 workers

-> the fleet is sized for the PEAK, and jitter is what stops
   the peak being unbounded
```

**Retention and cleanup.**

```
9,000,000,000 completed runs over 90 days

DELETE FROM runs WHERE state IN ('done','failed') AND run_at < now() - 90 days

-> a DELETE over billions of rows is a disaster: it locks, bloats,
   and never finishes

-> PARTITION BY MONTH and DROP the old partition
   -> instant, no locking, no bloat

Same lesson as the pastebin's expiry: at this size, deletion is
a partition drop, not a DELETE.
```

**Duplicate rate, which is the honest number:**

```
at-least-once, 60-second lease with heartbeat:

  duplicates occur when a worker is partitioned from the database
  for longer than the lease while still executing

  realistically: ~0.01% - 0.1% of runs
  at 100,000,000/day: 10,000 - 100,000 duplicate executions/day

-> which is why "make the job idempotent" is not advice, it is
   a REQUIREMENT. Ten thousand duplicate emails a day is a product
   failure; ten thousand idempotent no-ops is nothing.
```

**Latency.**

```
poll interval 1 s        -> up to 1 s of scheduling lag
claim query              -> ~1-5 ms
job dispatch             -> ~1 ms

-> a job scheduled for 09:00:00 starts by about 09:00:01

sub-second precision would need event-driven scheduling —
a timer wheel or a delay queue — which is a substantially
different design and is very rarely required.
```

---

## 7. The trade-offs

**Lease length: short against long.** Short detects dead workers quickly and **steals jobs from slow-but-alive
workers, causing duplicate execution.** Long protects slow workers and **leaves a dead worker's job idle for
the whole lease.** **There is no setting that avoids both, because a dead worker and a slow one are
indistinguishable over a network** — and the resolution is heartbeating, which makes short leases safe at the
cost of a small continuous write load.

**At-least-once against at-most-once.** At-least-once is the default and **requires every job to be
idempotent** — which is a real constraint on job authors, and it is not optional at 100,000 duplicates a day.
At-most-once loses work on a crash **and is correct when a duplicate is worse than a miss**, which is rare and
should be an explicit per-job choice rather than an accident of where the `complete` call sits.

**Polling against event-driven.** Polling every second is simple, robust, and adds up to a second of lag.
**Event-driven — a timer wheel, or a delay queue — gives sub-second precision and is substantially more
complex**, with its own recovery problems. **Almost no scheduled job needs sub-second precision**, and asking
whether this one does is worth ten seconds.

**A database against a dedicated queue.** Postgres with `SKIP LOCKED` handles thousands of jobs a second,
gives transactions, history and ad-hoc queries for free, **and is one system rather than two.** A dedicated
queue scales further and **loses the ability to ask "what is scheduled for tomorrow"**, which is a question
operators ask constantly.

**Catch-up policy.** Running every missed occurrence is correct for accounting jobs and **catastrophic for
notifications** — a week's outage becomes a hundred and sixty-eight emails at once. Skipping to the most recent
is right for most things and **silently loses work** for some. **There is no default, and the bound on
catch-up is not optional**, or recovery from an outage becomes a second outage.

**Jitter against precision.** Jitter removes the herd for one line of code and **makes the run time
approximate.** "Send at nine" tolerates it; **"expire this token at nine" does not.** So it is per job and
defaults to zero, **which means the herd comes back for any job type where somebody set it to zero across the
board.**

**When would I not build this?** **`cron` on one machine is correct for a great many systems** — no
coordination, no lease, no distributed anything — and the failure mode, that the machine dying stops
everything, is often acceptable. **Managed schedulers exist**: cloud cron services, Temporal, Airflow. **And if
the jobs have dependencies between them** — "run B after A succeeds" — **this is a workflow engine and not a
scheduler**, which is a genuinely different and larger system.

---

## 8. In the interview

### How it gets asked

- *"Design a distributed job scheduler."* or *"Design cron as a service."*
- *"A worker picks up a job and dies. What happens?"* — the lease question.
- *"Can you guarantee a job runs exactly once?"* — where honesty scores.
- *"A million jobs are all scheduled for 09:00. What happens?"* — the herd.
- *"How do you handle jobs that run for hours?"*
- *"How do recurring jobs work?"*

### The first ninety seconds

> "The scheduling part is easy and I want to say that first, because it is not where the design is.
>
> **A table of runs keyed by time, an index on `(state, run_at)`, and a loop that claims whatever is due.**
> Even a hundred million jobs a day is about twelve hundred a second — **an ordinary database workload.**
>
> **What is hard is failure**, and there are three distinct problems.
>
> **First, two workers must not claim the same run.** A select followed by an update is a race. **The claim has
> to be one atomic statement** — an `UPDATE ... WHERE id IN (SELECT ... FOR UPDATE SKIP LOCKED)`.
>
> **And `SKIP LOCKED` is what makes it scale**: without it, ten workers polling simultaneously all block on the
> same rows and the throughput is one worker's. **With it, each takes rows nobody else holds and there is no
> coordination at all.**
>
> **Second, a worker that dies must not hold the job forever.** So the claim carries a **lease with an
> expiry**, and an expired lease means the run is available again.
>
> **And that produces a trade with no good setting.** **A short lease detects dead workers fast and steals jobs
> from slow-but-alive ones**, so they run twice. **A long lease protects slow workers and leaves a dead
> worker's job idle for the whole lease.** **You cannot distinguish dead from slow over a network** — so the
> resolution is a **heartbeat**: keep the lease short and renew it while genuinely working.
>
> **Third, and I would raise it unprompted: exactly-once execution is not available.**
>
> **A worker can finish the work and die before recording that it did.** You cannot make the side effect and
> the record atomic when the side effect is in somebody else's system. **So it is at-least-once with idempotent
> jobs, or at-most-once with the risk of loss** — and that is a per-job decision, not a system-wide one.
>
> **And I would model jobs and runs separately.** A daily report is **one job and three hundred and sixty-five
> runs** — which gives a history, makes retries natural, and stops recurring schedules drifting.
>
> **One question before I go further: does anything here need sub-second precision?** Because polling once a
> second is simple and robust, **and event-driven scheduling is a substantially different design that very few
> jobs actually need.**"

### The follow-ups

**"A worker picks up a job and dies. What happens?"**

> "The lease expires and another worker takes it — **and the interesting part is the trade that sets the lease
> length, because there is no setting that is right.**
>
> **When a worker claims a run it sets `lease_until` to now plus some period.** A background sweep resets
> anything whose lease has passed back to pending. **So a dead worker's job becomes available again with no
> failure detection needed** — the absence of a renewal is the signal.
>
> **Now the trade.**
>
> **A short lease — say ten seconds — detects death fast**, and **steals the job from any worker that is merely
> slow.** A job taking thirty seconds gets taken away and run again by somebody else, **so it executes twice
> and both workers think they own it.**
>
> **A long lease — an hour — protects slow workers**, and **a dead worker's job sits idle for up to an hour**,
> which for a retry is unacceptable latency.
>
> **And there is no value that avoids both, because a dead worker and a slow one look identical from the
> database's point of view.** That is the failure-detection result: **you cannot distinguish a crashed process
> from a slow one over a network.**
>
> **So the resolution is not to tune the lease — it is to heartbeat.** Keep the lease short, and have the
> worker extend it periodically while genuinely working. **A sixty-second lease with a twenty-second heartbeat
> detects death within a minute and lets a six-hour job run untouched.**
>
> **And the heartbeat must check ownership.** `UPDATE ... WHERE id = ? AND worker = ?` — **if the lease already
> expired and somebody else took the run, the update affects zero rows and the original worker must stop.**
> Without that check, a worker happily extends a lease it no longer holds, **and two workers both believe they
> own the run.**
>
> **One more detail: the attempt counter increments on the CLAIM, not on completion.** **A worker that dies has
> already consumed an attempt**, which is what stops a job that crashes the worker every time from retrying
> forever."

**"Can you guarantee a job runs exactly once?"**

> "No, and I would rather say that plainly than describe something that is not exactly-once and call it that.
>
> **The reason is specific.** A worker does the work — sends the email, calls the webhook — **and then records
> that it did.** **If it crashes between those two moments, the side effect has happened and the record does
> not exist.**
>
> **And you cannot make those atomic**, because the side effect is in somebody else's system. **A database
> transaction cannot cover an email that has already been sent.**
>
> **So there are exactly two honest choices, and they are a per-job decision.**
>
> **At-least-once: mark the run complete after the work.** A crash means it runs again. **This is the default**,
> and it **requires the job to be idempotent** — which is a real constraint on whoever writes the job, not a
> nice-to-have.
>
> **At-most-once: mark it complete before the work.** A crash means it never runs. **Correct when a duplicate
> is worse than a miss**, which is rare — and it should be an explicit choice, **not an accident of where
> somebody put the `complete` call.**
>
> **And the practical answer is: at-least-once plus an idempotency key**, derived from `(job_id,
> scheduled_time)` — **not generated per attempt**, because a retry must carry the same key or deduplication
> downstream does nothing. **That is the same rule as payments and notifications.**
>
> **I would give the honest number too**, because it turns this from a theoretical concern into a requirement.
> **Duplicates happen when a worker is partitioned from the database for longer than its lease while still
> executing** — realistically a hundredth to a tenth of a percent of runs. **At a hundred million runs a day,
> that is ten to a hundred thousand duplicate executions.**
>
> **Ten thousand duplicate emails a day is a product failure. Ten thousand idempotent no-ops is nothing.**
>
> **And there is a genuinely different approach worth naming: durable execution**, as in Temporal. **Instead of
> making jobs idempotent, it persists the execution state so a crashed job resumes where it stopped.** That
> changes the guarantee rather than working around it — **at the cost of a much heavier programming model.**"

**"A million jobs are all scheduled for 09:00. What happens?"**

> "Everything falls over, **and the reason is that the average rate is fine and the instantaneous rate is
> not.**
>
> **A hundred million jobs a day is twelve hundred a second, which is comfortable.** But the distribution is
> nothing like uniform — **people schedule on the hour.** Perhaps forty percent of everything lands at some
> `:00`, and a large share at midnight.
>
> **So at nine o'clock exactly, the claim query has forty million matching rows**, every scheduler instance
> polls at once, **the query goes from a millisecond to seconds, workers time out — and the retries make it
> worse.** The classic pattern where the recovery attempt is the second failure.
>
> **The fix is jitter, and it is one line.** **When materialising a run, add a random offset within an
> acceptable window.** 'At nine' becomes 'between nine and five past'.
>
> **Forty million jobs spread over three hundred seconds is a hundred and thirty-three thousand a second,
> evenly** — which is a capacity question rather than a crisis.
>
> **And the window is a product decision, per job.** 'Send the daily digest at nine' tolerates five minutes
> happily. **'Expire this token at nine' does not** — so jitter defaults to zero and is set deliberately.
>
> **Which is worth flagging as a risk: if job authors leave it at zero everywhere, the herd comes straight
> back.** So I would make it a default on the job *type* rather than something each author remembers.
>
> **The second mechanism is rate-limited dispatch.** The scheduler claims at a bounded rate regardless of how
> much is due, **so a backlog drains smoothly rather than arriving at once** — and it protects against the case
> where jitter was not applied, or where a recovery has produced a genuine backlog.
>
> **And that connects to the catch-up policy, which is the same problem wearing a different hat.** If the
> system was down for a week and a job runs hourly, **materialising every missed occurrence creates a hundred
> and sixty-eight runs at once — a self-inflicted herd at exactly the moment the system is recovering.** **So
> the catch-up bound is not optional**, and neither is the choice between running all missed occurrences,
> only the most recent, or none — **which has no default answer and belongs on the job.**"

### The model answer

*"Design a job scheduler for a platform where customers can schedule arbitrary tasks: a hundred million jobs a
day, tasks lasting from milliseconds to hours, and it must survive workers dying."*

> "The scheduling is the easy part and I want to establish that first so we spend the time correctly.
>
> **A hundred million jobs a day is twelve hundred a second — an ordinary database workload.** A table of runs
> with an index on `(state, run_at)`, and a loop that claims what is due. **The difficulty is entirely in
> failure and in the distribution.**
>
> **Modelling: jobs and runs are separate.** A job has a payload and optionally a schedule; **each occurrence
> is its own run row.** That gives a history, makes retries natural, and — because the next run is computed
> from the schedule rather than from when the last one finished — **recurring jobs do not drift.**
>
> **A unique constraint on `(job_id, run_at)`** so two scheduler instances materialising the same next
> occurrence cannot both succeed.
>
> **Claiming: one atomic `UPDATE ... WHERE id IN (SELECT ... FOR UPDATE SKIP LOCKED)`.** A select-then-update
> is a race. **And `SKIP LOCKED` is what lets workers scale horizontally with zero coordination** — without
> it, every worker blocks on the same rows and the fleet has the throughput of one.
>
> **The attempt counter increments on the claim**, so a worker that dies has already consumed an attempt and a
> job that crashes its worker cannot retry forever.
>
> **Leases with heartbeats, because tasks run from milliseconds to hours.** **A sixty-second lease renewed
> every twenty seconds** detects a dead worker within a minute **and lets a six-hour job run untouched.** **The
> heartbeat must check ownership** — if the lease lapsed and somebody else took the run, the update affects
> zero rows and the original worker stops.
>
> **And I would say plainly why there is no lease length that works without heartbeating: a dead worker and a
> slow one are indistinguishable over a network.**
>
> **The delivery guarantee: at-least-once, with an idempotency key derived from `(job_id, run_at)`.** **Exactly
> once is not available** — the work and the record of it cannot be made atomic when the work is an external
> side effect. **And I would give the number: roughly 0.01 to 0.1% of runs duplicate, which at this volume is
> ten to a hundred thousand a day.** **So idempotency is a requirement on job authors, not advice.**
>
> **At-most-once is available per job** for anything where a duplicate is worse than a miss — **and it should
> be an explicit flag, not an accident of where the `complete` call sits.**
>
> **Now the thing that actually breaks this system: the herd.** Forty percent of jobs get scheduled on the
> hour. **Forty million at 09:00:00 is not a capacity problem, it is an outage.**
>
> **Jitter is one line and removes it** — spread each run over an acceptable window. **Forty million over five
> minutes is a hundred and thirty-three thousand a second, evenly.** Per-job, defaulting to zero, **and I would
> set it on the job type rather than trusting each author** — because if it is left at zero everywhere the herd
> returns.
>
> **Plus rate-limited dispatch and a bounded catch-up policy**, because a week's outage on an hourly job would
> otherwise materialise a hundred and sixty-eight runs at once — **a self-inflicted herd during recovery.**
>
> **Sizing: the scheduler is a handful of instances polling once a second.** **The workers are where the
> machines are** — about five hundred at the jittered peak, sized by job duration rather than by count.
>
> **And retention: partition the runs table by month and drop old partitions.** **A `DELETE` over nine billion
> rows locks, bloats and never finishes.** Plus a **partial index covering only pending and leased rows**,
> which is what keeps the polling query fast against a table that is 99.99% completed runs.
>
> **Two closing points.** **I would question whether anything needs sub-second precision**, because polling
> once a second is simple and robust and event-driven scheduling is a much larger design.
>
> **And if the tasks have dependencies on each other — 'run B after A succeeds' — this is the wrong system.**
> That is a workflow engine, and building it as a scheduler with jobs that schedule other jobs **is how
> people end up with an undebuggable pile of scheduled work.** Worth establishing early."

---

## 9. Recall card

**The scheduling is the easy part** — a table indexed on `(state, run_at)` and a poll loop; even 100M jobs/day
is ~1,200/second. **Everything hard is failure and distribution.**

**Model JOBS and RUNS separately** (one job, many runs) for history, natural retries, and **no drift** — the
next run is computed from the schedule, not from when the last finished. **`UNIQUE (job_id, run_at)`** stops
two schedulers materialising the same occurrence.

**Claim in ONE atomic statement with `FOR UPDATE SKIP LOCKED`** — a select-then-update is a race, and without
`SKIP LOCKED` every worker blocks on the same rows and the fleet has the throughput of one. **Increment the
attempt counter on the CLAIM**, so a worker that dies has consumed an attempt.

**Leases have no good length, because a dead worker and a slow one are indistinguishable over a network.**
Short steals jobs from slow workers (duplicate execution); long leaves a dead worker's job idle. **The
resolution is a HEARTBEAT** — 60-second lease, 20-second renewal — **and the heartbeat MUST check ownership**,
or two workers both believe they own the run.

**Exactly-once is not available:** the side effect and the record of it cannot be atomic when the side effect
is in someone else's system. **At-least-once + an idempotency key from `(job_id, run_at)`** (not per attempt)
is the default; at-most-once is an explicit per-job flag. **~0.01–0.1% of runs duplicate — 10,000–100,000/day
at this volume — so idempotency is a REQUIREMENT, not advice.**

**The herd is what actually breaks it:** ~40% of jobs are scheduled on the hour, so the average rate is fine
and the instantaneous rate is an outage. **Jitter is one line** (40M over 5 minutes = 133k/second, evenly) —
**per job, defaulting to zero, so set it on the job TYPE or it will be left at zero.** Plus rate-limited
dispatch and a **bounded catch-up policy**, or recovering from an outage becomes a second one. **And partition
by month and DROP** — a `DELETE` over 9 billion rows never finishes.
