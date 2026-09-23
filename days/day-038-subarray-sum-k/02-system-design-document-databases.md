---
day: 38
track: system-design
title: "Document databases"
phase: "Databases from zero"
status: written
---

# Day 038 · System Design — Document databases

**After today you can:** You can model a domain as documents and say where the model breaks.

**The interviewer asks it as:** *Model a blog in MongoDB. What happens when a user changes their name?*

---

## 1. What this is, and why they ask it

A **document database** stores each record as a self-contained document — a nested, JSON-shaped
value holding an entity and the things that belong to it, read and written as one unit. Where
yesterday's key-value store treats the value as an opaque bag, a document store can see inside:
index a field, query by it, update one nested piece in place. **MongoDB** is the product that
defines the category.

Interviewers use document modelling as a design test with teeth, and the hub question is the
classic form: model a blog, then — *what happens when a user changes their name?* The question is a
trap for people who embedded everything and a trap for people who referenced everything; the
passing answer knows the two tools, chooses per relationship using how the data is read and how
often it changes, and can name the failure modes — the unbounded array, the 16-megabyte ceiling,
the fact that atomicity stops at the document's edge. Everything needed to answer well is a
database costume over ideas already met: [day 029](../day-029-read-write-pointer/README.md)'s copies
that need owners, and [day 036](../day-036-two-pointers-revision/README.md)'s arranged-for-serving.

---

## 2. The story

Salim shoots weddings, and his phone gallery is organised the way his work arrives: one album per
wedding. Everything about the Fernandes wedding lives in the Fernandes album — the photos, the
short clips, a screenshot of the booking message, the venue pin, the shot list the bride sent.
When the family calls a year later, he opens one album and their whole world is in his hand.
Nothing to gather. That is the design, and on delivery day it is unbeatable.

The design has a seam, and he knows exactly where it runs.

His cousin Rafiq assists at most shoots, and Salim used to note Rafiq's number inside each album's
notes, so everything stayed in one place. Then Rafiq changed his number. Salim fixed it in the
Colaco album, missed it in nine others, and spent a furious Sunday months later, opening every
album one by one, because a caterer had reached a dead number found in an old shared album. These
days Rafiq's number lives in exactly one place — the phone's contacts — and albums say only
*Rafiq*. One fact, one home. Looking it up is one extra tap, and he pays that tap gladly.

Some things he still copies into the album deliberately. The venue's address goes in even though it
is also in his contacts — because the address *as it was on that day* is part of that wedding's
record. If the hall renames itself next year, the Fernandes album should still say what the
invitation said. A copy that is *meant* to stay old, he has learnt, is not a mistake.

And one seam he only found at scale: the D'Souza wedding, three days, four thousand photos, and the
album so fat his phone stutters opening it. The gallery grumbles above a certain size. He split it
— main album, plus one per day — and made a note for the future: an album is for what belongs
together *and stays a sensible size*. Things that grow forever get their own album.

---

## 3. The idea in plain English

Salim's albums are documents. His three lessons — the number that changed, the address that
should not change, the album that grew too fat — are the entire discipline of document modelling.

### What a document is

One entity and its belongings, nested, stored and fetched as a unit:

```json
{
  "_id": "post_812",
  "title": "Why B-trees",
  "author": { "id": "u7", "name": "Meena" },
  "tags": ["storage", "trees"],
  "comments": [
    { "user": "u41", "text": "Cleared it up for me", "at": "2026-03-02" }
  ]
}
```

Documents live in **collections** (MongoDB's tables), and unlike rows, two documents in one
collection may have different fields — there is no declared schema. The blog post above is read by
one lookup: the page renders from one document, no joins,
[day 036](../day-036-two-pointers-revision/README.md)'s arranged-for-serving made concrete.

### The one real decision: embed or reference

Every relationship in the model gets one of two treatments, and the whole craft is choosing:

**Embed** — put the data inside the document, like photos in the album. One read serves the page;
the data travels with its owner.

**Reference** — store only an id, like *Rafiq* pointing at the contacts entry. One fact, one home;
readers pay an extra lookup.

The choice is made by three questions, and they are Salim's three lessons in order:

1. **Is it read together with the parent, nearly always?** Read-together data wants embedding —
   that is what the one-read benefit is *for*.
2. **How often does it change, and how many copies would a change touch?** Rafiq's number: changes
   rarely but catastrophically when copied — reference it. The venue address on the day: *should*
   never change — embed it, deliberately, as a snapshot. This is
   [day 029](../day-029-read-write-pointer/README.md)'s snapshot-versus-copy distinction, verbatim:
   a copy that is meant to stay old is a snapshot, not a bug.
3. **Does it grow without limit?** Comments on a viral post, events on a device — unbounded arrays
   fatten the document until reads slow and the 16 MB ceiling nears. Unbounded children get their
   own collection, referenced back — the D'Souza split.

### The hub question, answered in the frame

*A user changes their name.* If the name is embedded in every post and comment for display — the
usual choice, because pages read it constantly — then a rename must **fan out** to every copy: one
update on the `users` document, plus a background pass rewriting the embedded `author.name`
everywhere it appears. The alternatives are honest but different trades: reference-only (every page
pays a lookup to render a byline) or accept staleness until the fan-out completes (what most real
systems do — the rename propagates over minutes, and nobody minds). What fails the interview is
not noticing the copies exist. [Day 029](../day-029-read-write-pointer/README.md)'s law stands:
**every copy needs an owner and a reconciliation path** — here, the `users` document owns the
truth, and the fan-out job is the reconciliation.

---

## 4. The picture

The same blog, both treatments, seams marked:

```
 EMBED (read-optimised)                REFERENCE (change-optimised)

 posts:                                posts:                users:
 {                                     {                     {
   title: "Why B-trees",                 title: "...",         _id: "u7",
   author: {id:"u7",                     author_id: "u7", --->  name: "Meena"
            name:"Meena"},  <- copy      comments: [...]      }
   comments: [ ...500... ],  <- grows  }
   tags: [...]
 }

 page render:  1 read                  page render:  2 reads (post + author)
 rename Meena: 1 + fan-out to          rename Meena: 1 write, done
               every post/comment
 viral post:   document fattens        viral post:   comments in their own
               toward 16 MB                          collection, unbounded
```

**What to notice:** neither column is "correct" — the left is Salim's album, the right is his
contacts app, and a real model uses both at once: embed the read-together and the snapshot-worthy,
reference the shared and the unbounded.

The growth seam, drawn as a timeline:

```
 comments embedded in the post document:

 day 1      [c1]                          4 KB   fine
 month 1    [c1..c120]                   250 KB  fine, reads slowing
 viral      [c1..c48,000]                 15 MB  every read hauls 15 MB;
                                                 next comment nears the
                                                 16 MB hard ceiling -> writes fail

 the split: posts hold a count + the newest 10;
            comments live in their own collection, keyed by post_id
```

**What to notice:** the failure is gradual and then sudden — reads degrade quietly for months, and
the ceiling arrives as a hard write error on your most popular content, which is the worst possible
place to discover a modelling decision.

---

## 5. How it actually works

### MongoDB's machinery, briefly

Documents are stored as **BSON** (binary JSON, with real types — dates, numbers, binary), each
with a unique `_id` serving as its primary key. **Secondary indexes** work on any field, nested
fields and array elements included — B-trees, exactly [day 030](../day-030-fast-and-slow/README.md)'s
and [day 031](../day-031-fixed-window/README.md)'s machinery, so `db.posts.find({"tags": "storage"})`
is an index lookup, not a scan. This is the real distance from yesterday's key-value store: the
store can see inside the value, and you can ask questions you did not pre-key — at
[day 030](../day-030-fast-and-slow/README.md)'s standard price of one more index maintained per
write.

### The atomicity boundary

A write to **one document is atomic**, however deep and complex the update — set a field, push to
an array, increment a counter, all in one operation, all-or-nothing. That single-document guarantee
is the design centre: model so that things which must change together *live* together, and the
everyday writes never need more. Multi-document transactions exist since MongoDB 4.0 —
[day 033](../day-033-window-with-a-map/README.md)'s machinery, opt-in — and they work, at a real
cost in latency and coordination; the grain of the tool, as
[day 036](../day-036-two-pointers-revision/README.md) put it, is to rarely need them. If every
workflow in the domain updates three documents atomically, the domain is telling you it wanted
[day 026](../day-026-strings-revision/README.md)'s tables.

### The limits that shape models

The **16 MB document cap** is a hard error, not a warning. The practical limit arrives earlier:
big documents make every read haul the whole album, and growth forces the storage engine to
relocate and rewrite. Hence the standing rules: **embed the bounded, reference the unbounded**, and
for the middle ground, hybrid patterns — keep the newest ten comments embedded for the first paint,
the full history in its own collection.

### Where the truth lives, and the Postgres question

Two closing placements, both interview-ready. MongoDB replicates (replica sets) and partitions
(sharding by a key) — the distributed machinery arrives properly in a later phase; today's point is
only that the *modelling* discipline is identical at any scale. And the honest rival:
**Postgres JSONB** puts indexed, queryable documents inside the relational store — so "we need
flexible nested records" alone does not justify a second database. The document store earns its
place when the *whole domain* is document-shaped and the one-read-per-page access pattern
dominates; a document-shaped corner of a relational domain is usually a JSONB column.

---

## 6. The numbers

### The read the model buys

```
blog page, relational:  post + author + comments + tags
  4 index lookups (1 query joined, ~1-2 ms; 4 round trips done badly, ~4-8 ms)
blog page, document:    1 lookup, ~0.5-1 ms, one disk page if small

at 2,000 page views/s: the document model does 2,000 reads/s
                       where the naive relational app does 8,000
```

### The rename the model pays

```
Meena's name embedded in 12,000 posts and 90,000 comments:

storage cost of the copies:  ~102,000 × 20 bytes ≈ 2 MB      — irrelevant
rename fan-out:              102,000 document writes
  batched at 5,000 writes/s ≈ 20 seconds of background work  — fine, IF built
  never built               = day 029's Sunday: stale names forever
```

The multiplication to say out loud: **copies × change-rate**, not copies × bytes. Two megabytes is
nothing; 102,000 writes nobody wrote a job for is a data-quality incident.

### The growth arithmetic

```
comments at 2 KB each, embedded:

    100 comments =  200 KB   fine
  1,000 comments =    2 MB   every page view hauls 2 MB — reads hurt
  8,000 comments =   16 MB   writes FAIL with a hard error

an "events" array at 1 KB × 100/day = 36 MB/year: breaches in ~5 months
```

Run this arithmetic at design time for every array in the model: **size × growth rate against
16 MB**, and against "every read carries the whole document" long before that.

### Sizing the store

```
1 million posts × ~20 KB average (text + embedded recent comments) = 20 GB
  -> one node, comfortably; indexes add 10-25% each (day 030's rule holds here)
```

Document stores are rarely chosen for raw size — [day 037](../day-037-prefix-sums/README.md)'s
count-times-size still decides where things fit. They are chosen for the shape of the read.

---

## 7. The trade-offs

### What the model gives up

The mirror of the one-read page, all inherited from
[day 036](../day-036-two-pointers-revision/README.md) and now concrete: **cross-entity queries**
("top commenters this month" walks every post or needs a separate arrangement), **cross-document
invariants** (nothing like a foreign key stops a comment pointing at a deleted post — integrity is
application code now), and **fan-out on shared facts** (every embedded copy is a write you owe on
change). Plus the quiet one: **schema flexibility means schema in the code** — the database will
happily store five generations of document shapes, and every reader carries the if-else archaeology
to handle them. Real teams version their documents (`"schema": 3`) and run migrations anyway.

### When it breaks

The model breaks where relationships stop being tree-shaped. A blog is a tree: post owns comments,
owns tags — documents fit. A marketplace is a web: orders touch products, buyers, sellers,
inventory, payments, and every entity is shared by every other — model that as documents and you
either embed copies of everything (fan-out hell) or reference everything (joins in application
code, without the database's help). **Webs want tables; trees tolerate documents.** That sentence
routes most modelling questions.

### I would not use it if...

**I would not use a document store where money or inventory moves between records** — cross-record
atomicity is the relational deal, and needing the opt-in transactions constantly means the grain is
wrong. **I would not use one for an analytics-heavy domain** — arranged-for-serving is arranged
against ad-hoc questions. **And I would not add MongoDB beside Postgres just for nested data** —
JSONB covers that inside the store that already holds the truth. The document store earns its place
when the domain is genuinely tree-shaped, page reads dominate, and the one-read pattern is worth
owning the fan-out discipline.

### The honest sentence

> Embedding is not a performance trick; it is a *promise* — that this data is read with its parent,
> bounded in growth, and either never changes or has a job that changes every copy. Model documents
> by which promises you can keep.

---

## 8. In the interview

### How it gets asked

- *"Model a blog / e-commerce catalogue / chat app in MongoDB."* — the design form; they are
  watching the embed-versus-reference reasoning, not the field names.
- *"What happens when a user changes their name?"* — the fan-out probe, and the reason this hub
  question exists.
- *"When would you embed and when would you reference?"* — the direct form; answer with the three
  questions.
- *"What are the limits of a document?"* — 16 MB, unbounded arrays, atomicity at the document edge.
- *"MongoDB or Postgres for this domain?"* — tree or web, plus the JSONB escape hatch;
  [day 040](../day-040-2d-prefix-sums/README.md) makes this a full lesson.

### What to say out loud, in the first ninety seconds

1. **Name the unit and its guarantee.** *"A document is one entity and its belongings, read and
   written as a unit — and atomicity is per document, which drives the whole model."*
2. **State the one decision.** *"Every relationship gets embedded or referenced, and I choose with
   three questions: read together? how often does it change, times how many copies? does it grow
   without bound?"*
3. **Model the blog in one breath.** *"Posts embed tags and the author's name for display; comments
   get their own collection — unbounded; the author's truth lives in users — shared."*
4. **Answer the rename before it is asked.** *"A rename updates users, then fans out to the
   embedded display names as a background job — the copy has an owner and a reconciliation path, or
   I don't make the copy."*
5. **Name the ceilings.** *"16 MB hard cap, and reads haul the whole document long before that — so
   bounded things embed, growing things reference."*

### The follow-ups

**"Walk me through the rename fan-out. What breaks, and how do you make it safe?"**
The truth changes in one place — the `users` document — and then 102,000 embedded display names are
stale until rewritten. I would run the fan-out as an idempotent background job: query the indexed
`author.id` fields, rewrite in batches with retries, and record progress so a crash resumes rather
than restarts — [day 018](../day-018-arrays-revision/README.md)'s idempotency arriving in a data
job. Two failure modes to name. Mid-fan-out reads see mixed names — old on some posts, new on
others — which is an eventual-consistency window, acceptable for display names, and I would say so
explicitly rather than let it be discovered. And writes racing the job: a comment created with the
old cached name after the job passed its range — prevented by having creation always read the name
from `users` at write time, never from another embedded copy. If the domain cannot tolerate the
staleness window at all — legal names on invoices — then the name was never embeddable, and that
field becomes a reference or, for the invoice case, a deliberate snapshot that *should not* change:
day 029's distinction deciding the model.

**"How do you handle something needing atomic updates across two documents?"**
First I check whether the model is telling me something: the standard move is to *re-draw the
boundary* so the invariant lives inside one document — if an order and its line items must change
together, the line items belong embedded in the order, and the single-document atomic write covers
it. That redesign answers most cases and is the idiomatic one. Where the invariant genuinely spans
entities — decrement stock and record the order — MongoDB's multi-document transactions exist and
work, with real costs: coordination latency, aborts under contention, and pressure to keep them
short — day 033's rules apply unchanged. If I find them everywhere in the design, the honest
conclusion is that the domain is web-shaped and wants a relational store. And there is the pattern
in between: make one document the record of intent (an order document with a status field) and
drive the side effects from it asynchronously with retries — which is eventual consistency with an
audit trail, the same shape sagas took in day 033.

**"Why not just always reference, like a relational database?"**
Because then the document store is a worse relational database — every page render becomes
application-side joins, without the query planner, join algorithms, or foreign keys that make
joins safe and fast in Postgres; `$lookup` exists but is not the tool's grain. The point of the
document model *is* the locality: the page's read is one document because the things read together
live together. Reference-everything spends that advantage and keeps all the costs — no cross-
document integrity, weaker ad-hoc queries. So all-reference is a smell in both directions: if
everything is referenced, the data is web-shaped and belongs relational; if the model is genuinely
tree-shaped, embedding the read-together, bounded, own-able parts is what buys the one-read page.
The craft is per-relationship, not a global policy — embed the album's photos, reference Rafiq.

### A model answer

> "I'll model the blog as three collections, choosing embed or reference per relationship.
>
> Posts embed what the page reads together and what is bounded: the title, body, tags — a small
> fixed array — and the author's id *plus display name*, a deliberate copy so rendering a page is
> one read. Comments do not embed: they are unbounded — a viral post's comments would fatten the
> document toward the 16 MB cap and make every read haul megabytes — so they get their own
> collection, keyed and indexed by post_id, with maybe the newest ten duplicated into the post for
> first paint. Users own the truth about people.
>
> Now the rename. The user document updates atomically — that is the easy part. The embedded
> display names on every post and comment are now stale: those are copies, and every copy needs an
> owner and a reconciliation path. The owner is the users collection; the reconciliation is an
> idempotent background job that fans the new name out — a hundred thousand embedded copies is
> about twenty seconds of batched writes. Until it finishes, pages show mixed names; for display
> names that eventual consistency is acceptable, and I am saying so out loud rather than letting it
> be discovered. If it weren't acceptable, the name was never embeddable — reference it and pay a
> lookup per render.
>
> Where this model breaks: cross-entity questions — 'top commenters this month' — want a different
> arrangement; nothing enforces that a comment's post exists, so integrity is my application's job;
> and if the domain grew into a marketplace — orders, inventory, payments, everything shared by
> everything — the relationships stop being a tree, and webs want tables. I'd also flag that if
> this blog lived inside an existing Postgres system, JSONB would carry the flexible parts without
> a second database."

---

## 9. Recall card

- **A document = one entity + its belongings, read and written as one unit; atomicity ends at the
  document's edge.** Model so everyday writes never cross it.
- **Embed or reference, by three questions:** read together? change-rate × copies? unbounded
  growth? Bounded + read-together + own-able → embed; shared or growing → reference.
- **The rename answer:** truth in `users`, embedded display names fanned out by an idempotent
  background job — every copy has an owner and a reconciliation path, or the copy is not made.
- **Ceilings:** 16 MB hard cap; reads haul the whole document far sooner. Run size × growth on
  every array at design time.
- **Trees tolerate documents; webs want tables.** And nested data alone justifies JSONB, not a
  second database.
