---
day: 116
track: system-design
title: "Eventual consistency in practice"
phase: "Distributed systems core"
status: written
---

# Day 116 · System Design — Eventual consistency in practice

**After today you can:** You can design a feature that stays usable while the data is briefly stale.

**The interviewer asks it as:** *The like count is wrong for two seconds. Is that acceptable?*

---

## 1. What this is, and why they ask it

[Yesterday](../day-115-heapq/README.md) was the ladder of consistency models. Today is the practical
half: **how do you build a product on top of the weak end of it, so that users do not notice — or, when
they do, do not mind?**

Three sentences. The answer is not a technique but a discipline: **decide, per piece of data, what a user
would see and how bad it is**, and then choose from a small set of patterns — show the state honestly,
predict it optimistically, or route around the staleness. The systems that do this well take an idea from
outside software entirely: **banks, couriers and ticket offices have always been eventually consistent,
and they cope by making the pending state visible** rather than pretending it does not exist. And the
convergence machinery underneath — read repair, anti-entropy, hinted handoff — is worth knowing because
"eventually" has a shape and you should be able to say what it is.

They ask *"is two seconds acceptable?"* because it is a product question wearing an engineering costume,
and the right answer starts by asking **what happens in those two seconds**. A candidate who says "yes,
eventual consistency is fine" has not asked; a candidate who says "for a like count yes, and here is how I
would make the user's *own* like feel instant anyway" has designed something.

---

## 2. The story

Mariappan had banked at the same branch for thirty-one years and he still went in on Fridays, and the
thing he had never once complained about was the cheque.

He would hand over a cheque for, say, eleven thousand rupees. The clerk stamped it, entered it, and gave
him a slip. And the slip said the amount, and it said — printed, in the same size as everything else —
that it would be available on Tuesday.

His account, if he checked it that evening, showed two numbers. The balance, which had gone up by eleven
thousand. And below it, in the same statement, an amount marked as not yet cleared.

His nephew, who had started using a phone application for everything, found this ridiculous. He said the
money is either there or it is not.

Mariappan said that was exactly the point, and it was not there yet, and the bank was telling him so.
The cheque had to go to the other bank, and the other bank had to agree, and that took until Tuesday. What
would his nephew prefer — that they hide it, and let him spend money that might come back?

The nephew said they could just refuse to show it at all until Tuesday.

Mariappan said they had tried that, before his time, and people came in on Saturday convinced their cheque
had been lost.

There were two other things about the arrangement that he pointed out, and both of them had taken the
bank a long time to arrive at.

The first was that the branch let him **spend against it in small amounts** — up to two thousand rupees —
even before Tuesday. Not the whole eleven. Because for two thousand they were confident enough, and if the
cheque did bounce they could take it back out of the account without much trouble. Above that they made
him wait.

The second was what happened when a cheque did bounce, which had happened to him twice in thirty-one
years. The bank did not pretend it had never gone in. They **reversed it** — a separate line on the
statement, with the date, saying the amount had been taken back out and why. Both entries stayed.

He said the whole system worked because nobody ever claimed to know something they did not know. The slip
said Tuesday. The statement said uncleared. The reversal said reversed.

---

## 3. The idea in plain English

The bank is an eventually consistent system that has been running for two centuries, and every one of its
conventions is a pattern you should copy.

- The cheque taking until Tuesday is **replication lag**, made explicit.
- "Available on Tuesday" on the slip is **showing the pending state** rather than hiding it.
- The uncleared line on the statement is **surfacing the uncertainty in the data model**.
- Spending up to two thousand is **bounded optimism** — act early where the downside is small.
- The reversal line is a **compensating action**, not a deletion.
- "Nobody ever claimed to know something they did not know" is the whole design principle.

### The first question is always the same

> **What does a user see during the window, and how bad is it?**

Not "is eventual consistency acceptable" in the abstract. The answer depends entirely on **which datum**
and **which user**.

```
 a like count off by one for 2 s, seen by a stranger        invisible
 a like count that does not move when YOU tap it            a BUG, and reported
 a follower count off by three for 10 s                     invisible
 a bank balance off by ₹11,000 for 2 s                      terrifying
 a seat marked free that was sold 2 s ago                   a double booking
```

**The same two seconds is unnoticeable, annoying, or unacceptable depending on the datum.** So the
question is never answered at the system level.

### The rule that carries most of it

> **Cache — and replicate — the DISPLAY. Never the DECISION.**

```
 SHOWING "12 left in stock"    stale is fine; it is information
 DECIDING whether to accept    must be current; it is a commitment
   the order
```

**Every one of the patterns below is an application of that line.** It is the same rule as
[caching](../day-101-bfs-level-order/README.md), and it generalises to every weakly consistent system.

### The four patterns

**1 — Optimistic UI: predict the result and show it immediately.**

The user taps *like*. You increment the number on their screen **before the server replies**, because you
are almost certain what the answer will be.

```
 tap -> number changes instantly, locally
     -> request sent in the background
     -> success:  nothing further happens, the user never knew
     -> failure:  revert, and say why
```

**This makes read-your-writes a client-side problem rather than a server-side one**, which is enormously
cheaper: no leader routing, no version tokens, no extra load. **It is the single highest-value pattern
here.**

Its limit is the failure case: **you must be able to revert visibly and honestly.** Optimistically showing
a payment as complete is not acceptable, because there is no good way to un-show it.

**2 — Show the pending state honestly.**

Mariappan's slip. When you cannot know yet, **say so in the interface** rather than showing a value that
might change.

```
 "Processing"        a transfer that has not settled
 "Uploading"         a photo not yet replicated
 "Pending"           an order not yet confirmed
 "Last updated 30s ago"   a dashboard
```

**Users tolerate uncertainty they can see and are angry about uncertainty they discover.** That is the
whole lesson from the bank, and it is a product decision as much as an engineering one.

**3 — Route around the staleness for the affected user.**

From [day 105](../day-105-lowest-common-ancestor/README.md): send a user's reads to the leader for a
window after they write, or only for the objects they touched, or carry a version token.

**Use this when the optimistic prediction is not safe** — when the server may legitimately reject or
transform what the user did.

**4 — Compensate rather than prevent.**

The bank's reversal. Instead of guaranteeing that a bad outcome cannot happen, **allow it and have a
defined correction.**

```
 an airline oversells a flight        -> compensation at the gate
 two people order the last item       -> one is refunded and apologised to
 a payment is double-charged          -> automatic reversal within 24 hours
```

**This is how nearly all commerce works**, and it is often far cheaper than the coordination required to
prevent the case. **The rule for choosing: compensate when the correction is cheaper than the
coordination.** Overselling a hotel room is; overselling a concert seat that costs you a lawsuit is not.

### Bounded optimism, which is the bank's cleverest move

Mariappan spending two thousand of an eleven-thousand cheque. **You do not have to choose between fully
trusting the stale value and fully refusing.**

```
 the risk is small       act now, reconcile later
 the risk is large       wait for confirmation

 examples:
   a small purchase on a card with a stale balance    -> approve offline
   a large one                                        -> require authorisation
   a coupon redeemed twice in a race                  -> allow it, absorb the loss
   the last ticket to a sold-out show                 -> serialise it
```

**Card networks do exactly this**: terminals have an offline floor limit, below which they approve without
contacting the bank at all. The stale answer is accepted because the exposure is bounded.

### How convergence actually happens

"Eventually" is not magic, and there are three mechanisms. **Naming them is what turns a vague answer into
a specific one.**

**Read repair.** When a read touches several replicas and they disagree, the coordinator returns the
newest value **and writes it back** to the stale ones. Free convergence for anything that gets read.

```
 -> hot keys converge in milliseconds
 -> cold keys are never repaired this way
```

**Anti-entropy.** A background process where replicas compare and exchange what they lack. To avoid
shipping everything, they compare **Merkle trees** — a hash tree over the key ranges, so two replicas can
find exactly which ranges differ in `O(log n)` exchanges instead of comparing every key.

```
 -> runs every few minutes to hours
 -> this is what converges the COLD keys
```

**Hinted handoff.** If a replica is down, another node accepts the write **on its behalf** and holds a
hint; when the node returns, the hint is replayed.

```
 -> keeps writes available during a short outage
 -> and hints are usually kept for a bounded time only, after which
    anti-entropy has to do the work
```

**So the honest answer to "how long is eventually?"**:

```
 a key read often                milliseconds (read repair)
 a key rarely read               minutes to hours (anti-entropy interval)
 a replica that was down         until hinted handoff replays, or anti-entropy
 a key never read, on a replica
   that missed the write and the
   hint expired                  until the next anti-entropy pass — which is
                                 why anti-entropy exists at all
```

### What to make eventual, and what not to

```
 SAFE TO BE EVENTUAL             MUST BE STRONG
 like/view/follower counts       account balances at the moment of a transfer
 recommendations                 stock at the point of purchase
 search indexes                  seat and ticket allocation
 analytics dashboards            unique constraints (usernames, emails)
 "who is online"                 permission checks
 feed ordering                   anything a user cannot undo
 comment counts                  anything with legal or financial consequence

 THE TEST: if this is wrong for two seconds, can the mistake be
           corrected afterwards without anyone being harmed?
```

**Counters deserve a special note**, because they are the canonical eventual datum and they are almost
always implemented wrong the first time: a read-modify-write of a shared counter is a
[lost update](../day-095-n-queens/README.md) under concurrency. The right answers are an **atomic
increment** in the store, or a **per-replica counter summed on read** — which is a CRDT and converges
without coordination.

---

## 4. The picture

The bank statement, which is the design pattern.

```
 ┌────────────────────────────────────────────────┐
 │  Balance                          ₹ 47,300     │   ← the optimistic number
 │  Of which uncleared               ₹ 11,000     │   ← the HONEST caveat
 │  Available now                    ₹ 36,300     │   ← what you can actually use
 │                                                │
 │  12 Sep  Cheque 447812   +11,000   UNCLEARED   │   ← the pending state, VISIBLE
 │  15 Sep  Cheque 447812   -11,000   RETURNED    │   ← a COMPENSATING entry,
 │                                                │      not a deletion
 └────────────────────────────────────────────────┘

 THREE numbers instead of one, because three different questions have
 three different answers — and the system never claims to know something
 it does not know.
```

The four patterns, and when each applies:

```
 1. OPTIMISTIC UI              user taps LIKE
                                   │
                     ┌─────────────┴──────────────┐
                     ▼                            ▼
              UI updates NOW              request in flight
              (count 41 -> 42)                    │
                                        ┌─────────┴─────────┐
                                     success              failure
                                        │                    │
                                   do nothing          REVERT + explain
                                   (user never knew)
    -> makes read-your-writes a CLIENT problem. Cheapest fix there is.
    -> limit: you must be able to revert HONESTLY. Never for payments.

 2. SHOW THE PENDING STATE     "Processing…"  "Uploading…"  "Updated 30s ago"
    -> users tolerate uncertainty they can SEE, and resent uncertainty
       they DISCOVER

 3. ROUTE AROUND IT            this user's reads -> the leader, for 30 s
    -> when optimism is not safe because the server may reject or transform

 4. COMPENSATE                 allow the bad outcome, define the correction
    -> airlines oversell; the correction is cheaper than the coordination
```

Bounded optimism — the middle position:

```
 exposure
    ▲
    │  ₹11,000 cheque   ████████  WAIT for clearance
    │
    │  ₹2,000 spend     ██        ACT NOW, reconcile later
    │
    │  a like           ▪         ACT NOW, and never even check
    └──────────────────────────────────────────────►
                                      confidence in the stale value

 CARD NETWORKS DO EXACTLY THIS: an offline floor limit, below which the
 terminal approves without contacting the bank at all.
 -> you do NOT have to choose between fully trusting stale data
    and fully refusing.
```

How convergence happens, and how long it takes:

```
 WRITE arrives at 2 of 3 replicas
        │
        ├─ replica C missed it
        │
   ┌────┴──────────────────────────────────────────────┐
   │                                                    │
 READ REPAIR                                    ANTI-ENTROPY
 a read touches A, B, C, sees the               a background pass compares
 disagreement, returns the newest,              MERKLE TREES to find which
 and WRITES IT BACK to C                        RANGES differ in O(log n)
   -> milliseconds, for HOT keys                exchanges, then syncs them
   -> never happens for cold keys                 -> minutes to hours
                                                   -> this is what fixes COLD keys

 HINTED HANDOFF
 C was DOWN, so B accepted the write on its behalf and kept a hint;
 when C returns, B replays it
   -> keeps writes available during a short outage
   -> hints expire, after which anti-entropy has to do the work

 SO "EVENTUALLY" IS:
   milliseconds   for a frequently read key
   minutes-hours  for a rarely read one
   never          for a key nobody reads on a replica that missed the write
                  and whose hint expired — until the next anti-entropy pass
```

The decision, per datum:

```
 "If this value is wrong for two seconds, what happens?"

  nobody can tell            ────────► EVENTUAL. Do nothing.
    (like counts, recommendations)

  the USER who changed it                OPTIMISTIC UI, or route their
  can tell                   ────────►   reads to the leader for 30 s
    (their own post, their own profile)

  two users can get the                  LINEARIZABLE. No choice.
  same thing                 ────────►   (seats, stock, usernames)

  money or law is involved   ────────►   LINEARIZABLE, or COMPENSATE with
                                         a defined, auditable correction
```

---

## 5. How it actually works

### Designing a counter that is eventually consistent and correct

The canonical case, and the naive version is wrong:

```python
    count = db.get(key)                     # read
    db.set(key, count + 1)                  # modify-write  -> LOST UPDATE
```

**Three correct options**, in increasing order of scale:

```
 1. ATOMIC INCREMENT in the store        Redis INCR, DynamoDB ADD
    -> correct, and the counter is a single hot key

 2. PER-REPLICA COUNTERS, summed on read (a G-counter CRDT)
    -> each node counts its own increments; the value is the sum
    -> converges with no coordination at all

 3. SHARDED counters
    -> increment one of N sub-counters at random; sum on read
    -> spreads the write load; the read costs N lookups
```

**Option 2 is the one worth naming**, because it explains why counters are the textbook CRDT: addition is
commutative and associative, so order does not matter and conflicts cannot occur.

### Making a write idempotent so retries are safe

From [day 113](../day-113-the-heap/README.md): at-least-once delivery plus idempotent processing gives an
exactly-once **effect**.

```
 the client generates a key per logical operation
 the server records the key with the result
 a repeat returns the stored result instead of acting again
```

**In an eventually consistent store the idempotency check is itself eventually consistent**, which is a
real subtlety: two replicas may not yet know about each other's record of the same key. **The usual answer
is to make the idempotency store strongly consistent even when the data store is not** — it is small, it is
written once, and the cost is bounded.

### Handling the failure of an optimistic update

```
 1. apply locally and show it
 2. send the request
 3. on failure:
      revert the local change
      TELL the user what happened, specifically
      offer the action again
 4. never leave the two states diverged silently
```

**The failure path is the whole design.** An optimistic UI without a considered revert is worse than no
optimism, because the user believes something that is not true and finds out later.

### Measuring convergence, so you can talk about it

```
 write a sentinel value on the leader with a timestamp
 read it from every replica on a schedule
 record the delay until each one has it
 alert on the p99 rather than the mean
```

**"How stale is our data?" should be a graph, not an opinion** — and it is the same heartbeat technique as
measuring [replication lag](../day-105-lowest-common-ancestor/README.md).

### What real systems do

- **DynamoDB and Cassandra** implement all three convergence mechanisms — read repair, anti-entropy with
  Merkle trees, and hinted handoff — and the Dynamo paper is where the vocabulary comes from.
- **Amazon's shopping cart** is the canonical worked example: divergent carts are **unioned**, so a deleted
  item can reappear. **Deliberately** — a resurrected item annoys; a lost item costs a sale.
- **Twitter's like and retweet counts** are eventually consistent and shown optimistically to the user who
  tapped, which is why *your* like always feels instant even though the global count lags.
- **Airlines oversell** systematically, because compensation at the gate is far cheaper than the
  coordination required to guarantee it never happens.
- **Card terminals** approve offline below a floor limit, which is bounded optimism in a system that
  predates computers.
- **Google Docs and Figma** use CRDTs or operational transformation, because the requirement is that
  everyone converges and nobody's keystroke is lost — a merge problem rather than an ordering one.

---

## 6. The numbers

### How long "eventually" actually is

```
 mechanism           typical convergence
 -----------------   ---------------------------------
 read repair         milliseconds — but ONLY for keys that get read
 hinted handoff      seconds after the node returns
 anti-entropy        minutes to hours (the scheduled interval)
 no mechanism fires  indefinite
```

```
 a hot key (read 1,000×/s)     converges in milliseconds
 a cold key (read once a week) converges at the next anti-entropy pass
```

**So the distribution is bimodal**, which is worth saying: popular data is almost always fresh, and the
long tail is exactly the data nobody is looking at.

### The window in which a user can notice

```
 replication lag, healthy      1-50 ms
 replication lag, heavy load   100 ms - seconds
 during a bulk job             seconds to MINUTES

 P(a user sees stale data) = P(they read within the lag window)

 a random read, lag 50 ms, one read per minute
   -> ~0.00008 probability. Invisible.

 a read triggered BY the write (the UI reloading)
   -> lands inside the window essentially ALWAYS
```

**That asymmetry is the entire reason read-your-writes is the reported bug and general staleness is not.**

### What each fix costs

```
 optimistic UI              zero server cost; a client change
                            -> the highest-value pattern here

 pending-state UI           zero server cost; a data-model and design change

 leader routing for 30 s    ~10-15% of a user's reads return to the leader

 leader routing, object-based  ~2-5%

 version tokens             a token on every request; the store must expose
                            a comparable position

 strong consistency         2x cost in DynamoDB, and 5-150 ms of latency
```

**The two cheapest patterns cost nothing on the server at all**, which is why they should be considered
first.

### Compensation economics

```
 an airline: overselling by 3% and compensating
   cost of compensation     ~₹15,000 per bumped passenger
   frequency                ~1 in 2,000 passengers
   expected cost            ~₹7.50 per passenger
   revenue from the extra
     seats sold             ~₹300 per passenger

 -> compensating is ~40x cheaper than the empty seats that guaranteeing
    would cost
```

**That arithmetic is the argument**, and it generalises: **compensate when the expected cost of the
correction is below the cost of the coordination.**

### Counter approaches

```
 1,000,000 increments/second on one counter

 read-modify-write        WRONG — lost updates under any concurrency
 atomic INCR (Redis)      correct; one hot key, ~100,000 ops/s per instance
                          -> needs sharding above that
 sharded counter, 100     10,000 ops/s per shard; a read costs 100 lookups
 per-replica CRDT counter each node counts locally; the read sums N values
                          -> no coordination at all
```

### Merkle tree comparison

```
 comparing 1,000,000 keys between two replicas

 key by key           1,000,000 exchanges
 Merkle tree          ~20 exchanges to locate a differing range,
                      then only that range is synced

 -> O(log n) to find where they differ, instead of O(n)
```

**That is why anti-entropy is affordable at all**, and it is the same idea as a hash of a hash of a hash.

---

## 7. The trade-offs

### Optimistic UI trades honesty for latency, and needs a revert

**It is the cheapest and best pattern for the common case**, and it fails badly when the revert is
awkward. Never optimistically confirm a payment, a booking, or anything with a receipt — because there is
no graceful way to un-tell someone.

### Showing the pending state costs product complexity

Three states — done, pending, failed — instead of one. Every screen and every notification has to handle
all three, and somebody has to design what "pending" looks like.

**The bank's answer is that it is worth it**, because the alternative — hiding the uncertainty — produces
users who discover it and lose trust. **I would show the pending state whenever the window is long enough
for a user to act during it.**

### Compensation trades a guarantee for an occasional apology

**Cheaper than coordination when the correction is cheap and the case is rare.** It stops being acceptable
when the correction is expensive, when the harm cannot be undone, or when it is illegal.

**And it has a hidden cost people miss:** a compensating action needs a whole workflow — detection,
notification, refund, audit — and building that properly is not free. It is often more engineering than
the coordination it replaced, and worth it anyway because it degrades better.

### Eventual consistency without a conflict strategy is not a design

From [yesterday](../day-115-heapq/README.md): last-write-wins silently loses data and, with clock skew,
may keep the older write. **Choosing eventual means choosing one of last-write-wins, version vectors,
CRDTs, or an application merge** — and saying which.

### Where this approach breaks

- **Anything a user cannot undo.** A sent message, a published post, a completed payment. Optimism there
  is a lie you cannot retract.
- **Anything with a legal or financial audit requirement**, where "we corrected it later" is not an
  acceptable answer.
- **Chains of dependent eventual operations.** One stale read feeding another compounds, and the window
  becomes unbounded.
- **Cold data.** Read repair never fires, so convergence waits on anti-entropy — and the data nobody looks
  at is exactly the data that stays wrong longest, which is a poor property when somebody finally looks.
- **The idempotency store itself being eventually consistent**, which quietly reintroduces duplicates.

---

## 8. In the interview

### How it gets asked

- The direct one: *"The like count is wrong for two seconds. Is that acceptable?"*
- The follow-up: *"How would you make the user's own action feel instant?"*
- The design one: *"How do you build a feature that works while the data is stale?"*
- The mechanism one: *"How long is 'eventually', actually?"*
- The hard one: *"What would you never make eventually consistent?"*

### What to say out loud, in the first ninety seconds

1. **Turn it into the right question.** "It depends what a user sees in those two seconds, and for which
   user. A like count off by one, seen by a stranger, is invisible. The same count not moving when *you*
   tap it is a bug people report."
2. **Give the rule.** "The rule I use is: the **display** may be stale, the **decision** may not. Showing
   'twelve in stock' can be seconds old; deciding whether to accept the order cannot."
3. **Name the cheapest fix first.** "For the user's own action I would use an **optimistic UI** — update
   the number locally the moment they tap, send the request in the background, and revert visibly if it
   fails. That makes read-your-writes a client-side problem, which costs nothing on the server."
4. **Name the honest fallback.** "Where optimism is not safe, I would **show the pending state** — the way
   a bank shows an uncleared cheque. Users tolerate uncertainty they can see and resent uncertainty they
   discover."
5. **Say what "eventually" actually means.** "Convergence comes from read repair for hot keys —
   milliseconds — and anti-entropy for cold ones, which is minutes to hours. So the distribution is
   bimodal: popular data is nearly always fresh and the long tail is what nobody is looking at."
6. **Draw the line.** "And I would not make anything eventual where two users can get the same thing, or
   where the mistake cannot be corrected afterwards without harming someone."

### The follow-ups

**"How would you make the user's own action feel instant?"**
"**Optimistic UI**, and it is the highest-value pattern in this whole area because it costs nothing on the
server. When they tap like, I increment the number on their screen immediately — before the request even
leaves — because I am almost certain what the answer will be. The request goes in the background; on
success nothing further happens and they never knew there was a request; on failure I **revert visibly and
say why**. The reason it matters so much is that it converts read-your-writes from a server problem into a
client one: no leader routing, no version tokens, no extra database load, and it fixes the single most
reported anomaly in this phase. Its limit is the failure path — you must be able to revert **honestly**,
so I would never do it for a payment or a booking confirmation, where there is no graceful way to
un-tell someone. And I would build the revert first, because an optimistic UI without a considered failure
path is worse than none: the user believes something untrue and finds out later."

**"How long is 'eventually', actually?"**
"It has a shape, and there are three mechanisms with very different speeds. **Read repair**: when a read
touches several replicas and they disagree, the coordinator returns the newest value and writes it back to
the stale ones — milliseconds, and it only ever fires for keys that get **read**. **Hinted handoff**: if a
replica was down when the write happened, another node accepted it on that node's behalf and replays it
when it returns — seconds after recovery, and hints expire. **Anti-entropy**: a scheduled background pass
where replicas compare **Merkle trees** to find which key ranges differ — `O(log n)` exchanges instead of
comparing a million keys — and then sync only those ranges. That runs every few minutes to hours. So the
distribution is **bimodal**: a hot key converges in milliseconds because read repair fires constantly, and
a cold key waits for the next anti-entropy pass. Which has an uncomfortable corollary — the data that stays
wrong longest is exactly the data nobody is looking at, right up until somebody does."

**"What would you never make eventually consistent?"**
"Anything where **two users can get the same thing**, and anything where **the mistake cannot be corrected
afterwards without harming someone**. Concretely: seat and ticket allocation, stock at the moment of
purchase, unique constraints like usernames and email addresses, permission checks, and account balances at
the moment of a transfer. In all of those the failure is not staleness — it is two people holding the same
seat, and no amount of later convergence undoes that. The test I actually apply is: *if this value is wrong
for two seconds, can the mistake be corrected afterwards without anyone being harmed?* If yes, eventual is
fine and probably cheaper. If no, it needs to be linearizable, and I would rather pay the latency than
design an apology workflow."

**"An airline oversells flights. Isn't that just a bug?"**
"No — it is the most instructive example in the whole topic, because it is a deliberate choice with
arithmetic behind it. Guaranteeing a seat for every ticket means coordinating perfectly and flying with
empty seats when people do not turn up. Overselling by around three percent and compensating the
occasional bumped passenger costs perhaps fifteen thousand rupees each, at roughly one in two thousand
passengers — call it seven or eight rupees per passenger expected — against a few hundred rupees per
passenger of revenue from the seats they can now sell. **Compensation is around forty times cheaper than
prevention.** The general rule is: **compensate when the expected cost of the correction is below the cost
of the coordination** — and the same logic explains why a hotel oversells and a concert with legal
liability does not. The engineering consequence is that a compensating action is a real workflow —
detection, notification, refund, audit — and building it properly is often more work than the coordination
it replaced. It is still the right choice, because it degrades better."

**"How do you show a value you are not sure about?"**
"Honestly, and with the uncertainty in the **data model** rather than only in the wording. The bank
statement is the design: it shows the balance, and separately the uncleared amount, and separately what is
actually available — three numbers, because three different questions have three different answers. In
software that is 'Processing', 'Uploading', 'Pending', or 'Last updated thirty seconds ago' on a dashboard.
The principle is that **users tolerate uncertainty they can see and resent uncertainty they discover** —
and the failure mode of hiding it is worse than the failure mode of showing it, because a user who
discovers that a number was wrong stops trusting all your numbers. The cost is product complexity: three
states instead of one, on every screen and in every notification. I would pay it whenever the window is
long enough for a user to act during it."

**"What about a counter — is that not trivially eventual?"**
"The concept is, and the implementation catches people. The naive version — read the count, add one, write
it back — is a **lost update** under any concurrency, and it is wrong even on a single machine. Three
correct approaches. An **atomic increment** in the store, like Redis `INCR` or DynamoDB `ADD` — correct,
and it makes the counter one hot key, so it caps out around a hundred thousand a second. A **sharded
counter** — increment one of a hundred sub-counters at random and sum on read — which spreads the writes
and makes the read cost a hundred lookups. Or **per-replica counters summed on read**, which is a
G-counter CRDT: each node counts only its own increments, the value is the sum, and because addition is
commutative and associative there is no order to get wrong and no conflict to resolve. That last one is
why counters are the textbook CRDT, and it converges with **no coordination at all**."

### A model answer

Asked: *the like count is wrong for two seconds. Is that acceptable?*

> "It depends on **who is looking and at what**, so let me split it, because there are really two questions
> hiding in one.
>
> For a **stranger** looking at somebody else's post, two seconds is completely invisible. Nobody knows
> what the count should be, nobody is comparing it against anything, and being off by one is
> unobservable. So: yes, eventual, and I would not spend anything to fix it.
>
> For the **user who just tapped like**, two seconds is a bug and it gets reported. And it is not a rare
> event — it is essentially certain, because the read that follows a write is not a random sample, it is the
> worst possible one: the interface refreshes immediately, so it lands squarely inside the replication
> window every single time.
>
> The rule I would apply throughout is: **the display may be stale, the decision may not.** Showing 'twelve
> left in stock' can be seconds old; deciding whether to accept the order cannot.
>
> So for the person who tapped, my first choice is an **optimistic UI**: increment the number on their
> screen the instant they tap, before the request is even sent, because I am almost certain what the answer
> will be. Send it in the background; on success nothing further happens and they never knew there was a
> request; on failure revert visibly and say why. That is the highest-leverage pattern here because it
> costs **nothing on the server** — it converts read-your-writes from a routing problem into a client
> concern. The one thing I would build first is the failure path, because an optimistic UI with no
> considered revert is worse than none.
>
> Where optimism is not safe — where the server may legitimately reject or transform the action — I would
> either route that user's reads to the leader for a short window, which costs ten to fifteen percent of
> their reads, or **show the pending state honestly**. That is the bank-statement pattern: an uncleared
> cheque is displayed as uncleared, with the date it will clear. Users tolerate uncertainty they can see
> and resent uncertainty they discover.
>
> I would also be able to say **how long 'eventually' is**, because it is not one number. Hot keys converge
> in milliseconds through read repair — a read that sees disagreement writes the newest value back. Cold
> keys wait for anti-entropy, which compares Merkle trees to find differing ranges and runs every few
> minutes to hours. So it is bimodal, and the long tail is exactly the data nobody is reading.
>
> And I would draw the line: I would not make anything eventual where **two users can get the same thing**,
> or where the mistake cannot be corrected afterwards without harming somebody. Seats, stock at purchase,
> usernames, permissions, balances at the moment of a transfer. For a like count, though — yes, two seconds
> is fine, and I would spend the effort on making the user's own tap feel instant instead."

---

## 9. Recall card

- **The question is never "is eventual consistency acceptable" — it is "what does a user see in that
  window, and how bad is it?"** The same two seconds is invisible on a stranger's like count, a reported
  bug on your own, and a double booking on a seat. **The rule: the DISPLAY may be stale, the DECISION may
  not.**
- **Four patterns. OPTIMISTIC UI is the highest-value one** — update locally on tap, send in the
  background, **revert visibly on failure** — because it makes read-your-writes a *client* problem and
  costs nothing on the server. Never use it where the revert is not honest (payments, bookings). Then:
  **show the pending state** (the bank's uncleared cheque), **route around it** (leader reads for 30 s,
  ~10–15% of reads), and **compensate** rather than prevent.
- **Bounded optimism is the underrated move**: act on stale data where the exposure is small and wait
  where it is large — which is exactly a card terminal's **offline floor limit**. You do not have to choose
  between fully trusting stale data and fully refusing.
- **"Eventually" is bimodal and has three mechanisms: read repair (milliseconds, but only for keys that
  get READ) · hinted handoff (seconds after a node returns; hints expire) · anti-entropy (minutes to
  hours, comparing MERKLE TREES to find differing ranges in `O(log n)` instead of `O(n)`).** The data that
  stays wrong longest is the data nobody reads.
- **Never eventual: two users can get the same thing, or the mistake cannot be corrected without harm** —
  seats, stock at purchase, unique constraints, permissions, balances at transfer. **Compensate when the
  expected correction is cheaper than the coordination** (airlines: ~40× cheaper). And a **counter** is not
  trivial: read-modify-write is a **lost update** — use an atomic increment, a sharded counter, or
  **per-replica counters summed on read**, which is a CRDT and needs no coordination at all.
