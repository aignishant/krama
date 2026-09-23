---
day: 162
track: system-design
title: "Design Google Maps"
phase: "High-level design case studies"
status: written
---

# Design Google Maps

## 1. What this is, and why they ask it

Google Maps answers one question — **"how do I get from here to there, and how long will it take?"** — over a
road network with hundreds of millions of intersections, for billions of queries a day, with traffic changing
by the minute.

They ask it because **it is the design where a classic algorithm you know is completely inadequate, and
knowing why is the whole interview.**

**Dijkstra's algorithm solves shortest path correctly.** On a continental road network it visits tens of
millions of nodes and takes seconds. **At the query rate this system needs, that is not off by a constant
factor — it is off by four orders of magnitude.** So the interesting question is not "which algorithm" but
**"what can you compute in advance so the query does almost nothing".**

The answer is preprocessing, and it is the most dramatic example in this course: **hours of offline computation
per continent turning a multi-second query into under a millisecond.** That is the trade to be able to state.

**And traffic is what makes it hard rather than merely large.** A route depends on current conditions, which
change every few minutes, **and the whole point of preprocessing is that it assumes the costs are fixed.**
Reconciling those two is the real design problem, and it has a real answer.

The third thing is **map rendering and tiles**, which is a separate system with different economics —
pre-rendered images at many zoom levels, served like any other static content — and knowing that it is
separate is part of scoping the answer.

By the end of this lesson you can explain why plain Dijkstra fails, describe contraction hierarchies well
enough to defend them, handle live traffic, design the tile pipeline, and size the whole thing.

---

## 2. The story

The transport office issued the permits and the man who actually decided the bus routes was Bhaskaran, who had
done it for twenty-two years and had never seen a map of the district that was correct.

**He was asked the same question forty times a day.** How does this bus get from here to there, and how long.

And for the first few years he did what anybody would do: **he traced it.** Finger on the map, through the
villages, adding up the times, and it took four or five minutes and he got it wrong reasonably often, because
four or five minutes is a long time to hold twenty numbers in your head.

**What changed was the highway.**

Because once the highway existed, **almost every long journey used it.** Not the short ones — a village to the
next village went the small roads. **But anything more than about thirty kilometres got onto the highway as
soon as it could, stayed on it, and came off as late as it could.**

So Bhaskaran stopped tracing the whole route.

**He built one table, over about a month, and it was the highway junctions.** Eleven of them, and for every
pair, the time between them. **Eleven by eleven, one small card pinned above his desk, and it never
changed.**

And then any long question became three small ones. **How do I get from the village to the nearest junction —
which is a short problem I can do in my head. Junction to junction — which is on the card. And the last
junction to the destination — short again.**

**Four or five minutes became about twenty seconds.**

Two things went wrong with it, and both took a while.

**The first was that the short bits were not always short.** A village forty kilometres off the highway had a
long approach, and for those he eventually made a second, smaller card.

**The second was the one he never fully solved.** The card said what the highway took **on an ordinary day**.
It did not know about the market at Perambur on a Thursday, or the level crossing when the goods train was
through, or the road being dug up.

**So he kept the card, and he kept a second thing in his head that changed constantly**, and the answer he
gave was the card adjusted by what he had heard that morning.

His deputy, who wanted the card to be correct, kept asking him to redo it.

**"It took a month," Bhaskaran said. "By the time I finished redoing it, it would be Thursday again."**

---

## 3. The idea in plain English

Bhaskaran's junction table is preprocessing, his three-part journey is the query, and his deputy's question is
the traffic problem — **the table takes a month to build and the world changes on Thursday.**

**Start with what is being asked, because scoping matters here.**

```
IN     routing: from A to B, fastest route
       ETA: how long it will take, given current conditions
       live traffic
       map tiles and rendering
OUT    search and geocoding ("pizza near me"), Street View,
       satellite imagery, business listings, indoor maps,
       turn-by-turn voice, offline maps
```

**Search is its own enormous system** and offering to design it here is how the time disappears.

**Now the graph, and the first number that matters.**

**The road network is a graph.** Nodes are intersections, edges are road segments, and each edge has a cost —
travel time, which is length divided by speed.

**For the whole world that is roughly 100 million nodes and 200 million edges.** For one continent, tens of
millions.

**And here is the failure.** **Dijkstra's algorithm from [day 136](../day-136-dijkstra/README.md) explores
outward from the source in all directions until it reaches the destination.** For a route across a country,
that means visiting a large fraction of the continent's nodes — **tens of millions of them, taking seconds.**

**At billions of queries a day, seconds per query is not a performance problem. It is a different system.**

**Two cheap improvements, neither sufficient:**

**Bidirectional search** runs Dijkstra from both ends and stops when they meet. **It roughly halves the
explored area** — two circles of radius `d/2` instead of one of radius `d` — which at constant factors is
maybe a two-to-fourfold saving. **Real and not enough.**

**A\* adds a heuristic**: prefer nodes that are geometrically closer to the destination, using straight-line
distance as a lower bound on remaining travel time. **On road networks this helps by perhaps five to ten
times** — better, and still milliseconds-to-seconds rather than microseconds.

**Neither gets four orders of magnitude, which is what is needed. So: preprocess.**

**Contraction hierarchies are the standard answer, and the idea is Bhaskaran's junction table.**

**The observation is that road networks have a hierarchy.** Long journeys use motorways; residential streets
only appear at the very beginning and the very end. **So most of the graph is irrelevant to most long
queries.**

**The preprocessing makes that formal.** Order the nodes by "importance" — roughly, how many shortest paths
pass through them — and then **contract them one at a time from least important upwards.**

**Contracting a node means removing it and adding shortcut edges between its neighbours** wherever the path
through it was the only shortest route. **A shortcut says "this stretch of small roads takes eleven minutes"
without storing the small roads.**

**After contracting everything, you have the original graph plus a few million shortcuts, arranged in
levels.**

**And then the query is startlingly simple: bidirectional search, where each direction only ever moves
UPWARDS in the hierarchy.** Forward from the source going up, backward from the destination going up, and the
meeting point is somewhere near the top.

**Because both searches only go up, they touch a few hundred nodes instead of tens of millions.** That is the
four orders of magnitude, and it is why the preprocessing is worth hours per continent.

**Now traffic, which is what makes this genuinely hard.**

**Preprocessing assumes the edge costs are fixed. Traffic changes them every few minutes.** And
**recomputing the hierarchy takes hours**, so you cannot simply rebuild it — Bhaskaran's answer to his
deputy.

**Three techniques, used together.**

**Customisable route planning** splits the preprocessing into two phases: **a slow phase that depends only on
the road *topology*, and a fast phase that depends on the *weights*.** Since traffic changes the weights and
not the topology, **only the fast phase reruns — minutes rather than hours.** That is the main answer and it
is what modern systems do.

**Live traffic as an overlay.** Most edges are unaffected at any moment. **Keep the current speed for the
affected ones in a separate fast store**, and have the query check it for the edges it actually touches. **A
few hundred lookups per query, not millions.**

**And a fallback.** If traffic makes a route much worse than the preprocessed structure assumed, **run a
bounded ordinary search around the affected region.** Slower, rarer, and correct.

**Then: where does the traffic data come from?**

**From the phones.** Anonymised location and speed reports from devices using the app. **Millions of them, a
free and enormous sensor network** — and it is the reason a navigation product improves with the number of
users, which is a genuine competitive property.

**Speeds are aggregated per road segment over a short window**, with outliers removed — a phone in a bus is not
reporting car speed, and a phone in a passenger's pocket in a stationary car is not reporting a jam.

**And there is a privacy requirement that is not optional**: reports must be anonymised and aggregated,
because **a sequence of location reports is a person's movements**, and a segment with only one contributor
identifies them.

**Then the ETA, which is a prediction rather than a sum.**

**Adding up current segment speeds gives the wrong answer for a long journey**, because by the time you reach
a segment forty minutes away, conditions there have changed. **So the ETA uses predicted speeds at the
predicted arrival time** — a model over historical patterns by hour and day, adjusted by current conditions.

**And it should not be a point estimate.** "Twenty-five minutes" is less useful than "twenty-two to thirty-two"
— **and predicting the distribution rather than the mean is a real product decision** that matters most exactly
when traffic is worst.

**Finally, map tiles, which are a different system.**

**The map is not drawn on demand.** The world is divided into square tiles at about twenty zoom levels, **each
tile pre-rendered as an image or as vector data, and served from a CDN like any other static file.**

**The arithmetic is the interesting part**: each zoom level has four times as many tiles as the one above, so
**level 20 has about a trillion tiles.** Rendering all of them is impossible, **so the deep levels are rendered
lazily on first request and cached** — which works because almost nobody zooms all the way in on the middle of
an ocean.

**And vector tiles are the modern choice**: send the geometry and let the client draw it. **Smaller, and one
tile serves every rotation, label language and style**, where raster tiles need a separate render for each.

---

## 4. The picture

Why plain Dijkstra fails:

```
   DIJKSTRA from A to B                A* WITH A HEURISTIC

        . . . . . . .                       . . .
      . . . . . . . . .                   . . . . .
    . . . . A . . . . . .               . . A . . . . .
      . . . . . . . . .                   . . . . . . . B
        . . . . . . .                       . . . . .
            (B is over here)

   explores a CIRCLE around A          explores an ELLIPSE towards B
   radius = distance to B              ~5-10x fewer nodes
   -> tens of millions of nodes
   -> SECONDS per query                -> still milliseconds-to-seconds

   At billions of queries/day, seconds is not slow. It is a
   DIFFERENT SYSTEM. You need four orders of magnitude, and
   neither of these gives it.
```

Contraction hierarchies, which is the junction table:

```
  THE OBSERVATION: road networks are hierarchical

     residential -> arterial -> highway -> motorway

     a 200 km journey uses motorway for 190 km of it.
     the residential streets matter only at the two ENDS.

  PREPROCESSING (hours, offline, per continent)

     order nodes by importance (least important first)
     contract each one: REMOVE it, and add SHORTCUT edges
     between its neighbours where the path through it was the
     only shortest route

        A --3-- X --4-- B         contract X
        =>  A --7-- B             one shortcut replaces two edges
                                  and one node

     after contracting everything: the original graph
     + a few million shortcuts, arranged in LEVELS

  QUERY (microseconds)

     bidirectional search where BOTH directions only move UPWARDS

         source ---up---> \
                           X  meet near the top
     destination ---up---> /

     -> a few HUNDRED nodes touched, not tens of millions
```

The three-part journey, which is Bhaskaran's method:

```
   village ----> nearest junction ----> junction ----> destination
     (small roads)     (THE TABLE)        (small roads)
      ~20 nodes       one lookup          ~20 nodes

   the middle is precomputed and never changes
   the two ends are small and local

   CONTRACTION HIERARCHIES ARE THIS, DONE AUTOMATICALLY
   and with the "junctions" discovered rather than chosen.
```

The traffic problem, and why you cannot just rebuild:

```
   preprocessing assumes FIXED edge costs
   traffic changes costs every ~2 minutes
   rebuilding the hierarchy takes HOURS

   -> you cannot rebuild. Bhaskaran's answer to his deputy.

   THE FIX — split the preprocessing in two:

   PHASE 1 (slow, hours)     depends only on the road TOPOLOGY
                             which roads connect to which
                             -> changes when roads are BUILT,
                                i.e. essentially never

   PHASE 2 (fast, minutes)   depends on the WEIGHTS
                             how long each road takes
                             -> reruns on every traffic update

   traffic changes weights, NOT topology.
   -> only phase 2 reruns. Minutes, not hours.
```

The traffic pipeline:

```
   millions of phones
        |  anonymised (location, speed, heading) every few seconds
        v
   [ INGEST ] --> [ map-match to a road segment ]
                        |  which road is this point actually on?
                        v
                  [ aggregate per segment, 2-min window ]
                        |  median speed, outliers removed
                        |  (a bus is not a car; a parked phone
                        |   is not a jam)
                        v
                  [ live speed store ]  <-- the query reads this
                        |                   for the few hundred
                        v                   edges it touches
                  [ historical archive ] --> ETA prediction models

   PRIVACY IS NOT OPTIONAL: a sequence of location reports IS a
   person's movements. Aggregate, and suppress segments with too
   few contributors.
```

Map tiles, and the arithmetic that shapes them:

```
   zoom 0:  1 tile        the whole world
   zoom 1:  4 tiles
   zoom 2:  16 tiles
   ...
   zoom n:  4^n tiles

   zoom 10:  ~1,000,000 tiles
   zoom 15:  ~1,000,000,000
   zoom 20:  ~1,000,000,000,000 tiles

   -> RENDERING ALL OF THEM IS IMPOSSIBLE

   FIX: pre-render zoom 0-12 (~22 million tiles, feasible),
        render 13-20 LAZILY on first request, then cache

   which works because almost nobody zooms to street level
   in the middle of the Pacific.

   RASTER vs VECTOR tiles:
     raster: a PNG. One render per style, language, rotation.
     vector: the geometry; the client draws it.
             -> smaller, and ONE tile serves every style,
                every label language, every rotation
```

---

## 5. How it actually works

### The graph

```
nodes:  ~100,000,000 worldwide (intersections)
edges:  ~200,000,000 (road segments)

per edge: from_node, to_node, length, road_class, speed_limit,
          turn restrictions, one-way flag
        = ~50 bytes packed

200,000,000 x 50 B = 10 GB for the world's road graph
-> one continent fits comfortably in one machine's memory
```

**Ten gigabytes for every road on Earth** is worth saying, because it reframes the problem: **the graph is not
big data. The query rate is the problem.**

### Contraction, in outline

```python
def contract_node(graph, node) -> list[tuple]:
    """Remove `node`, adding shortcuts only where they are necessary."""
    shortcuts = []
    for u, cost_in in graph.incoming(node):
        for v, cost_out in graph.outgoing(node):
            if u == v:
                continue
            through = cost_in + cost_out
            # is the path u -> node -> v the ONLY shortest route?
            if local_shortest_path(graph, u, v, limit=through) > through:
                shortcuts.append((u, v, through))
    graph.remove(node)
    graph.add_edges(shortcuts)
    return shortcuts
```

**The `local_shortest_path` check is what keeps the number of shortcuts manageable.** Without it every
contraction adds an edge for every pair of neighbours, **and the graph explodes.** With it, a shortcut is added
only when there is no other equally short way round — **and the search is bounded, so it is cheap.**

**The contraction order matters enormously**, and it is chosen by a heuristic — roughly, contract the node
whose removal adds the fewest shortcuts. **A bad order produces ten times as many shortcuts and a much slower
query.**

### The query

```python
def query(graph, source, target):
    """Bidirectional search that only ever moves UPWARDS in the hierarchy."""
    forward = {source: 0}
    backward = {target: 0}
    fq, bq = [(0, source)], [(0, target)]
    best = float("inf")

    while fq or bq:
        for queue, seen, other in ((fq, forward, backward), (bq, backward, forward)):
            if not queue:
                continue
            cost, node = heapq.heappop(queue)
            if node in other:
                best = min(best, cost + other[node])          # they met
            for nxt, weight in graph.upward_edges(node):      # UPWARD only
                if cost + weight < seen.get(nxt, float("inf")):
                    seen[nxt] = cost + weight
                    heapq.heappush(queue, (cost + weight, nxt))
    return best
```

**`graph.upward_edges` is the entire trick.** Each search only follows edges to more important nodes, **so it
climbs rather than spreads** — and the two searches necessarily meet near the top of the hierarchy.

**The correctness argument is the non-obvious part**: because the shortcuts encode every path that was
removed, **an up-only search still finds the true shortest path.** That is what the preprocessing guarantees,
and it is worth saying you know it is a theorem rather than an optimisation.

### Live traffic on top

```python
def edge_cost(edge, departure_time: float) -> float:
    live = traffic_store.get(edge.id)                         # a fast lookup
    if live and live.age < 300:
        return edge.length / live.speed
    predicted = eta_model.speed(edge.id, departure_time)       # historical
    return edge.length / predicted
```

**The query touches a few hundred edges**, so **a few hundred traffic lookups per query is affordable** where
consulting traffic for the whole graph would not be.

**And `live.age < 300` matters**: a five-minute-old reading is useful; a two-hour-old one is worse than the
historical model, **so stale data must fall back rather than be trusted.**

### Ingesting traffic

```python
def ingest_report(device_hash: str, lat: float, lon: float,
                  speed: float, heading: float, at: float) -> None:
    segment = map_match(lat, lon, heading)                    # which road?
    if segment is None:
        return                                                # off-network
    redis.zadd(f"speeds:{segment}", {f"{device_hash}:{at}": speed})
    redis.zremrangebyscore(f"speeds:{segment}", 0, at - 120)   # 2-minute window


def aggregate(segment: str) -> float | None:
    samples = redis.zrange(f"speeds:{segment}", 0, -1, withscores=True)
    if len(samples) < MIN_CONTRIBUTORS:                       # privacy AND accuracy
        return None
    speeds = sorted(s for _, s in samples)
    return speeds[len(speeds) // 2]                           # median, not mean
```

**`map_match` is a real subsystem**, not a lookup: **GPS is accurate to a few metres and roads are metres
apart**, so deciding which road a point is on uses the heading, the recent trajectory and the network topology.
**A phone on a flyover and one on the road beneath it are metres apart and have completely different speeds.**

**The median rather than the mean** is deliberate: one stationary phone in a parked car would drag a mean
towards zero, **and a jam is a median, not an average.**

**And `MIN_CONTRIBUTORS` does two jobs at once** — it suppresses noisy segments **and it is the privacy
guarantee**, because a segment with one contributor is one identifiable person's journey.

### ETA prediction

```python
def predict_eta(route: list, departure: float) -> tuple[float, float]:
    total, time_now = 0.0, departure
    for edge in route:
        speed = eta_model.speed(edge.id, time_now)            # AT ARRIVAL TIME
        seconds = edge.length / speed
        total += seconds
        time_now += seconds                                   # advance the clock
    spread = uncertainty_model.spread(route, departure)
    return total, spread
```

**`time_now += seconds` inside the loop is the important line.** A segment forty minutes into the journey is
evaluated at its *predicted* conditions forty minutes from now, **not at current conditions** — which is the
difference between an ETA that is right and one that is systematically wrong during rush hour.

**And returning a spread rather than a single number** is the honest output: **"twenty-two to thirty-two
minutes" is more useful than "twenty-five"**, and most useful exactly when traffic is worst.

### Tiles

```python
def tile_url(z: int, x: int, y: int) -> str:
    return f"https://tiles.example.com/{z}/{x}/{y}.mvt"


def serve_tile(z: int, x: int, y: int) -> bytes:
    key = f"{z}/{x}/{y}"
    cached = tile_cache.get(key)
    if cached:
        return cached
    if z <= 12:
        return prerendered.get(key)                           # always exists
    data = render_vector_tile(z, x, y)                        # lazy, on demand
    tile_cache.put(key, data, ttl=30 * 86400)
    return data
```

**Zoom 12 and above is the split**, and the reason is arithmetic: **zoom 0 to 12 is about 22 million tiles,
which can be pre-rendered; zoom 20 is a trillion, which cannot.**

**Deep tiles are rendered on first request and cached**, which works because the distribution of requests is
enormously skewed towards places people are.

### The real systems

```
OpenStreetMap     the open road network data everyone else compares to
OSRM              open-source routing with contraction hierarchies
Valhalla          open-source, tiled routing — designed for dynamic costs
GraphHopper       open-source CH and CRP implementations
Mapbox / MapLibre vector tiles and client-side rendering
S2 / H3           the cell systems for spatial indexing (day 161)
Overpass          querying OSM data
```

**Naming OSRM and Valhalla is a good signal**, because they are real implementations of the two approaches —
**OSRM precomputes hard and is fast and static; Valhalla is tiled and designed for costs that change**, which
is exactly the trade this design is about.

---

## 6. The numbers

**The graph.**

```
worldwide:  ~100,000,000 nodes, ~200,000,000 edges
packed:     ~50 bytes per edge

200e6 x 50 B = 10 GB for every road on Earth

one continent (Europe): ~20,000,000 nodes -> ~2 GB
-> FITS IN MEMORY on one machine
```

**Ten gigabytes for the world's roads** — **the data is not the problem, the query rate is.**

**Query cost, which is the whole argument.**

```
DIJKSTRA, London to Edinburgh (~600 km):
  explores a circle of radius 600 km
  ~5,000,000 nodes settled
  at ~10,000,000 node-operations/second in C
  -> ~0.5-2 seconds

A*, same route:
  ~500,000-1,000,000 nodes
  -> ~0.1-0.2 seconds     (5-10x better)

CONTRACTION HIERARCHIES, same route:
  ~500 nodes settled
  -> ~0.1 MILLISECONDS

  10,000x faster than Dijkstra.
```

**Four orders of magnitude is what makes the query rate possible**, and it is the number to lead with.

**The preprocessing that buys it.**

```
contracting a continent (~20,000,000 nodes):
  ~1-4 hours on a large machine
  produces ~1.5x the original edge count in shortcuts
  -> ~2 GB becomes ~3 GB

worldwide: ~10-20 hours, and it is run when the map data changes
           (weekly or so), not when traffic changes
```

**Query load.**

```
~1,000,000,000 route requests/day
= ~11,600/second average
  peak ~40,000/second

at 0.1 ms per query: 40,000 x 0.0001 s = 4 CPU-seconds per second
-> ~4 cores of routing at peak, plus overhead

WITH DIJKSTRA INSTEAD:
  40,000 x 1 s = 40,000 CPU-seconds per second
  -> 40,000 cores. About 1,300 machines, for routing alone.

-> the preprocessing replaces ~1,300 machines with ~10.
```

**That comparison is the best thing to say in this interview**: **hours of offline work per continent against
a thirteen-hundred-machine fleet, forever.**

**Traffic ingestion.**

```
~500,000,000 devices with the app, ~5% moving and reporting at once
= 25,000,000 active reporters
each reports every ~5 seconds
= 5,000,000 reports/second

each report: ~40 bytes
-> 200 MB/s of ingest = ~17 TB/day
```

**Five million reports a second** is the largest write rate in this course, **and it is the same disposable
shape as Uber's location stream** — only the latest matters, losing one is fine.

```
aggregated output:
  200,000,000 segments, but only ~5% have live data at any moment
  = 10,000,000 segments x ~50 bytes = 500 MB of live speed state

-> the live traffic layer fits in memory. Again: the raw stream
   is huge and the useful state is small.
```

**The traffic reprocessing cycle.**

```
full contraction rebuild:     1-4 hours    -> impossible per update
customisable (weights only):  ~2-10 minutes for a continent
                              -> runs every few minutes. Viable.

-> which is exactly why the preprocessing is split into a
   topology phase and a weights phase.
```

**Tiles.**

```
zoom level n has 4^n tiles

  z=12:  16,777,216 tiles
  cumulative z=0..12: ~22,000,000 tiles
  at ~20 KB each (vector): ~440 GB       -> pre-render all of these

  z=20:  ~1.1 x 10^12 tiles
  at 20 KB: ~22 EXABYTES                 -> impossible

-> pre-render to z=12, render z=13-20 lazily and cache
   the request distribution is extremely skewed, so the working
   set is a tiny fraction of the theoretical total
```

**Tile serving.**

```
~10,000,000,000 tile requests/day
= ~116,000/second average, peak ~400,000/second

these are STATIC FILES -> a CDN, exactly like images
at a 98% cache hit rate: ~8,000/second reach the origin

vector tile ~20 KB:
  10e9 x 20 KB = 200 TB/day of egress
  -> comparable to a mid-sized video platform, and it is why
     vector tiles (small) beat raster tiles (large) on cost
```

**Raster against vector, quantified:**

```
raster PNG tile:   ~100 KB, and you need a separate render per
                   style, per label language, per rotation
                   -> 10+ variants of every tile

vector tile:       ~20 KB, and ONE tile serves every style,
                   language and rotation — the client draws it

-> 5x smaller AND 10x fewer variants = ~50x less storage and egress
```

**The full bill, roughly:**

```
tile delivery (200 TB/day)              ~$60M/year
traffic ingest + aggregation            ~$30M/year
routing (small!)                        ~$2M/year
map data + preprocessing                ~$10M/year
                                        --------------
                                        ~$100M/year

-> ROUTING, the algorithmically interesting part, is 2% of the bill.
   The bytes are all tiles and telemetry.
```

---

## 7. The trade-offs

**Preprocessing against flexibility.** Contraction hierarchies give a ten-thousandfold query speedup and
**bake the edge weights in.** Change what "cost" means — avoid motorways, prefer cycle routes, a lorry with a
height limit — **and you need a different hierarchy for each.** Every routing profile is a separate
preprocessing run, which is why products offer four or five profiles and not arbitrary ones.

**Contraction hierarchies against customisable route planning.** CH is faster to query and slower to update.
**CRP splits the work so weight changes cost minutes instead of hours**, at the cost of a somewhat slower query
and a more complex implementation. **For a system with live traffic, CRP wins** — which is why it is what the
production systems moved to.

**Live traffic against predictability.** Using live speeds gives better ETAs and **makes routes unstable** —
the same query a minute apart can return a different road, which is disorienting mid-journey. **So route
changes en route need hysteresis**: only reroute when the saving is meaningfully large, not whenever it is
positive.

**Point ETAs against distributions.** A single number is simple and **systematically overconfident**, and it
is worst when traffic is worst — exactly when the user needs the warning. A range is more honest **and harder
to display and to reason about**, and users have been trained to expect one number.

**Pre-rendered against lazily-rendered tiles.** Pre-rendering everything is impossible past zoom 12 — a
trillion tiles. **Lazy rendering makes the first request for an unusual place slow**, which is acceptable
because unusual places are unusual. **The risk is a cold cache after a style change**, when every tile is
suddenly a miss.

**Raster against vector tiles.** Vector is five times smaller, serves every style and language from one tile,
and **pushes rendering onto the client**, which needs a capable device and more battery. **Raster is
universally supported and multiplies storage by the number of variants.** Vector is the modern default and
raster is the fallback for old clients.

**And the honest one: routing is 2% of the bill.** The algorithmically fascinating part of this system is
cheap; **the money is in tile delivery and telemetry ingest.** That is worth saying, because it is a good
reminder that the interesting engineering and the expensive engineering are often not the same.

**When would I not build this?** **Almost always — this is a build-versus-buy question with an obvious
answer.** The Google Maps and Mapbox APIs exist, the data is the hard part, and **collecting a global road
network is a decade of work.** Self-hosting OSRM or Valhalla on OpenStreetMap data is right when you need a
custom cost function, offline operation, or you are doing millions of routes a day and the API bill dominates.
**And for a single city, or fixed routes, this whole design is unnecessary** — a precomputed table between
every pair of points of interest is a few megabytes.

---

## 8. In the interview

### How it gets asked

- *"Design Google Maps."* — usually meaning routing and ETAs.
- *"Why can't you just use Dijkstra?"* — the central question.
- *"How do you handle live traffic?"* — the one that defeats naive preprocessing.
- *"Where does the traffic data come from?"*
- *"How do you serve the map itself?"* — the tile question.
- *"How would you compute the ETA?"*

### The first ninety seconds

> "I would scope first: **routing, ETAs, live traffic and map tiles are in; search, Street View, satellite
> imagery and business listings are out** — search in particular is its own enormous system.
>
> **The road network is a graph: about a hundred million nodes and two hundred million edges worldwide, which
> packs into around ten gigabytes.** So the data fits in memory on one machine. **The data is not the problem;
> the query rate is.**
>
> **And the central fact is that Dijkstra does not work here — not by a constant factor, by four orders of
> magnitude.** A route from London to Edinburgh explores a circle of six hundred kilometres' radius, settling
> around five million nodes, **which is one to two seconds per query.**
>
> **At a billion route requests a day, that is forty thousand CPU-seconds per second at peak — about thirteen
> hundred machines for routing alone.**
>
> **Bidirectional search roughly halves it and A\* with a straight-line heuristic gives maybe five to ten
> times.** Both real, both nowhere near enough.
>
> **So the answer is preprocessing, and specifically contraction hierarchies.** The observation is that road
> networks are hierarchical — **a two-hundred-kilometre journey uses motorway for a hundred and ninety of it,
> and the residential streets matter only at the two ends.**
>
> **The preprocessing makes that formal:** order the nodes by importance, contract them from least important
> upwards, and **each contraction removes a node and adds shortcut edges wherever the path through it was the
> only shortest route.**
>
> **Then the query is bidirectional search where both directions only ever move upwards in the hierarchy** —
> so they climb rather than spread, and meet near the top. **A few hundred nodes instead of five million:
> about a tenth of a millisecond.**
>
> **Ten thousand times faster, in exchange for a few hours of offline work per continent** — and it turns
> thirteen hundred routing machines into about ten.
>
> **The thing that makes this genuinely hard is traffic**, because preprocessing assumes fixed edge costs and
> **rebuilding the hierarchy takes hours while traffic changes every couple of minutes.** I would want to
> spend most of the time there, if that suits you."

### The follow-ups

**"Why can't you just use Dijkstra?"**

> "Because it is off by four orders of magnitude, and it is worth being precise about where that comes from.
>
> **Dijkstra explores outward from the source in every direction until it reaches the destination.** It has no
> idea where the destination is — **it settles every node closer than the target before it settles the
> target.**
>
> **For London to Edinburgh, that is a circle of six hundred kilometres' radius, which is essentially the whole
> of Britain — around five million nodes.** At ten million node-operations a second in C, that is one to two
> seconds.
>
> **At a billion queries a day with a peak of forty thousand a second, one second per query is forty thousand
> cores.** So this is not a slow implementation, it is the wrong approach.
>
> **Two standard improvements, and I would name both and their limits.**
>
> **Bidirectional search** runs from both ends and stops when they meet — **two circles of radius `d/2` instead
> of one of radius `d`**, which is a factor of two to four in area. **Real, and not enough.**
>
> **A\* with a heuristic** — straight-line distance divided by the maximum speed limit is an admissible lower
> bound — **turns the circle into an ellipse pointed at the destination.** On road networks that is maybe five
> to ten times fewer nodes. **Better, and still milliseconds to seconds.**
>
> **Neither gives ten thousand times, and ten thousand is what is required.**
>
> **So the question changes from 'which algorithm' to 'what can I compute in advance'** — and that is the real
> insight. **Contraction hierarchies spend a few hours offline per continent and reduce a query from five
> million nodes to about five hundred.**
>
> **I would frame the trade explicitly**: a few hours of preprocessing, rerun when the map data changes —
> which is weekly, not minutely — **against a fleet of thirteen hundred machines running forever.** That is not
> a close decision."

**"How do you handle live traffic?"**

> "This is the part that defeats naive preprocessing, and it has a real answer that took the field a while to
> find.
>
> **The problem: contraction hierarchies bake the edge weights into the shortcuts.** A shortcut says 'this
> stretch takes eleven minutes'. **Traffic changes that, and rebuilding the hierarchy takes hours while
> traffic changes every couple of minutes.** You cannot rebuild.
>
> **Three things, used together.**
>
> **The main one is to split the preprocessing into two phases** — customisable route planning.
> **Phase one depends only on the road topology: which roads connect to which.** That changes when roads are
> built, which is essentially never. **Phase two depends on the weights: how long each road takes.**
>
> **Traffic changes weights and not topology**, so only phase two reruns — **minutes for a continent rather
> than hours.** That is what modern production systems do, and it is the answer to the question.
>
> **Second, a live traffic overlay for the fine detail.** At any moment only a few percent of segments have
> unusual conditions. **Keep the current speed for those in a fast store, and have the query check it for the
> edges it actually touches** — a few hundred lookups, which is affordable where consulting the whole graph
> would not be. **And stale readings must fall back to the historical model**, because a two-hour-old speed is
> worse than a good prediction.
>
> **Third, a bounded fallback.** If live conditions make a route much worse than the preprocessed structure
> assumed — an accident closing a motorway — **run an ordinary search over a bounded region around the
> problem.** Slower, rare, and correct.
>
> **And a product point I would raise.** Live traffic makes routes **unstable**: the same query a minute apart
> can give a different road. **Rerouting a driver mid-journey every time a marginally better option appears is
> disorienting**, so route changes need hysteresis — only reroute when the saving is meaningfully large, not
> whenever it is positive."

**"Where does the traffic data come from, and how do you turn it into speeds?"**

> "From the phones, and that is the interesting answer: **the users are the sensor network.**
>
> **Anonymised location, speed and heading reports from devices with the app running.** With five hundred
> million devices and perhaps five percent moving at once, that is twenty-five million reporters at one report
> every five seconds — **about five million reports a second**, roughly seventeen terabytes a day.
>
> **And that is the same disposable shape as any location stream: only the latest matters, and losing one is
> fine.**
>
> **The first real step is map matching, and it is a genuine subsystem rather than a lookup.** GPS is accurate
> to a few metres and roads are metres apart, **so deciding which road a point is on uses the heading, the
> recent trajectory and the network topology.** A phone on a flyover and one on the road beneath it are metres
> apart and have completely different speeds — **getting that wrong reports a jam on a clear road.**
>
> **Then aggregation per segment over a short window, and two choices matter.**
>
> **Use the median, not the mean.** One phone in a parked car reports zero and would drag a mean towards it —
> **a jam is a median, not an average.**
>
> **And require a minimum number of contributors before publishing a speed.** That does two jobs: **it
> suppresses noise on quiet roads, and it is the privacy guarantee** — a segment with one contributor is one
> identifiable person's journey, and a sequence of their reports is their movements.
>
> **Privacy is not optional here** and I would raise it unprompted: **the raw stream is the most sensitive data
> in the entire system**, far more so than anything in the routing layer.
>
> **The output is small, which is the nice part.** Two hundred million segments, but only about five percent
> have live data at any moment — **ten million segments at fifty bytes is five hundred megabytes, which fits
> in memory.** The raw stream is enormous and the useful state is tiny, which is the same pattern as every
> other telemetry system in this course."

### The model answer

*"Design the routing and ETA system for a maps product: a billion route requests a day, global road network,
live traffic."*

> "Let me scope, then give the central fact, because it determines the whole design.
>
> **In: routing, ETA, live traffic. Out: search and geocoding, imagery, business listings** — search is its own
> system.
>
> **The graph is about a hundred million nodes and two hundred million edges, which packs into ten gigabytes.**
> A continent fits in one machine's memory. **The data is not the problem.**
>
> **The central fact: Dijkstra is off by four orders of magnitude.** London to Edinburgh settles about five
> million nodes — one to two seconds. **At a peak of forty thousand queries a second, that is forty thousand
> cores, about thirteen hundred machines for routing alone.** A\* helps by five to ten times and bidirectional
> search by two to four. **Neither is close.**
>
> **So: preprocessing.** Contraction hierarchies exploit the fact that road networks are hierarchical — a long
> journey is almost entirely motorway, with local roads only at the ends. **Order nodes by importance,
> contract from the bottom up, adding shortcuts only where the path through a node was the sole shortest
> route.** Then the query is **bidirectional search that only moves upwards**, touching a few hundred nodes:
> **about a tenth of a millisecond, ten thousand times faster.**
>
> **A few hours of offline work per continent replaces thirteen hundred machines with about ten.**
>
> **Now the hard part: traffic invalidates the preprocessing, and rebuilding takes hours while traffic changes
> every two minutes.**
>
> **The answer is to split the preprocessing.** A slow phase over the road **topology**, which changes when
> roads are built — essentially never. **A fast phase over the weights**, which reruns in minutes when traffic
> updates. **Traffic changes weights, not topology**, so only the fast phase repeats.
>
> **Plus a live overlay** for the few percent of segments with unusual conditions, checked for the few hundred
> edges a query actually touches, **with stale readings falling back to the historical model.** And a bounded
> ordinary search as a fallback when an incident makes the preprocessed structure badly wrong.
>
> **Traffic data comes from the phones** — five million reports a second, seventeen terabytes a day. **Map
> matching first**, which is a real subsystem because GPS accuracy is comparable to the distance between
> roads. **Then median aggregation per segment with a minimum contributor count**, which suppresses noise
> **and is the privacy guarantee** — a segment with one contributor is one person's identifiable journey. **The
> raw stream is the most sensitive data in the system, and I would say so unprompted.**
>
> **ETA is a prediction, not a sum.** Walking the route, each segment is evaluated at its predicted conditions
> **at the time you will actually arrive there**, advancing the clock as you go — a segment forty minutes ahead
> is not evaluated at current conditions. **And I would return a range rather than a point estimate**, because
> a single number is systematically overconfident exactly when traffic is worst.
>
> **Two things I would flag.**
>
> **Routing is about two percent of the bill.** The money is in tile delivery — two hundred terabytes a day —
> and telemetry ingest. **The algorithmically interesting part is the cheap part**, which is worth saying out
> loud.
>
> **And every routing profile needs its own preprocessing.** Avoid motorways, cycling, a lorry with a height
> restriction — **each is a different cost function and therefore a different hierarchy**, which is why
> products offer four or five profiles rather than arbitrary ones. **If the requirement were truly arbitrary
> per-user costs, contraction hierarchies would be the wrong choice**, and I would move to a customisable
> approach with a slower query."

---

## 9. Recall card

**Dijkstra is off by FOUR ORDERS OF MAGNITUDE, not a constant factor.** London→Edinburgh settles ~5,000,000
nodes (1–2 s); at 40,000 queries/second that is ~1,300 machines for routing alone. **Bidirectional gives 2–4×,
A\* gives 5–10× — neither is close.** So the question is not "which algorithm" but **"what can I compute in
advance".**

**Contraction hierarchies: road networks are hierarchical** — a 200 km journey is 190 km of motorway. Order
nodes by importance, **contract from the bottom up, adding a shortcut only where the path through the node was
the sole shortest route** (the bounded local search is what stops the shortcuts exploding). **The query is
bidirectional search that only moves UPWARDS** — ~500 nodes, ~0.1 ms, **10,000× faster for a few hours of
offline work per continent.**

**Traffic defeats naive preprocessing**: weights are baked in, and rebuilding takes hours while traffic changes
every 2 minutes. **Split the preprocessing — a slow TOPOLOGY phase (roads change ~never) and a fast WEIGHTS
phase (minutes)** — because traffic changes weights, not topology. **Plus a live overlay** checked only for the
few hundred edges a query touches, with stale readings falling back to the model.

**Traffic comes from the phones: ~5M reports/second, 17 TB/day.** **Map matching is a real subsystem** — GPS
accuracy is comparable to the gap between a flyover and the road beneath it. **Median, not mean** (a parked
phone is not a jam) and **a minimum contributor count, which is simultaneously the noise filter and the privacy
guarantee.** The raw stream is the most sensitive data in the system.

**ETA is a prediction, not a sum: advance the clock as you walk the route**, so a segment 40 minutes ahead is
evaluated at its predicted conditions then — and **return a range**, since a point estimate is overconfident
exactly when traffic is worst. **Tiles are 4ⁿ per zoom level** — pre-render to z=12 (~22M tiles), render deeper
lazily (z=20 is 10¹² tiles). **Vector tiles are ~50× cheaper than raster** overall. **And routing is ~2% of
the bill** — the money is tiles and telemetry.
