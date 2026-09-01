---
day: 153
track: system-design
title: "Design a news feed"
phase: "High-level design case studies"
status: written
---

# Design a news feed

## 1. What this is, and why they ask it

A news feed is the home screen of every social product: **you open the app and see recent posts from the
people you follow, newest first.**

They ask it because **it is the canonical read-heavy fan-out problem**, and it has exactly one central
decision with two defensible answers. **Do you build each person's feed when they write, or when someone
reads?** Push or pull. Fan-out on write or fan-out on read. **Almost the entire interview is that question and
its consequences.**

And the reason it is a genuine decision rather than a lookup is that **both answers break, in opposite
directions.** Fan-out on write gives instant reads and collapses when someone with fifty million followers
posts — one write becomes fifty million. Fan-out on read scales beautifully for writers and makes every read
query hundreds of timelines and merge them. **The real answer is a hybrid, and being able to say exactly where
the boundary sits, and why, is what is being tested.**

The other reason is the read-to-write ratio, which is more extreme here than anywhere else in this course.
**A social product sees something like a hundred reads per write.** That single number justifies doing
expensive work at write time, and a candidate who computes it before choosing is answering the question the
right way round.

By the end of this lesson you can choose and defend the fan-out strategy, handle the celebrity problem, design
the cache layout and the ranking pipeline, handle pagination correctly, and size the whole thing.

---

## 2. The story

The noticeboard outside the milk booth had been there longer than anyone could remember, and there was a
system, of sorts, and it had a problem.

**The system was that if you wanted people to know something, you wrote it and pinned it up.** The tuition
class, the lost cat, the plumber's number, the flat for rent on the second floor of C block.

And people came past in the morning and read it.

**The trouble was that it was one board and there were nine buildings.**

So a woman called Prameela, who ran the tuition class and therefore cared more than most, started doing
something extra. **When she pinned a notice on the main board, she also wrote out four more copies and pinned
one at each of the four buildings furthest from the booth.**

It was more work for her. Twenty minutes instead of two.

**And it meant that everyone in those buildings saw it without walking anywhere.** They looked at their own
board, which was ten steps from their door, and everything relevant was already on it.

That worked, and within a year most people were doing it, and the boards were full and current and nobody had
to walk to the milk booth to find out anything.

**Then the temple committee started putting up notices.**

Because the temple concerned everybody — all nine buildings, about four hundred families — **one notice meant
writing out nine copies and walking to nine boards**, and the man who did it, who was seventy-one, took an
entire morning over it. And the temple put up something most weeks.

**So they stopped.** The committee's notices went on the main board only, and there was a line at the top of
every other board that said, in Prameela's handwriting, **"for temple notices see the main board."**

Which meant the temple's readers walked, and everybody else's did not.

**And it was the right answer, and nobody had planned it.** The people with four readers copied their notices
outward, because it was cheap. **The people with four hundred readers did not, because it was not**, and their
readers accepted one extra walk.

---

## 3. The idea in plain English

Prameela invented fan-out on write, the temple committee forced the hybrid, and the line at the top of every
board is the merge step.

**First the numbers that make this a design problem at all.**

**A social feed is read far more than it is written** — something like a hundred to one. People open the app
constantly and post rarely. **So it is worth doing a lot of work at write time to make reads cheap**, and that
asymmetry is the first thing to say.

**Now the central decision, and there are two ways to build a feed.**

**Fan-out on write, also called push.** When you post, the system immediately writes your post's id into the
precomputed feed of every one of your followers. **Reading a feed is then one lookup of an already-assembled
list** — a few milliseconds, no joins, no merging.

**That is Prameela copying her notice to four boards.** Expensive when she writes, free when anyone reads.

**Fan-out on read, also called pull.** Nothing happens at write time beyond storing the post. When you open
the app, the system looks up everyone you follow, fetches their recent posts, merges them by time, and returns
the top few.

**That is walking to the milk booth.** Free to write, expensive to read, and the expense is paid by every
reader every time.

**The comparison, stated plainly:**

```
                    fan-out on WRITE          fan-out on READ
  write cost        O(followers)              O(1)
  read cost         O(1)                      O(following) queries + merge
  read latency      ~5 ms                     ~200-500 ms
  storage           one entry per follower    none extra
  a celebrity posts 50,000,000 writes         nothing
  you follow 5,000  nothing special           5,000 queries per refresh
```

**Given a hundred-to-one read-to-write ratio, fan-out on write is right for almost everybody** — you pay once
per post to make a hundred reads free.

**And it breaks completely on one input: the account with tens of millions of followers.**

**One post becoming fifty million writes is the celebrity problem**, and the numbers are brutal. At fifty
thousand writes a second sustained, fifty million writes takes about seventeen minutes — **so the last
follower sees the post seventeen minutes after the first**, and during those seventeen minutes the write
pipeline is doing nothing else.

**The fix is the hybrid, and it is exactly what the noticeboards converged on.**

- **Normal accounts — say under ten thousand followers — fan out on write.** Their posts land in followers'
  precomputed feeds immediately.
- **Celebrity accounts fan out on read.** Their posts are stored once and nothing is pushed.
- **When you open the app, you read your precomputed feed and separately fetch recent posts from the handful
  of celebrities you follow, then merge the two by time.**

**That merge is Prameela's line at the top of the board**, and it is cheap because you follow at most a few
dozen celebrities, not a few thousand.

**The threshold is a tuning parameter, not a principle.** Ten thousand is a common choice. **What matters is
being able to say why there is a threshold at all**: below it, `O(followers)` writes are cheaper than making
every reader merge; above it, they are not.

**Now the storage, which follows from the choice.**

**The precomputed feed is a list of post ids, not post contents.** Storing the content in every follower's
feed would multiply the data by the follower count — **a 1 KB post with a thousand followers becomes a
megabyte.** Storing ids is 8 bytes each, and the contents are fetched once from a shared store and cached.

**And the feed is capped.** Keep the most recent 500 or 1,000 ids per user and discard the rest. **Nobody
scrolls past a few hundred posts**, and an uncapped feed grows forever. If someone does scroll past the cap,
fall back to the read-path query for the older material.

**Redis sorted sets are the natural structure**: score is the timestamp, member is the post id, and
`ZREVRANGE` gives the newest `n` in one call, with `ZREMRANGEBYRANK` doing the capping.

**Then ranking, because a modern feed is not chronological.**

**Chronological is simple and honest and produces a worse feed**, because the newest post is not the most
interesting one. **Ranked feeds score candidates** by predicted engagement — how likely you are to like,
comment or dwell — using features like the author's affinity with you, the post's age, its early engagement
rate, and its type.

**The pipeline is: candidates → features → score → filter → return.** Typically a few thousand candidates are
scored to produce twenty results, and it happens in under two hundred milliseconds.

**And ranking makes pagination hard**, which is the practical detail people miss. **Offset-based pagination
breaks on a changing feed**: new posts arrive between page one and page two, everything shifts down, and the
user sees a post they already saw. **Cursor-based pagination** — "give me what comes after this post id" — is
correct, and for a ranked feed the cursor must encode the ranking session so page two is scored consistently
with page one.

**Finally, the things that go wrong at the edges.**

**Deleting a post** means removing it from every feed it was pushed to — expensive, so most systems **filter at
read time instead**: check the post still exists and is visible when hydrating, and let the stale id sit in the
feed harmlessly.

**Unfollowing** has the same shape: rather than scrubbing every pushed entry, filter at read.

**A new user's feed is empty**, and an empty home screen is the worst possible first impression. **Seed it**
with popular posts from their stated interests or their location until they follow enough people.

**And the read path always ends with hydration**: the feed gives you ids, and you fetch the actual posts,
authors and engagement counts in one batched call. **That batch is the difference between one round trip and
five hundred.**

---

## 4. The picture

The two strategies:

```
  FAN-OUT ON WRITE (push)

  user posts ---> [ post store ]
                       |
                       v
              +-------------------+
              | FANOUT WORKER     |  reads follower list
              +---------+---------+
                        |
     +------------+-----+------+------------+
     v            v            v            v
  feed:u1      feed:u2      feed:u3  ...  feed:u900
  (Redis sorted set per follower, capped at ~800 ids)

  READ: ZREVRANGE feed:u1 0 19   -> 20 ids -> hydrate -> done. ~5 ms.


  FAN-OUT ON READ (pull)

  user posts ---> [ post store ]    and nothing else happens.

  READ: get the 500 accounts u1 follows
        -> 500 queries for recent posts
        -> merge by timestamp
        -> take the top 20
        -> hydrate
        ~200-500 ms, every single time.
```

The hybrid, which is what actually gets built:

```
                       followers > 10,000?
                       /                \
                    no                    yes
                     |                     |
          FAN OUT ON WRITE          STORE ONLY, no fanout
          push to every              (the "celebrity" path)
          follower's feed
                     \                     /
                      \                   /
                       v                 v
          READ TIME:   [ my precomputed feed  ]
                     + [ recent posts from the
                         ~30 celebrities I follow ]
                     -> MERGE by time/score
                     -> top 20
                     -> hydrate

  The merge is cheap because you follow ~30 celebrities, not ~3,000.
```

The celebrity problem, quantified:

```
  account with 50,000,000 followers posts once

  fan-out on write:
     50,000,000 sorted-set inserts
     at 50,000 writes/second sustained
     = 1,000 seconds = ~17 MINUTES

     -> the first follower sees it instantly
     -> the last follower sees it 17 minutes later
     -> and for those 17 minutes the fanout pipeline does nothing else

  fan-out on read for that one account:
     1 write. Readers merge in ~5 ms extra.
```

The feed entry, and why it holds ids:

```
  WRONG: store the post CONTENT in every feed

     post = 1 KB
     1,000 followers
     -> 1 MB written per post
     -> 1 billion posts/day x 1 KB x 1,000 = 1 PB/day

  RIGHT: store the post ID

     8 bytes (post id) + 8 bytes (score) = 16 bytes
     1,000 followers -> 16 KB per post
     -> 64x less, and the content is stored ONCE and cached
```

The read path, end to end:

```
  GET /feed?cursor=...
      |
      v
  [ my feed ]  ZREVRANGE feed:u1 0 19        ~1 ms
      +
  [ celebrities ] recent posts from ~30       ~3 ms
      |
      v
  MERGE + RANK                                ~2 ms
      |
      v
  FILTER  deleted? blocked? already seen?     ~1 ms
      |
      v
  HYDRATE  ONE batched multi-get for
           20 posts + authors + counts        ~5 ms
      |
      v
  ~12 ms total

  Without batching, hydration is 20 x 3 = 60 round trips.
  The batch is the difference between 5 ms and 200 ms.
```

Why offset pagination breaks:

```
  page 1 (offset 0, limit 5):   [P10 P9 P8 P7 P6]
     user reads them.
     THREE NEW POSTS ARRIVE:    P13 P12 P11
  page 2 (offset 5, limit 5):   [P8 P7 P6 P5 P4]
                                  ^^^^^^^^^^
                       P8, P7 and P6 are shown AGAIN.

  CURSOR: "give me what comes after P6"
  page 2:                       [P5 P4 P3 P2 P1]
  correct regardless of what arrived in between.
```

---

## 5. How it actually works

### The data model

```
users(id, name, ...)
follows(follower_id, followee_id, created_at)        -- indexed BOTH ways
posts(id, author_id, content, created_at, ...)       -- id is a Snowflake
feed:<user_id>                                       -- Redis sorted set
```

**`follows` needs an index in both directions.** `followee_id → followers` for fan-out; `follower_id →
following` for the read path and the celebrity merge. **One index gives you half the system.**

**And post ids are Snowflakes** — [day 150](../day-150-coin-change/README.md)'s design — because a
time-sortable id means the feed's sort order is the id order, and "posts after this id" is a range query.

### Fan-out on write

```python
CELEBRITY_THRESHOLD = 10_000
FEED_CAP = 800

def on_post_created(post_id: int, author_id: int, created_at: float) -> None:
    follower_count = follow_store.count_followers(author_id)
    if follower_count > CELEBRITY_THRESHOLD:
        return                                # celebrity: read path handles it

    for batch in follow_store.iter_followers(author_id, batch_size=1000):
        queue.publish("fanout", {"post_id": post_id, "at": created_at,
                                 "targets": batch})
```

**Each batch of a thousand becomes its own queue message**, so the work parallelises and a crash costs one
batch. **This is exactly the notification fan-out shape** from
[day 152](../day-152-longest-increasing-subsequence/README.md).

```python
def handle_fanout_batch(msg: dict) -> None:
    pipe = redis.pipeline()
    for user_id in msg["targets"]:
        key = f"feed:{user_id}"
        pipe.zadd(key, {msg["post_id"]: msg["at"]})
        pipe.zremrangebyrank(key, 0, -(FEED_CAP + 1))   # keep newest 800
    pipe.execute()
```

**`zremrangebyrank(key, 0, -801)` is the cap**, removing everything except the newest 800. **Without it, a
feed grows forever** — a user following active accounts for five years accumulates millions of ids they will
never scroll to.

**The pipeline batches the round trips**: a thousand users is two thousand commands in one network call, not
two thousand calls.

### The read path

```python
def get_feed(user_id: int, cursor: str | None, limit: int = 20) -> list[dict]:
    own = redis.zrevrange(f"feed:{user_id}", 0, limit * 3 - 1, withscores=True)

    celebrities = follow_store.celebrities_followed(user_id)      # ~30, cached
    extra = []
    for celeb_id in celebrities:
        extra.extend(post_store.recent(celeb_id, limit=limit))

    merged = merge_by_score(own, extra)
    ranked = rank(user_id, merged)[:limit]
    return hydrate(ranked)                    # ONE batched fetch
```

**`limit * 3` over-fetches deliberately**, because filtering will drop some — deleted posts, blocked authors,
already-seen items — and a second round trip to top up is worse than fetching sixty and keeping twenty.

**`celebrities_followed` is cached per user** and changes rarely; recomputing it on every refresh would be a
join on every read.

### Hydration, which is where the latency actually goes

```python
def hydrate(entries: list[tuple[int, float]]) -> list[dict]:
    post_ids = [post_id for post_id, _ in entries]
    posts = post_cache.multi_get(post_ids)                  # one call
    author_ids = {p["author_id"] for p in posts.values()}
    authors = user_cache.multi_get(list(author_ids))        # one call
    counts = counter_cache.multi_get(post_ids)              # one call
    return [build(posts[i], authors[posts[i]["author_id"]], counts[i])
            for i in post_ids if i in posts]
```

**Three batched calls, not sixty individual ones.** `if i in post_ids if i in posts` also silently drops
deleted posts — **which is the read-time filter that saves you from scrubbing every feed on delete.**

### Cursor pagination

```python
import base64, json

def make_cursor(last_score: float, last_id: int, session: str) -> str:
    return base64.urlsafe_b64encode(
        json.dumps({"s": last_score, "i": last_id, "sess": session}).encode()).decode()

def parse_cursor(cursor: str) -> dict:
    return json.loads(base64.urlsafe_b64decode(cursor))
```

**The cursor carries the score and the id of the last item returned**, so page two is "everything below this
score" rather than "skip twenty" — correct even when new posts arrive in between.

**And `sess` is the ranking session**, which matters for a ranked feed: **without it, page two is scored with a
fresher model or fresher engagement counts and can contain items that were on page one.**

### Ranking

```python
def rank(user_id: int, candidates: list) -> list:
    features = feature_store.batch(user_id, [c.post_id for c in candidates])
    scores = model.predict(features)          # p(engage), from a trained model
    for candidate, score in zip(candidates, scores):
        age_hours = (time.time() - candidate.created_at) / 3600
        candidate.final = score / ((age_hours + 2) ** 1.5)   # time decay
    return sorted(candidates, key=lambda c: -c.final)
```

**The time decay is the part worth explaining**: a raw engagement score would let a two-day-old viral post
outrank everything new forever. **Dividing by a power of age keeps the feed fresh**, and the exponent is the
knob between "recent" and "good".

**`+2` in the denominator stops brand-new posts from being divided by nearly zero** and dominating absolutely.

### The real systems

```
Twitter/X       hybrid; the original "Timelines at Scale" talk is the
                reference for this whole design
Facebook        heavily ranked, pull-leaning with aggressive caching
Instagram       fan-out on write into Cassandra, ranked at read time
LinkedIn        hybrid, with Kafka driving the fanout
Redis           sorted sets are the standard feed store everywhere
```

**Naming Twitter's hybrid explicitly is expected**, because it is the design the question is drawn from.

---

## 6. The numbers

**The ratio that justifies everything.**

```
300 million daily active users
each opens the app ~10 times a day        = 3,000,000,000 feed reads/day
each posts ~0.1 times a day               = 30,000,000 posts/day

read : write = 100 : 1
```

**A hundred reads per write is why you do expensive work at write time**, and it is the first number to
compute.

```
3,000,000,000 / 86,400 = ~35,000 feed reads/second average
peak ~3x                = ~100,000 reads/second

30,000,000 / 86,400     = ~350 posts/second average
peak                    = ~1,000 posts/second
```

**Fan-out volume.**

```
350 posts/second x average 200 followers = 70,000 feed inserts/second
peak: 1,000 x 200                        = 200,000 inserts/second

Redis: ~100,000 ops/second per instance
-> 2-4 instances at average, ~10 at peak, sharded by user id
```

**And the celebrity case, which is why the average is misleading:**

```
one account with 50,000,000 followers

fan-out on write:
  50,000,000 inserts at 50,000/s = 1,000 s = ~17 minutes
  and the whole pipeline is blocked on it

with a 10,000 threshold:
  ~0.1% of accounts are above it
  but they produce a large share of the posts people read
  -> those posts cost 1 write each and ~5 ms extra at read time
```

**Storage for the feeds.**

```
300,000,000 users
800 entries each
16 bytes per entry (8-byte post id + 8-byte score)

300,000,000 x 800 x 16 B = 3.84 TB
+ Redis overhead (~2x for sorted sets)  = ~8 TB

-> ~80 Redis instances of 100 GB, or fewer larger ones
   at ~$0.05/GB/hour for managed Redis: ~$25,000-30,000/month
```

**And the comparison that justifies storing ids:**

```
storing post CONTENT in each feed instead (1 KB average):
  300,000,000 x 800 x 1 KB = 240 TB
  -> 30x more, and every edit to a post would need 800 updates

storing ids: 8 TB, content stored once and cached.
```

**Read latency, broken down.**

```
fan-out on write path:
  ZREVRANGE own feed                    ~1 ms
  fetch ~30 celebrities' recent posts   ~3 ms
  merge + rank 60 candidates            ~2 ms
  filter                                ~1 ms
  hydrate (3 batched multi-gets)        ~5 ms
                                        -------
                                        ~12 ms

fan-out on read path (if you followed 500 people):
  500 queries for recent posts          ~150 ms (batched, parallel)
  merge 500 x 20 = 10,000 candidates    ~20 ms
  rank + hydrate                        ~10 ms
                                        -------
                                        ~180 ms, EVERY read
```

**Fifteen times slower on every one of a hundred reads per write.** That comparison is the argument.

**Hydration, and why batching is not optional:**

```
20 posts, hydrated individually
  20 posts + 20 authors + 20 counters = 60 round trips
  at 0.5 ms each                      = 30 ms

batched into 3 multi-gets
  3 round trips at ~1.5 ms each       = 4.5 ms

~7x faster, and it is one line of code.
```

**Cache sizing for post content.**

```
30,000,000 posts/day, and reads are heavily skewed to recent posts
  ~90% of reads hit posts from the last 48 hours

48 hours of posts = 60,000,000 posts x 1 KB = 60 GB
-> one 100 GB cache covers ~90% of all reads

at a 90% hit rate:
  100,000 reads/s x 20 posts = 2,000,000 post fetches/second
  10% miss = 200,000 database reads/second   <- still a lot
  -> a second cache layer, or a higher hit rate, matters enormously here
```

**That last line is worth saying**: at this scale, moving the hit rate from 90% to 95% halves the database
load.

---

## 7. The trade-offs

**Fan-out on write against on read, which is the whole design.** Write costs `O(followers)` and makes reads a
single lookup at about 12 ms. Read costs nothing to write and makes every read query hundreds of timelines at
about 180 ms. **At a hundred-to-one read ratio, write wins decisively** — and it fails completely on the
celebrity, where one post becomes fifty million writes and seventeen minutes.

**So: hybrid, and the threshold is a tuning parameter rather than a truth.** Below it, `O(followers)` writes
are cheaper than making every reader merge; above it, they are not. **Ten thousand is conventional; the number
matters less than being able to derive it.**

**Chronological against ranked.** Chronological is simple, predictable, explicable to users, and produces a
worse feed — the newest post is rarely the best one. **Ranked improves engagement measurably and costs a
feature store, a model, a training pipeline, and pagination that is much harder to get right.** It also makes
the product harder to reason about, for users and for you.

**Precomputed feeds are stale by design.** A push-based feed reflects the world as of when the fan-out ran, so
a post from thirty seconds ago may not be there yet. **For a social feed nobody notices; for anything where
completeness matters it would be unacceptable**, and that is worth stating rather than glossing.

**Deleting is expensive to do properly and cheap to fake.** Removing a post from every feed it was pushed to
is `O(followers)` again. **Filtering at read time is free — the hydration already drops missing posts** — at
the cost of the id lingering in millions of sorted sets. **The stale ids are harmless and they do consume the
feed cap**, so a user who follows someone who deletes constantly gets a slightly shorter effective feed.

**The feed cap trades completeness for bounded storage.** Eight hundred entries is 8 TB across the user base;
uncapped is unbounded. **A user who scrolls past the cap falls back to the slow read path** — which is correct,
because that is a rare action and paying 180 ms for it is fine.

**When would I not build this?** **When the follower graph is small and uniform** — a team chat, a classroom
app — where a single query with a join is the whole feed and fan-out infrastructure is pure overhead. **When
the feed is not personalised**, like a news site's front page, where one cached page serves everybody and none
of this applies. **And below roughly a million users, where fan-out on read with good caching is simpler,
correct, and fast enough** — building the hybrid first is the classic premature-scaling mistake here.

---

## 8. In the interview

### How it gets asked

- *"Design a news feed / Twitter timeline / Facebook feed."* — the standard prompt.
- *"Push or pull?"* — the central question, sometimes asked in exactly those words.
- *"A celebrity with fifty million followers posts. What happens?"*
- *"How do you paginate?"* — the detail that separates people.
- *"How do you rank it?"*
- *"What happens when a post is deleted?"*

### The first ninety seconds

> "Let me compute one number first, because it decides the architecture.
>
> **Three hundred million daily users opening the app ten times a day is three billion feed reads. They post
> about a tenth of a time a day, so thirty million posts. That is a hundred reads per write.**
>
> **So it is worth doing a lot of work at write time to make reads cheap**, and that points at fan-out on
> write.
>
> **Fan-out on write means: when you post, I immediately insert your post id into the precomputed feed of
> every follower.** Reading is then one lookup of an assembled list — about five milliseconds, no joins, no
> merging.
>
> **The alternative, fan-out on read, does nothing at write time and, when you open the app, queries everyone
> you follow, merges by time and returns the top twenty.** For someone following five hundred accounts that is
> five hundred queries and a merge — **about 180 milliseconds, on every one of those hundred reads.**
>
> **Fifteen times slower, a hundred times as often. Write wins.**
>
> **And it fails completely on one input.** An account with fifty million followers posting once becomes fifty
> million inserts. At fifty thousand writes a second that is **seventeen minutes**, during which the last
> follower has not seen the post and the pipeline is doing nothing else.
>
> **So: hybrid.** Accounts under about ten thousand followers fan out on write. Above that, the post is just
> stored. **At read time I take my precomputed feed and separately fetch recent posts from the roughly thirty
> celebrities I follow, and merge.** That merge is cheap precisely because you follow thirty celebrities and
> not three thousand.
>
> **Storage: the feed holds post ids, not content.** Sixteen bytes an entry, capped at eight hundred entries
> per user — three hundred million users is about eight terabytes of Redis. **Storing the content instead would
> be 240 terabytes and would mean eight hundred updates every time someone edits a post.**
>
> **Redis sorted sets**, scored by timestamp, with `ZREVRANGE` for the read and `ZREMRANGEBYRANK` for the cap.
>
> **Two questions before I go further: is the feed chronological or ranked?** Because ranking changes the read
> path and makes pagination substantially harder. **And what is the follower distribution?** Because the whole
> hybrid exists to handle its tail."

### The follow-ups

**"A celebrity with fifty million followers posts. Walk me through it."**

> "Under pure fan-out on write, that one action becomes fifty million sorted-set inserts.
>
> **At about fifty thousand writes a second sustained, that is a thousand seconds — roughly seventeen
> minutes.** So the first follower sees it immediately and the last sees it seventeen minutes later, **and for
> those seventeen minutes the fan-out pipeline is doing nothing else** — every ordinary user's posts are
> queued behind it.
>
> **And it is worse than a single spike, because these accounts post repeatedly**, and a few of them posting
> in the same minute saturates the pipeline for an hour.
>
> **So celebrity accounts are excluded from fan-out entirely.** Above a threshold — ten thousand followers,
> say — a post is written once to the post store and nothing is pushed.
>
> **The cost moves to the read path, and it is small.** When I open the app, I read my precomputed feed and
> **separately fetch recent posts from the celebrities I follow — typically twenty or thirty accounts** — then
> merge by score and take the top twenty. That is a handful of extra queries, cached, adding maybe three
> milliseconds.
>
> **The asymmetry is what makes it work: the number of celebrities I follow is small even though the number of
> people who follow them is enormous.**
>
> **Two refinements I would mention.** **The celebrity list per user should be cached**, because recomputing
> 'which of the people I follow are above the threshold' on every refresh is a join on the read path.
>
> **And the threshold does not have to be a hard cutoff.** An account with fifteen thousand followers could
> fan out to its most active followers — the ones who opened the app today — and leave the rest to the read
> path. **That gets instant delivery for the people who will actually see it soon, and bounds the write cost.**
>
> **The number itself is a tuning parameter, not a principle.** What matters is the reason there is one:
> **below it, `O(followers)` writes are cheaper than making every reader merge; above it, they are not.**"

**"How do you paginate the feed?"**

> "Not with offsets, and this is the detail that quietly ruins feeds.
>
> **Offset pagination breaks on a changing list.** I ask for offset zero, limit five and get posts ten through
> six. While I am reading them, three new posts arrive. I ask for offset five, limit five — **but the list has
> shifted down by three, so I get posts eight through four, and posts eight, seven and six are shown to me
> again.**
>
> **Duplicates on page two, every time the feed is active** — and the more active the feed, the worse it is,
> which means it is worst for exactly the users who use the product most.
>
> **Cursor pagination fixes it.** Instead of 'skip five', the request says 'give me what comes after this
> point', where the cursor encodes the score and id of the last item I returned. **New posts arriving above the
> cursor do not affect it at all**, because I am asking for things below a fixed position rather than at a
> fixed offset.
>
> **The cursor needs both the score and the id**, not just the score, because two posts can share a timestamp
> and the id breaks the tie deterministically.
>
> **And for a ranked feed there is a further problem.** Scores change — engagement counts move, the model gets
> retrained — so a post that scored low on page one might score higher by the time I ask for page two, and
> appear again. **So the cursor must also carry a ranking session id**, and page two is scored against the same
> snapshot as page one. **Without that, ranking reintroduces exactly the duplicates that cursors were meant to
> remove.**
>
> **Two practical points.** **The cursor should be opaque** — base64 of a small JSON blob — so I can change
> what is inside it without breaking clients. **And I would over-fetch**: request sixty candidates to return
> twenty, because filtering will drop deleted posts, blocked authors and already-seen items, and a second round
> trip to top up is worse than fetching three times as much."

**"What happens when someone deletes a post, or unfollows someone?"**

> "Both are the same shape of problem, and the answer to both is the same: **do not fix the feeds, filter at
> read.**
>
> **Deleting properly means removing the post id from every feed it was pushed to** — which is `O(followers)`
> again, the same cost as the original fan-out. For a post with a million followers that is a million deletes,
> and a user expects a delete to take effect immediately, not in twenty minutes.
>
> **So instead: delete the post from the post store, and leave the ids in the feeds.** At read time, hydration
> fetches the posts by id, and a deleted post simply is not returned — **the filtering already happens as a
> side effect of the batched fetch.** The id lingers in millions of sorted sets, harmlessly.
>
> **What it costs is the feed cap.** A stale id occupies one of the eight hundred slots, so a user who follows
> someone who deletes a lot has a slightly shorter effective feed. **In practice that is invisible**, and a
> background job can compact feeds lazily if it ever matters.
>
> **Unfollowing is the same.** Rather than scrubbing every entry that user contributed, keep the follow edge's
> removal authoritative and let the read path filter — though in practice, unfollow is rarer and the feed
> refreshes past the old entries within a day anyway.
>
> **Blocking is the one case where I would not rely on lazy filtering alone**, because the requirement is
> stronger: a blocked user's content must not appear, and 'it will age out' is not an acceptable answer.
> **Filter at read against the block list**, which must be checked on every hydration rather than treated as a
> cache-warming nicety.
>
> **The general principle is worth naming: in a fan-out-on-write system, writes are expensive and reads are
> cheap, so push corrections to the read path.** Anything that would require touching many feeds should instead
> become a filter applied to the twenty items actually being returned."

### The model answer

*"Design the feed for a photo-sharing app: two hundred million daily users, an average of three hundred
follows each, some accounts with tens of millions of followers, and the feed should be ranked rather than
chronological."*

> "Three things in that prompt drive the design: **two hundred million daily users, a heavy follower tail, and
> ranked rather than chronological.** Let me size it first.
>
> **Two hundred million users opening the app maybe eight times a day is 1.6 billion feed reads, about 18,000 a
> second average and 55,000 at peak.** Photo apps post more than text apps — say 0.3 posts per user per day —
> so sixty million posts, about 700 a second. **That is still a 25-to-1 read ratio, which justifies fan-out on
> write.**
>
> **Fan-out volume: 700 posts a second times 300 average followers is 210,000 feed inserts a second**, peaking
> around 600,000. Redis does about 100,000 operations a second per instance, so **six to ten instances sharded
> by user id**, with pipelining so a thousand-follower batch is one network call rather than a thousand.
>
> **Hybrid at a ten-thousand-follower threshold**, for the reason the prompt hints at: an account with fifty
> million followers would take seventeen minutes to fan out and block everything else. **Those accounts store
> once; readers merge in the twenty or thirty celebrity accounts they follow.**
>
> **Feed storage: post ids in Redis sorted sets, capped at 800.** Two hundred million users at 800 entries of
> 16 bytes is about 2.5 TB, roughly 5 TB with sorted-set overhead. **Storing the images or even the post
> content there would be absurd** — the media lives in object storage behind a CDN and the feed holds ids.
>
> **Now ranking, which the prompt asks for and which changes the read path.**
>
> **Candidates → features → score → filter → return.** I over-fetch: take about two hundred candidates from
> the precomputed feed plus the celebrity merge, score them, return twenty. **Features are author affinity —
> how much this user interacts with this author — post age, early engagement rate, and media type.**
>
> **Time decay is the part I would be explicit about.** A raw predicted-engagement score would let a viral
> two-day-old photo outrank everything new forever, so the score is divided by a power of age. **The exponent
> is the product's dial between 'recent' and 'good', and I would want it configurable rather than compiled
> in.**
>
> **Ranking's real cost is pagination.** Cursor-based, and **the cursor must carry a ranking session id** so
> page two is scored against the same snapshot as page one — otherwise a post whose engagement rose between
> requests appears on both pages. **That is the failure mode people miss, and it is worse for the most active
> users.**
>
> **The read path end to end: read my feed, merge celebrities, rank, filter for deleted and blocked, then one
> batched hydration.** Three multi-gets — posts, authors, counters — not sixty round trips. **That batching is
> the difference between about 5 milliseconds and 30 on the same work**, and it is one line.
>
> **Media, which is specific to a photo app.** The feed returns image URLs pointing at a CDN, with several
> pre-generated sizes so a phone on a slow connection fetches a thumbnail and not a four-megabyte original.
> **The CDN is doing the heavy lifting here — the feed API is small JSON, and the bytes are all images.**
>
> **Two things I would raise as risks.** **A precomputed feed is stale by design** — a post from thirty
> seconds ago may not have fanned out yet — which for a photo feed nobody notices, and I would say it out loud
> rather than let it be discovered. **And a new user's feed is empty**, which is the worst possible first
> impression, so it needs seeding from popular content in their interests until they follow enough accounts.
>
> **And the thing I would leave for version two:** the partial fan-out refinement, where accounts just above
> the threshold push only to followers who were active today. **It is a real improvement and it adds a
> liveness signal to the write path**, and I would not put that complexity in before measuring whether the
> hard threshold actually hurts."

---

## 9. Recall card

**Compute the ratio first: ~100 reads per write.** That is what justifies expensive writes. **Fan-out on write
(push)** = `O(followers)` per post, ~12 ms reads. **Fan-out on read (pull)** = free writes, ~180 ms reads
querying hundreds of timelines. **15× slower, 100× as often — write wins.**

**And write breaks on the celebrity: 50M followers = 50M inserts = ~17 minutes**, with the pipeline blocked
throughout. **So: hybrid.** Under ~10,000 followers → fan out on write; above → store only, and **readers merge
in the ~30 celebrities they follow.** The asymmetry is the point: few celebrities followed, many followers
each. **The threshold is a tuning parameter — be able to derive it, not recite it.**

**Feeds hold post IDs, never content** — 16 bytes vs 1 KB, and content is stored once (8 TB vs 240 TB at 300M
users). **Redis sorted sets, `ZREVRANGE` to read, `ZREMRANGEBYRANK` to cap at ~800** — uncapped feeds grow
forever.

**Cursor pagination, never offsets** — new posts shift an offset and page two repeats page one's items. The
cursor carries **score + id**, and for a ranked feed **a ranking session id too**, or changing scores
reintroduce duplicates.

**Hydrate in 3 batched multi-gets, not 60 round trips** (~5 ms vs ~30). **Deletes and unfollows are filtered at
read**, not scrubbed from millions of feeds — the batched fetch drops missing posts for free. **Ranking =
candidates → features → score → filter**, with **time decay** (`score / (age+2)^1.5`) so a viral old post does
not outrank everything new.
