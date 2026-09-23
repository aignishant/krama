---
day: 137
track: system-design
title: "Time-series and metrics stores"
phase: "Building blocks of big systems"
status: written
---

# Time-series and metrics stores

## 1. What this is, and why they ask it

Every system you build produces measurements. Requests per second, latency, queue depth, CPU, error counts,
temperature from a sensor, price of a stock. They arrive constantly, they are never updated once written, and
they are read in ranges — "the last six hours" — rather than one at a time.

That access pattern is unlike anything a relational database is built for, and at volume the difference is not
a tuning problem. A million measurements a second into a Postgres table is not slow, it is impossible: the
index maintenance alone exceeds what the machine can do.

A **time-series database** exploits the shape. Points arrive in timestamp order, consecutive values are
similar, nothing is ever updated, and old data is wanted at lower resolution. Each of those facts buys an
enormous saving, and together they turn 16 bytes per point into about 1.5.

They ask this because "where would you store the metrics for this system?" is a question every design touches,
and because the failure mode has a name — **cardinality explosion** — that separates people who have run a
monitoring system from people who have configured one. **The number of distinct series, not the number of
points, is what kills these systems**, and knowing that is most of the answer.

By the end of this lesson you can say what makes time-series data special, size a metrics store from a fleet
size, explain compression and downsampling with numbers, name the cardinality trap and how to avoid it, and
choose between Prometheus, a wide-column store and a columnar analytical database.

---

## 2. The story

Kulkarni has read the society's water meter at six every morning since 2011.

It is in a pit behind the pump room with a steel cover, and the routine is the same: lift the cover, wipe the
glass, read the number, put it in his phone.

The numbers themselves are enormous and almost identical. `1,847,203`. The next morning, `1,847,391`. The
morning after, `1,847,566`.

He worked out early that what he actually cares about is never the number. It is the gap. One eighty-eight,
then one seventy-five, then a Sunday when it is two forty because everybody is home and washing.

Once, in 2017, the gap was eleven hundred and he was down there before nine looking for the leak. Found it too,
in the line to the back garden tap, and the committee reckoned it had been running for three days.

Two other things he has settled over the years, without anybody telling him to.

He does not keep every day forever. This month's daily readings, yes, all of them. Last month's, he keeps as a
monthly figure and a rough daily average. For 2014, all he has is a number for the year and a note that it was
high because of the tanker business in May. The old detail went, and he has never once wanted it back — when
somebody at a meeting asks about water, the question is always "are we using more than last year" and never
"what was the reading on the fourteenth of March 2014".

And the second thing, which is the one his son found funny when he saw the phone. Kulkarni does not write down
the whole number any more. He writes the gap. `188`. `175`. `240`. Three characters instead of seven, and he
can always add them up if he needs the total, which he does about once a year for the committee.

His son, who works with computers, looked at it for a moment and said something about how that was clever, and
Kulkarni said it was not clever, it was that his thumbs are sixty-three years old and seven digits every
morning for fourteen years is a lot of digits.

---

## 3. The idea in plain English

Kulkarni's meter book is a time-series database, and the three habits he arrived at are the three ideas.

**A time series is a named sequence of timestamped values.** The name is not just a string — it is a
**metric name plus a set of labels**:

```
http_requests_total{service="checkout", method="POST", status="500", host="web-14"}
```

**Every distinct combination of label values is a separate series.** That sentence is where all the trouble
comes from, and section 7 is mostly about it.

**Four properties make this data unlike anything else**, and each one buys a specific optimisation:

**It arrives roughly in time order and is never updated.** No `UPDATE`, no `DELETE` of individual rows. That
means the storage can be append-only, sorted, and immutable — no random writes, no page splits, no index
rebalancing.

**Consecutive values are similar.** CPU was 41.2% and is now 41.4%. Kulkarni writing `188` instead of
`1,847,391`. Storing the *difference* instead of the value makes the number tiny, and tiny numbers compress
brutally well.

**Timestamps are regular.** Scrapes every 15 seconds means the gap between timestamps is 15,000 milliseconds,
every time. So you store the difference of the differences — the **delta of delta** — which is almost always
**zero**, and zero costs one bit.

**Queries are ranges and aggregates, never point lookups.** "Average latency per minute over the last six
hours", not "the value at 14:32:07.412". So the storage is arranged in **chunks by time**, and a query reads a
few contiguous blocks instead of seeking.

**Now the arithmetic that follows.** A naive row is a timestamp (8 bytes) plus a value (8 bytes) plus a series
identifier — call it 16 bytes minimum, and in a relational table with an index far more. With delta-of-delta
timestamps and XOR-compressed floats, the real-world figure is **1 to 2 bytes per point**. That is roughly a
**tenfold saving**, and it is the difference between a metrics system that fits on one machine and one that
does not.

**Downsampling is Kulkarni's second habit.** Keep every point for a short window, then keep only summaries.

```
raw, 15-second resolution     kept for 15 days
1-minute averages             kept for 90 days
1-hour averages               kept for 2 years
```

**And you keep more than the average.** Storing only the mean loses the spikes, which is usually the thing you
actually needed. Minimum, maximum, count and sum let you reconstruct averages over any longer window and still
see the worst moment.

**Retention is deletion by time, and it is cheap here.** Because data is stored in immutable chunks by time
range, expiring old data is deleting whole files. No `DELETE FROM ... WHERE timestamp < ...` scanning a table,
no vacuum, no index bloat. **That is a real architectural advantage and it is worth naming.**

**Counters versus gauges is the other thing to get right.** A **gauge** goes up and down — temperature, queue
depth, memory in use. A **counter** only increases — total requests served, total bytes sent — and what you
want from it is the **rate**, not the value. Kulkarni's meter is a counter, and the useful thing is the daily
gap, not the reading.

**Counters reset when the process restarts**, so a rate calculation has to notice a value that went *down* and
treat it as a reset rather than as a huge negative rate. Every real system handles this; it is worth knowing
that it is a case that needs handling.

**And the trap that dominates operating these systems: cardinality.** Adding a label with many distinct values
multiplies the number of series. A `user_id` label on a metric with a million users is a million series, each
needing its own index entry and its own in-memory chunk. **Systems fall over from too many *series*, almost
never from too many *points***, and the rule is: **labels must have bounded, low cardinality.** Never a user
id, never a request id, never a full URL path with ids in it, never an unbounded error message.

---

## 4. The picture

What a series looks like, and why the compression works:

```
series:  cpu_usage{host="web-14"}

  timestamp        value      naive bytes    what is actually stored
  --------------   --------   -----------    -----------------------------
  10:00:00.000     41.2       16             full timestamp + full value
  10:00:15.000     41.4       16             delta-of-delta: 0   value XOR: tiny
  10:00:30.000     41.3       16             delta-of-delta: 0   value XOR: tiny
  10:00:45.000     41.5       16             delta-of-delta: 0   value XOR: tiny
  10:01:00.000     44.9       16             delta-of-delta: 0   value XOR: small
                              -----------    -----------------------------
  5 points          80 bytes                 ~8 bytes
```

**What to notice.** The timestamps cost almost nothing after the first, because the gap is always 15,000 ms so
the delta-of-delta is always zero — one bit each. And the values are floats that differ only in their low bits,
so XOR-ing consecutive values leaves mostly zeros. **This is Facebook's Gorilla scheme and it is what every
modern time-series store uses.**

Storage layout, and why range queries are fast:

```
  BY TIME CHUNKS (what a TSDB does)

  [ 00:00 - 02:00 ]  [ 02:00 - 04:00 ]  [ 04:00 - 06:00 ]  ...
     all series          all series         all series
     immutable           immutable          being written

  query "cpu of web-14, last 4 hours"
      -> open 2 chunks, seek to this series, read contiguously
      -> a few disk reads

  RETENTION
      delete chunks older than 15 days  ->  unlink whole files
      no row-by-row DELETE, no vacuum, no index bloat
```

Downsampling, drawn as what survives:

```
  raw (15 s)      ||||||||||||||||||||||||||||||||||||   15 days
  1-minute        |  |  |  |  |  |  |  |  |  |  |  |     90 days
  1-hour          |           |           |              2 years

  storage for one series over 2 years:
    raw for 15 days      15 x 24 x 240   =   86,400 points
    1-min for 90 days    90 x 24 x 60    =  129,600 points
    1-hour for 2 years   730 x 24        =   17,520 points
                                            -------------
                                            233,520 points
    raw for 2 years would be              4,204,800 points
                                            -> 18x less
```

**What to notice.** Keeping full resolution forever costs eighteen times more for data nobody looks at. And the
1-minute rollup stores min, max, sum and count — not just the average — so a spike at 10:03:22 is still
visible as a maximum a year later.

And the cardinality trap, which is the picture to remember:

```
  http_requests_total{service, method, status}
      services  20
      methods   4
      statuses  8
                       20 x 4 x 8 = 640 series          fine

  ... add host
      hosts     200
                       640 x 200 = 128,000 series       large but workable

  ... add user_id
      users     1,000,000
                       128,000 x 1,000,000
                       = 128,000,000,000 series         the system is dead

  the POINT count did not change at all. Only the SERIES count did.
```

---

## 5. How it actually works

### The compression, concretely

Two techniques, both from Facebook's Gorilla paper, both now universal.

**Delta-of-delta timestamps.** Store the first timestamp fully. Then store the delta. Then, for each
subsequent point, store `delta − previous delta`. On a regular scrape interval that value is 0, encoded as a
single bit. A one-second jitter is a small number needing a handful of bits.

```
timestamps  10:00:00, 10:00:15, 10:00:30, 10:00:46, 10:01:01
deltas             15,        15,        16,        15
delta-of-deltas             0,         1,        -1
                            ^          ^          ^
                          1 bit    ~9 bits    ~9 bits
```

**XOR-compressed floats.** Consecutive float values usually share their sign, exponent and most of their
mantissa, so `current XOR previous` is mostly zeros. Store the number of leading zeros, the number of
meaningful bits, and those bits. A repeated value XORs to exactly zero — one bit.

```
41.2 XOR 41.4   ->  mostly zeros, ~14 meaningful bits
41.4 XOR 41.4   ->  all zeros, 1 bit
```

**Together: Facebook reported an average of 1.37 bytes per point** against 16 uncompressed, a twelvefold
reduction, and that is the number to quote.

### The systems, and what each is for

| System | Model | Best for | Weakness |
|---|---|---|---|
| **Prometheus** | pull, local storage | infrastructure monitoring, alerting | single node, ~weeks of retention |
| **VictoriaMetrics / Thanos / Mimir** | Prometheus-compatible, clustered | long retention, many clusters | more to operate |
| **InfluxDB** | push, purpose-built | IoT, application metrics | query language churn across versions |
| **TimescaleDB** | Postgres extension | time-series **plus** relational joins | inherits Postgres's write ceiling |
| **ClickHouse** | columnar OLAP | high-cardinality events, analytics | not a metrics system out of the box |
| **Amazon Timestream / GCP Monitoring** | managed | not wanting to run any of this | cost, lock-in |

**The most useful distinction is Prometheus's pull model.** Prometheus **scrapes** targets over HTTP on a
schedule rather than receiving pushes. That sounds like a detail and has real consequences:

- **Service discovery is built in** — it asks Kubernetes what exists and scrapes it, so a new pod is monitored
  automatically.
- **A target being down is itself a signal** — the `up` metric goes to 0, which is often the alert you
  actually want.
- **It does not work for short-lived jobs** that finish before a scrape, which is what the Pushgateway exists
  for and why that component always feels bolted on.

**TimescaleDB is the interesting middle option** and is worth knowing. It is a Postgres extension that
partitions a table by time into **hypertable chunks**, adds columnar compression on older chunks, and gives you
continuous aggregates for downsampling — while keeping full SQL and the ability to join metrics against
ordinary relational tables. **If you need "average latency per customer tier", where the tier lives in a
`customers` table, that join is trivial in TimescaleDB and awkward everywhere else.**

### Why a plain relational table fails

```sql
CREATE TABLE metrics (
    series_id BIGINT,
    ts        TIMESTAMPTZ,
    value     DOUBLE PRECISION
);
CREATE INDEX ON metrics (series_id, ts);
```

This is correct and it dies at volume, for four reasons and all of them matter:

- **Index maintenance per row.** Every insert updates a B-tree. At a million rows a second, that is the
  bottleneck long before the disk is.
- **Row overhead.** Postgres row headers are ~24 bytes, so a 16-byte measurement costs about 40 bytes stored,
  plus the index. **Roughly 30 times a compressed TSDB.**
- **Deleting old data is expensive.** `DELETE FROM metrics WHERE ts < now() - '30 days'` scans, writes dead
  tuples, and then autovacuum has to reclaim them — on a hot table, at volume, this alone can be
  unsustainable.
- **No downsampling.** You either keep everything or write and maintain rollup jobs yourself.

**Partitioning by time fixes the third problem completely** — dropping a partition is instant — and it is why
TimescaleDB's hypertables exist. It does not fix the first two.

### Query languages

PromQL is worth being able to read, because it appears in interviews:

```promql
# per-second rate of 5xx, averaged over 5 minutes, by service
sum by (service) (rate(http_requests_total{status=~"5.."}[5m]))

# 99th percentile latency from a histogram
histogram_quantile(0.99,
  sum by (le, service) (rate(http_request_duration_seconds_bucket[5m])))
```

**`rate()` is the function that matters**, and it is what turns a counter into something meaningful. It also
handles counter resets — a value going down is treated as a restart, not as a negative rate.

**Histograms deserve a note**, because percentiles are where naive metrics go wrong. You cannot average
percentiles: the mean of each host's p99 is not the fleet's p99. So latency is recorded as a **histogram** —
counts in buckets — and percentiles are computed from the summed buckets at query time. **Each bucket is a
separate series**, so a histogram with 12 buckets multiplies cardinality by 12, which is the main reason not to
put histograms on everything.

### The other axis: logs, metrics, traces

Metrics are numbers over time, aggregated, cheap, and lose per-request detail. **Logs** are individual events
with full detail and are far more expensive. **Traces** follow one request across services.

**Metrics tell you something is wrong; traces tell you where; logs tell you why.** That sentence is a good
thing to say, and the practical consequence is that you do not solve a metrics cardinality problem by putting
per-user labels on metrics — you solve it by putting the user id in a trace or a log, where high cardinality is
normal and expected.

---

## 6. The numbers

**Sizing from a fleet.** 500 machines, 1,000 metrics each, scraped every 15 seconds:

```
series            500 x 1,000              = 500,000
points per second 500,000 / 15             = 33,333 per second
points per day    33,333 x 86,400          = 2,880,000,000
```

```
uncompressed at 16 bytes                   = 46 GB per day
compressed at 1.5 bytes                    = 4.3 GB per day
                                             -> ~10x
```

```
15 days of raw at 4.3 GB/day               = 65 GB
```

**Sixty-five gigabytes for a fortnight of full-resolution metrics on a 500-machine fleet**, which fits on one
node comfortably. That is why Prometheus's single-node design works for so many people.

**With downsampling for long retention:**

```
raw 15 s,  15 days      500,000 series x 86,400 pts x 1.5 B   = 65 GB
1-min,     90 days      500,000 x 129,600 x 1.5 B             = 97 GB
1-hour,    2 years      500,000 x 17,520 x 1.5 B              = 13 GB
                                                                --------
                                                                175 GB
```

```
raw kept for 2 years instead:  500,000 x 4,204,800 x 1.5 B    = 3.15 TB
                                                                -> 18x more
```

**Ingestion rates:**

```
Prometheus, single node        ~ 500,000 - 1,000,000 samples/s
VictoriaMetrics, per node      ~ 1,000,000+ samples/s
InfluxDB, per node             ~ 500,000 samples/s
TimescaleDB                    ~ 100,000 - 1,000,000 rows/s (with batching)
plain Postgres, indexed        ~ 10,000 - 50,000 rows/s
```

**Plain Postgres is one to two orders of magnitude short**, and the gap is index maintenance rather than disk.

**Memory, which is the real Prometheus constraint:**

```
Prometheus holds ~2 hours of each active series in memory
per active series, roughly       ~3 KB of in-memory chunk + index
500,000 series                   ~1.5 GB
2,000,000 series                 ~6 GB
10,000,000 series                ~30 GB and the process is fragile
```

**The memory scales with the number of *series*, not with the number of points.** That is the sentence that
explains cardinality explosion in one line.

**Cardinality, worked out:**

```
base metric with 3 labels
    service 20 x method 4 x status 8          = 640 series
+ host (200)                                  = 128,000
+ a histogram with 12 buckets                 = 1,536,000
+ user_id (1,000,000)                         = 1.5 x 10^12   -> dead
```

**And the same story as an accident:** somebody adds a `path` label to an HTTP metric, and the paths include
ids — `/orders/8837412`. That is one series per order.

```
100,000 orders a day x 12 histogram buckets   = 1,200,000 new series per day
                                                accumulating
```

**A monitoring system killed by a one-line change, and the point count barely moved.**

**Query cost:**

```
"average CPU across 200 hosts, last 6 hours" at 15 s resolution
    200 series x 1,440 points                 = 288,000 points read
    -> tens of milliseconds

"p99 latency by endpoint, last 30 days" at raw resolution
    50 endpoints x 12 buckets x 172,800 pts   = 103,680,000 points
    -> seconds to minutes
    with 1-hour rollups: 50 x 12 x 720        = 432,000  -> instant
```

**Downsampling is not only about storage — it is what makes long-range queries possible at all.**

**Cost, roughly:**

```
self-hosted Prometheus + Grafana, 500 hosts   1-2 VMs, ~$200/month
managed metrics (Datadog-style)               often $15-25 per host per month
                                              500 hosts = $7,500-12,500/month
```

**That gap is why large fleets self-host**, and it is also why per-host pricing makes people delete metrics
they should keep.

---

## 7. The trade-offs

**You give up per-event detail.** A metric is an aggregate: "142 requests returned 500 in this minute". It
cannot tell you *which* requests, or what the user id was, or what the payload looked like. That is what logs
and traces are for, and the mistake is trying to recover the detail by adding labels — which is exactly the
cardinality explosion.

**You give up flexible querying.** A time-series store answers "this series, over this range, aggregated this
way" extremely well and "join these measurements against the customer table" not at all. TimescaleDB is the
exception and it pays for that with a lower write ceiling.

**Downsampling permanently destroys detail.** Once the raw fifteen-second data is gone, no query can recover
the shape of a spike inside a minute. **Storing min, max, sum and count rather than only the mean recovers
most of what matters**, and choosing rollup windows is choosing what future incidents you will be able to
investigate.

**Cardinality is a hard limit, not a soft one.** Systems degrade non-linearly: fine at a million series,
sluggish at five, dead at twenty. And because a label is added in application code, the failure arrives from a
deploy by someone who was not thinking about monitoring at all. **Enforce it with review and with a limit on
the ingest side**, because the alternative is discovering it during an incident when your monitoring is the
thing that is down.

**Push versus pull is a genuine trade.** Pull gives you service discovery, up/down as a first-class signal, and
no client-side buffering to get wrong. It cannot see short-lived jobs, and it needs network access from the
monitor to every target — awkward across NAT or firewalls. Push handles ephemeral work and firewalled
networks, and gives you no way to distinguish "healthy and silent" from "dead".

**And the operational one: your monitoring must not depend on the thing it monitors.** A metrics system running
inside the cluster it watches tells you nothing during the outage you most care about. The usual answer is a
small independent monitoring stack watching the main one, and an external check watching that.

**When would I not use a time-series database?** When the volume is small — a few thousand points a minute in
a Postgres table with a time-partitioned index is completely fine and is one fewer system. When the questions
are really analytical, over high-cardinality event data, where a columnar store like ClickHouse is a better
fit than a metrics system. And when the real requirement is per-request debugging, where the answer is tracing,
not metrics with more labels.

---

## 8. In the interview

### How it gets asked

- *"Where would you store the metrics for this system?"* — the direct version.
- *"Why not just put them in a Postgres table?"*
- *"Your monitoring system fell over. What happened?"* — almost always cardinality.
- *"How do you keep two years of metrics without spending a fortune?"*
- *"How would you compute the p99 latency across the fleet?"* — the histogram question.
- *"Design a monitoring system."* — where all of this appears as follow-ups.

### The first ninety seconds

> "A time-series database, and the reason is that the data has four properties a relational table does not
> exploit.
>
> **It is append-only and arrives in time order**, so storage can be immutable chunks sorted by time — no index
> rebalancing, no page splits, and expiring old data is deleting whole files rather than a `DELETE` that scans
> and then needs vacuuming.
>
> **Consecutive values are similar and timestamps are regular**, so you store delta-of-delta timestamps — which
> on a fixed scrape interval is zero, one bit — and XOR-compressed floats. That takes 16 bytes per point down
> to about 1.5. Facebook's Gorilla paper reports 1.37, and it is a tenfold saving.
>
> **Queries are ranges and aggregates**, never point lookups, so the layout is optimised for reading contiguous
> blocks.
>
> **And old data is wanted at lower resolution**, so you downsample: raw for a fortnight, one-minute rollups for
> three months, hourly for two years. That is about eighteen times less storage than keeping everything, and
> more importantly it is what makes a thirty-day query possible at all.
>
> Concretely, for 500 machines with a thousand metrics each scraped every 15 seconds: that is 500,000 series,
> 33,000 samples a second, and about 4.3 gigabytes a day compressed. Fifteen days of raw data is 65 gigabytes,
> which fits on one machine — which is why single-node Prometheus works for a lot of people.
>
> **The thing I would raise before you ask is cardinality**, because that is what actually kills these systems.
> Every distinct combination of label values is a separate series, and memory scales with the number of series,
> not the number of points. Adding a `user_id` label to a metric on a system with a million users creates a
> million series per existing combination, and the point count does not change at all. **Labels must have
> bounded, low cardinality — never a user id, a request id, or a URL path containing ids.**
>
> How large is the fleet, and do you need to join metrics against business data? Because that last one is the
> question that pushes me towards TimescaleDB rather than Prometheus."

### The follow-ups

**"Why not a Postgres table? Be specific."**

> "Four reasons, and I would give the numbers rather than assert it.
>
> **Index maintenance.** Every insert updates a B-tree, and at scale that is the bottleneck long before the
> disk is. Indexed Postgres does maybe ten to fifty thousand rows a second; a purpose-built store does a
> million. **One to two orders of magnitude**, and it is not a tuning gap.
>
> **Row overhead.** A Postgres row header is about 24 bytes, so a 16-byte measurement costs around 40 bytes
> stored, plus the index entry. Against 1.5 bytes compressed, that is roughly thirty times the storage.
>
> **Deleting old data.** `DELETE FROM metrics WHERE ts < now() - interval '30 days'` scans, marks dead tuples,
> and hands the problem to autovacuum, on a table that is being written to constantly. At volume this alone can
> be unsustainable. A time-series store deletes a whole chunk file.
>
> **No downsampling.** You keep everything or you write and maintain rollup jobs yourself.
>
> **But I would not say never.** At a few thousand points a minute, a time-partitioned Postgres table is
> completely fine and is one fewer system to run — partitioning by time fixes the deletion problem entirely.
> And TimescaleDB is genuinely the right answer when I need to join metrics against relational data, because
> 'p99 latency by customer tier', where the tier lives in a customers table, is trivial in SQL and awkward in
> PromQL."

**"Our monitoring fell over. What happened?"**

> "Cardinality, almost certainly, and I would say what to look for.
>
> Memory in these systems scales with the number of active **series**, not with the number of points — roughly
> a few kilobytes of in-memory chunk and index per active series. Half a million series is a gigabyte and a
> half; ten million is thirty gigabytes and a fragile process.
>
> The usual cause is a deploy. Somebody adds a label to an existing metric — a `path` label on an HTTP counter,
> and the paths contain order ids. That is one new series per order, multiplied by however many other labels
> already existed, and multiplied again by twelve if it is a histogram. A hundred thousand orders a day becomes
> 1.2 million new series a day, accumulating. **The person who did it was not thinking about monitoring at
> all**, which is why review does not catch it.
>
> Diagnosis: look at series count over time and find the step change, then look at which metric contributed.
> Prometheus exposes this directly, and the query for the worst offenders by label is one line.
>
> The fix has three parts. Immediately, drop the offending label at ingest with a relabel rule, which stops the
> bleeding without a deploy. Then remove it in code. Then prevent recurrence: a limit on series per metric at
> the ingest side, and a rule that anything unbounded — user ids, request ids, paths with ids, error strings —
> goes into a trace or a log, where high cardinality is normal, not into a metric label.
>
> **And the deeper point I would make: the monitoring system must not be able to be killed by an application
> deploy**, so the ingest-side limit is the real fix and the code change is a follow-up."

**"How do you compute p99 latency across the whole fleet?"**

> "Not by averaging per-host percentiles, and that is the first thing to say, because it is the common mistake.
> The mean of each host's p99 is not the fleet's p99 — percentiles do not average, and the error is largest
> exactly when the load is uneven, which is when you care.
>
> The correct approach is **histograms**. Each host records counts in latency buckets — under 10 ms, under 25,
> under 50, and so on — and every bucket is a counter. To get the fleet p99, you sum the buckets across hosts
> and then interpolate the quantile from the summed distribution. In PromQL that is `histogram_quantile(0.99,
> sum by (le) (rate(bucket[5m])))`, and the important part is that the summing happens **before** the quantile
> is computed.
>
> **The cost is cardinality:** a histogram with twelve buckets is twelve series per label combination, so
> histograms multiply your series count by their bucket count. That is why you put them on the handful of
> metrics where latency distribution matters and not on everything.
>
> **The accuracy limit is the bucket boundaries.** You cannot get a more precise answer than your bucket
> widths, so the boundaries have to be chosen for the range you care about — and if your p99 falls in the
> bucket 'between 1 second and 10 seconds', the interpolated answer is a guess. Native histograms in newer
> Prometheus versions fix this with exponential buckets, which is worth mentioning.
>
> **The alternative, summaries, computes the quantile on each host** — which is accurate per host and cannot be
> aggregated at all, so it answers a different and usually less useful question."

**"Keep two years of metrics without spending a fortune."**

> "Downsampling and tiered retention, and I would give the arithmetic.
>
> Raw fifteen-second data for two years on 500,000 series is about 3.1 terabytes. Raw for fifteen days,
> one-minute rollups for ninety days, and one-hour rollups for two years is about 175 gigabytes. **Eighteen
> times less**, for data nobody looks at in full resolution after a fortnight.
>
> **The design detail that matters is what you store in a rollup.** Not just the mean — minimum, maximum, sum
> and count. That way a spike at 10:03 is still visible as a maximum a year later, and you can recompute the
> average over any longer window correctly from the sum and count. Storing only the mean is the mistake that
> makes historical data useless for exactly the questions people ask of it.
>
> **And downsampling is not only about storage — it is what makes long queries possible.** A thirty-day p99
> query over raw data is a hundred million points and takes minutes; over hourly rollups it is four hundred
> thousand points and is instant.
>
> Implementation: Prometheus alone does not do this well, so it is Thanos, Mimir or VictoriaMetrics for the
> long-term tier, with the older chunks in object storage — which at two cents a gigabyte makes even the raw
> retention affordable if you really wanted it. Or continuous aggregates in TimescaleDB, which does it in SQL.
>
> **The question I would ask back is what the two years are actually for.** If it is capacity planning and
> year-on-year comparison, hourly is plenty. If it is a compliance requirement to reproduce an exact incident
> timeline, that is a different requirement and probably belongs in logs in object storage, not in a metrics
> system."

### The model answer

*"Design the monitoring for a platform: 2,000 services across 10,000 containers, plus business metrics like
orders per minute. Engineers need dashboards and alerts, and the data must be queryable for a year."*

> "Let me split this into three tiers, because 'metrics' here covers three things with different requirements
> and treating them the same is the mistake.
>
> **Tier one: infrastructure and service metrics.** Ten thousand containers, maybe 500 metrics each after
> exporters. That is five million series before any application labels — already large. Prometheus-compatible
> ingestion, but **not a single Prometheus**: I would shard by cluster or by service group, each instance
> scraping its own targets, with a global query layer — Thanos or Mimir — federating them. That keeps each
> instance's memory manageable and means one cluster's cardinality problem cannot take down monitoring for the
> others.
>
> **Pull for these**, because service discovery is the killer feature at this scale: the monitor asks
> Kubernetes what exists and scrapes it, so a new deployment is monitored with no configuration. And the `up`
> metric — a target failing to respond — is often the alert I actually want.
>
> **Tier two: business metrics.** Orders per minute, revenue, signup conversions. Lower volume, higher value,
> and they need to be joined against relational data — 'orders per minute by customer tier'. **This is where I
> would use TimescaleDB rather than Prometheus**, because that join is trivial in SQL and impossible in PromQL,
> and the volume is low enough that Postgres's write ceiling is irrelevant. Two different stores for two
> different jobs is the right answer here, not a compromise.
>
> **Tier three: what does not belong in metrics at all.** Per-request detail — user ids, order ids, paths with
> ids — goes into traces and logs. I would state this as a rule with a mechanism behind it, because the biggest
> operational risk in this design is a single deploy adding a high-cardinality label. So: an ingest-side limit
> on series per metric, alerting when it is approached, and relabel rules that drop known-dangerous labels.
> **The monitoring system must not be killable by an application deploy.**
>
> **Retention:** raw at 15 seconds for 15 days on local SSD; one-minute rollups for 90 days; one-hour rollups
> for two years, with the long tail in object storage through Thanos. Rollups store min, max, sum and count,
> not just the mean. Sizing: five million series at 1.5 bytes a point and a 15-second interval is about 43
> gigabytes a day raw, so 650 gigabytes for the fortnight — spread across the shards, that is comfortable per
> node, and the yearly tier in object storage is a few terabytes at two cents a gigabyte.
>
> **Alerting is where I would spend the design time**, because a monitoring system nobody trusts is worse than
> none. Alerts on symptoms rather than causes — error rate and latency that users experience, not CPU — with
> multi-window burn-rate alerts against a stated error budget, so a brief blip does not page anyone and a slow
> burn does. And every alert has to have an owner and a runbook, or it gets deleted.
>
> **And the part people leave out: the monitoring must not depend on what it monitors.** If Prometheus runs in
> the cluster it watches, it tells me nothing during the outage I care most about. So a small independent
> monitoring stack outside the main platform watches the platform, and an external service watches that one.
> **Two levels, and the outermost one is somebody else's problem** — which is the correct place for it to be."

---

## 9. Recall card

**Time-series data is append-only, arrives in order, has similar consecutive values and regular timestamps, and
is queried in ranges.** Each fact buys an optimisation: immutable time-chunks, delta-of-delta timestamps (one
bit on a fixed interval), XOR-compressed floats. **16 bytes per point becomes ~1.5.**

**Cardinality kills these systems, not point volume.** Every distinct label combination is a series, and memory
scales with **series count**. Never label with a user id, request id, or a path containing ids — that detail
belongs in traces and logs.

**Downsample and tier:** raw for ~15 days, 1-minute for 90, 1-hour for 2 years — about **18× less storage**,
and it is what makes long-range queries possible at all. **Store min/max/sum/count, not just the mean.**

**Percentiles do not average.** Use histograms, sum the buckets across hosts, then compute the quantile — and
remember each bucket is a series, so histograms multiply cardinality by the bucket count.

**Plain Postgres tops out around 10–50k rows/s** against ~1M for a purpose-built store, from index maintenance
and ~24-byte row headers. Fine at small volume with time partitioning; **TimescaleDB when you need to join
metrics against relational data.**
