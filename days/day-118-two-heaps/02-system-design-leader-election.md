---
day: 118
track: system-design
title: "Leader election"
phase: "Distributed systems core"
status: written
---

# Day 118 · System Design — Leader election

**After today you can:** You can say why a system needs one leader and how it picks a new one.

**The interviewer asks it as:** *The leader crashed. How does the cluster choose the next one?*

---

## 1. What this is, and why they ask it

**Leader election** is how a group of machines agrees that exactly one of them is in charge, and how they
agree on a replacement when that one stops responding.

Three sentences. A leader exists to make coordination cheap: with one machine deciding, ordering is free
and there are no conflicts to resolve, which is why [replication](../day-104-tree-path-problems/README.md),
[sharding](../day-107-bst-operations/README.md) and every distributed lock are built on one. Electing a
replacement is hard for exactly the reason from [day 113](../day-113-the-heap/README.md) — **you cannot
distinguish a crashed leader from a slow one** — so every election starts with a **guess** made by a
timeout. And the entire body of machinery around it exists for one purpose: **being safe when that guess
is wrong**, because a wrong guess means two leaders, which is the worst failure in the subject.

They ask it because it is where several earlier threads meet: partial failure, timeouts, quorums,
fencing. The answer that lands is not the election algorithm — it is *"the election is the easy part; the
hard part is making sure the old leader cannot still be writing."*

---

## 2. The story

The four boats went out together from the same landing and had done for as long as anyone could remember,
and the rule was that one man decided where they fished that day.

It was not seniority. It was whoever had the radio set that worked, more or less, and by 2009 that was
Antony. He called the ground at about five in the morning, and the other three followed him out and stayed
within sight.

The reason for having one man decide was not politics. It was that the fish moved, and if the four boats
spread out and each guessed, they caught nothing. Four boats on the same shoal caught something. One
decision, followed by everybody, beat four good decisions.

The rule about what happened when Antony did not call was written on the wall of the landing shed, and it
had been rewritten twice.

The first version said: if you do not hear from him, go where you think best. That lasted one season. On
the mornings when his radio was down but he had gone out anyway, the four boats ended up in four places
and the day was wasted.

The second version said: if you do not hear from Antony by half past five, Selvaraj decides. That was
better and it failed on a specific morning in 2011, when Antony's radio was working but the aerial on
Selvaraj's boat was wet. Antony called at ten past five; Selvaraj did not hear it; at half past five
Selvaraj started calling the ground; and two boats followed Antony while two followed Selvaraj.

The third version, which was still on the wall, was longer and it had three parts.

**One.** Nobody decides alone. Before you call a ground, you must first raise the other boats and have at
least **three of the four** — including yourself — say they will follow you. Two boats cannot make a
decision, because two other boats might be making a different one.

**Two.** Every decision carries a **number**, counting up, and the man calling it says it. *"This is the
fourth call of the morning."* If you hear a call with a lower number than one you have already followed,
you ignore it — because it is somebody who has been out of contact and does not know yet.

**Three.** If you have agreed to follow somebody, you say so, and then **you do not agree to follow anybody
else for that call number**. One vote per number.

The old fisherman who had written it said the second part was the one that had taken him longest to think
of. He said the problem was never that they could not choose. The problem was that a man who had been
out of contact would come back on the radio still believing he was in charge, and sound completely
confident, because from where he sat nothing had changed.

The numbers meant nobody had to argue. You just checked whether his number was old.

---

## 3. The idea in plain English

The landing shed's third rule is Raft, essentially unchanged, and the fisherman's observation about the
confident man is the reason for all of it.

- One boat deciding is the **leader**, and the reason is coordination, not hierarchy.
- "By half past five" is the **election timeout** — the guess that the leader is gone.
- "Three of the four must agree" is a **quorum** — the majority from
  [day 117](../day-117-merge-k-sorted/README.md).
- The counting number is the **term** (or epoch), and ignoring lower numbers is **fencing**.
- "One vote per number" is what stops two leaders being elected in the same term.
- The confident man returning is **split-brain**, and the numbers are what make it harmless.

### Why have a leader at all

**Because coordination without one is expensive.** With a single decision-maker:

```
 ordering        the leader's sequence IS the order. Nothing to agree.
 conflicts       impossible: only one writer.
 correctness     invariants can be checked in one place.
 simplicity      no consensus on every operation, only on who leads.
```

**Compare with leaderless** — Dynamo, Cassandra — where every node accepts writes:

```
 + no election, no failover gap, no single bottleneck
 - conflicts are now YOUR problem: vector clocks, CRDTs, last-write-wins
 - no global ordering, so no transactions across keys
 - no place to enforce a uniqueness constraint
```

**The trade in one line: a leader turns a hard agreement problem into an easy one, in exchange for a
failover gap and a bottleneck.** Say that, because "why not leaderless?" is the follow-up.

### Where leaders appear

```
 database replication      one primary takes writes            (day 104)
 sharding                  one node owns each shard            (day 107)
 distributed locks         the lock holder is a leader of one
 job schedulers            one instance runs the cron, not all fifty
 stream processing         one consumer owns each partition
 cluster management        one controller reconciles state
```

**The scheduled-job case is the one people meet first**: deploy a nightly billing job to fifty machines and
it runs fifty times. **Leader election is the fix, and it is worth naming as the everyday version.**

### The three ways to elect one

**1 — Use a consensus protocol yourself.** Raft or Paxos, built into your system. Correct, and a
substantial amount of code.

**2 — Use a lock service.** ZooKeeper, etcd or Consul already run consensus; you ask them for a lock or a
key with a lease and whoever gets it is the leader. **This is what almost everybody does**, and it is the
right answer in an interview: *"I would not implement Raft; I would use etcd."*

**3 — A lease from a shared store.** A row in a database with an expiry, taken by a conditional write.
Simple, and correct **only if** the store itself is linearizable and you use fencing tokens.

### Raft's election, which is the fisherman's rule

**Terms.** Time is divided into numbered terms. Each term has at most one leader.

**The timeout.** Every follower has a **randomised** election timeout, typically 150–300 ms. If it hears
nothing from the leader in that time, it becomes a **candidate**, increments the term, votes for itself,
and asks the others for votes.

**The vote.** A node grants its vote if it has not already voted in that term **and** the candidate's log
is at least as up to date as its own. **One vote per term** — the fisherman's rule three.

**The majority.** A candidate becomes leader on receiving votes from a majority. **Two candidates cannot
both get a majority**, so at most one leader per term — which is the pigeonhole argument from
[day 117](../day-117-merge-k-sorted/README.md) doing safety work rather than consistency work.

**The randomisation matters.** If every follower timed out at the same instant, they would all become
candidates, split the vote, and nobody would win — then repeat. **A random timeout in a range makes one
node time out first almost always**, which is why elections usually complete in a single round.

### Fencing: the part that actually matters

**The election is the easy half.** The hard half is that the old leader may not know it has been replaced.

```
 the old leader was PAUSED, not dead
   a long garbage-collection pause
   the machine was swapping
   a network partition that has now healed

 -> it wakes up still believing it is the leader
 -> and it is CONFIDENT, because from its point of view nothing happened
```

**The defence is a monotonically increasing number** — a **fencing token**, a term, an epoch — attached to
every write:

```
 leader in term 5 writes:  "write X, term 5"
 a new leader is elected:  term 6
 the storage layer has seen term 6, so it REJECTS anything stamped term 5
```

**The storage layer does the enforcing**, not the leader. That is the crucial detail: you cannot trust a
node to know it has been deposed, so the thing being written to must refuse stale writes.

**The fisherman's numbers.** *"If you hear a call with a lower number than one you have already followed,
ignore it."*

The other defences, worth naming:

- **STONITH** — "shoot the other node in the head": the new leader forcibly disables the old one, by
  cutting power or revoking its storage lease, before accepting any write.
- **A quorum requirement for the leader itself**: a leader must be able to see a majority to act, so a
  partitioned old leader **stops on its own**.

### Leases, and why they need clocks carefully

A **lease** is leadership with an expiry: you are the leader until time `T` unless you renew.

```
 + the old leader stops BY ITSELF when the lease expires — no fencing needed
   in the common case
 - it depends on CLOCKS, and clocks drift and jump  (day 113)
```

**The safe pattern**: the leader treats its lease as expiring **earlier** than the grantor does, so there
is a gap in which nobody believes they are leader.

```
 grantor:  the lease is valid until T
 holder:   I will stop acting at T − delta

 delta must exceed the maximum clock skew plus the maximum message delay
```

**Get that backwards and you have two leaders during the gap**, which is why leases are not a substitute
for fencing tokens — they reduce how often you need them.

### The trade-off in the timeout

```
 short election timeout   fast failover, more FALSE elections
                          (a GC pause looks like a crash)
 long election timeout    fewer false elections, longer unavailability
```

```
 Raft's typical range     150-300 ms, randomised
 failover in practice     ~1 second, including client redirection
 ZooKeeper session        typically 5-30 seconds
```

**Every false election is a small outage**: the old leader stops, a new one starts, in-flight work is
retried, and caches are cold. **So the timeout is tuned by how often you can afford that**, and there is no
setting that avoids both problems — the same trade as
[health checks](../day-099-binary-trees-in-code/README.md).

---

## 4. The picture

The election, as a timeline.

```
 t=0     leader (term 5) is sending heartbeats every 50 ms
         ─────♥─────♥─────♥─────
 t=200   ** the leader stops responding **   (crashed? paused? partitioned?)

 t=200   followers stop hearing heartbeats
 t=380   follower B's RANDOM timeout fires first (180 ms)
           -> becomes a CANDIDATE
           -> term 5 → 6
           -> votes for itself, asks the others

 t=385   C votes for B  (has not voted in term 6, B's log is up to date)
 t=387   D votes for B
           -> B has 3 of 5: a MAJORITY

 t=390   B is leader for term 6, starts heartbeats
 t=400+  clients redirected

 ── the RANDOM timeout is what stops all four becoming candidates at once,
    splitting the vote, and having to repeat. One node almost always fires
    first.
```

The dangerous case, and what saves it:

```
 THE OLD LEADER WAS PAUSED, NOT DEAD

 A (term 5)   ──── 20-second GC pause ────────────►  wakes up
                                                     "I am the leader"
                                                     ...and it is CONFIDENT,
                                                     because from where it
                                                     sits, nothing happened

 meanwhile:   B elected leader in term 6, has been writing for 15 seconds

 A now sends:  "write X, term 5"
                              ▲
 THE STORAGE LAYER has already seen term 6, so it REJECTS this.

 ── the enforcement is at the STORAGE, not at the leader. You cannot trust
    a node to know it has been deposed.
```

The three defences, and what each one catches:

```
 FENCING TOKEN        every write carries a monotonically increasing term;
   (term / epoch)     the storage rejects anything stamped older
                      -> catches the paused leader that woke up

 QUORUM REQUIREMENT   a leader may only act while it can see a majority
                      -> a partitioned old leader STOPS ON ITS OWN
                      -> and it is why cluster sizes are ODD

 STONITH / FENCING    the new leader forcibly disables the old one before
   the node           accepting a single write
                      -> catches everything, and needs infrastructure
                         (power control, storage lease revocation)
```

The fisherman's three rules, mapped:

```
 "three of the four must agree"      -> a MAJORITY QUORUM
                                        two candidates cannot both get one,
                                        so at most one leader per number

 "every call carries a number, and   -> TERMS and FENCING
  you ignore a lower one"               the confident man's calls are
                                        recognised as stale without argument

 "one vote per number"               -> a node votes at most once per term
                                        which is what makes the majority
                                        argument work at all
```

Leases and the safety gap:

```
 grantor's view:  |─────────── lease valid until T ───────────|
 holder's view:   |──── I stop acting at T − delta ────|
                                                        ▲
                                                        the SAFETY GAP:
                                                        nobody believes
                                                        they are leader

 delta must exceed  (max clock skew) + (max message delay)

 GET IT BACKWARDS — the holder thinking the lease lasts LONGER than the
 grantor does — and there is a window with TWO leaders.
```

---

## 5. How it actually works

### Doing it with etcd or ZooKeeper — the practical answer

**Nobody implements Raft for an application.** They use something that already has it.

```
 etcd:      put a key with a LEASE, using a compare-and-swap that only
            succeeds if the key does not exist
            -> the winner is the leader
            -> it must KEEP RENEWING the lease (a keepalive)
            -> if it stops, the key expires and someone else wins

 ZooKeeper: create an EPHEMERAL SEQUENTIAL node
            -> the lowest sequence number is the leader
            -> "ephemeral" means it disappears when the session ends
            -> each node watches only the one immediately below it
               (which avoids the herd effect of everyone watching the leader)
```

**The ZooKeeper detail is worth knowing**: if all `n` followers watch the leader's node, its disappearance
wakes all of them at once — a **herd**. Watching only your immediate predecessor means one node wakes.

### And the fencing token comes from the same place

```
 etcd:      the lease's revision number increases monotonically
 ZooKeeper: the znode's zxid, or the sequence number

 -> pass it with every write, and have the storage reject older ones
```

**A lock without a fencing token is not safe**, and this is the single most useful practical takeaway: any
lock service can hand you a lock and then have you pause for thirty seconds, and only the token protects
what you do next.

### What a leader actually does differently

```
 all writes go to it              -> ordering is free
 it assigns sequence numbers      -> replicas apply in the same order
 it holds the authoritative state -> reads from it are current
 it sends heartbeats              -> so followers know it is alive
```

**And the corollary**: the leader is a **bottleneck** for writes and a **single point of failure** for the
failover window. Both are accepted deliberately in exchange for cheap coordination.

### The client's problem, which people forget

Electing a leader is useless if clients keep talking to the old one.

```
 discovery options:
   ask any node, and be redirected                 (Raft's usual answer)
   look it up in the same lock service             (an extra dependency)
   a proxy in front that knows the current leader   (an extra hop)
   DNS                                              -> bounded below by the TTL
```

**The DNS option is the trap** — a 60-second TTL means a 60-second failover no matter how fast the
election was, which is the same
[day 104](../day-104-tree-path-problems/README.md) point.

### What real systems do

- **Raft** is the default modern answer because it was explicitly designed to be understandable, and it is
  what **etcd**, **Consul**, **CockroachDB**, **TiDB** and **RethinkDB** use.
- **Paxos** is older, harder to describe, and underpins **Chubby** (Google's lock service) and
  **Spanner**.
- **ZooKeeper** uses **ZAB**, which is Paxos-like, and is the classic answer for Hadoop-era systems and
  for **Kafka** before KRaft.
- **Kafka** historically used ZooKeeper for controller election and now uses its own Raft implementation
  (**KRaft**) — a good example of a system that outgrew an external dependency.
- **Kubernetes** elects a leader per controller using a **lease object in etcd**, which is exactly the
  lock-service pattern.
- **Redis Sentinel** does leader election for failover, and Redis's own documentation is candid that
  Redis replication is asynchronous, so a failover can lose writes.

---

## 6. The numbers

### Election timing

```
 heartbeat interval          50 ms
 election timeout (random)   150-300 ms
 detection                   150-300 ms after the last heartbeat
 election round              1-2 round trips  ->  ~5-20 ms in a datacentre
 becoming leader             ~200-350 ms total
 + client redirection        ~100 ms to several seconds
 --------------------------------------------------------------
 practical failover          ~1 second, and DNS-based can be MINUTES
```

**The election itself is fast. The client redirection is usually the slow part**, which is why the proxy
or virtual-IP approach beats DNS.

### The timeout trade

```
 election timeout   detection   false elections
 ----------------   ---------   -------------------------------------------
 50 ms              fast        frequent — a 100 ms GC pause triggers one
 150-300 ms         ~0.3 s      rare, and this is Raft's default range
 5 s                slow        essentially never
 30 s (ZooKeeper
   session default) very slow   never, but 30 s of unavailability
```

```
 a false election costs:
   the old leader stops accepting writes
   in-flight requests fail and are retried
   caches on the new leader are cold
   -> typically 1-5 seconds of degraded service, for nothing
```

**So the timeout is tuned by how often you can afford a small unnecessary outage**, which is exactly the
health-check trade from [day 099](../day-099-binary-trees-in-code/README.md).

### Cluster size

```
 nodes   majority   tolerates   election messages (a round)
 -----   --------   ---------   --------------------------
 3          2           1                 2
 5          3           2                 4
 7          4           3                 6
 9          5           4                 8
```

**Odd numbers only.** Four nodes tolerate the same single failure as three, and a 2-2 split leaves nobody
with a majority so the cluster stops entirely.

**And bigger is not better**: more nodes means more messages per decision, so **latency rises with cluster
size**. Three or five is almost always right, and etcd's own guidance is to stay at five or below.

### The GC pause problem, quantified

```
 a JVM full GC on a large heap      100 ms - several SECONDS
 a Raft election timeout            150-300 ms

 -> a full GC longer than the timeout looks EXACTLY like a crash
 -> the node is deposed, wakes up, and believes it is still leader
 -> WITHOUT fencing, it writes with stale authority
```

**This is not theoretical** — it is the most commonly reported cause of split-brain in production, and it
is why fencing tokens exist rather than being an optional refinement.

### Lease safety margin

```
 lease duration              10 s
 max clock skew (NTP)        ~50 ms
 max message delay           ~200 ms
 safety margin (delta)       ≥ 250 ms, and in practice 1-2 s

 holder stops acting at      T − 2 s
 grantor considers expired   T
 -> a 2-second window in which NOBODY is leader
 -> which is the price of never having TWO
```

### The leader as a bottleneck

```
 all writes through one node
   a relational leader     ~5,000 writes/s
   etcd                    ~10,000 writes/s (small keys, fsync-bound)

 -> when the write rate exceeds one machine, a single leader is the ceiling
 -> the answer is SHARDING: one leader PER SHARD, so leadership scales
    with the number of shards
```

**"One leader per shard" is the answer to "isn't the leader a bottleneck?"**, and it is what every large
system does.

---

## 7. The trade-offs

### A leader costs you a bottleneck and a gap

**All writes go through one machine**, so its capacity is the system's write ceiling, and there is a
window during every failover when nothing can be written.

**The mitigation is sharding** — one leader per shard — so leadership scales horizontally even though each
individual leader does not.

**I would not use a single leader** if the write rate exceeds one machine and the data does not partition
cleanly, or if writes must survive a whole-region failure without a gap — which pushes you towards
leaderless.

### Leader or leaderless?

**A leader** makes ordering free and conflicts impossible, at the cost of the gap and the bottleneck.

**Leaderless** (Dynamo, Cassandra) has no election, no failover gap, and no bottleneck — and it hands you
the conflict problem: vector clocks, CRDTs or last-write-wins, plus no global ordering and no way to
enforce a uniqueness constraint.

**Take a leader when you need ordering or invariants; take leaderless when you need availability and can
resolve conflicts.** That is the same CP/AP choice from [day 114](../day-114-heapify/README.md), arriving
from a different direction.

### Roll your own, or use etcd?

**Use etcd or ZooKeeper.** Implementing Raft correctly is months of work and the failure modes are subtle;
using a service that already does it is a configuration file.

**The cost is a new dependency in the critical path** — if etcd loses quorum, nothing can elect a leader,
which is why Kubernetes stops scheduling when etcd is unhealthy. **That is correct behaviour**, and worth
saying so, because it looks like a bug.

**I would build my own** only if the system is itself a database that cannot take a dependency, which is
why CockroachDB and Kafka eventually did.

### Fencing is not optional

**A lock without a fencing token is not a lock.** Any lock service can grant you leadership and then let
you pause for thirty seconds, and when you wake up the lock is somebody else's while you still believe it
is yours.

**The token has to be enforced by the resource being protected**, not by the holder — because the holder is
precisely the thing that cannot be trusted to know.

### Where it goes wrong

- **A GC pause longer than the election timeout.** The most common real cause of split-brain.
- **Clock-based leases without a safety margin**, or with the margin the wrong way round.
- **Even-numbered clusters**, which tolerate no more failures and stop entirely on an even split.
- **Client redirection through DNS**, where the TTL sets the floor on failover time.
- **Too many nodes**, where every decision needs more round trips and latency rises for no extra fault
  tolerance.
- **Forgetting that the leader is also a cache-warmth problem** — the new leader starts cold, so failover
  costs more than the election time suggests.

---

## 8. In the interview

### How it gets asked

- The direct one: *"The leader crashed. How does the cluster choose the next one?"*
- The dangerous one: *"What if the old leader comes back?"*
- The practical one: *"Would you implement Raft?"*
- The design one: *"I have fifty servers and a nightly job. How do I run it once?"*
- The limits one: *"Isn't the leader a bottleneck?"*

### What to say out loud, in the first ninety seconds

1. **Say why there is a leader at all.** "A leader makes coordination cheap: one writer means ordering is
   free and there are no conflicts. That is why replication, sharding and locks are all built on one."
2. **Start the election with the guess.** "Followers stop hearing heartbeats and, after a **randomised**
   timeout, one becomes a candidate, increments the term, and asks for votes. The randomisation is what
   stops everyone becoming a candidate at once and splitting the vote."
3. **State the safety property.** "A candidate needs a **majority**, and a node votes at most once per
   term — so two candidates cannot both win. At most one leader per term."
4. **Go straight to the hard part.** "The election is the easy half. The hard half is that the old leader
   may not know it was replaced — a long GC pause looks exactly like a crash, and the node wakes up
   confident."
5. **Name fencing and say where it is enforced.** "So every write carries a monotonically increasing term,
   and **the storage layer rejects anything stamped with an older one**. The enforcement has to be at the
   resource, not at the leader, because the leader is precisely what cannot be trusted."
6. **Say what you would actually build.** "And I would not implement Raft — I would take a lease from etcd
   or ZooKeeper, and use the revision number as the fencing token."

### The follow-ups

**"What if the old leader comes back?"**
"That is the failure the whole design exists to prevent, and the reason it happens is that a paused leader
is **indistinguishable from a crashed one**. A twenty-second garbage-collection pause, a machine swapping,
or a network partition that heals — from the node's own point of view nothing happened, so it wakes up
confident that it is still in charge and starts writing. Three defences and I would want at least two.
**Fencing tokens**: every write carries the term, and the storage rejects anything older than the highest
term it has seen — the crucial part being that the **storage** enforces it, because the leader cannot be
trusted to know it was deposed. **A quorum requirement for the leader itself**: it may only act while it
can see a majority, so a partitioned old leader stops on its own — which is also why cluster sizes are odd.
And **STONITH**, where the new leader forcibly disables the old one, by cutting power or revoking its
storage lease, before accepting a single write. Without any of these you get two leaders writing
simultaneously, and that data cannot be automatically reconciled."

**"Would you implement Raft?"**
"No, and I would say so directly. Implementing consensus correctly is months of work and the failure modes
are subtle enough that most hand-rolled implementations are wrong in ways that only appear under
partition. I would take a lease from **etcd** or **ZooKeeper**, which already run consensus: in etcd, put
a key with a lease using a compare-and-swap that only succeeds if the key is absent, keep renewing it, and
whoever holds it is the leader. In ZooKeeper, create an ephemeral sequential node and the lowest sequence
number wins — and each node watches only the one immediately below it, which avoids waking every node at
once when the leader disappears. Crucially, both give me a **monotonically increasing number** — etcd's
revision, ZooKeeper's zxid — which I use as the fencing token. The cost of that choice is a new dependency
on the critical path: if etcd loses quorum, nothing can elect a leader, which is exactly why Kubernetes
stops scheduling when etcd is unhealthy. That is correct behaviour rather than a bug. I would build my own
only if the system were itself a database that cannot take an external dependency, which is why
CockroachDB and Kafka eventually did."

**"I have fifty servers and a nightly job. How do I run it once?"**
"That is leader election in its most everyday form, and the failure without it is that the job runs fifty
times — fifty billing runs, fifty emails to every customer. The simplest correct answer is a **lease**:
each instance tries to acquire a named lock in etcd, Redis or a database row with a compare-and-set, and
only the winner runs the job. Three things I would get right. The lease must have an **expiry**, so a
crashed holder does not block the job forever. The holder must **renew** it while the job runs, or a long
job outlives its own lease and a second instance starts. And the job itself should be **idempotent** where
possible, because if the lease does expire mid-run — a GC pause, again — two instances may overlap, and
that is far cheaper to survive than to prevent. If the job is long, I would also make it **resumable** and
checkpoint its progress, so an overlap costs duplicated work rather than duplicated side effects."

**"Isn't the leader a bottleneck?"**
"Yes, in two ways, and both are accepted deliberately. **Throughput**: every write goes through one
machine, so its capacity is the system's write ceiling — a relational leader is around five thousand writes
a second and etcd around ten thousand for small keys. **Availability**: there is a window during every
failover when nothing can be written, typically around a second including client redirection. The standard
answer to the throughput problem is **sharding**: one leader per shard, so leadership scales with the
number of shards even though each individual leader does not. That is what every large system does — Kafka
elects a leader per partition, and a sharded database elects one per shard. The alternative is going
**leaderless**, which removes the election and the bottleneck and hands you conflict resolution instead:
vector clocks or CRDTs, no global ordering, and no way to enforce a uniqueness constraint. That is the
same CP-versus-AP choice arriving from a different direction."

**"How long is the failover, and what sets it?"**
"The election itself is fast: heartbeats every fifty milliseconds, a randomised election timeout of a
hundred and fifty to three hundred, then one or two round trips to collect votes — so a new leader exists
within about a third of a second. **The slow part is almost always telling the clients.** If they discover
the leader through DNS with a sixty-second TTL, the failover is sixty seconds regardless of how fast the
election was — which is why production systems use a proxy or a virtual IP, or have clients ask any node
and be redirected. There is also a cost the timing does not show: the new leader starts with **cold
caches**, so the first minute after a failover is slower even once everything is technically working. And
the timeout itself is a trade — shorter means faster detection and more **false** elections, and every
false election is a small outage in which the old leader stops, in-flight work is retried and caches go
cold. A GC pause longer than the timeout triggers one, which is exactly the case that then needs fencing."

**"Why is the election timeout randomised?"**
"To avoid a **split vote**. If every follower used the same timeout, they would all stop hearing heartbeats
at the same moment, all become candidates at the same instant, all vote for themselves, and none would
reach a majority — and then they would all time out again together and repeat, potentially for a long time.
Randomising the timeout over a range, typically a hundred and fifty to three hundred milliseconds, means
one node almost always fires meaningfully earlier than the others, wins the votes before anyone else even
becomes a candidate, and the election completes in a single round. It is a very small design decision that
makes the difference between elections that reliably converge and elections that can livelock, and it is
one of the reasons Raft is easier to reason about than the alternatives."

### A model answer

Asked: *the leader crashed. How does the cluster choose the next one?*

> "Let me answer in two halves, because the second one is where the difficulty is.
>
> **The election.** Followers expect heartbeats from the leader — say every fifty milliseconds. If a
> follower hears nothing for its **election timeout**, which is randomised between roughly a hundred and
> fifty and three hundred milliseconds, it becomes a **candidate**: it increments the **term** number,
> votes for itself, and asks the other nodes for their votes. A node grants its vote if it has not already
> voted in that term and the candidate's log is at least as up to date as its own. A candidate that
> receives votes from a **majority** becomes the leader for that term.
>
> Two details in that carry the safety. **A majority is required**, and a node votes at most once per term
> — so two candidates cannot both win, and there is at most one leader per term. That is the pigeonhole
> argument again. And the **timeout is randomised**, because if every follower timed out simultaneously
> they would all become candidates, split the vote, and have to repeat — randomising means one node almost
> always fires first and the election finishes in one round.
>
> That whole process takes about a third of a second. **The slow part is usually telling the clients** — if
> they find the leader through DNS with a sixty-second TTL, the failover is sixty seconds however fast the
> election was.
>
> **Now the hard half.** The election assumed the old leader was dead, and that was a **guess** — a timeout
> cannot distinguish a crashed node from a slow one. A twenty-second garbage-collection pause looks exactly
> like a crash, and the node wakes up **still believing it is the leader** and completely confident, because
> from where it sits nothing happened. That is split-brain, and two leaders writing simultaneously produces
> data that cannot be automatically reconciled.
>
> So: **fencing**. Every write carries the term number, and the storage layer rejects anything stamped with
> a term older than the highest it has seen. The essential detail is that **the storage enforces it, not the
> leader** — because the leader is precisely the thing that cannot be trusted to know it has been deposed.
> On top of that I would require a leader to be able to see a **majority** in order to act at all, so a
> partitioned old leader stops on its own; and where the infrastructure allows it, have the new leader
> forcibly fence the old one before accepting a single write.
>
> And in practice I would not implement any of this. I would take a lease from **etcd** — a compare-and-set
> on a key with an expiry, renewed by the holder — and use etcd's revision number as the fencing token. The
> honest cost is a dependency on the critical path: if etcd loses quorum, no leader can be elected, which is
> exactly why Kubernetes stops scheduling when etcd is unhealthy."

---

## 9. Recall card

- **A leader exists to make coordination cheap: one writer means ordering is free and conflicts are
  impossible.** That is why replication, sharding, locks and schedulers are built on one. The everyday case
  is a **nightly job on 50 machines running 50 times**.
- **The election: heartbeats stop → a RANDOMISED timeout (150–300 ms) fires → a candidate increments the
  TERM, votes for itself, and needs a MAJORITY.** One vote per term, so two candidates cannot both win —
  at most one leader per term. **Randomisation prevents split votes** and makes elections finish in one
  round.
- **The election is the EASY half. The hard half: a paused leader is indistinguishable from a crashed one**
  — a GC pause longer than the timeout is the most common real cause of split-brain — **and it wakes up
  confident.**
- **FENCING is the answer, and the STORAGE must enforce it, not the leader**: every write carries a
  monotonically increasing term/epoch, and anything older is rejected. Plus a **quorum requirement** so a
  partitioned leader stops on its own (hence **odd** cluster sizes), and **STONITH** where available.
  **A lock without a fencing token is not a lock.**
- **Do not implement Raft — take a lease from etcd or ZooKeeper** (ephemeral sequential nodes, each
  watching only its predecessor to avoid a herd) and **use their revision/zxid as the token**. The cost is a
  critical-path dependency — Kubernetes stopping when etcd loses quorum is correct, not a bug. And the
  leader is a **write bottleneck**, answered by **one leader per shard**; **client redirection, not the
  election, usually dominates failover time.**
