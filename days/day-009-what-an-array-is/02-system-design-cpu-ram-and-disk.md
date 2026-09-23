---
day: 9
track: system-design
title: "CPU, RAM, and disk: the speed hierarchy"
phase: "How computers and the internet work"
status: written
---

# Day 009 · System Design — CPU, RAM, and disk: the speed hierarchy

**After today you can:** You can order register, cache, RAM, SSD, disk and network by speed, and say how far apart they are.

**The interviewer asks it as:** *How much slower is a disk read than a memory read?*

---

## 1. What this is, and why they ask it

Storage is a ladder. At the top, values sitting inside the processor, reachable in less than a
nanosecond. At the bottom, a request crossing an ocean, taking a fifth of a second. Between
them: cache, main memory, solid-state storage, spinning disk.

The gaps are not small. Each step down is roughly one hundred to one thousand times slower
than the one above it. From the top of the ladder to the bottom is a factor of about a
hundred million.

Interviewers ask because every design decision you will ever justify comes down to which rung
you put something on. Why is Redis fast? It is on the memory rung. Why do we cache? To move
data up a rung. Why do database indexes exist? To turn many disk reads into a few. A candidate
who knows these numbers can do back-of-the-envelope estimation in their head and will give
sized answers instead of adjectives — and sized answers are what a system design round is
scored on.

---

## 2. The story

Meenal has a wedding to get to, and the car is coming at six in the morning.

She gets up at half past four, and the first ten minutes need no thought at all. Her towel is
on the hook where it always is. Her everyday clothes are folded on the chair beside the bed,
where she put them last night. She does not look for anything, because none of it is anywhere
except exactly where her hand goes.

Then she needs her good earrings, and those are in the small box on the dressing table. Two
steps, open the drawer, and there they are. Twenty seconds. It is not instant, and it is not
something she would ever describe as slow.

The saree is a different matter. The good sarees live in the big suitcase on top of the
almirah, and the top of the almirah is out of reach. It means going to the kitchen for the
plastic stool, carrying it back, standing on it, sliding the suitcase forward without bringing
the other one down with it, getting it onto the bed and opening it. Five minutes, minimum, and
it wakes her husband.

And this is the thing about Meenal: she knew that yesterday. On Wednesday evening she went up
once, brought the saree down, and left it hanging on the back of the door. This morning it is
already there, and the five minutes cost her nothing at all today because she had already
spent them.

She did something else on Wednesday that she does without thinking. While she was standing on
that stool with the suitcase open, she took out the matching petticoat and the second blouse
too. Not because she needed them, but because she was already up there, and going up is the
expensive part. Once the suitcase is open, taking three things costs almost exactly what
taking one thing costs.

The blouse is the problem. The blouse is at the tailor's, two kilometres away, because it
needed taking in at the sides. The shop opens at ten. It is twenty to five in the morning, and
there is nothing whatsoever she can do about it. It is not slow in the way the suitcase is
slow. It is a completely different kind of thing — it depends on somebody else, it happens on
somebody else's schedule, and no amount of getting up early affects it.

She wears the other blouse. She had a second one down from the suitcase, because she brought
three things instead of one.

---

## 3. The idea in plain English

Meenal's morning is the memory hierarchy, in order, including the two clever things she did
without calling them anything.

### The ladder, from the top

**The chair beside the bed — registers.** A **register** is a tiny store inside the processor
itself, holding one value. There are a few dozen. Access is under a nanosecond — effectively
free, because it is where the processor does its work.

**The dressing table drawer — CPU cache.** A **cache** is a small, fast store that keeps
recently used data close by. There are usually three levels, getting bigger and slower: **L1**
at about 64 KB per core and 1 nanosecond, **L2** at about 1 MB and 4 nanoseconds, **L3** shared
across cores at perhaps 32 MB and 15 nanoseconds.

**The suitcase on the almirah — main memory, RAM.** **RAM** — random access memory — is where
your running program's data lives. Gigabytes of it, at about 80–100 nanoseconds per access.
It is a hundred times slower than L1 and it is where everything ends up that does not fit in
cache. It is also **volatile**: switch the power off and it is gone.

**A shelf in another room — SSD.** A **solid-state drive** stores data permanently, with no
moving parts. About 100 **microseconds** for a read — a thousand times slower than RAM.

**The store room with a heavy door — spinning disk.** A traditional **hard disk drive** has a
physical arm that must move to the right track and wait for the platter to rotate underneath
it. About 10 **milliseconds** — a hundred times slower again than SSD, and a hundred thousand
times slower than RAM.

**The tailor's shop — the network.** A round trip within a data centre is about 0.5 ms. Across
a continent, 40 ms. Across the world, 150–250 ms. And, exactly like the tailor, it depends on
somebody else and can simply be unavailable.

### The numbers, and the trick for remembering them

Nobody remembers nanoseconds. Everybody remembers this: **scale it so one CPU cycle is one
second.**

| Where | Real time | If one cycle were one second |
|---|---|---|
| Register | 0.3 ns | **1 second** |
| L1 cache | 1 ns | 3 seconds |
| L2 cache | 4 ns | 13 seconds |
| L3 cache | 15 ns | 50 seconds |
| **Main memory (RAM)** | **80 ns** | **4 minutes** |
| **SSD read** | **100 µs** | **4 days** |
| **Spinning disk seek** | **10 ms** | **11 months** |
| Network, same data centre | 0.5 ms | 19 days |
| Network, across a continent | 40 ms | 4 years |
| Network, across the world | 150 ms | 16 years |

**Read the three bold rows.** Memory is minutes, SSD is days, spinning disk is nearly a year.
That is the answer to today's question, and it is why "just read it from the database" and
"it's already in memory" are two completely different sentences.

The ratio to actually memorise: **RAM is about 1,000× faster than SSD, and about 100,000×
faster than a spinning disk.**

### The suitcase and the trip: why you fetch a block, not a value

Meenal brought down three garments in one trip because climbing up is the expensive part.
Every level of this hierarchy does the same thing.

The processor never reads one byte from RAM. It reads a **cache line** of **64 bytes**. A
disk never reads one byte; it reads a **block** or **page**, typically **4 KB** — and
PostgreSQL reads 8 KB pages, and SSDs erase in blocks of megabytes.

The consequence is the single most useful design rule in this lesson: **once you have paid to
get there, take everything nearby.** Reading 64 sequential bytes costs the same as reading 1.
Reading a 4 KB page costs almost the same as reading 100 bytes from it.

That is why **sequential access is dramatically faster than random access** at every level,
and why database people care so much about whether rows that are read together are stored
together.

### The saree on the door: caching

Meenal spent the five minutes on Wednesday so that Friday would be free. That is a **cache**:
keep a copy of something expensive to fetch, somewhere cheap to reach.

Every layer of every system does this. The processor caches RAM. The operating system caches
disk pages in RAM. The database caches its pages in a buffer pool. The application caches
query results in **Redis**. The browser caches responses. A CDN caches your files near the
user.

And every one of them has the same two problems, which come up in every interview about
caching: what do you throw out when it is full (**eviction**), and what happens when the
original changes and your copy does not (**invalidation**). Day 097 onwards is where these
get their proper treatment; the point today is that caching is not a trick, it is **the**
response to a hierarchy with gaps this large.

### Volatile and durable

One more distinction, because it decides where data is allowed to live.

**RAM is volatile.** Power off, gone. **Disk and SSD are durable.** They survive a restart.

That is why a database writes to disk before telling you the write succeeded, and why Redis —
which lives in memory — is a cache first and a database second. When someone asks "why not
keep everything in RAM?", the answer is two-thirds cost and one-third durability.

---

## 4. The picture

The ladder, with the gaps drawn to scale as best a page allows:

```
        SIZE            SPEED             HUMAN SCALE (1 cycle = 1 second)

  ^   registers       ~200 bytes      0.3 ns     |  1 second
  |   L1 cache          64 KB           1 ns     |  3 seconds
  |   L2 cache           1 MB           4 ns     |  13 seconds
  |   L3 cache          32 MB          15 ns     |  50 seconds
  |   ------------------------------------------------------------- volatile
  |   RAM             8-512 GB          80 ns    |  4 minutes
  |   -------------------------------------------------------------
  |   SSD              0.5-8 TB        100 us    |  4 days
  |   HDD              1-20 TB          10 ms    |  11 months
  |   -------------------------------------------------------------
  |   same DC network      -           0.5 ms    |  19 days
  |   cross-continent      -            40 ms    |  4 years
  v   cross-world          -           150 ms    |  16 years

      smaller & faster & more expensive per byte at the top
      bigger  & slower & cheaper per byte at the bottom
```

**What to notice:** the two horizontal lines. Above the first one, everything vanishes when
the power goes. Below the second, everything depends on another machine being alive. Those are
not speed boundaries; they are boundaries of what can go wrong.

The cost per gigabyte, which is why the ladder exists at all:

```
   RAM     ~ $3.00 per GB          1 TB of RAM  = $3,000  (and needs a server that takes it)
   SSD     ~ $0.08 per GB          1 TB of SSD  = $80
   HDD     ~ $0.02 per GB          1 TB of HDD  = $20
   S3      ~ $0.023 per GB/month   1 TB in S3   = $23 per month
```

**What to notice:** RAM is roughly 40× the price of SSD per byte. That, not speed, is why
everything is not simply held in memory.

And what caching does to an average, which is the arithmetic behind every cache decision:

```
   90% of reads hit RAM (80 ns), 10% go to SSD (100,000 ns)

   average = 0.90 x 80 + 0.10 x 100,000
           = 72 + 10,000
           = 10,072 ns

   99% hit RAM:   0.99 x 80 + 0.01 x 100,000 =  1,079 ns
   99.9% hit RAM: 0.999 x 80 + 0.001 x 100,000 =   180 ns
```

**What to notice:** going from 90% to 99% is a 9× improvement, and 99% to 99.9% is another
6×. **The misses dominate the average completely.** This is why "our cache hit rate is 90%"
is a much worse position than it sounds, and it is a genuinely counter-intuitive result worth
being able to produce on demand.

---

## 5. How it actually works

### What happens on a memory read

The processor asks for an address. Then:

1. **L1** is checked. Hit, and you are done in about a nanosecond.
2. Miss → **L2**, then **L3**.
3. All missed — a **cache miss**. The memory controller fetches the whole 64-byte line
   containing that address from RAM, and it is placed in cache, evicting something else
   (usually the least recently used line).
4. If the address is not in RAM at all because the page was swapped out, that is a **page
   fault**: the OS reads a 4 KB page from disk, which is roughly a hundred thousand times
   slower, while the process waits.

This is why a program that fits in cache can be an order of magnitude faster than the same
program with slightly more data, and why swap thrashing takes a machine from working to
unusable rather than to slightly slower.

### Why sequential access is so much faster

At every level, hardware assumes you will read forwards.

**The prefetcher** watches your access pattern, notices sequential reads, and fetches the next
lines before you ask. **Disks** read a whole track at once. **SSDs** parallelise across
internal channels when reads are contiguous.

The measured gap:

```
HDD sequential  : 150-250 MB/s      HDD random 4 KB  : ~1 MB/s     (150-250x)
SSD sequential  : 500-7,000 MB/s    SSD random 4 KB  : ~50 MB/s    (10-100x)
```

That single table explains an enormous amount of database design. It is why **Kafka** is so
fast despite writing everything to disk — it only ever appends, sequentially. It is why
**LSM-tree** stores such as **Cassandra** and **RocksDB** buffer writes in memory and flush
them in large sorted runs. And it is why an index that lets you read 100 sequential rows
beats one that makes you fetch 100 scattered ones.

### Where real products sit on the ladder

| Product | Rung | Consequence |
|---|---|---|
| **Redis**, **Memcached** | RAM | microsecond reads; loses data on restart unless you configure persistence |
| **PostgreSQL**, **MySQL** | SSD, with a RAM buffer pool | the buffer pool hit rate is the single most important number in its performance |
| **Cassandra**, **RocksDB** | SSD, write-optimised | sequential writes, background compaction |
| **Kafka** | disk, sequential only | appends at near-sequential disk speed, and relies on the OS page cache for reads |
| **S3** | disk, over the network | ~50–100 ms first byte; enormous, cheap, durable |
| **Glacier** | offline | minutes to hours to retrieve; a tenth of S3's price |

**Postgres's buffer pool** is worth pausing on because it is the story exactly. It keeps
recently used 8 KB pages in RAM. If the working set fits, queries run at memory speed. If it
does not, every query touches the SSD, and the same query becomes a thousand times slower
with no change to the SQL. When someone says "the database got slow and we didn't change
anything", this is usually what happened: the data grew past the buffer pool.

### Virtual memory, briefly

Every process sees its own flat address space; the OS maps those to real pages. When RAM runs
out, pages are written to **swap** on disk. A program whose working set exceeds RAM starts
paging, and because disk is 100,000× slower, it does not degrade gracefully — it falls off a
cliff. On a server the usual advice is to disable swap and let the process be killed instead,
because a dead process restarts in seconds and a thrashing one takes the machine with it.

### NUMA, for completeness

On large multi-socket servers, memory is attached to particular processors. Reading memory
attached to another socket is roughly twice as slow. That is **NUMA** — non-uniform memory
access — and it matters for databases pinned to cores. Worth knowing the word; rarely worth
more than a sentence in an interview.

---

## 6. The numbers

**The one to memorise**, in the form interviewers ask for:

```
RAM read           :        80 ns
SSD read           :   100,000 ns   =    1,250x slower
HDD seek + read    : 10,000,000 ns  =  125,000x slower
```

So: **SSD is about a thousand times slower than RAM. A spinning disk is about a hundred
thousand times slower.** Those two ratios answer the question directly.

**How much you can read in one second:**

```
RAM  : 1 s / 80 ns          = 12,500,000 random reads
SSD  : 1 s / 100 us         =     10,000 random reads   (per queue; NVMe parallelises to ~500,000 IOPS)
HDD  : 1 s / 10 ms          =        100 random reads
```

**One hundred random reads per second from a spinning disk.** That number single-handedly
explains why databases have indexes, why full table scans are feared, and why the industry
moved to SSDs.

**Sizing a cache, properly.** A service holds 500 GB of data, and 20% of it is accessed 80% of
the time:

```
hot set = 500 GB x 0.20 = 100 GB
```

A machine with 128 GB of RAM holds the hot set, giving roughly an 80% hit rate before any
tuning. Now the average read time:

```
0.80 x 80 ns + 0.20 x 100,000 ns = 64 + 20,000 = 20,064 ns = 20 us
```

Push the hit rate to 99%:

```
0.99 x 80 + 0.01 x 100,000 = 79 + 1,000 = 1,079 ns = 1 us
```

**Twenty times faster from 19 percentage points of hit rate.** That is the argument for
spending money on RAM, and it is arithmetic rather than assertion.

**Serving a page: where the time actually goes.**

```
parse request, route             :      0.05 ms
session lookup in Redis (RAM+net):      0.60 ms
database query, buffer pool hit  :      1.00 ms
database query, buffer pool miss :     10.00 ms
render template                  :      2.00 ms
                                       --------
all cached                       :      3.65 ms
one page miss                    :     12.65 ms   (3.5x, from one miss)
```

**Reading a 1 GB file:**

```
sequential from SSD  : 1 GB / 3 GB/s  = 0.33 s
sequential from HDD  : 1 GB / 200 MB/s = 5 s
random 4 KB from HDD : 262,144 reads x 10 ms = 2,621 s = 44 minutes
```

**Half a second against forty-four minutes**, for the same gigabyte. Access pattern beats
hardware.

**Cost of a cache miss, expressed as wasted work.** At 3 GHz, a processor does 3 cycles per
nanosecond:

```
one RAM access = 80 ns = 240 cycles of work the CPU could have done instead
one SSD read = 100 us = 300,000 cycles
one HDD seek = 10 ms = 30,000,000 cycles
```

Thirty million instructions' worth of doing nothing, per disk seek. That is why blocking I/O
costs so much and why the asynchronous model from
[day 007](../day-007-space-complexity/README.md) exists.

---

## 7. The trade-offs

**RAM is fast, expensive and forgets.** About 40× the cost per byte of SSD and roughly a
thousand times the speed, and everything vanishes on restart. Which is why in-memory systems
are chosen for data that can be rebuilt — caches, sessions, leaderboards, rate-limit counters
— and why using Redis as the only copy of something is a decision that needs saying out loud
rather than drifting into.

**SSD is the modern default and it wears out.** Fast, cheap enough, durable, no moving parts.
The costs are real but rarely decisive: flash cells have limited write cycles, so
write-heavy workloads shorten drive life, and writes get slower as the drive fills because
there are fewer pre-erased blocks. Both are managed by the drive and both are why
write-amplification is a real metric in database operations.

**Spinning disk survives on price per byte and nothing else.** Two cents a gigabyte, and a
hundred random reads per second. It is genuinely correct for backups, archives, and
large-file sequential workloads — video, logs, data lakes — and genuinely wrong for anything
that reads randomly.

**Caching buys speed and charges you correctness.** Every cache introduces the possibility
that your copy is out of date. The whole discipline of invalidation exists because of this,
and the trade is always the same: how stale can this be, and what does it cost if it is? For
a product catalogue, minutes are fine. For an account balance, nothing is fine, and the right
answer is not to cache it.

**Sequential versus random is often a bigger lever than the hardware.** The 1 GB example
above is half a second against forty-four minutes on the *same* drive. So before spending
money moving down the ladder, it is worth asking whether the access pattern can be changed
instead — batch the reads, sort by key, store together what is read together. That question
is usually cheaper than the hardware and it is what a good design conversation gets to.

**I would not put this in memory if...** the dataset is much larger than RAM and access is
genuinely uniform, so no hot set exists and a cache would thrash. Or if losing it is
unacceptable and I am not willing to pay for replication and persistence. Or if it is written
far more often than it is read, in which case a cache adds invalidation work for very little
benefit — a write-heavy counter is better handled by a store designed for writes than by a
cache in front of one designed for reads.

---

## 8. In the interview

### How it gets asked

- *"How much slower is a disk read than a memory read?"* — the direct version. Give ratios
  and at least one absolute number.
- *"Why is Redis fast?"* — the applied version. The answer is "it's on the memory rung", not
  "it's written well".
- *"Estimate how long this operation takes."* — back-of-the-envelope, and these numbers are
  the raw material.
- *"Our database got slow and we didn't change anything. What happened?"* — usually the
  working set outgrew the buffer pool.

### What to say out loud, in the first ninety seconds

1. **Give the ladder in order.** *"Registers, L1, L2, L3, RAM, SSD, spinning disk, network."*
2. **Give the two ratios that matter.** *"RAM is about 80 nanoseconds. SSD is about 100
   microseconds, so roughly a thousand times slower. A spinning disk seek is about 10
   milliseconds — a hundred thousand times slower than RAM."*
3. **Make it human.** *"If a CPU cycle were one second, RAM would be four minutes, an SSD
   read four days, and a disk seek about eleven months."*
4. **Name the block effect.** *"And nothing reads one byte. The CPU fetches 64-byte cache
   lines, disks read 4 KB pages. So sequential access is enormously cheaper than random —
   the same gigabyte is half a second sequentially off an SSD and could be forty minutes if
   read randomly off a spinning disk."*
5. **Say what follows.** *"Which is why every layer caches: keep the hot data one rung up.
   And why the hit rate matters so much — at 90% hit rate the misses still dominate the
   average completely."*
6. **Give the boundary.** *"The two lines that matter are volatility — everything above RAM
   is lost on restart — and the network, where you're depending on another machine being
   alive."*

### The follow-ups

**"So why not keep everything in RAM?"**
Cost and durability. RAM is roughly forty times the price per byte of SSD, so a 20 TB dataset
is a few hundred dollars on disk and a six-figure hardware problem in memory. And RAM is
volatile — a restart loses everything, so anything that must survive needs writing down
anyway. That said, "keep the hot subset in RAM" is almost always right, and the useful
question is what fraction is hot. If 20% of the data serves 80% of the reads, buying enough
RAM for that 20% gets most of the benefit for a fifth of the price.

**"Why is a database index worth having, in these terms?"**
Because it converts a large number of reads into a small number. A full scan of a million-row
table on a spinning disk that does a hundred random reads per second is not a query, it is a
coffee break. An index turns that into a handful of page reads by narrowing the search before
touching the data. In hierarchy terms, the index is small enough to stay cached in RAM while
the table is not — so you pay memory-speed lookups to avoid disk-speed scans. That is also
why an index that does not fit in memory is a much weaker index.

**"Our reads got slow and nothing changed. What would you check?"**
First, whether the working set outgrew the buffer pool or the cache. That transition is not
gradual: while the hot data fits in RAM, reads are microseconds; the moment it does not, the
same query hits the SSD and is a thousand times slower with no code change. I'd look at cache
hit rate over time, not at the current value. Second, whether the access pattern became more
random — a new query, or data that used to be clustered and is now scattered after many
updates. Third, whether the machine started swapping, which is the same cliff one level down.

**"How would you estimate the time for a request that does three database queries?"**
I'd break it into hierarchy steps and add them. Say each query is a buffer-pool hit at about
1 ms, plus a network round trip within the data centre at 0.5 ms each way — so about 2 ms per
query, 6 ms for three. Plus maybe 2 ms of application work. So under 10 ms if everything is
cached. Then I'd ask what happens at the tail: if one query misses the buffer pool, that is
10 ms of SSD instead of 1, so the p99 is several times the median. The useful output of this
exercise is usually not the average — it is noticing where the variance comes from.

### A model answer

> "The hierarchy, top to bottom, is registers, then L1, L2 and L3 cache, then main memory,
> then SSD, then spinning disk, then the network.
>
> The absolute numbers I carry are: L1 about 1 nanosecond, RAM about 80 nanoseconds, an SSD
> read about 100 microseconds, and a spinning-disk seek about 10 milliseconds. So SSD is
> roughly a thousand times slower than RAM, and a spinning disk is roughly a hundred thousand
> times slower.
>
> Those are hard to feel, so I scale them: if one CPU cycle were one second, an L1 hit is
> three seconds, RAM is four minutes, an SSD read is four days, and a disk seek is about
> eleven months. A round trip to a data centre on another continent would be four years.
>
> Two things follow. First, nothing reads one byte — the CPU fetches 64-byte cache lines and
> disks read 4 KB pages — so sequential access is vastly cheaper than random. Reading a
> gigabyte sequentially off an SSD is about a third of a second; reading the same gigabyte as
> scattered 4 KB reads off a spinning disk is over forty minutes. That's the same hardware and
> a different access pattern, and it's often a bigger lever than buying faster storage.
>
> Second, every layer caches, because the gaps are too big not to. The CPU caches RAM, the OS
> caches disk pages, the database has a buffer pool, the application has Redis, the CDN caches
> at the edge. And the arithmetic on hit rates is unforgiving: at 90% hits with an 80
> nanosecond RAM read and a 100 microsecond SSD read, the average is about 10 microseconds —
> the misses are 99% of the time spent. Getting to 99% takes that to 1 microsecond. So 'we
> have a cache' is a much weaker statement than 'our hit rate is 99%'.
>
> The last thing I'd flag is that two of these boundaries aren't about speed. Everything above
> RAM disappears on restart, which decides what can live in Redis. And the network isn't just
> slow, it's a dependency on another machine — it can fail in ways local storage cannot."

That answer gives the order, the absolute numbers, the ratios, a memorable scale, the
sequential-versus-random consequence, the cache-hit arithmetic, and the two non-speed
boundaries.

---

## 9. Recall card

1. **The ladder:** register → L1 → L2 → L3 → RAM → SSD → HDD → network. Each step is roughly
   100–1,000× slower and cheaper per byte.
2. **The three numbers:** RAM **80 ns**, SSD **100 µs**, disk seek **10 ms**. So SSD is
   ~1,000× slower than RAM, and a spinning disk ~100,000× slower.
3. **If one cycle were one second:** L1 = 3 s, RAM = 4 minutes, SSD = 4 days, disk seek =
   11 months, cross-world network = 16 years.
4. **Nothing reads one byte.** 64-byte cache lines, 4 KB disk pages. Sequential access can be
   100× faster than random on the same hardware.
5. **Misses dominate the average.** 90% hit rate on RAM-vs-SSD still averages 10 µs; 99%
   averages 1 µs. And everything above RAM is volatile.
