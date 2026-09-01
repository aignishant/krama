---
day: 157
track: system-design
title: "Design a chat system with presence"
phase: "High-level design case studies"
status: written
---

# Design a chat system with presence

## 1. What this is, and why they ask it

Yesterday you designed WhatsApp: **one-to-one messages, delivered and forgotten, end-to-end encrypted.**

Today is the other kind of chat — **Slack, Discord, Teams.** Persistent channels rather than conversations.
Message history that must survive forever and be searchable. Threads. And **presence** — who is online, who is
typing, who is away — which is the part this lesson is named for and the part that is genuinely surprising.

They ask it because **it inverts three of yesterday's decisions**, and the interviewer wants to see whether
you know why.

**History is kept, not deleted**, because a workspace's messages are a shared organisational record and
"scroll back to what was decided in March" is the product. **Which means server-side storage grows forever and
search becomes a first-class system** rather than something encryption forbade.

**A channel has many members and no cap**, so a message in a busy channel fans out to thousands of connected
clients, and you are back to a fan-out problem WhatsApp's thousand-member limit had deleted.

**And presence, which people underestimate by two orders of magnitude.** Online status changes constantly, it
fans out to everyone who can see you, and **built naively it generates more traffic than the messages do.**
Computing that unprompted is the single strongest signal in this interview.

By the end of this lesson you can design channels and history, fan out to connected clients, build presence
and typing indicators that scale, add search and threads, and size all of it.

---

## 2. The story

The factory ran three shifts and the thing that held it together was a whiteboard by the door of the
supervisor's office.

**Not the machines. The whiteboard.**

Because the man coming on at six needed to know what had happened at four, and the man who had been there at
four was on a bus. **So he wrote it down.** Line six stopped twice. The compressor is making a noise. Do not
use the second forklift, the horn is gone.

And it worked, and over eleven years it grew four features, each because of a specific disaster.

**The first was that they stopped wiping it.** Somebody wiped the board on a Tuesday and on Friday there was
an argument about when exactly the compressor had first been reported, **and nobody could answer it.** After
that there was a register, and the board was only the last day of it.

**The second was that they split it.** One board became four columns — maintenance, dispatch, quality,
general — because a man from dispatch had to read forty lines about a bearing to find the one line that
concerned him.

**The third was Fatima.** She was in the office and had been there nineteen years, and if you asked her about
anything at all she could tell you which month it had been written in. **Nobody had ever called that a
system.** When she retired they discovered they had been leaning on her the whole time, and it took two years
to build something that did half of what she had done.

**And the fourth was the one that caused the most trouble for the least reason.**

Somebody put a second small board next to the first, with the names of the eleven supervisors and a magnet
against each one. **Present. In the plant. Gone home.**

It seemed helpful for about a month.

Then it became a full-time job, **because a magnet is only useful if it is correct**, and people moved and
forgot. So somebody had to walk round and update it. And when it was wrong, it was worse than nothing, because
people acted on it — they walked to the far end of the plant for a man whose magnet said he was there.

**They tried making everyone move their own magnet, and people forgot.**

What eventually worked was a rule that nobody planned: **the magnet was only trusted for the last hour.**
After that it went grey, and you telephoned instead of walking.

**The board stopped claiming to know things it did not know**, and the arguments stopped with it.

---

## 3. The idea in plain English

The whiteboard is a channel, the register is message history, Fatima is the search index, and the magnets are
presence — including the rule that made them work.

**Start with what differs from yesterday, because the transport is the same.**

```
                       WhatsApp                 Slack / Discord
  conversation shape   1:1 and small groups     channels, unbounded members
  history              deleted after delivery   kept forever, and searchable
  encryption           end-to-end               server-side (usually)
  fan-out per message  1-2 recipients           thousands of connected clients
  presence             last-seen, minimal       central to the product
```

**WebSockets and the connection registry are unchanged** — [day 156](../day-156-grid-dp/README.md) covers
them, and it is worth saying "the connection layer is the same as yesterday's" and moving on rather than
re-deriving it.

**Now the four things that are different.**

**One: messages are stored, and the storage model is the design.**

A channel is an ordered, append-only log of messages. **The access pattern is overwhelmingly "the last fifty
messages in this channel", plus occasional scrollback.**

**So partition by channel and sort by time within it.** In Cassandra terms, `channel_id` is the partition key
and `(timestamp, message_id)` is the clustering key — **which makes "the newest fifty" a single sequential read
from one partition.**

**And the message id should be a Snowflake**, so the id itself sorts by time and pagination is "everything
before this id" rather than an offset.

**The one thing that breaks this model is a channel that never stops growing.** A partition with ten million
messages is too large for most stores, so **bucket by time**: the partition key becomes `(channel_id, month)`.
Reads for recent messages hit one bucket; scrollback walks backwards through them.

**Two: fan-out to connected clients, which is a real problem again.**

A message in a channel with five thousand members, of whom eight hundred are currently connected, must reach
**eight hundred WebSockets spread across many connection servers.**

**Doing that with eight hundred registry lookups per message is the naive design**, and it works until it does
not. **The scalable version is a pub/sub bus**: every connection server subscribes to the channels its clients
care about, a message is published once to the channel's topic, and each server delivers to its own local
connections.

**One publish instead of eight hundred lookups**, and the fan-out cost moves from the sender's request to the
messaging bus, which is what it is for.

**And the offline members are a separate path entirely.** They do not get a push; **their unread state is
computed when they return**, from a per-user-per-channel `last_read_message_id`. **That single field is the
whole unread system**, and it is much cheaper than a per-user queue.

**Three: presence, which is the surprising part.**

**The naive design is: every client reports online, and every state change is pushed to everyone who could see
it.** In a ten-thousand-person workspace that is a change fanning out to ten thousand people, and people change
state constantly.

**The arithmetic kills it**, and it is worth doing out loud: **presence fan-out exceeds message fan-out by an
order of magnitude**, because state changes are far more frequent than messages and reach far more people.

**Four fixes, and they compose.**

**Push presence only to people who can currently see it.** Nobody needs your status while they are looking at a
different channel. **Subscribe to presence per visible view**, not per contact.

**Throttle.** Batch presence updates and flush every few seconds. **Nobody notices a three-second delay on a
green dot**, and it collapses a burst of changes into one message.

**Make it expiring rather than authoritative.** A heartbeat sets a key with a TTL; **absence of a heartbeat is
absence of presence.** No explicit "offline" event is needed, which matters because **a client that loses
network never sends one** — the same reason yesterday's connection registry needed a TTL, and it is the
whiteboard's grey magnet.

**And accept that it is approximate.** Presence is a hint. **A system that guarantees correct presence is
solving a much harder problem than the product needs**, and saying so is better than designing for it.

**Typing indicators are presence with a shorter fuse.** Same mechanism, a two-to-three second TTL, throttled
so a keystroke does not become a network message, and **never persisted** — a typing event that arrives late
is worse than one that is dropped.

**Four: search, which encryption made impossible yesterday and is now central.**

**Server-side search over an inverted index** — the structure from [day 135](../day-135-dependency-problems/README.md)
— with one enormous additional requirement: **permissions.** A search must return only messages in channels
the user can see, **and filtering after retrieval is wrong**, because a user could infer the existence of
private channels from result counts.

**So the permission filter goes into the query itself**: search within the set of channels this user is a
member of. **That set is small — a few hundred — and cacheable**, and it turns a permission problem into a
filter clause.

**And threads, briefly.** A thread is a message with a `parent_id`. **The design decision is whether thread
replies appear in the main channel**, and both answers exist in real products — Slack makes it optional per
message, which is a product decision rather than an architectural one.

---

## 4. The picture

The two shapes, side by side:

```
   WHATSAPP (yesterday)              SLACK (today)

   [Alice] <---> [Bob]               #engineering
                                       members: 5,000
   deliver, then DELETE                connected now: 800
   the phone is the archive            history: KEPT FOREVER, SEARCHABLE
   1-2 recipients per message          800 live deliveries per message
   E2E encrypted -> no search          server-side -> search is a feature
   presence = last seen                presence = core product surface
```

Fan-out by pub/sub instead of by lookup:

```
   NAIVE                              PUB/SUB

   message to #eng                    message to #eng
        |                                  |
   look up 800 members                publish once to topic "channel:eng"
   in the registry                         |
        |                             +----+----+----+
   800 lookups + 800 pushes           v    v    v    v
   from ONE server                  conn-1 conn-2 conn-3 conn-4
                                      |     |      |     |
   -> the sender's request           each delivers to ITS OWN
      does all the work              local connections

                                     ONE publish. The bus does the fan-out.
```

Storage layout, and why it is partitioned this way:

```
  PARTITION KEY   (channel_id, month)
  CLUSTERING KEY  (message_id DESC)      <- Snowflake: sorts by time

  channel:eng|2026-03  ->  [ msg 9912, msg 9911, msg 9910, ... ]
  channel:eng|2026-02  ->  [ msg 8801, msg 8800, ... ]
  channel:random|2026-03 -> [ ... ]

  "the last 50 in #eng"  = ONE sequential read from ONE partition
  "scroll back"          = walk backwards, month by month

  WHY BUCKET BY MONTH:
    a 5-year-old channel with 10M messages in one partition is
    too large for the store to handle well.
    Bucketing bounds every partition.
```

The presence arithmetic, which is the point of the lesson:

```
  10,000-person workspace, naive presence

  each person changes state ~30 times/hour
    (online, away, typing, stopped typing, back)
  = 300,000 events/hour

  each fanned out to everyone who could see them: 10,000
  = 3,000,000,000 pushes/hour = ~833,000 pushes/second

  MESSAGES in the same workspace:
    ~10,000 messages/hour x ~200 recipients = 2,000,000/hour = 555/s

  -> PRESENCE IS 1,500x THE MESSAGE TRAFFIC.

  Fixes, multiplied together:
    only to viewers of the same channel   x 1/500
    throttle to one update per 5 s        x 1/6
    -> ~280 pushes/second. Manageable.
```

Presence as an expiring key, which is the grey magnet:

```
  client heartbeat every 30 s:
      SET presence:<user> "online" EX 60

  reading presence:
      GET presence:<user>  ->  "online" or MISSING

  MISSING means offline. There is no "offline" event, and there
  must not be:
     a phone that loses signal NEVER sends one
     a browser tab that is force-quit NEVER sends one

  -> absence of a heartbeat IS the offline signal
  -> and the status is only ever trusted for its TTL,
     which is exactly what "the magnet goes grey after an hour" was
```

Unread state, which is one field and not a queue:

```
  WRONG: a per-user queue of unread messages
         5,000 members x every message = 5,000 rows per message

  RIGHT: last_read[user][channel] = message_id

         unread count = messages in the channel with id > last_read
                      = a range count on an already-sorted partition

  ONE row per user per channel, updated when they read.
  The unread COUNT is computed, not stored.

  (and for very busy channels, cache the count and invalidate on
   new messages, because the range count is not free)
```

Search with permissions in the query, not after it:

```
  WRONG:  search everything, then drop what the user cannot see
          -> result counts leak the existence of private channels
          -> "about 47 results" for a query that shows 3

  RIGHT:  channels = the user's memberships (a few hundred, cached)
          query: term AND channel_id IN (channels)

          the permission is a FILTER CLAUSE, evaluated by the index
          -> no leak, and it is faster
```

---

## 5. How it actually works

### Storing a message

```python
def post_message(user_id: int, channel_id: int, text: str,
                 client_id: str, parent_id: int | None = None) -> dict:
    if existing := message_store.by_client_id(user_id, client_id):
        return existing                       # idempotent retry

    message = message_store.insert(
        message_id=snowflake.next_id(),       # sorts by time
        bucket=f"{channel_id}|{month_of(time.time())}",
        channel_id=channel_id,
        parent_id=parent_id,
        author_id=user_id,
        text=text,
    )
    bus.publish(f"channel:{channel_id}", message)      # ONE publish
    queue.publish("index", message)                    # async search indexing
    return message
```

**`bus.publish` once, not one push per member** — that is the whole difference from a naive fan-out, and the
messaging bus is what turns eight hundred deliveries into one operation on the request path.

**The `client_id` check is the same idempotency as yesterday**, and for the same reason: a retry after a lost
acknowledgement must not create a second message.

### Delivery on the connection servers

```python
class ConnectionServer:
    def __init__(self) -> None:
        self.local: dict[int, set[Connection]] = {}     # channel -> connections

    def on_subscribe(self, conn: Connection, channel_id: int) -> None:
        if channel_id not in self.local:
            bus.subscribe(f"channel:{channel_id}", self.on_bus_message)
        self.local.setdefault(channel_id, set()).add(conn)

    def on_bus_message(self, channel_id: int, message: dict) -> None:
        for conn in self.local.get(channel_id, ()):
            conn.send(message)                # local, in-process, no lookups
```

**Each server subscribes once per channel it holds clients for, regardless of how many.** A server with two
hundred clients in `#general` has one subscription, and delivery is an in-process loop.

**The `if channel_id not in self.local` guard matters**: subscribing per connection instead of per channel
multiplies the bus's work by the number of clients, which is exactly what you were avoiding.

### Reading history

```python
def get_history(channel_id: int, before: int | None, limit: int = 50) -> list[dict]:
    results: list[dict] = []
    bucket_time = time.time() if before is None else timestamp_of(before)
    while len(results) < limit:
        bucket = f"{channel_id}|{month_of(bucket_time)}"
        page = message_store.read(bucket, before=before, limit=limit - len(results))
        results.extend(page)
        if not page:
            bucket_time -= 30 * 86400         # step back a month
            if too_old(bucket_time):
                break
        else:
            before = page[-1]["message_id"]
    return results
```

**The loop over buckets is the cost of bucketing**, and it is worth showing: a quiet channel may need several
buckets to fill fifty messages, while a busy one fills from the first.

**`before` as a message id rather than an offset** is cursor pagination — stable when new messages arrive
between pages.

### Presence

```python
HEARTBEAT_TTL = 60

def heartbeat(user_id: int, status: str = "online") -> None:
    redis.set(f"presence:{user_id}", status, ex=HEARTBEAT_TTL)

def get_presence(user_ids: list[int]) -> dict[int, str]:
    keys = [f"presence:{u}" for u in user_ids]
    values = redis.mget(keys)                 # ONE round trip for the whole list
    return {u: (v or "offline") for u, v in zip(user_ids, values)}
```

**There is no `set_offline`.** The TTL is the offline signal, **because a client that loses network never
sends a disconnect** — and a design that waits for one will show people online for hours after they have gone.

**`mget` for the whole member list in one round trip** matters, because rendering a channel's member sidebar
asks for hundreds of statuses at once.

### Presence fan-out, throttled and scoped

```python
class PresenceBroadcaster:
    def __init__(self, interval: float = 5.0) -> None:
        self.pending: dict[int, str] = {}
        self.interval = interval

    def changed(self, user_id: int, status: str) -> None:
        self.pending[user_id] = status        # coalesce: last write wins

    def flush(self) -> None:                  # called every `interval` seconds
        if not self.pending:
            return
        batch, self.pending = self.pending, {}
        for channel_id in channels_containing(batch.keys()):
            bus.publish(f"presence:{channel_id}",
                        {u: s for u, s in batch.items()
                         if u in members_of(channel_id)})
```

**Two mechanisms doing two jobs.** **Coalescing** means a user who toggles four times in five seconds
generates one update. **Scoping to channels** means the update reaches people currently viewing a channel that
person is in, not everyone in the workspace.

**Together those are the difference between 833,000 pushes a second and about 280.**

### Typing indicators

```python
def typing(user_id: int, channel_id: int) -> None:
    key = f"typing:{channel_id}:{user_id}"
    if redis.set(key, "1", nx=True, ex=3):    # nx: only the FIRST keystroke
        bus.publish(f"typing:{channel_id}", {"user": user_id})
```

**`nx=True` is the throttle**, and it is elegant: the first keystroke sets the key and publishes; every
keystroke for the next three seconds finds the key present and publishes nothing. **The client shows the
indicator for three seconds and lets it lapse.**

**Never persisted.** A typing event that arrives after the message did is noise, and there is nothing to
recover.

### Unread counts

```python
def mark_read(user_id: int, channel_id: int, message_id: int) -> None:
    read_store.upsert(user_id, channel_id, message_id)

def unread_counts(user_id: int) -> dict[int, int]:
    marks = read_store.all_for(user_id)                  # a few hundred rows
    latest = channel_store.latest_message_ids(marks.keys())   # cached
    return {c: count_between(c, marks[c], latest[c]) for c in marks
            if latest[c] > marks[c]}
```

**One row per user per channel**, and the count is computed rather than stored. **A per-user queue would mean
five thousand rows written per message in a five-thousand-member channel** — the thing the design exists to
avoid.

**`count_between` should be cached for busy channels**, because a range count on a large partition is not free
and the answer changes on every message.

### Search with permissions

```python
def search(user_id: int, query: str, limit: int = 20) -> list[dict]:
    channels = membership_cache.get(user_id)             # a few hundred ids
    if not channels:
        return []
    return search_index.query(
        text=query,
        filters={"channel_id": channels},                # IN the query, not after
        sort="relevance",
        limit=limit,
    )
```

**The membership filter is part of the query.** **Filtering after retrieval leaks information** — a total
result count that does not match the visible results tells the user how many private messages matched, which
is a genuine data leak in a workplace product.

### The real systems

```
Slack            channels in MySQL sharded by workspace, search in Solr;
                 famously one shard per workspace early on
Discord          Cassandra then ScyllaDB, bucketed by channel+time —
                 they published the migration in detail
Elasticsearch    the usual search index for this shape
Redis            presence, typing, and the connection registry
Kafka / NATS     the pub/sub bus for channel fan-out
```

**Discord's Cassandra bucketing is the specific reference for the storage model**, and naming it is a good
signal because the write-up is public and the problem — an unbounded partition per channel — is exactly the one
you have to solve.

---

## 6. The numbers

**Scale.**

```
10,000,000 daily active users
2,000,000 concurrent
average 50 channels per user, ~200 members per channel

messages:  ~50/user/day  -> 500,000,000/day = ~5,800/second
                                              peak ~20,000/second
```

**Message fan-out.**

```
5,800 messages/s x ~40 connected members per channel on average
= ~230,000 live deliveries/second

via pub/sub: 5,800 publishes/second, and each connection server
delivers locally to its own clients
-> the sender's request does ONE publish, not 40 lookups
```

**Presence, computed naively — the number that matters.**

```
2,000,000 concurrent users
each changes state ~30 times/hour     = 60,000,000 events/hour
                                      = ~16,700 events/second

naive fan-out, to everyone sharing any channel with them (~1,000 people):
  16,700 x 1,000 = 16,700,000 pushes/second

against 230,000/second for MESSAGES.

-> presence is ~70x the message traffic, built naively.
```

**With the two mitigations:**

```
START:  16,700 state changes/second

FIX 1 — SCOPE: push only to people currently VIEWING a channel that
        person is in, which is ~20 people rather than ~1,000.

  16,700 x 20 = 334,000 pushes/second       (50x better)

FIX 2 — THROTTLE: coalesce each user's changes into one update per
        5-second window, last write wins.

  16,700 events/s x 5 s = 83,500 events per window
  but they come from far fewer distinct users, because a user who
  toggles several times in 5 seconds collapses to one update:
  ~5,000 distinct users per window

  5,000 updates / 5 s = 1,000 flushes/second
  1,000 x 20 viewers  = 20,000 pushes/second   (another 17x)

-> ~20,000/second, from 16,700,000. An order of magnitude BELOW
   the message traffic, which is where presence belongs.
```

**Storage.**

```
500,000,000 messages/day x 500 bytes (text + metadata)
  = 250 GB/day
  x 365                         = 91 TB/year
  x 3 replicas                  = 273 TB/year

kept forever, so this accumulates. Ten years = 2.7 PB.

compare WhatsApp: a few TB total, because it deletes.
-> keeping history costs three orders of magnitude more storage.
```

**The search index.**

```
500,000,000 messages/day x ~15 terms x 8 bytes
  = 60 GB/day of postings
  x 90 days hot                 = 5.4 TB hot index
  older: cold shards, queried rarely

Elasticsearch wants the hot index largely in memory
-> ~50-100 machines with 64 GB each for the hot tier
```

**Partition sizing, which is why bucketing exists.**

```
a busy channel: 1,000 messages/day
  over 5 years = 1,825,000 messages x 500 B = ~900 MB in ONE partition

Cassandra guidance: keep partitions under ~100 MB
-> a single-partition-per-channel design fails on exactly the
   channels you care most about

bucketed by month:
  1,000 x 30 = 30,000 messages x 500 B = 15 MB per partition
-> comfortable, and reads for recent messages touch one bucket
```

**Unread counts, and why they are cached.**

```
2,000,000 concurrent users x 50 channels = 100,000,000 unread counts
recomputed on every message in every channel

a range count on a partition: ~1 ms
naive: every message invalidates ~200 members' counts
  5,800 messages/s x 200 = 1,160,000 recomputes/second at 1 ms
  = 1,160 cores doing nothing but counting

cached per (user, channel), invalidated on new messages, and
computed lazily when the client asks:
  -> only for channels the user actually looks at, ~5 per session
  -> ~10,000 computations/second. Fine.
```

**Latency budget.**

```
post message -> persisted            ~5 ms
publish to the bus                   ~2 ms
bus -> connection server             ~3 ms
server -> client WebSocket           ~30 ms
                                     -------
                                     ~40 ms

history read (one partition, 50 rows)  ~10 ms
search (hot index)                     ~100 ms
presence lookup (mget of 200)          ~2 ms
```

**Cost, roughly:**

```
connection tier (2M connections)     ~50 machines      ~$50,000/month
message store (273 TB/year, growing) ~100 machines     ~$150,000/month
search (5.4 TB hot + cold)           ~80 machines      ~$120,000/month
pub/sub bus                          ~20 machines      ~$25,000/month
presence (Redis)                     ~10 machines      ~$10,000/month
                                                       ----------------
                                                       ~$355,000/month

for 10M DAU = ~$0.035/user/month
-> which is why this is a paid product and WhatsApp could be free.
```

---

## 7. The trade-offs

**Keeping history against deleting it.** Keeping it is the product — a workspace's messages are an
organisational record, and scrollback and search are why people pay. **It costs three orders of magnitude more
storage than WhatsApp's model, makes search a first-class system, and creates a compliance surface**: an
archive that exists can be subpoenaed, exported, and retained under legal hold. **That is a feature for an
enterprise product and a liability for a consumer one**, which is exactly why the two products chose
differently.

**Server-side encryption against end-to-end.** Server-side makes search, moderation, compliance export and
multi-device trivial. **End-to-end would break all four**, and for a workplace product where the employer owns
the data, the privacy argument for E2E is much weaker. **Say which you are building and why, because it is a
product decision, not a technical one.**

**Pub/sub fan-out against direct lookups.** Direct is simple, obvious, and puts `O(members)` work on the
sender's request. **Pub/sub is one publish and moves the fan-out to a bus built for it** — at the cost of an
extra system, extra latency of a few milliseconds, and **a harder failure story**: a bus partition means
messages are stored but not delivered live, and clients must reconcile on reconnect.

**Presence accuracy against presence cost.** Naive, correct presence is seventy times the message traffic.
**Scoped and throttled presence is approximate, delayed by seconds, and affordable.** The product does not need
accuracy — **nobody makes a decision based on a green dot being three seconds stale** — and a system that
guarantees it is solving a much harder problem than the product asked for.

**Expiring presence against explicit offline events.** Expiry is the only design that survives reality:
**clients that crash, lose network or are force-quit never send a disconnect.** The cost is that presence lags
by up to the TTL, so someone who closed their laptop shows online for a minute. **Shortening the TTL fixes the
lag and multiplies the heartbeat traffic**, so the TTL is the dial between those two.

**Computed unread counts against stored ones.** Computing from `last_read_message_id` is one row per user per
channel and no write amplification. **Storing a per-user unread queue would mean thousands of writes per
message** in a large channel. The cost is that the count must be computed on demand and cached, **and cache
invalidation on every message in a busy channel is itself a load** — mitigated by computing lazily, only for
channels the user actually opens.

**When would I not build this?** **When the chat is a feature, not the product** — support chat, a comment
thread, a game lobby — where the message volume is low and a database table with polling is genuinely enough.
**When a hosted service fits**: Stream, Sendbird and Twilio Conversations do all of this, and below a few
hundred thousand users they cost less than the connection tier alone. **And presence specifically is worth
questioning** — it is the most expensive feature per unit of user value in the whole system, and plenty of
successful products do without it.

---

## 8. In the interview

### How it gets asked

- *"Design Slack."* or *"Design a group chat system."* — the standard prompt.
- *"How do you show who is online?"* — the presence question, and the one with a surprising answer.
- *"A message is posted in a channel with five thousand members. What happens?"*
- *"How do you store message history?"* — the partitioning question.
- *"How does search work, and how do you handle permissions?"*
- *"How do unread badges work?"*

### The first ninety seconds

> "This is the other kind of chat, and I want to contrast it with a WhatsApp-style design in three points,
> because the differences are what make it interesting.
>
> **History is kept, not deleted.** A workspace's messages are an organisational record and scrollback is the
> product. **That means server-side storage grows forever — about ninety terabytes a year at ten million
> users, against a few terabytes total for WhatsApp — and search becomes a first-class system.**
>
> **Channels have unbounded membership**, so a message fans out to hundreds or thousands of connected clients.
> WhatsApp's thousand-member cap deleted that problem; here it is back.
>
> **And presence is central to the product**, which is the part I would spend time on, because it is
> surprisingly expensive.
>
> **The transport is the same as yesterday** — WebSockets, a connection registry with a heartbeat TTL — so I
> would not re-derive it.
>
> **Storage: partition by channel and time bucket, sorted by message id.** `(channel_id, month)` as the
> partition key and a Snowflake message id as the clustering key, **so 'the last fifty in this channel' is one
> sequential read from one partition.** The month bucket exists because a five-year-old busy channel would
> otherwise be a nine-hundred-megabyte partition, which most stores handle badly.
>
> **Fan-out: a pub/sub bus, not per-member lookups.** Each connection server subscribes once per channel it
> holds clients for; a message is published once; each server delivers to its own local connections. **One
> publish instead of eight hundred registry lookups on the sender's request.**
>
> **Unread state is one field, not a queue:** `last_read_message_id` per user per channel, and the count is
> computed. **A per-user unread queue would mean thousands of writes per message in a large channel.**
>
> **Now presence, and I want to do the arithmetic because it decides the design.** Two million concurrent
> users changing state about thirty times an hour is roughly seventeen thousand events a second. **Fanned out
> naively to everyone sharing a channel — say a thousand people — that is seventeen million pushes a second,
> against two hundred and thirty thousand for actual messages.** **Presence is seventy times the message
> traffic if you build it the obvious way.**
>
> **So it has to be scoped and throttled**, and I would design that in rather than discover it."

### The follow-ups

**"How do you show who is online?"**

> "Three design decisions, and the first is arithmetic rather than architecture.
>
> **Presence built naively is more traffic than the messages.** Two million concurrent users change state —
> online, away, typing, back — about thirty times an hour, which is seventeen thousand events a second.
> **Fanned out to everyone who shares a channel with them, roughly a thousand people, that is seventeen
> million pushes a second.** Messages are two hundred and thirty thousand. **Seventy times.**
>
> **So: scope it.** Presence goes only to people **currently viewing** a channel that person is in — about
> twenty people, not a thousand. **Nobody needs your status while they are looking at a different channel**,
> and the client subscribes to presence per visible view rather than per contact.
>
> **Then throttle it.** Coalesce changes in a five-second window and flush once — last write wins. **A user
> who toggles four times generates one update**, and nobody perceives a three-second delay on a green dot.
> **Together those take it to about twenty thousand pushes a second**, which is an order of magnitude below
> the message traffic, where it belongs.
>
> **The second decision is that presence must be an expiring key, not an explicit state.** A heartbeat every
> thirty seconds sets a Redis key with a sixty-second TTL, **and absence of the key means offline.**
>
> **There must be no 'set offline' call**, because the cases that matter never send one: a laptop that closes,
> a phone that loses signal, a browser tab that is force-quit. **A design waiting for a disconnect shows people
> online for hours after they have gone**, which is worse than showing nothing.
>
> **The TTL is the dial**: shorter means presence is fresher and heartbeats are more frequent.
>
> **The third decision is to accept that it is approximate**, and say so. **Presence is a hint, not a fact.**
> Someone shows online for up to a minute after closing their laptop, and that is fine — nobody makes a
> decision based on a green dot. **A system that guaranteed correct presence would be solving a much harder
> problem than the product needs**, and I would rather spend that effort on message delivery.
>
> **Typing indicators are the same mechanism with a three-second TTL**, and there is a neat throttle: **set the
> key with `NX`, and only publish if the set succeeded.** The first keystroke publishes; every keystroke for
> the next three seconds finds the key present and publishes nothing. **And typing is never persisted** — a
> typing event that arrives after the message is noise."

**"A message is posted in a channel with five thousand members. Walk me through it."**

> "The naive path is what I would rule out first, because it is what people write.
>
> **Naively: look up all five thousand members in the connection registry, find the eight hundred who are
> online, and push to each.** That is eight hundred lookups and eight hundred pushes **on the sender's
> request**, and it scales with membership rather than with anything you control.
>
> **What I would build is a pub/sub bus.** Every connection server subscribes to `channel:<id>` **once, for as
> long as it holds any client interested in that channel** — not once per client, which is the mistake that
> multiplies the bus's work by the number of connections.
>
> **The message is published once.** The bus delivers it to the handful of connection servers that subscribed,
> and each one loops over its own local connections in process. **One publish on the request path; the fan-out
> happens on a system built for fan-out.**
>
> **The offline members are a completely separate path, and I would not queue anything for them.** Their unread
> state comes from `last_read_message_id`, which is one row per user per channel. **When they come back, the
> unread count is a range count over an already-sorted partition** — messages newer than their mark.
>
> **A per-user queue would mean five thousand rows written per message**, which is the write amplification the
> design exists to avoid.
>
> **Three details I would add.**
>
> **The message is persisted before it is published**, so a bus failure means it is undelivered rather than
> lost, and clients reconcile on reconnect by asking for everything after their last received id.
>
> **Search indexing is asynchronous** — a separate queue — so a slow index cannot slow down posting.
>
> **And unread counts are computed lazily, not eagerly.** Recomputing two hundred members' badges on every
> message would be over a million recomputations a second across the system. **Computing them when a client
> actually asks means about five per user session**, which is thousands rather than millions."

**"How does search work, and how do you handle permissions?"**

> "An inverted index, asynchronously populated — and **the permissions part is the half that is actually
> interesting**, because getting it wrong is a data leak rather than a bug.
>
> **The index maps each term to the message ids containing it**, in Elasticsearch or similar. Every message is
> written to it from a queue, so indexing is near-real-time — a message is searchable within seconds. **Making
> it synchronous would put the index on the posting path and mean a message fails when search is slow**, which
> is a much worse property.
>
> **Sharded by time**, because almost all searches are about recent messages: a hot index over the last ninety
> days largely in memory, and cold shards for history.
>
> **Now permissions.** A user must only see results from channels they are a member of. **The wrong design is
> to search everything and filter the results afterwards.**
>
> **And it is wrong for a specific, non-obvious reason: result counts leak.** If I search and the system says
> 'about forty-seven results' while showing me three, **I have just learned that forty-four messages I cannot
> see match my query** — which tells me private channels exist, roughly how active they are, and that they
> discuss my search term. **In a workplace product that is a real leak**, and it has been a real incident at
> real companies.
>
> **The right design puts the permission in the query.** Fetch the user's channel memberships — a few hundred
> ids, cached — and add `channel_id IN (...)` as a filter clause. **The index evaluates it, so the counts are
> correct and nothing about invisible channels is observable.** It is also faster, because the filter prunes
> before ranking.
>
> **Two more things.** **Membership changes must invalidate the cache**, or someone removed from a channel keeps
> searching it. **And deleted messages must be removed from the index**, not just flagged — a search index is
> exactly where deleted content survives longest, and 'deleted' meaning 'still findable by search' is the kind
> of thing that ends up in a news article."

### The model answer

*"Design a team chat product: ten million daily users across many workspaces, channels of up to fifty thousand
members, full history, search, and presence."*

> "Two things in that prompt shape the design: **full history, which inverts the storage model, and fifty
> thousand-member channels, which is a genuine fan-out problem.** And presence, which I will come to last
> because it is where the surprising number is.
>
> **Sizing.** Ten million daily users, two million concurrent, about fifty messages each per day —
> **five hundred million messages a day, roughly 5,800 a second, twenty thousand at peak.**
>
> **Transport: WebSockets with a connection registry in Redis, heartbeat-refreshed TTL.** Same as any push
> system; I would not spend time re-deriving it.
>
> **Storage: partition by `(channel_id, month)`, cluster by Snowflake message id descending.** 'The last fifty'
> is one sequential read from one partition. **The month bucket is not optional** — a busy channel over five
> years is about nine hundred megabytes in a single partition, and Cassandra-family stores want partitions
> under a hundred. **Bucketing bounds every partition at around fifteen megabytes.** Discord published exactly
> this migration, which is the reference.
>
> **Ninety terabytes a year, tripled for replicas, kept forever.** That is the cost of history, and it is three
> orders of magnitude more than a delete-on-delivery design. **I would raise the compliance consequence at the
> same time: an archive that exists can be subpoenaed and must support legal hold and export** — which for an
> enterprise product is a feature rather than a cost.
>
> **Fan-out: a pub/sub bus.** Connection servers subscribe once per channel they hold clients for; a message is
> one publish. **At fifty thousand members with maybe eight thousand connected, the alternative is eight
> thousand registry lookups on the sender's request**, which is unacceptable at twenty thousand messages a
> second.
>
> **And for very large channels I would add one thing: a rate limit on posting.** A fifty-thousand-member
> channel where anyone can post at will is a fan-out amplifier, and **most products end up making huge channels
> announcement-only** — a product constraint doing an architecture's job, like WhatsApp's group cap.
>
> **Unread: `last_read_message_id` per user per channel, counts computed lazily and cached.** Eager
> recomputation would be over a million range counts a second across the system; lazy is about ten thousand.
>
> **Search: an inverted index, asynchronously populated, sharded by time, with the user's channel memberships
> as a filter clause in the query.** **Not a post-filter** — result counts would leak the existence and
> activity of private channels, which is a real data-leak class in workplace products.
>
> **Now presence, and I want to do the arithmetic because it is the part people get wrong by two orders of
> magnitude.**
>
> **Two million concurrent users changing state thirty times an hour is seventeen thousand events a second.
> Fanned out to everyone sharing a channel — a thousand people — that is seventeen million pushes a second,
> against two hundred and thirty thousand for actual messages.** Seventy times the message traffic, for a green
> dot.
>
> **Three fixes.** **Scope**: push only to people currently viewing a channel that person is in — about twenty,
> not a thousand. **Throttle**: coalesce into one update per five seconds. **Together, about twenty thousand
> pushes a second**, which is where it belongs.
>
> **And presence must be an expiring key with no explicit offline event**, because laptops close and phones
> lose signal and neither sends a disconnect. **Absence of a heartbeat is the offline signal.**
>
> **I would state plainly that presence is approximate** — up to a minute stale — **and that this is correct
> rather than a limitation.** Nobody makes a decision based on a green dot, and guaranteeing accuracy would
> cost more than message delivery does.
>
> **Two risks I would flag.** **Deploys disconnect everyone a connection server holds**, so clients need
> exponential backoff with jitter and deploys need to drain slowly, or the release is a self-inflicted
> thundering herd. **And a bus partition means messages are stored but not delivered live** — so clients must
> reconcile on reconnect by requesting everything after their last received id, and that reconciliation path
> has to be tested, because it only runs during incidents."

---

## 9. Recall card

**Inverts three WhatsApp decisions: history is kept forever (≈91 TB/year vs a few TB), channels have unbounded
membership, and encryption is server-side — which makes search possible and makes it a first-class system.**
The WebSocket transport is unchanged; say so and move on.

**Storage: partition by `(channel_id, month)`, cluster by Snowflake id.** "The last fifty" is one sequential
read. **The month bucket is required** — a busy channel over five years is ~900 MB in one partition against a
~100 MB guideline (Discord's published migration is the reference).

**Fan-out by pub/sub, not per-member lookups.** Each connection server subscribes **once per channel**, not per
client; one publish replaces hundreds of registry lookups on the sender's request. **Offline members get no
queue** — `last_read_message_id` is one row per user per channel and the unread count is **computed lazily and
cached** (eager recomputation is >1M range counts/second).

**Presence is the surprise: built naively it is ~70× the message traffic** — 17,000 events/s × ~1,000 viewers
= 17M pushes/s against 230,000 for messages. **Fix by scoping (only people currently viewing a shared channel,
~20 not 1,000) and throttling (coalesce to one update per 5 s)** → ~20,000/s.

**Presence must be an expiring key with NO explicit offline event** — closed laptops, lost signal and killed
tabs never send a disconnect. **Absence of a heartbeat is the offline signal**, and the TTL is the dial between
staleness and heartbeat traffic. **Typing = the same thing with a 3 s TTL and `SET NX` as the throttle**, never
persisted. **Presence is approximate by design, and that is correct.**

**Search permissions go IN the query as a `channel_id IN (...)` filter, never as a post-filter** — result
counts would leak the existence and activity of private channels.
