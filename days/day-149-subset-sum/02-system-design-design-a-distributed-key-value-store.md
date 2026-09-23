---
day: 149
track: system-design
title: "Design a distributed key-value store"
phase: "High-level design case studies"
status: written
---

# Design a distributed key-value store

## 1. What this is, and why they ask it

A key-value store does two things: `put(key, value)` and `get(key)`. That is the whole interface.

**Designing one across a thousand machines is the hardest thing in this course**, and it is asked constantly,
because it is the one design where every distributed-systems idea has to be present at once and none of them
can be waved at. Partitioning, replication, consistency, failure detection, conflict resolution, and
membership — all of them, in one system, interacting.

They ask it because **it has no diagram to memorise**. "Design Twitter" has a shape you can recognise. This
has decisions, and each one has a defensible answer in both directions, so the interviewer can push on any of
them and see whether you understood or recited.

And they ask it because the reference design is public and famous. **Amazon's Dynamo paper is the single most
influential systems paper of the last twenty years** — Cassandra, Riak, Voldemort and DynamoDB all descend
from it — so the interviewer usually has a specific set of mechanisms in mind: consistent hashing, `N`, `R`
and `W` quorums, vector clocks, hinted handoff, Merkle trees, gossip. **Naming them is expected.**

By the end of this lesson you can partition with consistent hashing and virtual nodes, replicate with a
tunable quorum, state the consistency guarantee precisely, resolve conflicts, handle node failure and repair,
and size the whole thing.

---

## 2. The story

The lending library was Sushila's idea and by the third year it had outgrown her flat entirely.

It had started as a shelf. Then two shelves. Then the whole of one wall, and then a woman on the fourth floor
offered to keep some, and after that it was in six flats across three buildings and about eleven hundred
books.

**And the moment it left one room, the problem changed completely.**

Because when it was a shelf, everything was simple. You wanted a book, you looked. It was there or it was not.

Now, you wanted a book, and the first question was **which flat**.

Sushila's answer was the alphabet. A to E in her flat, F to K on the fourth floor, and so on. It worked
beautifully and it worked for about four months, until somebody pointed out that she had four hundred books
and the woman with T to Z had sixty-one. **The letters are not evenly spread and nobody had thought about it.**

Then the second problem, which was worse. **The fourth-floor family went to Pune for a month and locked the
flat.** Two hundred books, gone, not lost but unreachable, and there was no way to know which two hundred until
somebody wanted one.

So they started keeping **two copies of the popular ones, in two different flats.** Which solved the locked
door and created the thing that took a year to get right.

Because a woman on the second floor borrowed one copy, and wrote her name in the register in that flat. And
somebody else borrowed the other copy from the other flat, and wrote *their* name in *that* register. **And
both registers were correct. They just did not agree.**

Nobody had done anything wrong. There was no lying and no mistake. There were two books and two registers and
one title, and when the two registers were finally compared, in March, **there was no way at all to work out
which entry had come first**, because neither register recorded the time and the two clocks in question were
two different people's memories.

**Sushila's rule, when she finally made one, was not about preventing it.** It was that when the registers
disagreed, both names got kept, and whoever collected the books went and asked.

---

## 3. The idea in plain English

Sushila built Dynamo. Badly, over three years, in the order the problems arrived — which is the order they
arrive in every distributed store.

**Start with the interface, because it is small and that is the point.**

```
put(key, value)     -> stored
get(key)            -> value
delete(key)
```

**No joins, no transactions across keys, no queries by value, no ordering.** That poverty is what buys the
scale: a store that cannot ask "all users in Delhi" never needs to talk to more than a handful of machines for
any one request.

**Problem one: which machine holds this key?**

The obvious answer is `hash(key) % number_of_machines`. **And it is catastrophic**, because adding one machine
changes the modulus and therefore changes the answer for almost every key. Going from 10 machines to 11
remaps roughly **91% of all keys** — every one of which then has to move.

**Consistent hashing fixes that.** Imagine the hash output as a circle, `0` to `2^128`. Every machine is placed
at a point on the circle, by hashing its name. Every key is placed on the circle too, by hashing the key.
**A key belongs to the first machine you meet going clockwise from where the key landed.**

**Now adding a machine moves only the keys between it and its predecessor** — roughly `1/n` of the data, not
91% of it. That is the entire idea, and it is the one thing to be able to draw.

**But raw consistent hashing is uneven**, exactly like Sushila's alphabet. Hash ten machine names onto a
circle and the arcs between them will not be equal; one machine ends up with three times the data of another.

**Virtual nodes fix that.** Each physical machine is placed on the circle **many times** — 100 to 256 positions
each, by hashing `machine-1#0`, `machine-1#1`, and so on. With a thousand points instead of ten, the arcs
average out and every machine gets close to its fair share. **And when a machine dies, its hundreds of small
arcs are inherited by many different machines rather than all landing on one neighbour**, which is the second,
less obvious benefit.

**Problem two: a machine will die, so keep copies.**

**Replication factor `N`**, usually 3. A key is stored on the machine that owns it plus the next `N - 1`
distinct physical machines clockwise. That list is the key's **preference list**.

**And it must skip virtual nodes belonging to a machine already in the list**, or three replicas can land on
one machine and the whole point is lost. **In practice it also skips racks and availability zones**, so a
single rack losing power does not take all three copies.

**Problem three: how many replicas must answer?**

This is the tunable part, and it is what the interview is usually about.

```
N = how many copies exist
W = how many must acknowledge a write before it is called successful
R = how many must respond to a read before you answer
```

**If `R + W > N`, the read set and the write set must overlap in at least one machine**, so at least one
machine that answers the read has the newest write. **That is a strong-consistency quorum**, and it is a
counting argument, not a protocol — worth saying exactly that way.

```
N=3, W=2, R=2    R + W = 4 > 3    overlap guaranteed. The default.
N=3, W=3, R=1    fast reads, and a single slow node blocks every write.
N=3, W=1, R=1    fastest possible, and R + W = 2 < 3: you can read stale.
```

**`W = 1` is not a mistake** — it is the right choice when writes must never block and staleness is
acceptable, and being able to say when that is true is the answer they want.

**Problem four: two writes to the same key, and no agreed time.**

This is Sushila's two registers, and [day 123](../day-123-word-search-ii/README.md) explains why it cannot be
solved with timestamps: **there is no global clock, and the two machines' clocks can disagree by more than the
gap between the two writes.**

**Three answers, in increasing order of honesty.**

**Last-write-wins**, using wall-clock timestamps. Simple, and it silently discards a write whenever the clocks
are skewed. **Cassandra defaults to this**, and the data loss is real and invisible.

**Vector clocks.** Each value carries a small map of `machine -> counter`. When machine A writes, it increments
its own counter. Comparing two vectors gives one of three results: **A is strictly newer, B is strictly newer,
or neither** — and "neither" means concurrent, which is exactly Sushila's case. **The store cannot decide, so
it keeps both** and returns both on the next read.

**Application-level merge**, which is what "keeps both" leads to. The classic example is Amazon's shopping
cart: two concurrent adds produce two carts, and the merge is **union of the items** — a customer sees an item
they thought they removed, which is annoying, and never loses an item they added, which matters more.

**Sushila's rule — keep both names and go and ask — is exactly this**, and it is the honest design.

**Problem five: a node is down. Now what?**

**Hinted handoff.** If a replica is unreachable, write to the next healthy machine clockwise, tagged with a
hint saying who it was really for. When the real owner returns, the hint is delivered and the temporary copy
deleted. **This keeps writes available during a failure** and is why Dynamo-style stores are described as
always-writeable.

**Anti-entropy with Merkle trees**, for the divergence hinted handoff misses. Each replica builds a hash tree
over its key range. Two replicas compare root hashes — **equal means identical, one comparison for a million
keys.** Unequal, and they descend into the differing subtree only. **Logarithmic repair instead of a full
scan**, and that saving is the reason the structure is used.

**Read repair**, the cheap one: when a read finds replicas disagreeing, write the newest value back to the
stale ones. **Free, because the read already fetched everything**, and it fixes the keys people actually
read.

**Gossip for membership.** No central registry. Each node periodically picks a random peer and exchanges what
it knows about who is alive. **Information spreads in `O(log n)` rounds** and there is no coordinator to lose.
[Day 124](../day-124-tries-revision/README.md)'s failure detection is what each node runs locally; gossip is
how the conclusions travel.

---

## 4. The picture

The hash ring, with virtual nodes:

```
                        0 / 2^128
                            |
              B3 -----------+----------- A1
             /                            \
           C2                              C1
           |         key "user:42"          |
           |         hashes to here  ---->  * 
           |                                |     first node clockwise = A2
           A3                              A2     -> A2 owns it
             \                            /
              C3 -----------+----------- B1
                            |
                           B2

  Three machines A, B, C, three virtual nodes each.
  In production: 128-256 virtual nodes per machine, so the arcs even out.
  Adding machine D inserts D1..D256 and moves only the keys in those arcs
  — about 1/4 of the data, not 91% of it.
```

Why plain modulo is unusable:

```
  hash(key) % 10   ->  machine 0..9
  add one machine
  hash(key) % 11   ->  machine 0..10

  a key with hash 1234:   1234 % 10 = 4      1234 % 11 = 2     MOVED
  a key with hash 5678:   5678 % 10 = 8      5678 % 11 = 5     MOVED
  a key with hash 1000:   1000 % 10 = 0      1000 % 11 = 10    MOVED

  ~91% of all keys move. Every one is a network transfer.
  Consistent hashing: ~9% move. That is the whole reason it exists.
```

The preference list and a quorum write:

```
  key "cart:99" hashes into A's arc.
  preference list, N=3:  [A, B, C]   (next 3 DISTINCT physical machines)

  put("cart:99", v2), W=2:

     coordinator (any node) -> A  ... ack
                            -> B  ... ack     <- 2 acks, W satisfied
                            -> C  ... slow / down
     return SUCCESS to the client immediately.

  C is repaired later by read repair or anti-entropy.
  If C is DOWN, the write goes to D with a hint "this belongs to C".
```

The quorum overlap argument, drawn:

```
  N = 3 replicas:        [ A ][ B ][ C ]

  W = 2 -> a write is on at least 2 of them:   [ A ][ B ]
  R = 2 -> a read asks at least 2 of them:          [ B ][ C ]
                                                     ^
                          B is in both sets. It has the new value.

  R + W = 4 > 3  =>  the sets MUST share at least one machine.
                     Pure counting. There is no protocol here.

  R + W <= N  =>  they can be disjoint  =>  a stale read is possible.
```

Vector clocks producing a conflict:

```
  client writes v1 via node A        ->  value v1, clock {A:1}
  network partitions

  client X writes via A              ->  value v2, clock {A:2}
  client Y writes via B              ->  value v3, clock {A:1, B:1}

  partition heals. Compare {A:2} and {A:1, B:1}:

     is {A:2}     >= {A:1,B:1}?  A: 2>=1 yes.  B: 0>=1 NO.
     is {A:1,B:1} >= {A:2}?      A: 1>=2 NO.

  Neither dominates -> CONCURRENT -> keep BOTH.
  The next read returns [v2, v3] and the application merges them.

  This is the two registers. Neither is wrong; they disagree.
```

Merkle trees making repair cheap:

```
  replica A                        replica B
      root  H(abcd)                    root  H(abcX)
       /        \                       /        \
   H(ab)       H(cd)               H(ab)       H(cX)
    /  \        /  \                /  \        /  \
  H(a) H(b)  H(c) H(d)           H(a) H(b)  H(c) H(X)

  compare roots:      differ  -> descend
  compare H(ab):      EQUAL   -> skip this entire half, half a million keys
  compare H(cd):      differ  -> descend
  compare H(c):       equal   -> skip
  compare H(d)/H(X):  differ  -> transfer just this key

  1 differing key out of 1,000,000 found in ~20 comparisons.
  A full scan would be 1,000,000 comparisons and the whole dataset over
  the network.
```

---

## 5. How it actually works

### Consistent hashing with virtual nodes

```python
import bisect, hashlib

class Ring:
    def __init__(self, vnodes: int = 256) -> None:
        self.vnodes = vnodes
        self.points: list[int] = []          # sorted hash positions
        self.owner: dict[int, str] = {}      # position -> physical machine

    def _hash(self, s: str) -> int:
        return int(hashlib.md5(s.encode()).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        for i in range(self.vnodes):
            point = self._hash(f"{node}#{i}")
            bisect.insort(self.points, point)
            self.owner[point] = node
```

**`bisect.insort` keeps the positions sorted**, which is what makes lookup a binary search — the same
`bisect` from [day 038](../day-043-binary-search-without-bugs/README.md). The ring is just a sorted list of
integers.

Now the lookup, which is the whole point:

```python
    def preference_list(self, key: str, n: int) -> list[str]:
        """The n distinct physical machines that should hold this key."""
        index = bisect.bisect(self.points, self._hash(key))
        result: list[str] = []
        for offset in range(len(self.points)):
            point = self.points[(index + offset) % len(self.points)]
            node = self.owner[point]
            if node not in result:           # skip vnodes of a machine already listed
                result.append(node)
            if len(result) == n:
                break
        return result
```

**`if node not in result` is the line that matters.** Without it, three consecutive virtual nodes belonging to
machine A give you three "replicas" all on machine A, and the replication factor is a lie. **In production the
same check also excludes racks and availability zones.**

**`bisect.bisect` then wrapping with `% len` is the circle** — past the last point you come back to the first.

### The coordinator, and a quorum write

```python
def put(ring, key: str, value, n: int, w: int) -> bool:
    replicas = ring.preference_list(key, n)
    acks = 0
    for node in replicas:
        if send_write(node, key, value):     # fire in parallel in reality
            acks += 1
        if acks >= w:
            return True                      # do NOT wait for the rest
    return False
```

**Returning at `w` acks and not waiting for the rest is the latency win**, and it is the whole reason quorums
are tunable. With `N = 3, W = 2` you are waiting for the second-fastest of three replicas, **not the slowest**
— which removes the one slow machine from the critical path, and one machine in three being slow is normal.

**In reality the writes go out in parallel** and the coordinator waits on the first `w` responses.

### The quorum read, and read repair

```python
def get(ring, key: str, n: int, r: int) -> list:
    replicas = ring.preference_list(key, n)
    responses = [send_read(node, key) for node in replicas[:r]]
    versions = reconcile(responses)          # vector-clock comparison
    if len(versions) == 1:
        repair_stale(replicas, key, versions[0])   # read repair, in the background
    return versions                          # more than one = conflict, caller merges
```

**`get` returns a list, not a value**, and that is the API decision that follows from vector clocks. Most of
the time it has one element. When it has two, **the caller must merge**, and the API forces them to notice
rather than silently picking one.

**Read repair happens on the read path and costs nothing extra**, because the values were already fetched.

### Vector clocks

```python
def dominates(a: dict[str, int], b: dict[str, int]) -> bool:
    """True if a is strictly at least as new as b on every node."""
    return all(a.get(node, 0) >= count for node, count in b.items())

def reconcile(versions: list) -> list:
    keep = []
    for v in versions:
        if any(dominates(other.clock, v.clock) and other.clock != v.clock
               for other in versions):
            continue                         # superseded by a strictly newer version
        keep.append(v)
    return keep                              # >1 means genuinely concurrent
```

**`dominates` is the whole comparison** — every counter in `b` must be matched or exceeded in `a`. If neither
dominates the other, they are concurrent and both survive.

**Vector clocks grow**, one entry per node that has ever written the key, so production systems truncate the
oldest entries past about ten. **Truncation can produce false conflicts** — two values that were actually
ordered look concurrent — which is safe, because a false conflict causes an unnecessary merge rather than lost
data.

### Hinted handoff

```python
def write_with_hint(ring, key, value, n, w):
    for node in ring.preference_list(key, n):
        if is_alive(node):
            send_write(node, key, value)
        else:
            fallback = next_healthy_after(ring, node)
            send_write(fallback, key, value, hint_for=node)   # hold it for them
```

**The fallback stores it in a separate hint area, not as its own data**, and hands it over when the real owner
returns. **Writes stay available through a node failure**, which is the guarantee Dynamo is built around.

**And it fails if the fallback also dies before delivering** — which is what anti-entropy is for.

### The real systems

```
DynamoDB (AWS)     managed, single-digit-ms, strong OR eventual reads per request
Cassandra          Dynamo partitioning + a wide-column model, tunable per query
Riak               the closest open-source Dynamo, vector clocks exposed
Voldemort          LinkedIn's; largely historical now
etcd / ZooKeeper   NOT this design — Raft, strongly consistent, small data,
                   for configuration and coordination, not for bulk storage
```

**Naming etcd as the counter-example is worth doing**, because it shows you know these are different tools for
different jobs rather than competitors.

### The storage engine on each node

```
writes -> in-memory memtable (sorted)
       -> also appended to a write-ahead log (crash recovery)
       -> when full, flushed to disk as an immutable SSTable
       -> SSTables compacted in the background

reads  -> memtable, then SSTables newest-first
       -> a BLOOM FILTER per SSTable answers "definitely not here" in
          one memory access, skipping the disk read entirely
```

**This is an LSM tree, and it is the standard choice** because writes become sequential appends rather than
random disk seeks. The Bloom filter is [day 143](../day-143-what-dp-is/README.md)'s, doing exactly the job it
was introduced for.

---

## 6. The numbers

**Sizing the cluster.**

```
1 billion keys
average value 1 KB
replication factor N = 3

raw data      1,000,000,000 x 1 KB          = 1 TB
replicated    1 TB x 3                      = 3 TB
+ overhead    indexes, Bloom filters, ~20%  = 3.6 TB
+ headroom    never run past ~60% full      = 6 TB provisioned
```

```
per machine: 2 TB of SSD usable
-> 6 TB / 2 TB = 3 machines minimum on storage

but availability wants 3 AZs and headroom for failure:
-> 12 machines, 4 per AZ, is the realistic floor
```

**Storage rarely sets the machine count. Throughput and failure tolerance do**, and saying that is worth more
than the division.

**Throughput.**

```
100,000 reads/s, 20,000 writes/s

each write with N=3 becomes 3 physical writes    = 60,000 disk writes/s
each read with R=2 becomes 2 physical reads      = 200,000 reads/s

per machine (SSD, LSM engine): ~20,000 ops/s sustained
-> (200,000 + 60,000) / 20,000 = 13 machines

matches the availability floor. 15 machines, comfortably.
```

**Latency, and where the quorum choice shows up.**

```
single replica read                     ~1 ms  (memory or SSD)
network round trip within an AZ         ~0.5 ms
network round trip across AZs           ~1-2 ms

R=1 : wait for 1 of 3       -> ~1.5 ms   fastest, can be stale
R=2 : wait for 2 of 3       -> ~2.5 ms   the second-fastest replica
R=3 : wait for all 3        -> ~8 ms     the SLOWEST replica, every time
```

**`R = 3` means the p99 of every read is the p99 of the worst of three machines**, which is dramatically worse
than the p99 of one. **That is the concrete argument for `R = 2`**, and it is a better answer than "quorums are
a good balance".

**The consistent hashing win, quantified.**

```
1 billion keys, 10 machines, growing to 11

modulo:              ~91% of keys move   = 910,000,000 keys
                     at 1 KB each        = 910 GB over the network
                     at 1 Gbps           = ~2 hours of saturated network,
                                           during which everything is slow

consistent hashing:  ~1/11 of keys move  = 91,000,000 keys
                     = 91 GB             = ~12 minutes

10x less data moved, and it is spread across all machines rather
than being one machine's problem.
```

**Virtual node balance.**

```
10 machines, 1 virtual node each:
  arcs are random; worst machine typically holds 2-3x the average.
  -> one machine at 300 GB while another holds 100 GB

10 machines, 256 virtual nodes each (2,560 points):
  the law of large numbers applies
  -> worst machine within about 10% of the average
```

**More virtual nodes cost ring metadata**, which every node gossips: `2,560 points × ~50 bytes = 128 KB`.
**Trivial**, which is why 256 is a free choice.

**Merkle tree repair.**

```
1,000,000 keys per node, one key differs

full comparison   1,000,000 key hashes exchanged
                  at 20 bytes each = 20 MB per pair of replicas per round

Merkle tree       root, then descend one path
                  depth = log2(1,000,000) ~ 20
                  ~20 hashes exchanged = 400 bytes

50,000x less network traffic, and this runs continuously in the background.
```

**Vector clock size.**

```
one entry = node id (16 B) + counter (8 B)  = 24 bytes
typical 2-5 entries                          = 48-120 bytes per value

on a 1 KB value:  ~10% overhead — acceptable
on a 50 B value:  ~200% overhead — the metadata dwarfs the data

-> truncate past ~10 entries, and reconsider vector clocks entirely for
   very small values
```

**Cost.**

```
15 machines, i3.2xlarge-class (8 vCPU, 61 GB, 1.9 TB NVMe)
  ~$0.62/hour x 15 x 730 hours    = ~$6,800/month
cross-AZ traffic: replication is 2 of 3 writes crossing an AZ
  20,000 writes/s x 2 x 1 KB      = 40 MB/s = ~103 TB/month
  at $0.01/GB                     = ~$1,000/month

total ~$8,000/month for 1 billion keys at 120,000 ops/s.

DynamoDB at that load: on-demand pricing would be several times more;
provisioned with reserved capacity, comparable. The trade is operational
effort against price, and at this size managed usually wins.
```

---

## 7. The trade-offs

**Consistency against availability, which is the whole design.** [Day 114](../day-114-heapify/README.md)'s
CAP result says that during a network partition you choose. **Dynamo chooses availability**: both sides of a
partition keep accepting writes, and the divergence is repaired afterwards, sometimes by the application.
**A strongly consistent store like etcd chooses consistency**: the minority side stops serving writes
entirely.

**Neither is better. They are for different data.** A shopping cart should accept writes during a partition —
a customer unable to add an item is a lost sale, and a duplicated item is an annoyance. **A bank ledger should
not.** Say which one the data is before choosing.

**Tunable quorums are a real knob, not marketing.** `N = 3, W = 1, R = 1` is a fast, eventually consistent
store. `W = 2, R = 2` guarantees overlap. `W = 3` makes reads fast at the cost of a write path that any single
slow machine can block. **The same cluster can serve both, per request**, and that flexibility is genuinely
Dynamo's best feature.

**Last-write-wins against vector clocks.** LWW is one timestamp, trivially simple, and it **silently loses
writes when clocks are skewed** — a machine whose clock is two seconds fast wins every conflict it is in, and
nothing reports it. Vector clocks never lose a write and **push the merge onto the application**, which most
teams do not want to write. **Cassandra chose LWW and is enormously popular**, which tells you what most teams
actually pick.

**Virtual nodes cost ring metadata and buy balance**, and the trade is so lopsided — 128 KB against a machine
holding three times its share — that there is no real decision here. **Say the number and move on.**

**Read repair against anti-entropy.** Read repair is free and only fixes what is read; a key nobody reads
stays divergent forever, which matters when it is finally read after a year. Anti-entropy fixes everything and
**costs continuous background I/O and network**. Run both.

**Eventual consistency's real cost is the application code**, and this is the honest thing to say. `get`
returning a list means every caller handles conflict. Most developers will not, so they take the first element
and the store's careful conflict preservation is thrown away at the call site. **If the team will not write
merge logic, use a strongly consistent store and accept the availability cost.**

**When would I not build this?** Almost always. **A single Postgres instance handles a billion keys at ten
thousand operations a second** and gives you transactions, secondary indexes and joins for free. This design
earns its complexity above roughly a terabyte with a global footprint and a hard availability requirement — and
**below that, reaching for it is the most expensive mistake in this course.** And if you genuinely need it,
**DynamoDB exists and is managed**, and choosing to operate your own needs a reason beyond preference.

---

## 8. In the interview

### How it gets asked

- *"Design a key-value store like DynamoDB."* — the standard prompt.
- *"How do you decide which machine holds a key?"* — consistent hashing, and why not modulo.
- *"What is `R + W > N` and why does it work?"* — the counting argument.
- *"Two clients write the same key at the same time. What happens?"* — conflict resolution.
- *"A node has been down for an hour and comes back. How does it catch up?"*
- *"Is it CP or AP?"*

### The first ninety seconds

> "The interface is two operations, `put` and `get`, and I want to start by saying what it deliberately cannot
> do: **no joins, no cross-key transactions, no queries by value.** That poverty is what buys the scale —
> every request touches a handful of machines and never the whole cluster.
>
> **Four decisions, and I will take them in the order the problems arrive.**
>
> **First, placement.** I would not use `hash(key) % machines`, because going from ten machines to eleven
> changes the modulus and remaps about **ninety-one percent of all keys** — a billion keys is 910 GB moving
> across the network while the cluster is degraded. **Consistent hashing** instead: hash the key onto a
> circle, hash each machine onto the same circle, and a key belongs to the first machine clockwise. **Adding a
> machine now moves only about one-eleventh of the data.**
>
> **And virtual nodes on top**, 256 per machine, because ten random points on a circle give badly uneven arcs —
> one machine ends up with three times its share. With 2,560 points the arcs even out to within about ten
> percent. **The second benefit is that a dead machine's load spreads across many survivors instead of landing
> entirely on its clockwise neighbour.**
>
> **Second, replication.** `N = 3` — the owning machine plus the next two **distinct physical machines**
> clockwise, skipping virtual nodes of a machine already in the list, and spread across three availability
> zones. That list is the key's preference list.
>
> **Third, the quorum, which is the interesting decision.** `W` replicas must acknowledge a write, `R` must
> answer a read. **If `R + W > N` the two sets cannot be disjoint, so a read always touches at least one
> machine holding the newest write.** That is pure counting, not a protocol. **I would default to `N=3, W=2,
> R=2`** — and the reason `R=2` rather than `R=3` is latency: `R=3` means every read waits for the slowest of
> three machines, so the p99 becomes the p99 of the worst replica.
>
> **Fourth, conflicts**, which the quorum does not solve. Two clients writing concurrently produce two values
> and **there is no global clock to order them.** I would use vector clocks, keep both versions, and return
> both on read for the application to merge — the shopping-cart approach.
>
> **The main question I would ask first: what kind of data is this?** If it is carts or sessions or user
> profiles, this design is right. **If it is money, I would not build this at all** — I would use something
> strongly consistent and accept the availability cost."

### The follow-ups

**"Explain `R + W > N`. Why does it guarantee anything?"**

> "It is a counting argument about overlapping sets, and there is no protocol involved at all — which is worth
> saying, because it sounds like there should be.
>
> There are `N` replicas. A successful write has landed on at least `W` of them. A read asks at least `R` of
> them.
>
> **If `R + W > N`, those two sets cannot be disjoint.** With `N = 3, W = 2, R = 2`: the write is on two
> machines, the read asks two machines, and there are only three machines. Two plus two is four, and four
> things cannot fit in three boxes without a collision. **So at least one machine that answers my read has the
> new value.**
>
> **And that gives me the newest value only because I can recognise it** — the versions carry vector clocks, so
> among the responses I can tell which dominates. Without versioning, overlap alone would just give me two
> values and no way to choose.
>
> **If `R + W ≤ N` the sets can be disjoint.** `W = 1, R = 1` on three replicas: the write went to A, the read
> asked C, and C has never heard of it. **A stale read, guaranteed possible** — and that is a legitimate
> configuration when writes must never block and staleness is fine.
>
> **What it does not give me is linearizability.** It bounds staleness for a *completed* write. **A write in
> flight — acknowledged by one replica, not yet by the second — can be read by one client and not another**,
> so two concurrent readers can disagree. That is why Dynamo says eventual consistency rather than strong,
> even at `W=2, R=2`.
>
> **And there is a failure mode people forget:** if two of three replicas are down, `W = 2` cannot be satisfied
> and **writes fail**. A sloppy quorum takes the acks from any two healthy machines with hinted handoff instead,
> which keeps writes available and weakens the overlap guarantee — the availability choice again, made
> explicit."

**"Two clients write the same key at the same time. What happens?"**

> "The store cannot order them, and the honest design admits that rather than pretending.
>
> **Why it cannot: there is no global clock.** Client X writes through node A, client Y writes through node B,
> and A and B have clocks that can differ by more than the gap between the writes. **Ordering by timestamp
> would be picking a winner based on clock skew.**
>
> **The simple answer is last-write-wins** — attach a wall-clock timestamp, highest wins. Cassandra defaults to
> this. **It silently loses one of the two writes**, and worse, a machine whose clock runs two seconds fast wins
> every conflict it participates in, forever, and nothing reports it.
>
> **What I would use is vector clocks.** Each value carries a map of node to counter; the node handling a write
> increments its own entry. Comparing two clocks gives one of three answers: **A strictly dominates B, B
> strictly dominates A, or neither** — and neither means they are genuinely concurrent.
>
> **When they are concurrent, the store keeps both**, and the next `get` returns both. **So `get` returns a
> list**, not a value, which is an API decision that forces the caller to notice.
>
> **The application merges.** For a shopping cart, the merge is the union of items — a customer might see
> something they removed, which is annoying, and never loses something they added, which is what matters. **For
> a counter, union is wrong**, and you would use a CRDT or a strongly consistent store instead.
>
> **Two honest costs.** Vector clocks grow, one entry per node that has ever written the key, so production
> systems truncate past about ten entries — **truncation can create false conflicts**, which is safe, since a
> false conflict means an unnecessary merge rather than lost data.
>
> **And the real cost is that most developers will not write the merge.** They will take the first element of
> the list, and everything the store did to preserve both versions is discarded at the call site. **If the team
> will not write merge logic, vector clocks buy nothing and I would use last-write-wins knowingly, or a
> strongly consistent store.**"

**"A node has been down for an hour. It comes back. How does it catch up?"**

> "Three mechanisms, and they cover different gaps, so I would run all three.
>
> **During the outage: hinted handoff.** When a write's target replica is unreachable, the coordinator writes
> to the next healthy machine clockwise with a hint saying who it was really for. That machine stores it in a
> separate hint area, not as its own data. **When the node returns, the hints are delivered and deleted.**
> This is why the store stays writeable through a failure, and it handles most of the hour cleanly.
>
> **On the read path: read repair.** When a read at `R = 2` gets two different versions back, the coordinator
> writes the newer one to the stale replica. **This is free** — the values were already fetched for the read —
> **and it only fixes keys people actually read.** A key nobody reads stays wrong until someone reads it, which
> is the exact moment you least want to discover it.
>
> **In the background: anti-entropy with Merkle trees**, which is the one that guarantees convergence. Each
> replica maintains a hash tree over its key range. Two replicas compare root hashes — **equal means the
> ranges are identical, one comparison for a million keys.** If they differ, they descend into only the
> differing subtree.
>
> **The saving is enormous and worth quantifying.** One differing key in a million: a full comparison would
> exchange a million hashes, about 20 MB. The tree finds it in about twenty comparisons — four hundred bytes.
> **Fifty thousand times less traffic**, which is what makes it viable to run continuously.
>
> **And the case none of them handle: an hour is fine, a week is not.** Hints expire, and a node that has been
> gone long enough has to be treated as a new node — wiped and streamed a fresh copy of its ranges from its
> peers. **Most systems have a configured window, typically a few hours, past which a returning node is
> rebuilt rather than repaired.**"

### The model answer

*"Design a distributed key-value store: one billion keys, a hundred thousand reads and twenty thousand writes
a second, five nines of availability, deployed in three availability zones."*

> "Five nines is the number that decides everything here — twenty-six seconds of downtime a year — so I am
> building an AP system and I will say where that hurts.
>
> **Interface: `put`, `get`, `delete`. No queries by value, no cross-key transactions.** That is what makes the
> rest possible.
>
> **Partitioning: consistent hashing with 256 virtual nodes per machine.** A key hashes onto a circle and
> belongs to the first machine clockwise. **Not modulo** — going from ten machines to eleven would remap ninety
> percent of a billion keys, which is 910 GB of network transfer during exactly the period the cluster is
> already stressed. **Consistent hashing moves about a ninth of that**, and virtual nodes keep the per-machine
> load within about ten percent of even rather than letting one machine hold three times its share.
>
> **Replication: `N = 3`, one replica per availability zone**, using the next three distinct physical machines
> clockwise. **The distinctness check is the easy thing to get wrong** — consecutive virtual nodes can belong
> to the same machine, and then the replication factor is a fiction.
>
> **Quorum: `W = 2, R = 2` by default, tunable per request.** `R + W = 4 > 3`, so the read and write sets must
> overlap. **`R = 2` rather than `3` because `R = 3` makes every read wait for the slowest of three machines** —
> the p99 goes from about 2.5 milliseconds to about 8. **And I would expose the knob:** a session read can use
> `R = 1` for speed; something that must not be stale can use `R = 3`.
>
> **Sizing.** A billion keys at 1 KB is 1 TB, times three replicas is 3 TB, plus twenty percent overhead and
> never running past sixty percent full is about 6 TB provisioned. **But storage is not what sets the machine
> count.** Throughput does: 100,000 reads at `R=2` is 200,000 physical reads, 20,000 writes at `N=3` is 60,000
> physical writes, and an LSM-based node sustains about 20,000 operations a second — so thirteen machines, and
> I would run fifteen across three AZs.
>
> **Storage engine per node: an LSM tree** — memtable, write-ahead log, immutable SSTables, background
> compaction — because writes become sequential appends instead of random seeks. **A Bloom filter per SSTable**
> answers 'definitely not here' in one memory access and skips the disk read entirely.
>
> **Conflicts: vector clocks, both versions kept, `get` returns a list.** I would be explicit with the team that
> this pushes merge logic into the application, and that if they will not write it, the design should change
> rather than the guarantee being quietly abandoned at the call site.
>
> **Failure: hinted handoff during the outage, read repair on the read path, Merkle-tree anti-entropy in the
> background.** And a window — a few hours — past which a returning node is rebuilt from scratch rather than
> repaired.
>
> **Membership: gossip.** Each node exchanges its view with a random peer every second; information reaches
> everyone in about log-n rounds and there is no coordinator to lose. **A central registry would be a single
> point of failure in a system whose entire point is not having one.**
>
> **What five nines actually costs me, stated plainly:** during a network partition both sides keep accepting
> writes, so the data diverges and the application sees conflicts. **I get availability and I pay in
> application complexity.** If this were payment data I would build the opposite system — Raft, strongly
> consistent, unavailable in the minority partition — and accept four nines instead.
>
> **And the honest closing point:** at a billion keys and 120,000 operations a second this design is justified.
> **Below about a terabyte, a single Postgres instance does this with transactions and secondary indexes for
> free**, and choosing this instead would be the most expensive kind of mistake."

---

## 9. Recall card

**Consistent hashing, not modulo:** modulo remaps ~91% of keys when 10 machines becomes 11; the ring moves
~1/n. **256 virtual nodes per machine** evens the arcs to within ~10% and spreads a dead machine's load across
many survivors. **The preference list must skip virtual nodes of a machine already in it** (and skip AZs).

**`R + W > N` is a counting argument, not a protocol** — the read set and write set cannot be disjoint, so one
responding replica has the newest write. **`N=3, W=2, R=2` by default**; `R=3` makes every read wait for the
slowest of three replicas (p99 ~2.5 ms → ~8 ms). It bounds staleness for completed writes; **it is not
linearizability.**

**No global clock means concurrent writes cannot be ordered.** Last-write-wins is one timestamp and silently
loses writes under clock skew (Cassandra's default). **Vector clocks keep both versions, `get` returns a
list, the application merges** — cart = union. Truncate past ~10 entries; false conflicts are safe.

**Three repair mechanisms, all of them:** hinted handoff keeps writes available during a failure; read repair
is free but only fixes what is read; **Merkle-tree anti-entropy** finds 1 differing key in 1,000,000 in ~20
comparisons instead of 20 MB of hashes. **Gossip for membership**, no central registry.

**Per node: an LSM tree** (memtable → WAL → SSTables → compaction) with a **Bloom filter per SSTable**.
**Dynamo is AP by choice** — both sides of a partition accept writes. **And below ~1 TB, one Postgres does this
with transactions and indexes for free**; reaching for this design too early is the expensive mistake.
