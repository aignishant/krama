---
day: 151
track: system-design
title: "Design a web crawler"
phase: "High-level design case studies"
status: written
---

# Design a web crawler

## 1. What this is, and why they ask it

A crawler starts from a few URLs, fetches each page, extracts the links in it, and repeats. **That is a
breadth-first search on a graph with a billion nodes that you do not own, cannot see in advance, and are only
allowed to touch politely.**

They ask it because **it is the one design that is transparently an algorithm.** The DSA lesson you have been
doing all month is the crawler: a frontier is a queue, a visited set is a hash set, and the crawl is BFS.
**The interview is about everything that goes wrong when the queue is on a hundred machines and the graph
fights back.**

And it fights back specifically. **Politeness** — hitting one site too fast is an attack, and you will be
blocked or sued. **Traps** — infinite calendars, session IDs in URLs, pages that generate links forever.
**Duplicates** — the same page under five URLs, and near-duplicates everywhere. **Scale** — a billion pages is
petabytes, and the visited set alone does not fit in memory.

The politeness constraint is the one that separates candidates, because it inverts the obvious design. **The
natural queue is one big FIFO, and that is exactly wrong** — it interleaves URLs from many hosts and hammers
whichever host happens to be popular. **The right answer is a queue per host**, and being able to say why is
worth more than the rest of the design.

By the end of this lesson you can design the frontier with politeness and priority, deduplicate at three
levels, handle traps, size the storage and bandwidth, and say what you would do about robots.txt.

---

## 2. The story

The census work paid four hundred rupees a day and Nirmala took it because it was three weeks and she needed
three weeks.

The instructions were simple. **Start at the corner of the lane. Every house, in order. Ask the questions,
fill the form, and at each house also ask which other houses in the ward have people living in them**, because
the ward map was eleven years old and half of it was wrong.

So by the end of the first morning she had a notebook with forty houses in it and she had visited nine.

**The list grew faster than she could work through it.** That was the first thing she understood, and it did
not stop being true for three weeks.

The second thing took two days. **She kept arriving at houses she had already done.** The same house, because
one person called it "the blue gate" and another called it "number 14" and a third called it "Sharma's place
behind the temple", and she had written all three in her book as three separate entries.

So she started writing the number on the gatepost, always, whatever anyone called it. **One name per house, and
check the list before walking.**

The third thing was the one that got her shouted at.

**She did four houses on the same street in twenty minutes** — they were next to each other and it seemed
efficient — and the fourth woman had already heard from the other three, and she said something about the
government sending people to bother the same street all morning, and she shut the door.

**After that Nirmala rotated.** One house here, then a house on the next street, then the street after, and
back. **Slower, and nobody shut a door on her again.**

And the last one, which she never entirely solved.

There was a building on the main road with flats numbered 1 to 40, and at flat 40 somebody told her there was
also a 40A, and at 40A they told her about 40B, **and she got to 40F before she understood that the man on the
ground floor had been inventing them.**

She wrote a rule in the front of her book that evening. **Nothing past the fortieth flat in any building.** Not
because it was right, but because there had to be a stopping point somewhere.

---

## 3. The idea in plain English

Nirmala built a crawler, including all four of the problems that matter, in the order they arrive.

**The loop is four steps and it is genuinely this simple:**

```
1. take a URL from the frontier
2. fetch the page
3. store it
4. extract the links, and add the unseen ones back to the frontier
```

**The frontier is the queue. The seen set is her notebook. The crawl is BFS**, and
[day 127](../day-127-graph-bfs/README.md)'s traversal is exactly the algorithm — the difference is that the
graph has a billion nodes, the edges are discovered by downloading them, and the nodes belong to other people.

**Problem one: the same page under many URLs.** Nirmala's blue gate.

**Normalise the URL before doing anything with it.** Lowercase the host, drop the default port, drop the
fragment after `#`, sort the query parameters, strip the tracking ones, resolve `.` and `..`. `HTTP://Example.
COM:80/a/../b?b=2&a=1#top` and `http://example.com/b?a=1&b=2` are the same page, and without normalisation you
fetch it twice and store it twice.

**Then hash the normalised URL and check a set.** At a billion URLs the set does not fit in memory as strings,
so store 8-byte hashes, or use a **Bloom filter** — [day 143](../day-143-what-dp-is/README.md)'s structure,
doing exactly this job at Google scale. **A Bloom filter can say "probably seen" wrongly**, which means
occasionally skipping a page you have never fetched. **For a crawler that is an acceptable loss** and it is
worth saying so explicitly, because it is a rare case where a false positive is genuinely fine.

**And separately, the same content under different URLs.** Mirrors, print versions, `?utm_source=` variants
that normalisation missed. **Hash the page content too** and skip the store if you have that hash already —
typically 20–30% of the web is exact duplicates. **Near-duplicates** — the same article with a different
advert — need **SimHash**, which produces similar fingerprints for similar documents, so you compare Hamming
distance rather than equality.

**Problem two: politeness, and this is the one that shapes the architecture.**

**One FIFO queue is the wrong design.** URLs from a popular host cluster together in the frontier — every page
on a site links to many other pages on the same site — so a single queue drains hundreds of URLs for one host
in a row and sends them all at once.

**The fix is a queue per host, and a worker that owns a host at a time.** Nirmala rotating streets. Each host
gets its own FIFO; a worker picks a host, fetches one URL, waits the politeness delay, fetches the next.
**One connection per host, and a delay of a second or so between requests** — or whatever `robots.txt` says
via `Crawl-delay`.

**And `robots.txt` is not optional.** Fetch `https://host/robots.txt` before crawling a host, cache it for a
day, and obey it. **Ignoring it gets your IP blocked within hours and can get you sued**, and an interviewer
asking about crawlers is listening for whether you mention it unprompted.

**Problem three: priority, because you cannot crawl everything.**

The frontier grows faster than you drain it, permanently — that is Nirmala's first observation and it never
stops being true. **So the order matters more than the throughput.**

**A front queue set for priority, a back queue set for politeness.** URLs enter a priority queue chosen by
importance — PageRank, update frequency, domain authority, depth from the seed. A router then moves them into
per-host back queues. **Two separate structures doing two separate jobs**, and combining them is the mistake:
a single priority queue cannot enforce politeness, and a single host queue cannot express priority.

**Problem four: traps, which is Nirmala's flat 40F.**

**Infinite spaces exist and are usually not malicious.** A calendar with a "next month" link generates URLs
forever. A shop with faceted filters generates a URL per combination — five filters with ten values each is a
hundred thousand pages of nearly identical content. Session IDs in URLs make every visit look new.

**Four defences, and none of them is clever:** a **maximum depth** from the seed, typically 10 to 20; a
**per-domain page cap**; a **URL length limit**, since generated URLs grow; and **detecting repeated path
segments** like `/a/b/a/b/a/b`. **All four are heuristics, and Nirmala's rule about the fortieth flat is the
honest description of them** — not right, but there has to be a stopping point.

**And the last piece: the crawl never finishes.** Pages change, so the crawler recrawls, and the interesting
part is deciding how often. **A news homepage changes hourly; an archived PDF never changes.** Track the
observed change rate per URL and recrawl proportionally — and use `If-Modified-Since` and `ETag` so that an
unchanged page costs a `304 Not Modified` and no body at all. **That one header cuts recrawl bandwidth by
roughly the fraction of pages that have not changed**, which is most of them.

---

## 4. The picture

The whole system:

```
   seeds
     |
     v
  +-----------+     +--------------+     +------------------+
  | FRONTIER  |---->|   FETCHER    |---->|  CONTENT STORE   |
  | (queues)  |     |  (workers)   |     |  (S3 / HDFS)     |
  +-----------+     +--------------+     +------------------+
     ^                     |                     |
     |                     v                     v
     |              +--------------+     +------------------+
     |              | LINK PARSER  |     | CONTENT HASH SET |
     |              +--------------+     | (exact dupes)    |
     |                     |             +------------------+
     |                     v
     |              +--------------+
     +--------------| URL SEEN SET |
      unseen only   | (Bloom /     |
                    |  hash store) |
                    +--------------+

  The cycle is BFS. Everything else is the frontier's internal design.
```

The frontier, which is the part that matters:

```
  FRONT QUEUES — priority                BACK QUEUES — politeness

   [ p1 ] high (news, popular)            host: bbc.co.uk    [u1 u2 u3]
   [ p2 ]                        ROUTER   host: wikipedia    [u4 u5]
   [ p3 ]                       -------->  host: smallblog    [u6]
   [ p4 ] low (deep, obscure)             host: shop.example [u7 u8 u9]
        |                                      ^
   selector picks by priority              ONE worker owns ONE host queue
   (p1 more often than p4)                 and waits the delay between
                                           its fetches

  TWO structures because they do TWO jobs. A single priority queue
  cannot enforce politeness; a single host queue cannot express priority.
```

Why one FIFO fails:

```
  SINGLE FIFO after crawling one page of bigsite.com:

   [ bigsite/a  bigsite/b  bigsite/c  ...  bigsite/z  other.com/1 ]
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
     100 workers pull these simultaneously
     -> 100 concurrent requests to ONE host
     -> that is indistinguishable from an attack
     -> blocked within minutes

  Pages link mostly to their own site, so the frontier is ALWAYS
  clustered by host. This is not an edge case; it is the normal state.
```

URL normalisation, which removes most duplicates for free:

```
  raw:  HTTP://Example.COM:80/a/../b/?utm_source=x&b=2&a=1#section

  lowercase scheme+host   http://example.com:80/a/../b/?utm_source=x&b=2&a=1#section
  drop default port       http://example.com/a/../b/?utm_source=x&b=2&a=1#section
  resolve . and ..        http://example.com/b/?utm_source=x&b=2&a=1#section
  drop fragment           http://example.com/b/?utm_source=x&b=2&a=1
  strip tracking params   http://example.com/b/?b=2&a=1
  sort query params       http://example.com/b/?a=1&b=2

  -> ONE canonical string, hashed to 8 bytes for the seen set.
```

The three levels of duplicate detection:

```
  level 1: SAME URL            normalise + hash        catches ~30% of links
  level 2: SAME CONTENT        SHA-256 of the body     catches ~25% of pages
  level 3: NEARLY SAME         SimHash + Hamming < 3   catches templated pages,
                                                       print versions, mirrors

  Level 1 saves the FETCH. Levels 2 and 3 only save the STORE and the
  index — the bytes have already crossed the network.
```

---

## 5. How it actually works

### URL normalisation

```python
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import posixpath, hashlib

TRACKING = {"utm_source", "utm_medium", "utm_campaign", "fbclid", "gclid"}

def normalise(url: str) -> str:
    parts = urlsplit(url)
    scheme, host = parts.scheme.lower(), parts.hostname or ""
    if (scheme, parts.port) in (("http", 80), ("https", 443)):
        netloc = host
    else:
        netloc = f"{host}:{parts.port}" if parts.port else host
    path = posixpath.normpath(parts.path or "/")          # resolves . and ..
    query = urlencode(sorted(
        (k, v) for k, v in parse_qsl(parts.query) if k not in TRACKING))
    return urlunsplit((scheme, netloc, path, query, ""))   # "" drops the fragment
```

**Sorting the query parameters is the one people forget**, and it matters: `?a=1&b=2` and `?b=2&a=1` are the
same page and hash differently without it.

**`posixpath.normpath` resolves `..`** — and note it also strips a trailing slash, which for some servers is a
different page. **That is a deliberate trade**: you lose a few legitimate pages and you kill a large class of
duplicates.

### The seen set at scale

```python
class SeenUrls:
    """8-byte hashes in a sharded key-value store. Exact, and it fits."""
    def __init__(self, store) -> None:
        self.store = store

    def add_if_new(self, url: str) -> bool:
        digest = hashlib.blake2b(normalise(url).encode(), digest_size=8).digest()
        return self.store.set_if_absent(digest, b"1")      # atomic
```

**`set_if_absent` must be atomic**, or two workers that discover the same URL simultaneously both think they
are first and it gets fetched twice. **Redis `SETNX` or a conditional put does this in one round trip.**

**The Bloom filter alternative**, when even 8 bytes per URL is too much:

```python
class SeenBloom:
    """~1.2 GB for 1 billion URLs at a 1% false-positive rate."""
    def __init__(self, bloom) -> None:
        self.bloom = bloom

    def add_if_new(self, url: str) -> bool:
        key = normalise(url)
        if key in self.bloom:          # may be a FALSE POSITIVE
            return False               # -> we skip a page we never fetched
        self.bloom.add(key)
        return True
```

**The false positive means silently never crawling a page**, and there is no way to detect it. **For a crawler
that is acceptable** — the web is larger than you will crawl anyway — and it is worth saying that trade out
loud rather than presenting the Bloom filter as free.

### The frontier

```python
import time, heapq
from collections import defaultdict, deque

class Frontier:
    def __init__(self) -> None:
        self.front: list[tuple[int, str]] = []                    # (priority, url)
        self.back: dict[str, deque[str]] = defaultdict(deque)     # host -> urls
        self.ready: list[tuple[float, str]] = []                  # (next_ok_at, host)

    def add(self, url: str, priority: int) -> None:
        heapq.heappush(self.front, (priority, url))
```

**Two structures, and the router between them is what moves URLs from one to the other**, keeping each back
queue non-empty without letting any host's queue grow unboundedly.

```python
    def next_url(self) -> str | None:
        """Pop the host whose politeness delay expired earliest."""
        if not self.ready:
            return None
        ready_at, host = self.ready[0]
        if ready_at > time.monotonic():
            return None                       # nothing is polite to fetch yet
        heapq.heappop(self.ready)
        url = self.back[host].popleft()
        if self.back[host]:                   # still work for this host
            heapq.heappush(self.ready, (time.monotonic() + self.delay(host), host))
        return url
```

**The `ready` heap keyed on "when may I next touch this host" is the whole politeness mechanism.** A host is
simply not available until its delay has passed. **`time.monotonic()`, not wall clock**, for
[day 123](../day-123-word-search-ii/README.md)'s reason.

### robots.txt

```python
from urllib.robotparser import RobotFileParser

class RobotsCache:
    def __init__(self, ttl: int = 86400) -> None:
        self.cache: dict[str, tuple[RobotFileParser, float]] = {}
        self.ttl = ttl

    def allowed(self, url: str, agent: str = "MyCrawler") -> bool:
        host = urlsplit(url).netloc
        entry = self.cache.get(host)
        if entry is None or time.time() - entry[1] > self.ttl:
            parser = RobotFileParser()
            parser.set_url(f"https://{host}/robots.txt")
            try:
                parser.read()
            except Exception:
                return True                   # unreachable robots.txt: allow
            self.cache[host] = (parser, time.time())
            entry = self.cache[host]
        return entry[0].can_fetch(agent, url)
```

**The cache is not an optimisation, it is politeness** — fetching `robots.txt` before every request would
itself be hammering the host. **One day is the conventional TTL.**

**And "unreachable means allow" is a choice.** Google treats a `5xx` on `robots.txt` as *disallow everything*
for a while, which is more conservative. **Either is defensible; say which you picked.**

### Content deduplication

```python
def content_hash(body: bytes) -> bytes:
    return hashlib.sha256(body).digest()      # exact duplicates

def simhash(text: str, bits: int = 64) -> int:
    """Similar documents get similar fingerprints."""
    vector = [0] * bits
    for token in text.split():
        h = int.from_bytes(hashlib.blake2b(token.encode(), digest_size=8).digest(), "big")
        for i in range(bits):
            vector[i] += 1 if (h >> i) & 1 else -1
    result = 0
    for i, weight in enumerate(vector):
        if weight > 0:
            result |= 1 << i
    return result

def near_duplicate(a: int, b: int, threshold: int = 3) -> bool:
    return bin(a ^ b).count("1") <= threshold     # Hamming distance
```

**SimHash is the interesting one**, because unlike a normal hash, **similar inputs give similar outputs** —
each token votes on each bit, so changing a few tokens flips only a few bits. **Two documents within a Hamming
distance of 3 are near-duplicates**, which catches the same article with a different advert.

### Trap detection

```python
MAX_DEPTH, MAX_URL_LENGTH, MAX_PER_DOMAIN = 20, 2000, 1_000_000

def is_trap(url: str, depth: int, domain_count: int) -> bool:
    if depth > MAX_DEPTH or len(url) > MAX_URL_LENGTH:
        return True
    if domain_count > MAX_PER_DOMAIN:
        return True
    segments = urlsplit(url).path.split("/")
    for i in range(len(segments) - 4):         # /a/b/a/b/a/b
        if segments[i:i + 2] == segments[i + 2:i + 4] == segments[i + 4:i + 6]:
            return True
    return False
```

**Every one of these is a heuristic that will occasionally reject a real page**, and that is the correct trade.
**An unbounded crawl of one calendar costs more than the handful of legitimate deep pages you lose.**

### The real systems

```
Apache Nutch      the open-source reference; Hadoop-based
Scrapy            Python, single-machine to medium scale
Heritrix          the Internet Archive's crawler
Common Crawl      a public crawl of billions of pages, on S3
Googlebot         the one everyone is really being asked about
```

**Common Crawl is worth naming**, because "I would check whether Common Crawl already has this" is a genuinely
good answer to a crawler question with a narrow purpose.

---

## 6. The numbers

**The crawl budget.**

```
1 billion pages per month

1,000,000,000 / 30 days / 86,400 s = ~386 pages/second

per machine: ~100 concurrent fetches, ~2 s average fetch
             = 50 pages/second/machine
-> 386 / 50 = 8 machines

round up for retries, DNS, parsing: ~20 machines
```

**Under twenty machines for a billion pages a month is smaller than people expect**, and it is worth saying,
because it reframes the problem: **the bottleneck is not compute, it is politeness and storage.**

**Bandwidth.**

```
average HTML page: ~100 KB compressed (~500 KB raw)

386 pages/s x 500 KB = 193 MB/s raw
                     = 1.5 Gbps sustained, inbound

per month: 1,000,000,000 x 500 KB = 500 TB downloaded
```

```
storing it compressed, ~100 KB per page:
  1,000,000,000 x 100 KB = 100 TB per month of crawl
  on S3 at $0.023/GB     = ~$2,300/month, growing every month
```

**Storage is the recurring cost and it accumulates**, which is why a real crawler stores the extracted text
rather than the raw HTML for anything but the most recent crawl.

**The seen set, which is the memory question.**

```
1 billion URLs

as full strings, average 80 bytes    = 80 GB      does not fit in memory
as 8-byte hashes                     = 8 GB       fits on ONE machine
as a Bloom filter, 1% false positive = 1.2 GB     fits comfortably
   (10 bits per element)
as a Bloom filter, 0.1%              = 1.8 GB
```

**Ten bits per element for 1% is the number to remember**, and the false-positive rate is the price: **1% of a
billion is ten million pages silently never crawled.** Whether that is acceptable is the design question, and
for a general web crawl it is.

**Politeness, and what it actually costs.**

```
one URL per host per second

a site with 100,000 pages
  = 100,000 seconds = 27.8 HOURS to crawl that one site

-> to crawl 386 pages/second overall, you need
   386 DIFFERENT HOSTS being crawled concurrently

That is the real constraint. Not bandwidth, not CPU — host diversity.
```

**That calculation is the best thing to say in this interview**, because it explains why the frontier is
designed the way it is: **the system is not throughput-bound, it is bound by how many distinct hosts it can
have in flight.**

**Recrawl economics.**

```
1 billion pages, recrawled monthly, 80% unchanged

WITHOUT If-Modified-Since:
  1,000,000,000 x 500 KB = 500 TB downloaded

WITH If-Modified-Since:
  200,000,000 changed  x 500 KB = 100 TB
  800,000,000 unchanged x ~1 KB (304 response) = 0.8 TB
  total ~101 TB

-> 5x less bandwidth, from one request header.
```

**Duplicate detection's payoff.**

```
of 1 billion fetched pages:
  ~25% exact duplicates    = 250,000,000 pages
  at 100 KB stored each    = 25 TB of storage avoided
  = ~$575/month saved, forever, and a cleaner index

  BUT the bytes were already downloaded. Content dedup saves
  STORAGE, not BANDWIDTH. Only URL dedup saves the fetch.
```

**That distinction is worth stating precisely**, because candidates often claim content hashing saves
bandwidth, and it does not.

**DNS, which is the surprise bottleneck.**

```
one DNS lookup per host, ~50-200 ms uncached

crawling 386 pages/s across 400 hosts, no cache
  -> 386 lookups/s at 100 ms each
  -> DNS becomes the slowest step in the pipeline

with a local caching resolver and a long TTL:
  -> ~1 lookup per host per hour
  -> 400 lookups/hour, negligible
```

**A dedicated DNS cache is a real component of a real crawler**, and mentioning it signals experience.

---

## 7. The trade-offs

**Breadth-first against priority-first.** Pure BFS is simple and treats a spam farm exactly like Wikipedia.
**Priority ordering by PageRank or domain authority gets useful pages sooner**, and it costs a scoring pipeline
and can starve legitimate small sites forever. **The frontier's two-tier design exists precisely because you
want both**, and neither structure alone can do it.

**Bloom filter against exact hashes for the seen set.** 1.2 GB against 8 GB, and the price is that **1% of
URLs are silently never crawled** — no error, no log line, no way to know which. **For a web crawler that is
fine** and for a crawler with a specific target list it is not, so the answer depends on whether missing pages
is a bug or a rounding error.

**Politeness against throughput, which is not really a trade.** You can crawl a site faster; you will be
blocked, and possibly sued, and the pages you lose permanently exceed what you gained. **The real lever is host
diversity** — crawl more sites concurrently, not one site harder — and a candidate who frames it that way has
understood the constraint.

**Trap heuristics reject real pages.** A depth limit of 20 loses genuinely deep archives; a per-domain cap
truncates large legitimate sites; a URL length limit drops pages with long legitimate query strings. **All
four are wrong sometimes and all four are necessary**, and the honest framing is Nirmala's: there has to be a
stopping point, and it is chosen rather than derived.

**Recrawl frequency against freshness.** Recrawling everything monthly wastes most of the bandwidth on pages
that did not change; recrawling by observed change rate is better and needs per-URL history and a model that
can be wrong in both directions. **`If-Modified-Since` makes the mistake cheap** — an unnecessary recrawl of an
unchanged page costs a `304` and no body — which is why it matters more than the scheduling cleverness.

**Storing raw HTML against storing extracted text.** Raw HTML is five times larger and lets you re-parse when
your extractor improves, which it will. **Extracted text is small and throws away information you cannot get
back without recrawling.** The usual answer is both, with raw HTML on cold storage and a short retention.

**When would I not build this?** **When someone has already crawled it.** Common Crawl publishes billions of
pages on S3 and downloading it is dramatically cheaper than crawling. When the target is a handful of sites
with APIs — **an API is better than scraping in every respect** and the politeness problem disappears. And
when the content is behind JavaScript, where a fetcher must run a headless browser, and **the cost per page
goes up by roughly fifty times** — which changes the machine count from twenty to a thousand and should be
raised before designing anything else.

---

## 8. In the interview

### How it gets asked

- *"Design a web crawler."* — the standard prompt, usually with a scale like a billion pages a month.
- *"How do you avoid crawling the same page twice?"* — three levels, and which one saves what.
- *"How do you avoid overwhelming a website?"* — the politeness question, and the queue design.
- *"What is a crawler trap and how do you handle it?"*
- *"How do you know when to recrawl?"*
- *"How does this run on a hundred machines?"*

### The first ninety seconds

> "The loop is four steps and it is genuinely simple: **take a URL from the frontier, fetch it, store it,
> extract the links, add the unseen ones back.** That is breadth-first search on a graph with a billion nodes,
> and the frontier is the queue and the seen set is the visited set.
>
> **Everything interesting is in the constraints, so let me take the four that shape the design.**
>
> **First, duplicates, at three levels.** Same URL — normalise it and hash it: lowercase the host, drop the
> default port and the fragment, sort the query parameters, strip tracking parameters, resolve dot-dot. **A
> billion URLs as strings is eighty gigabytes; as eight-byte hashes it is eight, and as a Bloom filter about
> 1.2.** Then same content under different URLs — hash the body, which catches maybe a quarter of the web.
> Then near-duplicates — SimHash, where similar documents give similar fingerprints and you compare Hamming
> distance. **Only the first level saves the fetch**; the other two save storage, and I would say that
> explicitly because it is often claimed the other way.
>
> **Second, politeness, and this is the constraint that inverts the obvious design.** One big FIFO queue is
> wrong, because pages link mostly to their own site, so the frontier is always clustered by host — a hundred
> workers pull a hundred URLs for the same host and send them simultaneously, which is indistinguishable from
> an attack. **So: a queue per host, and one worker owns a host at a time**, with a delay between fetches. And
> `robots.txt`, fetched once per host and cached for a day.
>
> **Third, priority, because the frontier grows faster than I drain it, permanently.** So the order matters
> more than the throughput. **Two tiers: front queues for priority, back queues for politeness**, with a router
> between them — because a single priority queue cannot enforce politeness, and a single host queue cannot
> express priority.
>
> **Fourth, traps.** Calendars with a next-month link forever, faceted shop filters, session IDs in URLs.
> **Depth limit, per-domain cap, URL length limit, repeated-segment detection** — all heuristics, all
> occasionally wrong, all necessary.
>
> **And here is the sizing point I would lead with, because it reframes the problem.** A billion pages a month
> is 386 pages a second, which is about twenty machines — small. **But at one request per host per second,
> 386 pages a second means 386 distinct hosts in flight at all times.** The system is not bandwidth-bound or
> CPU-bound. **It is bound by host diversity**, and that is what the frontier is really managing.
>
> **One thing I would ask first: does this need to render JavaScript?** Because a headless browser is about
> fifty times the cost per page, and that changes twenty machines into a thousand."

### The follow-ups

**"How do you avoid hitting one website too hard?"**

> "This is the constraint that decides the architecture, so let me say why the obvious design fails first.
>
> **A single FIFO frontier does not work, and not as an edge case — as its normal state.** Pages link
> overwhelmingly to their own site, so after fetching one page of a large site I have added a hundred URLs for
> that same host, contiguously, to the queue. **A hundred workers pull from the front of that queue and issue
> a hundred simultaneous requests to one server.** From the site's perspective that is a denial of service, and
> I get blocked within minutes.
>
> **So the back of the frontier is one queue per host**, and the invariant is that **at most one worker is
> assigned to a host at a time**. That worker fetches one URL, waits the politeness delay, fetches the next.
>
> **The mechanism is a heap keyed on 'the earliest time I may next touch this host'.** A host that was fetched
> half a second ago is simply not in the ready set yet. **And it must use a monotonic clock**, or an NTP
> correction makes hosts available early or late.
>
> **The delay comes from `robots.txt` if it specifies `Crawl-delay`, and otherwise a default** — a second is
> conventional, and adapting it to the server's observed response time is better, because a slow server is
> telling you something.
>
> **`robots.txt` itself: fetch once per host, cache for a day, obey it.** The cache is politeness, not
> optimisation — checking it before every request would itself be hammering the host. **And I would decide
> deliberately what to do when it is unreachable.** I would allow, because a transient error should not lose
> me a site; Google disallows for a period, which is more conservative. **Either is defensible; not having
> decided is not.**
>
> **And the consequence, which is the number worth saying:** at one URL per host per second, a site with a
> hundred thousand pages takes twenty-eight hours to crawl. **So overall throughput comes entirely from host
> diversity** — to sustain 386 pages a second I need 386 hosts in flight. **Crawling more sites concurrently,
> never one site harder.**"

**"What is a crawler trap, and what do you do?"**

> "An infinite or effectively infinite space of URLs that the crawler will happily walk forever, and most of
> them are not malicious — they are ordinary sites doing ordinary things.
>
> **The classic is a calendar.** Every month page has a 'next month' link, so there is a valid, distinct,
> fetchable URL for December 40,000. Nothing is wrong with the site; the space is just unbounded.
>
> **Faceted navigation is the expensive one.** A shop with five filters of ten values each generates a hundred
> thousand URLs of nearly identical content, all reachable, all distinct. **That is a hundred thousand fetches
> to learn nothing.**
>
> **Session IDs in URLs** make every visit look like new pages, so the same site is crawled endlessly under
> different identifiers.
>
> **And deliberate ones exist** — pages that generate random links to poison crawlers.
>
> **Four defences, and I would be honest that none is clever.** A **maximum depth** from the seed, around ten
> to twenty. A **per-domain page cap**. A **URL length limit**, because generated URLs grow. And
> **repeated-path-segment detection** for `/a/b/a/b/a/b`.
>
> **Beyond those, content-based detection helps**: if a hundred URLs on one domain all produce near-identical
> content by SimHash, that is a facet trap, and I would deprioritise the whole pattern rather than the
> individual URLs.
>
> **Every one of these rejects real pages sometimes.** A depth limit loses genuinely deep archives; a domain
> cap truncates large legitimate sites. **I would say plainly that they are heuristics chosen rather than
> derived, and that the trade is right** — an unbounded crawl of one calendar costs far more than the handful
> of deep pages lost. **The right way to run them is with logging**, so a site hitting a cap is visible and can
> be whitelisted, rather than silently truncated forever."

**"How do you decide when to recrawl a page?"**

> "The crawl never finishes — pages change — so this is really the whole steady-state problem, and the naive
> answer wastes most of the budget.
>
> **Recrawling everything monthly means about eighty percent of the bandwidth is spent on pages that did not
> change.** At a billion pages that is four hundred terabytes downloaded for nothing.
>
> **The cheap fix, which matters more than the clever one: `If-Modified-Since` and `ETag`.** Send the
> timestamp or the etag from last time; an unchanged page answers `304 Not Modified` with no body. **A
> kilobyte instead of five hundred.** At eighty percent unchanged that turns five hundred terabytes into about
> a hundred and one — **five times less bandwidth from one request header**, and it makes an unnecessary
> recrawl almost free, which changes how careful the scheduling has to be.
>
> **Then the scheduling itself: track the observed change rate per URL and recrawl proportionally.** A news
> homepage changes hourly and gets crawled hourly. An archived PDF has never changed in twenty visits and gets
> crawled every few months. **The estimator is simple** — exponential moving average of the interval between
> observed changes — and it self-corrects, because a page that changes when you did not expect it moves up.
>
> **Two signals I would use beyond that.** **The sitemap**, if the site publishes one, because `lastmod` is
> the site telling you directly and it is free. And **importance**, because a page nobody looks at does not
> need to be fresh — freshness is only valuable in proportion to traffic.
>
> **And I would set a floor and a ceiling.** Never more often than the politeness delay allows, and never less
> often than some maximum, because a page that has been static for years can still change and a crawler that
> has written it off will never notice."

### The model answer

*"Design a crawler for a search engine: one billion pages a month, respecting site owners, and the index must
be reasonably fresh."*

> "Let me start with the sizing, because one number reframes the whole problem.
>
> **A billion pages a month is 386 pages a second.** At a hundred concurrent fetches per machine and a two
> second average fetch, that is fifty pages a second per machine — **about eight machines, twenty with
> headroom.** Compute is not the problem.
>
> **But politeness is one request per host per second. So 386 pages a second requires 386 distinct hosts in
> flight, continuously.** That is the actual constraint, and everything in the frontier design follows from
> it.
>
> **The frontier, in two tiers.** Front queues hold URLs by priority — domain authority, depth from seed,
> observed change rate. A router moves them into back queues, one per host. A worker takes the host whose
> politeness delay expired earliest, fetches one URL, and the host goes back into the heap with a new ready
> time. **Two structures because they do two jobs**, and the router's real task is keeping enough distinct
> hosts populated to sustain the throughput.
>
> **Duplicate detection at three levels, and I would name what each one saves.** URL normalisation plus an
> eight-byte hash in a sharded store — the check must be atomic, or two workers both think they are first.
> **This is the only level that saves a fetch.** Then a SHA-256 of the body, catching maybe a quarter of pages
> as exact duplicates and saving twenty-five terabytes a month of storage. Then SimHash with a Hamming
> threshold of three for near-duplicates — print versions, mirrors, the same article with a different advert.
> **Levels two and three save storage and index quality, never bandwidth**, because the bytes have already
> arrived.
>
> **Seen set sizing: a billion URLs is eighty gigabytes as strings, eight as hashes, 1.2 as a Bloom filter at
> one percent.** I would use exact hashes, because **one percent of a billion is ten million pages silently
> never crawled, with no way to know which** — and for a search engine, invisible gaps in coverage are worse
> than eight gigabytes.
>
> **Politeness: `robots.txt` per host, cached a day, obeyed, with `Crawl-delay` honoured.** A `User-Agent` that
> identifies the crawler and links to a page explaining it, and a working way for site owners to complain.
> **That last part is not decoration** — it is the difference between a crawler that operates for years and one
> that gets IP-blocked across the web.
>
> **Traps: depth cap of twenty, per-domain cap, URL length limit, repeated-segment detection, plus
> content-based facet detection via SimHash.** Logged, so a truncated site is visible rather than silently
> lost.
>
> **Freshness, which the prompt asks for specifically.** Per-URL change-rate estimation with an exponential
> moving average, sitemaps' `lastmod` where available, and importance weighting — freshness matters in
> proportion to traffic. **And `If-Modified-Since` on every recrawl**, which turns eighty percent of the
> recrawl budget into `304`s and cuts monthly bandwidth from five hundred terabytes to about a hundred.
>
> **Storage: raw compressed HTML to object storage at roughly a hundred kilobytes a page — a hundred terabytes
> a month, about $2,300 — with a short retention, plus extracted text kept indefinitely.** Keeping raw HTML for
> a while matters because the extractor will improve and re-parsing is free while recrawling is not.
>
> **Distribution: partition the frontier by host hash**, so each machine owns a set of hosts entirely. **That
> makes politeness a local invariant rather than a distributed one**, which is the single biggest
> simplification available here — no coordination is needed to guarantee one worker per host. The seen set is
> sharded separately by URL hash.
>
> **Two things I would raise before building.** **Does this need JavaScript rendering?** A headless browser is
> roughly fifty times the cost per page, turning twenty machines into a thousand, so it should be a targeted
> decision per site rather than a default. **And a dedicated caching DNS resolver**, because at 386 fetches a
> second, uncached lookups at a hundred milliseconds each become the slowest step in the pipeline.
>
> **What I would monitor:** pages per second per machine, distinct hosts in flight — which is the real health
> metric — the `304` rate on recrawls, the frontier size, and `4xx`/`5xx` rates per host, because a spike on
> one host usually means I am being blocked and should back off before somebody has to email me."

---

## 9. Recall card

**The loop is BFS:** frontier → fetch → store → extract links → add unseen. **The frontier is the whole
design.**

**Politeness inverts the obvious structure.** A single FIFO clusters by host (pages link to their own site), so
a hundred workers hit one server at once. **Queue per host, one worker per host, a heap keyed on next-allowed
time** (monotonic clock). **`robots.txt` per host, cached a day, obeyed** — and decide in advance what an
unreachable one means.

**Two-tier frontier: front queues for priority, back queues for politeness**, with a router between — a single
priority queue cannot enforce politeness and a single host queue cannot express priority.

**Three levels of dedup, and only the first saves bandwidth.** Normalise + hash the URL (sort query params!);
SHA-256 the body (~25% exact dupes → 25 TB/month saved); **SimHash + Hamming ≤ 3** for near-duplicates.
**Seen set: 80 GB as strings, 8 GB as hashes, 1.2 GB as a Bloom filter at 1%** — and 1% of a billion is ten
million pages silently never crawled.

**The number that reframes the problem: 386 pages/s at 1 req/host/s means 386 distinct hosts in flight.**
Not bandwidth-bound, not CPU-bound — **host-diversity-bound.** A 100,000-page site takes 28 hours.

**Traps are calendars, facets and session IDs, not malice.** Depth cap, per-domain cap, URL length, repeated
segments — all heuristics, all sometimes wrong, all necessary; log them. **`If-Modified-Since` cuts recrawl
bandwidth ~5×** (500 TB → 101 TB at 80% unchanged). **Partition the frontier by host** so politeness stays a
local invariant.
