---
day: 63
track: practice
title: "Practice — Counting with dictionaries"
status: written
---

# Day 063 · Practice

**DSA topic:** Counting with dictionaries
**System design topic:** What a design pattern actually is

---

## Code these, in this order

One rule for the whole set: **write the counting loop by hand at least once today, without
`Counter`.** Interviewers ask for it, and the three-line `.get(k, 0) + 1` version should come out of
your fingers without thought.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Valid Anagram | LeetCode 242 (Easy) | Counting versus sorting, and whether you can say which wins on time and which on space. |
| 2 | First Unique Character in a String | LeetCode 387 (Easy) | Two passes, and whether you walk the original or the counter on the second one. |
| 3 | Sort Characters By Frequency | LeetCode 451 (Medium) | Counts as sort keys, and the tie-break question nobody asks. |
| 4 | Top K Frequent Elements | LeetCode 347 (Medium) | Whether you know all three selection strategies and can pick one with a reason. |

### On problem 1, give both answers

Write the `Counter` version, then say the sorting version out loud with its complexity. Then answer
the follow-up you will actually get: *what if the strings contain Unicode?* A fixed 26-slot array
stops working; the dictionary does not. That is the real reason to prefer the map.

### On problem 3, find the ambiguity before you code

`"tree"` can correctly return `"eert"` or `"eetr"`. Say out loud which one your code gives and why
both are accepted. Then say what you would ask the interviewer if the problem had not told you.

### On problem 4, write it twice

Once with `heapq.nlargest`, once with buckets. Time both on a million elements with a hundred
thousand distinct values and `k = 10`. Then answer: which one would you write if `n` were a billion
and there were twelve distinct values, and why.

### The four-spellings drill

Count the characters of `"mississippi"` five times, each a different way, and say when you would use
each:

1. An explicit `if key in counts: ... else: ...`
2. `counts.get(key, 0) + 1`
3. `defaultdict(int)`
4. `Counter(text)`
5. `try: counts[key] += 1 / except KeyError:`

Then say which of the five you would write in an interview and which one would count against you.

### The missing-key drill

Trigger each of these, read the exact output, and give the fix:

1. `counts = {}; counts["a"] += 1`
2. `counts = {}; print(counts["a"])`
3. A `defaultdict(int)`, then `print(d["zzz"])`, then `print(len(d))` — explain the number.
4. A `Counter`, then `print(c["typo"])` — explain why nothing raises and why that is dangerous.
5. `for k in d: d[k + "!"] = 1`
6. `sum(Counter(w) for w in ["ab", "bc"])`

Two of those six produce a wrong answer with no error at all. Name them, and say what would have
caught each one.

### The complexity drill

For each snippet, count the operations at `n = 20,000` and name the complexity:

1. `Counter(items)`
2. `for x in items: if items.count(x) == 1: return x`
3. `for x in items: if x in seen_list: ... ; seen_list.append(x)`
4. `sorted(counts.items(), key=lambda kv: -kv[1])[:k]`
5. `heapq.nlargest(k, counts, key=counts.get)`
6. The bucket version

Then time 1 against 2 and quote the ratio. Numbers 2 and 3 are the same mistake in two costumes —
say what the mistake is in one sentence.

### The derived-key drill

Build a `Counter` whose key is not the element itself. For a list of words, produce:

1. How many words of each length.
2. How many words start with each letter.
3. How many words share each set of letters, ignoring order.
4. How many words have each number of vowels.
5. How many words are the same when reversed.
6. How many words fall into each of `{short, medium, long}` by a rule you choose.

Number 3 is tomorrow's lesson. Say what the key is, precisely, and why a `list` cannot be used as one.

### The top-k drill

For each situation, say which of the three selection strategies you would use and give the deciding
number:

1. `n = 1,000`, `m = 900`, `k = 5`
2. `n = 1,000,000`, `m = 12`, `k = 3`
3. `n = 1,000,000`, `m = 800,000`, `k = 100,000`
4. `n = 50`, `m = 50`, `k = 50`
5. A stream you can only read once and cannot store
6. Ten machines each holding a tenth of the data

Situations 5 and 6 are not on the list of three. Say what each one actually needs, and name the idea.

### The pattern-definition drill

Answer each in one sentence, out loud:

1. What are the four parts of a pattern?
2. Which part do people skip, and why does it matter?
3. Name the three groups and the question each one answers.
4. Name two patterns from each group.
5. Give one thing a pattern is *not*.
6. Why is a class called `OrderFactoryFactory` a warning sign?

### The pain-to-pattern drill

For each symptom, name the axis that is moving and then the pattern. Then say what it costs.

1. "Adding a country means editing a function twelve people depend on."
2. "Testing this needs a live payment gateway."
3. "Every caller has to call six services in the right order."
4. "The third-party SDK's method names are nothing like ours and we cannot change either side."
5. "We want logging and caching on this service without touching it."
6. "This object has fifteen optional fields and the constructor has fifteen parameters."
7. "When an order ships, four unrelated things have to happen."
8. "We need exactly one connection pool for the whole process."

Then go back through all eight and mark the ones where you would do nothing yet, and say what would
change your mind.

### The over-application drill

For each, say whether the pattern is earning its keep, and give the test you applied:

1. A `Strategy` interface with one implementation and no test double.
2. A `Factory` producing one concrete class.
3. Three tax rates as three classes implementing `TaxRule`.
4. A `Facade` over six services, with no business rules in it.
5. A `Singleton` holding the database connection, in a codebase with 400 tests.
6. An `Adapter` around a vendor SDK used in one place.

Two of the six are defensible for a reason that has nothing to do with the number of
implementations. Name them and say the reason.

### The regret drill

Answer this out loud, in ninety seconds, as you would in an interview:

*Tell me about a pattern you applied and later regretted, or removed.*

If you have not shipped one yet, use the lesson's example and make it specific: which pattern, what
pain you thought you were solving, what actually happened, how many files you deleted, and what you
would look for before doing it again.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the top k most frequent elements.*
   The two halves separated, n and m named, all three selection strategies with their costs, one
   chosen with a reason, and the memory trade volunteered before it is asked for.

2. *Which design patterns have you used, and why?*
   The one-sentence definition with all four parts, the vocabulary argument, two or three you have
   used with the specific pain that caused each, the consequence you accepted, and one you regret.

3. *Why does bucket counting beat the O(n log n) sorting bound?*
   Because it does not compare — the counts are integers between 1 and n, so you index by them. Then
   the price: `n + 1` buckets allocated regardless, and when the heap wins instead.

---

## Before you move on

- [ ] I wrote the counting loop by hand, without `Counter`, from memory.
- [ ] I triggered `KeyError` on `counts[k] += 1` and fixed it three different ways.
- [ ] I proved that reading a missing key from a `defaultdict` changes `len()`.
- [ ] I timed `list.count()` inside a loop against `Counter` and can quote the ratio.
- [ ] I wrote top-k twice — heap and buckets — and can say which wins for which shape of input.
- [ ] I can say what the `len(result) == k` check has to be inside, and what breaks otherwise.
- [ ] I can give the four parts of a design pattern and say which one people skip.
- [ ] I can go from a symptom to an axis to a pattern for at least five of the eight symptoms.
- [ ] I have one specific pattern I regret, with numbers, ready to say out loud.
- [ ] I answered all three questions above out loud.
