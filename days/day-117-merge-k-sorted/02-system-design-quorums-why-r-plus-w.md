---
day: 117
track: system-design
title: "Quorums: why R plus W must exceed N"
phase: "Distributed systems core"
status: written
---

# Day 117 · System Design — Quorums: why R plus W must exceed N

**After today you can:** You can compute a quorum and show why the inequality guarantees an overlap.

**The interviewer asks it as:** *You have five replicas. What R and W would you pick?*

---

## 1. What this is, and why they ask it

A **quorum** is the number of replicas that must respond before an operation counts as done. Write to `W`
of `N` replicas; read from `R` of them; and if you choose them correctly, **the read is guaranteed to see
the write**.

Three sentences. The rule is one inequality — **`R + W > N`** — and the reason it works is the
pigeonhole principle: if the set you wrote to and the set you read from together exceed the total, they
must share at least one replica, and that replica has the newest value. It is the **dial** that
[CAP](../day-114-heapify/README.md) does not describe and that
[consistency models](../day-115-heapq/README.md) hinted at, because moving `R` and `W` slides you between
fast-and-stale and slow-and-correct without changing anything else. And the interesting part is what
happens when you deliberately break the inequality, which is what most large systems actually do.

They ask *"five replicas — what R and W?"* because it is arithmetic with a reason behind it, and the
follow-ups are unforgiving: *why not `W = 5`?*, *what does the overlapping replica actually give you?*, and
*is that really linearizable?* The last one has a surprising answer, and knowing it separates people who
have read about quorums from people who have thought about them.

---

## 2. The story

The temple trust had eleven trustees and a rule book written in 1954, and the rule that mattered was
about how a decision became a decision.

For anything involving money, six trustees had to sign. Not a majority of those present — six of the
eleven, wherever they were.

Perumal, who kept the register, explained the other half of the rule to a new trustee in his first month,
because the new man had asked a reasonable question: how do you know, six months later, what was actually
decided?

The rule book said you asked six trustees.

The new man said that was strange. Six to decide and six to find out — why the same number?

Perumal said it is not a coincidence and it is not tradition. There are eleven of us. If six signed, and
you go and ask six, then **at least one of the people you ask must have been one of the people who
signed**. Six and six is twelve, and there are only eleven of us, so somebody is in both groups. There is
no way to pick six who were all absent.

He said if the rule had been five to decide and five to ask, you could very easily talk to five people who
had all been away that day, and every one of them would honestly tell you nothing had been decided. Five
and five is ten, and eleven minus ten leaves room for a complete miss.

The new man asked why they did not just require all eleven to sign, which would make it certain.

Perumal said they had tried it in the sixties, and it had lasted about a year. One trustee was in Singapore
for four months and the trust could not do anything at all. **The more people you need, the more certain
you are and the more easily you are stopped.** Six is the smallest number that cannot be dodged.

And there was one more part of the rule that the new man found odd until it was explained. If you asked six
and two of them said one thing and four said another, the register entry with the later date was the
decision, and you were supposed to **tell the two who had it wrong**, so that next time they would be
right.

Perumal said that was the part that kept the whole thing from drifting. Without it, the same two people
would go on giving the same wrong answer for years, and every time you happened to ask them you would get
it.

---

## 3. The idea in plain English

The trust is a quorum system, and Perumal's argument about six and six is the proof of `R + W > N`.

- Eleven trustees are the `N` **replicas**.
- Six signatures is the **write quorum, `W`**.
- Asking six is the **read quorum, `R`**.
- "Somebody must be in both groups" is the **pigeonhole argument**, and it is the whole theorem.
- Requiring all eleven is `W = N`, and the trustee in Singapore is why nobody does it.
- Telling the two who had it wrong is **read repair**.

### The rule, and why it works

> **`R + W > N` guarantees that the read set and the write set overlap.**

**The proof is one sentence.** The write went to `W` replicas. The read asks `R` replicas. If `R + W > N`,
then those two sets cannot be disjoint — there are not enough replicas for them to avoid each other — so
at least one replica you read from received the write, and it has the newest value.

```
 N = 5
   W = 3, R = 3   ->  3 + 3 = 6 > 5   ✓  they MUST share at least one
   W = 2, R = 2   ->  2 + 2 = 4 ≤ 5   ✗  you can read {A,B} after writing {D,E}

 the overlap size is exactly  R + W − N
   W=3, R=3, N=5  ->  at least 1 replica in common
   W=4, R=4, N=5  ->  at least 3 in common
```

**And the second half, which people forget: you must be able to tell which value is newest.** The
overlapping replica has the new value, but the others may return an old one, so every record carries a
**version** — a counter, a timestamp, or a vector clock — and the reader takes the highest. Without
versioning, the overlap is useless because you cannot tell which of the returned values to believe.

**That is the second sentence of the answer**, and it is the one that shows understanding rather than
recall.

### Choosing R and W

```
 N=3, W=2, R=2    the default. 2+2 = 4 > 3 ✓
                  tolerates 1 failure for both reads and writes
                  balanced latency

 N=3, W=3, R=1    fast reads (any replica), brittle writes
                  ONE replica down blocks ALL writes

 N=3, W=1, R=3    fast writes, slow reads
                  ONE replica down blocks ALL reads

 N=5, W=3, R=3    3+3 = 6 > 5 ✓
                  tolerates 2 failures for both. The standard for
                  something important.

 N=5, W=1, R=1    1+1 = 2 ≤ 5 ✗  NO overlap guarantee
                  fastest possible, fully eventual
                  -> and this is what many large systems actually run
```

**The choice is a latency-and-availability trade**, and the shape of it is worth saying:

- **Increasing `W`** makes writes slower and less available, and reads faster.
- **Increasing `R`** does the reverse.
- **`W = 1, R = N`** and **`W = N, R = 1`** both satisfy the inequality and are opposite extremes.
- **The balanced choice is `W = R = ⌈(N+1)/2⌉`** — a majority both ways.

### Why not `W = N`?

Perumal's trustee in Singapore. **Requiring every replica means any single failure blocks every write.**

```
 N = 3, W = 3
   each replica 99.9% available
   P(all three up) = 0.999^3 = 99.7%   ->  ~26 hours/year of blocked writes

 N = 3, W = 2
   P(at least 2 up) = 99.9997%          ->  ~1.6 minutes/year
```

**Sixteen thousand times better availability**, for one fewer replica. **That arithmetic is the answer to
"why not just write to all of them?"**

### Latency: the quorum is as slow as its slowest member

This is the operational fact people miss.

```
 W = 3 of N = 5
 -> you wait for the THIRD FASTEST replica to acknowledge
 -> not the average, not the fastest

 replica latencies: 2 ms, 3 ms, 5 ms, 40 ms, 200 ms
   W=1  ->  2 ms
   W=3  ->  5 ms
   W=5  ->  200 ms      ← one slow replica sets the whole latency
```

**Which is why `W = N` is bad for latency as well as availability**: you inherit the tail of every replica.
A quorum of a majority lets you ignore the slowest `N − W` replicas, and **that is the main reason
quorums exist at all** — not just fault tolerance, but tail-latency insulation.

### Sloppy quorums and hinted handoff

Strict quorums require the `W` acknowledgements to come from the `N` replicas **that own the key**. A
**sloppy quorum** relaxes that: if some of the owners are unreachable, write to `W` nodes *somewhere* in
the cluster, and hand the data back when the owners return.

```
 STRICT     W acks from the N designated replicas
            -> if fewer than W owners are reachable, the write FAILS
            -> R + W > N still guarantees overlap

 SLOPPY     W acks from ANY W nodes, with hints for the absent owners
            -> the write SUCCEEDS during a partition
            -> R + W > N NO LONGER guarantees overlap, because the
               writers and the readers may be different sets entirely
```

**Say that trade explicitly.** Dynamo and Cassandra default to sloppy quorums because availability during a
partition is worth more to them than the overlap guarantee — and the guarantee is restored when the hints
are replayed. **It is a deliberate weakening, not a bug.**

### The uncomfortable truth: quorums are not linearizable

**`R + W > N` guarantees you read *a* value at least as new as the last completed write. It does not give
you [linearizability](../day-115-heapq/README.md).** Three specific holes:

**A partial write.** A write reaches two of three replicas and then the client dies. It was never
acknowledged, so it is neither committed nor rolled back — and subsequent reads may or may not see it,
non-deterministically.

**Concurrent writes.** Two clients write different values at the same time, each reaching a quorum. There
is no ordering between them, so which one "wins" depends on the conflict-resolution rule, and different
readers may briefly see different answers.

**Read-after-read going backwards.** A read repairs some replicas and not others, so a subsequent read
touching a different subset may return an older value — a **monotonic reads** violation.

**The fix for genuine linearizability is a consensus protocol** — Paxos or Raft — which is
[day 119](../day-119-heaps-revision/README.md). Cassandra exposes this as **lightweight transactions**,
which use Paxos for a single key and are roughly four times slower than a quorum write.

**Being able to say "a quorum is not linearizability, and here is why" is the strongest single thing you
can say about this topic.**

### Read repair, and how the system heals

When a read collects `R` responses and they disagree, the coordinator:

1. returns the value with the **highest version**;
2. **writes it back** to the replicas that were behind.

Perumal telling the two trustees who had it wrong. **Without it, a stale replica stays stale for every
future read that happens to include it**, and the divergence persists indefinitely.

Read repair only fixes keys that are **read**. Cold keys are healed by
[anti-entropy](../day-116-top-k/README.md) with Merkle trees, and a replica that was down is caught up by
**hinted handoff**.

---

## 4. The picture

The pigeonhole argument, drawn. **This is the diagram.**

```
 N = 5 replicas:  A  B  C  D  E

 WRITE to W=3:    [A] [B] [C]  D   E
                   ▲   ▲   ▲
                   the write set

 READ  from R=3:   A   B  [C] [D] [E]
                           ▲   ▲   ▲
                           the read set

                          ┌───┐
                          │ C │  ← IN BOTH. Guaranteed.
                          └───┘

 3 + 3 = 6 > 5, and there are only 5 replicas — so the two sets of
 three CANNOT be disjoint. There is nowhere for them both to hide.

 overlap size = R + W − N = 1


 NOW BREAK IT:  W = 2, R = 2

 WRITE to:  [A] [B]  C   D   E
 READ from:  A   B   C  [D] [E]      ← NO OVERLAP. The read misses the write.

 2 + 2 = 4 ≤ 5. There is room for the two sets to avoid each other entirely.
```

The trust, as the same picture:

```
 11 trustees. Six sign. You ask six.

 signed:  ●●●●●●○○○○○
 asked:   ○○○○○●●●●●●
                ▲
          6 + 6 = 12 > 11, so at least ONE person is in both groups.

 if it were FIVE and FIVE:
 signed:  ●●●●●○○○○○○
 asked:   ○○○○○○●●●●●
          5 + 5 = 10 ≤ 11 — and 11 − 10 = 1 leaves room for a COMPLETE MISS.
          You could ask five people who were all away, and every one of
          them would honestly say nothing was decided.
```

Choosing R and W, and what each costs:

```
 N = 5

 W  R  W+R  overlap  write latency   read latency   tolerates
 -  -  ---  -------  -------------   ------------   ---------------------
 1  5   6      1     fastest         slowest        0 replica failures for reads
 2  4   6      1     fast            slow           1 write, 1 read failure
 3  3   6      1     balanced        balanced       2 failures BOTH ways ← default
 4  2   6      1     slow            fast           1 write, 3 read failures
 5  1   6      1     SLOWEST         fastest        0 failures for writes
 1  1   2      ✗     fastest         fastest        NO guarantee — fully eventual

 the OVERLAP is the same (1) for every valid row.
 what changes is WHERE you pay: writes or reads, latency or availability.
```

Latency is the slowest member of the quorum:

```
 five replicas respond in:  2 ms · 3 ms · 5 ms · 40 ms · 200 ms

 W=1  ├─┤                                    2 ms
 W=3  ├────┤                                 5 ms      ← ignores the slow two
 W=5  ├──────────────────────────────────┤ 200 ms      ← inherits the WORST tail

 THIS is the main reason quorums exist: not only fault tolerance, but
 insulation from the tail latency of the slowest N−W replicas.
```

Why a quorum is not linearizability:

```
 1. PARTIAL WRITE
    client writes to A, B → then DIES before the ack
    the write is neither committed nor rolled back
    -> some later reads see it, some do not. Non-deterministic.

 2. CONCURRENT WRITES
    client 1 writes x=5 to {A,B,C}
    client 2 writes x=9 to {C,D,E}   at the same moment
    -> no ordering exists between them; the "winner" depends on the
       conflict rule, and different readers may briefly disagree

 3. READS GOING BACKWARDS
    read 1 touches {A,B,C}, repairs A and B
    read 2 touches {C,D,E}                     ← D and E are still stale
    -> the second read returns an OLDER value. Monotonic reads violated.

 R + W > N gives you "at least as new as the last COMPLETED write".
 It does NOT give you a single global order. For that: Paxos or Raft.
```

---

## 5. How it actually works

### The write path

```
 1. the coordinator sends the write to ALL N replicas (not just W)
 2. it waits for W acknowledgements
 3. it returns success to the client
 4. the remaining N − W acks arrive later, or never

 -> the write is SENT to all N; only the ACK count is W
 -> which is why the extra replicas still converge, and why W is about
    latency and durability rather than about how many copies exist
```

**That detail matters**: `W = 2` of `N = 3` does not mean only two copies exist. All three are written to;
you simply do not wait for the third.

### The read path

```
 1. the coordinator sends the read to R replicas (often to all N)
 2. it collects R responses with their VERSIONS
 3. it returns the highest version to the client
 4. it WRITES THAT VALUE BACK to any replica that was behind  ← read repair
```

**Step 3 is why versioning is not optional.** The overlap guarantees one replica has the new value; the
version is how you recognise which one.

### The version, and what it can and cannot do

```
 a simple counter or timestamp
   -> tells you which is NEWER
   -> cannot distinguish "newer" from "concurrent"
   -> last-write-wins, and it SILENTLY LOSES the other write

 a vector clock (one counter per replica)
   -> distinguishes "A happened before B" from "A and B are CONCURRENT"
   -> surfaces genuine conflicts to the application instead of hiding them
   -> costs one counter per replica in every record
```

**Dynamo used vector clocks and handed conflicts to the application** — the shopping cart that unions
divergent versions. **Cassandra uses last-write-wins timestamps** and accepts the data loss, which is
simpler and is why clock skew matters there.

### Sloppy quorums, concretely

```
 N = 3 for key K, owned by replicas A, B, C.  W = 2.
 B and C are unreachable.

 STRICT:  only A is available -> fewer than W -> the write FAILS

 SLOPPY:  write to A, and to D and E (which do NOT own K),
          with HINTS saying "this belongs to B and C"
          -> the write SUCCEEDS
          -> when B and C return, D and E hand the data over
          -> until then, a strict read of {A,B,C} may MISS it
```

**So during the window, `R + W > N` does not hold in any meaningful sense** — the writers and readers are
different sets. **That is the price of availability, paid knowingly.**

### What real systems do

- **Dynamo, Cassandra, Riak** expose `N`, `R` and `W` directly, with `QUORUM` as a named level meaning
  `⌊N/2⌋ + 1`. Cassandra's default for a serious workload is `N=3, R=QUORUM, W=QUORUM`.
- **Cassandra's `LOCAL_QUORUM`** is the practical multi-region setting: a majority **within one
  datacentre**, so you get the overlap guarantee locally without paying a cross-region round trip on every
  operation. **Naming this is a strong, specific detail.**
- **DynamoDB** hides the knobs and offers two levels: eventually consistent reads (one replica, half the
  cost) and strongly consistent reads (a quorum, full cost and higher latency).
- **Cassandra's lightweight transactions** (`IF NOT EXISTS`) use Paxos for genuine linearizability on a
  single partition, at roughly four times the cost of a quorum write.
- **ZooKeeper, etcd and Raft-based systems** use a majority quorum for **consensus**, not just for
  overlap — which is the difference between `R + W > N` and an actual total order.

---

## 6. The numbers

### The inequality, worked

```
 N   majority   W=R=majority   W+R    overlap    tolerates
 --  --------   ------------   ---    -------    ---------
 3      2         2, 2          4 > 3    1        1 failure
 4      3         3, 3          6 > 4    2        1 failure  ← no better than 3
 5      3         3, 3          6 > 5    1        2 failures
 6      4         4, 4          8 > 6    2        2 failures ← no better than 5
 7      4         4, 4          8 > 7    1        3 failures
```

**Even `N` buys nothing**, exactly as with [leader election](../day-111-serialise-a-tree/README.md): a
majority of 4 is 3, the same as a majority of 3 requires you to tolerate only one failure — and you pay
for an extra replica.

### Availability, by configuration

```
 each replica 99.9% available (8.8 hours/year down)

 N=3, W=1   P(≥1 up) = 99.9999999%      ~0.03 s/year
 N=3, W=2   P(≥2 up) = 99.9997%         ~1.6 minutes/year
 N=3, W=3   P(3 up)  = 99.7%            ~26 hours/year   ← WORSE than one machine
 N=5, W=3   P(≥3 up) = 99.99999%        ~0.3 s/year
```

**`W = N` is worse than a single machine.** That is the arithmetic behind "never require all replicas",
and it is worth stating as a number rather than a principle.

### Latency, by configuration

```
 replica response times: 2, 3, 5, 40, 200 ms  (N = 5)

 W=1   2 ms     the fastest replica
 W=2   3 ms
 W=3   5 ms     ← ignores the slowest two entirely
 W=4  40 ms
 W=5 200 ms     inherits the worst tail

 p99 effect: with W=3 of 5, you need three of five to be fast,
 which is far more likely than all five being fast.
```

**This is the tail-latency argument for quorums**, and it is the half people forget: a majority quorum
does not just tolerate failures, it **routinely ignores the slowest replicas**, which is worth more in
day-to-day latency than the fault tolerance is.

### The cost of each configuration

```
 6,000 reads/s, 600 writes/s, N=3

 W=2, R=2   each write hits 3 replicas, waits for 2   -> 1,800 replica writes/s
            each read hits 2 (or 3) replicas          -> 12,000-18,000 replica reads/s

 W=2, R=1   reads hit 1 replica                       -> 6,000 replica reads/s
            (but NO overlap guarantee: 2 + 1 = 3, not > 3)
```

**`R = 1` halves the read load and gives up the guarantee** — which is exactly the eventual-versus-strong
choice, priced in load rather than in latency.

### Cross-region

```
 same-region quorum        ~5 ms
 cross-region quorum       ~150-300 ms   (you wait for a remote replica)

 N=6 across 2 regions, W=4  -> every write waits for a remote ack: ~150 ms
 N=6, LOCAL_QUORUM=2        -> ~5 ms, with the overlap guarantee only
                               WITHIN the region
```

**That is why `LOCAL_QUORUM` exists**, and it is the standard multi-region configuration: local
consistency, cross-region eventual.

### Overlap size

```
 overlap = R + W − N

 N=5, W=3, R=3   ->  1 replica in common (the minimum that works)
 N=5, W=4, R=4   ->  3 in common
```

**A bigger overlap buys nothing for correctness** — one is enough — and costs latency and availability on
both sides. **`R + W = N + 1` is the efficient point.**

---

## 7. The trade-offs

### Where you pay: reads or writes

The inequality says the *sum* must exceed `N`; it says nothing about how to split it. **So the choice is
which side pays.**

```
 read-heavy workload    -> low R, high W    (W=N, R=1: fast reads, brittle writes)
 write-heavy workload   -> low W, high R
 balanced / unknown     -> W = R = majority
```

**I would default to majority-majority** unless the ratio is extreme, because it tolerates the most
failures on both sides and its latency is symmetric.

### Strict or sloppy?

**Strict** preserves the overlap guarantee and refuses writes when fewer than `W` owners are reachable —
which is a CP choice.

**Sloppy** accepts the write anywhere and hands it back later, so writes stay available during a
partition — an AP choice, and it **gives up the guarantee** for the duration.

**Dynamo-lineage systems default to sloppy**, and I would say so explicitly rather than let someone assume
the inequality always holds. **It is a deliberate weakening.**

### Quorum or consensus?

**A quorum gives you overlap.** It is cheap, it needs no leader, and every node can coordinate.

**Consensus gives you a total order.** It costs a leader, an election protocol, and roughly four times the
latency for a single operation.

**I would use a quorum for data and consensus for decisions** — configuration, locks, leadership, unique
constraints — which is exactly why Cassandra holds your data and etcd holds your cluster's mind.

### What versioning you choose matters more than R and W

```
 timestamps (last-write-wins)
   + simple, one field
   − silently loses one of two concurrent writes
   − with clock skew, may keep the OLDER one

 vector clocks
   + distinguishes concurrent from ordered
   + surfaces conflicts instead of hiding them
   − one counter per replica in every record, and the app must resolve
```

**"Which conflict-resolution strategy?" is a more consequential question than "which R and W?"**, and it
is the one candidates skip.

### Where quorums mislead

- **They are not linearizability.** Partial writes, concurrent writes and non-monotonic reads all remain
  possible.
- **`R + W > N` says nothing about durability.** `W = 2` means two replicas acknowledged; if both are in
  the same rack and it loses power, the write is gone. **Placement matters as much as the count.**
- **Sloppy quorums quietly suspend the guarantee**, and the system does not tell you when.
- **Bigger is not better.** `W = N` is worse than one machine for availability and inherits the worst
  replica's latency.

---

## 8. In the interview

### How it gets asked

- The arithmetic: *"You have five replicas. What R and W would you pick?"*
- The proof: *"Why does `R + W > N` work?"*
- The trap: *"Why not write to all five?"*
- The depth probe: *"Is that linearizable?"*
- The applied one: *"How would you configure this across two regions?"*

### What to say out loud, in the first ninety seconds

1. **Give the rule and the proof together.** "`R + W > N`, and the reason is pigeonhole: if the set I wrote
   to and the set I read from together exceed the total number of replicas, they must share at least one —
   and that one has the newest value."
2. **Give the concrete answer.** "For `N = 5` I would take `W = 3, R = 3`. Six is greater than five, so
   there is always an overlap of at least one, and it tolerates two failures on both the read and the
   write path."
3. **Say the second half immediately.** "And the overlap is only useful if I can tell which returned value
   is newest — so every record carries a version, and the reader takes the highest. Without versioning the
   guarantee is worthless."
4. **Pre-empt "why not all five".** "I would not use `W = 5`: any single replica being down blocks every
   write, and at 99.9 percent each that is twenty-six hours a year against about a minute and a half for
   `W = 3`."
5. **Give the latency reason, which is the underrated one.** "A quorum also insulates me from tail
   latency — with `W = 3` of 5 I wait for the third fastest and ignore the slowest two, so one sick
   replica does not set my write latency."
6. **Volunteer the limitation.** "One thing worth saying: a quorum is **not** linearizability. It
   guarantees I read something at least as new as the last completed write, not a single global order."

### The follow-ups

**"Why does `R + W > N` work?"**
"Pigeonhole. The write went to `W` replicas; the read asks `R` replicas. If `R + W > N`, those two sets
cannot be disjoint — there simply are not enough replicas for them to avoid each other — so at least one
replica in my read set received the write. With `N = 5, W = 3, R = 3`, six exceeds five, so the overlap is
at least one. Break it — `W = 2, R = 2`, which is four and not more than five — and I can write to A and B
and then read from D and E and miss it entirely. And the second half matters just as much: the overlapping
replica has the new value, but the others will return old ones, so **every record has to carry a version**
and the reader takes the highest. Without versioning I have an overlap I cannot recognise, which is no
guarantee at all."

**"Why not write to all five?"**
"Because availability collapses and latency inherits the worst replica. With each replica at 99.9 percent,
requiring all three of `N = 3` gives about 99.7 percent — roughly twenty-six hours a year of blocked
writes, which is **worse than a single machine**. Requiring two gives 99.9997 percent, about a minute and
a half a year. That is a factor of sixteen thousand for one fewer acknowledgement. And separately, a
quorum's latency is the latency of its **slowest member**: if five replicas respond in 2, 3, 5, 40 and 200
milliseconds, waiting for three costs 5 milliseconds and waiting for all five costs 200. So a majority
quorum is not only fault tolerance — it routinely lets me **ignore the slowest replicas**, which is worth
more in day-to-day p99 than the failure tolerance is."

**"Is that linearizable?"**
"No, and this is the most important thing to know about quorums. `R + W > N` guarantees I read a value at
least as new as the last **completed** write — it does not give a single global order, and there are three
concrete holes. **Partial writes**: a client writes to two of three replicas and then dies before the
acknowledgement, so the write is neither committed nor rolled back, and subsequent reads may or may not
see it, non-deterministically. **Concurrent writes**: two clients each reach a quorum with different
values at the same moment; there is no ordering between them, so which one wins depends on the
conflict-resolution rule and different readers can briefly disagree. And **reads going backwards**: a read
that repairs some replicas but not others means a later read touching a different subset can return an
older value, which violates monotonic reads. For genuine linearizability you need a consensus protocol —
Paxos or Raft — and Cassandra exposes exactly that as lightweight transactions, at roughly four times the
cost of a quorum write."

**"How would you configure this across two regions?"**
"Not with a global quorum, because every write would wait for a cross-region acknowledgement — a hundred
and fifty to three hundred milliseconds instead of five. The standard answer is **`LOCAL_QUORUM`**: a
majority **within one datacentre**, so I get the overlap guarantee locally at local latency, and
cross-region replication is asynchronous and eventual. So with `N = 6` split three and three, I would use a
local quorum of two rather than a global quorum of four. What that costs is honest and worth stating: a
reader in the other region may not see a write for the replication lag, and if a whole region is lost, the
writes that had not yet crossed are gone. That is the same trade as
[synchronous versus asynchronous replication](../day-104-tree-path-problems/README.md) — cross-region
synchronous is physics-limited and essentially nobody does it."

**"What is a sloppy quorum?"**
"A strict quorum requires the `W` acknowledgements to come from the `N` replicas that actually **own** the
key. If fewer than `W` of those owners are reachable, the write fails — a CP choice. A **sloppy** quorum
relaxes it: write to any `W` nodes in the cluster, with **hints** recording which owners the data really
belongs to, and hand it over when they return. The write succeeds during a partition, which is an AP
choice, and the cost is that **`R + W > N` no longer guarantees an overlap** for the duration — the
writers and the readers may be entirely different sets. Dynamo-lineage systems default to this because
availability during a partition is worth more to them than the guarantee, and the guarantee is restored
when hinted handoff replays. I would call it out explicitly, because it is easy to quote the inequality
and not notice that the system you are using has suspended it."

**"How does the system heal after a stale read?"**
"Three mechanisms, and they cover different data. **Read repair**: when the coordinator collects `R`
responses and they disagree, it returns the highest version **and writes it back** to the replicas that
were behind — so any key that gets read converges within milliseconds. That is the trust register telling
the two trustees who had it wrong, and without it the same replicas would keep giving the same stale
answer indefinitely. **Hinted handoff**: writes accepted on behalf of a node that was down are replayed
when it returns. And **anti-entropy**: a background pass comparing Merkle trees to find which key ranges
differ in `O(log n)` exchanges, which is the only thing that fixes **cold** keys — the ones no read ever
touches. So the convergence time is bimodal: milliseconds for hot keys, and the anti-entropy interval for
everything else."

### A model answer

Asked: *you have five replicas — what R and W would you pick?*

> "**`W = 3` and `R = 3`**, and let me give the rule and the reason together, because the reason is the
> whole answer.
>
> The rule is **`R + W > N`**. Here that is three plus three is six, which is greater than five. And the
> reason it works is pigeonhole: the write went to three replicas, the read asks three replicas, and there
> are only five in total — so those two sets of three **cannot avoid each other**. At least one replica I
> read from received the write. If I dropped to `W = 2, R = 2`, that is four, which is not more than five,
> and I could write to A and B and then read from D and E and miss the write entirely.
>
> There is a second half that is just as necessary and that people leave out. The overlapping replica has
> the new value, but the other two will return old ones — so **every record must carry a version**, and the
> reader takes the highest. Without versioning I have an overlap I cannot identify, which is no guarantee
> at all. And what kind of version matters: a plain timestamp gives last-write-wins, which silently
> discards one of two concurrent writes and, with clock skew, may keep the older one. A vector clock
> distinguishes 'newer' from 'concurrent' and surfaces the conflict instead of hiding it, at the cost of a
> counter per replica in every record.
>
> Three-and-three is also the balanced choice: it tolerates **two failures on both the read and the write
> path**, which is the most you can get from five, and its latency is symmetric.
>
> I would not use `W = 5`, and the arithmetic is stark. With each replica at 99.9 percent available,
> requiring all of them gives you availability **worse than a single machine** — for `N = 3, W = 3` that is
> about twenty-six hours a year of blocked writes against ninety seconds for `W = 2`. And there is a
> latency reason as well, which is the one people miss: a quorum's latency is the latency of its **slowest
> member**. If five replicas respond in 2, 3, 5, 40 and 200 milliseconds, `W = 3` costs five milliseconds
> and `W = 5` costs two hundred. So a majority quorum is not only fault tolerance — it routinely lets me
> **ignore the slowest replicas**, which does more for my p99 than the fault tolerance does.
>
> The last thing I would say unprompted: **this is not linearizability**. `R + W > N` gives me a value at
> least as new as the last completed write; it does not give a single global order. A partial write from a
> client that died is neither committed nor rolled back; two concurrent writes have no ordering between
> them; and successive reads can go backwards if one repaired some replicas and the next touches others.
> If I need a genuine total order — for a lock, a unique username, or a leader — that is consensus, Paxos
> or Raft, and it costs several times a quorum write."

---

## 9. Recall card

- **`R + W > N`, and the proof is PIGEONHOLE**: the write set and the read set together exceed the number
  of replicas, so they **must share at least one** — and that replica has the newest value. `N=5, W=3, R=3`
  → 6 > 5 ✓. `W=2, R=2` → 4 ≤ 5 ✗, and you can write {A,B} then read {D,E} and miss it entirely.
- **The overlap is useless without VERSIONS** — every record carries one and the reader takes the highest.
  A timestamp gives last-write-wins (**silently loses a concurrent write**, and with clock skew keeps the
  *older*); a **vector clock** distinguishes concurrent from ordered and surfaces the conflict.
- **Never `W = N`.** At 99.9% per replica, `N=3, W=3` gives ~**26 hours/year** of blocked writes — *worse
  than one machine* — against ~**1.6 minutes** for `W=2`. And **a quorum's latency is its SLOWEST member**:
  with responses of 2/3/5/40/200 ms, `W=3` costs 5 ms and `W=5` costs 200. **Tail-latency insulation is the
  underrated half of why quorums exist.**
- **A QUORUM IS NOT LINEARIZABILITY.** It guarantees a value at least as new as the last *completed* write,
  not a global order. Three holes: a **partial write** from a dead client is neither committed nor rolled
  back; **concurrent writes** have no ordering; and **reads can go backwards** after partial read repair.
  For a total order you need **consensus** (Paxos/Raft) — Cassandra's lightweight transactions, ~4× the
  cost.
- **A SLOPPY quorum accepts `W` acks from ANY nodes with hints for the absent owners** — the write survives
  a partition and the inequality's guarantee is **suspended** until hints replay. Dynamo-lineage systems
  default to this. Healing is **read repair** (hot keys, milliseconds) · **hinted handoff** (a returning
  node) · **anti-entropy with Merkle trees** (cold keys). Across regions use **`LOCAL_QUORUM`**: ~5 ms
  instead of ~150–300 ms, with the guarantee holding only within the region. **Even `N` buys nothing.**
