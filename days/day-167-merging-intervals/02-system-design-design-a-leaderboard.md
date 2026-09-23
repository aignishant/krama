---
day: 167
track: system-design
title: "Design a leaderboard"
phase: "High-level design case studies"
status: written
---

# Design a leaderboard

## 1. What this is, and why they ask it

A leaderboard shows who is winning. **Top ten, and "you are 4,412th".** That is the whole product.

They ask it because **it looks trivial for about ninety seconds and then does not.** "Sort by score" is the
obvious answer and it is right for a thousand players. **At fifty million players with scores changing every
second, sorting on every read is impossible and sorting on every write is worse.**

Three things carry the interview.

**The top ten is easy and the rank is hard.** Returning the highest ten scores is a cheap query in almost any
store. **Answering "what is my rank" requires counting everyone above you**, which is a full scan unless the
structure was built for it — **and that asymmetry is the thing to notice.**

**The obvious answer is a sorted set, and knowing why is the point.** Redis sorted sets keep elements ordered
by score in a skip list with an auxiliary hash, **so insertion, rank lookup and range queries are all
logarithmic.** A candidate who says "Redis `ZADD` and `ZREVRANK`" has the right answer; **a candidate who can
say what is underneath and where it stops scaling has the interview.**

**And where it stops scaling is genuinely interesting.** One sorted set holds tens of millions of entries in a
few gigabytes. **A hundred million players across many leaderboards does not fit in one, and sharding a ranked
structure is hard** — because rank is inherently global, and any split makes "how many are above me" a query
across every shard.

By the end of this lesson you can design the sorted-set solution and size it, handle exact rank at scale,
know when approximate rank is correct, deal with ties and time windows, and say what breaks.

---

## 2. The story

The wrestling akhara had about ninety boys and one board and Gopichand had kept it since before any of them
were born.

**Names down the left, in order. The best at the top.**

**And what he did with it took about four minutes a day.** A boy won a bout, and Gopichand rubbed out two
names and wrote them again the other way round, **and the whole board was correct in under a minute because
one win almost never moves anybody more than a place or two.**

**That was the first thing, and it stayed true for thirty years.**

**The second thing was the question he could not answer quickly, and he did not notice for a long time that it
was a different question.**

Because "who is at the top" was one glance. **And "where am I" — asked by a boy standing next to him, every
single day — meant counting.**

Ninety names, from the top, with a finger. **Twenty seconds.** Which was fine for ninety.

**And then the akhara joined the district association and there were four thousand names.**

**The top ten was still one glance.** The board was still correct. **And "where am I" had become
unanswerable**, because counting four thousand names with a finger is twenty minutes and by the end it was
wrong anyway.

His solution was not clever and it worked for eleven years.

**He drew a line every hundred names and wrote the number in the margin.**

So a boy at position three thousand two hundred and something — **you found the line marked three thousand two
hundred, and counted forward from there.** Never more than a hundred names. **Four seconds instead of twenty
minutes.**

And the second half of it, which the boys worked out for themselves and he never had to say.

**Below about the first two hundred, nobody asked for the exact number.**

They asked whether they were in the top five hundred, or roughly where in the middle. **"About two thousand
one hundred" was a completely acceptable answer to a boy at position 2,137**, and it would have been an
insulting one to the boy at position four.

**"At the top they want the number," Gopichand said. "In the middle they want the neighbourhood."**

---

## 3. The idea in plain English

Gopichand's board is a sorted set, his lines in the margin are the index that makes rank cheap, and his last
sentence is the thing that makes this affordable at scale.

**Start with the two questions, because they have different costs.**

```
   "TOP TEN"                       "WHAT IS MY RANK?"
   read the first 10 entries       COUNT how many are above me
   O(1) or O(log n) anywhere       O(n) unless the structure supports it

   -> the top-k is easy in ANY sorted store
   -> the RANK is what makes this a design problem
```

**Almost every naive design gets the top-ten right and cannot answer the rank**, and noticing that asymmetry in
the first minute is the strongest opening move available.

**Now the obvious answer, and what is underneath it.**

**A Redis sorted set is the right default**, and it is worth being able to say why rather than just naming it.

```
   ZADD  leaderboard 4820 "player:1234"      update a score       O(log n)
   ZREVRANK leaderboard "player:1234"        my rank              O(log n)
   ZREVRANGE leaderboard 0 9 WITHSCORES      the top ten          O(log n + 10)
   ZREVRANGE leaderboard 4405 4415           the ten around me    O(log n + 10)
   ZCARD leaderboard                         how many players     O(1)
```

**Underneath it is a skip list plus a hash map.** The skip list keeps the elements in score order and **carries
a span on each forward pointer — the number of elements it jumps over** — which is what makes rank a
logarithmic query rather than a count. **The hash map gives `O(1)` lookup from member to score**, so updating
an existing player does not require a search.

**That combination — ordered structure plus the span counts — is the whole reason this is the standard
answer**, and it is exactly Gopichand's lines in the margin.

**Now the sizing, which decides whether one sorted set is enough.**

**Roughly a hundred bytes per entry** in Redis, including the skip-list nodes and the hash entry. **Ten million
players is about a gigabyte** and answers every query in microseconds. **A hundred million is ten gigabytes**,
which is one large instance and is beginning to be uncomfortable.

**And the thing to notice is that it is a single-machine structure.** You cannot split a sorted set across
machines and still answer rank cheaply, **because rank is global** — "how many are above me" is a question
about every player, everywhere.

**So the scaling answer is not "shard the sorted set". It is one of three other things.**

**One: partition the leaderboard, not the data.** Most games do not have one global board — **they have one per
region, per level, per week, per friend group.** Each of those is a separate, smaller sorted set, **and the
partitioning is a product fact rather than an engineering compromise.** This is by far the most common answer
and it is usually the right one.

**Two: keep only the top N exactly.** **Nobody below the top ten thousand needs an exact rank.** Keep a bounded
sorted set of the top ten thousand — trimmed on every write — **and answer everyone else approximately.**
Gopichand's boys, exactly.

**Three: approximate rank by bucketing.** Keep a histogram of scores — how many players fall in each score
range — **and a rank is the sum of the buckets above yours plus a count within your bucket.** **Sub-millisecond,
tiny, and accurate to within a bucket.**

**And the approximation is not a compromise for most users**, because "about 2,100th of 50,000" is a better
answer than an exact number nobody can act on. **Exact at the top, approximate in the middle** — which is a
product decision that happens to be the cheap one.

**Then ties, which are a real product problem and not an edge case.**

**Two players with the same score.** What order? **Redis breaks ties lexicographically by member name**, which
is stable and arbitrary and means player "aaa" always beats player "zzz" at equal score.

**The usual fix is to encode the tie-break into the score itself.** A common trick: **use a composite score
where the high bits are the game score and the low bits are an inverted timestamp**, so an earlier achiever
ranks higher.

```
   composite = score * 10^10 + (10^10 - seconds_since_epoch)
```

**Doubles hold 53 bits of integer precision**, so this works while `score × 10^10` stays under about `9 × 10^15`
— **which is a real constraint worth checking rather than assuming.**

**Then time windows, which is where most of the actual complexity is.**

**"Top players today", "this week", "all time" are three different leaderboards**, and the naive answer —
recompute from an event log — is far too slow for a live board.

**Keep a separate sorted set per window and expire it.** `leaderboard:daily:2026-09-01` with a TTL of a couple
of days; `leaderboard:weekly:2026-W35`; `leaderboard:alltime` with no expiry. **A score update writes to all
three**, which is three cheap operations rather than one expensive recomputation.

**The cost is write amplification** — one score becomes three or four writes — **and it is worth it, because
reads vastly outnumber writes and each read becomes a single lookup.**

**And "rolling last 24 hours" is a genuinely harder problem** than "today", because there is no window to
expire. **The honest answer is usually to approximate it with hourly buckets** and accept an hour of
granularity, rather than to build something exact.

**Finally: the durability question, which people forget.**

**Redis is the serving structure and it is not the source of truth.** A score is written to a durable store —
**the game's own database — and then to the sorted set.** If Redis is lost, **the leaderboard is rebuilt from
the durable store**, which takes minutes and is fine.

**Building it the other way round — treating the sorted set as authoritative — means a Redis failure loses
scores**, and scores are the product.

---

## 4. The picture

The asymmetry that defines the problem:

```
   TOP TEN                            MY RANK

   [ 1] Ravi     9,912               "how many players have a
   [ 2] Meera    9,880                score above 4,820?"
   [ 3] Anil     9,844
   ...                                -> a COUNT over everyone
   [10] Kavya    9,301                -> O(n) unless the structure
                                         was built for it
   -> read the first 10
   -> cheap in ANY sorted store

   ALMOST EVERY NAIVE DESIGN GETS THE TOP TEN RIGHT AND
   CANNOT ANSWER THE RANK. Notice that in the first minute.
```

What is inside a sorted set:

```
   SKIP LIST, ordered by score, with SPANS on the forward pointers

   level 3  head ---------------------------> [8200] ------> nil
                   span 5                       span 3
   level 2  head -------> [9301] ------------> [8200] -----> nil
                  span 2     span 3              span 3
   level 1  head -> [9912] -> [9880] -> [9844] -> ... -> nil
              span 1   span 1    span 1

   + A HASH MAP:  member -> score      (O(1) score lookup)

   THE SPANS ARE THE POINT: each forward pointer records how many
   elements it jumps over, so RANK is the sum of the spans along
   the search path — O(log n), not a count.

   That is exactly Gopichand's line every hundred names.
```

Where one sorted set stops:

```
   ~100 bytes per entry (skip-list nodes + hash entry)

   1,000,000 players     ~100 MB    comfortable
   10,000,000            ~1 GB      fine
   100,000,000           ~10 GB     one large instance, uncomfortable
   1,000,000,000         ~100 GB    does not fit

   AND YOU CANNOT SHARD IT USEFULLY, because RANK IS GLOBAL:
     "how many are above me" is a question about EVERY player
     -> sharded, every rank query hits every shard and sums
     -> which is correct and slow, and gets slower with more shards
```

The three scaling answers:

```
   1. PARTITION THE LEADERBOARD, NOT THE DATA

      one global board          ->  per region, per level, per week,
      100,000,000 entries           per friend group
                                    -> each is small
      -> this is a PRODUCT FACT, not a compromise, and it is
         usually the real answer


   2. EXACT TOP N, APPROXIMATE BELOW

      keep the top 10,000 in a bounded sorted set (trim on write)
      everyone else: approximate

      -> "at the top they want the number; in the middle they
         want the neighbourhood"


   3. BUCKETED APPROXIMATE RANK

      a histogram: how many players in each score range

        score 9000-9999:   1,204 players
        score 8000-8999:  11,873
        score 7000-7999:  48,200
        ...

      my rank ~ sum of the buckets above mine
      -> sub-millisecond, a few KB, accurate to within a bucket
```

The tie problem:

```
   three players, all on 4,820

   REDIS default: ties break LEXICOGRAPHICALLY by member name
     -> "player:aaa" always ranks above "player:zzz"
     -> stable, arbitrary, and visible to users who notice

   THE FIX: encode the tie-break INTO the score

     composite = score * 10^10 + (10^10 - timestamp)
                 ^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^^^^
                 the real score   earlier = LARGER = ranks higher

   CHECK THE PRECISION: doubles hold 53 bits of exact integer range,
   so this is safe while score x 10^10 stays under ~9 x 10^15.
   Not an assumption to make silently.
```

Time windows, and the write amplification:

```
   ONE SCORE UPDATE ->  ZADD leaderboard:daily:2026-09-01   (TTL 2 days)
                        ZADD leaderboard:weekly:2026-W35    (TTL 2 weeks)
                        ZADD leaderboard:alltime            (no TTL)

   3-4x write amplification, and each READ is a single lookup.

   -> the right trade, because reads vastly outnumber writes

   AND: "rolling last 24 hours" is genuinely harder — there is no
   window to expire. The honest answer is hourly buckets and an
   hour of granularity, not an exact rolling window.
```

---

## 5. How it actually works

### The basic operations

```python
def submit_score(player_id: int, score: int) -> None:
    """Durable store FIRST, then the serving structure."""
    db.execute("""INSERT INTO scores (player_id, score, at)
                  VALUES (%(p)s, %(s)s, now())""",
               {"p": player_id, "s": score})
    redis.zadd("leaderboard:alltime", {f"player:{player_id}": score})


def top_n(n: int = 10) -> list[tuple[str, float]]:
    return redis.zrevrange("leaderboard:alltime", 0, n - 1, withscores=True)


def my_rank(player_id: int) -> int | None:
    rank = redis.zrevrank("leaderboard:alltime", f"player:{player_id}")
    return None if rank is None else rank + 1        # 0-indexed -> 1-indexed


def around_me(player_id: int, window: int = 5) -> list[tuple[str, float]]:
    rank = redis.zrevrank("leaderboard:alltime", f"player:{player_id}")
    if rank is None:
        return []
    lo = max(0, rank - window)
    return redis.zrevrange("leaderboard:alltime", lo, rank + window,
                           withscores=True)
```

**The durable write comes first**, and that ordering is the design decision: **Redis is the serving structure,
not the source of truth.** If Redis is lost, the leaderboard is rebuilt in minutes; **if the durable write were
second, a Redis failure would lose scores.**

**And `rank + 1` is worth a comment** — `ZREVRANK` is zero-indexed and users count from one, which is a
one-character bug that ships surprisingly often.

### Highest score, not latest

```python
def submit_best_score(player_id: int, score: int) -> bool:
    """Most games keep a player's BEST score, not their most recent."""
    member = f"player:{player_id}"
    current = redis.zscore("leaderboard:alltime", member)
    if current is not None and current >= score:
        return False                          # not an improvement
    redis.zadd("leaderboard:alltime", {member: score}, gt=True)
    return True
```

**`gt=True` makes it atomic** — Redis updates only if the new score is greater — **so a check-then-write race
between two concurrent submissions cannot lower a player's score.**

**Without it, the read and the write are separate and an older submission arriving late can overwrite a better
one.**

### Ties, encoded into the score

```python
TIE_SCALE = 10 ** 10

def composite_score(score: int, achieved_at: float) -> float:
    """Higher score wins; on a tie, the EARLIER achievement wins."""
    inverted_time = TIE_SCALE - int(achieved_at)
    composite = score * TIE_SCALE + inverted_time
    assert composite < 2 ** 53, "beyond exact double precision"
    return float(composite)


def real_score(composite: float) -> int:
    return int(composite) // TIE_SCALE
```

**The assertion is not decoration.** **A double holds 53 bits of exact integer range — about 9 × 10¹⁵** — and
a composite beyond that silently loses precision, **which reorders players in a way nobody will diagnose.**

**And `real_score` exists because the displayed score must be the real one**, not the composite — which is easy
to forget and produces absurd numbers on screen.

### Time windows

```python
WINDOWS = {
    "daily":   (lambda t: time.strftime("%Y-%m-%d", time.gmtime(t)), 2 * 86400),
    "weekly":  (lambda t: time.strftime("%Y-W%W", time.gmtime(t)), 14 * 86400),
    "alltime": (lambda t: "", None),
}

def submit_all_windows(player_id: int, score: int, at: float) -> None:
    member = f"player:{player_id}"
    pipe = redis.pipeline()
    for name, (key_of, ttl) in WINDOWS.items():
        key = f"leaderboard:{name}:{key_of(at)}".rstrip(":")
        pipe.zadd(key, {member: score}, gt=True)
        if ttl:
            pipe.expire(key, ttl)             # the window expires itself
    pipe.execute()
```

**The TTL is what removes old windows** — no cleanup job, no cron, **and yesterday's daily board simply ceases
to exist.**

**And the pipeline makes three or four writes one network round trip**, which is what keeps the write
amplification cheap.

**Setting the TTL on every write is slightly wasteful and is correct**: **setting it only on creation risks a
key that never expires** if the creating call failed after the `ZADD`.

### Approximate rank by bucketing

```python
BUCKET_SIZE = 100

def record_for_histogram(score: int) -> None:
    redis.hincrby("score_histogram", str(score // BUCKET_SIZE), 1)


def approximate_rank(score: int) -> int:
    """Sum the buckets above mine. Sub-millisecond, accurate to a bucket."""
    my_bucket = score // BUCKET_SIZE
    buckets = redis.hgetall("score_histogram")
    above = sum(int(count) for bucket, count in buckets.items()
                if int(bucket) > my_bucket)
    return above + 1
```

**The whole histogram is a few thousand entries** — one per hundred-point band — **so fetching all of it is
kilobytes and summing it is microseconds.**

**And the accuracy is exactly one bucket**, which for a player at rank 2,137 is completely acceptable **and
would be unacceptable at rank 4** — which is why the exact structure covers the top.

### Exact at the top, approximate below

```python
TOP_N = 10_000

def submit_hybrid(player_id: int, score: int) -> None:
    member = f"player:{player_id}"
    pipe = redis.pipeline()
    pipe.zadd("leaderboard:top", {member: score}, gt=True)
    pipe.zremrangebyrank("leaderboard:top", 0, -(TOP_N + 1))   # trim the tail
    pipe.hincrby("score_histogram", str(score // BUCKET_SIZE), 1)
    pipe.execute()


def rank_hybrid(player_id: int, score: int) -> tuple[int, bool]:
    """Returns (rank, is_exact)."""
    exact = redis.zrevrank("leaderboard:top", f"player:{player_id}")
    if exact is not None:
        return exact + 1, True
    return approximate_rank(score), False
```

**`zremrangebyrank(key, 0, -(TOP_N + 1))` keeps the structure bounded** — the top ten thousand and nothing
else — **so it stays at about a megabyte regardless of how many players exist.**

**And returning `is_exact` matters for the interface**: the client shows "4,412th" or "about 2,100th",
**and the distinction should be visible rather than implied.**

### Sharding, and why it is unpleasant

```python
def sharded_rank(player_id: int, score: int, shards: int) -> int:
    """Correct, and it queries EVERY shard. Rank is inherently global."""
    total_above = 0
    for shard in range(shards):
        total_above += redis.zcount(f"leaderboard:{shard}",
                                    f"({score}", "+inf")
    return total_above + 1
```

**Every rank query hits every shard**, and **it gets slower as you add shards** — which is the opposite of what
sharding is supposed to do.

**That is the argument for partitioning the leaderboard by a product dimension instead**: a per-region board is
a *smaller* structure, not a *split* one, **and every query stays within it.**

### Rebuilding from the durable store

```python
def rebuild(window: str = "alltime", batch: int = 10_000) -> int:
    """Redis is not the source of truth. This is the recovery path."""
    key = f"leaderboard:{window}"
    temp = f"{key}:rebuilding"
    count, offset = 0, 0
    while True:
        rows = db.query("""SELECT player_id, MAX(score) AS best
                             FROM scores GROUP BY player_id
                            ORDER BY player_id LIMIT %(l)s OFFSET %(o)s""",
                        {"l": batch, "o": offset})
        if not rows:
            break
        redis.zadd(temp, {f"player:{r.player_id}": r.best for r in rows})
        count += len(rows)
        offset += batch
    redis.rename(temp, key)                   # atomic swap
    return count
```

**Building into a temporary key and renaming is what makes this safe to run against a live system** — **the old
leaderboard serves until the moment the new one is complete**, and `RENAME` is atomic.

**Rebuilding fifty million entries takes a few minutes**, which is an acceptable recovery time for a
leaderboard and would not be for a payments ledger — **and that difference is why Redis is allowed to be the
serving structure here.**

### The real systems

```
Redis sorted sets   the standard answer; skip list + hash, with
                    SPANS on the forward pointers making rank O(log n)
Valkey / KeyDB      Redis forks, same data structures
PostgreSQL          the durable source of truth for scores;
                    window functions can compute rank, slowly
ClickHouse          for historical analysis and rebuilds over
                    billions of score events
Kafka               the score event stream feeding both stores
```

**Naming the skip list and its spans is what distinguishes a real answer from "use Redis"**, because it
explains *why* rank is cheap — and that is the thing the question is actually about.

---

## 6. The numbers

**Scale.**

```
50,000,000 players
each plays ~5 sessions/day, each producing a score
= 250,000,000 score updates/day
= ~2,900/second average, peak ~15,000/second

leaderboard READS:
  each session opens the leaderboard ~3 times
  = 750,000,000 reads/day = ~8,700/second, peak ~40,000/second

read : write = 3 : 1
```

**Only three to one**, which is unusually write-heavy for a read-facing feature — **and it is why the write
path being cheap matters as much as the read path.**

**The sorted set.**

```
~100 bytes per entry (skip-list node with several levels,
                      plus the hash map entry, plus the member string)

50,000,000 players x 100 B = ~5 GB

-> one Redis instance, comfortably, with room for the windowed copies

10,000,000  -> ~1 GB
100,000,000 -> ~10 GB      one large instance, uncomfortable
1,000,000,000 -> ~100 GB   does not fit
```

**Operation costs.**

```
ZADD       O(log n)   50,000,000 entries -> ~26 comparisons
ZREVRANK   O(log n)   ~26 comparisons, summing spans
ZREVRANGE  O(log n + k)

in practice, all of them: ~50-100 MICROSECONDS

15,000 writes/second x 100 us = 1.5 CPU-seconds per second
40,000 reads/second  x 100 us = 4 CPU-seconds per second

-> ~6 cores of Redis work at peak.
   A single Redis instance is single-threaded and does ~100,000
   ops/second, so this is at about 55% of one instance.
```

**Fifty-five percent of a single instance at fifty million players** is worth saying, **because it reframes
the problem: the data structure is not the bottleneck at any realistic scale for one board.**

**Write amplification from windows.**

```
daily + weekly + monthly + all-time = 4 sorted sets
15,000 score updates/second x 4 = 60,000 ZADDs/second

-> now at ~150% of one instance
-> so: pipeline them (one round trip), and shard BY WINDOW
   across instances if needed — which is easy, because the
   windows are independent structures
```

**Sharding by window is the easy sharding** — the daily board on one instance, all-time on another —
**because no query ever crosses them.**

**Memory for the windowed copies.**

```
all-time:  50,000,000 players     ~5 GB
daily:     ~10,000,000 active players/day  ~1 GB   (TTL 2 days -> 2 GB)
weekly:    ~25,000,000            ~2.5 GB          (TTL 2 weeks -> 5 GB)
monthly:   ~40,000,000            ~4 GB

total: ~16 GB of Redis

-> one large instance or a small cluster, and the TTLs keep it
   from growing without bound
```

**The approximate structures, for contrast.**

```
HISTOGRAM (buckets of 100 points, scores up to 1,000,000)
  10,000 buckets x ~20 bytes = 200 KB

  -> the ENTIRE rank-approximation structure is 200 KB
     against 5 GB for the exact one
  -> 25,000x smaller, accurate to within 100 points of score

TOP 10,000 EXACT
  10,000 x 100 B = 1 MB

  -> exact where it matters, 1 MB
  -> approximate everywhere else, 200 KB
  -> 1.2 MB total against 5 GB
```

**A thousandth of the memory for a product that is arguably better** — exact where people care, approximate
where they do not.

**The sharded-rank cost, which is the argument against it.**

```
rank across 10 shards:
  10 x ZCOUNT, each O(log n)
  ~10 round trips (or one pipelined) -> ~1-2 ms

against 100 us for a single sorted set

-> 10-20x slower, AND it gets worse with more shards
-> which is backwards: sharding should help
```

**Rebuild time.**

```
50,000,000 players from the durable store
  reading:  ~10,000 rows/second/connection, 10 connections
            -> ~500 seconds
  ZADD:     pipelined in batches of 10,000
            -> ~50,000,000 / 100,000 per second = 500 seconds

  total: ~10-15 minutes

-> acceptable for a leaderboard.
   NOT acceptable for anything transactional, which is exactly
   why Redis is the serving layer here and not the record.
```

**Latency budget.**

```
top ten             ~0.2 ms
my rank             ~0.2 ms
players around me   ~0.3 ms  (rank, then a range)
+ network           ~1-5 ms

-> the leaderboard is not a latency problem.
   It is a MEMORY problem at very large scale, and a PRODUCT
   problem in the middle of the distribution.
```

---

## 7. The trade-offs

**Exact rank against approximate.** Exact costs a full sorted set — five gigabytes at fifty million players —
and answers in microseconds. **Approximate costs two hundred kilobytes and is accurate to a bucket.** **And for
most of the distribution, approximate is the better product**: "about 2,100th of 50,000" is more useful than an
exact number that changes every few seconds. **Exact at the top, approximate below** is the answer, and it is a
product decision that happens to be the cheap one.

**One sorted set against sharding.** One instance handles fifty million players at half its capacity — **so do
not shard until forced.** And when forced, **shard by leaderboard, not by player**, because rank is global and
a split structure makes every rank query hit every shard **and get slower as you add shards.**

**Time windows: separate structures against computing on demand.** Separate sorted sets per window cost three
to four times the writes and make every read a single lookup. **Computing "this week's top" from an event log
is minutes, which no live board can absorb.** The write amplification is the right trade **because reads
outnumber writes and each read must be fast.**

**Rolling windows against fixed ones.** "Today" and "this week" expire themselves with a TTL. **"The last
twenty-four hours" has nothing to expire** and would need a sliding structure. **Hourly buckets with an hour of
granularity is the honest approximation**, and pretending to offer an exact rolling window is how a simple
feature becomes an expensive one.

**Best score against latest score.** Most games rank a player's best, which needs an atomic
update-only-if-greater — **without which a late-arriving old submission overwrites a better one.** Ranking the
latest is simpler and makes the board volatile in a way players dislike. **Say which the product wants.**

**Redis as serving structure against source of truth.** Serving-only means a Redis failure costs a ten-minute
rebuild and nothing else. **Treating it as authoritative removes the durable write and loses scores on
failure** — and scores are the product. **The ten minutes is affordable precisely because it is a leaderboard**;
the same architecture would be unacceptable for a ledger.

**When would I not build this?** **Below a few hundred thousand players, `ORDER BY score DESC LIMIT 10` on the
database is the whole feature**, and rank via a window function is fine at that size. **Managed services exist**
— PlayFab, GameSparks, Firebase — **and for a small game they are cheaper than the operational cost of a Redis
cluster.** The design here is justified by scale and by the rank query specifically, **not by the top-ten
query, which was never hard.**

---

## 8. In the interview

### How it gets asked

- *"Design a leaderboard."* — usually with a scale like fifty million players.
- *"How do you show a player their rank?"* — the question that is actually hard.
- *"What data structure would you use, and why?"* — where naming the skip list matters.
- *"What if there are a hundred million players?"* — the scaling question.
- *"How do you handle daily and weekly boards?"*
- *"Two players have the same score. What order?"*

### The first ninety seconds

> "There are two questions here and they have completely different costs, **and I would separate them
> immediately because almost every naive design gets one right and cannot answer the other.**
>
> **The top ten is easy.** Read the first ten entries of anything sorted by score. **Cheap in any store.**
>
> **The rank is hard.** 'What is my position' means **counting how many players have a score above mine** —
> which is a full scan unless the structure was built for it. **That asymmetry is the actual problem.**
>
> **The right default is a Redis sorted set**, and I want to say why rather than just name it. **Underneath it
> is a skip list plus a hash map.** The skip list keeps elements in score order, **and each forward pointer
> carries a span — the number of elements it jumps over.** **Rank is the sum of the spans along the search
> path**, which makes it logarithmic rather than a count. The hash map gives constant-time score lookup, so
> updating an existing player needs no search.
>
> **That combination is the whole reason it is the standard answer.**
>
> **Sizing it: about a hundred bytes per entry, so fifty million players is five gigabytes** — one instance,
> comfortably. **And every operation is fifty to a hundred microseconds**, so at fifteen thousand writes and
> forty thousand reads a second, **I am at roughly half of one Redis instance.** The data structure is not the
> bottleneck at any realistic scale for a single board.
>
> **Where it stops is memory, and the answer is not to shard the sorted set.** **Rank is inherently global** —
> 'how many are above me' is a question about every player — **so a split structure means every rank query hits
> every shard and gets slower as you add shards.** That is backwards.
>
> **Three better answers.** **Partition the leaderboard by a product dimension** — region, level, week, friend
> group — which is usually what the product already wants. **Keep the top ten thousand exact and approximate
> everyone else.** **Or a score histogram**, where a rank is the sum of the buckets above yours.
>
> **And the approximate answer is not a compromise for most users.** 'About two thousand one hundred of fifty
> thousand' is a better answer than an exact number nobody can act on. **Exact at the top, approximate in the
> middle** — a product decision that happens to be a thousand times cheaper.
>
> **One thing before I go further: does the board rank a player's best score or their most recent?** Because
> best needs an atomic update-only-if-greater, and getting that wrong lets a late submission lower somebody's
> score."

### The follow-ups

**"What data structure, and why?"**

> "A Redis sorted set, and the interesting part is what is underneath, because that is what explains the cost.
>
> **A sorted set is two structures kept in step.** **A skip list**, which keeps the members in score order,
> **and a hash map from member to score.**
>
> **The hash map is why updating a player is cheap** — I can find their current score in constant time without
> searching the list.
>
> **And the skip list is why rank is cheap, because of one detail: each forward pointer carries a span** — the
> number of elements it jumps over. **So when I search down for a member, I sum the spans I skip past, and that
> sum is the rank.** Logarithmic, not a count.
>
> **Without those spans, a skip list would give me ordered iteration and rank would still be `O(n)`** — so the
> spans are precisely the feature that makes this the right structure, and they are exactly the equivalent of
> writing a number in the margin every hundred names.
>
> **The operations I would use:** `ZADD` to update a score, `ZREVRANK` for a player's rank, `ZREVRANGE` for the
> top ten or for a window around a player. **All `O(log n)`, all about fifty to a hundred microseconds at fifty
> million entries.**
>
> **Two implementation details worth mentioning.** **`ZREVRANK` is zero-indexed** and users count from one,
> which is a one-character bug that ships more often than it should. **And `ZADD` with `GT` makes 'keep the
> best score' atomic** — without it, reading the current score and then writing is a race, and a late-arriving
> old submission can lower a player's score.
>
> **Sizing: about a hundred bytes per entry** including the skip-list node, the hash entry and the member
> string. **Fifty million players is five gigabytes.**
>
> **The alternative I would rule out explicitly is a relational database with `ORDER BY score`.** The top ten is
> fine — that is an index scan. **But rank requires a window function or a count, which is a scan over every
> row above you**, and at fifty million rows that is seconds. **Below a few hundred thousand players it is
> genuinely the right answer**, and above that it is not."

**"A hundred million players. What breaks?"**

> "Memory, and then the instinct to shard — **which is the interesting part, because sharding makes it worse.**
>
> **A hundred million entries at a hundred bytes is ten gigabytes.** That is one large instance, and it is
> beginning to be uncomfortable — **not for throughput, which is fine, but for the blast radius and the restart
> time.**
>
> **And the obvious fix does not work.** **Rank is inherently global**: 'how many players have a score above
> mine' is a question about every player, everywhere. **If I split the sorted set across ten shards, every rank
> query has to ask every shard how many of its members are above my score and sum the answers.**
>
> **That is correct and it is ten to twenty times slower — and it gets worse as I add shards.** Sharding is
> supposed to make things faster with scale, **and here it does the opposite.**
>
> **So there are three real answers, and I would take the first.**
>
> **One: partition the leaderboard rather than the data.** Most games do not actually have one global board —
> **they have one per region, per level, per season, per friend group.** Each of those is a *smaller structure*,
> not a *split* one, **and every query stays entirely within it.** This is usually what the product already
> wants, so it is a product fact rather than an engineering compromise — **and it is by far the most common
> answer in practice.**
>
> **Two: exact top N, approximate below.** Keep a bounded sorted set of the top ten thousand, trimmed on every
> write, **so it stays at about a megabyte regardless of how many players exist.** Everyone outside it gets an
> approximate rank.
>
> **Three: a score histogram** — how many players fall in each hundred-point band. **A rank is the sum of the
> buckets above yours.** Ten thousand buckets is two hundred kilobytes, **against ten gigabytes for the exact
> structure — twenty-five thousand times smaller, accurate to within a bucket.**
>
> **And I would argue that the approximation is the better product below the top few hundred.** **'About two
> thousand one hundred of fifty thousand' is more useful than an exact number** that changes every few seconds
> and that nobody can act on. **The interface should show which it is** — 'about' or a precise number — rather
> than implying precision it does not have."

**"Two players have the same score. What order do they appear in?"**

> "By default, an arbitrary one — **and it is arbitrary in a way that is stable and therefore visible, which is
> worse than random.**
>
> **Redis breaks ties lexicographically by member name.** So if members are `player:aaa` and `player:zzz`,
> **`aaa` always ranks above `zzz` at equal score, forever.** Players notice patterns like that, and it looks
> like favouritism rather than a data structure detail.
>
> **So the tie-break has to be a product decision, and then encoded.**
>
> **The usual rule is: on equal score, whoever achieved it first ranks higher** — which rewards being early and
> is what most people expect.
>
> **And the way to implement it is to fold the tie-break into the score itself**, rather than maintaining a
> second structure. **Multiply the real score by a large constant and add an inverted timestamp**, so a lower
> timestamp produces a higher composite.
>
> **Two things I would be careful about, and I would say both.**
>
> **Precision.** A double holds fifty-three bits of exact integer range — **about nine times ten to the
> fifteen.** So if the real score can be a million and I multiply by ten to the ten, I am at ten to the sixteen
> and **I have silently lost precision**, which reorders players in a way nobody will ever diagnose. **I would
> assert the bound rather than assume it**, and pick the scale from the actual maximum score.
>
> **And the displayed score must be the real one**, recovered by integer division — **not the composite**, which
> would put an absurd number on screen. That sounds obvious and is a genuine bug people ship.
>
> **The alternative is to keep the tie-break outside the score** — sort by score in Redis, then re-sort ties by
> timestamp in the application. **That works for the top ten and cannot work for rank**, because the rank query
> happens inside Redis. **So encoding it into the score is the answer whenever rank matters.**"

### The model answer

*"Design the leaderboard for a mobile game: fifty million players, daily, weekly and all-time boards, and each
player must see their own rank."*

> "Let me separate the two questions first, because they have different costs and the design follows from that.
>
> **The top ten is easy in any sorted store. The rank is the hard part** — 'how many players are above me' is a
> count over everyone unless the structure supports it. **And 'each player must see their own rank' is in the
> requirements, so this is a rank problem, not a top-ten problem.**
>
> **Sizing.** Fifty million players at five sessions a day is two hundred and fifty million score updates —
> about three thousand a second, fifteen thousand at peak. **Reads are only about three times that**, which is
> unusually write-heavy for a read-facing feature, **so the write path being cheap matters as much as the read
> path.**
>
> **The structure: Redis sorted sets.** A skip list keeping members in score order, **with spans on the forward
> pointers so rank is the sum of the spans along the search path** — logarithmic, not a count — **plus a hash
> map for constant-time score lookup on update.**
>
> **About a hundred bytes an entry, so five gigabytes for fifty million players**, and every operation is
> fifty to a hundred microseconds. **At peak that is roughly half of one Redis instance** — the data structure
> is comfortably not the bottleneck.
>
> **Windows: a separate sorted set per window, with TTLs.** `daily:2026-09-01` expiring after two days,
> `weekly:2026-W35` after two weeks, `alltime` never. **A score update writes to all of them in one pipelined
> round trip** — three or four times the writes, and every read stays a single lookup. **The TTL removes old
> windows with no cleanup job.**
>
> **And that pushes me to about a hundred and fifty percent of one instance**, so I would **shard by window** —
> daily on one instance, all-time on another. **That is the easy sharding, because no query ever crosses
> windows.** Total memory across all windows is around sixteen gigabytes.
>
> **Best score, not latest**, which most games want — using `ZADD` with `GT` so it is atomic. **Without that,
> reading and then writing is a race, and a late-arriving old submission lowers somebody's score.**
>
> **Ties: encode the tie-break into the score** — the real score times a large constant, plus an inverted
> timestamp, so an earlier achiever wins. **And I would assert the fifty-three-bit precision bound rather than
> assume it**, because exceeding it silently reorders players. **The displayed score is recovered by division;
> the composite never reaches the screen.**
>
> **Durability: the game's database is the source of truth and Redis is the serving structure.** The durable
> write happens first. **A Redis failure costs a ten-minute rebuild** — build into a temporary key, then
> `RENAME`, which is atomic, so the old board serves until the new one is complete. **Ten minutes is fine for a
> leaderboard and would be unacceptable for anything transactional**, which is exactly why this architecture is
> allowed here.
>
> **Two things I would raise unprompted.**
>
> **At a hundred million players, do not shard the sorted set.** **Rank is global, so a split structure makes
> every rank query hit every shard and get slower as you add shards** — the opposite of what sharding is for.
> **Partition the leaderboard by a product dimension instead** — region, level, season — which is a smaller
> structure rather than a split one.
>
> **And I would propose exact-at-the-top, approximate-below as a feature rather than a fallback.** The top ten
> thousand exact in a bounded set — about a megabyte — **and everyone else from a score histogram, which is two
> hundred kilobytes and accurate to a hundred points.** **A thousandth of the memory, and for a player at rank
> two thousand it is arguably the better answer**, because a precise number that changes every few seconds is
> not information they can use. **The interface should say 'about', so the approximation is honest rather than
> hidden.**"

---

## 9. Recall card

**Two questions with different costs, and separating them is the opening move: the TOP TEN is easy in any
sorted store; the RANK is a count over everyone unless the structure supports it.** Almost every naive design
gets the first and fails the second.

**Redis sorted sets — and say what is underneath.** A **skip list with SPANS on the forward pointers** (rank is
the sum of spans along the search path, so `O(log n)` rather than a count) **plus a hash map** for `O(1)` score
lookup on update. **The spans are precisely the feature that makes rank cheap.** ~100 bytes/entry → 50M players
≈ **5 GB**, ~50–100 µs per operation, **about half of one instance at peak.**

**Do NOT shard the sorted set: rank is inherently GLOBAL**, so a split makes every rank query hit every shard
**and get slower as you add shards.** Three better answers: **partition the leaderboard by a product dimension**
(region, level, season — usually what the product wants anyway); **exact top 10,000 in a bounded set** (~1 MB,
trimmed with `ZREMRANGEBYRANK` on every write); **or a score histogram** (~200 KB, **25,000× smaller**, accurate
to a bucket).

**Approximate is the better product below the top few hundred** — "about 2,100th of 50,000" beats a precise
number that changes every few seconds — **and the interface should say "about" rather than imply precision.**

**Ties break lexicographically by member name by default** — stable, arbitrary, and visible. **Encode the
tie-break into the score** (`score × 10^10 + inverted timestamp`), **and assert the 53-bit double precision
bound**, because exceeding it silently reorders players. **Display the real score, never the composite.**

**Windows are separate sorted sets with TTLs** (3–4× write amplification, every read one lookup; shard *by
window*, which is easy because no query crosses them). **"Rolling last 24 hours" has nothing to expire** —
hourly buckets and an hour of granularity is the honest answer. **`ZADD ... GT` makes best-score atomic**;
**`ZREVRANK` is zero-indexed.** **Redis is the serving structure, not the source of truth** — rebuild into a
temp key and `RENAME`, ~10 minutes, which is affordable precisely because it is a leaderboard.
