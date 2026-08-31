---
day: 107
track: system-design
title: "Sharding, part two: rebalancing and hot spots"
phase: "Scaling fundamentals"
status: written
---

# Day 107 · System Design — Sharding, part two: rebalancing and hot spots

**After today you can:** You can describe resharding without downtime and identify a hot shard.

**The interviewer asks it as:** *One shard is taking 60 percent of the traffic. Now what?*

---

## 1. What this is, and why they ask it

[Yesterday](../day-106-bst-property/README.md) you chose a shard key. Today the shards are live, and two
things have gone wrong: you need **more** of them, and one of them is doing far more work than the
others.

Three sentences. Adding a shard under plain `hash % N` remaps almost every key, which means moving almost
all your data — so the standard fix is an **indirection**: many more logical shards than physical
machines, so growing means moving whole logical shards rather than rehashing anything. Moving data while
the system is serving traffic is a four-phase procedure that every large migration uses, and knowing the
phases is worth more than knowing the theory. And **hot spots are not a hashing problem** — a perfect hash
distributes *keys* evenly and cannot distribute *traffic* evenly, because some keys are a thousand times
more popular than others.

They ask it because part one is a design question and part two is an operations question, and the second
one is where systems actually fail. *"One shard is taking 60 percent of the traffic"* has four distinct
causes with four different fixes, and a candidate who diagnoses before prescribing is doing the thing the
question is testing.

---

## 2. The story

The records office had been running with four rooms for two years and both of the remaining problems came
to a head in the same month.

The first was space. The rooms were full. They were given a fifth room, and somebody cheerfully suggested
changing the rule from divide-by-four to divide-by-five.

The head clerk worked out what that meant on the back of an envelope and refused.

Under divide-by-four, a document numbered 4,117 was in room two. Under divide-by-five it belonged in room
three. He checked a few more and then stopped checking, because the pattern was obvious: **almost every
document in the building would have to move.** Four rooms' worth of documents carried down a corridor to
be put in five rooms, for the sake of adding one room.

What they did instead was the thing the youngest clerk had been arguing for since the beginning, which
nobody had understood until then.

He said: stop thinking about rooms. Divide by **a hundred** instead of by four, and call those hundred
things *bundles*. Bundle nought to bundle ninety-nine. Then keep a list on the wall saying which bundles
live in which room — twenty-five bundles in each room to start with.

When the fifth room arrived, they did not change the division at all. They moved twenty bundles — five
from each of the four rooms — into room five, and updated the list on the wall. One document in five
moved instead of four in five, and the rule for finding a document never changed.

The second problem was worse and had nothing to do with space.

Room three had a queue every morning and the others did not. It was not that room three had more
documents — it had exactly the same number. It was that one particular housing layout near the ring road
was being subdivided and sold in pieces, and every one of those transactions referenced the same parent
document, and that document was in room three.

They tried moving that bundle to room five. For about a week the queue was outside room five.

What actually worked was two things done together. They photocopied the parent document and put a copy in
every room, so anybody could see it without going to room three. And for the three or four documents that
genuinely could not be copied, they gave those a room of their own — a small room with one clerk who did
nothing else.

The head clerk's line about it afterwards was that dividing the documents evenly had never been the
problem. **The documents were even. The people were not.**

---

## 3. The idea in plain English

The office has just discovered the two operational problems of sharding: **resharding** and **hot spots**,
and it landed on both standard answers.

- Dividing by a hundred instead of by four is **logical (or virtual) shards**.
- The list on the wall is the **shard map**.
- Moving twenty bundles is **rebalancing** — moving whole logical shards, not rehashing keys.
- Room three's queue is a **hot shard**, caused by a **hot key**.
- Photocopying the parent document is **caching the hot key**.
- The small room with one clerk is a **dedicated shard for the outlier**.

### Why plain `hash % N` cannot grow

```
 4 shards:  shard = hash(key) % 4
 5 shards:  shard = hash(key) % 5

 key 4117:  4117 % 4 = 1  ->  shard 1
            4117 % 5 = 2  ->  shard 2      MOVED

 fraction of keys that stay put when going from N to N+1:  about 1/(N+1)
   4 -> 5:   ~20% stay, 80% move
   8 -> 9:   ~11% stay, 89% move
```

**Almost everything moves, to add one machine.** That is why nobody runs plain modulo in production, and
it is the problem both of today's techniques exist to solve.

### Fix one: many logical shards, few physical machines

Decide **once, at the start**, on a large fixed number of logical shards — 256, 1,024, 4,096 — and then
map them onto machines.

```
 shard_id  = hash(key) % 1024        <- FIXED FOREVER. Never changes.
 machine   = shard_map[shard_id]     <- a small table you can change

 8 machines:   128 logical shards each
 add a 9th:    move ~114 logical shards' worth of data (1/9 of the total)
               and update the map. The hash function is untouched.
```

**The hash never changes; only the map does.** Adding a machine moves `1/(N+1)` of the data — the minimum
possible — and every client that reloads the map immediately routes correctly.

Two consequences worth stating:

- **The logical shard count is a hard ceiling on your machine count.** 1,024 logical shards means at most
  1,024 machines, ever, without a genuine resharding project. Pick generously; the cost of extra logical
  shards is small.
- **Pick a power of two**, so a logical shard can be split cleanly later if you ever do need more.

This is what **Vitess** calls keyspaces and shards, what **Citus** calls shards, what **Cassandra**'s
token ranges do, and what **Redis Cluster**'s 16,384 hash slots are. **Redis Cluster's number is worth
knowing: 16,384 slots, fixed, and resharding means moving slots.**

### Fix two: consistent hashing

The other approach, and [tomorrow's](../day-108-validating-a-bst/README.md) subject in full: place both
keys and machines on a ring, and a key belongs to the next machine clockwise. Adding a machine steals a
slice from one neighbour and moves only `1/N` of the keys, with no map at all.

```
 logical shards      an explicit map; total control; the map must be distributed
 consistent hashing  no map; computed; less control over where things land
```

**Both solve the same problem.** Logical shards are more common in databases (you want to control
placement); consistent hashing is more common in caches and stateless routing (you want no coordination).

### Resharding without downtime: the four phases

This is the procedure, and it is the same for every migration of this shape. **Learn the four names.**

```
 1. DUAL WRITE     start writing to BOTH the old and the new location.
                   Reads still come from the old. Nothing is exposed yet.

 2. BACKFILL       copy the historical data to the new location, in batches,
                   while dual writes keep the tail current.

 3. VERIFY         read from both and compare. Log every mismatch. Do not
                   skip this and do not shorten it — this phase is where you
                   find the bugs.

 4. CUT OVER       switch reads to the new location, one percent of traffic
                   at a time. Keep dual writes running for a while, so you
                   can switch back instantly.
                   Only then stop writing to the old, and only then delete.
```

**Every phase is reversible until the last.** That is the property that makes it safe, and it is why the
order matters: dual writes come first precisely so that a failed cutover costs nothing.

The detail people miss: **the backfill and the dual writes race.** A row copied by the backfill and then
updated by a dual write is fine; a row updated and *then* copied with stale data is not. The standard
answers are to make the copy idempotent and last-write-wins by timestamp, or to backfill only rows older
than the moment dual writes began.

### Hot spots: four causes, four fixes

**Diagnose first.** These have different fixes and prescribing before diagnosing is the failure mode.

**Cause 1 — a sequential shard key.** All new writes land on the newest shard. The append hotspot from
yesterday.
**Fix:** change the key, or prefix it with something that spreads. This is a design fix and it means
resharding.

**Cause 2 — a hot key.** One value is enormously more popular: a celebrity, a viral post, one huge
tenant.
**Fix:** you cannot split a single key across shards, so **cache it** — the photocopy — or **replicate
it** to every shard, or give it **its own shard**. For read-heavy hot keys a cache solves it completely,
because the requests never reach the shard.

**Cause 3 — skewed key distribution.** The keys themselves are uneven: sharding by country, by surname,
by `status = 'active'`.
**Fix:** a better key, usually a hash of something with high cardinality.

**Cause 4 — an uneven shard map.** The mapping simply put more logical shards, or more big ones, on one
machine.
**Fix:** rebalance. This is the easy one, and it is worth checking first because it is free.

### The one with no clean fix

**A single key whose data grows without limit.** One tenant with a billion rows, one conversation with
ten million messages, one celebrity's follower list.

You cannot split it, because a shard key value is atomic — every row with that value is on one machine by
definition.

**The only real answer is at design time**: make the key a **composite** so that no single value can grow
unboundedly.

```
 bad:   shard by  conversation_id           one huge conversation = one huge shard
 good:  shard by  (conversation_id, bucket) where bucket = month, or message_id / 10000
        -> one conversation is spread over many shards, and a query for
           "recent messages" touches one or two buckets
```

**Say this as a design-time rule, not a fix**, because by the time you have the problem it is a
resharding project.

### Detecting a hot shard

You cannot fix what you are not measuring. **Per-shard**, not aggregate:

```
 requests/second     per shard      -> traffic skew
 CPU and disk        per shard      -> the machine's view
 rows / bytes        per shard      -> storage skew (a different problem)
 p99 latency         per shard      -> the user's view
 top keys by traffic per shard      -> WHICH key, not just which shard
```

**That last line is the one that matters and the one people do not have.** "Shard three is hot" leads to
moving shard three. "Key `user:8823` is 40 percent of shard three's traffic" leads to caching one key,
which takes ten minutes.

---

## 4. The picture

Why plain modulo cannot grow, and what the indirection fixes.

```
 PLAIN MODULO — adding a machine remaps almost everything

  key 4117:   % 4 = 1   ->  machine 1
              % 5 = 2   ->  machine 2      MOVED
  key 4118:   % 4 = 2   ->  machine 2
              % 5 = 3   ->  machine 3      MOVED
  key 4120:   % 4 = 0   ->  machine 0
              % 5 = 0   ->  machine 0      stayed (1 in 5 do)

  4 -> 5 machines:  ~80% of ALL DATA moves.


 LOGICAL SHARDS — the hash never changes; the MAP changes

  hash(key) % 1024  ->  a logical shard, FIXED FOREVER
  shard_map[shard]  ->  a machine, CHANGEABLE

  8 machines                      9 machines
  ┌─────────────────────┐         ┌─────────────────────┐
  │ m0: shards 0-127    │         │ m0: shards 0-113    │
  │ m1: shards 128-255  │   -->   │ m1: shards 128-241  │
  │ ...                 │         │ ...                 │
  │ m7: shards 896-1023 │         │ m8: 114-127, 242-255│  <- the moved slices
  └─────────────────────┘         └─────────────────────┘

  ~1/9 of the data moves. The routing rule is untouched.
```

The four-phase migration, on a timeline:

```
 ──────────────────────────────────────────────────────────────────────►

 phase 1  DUAL WRITE     writes → old AND new        reads → old
          ├──────────────────────────────────────────────────────┤
 phase 2  BACKFILL       copy history in batches     reads → old
                    ├────────────────────┤
 phase 3  VERIFY        read both, compare, log      reads → old
                                    ├───────────────────────┤
 phase 4  CUT OVER      reads → new, 1% → 10% → 100%
                                                 ├──────────┤
          then stop dual writes                            ├───┤
          then delete the old data                             ├─┤

 EVERY PHASE IS REVERSIBLE UNTIL THE LAST TWO.
 That is the whole point of doing dual writes first.
```

The four hot-spot causes, and why the diagnosis matters:

```
 SYMPTOM: shard 3 is at 60% of total traffic

 cause                         evidence                        fix
 ---------------------------   -----------------------------   -----------------------
 1. sequential key             the NEWEST shard is hot,        change the key
                               and it moves over time          (a resharding project)

 2. one hot key                per-key stats: one key is        CACHE it, replicate it,
                               most of the shard's traffic      or give it its own shard
                                                                (minutes, not months)

 3. skewed key distribution    many keys, all landing on        change the key
                               one shard                        (a resharding project)

 4. uneven shard map           shard 3 holds more logical       rebalance the map
                               shards than the others           (free — CHECK THIS FIRST)

 prescribing before diagnosing is the failure. Cause 4 takes an hour;
 causes 1 and 3 take a quarter.
```

The unbounded key, which is the one with no fix:

```
 shard by conversation_id

   conversation 91:      1,200 messages        fine
   conversation 4471:    8,000 messages        fine
   conversation 88123:  40,000,000 messages    ← one shard, and it cannot be split

 you cannot divide a single key's rows across shards — every row with that
 value belongs to one machine BY DEFINITION.

 the ONLY answer is at design time:
   shard by (conversation_id, month)   or   (conversation_id, message_id / 10000)
   -> the big conversation is spread across many shards
   -> "recent messages" still touches only one or two buckets
```

---

## 5. How it actually works

### The shard map, concretely

```
 stored in:   ZooKeeper, etcd, Consul, or a small highly-available table
 size:        1,024 entries — a few kilobytes
 read by:     every client, cached locally, refreshed on a version bump
 changed by:  the rebalancing process, one entry at a time
```

**It is tiny and it is critical.** Every client caches it, so the failure mode to design for is a client
holding a stale map and writing to the wrong machine during a move. The standard defences are a **version
number** on the map that the shard checks and rejects if stale, and keeping the source shard able to
**forward** requests for a moved shard for a while afterwards.

### Moving one logical shard, live

```
 1. mark logical shard 217 as MOVING in the map (readers still go to the source)
 2. copy its rows from machine A to machine B
 3. start dual-writing shard 217 to both A and B
 4. catch up the delta accumulated during the copy
 5. briefly PAUSE writes to shard 217 — milliseconds
 6. flip the map entry to B; bump the map version
 7. resume; A forwards any stragglers for a grace period
 8. delete shard 217's rows from A
```

**Step 5 is the only moment of unavailability, and it is milliseconds, for one logical shard out of a
thousand.** That is the whole reason for the indirection: you are never moving more than a thousandth of
the system at a time, and only that thousandth pauses.

### Handling a hot key, in order of cost

```
 1. CACHE IT              minutes to deploy. Solves read-heavy hot keys
                          completely — the requests never reach the shard.

 2. REPLICATE IT          put a read-only copy on every shard. Good for small,
                          rarely-changing hot data (a config row, a popular
                          product's details).

 3. SPLIT THE KEY         append a random suffix: key -> key#0 .. key#9, and
                          fan out reads across the ten. Turns one hot key into
                          ten warm ones. Writes become 10x cheaper to spread,
                          reads become a 10-way scatter-gather.

 4. DEDICATED SHARD       give the big tenant their own machine. What
                          multi-tenant SaaS actually does, and why they use
                          DIRECTORY sharding rather than hashing.
```

**Fix 1 first, always.** It is the photocopy, it takes ten minutes, and for a read-heavy hot key it ends
the problem.

**Fix 3 — key salting — is the one worth naming**, because it is the only thing that helps a
**write**-heavy hot key. The cost is that every read must now check all ten suffixes.

### What real systems do

- **Redis Cluster**: 16,384 fixed hash slots. Resharding is `CLUSTER SETSLOT` — moving slots between
  nodes, live, one at a time. The slot count never changes.
- **Cassandra**: consistent hashing with virtual nodes — each machine owns many token ranges, so adding a
  machine takes a slice from many machines at once rather than one, which also spreads the streaming load.
- **Vitess**: resharding is a first-class workflow — `VReplication` streams data to the new shards, with
  built-in dual writes, verification and a controlled cutover. It is the four phases, productised.
- **DynamoDB**: splits partitions automatically when they exceed size or throughput limits, and its
  adaptive capacity moves throughput toward hot partitions — but it still cannot split a single partition
  key, so a hot key is throttled. **That constraint, priced and enforced, is the clearest statement of the
  problem anywhere.**
- **Slack, Notion, Figma** have all published multi-month shard migrations following exactly the
  dual-write, backfill, verify, cut-over shape.

---

## 6. The numbers

### The cost of plain modulo

```
 fraction of keys that move when going from N to N+1 machines
   plain modulo:        ~N/(N+1)   -> 80% at 4→5, 89% at 8→9
   logical shards:      ~1/(N+1)   -> 20% at 4→5, 11% at 8→9
   consistent hashing:  ~1/(N+1)   -> the same

 1 TB of data, 8 → 9 machines
   plain modulo:     ~890 GB moved
   logical shards:   ~111 GB moved      8× less
```

**At 100 MB/s of copy throughput per machine, 890 GB is about two and a half hours of saturated network,
and 111 GB is about twenty minutes.** And the modulo version has no safe intermediate state, because every
key's location changes at once.

### Sizing the logical shard count

```
 logical shards    max machines    per-machine shards at 8 machines
 --------------    ------------    --------------------------------
 64                64              8
 256               256             32
 1,024             1,024           128
 4,096             4,096           512

 cost per logical shard: a map entry (~tens of bytes) and, in some systems,
 a file handle or a connection. Cheap.
```

**Pick 1,024 or more.** The ceiling is on machines, and running out means the resharding project you were
trying to avoid.

### Detecting skew

```
 healthy               busiest shard ≈ 1.2× the mean
 mild skew             1.5-2×          — investigate, do not panic
 hot shard             3×+             — act
 the 60% case          with 4 shards, even is 25%: 60% is 2.4× the mean
                       and the other three are at ~13% each
```

```
 4 shards, 10,000 requests/s total
   even:      2,500 each
   observed:  6,000 / 1,300 / 1,400 / 1,300

 effective capacity: whatever ONE machine can do, ÷ 0.6
 -> if a machine handles 5,000/s, the cluster tops out at ~8,300/s
    despite having 20,000/s of hardware
```

**A hot shard caps the whole cluster at the hot shard's capacity.** That arithmetic is the reason it
matters.

### Hot key, and what caching does

```
 shard 3: 6,000 req/s, of which key `user:8823` is 3,500 req/s

 cache that one key at a 95% hit rate:
   3,500 × 0.05 = 175 req/s reach the shard
   shard 3 total: 6,000 - 3,500 + 175 = 2,675 req/s     ← back in line

 time to implement: ten minutes
 time to reshard:   a quarter
```

**That comparison is the argument for diagnosing before prescribing.**

### Key salting, for a write-heavy hot key

```
 one key at 5,000 writes/s      -> one shard, over capacity
 salted into 10 (key#0..key#9)  -> ~500 writes/s each, across up to 10 shards

 cost: every READ must query all 10 suffixes and merge
       -> a 10-way scatter-gather on the hottest key in the system
```

**Only do this when the hot key is write-heavy**, because it makes reads worse.

### The migration, in calendar time

```
 dual write         days      (code change, deploy, monitor)
 backfill           hours to weeks, depending on data size and rate limits
 verify             days to weeks   ← DO NOT SHORTEN THIS
 cut over           days      (1% → 10% → 50% → 100%, with soak time)
 -----------------------------------------------------------------
 total              4-12 weeks for a large table, and that is normal
```

**Backfill throughput is deliberately limited**, because a backfill running at full speed competes with
live traffic and can cause the outage you were trying to prevent. Rate-limiting the backfill to a fraction
of spare capacity is standard, and it is why "hours" becomes "weeks".

---

## 7. The trade-offs

### Logical shards or consistent hashing?

**Logical shards** give an explicit map, so you control exactly what lives where, can pin a big tenant to
its own machine, and can move one slice deliberately. The map is a distributed dependency that every
client must have and that can go stale.

**Consistent hashing** needs no map — the location is computed — so there is nothing to distribute or
keep in step. You give up control over placement, and you cannot easily give one key special treatment.

**Databases usually take logical shards; caches and stateless routers usually take consistent hashing.**
The dividing line is whether you need to *decide* where something lives.

### How many logical shards?

**More is safer** — a higher machine ceiling and finer rebalancing — and costs map entries and, in some
systems, per-shard overhead like connections or files. **1,024 is a good default** and 16,384 (Redis's
number) is not unreasonable.

**Too few is the mistake that cannot be undone cheaply**, because raising the count is a full resharding
project.

### Should the cutover be gradual?

**Yes, always**, and the reason is not correctness — it is that verification never catches everything. One
percent of traffic reading from the new location for a day surfaces the cases your comparison job did not
think to compare.

**I would not do a big-bang cutover** even for a small table, because the cost of the gradual version is a
week of patience and the cost of a bad big-bang is an outage with no fast way back.

### Fix the hot shard or fix the key?

**Diagnose first.** Four causes, and the fixes range from an hour to a quarter:

```
 uneven map        rebalance                    hours     ← check this first
 one hot key       cache / replicate / salt     hours to days
 skewed key        change the key               a quarter
 sequential key    change the key               a quarter
```

**I would not reshard for a hot key**, because caching that one key almost always ends it. And I would not
try to cache my way out of a badly chosen key, because the hotness will move.

### Where this breaks

- **The unbounded key.** No fix after the fact. Design composite keys so no single value can grow
  indefinitely.
- **The shard map going stale during a move.** Clients cache it, so a slow client can write to the old
  machine after a flip. Version the map, have shards reject stale writes, and keep forwarding for a grace
  period.
- **Backfill competing with live traffic.** The migration causes the incident. Rate-limit it and run it
  against a replica where possible.
- **Verification being skipped under schedule pressure.** This is where every published post-mortem of a
  failed migration points.
- **Cross-shard invariants during the move.** For the duration of a migration, some data exists in two
  places; anything that assumed a single source of truth needs an explicit answer.

---

## 8. In the interview

### How it gets asked

- The diagnostic: *"One shard is taking 60 percent of the traffic. Now what?"*
- The growth question: *"You need to add a shard. How much data moves?"*
- The procedure: *"How do you reshard without downtime?"*
- The one with no fix: *"One tenant is a hundred times bigger than the others."*
- The measurement: *"How would you know a shard is hot?"*

### What to say out loud, in the first ninety seconds

1. **Diagnose before prescribing.** "Sixty percent on one shard has four possible causes and they have
   very different fixes, so the first thing I want is per-shard *and per-key* traffic. 'Shard three is
   hot' leads to a resharding project; 'one key is forty percent of shard three' leads to a ten-minute
   cache change."
2. **Give the four causes.** "A sequential shard key; one genuinely hot key; a skewed key distribution;
   or just an uneven shard map. I would check the last one first because it is free to fix."
3. **State the capacity consequence.** "A hot shard caps the whole cluster at the hot shard's capacity —
   with four shards, 60 percent on one means the cluster tops out at about a third of the hardware you are
   paying for."
4. **Say the growth answer before being asked.** "And for adding capacity: I would never run plain `hash %
   N`, because going from eight machines to nine moves 89 percent of the data. I use a fixed number of
   logical shards — 1,024 — mapped onto machines, so the hash never changes and only the map does. Then
   adding a machine moves a ninth of the data."
5. **Name the four migration phases.** "Dual write, backfill, verify, cut over gradually — and everything
   is reversible until the last step."
6. **Name the one with no fix.** "The case I would design against up front is a single key that grows
   without limit, because a shard key value cannot be split. That needs a composite key from day one."

### The follow-ups

**"One shard is taking 60 percent of the traffic. Now what?"**
"I would not fix anything until I know which of four things it is, because the fixes range from an hour to
a quarter. **An uneven shard map** — that shard simply owns more logical shards than the others. Free to
fix, so I check it first. **One hot key** — a celebrity, a viral item, a huge tenant. **A skewed key
distribution** — many keys all landing on one shard because the key itself is uneven, like country or
status. Or **a sequential key**, where the newest shard is hot and the hotness migrates over time. The
evidence that separates them is **per-key traffic within the shard**, which most teams do not have and
should. If one key is most of that shard's traffic, I cache it and the problem is over in ten minutes. If
it is spread across thousands of keys, the key itself is wrong and I am looking at a resharding project.
And the number worth stating: with four shards, 60 percent on one means the cluster's ceiling is that one
machine's capacity divided by 0.6 — so about a third of the hardware I am paying for."

**"You need to add a shard. How much data moves?"**
"With plain `hash % N`, almost all of it — going from eight machines to nine leaves only about one key in
nine where it was, so 89 percent of the data moves, and there is no safe intermediate state because every
key's location changes at the same instant. That is why nobody runs plain modulo. Instead I fix a large
number of **logical shards** at the start — 1,024, say — and hash keys into those. The hash never changes.
What changes is a small map from logical shard to machine. Adding a ninth machine means moving about 114
logical shards, which is a ninth of the data, and the routing rule is untouched. The two things to get
right are that the logical shard count is a permanent ceiling on machine count, so pick generously, and it
should be a power of two so a shard can be split later if you ever must."

**"How do you reshard without downtime?"**
"Four phases, and the order is what makes it safe. **Dual write**: start writing to both the old and new
locations while reads still come from the old — nothing is exposed and it is fully reversible. **Backfill**:
copy the historical data in rate-limited batches, while dual writes keep the tail current; rate-limited
because a backfill at full speed competes with live traffic and causes the incident you were avoiding.
**Verify**: read from both, compare, log every mismatch, and do not shorten this phase — it is where the
bugs are, and every published failed migration skipped it. **Cut over**: move reads gradually, one percent
then ten then fifty, keeping dual writes running so you can switch back instantly. Only after a soak do
you stop dual-writing, and only then delete the old data. The subtlety in phase two is that the backfill
races the dual writes, so the copy must be idempotent and last-write-wins by timestamp, or you only
backfill rows older than the moment dual writes started. For one logical shard the whole thing is faster:
copy, catch up, pause writes for a few milliseconds, flip the map entry, resume."

**"One tenant is a hundred times bigger than the others."**
"That is the case with no clean after-the-fact fix, and I would say so directly. You cannot split a single
shard key value — every row with that value lives on one machine by definition — so no amount of
rebalancing helps. What you can do: give that tenant a **dedicated shard**, which is exactly why
multi-tenant systems use **directory** sharding rather than hashing, since a lookup table lets you place
one customer anywhere. Cache their hot reads. And if the problem is write volume rather than size,
**salt** the key — append a random suffix so one key becomes ten — at the cost of every read becoming a
ten-way fan-out. But the real answer is at design time: make the key **composite**, so no single value can
grow without bound. Shard by `(tenant_id, month)` or `(conversation_id, message_id / 10000)`, and then one
enormous tenant is spread across many shards while a query for recent data still touches one or two
buckets."

**"How would you know a shard is hot?"**
"Per-shard metrics, and critically **per-key** metrics within each shard. The per-shard set is requests
per second, CPU, storage, and p99 latency — and I would alert on the ratio of the busiest shard to the
mean rather than on absolute numbers, because that is what actually indicates skew: 1.2× is healthy, 2× is
worth investigating, 3× needs action. But per-shard alone only tells me *that* something is wrong; it
leads to moving the shard, which usually just moves the queue. The measurement that decides the fix is
**top keys by traffic within the shard**, because 'key `user:8823` is 40 percent of this shard' turns a
quarter-long project into a ten-minute cache change. Most teams discover they do not have that metric at
exactly the moment they need it."

**"Logical shards or consistent hashing?"**
"They solve the same problem — adding a machine should move `1/N` of the data, not all of it — and they
differ in whether you get to *decide* placement. **Logical shards** keep an explicit map, so I can pin a
large tenant to its own machine, move one slice deliberately, and reason about exactly what lives where.
The cost is that the map is a distributed dependency: every client caches it, so I need a version number
and a grace period where the old shard forwards, or a stale client writes to the wrong machine during a
move. **Consistent hashing** computes the location, so there is no map to distribute or keep in step, and
adding a node steals a slice from its neighbours automatically. The cost is that I lose control of
placement and cannot easily special-case one key. In practice databases take logical shards and caches
take consistent hashing, and the dividing line is whether placement is a decision or a computation."

### A model answer

Asked: *one shard is taking 60 percent of the traffic. Now what?*

> "Before fixing anything I want to know **which** of four things it is, because the fixes range from an
> hour to a quarter and prescribing before diagnosing is how people spend a quarter solving the wrong
> problem.
>
> **One: the shard map is simply uneven** — that machine owns more logical shards than the others. Free to
> fix, so I check it first. **Two: one hot key** — a celebrity, a viral item, one enormous tenant. **Three:
> the key distribution is skewed** — many different keys all landing on the same shard, which happens when
> you shard by country, or status, or surname. **Four: the key is sequential**, so the newest shard is hot
> and the hotness migrates over time.
>
> The evidence that separates them is **per-key traffic inside the shard**, and that is the metric most
> teams find they do not have at the moment they need it. 'Shard three is hot' leads you to move shard
> three, and the queue moves with it. 'Key `user:8823` is forty percent of shard three's traffic' leads you
> to cache one key, which takes ten minutes and ends the problem — because a read-heavy hot key never
> reaches the shard once it is cached.
>
> The arithmetic worth stating: with four shards, even would be 25 percent each. Sixty percent on one
> means that machine is at 2.4 times the mean, and **the cluster's ceiling is now that one machine's
> capacity divided by 0.6** — so if a machine does 5,000 requests a second, the cluster tops out around
> 8,300 despite having 20,000 of hardware. A hot shard caps everything.
>
> So my order would be: check the map, then look at per-key traffic. If it is one key: cache it, or
> replicate it to every shard if it is small and rarely changes, or — if it is *write*-heavy, where caching
> does not help — **salt** it, appending a random suffix so one key becomes ten, accepting that every read
> becomes a ten-way fan-out. If it is a big tenant, give them a dedicated shard, which is why multi-tenant
> systems use directory sharding rather than hashing.
>
> If it is the key itself that is wrong, then it is a resharding project, and I would do it in four
> phases: **dual write** to both locations while reads stay on the old, **backfill** the history in
> rate-limited batches, **verify** by reading both and comparing — which is the phase people shorten and
> should not — and then **cut over** gradually, one percent at a time, keeping dual writes running so
> reverting is instant. Everything is reversible until the last step, and that is the entire point of the
> ordering.
>
> And the case I would flag as having no fix after the fact: **a single key that grows without limit.** You
> cannot split a shard key value — every row with it is on one machine by definition. The answer is at
> design time: make the key composite, so no single value can grow unboundedly."

---

## 9. Recall card

- **Never run plain `hash % N`: going from 8 machines to 9 moves ~89% of the data.** Fix with an
  **indirection** — a large fixed number of **logical shards** (1,024, a power of two) hashed once and
  never changed, plus a small **map** from logical shard to machine. Then adding a machine moves **1/(N+1)**
  of the data and the routing rule is untouched. **The logical shard count is a permanent ceiling on
  machine count** — Redis Cluster's is 16,384.
- **Resharding live is four phases and the order is the safety: DUAL WRITE → BACKFILL → VERIFY → CUT OVER
  gradually.** Everything is reversible until the last two. **Rate-limit the backfill** (it competes with
  live traffic) and **do not shorten verification** — that is where every failed migration went wrong. A
  single logical shard moves with a **millisecond** write pause.
- **A hot spot has FOUR causes and you must diagnose before prescribing: uneven map (free) · one hot key
  (hours) · skewed key distribution (a quarter) · sequential key (a quarter).** The metric that decides it
  is **top keys *within* the shard**, not just per-shard traffic.
- **A hot shard caps the whole cluster**: 60% on one of four shards means the ceiling is that machine's
  capacity ÷ 0.6 — about a third of the hardware you are paying for. **Caching one hot key** at a 95% hit
  rate can take a shard from 6,000 to 2,675 req/s in ten minutes. For a **write**-heavy hot key, **salt**
  it (`key#0..key#9`) and pay a 10-way fan-out on reads.
- **The unbounded key has no after-the-fact fix** — a shard key value is atomic, so every row with it is
  on one machine. **Design a composite key** (`(tenant_id, month)`, `(conversation_id, message_id/10000)`)
  so no single value can grow without limit. And version the shard map, with the old shard **forwarding**
  during a grace period, or a stale client writes to the wrong machine mid-move.
