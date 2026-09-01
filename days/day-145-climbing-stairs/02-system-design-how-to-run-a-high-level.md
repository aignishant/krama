---
day: 145
track: system-design
title: "How to run a high-level design interview: the forty-five-minute script"
phase: "High-level design case studies"
status: written
---

# How to run a high-level design interview: the forty-five-minute script

## 1. What this is, and why they ask it

Somebody says "design Twitter" and then stops talking. There is a whiteboard, or an empty document, and
forty-five minutes.

The thing that goes wrong is not knowledge. Most candidates who fail this round know what a cache is and what
sharding means. What they do not have is **an order**, so they start drawing boxes, get pulled into a detail
somebody asked about at minute six, and run out of time having never mentioned the thing the interviewer was
actually waiting for.

**This lesson is a script.** Six phases, with a rough number of minutes on each and a stated goal for each.
It is not a formula for a good design — it is a way of not freezing, of covering the ground the interviewer is
marking against, and of controlling the clock so that the interesting part gets time.

Everything from here to day 170 is a case study run against this script. **Today is the script itself**, and
it is the most reusable thing in the entire system design track: the same six phases work for Twitter, Uber,
Dropbox, a rate limiter and a system nobody has ever asked about before.

By the end of this lesson you can run the six phases with the clock, know what to say in each and what to
leave out, recognise the four ways candidates lose the round, and handle the two hardest moments — being
interrupted, and not knowing.

---

## 2. The story

Sister Mary has worked casualty at the same hospital for twenty-six years, and the thing she is known for is
that she is slow to start.

A man came in on a Tuesday with his hand wrapped in a towel that was soaked through, and three people were
talking at once, and the natural thing — the thing every new nurse does — is to go straight for the hand,
because it is the thing everybody is looking at.

She did not go for the hand. She asked his name and whether he could tell her what happened. Not out of
politeness: if he can answer, he is breathing and conscious and oriented, and that is three of her five
questions settled in four seconds.

Then she looked at his colour and his breathing, then his pulse, then she asked what he had taken today, and
only then did she unwrap the hand.

The registrar who was new that year found this maddening for about six months. There is a bleeding hand and
she is asking about tablets.

What changed his mind was a Thursday when a woman came in having fallen off a scooter, with a bad graze down
one arm that everybody was looking at, and Sister Mary went through the same five questions in the same order
and on the third one — the pulse — she did not like it, and the woman was on a trolley and through to the back
in under two minutes with something internal that nobody would have looked for another twenty minutes if they
had started with the arm.

Her line about it, which she has said many times and which the registrar quotes to people now, is that the
dramatic injury is very often not the dangerous one, and that **the order exists precisely because you cannot
tell which is which by looking.**

The other thing about the order is what it does for her when she is tired. On a bad night at four in the
morning, with four people waiting and someone shouting in the corridor, she does not have to decide what to do
next. **The order decides, and she just does it**, and that is worth more at four in the morning than any
amount of judgement.

---

## 3. The idea in plain English

Sister Mary's five questions are the script, and both of her observations apply directly.

**The dramatic thing is usually not the dangerous thing.** In a design interview the dramatic thing is the
clever bit — the sharding scheme, the consistent hashing, the fan-out strategy. **The dangerous thing is
usually the requirements, which nobody asks about**, or the scale estimate, which decides everything and takes
three minutes.

**And the order decides so you do not have to.** Under pressure, with forty-five minutes and someone watching,
having a fixed sequence means you are never choosing what to do next.

**The six phases, with minutes:**

| Phase | Minutes | The goal |
|---|---|---|
| **1. Requirements** | 5 | Agree what you are building and what you are not |
| **2. Scale** | 5 | Turn users into numbers that decide the design |
| **3. API and data model** | 5 | Fix the contract and the entities |
| **4. High-level design** | 10 | The boxes and arrows that satisfy phase 1 |
| **5. Deep dive** | 15 | The one or two hard parts, in detail |
| **6. Wrap-up** | 5 | Bottlenecks, failures, what you would do next |

**Phase 1 — Requirements, five minutes.** Ask, do not assume. "Design Twitter" means nothing until you know
whether it includes search, direct messages, trends, ads, or none of those. **List three or four functional
requirements and explicitly say what you are excluding.**

Then the non-functional ones, and these matter more: how many users, read-heavy or write-heavy, what latency,
what availability, and — the one nobody asks — **what consistency does this actually need?** A feed can be
seconds stale. A balance cannot.

**Say your assumptions out loud and write them down.** An interviewer who disagrees will correct you, which is
free information. An assumption you never stated is one you can be marked down for later.

**Phase 2 — Scale, five minutes.** Turn the user count into numbers.

```
daily active users -> requests per second -> peak -> storage per year -> bandwidth
```

**This is five minutes of arithmetic and it decides the whole design.** Two hundred writes a second needs no
sharding and no queue; two hundred thousand needs both. **A candidate who skips this is guessing for the next
forty minutes**, and it shows.

**Phase 3 — API and data model, five minutes.** Three or four endpoints, with their parameters. Then the main
entities and their key fields. **This is where you decide relational or not**, and it should follow from the
access pattern rather than from preference.

**Phase 4 — High-level design, ten minutes.** Now draw. Client, load balancer, services, databases, caches,
queues. **Trace one write and one read through the whole picture out loud** — that is what makes it a design
rather than a diagram, and it catches missing pieces immediately.

**Keep it boring.** The high-level picture should be unsurprising. The interesting decisions belong in phase
5, and putting them here means you spend your best fifteen minutes explaining boxes.

**Phase 5 — Deep dive, fifteen minutes.** The largest block, and the one that is actually being marked.

**Ask which part to go deep on.** "The two hard parts here are the feed fan-out and the search index — which
would you like?" That is not weakness; it is how you avoid spending fifteen minutes on the half they did not
care about. If they say "you choose", pick the one with a real trade-off and say why.

**Then go properly deep: the mechanism, the numbers, the failure mode, and the alternative you rejected.**
Depth is what separates candidates, and it is impossible if phases 1 to 4 ran long.

**Phase 6 — Wrap-up, five minutes.** Name the bottleneck. Say what breaks first as traffic grows tenfold. Name
what you would monitor. And say what you deliberately left out and would do next.

**Ending with "here is what I would do next" is much stronger than trailing off**, because it shows you know
the design is unfinished, which every real design is.

**Now the four ways people lose this round**, and they are all about time rather than knowledge:

**Drawing before asking.** Twenty minutes into a design for a system whose requirements were never agreed.
Everything after that is unmarkable, because it might be answering the wrong question.

**No numbers.** "We'll shard the database" without knowing whether one machine would do. **Every design
decision should be traceable to a number from phase 2**, and if it cannot be, it is decoration.

**Breadth with no depth.** Mentioning fifteen components and going into none. The interviewer needs to see
you reason about one thing properly, not list things you have heard of.

**Losing the clock.** Being at minute forty with the deep dive not started. **The fix is a running commentary
on time** — "I've used about ten minutes on the high-level, so let me go deep on the fan-out now" — which also
signals that you are managing the session rather than being carried by it.

**And the two hard moments.**

**Being interrupted.** An interviewer's question is almost always a hint, not an attack. Answer it, then say
where you were. If it drags you off the script for five minutes, say so: "That's taken us into the deep dive
early — shall I carry on here, or finish the high-level first?"

**Not knowing.** Say so, and then say how you would find out or what you would use instead. **"I don't know
Cassandra's exact consistency levels, but the property I need is that a read sees my own write, and I would
check whether it can give me that"** is a much better answer than a confident wrong one — and interviewers
generally cannot tell how much you know, only how you handle not knowing.

---

## 4. The picture

The script, with the clock:

```
  0 ---- 5 -------- 10 ------- 15 ---------------- 25 ------------------------ 40 ---- 45
  |      |          |          |                   |                            |       |
  |  1.  |    2.    |    3.    |        4.         |            5.              |   6.  |
  | REQS |  SCALE   | API +    |   HIGH-LEVEL      |        DEEP DIVE           | WRAP  |
  |      |          | DATA     |   DESIGN          |                            |       |
  | ask, | numbers  | contract | boxes, arrows,    | one or two hard parts:     | bottle|
  | scope| that     | and      | trace one write   | mechanism, numbers,        | necks,|
  | out  | decide   | entities | and one read      | failure, alternative       | next  |
  |      |          |          |                   |                            | steps |

           \_____ 15 minutes of setup _____/        \___ the part being marked ___/
```

**What to notice.** The first fifteen minutes are setup and should feel almost mechanical. **The deep dive is
a third of the session**, and every minute overspent earlier comes out of it.

What each phase produces, concretely:

```
PHASE 1 OUTPUT
  in scope:      post a tweet, see a home feed, follow a user
  out of scope:  search, DMs, ads, trends          <- say this explicitly
  non-functional: read-heavy ~100:1, feed can be 5s stale, 99.9% availability

PHASE 2 OUTPUT
  200M DAU, 2 posts/user/day     -> 400M posts/day -> 4,600 writes/s, peak ~14,000
  100:1 read ratio               -> 460,000 reads/s
  300 bytes/post x 400M x 365    -> 44 TB/year
  -> writes fit on one machine; reads do not. THAT is the design driver.

PHASE 3 OUTPUT
  POST /tweets {text}            -> {id, created_at}
  GET  /feed?cursor=...&limit=20 -> [{tweet}]
  POST /follow {user_id}
  entities: users, tweets, follows(follower_id, followee_id)

PHASE 4 OUTPUT
  a diagram, and one write and one read traced through it out loud

PHASE 5 OUTPUT
  fan-out on write vs on read, with the celebrity number,
  the hybrid, and what it costs

PHASE 6 OUTPUT
  bottleneck: feed assembly for high-follower accounts
  at 10x: the fan-out queue, before the database
  monitor: feed p99, fan-out lag, cache hit rate
  next: search, and per-user ranking
```

**What to notice about phase 2.** The last line — "writes fit on one machine; reads do not" — is a *decision*
produced by arithmetic. **Every later choice should point back to a line like that.**

And the four failure modes, as a timeline:

```
  GOOD                    0---5---10---15---------25--------------40--45
                          reqs scale api  high-level   deep dive    wrap

  drawing first           0-------------------------------------------45
                          boxes, boxes, boxes, and an unclear question

  no numbers              0---5---[skipped]---api---high-level------45
                          every decision is a guess wearing confidence

  breadth, no depth       0---5---5---5---[15 components, 2 min each]--45

  lost the clock          0-------12--------22-----------38---[deep dive]-45
                                                              5 minutes left
```

---

## 5. How it actually works

The script, phase by phase, with what to actually say.

### Phase 1 — Requirements (5 min)

**Ask four or five questions. Do not design yet.**

```
"Which of these are in scope: posting, the home feed, following, search, DMs, notifications?"
"How many users, roughly? Daily active?"
"Read-heavy or write-heavy, and by roughly what ratio?"
"How fresh does the feed need to be — seconds, or can it be a minute behind?"
"Is this global or one region?"
```

**Then state the scope back, including the exclusions:**

> "So: posting, the home feed and following are in scope; search, DMs and ads are out. Two hundred million
> daily actives, heavily read-skewed, and the feed can be a few seconds stale. I'll assume global with users
> concentrated in a few regions — tell me if that's wrong."

**The exclusions matter as much as the inclusions**, because they are what stops you being marked down for
not covering something you deliberately dropped.

### Phase 2 — Scale (5 min)

**The standard chain, and it is always the same four steps:**

```
1. users -> actions per user per day -> actions per day
2. actions per day / 86,400 -> average per second; x3 to x5 -> peak
3. bytes per record x records per day x 365 -> storage per year
4. bytes per response x reads per second -> bandwidth
```

Worked, out loud:

```
200,000,000 DAU x 2 posts        = 400,000,000 posts/day
400,000,000 / 86,400             = ~4,600 writes/s
x3 for peak                      = ~14,000 writes/s

reads at 100:1                   = ~460,000 reads/s

300 bytes/post x 400M            = 120 GB/day
x 365                            = 44 TB/year
```

**Then the sentence that turns arithmetic into a decision:**

> "So the write path is modest — fourteen thousand a second is one well-provisioned database with a queue in
> front. The read path is four hundred and sixty thousand a second, which is not, and that is the whole
> design problem."

**Round aggressively.** 86,400 is 100,000. A day is 10⁵ seconds. **Nobody is checking your arithmetic; they
are checking whether you use numbers at all.**

**Numbers worth having memorised** so the arithmetic is fast:

```
1 day             ~100,000 seconds  (86,400)
1 million/day     ~12 per second
1 billion/day     ~12,000 per second
1 KB x 1M/day     ~1 GB/day, ~365 GB/year
```

### Phase 3 — API and data model (5 min)

**Three or four endpoints, with parameters and return shapes.** Not a full specification.

```
POST /tweets            {text}                    -> {id, created_at}
GET  /feed              ?cursor=&limit=20         -> [{id, author, text, created_at}]
POST /users/{id}/follow                           -> 204
```

**Cursor-based pagination, not offset**, and say why in half a sentence: offsets shift as new items arrive, so
a user paging through a feed sees duplicates and gaps. **That is a small detail that signals experience.**

**Then the entities and the storage choice, derived from the access pattern:**

> "Users, tweets, and a follows table with `(follower_id, followee_id)`. The follows table is the interesting
> one — I need 'who follows me' for fan-out and 'who do I follow' for the read path, so I'd index both
> directions. Tweets are append-only and never updated, which is a hint that they don't need a relational
> store, but I'd start relational and move if the numbers say so."

### Phase 4 — High-level design (10 min)

**Draw the boring version.**

```
client -> CDN (static) -> load balancer -> API servers
                                              |
                          +-------------------+-------------------+
                          |                   |                   |
                      write path          read path           async
                          |                   |                   |
                    tweet service       feed service        queue -> workers
                          |                   |                   |
                      database            cache + DB         fan-out, notifications
```

**Then trace one write and one read out loud**, which is the part that makes it a design:

> "A post: client hits the API, we write the tweet to the database, publish an event, and return. The fan-out
> worker picks up the event and pushes the tweet id into the feed cache of each follower.
>
> A feed read: client hits the API, we read the precomputed list of tweet ids from the cache, hydrate them from
> the tweet store — probably also cached — and return twenty. Cache miss falls back to assembling from the
> database."

**Tracing catches missing pieces immediately**, and it is much more convincing than pointing at boxes.

### Phase 5 — Deep dive (15 min)

**Offer a choice:**

> "The two genuinely hard parts here are the feed fan-out and the celebrity problem. Which would you like me to
> go into?"

**Then, whichever it is, cover four things:**

1. **The mechanism.** How it actually works, concretely.
2. **The numbers.** What it costs, sized from phase 2.
3. **The failure mode.** What breaks, and what happens then.
4. **The alternative.** What you rejected and why.

**That fourth one is what makes it a trade-off rather than a decision**, and it is the most commonly missing
part.

### Phase 6 — Wrap-up (5 min)

**Four sentences:**

> "The bottleneck is feed assembly for accounts with millions of followers — everything else has headroom.
>
> At ten times the traffic, the fan-out queue saturates before the database does, and I would shard the workers
> by user id.
>
> I would monitor feed p99, fan-out lag as a time rather than a queue depth, and cache hit rate — a hit rate
> below eighty percent means the cache is adding a hop rather than saving one.
>
> What I have left out: search, ranking, and media. Search would be a separate index fed from the same event
> stream, and I would do that next."

**Naming what you left out is not a weakness.** It shows you know the boundary of what you built, and it gives
the interviewer somewhere to take the conversation if there is time.

### Handling interruptions

Almost every interruption is a hint. **Three responses:**

**If it is a small correction**, take it and move on. "Good point, yes — the cursor should be the tweet id, not
a timestamp, because timestamps collide."

**If it pulls you deep early**, answer properly and then reorient: "That's the fan-out question, which I was
going to cover in the deep dive — shall I do it now and come back to the high-level after?"

**If you disagree**, say so once, with a reason, and then defer: "I'd push back slightly — at fourteen thousand
writes a second I don't think we need to shard yet. But if you'd like me to design for a hundred times that,
I'll change the storage layer."

### The universal opening

If you are given a system you have never thought about, the first ninety seconds are always the same:

> "Let me start by pinning down what's in scope, then size it, and then design against those numbers. Can I ask
> a few questions first?"

**That sentence works for every prompt**, and it buys you thirty seconds to think while sounding like a plan.

---

## 6. The numbers

**The estimation toolkit — memorise these six and the arithmetic is fast.**

```
seconds in a day               86,400      ->  round to 100,000
1 million/day                  ~12/second
1 billion/day                  ~12,000/second
peak multiplier                3x to 5x average
read:write ratio, social       100:1 to 1000:1
```

**The latency ladder** — for justifying where things live:

```
memory                 100 ns
SSD read               100 us
same-datacentre hop    0.5 ms
cross-region           80 ms
cross-planet           200 ms
```

**Capacity per machine** — for deciding how many:

```
web server             ~10,000 requests/s
Redis                  ~100,000 ops/s
Postgres               ~10,000 writes/s; a hot row ~200/s
Kafka                  ~100,000 msg/s per broker
WebSocket connections  ~50,000-100,000 per machine
```

**Storage per record** — for the yearly figure:

```
a tweet / short post   ~300 bytes
a user row             ~1 KB
a photo                ~2 MB
a video minute         ~50 MB
a log line             ~200 bytes
a metric point         ~1.5 bytes compressed
```

**A full worked estimate, in the order you would say it:**

```
"Design Instagram."

200M DAU, 1 photo uploaded per user per week
  uploads/day     200,000,000 / 7            = ~28,000,000
  per second      28,000,000 / 100,000       = ~280 writes/s
  peak x5                                    = ~1,400 writes/s
                                             -> writes are easy

feed views: 20 per user per day
  reads/day       200,000,000 x 20           = 4,000,000,000
  per second      4,000,000,000 / 100,000    = ~40,000 reads/s
  peak x5                                    = ~200,000 reads/s
                                             -> reads are the problem

storage
  2 MB per photo x 28,000,000/day            = 56 TB/day
  x 365                                      = 20 PB/year
                                             -> object storage, obviously
                                             -> and the CDN is not optional

bandwidth
  200,000 reads/s x 200 KB (a thumbnail)     = 40 GB/s
  at $0.09/GB egress                         = $3,600/second at origin prices
                                             -> a CDN is a COST decision, not
                                                a latency one
```

**That last line is the point of doing the arithmetic.** The CDN was already obvious; the number tells you it
is the largest line on the bill and therefore a first-class design concern rather than an afterthought.

**Time budget within the interview itself:**

```
phase 1  5 min   ~10%
phase 2  5 min   ~10%
phase 3  5 min   ~10%
phase 4  10 min  ~22%
phase 5  15 min  ~34%      <- the part being marked
phase 6  5 min   ~10%
```

**If you are at minute 25 and have not started phase 5, you are behind** — and the fix is to compress phase 4
by saying "let me keep the high-level brief and spend the time on the fan-out."

---

## 7. The trade-offs

**The script costs you spontaneity and buys you coverage.** Following it means you will occasionally spend
five minutes on requirements for a problem where the interviewer wanted to jump straight in. **That is a much
smaller cost than the alternative**, which is designing the wrong system confidently. If the interviewer says
"assume the requirements, go", drop phase 1 to ninety seconds and keep the rest.

**Breadth against depth, and the script is deliberately weighted.** Fifteen of the forty-five minutes are one
or two components in detail. That means whole areas go unmentioned — and **saying so in phase 6 is how you get
credit for knowing they exist** without spending time on them.

**Numbers against speed.** Five minutes of arithmetic is a ninth of the session and it is the highest-value
five minutes there is, because every subsequent decision either follows from it or is a guess. **The only time
to skip it is when the interviewer explicitly says the scale is not the point.**

**Asking questions against appearing decisive.** Some candidates worry that asking looks uncertain. It does
not — **it looks like someone who has built something before**, because nobody who has built a real system
starts without agreeing scope. The failure mode is asking too many, or asking questions whose answers do not
change the design. **Ask four or five, and only ones whose answer would change what you build.**

**And the honest limit of the script: it is a way of not failing, not a way of being brilliant.** It guarantees
you cover requirements, scale, structure and depth. What it cannot supply is the insight in phase 5 — the
observation that a celebrity breaks fan-out on write, or that driver locations do not need durability. **The
script gets you to the point where that insight is worth having**, which is the most it can do.

**When would I deviate?** When the interviewer drives — follow them, and use the script only to notice what is
being skipped. When the prompt is a narrow component rather than a system — "design a rate limiter" — where
phases 1 and 2 compress to two minutes and the deep dive is almost the whole session. And when you genuinely
know the domain deeply, where leading with the hard part can be stronger, as long as requirements and scale
still get their five minutes.

---

## 8. In the interview

### How it gets asked

- *"Design Twitter."* — and nothing else. The prompt is deliberately empty.
- *"Design a URL shortener / a chat app / Uber."*
- *"Design a system you have never seen before."* — day 170's mock.
- *"How would you approach this?"* — occasionally asked directly, which is a gift.

### The first ninety seconds

> "Let me pin down what's in scope, then size it, and then design against those numbers — that way every choice
> traces back to something. Can I ask a few questions first?
>
> **What's in scope?** Posting, the home feed and following, I assume — is search in scope? Direct messages?
> Ads?
>
> **How many users?** Daily active rather than registered, if you have a figure.
>
> **Read-heavy or write-heavy?** For something feed-shaped I'd assume very read-skewed, maybe a hundred to
> one, but I'd rather use your number.
>
> **And how fresh does the feed have to be?** Because 'within a few seconds' and 'immediately' lead to
> completely different designs.
>
> ...
>
> Right. So: posting, feed and follows in scope; search and DMs out of scope. Two hundred million daily
> actives, roughly a hundred to one read-skewed, and a few seconds of feed staleness is acceptable. I'll assume
> we're global with the users concentrated in a handful of regions — stop me if that's wrong.
>
> Let me spend a couple of minutes turning that into numbers, because the write path and the read path are
> going to need very different answers and I want to know which one is actually hard before I design either."

### The follow-ups

**"Skip the requirements, just design it."**

> "Happily — let me state what I'm assuming in about thirty seconds so you can correct me, and then go
> straight to the design.
>
> I'm assuming posting, home feed and follows are in scope and search isn't; a couple of hundred million daily
> actives; heavily read-skewed; and that a few seconds of feed staleness is fine. If any of those is wrong,
> the design changes and I'd rather know now than at minute thirty.
>
> **The reason I still say them rather than skipping entirely** is that half of them are load-bearing. If the
> feed had to be immediately consistent I couldn't precompute it, and that changes the whole architecture. So
> it's thirty seconds rather than five minutes, but it isn't zero.
>
> Then I'd go straight to sizing, because I need to know whether the read path is four thousand a second or
> four hundred thousand before I decide whether it needs a cache at all."

**"You're spending too long on estimation."**

> "Fair — let me get to the decision and move on.
>
> The numbers I actually need are: about fourteen thousand writes a second at peak, about four hundred and
> sixty thousand reads a second at peak, and forty-four terabytes a year. **The decision that follows is that
> the write path fits comfortably on a single primary with a queue in front, and the read path does not fit
> anywhere without precomputation** — so the design problem is entirely on the read side.
>
> That's the only thing I needed the arithmetic for, and I'll refer back to those three numbers rather than
> recomputing.
>
> **The reason I do it at all** is that without it I'd be guessing whether to shard, and sharding a system that
> doesn't need it is a common and expensive mistake. But you're right that thirty seconds of it is worth as
> much as five minutes."

**"How do you handle not knowing something?"**

> "Say so immediately, and then say what I'd do about it — because a confident wrong answer is much worse than
> an honest gap, and interviewers can usually tell the difference.
>
> Concretely: **'I don't know Cassandra's exact consistency level names. What I need here is read-your-writes
> for the author's own timeline, and I'd check whether it can give me that — if not, I'd read the author's own
> recent posts from the primary and merge them in.'** That answers the actual question, shows I know what
> property matters, and does not pretend.
>
> **The related move is to say what I would measure rather than guess a number.** If asked what the cache hit
> rate would be, 'I don't know, and it depends on the access distribution — I'd instrument it before sizing the
> cache, and design so that a low hit rate degrades rather than breaks' is better than inventing ninety
> percent.
>
> **And if it is something I genuinely should know**, I'd say that too and move on rather than dwelling. One
> sentence of acknowledgement, then back to the design — the round is forty-five minutes and there is no time
> to be embarrassed in."

**"You have five minutes left and you're mid-deep-dive."**

> "Then I'd stop the deep dive and spend the five on the wrap-up, because an unfinished deep dive plus a
> summary beats a finished deep dive with no summary.
>
> Concretely I'd say: 'Let me pause here and close out, and I can come back if there's time.' Then the four
> wrap-up sentences — the bottleneck, what breaks at ten times the load, what I'd monitor, and what I
> deliberately left out.
>
> **The reason that ordering is right** is that the wrap-up is where I demonstrate that I know the design is
> incomplete and know *how* it is incomplete, which is a senior signal. Trailing off mid-sentence at
> forty-five minutes signals the opposite, even if the content was better.
>
> **And I'd watch the clock out loud earlier than that**, so it doesn't happen. Around minute twenty-five I
> would normally say 'I've used about ten minutes on the high-level, so let me go deep on the fan-out now' —
> which both manages the time and signals that I'm running the session rather than being carried by it."

### The model answer

*"Design a URL shortener."* — run against the script, compressed to show the shape.

> **Phase 1, requirements — two minutes.** "Is custom aliasing in scope? Analytics on clicks? Expiry? I'll
> assume: shorten a URL, redirect, optional custom alias, and basic click counts — and I'll exclude user
> accounts and ads. Non-functional: redirects must be fast, single-digit milliseconds, because they're on the
> critical path of somebody else's page load. Availability matters more than consistency — a redirect that
> works is worth more than one that's perfectly fresh. And it's extremely read-heavy."
>
> **Phase 2, scale — three minutes.** "Say a hundred million new URLs a month. That's about forty a second on
> average, a couple of hundred at peak — trivial. Reads at a hundred to one is four thousand a second average,
> maybe twenty thousand peak. Storage: a hundred million a month at, say, five hundred bytes is fifty gigabytes
> a month, six hundred gigabytes a year — small. **The decision: this fits on one database. The interesting
> problem is not scale, it's the ID generation and the redirect latency.**"
>
> **Phase 3, API — two minutes.** "`POST /urls {long_url, custom_alias?}` returns `{short_url}`.
> `GET /{code}` returns a 301 or 302. Entities: a single table of `code`, `long_url`, `created_at`,
> `expires_at`, `click_count`. `code` is the primary key, which makes the redirect a single primary-key lookup —
> and that is the entire read path."
>
> **Phase 4, high-level — five minutes.** "Client, load balancer, stateless app servers, a cache in front of
> the database, and the database. Write path: generate a code, insert, return. Read path: look up the code in
> the cache, fall back to the database, redirect. Click counts go onto a queue rather than being an update on
> the read path, because I do not want a write on every redirect."
>
> **Phase 5, deep dive — the code generation, and I'd offer the choice.** "The two interesting parts are how
> the code is generated and how the redirect gets to single-digit milliseconds. Which would you like?
>
> On generation: **hashing the URL and taking the first seven characters** is the obvious approach and it
> collides — birthday paradox says at a hundred million URLs over a 62⁷ space, collisions are rare but real,
> so it needs a check-and-retry loop, and that is a read before every write.
>
> **A counter encoded in base 62** avoids collisions entirely, is shorter, and gives sequential — therefore
> guessable — codes, which matters if anyone shortens something private. **A distributed counter is the
> problem**: a single sequence is a bottleneck and a single point of failure, so I'd hand each server a block
> of a thousand ids at a time from a central counter, which makes it one coordination call per thousand URLs
> and tolerates a server dying by wasting up to a thousand ids.
>
> **What I'd actually choose**: the counter with block allocation, plus base-62 encoding, plus a random offset
> or a shuffled alphabet so codes are not trivially enumerable. And I'd support custom aliases through the same
> table with a uniqueness constraint, which is where the collision handling actually earns its keep.
>
> The number that matters: seven base-62 characters is 3.5 trillion codes, which at a hundred million a month
> is about three thousand years. **Six characters would be fifty-seven billion, which is forty-seven years —
> also fine, and a shorter URL.** I'd start at six and have seven ready."
>
> **Phase 6, wrap-up — two minutes.** "The bottleneck is the redirect read, and it is entirely a cache problem
> — with a hot-key distribution, a small cache covers most traffic, and I'd expect well over ninety percent.
>
> At ten times the load, nothing structural changes; I'd add cache capacity and read replicas.
>
> I'd monitor redirect p99, cache hit rate, and the block-allocation counter's remaining headroom.
>
> **What I left out:** analytics beyond a click count, abuse prevention — which is genuinely important for a
> shortener and I'd do next — and expiry, which is a background job over `expires_at`. And I'd note that
> **301 versus 302 is a real decision**: 301 is cacheable by the browser and therefore fast and un-analysable,
> 302 gives me every click and costs a round trip. That is a product question, not a technical one."

---

## 9. Recall card

**Six phases, forty-five minutes: requirements (5), scale (5), API and data model (5), high-level design (10),
deep dive (15), wrap-up (5).** The first fifteen minutes are setup and should feel mechanical; **the deep dive
is what is being marked.**

**Phase 1: ask, and state the exclusions.** Phase 2: users → per second → peak → storage per year, and end
with **the sentence that turns arithmetic into a decision** ("writes fit on one machine; reads do not").

**Phase 4: draw the boring version and trace one write and one read out loud.** Phase 5: **offer a choice**,
then cover mechanism, numbers, failure mode, and **the alternative you rejected** — that last one is what makes
it a trade-off.

**Four ways to lose it, all about time:** drawing before asking; no numbers; breadth with no depth; and losing
the clock. **Narrate the time** — "I've used ten minutes on the high-level, let me go deep now."

**Interruptions are hints — answer, then reorient.** And **not knowing is fine if you say what you would do
instead**: "I don't know that product's consistency levels; the property I need is read-your-writes, and I'd
check whether it gives me that."
