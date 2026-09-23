---
day: 142
track: practice
title: "Practice — Graphs revision and mock round"
status: written
---

# Day 142 · Practice

**DSA topic:** Graphs revision and mock round
**System design topic:** Geospatial indexing: geohash and quadtrees

---

## Code these, in this order

This is a closing day, so the rule is different: **write every one of these from an empty file, with the
lesson closed.** If you have to look something up, finish the problem, then write that template out three
times from memory before starting the next one.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Number of Islands | LeetCode 200 (Medium) | Grid as a graph, iterative, mark on push. |
| 2 | Course Schedule II | LeetCode 210 (Medium) | Kahn's, edge direction, build from `range(n)`. |
| 3 | Network Delay Time | LeetCode 743 (Medium) | Dijkstra, `(cost, vertex)`, `max` of the distances. |
| 4 | Accounts Merge | LeetCode 721 (Medium) | The shared-property-as-vertex move. |
| 5 | Most Stones Removed | LeetCode 947 (Medium) | Mock problem 1, timed. |
| 6 | Min Cost to Connect All Points | LeetCode 1584 (Medium) | Mock problem 2's shape — dense Prim's. |

### Run the mock round properly

Twenty minutes each for problems 5 and 6, with a timer, standing up, talking throughout. Then listen back for
three things:

1. Did you say the two modelling sentences before writing anything?
2. Did you give the cost without being asked?
3. When you were stuck, did you keep talking and offer a correct-but-slow fallback?

The third one is what actually fails interviews.

### Then the recognition drill, cold

Ten problem statements, no solving. For each, write the two sentences, the four classification words, and the
algorithm — in under ninety seconds each.

1. "Given a list of dominoes, can they be arranged in a line so touching ends match?"
2. "Given exchange rates, is there a sequence of trades that ends with more than you started?"
3. "Given people and who reports to whom, how long until a message reaches everyone?"
4. "Fewest single-letter changes from one dictionary word to another."
5. "Given a set of tasks with durations and dependencies, when is everything done?"
6. "Given a grid of costs, cheapest path from corner to corner."
7. "Split the students into two classrooms so no two who fight are together."
8. "After each new cable is laid, how many separate networks are there?"
9. "Which cables could be removed without disconnecting anything?"
10. "How far is every house from the nearest fire station?"

Two of the ten are the same problem in different clothes. Say which.

### Then the eight-bugs drill

Write a small graph program and deliberately introduce each of the eight bugs, one at a time. Record the exact
output or error for each. **Five produce no error**, and seeing that yourself is worth more than reading it.

### Then the templates, timed

From an empty file:

1. `build` plus the grid `neighbours` function. Target: two minutes.
2. BFS with distances and parents. Target: three minutes.
3. Three-colour cycle detection. Target: three minutes.
4. Kahn's. Target: three minutes.
5. Dijkstra with lazy deletion. Target: four minutes.
6. Union-Find with both optimisations. Target: four minutes.
7. Kruskal's on top of it. Target: two minutes.

---

### The modelling drill

1. Give the two sentences you say before any code.
2. Give the four classification words and say what each decides.
3. State the recognition question in one line.
4. Recite the tells table: ten phrasings and their algorithms.
5. Name the three modelling moves and give a problem for each.

### The one-shape drill

1. Write the eight-line traversal skeleton from memory.
2. Give the four `TAKE`/`PUSH` substitutions and the algorithm each produces.
3. Say where the mark goes and why.
4. Say what changes to make it multi-source.

### The costs drill

Recite the whole table from memory, then check:

1. BFS, DFS, multi-source, 0-1 BFS, bipartite.
2. Topological sort, and DAG shortest path with any weights.
3. Dijkstra, Bellman-Ford, Floyd-Warshall.
4. Union-Find, Kruskal, both Prims.
5. Then compute all of them on `V = 100,000, E = 300,000`.

### The comparisons drill

1. Multi-source against one-BFS-per-source, with numbers.
2. Traversal against Union-Find for arriving edges, with numbers.
3. Adjacency list against matrix, with numbers.
4. Dijkstra against BFS on an unweighted graph.
5. Say why `E` is the memory and `V` is not.

### The eight-bugs drill

For each: the symptom first, then the fix, then whether it errors.

1. Reversed edge direction.
2. Built from the edge list.
3. One component only.
4. Marked on pop.
5. Undirected edge added once.
6. "Seen" as the cycle test — both flavours.
7. Recursion on a long chain.
8. Missing grid bounds check.

---

### The why-not-a-B-tree drill

1. Say why an index on latitude does not work.
2. Say why a composite `(lat, lng)` index does not fix it.
3. Give rows-examined figures for the naive version and the geohash version.
4. State the general move in one sentence.

### The geohash drill

1. Say how a geohash is constructed.
2. State the prefix property.
3. Give cell sizes for precisions 4 through 8.
4. Say how you choose a precision from a search radius.
5. Say what the query looks like, including the two filters after the cell lookup.

### The boundary drill

1. Explain the boundary problem in two sentences.
2. Give the standard fix and how many lookups it costs.
3. Compute the fraction of query points that need it, for a 500 m radius on precision-6 cells.
4. Say why it is a design error rather than an edge case.
5. Say what H3 does better here, and why.

### The quadtree drill

1. Describe insertion and the capacity parameter.
2. Say what property every leaf has, and why that matters.
3. Say what quadtrees cost that geohashes do not.
4. Give the rule for choosing between them.
5. Size a quadtree for 10M points at capacity 100.

### The alternatives drill

1. Say what S2 does differently and what the Hilbert curve buys.
2. Give H3's two properties and its one compromise.
3. Say what PostGIS uses and what it removes entirely.
4. Say where PostGIS stops being the right answer.
5. Say what Redis GEO is, underneath.

### The numbers drill

1. Compute writes and reads per second for 100,000 drivers reporting every 4 s.
2. Size the Redis memory for that.
3. Give write throughput for Redis GEO and for Postgres with GiST.
4. Give geohash cell width at four different latitudes.
5. Compute candidates and distance calculations for a 9-cell query in a dense city.

### The architecture drill

1. Say why driver locations do not belong in the durable database.
2. Say what the TTL does for you, beyond cleanup.
3. Say what does go to durable storage, and at what volume.
4. Say what the index does and does not decide, on the read path.
5. Say why sharding by city is unusually clean here.

### The failure drill

For each, say what happens and what you would build:

1. A driver twenty metres away is not returned.
2. A precision tuned for Mumbai, used in a rural district.
3. A quadtree under 25,000 location updates a second.
4. A query that returns candidates but skips the exact distance filter.
5. Location updates written to Postgres with a GiST index at 25,000/s.
6. Two riders matched to the same driver.
7. The entire Redis location store is lost.

Two of the seven are working as designed. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Is this a graph problem? What are the vertices and edges?*
   The two sentences, the four words, the recognition question, and the three modelling moves — offered as
   things you check rather than recited.

2. *Why did you choose that algorithm?*
   What is being asked, what the edges look like, whether the graph changes, and the size — in that order,
   with the DAG case named as the one people forget.

3. *How do you find all drivers within two kilometres?*
   Why a B-tree fails, the 2D-to-1D move, geohash prefixes with cell sizes, the boundary problem with its
   70% figure, the exact distance filter, and the write/read asymmetry that decides where the data lives.

---

## Before you move on

- [ ] I say the two modelling sentences before writing any code.
- [ ] I can give the four classification words and what each decides.
- [ ] I can recite the tells table.
- [ ] I can name the three modelling moves with a problem for each.
- [ ] I can write the eight-line skeleton and its four substitutions.
- [ ] I can recite the whole costs table from memory.
- [ ] I can compute every algorithm's cost on a sparse graph.
- [ ] I know multi-source against per-source, with numbers.
- [ ] I know traversal against Union-Find, with numbers.
- [ ] I know `E` is the memory, not `V`.
- [ ] I can name all eight bugs and which five are silent.
- [ ] I wrote all seven templates from an empty file, timed.
- [ ] I ran both mock problems out loud with a clock.
- [ ] I kept talking when I was stuck.
- [ ] I can say why an index on latitude does not work.
- [ ] I can say why a composite index does not fix it.
- [ ] I can explain geohash construction and the prefix property.
- [ ] I know cell sizes for precisions 4 to 8.
- [ ] I can choose a precision from a radius.
- [ ] I can explain the boundary problem and quantify it.
- [ ] I know the nine-cell query is the standard, not a workaround.
- [ ] I can describe a quadtree and its capacity parameter.
- [ ] I know the rule for geohash against quadtree.
- [ ] I know what S2 and H3 fix, and H3's two properties.
- [ ] I know what PostGIS removes and where it stops scaling.
- [ ] I know the index narrows and never answers.
- [ ] I can compute the write/read asymmetry for ride-hailing.
- [ ] I know why live locations are ephemeral and what the TTL buys.
- [ ] I answered all three questions above out loud.
