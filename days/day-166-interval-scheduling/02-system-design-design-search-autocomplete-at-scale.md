---
day: 166
track: system-design
title: "Design search autocomplete at scale"
phase: "High-level design case studies"
status: written
---

# Design search autocomplete at scale

## 1. What this is, and why they ask it

Autocomplete suggests query completions as you type. **You wrote the trie for it on
[day 122](../day-122-autocomplete/README.md).** Today is what happens when a billion people use it.

They ask it because **it is the design where a data structure you know well turns out to be the easy part**,
and the interesting engineering is everywhere else.

**The latency requirement is brutal and it is the constraint that shapes everything.** Suggestions must appear
before the user types the next character — **under about a hundred milliseconds end to end, including the
network** — and a suggestion that arrives after the next keystroke is worse than useless, because the user has
moved on.

**The query rate is extreme, and for an unusual reason: it is per keystroke, not per search.** A single search
for "manchester united" generates seventeen autocomplete requests. **So autocomplete traffic is roughly an
order of magnitude larger than search traffic**, which surprises people and is the first thing to compute.

**And the ranking is where the product lives.** Any trie can return the completions of a prefix. **Returning
the five that this person, in this place, right now, actually wants** is the whole value, and it involves
popularity, recency, personalisation and a serious amount of filtering.

**The fourth thing — and it is the one that separates candidates — is that this is not a live query at all.**
The obvious design walks a trie at request time. **The scalable design precomputes the answer for every
prefix and serves it as a lookup**, and understanding why that inversion is necessary is the point of the
interview.

By the end of this lesson you can design the data structure and its precomputation, get inside the latency
budget, rank and personalise, handle trending queries and abuse, and size the whole thing.

---

## 2. The story

The chemist's shop had eleven thousand things in it and Ravindran had worked there since he was nineteen, and
by the time he was fifty he did something that visitors found unsettling.

**You would get four words into a sentence and he would already be reaching.**

Not guessing. **He would be right almost every time, and when he was wrong he was wrong in a way that told you
he had been thinking about it.**

His nephew, who took over the shop, spent a year trying to work out how it was done, **because he could not do
it and he had the same eleven thousand things.**

**And when he finally asked, the answer was in three parts and none of them was memory.**

**"Most of what anybody asks for is about forty things."** Eleven thousand on the shelves, and forty of them
were nine out of every ten sales. **"I am not searching eleven thousand. I am searching forty."**

**Second: he did not wait for you to finish.** As you started, he was already narrowing — and by the fourth
word there were usually two or three possibilities, **and he had thought about all three before you stopped
talking.**

**"If I start thinking when you finish, I am slower than you. I have to be ahead of you."**

**And the third part was the one his nephew had not expected at all.**

**"It changes."** In the fever season, the first thing anybody says leads somewhere different from the same
words in December. **And a man who came in every fortnight got a different answer from a stranger saying
exactly the same thing**, because Ravindran knew what he had bought last time.

His nephew said that was just knowing the customers.

**"It is knowing that the same four words mean different things depending on who said them and what month it
is,"** he said. **"The words are not the question. The words plus everything else are the question."**

And then, because his nephew was writing this down, he added the part he was actually proud of.

**"And I decide before you ask. All day, while I am doing other things, I am working out what people are going
to want. By the time you open your mouth the answer is already made."**

---

## 3. The idea in plain English

Ravindran's three parts are the three ideas: **the popular set is tiny, you must be ahead of the user, and the
answer is precomputed rather than searched.**

**Start with the latency budget, because it is the constraint everything else obeys.**

```
   a fast typist:            ~100-200 ms between keystrokes
   the network round trip:   ~50-80 ms (mobile, realistically)
   -> the SERVER has ~20-50 ms

   and a suggestion that arrives after the next keystroke is
   WORSE than none, because the user has already moved on
```

**Twenty to fifty milliseconds of server time is not enough to walk a trie of a billion queries, rank the
results, personalise them and filter them.** **So you do not.**

**The central inversion: precompute, do not search.**

**The obvious design walks a trie at request time.** For each prefix, find the node, collect the completions
beneath it, rank them, return the top five.

**The scalable design stores the answer at the node.** **Every prefix maps directly to its top five
completions, already ranked**, and the request is a single lookup with no traversal at all.

```
   "man"  ->  ["manchester united", "manchester weather",
               "manga", "mango", "manual"]
```

**A hash map from prefix to a list of strings.** **Not a search — a dictionary lookup**, and that is what fits
in the budget.

**The cost is that it must be rebuilt, and that is the trade to state.** New queries do not appear until the
next rebuild, **which is hours** — and there is a separate fast path for trending terms, which is the third
idea below.

**Now the data structure, and the honest version of it.**

**A trie is the right mental model and often not the right storage.** A trie of a billion distinct queries has
enormous pointer overhead — **the pointers can outweigh the strings** — so real systems use one of:

**A compressed trie (a radix tree)**, where chains of single-child nodes collapse into one edge holding a
string. **"manchester" is one edge, not ten nodes**, and for query data this typically reduces the node count
by an order of magnitude.

**Or, simpler and often better: a flat hash map from prefix to results.** **You lose the ability to walk the
structure and you gain constant-time lookup and trivial sharding**, and since the answers are precomputed
anyway, walking was not needed.

**And the prefixes are capped.** **Only prefixes up to about twenty characters are stored** — beyond that the
result set is tiny, users rarely type that far without selecting, and **the storage would grow without
bound.**

**Then ranking, which is where the product is.**

**Popularity alone gives a stale, generic list.** The ranking signals that matter:

```
   frequency          how often this query is issued        the base
   recency            weighted towards the last few days    stops staleness
   click-through      did people SELECT this suggestion?    the real signal
   personal history   have YOU searched this before?        strongest of all
   location           "weather" means different things       cheap and effective
   time               "cricket score" during a match
```

**Personal history is the strongest signal and the cheapest to apply**, because a user's own recent queries are
a short list that can live on the device — **so personalisation can happen client-side with no server cost at
all.** That is worth saying: **the most valuable ranking signal need not touch your infrastructure.**

**Then trending, which is the thing precomputation cannot do.**

**Something happens. Within minutes, millions of people search for it.** **And it is not in the precomputed
index, because that was built last night.**

**So there is a second, small, fast layer**: a real-time counter of query frequency over the last few minutes,
**merged with the precomputed results at request time.** Small enough to update continuously, and it only has
to handle the tail of unusual queries — **the head is handled by the index that was built overnight.**

**Two layers, two update frequencies**, and merging them is a few milliseconds.

**Then the delivery layer, which is most of where the latency goes.**

**Because the server has twenty to fifty milliseconds and the network has fifty to eighty**, the biggest
available win is **not being on the network at all.**

**Cache in the browser.** The completions of "m" contain everything the completions of "man" need, **so the
client can filter locally as the user types further** — one request per few keystrokes rather than one per
keystroke. **That alone removes most of the traffic.**

**Debounce.** Do not fire on every keystroke; wait fifty milliseconds for the typing to pause. **A fast typist
generates one request instead of five.**

**And serve from the edge.** The precomputed index is small enough — **a few gigabytes for the popular
prefixes** — to sit at a CDN point of presence, **which removes the transcontinental round trip.**

**Then the thing that must not be skipped: filtering.**

**Autocomplete is a highly visible surface that puts words in a user's mouth**, and suggesting something
offensive, defamatory or illegal is a real and recurring problem — **it has produced lawsuits.**

**So: a blocklist applied at index-build time and again at serve time**, personal names handled specially,
and a mechanism for removing a suggestion quickly **without waiting for the next nightly build.** That last
requirement is why the serve-time filter exists as well as the build-time one.

**Finally, the sizing intuition that makes this manageable.**

**Ravindran's forty things.** **The distribution of queries is extraordinarily skewed** — a small number of
queries account for most of the traffic, and the long tail is enormous and rarely typed.

**So the precomputed index does not need every prefix of every query.** **Cover the popular prefixes
completely and fall back to a slower path for the rest**, and the slow path is almost never taken.

---

## 4. The picture

The latency budget, which drives everything:

```
   user types a character
        |
        v
   |<---------------- ~100-200 ms until the next keystroke ---------------->|
   |                                                                        |
   | network out  |  SERVER  | network back | render |
   |   25-40 ms   | 20-50 ms |   25-40 ms   |  5 ms  |
                     ^^^^^^^
                     this is ALL you have

   In 20-50 ms you cannot: walk a trie over a billion queries,
   rank the candidates, personalise them, and filter them.

   -> SO DO NOT. Precompute the answer and make the request a LOOKUP.
```

Search against precompute:

```
   AT REQUEST TIME (the obvious design)

     prefix "man"
       -> walk the trie to the "man" node
       -> collect every completion beneath it   (could be millions)
       -> score each one
       -> sort, take 5
     -> tens of milliseconds at best, unbounded at worst


   PRECOMPUTED (the scalable design)

     "man" -> ["manchester united", "manchester weather",
               "manga", "mango", "manual"]

     -> ONE hash lookup. Microseconds.
     -> the ranking already happened, offline, last night

   THE COST: new queries do not appear until the next rebuild.
   -> hence a second, small, REAL-TIME layer for trending.
```

The two layers:

```
   +--------------------------------------------------+
   |  PRECOMPUTED INDEX   rebuilt every few hours      |
   |  every prefix -> its top 5, already ranked        |
   |  large (GBs), covers the HEAD of the distribution |
   +--------------------------------------------------+
                          +
   +--------------------------------------------------+
   |  TRENDING LAYER      updated every few MINUTES    |
   |  query counts over a short window                 |
   |  small (MBs), covers what just started happening  |
   +--------------------------------------------------+
                          |
                          v
              merge at request time (~1 ms)

   Two structures, two update frequencies.
   The overnight build cannot know about the last ten minutes;
   the trending layer cannot rank a billion queries.
```

The trie, and why it is usually not stored as a trie:

```
   PLAIN TRIE                        COMPRESSED (RADIX)

   m - a - n - c - h - e - s ...      "manchester" as ONE edge
   |   |   |
   ...                                -> chains of single-child nodes
                                         collapse into one string edge
   10 nodes for "manchester"         -> ~10x fewer nodes for query data
   each with a child map
   -> POINTERS OUTWEIGH THE STRINGS

   OR, SIMPLER: a flat hash map

     prefix -> [top 5]

   -> you lose the ability to WALK the structure
   -> you gain O(1) lookup and trivial sharding by prefix
   -> and since the answers are PRECOMPUTED, walking was
      never needed
```

Where the traffic actually goes, and how to remove it:

```
   NAIVE: one request per keystroke

     "manchester united" = 17 requests

   DEBOUNCE (wait 50 ms for a pause):
     a fast typist -> ~4 requests        -> 4x fewer

   CLIENT-SIDE FILTERING:
     the results for "man" CONTAIN everything "manc", "manch"...
     need — so filter locally until the prefix leaves the
     cached set
     -> ~2 requests                       -> another 2x

   EDGE CACHING:
     the popular prefixes are a few GB -> they fit at a CDN PoP
     -> removes the transcontinental round trip (~100 ms -> ~20 ms)

   THE BIGGEST WIN IS NOT BEING ON THE NETWORK AT ALL.
```

The skew, which is Ravindran's forty things:

```
   query frequency (roughly)

   top 1,000 queries          ~20% of all traffic
   top 100,000                ~50%
   top 10,000,000             ~85%
   the long tail (billions)   ~15%, each query seen a handful of times

   -> the precomputed index does NOT need every prefix of every query
   -> cover the popular prefixes completely; fall back to a slower
      path for the rest
   -> and the slow path is almost never taken

   "I am not searching eleven thousand. I am searching forty."
```

---

## 5. How it actually works

### The precomputed index

```python
def build_index(query_counts: dict[str, int], top_k: int = 5,
                max_prefix: int = 20) -> dict[str, list[str]]:
    """Offline. For every prefix, the top-k completions, already ranked."""
    candidates: dict[str, list[tuple[float, str]]] = {}
    for query, count in query_counts.items():
        score = rank_score(query, count)
        for length in range(1, min(len(query), max_prefix) + 1):
            prefix = query[:length]
            bucket = candidates.setdefault(prefix, [])
            bucket.append((score, query))
            if len(bucket) > top_k * 20:               # keep it bounded
                bucket.sort(reverse=True)
                del bucket[top_k * 20:]

    return {prefix: [q for _, q in sorted(bucket, reverse=True)[:top_k]]
            for prefix, bucket in candidates.items()}
```

**`max_prefix = 20` bounds the storage.** Without it, every query contributes one entry per character, **and
long queries dominate the index while nobody ever types that far.**

**And the `top_k * 20` truncation inside the loop is what keeps memory bounded during the build** — a popular
prefix like `"a"` would otherwise accumulate every query in the corpus.

**This is a batch job**, and in practice it is a MapReduce or Spark job over a day of query logs — **map each
query to its prefixes, reduce by taking the top-k per prefix.**

### Serving

```python
def suggest(prefix: str, user_id: int | None, region: str) -> list[str]:
    prefix = normalise(prefix)                        # lowercase, strip accents
    base = index.get(prefix, [])                      # ONE lookup
    trending = trending_layer.get(prefix, region)     # small, fast, recent
    merged = merge_ranked(base, trending)
    return [s for s in merged if not blocklist.contains(s)][:5]
```

**Three lookups and a merge**, and no traversal anywhere. **That is what fits in the budget.**

**`normalise` matters more than it looks**: `"Man"`, `"man"` and `"mán"` must hit the same entry, **or the
index is three times larger and mostly missed.**

**And the blocklist is applied here as well as at build time**, because **a suggestion that must be removed
cannot wait for the next nightly rebuild.**

### The trending layer

```python
WINDOW_SECONDS = 600

def record_query(query: str, region: str) -> None:
    bucket = int(time.time()) // 60
    redis.zincrby(f"trend:{region}:{bucket}", 1, query)
    redis.expire(f"trend:{region}:{bucket}", WINDOW_SECONDS * 2)


def trending_for(prefix: str, region: str, top_k: int = 3) -> list[str]:
    now = int(time.time()) // 60
    keys = [f"trend:{region}:{b}" for b in range(now - 10, now + 1)]
    merged = redis.zunionstore_temp(keys)             # ten one-minute buckets
    return [q for q, _ in redis.zrevrange(merged, 0, 200)
            if q.startswith(prefix)][:top_k]
```

**One-minute buckets with a TTL is the standard sliding-window shape** — old buckets expire on their own, and
there is no cleanup job.

**Scanning the top two hundred and filtering by prefix is the compromise.** **A proper prefix index over
trending data would be another whole structure**, and since trending is by definition a short list, a scan is
fine.

**And it is per region**, because what is trending in one country is irrelevant in another — **which also
keeps each list short enough to scan.**

### Client-side filtering, which is the biggest win

```javascript
let cache = { prefix: "", results: [] };

function onInput(text) {
  // if the new text extends a prefix we already have, filter locally
  if (text.startsWith(cache.prefix) && cache.results.length >= 5) {
    const local = cache.results.filter(r => r.startsWith(text));
    if (local.length >= 5) {
      render(local.slice(0, 5));
      return;                     // NO REQUEST AT ALL
    }
  }
  debouncedFetch(text);
}
```

**`if (local.length >= 5)` is the condition that makes this safe.** The cached results for `"man"` contain the
top five for `"man"`, **not necessarily the top five for `"manch"`** — **so local filtering is only valid while
enough results survive**, and it falls back to the server otherwise.

**This removes most of the requests**, and it costs nothing on the server.

### Debouncing

```javascript
let timer = null;
function debouncedFetch(text) {
  clearTimeout(timer);
  timer = setTimeout(() => fetch(`/suggest?q=${encodeURIComponent(text)}`)
                            .then(r => r.json()).then(render), 50);
}
```

**Fifty milliseconds is the usual value** — long enough that a fast typist's keystrokes coalesce, **short
enough that a pause feels instant.**

**And the request must be cancellable**, or a slow response for `"man"` can arrive after the response for
`"manch"` and overwrite it — **which is the out-of-order rendering bug that makes autocomplete feel broken.**

### Ranking

```python
import math

def rank_score(query: str, count: int, last_seen: float = 0.0,
               clicks: int = 0, impressions: int = 1) -> float:
    """Frequency, decayed by age, weighted by whether people SELECT it."""
    popularity = math.log1p(count)                     # log: damp the head
    age_days = (time.time() - last_seen) / 86400 if last_seen else 30
    recency = math.exp(-age_days / 14)                 # two-week half-life-ish
    click_rate = (clicks + 1) / (impressions + 10)     # smoothed
    return popularity * (0.5 + 0.5 * recency) * (0.5 + click_rate)
```

**`log1p` on the count is deliberate**: raw frequency lets a handful of enormous queries dominate every
prefix, **and the log compresses the head so that the merely-popular can still appear.**

**And the click rate is the strongest of the three signals**, because it measures whether a suggestion was
useful rather than whether the query is common — **a query people type but never select from the suggestions
should rank lower.**

### Personalisation, which need not touch the server

```javascript
function personalise(suggestions, localHistory) {
  const recent = new Set(localHistory.slice(-200));
  const boosted = suggestions.filter(s => recent.has(s));
  const rest    = suggestions.filter(s => !recent.has(s));
  return [...boosted, ...rest].slice(0, 5);
}
```

**The strongest ranking signal is the user's own history, and it can live entirely on the device.** **No server
cost, no privacy exposure, and it applies instantly** — which is a rare combination and worth pointing at.

### Filtering

```python
def is_blocked(suggestion: str, blocklist, patterns) -> bool:
    lowered = suggestion.lower()
    if lowered in blocklist:
        return True
    if any(p.search(lowered) for p in patterns):        # regex families
        return True
    if contains_person_name(lowered) and is_defamatory_shape(lowered):
        return True                                    # "<name> is a ..."
    return False
```

**The person-name rule is the one that exists because of lawsuits.** **Completing a real person's name with a
defamatory phrase is a legal problem in several jurisdictions**, and the pattern is specific enough to detect.

**And the blocklist runs at serve time as well as build time**, because **removal must be immediate.**

### Sharding

```python
def shard_for(prefix: str, shard_count: int) -> int:
    """By the first two characters — an even, stable split."""
    return hash(prefix[:2]) % shard_count
```

**Sharding by the first two characters keeps a prefix and its extensions on the same shard**, which is useful
if you ever do need to walk, **and it distributes evenly enough** — the first character alone is badly skewed.

**And a prefix's entry never needs another shard**, because the answer is precomputed — **so there are no
cross-shard queries at all.**

### The real systems

```
Elasticsearch      completion suggester — an in-memory FST
                   (finite state transducer), which is a compressed
                   trie with shared suffixes
Lucene FST         the underlying structure; ~10x smaller than a
                   plain trie
Redis              the trending layer (sorted sets), and often the
                   serving cache
Spark / MapReduce  the nightly index build over query logs
CDN / edge         serving the popular prefixes close to users
Solr, Algolia,     hosted alternatives, all of which precompute
Typesense
```

**Naming the FST is worth doing**, because it is the specific answer to "how do you store a billion prefixes"
— **shared prefixes *and* shared suffixes, which a plain trie does not give you.**

---

## 6. The numbers

**The traffic, and the number that surprises people.**

```
5,000,000,000 searches/day

each search: ~15 characters typed
naive: one request per keystroke
= 75,000,000,000 autocomplete requests/day
= ~870,000/second average, peak ~3,000,000/second

-> AUTOCOMPLETE TRAFFIC IS 15x SEARCH TRAFFIC.
   That is the first thing to compute, and it is why the delivery
   layer matters more than the algorithm.
```

**And what the client-side work removes:**

```
   naive, per keystroke:        75,000,000,000/day
   + debounce (50 ms):          ~20,000,000,000    (4x fewer)
   + client-side filtering:     ~10,000,000,000    (another 2x)
   + edge caching (90% hit):     ~1,000,000,000 reaching origin

   -> 75x fewer requests reaching your servers, entirely from
      client and edge behaviour.
```

**Seventy-five times, from three client-side techniques** — which is why the delivery layer is where the
engineering effort goes.

**The latency budget, itemised.**

```
   time between keystrokes (fast typist)    100-200 ms
   network round trip, mobile                50-80 ms
   TLS/connection (if not reused)            +50 ms   <- keep connections alive
   render                                     5 ms
                                            ---------
   LEFT FOR THE SERVER                       20-50 ms

   within that:
     hash lookup in the index                <1 ms
     trending layer lookup                   ~2 ms
     merge and filter                        ~1 ms
     serialisation                           ~1 ms
                                            --------
                                             ~5 ms

   -> the server work is comfortably inside the budget.
      THE NETWORK IS THE PROBLEM, which is why edge serving matters.
```

**Index size.**

```
1,000,000,000 distinct queries, average 20 characters
prefixes per query: up to 20
-> 20,000,000,000 prefix entries if built naively

with the SKEW:
  only ~10,000,000 queries account for 85% of traffic
  their prefixes: 10,000,000 x 20 = 200,000,000 entries

each entry: prefix (~10 B) + 5 suggestions x ~20 B = ~110 B
200,000,000 x 110 B = ~22 GB

-> fits on one machine; shards comfortably to a few
-> and the popular subset (the top 1,000,000 prefixes) is
   ~110 MB, which fits at every CDN edge
```

**That last line is the important one**: **the head of the index is small enough to replicate everywhere**,
which is what makes edge serving possible.

**The nightly build.**

```
5,000,000,000 queries/day of log data at ~50 bytes = 250 GB/day

MapReduce:
  map: each query -> up to 20 (prefix, query, score) pairs
       = 100,000,000,000 intermediate records
  reduce: top-5 per prefix

on a 500-machine cluster: ~1-2 hours

-> run it every 4-6 hours rather than nightly, which halves the
   staleness for the cost of more cluster time
```

**The trending layer, for contrast:**

```
   10-minute window, per region
   ~1,000,000 distinct queries in 10 minutes globally
   ~50 regions -> ~20,000 per region

   20,000 entries x ~50 B = 1 MB per region
   50 regions            = 50 MB total

-> the trending layer is 50 MB against the index's 22 GB.
   Small enough to update every minute, which is exactly why
   there are two layers.
```

**Storage against a plain trie, which is why FSTs exist:**

```
   plain trie, 1 billion queries:
     ~10,000,000,000 nodes
     each with a child map: ~100 bytes with pointer overhead
     = ~1 TB

   compressed trie (radix): ~10x fewer nodes    -> ~100 GB
   FST (shared prefixes AND suffixes):          -> ~10-20 GB

   -> the pointers outweigh the strings in a plain trie, which is
      the whole reason for the compressed forms.
```

**Cost, roughly:**

```
   serving fleet (1B requests/day at origin)  ~$50,000/month
   edge/CDN                                   ~$30,000/month
   index build (6-hourly on a big cluster)    ~$40,000/month
   trending layer (Redis)                     ~$5,000/month
                                              ----------------
                                              ~$125,000/month

   for a feature that never returns a search result and exists
   purely to save the user typing.

-> which is worth stating: the justification is that it measurably
   increases completed searches, and it is expensive.
```

**The abuse surface, sized:**

```
   a coordinated group issuing a query repeatedly to make it appear
   in autocomplete

   trending layer, 10-minute window, ~20,000 queries per region:
     ~500 repetitions would put a query near the top

   -> trivially cheap to attack
   -> hence: per-user rate limiting on what COUNTS towards trending,
      requiring queries from distinct accounts and addresses,
      and a minimum distinct-user threshold before anything trends
```

---

## 7. The trade-offs

**Precomputing against searching at request time.** Precomputing turns a traversal into a lookup and **fits the
twenty-millisecond budget**; searching does not. **The cost is staleness — a new query does not appear until
the next build**, which is hours. **The trending layer patches the hole** at the cost of a second structure
with a different update cycle and a merge on every request.

**Index size against coverage.** Storing every prefix of every query is twenty billion entries. **Storing only
the popular prefixes is two hundred million and covers 85% of traffic** — and the remaining 15% falls back to a
slower path. **That fallback must exist and be tested**, because it runs rarely and always for the users with
unusual queries.

**Client-side filtering against correctness.** Filtering locally removes most of the traffic and **can return
the wrong answer**: the cached top five for `"man"` may not contain the top five for `"manch"`. **Guarding on
"do I still have five results" makes it safe** at the cost of falling back more often — and getting that guard
wrong degrades quality invisibly.

**Personalisation on the device against on the server.** On-device is free, private and instant, **and cannot
use anything the device does not know** — no cross-device history, no collaborative signals. Server-side
personalisation is more powerful and **costs a per-user lookup inside a twenty-millisecond budget**, plus a
privacy surface. **Most of the value is in the user's own recent queries, which the device already has.**

**Trending window length.** Ten minutes reacts fast and is **easy to manipulate** — a few hundred coordinated
queries can promote a term. An hour is robust and slow. **The mitigation is not the window length but the
counting rule**: distinct users, rate-limited, with a minimum threshold.

**Filtering aggressiveness.** Blocking too little produces offensive suggestions on a highly visible surface
**and has produced lawsuits.** Blocking too much removes legitimate queries and is invisible — **nobody reports
a suggestion that did not appear.** The asymmetry is entirely towards over-blocking, which is the right
default and should be a stated decision.

**When would I not build this?** **Almost always — the completion suggester in Elasticsearch or a hosted
service like Algolia does this well**, and below a few thousand queries a second the whole design is overhead.
**A trie in memory on each application server is genuinely sufficient for a catalogue of a million items.**
**Building this is justified by the traffic and the ranking**, not by the data structure — **and if the ranking
is just alphabetical or by popularity, buy it.**

---

## 8. In the interview

### How it gets asked

- *"Design search autocomplete."* or *"Design a typeahead system."* — the standard prompts.
- *"How do you make it fast enough?"* — the latency question, and the core of it.
- *"How do new or trending queries appear?"* — the precomputation gap.
- *"How do you rank the suggestions?"*
- *"How much traffic is this?"* — where the per-keystroke insight lands.
- *"How do you stop it suggesting something offensive?"*

### The first ninety seconds

> "Let me start with two numbers, because they determine the design.
>
> **The first: the latency budget.** A fast typist leaves a hundred to two hundred milliseconds between
> keystrokes. **The network round trip on mobile is fifty to eighty of that.** So **the server has twenty to
> fifty milliseconds** — and a suggestion arriving after the next keystroke is worse than none, because the
> user has moved on.
>
> **The second, which surprises people: this is per keystroke, not per search.** Five billion searches a day at
> fifteen characters each is **seventy-five billion autocomplete requests — fifteen times the search traffic.**
>
> **Those two numbers rule out the obvious design.** In twenty milliseconds I cannot walk a trie over a billion
> queries, collect the completions, rank them, personalise and filter.
>
> **So the central move is: do not search — precompute.** **For every prefix, store its top five completions,
> already ranked.** The request becomes a single hash lookup with no traversal at all.
>
> **The cost is staleness**: a query that started trending an hour ago is not in an index built last night.
> **So there is a second, small, real-time layer** — query counts over the last ten minutes, per region — **and
> the two are merged at request time in about a millisecond.** Two structures, two update frequencies.
>
> **Now the part that I think matters most, and it is not the algorithm.** The server work is about five
> milliseconds and the network is fifty to eighty. **So the biggest win available is not being on the network
> at all.**
>
> **Debouncing** — wait fifty milliseconds for a pause — removes about three quarters of the requests.
> **Client-side filtering** — the results for "man" contain what "manch" needs — removes half of the rest.
> **And edge serving**, because the popular prefixes are about a hundred megabytes and fit at every point of
> presence.
>
> **Together those are about seventy-five times fewer requests reaching my servers**, entirely from client and
> edge behaviour.
>
> **And one thing I would raise unprompted: filtering.** Autocomplete puts words in a user's mouth on a highly
> visible surface, **and suggesting something defamatory about a real person has produced lawsuits.** So there
> is a blocklist at build time and again at serve time, **because removal cannot wait for the next build.**"

### The follow-ups

**"How do you make it fast enough?"**

> "By making the request do almost nothing, and then by making most requests not happen at all.
>
> **The budget first, because it is tighter than people expect.** A hundred to two hundred milliseconds between
> keystrokes, fifty to eighty of it network on mobile, five to render. **Twenty to fifty milliseconds for the
> server.**
>
> **In that time the obvious design cannot work.** Walking a trie over a billion queries, collecting the
> completions beneath a popular prefix — which could be millions — ranking them and filtering them is tens of
> milliseconds at best and unbounded at worst.
>
> **So the answer is precomputation.** Offline, for every prefix, compute and store the top five completions
> already ranked. **The request is one hash lookup.** About a millisecond, plus two for the trending layer and
> one for the merge — **five milliseconds of server time, comfortably inside the budget.**
>
> **But notice where the time actually goes: five milliseconds of server against fifty to eighty of network.**
> **So the algorithm is not the problem. The network is.**
>
> **Three things, and they are where the real gains are.**
>
> **Debounce** — do not fire on every keystroke, wait fifty milliseconds for a pause. **A fast typist generates
> one request instead of four.**
>
> **Client-side filtering.** The results for `"man"` contain everything the results for `"manc"` need, **so
> filter locally until the prefix leaves the cached set.** The guard is 'do I still have five results after
> filtering' — **because the cached top five for a short prefix is not necessarily the top five for a longer
> one**, and without that check the quality degrades invisibly.
>
> **And edge serving.** The popular prefixes — the top million — are about a hundred megabytes. **That fits at
> every CDN point of presence**, which turns a transcontinental round trip into a local one: eighty
> milliseconds down to twenty.
>
> **Two smaller things that matter.** **Keep connections alive** — a TLS handshake is another fifty
> milliseconds and would blow the budget on its own. **And make requests cancellable**, or a slow response for
> a short prefix arrives after a fast one for a longer prefix and overwrites it, **which is the out-of-order
> rendering bug that makes autocomplete feel broken.**"

**"How do new and trending queries appear?"**

> "They do not, in the precomputed index — **and that is the honest cost of precomputing, so I would state it
> as a gap and then close it.**
>
> **The index is built from query logs, and the build takes an hour or two over a day of data.** So even
> running it every four to six hours, **a query that started trending twenty minutes ago is simply not there.**
>
> **And that is exactly when autocomplete matters most** — something happens, millions of people search for it,
> and they are all typing the same new thing.
>
> **So: a second layer, small and fast.** A count of query frequency over the last ten minutes, per region,
> **updated continuously** — one-minute buckets in Redis sorted sets with a TTL, so old buckets expire
> themselves and there is no cleanup job.
>
> **At request time, look up both and merge.** The precomputed layer gives the stable, well-ranked head; **the
> trending layer contributes anything that has become popular in the last few minutes.**
>
> **The sizes make it work.** The main index is around twenty-two gigabytes; **the trending layer is about
> fifty megabytes across all regions** — small enough to update every minute, **which is precisely why they are
> separate structures rather than one.**
>
> **Per region matters too**, because what is trending in one country is irrelevant in another — **and it keeps
> each list short enough that a simple prefix scan over the top few hundred is fast enough**, rather than
> needing a second indexed structure.
>
> **And I would raise the abuse problem unprompted, because it is real.** With a ten-minute window and maybe
> twenty thousand distinct queries per region, **a few hundred coordinated repetitions would put a query near
> the top.** That is trivially cheap to attack.
>
> **The mitigation is not a longer window** — that just makes it slower to react. **It is the counting rule:
> count distinct users rather than queries, rate-limit what counts, and require a minimum number of distinct
> accounts before anything is eligible to trend.**"

**"How do you rank the suggestions?"**

> "Popularity is the base and it is not enough on its own — **a purely popularity-ranked list is stale and
> generic**, and the signals that improve it are cheap.
>
> **Frequency, damped.** How often the query is issued, **but through a logarithm**, because raw counts let a
> handful of enormous queries dominate every prefix they touch **and squeeze out the merely popular.**
>
> **Recency**, with something like a two-week decay. **Search interest moves**, and a query that was popular
> last year and is dead now should not outrank one that is currently rising.
>
> **Click-through rate, which is the strongest of the server-side signals.** It measures whether a suggestion
> was *useful* rather than whether the query is common. **A query people type but never select from the
> suggestions should rank lower** — and that distinction is invisible to frequency alone.
>
> **Location and time, which are cheap and effective.** 'Weather' means something different in two countries;
> 'cricket score' means something specific during a match.
>
> **And then personal history, which is the strongest signal of all — and the interesting thing about it is
> that it need not touch my infrastructure.**
>
> **A user's own recent queries are a short list that can live on the device.** So personalisation can be a
> client-side reordering: **boost anything the user has searched before, then everything else.**
>
> **That is free, private, instant, and it is the highest-value signal available** — which is a rare
> combination and worth pointing at explicitly. **No server cost inside a twenty-millisecond budget, and no
> per-user data leaving the device.**
>
> **What it cannot do is cross-device or collaborative signals** — 'people like you also searched' — which
> would need server-side personalisation. **I would only add that if measurement showed it was worth the
> latency and the privacy surface**, because the device already has most of the value."

### The model answer

*"Design autocomplete for a large search engine: five billion searches a day, global, and suggestions must
appear as the user types."*

> "Two numbers first, because they settle the architecture.
>
> **The latency budget: a hundred to two hundred milliseconds between keystrokes, fifty to eighty of it network
> — so twenty to fifty milliseconds of server time.** And a suggestion that arrives after the next keystroke is
> worse than none.
>
> **And the traffic, which surprises people: this is per keystroke.** Five billion searches at fifteen
> characters is **seventy-five billion requests a day, fifteen times the search traffic itself.**
>
> **Those two rule out searching at request time**, so the central move is **precomputation: every prefix maps
> directly to its top five completions, already ranked.** The request is one hash lookup.
>
> **Sizing that index.** A billion distinct queries, but the distribution is extraordinarily skewed — **ten
> million queries account for eighty-five percent of traffic.** Their prefixes, capped at twenty characters,
> are about two hundred million entries at roughly a hundred and ten bytes: **twenty-two gigabytes.** Fits on
> one machine, shards easily. **And the top million prefixes are about a hundred megabytes, which fits at every
> CDN edge** — that is what makes edge serving possible.
>
> **Storage: an FST rather than a plain trie.** A plain trie over a billion queries is roughly a terabyte
> because **the pointers outweigh the strings**; an FST shares prefixes *and* suffixes and gets it to ten or
> twenty gigabytes. **Or, since the answers are precomputed, a flat hash map from prefix to results is simpler
> and shards trivially** — and walking was never needed.
>
> **The gap in precomputation is trending**, so a second layer: **query counts over a ten-minute window, per
> region, in Redis sorted sets with per-minute buckets and TTLs.** About fifty megabytes globally against the
> index's twenty-two gigabytes — **small enough to update every minute, which is exactly why it is a separate
> structure.** Merged with the main results in about a millisecond.
>
> **Ranking: log-damped frequency, two-week recency decay, and click-through rate** — the last being the
> strongest, because it measures usefulness rather than volume. **Plus location and time.**
>
> **And personalisation on the device**, boosting the user's own recent queries. **The strongest single signal,
> and it costs my servers nothing and exposes no data** — worth calling out as the unusual case where the best
> option is also the cheapest.
>
> **Now the part where the real engineering is, which is delivery.** Server work is about five milliseconds and
> network is fifty to eighty, **so the win is in not being on the network.**
>
> **Debouncing at fifty milliseconds** takes seventy-five billion to twenty. **Client-side filtering**, guarded
> on still having five results, takes it to ten. **Edge caching at ninety percent** takes it to about one
> billion reaching origin. **Seventy-five times fewer, entirely from client and edge behaviour.**
>
> **Two things I would insist on.**
>
> **Filtering, at build time and again at serve time.** Autocomplete puts words in a user's mouth on a very
> visible surface, **and completing a real person's name with a defamatory phrase has produced actual
> lawsuits.** The serve-time filter exists specifically **because a removal cannot wait for the next build.**
> And the asymmetry favours over-blocking: **nobody ever reports a suggestion that did not appear.**
>
> **And abuse of the trending layer.** With a ten-minute window, **a few hundred coordinated queries could
> promote a term** — trivially cheap. **The fix is the counting rule, not the window: distinct users,
> rate-limited, with a minimum account threshold.**
>
> **Closing thought on cost.** This is around a hundred and twenty-five thousand dollars a month for a feature
> that **never returns a search result** — it exists purely to save typing. **The justification has to be
> measured** — completed searches, time to result — **and I would want that measurement to exist, because it is
> a genuinely expensive convenience.**"

---

## 9. Recall card

**Two numbers settle the design.** The **latency budget**: ~100–200 ms between keystrokes minus ~50–80 ms of
network leaves **20–50 ms of server time**, and a late suggestion is worse than none. **And the traffic is per
KEYSTROKE, not per search** — 5B searches × ~15 characters = **75B requests/day, ~15× search traffic.**

**The central inversion: do not search, PRECOMPUTE.** Every prefix maps to its **top five, already ranked** —
one hash lookup, no traversal. **The cost is staleness**, patched by a **second, small, real-time trending
layer** (~50 MB against the index's ~22 GB) merged at request time. **Two structures, two update frequencies.**

**A plain trie is ~1 TB for a billion queries — the pointers outweigh the strings.** Use a **radix tree or an
FST** (shared prefixes *and* suffixes, ~10–20 GB), **or just a flat hash map**, since precomputed answers never
need walking. **Cap prefixes at ~20 characters** or storage grows without bound.

**Server work is ~5 ms and network is 50–80 ms, so the biggest win is NOT BEING ON THE NETWORK.** **Debounce**
(~4×), **client-side filtering** (~2×, guarded on still having five results — the cached top-5 for `"man"` is
not necessarily the top-5 for `"manch"`), and **edge serving** the ~100 MB popular head. **~75× fewer requests
reach origin, entirely from client and edge behaviour.** Keep connections alive, and **make requests
cancellable** or a slow short-prefix response overwrites a fast long-prefix one.

**Ranking: log-damped frequency, recency decay, and click-through (the strongest server-side signal — it
measures usefulness, not volume).** **Personal history is the strongest signal overall and can live entirely
on the device** — free, private, instant.

**Filter at build time AND at serve time**, because removal cannot wait for the next build — completing a real
person's name defamatorily has produced lawsuits, and **the asymmetry favours over-blocking** since nobody
reports a suggestion that never appeared. **And the trending layer is trivially cheap to attack** (~500
repetitions in a 10-minute window): fix it with the **counting rule — distinct users, rate-limited** — not with
a longer window.
