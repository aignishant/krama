---
day: 165
track: system-design
title: "Design a ticket booking system"
phase: "High-level design case studies"
status: written
---

# Design a ticket booking system

## 1. What this is, and why they ask it

A ticket system sells specific, numbered, non-interchangeable things — **seat 14F on tonight's 19:30 show** —
to many people who all want them at once.

They ask it because **it is the extreme case of a problem you met yesterday, and the extremity changes the
answer.** E-commerce has inventory contention; **ticketing has inventory contention as its defining
property.** A concert sells out in forty seconds. A train's Tatkal quota opens at ten in the morning and a
hundred thousand people submit within the same second.

Three things make it genuinely different from selling ordinary stock.

**Every unit is unique and non-substitutable.** You cannot ship "an equivalent seat". **So there is no
oversell recovery** — with a warehouse you can apologise and back-order; **with a seat there is one and someone
is standing in the aisle.**

**The contention is extreme and predictable.** Both halves matter: **extreme**, because a hundred thousand
requests hit the same few hundred rows in one second; **predictable**, because you know the sale opens at ten
o'clock. **Predictability is a gift** — it lets you pre-warm, pre-shard and queue in advance, which is not
available to systems whose spikes are surprises.

**And there is a deep product decision that is really an engineering one: what to do with the people you
cannot serve.** A hundred thousand people, a thousand seats. **Ninety-nine thousand of them are going to be
disappointed, and the design is about how.** Rejecting them in fifty milliseconds with a clear message is a
much better system than making them all wait thirty seconds for a timeout.

By the end of this lesson you can design seat locking under extreme contention, run the sale-opening spike,
handle the hold-and-pay flow, prevent bots, and size the whole thing.

---

## 2. The story

The cinema had two hundred and forty seats and one glass window and Munuswamy sat behind it for nineteen
years, and the only day that mattered was the first day of a big picture.

**Ordinary days the queue was a queue.** You came, you asked, he tore the tickets from the book, you paid, you
went in.

**On a first day there were four hundred people and the queue was not a queue.**

And the thing that went wrong in the early years, the thing that caused the trouble, was not running out.
**Running out was fine.** People understood running out.

**What caused the trouble was selling the same seat twice.**

Because a man would ask for two in the middle, and Munuswamy would look at the chart, and see that H14 and H15
were free, **and then the man would count his money, or go to fetch his wife, or argue about the price**, and
in that time the boy at the second window had sold H14 to somebody else.

**Two people, one seat, both holding a ticket, and the picture starting in eleven minutes.**

**The rule he made was small and it changed everything.** The moment he said a seat aloud, **he put a pin in
it on the chart.** Not sold. Pinned. And the pin meant nobody else could say that seat.

**And the pin came out after two minutes if the money did not arrive**, which he timed by the clock on the
wall behind him, because otherwise a man who wandered off would hold the best seats in the house all evening.

Two minutes was short and people complained, **and on a first day it had to be short, because there were four
hundred people and the pins were the only thing standing between him and the eleven-minutes-to-showtime
argument.**

The second thing took him longer, and it was about the queue rather than the chart.

**He started saying "sold out" before it was sold out.**

Not lying. **When there were forty seats and two hundred people still waiting, he would walk down the line and
tell everybody past about the sixtieth that there was nothing.** They were annoyed and they went home, **and
they were much less annoyed than the ones who had queued for forty minutes and reached the window and been
told no.**

**"The number I cannot change,"** he told his nephew. **"What I can change is how long somebody waits to find
out."**

---

## 3. The idea in plain English

Munuswamy's pin is a distributed lock with a TTL, his two-minute clock is the hold expiry, and his walk down
the queue is the waiting room. **All three are the design.**

**Start with what makes this different from ordinary inventory.**

```
   ORDINARY STOCK                    TICKETS
   units are interchangeable         each unit is UNIQUE
   oversell -> back-order, apologise oversell -> two people, one seat
   demand is spread over time        demand is a SPIKE at a known time
   "one left" is a number            "one left" is seat H14, specifically
```

**Two consequences.** **You cannot use a counter** — "997 seats remaining" does not tell anyone which ones, and
the customer is choosing a specific seat on a map. **And you cannot recover from overselling**, so the
correctness bar is absolute in a way it is not for a warehouse.

**Now the core mechanism, which is the hold.**

**A seat has three states**, exactly like yesterday's inventory but per-unit:

```
   available     nobody has it
   held          somebody is paying for it, with a TTL
   sold          paid for
```

**Selecting a seat holds it.** **Paying converts the hold to a sale.** **An expired hold releases it.**

**And the TTL is the entire safety mechanism**, because **nobody sends "I have given up"** — the browser tab
closes, the phone battery dies, the network drops. **A hold without an expiry is a seat lost forever.**

**The hold must be atomic.** Two people clicking H14 at the same instant is the whole problem, **and a
check-then-write loses it.** The correct forms are the same as yesterday's:

```
   Redis:     SET seat:show:H14 <session> NX EX 300
              -> succeeds only if nobody holds it

   Postgres:  UPDATE seats SET status='held', session=?, expires=?
               WHERE show=? AND seat='H14' AND status='available'
              -> then check rows_affected == 1
```

**Both are one operation.** **`SET NX` and a conditional `UPDATE` do the check and the write together**, which
is the property that makes them safe.

**And two people wanting adjacent seats introduces a second problem.** **A group booking of four seats is four
locks, and acquiring them one at a time can deadlock** — two sessions each holding two of the four. **The fix
is to acquire in a fixed order** — sorted by seat identifier — **so two sessions contending for the same seats
always contend in the same sequence, and one simply fails.**

**Now the spike, which is what makes ticketing hard.**

**A hundred thousand people at ten o'clock, for a thousand seats.**

**The single most important idea is that ninety-nine percent of those requests must never reach the seat
map.** Every one that does is contention on a resource that cannot serve it.

**Three layers, in order of how much they help.**

**A waiting room.** Munuswamy walking down the line. **Requests arriving at the sale opening are given a queue
position and a token**, and admitted to the actual booking system at a controlled rate. **A hundred thousand
people become a thousand at a time.**

**And the honest framing: this makes the wait visible rather than making it shorter.** **A visible position in
a queue is enormously better than a spinner and a timeout**, which is a product truth as much as an engineering
one.

**Fair admission.** First-come-first-served rewards fast networks and bots. **Randomised admission from
everyone who arrived within a short window is fairer**, and several real systems do exactly this.

**And rejecting early.** When there are more people admitted than seats remaining, **tell the rest immediately.**
Munuswamy's "sold out" before it was sold out. **The number cannot change; the time to find out can.**

**Then the seat map, which is a read problem with an unusual property.**

**Everybody wants to see the same thing at the same moment, and it changes constantly.**

**Serve the map from a cache, and accept that it is a few seconds stale.** A seat shown as available that is
actually held is **not a correctness problem** — the atomic hold rejects the attempt and the client refreshes.
**Trying to make the map real-time for a hundred thousand viewers is the mistake**, because the authoritative
check happens at hold time anyway.

**What is worth doing is pushing updates rather than polling.** **One WebSocket broadcast per seat change to
everyone viewing that show** is far cheaper than a hundred thousand clients polling every two seconds.

**Then payment, which inherits yesterday's design.**

**Hold, then authorise, then confirm the hold is still valid, then capture.** The hold TTL must comfortably
exceed the payment time, **and if the hold expires mid-payment — which happens — the honest response is to void
the authorisation and tell the customer**, not to sell a seat that has been taken.

**And bots, which are a first-class problem here rather than a nuisance.**

**Tickets have resale value**, so there is real money in automating purchases. **The defences are layered**:
rate limits per account and per address, a limit on tickets per person, requiring account age or verification,
device fingerprinting, and a challenge at the waiting-room boundary rather than at checkout.

**And none of them work perfectly**, which is worth saying. **The realistic goal is to make automation
expensive enough that it does not dominate**, not to eliminate it.

**Finally: the thing that is genuinely unresolvable.**

**Overselling is unacceptable and underselling is invisible.** A held seat that is never paid for and expires
thirty seconds after the show sells out **is a seat that went empty while somebody wanted it.**

**Short TTLs reduce that waste and break more slow payments.** **Long TTLs are kind to slow customers and hold
seats out of circulation.** There is no correct answer, **and the honest design states the trade rather than
pretending a number is derived.**

---

## 4. The picture

Why a counter does not work:

```
   ORDINARY STOCK                    TICKETS

   "997 units available"             seat map:
   -> decrement to 996                 A1 A2 A3 [A4] A5 ...
   -> any unit will do                 B1 [B2] [B3] B4 ...
                                       ^^^^ specific, chosen, unique

   one atomic counter                 ONE LOCK PER SEAT
   contention on ONE row              contention on the FEW GOOD SEATS
                                      (the front rows go first —
                                       the load is not uniform)
```

The three states and the pin:

```
                  select a seat
   [ AVAILABLE ] --------------> [ HELD ]  (TTL 5 minutes)
        ^                            |
        |                            | pay
        | TTL expires                v
        +-------------------------[ SOLD ]
          (tab closed, battery
           died, network dropped)

   THE TTL IS THE ENTIRE SAFETY MECHANISM.
   Nobody sends "I have given up". The browser just stops existing.
   A hold without an expiry is a seat lost forever.
```

The hold must be atomic:

```
   BROKEN — check then write

     A: is H14 free?  -> yes
     B: is H14 free?  -> yes           <- both see free
     A: mark H14 held
     B: mark H14 held                  <- BOTH HOLD IT
     -> two people pay for one seat

   CORRECT — one operation

     SET seat:show42:H14 <session> NX EX 300
       A: OK        -> A holds it
       B: nil       -> B is told to pick another

     or:  UPDATE seats SET status='held', ...
           WHERE seat='H14' AND status='available'
          then check rows_affected == 1

   The condition and the write happen TOGETHER. That is the property.
```

Group bookings, and the deadlock:

```
   session A wants  H14 H15 H16 H17
   session B wants  H16 H17 H18 H19

   ACQUIRED IN ARRIVAL ORDER:
     A locks H14, H15          B locks H18, H19
     A wants H16 ...           B wants H17 ...
     A waits for B             B waits for A          <- DEADLOCK

   ACQUIRED IN SORTED ORDER (always ascending by seat):
     A locks H14, H15, H16, H17
     B tries H16 -> fails immediately -> releases H18, H19, retries

   -> one fails fast instead of both waiting forever.
      A fixed global order is the standard fix, and it is one `sorted()`.
```

The spike, and the three layers:

```
   10:00:00 — 100,000 people, 1,000 seats

   WITHOUT A WAITING ROOM:
     100,000 requests -> the seat map -> the lock store
     the good seats are a few dozen keys
     -> everything queues, everything times out, everyone retries
     -> the retries are worse than the original load

   WITH THE THREE LAYERS:

     [ 100,000 arrive ]
             |
     1. WAITING ROOM: issue a position + token, admit ~1,000 at a time
             |          -> the booking system sees a manageable rate
             v
     2. FAIR ADMISSION: randomise within the arrival window
             |          -> not a reward for a fast network or a bot
             v
     3. REJECT EARLY: once admitted > seats remaining, tell the rest NOW
             |          -> Munuswamy walking down the line
             v
     [ ~2,000 reach the seat map ]

   "The number I cannot change. What I can change is how long
    somebody waits to find out."
```

The seat map: stale is fine, and why:

```
   100,000 people watching the same map, changing every millisecond

   REAL-TIME FOR EVERYONE:  impossible, and unnecessary
   CACHED, ~2 SECONDS OLD:  fine

   because a seat shown as free that is actually held is NOT a
   correctness problem:
     - the client attempts the hold
     - the ATOMIC hold rejects it
     - the client refreshes and picks another

   the authoritative check happens at HOLD time, not at DISPLAY time.

   AND: push changes over a WebSocket rather than letting 100,000
   clients poll every 2 seconds
     polling:  100,000 / 2s = 50,000 requests/second
     pushing:  ~50 seat changes/second, broadcast
     -> 1,000x fewer operations
```

The TTL trade, which has no correct answer:

```
   SHORT TTL (2 minutes)          LONG TTL (10 minutes)

   seats return to sale fast      slow customers succeed
   more failed payments           seats sit unavailable
   less waste at sell-out         more waste at sell-out

   AND THE ASYMMETRY:
     overselling   -> visible, unacceptable, unrecoverable
     underselling  -> invisible: an empty seat somebody wanted

   -> there is no derived answer. State the trade; pick a number;
      measure the failed-payment rate and the expired-hold rate,
      and move it.
```

---

## 5. How it actually works

### Holding a seat

```python
HOLD_SECONDS = 300

def hold_seat(show_id: int, seat: str, session_id: str) -> bool:
    """Atomic. SET NX is the check and the write in one operation."""
    return bool(redis.set(f"hold:{show_id}:{seat}", session_id,
                          nx=True, ex=HOLD_SECONDS))


def release_seat(show_id: int, seat: str, session_id: str) -> bool:
    """Only the holder may release it — check-and-delete must be atomic."""
    script = """
        if redis.call('GET', KEYS[1]) == ARGV[1] then
            return redis.call('DEL', KEYS[1])
        else
            return 0
        end
    """
    return bool(redis.eval(script, 1, f"hold:{show_id}:{seat}", session_id))
```

**`nx=True` is the whole correctness argument**: the key is set only if it does not exist, **and that check
happens inside Redis rather than in your code.**

**The release must be a Lua script**, not a `GET` followed by a `DEL`. **Between the two, the hold could expire
and somebody else could acquire it** — and your `DEL` would then release *their* hold. **That is the classic
distributed-lock bug** from [day 127](../day-127-graph-bfs/README.md), and it is why the value is a session id
rather than a flag.

### Group bookings, in a fixed order

```python
def hold_seats(show_id: int, seats: list[str], session_id: str) -> list[str]:
    """All or nothing. Acquire in SORTED order to make deadlock impossible."""
    acquired: list[str] = []
    for seat in sorted(seats):                # the fixed global order
        if hold_seat(show_id, seat, session_id):
            acquired.append(seat)
        else:
            for held in acquired:             # roll back cleanly
                release_seat(show_id, held, session_id)
            return []
    return acquired
```

**`sorted(seats)` is the deadlock prevention**, and it is one word. **Two sessions contending for overlapping
seats now always contend in the same sequence**, so one fails immediately rather than both waiting.

**And the rollback matters**: a partial hold that is never released takes seats out of sale for the whole TTL,
**which at sell-out is seats that go empty.**

### The waiting room

```python
def enter_queue(show_id: int, user_id: int) -> dict:
    token = str(uuid.uuid4())
    position = redis.rpush(f"queue:{show_id}", token)
    redis.setex(f"token:{token}", 3600, user_id)
    return {"token": token, "position": position,
            "estimated_wait_seconds": position // ADMIT_PER_SECOND}


def admit_batch(show_id: int, count: int) -> None:
    """Runs continuously. Admits a controlled number per second."""
    tokens = redis.lpop(f"queue:{show_id}", count)
    for token in tokens or []:
        redis.setex(f"admitted:{token}", 900, "1")     # 15 minutes to book
        notifier.push(token, {"admitted": True})
```

**Returning the position is the product decision that matters most.** **A number that counts down is
qualitatively different from a spinner**, even when the wait is identical — and it is the difference between a
user who waits and one who reloads twenty times, adding to the load.

**And `admit_batch` running at a fixed rate is what protects everything downstream** — the booking system never
sees more than it can handle, **regardless of how many people arrived.**

### Fair admission

```python
def admit_fairly(show_id: int, window_seconds: int = 60, count: int = 1000):
    """Randomise within an arrival window: not a race, and not a bot reward."""
    arrivals = redis.zrangebyscore(
        f"arrivals:{show_id}", time.time() - window_seconds, time.time())
    chosen = random.sample(arrivals, min(count, len(arrivals)))
    for token in chosen:
        redis.setex(f"admitted:{token}", 900, "1")
        redis.zrem(f"arrivals:{show_id}", token)
```

**Random sampling within a window removes the reward for a fast connection**, which is what pure
first-come-first-served gives — **and which is exactly the advantage a bot has.**

**It is not perfectly fair either**, and it is fairer than a race, and **saying which unfairness you chose is
better than pretending there is a fair option.**

### The seat map, cached and pushed

```python
def seat_map(show_id: int) -> dict:
    cached = redis.get(f"map:{show_id}")
    if cached:
        return json.loads(cached)                      # up to 2 seconds stale
    seats = db.query("SELECT seat, status FROM seats WHERE show_id = %s", show_id)
    payload = {"seats": {s.seat: s.status for s in seats}, "at": time.time()}
    redis.setex(f"map:{show_id}", 2, json.dumps(payload))
    return payload


def on_seat_changed(show_id: int, seat: str, status: str) -> None:
    """One broadcast per change beats 100,000 clients polling."""
    bus.publish(f"show:{show_id}", {"seat": seat, "status": status})
```

**A two-second cache is not a compromise on correctness**, because **the authoritative check is the atomic
hold.** A stale map produces a failed hold and a refresh, which is a fine outcome.

**And the push-versus-poll arithmetic is stark**: fifty seat changes a second broadcast, against a hundred
thousand clients polling every two seconds. **A thousandfold difference for the same information.**

### The booking flow

```python
def book(show_id: int, seats: list[str], session_id: str,
         payment_token: str, idempotency_key: str) -> dict:
    if not redis.get(f"admitted:{session_id}"):
        return {"error": "not_admitted"}, 403

    held = hold_seats(show_id, seats, session_id)
    if not held:
        return {"error": "seats_unavailable"}, 409

    auth = payments.authorise(price_of(show_id, held), payment_token,
                              idempotency_key=f"auth:{idempotency_key}")
    if not auth.ok:
        for seat in held:
            release_seat(show_id, seat, session_id)
        return {"error": "payment_declined"}, 402

    if not still_held(show_id, held, session_id):       # the TTL may have lapsed
        payments.void(auth.id)                          # free, invisible
        return {"error": "hold_expired"}, 409

    with db.transaction():
        db.execute("""UPDATE seats SET status='sold', booking_id=%(b)s
                       WHERE show_id=%(s)s AND seat = ANY(%(seats)s)
                         AND status <> 'sold'""",
                   {"b": booking_id, "s": show_id, "seats": held})
        booking = booking_store.create(show_id, held, session_id, idempotency_key)

    payments.capture(auth.id, idempotency_key=f"capture:{idempotency_key}")
    for seat in held:
        on_seat_changed(show_id, seat, "sold")
    return {"booking_id": booking.id, "seats": held}
```

**`still_held` after authorisation is the check people omit.** **Payment takes seconds and the hold can lapse
in that window** — rarely, and it happens. **Voiding the authorisation and telling the customer is the honest
response**; selling a seat somebody else now holds is not.

**And the database write is the durable record**, with Redis holding the *hold* and Postgres holding the
*sale* — **two stores with two different jobs, and the `status <> 'sold'` guard is the last line of defence.**

### Releasing expired holds

```python
def sweep_expired(show_id: int) -> int:
    """Redis expires the keys; this reconciles the durable seat map."""
    released = 0
    for seat in db.seats_in_state(show_id, "held"):
        if not redis.exists(f"hold:{show_id}:{seat.seat}"):
            db.execute("""UPDATE seats SET status='available'
                           WHERE show_id=%(s)s AND seat=%(seat)s
                             AND status='held'""",
                       {"s": show_id, "seat": seat.seat})
            on_seat_changed(show_id, seat.seat, "available")
            released += 1
    return released
```

**Redis expires the hold automatically; the durable seat map does not know.** **This job reconciles them**, and
without it the database shows seats as held forever while Redis has released them — **which is underselling
that nobody notices.**

### Bot defences, layered

```python
def can_attempt(user_id: int, show_id: int, ip: str) -> tuple[bool, str]:
    if account_age_days(user_id) < 1:
        return False, "account_too_new"
    if bookings_for_show(user_id, show_id) >= MAX_PER_PERSON:
        return False, "limit_reached"
    if not rate_limiter.allow(f"user:{user_id}", limit=5, per=60):
        return False, "too_many_attempts"
    if not rate_limiter.allow(f"ip:{ip}", limit=20, per=60):
        return False, "too_many_from_address"
    return True, ""
```

**Layered, because none of them works alone.** Account age defeats trivial scripts; **per-person limits are
the most effective and the most easily defeated by many accounts**; IP limits are crude because a whole office
shares one address.

**And the challenge belongs at the waiting-room boundary rather than at checkout**, because **making somebody
solve a puzzle after they have chosen their seats is the worst possible moment.**

### The real systems

```
Redis            holds (SET NX EX), the queue, the cached seat map
PostgreSQL       the durable seat map, bookings, payments
Kafka / NATS     seat-change broadcasts to connected clients
WebSockets       pushing map updates instead of polling
Ticketmaster,    all use a waiting room ("Smart Queue"), all use
BookMyShow,      short holds, all limit tickets per person
IRCTC            Tatkal is the extreme case: a known-in-advance
                 spike of millions in one second
Stripe / etc.    payments, with authorise/capture as yesterday
```

**IRCTC's Tatkal is worth naming**, because it is the largest predictable booking spike in the world and it
illustrates the point exactly: **the time is published in advance, so everything about the system can be
prepared for it.**

---

## 6. The numbers

**Ordinary load against the spike, which is the whole story.**

```
ORDINARY DAY
  ~1,000,000 bookings/day = ~12/second average
  seat map views: ~10,000,000/day = ~120/second
  -> a small system

SALE OPENING (a popular event)
  100,000 people in the first 10 seconds
  = 10,000 requests/second, against ~12/second normally
  -> 800x the ordinary rate, for 60 seconds

AND IT IS PREDICTABLE: the sale opens at a published time.
-> pre-scale, pre-warm caches, pre-shard, staff the incident channel.
   A predictable spike is a completely different problem from a
   surprise one.
```

**Contention, which is where a naive design dies.**

```
1,000 seats, 100,000 people

WITHOUT a waiting room:
  every request reads the seat map and attempts a hold
  the GOOD seats are maybe 50 keys
  -> ~2,000 attempts per good seat, in one second
  -> Redis handles the ops; the RETRIES are what kills it:
     99% fail, every one retries, the load doubles

WITH a waiting room admitting 1,000 at a time:
  ~1,000 concurrent seat-map views
  ~1,000 hold attempts against 1,000 seats
  -> contention is roughly 1:1. Comfortable.

-> the waiting room is not a nicety. It is what makes the
   arithmetic work.
```

**Hold storage.**

```
one hold: key ~40 bytes + session id ~40 = ~100 bytes with overhead

peak concurrent holds for a big event: ~5,000
5,000 x 100 B = 500 KB

-> trivial. The holds are not a storage problem; they are a
   CONTENTION problem.
```

**Seat map: push against poll.**

```
100,000 clients watching one show

POLLING every 2 seconds:
  100,000 / 2 = 50,000 requests/second
  each returns ~20 KB of seat map
  = 1 GB/second of egress    <- for one show

PUSHING changes over WebSockets:
  ~50 seat changes/second during the rush
  broadcast to 100,000 connections
  each message ~50 bytes
  = 50 x 100,000 x 50 B = 250 MB/second

  and with DELTA batching (one message per 500 ms with all changes):
  = 2 x 100,000 x 500 B = 100 MB/second

-> 10x better, and the connection count is the real cost:
   100,000 WebSockets at ~10 KB each = 1 GB of RAM. One machine.
```

**The TTL trade, quantified.**

```
1,000 seats, 5-minute holds, ~20% of holds abandoned

with a 5-minute TTL:
  200 abandoned holds x 5 minutes = 1,000 seat-minutes unavailable
  during a 10-minute sell-out, that is 100 seats' worth of time
  -> some of those seats go EMPTY

with a 2-minute TTL:
  200 x 2 = 400 seat-minutes
  but the payment failure rate rises — slow customers, 3-D Secure
  challenges, bank apps — perhaps from 5% to 15%

-> 10% more failed payments to recover 600 seat-minutes.
   There is no derived answer. Measure both rates and move the number.
```

**Payment latency against the hold.**

```
authorise:  500-2,000 ms
3-D Secure: 10-60 SECONDS (the bank's app, the customer's phone)

-> a 2-minute hold is genuinely tight when 3-D Secure is involved
-> and it is why "hold expired mid-payment" is a real code path
   rather than a theoretical one
```

**Database load at the moment of sale.**

```
1,000 seats sold in 60 seconds = ~17 sales/second
each sale: one seat UPDATE + one booking INSERT + payment rows
= ~70 writes/second

-> TRIVIAL. The durable write path is never the bottleneck.

The bottleneck is entirely:
  1. the number of requests reaching the system  (waiting room)
  2. contention on the popular seats             (atomic holds)
  3. serving the seat map to viewers             (cache + push)
```

**That is worth stating plainly**: **the part that must be durable and correct is tiny**, exactly as in
payments — **and everything expensive is upstream of it.**

**Bot impact, roughly:**

```
for a high-demand event, industry estimates put automated
purchasing at 20-40% of attempts

per-person limits are the most effective single defence:
  limit 4 per person -> a bot needs 250 accounts for 1,000 tickets
  account age >= 1 day -> those accounts must exist in advance

-> the goal is to make automation EXPENSIVE, not impossible.
   Claiming to eliminate it is not credible.
```

---

## 7. The trade-offs

**Hold TTL: short against long.** Short returns seats to sale quickly and **breaks more slow payments** —
especially with 3-D Secure, which can take a minute of the customer's time in their bank's app. Long is kind
to slow customers and **holds seats out of circulation during exactly the window when they are scarce.**
**Overselling is unacceptable and underselling is invisible**, so the pressure is all one way and the number
drifts long unless somebody measures the expired-hold rate.

**Waiting room against open access.** A waiting room protects everything downstream and **makes the wait
explicit**, which users tolerate far better than a spinner. **It also adds a component that must itself survive
the spike**, and if it fails the whole sale fails. **A queue that is the single point of failure for a
high-profile sale needs more care than the booking system it protects.**

**First-come-first-served against randomised admission.** FCFS is what users expect and **rewards fast
networks, proximity to the data centre, and bots.** Randomised admission within a window is fairer and
**feels arbitrary** — a user who clicked at exactly ten o'clock and lost to someone who clicked at ten
o'clock and three seconds finds it hard to accept. **Neither is fair; choose which unfairness and say so.**

**Cached seat map against real-time.** Cached is the only thing that scales and **shows seats that are already
gone**, producing failed hold attempts. That is acceptable **because the atomic hold is the authority**, and
trying to make the display authoritative is the mistake. **The cost is user frustration**, mitigated by pushing
changes rather than lengthening the cache.

**Per-person limits against revenue.** Limits are the most effective bot defence and **turn away legitimate
group bookings** — a family of six against a limit of four. **Every exception mechanism is also a bot
loophole**, which is why the limits tend to be blunt.

**Holds in Redis against holds in the database.** Redis gives atomic operations at the required rate and TTLs
for free, **and it is a second source of truth that can disagree with the durable seat map** — hence the
reconciliation sweep. **Postgres-only is simpler and correct and serialises on hot rows**, which at ten
thousand requests a second is the thing you were trying to avoid.

**When would I not build this?** **When the event is small and the demand is not spiky** — a hundred-seat
theatre selling over three weeks needs a table and a transaction, and every mechanism here is overhead.
**When a platform exists**: Ticketmaster, BookMyShow and Eventbrite have solved the spike, the bots and the
payments, **and the waiting room alone is a serious piece of engineering.** **Building your own is justified by
volume, by unusual seating rules, or by needing the customer relationship** — and that last one is a business
reason, which is fine as long as it is stated as one.

---

## 8. In the interview

### How it gets asked

- *"Design Ticketmaster."* or *"Design a seat booking system."* — the standard prompts.
- *"Two people click the same seat at the same moment. What happens?"* — the central question.
- *"A hundred thousand people arrive when the sale opens. What breaks?"*
- *"How long do you hold a seat, and why?"*
- *"How do you show the seat map to everyone?"*
- *"How do you stop bots?"*

### The first ninety seconds

> "The thing that makes this different from ordinary inventory is that **every unit is unique and
> non-substitutable.** You cannot ship an equivalent seat. **So there is no oversell recovery** — with a
> warehouse you apologise and back-order; **with a seat there is one, and somebody is standing in the aisle.**
>
> **And the contention is extreme and predictable.** A hundred thousand people for a thousand seats, at a time
> that is published in advance. **Predictability is a gift** — I can pre-scale, pre-warm and queue, which is
> not available for a spike that surprises me.
>
> **The core mechanism is a hold with a TTL.** A seat has three states: available, held, sold. **Selecting
> holds it, paying converts it, expiry releases it.**
>
> **The hold must be atomic** — two people clicking the same seat is the entire problem — **so it is a `SET NX`
> in Redis or a conditional `UPDATE` checking the affected row count.** The condition and the write happen
> together; a check-then-write loses the race.
>
> **And the TTL is the whole safety mechanism, because nobody sends 'I have given up'.** The tab closes, the
> battery dies. **A hold without an expiry is a seat lost forever.**
>
> **Now the part I would spend most time on: the spike.**
>
> **A hundred thousand requests for a thousand seats means ninety-nine percent of them must never reach the
> seat map.** Every one that does is contention on a resource that cannot serve it — **and worse, they all fail
> and all retry, so the load doubles.**
>
> **Three layers. A waiting room** that gives everyone a position and admits perhaps a thousand at a time.
> **Fair admission** — randomised within an arrival window, rather than a race that rewards fast networks and
> bots. **And rejecting early**: once more people are admitted than there are seats, tell the rest immediately.
>
> **The number of disappointed people is fixed. What the design controls is how long they wait to find out** —
> and a visible queue position is enormously better than a spinner and a timeout.
>
> **One thing I would flag early: the seat map is cached and stale, and that is correct.** A seat shown as free
> that is actually held is not a correctness problem — **the atomic hold rejects it and the client refreshes.**
> The authoritative check is at hold time, not at display time."

### The follow-ups

**"Two people click the same seat at the same moment. What happens?"**

> "One gets it and the other is told immediately, **and the mechanism is a single atomic operation** — that
> single-operation property is the whole answer.
>
> **The broken version is a check followed by a write.** Is H14 free? Yes. Mark it held. **Two requests
> overlapping by a few milliseconds both see 'free', both mark it, and two people pay for one seat.**
>
> **And unlike a warehouse, there is no recovery.** You cannot ship an equivalent seat. Somebody arrives and
> somebody else is in their chair.
>
> **The fix is `SET key value NX EX 300`.** The key is set only if it does not exist, **and the check happens
> inside Redis rather than in my code**, so there is no window between them. The second request gets nil and is
> told to pick another seat.
>
> **The Postgres equivalent is a conditional update** — `SET status='held' WHERE seat=? AND status='available'`
> — **and then checking that exactly one row was affected.** Same property: the condition and the write are one
> operation.
>
> **Two details I would add, because they are where the real bugs are.**
>
> **The release must also be atomic, and it must check ownership.** A `GET` followed by a `DEL` is broken:
> between them, the hold can expire and somebody else can acquire it, **and your `DEL` then releases their
> hold.** So the value stored is a session id and the release is a Lua script that deletes only if the value
> matches.
>
> **And group bookings can deadlock.** Four adjacent seats is four locks, and two sessions wanting overlapping
> sets can each hold half and wait for the other. **The fix is to always acquire in sorted order** — one
> `sorted()` call — **so two contending sessions always contend in the same sequence and one fails
> immediately** rather than both waiting.
>
> **And a partial acquisition must roll back cleanly**, or seats sit unavailable for the whole TTL at exactly
> the moment they are scarce."

**"A hundred thousand people arrive when the sale opens. What breaks?"**

> "Everything, if they all reach the booking system — **and the failure is worse than it first appears because
> of retries.**
>
> **The direct problem: a hundred thousand requests want a thousand seats**, and the *good* seats are maybe
> fifty keys. That is two thousand attempts per popular seat in one second. **Redis can do the operations —
> what it cannot absorb is that ninety-nine percent fail, every one of those users retries, and the load
> doubles.**
>
> **So the design principle is that almost none of them should reach the seat map at all.**
>
> **Layer one: a waiting room.** Arrivals get a token and a position, and a background process admits a
> controlled number per second. **A hundred thousand people become a thousand at a time**, and the booking
> system never sees more than it can handle regardless of how many arrived.
>
> **And returning the position is the design decision that matters most**, and it is a product one. **A number
> that counts down is qualitatively different from a spinner**, even when the wait is identical — and a user
> who can see progress does not reload twenty times and add to the load.
>
> **Layer two: fair admission.** Pure first-come-first-served rewards a fast network, physical proximity to the
> data centre, and automation. **Randomised admission from everyone who arrived within a short window removes
> that advantage.** It is not perfectly fair either — **I would say which unfairness I chose rather than claim
> a fair option exists.**
>
> **Layer three: reject early.** Once more people have been admitted than there are seats remaining, **tell
> everyone else immediately.** The number of disappointed people is fixed by the seat count; **what I control
> is whether they find out in fifty milliseconds or after thirty seconds of timeouts.**
>
> **And because the spike is predictable — the sale time is published — I can prepare**: pre-scale the fleet,
> pre-warm the seat-map cache, pre-establish the WebSocket capacity. **A predictable spike is a completely
> different problem from a surprise one**, and I would take full advantage of that.
>
> **One risk I would flag: the waiting room is now a single point of failure for a high-profile sale.** If it
> falls over, the whole event fails publicly. **It needs more operational care than the booking system it
> protects**, which is slightly uncomfortable and is true."

**"How long do you hold a seat, and why?"**

> "There is no derived answer, and I think the honest thing is to say that and then explain the trade — because
> the pressure runs one way and the failure it causes is invisible.
>
> **Too short and you break slow payments.** The customer is entering card details, or their bank has sent
> them to an app for 3-D Secure, **which routinely takes thirty to sixty seconds of the customer's own time.**
> A two-minute hold is genuinely tight in that case.
>
> **Too long and seats sit out of circulation.** With a five-minute hold and twenty percent abandonment, a
> thousand-seat event accumulates a thousand seat-minutes of unavailability — **and during a ten-minute
> sell-out, that is seats that go empty while people were still trying to buy.**
>
> **And here is the asymmetry that makes this hard.** **Overselling is visible, unacceptable and
> unrecoverable. Underselling is invisible** — nobody ever sees the empty seat that somebody wanted.
>
> **So the incentive is entirely towards longer holds**, and the number drifts up unless somebody actively
> measures the expired-hold rate against the failed-payment rate.
>
> **What I would build is: five minutes as a starting point, and both metrics on a dashboard** — the fraction
> of holds that expire unpaid, and the fraction of payments that fail because the hold lapsed. **Move the
> number based on those, and expect it to differ by event type.**
>
> **Two mechanisms that soften it.** **Extend the hold when the payment is genuinely in flight** — once the
> authorisation is submitted, the customer is not idle, so the clock can be paused. **And show the customer
> the countdown**, which both reduces abandonment and makes the expiry feel fair rather than arbitrary.
>
> **And the code path for 'the hold expired mid-payment' has to exist.** It is rare and it happens, **and the
> honest response is to void the authorisation — which is free — and tell the customer**, rather than sell a
> seat that somebody else now holds."

### The model answer

*"Design a ticket booking system for a large events platform: ten thousand events, seat-level selection, and
sales that open at a published time with a hundred thousand people waiting."*

> "Let me name what makes this different from ordinary inventory, because it determines everything.
>
> **Every unit is unique and non-substitutable, so there is no oversell recovery.** And **the contention is
> both extreme and predictable** — a hundred thousand people at a published time. **Predictability is the one
> advantage I have and I would use all of it.**
>
> **Ordinary load is tiny**: a million bookings a day is twelve a second. **The sale opening is ten thousand
> requests a second — eight hundred times the normal rate, for about a minute.** So this is a system designed
> entirely around sixty seconds a day.
>
> **The core mechanism is a per-seat hold with a TTL**, in Redis via `SET NX EX`. **Atomic**, because two
> people clicking H14 is the whole problem and a check-then-write loses it. **The value is a session id and
> the release is a Lua script**, because a `GET` then `DEL` can release somebody else's hold after an expiry.
> **Group bookings acquire in sorted seat order** to make deadlock impossible, and roll back cleanly on
> partial failure.
>
> **The durable seat map and the bookings are in Postgres**, with a `status <> 'sold'` guard on the final
> update as a last line of defence. **And a sweep job reconciles Redis expiries into the durable map**, without
> which the database shows seats held forever — **underselling that nobody notices.**
>
> **Now the spike, which is most of the design.**
>
> **A waiting room in front of everything.** Arrivals get a token and a **visible position**; a background
> process admits about a thousand at a time. **The booking system never sees more than it can handle.** And the
> position is not decoration — **a countdown is qualitatively different from a spinner**, and it stops users
> reloading and doubling the load.
>
> **Admission is randomised within a short arrival window** rather than first-come-first-served, because FCFS
> rewards fast networks and bots. **It is a different unfairness rather than fairness, and I would say so.**
>
> **And rejection is early and explicit.** Once admissions exceed remaining seats, everyone else is told
> immediately. **The number of disappointed people is fixed; the time they wait to find out is not.**
>
> **The seat map is cached for about two seconds and pushed over WebSockets.** Stale is fine, **because the
> authoritative check is the atomic hold** — a stale map produces a rejected attempt and a refresh. **And
> pushing beats polling by about a thousand times**: fifty seat changes a second broadcast, against a hundred
> thousand clients polling every two seconds, which would be a gigabyte a second of egress for one show.
>
> **Payment inherits the standard design**: hold, authorise, **re-check the hold is still valid**, capture.
> That re-check is the step people omit, **and 3-D Secure can take a minute of the customer's time**, so hold
> expiry mid-payment is a real path rather than a theoretical one. **Void and tell them — never sell a seat
> twice.**
>
> **Bots are a first-class problem here because tickets have resale value.** Layered defences: account age,
> per-person limits, rate limits per account and address, and a challenge **at the waiting-room boundary rather
> than at checkout** — making somebody solve a puzzle after choosing their seats is the worst possible moment.
> **And the goal is to make automation expensive, not to eliminate it**; claiming otherwise is not credible.
>
> **Two closing points.**
>
> **The durable write path is trivial** — a thousand seats in sixty seconds is seventeen sales a second. **All
> the difficulty is upstream: request admission, seat contention, and serving the map.** That is worth saying,
> because it is where the engineering effort should go.
>
> **And the hold TTL has no correct value.** Short breaks slow payments; long wastes seats. **Overselling is
> visible and underselling is invisible**, so the number drifts long unless both rates are measured. **I would
> start at five minutes, put both metrics on a dashboard, and treat it as a number to tune rather than one to
> derive.**"

---

## 9. Recall card

**Every unit is UNIQUE and non-substitutable, so there is NO oversell recovery** — you cannot ship an
equivalent seat. **And the contention is extreme AND predictable**: 100,000 people at a published time, ~800×
the ordinary rate for sixty seconds. **Predictability is the advantage — pre-scale, pre-warm, pre-queue.**

**Three seat states — available / held / sold — and the hold must be ATOMIC:** `SET NX EX` or a conditional
`UPDATE` with a row-count check. **The TTL is the entire safety mechanism, because nobody sends "I gave up".**
**Release must be a Lua script checking a session id** — `GET` then `DEL` can release somebody else's hold
after an expiry. **Group bookings acquire in SORTED order** so contention is always in the same sequence and
one side fails fast instead of deadlocking.

**99% of requests must never reach the seat map** — not because of the operations but because **they all fail,
all retry, and double the load.** Three layers: **a waiting room with a VISIBLE position** (a countdown is
qualitatively different from a spinner), **randomised admission within a window** (FCFS rewards fast networks
and bots — it is a different unfairness, not fairness), and **rejecting early**: the number of disappointed
people is fixed, the time they wait to find out is not.

**The seat map is cached (~2 s) and stale, and that is CORRECT** — the atomic hold is the authority, so a
stale map produces a rejected attempt and a refresh. **Push over WebSockets, never poll**: ~50 changes/second
broadcast against 100,000 clients polling every 2 s (1 GB/s for one show).

**Payment: hold → authorise → RE-CHECK the hold → capture.** 3-D Secure takes 30–60 seconds of the customer's
time, so **"hold expired mid-payment" is a real path** — void (free) and tell them.

**The hold TTL has no derived answer.** Short breaks slow payments; long wastes seats. **Overselling is visible
and underselling is invisible**, so the number drifts long unless you measure the expired-hold rate against the
failed-payment rate. **And the durable write path is trivial (~17 sales/second) — all the difficulty is
upstream.**
