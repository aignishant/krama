---
day: 54
track: practice
title: "Practice — Quicksort and partitioning"
status: written
---

# Day 054 · Practice

**DSA topic:** Quicksort and partitioning
**System design topic:** Object-oriented design revision and interview questions

**Theme:** Databases II: Postgres and connection pools

---

## Code these, in this order

One rule for the whole set: **write `partition` on its own and check the returned position before you
write the sort.** Every quicksort bug is a partition bug or a recursion-bounds bug.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Sort Colors | LeetCode 75 (Medium) | A three-way partition with the pivot value fixed at 1 — the Dutch flag, in its purest form. |
| 2 | Partition Array According to Given Pivot | LeetCode 2161 (Medium) | Three-way partitioning where *stability* is required, so the in-place swap version is wrong. |
| 3 | Sort an Array | LeetCode 912 (Medium) | Whether your quicksort survives sorted input and 50,000 duplicates. |
| 4 | Wiggle Sort II | LeetCode 324 (Medium) | Partitioning as a tool rather than a sort — find the median, then place around it. |

### On problem 1, write it as a partition, not as counting

The counting solution (count the 0s, 1s and 2s, then overwrite) is two passes and it is fine. Write
it, then write the one-pass three-region version, and say out loud which region each of `low`, `i`
and `high` bounds. Then answer: why does `i` not advance when you swap with `high`?

### On problem 2, discover why stability matters

Solve it with the in-place three-way swap first and check it against the expected output. It fails,
and the reason is that the problem requires the original relative order to be preserved inside each
group. Say out loud which of the sorts you know are stable, and why partitioning cannot be.

### On problem 3, break it deliberately, then fix it

1. Submit quicksort with a last-element pivot. Note the verdict on the sorted-input test case.
2. Add the two lines of random pivot selection. Submit again.
3. Now build a list of 50,000 identical values locally and run your version on it. If you used `<=`
   in the partition, paste the `RecursionError`.
4. Switch to the three-way partition and run the same input. Say the before-and-after operation
   counts.

### On problem 4, use the partition without sorting

Wiggle Sort II needs the median, and the median comes from quickselect — tomorrow's topic, built on
today's partition. Solve it with `sorted()` first to get the placement rule right, then say out loud
what you would replace the sort with and what the complexity becomes.

### The partition drill

Write `partition` from memory, then verify by hand:

1. `partition([7, 2, 9, 4, 1, 8, 3], 0, 6)` — what does it return, and what is the list afterwards?
2. `partition([1, 2, 3], 0, 2)` — where does the pivot land, and what does that mean for the
   recursion?
3. `partition([3, 2, 1], 0, 2)` — the same question in reverse.
4. `partition([5, 5, 5, 5], 0, 3)` — with `<` and then with `<=`. Compare the returned positions.
5. `partition([2], 0, 0)` — does it terminate?

For each, state the invariant that holds at the moment the loop ends.

### The worst-case drill

Run the comparison counter from §5 of the lesson and record the numbers:

1. 500 sorted values, first-element pivot.
2. 500 sorted values, random pivot.
3. 500 reversed values, first-element pivot.
4. 500 reversed values, median-of-three pivot.
5. 500 identical values, two-way partition with `<`.
6. 500 identical values, three-way partition.

Then say, without looking: which input is the surprising one, and why is it surprising?

### The break-it drill

Introduce each bug, run it, and read the failure:

1. `quicksort(nums, lo, p)` instead of `p - 1`. Paste the error and say which pivot placement causes
   it.
2. `<=` instead of `<` in the partition, on a list of 3,000 equal values. Paste the error.
3. Last-element pivot on `list(range(5000))`. Paste the error and say why an already sorted list is
   the worst case.
4. Use Hoare's partition but recurse with `p - 1` and `p + 1`. Find an input where the output is
   wrong.
5. In the three-way partition, advance `i` after swapping with `gt`. Find the input that breaks it.

### The complexity drill

Answer out loud, in under fifteen seconds each:

1. What is quicksort's worst case, and what input causes it?
2. Why does randomising the pivot fix it? What exactly does it change?
3. What is the expected number of comparisons, and how does that compare with merge sort's?
4. Why is quicksort faster in practice despite doing *more* comparisons?
5. What is the extra space, and what is the recursion depth — with and without the smaller-side
   trick?
6. Name the three pivot strategies and one weakness of each.

### The design drill

Set a timer for twenty minutes and run the five moves out loud on this prompt:

> *Design the classes for a cinema ticket booking system. A chain has several cinemas; each cinema
> has several screens; each screen shows several shows a day; each show has seats of two classes.
> Users search by film and city, pick seats, pay, and can cancel up to two hours before the show for
> a partial refund. Prices vary by day of week and seat class.*

1. **Minutes 0-5** — four clarifying questions and the assumptions you will proceed on. Name what you
   are leaving out.
2. **Minutes 5-10** — the nouns, one sentence each. Then the noun that is *not* in the paragraph, and
   what has nowhere to live without it.
3. **Minutes 10-15** — the class diagram, with a multiplicity on every line.
4. **Minutes 15-20** — the one flow that matters, coded: seat selection and payment.

Then answer the three questions you know are coming:

- *Two users select the same seat at the same instant. What happens?*
- *Where did you put an interface, and where did you deliberately not?*
- *Now add a "book the whole row" feature.*

### The missing-noun drill

For each prompt, name the class that is not in the sentence, and say what has nowhere to live without
it:

1. "A guest books a room."
2. "A user picks seats for a show."
3. "A car parks in a spot and pays on exit."
4. "A member borrows a book."
5. "A rider requests a ride to a destination."
6. "A customer orders food from a restaurant."

### The race-condition drill

For each, name the check-then-write gap, say what two users see when it goes wrong, and give the
atomic fix as a single operation:

1. The last hotel room.
2. The last cinema seat.
3. The last parking spot.
4. Two withdrawals from the same account balance.
5. Two users claiming the same username.
6. A stock counter reaching zero during a flash sale.

### The interface-justification drill

For each, say whether you would create an interface, and name the second implementation — or say
plainly that you cannot:

1. Pricing in a hotel booking system.
2. `IHotel`.
3. The cancellation policy.
4. The payment gateway.
5. `IRoom`.
6. The booking repository.

---

## Build these, in all three languages

*Three exercises, easiest first. Each one says what it is really testing. Every
exercise is done three times: once in Python, once in Go, once in C++.*

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Measure the handshake | Whether you can put a number on what a connection costs, on your own machine. |
| 2 | Exhaust the pool on purpose | Recognising a pool timeout, and telling a slow database from a held connection. |
| 3 | The server on a pool | Moving the day 50 CRUD server from SQLite to Postgres with a shared pool and no per-request connect. |

All three need the Postgres container from the lesson running, and `DATABASE_URL` set in the
environment. Delete and recreate the `users` table between exercises with
`docker exec pg psql -U postgres -d app -c "DROP TABLE IF EXISTS users"`.

### 1. Measure the handshake

Time two hundred `SELECT 1` calls two ways: opening a fresh connection for each, and borrowing
from a pool of four for each. Print both totals and the per-call average. Then run the
per-call version with three hundred threads or goroutines at once against a Postgres with
`max_connections` left at its default, and paste the error you get. Done means the two averages
pasted per language, the ratio between them said out loud, and the `too many clients` error
captured in at least one language.

### 2. Exhaust the pool on purpose

With a pool of four, start four holds of `pg_sleep(10)` on four threads, then make a fifth
ordinary query with a two-second timeout. Paste the error: `PoolTimeout` in Python,
`context deadline exceeded` in Go, your own `no connection free` in C++. Then, while the four
holds are running, run `docker exec pg psql -U postgres -d app -c "SELECT pid, state, query FROM pg_stat_activity WHERE datname = 'app'"`
and paste the four `pg_sleep` rows. Write two sentences under it: what you would see there if
the database were slow instead, and what you would see if code were holding connections
without querying. Done means the three errors pasted, the activity rows pasted, and the two
sentences written.

### 3. The server on a pool

Port the day 50 CRUD server to Postgres in each language: one pool created at start-up from
the day 51 settings, every handler borrowing from it, `$1` or `%s` placeholders, `RETURNING id`
on the create, the unique violation mapped to 409, and no connection opened anywhere except in
the pool's constructor. In Go, every query takes `r.Context()`. Run the twelve curl commands
from day 50 against it and paste the twelve status lines. Then run the day 48 load test,
fifty POSTs at once, against the pool of four and paste the pool's stats afterwards. Done means
twelve correct status lines per language and a load test that finished with no connection
opened per request.

## Say these out loud

### DSA and system design

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Write quicksort. What is its worst case, and when does it happen?*
   The partition with its invariant, the excluded pivot in the recursion, `O(n²)` on **sorted** input
   with a fixed pivot, and the two lines that fix it — plus what randomising actually changes.

2. *Design the classes for a hotel booking system.*
   The five moves on a clock, the missing noun, the two justified interfaces, and the
   check-then-write race named before you are asked.

3. *Quicksort or merge sort?*
   In place and fast against guaranteed and stable, with the numbers — and the three situations where
   merge sort is the only answer.

### Languages

*Three questions from today. Answer each in two minutes, standing up, no notes.*

1. Why do you need a connection pool?
   What a connection costs on both ends, the `max_connections` cap, where the queue forms with
   and without a pool, and why the size is not "as many as possible". Then one sentence on the
   thing that breaks a pool: holding a connection across slow work.
2. How would you implement a connection pool?
   The vector, the mutex, the condition variable with `wait_for` and a predicate, the lease
   whose destructor returns the connection, and the timeout. Then say what Python's `with
   pool.connection()` and Go's `pool.Begin` are doing in those terms.
3. What does the context do on a Go database call, and what is the equivalent elsewhere?
   Bounding the wait for a connection, cancelling the running query when the caller is gone,
   `r.Context()` in a handler; then the honest answer for Python and C++, where the wait is
   bounded but a running query is not cancelled.

## Before you move on

- [ ] I wrote `partition` from memory and can state its invariant at the moment the loop ends.
- [ ] I crashed quicksort on an already sorted list and can explain why that input is the worst case.
- [ ] I crashed it again on 3,000 equal values with `<=` and can say what the one character changed.
- [ ] I can give the three pivot strategies and one weakness of each, unprompted.
- [ ] I ran the twenty-minute cinema design out loud, including the missing noun and the race.
- [ ] I can name the check-then-write gap in six different prompts and give the atomic fix for each.
- [ ] I can say which interfaces I would create and name the second implementation for each.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] The three lesson programs run against the container and print the two-second line for five holds on a pool of four.
- [ ] Exercise 1 gives me a per-connection cost in milliseconds on my machine, and I have seen `too many clients already`.
- [ ] Exercise 2's three timeout errors are pasted with the `pg_stat_activity` rows, and my two sentences tell a slow database from a held connection.
- [ ] Exercise 3's servers pass the twelve day 50 commands on Postgres with one pool and no per-request connect.
- [ ] I can say the pool's four parts, vector, mutex, condition variable, lease, and what each prevents.
- [ ] I can say why a transaction must stay on one borrowed connection, and what `$1` versus `%s` versus `?` means.
