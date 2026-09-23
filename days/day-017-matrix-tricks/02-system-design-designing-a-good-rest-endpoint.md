---
day: 17
track: system-design
title: "Designing a good REST endpoint"
phase: "APIs: how services talk"
status: written
---

# Day 017 · System Design — Designing a good REST endpoint

**After today you can:** You can name a resource, pick the verb, and design a URL the interviewer will not argue with.

**The interviewer asks it as:** *Design the endpoints for a comments feature.*

---

## 1. What this is, and why they ask it

Yesterday was the theory of REST. Today is the craft: given a feature in plain English, produce the
list of endpoints. What are the things? What is each one called? Which method does what to it? What
goes in the request, what comes back, and what happens when it goes wrong?

There are perhaps ten decisions, and they recur in every feature you will ever design. Is this a
new resource or a filter on an existing one? Does it nest under its parent or stand on its own? Is
this an action that deserves a sub-resource? How does the caller ask for page two? What status code
does "already exists" get?

This is asked in almost every design round, and often as its own small exercise before the big one.
It is a good question because it is fast — ten minutes — and it separates people cleanly. Weak
candidates produce `/getComments`, `/addComment`, `/deleteCommentById` and no pagination. Strong
candidates produce a resource model, admit the one place where the resource model does not fit, and
mention pagination before being asked. Nothing about it requires experience at scale, so there is
nowhere to hide.

---

## 2. The story

Farooq has run a hardware shop off the main road in Kanpur for twenty-two years. It is one long
room with shelves to the ceiling on both sides, and there are somewhere near four thousand different
things in it — screws, hinges, taps, wire, brushes, three kinds of glue, a whole shelf of nothing
but door handles.

His nephew Amaan started three weeks ago and can already find almost anything, which surprises
customers.

There is no secret. Every shelf has a number painted on the front edge. Every box on the shelf has
a label, and every label says the same two things in the same order: what the thing is, then its
size. Screws, one inch. Screws, two inch. Hinges, four inch. Amaan learnt three shelves properly in
his first week, and after that he was mostly guessing correctly, because the guesses work — if the
one-inch screws are in the third box on shelf nine, the one-and-a-half-inch ones are next to them,
and you do not need to be told.

Two more habits are worth watching.

When a customer says "give me screws", Amaan never brings the whole box to the counter. He asks two
questions — what size, and how many — and brings a handful. Farooq taught him that on the first day
after he tipped four hundred washers onto the counter for a man who wanted six.

And when a customer asks for something the shop does not keep, Amaan says so straight away. He does
not go to the back, stand there for a minute, and come back with an empty hand and a shrug. He says
"we don't stock that, try the shop past the temple", and the customer is out of the door in ten
seconds instead of two minutes.

There is one thing in that shop that does not fit the system, and Farooq admits it. They sharpen
blades. It is not a thing on a shelf — it is something you do — and there was nowhere to put it, so
it lives behind the counter and every customer has to ask about it, and Amaan had to be told
because he could never have guessed. One exception in four thousand items. Farooq says the trick is
having only the one.

---

## 3. The idea in plain English

Farooq's shelves are an API. Amaan guessing correctly is the whole payoff of good design.

### Find the things first

Before writing a single path, list the **resources** — the things the feature is about. For a
comments feature the list is short:

- a **comment**
- the **post** a comment belongs to
- a **reaction** to a comment (a like)
- a **report** of a comment (a moderation flag)

Notice what is *not* on that list: "getComments", "addComment", "deleteComment". Those are things
you *do*. In REST the doing is carried by the method, so the noun list stays small and stable. A
feature with four resources needs four names, however many operations it ends up supporting.

The naming rules, which are Farooq's labels:

- **Plural, always.** `/comments`, never `/comment`. It reads correctly for both the collection and
  one item: `/comments` and `/comments/91`.
- **Lower case, hyphens for gaps.** `/purchase-orders`, not `/purchaseOrders` or `/purchase_orders`.
- **The same word everywhere.** If it is a comment in one place it is not a "remark" in another.
  Amaan can guess because every label is written the same way.
- **No file extensions and no verbs.** `/comments/91`, not `/comments/91.json` and not
  `/comments/getById/91`.

### Decide what nests and what does not

A comment belongs to a post. That relationship can be expressed two ways, and both are correct:

```
GET /posts/17/comments      # the comments on post 17 — nested
GET /comments?post_id=17    # the same set, as a filter — flat
```

The rule most teams use, and the one to state in an interview: **nest when the child has no
meaning without the parent, and only one level deep.** Comments only exist in the context of a post,
so `/posts/17/comments` is right for listing and creating. But a comment also has its own permanent
identity, so once it exists you address it directly:

```
GET    /comments/91
PATCH  /comments/91
DELETE /comments/91
```

Not `/posts/17/comments/91`. That path carries a fact — which post it belongs to — that the server
already knows from the comment id, and it opens the door to an inconsistent request where post 17
and comment 91 do not match. **List and create under the parent; read, update and delete at the top
level.** That pattern is worth memorising because it answers half the questions in this topic.

And never nest three deep. `/posts/17/comments/91/reactions/4` is a path nobody can remember; make
reactions their own collection at `/reactions/4`.

### Filtering, sorting and paging are not new resources

This is Amaan not bringing the whole box. When the caller wants a subset, it goes in the **query
string** — the part after the `?` — because it is a different *view* of one collection, not a
different collection.

```
GET /posts/17/comments?sort=newest&limit=20&after=cur_8fj2
```

Not `/posts/17/newestComments` and not `/posts/17/comments/top`. Every time you invent a path for
a filter you double the number of endpoints, and none of them can be combined.

**Every collection endpoint must be paginated from the day it is written.** Not later, not when it
gets slow. A comment thread with fifty thousand replies must not be able to return fifty thousand
replies, and a `limit` with a hard maximum enforced by the server is the only thing standing
between you and that. Give it a default too — twenty, say — because callers forget.

### The exception, and having only one of them

Farooq's blade sharpening is the operation that is not a thing. Every real feature has one or two.
For comments it is moderation:

```
POST /comments/91/approve
POST /comments/91/hide
```

Those are verbs in paths, which yesterday's rules forbid. They are also what everybody does,
including well-regarded APIs, because the alternatives are worse — either `PATCH /comments/91` with
`{"status": "hidden"}`, which hides an important state change inside a generic update, or inventing
a `/moderation-actions` resource that exists only to be posted to.

The honest position, and the one to say out loud: **prefer a state change on the resource; use an
action sub-resource when the operation has its own meaning, its own permissions or its own audit
trail; and keep the number of them small.** One exception in four thousand items. The trick is
having only the one.

### Say what comes back, including when it fails

Amaan says "we don't stock that" immediately. An endpoint must do the same, and the way it says so
is the **status code**.

- `200 OK` — here it is.
- `201 Created` — made it, and a `Location` header says where it now lives.
- `204 No Content` — done, nothing to say. The usual answer to `DELETE`.
- `400 Bad Request` — your request is malformed.
- `401 Unauthorized` — I do not know who you are. (`403 Forbidden` — I do, and you may not.)
- `404 Not Found` — no such thing.
- `409 Conflict` — the thing exists but its state forbids this.
- `422 Unprocessable Entity` — well-formed but semantically wrong, such as an empty comment body.
- `429 Too Many Requests` — slow down.

The failure that matters most: **an empty list is not a 404.** `GET /posts/17/comments` on a post
with no comments is `200 OK` with `[]`. The collection exists; it is empty. `404` is for post 17
not existing at all. Getting this wrong is the single most common mistake in API design, and
interviewers ask about it precisely.

---

## 4. The picture

The comments feature, complete:

```
  RESOURCE            METHOD  PATH                              SUCCESS
  ------------------  ------  --------------------------------  ------------------
  list comments       GET     /posts/17/comments?limit=20        200 + page of items
  post a comment      POST    /posts/17/comments                 201 + Location
  read one            GET     /comments/91                       200
  edit one            PATCH   /comments/91                       200
  remove one          DELETE  /comments/91                       204
  replies to one      GET     /comments/91/replies?limit=20      200 + page
  reply to one        POST    /comments/91/replies               201 + Location
  like one            PUT     /reactions/comment/91/me           204   (idempotent)
  unlike one          DELETE  /reactions/comment/91/me           204
  report one          POST    /reports                           201
  hide one (mod)      POST    /comments/91/hide                  200   (the exception)

     nested for LIST and CREATE      |    top-level for READ, UPDATE, DELETE
     ------------------------------  |    -------------------------------
     /posts/17/comments              |    /comments/91
```

**What to notice:** the horizontal line. Everything above it needs the parent to make sense —
"which post's comments?" — and everything below it does not, because a comment id is already
unique. That split is the design, and it is what an interviewer is checking for.

Note also `PUT` on the like. `PUT /reactions/comment/91/me` means *the state of my reaction to
comment 91 is: liked*. Pressing like twice leaves one like, because `PUT` is idempotent. Using
`POST /comments/91/likes` instead would create two likes on a double-tap, which on a mobile network
with retries happens constantly.

The shape of one response, which is as much a part of the design as the path:

```json
{
  "data": [
    {
      "id": "91",
      "post_id": "17",
      "author": { "id": "42", "name": "Amaan", "avatar_url": "https://..." },
      "body": "Second this — the two-inch ones are on shelf nine.",
      "created_at": "2026-08-27T09:14:02Z",
      "edited_at": null,
      "reply_count": 3,
      "reaction_count": 12,
      "viewer_has_reacted": false
    }
  ],
  "paging": {
    "next": "cur_8fj2kd0",
    "has_more": true
  }
}
```

**What to notice:** four decisions are visible here. The list is wrapped in `data` rather than being
a bare array, so `paging` has somewhere to live and so new top-level fields can be added later. The
author is **embedded**, not just an `author_id`, so a client rendering fifty comments does not make
fifty extra calls. `reply_count` is a count, not the replies themselves, so one huge thread cannot
blow up one response. And `viewer_has_reacted` is computed for the caller, which saves every client
from working it out.

---

## 5. How it actually works

### Designing it, in the order you should do it live

**1. Write down the nouns.** Comment, post, reply, reaction, report. Two minutes, and it makes the
rest mechanical.

**2. For each noun, write the collection and the item.** `/comments` and `/comments/{id}`.

**3. Fill in the methods you actually need.** Not all five for everything. Comments are never
replaced wholesale, so there is no `PUT /comments/91` — editing a comment changes the body and
nothing else, so `PATCH`.

**4. Decide nesting.** List and create under the parent, everything else at the top level.

**5. Add the query parameters to every collection.** `limit`, a cursor, `sort`. Then any filters
the feature genuinely needs: `?status=visible`, `?author_id=42`.

**6. Write one example response body.** This is where you decide what is embedded, what is a count,
and what is a link. It is also the step candidates skip, and it is where the interesting questions
live.

**7. List the error cases.** Post does not exist, comment does not exist, empty body, not logged in,
not your comment, too many requests, comment on a locked post.

### Replies: the decision that actually matters

Comment threads nest, and how you model that is the most interesting question in this whole
feature.

**Option A — one level of replies.** A comment can have replies; a reply cannot. This is what
Instagram and YouTube do. Each comment carries a `reply_count`, and `/comments/91/replies` is
paginated separately. It is simple, it is fast, and every response has a bounded size.

**Option B — arbitrary nesting.** A comment has a `parent_id` pointing at another comment. This is
Reddit and Hacker News. Storing it is easy — one nullable column — but reading a whole tree is not,
because fetching depth 12 means twelve round trips to the database unless you do something cleverer.

The something cleverer is a **materialised path**: store, on every comment, the chain of ancestors
as a string like `17/44/91`. Then the whole subtree under comment 44 is every row whose path starts
with `17/44/`, which is one indexed prefix scan. Postgres does this well; there is even a dedicated
`ltree` type for it. The cost is that moving a subtree means rewriting the paths beneath it, which
for comments essentially never happens.

**What to say:** *"I would start with one level of replies, because it bounds every response and
covers most of the product need. If arbitrary nesting is required I would store a parent id plus a
materialised path so a subtree is one prefix query, and I would still cap the rendered depth and
paginate at each level."* That answer shows you know both and have a reason for choosing.

### Pagination, concretely

Offset pagination — `?page=3&per_page=20` — is what everyone writes first, and it has two real
problems on a comment feed. It gets slower with depth, because the database must count past all
skipped rows. And it is unstable: new comments arriving while a user scrolls shift everything down,
so page 2 repeats items from page 1.

Cursor pagination fixes both. The cursor encodes the last item seen — usually `created_at` plus
`id` to break ties — so page two becomes "the twenty comments after this exact point", which is an
indexed lookup at any depth and is unaffected by inserts.

```
GET /posts/17/comments?limit=20
→ { "data": [...], "paging": { "next": "cur_8fj2kd0", "has_more": true } }

GET /posts/17/comments?limit=20&after=cur_8fj2kd0
```

Make the cursor **opaque** — base64 of a small JSON blob — so clients cannot construct one and you
stay free to change what is inside it. Stripe, Slack, GitHub and Twitter all work this way.

### Deleting a comment

Almost never a real delete. A deleted comment in the middle of a thread still has replies hanging
off it, so the row survives with a `deleted_at` timestamp and the API returns a tombstone:

```json
{ "id": "91", "deleted": true, "body": null, "reply_count": 3 }
```

`DELETE /comments/91` still returns `204`, and the caller does not need to know it was a soft
delete. That is encapsulation doing its job. The genuinely hard part is that a legal deletion
request — a takedown, or a privacy request — must really remove the content, so you need both paths.

### Real comment APIs to name

- **Reddit** — `GET /comments/{article}` returns the whole tree with `more` placeholders where it
  truncated, which is a neat, honest answer to unbounded depth.
- **GitHub** — `GET /repos/{owner}/{repo}/issues/{n}/comments`, exactly the nested-for-list pattern,
  with `Link` headers for pagination.
- **Disqus** and **YouTube Data API** — both one level of replies, both cursor-paginated.
- **Slack** — threads are a parent message plus a flat list of replies, again one level.

The convergence is not an accident. Almost every production comment system caps nesting.

---

## 6. The numbers

Take a content site with **10 million daily active users**.

**Write volume.** Suppose 2% of them leave a comment on a given day, and those who do leave 1.5 on
average:

```
10,000,000 × 0.02 × 1.5 = 300,000 comments/day
300,000 ÷ 86,400          ≈ 3.5 writes/second average
peak (say 4×)             ≈ 14 writes/second
```

Fourteen writes a second is nothing. One Postgres instance handles that without noticing. This is
worth saying out loud, because candidates reflexively reach for a queue and a sharded store for
numbers that a single database eats for breakfast.

**Read volume.** Each active user views maybe 8 comment threads a day:

```
10,000,000 × 8 = 80,000,000 reads/day
80,000,000 ÷ 86,400 ≈ 926 reads/second average, ~3,700 at peak
```

**The ratio is the design.** `926 ÷ 3.5 ≈ 265 reads per write`. A 265:1 read-heavy workload says:
cache aggressively, denormalise counts, and do not worry much about write throughput. That single
ratio drives more decisions than any other number in the exercise.

**Storage.** A comment row: id 8 bytes, post id 8, author id 8, parent id 8, timestamps 16, plus
the body. Comment bodies average around 200 bytes.

```
per comment ≈ 250 bytes
per day     = 300,000 × 250 bytes  = 75 MB/day
per year    = 75 MB × 365          ≈ 27 GB/year
```

Twenty-seven gigabytes a year of comment text. That fits on one machine for a decade. The indexes
roughly double it, so call it 55 GB a year, and it is still not a sharding problem. Being able to
say "this does not need sharding, and here is the arithmetic" is a much stronger answer than
proposing a distributed store nobody needs.

**Why pagination is not optional.** A popular post gets 50,000 comments.

```
unpaginated: 50,000 × 250 bytes ≈ 12.5 MB in one response
paginated:        20 × 250 bytes = 5 KB
```

12.5 MB over a mobile connection at 2 Mbps is **fifty seconds**, and the client has to parse all of
it to render the first twenty. The page-size cap is the single most valuable line in the whole
design.

**What caching buys.** With 265 reads per write, the first page of comments on any post is read
enormously more often than it changes. Cache it in Redis for 30 seconds:

```
reads reaching the database = 3,700 × (1 - 0.9) = 370/second
```

A 90% hit rate turns 3,700 reads a second into 370. That is the difference between one database and
four.

---

## 7. The trade-offs

### Nesting the path

Nesting reads beautifully and encodes the relationship, but it hard-codes it. If comments later need
to attach to photos and videos as well as posts, `/posts/17/comments` becomes
`/photos/9/comments` and `/videos/4/comments` — three near-identical endpoints. The flat form,
`/comments?parent_type=post&parent_id=17`, survives that change untouched but reads worse and lets
callers construct combinations you never intended. **I would nest when the parent type is stable and
go flat when the feature is clearly heading towards many parent types.**

### Embedding the author

Embedding the author object saves a round trip per rendered list and is why almost every real API
does it. It also duplicates data in every response — fifty comments by one person carry fifty copies
of their name — and it means a user renaming themselves leaves stale names in every cache. The
alternative, returning only `author_id`, is smaller and always fresh, and it forces every client to
make a second call or maintain its own user cache. **Embed a small subset — id, display name, avatar
URL — and nothing that changes often or matters legally.**

### Counts in the payload

`reply_count` and `reaction_count` are denormalised: they are stored, not computed at read time,
because counting rows on every read at 3,700 reads a second is unaffordable. The price is that they
can drift out of true when an update fails halfway, so they need a periodic reconciliation job. That
is a real cost and it is the right trade at this read-to-write ratio.

### Action sub-resources

`POST /comments/91/hide` is honest about what is happening and gets its own permission check and
audit entry. It is also a verb in a path, and if you allow yourself one you will find twelve within
a year, at which point the API is RPC wearing a REST costume. **Cap it deliberately.**

### Soft delete

Keeping the row keeps the thread readable and makes moderation reversible. It also means "deleted"
data is still in your database, which is a compliance problem the day someone exercises a legal
right to erasure. You need a genuine purge path as well, and you should say so.

### The sentence that separates candidates

> **I would not design it this way if** the comment volume were closer to the read volume, or if
> threads genuinely needed unbounded depth rendered in one shot. At 265 reads per write, caching and
> denormalised counts are obviously right and write throughput is a non-issue. If writes were within
> an order of magnitude of reads — a live chat rather than a comment thread — I would stop treating
> this as a REST collection at all, because polling a paginated endpoint is the wrong shape for
> real-time, and I would move to a websocket stream with the REST endpoints kept only for history.

---

## 8. In the interview

### How it gets asked

- *"Design the endpoints for a comments feature."* — the standard version, often ten minutes before
  a larger design question.
- *"Design the API for a URL shortener / a parking lot / a food delivery app."* — the same exercise
  with different nouns.
- *"Here's an endpoint. What would you change?"* — shown something like
  `POST /api/getCommentsForPost` and asked to critique it.
- *"How would you handle a comment thread with fifty thousand replies?"* — the pagination question,
  asked as a scenario.

### What to say out loud, in the first ninety seconds

1. **Scope it before designing.** *"Quick scope check: one level of replies or arbitrary nesting?
   Are edits allowed? Is there moderation? Do I need reactions?"* Thirty seconds of this prevents
   designing the wrong feature.
2. **List the nouns, out loud, first.** *"The resources are comment, reply, reaction and report. The
   post already exists."* Never start with a path.
3. **State the nesting rule as a rule.** *"I'll nest for list and create, since a comment has no
   meaning without its post, and address individual comments at the top level, since a comment id is
   already unique. So `GET /posts/{id}/comments` and `POST /posts/{id}/comments`, but
   `PATCH /comments/{id}` and `DELETE /comments/{id}`."*
4. **Mention pagination before being asked.** *"Every collection endpoint is paginated from day one,
   with a default limit of twenty and a hard server-side cap. I'd use an opaque cursor rather than
   offsets, because a comment feed has items arriving while you scroll and offsets duplicate rows."*
5. **Sketch one response body.** *"Here's a comment as it comes back — id, embedded author summary,
   body, timestamps, reply count, and whether the viewer has reacted."* This is where the good
   conversation starts.
6. **Name the errors.** *"404 if the post doesn't exist, 200 with an empty array if it exists with no
   comments — those are different. 422 for an empty body, 403 for editing someone else's, 429 on
   rate limit."*
7. **Flag your one exception.** *"Moderation actions like hide and approve are genuinely operations
   rather than things, so I'd give them action sub-resources and keep the number of those small."*

### The follow-ups

**"A post has fifty thousand comments. What happens?"**
Nothing bad, because the endpoint is paginated and the server caps the limit — a caller asking for
`limit=50000` gets twenty, or an error, but never fifty thousand rows. Fifty thousand comments at
about 250 bytes each is 12.5 MB, which is roughly fifty seconds on a 2 Mbps mobile connection and
would have to be fully parsed before the client can render the first screen. With cursor pagination
the first page is 5 KB and arrives immediately, and the cursor makes page 500 exactly as fast as
page 2, which offset pagination cannot do — at that depth the database has to count past a million
rows. I would also cap thread depth in the response and return a "load more replies" cursor per
comment rather than expanding the whole tree.

**"Should replies be a separate endpoint or included in the comment?"**
Separate, with a count included. If replies are embedded, one viral comment makes a single response
unbounded, and you cannot paginate something nested inside a paginated list. So each comment carries
`reply_count`, and `GET /comments/{id}/replies` is its own paginated collection. The cost is an
extra round trip for threads the user actually opens, which is the right trade because most threads
are never opened. If the product needs the first two replies inline — which is what Instagram
does — I would embed exactly two as a `top_replies` array and still keep the paginated endpoint for
the rest. That is a deliberate, bounded exception rather than an open-ended one.

**"What status code for posting a comment on a post that doesn't exist? And on a locked post?"**
`404 Not Found` for the missing post, because the resource in the path does not exist and the
request can never succeed as written. `409 Conflict` for the locked post, because the resource does
exist and the request is well-formed — it is the current *state* that forbids it, and that state can
change. I would not use `400` for either: `400` means the request itself is malformed. And an
important related case — `GET /posts/17/comments` on a post with no comments is `200 OK` with an
empty array, not `404`. The collection exists and is empty. Confusing "empty" with "missing" breaks
every client that reasonably treats `404` as an error.

**"How do you stop someone editing another person's comment?"**
That is `403 Forbidden`, not `404` and not `400`, and the check belongs on the server, never in the
client. `401` means I do not know who you are; `403` means I do and you may not. There is a real
argument for returning `404` instead of `403` when merely knowing the resource exists is itself
sensitive — a private repository, for instance — because a `403` confirms existence. For public
comments that does not apply, so `403` is the honest answer. I would also make the edit a `PATCH`
with only the body field, so an edit cannot accidentally overwrite the author id, and record an
`edited_at` timestamp because clients need to show "edited".

### A model answer

> "Let me scope it first: one level of replies or arbitrary nesting, and is there moderation?
>
> ...One level and yes, moderation. Good.
>
> Then the resources are: comment, reply, reaction, report. The post already exists, so I am adding
> to it rather than designing it.
>
> My nesting rule is that list and create go under the parent, because a comment has no meaning
> without a post, and everything else is top-level, because a comment id is already unique. So:
>
> ```
> GET    /posts/{post_id}/comments?limit=20&after={cursor}&sort=newest   200
> POST   /posts/{post_id}/comments                                       201 + Location
> GET    /comments/{id}                                                  200
> PATCH  /comments/{id}                                                  200
> DELETE /comments/{id}                                                  204
> GET    /comments/{id}/replies?limit=20&after={cursor}                  200
> POST   /comments/{id}/replies                                          201 + Location
> PUT    /reactions/comment/{id}/me                                      204
> DELETE /reactions/comment/{id}/me                                      204
> POST   /reports                                                        201
> ```
>
> Two deliberate choices in there. `PATCH` rather than `PUT` on a comment, because you only ever
> change the body — a `PUT` would imply replacing the whole object, including the author, which
> makes no sense. And `PUT` on the reaction rather than `POST`, because `PUT` is idempotent: a
> double-tap on a flaky mobile connection leaves one like, whereas `POST /likes` would create two.
>
> Every collection is paginated from day one — default limit twenty, hard cap enforced by the
> server, opaque cursor rather than offsets. Cursors matter here specifically because comments arrive
> while the user is scrolling, and offset pagination duplicates rows when that happens; cursors also
> stay fast at depth, where offsets get slower.
>
> A comment comes back with id, an embedded author summary of id, name and avatar so a client
> rendering fifty comments doesn't make fifty extra calls, the body, created and edited timestamps,
> a `reply_count` rather than the replies themselves, and `viewer_has_reacted`. The counts are
> denormalised because the read-to-write ratio here is around 265 to 1 — with 300,000 comments a day
> and 80 million thread views, counting rows on every read is unaffordable, and stale counts are a
> tolerable price with a reconciliation job.
>
> Errors: 404 if the post doesn't exist, but 200 with an empty array if it exists with no comments —
> those are genuinely different. 422 for an empty body, 403 for editing someone else's comment, 409
> for commenting on a locked post, 429 on rate limit.
>
> Deletes are soft, because a deleted comment mid-thread still has replies hanging off it, so the row
> stays with a `deleted_at` and the API returns a tombstone. The endpoint still answers 204 — the
> caller doesn't need to know. I would keep a separate genuine purge path for legal takedowns.
>
> The one place I break the resource model is moderation: `POST /comments/{id}/hide` and
> `/approve`. Those are actions, not things, and forcing them into a `PATCH` would bury a
> significant state change inside a generic update and lose the separate permission check and audit
> trail. I would keep the number of such endpoints deliberately small — that is the exception, and
> the discipline is having only one."

---

## 9. Recall card

- **Nouns first, plural, consistent.** List the resources before writing a single path.
- **Nest for list and create; go top-level for read, update and delete.** Never nest three deep.
- **Filters, sorting and paging go in the query string** — they are views of a collection, not new
  collections.
- **Paginate every collection from day one:** default limit, hard server cap, opaque cursor rather
  than offset.
- **An empty collection is `200` with `[]`, not `404`.** `404` is the parent missing; `409` is the
  state forbidding it; `403` is you may not.
