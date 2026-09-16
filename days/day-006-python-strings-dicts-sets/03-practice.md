---
day: 6
track: practice
title: "Practice — Python for DSA II: strings, dictionaries, and sets"
status: written
---

# Day 006 · Practice

**DSA topic:** Python for DSA II: strings, dictionaries, and sets
**System design topic:** HTTPS and TLS, without the maths

**Theme:** Growable sequences

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

## Build these, in all three languages

Three exercises, easiest first. Every exercise is done three times: once in Python, once in Go, once in C++. For each, say out loud before running: "this line copies" or "this line shares".

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Start with an empty sequence and add the numbers 1 to 30 one at a time. Print a line every time the hidden block changes size. In Python use `sys.getsizeof`, in Go `cap`, in C++ `capacity()`. Then do it again after asking for room for 30 up front where the language lets you, and count the copies. | Can you see amortised growth happen, and do you know which languages let you pre-size? |
| 2 | Make a sequence of five names. Make a second name for it with plain `=`, and a third with whatever the language's real copy is. Add a name through the second, change the first element through the third, then print all three. Predict the output before you run. | Do you know what `=` does in each language, and what a real copy looks like? |
| 3 | Given the sequence `[10, 20, 30, 40, 50]`, remove every value greater than 25 while walking the sequence, the naive way, and print the result. Then do it the right way. In Go, additionally take a sub-slice of the first two, append to it, and print the original. In C++, additionally read index 7 with `[]` and then with `at()`. | Do you know the three classic bugs: mutating while iterating, the shared sub-slice, and the unchecked index? |

**Exercise 1, what you should notice.** All three double for small sizes. Python: 1, 5, 9, 17, 25. Go and C++: 1, 2, 4, 8, 16, 32. Go's `make([]int, 0, 30)` and C++'s `reserve(30)` give zero copies; Python has no equivalent, and that is a fact about Python worth saying out loud.

**Exercise 2, what you should notice.** Python and Go: the second name shares, so the addition shows through the first name; the real copy, `list(a)` or `a[:]` and `slices.Clone(a)`, does not. C++: `=` already is the real copy, so nothing shows through. If your prediction was wrong in any language, that is the day's lesson and it is worth ten minutes.

**Exercise 3, what you should notice.** The naive removal skips an element in Python and C++ and in Go the `append`-based delete inside a `range` loop behaves worse. The right way in all three is to build a new sequence of the ones to keep. The Go sub-slice overwrites the original's third element. The C++ `[]` prints garbage or nothing; `at()` stops with `std::out_of_range`.

## Compare

- **Python** — list: append, insert, pop, slicing, and the cost of each. Capacity hidden, `=` shares, slicing copies, every index checked, and no way to pre-size.
- **Go** — slice: length, capacity, append, and the backing array. Capacity visible, `=` and slicing both share the backing array, `append` may or may not move, every index checked with a panic.
- **C++** — std::vector: push_back, size, capacity, and reallocation. Capacity visible and reservable, `=` copies everything, `[]` checks nothing, and a reference dies when the block moves.

## Say these out loud

### DSA and system design
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



### Languages
Three questions from today. Answer each in two minutes, standing up, no notes.

1. What happens under the hood when you append to a full sequence?
2. In each language, what does `b = a` do to a sequence, and how do you make a real copy?
3. What does reading one past the end do in each language, and which answer is the most dangerous?

## Before you move on

- [ ] "Have I seen this before?" makes me think `set` before I think about loops.
- [ ] I can say why `x in some_set` is `O(1)` and `x in some_list` is `O(n)`, from the
      mechanism.
- [ ] I know why a list cannot be a dictionary key, and what to use instead.
- [ ] I never build a string with `+=` in a loop. I reach for `"".join(pieces)`.
- [ ] I can list four things an observer sees even when the connection is encrypted.
- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered the DSA, system design, and language questions out loud.
