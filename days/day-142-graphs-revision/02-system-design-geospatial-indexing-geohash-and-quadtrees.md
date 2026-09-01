---
day: 142
track: system-design
title: "Geospatial indexing: geohash and quadtrees"
phase: "Building blocks of big systems"
status: written
---

# Geospatial indexing: geohash and quadtrees

## 1. What this is, and why they ask it

"Find every driver within two kilometres of me" sounds like a filter and is not. A `WHERE` clause on latitude
and longitude cannot use an ordinary index, because a B-tree sorts on one dimension and a location is two.
Index the latitude and you narrow a horizontal band across the entire planet; index both and the database
still has to intersect two enormous sets.

The fix is to turn two dimensions into one, in a way that preserves nearness: **give every location a name
such that nearby locations have similar names.** Then "near me" becomes a prefix match or a small set of key
lookups, which a B-tree does very well.

There are two families. **Geohash** interleaves the bits of latitude and longitude into a single string, so a
shared prefix means a shared area. **Quadtrees** recursively split space into four, subdividing only where
things are dense, so a busy city gets fine cells and an empty desert gets one enormous one.

They ask this because it appears in every location design — ride-hailing, food delivery, dating, maps, store
locators — and because the naive answer has a specific failure that you can quantify. **It is also one of the
few areas where the standard solution has a well-known bug** — the boundary problem — and knowing about it is
the difference between reciting a technique and having used one.

By the end of this lesson you can explain why a two-column index fails, describe geohashes and quadtrees and
choose between them, handle the boundary problem, size a real system, and say which parts you would not build
yourself.

---

## 2. The story

Ramnath has delivered in the same three wards for thirty-four years, and the thing that makes the job possible
is that an address narrows.

He gets a sack in the morning and the first thing he does is sort it, and the sorting is not by name or by
street. It is by the number.

The first two digits get him to the region. The next one narrows it further. The last three name one office —
his office. Anything that does not start with those six digits is somebody else's problem and goes back in the
bin at the counter, which takes him about eleven minutes and removes most of the sack.

Then within the ward he sorts by street and by the side of the street, and by ten past eight he is walking.

**The property he relies on without ever having said it out loud is that two addresses with the same first
five digits are almost always close together.** Not always. Almost always. It is enough that he can pick up a
bundle, see that the numbers match, and know without checking that they are all within a few hundred metres of
each other.

He has never had to look at a map. The number *is* the map, in the sense that matters to him.

The one place where it goes wrong, and it has annoyed him for three decades, is Ambedkar Road.

His beat ends at that road. The houses on his side are in his ward. The houses on the other side — and one of
them is forty feet from a house he delivers to every day, close enough that the two families share a wall at
the back where the plots meet — belong to a different office entirely. Their letters go to a sorting point
six kilometres away, get sorted by a different man, and arrive on a different round.

He has stood on that road and been able to see both houses at once. The numbers say they are far apart. They
are forty feet apart.

The other thing about the system, which he thinks is rather clever and which nobody designed on purpose, is
that the areas are not all the same size. His ward is about two square kilometres and has eleven thousand
addresses. His cousin, who delivers in a rural block, has a number that covers something like sixty square
kilometres and about the same number of addresses, because there is nothing in between.

**The numbers do not divide the land evenly. They divide the people evenly**, more or less, which is the thing
that actually matters when you are the one walking.

---

## 3. The idea in plain English

Ramnath's number is a geohash and his cousin's ward is a quadtree, and Ambedkar Road is the boundary problem.

**Start with why the obvious approach fails.** A location is a pair — latitude and longitude — and a B-tree
index sorts on one thing.

```sql
CREATE INDEX ON drivers (lat);
SELECT * FROM drivers WHERE lat BETWEEN 19.05 AND 19.09
                        AND lng BETWEEN 72.85 AND 72.89;
```

The index on `lat` narrows to a **horizontal band around the entire planet** at that latitude, which for a
global system is millions of rows, and then every one of them is checked against the longitude. **A composite
index on `(lat, lng)` does not fix it either**, because a composite index only narrows on the second column
after the first is fixed to a single value — and latitude is a range, not a value.

**So: reduce two dimensions to one, preserving nearness.** That is the whole idea, and both families are ways
of doing it.

**A geohash interleaves the bits.** Take the latitude's bits and the longitude's bits and alternate them —
lat, lng, lat, lng — then encode the result in base 32. The result is a short string like `te7ud`.

**And the property that makes it useful is exactly Ramnath's: a shared prefix means a shared area.** Every
location whose geohash starts with `te7ud` is inside one box on the earth's surface. Longer prefix, smaller
box:

```
1 character   ~5,000 km x 5,000 km
4 characters  ~39 km x 20 km
6 characters  ~1.2 km x 0.6 km
8 characters  ~38 m x 19 m
```

**So "find everything near me" becomes "find everything whose geohash starts with my first six characters"** —
which is a prefix range scan on an ordinary B-tree, and B-trees are extremely good at that. **Two dimensions
became one, and a standard index works.**

**The boundary problem is Ambedkar Road, and it is the thing to raise unprompted.** Two points can be metres
apart and share no prefix at all, because a cell boundary runs between them. A driver twenty metres away,
across the line, is invisible to a pure prefix search.

**The fix is to query the cell and its eight neighbours.** Geohash libraries compute a cell's neighbours
directly, so a search is nine prefix scans rather than one. **That is not a workaround, it is the standard
way to do it**, and a design that does one prefix scan is wrong.

**The second problem is that the boxes are a fixed size and the world is not evenly full.** A six-character
cell in central Mumbai contains thousands of drivers; the same size cell over the Arabian Sea contains none.
Query a fixed precision and you either get a useless number of results or none at all.

**Quadtrees solve that by subdividing only where it is needed.** Start with one box covering everything. When
a box holds more than some number of points — say a hundred — split it into four quadrants and push the points
down. Repeat. **Dense areas end up deeply subdivided and empty areas stay as one large cell**, which is
Ramnath's cousin's enormous rural ward and his own small urban one.

**So the trade is: geohash cells are fixed-size and dead simple to store; quadtree cells are adaptive and need
a real structure that changes as points move.**

**And the third idea, which is what most modern systems actually use: cells on a sphere.** Geohashes are
computed on a flat latitude/longitude rectangle, so cells become badly distorted near the poles and a cell's
"size" varies with where you are. **Google's S2** and **Uber's H3** map the sphere properly — S2 by projecting
onto a cube, H3 by tiling with hexagons — so cells have consistent area, and neighbours behave sensibly.
H3's hexagons have one nice property worth knowing: **every neighbour is the same distance away**, whereas a
square's diagonal neighbours are further than its edge neighbours.

**Whatever the indexing, the last step is always the same: the index narrows, and then you compute real
distances.** A cell is a box, and "within two kilometres" is a circle. So the index gives you a candidate set
of the right order of magnitude, and then you filter it exactly. **The index's job is to avoid scanning
everything, not to give the final answer.**

---

## 4. The picture

Why a two-column index does not work:

```
  index on lat, then filter on lng:

     lng ->
  lat +-------------------------------------------+
   ^  |                                           |
      |###########################################|  <- the lat index gives you
      |###########################################|     THIS BAND, around the
      |###########################################|     whole planet
      |                  +---+                    |
      |                  | X |                    |  <- you wanted this box
      |                  +---+                    |
      +-------------------------------------------+

  millions of rows scanned to find a few hundred.
```

Geohash: interleaving, and the prefix property:

```
  lat bits:      1 0 1 1 0 ...
  lng bits:     0 1 1 0 0 ...
  interleaved:  1 0 0 1 1 1 1 0 0 0 ...     -> base32 -> "te7ud..."

  the tree of cells:

     "t"            one huge box
      |
     "te"           1/32 of it
      |
     "te7"          1/32 again
      |
     "te7u"   "te7v"   "te7w"  ...
      |
     "te7ud"        ~1.2 km x 0.6 km

  shared prefix = shared box.  Longer prefix = smaller box.
```

The boundary problem, drawn:

```
        geohash cell "te7ud"    |    geohash cell "te7uf"
                                |
             A .                |  . B
                                |
                     20 metres apart
                     prefixes share NOTHING useful

   prefix search from A's cell finds A and misses B.

   THE FIX: query the cell AND its 8 neighbours

        +-----+-----+-----+
        | NW  |  N  | NE  |
        +-----+-----+-----+
        |  W  | ME  |  E  |          9 prefix scans instead of 1
        +-----+-----+-----+
        | SW  |  S  | SE  |
        +-----+-----+-----+
```

Quadtree adaptivity, which is the other half:

```
  FIXED GRID (geohash, precision 6)          QUADTREE (capacity 100)

  +----+----+----+----+                      +--------+--------+
  |    |    |####|####|                      |        |  +--+--+
  |    |    |####|####|   <- city            |        |  |##|##|
  +----+----+----+----+                      |        |  +--+--+
  |    |    |####|####|                      | (empty,|  |##|##|
  |    |    |####|####|                      |  ONE   |  +--+--+
  +----+----+----+----+                      |  cell) |        |
  |    |    |    |    |   <- sea             +--------+--------+
  |    |    |    |    |                      |        |        |
  +----+----+----+----+                      |        |        |
                                             +--------+--------+
  every cell the same size:                  cells sized by DENSITY:
  4 cells with 3,000 each                    the city is subdivided 4 more
  12 cells with 0                            levels; the sea is one cell
```

**What to notice.** The geohash grid does the same amount of dividing everywhere, so a query in the city
returns thousands and a query at sea returns nothing. The quadtree divides where the points are, so **every
leaf holds roughly the same number of points** — which is Ramnath's cousin's sixty square kilometres with the
same number of addresses as Ramnath's two.

---

## 5. How it actually works

### Geohash, concretely

```python
import geohash                              # python-geohash, or pygeohash

h = geohash.encode(19.0760, 72.8777, precision=6)     # -> 'te7ud5'
lat, lng = geohash.decode(h)
neighbours = geohash.neighbors(h)                     # the 8 surrounding cells
```

Storage is a plain indexed column:

```sql
CREATE TABLE driver_locations (
    driver_id  BIGINT PRIMARY KEY,
    lat        DOUBLE PRECISION NOT NULL,
    lng        DOUBLE PRECISION NOT NULL,
    geohash6   TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX ON driver_locations (geohash6);
```

And the query is the nine-cell scan, then an exact filter:

```sql
SELECT driver_id, lat, lng
FROM driver_locations
WHERE geohash6 IN ('te7ud5','te7ud4','te7ud6','te7ud7','te7udh', ...)   -- 9 cells
  AND updated_at > now() - interval '1 minute'
  AND earth_distance(ll_to_earth(lat, lng), ll_to_earth(:lat, :lng)) < 2000
ORDER BY earth_distance(...) LIMIT 20;
```

**Three things in that query matter.** The nine cells, not one. The freshness filter, because a driver's
location from an hour ago is not a driver. And the exact distance calculation at the end, because a cell is a
box and the requirement is a circle.

**Choosing the precision is the design decision**, and it comes from the radius you want:

```
radius 500 m   -> precision 7 (~150 m cells), 9 cells covers ~450 m
radius 2 km    -> precision 6 (~1.2 km cells), 9 cells covers ~3.6 km
radius 10 km   -> precision 5 (~5 km cells)
```

**Pick the precision so that nine cells comfortably cover the radius**, then filter exactly. Too fine and you
need far more than nine cells; too coarse and you scan a huge candidate set.

### Redis GEO, which is what many systems actually use

Redis has this built in, and it is a sorted set with geohash values as scores:

```
GEOADD drivers 72.8777 19.0760 driver:8814
GEOSEARCH drivers FROMLONLAT 72.8777 19.0760 BYRADIUS 2 km ASC COUNT 20
```

`O(log n + m)` per query, in memory, with the boundary handling and the distance maths done for you.
**For live location on a fleet of moderate size this is the whole answer**, and reaching past it needs a
reason — usually scale, durability, or wanting the data queryable alongside other columns.

### Quadtrees

```
insert(point):
    find the leaf containing it
    add the point
    if the leaf now holds more than CAPACITY:
        split into 4 children
        redistribute the points

query(circle):
    start at the root
    for each child whose box INTERSECTS the circle:
        recurse
    at leaves, test each point exactly
```

**The `capacity` is the tuning knob** — usually a few tens to a few hundred. Small capacity means a deeper
tree and more nodes; large capacity means more points to filter at each leaf.

**What quadtrees cost you is mutation.** A ride-hailing system updates every driver's location every few
seconds; every update potentially removes a point from one leaf, inserts into another, and may trigger a split
or a merge. **That is real work and it needs locking**, which is exactly what geohashes avoid — updating a
geohash is writing one string.

**So the honest rule: quadtrees for relatively static data with wildly uneven density** — points of interest,
shops, property listings. **Geohash or S2/H3 for high-churn moving objects.**

### S2 and H3

**S2** (Google) projects the sphere onto the six faces of a cube and uses a Hilbert curve within each face, so
that nearby cells have nearby 64-bit ids. Thirty levels of subdivision, from the whole earth down to about a
square centimetre. **The Hilbert curve preserves locality better than geohash's simple interleaving**, which
reduces — though does not eliminate — the boundary problem.

**H3** (Uber) tiles the sphere with **hexagons**. Two properties matter:

- **All six neighbours are equidistant** from a cell's centre, unlike a square where diagonal neighbours are
  1.41 times as far. That makes "expand the search by one ring" behave uniformly.
- **Cells are close to equal area** across the globe, which geohash cells are not — a geohash cell at 60°
  latitude is about half the width of one at the equator.

Hexagons cannot tile perfectly at every level, so H3's hierarchy is approximate rather than exact — a child is
not exactly one seventh of its parent. **That is the trade, and it rarely matters in practice.**

### PostGIS and R-trees

```sql
CREATE EXTENSION postgis;
ALTER TABLE places ADD COLUMN geom geography(Point, 4326);
CREATE INDEX ON places USING GIST (geom);

SELECT * FROM places
WHERE ST_DWithin(geom, ST_MakePoint(:lng, :lat)::geography, 2000)
ORDER BY geom <-> ST_MakePoint(:lng, :lat)::geography
LIMIT 20;
```

PostGIS uses an **R-tree** (via GiST): a tree of bounding rectangles, where each node's rectangle contains its
children's. It handles points, lines and polygons, does real spherical distance, and there is **no boundary
problem and no cell-size tuning** — the index is genuinely two-dimensional rather than a projection to one.

**For anything already in Postgres and not at extreme write rates, this is the right answer**, and reaching
for a hand-rolled geohash scheme instead is usually a mistake. Where it stops being right is very high write
volume — R-tree updates are more expensive than writing a string — and horizontal scale.

### The read/write asymmetry, which shapes the architecture

```
ride-hailing:
  writes   every driver, every 4 seconds       -> enormous, tiny, and disposable
  reads    every rider request                 -> fewer, and must be fast
```

**Driver locations are ephemeral and do not belong in the durable database at all.** Redis with a TTL, or an
in-memory service, and the source of truth is "wherever the driver last reported". Losing the whole store
means every driver re-reports within four seconds. **Recognising that the write-heavy part needs no durability
is the main architectural insight in these designs.**

---

## 6. The numbers

**Why the naive query fails:**

```
1,000,000 drivers worldwide
index on lat, band of 0.04 degrees (~4.4 km)
  fraction of the planet's latitude range covered   0.04 / 180 = 0.02%
  but drivers are NOT uniform: in a city, that band
  crosses many dense areas globally
  realistic rows examined                           50,000 - 200,000
  then filtered on lng to                           ~200
```

```
with a geohash-6 index:
  9 cells x ~1.2 km each
  drivers in ~3.6 km^2 of a dense city               ~500
  exact distance filter                              -> ~200
                                                     -> 250x fewer rows
```

**Geohash cell sizes, worth memorising roughly:**

```
precision   width x height (at the equator)
    4       39 km   x 20 km
    5        5 km   x 5 km
    6        1.2 km x 0.6 km
    7      153 m    x 153 m
    8       38 m    x 19 m
```

**Sizing a ride-hailing system.** 100,000 active drivers in a city, reporting every 4 seconds:

```
writes    100,000 / 4 s                = 25,000 writes/second
each      driver_id + lat + lng + time = ~50 bytes
                                       = 1.25 MB/s
```

```
reads     50,000 ride requests/hour peak = ~14/second
          each: 9 cell lookups + distance filter on ~500 candidates
```

**Twenty-five thousand writes a second against fourteen reads.** That asymmetry is the whole design: **the
write path must be cheap and the data must be disposable.**

```
Redis GEOADD                    ~100,000 ops/s per instance  -> comfortable
Postgres with a GiST index      ~5,000-20,000 writes/s       -> needs sharding
```

**Memory for the live set:**

```
100,000 drivers x ~100 bytes in a Redis sorted set   = 10 MB
1,000,000 drivers                                    = 100 MB
```

**Trivial**, which is the other reason this lives in memory.

**Quadtree sizing** for 10 million static points of interest, capacity 100:

```
leaves          10,000,000 / 100      = 100,000 leaves
internal nodes  ~ leaves / 3          = ~33,000
total nodes     ~133,000
per node        ~100 bytes            = ~13 MB of structure
depth           log4(100,000)         = ~8 levels
query           8 node hops + ~100 point tests
```

**Query cost, compared:**

```
full scan, 10M points                  10,000,000 distance calculations
geohash, 9 cells                       ~500 candidates + 500 distance calcs
quadtree                               ~8 hops + ~100-400 distance calcs
PostGIS GiST                           ~log(n) index descent + candidates
```

**The exact-distance step is not free and is often forgotten** in estimates: 500 haversine calculations is
about 50 microseconds, which is fine, and 50,000 would not be.

**Boundary problem, quantified:**

```
precision-6 cell: 1.2 km x 0.6 km, perimeter ~3.6 km
search radius 500 m
fraction of a cell's area within 500 m of an edge:  ~70%

-> for a MAJORITY of query points, the answer requires neighbouring cells
```

**That is why nine cells is the standard and one cell is a bug** — it is not a rare edge case, it is most
queries.

**Cell distortion by latitude**, which is the argument for S2 and H3:

```
geohash precision 6, cell width
  at the equator (0 deg)        1.2 km
  at Mumbai (19 deg)            1.1 km
  at London (51 deg)            0.75 km
  at Reykjavik (64 deg)         0.53 km

-> the same precision means different real areas
-> a fixed precision tuned for one city is wrong in another
```

---

## 7. The trade-offs

**Geohash is simple and its cells are fixed.** One indexed string column, ordinary B-tree, works in any
database, trivially shardable by prefix. What you give up: cells do not adapt to density, so a precision
tuned for Mumbai returns nothing useful in a rural area and thousands in a city centre; cells are distorted by
latitude; and **the boundary problem means every query is nine lookups rather than one.**

**Quadtrees adapt to density and cost you mutation.** Every leaf holds a similar number of points regardless
of how crowded the area is, which makes query cost predictable. In exchange, moving a point may trigger a
split or a merge, the structure needs locking under concurrent updates, and it is a real data structure to
implement and operate rather than a string. **Static-ish data with uneven density: quadtree. Constantly moving
objects: not a quadtree.**

**S2 and H3 fix the geometry and add a dependency.** Proper spherical cells, consistent areas, better locality
from the Hilbert curve, and H3's equidistant neighbours. The cost is a library and a set of concepts your team
has to learn, and ids that are opaque 64-bit integers rather than human-readable strings.

**PostGIS is the least work and the least scalable.** A real two-dimensional index, no boundary problem, no
cell tuning, exact spherical distances, and polygons and lines as well as points. It tops out on write
throughput far earlier than a Redis-based approach, and scaling it horizontally is a project.

**Precision is a permanent trade.** Finer cells mean a smaller candidate set and more cells to query; coarser
means fewer lookups and more filtering. **And it interacts with density**, so any single global precision is
wrong somewhere — which is the argument for storing several precisions, or for a quadtree, or for accepting
that the numbers are tuned for the cities that matter.

**The index never gives the final answer.** A cell is a box and the requirement is a circle, so the exact
distance filter always runs. Estimates that omit it under-count the work, and designs that omit it return
drivers 2.8 km away for a 2 km query.

**When would I not build any of this?** When the data fits in memory and the query rate is low — a few
thousand points and a linear scan with a distance calculation is a millisecond and needs no index at all.
When PostGIS is available and the write rate is modest, where a GiST index is one line and has none of the
boundary or tuning problems. And when the requirement is really "the nearest one" rather than "everything
within a radius", where a managed service or a routing engine may be a better fit than an index you maintain.

---

## 8. In the interview

### How it gets asked

- *"How do you find all drivers within two kilometres?"* — the direct version.
- *"Why can't you just index latitude and longitude?"* — the arithmetic question.
- *"Design Uber / a food delivery app / a store locator."* — where this appears as a component.
- *"What is a geohash?"*
- *"A driver twenty metres away is not being returned. Why?"* — the boundary question, and the best one.
- *"Drivers report their location every four seconds. Where does that go?"*

### The first ninety seconds

> "The reason this is not a simple `WHERE` clause is that a B-tree indexes one dimension and a location is
> two. An index on latitude narrows me to a horizontal band around the entire planet, and then every row in
> that band is checked against longitude — hundreds of thousands of rows to find a couple of hundred. **And a
> composite index on `(lat, lng)` does not help**, because it only narrows on the second column once the first
> is a single value, and latitude here is a range.
>
> **So the move is to reduce two dimensions to one while preserving nearness: give every location a name such
> that nearby locations share a prefix.**
>
> **A geohash** does that by interleaving the bits of latitude and longitude and encoding them in base 32. A
> shared prefix means a shared box: six characters is about 1.2 by 0.6 kilometres, seven is about 150 metres.
> So 'near me' becomes a prefix range scan on an ordinary B-tree, which is exactly what B-trees are good at.
>
> **The thing I would raise before you ask is the boundary problem.** Two points twenty metres apart can share
> no prefix at all if a cell edge runs between them. So a query is **the cell plus its eight neighbours** —
> nine prefix scans — and the libraries compute neighbours for you. **That is not an edge case: for a
> 500-metre radius on precision-6 cells, roughly 70% of query points are within 500 metres of a cell edge, so
> most queries need it.**
>
> **And the index never gives the final answer.** A cell is a box and the requirement is a circle, so the last
> step is always an exact distance filter over the candidates. The index's job is to get me from ten million
> rows to five hundred, not to five hundred to twenty.
>
> The other question I would ask is about the write pattern, because for something like ride-hailing it is a
> hundred thousand drivers reporting every four seconds — twenty-five thousand writes a second against maybe
> fourteen reads. **That data is ephemeral and does not belong in the durable database at all**, and
> recognising that changes the whole architecture."

### The follow-ups

**"A driver twenty metres away is not being returned. What is wrong?"**

> "Almost certainly the boundary problem, and I would explain the mechanism rather than just name it.
>
> A geohash cell is a box, and two points on opposite sides of a cell edge share no useful prefix even if they
> are metres apart — one might be `te7ud5` and the other `te7uf0`. A pure prefix search on my own cell simply
> does not see the other one.
>
> **The fix is to search the cell and its eight neighbours**, which the geohash library gives me directly.
> Nine lookups instead of one.
>
> **And the reason I would call this a design error rather than a rare edge case is the arithmetic.** With
> precision-6 cells at roughly 1.2 by 0.6 kilometres, and a 500-metre search radius, about seventy percent of
> possible query positions are within 500 metres of some edge. So a majority of queries need at least one
> neighbouring cell. Anyone who tested with a point in the middle of a cell would never see it.
>
> **The other candidates I would check**, because it might not be the boundary: a freshness filter excluding a
> driver whose last report is stale — which is correct behaviour, not a bug; the precision being too fine so
> that nine cells do not cover the radius; and the exact distance filter using a flat-earth approximation
> that is wrong at that scale.
>
> **And the structural fix, if this keeps happening:** move to H3 or S2, where the neighbour handling is
> cleaner — H3's hexagons have all six neighbours equidistant, so 'expand by one ring' is uniform, whereas a
> square's diagonal neighbours are 1.41 times further and the ring is lopsided."

**"Geohash or quadtree? What decides it?"**

> "How much the data moves, and how uneven the density is.
>
> **Geohash cells are a fixed grid.** Simple — one indexed string, ordinary B-tree, works in any database, and
> shards naturally by prefix. Updating a point's location is writing one string, which is why it survives a
> heavy write load. What it does not do is adapt: precision-6 in central Mumbai returns thousands and the same
> precision over farmland returns nothing, and cells are noticeably distorted by latitude — a precision-6 cell
> is 1.2 km wide at the equator and 0.53 km in Reykjavik.
>
> **A quadtree subdivides only where points are dense**, so every leaf holds roughly the same number of points
> and query cost is predictable everywhere. That is exactly what you want for shops, property listings, or
> points of interest — data that is wildly uneven and does not move.
>
> **The cost is mutation.** A moving point may leave one leaf and enter another, which can trigger a split or
> a merge, and under concurrent updates that needs locking. For a hundred thousand drivers reporting every
> four seconds — twenty-five thousand updates a second — that is the wrong structure.
>
> **So: quadtree for static-ish, uneven data. Geohash or H3 for moving objects.** And in practice, for live
> driver locations I would reach for Redis GEO first, which is a sorted set with geohash scores and does the
> boundary and distance handling for me — a hundred thousand operations a second on one instance, and about
> ten megabytes for a hundred thousand drivers."

**"Where do twenty-five thousand location updates a second actually go?"**

> "Not into the durable database, and I think recognising that is the main architectural point in these
> designs.
>
> **The data is ephemeral.** A driver's location four seconds ago is worthless — the current one supersedes it
> entirely. There is no query that needs history for dispatch, and if the entire store were lost, every driver
> re-reports within four seconds and the system is whole again.
>
> **So: Redis, keyed by city or region, with a TTL of maybe thirty seconds.** `GEOADD` per update, `GEOSEARCH`
> per rider request. A hundred thousand drivers is about ten megabytes and well within one instance's
> throughput; sharding by city is natural and never needs a cross-shard query, because nobody requests a ride
> across cities.
>
> **The TTL is doing real work.** A driver who goes offline stops reporting, and their entry expires
> automatically — so 'is this driver still available' needs no separate mechanism and no cleanup job. That is
> a nice property to get for free.
>
> **What does go to durable storage is the trip**, not the pings — start, end, route, fare — which is a few
> writes per trip rather than tens of thousands a second. And if location history is needed for analytics or
> disputes, that is a separate, batched, append-only stream into object storage, sampled rather than complete.
>
> **The general principle:** separate the high-churn ephemeral state from the low-volume durable state, and
> give them completely different homes. Trying to serve both from one database is what makes these systems
> expensive."

**"Would you use PostGIS instead?"**

> "For most systems, yes, and I would say that rather than reflexively building a geohash scheme.
>
> PostGIS gives me a genuine two-dimensional index — a GiST R-tree over bounding boxes — so there is **no
> boundary problem and no cell precision to tune.** `ST_DWithin` does proper spherical distance,
> `ORDER BY geom <-> point` does an indexed nearest-neighbour search, and it handles polygons and lines as
> well as points, which matters the moment somebody asks 'which delivery zone is this address in'.
>
> And it is one extension and one index on data that is already in the database, queryable alongside every
> other column — 'restaurants within 2 km that are open now and rated above four' is one query, whereas with
> an external geo store it is a join across two systems.
>
> **Where it stops being right is write throughput.** An R-tree update is considerably more expensive than
> writing a string, so twenty-five thousand location updates a second is beyond a single Postgres instance —
> realistically five to twenty thousand writes a second with a GiST index. For read-heavy location data —
> shops, listings, addresses — that ceiling is irrelevant.
>
> **So my default is: PostGIS for anything that is mostly read, Redis GEO for live moving objects, and H3 or
> S2 when I need consistent cell geometry across the globe or want to shard by cell across many machines.**
> Hand-rolling geohash prefixes is the option I would justify rather than assume."

### The model answer

*"Design the driver-matching component of a ride-hailing service: 100,000 active drivers in a city, drivers
report location every four seconds, riders request a car and want the nearest few."*

> "Let me lead with the asymmetry, because it decides everything else.
>
> **Twenty-five thousand writes a second against maybe fourteen reads a second at peak.** A hundred thousand
> drivers reporting every four seconds is twenty-five thousand updates; fifty thousand ride requests an hour is
> about fourteen a second. **This is one of the most write-skewed workloads in any common design**, and the
> write data is completely disposable — a location from four seconds ago has no value.
>
> **So the live location store is Redis, not the database.** A geospatial sorted set per city, `GEOADD` on
> every driver ping, with a thirty-second TTL on each driver's entry. A hundred thousand drivers is about ten
> megabytes and twenty-five thousand operations a second is comfortable for one instance. **If the whole store
> is lost, it rebuilds itself in four seconds**, so it needs no replication for durability — only for
> availability.
>
> **The TTL is load-bearing.** A driver who closes the app stops reporting and disappears automatically, so
> 'currently available' needs no separate heartbeat mechanism and no reaper job.
>
> **The read path.** A rider requests a car at a point. `GEOSEARCH ... BYRADIUS 2 km ASC COUNT 20` gives me
> the nearest twenty candidates with distances, boundary handling and spherical maths already done.
> **I would not hand-roll geohash prefixes here** — Redis's implementation is exactly that, done correctly,
> and reimplementing it is how you get the boundary bug.
>
> **Then the part the index does not do: ranking.** Straight-line distance is not the right answer — a driver
> 800 metres away across a river is worse than one 1.5 kilometres away on the same road. So the candidate set
> from Redis is scored on estimated time of arrival, driver rating, and whether they are already finishing a
> trip nearby. **The index narrows ten thousand to twenty; the business logic picks one of the twenty**, and
> conflating those two steps is the common mistake.
>
> **Sharding is by city, and that is the nice property of this domain**: nobody requests a ride across cities,
> so there is never a cross-shard query. A geo-partitioned Redis cluster keyed by city id, with the API
> routing on the request's coordinates.
>
> **What goes to the durable database** is the trip — request, matched driver, start, end, route, fare — which
> is a handful of writes per trip, so a few hundred a second. Completely different volume, completely different
> durability requirement, and a completely different store.
>
> **Two things I would flag as harder than they look.** First, **matching is not just search** — two riders
> must not be offered the same driver, so there is a reservation step with a short lock or a conditional
> write, which is the [day 127](../day-127-graph-bfs/README.md) distributed-lock problem and needs the fencing
> discussion. Second, **surge and supply balance are the actual product**, and they need aggregate density per
> cell rather than per-driver lookups — which is where H3 earns its place, because equal-area hexagons make
> 'demand per cell' comparable across the city in a way that latitude-distorted geohash cells do not.
>
> **And what I would not build:** a quadtree. The data moves constantly, and a structure that splits and merges
> on every update is the wrong shape for twenty-five thousand writes a second. Quadtrees are for the static
> half of this problem — the restaurants, not the drivers."

---

## 9. Recall card

**A B-tree indexes one dimension and a location is two** — an index on latitude gives you a band round the
planet, and a composite `(lat, lng)` index does not help because latitude is a range, not a value.

**The move is to reduce 2D to 1D preserving nearness.** A **geohash** interleaves the bits so a **shared prefix
= a shared box** (precision 6 ≈ 1.2 × 0.6 km, precision 7 ≈ 150 m), and "near me" becomes a prefix range scan.

**The boundary problem is not an edge case.** Points metres apart can share no prefix, so you query the cell
**and its eight neighbours** — for a 500 m radius on precision-6 cells, ~70% of query points need it.

**Geohash: fixed cells, trivial updates, distorted by latitude → moving objects. Quadtree: cells adapt to
density, mutation is expensive → static uneven data. S2/H3: proper spherical cells, H3's six neighbours
equidistant. PostGIS/R-tree: no boundary problem, no tuning, lower write ceiling.**

**The index narrows; it never answers.** A cell is a box and the query is a circle, so an exact distance filter
always follows. And for live locations, **the write path is ephemeral** — Redis with a TTL, rebuilt in seconds
if lost, while trips go to the durable store.
