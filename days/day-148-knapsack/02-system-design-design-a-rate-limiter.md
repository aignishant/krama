---
day: 148
track: system-design
title: "Design a rate limiter, at system scale"
phase: "High-level design case studies"
status: written
---

# Design a rate limiter, at system scale

## 1. What this is, and why they ask it

A rate limiter decides, for each incoming request, whether to serve it or reject it with a `429 Too Many
Requests`. "A hundred requests per minute per API key" is the usual shape.

It is a small, self-contained component and it is asked constantly, because it is one of the few designs where
**there is a specific algorithm to choose and the choices have visible, quantifiable differences**. Five
algorithms, each with a different memory cost and a different failure mode, and a candidate who knows why
sliding-window-counter exists is demonstrating something a candidate who says "we'll use Redis" is not.

The other half is the distributed problem, and it is the interesting half. **A limit is a shared count, and
your service is many machines.** Every machine checking a shared counter means a network round trip on every
request — on the path of every request in the system. Every machine keeping its own count means the effective
limit is `n` times what you promised.

They also ask it because it sits on the most latency-sensitive path there is: **the limiter runs before the
work, on every request, including the ones it is about to reject** — so it has to be faster than the thing it
protects.

By the end of this lesson you can choose an algorithm and defend it, handle the distributed count with a
stated accuracy trade, size the memory, decide what happens when the limiter itself fails, and name what to
limit on.

---

## 2. The story

The tank on the roof of Savitri's building holds about six thousand litres and the municipal line fills it at
whatever rate the municipal line feels like, which is roughly steady and roughly slow.

Twenty flats draw from it.

Most days nobody thinks about it. The line runs, the tank fills, people use water, and the level stays
somewhere in the middle.

**What everybody understands without ever having explained it is that the tank lets you take a lot at once.**
If nobody has drawn much since yesterday, the tank is full, and you can run the washing machine and fill the
drums and wash the car and it is fine. The tank absorbs that.

**And that if everybody does it on the same morning, there is nothing.** The tank empties by nine, and then
you get whatever the line is putting in, drop by drop, which is not enough to wash a bucket.

The thing that caused the trouble, and eventually the meeting, was the second-floor flat.

They have a motor. Everybody has a motor, but theirs runs at half past five every morning and pulls until
their own tank is full, and their own tank is a thousand litres. So by six o'clock, six mornings a week, a
sixth of the building's water had gone to one flat, and by the time anybody else was up there was not much
left.

Nobody was breaking any rule, because there was no rule. **They were just faster.**

The committee's answer, after two meetings and one shouting match, was a timer on each flat's motor. Fifteen
minutes, and then it cuts, and you wait an hour before it will run again.

Savitri's observation, which she made at the second meeting and which everybody agreed with and nobody acted
on for another month, was that the rule was not really about being fair. **It was that if everybody drew as
fast as they physically could, the pump at the bottom burnt out**, and it had, twice, and each time cost
eleven thousand rupees and four days without water.

**The timer was not there to make people share. It was there to stop the pump dying.**

---

## 3. The idea in plain English

Savitri's tank is a token bucket, and her observation at the second meeting is what rate limiting is actually
for.

**A rate limiter answers one question per request: is this allowed right now?** If yes, serve it. If no,
return `429 Too Many Requests`, ideally with a `Retry-After` header saying when to come back.

**And it exists for three different reasons that are worth separating**, because they lead to different
limits:

- **Protecting the system.** The pump. Beyond some rate, the service degrades for everybody, so the limiter
  sheds load to keep it alive. This is the important one.
- **Fairness.** Stopping one client consuming everything. The second-floor flat.
- **Cost and abuse.** Metering a paid API, or stopping credential-stuffing and scraping.

**Now the five algorithms**, in increasing order of accuracy and cost.

**Fixed window.** Count requests per key per clock minute. Reset at the boundary. **One counter and one
timestamp per key — the cheapest possible.**

**And it allows twice the limit**, which is its defining flaw. With a limit of a hundred per minute, a client
can send a hundred at 10:00:59 and another hundred at 10:01:00 — two hundred requests in one second, both
windows technically satisfied. **That is the boundary problem**, and it matters exactly when it matters most,
because a burst is what you were trying to prevent.

**Sliding window log.** Store the timestamp of every request in the last window. To decide, drop everything
older than the window and count what is left. **Perfectly accurate** — no boundary problem at all.

**And it stores one timestamp per request.** A limit of a thousand per hour means up to a thousand timestamps
per key, and at a million keys that is a billion timestamps. **Accurate and expensive**, and the memory scales
with the *limit*, not with the number of keys.

**Sliding window counter.** The practical compromise. Keep a counter for the current window and the previous
one, and estimate:

```
count = current_window_count + previous_window_count x (fraction of the previous window still in view)
```

At 10:00:15 with a one-minute window, 75% of the previous minute is still inside the sliding window, so you
count 75% of it. **Two counters per key — the same memory as fixed window — and it removes almost all of the
boundary problem.**

**It is an approximation** — it assumes the previous window's requests were spread evenly — so it can be
slightly wrong in both directions. **In practice the error is small and it is what most production limiters
use.**

**Token bucket.** Savitri's tank. A bucket of capacity `B` refills at `R` tokens per second. Each request
takes one token; no token, no service.

**Two numbers with two different jobs, and separating them is the point:** `R` is the sustained rate, `B` is
how much burst is tolerated. **A client that has been quiet can spend the whole bucket at once**, which is
usually the behaviour you want — a mobile app that syncs after being offline should not be throttled for
being idle.

**And it stores two values per key** — the token count and the last refill time — and the refill is computed
lazily on read rather than by a background job:

```
tokens = min(capacity, tokens + (now - last_refill) x rate)
```

**Leaky bucket.** A queue drained at a fixed rate. Requests join the queue; the queue is served steadily;
overflow is rejected. **It smooths output completely** — the downstream sees a perfectly even rate regardless
of the input — at the cost of latency, because a request may sit in the queue.

**Token bucket allows bursts; leaky bucket eliminates them.** That is the distinction, and which you want
depends on whether the thing you are protecting minds a burst.

**Now the distributed half, which is the interesting part.**

**The limit is per client and your service is `n` machines.** Three options.

**One: a shared counter in Redis.** Every request does an atomic increment against a central store.
**Accurate**, and it adds a network round trip — half a millisecond in the same datacentre — to *every request
in the system*, including rejected ones, and makes Redis a hard dependency of every request.

**Two: local counters, limit divided by `n`.** No coordination at all, no latency. **And it is wrong whenever
traffic is uneven**, which it always is: a client hitting one machine gets a hundredth of the intended limit,
and the same client spread across all machines gets the full limit. **Load balancers do not distribute one
client's traffic evenly**, so this is not a theoretical objection.

**Three: local counters with asynchronous synchronisation.** Each machine limits locally and periodically
shares its counts. **Fast, approximately correct, and it over-admits by up to one sync interval's worth of
traffic.** This is what most large systems actually do, and being able to say "it over-admits by a bounded
amount, and here is the bound" is the answer.

**And the last decision, which is a policy question rather than a technical one: what happens when the limiter
fails?**

**Fail open** — allow everything — means an outage of Redis becomes unlimited traffic to the thing the limiter
was protecting, which is how a small failure becomes a large one. **Fail closed** — reject everything — means
an outage of Redis becomes a total outage of your service.

**The usual answer is to fail open with a local fallback**: if the shared store is unreachable, fall back to
a per-machine limit that is deliberately generous. **Not perfect, and much better than either extreme** — and
it must be decided in advance, or whoever writes the error handler decides it for you.

---

## 4. The picture

The boundary problem, which is why fixed window is not enough:

```
  limit: 100 per minute, FIXED WINDOW

  10:00:00 ------------------------ 10:01:00 ------------------------ 10:02:00
  |                                 |                                 |
  |                          100 reqs|100 reqs                        |
  |                          at :59  |at :00                          |
  |                                 |                                 |
  window 1 count: 100  (allowed)    window 2 count: 100  (allowed)

  -> 200 requests in ONE SECOND, and both windows are within the limit.
```

The five algorithms, compared:

```
                     state per key        accuracy         bursts
  fixed window       counter + window     2x at boundary   allowed at boundaries
  sliding log        one ts per request   exact            none
  sliding counter    2 counters           ~exact           slight
  token bucket       tokens + timestamp   exact rate       ALLOWED, up to B
  leaky bucket       queue                exact rate       eliminated (queued)
```

Token bucket, drawn as the tank:

```
  capacity B = 10 tokens,  refill R = 1 token/second

  t=0    [##########]  10 tokens.  A burst of 10 requests: all served.
  t=0+   [          ]   0 tokens.  Request 11: REJECTED.
  t=3    [###       ]   3 tokens.  (3 seconds x 1/s)
  t=10   [##########]  10 tokens.  Capped at B — idle time does not accumulate forever.

  R decides the SUSTAINED rate.
  B decides how much BURST is forgiven.
  Two numbers, two jobs.
```

Sliding window counter, which is the practical middle:

```
  limit 100/minute, now = 10:01:15   (25% into the current window)

  previous window (10:00-10:01):  80 requests
  current  window (10:01-10:02):  30 requests so far

  the sliding window covers the last 60 s:
     75% of the previous window + all of the current

  estimate = 80 x 0.75 + 30 = 60 + 30 = 90     -> under 100, ALLOW

  two counters per key. Fixed-window memory, sliding-window behaviour.
```

The distributed problem:

```
  SHARED COUNTER                LOCAL, LIMIT/n            LOCAL + SYNC

  every request                 no coordination           local decisions,
   -> Redis INCR                 -> zero latency           periodic gossip
                                                           of counts
  + exact                       + fastest possible        + fast
  - +0.5 ms on EVERY request    - wrong whenever traffic  + approximately right
  - Redis is now a hard           is uneven, which is     - over-admits by up to
    dependency of everything      always                    one sync interval
```

---

## 5. How it actually works

### Token bucket, which is the one to be able to write

```python
import time

class TokenBucket:
    """capacity = burst allowance, rate = sustained tokens per second."""

    def __init__(self, capacity: float, rate: float) -> None:
        self.capacity = capacity
        self.rate = rate
        self.tokens = capacity
        self.last = time.monotonic()

    def allow(self, cost: float = 1.0) -> bool:
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False
```

**Three things to point at.**

**`time.monotonic()`, not `time.time()`** — for exactly the reason from
[day 123](../day-123-word-search-ii/README.md). A wall-clock correction that steps backwards makes
`now - last` negative and the bucket loses tokens; one that steps forward hands out a full refill instantly.
**A rate limiter that occasionally lets through double the limit is usually this bug.**

**The refill is lazy**, computed on access from the elapsed time. No background job, no per-key timer, and a
key that is never touched costs nothing.

**And `cost` as a parameter** means expensive endpoints can consume more than one token, which is how you
express "a search costs ten times a simple read" in a single limiter.

### Sliding window counter, in Redis

```python
def allow(redis, key: str, limit: int, window: int) -> bool:
    now = time.time()
    current_window = int(now // window)
    elapsed_fraction = (now % window) / window

    pipe = redis.pipeline()
    pipe.get(f"{key}:{current_window}")
    pipe.get(f"{key}:{current_window - 1}")
    current, previous = (int(x or 0) for x in pipe.execute())

    estimate = previous * (1 - elapsed_fraction) + current
    if estimate >= limit:
        return False

    pipe = redis.pipeline()
    pipe.incr(f"{key}:{current_window}")
    pipe.expire(f"{key}:{current_window}", window * 2)     # self-cleaning
    pipe.execute()
    return True
```

**The `expire` is what keeps the memory bounded** — keys for old windows delete themselves, so there is no
cleanup job and no unbounded growth. **That is the single most important line for operating this**, and it is
easy to leave out.

**The read-then-write is not atomic**, so two concurrent requests can both read 99 and both proceed. **That is
usually acceptable** — being one over on a limit of a hundred is not a failure — and if it is not, the whole
thing goes into a Lua script, which Redis executes atomically.

### Token bucket in Redis, atomically

```lua
-- KEYS[1] = bucket key, ARGV = capacity, rate, now, cost
local bucket = redis.call('HMGET', KEYS[1], 'tokens', 'last')
local tokens = tonumber(bucket[1]) or tonumber(ARGV[1])
local last   = tonumber(bucket[2]) or tonumber(ARGV[3])

tokens = math.min(tonumber(ARGV[1]), tokens + (ARGV[3] - last) * ARGV[2])

local allowed = tokens >= tonumber(ARGV[4])
if allowed then tokens = tokens - tonumber(ARGV[4]) end

redis.call('HMSET', KEYS[1], 'tokens', tokens, 'last', ARGV[3])
redis.call('EXPIRE', KEYS[1], 3600)
return allowed and 1 or 0
```

**One round trip, atomic, and the `EXPIRE` bounds the memory.** This is close to what production limiters
actually run, and being able to say "the whole check-and-decrement is one Lua script so it is atomic" is worth
more than the exact Lua.

### Where the limiter goes

```
client -> CDN -> API gateway -> [RATE LIMITER] -> service -> database
                                     ^
                          before the work, on every request
```

**At the gateway, not in each service**, for three reasons: rejected requests never reach the services at all,
the policy is in one place, and the count is naturally shared because the gateway fleet is one thing rather
than many.

**And a second, cruder limiter belongs further out** — at the CDN or load balancer — because a volumetric
attack should be dropped before it reaches anything of yours. **Layered limits: a crude one at the edge, a
precise one at the gateway.**

### What to limit on

```
by API key / account     the normal case for a paid API
by user id               for authenticated traffic
by IP                    for unauthenticated traffic — and it is crude:
                           a university or a mobile carrier NATs thousands
                           of users behind one address
by endpoint              expensive endpoints get their own, tighter limit
by a combination         (user, endpoint) is the usual production shape
```

**Multiple limits apply at once**, and a request must pass all of them: a global limit, a per-user limit, and
a per-endpoint limit. **Which is worth saying, because a single limiter is rarely enough** — you want to stop
one user hammering search *and* stop the whole system exceeding what the database can take.

### The response

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1767225600
```

**`Retry-After` is the one that matters**, because without it every rejected client retries immediately and
the limiter becomes a busy-wait for the whole client base. **And the retry should be jittered**, or every
client rejected in the same second comes back in the same second — which is
[day 125](../day-125-what-a-graph-is/README.md)'s thundering herd, caused by your own limiter.

**Returning the headers on successful requests too** lets a well-behaved client slow down before being
rejected, which is strictly better than rejecting it.

### The failure decision

```
shared store unreachable:
  fail closed   -> reject everything    -> Redis outage = total outage
  fail open     -> allow everything     -> Redis outage = unlimited traffic to
                                           the thing you were protecting
  fail open with a LOCAL fallback:
                -> each machine applies a generous local limit
                -> approximately right, bounded damage
```

**The third is the answer, and it must be decided in advance.** Whoever writes the exception handler decides
it otherwise, and they will pick whichever is easier to type.

---

## 6. The numbers

**Memory per key, which is what decides the algorithm at scale:**

```
fixed window        counter + window id                 ~16 bytes
sliding counter     2 counters + 2 window ids           ~32 bytes
token bucket        tokens + timestamp                  ~16 bytes
sliding log         one timestamp per request in window ~8 bytes x limit
```

```
1,000,000 active keys, limit 1,000/hour

  fixed window       1,000,000 x 16 B                   = 16 MB
  sliding counter    1,000,000 x 32 B                   = 32 MB
  token bucket       1,000,000 x 16 B                   = 16 MB
  sliding log        1,000,000 x 1,000 x 8 B            = 8 GB
```

**Eight gigabytes against thirty-two megabytes**, and that is the whole argument against the exact algorithm.
**With Redis key overhead the real figures are two to five times larger**, so the sliding log is realistically
20–40 GB — one node's entire memory to be exactly right about a limit where being 2% wrong is harmless.

**Latency, and this is on every request:**

```
local in-memory check          ~0.001 ms
Redis in the same datacentre   ~0.5 ms round trip
Redis cross-AZ                 ~1-2 ms
```

```
service p50 latency 20 ms
  + 0.5 ms limiter              = 2.5% slower
service p50 latency 2 ms
  + 0.5 ms limiter              = 25% slower
```

**The limiter's cost is a percentage of what it protects**, so it matters enormously for a fast service and
barely at all for a slow one. **That is the argument for local-with-sync in front of a very fast service.**

**Redis capacity:**

```
Redis                          ~100,000 ops/s per instance
one Lua script per request     = 1 op
                               -> 100,000 requests/s per Redis instance
```

```
service handling 1,000,000 requests/s
  -> 10 Redis instances, sharded by key
  -> and sharding is trivial, because each key is independent
```

**The independence of keys is why this shards perfectly** — there is never a cross-shard question — and it is
worth saying, because it means the shared-counter approach scales further than people assume.

**The boundary problem, quantified:**

```
limit 100/minute, fixed window
  worst case in any 60-second span: 200
  -> 2x the intended limit, in the worst possible instant

sliding window counter
  error depends on how unevenly the previous window was distributed
  worst case ~ +/- 10-20% in adversarial patterns
  typical    < 5%
```

**Two hundred percent against five percent, for the same memory.** That comparison is the reason
sliding-window-counter exists.

**The distributed error:**

```
local counters, sync every 10 s, limit 100/minute, 10 machines

  worst case: each machine admits up to its share, unaware of the others,
  for up to one sync interval
  over-admission bound ~ (machines x limit x sync interval / window)
                       = 10 x 100 x 10/60  ~ 167 extra requests worst case

  -> the limit is effectively "100, but up to ~270 in a bad minute"
```

**Being able to state that bound is the answer**, rather than claiming the approximation is exact.

**Cost of the limiter itself:**

```
3 Redis nodes for 300,000 req/s of limiting  ~$300-600/month
against protecting a database fleet costing many times that
```

**And what it saves**, which is the justification:

```
without a limiter, one client scraping at 10,000 req/s
  -> database saturated, p99 for everyone goes from 50 ms to 5 s
  -> effectively an outage caused by one client
with a limiter at 100/s for that client
  -> 99% of that traffic rejected in 0.5 ms each, never reaching the database
```

---

## 7. The trade-offs

**Accuracy against memory, and the sliding log is the extreme.** Exact limiting costs one timestamp per
request — 8 GB against 32 MB at a million keys with a limit of a thousand. **Almost nobody needs exactness**,
because a limit is a policy choice with a round number in it, and being 5% over on "a hundred a minute" harms
nothing. **Pay for exactness only when the limit represents something real** — a paid quota, a regulatory cap.

**Accuracy against latency in the distributed case.** A shared counter is exact and adds half a millisecond to
every request in the system, including the ones being rejected, and makes the store a hard dependency of
everything. Local counters are free and wrong. **Local-with-sync is fast and over-admits by a bounded amount**,
and the honest version of that answer states the bound.

**Bursts allowed against bursts eliminated.** Token bucket forgives a client that has been quiet, which is
usually correct — a mobile app syncing after being offline is not abusive. Leaky bucket smooths completely and
adds queueing latency. **Ask what you are protecting: a database that dislikes spikes wants smoothing; an API
whose users are bursty by nature wants the bucket.**

**Limiting by IP is crude and often the only option.** A university, an office or a mobile carrier puts
thousands of users behind one address, so an IP limit either throttles them all or is too loose to matter. **For
unauthenticated traffic there is nothing better**, which is an argument for requiring authentication on
anything expensive rather than for a cleverer limiter.

**Fail open against fail closed, and neither is right alone.** Open turns a limiter outage into unlimited load
on the protected system; closed turns it into a total outage. **Open with a generous local fallback is the
answer, and it must be chosen deliberately.**

**And the limiter is itself something that can fail.** It runs before every request, so its latency is added to
everything and its availability multiplies with the service's. **A rate limiter that adds two milliseconds and
99.9% availability to a service with a 2 ms p50 has made things worse**, and that is worth checking rather than
assuming.

**When would I not build one?** When the traffic is internal and trusted, where a limiter adds latency and
failure modes against an attack that does not exist. When the platform already provides one — every API
gateway and CDN has rate limiting built in, and using it is strictly better than writing one. And when the
real problem is a single misbehaving client, where a targeted block is simpler than a general mechanism.

---

## 8. In the interview

### How it gets asked

- *"Design a rate limiter for an API used by a million clients."* — the standard prompt.
- *"Which algorithm, and why?"* — the part with a real answer.
- *"Your service is fifty machines. How do you share the count?"* — the distributed half.
- *"What happens when Redis is down?"* — the policy question.
- *"A client sends a hundred requests at 59 seconds and a hundred at 60. What happens?"* — the boundary
  problem.
- *"What do you limit on?"*

### The first ninety seconds

> "Let me split it into the algorithm and the distributed problem, because they are separate decisions and the
> second is the harder one.
>
> **On the algorithm, I would use a sliding window counter or a token bucket, and I would reject fixed window
> for a specific reason.** Fixed window counts per clock minute and resets at the boundary, which means a
> client can send a hundred requests at 10:00:59 and another hundred at 10:01:00 — **two hundred in one
> second, with both windows within the limit.** That is twice the intended rate at exactly the moment a burst
> is happening, which is what I was trying to prevent.
>
> **The exact fix is a sliding window log** — store every request's timestamp and count what falls inside the
> window. Perfectly accurate, and it costs one timestamp per request: at a million keys with a limit of a
> thousand an hour, that is eight gigabytes against thirty-two megabytes for two counters. **I would not pay
> that**, because a limit is a policy number and being a few percent over harms nothing.
>
> **So: sliding window counter.** Keep the current window's count and the previous window's, and weight the
> previous one by how much of it is still in view. Two counters per key — fixed-window memory, and the
> boundary error drops from 200% to a few percent.
>
> **Or a token bucket if bursts should be forgiven**, which is often what you actually want: a bucket of
> capacity `B` refilling at `R` per second, where `R` is the sustained rate and `B` is how much burst is
> tolerated. **Two numbers doing two different jobs.** A client that has been idle can spend the whole bucket
> at once, which is right for something like a mobile app syncing after being offline.
>
> **Now the distributed half, which is the interesting part.** The limit is per client and I have many
> machines, so the count is shared state. Shared Redis is exact and adds half a millisecond to **every request
> in the system**, including rejected ones. Local counters with the limit divided by the machine count need no
> coordination and are wrong whenever traffic is uneven, which it always is.
>
> **I would use local counters with periodic synchronisation and state the error bound** — it over-admits by
> up to one sync interval's worth of traffic, which I can compute.
>
> How fast is the service being protected? Because if its p50 is two milliseconds, a half-millisecond limiter
> is a 25% tax and that changes the answer."

### The follow-ups

**"Walk me through the boundary problem."**

> "Fixed window with a limit of a hundred per minute. The counter resets at each clock minute.
>
> A client sends a hundred requests at 10:00:59. The counter for the 10:00 window reaches a hundred — allowed,
> exactly at the limit. One second later the clock ticks over, the counter resets, and the client sends another
> hundred at 10:01:00. The 10:01 window reaches a hundred — also allowed.
>
> **Two hundred requests in a one-second span, and no window was ever exceeded.** The implementation is
> perfectly correct against its own definition and the effective limit is double.
>
> **And it is worst exactly when it matters**, because a client trying to maximise throughput will discover the
> boundary and sit on it.
>
> **The exact fix is the sliding window log** and it costs a timestamp per request. **The practical fix is the
> sliding window counter:** hold the current and previous window counts and weight the previous by the fraction
> still in view. At fifteen seconds into a minute, seventy-five percent of the previous minute is still inside
> the last sixty seconds, so I count seventy-five percent of it.
>
> **That is an approximation** — it assumes the previous window's traffic was spread evenly, which a burst at
> the very end violates — so it can be off by ten or twenty percent in an adversarial pattern and under five
> percent normally. **Two hundred percent error down to five, for the same memory**, which is why it is what
> most production limiters use."

**"Fifty machines. How do you share the count?"**

> "Three options, and I would name the trade in each rather than pick one blindly.
>
> **A shared counter in Redis** is exact: every request does one atomic operation against a central store. The
> cost is a network round trip on the path of every request in the system — half a millisecond in the same
> datacentre, one to two across availability zones — including on requests that are about to be rejected, which
> is faintly absurd. **And it makes Redis a hard dependency of every request**, which raises the failure
> question immediately.
>
> **It shards perfectly, though**, and that is worth saying: each key's count is independent, so there is never
> a cross-shard question, and a million requests a second is ten Redis instances sharded by key.
>
> **Local counters with the limit divided by fifty** need no coordination and are simply wrong, because load
> balancers do not spread one client's traffic evenly. A client whose connections land on one machine gets a
> fiftieth of the intended limit; one spread across all of them gets the full limit. **That is not a
> theoretical objection, it is what happens.**
>
> **Local counters with periodic synchronisation** is what I would use, and the answer is to state the bound.
> Each machine limits locally and broadcasts its counts every few seconds; between syncs a machine is unaware
> of the others, so the worst-case over-admission is roughly the machine count times the limit times the sync
> interval divided by the window. At fifty machines, a hundred per minute and a ten-second sync, that is a few
> hundred extra requests in a bad minute.
>
> **So the honest description is 'a hundred a minute, and up to about three hundred in an adversarial minute'**
> — and whether that is acceptable is a product question, not a technical one. For protecting a database it
> absolutely is; for a metered paid quota it is not, and then I pay the round trip."

**"What happens when Redis goes down?"**

> "That is a policy decision that has to be made in advance, because otherwise whoever writes the exception
> handler makes it, and they will pick whichever is easier to type.
>
> **Fail closed** — reject everything when the limiter cannot decide — means a Redis outage becomes a total
> outage of the service. **The limiter, which exists to protect availability, has become the thing that
> destroys it.**
>
> **Fail open** — allow everything — means a Redis outage becomes unlimited traffic to whatever I was
> protecting. **A small failure becomes a large one**, and it happens at the worst moment, because the same
> incident that took Redis down may be the one generating the traffic.
>
> **What I would build is fail open with a local fallback.** If the shared store is unreachable, each machine
> applies a generous local limit from memory — say five times the per-machine share. Not accurate, and it
> bounds the damage: the protected system sees a multiple of the intended load rather than an unbounded amount,
> and the service stays up.
>
> **And I would circuit-break the limiter itself.** If Redis is timing out, I should not wait for the timeout
> on every request — that adds the full timeout to every request in the system and turns a degraded dependency
> into an outage by thread exhaustion. **After a few failures, stop calling it and use the local fallback**,
> with periodic probes. That is [day 126](../day-126-graph-representation/README.md)'s circuit breaker applied
> to the limiter, and it is the part people forget."

**"What do you limit on?"**

> "Several things at once, and a request has to pass all of them — a single limiter is rarely enough.
>
> **By API key or account** for authenticated traffic, which is the normal case and the one that maps to a
> plan or a quota.
>
> **By IP for unauthenticated traffic**, and I would be honest that it is crude: a university, an office or a
> mobile carrier puts thousands of users behind one address, so the limit either throttles them all or is too
> loose to be useful. **The real answer to that is to require authentication for anything expensive**, rather
> than to build a cleverer limiter.
>
> **By endpoint**, because a search that runs a full-text query and a fetch-by-id are not comparable. Either a
> separate limit per endpoint, or — which I prefer — a **cost per request** in the token bucket, so an
> expensive endpoint takes ten tokens and a cheap one takes one. **One limiter, one number per endpoint**, and
> it composes better than a matrix of limits.
>
> **And a global limit**, which is the one people forget: the sum of everybody's permitted traffic can still
> exceed what the database can take. **The per-user limit is about fairness; the global limit is about the
> pump.**
>
> **Layered, too:** a crude volumetric limit at the CDN or load balancer, so an attack is dropped before it
> reaches anything of mine, and the precise per-user limit at the gateway. **Rejecting a flood at the edge costs
> nothing; rejecting it at the gateway still costs a TLS handshake and a Redis lookup per request.**"

### The model answer

*"Design a rate limiter for a public API: a million clients, a hundred thousand requests a second, per-client
limits that vary by plan."*

> "Let me establish where it sits, then the algorithm, then the distributed problem — and the constraint that
> shapes it is that this thing runs before every request, including the ones it rejects, so its own cost is on
> the critical path of everything.
>
> **Placement: at the API gateway.** Rejected requests then never reach the services at all, the policy lives
> in one place, and the gateway fleet is a natural place for shared state. **Plus a crude volumetric limit at
> the CDN**, so a genuine flood is dropped before it costs me a TLS handshake.
>
> **Algorithm: token bucket**, and I would choose it over sliding window counter for a specific reason. Plans
> vary, and a token bucket expresses a plan as two numbers — sustained rate and burst allowance — which maps
> directly onto how plans are actually sold: 'a thousand requests a minute, bursting to two hundred'. **And a
> per-request cost lets me price expensive endpoints in the same mechanism** rather than maintaining a separate
> limit per endpoint.
>
> **Implementation: one Redis hash per key holding the token count and the last refill time, updated by a Lua
> script** so the whole check-and-decrement is atomic in one round trip. The refill is lazy — computed from the
> elapsed time on access — so there is no background job and an idle key costs nothing. **And an `EXPIRE` on
> every write**, which is what keeps the memory bounded with no cleanup job, and is the line most often left
> out.
>
> **Sizing.** A million active keys at roughly a hundred bytes with Redis overhead is about a hundred
> megabytes — trivial. A hundred thousand requests a second is one Lua call each, and Redis does around a
> hundred thousand operations a second per instance, so **three instances sharded by key**, with headroom.
> Sharding is trivial here because keys are independent — there is never a cross-shard question.
>
> **The latency decision, which I would raise explicitly.** Half a millisecond on every request is fine if the
> API's p50 is twenty milliseconds — two and a half percent. **If the API's p50 were two milliseconds it would
> be a twenty-five percent tax**, and then I would move to local buckets with a few seconds of synchronisation
> and accept a stated over-admission bound. **So I would ask for the service's latency before committing**,
> because it genuinely changes the design.
>
> **Failure: fail open with a local fallback, plus a circuit breaker on the limiter itself.** If Redis is
> unreachable, each gateway applies a generous local bucket. And if Redis is *slow* rather than down, I stop
> calling it after a few timeouts rather than adding the full timeout to every request — otherwise a degraded
> Redis exhausts the gateway's threads and takes down the whole API, which is the limiter causing the outage it
> exists to prevent.
>
> **The response: `429` with `Retry-After`**, and rate-limit headers on successful responses too so a
> well-behaved client can slow down before being rejected. **And the `Retry-After` value must be jittered**,
> or every client rejected in the same second comes back in the same second and I have built myself a
> thundering herd.
>
> **What I would monitor:** rejection rate per plan — a spike means either an attack or a limit set too low, and
> those look identical on a dashboard until you segment by client; limiter latency at p99; and Redis
> availability, because it is now on the path of every request.
>
> **And the thing I would leave for later:** dynamic limits that adapt to system load, so the global limit
> tightens automatically when the database is struggling. That is genuinely useful and it is a control loop
> with its own failure modes, and I would not put one in the first version."

---

## 9. Recall card

**Fixed window is the cheapest and allows 2× the limit at the boundary** — 100 at 10:00:59 and 100 at
10:01:00. **Sliding log is exact and costs a timestamp per request** (8 GB vs 32 MB at 1M keys, limit 1,000).
**Sliding window counter is the practical answer:** two counters, weight the previous window by the fraction
still in view, error under ~5%.

**Token bucket separates two numbers with two jobs** — rate `R` is the sustained limit, capacity `B` is how
much burst is forgiven — with **lazy refill** on access and `time.monotonic()`, never wall-clock. **Leaky
bucket eliminates bursts entirely**, at the cost of queueing latency.

**The distributed count is the hard half.** Shared Redis is exact and adds ~0.5 ms to *every* request; local
counters at limit/n are wrong because traffic is never even; **local-with-sync is what to use, and the answer
states the over-admission bound.**

**Decide the failure policy in advance: fail open with a generous local fallback**, plus a **circuit breaker on
the limiter itself** — a slow Redis that you wait for on every request is how the limiter causes the outage.

**Limit on several things at once** (account, IP for anonymous — crude because of NAT, endpoint via per-request
**cost**, and a **global** limit for the system itself), layer a crude limit at the edge, and return `429` with
a **jittered `Retry-After`** or you have built your own thundering herd.
