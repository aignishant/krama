---
day: 168
track: system-design
title: "Design an ad click aggregator"
phase: "High-level design case studies"
status: written
---

# Design an ad click aggregator

## 1. What this is, and why they ask it

An ad click aggregator counts events — impressions and clicks — and answers questions about them: **how many
clicks did this campaign get in the last hour, broken down by country?**

They ask it because **it is the canonical streaming-aggregation problem, and it is the one design in this set
where counting is the entire product.** Everything else here stores things and retrieves them. **Here the raw
events are almost worthless individually and the aggregates are what people pay for.**

Three things make it hard, and they are all about counting rather than about scale.

**The volume is enormous and the payload is tiny.** A million events a second at a hundred bytes each. **That
is a different shape from anything else this month** — it is not a storage problem, it is a *throughput and
aggregation* problem.

**And the money makes correctness matter in an unusual way.** **Advertisers pay per click**, so an
overcount is fraud and an undercount is lost revenue. **But the events arrive at-least-once**, so duplicates
are guaranteed by the transport — **and reconciling "exactly-once counting" with "at-least-once delivery" is
the design.**

**Then late data, which is the part people underestimate.** A phone goes into a tunnel and reports its clicks
twenty minutes later. **Which hour do they belong to — the hour they happened, or the hour they arrived?** The
answer decides whether your reports are correct or merely available, **and every stream-processing system has
a name for this problem because it is unavoidable.**

**And the fourth thing, which is the interesting inversion: the dashboard queries are not over raw events at
all.** Nobody scans a trillion rows. **The aggregates are computed as the data arrives and stored
pre-summed** — which is yesterday's sweep-line idea applied to a stream: **process events in order,
accumulate, and never look back.**

By the end of this lesson you can design the ingestion path, aggregate in a stream with windows, handle late
and duplicate events, serve the queries, and reconcile the fast path against a batch recomputation.

---

## 2. The story

The mill weighed lorries in and out and Sarojini had run the weighbridge for nineteen years, and the whole of
her job was one number per lorry.

**Weight in, minus weight out. That was the cane.**

And the number mattered in a way nothing else at the mill mattered, **because the farmers were paid on it.**

**Her first system was a register with every lorry in it.** Registration number, time, weight in, weight out.
Eleven hundred lorries a day in the season. **And when the office wanted to know how much cane had come in
from the Nandigama villages that week, somebody sat down with the register and added it up, and it took two
hours and it was wrong about a third of the time.**

**So she started keeping the totals as she went.**

A board on the wall with the villages down the side. **A lorry weighs out, she does the subtraction, and she
adds it to that village's line immediately.** The register still recorded every lorry — **the totals were not
instead of it, they were as well as it** — but the question the office asked was already answered before they
asked it.

**Two hours became a glance.**

And then two things went wrong, in the second season, and both took her a while.

**The first was the lorry that came back.** A driver would weigh in, go off to the yard, and weigh out four
hours later — **and sometimes the paperwork for a lorry from the morning arrived at her window in the
evening**, because it had gone round the wrong way.

**Which village's line did it go on?** The one for the day it arrived, or the day it was weighed? **She had
been adding it to today, and the Nandigama total for Tuesday was wrong for a week before anybody noticed.**

**The second was worse and it took a season to find.** A clerk, trying to be helpful, wrote a lorry into her
board when it weighed in **and again when it weighed out.** Every lorry that clerk handled was counted twice.

**And she could not tell from the board.** The board only had totals. **The only way she found it was by
adding up the register, by hand, for one day** — and comparing.

After that she did that every Sunday, for the whole of the rest of her career.

**"The board is for answering. The register is for being right,"** she told the man who replaced her. **"They
should agree. When they do not, the register is what happened."**

---

## 3. The idea in plain English

Sarojini's board is the streaming aggregate, her register is the raw event log, and her Sunday is
reconciliation. **Those three things are the whole architecture.**

**Start with the shape, because it is unlike everything else this month.**

```
   EVENTS                          AGGREGATES
   1,000,000/second                a few thousand queries/second
   ~100 bytes each                 "clicks for campaign X, last hour,
   individually worthless           by country"
   ~100 GB/day                     tiny
   at-least-once                   must be exactly right — money
```

**The raw events are a firehose of tiny, individually meaningless records.** **The product is the sums**, and
nobody ever queries a single click.

**Which means the central design move is: aggregate on the way in, not on the way out.**

**Nobody scans a trillion rows to answer "clicks last hour".** The counts are computed as the events arrive
and stored already summed — **and a query is a lookup, not a scan.**

**That is yesterday's sweep line applied to a stream**: process events in time order, accumulate into a running
total, **and never look back at individual events.**

**Now the pipeline, which is five stages.**

```
   1. INGEST     a tiny endpoint that does almost nothing
   2. QUEUE      Kafka, partitioned — the durable buffer
   3. AGGREGATE  stream processing into time windows
   4. STORE      pre-summed counts, by dimension and window
   5. SERVE      the dashboard, which does lookups
```

**Stage one must be as small as possible.** The click endpoint's only job is **to write the event to the queue
and return** — no validation beyond the minimum, no enrichment, no database write. **It sits on the path of
every ad interaction on the internet**, so its latency and availability are the product's.

**Stage two is the durable buffer**, and it is what makes everything downstream restartable. **If the
aggregator falls over, the events are still in Kafka** and it resumes from its offset. **Without the queue, a
crash loses whatever was in flight** — and those are clicks somebody is being charged for.

**Partition by campaign** rather than randomly, **so all the events for one campaign land on one partition and
one aggregator instance**, which makes the aggregation local and removes cross-instance coordination
entirely.

**Stage three is the interesting one: windowed aggregation.**

**"How many clicks in the last hour" needs the events bucketed by time.** A tumbling window — fixed,
non-overlapping, one-minute buckets — is the usual choice, **and one-minute granularity is fine enough that
hourly, daily and monthly totals are all sums over minute buckets.**

**And that is why minute buckets are the right unit**: they are small enough to answer any window a dashboard
asks for and large enough that there are not too many of them.

**Now the two hard problems: event time against processing time, and duplicates.**

**Event time is when the click happened. Processing time is when your system saw it.** They differ by
milliseconds usually and by **twenty minutes** for a phone that went into a tunnel.

**Bucketing by processing time is easy and wrong**: Tuesday's report includes clicks from Monday, and Monday's
report changes if you rerun it. **Bucketing by event time is correct and means a window is never truly
closed** — a late event can always arrive for an hour you already reported.

**The standard resolution is a watermark**: a moving estimate of "we have probably seen everything up to time
T". **Windows are closed when the watermark passes them, with a grace period** — typically minutes — **and
anything later goes to a separate late-data path** rather than being silently dropped or silently
incorporated.

**And the honest framing is that there is no correct answer, only a stated one.** **Wait longer and the
numbers are more complete and less timely; wait less and the reverse.** Naming the trade-off is what is being
tested.

**Then duplicates, which are guaranteed rather than possible.**

**Kafka is at-least-once. Network retries happen. A client that does not get an acknowledgement resends.**
**So an event will be delivered twice**, and each duplicate is a click somebody pays for.

**The answer is a client-generated event id and deduplication in a window.** The client — the ad SDK — assigns
an id when the click happens; **the aggregator keeps recently-seen ids and drops repeats.**

**And the window is the compromise.** Keeping every id forever is impossible at a million a second. **Keeping
an hour of them is about 3.6 billion ids** — which is where a Bloom filter or a sketch becomes attractive,
**with the honest cost that a false positive drops a real click.**

**Then stage four: what to store.**

**Not the raw events, for querying.** Pre-aggregated counts, keyed by the dimensions people actually filter
on: **campaign, country, device, minute.**

**And the dimensionality is the thing that explodes.** Every extra dimension multiplies the number of rows —
**campaign × country × device × ad-slot × minute is a very large number** — so **you store the combinations
people actually query and not the full cross-product.**

**Stage five is a lookup**, and it is why the whole design exists: a dashboard asking for "campaign 4471,
today, by country" **reads a few hundred pre-summed rows** rather than scanning a hundred billion events.

**And finally: the two paths, which is Sarojini's board and register.**

**The streaming aggregate is fast and approximately right.** It has deduplicated within a window, closed
windows on a watermark, and dropped some late data.

**The raw event log is slow and exactly right.** It is every event, kept.

**So: recompute the aggregates from the raw log periodically — nightly — and reconcile.** The batch numbers
replace the streaming ones for closed periods. **The stream serves the last few hours; the batch serves
everything older.**

**That is the lambda architecture**, and it is much criticised for the duplicated logic — **and for billing
data it remains the honest answer**, because a fast approximate number and a slow exact one are genuinely
different products and you need both.

---

## 4. The picture

The shape, which is unlike the rest of this month:

```
   EVENTS IN                        QUERIES OUT

   1,000,000/second                 ~1,000/second
   ~100 bytes each                  "campaign 4471, last hour,
   individually meaningless          by country"
   ~100 GB/day raw                  ~200 rows

   -> a THROUGHPUT problem on the way in
   -> a LOOKUP problem on the way out
   -> and NOBODY EVER SCANS THE RAW EVENTS to answer a query
```

The pipeline:

```
   ad SDK
     |  click event (id, campaign, country, device, timestamp)
     v
   [ INGEST ]  does almost nothing: write to the queue, return 202
     |
     v
   [ KAFKA ]  partitioned BY CAMPAIGN
     |          -> all of one campaign's events on one partition
     |          -> aggregation is local, no cross-instance coordination
     v
   [ AGGREGATOR ]  dedupe -> bucket by EVENT TIME -> accumulate
     |
     +--------------------------+
     v                          v
   [ PRE-SUMMED COUNTS ]     [ RAW EVENT LOG ]
   fast, approximate          slow, exact
   serves the last hours      serves everything older
     |                          |
     |                          v
     |                    [ NIGHTLY BATCH ] -> overwrite closed periods
     v
   [ DASHBOARD ]  a lookup, never a scan

   "The board is for answering. The register is for being right."
```

Event time against processing time:

```
   a phone goes into a tunnel at 14:58, clicks at 14:59, surfaces at 15:20

   BUCKET BY PROCESSING TIME (when we saw it)         EASY AND WRONG
     the click lands in the 15:20 bucket
     -> the 14:59 report is missing a click, forever
     -> and RERUNNING the pipeline gives DIFFERENT numbers,
        because processing time depends on when you ran it

   BUCKET BY EVENT TIME (when it happened)            CORRECT AND HARD
     the click belongs to 14:59
     -> but 14:59 was reported 20 minutes ago
     -> so a window is NEVER truly closed

   THE RESOLUTION: a WATERMARK
     a moving estimate of "we have probably seen everything up to T"
     close windows when the watermark passes them, plus a grace period
     anything later -> a separate LATE-DATA path, corrected explicitly

   THERE IS NO CORRECT ANSWER, ONLY A STATED ONE:
     wait longer  -> more complete, less timely
     wait less    -> more timely, less complete
```

Duplicates, which are guaranteed:

```
   the client does not get an ack and RESENDS
   Kafka delivers at-least-once
   the aggregator crashes after counting and before committing its offset

   -> THE SAME CLICK IS COUNTED TWICE
   -> and each duplicate is money an advertiser is charged

   THE FIX: a CLIENT-GENERATED event id, deduplicated in a window

     seen = a set of recent ids
     if event.id in seen: drop
     else: count it, and remember the id

   AND THE WINDOW IS THE COMPROMISE:
     1,000,000 events/second x 3,600 s = 3.6 BILLION ids per hour
     as 16-byte ids: 58 GB          -> too much to keep exactly
     as a Bloom filter at 1%:  ~4 GB -> and 1% of real clicks DROPPED

   -> so: exact dedup over a SHORT window (a few minutes),
      plus batch dedup over the raw log for the authoritative number
```

Dimensional explosion, which is where storage goes:

```
   dimensions and their cardinalities

     campaign      100,000
     country       200
     device        5
     ad slot       50
     minute        1,440/day

   FULL CROSS-PRODUCT:
     100,000 x 200 x 5 x 50 x 1,440 = 7.2 x 10^12 rows/day

   -> IMPOSSIBLE, and almost all of it is zero

   WHAT YOU ACTUALLY STORE:
     only combinations that OCCURRED (sparse)
     only combinations people QUERY (a handful of dimension sets)

     campaign x minute                   ~100M rows/day
     campaign x country x minute         ~500M rows/day
     campaign x device x minute          ~10M rows/day

   -> ~600M rows/day, not 7 x 10^12.
      The cross-product is a trap; sparsity and query-driven
      rollups are the answer.
```

The two paths, and why both exist:

```
   STREAMING                      BATCH

   latency: seconds               latency: hours
   deduped over minutes           deduped over everything
   windows closed on a watermark  every event, in event-time order
   late data partly dropped       late data included
   -> FAST and APPROXIMATE        -> SLOW and EXACT

   SERVE: the last few hours      SERVE: everything older
   the batch OVERWRITES the streaming numbers for closed periods

   Criticised as "lambda architecture" for duplicating the logic.
   FOR BILLING DATA IT IS STILL THE HONEST ANSWER, because
   "fast and roughly right" and "slow and exactly right" are
   genuinely different products and you need both.
```

---

## 5. How it actually works

### Ingestion: do almost nothing

```python
@app.post("/click")
def record_click(payload: dict) -> tuple[str, int]:
    """On the path of every ad interaction. Write and return."""
    event = {
        "id": payload["event_id"],            # CLIENT-generated
        "campaign": payload["campaign_id"],
        "country": geo_of(request.remote_addr),
        "device": payload.get("device", "unknown"),
        "event_time": payload["timestamp"],   # WHEN IT HAPPENED
        "received_at": time.time(),           # when we saw it
    }
    producer.send("clicks", key=str(event["campaign"]), value=event)
    return "", 202
```

**`202`, not `200`** — accepted for processing, not processed. **And no database write, no validation beyond
parsing, no enrichment that needs a lookup**, because this endpoint sits in front of every ad on the internet
and its latency is the product's.

**`key=campaign` is the partitioning decision**: all of a campaign's events go to one partition, **so one
aggregator instance owns that campaign and no cross-instance coordination is needed.**

**And both timestamps are carried.** `event_time` is what the aggregation uses; `received_at` is what tells you
how late the data was, **which is the metric you need to choose the watermark.**

### Deduplication

```python
DEDUP_WINDOW = 300

def is_duplicate(event_id: str) -> bool:
    """Exact, over a short window. Long windows need a sketch."""
    return not redis.set(f"seen:{event_id}", "1", nx=True, ex=DEDUP_WINDOW)
```

**`SET NX` is atomic**, so two aggregator instances racing on the same id cannot both proceed — **a
check-then-write would let both through.**

**Five minutes is the compromise.** It covers retries and short outages; **it does not cover a phone that
surfaces after twenty minutes**, and that gap is closed by the batch layer rather than by a bigger window.

**Because the arithmetic is unforgiving:** an hour of ids at a million a second is 3.6 billion, **and even a
Bloom filter at one percent drops one percent of real clicks** — which is revenue.

### Windowed aggregation

```python
from collections import defaultdict

WINDOW_SECONDS = 60
GRACE_SECONDS = 120

class Aggregator:
    def __init__(self) -> None:
        self.windows: dict[int, dict[tuple, int]] = defaultdict(
            lambda: defaultdict(int))
        self.watermark = 0.0

    def consume(self, event: dict) -> None:
        if is_duplicate(event["id"]):
            return

        bucket = int(event["event_time"]) // WINDOW_SECONDS   # BY EVENT TIME
        self.watermark = max(self.watermark,
                             event["event_time"] - GRACE_SECONDS)

        if bucket * WINDOW_SECONDS < self.watermark - GRACE_SECONDS:
            late_events.send(event)                           # NOT dropped
            return

        for key in rollup_keys(event):
            self.windows[bucket][key] += 1

    def flush_closed(self) -> None:
        """Emit windows the watermark has passed."""
        for bucket in sorted(self.windows):
            if bucket * WINDOW_SECONDS + WINDOW_SECONDS < self.watermark:
                store.write(bucket, self.windows.pop(bucket))
```

**`event["event_time"] // WINDOW_SECONDS` is the whole correctness decision** — bucketing by when it happened,
not by when it arrived. **The alternative is one character shorter and produces reports that change when you
rerun them.**

**The watermark is derived from the events themselves** — the maximum event time seen, minus a grace period —
**so it advances with the data rather than with the clock**, which is what makes it work when a partition is
delayed.

**And `late_events.send(event)` rather than a silent drop** is the honest handling: **late data goes somewhere
it can be counted later**, and its volume is a metric worth alerting on.

### The rollups people actually query

```python
def rollup_keys(event: dict) -> list[tuple]:
    """Only the combinations people query — NOT the full cross-product."""
    c, country, device = event["campaign"], event["country"], event["device"]
    return [
        ("campaign", c),
        ("campaign_country", c, country),
        ("campaign_device", c, device),
        ("country", country),
    ]
```

**Four rollups rather than the cross-product**, which would be seven trillion rows a day. **The list is driven
by the dashboard's filters**, and adding a new one means backfilling from the raw log — **which is a real cost
and the reason to think about this in advance.**

### Storage

```python
def write_window(bucket: int, counts: dict[tuple, int]) -> None:
    """Pre-summed, keyed by dimension and minute. A query is a lookup."""
    rows = [{"bucket": bucket, "dimension": key[0], "values": key[1:],
             "count": count}
            for key, count in counts.items()]
    store.bulk_upsert(rows)                   # upsert: the batch layer overwrites


def query(dimension: str, values: tuple, start: float, end: float) -> int:
    """Sum the minute buckets in the range. A few hundred rows, not billions."""
    lo, hi = int(start) // WINDOW_SECONDS, int(end) // WINDOW_SECONDS
    return store.sum_counts(dimension, values, lo, hi)
```

**`bulk_upsert` rather than insert** is what lets the batch layer overwrite the streaming numbers for a closed
period **without a delete-then-insert race.**

**And an hour's query is sixty minute-rows**, a day's is 1,440 — **which is why minute granularity is the right
unit: fine enough for any window, coarse enough that the sums stay small.**

### The batch reconciliation

```python
def reconcile(day: str) -> dict:
    """Sarojini's Sunday. The register is what happened."""
    exact = spark.sql(f"""
        SELECT dimension, values, bucket, COUNT(DISTINCT event_id) AS count
          FROM raw_events
         WHERE event_date = '{day}'
         GROUP BY dimension, values, bucket
    """)
    streaming = store.read_day(day)

    report = {"matched": 0, "differ": []}
    for row in exact:
        streamed = streaming.get((row.dimension, row.values, row.bucket), 0)
        if streamed == row.count:
            report["matched"] += 1
        else:
            report["differ"].append((row, streamed))
    store.overwrite_day(day, exact)           # the batch number wins
    return report
```

**`COUNT(DISTINCT event_id)` is the batch deduplication**, and it is over the whole day rather than a
five-minute window — **which is exactly the gap the streaming layer could not close.**

**And the streaming numbers are overwritten rather than corrected**, because the batch layer's answer is
authoritative. **The comparison is kept as a report**, because a growing discrepancy is the earliest signal
that something in the fast path is broken.

### Fraud filtering, which is not optional

```python
def looks_fraudulent(event: dict) -> str | None:
    if click_rate(event["ip"], window=60) > 20:
        return "ip_rate"
    if event["event_time"] - impression_time(event["impression_id"]) < 0.1:
        return "too_fast"                     # clicked before it rendered
    if not impression_exists(event["impression_id"]):
        return "no_impression"                # a click with no ad shown
    return None
```

**A click that arrives less than a hundred milliseconds after the impression is not a human**, and **a click
with no matching impression is not a click at all** — those two rules catch a large fraction of simple
automation.

**And the flagged events are stored separately rather than discarded**, because **advertisers dispute charges
and you must be able to show what was excluded and why.**

### Approximate counting, where exactness is not needed

```python
def unique_users(campaign: int, bucket: int) -> int:
    """HyperLogLog: ~1.6% error in 12 KB, against gigabytes for a set."""
    return redis.pfcount(f"hll:{campaign}:{bucket}")


def record_unique(campaign: int, bucket: int, user_id: str) -> None:
    redis.pfadd(f"hll:{campaign}:{bucket}", user_id)
```

**Unique users is a cardinality question, not a count** — and an exact set of a hundred million user ids is
gigabytes per campaign per hour.

**HyperLogLog gives about 1.6% error in twelve kilobytes**, which is **completely acceptable for reach and
completely unacceptable for billing.** **Approximate the reporting metrics; count the billable ones exactly.**

### The real systems

```
Kafka                the durable buffer; partition by campaign
Flink / Spark        stream processing with event-time windows and
  Streaming          watermarks — both have first-class support
                     for exactly this problem
Druid / ClickHouse   the pre-aggregated store; both designed for
                     time-series rollups with dimensional filters
Redis                short-window deduplication, HyperLogLog
S3 + Spark           the raw event log and the nightly batch
Kappa architecture   the alternative to lambda: one code path,
                     replay the log to recompute
```

**Naming Flink's watermarks specifically is worth doing**, because **event-time windowing with watermarks is
the thing the framework exists to provide** — and knowing that it is a solved problem with a name is better
than describing it as if it were novel.

---

## 6. The numbers

**Volume.**

```
1,000,000 events/second (impressions and clicks)
= 86,400,000,000 events/day

each event ~100 bytes
= 8.6 TB/day of raw events
= 3.1 PB/year

compressed (~5:1, they are highly repetitive):  ~1.7 TB/day
```

**Eight terabytes a day of hundred-byte records** is the shape: **enormous count, trivial size each.**

**Ingestion.**

```
1,000,000 requests/second at peak
each doing: parse + one Kafka produce

per instance: ~20,000 requests/second (network-bound)
-> 50 instances at peak

Kafka: ~1,000,000 messages/second across the cluster
       at ~100 bytes = 100 MB/s
       -> ~20 brokers, comfortably
```

**Fifty machines for a million requests a second** — **and the endpoint is small precisely so that this number
stays small.**

**Aggregation.**

```
1,000,000 events/second, 4 rollups each = 4,000,000 counter updates/second

in-memory, per instance: ~500,000 updates/second
-> ~8 aggregator instances

and because Kafka is partitioned BY CAMPAIGN, each instance owns a
disjoint set of campaigns
-> no cross-instance coordination at all
```

**Partitioning by campaign is what removes the coordination**, and it is worth stating as the reason rather
than as a detail.

**Storage: the raw log against the aggregates.**

```
RAW EVENTS
  8.6 TB/day compressed to ~1.7 TB
  x 90 days retention = ~155 TB
  on object storage at $0.023/GB = ~$3,600/month

AGGREGATES
  ~600,000,000 rows/day (sparse, query-driven rollups)
  each ~50 bytes = 30 GB/day
  x 400 days = 12 TB
  -> 13x SMALLER than 90 days of raw events, and it answers
     every query
```

**And the cross-product, for contrast:**

```
   campaign x country x device x slot x minute
   = 100,000 x 200 x 5 x 50 x 1,440 = 7.2 x 10^12 rows/day

   at 50 bytes: 360 TB/day

   -> against 30 GB/day for the sparse, query-driven rollups
   -> 12,000x, and almost every one of those rows would be ZERO
```

**Twelve thousand times, entirely from storing what occurred rather than what could occur** — which is the
single most important sizing insight in this design.

**Deduplication memory.**

```
1,000,000 ids/second

5-minute exact window:   300,000,000 ids
                         x ~50 B in Redis = 15 GB       feasible
1-hour exact window:     3,600,000,000 ids
                         x ~50 B = 180 GB               not feasible
1-hour Bloom filter, 1%: ~4 GB
                         -> and 1% of REAL clicks dropped
                         -> 1% of revenue. NOT acceptable.

-> exact dedup over minutes in the stream
-> COUNT(DISTINCT) over the whole day in the batch layer
```

**The Bloom filter arithmetic is the argument**: **a structure that is fine for a crawler is unacceptable here,
because the false positives are money.**

**Query cost.**

```
"campaign 4471, last hour, by country"
  60 minute-buckets x ~50 countries = ~3,000 pre-summed rows
  -> ~10 ms

the same question over RAW events:
  1 hour x 1,000,000/second = 3,600,000,000 events to scan
  -> minutes, on a cluster

-> ~5 orders of magnitude, which is why the aggregation exists
```

**Late data, measured.**

```
typical distribution of (received_at - event_time):

  < 1 second      ~95%
  1-10 seconds    ~4%
  10-60 seconds   ~0.9%
  > 60 seconds    ~0.1%     <- 1,000,000 events/day

with a 2-minute grace period: ~99.98% included in the window
-> ~0.02% goes to the late path = ~17,000,000 events/day

-> which is why the late path must EXIST and be counted,
   not silently dropped
```

**Seventeen million late events a day is not an edge case**, and it is the number that justifies the batch
layer.

**Cost, roughly:**

```
ingestion fleet (50-80 machines)      ~$80,000/month
Kafka cluster (20 brokers)            ~$40,000/month
aggregation (10 machines)             ~$15,000/month
aggregate store (Druid/ClickHouse)    ~$50,000/month
raw log on object storage             ~$4,000/month
nightly batch (Spark)                 ~$30,000/month
                                      ----------------
                                      ~$220,000/month

-> for a system whose entire output is sums.
   And it is justified because those sums ARE the billing.
```

---

## 7. The trade-offs

**Event time against processing time.** Processing time is trivial to implement and **makes reports
non-reproducible** — rerun the pipeline and the numbers change, because they depend on when you ran it. Event
time is correct and **means no window is ever truly closed.** **For billing there is no choice**: the number
must be the same tomorrow as today.

**Watermark grace period.** Longer means more complete numbers and more delay before a window can be reported.
Shorter means timely numbers and more late data. **There is no correct value — only a stated one**, and the
right way to choose it is to measure the actual distribution of lateness and pick a percentile.

**Exact deduplication against a sketch.** Exact over five minutes costs fifteen gigabytes and misses the
twenty-minute stragglers. **A Bloom filter over an hour is four gigabytes and drops one percent of real
clicks** — which is one percent of revenue, **so it is unacceptable here even though the same structure was
fine for a web crawler.** The resolution is a short exact window plus batch deduplication.

**Which rollups to precompute.** The full cross-product is seven trillion rows a day and almost entirely zero.
**Query-driven rollups are thirty gigabytes** — twelve thousand times smaller. **The cost is that a new query
dimension requires a backfill from the raw log**, which takes hours, **so the set of dimensions is a decision
with real inertia** and worth getting roughly right in advance.

**Lambda against kappa.** Lambda — a fast approximate path and a slow exact one — **duplicates the aggregation
logic in two places, which is the standard criticism and is fair.** Kappa keeps one code path and recomputes by
replaying the log, **which is elegant and means the fast path's approximations are the only numbers you have
until a replay completes.** **For billing, lambda is still the honest answer**, because a fast rough number and
a slow exact one are genuinely different products.

**Approximate metrics against exact ones.** HyperLogLog gives unique-user counts within about 1.6% in twelve
kilobytes rather than gigabytes. **That is right for reach and reporting and wrong for anything billable.**
**Approximate what is reported; count exactly what is charged** — and say which is which on the dashboard.

**And the honest one: aggregation is lossy by construction.** Once you have stored "4,412 clicks for campaign X
in minute Y", **you cannot answer a question you did not anticipate** without going back to the raw log. **That
is why the raw log is kept**, and it is why deleting it to save four thousand dollars a month would be a false
economy.

**When would I not build this?** **Below a few thousand events a second, a database with an index on
`(campaign, timestamp)` and a `GROUP BY` is the whole system**, and every component here is overhead. **Managed
analytics — BigQuery, Snowflake, Redshift — will ingest and aggregate at billions of rows a day** and cost less
than the team. **Building this is justified by the latency requirement on the fast path** — advertisers want
near-real-time spend — **and by the volume**, not by the aggregation, which is the easy part.

---

## 8. In the interview

### How it gets asked

- *"Design an ad click aggregator."* — usually with a scale like a million events a second.
- *"How do you handle events that arrive late?"* — the event-time question, and the core of it.
- *"An event is delivered twice. What happens?"* — deduplication, and the money.
- *"How do you answer 'clicks in the last hour by country' quickly?"*
- *"How do you know your numbers are right?"* — reconciliation.
- *"What if I want a breakdown you did not precompute?"*

### The first ninety seconds

> "The shape of this is unlike anything else, so let me start there. **A million events a second at a hundred
> bytes each, and a few thousand queries a second.** The raw events are individually worthless — **the product
> is the sums.**
>
> **Which means the central move is: aggregate on the way in, not on the way out.** Nobody scans a trillion
> rows to answer 'clicks last hour'. **The counts are computed as the events arrive and stored pre-summed, and
> a query is a lookup.**
>
> **The pipeline is five stages.** A tiny ingest endpoint that writes to a queue and returns. **Kafka,
> partitioned by campaign** — so one instance owns each campaign and there is no cross-instance coordination.
> A stream aggregator. A pre-summed store. And a dashboard that does lookups.
>
> **The ingest endpoint must do almost nothing** — no database write, no enrichment — **because it sits in
> front of every ad interaction and its latency is the product's.**
>
> **Now the two things that are actually hard, and both are about counting rather than scale.**
>
> **First, event time against processing time.** A phone goes into a tunnel and reports its clicks twenty
> minutes later. **Bucketing by when we saw it is easy and wrong** — the numbers change if you rerun the
> pipeline. **Bucketing by when it happened is correct and means a window is never truly closed.**
>
> **The resolution is a watermark**: a moving estimate of 'we have probably seen everything up to T', closing
> windows with a grace period, **and sending anything later to an explicit late-data path rather than silently
> dropping it.** And I would be honest that **there is no correct grace period, only a stated one** —
> longer is more complete and less timely.
>
> **Second, duplicates, which are guaranteed rather than possible.** Kafka is at-least-once, clients retry,
> and **every duplicate is money an advertiser is charged.** So: a client-generated event id and deduplication
> in a window.
>
> **And the window is the compromise, because the arithmetic is unforgiving.** An hour of ids at a million a
> second is 3.6 billion — **and a Bloom filter at one percent would drop one percent of real clicks, which is
> one percent of revenue.** **So: exact dedup over a few minutes in the stream, and `COUNT(DISTINCT)` over the
> whole day in a batch layer.**
>
> **Which brings me to the last piece: two paths.** The stream is fast and approximate; **a nightly batch over
> the raw log is slow and exact and overwrites the closed periods.** For billing data that duplication is the
> honest answer."

### The follow-ups

**"How do you handle events that arrive late?"**

> "This is the question that decides whether the reports are correct or merely available, **so let me be
> precise about what 'late' means first.**
>
> **Every event has two timestamps: when it happened, and when we saw it.** They differ by milliseconds
> normally, **and by twenty minutes for a phone that went into a tunnel and surfaced.**
>
> **Bucketing by processing time — when we saw it — is one character easier and it is wrong.** The click gets
> counted in the fifteen-twenty bucket instead of fourteen-fifty-nine, **and worse, rerunning the pipeline
> gives different numbers**, because processing time depends on when you happened to run it. **For billing,
> non-reproducible numbers are not acceptable.**
>
> **So: bucket by event time.** And the consequence is that **a window is never truly closed** — a late event
> can always arrive for an hour you already reported.
>
> **The standard resolution is a watermark**, and it is what stream processors like Flink exist to provide. **A
> watermark is a moving estimate of 'we have probably seen everything up to time T'** — typically the maximum
> event time seen so far, minus a grace period. **It advances with the data rather than with the clock**, which
> matters when a partition is delayed.
>
> **Windows are closed when the watermark passes them.** And **anything arriving after that goes to an explicit
> late-data path** — not dropped silently, and not silently folded into a report somebody has already seen.
>
> **The grace period is a genuine trade with no correct answer**: wait longer and the numbers are more complete
> and less timely; wait less and the reverse. **The right way to pick it is to measure the actual distribution
> of lateness.** In practice about ninety-five percent of events arrive within a second and **about a tenth of
> a percent take more than a minute** — which at a million a second is **a million events a day**, so this is
> not an edge case.
>
> **And the batch layer is what makes the trade survivable.** The nightly recomputation over the raw log sees
> every event regardless of when it arrived, **so the authoritative number is eventually right even though the
> streaming number was not.** The stream serves the last few hours; the batch overwrites everything older."

**"An event is delivered twice. What happens?"**

> "It gets counted twice, **and an advertiser is charged twice** — so this is a correctness problem with money
> attached rather than a hygiene issue.
>
> **And duplicates are guaranteed, not possible.** Three separate sources: **a client that does not receive an
> acknowledgement and resends; Kafka's at-least-once delivery; and an aggregator that crashes after counting an
> event and before committing its offset**, so it reprocesses from the last commit.
>
> **The answer is a client-generated event id.** The ad SDK assigns an id when the click happens — **not the
> server on receipt**, because a retried request would get a different server-generated id and deduplicate
> nothing. **That is the same rule as payment idempotency keys.**
>
> **Then the aggregator keeps recently-seen ids and drops repeats**, using an atomic set-if-absent — **a
> check-then-write would let two racing instances both through.**
>
> **The hard part is the window, and the arithmetic is unforgiving.** At a million events a second, **an hour
> of ids is 3.6 billion.** As sixteen-byte ids with overhead that is **around 180 gigabytes** — not feasible.
>
> **And the obvious answer is a Bloom filter, which is wrong here for an interesting reason.** Four gigabytes at
> one percent false positive — **and a false positive means dropping a real click. One percent of revenue.**
> The same structure was completely fine for a web crawler, where a false positive meant skipping a page
> nobody would miss. **Here the false positives are money, so it is unacceptable.**
>
> **So the resolution is two-layered.** **Exact deduplication over a short window in the stream** — five
> minutes, about fifteen gigabytes, which covers retries and short outages. **And `COUNT(DISTINCT event_id)`
> over the whole day in the batch layer**, which catches the twenty-minute stragglers the short window could
> not.
>
> **The streaming number may be slightly high; the batch number is right and overwrites it.** **And I would
> track the difference as a metric**, because a growing gap is the earliest signal that something in the fast
> path has broken."

**"What if I want a breakdown you did not precompute?"**

> "Then it is slow, **and I would rather say that plainly than pretend the design covers everything** — because
> the reason it is fast is precisely that it does not.
>
> **The aggregates are precomputed for specific dimension combinations** — campaign by minute, campaign by
> country by minute, and so on. **A query in that set is a lookup over a few hundred pre-summed rows: about ten
> milliseconds.**
>
> **A combination I did not precompute has to come from the raw log**, which for an hour is 3.6 billion events
> — **minutes on a cluster, not milliseconds.**
>
> **And the reason I do not precompute everything is the cross-product.** Campaign times country times device
> times ad slot times minute is **about seven trillion rows a day**, and almost every one of them is zero.
> **Against thirty gigabytes a day for the sparse, query-driven rollups — twelve thousand times smaller.**
>
> **So the design decision is: store what occurred, in the combinations people query.** Not the full space.
>
> **Which means the set of dimensions has real inertia**, and adding one requires backfilling from the raw log
> — **hours of batch work.** **So I would want the likely query patterns established early**, and I would treat
> "which breakdowns do advertisers actually look at" as a product question to be answered before building
> rather than after.
>
> **Two things that soften it.** **A slow ad-hoc path is fine as a feature**, as long as it is honest — a query
> that says 'this will take a few minutes' is better than one that quietly times out. **And keeping the raw log
> is what makes any of this possible**, which is why deleting it to save a few thousand dollars a month would
> be a false economy — **the aggregates are lossy by construction, and the log is the only thing that can
> answer a question you did not anticipate.**
>
> **That is Sarojini's point: the board is for answering, and the register is for being right.**"

### The model answer

*"Design a system that counts ad impressions and clicks: a million events a second, and advertisers see their
spend updated within a minute."*

> "Two constraints in that sentence drive everything: **a million events a second**, and **within a minute** —
> so this needs a fast path, and the money means it also needs a correct one.
>
> **The shape first.** A million hundred-byte events a second is **8.6 terabytes a day**, against a few
> thousand queries. **The raw events are individually worthless; the product is the sums.** So the central move
> is **aggregate on the way in, not on the way out** — nobody scans a trillion rows.
>
> **Ingestion does almost nothing**: parse, write to Kafka, return `202`. **No database write, no enrichment**,
> because it sits in front of every ad interaction on the internet. **Fifty machines at a million requests a
> second**, and it is small so that number stays small.
>
> **Kafka partitioned by campaign**, so all of a campaign's events land on one partition and one aggregator
> owns it — **no cross-instance coordination at all.** About twenty brokers for a hundred megabytes a second.
>
> **Aggregation into one-minute tumbling windows, bucketed by EVENT time.** Minute granularity because hourly,
> daily and monthly are all sums over minute buckets — **fine enough for any window a dashboard asks for.**
>
> **And bucketing by event time rather than arrival time is the correctness decision.** Arrival time is easier
> and **makes the numbers change when you rerun the pipeline**, which for billing is not acceptable.
>
> **Windows close on a watermark with a grace period of a couple of minutes**, which covers about 99.98% of
> events. **The remaining tenth of a percent — a million events a day — goes to an explicit late path**, not a
> silent drop.
>
> **Deduplication with a client-generated event id**, exact over a five-minute window in Redis. **And I would
> explicitly reject a Bloom filter here**: four gigabytes for an hour at one percent false positive sounds
> attractive, **but a false positive drops a real click, which is one percent of revenue.** The same structure
> was fine for a crawler; here the errors are money.
>
> **Storage: query-driven rollups, not the cross-product.** The full space is seven trillion rows a day and
> almost all zero; **the four or five combinations people actually filter on are about six hundred million rows
> a day, thirty gigabytes.** **Twelve thousand times smaller**, entirely from storing what occurred.
>
> **And the two paths, which is the part I would insist on.** **The stream is fast and approximate** —
> deduplicated over minutes, windows closed on a watermark, some late data missed. **A nightly batch over the
> raw log is slow and exact**, deduplicating with `COUNT(DISTINCT)` over the whole day, **and it overwrites the
> streaming numbers for closed periods.**
>
> **Advertisers see the streaming number within a minute, which satisfies the requirement. The invoice uses the
> batch number.** **And the difference between them is a metric I would alert on**, because a growing gap is
> the first sign the fast path is broken.
>
> **Two things I would raise unprompted.**
>
> **Fraud filtering is not optional.** A click arriving less than a hundred milliseconds after its impression
> is not a human; a click with no matching impression is not a click. **And flagged events must be stored
> separately rather than discarded**, because advertisers dispute charges and you have to show what was
> excluded and why.
>
> **And approximate where it is not billable.** Unique reach via HyperLogLog is 1.6% error in twelve kilobytes
> against gigabytes for an exact set — **completely fine for a reach report and completely wrong for a charge.**
> **Approximate what is reported; count exactly what is billed** — and label which is which on the dashboard,
> because an advertiser who discovers the distinction themselves will not be pleased."

---

## 9. Recall card

**The shape is unlike the rest: a million tiny events a second in, a few thousand queries out, and the raw
events are individually worthless.** So the central move is **aggregate on the way IN, not on the way out** —
a query becomes a lookup over pre-summed rows, never a scan.

**Five stages: a tiny ingest endpoint (write to Kafka, return `202`, no DB write), Kafka PARTITIONED BY
CAMPAIGN (so one instance owns each campaign — no cross-instance coordination), stream aggregation into
one-minute windows, a pre-summed store, and a dashboard that does lookups.**

**Event time versus processing time is the correctness decision.** Processing time is easier and **makes
reports change when you rerun them.** Event time is correct and means **no window is ever truly closed** —
resolved by a **watermark** (max event time seen minus a grace period, advancing with the data, not the clock)
plus an **explicit late-data path**. **~0.1% arrive over a minute late — a million events a day, not an edge
case.** There is no correct grace period, only a stated one.

**Duplicates are GUARANTEED** (client retries, Kafka at-least-once, aggregator restarts) **and each one is
money.** **Client-generated event id**, atomic set-if-absent, exact over ~5 minutes (~15 GB). **Explicitly
reject a Bloom filter**: 4 GB for an hour at 1% sounds good, **but a false positive drops a real click — 1% of
revenue.** The same structure was fine for a crawler because there the errors were free.

**Never store the cross-product**: campaign × country × device × slot × minute is **7×10¹² rows/day, almost all
zero**, against **~30 GB/day** for sparse query-driven rollups — **12,000×**. The cost is that a new dimension
needs a backfill, so the dimension set has real inertia.

**Two paths, deliberately.** Stream = fast and approximate; **nightly batch over the raw log = slow and exact
(`COUNT(DISTINCT)` over the whole day) and it OVERWRITES closed periods.** Advertisers see the streaming number
in a minute; **the invoice uses the batch number, and the gap between them is the alert.** **Approximate what
is reported (HyperLogLog, 1.6% in 12 KB), count exactly what is billed.**
