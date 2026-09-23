---
day: 67
track: practice
title: "Practice — Hashing revision and mock round"
status: written
---

# Day 067 · Practice

**DSA topic:** Hashing revision and mock round
**System design topic:** Prototype, and cloning objects

---

## Code these, in this order

This is a mock day, so the rule is different from every other practice sheet: **set a timer, do not
look anything up, and talk out loud the entire time.** A problem solved in silence today is a problem
you have not practised, because silence is the thing that fails in the room.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Top K Frequent Words | LeetCode 692 (Medium) | Counting plus a two-direction tie-break — the `reverse=True` trap in a hashing costume. |
| 2 | Subarray Sum Equals K | LeetCode 560 (Medium) | Prefix sums plus a frequency map: the composition that carries two phases at once. |
| 3 | Longest Substring Without Repeating Characters | LeetCode 3 (Medium) | Sliding window plus a map from value to index — and the index-jump most people get wrong. |
| 4 | Insert Delete GetRandom O(1) | LeetCode 380 (Medium) | Designing with two structures, and deletion done in O(1) with the swap-with-last trick. |

### On all four: run the forty seconds first

Before writing anything, say out loud, in this order: the repeated question, the structure, the key,
the invariant, the complexity. Time yourself. If it takes more than a minute, do it again tomorrow
until it does not.

### On problem 1, find the trap before it finds you

The counts go descending and the words go ascending. Write `sorted(..., reverse=True)` first, watch
it get the alphabetical order backwards, then fix it with a composite key and say out loud why
negating the count works and negating the word does not.

### On problem 2, say which structure holds what

There are two ideas here: a running prefix sum, and a map from *prefix value* to *how many times it
has occurred*. Say the invariant out loud before coding: *the map holds the counts of every prefix
sum seen before the current index.* Then say why the map must be seeded with `{0: 1}`, and give the
input that fails without it.

### On problem 4, notice why a dict alone is not enough

`getRandom` needs uniform choice, which a dict cannot give in O(1). So it is a list plus a map from
value to its index in the list. Say what has to be updated when you swap-with-last, and why
forgetting it is the same class of bug as mutating a key in place.

### The forty-second drill

For each problem statement, run the five questions out loud and stop. Do not code any of them.

1. "Find the two numbers that add to the target."
2. "Return the length of the longest run of consecutive integers."
3. "Group these files by identical contents."
4. "Return the third-most-common word."
5. "Find the first character that appears exactly once."
6. "Which user ids appear in both of these two-million-line files?"
7. "Return all orders placed between two timestamps."
8. "The values are between 1 and n. Which one is missing?"

Two of the eight should end with "not a map". Name them and say what you would use.

### The mock drill

Do this three times this week, with a timer, out loud, and ideally with somebody in the room.

1. Pick an unseen medium problem you have not read.
2. Minutes 0-3: read twice, restate, ask two clarifying questions out loud.
3. Minutes 3-6: state the brute force and its cost with a real number. Do not write it.
4. Minutes 6-10: structure, key, invariant, complexity.
5. Minutes 10-25: write it, narrating every few lines.
6. Minutes 25-30: test it yourself on empty, one element, all-identical, and a negative or edge value.
7. Minutes 30-40: have somebody ask "now O(1) space" and "now it does not fit in memory".

Afterwards, score yourself out of five on communication, approach, correctness, edge cases and
follow-ups. The one you score lowest on is what to practise, and it is almost never correctness.

### The trap-recall drill

Without looking at the lesson, write down the exact error text or the wrong answer for each:

1. `seen = []` instead of `seen = set()`
2. `counts[key] += 1` on a missing key
3. `.add` on `{}`
4. Reading a missing key from a `defaultdict`
5. `{1, 2}.add([3])`
6. `itertools.groupby` on unsorted input
7. `@dataclass` without `frozen=True`, put in a set
8. Mutating a key while it is in a dictionary
9. `-x` instead of `-abs(x)` in the marking trick, on `[1, 1]`
10. Adding to a set while iterating it

Three of the ten produce **no error at all**. Name them, and say what each one silently returns.

### The five-sentences drill

Say each of these out loud from memory, then check it:

1. What a hash map does instead of searching.
2. What `O(1)` actually rests on, and what the worst case is.
3. Why `in` on a list and `in` on a set look identical and are not.
4. What the two tests on a grouping key are.
5. What a map buys and what it throws away.

### The shallow-versus-deep drill

Reproduce each, predict the output first, then run it:

1. `b = a` on a list, then `b.append(1)`. Print `a`.
2. `copy.copy` on a dict of lists, mutate a list, print the original.
3. `copy.deepcopy` on the same, mutate, print the original.
4. `a[:]` on a list of lists, mutate an inner list, print the original.
5. A `@dataclass(frozen=True)` with a `list` field. Shallow copy it, mutate the list. What happens,
   and why does `frozen=True` not save you?
6. Two objects, each holding the other. `copy.deepcopy` one of them. Does it terminate? Why?
7. An object with two fields pointing at the *same* list. Deep copy it. How many lists exist now?

Number 5 and number 7 are the two that surprise people. Say precisely what `frozen` guarantees, and
what the memo dictionary preserves.

### The resource drill

1. Build an object holding a `threading.Lock`. Try to `deepcopy` it. Quote the exact error.
2. Do the same with an open file handle.
3. Write a `__deepcopy__` that copies the data and leaves the resource out.
4. Say what would go wrong if the deep copy had silently succeeded instead of raising.
5. Name three more things that must never be deep-copied.

### The cost drill

On a dict of 1,000 keys each holding a list of 100 integers:

1. Time `b = a`.
2. Time `copy.copy(a)`.
3. Time `copy.deepcopy(a)`.
4. Compute the two ratios.
5. Measure the memory added by each.
6. Now answer: at 200 requests a second, what does a `deepcopy` per request cost you in CPU seconds
   per second? Is that possible?

### The prototype-or-not drill

For each, say whether you would clone or construct, and give the arithmetic:

1. A `Point(x, y)`.
2. A `Report` whose construction reads a database, parses a template and makes an HTTP call.
3. A configuration object with forty fields, of which a caller changes two.
4. An object holding an open database connection.
5. A subclass whose concrete type the caller does not know.
6. A test fixture used in sixty tests.

Two of the six are "construct" for the same reason. Name it.

### The Cloneable drill

Answer each in one sentence:

1. Why does implementing `Cloneable` not give you a `clone()` method?
2. Why is `Object.clone()` being protected a problem?
3. What does `Object.clone()` do about `final` fields, and why?
4. What exception does it declare, and why is that a design flaw?
5. What is the recommended replacement, and why is it better?

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Two problems, no hints, talk as you go.*
   Run the whole script: restate, two clarifying questions, the brute force refused with a number,
   the structure and key and invariant and complexity named before any code, narration while writing,
   and four edge cases you test yourself.

2. *What is the difference between a shallow copy and a deep copy?*
   Both in terms of pointers, the boxes-and-arrows drawing, the three-line reproduction, the real
   rule about immutability, and the three failures of deep copy volunteered before being asked.

3. *When would you not use a hash map?*
   The three cases with an example each, the two triggers that come first in the decision procedure,
   and the sentence about O(1) being an average rather than a bound.

---

## Before you move on

- [ ] I ran a full timed mock, out loud, from restatement to follow-up.
- [ ] I scored myself on all five rubric lines and know which one is my weakest.
- [ ] I can run the five decision questions in under a minute on an unseen problem.
- [ ] I can recite the five sentences that carry the phase, from memory.
- [ ] I wrote down the exact error text for at least seven of the ten traps.
- [ ] I can name the three traps that produce no error at all, and what each returns instead.
- [ ] I reproduced the shallow-copy bug and drew the boxes and arrows for it.
- [ ] I triggered a deep-copy failure on a lock and quoted the exact error.
- [ ] I measured the deepcopy ratio myself and can quote it.
- [ ] I can say when Prototype does *not* pay, with the arithmetic.
- [ ] I answered all three questions above out loud.
