---
day: 58
track: practice
title: "Practice — Custom comparators and sorting by keys"
status: written
---

# Day 058 · Practice

**DSA topic:** Custom comparators and sorting by keys
**System design topic:** Interface segregation

**Theme:** Testing a service

---

## Code these, in this order

One rule for the whole set: **say the key out loud as a sentence before you type it.** "Negative
score first so high scores come first, then name so it only decides ties." If you cannot say it, you
do not have it.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Sort Array By Parity II | LeetCode 922 (Easy) | That not every ordering problem is a sort — sometimes the key is a placement rule. |
| 2 | Sort Characters By Frequency | LeetCode 451 (Medium) | Two keys in opposite directions, with a count you have to build first. |
| 3 | Largest Number | LeetCode 179 (Medium) | The one problem where no per-element key exists. `cmp_to_key`, and the sign convention. |
| 4 | Reorder Data in Log Files | LeetCode 937 (Medium) | A tuple key mixing types and a group that must keep its original order — stability in production. |

### On problem 2, hit the wall on purpose

Sort by frequency descending, then character ascending. Do it with one tuple key (you can — frequency
is a number). Then invert the requirement to "character descending, frequency ascending", try the
tuple key, paste the `TypeError`, and solve it in two passes. Say which pass goes first and why.

### On problem 3, say the convention out loud before you write it

The comparison function returns a **negative** number when the **first** argument should come first.
Write that on the board. Then handle the `[0, 0]` case, which is the test that catches people —
`"00"` is not a valid answer.

### On problem 4, find the stability requirement

Digit-logs must stay in their original relative order. That is not something you sort — it is
something you must not disturb. Say out loud how your key achieves that, and what would happen with
an unstable sort.

### The key-function drill

Write each in one line, then check it:

1. Words by length, then alphabetically.
2. Words by length descending, then alphabetically ascending.
3. Files by extension, then by size descending.
4. People by city ascending, age descending, name ascending.
5. Strings by their last character.
6. Tuples by the second element, falling back to the first.
7. Dictionaries by `d["score"]`, treating a missing score as zero.
8. Names case-insensitively, with ties broken by the original case-sensitive value.

### The opposite-directions drill

For each, say which of the three techniques you would use — negate, two passes, or a wrapper — and
why the other two are wrong or unavailable:

1. Score descending, name ascending.
2. Name descending, score ascending.
3. Date descending, id ascending.
4. Department descending, salary descending.
5. Priority ascending, created-at descending, title ascending.
6. Status by a custom order, then name descending.

### The break-it drill

Run each and record the output or the error:

1. `sorted(students, key=lambda s: (s.score, s.name), reverse=True)` — what is wrong with the output,
   and why is there no error?
2. `sorted(people, key=lambda p: (-p.name, p.age))` — paste the error.
3. `sorted(words, key=len(words))` — paste the error.
4. `sorted([Student("Asha", 90), Student("Bala", 85)])` on a plain dataclass — paste the error.
5. `sorted(tickets, key=lambda t: STATUS_ORDER[t["status"]])` with one unknown status — paste the
   error, then fix it two ways and say which you prefer.
6. A comparator that never returns 0. Sort ten items with it and say what guarantee you have lost.

### The call-count drill

1. Instrument a key function with a counter and sort 1,000 elements. How many calls?
2. Do the same with `cmp_to_key`. How many calls now?
3. Compute the ratio, and say what it would be at a million elements.
4. Time `key=attrgetter("score")` against `key=lambda s: s.score` on 500,000 records.
5. Estimate the memory used by the keys when sorting a million records with a two-element tuple key.
6. Given all that, state the rule for when to use `cmp_to_key` in one sentence.

### The determinism drill

1. Sort 1,000 tickets by status alone, where 400 share a status. Shuffle the input and sort again.
   Do you get the same output?
2. Add a unique tie-break and repeat. What changed?
3. Say what class of test failure this prevents.
4. Sort with `key=lambda x: random.random()`. What does Python guarantee about the result? What
   should you use instead?

### The interface-segregation drill

Here is the interface. Do not refactor it yet.

```python
class OrderStore(Protocol):
    def get(self, order_id: str) -> Order: ...
    def save(self, order: Order) -> None: ...
    def delete(self, order_id: str) -> None: ...
    def find_by_customer(self, customer_id: str) -> list[Order]: ...
    def stream_all(self) -> Iterator[Order]: ...
    def bulk_import(self, orders: list[Order]) -> None: ...
    def begin_transaction(self) -> Transaction: ...
    def rebuild_index(self) -> None: ...
```

And its callers:

```
  order_confirmation_email(store, order_id)   calls: get
  customer_order_history(store, customer_id)  calls: find_by_customer
  nightly_csv_export(store, path)             calls: stream_all
  admin_delete_order(store, order_id)         calls: get, delete
  checkout(store, order)                      calls: get, save, begin_transaction
  data_migration(store, rows)                 calls: bulk_import, rebuild_index
```

1. Build the table: for each caller, methods called against methods depended on. Total the forced
   dependencies.
2. Group the callers by the set of methods they use. How many clusters?
3. Name each cluster as a role interface. Use `-er` names. Reject any name you find awkward and say
   why.
4. Write the `Protocol` declarations. How many lines?
5. Rewrite the six caller signatures.
6. Which implementations had to change? Answer honestly, and say what feature of Python makes that
   answer what it is.
7. Write the test fake for `order_confirmation_email` before and after. Count the lines of each.
8. Someone wants to add `archive(order_id)`. Which interface does it go on, and how many files change
   now compared with before?

### The NotImplementedError drill

For each, say whether the `NotImplementedError` is an interface segregation failure or something
legitimate:

1. `CsvRepository.save` raising, because the file is read-only.
2. An abstract base class's `body()` raising, with subclasses required to supply it.
3. `Robot.eat` raising, in a `Worker` interface.
4. `InMemoryCache.persist` raising, because there is no disk.
5. A `Shape.volume()` raising for two-dimensional shapes.
6. A method in a `Protocol` body — `def get(self) -> Row: ...` — which is not raising at all.

### The role-naming drill

Rename each header interface into one or more role interfaces, and say which callers would take each:

1. `UserService` with 12 methods.
2. `FileManager` with `read`, `write`, `delete`, `list`, `compress`, `upload`.
3. `Machine` with `print`, `scan`, `fax`, `staple`.
4. `PaymentProvider` with `charge`, `refund`, `list_transactions`, `configure_webhook`.
5. `Cache` with `get`, `set`, `delete`, `flush_all`, `stats`.
6. `Logger` with `debug`, `info`, `warn`, `error`, `set_level`, `add_handler`.

Two of those six are probably fine as they are. Name them and defend it.

---

## Build these, in all three languages

*Three exercises, easiest first. Each one says what it is really testing. Every
exercise is done three times: once in Python, once in Go, once in C++.*

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Make the tests fail on purpose | That each test can actually fail, and fails for the reason it claims to protect. |
| 2 | The timeout case | Turning a slow dependency into a 504 without ever waiting for it in the test. |
| 3 | A second dependency behind the seam | Adding a stock service, mocking two things at once, and asserting what each was asked. |

All three start from the lesson's price service and its four tests. Keep the Wi-Fi off for every
run; if a test needs it, the test is wrong.

### 1. Make the tests fail on purpose

Break the handler four ways, one at a time, and run the suite after each: return the rupee price
without converting; return 500 instead of 404 for a missing item; call the rate source even when
the currency is INR; and swallow the rate source's failure and return 200 with a price of zero.
Each break must make exactly one test fail, and you must be able to say which assertion caught it.
The third break is the interesting one: in Python it is `route.called`, in Go it is the `calls`
column, in C++ it is `Times(0)`. Undo each break before the next. Done means four breaks, four
single failures, and the name of the assertion that caught each, in all three languages.

### 2. The timeout case

The rates service is not down; it is slow. In Python, mock the route with
`side_effect=httpx.TimeoutException("slow")`; in Go, have the fake return `context.DeadlineExceeded`;
in C++, have the mock `Throw` a `std::runtime_error("timeout")`. The handler should answer 504,
not 502, and the test should assert it. Then the harder half: prove the test itself never waits.
Time the suite before and after; if the timeout test added seconds, the mock is not intercepting
and the real timeout is running. Done means a 504, a distinct error code in the body, and a suite
that is no slower than before, in all three languages.

### 3. A second dependency behind the seam

Add a stock service: `GET /price/{sku}` must also report `"in_stock": true` or `false`, from a
second outside call. Put it behind the same kind of seam as the rates service: a second respx
route in Python, a second interface and fake in Go, a second abstract base and mock in C++. Write
one test where rates answers and stock is down, and one the other way round, and say which
status each should produce and why they might differ. Assert on what each stand-in was asked.
Done means two seams, both mocked, both failure orders tested, and the same four statuses in all
three languages.

## Compare

*One sentence per language: what was easiest, what was hardest, and why.*

- **Python** — Easiest to retrofit, because respx patches `httpx` from outside and `dependency_overrides` swaps a function by identity, so nothing in the route had to be designed for testing; hardest is remembering `clear()` so the override does not leak.
- **Go** — Easiest to read, because the fake is a ten-line struct and the table names every case; hardest is that the seam must be an interface in the design, and `:memory:` needs `SetMaxOpenConns(1)` or the table vanishes between connections.
- **C++** — Easiest to assert with, because gMock checks counts and arguments for you; hardest is that there is no in-process client, so the fixture must bind, thread, wait until ready, stop, and join, and each of those can race.

## Say these out loud

### DSA and system design

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Sort by score descending, then by name ascending.*
   The tuple key with the negated number, read aloud as a sentence, why `reverse=True` is the trap,
   and what you would do if the descending field were a string.

2. *Why is a single large interface a problem?*
   Both costs — forced lies producing Liskov violations, and churn reaching callers that do not care
   — with the forced-dependency count, and then the Python `Protocol`-at-the-consumer answer.

3. *When would you need a comparator instead of a key?*
   The largest-number example, why no per-element key exists there, the sign convention, and the cost
   ratio that makes it the last resort.

### Languages

*Three questions from today. Answer each in two minutes, standing up, no notes.*

1. How do you test code that calls another service?
2. What is the difference between a fixture, a fake, and a mock, and which of today's three pieces is which?
3. Why does the Python version need no interface, and what does that cost the Go and C++ versions?

## Before you move on

- [ ] I can write the score-descending-name-ascending key in one line and read it aloud as a
      sentence.
- [ ] I ran the `reverse=True` version and can say exactly which part of the output is wrong.
- [ ] I hit the string-negation `TypeError` and solved it with two passes, least significant first.
- [ ] I instrumented the call count for `key` and for `cmp_to_key` and can quote the ratio.
- [ ] I can state the `cmp_to_key` sign convention without hesitating.
- [ ] I built the forced-dependency table for `OrderStore` and can give the total.
- [ ] I can say what makes narrow interfaces nearly free in Python and expensive in Java.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
