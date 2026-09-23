---
day: 39
track: system-design
title: "Wide-column and time-series stores"
phase: "Databases from zero"
status: written
---

# Day 039 · System Design — Wide-column and time-series stores

**After today you can:** You can say what Cassandra's data model really is and when a time-series store is right.

**The interviewer asks it as:** *Which database would you pick for storing metrics, and why?*

---

## 1. What this is, and why they ask it

A **wide-column store** — Cassandra is the name to know — organises data by two keys: a
**partition key** that decides which machine (and which bucket on it) a row belongs to, and
**clustering columns** that keep rows *sorted inside* that bucket. One request fetches a slice of
one partition, in order — and almost nothing else is cheap. A **time-series store** — InfluxDB,
TimescaleDB, Prometheus — is the same instinct specialised for measurements over time: enormous
append-only write volume, queries that are always "this thing, this time range", and data that
ages out on schedule.

Interviewers reach for these when the design has a firehose in it — metrics, chat messages,
sensor readings, activity feeds — because the stores that survive firehoses all made the same
trade, and they want to hear you say it: **you must know your queries when you design the table.**
Cassandra powers exactly these workloads at Discord, Netflix and Apple scale, and "why not just
Postgres?" is the follow-up that sorts slogan-repeaters from engineers.

---

## 2. The story

The mailroom in the old head office is a wall of pigeonholes, one per department, and Xavier has
sorted the post there for eleven years.

His rule is the wall's whole design: everything for a department goes in that department's hole,
and inside the hole, newest on top. A courier drops forty envelopes at ten o'clock; Xavier reads
only the department name, walks the wall once, and drops each envelope on top of its stack. He
never rearranges anything, never reads past the first line of an address, never goes back. Sorting
happens by *where things land*, not by work done later. That is why the morning flood, three
hundred envelopes some days, takes him under twenty minutes.

Collection is the same story in reverse. The accounts clerk comes at four and says: whatever came
for us since Tuesday. One hole, top of one stack, stop when the dates go past Tuesday — ten
seconds, and the envelopes are already in order. Nobody ever asks him for anything else, because
the wall has trained the whole building in what it is good at.

Once, a new auditor asked for every envelope from a particular insurance company, across all
departments, for the whole year. Xavier did it — every hole, every stack, top to bottom, an
afternoon on a stool — and then told her, kindly, that next time she should ask the sender for
their list instead. The wall answers by department and date. It does not answer by sender. No
amount of effort at collection time fixes what the landing rule never recorded.

And every January, the bottom of every stack goes into boxes for the basement, and after three
years the boxes are pulped. Nobody decides envelope by envelope. Old post ages out on a schedule,
because a pigeonhole that keeps everything forever eventually holds everything and finds nothing.

The wall, Xavier says, was designed by his predecessor around one question asked a hundred times a
day. Design it around the question, and the question costs nothing.

---

## 3. The idea in plain English

Xavier's wall is a Cassandra table. The department name is the **partition key**. Newest-on-top is
the **clustering order**. The auditor is the query you did not design for. And January is
**retention**.

### The two-part key, and what each part buys

A Cassandra table's primary key has two jobs, split explicitly:

```sql
CREATE TABLE messages (
    channel_id  bigint,          -- partition key: WHICH pigeonhole
    sent_at     timeuuid,        -- clustering column: ORDER inside it
    author_id   bigint,
    body        text,
    PRIMARY KEY ((channel_id), sent_at)
) WITH CLUSTERING ORDER BY (sent_at DESC);
```

The **partition key** is hashed to place the row — [day 037](../day-037-prefix-sums/README.md)'s
key-value placement, deciding both the machine in the cluster and the bucket on it. The
**clustering columns** sort rows *within* the partition, physically. So the query the table was
built for — *the latest 50 messages in this channel* — is: hash to one machine, find one
partition, read the top of one sorted run. One seek, sequential read, already in order —
Xavier's ten seconds.

This is [day 026](../day-026-strings-revision/README.md)'s primary key split into its two real
jobs, and it is the whole data model. There are no joins, no foreign keys, and — effectively — no
queries that do not start with the partition key. The auditor's question ("by sender, across all
partitions") is a full cluster scan, and the honest Cassandra answer is Xavier's: that question
needs **its own table**, written at the same time — one table per query shape, copies maintained
at write time, [day 036](../day-036-two-pointers-revision/README.md)'s arranged-for-serving taken
to its disciplined extreme.

### Why writes are the superpower

Cassandra's storage engine is the **log-structured merge tree** from
[day 031](../day-031-fixed-window/README.md) — writes append; sorting happens by where things
land, then by background merging; nothing is updated in place. Add that every node accepts writes
(no single leader — the distributed machinery is a later phase; today, just the consequence), and
you get the headline: write throughput that scales nearly linearly with machines. Discord's
message history, Netflix's viewing events, Apple's iCloud metadata — this store, this reason.

### Time series: the same instinct, specialised

Metrics are the extreme case: writes are *only* appends of `(thing, timestamp, value)`; reads are
*only* "this thing, this window, aggregated"; and old data loses value on a schedule. Time-series
stores hard-code all three:

- **Partition by thing and time bucket**, so every query is one pigeonhole slice — the Cassandra
  idea, made automatic (TimescaleDB calls the buckets chunks; Influx, shards).
- **Compress brutally** — timestamps arrive at fixed intervals and values drift slowly, so
  delta-encoding gets 10–20× ([day 037](../day-037-prefix-sums/README.md)'s running differences,
  used as a compression trick: store the small deltas, not the big values).
- **Age data out by policy** — keep raw data 15 days, keep 5-minute averages a year, drop the
  rest: **retention and downsampling**, Xavier's January, built into the store.

Prometheus owns the pull-based metrics niche; InfluxDB the push-based one; TimescaleDB is the
"Postgres with time-series superpowers" answer — a real Postgres extension, so SQL, joins and one
operational stack survive.

---

## 4. The picture

The wall, as a cluster:

```
                     hash(channel_id) picks the node

   node A                node B                node C
   +---------------+     +---------------+     +---------------+
   | channel 17    |     | channel 4     |     | channel 92    |
   |  msg 09:41 <- |     |  msg 09:40    |     |  msg 09:44    |
   |  msg 09:38    |     |  msg 09:22    |     |  msg 09:41    |
   |  msg 09:31    |     |  ...          |     |  ...          |
   |  ...sorted... |     +---------------+     +---------------+
   +---------------+     | channel 51    |
   | channel 33    |     |  ...          |
   |  ...          |     +---------------+
   +---------------+

 "latest 50 in channel 17"  -> one node, one partition, top of one sorted run
 "all messages by user 7"   -> EVERY node, EVERY partition  (the auditor)
```

**What to notice:** the fast query never fans out; the undesigned query always does. The
difference is not indexes or tuning — it is where the landing rule put things.

The time-series lifecycle, on one axis:

```
      now                  15 days                    1 year
 ------|---------------------|--------------------------|--------> age
  raw points             downsampled to               dropped
  1/sec, compressed      5-min averages
  ~1.5 bytes/point       288 points/day/series

 writes only ever land at "now" -> the newest chunk stays hot in memory,
 old chunks are sealed, compressed, and eventually deleted whole.
```

**What to notice:** deletion happens by dropping sealed chunks whole — cheap, like pulping a box —
never by hunting individual rows, which is exactly what a B-tree store would have to do.

---

## 5. How it actually works

### Writing and reading a partition

A write hashes the partition key, lands on the owning nodes, appends to the commit log (the
write-ahead log from [day 025](../day-025-pattern-matching/README.md), same job) and into an
in-memory table; sealed memtables flush to sorted files that background **compaction** merges —
the LSM lifecycle from [day 031](../day-031-fixed-window/README.md), verbatim. A read finds the
partition, merges the memtable and the few sorted files that could hold the slice, and streams
rows in clustering order. Point lookups and slices: fast. Anything without the partition key:
a cluster-wide scatter, which the query language makes you say out loud
(`ALLOW FILTERING` — a phrase that should read as a warning label).

### Modelling: one table per query

The discipline that follows from the model, and the thing interviewers probe: you write the
queries first, then a table *per query shape*, and the application writes each event to all of
them. Messages by channel *and* messages by author? Two tables, two writes per message — the
application's own fan-out, [day 029](../day-029-read-write-pointer/README.md)'s copies-with-owners
again. What Cassandra will not give you: joins, ad-hoc filters, cross-partition transactions
([day 033](../day-033-window-with-a-map/README.md)'s lightweight transactions are a single-
partition compare-and-set, and expensive). The store is a set of pigeonhole walls, each built for
its one question.

### Two Cassandra failure modes worth naming

**Hot partitions**: partition by `celebrity_user_id` and one pigeonhole takes the whole flood —
one node melts while the cluster idles. The fix is in the key: add a bucket to spread it
(`(user_id, day)` or `(user_id, hash % 16)`), at the cost of collecting from several partitions on
read — [day 035](../day-035-choosing-the-pattern/README.md)'s hot-row arithmetic, at partition
scale. **Unbounded partitions**: a partition that only ever grows (one channel, forever) slows
reads and compaction as it fattens — same disease as [day 038](../day-038-subarray-sum-k/README.md)'s
unbounded embedded array, same cure: bucket by time, `(channel_id, month)`. Both are landing-rule
decisions; neither is fixable later by tuning.

### The time-series engines, one line deeper

**TimescaleDB**: a Postgres extension that auto-partitions a normal table into time chunks —
you keep SQL, joins against business tables, and one backup story; right when metrics live *next
to* an application. **InfluxDB**: purpose-built, its own query language, tags-and-fields model;
right when metrics *are* the application. **Prometheus**: pull-model scraping for infrastructure
monitoring, local storage, PromQL — the operational default for watching services, less a general
database than the monitoring stack's heart. All three share the machinery in §4: time-bucketed
chunks, delta compression, retention by policy.

---

## 6. The numbers

### The firehose, sized

```
10,000 servers × 100 metrics × every 10 s  =  100,000 points/second
   × 86,400 s  ≈  8.6 billion points/day

as naive Postgres rows (~100 bytes each incl. index):  ~860 GB/day
time-series compressed (~1.5-2 bytes/point):           ~15-17 GB/day   (~50×)
```

That 50× is delta encoding earning its keep: timestamps at fixed intervals compress to almost
nothing, and slowly-drifting values to a few bits.

### Retention arithmetic

```
raw forever:            15 GB/day × 365           ≈ 5.5 TB/year, growing
15 days raw + 5-min averages for a year:
   raw window:          15 × 15 GB                ≈ 225 GB
   downsampled: 10,000 × 100 series × 288/day × 365 × ~2 B ≈ 210 GB
   total                                          ≈ half a TB, FLAT
```

Retention is not housekeeping; it is the difference between a system that grows forever and one
that plateaus. Say the two-tier policy in interviews — raw briefly, aggregates long.

### Why per-node write throughput differs

```
B-tree write (Postgres): find the page, read-modify-write in place,
                         plus every index          -> thousands-tens of
                                                      thousands of rows/s/node
LSM write (Cassandra):   append to log + memtable  -> ~10,000-50,000+
                                                      writes/s/node, and
                         nearly linear with nodes  -> millions/s per cluster
```

Day 031's read-favouring versus write-favouring shapes, now with product names attached. The
honest counterweight: at 100,000 points a second, a *single* TimescaleDB node with batched
inserts also copes — the cluster is for when one node's ceiling, or one node's failure, is the
problem.

### The query the wall answers

```
"CPU for server-42, last 6 hours, 1-min averages":
  one series, one or two chunks, ~2,160 points -> a few ms

"which of 10,000 servers averaged > 90% yesterday":
  10,000 series × 8,640 points = 86M points scanned -> seconds,
  UNLESS yesterday's 5-min rollups exist: 10,000 × 288 = 2.9M -> sub-second
```

Downsampling is not only retention — it is precomputation,
[day 037](../day-037-prefix-sums/README.md)'s prepare-once trade applied to aggregates.

---

## 7. The trade-offs

### What the wall costs

Everything is decided at landing time: **queries must be known up front** (a new question means a
new table and a backfill, not a new index), **copies multiply** (one table per query shape, all
written by the application, all needing owners), and **the relational comforts are gone** — no
joins, no ad-hoc filters, transactions only within a partition. Against that: writes that scale
with machines, reads that never fan out, and data that ages out for free.

### Choosing within the family

Metrics beside an existing Postgres application, at thousands of points a second:
**TimescaleDB** — one stack, SQL, joins to business data. Infrastructure monitoring:
**Prometheus**, because the ecosystem (scraping, alerting, dashboards) is the product. Metrics as
the product, or write volume beyond one node: **InfluxDB or Cassandra**, and the operational
weight that comes with a cluster. The deciding questions are always the same three: points per
second, queries known or ad-hoc, and who operates it.

### I would not use it if...

**I would not use Cassandra when the queries are still being discovered** — every new question is
a new table, and a young product asks new questions weekly; that is
[day 036](../day-036-two-pointers-revision/README.md)'s relational home ground. **I would not use
it below real scale** — a cluster's operational cost buys nothing that one Postgres node was not
already doing at 10,000 writes a second. **And I would not put metrics in plain Postgres rows** —
uncompressed points and per-row deletion lose 50× storage and make retention a nightly `DELETE`
that fights `VACUUM` ([day 033](../day-033-window-with-a-map/README.md)'s bloat, self-inflicted);
TimescaleDB exists precisely to keep Postgres and fix those two things.

### The honest sentence

> A wide-column store is a promise to the database: *I already know my questions.* Keep the
> promise and it serves them at any scale; break it and every new question is a schema project.
> The interview answer is knowing which promise the product can actually make.

---

## 8. In the interview

### How it gets asked

- *"Which database for metrics, and why?"* — the hub question; they want the write rate, the
  query shape, and retention named before a product is.
- *"What is Cassandra's data model, actually?"* — partition key places, clustering columns sort;
  one table per query.
- *"Design Discord's message storage."* — the canonical wide-column case study: partition by
  channel (bucketed), cluster by time.
- *"Why not just Postgres?"* — the counter-question; answer with numbers, and concede it below
  scale.
- *"How do you handle a celebrity / a channel that never stops growing?"* — hot and unbounded
  partitions; the fix is in the key.

### What to say out loud, in the first ninety seconds

1. **Size the firehose first.** *"Ten thousand servers, a hundred metrics, every ten seconds —
   a hundred thousand points a second, 8.6 billion a day. That number picks the family."*
2. **Name the two keys and their jobs.** *"Wide-column means: partition key decides where —
   machine and bucket; clustering columns keep rows sorted inside. The designed query reads one
   sorted slice of one partition."*
3. **Say the promise.** *"The model requires knowing the queries up front — one table per query
   shape, no joins, no ad-hoc filters. Metrics keep that promise naturally: always 'this series,
   this window'."*
4. **Add the time-series specials.** *"A time-series store adds delta compression — 50× on
   metrics — and retention with downsampling: raw for 15 days, 5-minute averages for a year, so
   storage plateaus instead of growing."*
5. **Give the decision.** *"Beside an existing app at modest volume: TimescaleDB. Infra
   monitoring: Prometheus. Metrics as the product at cluster scale: InfluxDB or Cassandra."*

### The follow-ups

**"Design the message table for Discord. Walk me through the key."**
The query is fixed and known: the latest N messages in a channel, older pages on scroll. So:
partition by channel, cluster by a time-ordered id descending — the read is one partition's top
slice, in order, no sort at read time. Then the two failure modes force one refinement each. A
channel lives for years, so the partition is unbounded — it fattens forever and compaction
suffers — so the partition key becomes `(channel_id, time_bucket)`, say a month: reads usually
touch one bucket and occasionally step to the previous one at a page boundary. And a huge public
channel is a hot partition — one bucket taking a whole flood — which the time bucket already
softens and a further split (`hash % k` added to the key) can spread at the cost of merging k
slices on read. Any second question — messages by author, search — is its own table or its own
system, written at the same time; I would say that at design time, not discover it later. This is,
concretely, how Discord stores messages, and the reasoning is the reusable part: query first, key
second, then stress the key with "does it grow forever?" and "can one value take the flood?".

**"Why is Cassandra so fast at writes when Postgres isn't? Same hardware."**
Different promises, different physics. A Postgres write finds the row's page in a B-tree,
modifies it in place, and updates every index — random reads and writes, multiplied by
day 030's every-index-is-a-write rule, all to keep the data readable in any order at any moment.
A Cassandra write appends to a commit log and an in-memory table, and sorting into files happens
later, in the background, by sequential merges — day 031's LSM shape: it defers and batches the
expensive part. Add no-single-leader, so every node takes writes, and throughput scales with the
cluster. The price is symmetrical and worth saying: reads must merge several sorted files, ad-hoc
reads are poor, and compaction consumes background I/O forever. Postgres spent the write to make
every future read cheap; Cassandra spends the read to make every write cheap — neither is free,
and the workload picks the winner. Metrics and messages are write-dominated with narrow reads, so
they pick the LSM.

**"You said don't use plain Postgres for metrics — but the team knows only Postgres. Now what?"**
TimescaleDB, and it is a genuinely good answer rather than a compromise. It is a Postgres
extension: the metrics table *is* a Postgres table, so the team keeps SQL, joins to business
data, backups and the operational knowledge they have — one stack. Underneath, it fixes exactly
the two things plain rows get wrong: it auto-partitions by time into chunks, so retention is
`drop_chunks` — deleting sealed chunks whole, no million-row `DELETE` fighting VACUUM — and its
columnar compression gets metrics within sight of the purpose-built stores' 10–20×. Continuous
aggregates give the downsampling tier. Honest limits, also worth saying: one node's write ceiling
(batched, hundreds of thousands of points a second — usually plenty), and clustering beyond that
is where the purpose-built systems pull ahead. So the decision sentence is: below cluster scale,
the team's stack wins; at cluster scale, the workload's stack wins.

### A model answer

> "Metrics first means sizing the firehose: say ten thousand servers, a hundred metrics each,
> every ten seconds — a hundred thousand points a second, 8.6 billion a day. Three properties
> follow: writes are append-only and enormous; reads are always 'this series, this time range,
> aggregated'; and old data loses value on a schedule. The right store hard-codes all three.
>
> That is a time-series database. It partitions by series and time bucket, so a query reads one
> sorted slice — Cassandra's partition-and-clustering model, specialised. It delta-compresses —
> fixed-interval timestamps and drifting values go from a hundred bytes a point as database rows
> to under two, a 50× difference that decides whether a year of data is terabytes or hundreds of
> gigabytes. And it retains by policy: raw points for fifteen days, five-minute averages for a
> year, dropped chunks deleted whole — storage plateaus instead of growing.
>
> Which product depends on context. Metrics beside an existing Postgres application:
> TimescaleDB — it's a Postgres extension, so the team keeps SQL and one operational stack, and it
> handles this write rate on a node. Infrastructure monitoring: Prometheus, because scraping,
> alerting and dashboards come with it. Metrics as the product, or volume past one node:
> InfluxDB, or Cassandra with a hand-built schema.
>
> What I'd not do is plain Postgres rows — 860 gigabytes a day uncompressed, and retention as a
> nightly DELETE that fights VACUUM — and I'd not reach for a Cassandra cluster below the scale
> that needs one. The model's price is the same everywhere: these stores require the queries to
> be known up front. Metrics keep that promise; a product still discovering its questions does
> not, and belongs relational."

---

## 9. Recall card

- **Wide-column = two-part key:** partition key → which machine and bucket (hashed); clustering
  columns → sort order inside. The designed query reads one sorted slice; everything else fans
  out to the whole cluster.
- **One table per query, written at write time** — no joins, no ad-hoc filters; a new question is
  a new table, not a new index. The promise: *I already know my queries.*
- **Writes scale because of the LSM** — append, flush, background-merge (day 031), every node
  accepts writes: millions/s per cluster. Price: read merges and compaction forever.
- **Key stress-test: unbounded partitions (bucket by time) and hot partitions (spread the key)** —
  both are landing-rule decisions, unfixable by tuning later.
- **Time series = the model + compression + retention:** delta encoding ~50×; raw briefly,
  downsampled aggregates long, chunks dropped whole. TimescaleDB beside an app; Prometheus for
  infra; InfluxDB/Cassandra at cluster scale.
