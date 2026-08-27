---
day: 23
track: practice
title: "Practice — Palindromes and the two-ends habit"
status: written
---

# Day 023 · Practice

**DSA topic:** Palindromes and the two-ends habit
**System design topic:** Rate limiting and API gateways

---

## Code these, in this order

Four problems built on two indices walking towards each other. The algorithm is never the hard part;
the input rules and the boundaries are.

Before each one, ask:

1. Which characters count, and does case matter?
2. Is the loop `left < right` or `left <= right`, and why?
3. What are the three inputs that break skip loops? (Empty, one space, pure punctuation.)
4. Am I allowed extra space, or is `O(1)` the point of the question?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Valid Palindrome | LeetCode 125 (Easy) | The messy input rules, and whether you can do it in `O(1)` space rather than reversing. `"0P"` is the trap input. |
| 2 | Valid Palindrome II | LeetCode 680 (Easy) | That only two deletions are possible at the first mismatch, and that you must try **both** rather than guess. |
| 3 | Longest Palindromic Substring | LeetCode 5 (Medium) | `2n - 1` centres, not `n`. Forgetting the even-length centres is the standard bug, and `"cbbd"` finds it. |
| 4 | Palindrome Linked List | LeetCode 234 (Easy) | The same idea where you cannot index backwards. Reverse the second half in place, compare, restore. Two pointers again, in a shape you will meet properly on [day 082](../day-082-runner-technique/README.md). |

### On problem 1, write both versions

Write `cleaned == cleaned[::-1]` first. Say its cost out loud: `O(n)` time, `O(n)` space. Then write
the two-pointer version and say why it is better, in one sentence.

Then run **both** on this list and check they agree:

```python
["A man, a plan, a canal: Panama", "race a car", "", " ", ".,", "0P",
 "aba", "abba", "ab", "a"]
```

Expected: `[True, False, True, True, True, False, True, True, False, True]`

If your two-pointer version crashes on `".,"`, you have found the missing `left < right` guard. Read
the traceback before you fix it.

### On problem 1, break it deliberately

Run each of these and say what is wrong:

```python
# A
cleaned = "".join(ch.lower() for ch in s if ch.isalpha())
```

```python
# B
while left < right:
    if not s[left].isalnum():
        left += 1
    if not s[right].isalnum():
        right -= 1
    ...
```

```python
# C
while left < right:
    while not s[left].isalnum():
        left += 1
    ...
```

A fails on `"0P"`. B fails on `"a,,,  ,a"`. C raises on `".,"`. Reproduce all three and name the rule
each one broke.

### On problem 2, prove the two-branch claim

Before coding, answer this out loud: at the first mismatch between `s[left]` and `s[right]`, why must
the character to delete be one of exactly those two? Why can it not be something in the middle?

The answer is one sentence about what has already been checked. If you cannot produce it, the code
will feel like a guess.

Then write the greedy version — the one that peeks at `s[left+1]` and commits — and find an input
where it is wrong. Try `"eeccccbebaeeabebccceees"`.

### On problem 3, count the centres

Take `"abcd"` and list every centre you would try. There should be seven: four characters and three
gaps. Then take `"cbbd"` and confirm your solution returns `"bb"` and not `"c"`.

Then answer:

1. Why does `expand` return `left + 1, right - 1` rather than `left, right`?
2. What is the cost, counted out loud from the two loops?
3. At what input size does `O(n²)` stop being acceptable?
4. What is the `O(n)` algorithm called, and what would you say about it in an interview?

Question 4 has a specific right answer, and it is not "I'd implement it".

### The boundary drill

Answer without running anything:

1. In `while left < right`, what happens on a string of length 1? Length 0?
2. Why is `<=` not wrong, merely wasteful?
3. In the skip loops, why is the `left < right` test needed **inside each one** and not only in the
   outer loop?
4. `is_palindrome("")` — what should it return, and what does your code return?
5. Trace `is_palindrome(" ")` step by step. Which loop runs, and how many times?

### The cost-argument drill

There are two nested `while` loops inside a `while` loop, and the answer is still `O(n)`. Say the
argument out loud, in one sentence, without using the word "amortised".

Then do the same for these:

1. The two-pointer palindrome check.
2. `valid_palindrome` with one deletion. (Why does the branch not make it `O(n²)`?)
3. `longest_palindrome` by expanding around centres. (Why *is* this one `O(n²)`?)

### The rate-limiter drill

Answer each in one or two sentences, out loud:

1. Describe the token bucket in three sentences, naming capacity and refill rate.
2. What is the fixed-window boundary problem? Give the two timestamps.
3. Why does the token bucket use two numbers per caller while a sliding window log uses one entry per
   request?
4. Where does the limiter run, and what are the two reasons for that placement?
5. Ten gateway servers share one limit. Where does the state live, and what must be atomic?
6. Redis is down. Do you allow or refuse? Defend it.
7. What do you return, and which header stops you creating a thundering herd?
8. What do you key on before the user has logged in, and what is wrong with that key?
9. Does any of this protect you from a DDoS?

Number 5 is the one interviewers push on. Have the word *atomic* ready.

### The design drill

Set limits for these five endpoints and justify each in one sentence:

| Endpoint | Your limit | Why |
|---|---|---|
| `GET /products` | | |
| `POST /login` | | |
| `POST /password-reset` | | |
| `POST /orders` | | |
| `GET /search?q=` | | |

Then derive one of them properly: if a screen fires 8 requests when it opens and a user opens 4
screens a minute, what capacity and refill rate would you choose, and why is that better than picking
a round number?

### The arithmetic drill

From memory, in under two minutes:

- Limit 100/minute, fixed windows — the worst-case burst, and when it happens.
- 1 million active callers — memory for a token bucket, and for a sliding window log at 1,000
  requests a minute each.
- 100,000 requests a second with one Redis operation each — Redis load and latency added.
- The same with local counters synced every second across 10 nodes — Redis load, and the accuracy
  cost.
- Cost of a `429` at the gateway versus serving the request.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Is this string a palindrome, ignoring punctuation and case?*
   Pin the rules first. Give the one-liner and its space cost, then offer two pointers unprompted.
   Name the three loops, the `while`-not-`if` point, and the inner bound check. Finish with the
   `O(n)`-not-`O(n²)` argument and your four test inputs.

2. *How would you stop one client from hammering your API?*
   Token bucket, described concretely. Then the fixed-window flaw with the two timestamps. Then
   placement and why. Then the shared-state and atomicity point. Then the response and its headers.
   Ninety seconds.

3. *Can this string become a palindrome by deleting at most one character?*
   The point is the argument, not the code: at the first mismatch, everything outside has already
   matched, so the deletion must be at one of those two positions — and you must try both rather than
   guess. Then say why it is still `O(n)`.

---

## Before you move on

- [ ] I reach for two indices from the ends without thinking about it.
- [ ] I write `while left < right` and can say why `<=` is unnecessary.
- [ ] My skip loops are `while`, not `if`, and each repeats the bound check.
- [ ] I test with `""`, `" "`, `".,"` and `"0P"` every time.
- [ ] I can argue `O(n)` for nested loops by counting how far the indices travel.
- [ ] I remember there are `2n - 1` centres, not `n`.
- [ ] I can describe the token bucket in three sentences with both of its numbers.
- [ ] I can state the fixed-window boundary problem with real timestamps.
- [ ] I say "the check-and-decrement must be atomic" without being prompted.
- [ ] I can redraw the token-bucket and gateway diagrams from memory, in whatever tool I like.
