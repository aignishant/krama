---
day: 171
track: system-design
title: "Monitoring, metrics, and alerting"
phase: "Reliability, security, and the interview itself"
status: written
---

# Monitoring, metrics, and alerting

## 1. What this is, and why they ask it

**Monitoring is how you find out that the thing you built is broken.** Metrics are the numbers you collect.
Alerting is the part that wakes someone up.

They ask it because **every high-level design interview ends here** — "what would you measure?", "what would
page you?" — and because **it is the question where prepared candidates most often have nothing.** They can
design the system and cannot say how they would know it was working.

**And because the answers separate people who have been on call from people who have not.** Anyone can say
"monitor CPU and memory". **The interesting answers are the ones that come from having been woken at three in
the morning by something that did not matter.**

**Three ideas carry almost the whole topic.**

**Averages lie, and percentiles do not.** An average response time of a hundred milliseconds can hide fifty
users waiting two seconds. **The average describes nobody.**

**Alert on symptoms, not on causes.** A machine at ninety percent memory is not a problem if users are fine.
**Users getting errors is a problem even if every machine looks healthy.**

**And every alert that fires without needing action makes every other alert less effective.** This is the one
that has a body count — **not because the systems failed, but because the person on call had stopped
listening.**

By the end of this lesson you can name the four golden signals, explain why the average is the wrong statistic
and why percentiles cannot be averaged either, size a metrics system's cardinality, write an alert that
deserves to wake someone, and answer "what would you put on the dashboard" for any system you have just
designed.

---

## 2. The story

The bell at the cold storage was wired to everything, and that was the trouble.

Karim had the night shift, in a room with a stool and a heater and a bell on the wall above the door. When
something at the plant was not right, the bell rang, and he went and looked.

**In the first week he went every time.**

The bell rang because the outer gate was open — the loading men had propped it with a crate again. It rang
because one of the small motors near the back was running warm, which it always did after midnight and always
settled by itself. It rang because a fuse in the lighting had gone. It rang, once, because a cat had got in
and sat on something.

**By the second week he had counted eleven ringings in a night.**

By the third week he went when it rang twice in a row.

By the fifth week he did not go at all until morning, **and he was not being lazy — he had learnt, correctly,
that the bell did not mean anything.**

**And then there was a night in March.**

The bell rang at about half past one, and Karim heard it, and turned over.

By the time the day men came in, everything in the far room had spoiled.

The manager came down and Karim expected to be shouted at, and instead the man stood in the doorway for a
long while looking at the bell.

**Then he said: "How many times did that thing ring last week?"**

Karim told him. Seventy-something. Maybe more.

**"And how many of them were worth getting up for?"**

Karim thought about it and said one. **The one in March.**

They rewired it that Thursday. **The bell was allowed to ring for exactly one thing — the temperature in the
rooms going the wrong way.** Everything else — the gate, the warm motor, the lights — went onto a board on the
wall that Karim walked past and looked at when he came on and when he left.

**Nobody added anything. They took things away.**

And the manager said one more thing on his way out, which Karim repeated for years afterwards.

**"The bell was never broken. It rang perfectly, every time. It was just ringing about things that were not
the point."**

---

## 3. The idea in plain English

**Karim's rewiring is the whole topic.** The board on the wall is a **dashboard**. The bell is an **alert**.
And the fix was not a better bell — **it was deciding which single thing was worth waking a person for.**

### The three pillars

**Metrics, logs, and traces answer different questions and cost wildly different amounts.**

```
   METRICS   numbers over time: requests/second, error rate, p99
             CHEAP — a few bytes per sample, aggregated on the way in
             ANSWERS: "is something wrong, and roughly where?"
             CANNOT ANSWER: "what happened to this particular request?"

   LOGS      one line per event, with detail
             EXPENSIVE — kilobytes per request
             ANSWERS: "what exactly happened at 02:14?"
             CANNOT ANSWER: "is the system healthy right now?" (too slow)

   TRACES    one request's journey across every service it touched
             VERY EXPENSIVE — sampled, typically at 1%
             ANSWERS: "where did those 800 milliseconds go?"
             CANNOT ANSWER: anything about the requests you didn't sample
```

**The workflow is metrics to detect, traces to localise, logs to diagnose.** **You do not choose between
them** — you use each for the question it answers cheaply.

### The four golden signals

**These four cover almost every service.** They come from Google's SRE practice and they are worth knowing by
name.

```
   LATENCY      how long requests take
                -> and SPLIT successful from failed: a fast 500 is
                   not good news, and it drags the average DOWN

   TRAFFIC      how many requests, per second

   ERRORS       what fraction fail
                -> including the ones that "succeed" with the wrong
                   answer, which is the hard part

   SATURATION   how full the system is — the resource nearest its limit
                -> the LEADING indicator: the only one that warns you
                   BEFORE users notice
```

**Two shorthands you will hear.** **RED — Rate, Errors, Duration — for services.** **USE — Utilisation,
Saturation, Errors — for resources** like disks and queues. **They are the same four signals viewed from
either end.**

### Percentiles, because the average lies

**This is the single most useful idea in the lesson.**

```
   1,000 requests:
     950 took 10 ms
      50 took 2,000 ms

   AVERAGE = (950 x 10 + 50 x 2,000) / 1,000 = 109.5 ms

   And NO REQUEST TOOK 109.5 ms.
   The average describes nobody.

   MEDIAN (p50) = 10 ms      "a typical request is fast"
   p95          = 10 ms
   p99          = 2,000 ms   "one in a hundred waits two seconds"
```

**A dashboard showing 109 milliseconds looks fine.** The fifty people who waited two seconds are invisible in
it. **Percentiles make them visible, and that is the entire argument.**

**And p99 matters more than "one percent" sounds**, because **a single page load makes many requests.**

```
   a page that makes 20 backend calls:
   P(all 20 under p99) = 0.99^20 = 0.818

   -> 18% of page loads contain at least one p99-slow call

   at 100 calls: 0.99^100 = 0.366
   -> 63% of page loads hit a p99 call
```

**So "only one percent of requests are slow" can mean "most page loads feel slow".** That arithmetic is worth
having ready — it is the strongest possible argument for caring about the tail.

**And here is the part that catches people: you cannot average percentiles.**

```
   machine A: 1,000,000 requests, p99 = 100 ms
   machine B:       100 requests, p99 = 10,000 ms

   average of the two p99s = 5,050 ms

   TRUE combined p99: the slowest 1% of 1,000,100 requests
   is about 10,001 requests, essentially all from A
   -> ~100 ms

   THE AVERAGE OF THE PERCENTILES IS 50x THE TRUTH.
```

**The fix is histograms.** Each machine exports **bucket counts** — "how many requests fell in 0–10 ms, 10–50
ms, 50–100 ms" — and **you sum the buckets across machines and compute the percentile from the sum.** That is
exactly what Prometheus's `histogram_quantile` does, **and it is why counters and histograms are the metric
types that aggregate and pre-computed percentiles are not.**

### SLI, SLO, SLA, and the error budget

**Three words that get confused, and the distinction is worth thirty seconds in an interview.**

```
   SLI   Service Level INDICATOR    the measurement
         "99.95% of requests succeeded in the last 30 days"

   SLO   Service Level OBJECTIVE    the target you hold yourselves to
         "99.9% of requests succeed"

   SLA   Service Level AGREEMENT    the contract, with money attached
         "99.5%, or we refund 10%"
         -> ALWAYS looser than the SLO, deliberately
```

**And the error budget is what makes an SLO useful rather than decorative.**

```
   an SLO of 99.9% is a BUDGET of 0.1% failure

   0.1% of a 30-day month = 43 minutes of downtime

   -> if you have used 5 minutes, ship freely
   -> if you have used 40, freeze and fix

   THE POINT: 100% is not a target. It is not achievable and
   aiming for it means never shipping anything. The budget
   converts reliability from an argument into arithmetic.
```

### Alert on symptoms, not causes

**Karim's manager rewired the bell to the temperature in the rooms — the thing that actually mattered — and
put the gate and the warm motor on the board.** That is the rule.

```
   ALERT (wake someone)         DASHBOARD (look at it in the morning)

   error rate above 1%          a machine at 90% memory
   p99 above 2 seconds          one node out of fifty unhealthy
   queue depth growing for      cache hit rate down 5%
     10 minutes                 disk 70% full
   no successful writes in
     5 minutes

   THE DIFFERENCE: the left-hand column is what a USER FEELS.
   The right-hand column is a CAUSE that may or may not become
   a symptom.
```

**A machine at ninety percent memory that is serving users perfectly is not an emergency.** **Users getting
errors while every machine looks healthy is an emergency** — and cause-based alerting misses it completely,
because you cannot enumerate every cause in advance. **You can enumerate the symptoms, and there are about
five of them.**

**The one exception is saturation**, which is a cause you *do* alert on — **"the disk will be full in four
hours"** — precisely because the symptom, when it arrives, is unrecoverable.

### Every page must pass three tests

```
   1. ACTIONABLE   is there something a human can do right now?
                   if not, it is a dashboard entry

   2. URGENT       must it be done now, or can it wait until morning?
                   if it can wait, it is a ticket

   3. HUMAN        does it need a person, or could it be automated?
                   if it can be automated, automate it
```

**Anything failing one of the three is Karim's bell.** And **every unnecessary page makes every real page less
effective**, because the person on call is learning — correctly — that the bell does not mean anything.

**The measurable version: track your alert-to-incident ratio.** If fewer than half of pages correspond to a
real problem, **the problem is the alerting, not the system.**

### Cardinality, which is what actually kills metrics systems

**Every distinct combination of label values is a separate stored series.** This multiplies, and it multiplies
faster than anyone expects.

```
   http_requests_total{endpoint, status, region, instance}

   50 endpoints x 5 statuses x 10 regions x 500 instances
   = 1,250,000 series

   add user_id, with 10,000,000 users:
   = 12,500,000,000,000 series

   -> the monitoring system falls over before the system it
      is monitoring does
```

**Never put an unbounded value in a label.** User ids, request ids, email addresses, full URLs with query
strings, error messages. **Those belong in logs and traces, which are built for high cardinality; metrics are
not.**

**This is the most common real-world monitoring outage**, and it is worth naming as a design constraint rather
than an operational footnote.

---

## 4. The picture

The three pillars, and which question each answers:

```
   ALERT FIRES: "error rate above 1%"
        |
        v
   METRICS   "errors started at 02:14, only in the eu-west region,
              only on the checkout endpoint"
        |    -> cheap, aggregated, always on
        v
   TRACES    "of the failing requests, 800 ms is spent in the
              payments service, and it then times out"
        |    -> sampled at 1%, one request's full journey
        v
   LOGS      "connection pool exhausted: 100/100 in use"
             -> expensive, full detail, the actual cause

   DETECT with metrics. LOCALISE with traces. DIAGNOSE with logs.
   Not a choice — a sequence.
```

Why the average lies:

```
   1,000 requests

   950 at 10 ms    ##################################################
    50 at 2,000 ms  ##

   AVERAGE  109.5 ms          <- describes NOBODY. No request
                                 took anything like this.
   p50       10 ms            <- "a typical request is fast"
   p95       10 ms
   p99    2,000 ms            <- the fifty people who waited

   A dashboard reading "109 ms" looks healthy.
   Fifty users waited two seconds and are invisible in it.


   AND THE TAIL COMPOUNDS:

   one page load = 20 backend calls
   P(all 20 fast) = 0.99^20 = 0.818

   -> 18% of PAGE LOADS contain a p99-slow call
   -> at 100 calls: 63%

   "Only 1% of requests are slow" can mean
   "most page loads feel slow".
```

Why percentiles cannot be averaged:

```
   machine A   1,000,000 requests   p99 =    100 ms
   machine B         100 requests   p99 = 10,000 ms

   NAIVE:  (100 + 10,000) / 2 = 5,050 ms

   TRUTH:  1,000,100 requests total
           the slowest 1% is ~10,001 requests
           essentially ALL of them are A's
           -> combined p99 ~= 100 ms

   THE NAIVE ANSWER IS 50x WRONG.

   THE FIX — export HISTOGRAM BUCKETS, sum them, then compute:

     bucket      A          B        SUM
     0-10 ms     900,000      0      900,000
     10-100 ms    90,000      5       90,005
     100ms-1s      9,900     30        9,930
     1-10 s          100     65          165

     -> now find the rank-990,099 request in the SUM
     -> this is what histogram_quantile() does

   Counters and histograms AGGREGATE. Pre-computed
   percentiles DO NOT. That is why the metric type matters.
```

The alerting pyramid:

```
                    /\
                   /  \      PAGE — wake someone
                  / 3-5 \    symptoms only, user-visible,
                 /alerts \   actionable + urgent + needs a human
                /----------\
               /            \   TICKET — look at it tomorrow
              /   ~20 rules   \  degradations, capacity warnings
             /------------------\
            /                    \  DASHBOARD — look when investigating
           /     everything else   \ causes, resource use, every metric
          /--------------------------\

   KARIM'S RULE: the bell rings for ONE thing.
   Everything else goes on the board.

   THE FIX IS ALWAYS SUBTRACTION. Nobody has ever improved
   an alerting system by adding alerts.
```

The error budget, as arithmetic:

```
   SLO 99.9%  ->  budget 0.1%

   per 30-day month (43,200 minutes):

     99%      432 minutes   = 7.2 hours
     99.9%     43 minutes
     99.95%    22 minutes
     99.99%     4.3 minutes
     99.999%   26 seconds     <- no human can respond in this;
                                 it must be fully automated

   USING THE BUDGET:
     5 of 43 minutes used   -> ship freely, take risks
    40 of 43 minutes used   -> freeze, fix reliability

   100% IS NOT A TARGET. It is unachievable, and aiming for it
   means never shipping. The budget turns an argument between
   product and operations into arithmetic.
```

Cardinality, which multiplies:

```
   http_requests_total{endpoint="/checkout", status="200",
                       region="eu-west", instance="i-4a2f"}

   50 endpoints
   x  5 statuses
   x 10 regions
   x 500 instances
   = 1,250,000 series      -> fine, ~9 GB/day

   NOW ADD user_id:
   x 10,000,000 users
   = 12,500,000,000,000 series

   -> your monitoring falls over before your system does

   NEVER a label:  user_id, request_id, email, full URL,
                   error message, timestamp

   Those belong in LOGS and TRACES, which are built for
   high cardinality. Metrics are not.
```

---

## 5. How it actually works

### The four metric types

**Getting these right is most of the practical skill**, and the aggregation rules follow from them.

```
   COUNTER     only ever goes up (or resets to zero on restart)
               requests_total, errors_total, bytes_sent_total
               -> you never read a counter; you read its RATE
               -> rate(requests_total[5m])
               -> ALWAYS use a counter for "how many things happened",
                  because the reset is detectable and a gauge's
                  missed increment is not

   GAUGE       goes up and down
               queue_depth, memory_bytes, active_connections
               -> read directly, and average or max across machines

   HISTOGRAM   counts per bucket, plus a sum and a count
               request_duration_seconds_bucket{le="0.1"}
               -> the ONLY correct way to get percentiles across
                  machines
               -> cost: one series PER BUCKET, so ~10-15x a gauge

   SUMMARY     percentiles computed on each machine
               -> CANNOT be aggregated. Use only when there is
                  exactly one instance, which there almost never is
```

**The counter-versus-gauge choice is where beginners go wrong**, and the rule is simple: **if you are counting
occurrences, it is a counter, always.** A gauge that you increment loses every increment that happened while a
scrape was missed; **a counter's true value is recoverable from any two samples.**

### Pull against push

```
   PULL (Prometheus)
     the monitoring system scrapes each instance every 15 seconds
     + the scrape itself is a health check
     + no client-side buffering or backpressure to design
     + service discovery tells it what exists
     - short-lived jobs die before being scraped
       -> a "push gateway" for those, which is an acknowledged wart

   PUSH (StatsD, OpenTelemetry, most hosted services)
     each instance sends its metrics onward
     + short-lived jobs and serverless work naturally
     + works through firewalls and across networks
     - a burst of clients can overwhelm the collector
     - "instance stopped sending" is ambiguous: dead, or just idle?
```

**Prometheus's pull model plus Grafana for display is the default open-source stack**, and naming it is worth
doing — **but the pull-versus-push trade is the part that shows understanding.**

### What a good alert looks like

```yaml
- alert: HighErrorRate
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
      / sum(rate(http_requests_total[5m])) > 0.01
  for: 5m
  labels:
    severity: page
  annotations:
    summary: "Error rate {{ $value | humanizePercentage }} (threshold 1%)"
    runbook: "https://wiki/runbooks/high-error-rate"
```

**Four things make this a good alert rather than a bad one.**

**`for: 5m`** — the condition must hold for five minutes. **Without it, a one-second blip at 02:14 pages
someone**, and that is Karim's warm motor.

**A ratio, not a count.** `errors > 100` fires during a traffic spike when the *rate* is unchanged. **The
fraction is what users experience.**

**The current value in the summary**, so the person woken knows whether it is 1.1% or 90% **before opening
anything.**

**A runbook link.** **An alert without one is an alert that assumes whoever is woken already knows what to
do** — and at three in the morning, six months after you wrote it, that person is not you.

### The runbook

```
   ALERT: HighErrorRate

   WHAT IT MEANS   more than 1% of requests returned 5xx for 5 minutes
   WHO IT AFFECTS  all users of the checkout flow
   FIRST CHECK     the errors-by-endpoint dashboard — is it one
                   endpoint or all of them?
   COMMON CAUSES   1. a deploy in the last 30 minutes -> roll back
                   2. the payments provider is down   -> enable the
                      degraded mode flag
                   3. connection pool exhausted       -> check pool
                      metrics, scale out
   ESCALATE TO     the payments on-call, if it is provider-side
   DO NOT          restart the whole fleet; it will make it worse
```

**The `DO NOT` line is the one people forget and the one that saves incidents.**

### Sampling traces

**A trace per request is unaffordable at scale**, so the question is which ones to keep.

```
   HEAD SAMPLING     decide at the start: keep 1% at random
                     + cheap, simple, no buffering
                     - you keep 1% of the errors too, which are
                       exactly the ones you wanted

   TAIL SAMPLING     buffer the whole trace, decide at the end
                     -> keep 100% of errors, 100% of anything
                        slower than a second, 1% of the rest
                     + you keep what matters
                     - must buffer every trace until it completes,
                       which is real memory and real complexity
```

**Tail sampling is what you want and head sampling is what most people run**, and saying that honestly is
better than pretending otherwise.

### Structured logs

```python
# bad: unparseable, and the interesting fields are trapped in prose
log.info(f"User {user_id} checkout failed after {ms}ms: {error}")

# good: queryable, and every field can be filtered on
log.info("checkout_failed", extra={
    "user_id": user_id,
    "duration_ms": ms,
    "error_code": error.code,
    "trace_id": trace_id,          # ties this line to the trace
})
```

**`trace_id` on every log line is the join key** between the three pillars — **it is what turns "metrics, logs
and traces" from three separate tools into one workflow.**

### The real systems

```
Prometheus            metrics, pull-based; the open-source default
Grafana               dashboards over almost any metrics store
OpenTelemetry         the vendor-neutral standard for all three pillars
Jaeger / Tempo        distributed tracing
Loki / Elasticsearch  log aggregation and search
PagerDuty / Opsgenie  routing pages to whoever is on call
Datadog / New Relic   all of the above, hosted, expensive at scale
```

---

## 6. The numbers

**Metrics storage, and where the cost comes from.**

```
1,250,000 series, scraped every 15 seconds:

  4 samples/minute x 60 x 24 = 5,760 samples/day per series
  1,250,000 x 5,760 = 7,200,000,000 samples/day

  Prometheus compresses to ~1.3 bytes/sample
  -> 7.2e9 x 1.3 = ~9.4 GB/day
  -> ~280 GB/month

-> AND THE DRIVER IS CARDINALITY, NOT SAMPLE RATE.
   Halving the scrape interval doubles the cost.
   Adding one label with 100 values multiplies it by 100.
```

**The cardinality explosion, quantified.**

```
   base:                          1,250,000 series    ~9 GB/day
   + user_id (10,000,000):   12,500,000,000,000       ~94 PB/day

-> a factor of TEN MILLION, from one label

This is the most common real-world monitoring outage, and the
fix is a rule rather than capacity: no unbounded value ever
becomes a label.
```

**The three pillars, priced against each other.**

```
100,000,000 requests/day

METRICS   aggregated, independent of request count
          ~9 GB/day

LOGS      1 KB per request
          100,000,000 x 1 KB = ~100 GB/day
          compressed ~10:1   = ~10 GB/day stored
          retained 30 days   = ~300 GB

TRACES    20 spans x 500 bytes = 10 KB per request
          100,000,000 x 10 KB = 1 TB/day at 100%
          at 1% sampling      = 10 GB/day

-> metrics are ~10x cheaper than logs and ~100x cheaper than
   unsampled traces, PER REQUEST

-> which is exactly why the workflow is metrics first: you
   detect with the cheap thing and only reach for the
   expensive ones once you know where to look
```

**Error budgets.**

```
per 30-day month = 43,200 minutes

  99%       432 minutes   7.2 hours
  99.9%      43 minutes
  99.95%     22 minutes
  99.99%      4.3 minutes
  99.999%    26 seconds

-> at 99.99% a human cannot respond in time. Detection,
   failover and rollback must ALL be automatic.
-> at 99.999% you are not designing an on-call rotation,
   you are designing a system with no manual steps at all.

Each extra nine costs roughly 10x more to achieve. "What
availability do you need?" is therefore a budget question,
and asking it is worth doing before promising anything.
```

**The tail, compounded — the argument for caring about p99.**

```
one page load = N backend calls, each independently
                p99-slow with probability 0.01

  N =   5   ->  1 - 0.99^5   =  4.9% of page loads affected
  N =  20   ->  1 - 0.99^20  = 18.2%
  N =  50   ->  1 - 0.99^50  = 39.5%
  N = 100   ->  1 - 0.99^100 = 63.4%

-> "only 1% of requests are slow" becomes "most page loads
   feel slow" at a hundred calls

-> AND IT IS THE STRONGEST ARGUMENT FOR FAN-OUT DESIGNS
   BEING BOUNDED: every extra service in the path multiplies
   your exposure to everyone else's tail
```

**Alert volume, which is a number worth tracking.**

```
a healthy on-call rotation:
  0-2 pages per week
  > 50% of pages correspond to a real problem

Karim's plant:
  ~70 rings/week, 1 worth acting on
  -> a 1.4% signal rate
  -> the correct human response is to stop listening,
     and he did

IF YOUR ALERT-TO-INCIDENT RATIO IS BELOW 50%, THE PROBLEM
IS THE ALERTING, NOT THE SYSTEM.
```

---

## 7. The trade-offs

**More metrics against fewer.** Collecting everything means you have the data when something odd happens; **it
also means cardinality growth, cost, and dashboards nobody can read.** The practical resolution is **collect
broadly, alert narrowly** — the expensive mistake is alerting broadly, not collecting broadly.

**Sensitive alerts against specific ones.** A low threshold catches problems early **and fires on noise**; a
high one fires only on real problems **and lets them run longer first.** `for: 5m` is the cheapest way to buy
specificity without losing sensitivity — **it costs you five minutes of detection time and removes almost
every blip.**

**Symptom alerts against cause alerts.** Symptoms catch problems you did not predict **and tell you nothing
about why.** Causes point straight at the fix **and only cover the failures you thought of in advance.** Alert
on symptoms; **put causes on the dashboard the runbook sends you to** — that combination gets both.

**Percentiles against averages.** Percentiles describe real users; **averages are cheap and aggregate
trivially.** Percentiles need histograms, which cost **one series per bucket** — ten to fifteen times a plain
gauge. **Worth it, and it is a real cost that belongs in the cardinality budget.**

**Sampling rate for traces.** One percent is affordable and **loses the rare failure you most wanted to see.**
Tail sampling — keep everything that errored or ran slow, sample the rest — is the right answer **and requires
buffering every trace until it completes**, which is genuine complexity most teams do not take on.

**Pull against push.** Pull makes the scrape a health check and needs service discovery; **push handles
short-lived and serverless work and makes "stopped sending" ambiguous** — dead, or idle? **Most large systems
end up running both**, and saying so is more honest than defending one.

**Build against buy.** Prometheus and Grafana are free and **cost you an engineer's ongoing attention.** Hosted
tools are excellent and **priced per host or per gigabyte, which becomes a genuinely large bill at scale** —
large enough that companies build their own to escape it, which is how the cycle repeats.

**And the one people forget: monitoring must survive the outage.** If your metrics run on the same
infrastructure as your product, **the incident takes both down and you are debugging blind.** Monitoring lives
in a separate failure domain, **and the alerting path in particular should have as few shared dependencies as
you can manage.**

---

## 8. In the interview

### How it gets asked

- *"What metrics would you put on the dashboard for this system?"* — the standard closer.
- *"What would page you at three in the morning?"*
- *"How would you know this was broken?"*
- *"Why percentiles rather than averages?"*
- *"What is an SLO, and how is it different from an SLA?"*
- *"What is the most useless alert you have ever had?"* — a real question, and a good one.

### The first ninety seconds

> "I would answer this in two halves, because **what you measure and what you get woken for are different
> questions**, and conflating them is where monitoring goes wrong.
>
> **What I measure: the four golden signals.** **Latency** — split into successful and failed, because a fast
> error is not good news and it drags the average down. **Traffic**. **Errors**, as a fraction. And
> **saturation** — how close the tightest resource is to its limit, **which is the only leading indicator of
> the four.**
>
> **And I would measure latency as percentiles, never averages.** If nine hundred and fifty requests take ten
> milliseconds and fifty take two seconds, **the average is a hundred and nine milliseconds and no request took
> anything like that.** The dashboard looks healthy and fifty people waited two seconds. **p50, p95, p99 —
> and the p99 is the one I would look at.**
>
> **What pages me: symptoms, not causes.** A machine at ninety percent memory is a dashboard entry. **Users
> getting errors is a page**, even if every machine looks perfectly healthy.
>
> **The reason is that you cannot enumerate the causes in advance** — there is always a new one — **but you
> can enumerate the symptoms, and there are about five of them.**
>
> **So: error rate above one percent for five minutes. p99 above two seconds for five minutes. Queue depth
> growing steadily for ten. No successful writes for five.** **Three to five paging alerts for a service, and
> if there are twenty, the on-call has already stopped reading them.**
>
> **The one cause I would page on is saturation** — 'the disk fills in four hours' — **because by the time
> that becomes a symptom it is unrecoverable.**
>
> **And every alert needs a runbook link.** At three in the morning, six months later, **the person woken is
> not me and does not have the context I had when I wrote it.**"

### The follow-ups

**"Why percentiles rather than averages?"**

> "**Because the average describes nobody, and I can show that in one example.**
>
> **A thousand requests: nine hundred and fifty take ten milliseconds, fifty take two seconds.** The average is
> **a hundred and nine and a half milliseconds** — and **not one request took anything close to that.** It is a
> number that describes an experience nobody had.
>
> **The median is ten milliseconds — 'typical requests are fast'. The p99 is two seconds — 'one in a hundred
> waits two seconds'.** Both are true, both matter, **and the average conceals both of them.**
>
> **The reason to care about the tail more than 'one percent' suggests is that a page load makes many
> requests.** **Twenty backend calls, each independently p99-slow one percent of the time: the chance all
> twenty are fast is 0.99 to the twentieth, which is 82%.** **So eighteen percent of page loads contain a
> p99-slow call.** **At a hundred calls it is sixty-three percent.**
>
> **'Only one percent of requests are slow' can mean 'most page loads feel slow'** — and that arithmetic is
> the strongest argument I know for bounding fan-out.
>
> **Now the part people get wrong, which is that you cannot average percentiles either.**
>
> **Machine A serves a million requests with a p99 of a hundred milliseconds. Machine B serves a hundred
> requests with a p99 of ten seconds.** Averaging gives **five thousand and fifty milliseconds.** **The true
> combined p99 is about a hundred milliseconds**, because the slowest one percent of a million and a hundred
> requests is essentially all A's. **The naive answer is fifty times wrong.**
>
> **The fix is histograms.** Each machine exports **bucket counts**; you **sum the buckets across machines and
> compute the percentile from the sum.** That is what `histogram_quantile` does.
>
> **Which is also why the metric type matters: counters and histograms aggregate correctly across machines and
> pre-computed percentiles — summaries — do not.** **So I would use a histogram even though it costs one
> series per bucket**, and I would count those buckets in the cardinality budget."

**"What would page you at three in the morning, and what would not?"**

> "**Three tests, and an alert has to pass all three: actionable, urgent, needs a human.**
>
> **Actionable** — is there something a person can do right now? If not, it is a dashboard entry. **Urgent** —
> must it be done now, or can it wait until morning? If it can wait, it is a ticket. **Needs a human** — if it
> can be automated, automate it and do not page anybody.
>
> **Anything failing one of those three degrades every other alert**, because the person on call learns that
> the alert does not mean anything. **And they are learning correctly** — that is the part worth stressing.
> It is not carelessness; it is an accurate response to a bad signal.
>
> **So: error rate above one percent for five minutes pages. p99 above two seconds for five minutes pages.
> Queue depth growing steadily for ten minutes pages** — that one is a leading indicator of a stall.
>
> **A single node unhealthy out of fifty does not page.** The system is meant to survive that; **if it does
> not, the fix is the system, not the alert.** **Ninety percent memory does not page.** **Cache hit rate down
> five percent does not page.**
>
> **The `for: 5m` on every one of those is not a detail.** Without it, **a one-second blip wakes someone**,
> and blips are constant. **It costs five minutes of detection and removes almost all of the noise.**
>
> **And every alert must be a ratio, not a count.** `errors > 100` fires during a traffic spike when nothing
> has actually got worse. **The fraction is what users experience.**
>
> **The number I would actually track is the alert-to-incident ratio.** **If fewer than half of pages
> correspond to a real problem, the problem is the alerting, not the system** — and the fix is always
> subtraction. **Nobody has ever improved an alerting system by adding alerts.**"

**"What is an SLO, and what is an error budget?"**

> "**An SLI is the measurement, an SLO is the target, an SLA is the contract with money attached.**
>
> **SLI: '99.95% of requests succeeded in the last thirty days.'** That is a number you measured.
>
> **SLO: '99.9% of requests succeed.'** That is what you hold yourselves to internally.
>
> **SLA: '99.5%, or we refund ten percent.'** **Always looser than the SLO, deliberately** — you want to breach
> your internal target and start fixing things long before you owe anyone money.
>
> **The error budget is what makes an SLO useful rather than decorative.**
>
> **An SLO of 99.9% is a budget of 0.1% failure. Over a thirty-day month that is forty-three minutes.**
>
> **And it is a budget you are meant to spend.** **Five minutes used: ship freely, take risks, do the risky
> migration.** **Forty minutes used: freeze features and fix reliability.**
>
> **The point is that a hundred percent is not a target.** It is not achievable, **and aiming for it means
> never shipping anything** — which is its own kind of failure. **The budget turns what is otherwise an
> argument between product and operations into arithmetic.**
>
> **And the numbers are worth knowing per month: 99% is seven hours, 99.9% is forty-three minutes, 99.99% is
> four minutes, 99.999% is twenty-six seconds.**
>
> **That last one is the interesting one, because it changes the design rather than the target.** **At
> twenty-six seconds a month, no human can be woken, read a runbook and act.** **Detection, failover and
> rollback must all be automatic** — you are not designing an on-call rotation, you are designing a system with
> no manual steps in the recovery path.
>
> **Each extra nine costs roughly ten times more.** **So 'what availability do you actually need?' is a
> question worth asking before promising anything** — and 'as high as possible' is not an answer."

### The model answer

*"You have just designed a URL shortener. What would you monitor, and what would page you?"*

> "**Two questions, and I would keep them apart: what I measure, and what wakes someone.**
>
> **The four golden signals first, applied to this system specifically.**
>
> **Traffic**, split by the two paths — **redirects and creations** — because they have completely different
> volumes and completely different failure consequences. **A redirect failing is a broken link somebody
> published; a creation failing is a user who retries.**
>
> **Latency as percentiles: p50, p95, p99, and separately for successes and failures**, because a fast 404
> would otherwise flatter the numbers.
>
> **Errors as a fraction**: 5xx rate on redirects, 5xx rate on creations. **And separately, 404 rate** — which
> is not an error exactly, **but a sudden spike in 404s means either a broken deploy or somebody enumerating
> our key space**, and both are worth seeing.
>
> **Saturation**: the database connection pool, and **how much of the key space is used**, since running out of
> short codes is a slow-moving disaster with a long lead time.
>
> **And two that are specific to this system rather than generic.** **Cache hit rate**, because redirects are
> read-heavy and cheap only while the cache is working — **a hit rate falling from 95% to 60% is a
> ten-times increase in database load that has not become a symptom yet.** And **redirect latency at the
> edge**, since the whole product is 'this is fast'.
>
> **Now what pages, and it is a much shorter list.**
>
> **Redirect error rate above one percent for five minutes.** That is users hitting broken links, and it is
> the core promise of the product.
>
> **Redirect p99 above five hundred milliseconds for five minutes.**
>
> **No successful creations in five minutes** — a total write outage, which the error-rate alert would miss if
> traffic dropped to zero.
>
> **And the one cause I would page on: key space above ninety percent used.** **That is saturation, and by the
> time it becomes a symptom every creation fails and there is no quick fix.** Four hours of warning is worth
> a page.
>
> **Four paging alerts. Everything else goes on a dashboard.**
>
> **Cache hit rate does not page** — it is a cause, it is on the dashboard, **and the runbook for the error-rate
> alert points at it as the first thing to check.** **One node unhealthy does not page.** **Elevated 404s do
> not page; they raise a ticket.**
>
> **Every one of those four has `for: 5m` on it**, because a one-second blip is not an incident, **and every
> one has a runbook link** — including a `DO NOT` line, since the instinct during a redirect outage is to
> restart the fleet, which empties the cache and makes it much worse.
>
> **Two things I would add unprompted.**
>
> **The cardinality rule.** **The short code must never be a metric label.** It is unbounded — millions of
> values — **and it would take the monitoring system down before the product.** Short codes go in logs and
> traces, which are built for that.
>
> **And the monitoring must not share a failure domain with the product.** **If they run on the same
> infrastructure, the outage takes both and we are debugging blind** — which is the failure that turns a
> twenty-minute incident into a three-hour one."

---

## 9. Recall card

**Three pillars, and it is a sequence rather than a choice: METRICS to detect (cheap, aggregated), TRACES to
localise (sampled ~1%), LOGS to diagnose (expensive, full detail).** `trace_id` on every log line is the join
key. Roughly 9 GB/day of metrics against 100 GB/day of logs and 1 TB/day of unsampled traces at 100M requests.

**Four golden signals: LATENCY (split successful from failed — a fast error drags the average down), TRAFFIC,
ERRORS (as a fraction, never a count), SATURATION (the only leading indicator).** RED for services, USE for
resources.

**The average describes nobody:** 950 requests at 10 ms and 50 at 2,000 ms averages **109.5 ms**, which no
request took. p50 = 10 ms, p99 = 2,000 ms. **And the tail compounds — 20 backend calls means 18% of page loads
hit a p99 call; 100 calls means 63%.** **You cannot average percentiles either** (p99s of 100 ms and 10,000 ms
average to 5,050 ms when the truth is ~100 ms — 50× wrong); **sum HISTOGRAM BUCKETS instead.** Counters and
histograms aggregate; summaries do not.

**Alert on SYMPTOMS, not causes** — you cannot enumerate causes in advance but there are about five symptoms.
**Every page must be actionable, urgent, and need a human**; anything else is a dashboard entry or a ticket.
**Three to five paging alerts per service**, each with `for: 5m`, a ratio not a count, the current value, and a
**runbook link with a DO NOT line.** **Saturation is the one cause worth paging on.** **The fix is always
subtraction** — and if under half of pages are real problems, the alerting is the problem.

**SLI is the measurement, SLO the internal target, SLA the contract (always looser).** **Error budget: 99.9% =
43 minutes a month; 99.99% = 4.3; 99.999% = 26 seconds, at which no human can respond and recovery must be
fully automatic.** Each nine costs ~10× more. **And CARDINALITY is what actually kills metrics systems** — one
`user_id` label turns 1.25M series into 12.5 trillion — **so no unbounded value is ever a label.** **Monitoring
lives in a separate failure domain**, or the outage takes it with you.
