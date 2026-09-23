---
day: 106
track: system-design
title: "Sharding, part one: choosing the key"
phase: "Scaling fundamentals"
status: written
---

# Day 106 · System Design — Sharding, part one: choosing the key

**After today you can:** You can pick a shard key and predict which queries it will make expensive.

**The interviewer asks it as:** *How would you shard this table? What breaks after you do?*

---

## 1. What this is, and why they ask it

**Sharding** means splitting one logical table across several machines, so that each machine holds a
subset of the rows and takes the reads and writes for that subset.

Three sentences. It is the only technique that scales **writes**, which is why it exists —
[replication](../day-104-tree-path-problems/README.md) copies every write to every machine and
[read replicas](../day-105-lowest-common-ancestor/README.md) hit a hard ceiling because of that. The
whole design reduces to one decision, the **shard key**, and that decision is very expensive to change
later. And the reason it is expensive is that sharding takes things away permanently: **no joins across
shards, no transactions across shards, and no globally unique constraint except on the key itself.**

They ask it because the answer separates people who have read that sharding scales writes from people who
know what it costs. The good answer names a key, says which query it makes fast, says which query it
makes terrible, and says what the design does about that second query. *"What breaks after you do?"* is
the question — the first half is setup.

---

## 2. The story

The sub-registrar's office had one records room and it had run out of floor.

Eighty-odd years of documents in one long room with racks up to the ceiling, and it had reached the point
where two people looking for two different things could not get past each other in the aisle.

They were given three more rooms down the corridor, and the question of how to divide the documents took
a committee three meetings.

The first proposal was by surname. A to F in room one, G to L in room two, and so on. It was easy to
explain and everybody could remember it, and it was tried for about five months.

It did not work, and the reason was obvious in hindsight to everybody except the person who had proposed
it. The room with the S names had nearly half the documents. There were four rooms and one of them had a
permanent queue outside it while another was used twice a day. Splitting the alphabet evenly does not
split the *people* evenly, because names are not spread evenly.

The second proposal came from the youngest clerk and was resisted because it sounded stupid. He said: take
the document number, divide it by four, and use the remainder. Nought goes in room one, one in room two,
two in room three, three in room four.

Nobody could see the sense of it, because it put documents from the same street, the same family and the
same week in four different rooms. But it split the work perfectly evenly, and after two weeks nobody was
queuing anywhere.

What it cost showed up in the third month.

A lawyer came in wanting every transaction on one particular survey number over twenty years. Under the
old system, or even under the surname system, that had been one visit to one place. Now it meant walking
to four rooms, asking four people, and combining four answers, and if one of those rooms was locked
because the man had gone for lunch, you had nothing.

And the second thing, which was worse and took a year to surface. Documents had always been numbered in
one sequence, and each room now issued its own numbers. Two rooms issued the same number in the same
week, to two different documents, and nobody noticed until the two turned up in the same court case.

The head clerk's rule afterwards, which was written on a board and stayed there, was two lines.

**Decide what you are splitting by before you split, because moving it afterwards means moving
everything.**

**And write down, in advance, which questions will now need all four rooms — because those are the ones
that will be asked.**

---

## 3. The idea in plain English

The records office has been sharded, and it hit every consequence in the right order: the hotspot, the
cross-shard query, and the identifier collision.

- Each room is a **shard** — a machine holding a subset of the rows.
- The rule for deciding which room a document goes in is the **shard key** and the **sharding strategy**.
- The S room with half the documents is a **hotspot**.
- The lawyer's twenty-year search is a **cross-shard query**, also called a **scatter-gather**.
- Two rooms issuing the same number is the **unique identifier** problem.

### What sharding is, and what it is not

```
 REPLICATION    every machine holds ALL the data
                scales READS, not writes; every replica applies every write

 SHARDING       every machine holds SOME of the data
                scales WRITES and STORAGE; each shard sees only its own traffic
```

**They are orthogonal and real systems use both**: shard the data across `N` groups, and replicate each
shard within its group. Say that early — a candidate who treats them as alternatives has misunderstood
both.

### The four strategies

**Range sharding.** Rows go to a shard by where the key falls in an ordered range.

```
 user_id  1 -    1,000,000   -> shard 1
          1,000,001 - 2,000,000 -> shard 2
```

```
 + range queries stay on one shard: "users 500 to 900" is one machine
 + easy to split a shard: cut a range in two
 - HOTSPOTS, and they are almost guaranteed with any sequential key
```

**Every new user has the highest id, so every new user goes to the last shard.** With a timestamp key it
is worse: 100 percent of writes go to one shard while the others are idle. This is the single most common
sharding mistake, and it has a name — **the append hotspot**.

**Hash sharding.** Apply a hash function to the key and take the remainder.

```
 shard = hash(user_id) % 4
```

```
 + even distribution, essentially for free
 + no hotspot from sequential keys, because the hash destroys the ordering
 - range queries are DEAD: adjacent keys land on different shards
 - adding a shard moves almost everything — unless you use consistent hashing
```

The youngest clerk's proposal. **Even distribution and no locality**, and those are the same property
seen from two sides.

**Directory sharding.** Keep an explicit lookup table: this key lives on that shard.

```
 + total flexibility; move a single tenant without moving anything else
 + you can give a big customer their own shard
 - the directory is a lookup on every request, and a single point of failure
```

**This is what multi-tenant systems actually do**, because customers are wildly different sizes and you
need to be able to move one.

**Geographic sharding.** By region — European users in Europe, Indian users in India.

```
 + low latency for local users; often a legal requirement (data residency)
 - a user who travels is far from their data
 - regions are not equal sizes
```

### Choosing the key: four requirements

**One — it must appear in almost every query.** If the key is `user_id` and a query filters by `email`,
that query has no idea which shard to ask, so it asks all of them. **The key must match your dominant
access pattern**, and knowing that pattern is a prerequisite you should ask about out loud.

**Two — high cardinality.** The number of distinct values bounds the number of shards you can ever have.
Sharding by `country` gives you about 200 buckets — and one of them is enormous. Sharding by `gender`
gives you two. **The key must have far more distinct values than you will ever have shards.**

**Three — even distribution.** Not just many values: **evenly used** values. Surnames have high
cardinality and a very skewed distribution — that was room three's problem.

**Four — stability.** The key must not change. Changing a row's shard key means deleting it from one
shard and inserting it into another, which is a distributed transaction, which is the thing you gave up.
**Shard by `user_id`, never by `email` or `city`.**

### What breaks — the second half of the question

**Cross-shard joins.** `SELECT ... FROM orders JOIN users ON ...` where the two tables are sharded
differently. The database cannot do it. Your options are to denormalise (copy the user's name onto the
order), to query both and join in the application, or to shard both tables by the same key so related
rows land together — which is **co-location**, and it is the good answer.

**Cross-shard transactions.** "Move money from A to B" is trivial on one machine and requires two-phase
commit or a saga across two — [days 120 and 121](../day-120-the-trie/README.md). Most systems avoid the
problem by choosing a key that keeps the things that change together on one shard.

**Unique constraints.** A shard can only enforce uniqueness within itself. **A globally unique email
address cannot be enforced by the shards** — you need a separate service, or a second table sharded by
email whose job is to own that uniqueness.

**Auto-increment ids.** Two rooms issuing the same number. The fixes: UUIDs (large and unordered), a
central allocator (a bottleneck), per-shard ranges (shard 1 gets 1–1M), or **Snowflake ids** — a
timestamp, a machine id and a counter packed into 64 bits, which are unique, roughly ordered, and need no
coordination. **Snowflake is the standard answer** and worth naming.

**Aggregations.** `COUNT(*)`, `SUM`, `ORDER BY ... LIMIT 10` across all shards must query every shard and
combine. A top-10 needs the top 10 from each shard, merged — which is
[merging k sorted lists](../day-117-merge-k-sorted/README.md).

**Rebalancing.** Adding a shard with plain `hash % N` remaps almost every key. That is
[day 107](../day-107-bst-operations/README.md) and [day 108](../day-108-validating-a-bst/README.md).

### The question that chooses the key

> **What is the single most common query, and what does it filter by?**

For a social product it is *"give me this user's timeline"* → shard by `user_id`. For a chat app it is
*"give me this conversation's messages"* → shard by `conversation_id`. For a multi-tenant SaaS it is
*"everything for this customer"* → shard by `tenant_id`, and that one is the cleanest of all, because
tenants never share data.

**Then write down the queries the key makes expensive, before you shard**, because those are exactly the
ones somebody will ask for in month three.

---

## 4. The picture

Replication and sharding, which do different things.

```
 REPLICATION (day 104)                  SHARDING (today)

    ┌──────────┐                        ┌──────────┐  ┌──────────┐
    │ LEADER   │  all the data          │ Shard 1  │  │ Shard 2  │
    │ A B C D  │                        │ A B      │  │ C D      │
    └────┬─────┘                        └──────────┘  └──────────┘
         │ every write                   users 1-1M    users 1M-2M
    ┌────┴─────┐  ┌──────────┐
    │ Replica  │  │ Replica  │          each shard sees only ITS
    │ A B C D  │  │ A B C D  │          writes -> writes SCALE
    └──────────┘  └──────────┘
    all the data, again

 scales READS                            scales WRITES and STORAGE
 every machine does every write          each machine does 1/N of the writes

 REAL SYSTEMS DO BOTH: shard into N groups, replicate within each group.
```

The strategies, on the same data:

```
 users 1..1,000,000, four shards

 RANGE                                  HASH
 shard 1: ids       1 -   250,000       shard 1: hash(id) % 4 == 0
 shard 2: ids 250,001 -   500,000       shard 2: hash(id) % 4 == 1
 shard 3: ids 500,001 -   750,000       shard 3: hash(id) % 4 == 2
 shard 4: ids 750,001 - 1,000,000       shard 4: hash(id) % 4 == 3

 "users 1000 to 2000"                   "users 1000 to 2000"
   -> ONE shard                           -> ALL FOUR shards, and 1,000
                                             separate lookups

 new signups (id 1,000,001+)            new signups
   -> ALL go to shard 4                   -> spread evenly
   -> 100% of writes on 25% of                across all four
      the hardware  ← THE APPEND HOTSPOT
```

The hotspot, drawn as load:

```
 RANGE-SHARDED BY TIMESTAMP OR SEQUENTIAL ID

 writes/s
   │
   │                                        ████  shard 4
   │                                        ████
   │                                        ████
   │  ▒                ▒            ▒       ████
   └──────────────────────────────────────────────
      shard 1        shard 2      shard 3   shard 4

 25% of the hardware is doing 100% of the writes.
 The other three machines are paid for and idle.

 HASH-SHARDED
 writes/s
   │  ███       ███        ███        ███
   │  ███       ███        ███        ███
   └──────────────────────────────────────────────
      shard 1  shard 2   shard 3   shard 4        even, and no range queries
```

The scatter-gather, which is the cost of hashing:

```
 QUERY ON THE SHARD KEY                 QUERY ON ANYTHING ELSE
 "orders for user 4821"                 "orders placed yesterday"

     app                                    app
      │                                   ╱ │ │ ╲
      │ hash(4821) -> shard 3            ╱  │ │  ╲
      ▼                                 ▼   ▼ ▼   ▼
   [shard 3]                          [s1][s2][s3][s4]
                                        ╲  │ │  ╱
   1 network call                        ╲ │ │ ╱     4 calls, wait for ALL
   latency = 1 query                       app       latency = the SLOWEST one
                                                     any shard down = query fails
```

**That last line is the part people miss**: a scatter-gather's latency is the maximum of its parts, not
the average, and its availability is the product of all of them. Four shards at 99.9 percent each give a
scatter-gather query 99.6 percent availability.

---

## 5. How it actually works

### Where the routing decision lives

```
 IN THE APPLICATION      the code computes the shard and picks a connection
                         simple, and every service must implement it identically

 IN A PROXY              Vitess, Citus, ProxySQL: the app sees one database
                         and the proxy routes, and can even fan out and merge
                         -> the usual answer at scale

 IN THE DATABASE         MongoDB, Cassandra, DynamoDB, CockroachDB shard natively
                         -> the routing is invisible; the CONSTRAINTS are not
```

**Even when the database shards for you, the constraints remain**: MongoDB still cannot join across
shards efficiently, and DynamoDB still makes you choose a partition key that decides everything.

### A worked choice: an e-commerce order table

```
 candidate keys           what it makes fast              what it kills
 --------------------     ---------------------------     ----------------------------
 order_id (hash)          "fetch order 8412"              "my orders"  -> all shards
 user_id (hash)           "my orders"  -> ONE shard       "orders today" -> all shards
 created_at (range)       "orders today" -> one shard     APPEND HOTSPOT: every new
                                                           order hits the same shard
 seller_id (hash)         "seller's orders" -> one shard  buyer queries -> all shards
```

**`user_id` wins**, and the reasoning is the answer: the dominant query is *"show me my orders"*, users
are numerous and roughly evenly active, and a user's id never changes. Then write down what it costs:
*"orders placed today across all users"* becomes a scatter-gather, so analytics goes to a separate
system fed by a change stream rather than querying the shards.

**And co-locate.** Shard `order_items` by the same `user_id`, not by `order_id`, so an order and its items
are on one machine and the join stays local. That single decision removes most cross-shard joins from the
system.

### The composite-key trick for hotspots

If you must range-shard on something sequential, prefix the key with something that spreads:

```
 bad:   shard by  timestamp
        -> every write goes to the newest shard

 good:  shard by  (user_id, timestamp)
        -> writes spread across users; one user's history is still contiguous
           and range-queryable within its shard
```

**This is exactly what Cassandra's partition key plus clustering key does**, and it is the standard fix
for the append hotspot: **partition by something that spreads, order by something that is sequential.**

### Handling the queries the key makes slow

Three answers, and a good candidate names all three:

**A global secondary index** — a second table sharded by the other field, mapping it back to the primary
key. Costs a second write on every insert, and it is eventually consistent unless you pay for a
distributed transaction.

**Denormalise** — store the data twice, sharded two ways. Same trade: writes cost more, reads get
cheaper.

**A separate system** — push changes to a search index (Elasticsearch) or an analytics warehouse via a
change stream. **This is what real systems do for "orders today across all users"**, because those
queries are analytical and do not belong on the serving path at all.

### What real systems do

- **Vitess** shards MySQL and runs YouTube; it puts the routing in a proxy layer and supports resharding
  without downtime.
- **Citus** does the same for PostgreSQL, with an explicit distribution column and co-location groups.
- **MongoDB** requires a shard key at collection creation and — famously — historically could not change
  it, which taught a generation of teams that the decision is close to permanent.
- **DynamoDB** makes it unavoidable: you choose a **partition key** and a **sort key**, and every access
  pattern must be designed around them up front. Its per-partition throughput limit means a hot partition
  key is throttled even when the table has capacity — the hotspot problem, priced.
- **Cassandra** is the same model with the composite key trick built into its data model.
- **Instagram** sharded PostgreSQL by user id early, and published their scheme: ids embed the shard, so
  any id tells you where its row lives. That is a genuinely good trick worth mentioning.

---

## 6. The numbers

### When you actually need it

```
 one machine sustains          ~5,000 writes/second (relational, indexed)
 one machine holds             a few TB comfortably

 you need sharding when EITHER:
   write rate > ~5,000/s and vertical scaling is exhausted
   data size  > the largest machine's disk or working set
```

```
 10,000 writes/s, 4 shards   ->  2,500 writes/s each   comfortable
 10,000 writes/s, 1 machine  ->  impossible
```

**And not before.** The cost of sharding is permanent; the cost of one more vertical step is a restart.

### Hotspot arithmetic

```
 range-sharded by timestamp, 4 shards, 10,000 writes/s

 shard 4 (the newest range):  10,000 writes/s   -> over capacity, failing
 shards 1-3:                       0 writes/s   -> paid for, idle

 effective capacity: 5,000 writes/s from 4 machines
 -> you have quadrupled the cost and gained NOTHING
```

**That is the number that makes the append hotspot real.** Hash sharding on the same hardware gives 2,500
per shard and works.

### Skew, measured

```
 sharding a social product by user_id, hashed

 the average user       ~100 followers, ~5 posts/day
 the top 0.01% user     ~50,000,000 followers, and their writes fan out

 -> the SHARD holding a celebrity does not have more rows, it has more TRAFFIC
 -> observed skew in real systems: 5-20x between the busiest and quietest shard
```

**Even a perfect hash does not fix skew in *activity*.** The fix is not a better hash — it is
special-casing the outliers, which for a social product means handling celebrity accounts differently.

### Scatter-gather cost

```
 a query on the shard key           1 network call, ~1 ms
 a scatter-gather over 16 shards    16 calls in parallel
                                    latency = the SLOWEST of 16

 if each shard's p99 is 10 ms:
   P(at least one is slow) = 1 - 0.99^16 = 15%
   -> the query's p50 is now close to the shards' p99
```

**Fanning out turns your p99 into your p50.** That is the tail-latency amplification argument and it is
worth stating precisely.

Availability too:

```
 16 shards, each 99.9% available
 a query needing ALL of them:  0.999^16 = 98.4%
 -> from 8.8 hours of downtime a year to 140 hours
```

### Storage and capacity per shard

```
 1 billion rows × 1 KB          = 1 TB
 16 shards                      = 62.5 GB each     comfortable
 4 shards                       = 250 GB each      fine
 1 machine                      = 1 TB             possible, but the working set
                                                   will not fit in memory
```

### The cost of getting the key wrong

```
 changing the shard key = rewriting every row into a new arrangement

 1 TB, 16 shards, moving everything
   at 100 MB/s per shard, in parallel     ~10 GB per shard ÷ 100 MB/s ≈ 100 s of pure copy
   in practice, with dual writes,
   verification and a cutover             WEEKS of engineering, months of calendar
```

**"Weeks of engineering" is the honest number**, and it is why the decision deserves the meeting.

---

## 7. The trade-offs

### Range or hash?

**Range** keeps related keys together, so range queries are local and splitting a shard is easy. It
almost guarantees a hotspot on any sequential key, and sequential keys are the normal case.

**Hash** distributes perfectly and destroys locality — those are the same property. Range queries become
scatter-gathers, and adding a shard remaps everything unless you use consistent hashing.

**Take hash by default; take range when range queries dominate and the key is not sequential.** And when
you need both, use the composite trick: **partition by something that spreads, order by something
sequential.**

### Sharding costs you three things permanently

**Joins.** Only within a shard. Fixed by co-locating related tables on the same key, or by denormalising.

**Transactions.** Only within a shard. Fixed by choosing a key that keeps things that change together
together — which is the real reason `tenant_id` is such a good key.

**Unique constraints.** Only on the shard key. A globally unique email needs a separate owner.

**Say all three when asked what breaks.** They are the answer.

### Fewer big shards or more small ones?

**Fewer** means less scatter-gather fan-out and less operational surface. **More** means finer
rebalancing and smaller blast radius when one fails.

The usual answer is **more logical shards than physical machines** — say, 1,024 logical shards mapped
onto 8 machines. Then adding a machine moves logical shards rather than rehashing keys, and you never
re-shard again. **That indirection is worth mentioning; it is what makes rebalancing tractable**, and it
is [tomorrow's](../day-107-bst-operations/README.md) subject.

### When not to shard

**I would not shard if** vertical scaling has room, if the read load is the problem (that is caching and
replicas), or if the data is under a terabyte and the write rate is under a few thousand a second.

**And I would not shard a table that is small but joined against everything.** Reference tables —
countries, currencies, product categories — should be replicated to every shard, not split.

### Where this breaks

- **The unbounded partition.** One tenant, one celebrity, one popular conversation grows without limit and
  its shard cannot be split, because a shard key value cannot be divided. **This is the failure that has
  no clean fix** — you must design the key so that no single value can grow indefinitely, which usually
  means a composite key with a bucket.
- **Cross-shard analytics** are permanently awkward. Send changes to a warehouse and stop trying.
- **Schema changes** now happen `N` times, and a partially-applied migration leaves shards disagreeing.
- **The routing layer** becomes a critical dependency with its own availability.

---

## 8. In the interview

### How it gets asked

- The pair: *"How would you shard this table? What breaks after you do?"*
- The choice: *"Range or hash? Why?"*
- The trap: *"You've sharded by timestamp. What happens?"*
- The consequence: *"How do you get a globally unique order id now?"*
- The limit: *"When would you not shard?"*

### What to say out loud, in the first ninety seconds

1. **Separate it from replication.** "Replication copies all the data everywhere and scales reads.
   Sharding splits the data and scales writes and storage. They are orthogonal — I would shard into `N`
   groups and replicate within each group."
2. **Ask the question that chooses the key.** "What is the dominant query, and what does it filter by?
   The shard key has to be the thing almost every query already knows."
3. **Name the key and give all four reasons.** "`user_id`, hashed: it is in the dominant query, it has
   high cardinality, users are roughly evenly active, and a user's id never changes — which matters,
   because changing a row's shard key means moving it between machines."
4. **Say hash and say why not range.** "Hash, because a range on any sequential key gives an append
   hotspot — every new row goes to the newest shard, so a quarter of the hardware does all the writes."
5. **Answer the second half before it is asked.** "What breaks: no joins across shards, no transactions
   across shards, and no unique constraint except on the key. Plus auto-increment ids, which now collide
   between shards."
6. **Name the query you have made expensive.** "'All orders placed today' now needs every shard, so I
   would not serve it from here at all — that goes to a warehouse fed by a change stream."

### The follow-ups

**"You've sharded by timestamp. What happens?"**
"An **append hotspot**, and it is the worst outcome available because it costs money and delivers nothing.
Every new row has the newest timestamp, so every write goes to the shard holding the newest range. With
four shards and ten thousand writes a second, one machine is receiving all ten thousand and failing while
the other three are paid for and idle — so I have quadrupled the cost and my effective capacity is still
one machine's. Reads are just as bad, because recent data is the most-read data, so the hot shard is hot
in both directions. The fix, if I genuinely need time-ordered locality, is the composite key: **partition
by something that spreads, and order by time within the partition.** `(user_id, timestamp)` spreads the
writes across users while keeping one user's history contiguous and range-queryable. That is exactly
Cassandra's partition-key-plus-clustering-key model."

**"What breaks after you shard?"**
"Four things, and three of them are permanent. **Joins** only work within a shard, so I would co-locate
related tables on the same key — `order_items` sharded by `user_id` rather than `order_id`, so an order
and its items live together — and denormalise where I cannot. **Transactions** only work within a shard,
so 'move money from A to B' becomes two-phase commit or a saga, and the better answer is to choose a key
that keeps the things that change together on one machine. **Unique constraints** only work on the shard
key, so a globally unique email needs a separate table sharded by email whose job is to own that
uniqueness. And **auto-increment ids** collide, because each shard has its own counter — the standard fix
is Snowflake-style ids: a timestamp, a machine identifier and a counter packed into 64 bits, which are
unique and roughly ordered and need no coordination."

**"Range or hash?"**
"**Hash by default.** It distributes evenly for free, and evenness is the thing you are actually buying —
a shard scheme that is uneven has cost you money and given you nothing. The price is that it destroys
locality, so range queries become scatter-gathers, and adding a shard remaps almost every key unless I
use consistent hashing. **Range** is right when range queries dominate *and* the key is not sequential —
sharding by something like a geographic region or a product category, where the ranges are stable and the
new data does not all land at one end. The honest summary is that hash gives you distribution and takes
away locality, and those are the same property viewed from either side."

**"How expensive is a query that does not use the shard key?"**
"It becomes a **scatter-gather**: ask every shard, wait for all of them, merge. Two costs that people
usually only count one of. **Latency** — the query takes as long as the *slowest* shard, not the average.
If each shard has a p99 of 10 ms and I fan out to sixteen, there is about a fifteen percent chance at
least one is slow, so my query's median is now close to the shards' p99. That is tail-latency
amplification. And **availability** — the query needs all sixteen to answer, so at 99.9 percent each,
the query is 98.4 percent available, which is 140 hours of failure a year instead of nine. So I would not
serve such queries from the shards at all: either a **global secondary index** sharded by the other field,
or push changes into a search index or a warehouse and query there."

**"When would you not shard?"**
"Whenever something cheaper still has room, and usually something does. If the **reads** are the problem,
that is caching and read replicas, and a ninety percent cache hit rate removes ten times more load than
sharding would. If **one machine still has headroom**, scale up — up to about 32 to 64 vCPU the price per
unit of power is flat, and it is one command and a restart. Sharding is for when the **write rate**
exceeds what one machine can do, around five thousand writes a second for a relational database, or the
**data no longer fits** the largest machine. The reason to be strict about this is that sharding's cost is
not the migration — it is permanent: every feature built afterwards has to live within the shard key I
chose today, and changing that key later is weeks of engineering with dual writes and a cutover. I would
also not shard reference tables — countries, currencies, categories. Those get replicated to every shard,
not split."

**"How do you pick the key concretely?"**
"I ask what the single most common query is and what it filters by, because the key has to be something
almost every query already knows. Then I check four things. **Is it in the dominant query** — otherwise
every request is a fan-out. **Cardinality** — the number of distinct values bounds how many shards I can
ever have, so `country` gives me 200 buckets with one enormous one, and `gender` gives me two. **Even
distribution** — not just many values, but evenly used ones; surnames have high cardinality and terrible
skew. And **stability** — the value must never change, because changing it means deleting from one shard
and inserting into another, which is precisely the distributed transaction I gave up. For most consumer
products that lands on `user_id`; for chat it is `conversation_id`; and for multi-tenant SaaS it is
`tenant_id`, which is the cleanest of all because tenants never share rows."

### A model answer

Asked: *how would you shard this table, and what breaks after you do?*

> "First, what sharding is *for*, because it is often confused with replication. Replication puts all the
> data on every machine and scales **reads** — and it has a hard ceiling, because every replica applies
> every write. Sharding splits the data so each machine holds a subset, which is the only thing that
> scales **writes** and **storage**. They are orthogonal, and a real deployment does both: shard into `N`
> groups, and replicate within each group.
>
> Before choosing a key I would ask one question: **what is the dominant query, and what does it filter
> by?** The shard key has to be something almost every request already knows, because a query that does
> not include it has to ask every shard.
>
> For an orders table I would take **`user_id`, hashed**, and I would give four reasons. It is in the
> dominant query — 'show me my orders'. It has high cardinality, so it does not limit how many shards I
> can have. Users are roughly evenly active, so the distribution is reasonable. And a user's id never
> changes, which matters more than it sounds: changing a row's shard key means deleting it from one
> machine and inserting it on another, which is a distributed transaction — the exact thing sharding takes
> away.
>
> **Hash rather than range**, because a range on anything sequential produces an **append hotspot**: every
> new row has the newest key, so every write lands on the newest shard. With four shards and ten thousand
> writes a second, one machine takes all ten thousand and fails while three sit idle — I would have
> quadrupled the cost for no capacity at all. If I needed time locality I would use a composite key:
> partition by something that spreads, order by time inside it.
>
> I would also **co-locate**: shard `order_items` by `user_id` too, not by `order_id`, so an order and its
> items live on the same machine and that join stays local. That single choice removes most of the
> cross-shard joins from the system before they exist.
>
> Now what breaks, which is the more important half. **Joins** work only within a shard. **Transactions**
> work only within a shard, so anything spanning two users needs two-phase commit or a saga. **Unique
> constraints** work only on the shard key, so a globally unique email needs its own table sharded by
> email to own that uniqueness. And **auto-increment ids** collide, because every shard has its own
> counter — I would use Snowflake-style ids, a timestamp plus a machine id plus a counter in 64 bits,
> which are unique and roughly sorted and need no coordination.
>
> And I would name the query I have just made expensive: **'all orders placed today, across all users'**
> now touches every shard. A scatter-gather costs the *slowest* shard's latency, not the average, and its
> availability is the product of all of them — sixteen shards at 99.9 percent gives that query 98.4
> percent. So I would not serve it from here: analytics goes to a warehouse fed by a change stream, and if
> I need a user-facing lookup by a non-key field, that is a global secondary index sharded by that field.
>
> Finally, the thing I would say before any of this: **I would not shard unless I had to.** If reads are
> the problem, that is caching and replicas. If one machine still has headroom, scale up — it is one
> command. Sharding is for a write rate past what one machine can take, or data past what one machine can
> hold, and its cost is not the migration, it is that every feature afterwards lives inside the key I
> chose today."

---

## 9. Recall card

- **Replication copies all the data everywhere and scales READS; sharding splits the data and scales
  WRITES and STORAGE. They are orthogonal — real systems shard into N groups and replicate within each.**
- **The question that chooses the key: what is the dominant query, and what does it filter by?** Then four
  requirements: **in the dominant query · high cardinality · evenly distributed · never changes.** That is
  usually `user_id`, `conversation_id`, or — cleanest of all — `tenant_id`.
- **Hash by default; range only when range queries dominate AND the key is not sequential.** Range on
  anything sequential gives an **append hotspot**: at 10,000 writes/s over 4 shards, **one machine takes
  all 10,000 and three sit idle** — quadruple the cost, no capacity. The fix is a **composite key:
  partition by something that spreads, order by time within it.**
- **What breaks, permanently: no cross-shard joins · no cross-shard transactions · no unique constraint
  except on the key.** Plus **auto-increment ids collide** — use **Snowflake ids** (timestamp + machine +
  counter in 64 bits). **Co-locate related tables on the same key**, and replicate small reference tables
  to every shard instead of splitting them.
- **A query without the shard key is a scatter-gather, and it costs twice: latency is the SLOWEST shard**
  (16 shards with a 10 ms p99 → ~15% chance one is slow, so your p50 becomes their p99) **and availability
  is the product** (16 × 99.9% = **98.4%**, i.e. 140 hours a year). **Do not shard until a single machine
  is out of write capacity (~5,000 writes/s) or disk** — the cost is not the migration, it is that every
  future feature lives inside today's key.
