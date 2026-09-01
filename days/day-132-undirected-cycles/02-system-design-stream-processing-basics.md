---
day: 132
track: system-design
title: "Stream processing basics"
phase: "Building blocks of big systems"
status: written
---

# Stream processing basics

## 1. What this is, and why they ask it

Stream processing is computing over data that never stops arriving. Not "run a job at midnight over
yesterday's data" — a program that is always running, updating an answer as events come in.

The idea is easy. The difficulty is entirely in one thing: **events do not arrive in the order they
happened.** A phone that was in a lift sends its events four minutes late. A server in another region is
behind. A retry re-delivers something from thirty seconds ago. So when you are asked "how many clicks
happened between 10:00 and 10:01", you have to decide when to stop waiting for stragglers and commit to an
answer — and whatever you choose, some events will arrive after you have answered.

They ask this because it is where "just count the events" stops being easy, and because the vocabulary —
**windows**, **event time**, **watermarks**, **late events** — is used loosely by people who have not thought
about it. An interviewer asking "how do you count events per minute when events arrive late?" is checking
whether you know that the question has no clean answer, only a set of explicit trade-offs.

It sits directly on [day 130](../day-130-grids-are-graphs/README.md)'s Kafka and feeds
[day 168](../day-168-sweep-line/README.md)'s ad-click aggregator, which is the full case study.

By the end of this lesson you can explain windowing without jargon, state the difference between event time
and processing time and why it matters, describe what a watermark actually is, choose a lateness policy with
a number attached, and say what you do about the event that arrives after you have already published the
answer.

---

## 2. The story

Shalini closes the shop at ten, and closing the shop means counting the day.

The counting itself takes about six minutes. Cash from the drawer, the card machine total, and the amounts
the two delivery boys bring back, and then a figure for the day that goes into her phone and that she has kept
every day for eleven years.

The delivery boys are the problem, and they always have been.

Ravi is usually back by five past ten. Sohail is not. Sohail's last drop is often the flats behind the
petrol pump, and there is a gate there that shuts at ten, so some nights he has to go round, and he gets back
at twenty past.

For a long time Shalini simply waited. She sat there until both of them were in, and some nights that was
half past ten, and the whole family ate late.

What she does now is she waits until quarter past. That is the rule. At quarter past ten she counts what she
has, writes the figure down, and that is the day. If Sohail walks in at twenty past with three hundred rupees
from an order taken at half past nine, that money is a real part of Tuesday's business and it goes into
Wednesday's count.

She picked quarter past because she watched for a couple of weeks. Almost every night both boys are back
before then. About once a fortnight one of them is not.

Two things follow from that rule and she has thought about both.

The first is that her daily figures are slightly wrong, always, in a way that mostly cancels out. Tuesday is
three hundred short and Wednesday is three hundred over. Over a month it does not matter. For the monthly
total it does not matter at all, because the money is in there somewhere.

The second is that some nights it does matter, and then she breaks her own rule. On the last day of the month
she waits for Sohail however late he is, because a month boundary is a real boundary and money on the wrong
side of it makes the accounts harder to explain than a late dinner.

And there is a third thing, which happened once, in 2022. Sohail's cycle chain broke near the highway and he
did not get back until quarter to twelve, with eleven hundred rupees. Shalini had already written the figure
down and sent it to her husband. She went back into her phone, corrected Tuesday, and sent a message saying
the earlier number was wrong.

She does not like doing that. But eleven hundred was too big to just push into Wednesday and forget.

---

## 3. The idea in plain English

Shalini has built a stream processor, including the parts that people skip.

**A stream is data that keeps arriving.** No end, no "all the data". You cannot wait for it to finish, because
it does not finish. That single fact rules out every technique that assumes you can see everything before you
answer.

**A window is a bucket of time you compute over.** Shalini's day. In code: "clicks per minute", "revenue per
hour", "errors in the last five minutes". Windows come in three shapes:

- **Tumbling** — fixed, non-overlapping. 10:00–10:01, 10:01–10:02. Every event is in exactly one. This is
  Shalini's day and it is what you want most of the time.
- **Sliding** — fixed length, overlapping, advancing by a smaller step. "The last five minutes, recomputed
  every minute." An event belongs to five windows at once, so the work is five times as much.
- **Session** — no fixed length; a window ends after a gap of inactivity. "A user's browsing session ends
  after 30 minutes of nothing." Used for anything about a person's activity, where the natural boundary is
  behaviour rather than the clock.

**Now the distinction the whole subject rests on: event time against processing time.**

**Event time** is when the thing actually happened — the order was taken at half past nine. **Processing
time** is when your system found out about it — Sohail walked in at twenty past ten. **These are different,
and the gap is unpredictable.**

**Almost always you want event time.** "How many orders were placed between nine and ten" is a question about
when orders were placed, not about when the message reached your server. If you count by processing time,
your numbers change depending on how fast your network was, which makes them useless for comparison and
impossible to reproduce.

**And event time is what makes it hard**, because if you are bucketing by when things happened, you can never
be certain a bucket is complete. There might always be one more event on its way from a phone that was in a
lift.

**A watermark is a promise about how far behind you might be.** A watermark of "10:00" means: *I believe I
have now seen essentially all events that happened before 10:00.* It is Shalini's quarter past ten — the
moment she declares the day's takings complete.

**A watermark is a guess, and it is chosen, not derived.** The usual method is exactly hers: watch the actual
delay for a while, and set the watermark to lag by more than almost all of it. If 99% of events arrive within
90 seconds, a watermark lagging two minutes is right. **The number comes from measurement, and if you cannot
say where yours came from, you have not chosen it.**

**A late event is one that arrives after its window's watermark has passed.** Sohail at twenty past. You have
three choices and they are all legitimate:

1. **Drop it.** Simplest. The window is closed and the event is discarded, usually with a counter so you know
   how many you are losing. Right for approximate dashboards.
2. **Put it in the current window.** Shalini's default: Tuesday's money goes into Wednesday. The total over a
   long period is right; the per-window numbers are individually wrong. Right when only the aggregate matters.
3. **Reopen the window and correct the answer.** The 2022 cycle chain. The most correct and the most
   expensive: you must keep the window's state around for a defined **allowed lateness** period, and every
   downstream consumer must be able to handle a corrected number replacing one it already received.

**Allowed lateness is a second number, and it is not the watermark.** The watermark says when you emit an
answer. Allowed lateness says how much longer you keep the state so you can revise it. Emit at two minutes,
keep state for an hour, drop anything later than that.

**And "keep the state" is the real cost.** A stream processor computing per-minute counts for ten million
users must hold one counter per user per open window. **Every window you keep open is memory**, and allowed
lateness multiplies it directly.

**The month-end rule is the last idea: some boundaries cannot be fudged.** Shalini waits for Sohail on the
last day of the month. In a system, a billing period or a regulatory report is a boundary where "it will come
out in the wash" is not acceptable, and you either wait, or you publish a provisional figure and a final one.
**Knowing which of your outputs are provisional is part of the design.**

---

## 4. The picture

The three window shapes on the same stream:

```
events:      a    b       c   d      e         f    g
time:    |---+----+-------+---+------+---------+----+-----|
        10:00   10:01   10:02   10:03   10:04   10:05

TUMBLING (1 minute)
        [ 10:00-10:01 ][ 10:01-10:02 ][ 10:02-10:03 ][ ... ]
             a, b            c, d           e
        every event in exactly ONE window

SLIDING (2 minutes, every 1 minute)
        [ 10:00-10:02       ]
                [ 10:01-10:03       ]
                        [ 10:02-10:04       ]
        every event in TWO windows -> 2x the state and 2x the work

SESSION (gap of 90 seconds)
        [ a b ]        [ c d ]                 [ f g ]
        closed by inactivity, not by the clock
```

**What to notice.** Sliding windows multiply everything by the overlap factor. A five-minute window sliding
every ten seconds means each event is in thirty windows, which is thirty times the state and thirty times the
update work — a completely different sizing conversation from the tumbling version.

Event time against processing time, which is the picture worth memorising:

```
             EVENT TIME (when it happened)
                 |
   9:58   9:59  10:00  10:01  10:02
     |      |     |      |      |
     A      B     C      D      E
      \      \     \      \      \
       \      \     \      \      \        arrival delay varies
        \      \     \      \      \
   ------+------+-----+------+------+------> PROCESSING TIME
        10:00  10:01 10:01  10:02  10:07
                                     ^
                                     |
                              E happened at 10:02
                              and arrived at 10:07

   window 10:00-10:01 by EVENT time      -> {C}
   window 10:00-10:01 by PROCESSING time -> {A, B, C}   <- wrong bucket entirely

   watermark at processing 10:03 says "I have everything before event time 10:01"
   E arrives at 10:07 -> LATE by 4 minutes
```

**What to notice.** The two groupings give different answers for the same minute, and only one of them is
reproducible. Re-run the same stream tomorrow on a faster network and the processing-time answer changes; the
event-time answer does not.

And the watermark advancing, which is the mechanism:

```
watermark = (largest event time seen so far) - allowed_delay

  seen event times:  9:58, 9:59, 10:00, 10:01
  max = 10:01, allowed_delay = 2 min
  watermark = 9:59      -> windows ending at or before 9:59 may be closed

  a new event arrives with event time 10:05
  max = 10:05
  watermark = 10:03     -> windows up to 10:03 close, and emit

  NOTE: the watermark only moves when NEW events arrive.
  A quiet stream never closes its windows. That is a real production incident.
```

**What to notice at the last line.** If a partition stops receiving events — a device goes offline, a region
goes quiet at night — its watermark stops advancing, and because the overall watermark is the *minimum* across
partitions, **one idle partition freezes the whole job's output.** Systems handle this with an idle-source
timeout, and knowing about it is a strong signal.

---

## 5. How it actually works

### The systems

| System | Model | Windows | Event time | State |
|---|---|---|---|---|
| **Flink** | true streaming, event at a time | all three | first-class, with watermarks | RocksDB-backed, checkpointed |
| **Kafka Streams** | library, runs in your app | tumbling, hopping, session | yes, with grace periods | local RocksDB + changelog topic |
| **Spark Structured Streaming** | micro-batch (and continuous) | tumbling, sliding | yes, with watermarks | checkpointed |
| **Kinesis Data Analytics** | managed Flink | as Flink | as Flink | managed |
| **ksqlDB** | SQL over Kafka Streams | tumbling, hopping, session | yes | as Kafka Streams |

**The distinction worth knowing: true streaming versus micro-batch.** Flink processes each event as it
arrives — latency in milliseconds. Spark Structured Streaming groups events into small batches, typically
hundreds of milliseconds to seconds — higher latency, and simpler recovery because a batch is a unit. **For
most business use cases the difference does not matter**, and Spark's advantage is that the same code runs
over historical data.

### What the code actually looks like

Kafka Streams, counting clicks per minute per ad:

```java
builder.stream("clicks")
       .groupByKey()
       .windowedBy(TimeWindows.ofSizeAndGrace(
            Duration.ofMinutes(1),          // window size
            Duration.ofMinutes(10)))        // allowed lateness ("grace")
       .count()
       .toStream()
       .to("clicks-per-minute");
```

Two numbers, and they are the two decisions from section 3: the window size and how long you keep the state
open for corrections.

Flink, the same thing, with the watermark declared explicitly:

```java
stream.assignTimestampsAndWatermarks(
          WatermarkStrategy
              .<Click>forBoundedOutOfOrderness(Duration.ofSeconds(90))
              .withTimestampAssigner((e, t) -> e.eventTime))
      .keyBy(click -> click.adId)
      .window(TumblingEventTimeWindows.of(Time.minutes(1)))
      .allowedLateness(Time.minutes(10))
      .sideOutputLateData(lateTag)          // late events go somewhere, not nowhere
      .aggregate(new CountAggregate());
```

**`forBoundedOutOfOrderness(90 seconds)` is the watermark**, stated as a number in the code — "I assume events
are at most 90 seconds out of order". `allowedLateness(10 minutes)` is how long state is kept for revisions.
And `sideOutputLateData` is the line most people leave out: **events later than the allowance go to a separate
stream rather than being silently dropped**, so you can count them and know whether your 90 seconds was right.

### State, and what makes it survivable

A stream processor holds state — the running count for every open window for every key. Two things make that
production-grade:

**Local state with a durable changelog.** Kafka Streams keeps state in RocksDB on the local disk and writes
every change to a compacted Kafka topic. If the instance dies, a new one replays the changelog and rebuilds.
Fast reads, no remote lookup per event, and recovery is bounded by the changelog size.

**Checkpointing.** Flink periodically snapshots all operator state and the source offsets together, atomically.
On failure it restores the snapshot and rewinds the sources to the matching offsets. **That pairing — state
and offsets in one snapshot — is what gives exactly-once *effect* within the job**, in exactly the sense from
[day 122](../day-122-autocomplete/README.md). The moment the job writes to an external system, the guarantee
needs an idempotent sink or a transactional one.

### Triggers: when to emit

The default is "emit once, when the watermark passes the window's end". Two other patterns are common:

- **Early firing** — emit a partial result every ten seconds while the window is still open, so a dashboard
  updates continuously. The consumer must understand that the number will change.
- **Late firing** — emit an updated result when a late event arrives within the allowed lateness. The consumer
  must be able to *replace* the previous value rather than add to it.

**Both mean downstream receives more than one answer for the same window, and the design has to say what
downstream does with that.** The usual answer is that the sink is keyed by window so a later write overwrites
the earlier — an upsert, not an append. If the sink appends, early and late firing double-count.

### The idle-partition problem

The overall watermark is the **minimum** across all input partitions, because the job cannot claim to have
seen everything before time T until every partition has. So a single partition with no traffic holds the
watermark back, and no windows close anywhere.

This happens constantly in real deployments: a device fleet where some devices are asleep, a region that goes
quiet overnight, a topic partition that gets no traffic because of a skewed key. The fix is
`withIdleness(Duration)` in Flink or its equivalent, which excludes a partition from the watermark calculation
after a period of silence. **"The dashboard stopped updating at 2 a.m. and there was no error" is the symptom**,
and it is a good thing to have a story about.

### Joining two streams

Joining a stream to a table (enriching clicks with ad metadata) is straightforward: keep the table in local
state and look up per event.

Joining a stream to a stream — impressions to clicks, orders to payments — needs a **window**, because you
cannot hold every impression forever waiting for a click. "Join a click to an impression within thirty
minutes" means keeping thirty minutes of impressions in state:

```
1,000,000 impressions/minute x 30 minutes = 30,000,000 rows in state
x 200 bytes                               = 6 GB per instance-set
```

**The join window is a memory decision disguised as a business rule**, and it is worth stating the number.

---

## 6. The numbers

**Window count and state size.** Per-minute counts for ten million users:

```
keys                      10,000,000
open windows per key      1 (tumbling, no lateness)
state per entry           ~100 bytes (key + count + timestamps)
                          ------------------------------
                          10,000,000 x 100 = 1 GB
```

Now add allowed lateness of ten minutes:

```
open windows per key      10 (one per minute still open)
                          10,000,000 x 10 x 100 = 10 GB
```

**Allowed lateness multiplies state linearly, and it is the number people forget.** Ten minutes of grace on a
one-minute window is ten times the memory.

And a sliding window makes it worse:

```
5-minute window, sliding every 10 seconds
windows an event belongs to  = 300 / 10 = 30
state                        10,000,000 x 30 x 100 = 30 GB
update work per event        30 counter updates instead of 1
```

**Thirty times the memory and thirty times the CPU**, from one configuration line. If someone asks for "the
rolling five-minute count updated every ten seconds", that is what they have asked for, and it is worth
pricing before agreeing.

**Choosing the watermark from measured delay.** Measure `processing_time − event_time` over a day:

```
p50    1.2 s
p95    8 s
p99    45 s
p99.9  4 min
max    2 h        (a phone that was offline)
```

```
watermark lag = 60 s   ->  drops ~1% of events
watermark lag = 5 min  ->  drops ~0.1%, adds 5 min of latency to every window
watermark lag = 2 h    ->  drops ~0, and results are 2 hours stale
```

**That table is the whole decision**, and the answer depends entirely on what the output is for. A live
dashboard takes 60 seconds and 1% loss. A billing figure takes the two hours, or is published provisionally and
finalised.

**Throughput.**

```
Flink, simple aggregation      ~ 1,000,000 events/s per core-ish (heavily workload-dependent)
Kafka Streams                  ~ 100,000 - 500,000 events/s per instance
Spark micro-batch              higher throughput, latency 100 ms - seconds
```

**Latency, end to end:**

```
event happens                       t = 0
reaches Kafka                       + 50 ms - 2 s
consumed by the job                 + 10 ms
window closes (watermark lag)       + 60 s      <- this dominates
result written                      + 20 ms
                                    ----------
                                    ~ 61 s
```

**The watermark lag is almost always the dominant term**, which is worth saying explicitly: tuning the
processor's internals is pointless when 98% of the latency is a number you chose.

**Late-event volume, and why the side output matters:**

```
1,000,000 events/minute
0.1% arrive after a 10-minute allowance
                          = 1,000 events/minute discarded
                          = 1,440,000 per day
```

**One and a half million discarded events a day.** If they go to a side output you can count them, see which
sources produce them, and decide. If they are dropped silently you find out when someone reconciles against a
batch job and the numbers differ by 0.1%.

**And the reconciliation number that makes the design defensible:**

```
streaming count for yesterday    9,998,600
batch recount over the raw log   10,000,000
difference                       0.014%
```

**Running a nightly batch recount over the same raw data and comparing is the standard practice**, and it is
what turns "our streaming numbers are approximately right" into a number you can put in a document.

---

## 7. The trade-offs

**Latency against completeness, and this is the whole subject.** A short watermark lag gives fast answers and
drops more events. A long one gives complete answers late. There is no setting that gives both, and the right
answer depends entirely on what the number is used for — a dashboard and an invoice sit at opposite ends. **If
someone asks for "real-time and exactly right", they are asking for two things, and the design conversation is
which one to relax.**

**Event time against processing time.** Event time gives correct, reproducible buckets and requires
watermarks, state retention and a lateness policy. Processing time is trivial, has no late events by
definition, and produces numbers that change if your network is slow. **Use processing time only when the
question really is about your system** — "how many requests did we handle this minute" — and never for
anything about the outside world.

**Allowed lateness against memory.** Every minute of grace multiplies open windows. Ten minutes on a
one-minute window over ten million keys is ten gigabytes rather than one. And it is not just memory: it is
checkpoint size, recovery time, and how much state has to be shipped when the job rescales.

**Correcting results against a simple downstream contract.** Emitting a revised number for a closed window is
the most correct option and it forces every consumer to handle updates — the sink must upsert, the dashboard
must replace rather than accumulate, and anyone who copied the earlier number has a stale figure. **Many teams
choose to be slightly wrong rather than make every consumer handle revisions**, and that is a legitimate
engineering decision as long as it is decided rather than defaulted.

**Streaming against batch.** A streaming job is always running, always costing money, and fails at three in
the morning. A batch job runs once, is trivially re-runnable, and gives an answer hours later. **If the answer
is only looked at once a day, a batch job is a better engineering decision than a streaming one**, and saying
that is worth more than knowing Flink's API.

**And the honest position on exactly-once.** Flink's checkpoints give exactly-once *within the job* by
snapshotting state and source offsets together. As soon as the job writes to an external system, you need an
idempotent or transactional sink, and you are back to
[day 122](../day-122-autocomplete/README.md)'s idempotency keys. Claiming exactly-once without naming the sink
is the tell that someone has read a marketing page.

**When would I not use stream processing?** When the answer is consumed daily — batch is simpler and cheaper.
When the aggregation is small enough to do with a counter in Redis and a cron job, which covers a surprising
number of real "real-time metrics" requirements. And when the team is small, because a Flink cluster is a
serious operational commitment and a mis-tuned watermark produces wrong numbers silently, which is worse than
a batch job that fails loudly.

---

## 8. In the interview

### How it gets asked

- *"How do you count events per minute when events arrive late?"* — the direct version.
- *"What is the difference between event time and processing time?"*
- *"What is a watermark?"*
- *"An event arrives an hour late. What happens to it?"*
- *"Your dashboard stopped updating overnight and there were no errors. Why?"* — the idle-partition question.
- *"Design a real-time analytics pipeline."* — where all of this shows up as follow-ups.

### The first ninety seconds

> "The counting is easy; the ordering is the problem. Events do not arrive in the order they happened — a
> phone that was in a lift sends four minutes late, a retry replays something from thirty seconds ago — so the
> real question is when I stop waiting for a minute's events and commit to a number.
>
> **First decision: I bucket by event time, not processing time.** 'How many clicks happened between 10:00 and
> 10:01' is a question about when the clicks happened. If I bucket by arrival, the same stream replayed on a
> faster network gives different numbers, which makes them useless for comparison.
>
> **Second: a watermark.** A watermark of 10:01 is a claim that I have now seen essentially everything that
> happened before 10:01, so windows ending at or before then can be closed and emitted. It is a guess and I
> choose it from measurement — I would look at the actual distribution of `arrival minus event time` and set
> the lag above the p99. If p99 is forty-five seconds, a ninety-second watermark drops about one percent of
> events and adds ninety seconds of latency to every result.
>
> **Third: a policy for what is later than that.** Three options and I would say which and why. Drop it, with
> a counter, if the output is a dashboard. Fold it into the current window, so the total over an hour is right
> and individual minutes are slightly wrong. Or keep the window's state open for a defined allowed lateness —
> say ten minutes — and emit a corrected value. The third is the most correct and it forces every downstream
> consumer to handle a number being revised, so the sink has to upsert by window rather than append.
>
> **And whichever I choose, late events go to a side output rather than nowhere**, so I can count them and find
> out whether my ninety seconds was right.
>
> The cost I would flag immediately is state: ten million keys with a one-minute window is about a gigabyte,
> and ten minutes of allowed lateness makes it ten. Allowed lateness multiplies memory linearly.
>
> What is this number used for — a dashboard, or billing? Because that changes the watermark and the lateness
> policy completely."

### The follow-ups

**"What actually is a watermark? Be precise."**

> "It is a marker flowing through the stream that says 'no more events with an event time earlier than T are
> expected'. When it passes the end of a window, that window is complete and can be emitted.
>
> Mechanically, the common strategy is: watermark equals the largest event time seen so far, minus a fixed
> allowance for out-of-orderness. So if I have seen events up to 10:05 and my allowance is two minutes, the
> watermark is 10:03, and every window ending at or before 10:03 fires.
>
> Two consequences that matter and that people miss.
>
> **It is a heuristic, not a fact.** Nothing prevents an event with time 10:01 from arriving after the
> watermark passed 10:03. That event is late by definition, and what happens to it is a separate policy.
>
> **And it only advances when new events arrive**, because it is derived from the maximum event time seen.
> That is the source of a very specific production incident: if a partition goes quiet — a region overnight, a
> device fleet asleep — its watermark stops moving, and since the job's watermark is the *minimum* across
> partitions, **one idle partition freezes output everywhere.** The symptom is a dashboard that stops updating
> with no error at all. The fix is an idleness timeout that excludes a silent partition from the calculation
> after a while."

**"An event arrives an hour late. Walk me through what happens."**

> "It depends on two numbers I have already chosen, and I would restate them: the watermark lag, which decides
> when a window emits, and the allowed lateness, which decides how long I keep the state so I can revise.
>
> Say watermark lag is ninety seconds and allowed lateness is ten minutes. An event an hour late is past both.
> Its window closed fifty-eight minutes ago and its state has already been discarded, so I cannot revise the
> answer even if I wanted to.
>
> So it goes to the **side output** — a separate stream of late events. Not dropped silently. From there I do
> one of three things depending on what the pipeline is for. For a dashboard, I count them and expose 'late
> events per minute' as a metric, because a rise in that number means my watermark assumption has broken. For
> something that has to be right, they go into a table that a nightly batch job reconciles against, and the
> corrected figures replace the streaming ones. For billing, I would not rely on the streaming number at all —
> I would use the stream for the live view and a batch recount over the raw log as the number of record.
>
> **The thing I would push back on** is a design that just discards them inside the operator. One and a half
> million discarded events a day at a one-million-per-minute stream with a 0.1% late rate is a real number, and
> the only way to know it is real is to have kept it."

**"How do you know your streaming numbers are right?"**

> "I do not, and the design should say so. What I do is measure the disagreement.
>
> The standard practice is a nightly batch job that recomputes the same aggregation from the raw event log —
> the log is retained anyway — and compares it with what the streaming job published. The difference is a
> number I put on a dashboard: 'streaming counted 9,998,600 and batch counted 10,000,000, a gap of 0.014%'.
>
> That gives me three things. It tells me the streaming figures are trustworthy within a stated tolerance,
> which is much better than claiming they are exact. It turns a broken watermark or a stuck partition into a
> visible metric rather than a silent drift. And it gives me the authoritative number for anything that matters
> — billing, reporting — while the stream handles the live view.
>
> This is essentially the lambda architecture, and I would name it and also name the criticism: two code paths
> computing the same thing will diverge, and someone has to maintain both. The modern answer is a kappa
> architecture — one streaming code path, replayed over historical data from Kafka when you need a recount —
> which avoids the duplication as long as your retention is long enough to replay."

**"Tumbling, sliding or session windows here?"**

> "Tumbling unless there is a reason, because it is the cheapest and every event is in exactly one window.
>
> **Sliding** when the question is genuinely about a rolling period — 'alert if errors in the last five
> minutes exceed a threshold' — and I would price it before agreeing. A five-minute window advancing every ten
> seconds means every event belongs to thirty windows, so thirty times the state and thirty times the update
> work. That is a real number and it changes the cluster size.
>
> **Session** when the boundary is behaviour rather than the clock — user sessions, a device's period of
> activity, a support conversation. The gap parameter is the whole design: thirty minutes of inactivity ends a
> session is a product decision, not a technical one, and it should come from looking at the actual
> distribution of gaps.
>
> A cheaper alternative to sliding that is worth offering: keep tumbling one-minute windows and have the
> *consumer* sum the last five. One thirtieth of the state, and the trade is that the granularity of the
> rolling figure is a minute rather than ten seconds. For most alerting that is completely acceptable and
> nobody asks for it because they did not know it was an option."

### The model answer

*"Design a system that shows, in near real time, how many times each video on a platform was watched in the
last minute. Ten million events a second at peak."*

> "Let me settle the two numbers that decide everything, then the pipeline.
>
> **The two numbers are the watermark lag and the allowed lateness**, and both come from measurement. I would
> instrument the ingest path first and look at the distribution of `arrival − event_time`. Mobile clients
> batch and retry, so I would expect a long tail: p50 around a second, p99 around a minute, and a small
> fraction of events hours old from devices that were offline. On that shape I would set a watermark lag of
> ninety seconds — covering p99 — and allowed lateness of ten minutes.
>
> **Bucketing by event time**, one-minute tumbling windows, keyed by video ID. Not processing time: 'watches
> per minute' is a fact about viewers, and it has to be reproducible if we replay.
>
> **The pipeline.** Clients publish to Kafka, partitioned by video ID so all events for one video land on one
> partition and are ordered — and so the aggregation is local, with no shuffle per event. Ten million a second
> at, say, 200 bytes is 2 GB/s, which at 250 MB/s per broker and replication factor 3 is about 24 brokers.
> Partitions: a few thousand, driven by consumer parallelism rather than by throughput.
>
> **A Flink job** reading that topic, keyed by video, tumbling one-minute event-time windows, with the
> watermark and lateness above and `sideOutputLateData` on. Output goes to a store keyed by
> `(video_id, minute)` — so a revision **overwrites** rather than appends, which is what makes late firing
> safe. I would use something built for this shape rather than a relational table.
>
> **State sizing, which is the part I would show the arithmetic for.** Ten million events a second, but the
> state is per *video*, not per event. Say two million distinct videos watched in any given minute, at about
> 100 bytes each: that is 200 MB per open window. With ten minutes of allowed lateness, ten windows stay open,
> so 2 GB — spread across the job's parallel instances, so a few hundred megabytes each. Very comfortable, and
> the point is that it is driven by key cardinality, not by event rate.
>
> **Hot keys are the real risk**, not volume. A single viral video can be a large fraction of all events, and
> since I keyed by video ID that is one partition and one task doing that work. Two mitigations: pre-aggregate
> at the edge — each ingest node counts locally for a second and emits partial counts, which cuts the event
> rate into the job by orders of magnitude for exactly the hot keys — and, if that is not enough, salt the key
> for the top videos into `video_id#0..9` and sum the ten at read time. **Pre-aggregation is the one I would
> do first**, because it helps everything and costs a second of extra latency.
>
> **What the user sees, and what I would be honest about.** The dashboard number for the minute 10:00–10:01
> appears at about 10:02:30 — ninety seconds of watermark plus processing — and it may be revised upward once
> or twice over the following ten minutes as late events arrive. So the UI shows the last complete minute, and
> anything more recent is marked as partial. **A design that pretends the current minute's number is final is
> lying**, and users work that out and stop trusting the whole thing.
>
> **And the correctness answer.** The streaming figures are the live view, with a stated tolerance. A nightly
> batch job recomputes from the raw Kafka log and the difference is published as a metric. Anything that
> matters — creator payouts, reported figures — uses the batch number, not the stream. That separation is what
> lets me choose ninety seconds instead of two hours."

---

## 9. Recall card

**Stream processing is computing over data that never ends, and the whole difficulty is that events arrive out
of order.** Bucket by **event time** (when it happened, reproducible), never processing time (when you found
out, depends on your network).

**A watermark is a promise: "I have seen essentially everything before time T."** Usually `max event time seen
− a fixed allowance`, and the allowance comes from measuring the actual delay distribution — set it above p99.
It only advances when events arrive, so **one idle partition freezes the whole job's output.**

**Late events need a stated policy:** drop with a counter, fold into the current window, or keep state for an
**allowed lateness** and emit a correction — which forces every sink to upsert by window rather than append.
Send them to a side output either way, so you can count them.

**Windows: tumbling (one window per event, cheapest), sliding (multiplies state and CPU by the overlap —
a 5-minute window every 10 seconds is 30×), session (ends on a gap).**

**Latency is dominated by the watermark lag you chose, not by the engine.** And the way you know the numbers
are right is a nightly batch recount over the raw log, published as a percentage difference.
