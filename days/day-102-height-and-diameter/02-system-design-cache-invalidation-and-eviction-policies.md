---
day: 102
track: system-design
title: "Cache invalidation and eviction policies"
phase: "Scaling fundamentals"
status: written
---

# Day 102 · System Design — Cache invalidation and eviction policies

**After today you can:** You can pick write-through, write-back or write-around and defend it.

**The interviewer asks it as:** *How do you keep the cache consistent with the database?*

---

## 1. What this is, and why they ask it

**Invalidation** is how a cached copy stops being served once the real value has changed. **Eviction** is
how a cache decides what to throw away when it is full. They are different problems and they are almost
always confused.

Three sentences. Invalidation is about **correctness** — the cache holds something that is now wrong —
and eviction is about **capacity**, where the cache holds something that is still right but which you
cannot afford to keep. Invalidation has three real mechanisms, and choosing between them is choosing how
stale you are willing to be. And there is one specific race between a read and a write that produces a
permanently wrong cache entry, which is the thing interviewers are actually testing.

They ask it because [yesterday's](../day-101-bfs-level-order/README.md) lesson made the cache sound free,
and this is the bill. The famous line — *there are only two hard things in computer science: cache
invalidation and naming things* — is a joke about a real problem: the moment there are two copies of a
value, something has to guarantee they agree, and nothing in the cache itself does. Say "I would add a
cache" without saying how it is invalidated and you have described half a design.

---

## 2. The story

The board outside Chandran's shop had the prices on it in chalk, and the board was the whole reason
people stopped there instead of walking another hundred metres to the market.

Tomato 40. Onion 30. Beans 60. Written big, readable from the road, so nobody had to get off their
scooter to ask.

The prices came from the wholesale market at four in the morning, and they moved. Not every day, but
often enough — a lorry did not arrive, or it rained in Kolar, and onions were 45 instead of 30.

There were three ways of handling that, and over about six years Chandran tried all three.

The first was to change the board the moment he unloaded. Four fifteen in the morning, before opening,
with a wet cloth and cold hands. That was correct and it was miserable, and on the days when nothing had
changed it was fifteen minutes of work for nothing.

The second was to not touch the board at all in the morning, and instead **wipe off any line whose price
had moved**. The board then said tomato and beans, and nothing about onions, and the first person to ask
for onions was told the price by Chandran and he chalked it back up then. Less work, and for the first
hour of the day some people had to actually ask.

The third was what he did on Sundays, when he was tired. He wiped the whole board at closing time and
wrote it fresh the next morning from scratch.

The thing that convinced him to settle on the second way happened in his fourth year and it was not
about work at all.

His nephew was helping. A customer asked for beans, the boy shouted the question inside, Chandran said
sixty, and the boy went to write it up. But in between the question and the chalk, Chandran had come out
and changed beans to seventy, because a new crate had come in at a higher rate.

The boy, who had been holding the old number in his head the whole time, then wrote sixty on the board.
Over the top of the seventy.

And there it stayed. Nobody wiped it, because nothing had changed since — the board was simply wrong, and
it stayed wrong until somebody happened to notice at about four in the afternoon.

Chandran's rule after that was that his nephew was allowed to **wipe** a line, and was never allowed to
**write** one from a number he had been holding for a while. If you have been carrying an old number
around, do not put it on the board. Rub it out and let the next person ask.

---

## 3. The idea in plain English

Chandran's three methods are the three cache-write strategies, and his nephew's mistake is the race
condition every interviewer asks about.

- The board is the **cache**; the crates and the wholesale rate are the **origin** — the database.
- Changing the board at four fifteen is **write-through**: update the cache when you update the truth.
- Wiping a line when the price moves is **write-around with invalidation**: update the truth, delete the
  cache entry, and let the next reader repopulate it.
- Wiping the whole board at closing time is a **TTL** — everything expires and is rebuilt.
- The boy writing a stale sixty over a fresh seventy is the **read-modify race**, and it produces a cache
  entry that is wrong *and not going to be corrected*.

### Invalidation: the three mechanisms

**One — TTL (time to live).** Every entry expires after `n` seconds. Nothing has to be tracked or
notified.

```
 + trivially simple, and self-healing: every bug in your invalidation logic
   is fixed within one TTL
 + no coordination between the writer and the cache at all
 - guaranteed staleness of up to the TTL
```

**A TTL is the seatbelt.** Even with perfect explicit invalidation, put one on every key — it bounds how
long any mistake can last.

**Two — explicit invalidation on write.** When the data changes, delete the key.

```
 + staleness is near zero
 - the writer must know every key derived from the data it just changed,
   which is the hard part
```

The difficulty is not the deleting. It is that one write can affect many keys: changing a product's price
invalidates the product page, the category listing, the search result, the user's cart total, and the
homepage banner. **Finding all of them is the actual work**, and the standard answer is to publish an
event and let each cache owner decide what to drop.

**Three — versioned keys.** Put a version in the key, and bump the version instead of deleting anything.

```
 product:987:v41    ->    product:987:v42
```

```
 + no delete, no race — a new version is simply a different key
 + old entries fall out by themselves under eviction
 - you must store the current version somewhere, and read it
 - the old entries occupy memory until evicted
```

This is genuinely useful when one change invalidates thousands of keys: bump a *namespace* version and
every key underneath it becomes unreachable in one operation.

### The write path: three strategies

| | What happens on a write | Staleness | Cost |
|---|---|---|---|
| **Write-through** | write DB **and** cache, synchronously | none | every write pays both; caches data nobody may read |
| **Write-around** | write DB, **delete** the cache key | one miss | the next read is slow |
| **Write-back** | write cache, flush to DB later | none to readers | **data loss if the cache dies** |

**Write-around is the default.** Say it that way: *"I write to the database and delete the cache entry.
The next read repopulates it."*

**Write-through** is right when a write is almost always followed immediately by a read of the same key —
a user editing their own profile, then being shown it. It wastes cache space on data nobody reads.

**Write-back** is fast and it can lose data, so it is only for values whose loss is tolerable: view
counts, last-seen timestamps, non-critical counters. Its real advantage is **collapsing writes** — a
video watched ten thousand times in a minute becomes one database write instead of ten thousand.

### Delete, do not update

This is the rule Chandran arrived at, and it is the single most useful thing in this lesson.

**On a write, delete the cache key. Do not write the new value into the cache.**

Why: writing the new value opens a window where a *concurrent reader* can overwrite it with an older
value. Deleting does not, because a deleted key produces a miss, and a miss re-reads the truth.

Here is the race, precisely. It is the interview question.

```
 A is a READER (cache miss). B is a WRITER.

 t1  A: cache GET x -> miss
 t2  A: DB read x   -> gets the OLD value, 60
 t3          B: DB write x = 70
 t4          B: cache DELETE x        (or SET x = 70)
 t5  A: cache SET x = 60              <- A writes its stale value LAST

 result: the cache holds 60. The database holds 70.
         Nothing will correct it — there is no further write.
         It is wrong until the TTL expires.
```

**A has been holding an old number in its head, and it writes it on the board last.** Exactly the nephew.

The mitigations, in the order you would state them:

1. **A TTL on every key.** Bounds the damage to the TTL. Always do this.
2. **Delete rather than set on write.** It does not eliminate the race above but it eliminates the much
   more common writer-versus-writer version of it.
3. **Delete twice** ("delayed double delete"): delete, write the database, then delete again after a
   short delay, so a reader that populated the cache in between is cleared.
4. **A per-key lock** on the miss path, so only one reader is ever fetching-and-setting a key.
5. **Compare-and-set with a version**, so a stale write cannot land on top of a newer one — the same
   mechanism as [day 095's](../day-095-n-queens/README.md) auction.

**Say the race, then say the TTL bounds it, then say the stronger options exist.** That sequence is the
answer.

### Eviction: a different problem

Invalidation removes entries that are **wrong**. Eviction removes entries that are **right but do not
fit**.

| Policy | Throws out | Good for | Bad at |
|---|---|---|---|
| **LRU** | least recently used | almost everything | one big scan wipes the cache |
| **LFU** | least frequently used | stable popularity | new items never build a count |
| **FIFO** | oldest inserted | nothing much | ignores usage entirely |
| **Random** | any entry | when memory is tight | unpredictable, but surprisingly decent |
| **TTL only** | expired entries | time-bounded data | does not respond to memory pressure |

**LRU is the default and it is right most of the time**, because recency predicts reuse. You implemented
it on [day 076](../day-076-lru-cache/README.md).

Its famous weakness is worth being able to name: **a single sequential scan of everything** — a nightly
report, an export, a crawler — touches every key once, evicts the entire working set, and leaves you with
a cache full of items nobody will ask for again. The hit rate collapses and stays collapsed until the
working set is faulted back in.

The fixes: **admission control** (do not put an item in the cache until it has been requested twice), or
**segmented LRU** (a small probationary area that new items must earn their way out of). Modern caches
use **W-TinyLFU**, which is an admission filter in front of an LRU — it is what Caffeine and several
CDNs use, and naming it is a strong signal.

### Redis's policies, which you will be asked about by name

```
 noeviction        refuse writes when full  <- the DEFAULT, and it surprises people
 allkeys-lru       evict any key, least recently used
 allkeys-lfu       evict any key, least frequently used
 allkeys-random
 volatile-lru      evict only keys that have a TTL set
 volatile-ttl      evict the key expiring soonest
 volatile-random
```

**`noeviction` is the default**, which means a Redis used as a cache without configuration will start
returning errors on writes when it fills up rather than making room. **If Redis is a cache, set
`allkeys-lru`. If Redis is a database, leave `noeviction`.** That one sentence is a genuinely useful
thing to say.

Also: Redis's LRU is **approximate** — it samples a handful of keys and evicts the least recently used
among them, rather than maintaining a true global ordering, because exact LRU would cost a linked-list
update on every access. Five samples gets you close to true LRU; the sample count is tunable.

---

## 4. The picture

The two problems, which are genuinely separate.

```
 INVALIDATION                            EVICTION
 the entry is WRONG                      the entry is RIGHT but does not fit

 caused by: a write to the origin        caused by: memory pressure
 fixed by:  TTL, delete on write,        fixed by:  LRU, LFU, admission control
            versioned keys
 failure:   serving stale data           failure:   a collapsed hit rate
            (a correctness bug)                     (a performance bug)
```

The race, drawn on a timeline. This is the diagram to be able to produce.

```
 time ──────────────────────────────────────────────────────────────►

 READER A   GET x → MISS
            └─ DB read x = 60 ──────────────────┐
                                                │
 WRITER B                  DB write x = 70      │
                           cache DELETE x       │
                                                │
 READER A                                       └─► cache SET x = 60   ✗

 cache: 60          database: 70          nothing will fix it
                                          until the TTL expires

 A was holding an old number and wrote it on the board last.
```

The three write strategies, side by side:

```
 WRITE-THROUGH              WRITE-AROUND               WRITE-BACK
 ------------------         --------------------       -----------------------
 app ──► cache SET          app ──► DB write           app ──► cache SET
     └─► DB write               └─► cache DELETE           (returns immediately)
     (both, then return)        (then return)                       │
                                                          after 30s │
 cache always fresh         next read is a miss                     ▼
 every write pays twice     nothing wasted              ──────► DB write
 caches unread data                                     fastest writes
                                                        LOSES DATA on crash
                                                        collapses repeated writes
```

Eviction under a scan, which is the failure worth drawing:

```
 hit rate over the day, LRU, with a nightly export at 02:00

 95% │████████████████████                    ████████████████
     │                    │
 50% │                    │
     │                    │  ← the export touched every key once,
  5% │                    ████                  evicting the entire working set
     └──────────────────────────────────────────────────────────
      00:00      02:00   02:05      03:30              06:00

 recovery takes as long as it takes real traffic to fault the working set
 back in — here, ninety minutes of degraded service caused by a report.

 fix: admission control — an item enters the cache only on its SECOND request,
      so a one-off scan never displaces anything.
```

---

## 5. How it actually works

### Choosing an invalidation strategy, in order

**Step 1 — put a TTL on everything.** Even if you invalidate explicitly. It is the bound on every bug you
have not found yet, and it costs nothing.

**Step 2 — decide the tolerable staleness per kind of data.** This is a product question, not an
engineering one:

```
 a user's own profile after they edit it     0 seconds     -> invalidate on write
 another user's profile                      60 seconds    -> TTL
 a product price                             5 minutes     -> TTL, plus invalidate on change
 a category listing                          10 minutes    -> TTL
 a homepage banner                           1 hour        -> TTL
 exchange rates                              1 minute      -> TTL
```

**"I saved it and it did not change" is the worst possible staleness**, which is why the user's own
writes always get explicit invalidation even when everything else is on a TTL.

**Step 3 — for explicit invalidation, publish an event rather than deleting directly.** The writer does
not know every derived key. Publishing `product.updated` and letting each cache owner subscribe keeps
that knowledge where it belongs.

**Step 4 — for one-to-many invalidation, version a namespace.**

```
 GET  category:electronics:version   ->  17
 GET  category:electronics:v17:page:1

 to invalidate the whole category:
 INCR category:electronics:version   ->  18
 -> every v17 key is now unreachable, in one operation
 -> they age out under eviction on their own
```

**One `INCR` invalidates thousands of keys** with no scan and no key list. This is the trick to reach for
when someone says "but that change affects a hundred cached pages".

### The cache-aside code, written properly

```python
def get_product(product_id: int) -> Product:
    key = f"product:{product_id}"
    cached = cache.get(key)
    if cached is not None:
        return deserialise(cached)

    product = db.query("SELECT ... WHERE id = ?", product_id)
    cache.set(key, serialise(product), ttl=300)     # ALWAYS a TTL
    return product


def update_product(product_id: int, changes: dict) -> None:
    db.update("UPDATE products SET ... WHERE id = ?", product_id, changes)
    cache.delete(f"product:{product_id}")           # DELETE, not SET
    events.publish("product.updated", product_id)   # others invalidate their own
```

**Three things to point at while writing it**: the TTL is not optional; the write **deletes** rather than
sets; and the database write happens **before** the delete, not after.

That last one matters:

```
 delete first, then write DB:
   t1 delete cache
   t2 a reader misses, reads the OLD value from the DB, caches it
   t3 the write lands in the DB
   -> the cache holds the old value with a fresh TTL

 write DB first, then delete:
   the window is much smaller — only a reader who read before t1
   and writes after the delete
```

**Database first, then invalidate.** Both orders have a race; this one's window is far smaller.

### Sizing eviction

The question "is my cache big enough" has a measurable answer:

```
 watch two numbers:
   hit rate            — is the cache doing its job?
   eviction rate       — how many keys per second are being pushed out?

 low hit rate + high eviction rate    -> too small; the working set does not fit
 low hit rate + low eviction rate     -> wrong keys, or access is uniform;
                                          a bigger cache will not help
 high hit rate + high eviction rate   -> fine; a long tail is churning harmlessly
```

**That two-by-two is the answer to "how would you tune the cache"**, and it is much better than "I would
make it bigger".

### What real systems do

- **Redis** with `maxmemory` and `maxmemory-policy allkeys-lru` is the standard application cache. Its
  LRU is **approximate** — sampled, not exact — and `maxmemory-samples` tunes how close it gets.
- **Memcached** uses a segmented LRU with slab allocation, which is why it can suffer *slab calcification*:
  memory assigned to one object size cannot easily be reused for another.
- **CDNs** invalidate by **purge** — an API call that tells every edge location to drop a URL — and it is
  slow and rate-limited, which is why the standard practice is **cache-busting URLs** instead:
  `app.a3f9c2.js` rather than `app.js`. **A new name is a new key, so nothing needs invalidating.** That
  is the versioned-key idea, applied at the edge.
- **Facebook's memcached paper** introduced **leases**: on a miss, the cache hands the reader a token, and
  a `set` is only accepted if the token is still valid — which closes exactly the race above. It is the
  most rigorous published answer to this problem.
- **Caffeine** (Java) and several CDNs use **W-TinyLFU**: a small frequency sketch decides whether a new
  item is worth admitting at all, which is what makes them resistant to scans.

---

## 6. The numbers

### What a TTL is actually choosing

```
 TTL      max staleness    refreshes/day/key    DB load for 1M cached keys
 ------   --------------   ------------------   --------------------------
 10 s     10 s             8,640                100,000 reads/s
 60 s     1 min            1,440                 17,000 reads/s
 5 min    5 min            288                    3,300 reads/s
 1 hour   1 hour           24                       280 reads/s
 1 day    1 day            1                         12 reads/s
```

**The TTL is a dial between staleness and origin load, and the relationship is linear.** Going from 60
seconds to 5 minutes cuts the refresh load by a factor of five and increases the worst-case staleness by
the same factor. There is no cleverness in it — that is the entire trade.

### The cost of the race, if you never fix it

```
 6,000 reads/s, 100 writes/s
 race window (DB read to cache set)        ~2 ms
 probability a given write overlaps a
   concurrent read of the SAME key         depends on key popularity

 for a hot key read 100 times/second:
   P(a write lands inside a 2 ms window)   100 × 0.002  =  20% per write
 -> a hot key that is written once a minute is stale
    for the remainder of its TTL, roughly one time in five
```

**With a 300-second TTL, that is a wrong value served for up to five minutes, several times an hour, on
your most-read key.** That number is why the race is worth taking seriously rather than dismissing as
unlikely.

### Eviction and hit rate

```
 working set 2 GB, cache 2 GB       hit rate ~90%,  eviction rate low
 working set 2 GB, cache 1 GB       hit rate ~70%,  eviction rate high
 working set 2 GB, cache 500 MB     hit rate ~45%,  eviction rate very high

 and the load consequence at 6,000 reads/s:
   90% ->    600 reads/s reach the DB
   70% ->  1,800 reads/s
   45% ->  3,300 reads/s
```

**Halving the cache more than doubled the database load.** Cache memory is usually the cheapest capacity
you can buy, and this table is the argument.

### The scan disaster, measured

```
 before the nightly export   hit rate 95%,   600 DB reads/s
 during and after            hit rate  5%,  5,700 DB reads/s      9.5×
 recovery time               as long as real traffic takes to refill the working set
                             — commonly 30-90 minutes

 with admission control (enter on the second request):
   the export's keys are never admitted at all
   hit rate during the export: unchanged
```

**A nightly report causing a ninety-minute morning outage is a real and common incident**, and "an
admission filter, or run the export against a replica with its own cache" is the answer.

### Write-back's collapse ratio

```
 a video watched 10,000 times in a minute
   write-through:  10,000 database writes
   write-back:          1 database write per flush interval

 collapse ratio for a hot counter: 100x - 10,000x
 cost of a crash: up to one flush interval of counts, lost
```

**That ratio is why view counters are the canonical write-back use case** — and why they are also the
canonical example of data whose loss is acceptable.

---

## 7. The trade-offs

### TTL against explicit invalidation

**A TTL** is simple, needs no coordination, and is self-healing — every invalidation bug you have not
found is bounded by it. It guarantees staleness.

**Explicit invalidation** gives near-zero staleness and requires the writer to know every derived key,
which is where the bugs live. Miss one, and it is stale until the TTL saves you — which is why you want
both.

**Use both, always.** Explicit invalidation for the paths that matter, and a TTL underneath as the
backstop.

### Delete or update on write?

**Delete.** Two reasons. It closes the writer-versus-writer race entirely, because there is nothing to
overwrite. And it avoids caching values that nobody subsequently reads — a write-heavy key that is rarely
read should not be occupying cache space.

**I would update instead if** the value is expensive to recompute and is certain to be read immediately
— a user's own profile right after they save it, where the alternative is a guaranteed miss on the very
next request. That is write-through, and it is a deliberate exception.

### Write-back, and what it is really for

**I would not use write-back for anything I could not lose.** The failure is not subtle: the cache dies
and everything not yet flushed is gone, with no trace.

**But for counters it is the right answer and the alternative is worse** — ten thousand database writes a
minute for a view count is real load, spent on a number nobody needs to be exact. The honest framing is:
*this data is approximate by nature, so I am trading exactness I do not need for load I cannot afford.*

### LRU, and where it fails

**LRU by default.** It is one line of configuration, it matches how most data is accessed, and everyone
understands it.

**I would not use plain LRU if** the workload contains periodic full scans — reports, exports, crawlers —
because a single scan evicts the entire working set. Then: admission control, a separate cache for the
scanning workload, or run the scan against a replica.

**LFU is right when popularity is stable and long-lived** — a catalogue where the same items are popular
for months. Its weakness is the mirror image: a genuinely new item can never accumulate a count and so is
evicted immediately, which is why practical implementations decay the counts over time.

### The thing that is genuinely hard

**One write invalidating many keys.** A price change touches the product page, the category listing, the
search index, the cached cart totals, and the homepage. There is no mechanism that finds those for you.
The three answers are: **events**, so each cache owner drops its own keys; **namespace versioning**, so
one `INCR` invalidates a whole family; or **short TTLs**, and accept the staleness.

Anyone who says invalidation is easy has only ever invalidated one key at a time.

### Where this breaks entirely

- **Multiple caches with different TTLs.** The browser has one copy, the CDN another, Redis a third. A
  user who "hard refreshes" and sees a different answer from a normal refresh is seeing exactly this, and
  invalidating all layers is genuinely difficult. **This is why static assets get content-hashed names
  instead.**
- **Read-your-own-writes across layers.** A user saves and immediately reads, and the read goes through a
  CDN with a five-minute TTL. Invalidating Redis was not enough.
- **Cache warm-up after a deploy.** An empty cache at peak is the same spike as an outage, which is why
  large systems pre-warm before taking traffic.

---

## 8. In the interview

### How it gets asked

- The direct one: *"How do you keep the cache consistent with the database?"*
- The race: *"A write and a read happen at the same time. Walk me through it."*
- The choice: *"Write-through, write-back or write-around?"*
- The eviction one: *"The cache is full. What do you throw away?"*
- The nasty one: *"A nightly report runs and the morning is slow. Why?"*
- The scope one: *"Changing this one product invalidates a hundred cached pages. Now what?"*

### What to say out loud, in the first ninety seconds

1. **Separate the two problems immediately.** "Invalidation is about correctness — the entry is wrong.
   Eviction is about capacity — the entry is right but does not fit. They have different mechanisms and
   different failure modes."
2. **Give the default and the backstop together.** "Write to the database, then **delete** the cache key —
   write-around. And a TTL on every key regardless, as the bound on every invalidation bug I have not
   found."
3. **Say delete, not update, and why.** "I delete rather than write the new value, because writing opens a
   window where a concurrent reader holding an older value can overwrite mine."
4. **Name the staleness you are accepting, per data type.** "A user's own profile after they edit it gets
   explicit invalidation, because 'I saved it and it did not change' is the worst kind of staleness.
   Another user's profile can sit on a sixty-second TTL."
5. **Pre-empt the eviction question.** "LRU, and `allkeys-lru` specifically in Redis, because the default
   is `noeviction` which returns errors on write when full."
6. **Flag the scan weakness.** "The failure mode of LRU is a sequential scan — a nightly export touches
   every key once and evicts the entire working set."

### The follow-ups

**"Walk me through the race between a read and a write."**
"A reader misses the cache and goes to the database, and gets the old value — say 60. Before it writes
that into the cache, a writer updates the database to 70 and deletes the cache key. Then the reader
finishes and sets the cache to 60. The cache now holds 60, the database holds 70, and **nothing will
correct it**, because there are no further writes — it is wrong until the TTL expires. The reader was
holding an old number and wrote it last. Four mitigations, in the order I would apply them. A **TTL on
every key**, which bounds the damage — that is non-negotiable regardless. **Delete rather than set on
write**, which eliminates the much more common writer-versus-writer version. A **delayed double delete**:
delete, write, then delete again after a short delay to clear anything a reader populated in between. And
if it genuinely matters, a **per-key lock on the miss path**, or Facebook's **lease** mechanism, where the
cache hands out a token on a miss and only accepts a `set` if that token is still valid."

**"Write-through, write-back or write-around?"**
"**Write-around by default**: write the database, delete the cache key, let the next read repopulate. It
wastes nothing on data that is written and never read, and deleting is safer than setting. **Write-through**
when a write is almost always followed by a read of the same key — a user editing their own profile and
then being shown it — because otherwise you have engineered a guaranteed miss on the very next request.
**Write-back** only for data I can afford to lose, and the canonical case is counters: a video watched
ten thousand times in a minute is ten thousand database writes with write-through and one with
write-back. That collapse ratio is the point, and the cost is that a crash loses up to one flush interval
of counts — which for a view counter is acceptable and for anything financial is not."

**"The cache is full. What do you throw away?"**
"**LRU**, because recency predicts reuse and it is one configuration line. In Redis specifically I would
set `allkeys-lru`, and I would point out that the **default is `noeviction`**, which means an
unconfigured Redis used as a cache starts returning errors on writes when it fills rather than making
room. Redis's LRU is also **approximate** — it samples a few keys and evicts the least recently used
among them, because maintaining exact ordering would cost a list update on every read. LRU's weakness is
**scans**: one nightly export touches every key once and evicts the whole working set, and the hit rate
does not recover until real traffic faults it back in. The fix is **admission control** — only admit an
item on its second request — which is what W-TinyLFU does, and it is why Caffeine and several CDNs use
it."

**"A nightly report runs and the morning is slow. Why?"**
"That is the LRU scan problem, and it is a real incident pattern rather than a theoretical one. The report
reads every row once. Every one of those reads populates the cache, and every insertion evicts something
from the actual working set. By the time it finishes, the cache is full of items nobody will request
again, the hit rate has gone from ninety-five percent to single digits, and the database is taking nine or
ten times its normal read load at exactly the hour traffic picks up. Recovery is however long real traffic
takes to refill the working set — commonly half an hour to ninety minutes. Three fixes: **do not admit
scan traffic** into the cache at all, which is admission control or simply a flag on those queries; run the
report against a **read replica** with its own cache; or run it against a snapshot. The one thing that does
not work is making the cache bigger."

**"Changing one product invalidates a hundred cached pages. Now what?"**
"Three options and I would pick based on how many keys and how well I know them. If the set is knowable,
**publish an event** — `product.updated` — and let each cache owner delete its own keys, because the
writer should not have to know that the search service caches something derived from this. If the set is
large or unknown, **version a namespace**: put a version number in the key prefix, and invalidate by
incrementing that one counter — a single `INCR` makes thousands of keys unreachable, and they age out
under eviction on their own. And if neither is worth the complexity, **short TTLs and accept the
staleness**, which is a legitimate answer if the data can be a minute old. The one thing I would not do is
try to enumerate and delete a hundred keys from the writer, because that list is wrong within a month."

**"Does the order matter — delete the cache before or after writing the database?"**
"Yes, and both orders have a race, but the windows are very different. If I **delete first and then
write**, a reader can miss, read the old value from the database, and cache it with a fresh TTL — all
before my write lands. That window is as long as my database write takes, which is milliseconds, and the
result is stale for a full TTL. If I **write first and then delete**, the only reader that can hurt me is
one that read the database *before* my write and sets the cache *after* my delete — a much smaller
window. So: **database first, then invalidate.** And I would still have the TTL underneath, because
neither order is airtight."

### A model answer

Asked: *how do you keep the cache consistent with the database?*

> "First I want to separate two things that get run together. **Invalidation** is about correctness — the
> cached entry is wrong because the underlying value changed. **Eviction** is about capacity — the entry
> is still correct but there is no room for it. Different mechanisms, different failure modes: bad
> invalidation serves wrong data, bad eviction just makes things slow.
>
> For invalidation, my default is **write-around**: write the database, then **delete** the cache key, and
> let the next reader repopulate it. I delete rather than write the new value, and that choice matters —
> writing opens a window where a concurrent reader that is holding an older value can land on top of mine,
> whereas a deleted key simply produces a miss and a fresh read of the truth.
>
> And regardless of everything else, **a TTL on every key**. Not because I expect to need it, but because
> it bounds every invalidation bug I have not found yet. Explicit invalidation is where the mistakes live
> — one write often affects many derived keys, and the writer rarely knows all of them.
>
> The race I would want to talk about is the read-write one. A reader misses, goes to the database, gets
> 60. Before it caches that, a writer sets the database to 70 and deletes the key. Then the reader
> completes and caches 60. **The cache now holds 60, the database holds 70, and nothing is going to fix
> it** — there are no more writes, so it stays wrong until the TTL expires. On a hot key that is read a
> hundred times a second, a write has roughly a one-in-five chance of hitting that window. So: the TTL
> bounds it; deleting rather than setting removes the more common writer-versus-writer variant; a delayed
> second delete clears anything a reader populated in between; and if it genuinely matters, a per-key lock
> on the miss path, or leases, where the cache issues a token on a miss and only accepts a `set` if the
> token is still valid.
>
> On ordering: **write the database first, then invalidate.** Both orders race, but deleting first leaves
> a window as long as the database write during which a reader can cache the old value with a fresh TTL,
> which is much worse.
>
> For the staleness budget I would go data type by data type, because it is a product decision. A user's
> own profile after they edit it gets explicit invalidation — 'I saved it and it did not change' is the
> worst possible staleness. Another user's profile is fine on a sixty-second TTL. A homepage banner can be
> an hour.
>
> On eviction: **LRU**, and in Redis specifically `allkeys-lru`, because the default is `noeviction` and
> an unconfigured Redis will start refusing writes rather than making room. The weakness worth naming is
> scans — a nightly export touches every key once and evicts the entire working set, taking the hit rate
> from ninety-five percent to nearly nothing and roughly ten-times-ing the database load right as the
> morning starts. The fix is admission control, not a bigger cache.
>
> And if you tell me one write invalidates a hundred cached pages, my answer is namespace versioning: put
> a version in the key prefix and increment it once, which makes every key underneath unreachable in a
> single operation and lets them age out under eviction."

---

## 9. Recall card

- **Invalidation is correctness (the entry is wrong); eviction is capacity (the entry is right but does
  not fit).** Different mechanisms, different failures. Default: **write-around** — write the DB, then
  **DELETE** the key — plus **a TTL on every key** as the bound on every invalidation bug you have not
  found.
- **Delete, do not update, on a write**, and **write the database FIRST, then invalidate** — deleting
  first leaves a window as long as the DB write in which a reader caches the old value with a fresh TTL.
- **The race to be able to draw:** reader misses → reads 60 from the DB → writer sets 70 and deletes →
  reader sets 60. **Cache 60, DB 70, and nothing will correct it** until the TTL. On a key read 100×/s, a
  write has ~20% chance of hitting the window. Fixes in order: **TTL · delete-not-set · delayed double
  delete · per-key lock or leases.**
- **Write-through** when a read always follows the write (a user's own profile). **Write-around** by
  default. **Write-back only for data you can lose** — a counter watched 10,000 times a minute becomes
  **one** DB write instead of 10,000.
- **LRU by default, and `allkeys-lru` in Redis — the default is `noeviction`, which returns errors when
  full.** Redis's LRU is **approximate** (sampled). Its weakness is **scans**: a nightly export evicts the
  whole working set, hit rate 95% → 5%, DB load ~10×, recovery 30–90 minutes — fixed by **admission
  control**, not a bigger cache. And for **one write invalidating many keys**: publish an **event**, or
  **version a namespace** so one `INCR` invalidates thousands.
