---
day: 51
track: practice
title: "Practice — Why sorting matters more than any single sorting algorithm"
status: written
---

# Day 051 · Practice

**DSA topic:** Why sorting matters more than any single sorting algorithm
**System design topic:** Modelling a real domain

**Theme:** Configuration: flags, environment, files

---

## Code these, in this order

One rule for the whole set: **before writing anything, say out loud whether sorting helps, which of
the four payoffs you want, and what the cost becomes.** On one of these four the answer is no, and
spotting which is the point.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Minimum Absolute Difference | LeetCode 1200 (Easy) | The purest form: closest-in-value becomes adjacent-after-sorting. |
| 2 | Merge Intervals | LeetCode 56 (Medium) | That the sort *is* the algorithm, and which field you sort on. |
| 3 | 3Sum | LeetCode 15 (Medium) | One sort buying two things — the two-pointer sweep and easy duplicate skipping. |
| 4 | Two Sum | LeetCode 1 (Easy) | The trap: sorting is slower here *and* destroys the answer. |

### On problem 1, say the proof before the code

*If two values are the closest pair, nothing lies between them in value — so after sorting, nothing
lies between them in position either.* Then two lines. Then state the cost both ways: n(n−1)/2 against
n log n + n, and the ratio at a million.

### On problem 2, get the key right and prove it matters

Sort by **start**, then one pass. Then deliberately sort by `iv[1]` instead and run it on
`[[1, 4], [0, 2], [3, 5]]` — you get a plausible wrong answer with no error. Say the difference: merge
by start, pack the most non-overlapping meetings by end. When the sort is the algorithm, the key is
the algorithm.

### On problem 3, notice the sort is doing two jobs

Write it, then find both payoffs in your own code: the two-pointer sweep needs order, and the
duplicate-skipping `while` loops need equal values to be adjacent. Say "one sort, two payoffs" out
loud — that is why the O(n log n) is almost never the thing you regret.

### On problem 4, write the wrong version first

Write the sort-plus-two-pointers version. Run it on `[3, 2, 4]` with target 6 and read the answer:
`[0, 2]`, which are positions in the *sorted* list, not the input. No exception. Then write the
dictionary version, say it is O(n) rather than O(n log n), and say the second reason it is better —
it never had the indices to lose.

### The four-payoffs drill

For each problem, name which of the four things sorting buys — equal-adjacent, near-adjacent, binary
search / early exit, or a correct greedy order:

1. Are there any duplicates?
2. What is the smallest difference between any two values?
3. How many values lie between 10 and 44?
4. Merge overlapping intervals.
5. Group anagrams together.
6. What is the maximum number of non-overlapping meetings?

Two of these have a better non-sorting answer. Name them and say what it is.

### The don't-sort drill

For each, say whether to sort — and if not, what instead, with the cost:

1. Find the ten largest of a million values.
2. Find whether any value appears twice.
3. Find the indices of two values summing to a target.
4. Find the median of a stream that will not fit in memory.
5. Answer a thousand "how many values in [a, b]" queries on a fixed array.
6. Find the two closest values.

### The arithmetic drill

Answer with numbers, in under ten seconds each:

1. Comparisons to sort a million elements.
2. Comparisons to compare every pair of a million elements.
3. The ratio between those two.
4. Operations for the ten largest of a million: full sort, heap, quickselect.
5. The break-even query count for "sort once and binary search" against "scan every time" at
   n = 100,000.

### The Python drill

Say what each does, and which is right for which situation:

1. `nums.sort()` versus `sorted(nums)` — return value, space, and what happens to the caller's list.
2. `key=lambda p: (p.city, -p.age)` — what order, and why the minus sign is needed rather than
   `reverse=True`.
3. Two-pass sorting by city then name — which pass goes first, and what property makes it work.
4. `sorted((value, i) for i, value in enumerate(nums))` — what problem does this solve.
5. `sorted([3, "1", 2])` — paste the exact error.
6. How many times is `key` called for a list of n elements?

### The modelling drill

Set a timer for fifteen minutes and model this out loud, running the six steps in order:

> *A gym sells memberships. A member books classes; each class has a trainer, a room and a capacity. A
> member can cancel up to two hours before a class and the slot goes back on sale. Members on a
> monthly plan can book unlimited classes; members on a ten-class pack lose a credit per booking, and
> a cancellation returns it.*

1. Nouns and verbs, in the gym's words. Then three questions that would change the model.
2. Entities against value objects, with the "would I care which one I got" test applied to at least
   two.
3. The noun that is not in the paragraph. Name it, and say exactly what has nowhere to live without
   it.
4. Three invariants, as sentences.
5. The aggregate roots, and what is referenced by id from outside — with the invariant that justifies
   each boundary.
6. Where the cancellation rule goes, and the one-sentence reason. Then where the credit rule goes, and
   whether it is the same object.

Then answer the extension you know is coming: *"now a class can be booked by a member on behalf of a
guest."* Say what changes and what does not.

### The vocabulary drill

Define each in one sentence, then give one example from the gym model:

1. Entity.
2. Value object.
3. Aggregate root.
4. Repository — and how many you would have for the gym.
5. Domain service — and why it is the last resort.
6. Ubiquitous language.
7. Bounded context — and where one would appear in a gym chain.

### The missing-noun drill

For each requirement, name the class that is not in the sentence, and say what has nowhere to live
without it:

1. "Members borrow books."
2. "A customer books a seat for a show."
3. "A vehicle parks in a spot and pays on exit."
4. "Parcels travel between hubs and each movement is recorded."
5. "Employees claim expenses, which a manager approves."
6. "A patient sees a doctor and is prescribed medicines."

---

## Build these, in all three languages

*Three exercises, easiest first. Each one says what it is really testing. Every
exercise is done three times: once in Python, once in Go, once in C++.*

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Prove the order | Whether each layer really overrides the one below and leaves the rest alone. |
| 2 | Refuse the password in the file | Turning "never" into a check the program makes, not a rule people remember. |
| 3 | Wire it into the server | Replacing every hard-coded value in the day 50 server with the settings object, and nothing else. |

All three start from the lesson's loader. Keep `config.json` next to the program and run each
command from a fresh shell so a leftover `APP_*` variable does not confuse the result.

### 1. Prove the order

Add a fifth setting, `log_level: str = "info"`, to every layer: a default, a key in the file, an
`APP_LOG_LEVEL` variable, and a `--log-level` flag. Then run eight commands, every combination of
"file sets it or not", "environment sets it or not", "flag sets it or not", and paste a table of
the eight results into a comment. Every row must be explained by "later wins, absent leaves it
alone". Then break the Go version by assigning the flag unconditionally, and the C++ version by
dropping `app.count`, and add the row that changed to the comment. Done means an eight-row table
per language and the two broken rows identified.

### 2. Refuse the password in the file

Make `db_password` in `config.json` a start-up failure with the message
`config.json: db_password must not be in the file; set APP_DB_PASSWORD`, in all three languages,
while still accepting it from the environment. Then make `APP_PORT=abc` a one-line refusal that
names the variable in all three, with no traceback, panic, or `terminate called`. Paste the four
outputs, two per case, into a comment. Done means the file with a password is refused, the bad
port is refused with the variable's name, and a good run still starts.

### 3. Wire it into the server

Take the day 50 CRUD server in each language and remove every literal `8000`, `127.0.0.1` and
`"secret-123"`. The port and host come from the settings object; the API key from day 49 comes
from `APP_API_KEY` in the environment, and the server refuses to start without it. Print the
masked settings as the first log line. Start the server three ways, with the file only, with the
environment overriding the port, and with `--port` overriding both, and paste the three first
log lines and the three `curl -i http://127.0.0.1:<port>/health` status lines. Done means the
server listens where the settings say, in all three languages, and the first log line never
shows the key.

## Say these out loud

### DSA and system design

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Would sorting first make this problem easier?*
   The question, the payoff you want, the class arithmetic with real numbers, and the three checks
   that would make the answer no.

2. *Here are the requirements. Model it.*
   The six steps in order on the gym, ending on where one specific rule lives and why. If you reach
   for a service before step three, start again.

3. *You sorted. Justify the extra n log n.*
   Half a trillion against twenty-one million, the class-change test, and the counter-example where
   sorting makes it twenty times worse for the same answer.

### Languages

*Three questions from today. Answer each in two minutes, standing up, no notes.*

1. Where should a database password come from, and where should it never be?
   Environment or a secrets manager; never the repo's file, never a flag, never a log line, with
   the reason for each never. Then the refusal at start-up, and the masked print.
2. What is your configuration precedence order, and how does each language know a flag was not
   given?
   Defaults, file, environment, flags, later wins, and why that direction. Then `None` in
   Python, `flag.Visit` in Go, `app.count` in C++, and the bug each one prevents.
3. What does reading a missing environment variable do in each language?
   `None` from `os.environ.get`, `""` and `false` from `os.LookupEnv`, `nullptr` from `getenv`,
   and what happens if you forget: a `KeyError`, an empty string that looks set, or a crash.

## Before you move on

- [ ] I said the sort decision out loud before coding on all four problems.
- [ ] I broke Merge Intervals by sorting on the wrong field and can say which key each problem wants.
- [ ] I wrote the sorted Two Sum, read the wrong indices, and can say both reasons the dict is better.
- [ ] I can give the four payoffs and the four times not to sort, unprompted.
- [ ] I can quote the closest-pair arithmetic and the ratio.
- [ ] I ran the gym modelling drill in fifteen minutes, including the missing noun and the aggregate
      boundaries.
- [ ] I can define entity, value object, aggregate root, repository and ubiquitous language in one
      sentence each.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] The three lesson loaders print the same four lines for the four commands, and the refusal comes first.
- [ ] Exercise 1 has an eight-row table per language, and I found the row that breaks without `Visit` or `count`.
- [ ] Exercise 2 refuses a password in the file and a bad `APP_PORT` with one clear line each, in all three.
- [ ] Exercise 3's servers listen where the settings say, and the first log line masks the key.
- [ ] I can say the precedence order and the reason for its direction without pausing.
- [ ] I can say what `getenv` returns for a missing variable in C++ and why the `env` wrapper exists.
