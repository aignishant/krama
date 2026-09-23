---
day: 110
track: system-design
title: "Capacity planning: QPS, storage, bandwidth"
phase: "Scaling fundamentals"
status: written
---

# Day 110 · System Design — Capacity planning: QPS, storage, bandwidth

**After today you can:** You can turn a product requirement into a server count.

**The interviewer asks it as:** *How many servers does this system need?*

---

## 1. What this is, and why they ask it

[Day 109](../day-109-balanced-trees/README.md) produced numbers. Today turns them into a **fleet**: how
many machines, of what size, with how much room to spare.

Three sentences. The naive answer — peak load divided by what one machine does — is wrong by roughly a
factor of two, and the reason is the most useful idea in this lesson: **a queue's waiting time explodes as
utilisation approaches one**, so a machine at 90 percent busy is not "90 percent used", it is unusable.
On top of that you need headroom for a **machine failing**, for **growth between now and the next
purchase**, and for the fact that **autoscaling takes minutes** while a traffic spike takes seconds. And
the three resources — compute, storage, bandwidth — run out at different times, so the binding one is
rarely the one you were watching.

They ask *"how many servers?"* because it is the shortest question with a genuinely layered answer.
Dividing two numbers takes ten seconds; explaining why you then multiply by 1.5 for utilisation, add one
for redundancy, and add fifty percent for growth is what the question is for.

---

## 2. The story

Dr Vasanthi's clinic opened at nine and she saw patients until about two, and for eleven years the
waiting room had been a problem that everybody blamed on the wrong thing.

She could see a patient in about ten minutes. Six an hour, five hours, so thirty patients in a morning —
and the receptionist, sensibly, booked thirty.

The waiting room was chaos. People booked for eleven were being seen at half past twelve. Everybody
assumed she was slow, or that patients were arriving late, and both were slightly true and neither was
the reason.

Her nephew, who was doing something with statistics at college, sat in the waiting room for three
mornings and then explained it to her in a way she remembered.

He said: you can do thirty. So you booked thirty. But patients do not arrive spread out evenly, and they
do not all take ten minutes. Some take four and some take twenty-five. When you have booked exactly as
many as you can do, **there is no gap anywhere in the morning to absorb a long one.** One patient who
takes twenty-five minutes pushes everybody after him back by fifteen, and nothing in the rest of the
morning ever catches that up, because every slot after it is already full.

He said the queue does not grow slowly as you book more. It grows slowly, and slowly, and then at the end
it goes vertical.

He gave her the numbers he had counted. At twenty patients — two thirds of what she could do — the
average wait was about six minutes. At twenty-four, about twelve. At twenty-seven, about half an hour. At
thirty, an hour and a half and getting worse every day.

She dropped it to twenty-four and the waiting room emptied out. She was seeing six fewer people, and she
was finishing earlier, and nobody was angry.

Two other things came out of those three mornings.

He pointed out that on the two days a month when her assistant was away, she did everything herself and
the whole thing collapsed — so the twenty-four was really only true when both of them were there. If she
wanted the clinic to work on the assistant's day off, she had to book for what **one** person could do,
not two.

And he said the thing about the following year. The colony behind the clinic was being built out and
there would be more people, so whatever number she chose would be wrong within eighteen months, and she
should decide now whether she was planning for today or for the day she would have to hire somebody.

---

## 3. The idea in plain English

The clinic is a capacity plan, and all three of the nephew's points are the three things people leave out
of the server count.

- Ten minutes a patient is **service time**; thirty a morning is **capacity**.
- Booking thirty is planning at **100 percent utilisation**, and the waiting room is the **queue**.
- "It goes vertical at the end" is the fact that **latency explodes near saturation** — the single most
  useful idea here.
- The assistant's day off is **N+1 redundancy**: size so that the system still works with one unit gone.
- The new colony is **growth headroom**.

### The naive answer, and why it is wrong

```
 servers = peak QPS ÷ QPS per server
         = 6,000 ÷ 1,000
         = 6
```

**Six machines is the answer to a different question**: how many machines are needed for the work to be
theoretically possible. It is not how many you run.

Three multipliers are missing.

### Multiplier one: utilisation, and why latency explodes

The essential fact. For a queue where work arrives unevenly, the average waiting time behaves roughly
like:

```
 wait  ∝  utilisation / (1 - utilisation)
```

That denominator is the whole story. As utilisation approaches 1, the wait approaches infinity.

```
 utilisation   relative queueing delay
 -----------   -----------------------
 50%           1×      (the baseline)
 70%           2.3×
 80%           4×
 90%           9×
 95%           19×
 99%           99×
```

**At 90 percent utilisation, requests wait nine times longer than at 50 percent.** Not nine percent —
nine times. And the machine is not broken; it is doing exactly what it was asked to do.

**So you size for 60 to 70 percent, not 100.** That is a multiplier of about 1.5.

```
 6 machines at 100%  ->  9-10 machines at 65%
```

Dr Vasanthi booking twenty-four instead of thirty.

The reason it is not a straight line, in one sentence: **work does not arrive evenly.** If exactly one
request arrived every millisecond and each took exactly one millisecond, 100 percent utilisation would be
fine. Real arrivals are bursty, and a burst arriving at a busy machine has nowhere to go but the queue.

### Multiplier two: redundancy

A machine will fail, be patched, or be restarted for a deployment. **The fleet must still work when one is
gone.**

```
 N+1   survives one failure     -> add 1 machine
 N+2   survives two             -> add 2
 2N    survives a whole zone    -> double it
```

```
 9 machines at 65% utilisation
 lose one -> the remaining 8 go to 73%      still fine
 lose two -> 7 go to 84%                    degraded, and latency is 4x
```

**The smaller the fleet, the more expensive redundancy is**, proportionally:

```
 fleet of 3, lose one   -> the survivors take 50% more each
 fleet of 30, lose one  -> 3.4% more each
```

That is a real argument for more, smaller machines rather than fewer, larger ones — **the opposite of the
[day 098](../day-098-what-a-tree-is/README.md) vertical-scaling instinct**, and worth being able to
reconcile: scale up until the cost curve bends, then out, and past that point smaller units make failure
cheaper.

### Multiplier three: growth

Capacity you provision today has to last until you next provision. **Ask over what horizon.**

```
 20% growth per year, planning 12 months ahead   -> ×1.2
 100% growth per year (a doubling), 12 months    -> ×2
 a launch, growth unknown                         -> autoscale, and set the ceiling high
```

**On cloud infrastructure this multiplier is much smaller than it used to be**, because adding a machine
takes minutes rather than a purchase order. Say that: the growth multiplier is a function of how long it
takes you to add capacity.

### Putting the three together

```
 raw need            peak QPS ÷ per-server QPS       6,000 ÷ 1,000  =  6
 × utilisation       ÷ 0.65                                          =  9.2  -> 10
 + redundancy        N+1                                             =  11
 × growth            ×1.2 for a year                                 =  13.2 -> 14

 ANSWER: about 14 machines, and here is the reasoning for each step.
```

**Six to fourteen.** The multipliers matter more than the division.

### Autoscaling does not remove the problem

Autoscaling changes *when* you buy capacity, not whether you need headroom.

```
 spike arrives                      t = 0
 metric window                      +60 s     (you scale on a 1-minute average)
 scaling decision + API call        +10 s
 instance boots                     +60 s
 application starts, warms up       +60 s
 passes health checks, gets traffic +30 s
 -----------------------------------------
 total                              ~3-4 minutes
```

**For three to four minutes, the existing fleet takes the entire spike alone.** So the steady-state fleet
must survive the spike unaided for that long — which means autoscaling saves money on the *trough*, not on
the peak.

**This is the most common mistake in a design interview involving autoscaling**, and stating it is a
strong signal.

### The three resources run out at different times

Compute, storage and bandwidth are separate plans, and the binding one is often not the obvious one.

```
 COMPUTE     peak QPS ÷ per-server QPS, then the multipliers
             -> scales with TRAFFIC, and is elastic

 STORAGE     bytes/day × retention × replication
             -> scales with TIME, and only ever grows
             -> you cannot autoscale it down

 BANDWIDTH   QPS × bytes per response
             -> often the first to bind, for anything with media
             -> and it is metered, so it is a bill rather than a wall
```

**Ask which one binds first.** For a text-heavy API it is compute; for a photo product it is bandwidth;
for a logging system it is storage. Getting that right early changes the whole architecture.

### Per-machine numbers, and the honest caveat

```
 app server, simple request        1,000 - 5,000 QPS
 app server, real work              200 - 1,000 QPS
 relational DB, indexed reads     5,000 - 15,000 QPS
 relational DB, writes              500 - 5,000 QPS
 Redis                          100,000+ ops/s
 one 10 Gbit/s network link           ~1 GB/s
 one SSD                        ~500 MB/s, ~50,000 IOPS
```

**These are order-of-magnitude figures and they depend enormously on what a request does.** Say so: *"I am
assuming about a thousand requests a second per application server, and that depends completely on the
work per request — if each one runs a complex query it might be two hundred. I would measure rather than
assume, and this is the number I would want from a load test first."*

**Naming the number you would go and measure is better than pretending to know it.**

---

## 4. The picture

The utilisation curve. **This is the diagram that makes the whole lesson.**

```
 queueing delay (relative)

 100× │                                                        *
      │                                                       *
      │                                                      *
  20× │                                                   *
      │                                              *
  10× │                                        *
      │                                   *
   5× │                            *
      │                  *
   1× │  *   *    *
      └──────────────────────────────────────────────────────────
        20%  40%  50%  60%  70%   80%    90%   95%  99%
                          ▲
                     SIZE HERE
                    (60-70%)

 the curve is nearly flat to 60% and then goes vertical.
 90% utilisation is NOT "90% used" — it is 9x the waiting time.
 Dr Vasanthi booking 30 patients when she could do 30.
```

The three multipliers, stacked:

```
              peak QPS 6,000
                    │
                    │ ÷ 1,000 QPS per server
                    ▼
 raw need           6 machines      ← the answer to a DIFFERENT question
                    │
                    │ ÷ 0.65 (size for 65% utilisation)
                    ▼
 with headroom      10
                    │
                    │ + 1 (survive one failure)
                    ▼
 with redundancy    11
                    │
                    │ × 1.2 (a year of growth)
                    ▼
 THE ANSWER         14 machines

 the division is the easy part. The three multipliers are the answer.
```

Why autoscaling does not remove the headroom:

```
 traffic
   │                    ┌──────────────  the spike
   │                    │
   │                    │
   │────────────────────┘
   │
 capacity
   │────────────────────────────┐
   │                            │  new instances arrive HERE
   │                    ┌───────┘
   │────────────────────┘
   └──────────────────────────────────────────────────► time
                        │◄── 3-4 min ──►│
                        the existing fleet takes the
                        WHOLE spike, alone, for this long

 -> autoscaling saves money in the TROUGH.
 -> the steady-state fleet must survive the PEAK unaided.
```

Redundancy is proportionally cheaper in a bigger fleet:

```
 fleet size   lose one   survivors' load increases by
 ----------   --------   ----------------------------
 2            1 left     +100%     ← catastrophic
 3            2 left     +50%
 5            4 left     +25%
 10           9 left     +11%
 30           29 left    +3.4%

 many small machines make failure cheap.
 few large machines make failure expensive.
 (and this pulls AGAINST the vertical-scaling argument from day 098 —
  scale up until the cost curve bends, then out.)
```

The three resources, and which binds:

```
 a TEXT API                a PHOTO product            a LOGGING system
 compute  ████████░░ 80%   compute  ██░░░░░░░░ 20%    compute  ███░░░░░░░ 30%
 storage  ██░░░░░░░░ 20%   storage  █████░░░░░ 50%    storage  ██████████ 100% ←
 bandwidth ███░░░░░░ 30%   bandwidth ██████████ 100% ←bandwidth ████░░░░░░ 40%
          ▲
     compute binds          bandwidth binds           storage binds
     -> more app servers    -> a CDN                  -> retention policy,
                                                          compression, tiering
```

---

## 5. How it actually works

### The procedure

```
 1. peak QPS                  from the estimate (day 109), including the peak factor
 2. per-server capacity       from a load test if possible; an assumption if not
 3. raw machine count         1 ÷ 2
 4. ÷ target utilisation      0.6-0.7
 5. + redundancy              N+1, or N+2, or 2N for zone failure
 6. × growth                  over your provisioning horizon
 7. repeat for storage        bytes/day × retention × replication
 8. repeat for bandwidth      QPS × bytes/response
 9. say which one binds       and what you would change if it were different
```

**Steps 4 to 6 are the ones that distinguish an answer from a division.**

### Choosing the utilisation target

It is not always 65 percent, and knowing when it moves is worth stating:

```
 latency-sensitive, user-facing      50-60%    the queueing curve is the constraint
 general web tier                    60-70%    the default
 batch / async workers               80-90%    a queue in front absorbs the burst,
                                               and nobody is waiting
 anything with a hard SLA at p99     40-50%    tail latency is what saturation destroys
```

**Batch work is the interesting case**: because a queue absorbs arrival variance and nobody is watching a
spinner, you can run those machines hot. **That is the single biggest lever for cost**, and it is why
moving work off the request path is worth so much.

### Sizing storage, which is a different kind of plan

```
 bytes per record × records per day × retention days × replication factor
```

```
 5,000,000 writes/day × 1 KB          =  5 GB/day
 × 365 (one year retention)           =  1.8 TB
 × 3 (replication)                    =  5.5 TB
 + 30% for indexes                    =  7.2 TB
 + 20% free space headroom            =  8.6 TB
```

**Two additions people forget:**

- **Indexes.** A well-indexed table is commonly 1.3 to 2 times the size of its data. Say "plus thirty
  percent for indexes" and it sounds like you have run a database.
- **Free space.** A disk at 95 percent full is a problem for a database long before it is full —
  compaction, vacuum and temporary sort space all need room.

**And storage cannot be scaled down**, so the retention policy *is* the capacity plan. "Ninety days hot,
then archive" is a capacity decision disguised as a product decision.

### Sizing bandwidth

```
 peak QPS × bytes per response = bytes per second
```

```
 6,000 QPS × 5 KB JSON                =  30 MB/s      one machine's link, easily
 6,000 QPS × 500 KB images            =  3 GB/s       THREE machines' worth of
                                                       network, for the images alone
```

**Which is why images go to a CDN** — and the number above is the reason, stated as a number rather than
as a principle.

Also worth separating: **egress is metered and charged**, so bandwidth is usually a bill rather than a
wall. Compute and storage are walls.

### What real practice looks like

- **Load test to find the per-machine number.** Every figure in the table above is a starting assumption;
  the real one comes from ramping load against one instance until p99 latency degrades, and taking the
  QPS just below that knee. **The knee is the capacity, not the point where it falls over.**
- **Autoscaling policies** are usually on CPU utilisation with a target around 50 to 60 percent — which
  looks low until you remember the queueing curve, and that the metric lags.
- **Google's SRE practice** is to run services at a utilisation that keeps error budgets intact, and to
  treat headroom as a deliberate, costed decision rather than a leftover.
- **Reserved or committed capacity** is 30 to 60 percent cheaper than on-demand, so the usual pattern is
  to reserve the steady-state fleet and autoscale the peak on-demand.

---

## 6. The numbers

### The utilisation multiplier

```
 target utilisation   machines needed for 6,000 QPS at 1,000 QPS each
 ------------------   -----------------------------------------------
 100%                 6      (and unusable: latency is unbounded)
 90%                  6.7 -> 7      queueing delay 9x
 80%                  7.5 -> 8      queueing delay 4x
 70%                  8.6 -> 9      queueing delay 2.3x
 65%                  9.2 -> 10     the usual target
 50%                  12            for a hard tail-latency SLA
```

**The cost of going from 90 to 65 percent is three machines. The benefit is a four-fold reduction in
queueing delay.** Stated that way, it is obviously worth it.

### The full worked count

```
 GIVEN: 6,000 peak QPS, ~1,000 QPS per app server

 raw                          6
 ÷ 0.65 utilisation           9.2  ->  10
 + 1 redundancy (N+1)         11
 × 1.2 growth (12 months)     13.2 ->  14

 and check the failure case:
   14 machines, one dies -> 13 carry 6,000 QPS -> 462 QPS each -> 46% utilisation ✓
   14 machines, a whole AZ (a third) dies -> 9 carry 6,000 -> 667 each -> 67% ✓
```

**That last check is the part that impresses**: sizing is not finished until you have verified the failure
case.

### Storage, fully loaded

```
 5 GB/day of rows
 × 365 days                       =  1.8 TB
 × 3 replicas                     =  5.5 TB
 × 1.3 for indexes                =  7.2 TB
 ÷ 0.8 for free-space headroom    =  9.0 TB

 -> "about 9 TB provisioned for 1.8 TB of actual data"
    a 5x multiplier, and every step of it is real.
```

**People quote 1.8 TB and provision 2.** The 5× is the answer.

### Bandwidth, and when it binds

```
 responses     peak QPS   bytes/response   bandwidth   machines' worth of link
 -----------   --------   --------------   ---------   -----------------------
 JSON API      6,000      5 KB             30 MB/s     0.03
 HTML pages    6,000      50 KB            300 MB/s    0.3
 thumbnails    6,000      200 KB           1.2 GB/s    1.2
 full images   6,000      2 MB             12 GB/s     12
 video         1,000      5 Mbit/s each    625 MB/s    0.6 (but continuous)
```

**Anything above about 1 GB/s means the CDN is not optional**, and this table says at what point.

### Autoscaling lag, and what it costs

```
 reaction time                    ~3-4 minutes
 a spike of 3x, arriving in 10 s

 fleet sized at 65% for normal load:
   during the spike it is at 195% -> requests queue, latency explodes,
   health checks start failing, and the autoscaler may even remove instances

 fleet sized to absorb a 3x spike unaided:
   normal utilisation ~22%, which is expensive

 the usual compromise:
   size for the LARGEST spike you can predict (evening peak) as steady state,
   autoscale for the unpredictable part,
   and put a QUEUE in front of anything that can be made asynchronous
```

### Cost, which is what the number is for

```
 14 app servers × ₹12,000/month             =  ₹168,000
 reserved instead of on-demand (-40%)       =  ₹101,000
 database: 1 primary + 2 replicas           =  ₹150,000
 Redis                                      =   ₹25,000
 storage 9 TB block                         =   ₹72,000
 bandwidth 30 MB/s ≈ 78 TB/month @ ₹7/GB    =  ₹546,000   ← the biggest line
 -----------------------------------------------------------
 ~₹894,000/month
```

**Bandwidth being the largest line is the common surprise**, and it is the arithmetic that justifies a CDN
in a budget meeting rather than in a design review.

---

## 7. The trade-offs

### Utilisation against cost

Running at 40 percent is safe and costs 60 percent more than running at 65. Running at 90 saves money and
gives you nine times the queueing delay and no room for a failure.

**Sixty to seventy percent is the default for user-facing work; eighty to ninety is right for batch work
behind a queue.** The difference is whether a human is waiting.

### Few large machines, or many small?

**Many small** makes failure cheap — losing one of thirty costs 3.4 percent — and makes autoscaling
granular. **Few large** is simpler to operate, uses less total overhead, and makes each failure expensive:
losing one of three costs the survivors 50 percent each.

**And this pulls against [day 098's](../day-098-what-a-tree-is/README.md) advice to scale up first.** The
reconciliation: scale up while the price per unit of power is flat, then out — and once you are out,
prefer enough units that any single loss is absorbable.

### Autoscale, or provision statically?

**Autoscaling** saves real money on a workload with a large daily trough, and it cannot react to a fast
spike — three to four minutes is an eternity for a 10-second surge.

**Static provisioning** is predictable, and you pay for the peak at three in the morning.

**Take both**: reserve the steady state, autoscale the predictable daily variation, and put a queue in
front of anything that can absorb a spike asynchronously.

### Where the plan is wrong

- **Per-machine capacity is a guess until you load-test it.** Everything downstream is proportional to it,
  so it is the number worth measuring first.
- **The peak factor is the input most often wrong**, and it is a multiplier on everything.
- **Scaling the application does not scale the database.** Fourteen app servers with twenty connections
  each is 280 database connections, which many databases will not accept — so a connection pooler becomes
  a required component, not an optimisation.
- **Storage is a ratchet.** It only goes up, it cannot be autoscaled down, and the retention policy is the
  only real lever.
- **A dependency you do not control has its own limits.** A third-party API with a 1,000-requests-per-second
  quota is your capacity ceiling regardless of how many machines you run.

---

## 8. In the interview

### How it gets asked

- The direct one: *"How many servers does this system need?"*
- The probe: *"Why not six? You said each one does a thousand."*
- The failure question: *"What happens when one of them dies?"*
- The autoscaling question: *"Would you just autoscale?"*
- The binding-constraint question: *"What runs out first?"*

### What to say out loud, in the first ninety seconds

1. **Do the division, and immediately say it is not the answer.** "Six thousand peak QPS at about a
   thousand per server is six machines — but six is the answer to 'what is theoretically possible', not
   'what would I run'."
2. **Give the utilisation reason, with the number.** "I would size for sixty-five percent utilisation, not
   a hundred, because queueing delay grows as utilisation over one-minus-utilisation. At ninety percent,
   requests wait about nine times longer than at fifty. So that is ten machines, not six."
3. **Add redundancy explicitly.** "Then N+1, because a machine will fail or be patched and the fleet has
   to work without it. Eleven."
4. **Add growth, and qualify it.** "Then growth over my provisioning horizon — twenty percent for a year,
   so fourteen. On cloud that multiplier is small, because adding a machine takes minutes."
5. **Check the failure case.** "And I would verify: with fourteen, losing one leaves thirteen at
   forty-six percent, and losing a whole availability zone leaves nine at sixty-seven percent. Both fine."
6. **Say which resource binds.** "That is compute. I would size storage and bandwidth separately, because
   they run out at different times — and for anything with images, bandwidth binds first."

### The follow-ups

**"Why not six? You said each one does a thousand."**
"Because a machine at a hundred percent utilisation is not a machine that is fully used — it is a machine
with an unbounded queue. Waiting time in a queue grows roughly as utilisation divided by one minus
utilisation, so the curve is nearly flat up to about sixty percent and then goes vertical: at eighty
percent requests wait four times longer than at fifty, at ninety percent nine times, at ninety-nine
percent about a hundred. The machine is not broken and nothing has failed — that is simply what queues do
when work arrives unevenly, and real traffic is bursty. So I size for sixty-five percent, which turns six
machines into ten. The cost of that is four machines; the benefit is a fourfold reduction in queueing
delay and somewhere for a burst to go. For a batch workload behind a queue I would happily run at eighty
or ninety, because nobody is waiting and the queue absorbs the variance — that difference is one of the
biggest cost levers there is."

**"What happens when one of them dies?"**
"That is the check I would do before giving you a final number, and it is why I add N+1. With fourteen
machines carrying six thousand QPS, losing one leaves thirteen at about four hundred and sixty each,
which is forty-six percent utilisation — comfortable. Losing an entire availability zone, which is a
third of them, leaves nine carrying six hundred and sixty-seven each, about sixty-seven percent — still
inside my target. If the answer to either of those had been over eighty percent, the fleet is too small,
because a failure would then push it into the steep part of the queueing curve and the latency damage
would be far worse than the lost capacity. It is also worth saying that redundancy is proportionally much
cheaper in a large fleet: losing one of thirty costs the survivors three percent each, and losing one of
three costs them fifty percent."

**"Would you just autoscale?"**
"Autoscaling is worth having and it does not remove the need for headroom, because it is slow relative to
a spike. The chain is: the metric window is typically a minute, then the scaling decision and API call,
then the instance boots, then the application starts and warms up, then it has to pass health checks
before it receives traffic — three to four minutes end to end. A traffic spike arrives in ten seconds. So
for those three or four minutes the **existing fleet takes the entire spike alone**, which means the
steady-state fleet still has to survive the peak unaided. What autoscaling actually saves is money in the
**trough** — at three in the morning — not capacity at the peak. So my pattern would be: reserve the
steady-state fleet, which is also thirty to sixty percent cheaper than on-demand, autoscale the
predictable daily variation, and put a queue in front of anything that can be processed asynchronously,
because a queue is the only thing that genuinely absorbs a spike instantly."

**"What runs out first?"**
"Depends on the product, and I would size all three separately rather than assume. **Compute** scales with
traffic and is elastic. **Storage** scales with time and only ever grows — you cannot autoscale it down,
so the retention policy *is* the capacity plan. **Bandwidth** scales with response size, and for anything
media-heavy it binds first by a wide margin. Concretely: six thousand requests a second of five-kilobyte
JSON is thirty megabytes a second, which is three percent of one machine's network link. The same six
thousand serving two-megabyte images is twelve gigabytes a second — twelve machines' worth of network for
the images alone, which is why that content goes to a CDN. So for a text API compute binds, for a photo
product bandwidth binds, and for a logging system storage binds — and the architecture follows from which
one it is."

**"How confident are you in the thousand-QPS-per-server figure?"**
"Not very, and I would say so rather than pretend. It is an order-of-magnitude assumption and it depends
entirely on what a request actually does — a simple cached lookup might be five thousand a second and
something running a complex query might be two hundred. Since every number downstream is proportional to
it, it is the first thing I would measure: ramp load against a single instance until p99 latency starts
to degrade, and take the QPS just **below that knee**, not the point where it falls over. That knee is the
real capacity. I would rather tell you 'here is the shape of the calculation and here is the one number I
would go and measure' than give you a confident figure built on a guess."

**"How would you size storage?"**
"Bytes per record times records per day times retention times replication — and then two things people
leave out. **Indexes**, which typically add thirty percent to a hundred percent on a well-indexed table.
And **free-space headroom**, because a database on a disk that is ninety-five percent full is in trouble
long before it is full: compaction, vacuum and temporary sort space all need room, so I would provision to
about eighty percent target usage. Concretely: five gigabytes a day of rows, times a year, is 1.8
terabytes; times three replicas is 5.5; plus thirty percent for indexes is 7.2; divided by 0.8 for
headroom is about nine terabytes provisioned for 1.8 terabytes of actual data. That five-times multiplier
is the thing people miss when they quote the raw figure. And the real lever is **retention** — storage is
a ratchet, so 'ninety days hot then archive' is a capacity decision wearing a product decision's clothes."

### A model answer

Asked: *how many servers does this system need?*

> "Let me do the division first and then explain why it is not the answer.
>
> Six thousand requests a second at peak, and roughly a thousand a second per application server, gives
> **six machines**. That is the answer to 'how many are theoretically required'. It is not what I would
> run, and there are three multipliers between that and a real number.
>
> **Utilisation.** A machine at a hundred percent busy is not fully used — it is a machine with an
> unbounded queue. Waiting time grows roughly as utilisation over one minus utilisation, so the curve is
> almost flat up to sixty percent and then goes vertical: at eighty percent requests wait four times
> longer than at fifty, and at ninety percent nine times. That is not a failure; it is what queues do when
> arrivals are bursty, and real traffic is bursty. So I size for about **sixty-five percent**, which turns
> six into **ten**.
>
> **Redundancy.** A machine will fail, or be patched, or be restarted during a deploy, and the fleet has to
> work without it. N+1 takes me to **eleven**.
>
> **Growth.** Capacity has to last until I next provision. Twenty percent for a year takes me to about
> **fourteen**. On cloud infrastructure that multiplier is small, because adding a machine is minutes
> rather than a purchase order.
>
> Then I would **check the failure case**, because the sizing is not finished until I have. Fourteen
> machines, one dies: thirteen carry six thousand, so four hundred and sixty each, forty-six percent —
> fine. A whole availability zone dies, so a third of them: nine carry six thousand, six hundred and
> sixty-seven each, sixty-seven percent — still inside target. If either had come out above eighty percent
> I would add machines, because a failure would then push the fleet into the steep part of the queueing
> curve and the latency damage would be worse than the lost capacity.
>
> Two things I would add unprompted. **Autoscaling does not remove this headroom** — the chain from metric
> window through boot to passing health checks is three to four minutes, and a spike arrives in seconds,
> so the existing fleet takes the whole spike alone for that long. Autoscaling saves money in the trough,
> not capacity at the peak.
>
> And **compute is only one of three plans**. Storage scales with time and only ever grows, so retention is
> the real lever — and the fully-loaded number is about five times the raw data once you count replication,
> indexes and free-space headroom. Bandwidth scales with response size, and it is the one that binds first
> for anything with media: six thousand requests a second of JSON is thirty megabytes a second, and the same
> six thousand serving two-megabyte images is twelve gigabytes a second, which is twelve machines' worth of
> network link. That number is the reason for the CDN.
>
> The one figure I would want to replace with a measurement is the thousand QPS per server. Everything
> above is proportional to it, and the way to get it is a load test that ramps until p99 degrades — the
> capacity is the QPS just below that knee, not where it falls over."

---

## 9. Recall card

- **Peak QPS ÷ per-server QPS is NOT the answer** — it is the answer to "what is theoretically possible".
  Three multipliers follow: **÷ utilisation (0.65) · + redundancy (N+1) · × growth.** 6 machines becomes
  **14**.
- **The one idea that matters: queueing delay grows as `u / (1 − u)`.** Flat to ~60%, then vertical: **80%
  = 4× the wait, 90% = 9×, 99% = 99×.** So **size for 60–70% for user-facing work, 80–90% for batch behind
  a queue** — that difference is the biggest cost lever available.
- **Verify the failure case before answering.** 14 machines, one dies → 13 at 46%; a whole AZ dies → 9 at
  67%. And **redundancy is proportionally cheaper in a big fleet**: losing 1 of 30 costs the survivors
  3.4%, losing 1 of 3 costs them 50%.
- **Autoscaling does not remove headroom.** Metric window + decision + boot + warm-up + health checks =
  **3–4 minutes**, and a spike arrives in seconds — so **the existing fleet takes the whole spike alone.**
  Autoscaling saves money in the **trough**; a **queue** is the only thing that absorbs a spike instantly.
- **Three separate plans, and the binding one is rarely the obvious one.** Compute scales with traffic;
  **storage scales with time and is a ratchet** (retention *is* the plan — and fully loaded it is ~**5×**
  the raw data after replication, **+30% indexes** and **÷0.8 free space**); **bandwidth binds first for
  media** — 6,000 QPS × 5 KB is 30 MB/s, but × 2 MB is **12 GB/s**, twelve machines' worth of link. And the
  per-server figure is an assumption: **load-test to the knee where p99 degrades**, and take the QPS just
  below it.
