---
day: 7
track: lang-practice
title: "Practice — Key-value and membership"
status: written
---

# Day 007 · Practice

**Theme:** Key-value and membership

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

Three questions from today. Answer each in two minutes, standing up, no notes.

1. What does your language do when you read a key that is not there?
2. Why is a hash-table lookup constant time, and what does that require of the key?
3. When would you choose a sorted map over a hashed one, and how do you get sorted output from a hashed one in each language?

## Before you move on

- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered all three questions above out loud.
