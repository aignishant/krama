---
day: 113
track: system-design
title: "Why distributed systems are hard"
phase: "Distributed systems core"
status: written
---

# Day 113 · System Design — Why distributed systems are hard

**After today you can:** You can name the three things that stop being true once there are two machines.

**The interviewer asks it as:** *What changes when you go from one server to two?*

---

## 1. What this is, and why they ask it

A **distributed system** is one where the work is spread across machines that can only talk to each other
over a network. You have been building them for fifteen days — load balancers, replicas, shards, caches —
without naming the thing they all have in common.

Three sentences. On one machine, a function call either succeeds or throws, the clock is the same
everywhere, and memory is shared — and **all three of those stop being true the moment there are two
machines**. The one that matters most is **partial failure**: a call over a network has a third outcome
that does not exist locally, *"I do not know"*, and almost every difficult problem in the rest of this
phase is a consequence of it. And the honest conclusion is not a technique but a limit: there are things
you would like to guarantee that are provably impossible, so the work is choosing which guarantee to give
up.

They ask *"what changes with two machines?"* because it is the frame for everything after it —
[CAP](../day-114-heapify/README.md), [consistency models](../day-115-heapq/README.md),
[quorums](../day-117-merge-k-sorted/README.md), [leader election](../day-118-two-heaps/README.md),
[consensus](../day-119-heaps-revision/README.md). A candidate who can say *"the third outcome is
'unknown', so every operation must be safe to repeat"* has the key that unlocks all of them.

---

## 2. The story

The auction at the cattle market was on the second Tuesday and the two brothers had decided, finally,
that they would buy the pair of bullocks together.

Selvam was in Palani. Murugan was in Dindigul, four hours away. Neither could get to the other's town
before the auction, and the rule they had agreed was that they would only bid if **both** of them turned
up — one of them alone could not carry the money or handle the animals.

The phone line between those two exchanges was bad. Not dead — bad. Calls dropped in the middle, and you
could not always tell whether the other person had heard the last thing you said.

Selvam rang on the Sunday and said: Tuesday, eleven o'clock, at the north gate.

The line cut.

He did not know whether Murugan had heard "eleven o'clock" or whether the call had dropped before that. So
he rang again. Murugan answered and said yes, I heard, eleven, north gate.

And then Murugan put the phone down and immediately had the same problem in reverse. Selvam did not know
that Murugan had heard him — unless Murugan's confirmation had got through. And Murugan did not know that
his confirmation had got through, so from where he sat, Selvam might still be sitting in Palani thinking
the plan had failed.

So Murugan rang back and said: did you get my confirmation?

Selvam said yes.

And then Selvam thought about it while walking home and realised that Murugan now did not know whether
*that* had got through either.

He described it to his wife that evening, who was less interested than he had hoped, and he put it like
this: every message needs a reply to be sure it arrived, and the reply needs a reply, and there is no last
one. You can go on all night and there is always one message at the end that somebody is not sure about.

What they actually did on the Tuesday was not solve it. They changed the rule.

Selvam said: I will be at the north gate at eleven, and I will wait until half past twelve, and if you are
not there I will go home. It does not matter whether you got this message or not — if you are there, we
buy; if you are not, I lose a morning.

Both of them turned up at ten to eleven.

Murugan said afterwards that the trick was not agreeing better. It was building a plan where **not
agreeing did not cost very much**.

---

## 3. The idea in plain English

The brothers have discovered the Two Generals problem, and their solution is the one real systems use:
stop trying to guarantee agreement, and make disagreement cheap.

- The bad phone line is an **unreliable network**.
- "I do not know whether he heard me" is **partial failure** — the third outcome.
- The endless chain of confirmations is the **Two Generals problem**, and it is **provably unsolvable**.
- "Wait until half past twelve and then go home" is a **timeout**.
- "It does not matter whether you got this message" is designing for **idempotency and independent
  progress**.

### The three things that stop being true

**One: an operation has three outcomes, not two.**

```
 ONE MACHINE                    TWO MACHINES
 the call returns    ✓          the call returns              ✓
 the call throws     ✗          the call throws               ✗
                                THE CALL TIMES OUT            ???
                                and you cannot tell whether
                                it happened
```

**This is the whole subject.** A timeout does not mean failure. It means: the request may have been lost
on the way, or executed and the reply lost on the way back, or it is still running and will complete in a
minute. You cannot distinguish those from the outside, and **no amount of engineering makes that third
outcome go away.**

Everything downstream follows: **if you cannot tell whether it happened, you have to be able to do it
again safely.** That is why idempotency appears in every design in this course.

**Two: there is no shared clock.**

Two machines' clocks drift, and NTP corrects them in jumps — so time can appear to go **backwards** on a
machine.

```
 machine A says the write happened at 10:00:00.100
 machine B says its write happened at 10:00:00.050
 -> is B's write earlier? YOU CANNOT TELL. Their clocks differ by more than that.
```

**Consequences that come up constantly:** "last write wins" is not well defined; you cannot order events
across machines by timestamp; and a lease that expires "in 30 seconds" means 30 seconds *on somebody's
clock*.

The replacement is **logical time** — Lamport clocks and vector clocks — which order events by
*causality* rather than by wall time. **What you can know is "A happened before B" when there is a chain
of messages from A to B.** Anything else is genuinely concurrent, and calling it ordered is a fiction.

**Three: the network is not reliable, and it is not fast.**

```
 a local function call    ~1 nanosecond
 a call to another machine ~500,000 nanoseconds (0.5 ms) in the same DC
                          ~150,000,000 ns (150 ms) across the world
```

**Five hundred thousand times slower in the best case.** So a design that made sense as ten function calls
becomes a design that makes no sense as ten network calls, and "just extract it into a service" is a
performance decision, not only an organisational one.

### The fallacies, which are the checklist

L. Peter Deutsch's list from 1994 is still the standard, and each one is an assumption that is false and
that people keep making:

```
 1. the network is reliable         -> messages are lost; design for retries
 2. latency is zero                 -> a call is ~500,000x a function call
 3. bandwidth is infinite           -> the response size matters
 4. the network is secure           -> encrypt, authenticate, authorise
 5. topology does not change        -> machines come and go constantly
 6. there is one administrator      -> nobody knows the whole system
 7. transport cost is zero          -> serialisation and egress are real bills
 8. the network is homogeneous      -> different clouds, versions, protocols
```

**Name three of these and say which one your design is currently assuming.** That is a very strong move.

### Partial failure, in detail

On one machine, if the process dies, *everything* stops — and that is a much easier world than it sounds.
In a distributed system, **some parts are running and some are not, and the running parts do not know
which is which.**

```
 SCENARIO: service A calls service B to charge a card. A times out.

 possibilities:
   1. B never received it              -> retrying is correct
   2. B charged the card, reply lost   -> retrying charges TWICE
   3. B is still processing            -> retrying may charge twice
   4. B is dead                        -> retrying will fail again

 A cannot tell these apart. Ever.
```

**The only workable answer is to make the operation idempotent** — give it a key, so that a repeat is
recognised and returns the first result. That is why every serious API takes an idempotency key, and it is
the single most reusable idea in this phase.

### Exactly-once is not available

```
 AT MOST ONCE    send it, do not retry.            May be lost.
 AT LEAST ONCE   retry until acknowledged.         May be duplicated.
 EXACTLY ONCE    ...impossible over an unreliable network.
```

**You cannot have exactly-once delivery.** What you can have is **at-least-once delivery plus idempotent
processing**, which is *observationally* exactly-once — the effect happens once, even though the message
may arrive several times.

**Say it that way**: *"exactly-once delivery is impossible; exactly-once **effect** is achievable, with
at-least-once delivery and an idempotency key."* Systems that advertise exactly-once are doing precisely
this.

### The impossibility results worth naming

Two, and naming them is worth more than deriving them.

**Two Generals.** Two parties over an unreliable network can never be **certain** they have agreed. Every
message needs an acknowledgement, and the acknowledgement needs one. The brothers' evening.

**FLP (Fischer, Lynch, Paterson, 1985).** In an asynchronous system where even one process may fail, there
is **no algorithm that guarantees consensus** — because you cannot distinguish a crashed machine from a
slow one.

**What real systems do about them:** stop demanding certainty, and use **timeouts** to make progress. A
timeout is a *guess* that a machine is dead. It may be wrong — that is the price — and the whole of
[Raft and Paxos](../day-119-heaps-revision/README.md) is machinery for being safe when the guess is
wrong.

**The one-line summary: you cannot detect failure, so you assume it after a timeout and design for being
wrong.**

### What you get in exchange

The costs above are real, and so is the reason anybody accepts them:

```
 SCALE          past what one machine can do            (day 098, 106)
 AVAILABILITY   survive a machine failure               (day 104, 111)
 LATENCY        be near your users                      (day 103)
 ISOLATION      one team's failure is not everyone's    (bulkheads, day 111)
```

**Distribution is not a goal.** It is a price you pay for one of those four, and the right first question
about any distributed design is *which of the four am I buying?*

---

## 4. The picture

The third outcome, which is the whole subject.

```
 ONE MACHINE                          TWO MACHINES

   caller ──► function                  caller ──► network ──► service
      ◄────── returns                      ◄──────  ???  ◄─────

   TWO outcomes:                        THREE outcomes:
     returned a value  ✓                  returned a value        ✓
     raised            ✗                  returned an error       ✗
                                          TIMED OUT               ???
                                            ├─ never arrived
                                            ├─ ran, reply lost
                                            ├─ still running
                                            └─ the machine is dead
                                          AND YOU CANNOT TELL WHICH

 EVERYTHING ELSE IN THIS PHASE IS A CONSEQUENCE OF THAT THIRD BOX.
```

The brothers' endless acknowledgements:

```
 Selvam  ──"Tuesday, 11, north gate"──►  Murugan
         ◄──────"yes, I heard"────────
         ───"did you get my reply?"───►
         ◄──────"yes I did"───────────
         ───"and did you get THAT?"───►
                    ...

 there is always ONE message at the end that somebody is unsure about.
 No number of round trips removes it. That is the Two Generals result.

 WHAT THEY DID INSTEAD:
   "I will be there at 11 and wait until 12:30, whatever happens."
   -> a TIMEOUT, plus a plan that does not require agreement.
```

The three broken assumptions, side by side:

```
 ASSUMPTION            ON ONE MACHINE          ACROSS MACHINES
 -------------------   ---------------------   ------------------------------
 a call succeeds or    two outcomes            THREE — and "unknown" is the
 fails                                          one that matters

 time is shared        one clock               clocks drift; NTP jumps;
                                                time can go BACKWARDS
                                                -> use LOGICAL time

 memory is shared      one address space       messages, which are slow
 and instant           ~1 ns                    (~0.5 ms local, 150 ms global)
                                                and can be lost
```

Delivery guarantees, and where "exactly once" actually lives:

```
 AT MOST ONCE      send once, never retry
                   ├─ message lost  ->  the effect never happens
                   └─ fast, and lossy

 AT LEAST ONCE     retry until acknowledged
                   ├─ ack lost  ->  the effect happens TWICE
                   └─ reliable, and duplicating

 EXACTLY ONCE      ✗ IMPOSSIBLE as a delivery guarantee

 WHAT YOU BUILD:   at-least-once delivery + IDEMPOTENT processing
                   = exactly-once EFFECT
                     ▲
                     the idempotency key is what makes the duplicate harmless
```

Why a timeout is a guess:

```
 A sends a request to B and hears nothing for 5 seconds.

 B is dead        ──┐
 B is slow        ──┼── A CANNOT TELL THESE APART
 the request lost ──┤    (this is FLP, informally)
 the reply lost   ──┘

 so A GUESSES: "assume dead after 5 seconds"

 if the guess is WRONG:  B is alive and still working, and A has retried
                         -> duplicate work, or two leaders, or a lost update
 -> which is why every mechanism in this phase (fencing, quorums, epochs,
    idempotency keys) exists to be SAFE WHEN THE GUESS IS WRONG.
```

---

## 5. How it actually works

### The defences, and what each one is for

**Timeouts on every remote call.** Without one, a slow dependency holds your thread or connection until it
gives up, which is often never — and **a slow dependency is more dangerous than a dead one**, because a
dead one fails fast. The number matters: a timeout longer than your own caller's timeout is useless.

**Retries with exponential backoff and jitter.** Retrying immediately, in lockstep, turns a brief blip into
a stampede. Backoff spreads them out; jitter stops them synchronising.

**Idempotency keys.** The caller generates one per logical operation and sends it with every attempt. The
server records it and returns the stored result on a repeat. **This is what makes at-least-once delivery
safe**, and it is the single most reusable idea here.

**Circuit breakers.** After `n` consecutive failures, stop calling and fail fast for a while. That
protects *you* from a slow dependency and protects *it* from a thundering retry storm during recovery.

**Bulkheads.** A separate connection pool per dependency, so one slow service cannot exhaust everything.

**Deadlines that propagate.** Pass the remaining time budget down the call chain, so a service does not
start work its caller has already given up on. gRPC does this natively and it is the mature version of
timeouts.

### Ordering without a clock

**Lamport timestamps.** Every process keeps a counter, increments it on each event, and sends it with
every message. On receipt, `counter = max(own, received) + 1`.

```
 gives you: if A happened-before B, then L(A) < L(B)
 does NOT give you: the reverse. L(A) < L(B) does not mean A caused B.
```

**Vector clocks.** A counter per process instead of one. Now you can distinguish *"A happened before B"*
from *"A and B are concurrent"* — which is exactly what a conflict detector needs. The cost is a vector
that grows with the number of processes.

**Hybrid logical clocks** combine physical time with a logical counter, so timestamps are both causally
correct and roughly comparable to wall time. **CockroachDB and MongoDB use them**, and they are the modern
answer.

**And Google's TrueTime** takes the other route entirely: put atomic clocks and GPS receivers in every
datacentre, bound the uncertainty to a few milliseconds, and then **deliberately wait out the
uncertainty** before committing. Spanner is the only widely known system that buys its way past this
problem with hardware.

### Failure detection, honestly

```
 heartbeat every 1 s, declare dead after 3 misses  ->  ~3 s to detect
                                                       higher false-positive rate
 heartbeat every 5 s, 3 misses                     ->  ~15 s to detect
                                                       fewer false positives
```

**You are trading detection speed against false positives, and there is no setting that avoids both.** A
false positive means you fail over a healthy machine — which, if fencing is imperfect, gives you two
leaders.

**Phi-accrual failure detectors** — used by Cassandra and Akka — output a *suspicion level* rather than a
boolean, so the application can decide how much suspicion warrants action.

### What real systems do

- **Stripe, AWS and most payment APIs require an idempotency key** on every write. It is the industry's
  standard answer to partial failure and it is worth naming specifically.
- **Kafka's "exactly-once semantics"** is at-least-once delivery plus idempotent producers plus
  transactional writes — the effect is exactly-once; the delivery is not.
- **gRPC deadlines** propagate a remaining time budget through the whole call chain.
- **Amazon Dynamo** used vector clocks for conflict detection and pushed resolution to the application —
  the shopping cart that merges rather than picks a winner.
- **Spanner's TrueTime** is the hardware answer, and its commit-wait is the clearest demonstration that
  clock uncertainty is a real cost and not a theoretical one.
- **Jepsen** is the testing practice worth naming: deliberately partition a real cluster and check whether
  it violates the guarantees it claims. It has found violations in most major distributed databases.

---

## 6. The numbers

### The cost of leaving one machine

```
 in-process function call      ~1 ns
 same-machine IPC              ~10 µs           10,000x
 same-datacentre RPC           ~0.5 ms          500,000x
 same-continent RPC            ~30 ms           30,000,000x
 cross-world RPC               ~150 ms          150,000,000x
```

**A network call is roughly half a million times a function call**, so a design of ten chained calls costs
five milliseconds before any work happens — and across regions, one and a half seconds.

### Clock drift

```
 a typical quartz clock drifts      ~10-100 ppm  =  ~1-9 seconds per day
 NTP over the internet              ~1-50 ms accuracy, and it corrects in JUMPS
 NTP on a local network             ~0.1-1 ms
 GPS / atomic (Spanner TrueTime)    ~1-7 ms of BOUNDED uncertainty
```

```
 two events 5 ms apart on different machines with 50 ms clock skew:
 -> the timestamps may report them in the WRONG ORDER
 -> "last write wins" silently picks the older write
```

**That is the concrete cost of having no shared clock**, and it is why last-write-wins loses data.

### Failure probability at scale

```
 one machine, 99.9% available in a year   ->  ~8.8 hours down

 in a fleet of 1,000 machines with a 3-year MTBF each:
   expected failures per year    1,000 / 3   ≈ 333
   expected failures per day     ≈ 1
```

**At a thousand machines, something is failing every day.** So failure is not an exceptional path to be
handled defensively — it is the normal operating condition, which is a genuine change in mindset from
single-machine programming.

### Timeout and retry arithmetic

```
 timeout 1 s, 3 retries with exponential backoff:
   attempt 1 at t=0        fails at t=1
   attempt 2 at t=2        fails at t=3     (1 s backoff)
   attempt 3 at t=5        fails at t=6     (2 s backoff)
   total worst case ≈ 6 s

 if the CALLER's timeout is 3 s, attempts 2 and 3 are pure waste —
 the caller gave up at t=3.
 -> which is why DEADLINES must propagate, not just timeouts.
```

### The retry storm

```
 a dependency is down for 30 s; 1,000 clients each retry
   without backoff:  1,000 retries/s continuously, and the moment it
                     recovers it receives 1,000 simultaneous requests
   with backoff + jitter: spread over ~30 s, ~30/s
```

**Retries without backoff turn a 30-second outage into a much longer one**, because the recovering service
is immediately overwhelmed.

### Duplicate probability

```
 1,000,000 payment requests/day, 0.1% of which time out ambiguously
 -> 1,000 requests/day where the caller does not know whether it happened
 -> WITHOUT idempotency keys: up to 1,000 double charges a day
 -> WITH: 0
```

**That number is the business case for idempotency keys**, and it is far more persuasive than the theory.

---

## 7. The trade-offs

### Do not distribute unless you are buying something

Every machine you add costs you: a network hop, a new failure mode, a component in series reducing
availability, and an operational burden. **The only reasons that justify it are scale, availability,
latency and isolation** — and if none of them applies, one machine is faster, simpler and more reliable.

**A monolith on one large machine is a completely respectable answer**, and saying so at the right moment
is a mark of judgement rather than naivety.

### Timeouts: too short or too long

**Too short** turns a healthy-but-slow service into a failed one, triggers unnecessary retries, and can
cascade. **Too long** ties up your resources while a dead dependency does nothing, which is how a slow
dependency takes down its callers.

**The rule: a timeout must be shorter than your caller's timeout**, and the whole chain must fit inside
the user's patience. **Propagating deadlines is the mature form of this.**

### At-least-once plus idempotency, or at-most-once?

**At-least-once with idempotency** is the default and it costs you a key, storage for seen keys, and
discipline: every write path must honour it.

**At-most-once** is right when duplication is worse than loss and the operation genuinely cannot be made
idempotent — some notifications, some metrics. **Say which you are choosing and why**, because silently
assuming exactly-once is the most common conceptual error in this space.

### Where the honesty matters

- **"Exactly-once" is a claim about the effect, never about delivery.** Anyone claiming exactly-once
  delivery has either not thought about it or is describing idempotent processing.
- **A timeout is a guess about death.** Every mechanism after this — fencing, quorums, epochs, leases — is
  machinery for being safe when the guess is wrong.
- **You cannot order events across machines by timestamp.** Last-write-wins loses data silently, and the
  amount lost is bounded by the clock skew, not by anything you control.
- **Testing is genuinely hard**, because the interesting failures are timing-dependent and rare. Fault
  injection and Jepsen-style testing exist because ordinary tests do not find these.

### The thing that does not get easier

**Debugging.** On one machine you have a stack trace. Across twenty services you have twenty log streams,
clocks that disagree, and a request that touched eight of them. **Distributed tracing with a correlation
id is not a nice-to-have; it is the only way to understand what happened**, and it has to be designed in
from the first day rather than added during an incident.

---

## 8. In the interview

### How it gets asked

- The frame: *"What changes when you go from one server to two?"*
- The concrete one: *"Your service calls another and the call times out. What do you do?"*
- The trap: *"Can you guarantee exactly-once delivery?"*
- The clock one: *"How do you know which of two writes happened first?"*
- The judgement one: *"When would you not distribute?"*

### What to say out loud, in the first ninety seconds

1. **Name the three broken assumptions.** "Three things stop being true. A call no longer either succeeds
   or fails — there is a third outcome. There is no shared clock. And memory is replaced by messages that
   are slow and can be lost."
2. **Say which one matters most.** "The third outcome is the whole subject. A timeout means the request may
   never have arrived, or may have executed with the reply lost, or may still be running — and you cannot
   tell which."
3. **Draw the consequence immediately.** "So if I cannot tell whether it happened, I have to be able to do
   it again safely. That is why idempotency keys appear in every design here."
4. **Kill exactly-once before it is offered.** "Which is also why exactly-once *delivery* is impossible.
   What is achievable is at-least-once delivery plus idempotent processing, giving an exactly-once
   *effect*."
5. **Give the clock consequence.** "And with no shared clock, you cannot order events across machines by
   timestamp — clock skew is often larger than the interval you are trying to order, so last-write-wins
   silently discards data. You order by causality instead."
6. **Say why anyone accepts all this.** "Distribution is not a goal. It is the price of scale,
   availability, latency or isolation — and if I am not buying one of those, one machine is faster and more
   reliable."

### The follow-ups

**"Your call times out. What do you do?"**
"First, name the problem: a timeout is not a failure, it is an **unknown**. Four things may have happened —
the request never arrived, it executed and the reply was lost, it is still running, or the machine is dead
— and from the outside they are indistinguishable. So the question is not 'do I retry', it is 'is retrying
safe'. If the operation is **idempotent** — a read, a set-to-a-value, a delete — I retry with exponential
backoff and jitter, backoff so a brief outage does not become a retry storm and jitter so a thousand
clients do not come back in lockstep. If it is **not** idempotent, like charging a card, retrying blindly
may charge twice, so I make it idempotent: the caller generates a key per logical operation and sends it
with every attempt, and the server records the key and returns the stored result on a repeat. That is what
turns at-least-once delivery into an exactly-once effect. I would also cap the retries, and make sure my
timeout is shorter than my caller's — otherwise I am doing work nobody is waiting for any more."

**"Can you guarantee exactly-once delivery?"**
"No, and it is worth being precise about why rather than just saying no. Over an unreliable network, the
sender cannot know whether a message arrived without an acknowledgement, and the acknowledgement can be
lost, and an acknowledgement of the acknowledgement can be lost — that is the Two Generals result, and
there is no protocol that removes the final uncertain message. So the choice is at-most-once, which may
lose messages, or at-least-once, which may duplicate them. What **is** achievable is an **exactly-once
effect**: at-least-once delivery plus idempotent processing, where a duplicate is recognised and
discarded. That is what systems advertising exactly-once are actually doing — Kafka's exactly-once
semantics is idempotent producers plus transactional writes on top of at-least-once delivery. The
distinction between delivery and effect is the whole answer."

**"How do you know which of two writes happened first?"**
"Usually you cannot, and that is more surprising than it sounds. Two machines' clocks drift — a typical
quartz oscillator is tens of parts per million, which is seconds per day — and NTP corrects in jumps, so a
machine's clock can go **backwards**. If the skew is fifty milliseconds and the two writes are five
milliseconds apart, the timestamps may report them in the wrong order, and 'last write wins' then silently
discards the newer write. So you order by **causality** instead of by wall time. **Lamport timestamps**
give you: if A happened before B, then A's stamp is lower — though not the converse. **Vector clocks** go
further and let you distinguish 'A before B' from 'A and B are genuinely concurrent', which is what a
conflict detector needs, at the cost of a vector per process. The modern practical answer is **hybrid
logical clocks**, which combine physical time with a logical counter so stamps are causally correct and
still comparable to wall time — CockroachDB and MongoDB use them. And Google's Spanner buys its way out
with **TrueTime**: atomic clocks and GPS bound the uncertainty to a few milliseconds, and then it
deliberately **waits out** that uncertainty before committing."

**"When would you not distribute?"**
"Whenever I am not buying one of four things: **scale** past a single machine, **availability** through
redundancy, **latency** by being near users, or **isolation** so one team's failure is not everyone's. If
none of those applies, one machine is faster, simpler, and more available than two — because every added
component sits in series and availabilities multiply. A monolith on a large machine is a completely
respectable architecture, and going distributed for organisational reasons alone means paying the network
tax on every call: a remote call is about half a million times a local one, so what was ten function calls
becomes five milliseconds of pure latency, and across regions one and a half seconds. Plus you have
acquired partial failure, clock skew, and a debugging problem that needs distributed tracing designed in
from day one."

**"What is the hardest part in practice?"**
"Debugging, and it is not close. On one machine a failure gives you a stack trace. Across twenty services
you have twenty log streams, machines whose clocks disagree by more than the events you are trying to
order, and a single user request that touched eight of them — and the interesting failures are
timing-dependent, so they do not reproduce. That is why a **correlation id** propagated through every call
and distributed tracing are not optional extras; they are the only way to reconstruct what happened, and
they have to be there before the incident. The related practice worth naming is deliberate fault injection
— Jepsen-style testing, where you partition a real cluster and check whether it violates the guarantees it
claims. It has found violations in most major distributed databases, which tells you something about how
hard this is to get right by reasoning alone."

**"So how do real systems cope with the impossibility results?"**
"They stop demanding certainty and use **timeouts** to make progress — and then build machinery to be safe
when the timeout's guess is wrong. FLP says you cannot guarantee consensus in an asynchronous system where
a process may fail, because a crashed machine and a slow machine are indistinguishable. So a system
**guesses** after a timeout: it assumes the machine is dead and elects a new leader. If the guess is wrong
you have two leaders — and that is what **fencing**, **quorums** and **epoch numbers** exist for: the old
leader cannot see a majority, or its writes are stamped with a stale term and rejected. The pattern is:
you cannot detect failure, so you assume it and design so that being wrong is survivable. Every mechanism
in the rest of this phase is a variation on that."

### A model answer

Asked: *what changes when you go from one server to two?*

> "Three things stop being true, and all of the difficulty comes from them.
>
> **First, an operation no longer has two outcomes.** On one machine a function call either returns or
> throws. Across a network there is a third: it **times out**, and you cannot tell whether the request never
> arrived, or executed and the reply was lost, or is still running, or the machine is dead. Those are
> indistinguishable from the outside, and no amount of engineering removes the third box.
>
> That single fact generates most of the rest. **If I cannot tell whether something happened, I have to be
> able to do it again safely** — which is why every serious write API takes an **idempotency key**, and why
> **exactly-once delivery is impossible** while an exactly-once *effect* is achievable: at-least-once
> delivery plus idempotent processing. That distinction between delivery and effect is worth being precise
> about, because systems advertising exactly-once are all doing the second thing.
>
> **Second, there is no shared clock.** Clocks drift by seconds a day and NTP corrects them in jumps, so
> time can run backwards on a machine. If the skew between two machines is fifty milliseconds and two
> writes are five milliseconds apart, their timestamps can report them in the wrong order — so
> 'last write wins' silently discards the newer value. You order events by **causality** instead: Lamport
> timestamps for happened-before, vector clocks if you also need to detect genuine concurrency, or hybrid
> logical clocks in practice. Spanner is the exception that proves the rule — it puts atomic clocks in
> every datacentre and then deliberately waits out the remaining uncertainty before committing.
>
> **Third, memory becomes messages.** A local call is about a nanosecond; a call to another machine in the
> same datacentre is half a millisecond, and across the world a hundred and fifty. Half a million times
> slower in the best case. So a design that was ten function calls is a very different design as ten
> network calls.
>
> The practical consequences I would build in from the start: **a timeout on every remote call**, because a
> slow dependency is more dangerous than a dead one; **retries with exponential backoff and jitter**, so a
> thirty-second outage does not become a retry storm on recovery; **idempotency keys** on every non-read
> operation; **circuit breakers**, so a failing dependency fails fast rather than filling my connection
> pool; and **a correlation id on every request**, because without distributed tracing an incident across
> twenty services is unreadable.
>
> And the thing I would say before any of it: **distribution is not a goal.** It is the price of scale,
> availability, latency, or isolation. If I am not buying one of those four, one machine is faster, simpler
> and more available — because every component I add sits in series, and availabilities multiply."

---

## 9. Recall card

- **Three things stop being true with two machines: an operation has a THIRD outcome ("unknown"), there is
  NO shared clock, and memory becomes slow, lossy messages** (~1 ns local against **~0.5 ms** in a
  datacentre and **~150 ms** across the world — half a million times).
- **The third outcome is the whole subject.** A timeout may mean: never arrived · executed with the reply
  lost · still running · dead — **indistinguishable from outside**. Therefore **if you cannot tell whether
  it happened, it must be safe to repeat** — an **idempotency key** on every write.
- **Exactly-once DELIVERY is impossible** (Two Generals: every ack needs an ack). **At-least-once delivery
  + idempotent processing = exactly-once EFFECT** — which is what Kafka and everyone else actually mean.
  At 1M requests/day with 0.1% ambiguous timeouts, that is **1,000 potential double charges a day**.
- **You cannot order events across machines by timestamp** — clock skew (tens of ms) usually exceeds the
  interval you are ordering, so **last-write-wins silently discards data**. Use **causality**: Lamport,
  vector clocks, hybrid logical clocks; Spanner buys its way out with **TrueTime** and a deliberate
  commit-wait.
- **A timeout is a GUESS that a machine is dead** (FLP: crashed and slow are indistinguishable), so
  fencing, quorums and epochs exist to be **safe when the guess is wrong**. Build in **timeouts · backoff
  with jitter · idempotency keys · circuit breakers · propagated deadlines · a correlation id**. And
  **distribution is not a goal** — it is the price of **scale, availability, latency or isolation**, and
  one machine is faster and more available if you are buying none of them.
