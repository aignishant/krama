---
day: 174
track: practice
title: "Practice — Number theory and deployments"
status: written
---

# Day 174 · Practice

**DSA topic:** Primes, GCD, and modular arithmetic
**System design topic:** Deployments: blue-green, canary, and rollback

---

## Code these, in this order

One rule for the whole set: **say the precondition before you write the line.** "This needs the modulus to be
prime." "This needs `a` and `m` to share no factor." **Every wrong answer in this topic is a violated
precondition that nothing checks**, and saying it out loud is the only defence.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Count Primes | LeetCode 204 (Medium) | The sieve, and why you start at `p × p`. |
| 2 | Greatest Common Divisor of Strings | LeetCode 1071 (Easy) | That Euclid is about structure, not just numbers. |
| 3 | Ugly Number II | LeetCode 264 (Medium) | Factors as generators, and the three-pointer merge. |
| 4 | Pow(x, n) | LeetCode 50 (Medium) | Square and multiply, plus the negative-exponent edge case. |
| 5 | Super Pow | LeetCode 372 (Medium) | Fast power with the exponent given as digits. |
| 6 | Fraction to Recurring Decimal | LeetCode 166 (Medium) | Remainders repeating, which is modular arithmetic in disguise. |

### On problem 1, count the crossings

Instrument the sieve so it counts how many numbers each prime actually strikes out, for a limit of 100.
**Record the counts for 2, 3, 5 and 7.** Say why they fall so fast, and connect that to why the total is
`n log log n` rather than `n log n`.

### On problem 1 again, change the start

Change the inner loop to start at `2p` instead of `p × p`. **Count the total crossings both ways at a limit of
one million.** Record both numbers. Say why the answer is identical and the work is not.

### On problem 2, find Euclid where it is hiding

Nothing in this problem mentions numbers. **Work out for yourself why the answer is the string of length
`gcd(len(a), len(b))`**, and say what "divides" means for strings. Then say what property of Euclid you used.

### On problem 4, break it on the edge

Run your fast power on `n = -2147483648`. **Record what happens.** Say why negating that particular value is a
problem in a fixed-width language, and what you would do about it.

### Then the square-root drill

Take 1,000,003. **Say how many divisions the naive test does, how many the square-root test does, and how many
the `6k ± 1` version does.** Then say, in one sentence, why the square root is enough.

### Then the sieve-memory drill

Compute the memory a Python list sieve needs for limits of one million, ten million and a hundred million.
**Then do it again for a bytearray and for a bitset.** Say at which limit each one stops being sensible, and
what you would say if asked for primes below a billion.

### Then the Euclid drill

Compute `gcd(1071, 462)` by hand, writing every remainder. **Count the steps.** Then do `gcd(89, 55)` and count
those. Say why the Fibonacci pair is the worst case.

### Then the overflow drill

Write `lcm` both ways. **In Python they agree.** Say exactly which values would break the multiply-first
version in a 64-bit language, and compute the threshold.

### Then the modulus drill

Compute `(3 - 10) % 7` in Python. **Then say what C, Java and Go give.** Write the three-token fix. Then say
which of `+`, `−`, `×` and `÷` survive a modulus, and what replaces the one that does not.

### Then the Fermat drill

Compute the inverse of 3 modulo 10 using Fermat's formula. **Check it by multiplying.** Record that it is
wrong, say why, and give the true inverse. Then say which two preconditions Fermat needs and which one
`10^9 + 7` satisfies.

### Then the deployment drill

Take any service you can imagine and describe out loud how a change reaches production. **Name the strategy,
the abort rule, and the rollback time.** Then say what would have to be true for the rollback to be unsafe.

### Then the migration drill

Say the five steps of expand and contract from memory, and **for each one, say what would break if you skipped
it.** Then size the backfill for five hundred million rows in ten-thousand-row batches.

### Then the canary arithmetic drill

At 100 million requests a day and a 1 percent canary, **compute how long you must wait to see a hundred errors
at a 0.5 percent error rate.** Then at 0.05 percent. Then say what that tells you about ten-minute canaries.

---

### The primality drill

1. Say what a prime is, and the two numbers people get wrong.
2. Say why testing to the square root is enough.
3. Give the `6k ± 1` optimisation and why it works.
4. Give the cost, and the size of number at which you would name Miller–Rabin.

### The sieve drill

1. Describe the sieve in three sentences.
2. Say why crossing off starts at `p × p`.
3. Say why sieving stops at the square root of the limit.
4. Give the cost and where `log log n` comes from.
5. Give the memory for three limits and three representations.
6. Say what a segmented sieve is for.

### The factorising drill

1. Say what an spf table stores.
2. Give the factorising loop and its step count.
3. Say why each step at least halves the number.
4. Say after how many queries the table has paid for itself.

### The Euclid drill

1. State the identity.
2. Give the one-sentence reason it preserves the answer.
3. Give the rectangle picture.
4. Give the cost and the worst case.
5. Give the LCM relation and the overflow-safe form.
6. Say what `gcd(a, 0)` is and why that is not a special case.

### The modular drill

1. Say which three operations pass through a modulus and which does not.
2. Give the replacement for the one that does not.
3. Give Fermat's formula and its two preconditions.
4. Say what happens when the modulus is composite.
5. Give the alternative that does not need a prime.
6. Give the three reasons for `10^9 + 7`.
7. Give the negative-modulo fix and the languages that need it.

### The fast-power drill

1. Give the idea in one sentence, using the binary expansion.
2. Trace `3^13` through the four steps.
3. Give the step count for exponents of `10^9` and `10^18`.
4. Say what goes wrong without the modulus inside the loop, and why that is hard to debug.

### The strategies drill

1. Name five deployment strategies.
2. For each: what it costs and what it buys.
3. Say what is true during every one of them.
4. Say which one is the only way to find load-dependent bugs.

### The probes drill

1. Define liveness and readiness, and what failing each one does.
2. Say what goes wrong with only a liveness check.
3. Say what goes wrong when liveness is wired to a slow condition.
4. Say why readiness should not depend hard on a shared dependency.
5. Give the connection-draining sequence and the cost of skipping it.

### The rollback drill

1. Give the target time and why the number shapes team behaviour.
2. Say the order: roll back or investigate, and why.
3. Give the rollback time for each of three strategies.
4. Name five things that cannot be rolled back.
5. Say what to do about them instead.

### The migration drill

1. Give the five steps of expand and contract.
2. Say what breaks if you rename in one step.
3. Say why the backfill is batched.
4. Say why the gap before dropping is deliberately long.
5. Give the rule that generates the whole pattern.

### The break-it drill

For each, say what happens and whether anything reports it:

1. `is_prime` without the `n < 2` check.
2. A sieve built for a limit of `10^11`.
3. `lcm = a * b // gcd(a, b)` in Java, with `a` and `b` around `3 × 10^9`.
4. `(a - b) % m` in C, when `b > a`.
5. Fermat's inverse with a composite modulus.
6. Fast power with the `% m` missing inside the loop.
7. A rolling update with no readiness check.
8. A rolling update with no connection draining.
9. Renaming a column and deploying the new code straight afterwards.
10. A ten-minute canary at one percent, against a 0.05 percent regression.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find all primes below one million.*
   The sieve, why it starts at `p × p` and stops at the square root, the `n log log n` cost with the
   reciprocal-sum reason, the hundredfold comparison against testing each number, and memory as the real
   limit.

2. *The answer may be large, so return it modulo 10^9 + 7. What does that change?*
   Which operations survive, why division does not, Fermat with its preconditions, what happens on a composite
   modulus, extended Euclid as the general answer, and the three reasons for that particular number.

3. *How do you deploy a change to a service handling live traffic?*
   Two versions at once against one database, the five strategies with what each costs, the rollback-time
   number, roll back before investigating, and expand-and-contract for the schema.

---

## Before you move on

- [ ] I know 1 is not prime and 2 is, and I write the base cases first.
- [ ] I can say why testing to the square root is enough.
- [ ] I know the `6k ± 1` optimisation and why it works.
- [ ] I can write the sieve from memory.
- [ ] I can say why it starts at `p × p` and stops at the square root.
- [ ] I know the cost is `n log log n` and where that comes from.
- [ ] I know memory limits the sieve before time does.
- [ ] I know what a segmented sieve is for.
- [ ] I can factorise with an spf table and give the step count.
- [ ] I can state Euclid's identity and the one-sentence reason it holds.
- [ ] I can give the rectangle picture for a GCD.
- [ ] I know the cost and the Fibonacci worst case.
- [ ] I write `lcm` dividing first, and I can say which values break the other form.
- [ ] I know which three operations pass through a modulus and which does not.
- [ ] I can compute a modular inverse with Fermat and state both preconditions.
- [ ] I know what Fermat does on a composite modulus, and that it does not complain.
- [ ] I know extended Euclid is the general answer.
- [ ] I can give the three reasons for `10^9 + 7`.
- [ ] I know the negative-modulo fix and which languages need it.
- [ ] I can write fast power and give the step count for `10^9`.
- [ ] I know what happens without the modulus inside the loop.
- [ ] I can name five deployment strategies with their costs.
- [ ] I know two versions always run at once, against one database.
- [ ] I can define liveness and readiness and say what failing each one does.
- [ ] I know the two probe misconfigurations and what each looks like.
- [ ] I can give the connection-draining sequence and price skipping it.
- [ ] I know my rollback target and why that number shapes behaviour.
- [ ] I roll back before investigating, and I can say why.
- [ ] I can give the five steps of expand and contract from memory.
- [ ] I know why the backfill is batched and the gap before dropping is long.
- [ ] I can do the canary arithmetic for 0.5 percent and 0.05 percent.
- [ ] I can name five things no rollback can undo.
- [ ] I answered all three questions above out loud.
