---
day: 115
track: system-design
title: "Consistency models"
phase: "Distributed systems core"
status: written
---

# Day 115 · System Design — Consistency models

**After today you can:** You can order strong, causal and eventual consistency and give an example of each.

**The interviewer asks it as:** *What consistency does this feature need? Justify it.*

---

## 1. What this is, and why they ask it

A **consistency model** is a promise about what a read may return when there are several copies of the
data. [CAP](../day-114-heapify/README.md) said you must sometimes give up consistency; today is about the
fact that consistency is not one thing you either have or lose — **it is a ladder**, and you choose a
rung.

Three sentences. At the top is **linearizability**: the system behaves as if there were one copy and every
operation happened at a single instant, which is what a single machine gives you for free and what a
distributed system pays dearly for. At the bottom is **eventual consistency**: if writes stop, the copies
will agree — eventually, with no promise about when or what you see meanwhile. And the interesting rungs
are in the middle, particularly **causal consistency** and the four **session guarantees**, because they
are what users actually notice and they are much cheaper than the top.

They ask *"what consistency does this feature need?"* because the answer is almost never "strong" and
almost never "eventual" for a whole system — it is **per operation**, and the good answer names the
specific anomaly it is preventing. A candidate who says "we'll use eventual consistency" without being
able to say *which* anomaly a user would see has not chosen anything.

---

## 2. The story

The news that Kuppan's daughter had got the government job reached the village on a Tuesday, and Sarala
spent the rest of the week reconstructing how.

It had started with Kuppan telling Ratnam at the milk booth at six in the morning. By eight, four people
knew. By noon, most of the main street. By the evening, the far end near the burial ground had it, and by
Thursday the outlying farms.

Three things about how it travelled struck her as interesting, and she pointed them out to her
daughter-in-law, who was less interested.

The first was that at any given moment, different people knew different things, and none of them was
wrong. The woman at the far end who had not heard yet was not mistaken — she simply had older
information. And if you had stopped everybody talking on Tuesday evening, by Thursday everyone would have
had the same news, without anybody doing anything special. It sorted itself out.

The second was about order, and this was the part she thought mattered. On Wednesday there was a second
piece of news: that the family was arranging a small function on Sunday. Now — **nobody in the village
heard about the function before they heard about the job.** Not one person. Because the function only
made sense as a consequence of the job, so whoever passed it on always said both, in that order. The news
travelled at different speeds to different people, but it never arrived out of order, because each piece
was carried by somebody who already had the earlier piece.

The third was the one that had actually caused trouble, twice.

Sarala's own sister lived two streets away, and on Wednesday morning Sarala told her about the function.
In the afternoon her sister came back from the temple and said, quite crossly, that she had asked three
people and nobody had said anything about a function, and had Sarala made it up.

She had not. Her sister had simply asked people who had not been told yet. And what upset her was not
being behind — it was that **she had heard it, and then heard nothing, and the second thing felt like it
had taken the first one away.**

Sarala said the rule she had learned over sixty years was that you could not make news travel faster. What
you could do was be careful about **who you sent somebody to ask**. If she wanted her sister to hear
something confirmed, she sent her to the person she had told herself.

---

## 3. The idea in plain English

The village is an eventually consistent system, and Sarala has identified the three things that matter:
convergence, causal order, and the session guarantees.

- Different people knowing different things is **replica divergence** — and none of them is wrong.
- "By Thursday everyone had it" is **eventual consistency**: convergence if writes stop.
- The function never arriving before the job is **causal consistency**.
- Her sister hearing it and then not hearing it is a **monotonic reads** violation.
- "Send her to the person I told" is **session guarantees** — routing to preserve what one person has
  seen.

### The ladder

```
 STRONGEST
    │
    │  LINEARIZABLE          as if there were ONE copy; every read sees the
    │   (strong)              latest write, and operations appear to happen
    │                         at a single instant
    │
    │  SEQUENTIAL            all nodes see the SAME order of operations,
    │                         but it need not match real time
    │
    │  CAUSAL                operations that are causally related are seen
    │                         in order by everyone; unrelated ones may differ
    │
    │  SESSION GUARANTEES    per-client promises: read-your-writes,
    │   (read-your-writes,    monotonic reads, monotonic writes,
    │    monotonic, prefix)   consistent prefix
    │
    │  EVENTUAL              if writes stop, the copies converge. No promise
    │                         about when, or about what you see meanwhile.
    ▼
 WEAKEST — and CHEAPEST, and FASTEST
```

**Going down the ladder buys latency and availability and costs anomalies.** The engineering question is
always *which anomaly can this feature tolerate?* — not *how consistent can we be?*

### Linearizable: as if there were one copy

**The definition to give**: every operation appears to take effect at a single instant between its start
and its completion, and every read returns the most recently completed write.

The consequence that makes it expensive: **it is a real-time guarantee.** If I write and then telephone
you, and you read, you must see my write — even though our two operations touched different machines and
nothing connects them but the phone call.

```
 what it costs:
   a read must consult a majority, or come from the leader
   -> same region:   ~5-10 ms instead of ~1 ms
   -> cross-region:  ~150 ms
   -> and during a partition, the minority side must REFUSE  (CAP)
```

**Use it for**: locks, leader election, unique-constraint checks, account balances at the moment of a
transfer, inventory at the point of sale, anything where two clients can race for the same thing.

### Sequential: everyone agrees on an order, just not the real one

All nodes observe the same sequence of operations, and each client's own operations appear in the order it
issued them — but the global order need not match wall-clock time.

```
 A writes x=1 at 10:00:00
 B writes x=2 at 10:00:01
 -> a sequentially consistent system may order them (x=2, x=1)
    as long as EVERY node sees that same order
```

**In practice this rung is rarely offered explicitly**, but it is worth knowing because it is exactly the
gap between "everyone agrees" and "it matches real time" — and that gap is what makes linearizability
expensive.

### Causal: the important middle rung

**If one operation could have influenced another, everyone sees them in that order. Operations that could
not have influenced each other may be seen in any order.**

The village's news. Nobody heard about the function before the job, because the function was only ever
passed on by somebody who already had the job news.

```
 causally related      A posts a photo, then A comments on it
                       -> nobody sees the comment before the photo
 concurrent            A posts a photo, B posts an unrelated photo
                       -> different viewers may see them in either order,
                          and that is FINE
```

**Why it matters**: almost every anomaly users actually complain about is a *causality* violation, not a
staleness one.

```
 "I replied to a message that isn't there"           causal violation — REAL bug
 "the like count says 41 and my friend sees 42"      staleness — nobody cares
```

**Causal consistency is available during a partition**, which linearizability is not — so it is the
strongest model that is still AP. That single fact is why it is the most interesting rung on the ladder,
and it is implemented with the vector clocks and version vectors from
[day 113](../day-113-the-heap/README.md).

### The four session guarantees

These are per-client promises, cheap to implement, and they cover most of what users notice.

**Read-your-writes.** *If I do something, I see it.* The most-reported bug in the phase —
[day 105](../day-105-lowest-common-ancestor/README.md). Fix: route a user's reads to the leader for a
window after they write, or carry a version token.

**Monotonic reads.** *Time does not go backwards.* Sarala's sister. If I see a value, a later read must
not show an older one. Fix: **pin a client to one replica**.

**Monotonic writes.** *My own writes are applied in the order I made them.* If I set my name and then set
my photo, the system must not apply them in the other order. Fix: route a client's writes through one
path, or number them.

**Consistent prefix reads.** *Cause before effect.* You must not see the answer to a question before the
question. Mostly a **sharding** problem — two related writes travelling through different partitions can
arrive out of order.

**These four are worth memorising as a set**, because "which of the four does this feature need?" is a
much better answer than "strong or eventual".

### Eventual: convergence, and nothing else

**If writes stop, all replicas will converge to the same value.** That is the entire promise. It says
nothing about how long, and nothing about what a read returns meanwhile.

**Which means it permits things that surprise people:**

```
 a read may return a value older than one you already saw   (no monotonic reads)
 you may not see your own write                             (no read-your-writes)
 two reads in a row may disagree                            (no ordering at all)
 a value may go 5 -> 7 -> 5 -> 7 before settling
```

**"Eventually" has no bound.** In practice convergence is milliseconds; during a partition it is the
length of the partition; and if two replicas never reconcile, it is never.

**Use it for**: view counts, like counts, recommendations, search indexes, analytics, anything where the
user cannot tell and would not care.

**And the honest addition:** eventual consistency requires a **conflict resolution** strategy, which is
where the real design work is — last-write-wins (which loses data), version vectors, CRDTs, or an
application merge.

### CRDTs, briefly, because they change the question

A **conflict-free replicated data type** is a structure whose merge function is designed so that any two
replicas that have seen the same set of updates end up identical, **regardless of the order they arrived
in**.

```
 a G-counter        each node counts its own increments; merge = sum
 a G-set            add-only; merge = union
 an OR-set          add and remove with tags; merge is well defined
 an LWW-register    last write wins, with a tie-break rule
```

**The point is that conflicts become impossible by construction**, not that they are resolved well. The
price is that you can only store what a CRDT can express — and a bank balance with a minimum of zero is
not one of them, because "do not go below zero" is a global invariant and CRDTs deliberately have none.

**Redis, Riak and collaborative editors use them.** Naming CRDTs and saying what they cannot do is a
strong finish.

### How to choose, in one question

> **What would a user actually notice, and how bad is it?**

```
 the user does something and cannot see it       -> read-your-writes. Fix it.
 the user sees it, then it vanishes              -> monotonic reads. Fix it.
 a reply appears before the message              -> causal. Fix it.
 two people can take the same seat               -> LINEARIZABLE. No choice.
 the like count is off by one for two seconds    -> eventual. Leave it.
```

**Name the anomaly, not the model.** That is the whole skill.

---

## 4. The picture

The ladder, with the cost on one side and the anomalies on the other.

```
              cost                                   what it prevents
              ────                                   ────────────────
 LINEARIZABLE  ████████████  leader or quorum         everything
               ~5-150 ms     reads; refuses during    (and it is the only
                             a partition               one that prevents races)
                    │
 SEQUENTIAL    ██████████    global agreement on      disagreement about order
                             order, not on time
                    │
 CAUSAL        ██████        version vectors;         effect-before-cause
               ~1-5 ms       AVAILABLE during a       ← the strongest model
                             partition                  that is still AP
                    │
 SESSION       ████          per-client routing       "I can't see my own post"
 GUARANTEES    ~1 ms         or a token               "it appeared then vanished"
                    │
 EVENTUAL      █             read the nearest         nothing — only convergence
               ~1 ms         replica                  (if writes stop)

 going DOWN buys latency and availability, and costs anomalies.
 the question is never "how consistent can we be" — it is
 "WHICH ANOMALY CAN THIS FEATURE TOLERATE?"
```

The village, as the ladder:

```
 EVENTUAL         by Thursday everyone knew — with no one doing anything special
                  "different people knew different things, and none was wrong"

 CAUSAL           NOBODY heard about the function before the job,
                  because whoever passed on the function already had the job news
                  -> causally related news never arrived out of order

 MONOTONIC READS  Sarala's sister heard it, then asked three people who had not
                  been told, and it FELT like the news had been taken away
                  -> the violation users actually complain about

 THE FIX          "send her to the person I told" — route her to a replica
                  that has already seen it
```

The four session guarantees, with the user's own words:

```
 READ-YOUR-WRITES     "I posted it and it's not there"
                      write -> leader.  read -> a replica that hasn't caught up.
                      FIX: read from the leader for ~30 s after a write.

 MONOTONIC READS      "it was there, now it's gone"
                      read 1 -> replica A (lag 20 ms).  read 2 -> replica B (lag 2 s).
                      FIX: pin the client to ONE replica.

 MONOTONIC WRITES     "I changed my name then my photo, and the name reverted"
                      write 1 and write 2 took different paths and arrived
                      out of order.
                      FIX: one write path per client, or sequence numbers.

 CONSISTENT PREFIX    "the reply is above the message"
                      two related writes on DIFFERENT SHARDS arrive out of order.
                      FIX: co-locate related writes, or a causal token.
```

Which rung for which feature:

```
 feature                       model            why
 ---------------------------   --------------   ---------------------------------
 seat booking                  LINEARIZABLE     two people, one seat
 account balance at transfer   LINEARIZABLE     a race is money
 leader election / a lock      LINEARIZABLE     two leaders is a disaster
 a user's own profile edit     read-your-writes "I saved it and nothing changed"
 a chat thread                 CAUSAL           a reply before its message
 a social feed                 CAUSAL           a comment before its post
 a like count                  EVENTUAL         off by one for 2 s: invisible
 a recommendation list         EVENTUAL         nobody can tell
 an analytics dashboard        EVENTUAL         minutes stale is expected

 A SYSTEM IS NOT "STRONGLY CONSISTENT". OPERATIONS ARE.
```

---

## 5. How it actually works

### Achieving each rung

**Linearizable**: all reads and writes go through a single leader, **or** a quorum with `R + W > N` plus a
protocol that prevents a stale leader answering. **The subtlety is that quorum reads alone are not
enough** — you also need to defend against an old leader that has not yet noticed it was replaced, which is
what fencing and epoch numbers do.

**Causal**: attach a **version vector** to each write recording what the writer had seen, and a replica
delays applying a write until it has applied everything that write depends on. That is why causal
consistency is available during a partition: a replica can keep serving from what it has, and it just
holds back writes whose dependencies have not arrived.

**Session guarantees**: mostly routing.

```
 read-your-writes    route to the leader for N seconds after a write,
                       or send a version token with the read
 monotonic reads     pin the client to one replica (hash the user id)
 monotonic writes    one write path per client, or sequence numbers
 consistent prefix   co-locate causally related data on one shard
```

**Eventual**: read the nearest replica, write anywhere, reconcile in the background — with anti-entropy
(replicas comparing and exchanging what they lack) and read-repair (fixing a stale replica when a read
notices).

### Tunable consistency, per query

Cassandra and DynamoDB let you choose per request, which makes the per-operation argument concrete:

```
 N = 3 replicas

 W=1, R=1   fastest; 1+1 = 2, NOT > 3   -> may read stale
 W=2, R=2   2+2 = 4 > 3                 -> strongly consistent, both slower
 W=3, R=1   fast reads, brittle writes  -> a single replica down blocks writes
 W=1, R=3   fast writes, slow reads
```

**`R + W > N` guarantees the read set and the write set overlap**, so at least one replica returns the
newest value. That is [day 117](../day-117-merge-k-sorted/README.md), and it is the dial people mean when
they say they "tuned consistency".

### What real systems offer

- **PostgreSQL / MySQL on one primary** — linearizable for writes; reads from replicas are eventually
  consistent unless you route them to the primary.
- **DynamoDB** — eventually consistent reads by default, strongly consistent reads on request at **twice
  the capacity cost** and higher latency. The trade, priced per request.
- **Cassandra** — tunable per query, from ONE to QUORUM to ALL, plus **lightweight transactions** using
  Paxos when you genuinely need linearizability for one key.
- **MongoDB** — read and write concerns per operation, plus **causally consistent sessions**, which is one
  of the clearest implementations of that rung.
- **Spanner** — externally consistent, which is linearizability plus a real-time ordering guarantee across
  the whole database, bought with **TrueTime** and a commit-wait of a few milliseconds on every
  transaction.
- **Redis** — asynchronous replication, so a failover can lose recent writes: not linearizable, and the
  documentation says so.
- **Collaborative editors** (Google Docs, Figma) — CRDTs or operational transformation, because the
  requirement is that everyone converges to the same document and nobody's keystroke is lost, which is a
  merge problem rather than an ordering one.

### Measuring it

You cannot reason your way to correctness here, and the practice worth naming is **Jepsen**: run a real
cluster, partition it deliberately, record every operation, and check afterwards whether the history is
consistent with the model the vendor claims. **It has found violations in most major distributed
databases**, including several that advertised linearizability.

**"I would want to see the Jepsen report"** is a genuinely strong thing to say about any distributed store.

---

## 6. The numbers

### The cost of each rung

```
 model              typical read latency        availability during a partition
 ----------------   -------------------------   -------------------------------
 eventual           ~1 ms (nearest replica)     fully available
 session/monotonic  ~1 ms (pinned replica)      available
 causal             ~1-5 ms                     AVAILABLE — the strongest AP model
 linearizable       ~5-10 ms same region        minority side REFUSES
                    ~150 ms cross-region
```

```
 DynamoDB, per request:
   eventually consistent read   0.5 read capacity units
   strongly consistent read     1.0 units          -> 2x the cost
```

**A vendor charging double is the clearest statement of the trade there is.**

### Staleness in practice

```
 same datacentre, healthy         1-50 ms behind
 same datacentre, heavy writes    100 ms - a few seconds
 cross-region                     200 ms+
 during a bulk load or migration  seconds to MINUTES
```

```
 P(a user hits a stale read) = P(they read within the lag window)

 a UI that reloads immediately after a write:
   read at ~50 ms after the write, replica lag ~200 ms
   -> stale ESSENTIALLY ALWAYS
```

**That is why read-your-writes is the anomaly users report**, and staleness in general is not: the read
that follows a write is not a random sample, it is the worst possible sample.

### What each fix costs

```
 read from the leader for 30 s after a write
   reads inside those windows          ~10-15% of a user's reads
   -> that much read load returns to the leader

 pin a client to one replica
   load spread between busiest and quietest    2-3x
   -> ~30% wasted capacity

 causal consistency with version vectors
   metadata per write                  one counter per replica
   -> at 5 replicas, ~40 bytes per record; at 100, it stops being free

 quorum reads (R=2, W=2, N=3)
   latency: the SECOND-slowest replica, not the fastest
   -> typically 2-3x the single-replica read latency
```

### The convergence window

```
 anti-entropy interval          typically seconds to minutes
 read-repair                    on the next read of that key
 hinted handoff replay          when the failed node returns

 so "eventually" in practice:
   milliseconds, if the key is read often
   minutes,      if it is not
   never,        if the replicas never exchange and no read touches it
```

**"Eventually" has no bound in the model and a practical distribution in reality** — and a key that is
written and never read may stay divergent for a very long time.

---

## 7. The trade-offs

### Strong consistency costs latency always and availability sometimes

**Always**, because a linearizable read must consult more than one machine — the "else" branch of
[PACELC](../day-114-heapify/README.md). **Sometimes**, because during a partition the minority must
refuse.

**I would not use strong consistency for a read that a user cannot verify.** Nobody can tell whether a
like count is two seconds old, and paying quorum latency for it on every request is buying a guarantee no
one will ever observe.

### Eventual consistency's cost is not staleness, it is the conflict problem

Staleness is usually invisible. What is not invisible is **what happens when two replicas disagree**, and
"eventual" says nothing about that. You must choose:

- **Last-write-wins** — silently discards data, and with clock skew may keep the *older* write.
- **Version vectors** — correct detection, and the application must then have a resolution rule.
- **CRDTs** — no conflicts by construction, and you can only store what they can express.
- **Application merge** — Amazon's cart union: over-keep rather than lose.

**Choosing "eventual" without choosing one of those is not a design.**

### Causal is the underrated middle

**It prevents the anomalies users actually complain about** — effect before cause — and it remains
available during a partition, so it is the strongest model that does not force a CAP choice.

Its cost is **metadata**: a version vector per write, which grows with the number of replicas, and a
replica that must hold back writes whose dependencies have not arrived.

**I would reach for causal (or the session guarantees) far more often than for linearizable**, and saying
that is a considered position rather than a default.

### Session guarantees are the cheapest real win

Read-your-writes and monotonic reads cost a routing rule, and between them they remove the two complaints
that generate support tickets. **They are the highest ratio of user-visible improvement to engineering
cost anywhere in this phase.**

### Where the reasoning breaks down

- **Claiming a model without testing it.** Jepsen has found violations in most major systems, including
  ones that advertised linearizability. The correct posture is scepticism.
- **"Eventually" with no bound.** A key that is written and never read can stay divergent indefinitely,
  and anti-entropy intervals of minutes are normal.
- **Mixing models within one user action.** If checkout reads inventory from a replica and writes the
  order to the leader, the guarantee of the whole action is the weakest link.
- **Assuming a transaction gives you distributed consistency.** ACID's C is about integrity constraints
  within one database. It says nothing about several machines.

---

## 8. In the interview

### How it gets asked

- The direct one: *"What consistency does this feature need? Justify it."*
- The ladder question: *"What is the difference between strong and eventual consistency?"*
- The one that separates people: *"Is there anything in between?"*
- The applied one: *"A user posts a comment and cannot see it. Which guarantee is missing?"*
- The sceptical one: *"How would you know your database actually provides what it claims?"*

### What to say out loud, in the first ninety seconds

1. **Reject the binary.** "Consistency is not strong-or-eventual — it is a ladder, and the useful rungs
   are in the middle."
2. **Define the top precisely.** "Linearizable means the system behaves as if there were one copy: every
   read sees the latest completed write, in real time. That is what a single machine gives you free and
   what a distributed system pays for."
3. **Define the bottom precisely, including what it does not promise.** "Eventual means: if writes stop,
   the replicas converge. It promises nothing about when, and nothing about what you see meanwhile — a
   read can even return something older than one you already saw."
4. **Name the middle, and why it matters.** "In between is **causal** — anything that could have influenced
   anything else is seen in that order — and the **session guarantees**: read-your-writes, monotonic reads,
   monotonic writes, consistent prefix. Causal is the strongest model that is still available during a
   partition."
5. **Make it per operation.** "And it is chosen per operation. In one system: seat booking is
   linearizable, a chat thread is causal, and a like count is eventual."
6. **Choose by the anomaly.** "The question I actually ask is: what would a user notice, and how bad is
   it? 'I posted and cannot see it' is read-your-writes and I fix it. 'The count is off by one for two
   seconds' is eventual and I leave it."

### The follow-ups

**"Is there anything in between strong and eventual?"**
"Yes, and it is where most real design happens. The rung that matters most is **causal consistency**: if
one operation could have influenced another, everyone sees them in that order; operations that could not
have influenced each other may be seen in any order. That is what prevents the anomalies users actually
complain about — a reply appearing above the message it replies to, a comment before the post. And the
crucial property is that **causal consistency remains available during a partition**, which linearizability
does not — so it is the strongest model that does not force a CAP choice. Below it are the four **session
guarantees**, which are per-client and very cheap: read-your-writes, monotonic reads, monotonic writes and
consistent prefix. Those four cover almost everything a user would report, and they cost routing rules
rather than quorums."

**"A user posts a comment and cannot see it. Which guarantee is missing?"**
"**Read-your-writes**, and it is the most-reported anomaly in this whole area — because the read that
follows a write is not a random sample, it is the worst possible one. The write went to the leader; the
read went to a replica a few hundred milliseconds behind; and the interface reloads immediately, so it
lands squarely inside the lag window essentially every time. Three fixes, in increasing precision.
**Route that user's reads to the leader for a window after they write** — thirty seconds, simple, and it
costs maybe ten to fifteen percent of the read load coming back to the leader. **Object-based routing** —
only reads of things they recently touched, which is a few percent. Or a **version token**: the write
returns the leader's log position, the client sends it back with reads, and a replica that has not reached
it either waits or forwards. And I would mention its sibling: **monotonic reads**, where the comment
appears and then disappears because two consecutive reads hit replicas with different lag — that one looks
like data loss, and the fix is to pin the client to one replica."

**"What consistency does this feature need?"**
"That depends on what a user would notice and how bad it is, and I would go feature by feature rather than
declaring a system-wide policy. Anything where **two clients can race for the same thing** must be
linearizable — seat booking, taking the last item of stock, a lock, a leader election, a balance at the
moment of a transfer — because there the anomaly is not staleness, it is two people getting the same
thing, and no amount of eventual convergence undoes it. Anything with **causal structure** wants causal
consistency: chat threads, comments on posts, anything where B only makes sense given A. Anything a user
**does to their own data** needs at least read-your-writes. And anything the user **cannot verify** —
a like count, a recommendation list, a search index, an analytics figure — should be eventual, because
paying quorum latency for a guarantee nobody can observe is pure cost."

**"What exactly does eventual consistency promise?"**
"Very little, and it is worth being precise because people assume more. It promises **only that if writes
stop, all replicas will converge to the same value**. It does not say how long that takes. It does not
promise you see your own writes. It does not promise that two consecutive reads agree — you can read a
value and then read an older one. And 'eventually' has no bound in the model: in practice it is
milliseconds for a hot key that gets read-repaired constantly, minutes for a cold one that waits for an
anti-entropy pass, and indefinite for a key that is written once and never read. The other thing eventual
consistency does not give you is a **conflict resolution** strategy — and that is where the real work is.
Choosing 'eventual' without also choosing last-write-wins, version vectors, CRDTs or an application merge
is not a design, it is a gap. And I would note that last-write-wins silently loses data, and with clock
skew it can keep the older write."

**"How would you know your database actually provides what it claims?"**
"I would look for a **Jepsen** report, and I would be sceptical without one. Jepsen is the practice of
running a real cluster, deliberately partitioning it, recording every operation with its start and end
time, and then checking whether the resulting history is consistent with the model the vendor advertises.
It has found violations in most major distributed databases — including several that claimed
linearizability — which tells you two things: that these guarantees are genuinely hard to implement, and
that documentation is not evidence. The related point for my own systems is that **you cannot reason your
way to this**; the failures are timing-dependent and rare, so they need deliberate fault injection rather
than ordinary tests."

**"What about CRDTs?"**
"They change the question rather than answering it. A conflict-free replicated data type is a structure
whose merge is designed so that any two replicas that have seen the same set of updates end up identical
**regardless of the order the updates arrived in** — a counter that sums per-node counts, a grow-only set
that unions, an observed-remove set with tags. So conflicts become impossible by construction, not
resolved well after the fact, and you get strong eventual consistency without coordination. The price is
that **you can only store what a CRDT can express**, and the things they cannot express are exactly the
global invariants — a balance that must not go below zero cannot be a CRDT, because that constraint is
about the whole system and CRDTs deliberately have no global view. They are excellent for collaborative
editing, presence, counters and sets, and they are not a general replacement for a transactional store."

### A model answer

Asked: *what consistency does this feature need? Justify it.*

> "Before I answer for a feature, I want to reject the binary, because the useful part is the middle.
> Consistency is a **ladder**, not a switch.
>
> At the top is **linearizable**: the system behaves as if there were exactly one copy, and every read
> returns the most recently completed write — a **real-time** guarantee, so if I write, then telephone you,
> and you read, you must see my write. That is what one machine gives you free and what a distributed system
> pays for: a read must consult the leader or a quorum, which is five to ten milliseconds in a region and
> about a hundred and fifty across regions, and during a partition the minority side must refuse.
>
> At the bottom is **eventual**: if writes stop, the replicas converge. That is the entire promise. It does
> not say when, it does not promise I see my own writes, and it permits a read returning something older
> than one I already saw.
>
> In between are the rungs that matter. **Causal consistency** — anything that could have influenced
> anything else is seen in that order by everyone, while genuinely concurrent operations may be seen in
> either order. That prevents the anomalies users actually report: a reply above its message, a comment
> before its post. And critically it **remains available during a partition**, so it is the strongest model
> that does not force a CAP choice. Below that are the four **session guarantees** — read-your-writes,
> monotonic reads, monotonic writes, consistent prefix — which are per-client, cost routing rules rather
> than quorums, and cover almost everything a user would complain about.
>
> So my answer for a feature is chosen by asking **what would a user notice, and how bad is it?**
>
> If two clients can **race for the same thing** — a seat, the last item in stock, a lock, a balance at the
> moment of a transfer — it must be **linearizable**, because the anomaly is not staleness, it is two people
> getting the same thing, and convergence afterwards does not undo it.
>
> If the data has **causal structure** — a chat thread, comments on a post — **causal**, because effect
> before cause is a real bug and staleness is not.
>
> If a user is looking at **their own data just after changing it**, at least **read-your-writes**, which I
> would implement by routing their reads to the leader for thirty seconds afterwards.
>
> And if the user **cannot verify it** — a like count, recommendations, a search index, a dashboard —
> **eventual**, because paying quorum latency for a guarantee nobody can observe is pure cost.
>
> One thing I would add: choosing eventual is not finished until I have chosen a **conflict resolution**
> strategy. Last-write-wins silently loses data and, with clock skew, can keep the older write. Version
> vectors detect true concurrency and hand it to the application. CRDTs make conflicts impossible by
> construction, at the price of only storing what they can express. And I would want to see a **Jepsen**
> report before believing any vendor's claim about which rung they are on."

---

## 9. Recall card

- **Consistency is a LADDER, not a switch: linearizable → sequential → CAUSAL → session guarantees →
  eventual.** Going down buys **latency and availability** and costs **anomalies**. The question is never
  "how consistent can we be" but **"which anomaly can this feature tolerate?"**
- **Linearizable = as if there were ONE copy, in real time.** Needs the leader or a quorum (~5–10 ms in
  region, ~150 ms across) and **refuses on the minority side of a partition**. Required whenever **two
  clients can race for the same thing**: seats, stock, locks, balances, leader election.
- **Causal is the underrated middle: anything that could have influenced anything else is seen in that
  order — and it stays AVAILABLE during a partition**, so it is the strongest model that is still AP. It
  prevents the anomalies users actually report (a reply above its message); staleness is not one of them.
- **The four session guarantees, by the user's own words:** *"I posted it and it's not there"* =
  **read-your-writes** (route to the leader for ~30 s, ~10–15% of reads); *"it was there, now it's gone"* =
  **monotonic reads** (pin to one replica); *"my two edits applied backwards"* = **monotonic writes**;
  *"the reply is above the message"* = **consistent prefix** (a sharding problem). **Cheapest real win in
  the phase.**
- **Eventual promises ONLY convergence if writes stop** — not your own writes, not monotonic reads, and
  with **no bound** on "eventually". Choosing it is not a design until you choose a **conflict resolution**
  strategy: last-write-wins (**loses data**, and with clock skew keeps the *older* write) · version vectors
  · **CRDTs** (no conflicts by construction, but cannot express global invariants like "never below zero")
  · application merge. **DynamoDB charges 2× for a strongly consistent read**, and **Jepsen** has found
  violations in most major systems — documentation is not evidence.
