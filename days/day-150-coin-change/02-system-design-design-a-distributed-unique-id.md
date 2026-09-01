---
day: 150
track: system-design
title: "Design a distributed unique ID generator"
phase: "High-level design case studies"
status: written
---

# Design a distributed unique ID generator

## 1. What this is, and why they ask it

Every row in every table needs an identifier. On one database, `AUTO_INCREMENT` handles it and nobody thinks
about it again.

**Across a hundred machines with no shared counter, it becomes a real design problem** — and the reason it is
asked so often is that it is small enough to finish in twenty minutes and deep enough that the follow-ups are
genuine. There is a right answer, it is public, and it fits in sixty-four bits.

**Snowflake** — Twitter's design from 2010 — is what most interviewers have in mind: a timestamp, a machine
identifier, and a per-millisecond sequence number, packed into one 64-bit integer. **Every production system
you have used generates IDs this way or something very close to it.**

They ask it because it forces four things to be said precisely at once. **Uniqueness** without coordination.
**Sortability**, because an ID that sorts by time makes range queries and database indexes dramatically
cheaper. **Size**, because 128-bit UUIDs cost real money at scale in ways that surprise people. And **clocks**,
because the whole design rests on time moving forwards and time does not always move forwards.

The clock question is the one that separates candidates. **What happens when NTP steps the clock backwards?**
is the follow-up, and the honest answer is a short, specific piece of engineering.

By the end of this lesson you can lay out the 64 bits and justify each field, explain why UUIDs are the wrong
default, handle clock skew, assign machine IDs without a human, and size the whole thing.

---

## 2. The story

The hospital gave every patient a number and for nineteen years the number came from one book.

The book lived at the front desk. You arrived, the man at the desk wrote your name, and beside it he wrote the
next number, and that number was yours. **Nothing could go wrong, because there was one book and one man and
one pen.**

Then they opened the second building.

And the obvious thing happened, which is that the second building could not send someone across the compound
to the front desk for every patient, so the second building got its own book. Which started, because nobody
thought about it for more than four seconds, **at one**.

**By the end of that month there were two patients with the number 4,412** and both of their folders were in
the same cupboard.

The fix was the kind of fix that gets made in an afternoon. **The first building's numbers would start with a
one and the second building's with a two.** Building one issued 1-0001, building two issued 2-0001, and they
could never collide, and nobody had to talk to anybody.

That held for eight years and three more buildings.

**What broke it was the filing.**

Because the folders were kept in number order, and number order was now building order, and **a doctor looking
for everyone admitted in the same week had to walk to five cupboards.** The numbers no longer told you when.
They told you where.

So the sister who ran the records room made the change that actually mattered, and she made it without asking
anyone. **She put the date at the front.**

**Year, month, day, then the building, then the count for that day in that building.** 25-03-14-2-0087.

And the folders sorted themselves. Everything from the fourteenth sat together regardless of which building
had issued it, the building was still there so nothing could collide, and the daily count reset every morning
so it never grew large.

The only trouble came the following March, when the clock on the wall of building four was found to be
eleven days slow.

---

## 3. The idea in plain English

The sister invented Snowflake. Timestamp first, then the machine, then a counter — and the wall clock in
building four is the failure mode the whole design has to survive.

**Start with what you need from an ID.** Four things, and they conflict:

- **Unique.** Two machines must never produce the same value, ever, with no coordination between them.
- **Sortable by time.** Newer IDs should be numerically larger. This is not cosmetic — it is what makes
  database indexes fast and "give me the last fifty" a range scan.
- **Small.** Every foreign key, every index entry, every log line carries it.
- **Fast.** Generated locally, no network call, millions per second.

**Now the options, in the order people reach for them.**

**A database auto-increment.** One counter, guaranteed unique, perfectly sortable. **And it is a single point
of failure and a hard throughput ceiling**, because every insert in the entire system serialises through one
row. It works until it does not, and then it is very hard to change.

**A UUID (version 4).** 128 random bits. **Genuinely unique with no coordination at all** — the collision
probability is negligible — and generated locally in microseconds. **Two serious costs.**

**It is twice the size**, which sounds trivial and is not: a billion rows with three foreign keys and four
indexes multiplies that difference by eight.

**And it is random, which destroys the index.** A B-tree index on a random key means every insert lands in a
different page, so the database is writing random pages instead of appending to one. **Insert throughput drops
by a factor of two to ten**, index pages fragment, and the cache hit rate collapses because the working set
becomes the whole index rather than its right-hand edge. **This is the single most important practical fact in
this lesson**, and it is why "just use UUIDs" is the answer that loses the interview.

**Snowflake**, which is what to design. **64 bits, laid out in four fields:**

```
 1 bit    unused (sign bit — keeps the number positive)
41 bits   milliseconds since a custom epoch
10 bits   machine id
12 bits   sequence within that millisecond
```

**Every field earns its width, and being able to say why is the answer.**

**41 bits of milliseconds is 69 years.** `2^41` milliseconds is about 69.7 years — and the epoch is *custom*,
set to the day the system launched, rather than 1970. **That choice buys back the decades already spent**, and
it is a one-line decision with a fifty-year consequence.

**10 bits of machine id is 1,024 machines.** Enough for almost anything, and it is the field to rebalance if
your situation differs: fewer machines and more sequence, or the reverse.

**12 bits of sequence is 4,096 IDs per machine per millisecond**, which is **4.096 million per machine per
second**. If a machine exhausts it, generation **waits for the next millisecond** — it does not overflow into
the machine field, which would be catastrophic.

**The result sorts by time, because the timestamp occupies the high bits.** Comparing two IDs as integers
compares their timestamps first. That is the entire reason for the field order, and it is why the timestamp
must be first — not first because it is important, but first because **numeric order is lexicographic order on
the bit fields.**

**Now the clock, which is the interesting part.**

**The design assumes time moves forwards, and NTP corrections can step it backwards.** If the clock jumps back
50 ms, the generator produces timestamps it has already used, with a sequence counter that has reset — **and
it will produce duplicate IDs.**

**Three responses, and the right one depends on how far back it jumped.**

**Small step back — a few milliseconds — wait.** Block until the clock catches up to the last timestamp
issued. A few milliseconds of added latency, and correctness preserved.

**Large step back — seconds — refuse.** Throw an error and stop generating. **The machine should be removed
from service rather than produce duplicates**, and a loud failure is enormously better than a silent
collision that will be discovered months later in a support ticket.

**And prevent it: use a monotonic clock where possible, and configure NTP to slew rather than step.** Slewing
means correcting by running the clock slightly fast or slow until it converges, never jumping. **That is one
line of NTP configuration and it removes most of the problem.**

**The last question: where does the machine id come from?**

**Not from a configuration file a human edits**, because two machines will eventually get the same value and
the failure is silent. Three real answers: **ZooKeeper or etcd hands out a lease on startup** — a small
coordination cost paid once per boot rather than once per ID; **derive it from the private IP address**, which
works when the address space maps cleanly to 10 bits; or **use the ordinal from a Kubernetes StatefulSet**,
which is already unique and stable by construction.

**All three are better than a config file**, and saying which one and why is the answer.

---

## 4. The picture

The 64 bits, laid out:

```
  63    62                          22        12                    0
   +----+---------------------------+---------+---------------------+
   | 0  |  timestamp (41 bits)      | machine |  sequence (12 bits) |
   |    |  ms since custom epoch    | 10 bits |                     |
   +----+---------------------------+---------+---------------------+
     ^              ^                    ^               ^
   sign bit    69 years of ms       1,024 machines   4,096 per ms
   always 0                                          per machine
   -> positive

  TIMESTAMP IS FIRST because integer comparison compares high bits
  first. That is the ONLY reason for this order, and it is what makes
  the IDs sort by time.
```

Why a random UUID destroys the index:

```
  SEQUENTIAL IDS (Snowflake)        RANDOM IDS (UUIDv4)

  B-tree, inserting 1..8            B-tree, inserting random values

        [ 4 ]                             [ 4c ]
       /     \                           /      \
   [1 2 3]  [5 6 7 8]               [0a 2f]   [9d f1]
                ^                      ^  ^     ^  ^
        every insert lands       every insert lands in a
        in the RIGHTMOST page    DIFFERENT page, chosen at
        -> that one page stays   random
           in memory, always     -> the whole index must be in
        -> one page written         memory or every insert is a
                                    random disk read + write
                                 -> pages split and fragment

  Measured effect: 2-10x lower insert throughput, and an index
  that is 30-40% larger after fragmentation.
```

The clock going backwards:

```
  time -->
     t=1000ms  |  seq 0,1,2,3        IDs issued
     t=1001ms  |  seq 0,1            IDs issued
     NTP steps the clock back 2 ms
     t=999ms   |  seq 0,1,2  <-- t=999 was ALREADY used with seq 0,1,2
                                DUPLICATE IDs. Silently.

  Defence:
     last_timestamp = 1001
     now = 999
     if now < last_timestamp:
         gap = last_timestamp - now
         if gap <= 5 ms:  sleep until now >= last_timestamp   (wait)
         else:            raise ClockMovedBackwards            (refuse)
```

The sequence exhausting within a millisecond:

```
  within t = 1000ms:
     request 1     -> seq 0
     request 2     -> seq 1
     ...
     request 4096  -> seq 4095
     request 4097  -> sequence field is FULL

  WRONG: let it wrap to 0        -> duplicate of request 1
  WRONG: carry into machine id   -> collides with another machine
  RIGHT: busy-wait until t = 1001ms, then reset seq to 0

  The cap is 4,096 per ms = 4.096 MILLION per second per machine.
  Nothing real hits this. The handling still has to exist.
```

The alternatives, compared:

```
                      size    sortable   coordination   index-friendly
  auto-increment      8 B     yes        every insert   yes
  UUIDv4              16 B    NO         none           NO
  UUIDv7              16 B    yes        none           yes
  Snowflake           8 B     yes        once at boot   yes
  ticket server       8 B     yes        every insert   yes

  Snowflake is the only row with no bad cell.
  UUIDv7 (2024) is the modern near-equal, at twice the size.
```

---

## 5. How it actually works

### The generator

```python
import time, threading

EPOCH = 1704067200000          # 2024-01-01, chosen at launch

TIMESTAMP_BITS, MACHINE_BITS, SEQUENCE_BITS = 41, 10, 12
MAX_MACHINE = (1 << MACHINE_BITS) - 1          # 1023
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1        # 4095
```

**`EPOCH` set to the launch date, not 1970**, is the free fifty years. With a 1970 epoch, 41 bits ran out in
2039; from 2024 it runs to 2093.

```python
class SnowflakeGenerator:
    def __init__(self, machine_id: int) -> None:
        if not 0 <= machine_id <= MAX_MACHINE:
            raise ValueError(f"machine_id must be 0..{MAX_MACHINE}")
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()
```

**The lock is not optional.** Two threads reading `self.sequence` at the same time produce the same ID, and
the whole guarantee is gone. **In Java this is usually `synchronized`; in Go, a mutex.**

Now the generation, which is where the clock is handled:

```python
    def next_id(self) -> int:
        with self.lock:
            now = int(time.time() * 1000)

            if now < self.last_timestamp:              # clock went backwards
                gap = self.last_timestamp - now
                if gap > 5:
                    raise RuntimeError(f"clock moved backwards by {gap}ms")
                while now < self.last_timestamp:       # small: wait it out
                    now = int(time.time() * 1000)
```

**Small step: wait. Large step: refuse.** The threshold is a policy number — five milliseconds is a common
choice — and the important part is that **the large case fails loudly** rather than producing duplicates.

```python
            if now == self.last_timestamp:
                self.sequence = (self.sequence + 1) & MAX_SEQUENCE
                if self.sequence == 0:                 # 4096 used this ms
                    while now <= self.last_timestamp:  # wait for the next ms
                        now = int(time.time() * 1000)
            else:
                self.sequence = 0                      # new millisecond

            self.last_timestamp = now
            return ((now - EPOCH) << (MACHINE_BITS + SEQUENCE_BITS)
                    | self.machine_id << SEQUENCE_BITS
                    | self.sequence)
```

**`& MAX_SEQUENCE` wraps to zero at 4096**, and the `if self.sequence == 0` catches exactly that case and
waits. **Without the wait, the wrap produces a duplicate of the first ID in that millisecond.**

**The final line is three shifts and two ORs** — a few nanoseconds. There is no network call anywhere in this
function, which is the point.

### Reading an ID back

```python
def parse(snowflake_id: int) -> tuple[int, int, int]:
    sequence = snowflake_id & MAX_SEQUENCE
    machine = (snowflake_id >> SEQUENCE_BITS) & MAX_MACHINE
    timestamp = (snowflake_id >> (SEQUENCE_BITS + MACHINE_BITS)) + EPOCH
    return timestamp, machine, sequence
```

**Every ID carries its own creation time and origin machine**, which is genuinely useful in an incident: an ID
in a log tells you when it was created and which machine created it, with no lookup.

**And it is an information leak.** A public ID reveals your creation rate — two IDs a second apart let anyone
compute how many rows you created in between. **Instagram's sequential IDs let people measure their signup
rate for years.** If that matters, expose a hashed or encrypted public ID and keep the Snowflake internal.

### Getting a machine id without a human

```python
def machine_id_from_zookeeper(zk, path: str = "/snowflake/workers") -> int:
    """Ephemeral sequential znode: unique while the process lives."""
    node = zk.create(f"{path}/worker-", ephemeral=True, sequence=True)
    return int(node.rsplit("-", 1)[1]) % (MAX_MACHINE + 1)


def machine_id_from_ip() -> int:
    """Last 10 bits of the private IP. Works when the subnet is small."""
    import socket
    octets = [int(x) for x in socket.gethostbyname(socket.gethostname()).split(".")]
    return ((octets[2] << 8) | octets[3]) & MAX_MACHINE
```

**The ZooKeeper version is correct and adds a dependency at boot.** The IP version has no dependency and
**breaks silently if two subnets share the low ten bits** — `10.0.1.5` and `10.1.1.5` collide. Check the
address plan before choosing it.

**Kubernetes gives you this free:** a StatefulSet pod is named `app-0`, `app-1`, and that ordinal is unique and
stable across restarts. **Parse the hostname.**

### The alternatives, and when each is right

```
UUIDv4        random 128 bits. No coordination, not sortable, index-hostile.
              Right for: client-generated ids, distributed systems with no
              central anything, ids that must reveal nothing.

UUIDv7        48-bit ms timestamp + 74 random bits. Sortable AND uncoordinated.
              Standardised in 2024 (RFC 9562). Twice Snowflake's size and
              needs no machine id at all. The modern default when 16 bytes
              is acceptable.

ticket server one database whose only job is issuing ids, in batches.
              A machine takes 1,000 ids at a time, so the database sees one
              write per thousand ids. Simple, and a single point of failure.

Snowflake     8 bytes, sortable, no per-id coordination. Needs a machine id
              and a well-behaved clock.
```

**Naming UUIDv7 is worth doing**, because it is the genuine modern alternative and it shows you are not just
reciting a 2010 design. **The trade is: UUIDv7 needs no machine id and costs 8 extra bytes per row.**

### Who uses what

```
Twitter/X       Snowflake (the original)
Discord         Snowflake, visible in every message id
Instagram       a Postgres stored procedure: 41-bit ms + 13-bit shard
                + 10-bit per-shard sequence
Sony            "Sonyflake" — 39-bit 10ms units, 16-bit machine, 8-bit seq
                -> 174 years, fewer ids per ms
MongoDB         ObjectId: 12 bytes, 4-byte timestamp + 5 random + 3 counter
```

**Sonyflake is the useful one to mention**, because it shows the field widths are a design choice: it trades
per-millisecond throughput for 174 years of range and 65,536 machines.

---

## 6. The numbers

**The bit budget, and why each field is that wide:**

```
41 bits of milliseconds
  2^41 = 2,199,023,255,552 ms
       = 2,199,023,255 seconds
       = 69.7 years

  from a 1970 epoch: exhausted in 2039  (only 15 years left)
  from a 2024 epoch: exhausted in 2093  (69 years)
  -> the custom epoch is worth 54 years and costs one constant
```

```
10 bits of machine id     2^10 = 1,024 machines
12 bits of sequence       2^12 = 4,096 ids per machine per millisecond
```

**Total throughput:**

```
4,096 per ms per machine
  x 1,000 ms                = 4,096,000 ids/second/machine
  x 1,024 machines          = 4,194,304,000 ids/second

4.2 billion ids per second, from 8 bytes.
```

**Compare that with what anyone needs:**

```
Twitter at peak:  ~10,000 tweets/second
                  -> 0.0002% of one machine's capacity

a busy e-commerce site: 100,000 orders/second at peak
                  -> 2.4% of ONE machine's capacity
```

**Nothing real exhausts a single generator**, and saying that is worth more than the multiplication — it tells
the interviewer you know the sequence field exists for correctness under bursts, not for throughput.

**Storage, which is where UUIDs actually cost money:**

```
1 billion rows

Snowflake (BIGINT, 8 bytes)
  primary key            1,000,000,000 x 8 B   = 8 GB
  3 foreign keys         x 3                   = 24 GB
  4 secondary indexes    (each holds the PK)   = 32 GB
  TOTAL                                        = 64 GB

UUID (16 bytes)
  same layout, doubled                         = 128 GB

difference                                     = 64 GB
```

**And stored as a string, which happens constantly:**

```
UUID as CHAR(36): "550e8400-e29b-41d4-a716-446655440000"
  1,000,000,000 x 36 B x 8 places              = 288 GB

vs 64 GB for BIGINT. 4.5x, and the comparisons are string
comparisons rather than integer comparisons.
```

**The insert throughput difference, which matters more than the storage:**

```
sequential inserts (Snowflake)
  every insert appends to the rightmost B-tree page
  that page is always in memory
  -> ~50,000 inserts/second on ordinary hardware

random inserts (UUIDv4)
  every insert targets a random page
  index is 64 GB, memory is 32 GB
  -> most inserts are a random disk read + a random write
  -> ~5,000-25,000 inserts/second

2-10x slower, and it degrades as the index grows past memory.
```

**That degradation shape is the real problem**: it is fine in testing with a small table and collapses in
production a year later.

**Generation latency:**

```
Snowflake:      3 shifts, 2 ORs, 1 clock read      ~100 nanoseconds
UUIDv4:         16 bytes from a CSPRNG              ~200 nanoseconds
ticket server:  one network round trip              ~500,000 nanoseconds
                (amortised over a batch of 1,000)   ~500 ns per id
database auto-increment: part of the insert         no separate cost,
                                                    but serialises everything
```

**Clock skew, quantified:**

```
NTP with default configuration
  typical offset          1-10 ms
  after a network blip    up to several hundred ms
  a step correction       can be seconds

with `ntpd -x` (slew only, never step)
  the clock is corrected at up to 500 ppm
  -> a 1-second error takes ~33 minutes to correct
  -> never jumps backwards
```

**33 minutes of slightly-wrong time against a possible duplicate ID** is an easy trade, and it is one
configuration flag.

**Sequence exhaustion in practice:**

```
to exhaust 4,096 in one millisecond, a single machine must generate
4.096 million ids per second

a Java service doing this does nothing else — the ids alone saturate
a core. If you are here, the bottleneck is not the id generator.

-> the exhaustion branch runs approximately never, and must still be
   correct, because "approximately never" is where the worst bugs live.
```

---

## 7. The trade-offs

**Sortability against privacy, and this is the real one.** A time-sortable ID makes indexes fast and makes
"the newest fifty" a range scan instead of a sort. **It also publishes your creation rate.** Anyone can create
two objects a minute apart, subtract the IDs, and compute exactly how many you created in between —
competitors have measured signup rates this way for years. **If that matters, keep the Snowflake internal and
expose a hashed public identifier**, and accept the extra lookup.

**Size against coordination.** Snowflake is 8 bytes and needs a unique machine id, which needs ZooKeeper, or
an IP scheme, or Kubernetes ordinals — a small operational dependency at boot. **UUIDv7 is 16 bytes and needs
nothing at all.** At a billion rows with several indexes that is roughly 64 GB of difference, so **the question
is whether 64 GB or the coordination is cheaper for you**, and at smaller scale the answer is usually UUIDv7.

**Waiting against failing on a backwards clock.** Waiting adds latency and preserves correctness; failing takes
the machine out of service. **Both are correct and the threshold between them is a policy number** — the wrong
answer is to do neither and produce duplicates. **And a duplicate ID is close to unrecoverable**, because it is
discovered long after the fact, in data that has already been joined and copied.

**Machine ids from configuration against machine ids from coordination.** A config file is simple and **fails
silently when two machines share a value** — duplicate IDs with no error anywhere. ZooKeeper is correct and
puts a dependency in the boot path, so a ZooKeeper outage stops new machines starting. **Kubernetes ordinals
are the best of both** where they apply, because uniqueness is structural rather than enforced.

**Field widths are a genuine choice, not a constant.** 41/10/12 suits a service with hundreds of machines and
moderate per-machine rates. **Sony chose 39/16/8** — 174 years and 65,536 machines, at 256 IDs per 10 ms — for
a fleet with many small machines. **Being willing to redistribute the bits for the stated constraints is what
distinguishes understanding the design from having memorised it.**

**When would I not build this?** **Below a few thousand writes a second, a database auto-increment is
correct, simpler, and has no clock dependency at all** — and reaching for Snowflake there adds a machine-id
management problem to solve a throughput problem you do not have. **If IDs are generated by clients** — a
mobile app creating rows offline — no server-side scheme works and UUIDs are the answer. **And if 16 bytes is
acceptable, UUIDv7 gives you sortable, uncoordinated IDs with no clock handling and no machine registry**,
which is less code to get wrong.

---

## 8. In the interview

### How it gets asked

- *"Generate unique IDs across a hundred servers. No central counter."* — the standard prompt.
- *"Why not just use UUIDs?"* — always asked, and the index answer is the one they want.
- *"Walk me through the 64 bits."* — say what each field buys.
- *"What happens when the clock goes backwards?"* — the separating question.
- *"How does each machine get its ID?"*
- *"What if a machine generates more than 4,096 in a millisecond?"*

### The first ninety seconds

> "Four requirements, and they pull against each other: **unique with no coordination, sortable by time, small,
> and generated locally with no network call.**
>
> **Sortable is the one people skip, and it is the one that matters most**, because it decides whether the
> database index works.
>
> **I would use a Snowflake ID: 64 bits, four fields.** One unused sign bit so the number stays positive.
> **Forty-one bits of milliseconds** since a custom epoch. **Ten bits of machine id.** **Twelve bits of
> sequence** within that millisecond.
>
> **Each width earns itself.** Forty-one bits of milliseconds is 69 years — and **the epoch is the day we
> launch, not 1970**, which buys back the fifty-four years already spent, from one constant. Ten bits is 1,024
> machines. Twelve bits is 4,096 IDs per machine per millisecond, which is four million a second per machine —
> **nothing real approaches that**, so the field exists for correctness under bursts, not for throughput.
>
> **The timestamp is in the high bits and that is the whole point of the layout**, because comparing two IDs as
> integers compares the timestamps first. The IDs sort by time for free.
>
> **Why not UUIDs, which is the obvious alternative.** Two reasons. **They are sixteen bytes rather than
> eight**, and at a billion rows with three foreign keys and four indexes that is about sixty-four gigabytes of
> difference. **And version 4 is random, which destroys the B-tree index** — every insert lands in a different
> page, so instead of always appending to one hot page in memory, the database does a random read and a random
> write per insert. **Two to ten times slower on inserts**, and it gets worse as the index outgrows memory,
> which means it looks fine in testing and collapses a year into production.
>
> **The part I would want to talk about is the clock**, because the whole design assumes time moves forwards
> and NTP can step it backwards. **If that happens, the generator reissues timestamps it has already used with
> a reset sequence, and produces duplicates silently.**
>
> **Generation is three shifts and two ORs — about a hundred nanoseconds, no network call.** And I would ask
> one thing before finalising: **are these IDs public?** Because a time-sortable ID publishes the creation
> rate, and if that is sensitive I would keep the Snowflake internal and expose a hashed identifier."

### The follow-ups

**"Why not just use UUIDs?"**

> "They are correct — the uniqueness is genuinely fine — and they cost in two ways, one obvious and one that
> surprises people.
>
> **The obvious one: sixteen bytes against eight.** That sounds negligible per row and it multiplies. A billion
> rows, a primary key, three foreign keys and four secondary indexes — and in most databases every secondary
> index entry also stores the primary key. **That is eight copies of the identifier per row: sixty-four
> gigabytes for BIGINT, a hundred and twenty-eight for UUID.** And if it is stored as a `CHAR(36)` string,
> which happens constantly, it is two hundred and eighty-eight gigabytes and every comparison is a string
> comparison.
>
> **The one that actually hurts: version 4 UUIDs are random, and that destroys the index.**
>
> A B-tree with sequential keys means every insert goes into the rightmost page. **That page is always in
> memory, so an insert is one page write and nothing else.** With random keys, every insert targets a
> different page chosen uniformly across the whole index — so unless the entire index fits in memory, **each
> insert is a random disk read followed by a random write.** Pages split constantly and the index fragments,
> typically ending up thirty to forty percent larger.
>
> **Measured, that is two to ten times fewer inserts per second**, and the shape of the degradation is what
> makes it dangerous: **it is invisible until the index outgrows memory.** It tests fine and fails in
> production a year later, and by then the ID type is in every table.
>
> **Where UUIDs are right:** IDs generated on a client, offline, with no server involved. IDs that must reveal
> nothing about creation time or volume. Systems with genuinely no coordination available anywhere.
>
> **And I would name UUIDv7**, standardised in 2024, which is a 48-bit millisecond timestamp followed by
> random bits. **Sortable, index-friendly, and needs no machine id at all** — so it fixes the index problem and
> keeps the zero-coordination property. **It is still sixteen bytes.** If the extra eight bytes per reference
> is acceptable, UUIDv7 is less machinery to get wrong than Snowflake, and I would genuinely consider it
> first."

**"What happens when the clock goes backwards?"**

> "That is the failure mode the whole design rests on, so let me say exactly what breaks and then what I do.
>
> **What breaks: duplicates, silently.** The generator remembers the last timestamp it issued. If the clock
> jumps back fifty milliseconds, it starts producing timestamps it has already used, and the sequence counter
> resets to zero because the timestamp looks new. **So it reissues IDs it has already handed out**, with no
> error anywhere, and the collision is discovered months later in data that has already been joined and
> copied. **That is close to unrecoverable.**
>
> **Why it happens: NTP.** A machine whose clock has drifted gets corrected, and the default correction for a
> large offset is a *step* — an instantaneous jump. Backwards, if the clock was fast. **Virtual machines are
> worse**, because live migration and host suspension both disturb the guest clock.
>
> **Three things, and I would do all three.**
>
> **Prevent it: configure NTP to slew, never step.** Slewing corrects by running the clock slightly fast or
> slow until it converges — up to about 500 parts per million, so a one-second error takes about half an hour
> to fix. **Slow, and it never goes backwards.** That is one flag and it removes most of the problem.
>
> **Detect and wait, for small steps.** The generator compares the current time with the last timestamp it
> issued. If time went back by a few milliseconds, **block until the clock catches up.** A few milliseconds of
> latency, correctness preserved.
>
> **Detect and refuse, for large ones.** If it went back by more than the threshold — a few milliseconds — the
> generator throws and stops issuing IDs. **That machine should be pulled out of the load balancer.** A loud
> failure on one machine is dramatically better than silent duplicates across the fleet.
>
> **And where I can, use the monotonic clock** — `CLOCK_MONOTONIC`, which never goes backwards — anchored to
> one wall-clock reading at startup. That gives me a timestamp that cannot regress within a process, though it
> does not survive a restart, so the on-disk last-timestamp check still has to exist."

**"How does each machine get its ID, and what if two get the same one?"**

> "If two machines share a machine id they will produce identical IDs whenever they generate in the same
> millisecond with the same sequence number — **and nothing reports it.** So the assignment mechanism is a
> correctness mechanism, not configuration.
>
> **What I would not do is put it in a config file or an environment variable**, because a copy-pasted deploy
> config, a scaled-up instance group, or a rolled-back change will eventually produce two machines with the
> same number, and there is no error to notice.
>
> **Three mechanisms I would actually use.**
>
> **ZooKeeper or etcd, with an ephemeral sequential node.** On startup the process creates a node and gets back
> a unique number. **Ephemeral means it disappears when the process dies**, so the id returns to the pool.
> Correct, and it puts a dependency in the boot path — a ZooKeeper outage means no new machines can start,
> though running ones are unaffected. **Worth stating explicitly, because it is a real availability cost.**
>
> **Derive it from the private IP address**, taking the low ten bits. No dependency at all, and it works when
> the address plan guarantees uniqueness in those bits. **It fails silently when two subnets share them** —
> `10.0.1.5` and `10.1.1.5` give the same ten bits. So I would only use it after checking the network plan,
> and I would log the derived id at startup so a collision is at least visible in the logs.
>
> **Kubernetes StatefulSet ordinals**, where they apply, are the best answer. A pod is `service-0`,
> `service-1`, and the ordinal is unique and stable across restarts by construction. **No extra system, no
> derivation that can collide** — parse the hostname.
>
> **Whichever I use, I would add detection:** each generator writes its machine id and a heartbeat to a shared
> store, and an alert fires if two heartbeats claim the same id. **It does not prevent the collision, and it
> turns a silent corruption into a page**, which is the difference that matters."

### The model answer

*"Design an ID generator for a social platform: two hundred application servers, ten thousand new objects a
second at peak, IDs appear in public URLs, and they will be the primary key of every table."*

> "Three things in that prompt change the design, so let me take them in order: **two hundred servers, IDs in
> public URLs, and primary key of every table.**
>
> **Primary key of every table means index behaviour dominates everything else**, so I am ruling out random
> IDs immediately. A UUIDv4 primary key at this scale means every insert lands in a random B-tree page — two
> to ten times slower on inserts once the index outgrows memory, and it degrades invisibly as the table grows.
>
> **So: Snowflake, 64 bits.** Sign bit, 41 bits of milliseconds from a 2024 epoch, 10 bits of machine, 12 bits
> of sequence.
>
> **The custom epoch is worth saying out loud** — from 1970, 41 bits runs out in 2039; from launch, it runs to
> 2093. One constant, fifty-four years.
>
> **The field widths for two hundred servers.** Ten bits gives 1,024 machines, so there is five times headroom
> — comfortable, and I would keep it rather than shrinking it, because machine counts grow and the sequence
> field has enormous slack. **Twelve bits is 4,096 IDs per machine per millisecond, four million a second per
> machine.** At ten thousand objects a second across two hundred servers, that is fifty per server per second
> — **about a thousandth of one percent of one machine's capacity.** The sequence field is there for
> correctness during a burst, not for throughput, and I would say that rather than presenting the four-billion
> figure as if it were needed.
>
> **Machine ids: Kubernetes StatefulSet ordinals if the platform is on Kubernetes**, because uniqueness is
> structural. Otherwise ZooKeeper ephemeral sequential nodes, accepting that a ZooKeeper outage blocks new
> machines from starting. **Not a config file** — two machines with the same id produce duplicate primary keys
> and nothing reports it.
>
> **Now the part the prompt forces, which is that IDs appear in public URLs.**
>
> **A Snowflake ID publishes its creation time and the creation rate.** Anyone can create two objects a minute
> apart, subtract, divide by the sequence width, and compute how many objects the platform created in between.
> **Instagram's signup rate was measurable this way for years.** For a social platform that is a genuine
> business leak.
>
> **So I would separate the two identifiers.** The Snowflake stays internal — primary key, foreign keys,
> indexes, logs. **The public URL carries a different, opaque identifier**: either a random short code stored
> alongside the row, or the Snowflake encrypted with a block cipher, which is reversible and needs no extra
> column. **The encrypted form is nicer** because there is no second uniqueness problem to solve and no extra
> index, at the cost of a cipher operation per request.
>
> **Clock handling, which is the correctness core.** NTP configured to slew rather than step, so the clock
> never jumps backwards. In the generator: if time has gone back a few milliseconds, wait; if it has gone back
> further, throw and take the machine out of service. **And the last issued timestamp persisted, so a restart
> after a clock jump does not reissue.**
>
> **Sizing.** Ten thousand a second is 864 million objects a day, so 41 bits of millisecond is untouched by
> volume. At a billion rows with three foreign keys and four indexes, BIGINT costs about 64 GB against 128 GB
> for UUID — **and the insert throughput difference matters more than the storage.**
>
> **What I would monitor:** duplicate machine ids, via a heartbeat table with an alert on collision; clock
> offset per machine, alerting well before the refuse threshold; and the rate of sequence-exhaustion waits,
> which should be zero and tells me about bursts if it is not.
>
> **And the honest alternative I would put on the table: UUIDv7.** Sortable, index-friendly, no machine
> registry, no clock-skew handling, standardised. **It costs eight extra bytes per reference and removes two
> entire classes of operational failure.** At two hundred servers and ten thousand a second I would genuinely
> consider it the safer choice — **and I would still need the separate public identifier**, because UUIDv7
> leaks creation time too."

---

## 9. Recall card

**Snowflake, 64 bits: 1 sign + 41 ms + 10 machine + 12 sequence.** Timestamp in the **high** bits, which is the
only reason the IDs sort by time — integer comparison compares high bits first. **Custom epoch at launch, not
1970**: 69 years from launch instead of exhausting in 2039.

**41 bits = 69.7 years. 10 bits = 1,024 machines. 12 bits = 4,096/ms = 4.1M/s per machine** — nothing real
approaches it, so the sequence field is for burst correctness, not throughput. On exhaustion, **wait for the
next millisecond**; never wrap, never carry into the machine field.

**Why not UUIDv4: 16 bytes not 8** (~64 GB extra at 1B rows × 8 index copies) **and random keys destroy the
B-tree** — every insert hits a different page instead of the hot rightmost one, **2–10× fewer inserts/second**,
degrading invisibly as the index outgrows memory. **UUIDv7 (RFC 9562, 2024) fixes sortability** and needs no
machine id — the real modern alternative at 16 bytes.

**Clock going backwards is the failure mode:** reissued timestamps with a reset sequence = silent duplicates.
**Slew NTP, never step; wait on a small step; refuse loudly on a large one**, and persist the last timestamp
across restarts.

**Machine ids from ZooKeeper ephemeral sequential nodes, the private IP's low bits, or Kubernetes StatefulSet
ordinals — never a config file**, because two machines sharing an id produce duplicates with no error.
**Sortable IDs leak your creation rate**, so keep the Snowflake internal and expose an encrypted or random
public identifier.
