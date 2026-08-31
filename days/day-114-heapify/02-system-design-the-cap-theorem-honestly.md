---
day: 114
track: system-design
title: "The CAP theorem, honestly"
phase: "Distributed systems core"
status: written
---

# Day 114 · System Design — The CAP theorem, honestly

**After today you can:** You can state CAP correctly and stop misusing the word availability.

**The interviewer asks it as:** *Explain CAP. Which one does your design give up?*

---

## 1. What this is, and why they ask it

**CAP** says that when the network between your machines breaks, you must choose between **staying
consistent** and **staying available**. That is the whole theorem, and it is much narrower than the way it
is usually quoted.

Three sentences. The popular version — *"pick two of three"* — is wrong in a specific and important way:
**partition tolerance is not a choice**, because networks partition whether or not you approve, so the
real decision is a two-way one and it only applies **during** a partition. The words also do not mean what
they normally mean: **consistency** here is a very strong guarantee about a single value, and
**availability** is a very strong claim that *every* non-failing node answers. And the useful extension —
**PACELC** — points out that the interesting trade-off happens far more often when there is *no*
partition at all, between **latency** and **consistency**.

They ask it because it is the most misquoted result in the field, so it is a fast way to separate people
who have read a summary from people who have thought about it. The tell is what happens when they ask
*"which one do you give up?"* — the good answer is *"neither, until there is a partition; and then it
depends on the operation, and different operations in the same system can choose differently."*

---

## 2. The story

The cloth shop had two branches, one on the main road in Erode and one in Perundurai eleven kilometres
away, and between them they shared one stock book.

The book lived in Erode. When Perundurai sold something, the boy there rang and told them, and the entry
went into the book. When somebody in Perundurai asked whether a particular silk sari was still available —
there was often only one of each — the boy rang and asked.

It worked for years.

Then the exchange had a fault and the two shops could not reach each other. Not the phones being engaged —
completely down, and nobody could say for how long. It happened three or four times a year and it
sometimes lasted two hours.

The manager in Perundurai had exactly two options when a customer stood in front of him with a sari in her
hand and cash in the other, and he had to pick one before he could say anything.

He could **sell it**. Take the money, write it on a slip, and tell Erode later. Fast, and the customer
leaves happy. But if Erode had sold the same sari twenty minutes ago, he has just sold something that
does not exist, and somebody will be telephoned in the evening and told their sari is not coming.

Or he could **refuse**. Say: I cannot confirm this is still here, please come back after five o'clock.
Correct — he will never sell something twice — and the customer is standing there with money and is
being turned away over a telephone fault.

He could not do both. There was no third option, and no amount of cleverness produced one, because the
only thing that would have helped was the thing that was broken.

What he actually did, and what took him a few years to arrive at, was to stop treating it as one decision.

For ordinary cotton — where there were forty of them in the back and one extra sale made no difference —
he sold. For the expensive silks, where there was one of each and a double sale meant a very unpleasant
phone call, he refused and asked people to come back.

And there was a third category he was proud of. For things where he could not check the stock but could
check the *price*, he took an advance and wrote the order, promising to confirm by evening. The customer
went home having done something, and nothing was promised that might not be true.

He told his son once that the mistake people make is arguing about which of the two is right. Both are
wrong. The question is which one is wrong **less**, and that depends entirely on what is being sold.

---

## 3. The idea in plain English

The two shops are a distributed system, the telephone fault is a network partition, and the manager's
final position is the correct understanding of CAP.

- The two branches are **nodes**; the shared stock book is the **data**.
- The exchange fault is a **network partition** — the nodes are alive but cannot talk.
- **Selling anyway** is choosing **availability** (AP).
- **Refusing until the line is back** is choosing **consistency** (CP).
- "Cotton one way, silk the other" is the real answer: **the choice is per operation, not per system.**

### The theorem, stated correctly

> **When a network partition occurs, a distributed system must choose between remaining consistent and
> remaining available. It cannot be both.**

**Note what that sentence does not say.** It says nothing about normal operation. When the network is
healthy, a system can be both consistent and available, and almost all of them are.

The three words, with their real meanings — **and none of them means what it means in ordinary
engineering conversation:**

**C — Consistency.** Specifically **linearizability**: every read sees the most recent write, and the
system behaves as if there were one copy of the data. **This is not the C of ACID**, which is about
integrity constraints. Two different meanings, same letter, endless confusion.

**A — Availability.** **Every** request to a **non-failing** node returns a non-error response. This is
an extremely strong definition — it means no node may say "I am not sure, ask later". **It is not
"99.99% uptime"**, and this is where almost all the misuse comes from.

**P — Partition tolerance.** The system continues to operate when messages between nodes are lost.

### Why "pick two of three" is wrong

**Because P is not optional.** Networks partition: a cable is cut, a switch fails, a rack loses power, a
misconfigured firewall drops packets. You do not get to choose whether it happens; you only choose what
your system does when it does.

```
 "CA" — consistent and available, no partition tolerance
   -> means: a single machine, or a cluster that stops entirely when the
      network breaks
   -> a SINGLE-NODE database is genuinely CA, and that is the only honest example
   -> any distributed system claiming CA is claiming partitions never happen
```

**So the real theorem is a two-way choice made during a partition**, and the systems are labelled CP or AP
by what they do then.

### CP and AP, with real examples

**CP — refuse rather than be wrong.** During a partition, the minority side stops serving. Requests fail
or hang.

```
 ZooKeeper, etcd, Consul     a minority partition refuses all writes
 HBase                       regions become unavailable
 MongoDB (default)           the minority side cannot elect a primary, so no writes
 Spanner                     stops rather than serve stale data
```

**Use CP for anything where a wrong answer is worse than no answer**: configuration, leader election,
locks, account balances, inventory at the point of sale.

**AP — answer anyway and reconcile later.** During a partition, every side keeps serving from what it has.

```
 Cassandra, DynamoDB, Riak   both sides accept reads and writes
 DNS                         serves cached records long after the source is unreachable
 CDNs                        serve stale content rather than nothing
 shopping carts (Dynamo)     merge the divergent versions afterwards
```

**Use AP for anything where a slightly stale answer is much better than an error**: feeds, product
catalogues, recommendations, view counts, session data.

### The manager's point: the choice is per operation

**This is the sentence that makes the answer sound experienced.**

```
 the same e-commerce system:
   browsing the catalogue     AP — a stale price for a few seconds is fine
   adding to a cart           AP — merge divergent carts, Dynamo's own example
   checking out               CP — you cannot sell the last item twice
   the payment itself         CP — obviously
   the order confirmation
     email                    AP — send it late rather than not at all
```

**A system is not CP or AP. Individual operations are.** Cotton and silk.

And there is a third position, which is the manager's advance-order: **degrade rather than refuse.** Do
something useful that promises less — accept the order and confirm later, show cached data and label it
as such, queue the write for when connectivity returns.

### PACELC: the part CAP leaves out

CAP describes what happens during a partition, which is rare. **PACELC** adds the far more common case:

> **If there is a Partition, choose Availability or Consistency. Else, choose Latency or Consistency.**

The "else" half is the one you live with every day. Even with a perfectly healthy network, **making a read
strongly consistent means asking more than one machine, and that costs latency.**

```
 read from the nearest replica           ~1 ms,  possibly stale
 read from the leader                    ~5 ms,  current
 read with a quorum across regions       ~150 ms, current
```

```
 system              partition        no partition
 ---------------     -------------    -----------------------
 DynamoDB            PA               EL   (eventual by default,
                                            strong costs 2x and is slower)
 Cassandra           PA               EL   (tunable per query)
 MongoDB             PC               EC   (reads from the primary by default)
 Spanner             PC               EC   (and pays commit-wait for it)
 PostgreSQL (single) —                EC
```

**PACELC is the more useful framework in practice**, because the "else" branch applies always and the "if"
branch applies for a few minutes a year. Naming it is one of the strongest things you can say about CAP.

### What CAP does not say, and the misuses to avoid

**It is not about uptime.** "We are AP so we have high availability" is a category error. A CP system can
have five nines of uptime; it just refuses service on the minority side of a partition, which is a rare
event.

**It is not a spectrum.** The theorem is a hard impossibility about linearizability, not a dial. The
*dial* exists — it is the [consistency models](../day-115-heapq/README.md) of tomorrow, and the
[quorum settings](../day-117-merge-k-sorted/README.md) of day 117 — but that is a different framework.

**It says nothing about latency, throughput, or partial failures within a node.** Most real outages are
not partitions at all — they are overload, bad deploys and expired certificates.

**And "eventually consistent" is not the same as AP.** Eventual consistency is a guarantee about
convergence over time; AP is a choice made during a partition. They usually travel together and they are
different claims.

---

## 4. The picture

The partition, and the two choices.

```
                    ┌─────────────────┐
                    │   THE NETWORK   │
                    │   IS BROKEN     │
                    └────────┬────────┘
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
   ┌────▼─────┐                             ┌─────▼────┐
   │  Node A  │   ✗ cannot talk to B ✗      │  Node B  │
   │ sari: 1  │                             │ sari: 1  │
   └────┬─────┘                             └─────┬────┘
        │                                         │
   customer asks                             customer asks
   "can I buy it?"                           "can I buy it?"

   ┌─────────────────────┐          ┌─────────────────────────┐
   │  CHOOSE AVAILABLE   │          │   CHOOSE CONSISTENT     │
   │  (AP)               │          │   (CP)                  │
   │                     │          │                         │
   │  "yes" — both sides │          │  "I cannot confirm —    │
   │  sell it            │          │   come back later"      │
   │                     │          │                         │
   │  ✓ nobody is turned │          │  ✓ never sold twice     │
   │    away             │          │  ✗ customer with cash   │
   │  ✗ SOLD TWICE       │          │    is turned away       │
   └─────────────────────┘          └─────────────────────────┘

 THERE IS NO THIRD OPTION. The only thing that would help is the
 thing that is broken.
```

Why "pick two of three" is the wrong picture:

```
 THE POPULAR (WRONG) VERSION          THE HONEST VERSION

        C                              is there a partition?
       / \                                    │
      /   \        "pick 2"           ┌───────┴────────┐
     A ─── P                        NO                YES
                                     │                 │
  suggests CA is a real            you can have    choose ONE:
  choice for a distributed         BOTH C and A     C or A
  system. It is not.                   │
                                  (and PACELC says
  P IS NOT OPTIONAL —              you still trade
  networks partition whether        LATENCY vs
  you like it or not.               CONSISTENCY here)
```

The word "availability" means something unusual here:

```
 CAP AVAILABILITY                     ORDINARY AVAILABILITY
 every non-failing node returns       "the system is up"
 a non-error response                 measured in nines

 a CP system in a partition:          a CP system over a year:
   the minority side returns errors     partitions are rare
   -> NOT "available" by CAP            -> uptime can be 99.99%

 SO: "we chose CP" does NOT mean "our system has poor uptime".
     Confusing the two is the single most common misuse.
```

PACELC — the branch you actually live in:

```
                    ┌──────────────┐
                    │  PARTITION?  │
                    └──────┬───────┘
              YES ─────────┴───────── NO  ("ELSE")
               │                        │
       ┌───────┴───────┐        ┌───────┴────────┐
       │ A  or  C      │        │ L  or  C       │
       └───────────────┘        └────────────────┘
   a few minutes a year        EVERY REQUEST, ALL THE TIME

  DynamoDB    P → A            E → L   (eventual by default; strong costs 2x)
  Cassandra   P → A            E → L   (tunable per query)
  MongoDB     P → C            E → C   (primary reads by default)
  Spanner     P → C            E → C   (and pays commit-wait to do it)

 the "else" branch applies ALWAYS. That is why PACELC is more useful.
```

The manager's real answer — per operation, not per system:

```
 one e-commerce system

 browse catalogue    ████████░░  AP   stale price for 2 s: fine
 add to cart         ████████░░  AP   merge divergent carts
 check stock         ░░░░██████  CP   cannot sell the last one twice
 take payment        ░░░░██████  CP   obviously
 send confirmation   ████████░░  AP   late is better than never

 A SYSTEM IS NOT CP OR AP. OPERATIONS ARE.
 Cotton one way, silk the other.
```

---

## 5. How it actually works

### What a partition actually looks like

Not usually a cut cable. In practice:

```
 an asymmetric partition   A can reach B, but B cannot reach A
 a partial partition       A and B are fine; both lost the third node
 a slow network            not partitioned, just 30 s round trips —
                             which is INDISTINGUISHABLE from a partition
                             from the outside (this is the day 113 point)
 a GC pause                a node is frozen for 20 s and rejoins believing
                             it is still the leader
```

**That last one is why partitions are more common than people think**: a long garbage-collection pause or
a machine swapping is *observationally* a partition, and a system must survive it identically.

### How a CP system behaves

**Require a quorum.** A write, and often a read, needs a majority of nodes to agree.

```
 5 nodes, partitioned 3 | 2
   the side with 3 has a majority  -> keeps serving
   the side with 2 does not        -> refuses
```

**Why odd numbers.** A 4-node cluster split 2|2 has no majority on either side and stops entirely — so
four nodes tolerate exactly the same single failure that three do, at a higher cost.

**Why a majority.** Two majorities cannot exist simultaneously, so there can never be two sides both
believing they may proceed. That single property is what prevents [split-brain](../day-111-serialise-a-tree/README.md).

### How an AP system behaves

**Accept writes on every side, and reconcile afterwards.** Which means you need a conflict-resolution
strategy, chosen deliberately:

```
 LAST WRITE WINS       simplest, and it LOSES DATA — and with clock skew
                         (day 113) it may keep the OLDER write
 VERSION VECTORS       detect concurrency, then hand the conflict to the
                         application — Dynamo's shopping cart
 CRDTs                 data types that merge automatically and correctly:
                         counters, sets, registers. No conflicts by construction.
 APPLICATION MERGE     e.g. union the two carts, which over-keeps rather
                         than losing — Amazon's actual choice
```

**Amazon's shopping-cart example is the canonical one and worth naming**: they chose to union divergent
carts, so an item you deleted might reappear. **Deliberately** — a resurrected item is a much smaller
problem than a lost sale.

### Tunable consistency: the dial that CAP does not describe

Cassandra and DynamoDB let you choose **per query**:

```
 ONE          respond as soon as one replica answers        fastest, weakest
 QUORUM       a majority must answer                        R + W > N
 ALL          every replica must answer                     strongest, brittle
```

```
 N = 3 replicas
   W=1, R=1   fast, may read stale             (1 + 1 = 2, not > 3)
   W=2, R=2   strongly consistent              (2 + 2 = 4 > 3)  ✓
   W=3, R=1   fast reads, brittle writes       (3 + 1 = 4 > 3)  ✓
```

**`R + W > N` is the condition that guarantees an overlap** between the nodes written and the nodes read,
so at least one node returns the newest value. That is [day 117](../day-117-merge-k-sorted/README.md), and
it is the actual dial people mean when they say "we tuned our consistency".

### What real systems do

- **ZooKeeper, etcd, Consul** are CP by design, because they hold configuration and leadership, where a
  wrong answer is far worse than no answer. **Kubernetes stops scheduling if etcd loses quorum** — and that
  is correct behaviour, not a bug.
- **Cassandra and DynamoDB** are AP with tunable consistency, so the same cluster can serve a strongly
  consistent read and an eventually consistent one depending on the query.
- **MongoDB** is CP: the minority side of a partition cannot elect a primary, so it accepts no writes.
- **Spanner** is CP and famously "beats CAP" only in the sense that Google's private network makes
  partitions extremely rare — it still chooses consistency when one occurs, and it pays a **commit-wait**
  of a few milliseconds on every transaction to do it.
- **DNS** is the everyday AP system: it serves cached records for the TTL regardless of whether the
  authoritative server is reachable, and nobody would want it any other way.

---

## 6. The numbers

### How often does a partition actually happen?

```
 a single-datacentre cluster        rare — a few events a year
 cross-datacentre links             more common; several a year is normal
 cross-region / over the internet   routine
 "partition-like" events
   (GC pauses, overload, swap)      MUCH more common than real ones
```

**Google's Spanner papers report that most of their incidents were not network partitions at all**, which
is the honest framing: CAP describes the rare case, and PACELC's "else" branch describes the normal one.

### The cost of consistency when there is no partition

```
 read from the local replica            ~1 ms
 read from the leader, same region      ~5 ms
 quorum read, same region               ~5-10 ms
 quorum read, cross-region              ~150 ms+
 Spanner's commit-wait                  ~5-10 ms on EVERY transaction
```

```
 DynamoDB: a strongly consistent read costs 2x the capacity units
           of an eventually consistent one, and is slower.
 -> the trade is priced, explicitly, per request
```

**That last line is the clearest statement of PACELC anywhere**: a vendor charging double for consistency
is telling you exactly what it costs.

### Quorum arithmetic

```
 nodes   majority   tolerates
 -----   --------   ---------
 3       2          1 failure
 4       3          1 failure   ← no better than 3, and costs more
 5       3          2 failures
 6       4          2 failures  ← no better than 5
 7       4          3 failures
```

**Even numbers buy nothing.** And a 4-node cluster split 2|2 stops entirely, which is worse than a 3-node
cluster split 2|1.

### The cost of AP: reconciliation

```
 a 2-hour partition, 1,000 writes/second on each side
   -> 7.2 million writes on each side to reconcile
   -> with last-write-wins: an unknown number silently discarded
   -> with version vectors: conflicts surfaced to the application
```

**Last-write-wins is not free**, and the amount of data it loses is proportional to the length of the
partition and the write rate. **State that as a number**, because "we use last write wins" sounds
harmless until you multiply it out.

### Availability arithmetic, to separate CAP-A from uptime

```
 a CP system, partitions 4 times a year, 10 minutes each,
 affecting the minority third of nodes:
   downtime for those clients   40 minutes/year   ->  99.992%
   -> a CP system with FOUR NINES of uptime

 "we chose CP" and "we have poor availability" are different claims.
```

---

## 7. The trade-offs

### CP costs you availability exactly when the network is worst

The minority side stops serving. For a config store, that is correct — a wrong configuration is far worse
than none. For a shopping catalogue it is absurd.

**I would not choose CP for anything where a slightly stale answer is acceptable**, because you are paying
real refusals for a guarantee nobody needed.

### AP costs you a reconciliation problem you must actually solve

Accepting writes on both sides means they will diverge, and **"we will sort it out later" is not a
strategy** — you need a chosen mechanism, and every mechanism has a cost:

- **Last-write-wins** silently discards data, and with clock skew it may keep the *older* write.
- **Version vectors** are correct and push the decision to the application, which now has to have an
  answer.
- **CRDTs** merge automatically and correctly, and restrict you to data types that can do so.

**I would not choose AP without naming the resolution strategy**, because that is where the real design
work is.

### The choice is per operation, and saying so is the answer

Cotton and silk. **The strongest version of this answer is to give a table of operations in the system you
are designing and mark each one**, rather than labelling the whole system.

### Where CAP misleads

- **It describes a rare case.** Partitions are minutes a year; the latency-versus-consistency trade is
  every request. **PACELC is the more useful framework**, and saying so is a strong move.
- **The words are unusual.** CAP-availability is not uptime; CAP-consistency is not ACID's C. Most
  arguments about CAP are two people using the same word for different things.
- **"Eventually consistent" is not a synonym for AP.** One is a convergence guarantee, the other is a
  partition-time choice.
- **It ignores the failures that actually cause outages** — overload, bad deploys, expired certificates,
  configuration pushes. **None of those are partitions**, and a CAP-perfect system fails to all of them.

### Where the theorem genuinely bites

- **Multi-region writes.** You cannot have synchronous cross-region replication and low-latency writes;
  physics forbids it. Choose consistency and pay 150 ms, or choose availability and reconcile.
- **Leader election.** By definition it needs agreement, so it is CP — which is why etcd stops rather than
  risk two leaders.
- **Inventory and money.** Where a double-spend is unacceptable, CP is not a preference.

---

## 8. In the interview

### How it gets asked

- The direct one: *"Explain CAP. Which one does your design give up?"*
- The correction test: *"So you pick two of three?"*
- The applied one: *"Would you use Cassandra or PostgreSQL for this?"*
- The precision test: *"What does availability mean there — is that the same as uptime?"*
- The modern one: *"Have you heard of PACELC?"*

### What to say out loud, in the first ninety seconds

1. **State it correctly, and narrowly.** "When a network partition occurs, you must choose between staying
   consistent and staying available. That is all it says — it is silent about normal operation."
2. **Correct "two of three" before it is offered.** "The popular 'pick two of three' framing is
   misleading, because **partition tolerance is not a choice** — networks partition whether you like it or
   not. The only genuine CA system is a single node."
3. **Define the words, because they are unusual.** "Consistency here means **linearizability** — every read
   sees the latest write — not ACID's C. And availability means **every non-failing node returns a
   non-error response**, which is much stronger than 'uptime'. A CP system can have four nines and still be
   'unavailable' by CAP's definition during a partition."
4. **Make the choice per operation.** "And a system is not CP or AP — **operations are**. In one
   e-commerce system, browsing is AP and checkout is CP, because a stale price for two seconds is fine and
   selling the last item twice is not."
5. **Name the third option.** "There is often a middle answer that is better than either: **degrade**.
   Serve cached data and label it, or accept the order and confirm later — do something useful that
   promises less."
6. **Bring in PACELC.** "And the more useful framework is PACELC: if partitioned, availability or
   consistency — **else, latency or consistency**. The else branch applies to every request, all the time,
   and the partition branch applies for a few minutes a year."

### The follow-ups

**"So you pick two of three?"**
"No, and that framing is the main reason CAP is misunderstood. **Partition tolerance is not something you
choose** — cables get cut, switches fail, and a long garbage-collection pause looks exactly like a
partition from outside. So 'CA' is not an option for a distributed system; the only honest CA system is a
single machine, which trivially never partitions. The real theorem is a **two-way choice, made only during
a partition**: when the network breaks, do the isolated nodes keep answering with possibly-stale data, or
do they refuse? When the network is healthy you can have both consistency and availability, and almost
every system does. So the labels CP and AP describe what a system does in a rare situation, not a permanent
property."

**"What does availability mean there — is it uptime?"**
"No, and this is where most of the misuse comes from. CAP's availability is a very strong, formal claim:
**every request to every non-failing node returns a non-error response**. No node is allowed to say 'I am
not sure, try later'. Ordinary availability is a statistic about uptime, measured in nines. They come apart
immediately: a CP system refuses service on the minority side of a partition, so it is not
CAP-available — but if partitions happen four times a year for ten minutes and affect a third of clients,
that is forty minutes a year, which is over four nines of ordinary uptime. So 'we chose CP' and 'we have
poor availability' are completely different claims, and conflating them is the single most common CAP
error."

**"Cassandra or PostgreSQL for this?"**
"That depends on the operation rather than the system, which is the answer I would actually want to give.
Cassandra is AP with tunable consistency: during a partition every side keeps accepting reads and writes,
and you resolve conflicts afterwards — and per query you can ask for ONE, QUORUM or ALL, so you can get a
strongly consistent read when you need one by satisfying `R + W > N`. PostgreSQL with replication is
effectively CP: writes go to one primary, and if that primary is on the wrong side of a partition, writes
stop. So: if the workload is a feed, a catalogue, event ingestion, anything where a two-second-stale answer
is fine and refusing is expensive, Cassandra. If it is money, inventory at the point of sale, or anything
with real invariants across rows, PostgreSQL — and I would want the transactions and joins anyway. And most
real products need both, for different parts."

**"Have you heard of PACELC?"**
"Yes, and I think it is the more useful framework, because it covers the case you actually live in.
PACELC says: **if there is a Partition, choose Availability or Consistency; Else, choose Latency or
Consistency.** The 'else' half is the point — even with a perfectly healthy network, making a read
strongly consistent means consulting more than one machine, and that costs time. Reading from the nearest
replica is about a millisecond and may be stale; a quorum read is five to ten; a cross-region quorum is a
hundred and fifty. DynamoDB prices this explicitly: a strongly consistent read costs twice the capacity of
an eventually consistent one and is slower. So DynamoDB is PA/EL, MongoDB is PC/EC, Spanner is PC/EC and
pays a commit-wait of several milliseconds on every transaction to be so. CAP describes a few minutes a
year; PACELC's else branch describes every request."

**"If you choose AP, what happens to the conflicting writes?"**
"That is the real design work, and 'we will reconcile later' is not an answer — you have to name the
mechanism. **Last-write-wins** is simplest and it silently discards data, and worse, with clock skew it may
keep the *older* write, since two machines' clocks can differ by more than the interval between the
writes. **Version vectors** detect that two writes were genuinely concurrent rather than ordered, and hand
the conflict to the application to resolve — which means the application must have a rule. **CRDTs** are
data types that merge automatically and correctly — counters, sets, registers — so conflicts cannot occur
by construction, at the cost of restricting what you can store. And **application-level merge** is what
Amazon actually did for the shopping cart: union the divergent versions, so a deleted item may reappear.
That is a deliberate choice — a resurrected item annoys a customer, a lost sale costs money. I would also
put a number on it: a two-hour partition at a thousand writes a second on each side is seven million
writes to reconcile, so last-write-wins is discarding an unknown but large quantity."

**"Is there anything better than choosing?"**
"Often, yes, and it is the answer the theorem does not offer you: **degrade**. The theorem forces a choice
between a correct answer and any answer, but you can frequently do something useful that promises less.
Serve cached data and label it as possibly stale. Accept the order and confirm by email rather than
confirming instantly. Queue the write locally and apply it when connectivity returns. Show the catalogue
but disable checkout. Each of those keeps the user making progress without asserting something that might
be false — and in product terms it is nearly always better than either a wrong answer or a blank error
page. So my answer to 'which do you give up' is usually: neither, until there is a partition; and then it
depends on the operation, and for several of them the right answer is to give up **completeness** rather
than either consistency or availability."

### A model answer

Asked: *explain CAP — which one does your design give up?*

> "Let me state it precisely first, because the usual phrasing gets it wrong in a way that matters.
>
> CAP says: **when a network partition occurs, a distributed system must choose between remaining
> consistent and remaining available.** That is the whole theorem. It says nothing about normal operation —
> when the network is healthy you can have both, and nearly every system does.
>
> The popular version, 'pick two of three', is misleading because **partition tolerance is not a choice**.
> Cables get cut, switches fail, and a twenty-second garbage-collection pause is indistinguishable from a
> partition from the outside. You do not choose whether partitions happen; you only choose what you do
> when one does. The only genuine 'CA' system is a single machine, which never partitions because there is
> nothing to partition.
>
> The words also do not mean what they normally mean, and most CAP arguments are really vocabulary
> arguments. **Consistency** here is **linearizability** — every read sees the most recent write, as if
> there were one copy — not the C of ACID, which is about integrity constraints. And **availability** is a
> very strong formal claim: **every** request to **every** non-failing node returns a non-error response.
> That is not uptime. A CP system refuses on the minority side of a partition, so it is not CAP-available —
> and if partitions cost forty minutes a year, it still has better than four nines of ordinary uptime.
>
> So, to your question: **my design gives up neither, until there is a partition.** And then the honest
> answer is that it depends on the operation, because **a system is not CP or AP — operations are.** In an
> e-commerce system I would make browsing the catalogue AP, because a price that is two seconds stale is
> fine and refusing to show the shop is absurd. I would make the cart AP and merge divergent versions —
> which is what Amazon actually did, deliberately over-keeping items rather than losing a sale. And I would
> make the stock check and the payment CP, because selling the last item twice is a real cost that a
> refusal is not.
>
> If I choose AP anywhere, I would name the reconciliation mechanism rather than saying 'we will sort it
> out': last-write-wins silently loses data and, with clock skew, can keep the *older* write; version
> vectors detect true concurrency and hand it to the application; CRDTs merge correctly by construction.
>
> Two things I would add. There is often a **third option** better than either — degrade: serve cached data
> and label it, take the order and confirm later, disable checkout but keep the catalogue up. And the more
> useful framework is **PACELC**: if partitioned, availability or consistency; **else, latency or
> consistency**. That 'else' branch applies to every single request, all the time — DynamoDB charges twice
> as much for a strongly consistent read as an eventual one — whereas CAP's branch applies for a few
> minutes a year."

---

## 9. Recall card

- **The correct statement: WHEN A PARTITION OCCURS, choose between consistency and availability.** It says
  nothing about normal operation. **"Pick two of three" is wrong because P is not a choice** — cables cut,
  and a 20-second GC pause is indistinguishable from a partition. **The only genuine CA system is a single
  node.**
- **The words are unusual. C = linearizability** (every read sees the latest write) — **not ACID's C**.
  **A = every non-failing node returns a non-error response** — **not uptime**. A CP system can refuse
  during partitions and still have **four nines** of ordinary availability. Conflating those is the most
  common misuse.
- **A system is not CP or AP — OPERATIONS are.** In one shop: browse AP, cart AP (merge), stock check CP,
  payment CP. **CP: etcd, ZooKeeper, MongoDB, Spanner, HBase. AP: Cassandra, DynamoDB, Riak, DNS, CDNs.**
  And there is a **third option the theorem does not offer: degrade** — serve labelled stale data, accept
  and confirm later, keep the catalogue and disable checkout.
- **If AP, name the reconciliation mechanism.** Last-write-wins **silently loses data** and with clock skew
  may keep the **older** write; version vectors detect true concurrency; CRDTs merge by construction;
  Amazon's cart **unions** divergent versions on purpose. A 2-hour partition at 1,000 writes/s per side is
  **7 million writes** to reconcile.
- **PACELC is the more useful framework: if Partitioned, A or C; ELSE, Latency or Consistency.** The else
  branch applies to **every request** — local replica ~1 ms and stale, quorum ~5–10 ms, cross-region
  quorum ~150 ms — and **DynamoDB charges 2× for a strongly consistent read**, which is the trade, priced.
  Quorums need **odd** cluster sizes: 4 nodes tolerate no more failures than 3, and split 2|2 they stop
  entirely.
