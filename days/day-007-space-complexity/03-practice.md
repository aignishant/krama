---
day: 7
track: practice
title: "Practice — Space complexity, and what in-place really means"
status: written
---

# Day 007 · Practice

**DSA topic:** Space complexity, and what in-place really means
**System design topic:** What a web server actually does

**Theme:** Key-value and membership

---

## Code these, in this order

Four problems that each have an easy `O(n)`-space solution and a harder `O(1)`-space one.
Write **both** versions of every one of them. The second version is the exercise.

For each problem:

1. Write the natural solution and state its extra space.
2. Then ask yourself the interviewer's question: *can I do this in `O(1)` extra space?*
3. Write that version, and state exactly what you kept: how many variables, and why none of
   them grow.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Reverse String | LeetCode 344 (Easy) | The problem statement explicitly demands `O(1)` extra space, which is why the input is a character list rather than a string. Two pointers and a swap. |
| 2 | Remove Duplicates from Sorted Array | LeetCode 26 (Easy) | The write pointer, in its purest form. The signature returns a length rather than a list, and that is the whole hint. |
| 3 | Move Zeroes | LeetCode 283 (Easy) | Same pattern, one step harder. Building a new list is trivial; doing it in place with one pass and one extra index is the point. |
| 4 | Majority Element | LeetCode 169 (Easy) | Three solutions with three different space costs: a `Counter` is `O(n)`, sorting is `O(1)` extra with an in-place sort, and Boyer-Moore is `O(1)` with one candidate and one count. |

### On problem 4, do this properly

Write all three. Then say out loud, for each one, the time and the extra space:

- `Counter(nums).most_common(1)` →
- `sorted(nums)[len(nums) // 2]` →
- Boyer-Moore voting →

Then answer the question that matters: **what did Boyer-Moore replace the whole count map
with?** If you can say that in one sentence, you have understood what "reformulate the state"
means, and it is the fourth of the four moves from §8 of the lesson.

### The measurement drill

Run the complete program from §5 at `N = 200_000`, then at `N = 400_000`.

The `O(n)` rows should double. The `O(1)` rows should stay at zero. Then add one line of your
own to the program — a function that solves any of today's problems by slicing — and confirm
it lands in the `O(n)` group even though it is one line long.

### The trap drill

Type this out and run it before you read the answer:

```python
def reverse(items):
    items = items[::-1]

nums = [1, 2, 3, 4]
reverse(nums)
print(nums)
```

Predict the output first. Then explain, out loud, in one sentence, why assigning to `items`
inside the function did nothing — and name the two ways to write it so that it does.

---

## Build these, in all three languages

Three exercises, easiest first. Every exercise is done three times: once in Python, once in Go, once in C++. Before each lookup of a key that might be missing, say out loud which of the three cloakroom attendants this language is.

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Count the words in the sentence `"the cat sat on the mat the end"` and print each word with its count, in alphabetical order. Then print the count for `"dog"`, a word that is not there, without crashing and without adding it. | Can you count with a map, sort the keys, and read a missing key safely in each language? |
| 2 | Group the numbers 1 to 20 by their remainder when divided by 3, so that the key `0` holds `[3, 6, 9, ...]` and so on. Print the groups. Then delete the group for remainder `1` and print the size. | Can you build a map whose values are sequences, starting each sequence from nothing, and remove a key? |
| 3 | Two guest lists: invited `{"Asha", "Ravi", "Meera", "Tom"}` and arrived `["Ravi", "Asha", "Ravi", "Priya"]`. Print who arrived that was not invited, who was invited and never arrived, and how many distinct people arrived. Then, in each language, write the innocent-looking existence check that *changes the map* if the language allows it, and prove whether it did by printing the size before and after. | Do you know the set operations, and have you personally seen which language's `[]` inserts on a read? |

**Exercise 1, what you should notice.** Counting is `get(w, 0) + 1` in Python, `counts[w]++` in Go, and `counts[w]++` in C++. The last two look identical and only C++'s version would also insert on a bare read. Sorted output is `sorted(d)` in Python, `slices.Sorted(maps.Keys(m))` in Go, and free with `std::map` in C++. The safe miss is `get`, comma-ok, and `contains` or `find`.

**Exercise 2, what you should notice.** Python `setdefault(k, []).append(n)`; Go `groups[k] = append(groups[k], n)`, which works because a missing key reads as a nil slice; C++ `groups[k].push_back(n)`, which works because `[]` inserts an empty vector. Delete is `del d[k]`, `delete(m, k)`, `m.erase(k)`.

**Exercise 3, what you should notice.** Python has real set algebra: `arrived - invited`, `invited - arrived`. Go has none; you write the loops over `map[string]bool`. C++ has `std::set` but the algebra lives in `<algorithm>` as `std::set_difference`, which is awkward enough that most people write the loop. For the existence check: Python's `d[k] == ""` raises; Go's `m[k] == ""` is fine and inserts nothing; C++'s `m[k] == ""` inserts and the size grows by one.

## Compare

- **Python** — dict and set: hashing, ordering, and the in operator. Refuses a missing key with `KeyError`, offers `get` and `in`, keeps insertion order, and has a real set with real algebra.
- **Go** — map: make, lookup with the comma-ok idiom, delete, and no order. Returns the zero value on a miss and a second `ok` result on request, randomises iteration order on purpose, has no set, and panics on a write to a nil map.
- **C++** — std::unordered_map, std::map, std::set, and the choice between them. Inserts on a miss through `[]`, refuses through `at`, asks through `find` and `contains`, and makes you choose hashed or sorted up front.

## Say these out loud

### DSA and system design
Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *Can you do that in O(1) extra space?*
   Use problem 3. Say what you would keep, why it does not grow, and what you gave up to get
   there.

2. *What happens inside the server between receiving a request and sending a response?*
   Four words for the loop, then the nine steps of handling, then the one-worker-one-request
   constraint.

3. *How many requests per second can one machine handle?*
   Do not guess. Pick a request duration, pick a worker count, do the division out loud, then
   state Little's Law and use it to turn a target into a worker count.



### Languages
Three questions from today. Answer each in two minutes, standing up, no notes.

1. What does your language do when you read a key that is not there?
2. Why is a hash-table lookup constant time, and what does that require of the key?
3. When would you choose a sorted map over a hashed one, and how do you get sorted output from a hashed one in each language?

## Before you move on

- [ ] I say "O(1) **extra** space" and can explain what I am not counting.
- [ ] I can reverse an array in place with two pointers, from memory, first try.
- [ ] I know that `items.sort()` is in place and still `O(n)` auxiliary, and which sort is
      genuinely `O(1)`.
- [ ] I count recursion depth as space, every time.
- [ ] I can say the server loop in four words and name the three concurrency models with
      their memory costs.
- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered the DSA, system design, and language questions out loud.
