---
day: 135
track: system-design
title: "Search: how a search index actually works"
phase: "Building blocks of big systems"
status: written
---

# Search: how a search index actually works

## 1. What this is, and why they ask it

Every product has a search box, and almost every one of them starts as `WHERE description LIKE '%camera%'`.
That works until it does not, and when it stops working it stops completely: it cannot use an index, so it
reads every row of the table for every keystroke.

A **search index** turns the question inside out. Instead of storing documents and scanning them for words, it
stores **words** and, for each one, the list of documents containing it. Then "find documents containing
camera" is one lookup instead of a scan. That structure is an **inverted index**, and it is what Elasticsearch,
Lucene, Solr, Postgres full-text search and Google all use.

They ask this because the naive answer is so tempting and so bad, and because the follow-ups have real
substance: how do you handle "cameras" versus "camera", how do you rank the results, how does the index stay
in step with the database, and what do you do when the two disagree. **"Why not just use LIKE?" has a
quantitative answer**, and giving it with numbers is the difference between a good answer and a recited one.

Tomorrow is [Elasticsearch in an architecture](../day-136-dijkstra/README.md) — where the cluster sits and how
it stays fresh. Today is what is inside it.

By the end of this lesson you can explain an inverted index and the analysis pipeline that feeds it, describe
how results are ranked, quantify why `LIKE` does not scale, choose between Postgres full-text search and a
dedicated engine, and name what search gives up in exchange for what it gives you.

---

## 2. The story

The hardware market off Abdul Rehman Street is about four hundred shops in a space you can walk across in ten
minutes, and Ismail sits on a stool near the second entrance with a flask of tea.

He does not sell anything. He has not sold anything since 1998, when he closed his own shop. What he does is
tell people where to go, and he is extremely good at it.

A man came in one morning looking for brass hinges. Not steel — brass, and a particular size, for a cupboard
his father had made.

Ismail did not get up. He said: Farooq, third lane, left side, he will have it. If not, Prakash two doors
after him, but he keeps mostly steel and you will have to ask. And there is a man at the far end near the
water tap who had brass last year but I do not know about now.

Three names, in that order, in about four seconds.

The man went to Farooq and got them.

What is worth understanding is what Ismail did *not* do, which is what everybody else does. A person who does
not know the market walks in and starts at the first shop and asks. Then the second. Then the third. Four
hundred shops, and on a bad day you find the thing at shop two hundred and eleven after three hours, and on a
worse day you give up.

Ismail has spent twenty-seven years building the other list. Not a list of shops and what each one sells —
that is what the shops themselves have, and it is no use to anyone standing at the entrance. His list is the
other way round. **For each thing, who has it.** Brass hinges: Farooq, Prakash, maybe the man near the tap.
Hinges of any kind: about eleven shops. Screws: nearly everybody, so he asks what size before answering.

And the order matters as much as the names. Farooq first because he definitely has them and he is close. The
man near the tap last because it is a long walk and Ismail is not sure. If he read out eleven names in a
random order he would be technically correct and completely useless.

The other thing he does, and he does it without thinking about it, is that it makes no difference whether you
say hinge, hinges, or brass hinge. Same three shops. He is not matching what you said; he is working out what
you meant.

His nephew tried to learn the job in 2016 and lasted about five weeks. He could remember shops. What he could
not do was hold the list the other way round, and he kept walking people to the third lane and back.

---

## 3. The idea in plain English

Ismail's list is an inverted index, and his nephew's failure is the `LIKE` query.

**A forward index is documents to words.** Each shop knows its own stock. Each row in your table has a
description. That is the natural way to store things and it is useless for search, because answering "who has
brass hinges" means asking all four hundred shops.

**An inverted index is words to documents.** For every word, the list of documents containing it. `hinges →
[shop 14, shop 31, shop 208, ...]`. That list is called a **postings list**, and looking one up is a single
dictionary lookup rather than a scan.

**That inversion is the entire idea.** Everything else is refinement.

**A multi-word query is an intersection.** "brass hinges" means fetch the postings list for `brass`, fetch the
one for `hinges`, and intersect them. Postings lists are kept **sorted by document id** precisely so that the
intersection is a linear merge rather than a hash join — walk both lists together, advance whichever is
behind.

**The words in the index are not the words the user typed, and that is the second idea.** Ismail gives the
same answer for "hinge", "hinges" and "brass hinge". The index does this with an **analysis pipeline**, which
runs on the document when it is indexed **and on the query when it is searched** — and it must be the same
pipeline both times, or nothing matches.

The pipeline, in order:

- **Tokenise** — split text into words. Harder than it looks: `wi-fi`, `C++`, `₹1,299`, and languages with no
  spaces all need decisions.
- **Lowercase** — so `Camera` and `camera` are the same term.
- **Remove stop words** — `the`, `and`, `of`. Optional and now usually skipped, because it breaks phrase
  queries like "to be or not to be".
- **Stem or lemmatise** — reduce words to a root, so `running`, `runs` and `ran` all become one term.
  Stemming is a crude rule-based chop (`cameras → camera`); lemmatisation is dictionary-based and slower and
  more correct.
- **Synonyms**, optionally — map `laptop` and `notebook` to the same term.

**Ranking is the third idea, and it is what makes search different from filtering.** A database `WHERE` clause
gives you a set. Search gives you an **ordered** list, and the order is most of the value — Ismail reading
eleven names in a random order would be correct and useless.

The standard ranking function is **BM25**, and its three ideas are worth knowing in words:

- **Term frequency** — a document mentioning "camera" eight times is more about cameras than one mentioning it
  once. But with **diminishing returns**: the eighth mention adds much less than the second.
- **Inverse document frequency** — a word appearing in every document tells you nothing; a rare word is
  highly informative. Matching "hinges" is worth far more than matching "the".
- **Field length normalisation** — a match in a five-word title means more than a match in a two-thousand-word
  description.

**BM25 is TF-IDF with the diminishing returns and length normalisation made explicit**, and it has been the
default in Lucene since 2016. Saying "BM25, which is TF-IDF with saturation and length normalisation" is
enough.

**Now why `LIKE` cannot do this.** `WHERE description LIKE '%camera%'` has a leading wildcard, so no B-tree
index can be used — the index is sorted by the *start* of the string and you are asking about the middle. So
it is a full table scan, comparing every row's text against the pattern. **It also cannot stem, cannot rank,
cannot match multiple words sensibly, and matches inside other words** — "camera" matches "camerawork" and
"scameras".

**And the fourth idea: the index is a separate system, so it can be stale.** The inverted index is not your
database. Something has to keep it in step, and that something is asynchronous, which means there is a window
where the two disagree. **Every search design has to answer "how stale can it be, and what happens when a user
searches for something they just created?"** — and that is [tomorrow's](../day-136-dijkstra/README.md) lesson.

---

## 4. The picture

The inversion, drawn:

```
FORWARD (what the table has)          INVERTED (what search needs)

doc 1: "brass hinges for cupboard"    brass    -> [1, 4]
doc 2: "steel screws box"             hinges   -> [1, 3, 4]
doc 3: "hinges and handles"           cupboard -> [1]
doc 4: "brass hinges heavy duty"      steel    -> [2]
                                      screws   -> [2]
                                      box      -> [2]
"which docs have brass?"              handles  -> [3]
  forward: read all 4 docs            heavy    -> [4]
  inverted: one lookup -> [1, 4]      duty     -> [4]
```

**What to notice.** The forward direction is how the data naturally lives, and answering any query with it
costs a pass over everything. The inverted direction costs a build, once, and then every query is a lookup.

A two-word query as a merge:

```
query: "brass hinges"

brass  -> [1,        4        ]
hinges -> [1,  3,    4        ]
            ^        ^
            |        |
         both lists advance together, sorted by doc id

  i=0: 1 == 1  -> MATCH, advance both
  i=1: 4 vs 3  -> 3 is smaller, advance the hinges pointer
  i=2: 4 == 4  -> MATCH, advance both

result: [1, 4]      cost: O(len(a) + len(b)), not O(a x b)
```

**What to notice.** The lists are sorted by document id, and that is not incidental — it is what makes the
intersection a linear merge with two pointers, the same two-pointer walk you learned on
[day 28](../day-028-opposite-ends/README.md). An unsorted structure would need a hash set and much more
memory.

The analysis pipeline, applied to both sides:

```
DOCUMENT: "Brass Hinges for Cupboards"
  tokenise    -> ["Brass", "Hinges", "for", "Cupboards"]
  lowercase   -> ["brass", "hinges", "for", "cupboards"]
  stop words  -> ["brass", "hinges", "cupboards"]
  stem        -> ["brass", "hing", "cupboard"]
                                         ^
                          indexed under these terms

QUERY: "cupboard hinge"
  tokenise    -> ["cupboard", "hinge"]
  lowercase   -> ["cupboard", "hinge"]
  stem        -> ["cupboard", "hing"]
                                ^
                       MATCHES, because both sides were stemmed

  If the query were NOT stemmed: "hinge" != "hing"  ->  no match at all.
```

**What to notice.** The stemmed forms are not real words — `hing` is nonsense — and that is fine, because
nobody looks at them. **The only requirement is that the same pipeline runs on both sides**, and a mismatch
there produces a search that returns nothing for obviously correct queries, with no error.

And the scan that `LIKE` forces:

```
  1,000,000 rows, average description 500 bytes

  LIKE '%camera%'
    read every row                 1,000,000 rows
    500 MB of text scanned
    at ~1 GB/s                     ~0.5 s per query
    at 100 queries/second          impossible

  inverted index
    lookup "camera"                one dictionary hit
    postings list                  ~2,000 doc ids
    read + rank                    ~2,000 entries
                                   ~1 ms
```

---

## 5. How it actually works

### What a postings list actually holds

Not just document ids. A real postings entry carries enough to rank and to match phrases:

```
term "camera" -> [
    (doc 14, freq 3, positions [2, 47, 91]),
    (doc 31, freq 1, positions [8]),
    (doc 88, freq 7, positions [0, 5, 12, 30, 44, 60, 77]),
    ...
]
```

- **Frequency** feeds the ranking.
- **Positions** are what make **phrase queries** possible: `"brass hinges"` as an exact phrase means finding
  documents where `hinges` appears at position `p + 1` for some position `p` of `brass`. Positions typically
  double or triple the index size, which is why they can be turned off per field.

### Compression, which is why the index is small

Postings lists are the bulk of the index, and two tricks shrink them enormously:

- **Delta encoding.** Store `[14, 31, 88, 91]` as `[14, 17, 57, 3]` — the gaps. Gaps are small numbers even
  when document ids are large.
- **Variable-byte or bit-packed integers.** A gap of 17 needs one byte, not four.

Together these routinely get postings down to **one or two bytes per entry**, which is what makes an index
over hundreds of millions of documents fit on ordinary machines.

### Segments, and why deletes are strange

Lucene — the library under Elasticsearch and Solr — writes **immutable segments**. A batch of documents is
analysed, indexed and written as a self-contained little index, and then never modified.

Consequences worth knowing:

- **A search queries every segment and merges the results.** More segments means slower searches.
- **A background merge process** combines small segments into larger ones.
- **An update is a delete plus an insert.** The old document is marked deleted in a bitmap; the space is only
  reclaimed at the next merge.
- **A document is not searchable until its segment is written.** Elasticsearch calls this the **refresh
  interval**, and it defaults to **one second**. That is the source of "I created it and it does not appear in
  search yet", and it is a setting rather than a bug.

**Immutability is the same idea as the LSM tree you met on [day 31](../day-031-fixed-window/README.md)** —
write-once files plus background compaction — and for the same reason: it makes writes sequential and reads
predictable.

### Ranking, concretely

BM25's shape, without the full formula:

```
score(doc, query) = sum over query terms of:
      IDF(term)                     rare terms are worth more
    x TF saturation                 more mentions help, with diminishing returns
    x length normalisation          shorter fields score higher
```

Two parameters: `k1` controls how fast term frequency saturates (default ~1.2), `b` controls how strongly
length is normalised (default 0.75). **You almost never tune these; you tune field boosts instead** — "a match
in the title is worth three times a match in the body" is a much more effective lever and is what product
teams actually change.

**And relevance is a product problem, not only a technical one.** Real systems layer business rules on top:
boost in-stock items, boost recent content, demote low-rated sellers, personalise by past behaviour. **Saying
that ranking is where the product lives is a strong thing to say**, because a technically perfect BM25 that
ranks out-of-stock items first is a worse product than a crude ranking that does not.

### Postgres full-text search

Postgres has this built in, and for many systems it is the right answer.

```sql
ALTER TABLE products ADD COLUMN search_vector tsvector
    GENERATED ALWAYS AS (
        setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(description, '')), 'B')
    ) STORED;

CREATE INDEX products_search_idx ON products USING GIN (search_vector);

SELECT id, title, ts_rank(search_vector, query) AS rank
FROM products, plainto_tsquery('english', 'brass hinges') query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;
```

`to_tsvector` is the analysis pipeline — tokenise, lowercase, stop words, stem. `GIN` is a genuine inverted
index. `setweight` gives you title-versus-body boosting. `@@` is the match operator.

**What you get:** real search, in your existing database, **transactionally consistent with your data** — no
sync, no staleness, no second system. That last property is worth a great deal and is the main reason to
choose it.

**What you do not get:** distributed scaling beyond one machine, BM25 by default (`ts_rank` is cruder),
built-in fuzzy matching and typo tolerance, faceted aggregations, and the operational tooling of a dedicated
engine.

**The rule of thumb: under a few million documents with modest query rates, Postgres full-text search, and be
glad you have one fewer system.** Beyond that, or when relevance features matter, a dedicated engine.

### Trigram indexes, for the case that is not really search

`pg_trgm` indexes every three-character sequence, which makes `LIKE '%camera%'` and fuzzy matching genuinely
indexable:

```sql
CREATE EXTENSION pg_trgm;
CREATE INDEX ON products USING GIN (title gin_trgm_ops);
-- now LIKE '%camera%' can use an index
```

**This is the right answer for autocomplete on names, for typo tolerance, and for substring matching** — cases
where word-based search is the wrong model. It is not a replacement for full-text search; it is a different
tool that happens to solve the `LIKE` problem specifically.

---

## 6. The numbers

**Why `LIKE` does not scale:**

```
1,000,000 rows, 500 bytes of text each = 500 MB
LIKE '%camera%'  ->  sequential scan of all of it
at ~1 GB/s                          ~500 ms per query
at 10 queries/second                5 CPU-seconds per second -> saturated
```

```
inverted index
lookup                              ~1 dictionary hit
postings list for a common term     ~2% of docs = 20,000 entries
decode + score + top 20             ~20,000 operations
                                    ~2 ms
```

**Two hundred and fifty times faster, and it gets better as the corpus grows**, because the postings list
grows linearly while the scan grows linearly too — but from a base that is already hundreds of times larger.

**Index size:**

```
1,000,000 documents, average 100 words, 20,000 distinct terms

postings entries         1,000,000 x 100 = 100,000,000
                         (each word occurrence is one entry)
raw, 4 bytes per doc id  400 MB
delta + varint encoded   ~1.5 bytes each = 150 MB
with positions           ~2-3x            = 300-450 MB
```

```
original text            1,000,000 x 500 B = 500 MB
index without positions  ~150 MB           = 30% of the source
index with positions     ~400 MB           = 80% of the source
```

**A useful rule: a search index is roughly 20-50% of the source text without positions, and can approach 100%
with them.** If someone says "the index will be tiny", that is the number to correct them with.

**Query cost by term rarity:**

```
rare term ("hinges")      postings list ~2,000 docs     ~0.5 ms
common term ("the")       postings list ~950,000 docs   ~200 ms
```

**Which is exactly why stop words used to be removed** — and why modern engines instead process the *rarest*
term first in a multi-term query, so the intersection shrinks immediately.

```
"the brass hinges"
  start with hinges (2,000)   -> intersect with brass (30,000) -> 400
  start with the (950,000)    -> intersect with brass -> 28,000 -> then hinges -> 400
                                 same answer, 50x more work
```

**Refresh and staleness:**

```
Elasticsearch default refresh interval   1 s
        -> a document is searchable ~1 s after indexing
raising it to 30 s                       fewer segments, faster indexing,
                                         30 s of staleness
```

**Indexing throughput:**

```
Elasticsearch, one node, bulk indexing   10,000 - 50,000 docs/s
Postgres tsvector GIN, single inserts    ~5,000 docs/s
                                         (GIN updates are expensive)
```

**Postgres versus a dedicated engine, sized:**

```
Postgres full-text search
  works well to           ~1-5 million documents
  query latency           5-50 ms
  cost                    zero extra systems

Elasticsearch
  works to                billions, sharded
  query latency           5-50 ms at any size
  cost                    3-node minimum cluster,
                          ~1.5x the source data in RAM for good performance
```

**The RAM figure is the one people miss:** search performance depends heavily on the index being in the page
cache, so a 400 GB index wants a cluster with a comparable amount of memory, and that is the real cost of a
large search deployment.

---

## 7. The trade-offs

**A search index is a second copy of your data, and second copies go stale.** Between the write to the database
and the update to the index there is a window — a second by default, minutes if the pipeline backs up, hours
if it breaks. **Every search design owes an answer to "what does a user see immediately after creating
something?"** and the usual answer is to read that one item from the database directly rather than from search.

**Search is not a transaction.** You cannot index a document and update a row atomically. So the index can
contain deleted items, miss new ones, or hold a stale version. Mitigations are a reconciliation job and
filtering search results against the database before display — and the second one is why search should return
*ids* that you then hydrate from the source of truth.

**Ranking is subjective and never finished.** BM25 is a starting point. Every real system layers business
rules on top, and those rules are a product decision that changes constantly. **A system with no way to
measure relevance cannot improve it**, so click-through rate on results and manually judged query sets are part
of the design, not an afterthought.

**More index features cost storage and indexing time.** Positions for phrase queries double or triple the
index. Trigrams for fuzzy matching multiply it again. Storing every field as both searchable and sortable
doubles it. **Index only what you will query on**, and this is where most bloated search clusters come from.

**A dedicated engine is a distributed system to run.** Three nodes minimum, shard planning, memory sizing,
version upgrades, and a whole class of failure modes. **For under a few million documents, Postgres full-text
search removes all of that and stays transactionally consistent**, which is a genuine advantage rather than a
compromise.

**And `LIKE` is not always wrong.** On a table of a few thousand rows, a sequential scan takes a millisecond
and any index is over-engineering. The failure is not using `LIKE`; it is using it at a million rows and being
surprised.

**When would I not build search at all?** When the user knows exactly what they want and filters would serve
better — a dropdown of categories beats a search box for structured choices. When the corpus is small enough
to scan. And when the real requirement is *lookup by identifier*, where an ordinary index is correct and a
search engine is a strange way to spell `WHERE id = ?`.

---

## 8. In the interview

### How it gets asked

- *"How does full-text search work? Why not just use LIKE?"* — the direct version.
- *"Design search for a product catalogue."*
- *"Why does searching for 'cameras' not find the item titled 'camera'?"* — the analysis question.
- *"How would you rank the results?"*
- *"Elasticsearch or Postgres?"*
- *"A user creates a listing and cannot find it in search. What is happening?"*

### The first ninety seconds

> "`LIKE '%camera%'` has a leading wildcard, so no B-tree index can help — the index is sorted by how strings
> *start* and the query is about the middle. So every query is a full table scan. On a million rows with
> 500-byte descriptions that is 500 MB of text read per query, roughly half a second, and at ten queries a
> second the database is saturated. It also cannot stem, cannot rank, and matches inside other words —
> 'camera' matches 'camerawork'.
>
> The fix is to invert the storage. Instead of documents containing words, store **words containing
> documents**: for each term, a sorted list of the document ids that contain it — a postings list. Then
> 'find documents with camera' is one lookup, and a two-word query is a linear merge of two sorted lists, not
> a scan.
>
> **The second half is the analysis pipeline**, and it is what makes 'cameras' find 'camera'. Tokenise,
> lowercase, optionally drop stop words, and stem to a root form — and crucially, **the same pipeline runs on
> the document at index time and on the query at search time.** If they differ, you get a search that returns
> nothing for obviously correct queries and reports no error.
>
> **The third is ranking, which is what makes it search rather than filtering.** A `WHERE` clause gives a set;
> search gives an ordered list, and the order is most of the value. BM25 is the standard — essentially TF-IDF
> with two refinements: term frequency saturates, so the eighth mention adds much less than the second, and
> matches in shorter fields count for more.
>
> Index size is worth knowing: roughly 20 to 50 percent of the source text without positions, and up to about
> 100 percent with them — positions are what phrase queries need.
>
> **And the thing I would raise before you ask: the index is a second copy, so it can be stale.** Elasticsearch
> refreshes once a second by default, which is where 'I just created it and cannot find it' comes from.
>
> How many documents, and is this Postgres already?"

### The follow-ups

**"Elasticsearch or Postgres full-text search?"**

> "Postgres, unless there is a reason — and I would give the reason rather than treat it as a default.
>
> Postgres has a genuine inverted index: `tsvector` for the analysed form, a GIN index over it, `setweight`
> for field boosting, and `ts_rank` for ranking. A generated column keeps the vector in step with the row
> **inside the same transaction**, which is the big win: no sync pipeline, no staleness, no second system to
> operate, and no window where the index and the data disagree. For a catalogue of a few million products with
> modest query rates, that is the right engineering choice and it removes an entire class of problem.
>
> I would move to Elasticsearch for four reasons, any one of which is sufficient. **Scale** — beyond roughly
> five million documents, or when the index no longer fits comfortably in one machine's memory, because search
> performance is largely about the index being cached. **Relevance features** — proper BM25, typo tolerance,
> synonyms, phrase boosting, learning-to-rank. **Aggregations** — faceted navigation, 'show me counts by
> brand and price band alongside the results', which Postgres can do but not at speed. And **query volume**,
> where I want search traffic off the primary database entirely.
>
> The cost of moving is a three-node cluster, shard planning, memory roughly comparable to the index size, and
> a sync pipeline with all the staleness and reconciliation that implies. **That last one is not a small cost**
> and it is the thing I would weigh hardest."

**"A user creates a listing and cannot find it in search."**

> "Expected, and I would explain it as a design property rather than a bug — then say what I do about it.
>
> Lucene writes immutable segments. A document is not searchable until its segment is written, and
> Elasticsearch's default refresh interval is one second. So there is a floor of about a second, and if the
> indexing pipeline is a queue that has backed up, it can be minutes.
>
> Three responses depending on what the product needs.
>
> **For 'my own listing', do not use search at all.** After creating something, the user's next view should
> read it from the database by id. That is the source of truth, it is instantly consistent, and it removes the
> problem rather than tuning it.
>
> **For 'my listings' lists, read from the database, not the index.** Anything scoped to one user is a
> straightforward indexed query and does not need search.
>
> **For genuinely global search, accept the second and set expectations** — and monitor the actual lag, not the
> configured refresh interval, because the real number is refresh plus queue depth plus indexing time. I would
> alert on the age of the oldest unindexed document, exactly like the consumer lag metric from
> [day 130](../day-130-grids-are-graphs/README.md).
>
> What I would not do is call `refresh` after every write to force it. That creates a segment per document,
> the segment count explodes, merges thrash, and query performance falls off a cliff. It is the fix that makes
> everything worse."

**"How would you rank the results?"**

> "BM25 as the base, then business rules on top, and I would be clear that the second part is where the
> product actually lives.
>
> BM25 in words: rare terms count for more than common ones; more occurrences help but with diminishing
> returns; and a match in a short field counts for more than one in a long field. Two parameters control the
> saturation and the length normalisation, and **I would not tune them** — the effective lever is field
> boosting, saying a title match is worth three or four times a description match, and that is one line of
> configuration with a large effect.
>
> Then the layer that matters commercially. In-stock items above out-of-stock ones. Recent above stale, if
> recency matters in this domain. Highly rated sellers above poor ones. Possibly personalisation from past
> behaviour. **A technically perfect BM25 ranking that puts out-of-stock items first is a worse product than a
> crude ranking that does not**, and I would say that explicitly, because it is the thing engineers
> under-weight.
>
> **And I would insist on measurement**, because relevance cannot be improved without it. Click-through rate on
> the top results, the position of the result the user actually clicked, and the rate of searches with no
> clicks at all — that last one is the best single signal that search is failing. Plus a judged set of maybe
> two hundred queries with hand-marked correct answers, run on every ranking change, so a 'small tweak' cannot
> silently break the common cases."

**"How do you keep the index in sync with the database?"**

> "Three options, and I would pick based on how much staleness is acceptable.
>
> **Dual write** — the application writes to the database and to the index. Simplest, and wrong, because there
> is no transaction across the two: a crash in between leaves them permanently inconsistent, and it will
> happen. I would name it to reject it.
>
> **Outbox plus a consumer.** The application writes the row and an outbox record in the same transaction; a
> consumer reads the outbox and updates the index. That is the pattern from
> [day 121](../day-121-trie-operations/README.md) and it is what I would build: the write is atomic, delivery
> is at-least-once, and indexing is idempotent because it is keyed by document id.
>
> **Change data capture** — read the database's replication log directly with something like Debezium. No
> application changes at all, catches writes from anywhere including manual ones, and it is the more robust
> option at the cost of another moving part.
>
> **And whichever I use, a reconciliation job**, because all three drift. Nightly, compare counts and
> checksums per shard or per id range, and re-index the differences. **This is not optional** — the index will
> drift from the database over months, through failed consumers, replayed events and bugs, and the only way to
> know is to check.
>
> One design detail that makes all of this safer: **search returns ids, and the application hydrates them from
> the database.** Then a stale index shows a slightly wrong *set* of results, but never wrong *content*, and
> deleted items are filtered out at hydration time rather than being served."

### The model answer

*"Design search for a marketplace with 50 million listings. Users search by keywords, filter by category and
price, and sort by relevance or price. New listings must be findable quickly."*

> "Fifty million documents settles the engine question, so let me start there and then spend most of the time
> on the parts that are actually decisions.
>
> **Elasticsearch, not Postgres full-text search.** At fifty million documents the index will be tens of
> gigabytes and wants to be resident in memory for good latency; that is beyond what I want a primary
> transactional database doing, and the faceted filtering — counts by category and price band shown alongside
> results — is something a dedicated engine does well and Postgres does not.
>
> **What goes in the index, and this is where clusters get bloated.** Title and description analysed for
> search. Category, price, location and seller rating as filterable fields. Nothing else. **In particular I
> would not store the full listing body in the index** — search returns listing ids, and the application
> hydrates them from the database. That keeps the index small, and it means a stale index can show a slightly
> wrong result *set* but never wrong *content*, and a deleted listing is filtered out at hydration.
>
> **Analysis:** standard tokenising, lowercase, English stemming, and a synonym list maintained by the product
> team — 'mobile' and 'phone', 'cycle' and 'bicycle'. The same analyser on query and document, and I would put
> a test in CI that asserts a handful of query-document pairs still match, because an analyser change that
> breaks matching produces zero errors and a catastrophe.
>
> **Sharding:** with fifty million documents and growth, maybe ten to twenty shards, sized so each is under
> about 30 GB, which is the range where recovery and merges stay manageable. **Shard count cannot be changed
> without reindexing**, so I would over-provision slightly rather than plan to migrate. Replicas of one for
> availability and read throughput.
>
> **Sync via the outbox pattern.** The listing write and an outbox row in one transaction; a consumer bulk-
> indexes in batches of a few hundred, which is far more efficient than per-document indexing. Refresh interval
> left at one second so new listings are findable in about a second — and I would explicitly not lower it,
> because forcing refreshes per document destroys performance.
>
> **The 'findable quickly' requirement needs a product answer as well as a technical one.** After posting, the
> seller is shown their listing from the database directly, and 'my listings' reads from the database. So the
> one-second window is invisible to the person who cares most about it. That is a better answer than trying to
> make search instantly consistent.
>
> **Ranking:** BM25 with the title boosted about three times over the description, then business rules —
> recency matters a lot in a marketplace, so a decay on listing age; seller rating as a modest boost; and sold
> or expired listings excluded by a filter rather than demoted, because showing them at all is a bad
> experience. Sorting by price is a filter-and-sort, not a relevance query, and I would make sure the UI is
> clear about which mode the user is in, because a price-sorted result set that also applies relevance
> ranking confuses everyone.
>
> **Monitoring:** query latency at p99, the age of the oldest unindexed document from the outbox, the
> zero-result-search rate, and the click-through position. **The zero-result rate is the one I would put in
> front of the product team weekly**, because it is the clearest signal that search is failing users and it is
> usually fixable with synonyms rather than engineering.
>
> **And the reconciliation job**, nightly: compare document counts and a checksum per id range between the
> database and the index, and re-index the differences. Over a year the index *will* drift — a consumer that
> died, a bad deploy, a bulk import that bypassed the outbox — and this is the only mechanism that finds it."

---

## 9. Recall card

**An inverted index maps terms to sorted lists of document ids** (postings), so a query is a lookup and a
multi-word query is a linear merge of sorted lists. `LIKE '%x%'` cannot use a B-tree at all — leading wildcard
— so it scans everything: ~500 ms per query on a million rows against ~2 ms.

**The analysis pipeline must be identical at index time and query time:** tokenise, lowercase, stop words,
stem. A mismatch returns nothing for correct queries, with no error.

**Ranking is what makes it search rather than filtering.** BM25 = rare terms count more (IDF), term frequency
**saturates**, shorter fields count more. Tune field boosts, not the parameters — and layer business rules on
top, because that is where the product is.

**The index is a second copy and it goes stale.** Elasticsearch refreshes ~1 s by default. Sync via the
**outbox** or CDC, never dual write; **search returns ids and you hydrate from the database**; and run a
reconciliation job, because it will drift.

**Postgres full-text search (`tsvector` + GIN) up to a few million documents** — transactionally consistent,
one fewer system. Beyond that, or for facets, typo tolerance and real BM25, a dedicated engine — and budget
memory comparable to the index size.
