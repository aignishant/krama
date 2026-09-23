---
day: 175
track: practice
title: "Practice — Combinatorics and security"
status: written
---

# Day 175 · Practice

**DSA topic:** The combinatorics you actually need
**System design topic:** Security in a design interview

---

## Code these, in this order

One rule for the whole set: **count a tiny case by hand before you write a formula.** Three items. Four items.
**An exhaustive count of a small case is the only check you have** on an answer too large to verify — and if
your small cases come out 1, 2, 5, 14, you already know what you are looking at.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Unique Paths | LeetCode 62 (Medium) | That a path is a choice of which steps go down. |
| 2 | Pascal's Triangle II | LeetCode 119 (Easy) | One row in O(n) space, by the multiplicative rule. |
| 3 | Unique Binary Search Trees | LeetCode 96 (Medium) | Catalan, arrived at through the split-and-multiply recurrence. |
| 4 | Combinations | LeetCode 77 (Medium) | Generating them, not counting them — and the size of the output. |
| 5 | Count Sorted Vowel Strings | LeetCode 1641 (Medium) | Stars and bars in disguise, or a four-line DP. |
| 6 | Number of Ways to Divide a Long Corridor | LeetCode 2147 (Hard) | The multiplication principle over independent gaps, modulo a prime. |

### On problem 1, do it twice

Solve it with dynamic programming, then with `C(m+n−2, m−1)`. **Check they agree for a 3 by 7 grid.** Then
**add an obstacle in the middle** and say which of the two solutions survives. Say which one you would write in
an interview and why the answer is not always the faster one.

### On problem 2, watch the intermediate values

Print the running value at every step while computing row 100. **Record the largest one.** Compare it with the
largest number in the row. Then rewrite the line as `result // (i+1) * (n-i)` and record what happens.

### On problem 3, find Catalan yourself

Write the recurrence first — **pick the root, split the remaining nodes left and right, multiply.** Compute the
first eight values. **Recognise the sequence.** Only then look up the closed form and check it agrees.

### On problem 4, notice the difference

This asks you to *generate* the combinations, not count them. **Compute `C(20, 10)` first and say how many
lists that is.** Then say why a counting problem and a generating problem have completely different cost
profiles, even with the same formula on the page.

### Then the overflow drill

Compute `20!` and `21!`. **Record which fits in a signed 64-bit integer.** Then write `nCr` the naive way and
say what `C(21, 2)` would produce in Java. Then write the multiplicative version and record its largest
intermediate value for `C(100, 50)`.

### Then the float drill

Write `nCr` with `/` instead of `//`. **Run it on `C(30, 15)`, `C(50, 25)` and `C(100, 50)`.** Record all
three against the exact answers. Say at roughly how many digits it starts lying, and why the small cases are
the dangerous part.

### Then the four-cases drill

Take five items and pick three. **Compute all four cases** — order with and without repeats, no order with and
without repeats. Get four different numbers. **Say the question that separates each pair.**

### Then the over-counting drill

Count the three-letter strings from {A, B} with at least one A, **using the wrong method first** — choose a
position for the A, fill the rest freely. Record the wrong answer. Say which string was counted twice. Then do
it by complement and say why that is nearly always easier.

### Then the modulus drill

Build factorial and inverse-factorial tables to 200,000. **Time the build with one fast power per entry, and
again with the walk-down.** Record both. Then say what breaks if `n` is bigger than the modulus.

### Then the password drill

Compute how long an exhaustive search of all eight-character lowercase passwords takes **at ten billion guesses
a second and at four guesses a second.** Then do it again for ten characters. Say which of length and
complexity wins, and by how much.

### Then the token drill

Say what a stolen access token is worth at three different lifetimes. **Then say how long it takes to lock
somebody out** with a fifteen-minute access token, and with a thirty-day JWT and no denylist.

### Then the authorisation drill

Take any endpoint you can imagine that returns a record by id. **Write the check that is usually missing.** Say
why putting it in the query rather than beside the query matters, and what the database-level version of the
same idea is called.

---

### The four-cases drill

1. Give the two questions that pick the formula.
2. Give all four formulas and one example of each.
3. Derive `nPr` from first principles in one sentence.
4. Derive `nCr` from `nPr` in one sentence.

### The safety drill

1. Say which factorial is the last one that fits in 64 bits.
2. Give the multiplicative form of `nCr` and the order of operations.
3. Say why the division is exact at every step.
4. Say what `min(r, n-r)` saves on `C(1000, 997)`.
5. Say what `/` instead of `//` does, and when you would notice.

### The Pascal drill

1. Give the identity and the sentence it means.
2. Say what the row sums are and why.
3. Give the cost in time and space.
4. Say when Pascal is the right tool and when it is impossible.

### The modulus drill

1. Say why the modulus is a hint about the answer's size.
2. Give the three-lookup formula.
3. Give the walk-down trick and what it saves.
4. Give the preparation cost and the per-query cost.
5. Say what constraint on `n` the method has, and what to name if it is violated.

### The shapes drill

1. Grid paths, and the one-sentence reason.
2. Catalan, its formula, and five things it counts.
3. Stars and bars, with and without the "at least one" variant.
4. Arrangements with repeats, and the division argument.
5. Subsets, and the connection to counting in binary.

### The two-words drill

1. Define authentication and authorisation, and say how often each is checked.
2. Name the most common serious flaw in real systems.
3. Give the fix, and say where it must live.
4. Give the database-level version of the same protection.

### The passwords drill

1. Name three acceptable password hashes and one unacceptable one.
2. Say why fast is the wrong property.
3. Give the two crack times for an eight-character lowercase password.
4. Say what the salt does, separately from the slowness.
5. Say why the work factor is stored inside the hash.
6. Say why the login endpoint needs the strictest rate limit.

### The tokens drill

1. Give the two ways to remember a login and what each costs.
2. Say the one thing a JWT cannot do.
3. Give the two-token shape and both lifetimes.
4. Say what a stolen access token is worth, and why.

### The encryption drill

1. Say what TLS covers and why it applies inside the network too.
2. Say exactly what encryption at rest protects against.
3. Say what it does not protect against, and why.
4. Say what field-level encryption costs you.
5. Describe envelope encryption in four steps and say what rotation then means.

### The attacks drill

1. Name five attacks and the mechanism of the fix for each.
2. Say what a parameterised statement does differently from escaping.
3. Say why an allowlist and not a blocklist.
4. Say why rate limits must be per account and per address.

### The audit drill

1. Give four differences between an audit log and an application log.
2. Give the six fields every entry carries.
3. Say which entries carry the most signal, and why.
4. Say why it lives in a separate store.
5. Compute its volume and seven-year cost from a stated scale.

### The break-it drill

For each, say what happens and whether anything reports it:

1. `factorial(n) // (factorial(r) * factorial(n-r))` in Java at `n = 21`.
2. `nCr` computed with floats, at `n = 100`.
3. Dividing before multiplying in the multiplicative form.
4. Pascal's triangle at `n = 100,000`.
5. Factorial tables under a modulus when `n` exceeds the modulus.
6. Multiplying two choices that are not independent.
7. An endpoint that checks the token but not the object's owner.
8. SHA-256 for passwords, with a salt.
9. A thirty-day JWT after an account is compromised.
10. An audit log the application's own credentials can rewrite.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *How many ways can you arrange these? Now with repetitions.*
   The two questions, all four cases derived rather than recalled, the division argument for over-counting, the
   MISSISSIPPI example, and why you never compute a factorial.

2. *Compute nCr for n up to 200,000, modulo 10^9 + 7.*
   Why division needs an inverse, the two tables, the three-lookup query, the walk-down trick and what it
   saves, and the constraint on `n`.

3. *What are the security concerns in this design?*
   The four layers, the authorisation bug that actually happens with the fix in the query, the password
   arithmetic, token lifetime as blast radius, the five attacks with mechanisms, and the audit log.

---

## Before you move on

- [ ] I ask "does order matter" and "can things repeat" before writing anything.
- [ ] I can derive all four formulas rather than recall them.
- [ ] I can explain `nCr = nPr / r!` in one sentence about over-counting.
- [ ] I know `21!` overflows a 64-bit integer.
- [ ] I never compute a factorial to get `nCr`.
- [ ] I multiply before I divide, and I know why the division is exact.
- [ ] I use `min(r, n-r)` every time.
- [ ] I know what `/` instead of `//` does and when it starts lying.
- [ ] I can state Pascal's identity as a sentence about one item.
- [ ] I know the row sums are `2^n` and why.
- [ ] I know when Pascal's triangle is right and when it is impossible.
- [ ] I can build factorial and inverse tables under a modulus.
- [ ] I know the walk-down trick and what it saves.
- [ ] I know the method needs `n` below the modulus, and what to name otherwise.
- [ ] I can explain grid paths as a choice of steps.
- [ ] I recognise 1, 2, 5, 14, 42 and know five things it counts.
- [ ] I can do stars and bars, both variants.
- [ ] I know over-counting is the usual error, and to count the complement.
- [ ] I check independence before multiplying.
- [ ] I can define authentication and authorisation and say how often each is checked.
- [ ] I know the most common serious flaw and where its fix must live.
- [ ] I know what row-level security buys.
- [ ] I can name three good password hashes and say why fast is wrong.
- [ ] I can give both crack times for an eight-character password.
- [ ] I know what the salt does, separately from the slowness.
- [ ] I know why login needs the strictest rate limit.
- [ ] I can give the trade between sessions and JWTs in one sentence.
- [ ] I know the two-token shape and both lifetimes.
- [ ] I know exactly what encryption at rest does and does not protect.
- [ ] I can describe envelope encryption and what rotation then means.
- [ ] I can name five attacks with the mechanism of each fix.
- [ ] I know why rate limits are per account and per address.
- [ ] I can list four ways an audit log differs from an application log.
- [ ] I know denied attempts carry the most signal.
- [ ] I know the review question is "what was quietly bypassed", not "what is missing".
- [ ] I answered all three questions above out loud.
