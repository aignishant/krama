---
day: 6
track: cpp
title: "string, map, set, and pair: half of DSA in four containers"
phase: "C++ and competitive programming"
status: written
---

# Day 006 · C++ — string, map, set, and pair: half of DSA in four containers

**After today you can:** You can choose between map and unordered_map with a reason, and count, group and deduplicate anything.

**The interviewer asks it as:** *When would you use std::map instead of std::unordered_map?*

---

> Fifth of the twelve C++ days, and the twin of today's DSA lesson. After this you have enough C++
> to solve real problems, and the next C++ day is not until day 042. From tomorrow, do the
> course's problems in C++ as well as Python.

---

## 1. What this is, and why they ask it

Python gives you one dictionary and one set. C++ gives you two of each, and makes you choose.

`std::unordered_map` is the one that matches Python's `dict`: it finds a key in O(1) on average
by computing a number from the key and going straight to a slot. `std::map` is different — it
keeps its keys **in sorted order**, in a balanced tree, and finds a key in O(log n). It is
slower for a single lookup and it can do things the fast one cannot: give you the smallest key,
walk the keys in order, or find the first key at least as large as 50.

Choosing wrongly costs you either speed or correctness, and the choice comes up in almost every
problem, so interviewers ask it constantly. "`map` is a tree, `unordered_map` is a hash table" is
half an answer. The full answer names what the ordering buys you and what the collisions cost
you, and that is what this lesson gives you.

Today's DSA lesson gives you Python's strings, dictionaries and sets. This gives you the C++
versions, plus the one container Python does not have a separate name for: `pair`.

---

## 2. The story

Anjali took over her father's medical shop on Hamidia Road when he had his knee done, and stayed
on afterwards because he was slower on the stairs than he admitted.

Her father had arranged the whole shop alphabetically. Two hundred and forty small drawers, four
walls of them, running A at the top left round to Z by the back door. Anjali had grown up with
it. Somebody asked for something and she walked to roughly the right wall, ran her eye down, and
had it in about eight seconds. Not instant. But when a company man came in and asked what she
was stocking that began with "Aten", she opened four drawers in a row and told him, because
everything beginning with those letters sat together. She could give him a whole stretch of the
alphabet in the time it took to say it.

Then Suresh started, in the second week of June. Seventeen, quick, and he could not read the
small print on the drawer labels at any speed at all.

What he did instead was memorise the shop. Not the order of it — the position of each name in
it. Somebody said a name and his hand went to the drawer. No walking, no scanning, no working
from A towards M. Anjali timed him once against herself on eleven different names and he beat her
on every one, usually by half.

Two things went wrong with it, and they were both instructive.

The first was that when the company man came back in August and asked the same kind of question —
everything from M to P, he wanted to know — Suresh was no use at all. He knew two hundred and
forty exact positions and nothing whatever about which was near which. To answer he would have
had to go through every drawer in the shop.

The second was a Thursday in September, when a bulk order came in and it happened, by chance,
that eleven of the names on it lived in the same crowded drawer at the bottom of the third wall.
Suresh's hand went to the right drawer eleven times, instantly, and then he had to pick through
the same overfull drawer eleven times. That afternoon he was slower than Anjali.

Most days, though, he was faster. It was only the days somebody wanted a stretch of the alphabet,
or the drawer happened to be crowded.

---

## 3. The idea in plain English

Anjali is a `std::map`. Suresh is a `std::unordered_map`. The whole lesson is in the story.

### `unordered_map`: go straight to the slot

An **unordered_map** stores key-value pairs. To find a key it computes a number from the key —
that number is called a **hash** — and uses it to jump straight to one of many slots, called
**buckets**. No searching, no walking. That is Suresh's hand going to the drawer.

```cpp
#include <unordered_map>

std::unordered_map<std::string, int> count;
count["salt"] = 3;
count["sugar"]++;
if (count.count("salt")) std::cout << count["salt"];
```

Average cost is **O(1)** for insert, lookup and erase. It is Python's `dict`, and it is your
default.

The words you need: two different keys can hash to the same bucket, which is a **collision**.
The bucket then holds several entries and has to be searched through. With a good hash and
ordinary data, buckets hold one or two entries and the O(1) holds. With unlucky or *deliberately
chosen* data, one bucket holds everything and lookup degrades to O(n). That is the crowded drawer
on the Thursday, and section 7 shows how it is used as a weapon against you in contests.

### `map`: sorted, always

A **map** stores the same key-value pairs, but in a balanced binary search tree, keeping the keys
in sorted order at all times. Finding a key means walking down the tree, comparing as you go:
**O(log n)**, not O(1).

```cpp
#include <map>

std::map<std::string, int> count;
count["salt"] = 3;

for (const auto& [key, value] : count)     // ALWAYS in sorted key order
    std::cout << key << " " << value << "\n";
```

What you buy for that log n:

| You can ask | `map` | `unordered_map` |
|---|---|---|
| the value for a key | O(log n) | **O(1) average** |
| iterate in sorted order | **yes, free** | no — arbitrary order |
| the smallest / largest key | **O(1)**, `begin()` / `rbegin()` | no |
| the first key ≥ 50 | **O(log n)**, `lower_bound` | no |
| every key between 20 and 60 | **yes**, walk from `lower_bound` | no — check all n |
| worst case | **O(log n), guaranteed** | O(n) |

The last row matters more than it looks. `map` has no bad days. `unordered_map` has the
Thursday.

### The rule

> **Default to `unordered_map`. Switch to `map` the moment you need order, a range, or a
> guaranteed worst case.**

Say it in an interview as "I reach for `unordered_map` for plain lookup, and `map` when I need
the keys ordered or I need `lower_bound`". That one sentence is the whole answer.

`set` and `unordered_set` are the same pair with the values removed — they store keys only, for
membership and deduplication. And `multiset` allows duplicates, which is a real tool: it is a
sorted bag you can erase the smallest element from in O(log n).

### `std::string`

C++'s string is closer to Python's list than to Python's string, in one crucial way: **it is
mutable**.

```cpp
#include <string>

std::string s = "hello";
s[0] = 'H';                      // legal. Python cannot do this.
s += " world";                   // O(1) amortised, exactly like vector::push_back
std::string t = s.substr(0, 5);  // "Hello" — a COPY, O(k)
int n = s.size();
```

That mutability removes a trap you have to work around in Python. Today's DSA lesson warns you
that building a string with `+=` in a loop is quadratic in Python, because each `+` builds a
whole new string. In C++, `s += "x"` appends into spare capacity and is **O(1) amortised**, so
the obvious loop is already the right one. [Day 020](../day-020-building-strings/README.md) is
about that trap; in C++ you simply do not have it.

The operations you will use constantly:

```cpp
s.size(), s.empty(), s.back(), s.push_back('x'), s.pop_back()
s.substr(pos, len)                  // copy of a piece
s.find("abc")                       // position, or std::string::npos
std::sort(s.begin(), s.end())       // sort the characters, in place
std::stoi(s), std::stoll(s)         // string to number
std::to_string(42)                  // number to string
s1 + s2, s1 == s2, s1 < s2          // concatenate and compare, as you would expect
```

Character arithmetic is the other thing worth having in your fingers. A `char` **is a small
number**, so:

```cpp
int i = c - 'a';        // 'a'->0, 'b'->1, ... 'z'->25
char c = 'a' + i;       // back again
bool digit = (c >= '0' && c <= '9');
```

That `c - 'a'` is how you count letters into a 26-slot table instead of a map, which is faster
and is what you want for [day 021](../day-021-frequency-maps/README.md).

### `pair` and `tuple`

C++ has no tuple literal, so pairs are a named thing.

```cpp
#include <utility>

std::pair<int, int> p = {3, 7};
std::cout << p.first << " " << p.second;

std::vector<std::pair<int, std::string>> v;
v.push_back({5, "apple"});
```

Two facts make pairs worth knowing. They compare **lexicographically** — first by `.first`, then
by `.second` — so sorting a `vector<pair<int,string>>` sorts by the number and breaks ties by the
word, for free. And they are the natural element for a grid coordinate, a weighted edge, or a
value with its position attached.

Since C++17 you can unpack one on the spot, which is called a **structured binding**:

```cpp
auto [row, col] = position;
for (const auto& [key, value] : counts) { ... }
```

That reads exactly like Python's `for key, value in counts.items()`.

For three or more values, `std::tuple<int,int,int>` and `auto [a,b,c] = t;`. For anything you
will keep, define a `struct` instead — it gives the fields names, and names beat `.first.second`.

---

## 4. The picture

The two containers, drawn as the shop:

```
  std::map  —  Anjali's alphabetical wall
  a balanced tree, keys always in sorted order

                      +--------+
                      | "sugar"|
                      +--------+
                     /          \
              +-------+        +--------+
              | "salt"|        | "tulsi"|
              +-------+        +--------+
             /        \
      +--------+   +-------+
      | "atta" |   | "rice"|
      +--------+   +-------+

  find("rice"):  sugar -> salt -> rice.   3 comparisons for 5 keys.
                 log2(n) steps, ALWAYS.  There is no bad day.
  walking left-to-right gives: atta, rice, salt, sugar, tulsi   <- sorted, free


  std::unordered_map  —  Suresh's memory
  buckets, reached by computing a number from the key

    hash("rice")  = 4382719  ->  4382719 % 8  =  bucket 7

    bucket  0    1    2    3    4    5    6    7
          +----+----+----+----+----+----+----+----+
          |    |atta|    |salt|    |sugar|   |rice|
          +----+----+----+----+----+----+----+----+
                                              |
                                           tulsi        <- a collision:
                                                           two keys, one bucket

  find("rice"):  compute the number, go to bucket 7, compare.  1 step.
  find("tulsi"): compute, go to bucket 7, compare 'rice', compare 'tulsi'.  2 steps.
  walking the buckets gives: atta, salt, sugar, rice, tulsi   <- NOT sorted
```

**What to notice:** the tree picture has an order you can read off left to right. The bucket
picture does not — the keys are scattered by a number that has nothing to do with their meaning.
That is the entire trade. You gave up order to get the direct jump.

And the bad day:

```
  every key lands in bucket 3

    bucket  0    1    2    3    4    5    6    7
          +----+----+----+----+----+----+----+----+
          |    |    |    | k1 |    |    |    |    |
          +----+----+----+-|--+----+----+----+----+
                           k2
                           k3
                            .
                            .
                           k100000        <- find() now walks 100,000 entries

  O(1) has become O(n).  The map's tree cannot do this to you.
```

**What to notice:** nothing is broken, and no error is reported. The container still returns the
right answers. It just takes a hundred thousand times longer, which on a judge is a time-limit
verdict with no explanation.

---

## 5. The code, built step by step

### Counting, which is half of all DSA problems

```cpp
std::unordered_map<std::string, int> freq;
for (const std::string& w : words) freq[w]++;
```

Two lines. `freq[w]` creates the entry with value 0 if it is not there, then `++` makes it 1. It
is Python's `Counter` in one line, and it is the single most useful idiom in the language.

For characters, skip the map entirely:

```cpp
std::array<int, 26> freq{};              // 26 zeros
for (char c : s) freq[c - 'a']++;
```

That is a fixed 104-byte table with no hashing and no allocation, and it is roughly twenty times
faster than a map. Use it whenever the keys are lowercase letters.

### Membership and deduplication

```cpp
std::unordered_set<int> seen;
for (int x : v) {
    if (seen.count(x)) { /* duplicate */ }
    seen.insert(x);
}
```

`.count(k)` returns 0 or 1 and is the idiomatic "is it there". C++20 adds `.contains(k)`, which
reads better; use it if your judge is on C++20.

To deduplicate a vector and keep it sorted, the standard trick:

```cpp
std::sort(v.begin(), v.end());
v.erase(std::unique(v.begin(), v.end()), v.end());
```

`std::unique` collapses *adjacent* equal elements, which is why the sort has to come first. This
is O(n log n) and beats building a set when you want the result as a vector.

### Grouping, which is [day 064](../day-064-grouping/README.md) and the anagram problem

```cpp
std::unordered_map<std::string, std::vector<std::string>> groups;
for (const std::string& w : words) {
    std::string key = w;
    std::sort(key.begin(), key.end());    // "eat" and "tea" both become "aet"
    groups[key].push_back(w);
}
```

`groups[key]` on a missing key creates an empty vector and returns a reference to it, so
`.push_back` on the same line just works. That is `defaultdict(list)` without needing a
`defaultdict`.

### The ordered operations, which are why `map` exists

```cpp
std::map<int, std::string> m = {{10,"a"}, {20,"b"}, {30,"c"}};

auto it = m.lower_bound(15);     // first key >= 15  -> 20
auto jt = m.upper_bound(20);     // first key >  20  -> 30

int smallest = m.begin()->first;         // 10, O(1)
int largest  = m.rbegin()->first;        // 30, O(1)

for (auto it = m.lower_bound(15); it != m.end() && it->first <= 30; ++it)
    std::cout << it->first << " ";       // 20 30 — a range walk
```

None of that exists on `unordered_map`. When a problem says "the nearest value not less than x"
or "everything in this range", that is a `map` or a sorted `vector`, and the choice is made for
you.

### A hash for `pair`, because C++ does not provide one

`unordered_map<pair<int,int>, int>` does not compile. The standard library ships hashes for the
built-in types and `string`, and not for `pair`. For grid coordinates you have three options,
best first:

```cpp
// 1. Pack two ints into one long long. Fastest, and no custom code.
std::unordered_map<long long, int> seen;
seen[1LL * row * 100000 + col] = 1;

// 2. Use std::map<std::pair<int,int>, int>, which needs only <, which pair has.
std::map<std::pair<int,int>, int> ok;

// 3. Write a hash. Needed if you want unordered_map with a pair key.
struct PairHash {
    size_t operator()(const std::pair<int,int>& p) const {
        return std::hash<long long>()(1LL * p.first * 1000003 + p.second);
    }
};
std::unordered_map<std::pair<int,int>, int, PairHash> grid;
```

Option 1 is what experienced competitive programmers actually write.

### The complete program

```cpp
// containers.cpp — string, map, set and pair, and when each one is right.
//   g++ -std=c++20 -O2 -Wall -Wextra -o containers containers.cpp && ./containers

#include <bits/stdc++.h>
using namespace std;

// Group words that are rearrangements of each other. Day 022's problem, in C++.
vector<vector<string>> group_anagrams(const vector<string>& words) {
    unordered_map<string, vector<string>> groups;
    for (const string& w : words) {
        string key = w;
        sort(key.begin(), key.end());        // the shared signature
        groups[key].push_back(w);
    }
    vector<vector<string>> out;
    for (auto& [key, list] : groups) out.push_back(list);
    return out;
}

// Count characters without a map: 26 slots, no hashing, no allocation.
array<int, 26> letter_counts(const string& s) {
    array<int, 26> freq{};                   // the {} zero-fills. Without it: rubbish.
    for (char c : s)
        if (c >= 'a' && c <= 'z') freq[c - 'a']++;
    return freq;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // ---- string: mutable, and += is cheap ----
    string s = "hello";
    s[0] = 'H';
    s += " world";
    cout << s << " | size " << s.size() << " | first5 " << s.substr(0, 5) << "\n";

    size_t at = s.find("world");
    cout << "find(\"world\") = " << (at == string::npos ? -1 : (int)at) << "\n";
    cout << "find(\"xyz\")   = " << (s.find("xyz") == string::npos ? "npos" : "found") << "\n";

    // ---- counting with a map ----
    vector<string> words = {"tea", "eat", "tan", "ate", "nat", "bat", "tea"};
    unordered_map<string, int> freq;
    for (const string& w : words) freq[w]++;
    cout << "tea appears " << freq["tea"] << " times\n";

    // ---- grouping ----
    cout << "anagram groups: " << group_anagrams(words).size() << "\n";

    // ---- set: deduplicate ----
    vector<int> v = {5, 3, 5, 8, 3, 1};
    unordered_set<int> uniq(v.begin(), v.end());
    cout << "distinct values: " << uniq.size() << "\n";

    // ---- map: the ordered operations unordered_map cannot do ----
    map<int, string> m = {{10, "a"}, {20, "b"}, {30, "c"}};
    cout << "smallest key " << m.begin()->first
         << " largest key " << m.rbegin()->first << "\n";
    cout << "first key >= 15 is " << m.lower_bound(15)->first << "\n";
    cout << "in order:";
    for (const auto& [key, value] : m) cout << " " << key << "=" << value;
    cout << "\n";

    // ---- pair: sorts by first, then second, for free ----
    vector<pair<int, string>> people = {{30, "meera"}, {25, "farid"}, {30, "anjali"}};
    sort(people.begin(), people.end());
    cout << "sorted:";
    for (const auto& [age, name] : people) cout << " " << age << ":" << name;
    cout << "\n";

    // ---- the 26-slot table ----
    auto counts = letter_counts("mississippi");
    cout << "s appears " << counts['s' - 'a'] << " times\n";

    return 0;
}
```

Expected output:

```
Hello world | size 11 | first5 Hello
find("world") = 6
find("xyz")   = npos
tea appears 2 times
anagram groups: 3
distinct values: 4
smallest key 10 largest key 30
first key >= 15 is 20
in order: 10=a 20=b 30=c
sorted: 25:farid 30:anjali 30:meera
s appears 4 times
```

Note `sorted: 25:farid 30:anjali 30:meera` — the two thirty-year-olds came out alphabetically
without you asking, because pairs compare on `.second` when `.first` ties.

---

## 6. What it costs

### Time, per operation

Measured on 10^6 operations with `int` keys, on an ordinary machine:

```
  container                  insert      lookup     notes
  -----------------------    --------    --------   -------------------------
  vector<int> push_back        ~2 ns       ~1 ns    if you can index directly, do
  array<int,26>                   —        ~1 ns    the 26-slot table
  unordered_map<int,int>      ~90 ns      ~45 ns    one hash, one jump
  map<int,int>               ~180 ns     ~140 ns    log n comparisons, pointer chasing
  unordered_map<string,int>  ~140 ns      ~75 ns    hashing a string costs more
```

`map` is roughly **three times slower** than `unordered_map` for a plain lookup. Not a hundred
times — three. That is why "always use `unordered_map`" is bad advice: three times is often a
price worth paying for guaranteed worst-case behaviour and free ordering.

Put it in a problem's terms:

```
  n = 10^6 lookups

  unordered_map:  10^6 x  45 ns  =  0.045 s
  map:            10^6 x 140 ns  =  0.140 s
  a plain vector: 10^6 x   1 ns  =  0.001 s

  unordered_map on its BAD day (everything in one bucket):
                  10^6 x 10^6 / 2 comparisons  =  5 x 10^11   -> hours
```

### Memory, which is the cost nobody mentions

```
  vector<int>, 10^6 elements
    = 10^6 x 4 bytes                    =  4 MB

  unordered_map<int,int>, 10^6 entries
    = 8 bytes of data + ~24 bytes of node and pointer overhead, plus the bucket array
    ~ 10^6 x 32 + 8 MB                  =  ~40 MB

  map<int,int>, 10^6 entries
    = 8 bytes of data + ~40 bytes per tree node (three pointers, a colour, padding)
    ~ 10^6 x 48                         =  ~48 MB
```

**A map costs about ten times what the same data costs in a vector.** On a 256 MB limit that is a
real constraint, and it is why "sort a vector of pairs and binary search it" beats a `map` in many
contest problems: same log n lookup, a tenth of the memory, and far better cache behaviour
because the data is contiguous.

The cache point is worth one more sentence. A `map` scatters its nodes across the heap, so every
step down the tree is likely a cache miss — about 100 nanoseconds of waiting. A sorted vector
keeps everything adjacent, so the same binary search touches memory that is already close by.
This is why the measured gap is three times rather than the "same log n" theory would suggest.

---

## 7. The traps

### The near-miss: `m[key]` inserts

The single most common `map` bug in C++, and Python programmers walk straight into it because
Python's `d[key]` raises instead.

```cpp
std::map<std::string, int> m;
m["salt"] = 3;

if (m["sugar"] == 0)            // "sugar" is not in the map...
    std::cout << "no sugar\n";

std::cout << m.size();          // 2.  Reading it CREATED it.
```

`operator[]` on a missing key **default-constructs the value and inserts it**. For `int` that is
0, so the comparison is true and the code looks right — but the map has silently grown. In a loop
over a million missing keys you have just built a million-entry map by reading.

It also does not compile at all on a `const` map, for exactly this reason.

Three safe ways to read:

```cpp
if (m.count("sugar"))      { ... }      // 0 or 1, no insert
if (m.contains("sugar"))   { ... }      // C++20, reads better
if (auto it = m.find("sugar"); it != m.end()) { use(it->second); }   // lookup once
```

The `find` form is best when you need the value too, because it does one lookup rather than two.

### The real error: `.at()` when the key is missing

`.at()` is the checked version, and it throws rather than inserting:

```
terminate called after throwing an instance of 'std::out_of_range'
  what():  map::at
Aborted (core dumped)
```

For `unordered_map` the message is `what():  _Map_base::at`. Neither tells you which key, which
is why `.at()` is a poor debugging tool but a good production one.

### The real error: `unordered_map` with a `pair` key

```cpp
std::unordered_map<std::pair<int,int>, int> grid;    // does not compile
```

The message is long and template-heavy. The line that matters, buried in it, is:

```
/usr/include/c++/13/bits/hashtable_policy.h:1319:7: error: static assertion failed: hash function must be invocable with an argument of key type
 1319 |       static_assert(__is_invocable<const _Hash&, const _Key&>{},
      |       ^~~~~~~~~~~~~
```

**When a C++ error is two hundred lines, search it for `static assertion failed` or the first
line that names your own file.** Everything else is the library explaining itself to itself. The
fix here is one of the three options from section 5, and packing into a `long long` is the
easiest.

### The near-miss: `s.find` returns an unsigned value

```cpp
if (s.find("abc") >= 0) { /* always true */ }
```

`find` returns `size_t`, which is unsigned, and when it fails it returns `std::string::npos` —
which is the largest possible `size_t`, 18,446,744,073,709,551,615. That is `>= 0`. So the
condition is true whether the substring was found or not.

```cpp
if (s.find("abc") != std::string::npos) { /* correct */ }
```

Same family as the `.size() - 1` bug from
[day 002's C++ lesson](../day-002-counting-steps/04-cpp-types-numbers.md). Unsigned values do not
go negative; they wrap.

### The one that costs contests: the anti-hash test

This is real, it is deliberate, and it is specific to competitive programming.

GCC's `std::hash<int>` is the identity function — hashing the number 5 gives you 5. The bucket
count is a prime, but it is a *known* prime, from a published list. So anyone can compute a set of
integers that all land in the same bucket, and on Codeforces, where other competitors can read
your submitted source and hack it with a test of their choosing, they do. Your accepted O(n)
solution becomes O(n²) on a test built specifically to make it so.

The fix is to make your hash unpredictable, by mixing in the clock:

```cpp
struct SafeHash {
    static uint64_t splitmix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15ULL;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
        x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
        return x ^ (x >> 31);
    }
    size_t operator()(uint64_t x) const {
        static const uint64_t SEED =
            std::chrono::steady_clock::now().time_since_epoch().count();
        return splitmix64(x + SEED);
    }
};

std::unordered_map<long long, int, SafeHash> safe;
```

The seed differs on every run, so no fixed test can target it. Paste this into your template and
use it for any `unordered_map` with number keys in a contest where hacking is allowed. In an
interview, mentioning that the worst case is O(n) and that adversarial input can trigger it is
worth real credit; you do not need to produce the code.

The simpler alternative, and the honest one: **use `map` when the worst case matters.** O(log n)
with no bad day beats O(1) with one.

---

## 8. In the interview

### How it gets asked

- *"When would you use `std::map` instead of `std::unordered_map`?"* — the direct version, and
  extremely common.
- *"What's the complexity of a hash map lookup?"* — where the wrong answer is "O(1)" full stop
  and the right one has the word "average" in it.
- *"Your solution uses a hash map and it's timing out on one test. Why?"* — the applied version.
- *"How would you count the frequency of every word in a file?"* — the practical one, where they
  watch which container you reach for.

### What to say out loud, in the first ninety seconds

1. **Name the structures.** *"`unordered_map` is a hash table — average O(1) lookup. `map` is a
   balanced binary search tree — O(log n), with the keys always in sorted order."*
2. **Say what the ordering buys.** *"So `map` gives me iteration in sorted order for free, the
   smallest and largest key in O(1), and `lower_bound` — the first key at least as large as x.
   `unordered_map` can do none of those."*
3. **Say what the hash costs.** *"And `unordered_map`'s O(1) is average, not worst case. With
   collisions it degrades to O(n), and `map`'s O(log n) is guaranteed."*
4. **Give the rule.** *"So I default to `unordered_map` for plain key lookup, and switch to `map`
   the moment I need order, a range, or a guaranteed bound."*
5. **Add the numbers.** *"In practice `map` is about three times slower per lookup and uses more
   memory, because the nodes are scattered and every step down the tree is likely a cache miss."*
6. **Offer the third option.** *"And if the data is static, I would often use a sorted vector with
   `std::lower_bound` instead of either — same log n, a tenth of the memory, and contiguous."*

Step 6 is the one that gets remembered. Most candidates present it as a two-way choice.

### The follow-ups

**"Why is hash map lookup only O(1) on average?"**
Because two keys can hash to the same bucket. With a good hash and ordinary data the buckets hold
one or two entries and lookup is constant. But nothing prevents every key landing in one bucket,
and then lookup walks a list of n entries. In practice that happens two ways: a bad hash for the
data at hand, or an adversary choosing the keys. GCC's `std::hash<int>` is the identity function,
so on Codeforces, where competitors can read your source and submit a test, people generate keys
that collide deliberately and turn an O(n) solution into O(n²). The defence is a custom hash
seeded from the clock, so the mapping differs on every run — or using `map`, where the worst case
is the same as the average case.

**"How does the tree stay balanced?"**
`std::map` is a red-black tree in every mainstream implementation. Each node carries one extra bit
of colour, and insertions and deletions repair a set of invariants by rotating subtrees, which
keeps the longest root-to-leaf path within twice the shortest. That bounds the height at O(log n),
so lookup, insert and erase are all O(log n) worst case. The rebalancing is why insertion into a
map is slower than into a vector, and the extra pointers are why a node is about forty-eight bytes
for eight bytes of data.

**"What about `multiset`, and when is it the right answer?"**
`multiset` is a sorted container that allows duplicates. It is the right answer when you need to
repeatedly take the smallest or largest element *and* remove arbitrary elements — a priority queue
can do the first but not the second. The sliding-window-median and skyline problems are the
classic uses. One trap: `ms.erase(value)` erases *every* copy of that value; to erase one, call
`ms.erase(ms.find(value))`. That has caught almost everyone once.

**"How would you count word frequencies in a large file?"**
`unordered_map<string, int>` and `freq[word]++`, which is the whole thing. Two refinements if the
data is large. I would `reserve` the map if I can estimate the distinct count, because rehashing a
growing hash table is a real cost. And if the file is very large I would care that hashing a string
is proportional to its length, so the total is O(total characters) rather than O(number of words) —
which is the right answer anyway, but worth saying so it does not look like I think string hashing
is free. If I then needed the results alphabetically, I would collect into a vector and sort at the
end rather than using a `map` throughout, because paying log n on every insert to get an order I
only need once is the wrong trade.

### A model answer

> "They store the same thing — key-value pairs — and they differ in how they find a key.
>
> `unordered_map` is a hash table. It computes a number from the key and jumps straight to a
> bucket, so lookup, insert and erase are O(1) on average. `map` is a balanced binary search tree,
> a red-black tree in practice, so those operations are O(log n) — but it keeps the keys in sorted
> order at all times.
>
> That ordering is the whole reason to accept the log n. With a `map` I get iteration in sorted
> key order for free, the smallest and largest key in constant time, and `lower_bound` — the first
> key not less than x — which lets me answer range questions like 'every key between 20 and 60'.
> An `unordered_map` cannot answer any of those; its iteration order is arbitrary and its keys
> have no meaningful neighbours.
>
> The other half of the trade is the worst case. `unordered_map`'s O(1) is average. If many keys
> collide into one bucket it degrades to O(n), and that is not hypothetical — GCC's hash for
> integers is the identity function, so on Codeforces people deliberately construct tests that
> collide and hack otherwise-correct solutions. `map` has no bad day: O(log n) is a guarantee.
>
> So my rule is: default to `unordered_map` for plain lookup; switch to `map` when I need order, a
> range, or a guaranteed bound. In a contest with hacking, I use a clock-seeded custom hash so my
> bucket layout cannot be predicted.
>
> One thing I would add: it is not a two-way choice. `map` is about three times slower per lookup
> and roughly ten times the memory of the raw data, because every node is a separate allocation and
> every step down the tree is likely a cache miss. If the data is built once and then only queried,
> I would sort a `vector<pair<K,V>>` and use `std::lower_bound` on it — same log n, contiguous
> memory, far less overhead. And if the keys are small integers or letters, I would use a plain
> array or a 26-slot table and skip hashing entirely, which is about twenty times faster than any
> of them."

That answer names both structures, gives the mechanism, says what each buys and costs, gives a
decision rule, names a real-world failure mode, and offers two options the question did not ask
about.

---

## 9. Recall card

1. **`unordered_map` = hash table, O(1) average. `map` = balanced tree, O(log n), keys always
   sorted.** Default to `unordered_map`; switch when you need order, `lower_bound`, or a
   guaranteed worst case.
2. **`m[key]` on a missing key inserts it.** Use `.count()`, `.contains()` (C++20) or `.find()`
   to read. `.at()` throws instead.
3. **`std::string` is mutable and `+=` is O(1) amortised.** So the loop that is quadratic in
   Python is already correct in C++. `s.find` returns `npos`, never −1.
4. **`freq[x]++` counts anything in one line.** For lowercase letters use `array<int,26>` and
   `c - 'a'` — no hashing, no allocation, about twenty times faster.
5. **`unordered_map`'s worst case is O(n), and in contests it is weaponised.** Seed a custom hash
   from the clock, or use `map`. And there is no standard hash for `pair` — pack two ints into a
   `long long`.

---

**Next in C++:** [day 042 — sort, lambdas, and
lower_bound](../day-042-binary-search-idea/04-cpp-sort-lambdas.md). That is a long way off. Until
then, solve the course's daily problems in C++ with what you now have.
