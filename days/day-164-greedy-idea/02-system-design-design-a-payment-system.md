---
day: 164
track: system-design
title: "Design a payment system"
phase: "High-level design case studies"
status: written
---

# Design a payment system

## 1. What this is, and why they ask it

A payment system moves money from one party to another and **keeps a record that survives an audit.**

They ask it because **it is the only design in this course where being wrong is not recoverable by trying
again.** Every other system can drop a location update, lose a view count, serve a stale tweet. **Here, a lost
payment is somebody's money that is gone, and a duplicated one is a charge on a real card that somebody has to
notice, dispute and reverse.**

And the specific difficulty is a mismatch that runs through the whole system. **The business requires
exactly-once. The network offers at-least-once.** Every payment API call can time out with the request having
succeeded, **and the caller genuinely cannot tell.** Reconciling that is not a detail — **it is the design.**

Three things carry the interview.

**Idempotency, done properly.** Not "we use a key", but where the key comes from, what it is stored against,
what happens on a concurrent retry, and how long it lives.

**Double-entry bookkeeping**, which is a five-hundred-year-old idea that solves a real engineering problem:
**every transfer is two entries that must sum to zero**, so the books either balance or you know instantly
that they do not. **Most candidates have never heard of it and it is the correct data model.**

**And reconciliation**, which is the acknowledgement that distributed systems fail and money must still add up.
**You compare your records against the bank's, every day, and you find discrepancies — because you always
do.**

By the end of this lesson you can design the ledger, make payments idempotent under concurrency, handle the
authorise-capture-refund lifecycle, run reconciliation, and say honestly what consistency you can and cannot
offer.

---

## 2. The story

The society had four hundred and twenty flats and the accounts had been kept by whoever was on the committee,
which meant they had been kept eleven different ways.

**And when Zubeida took over as treasurer, the books did not balance by eleven thousand rupees.**

Not stolen. Nobody thought that. **Just eleven thousand rupees of the difference between what people had paid
and what had been written down, accumulated over four years, in a register that recorded one thing per line.**

*Received 2,400 from flat 312.*

**And that was all it said. Received. Not where it went.**

Because the money went into the account, or it went into the petty cash tin, or it went into the man's pocket
until Tuesday when he remembered to bank it. **The register recorded that money had arrived and never recorded
where it had arrived.**

Zubeida's husband had been a bank clerk for thirty-one years, and when she described the problem he told her
what to do in one sentence, and she thought it was pedantic, and it took her a month to understand it was
not.

**"Write every payment twice. Once where it came from, once where it went. And the two numbers must be the
same."**

*Flat 312 owes us 2,400 less. The bank account has 2,400 more.*

**Two lines, equal and opposite, for every single thing.**

Which was double the writing, and she said so, and he said the thing that settled it.

**"If you write one line you can be wrong and never know. If you write two, they either match or they do
not, and you find out on the same day."**

And then he told her the second half, which she had not asked about.

**"And every month you take the bank's own statement and go down it line by line against yours."**

She said that if the two lines always matched, surely her book was right.

**"Your book is right about what you wrote down,"** he said. **"The bank's statement is right about what
happened. Those are different, and the difference is always something — a cheque that has not cleared, a
charge you did not know about, something entered twice. You will never once find them identical. That is not
a failure. That is the point of doing it."**

---

## 3. The idea in plain English

Zubeida's husband has described the two halves of every payment system: **double-entry bookkeeping, and
reconciliation.** The first makes errors detectable; the second finds the ones that got in anyway.

**Start with the scope, because "payment system" means three different things.**

```
IN     accepting a payment from a customer
       the ledger — where money is recorded
       the authorise / capture / refund lifecycle
       idempotency and retries
       reconciliation with the bank
OUT    fraud detection, PCI compliance in detail, currency
       exchange, lending, the card networks' internals
```

**And one thing has to be said before designing anything: you almost certainly do not touch the card.** **PCI
DSS compliance for handling card numbers is an enormous burden**, so real systems use a provider's hosted
fields or tokenisation — **the card number never reaches your servers and you store a token instead.** Saying
that in the first minute is a strong signal.

**Now the ledger, which is the data model.**

**A payment is not a row that says "customer paid £50".** It is **two entries**: money leaving one account and
money arriving in another, **and they must sum to zero.**

```
transfer £50 from customer C to merchant M:

  entry 1:  account C   -5000   (in the smallest unit: pence)
  entry 2:  account M   +5000
                        -----
  sum:                      0     <- ALWAYS, for every transaction
```

**Three properties fall out of that and they are the reason for it.**

**Errors are detectable.** If the entries do not sum to zero, something is wrong, **and you know immediately
rather than in four years.**

**The balance is derived, not stored.** An account's balance is the sum of its entries. **You can recompute it
from scratch at any time**, which means a corrupted balance is repairable — and a stored balance that drifts is
not.

**And the ledger is append-only.** **You never update or delete an entry.** A mistake is corrected by writing
a compensating pair, **so the history is complete and an auditor can see what happened and when it was
fixed.** A payment that was reversed shows as two transactions, not as an absence.

**Two mechanical rules that are not negotiable.**

**Store money as integers in the smallest unit** — pence, paise, cents. **Never floating point**, because
`0.1 + 0.2` is not `0.3`, and a system that loses a hundredth of a penny per transaction loses real money at
scale and fails its audit.

**And every entry carries its currency.** **Adding rupees to dollars is a bug that a type system will not catch
for you**, so the currency is part of the amount, and cross-currency transfers are two transactions plus an
explicit exchange entry.

**Now idempotency, and this is where the interview usually goes.**

**The problem, stated exactly: the client sends a payment request. The connection times out. Did the money
move?**

**Nobody knows.** Not the client, not the user, and the user will press the button again.

**The answer is an idempotency key, and four details make it actually work.**

**Where it comes from.** The client generates it **when the user's intention forms** — when they open the
checkout — **not per request.** A key generated per attempt differs on the retry and deduplicates nothing,
**which is the mistake that looks like a solution.**

**What it is stored against.** The key maps to the **result**, not merely to "seen". A retry must return the
original response — the same payment id, the same status — **so the client sees exactly what it would have
seen.**

**What happens on a concurrent retry.** Two requests with the same key arriving at once. **A check-then-write
is a race**, so the insert of the key must be atomic — a unique constraint on the key column, or a `SET NX` —
**and the loser waits for the winner's result rather than proceeding.**

**And how long it lives.** **At least twenty-four hours**, because that is the realistic window for a client
retrying after an outage. **Storing them forever is unnecessary and storing them for five minutes is
useless.**

**Then the lifecycle, which is three operations and not one.**

```
AUTHORISE   reserve the money on the card; the customer's available
            balance drops; nothing is transferred
CAPTURE     take it; the money actually moves
REFUND      send it back, after capture
VOID        cancel an authorisation before capture
```

**The gap between authorise and capture is the useful part.** **You authorise, then verify you can fulfil, then
capture.** If you cannot fulfil, **you void — which is free, instant and invisible to the customer.**

**Refunding after capture is a completely different thing.** It costs the transaction fee again, **takes days
to appear on the customer's statement**, and generates a support contact. **The asymmetry is why the ordering
matters**, and it is worth quantifying.

**And authorisations expire** — typically after about seven days — so an order that cannot be fulfilled quickly
must be captured or re-authorised.

**Then the payment flow itself, and the part that is genuinely hard.**

**Your service calls the provider. The call times out.** You do not know whether the charge succeeded, **and
you must not simply retry**, because a retry without an idempotency key charges twice.

**Three mechanisms together, and all three are needed.**

**Idempotency keys passed to the provider**, so your retry is safe.

**A reconciliation job** that queries the provider for any payment stuck in a pending state past a few minutes.
**The provider is the source of truth for whether money moved — not your database.**

**And webhooks**, which the provider sends when the payment settles. **They arrive independently of your
request** — possibly before your own response, possibly instead of it — **so the handler must be idempotent
and must not assume ordering.**

**Then reconciliation, which is Zubeida's monthly statement.**

**Every day, you take the provider's or the bank's settlement file and compare it against your ledger, line by
line.**

**And you always find discrepancies.** A payment your system recorded that the bank did not, or the reverse. A
fee you did not know about. A refund processed on their side that your webhook missed. **Finding nothing would
mean the job is broken.**

**The categories are worth knowing**: in your books and not theirs; in theirs and not yours; **amounts that
differ**; and timing differences where a payment falls either side of the cut-off. **Only the third is
alarming; the first two are usually timing, and the fourth is expected.**

**Finally, the consistency question, answered honestly.**

**A payment system needs strong consistency where money moves and can tolerate eventual consistency
everywhere else.**

**The ledger writes are transactional in a relational database**, and the volume makes that affordable —
**this is the argument for boring technology, and it is the right one.**

**But the moment the money is with an external provider, you are in a distributed system you do not control**,
and no amount of local transaction discipline changes that. **What you get is: exactly-once *recorded*, via
idempotency and reconciliation, on top of at-least-once *attempted*.** Saying that precisely is the answer.

---

## 4. The picture

Double-entry, and why it makes errors detectable:

```
   SINGLE ENTRY (Zubeida's old register)

     received 2,400 from flat 312

     -> where did it go? the bank? the tin? somebody's pocket?
     -> the register cannot tell you
     -> an error is INVISIBLE until somebody counts the money


   DOUBLE ENTRY

     transaction #4471
       account flat_312     -240000    (paise)
       account bank_hdfc    +240000
                            --------
       sum                        0    <- ALWAYS

     -> every transaction sums to zero, or it is REJECTED
     -> the balance of any account = the sum of its entries
     -> an error is caught the same day, by arithmetic

   "If you write one line you can be wrong and never know."
```

The append-only rule:

```
   WRONG: fix a mistake by editing

     UPDATE entries SET amount = 240000 WHERE id = 4471
     -> the history is gone
     -> an auditor cannot see what happened
     -> and two people editing concurrently is a lost update

   RIGHT: fix a mistake by writing a compensating pair

     #4471   flat_312  -250000 ; bank_hdfc  +250000    (the error)
     #4498   flat_312  +250000 ; bank_hdfc  -250000    (the reversal)
     #4499   flat_312  -240000 ; bank_hdfc  +240000    (the correction)

     -> three transactions, all visible
     -> the balance is correct
     -> the history explains itself
```

The idempotency race, which is the detail that matters:

```
   TWO REQUESTS, SAME KEY, ARRIVING TOGETHER

   NAIVE (check then write) — BROKEN

     A: SELECT ... WHERE key = K   -> not found
     B: SELECT ... WHERE key = K   -> not found      <- both miss
     A: charge the card
     B: charge the card                              <- TWICE
     A: INSERT key K
     B: INSERT key K

   CORRECT — the insert IS the lock

     A: INSERT key K  -> succeeds, A proceeds
     B: INSERT key K  -> UNIQUE VIOLATION
                      -> B waits for A's result, then returns it

     the database's unique constraint does the mutual exclusion.
     A check-then-write cannot, because there is a window between them.
```

The lifecycle, and the asymmetry that shapes it:

```
   AUTHORISE ---------> CAPTURE ---------> (settled)
       |                    |
       | VOID               | REFUND
       v                    v
   free, instant,       costs the fee AGAIN,
   invisible to         takes DAYS to appear,
   the customer         the customer notices

   -> put every check that can fail BETWEEN authorise and capture

   AND: authorisations EXPIRE (~7 days), so an order that cannot be
        fulfilled quickly must be captured or re-authorised.
```

The timeout, which is the real problem:

```
   your service ---- charge ----> provider
                                     |
                                  [ charges the card ]
                                     |
                <---- response --X    (lost: timeout, crash, network)

   YOU DO NOT KNOW WHETHER THE MONEY MOVED.
   Retrying without a key charges twice. Not retrying may lose it.

   THREE MECHANISMS, ALL THREE NEEDED:

   1. IDEMPOTENCY KEY sent to the provider
      -> your retry is safe: the same key returns the same result

   2. RECONCILIATION JOB
      -> anything pending for more than N minutes: ASK the provider
      -> the provider is the source of truth, not your database

   3. WEBHOOK from the provider
      -> arrives independently; may come BEFORE your own response
      -> so the handler must be idempotent and order-independent
```

Daily reconciliation, and what you expect to find:

```
   YOUR LEDGER              THE BANK'S SETTLEMENT FILE
   4,412 transactions       4,409 transactions
   £221,043.55              £220,912.10

   THE FOUR CATEGORIES:

   in yours, not theirs     usually TIMING — after the cut-off
                            sometimes a payment that silently failed
   in theirs, not yours     a webhook you missed, or a chargeback
   amounts DIFFER           ALARMING. A fee, a partial capture,
                            or a real bug
   timing differences       expected, and they resolve tomorrow

   YOU WILL NEVER FIND THEM IDENTICAL.
   "That is not a failure. That is the point of doing it."
```

---

## 5. How it actually works

### The ledger schema

```sql
CREATE TABLE transactions (
    id           BIGINT PRIMARY KEY,
    created_at   TIMESTAMPTZ NOT NULL,
    kind         TEXT NOT NULL,          -- payment, refund, fee, payout
    reference    TEXT,                   -- the order, the dispute, ...
    idempotency_key TEXT UNIQUE          -- one transaction per key
);

CREATE TABLE entries (
    id             BIGSERIAL PRIMARY KEY,
    transaction_id BIGINT NOT NULL REFERENCES transactions(id),
    account_id     BIGINT NOT NULL,
    amount         BIGINT NOT NULL,      -- SIGNED, in the smallest unit
    currency       CHAR(3) NOT NULL
);

CREATE INDEX ON entries (account_id, id);
```

**`amount BIGINT` in the smallest unit and never a float.** **`0.1 + 0.2 != 0.3`**, and a system that rounds
in the wrong direction a million times a day loses real money and fails its audit.

**`entries` has no update or delete path** — that is enforced by permissions rather than by convention, because
"we agreed not to" is not a guarantee.

**And `idempotency_key UNIQUE` on `transactions` is doing real work**: the database enforces one transaction
per key, **so a concurrent duplicate fails at insert rather than after charging.**

### Writing a transfer

```python
def transfer(from_account: int, to_account: int, amount: int,
             currency: str, idempotency_key: str, kind: str) -> int:
    if amount <= 0:
        raise ValueError("amount must be positive")

    with db.transaction():
        try:
            tx_id = db.insert_returning_id("""
                INSERT INTO transactions (id, created_at, kind, idempotency_key)
                VALUES (%(id)s, now(), %(kind)s, %(key)s)
            """, {"id": snowflake.next_id(), "kind": kind,
                  "key": idempotency_key})
        except UniqueViolation:
            return db.query_one("""
                SELECT id FROM transactions WHERE idempotency_key = %(key)s
            """, {"key": idempotency_key})            # the retry's answer

        entries = [(from_account, -amount), (to_account, +amount)]
        assert sum(a for _, a in entries) == 0        # the invariant, checked
        for account_id, signed in entries:
            db.insert("""
                INSERT INTO entries (transaction_id, account_id, amount, currency)
                VALUES (%(tx)s, %(acct)s, %(amt)s, %(cur)s)
            """, {"tx": tx_id, "acct": account_id, "amt": signed, "cur": currency})
        return tx_id
```

**The `UniqueViolation` branch is the idempotency**, and it is the database doing the mutual exclusion —
**there is no window between checking and inserting, because they are the same operation.**

**`assert sum(...) == 0` looks like decoration and is not.** **It is the invariant that makes the whole model
work**, and asserting it on every write catches an entire class of bug at the point of insertion rather than
during an audit.

### Balances, derived rather than stored

```python
def balance(account_id: int, currency: str) -> int:
    return db.query_scalar("""
        SELECT COALESCE(SUM(amount), 0) FROM entries
         WHERE account_id = %(acct)s AND currency = %(cur)s
    """, {"acct": account_id, "cur": currency}) or 0


def balance_cached(account_id: int, currency: str) -> int:
    """A snapshot plus the entries after it. The snapshot is a cache."""
    snap = db.query_one("""
        SELECT balance, last_entry_id FROM balance_snapshots
         WHERE account_id = %(acct)s AND currency = %(cur)s
    """, {"acct": account_id, "cur": currency})
    if snap is None:
        return balance(account_id, currency)
    delta = db.query_scalar("""
        SELECT COALESCE(SUM(amount), 0) FROM entries
         WHERE account_id = %(acct)s AND currency = %(cur)s
           AND id > %(after)s
    """, {"acct": account_id, "cur": currency, "after": snap.last_entry_id})
    return snap.balance + (delta or 0)
```

**The snapshot is a cache and never the truth.** **The truth is always the sum of the entries**, so a corrupted
snapshot is repaired by recomputation rather than by investigation.

**Without snapshots, summing an account with ten million entries takes seconds** — so they exist for
performance, and **the key property is that discarding them all loses nothing.**

### The payment flow

```python
def charge(order_id: int, amount: int, currency: str, token: str,
           idempotency_key: str) -> dict:
    payment = payment_store.get_or_create(
        order_id=order_id, amount=amount, currency=currency,
        idempotency_key=idempotency_key, state="pending")
    if payment.state in ("succeeded", "failed"):
        return payment.as_dict()              # a retry: the same answer

    try:
        result = provider.charge(
            amount=amount, currency=currency, source=token,
            idempotency_key=f"charge:{idempotency_key}")   # THE PROVIDER'S KEY
    except (Timeout, ConnectionError):
        payment_store.mark(payment.id, "unknown")          # NOT "failed"
        return {"state": "processing", "payment_id": payment.id}

    if result.succeeded:
        transfer(payment.customer_account, payment.merchant_account,
                 amount, currency, f"tx:{idempotency_key}", "payment")
        payment_store.mark(payment.id, "succeeded", provider_id=result.id)
    else:
        payment_store.mark(payment.id, "failed", reason=result.error)
    return payment_store.get(payment.id).as_dict()
```

**`mark(payment.id, "unknown")` rather than `"failed"` on a timeout is the most important line here.** **A
timeout does not mean the charge failed** — it means you do not know. **Marking it failed and letting the
customer retry is how you charge twice**, and it is the single most common mistake in payment code.

**And the idempotency key passed to the provider is derived from ours with a prefix**, so the charge and any
later capture do not deduplicate against each other.

### Resolving unknowns

```python
def reconcile_pending() -> None:
    """Runs every minute. The PROVIDER is the source of truth."""
    stuck = payment_store.in_state("unknown", older_than_seconds=120)
    for payment in stuck:
        result = provider.lookup(idempotency_key=f"charge:{payment.idempotency_key}")
        if result is None:
            payment_store.mark(payment.id, "failed", reason="never reached provider")
        elif result.succeeded:
            transfer(payment.customer_account, payment.merchant_account,
                     payment.amount, payment.currency,
                     f"tx:{payment.idempotency_key}", "payment")
            payment_store.mark(payment.id, "succeeded", provider_id=result.id)
        else:
            payment_store.mark(payment.id, "failed", reason=result.error)
```

**Asking the provider is the only correct resolution.** **Your database recorded what you intended; the
provider recorded what happened**, and after a timeout only the second one is authoritative.

**And the `transfer` here is safe to call even if the webhook already did it**, because it carries the same
idempotency key — **which is why the ledger's key matters as much as the provider's.**

### The webhook handler

```python
@app.post("/webhooks/provider")
def handle_webhook(payload: dict, signature: str) -> tuple[str, int]:
    if not verify_signature(payload, signature):
        return "bad signature", 401           # anyone can POST to this URL

    event_id = payload["id"]
    if not redis.set(f"webhook:{event_id}", "1", nx=True, ex=7 * 86400):
        return "ok", 200                      # already processed

    if payload["type"] == "payment.succeeded":
        key = payload["metadata"]["idempotency_key"]
        payment = payment_store.by_idempotency_key(key)
        if payment and payment.state != "succeeded":
            transfer(payment.customer_account, payment.merchant_account,
                     payment.amount, payment.currency, f"tx:{key}", "payment")
            payment_store.mark(payment.id, "succeeded")
    return "ok", 200
```

**Signature verification first**, because the endpoint is public and **anyone can post a "payment succeeded"
event to it** — which without verification is free money.

**Deduplication on the event id**, because providers deliver at-least-once and a retried webhook must not
double-post to the ledger.

**And the handler must tolerate arriving before your own response**, which happens: the provider's webhook can
land while your `charge` call is still in flight. **Both paths write the same ledger transaction with the same
key, so whichever arrives first wins and the other is a no-op.**

### Daily reconciliation

```python
def reconcile_day(settlement_file: str, date: str) -> dict:
    theirs = {row.reference: row for row in parse_settlement(settlement_file)}
    ours = {tx.provider_id: tx for tx in ledger.transactions_on(date)}

    report = {"matched": 0, "missing_from_theirs": [], "missing_from_ours": [],
              "amount_mismatch": []}

    for ref, our_tx in ours.items():
        their_row = theirs.get(ref)
        if their_row is None:
            report["missing_from_theirs"].append(ref)      # usually timing
        elif their_row.amount != our_tx.amount:
            report["amount_mismatch"].append(                # ALARMING
                (ref, our_tx.amount, their_row.amount))
        else:
            report["matched"] += 1

    for ref in theirs.keys() - ours.keys():
        report["missing_from_ours"].append(ref)             # a missed webhook?

    alert_if_needed(report)
    return report
```

**`amount_mismatch` is the category to alert on loudly.** The other three are usually timing or a missed
webhook that the next run resolves; **an amount that differs is a fee you did not model, a partial capture, or
a genuine bug.**

**And the job must be expected to find things.** **A reconciliation that reports zero discrepancies every day
is almost certainly broken**, and monitoring should alert on that too.

### Money as integers

```python
from decimal import Decimal

def to_minor_units(amount: str, currency: str) -> int:
    """'12.34' GBP -> 1234. Decimal, never float."""
    exponent = CURRENCY_EXPONENT[currency]    # GBP 2, JPY 0, BHD 3
    return int(Decimal(amount).scaleb(exponent))


def format_amount(minor: int, currency: str) -> str:
    exponent = CURRENCY_EXPONENT[currency]
    return str(Decimal(minor).scaleb(-exponent))
```

**`CURRENCY_EXPONENT` is not always two.** **Japanese yen has no subunit; Bahraini dinar has three decimal
places.** Hard-coding two is a bug that only appears in some countries, which is the worst kind.

**And `Decimal`, not `float`, even for the conversion** — `float("12.34") * 100` is `1233.9999999999998`, and
`int()` of that is `1233`.

### The real systems

```
Stripe / Adyen /        the providers. All require idempotency keys,
Razorpay / Braintree    all support authorise/capture separately,
                        all send webhooks and settlement files
PostgreSQL              the ledger — transactions are exactly what
                        this is for, and the volume is small
Kafka                   payment events out to other services
                        (never the ledger itself)
double-entry            not a technology: an accounting practice from
                        1494, and still the correct data model
PCI DSS                 the compliance regime for handling card data,
                        which is why you use hosted fields and never
                        see the number
```

**Naming double-entry's age is worth doing**, because it makes the point that this is a solved problem and the
engineering job is to implement it correctly rather than to invent something.

---

## 6. The numbers

**Scale, and it is small — which is the point.**

```
10,000,000 payments/day
= ~116/second average, peak ~500/second

each payment: ~2 ledger entries + 1 transaction row
= ~30,000,000 ledger rows/day
= ~350 row-writes/second, peak ~1,500
```

**Fifteen hundred writes a second at peak** is an ordinary relational workload. **One primary with replicas
handles it comfortably**, which is the argument for boring technology and is the correct answer.

**Storage.**

```
transaction row  ~200 bytes
entry row        ~80 bytes

per day: 10,000,000 x (200 + 2 x 80) = 3.6 GB/day
per year:                              1.3 TB/year
x 3 replicas:                          4 TB/year

and it is APPEND-ONLY and must be kept for SEVEN YEARS
(the usual statutory retention)
-> ~28 TB over the retention period

-> partition by month, keep recent partitions hot, archive the rest.
   Small by this course's standards, and it never shrinks.
```

**Balance computation, and why snapshots exist.**

```
a busy merchant account: 10,000 entries/day x 365 = 3,650,000 entries/year

summing them: ~50 ms per query at that size, growing forever

with a daily snapshot: sum the snapshot plus today's entries
  -> ~10,000 rows -> ~1 ms

50x faster, and the key property is that the snapshot can be
DISCARDED AND RECOMPUTED — it is a cache, not the truth.
```

**Idempotency key storage.**

```
10,000,000 keys/day, retained 24 hours
key ~40 bytes + the stored result reference ~60 bytes = ~100 bytes

10,000,000 x 100 B = 1 GB

-> trivial. There is no excuse for a short TTL.
   24 hours is the realistic client-retry window; 5 minutes is useless.
```

**Provider latency, which dominates everything.**

```
ledger write (local)          ~5 ms
provider charge (external)    ~500-2,000 ms       <- 100-400x
webhook round trip            seconds to minutes

-> the payment provider is the slowest component by two orders
   of magnitude, and you do not control it
-> so the customer-facing flow must be ASYNCHRONOUS:
   "processing", then confirm on the webhook
```

**The void-versus-refund asymmetry, in money.**

```
10,000,000 payments/day, average £40
card fees ~1.5% + 20p

fee per payment:  £40 x 0.015 + £0.20 = £0.80
daily fees:       10,000,000 x £0.80  = £8,000,000/day

A VOID (before capture):   costs NOTHING
A REFUND (after capture):  the original fee is NOT returned,
                           plus a refund fee of ~20p

at a 1% failure-after-capture rate:
  100,000/day x (£0.80 + £0.20) = £100,000/DAY
  = £36,500,000/year

-> which is the entire argument for AUTHORISE, CHECK, THEN CAPTURE.
```

**That is the largest single number in this lesson**, and it is a business argument rather than a technical
one — **which makes it the more persuasive kind.**

**Reconciliation.**

```
10,000,000 transactions/day to compare
a hash-join of two 10M-row sets: seconds on one machine

typical discrepancy rate: 0.01% - 0.1%
= 1,000 - 10,000 items/day needing review

-> which is why the CATEGORIES matter: 99% are timing and resolve
   themselves tomorrow. The amount mismatches are the ~10/day that
   a human must look at.

A run reporting ZERO discrepancies means the job is broken.
```

**Infrastructure cost, against the fees:**

```
ledger database (primary + 2 replicas)   ~$5,000/month
application tier                         ~$10,000/month
reconciliation + jobs                    ~$2,000/month
key store / cache                        ~$1,000/month
                                          ---------------
                                          ~$18,000/month

against £8,000,000/DAY in card fees.

-> infrastructure is ~0.007% of the fees.
   The system that must never be wrong is essentially free to run,
   and the correct engineering choice is always the safe one.
```

**Failure budget, stated honestly:**

```
at 10,000,000 payments/day and 99.99% correctness:
  1,000 wrong payments per day

which is NOT ACCEPTABLE — each one is a person whose money moved
incorrectly.

the target is not a percentage. It is:
  - zero unreconciled discrepancies older than 48 hours
  - every discrepancy CATEGORISED, not merely counted
  - and the ledger balancing to zero, every day, exactly
```

---

## 7. The trade-offs

**Double-entry against a simple balance column.** A balance column is one row per account and one update per
payment — simpler, faster, and **an error in it is undetectable and unrepairable.** Double-entry doubles the
rows and makes the balance derived, **so corruption is caught by arithmetic and fixed by recomputation.** At
this volume the extra rows cost nothing, **and the auditability is not optional in a regulated context.**

**Append-only against updating.** Never editing means the history is complete and concurrent writers cannot
lose an update. **It means corrections are compensating pairs**, so a reversed payment appears as two
transactions rather than as an absence — **which is more confusing to a naive reader and is what an auditor
requires.**

**Synchronous against asynchronous payment.** Synchronous is simpler and **couples the customer's request to a
provider that takes up to two seconds and sometimes times out.** Asynchronous — "processing", then confirm on
the webhook — is the right answer and **costs a whole state machine plus the reconciliation of unknowns.**
There is no version of this without the unknown state.

**Strong consistency in the ledger against scale.** A single relational primary is correct, transactional and
**a bottleneck if you ever exceed it.** At ten million payments a day you will not — **fifteen hundred writes a
second at peak** — and **sharding a ledger by account breaks cross-account transactions**, which is exactly
what a transfer is. **The right answer is not to shard until forced, and then to shard by a boundary that
transfers do not cross.**

**Idempotency key retention.** Twenty-four hours costs a gigabyte and covers realistic retries. **A short
window is a correctness bug that appears only during an outage** — which is precisely when clients retry
hardest. **Storing them forever costs little and complicates nothing**, so this trade barely exists: err long.

**Reconciliation frequency.** Daily is standard and means a discrepancy can live for a day. **Hourly finds
problems sooner and produces more timing-related noise**, because more payments straddle the cut-off. **The
useful metric is not the frequency but the age of the oldest unresolved item.**

**And the honest one: exactly-once does not exist.** You get **at-least-once attempted plus deduplication on a
key**, which produces exactly-once *recorded*. **Anyone claiming exactly-once delivery over a network is
describing idempotency and calling it something else** — and saying so precisely is a better answer than
claiming the guarantee.

**When would I not build this?** **The payment rails themselves: never.** Stripe and its peers exist, the
compliance surface alone justifies them, and **card handling without PCI scope is worth more than any
engineering.** **The ledger, though, you often do build** — even on top of a provider, you need your own record
of what you believe happened, **because reconciling against theirs requires having something to reconcile.**
And for internal balances — wallets, credits, marketplace payouts — **there is no provider to defer to and the
double-entry ledger is yours.**

---

## 8. In the interview

### How it gets asked

- *"Design a payment system."* or *"Design Stripe."* — the standard prompts.
- *"The charge request times out. What do you do?"* — the central question.
- *"How do you make sure a customer is not charged twice?"* — idempotency, in detail.
- *"How do you store money?"* — the double-entry and integers question.
- *"How do you know your numbers are right?"* — reconciliation.
- *"What consistency guarantees can you offer?"* — where honesty scores.

### The first ninety seconds

> "Two things before I design anything.
>
> **First, I would not handle card numbers.** PCI compliance for storing card data is an enormous burden, so
> **the card goes to the provider through hosted fields and I store a token.** That is worth establishing
> immediately because it removes most of the security surface.
>
> **Second, the scale here is small and that shapes everything.** Ten million payments a day is about fifteen
> hundred writes a second at peak. **This is an ordinary relational workload, and it must be exactly right** —
> so the answer is a single Postgres primary with replicas, and I would resist any instinct to distribute it.
>
> **Now the data model, which is where I would spend the time: double-entry bookkeeping.**
>
> **A payment is not a row saying 'the customer paid fifty pounds'. It is two entries — money leaving one
> account and arriving in another — and they must sum to zero.**
>
> **Three things follow.** **Errors become detectable**: if the entries do not sum to zero, something is wrong
> and I know today rather than in four years. **The balance is derived, not stored** — it is the sum of the
> entries, so a corrupted balance is repairable by recomputation. **And the ledger is append-only**: a mistake
> is corrected by a compensating pair, never by an edit, so the history is complete for an auditor.
>
> **Two mechanical rules.** **Money is integers in the smallest unit — pence, never floats** — because point
> one plus point two is not point three, and rounding errors at this volume are real money and a failed audit.
> **And every amount carries its currency**, because adding rupees to dollars is a bug no type system will
> catch.
>
> **Then the hard part, which is that the business needs exactly-once and the network offers at-least-once.**
>
> **The charge request times out. Did the money move? Nobody knows, including the customer, who will press the
> button again.**
>
> **Three mechanisms and all three are needed.** **Idempotency keys**, generated by the client when the
> checkout begins, so a retry is safe. **A reconciliation job** that asks the provider about anything stuck —
> because after a timeout, the provider is the source of truth and my database is not. **And webhooks**, which
> arrive independently and must be handled idempotently.
>
> **And the fourth thing, which is Zubeida's monthly statement: daily reconciliation against the bank's
> settlement file.** **You always find discrepancies. Finding none means the job is broken.**"

### The follow-ups

**"The charge request times out. What do you do?"**

> "The first thing is what I do *not* do: **I do not mark it failed.**
>
> **A timeout does not mean the charge failed. It means I do not know.** Marking it failed and letting the
> customer retry is exactly how you charge somebody twice, **and it is the single most common mistake in
> payment code.**
>
> **So the payment goes into an `unknown` state**, and the customer is shown 'processing' rather than either
> outcome.
>
> **Then three mechanisms resolve it, and all three are needed.**
>
> **One: the idempotency key I sent to the provider.** If I retry with the same key, **the provider returns the
> original result rather than charging again.** Every real provider requires this, and that is why.
>
> **And the key has to come from the client when the checkout begins, not per request** — a key generated per
> attempt differs on the retry and deduplicates nothing. **That is the mistake that looks like a solution.**
>
> **Two: a reconciliation job that runs every minute** and asks the provider about anything in `unknown` for
> more than a couple of minutes. **The provider is the source of truth for whether money moved.** My database
> records what I intended; theirs records what happened, **and after a timeout only the second is
> authoritative.**
>
> **Three: the webhook**, which the provider sends on completion. It arrives independently of my request —
> **possibly before my own response returns, possibly instead of it** — so the handler must be idempotent and
> must not assume any ordering.
>
> **Both the webhook path and the reconciliation path write the same ledger transaction with the same
> idempotency key**, so whichever arrives first wins and the other is a harmless no-op. **That is why the
> ledger's own key matters as much as the provider's.**
>
> **And I would verify the webhook's signature before anything else**, because the endpoint is public and
> **anyone can post a 'payment succeeded' event to it**, which without verification is free money.
>
> **The honest summary: I cannot get exactly-once over a network.** What I get is **at-least-once attempted,
> plus deduplication on a key, which produces exactly-once recorded** — and I would state it that way rather
> than claim a guarantee that does not exist."

**"How do you store money, and why not just a balance column?"**

> "Two answers: **integers in the smallest unit**, and **double-entry rather than a balance column.**
>
> **On the representation: never floating point.** `0.1 + 0.2` is not `0.3` in binary floating point, and a
> system that rounds the wrong way a million times a day loses real money and fails its audit. **Store pence,
> paise, cents — as a signed 64-bit integer.**
>
> **And the exponent is not always two.** **Japanese yen has no subunit; Bahraini dinar has three decimal
> places.** Hard-coding two decimal places is a bug that only appears in some countries, which is exactly the
> kind that reaches production.
>
> **Every amount also carries its currency**, because adding rupees to dollars is a bug a type system will not
> catch for you.
>
> **Now double-entry, which is the more interesting half.**
>
> **The naive model is a balance column: one row per account, updated on each payment.** Simple, and it has two
> fatal properties. **An error in it is undetectable** — the number is just wrong and nothing contradicts it.
> **And it is unrepairable**, because there is no record of how it was reached.
>
> **Double-entry records every transfer as two signed entries that sum to zero.** Money leaves one account and
> arrives in another, and the transaction is rejected if the sum is not zero.
>
> **Three properties follow.** **Errors are caught by arithmetic, the same day.** **The balance is derived** —
> the sum of an account's entries — so it can be recomputed at any time and a corrupted cache is repaired
> rather than investigated. **And the ledger is append-only**: a mistake is fixed with a compensating pair, so
> the history is complete.
>
> **That last one matters more than it looks.** A reversed payment appears as **two transactions, not as an
> absence** — which is more confusing to read and is exactly what an auditor requires.
>
> **The cost is double the rows and a derived balance that needs snapshots for performance** — a busy account
> accumulates millions of entries and summing them gets slow. **But the snapshot is a cache: you can throw all
> of them away and recompute, which is the property that makes the whole model safe.**
>
> **And this is a five-hundred-year-old idea**, which is worth saying: it is a solved problem, and the job is
> to implement it correctly rather than invent something."

**"How do you know your numbers are right?"**

> "You do not, from inside your own system — **which is the point of reconciliation, and it is the half people
> forget.**
>
> **Double-entry catches internal errors.** If the entries do not sum to zero, something is wrong. **But it
> cannot catch a payment that your system recorded and the bank never processed**, because both of your entries
> are perfectly consistent with each other and both are wrong.
>
> **So: every day, take the provider's settlement file and compare it against the ledger, line by line.**
>
> **And you will always find discrepancies.** Typically a hundredth to a tenth of a percent — at ten million
> payments a day, **that is one to ten thousand items.** **A run reporting zero discrepancies almost certainly
> means the job is broken**, and I would alert on that too.
>
> **Four categories, and they need different responses.**
>
> **In your books and not theirs** — usually **timing**, a payment that fell after their cut-off, which
> resolves tomorrow. Occasionally a payment that silently failed.
>
> **In theirs and not yours** — a webhook you missed, or a chargeback initiated on their side that you have
> not seen.
>
> **Amounts that differ** — **this is the alarming one.** A fee you did not model, a partial capture, or a
> genuine bug. **At ten million payments a day it might be ten items, and every one needs a human.**
>
> **And timing differences around the cut-off**, which are expected and self-resolving.
>
> **The useful metric is not the discrepancy count — it is the age of the oldest unresolved item.** A thousand
> items resolving within a day is healthy; **three items that have been open for a week is an incident.**
>
> **And this is Zubeida's husband's point, which I think is the right framing.** Her book was right about what
> she wrote down; the bank's statement was right about what happened. **Those are different, the difference is
> always something, and finding it is the job — not a sign that something has gone wrong.**"

### The model answer

*"Design a payment system for a marketplace: buyers pay, the platform takes a commission, and sellers get paid
out weekly. Ten million payments a day."*

> "A marketplace adds one thing to a plain payment system — **the money sits with the platform between the
> purchase and the payout** — and that is exactly what a ledger is for, so let me build it around that.
>
> **Scale first: ten million payments a day is about fifteen hundred writes a second at peak.** That is an
> ordinary relational workload. **One Postgres primary with replicas, and I would resist distributing it** —
> this is the part that must be exactly right, and it is small.
>
> **Card handling: hosted fields, tokens only. The card number never reaches my servers.** The PCI surface
> alone justifies it.
>
> **The ledger is double-entry, and the marketplace shape makes it earn its place.** A single purchase is not
> two entries, it is four:
>
> **Buyer's account down by the full amount. Seller's payable account up by the amount minus commission.
> Platform revenue up by the commission. And the fee to the payment provider as its own entry.** **All of them
> summing to zero, in one transaction.**
>
> **That is the argument for double-entry in one example**: with a balance column, the commission split is
> arithmetic done in application code and never checked. **With entries, it either balances or the transaction
> is rejected.**
>
> **Money as signed integers in the smallest unit, with the currency on every entry** — and the currency
> exponent looked up, not assumed to be two.
>
> **The payout is then a second transaction, weekly:** seller payable down, bank clearing account up. **And the
> seller's balance is derived from the entries**, so 'how much am I owed' is a query rather than a stored
> number that could drift.
>
> **The payment flow is asynchronous, because the provider takes up to two seconds and sometimes times out.**
> The customer sees 'processing'. **On a timeout the payment goes to `unknown`, never to `failed`** — marking a
> timeout as failed is how you charge twice.
>
> **Three mechanisms resolve unknowns**: idempotency keys generated by the client at checkout, a job that asks
> the provider about anything pending past two minutes, and signature-verified idempotent webhooks. **All three
> write the same ledger transaction with the same key, so whichever arrives first wins.**
>
> **Daily reconciliation against the settlement file, in four categories** — with amount mismatches alerting
> loudly and the others tracked by **age of the oldest unresolved item** rather than by count.
>
> **Two things specific to a marketplace that I would raise.**
>
> **Refunds after payout are the hard case.** If a buyer is refunded after the seller has been paid, **the
> money is gone from my control.** So either payouts are delayed past the refund window, **or the seller's
> future payouts carry a negative balance**, which is a ledger entry and a product policy — and I would want
> that policy decided explicitly rather than discovered.
>
> **And the void-versus-refund asymmetry is worth real money here.** A void before capture costs nothing; **a
> refund after capture loses the original fee and adds another.** At ten million payments averaging forty
> pounds, **a one percent failure-after-capture rate is around a hundred thousand pounds a day.** So every
> check that can fail — stock, seller validity, fraud — **goes between authorise and capture**, and that
> ordering is a business decision as much as a technical one.
>
> **Closing thought on scale.** Infrastructure here is around eighteen thousand dollars a month against
> **eight million pounds a day in card fees**. **The system that must never be wrong is essentially free to
> run** — so whenever there is a choice between the safe option and the clever one, take the safe one, because
> the cost difference does not exist and the failure cost is unbounded."

---

## 9. Recall card

**The mismatch is the design: the business needs exactly-once, the network offers at-least-once.** What you
actually get is **at-least-once attempted + deduplication on a key = exactly-once *recorded*** — say it that
way rather than claiming a guarantee.

**Double-entry: every transfer is TWO signed entries summing to ZERO.** Errors become detectable by
arithmetic; **the balance is DERIVED (a snapshot is a cache you can throw away and recompute)**; and the ledger
is **append-only** — corrections are compensating pairs, never edits. A five-hundred-year-old idea, and the
correct data model.

**Money is signed integers in the smallest unit, never floats** (`0.1 + 0.2 != 0.3`), **and the exponent is
not always 2** — JPY has none, BHD has three. Every amount carries its currency.

**On a timeout, mark it `unknown` — NEVER `failed`.** That single line is the most common bug in payment code.
Resolve with three mechanisms, all needed: **client-generated idempotency keys** (per checkout, not per
request), **a job that asks the provider** (which is the source of truth after a timeout, not your database),
and **signature-verified, deduplicated webhooks** that may arrive before your own response.

**The idempotency insert must BE the lock** — a unique constraint or `SET NX`, because check-then-write has a
window and two concurrent retries both charge.

**Authorise → check → capture, because a VOID is free and a REFUND costs the fee twice and takes days.** At
10M payments/day averaging £40, a 1% failure-after-capture rate is **~£100,000/day**.

**Reconcile daily against the settlement file, in four categories** — timing, missed webhooks, **amount
mismatches (the alarming one)**, and cut-off effects. **You will always find discrepancies; finding none means
the job is broken.** Track the **age of the oldest unresolved item**, not the count. And **infrastructure is
~0.007% of the card fees** — always take the safe option.
