---
day: 152
track: system-design
title: "Design a notification system at scale"
phase: "High-level design case studies"
status: written
---

# Design a notification system at scale

## 1. What this is, and why they ask it

A notification system takes an event — someone liked your photo, your order shipped, your card was declined —
and gets a message to a person, through push, SMS, email or in-app, on whatever device they are using.

**It looks like the easiest design in the set and it is not.** The core loop is "receive event, look up user,
call a provider", and that fits in a page. Everything that makes it hard is around the edges, and every one of
those edges is asked about.

They ask it because it is the design where **third parties are on the critical path and you do not control
them.** Apple's push service, Google's, Twilio, SendGrid — all of them have their own rate limits, their own
outages, their own error codes, and their own opinions about what counts as abuse. **A design that assumes the
provider always works is not a design.**

And they ask it because of one property no other system in this course has: **a notification is visible to a
human, and sending it twice is a real, felt failure.** A duplicated database write is a bug; a duplicated
"your card was charged" push at three in the morning is a support ticket and a lost user. **The
exactly-once conversation from [day 122](../day-122-autocomplete/README.md) has real stakes here.**

The other half is that **the volume is enormous and mostly unwanted.** A social app sends billions of
notifications a day and most of them are ignored. **The interesting engineering is in not sending things** —
preferences, rate limits per user, batching, quiet hours — and a candidate who talks about deduplication and
throttling before talking about throughput is answering the real question.

By the end of this lesson you can design the pipeline, handle provider failures and retries, deduplicate
properly, respect preferences and quiet hours, fan out to a million recipients, and size the whole thing.

---

## 2. The story

The school had four hundred children and one way of telling anybody anything, which was Ganeshan.

He was the office assistant, and when something needed saying he wrote it in the diary of every child it
concerned and the parents signed it the next morning.

**And it worked, badly, for a very long time.**

The trouble was never the writing. It was everything else.

**Some parents wanted to know everything** — the fee reminder, the sports day, the change of bus timing, the
list of what to bring on Thursday. **Some wanted only the things that mattered**, and their definition of what
mattered was not the school's, and the only way to find out was to be told off.

Then there was Mrs Fernandes, who told him in September that she did not want to hear about the bus, ever, and
in January complained that nobody had told her the bus was cancelled. **He had the note she had written. It
did not help.**

There was the family with three children in the school, who got the same fee notice three times, once in each
diary, and the father came in and asked whether the school thought he could not read.

There was the evening the principal decided at nine at night that the next day was a holiday, **and Ganeshan
made forty phone calls before somebody's grandmother told him what she thought of people who telephone at ten
o'clock.**

And there was the sports day, when he wrote the notice in every diary in the school, four hundred of them, and
it took him from lunch until eight in the evening, **and by the time he finished the ones he had written at
lunch had already been read and the ones at the end arrived a day late.**

What eventually fixed it was not a better diary.

It was a list on the office wall that Ganeshan made himself, with four columns. **Who. What kind of thing.
How they want to hear it. When it is too late to tell them.** And a rule underneath, in his own writing, that
he followed for the next eleven years:

**"If it can wait until morning, it waits until morning. If it cannot, say so at the top."**

---

## 3. The idea in plain English

Ganeshan's four-column list is the notification system, and his rule at the bottom is the priority tier.

**The pipeline is five stages**, and each one exists because of a specific failure:

```
1. INGEST      an event arrives from some service
2. RESOLVE     who should be told, and how do they want to hear it
3. BUILD       render the message from a template
4. SEND        hand it to a provider
5. TRACK       delivered? opened? failed? bounced?
```

**Stage one: ingest, and the first decision is asynchronous.**

**A service that emits an event must not wait for the notification to be sent.** Checkout should not be slower
because SendGrid is slow, and checkout should certainly not fail because SendGrid is down. **So the event goes
onto a queue and the API returns immediately** — [day 129](../day-129-connected-components/README.md)'s
message queue, doing the job it exists for.

**And the queue is what makes retries possible at all**, because a failed send needs somewhere to live between
attempts.

**Stage two: resolve, and this is where most of the logic is.**

For each event, work out **who** to notify, and then for each person, **which channels**, and then **whether
to send at all.** That last one is the important one, and it has four separate gates:

- **Preferences.** Mrs Fernandes said no to bus notices. Per user, per notification type, per channel.
- **Quiet hours.** Not between 10pm and 8am **in the user's timezone**, which is the part people forget.
- **Rate limits.** No more than `N` notifications an hour to one person, whatever the events say. **This is
  the single most valuable feature in the system** and it is usually built last, after somebody's bug sends a
  user four hundred pushes.
- **Deduplication.** The same event processed twice must produce one notification.

**Stage three: build.** Render a template with the user's data, in the user's language. **Templates live in a
store and are versioned**, because marketing will change the wording and you need to know what was actually
sent.

**Stage four: send, and this is where the third parties live.**

```
push (iOS)      APNs        HTTP/2, certificate or token auth
push (Android)  FCM         also handles web push
SMS             Twilio, MSG91, AWS SNS
email           SendGrid, SES, Mailgun
in-app          your own websocket or a poll of your own store
```

**Each has different limits, different error codes, and different failure modes**, so each gets its own
worker pool and its own queue. **One shared pool is wrong**: an SMS provider timing out would consume every
worker and stop email too. **That is [day 126](../day-126-graph-representation/README.md)'s bulkhead**, and it
is the specific reason for the per-channel split.

**Stage five: track.** Providers report delivery asynchronously, by webhook. **A push can be accepted by APNs
and never arrive** — the phone is off, the app was uninstalled, the token is stale — and you only find out
later. **Feed that back**: a token that APNs reports as invalid must be deleted, or you send to it forever.

**Now the four things that are genuinely hard.**

**One: duplicates, and why they are worse here.** At-least-once delivery from the queue means an event can be
processed twice. Everywhere else that produces a duplicate row; **here it produces a second push notification
on someone's lock screen.**

**The fix is an idempotency key**, and the key must come from the event, not be generated during processing:
`hash(user_id, notification_type, event_id)`. Store it in Redis with a TTL, check before sending. **The check
and the send are not atomic**, so a crash between them can still duplicate — **which is why the key should also
be passed to the provider where the provider supports it**, since APNs deduplicates on
`apns-collapse-id`.

**Two: retries, and the trap in them.** A provider returns `503`. Retry with exponential backoff and jitter —
[day 125](../day-125-what-a-graph-is/README.md)'s reasoning exactly.

**But not all failures should be retried, and this is the distinction that matters.** A `429` means slow down
and retry. A `500` means retry. **A `400` — bad token, invalid number, unsubscribed address — must never be
retried**, because it will fail identically forever and each attempt costs money. **Retrying a permanent
failure is the most common way to burn a provider quota.**

**And a notification has a shelf life.** "Your ride is arriving" is worthless twenty minutes later. **Every
notification carries a TTL, and a message that expires in the queue is dropped rather than sent** — Ganeshan's
rule about the morning, made mechanical.

**Three: fan-out, which is Ganeshan's four hundred diaries.** A celebrity posts and ten million followers
should be told. **Doing that in one worker takes hours and the last person is told tomorrow.**

**So fan out in stages.** One event becomes a fan-out job; the job reads followers in batches of a thousand and
writes a message per batch onto the send queue; hundreds of workers drain that. **The key is that the fan-out
job and the send job are separate queue messages**, so the work is parallel and a crash loses one batch rather
than everything.

**And for very large fan-outs, do not send at all.** A hundred million followers means most of them do not
want it. **Filter by engagement first** — people who have opened a notification from this source in the last
thirty days — which typically cuts the volume by ninety percent and improves the open rate at the same time.

**Four: priority, because not everything is equal.** A one-time password must go now. A "someone liked your
photo" can wait five minutes and be batched with the next four likes.

**Separate queues per priority, not a priority field on one queue.** A single queue with priorities still lets
a million low-priority messages sit in front of the OTP if the consumer is not careful, and separate queues
with separate worker pools make the guarantee structural.

**And batching low-priority notifications is the highest-value optimisation in the system.** Five separate
"X liked your photo" pushes is worse than one "5 people liked your photo" — fewer notifications, better open
rate, less provider cost, happier user. **Three things improved at once, which is rare.**

---

## 4. The picture

The pipeline:

```
  services            +-------------+
  (order, social, ->  |  INGEST API |  returns 202 immediately
   payments)          +------+------+
                             |
                             v
                     +---------------+
                     | EVENT QUEUE   |  (Kafka / SQS)
                     +-------+-------+
                             |
                             v
                     +---------------+       +------------------+
                     |   RESOLVER    | <---> | user prefs,      |
                     |               |       | device tokens,   |
                     | - who?        |       | timezone         |
                     | - channels?   |       +------------------+
                     | - allowed?    |
                     | - duplicate?  | <---> [ dedup store, Redis ]
                     +-------+-------+
                             |
              +--------------+--------------+--------------+
              v              v              v              v
        [PUSH QUEUE]   [SMS QUEUE]   [EMAIL QUEUE]   [IN-APP QUEUE]
              |              |              |              |
         push workers   sms workers   email workers    ws / store
              |              |              |
              v              v              v
           APNs/FCM       Twilio        SendGrid
              |              |              |
              +--------------+--------------+
                             |
                             v
                    [ DELIVERY WEBHOOKS ] -> tracking, token cleanup

  ONE QUEUE AND POOL PER CHANNEL. A slow SMS provider must not be able
  to consume the workers that send email.
```

The four gates in the resolver, in order:

```
  event: "photo_liked", user 4471

  gate 1  PREFERENCES   does this user want photo_liked on push?
                        -> no  => STOP (cheapest possible exit)
  gate 2  DEDUP         have I already sent this exact notification?
                        -> yes => STOP
  gate 3  RATE LIMIT    has this user had > 10 pushes this hour?
                        -> yes => batch it for later, or STOP
  gate 4  QUIET HOURS   is it 02:00 in THEIR timezone?
                        -> yes => schedule for 08:00 local

  ORDER MATTERS: the cheapest and most-likely-to-stop checks first.
  Preferences reject the most and cost one cached lookup.
```

Retry classification, which is the part people get wrong:

```
  provider response          retry?     why
  ---------------------------------------------------------------
  200 OK                     no         done
  429 Too Many Requests      YES        back off, honour Retry-After
  500 / 503                  YES        transient, exponential + jitter
  timeout                    YES        but check for duplicates
  400 Bad Request            NO         malformed; will fail forever
  410 Gone (bad token)       NO         + DELETE THE TOKEN
  403 unsubscribed           NO         + record the preference

  Retrying a 4xx burns quota and money and never succeeds.
  Not retrying a 5xx loses a notification that would have worked.
```

Fan-out in two stages:

```
  celebrity posts
        |
        v
  +---------------+
  | FANOUT JOB    |   one message
  +-------+-------+
          |  reads followers in pages of 1,000
          v
  [ batch 1 ][ batch 2 ][ batch 3 ] ... [ batch 10,000 ]   10M followers
          |          |          |
      worker     worker     worker      ... hundreds in parallel
          |          |          |
          v          v          v
        APNs       APNs       FCM

  ONE worker doing 10M sequentially at 100/s = 27 hours.
  10,000 batches across 200 workers          = ~8 minutes.

  And filter FIRST: of 10M followers, maybe 1M have opened a
  notification from this source in 30 days. Send to those.
  -> 10x less cost, HIGHER open rate.
```

Batching, and why it improves three things at once:

```
  WITHOUT batching                 WITH a 5-minute window

  10:01 "A liked your photo"       10:05 "5 people liked your photo"
  10:02 "B liked your photo"
  10:03 "C liked your photo"       1 notification instead of 5
  10:04 "D liked your photo"       -> 80% less provider cost
  10:05 "E liked your photo"       -> higher open rate (less fatigue)
                                   -> user does not mute you

  5 interruptions -> 1.
  This is the highest-value feature in the system and it is
  almost always built last.
```

---

## 5. How it actually works

### Ingest, which returns immediately

```python
@app.post("/notify")
def notify(event: dict) -> tuple[dict, int]:
    event["event_id"] = event.get("event_id") or str(uuid.uuid4())
    event["received_at"] = time.time()
    queue.publish("events", event)            # does not wait for delivery
    return {"accepted": event["event_id"]}, 202
```

**`202 Accepted`, not `200 OK`**, and the distinction is real: you have accepted responsibility for trying, not
reported success. **The caller gets an event id it can use to query status later.**

**And the `event_id` must come from the caller when the caller has one**, because that is what makes the whole
pipeline idempotent — a retried API call with the same event id must not produce a second notification.

### The four gates

```python
def should_send(user_id: int, kind: str, channel: str, event_id: str) -> str:
    prefs = prefs_cache.get(user_id)
    if not prefs.wants(kind, channel):
        return "opted_out"                    # cheapest, rejects the most

    key = f"dedup:{user_id}:{kind}:{event_id}"
    if not redis.set(key, "1", nx=True, ex=86400):
        return "duplicate"                    # SET NX is atomic

    if rate_limiter.count(user_id, channel) >= prefs.hourly_cap:
        return "rate_limited"

    if in_quiet_hours(prefs.timezone) and kind not in URGENT:
        return "quiet_hours"

    return "send"
```

**`redis.set(..., nx=True)` is the deduplication**, and it is atomic — two workers processing the same event
concurrently cannot both get `True`. **A separate `GET` then `SET` would be a race**, and at a million events a
second that race fires constantly.

**The order is deliberate**: preferences first because they are a cached lookup and reject the most.

### Quiet hours, in the user's timezone

```python
from zoneinfo import ZoneInfo
from datetime import datetime

def in_quiet_hours(tz_name: str, start: int = 22, end: int = 8) -> bool:
    local_hour = datetime.now(ZoneInfo(tz_name)).hour
    return local_hour >= start or local_hour < end        # wraps midnight
```

**`local_hour >= start or local_hour < end` handles the wrap**, and writing it as `start <= h <= end` is the
bug: 22 to 8 never satisfies that, so quiet hours never trigger and nobody notices until a user in another
timezone complains.

**And storing the user's timezone is a real requirement.** A server-side "night" is meaningless when your users
span twelve zones.

### Sending, with retry classification

```python
PERMANENT = {400, 403, 404, 410, 422}

def send_with_retry(message, max_attempts: int = 5) -> str:
    for attempt in range(max_attempts):
        response = provider.send(message)
        if response.ok:
            return "sent"
        if response.status in PERMANENT:
            handle_permanent(message, response)      # delete token, record opt-out
            return "permanent_failure"               # NEVER retry
        delay = min(2 ** attempt, 60) + random.uniform(0, 1)   # backoff + jitter
        time.sleep(delay)
    dead_letter.publish(message)
    return "exhausted"
```

**The `PERMANENT` set is the important line.** A `410 Gone` from APNs means the device token is dead — the app
was uninstalled — and retrying it five times costs five API calls and will never work. **`handle_permanent`
deletes the token**, or you retry that user's dead token on every notification, forever.

**Jitter, not just backoff.** Without it, everything that failed during a provider outage retries at the same
instant when it recovers, and the recovery is immediately undone.

### The TTL, which prevents sending stale things

```python
def process(message) -> None:
    age = time.time() - message["created_at"]
    if age > message.get("ttl", 3600):
        metrics.increment("dropped_expired", tags={"kind": message["kind"]})
        return                                # do NOT send
    send_with_retry(message)
```

**A queue that backed up for two hours should not then deliver two hours of "your ride is arriving".** The TTL
is per notification type: an OTP is 5 minutes, a ride update is 10, a marketing message is a day.

**And `dropped_expired` must be a metric**, because a rising count is the earliest signal that the pipeline is
behind.

### Fan-out in two stages

```python
def handle_fanout(event: dict) -> None:
    cursor = None
    while True:
        followers, cursor = follower_store.page(event["author_id"], cursor, limit=1000)
        if not followers:
            break
        engaged = engagement_filter(followers, event["author_id"])   # cut ~90%
        queue.publish("send", {"recipients": engaged, "event": event})
        if cursor is None:
            break
```

**Each page becomes its own queue message**, so hundreds of workers drain them in parallel and a crash costs
one batch rather than the whole fan-out.

**`engagement_filter` is the highest-leverage line here**: of ten million followers, perhaps one million have
opened a notification from this author in the last month. **Sending to the other nine million costs money and
lowers the open rate**, which is the metric the product team actually cares about.

### Batching

```python
def maybe_batch(user_id: int, kind: str, payload: dict) -> None:
    if kind not in BATCHABLE:
        send_now(payload)
        return
    redis.rpush(f"batch:{user_id}:{kind}", json.dumps(payload))
    redis.expire(f"batch:{user_id}:{kind}", 600)
    scheduler.schedule_once(f"flush:{user_id}:{kind}", delay=300)   # 5-minute window
```

**`schedule_once` is the whole design** — the first item in a window starts a timer, and later items join the
existing batch rather than starting another. **Then one flush renders "5 people liked your photo".**

### The real systems

```
APNs (Apple)        HTTP/2, token auth, apns-collapse-id for dedup,
                    apns-priority 5 (batched) or 10 (immediate)
FCM (Google)        Android and web; also proxies to APNs for iOS
Twilio / MSG91      SMS; per-country rules, sender IDs, DLT in India
SendGrid / SES      email; reputation matters — bounces and complaints
                    get you blocked by the receiving mail servers
OneSignal, Braze,   full platforms: templating, scheduling, segmentation
Airship, Firebase   — usually cheaper than building this
```

**Email reputation is worth one sentence in the interview**, because it is a failure mode unique to that
channel: **sending to bad addresses damages your sending domain's reputation**, and once Gmail starts
classifying you as spam, your legitimate mail stops arriving too. **So bounce handling is not hygiene, it is
deliverability.**

---

## 6. The numbers

**Volume.**

```
100 million users
average 10 notifications per user per day

1,000,000,000 notifications/day
  / 86,400 s          = ~11,600/second average
  peak is ~5x average = ~58,000/second
```

**Split by channel, which is what decides the cost:**

```
push   80%   800,000,000/day     free (APNs and FCM cost nothing)
in-app 15%   150,000,000/day     your own storage
email   4%    40,000,000/day     ~$0.0001 each = $4,000/day
SMS     1%    10,000,000/day     ~$0.006 each  = $60,000/day
```

**SMS is one percent of the volume and eighty-eight percent of the cost.** That single line is the most useful
thing in this section, and it drives a real design decision: **prefer push, fall back to SMS only when push is
unavailable and the message is important.**

```
monthly: email $120,000 + SMS $1,800,000 = ~$1.9M/month
moving 20% of SMS to push saves ~$360,000/month
```

**Machines.**

```
58,000 sends/second at peak
one worker: ~500 sends/second (network-bound, mostly waiting)
-> 116 workers at peak

at ~50 workers per machine (async I/O)
-> ~3 machines for sending

resolver: 58,000/s x ~3 cache lookups each = 174,000 lookups/s
-> Redis at 100,000 ops/s per instance -> 2-3 instances
```

**Under ten machines for a billion notifications a day** — and, as with the crawler, the point is that the
bottleneck is not compute. **It is provider rate limits and money.**

**Storage.**

```
notification record: id, user, type, channel, status, timestamps, payload ref
  ~200 bytes

1,000,000,000/day x 200 B = 200 GB/day
  x 30 days retention     = 6 TB
  x 3 replicas            = 18 TB

-> keep 30 days hot for the in-app inbox and support queries,
   archive the rest to object storage at $0.023/GB
```

**Dedup store.**

```
1,000,000,000 keys/day, TTL 24 hours
key ~60 bytes + Redis overhead ~100 bytes = 160 bytes

1,000,000,000 x 160 B = 160 GB of Redis

-> that is expensive. Options:
   - shorter TTL (1 hour): 6.7 GB. Covers retry windows, misses
     a duplicate 3 hours later.
   - Bloom filter: ~1.2 GB at 1% false positive
     -> 1% of notifications silently NOT sent. Unacceptable here,
        unlike the crawler.
   - shard Redis by user id: 160 GB across 10 instances = 16 GB each.
```

**The contrast with the crawler is worth stating**: a Bloom filter's false positive was fine there and is not
fine here, **because silently dropping one percent of notifications includes one percent of OTPs.**

**Fan-out timing.**

```
celebrity with 10,000,000 followers

single worker at 500 sends/s   = 20,000 s = 5.5 hours
                                 (last follower notified tomorrow)

batched, 10,000 batches of 1,000, 200 workers
  each batch: 1,000 / 500 per second = 2 s
  10,000 batches / 200 workers = 50 rounds x 2 s = 100 seconds

with engagement filtering (10% engaged):
  1,000,000 recipients -> ~10 seconds
```

**Five and a half hours against ten seconds**, and most of that gain is the filter rather than the
parallelism.

**Batching's saving.**

```
a user gets 5 likes in 5 minutes

unbatched: 5 pushes
batched:   1 push

if 40% of all notifications are batchable social events,
and batching averages 4:1:

  400,000,000/day batchable -> 100,000,000/day sent
  -> 300,000,000 fewer notifications/day
  -> 30% less total volume, and a measurably higher open rate
```

**Provider rate limits, which are the real ceiling:**

```
APNs        no published hard limit, but connection-based;
            ~10,000/s per HTTP/2 connection, many connections allowed
FCM         ~600,000 messages/minute per project = 10,000/s
Twilio      1/second per number by default; short codes ~100/s
            -> 10,000,000 SMS/day needs ~116/s sustained
            -> you need short codes or many numbers, arranged in ADVANCE
```

**The Twilio line is the one that catches people.** One phone number sends one SMS a second — **86,400 a day**
— so ten million a day is not a scaling problem you can solve at runtime. **It is a procurement problem, and it
takes weeks.**

---

## 7. The trade-offs

**Synchronous against asynchronous ingest.** Asynchronous is right: the emitting service returns in
milliseconds and a provider outage does not break checkout. **The cost is that the caller cannot know whether
the notification arrived**, so "did my user get the OTP" becomes a separate status query rather than a return
value. **For OTPs specifically, some systems go synchronous** and accept the coupling, because the user is
staring at a screen waiting.

**At-least-once against at-most-once.** Queues give at-least-once, so duplicates happen and dedup is required.
**At-most-once would mean occasionally losing a notification**, which for a marketing message is fine and for
an OTP is not. **Different notification types genuinely want different guarantees**, and the honest design uses
at-least-once plus dedup everywhere rather than two pipelines.

**Dedup store size against dedup window.** A 24-hour window costs about 160 GB of Redis; an hour costs 6.7 GB
and misses a duplicate that arrives three hours later. **A Bloom filter is 1.2 GB and silently drops one
percent** — acceptable for a crawler, **not acceptable when one percent includes one percent of one-time
passwords.**

**Batching against latency.** Batching cuts volume by a third, raises open rates and saves money, and it means
a notification arrives up to five minutes late. **For social events that is invisible; for an OTP it is
useless.** So batching is per notification type, never global, and the type list is a product decision.

**Aggressive filtering against reach.** Sending only to engaged users cuts cost tenfold and raises the open
rate — **and it means people who would have engaged this time do not hear about it.** The filter is a model
and models are wrong. **A small holdout that always receives is worth keeping**, both to measure the filter and
to avoid a permanent silent exclusion.

**Building against buying.** OneSignal, Braze and Airship do all of this, including templating, segmentation,
scheduling and analytics. **Building your own is justified by volume — at a billion a day the per-message
pricing is real money — and by data residency requirements.** Below roughly ten million a day, buying is
almost always correct, and saying so is a better answer than designing enthusiastically.

**When would I not build this?** When the volume is low enough that a managed platform is cheaper than the
engineers. When notifications are transactional only — order confirmations, password resets — where a queue
and a provider SDK is genuinely the whole system and the preference machinery is over-engineering. **And when
what is actually wanted is in-app messaging**, which is a different product: it needs no providers, no tokens
and no quiet hours, because nothing interrupts anyone.

---

## 8. In the interview

### How it gets asked

- *"Design a notification system."* — usually with a scale like a billion a day.
- *"How do you make sure a user doesn't get the same notification twice?"*
- *"A push provider is down. What happens?"* — retry classification.
- *"A celebrity with ten million followers posts. Walk me through it."*
- *"How do you handle user preferences and quiet hours?"*
- *"What is your most expensive channel?"* — the SMS question.

### The first ninety seconds

> "Five stages — ingest, resolve, build, send, track — and I want to say up front that **the interesting
> engineering here is in not sending things**, because most notifications at scale are unwanted and the
> failure mode is a human being annoyed.
>
> **Ingest is asynchronous.** The emitting service puts an event on a queue and gets a `202` back immediately.
> **Checkout must not be slower because an email provider is slow, and must certainly not fail because it is
> down.** The queue is also what makes retries possible, because a failed send needs somewhere to live between
> attempts.
>
> **Resolve is where most of the logic lives, and it is four gates in a deliberate order.** Preferences first,
> because it is one cached lookup and it rejects the most. Then deduplication. Then a per-user rate limit —
> **no more than ten pushes an hour to one person, whatever the events say.** Then quiet hours, **in the
> user's timezone**, which is the part that gets forgotten.
>
> **Send is split by channel: one queue and one worker pool for push, one for SMS, one for email.** Not a
> shared pool — a slow SMS provider would otherwise consume every worker and stop email too. **That is a
> bulkhead, and it is the specific reason for the split.**
>
> **Track is a webhook back from the provider**, and the important part is the feedback loop: **when APNs
> reports a token as gone, delete it**, or you send to a dead token forever.
>
> **Now the number I would lead with, because it drives a real decision.** At a billion a day: push is eighty
> percent of volume and free; SMS is **one percent of volume and eighty-eight percent of the cost**, at about
> $60,000 a day. **So the design should prefer push and fall back to SMS only when push is unavailable and the
> message matters** — that is a bigger win than anything architectural.
>
> **And the second thing I would raise early: batching.** Five separate 'someone liked your photo' pushes
> should be one 'five people liked your photo'. **That cuts volume by about a third, costs less, and raises the
> open rate** — three things improved at once, which is rare, and it is almost always built last.
>
> **One question before I go further: what is the mix of transactional and marketing?** Because an OTP wants
> low latency and no batching, and a marketing push wants filtering and batching, and they barely share
> requirements beyond the transport."

### The follow-ups

**"How do you make sure a user doesn't get the same notification twice?"**

> "This matters more here than almost anywhere else, because **a duplicate is visible to a human.** A
> duplicated database row is a bug I fix on Monday; a second 'your card was charged' push at three in the
> morning is a support ticket and possibly a deleted app.
>
> **Where duplicates come from: the queue is at-least-once.** A worker takes a message, sends it, and crashes
> before acknowledging — the message is redelivered and sent again. That is not a bug in the queue; it is what
> at-least-once means.
>
> **The fix is an idempotency key that comes from the event, not from processing.** Something like a hash of
> user id, notification type and event id. **If I generate the key during processing, both attempts generate
> different keys and dedup does nothing** — which is the mistake worth naming.
>
> **Store it with `SET key value NX EX 86400` in Redis.** `NX` means set-if-absent and it is atomic, so two
> workers handling the same event concurrently cannot both get true. **A `GET` followed by a `SET` is a race**,
> and at fifty thousand a second that race fires constantly.
>
> **The gap I would admit to: the check and the send are not atomic.** If I set the key, then crash before
> sending, the notification is lost; if I send, then crash before setting, it duplicates. **I would set the key
> first — losing a notification is better than duplicating one** for most types, and for OTPs the user can
> request another.
>
> **And I would push the key down to the provider where it supports one.** APNs has `apns-collapse-id`, which
> makes it replace rather than add — so even if I do send twice, the phone shows one. **Defence at two layers,
> because the first one has a real hole.**
>
> **Sizing, since it is not free.** A billion keys a day at about 160 bytes with Redis overhead is 160 GB. **I
> would shard by user id across ten instances**, rather than shortening the TTL, and I would specifically not
> use a Bloom filter here — **a one percent false positive rate means silently not sending one percent of
> notifications, and that includes one percent of one-time passwords.**"

**"APNs starts returning errors. What happens?"**

> "It depends entirely on which error, and getting that classification right is the difference between a system
> that recovers and one that burns its quota.
>
> **Transient failures get retried with exponential backoff and jitter.** `500`, `503`, timeouts. Back off one
> second, two, four, up to a minute, with a random component — **without jitter, everything that failed during
> the outage retries at the same instant when it recovers and knocks it over again.**
>
> **`429` is a special transient case: honour the `Retry-After` header** rather than my own backoff, because
> the provider is telling me exactly what it wants.
>
> **Permanent failures must never be retried, and this is the one people get wrong.** A `400` for a malformed
> payload will fail identically forever. A `410 Gone` means the device token is dead — the app was uninstalled.
> **Retrying those costs five API calls, five times the quota, and succeeds zero times.**
>
> **And permanent failures need an action, not just an absence of retry.** A `410` must **delete the token from
> my store**, or I attempt that dead token on every future notification for that user, forever. A `403` for an
> unsubscribed email address must **record the preference**, because continuing to send damages my sending
> domain's reputation and eventually my legitimate mail stops arriving too.
>
> **After the retries are exhausted, the message goes to a dead letter queue** — not dropped silently — so I can
> see what failed and why.
>
> **Two more things for a full provider outage.** **A circuit breaker**: after enough consecutive failures,
> stop calling APNs and fail fast, so I do not have every worker blocked on a five-second timeout — otherwise
> a slow provider exhausts the pool and takes down the channels that are working. **And the TTL**: if APNs is
> down for two hours and then recovers, I should not deliver two hours of stale 'your ride is arriving'.
> **Every message carries a TTL and expired messages are dropped and counted**, and that counter is my earliest
> signal that the pipeline is behind."

**"A celebrity with ten million followers posts. Walk me through it."**

> "The naive version takes five and a half hours and the last follower hears about it tomorrow, so this needs
> two things: **parallelism, and — more importantly — sending to fewer people.**
>
> **First, the fan-out is two stages, not one.** The post event becomes a single fan-out job. That job pages
> through the follower list a thousand at a time, and **each page becomes its own message on the send queue.**
> Hundreds of workers drain that queue in parallel.
>
> **Two separate queue messages matters for a specific reason:** if it were one long-running job and the worker
> crashed at follower nine million, I would lose everything or resend everything. **With batches, a crash costs
> one batch of a thousand, and the retry is cheap and idempotent.**
>
> **The arithmetic.** One worker at five hundred sends a second is twenty thousand seconds — five and a half
> hours. Ten thousand batches across two hundred workers, two seconds each, is about a hundred seconds.
>
> **But the bigger win is not sending.** Of ten million followers, how many have opened a notification from
> this author in the last thirty days? **Realistically about a tenth.** Filtering to those cuts it to one
> million recipients — **about ten seconds, a tenth of the cost, and a higher open rate**, because the people
> who were going to ignore it were also the people slowly training themselves to ignore me.
>
> **Two things I would be careful about.** **The filter is a model and models are wrong**, so I would keep a
> small holdout that always receives, both to measure whether the filter is right and to make sure nobody is
> permanently and invisibly excluded.
>
> **And ordering: for a fan-out this large, some followers get it a minute after others.** For a social post
> that is fine. **If this were a live-event notification where fairness matters** — a ticket drop, say — I would
> have to say plainly that a ten-million fan-out cannot be simultaneous, and either randomise the batch order
> so the unfairness is not correlated with anything, or send a single broadcast through a topic-based channel
> instead of per-user messages."

### The model answer

*"Design the notification system for a ride-hailing app: driver assigned, driver arriving, trip complete,
payment receipt, plus promotions. Ten million rides a day."*

> "The thing that shapes this design is that **the notification types have wildly different requirements**, and
> treating them uniformly would be the main mistake. Let me separate them first.
>
> **'Driver arriving' is time-critical and worthless late** — a notification that arrives after the driver has
> gone is worse than nothing. **'Payment receipt' can be a minute late and nobody cares.** **Promotions should
> be batched, filtered, and never sent at 2am.** So: **three priority tiers with separate queues and separate
> worker pools**, not a priority field on one queue — because a million promotional messages must not be able
> to sit in front of a driver-arriving push.
>
> **Volume.** Ten million rides a day at roughly five notifications each is fifty million a day, about 580 a
> second average and maybe 3,000 at peak — which is small. **Compute is not the problem here.**
>
> **The problem is SMS.** Ride-hailing needs SMS because drivers and riders may not have the app in the
> foreground, and **SMS at six-tenths of a paisa each adds up fast**. If ten percent of those fifty million go
> by SMS, that is five million a day, about $30,000 a day. **So the design tries push first and falls back to
> SMS only when push fails or the device has no valid token** — and for 'driver arriving' specifically, I would
> pay for the SMS fallback, because a missed ride is worth more than the message.
>
> **And a procurement point I would raise early:** Twilio sends one SMS per second per number by default.
> **Five million a day is about sixty a second sustained, so this needs short codes or a pool of numbers,
> arranged weeks in advance.** That is not something you fix at runtime, and in India there is DLT
> registration on top.
>
> **The pipeline.** Ride services publish events to Kafka. A resolver consumes them, runs the four gates —
> preferences, dedup, rate limit, quiet hours — and routes to per-channel queues.
>
> **Quiet hours with an exception list, which this app needs specifically.** Promotions respect 10pm–8am in the
> rider's local timezone. **'Driver arriving' ignores quiet hours entirely**, because the user booked a ride at
> 2am and wants to know. **That exception list is a product decision I would want written down**, because
> getting it wrong in either direction is bad — waking people up, or silently not telling them their car is
> outside.
>
> **Deduplication with an event-derived key** — hash of user, type and ride id — in Redis with `SET NX`. At
> fifty million a day and a 24-hour TTL that is about 8 GB, which is one instance. **And `apns-collapse-id`
> passed through**, which does something genuinely useful here: **successive 'driver is 3 minutes away' /
> '2 minutes away' updates replace each other on the lock screen instead of stacking.**
>
> **TTLs per type, which matter more here than in most systems.** 'Driver arriving' expires in five minutes —
> **if the queue backs up, that message must be dropped, not delivered late**, because a stale arrival
> notification actively misleads. Receipts get a day. Promotions get a day.
>
> **Retry classification as usual**, with `410` deleting the token — and I would call out that **ride-hailing
> has unusually stale tokens**, because drivers reinstall the app constantly, so the cleanup loop is not
> optional hygiene.
>
> **What I would monitor:** delivery latency at p99 per type, with a tight alert on the driver-arriving tier;
> the expired-drop counter, which is my earliest warning that the pipeline is behind; SMS spend per hour,
> because a bug that flips push to SMS is expensive within minutes; and provider error rates split by
> permanent and transient.
>
> **And the honest closing point.** At fifty million a day, **a managed platform would probably be cheaper than
> the team required to run this** — the per-message pricing at this volume is not obviously worse than the
> engineers. **What would justify building it is the latency requirement on driver-arriving and the tight
> coupling to ride state**, and I would want that to be the stated reason rather than a default."

---

## 9. Recall card

**Five stages: ingest → resolve → build → send → track.** Ingest is **asynchronous with a `202`** so a provider
outage cannot break checkout. **One queue and worker pool per channel** — a bulkhead, so slow SMS cannot starve
email.

**Four gates in the resolver, cheapest first: preferences → dedup → rate limit → quiet hours (in the user's
timezone**, and `h >= 22 or h < 8`, not a range check**)**. The per-user hourly cap is the most valuable
feature and is always built last.

**Dedup with an event-derived key** — `hash(user, type, event_id)`, never generated during processing — via
Redis **`SET NX EX`** (atomic; `GET`-then-`SET` is a race). Set the key **before** sending, and pass
`apns-collapse-id` so the provider deduplicates too. **No Bloom filter here** — 1% silently unsent includes 1%
of OTPs.

**Retry classification is the thing people get wrong.** `429`/`5xx`/timeout → backoff **with jitter**;
`400`/`410`/`403` → **never retry, and act**: delete the dead token, record the opt-out. **Every message has a
TTL** and expired ones are dropped and counted — that counter is the earliest signal of a backed-up pipeline.

**Fan-out in two stages** (one fan-out job → per-1,000 batches as separate messages): 10M followers is 5.5
hours on one worker, ~100 s batched, **~10 s with engagement filtering** — and the filter, not the parallelism,
is most of the win. **Batching 5 likes into 1 push cuts volume ~30%, costs less, and raises open rates.**

**SMS is ~1% of volume and ~88% of cost** ($60k/day at 1B/day) — prefer push. **And one Twilio number sends
1 SMS/second**, so high volume is a procurement problem, not a runtime one.
