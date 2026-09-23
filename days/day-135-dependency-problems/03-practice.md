---
day: 135
track: practice
title: "Practice — Course schedule and the dependency family"
status: written
---

# Day 135 · Practice

**DSA topic:** Course schedule and the dependency family
**System design topic:** Search: how a search index actually works

---

## Code these, in this order

One rule for the whole set: **write the two sentences at the top of every file, as a comment.** "A vertex is
___." "An edge from A to B means A must happen before B." Then, before writing the loop, work out by hand on
a two-item example which adjacency list gets the entry. Every problem below can be silently reversed.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Course Schedule | LeetCode 207 (Medium) | Shape 1, and the reversal that is invisible here. |
| 2 | Course Schedule II | LeetCode 210 (Medium) | Shape 2, where the reversal finally becomes visible. |
| 3 | Parallel Courses III | LeetCode 2050 (Hard) | Shape 4 with real durations — the `max` recurrence. |
| 4 | Sequence Reconstruction | LeetCode 444 (Medium) | Shape 5, uniqueness, and building edges from subsequences. |
| 5 | Alien Dictionary | LeetCode 269 (Hard) | Shape 6 — adjacent pairs, first difference, prefix case. |
| 6 | Sort Items by Groups Respecting Dependencies | LeetCode 1203 (Hard) | Two nested sorts. |

### On problems 1 and 2, prove the reversal is invisible

Solve problem 1 with the edges deliberately reversed. Record the answer — it will be correct, because a graph
has a cycle exactly when its reverse does. Then run the same reversed build on problem 2 and check the output
with the property test. Write one sentence on why the bug hid in the first problem and not the second.

### On problem 3, compare levels against the recurrence

Solve it once by counting levels (pretending all durations are equal) and once with
`finish[v] = duration[v] + max(finish of deps)`. Construct an input where they differ by a factor of ten, and
say what property of the input causes the gap.

### On problem 5, write the three rules first

Adjacent pairs only. First difference only. The prefix case. Write them as three comment lines, then solve.
Then break each one on purpose and record what each produces:

1. Compare all pairs — what changes?
2. Take every differing position — find an input where this invents a cycle.
3. Drop the `for ... else` — find the input that now passes and should not.

### On problem 6, name the two graphs

Before coding, write down what the vertices and edges are for the outer sort and for the inner sorts. Then say
what happens if either has a cycle.

### Then the property-test habit

Write this once and reuse it for every problem above:

```python
def is_valid_order(order, edges):
    position = {v: i for i, v in enumerate(order)}
    return all(position[a] < position[b] for a, b in edges)
```

Use it instead of comparing your output to a fixed list. That is the only correct way to test this family.

---

### The recognition drill

1. State the recognition question in one line.
2. Give the two sentences you say before any code.
3. Name the six shapes and give a problem for each.
4. Give the phrasing that signals each shape.
5. Name the three near-misses and what each actually needs.

### The modelling drill

1. State the adjacent-pairs rule and why non-adjacent pairs add nothing.
2. State the first-difference rule and give an input where ignoring it invents a cycle.
3. Give the prefix case and say what must be returned.
4. Describe the two-level pattern and its tell.

### The shapes drill

Write each from memory:

1. Shape 1, the boolean.
2. Shape 2, the order.
3. Shape 3, the smallest order.
4. Shape 4, levels — and then shape 4 with durations.
5. Shape 5, uniqueness.
6. Shape 6, deriving the edges.

### The DAG-DP drill

1. State the principle in one sentence.
2. Say why one pass is enough, referring to the ordering.
3. Give the recurrence for the longest path.
4. Give the recurrence for counting paths.
5. Say why this beats Dijkstra on a DAG, including the negative-weight point.

### The costs drill

1. Give the cost of each of the six shapes.
2. Say which one costs more and by what factor at `V = 100,000`.
3. Give the cost of the alien-dictionary derivation and say what is large and what is small.
4. Say what counting all valid orders costs and give an exploding example.

### The break-it drill

Trigger each and record the exact output or error:

1. Reversed edges on shape 1, then on shape 2.
2. Adjacency built from the pairs, with an isolated vertex.
3. Comparing all pairs, then taking every differing position, on `["abc", "bad"]`.
4. `["abc", "ab"]` with no `for ... else`.
5. Level count used as "minimum time" with one 100-second task among nine 1-second tasks.
6. A recursive DFS version on a 100,000-long chain.

---

### The inversion drill

1. Define a forward index and an inverted index.
2. Say what a postings list is and why it is sorted.
3. Show a two-term query as a merge and give its cost.
4. Say what else a postings entry holds besides the doc id, and what each is for.

### The LIKE drill

1. Say why `LIKE '%x%'` cannot use a B-tree.
2. Compute the scan cost for a million rows of 500 bytes.
3. Compare with an inverted index lookup and give the ratio.
4. Name three things `LIKE` cannot do besides being slow.
5. Say when `LIKE` is actually fine.

### The analysis drill

1. Name the five stages of the pipeline in order.
2. Say what stemming does and give an example of a nonsense stem.
3. State the rule about where the pipeline must run, and what breaks otherwise.
4. Say why stop-word removal is now usually skipped.
5. Say what happens if you stem documents and not queries.

### The ranking drill

1. Give BM25's three ideas in words.
2. Say what "saturation" means and why it matters.
3. Say what you would tune instead of the parameters.
4. Say why ranking is a product problem, with an example.
5. Name four things you would measure to know whether search is working.

### The staleness drill

1. Say why the index can be stale, mechanically.
2. Give Elasticsearch's default refresh interval and what it causes.
3. Give three responses to "I created it and cannot find it".
4. Say what forcing a refresh per document does.
5. Say what you alert on, and why it is not the configured interval.

### The sync drill

1. Name the three sync options and reject one with a reason.
2. Describe the outbox version and what makes it safe.
3. Say what change data capture buys and costs.
4. Say why a reconciliation job is not optional.
5. Say why search should return ids rather than content.

### The numbers drill

1. Compute index size for a million documents at 100 words each, with and without positions.
2. Give the index-size rule of thumb as a percentage of source text.
3. Compare query cost for a rare term and a common term.
4. Explain the rarest-term-first optimisation with the arithmetic.
5. Give indexing throughput for Elasticsearch and for Postgres GIN.
6. Say what memory a large index wants and why.

### The choose-one drill

1. Write the Postgres full-text setup from memory: column, index, query.
2. Say what Postgres gives you that a dedicated engine does not.
3. Give four reasons to move to Elasticsearch, any one sufficient.
4. Say what `pg_trgm` is for and why it is a different tool.
5. Give the document-count rule of thumb.

### The failure drill

For each, say what happens and what you would build:

1. Documents are stemmed and queries are not.
2. A user posts a listing and searches for it half a second later.
3. Someone calls refresh after every indexed document.
4. The indexing consumer dies for six hours.
5. A search returns a listing that was deleted an hour ago.
6. An analyser change is deployed without reindexing.
7. `LIKE '%camera%'` on a table that grew from 5,000 rows to 5,000,000.

Two of the seven produce wrong results with no error at all. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Can all courses be finished? Now give me a valid order.*
   The two modelling sentences, the direction checked by hand, Kahn's with in-degree in domain words,
   `len(order) != n` as the cycle test, and building from the full vertex list — with the phantom-cycle reason.

2. *Here are words in an unknown alphabet. Find the letter order.*
   The three derivation rules stated before any code, why the second one invents cycles when broken, the
   prefix case as the hidden test, and the observation that the input is large and the graph is tiny.

3. *How does full-text search work? Why not just use LIKE?*
   The leading-wildcard scan with numbers, the inversion, the analysis pipeline on both sides, BM25's three
   ideas, and staleness raised before it is asked.

---

## Before you move on

- [ ] I write the two modelling sentences before any code.
- [ ] I check the edge direction by hand on a two-item example.
- [ ] I know why the reversal is invisible on the boolean version.
- [ ] I can name all six shapes and a problem for each.
- [ ] I can name the three near-misses and what each needs.
- [ ] I know the adjacent-pairs and first-difference rules and why each matters.
- [ ] I handle the prefix case with a `for ... else`.
- [ ] I can write the two-level nested sort.
- [ ] I can state the DAG-DP principle and say why one pass suffices.
- [ ] I know levels under-estimate when durations vary.
- [ ] I test with a property check, never a fixed list.
- [ ] I build from the full vertex list, not the pairs.
- [ ] I use Kahn's rather than recursion, and can say why.
- [ ] I can define forward and inverted indexes.
- [ ] I know why postings lists are sorted and what that buys.
- [ ] I can explain why `LIKE '%x%'` cannot use an index.
- [ ] I can compute the scan cost and the index cost and give the ratio.
- [ ] I can name the five analysis stages in order.
- [ ] I know the pipeline must be identical on both sides, and what breaks otherwise.
- [ ] I can give BM25's three ideas in words.
- [ ] I know to tune field boosts rather than parameters.
- [ ] I can name four search metrics worth measuring.
- [ ] I know why the index is stale and what the default interval is.
- [ ] I know the three answers to "I cannot find what I just made".
- [ ] I know what forcing a refresh per document does.
- [ ] I can name the three sync options and reject dual write with a reason.
- [ ] I know why search should return ids and not content.
- [ ] I can size an index as a percentage of source text.
- [ ] I know when Postgres full-text search is the right answer.
- [ ] I answered all three questions above out loud.
