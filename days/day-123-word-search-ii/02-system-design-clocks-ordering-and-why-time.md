---
day: 123
track: system-design
title: "Clocks, ordering, and why time is a lie"
phase: "Distributed systems core"
status: written
---

# Clocks, ordering, and why time is a lie

## 1. What this is, and why they ask it

Every machine has a clock, every machine's clock is wrong, and they are all wrong by different amounts. That
is the whole problem. When two machines each write down "this happened at 10:42:31.204", you cannot conclude
anything about which one happened first.

This matters because an enormous number of designs quietly assume you can. Last-write-wins conflict
resolution assumes it. Expiry checks assume it. "Sort the events by timestamp" assumes it. Every one of those
is a bug waiting for a clock to drift.

They ask this because it is the fastest way to find out whether you have thought about distributed systems or
only read the vocabulary. "Two events have the same timestamp. Which happened first?" has an answer that most
candidates get wrong in a specific, revealing way: they reach for a better clock. The right answer is that
you stop asking clocks and start tracking **causality** — what a machine had already seen when it acted.
That is the idea Leslie Lamport published in 1978 and it is still the answer.

By the end of this lesson you can say why timestamps do not order events, define happens-before, use Lamport
clocks and vector clocks and say which one you need, explain what Google's TrueTime actually buys and what it
costs in milliseconds, and name the situations where last-write-wins silently destroys data.

---

## 2. The story

The printing workshop on the corner opens at seven, and there are two people with keys.

Sunita has had hers for nine years. Deepak got his in March. The arrangement is that whoever arrives first
opens the shutter, switches on the big machine so it can warm up, and puts the kettle on.

On Monday they had an argument about it.

Deepak said he had opened up at ten to seven. Sunita said that was not possible, because she had opened up at
five to seven and the shutter was already down when she got there, so if he had come at ten to, where was he?

The trouble is the clocks. The big round one on the workshop wall runs fast. Everybody knows it runs fast;
nobody knows by how much, and the last time anyone corrected it was before Diwali. Deepak goes by the small
display on his scooter, which is slow, and which he reset badly the last time the battery came out. Sunita
goes by her phone.

So Deepak's "ten to seven" and Sunita's "five to seven" are not two facts about the same morning. They are
two facts about two different instruments, and neither instrument is telling the truth.

They went round it for ten minutes and got nowhere, because there is nothing to get. Two numbers that came
from two wrong clocks cannot be compared, however confidently either person says them.

Then Rekha, who does the binding, said the thing that ended it.

"Deepak, was the kettle warm when you got here?"

He thought about it. It was, actually. He remembered noticing, because he did not have to wait for it.

"Then she was here first," Rekha said. "You saw something she had already done."

Nobody had to know what time it was. Nobody had to fix the wall clock. One person had seen the result of the
other person's work, and that settled the order completely — it is not possible to see the kettle already
warm before somebody has put it on.

Rekha went back to her binding. The wall clock is still fast.

---

## 3. The idea in plain English

Rekha solved in one sentence what two clocks could not.

**Wall-clock time is a measurement, not a fact.** The **wall clock** on a machine — the one that says
`2026-09-01 10:42:31` — is a physical device, usually a cheap crystal, that drifts. Left alone it typically
gains or loses somewhere between a few seconds and a minute a month. Two machines that were set correctly
last week are not set correctly now, and they are wrong in different directions.

**Clock skew is the gap between two clocks at the same instant.** Inside a well-run data centre, machines
synchronise against a time source and skew is usually under a few milliseconds. Across the internet, tens to
hundreds of milliseconds. It is never zero, and there is no way to make it zero, because the message that
carries the correction takes time to arrive and you do not know exactly how much.

**So a timestamp cannot order two events on two machines.** If machine A stamps `10:42:31.100` and machine B
stamps `10:42:31.050`, and the two clocks might be 80 milliseconds apart, then B's event might have happened
30 milliseconds *after* A's. The timestamps say the opposite. This is Deepak's scooter against Sunita's
phone.

**Worse, the clock can go backwards.** When the correction arrives and the machine is running fast, the time
is pulled back. An event at `10:42:31.200` can be followed by an event at `10:42:31.150` on the same machine.
Any code that assumed time only increases is now wrong. This is why every language has a second, separate
clock — a **monotonic clock**, which only ever counts forwards and is meaningless as a date, and which is the
only correct thing to use for measuring how long something took.

**The kettle is causality.** Rekha did not compare clocks. She found a case where one person *observed the
result* of the other's action. That is a fact about the world, not about any instrument, and it cannot be
wrong.

**That is the happens-before relation.** Event A **happens-before** event B, written `A → B`, when one of
three things is true:

1. A and B are on the same machine and A came first in its own sequence.
2. A is the sending of a message and B is the receiving of that same message.
3. There is a chain: `A → C` and `C → B`.

Nothing in that definition mentions a clock. It is built entirely out of "this machine did this, then that"
and "this message went from here to there".

**When neither happens-before the other, they are concurrent.** Written `A || B`. Concurrent does not mean
"at the same time" — it means **no information flowed between them**, so nothing in the system can put them
in an order, and you should stop trying. Two people editing different paragraphs of the same document at
opposite ends of the world are concurrent, and that is a fact about the system, not about their watches.

**A Lamport clock is a counter that respects causality.** Each machine keeps one number. Increment it before
every event. Send it with every message. On receiving a message, set your number to `max(mine, theirs) + 1`.
The result has one guarantee, and exactly one: if `A → B`, then `A`'s number is smaller than `B`'s. It gives
you a **total order** — sort by the number, break ties by machine name — that never contradicts causality.

**But a Lamport clock cannot tell you the opposite.** A smaller number does *not* mean it happened before. It
might just be concurrent. If you need to detect concurrency — "did these two writes conflict, or did one see
the other?" — one counter is not enough.

**A vector clock is one counter per machine.** Each machine keeps a list: what it believes every machine's
counter to be. Increment your own entry on every event; send the whole list with every message; on receipt,
take the element-wise maximum and then increment your own. Now you can compare two vectors:

- Every entry of `A` is ≤ the matching entry of `B`, and at least one is strictly smaller → `A → B`.
- Same the other way → `B → A`.
- Neither → **concurrent**, and the system must either merge them or hand them to a human.

That last line is the payoff. **A vector clock is the machinery that lets a system say "these two writes
genuinely conflict" instead of silently keeping one.**

---

## 4. The picture

Three machines, five events, and the message arrows that create the ordering.

```mermaid
sequenceDiagram
    participant A as Node A
    participant B as Node B
    participant C as Node C

    Note over A: e1 — write x=1
    A->>B: replicate x=1
    Note over B: e2 — receives, writes x=1
    Note over C: e3 — write x=9 (knows nothing)
    B->>C: replicate x=1
    Note over C: e4 — receives; conflict with e3
    Note over A: e5 — read x
```

**What to notice.** `e1 → e2` because a message went from A to B. `e2 → e4` for the same reason. So
`e1 → e4` by the chain rule. But `e3` and `e1` have no path between them in either direction: no message
went from one to the other before both had happened. They are **concurrent**, and no clock reading can change
that. When `e4` arrives at C, C is holding two values that nothing in the system can order.

Now the same three machines with the wall clocks written in, to show why the timestamps are useless:

```
                     what each machine's clock says
    real time    A (+40ms fast)   B (on time)   C (-70ms slow)
    ----------   --------------   -----------   --------------
    10:00.000    10:00.040        10:00.000     09:59.930     <- e1 on A
    10:00.020    10:00.060        10:00.020     09:59.950     <- e3 on C
    10:00.030    10:00.070        10:00.030     09:59.960     <- e2 on B

    stamps recorded:   e1 = 10:00.040   e3 = 09:59.950   e2 = 10:00.030

    sort by timestamp:  e3, e2, e1        <- completely wrong
    truth:              e1, e3, e2
```

**What to notice.** Sorting by the recorded timestamps puts `e3` first and `e1` last, which is the exact
reverse of what happened. The clocks are only 110 milliseconds apart in total, which is a perfectly ordinary
amount of skew across regions, and the events are 30 milliseconds apart, which is a perfectly ordinary gap
between related writes. **Skew larger than the gap between events is the whole failure, and it is normal.**

And here is the vector clock doing what timestamps cannot:

```
                A         B         C
    start     [0,0,0]   [0,0,0]   [0,0,0]

    e1 on A   [1,0,0]                        A writes x=1
    e3 on C                       [0,0,1]    C writes x=9
    e2 on B             [1,1,0]              B receives A's message
    e4 on C                       [1,1,2]    C receives B's message

    compare e3 [0,0,1] with e1 [1,0,0]:
        0 <= 1 but 1 > 0     -> not e3 -> e1
        1 <= 0 is false      -> not e1 -> e3
        => CONCURRENT. Two real values. The system must decide.
```

**What to notice.** The vector does not tell you which value to keep. It tells you, correctly and without
guessing, that there is a decision to make. Last-write-wins would have thrown one of them away and told
nobody.

---

## 5. How it actually works

### NTP, and what it can and cannot give you

**NTP** — the Network Time Protocol — is how machines fix their clocks. A machine asks a time source what
time it is, measures the round trip, assumes the delay was symmetric, and adjusts. It runs continuously and
corrects by small amounts.

What it achieves in practice:

- Within one data centre, against a local stratum-1 source: **0.1 to 5 milliseconds** of skew.
- Over the public internet: **10 to 100 milliseconds**, worse on congested or asymmetric paths.
- A machine that has lost its time source for a day: **seconds**, drifting steadily.

Two properties matter more than the numbers. First, NTP will **step the clock backwards** if it is far
enough ahead, so wall-clock time is not monotonic. (`ntpd` slews small corrections gradually and steps large
ones; either way you cannot rely on the wall clock only increasing.) Second, NTP gives you no bound you can
program against — it does not hand you an error bar, so you never know how wrong you are.

Leap seconds are the famous edge. In 2012 a leap second caused a live-lock in the Linux kernel's timer code
that took down Reddit, Mozilla and several airlines' booking systems on the same night. Google's response was
**leap smear** — spreading the extra second across 24 hours as a tiny slowdown, so no clock ever repeats or
jumps. AWS and Meta do the same now. This is worth knowing because it is a memorable, concrete example of
"time is not a reliable input".

### Monotonic clocks, and the bug everyone writes

Two clocks exist on every machine and they are for different jobs:

| | Wall clock | Monotonic clock |
|---|---|---|
| Python | `time.time()` | `time.monotonic()` |
| Means | Date and time of day | Seconds since some arbitrary point |
| Can jump | Yes, forwards and backwards | No, only increases |
| Use for | Timestamps, expiry dates, logs | Measuring durations, timeouts, rate limits |

The bug: measuring elapsed time with the wall clock. An NTP correction of −200 milliseconds during a
measurement yields a negative duration, and code that assumed durations are positive does something strange —
a timeout that never fires, a rate limiter that lets everything through, a lock lease that appears to have
expired the moment it was taken. Use the monotonic clock for every interval and this class of bug disappears.

### Lamport clocks in practice

A counter per machine, incremented per event, maxed on receipt. Cheap: eight bytes on the wire, one integer
in memory.

Where you actually see it: any system that needs a stable, agreed order but does not need to detect conflicts.
Kafka's per-partition offsets are a degenerate case — a single counter defining order within a partition,
which is exactly why Kafka can only promise ordering *within* a partition and not across topics. The
[replicated log](../day-119-heaps-revision/README.md) behind Raft is the same idea: the index in the log is
the order, and no clock is consulted.

### Vector clocks in practice

One counter per machine, so the metadata grows with the cluster. Amazon's original Dynamo paper used vector
clocks and exposed conflicts to the application, which then merged them — the famous shopping-cart example,
where merging two carts means taking the union, so a concurrent "add socks" and "add shoes" gives you both.
Riak did the same. CouchDB keeps conflicting revisions and makes you pick.

Cassandra explicitly does **not**. Cassandra uses last-write-wins on wall-clock timestamps, and its own
documentation warns you about the consequence: two writes within the clock skew window, and one silently
disappears. This is a genuine trade — Cassandra chose simplicity and constant-size metadata — but it means
**Cassandra can lose writes on a clock problem, by design.** Say that in an interview and you will be taken
seriously.

The practical problem with vector clocks is that the vector grows. A cluster of 500 nodes means 500 entries
of roughly 16 bytes each, or 8 KB of metadata on every value. The standard fixes are to attach entries only
for *client sessions* rather than nodes, and to truncate the oldest entries with a timestamp, accepting a
small chance of a false conflict.

### Hybrid logical clocks

An HLC packs a physical time and a logical counter into one value. It behaves like a wall-clock timestamp —
you can read it, sort it, and compare it to a real date — while guaranteeing that causally ordered events get
increasing values, because the logical part increments when the physical part has not moved enough.

CockroachDB, YugabyteDB and MongoDB (as `clusterTime`) all use HLCs. This is the modern default: you get
something close to a real timestamp *and* the causality guarantee, with 8 to 16 bytes of metadata instead of
a vector.

### TrueTime, and buying certainty with hardware

Google's Spanner takes the other route. Every data centre has GPS receivers and atomic clocks, and the
TrueTime API does not return a time — it returns an **interval**: "now is somewhere between `earliest` and
`latest`". The width of that interval, called epsilon, is typically **1 to 7 milliseconds**.

Spanner then does something blunt and effective. To commit a transaction, it picks a timestamp, and then
**waits until the interval has definitely passed** before making the commit visible. That is **commit-wait**,
and it costs about `2 × epsilon`, so roughly **10 milliseconds added to every write transaction**.

What you buy for those 10 milliseconds is enormous: timestamps that can be compared *globally*, so Spanner
can offer externally consistent transactions across continents. What you pay is 10 milliseconds and a fleet
of atomic clocks. AWS now offers a similar bounded-error clock service, so the technique is no longer unique
to Google — but the trade is the same, and it is the cleanest example in the whole field of **spending
latency to buy certainty about time.**

---

## 6. The numbers

**How wrong is a clock?** Start with the raw drift of an ordinary crystal oscillator:

```
typical drift          ~ 30 parts per million
per day                30 x 10^-6 x 86,400 s = 2.6 seconds per day
per month              ~ 78 seconds
```

So an unsynchronised machine is over a minute out within a month. That is why NTP runs continuously.

**With NTP running:**

```
same data centre, local source     0.1 - 5 ms
across regions, public internet    10 - 100 ms
source unreachable for 24 h        ~ 2.6 s and growing
```

**When does skew actually break ordering?** It breaks whenever skew exceeds the gap between two events you
want to order. Take a replicated write:

```
write on node A, replicate to node B
network hop between regions        ~ 40 ms
clock skew between regions         ~ 50 ms

50 ms skew > 40 ms gap  ->  B's timestamp can be EARLIER than A's
                            for an event that happened later
```

Now put traffic on it. Ten thousand writes a second to one hot key:

```
10,000 writes/s     -> one write every 0.1 ms
skew                -> 50 ms
writes inside the skew window: 50 / 0.1 = 500 writes
```

**Five hundred writes are unorderable by timestamp.** Under last-write-wins, any of those 500 could win, and
499 vanish. This is not a rare race; at that rate it is continuous.

**What last-write-wins costs.** Take a system doing 1,000 writes a second where 0.5% of writes touch a key
another node wrote within the skew window:

```
1,000/s x 0.005          = 5 conflicting writes per second
x 86,400                 = 432,000 conflicts per day
```

With last-write-wins, roughly half of those discard the value that should have survived — **on the order of
200,000 silently lost writes a day.** With vector clocks, all 432,000 are surfaced as conflicts for the
application to merge. The second number is much more alarming to look at and much less alarming to live with.

**What metadata costs.**

```
Lamport clock       8 bytes per value
HLC                 8 - 16 bytes per value
vector clock, 10 nodes    10 x (8 id + 8 counter) = 160 bytes
vector clock, 500 nodes   500 x 16                = 8,000 bytes
```

On a 200-byte value, a 10-node vector is 80% overhead and a 500-node vector is 4,000% overhead. That single
line explains why nobody runs plain vector clocks on a large cluster:

```
1 billion values x 8 KB of vector = 8 TB of pure metadata
1 billion values x 16 B of HLC    = 16 GB
```

**What TrueTime costs.**

```
epsilon                    1 - 7 ms, call it 5 ms
commit-wait                2 x epsilon = 10 ms per write transaction
```

```
a transaction that would take 5 ms   ->  15 ms
throughput on one hot row: 1000/5 = 200/s  ->  1000/15 = 66/s
```

Three times fewer transactions per second on a contended row, in exchange for globally comparable timestamps.
For a bank ledger that is a bargain. For a metrics pipeline it is absurd. **Naming which side of that line
your system is on is the answer to the trade-off question.**

---

## 7. The trade-offs

**Last-write-wins is cheap, simple, and loses data.** Constant metadata, no merge logic, no conflicts to
show a user. In exchange, any two writes inside the skew window are ordered arbitrarily and one is discarded
with no record. Choose it when a lost write is genuinely tolerable — a presence indicator, a "last seen"
value, a cached counter that will be recomputed. Do not choose it for anything a user typed. Cassandra's
default is LWW, and that is the single most common way people lose data in Cassandra.

**Vector clocks are correct and do not scale as written.** They detect concurrency exactly, with no false
negatives. They cost one entry per participant, which is fine at ten and impossible at five hundred, and they
push the merge decision onto the application — which is real work, and sometimes there is no sensible merge.
"Union the shopping carts" is easy. "Merge two versions of a user's address" is not.

**Hybrid logical clocks are the sensible default and they still have a hole.** Readable like a timestamp,
causally correct, 16 bytes. What they do not give you is a *bound* on how far ahead of real time you might
be — HLC guarantees causality, not accuracy. If your system needs "this certificate expired at 3 p.m. real
time", an HLC does not settle it.

**TrueTime buys certainty and pays in latency and hardware.** Ten milliseconds on every write transaction,
plus GPS receivers and atomic clocks in every data centre. Worth it when you need externally consistent
global transactions. Not worth it for anything that could be partitioned so that a single machine owns each
key — and if you can partition that way, you should, because a single owner gives you order for free.

**Physical timestamps in logs are fine, and you should still keep them.** None of this means removing wall
clocks from your log lines. It means not *ordering* by them across machines. Log the wall clock for humans,
log a request ID and a sequence number for machines, and put both in every line. Debugging an incident with
only causal clocks is miserable; debugging it with only wall clocks is impossible.

**When would I not think about this at all?** When there is a single writer. If one machine owns a key —
because it is the leader for that partition, or because the key is sharded to it — then the order is the
order that machine applied them, and no clock is involved. **Most systems avoid this entire problem by
funnelling writes for a key through one owner, and that is a legitimate answer to give.** The interesting
cases are multi-master, offline-capable clients, and cross-region active-active, which is exactly where these
problems live.

---

## 8. In the interview

### How it gets asked

- *"Two events have the same timestamp. Which happened first?"* — the direct version.
- *"How do you order events across machines?"*
- *"Two replicas got different writes to the same key. How do you resolve it?"*
- *"What is a vector clock and when would you use one over a timestamp?"*
- *"Your rate limiter lets through twice the limit occasionally. Why?"* — usually a wall-clock-vs-monotonic
  bug.
- *"How does Spanner give globally consistent transactions?"* — the TrueTime question.

### The first ninety seconds

> "The honest answer to 'which happened first' is that from the timestamps alone, you cannot tell, and I
> would not try. Two machines' clocks differ — a few milliseconds in one data centre, tens to hundreds of
> milliseconds across regions — and if the skew is larger than the gap between the two events, the timestamps
> can be in exactly the wrong order. At ten thousand writes a second and fifty milliseconds of skew, five
> hundred consecutive writes are unorderable by timestamp. So this is not a rare race.
>
> What I use instead is causality. Event A happened-before event B if they are on the same machine in that
> order, or if A sent a message that B received, or by a chain of those. That definition never mentions a
> clock — it is built out of what a machine had actually seen when it acted.
>
> The cheap implementation is a Lamport clock: one counter per machine, incremented per event, and on
> receiving a message you take the max of yours and theirs plus one. That guarantees that if A caused B, A's
> number is smaller. It gives me a total order that never contradicts reality.
>
> What it does not give me is the reverse. A smaller number does not prove A came first — the two might be
> concurrent, meaning no information flowed between them. If I need to *detect* that, which I do for conflict
> resolution, I need a vector clock: one counter per machine, compared element-wise. If neither vector
> dominates, the writes genuinely conflict and the system has a decision to make rather than a value to
> discard.
>
> Do you want me to go into what I would actually deploy, or into how Spanner sidesteps this with hardware?"

### The follow-ups

**"Why not just synchronise the clocks better?"**

> "Because 'better' has a floor you cannot get under, and more importantly NTP gives you no error bar. It
> corrects your clock but does not tell you how wrong you still are, so there is no threshold you can
> program against.
>
> There are two further problems. NTP can step the clock backwards, so wall-clock time is not even monotonic
> on one machine — an event stamped 31.200 can be followed by one stamped 31.150. And the correction message
> itself takes an unknown, asymmetric amount of time, which is the irreducible part.
>
> Google did solve it, and the solution shows the price. TrueTime returns an interval rather than a time —
> 'now is between these two points' — with an epsilon of one to seven milliseconds, backed by GPS and atomic
> clocks in every data centre. Then Spanner waits out that interval before making a commit visible, about ten
> milliseconds per write transaction. So the answer to 'synchronise better' is: yes, with atomic clocks, and
> it costs you ten milliseconds on every write. That is a real option and I would name it as one, but it is
> not a free fix."

**"Two replicas have different values for the same key. Walk me through resolving it."**

> "First I would ask what the metadata is, because that decides everything. Three cases.
>
> If all I have is wall-clock timestamps, it is last-write-wins, and I would say plainly that this can lose
> data: two writes inside the skew window get ordered arbitrarily and one is discarded with no record. That
> is Cassandra's default and it is the most common way people lose writes in Cassandra. Acceptable for a
> 'last seen at' field. Not acceptable for anything a user typed.
>
> If I have vector clocks, I compare element-wise. If one vector dominates the other, that write saw the
> other and supersedes it — keep it, no conflict. If neither dominates, they are concurrent and both are
> real, so I keep both as siblings and either merge them semantically or surface them.
>
> Merging semantically is the part worth designing. If the value is a set — a shopping cart, a set of tags —
> the union is correct and automatic; that is the Dynamo cart example, and the known cost is that a deleted
> item can come back. If the value is a counter, use a structure that merges by construction. If it is a
> plain scalar like an address, there is no sensible automatic merge and I would keep both and ask the user,
> the way CouchDB does.
>
> What I would not do is pretend a policy makes the conflict go away. Picking the larger value or the longer
> string is still discarding a real write, just with extra steps."

**"Our rate limiter occasionally lets through double the limit. Any idea?"**

> "Almost certainly the wall clock. If the window is computed with `time.time()`, an NTP correction that
> steps the clock backwards makes the current window restart, so a fresh allowance is handed out
> mid-window — and if it steps forward, a window is skipped entirely.
>
> The fix is one line: measure every interval with the monotonic clock, which only increases and is immune to
> corrections. Wall clocks are for dates you show to humans; monotonic clocks are for durations, timeouts and
> lease expiry.
>
> This same bug appears in three other places I would check while I am there: lock leases, retry backoff, and
> anything that computes 'how long has this been running'. A lock lease measured on a wall clock can appear
> to expire the instant it is taken, which then hands the lock to a second holder — and that is a
> correctness bug, not a performance one."

**"What does a Lamport clock actually guarantee? Be precise."**

> "One direction only. If A happens-before B, then Lamport(A) < Lamport(B). The converse does not hold:
> Lamport(A) < Lamport(B) tells me nothing, because A and B may be concurrent.
>
> That is enough to build a total order — sort by counter, break ties by machine ID — which is consistent with
> causality, and that is exactly what you need for something like a replicated state machine, where all you
> require is that everyone applies operations in the same order and that order never contradicts cause.
>
> It is not enough for conflict detection, which needs the converse. That is the one-sentence reason vector
> clocks exist."

**"What would you actually deploy in 2026?"**

> "Hybrid logical clocks, unless I had a specific reason not to. They give me a value that reads like a real
> timestamp — sortable, comparable to a date, usable in a log — while guaranteeing that causally ordered
> events get increasing values, and they cost eight to sixteen bytes rather than a vector that grows with the
> cluster. CockroachDB, YugabyteDB and MongoDB's `clusterTime` all use them.
>
> Before that, though, I would try to make the problem not exist: route all writes for a key through a single
> owner. If one machine applies every write to a key, the order is whatever it applied, and no clock is
> involved at all. Most well-designed systems dodge this entire topic that way, and I would say so rather
> than reach for clever clocks first.
>
> Vector clocks I would keep for genuinely multi-master or offline-capable cases — a mobile app that edits
> while disconnected — where concurrency is normal and merging is a product decision, not a bug."

### The model answer

*"Design the conflict resolution for a note-taking app that syncs across a phone, a laptop and a web client,
and works offline."*

> "Offline editing makes concurrent writes the normal case rather than a rare race, so this is exactly where
> the clock question earns its keep. Let me be concrete about what I would build.
>
> **First, I reject timestamps outright, and I would say why with a number.** A phone that has been on a
> plane for four hours has a clock that has drifted seconds, not milliseconds, and it will sync its edits all
> at once when it reconnects. Ordering those against the laptop's edits by wall clock is not approximately
> right, it is arbitrary. Last-write-wins here means a user watches a paragraph they typed on the plane
> disappear.
>
> **Every device gets a stable ID, and every note carries a version vector** — one counter per device that
> has ever edited it. On an edit, the device increments its own entry. On sync, the two vectors are compared
> element-wise: if one dominates, that version is strictly newer and wins with no conflict at all, which is
> the common case and costs nothing. If neither dominates, the edits are genuinely concurrent.
>
> **Vector size is bounded by devices per note, not by cluster size,** which is the reason this works here
> and would not work for a 500-node store. A user has three or four devices; that is 64 bytes of metadata on
> a note. I would prune entries for devices that have not touched the note in ninety days, accepting a small
> chance of a spurious conflict in exchange for a bounded size.
>
> **For genuine conflicts I merge rather than pick, where the data shape allows it.** Note text is a sequence,
> so I would use a structure designed to merge — a CRDT for text, which resolves character-level concurrent
> edits deterministically on every device without a coordinator. Tags are a set, so union, with the known
> caveat that deletes need tombstones or a removed tag reappears. Anything that genuinely cannot be merged —
> two different titles — I keep as two versions and show the user, because inventing an answer is worse than
> asking.
>
> **The server timestamps everything too, and never orders by it.** Wall-clock time goes in the sync log for
> humans debugging a support ticket. It never decides which edit wins. Those are two different jobs and
> mixing them is the bug.
>
> **The numbers I would quote.** Version vector: 4 devices × 16 bytes = 64 bytes on a note averaging 2 KB, so
> 3% overhead. Conflict rate in practice: with offline editing, a few percent of syncs, versus effectively
> continuous silent loss under last-write-wins. And the thing I would flag as the real cost is not storage —
> it is that merging is now product work. Someone has to decide what merging two versions of a title means,
> and that decision cannot be made in the storage layer."

---

## 9. Recall card

**A timestamp does not order events across machines.** Skew is 0.1–5 ms in one data centre and 10–100 ms
across regions; whenever skew exceeds the gap between two events, the timestamps can be exactly backwards.

**Order by causality instead.** `A → B` if same machine and earlier, or A sent the message B received, or by
a chain. No clock appears in that definition. Neither direction holding means **concurrent** — no information
flowed, and nothing can order them.

**Lamport clock:** one counter, `max(mine, theirs) + 1` on receive. Guarantees `A → B ⇒ L(A) < L(B)` and
*only* that. **Vector clock:** one counter per machine, compares element-wise, and is the only one that can
*detect* concurrency — at 16 bytes per participant.

**Last-write-wins silently discards data** inside the skew window; that is Cassandra's default. HLCs (16
bytes, readable, causally correct) are the modern default; TrueTime buys global order for ~10 ms of
commit-wait per transaction plus atomic clocks.

**Use the monotonic clock for every duration** — timeouts, leases, rate-limit windows. The wall clock jumps
backwards, and that bug shows up as a rate limiter letting through double.
