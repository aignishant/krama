---
day: 7
track: lang-cpp
title: "std::unordered_map, std::map, std::set, and the choice between them"
theme: "Key-value and membership"
phase: "Languages: every language, every basic"
status: written
---

# Day 007 · C++ — std::unordered_map, std::map, std::set, and the choice between them

**Today's theme:** Key-value and membership

**After today you can:** You can count, group and deduplicate with a map in each language and explain what happens on a missing key.

**The interviewer asks it as:** *What does your language do when you read a key that is not there?*

---

## 1. What this is, and why it matters

C++ gives you two maps: `std::unordered_map`, a hash table with constant-time lookup and no order, and `std::map`, a sorted tree with logarithmic lookup and keys always in order. Both share one behaviour that surprises everyone: reading a missing key with `[]` creates it, storing a default value under it, and hands that back. `at()` refuses instead, and `find`, `count` and `contains` let you ask without touching anything. `std::set` is the keys-only version, sorted, with `std::unordered_set` as its hashed twin.

At work, the choice between the two maps is a real design decision you will be asked to justify, and the `[]`-inserts rule is the reason a "read-only" function can quietly double the size of a map. Interviewers ask "when would you use `std::map` over `std::unordered_map`", "what does `operator[]` do on a missing key", and "why does `m[k]` not compile on a `const` map", and the third is a direct consequence of the second.

## 2. The story

Devika is running the cloakroom at her cousin's wedding. Three hundred guests, one long counter, a wall of numbered hooks behind her, and a bowl of plastic tokens with the same numbers.

A guest hands over a shawl. Devika hangs it on hook 47, hands the guest token 47, and forgets about it. That is the whole system. When the guest comes back with token 47, Devika does not search three hundred hooks. She walks to 47 and lifts the shawl. It takes the same five seconds whether the wall has ten hooks in use or all three hundred.

Around eleven, a man hands her token 112. She goes to hook 112. It is empty. She is sure of it, because she never gave out 112; that batch of tokens is still in the sealed bag. So what does she do?

Devika, being Devika, comes back to the counter and says, "There is nothing under 112. This token was never issued." She refuses to hand over anything, and the man, embarrassed, finds his real token in the other pocket.

Her brother, who took over at midnight, handles it differently. A woman hands him token 200. He goes to the hook, finds nothing, comes back, and hands her an empty hanger with a straight face. No shawl, no explanation, just the empty hanger, as if that is what was always there.

And the hired boy at the far end of the counter does the third thing. Token 250, empty hook. He writes 250 on a fresh tag, hangs an empty hanger on hook 250, and gives the guest the hanger. Now hook 250 exists, with nothing on it, and at the end of the night the count of hooks in use is one higher than the number of things anyone ever left.

Meanwhile at the gate, Devika's aunt has the guest list on her phone, and her whole job is one question: is this name on it, yes or no. She does not care about order or how many times a name appears. Just in, or not in.

## 3. The idea in plain English

A **map** stores **values** under **keys**. `std::unordered_map<int, std::string>`, from `<unordered_map>`, maps int keys to string values. Write with `cloakroom[51] = "coat"`, count with `.size()`, remove with `.erase(47)`.

`unordered_map` finds a key by **hashing** it to a slot: constant time on average, and the entries sit in no meaningful order. That is Devika walking straight to hook 47. Keys need a hash function, which the standard library provides for numbers, strings and a few others; for your own types you write one, which day 25 covers.

`std::map`, from `<map>`, is the other choice. It keeps its keys **sorted** in a balanced tree, so lookup takes time proportional to the logarithm of the size, about twenty steps for a million entries, and walking it gives keys in order. Keys need only to be comparable with `<`. Pick `unordered_map` by default for speed; pick `map` when you need the keys in order, or need "the smallest key at least this big", or your key has no hash.

Now the missing key. `cloakroom[112]` on a key that is not there **inserts** it, with a default-constructed value, `""` for a string, `0` for a number, and returns that. The map is now one bigger. That is the hired boy hanging an empty hanger on a fresh hook. It is deliberate: it is what makes `counts[word]++` a complete counting program. It is also why `[]` does not exist on a `const` map: a read that might insert is not a read.

To ask without inserting: `cloakroom.contains(112)` gives a bool, C++20. `cloakroom.count(112)` gives 0 or 1. `cloakroom.find(112)` gives a marker that equals `cloakroom.end()` when the key is absent, and otherwise points at the entry, so you can find and read in one lookup. And `cloakroom.at(112)` refuses: it throws `std::out_of_range`, which stops the program with a message today and which day 9 teaches you to catch. Devika.

Walking a map: `for (const auto& [hook, item] : cloakroom)` uses day 5's structured bindings to name the key and value of each entry; the `const auto&` means "do not copy each entry", and day 12 explains the `&`.

A **set** is keys only. `std::set<std::string>`, from `<set>`, is sorted; `std::unordered_set` is hashed. `insert` adds, and adding a duplicate does nothing; `contains` is the aunt's question.

## 4. The picture

```
 std::unordered_map<int, std::string> cloakroom = {{47, "shawl"}, {48, "bag"}};

 cloakroom[47]        → hash → slot → "shawl"                  size 2
 cloakroom[112]       → hash → slot empty → INSERT {112, ""} → ""   size 3  ◄── changed!
 cloakroom.at(200)    → hash → slot empty → throw std::out_of_range   size 3
 cloakroom.contains(300) → false                                       size 3

 std::map<int, std::string>  keeps keys sorted in a tree
                 (48)
                /    \
             (47)    (51)         walk → 47, 48, 51, always in order
                                  lookup → about log2(n) steps
```

*Notice that the `[]` line changed the size and the other three did not. Notice that the tree costs a few extra steps per lookup and buys you order.*

## 5. The code, built step by step

Start `cloakroom.cpp` in a `day07` folder.

```cpp
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <unordered_map>
#include <vector>

int main() {
    std::unordered_map<int, std::string> cloakroom = {{47, "shawl"}, {48, "bag"}};
    cloakroom[51] = "coat";
    std::cout << cloakroom[47] << " " << cloakroom.size() << "\n";
```

```
shawl 3
```

Each entry in the literal is a pair in braces. `[]` writes a new key or reads an existing one.

The missing key, four ways.

```cpp
    std::cout << std::boolalpha << cloakroom.contains(112) << " " << cloakroom.count(112) << "\n";
    std::cout << "[" << cloakroom[112] << "] size now " << cloakroom.size() << "\n";
    std::cout << cloakroom.contains(112) << "\n";
```

```
false 0
[] size now 4
true
```

`contains` and `count` asked and changed nothing. Then `[]` printed an empty string and the size went from 3 to 4. Then `contains(112)` is `true`: the read created the key. Hold on to that middle line; it is the whole C++ half of today.

`find`, which asks and reads in one go.

```cpp
    auto found = cloakroom.find(47);
    if (found != cloakroom.end()) {
        std::cout << "hook " << found->first << " holds " << found->second << "\n";
    }
    if (cloakroom.find(200) == cloakroom.end()) {
        std::cout << "token 200 was never issued\n";
    }
```

```
hook 47 holds shawl
token 200 was never issued
```

`find` returns an **iterator**, a marker pointing at an entry, or at `end()`, which means "past the last one, not found". `found->first` is the key and `found->second` the value, because each entry is a `std::pair`. This is the idiom you write when you need both the check and the value from one lookup.

`at`, which refuses.

```cpp
    std::cout << cloakroom.at(48) << "\n";
    std::cout << cloakroom.at(200) << "\n";
```

```
bag
terminate called after throwing an instance of 'std::out_of_range'
  what():  _Map_base::at
Aborted (core dumped)
```

The first `at` worked. The second stopped the program. Remove that line before moving on.

Counting, which is where `[]`-inserts is a feature.

```cpp
    std::vector<std::string> items = {"shawl", "bag", "shawl", "coat", "shawl", "bag"};
    std::map<std::string, int> counts;
    for (const std::string& item : items) {
        counts[item]++;
    }
    for (const auto& [item, n] : counts) {
        std::cout << item << ": " << n << "\n";
    }
```

```
bag: 2
coat: 1
shawl: 3
```

`counts[item]` on a new key inserts `0`, then `++` makes it `1`. Exactly Go's behaviour. And because `counts` is a `std::map`, the walk comes out alphabetically without any sorting step; that is what you pay the logarithm for.

A set.

```cpp
    std::set<std::string> guests = {"Asha", "Ravi", "Meera"};
    std::vector<std::string> arrived = {"Ravi", "Asha", "Ravi", "Tom"};
    std::set<std::string> unique;
    for (const std::string& name : arrived) {
        unique.insert(name);
        if (!guests.contains(name)) {
            std::cout << "gatecrasher: " << name << "\n";
        }
    }
    std::cout << "unique arrivals: " << unique.size() << "\n";
```

```
gatecrasher: Tom
unique arrivals: 3
```

`insert` of the second `Ravi` did nothing. `contains` is the gate.

Here is the build, run, and output for the complete program.

```bash
g++ -std=c++20 -Wall -Wextra cloakroom.cpp -o cloakroom
./cloakroom
```

```
hook 47 holds shawl; 3 hooks in use
contains 112? false; count 112: 0
cloakroom[112] gave [] and the size is now 4
contains 112? true
find 47: shawl; find 200: never issued
counts, in key order:
  bag: 2
  coat: 1
  shawl: 3
gatecrasher: Tom
unique arrivals: 3
```

And the complete file.

```cpp
// cloakroom.cpp — day 7, unordered_map, map, set, and the missing key
// Build: g++ -std=c++20 -Wall -Wextra cloakroom.cpp -o cloakroom
// Run:   ./cloakroom
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <unordered_map>
#include <vector>

int main() {
    std::unordered_map<int, std::string> cloakroom = {{47, "shawl"}, {48, "bag"}};
    cloakroom[51] = "coat";
    std::cout << "hook 47 holds " << cloakroom[47] << "; " << cloakroom.size() << " hooks in use\n";

    std::cout << std::boolalpha;
    std::cout << "contains 112? " << cloakroom.contains(112) << "; count 112: " << cloakroom.count(112) << "\n";
    std::cout << "cloakroom[112] gave [" << cloakroom[112] << "] and the size is now " << cloakroom.size() << "\n";
    std::cout << "contains 112? " << cloakroom.contains(112) << "\n";

    auto found = cloakroom.find(47);
    std::cout << "find 47: " << (found != cloakroom.end() ? found->second : "never issued");
    auto missing = cloakroom.find(200);
    std::cout << "; find 200: " << (missing != cloakroom.end() ? missing->second : "never issued") << "\n";

    std::vector<std::string> items = {"shawl", "bag", "shawl", "coat", "shawl", "bag"};
    std::map<std::string, int> counts;
    for (const std::string& item : items) {
        counts[item]++;
    }
    std::cout << "counts, in key order:\n";
    for (const auto& [item, n] : counts) {
        std::cout << "  " << item << ": " << n << "\n";
    }

    std::set<std::string> guests = {"Asha", "Ravi", "Meera"};
    std::vector<std::string> arrived = {"Ravi", "Asha", "Ravi", "Tom"};
    std::set<std::string> unique;
    for (const std::string& name : arrived) {
        unique.insert(name);
        if (!guests.contains(name)) {
            std::cout << "gatecrasher: " << name << "\n";
        }
    }
    std::cout << "unique arrivals: " << unique.size() << "\n";
    return 0;
}
```

The `condition ? a : b` form is the **conditional expression**: `a` if the condition holds, otherwise `b`. The two sides must have a common type, and here the quoted text converts to a `std::string` to match the other side.

## 6. How the other two languages do it

Python, where `[]` refuses and `get` returns a default without inserting:

```python
cloakroom = {47: "shawl", 48: "bag"}
print(cloakroom[112])                 # KeyError: 112
print(cloakroom.get(112, ""))         # "", and len is still 2
print(sorted(cloakroom))              # order on demand; the dict itself keeps insertion order
```

Go, where `[]` returns the zero value without inserting, and a second result says whether it was real:

```go
cloakroom := map[int]string{47: "shawl", 48: "bag"}
fmt.Println(cloakroom[112])           // "", and len is still 2
item, ok := cloakroom[112]            // ok == false
```

The one line of difference that matters: **C++ `[]` inserts on a miss; Python's raises; Go's returns zero and leaves the map alone.** All three languages let you count with one line, but only C++ makes that line mutate the map on a read, which is why the same `[]` is forbidden on a `const` map and why C++ programmers reach for `find` or `contains` when they mean "look, do not touch". The second difference: C++ makes you choose between hashed and sorted up front, `unordered_map` or `map`. Python and Go give you only the hashed one and you sort the keys yourself when you need order.

## 7. The traps

**The near-miss: the read that inserts.** Check whether a hook is free.

```cpp
    if (cloakroom[300] == "") {
        std::cout << "hook 300 is free\n";
    }
    std::cout << cloakroom.size() << "\n";
```

```
hook 300 is free
5
```

It printed the right thing and the map grew. Hook 300 now exists with an empty string on it, and every later walk over the map will visit it. Use `contains(300)` or `find(300) == end()`.

**The real error: `[]` on a `const` map.** Pass a map to a function that promises not to change it.

```cpp
void show(const std::unordered_map<int, std::string>& m) {
    std::cout << m[47] << "\n";
}
```

```
cloakroom.cpp: In function 'void show(const std::unordered_map<int, std::string>&)':
cloakroom.cpp:10:19: error: passing 'const std::unordered_map<int, std::__cxx11::basic_string<char> >' as 'this' argument discards qualifiers [-fpermissive]
   10 |     std::cout << m[47] << "\n";
      |                   ^
```

The message is ugly but the reason is clean: `[]` might insert, inserting changes the map, and you promised not to change it. Use `m.at(47)` or `m.find(47)` in a `const` context. Day 12 covers `const` and `&` properly; today, know that this error means "you used `[]` on a map you are not allowed to modify".

**The near-miss: relying on `unordered_map` order.** Print the cloakroom.

```cpp
    for (const auto& [hook, item] : cloakroom) {
        std::cout << hook << " ";
    }
```

```
51 48 47 
```

Or some other order. Or a different order after one more insert triggers a rehash. If the order matters, use `std::map`, or copy the keys into a vector and sort them.

## 8. Say it out loud

**How it gets asked**

- "When would you choose `std::map` over `std::unordered_map`?"
- "What does `operator[]` do when the key is not present?"
- "Why does `m[k]` not compile when `m` is `const`?"

**What to say out loud, the first ninety seconds**

"`std::unordered_map` is a hash table: average O(1) lookup, insert and erase, keys in no particular order, and it needs a hash for the key type. `std::map` is a balanced binary tree: O(log n) for the same operations, keys kept sorted, and it needs only `operator<`. I default to `unordered_map` and switch to `map` when I need ordered iteration, range queries like lower_bound, or a key type with no hash.

On both, `operator[]` with an absent key inserts a value-initialised entry and returns a reference to it. That makes counting `counts[k]++` correct with no setup, and it makes a naive existence check `if (m[k] == ...)` silently grow the map. For a non-mutating check I use `contains` in C++20, `count`, or `find` compared with `end()`, which also gives me the value in the same lookup. `at()` throws `std::out_of_range` instead of inserting. Because `[]` may insert, it is not a `const` member function, so calling it on a `const` map is a compile error; `at` and `find` work there. `std::set` and `std::unordered_set` are the key-only counterparts with the same trade-off."

**The follow-ups**

1. *"What is the complexity of `unordered_map` in the worst case?"* — O(n), when many keys collide into one bucket. A good hash function and the automatic rehash keep it O(1) in practice; an adversary who controls the keys can force the worst case.
2. *"What happens to iterators when an `unordered_map` rehashes?"* — They are invalidated, like a vector on reallocation. References to the values themselves remain valid, which is a nice property of node-based containers. `std::map` never invalidates on insert.
3. *"How do you insert only if the key is absent?"* — `try_emplace(k, args...)` or `insert({k, v})`, both of which return a pair of iterator and bool telling you whether the insert happened, in one lookup.

**A model answer**

"C++ offers `std::unordered_map`, a hash table with average O(1) operations and unspecified order, and `std::map`, a red-black tree with O(log n) operations and sorted keys; choose the tree for ordered traversal or range queries, the hash otherwise. On both, `operator[]` on an absent key inserts a value-initialised element and returns a reference, which is why it is non-`const` and why `counts[k]++` needs no initialisation. Non-mutating lookups are `contains`, `count`, or `find` against `end()`; `at` throws `std::out_of_range`. `std::set` and `std::unordered_set` are the key-only versions. Rehashing invalidates `unordered_map` iterators but not references to elements; `std::map` iterators survive inserts. `try_emplace` inserts only if absent and reports whether it did."

## 9. Recall card

- `std::unordered_map`: hashed, O(1) average, no order; `std::map`: tree, O(log n), keys sorted; same for `unordered_set` and `set`.
- `m[k]` on a missing key inserts a default value and returns it, so the map grows on a read; that is why `counts[k]++` works and why `[]` is an error on a `const` map.
- Ask without touching: `m.contains(k)`, `m.count(k)`, or `auto it = m.find(k); if (it != m.end()) use it->second`.
- `m.at(k)` throws `std::out_of_range` (`what(): _Map_base::at`) instead of inserting.
- Walk with `for (const auto& [key, value] : m)`; never rely on `unordered_map` order, and expect it to change after a rehash.
