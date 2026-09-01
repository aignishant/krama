---
day: 163
track: system-design
title: "Design an e-commerce system"
phase: "High-level design case studies"
status: written
---

# Design an e-commerce system

## 1. What this is, and why they ask it

An e-commerce system takes a product catalogue, lets people search it, put things in a basket, and pay — **and
then has to actually deliver the thing, which is where the interesting problems are.**

They ask it because **it is the only design in this set where correctness is worth money and mistakes are
visible to customers as a broken promise.** Every other system this month can lose a location point, a
presence update, a view count. **Here, overselling means telling a thousand people they have bought something
that does not exist**, and there is no technical recovery — somebody has to send apologies and refunds.

Three things carry the interview.

**Inventory, which is the hard part and the part candidates underestimate.** "One item left, two people
buying" is a distributed correctness problem with a specific answer, **and the naive read-then-write is wrong
in a way that only appears under load** — which is exactly when it matters.

**The read/write split, which is extreme.** Browsing and searching are enormous and can be slightly stale;
checkout and payment are tiny and must be exactly right. **Those are two different systems and treating them
as one is the main architectural mistake available here.**

**And the order as a long-running process.** An order is not a row — **it is a saga spanning payment,
inventory, warehouse, courier and email, over hours or days, where any step can fail and some cannot be
undone.** That is [day 121](../day-121-trie-operations/README.md)'s saga pattern with real money attached.

By the end of this lesson you can design the catalogue and search, handle inventory correctly under
concurrency, run checkout and payment idempotently, model the order lifecycle, and size it — including the
flash-sale case that breaks everything.

---

## 2. The story

The hardware shop had two rooms and a loft and Prakash's father had run it on memory for thirty-one years,
which worked until it did not.

**The failure, when it came, was small and it changed everything.**

A contractor asked for forty of a particular tap fitting. **Prakash said yes** — he was fairly sure there were
about fifty in the loft — took the money, and promised them for Thursday.

**There were eleven.**

And the contractor had a job depending on it, and Prakash spent a week finding thirty-nine more at three other
shops at a loss, **and the contractor never came back.**

**What he built afterwards took two years and it was four separate things, and he only understood at the end
why they had to be separate.**

**The first was the list on the wall** — everything they sold, with prices. **It changed slowly and everybody
could read it**, including customers, and copies of it went up in both rooms.

**The second was the loft count**, in a notebook that only he touched. **And the rule about that notebook was
the one that mattered: you did not read it and then act. You wrote in it at the moment you promised.**

Because the mistake had been reading a number, going away, thinking about it, and promising. **Somebody else
could have sold twenty in between.**

**The third was the promise itself**, and this was the part he had not expected. When a customer said yes, he
wrote their name against the goods **before** they paid, **and the goods were then not available to anyone
else**, and if the customer walked out without paying, he crossed it out an hour later and the goods came
back.

**Held, not sold. Two different things, and he had been treating them as one.**

**And the fourth was the ledger of what happened afterwards**, because an order was not one moment. It was
taken, then paid, then packed, then collected by the transport, then delivered, **and each of those was a
different day and a different person, and any of them could go wrong.**

His son, who came into the business later and had opinions about computers, once asked why the loft notebook
could not just be part of the wall list.

**"Because the wall is for looking at,"** Prakash said. **"The notebook is for promising. If you get the wall
wrong, somebody is annoyed. If you get the notebook wrong, somebody has paid for something I do not have."**

---

## 3. The idea in plain English

Prakash's four things are the four systems, and his last sentence is the whole architecture: **the catalogue
is for looking at and the inventory is for promising, and they have completely different requirements.**

**Start with the split, because it is the answer to the first question.**

```
   BROWSE / SEARCH                    CHECKOUT / ORDER
   millions of reads/second           thousands of writes/second
   staleness of MINUTES is fine       must be exactly right
   cacheable, CDN-friendly            transactional, not cacheable
   read replicas, search index        the primary database
   losing one is invisible            losing one is a lost sale;
                                      duplicating one is a double charge
```

**A hundred to a thousand reads per write**, and **the two halves want opposite things.** Say that in the
first minute.

**Now the catalogue, which is the easy half.**

**Products, categories, prices, images, descriptions, reviews.** It changes slowly — a price update is an
event, not a stream — **so it can be cached aggressively at every layer**: CDN for images, application cache
for product pages, read replicas for anything dynamic.

**And search is a separate index**, exactly as in [day 154](../day-154-edit-distance/README.md): an inverted
index with faceted filtering — brand, price range, rating, in-stock. **Populated asynchronously**, so a new
product is searchable within seconds rather than milliseconds, which nobody notices.

**The one interesting catalogue decision is where the price lives.** A price shown on a cached page can be
stale. **So the price is re-read at checkout and the customer is shown the difference** — because charging a
price different from the one displayed is a legal problem in most countries, not merely an annoyance.

**Now inventory, which is the hard part.**

**The naive version is wrong and it is worth being precise about why.**

```
   read stock  -> 1 available
   check       -> yes, enough
   write       -> stock = 0

   TWO PEOPLE DOING THAT AT THE SAME TIME BOTH SEE 1 AND BOTH SUCCEED.
```

**That is a read-then-write race**, and it does not show up in testing because it needs two requests inside the
same few milliseconds — **which happens constantly in production and never on a developer's machine.**

**Three correct answers, and they suit different situations.**

**Atomic decrement with a condition.** `UPDATE stock SET qty = qty - 1 WHERE sku = ? AND qty >= 1`, and check
how many rows were affected. **The database does the check and the write as one operation**, so two concurrent
attempts cannot both succeed. **Simple, correct, and it serialises on that row** — which is fine at ordinary
rates and is the bottleneck in a flash sale.

**Optimistic concurrency.** Read the stock and a version number, and write conditionally on the version being
unchanged. **If it changed, somebody else got there first: retry.** Better when conflicts are rare and worse
when they are common, because every conflict is a wasted round trip.

**Pessimistic locking.** `SELECT ... FOR UPDATE`, which holds a row lock for the transaction. **Correct, and it
serialises everything touching that row** — including readers, depending on the isolation level — so it is the
one to avoid on hot items.

**And then the idea that is actually the design: reservations.**

**Prakash's third notebook.** Stock has three states, not two:

```
   available     nobody has claimed it
   reserved      in somebody's basket, at checkout, held with a TTL
   sold          paid for and committed
```

**Adding to a basket reserves nothing.** **Beginning checkout reserves with a short expiry** — fifteen minutes
is typical. **Payment converts the reservation into a sale.** **And an abandoned checkout lets the reservation
expire and the stock return.**

**The TTL is what makes this safe.** A customer who closes the tab mid-payment must not hold the last item
forever, **and no "I gave up" message will ever arrive** — which is the same expiring-state argument as
presence and distributed locks.

**Now checkout and payment, where the requirement is exactly-once and the world only offers at-least-once.**

**The customer clicks "pay". The request times out. Did the payment go through?**

**Nobody knows, including the customer, who will click again.**

**The answer is an idempotency key**, generated by the client when the checkout begins and sent with every
attempt. **The payment service records the key with the result, and a repeat of the same key returns the
original result rather than charging again.** Every real payment provider — Stripe, Razorpay, Adyen — requires
one, and that is why.

**And the key must come from the client at the start of the checkout, not be generated per request**, because
a per-request key differs on the retry and deduplicates nothing.

**Then the order lifecycle, which is a saga rather than a transaction.**

**An order spans payment, inventory, the warehouse, a courier and several emails, over hours or days.** You
cannot hold a database transaction across that, **and several of the steps are in other companies' systems.**

**So: a state machine with explicit transitions, and compensating actions for failures.**

```
  created -> payment_authorised -> inventory_committed -> packed
          -> shipped -> delivered

  and at each step, a specific compensation:
    payment fails            -> release the reservation
    inventory fails          -> VOID the authorisation (do not capture)
    warehouse cannot fulfil  -> REFUND, and apologise
```

**Note that the compensations are not symmetric, and that is the point.** **Voiding an authorisation before
capture is free and invisible.** **Refunding after capture costs fees, takes days to appear, and the customer
notices** — which is why the ordering of the steps matters: **authorise first, commit inventory, capture
last.**

**And two-phase payment is the mechanism that makes that possible.** **Authorisation** reserves the money on
the card without taking it. **Capture** takes it. **The gap between them is where you check inventory**, and
using it correctly is the difference between a clean cancellation and a refund.

**Finally, the flash sale, which breaks every part of this.**

**A hundred thousand people trying to buy a thousand units in the same second.** The catalogue survives —
it is cached. **The inventory row does not**, because every one of those requests wants to decrement the same
row, and a database row serialises.

**Three things, in order of how much they help.**

**Admit fewer requests.** A queue in front of the purchase path, or a randomised waiting room, **so the
database sees a manageable rate rather than a hundred thousand simultaneous attempts.**

**Decrement in memory.** An atomic counter in Redis is the source of truth for the sale, **with the durable
write following asynchronously.** Redis does about a hundred thousand atomic decrements a second, where a
database row does a few thousand.

**And shard the counter.** Split a thousand units into twenty buckets of fifty, **and route each request to a
random bucket** — twenty rows instead of one. **The cost is that a bucket can empty while others have stock**,
so the last few units need a rebalancing pass, **which is a genuine trade rather than a free win.**

**And the honest framing: at flash-sale scale, "sold out" is a better answer than "sorry, we oversold".**
Rejecting requests early is correct behaviour, not a failure.

---

## 4. The picture

The four systems, and why they are separate:

```
   CATALOGUE            SEARCH             INVENTORY          ORDERS
   products, prices     inverted index     stock counts       the saga
   changes slowly       async populated    changes fast       long-running
   CACHE EVERYWHERE     near-real-time     ATOMIC ONLY        state machine
   millions of reads/s  ~100k queries/s    ~10k writes/s      ~1k orders/s
   stale = fine         stale = fine       stale = OVERSOLD   stale = wrong
                                                              status shown

   "the wall is for looking at; the notebook is for promising"
```

The read-then-write race, which is the bug:

```
   time ->
   request A            request B
   ---------            ---------
   read qty = 1
                        read qty = 1        <- both see 1
   qty >= 1? yes
                        qty >= 1? yes       <- both check, both pass
   write qty = 0
                        write qty = 0       <- both write
   "you bought it"      "you bought it"     <- TWO SALES, ONE ITEM

   This needs the two requests to overlap by a few MILLISECONDS.
   It never happens in testing and constantly happens in production.
```

The three correct fixes:

```
  ATOMIC CONDITIONAL UPDATE           OPTIMISTIC CONCURRENCY

  UPDATE stock                        read qty AND version
  SET qty = qty - 1                   ...
  WHERE sku = ? AND qty >= 1          UPDATE stock SET qty = ?, version = v+1
                                      WHERE sku = ? AND version = v
  rows_affected == 1 -> success
  rows_affected == 0 -> sold out      0 rows -> somebody beat me -> RETRY

  the DB does check+write as ONE       good when conflicts are RARE
  operation                            wasteful when they are common
  simple, correct, serialises the row


  PESSIMISTIC LOCK
  SELECT ... FOR UPDATE
  -> holds the row lock for the whole transaction
  -> correct, and serialises EVERYTHING touching that row
  -> the one to avoid on hot items
```

Reservations: three states, not two:

```
                    add to basket
                    (reserves NOTHING)
                          |
   [ AVAILABLE ] ---------+
        ^                 |
        |          begin checkout
        |          (RESERVE, TTL 15 min)
        |                 v
        +---------- [ RESERVED ] ------ payment succeeds ---> [ SOLD ]
          TTL expires
          (customer closed the tab)

  THE TTL IS THE POINT: nobody sends "I gave up".
  A customer who closes the tab mid-payment must not hold the last
  item forever, and no explicit release message will ever arrive.
```

Two-phase payment, and why the order of steps matters:

```
   AUTHORISE  (reserve the money on the card, do not take it)
        |
        v
   COMMIT INVENTORY   <- the check happens HERE, in the gap
        |
        +-- fails --> VOID the authorisation
        |             free, invisible to the customer, instant
        v
   CAPTURE  (take the money)
        |
        +-- warehouse cannot fulfil later --> REFUND
                      costs fees, takes DAYS to appear,
                      the customer definitely notices

  THE COMPENSATIONS ARE NOT SYMMETRIC.
  That asymmetry is why you authorise first, check inventory second,
  and capture last.
```

The idempotency key, and where it must come from:

```
   customer clicks PAY
        |
        +--> request, with key K -----> [ timeout ]
        |                                    |
        |                          did it go through?
        |                          NOBODY KNOWS, including the customer
        v
   customer clicks PAY again
        +--> request, with the SAME key K --> payment service:
                                              "I have seen K.
                                               Here is the original result."
                                              -> NO SECOND CHARGE

  THE KEY MUST BE GENERATED WHEN THE CHECKOUT STARTS, by the client.
  A key generated per REQUEST differs on the retry and deduplicates
  nothing — which is the mistake that looks like a solution.
```

The flash sale, and why a database row is the wall:

```
   100,000 requests, same second, one SKU with 1,000 units

   ONE DATABASE ROW:
     every request wants to decrement it
     the row serialises -> ~3,000 updates/second
     -> 33 seconds of queueing, timeouts, and a stampede of retries

   FIX 1 — ADMIT FEWER:  a queue or a waiting room in front
                         the DB sees a manageable rate

   FIX 2 — DECREMENT IN MEMORY:  Redis DECR is atomic, ~100,000/s
                                 durable write follows asynchronously

   FIX 3 — SHARD THE COUNTER:  1,000 units -> 20 buckets of 50
                               route randomly -> 20 rows, not 1
                               COST: a bucket can empty while others
                               have stock -> the last units need a
                               rebalancing pass

   AND: "sold out" is a BETTER answer than "sorry, we oversold".
        Rejecting early is correct behaviour.
```

---

## 5. How it actually works

### Inventory: the atomic decrement

```python
def reserve_stock(sku: str, quantity: int, reservation_id: str) -> bool:
    with db.transaction():
        rows = db.execute("""
            UPDATE inventory
               SET available = available - %(q)s,
                   reserved  = reserved  + %(q)s
             WHERE sku = %(sku)s AND available >= %(q)s
        """, {"sku": sku, "q": quantity})
        if rows != 1:
            return False                      # not enough — no state changed
        db.execute("""
            INSERT INTO reservations (id, sku, quantity, expires_at)
            VALUES (%(id)s, %(sku)s, %(q)s, now() + interval '15 minutes')
        """, {"id": reservation_id, "sku": sku, "q": quantity})
        return True
```

**`AND available >= quantity` in the `WHERE` clause is the entire correctness argument.** The database
evaluates the condition and performs the write as one atomic operation, **so two concurrent requests cannot
both see enough stock.**

**Checking `rows != 1` rather than reading the new value** is what makes it safe: **the row count tells you
whether *your* update was the one that succeeded.**

**And the reservation row with an expiry is Prakash's third notebook** — held, not sold.

### Releasing expired reservations

```python
def release_expired() -> int:
    """Runs every minute. The TTL is what makes reservations safe."""
    expired = db.execute("""
        DELETE FROM reservations
         WHERE expires_at < now()
         RETURNING sku, quantity
    """)
    for sku, quantity in expired:
        db.execute("""
            UPDATE inventory
               SET available = available + %(q)s,
                   reserved  = reserved  - %(q)s
             WHERE sku = %(sku)s
        """, {"sku": sku, "q": quantity})
    return len(expired)
```

**This job is not optional.** Without it, every abandoned checkout permanently removes stock, **and the store
sells out while the warehouse is full** — a failure that accumulates silently over weeks.

**And it must be idempotent**: the `DELETE ... RETURNING` makes it so, because a reservation can only be
deleted once even if the job runs twice.

### Checkout with an idempotency key

```python
@app.post("/checkout")
def checkout(user_id: int, basket: list, idempotency_key: str) -> dict:
    if existing := order_store.by_idempotency_key(idempotency_key):
        return existing                       # a retry: the same answer

    prices = pricing.current(basket)          # re-read: the page may be stale
    reservation_id = str(uuid.uuid4())
    for line in basket:
        if not reserve_stock(line.sku, line.quantity, reservation_id):
            release_reservation(reservation_id)      # all or nothing
            return {"error": "out_of_stock", "sku": line.sku}, 409

    order = order_store.create(
        user_id=user_id, lines=basket, prices=prices,
        reservation_id=reservation_id,
        idempotency_key=idempotency_key, state="created")
    return {"order_id": order.id, "total": prices.total}
```

**`prices = pricing.current(basket)` is not a detail.** The product page may have been cached for ten minutes,
**and charging a price different from the one displayed is a legal problem** — so the price is re-read and any
difference is shown to the customer before payment.

**And the reservation is all-or-nothing across the basket**: if the third line is out of stock, **the first
two must be released**, or an abandoned checkout holds stock nobody wanted.

### Payment, two-phase

```python
def process_payment(order_id: int) -> str:
    order = order_store.get(order_id)

    auth = payments.authorise(                # reserve the money, do not take it
        amount=order.total, method=order.payment_method,
        idempotency_key=f"auth:{order.idempotency_key}")
    if not auth.ok:
        release_reservation(order.reservation_id)
        order_store.transition(order_id, "payment_failed")
        return "payment_failed"

    order_store.transition(order_id, "payment_authorised")

    if not commit_inventory(order.reservation_id):
        payments.void(auth.id)                # FREE, invisible, instant
        order_store.transition(order_id, "cancelled")
        return "out_of_stock"

    capture = payments.capture(               # NOW take the money
        auth.id, idempotency_key=f"capture:{order.idempotency_key}")
    order_store.transition(order_id, "paid" if capture.ok else "payment_failed")
    return "paid"
```

**Authorise, check inventory, then capture** — and the ordering is the whole design. **Voiding an
authorisation is free and invisible; refunding a capture costs fees and takes days.** So the risky check goes
in the gap between them.

**And the idempotency keys are derived from the order's key**, with a prefix per operation, **so a retried
authorisation does not deduplicate against the capture.**

### Committing the reservation

```python
def commit_inventory(reservation_id: str) -> bool:
    with db.transaction():
        rows = db.execute("""
            DELETE FROM reservations
             WHERE id = %(id)s AND expires_at > now()
             RETURNING sku, quantity
        """, {"id": reservation_id})
        if not rows:
            return False                      # expired while paying — real, and rare
        for sku, quantity in rows:
            db.execute("""
                UPDATE inventory
                   SET reserved = reserved - %(q)s,
                       sold     = sold     + %(q)s
                 WHERE sku = %(sku)s
            """, {"sku": sku, "q": quantity})
        return True
```

**`AND expires_at > now()` handles the genuine race**: the customer took sixteen minutes to enter their card
details and the reservation expired. **It is rare and it happens**, and the code must handle it rather than
assume it away.

### The order saga

```python
TRANSITIONS = {
    "created":            {"payment_authorised", "payment_failed", "cancelled"},
    "payment_authorised": {"paid", "cancelled", "payment_failed"},
    "paid":               {"packed", "refunded"},
    "packed":             {"shipped", "refunded"},
    "shipped":            {"delivered", "returned"},
    "delivered":          {"returned"},
}

COMPENSATIONS = {
    "payment_failed": ["release_reservation"],
    "cancelled":      ["release_reservation", "void_authorisation"],
    "refunded":       ["refund_payment", "restock"],
}


def transition(order_id: int, to_state: str) -> None:
    with db.transaction():
        order = order_store.lock_for_update(order_id)
        if to_state not in TRANSITIONS.get(order.state, set()):
            raise InvalidTransition(f"{order.state} -> {to_state}")
        order_store.update(order_id, state=to_state)
        for action in COMPENSATIONS.get(to_state, []):
            outbox.enqueue(action, order_id)   # same transaction as the state change
```

**The explicit table checked on every write prevents the double-charge**: a retried "paid" on an order already
paid **raises rather than charging again.**

**And `outbox.enqueue` inside the same transaction is the transactional outbox pattern.** Writing the state
change and publishing the event **must be atomic**, or a crash between them leaves an order marked paid with no
warehouse ever told. **A separate process drains the outbox and publishes**, which is at-least-once and
therefore needs the consumers to be idempotent.

### The flash sale path

```python
def flash_sale_purchase(sku: str, user_id: int) -> bool:
    if not rate_limiter.allow(user_id, sku):
        return False                          # one attempt per user

    bucket = random.randrange(SHARDS)         # spread across N counters
    remaining = redis.decr(f"flash:{sku}:{bucket}")
    if remaining < 0:
        redis.incr(f"flash:{sku}:{bucket}")   # put it back
        return try_other_buckets(sku, user_id)

    queue.publish("flash_order", {"sku": sku, "user": user_id})  # durable, async
    return True
```

**`redis.decr` is atomic and returns the new value**, so checking `< 0` is the sold-out test — **no
read-then-write anywhere.**

**Putting it back on failure matters**, because otherwise a rejected request permanently destroys a unit.

**And the durable order is written asynchronously.** The customer is told "yes" on the basis of the Redis
decrement, **and the database write follows** — which is a deliberate choice: **the counter is the source of
truth for the sale, and losing the queue message means an order that must be reconciled, not a lost unit.**

**`try_other_buckets` is the cost of sharding.** With twenty buckets, the last few units end up stranded in
buckets that requests are not landing on, **so a request that finds its bucket empty checks the others before
giving up.**

### The real systems

```
PostgreSQL / MySQL      orders, inventory, payments — a relational
                        database, because this is what transactions
                        are for
Redis                   flash-sale counters, session baskets, caching
Elasticsearch           product search with facets
Kafka                   the event backbone: order events, inventory
                        updates, the outbox drain
Stripe / Razorpay /     payments, all requiring idempotency keys and
Adyen                   all supporting authorise/capture separately
CDN                     product images and cached catalogue pages
```

**"A relational database, because this is what transactions are for" is worth saying explicitly**, since the
instinct after a month of distributed systems is to reach for something scalable — **and the order volume here
is small enough that a single primary handles it, which is a much better answer than a distributed store with
weaker guarantees.**

---

## 6. The numbers

**Traffic, and the split.**

```
100,000,000 monthly users, ~10,000,000 daily
each views ~20 product pages/day       -> 200,000,000 page views/day
                                          = ~2,300/second, peak ~10,000/second

~1% convert to an order                -> ~100,000 orders/day
                                          = ~1.2/second, peak ~50/second

read : write = 2,000 : 1
```

**Two thousand reads per write** — **the browse path is a different system from the order path, by three
orders of magnitude.**

**Catalogue.**

```
10,000,000 products x ~5 KB of metadata = 50 GB
+ images: 10,000,000 x 5 images x 200 KB = 10 TB  -> CDN

the metadata fits in memory on one machine.
-> the catalogue is a CACHING problem, not a storage one.
```

**Search.**

```
~100,000,000 searches/day = ~1,200/second, peak ~5,000/second
index: 10,000,000 products x ~50 terms x 8 bytes = 4 GB
-> comfortably in memory on a few machines
```

**Orders and payments, which is the small, important half.**

```
100,000 orders/day x ~8 state transitions = 800,000 writes/day
                                          = ~10/second, peak ~400/second

order record ~5 KB (lines, addresses, prices, payment refs)
100,000 x 5 KB = 500 MB/day = ~180 GB/year
+ replicas    = ~550 GB/year

-> ONE relational primary handles this comfortably, for years.
   This is the part where correctness matters and the volume is small.
```

**That contrast is the point**: **the half that must be perfect is also the half that is tiny.**

**Inventory writes, and where they concentrate.**

```
ordinary trading:
  ~50 reservations/second at peak, spread over 10,000,000 SKUs
  -> essentially zero contention per row

FLASH SALE:
  100,000 requests in ~1 second, ONE SKU
  a single Postgres row: ~3,000 conditional updates/second
  -> 33 seconds of queueing, timeouts, retry storms

  Redis DECR:            ~100,000/second   -> 1 second
  sharded 20 ways:       ~2,000,000/second -> instant

-> the ordinary case needs nothing clever; the flash sale needs
   all three mitigations.
```

**Reservation expiry.**

```
~50 reservations/second created at peak
~30% abandoned -> ~15/second expiring
the cleanup job runs every minute: ~900 rows per run

trivial — but WITHOUT it:
  15/second x 86,400 = 1,300,000 units of stock removed per day
  -> the store shows "sold out" while the warehouse is full
  -> and it accumulates silently over weeks
```

**A trivial job whose absence is catastrophic** is worth flagging, because it is the kind of thing that gets
deprioritised.

**Payment costs.**

```
100,000 orders/day, average value $50
= $5,000,000/day of gross merchandise value

card fees ~2.5% + $0.30
= $5,000,000 x 0.025 + 100,000 x 0.30 = $155,000/day

REFUNDS cost the fee AGAIN and are not returned:
  a 1% refund rate = 1,000 refunds/day x ~$1.55 = ~$1,550/day
  = ~$570,000/year in fees on refunded orders alone

-> which is the concrete argument for AUTHORISE, CHECK, THEN CAPTURE.
   A void costs nothing; a refund costs the fee twice.
```

**That number is the best justification available for the two-phase design**, and it is more persuasive than
the correctness argument.

**Infrastructure, roughly:**

```
catalogue + CDN            ~$40,000/month  (10 TB of images)
search cluster             ~$15,000/month
application tier           ~$30,000/month
orders/inventory database  ~$8,000/month   (small!)
Redis / caching            ~$10,000/month
                            ---------------
                            ~$103,000/month

against $155M/year in payment fees.

-> INFRASTRUCTURE IS UNDER 1% OF PAYMENT FEES.
   The database that must never be wrong is the cheapest thing here.
```

**Latency budget.**

```
product page (cached)             ~50 ms
search query                      ~100 ms
add to basket                     ~30 ms
checkout: reserve N lines         ~50 ms
payment authorise (external!)     ~500-2,000 ms   <- dominates
capture (external)                ~500-2,000 ms

-> the payment provider is the slowest thing in the system by an
   order of magnitude, and it is the one you do not control.
   Which is why it must be async from the customer's perspective:
   show "processing", then confirm.
```

---

## 7. The trade-offs

**Atomic conditional update against optimistic concurrency against pessimistic locking.** The conditional
update is simplest and correct, and **serialises on the row**, which is fine below a few thousand writes a
second on that SKU. Optimistic concurrency wins when conflicts are rare and **wastes a round trip on every
conflict**, so it is worse exactly when contention is high. Pessimistic locking is correct and **holds the
lock for the whole transaction**, which on a hot item queues everything behind the slowest request in the
transaction.

**Reservations against decrementing at payment.** Reserving at checkout means a customer who reaches the
payment page will not be told "sold out" after entering their card — **which is the single worst checkout
experience there is.** It costs a reservation table, an expiry job, and **stock that is held but not sold**, so
the effective availability is lower than the physical stock. **Shorten the TTL and you free stock faster and
break more slow checkouts.**

**Strong consistency on inventory against availability.** A single authoritative row is correct and is a
bottleneck. **Sharded counters scale and can strand the last few units** in buckets nobody lands on. **And
showing slightly stale stock on the product page is fine** — the authoritative check happens at checkout, so
"only 3 left!" being wrong by one is a display issue rather than an oversell.

**Authorise-then-capture against charging immediately.** Two-phase costs an extra round trip and a more complex
state machine, **and it makes cancellation free instead of expensive** — around half a million a year in fees
at this volume. **It also has an expiry**: authorisations lapse after about a week, so an order that cannot be
fulfilled quickly must be captured or re-authorised.

**A relational database against something distributed.** Orders are small — a hundred thousand a day, under
two hundred gigabytes a year — **and they need real transactions.** A single primary with replicas is correct,
boring and sufficient. **Reaching for a distributed store here trades the one guarantee you actually need for
scale you do not**, and that is the most tempting mistake in this design after the month you have just had.

**Saga against distributed transaction.** A two-phase-commit across payment, inventory and a courier is not
available — **you cannot hold a lock inside another company's system.** So: a saga with explicit compensations,
**accepting that there are brief windows where the order is inconsistent** and that some compensations are
lossy. **A refund is not the inverse of a charge**; it costs money and takes days.

**When would I not build this?** **Almost always: Shopify, WooCommerce and BigCommerce exist**, and below
serious volume they are cheaper than the team. **Building your own is justified by unusual inventory rules,
unusual pricing, or margins thin enough that platform fees matter.** And **payments specifically should never
be built** — the compliance surface alone is a reason, and every provider gives you idempotency and two-phase
capture for free.

---

## 8. In the interview

### How it gets asked

- *"Design Amazon."* or *"Design an e-commerce checkout."* — the standard prompts.
- *"There is one item left and two people click buy. What happens?"* — the central question.
- *"The payment request times out. Now what?"* — idempotency.
- *"A product goes on flash sale. What breaks?"*
- *"What happens if the warehouse cannot fulfil an order that has already been paid?"*
- *"How do you handle the order lifecycle?"*

### The first ninety seconds

> "The first thing I would establish is that **this is two systems with a factor of two thousand between
> them.**
>
> **Browsing and search are a read problem** — millions of page views, staleness of minutes is fine, cache it
> everywhere. **Checkout and orders are a write problem** — a hundred thousand orders a day, about ten writes a
> second, **and every one must be exactly right.**
>
> **Two thousand reads per write, and the two halves want opposite things.** The read half wants caching and
> replicas; **the write half wants a single authoritative database with real transactions.**
>
> **And I would say that explicitly, because after a month of distributed systems the instinct is to reach for
> something scalable** — and here the correct answer for orders is a single relational primary. **A hundred
> thousand orders a day is under two hundred gigabytes a year. It is a small database that must never be
> wrong.**
>
> **The catalogue is straightforward**: products cached at every layer, images on a CDN, search in an inverted
> index populated asynchronously. **One decision worth naming: the price must be re-read at checkout**, because
> a cached page can be stale and **charging a different price from the one displayed is a legal problem, not
> just an annoyance.**
>
> **The hard part is inventory, and I would go there next unless you want otherwise.**
>
> **The naive version — read the stock, check it, write it back — is wrong**, and specifically it is wrong in a
> way that needs two requests inside a few milliseconds. **It never happens in testing and constantly happens
> in production.**
>
> **The fix is an atomic conditional update**: `UPDATE stock SET qty = qty - 1 WHERE sku = ? AND qty >= 1`, and
> check the affected row count. **The database does the check and the write as one operation**, so two
> concurrent attempts cannot both succeed.
>
> **And on top of that: reservations.** Stock has three states, not two — available, reserved, sold. **Checkout
> reserves with a fifteen-minute expiry; payment converts it to a sale; an abandoned checkout lets it lapse.**
> **The TTL is essential, because nobody sends 'I gave up'.**
>
> **Then the order itself is a saga rather than a transaction** — payment, inventory, warehouse, courier, over
> hours or days, with explicit compensations. **And the compensations are not symmetric**, which is what makes
> the ordering of the steps matter."

### The follow-ups

**"One item left, two people click buy. What happens?"**

> "With the obvious implementation, **both of them buy it**, and I would explain exactly why before giving the
> fix.
>
> **The naive code reads the stock, checks it is at least one, and writes back zero.** Two requests arriving
> within a few milliseconds **both read one, both pass the check, and both write zero.** Two sales, one item.
>
> **What makes this dangerous is that it needs the requests to overlap by milliseconds** — so it never appears
> in testing, and it appears constantly under real load. **It is a correctness bug that only manifests when the
> system is busy, which is when overselling costs the most.**
>
> **Three correct fixes, and I would pick the first.**
>
> **An atomic conditional update.** `UPDATE inventory SET available = available - 1 WHERE sku = ? AND
> available >= 1`, then check that exactly one row was affected. **The database evaluates the condition and
> performs the write as a single atomic operation**, so the second request's condition fails. **And checking
> the row count rather than re-reading the value is what makes it safe** — the count tells me whether *my*
> update was the successful one.
>
> **Optimistic concurrency** — read a version number and write conditionally on it being unchanged, retrying
> on conflict. **Correct, and it wastes a round trip per conflict**, so it is worse exactly when contention is
> high.
>
> **Pessimistic locking** — `SELECT ... FOR UPDATE`. Correct, and it **holds a row lock for the whole
> transaction**, so on a hot item everything queues behind the slowest request.
>
> **And then the design point that matters more than any of them: reservations.**
>
> **Stock should have three states, not two.** Available, reserved, sold. **Adding to a basket reserves
> nothing. Beginning checkout reserves with a fifteen-minute expiry. Payment converts the reservation to a
> sale. An abandoned checkout lets it expire.**
>
> **The reason is the customer experience.** Without reservations, somebody enters their card details and is
> then told the item is gone — **which is the worst possible moment to find out.**
>
> **And the TTL is not optional**, because a customer who closes the tab mid-payment sends nothing. **A
> background job releasing expired reservations is trivial and its absence is catastrophic** — abandoned
> checkouts would permanently remove stock, and the store would show sold out while the warehouse was full.
> **That accumulates silently over weeks.**"

**"The payment request times out. What do you do?"**

> "Nobody knows whether it went through — **including the customer, who will click the button again** — so this
> has to be designed for rather than handled.
>
> **The answer is an idempotency key**, and the detail that matters is where it comes from.
>
> **The client generates a key when the checkout begins**, and sends the same key with every attempt. **The
> payment service records the key alongside the result, and a repeat of that key returns the original result
> rather than charging again.**
>
> **Every real payment provider requires this** — Stripe, Razorpay, Adyen — and that is why.
>
> **The mistake that looks like a solution is generating the key per request.** A retry then carries a
> different key and deduplicates nothing. **The key must be tied to the customer's intention, not to the
> network attempt.**
>
> **And I would use derived keys per operation** — an authorise key and a capture key, both prefixed from the
> order's key — **so a retried authorisation does not deduplicate against the capture.**
>
> **Now the deeper version of the question: what if the timeout happened after the charge succeeded but before
> I recorded it?** **My order is in an unknown state and the money has moved.**
>
> **Two things.** **A reconciliation job** that queries the provider for any order stuck in a pending state
> beyond a few minutes — **the provider is the source of truth for whether money moved, not my database.** And
> **the webhook** the provider sends on completion, which arrives independently of my request and **must be
> handled idempotently**, because it can arrive before, after, or instead of my response.
>
> **The general shape is worth naming: I cannot achieve exactly-once over a network, so I get at-least-once
> plus deduplication, and the deduplication key has to survive the retry.** That is the same answer as message
> queues and notifications — **but here the cost of getting it wrong is a double charge on someone's card**,
> which is a different level of consequence."

**"A flash sale starts. A hundred thousand people want a thousand units. What breaks?"**

> "The catalogue is fine — it is cached, and a hundred thousand page views is ordinary. **What breaks is the
> single inventory row**, because every one of those requests wants to decrement the same row and **a database
> row serialises.**
>
> **A Postgres row does maybe three thousand conditional updates a second.** A hundred thousand requests is
> thirty-three seconds of queueing, **which means timeouts, and timeouts mean retries, and retries make it
> worse.**
>
> **Three mitigations, in order of how much they help.**
>
> **First, admit fewer requests.** A queue or a randomised waiting room in front of the purchase path, so the
> database sees a manageable rate. **And a per-user rate limit**, because one person's script should not be a
> thousand of those requests.
>
> **Second, decrement in memory.** A Redis counter with atomic `DECR` — **about a hundred thousand a second
> against three thousand** — and the durable write follows asynchronously. **The counter becomes the source of
> truth for the sale**, which is a deliberate choice: losing the queue message means an order to reconcile, not
> a lost unit.
>
> **Third, shard the counter.** Split a thousand units into twenty buckets of fifty and route each request to a
> random bucket. **Twenty rows instead of one.**
>
> **And I would state the cost of sharding rather than presenting it as free**: **buckets empty unevenly**, so
> the last few units end up stranded in buckets nobody is landing on. A request that finds its bucket empty has
> to check the others, **and there is a rebalancing pass at the end.** That is a real trade.
>
> **Two more things I would raise.**
>
> **Reservations should probably be disabled or very short for a flash sale.** A fifteen-minute hold on a
> thousand units when a hundred thousand people want them means the stock is invisible for fifteen minutes and
> most of it comes back unsold. **Thirty seconds, or immediate purchase, is the right answer there.**
>
> **And the honest framing: 'sold out' is a better answer than 'sorry, we oversold'.** Rejecting the hundred
> thousandth request quickly is correct behaviour, **not a failure to be engineered away** — and designing the
> rejection path to be fast and clear is more valuable than trying to serve everyone."

### The model answer

*"Design the checkout and order system for an online retailer: ten million daily users, a hundred thousand
orders a day, occasional flash sales."*

> "Let me start with the split, because it determines everything and it is the mistake I most want to avoid.
>
> **Browsing is two thousand times the volume of ordering.** Two hundred million page views a day against a
> hundred thousand orders. **The read half wants caching and replicas and tolerates minutes of staleness. The
> write half is small and must be exactly right.**
>
> **So the order and inventory database is a single relational primary with replicas** — a hundred thousand
> orders a day is under two hundred gigabytes a year, and **it needs real transactions.** **I want to say that
> explicitly, because the instinct is to reach for something distributed, and here that would trade the one
> guarantee I actually need for scale I do not.**
>
> **Catalogue and search: cached at every layer, images on a CDN, an inverted index populated asynchronously.**
> **And the price is re-read at checkout**, because the page may be ten minutes stale and charging a different
> price from the one displayed is a legal problem.
>
> **Inventory, which is the hard part.** Three states — available, reserved, sold. **Checkout reserves with a
> fifteen-minute expiry** via an atomic conditional update: `WHERE sku = ? AND available >= ?`, checking the
> affected row count. **The condition and the write are one operation, so the read-then-write race cannot
> happen.**
>
> **A background job releases expired reservations every minute.** Trivial, and **its absence is catastrophic**
> — abandoned checkouts would permanently remove about a million units a day and the store would show sold out
> with a full warehouse.
>
> **Checkout is idempotent on a client-generated key, created when the checkout begins.** A retry after a
> timeout returns the original result. **A key generated per request would differ on the retry and deduplicate
> nothing**, which is the mistake that looks like a fix.
>
> **Payment is two-phase: authorise, commit inventory, then capture.** The ordering is the design. **Voiding an
> authorisation is free and invisible; refunding a capture costs the fee again and takes days.** At a hundred
> thousand orders a day averaging fifty dollars, **a one percent refund rate is over half a million a year in
> fees alone** — which is a more persuasive argument for two-phase than the correctness one.
>
> **The order is a saga, not a transaction.** It spans payment, inventory, warehouse and courier over days,
> and **I cannot hold a lock inside another company's system.** So: an explicit transition table checked on
> every write — **which is what prevents a retried "paid" from charging twice** — with compensations attached
> to the failure states.
>
> **And the state change and the event publication go in the same transaction, via an outbox.** Otherwise a
> crash between them leaves an order marked paid with the warehouse never told. **A separate process drains
> the outbox, which is at-least-once, so every consumer must be idempotent.**
>
> **Flash sales break the one part that cannot be cached: the inventory row.** A hundred thousand requests
> against a row that does three thousand updates a second is thirty-three seconds of queueing and a retry
> storm. **Three fixes: admit fewer requests with a queue and a per-user limit; decrement in Redis, which does
> a hundred thousand a second, with the durable write following; and shard the counter twenty ways.**
> **Sharding strands the last few units in empty buckets, so it needs a fallback and a rebalance** — a real
> cost, not a free win.
>
> **Two things I would flag.**
>
> **The payment provider is the slowest component by an order of magnitude** — half a second to two seconds,
> against fifty milliseconds for everything else — **and it is the one I do not control.** So payment must be
> asynchronous from the customer's view: show "processing", confirm on the webhook. **And the webhook must be
> idempotent, because it can arrive before, after, or instead of my own response.**
>
> **And infrastructure is under one percent of payment fees here** — about a hundred thousand a month against
> a hundred and fifty-five million a year in card charges. **The database that must never be wrong is the
> cheapest thing in the system**, which is worth remembering when someone proposes optimising it."

---

## 9. Recall card

**Two systems with 2,000:1 between them:** browse/search is a cacheable read problem tolerating minutes of
staleness; **checkout/orders is small (~100k/day, <200 GB/year) and must be exactly right.** Orders belong in
**a single relational primary** — reaching for a distributed store trades the one guarantee you need for scale
you do not.

**The read-then-write race is the central bug**: two requests both read 1, both pass the check, both write 0.
**It needs a few milliseconds of overlap — never in testing, constantly in production.** Fix with an **atomic
conditional update** (`WHERE sku = ? AND available >= ?`, then check the **affected row count**, not a re-read).
Optimistic concurrency wastes a round trip per conflict; pessimistic locking serialises everything on the row.

**Stock has THREE states: available / reserved / sold.** Basket reserves nothing; **checkout reserves with a
TTL**; payment converts it; abandonment lets it lapse — **because nobody sends "I gave up".** The expiry job is
trivial and its absence is catastrophic: the store shows sold out with a full warehouse.

**Idempotency key generated by the CLIENT when checkout begins**, not per request — a per-request key differs
on the retry and deduplicates nothing. **The provider is the source of truth for whether money moved**, so add
a reconciliation job and an idempotent webhook handler.

**Two-phase payment, and the ordering is the design: authorise → check inventory → capture.** A **void is free
and invisible; a refund costs the fee again and takes days** — ~$570k/year at 1% refunds, which beats the
correctness argument for persuasiveness.

**The order is a SAGA with an explicit transition table** (which is what stops a retried "paid" charging
twice) and **compensations that are not symmetric**. **State change and event publication go in one
transaction via an outbox.** **Flash sales break the single inventory row** (~3,000 updates/s): admit fewer,
decrement in Redis (~100,000/s), shard the counter — **and sharding strands the last units, which is a real
cost.** "Sold out" is a better answer than "we oversold".
