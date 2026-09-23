---
day: 161
track: system-design
title: "Design Uber"
phase: "High-level design case studies"
status: written
---

# Design Uber

## 1. What this is, and why they ask it

Uber matches a rider who wants a car with a driver who has one, **and the difficulty is that both of them are
moving.**

They ask it because **it is the only design in this set where the state changes continuously and physically.**
Every other system stores things that sit still — tweets, files, videos. **Here a million cars are each
sending a new position every four seconds**, and a query is "who is near me *right now*", where "now" means
within a few seconds and "near" means within a couple of kilometres.

Three things carry the interview.

**Geospatial indexing.** "Find drivers within 3 km" is not a query a normal index can answer, because **a
B-tree on latitude and a B-tree on longitude cannot be combined usefully** — you get everything in a band, not
everything in a circle. **The answer is to turn two dimensions into one**, with geohashing or a hierarchical
cell system, and knowing why that is necessary is the substance.

**The write rate.** A million drivers reporting every four seconds is **250,000 location writes a second**,
which is a large number for tiny payloads, and it makes the location store completely unlike the trip store
sitting next to it.

**And matching, which is not a lookup.** The nearest driver is often not the right one — traffic, direction of
travel, driver acceptance rate, and the fact that assigning greedily one rider at a time is measurably worse
than batching a few seconds of requests and solving them together. **That last point is where the DP and the
system design meet**, because batched matching is the assignment problem.

By the end of this lesson you can design the location pipeline, the geospatial index, the matching service,
the trip lifecycle and pricing, and size all of it.

---

## 2. The story

The auto stand outside the station had about forty drivers and one man with a whistle, and Karim had held the
whistle for nine years.

**His job was to know two things at once: who was free, and where they were.**

The first part was easy and physical. **The autos queued.** You came back from a fare, you joined the end, and
when you reached the front you took the next passenger. **Nobody argued because the queue was visible.**

**The problem was that the queue only worked at the stand.**

Because half the drivers were not at the stand. They were dropping somebody at the hospital, or waiting
outside the college, or stuck at the level crossing. **And a passenger at the stand did not care where they
were — but a passenger who telephoned did**, because the nearest auto to them might be the one at the college,
not the one at the front of the queue.

So Karim did the thing that made him useful, and it took him about a year to settle into.

**He divided the town into pieces.** Not on any map — in his head, and later on a board with chalk. **Station,
college, hospital, the market, the two colonies, the crossing.** Seven pieces, and later eleven.

**And he did not track where each auto was. He tracked which piece it was in.**

Which was much less information and almost as useful. **When a call came from the college, he looked at the
college piece and the two pieces next to it**, and if there was an auto in any of them he sent it, and if
there was not he looked wider.

There were two things he learned that took longer.

**The first was that the nearest one was often the wrong one.** The auto two hundred metres away might be
pointing the wrong way down a one-way, or on the far side of the crossing when the train was through.
**"Near" on his chalk board and "near" in minutes were not the same thing**, and he learned to know the
difference by knowing the town.

**And the second was the thing he did on Friday evenings**, which he never explained to anybody.

Friday at seven, four or five calls would come in together. **And instead of answering them one at a time,
which is what he did all week, he would hold them for a minute and then send all five autos at once.**

Because answering the first call with the nearest auto sometimes stranded the second caller. **Held together,
he could see all five and all the autos, and shuffle them** — and the total waiting was lower, even though the
first caller waited slightly longer than they would have.

---

## 3. The idea in plain English

Karim's chalk pieces are the geospatial index, his observation about the one-way street is the difference
between distance and travel time, and his Friday evening is batched matching.

**Start with the two problems, because they are genuinely separate systems.**

```
  LOCATION / MATCHING              TRIPS / PAYMENTS
  1,000,000 drivers                ~1,000 trips/second
  a write every 4 seconds          a few writes per trip
  = 250,000 writes/second          = ~5,000 writes/second
  tiny payloads, disposable        must be durable, transactional
  in-memory, sharded by region     a relational database
  losing a point is FINE           losing a payment is NOT
```

**Saying that split early is worth doing**, because the two halves have opposite requirements and combining
them is the mistake.

**Now the geospatial problem, which is the interesting one.**

**"Find drivers within 3 km of this point" is not something a normal index answers.** A B-tree on latitude
finds everything in a horizontal band. A B-tree on longitude finds a vertical band. **You cannot intersect
them efficiently** — the database would scan one band and filter, and in a city that band contains a large
fraction of all drivers.

**The fix is to turn two dimensions into one, so an ordinary index works.**

**Geohashing** does it by interleaving the bits of latitude and longitude and encoding the result as a string.
**Nearby points share a prefix.** `tdr1x` and `tdr1y` are adjacent cells; `tdr1` is the bigger cell containing
both.

**So "drivers near me" becomes "drivers whose geohash starts with `tdr1`"** — a prefix range scan, which every
index in the world can do.

**And there is a specific flaw worth knowing, because it is the follow-up.** **Two points can be metres apart
and share no prefix at all**, if they sit either side of a cell boundary. **The fix is to search the cell plus
its eight neighbours**, which geohash libraries compute directly. **Nine cells, not one**, and forgetting that
means missing the closest driver because they are across a line that does not exist on the ground.

**The alternatives are worth naming.** **Google's S2** maps the sphere onto a cube and uses a Hilbert curve,
**which keeps nearby points closer together than geohashing does** and handles the poles properly. **Uber's own
H3** uses hexagons, and the reason is neat: **a hexagon has six neighbours all at the same distance, while a
square has four edge neighbours and four corner ones at different distances** — which makes "expand the search
outwards" behave uniformly.

**And Redis has `GEOADD` and `GEOSEARCH` built in**, which is a sorted set with geohash scores underneath, and
it is what a smaller system should simply use.

**Now the write rate, which shapes the location store.**

**A million drivers reporting every four seconds is 250,000 writes a second.** That is large, and three
properties make it manageable.

**The payloads are tiny** — driver id, latitude, longitude, heading, timestamp: about fifty bytes.

**Only the latest matters.** A location from thirty seconds ago is useless, **so this is an overwrite, not an
append** — the store holds one row per driver, not a history.

**And losing one is fine.** A dropped location point is corrected four seconds later. **So the location store
can be entirely in memory with no durability guarantee at all**, which is what makes 250,000 writes a second
easy rather than hard.

**Sharding is by geography**, which is natural: a driver in Mumbai and a driver in Delhi never appear in the
same query, so the system is really thousands of independent small systems.

**Then matching, which is where the design gets opinionated.**

**The naive version: find the nearest available driver and assign.** It works and it is measurably worse than
the alternatives, for three reasons.

**Distance is not time.** Karim's one-way street. **Two hundred metres away across a river is twenty minutes;
a kilometre away on a clear road is three.** So candidates are found by distance and ranked by **estimated time
of arrival**, which needs a routing service that understands the road network.

**Greedy assignment is not optimal.** Assigning riders one at a time, each to their nearest driver, **can
strand a later rider whose only nearby driver was just taken.** Batching a few seconds of requests and solving
them together produces lower total waiting.

**And that batched problem is the assignment problem** — from [day 160](../day-160-bitmask-dp/README.md) —
which for small batches is exactly what bitmask DP solves, and for realistic batches is what the Hungarian
algorithm solves in `O(n³)`. **The connection is real and worth making explicitly.**

**The trade is latency**: batching adds a few seconds before anyone is matched. **Uber's published work says
the total wait still improves**, because the improvement in matching quality outweighs the delay.

**Then the dispatch protocol, which has a specific correctness requirement.**

**A driver must not be offered to two riders at once.** So the assignment takes a **lock on the driver**, sends
the offer, and waits a few seconds for acceptance. **On acceptance the trip is created; on rejection or
timeout the lock is released and the driver returns to the pool.**

**The lock must expire**, because a driver whose phone dies mid-offer would otherwise be unavailable forever.
**That is [day 127](../day-127-graph-bfs/README.md)'s distributed lock, and the TTL is the whole point.**

**Then the trip, which is the boring half and must be the reliable one.**

**A trip is a state machine**: requested → matched → driver arriving → in progress → completed → paid. **Each
transition is a durable write**, and the payment at the end is the one thing in this entire system that must
not be lost or duplicated.

**And the two halves have opposite requirements**: location data is high-volume and disposable; trip data is
low-volume and must be exactly right. **Do not put them in the same store.**

**Finally, pricing, which is a real-time feedback loop.**

**Surge pricing exists because demand and supply are local and change by the minute.** The mechanism is to
divide the city into cells, compute the ratio of open requests to available drivers per cell every minute or
two, and apply a multiplier where the ratio is high.

**It is a control loop and it can oscillate.** A high price suppresses demand, the ratio falls, the price
drops, demand returns. **Smoothing and rate limits on how fast the multiplier moves are not polish; they are
what stops the system hunting**, which is a genuinely interesting property to raise.

---

## 4. The picture

The two systems, which must not be one:

```
   LOCATION PIPELINE (hot, disposable)       TRIP SYSTEM (durable, small)

   driver app --every 4 s-->                 rider requests
        |                                          |
   [ ingest, sharded by region ]             [ trip service ]
        |                                          |
   [ in-memory geo index ]                   [ relational DB ]
        |   one row per driver                     | trips, payments,
        |   OVERWRITTEN, not appended              | receipts
        v                                          v
   "who is near this point?"                 must be durable
   250,000 writes/second                     ~5,000 writes/second
   losing a point: fine                      losing a payment: not
```

Why a normal index cannot answer "within 3 km":

```
  index on latitude:            index on longitude:

     +-----------------+           +--+
     |#################|           |##|
     |#################|           |##|      each finds a BAND
     +-----------------+           |##|
                                   +--+

  what you want:                intersecting them:

        .-''-.                     +--+
      /        \                   |##|   <- still a band's worth
     |    ()    |                  |##|      of candidates to filter
      \        /                   +--+
        '-..-'

  In a dense city, one band is a large fraction of ALL drivers.
  -> the database scans and filters, and it does not scale.
```

Geohashing: two dimensions into one:

```
  interleave the bits of latitude and longitude, then encode

     lat bits:  1 0 1 1 0 ...
     lon bits:   0 1 1 0 1 ...
     interleaved: 1 0 0 1 1 1 1 0 0 1 ...
     encoded:   "tdr1x"

  NEARBY POINTS SHARE A PREFIX:
     tdr1x  and  tdr1y   are adjacent
     tdr1                is the cell containing both
     tdr                 is the bigger cell containing that

  -> "drivers near me" = "geohash starts with tdr1"
  -> a PREFIX RANGE SCAN, which any ordinary index can do

  precision by prefix length:
     4 chars  ~20 km      6 chars  ~600 m
     5 chars  ~2.4 km     7 chars  ~76 m
```

The boundary problem, which is the follow-up:

```
             cell "tdr1"  |  cell "tdr4"
                          |
                    A  *  |  * B
                          |
       A and B are 20 METRES apart
       and share NO prefix at all

  -> searching only my own cell MISSES the nearest driver

  FIX: search the cell PLUS ITS EIGHT NEIGHBOURS

       +------+------+------+
       | tdr0 | tdr1 | tdr4 |
       +------+------+------+
       | tdr2 | ME   | tdr5 |     <- 9 cells, always
       +------+------+------+
       | tdr3 | tdr6 | tdr7 |
       +------+------+------+

  Every geohash library computes the neighbours directly.
  Forgetting this is the classic bug, and it fails only for
  riders near a boundary — which is most of them.
```

Why hexagons (H3):

```
   SQUARE CELLS                    HEXAGONAL CELLS

   +---+---+---+
   | a | b | c |                      / \ / \
   +---+---+---+                     | a | b |
   | d | X | e |                    / \ / \ / \
   +---+---+---+                   | c | X | d |
   | f | g | h |                    \ / \ / \ /
   +---+---+---+                     | e | f |
                                      \ / \ /
   b, d, e, g are EDGE neighbours
   a, c, f, h are CORNER neighbours   all six are EDGE neighbours
   -> different distances!            -> all the SAME distance

   "expand the search outwards" behaves uniformly with hexagons
   and unevenly with squares. That is Uber's reason for H3.
```

Greedy against batched matching, which is Karim's Friday:

```
   two riders (R1, R2), two drivers (D1, D2)

   ETAs:        D1     D2
        R1     2 min  9 min
        R2     3 min  20 min

   GREEDY, R1 arrives first:
      R1 -> D1 (2 min, the nearest)
      R2 -> D2 (20 min, all that is left)
      TOTAL 22 min

   BATCHED, both considered together:
      R1 -> D2 (9)   R2 -> D1 (3)    total 12
      R1 -> D1 (2)   R2 -> D2 (20)   total 22
      -> pick the first. TOTAL 12 min

   10 minutes better, and R1 waited 7 minutes longer.

   THIS IS THE ASSIGNMENT PROBLEM: n riders, n drivers,
   minimise the total. Hungarian algorithm, O(n^3).
   The COST of batching is a few seconds of delay before
   anyone is matched at all.
```

The dispatch lock, and why it must expire:

```
  match found: rider R -> driver D

  1. LOCK D             SET lock:D "R" NX EX 15
     -> if the lock exists, D was already offered to someone else
  2. send the offer to D's phone
  3. wait up to 15 seconds

  ACCEPT   -> create the trip, D is now "on trip"
  REJECT   -> DEL lock:D, D returns to the pool, rematch R
  TIMEOUT  -> the lock EXPIRES on its own, D returns to the pool

  THE TTL IS THE POINT: a driver whose phone dies mid-offer
  would otherwise be locked out forever, and no explicit
  "release" message will ever arrive.
```

---

## 5. How it actually works

### Ingesting locations

```python
def report_location(driver_id: int, lat: float, lon: float,
                    heading: float, at: float) -> None:
    cell = h3.geo_to_cell(lat, lon, resolution=8)          # ~460 m across
    pipe = redis.pipeline()
    pipe.hset(f"driver:{driver_id}", mapping={
        "lat": lat, "lon": lon, "heading": heading, "at": at, "cell": cell})
    pipe.expire(f"driver:{driver_id}", 30)                 # stale = gone
    pipe.zadd(f"cell:{cell}", {driver_id: at})
    pipe.execute()
```

**`expire` doing the offline detection is the neat part.** A driver whose app stops reporting simply
disappears from the index after thirty seconds — **there is no "go offline" message to lose**, which is the
same expiring-presence pattern as [day 157](../day-157-stock-dp/README.md).

**One row per driver, overwritten**, not a history — the location store holds the present, and the past goes
to an analytics pipeline via a separate stream.

**And moving cells needs the old entry removed**, which the code above omits for clarity — in practice the
write compares the new cell with the stored one and issues a `ZREM` when it changes.

### Finding nearby drivers

```python
def nearby_drivers(lat: float, lon: float, radius_m: int = 3000) -> list[dict]:
    centre = h3.geo_to_cell(lat, lon, resolution=8)
    rings = h3.k_ring(centre, k=radius_m // 460 + 1)       # the cell AND its ring
    candidates: set[int] = set()
    for cell in rings:
        candidates |= set(redis.zrange(f"cell:{cell}", 0, -1))

    result = []
    for driver_id in candidates:
        data = redis.hgetall(f"driver:{driver_id}")
        if data and haversine(lat, lon, data["lat"], data["lon"]) <= radius_m:
            result.append(data)
    return result
```

**`k_ring` is the neighbour expansion**, and it is why this returns the driver twenty metres away across a cell
boundary. **Searching only `centre` is the classic bug.**

**And the final `haversine` filter matters**: cells are approximate, so a driver in a neighbouring cell may be
further than the radius. **The index narrows; the exact test decides.**

### Ranking by time, not distance

```python
def rank_candidates(rider: dict, drivers: list[dict]) -> list[tuple[float, dict]]:
    etas = routing.batch_eta(
        origins=[(d["lat"], d["lon"]) for d in drivers],
        destination=(rider["lat"], rider["lon"]),
    )
    scored = []
    for driver, eta in zip(drivers, etas):
        score = eta
        score *= 1.0 - 0.1 * driver["acceptance_rate"]     # likely to accept
        if heading_towards(driver, rider):
            score *= 0.9                                   # already coming this way
        scored.append((score, driver))
    return sorted(scored)
```

**`routing.batch_eta` in one call, not one per driver.** Twenty candidates means one request, and doing it
individually is the difference between twenty milliseconds and four hundred.

**The score is not the ETA alone**, and each adjustment is a real effect: a driver who rejects most offers
wastes the fifteen-second lock, and a driver already travelling towards the rider will arrive sooner than the
straight-line estimate suggests.

### Batched matching

```python
def match_batch(requests: list[dict], window_seconds: float = 5.0) -> list[tuple]:
    """Collect a few seconds of requests, then solve them together."""
    riders = requests
    drivers = union_of_nearby_drivers(riders)
    if not drivers:
        return []

    cost = [[eta(driver, rider) for rider in riders] for driver in drivers]
    pairs = hungarian(cost)                   # O(n^3), optimal for the batch
    return [(drivers[d], riders[r]) for d, r in pairs]
```

**`hungarian(cost)` is the assignment problem**, and it is the same problem bitmask DP solved yesterday — **the
Hungarian algorithm is `O(n³)` where bitmask DP is `O(2ⁿ · n)`, so for a batch of fifty riders it is a hundred
and twenty-five thousand operations rather than an impossibility.**

**The window is the trade.** Five seconds of delay before anyone is matched, in exchange for a materially
better assignment. **Uber's published results say the total wait falls**, which is the justification.

### The dispatch lock

```python
OFFER_SECONDS = 15

def offer_ride(driver_id: int, rider_id: int) -> bool:
    if not redis.set(f"lock:driver:{driver_id}", rider_id,
                     nx=True, ex=OFFER_SECONDS):
        return False                          # already offered to someone else
    push.send(driver_id, {"type": "offer", "rider": rider_id,
                          "expires_in": OFFER_SECONDS})
    return True

def on_driver_accepts(driver_id: int, rider_id: int) -> dict | None:
    holder = redis.get(f"lock:driver:{driver_id}")
    if holder != str(rider_id):
        return None                           # the offer expired; too late
    trip = trip_store.create(driver_id, rider_id, state="matched")
    redis.delete(f"lock:driver:{driver_id}")
    return trip
```

**`SET NX EX` is both the mutual exclusion and the timeout.** Two matchers cannot offer the same driver, **and
a driver whose phone dies is released automatically** — no explicit unlock is required, which matters because
that message is exactly the one that will be lost.

**The re-check in `on_driver_accepts` handles the race** where the lock expired between the offer and the
acceptance: **the driver taps accept a moment too late, and the ride has already gone to someone else.** That
must be handled, and it happens constantly.

### The trip state machine

```python
TRANSITIONS = {
    "requested":  {"matched", "cancelled"},
    "matched":    {"arriving", "cancelled"},
    "arriving":   {"in_progress", "cancelled"},
    "in_progress": {"completed"},
    "completed":  {"paid"},
}

def transition(trip_id: int, to_state: str) -> None:
    with db.transaction():
        trip = trip_store.lock_for_update(trip_id)
        if to_state not in TRANSITIONS.get(trip.state, set()):
            raise InvalidTransition(f"{trip.state} -> {to_state}")
        trip_store.update(trip_id, state=to_state, at=time.time())
        events.publish("trip", {"trip_id": trip_id, "state": to_state})
```

**An explicit transition table, checked on every write.** Trips get cancelled, apps retry, network messages
arrive out of order — **and without the check, a retried "complete" on an already-paid trip charges twice.**

**`lock_for_update` inside a transaction is what makes it safe under concurrency**, and this is the half of the
system where a relational database earns its place.

### Surge pricing

```python
def compute_surge(cell: str) -> float:
    demand = redis.get(f"requests:{cell}:last_2min") or 0
    supply = redis.zcard(f"cell:{cell}")
    ratio = int(demand) / max(int(supply), 1)

    target = 1.0 if ratio < 1.5 else min(1.0 + (ratio - 1.5) * 0.4, 3.0)
    current = float(redis.get(f"surge:{cell}") or 1.0)
    smoothed = current + max(-0.2, min(0.2, target - current))    # rate-limited
    redis.set(f"surge:{cell}", smoothed, ex=300)
    return smoothed
```

**The rate limit on how fast the multiplier moves is the important line**, and it is not cosmetic. **Without
it the loop oscillates**: a high price suppresses demand, the ratio collapses, the price drops, demand
returns, and riders see the price swinging every two minutes. **Smoothing is what makes a control loop stable
rather than a hunting one.**

**And the cap at 3.0 is a policy decision**, not a technical one — worth naming as such.

### The real systems

```
H3               Uber's hexagonal grid, open-sourced; the reason for
                 hexagons is uniform neighbour distance
S2               Google's cell system: Hilbert curve on a cube
geohash          the simple, widely supported option; Redis uses it
Redis GEO        GEOADD / GEOSEARCH — a sorted set with geohash scores;
                 what a smaller system should just use
Kafka            the location stream, feeding analytics separately
                 from the live index
PostgreSQL/
PostGIS          trips and payments; PostGIS for offline geo queries
OSRM / Valhalla  open-source routing engines for ETAs
```

**Naming H3 and its reason is a good detail**, because it is a specific, defensible engineering decision that
came out of this exact problem.

---

## 6. The numbers

**Scale.**

```
5,000,000 drivers, ~1,000,000 online at peak
20,000,000 rides/day

rides:      20e6 / 86,400 = ~230/second average
                            peak ~1,000/second

locations:  1,000,000 online x 1 report / 4 s
          = 250,000 writes/second
```

**Two hundred and fifty thousand writes a second against a thousand rides a second** — **the location pipeline
is 250 times the write volume of the business it supports**, and that ratio is the first thing to say.

**Location data.**

```
per report: driver id (8) + lat (8) + lon (8) + heading (4) + timestamp (8)
          = ~40 bytes, ~50 with overhead

250,000/s x 50 B = 12.5 MB/s = ~1 TB/day IF stored

but only the LATEST matters:
  1,000,000 online drivers x ~200 bytes (hash + index entry)
  = 200 MB of live state

-> the live index is 200 MB. The 1 TB/day goes to a stream for
   analytics, and never to the query path.
```

**Two hundred megabytes for the entire live index** is the fact that makes this affordable: **it fits in one
machine's memory, and it is sharded by region for isolation rather than for capacity.**

**Query cost.**

```
1,000 ride requests/second at peak
each searches ~9-19 cells (the centre plus one or two rings)
each cell holds ~10-100 drivers in a dense city

-> ~500 candidate drivers per request, filtered to ~20 by exact distance
-> 1,000 x 19 cell reads = 19,000 Redis reads/second

trivial for Redis (~100,000 ops/s per instance)
-> the READ side is not the problem. The WRITE side is.
```

**Sharding by region.**

```
250,000 writes/second globally
but a driver in Mumbai never appears in a Delhi query

~500 cities, unevenly:
  the largest city at peak: ~50,000 drivers -> ~12,500 writes/second
  Redis handles ~100,000 ops/s -> one instance per large city,
  with several cities sharing an instance elsewhere

-> the system is really ~100 independent small systems, which is
   why the global number is misleading.
```

**Cell sizing, which is a real tuning decision.**

```
H3 resolution 8: ~460 m across, ~0.7 km^2

a dense city centre: ~2,000 drivers / 20 km^2 = 100 per km^2
                     -> ~70 drivers per cell

a 3 km search radius:
  radius / cell size = 3000 / 460 ~ 7 rings
  cells in 7 rings = 1 + 3*7*8 = 169 cells
  -> 169 x 70 = ~11,800 candidates. TOO MANY.

-> use a COARSER resolution for the search:
   resolution 7 (~1.2 km across): 3 rings = 37 cells x ~500 = 18,500
   resolution 6 (~3.2 km):        1 ring  = 7 cells x ~3,000 = 21,000

   or search resolution 8 with a SMALL radius first and widen
   only if too few candidates:
     1 ring (7 cells x 70 = ~490)  -> usually enough
     3 rings if not
   -> ~500 candidates in the common case, which is right.
```

**Starting small and widening is the design**, and it is worth showing, because a fixed radius is either too
slow downtown or empty in the suburbs.

**Matching cost.**

```
batch window 5 seconds at peak: 1,000/s x 5 = 5,000 requests
but batches are PER CITY:
  a large city at peak ~100 requests per 5-second window

Hungarian algorithm on 100 riders x ~300 candidate drivers:
  O(n^3) with n = 300 -> 27,000,000 operations -> ~30 ms in C
-> well within the window

greedy, for comparison: 100 x 300 = 30,000 operations
-> 1,000x cheaper and measurably worse results
```

**Trips and payments.**

```
20,000,000 rides/day x ~6 state transitions = 120,000,000 writes/day
                                            = ~1,400 writes/second
                                              peak ~6,000

trip record: ~2 KB (route, fare breakdown, timestamps, ids)
20e6 x 2 KB = 40 GB/day = ~15 TB/year
+ replicas  = 45 TB/year

-> a completely ordinary relational workload. Which is the point:
   the DURABLE half of this system is small and boring, and it
   must stay that way.
```

**ETA computation, the hidden cost.**

```
1,000 requests/second x ~20 candidates = 20,000 ETA calculations/second

a routing engine: ~1-5 ms per route on a city-sized graph
-> 20,000 x 3 ms = 60 CPU-seconds per second = ~60 cores

and BATCHING matters enormously:
  one request with 20 origins: ~5 ms total
  20 separate requests:        ~60 ms + 20 round trips

-> batch_eta is not an optimisation; it is what makes the
   matching latency budget possible.
```

**End-to-end latency:**

```
location write                    ~1 ms   (fire and forget)
nearby search (19 cells)          ~5 ms
exact distance filter             ~1 ms
batch ETA for 20 candidates       ~10 ms
ranking                           ~1 ms
matching (within the batch)       ~30 ms
                                  -------
                                  ~50 ms of compute

+ the batch window                 5 s    <- dominates everything
+ driver acceptance               ~5 s

-> the system's latency is a product decision, not an engineering one.
```

---

## 7. The trade-offs

**Geohash against S2 against H3.** Geohash is simple, widely supported, and **has uneven cell sizes away from
the equator and a nasty boundary discontinuity.** S2's Hilbert curve keeps nearby points closer in the ordering
and handles the sphere properly. **H3's hexagons give uniform neighbour distances**, which makes ring expansion
behave sensibly, at the cost of hexagons not tiling a sphere perfectly — **there are twelve pentagons in the
grid, which is a real edge case in the library.** For most systems, **Redis GEO is the right answer and
building on H3 is justified only when ring expansion is central**, which for Uber it is.

**Cell size.** Small cells mean precise results and many cells to search — a 3 km radius at 460 m resolution
is 169 cells. **Large cells mean few lookups and many false candidates to filter.** The answer is neither: **a
small radius that widens when it finds too few drivers**, which adapts to density automatically and is what
makes downtown and the suburbs both work.

**Greedy against batched matching.** Greedy is instant and locally optimal, and **it strands riders whose only
nearby driver was just assigned.** Batching is optimal within the window and **delays every match by several
seconds.** The published evidence says total wait improves; **the honest framing is that this is a product
decision informed by measurement, not a purely technical one**, because the first rider genuinely waits longer.

**In-memory locations against durable ones.** In-memory gives 250,000 writes a second and **loses everything
on a restart** — which is fine, because every driver reports again within four seconds. **Making it durable
would cost enormously and buy nothing**, and recognising which data is disposable is the judgement being
tested.

**The two-system split.** Combining the location store and the trip store would be simpler operationally and
is wrong: **one needs 250,000 disposable writes a second and the other needs transactional guarantees on
payments.** No single store is good at both, **and forcing one to be is how the payments end up unreliable.**

**Surge pricing as a control loop.** It genuinely balances supply and demand and **it oscillates without
smoothing and rate limits**. It is also the most disliked feature in the product, so the multiplier cap is a
policy decision that engineering should surface rather than choose.

**When would I not build this?** **When the fleet is small and known** — a taxi company with forty cars needs a
list and a map, not a geospatial index. **When the matching is not real-time**: scheduled deliveries, which
become a routing and planning problem instead. **And the geo layer specifically — Redis GEO or PostGIS handle
millions of points comfortably**, and building on H3 is justified by ring-expansion behaviour rather than by
scale alone.

---

## 8. In the interview

### How it gets asked

- *"Design Uber."* or *"Design a ride-hailing service."* — the standard prompt.
- *"How do you find the nearest drivers?"* — the geospatial question, and the core of it.
- *"A million drivers each send a location every four seconds. How do you store that?"*
- *"Two riders request at the same time and there is one driver nearby. What happens?"*
- *"How does surge pricing work?"*
- *"What is wrong with just assigning the nearest driver?"*

### The first ninety seconds

> "The first thing I would establish is that **this is two systems with opposite requirements**, and keeping
> them separate is most of the design.
>
> **The location and matching side handles a million drivers each reporting every four seconds — 250,000
> writes a second.** Tiny payloads, only the latest one matters, and **losing a point is completely fine**
> because another arrives in four seconds. **In memory, sharded by region, no durability at all.**
>
> **The trip and payment side handles about a thousand rides a second** — a few writes each. **Small, and it
> must be exactly right**, because losing a payment is not recoverable. A relational database.
>
> **The location pipeline is 250 times the write volume of the business it supports**, and it is the one that
> must be allowed to be lossy.
>
> **Now the interesting problem: finding drivers near a point.** **A normal index cannot do this** — a B-tree
> on latitude gives a horizontal band, one on longitude gives a vertical band, and **intersecting them still
> leaves a large fraction of a city's drivers to filter.**
>
> **So: turn two dimensions into one.** Geohashing interleaves the bits of latitude and longitude, **so nearby
> points share a prefix** and "drivers near me" becomes a prefix range scan that any index can do.
>
> **And there is a flaw I would name immediately, because it is the classic bug.** Two points can be twenty
> metres apart and share no prefix, if they are either side of a cell boundary. **So you always search the
> cell plus its eight neighbours** — nine cells, never one.
>
> **Uber uses H3, which is hexagons**, and the reason is neat: **a hexagon's six neighbours are all the same
> distance away, while a square has four edge neighbours and four corner ones at different distances** — so
> expanding the search outwards behaves uniformly.
>
> **The live index is small.** A million online drivers at about two hundred bytes each is **two hundred
> megabytes** — it fits in memory on one machine, and it is sharded by city for isolation rather than for
> capacity.
>
> **And then matching, which I would flag as more than a lookup.** The nearest driver by distance is often not
> the nearest by time, and **assigning greedily one rider at a time is measurably worse than batching a few
> seconds and solving them together** — which is literally the assignment problem.
>
> **Where would you like me to go deeper?**"

### The follow-ups

**"How do you find the nearest drivers?"**

> "Not with a normal index, and the reason is worth being precise about, because it is what motivates
> everything else.
>
> **A B-tree on latitude finds every driver in a horizontal band. A B-tree on longitude finds a vertical
> band.** The database can use one of them and then filter — **and in a dense city, one band contains a large
> fraction of all drivers**, so it is effectively a scan.
>
> **The fix is to collapse two dimensions into one, so that ordinary index machinery works.**
>
> **Geohashing does it by interleaving the bits of latitude and longitude and encoding the result.** The key
> property is that **nearby points share a prefix**: `tdr1x` and `tdr1y` are adjacent cells, and `tdr1` is the
> larger cell containing both. **So the query becomes a prefix range scan**, and prefix length controls
> precision — five characters is about 2.4 kilometres, seven is about seventy-six metres.
>
> **Now the flaw, and I would raise it before being asked.** **Two points twenty metres apart can share no
> prefix at all** if they sit either side of a cell boundary. **So searching only my own cell misses the
> closest driver** — and it fails specifically for riders near a boundary, which is a large fraction of them.
>
> **The fix is to search the cell plus its eight neighbours**, which every geohash library computes directly.
> **Nine cells, always.**
>
> **And after the index narrows the candidates, an exact distance check decides**, because cells are
> approximate and a driver in a neighbouring cell may be outside the radius.
>
> **On which system to use: Uber built H3, using hexagons.** The reason is that **a hexagon's six neighbours
> are all equidistant**, while a square grid has edge neighbours and corner neighbours at different distances —
> **so 'expand the search by one ring' means something uniform.** Google's S2 uses a Hilbert curve on a cube,
> which preserves locality better than plain geohashing and handles the poles correctly.
>
> **For most systems the right answer is Redis GEO**, which is geohashing under a sorted set and handles
> millions of points comfortably. **Building on H3 is justified when ring expansion is central to the
> algorithm**, which for dispatch it is."

**"A million drivers send a location every four seconds. How do you handle that?"**

> "Two hundred and fifty thousand writes a second, and **three properties of the data make it much easier than
> that number suggests.** I would name all three, because each one removes a requirement.
>
> **One: the payloads are tiny.** Driver id, latitude, longitude, heading, timestamp — about fifty bytes.
> **So 250,000 writes a second is only twelve megabytes a second of actual data.**
>
> **Two: only the latest matters.** A location from thirty seconds ago is useless for dispatch. **So this is
> an overwrite, not an append** — one row per driver, not a history. **The live index is a million rows at
> about two hundred bytes, which is two hundred megabytes.** That fits in memory on a single machine.
>
> **Three, and this is the one that matters most: losing a write is fine.** A dropped location point is
> corrected four seconds later by the next one. **So there is no durability requirement at all** — the store
> can be entirely in memory, with no write-ahead log, no replication for durability, and no acknowledgement
> beyond 'received'.
>
> **Recognising which data is disposable is the judgement here**, because making this durable would cost
> enormously and buy nothing.
>
> **Sharding is by geography, and it is the natural boundary.** A driver in Mumbai never appears in a Delhi
> query, so **this is really about a hundred independent small systems, not one large one.** The largest city
> at peak might have fifty thousand drivers — twelve thousand writes a second — **which one Redis instance
> handles comfortably.** The global figure is misleading.
>
> **Two details I would build in.** **A TTL on each driver's record does offline detection for free**: a driver
> whose app stops reporting disappears after thirty seconds, **and no 'going offline' message has to be
> delivered** — which matters because that is exactly the message that gets lost when a phone dies.
>
> **And the historical stream is separate.** A terabyte a day of location history is genuinely valuable for
> analytics, ETA models and surge, **so it goes to Kafka and then to a data warehouse — never to the query
> path.** Mixing the live index and the historical store is how the query path gets slow."

**"What is wrong with just assigning the nearest driver?"**

> "Two things, and the second is the more interesting one.
>
> **First, the nearest driver by distance is often not the nearest by time.** Two hundred metres away on the
> far side of a river is twenty minutes; **a kilometre away on a clear road is three.** One-way streets,
> level crossings, and the direction the driver is already travelling all matter.
>
> **So I would use the geospatial index to find candidates by distance and then rank them by estimated time of
> arrival**, which needs a routing service that understands the road network. **And the ETAs must be fetched in
> one batched call** — twenty separate routing requests is four hundred milliseconds and one batched request is
> ten.
>
> **I would also adjust for two behavioural things**: a driver who rejects most offers wastes the fifteen-second
> lock and delays the rider, and a driver already heading towards the rider will arrive sooner than a
> straight-line estimate suggests.
>
> **Second, and this is the interesting one: greedy assignment is not optimal even with perfect ETAs.**
>
> **Concretely.** Two riders, two drivers. Rider one is two minutes from driver one and nine from driver two.
> Rider two is three minutes from driver one and twenty from driver two. **Greedy gives rider one the nearest
> driver, and rider two is left with twenty minutes — twenty-two total.** **Considered together, rider one
> takes driver two at nine and rider two takes driver one at three — twelve total.**
>
> **Ten minutes better, and rider one waited seven minutes longer.**
>
> **So: batch a few seconds of requests and solve them together, which is exactly the assignment problem.**
> The Hungarian algorithm does it in `O(n³)` — for a hundred riders against three hundred candidates in a city,
> that is about thirty milliseconds, **well inside the window.**
>
> **The cost is real and I would state it: everybody waits a few seconds before being matched at all.** Uber's
> published work says total wait falls anyway, because the matching improvement outweighs the delay — **but
> the first rider in a batch is genuinely worse off, so this is a product decision informed by measurement,
> not a purely technical one.**"

### The model answer

*"Design a ride-hailing service: five million drivers, a million online at peak, twenty million rides a day,
global."*

> "Let me split it in two first, because the two halves have opposite requirements and combining them is the
> main mistake available here.
>
> **The location and matching side: a million online drivers reporting every four seconds is 250,000 writes a
> second.** Fifty-byte payloads, only the latest matters, and losing one is fine. **In-memory, sharded by
> city, zero durability.**
>
> **The trip and payment side: twenty million rides a day is about a thousand a second at peak**, six state
> transitions each. **Small, and it must be exactly right.** A relational database with real transactions.
>
> **The location pipeline is 250 times the write volume of the business it supports, and it is the half that
> is allowed to lose data.**
>
> **Geospatial index.** A normal index cannot answer 'within 3 km' — latitude and longitude B-trees each give
> a band, and intersecting them still leaves a large fraction of a city. **So collapse two dimensions into
> one.** I would use **H3 at around resolution 8 — cells about 460 metres across** — with the driver's cell
> stored alongside their position.
>
> **A search reads the cell plus a ring of neighbours**, never just the cell, **because two points twenty
> metres apart across a boundary share no cell at all** — and that failure hits riders near boundaries, which
> is most of them.
>
> **And the radius adapts.** One ring is seven cells and about five hundred candidates downtown, which is
> right; **in the suburbs one ring finds nobody, so it widens.** A fixed radius is either too slow in the
> centre or empty at the edge, so **starting small and expanding is the design, not an optimisation.**
>
> **The live index is 200 MB** for a million drivers, so it is sharded by city for isolation rather than for
> capacity — **the largest city is twelve thousand writes a second, which one Redis instance handles.**
>
> **A TTL on each driver record gives offline detection for free**, with no 'going offline' message to lose.
>
> **Matching.** Candidates by distance, **ranked by ETA from a batched routing call** — distance is not time,
> and twenty separate routing requests would blow the latency budget on their own.
>
> **And matching is batched over about five seconds and solved as an assignment problem**, because greedy
> assignment strands riders whose only nearby driver was just taken. **A hundred riders against three hundred
> drivers is thirty milliseconds with the Hungarian algorithm**, well inside the window. **The cost is that
> everyone waits a few seconds to be matched, and the first rider in a batch is genuinely worse off** — a
> product decision I would want made with data rather than by me.
>
> **Dispatch uses a lock on the driver with a fifteen-second TTL.** Two matchers cannot offer the same driver,
> **and a driver whose phone dies is released automatically** — the message that would release them explicitly
> is exactly the one that gets lost. **And the acceptance handler re-checks the lock**, because a driver
> tapping accept a moment late is a constant occurrence, not an edge case.
>
> **The trip is a state machine with an explicit transition table checked on every write.** Apps retry, messages
> arrive out of order, **and without the check a retried 'complete' charges twice.**
>
> **Surge pricing is a control loop**: demand over supply per cell every couple of minutes, with a multiplier.
> **The rate limit on how fast it can move is the important part** — without it the loop oscillates, because a
> high price suppresses demand which drops the price which brings demand back. **And the cap is policy, which
> I would surface rather than choose.**
>
> **Two things I would flag.** **ETA computation is a hidden cost** — twenty thousand route calculations a
> second, about sixty cores — **and it is the component most likely to be the bottleneck**, not the geo index.
>
> **And the failure mode that matters is a city-level outage, not a global one.** Because everything is sharded
> by city, **a bad deploy or a Redis failure takes out one city completely**, which is a much more visible
> failure than partial global degradation. **I would want per-city isolation in the deployment as well as in
> the data**, and a fallback to greedy matching when the batch matcher is unavailable — degraded is much
> better than stopped."

---

## 9. Recall card

**Two systems with opposite requirements: locations (250,000 writes/s, 50-byte payloads, overwrite-only,
LOSSY BY DESIGN, in-memory, sharded by city) and trips/payments (~5,000 writes/s, durable, transactional).**
The location pipeline is **250× the write volume of the business it supports** — do not put them in one store.

**A normal index cannot answer "within 3 km"** — latitude and longitude B-trees each give a *band*, and
intersecting them still leaves a large share of a city. **Collapse two dimensions into one:** geohashing
interleaves the bits so **nearby points share a prefix**, turning it into a prefix range scan.

**Always search the cell PLUS its eight neighbours** — two points 20 m apart across a boundary share no
prefix, and this fails precisely for riders near boundaries. **H3 uses hexagons because all six neighbours are
equidistant**, where a square has edge and corner neighbours at different distances. **Then an exact haversine
filter decides** — the index narrows, it does not answer.

**The live index is only ~200 MB** for a million drivers. **A TTL does offline detection for free** — no
"going offline" message to lose. **Search radius adapts**: one ring downtown, widen in the suburbs.

**Greedy matching is measurably wrong.** Distance ≠ time (batch the ETA calls), and assigning one rider at a
time strands later riders — **22 minutes greedy against 12 batched on the worked example.** Batched matching
**is the assignment problem** (Hungarian, `O(n³)`, ~30 ms for 100×300), **at the cost of a few seconds' delay
for everyone.**

**Dispatch takes a lock on the driver with a TTL** — mutual exclusion and automatic release from one `SET NX
EX`, because the explicit unlock is the message that gets lost. **Re-check the lock on acceptance.** **Trips
need an explicit transition table**, or a retried "complete" charges twice. **Surge is a control loop and
needs rate-limiting**, or it oscillates.
