---
day: 36
track: system-design
title: "NoSQL: what it actually means"
phase: "Databases from zero"
status: written
---

# Day 036 · System Design — NoSQL: what it actually means

**After today you can:** You can stop saying NoSQL is faster and start naming the real trade-off.

**The interviewer asks it as:** *What is the difference between SQL and NoSQL?*

---

## 1. What this is, and why they ask it

**NoSQL** is a family name for databases that do not organise data as normalised relational tables —
key-value stores, document stores, wide-column stores, graph stores. The name says what they are
*not*, which is why it confuses people: the four families have less in common with each other than
some of them have with Postgres. What they share is one design decision: **store the data in the
shape you will read it, instead of one fact in one place assembled by joins.**

Interviewers ask "SQL versus NoSQL?" at every level, and it is a trap question in a specific way:
the popular answer — *"NoSQL is faster and scales better"* — is a failing answer, because it is a
slogan where a trade-off should be. The answer that passes names what you give up (joins, ad-hoc
questions, cross-entity transactions, single-copy facts) and what you buy (access-path speed,
horizontal scaling, flexible records), and then refuses to pick a side without knowing the access
patterns. The next four days walk the families one by one; today builds the frame they hang on.

---

## 2. The story

Two women in one family feed people for a living, and their kitchens disagree about everything.

Meena runs a tiffin service from her flat — forty steel boxes out of the door by nine, a different
menu every day. Her kitchen is arranged like a shop. Every ingredient has one labelled jar, every
jar has one place on the racks: dals on the second shelf, spices in the drawer in alphabetical
order, rice and flours at the bottom. Ask her how much cumin is left and she answers in five
seconds, from one jar. When the wholesaler changes her turmeric brand, she changes one jar. But
cooking any single dish means walking the kitchen — eight jars from five shelves for a simple
sambar — and on a morning when three dishes run in parallel, most of her time is collecting.

Her sister-in-law Farida runs a dosa cart near the college, and the cart is arranged like the
serving window, not like a shop. One tub per item on the menu. The masala dosa tub holds everything
masala dosas need — the batter, the potato filling, the chutney portions, the ladle. Order comes;
she pulls one tub; everything is in her hand. No walking, no collecting. That is why her queue
moves.

But ask Farida how much cumin she has and she laughs. There is cumin in the dosa tub, cumin in the
upma tub, cumin in three chutney boxes — she would have to open every tub and add it up, and she has
never once done it. When her salt supplier changed, she repacked nine tubs. And when her nephew
suggested a new item for the menu, the hard part was not the recipe — it was that nothing on the
cart was arranged for it.

Neither kitchen is wrong. Meena's is arranged for **questions** — any question, asked once, answered
from one place. Farida's is arranged for **serving** — one known order, served fast, a thousand
times a day. Each pays for its arrangement exactly where the other collects.

---

## 3. The idea in plain English

Meena's kitchen is a relational database. Farida's cart is NoSQL. The whole of today is in the last
line of the story: **arranged for questions, or arranged for serving** — and each pays where the
other collects.

### The relational deal, restated

Everything since [day 026](../day-026-strings-revision/README.md) has described Meena's kitchen.
**Normalisation** — [day 029](../day-029-read-write-pointer/README.md) — puts each fact in exactly
one place: one jar per ingredient. **Joins** — [day 028](../day-028-opposite-ends/README.md) —
assemble a dish by walking the shelves. The payoff is enormous and easy to forget: *any* question
can be asked, including ones nobody predicted, and every answer is consistent because no fact has a
second copy that could disagree. The price is the walking — every read that spans entities pays for
assembly at read time.

### The NoSQL deal

Turn it around. Decide **first** what the application will ask — "give me this user's cart",
"render this product page" — and store each answer pre-assembled, like Farida's tubs. A read
becomes one lookup of one shaped record. The price arrives on the other side of the counter:

- **Unplanned questions are expensive or impossible.** "How much cumin?" means opening every tub —
  a full scan, or a separate analytics copy of the data.
- **Facts get copied**, and copies drift. The supplier change touched nine tubs. Every copy needs
  the reconciliation discipline [day 029](../day-029-read-write-pointer/README.md) demanded.
- **Guarantees shrink to the tub.** Most NoSQL stores make their ACID promises about one record,
  not across records — [day 033](../day-033-window-with-a-map/README.md)'s transaction, at its
  full strength, is a relational feature.

### The four families, in one pass

"NoSQL" covers four different data models. One line each today; the next three days take them up
properly:

| Family | The record is | Products | Built for |
|---|---|---|---|
| **Key-value** | an opaque value behind a key | Redis, DynamoDB | exact-key lookups, blindingly fast — [day 037](../day-037-prefix-sums/README.md) |
| **Document** | a nested JSON-like document | MongoDB | one entity's whole world in one read — [day 038](../day-038-subarray-sum-k/README.md) |
| **Wide-column** | rows grouped and sorted within partitions | Cassandra | huge write volume, known queries — [day 039](../day-039-difference-arrays/README.md) |
| **Graph** | nodes and edges | Neo4j | relationship-walking questions |

### Why "NoSQL is faster" is not a sentence

Faster **at what**? Farida serves a dosa faster than Meena could — and answers the cumin question
somewhere between slowly and never. A document store renders the page it was shaped for in one
read; ask it for "all users who bought X and Y last month" and it is slower than the relational
database would have been, or silent. Speed is a property of a *query against an arrangement*, not
of a product. The honest comparison is: **NoSQL is faster at the access paths you designed in, by
paying for them at write time and giving up the paths you did not.** Say it that way and the
interview changes tone.

There is a second, real reason for the family's reputation, and it deserves its own sentence:
**horizontal scaling**. Records that never need joining can be spread across a hundred machines by
key, and each request touches one machine. Relational joins want the data together; splitting a
relational database across machines is the hard, later part of this course. When people say "NoSQL
scales", this — not raw speed — is the thing that is true.

---

## 4. The picture

The same blog post, served by both kitchens:

```
 RELATIONAL — arranged for questions          DOCUMENT — arranged for serving

 users                                        posts collection, one document:
 +----+---------+                             {
 | id | name    |                               "title":  "Why B-trees",
 +----+---------+                               "author": {"id": 7,
 posts          comments        tags                        "name": "Meena"},
 +----+------+  +----+------+  +-----+          "comments": [ ... ],
 | id |title |  |post| body |  |post |          "tags": ["storage", "trees"]
 +----+------+  +----+------+  +-----+        }

 read = 1 query joining 4 tables              read = 1 lookup, already shaped
        (or 4 round trips, done badly)
 write "rename Meena"  = 1 row                write "rename Meena" = every
                                              document she ever wrote
 "all posts tagged X"  = easy                 "all posts tagged X" = only if
 "top commenters"      = easy                 you shaped an index for it;
                                              "top commenters" = a scan
```

**What to notice:** neither column is winning. Read the two "rename" lines, then the two
bottom-left questions — every advantage on one side has its bill on the other.

Why the split-across-machines argument favours the tubs:

```
 by key, no joins:                      with joins:

 machine A: users a-h    request for    posts on machine A,
 machine B: users i-q    user "meena"   comments on machine B,
 machine C: users r-z    -> ONE         users on machine C ->
                            machine     every join crosses the network
```

**What to notice:** the key-shaped arrangement gives each request a single home. The join-shaped
arrangement makes the network part of every query — which is the hard problem the distributed
phase of this course exists to study.

---

## 5. How it actually works

### Key-value: Redis and DynamoDB

The store is a giant dictionary: `GET key`, `PUT key value`, the value opaque. Redis keeps it in
memory — sub-millisecond reads, hundreds of thousands of operations a second on one node — and is
the standard cache, session store and counter. DynamoDB puts the same model on disk across many
machines with hash partitioning by key: single-digit-millisecond reads at any scale, priced per
request. Neither can answer "which values contain X?" — there is no *inside* to the value, as far
as the store is concerned. Tomorrow's lesson.

### Document: MongoDB

Records are JSON-like documents, nested, flexible per record, gathered into collections. The unit
of atomicity is **one document** — updating one document is atomic; updating three is your problem
unless you opt into its newer multi-document transactions, which cost. Secondary indexes exist, so
it is far more queryable than a key-value store — but the design centre is still "one entity, one
document, one read". [Day 038](../day-038-subarray-sum-k/README.md).

### Wide-column: Cassandra

Rows live inside **partitions** chosen by a partition key; within a partition, rows are sorted by
clustering columns. Writes append to a log-structured merge tree — from
[day 031](../day-031-fixed-window/README.md), the write-favouring shape — which is why Cassandra
swallows enormous write volumes across hundreds of nodes with no single leader. The price is that
**you must know your queries when you design the table**: data is queryable by its partition key
and sort order, and very little else. [Day 039](../day-039-difference-arrays/README.md).

### Graph: Neo4j

Nodes and edges as first-class records, so "friends of friends who like X" walks pointers instead
of joining tables repeatedly. Niche but unbeatable in its niche — recommendation, fraud rings,
networks. It gets this one line today, and reappears in the graphs phase of the DSA track.

### The blur, which interviewers respect you for naming

The border is not clean, and saying so signals currency. Postgres has `JSONB` — documents inside a
relational database, indexed, queried, transactional — which quietly serves most "we might need
Mongo" cases. MongoDB grew multi-document transactions. And **distributed SQL** — Google Spanner,
CockroachDB — puts real SQL and real transactions on top of horizontal partitioning, at the cost of
coordination machinery that belongs to the later phases of this course. The families are
converging; the *trade-offs* are what stay fixed, which is why today taught the trade-offs.

---

## 6. The numbers

### The read the document was shaped for

Rendering one product page:

```
relational, done badly (one query per table, sequentially):
  4 round trips × (0.5 ms network + query time ~0.5 ms) ≈ 4 ms
relational, done properly (one join): ≈ 1-1.5 ms
document store, one shaped read:      ≈ 0.5-1 ms

at 1,000 pages/second the gap between properly-joined SQL and a
document read is real but small. The 4-round-trip version is the
one that hurts — and that is an application bug, not a database law.
```

The honest number: most of the speed people attribute to NoSQL is the speed of **one read versus
several round trips** — which a well-written join usually also achieves.

### The write the document pays

The duplicated fact, priced:

```
author's name embedded in 40,000 of her documents, 20 bytes each:
  storage cost: 800 KB               -> nothing. storage is not the issue.
  rename cost:  40,000 document writes vs 1 row update
  at 5 ms per write, done naively:   200 seconds of writing
```

Duplication is cheap to hold and expensive to change — which is why the modelling question
tomorrow-but-one is *"how often does this fact change?"*, not *"how big is it?"*.

### Where horizontal scaling actually bites

```
one well-tuned Postgres node comfortably serves:
  ~10,000-50,000 simple transactions/second, terabytes of data

Cassandra at Discord/Netflix scale:
  millions of writes/second across hundreds of nodes

the gap between those two lines is the honest domain of NoSQL-for-scale.
Most products live their whole lives inside the first line.
```

The multiplication to carry: 50 million users × 20 events a day = 1 billion writes ≈ 11,600 a
second average — **inside one Postgres node's range**. NoSQL-for-scale is a real need at a scale
most systems never reach, and knowing which side of the line a design sits on is the entire game
of [day 040](../day-040-2d-prefix-sums/README.md).

---

## 7. The trade-offs

### What you hand over at the door

Choosing a NoSQL store for a system's main record of truth gives up, in rough order of pain:
**ad-hoc questions** (the analytics team now needs a copy of the data somewhere queryable),
**cross-entity transactions** (the all-or-nothing of [day 033](../day-033-window-with-a-map/README.md)
shrinks to one record), **single-copy facts** (every embedded copy needs an owner and a
reconciliation path), and **joins** (assembly becomes application code). What you get: reads shaped
to the product's hot paths, writes that scale by adding machines, and records that vary without
schema ceremony.

### I would not use it if...

**I would not choose NoSQL if** the access patterns are still unknown — early products pivot, and
a relational schema is the arrangement that survives a pivot, because it is arranged for questions
you have not thought of yet. **I would not choose it if** the domain is transactional across
entities — money moving between accounts is a two-row atomic write, and that is the relational
deal. **And I would not choose relational alone if** one access path utterly dominates at a scale
one node cannot hold — a feed, a session store, an event firehose — which is precisely where the
next three days' tools earn their keep.

### The honest default

> Start relational — Postgres — and add specialised stores per access path as measurements demand:
> Redis in front for hot keys, a document or wide-column store when a specific read or write path
> outgrows the node. "SQL or NoSQL" is rarely the real decision in production; the real decision is
> **which access path gets its own arrangement**, and most systems end up polyglot for exactly
> Meena-and-Farida reasons.

---

## 8. In the interview

### How it gets asked

- *"What is the difference between SQL and NoSQL?"* — the direct form; they are listening for a
  trade-off, not a feature list.
- *"Why is NoSQL faster?"* — the baited form; the right answer disputes the premise politely.
- *"Would you use MongoDB or Postgres for this?"* — the applied form, which is
  [day 040](../day-040-2d-prefix-sums/README.md)'s whole lesson.
- *"How can Cassandra handle writes Postgres can't?"* — the mechanism form: partitioning by key,
  no joins to keep together, log-structured writes.

### What to say out loud, in the first ninety seconds

1. **Refuse the slogan in the first sentence.** *"NoSQL isn't one thing and isn't simply faster —
   it's four data models sharing one decision: store data in the shape you'll read it, instead of
   normalised tables assembled by joins."*
2. **Name the trade in both directions.** *"You buy your designed access paths — one shaped read,
   partitionable by key across machines. You sell ad-hoc queries, cross-record transactions, and
   single-copy facts."*
3. **Give the families ten seconds.** *"Key-value for exact lookups — Redis, DynamoDB. Document
   for one entity's world in one read — MongoDB. Wide-column for huge write volume with known
   queries — Cassandra. Graph for relationship-walking — Neo4j."*
4. **Say where the scaling claim is true.** *"The real scaling advantage is horizontal: no joins
   means data splits cleanly by key, one machine per request. That's true — and it matters above a
   scale one good Postgres node can't hold, which is further away than people think."*
5. **Land on the default.** *"So my default is relational until a named access path and a real
   number push a piece of the data into a specialised store."*

### The follow-ups

**"So is NoSQL ever actually faster?"**
Yes — at the access path it was shaped for, and the mechanism is worth naming precisely. A document
read replaces a join: the assembly work moved from read time to write time, so the read is one
lookup of pre-assembled data. A key-value read replaces even the parsing: Redis serves from memory
in under a millisecond. A Cassandra write appends to a log-structured tree instead of updating a
B-tree in place — day 031's read-favouring versus write-favouring shapes — so sustained write
throughput per node is genuinely higher. Every one of those is a real speedup, and every one is
paid for: the document store answers unplanned questions badly, the key-value store not at all, and
Cassandra requires the queries to be designed into the table. What is *not* true is the blanket
claim — put a well-indexed Postgres and a document store side by side on an ad-hoc analytical
question and the relational side wins, because that is the query *it* is arranged for.

**"Why does NoSQL scale horizontally more easily than a relational database?"**
Because of what has to stay together. If records never join, you can split them across a hundred
machines by hashing the key, and every request computes its machine and touches only it — no
cross-machine coordination on the read path, so capacity grows nearly linearly with machines. A
relational database's value is precisely the cross-record operations — joins and multi-row
transactions — and those want the participating rows on the same machine. Split the tables across
machines and a join becomes network traffic and a transaction becomes a distributed commit, which
is the expensive machinery from day 033's two-phase-commit discussion. It is not that relational
databases cannot be distributed — Spanner and CockroachDB do it — it is that they must solve the
coordination problem NoSQL sidesteps by giving up the operations that need it. Same trade as
everywhere today: the families that scale easiest are the ones that promised least across records.

**"MongoDB has transactions now. Doesn't that end the debate?"**
It narrows it, and the direction of travel is real — Mongo grew multi-document ACID, Postgres grew
JSONB documents, and distributed SQL grew both. But defaults and design centres still differ. In
Postgres, a five-row transaction is the free, normal case; in MongoDB it is an opt-in with latency
and abort costs, on top of a data model that encourages you not to need it — the idiomatic Mongo
design embeds related data in one document so the single-document atomic update suffices. Choosing
by feature checklist misses this: the question is not "does it have transactions?" but "is the
workload's normal case the store's normal case?". A domain that constantly needs cross-entity
atomicity is fighting a document store's grain even when the feature exists — and a domain that
reads one aggregate at a time is paying Postgres's assembly cost for guarantees it rarely uses.
Grain over checklist is the durable answer.

### A model answer

> "NoSQL is an umbrella for four data models — key-value, document, wide-column, graph — that share
> one decision: store the data in the shape you'll read it, rather than normalised tables assembled
> by joins at read time.
>
> That decision trades in both directions. You buy the designed access paths: a product page is one
> shaped read instead of a four-table join, and because records don't join, data splits cleanly by
> key across machines — that's the honest version of 'NoSQL scales'. You sell the things
> normalisation gave you: ad-hoc questions the design didn't anticipate, transactions that span
> records, and facts that exist in one place — an embedded author name lives in forty thousand
> documents, and renaming her is forty thousand writes instead of one.
>
> So 'NoSQL is faster' isn't a sentence I'd say. Faster at what? A document store beats Postgres at
> the read it was shaped for and loses on the analytical question nobody planned. Speed belongs to
> a query against an arrangement, not to a product.
>
> Concretely: Redis and DynamoDB for exact-key lookups, MongoDB when one entity's whole world is
> read as a unit, Cassandra when write volume outgrows a node and the queries are known in advance,
> Neo4j for relationship-heavy questions. And one honest number for calibration: a billion events a
> day is about twelve thousand writes a second, which a single tuned Postgres node handles — so my
> default is relational until a named access path with a real number outgrows it, and then that
> path, not the whole system, moves to the store shaped for it."

---

## 9. Recall card

- **NoSQL = four models, one decision:** store data in the shape you will read it. Arranged for
  serving; relational is arranged for questions.
- **The trade, both directions:** buy designed access paths + horizontal scaling by key; sell
  ad-hoc queries, cross-record transactions, single-copy facts.
- **"Faster" needs an object.** Faster at the shaped path (assembly moved to write time); slower or
  silent elsewhere. Speed belongs to a query against an arrangement.
- **The scaling claim, stated honestly:** no joins → split by key → one machine per request. It
  matters above what one node holds (~tens of thousands of TPS) — most systems never get there.
- **Families and homes:** Redis/DynamoDB key-value, MongoDB document, Cassandra wide-column, Neo4j
  graph — and Postgres JSONB quietly covers many "need Mongo" cases. Default relational; move
  access paths, not systems.
