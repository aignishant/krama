---
day: 158
track: system-design
title: "Design YouTube"
phase: "High-level design case studies"
status: written
---

# Design YouTube

## 1. What this is, and why they ask it

**Video is the largest thing in computing that ordinary people do every day**, and designing a video platform
is where every number in this course gets multiplied by a thousand.

A photo is 2 MB. **A ten-minute video at decent quality is 300 MB, and the same video stored in five qualities
is more than a gigabyte.** A billion hours of watch time a day is exabytes of egress. **The bill is the design
constraint**, more directly than in any other system here.

They ask it because **it has three sub-systems that are each genuinely hard and are visibly separate.**

**Transcoding**, which is a compute problem of a size nothing else in this course approaches — roughly
real-time per output quality, so an hour of uploaded video is hours of CPU. **It is also embarrassingly
parallel if you chunk it correctly**, and seeing that is the main insight.

**Delivery**, where adaptive streaming means the client, not the server, decides what quality to fetch, chunk
by chunk, as the network changes. **That inverts the usual client-server relationship** and is why video plays
smoothly on a train.

**And storage economics**, where a brutal power law — a tiny fraction of videos get almost all the views —
means that tiering is not an optimisation but the only affordable design.

And they ask it because **it is the best test of scoping in the whole set.** The real product has
recommendations, comments, live streaming, monetisation, copyright detection, moderation and creator
analytics. **Naming those and picking three is the answer**; trying to design all of them produces nothing.

By the end of this lesson you can design the upload and transcoding pipeline, adaptive streaming, the delivery
layer, storage tiering and view counting — and size the bill.

---

## 2. The story

The video parlour was one room with a television and forty plastic chairs, and Bashir ran it for nineteen
years, and everything he learned he learned by being wrong first.

**The first thing was the tapes.**

He started with one copy of each film. Which was fine until *Sholay*, when eleven people wanted it on the same
Sunday and there was one cassette. **So he bought three more copies of the films people asked for, and one
copy of everything else.**

The shelf ended up strange-looking. **Four copies of six films, and one copy each of two hundred others**, and
most of those two hundred were not touched from one month to the next. When the shelf got full he moved the
untouched ones into a trunk under the stairs, **and if somebody asked for one it took him ten minutes to
find** — which happened about twice a year and nobody minded.

**The second thing was the machines.**

He had one player at first, and then the second-hand shop sold him a second one, and the thing he did with it
was not what anybody expected. **He used it to make copies.**

Because a tape that came from the distributor was one tape, **and copying it took as long as watching it** —
two and a half hours for a two-and-a-half-hour film. One machine, one film, an afternoon.

**With two machines he could copy two films at once. With five, five.** The copying did not get faster. There
was just more of it happening.

**The third thing was the picture quality, and it was the one that took longest to understand.**

His nephew had a shop in the next town with the same films, and he made his copies fast and rough. **Bashir
made his slowly, at the best quality the machine could do.** And Bashir was certain, for about two years, that
this made his parlour better.

Then he watched a film on his nephew's television, which was old and small, **and could not tell the
difference at all.**

**The good copy was better only on a good television.** On a bad one it was wasted — the same tape, the same
two and a half hours of machine time, and nobody in the room could see it.

So he started keeping two versions of the popular films. **The good one for the evening shows on the big set,
and the rough one for the small television in the back room**, which used less tape and was ready sooner.

**"It is not one film," he told his nephew. "It is the same film, four times, and you send whichever one fits
the television."**

---

## 3. The idea in plain English

Bashir's parlour is YouTube. **Extra copies of the popular ones, a trunk under the stairs for the rest,
copying that parallelises across machines but never gets faster per machine, and several qualities of the same
thing because the screen decides which one is worth sending.**

**Scope first, because the product is enormous.**

```
IN     upload
       transcode into multiple qualities
       adaptive playback
       view counts
       storage tiering
OUT    recommendations, comments, live streaming, monetisation,
       copyright matching (Content ID), moderation, analytics
```

**Say the out list and move on.** Recommendations in particular is a machine-learning system that deserves its
own interview, and offering to design it here is how you run out of time.

**The upload path is Instagram's, and the same rules apply.**

**Pre-signed URL, direct to object storage, never through your servers** —
[day 155](../day-155-string-dp/README.md)'s reasoning, and it matters more here because the files are
hundreds of times larger. **A 300 MB upload through your application tier is absurd; a 300 MB upload through
your application tier at a thousand a second is impossible.**

**And video needs resumable uploads**, which photos do not. A phone uploading 300 MB on a mobile connection
will lose the connection, and **restarting from zero is unacceptable.** Chunked upload with a session id and a
per-chunk acknowledgement — S3 multipart, or the `tus` protocol — so a dropped connection resumes from the
last completed chunk.

**Now transcoding, which is where the compute is.**

**The uploaded file is not what anyone watches.** It must become several *renditions* — resolutions and
bitrates — in a standard codec, split into short segments, with a manifest listing them.

```
2160p  @ 20 Mbps      only for the small fraction with the screen and the network
1080p  @  5 Mbps
720p   @  2.5 Mbps    the workhorse
480p   @  1 Mbps
360p   @  0.6 Mbps
240p   @  0.4 Mbps    the one that keeps playback alive on a bad connection
```

**Transcoding runs at roughly real-time per rendition on a CPU.** A ten-minute video with six renditions is
about an hour of CPU. **At five hundred hours uploaded per minute, that is thirty thousand hours of CPU per
minute of wall clock** — which is the number that makes video a different business from photos.

**And the key insight, which is Bashir's second machine: it parallelises by chunk.**

**Split the source into segments of a few seconds and transcode each independently, on a different machine.**
A ten-minute video becomes two hundred three-second chunks; two hundred workers finish in about three seconds
of wall time each rather than ten minutes.

**Two things make that work and are worth naming.** **Segments must be cut at keyframes**, because a video
frame is usually described relative to earlier frames and a chunk that starts mid-sequence cannot be decoded
alone. **And the outputs must be stitched with consistent timing**, or the player stutters at every boundary.

**Then delivery, and the idea that makes video work at all.**

**Adaptive bitrate streaming.** The client downloads a **manifest** — an HLS `.m3u8` or DASH `.mpd` — listing
every rendition and every segment. **It starts at a low quality, measures how fast segments arrive, and
switches quality between segments.**

**The client decides, not the server.** That inversion is the whole design: **the server publishes options and
the client picks**, which is why a video keeps playing when you walk into a lift and comes back to full quality
when you leave.

**And the segments are static files**, which is why this scales: **the CDN serves them like any other object,
with no video-specific logic at the edge.** There is no streaming server holding a connection per viewer.

**Then storage, where the power law does the work.**

**Almost all views go to a tiny fraction of videos.** Something like the top one percent gets ninety percent of
the traffic, and the long tail — Bashir's two hundred untouched tapes — is watched almost never.

**So tier by popularity, not only by age.** Hot videos live on fast storage in every region, warm ones in
fewer regions, cold ones in archival storage where retrieval takes minutes. **And the tail is enormous:** it
is most of the bytes and almost none of the traffic.

**One consequence worth stating: a cold video that suddenly goes viral must be promoted quickly**, or the first
thousand viewers get a video that takes minutes to start. **Popularity tiering needs a fast path back up.**

**And finally, view counts, which are harder than they look.**

**A view is not a page load.** It has a definition — thirty seconds watched, or a percentage of the video — and
that definition has to be enforced, because views are money.

**Counting exactly at this scale is expensive**, so counts are approximate and eventually consistent. **The
displayed count lags by minutes and that is fine** — except that creators care intensely, and fraud detection
means some views are removed hours later. **Real platforms display an approximate count immediately and
reconcile against a batch-computed exact count later**, which is why a video's count sometimes goes down.

---

## 4. The picture

The whole system:

```
  UPLOAD                    PROCESS                     DELIVER

  creator                 +-------------+
    |  resumable          | TRANSCODE   |
    |  chunked upload     | split into  |
    v  (pre-signed)       | chunks ->   |
  [ RAW STORAGE ] ------> | N workers   | ---> [ SEGMENT STORAGE ]
                          | in parallel |              |
                          +------+------+              v
                                 |                +---------+
                                 v                |   CDN   |
                          [ MANIFEST ]  --------> +----+----+
                          (.m3u8 / .mpd)               |
                                                       v
                                                    viewer
                                                 (picks quality
                                                  per segment)
```

Transcoding, and why chunking is the whole trick:

```
  SEQUENTIAL                        CHUNKED

  10-minute source                  10-minute source
        |                                 |
   one worker                       split at KEYFRAMES into
   transcodes                       200 segments of 3 seconds
   6 renditions                            |
        |                          +-------+-------+------ ...
   ~1x real-time each              v       v       v
   = 60 minutes                  worker  worker  worker      (200 of them)
                                   |       |       |
                                   +-------+-------+
                                           |
                                    stitch + manifest
                                           |
                                     ~3 seconds per rendition
                                     of WALL TIME

  The CPU total is identical. The LATENCY is 1,200x better.
  This is Bashir's second machine: copying does not get faster,
  there is just more of it happening at once.
```

Adaptive bitrate, and who is in charge:

```
  manifest.m3u8
    1080p -> seg0.ts seg1.ts seg2.ts ...
     720p -> seg0.ts seg1.ts seg2.ts ...
     480p -> seg0.ts seg1.ts seg2.ts ...
     240p -> seg0.ts seg1.ts seg2.ts ...

  player timeline:
    t=0    fetch 480p seg0   (start low: playback begins fast)
    t=3    arrived in 0.4 s  -> network is good -> step UP
    t=6    fetch 1080p seg2
    t=9    arrived in 2.8 s  -> buffer draining -> step DOWN
    t=12   fetch 480p seg4   (user walked into a lift)
    t=15   arrived in 0.3 s  -> step up again

  THE CLIENT DECIDES. The server publishes options.
  Every segment is a STATIC FILE, so the CDN needs no video logic.
```

The storage power law, which is Bashir's shelf:

```
  share of videos    share of views    where they live
  ----------------------------------------------------------
  top 0.1%              ~50%           every region, hot SSD
  next 1%               ~40%           several regions
  next 10%              ~9%            one region, standard
  bottom ~89%           ~1%            archival, minutes to retrieve

  the bottom 89% is MOST OF THE BYTES and almost none of the traffic
  -> tiering is not an optimisation, it is the only affordable design

  AND: a cold video that goes viral must be promoted FAST, or the
  first thousand viewers wait minutes for it to start.
```

Why the source file is kept:

```
  original upload (300 MB, whatever codec the phone used)
        |
        +--> 2160p, 1080p, 720p, 480p, 360p, 240p   (~1.2 GB total)

  KEEP THE ORIGINAL, because:
    - a better codec arrives (H.264 -> H.265 -> AV1) and everything
      must be re-encoded, at ~30-50% bandwidth saving
    - a rendition is found to be broken
    - a new resolution becomes standard

  -> the original goes to ARCHIVAL storage, not deleted.
     Re-encoding from a rendition loses quality irrecoverably.
```

---

## 5. How it actually works

### Resumable upload

```python
@app.post("/upload/start")
def start_upload(user_id: int, size: int, content_type: str) -> dict:
    video_id = snowflake.next_id()
    upload = s3.create_multipart_upload(Bucket=RAW, Key=f"raw/{video_id}")
    video_store.create(video_id, user_id, status="uploading")
    return {"video_id": video_id, "upload_id": upload["UploadId"],
            "chunk_size": 8 * 1024 * 1024}

@app.post("/upload/chunk-url")
def chunk_url(video_id: int, upload_id: str, part: int) -> dict:
    return {"url": s3.generate_presigned_url(
        "upload_part",
        Params={"Bucket": RAW, "Key": f"raw/{video_id}",
                "UploadId": upload_id, "PartNumber": part},
        ExpiresIn=3600)}
```

**A pre-signed URL per chunk, so the bytes never touch your servers** — and **the client can retry any single
chunk** without restarting the upload.

**Eight-megabyte chunks is the usual choice**: small enough that losing one is cheap, large enough that the
per-request overhead is negligible.

### Splitting and dispatching transcode work

```python
RENDITIONS = [(2160, 20_000), (1080, 5_000), (720, 2_500),
              (480, 1_000), (360, 600), (240, 400)]

def on_upload_complete(video_id: int) -> None:
    duration, keyframes = probe(f"raw/{video_id}")        # ffprobe
    segments = split_at_keyframes(keyframes, target_seconds=3)

    for index, (start, end) in enumerate(segments):
        for height, bitrate in RENDITIONS:
            queue.publish("transcode", {
                "video_id": video_id, "segment": index,
                "start": start, "end": end,
                "height": height, "bitrate": bitrate,
            })
    job_store.expect(video_id, len(segments) * len(RENDITIONS))
```

**`split_at_keyframes` is the line that matters.** A segment must begin at a keyframe — a frame encoded
without reference to any other — **because a chunk starting mid-sequence cannot be decoded on its own.**
Splitting at fixed three-second boundaries produces chunks that are silently corrupt.

**One queue message per segment per rendition** — a ten-minute video is 200 × 6 = 1,200 independent jobs.
**That is the parallelism.**

### The transcode worker

```python
def handle_transcode(job: dict) -> None:
    key = f"{job['video_id']}/{job['height']}/{job['segment']}.ts"
    if not blob_store.exists(key):             # idempotent: events are at-least-once
        ffmpeg(
            input=f"raw/{job['video_id']}",
            start=job["start"], end=job["end"],
            height=job["height"], bitrate=job["bitrate"],
            output=key,
        )
    if job_store.complete_one(job["video_id"]) == 0:
        write_manifest(job["video_id"])        # the LAST job publishes the video
```

**The existence check is the idempotency**, and it matters more here than anywhere else in the course:
**transcoding is the most expensive operation in the system, so doing it twice is real money.**

**`complete_one` returning zero means this was the last job**, which is how a distributed fan-out knows it has
finished — an atomic decrement of an expected count, not a scan.

### The manifest

```python
def write_manifest(video_id: int) -> None:
    lines = ["#EXTM3U", "#EXT-X-VERSION:3"]
    for height, bitrate in RENDITIONS:
        if blob_store.exists(f"{video_id}/{height}/0.ts"):
            lines.append(
                f"#EXT-X-STREAM-INF:BANDWIDTH={bitrate * 1000},"
                f"RESOLUTION={height * 16 // 9}x{height}")
            lines.append(f"{height}/index.m3u8")
    blob_store.put(f"{video_id}/master.m3u8", "\n".join(lines))
    video_store.mark_ready(video_id)
```

**The master manifest is a text file listing the options.** **That is the entire server side of adaptive
streaming** — there is no session, no state, no per-viewer connection. **The client reads the list and chooses.**

**And publishing renditions as they finish is better than waiting for all of them**: the 360p version is ready
long before the 2160p one, so **the video can be watchable within seconds of upload** while the high qualities
arrive later.

### View counting

```python
def record_view(video_id: int, user_id: int | None, watched_seconds: float,
                duration: float) -> None:
    if watched_seconds < min(30, duration * 0.3):
        return                                 # not a view, by definition
    key = f"view:{video_id}:{user_id or client_fingerprint()}"
    if not redis.set(key, "1", nx=True, ex=86400):
        return                                 # already counted today
    redis.incr(f"count:{video_id}")            # fast, approximate
    queue.publish("views", {"video_id": video_id, "at": time.time()})
```

**Two paths, deliberately.** The Redis counter is what gets displayed — **fast, approximate, and eventually
reconciled.** The queue feeds a batch pipeline that computes the authoritative count with fraud filtering.

**Which is why counts sometimes go down.** The displayed number is a fast estimate; the corrected one arrives
hours later.

**The `nx` deduplication window is a product decision**: counting a rewatch as a new view is a choice, and it
is worth asking about rather than assuming.

### Storage tiering

```python
def tier_for(video_id: int) -> str:
    views = view_stats.last_30_days(video_id)
    if views > 100_000:
        return "hot"          # replicated to every region, SSD
    if views > 1_000:
        return "warm"         # a few regions, standard object storage
    return "cold"             # archival, minutes to retrieve

def on_cold_video_requested(video_id: int) -> None:
    blob_store.restore(video_id, tier="warm", expedited=True)
    video_store.mark_restoring(video_id)       # the player shows a wait
```

**Tiering by views, not by age**, because a five-year-old video can be popular and a day-old one can be dead.

**And the restore path must exist**, or a cold video that suddenly trends is unwatchable for the minutes it
takes to retrieve — which is exactly when the views are happening.

### The real systems

```
ffmpeg              transcoding, universally
HLS (Apple)         .m3u8 manifests, .ts or fMP4 segments — the common default
DASH                the standard alternative; MPEG, codec-agnostic
H.264 / AVC         near-universal support, the safe baseline
H.265 / AV1         ~30-50% fewer bytes for the same quality; AV1 is
                    royalty-free and now widely supported
CMAF                one segment format usable by both HLS and DASH,
                    so you store one copy instead of two
S3 + Glacier        raw originals and the cold tail
CloudFront/Akamai   delivery, and most of the bill
```

**Mentioning CMAF is a genuine signal**, because it solves a real and expensive problem: **without it you store
HLS segments and DASH segments separately, doubling the storage of every video.**

---

## 6. The numbers

**Scale.**

```
2,000,000,000 monthly users
1,000,000,000 hours watched per day
500 hours of video UPLOADED per minute

uploads: 500 x 60 x 24 = 720,000 hours/day
views:   1e9 hours/day
```

**Transcoding, which is the compute problem.**

```
~1x real-time per rendition, 6 renditions
720,000 hours/day x 6 = 4,320,000 CPU-hours/day
                      = 180,000 CPU-hours per hour
                      = 180,000 cores running continuously

at ~$0.03/core-hour (spot):
  4,320,000 x $0.03 = ~$130,000/day = ~$4M/month

-> transcoding alone costs more than most systems in this course
   cost in total. Hence hardware encoders and custom silicon:
   Google built the Argos VCU specifically for this.
```

**And the chunking win, in latency rather than cost:**

```
10-minute video, 6 renditions, sequentially:
  60 minutes of wall time before it is watchable

chunked into 200 x 3-second segments, 1,200 jobs, 200 workers:
  ~3 seconds per job, 6 rounds = ~20 seconds of wall time

180x faster to publish. The CPU total is IDENTICAL.
```

**Storage.**

```
720,000 hours/day uploaded

per hour of video:
  original          ~2 GB
  2160p             ~9 GB
  1080p             ~2.3 GB
  720p              ~1.1 GB
  480p              ~0.45 GB
  360p              ~0.27 GB
  240p              ~0.18 GB
  ---------------------------
  total            ~15.3 GB per hour of video

720,000 x 15.3 GB = ~11 PB/day
                  = ~4 EB/year
```

**Four exabytes a year**, and it is worth saying that number out loud because it is where tiering stops being
optional.

```
untiered, all on standard storage at $0.023/GB/month:
  4 EB = 4,000,000,000 GB x $0.023 = ~$92,000,000/month

tiered by the power law:
  hot   1%   40 PB   x $0.023 = ~$920,000
  warm 10%  400 PB   x $0.0125 = ~$5,000,000
  cold 89% 3,560 PB  x $0.004  = ~$14,240,000
                                 ---------------
                                 ~$20,000,000/month

-> 4.6x cheaper, and it is still the second-largest line on the bill.
```

**Delivery, which is the largest.**

```
1,000,000,000 hours watched/day
average bitrate served: ~2 Mbps (most views are 480p-720p on phones)

1e9 hours x 3,600 s x 2 Mbps / 8 = 900,000,000 GB/day
                                 = 900 PB/day of egress
```

```
at commercial CDN rates of $0.01/GB:
  900,000,000 x $0.01 = $9,000,000/DAY = ~$270M/month

-> which is why YouTube does not use a commercial CDN.
   Google runs its own edge network and peers directly with ISPs,
   and places caching servers INSIDE ISP networks.
   That takes the marginal cost close to the cost of the hardware.
```

**That last point is the best thing to say in this interview**: **at this scale you stop buying delivery and
start building it**, and the break-even is somewhere in the tens of petabytes a month.

**The adaptive-bitrate saving:**

```
if every view were served at 1080p (5 Mbps) instead of an
adaptive average of 2 Mbps:

  900 PB/day -> 2,250 PB/day
  = 2.5x the largest line on the bill

-> adaptive bitrate is not a quality feature. It is a cost control
   that happens to also improve the experience.
```

**View counting.**

```
1e9 hours/day, average watch ~10 minutes -> ~6,000,000,000 views/day
                                          = ~70,000 views/second
                                            peak ~200,000/second

exact counting with a transaction per view: not viable
Redis INCR:  ~100,000 ops/s per instance -> 2-3 instances, sharded
             by video id
+ a batch pipeline for the authoritative, fraud-filtered count
```

**Latency budget for playback:**

```
manifest fetch (small text, from CDN edge)     ~30 ms
first segment (3 s at 480p ~ 400 KB)           ~200 ms
decode + first frame                           ~100 ms
                                               --------
                                               ~330 ms to first frame

starting at a LOW quality is what makes this possible.
Starting at 1080p would be ~2 MB and ~1.5 s.
```

**The full bill, ranked:**

```
delivery (own network, at cost)     ~$50,000,000/month
storage (tiered)                    ~$20,000,000/month
transcoding                          ~$4,000,000/month
everything else                      ~$5,000,000/month
                                     ------------------
                                     ~$79,000,000/month

-> per hour watched: ~$0.0026. Which is roughly what an ad pays.
   The whole business is that arithmetic.
```

---

## 7. The trade-offs

**Pre-generating every rendition against transcoding on demand.** Pre-generating costs the full compute for
every video, including the 89% that are watched almost never — **that is millions of CPU-hours spent on videos
nobody will see.** On-demand saves that and makes the first view of any video slow by minutes, which is
unacceptable. **The real answer is neither: pre-generate the low and middle renditions for everything, and
generate 2160p lazily on first request**, because almost nothing is watched at 4K.

**Storing more renditions against serving fewer.** Six renditions is 15 GB per hour of video; three would be
half that. **Fewer renditions means bigger quality jumps and more rebuffering on variable connections** — the
player has coarser options to fall back to. **The middle ones earn their storage; 2160p usually does not.**

**Segment length.** Short segments — two seconds — let the player adapt quickly and recover fast from a
network drop, **at the cost of more requests, more per-segment overhead, and more files to store.** Long
segments — ten seconds — are efficient and adapt sluggishly, so a network drop causes a visible stall.
**Four to six seconds is the usual compromise**, and live streaming pushes it shorter because latency matters
more than efficiency.

**Keeping the original against deleting it.** Originals are 2 GB an hour and are never served to anyone. **They
are kept because codecs improve** — moving a library from H.264 to AV1 saves thirty to fifty percent of the
largest line on the bill, and **re-encoding from a rendition loses quality irrecoverably.** So the original
goes to archival storage, and that is one of the clearest cases in this course of paying storage to preserve a
future option.

**Approximate view counts against exact ones.** Approximate is fast, cheap and displayed immediately. **Exact
requires a batch pipeline, arrives hours later, and can revise the number downwards** — which creators notice
and complain about. **Both are needed**, because the displayed count must be instant and the monetised count
must be defensible.

**Building the delivery network against buying it.** At 900 petabytes a day, a commercial CDN is $270M a month
and building your own edge network with ISP-embedded caches is a fraction of that. **Below roughly tens of
petabytes a month, buying is obviously right**; above it, the capital cost of building is repaid in months.
**Knowing that a break-even exists — and roughly where — is the point.**

**When would I not build this?** **Almost always.** Mux, Cloudflare Stream and AWS Elemental do upload,
transcoding, storage and delivery, and **below a few petabytes a month they are cheaper than the team.**
**If the product is a handful of videos** — a course, a marketing site — it is an object store, a CDN and a
one-off transcode. **The full pipeline is justified by volume alone**, and saying so is stronger than another
diagram.

---

## 8. In the interview

### How it gets asked

- *"Design YouTube."* or *"Design Netflix's playback."* — usually with no further constraints.
- *"How does transcoding work, and how do you make it fast?"* — the chunking question.
- *"How does the video keep playing when my connection gets worse?"* — adaptive bitrate.
- *"How much storage do you need?"* — where tiering appears.
- *"How do you count views?"*
- *"What would you leave out?"* — the scoping question.

### The first ninety seconds

> "The product is huge, so let me scope, size, and then design the three parts that are actually hard.
>
> **In: upload, transcoding, adaptive playback, storage, view counts. Out: recommendations, comments, live
> streaming, monetisation, copyright matching, moderation.** Recommendations especially is its own interview.
>
> **Sizing, and one number reframes everything.** Five hundred hours uploaded per minute is seven hundred and
> twenty thousand hours a day. **A billion hours watched a day at an average of two megabits is about nine
> hundred petabytes a day of egress.** That is the system.
>
> **Three sub-systems, each hard in a different way.**
>
> **Upload is Instagram's, with one addition: it must be resumable.** Pre-signed URLs straight to object
> storage, but chunked with per-chunk acknowledgement — **because a three-hundred-megabyte upload on a mobile
> connection will drop, and restarting from zero is unacceptable.**
>
> **Transcoding is the compute problem, and it is enormous.** Six renditions at roughly real-time each means
> seven hundred and twenty thousand hours a day becomes 4.3 million CPU-hours a day — **about a hundred and
> eighty thousand cores running continuously**, four million dollars a month even on spot pricing. **That is
> why Google built custom silicon for it.**
>
> **And the key insight is that it parallelises by chunk.** Split the source at keyframes into three-second
> segments and transcode each independently. **A ten-minute video sequentially is an hour before it is
> watchable; chunked across two hundred workers it is about twenty seconds.** The CPU total is identical —
> the latency is a hundred and eighty times better.
>
> **The keyframe part is not optional**: a segment must start at a frame that can be decoded on its own, or the
> chunk is silently corrupt.
>
> **Delivery is adaptive bitrate, and the inversion is the point.** The client fetches a manifest listing
> every rendition and every segment, starts low, measures throughput, and **switches quality between
> segments.** The client decides; the server just publishes options. **Every segment is a static file**, so the
> CDN needs no video logic at all — there is no per-viewer connection anywhere.
>
> **And storage: four exabytes a year, tiered by popularity.** The top one percent of videos gets ninety
> percent of the views; the bottom eighty-nine percent is most of the bytes and almost none of the traffic.
> **Tiering is not an optimisation here, it is the only affordable design** — ninety-two million a month
> untiered against twenty tiered.
>
> **Which of the three would you like me to go deep on?**"

### The follow-ups

**"How does the video keep playing when my connection gets worse?"**

> "Adaptive bitrate streaming, and the design idea is that **the client decides, not the server** — which is
> the reverse of almost everything else in this course.
>
> **The video exists in several renditions**, each a different resolution and bitrate, and each is **cut into
> short segments** of a few seconds. So a ten-minute video at six qualities is about twelve hundred small
> files.
>
> **The client first fetches a manifest** — an HLS `.m3u8` or a DASH `.mpd` — which is a text file listing
> every rendition, its bandwidth, and where its segments are.
>
> **Then it plays a loop.** Fetch a segment, measure how long it took, compare with how much buffer is left,
> and **choose the rendition for the next segment.** Arriving fast with a full buffer means step up; arriving
> slowly with a draining buffer means step down.
>
> **It starts low deliberately**, because the first frame should appear fast. A three-second 480p segment is
> about four hundred kilobytes and arrives in a couple of hundred milliseconds; **starting at 1080p would be
> two megabytes and about one and a half seconds to first frame.** So the player begins low and climbs within
> a few seconds.
>
> **What this buys architecturally is that every segment is a static file.** There is no streaming server, no
> session, no per-viewer connection, no video-aware logic at the edge. **The CDN serves them exactly like
> images**, which is why it scales to nine hundred petabytes a day.
>
> **The segment length is a real trade.** Two-second segments adapt quickly and recover fast from a network
> drop, at the cost of more requests and more files. **Ten-second segments are efficient and sluggish** — a
> connection that degrades mid-segment causes a visible stall. **Four to six seconds is the usual compromise**,
> and live streaming goes shorter because latency matters more than efficiency.
>
> **And I would add the cost argument, because it is the stronger one.** If every view were served at 1080p
> instead of an adaptive average of about two megabits, **egress would be two and a half times higher** — which
> at this scale is over a hundred million dollars a month. **Adaptive bitrate is a cost control that also
> happens to improve the experience.**"

**"Transcoding takes an hour per video. How do you make that acceptable?"**

> "You do not make it faster. **You make more of it happen at once**, and the enabling trick is chunking.
>
> **The compute is irreducible.** Transcoding runs at roughly real-time per output rendition, so a ten-minute
> video with six renditions is about an hour of CPU. **That does not change** — codecs are what they are.
>
> **What changes is the wall clock.** Split the source into segments of about three seconds and transcode each
> one independently, on a different machine. **A ten-minute video is two hundred segments times six renditions
> — twelve hundred completely independent jobs.** Across two hundred workers, that is about twenty seconds of
> wall time instead of an hour. **A hundred and eighty times faster to publish, with identical total CPU.**
>
> **Two things make it work and both are easy to get wrong.**
>
> **Segments must be cut at keyframes.** Most video frames are encoded as differences from earlier frames, so
> a chunk starting mid-sequence has nothing to decode against. **Cutting at fixed three-second boundaries
> produces chunks that are silently corrupt** — they encode without error and play as garbage.
>
> **And the outputs must be stitched with consistent timing**, or the player stutters at every boundary. In
> practice that means fixing the encoder parameters up front so every worker produces compatible output.
>
> **Three more things I would build in.**
>
> **Idempotency.** Queue events are at-least-once, and **transcoding is the most expensive operation in the
> system** — doing a job twice is real money. Check whether the output already exists before starting.
>
> **Progressive publishing.** The 360p rendition finishes long before the 2160p one. **Publish each as it is
> ready**, so the video is watchable within seconds and the high qualities appear later. Waiting for all six
> wastes the parallelism you just built.
>
> **And lazy 2160p.** Almost nothing is watched at 4K. **Generating it eagerly for every upload spends compute
> on videos nobody will watch at all**, let alone at that quality. I would generate the low and middle
> renditions always and 4K on first request, accepting a slow first 4K view.
>
> **On cost: 4.3 million CPU-hours a day is about four million dollars a month even on spot instances**, which
> is why the platforms at this scale build custom encoding hardware. Google's Argos VCU exists for exactly this
> line item."

**"How do you store this much video?"**

> "Four exabytes a year, and the answer is that **the access pattern is so skewed that tiering is the design
> rather than an optimisation.**
>
> **The arithmetic first.** Seven hundred and twenty thousand hours uploaded a day, and each hour of video is
> about fifteen gigabytes once you count the original plus six renditions. **That is eleven petabytes a day,
> four exabytes a year.**
>
> **On standard object storage that is ninety-two million dollars a month, and it grows every month.**
>
> **The power law rescues it.** The top one percent of videos gets something like ninety percent of the views;
> the bottom eighty-nine percent is watched almost never. **And crucially, that bottom tier is most of the
> bytes.**
>
> **So: tier by popularity, not by age.** Hot videos on fast storage replicated to every region. Warm ones in
> fewer regions on standard storage. **Cold ones in archival storage where retrieval takes minutes.** That
> takes ninety-two million to about twenty — **still the second-largest line on the bill, but survivable.**
>
> **By popularity and not by age matters**, because a five-year-old music video can be extremely hot and a
> day-old upload can be dead. Age is a bad proxy.
>
> **And the restore path must exist and be fast**, which is the part people forget. **A cold video that
> suddenly trends is unwatchable for the minutes archival retrieval takes — which is exactly when the views
> are happening.** So popularity monitoring needs to trigger expedited promotion, and the player needs to show
> something sensible while it happens.
>
> **One decision that looks wasteful and is not: keep the original.** It is two gigabytes an hour and is never
> served to anyone. **It is kept because codecs improve** — moving a library from H.264 to AV1 saves thirty to
> fifty percent of the delivery bill, which is the largest line — **and re-encoding from a rendition loses
> quality irrecoverably.** So originals go to the cheapest archival tier and stay there.
>
> **And I would mention CMAF**, because it solves an expensive and unglamorous problem: **without a common
> segment format you store HLS and DASH segments separately and double the storage of every video.**"

### The model answer

*"Design a video platform: five hundred hours uploaded per minute, a billion hours watched per day, global
audience. Tell me what it costs."*

> "The cost framing is the right one for video, because **the bill is the design constraint** more directly
> than in any other system. Let me scope, then size, then design against the numbers.
>
> **In: upload, transcode, adaptive playback, storage, view counts. Out: recommendations, comments, live,
> monetisation, Content ID, moderation.**
>
> **Upload: resumable chunked upload with pre-signed URLs, direct to object storage.** Eight-megabyte chunks
> so a dropped connection retries one chunk rather than three hundred megabytes. **No video bytes touch my
> servers.**
>
> **Transcoding: split at keyframes into three-second segments, fan out one job per segment per rendition.**
> A ten-minute video is twelve hundred independent jobs; across two hundred workers that is twenty seconds of
> wall time instead of an hour. **Idempotent, because at-least-once delivery on the most expensive operation
> in the system is real money.** **Progressive publishing**, so 360p is live in seconds. **And 2160p generated
> lazily**, because almost nothing is watched at 4K and eager generation spends compute on the long tail.
>
> **Cost: 720,000 hours a day times six renditions at real-time is 4.3 million CPU-hours a day — about
> $4 million a month on spot.** At that number, custom encoding hardware pays for itself, which is why it
> exists.
>
> **Delivery: adaptive bitrate over static segments.** The client fetches a manifest, starts low for a fast
> first frame, and switches quality between segments based on measured throughput. **Every segment is a static
> file, so the edge needs no video logic and there is no per-viewer connection anywhere.**
>
> **Cost: a billion hours a day at an adaptive average of two megabits is nine hundred petabytes a day.** **On
> a commercial CDN at a cent a gigabyte that is nine million dollars a day — $270 million a month, which is
> not a business.**
>
> **So at this scale you stop buying delivery and build it**: your own edge network, direct peering with ISPs,
> and caching servers placed inside ISP networks. **That takes the marginal cost close to hardware and
> power.** The break-even is somewhere in the tens of petabytes a month, and **knowing that a break-even exists
> is the point** — below it, building your own is a mistake.
>
> **And adaptive bitrate is doing real work on this line.** Serving everything at 1080p would be 2.5× the
> egress — **it is a cost control that happens to improve the experience.**
>
> **Storage: fifteen gigabytes per hour of video including the original, so eleven petabytes a day and four
> exabytes a year.** Untiered that is $92 million a month. **Tiered by popularity — not age — it is about
> $20 million.** Hot in every region, warm in a few, cold in archival with an expedited restore path, **because
> a cold video that trends is unwatchable for the minutes retrieval takes, which is exactly when the views
> arrive.**
>
> **Originals kept in archival, never served**, because codec migrations save thirty to fifty percent of the
> largest line and re-encoding from a rendition loses quality permanently.
>
> **View counts: approximate and immediate from a sharded counter, authoritative and delayed from a batch
> pipeline with fraud filtering.** Both are needed — the displayed number must be instant and the monetised
> number must be defensible — **and that is why counts sometimes go down.**
>
> **The ranked bill: delivery ~$50M at cost, storage ~$20M, transcoding ~$4M, everything else ~$5M.
> About $79 million a month, which is roughly a quarter of a cent per hour watched** — and that number is the
> whole business, because it has to sit under what an hour of viewing earns.
>
> **The thing I would flag as the biggest risk is the long tail.** Eighty-nine percent of videos are watched
> almost never and consume most of the storage and most of the transcoding compute. **Every lever that helps —
> lazy high renditions, aggressive cold tiering, fewer renditions for unpopular uploads — is about spending
> less on content nobody watches**, and that is where the engineering effort actually pays."

---

## 9. Recall card

**Scope out loud** (in: upload, transcode, playback, storage, views; out: recommendations, comments, live,
monetisation, Content ID) — the product is too big to design whole. **Video is ~7,000× a photo and ~10⁶× a
tweet**, and the bill is the design constraint.

**Transcoding is ~1× real-time per rendition** — 720,000 hours/day × 6 = **4.3M CPU-hours/day, ~$4M/month**,
which is why custom encoding silicon exists. **It parallelises by chunk: split at KEYFRAMES** (fixed-time
splits are silently corrupt), one job per segment per rendition — **an hour of wall time becomes ~20 seconds
with identical CPU.** Make it **idempotent** (the most expensive op in the system), **publish renditions
progressively**, and **generate 2160p lazily.**

**Adaptive bitrate inverts the usual relationship: the CLIENT decides.** It fetches a manifest, starts low for
a ~330 ms first frame, measures throughput and switches quality between segments. **Every segment is a static
file**, so the CDN needs no video logic and there is no per-viewer connection. **Segment length trades
adaptation speed against overhead — 4–6 s is the compromise.**

**Storage is ~15 GB per hour of video → 11 PB/day → 4 EB/year.** Untiered $92M/month; **tiered by POPULARITY,
not age** (top 1% gets ~90% of views; the bottom 89% is most of the bytes) → ~$20M. **The expedited restore
path is mandatory** — a cold video that trends is unwatchable exactly when the views arrive. **Keep the
original** for future codec migrations (AV1 saves 30–50% of the biggest line); re-encoding a rendition loses
quality permanently.

**Delivery is the largest line: 900 PB/day.** At commercial CDN rates that is **$270M/month, so at this scale
you build your own edge network and embed caches in ISPs.** **Adaptive bitrate itself is a 2.5× cost control.**
**View counts are two systems** — instant approximate for display, batch authoritative with fraud filtering
for money — which is why counts sometimes go down.
