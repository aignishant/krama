---
day: 154
track: system-design
title: "Design Twitter"
phase: "High-level design case studies"
status: written
---

# Design Twitter

## 1. What this is, and why they ask it

**"Design Twitter" is the most asked system design question there is.** It has been asked at every large
company for a decade, and there is a reason it survived: it is the smallest problem that contains almost
everything.

The product is tiny. **Post a short message. Follow people. See their messages, newest first.** Three verbs,
and every one of them is genuinely hard at three hundred million users.

They ask it because **it is a superset of yesterday's news feed with three additions that change the design.**
The social graph is now a first-class object with its own scaling problem — some accounts have a hundred
million followers and the follower list itself does not fit anywhere convenient. **Search and trends** appear,
which need a completely different index from the timeline. **And there are two timelines, not one** — your
home timeline of people you follow, and a user's own profile timeline, which are stored and served in
different ways for different reasons.

And they ask it because **it is the best available test of scoping.** The full product has direct messages,
lists, spaces, ads, moderation, notifications, media, verification and analytics. **A candidate who tries to
design all of it produces nothing; a candidate who names them, picks three, and goes deep produces a design.**
That choice, made out loud in the first minute, is a large part of what is being assessed.

By the end of this lesson you can scope the problem, design the graph store and both timelines, handle the
celebrity and the fan-out, add search and trending, and size the whole thing.

---

## 2. The story

The wedding hall took bookings a year ahead and the man who ran it, Krishnappa, had one book, and by the time
his daughter took over there were four.

**The first book was the diary**, and it was the only one that had existed for eleven years. One page a day.
Whoever booked, you wrote their name and the phone number and the advance. **It answered exactly one question:
what is happening on the fourteenth of March.**

**The second book came because of the phone calls.** People rang and said "I booked in your hall, what date did
I take?" and Krishnappa would go through the diary page by page until he found them, which took twenty minutes
and sometimes did not work. **So he started a second book, alphabetical by name, saying what each family had
booked.**

Same bookings. Written twice. **Two books because there were two questions**, and one arrangement could not
answer both quickly.

**The third book was his daughter's and it caused an argument.** She started writing down, at the end of each
month, which caterers and which decorators people had asked for. Not for any booking in particular. Just
counts.

Her father said it was a waste of an evening. **Then in November a decorator asked him whether people were
still asking for the old style of mandap, and he did not know, and she did.**

**And the fourth book was the one they never quite got right.** It was for the families who booked the hall
every year — the three or four big families in the town who had a function almost every month, and whose
entries filled so many pages of the diary that looking anything up became slow.

**They tried keeping those families' bookings on their own separate sheets.** Which worked, except that now the
diary was incomplete, and answering "what is happening on the fourteenth" meant checking the diary **and** the
four sheets.

His daughter's summary, which she said to a friend and not to her father, was the useful one.

**"He thinks the book is the bookings. It is not. The book is one way of arranging them, and we needed four,
and the big families broke all of them."**

---

## 3. The idea in plain English

Krishnappa's daughter has described the whole design: **the same data, stored several times, arranged
differently for each question — and the big families break every arrangement.**

**Scope first, because the product is enormous and the interview is forty-five minutes.**

```
IN     post a tweet
       follow / unfollow
       home timeline (people you follow, newest first)
       user timeline (one person's own tweets)
       search
       trending
OUT    direct messages, lists, spaces, ads, moderation,
       analytics, verification, media transcoding
```

**Say the out-of-scope list out loud and move on.** Naming them shows you know the product; designing them
shows you cannot prioritise.

**Now the scale, because it decides everything.**

```
300 million daily active users
each opens the app ~10 times/day    -> 3 billion timeline reads/day
each tweets ~0.1 times/day          -> 30 million tweets/day

read : write = 100 : 1
```

**A hundred reads per write** is the number that justifies doing expensive work at write time, exactly as in
[day 153](../day-153-longest-common-subsequence/README.md).

**The core data model is three things.**

```
tweets(id, author_id, text, created_at, reply_to, ...)
follows(follower_id, followee_id, created_at)
timeline:<user_id>       -- a precomputed list of tweet ids
```

**Tweet ids are Snowflakes** — [day 150](../day-150-coin-change/README.md)'s design — so they sort by time,
which makes "tweets after this id" a range query and makes the timeline's sort order free.

**Now the two timelines, which is Krishnappa's two books.**

**The user timeline** — one person's own tweets, shown on their profile — is a straightforward query:
`SELECT * FROM tweets WHERE author_id = ? ORDER BY id DESC LIMIT 20`. **One index, one query, done.** It is
stored once, sharded by author.

**The home timeline** — everyone you follow, merged — cannot be a query, because it would touch hundreds of
shards. **So it is precomputed and stored separately**, which is the same data arranged differently for a
different question.

**Fan-out on write** builds it: when you tweet, insert the tweet id into each follower's precomputed timeline.
**Reading is then one lookup.**

**And it breaks on the accounts with a hundred million followers**, so: **hybrid.** Under a threshold — ten
thousand followers — fan out on write. Above it, store once and let readers merge. **At read time, take your
precomputed timeline and merge in recent tweets from the celebrities you follow.**

**That is yesterday's design, and Twitter is where it comes from.** The difference today is everything around
it.

**The social graph, which is a real problem of its own.**

`follows` needs to be queried in **both** directions: `followee → followers` for fan-out, `follower →
followees` for the read path. **That is two indexes, or two tables, and at Twitter's size it is a dedicated
service.**

**The hard part is that follower lists are enormously skewed.** Most accounts have under a thousand followers.
A few have over a hundred million — **and a hundred million follower ids at 8 bytes each is 800 MB for one
row's worth of relationship.** That does not fit in a value, cannot be fetched at once, and must be paginated
and streamed during fan-out.

**Sharding the graph is the interesting decision**, and there are two options with a real trade:

- **Shard by follower** makes "who do I follow" a single-shard read — good for the read path, and fan-out has
  to scatter.
- **Shard by followee** makes "who follows this account" single-shard — good for fan-out, and now a celebrity
  is a single hot shard.

**Store both**, which is what real systems do: two denormalised copies, kept consistent asynchronously.
**Krishnappa's two books again.**

**Search, which needs a completely different index.**

**A timeline is ordered by time; search is ordered by relevance and looked up by word.** You cannot serve one
from the other. **So tweets are also written to an inverted index** — [day 135](../day-135-dependency-problems/README.md)'s
structure — mapping each term to the tweet ids containing it.

**And the index is near-real-time, not real-time.** A tweet becomes searchable within seconds, not
milliseconds, because indexing is asynchronous. **That is an accepted product property, not a failure**, and
saying so is better than pretending otherwise.

**The volume is the problem: thirty million tweets a day, each producing perhaps fifteen index entries.**
Search shards by time — recent tweets in a hot index, older ones in cold shards — because almost all queries
are about the last few days.

**Trending, which is a counting problem with a twist.**

**Naive trending is "the most used hashtags in the last hour", and it produces the same words every day** —
the terms that are always popular. **Trending is about the *change* in rate, not the rate.** A term used a
thousand times an hour every day is not trending; a term used five times an hour that is suddenly used four
hundred times is.

**So: count per term per time window, compare against a baseline, and rank by the ratio.** Counting exactly at
this volume is expensive, so **approximate counters — count-min sketch — are the standard answer**, trading a
small overcount for a fixed, tiny amount of memory.

**And the last piece: everything else is a cache.**

**Tweet content, user profiles and engagement counts are all fetched by id after the timeline gives you ids.**
That hydration is one batched multi-get, and it is where the read latency actually lives. **Ninety percent of
reads are for tweets from the last two days**, so a cache holding recent tweets covers almost everything.

---

## 4. The picture

The whole system:

```
                       +--------------+
   write path          |  API GATEWAY |
                       +------+-------+
                              |
        +---------------------+---------------------+
        v                     v                     v
  +-----------+        +-------------+       +-------------+
  | TWEET SVC |        | GRAPH SVC   |       | SEARCH IDX  |
  | (sharded  |        | follows,    |       | (inverted,  |
  |  by tweet |        |  both       |       |  sharded by |
  |  id)      |        |  directions)|       |  time)      |
  +-----+-----+        +------+------+       +-------------+
        |                     ^                     ^
        v                     |                     |
  +-------------+             |            (async indexing)
  | FANOUT SVC  |-------------+
  +------+------+  reads follower list in pages
         |
         v
  [ timeline:u1 ] [ timeline:u2 ] ... Redis sorted sets, capped ~800
         |
   read path
         v
  +---------------+     +-----------------+
  | TIMELINE SVC  | --> | merge celebrity |
  +-------+-------+     | tweets          |
          |             +-----------------+
          v
  +---------------+
  |   HYDRATION   |  one batched multi-get: tweets, users, counts
  +---------------+
```

The two timelines, which are two different books:

```
  USER TIMELINE (profile page)          HOME TIMELINE (the feed)

  "what did @ravi tweet?"               "what did everyone I follow tweet?"

  SELECT * FROM tweets                  cannot be a query — it would
  WHERE author_id = ?                   touch hundreds of shards
  ORDER BY id DESC LIMIT 20
                                        so it is PRECOMPUTED:
  one index, one shard, one query       timeline:<user> as a sorted set
                                        built by fan-out on write
  stored ONCE
                                        stored ONCE PER FOLLOWER

  Same tweets. Two arrangements. Two questions.
```

The follower-list problem, which is specific to Twitter:

```
  follower count distribution (roughly)

  < 1,000 followers      ~95% of accounts
  1,000 - 10,000         ~4%
  10,000 - 1,000,000     ~1%
  > 10,000,000           a few thousand accounts
  > 100,000,000          a few dozen

  ONE account with 100,000,000 followers:
     100,000,000 x 8 bytes = 800 MB just for the ID LIST
     -> cannot be one value, cannot be fetched at once
     -> must be PAGED and STREAMED during fan-out
     -> and fanning out to it would take ~33 minutes at 50k writes/s

  This is why the hybrid exists, and why the graph service is
  its own system rather than a table.
```

Sharding the graph — the trade:

```
  SHARD BY FOLLOWER                  SHARD BY FOLLOWEE

  "who do I follow?"                 "who follows me?"
    -> ONE shard. Fast.                -> ONE shard. Fast.
  "who follows me?"                  "who do I follow?"
    -> SCATTER to all shards           -> SCATTER to all shards

  good for the READ path             good for FAN-OUT
                                     and a celebrity is ONE HOT SHARD

  ANSWER: store both. Two denormalised copies, reconciled
  asynchronously. Twice the storage, and both questions are fast.
```

Search: a different index for a different question:

```
  TIMELINE INDEX                     SEARCH INDEX (inverted)

  key:   user id                     key:   term
  value: [tweet ids, by time]        value: [tweet ids containing it]

  "mumbai rain" -> intersect the posting lists for "mumbai"
                   and "rain", then rank by recency + engagement

  ordered by TIME                    ordered by RELEVANCE
  answers "what is new"              answers "what mentions X"

  Neither can serve the other's query. Both are written on every tweet.
```

Trending: rate of change, not rate:

```
  term          last hour   typical hour   ratio
  ------------------------------------------------
  "the"           850,000      840,000      1.01    not trending
  "cricket"        40,000       38,000      1.05    not trending
  "earthquake"      9,000           30      300.0   TRENDING
  "gujarat"        12,000          400       30.0   TRENDING

  Ranking by COUNT gives you "the" every single day.
  Ranking by count / baseline gives you the news.

  Counting exactly at 30M tweets/day is expensive, so use a
  COUNT-MIN SKETCH: fixed memory, small overcount, never undercounts.
```

---

## 5. How it actually works

### Posting a tweet

```python
def post_tweet(author_id: int, text: str) -> int:
    tweet_id = snowflake.next_id()            # time-sortable, from day 150
    tweet_store.put(tweet_id, author_id, text, time.time())

    queue.publish("fanout", {"tweet_id": tweet_id, "author_id": author_id})
    queue.publish("index",  {"tweet_id": tweet_id, "text": text})
    return tweet_id                           # returns immediately
```

**Three things, and only the first is synchronous.** The tweet is durable before the API returns; fan-out and
indexing happen behind the queue. **So a tweet appears on your own profile instantly and in followers' feeds a
second later**, which is exactly the behaviour users observe.

### Fan-out, with the celebrity check

```python
CELEBRITY_THRESHOLD = 10_000

def handle_fanout(msg: dict) -> None:
    author_id = msg["author_id"]
    if graph.follower_count(author_id) > CELEBRITY_THRESHOLD:
        return                                # read path handles it

    for page in graph.iter_followers(author_id, page_size=1000):
        queue.publish("fanout_batch", {"tweet_id": msg["tweet_id"], "targets": page})
```

**`iter_followers` must stream, not return a list.** A hundred million followers is 800 MB of ids — **calling
`.all()` on that is an out-of-memory error**, and it is the specific reason the graph service exposes a paged
cursor rather than a getter.

```python
def handle_fanout_batch(msg: dict) -> None:
    pipe = redis.pipeline()
    for user_id in msg["targets"]:
        key = f"timeline:{user_id}"
        pipe.zadd(key, {msg["tweet_id"]: msg["tweet_id"]})   # id IS the timestamp
        pipe.zremrangebyrank(key, 0, -801)                   # cap at 800
    pipe.execute()
```

**The score is the tweet id itself**, because Snowflakes sort by time — **no separate timestamp needed**, which
halves the memory of every timeline entry.

### The home timeline read

```python
def home_timeline(user_id: int, cursor: int | None, limit: int = 20) -> list[dict]:
    upper = cursor if cursor is not None else "+inf"
    own = redis.zrevrangebyscore(f"timeline:{user_id}", upper, "-inf",
                                 start=0, num=limit * 3)

    celebs = graph.celebrities_followed(user_id)          # ~30, cached
    extra = [t for c in celebs for t in tweet_store.recent(c, limit, before=cursor)]

    merged = sorted(set(own) | set(extra), reverse=True)[:limit]
    return hydrate(merged)
```

**`sorted(..., reverse=True)` works because ids sort by time**, so merging two id lists needs no timestamp
lookup at all. **That is the Snowflake decision paying off.**

**`zrevrangebyscore` with the cursor as the upper bound is cursor pagination** — "everything below this id" —
which is stable when new tweets arrive between pages.

### The user timeline, which is just a query

```python
def user_timeline(author_id: int, cursor: int | None, limit: int = 20) -> list[dict]:
    return hydrate(tweet_store.by_author(author_id, before=cursor, limit=limit))
```

**One query on an index of `(author_id, tweet_id)`.** No precomputation, no fan-out, nothing clever — **and
this is worth saying explicitly in an interview**, because candidates sometimes try to precompute it too.

### Search indexing

```python
def handle_index(msg: dict) -> None:
    terms = tokenize(msg["text"])             # lowercase, strip punctuation, stem
    shard = search_shard_for(msg["tweet_id"]) # sharded by TIME
    pipe = shard.pipeline()
    for term in set(terms):
        pipe.zadd(f"term:{term}", {msg["tweet_id"]: msg["tweet_id"]})
    pipe.execute()
```

**Sharded by time, not by term**, because almost every query is about recent tweets. **A hot shard holds the
last few days and answers most queries; cold shards hold history and are rarely touched.**

```python
def search(query: str, limit: int = 20) -> list[dict]:
    terms = tokenize(query)
    posting_lists = [shard.zrevrange(f"term:{t}", 0, 999) for t in terms]
    candidates = set.intersection(*map(set, posting_lists))
    ranked = rank_search(candidates, query)[:limit]
    return hydrate(ranked)
```

**Intersecting posting lists is the whole of boolean search**, and taking only the top thousand from each
keeps it bounded — **a common term's full posting list is millions of entries, and nobody scrolls past a few
pages.**

### Trending with a count-min sketch

```python
class CountMinSketch:
    def __init__(self, width: int = 2**16, depth: int = 5) -> None:
        self.table = [[0] * width for _ in range(depth)]
        self.width, self.depth = width, depth

    def add(self, item: str, count: int = 1) -> None:
        for row in range(self.depth):
            self.table[row][self._hash(item, row)] += count

    def estimate(self, item: str) -> int:
        return min(self.table[row][self._hash(item, row)] for row in range(self.depth))

    def _hash(self, item: str, row: int) -> int:
        return hash(f"{row}:{item}") % self.width
```

**`min` over the rows is the trick.** Collisions can only inflate a counter, so **the smallest of `d`
independent estimates is the closest to the truth — it never undercounts.** Five rows of 65,536 counters is
about 1.3 MB, regardless of how many distinct terms exist.

```python
def trending(current: CountMinSketch, baseline: CountMinSketch,
             candidates: list[str], top: int = 10) -> list[str]:
    scored = [(current.estimate(t) / max(baseline.estimate(t), 10), t) for t in candidates]
    return [t for _, t in sorted(scored, reverse=True)[:top]]
```

**Dividing by the baseline is what makes it trending rather than popular.** **`max(baseline, 10)` stops a term
with a baseline of one from scoring infinitely** — a single mention becoming two is not news.

### Hydration

```python
def hydrate(tweet_ids: list[int]) -> list[dict]:
    tweets = tweet_cache.multi_get(tweet_ids)                 # one call
    authors = user_cache.multi_get([t["author_id"] for t in tweets.values()])
    counts = counter_cache.multi_get(tweet_ids)               # one call
    return [build(tweets[i], authors[tweets[i]["author_id"]], counts[i])
            for i in tweet_ids if i in tweets]
```

**Three batched calls, and the `if i in tweets` silently drops deleted tweets** — which is why deletion does
not need to scrub every timeline.

### The real systems

```
Snowflake        Twitter's id generator, now used everywhere
Manhattan        Twitter's distributed key-value store (tweets, users)
FlockDB          the original graph store; "who follows whom" as a service
Earlybird        the real-time search index — Lucene-based, in-memory
Redis            timelines, as sorted sets
Kafka            the event backbone between all of the above
```

**Naming Earlybird is worth doing**, because it is the answer to "how is search real-time" — an in-memory
inverted index over recent tweets, separate from the historical one.

---

## 6. The numbers

**Traffic.**

```
300,000,000 DAU
10 timeline opens/day      -> 3,000,000,000 reads/day = ~35,000/s average
                                                        ~100,000/s peak
0.1 tweets/day             ->    30,000,000 writes/day = ~350/s average
                                                          ~1,000/s peak
search: ~10% of opens      ->   300,000,000 searches/day = ~3,500/s
```

**Fan-out volume.**

```
350 tweets/s x 200 average followers = 70,000 timeline inserts/s
peak: 1,000 x 200                    = 200,000/s

Redis at ~100,000 ops/s per instance
-> 2-4 instances average, ~10 at peak, sharded by user id
```

**And the celebrity, which is why averages mislead:**

```
100,000,000 followers, one tweet

fan-out on write:
  100,000,000 inserts at 50,000/s = 2,000 s = ~33 MINUTES
  and the follower LIST alone is 100,000,000 x 8 B = 800 MB

with the hybrid:
  1 write. Readers merge ~30 celebrity accounts, ~3 ms extra.
```

**Storage.**

```
TWEETS
  30,000,000/day x 300 bytes (text + metadata) = 9 GB/day
  x 365 days                                   = 3.3 TB/year
  x 3 replicas                                 = 10 TB/year
  -> ten years of tweets is ~100 TB. Genuinely small.

TIMELINES
  300,000,000 users x 800 entries x 8 bytes (id only) = 1.9 TB
  x ~2 for Redis sorted-set overhead                  = ~4 TB

  (the id IS the score, so 8 bytes per entry, not 16)

SOCIAL GRAPH
  300,000,000 users x 200 average follows x 16 bytes = 1 TB
  stored BOTH ways                                   = 2 TB

SEARCH INDEX
  30,000,000 tweets/day x 15 terms x 8 bytes = 3.6 GB/day of postings
  x 30 days hot                              = ~108 GB hot index
```

**Tweets are the smallest of these**, which surprises people: **the timelines and the graph are each larger
than the content.** That is what fan-out costs.

**Read latency.**

```
zrevrangebyscore timeline        ~1 ms
fetch ~30 celebrities' recent    ~3 ms
merge (ids sort by time — free)  ~0.5 ms
hydrate: 3 batched multi-gets    ~5 ms
                                 -------
                                 ~10 ms
```

**Cache sizing:**

```
90% of reads hit tweets from the last 48 hours
48 hours = 60,000,000 tweets x 300 B = 18 GB

-> a 32 GB tweet cache covers ~90% of all reads
   at 100,000 reads/s x 20 tweets = 2,000,000 fetches/s
   10% miss = 200,000 store reads/s   <- still the dominant load

moving the hit rate 90% -> 95% HALVES the backing store's load.
```

**Search cost.**

```
3,500 searches/s
each intersects 2-3 posting lists, top 1,000 each
-> ~10,000 list reads/s, plus ranking

the hot index is ~108 GB and must be in memory for this to work
-> ~4-8 machines with 32 GB each, sharded by time
```

**Trending, and why sketches:**

```
exact counting: ~5,000,000 distinct terms per hour
                x (term string ~20 B + counter 8 B) = 140 MB per window
                x 24 windows for the baseline       = 3.4 GB
                and it must be merged across shards

count-min sketch: 5 rows x 65,536 counters x 8 B = 2.6 MB per window
                  x 24 windows                   = 63 MB
                  and sketches MERGE by addition — trivially parallel

~50x less memory, and the error is a small overcount on rare terms,
which do not appear in the top ten anyway.
```

**The merge property is the best argument**: each shard keeps its own sketch and they are summed, which exact
counting cannot do without shipping every key.

---

## 7. The trade-offs

**Fan-out on write against on read, which is the same trade as the news feed and is settled by the same
number.** A hundred reads per write means paying `O(followers)` once beats paying a merge a hundred times.
**And it fails on the hundred-million-follower account, so the hybrid exists** — the threshold is a tuning
parameter, and being able to derive it is what matters.

**Storing the graph twice.** Sharding by follower makes the read path fast and the fan-out a scatter; sharding
by followee makes fan-out fast and the read path a scatter. **Both copies costs twice the storage — about 2 TB,
which is nothing — and buys both queries.** The real cost is consistency: the two copies are reconciled
asynchronously, so for a moment after a follow, one direction knows and the other does not.

**Timelines are stale by design.** A precomputed timeline reflects the world as of the last fan-out, so a
tweet from a second ago may not be there. **Users do not notice, and it is worth saying plainly** rather than
pretending the system is synchronous.

**Search is near-real-time, not real-time.** Indexing is asynchronous, so a tweet is searchable in seconds.
**Making it synchronous would put the index on the write path** and mean a tweet fails if the index is slow —
**a much worse property than a two-second delay.**

**Approximate trending against exact counting.** A count-min sketch is fifty times smaller, merges across
shards by addition, and **overcounts rare terms slightly.** Since rare terms are not in the top ten, the error
is invisible where it matters. **Exact counting would need every distinct term's counter shipped between
shards on every merge.**

**The timeline cap trades completeness for bounded storage.** Eight hundred entries per user is about 4 TB;
uncapped is unbounded. **A user scrolling past the cap falls back to the slow path**, which is rare and
therefore fine.

**And the honest one: this design is Twitter in 2013, not Twitter now.** The real system has ranking, ads
interleaved, conversation threading, quality filtering and a recommendation system that surfaces tweets from
people you do not follow. **Ranking in particular changes the read path substantially** — it means fetching
several hundred candidates and scoring them — and it makes pagination much harder.

**When would I not build this?** **Almost always.** Below a million users, the entire product is a Postgres
database with a `follows` table and a query with a join, and it will be fast, correct and maintainable.
**Building the fan-out infrastructure first is the classic mistake this question tempts people into** — and
saying that, briefly, at the end, is a stronger signal than another component.

---

## 8. In the interview

### How it gets asked

- *"Design Twitter."* — usually exactly that, with no further constraints.
- *"How does the home timeline work?"* — the fan-out question.
- *"What about someone with a hundred million followers?"*
- *"How would you add search?"* — the different-index question.
- *"How does trending work?"*
- *"What would you cut if you had ten minutes?"* — the scoping question, sometimes asked directly.

### The first ninety seconds

> "The product is huge, so let me scope first and then size, because both change what I build.
>
> **In scope: post a tweet, follow, home timeline, user timeline, search, trending. Out of scope: direct
> messages, lists, ads, moderation, media, analytics** — real, and not what makes this interesting.
>
> **The number that decides the architecture:** three hundred million daily users opening the app ten times is
> three billion timeline reads a day. They tweet about a tenth of a time each, so thirty million tweets.
> **A hundred reads per write** — so it is worth doing expensive work at write time.
>
> **There are two timelines and they are built completely differently, which is the first thing I would
> establish.**
>
> **The user timeline** — someone's own tweets on their profile — is a query. Select by author, order by id
> descending, limit twenty. **One index, one shard, done.** No precomputation.
>
> **The home timeline cannot be a query**, because merging hundreds of authors' tweets would touch hundreds of
> shards on every read. **So it is precomputed by fan-out on write:** when you tweet, the tweet id is inserted
> into each follower's timeline, stored as a Redis sorted set. **Reading is then one lookup — about ten
> milliseconds end to end.**
>
> **Tweet ids are Snowflakes**, which is worth calling out because it does two jobs: the ids sort by time, so
> the timeline needs no separate timestamp — **the id is the score** — and merging two id lists needs no
> lookups at all.
>
> **And fan-out breaks on the celebrity.** A hundred million followers means a hundred million inserts, about
> thirty-three minutes, **and the follower id list alone is 800 megabytes**, which cannot even be fetched at
> once. **So: hybrid.** Under ten thousand followers, fan out on write. Above, store once, and readers merge in
> the twenty or thirty celebrity accounts they follow.
>
> **Search and trending need different structures entirely**, which I would flag now: **a timeline is indexed
> by user and ordered by time; search is indexed by term and ordered by relevance.** Neither can serve the
> other, so every tweet is written to both.
>
> **Where would you like me to go deep — the fan-out and the graph, or search and trending?**"

### The follow-ups

**"Someone with a hundred million followers tweets. What happens?"**

> "Under pure fan-out on write, two things break, and the second one is the more interesting.
>
> **The obvious one: a hundred million sorted-set inserts.** At fifty thousand writes a second that is two
> thousand seconds — **about thirty-three minutes** — during which the last follower has not seen it and the
> fan-out pipeline is doing nothing else. Everyone else's tweets queue behind it.
>
> **The less obvious one: the follower list itself.** A hundred million ids at eight bytes each is **eight
> hundred megabytes**, for one account's followers. **That is not a value you can fetch** — calling something
> like `get_followers()` on it is an out-of-memory error. So the graph service has to expose a paged cursor,
> and fan-out streams through it a thousand at a time. **That constraint alone is why the graph is its own
> service rather than a table with an index.**
>
> **The fix is the hybrid.** Above a threshold, the tweet is stored once and nothing is pushed. At read time,
> I take my precomputed timeline and separately fetch recent tweets from the celebrities I follow — typically
> twenty or thirty accounts — and merge.
>
> **The asymmetry is what makes it work: the number of celebrities I follow is small even though the number of
> people following them is enormous.** And the merge is nearly free because the ids sort by time, so merging
> two id lists is a sort of eighty integers.
>
> **Two refinements.** **The celebrity list per user must be cached**, or 'which of the people I follow are
> above the threshold' becomes a join on every read.
>
> **And the threshold does not need to be a cliff.** An account with fifteen thousand followers could fan out
> only to followers who opened the app today — instant delivery for the people who will actually see it soon,
> and a bounded write cost. **The number itself is a tuning parameter; what matters is why there is one at
> all.**"

**"How would you add search?"**

> "With a completely different index, and I would say that first because it is the whole answer.
>
> **The timeline is keyed by user and ordered by time. Search is keyed by term and ordered by relevance.**
> Neither structure can answer the other's question, so **every tweet is written to both** — the same data
> arranged twice.
>
> **The search index is an inverted index**: for each term, a list of the tweet ids containing it. A query for
> 'mumbai rain' fetches both posting lists and intersects them, then ranks the survivors by recency and
> engagement.
>
> **Bounded, though: I take only the top thousand ids from each list.** A common term's full posting list is
> millions of entries, and nobody paginates that far — so the intersection is over a bounded set.
>
> **Sharding is by time, not by term**, and that is the decision worth defending. Almost every search is about
> the last few days, so **a hot in-memory index over recent tweets answers most queries, and cold shards hold
> history and are rarely touched.** Sharding by term instead would put 'the' on one machine and make it a hot
> spot.
>
> **Indexing is asynchronous, so search is near-real-time — seconds, not milliseconds.** I would state that as
> a deliberate property rather than let it be discovered: **making it synchronous would put the index on the
> write path**, so a tweet would fail if the index were slow. **A two-second delay is a much better property
> than that.**
>
> **Sizing: thirty million tweets a day at about fifteen index terms each is 3.6 GB of postings a day**, so a
> thirty-day hot index is roughly a hundred gigabytes and needs to be in memory — four to eight machines.
>
> **Twitter's real system is called Earlybird**, an in-memory Lucene index over recent tweets, kept separate
> from the historical one. **The split between a small hot index and a large cold one is the design**, and it
> follows directly from the query distribution."

**"How does trending work?"**

> "The naive version produces the same words every single day, and understanding why is most of the answer.
>
> **If I rank hashtags by count in the last hour, I get 'the', 'a', and whatever is permanently popular** —
> cricket, a big film — because those terms are always used a lot. **They are popular, not trending.**
>
> **Trending is about the rate of change, not the rate.** A term used a thousand times an hour every day is
> not news. A term used thirty times an hour that is suddenly used nine thousand times **is** news. **So I
> score by the ratio of the current window's count to a baseline** — the same term's typical count for this
> hour of this day of the week — and rank by that.
>
> **The baseline needs to be seasonal**, because 'good morning' spikes every morning and is not news, and a
> flat all-time average would report it daily.
>
> **Counting is the expensive part.** There are maybe five million distinct terms an hour, and exact counting
> means a counter per term per window — a few hundred megabytes per window, times twenty-four windows for the
> baseline, **and it has to be merged across every shard.**
>
> **So: a count-min sketch.** A fixed grid of counters, `d` hash functions; to add a term, increment one
> counter per row; to estimate, **take the minimum across the rows.** The minimum works because collisions can
> only inflate a counter, so the smallest of several independent estimates is the closest to the truth — **and
> it never undercounts.**
>
> **Five rows of sixty-five thousand counters is about 2.6 megabytes**, regardless of how many distinct terms
> exist. **Fifty times smaller than exact counting.**
>
> **And the property that actually sells it: sketches merge by addition.** Each shard keeps its own and they
> are summed — trivially parallel. **Exact counting would need every distinct key shipped between shards on
> every merge.**
>
> **The error is a small overcount, worst on rare terms** — and rare terms are not in the top ten, so it is
> invisible where it matters.
>
> **Two things I would add for a real product.** **A separate list of candidate terms**, because I need
> something to estimate — the sketch tells me a count for a term I name, not what the top terms are, so I keep
> a heavy-hitters structure alongside. **And filtering**, because trending is a highly visible surface and
> people deliberately try to game it — which is a moderation problem, not an algorithmic one, and I would name
> it rather than pretend the ranking solves it."

### The model answer

*"Design Twitter."*

> "Let me scope, size, then design, and I will say what I am leaving out so it is clear it is a choice.
>
> **In: tweeting, following, the home timeline, the user timeline, search, trending. Out: DMs, lists, ads,
> media, moderation, analytics.**
>
> **Sizing.** Three hundred million daily users, ten opens each — three billion timeline reads a day, about
> thirty-five thousand a second, a hundred thousand at peak. Thirty million tweets a day, about three hundred
> and fifty a second. **A hundred to one, which is what justifies fan-out on write.**
>
> **Ids are Snowflakes**, and that decision pays for itself three times: ids sort by time, so a timeline needs
> no separate score; merging two id lists needs no lookups; and 'tweets after this id' is a range query, which
> is my pagination cursor.
>
> **Two timelines, built differently.** The user timeline is a query by author on a `(author_id, tweet_id)`
> index — nothing clever, and I would say that explicitly because it is tempting to precompute it too. **The
> home timeline is precomputed** by fan-out into a Redis sorted set per user, **capped at eight hundred
> entries**, with the tweet id as both member and score.
>
> **Hybrid fan-out at a ten-thousand-follower threshold**, because a hundred-million-follower account would
> take thirty-three minutes to fan out and its follower list alone is eight hundred megabytes — **which is why
> the graph service exposes a streaming cursor rather than a getter.**
>
> **The graph is stored twice, sharded both ways.** Follower-to-followee for the read path, followee-to-
> follower for fan-out. **Two terabytes, which is nothing, and it makes both questions single-shard.** The
> cost is that the two copies reconcile asynchronously, so for a moment after a follow, one direction knows
> and the other does not — **acceptable here, and worth naming.**
>
> **Search is a separate inverted index, sharded by time**, with a hot in-memory index over recent tweets. Every
> tweet is written to both structures. **Indexing is asynchronous — near-real-time, seconds not milliseconds —
> because putting the index on the write path would mean a tweet fails when the index is slow.**
>
> **Trending is a count-min sketch per time window, scored against a seasonal baseline**, because ranking by
> raw count returns 'the' every day. Sketches are 2.6 megabytes each and **merge across shards by addition**,
> which is the property that makes them the right choice rather than just a smaller one.
>
> **The read path ends in hydration: three batched multi-gets** — tweets, authors, engagement counts — not
> sixty round trips. **Ninety percent of reads are for tweets from the last forty-eight hours**, which is
> eighteen gigabytes, so a thirty-two gigabyte cache covers almost everything. **At this scale, moving the hit
> rate from ninety to ninety-five percent halves the backing store's load** — worth more than most
> architectural changes.
>
> **Storage, and one number that surprises people: tweets are the smallest thing here.** Three hundred bytes
> each, thirty million a day, is 3.3 terabytes a year — ten years is about a hundred terabytes. **The timelines
> are four terabytes and the graph is two.** The derived data is larger than the content, and that is what
> fan-out costs.
>
> **Two honest closing points.**
>
> **This is Twitter around 2013, not Twitter now.** The real system ranks the timeline, interleaves ads,
> threads conversations, and recommends tweets from people you do not follow. **Ranking in particular changes
> the read path** — several hundred candidates fetched and scored — and makes pagination much harder, because
> the cursor has to pin a ranking session or page two repeats page one.
>
> **And I would not build this for a new product.** Below about a million users, a `follows` table and a query
> with a join is the entire home timeline, and it is fast and correct and one person can maintain it.
> **Everything here is what you build when that stops working, and knowing when that is is more valuable than
> knowing how to build it.**"

---

## 9. Recall card

**Scope out loud first** (in: tweet, follow, both timelines, search, trending; out: DMs, lists, ads, media,
moderation) — **that choice is a large part of what is assessed.** Then size: **3B reads / 30M writes a day =
100:1**, which justifies fan-out on write.

**Two timelines, built differently.** **User timeline is just a query** on `(author_id, tweet_id)` — do not
precompute it. **Home timeline is precomputed** into a Redis sorted set per user, capped ~800, **with the
Snowflake id as both member and score** so it needs no timestamp and merging is free.

**Hybrid fan-out at ~10,000 followers.** A 100M-follower account = **~33 minutes of inserts, and an 800 MB
follower id list** that cannot be fetched at once — which is why the graph service streams a paged cursor.
**Store the graph BOTH ways** (by follower and by followee, ~2 TB total), so both questions are single-shard;
the copies reconcile asynchronously.

**Search needs a different index entirely** — inverted, keyed by term, **sharded by time** so a hot in-memory
index over recent tweets answers most queries. **Asynchronous, so near-real-time**: putting it on the write
path would make a tweet fail when the index is slow.

**Trending is rate of change, not rate** — ranking by count returns "the" every day. **Count-min sketch**
(min across rows, never undercounts, 2.6 MB) scored against a **seasonal baseline**; the killer property is
that **sketches merge across shards by addition**.

**Hydrate in 3 batched multi-gets** (~10 ms end to end). **Tweets are the smallest data here** — 3.3 TB/year
against 4 TB of timelines and 2 TB of graph. **And below ~1M users this is a `follows` table and a join** —
building the fan-out first is the mistake the question tempts you into.
