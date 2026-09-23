---
day: 108
track: system-design
title: "Consistent hashing"
phase: "Scaling fundamentals"
status: written
---

# Day 108 · System Design — Consistent hashing

**After today you can:** You can explain why adding a server does not reshuffle every key.

**The interviewer asks it as:** *You add a cache node. How many keys move?*

---

## 1. What this is, and why they ask it

**Consistent hashing** is a way of deciding which machine owns which key, such that adding or removing a
machine moves only a small fraction of the keys instead of nearly all of them.

Three sentences. The problem it solves is the one from
[yesterday](../day-107-bst-operations/README.md): with `hash(key) % N`, changing `N` changes almost every
key's answer, so growing a cluster from eight machines to nine relocates about 89 percent of the data. The
trick is to stop dividing by the number of machines and instead **place both the keys and the machines on
a circle**, where a key belongs to the first machine clockwise from it — so adding a machine takes a slice
from one neighbour and disturbs nothing else. And the version everybody draws first does not work in
practice, because a handful of points on a circle land unevenly; the fix, **virtual nodes**, is what makes
it a real technique rather than a diagram.

They ask it because it has a clean answer with a number in it, and because the follow-ups sort people out
fast: *how even is the distribution really?*, *what happens to the load when a node dies?*, and *why
virtual nodes?* A candidate who draws the ring and stops has given a third of the answer.

---

## 2. The story

The road around the lake was a loop, about eleven kilometres, with houses scattered all the way round,
and the dairy collected milk from it twice a day.

For years there had been four collection points, and the rule everybody knew was: **you walk forwards
along the road until you reach a collection point, and that is yours.** Forwards meant clockwise, the
direction the road was numbered. Nobody had to be told which point they belonged to — you just walked the
way the road went until you hit one.

That rule was the reason the arrangement survived thirty years of changes.

When they added a fifth point near the temple, in 1996, almost nothing happened. The houses between the
temple and the *next* point clockwise — the ones who had previously walked past the temple to get to the
old point — now stopped at the temple instead. Everybody else on the entire eleven kilometres carried on
exactly as before. Perhaps sixty houses changed where they walked, out of nine hundred.

When the point near the sawmill closed in 2003, the same thing in reverse: the houses that had used it
simply carried on walking to the next one clockwise. Nobody else was affected at all.

Compare that with what the block office proposed in 1999, which was to number every house and send
odd-numbered ones to point one, and so on by remainder. It would have been perfectly even. It was rejected
in about four minutes, because under it a house's collection point had nothing to do with where the house
was, and every time a point opened or closed, **every single house** would have to be told a new number.

There was one real problem with the walk-forwards rule, and it took them a while to see it.

The five points were not evenly spaced. Three of them were clustered near the town end, within about a
kilometre and a half of each other, and then there was a four-kilometre stretch with nothing. The man at
the point just past that long empty stretch was collecting from nearly three hundred houses while one of
the town points had forty.

Somebody suggested moving the points to space them out, which was impossible, because the points were
where somebody was willing to stand.

What they did instead was stop thinking of a man as a point. Each collector was given **four** small
stands at four different places around the loop, and they took turns being at them across the week — or
sent a boy. Twenty stands around eleven kilometres instead of five, and the same five collectors. With
twenty of them scattered around, no single collector ended up with a four-kilometre stretch, because their
four stands were in four different parts of the loop and the good and bad stretches averaged out.

And it fixed a second thing nobody had planned for. When a collector was ill, previously his entire
stretch had gone to one neighbour, who then had a terrible day. Now his four stands went to four
different neighbours, and nobody had a terrible day.

---

## 3. The idea in plain English

The lake road is a consistent hashing ring, and the villagers found both the technique and the fix that
makes it work.

- The eleven-kilometre loop is the **hash ring** — the space of all hash values, joined end to end.
- Each collection point is a **node** (a server, a cache, a shard).
- "Walk forwards until you reach a point" is the **assignment rule**: a key belongs to the first node
  clockwise.
- Adding the temple point disturbing only sixty houses is the **key property**: adding a node moves only
  the keys between it and its predecessor.
- The four-kilometre gap is **uneven distribution**, the flaw in the naive version.
- Four stands per collector is **virtual nodes**, and the two things it fixed are the two reasons for it.

### The mechanism

```
 1. hash every KEY   to a number in a large space, say 0 .. 2^32 - 1
 2. hash every NODE  (by its name or address) into the SAME space
 3. join the space end to end: it is now a circle
 4. a key belongs to the FIRST NODE CLOCKWISE from it
```

That is the whole algorithm. **The number of nodes never appears in the calculation**, which is exactly
why changing it does not change every answer — that is the sentence to say, because it is the difference
from `% N` in one line.

```
 % N            location = f(key, NUMBER OF NODES)      -> N changes, everything changes
 consistent     location = f(key), then "who is next?"  -> N changes, one arc changes
```

### What happens when a node joins or leaves

```
 ADD a node at position p:
   it takes the arc between p and its PREDECESSOR
   -> only the keys in that arc move, and they all come from ONE node
   -> on average 1/(N+1) of the keys

 REMOVE a node:
   its arc is absorbed by its SUCCESSOR
   -> only that node's keys move, and they all go to ONE node
   -> on average 1/N of the keys

 EVERY OTHER KEY IN THE SYSTEM IS UNAFFECTED.
```

```
 8 nodes -> 9 nodes
   plain modulo:       ~89% of keys move
   consistent hashing: ~11% of keys move        the theoretical minimum
```

**You cannot do better than `1/(N+1)`**, because the new node has to receive *something*, and it should
receive its fair share. Consistent hashing achieves the minimum.

### Why the naive version does not work

With five nodes hashed onto a ring, the five points land wherever the hash function puts them —
**randomly, not evenly**.

```
 5 nodes, one point each, ring of 100 units

 node positions:   3, 11, 19, 24, 87
 arcs owned:      A: 87->3  = 16 units
                  B: 3->11  =  8
                  C: 11->19 =  8
                  D: 19->24 =  5
                  E: 24->87 = 63          <- 63% of all keys on ONE node
```

The four-kilometre stretch. **With `V` random points, the largest arc is much larger than the average**,
and with a handful of nodes the imbalance is severe.

There is a second problem, which matters more in a failure:

```
 node E dies  ->  ALL of E's 63% goes to its single successor, node A
              ->  A now owns 79% and falls over
              ->  A's keys go to B, which falls over
              -> CASCADING FAILURE
```

**A node's entire load lands on exactly one neighbour.** That is the collector's bad day, and at scale it
is how one failure becomes an outage.

### Virtual nodes: the fix, and the two things it fixes

Give each physical machine **many** points on the ring — typically 100 to 500 — by hashing
`"node-A#0"`, `"node-A#1"`, `"node-A#2"` and so on.

```
 5 machines × 200 virtual nodes = 1,000 points around the ring
 -> each machine owns 200 small scattered arcs instead of one large one
 -> the good and bad stretches average out
```

**Fix one: distribution.** The imbalance shrinks as the number of points grows.

```
 virtual nodes per machine    typical spread between busiest and quietest
 -------------------------    -------------------------------------------
 1                            5-10×      unusable
 10                           ~2×        still bad
 100                          ~1.2×      acceptable
 500                          ~1.05×     good
```

The standard deviation of load falls roughly as `1/√V`, which is why the returns diminish and 100–200 is
the usual choice.

**Fix two: failure spreading.** When a machine dies, its 200 arcs are absorbed by 200 different
successors, so the load is spread across the whole cluster rather than dumped on one neighbour.

```
 1 virtual node per machine:  a failure moves 1/N of the load onto ONE machine
                              -> that machine's load DOUBLES
 200 per machine:             a failure moves 1/N of the load, spread over
                              ~all other machines
                              -> each takes about 1/N(N-1) more. Barely noticed.
```

**This second reason is the one candidates leave out**, and it is the more important one operationally.

### Weighted nodes, which come free

A machine twice as powerful gets twice as many virtual nodes, and therefore about twice the keys. **No
special mechanism** — it falls out of the design, and it is a genuinely useful property when a cluster is
built from mixed hardware.

### Replication on the ring

For a store rather than a cache, a key is usually held by the **next `R` distinct nodes clockwise**, not
just the first. That gives replication with no separate placement logic, and it is exactly how Dynamo,
Cassandra and Riak assign replicas.

**The detail worth knowing: "distinct" matters.** Walking clockwise from a key, you might hit three
virtual nodes belonging to the same machine, so implementations skip until they have `R` different
physical machines — and often `R` different racks or availability zones.

### Where it is used, and where it is not

```
 USED FOR
   cache clusters (memcached clients, Redis client-side sharding)
   Cassandra, DynamoDB, Riak, Voldemort — partitioning
   CDN edge selection: which cache in this location holds this URL
   load balancers routing sticky traffic without a shared map
   sharded stateful services generally

 NOT USED FOR
   anything needing explicit placement control — pinning a large tenant to a
   specific machine, keeping data in a legal jurisdiction
   -> those use a DIRECTORY, or the logical-shard map from day 107
```

**The dividing line is whether placement is a computation or a decision.** Consistent hashing computes;
the shard map decides.

### The alternatives, worth naming

- **Rendezvous hashing** (highest random weight): for each key, compute `hash(key, node)` for every node
  and pick the highest. Same minimal-movement property, no ring, no virtual nodes, and perfectly even —
  at the cost of `O(N)` work per lookup instead of `O(log N)`. **Better for small clusters.**
- **Jump consistent hash**: a few lines of arithmetic, no memory, perfectly even — but nodes must be
  numbered `0..N-1` and you can only remove the *last* one. **Great when the cluster only grows.**
- **Maglev hashing** (Google's load balancer): builds a lookup table for `O(1)` routing with very even
  distribution and small disruption. **Used where lookups must be extremely fast.**

**Naming one alternative and its trade-off is a strong finish** to this question.

---

## 4. The picture

The ring, and what adding a node actually disturbs.

```
                       0 / 2^32
                          │
              node A ●────┼────● node B
                    ╱     │     ╲
                   ╱   k1 ○       ╲      ○ = keys
                  │     ○ k2       │     ● = nodes
       node D ●   │                │   ● node C
                  │        ○ k3    │
                   ╲              ╱
                    ╲            ╱
                     ●──────────●
                   node E    (empty arc)

 RULE: a key belongs to the first NODE CLOCKWISE from it.
   k1 -> B      k2 -> B      k3 -> C

 ADD node F between B and C:
   the keys in the arc (B, F] now go to F
   -> k3 may move to F
   -> k1, k2 and EVERY OTHER KEY are untouched
   -> and everything F receives comes from exactly ONE node: C
```

The naive version's problem, drawn to scale:

```
 5 nodes, ONE point each, ring of 100

 0        11   19  24                                        87        100
 |─────────|────|───|─────────────────────────────────────────|─────────|
      A         B    C   D                                          E
      ▲                                                             ▲
      │                                                             │
 arcs:  A: 87→3 (16)   B: 3→11 (8)   C: 11→19 (8)   D: 19→24 (5)   E: 24→87 (63)

 E owns 63% of the keyspace. This is the four-kilometre stretch.

 AND IF E DIES:  all 63% goes to A, its single successor.
                 A now has 79%. A falls over. Then B. Cascade.
```

Virtual nodes, and both fixes at once:

```
 SAME 5 MACHINES, 200 VIRTUAL NODES EACH — 1,000 points on the ring

 |aAcBdEbCaDeAbBcCdDeE...(1,000 small arcs, interleaved)...|

 FIX 1 — distribution:
   each machine owns ~200 small scattered arcs
   busiest / quietest ≈ 1.2× instead of 8×

 FIX 2 — failure spreading:
   machine E dies -> its 200 arcs are absorbed by ~200 DIFFERENT successors
   -> the load spreads across the whole cluster
   -> each survivor takes ~1/N(N-1) more, instead of one machine doubling
```

The comparison that answers the question:

```
 8 nodes -> 9 nodes, 1 TB of data

 PLAIN MODULO                         CONSISTENT HASHING
   keys that move:   ~89%               keys that move:   ~11%
   data moved:       ~890 GB            data moved:       ~111 GB
   source machines:  ALL of them        source machines:  spread over the ring
   safe partial state: NO               safe partial state: yes, arc by arc

 and the reason, in one line:
   modulo:      location = f(key, N)      N changes -> everything changes
   consistent:  location = f(key), then "who is next clockwise?"
                N changes -> one arc changes
```

---

## 5. How it actually works

### The implementation, in outline

```python
    ring = {}                              # hash position -> physical node
    sorted_positions = []                  # kept sorted, for binary search

    def add_node(name, vnodes=200):
        for i in range(vnodes):
            pos = hash_32(f"{name}#{i}")
            ring[pos] = name
            insort(sorted_positions, pos)

    def get_node(key):
        pos = hash_32(key)
        i = bisect_right(sorted_positions, pos)     # the first position > pos
        if i == len(sorted_positions):
            i = 0                                   # wrap around the circle
        return ring[sorted_positions[i]]
```

**Three details that decide whether it works:**

- **`bisect` on a sorted list of positions** makes a lookup `O(log(N × V))` — about 11 comparisons for
  five machines with 200 virtual nodes each. This is the
  [binary search](../day-042-binary-search-idea/README.md) from day 42 doing real work.
- **The wrap-around** — if a key hashes past the last node, it belongs to the first. Forgetting it is the
  classic implementation bug, and it silently sends a slice of keys to the wrong place.
- **The hash function must be well-distributed but need not be cryptographic.** MD5 was traditional;
  **MurmurHash** or **xxHash** are the modern choices, being much faster and well-spread. Do **not** use
  Python's built-in `hash()` for anything shared between processes — it is randomised per process by
  default, so two machines would disagree about where a key lives.

### Migrating the keys when a node joins

For a **cache**, you usually do nothing: the new node starts empty, its keys miss, and they are
repopulated from the origin. The cost is a brief dip in hit rate for `1/N` of the keys.

For a **store**, the arc's data must actually move:

```
 1. the new node joins the ring in a "joining" state — it receives WRITES but
    reads still go to the old owner
 2. the old owner streams the arc's data to it
 3. once caught up, the new node starts serving reads for that arc
 4. the old owner deletes the arc's data
```

**That is the same four-phase shape as [yesterday's](../day-107-bst-operations/README.md) resharding**,
which is worth noticing: dual write, backfill, cut over, clean up.

### Bounded-load consistent hashing

A refinement worth naming, because it addresses the honest weakness. Plain consistent hashing balances
**keys**, not **traffic** — a hot key still overloads its owner.

The bounded-load variant caps each node at, say, 1.25 times the average, and when a key hashes to a node
that is already at its cap, it walks on to the next one clockwise. **Used by Google's load balancers and
by Vimeo, whose engineering write-up is the standard reference.**

### What real systems do

- **Amazon Dynamo** (the 2007 paper) introduced virtual nodes for exactly the two reasons above, and it is
  where the vocabulary comes from.
- **Cassandra** calls them **vnodes** and uses 256 per machine by default. Its ring is the partitioner
  (Murmur3 by default), and replication walks clockwise skipping same-rack nodes.
- **DynamoDB** partitions this way internally, and splits a partition when it gets too large or too hot —
  though it still cannot split a single partition key, which is
  [yesterday's](../day-107-bst-operations/README.md) unbounded-key problem.
- **memcached clients** (`ketama`, originally from Last.fm) do consistent hashing entirely client-side,
  with no coordination between clients at all — which is the purest demonstration of the property: every
  client computes the same answer independently.
- **Akamai** — the technique was invented at MIT in 1997 for exactly this problem, assigning web objects
  to a changing set of caches, and Akamai was founded on it.

---

## 6. The numbers

### The headline

```
 keys that move when the cluster changes size

           plain modulo      consistent hashing
 4 -> 5    ~80%              ~20%
 8 -> 9    ~89%              ~11%
 16 -> 17  ~94%              ~6%
 100 -> 101 ~99%             ~1%

 consistent hashing moves 1/(N+1), which is the theoretical minimum:
 the new node must receive its fair share, and nothing else moves.
```

```
 1 TB across 8 nodes, adding a 9th
   modulo:      ~890 GB moved   ≈ 2.5 hours of saturated 1 Gbit/s copying
   consistent:  ~111 GB moved   ≈ 20 minutes
```

### Virtual nodes and evenness

```
 V per machine     spread (busiest / mean)     std. dev. of load
 --------------    ------------------------    -----------------
   1               5-10×                       ~100%
  10               ~2×                          ~32%
 100               ~1.2×                        ~10%
 200               ~1.15×                        ~7%
 500               ~1.05×                        ~4%

 the deviation falls roughly as 1/sqrt(V), so returns diminish quickly.
 100-256 is the standard choice; Cassandra defaults to 256.
```

**Cost of virtual nodes:**

```
 5 machines × 200 vnodes  =    1,000 ring entries    ~50 KB
 100 machines × 256       =   25,600 entries         ~1 MB
 lookup cost              =    O(log(N×V))
                          =    ~15 comparisons at 25,600 entries
```

**Negligible memory, negligible lookup cost.** There is no reason to skimp.

### Failure spreading, quantified

```
 10 machines, one dies

 V = 1:    its 10% of keys go to ONE successor
           -> that machine goes from 10% to 20% of total load: it DOUBLES
           -> if it was at 60% capacity, it is now at 120%. It fails. Cascade.

 V = 200:  its 10% is spread over ~9 other machines
           -> each goes from 10% to ~11.1% of total load
           -> a 1.1% increase each. Nothing happens.
```

**That contrast is the strongest argument for virtual nodes**, and it is about availability rather than
evenness.

### Cache hit rate during a change

```
 8 cache nodes, adding a 9th, no data migration
   keys that relocate:   ~11%
   those keys miss once, then repopulate

 at a 95% baseline hit rate and 10,000 reads/s:
   during the repopulation window, hit rate dips to ~85%
   origin load goes from 500/s to ~1,500/s for a few minutes

 with plain modulo:
   89% of keys relocate
   hit rate falls to ~10%
   origin load goes from 500/s to ~9,000/s   -> the origin falls over
```

**"Adding a cache node takes down the database" is a real incident**, and it is what consistent hashing
prevents.

### Lookup cost against the alternatives

```
 consistent hashing (ring)    O(log(N×V))    ~15 comparisons
 rendezvous hashing           O(N)           N hashes per lookup — fine for N < 50
 jump consistent hash         O(log N)       a few arithmetic operations, NO memory
 maglev                       O(1)           a table lookup, ~65,000 entries per cluster
```

---

## 7. The trade-offs

### What it costs you

**Placement control.** You cannot choose where a key lives; the hash decides. So you cannot pin a large
tenant to a specific machine, keep data in a jurisdiction, or move one noisy key. **That is the reason
databases with explicit shard maps exist**, and the reason multi-tenant systems use directory sharding
instead.

**It balances keys, not traffic.** A perfect ring with a hot key still has a hot node —
[yesterday's](../day-107-bst-operations/README.md) point, and it is the honest weakness. Bounded-load
consistent hashing addresses it partially; caching the hot key addresses it completely.

**Range queries are gone.** The hash destroys ordering, so "all keys between X and Y" is a scan of every
node. If you need ranges, use ordered partitioning with an explicit map.

### Ring or logical shard map?

**The ring** needs no shared state — every client computes the same answer from the node list alone, which
is why memcached clients use it with no coordination whatsoever. **The map** is explicit, controllable and
must be distributed and kept in step.

**Take the ring for caches and stateless routing; take the map for databases**, where you want to decide
placement, and where you already have a coordination service.

### How many virtual nodes?

**100 to 256.** Below about 100 the distribution is visibly uneven; above about 500 the improvement is
marginal and the ring gets large.

**I would use more** for a small cluster — with three machines, the spread with few virtual nodes is
severe — **and fewer** for a very large one, where `N` itself already smooths things and the ring size
starts to matter.

### Consistent hashing or rendezvous hashing?

**Rendezvous is simpler and more even**: for each key, hash it with every node and take the highest score.
No ring, no virtual nodes, no sorted structure, and it handles weights cleanly. Its cost is `O(N)` per
lookup.

**Take rendezvous for small clusters** — under about fifty nodes, `N` hashes per lookup is genuinely fine
and the code is ten lines. **Take consistent hashing for large ones**, where `O(log(N×V))` matters.

Being able to say "rendezvous hashing is simpler and I would use it under fifty nodes" is a strong,
uncommon answer.

### Where it breaks

- **A hot key.** The ring cannot help; only caching, replication or key splitting can.
- **Client disagreement.** Every client must have the same view of the node list. If one client thinks a
  dead node is alive, it routes there. A shared membership service — or a gossip protocol, as Cassandra
  uses — is required, and it is a real dependency.
- **A non-deterministic hash.** Python's `hash()` on strings is randomised per process by default, so two
  processes disagree about every key. **Use an explicit hash function.**
- **The wrap-around bug.** Keys hashing past the last node must go to the first. Forget it and a slice of
  the keyspace silently goes nowhere or to the wrong node.
- **Flapping nodes.** A machine that repeatedly leaves and rejoins causes its arc to migrate back and
  forth. Membership needs hysteresis, exactly like the health-check thresholds on
  [day 099](../day-099-binary-trees-in-code/README.md).

---

## 8. In the interview

### How it gets asked

- The direct one: *"You add a cache node. How many keys move?"*
- The setup: *"Why not just use `hash(key) % N`?"*
- The one that separates people: *"Why virtual nodes?"*
- The failure probe: *"A node dies. What happens to its load?"*
- The limits: *"Does this solve hot keys?"*

### What to say out loud, in the first ninety seconds

1. **State the problem first.** "With `hash % N`, the number of nodes is *inside* the calculation, so
   changing it changes almost every key's answer — going from eight nodes to nine relocates about 89
   percent of the keys."
2. **Give the mechanism in one sentence.** "Hash the keys and the nodes into the same space, treat it as a
   circle, and a key belongs to the first node clockwise. The node count never appears in the
   calculation."
3. **Give the number.** "Adding a node moves about `1/(N+1)` of the keys — 11 percent at eight-to-nine —
   and they all come from one neighbour. Everything else is untouched. That is the theoretical minimum,
   because the new node has to receive its fair share."
4. **Pre-empt the flaw.** "The version people draw first — one point per node — does not work: a handful
   of random points on a circle land very unevenly, so one node can easily own 60 percent of the ring."
5. **Give both reasons for virtual nodes.** "So each machine gets 100 to 200 points. That evens the
   distribution to about 1.2 times the mean — but the more important reason is failure: with one point per
   node, a machine's entire load lands on a single successor and doubles it, which cascades. With 200
   points, its load spreads across the whole cluster."
6. **Name the honest limit.** "It balances *keys*, not *traffic*. A hot key still overloads its owner, and
   that is a caching problem, not a hashing problem."

### The follow-ups

**"Why not just use `hash(key) % N`?"**
"Because `N` is inside the calculation, so every key's location is a function of the cluster size. Going
from eight nodes to nine, only about one key in nine stays put — 89 percent relocate. For a cache that
means the hit rate collapses from 95 percent to near zero and the origin takes the entire read load: at
10,000 reads a second, the database goes from 500 to 9,000 requests a second, which is how 'we added a
cache node' becomes 'the database fell over'. For a store it means moving 890 gigabytes out of a terabyte
to add one machine, and there is no safe intermediate state because every key changes owner at the same
instant. Consistent hashing removes `N` from the calculation entirely — the key's position on the ring
never changes; only the answer to 'who is the next node clockwise' does."

**"Why virtual nodes?"**
"Two reasons, and the second is the one people miss. **Distribution**: with one point per machine, the
points land wherever the hash puts them, which is random rather than even. With five machines it is common
for one to own well over half the ring — I have seen the textbook example where one node owns 63 percent.
Giving each machine 100 to 200 points makes it own many small scattered arcs, and the good and bad
stretches average out, taking the spread from something like eight times the mean down to about 1.2 times.
**Failure spreading**, which matters more: with one point each, when a machine dies its *entire* load goes
to a single successor — that machine's load doubles, and if it was at 60 percent capacity it is now at 120
and it fails too. That is a cascade. With 200 points, the dead machine's arcs are absorbed by 200
different successors, so in a ten-node cluster each survivor takes about one percent more and nobody
notices."

**"A node dies. What happens to its load?"**
"Its arcs are absorbed by whichever nodes are next clockwise from each of them. With virtual nodes that is
many different machines, so in a ten-machine cluster each survivor's share goes from 10 percent to about
11.1 percent — a one percent increase, invisible. Without virtual nodes it all lands on one machine and
doubles it. For a **cache**, that is the end of the story: the keys miss and repopulate from the origin,
and the hit rate dips for `1/N` of the keys for a few minutes. For a **store**, the data has to already be
somewhere else, which is why a ring-based store keeps each key on the next `R` **distinct** nodes clockwise
— replication falls straight out of the ring with no separate placement logic. 'Distinct' is the detail:
walking clockwise you may hit several virtual nodes of the same machine, so you skip until you have `R`
different physical machines, and usually `R` different racks."

**"Does this solve hot keys?"**
"No, and I would say that plainly, because it is the honest limitation. Consistent hashing distributes
**keys** evenly; it cannot distribute **traffic** evenly, because one key can be a thousand times more
popular than another and it still lives on exactly one node. A perfectly balanced ring with a celebrity's
key on it has a hot node. The fixes are the ones from yesterday: cache that key so the requests never reach
the node, replicate it to every node if it is small and rarely changes, or salt it into ten keys if the
traffic is writes. There is also a refinement called **bounded-load consistent hashing**, which caps each
node at, say, 1.25 times the average and walks a key on to the next node when its owner is full — Google's
load balancers and Vimeo use it — but it manages the symptom rather than removing it."

**"How would you implement the lookup?"**
"Keep the virtual node positions in a sorted array, and for a key, binary-search for the first position
greater than the key's hash — with a wrap-around to index zero if the key hashes past the last node. That
is `O(log(N × V))`, so about fifteen comparisons for a hundred machines with 256 virtual nodes each, and
the ring itself is under a megabyte. Two implementation details that are actual bugs rather than
preferences. The **wrap-around** must be there, or a slice of the keyspace goes to the wrong node silently.
And the **hash must be deterministic across processes** — Python's built-in `hash()` on strings is
randomised per process by default, so two clients would disagree about where every key lives. I would use
MurmurHash or xxHash; MD5 works and is slower, and a cryptographic hash is not needed."

**"Is there anything simpler?"**
"**Rendezvous hashing**, and I would genuinely prefer it for a small cluster. For each key you compute
`hash(key, node)` for every node and pick the highest score. It has the same minimal-movement property,
it needs no ring, no sorted structure and no virtual nodes, it is perfectly even, and weighting a node is
a one-line change. The cost is `O(N)` hashes per lookup instead of `O(log(N × V))` — which for under about
fifty nodes is nothing, and for a thousand nodes is too much. There is also **jump consistent hash**, which
is a few lines of arithmetic with no memory at all, but it requires nodes to be numbered zero to `N−1` and
you can only remove the last one — so it is excellent for a cluster that only grows and useless otherwise.
And **Maglev**, Google's, which builds a lookup table for `O(1)` routing."

### A model answer

Asked: *you add a cache node. How many keys move?*

> "With consistent hashing, about **`1/(N+1)`** — so going from eight nodes to nine, roughly 11 percent, and
> they all come from one neighbour. Everything else in the cluster is untouched. That is the theoretical
> minimum, because the new node has to receive its fair share and nothing more.
>
> The reason that matters is what the alternative does. With `hash(key) % N`, the node count is *inside*
> the calculation, so changing it changes almost every key's answer — eight to nine relocates about **89
> percent** of the keys. For a cache that is not a migration inconvenience, it is an outage: the hit rate
> falls from 95 percent to near zero, and at ten thousand reads a second the origin goes from about 500
> requests a second to nine thousand. 'We added a cache node and the database fell over' is a real
> incident, and this is its cause.
>
> The mechanism is simple. Hash every **key** into a large space — say 32 bits — and hash every **node** by
> its name into the *same* space. Treat that space as a circle by joining the ends. A key belongs to the
> **first node clockwise** from it. The number of nodes never appears anywhere in that calculation, which
> is exactly why changing it does not change every answer: a new node inserts itself at one point on the
> circle and takes the arc between itself and its predecessor. One arc changes; the rest of the ring does
> not know anything happened.
>
> The version people draw first, with one point per node, does not work in practice, and I want to say why
> before you ask. A handful of points hashed onto a circle land **randomly, not evenly** — with five nodes
> it is entirely normal for one to own more than half the ring. So each physical machine gets many points,
> typically **100 to 256**, by hashing `node-A#0`, `node-A#1` and so on. That is virtual nodes, and it fixes
> two separate things.
>
> The obvious one is **distribution**: many small scattered arcs per machine, so the busiest is about 1.2
> times the mean instead of eight times. The one that matters more is **failure**. With one point per
> machine, when a machine dies its entire share lands on a single successor and that machine's load
> doubles — and if it was at 60 percent capacity it is now over 100 and it fails too, which is a cascade.
> With 200 points, the dead machine's arcs are absorbed by 200 different successors, so in a ten-node
> cluster each survivor takes about one percent more and nothing happens.
>
> Two limits I would state. It balances **keys**, not **traffic** — a hot key still overloads its owner, and
> that is a caching problem rather than a hashing one. And it gives up **placement control**: you cannot
> pin a big tenant to a chosen machine or keep data in a jurisdiction, which is why databases often use an
> explicit shard map instead, and caches and stateless routers use the ring — because the ring needs no
> shared state at all. Every memcached client computes the same answer independently, with no coordination
> whatsoever, and that is the property that makes it worth the complexity."

---

## 9. Recall card

- **The problem: `hash % N` puts the node count INSIDE the calculation**, so 8 → 9 nodes relocates **~89%**
  of keys — for a cache, the hit rate collapses and the origin takes **9,000 req/s instead of 500**. **The
  fix: hash keys AND nodes into one space, join it into a circle, and a key belongs to the first node
  CLOCKWISE.** The node count never appears.
- **Adding a node moves `1/(N+1)` of the keys — ~11% at 8 → 9 — and they all come from ONE neighbour.**
  That is the theoretical minimum. Removing a node sends its arc to its successor and disturbs nothing
  else.
- **Virtual nodes (100–256 per machine, Cassandra defaults to 256) exist for TWO reasons, and the second
  is the one people miss.** Distribution: one point per node lands randomly, so one node can own **63% of
  the ring**; 200 points brings the spread to ~1.2× the mean. **Failure spreading**: with one point, a dead
  machine's entire load lands on one successor and **doubles** it → cascade; with 200, it spreads across
  the cluster and each survivor takes **~1% more**.
- **Implementation: sorted positions + binary search, `O(log(N×V))` ≈ 15 comparisons; the ring is under a
  megabyte.** Two real bugs: the **wrap-around** (a key past the last node belongs to the first) and a
  **non-deterministic hash** — Python's `hash()` is randomised per process, so use MurmurHash or xxHash.
  Replication falls out for free: the next **`R` distinct** nodes clockwise.
- **It balances KEYS, not TRAFFIC — it does not solve hot keys**, and it gives up **placement control**
  (hence directory sharding for big tenants and jurisdictions). **Rendezvous hashing is simpler and more
  even at `O(N)` per lookup — genuinely better under ~50 nodes**; jump hash is memory-free but only allows
  removing the last node; Maglev gives `O(1)`.
