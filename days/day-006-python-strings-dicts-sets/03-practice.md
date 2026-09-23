---
day: 6
track: practice
title: "Practice — Python for DSA II: strings, dictionaries, and sets"
status: written
---

# Day 006 · Practice

**DSA topic:** Python for DSA II: strings, dictionaries, and sets
**System design topic:** HTTPS and TLS, without the maths

---

## Code these, in this order

Four problems that all reduce to "have I seen this before?" or "how many times have I seen
this?". Every one of them has a nested-loop solution that works and times out.

For each problem:

1. Say out loud which structure the question implies — **set** if you care *whether*,
   **Counter** or **dict** if you care *how many*, **defaultdict** if you are grouping.
2. Write it with that structure first. Do not write the nested loop.
3. State the time and space complexity before you run it.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Contains Duplicate | LeetCode 217 (Easy) | The reflex, in its purest form. If this does not produce a `set` within five seconds, drill it until it does. |
| 2 | Valid Anagram | LeetCode 242 (Easy) | Set versus Counter. `set(a) == set(b)` passes some tests and is wrong — find the input that breaks it before you look it up. |
| 3 | Two Sum | LeetCode 1 (Easy) | A dictionary storing value → index. The insight is that you look for what you *need*, not what you *have*. |
| 4 | Group Anagrams | LeetCode 49 (Medium) | `defaultdict(list)` plus a canonical key. The whole problem is choosing what the key should be. |

### On problem 2, do this properly

- Write `return set(a) == set(b)` and submit it. Note which test case fails.
- Work out from that failing case exactly what a set forgot.
- Rewrite with `Counter` and submit again.
- Say the one-sentence rule out loud: **set when you care whether, Counter when you care how
  often.**

### The reflex drill

Answer each of these with a structure name in under three seconds. No code, just the name.

- "Find the first character that appears twice." →
- "Group words that are anagrams of each other." →
- "Does this array contain any repeated value?" →
- "Which number appears most often?" →
- "Is every element unique after removing one?" →
- "Store the positions I have already visited in a grid." →

Then check: the answers are set, defaultdict(list), set, Counter, set or Counter, and a set
of `(row, col)` tuples. If you hesitated on more than one, the reflex is not built yet.

### The measurement drill

Run the complete program from §5 at `N = 20_000`, then at `N = 40_000`.

The two `O(n²)` rows should quadruple. The two `O(n)` rows should double. Confirm it, then
answer out loud: **which single character is the difference between the second row and the
third?**

### The one to try in a browser

Open any HTTPS site and click the padlock, then "certificate details". Find four things:
the subject name, the issuer, the validity dates, and the chain above it. Then answer: how
many links are there between this certificate and something your browser already trusted
before you opened it?

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *How would you check for duplicates in O(n)?*
   Name the structure first, describe the pass, give both complexities, say why membership is
   `O(1)`, give the honest caveat, then give the `O(1)`-space alternative.

2. *What does HTTPS protect you from? What does it not protect you from?*
   Three guarantees, then the metadata list, then the phishing point. Do not stop after the
   first half.

3. *A site has a valid padlock. Is it safe to enter your card details?*
   One sentence on what the certificate actually proves, one on what it does not, and one on
   who checked what before it was issued.

---

## Before you move on

- [ ] "Have I seen this before?" makes me think `set` before I think about loops.
- [ ] I can say why `x in some_set` is `O(1)` and `x in some_list` is `O(n)`, from the
      mechanism.
- [ ] I know why a list cannot be a dictionary key, and what to use instead.
- [ ] I never build a string with `+=` in a loop. I reach for `"".join(pieces)`.
- [ ] I can list four things an observer sees even when the connection is encrypted.
