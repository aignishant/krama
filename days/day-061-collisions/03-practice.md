---
day: 61
track: practice
title: "Practice — Collisions, and why a hash map can turn slow"
status: written
---

# Day 061 · Practice

**DSA topic:** Collisions, and why a hash map can turn slow
**System design topic:** Coupling, cohesion, and code smells

---

## Code these, in this order

One rule for the whole set: **make a collision happen on purpose before you reason about one.** A
class whose `__hash__` returns a constant takes six lines and turns every claim in the lesson into
something you can watch.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Design HashSet | LeetCode 705 (Easy) | The same machinery as yesterday, minus the values — so the collision handling is all that is left. |
| 2 | Insert Delete GetRandom O(1) | LeetCode 380 (Medium) | Deletion done right: a dict plus a list, with the swap-with-last trick. |
| 3 | LRU Cache | LeetCode 146 (Medium) | A hash map that must also maintain order — where the dict alone is not enough. |
| 4 | Design HashMap | LeetCode 706 (Easy) | Write it a second time, with open addressing and tombstones instead of chaining. |

### On problem 2, notice which deletion problem you are solving

`remove` must be `O(1)`, so you cannot shift a list. The trick is to swap the doomed element with the
last one and pop. Say out loud what has to be updated when you do that, and why forgetting it is
exactly the "unreachable entry" failure in a different costume.

### On problem 4, use open addressing this time

You wrote chaining yesterday. Write it with probing today, with three slot states. Then, before you
submit, deliberately implement `remove` by blanking the slot, and find an input where a later `get`
returns the wrong answer. Say what you had to construct to make it fail.

### The collision drill

1. Write a `Colliding` class whose `__hash__` returns 42 and whose `__eq__` compares a name.
2. Put five of them in a `dict`. Does `len` say 5? Can you retrieve each one?
3. State, in one sentence, what collisions cost and what they do not cost.
4. Now put ten thousand of them in a dict and time it. Time ten thousand normal string keys.
5. Compute the ratio and say which complexity each case is.
6. Say what would happen to the same experiment in Java 8 or later, and why.

### The probing drill

Using your open-addressed table with capacity 8:

1. Insert four keys that all hash to slot 3. Draw the slot array afterwards.
2. How many probes did the fourth insert take?
3. Insert a fifth key hashing to slot 4. How many probes now, and why is that number bigger than you
   would expect?
4. Explain, in one sentence, why a cluster grows faster than it "should".
5. Say what quadratic probing changes and what it does not.
6. Say what double hashing changes, and what Python does that is in the same spirit.

### The tombstone drill

1. Build a table where key `b` probed past key `a`.
2. Delete `a` by blanking its slot. What does `get(b)` return? Does anything raise? What does `len`
   say?
3. Now do it with a tombstone. What does `get(b)` return?
4. Write the rule for how a lookup treats a tombstone, and how an insert treats one.
5. Insert twenty items and delete eighteen. Count the tombstones and compute both load factors — by
   `size` and by `used`.
6. Say what would go wrong if the resize triggered on `size` instead.
7. Say the surprising sentence this leads to, in one line.

### The load-factor drill

Fill a fixed-capacity table to each load and measure the average probes per lookup:

1. 0.25
2. 0.50
3. 0.66
4. 0.75
5. 0.90
6. 0.95

Then answer: where does the curve turn, why do implementations resize at about two-thirds rather than
reacting to slowness, and how would the same table look with chaining?

### The bad-hash drill

For each hash function, predict the distribution and then measure it with two thousand realistic
keys:

1. `hash(self.order_id[:4])` where every id starts `"ORD-"`.
2. `hash(len(self.name))`.
3. `hash(self.name[0])`.
4. `hash((self.first, self.last))`.
5. `return 0`.
6. `id(self)`, on a class that also defines `__eq__` by value.

Two of those six are broken in a way that has nothing to do with distribution. Name them.

### The break-it drill

Trigger each, read the output, and give the fix in one sentence:

1. Delete by blanking a slot in an open-addressed table, then look up an entry that probed past it.
2. Resize on `size` rather than `used`, under an insert-and-delete workload.
3. Mutate a key's hashed field after insertion, then `key in d`.
4. Insert one million integers stepping by exactly the table capacity into a hand-written table with
   `% capacity` and linear probing.
5. `python -c "print(hash('apple'))"` twice.
6. Assert a specific `hash()` value in a test, then run it again.

### The attack drill

1. Write a class with a constant hash and insert `n` of them, for `n` = 1,000, 5,000 and 20,000. Time
   each.
2. Plot or tabulate the times. What is the growth rate?
3. Compute the comparisons for `n = 20,000` and compare with the non-colliding case.
4. Say what an attacker would send to a web server to cause this, and why it worked across almost
   every language in 2011.
5. Name Python's defence and the two rules that follow from it for your own code.
6. Name Java's different defence and say what complexity it gives the flooded bucket.

### The review drill

Here is the module. Do not rewrite it yet.

```python
# billing/charger.py
import stripe
import psycopg

SETTINGS = {}

class Charger:
    def __init__(self, conn):
        self.conn = conn

    def charge(self, invoice, retry=False, partial=False, dry_run=False, notify=True):
        email = invoice.customer.contact.email.address
        amount = invoice.total_paise if not partial else invoice.total_paise // 2
        if dry_run:
            return "DRY"
        result = stripe.Charge.create(api_key=SETTINGS["stripe_key"],
                                      amount=amount, currency="inr",
                                      receipt_email=email)
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO charges (invoice, amount, ref) VALUES (%s,%s,%s)",
                        (invoice.id, amount, result["id"]))
        if notify:
            stripe.Email.send(email, f"Charged {amount/100} rupees")
        return result["id"]
```

1. Describe it in one sentence. Count the "and"s.
2. Name every distinct job it does, and the team that would own each.
3. Which smell is that? Name it.
4. Find the message chain. How many classes does that one line depend on?
5. Find the control coupling. How many combinations does the signature allow, and how many are
   meaningful? Which combination is nonsense but compiles?
6. Find the common coupling and say what breaks in tests because of it.
7. Find the stamp coupling. What does the amount calculation actually need?
8. Count the fan-out to external systems. What does that mean for testing?
9. Name the two missing concepts. What would you call them?
10. Rewrite it. Then write the test for "a partial charge is half the total" and count the lines of
    setup before and after.
11. Which single change would you make first, and why that one?
12. What would you look at before making any change at all?

### The smell-naming drill

Name the smell, say what it usually means, and give the fix:

1. `order.customer.address.city.name`
2. `def render(report, as_pdf=False, as_csv=False)`
3. A method on `Invoice` that uses six fields of `Customer` and none of its own.
4. `line1`, `line2`, `city`, `pincode` passed together in nine functions.
5. `phone: str` with the format checked in four places.
6. `db.configure()` must be called before `db.query()`.
7. A class whose every method is `return self._inner.same_method(...)`.
8. `utils.py`, 900 lines, 40 functions.
9. One file with commits from finance, marketing, platform and operations.
10. Adding one field means editing ten files.

Two of the ten are the *diagnostic* pair. Name them and say which fix each one gets.

### The coupling-ladder drill

For each call, name the level of coupling and say what would have to change to move it one rung
better:

1. `emailer._smtp.sendmail(...)`
2. `CONFIG["smtp_host"]`
3. `send(user, is_admin=True)`
4. `send_welcome(user)`
5. `send_welcome(user.email)`
6. `events.publish(UserSignedUp(email))`

### The cohesion drill

Name the level of cohesion, and say what the module would look like at the next level up:

1. `utils.py` with `slugify`, `retry`, `parse_date` and `send_sms`.
2. `validators.py` with every validator in the system.
3. `startup.py` that opens the log, connects the database, loads config and warms the cache.
4. `Address` with `format_label`, `validate_pincode` and `is_deliverable`.
5. `Matrix` with `multiply`, `transpose`, `invert` and `determinant`.

Two of those five are already fine. Name them and defend it.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *What is the worst-case complexity of a hash map lookup? When does it happen?*
   Both halves immediately, collisions as the normal condition with the birthday number, the two
   strategies and their trade, tombstones volunteered before being asked, and the three real causes.

2. *Review this module. What would you change?*
   The two-sentence framing, the one-sentence test with the "and"s counted, the specific smells with
   evidence rather than labels, what you would change first and why, and the version history you
   would go and look at.

3. *How would you implement deletion in an open-addressed table?*
   Start with what goes wrong, then the three slot states, then the tombstone accumulation problem
   and the counter that fixes it — ending on the surprising sentence about shrinking maps.

---

## Before you move on

- [ ] I built a collision on purpose and confirmed the dictionary was still correct.
- [ ] I broke deletion by blanking a slot and watched an entry become unreachable with no error.
- [ ] I can state the lookup rule for a tombstone and the insert rule, without hesitating.
- [ ] I measured the probe count at five load factors and can describe the shape of the curve.
- [ ] I can say why a shrinking hash map can need a rehash.
- [ ] I can name the three real causes of `O(n)` lookups and give an example of each.
- [ ] I reviewed `Charger` and named at least five smells with evidence, not just labels.
- [ ] I can give both ladders — coupling and cohesion — from worst to best.
- [ ] I answered all three questions above out loud.
