---
day: 57
track: practice
title: "Practice — Stability, and what Python's sort actually does"
status: written
---

# Day 057 · Practice

**DSA topic:** Stability, and what Python's sort actually does
**System design topic:** Liskov substitution

**Theme:** Authentication: hashing and tokens

---

## Code these, in this order

One rule for the whole set: **every time you sort by more than one thing, say out loud whether you
are using a tuple key or two passes, and if it is two passes, say which one goes first.**

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Relative Sort Array | LeetCode 1122 (Easy) | A custom order with a stable tie-break — the cleanest use of a tuple key. |
| 2 | Sort the People | LeetCode 2418 (Easy) | Sorting one list by another list's values, and keeping the pairing intact. |
| 3 | Custom Sort String | LeetCode 791 (Medium) | An ordering that is data rather than comparison, and where ties come from. |
| 4 | Sort Characters By Frequency | LeetCode 451 (Medium) | Two keys in opposite directions, which is where tuple keys start to run out. |

### On problem 1, find the tie

The problem says elements not in the reference order go at the end **in ascending order**. That is
the tie-break, and writing it as the second element of a tuple key is the whole solution. Say out
loud what happens if you leave it out.

### On problem 2, do not lose the pairing

The obvious wrong move is to sort the heights and then try to line the names back up. Say why that
fails, then solve it by sorting pairs. This is the same lesson as
[day 051](../day-051-why-sorting-matters/README.md)'s tag.

### On problem 3, notice there is no comparison

The order is given to you as a string, so the "key" is a position lookup. Build the lookup first,
then sort by it. Then answer: what should happen to characters not in the order string, and does your
solution make that decision on purpose?

### On problem 4, hit the wall deliberately

Sort by frequency descending, then by character ascending. Try to do it with one tuple key. You can,
because frequency is a number and can be negated — so do it. Then change the requirement to "by name
descending, then by frequency ascending" and try again. `-name` raises. Paste the `TypeError`, then
solve it with two passes and say which pass goes first.

### The stability-test drill

Write the four-line `is_stable` checker, then run it against everything you have written this phase:

1. Your `merge_sort` from [day 053](../day-053-merge-sort/README.md).
2. Your `insertion_sort` from [day 052](../day-052-quadratic-sorts/README.md).
3. Your `selection_sort`.
4. Your `quicksort` from [day 054](../day-054-quicksort/README.md).
5. Your `counting_sort` from [day 056](../day-056-non-comparison-sorts/README.md).
6. Python's `sorted`.

Predict each result before you run it. Then, for each `True`, find the single character that is
responsible.

### The two-pass drill

Given people with a name, a department and an age:

1. Sort by department, then name ascending. Tuple key.
2. The same, two passes. Which pass first?
3. Sort by department ascending, age descending. Tuple key — what makes it possible?
4. Sort by department ascending, name descending. Try the tuple key, paste the error, then do it in
   two passes.
5. Sort by age descending, and within equal ages keep the original input order. Which of
   `reverse=True` and `reversed(sorted(...))` is correct, and why is the other one wrong?
6. Sort by three keys: city ascending, department descending, age ascending. Say how many passes and
   in what order.

### The reverse drill

Run both and record the difference:

```python
ages = [("Asha", 34), ("Bala", 12), ("Chitra", 34)]
sorted(ages, key=lambda p: p[1], reverse=True)
list(reversed(sorted(ages, key=lambda p: p[1])))
```

1. What differs, and on which elements?
2. Which one would you want for a leaderboard where equal scores show earliest-achieved first?
3. What does `max(ages, key=lambda p: p[1])` return, and why is that consistent with stability?
4. What does `min` return on the same data?

### The Timsort drill

Time each on two million integers, and predict the ordering of the results first:

1. Already sorted.
2. Reverse sorted.
3. Random.
4. Sorted, with the last 1,000 elements shuffled.
5. All identical values.
6. Two sorted halves concatenated.

Then explain each result using runs, minrun and galloping. Number 6 is the one to think hardest
about.

### The other-languages drill

Say, for each, whether the sort is stable, and what you would do if you needed stability and did not
have it:

1. Python `sorted`.
2. C++ `std::sort`.
3. Java `Arrays.sort(String[])`.
4. Java `Arrays.sort(int[])`.
5. Go `sort.Slice`.
6. JavaScript `Array.prototype.sort` in a modern browser.

Then write the decorate-sort-undecorate function that gives you stability from any sort, and say what
it costs in time and memory at a million elements.

### The Liskov drill

For each, say whether it is a violation. If it is, name which of the three rules it breaks
(demands more / delivers less / breaks an invariant), and give the fix.

1. `Square(Rectangle)` with setters.
2. `Square(Rectangle)` where both are immutable.
3. `ReadOnlyList(list)` whose `append` raises.
4. `Penguin(Bird)` whose `fly()` raises.
5. `FixedDeposit(Account)` whose `withdraw` raises before maturity.
6. `CachedRepository(Repository)` whose `get` raises `CacheMissError` instead of returning `None`.
7. `NullLogger(Logger)` whose `log(msg)` does nothing at all.
8. A subclass whose `handle(event: LoginEvent)` narrows the parent's `handle(event: Event)`.

Two of those eight are fine. Name them and defend them.

### The square-rectangle drill

1. Write `Rectangle` with setters and `Square` inheriting from it.
2. Write `resize_and_check` and run it on a `Rectangle` and on a `Square`. Paste both results.
3. State, in one sentence, the promise `Rectangle` makes that nobody wrote down.
4. Make both immutable and re-run. What happened to the problem?
5. Rewrite them as two implementations of a `Shape` protocol.
6. Now answer the interview question out loud in under ninety seconds.

### The contract-test drill

Take an interface you can write in five lines — a key-value repository will do:

1. Write the contract test suite: at least five tests, written against the interface only.
2. Include one test for a missing key, one for overwriting, and one for deleting something that does
   not exist.
3. Write two implementations: an in-memory dict and one backed by a file or a list of tuples.
4. Wire both into the contract suite and run it.
5. Deliberately make one implementation raise on a missing key. Which test fails, and what does the
   failure tell you?
6. Say how this same file solves the "is my test fake honest?" problem from
   [day 053](../day-053-merge-sort/README.md).

### The isinstance-audit drill

For each place an `isinstance` check appears, say whether it is legitimate or a symptom:

1. Parsing a JSON payload that could be a dict or a list.
2. In a `Checkout` class, checking whether the discount policy is a `PercentageOff`.
3. Narrowing an `Any` returned by a third-party library.
4. In a loop over `Account` objects, checking for `FixedDeposit` before withdrawing.
5. In a `__eq__` method, checking that the other operand is the same class.
6. In a template renderer, checking whether a value is a `str` or a `Sequence`.

Three are legitimate. For the others, say what the real fix is.

---

## Build these, in all three languages

*Three exercises, easiest first. Each one says what it is really testing. Every
exercise is done three times: once in Python, once in Go, once in C++.*

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Salt and slowness, shown | Proving the hash is salted and slow, not a fast digest, with your own eyes. |
| 2 | Break the tokens | Making a tampered, expired, wrong-secret, and `alg: none` token all fail. |
| 3 | A login endpoint | Wiring register, login, and a protected route into the day 49 server. |

All three start from the lesson's program. Keep `JWT_SECRET` set to a long random value in the
environment for every run.

### 1. Salt and slowness, shown

Hash the same password twice and print both hashes: they must differ, because the salt differs.
Then time a hundred hashes and a hundred verifies and print the average: it must be milliseconds,
not microseconds, and you should be able to say why milliseconds is the point. For contrast, time
a hundred SHA-256 hashes of the same password and print how many you could do in a second, then
write one sentence on why that number is exactly the problem. Done means two different hashes of
one password, a per-hash time in milliseconds, and the SHA-256 rate with your sentence, in all
three languages.

### 2. Break the tokens

Issue a valid token and verify it. Then produce four bad tokens and show each is rejected: one
with a character changed in the signature, one with an `exp` already in the past, one signed with
a different secret, and one forged with `alg: none` and no signature. Paste the rejection for
each. The `alg: none` case is the important one: show that your verifier refuses it because it
pins the algorithm, and then, carefully and only in a throwaway file, show that a verifier without
the pin would accept it. Done means five outcomes, one valid and four rejected, and the `alg:
none` refusal explained, in all three languages.

### 3. A login endpoint

Add three routes to the day 49 server: `POST /register` takes a username and password and stores
the hash; `POST /login` checks the password and returns a token, or 401; and `GET /me` reads the
`Authorization: Bearer <token>` header, verifies it, and returns the subject, or 401. Register,
log in, call `/me` with the token, then call `/me` with a tampered token and with no header, and
paste the four status lines. Confirm, from the day 52 logs, that neither the password nor the
token appears in any log line. Done means register-login-me works, the two bad `/me` calls are
401, and the logs are clean, in all three languages.

## Say these out loud

### DSA and system design

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Is Python's sort stable? Why do you care?*
   The definition, the two-pass multi-key argument with the pass order, the tuple-key alternative,
   the `reverse=True` subtlety, and three facts about Timsort.

2. *Is a Square a Rectangle? Defend your answer in code.*
   The shape-versus-class split, the six-line failure, the unwritten promise, the capability fix, and
   the second-order cost — that a Liskov violation destroys open/closed.

3. *Which sorting algorithms are stable, and why?*
   The rule about neighbour swaps against long-distance swaps, the one character in each stable sort
   that makes it so, and the three-element selection-sort counter-example.

### Languages

*Three questions from today. Answer each in two minutes, standing up, no notes.*

1. How do you store a password?
   Not "hashed": slow, salted, with bcrypt or argon2; never a fast hash, never encryption. The
   salt and the work factor and what each defeats, and the constant-time compare the library does.
2. What is in a JWT, and what stops it being forged or misused?
   Signed JSON claims, a subject and an expiry, a server-only secret, HS256. Tampering breaks the
   seal, expiry bounds it, and pinning the algorithm on verify defeats `alg: none`. Signed, not
   encrypted, so no secrets in it.
3. What is the `alg: none` attack, and how does each language stop it?
   The forged unsigned token, and the allow-list that refuses it: `algorithms=` in Python, the
   key function asserting the method in Go, `allow_algorithm` in C++. Say what happens if you omit it.

## Before you move on

- [ ] I ran `is_stable` against all six sorts and predicted every result correctly.
- [ ] For each stable sort I wrote, I can point at the single character responsible.
- [ ] I hit the `TypeError` from negating a string key and solved it with two passes.
- [ ] I can say which pass goes first and why that is backwards from how it sounds in English.
- [ ] I can give three facts about Timsort and quote the sorted-versus-random timing.
- [ ] I ran the square-rectangle failure and can state the unwritten promise in one sentence.
- [ ] I wrote a contract test suite and watched it catch a deliberate substitution violation.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] The three lesson programs store a salted hash, verify right and wrong passwords, and reject tampered, expired, wrong-secret, and `alg: none` tokens.
- [ ] Exercise 1 shows two different hashes of one password, a millisecond-scale hash time, and the SHA-256 rate with my sentence, in all three.
- [ ] Exercise 2 rejects all four bad tokens, and I can explain the `alg: none` refusal, in all three.
- [ ] Exercise 3's register-login-me flow works, bad `/me` calls are 401, and no password or token is in the logs, in all three.
- [ ] I can say the password answer in one sentence with "slow", "salted", and "never encryption" in it.
- [ ] I can name the algorithm allow-list in each language and say what omitting it opens.
