---
day: 159
track: system-design
title: "Design Netflix"
phase: "High-level design case studies"
status: written
---

# Design Netflix

## 1. What this is, and why they ask it

Yesterday you designed YouTube. **Netflix delivers video too, and almost every design decision is different**,
because the catalogue is different in one crucial way: **it is small, and you know what is in it in advance.**

YouTube ingests five hundred hours a minute from strangers. **Netflix has perhaps twenty thousand titles, all
licensed, all known weeks before anyone watches them.** That single fact changes everything downstream.

**Transcoding stops being a firehose and becomes a batch job you can spend real effort on** — per-title,
per-scene optimisation that would be absurd at YouTube's ingest rate.

**Delivery stops being reactive and becomes predictive.** You know that a series drops on Friday, so **you can
push the files to every edge on Wednesday** rather than waiting for a cache miss. That is the single biggest
difference between the two systems and it is the thing to lead with.

**And the recommendation system stops being a feature and becomes the product**, because with twenty thousand
titles and no search intent, **what appears on the home screen decides what gets watched.**

They ask it because **it is the best test of whether you compare rather than recite.** A candidate who
produces the YouTube answer again has missed the question. A candidate who says "the catalogue is small and
known in advance, so I precompute and pre-position everything" has understood it in one sentence.

By the end of this lesson you can design the ingest and encoding pipeline, the open-connect-style delivery
model, playback and the home page, and say what predictability buys.

---

## 2. The story

The lending library in the town had two rooms and Ranganathan had run it for twenty-six years, and the thing
he was known for was not the books.

**It was that he had them ready.**

The school announced its reading list in the last week of May, every year, the same seven or eight books.
**And every year, by the time the list came out, he already had eleven copies of each of them on the front
table.**

Not because he was clever. **Because it was the same list, more or less, and he had been watching it for
twenty-six years.**

His rival in the next town — a bigger shop, more books — did it the other way. **A boy would come in asking
for the poetry book, and the man would say he could get it by Thursday.** Which was true. And by Thursday the
boy had borrowed it from a friend.

**Ranganathan's whole method was that he knew what was coming.**

And there was a second part to it, which took him longer to work out.

**He did not keep the eleven copies in the two rooms.** There was not space. So he had an arrangement with the
tailor near the school, and the man who ran the tea stall by the college, **and each of them kept three or
four copies under the counter.**

**The books were near the people, before the people wanted them.**

It cost him something. He paid the tailor a little. And sometimes he was wrong — one year he stocked forty
copies of a book the school dropped, and they sat there for two years and he gave most of them away.

But the arithmetic was not close. **When he was right, which was most of the time, the boy walked in and
walked out with the book.**

And the third part, which was the one his son did not understand for years.

**Ranganathan spent a lot of time on the front table.**

Which books faced outwards. Which sat at eye level. Which were in the little stack by the door. **He rearranged
it constantly**, and he did it differently depending on who was in the room — the college students got one
arrangement, the schoolchildren another.

His son said the books were the same wherever you put them.

**"There are four thousand books here," his father said, "and the boy will look at eleven of them. I decide
which eleven."**

---

## 3. The idea in plain English

Ranganathan is Netflix. **Know what is coming, put it near the people before they ask, and control the front
table.**

**Start with the comparison, because it is the answer to the question.**

```
                        YouTube                  Netflix
  catalogue           500 hrs/minute, from      ~20,000 titles, licensed,
                      anyone                    known weeks in advance
  encoding            must be fast; a firehose  a BATCH JOB, optimise hard
  content per title   watched once, mostly      watched millions of times
  delivery            reactive: cache on miss   PREDICTIVE: push before release
  discovery           search + recommendation   recommendation IS the product
  the hard part       ingest scale              delivery economics + ranking
```

**Say that table's first row and its consequence in the first minute.** Everything else follows from
"the catalogue is small and known".

**Now the four things it buys.**

**One: encoding becomes a batch job you can spend effort on.**

At YouTube you transcode as fast as possible because there is a queue behind you. **At Netflix a title is
encoded once and watched millions of times**, so **an hour of extra compute that saves two percent of the
bitrate pays for itself forever.**

**Which makes per-title and per-shot encoding worth doing.** A cartoon and a dark action film do not need the
same bitrate at the same resolution — **so instead of a fixed ladder, you compute the best ladder for each
title**, and even for each scene. **Netflix published exactly this**, and the reported saving is around twenty
percent of the bitrate at the same perceived quality.

**Twenty percent off the largest line on the bill is enormous**, and it is only worth the effort because the
encode is amortised over millions of views.

**Two: delivery becomes predictive, and this is the biggest difference.**

**YouTube's edge caches fill on a miss.** The first viewer in a region pays the latency of fetching from
origin.

**Netflix knows what is coming.** A series releases on Friday at midnight; **the files are pushed to every
edge server on Wednesday**, during off-peak hours, when bandwidth is cheap and nobody is watching.

**So on Friday there are no cache misses at all** — every viewer is served from a machine inside their own
internet provider's network, and the origin serves nothing.

**And the edge machines live inside ISP networks**, which is the Open Connect model: Netflix gives an ISP a
box, the ISP racks it, and Netflix's traffic never crosses an expensive transit link. **The ISP saves transit
costs and Netflix saves delivery costs**, which is why both sides agree.

**That arrangement is only possible because the catalogue is small enough to fit.** Twenty thousand titles is
a few hundred terabytes — **a box you can ship.** YouTube's exabytes are not.

**Three: the recommendation system is the product.**

**A user opens the app with no query.** There is no search intent, no link they followed. **The home page is
the entire interface**, and what is on it determines what is watched.

**The structure is rows**, and each row is a separate ranking problem: continue watching, because you watched
X, trending now, new releases. **Rows are personalised, ordered, and the artwork within them is chosen per
user** — the same film shown with a different image depending on what the model thinks appeals.

**And it is precomputed.** Ranking twenty thousand titles per user at request time would be expensive and
slow. **The home page is computed in batch — nightly, or on significant events — and cached**, with a small
real-time layer for "continue watching" and very recent activity.

**Which is a genuine architectural consequence of the catalogue being small**: precomputing a page over twenty
thousand items is feasible, and doing it over YouTube's billions is not.

**Four: playback, which is mostly yesterday's design with three additions.**

**Adaptive bitrate over static segments**, exactly as before. **The additions are:**

**Digital rights management.** The content is licensed, so it is encrypted and the player must obtain a
decryption licence from a licence server. **Widevine, PlayReady and FairPlay** are the three systems, one per
platform ecosystem, **and supporting all three means encrypting the content three ways** — or using CMAF with
common encryption to store one copy.

**Resume across devices.** Watch position is a small write, very frequently — every few seconds, per user, per
title. **That is a high-write, tiny-payload workload**, quite unlike everything else in the system, and it
needs its own store.

**And offline download**, which is DRM again with a different licence policy: a licence that works without a
network, for a limited time.

**Finally, the thing worth saying about scale.**

**Netflix's peak is a huge fraction of the internet's traffic in some countries**, and it is highly
predictable: evenings, weekends, and enormous spikes when a major title releases. **Predictable peaks are much
easier to plan for than unpredictable ones**, and they justify capacity that sits idle at four in the
morning.

---

## 4. The picture

The two systems, side by side:

```
   YOUTUBE                         NETFLIX

   500 hrs/min ingest              ~20,000 titles, known in advance
        |                                |
   TRANSCODE FAST                  ENCODE WELL (per-title, per-shot)
   6 fixed renditions              a ladder computed for THIS title
   ~1x real-time, at scale         hours per title, amortised over
                                   millions of views
        |                                |
   REACTIVE CDN                    PREDICTIVE PUSH
   cache fills on a MISS           files pushed to every edge BEFORE
   first viewer pays               release, during off-peak
        |                                |
   search + recommendation         RECOMMENDATION IS THE INTERFACE
   user usually knows what         no query; the home page decides
   they want                       what gets watched
```

Predictive placement, which is Ranganathan's tailor:

```
  WEDNESDAY (off-peak, 03:00 local)

    origin ---- push new season ----> [edge in ISP A]
           ---- push new season ----> [edge in ISP B]
           ---- push new season ----> [edge in ISP C]   ... thousands

    bandwidth is cheap, nobody is watching, no user waits

  FRIDAY 00:00 (release)

    10,000,000 viewers press play
    every single one is served from a box INSIDE their own ISP
    origin traffic: ~ZERO

  Compare a reactive CDN: the first viewer in each region waits for
  an origin fetch, and the origin sees a thundering herd at 00:00.
```

Why Open Connect works for both sides:

```
  WITHOUT an embedded cache        WITH one

  Netflix origin                   Netflix origin
       |                                | (one push, off-peak)
   TRANSIT LINK  $$$$                   v
       |                           [ OCA box inside the ISP ]
   ISP network                          |
       |                            ISP network (free, internal)
    viewer                              |
                                     viewer

  the ISP pays for transit          the ISP pays nothing
  Netflix pays for egress           Netflix ships a box once

  BOTH SIDES SAVE. That is why ISPs agree to rack them.
  And it only works because the catalogue FITS on a box.
```

Per-title encoding, and why it is worth the compute:

```
  FIXED LADDER (YouTube-style)
    every title: 1080p @ 5 Mbps, 720p @ 2.5, 480p @ 1 ...

    an animated film at 1080p looks perfect at 2 Mbps
       -> 3 Mbps wasted on EVERY VIEW
    a dark, grainy action film needs 8 Mbps at 1080p
       -> visibly bad at 5

  PER-TITLE LADDER
    compute the quality-vs-bitrate curve for THIS title
    pick the bitrates where quality actually improves

    reported saving: ~20% of bitrate at the same perceived quality

  WHY IT IS WORTH HOURS OF COMPUTE:
    encode once, serve millions of times
    20% of the largest line on the bill, forever

  WHY YOUTUBE CANNOT: 500 hours/minute arriving, most of it
  watched a handful of times. The amortisation is not there.
```

The home page as rows, which is the product:

```
  +------------------------------------------------+
  | Continue Watching        [real-time, per user] |
  +------------------------------------------------+
  | Because you watched X    [batch, per user]     |
  +------------------------------------------------+
  | Trending Now             [batch, per region]   |
  +------------------------------------------------+
  | New Releases             [batch, per region]   |
  +------------------------------------------------+

  each ROW is a separate ranking problem
  the ORDER of the rows is itself ranked
  the ARTWORK for each title is chosen per user

  precomputed nightly and cached, with a thin real-time layer
  for "continue watching" and very recent activity

  -> possible because the catalogue is 20,000 items.
     Not possible over billions.
```

---

## 5. How it actually works

### Ingest and encoding

```python
def ingest_title(title_id: str, master_file: str) -> None:
    analysis = analyse_complexity(master_file)         # per-shot complexity
    ladder = compute_ladder(analysis)                  # bitrates for THIS title
    shots = detect_shot_boundaries(master_file)

    for shot_index, (start, end) in enumerate(shots):
        for height, bitrate in ladder:
            queue.publish("encode", {
                "title_id": title_id, "shot": shot_index,
                "start": start, "end": end,
                "height": height, "bitrate": bitrate,
            })
    job_store.expect(title_id, len(shots) * len(ladder))
```

**`compute_ladder(analysis)` is the whole difference from yesterday.** YouTube uses a fixed list of six
renditions; **here the list is computed from the content**, because a cartoon and a grainy thriller need
different bitrates for the same perceived quality.

**Splitting by shot rather than by fixed duration** is the refinement: **a scene's complexity is roughly
constant within a shot and changes at cuts**, so per-shot encoding targets each one appropriately.

**The parallelism is yesterday's** — one job per shot per rendition — but the *goal* is different: **YouTube
chunks for latency; Netflix chunks because it has to be parallel anyway and the quality work is the point.**

### Predictive distribution

```python
def schedule_prepositioning(title_id: str, release_at: float) -> None:
    popularity = forecast.predicted_demand(title_id)   # by region
    for region, expected_viewers in popularity.items():
        for edge in edges_in(region):
            if expected_viewers > edge.threshold:
                push_jobs.schedule(
                    title_id, edge,
                    at=off_peak_window(edge, before=release_at),
                )
```

**`off_peak_window` is the key idea**: the push happens at three in the morning local time, **when the edge's
bandwidth is idle and nobody is watching.** The transfer is free in every sense that matters.

**And it is per edge, not global**, because a title popular in one country may be irrelevant in another —
**pushing everything everywhere would need far more storage per box than exists.**

**The forecast can be wrong**, and the consequence is Ranganathan's forty unwanted copies: **a box holding a
title nobody watches, which is wasted space rather than a failure.** The reverse — a title not pushed that
suddenly trends — falls back to fetching from a regional origin.

### The playback path

```python
@app.post("/play")
def start_playback(user_id: int, title_id: str, device: dict) -> dict:
    if not entitlements.allows(user_id, title_id, device["region"]):
        return {"error": "not available in your region"}, 403

    edge = steering.best_edge_for(user_id, device)      # by ISP, latency, health
    return {
        "manifest": f"https://{edge}/{title_id}/master.mpd",
        "licence_url": "https://licence.example.com/acquire",
        "start_position": watch_state.position(user_id, title_id),
    }
```

**`steering.best_edge_for` is a real system**, and it is more than DNS geolocation: **it picks the edge inside
the user's own ISP where one exists**, falls back to a nearby one, and routes around unhealthy boxes.

**`entitlements` is the licensing check** — content rights are per country and per date, so **a title
available in one region genuinely does not exist in another**, and that check belongs before anything else.

**And `start_position` comes back with the manifest**, so resume is one round trip rather than two.

### DRM, in outline

```python
@app.post("/licence")
def acquire_licence(user_id: int, title_id: str, drm_system: str,
                    challenge: bytes) -> bytes:
    if not entitlements.allows(user_id, title_id, region_of(user_id)):
        raise Forbidden
    if device_count(user_id) > plan_limit(user_id):
        raise TooManyStreams
    key = content_keys.get(title_id)
    return drm[drm_system].issue(challenge, key, policy=policy_for(user_id))
```

**The licence server, not the CDN, is where policy is enforced** — concurrent stream limits, region checks,
offline expiry. **The segments themselves are encrypted static files that anyone can download and nobody can
play**, which is what lets them sit on an ISP's box safely.

**Three DRM systems for three ecosystems** — Widevine for Android and Chrome, PlayReady for Windows and Xbox,
FairPlay for Apple. **With CMAF and common encryption you store one encrypted copy and issue three kinds of
licence**; without it you store the content three times.

### Watch position, which is a surprising workload

```python
def report_position(user_id: int, title_id: str, seconds: float) -> None:
    key = f"pos:{user_id}:{title_id}"
    redis.set(key, seconds, ex=90 * 86400)             # fast path
    if int(seconds) % 30 == 0:                         # durable path, sampled
        queue.publish("watch_state", {"user": user_id, "title": title_id,
                                      "seconds": seconds})
```

**Two paths again.** The Redis write is what "continue watching" reads — **frequent, tiny, and losing a few
seconds of it costs nothing.** The sampled queue write is what survives a Redis failure and what feeds
analytics.

**The volume is the surprise:** every playing device reports every few seconds, so **this is a higher write
rate than anything else in the system** — and each write is thirty bytes.

### The home page

```python
def home_page(user_id: int) -> list[dict]:
    rows = precomputed_rows.get(user_id)                # built nightly, cached
    if rows is None:
        rows = fallback_rows(region_of(user_id))        # popular, non-personalised
    live = [continue_watching_row(user_id)]             # real-time
    return live + rows
```

**Precomputed plus a thin real-time layer** is the shape. **The expensive personalised ranking runs in batch;
only the things that must be current are computed per request.**

**And the fallback matters:** a new user, or one whose batch job has not run, **must get a sensible page
rather than an empty one** — popular titles for their region, which is also what a cold start looks like.

### The real systems

```
Open Connect     Netflix's own CDN: appliances placed inside ISPs
AWS              everything except delivery — control plane, encoding,
                 recommendations, the API
Cassandra        viewing history and watch positions
EVCache          Netflix's memcached layer, for the home page and positions
Widevine /
PlayReady /
FairPlay         DRM, one per ecosystem
VMAF             Netflix's perceptual quality metric — the thing that makes
                 per-title encoding measurable
Chaos Monkey     deliberately killing instances to prove resilience
```

**VMAF is the good one to name**, because it is what makes per-title encoding possible at all: **you cannot
optimise bitrate against quality without a metric for quality that matches what people actually see.**

---

## 6. The numbers

**Scale.**

```
~270,000,000 subscribers
~2 hours watched per subscriber per day
= ~540,000,000 hours/day

peak concurrency: ~15% of subscribers in the evening
= ~40,000,000 concurrent streams
```

**Catalogue, which is the number that changes everything.**

```
~20,000 titles, average ~1.5 hours = ~30,000 hours of content

per hour of content, all renditions plus audio tracks and subtitles:
  ~15 GB (similar to yesterday)

30,000 x 15 GB = ~450 TB for the entire catalogue

compare YouTube: 4 EB/year.
-> Netflix's ENTIRE catalogue is ~0.01% of one year of YouTube uploads
```

**Four hundred and fifty terabytes is the whole system's content**, and that is the fact everything else
follows from: **it fits on a handful of drives, so you can ship it to every ISP.**

**Delivery.**

```
540,000,000 hours/day at an average ~4 Mbps (higher than YouTube:
big screens, good connections, longer sessions)

540e6 x 3,600 s x 4 Mbps / 8 = 972,000,000 GB/day
                             = ~970 PB/day

peak: 40,000,000 concurrent x 4 Mbps = 160 Tbps
```

**A hundred and sixty terabits a second at peak.** On a commercial CDN at a cent a gigabyte that is about
**$9.7 million a day**, or three hundred million a month.

```
with Open Connect:
  the marginal cost of a byte served from an ISP-embedded box is
  ~the amortised hardware + power, not a per-GB price

  ~18,000 appliances worldwide, ~$10-30k each, ~5-year life
  = ~$300M capital, ~$5M/month amortised
  + operations

-> roughly 50x cheaper than buying delivery, and it is the single
   largest engineering decision the company has made.
```

**Prepositioning, and what it saves:**

```
a major release: 10,000,000 viewers in the first 24 hours

REACTIVE CDN:
  first viewer per edge pays an origin fetch
  ~18,000 edges x ~15 GB per title = 270 TB from origin
  concentrated in the first minutes -> a thundering herd

PREDICTIVE PUSH:
  the same 270 TB, moved at 03:00 local over several days
  origin traffic at release: ~0
  and it is off-peak bandwidth, which is close to free

Same bytes. Completely different cost and risk profile.
```

**Per-title encoding, quantified:**

```
encoding a 2-hour film with per-shot optimisation:
  ~1,000 shots x ~10 renditions = 10,000 jobs
  each ~30 s of CPU = ~83 CPU-hours per title
  plus the analysis passes: call it ~150 CPU-hours

20,000 titles x 150 = 3,000,000 CPU-hours, ONCE
at $0.03/hour = ~$90,000 total for the whole catalogue

THE SAVING: ~20% of 970 PB/day
  = ~194 PB/day of bandwidth not sent

-> ninety thousand dollars of compute, once, against a fifth of
   the largest recurring line, forever.
   Compare YouTube: 4.3M CPU-hours PER DAY just to keep up.
```

**That comparison is the best thing in this lesson**: **YouTube spends more on transcoding in one day than
Netflix spends encoding its entire catalogue.**

**Watch positions, the surprising workload:**

```
40,000,000 concurrent streams, each reporting every 5 s
= 8,000,000 writes/second

each write ~30 bytes

-> higher write rate than the message rate of WhatsApp,
   for the smallest payloads in this course

Redis/EVCache absorbs it; a sampled subset goes to Cassandra
for durability and analytics.
```

**The home page:**

```
270,000,000 subscribers x ~40 rows x ~50 titles per row
  = the precomputed page is a few KB per user
  270e6 x 5 KB = ~1.4 TB of cached pages

recomputed nightly:
  270,000,000 users / 86,400 s = ~3,100 users/second of batch ranking
  -> a large but ordinary batch job

vs ranking 20,000 titles per user at request time:
  40,000,000 peak concurrent x a model over 20,000 items
  -> not viable, which is why it is precomputed
```

**The bill, ranked:**

```
delivery (Open Connect, amortised)   ~$5-10M/month
AWS: control plane, encoding,        ~$30M/month
  recommendations, data
content licensing                    ~$1.5 BILLION/month
                                     ---------------------
infrastructure is ~2% of the content spend

-> which is the real difference from YouTube. There the
   infrastructure IS the business; here it is a rounding error
   next to paying for the shows.
```

---

## 7. The trade-offs

**Predictive pre-positioning against reactive caching.** Prediction eliminates cache misses at release and
moves the bytes at off-peak, which is close to free. **It costs storage on every edge box for content that may
not be watched there** — Ranganathan's forty unwanted copies — and it depends on a forecast that is sometimes
wrong. **The fallback to a regional origin makes being wrong cheap**, which is what makes the bet worth
taking.

**Per-title encoding against a fixed ladder.** Per-title saves about twenty percent of the delivery bill
forever, at the cost of hours of compute per title and a much more complex pipeline. **It is only justified
because a title is encoded once and watched millions of times** — the amortisation is the whole argument, and
**it is exactly why YouTube cannot do it.**

**Building the CDN against buying it.** Open Connect is roughly fifty times cheaper at this volume and is a
multi-year capital and operational commitment: **hardware, logistics, relationships with thousands of ISPs,
and a team.** Below a few petabytes a month it would be an absurd thing to build. **Knowing that the
break-even exists, and that Netflix is far past it, is the answer.**

**DRM against openness.** DRM is a licensing requirement — **studios will not license content without it** — so
it is not really a choice. It costs three encryption systems, a licence server on the critical path of every
playback start, and **a whole class of platform-specific bugs**. CMAF with common encryption reduces the
storage cost from three copies to one.

**Precomputed home pages against real-time ranking.** Precomputing is cheap to serve and is stale by up to a
day. **Real-time would reflect what you watched five minutes ago and cannot be afforded at forty million
concurrent users.** The hybrid — batch rows plus a thin real-time layer for continue-watching — is what
everybody builds, **and the honest description is that most of the page is yesterday's opinion.**

**Regional licensing, which is a constraint rather than a trade.** The same title is available in some
countries and not others, and the rights change on fixed dates. **That means the catalogue is genuinely
different per region**, entitlement checks are on the playback path, and **content sometimes disappears from
a user's list**, which is a product problem with no technical solution.

**When would I not build this?** **Almost all of it, almost always.** For a video product below a few
petabytes a month, **a commercial CDN with reactive caching is cheaper and simpler than anything here.**
Per-title encoding is only worth it when views per title are in the millions. **And the recommendation system
is worth building only when the catalogue is large enough to need it and small enough to rank** — with two
hundred titles, a hand-curated home page beats a model.

---

## 8. In the interview

### How it gets asked

- *"Design Netflix."* — and the interviewer usually wants to hear how it differs from YouTube.
- *"How is this different from YouTube?"* — asked directly, and it is the whole question.
- *"A new season drops at midnight and ten million people watch it. What happens?"*
- *"How do you decide what bitrate to encode at?"* — the per-title question.
- *"How does the home page work?"*
- *"Why does Netflix run its own CDN?"*

### The first ninety seconds

> "The right way into this is the comparison with YouTube, because **one fact about the catalogue changes
> almost every decision.**
>
> **YouTube ingests five hundred hours a minute from strangers. Netflix has about twenty thousand titles, all
> licensed, all known weeks before anyone watches them.**
>
> **And the whole catalogue is about four hundred and fifty terabytes** — which is roughly a hundredth of one
> percent of a year of YouTube uploads. **It fits on a handful of drives, and that is what makes everything
> else possible.**
>
> **Four consequences, and I would take them in order of how much they matter.**
>
> **One: delivery becomes predictive rather than reactive.** A CDN normally fills its cache on a miss, so the
> first viewer in each region waits. **Netflix knows a series drops on Friday, so the files are pushed to every
> edge on Wednesday, at three in the morning local time**, when bandwidth is idle. **On Friday there are no
> cache misses at all.**
>
> **And the edges are inside ISP networks** — Netflix ships a box, the ISP racks it, and the traffic never
> crosses a paid transit link. **Both sides save**, which is why ISPs agree. **And it only works because the
> catalogue fits on a box.**
>
> **Two: encoding becomes a batch job worth optimising.** A title is encoded once and watched millions of
> times, **so hours of extra compute that save twenty percent of the bitrate pay for themselves forever.**
> That justifies per-title and even per-shot encoding — a cartoon and a grainy thriller genuinely need
> different bitrates. **YouTube cannot do this**, because its content is watched a handful of times and there
> is a firehose behind it.
>
> **The arithmetic is striking: YouTube spends more CPU on transcoding in one day than Netflix spends encoding
> its entire catalogue.**
>
> **Three: recommendations are the product, not a feature.** A user opens the app with no query. **The home
> page is the entire interface**, it is rows, each row is a separate ranking problem, and it is **precomputed
> nightly** — ranking twenty thousand titles per user at request time is not viable at forty million
> concurrent users, and precomputing over twenty thousand items is, which is again the catalogue size doing
> the work.
>
> **Four: playback is yesterday's adaptive bitrate plus DRM, entitlements and resume.**
>
> **Which of those would you like me to go deep on?**"

### The follow-ups

**"A new season drops at midnight and ten million people watch it. What happens?"**

> "Almost nothing dramatic, and the reason it is not dramatic is the whole design.
>
> **With a reactive CDN it would be a thundering herd.** At midnight, the first viewer at each of about
> eighteen thousand edge locations triggers an origin fetch of roughly fifteen gigabytes of content —
> **two hundred and seventy terabytes pulled from origin, concentrated into the first few minutes**, while
> every one of those first viewers waits.
>
> **Netflix does not do that, because it knows the release date.**
>
> **The files were pushed days in advance.** Each edge received its copy at about three in the morning local
> time, spread over several nights, **when its bandwidth was idle and nobody was watching.** The same two
> hundred and seventy terabytes moved, at close to zero marginal cost, with no user waiting.
>
> **So at midnight, origin traffic is essentially zero.** Every viewer is served from a box inside their own
> internet provider's network.
>
> **The pushing is per edge, not global**, because a box cannot hold everything and a title popular in one
> country may be irrelevant in another. **A demand forecast decides which edges get which titles.**
>
> **And the forecast is sometimes wrong**, in two directions. **Over-pushing wastes space on a box** — cheap,
> and the content is evicted eventually. **Under-pushing means a title that unexpectedly trends is not on the
> local box**, and those viewers fall back to a regional origin — slower, but correct, and it self-corrects
> within minutes as the miss triggers a fill.
>
> **The failure mode I would actually plan for is concurrency, not bandwidth.** Ten million people pressing
> play in the same minute is ten million licence acquisitions and ten million playback-start API calls.
> **The licence server and the playback API see a spike that the CDN does not**, because the CDN was
> pre-warmed and they cannot be. **That is where I would put the load testing and the autoscaling headroom**,
> and it is the non-obvious part of the answer."

**"How do you decide what bitrate to encode at?"**

> "Per title, and increasingly per shot — and the interesting part is why that is affordable here and not at
> YouTube.
>
> **The naive approach is a fixed ladder**: every title gets 1080p at five megabits, 720p at two and a half,
> and so on. **And it is wrong in both directions at once.**
>
> **An animated film looks perfect at 1080p and two megabits** — large flat areas of colour compress
> extremely well — **so three megabits are wasted on every single view.** **A dark, grainy action film needs
> perhaps eight megabits at 1080p** and looks visibly bad at five. **The same ladder over-serves one and
> under-serves the other.**
>
> **So: compute the ladder for each title.** Encode at many candidate bitrates, measure the resulting quality,
> and pick the points where quality actually improves. **The refinement is to do it per shot**, because
> complexity is roughly constant within a shot and changes at cuts.
>
> **The thing that makes this possible is a quality metric that matches human perception.** Netflix built VMAF
> for exactly this — **you cannot optimise bitrate against quality without a number for quality that agrees
> with what people see**, and older metrics like PSNR do not.
>
> **The reported saving is about twenty percent of bitrate at the same perceived quality.**
>
> **And here is the economics, which is the real answer.** Per-shot encoding a two-hour film is maybe a
> hundred and fifty CPU-hours. **Twenty thousand titles is three million CPU-hours — about ninety thousand
> dollars, once.** The saving is a fifth of the largest recurring line on the bill, forever.
>
> **YouTube cannot make that trade**, and it is worth saying why precisely: **its content is watched a handful
> of times on average, so there is nothing to amortise the extra compute over**, and it has four hundred and
> thirty thousand hours arriving per day, so there is a queue behind every encode. **Netflix optimises because
> it can afford to think; YouTube optimises for throughput because it cannot.**"

**"Why does Netflix run its own CDN?"**

> "Because at a hundred and sixty terabits a second, buying delivery costs more than building it by about a
> factor of fifty — **and because the catalogue is small enough to make building it possible.**
>
> **The arithmetic first.** Five hundred and forty million hours watched a day at around four megabits is
> nearly a petabyte a day, **and at a commercial rate of a cent a gigabyte that is about ten million dollars a
> day.** Three hundred million a month, on delivery alone.
>
> **Open Connect is a different model entirely.** Netflix builds appliances — ordinary servers full of drives —
> **and gives them to internet providers, who rack them in their own data centres for free.**
>
> **Both sides win, which is why it works.** The ISP's subscribers pull Netflix traffic from a box inside the
> ISP's own network, **so the ISP does not pay for transit** — and Netflix is a large fraction of that ISP's
> traffic, so the saving is real. Netflix ships hardware once instead of paying per gigabyte forever.
>
> **Roughly eighteen thousand appliances at ten to thirty thousand dollars each, on a five-year life, is
> around five million dollars a month amortised** — against three hundred million to buy the same delivery.
>
> **And the crucial enabler is that the catalogue fits.** Four hundred and fifty terabytes is a box you can
> build. **YouTube's exabytes are not**, which is why Google's edge strategy is different — it caches
> reactively and cannot pre-position, because it does not know what will be watched.
>
> **What it costs is not money.** It is a multi-year commitment: **hardware design, logistics, and
> relationships with thousands of individual internet providers** — which is an organisational capability, not
> a technical one, and it is much harder to acquire than the engineering.
>
> **So the honest framing is that this is right at Netflix's scale and absurd below it.** For a video product
> serving a few petabytes a month, **a commercial CDN is cheaper than the team you would need**, and I would
> want to know roughly where the crossover is before proposing it anywhere else."

### The model answer

*"Design Netflix. Two hundred and seventy million subscribers, twenty thousand titles, global."*

> "I want to lead with the comparison to a user-generated video platform, because **one fact about the
> catalogue determines most of the design.**
>
> **Twenty thousand titles at about fifteen gigabytes per hour of content is roughly four hundred and fifty
> terabytes for the entire catalogue** — against exabytes a year for YouTube. **The catalogue is small, and
> every title's release date is known weeks in advance.** Everything below follows from that.
>
> **Sizing.** Two hundred and seventy million subscribers watching about two hours a day is 540 million hours
> a day. At an average four megabits — higher than YouTube because it is big screens and long sessions — that
> is **about 970 petabytes a day, and 160 terabits a second at evening peak.**
>
> **Delivery: Open Connect, and this is the largest engineering decision in the system.** Netflix-built
> appliances placed inside ISP networks. **At commercial CDN rates this traffic would be three hundred million
> dollars a month; amortised hardware is around five.** Fifty times cheaper — **and it is only possible because
> four hundred and fifty terabytes fits on a box you can ship.**
>
> **And delivery is predictive, not reactive.** A release date is known, so **content is pushed to every
> relevant edge days ahead, at three in the morning local time.** At midnight on release there are no cache
> misses and origin traffic is essentially zero. **A reactive CDN would pull two hundred and seventy terabytes
> from origin in the first minutes while the first viewer at every edge waits.**
>
> **Which edges get which titles comes from a demand forecast**, because a box cannot hold everything.
> Over-pushing wastes space; under-pushing falls back to a regional origin and self-corrects. **Being wrong is
> cheap in both directions, which is what makes the bet sound.**
>
> **Encoding: per-title, and per-shot within a title.** Compute the quality-versus-bitrate curve for this
> content and pick the ladder from it, measured with a perceptual metric — **you cannot optimise against
> quality without a number for quality that agrees with human eyes.** About twenty percent bitrate saving at
> the same perceived quality.
>
> **The economics are the argument: three million CPU-hours for the entire catalogue, once — about ninety
> thousand dollars — against a fifth of the delivery bill, forever.** YouTube spends more on transcoding in
> one day. **The difference is amortisation: encode once, serve millions of times.**
>
> **Playback: adaptive bitrate over encrypted static segments, plus three things a user-generated platform
> does not need.** **DRM**, because studios require it — three systems for three ecosystems, and CMAF with
> common encryption so the content is stored once rather than three times. **Entitlements**, because rights
> are per country and per date, checked before playback starts. **And resume**, which is a surprisingly large
> workload: forty million concurrent streams reporting position every few seconds is **eight million writes a
> second of thirty bytes each** — higher write volume than most systems in this course, absorbed by a memory
> cache with a sampled durable path.
>
> **The home page, which is the product.** A user arrives with no query, so **what is on the screen decides
> what is watched.** Rows, each a separate ranking problem, with the row order itself ranked and the artwork
> chosen per user. **Precomputed nightly and cached**, with a thin real-time layer for continue-watching —
> because ranking twenty thousand titles per user at request time cannot be done at forty million concurrent
> users, and precomputing over twenty thousand items can. **Again the catalogue size doing the work.**
>
> **Two things I would flag.**
>
> **The spike at a major release is a control-plane problem, not a bandwidth one.** The CDN was pre-warmed;
> **the licence server and playback API cannot be, and they see ten million requests in a minute.** That is
> where the headroom and the load testing belong, and it is the non-obvious failure mode.
>
> **And the honest scale point: infrastructure is about two percent of what this business spends.** Content
> licensing is one and a half billion a month. **So the engineering goal is not to minimise cost in absolute
> terms — it is to make the service good enough that people keep paying for the content**, which is a
> different objective from YouTube's, where the infrastructure genuinely is the business."

---

## 9. Recall card

**One fact drives everything: the catalogue is SMALL (~20,000 titles, ~450 TB — 0.01% of a year of YouTube
uploads) and KNOWN WEEKS IN ADVANCE.** Lead with that comparison; every other difference follows from it.

**Delivery is PREDICTIVE, not reactive.** Files are pushed to every edge days before release, at 03:00 local
when bandwidth is idle — **so at midnight there are no cache misses and origin traffic is ~zero.** A reactive
CDN would pull ~270 TB from origin in the first minutes with the first viewer at every edge waiting.

**Open Connect: appliances placed INSIDE ISP networks.** Both sides save (the ISP avoids transit, Netflix
avoids per-GB egress), which is why ISPs rack them. **~$5M/month amortised against ~$300M/month to buy the
same delivery — 50× — and it only works because the catalogue fits on a box.**

**Per-title and per-shot encoding, measured with a perceptual metric (VMAF): ~20% bitrate saving.** Justified
purely by amortisation — encode once, serve millions of times. **~3M CPU-hours for the WHOLE catalogue (~$90k,
once) against YouTube's 4.3M CPU-hours PER DAY.** A cartoon needs 2 Mbps where a grainy thriller needs 8; a
fixed ladder is wrong in both directions.

**Recommendations are the interface, not a feature** — no query, so the home page decides what is watched.
Rows, each a ranking problem, **precomputed nightly** with a thin real-time layer; feasible over 20,000 items
and not over billions.

**Playback adds three things to yesterday's ABR:** **DRM** (three ecosystems; CMAF + common encryption stores
one copy not three), **entitlements** (rights are per country and per date), and **resume** — 40M concurrent
streams reporting every ~5 s is **8M writes/second of 30 bytes**, the highest write rate here. **The release
spike is a control-plane problem** — the CDN is pre-warmed, the licence server cannot be.
