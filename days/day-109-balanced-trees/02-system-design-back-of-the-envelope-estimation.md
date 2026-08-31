---
day: 109
track: system-design
title: "Back-of-the-envelope estimation"
phase: "Scaling fundamentals"
status: written
---

# Day 109 · System Design — Back-of-the-envelope estimation

**After today you can:** You can produce QPS, storage and bandwidth numbers out loud in three minutes.

**The interviewer asks it as:** *Estimate the storage for five years of this system's data.*

---

## 1. What this is, and why they ask it

[Day 097](../day-097-recursion-revision/README.md) gave you the conversions. Today is the
**performance**: doing the whole thing out loud, for a system you have never seen, in about three minutes,
while somebody watches.

Three sentences. The skill is not arithmetic — it is **a fixed routine** that always produces the same
five numbers, so that you are never deciding what to work out next. It depends on a small set of figures
held in memory, because looking things up is not available and hesitating is what makes an estimate sound
like a guess. And it depends on **rounding aggressively and saying that you are**, because an estimate
whose purpose is to choose an architecture does not need to be right to two significant figures.

They ask it because it is the moment a design conversation becomes concrete, and because it is very
easy to tell the difference between someone doing it and someone performing it. The tell is not accuracy.
It is whether the candidate **states assumptions before using them**, **sanity-checks the answer against
something known**, and **says what the number means for the design** — because a number with no
consequence attached was not worth computing.

---

## 2. The story

Muthu had been building walls for twenty-six years and he did not carry a measuring tape to a first
visit.

A man wanted a compound wall around a plot near the water tank and asked how much it would come to.
Muthu walked the boundary, counting, with his hands behind his back.

Twenty-eight paces on the road side. Then the long side, forty-one. Then twenty-eight again, then
forty-one. His pace was about two and a half feet, and he had checked that against a tape often enough to
trust it.

He said, out loud, so the man could follow: about a hundred and thirty-eight paces, call it a hundred and
forty, times two and a half — three hundred and fifty feet. Six feet high. Two thousand one hundred square
feet of wall.

The man asked how many bricks.

Muthu said a nine-inch wall takes about ten bricks a square foot. So twenty-one thousand. Add five per
cent for breakage and cutting — call it twenty-two thousand.

Then he did the thing that his nephew, who had been with him four years, had learned to watch for.

He stopped and said: the last one I did like this was the school ground, and that was about four hundred
feet, and we used twenty-six thousand bricks. This is a bit shorter, so twenty-two is about right.

The nephew asked once why he bothered, since he had just worked it out.

Muthu said that working it out tells you a number and does not tell you whether you have made a mistake.
You can drop a nought and never notice. Comparing against something you have actually built tells you
whether the number is the right *size*. If he had come out with two hundred thousand bricks, the
arithmetic would have looked fine on the way through and the answer would have been nonsense, and the only
thing that catches it is remembering the school ground.

He was also, deliberately, not precise. He said three fifty feet when it was three forty-five, and ten
bricks a square foot when it was nine and a half. He rounded up every time, and he said so to the
customer, because the point of the number was to decide whether the man could afford the wall — and for
that, twenty-two thousand and twenty thousand mean exactly the same thing.

The number he was careful about was the one that came at the end: the lorry. A lorry carries about four
thousand bricks. Twenty-two thousand means six lorries, and six is not five, and that changes the day.

---

## 3. The idea in plain English

Muthu is doing back-of-the-envelope estimation, and his three habits are the three things being marked.

- Counting paces and multiplying is the **routine** — the same sequence every time, said out loud.
- "The school ground was four hundred feet and twenty-six thousand bricks" is the **sanity check**.
- Rounding up and saying so is **precision discipline**.
- The lorries are the **consequence** — the number that changes a decision, which is the only number that
  actually mattered.

### The routine: six steps, in this order

Never deviate. The value is that you are not deciding what to do next.

```
 1. USERS       daily active users. State the assumption.
 2. ACTIONS     actions per user per day. REASON about it, do not guess.
 3. QPS         requests/day ÷ 100,000, then × 3 for peak.
 4. SPLIT       read:write ratio. Ask, or assume and say so.
 5. STORAGE     writes/day × bytes per record × days × replication.
 6. BANDWIDTH   requests/s × bytes per response. Only if media is involved.
```

**Then the seventh step, which is the one that counts:** say what each number *means*. "Two thousand
requests a second, so six to eight application servers." "Five terabytes a year, so this is one database
with archiving, not a sharding problem."

**A number with no consequence attached was not worth saying.**

### The figures to hold in memory

You cannot look anything up. This is the whole list, and it is short.

```
 TIME
   seconds per day        86,400      -> round to 100,000
   seconds per month      2.6 M       -> round to 2.5 M
   seconds per year       31.5 M      -> round to 30 M

 CONVERSIONS
   1 million/day    ≈       10 QPS
   100 million/day  ≈    1,000 QPS
   1 billion/day    ≈   10,000 QPS

 SIZES
   1 KB × 1 million  = 1 GB
   1 KB × 1 billion  = 1 TB
   1 MB × 1 million  = 1 TB
   1 MB × 1 billion  = 1 PB

 TYPICAL RECORDS
   short post / tweet        ~300 B
   database row, 10 columns  ~1 KB
   chat message              ~200 B
   log line                  ~500 B
   JSON API response         ~5 KB
   web page, total           ~2 MB
   compressed photo          ~2 MB
   1080p video, per minute   ~50 MB

 MACHINE CAPACITY
   app server                 ~1,000 QPS of real work
   relational DB, reads       ~10,000/s indexed
   relational DB, writes      ~5,000/s
   Redis                      ~100,000 ops/s
   one network link           ~1 GB/s
   one SSD                    ~500 MB/s, ~50,000 IOPS

 LATENCY
   memory              ~100 ns
   SSD                 ~100 µs
   same-DC round trip  ~0.5 ms
   cross-continent     ~30 ms
   cross-world         ~150 ms

 MULTIPLIERS
   peak factor         ×3       (×100+ for a scheduled event)
   replication         ×3
   DAU from registered ~10-20%
   cache hit rate      ~90%
```

**That fits on one page and it is the entire toolkit.** Everything else is multiplication.

### Rounding discipline

**Round to one significant figure and say that you are doing it.**

```
 86,400  ->  100,000        makes the answer ~15% low
 365     ->  400 (or 300)   depending on which way you want to err
 1,024   ->  1,000
 0.15    ->  0.2
```

Two rules that make rounding safe rather than sloppy:

**Round in the direction that makes you safe.** For capacity, round *up*: over-provisioning is a cost,
under-provisioning is an outage. For savings claims, round *down*.

**Say which direction and why.** "I am rounding 86,400 up to 100,000, so my QPS numbers are about fifteen
percent low — which does not change the architecture." That single sentence converts sloppiness into
judgement.

### The sanity check, which is the thing candidates skip

After every estimate, compare against something known. Muthu's school ground.

```
 "I got 50 TB/day of media."
   Is that plausible? Instagram handles roughly 100 million uploads a day.
   -> if my system is a tenth of Instagram, 50 TB/day is far too high.
   -> re-check: did I use 2 MB or 20 MB per photo?

 "I got 200 QPS."
   Twitter's average was ~6,000 tweets/second at its peak of fame.
   -> 200 QPS for a global product is suspiciously small.
   -> re-check: is my DAU number registered users rather than daily?

 "I got 40 servers."
   Stack Overflow served the whole site on about a dozen machines.
   -> 40 for something simpler suggests I have over-counted somewhere.
```

**Two or three reference points are enough**, and they catch the error that actually happens: a factor of
ten, from a dropped zero or from confusing per-day with per-second.

### The three sanity anchors worth memorising

```
 a small product      100,000 DAU     ->  ~10-20 QPS average
 a large product      10 million DAU  ->  ~2,000 QPS average
 a giant              1 billion DAU   ->  ~200,000 QPS average
```

**If your answer is not near one of those for the size of product described, something is wrong.**

### Reasoning about actions per user

This is the only step that is not arithmetic, and it is where candidates guess when they should reason.

**Do not say "let us assume twenty".** Say *why* twenty:

> "A user opens the app three or four times a day. Each session loads a feed — that is one request for the
> feed plus a handful for images, though images go to a CDN so they do not count against my servers. They
> scroll a couple of pages and open one or two items. So roughly five server requests per session, four
> sessions — twenty a day."

**The reasoning is the answer.** The number is a by-product, and the interviewer is listening to the
derivation.

### What to do when you do not know something

**Ask.** "What is the read-to-write ratio?" is a legitimate question and asking it is better than
assuming.

**If they will not tell you, assume and label it.** "I will assume a hundred reads per write, which is
typical for a feed product. If it is closer to one-to-one, like messaging, the answer changes and I would
want to know."

**Never silently invent a number.** A stated assumption that turns out wrong is a good answer with a wrong
input; an unstated one is a guess.

---

## 4. The picture

The routine, as a ladder you climb the same way every time.

```
  1. USERS (DAU)                    10,000,000        ← state the assumption:
        │                                                daily active, not registered
        │  × actions/user/day  ← REASON about this
        ▼
  2. REQUESTS/DAY                   200,000,000
        │
        │  ÷ 100,000   ← say you are rounding 86,400
        ▼
  3. AVERAGE QPS                          2,000
        │
        │  × 3 (peak)  ← ×100 if there is a scheduled event
        ▼
     PEAK QPS                             6,000
        │
        ├──────────────────┐
        │ × read share     │ × write share
        ▼                  ▼
  4. READS 5,900/s      WRITES 100/s
        │                  │
        │                  │ × bytes/record × 365 × 3 replicas
        │                  ▼
        │            5. STORAGE/YEAR
        │
        │ × bytes/response
        ▼
  6. BANDWIDTH

  7. AND THEN: what does each number MEAN?
     6,000 QPS  -> 6-8 app servers
     5,900 reads -> a cache, then one DB with replicas
     5 TB/year   -> one database with archiving, not sharding
```

Rounding, drawn as a decision:

```
 EXACT              ROUNDED        error      does it change the answer?
 -----------------  -------------  ---------  --------------------------
 86,400 s/day       100,000        -15%       no
 365 days           400            +10%       no
 1,024 MB           1,000          -2%        no
 2,314 QPS          2,000-2,500    ±10%       no
 2,314 QPS          23,000         10×        YES — and that is the error
                                               a sanity check catches

 the arithmetic is allowed to be 20% wrong.
 it is NOT allowed to be 10x wrong, and the only defence is comparing
 against something you already know.
```

Muthu's wall, as the same routine:

```
 1. paces          138  -> round to 140
 2. × 2.5 ft/pace       = 350 ft
 3. × 6 ft high         = 2,100 sq ft
 4. × 10 bricks/sq ft   = 21,000
 5. + 5% breakage       = 22,000
 6. SANITY CHECK        school ground: 400 ft -> 26,000 bricks.
                        This is shorter. 22,000 is the right SIZE. ✓
 7. CONSEQUENCE         4,000 bricks per lorry -> SIX lorries, not five.
                        ^^^ the only number that changed a decision
```

---

## 5. How it actually works

### Worked example one: a chat application

*"Design WhatsApp. Give me numbers."*

```
 1. USERS
    2,000,000,000 registered, and I will assume 50% daily active
    -> 1,000,000,000 DAU        (state it: "if that is wrong, everything scales")

 2. ACTIONS — reasoned
    an active user sends ~40 messages a day and receives ~40
    sends are the writes; receives are fan-out, not separate client requests
    -> 40,000,000,000 messages sent per day

 3. QPS
    40 billion ÷ 100,000                =  400,000 writes/second average
    × 3 peak                            =  1,200,000 writes/second peak

 4. SPLIT
    messaging is roughly 1:1 — every message sent is read about once
    -> reads ≈ writes.  THIS IS THE UNUSUAL PART and worth saying:
       "unlike a feed product, caching and read replicas will not save me here"

 5. STORAGE
    200 bytes per message × 40 billion   =  8 TB/day
    × 365                                =  2.9 PB/year
    × 3 replicas                         =  8.8 PB/year
    -> WhatsApp does not store delivered messages, which is why it can exist.
       If we did retain them, this is the number that forces that decision.

 6. CONNECTIONS — the real constraint here
    1 billion users with a persistent connection
    ÷ ~1,000,000 connections per tuned server
    =  ~1,000 servers just holding connections open

 7. WHAT IT MEANS
    - 1.2M writes/s is far past one database: this must be sharded, by
      conversation_id, from day one
    - reads ≈ writes means caching does NOT rescue this
    - the binding constraint is CONNECTIONS, not CPU
```

**That last line is the point of the whole exercise.** The estimate found the constraint, and the
constraint is not the one you would have guessed.

### Worked example two: a video service

*"Design YouTube. How much storage?"*

```
 1. UPLOADS
    500 hours uploaded per minute (a published figure, but derive it too:
    2 billion users × 0.0002 uploads/day ≈ 400,000 uploads/day)

 2. RAW SIZE
    500 hours/minute × 60 = 30,000 hours/hour
    × 24 = 720,000 hours/day
    1 hour of 1080p ≈ 3 GB
    -> 2.2 PB/day of raw uploads

 3. TRANSCODING MULTIPLIER  ← the step people forget
    every video is stored at ~5 resolutions
    plus audio-only, plus thumbnails
    the lower resolutions are much smaller: total ≈ 1.5× the original
    -> ~3.3 PB/day

 4. PER YEAR
    3.3 PB × 365  ≈  1,200 PB  =  1.2 EB/year

 5. REPLICATION
    ×2 (not ×3 — erasure coding is used for cold video, ~1.4× overhead)
    -> ~1.7 EB/year

 6. BANDWIDTH — the number that dwarfs storage
    1 billion hours watched per day
    at 5 Mbit/s average  =  2.25 GB/hour
    1 billion × 2.25 GB  =  2,250 PB/day of egress
    ÷ 86,400 s           ≈  26 TB/second
    -> this is why Netflix and YouTube ship hardware into ISPs

 7. WHAT IT MEANS
    - storage is object storage with erasure coding, not a database
    - the DOMINANT cost is bandwidth, by an order of magnitude
    - therefore the architecture is a CDN problem, not a database problem
```

**Notice step 3.** The transcoding multiplier is the step candidates omit, and omitting it makes the
answer wrong by a factor that matters.

### Worked example three: a URL shortener

*"How much storage in five years?"*

```
 1. WRITES
    100,000,000 new URLs per day       (state it as the assumption)

 2. RECORD SIZE
    short code (7 chars)    7 B
    long URL                ~100 B
    user id, timestamps     ~30 B
    row overhead + index    ~100 B
    -> ~250 B, call it 500 B with the index

 3. PER YEAR
    100M × 500 B          =  50 GB/day
    × 365                 =  18 TB/year
    × 5 years             =  90 TB
    × 3 replicas          =  270 TB

 4. SANITY CHECK
    90 TB of pure text over five years. Is that plausible?
    100M/day × 5 years = 180 billion URLs at ~500 B — yes, arithmetic holds.
    And 180 billion is more than the entire indexed web, which suggests
    100M/day is a generous assumption. Worth saying.

 5. READS
    read:write ≈ 10:1  ->  1 billion redirects/day  =  10,000 QPS average
                                                    =  30,000 peak

 6. WHAT IT MEANS
    - 90 TB does not fit one machine: this is sharded, by the short code
    - 30,000 QPS of reads on tiny immutable records: a cache at 95%+ is
      easy, so ~1,500/s reach the store
    - records are immutable, so caching has no invalidation problem at all
```

**Step 4 is the one to imitate.** The sanity check did not just confirm the arithmetic — it questioned the
*input*, which is where estimates actually go wrong.

---

## 6. The numbers

### The multiplication table for this skill

```
 DAU × actions/day               =  requests/day
 requests/day ÷ 100,000          =  average QPS
 average QPS × 3                 =  peak QPS
 writes/day × bytes              =  storage/day
 storage/day × 365 × 3           =  storage/year, replicated
 QPS × bytes/response            =  bandwidth
 peak QPS ÷ 1,000                =  app servers
 reads/s × (1 - hit rate)        =  reads reaching the database
```

**Eight lines. That is the entire subject.**

### Where estimates go wrong, in order of frequency

```
 1. registered users used as daily active         10× too high
 2. per-day confused with per-second              86,400× wrong
 3. forgetting the peak factor                    3× too low
 4. forgetting replication                        3× too low
 5. forgetting a fan-out or transcoding multiplier 2-100× too low
 6. forgetting that media goes to a CDN            10× too high on server load
```

**Every one of those is a factor, not a percentage** — which is exactly why the arithmetic being 20
percent off does not matter and the sanity check does.

### Sanity anchors

```
 Twitter          ~6,000 tweets/second average, ~143,000 peak (a 2013 spike)
 Instagram        ~100 million photos/day
 WhatsApp         ~100 billion messages/day
 YouTube          ~500 hours uploaded per minute
 Google search    ~100,000 searches/second
 Stack Overflow   ~2 billion page views/year on ~a dozen servers
```

**The Stack Overflow one is the most useful**, because it is the counterweight: it is the reminder that
most systems do not need a thousand machines, and that a candidate whose estimate produces four hundred
servers for a modest product has made an error.

### How precise is precise enough?

```
 answer differs by    does the design change?
 ------------------   -----------------------
 ±20%                 no
 ×2                   rarely
 ×10                  YES — different number of machines, maybe different DB
 ×100                 YES — a different architecture entirely
```

**So the target is the right order of magnitude, and one significant figure is plenty.** Say that; it
gives you permission to round and it tells the interviewer you know what the number is for.

### The consequence table

The last step, and the one that turns arithmetic into design:

```
 peak QPS      what it means
 -----------   --------------------------------------------------
 < 100         one server. Genuinely. Do not over-build.
 1,000         a few servers, one database
 10,000        load balancer, cache, read replicas, one DB still fine
 100,000       sharding, and the design conversation changes
 1,000,000+    a specialised architecture; expect published papers

 storage       what it means
 -----------   --------------------------------------------------
 < 100 GB      one machine, in memory if you like
 1 TB          one database, comfortable
 10 TB         one big machine, or start planning to shard
 100 TB        sharded, definitely
 1 PB+         object storage, not a database

 write rate    what it means
 -----------   --------------------------------------------------
 < 1,000/s     one database
 5,000/s       one large database, at its limit
 > 10,000/s    sharded. No other option.
```

**Memorise the left column of those three tables.** That is what makes the seventh step automatic.

---

## 7. The trade-offs

### Estimation is for choosing, not for planning

The purpose is to decide the **shape** of the design — one database or twenty, cache or no cache, CDN or
not. It is not a capacity plan, and treating it as one is the wrong use.

**So: round hard, move fast, and spend the saved time on what the numbers imply.** A candidate who spends
eight minutes getting to 2,314 QPS has spent six minutes badly.

### When the estimate is the whole answer

Occasionally the numbers settle the design entirely and there is nothing else to say. *"You want to store
every GPS ping from a million vehicles every second"* — that is 86 billion points a day, and the answer is
a time-series store with downsampling, and no amount of discussion changes it.

**Recognising that early is a strength**, not a shortcut.

### When the estimate misleads

- **Averages hide the peak.** The system that fails is the one sized for average QPS.
- **Fan-out is invisible in user-facing numbers.** One celebrity post is one write to the API and fifty
  million writes to the feed system. The user-facing rate says nothing about it, and it is the single
  biggest trap in estimating a social product.
- **Connections are not requests.** A chat app with a million idle users has almost no QPS and a million
  open sockets. Memory per connection, not CPU per request, is the constraint.
- **Storage accumulates; QPS does not.** Always quote storage per year, and always ask about retention.
- **Media dwarfs everything and belongs to a CDN.** Counting image bytes against your servers overstates
  the load by ten times or more.

### Being wrong out loud

**Recovering from a mistake well is worth more than not making one.** If a sanity check shows you are a
factor of ten out, say so: *"That is too big — Instagram is about a hundred million photos a day and I have
just produced a billion. Let me check my per-user rate."*

**An interviewer who sees you catch your own error learns more about you than one who sees a clean
answer.**

---

## 8. In the interview

### How it gets asked

- The direct one: *"Estimate the storage for five years of this system's data."*
- As the second thing in any design: *"Before we go further, give me some numbers."*
- The specific probe: *"How many servers?"* / *"What is the peak QPS?"*
- The check: *"Does that number seem right to you?"*
- The consequence: *"So what does that tell you about the design?"*

### What to say out loud, in the first ninety seconds

1. **Announce the routine.** "Let me work up from users: daily actives, actions per day, requests per
   second, peak, then the read-write split, then storage."
2. **State every assumption as you use it.** "I will assume that ten million is daily active rather than
   registered. If it is registered, daily active is usually ten to twenty percent, and everything below
   divides by ten."
3. **Reason about actions per user; do not guess.** "Three or four sessions a day, five server requests
   each — images go to a CDN so they do not count — so about twenty."
4. **Round out loud.** "There are 86,400 seconds in a day and I am rounding to a hundred thousand, so my
   QPS is about fifteen percent low. That does not change anything."
5. **Sanity-check against something known.** "That gives two thousand QPS average. For a product with ten
   million daily users, that is the right order — Twitter was around six thousand tweets a second at its
   peak of fame."
6. **Say what it means.** "Six thousand peak QPS is six to eight application servers and one database with
   a cache. Five terabytes a year is one database with archiving, not a sharding problem."

### The follow-ups

**"Estimate the storage for five years."**
"Let me build it up. First the write rate: ten million daily active users, and I will reason about writes
rather than guess — this is a feed product, so a user posts perhaps once every couple of days, which is
five million posts a day. Then the record size: a post row with an id, a user id, text, timestamps and
indexes is about one kilobyte, and I will say a kilobyte rather than five hundred bytes because indexes
usually double it. So five gigabytes a day, which is about **1.8 terabytes a year**, or **9 terabytes over
five years** — and with three-way replication, roughly **27 terabytes on disk**. Media is a separate
number and much larger: if ten percent of posts have a photo at two megabytes plus thumbnails, that is
another terabyte a day, so **400 terabytes a year**, and that goes to object storage rather than a
database. Sanity check: nine terabytes of text over five years for a ten-million-user product feels
right — it is the sort of number one large machine holds. What it means for the design: the metadata is
one database with archiving of old rows, and the media is S3 behind a CDN."

**"Does that number seem right to you?"**
"Let me check it against something I know rather than re-doing the arithmetic, because re-doing it repeats
the same mistake. Instagram handles roughly a hundred million photo uploads a day. My system is about a
hundredth of Instagram's size, so I would expect something around a million uploads a day — and I got half
a million, which is the right order. If I had produced fifty million, I would go back and look for a
dropped factor of ten, most likely from using registered users where I meant daily active, or from
confusing per-day with per-second. Those two are the errors that actually happen, and they are factors of
ten and eighty-six thousand respectively, which is why the sanity check matters more than the precision."

**"How many servers?"**
"Peak QPS divided by what one server does. I have six thousand peak, and an application server doing real
work handles around a thousand requests a second — so six machines at a hundred percent utilisation, which
is not a thing you run, so **nine or ten at a sane sixty to seventy percent**. That is the compute side. I
would then check the database separately: five thousand nine hundred reads a second is borderline for one
relational database, but with a cache at ninety percent only about six hundred reach it, which is very
comfortable. So the shape is: a load balancer, ten app servers, Redis, one primary with a couple of read
replicas. And I would say the caveat — those per-server numbers depend enormously on what a request does,
so if each request runs a complex query, one server might handle two hundred rather than a thousand and I
would want to measure rather than assume."

**"What is the read-to-write ratio, and does it matter?"**
"It matters more than almost any other number, because it decides whether the problem is caching or
sharding. If it is high — a hundred to one, which is typical for a feed or a catalogue — then reads
dominate, a cache removes ninety percent of them, and read replicas handle the rest; the write path is
almost free. If it is close to one to one, which is messaging, then caching does very little and I am
looking at sharding the write path much sooner. So I would ask, and if you would not tell me I would
assume a hundred to one for a feed product and say clearly that the answer changes if it is closer to
even."

**"So what does that tell you about the design?"**
"That is the step that makes the arithmetic worth doing, so let me go through each number. **Six thousand
peak QPS** means six to ten application servers — a normal deployment, nothing exotic. **A hundred writes a
second** means one database takes the writes comfortably; I am nowhere near needing to shard, which would
cost me joins and transactions. **Five thousand nine hundred reads a second** means a cache is the highest-
leverage thing I can add, because at ninety percent it removes ten times more load than another replica.
**Five terabytes a year** means one database with archiving rather than a distributed store. And if any one
of those numbers had been ten times larger, the answer would be different — at a hundred thousand QPS or
ten thousand writes a second, I would be sharding from day one and the whole conversation changes."

**"What if you do not know how many actions a user takes?"**
"I ask, because it is a legitimate question and asking is better than inventing. If you will not tell me, I
reason it out loud rather than guessing a number: how many times does someone open this app in a day, what
does a session actually do, and how many of those requests reach my servers rather than a CDN. For a feed
product that lands around twenty; for a messaging app it is closer to eighty; for e-commerce it is five
page views and a fraction of an order. Then I label it as an assumption and carry on, so that if it is
wrong you can correct one input rather than the whole estimate. The thing I would not do is state a number
with no derivation — the reasoning is what you are actually asking for."

### A model answer

Asked: *estimate the storage for five years of this system's data.*

> "Let me work up from users, and I will say every assumption as I use it so you can correct any of them.
>
> **Users.** You said ten million. I am going to take that as **daily active**, not registered — and that
> matters, because if it is registered then daily active is usually ten to twenty percent of it and every
> number I give divides by ten.
>
> **Writes.** I need writes per day, and rather than guess a number I will reason: this is a feed product,
> so a typical user posts something perhaps once every two days. That gives **five million posts a day**.
>
> **Record size.** A post row — id, user id, text, a couple of timestamps, some flags — is a few hundred
> bytes, and indexes typically double that, so I will call it **one kilobyte**. Rounding up, deliberately,
> because under-estimating storage is the expensive direction.
>
> So **5 GB a day**, times 365 is about **1.8 TB a year**, times five years is **9 TB**, and with the
> standard three-way replication that is roughly **27 TB on disk**.
>
> **Media is separate and much bigger.** If ten percent of those posts carry a photo, at about two
> megabytes plus a few thumbnails, that is another **1 TB a day** — **400 TB a year**. That does not belong
> in a database; it goes into object storage behind a CDN, with only the key stored in the row.
>
> Let me sanity-check the shape of that before I go on, because the error that actually happens in these
> estimates is a factor of ten, not twenty percent. Instagram handles around a hundred million photo
> uploads a day. My system is roughly a hundredth of that size and I have produced half a million uploads
> a day, which is the right order. If I had come out with fifty million I would go back and look for
> registered-versus-daily-active, or a per-day-versus-per-second slip.
>
> And then the part that makes the arithmetic worth doing — **what it means**. Nine terabytes of metadata
> over five years is comfortably one database with old rows archived; it is not a sharding problem, which
> matters because sharding would cost me joins and transactions permanently. Four hundred terabytes a year
> of media is object storage and a CDN, and the CDN is what stops that bandwidth touching my servers at
> all. The only number I would want to firm up before committing is the posts-per-user rate, because
> everything above scales linearly with it."

---

## 9. Recall card

- **Six steps, in the same order, every time: users → actions/day → QPS (÷100,000, ×3 for peak) →
  read:write split → storage (× bytes × 365 × 3) → bandwidth.** Then the **seventh and most important**:
  say what each number *means* for the design. **A number with no consequence attached was not worth
  computing.**
- **Round to one significant figure and SAY that you are** — "86,400 rounded to 100,000, so I am ~15% low,
  which changes nothing". Round **up** for capacity, **down** for savings. The target is the right **order
  of magnitude**: ±20% changes nothing, **×10 changes the design**.
- **Sanity-check against something known, every time.** Twitter ~**6,000 tweets/s**; Instagram ~**100M
  photos/day**; WhatsApp ~**100B messages/day**; YouTube ~**500 hours uploaded/minute**; Stack Overflow ran
  on **~a dozen servers**. The errors that actually happen are **factors**: registered-as-daily-active
  (10×), per-day-as-per-second (86,400×), forgetting peak (3×), replication (3×), fan-out or transcoding
  (2–100×).
- **Reason about actions per user; never guess a number.** "Three or four sessions, five server requests
  each, images go to the CDN — so twenty." **The derivation is the answer.** And when you do not know,
  **ask**; if refused, **assume and label it**.
- **Memorise the consequence table.** Peak QPS: **<100 → one server · 1,000 → a few + one DB · 10,000 →
  LB + cache + replicas · 100,000 → sharding**. Storage: **1 TB → one DB · 100 TB → sharded · 1 PB →
  object storage**. Writes: **>10,000/s → sharded, no other option.** And watch the three invisible
  constraints: **fan-out**, **connections** (not requests), and **storage accumulating** while QPS does
  not.
