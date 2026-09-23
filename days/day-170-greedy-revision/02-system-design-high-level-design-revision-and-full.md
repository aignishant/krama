---
day: 170
track: system-design
title: "High-level design revision and full mock"
phase: "High-level design case studies"
status: written
---

# High-level design revision and full mock

## 1. What this is, and why they ask it

This is the last day of the case studies, and it is not another case study. **It is the framework** — the
thing that lets you take a prompt you have never seen to a defended architecture in forty-five minutes.

Because that is the actual test. **They will not ask you to design Twitter.** They know you have read the
Twitter answer. **They will ask you to design something adjacent to it**, or something from their own product,
**and what they are measuring is whether you have a method or a memory.**

**A method looks like this: five minutes on requirements, five on the arithmetic, five on the interface and
the data, fifteen on the architecture, ten on one deep dive, five on failure.** Every prompt, every time.

**And the single most common failure has nothing to do with knowledge.** It is starting to draw boxes in
minute two. The candidate who names a message queue before anyone has said how many users there are **has
told the interviewer that they are recalling, not designing.**

They ask it because **the framework is what transfers.** A candidate who can be handed an unseen prompt and
produce structure — requirements, numbers, the one bottleneck that matters, an honest trade — **is the same
candidate on the job**, where every problem is unseen.

By the end of this lesson you have the minute-by-minute clock, the four questions to open with, the
back-of-envelope numbers to know cold, the recurring toolkit, and **a full mock on a prompt this course has
never covered**, worked through end to end.

---

## 2. The story

Shakuntala had been doing weddings for twenty-two years and she had one rule that annoyed everybody who walked
in.

**She would not talk about the food.**

A man came in on a Thursday in a very good shirt, sat down, and started straight in on the menu. Two kinds of
rice. Paneer done the way they do it at that place near the station. A sweet counter with three men behind it.

He had it all worked out and he wanted a price.

She let him finish, and then she asked him how many people.

"Four hundred. Maybe five."

**"Which is it?"**

He said he would find out.

**Then she asked when they eat.** Not the date — the hour. He said eight, and she said eight or nine thirty,
because at a wedding it is never eight, and if it is nine thirty the rice sits for ninety minutes and half of
what he had just described cannot be made at all.

**Then where.** Then whether there was water at the place, and shade, and how far a van could get to the back
of it.

And then the question the man did not expect, which was: **"What is the one thing that must not go wrong?"**

He thought about it and said that his mother-in-law was coming and there had to be enough of the sweet.

**Shakuntala wrote one number on the board behind her — the hour they would actually eat — and circled it.**

"Now I can tell you about food."

He said, a little stiffly, that he had come in with the menu already decided.

**"Everybody comes in with the menu already decided,"** she said. **"And everybody who fails at this trade
fails the same way. They start with it."**

**"Tell me how many people there are and when they eat, and I can build you a menu. Tell me the menu, and I
know nothing at all."**

---

## 3. The idea in plain English

Shakuntala's rule is the framework. **How many, when, and what must not go wrong — before a single box gets
drawn.**

Here is the clock. **Forty-five minutes, six blocks, and the discipline is announcing each one out loud** so
the interviewer knows where you are and can redirect you cheaply.

```
   0-5    REQUIREMENTS   what it does, what it must not do,
                         and what I am explicitly leaving out
   5-10   THE NUMBERS    users, reads/sec, writes/sec, storage/day
                         -> and the ONE number that drives the design
   10-15  INTERFACE      the three or four calls, and the data model
          + DATA
   15-30  ARCHITECTURE   the boxes, in the order requests flow
   30-40  DEEP DIVE      one thing, in real detail — theirs or mine
   40-45  FAILURE        what breaks, what I would measure,
                         what I would do with another hour
```

**The first five minutes are worth more than the last twenty**, and they are the ones candidates skip.

### The four questions to open with

**Ask these before anything else. They take ninety seconds and they change the design.**

**One: who uses it and how many of them?** "Everyone" is not an answer — **a thousand users and a hundred
million are different systems**, and the interviewer will tell you if you ask.

**Two: what is the read-to-write ratio?** This is **the single most decision-relevant number in system
design.** Read-heavy means caching, replicas, fan-out on write, denormalisation. **Write-heavy means the
opposite of all four.** Everything downstream depends on it.

**Three: what must not go wrong?** Shakuntala's question. **"We may lose a like" and "we may not lose a
payment" produce different systems** from the first box onwards. Ask it explicitly.

**Four: what am I not building?** **Say what is out of scope and get agreement.** "I am not doing search,
analytics, or the admin panel." **This is not laziness — it is the only way to finish**, and interviewers
almost always agree.

### The estimation ladder

**Every back-of-envelope in system design is the same four steps, in this order:**

```
   1. USERS          daily active users
   2. ACTIONS        per user, per day
   3. RATE           divide by 86,400 -> per second
                     then multiply by 10 for peak
   4. SIZE           per action, in bytes -> per day, per year
```

**Round aggressively.** 86,400 seconds a day is **100,000**. A million times a thousand is **a billion**.
**Nobody wants three significant figures**, and precision here reads as not knowing what matters.

**And say the conclusion, not the number.** "Twelve hundred writes a second — **that is one ordinary database,
so writes are not the problem here.**" **The number without the conclusion is arithmetic; with it, it is
design.**

### The numbers worth knowing cold

```
   seconds in a day            ~100,000  (86,400, rounded)
   1 million/day               ~12/second
   1 billion/day               ~12,000/second

   a tweet, a comment          ~200 bytes - 1 KB
   a photo                     ~200 KB - 2 MB
   a minute of video (1080p)   ~50 MB

   one commodity database      ~5,000 writes/second
                               ~50,000 reads/second with replicas
   one cache node              ~100,000 reads/second
   one machine, in memory      ~64-256 GB

   memory read                 ~100 ns
   SSD read                    ~100 microseconds  (1,000x memory)
   disk seek                   ~10 ms             (100,000x memory)
   same-datacentre round trip  ~0.5 ms
   cross-continent round trip  ~150 ms   (the speed of light; unfixable)
```

**The last one is the one to have ready**, because it is the only number in the list that no amount of
engineering will improve.

### The toolkit

**There are about a dozen building blocks and every case study is a rearrangement of them.** Knowing *when*
each one is the answer is the skill:

```
   LOAD BALANCER        spread requests; health-check; the front door
   CDN                  static and semi-static content, near the user
   CACHE                read-heavy, tolerant of slightly stale data
   QUEUE                decouple; absorb bursts; retry; at-least-once
   REPLICATION          read scale and durability, at the cost of staleness
   SHARDING             write scale and storage, at the cost of cross-shard
                        anything
   CONSISTENT HASHING   shard without reshuffling everything on a change
   BLOB STORE           big immutable things; never in the database
   SEARCH INDEX         text queries the main store cannot answer
   STREAM PROCESSOR     aggregate on the way in, not at read time
   RATE LIMITER         protect everything behind it
   IDEMPOTENCY KEY      the answer to every at-least-once delivery
```

**And the recurring trade-offs, which are what "why?" is asking about:**

```
   fan-out on WRITE vs on READ     -> read-heavy? write. celebrities? read.
   strong vs eventual consistency  -> what breaks if it is 200 ms stale?
   SQL vs NoSQL                    -> do you need transactions across rows?
   sync vs async                   -> does the user have to wait for it?
   push vs pull                    -> how many recipients, how urgent?
   precompute vs compute on read   -> read:write ratio decides it
```

### What senior sounds like

**Three habits separate a strong answer from a complete one.**

**Volunteering the failure mode.** Do not wait to be asked what happens when the cache dies. **Say it:** "if
this cache goes cold, every request hits the database at once and takes it down — **so I would warm it on
deploy and add a request-collapsing layer.**"

**Giving the number with the trade.** Not "we would cache it" but **"we would cache it; at a 90% hit rate that
turns 50,000 reads a second into 5,000, which one database handles — and the cost is up to sixty seconds of
staleness, which for a follower count is fine."**

**Saying what you do not know.** "I have not built one, but I would expect X, and I would verify it by
measuring Y." **This is a strong answer.** Confident invention is the weakest thing you can do in the room,
and it is always audible.

---

## 4. The picture

The clock, and what each block produces:

```
   0-5    REQUIREMENTS
          |  functional: 3-5 bullet points, no more
          |  non-functional: availability, consistency, latency
          |  OUT OF SCOPE: say it, get agreement
          v
   5-10   THE NUMBERS
          |  users -> actions -> per second -> bytes
          |  THE OUTPUT IS ONE SENTENCE:
          |  "this is a <read-heavy / write-heavy / storage> problem"
          v
   10-15  INTERFACE + DATA
          |  3-4 calls with their arguments
          |  the tables, and what is sharded by what
          v
   15-30  ARCHITECTURE
          |  boxes in REQUEST-FLOW order, not importance order
          |  say why each box exists as you draw it
          v
   30-40  DEEP DIVE
          |  ONE thing. Offer two, let them pick.
          v
   40-45  FAILURE + WRAP
             what breaks, what I would measure,
             what I would do with another hour

   THE MOST COMMON FAILURE IS DRAWING BOXES IN MINUTE TWO.
   It tells the interviewer you are recalling, not designing.
```

The one number that decides everything:

```
                   READ : WRITE RATIO

   1000:1  (social feed, product page, news)
     -> CACHE everything
     -> read REPLICAS
     -> FAN OUT ON WRITE (precompute the answer)
     -> DENORMALISE freely
     -> eventual consistency is almost always fine

   1:1     (chat, collaborative editing)
     -> caching buys little
     -> the write path IS the design

   1:1000  (metrics, logs, click events, sensor data)
     -> caching is USELESS
     -> batch and compress on the way in
     -> AGGREGATE at write time; never store raw at read scale
     -> a time-series or columnar store, not a row store

   ASK FOR THIS NUMBER IN THE FIRST TWO MINUTES.
   Every box you draw afterwards depends on it.
```

The estimation ladder, worked:

```
   "Design a photo sharing app"

   USERS      100,000,000 daily active
   ACTIONS    2 uploads/day, 100 views/day
   RATE       uploads: 200,000,000 / 100,000 s = 2,000/second
              views:  10,000,000,000 / 100,000 s = 100,000/second
              PEAK:   x10 -> 20,000 and 1,000,000
   SIZE       photo ~1 MB
              storage: 200,000,000 x 1 MB = 200 TB/DAY
                       = 73 PB/year

   THE SENTENCE: "50:1 read-heavy, and the storage is the
   real problem, not the compute. Photos go in a blob store
   behind a CDN; the database holds only metadata."

   THAT SENTENCE is what the five minutes was for.
```

The toolkit, as a decision table:

```
   SYMPTOM                              REACH FOR

   same data read many times            CACHE
   large static files, global users      CDN
   traffic spikes, slow work             QUEUE
   reads exceed one machine              REPLICAS
   writes or storage exceed one machine  SHARDING
   adding a machine reshuffles all keys  CONSISTENT HASHING
   big immutable blobs                   BLOB STORE + CDN
   "find posts containing X"             SEARCH INDEX
   counting at read time is too slow     STREAM PROCESSOR
   one client can hurt everyone          RATE LIMITER
   a retry might do it twice             IDEMPOTENCY KEY
```

---

## 5. How it actually works

**A full mock, on a prompt this course has not covered.** Read the prompt, set a clock at forty-five minutes,
and do it yourself before reading on.

> *"Design an online examination platform. Schools across the country run exams on it. When an exam starts,
> everyone taking it starts at the same moment."*

### Minutes 0–5 · Requirements

**Say the four questions out loud.**

> "Four things before I draw anything.
>
> **How many students, and are they concurrent?** I will assume **ten million students in a single national
> exam, all starting at 10:00 exactly** — and I want to flag straight away that the simultaneity is the whole
> problem, not the volume.
>
> **What is the read-to-write ratio?** Unusual here: **there is one enormous read at the start — the question
> paper — and then a steady stream of writes for three hours.** So it is two systems, not one, and I will
> design them separately.
>
> **What must not go wrong?** I will assume: **an answer, once written by a student, is never lost**, and
> **nobody sees the paper before 10:00.** Those two are non-negotiable and everything else bends around them.
>
> **What am I not building?** No question authoring, no marking, no proctoring, no analytics. **Just: deliver
> the paper, accept answers, submit.**"

**Functional:** start an exam at a fixed time; fetch the paper; save answers continuously; submit.

**Non-functional:** **durability of answers above everything**; the paper is secret until the start instant;
**degrade gracefully on a bad connection** — a student on a village link must not lose an hour of work.

### Minutes 5–10 · The numbers

**The paper delivery, first, because it looks like the hard part:**

```
10,000,000 students x 500 KB paper = 5 TB
delivered within 60 seconds of 10:00:00

5 TB / 60 s = 83 GB/second = 667 Gbps
```

**Say the conclusion: that is a content-delivery problem, not a compute problem** — and 667 Gbps in one minute
from an origin is not something you build.

**Then the answers:**

```
autosave every 30 seconds, 10,000,000 students:
  10,000,000 / 30 = ~333,000 writes/second
  at ~2 KB each  = ~667 MB/second

over a 3-hour exam:
  333,000 x 10,800 s = ~3.6 BILLION writes
```

**And the submission spike:**

```
most students submit in the final two minutes:
  ~5,000,000 / 120 s = ~42,000 submissions/second
```

**The sentence: "This is a burst problem twice — once at the start and once at the end — with a sustained
write load in between. Nothing here is read-heavy, so caching barely features."**

### Minutes 10–15 · Interface and data

```
GET  /exam/{id}/paper        -> the encrypted paper (available from 09:00)
GET  /exam/{id}/key          -> the decryption key (available from 10:00:00)
POST /exam/{id}/answers      -> {question_id, answer, version, client_time}
POST /exam/{id}/submit       -> finalise
```

**The two-call split for the paper is the central design decision**, and it is worth stating as one.

```sql
CREATE TABLE answers (
    student_id   BIGINT,
    exam_id      BIGINT,
    question_id  INT,
    answer       TEXT,
    version      INT,          -- monotonic per student, for ordering
    updated_at   TIMESTAMPTZ,
    PRIMARY KEY (student_id, exam_id, question_id)
);
-- sharded by student_id: every write touches exactly one shard,
-- and no query ever crosses students
```

**Sharding by `student_id` is free of cross-shard problems**, because **no operation in this system ever spans
two students.** Say that — it is the reason the sharding key is obvious, and obvious sharding keys are worth
naming.

### Minutes 15–30 · The architecture

**Paper delivery, and the move that makes it trivial:**

**Encrypt the paper and push it to the CDN an hour early.** Every student downloads it before 10:00 — **the
5 TB is spread over an hour instead of a minute.** At 10:00:00 exactly, **release only the decryption key.**

```
5 TB in 60 seconds        -> 667 Gbps       impossible
5 TB over an hour         -> 11 Gbps        ordinary CDN traffic

the key: 10,000,000 x 100 bytes = 1 GB
1 GB in 60 seconds        -> 133 Mbps       one machine

-> the burst shrinks by a factor of FIVE THOUSAND
```

**This is the whole trick, and it generalises: when a huge payload must appear at an instant, pre-position the
payload and release something tiny.** The same shape as a ticket sale that pre-generates the seat map, or a
game launch that pre-downloads and unlocks.

**The answer path, and the durability requirement:**

```
   browser
     |  1. writes to LOCAL STORAGE first, always
     |     -> a dropped connection loses nothing
     v
   load balancer
     |
     v
   stateless write service
     |  2. appends to a DURABLE LOG (Kafka), acks only after
     |     the log confirms
     v
   append-only log, replicated 3x
     |
     +--> 3. consumer materialises the latest answer per question
     |        into the sharded store
     |
     +--> 4. the log itself is the audit trail and the dispute record
```

**Acking from the log rather than from the database is what meets "never lose an answer"** — the log is a
sequential append, replicated, and it absorbs 333,000 writes a second without difficulty. **The database is
allowed to lag.**

**And writing to the browser's local storage first is not a nicety** — it is what makes a bad connection
survivable, which was a stated requirement. **The client retries from its own copy.**

**Submission, and why the spike is not a spike:**

**Because answers were autosaved throughout, "submit" is a state change on one row, not an upload.** Forty-two
thousand small state transitions a second across two hundred shards is **two hundred a second per shard.**

**Say this explicitly**, because it is the payoff of the earlier decision: **the continuous autosave is what
turns the end-of-exam spike into nothing.**

### Minutes 30–40 · The deep dive

**Offer two and let them choose.** "I could go deep on **keeping answers consistent when the same student has
two tabs open**, or on **what happens when a whole region loses connectivity mid-exam.** Which is more
interesting?"

**Take the second, since it is the harder one:**

> "A region goes dark at 11:00, an hour in. Two hundred thousand students.
>
> **Because every client holds its own answers locally, nothing is lost** — that was the point of writing
> locally first.
>
> **When the region comes back, two hundred thousand clients reconnect at once and replay their unsent
> writes.** That is a thundering herd, and it arrives at exactly the moment the system is recovering.
>
> **Three things.** **Jittered reconnect** — clients wait a random interval before retrying, so the return is
> spread over minutes rather than arriving in one second. **Exponential backoff** on failure. **And the writes
> are idempotent**, keyed by `(student_id, question_id, version)`, so replaying them is safe.
>
> **The harder question is the exam clock.** Do those students get their hour back? **That is a policy
> decision, not a technical one**, and I would raise it rather than assume — but technically it means the
> deadline is **per student, stored, and adjustable**, rather than a single global timestamp. **Which is a
> data-model decision that has to be made on day one**, so it is worth deciding now even though it looks like
> a product question."

### Minutes 40–45 · Failure and wrap

**Say what breaks, unprompted:**

- **The key-release endpoint is a single point of failure at 10:00:00.** Serve it from the CDN too, with a
  hard cache expiry set to the start instant.
- **A shard being unavailable loses writes for its students.** The log in front means they are only delayed,
  not lost.
- **Clock skew on clients** means "the exam started" is not simultaneous. The deadline is enforced
  **server-side**, and the client clock is advisory.

**Say what you would measure:** write acknowledgement latency at the 99th percentile, unacknowledged writes
per client, and **the count of students with no successful write in the last two minutes** — which is the
metric that would actually detect a regional outage.

**Say what you would do with another hour:** proctoring, marking, and **the hardest remaining problem, which
is preventing the paper leaking through a compromised client** — and that this is not solvable in software
alone.

### The real systems

```
CDN (CloudFront, Cloudflare)   pre-positioned encrypted papers
Kafka                          the durable write log
Cassandra / DynamoDB           the sharded answer store
Postgres                       exam metadata, students, schedules
Redis                          per-student session state, exam clocks
S3                             the immutable archive for disputes
```

---

## 6. The numbers

**The paper delivery, and what pre-positioning buys.**

```
NAIVE — everyone downloads at 10:00:00
  10,000,000 x 500 KB = 5 TB in 60 seconds
  = 83 GB/second = 667 Gbps
  -> not something you build; it is a bad afternoon for a CDN

PRE-POSITIONED — encrypted paper available from 09:00
  5 TB over 3,600 seconds = 1.4 GB/second = 11 Gbps
  -> ordinary CDN traffic

  then at 10:00:00, release the key:
  10,000,000 x 100 bytes = 1 GB in 60 seconds
  = 17 MB/second = 133 Mbps
  -> ONE MACHINE

RATIO: 5 TB -> 1 GB. A factor of 5,000.

The general form: when a huge payload must appear at an
INSTANT, pre-position the payload and release something tiny.
```

**The write load.**

```
autosave every 30 s, 10,000,000 students:
  333,000 writes/second sustained, for 3 hours
  x 2 KB = 667 MB/second

sharded by student_id across 200 shards:
  1,667 writes/second per shard
  -> comfortably one ordinary node each

the durable log absorbs it undivided:
  a sequential append at 667 MB/second is well within
  a modest Kafka cluster
```

**Total volume, and why you do not keep everything.**

```
every autosave stored:
  333,000/s x 10,800 s = 3.6 billion writes
  x 2 KB = 7.2 TB per exam

only the LATEST answer per student per question:
  10,000,000 students x 40 questions x 2 KB = 800 GB

-> the materialised store is 800 GB
-> the LOG is 7.2 TB, kept 90 days for disputes, then dropped

and if the client sends only CHANGED answers — perhaps 20% of
autosave ticks — both numbers fall fivefold: 67,000 writes/second
and a 1.4 TB log.

That optimisation is one client-side comparison, and it is worth
naming as a decision rather than leaving implicit.
```

**The submission spike, and why it is not one.**

```
5,000,000 students submit in the final 120 seconds
  = 42,000 submissions/second

BUT the answers are already saved. "Submit" is:
  UPDATE exams SET submitted_at = now() WHERE student_id = ?

  ~50 bytes, one row, one shard
  42,000 / 200 shards = 210 writes/second per shard

-> THE CONTINUOUS AUTOSAVE IS WHAT TURNS THE END-OF-EXAM
   SPIKE INTO NOTHING.

Without it, 5,000,000 x 80 KB of answers in 120 seconds
= 3.3 GB/second of uploads at the worst possible moment —
and any student whose upload fails has lost three hours.
```

**Compare that last pair honestly**, because it is the strongest argument in the design: **the same total data
either arrives smoothly over three hours or all at once in two minutes**, and the design choice is which.

**The estimation ladder in general, so it is reusable.**

```
   1 million actions/day    = ~12/second
   1 billion actions/day    = ~12,000/second
   peak                     = ~10x average

   1 KB x 1 million/day     = 1 GB/day = ~365 GB/year
   1 MB x 1 million/day     = 1 TB/day = ~365 TB/year

   one database             ~5,000 writes/second
   one cache node           ~100,000 reads/second
   one machine's memory     ~64-256 GB

Round 86,400 to 100,000. Nobody wants three significant
figures, and precision here reads as not knowing what
matters.
```

---

## 7. The trade-offs

**How to spend the forty-five minutes.** More time on requirements means less on the deep dive. **The
requirements time is the better investment** — a beautifully detailed design of the wrong system scores
nothing, and the interviewer will happily spend fifteen minutes on the deep dive if you leave time for it.
**The failure mode is the reverse: thirty minutes of architecture and no time to say what breaks.**

**Breadth against depth.** Covering everything shallowly is safe and unmemorable. **Going deep on one thing
risks going deep on the wrong thing** — which is exactly why you **offer two and let them choose.** That one
sentence converts a gamble into a collaboration.

**Volunteering weaknesses against defending the design.** Saying "this cache going cold takes the database down
with it" **sounds like an admission and reads as seniority**, because the alternative is the interviewer
finding it. **The cost is that you must then have the mitigation ready** — an unmitigated weakness you raised
yourself is worse than one nobody mentioned.

**Naming specific technologies against staying generic.** "Kafka" is more credible than "a message queue",
**and it invites a question about Kafka you may not be able to answer.** Name it when you can defend it, stay
generic when you cannot — **and never name something purely to sound current.**

**Following their hints against your plan.** When an interviewer says "interesting, but what about X", **X is
the thing they want.** Abandon your plan immediately. **Candidates who finish their prepared answer while the
interviewer waits are marked down**, and it is the most common way a strong candidate loses a round.

**Admitting ignorance against covering.** "I have not built one, but I would expect X and I would verify it by
measuring Y" **is a strong answer.** Confident invention is the weakest possible move **and it is always
audible** — the follow-up question that exposes it is the one thing an interviewer never forgets.

**When is this framework wrong?** **For a prompt with a genuine novelty in it, the arithmetic block can
mislead** — if the interesting part is a consistency requirement rather than a scale one, five minutes of
multiplication is five wasted minutes. **Read the prompt for where the difficulty actually is**, and if it is
not scale, say so and spend the time elsewhere.

---

## 8. In the interview

### How it gets asked

- *"Design a system you have never seen before. Forty-five minutes."*
- *"How would you approach a design problem you know nothing about?"*
- Any unseen prompt — an exam platform, a warehouse tracker, a queue for a temple.
- *"You have ten minutes. Just the high level."* — the same framework, compressed.

### The first ninety seconds

Said on any unseen prompt, before drawing:

> "Let me ask four things before I draw anything, because the answers change the design and I would rather not
> guess.
>
> **One: how many users, and how many at once?** A thousand and a hundred million are different systems.
>
> **Two: what is the read-to-write ratio?** This is the number I most want, **because everything downstream
> depends on it.** Read-heavy means caching, replicas, precomputing. **Write-heavy means none of those help and
> the write path is the design.**
>
> **Three: what must not go wrong?** 'We may lose a like' and 'we may not lose a payment' produce different
> systems **from the first box onwards.**
>
> **Four: what am I explicitly not building?** I would like to agree that up front — **it is the only way I
> finish in forty-five minutes.**
>
> **Then here is how I will use the time**, so you can redirect me cheaply if I am on the wrong thing.
>
> **Five minutes on requirements. Five on the arithmetic, so we know which part is actually hard. Five on the
> interface and the data model. Fifteen on the architecture. Ten going deep on one piece — and I will offer you
> two and let you pick. Five at the end on what breaks and what I would measure.**
>
> **The reason I do the arithmetic before the boxes is that it tells me which problem I am solving.** If it
> comes out at a thousand writes a second, **most of what I might have drawn is unnecessary**, and saying that
> is worth more than drawing it."

### The follow-ups

**"How do you approach a problem you know nothing about?"**

> "The same way every time, and the method is the point — **because they will not ask me to design Twitter.**
> They know I have read that answer. **They will ask for something adjacent, and what is being measured is
> whether I have a method or a memory.**
>
> **I start with the four questions**: how many users, what is the read-to-write ratio, what must not go wrong,
> and what am I not building.
>
> **Then the arithmetic, and it produces exactly one sentence:** 'this is a read-heavy problem', or 'the
> storage is the real constraint', or 'this is two bursts with a steady load in between'. **That sentence is
> what the five minutes was for.** The numbers on their own are just multiplication.
>
> **Then the interface and the data model, because they force the requirements to become concrete.** You cannot
> write down four calls without discovering an ambiguity you skated over.
>
> **Then the architecture, drawn in request-flow order rather than importance order**, saying why each box
> exists as it appears. **A box I cannot justify does not get drawn.**
>
> **Then one deep dive, and I offer two options** — that turns a guess about what interests them into a
> question.
>
> **And I always leave five minutes for failure**, because volunteering what breaks is the difference between
> a complete answer and a good one.
>
> **The single most common mistake is drawing boxes in minute two.** Naming a message queue before anyone has
> said how many users there are **tells the interviewer I am recalling, not designing** — and once they think
> that, everything after it is read as recall too."

**"Walk me through the arithmetic on something."**

> "Take a photo-sharing app. **Four steps, and I round hard.**
>
> **Users**: a hundred million daily active. **Actions**: two uploads and a hundred views each per day.
>
> **Rate**: two hundred million uploads a day. **I round 86,400 seconds to a hundred thousand** — so two
> thousand uploads a second. Ten billion views a day is **a hundred thousand a second.** **Peak is ten times
> average**: twenty thousand and a million.
>
> **Size**: a photo is about a megabyte, so **two hundred terabytes a day** — seventy-three petabytes a year.
>
> **Now the sentence, which is the actual output: 'It is fifty-to-one read-heavy, and the storage is the real
> problem, not the compute.'**
>
> **And that sentence decides three things immediately.** Photos go in a blob store behind a CDN, **never in
> the database.** The database holds only metadata — a few hundred bytes a photo, so a few hundred gigabytes a
> day, **which is an entirely different problem from two hundred terabytes.** And at fifty-to-one, **caching and
> precomputing are worth a great deal.**
>
> **I would round 86,400 to 100,000 out loud rather than quietly**, because the alternative is spending thirty
> seconds on long division while the interviewer waits. **Three significant figures here reads as not knowing
> what matters.**
>
> **And if the arithmetic comes out small, I say so and move on.** 'That is twelve hundred writes a second —
> **one ordinary database, so this is not where the difficulty is.**' **Discovering that a problem is easy is a
> result**, and it buys me time for the part that is not."

**"What separates a good answer from a complete one?"**

> "Three habits, and none of them is knowledge.
>
> **Volunteering the failure mode.** Not waiting to be asked what happens when the cache dies. **'If this
> cache goes cold, every request hits the database at once and takes it down — so I would warm it on deploy
> and collapse duplicate requests.'** Saying it first reads as seniority; **having it found for me reads as a
> gap.**
>
> **Giving the number with the trade.** Not 'we would cache it', but **'we would cache it; at a ninety percent
> hit rate that turns fifty thousand reads a second into five thousand, which one database handles — and the
> cost is up to sixty seconds of staleness, which for a follower count is fine.'** **Same decision, and one of
> them is a design.**
>
> **Saying what I do not know.** 'I have not run one at this size, but I would expect X, and I would verify it
> by measuring Y.' **Confident invention is the weakest thing I can do in the room, and it is always audible.**
>
> **And one more that is really about listening.** When an interviewer says 'interesting, but what about X',
> **X is the thing they want.** I abandon my plan immediately. **Finishing a prepared answer while the
> interviewer waits is the most common way a strong candidate loses a round**, and it is entirely avoidable."

### The model answer

*"Design an online examination platform. Ten million students, one national exam, everyone starts at ten
o'clock."*

> "Four questions first.
>
> **The read-to-write ratio here is unusual and it shapes everything: one enormous read at the start — the
> paper — and then three hours of steady writes.** So it is **two systems**, and I will design them separately.
>
> **What must not go wrong: an answer, once written, is never lost; and nobody sees the paper before ten.**
> Everything else bends around those two.
>
> **Out of scope: authoring, marking, proctoring, analytics.**
>
> **The arithmetic, and it names the real problem.** Ten million students times a five-hundred-kilobyte paper
> is **five terabytes, wanted inside a minute — six hundred and sixty-seven gigabits a second.** That is not
> something you build.
>
> **So: pre-position and release a key.** Push the **encrypted** paper to the CDN an hour early. Everyone
> downloads it before ten — **five terabytes over an hour is eleven gigabits a second, ordinary CDN traffic.**
> At ten exactly, release **only the decryption key**: ten million times a hundred bytes is **one gigabyte,
> which is one machine.** **A factor of five thousand, and it is the central decision in the design.**
>
> **The write path, and the durability requirement.** Autosave every thirty seconds is **three hundred and
> thirty thousand writes a second**, sustained for three hours.
>
> **The client writes to its own local storage first** — that is what makes a bad connection survivable, which
> was a stated requirement. Then to a **stateless write service, which appends to a durable replicated log and
> acks from the log, not from the database.** A sequential append absorbs that rate; the database is allowed to
> lag behind it. **The log is also the audit trail for disputes.**
>
> **Sharded by student id across two hundred shards — sixteen hundred writes a second each.** And the sharding
> key is obvious because **no operation in this system ever spans two students**, which is worth saying out
> loud.
>
> **Now the end-of-exam spike, and this is the payoff.** Five million students submitting in the last two
> minutes is forty-two thousand a second — **but the answers are already saved, so submit is a one-row state
> change, about two hundred a second per shard.** **Without the autosave it would be three point three
> gigabytes a second of uploads at the worst possible moment, and any student whose upload failed would have
> lost three hours.** **Same data — it either arrives smoothly over three hours or all at once.**
>
> **For the deep dive I could go into two tabs open on the same exam, or a region losing connectivity
> mid-exam. Which would you prefer?**
>
> **What breaks.** The key endpoint is a single point of failure at exactly ten o'clock — **serve it from the
> CDN with an expiry set to the start instant.** Client clocks are skewed, so **the deadline is enforced
> server-side and the client clock is advisory.** And when a region reconnects, **two hundred thousand clients
> replay at once — so jittered reconnect, exponential backoff, and idempotent writes keyed by student,
> question and version.**
>
> **What I would measure: acknowledgement latency at the ninety-ninth percentile, unacknowledged writes per
> client, and the number of students with no successful write in the last two minutes** — that last one is what
> would actually detect a regional outage.
>
> **And one thing I would flag as a decision rather than assume.** If students lose an hour, **do they get it
> back?** That is a policy question, **but it decides whether the deadline is one global timestamp or a stored
> per-student value** — a data-model choice that has to be made on day one. **So I would want an answer now,
> even though it looks like a product question.**"

---

## 9. Recall card

**Six blocks, forty-five minutes, announced out loud:** **0–5 requirements** (functional, non-functional, and
what is explicitly out of scope), **5–10 the arithmetic**, **10–15 interface and data model**, **15–30
architecture in request-flow order**, **30–40 one deep dive — offer two and let them pick**, **40–45 failure
and what you would measure.** **The most common failure is drawing boxes in minute two**, which says you are
recalling rather than designing.

**Four opening questions:** how many users and how many at once; **the read-to-write ratio** (the single most
decision-relevant number — it decides caching, replicas, fan-out and denormalisation); what must not go wrong;
and what you are **not** building.

**The estimation ladder: users → actions → per second (÷100,000, ×10 for peak) → bytes.** **Round hard** — three
significant figures reads as not knowing what matters. **The output is ONE SENTENCE**, not a number: *"read-heavy
50:1, and storage is the real problem."* **Discovering a problem is easy is a result.**

**Numbers cold:** 1M/day ≈ 12/s; 1B/day ≈ 12,000/s; one database ~5,000 writes/s; one cache node ~100,000
reads/s; memory 100 ns, SSD 100 µs, disk 10 ms; **cross-continent 150 ms and no engineering fixes it.**

**The move worth stealing from the mock: when a huge payload must appear at an INSTANT, pre-position it and
release something tiny.** 5 TB in a minute becomes 5 TB over an hour plus a 1 GB key — a factor of 5,000. **And
continuous autosave turns an end-of-exam spike into nothing: the same data either arrives smoothly or all at
once, and that is the design choice.**

**Three habits that read as senior:** volunteer the failure mode before you are asked (with the mitigation
ready); **give the number WITH the trade** ("90% hit rate turns 50,000 reads into 5,000, at up to 60 seconds
of staleness"); and say what you do not know. **And when they say "interesting, but what about X" — X is what
they want. Abandon your plan.**
