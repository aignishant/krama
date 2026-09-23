---
day: 155
track: system-design
title: "Design Instagram"
phase: "High-level design case studies"
status: written
---

# Design Instagram

## 1. What this is, and why they ask it

Instagram is yesterday's Twitter with one thing added, and that one thing changes everything: **the content is
images and video, and they are three orders of magnitude larger than text.**

A tweet is three hundred bytes. **A photo is two megabytes.** Everything downstream of that number is
different — the storage bill, the upload path, the delivery mechanism, where the money goes, and what your
users actually experience as "the app is slow".

They ask it because **it is the cleanest test of whether you understand that media is not just bigger data.**
It needs a separate write path with pre-signed uploads that never touch your servers. It needs transcoding
into several sizes, done asynchronously, because a phone on a train should get a 40 KB thumbnail and not a
4 MB original. **It needs a CDN, and the CDN is not an optimisation here — it is the product**, because at
this scale serving images from your own origin is financially impossible.

And it is a good question because **the metadata half is genuinely easy** — it is the news feed you already
know — so the interview goes quickly to the part that distinguishes candidates. **If you spend thirty minutes
on fan-out you will never reach the interesting half**, and knowing to move on is part of what is assessed.

By the end of this lesson you can design the upload path, the transcoding pipeline, the storage and delivery
layers, the feed on top, and size the whole thing — including the bill, which is the number that surprises
people most.

---

## 2. The story

The photo studio near the bus stand had been developing film for thirty-one years when Sadanand's son
persuaded him to buy the machine that printed from phones.

**And the queue changed shape immediately, in a way neither of them had expected.**

Before, someone brought a roll, left it, and came back on Thursday. **The waiting happened somewhere else.**

Now, people stood there.

They stood there while the phone talked to the machine, and while the machine thought about it, and while it
printed, and the whole thing took four minutes per photograph, **and there were nine people in the shop.**

Sadanand's son, who was twenty-four and had opinions, changed three things over about two months.

**The first was that he stopped making people wait for the printing.** He took the photos off the phone —
which took twenty seconds — gave them a token, and said come back at five. **The slow part still happened. It
just did not happen with the customer standing there.**

**The second was the sizes.** People kept asking for the small ones for passports, and the medium for albums,
and occasionally something big for framing. And he had been making each one when it was asked for.

So he started making all three the moment the photo came off the phone. **More work up front, and it meant
nobody ever waited for a size.**

**The third took a year and it was the one that actually mattered.**

Because his real problem was that the school six streets away sent him four hundred prints every February —
class photographs, the same eight images, four hundred copies — **and every single copy came out of his one
machine in his one shop.**

So he came to an arrangement with a fellow near the school who had a small printer. **He sent that fellow the
eight images, once, and the fellow printed the four hundred.**

**One journey instead of four hundred.** The images sat there for the whole of February, and when the
requests came, they came out of a printer six streets from the school instead of a machine six streets from
the bus stand.

His father, when it was explained to him, said the thing that summed it up.

**"So the picture only travels once, and after that it is already where the people are."**

---

## 3. The idea in plain English

Sadanand's son built the media pipeline. **Take the upload quickly, do the slow work afterwards, make every
size in advance, and push the file to where the readers are.**

**Start with the number that shapes everything.**

```
a tweet     ~300 bytes
a photo     ~2 MB
a 30s video ~15 MB

-> a photo is roughly 7,000x a tweet
```

**So the metadata system and the media system are two different systems**, with different stores, different
scaling limits and different bills. **Say that in the first minute.**

**The metadata half is the news feed you already know**, and it is worth being brief about it: posts, follows,
a precomputed timeline, hybrid fan-out for celebrities, hydration by batched multi-get.
[Day 153](../day-153-longest-common-subsequence/README.md) is the whole of it.

**The media half is today.**

**First: the upload must not go through your servers.**

The obvious design — the phone posts the image to your API, which writes it to storage — **puts every
megabyte through your application tier.** At a thousand uploads a second that is 2 GB/s of traffic through
machines whose job is business logic, and they will spend all their time copying bytes.

**Instead: pre-signed URLs.** The client asks your API "I want to upload"; the API returns **a short-lived,
signed URL that grants permission to write one specific object to your storage bucket**, and the client uploads
directly to S3. **Your server handles a few hundred bytes of JSON and never sees the image.**

**That single decision removes the largest traffic flow in the system from your servers**, and it is the first
thing to say about the upload path.

**Second: transcoding is asynchronous, and this is Sadanand's token.**

The uploaded original is not what gets served. **You need several sizes** — a thumbnail for the grid, a medium
for the feed, a large for full screen — plus format conversion to WebP or AVIF, orientation correction from
EXIF, and stripping of location metadata.

**That takes seconds, and the user must not wait for it.** So: the upload completes, an event goes on a queue,
workers transcode, and the post becomes visible when the first usable size is ready.

**The product decision hiding in there is worth naming.** Either the post appears immediately and the image
"pops in" when ready, or the post waits until transcoding finishes. **Instagram does the first**, showing the
user their own upload from the local file while the server catches up.

**Third: variants, generated in advance.**

```
thumbnail   150 x 150     ~10 KB    profile grid
small       320 wide      ~40 KB    feed on a slow connection
medium      640 wide      ~150 KB   feed, standard
large       1080 wide     ~400 KB   full screen
original    up to 4096    ~2 MB     kept for re-processing
```

**Generating on demand is the alternative** — a resizing service in front of storage — and it is tempting
because it stores less. **It also makes the first request for every size slow**, and it puts a compute
service on the read path of the most-read thing in the system. **Pre-generate.**

**And the client picks the size.** A phone on 3G asks for the 40 KB version; a laptop on wifi asks for the
400 KB one. **That one decision changes a user's experience of the product more than any backend
optimisation.**

**Fourth: the CDN, which is not an optimisation.**

This is the fellow near the school. **The image is copied once to an edge location, and every subsequent
request is served from there** — close to the user, and never touching your storage.

**At this scale it is not a nice-to-have; it is the only affordable design.** The arithmetic is stark, and it
is the best thing to be able to produce in this interview:

```
serving 100 TB/day from S3 directly:  ~$0.09/GB  = ~$9,000/day
serving it from a CDN at 95% hit rate: 5 TB origin + 95 TB edge
                                       = ~$450 + ~$4,750 = ~$5,200/day
and with committed CDN pricing (~$0.02/GB): ~$2,000/day
```

**And the cache hit rate is the single most valuable number in the system**, because it multiplies the largest
line on the bill.

**Fifth: storage, which grows forever and never shrinks.**

**Photos are never deleted in practice** — users delete a few, and the total only goes up. So storage is a
permanently accumulating cost, and the lever is tiering: **recent media on standard storage, older media moved
to infrequent-access and then archival classes**, because access follows a brutal power law. Almost every view
is of something posted in the last week.

**Sixth: the feed, briefly, because it is the part you already know.**

The feed returns **URLs, not images.** The API response is small JSON; the client then fetches the images from
the CDN. **So the feed API's latency and the image delivery are completely decoupled**, which is why a feed can
be fast while images are still loading.

**And the URLs must be signed if the content is private**, which conflicts with caching — a signed URL is
unique per user and cannot be shared in a cache. **The resolution is a signed URL whose signature covers a
path and an expiry rather than a user**, so many users share the cache entry.

**Finally: video, which is the same shape and worse.**

**Video is transcoded into an adaptive ladder** — several resolutions and bitrates — and delivered in small
chunks, so a player can switch quality mid-stream as the network changes. **Transcoding is expensive:** roughly
real-time per output rendition on a CPU, so a one-minute video with five renditions is five minutes of compute.
**That is where a video product's infrastructure money actually goes**, and it is worth one sentence even in a
photo-focused answer.

---

## 4. The picture

The two systems, side by side:

```
   METADATA (small, structured)        MEDIA (large, opaque)

   posts, users, follows, likes        images and video
   ~500 bytes per post                 ~2 MB per photo
   Postgres / Cassandra                S3 / object storage
   sharded by id                       flat, keyed by media id
   read via the feed                   read via a CDN
   cost: cheap                         cost: THE bill

   Same product. Two completely different systems.
   Say this in the first minute.
```

The upload path, and why it avoids your servers:

```
  NAIVE                              PRE-SIGNED

  phone --2 MB--> API server         phone --request--> API server
                     |                              <--signed URL--
                     v                     |
                    S3                     +--2 MB--> S3 directly

  every megabyte through your        your server handles ~200 bytes
  application tier                   of JSON and never sees the image

  1,000 uploads/s x 2 MB = 2 GB/s    1,000 uploads/s x 200 B = 200 KB/s
  through machines meant for
  business logic
```

The full write path:

```
  1. phone -> API: "I want to upload"           ~10 ms
  2. API -> phone: pre-signed URL + media_id    (server does no I/O)
  3. phone -> S3: PUT the 2 MB original         ~2 s on 4G
  4. S3 -> event -> QUEUE
  5. TRANSCODE WORKERS:
       - read the original
       - fix orientation from EXIF
       - STRIP location metadata          <- privacy, and easy to forget
       - produce 150 / 320 / 640 / 1080 as WebP
       - write each back to S3
  6. mark the post visible; fan out to followers' timelines

  The user sees their own post IMMEDIATELY, rendered from the local
  file, while steps 4-6 are still running.
```

The variants, and what each is for:

```
  size        pixels     bytes    used for
  ---------------------------------------------------------
  thumbnail   150x150     10 KB   profile grid, 3 across
  small       320 wide    40 KB   feed on a poor connection
  medium      640 wide   150 KB   feed, default
  large      1080 wide   400 KB   full screen, tapped
  original   up to 4096    2 MB   kept only for re-processing

  total stored per photo: ~2.6 MB, of which 2 MB is the original

  A phone on 3G that gets the 400 KB version instead of the 40 KB one
  has a 10x worse experience, and no backend change fixes that.
```

The delivery path, and where the money is:

```
  phone --> CDN EDGE (Mumbai)  --hit 95%-->  served, ~20 ms
                |
                +--miss 5%--> S3 origin (Mumbai region) --> edge --> phone

  100 TB/day delivered

  ALL FROM S3:      100 TB x $0.09/GB          = ~$9,000/day
  CDN at 95% hit:     5 TB origin x $0.09      = ~$450
                     95 TB edge   x $0.05      = ~$4,750
                                                 ~$5,200/day
  CDN, committed:    95 TB x $0.02             = ~$2,000/day

  -> the hit rate multiplies the biggest line on the bill.
     90% -> 95% halves the origin egress.
```

Storage growth, which never reverses:

```
  100M photos/day x 2.6 MB = 260 TB/day = ~95 PB/year

  tiered by age, because access follows a brutal power law:

  age        share of views    storage class     $/GB/month
  0-7 days       ~80%          standard            0.023
  7-90 days      ~15%          infrequent access   0.0125
  > 90 days       ~5%          archive/glacier     0.004

  95 PB all-standard:  ~$2.2M/month
  95 PB tiered:        ~$450K/month

  5x cheaper, from a lifecycle rule.
```

---

## 5. How it actually works

### The upload handshake

```python
@app.post("/upload/init")
def upload_init(user_id: int, content_type: str) -> dict:
    media_id = snowflake.next_id()
    key = f"originals/{media_id}"
    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": ORIGINALS, "Key": key, "ContentType": content_type},
        ExpiresIn=900,                        # 15 minutes
    )
    media_store.create(media_id, user_id, status="pending")
    return {"media_id": media_id, "upload_url": url}
```

**The server does one small write and returns.** No image bytes anywhere in this function — **which is the
entire point of the design.**

**`ExpiresIn=900` bounds the damage if the URL leaks**, and the key is derived from a server-generated id so a
client cannot choose where to write.

### Transcoding, triggered by the storage event

```python
VARIANTS = [("thumb", 150), ("small", 320), ("medium", 640), ("large", 1080)]

def handle_upload_complete(event: dict) -> None:
    media_id = event["key"].split("/")[-1]
    original = s3.get_object(ORIGINALS, event["key"])["Body"].read()

    image = Image.open(io.BytesIO(original))
    image = ImageOps.exif_transpose(image)    # honour the camera's rotation
    image = strip_metadata(image)             # remove GPS — privacy, not size

    for name, width in VARIANTS:
        resized = image.copy()
        resized.thumbnail((width, width * 4))          # preserve aspect ratio
        buffer = io.BytesIO()
        resized.save(buffer, format="WEBP", quality=82)
        s3.put_object(DERIVED, f"{name}/{media_id}.webp", buffer.getvalue())

    media_store.mark_ready(media_id)
    queue.publish("fanout", {"media_id": media_id})
```

**`exif_transpose` is not optional.** Phones store the sensor image plus a rotation flag; **if you resize
without honouring it, a quarter of your users' photos come out sideways** — and it is the single most common
bug in an image pipeline.

**`strip_metadata` removes GPS coordinates.** A photo taken at home carries the user's home address in EXIF,
and serving the original unmodified publishes it. **This is a privacy requirement, not a size optimisation.**

**And the fan-out is published only after the variants exist**, so a follower never sees a post with no
loadable image.

### Idempotency, because the event may fire twice

```python
def handle_upload_complete(event: dict) -> None:
    media_id = event["key"].split("/")[-1]
    if not redis.set(f"transcode:{media_id}", "1", nx=True, ex=3600):
        return                                # already being processed
    ...
```

**Storage events are at-least-once**, so without this the same image is transcoded several times — **wasted
CPU, and CPU is where the transcoding bill lives.** `SET NX` is the same idempotency pattern as
[day 152](../day-152-longest-increasing-subsequence/README.md)'s notifications.

### The feed response — URLs, not bytes

```python
def build_post(post: dict, media: dict) -> dict:
    base = f"https://cdn.example.com/{media['id']}"
    return {
        "id": post["id"],
        "author": post["author_id"],
        "caption": post["caption"],
        "media": {
            "thumb":  f"{base}/thumb.webp",
            "small":  f"{base}/small.webp",
            "medium": f"{base}/medium.webp",
            "large":  f"{base}/large.webp",
            "width": media["width"], "height": media["height"],
            "blurhash": media["blurhash"],
        },
    }
```

**The feed API returns a few hundred bytes per post and no image data at all.** The client picks a variant
based on its screen and connection, and fetches from the CDN.

**`blurhash` is a twenty-byte string encoding a blurred version of the image**, rendered instantly while the
real one loads. **It costs nothing and it is the difference between a feed that feels fast and one that feels
broken** — and including it signals that you have thought about the client.

**`width` and `height` let the client reserve the right space before the image arrives**, so the layout does
not jump.

### Signed URLs for private content

```python
def signed_media_url(media_id: int, variant: str, ttl: int = 3600) -> str:
    path = f"/{media_id}/{variant}.webp"
    expiry = int(time.time()) + ttl
    signature = hmac.new(CDN_KEY, f"{path}{expiry}".encode(), "sha256").hexdigest()
    return f"https://cdn.example.com{path}?e={expiry}&s={signature}"
```

**The signature covers the path and the expiry, not the user.** That matters: **a per-user signature would
make every URL unique and destroy the CDN cache**, since two users viewing the same photo would request
different URLs.

**The trade is that a signed URL, once issued, works for anyone who has it until it expires** — which is the
standard compromise, and worth naming rather than glossing.

### Deletion, and why it is harder than it looks

```python
def delete_media(media_id: int) -> None:
    media_store.mark_deleted(media_id)             # 1. immediate: feeds filter it
    cdn.purge(f"/{media_id}/*")                    # 2. minutes: edge caches
    queue.publish("gc", {"media_id": media_id})    # 3. later: the actual objects
```

**Three layers, and they complete at different times.** The metadata flag takes effect immediately because the
feed filters on it. **The CDN purge takes minutes and is not guaranteed at every edge.** The objects are
deleted last, by a background job.

**So "delete" means "no longer discoverable" long before it means "the bytes are gone"**, and that is worth
saying plainly, because it is what users and regulators actually ask about.

### Video, in outline

```
upload original -> queue -> transcode into an ADAPTIVE LADDER:
    240p  @  400 kbps
    480p  @  1 Mbps
    720p  @  2.5 Mbps
    1080p @  5 Mbps
  each segmented into 2-6 second chunks
  plus a manifest (HLS .m3u8 or DASH .mpd) listing them

player: fetches the manifest, starts low, measures throughput,
        switches rendition between chunks

cost: ~1x real-time per rendition on CPU
      a 60 s video x 4 renditions = ~4 minutes of compute
      -> hardware encoders or spot instances, and it is the
         dominant cost of a video product
```

### The real systems

```
S3 / GCS         object storage for originals and variants
CloudFront,      CDN — the delivery layer, and most of the bill
Fastly, Akamai
SQS / Kafka      the transcoding queue
ffmpeg           video transcoding, everywhere, universally
libvips          image resizing — several times faster and much
                 lighter on memory than ImageMagick
Cassandra        Instagram's metadata store, historically
```

**Naming libvips is a small, real signal**, because anyone who has run an image pipeline at scale has hit
ImageMagick's memory behaviour and moved off it.

---

## 6. The numbers

**Traffic.**

```
500,000,000 daily active users
each views ~50 photos/day        -> 25,000,000,000 photo views/day
each posts ~0.2 photos/day       ->    100,000,000 uploads/day

views:   25e9 / 86,400 = ~290,000 views/second   (peak ~900,000)
uploads: 1e8  / 86,400 = ~1,160 uploads/second   (peak ~3,500)

read : write = 250 : 1
```

**Bandwidth, which is the number that matters.**

```
average delivered variant: ~150 KB (most views are the feed size)

290,000 views/s x 150 KB = 43.5 GB/s
                         = ~350 Gbps sustained
per day: 25e9 x 150 KB   = 3,750 TB/day = 3.75 PB/day
```

**Nearly four petabytes a day of egress.** That is the system, and it is why the CDN is structural rather than
an optimisation.

**The bill, which is the best thing to be able to produce here:**

```
ALL FROM ORIGIN (S3 egress at $0.09/GB):
  3,750 TB/day x 1,024 GB x $0.09 = ~$345,000/DAY  = ~$10.4M/month
  -> not a business

CDN at 95% hit rate:
  origin: 187 TB/day x $0.09  = ~$17,000/day
  edge:  3,563 TB/day x $0.02 = ~$73,000/day   (committed pricing)
                                ~$90,000/day  = ~$2.7M/month

-> the CDN is a 4x saving, and the hit rate is the lever:
   95% -> 98% cuts origin egress by 60%.
```

**Upload bandwidth, for contrast:**

```
1,160 uploads/s x 2 MB = 2.3 GB/s inbound

with pre-signed URLs: 0 GB/s through your application servers
                      1,160 x 200 bytes = 232 KB/s of JSON

-> the entire upload flow costs your API tier nothing.
```

**Storage.**

```
100,000,000 uploads/day
  original       2 MB
  four variants  0.6 MB
  total          2.6 MB per photo

per day:   100e6 x 2.6 MB = 260 TB/day
per year:                   95 PB/year

untiered, S3 standard at $0.023/GB/month:
  95 PB = 97,280,000 GB x $0.023 = ~$2,240,000/month, growing

tiered (80% of views in the first week):
  0-7 days     1.8 PB  standard   $0.023  = ~$42,000
  7-90 days   21.6 PB  IA         $0.0125 = ~$276,000
  > 90 days   71.6 PB  archive    $0.004  = ~$293,000
                                            ~$611,000/month

-> 3.7x cheaper, from a lifecycle rule and nothing else.
```

**Transcoding cost.**

```
photos: ~200 ms of CPU per image for four variants
  1,160 uploads/s x 0.2 s = 232 CPU-seconds/second
  -> ~232 cores, say 30 machines of 8 cores
  -> ~$15,000/month. Trivial next to delivery.

video: ~1x real-time per rendition
  a 60 s clip x 4 renditions = 240 s of CPU
  10,000,000 video uploads/day x 240 s = 2.4e9 CPU-seconds/day
  = ~28,000 cores running continuously
  -> ~$1.5M/month, and this is why video products buy hardware encoders.
```

**Metadata, for scale contrast:**

```
100,000,000 posts/day x 500 bytes = 50 GB/day
                                  = 18 TB/year
                                  x 3 replicas = 55 TB/year

against 95 PB/year of media.

-> the metadata is 0.06% of the storage.
   All the interesting database work is on 0.06% of the bytes.
```

**That ratio is the single best line to say in this interview.**

**Latency budget.**

```
feed API (JSON only)          ~50 ms
image from CDN edge, hit      ~20-50 ms
image from origin, miss       ~200-400 ms
blurhash render               ~0 ms (it is in the JSON)

-> perceived load time is dominated by the CDN hit rate,
   not by anything your servers do.
```

---

## 7. The trade-offs

**Pre-signed uploads against proxying through your API.** Pre-signed removes 2.3 GB/s from your application
tier and is unambiguously right at scale. **The cost is that you cannot inspect the bytes as they arrive** —
validation, virus scanning and content moderation all have to happen after the fact, asynchronously, which
means a brief window where an unscanned object exists in your bucket. **Bound it by keeping originals in a
separate bucket that is never publicly readable.**

**Pre-generated variants against on-demand resizing.** Pre-generating costs 30% more storage and makes every
read a static file fetch. **On-demand stores less and puts a compute service on the read path of the
most-read thing in the system** — and the first request for each size is slow, which is exactly the request a
real user makes. **Pre-generate, and treat on-demand as an option only for rare sizes.**

**Storage tiering against retrieval latency.** Archival classes are five times cheaper and take minutes to
restore. **For a photo nobody has viewed in a year that is fine; for a photo that suddenly goes viral it is
not**, so the tiering rule needs a way back — usually a small standard-class copy of anything that gets
requested from archive.

**Signed URLs against cacheability.** A per-user signature makes every URL unique and **destroys the CDN cache
entirely** — the thing the whole architecture depends on. Signing the path and expiry instead keeps one cache
entry per image, **at the cost that a leaked URL works for anyone until it expires.** That is the standard
compromise and it should be stated, not hidden.

**Immediate visibility against transcoded visibility.** Showing the post immediately, rendered from the local
file, is a much better experience and means a follower can briefly see a post whose image is not ready.
**Waiting for transcoding is simpler and makes the poster stare at a spinner.** Show immediately for the
author, publish to followers only when the variants exist.

**And the honest one: delete is not delete.** The metadata flag is instant, the CDN purge takes minutes and is
not guaranteed everywhere, and the objects go last. **A user asking "is my photo gone" is asking about the
third thing and you are telling them about the first**, and under regulations like GDPR the distinction is
legally material.

**When would I not build this?** **Never build the media layer yourself when a managed one exists.**
Cloudinary, imgix and Mux do uploads, transcoding, variants and delivery, and below a few million users they
are cheaper than the engineers. **And if the product is not media-first** — a marketplace with a few product
photos — this entire pipeline is one S3 bucket, a CDN and a resize-on-upload lambda, and building the rest is
pure overhead.

---

## 8. In the interview

### How it gets asked

- *"Design Instagram."* — usually with a scale like five hundred million users.
- *"How does the upload work?"* — the pre-signed URL question.
- *"Where does the image resizing happen?"*
- *"How much does this cost to run?"* — the question this design is uniquely good for.
- *"How do you deliver images fast in India and Brazil?"* — the CDN question.
- *"What changes for video?"*

### The first ninety seconds

> "Instagram is two systems that happen to share a product, and I would separate them immediately because they
> have almost nothing in common.
>
> **The metadata system** — posts, follows, likes, the feed — **is small structured data**, about five hundred
> bytes a post, and it is the news feed design: precomputed timelines, hybrid fan-out for celebrities,
> hydration by batched multi-get. **I can go deep on that if you want, and I would rather spend the time on the
> other half**, because that is what makes this Instagram and not Twitter.
>
> **The media system is images, at two megabytes each — roughly seven thousand times a tweet.** Everything
> about it is different.
>
> **Sizing, and one ratio tells the whole story.** Five hundred million daily users viewing fifty photos a day
> is twenty-five billion views. At an average delivered size of a hundred and fifty kilobytes, that is
> **3.75 petabytes a day of egress** — about 350 gigabits a second sustained.
>
> **Meanwhile the metadata is fifty gigabytes a day. The media is 0.06 percent of the bytes' worth of database
> work and 99.94 percent of the bytes.**
>
> **Four decisions on the media path.**
>
> **One: uploads never touch my servers.** The client asks the API for permission and gets a short-lived
> pre-signed URL, then uploads directly to object storage. **Otherwise 2.3 gigabytes a second flows through
> machines whose job is business logic.** My server handles two hundred bytes of JSON.
>
> **Two: transcoding is asynchronous.** The upload completes, an event goes on a queue, workers produce four
> variants — thumbnail, small, medium, large — as WebP. **The user sees their own post immediately, rendered
> from the local file; followers see it when the variants exist.**
>
> **Three: variants are pre-generated, not resized on demand.** Thirty percent more storage, and every read
> becomes a static file fetch rather than a compute service on the hottest read path in the system.
>
> **Four: the CDN, which is not an optimisation here — it is the only affordable design.** Serving 3.75
> petabytes a day from S3 directly is about **three hundred and forty-five thousand dollars a day**, which is
> not a business. With a CDN at a ninety-five percent hit rate it is about ninety thousand. **The cache hit
> rate is the single most valuable number in the system.**
>
> **One question before I go deeper: photos only, or video too?** Because video's transcoding cost is roughly
> real-time per rendition, and it becomes the dominant infrastructure expense in a way photos never do."

### The follow-ups

**"Walk me through what happens when I upload a photo."**

> "Six steps, and the important thing is which of them the user waits for.
>
> **One: the client calls my API saying it wants to upload.** The API generates a media id, creates a
> `pending` metadata row, and returns **a pre-signed URL** — a short-lived signed permission to write one
> specific object to my bucket. **Fifteen minutes of validity, and the key is server-generated so the client
> cannot choose where to write.** That call is about ten milliseconds and moves no image data.
>
> **Two: the client uploads the two megabytes directly to object storage.** A couple of seconds on 4G, and
> **none of it goes through my servers** — which is the whole reason for the handshake. At a thousand uploads
> a second, proxying would be 2.3 gigabytes a second through machines meant for business logic.
>
> **Three: storage emits an event onto a queue.** From here everything is asynchronous.
>
> **Four: a transcode worker picks it up.** It reads the original, **honours the EXIF orientation flag** —
> which is not optional, because phones store the sensor image plus a rotation, and skipping it makes a
> quarter of your users' photos come out sideways — **strips the GPS metadata**, which is a privacy
> requirement rather than a size optimisation since a photo taken at home carries the user's address, and
> writes four WebP variants back to storage.
>
> **And that worker must be idempotent**, because storage events are at-least-once. A `SET NX` on the media id
> before starting, or the same image gets transcoded several times and transcoding is where the CPU bill is.
>
> **Five: the post is marked ready and fanned out to followers' timelines.** Publishing only after the
> variants exist means no follower ever sees a post with an unloadable image.
>
> **Six, and it happens out of order: the author sees their own post immediately**, rendered from the local
> file on their phone while steps three to five are still running. **They never wait for any of this**, which
> is the product decision that makes the pipeline invisible."

**"How much does this cost to run, and where does the money go?"**

> "Almost all of it is egress, and the arithmetic is worth doing out loud because it justifies the entire
> architecture.
>
> **Twenty-five billion photo views a day at an average delivered size of a hundred and fifty kilobytes is
> 3.75 petabytes a day.**
>
> **Served straight from S3 at nine cents a gigabyte, that is about three hundred and forty-five thousand
> dollars a day** — ten million a month, on bandwidth alone. **That is not a product, it is a rounding error
> away from bankruptcy.**
>
> **With a CDN at a ninety-five percent hit rate:** five percent goes to origin at nine cents, ninety-five
> percent leaves the edge at roughly two cents with committed pricing — **about ninety thousand a day, or 2.7
> million a month.** Four times cheaper, and **that gap is why the CDN is structural rather than an
> optimisation.**
>
> **And the hit rate is the lever.** Going from ninety-five to ninety-eight percent cuts origin egress by
> sixty percent. **That is why I would sign URLs on the path and expiry rather than per user** — a per-user
> signature makes every URL unique and destroys the cache entirely, which is the most expensive possible
> mistake in this system.
>
> **Storage is the second line, and it never shrinks.** A hundred million uploads a day at 2.6 megabytes — the
> original plus four variants — is 260 terabytes a day, ninety-five petabytes a year. **All on standard
> storage that is about 2.2 million dollars a month and rising forever.**
>
> **Tiered by age it is about six hundred thousand** — three point seven times cheaper, from a lifecycle rule
> and nothing else — **because access follows a brutal power law: roughly eighty percent of views are of
> content from the last week.**
>
> **Photo transcoding is trivial by comparison** — about two hundred milliseconds of CPU per upload, so a few
> hundred cores, maybe fifteen thousand a month.
>
> **Video is where that changes.** Transcoding runs at roughly real-time per rendition, so a sixty-second clip
> with four renditions is four minutes of compute. **At ten million video uploads a day that is around
> twenty-eight thousand cores running continuously** — over a million a month, and it is why every serious
> video product ends up buying hardware encoders rather than renting general-purpose CPU."

**"How do you make images load fast for a user in India and one in Brazil?"**

> "This is the part of the system the user actually experiences as speed, and it is four things, none of them
> in my application code.
>
> **First, the CDN, which is Sadanand's printer near the school.** The image is copied once to an edge
> location and every subsequent request in that region is served from there — **twenty to fifty milliseconds
> instead of two hundred to four hundred across an ocean.** Both users hit their nearest edge and the origin
> is touched once per region per image.
>
> **Second, and this matters more than people expect: the client picks the variant.** A phone on a slow
> connection asks for the forty-kilobyte version, not the four-hundred-kilobyte one. **That is a tenfold
> difference in bytes and it dominates anything I can do on the server.** So the feed API returns URLs for
> every variant plus the dimensions, and the client chooses based on screen size and measured throughput.
>
> **Third, blurhash.** Twenty bytes in the feed JSON encoding a blurred version of the image, rendered
> instantly. **The perceived load is zero even when the real image takes a second**, and the layout does not
> jump because the JSON also carries the width and height so the client reserves the right space. **This costs
> nothing and it is the difference between a feed that feels fast and one that feels broken.**
>
> **Fourth, format.** WebP or AVIF instead of JPEG is roughly thirty percent fewer bytes at the same visual
> quality, and modern clients all support it — with a JPEG fallback negotiated by content type.
>
> **And one thing I would push back on if it came up: this is not solved by adding application servers in
> those regions.** **The feed API is a few hundred bytes; the images are megabytes.** Putting compute near
> users helps the fifty-millisecond JSON call and does nothing for the ninety-nine percent of bytes that are
> already coming from an edge cache. **The CDN hit rate is the metric to watch, and a falling one is the first
> sign that something — usually a URL-signing change — has broken cacheability.**"

### The model answer

*"Design Instagram: five hundred million daily users, photos and short videos, and I care about what it
costs."*

> "The cost framing changes what I emphasise, so let me start there and work backwards, because **almost the
> entire bill is bytes leaving the building.**
>
> **Two systems.** Metadata — posts, follows, feed — is about five hundred bytes a post and is the standard
> feed design: hybrid fan-out, precomputed timelines in Redis, batched hydration. **It is fifty gigabytes a
> day.** Media is two megabytes a photo and **3.75 petabytes a day of egress.** The metadata is 0.06 percent
> of the bytes, and I would not spend the interview on it.
>
> **The upload path: pre-signed URLs.** The API returns a fifteen-minute signed permission and the client
> uploads directly to object storage. **That removes 2.3 gigabytes a second from my application tier
> entirely** — my servers handle two hundred bytes of JSON per upload. **The cost is that I cannot inspect
> bytes on arrival**, so validation, virus scanning and moderation are asynchronous, and originals live in a
> bucket that is never publicly readable.
>
> **Transcoding: asynchronous, idempotent, four variants plus the original.** EXIF orientation honoured, GPS
> stripped. **The author sees their own post immediately from the local file; followers see it when the
> variants exist.** Photo transcoding is about two hundred milliseconds of CPU each — a few hundred cores,
> around fifteen thousand dollars a month, which is noise.
>
> **Delivery: CDN, and this is the whole cost story.** Serving 3.75 petabytes a day from origin is **$345,000
> a day.** With a CDN at ninety-five percent hit rate it is about **$90,000 a day.** Four times cheaper, and
> the hit rate is the lever — ninety-five to ninety-eight percent cuts origin egress by sixty percent.
>
> **Which means the most expensive possible mistake is breaking cacheability**, and the way that happens is
> per-user signed URLs. **I sign the path and expiry, not the user**, so all viewers of a photo share one cache
> entry — accepting that a leaked URL works until it expires.
>
> **Storage: ninety-five petabytes a year and it never shrinks.** All-standard is 2.2 million a month; tiered
> by age it is about six hundred thousand. **Eighty percent of views are of content under a week old**, so a
> lifecycle rule moving media to infrequent-access at a week and archive at ninety days is a 3.7× saving for
> no engineering. **With a caveat: archived media takes minutes to retrieve, so anything requested from
> archive gets promoted back**, or a photo that goes viral after a year is unservable.
>
> **Video, since the prompt includes it, and it changes the shape of the bill.** An adaptive ladder — four
> renditions, chunked, with an HLS manifest — so the player switches quality as the network changes.
> **Transcoding is roughly real-time per rendition**, so a sixty-second clip is four minutes of compute. At ten
> million video uploads a day that is around twenty-eight thousand cores continuously — **over a million a
> month, and it overtakes everything except delivery.** That is the argument for hardware encoders or spot
> capacity, and it is a decision worth making early because it is hard to retrofit.
>
> **So the ranked bill:** delivery $2.7M, storage $600K, video transcoding $1M+, everything else combined
> under $100K. **Three of the four levers are in the media path and none of them is in my application code.**
>
> **Two things I would raise as risks.** **Delete is not delete** — the metadata flag is instant, the CDN purge
> takes minutes and is not guaranteed at every edge, and the objects go last. **Under GDPR that distinction is
> legally material** and I would want it written down rather than discovered during an audit.
>
> **And I would seriously ask whether to build the media layer at all.** Cloudinary, imgix and Mux do uploads,
> transcoding, variants and delivery. **At five hundred million users the per-unit economics favour building
> it**, and I would want that to be a calculation rather than an assumption — because below a few million
> users the managed service is cheaper than the team."

---

## 9. Recall card

**Two systems, and say so in the first minute:** metadata is ~500 bytes a post and is the standard feed design;
**media is ~2 MB a photo — 7,000× a tweet** — and is 99.94% of the bytes. All the interesting database work is
on 0.06% of the data.

**Uploads never touch your servers: pre-signed URLs.** The API returns a short-lived signed permission and the
client PUTs directly to object storage — **2.3 GB/s removed from the application tier**, at the cost of
after-the-fact validation and moderation.

**Transcoding is asynchronous and must be idempotent** (storage events are at-least-once). **Honour EXIF
orientation** or a quarter of photos come out sideways; **strip GPS** — a privacy requirement, not a size one.
**Pre-generate 4 variants**, don't resize on demand: 30% more storage against a compute service on the hottest
read path.

**The CDN is not an optimisation — it is the only affordable design.** 3.75 PB/day from origin is **~$345K/day**;
at a 95% hit rate ~$90K/day. **So the most expensive possible mistake is a per-user signed URL**, which makes
every URL unique and destroys the cache — **sign the path and expiry instead.**

**Storage never shrinks: 95 PB/year.** All-standard $2.2M/month, **tiered by age ~$600K** — 80% of views are of
content under a week old. Anything pulled from archive must be promoted back.

**The feed returns URLs, not bytes**, plus dimensions and a **blurhash** (20 bytes, instant render, no layout
jump) — and **the client picks the variant**, which is a 10× difference in bytes on a slow connection.
**Video's adaptive ladder costs ~1× real-time per rendition** and becomes the dominant compute bill.
**And delete is not delete:** metadata instant, CDN purge minutes and not guaranteed, objects last.
