---
day: 42
track: cpp
title: "sort, lambdas, and lower_bound: the algorithms header"
phase: "C++ and competitive programming"
status: written
---

# Day 042 · C++ — sort, lambdas, and lower_bound: the algorithms header

**After today you can:** You can sort by any key with a lambda, and binary search a sorted range without writing the loop yourself.

**The interviewer asks it as:** *What is the difference between lower_bound and upper_bound?*

---

> Sixth of the twelve C++ days, and the first since day 006. Today's DSA lesson teaches you to write
> binary search by hand, and you should — you will be asked to. This teaches you the library
> version you will actually use once you have proved you can write it.

---

## 1. What this is, and why they ask it

`<algorithm>` is the header that contains the functions you would otherwise write yourself:
sorting, searching, reversing, finding the largest, removing duplicates. They are already
written, already correct, and already faster than what you would produce under time pressure.

Two of them matter more than all the others. `std::sort` sorts anything in O(n log n), and takes
an optional rule saying what "in order" means, which lets you sort by any key you like.
`std::lower_bound` binary searches a sorted range and tells you the position of the first element
**not less than** the value you asked for — which sounds like a strange thing to want until you
realise it answers "where would this go", "does it exist", "how many are there" and "what is the
next one up", all with the same call.

Interviewers ask about `lower_bound` versus `upper_bound` because the pair of them is how you
count duplicates and find ranges, and because getting the boundary right is exactly the off-by-one
skill today's DSA lesson is about. They ask about comparators because writing one with `<=`
instead of `<` is undefined behaviour that crashes, and knowing why marks you out.

---

## 2. The story

The PT teacher at the Kendriya Vidyalaya in Bilaspur has to get sixty children into one line for
the class photograph, and the photographer has already said twice that he has another booking at
eleven.

He does it by height. Shortest at the left. That part everyone understands, and it takes about six
minutes of shuffling, mostly because the children keep swapping places with their friends when he
turns round.

The trouble starts with the ones who are the same height. There are nine pairs of them, near
enough identical, and every time he walks the line they have moved. Two boys spend a full minute
arguing about which of them is taller, which they are not.

So he adds a second rule, out loud, so all sixty of them hear it. Same height, then whoever's name
comes first in the register goes on the left. Now there is nothing to argue about. Every child has
exactly one correct place, and it does not change when he turns his back.

At twenty to eleven, with the line finished and the photographer setting up, a boy called Imran
arrives from the dentist.

The teacher does not walk the line from the left looking for the gap. Sixty children, and he has
about ninety seconds. He goes to the middle of the row, stands Imran next to the boy there, and
looks. Imran is taller. So the whole left half is gone — every child from there leftwards is
shorter, and Imran does not belong among them. He goes halfway along what is left. Shorter this
time. The right quarter is gone.

Four comparisons, and he is standing at the exact place where Imran fits. Not looking at sixty
children. Looking at four.

There is one small thing he decides on the spot. There are already three boys in the row at
exactly Imran's height. Does Imran go in front of all three, or behind them? He puts him in front,
because that keeps the register rule — Imran's name comes before theirs. But he notices that
"where does he go" had two sensible answers, and that he had to pick one.

---

## 3. The idea in plain English

### `std::sort`

```cpp
#include <algorithm>

std::vector<int> v = {5, 3, 8, 1};
std::sort(v.begin(), v.end());          // {1, 3, 5, 8}
```

`v.begin()` and `v.end()` mark the range: the first element, and one past the last. That
half-open convention — `end()` points past the end, not at the last element — is everywhere in
C++, and it is why `end() - begin()` is exactly the size.

`std::sort` is O(n log n) and it is **introsort**: quicksort, which switches to heapsort if the
recursion goes too deep, and to insertion sort for small pieces. That combination gives it
quicksort's speed with a guaranteed O(n log n) worst case, so it does not have the O(n²) bad day
that plain quicksort has. [Day 054](../day-054-quicksort/README.md) covers why that matters.

It is **not stable** — equal elements can come out in any order. `std::stable_sort` is, at the
cost of extra memory and a bit of speed. That is the teacher's second rule: if you need equal
elements to keep their original order, say so.

Sorting the other way:

```cpp
std::sort(v.rbegin(), v.rend());                   // descending, by reversing the range
std::sort(v.begin(), v.end(), std::greater<int>()); // descending, by saying so
```

### A lambda is a function you write where you need it

To sort by anything other than `<`, you hand `sort` a rule. That rule is usually a **lambda** — a
small unnamed function written inline.

```cpp
std::sort(v.begin(), v.end(), [](int a, int b) {
    return a > b;                    // "a comes before b" -> descending
});
```

The `[]` is the **capture list**, the `(int a, int b)` is the parameters, the body returns
`true` when `a` should come before `b`.

The capture list says which surrounding variables the lambda can see:

```cpp
[]          sees nothing outside itself
[&]         sees everything, by reference (can modify it)
[=]         sees everything, by copy
[&weights]  sees just weights, by reference
[n]         sees just n, by copy
```

For a comparator, `[]` is almost always right. When you need outside data — sorting positions by
the values they point at, which is a very common trick — use `[&]`:

```cpp
std::vector<int> value = {50, 10, 40};
std::vector<int> order = {0, 1, 2};
std::sort(order.begin(), order.end(), [&](int i, int j) {
    return value[i] < value[j];      // sort the POSITIONS by their value
});
// order is now {1, 2, 0}
```

### The comparator must be a strict weak ordering

This is the rule that catches people, and breaking it is not a wrong answer — it is a crash.

Your comparator must return `true` only when `a` comes **strictly** before `b`. In particular
`cmp(a, a)` must be `false`. Use `<`, never `<=`.

```cpp
[](int a, int b) { return a <= b; }    // WRONG. Undefined behaviour.
[](int a, int b) { return a <  b; }    // right
```

Why it crashes rather than merely mis-sorting: `sort` uses the comparator to decide when to stop
scanning, and with `<=` two equal elements each compare "before" the other, so the scan never
stops and runs off the end of the array. Section 7 has the real output.

### Sorting by several keys

The teacher's two rules. Two ways, and the second is better:

```cpp
// by height, then by name
std::sort(kids.begin(), kids.end(), [](const Kid& a, const Kid& b) {
    if (a.height != b.height) return a.height < b.height;
    return a.name < b.name;
});

// the same thing, using tie — harder to get wrong
std::sort(kids.begin(), kids.end(), [](const Kid& a, const Kid& b) {
    return std::tie(a.height, a.name) < std::tie(b.height, b.name);
});
```

`std::tie` makes a tuple of references, and tuples compare lexicographically — first field, then
second, and so on. With four keys the first form is a nest of `if`s you will get wrong; the second
stays one line. To reverse one key only, negate it: `std::tie(-a.height, a.name)`.

And a `pair` already does this for free, which is why sorting `vector<pair<int,string>>` sorts by
the number and breaks ties by the word without you writing anything.

### `lower_bound` and `upper_bound`

Both binary search a **sorted** range in O(log n). The difference is what they do about equal
elements — Imran's question.

> **`lower_bound(x)` — the first position where `x` could be inserted, keeping order. The first
> element `>= x`.**
> **`upper_bound(x)` — the last position where `x` could be inserted. The first element `> x`.**

On a range with no duplicates of `x` they give the same answer. On a range with three copies of
`x`, `lower_bound` points at the first one and `upper_bound` points just past the third.

That gives you everything:

```cpp
std::vector<int> v = {10, 20, 20, 20, 30};      // must be sorted

auto lo = std::lower_bound(v.begin(), v.end(), 20);   // -> index 1
auto hi = std::upper_bound(v.begin(), v.end(), 20);   // -> index 4

int  first_at_least_20 = lo - v.begin();              // 1
int  how_many_20s      = hi - lo;                     // 3
bool has_20            = (lo != v.end() && *lo == 20); // true
int  next_above_20     = (hi != v.end() ? *hi : -1);   // 30
```

Subtracting two positions gives the count between them. That is the whole technique, and it is
how you answer "how many values are between 20 and 60" in O(log n) instead of O(n).

`std::binary_search(v.begin(), v.end(), 20)` returns just `true` or `false`. It is less useful
than `lower_bound`, because it tells you nothing about where.

**They only work on sorted data**, and they give no warning if it is not sorted — you get a wrong
answer, quietly.

### The rest of the header, in one table

The ones you will actually reach for:

| Call | Does | Cost |
|---|---|---|
| `sort(b, e)` | sorts | O(n log n) |
| `stable_sort(b, e)` | sorts, keeping equal elements' order | O(n log n) |
| `reverse(b, e)` | reverses in place | O(n) |
| `max_element(b, e)` | position of the largest | O(n) |
| `min_element(b, e)` | position of the smallest | O(n) |
| `accumulate(b, e, 0LL)` | sums — note the `0LL` | O(n) |
| `count(b, e, x)` | how many equal `x` | O(n) |
| `find(b, e, x)` | position of the first `x`, or `e` | O(n) |
| `unique(b, e)` | collapses adjacent duplicates | O(n) |
| `next_permutation(b, e)` | next ordering, `false` when it wraps | O(n) |
| `nth_element(b, b+k, e)` | puts the k-th smallest in place | **O(n)** average |
| `partial_sort(b, b+k, e)` | sorts only the first k | O(n log k) |
| `__gcd(a, b)` | greatest common divisor | O(log n) |

`accumulate(v.begin(), v.end(), 0)` with a plain `0` sums into an `int` and overflows — the
initial value decides the type. Write `0LL`. This is the day-002 bug wearing a different hat.

`nth_element` is O(n) average and finds the k-th smallest without sorting, which is quickselect
from [day 055](../day-055-quickselect/README.md) already written for you.

---

## 4. The picture

The two bounds on a range with duplicates. This diagram is the whole lesson:

```
  value    10   20   20   20   30   40
  index     0    1    2    3    4    5
          +----+----+----+----+----+----+
          | 10 | 20 | 20 | 20 | 30 | 40 |
          +----+----+----+----+----+----+
                ^                   ^
                |                   |
       lower_bound(20) = 1     upper_bound(30) = 5
       first element >= 20     first element > 30

                     upper_bound(20) = 4
                     first element > 20
                                ^
                                |
          +----+----+----+----+----+----+
          | 10 | 20 | 20 | 20 | 30 | 40 |
          +----+----+----+----+----+----+
                \______________/
                  count = upper - lower = 4 - 1 = 3


  a value that is not there:  lower_bound(25) = upper_bound(25) = 4
                                                            ^
          +----+----+----+----+----+----+                   |
          | 10 | 20 | 20 | 20 | 30 | 40 |    both point here — where 25
          +----+----+----+----+----+----+    would go if inserted
```

**What to notice:** when the value is absent, both functions agree, and their answer is the
insertion point. When the value is present, they straddle the block of copies. Everything you can
ask about a sorted range comes from those two positions and the distance between them.

And the search itself, which is today's DSA lesson drawn as the teacher's ninety seconds:

```
  looking for 30 in a sorted row of 6

  step 1     10   20   20   20   30   40        mid = index 2, value 20
             ^-------------------------^        20 < 30, so the answer is to the RIGHT
                          |
  step 2                  20   30   40          mid = index 4, value 30
                          ^---------^           30 is not < 30, so go LEFT, keep 4
                               |
  step 3                       30               one element left
                               ^
                          answer: index 4

  6 elements, 3 comparisons.  1000 elements, 10 comparisons.
```

**What to notice:** every step throws away half of what is left. That is why the count is
log2(n) and why doubling the data adds exactly one comparison.

---

## 5. The code, built step by step

### Sorting a struct by two keys

```cpp
struct Kid {
    std::string name;
    int height;
};

std::vector<Kid> kids = {{"imran", 140}, {"asha", 138}, {"bala", 140}};

std::sort(kids.begin(), kids.end(), [](const Kid& a, const Kid& b) {
    return std::tie(a.height, a.name) < std::tie(b.height, b.name);
});
// asha(138), bala(140), imran(140)
```

`const Kid&` in the parameters, not `Kid` — a comparator is called O(n log n) times, so copying
the object each time is a real cost. This is [day 005's rule](../day-005-python-lists-and-tuples/04-cpp-vector-references.md)
in the place where it matters most.

### Sorting positions instead of values

The trick you will use over and over when you must not lose the original order:

```cpp
std::vector<int> score = {50, 90, 70};
std::vector<int> rank(score.size());
std::iota(rank.begin(), rank.end(), 0);       // fills with 0, 1, 2

std::sort(rank.begin(), rank.end(), [&](int i, int j) {
    return score[i] > score[j];               // highest score first
});
// rank == {1, 2, 0} — the winner was originally at position 1
```

`std::iota` from `<numeric>` fills a range with consecutive values. The `[&]` capture is what lets
the comparator see `score`.

### Counting occurrences in O(log n)

```cpp
std::vector<int> v = {10, 20, 20, 20, 30};
auto lo = std::lower_bound(v.begin(), v.end(), 20);
auto hi = std::upper_bound(v.begin(), v.end(), 20);
int how_many = hi - lo;                       // 3
```

Compare that with `std::count(v.begin(), v.end(), 20)`, which is O(n). On a sorted range, the
bounds version is O(log n), and on 10^6 elements that is twenty comparisons against a million.

### Values in a range, which is the real use

```cpp
// how many values are in [lo_val, hi_val], inclusive?
int in_range(const std::vector<int>& v, int lo_val, int hi_val) {
    auto a = std::lower_bound(v.begin(), v.end(), lo_val);       // first >= lo_val
    auto b = std::upper_bound(v.begin(), v.end(), hi_val);       // first  > hi_val
    return b - a;
}
```

Six lines, O(log n) per question, and it is the answer to a whole family of problems. Note the
asymmetry — `lower_bound` for the low end and `upper_bound` for the high end — which is exactly
what makes the range inclusive on both sides. Getting that pair the right way round is the skill.

### `lower_bound` on a `set` is a member function

```cpp
std::set<int> s = {10, 20, 30};

auto it = s.lower_bound(20);        // CORRECT: O(log n)
auto bad = std::lower_bound(s.begin(), s.end(), 20);   // compiles. O(n). Do not.
```

The free function needs to jump to the middle of a range, and a tree's iterators can only step
one node at a time — so it degrades to a linear walk. The member function walks the tree properly.
**Same for `map`.** This is a silent performance bug and the compiler will not warn you.

### The complete program

```cpp
// sorting.cpp — sort, lambdas, and the two bounds.
//   g++ -std=c++20 -O2 -Wall -Wextra -o sorting sorting.cpp && ./sorting

#include <bits/stdc++.h>
using namespace std;

struct Kid {
    string name;
    int height;
};

// How many values lie in [lo_val, hi_val]. The range must be sorted.
int in_range(const vector<int>& v, int lo_val, int hi_val) {
    auto a = lower_bound(v.begin(), v.end(), lo_val);   // first >= lo_val
    auto b = upper_bound(v.begin(), v.end(), hi_val);   // first  > hi_val
    return (int)(b - a);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // ---- sort with two keys ----
    vector<Kid> kids = {{"imran", 140}, {"asha", 138}, {"bala", 140}, {"chandra", 135}};
    sort(kids.begin(), kids.end(), [](const Kid& a, const Kid& b) {
        return tie(a.height, a.name) < tie(b.height, b.name);   // '<', never '<='
    });
    cout << "the line:";
    for (const auto& k : kids) cout << " " << k.name << "(" << k.height << ")";
    cout << "\n";

    // ---- sort positions, not values ----
    vector<int> score = {50, 90, 70};
    vector<int> rank(score.size());
    iota(rank.begin(), rank.end(), 0);
    sort(rank.begin(), rank.end(), [&](int i, int j) { return score[i] > score[j]; });
    cout << "ranking by position:";
    for (int i : rank) cout << " " << i;
    cout << "\n";

    // ---- the two bounds ----
    vector<int> v = {10, 20, 20, 20, 30, 40};
    auto lo = lower_bound(v.begin(), v.end(), 20);
    auto hi = upper_bound(v.begin(), v.end(), 20);
    cout << "lower_bound(20) = index " << lo - v.begin() << "\n";
    cout << "upper_bound(20) = index " << hi - v.begin() << "\n";
    cout << "count of 20     = " << hi - lo << "\n";
    cout << "lower_bound(25) = index " << lower_bound(v.begin(), v.end(), 25) - v.begin()
         << "   (where 25 would go)\n";
    cout << "values in [20,30] = " << in_range(v, 20, 30) << "\n";

    // ---- does it exist? ----
    auto it = lower_bound(v.begin(), v.end(), 25);
    cout << "25 present? " << ((it != v.end() && *it == 25) ? "yes" : "no") << "\n";

    // ---- the rest of the header ----
    cout << "largest      " << *max_element(v.begin(), v.end()) << "\n";
    cout << "sum          " << accumulate(v.begin(), v.end(), 0LL) << "\n";  // 0LL, not 0
    reverse(v.begin(), v.end());
    cout << "reversed     "; for (int x : v) cout << x << " "; cout << "\n";

    // ---- k-th smallest without sorting ----
    vector<int> w = {7, 2, 9, 4, 1, 8};
    nth_element(w.begin(), w.begin() + 2, w.end());       // 3rd smallest into position 2
    cout << "3rd smallest = " << w[2] << "\n";

    // ---- every ordering, for the n <= 8 problems ----
    vector<int> p = {1, 2, 3};
    cout << "permutations:";
    do {
        cout << " ";
        for (int x : p) cout << x;
    } while (next_permutation(p.begin(), p.end()));
    cout << "\n";

    return 0;
}
```

Expected output:

```
the line: chandra(135) asha(138) bala(140) imran(140)
ranking by position: 1 2 0
lower_bound(20) = index 1
upper_bound(20) = index 4
count of 20     = 3
lower_bound(25) = index 4   (where 25 would go)
values in [20,30] = 4
25 present? no
largest      40
sum          140
reversed     40 30 20 20 20 10
3rd smallest = 4
permutations: 123 132 213 231 312 321
```

Note the line order: `bala` before `imran` at the same height, because the name broke the tie
exactly as the teacher's second rule did. And `next_permutation` only produces the orderings from
the current one onwards, which is why the vector has to start sorted.

---

## 6. What it costs

### Sorting

```
  std::sort is O(n log n).  With C++ at ~10^8 simple operations per second:

  n = 10^5:   10^5 x 17   = 1.7 x 10^6 comparisons   ->  ~0.01 s
  n = 10^6:   10^6 x 20   = 2.0 x 10^7 comparisons   ->  ~0.10 s
  n = 10^7:   10^7 x 23   = 2.3 x 10^8 comparisons   ->  ~1.2 s   (tight)
```

**Sorting 10^6 integers costs about a tenth of a second.** Memorise that one figure; it settles
most "can I afford to sort" questions instantly.

The constant factor is not fixed, though, and this is where a comparator bites:

```
  sort(v) on 10^6 ints, built-in <              ~0.09 s
  sort(v) on 10^6 ints, lambda comparator       ~0.11 s     (inlined, nearly free)
  sort(v) on 10^6 strings                       ~0.60 s     (comparisons touch memory)
  sort(v) of structs taken BY VALUE in the cmp  ~0.35 s     (a copy per comparison)
```

Row four is the mistake. `[](Kid a, Kid b)` instead of `[](const Kid& a, const Kid& b)` copies two
objects on each of 2 × 10^7 comparisons. Same output, four times the time.

### The bounds

```
  lower_bound on 10^6 sorted elements = log2(10^6) = 20 comparisons

  10^6 queries x 20 comparisons = 2 x 10^7   ->  ~0.05 s
  the same 10^6 queries with a linear scan   =  10^12  ->  ~3 hours
```

That is the difference today's DSA lesson is about, with the library doing the writing.

One honest caveat: a binary search on a large array is **cache-hostile**. Each step jumps to a
distant position, so nearly every comparison is a cache miss at roughly 100 nanoseconds. So 20
steps is closer to 2 microseconds than the instruction count suggests. It is still
overwhelmingly better than O(n); it is just not twenty nanoseconds.

### `nth_element` versus `sort`

```
  finding the 100th largest of 10^6 values

  sort then index          10^6 x 20  = 2 x 10^7   ->  ~0.10 s
  nth_element              ~2n        = 2 x 10^6   ->  ~0.01 s
  partial_sort (k = 100)   n log k    = 6.6 x 10^6 ->  ~0.03 s
```

Ten times faster, for one call. Whenever a problem says "the k-th largest" and does not need the
rest sorted, `nth_element` is the answer.

---

## 7. The traps

### The real error: `<=` in a comparator

```cpp
std::sort(v.begin(), v.end(), [](int a, int b) { return a <= b; });
```

It looks harmless and more permissive. It is undefined behaviour, and on a vector with enough
duplicates it crashes:

```
Segmentation fault (core dumped)
```

Compile with libstdc++'s debug mode and you get the diagnosis instead of the crash:

```
g++ -std=c++20 -D_GLIBCXX_DEBUG -g -o prog prog.cpp
```

```
/usr/include/c++/13/bits/stl_algo.h:4861:
In function:
    void std::sort(_RAIter, _RAIter, _Compare)

Error: comparison doesn't meet irreflexive requirements, assert(!(a < a)).

Objects involved in the operation:
    instance "functor" @ 0x7ffd3c1a2b40 {
      type = main::{lambda(int, int)#1};
    }
```

"Irreflexive" means `cmp(a, a)` must be false. With `<=` it is true, and `sort`'s inner scan uses
the comparator as its stopping condition — so with two equal elements each "less than" the other,
the scan walks off the end of the array and into memory that is not yours.

**Comparators use `<`. Always. If you want descending, use `>`, not `>=`.**

### The near-miss: `lower_bound` on unsorted data

```cpp
std::vector<int> v = {5, 3, 8, 1};             // not sorted
auto it = std::lower_bound(v.begin(), v.end(), 3);   // meaningless answer
```

No error, no warning, no crash. Binary search assumes the range is partitioned and returns
whatever the halving happens to land on. It is a wrong answer that will pass your two-element test
and fail on the judge.

**Sort first, or use a container that is always sorted.** And when you sort with a custom
comparator, `lower_bound` needs *the same* comparator passed to it, or it is searching by a
different rule than the data was ordered by.

### The near-miss: `std::lower_bound` on a `set` or `map`

```cpp
std::set<int> s = { /* 10^6 values */ };
auto it = std::lower_bound(s.begin(), s.end(), x);   // compiles. O(n).
auto ok = s.lower_bound(x);                          // O(log n). Use this.
```

The free function needs to jump to the middle of the range in one step. A tree's iterator can only
move to the next node, so the "jump" becomes a walk and the whole thing degrades to linear. It
compiles, it returns the right answer, and it is a thousand times slower than it should be.

**Rule: if the container has a member function with that name, use the member function.** `set`,
`map`, `multiset` and `multimap` all have `find`, `count`, `lower_bound` and `upper_bound` as
members, and every one of them beats the free version.

### The near-miss: `accumulate` with the wrong initial value

```cpp
std::vector<int> v(100000, 100000);
auto sum = std::accumulate(v.begin(), v.end(), 0);     // int. Overflows. 1410065408.
auto ok  = std::accumulate(v.begin(), v.end(), 0LL);   // long long. 10000000000.
```

The **initial value decides the accumulator type**, not the element type and not what you assign
it to. `0` is an `int`. This is exactly the day-002 overflow with a library function in front of
it, and it is invisible because the line looks like it says nothing about types.

### The quiet one: a lambda that captures a reference that dies

```cpp
auto make_comparator() {
    std::vector<int> weights = {3, 1, 2};
    return [&](int a, int b) { return weights[a] < weights[b]; };   // weights dies here
}
```

The lambda holds a reference to a local vector that is destroyed when the function returns. Calling
it later reads freed memory. `-Wall` does not catch this one — `-fsanitize=address` does:

```
==21077==ERROR: AddressSanitizer: stack-use-after-return on address 0x7f83a1c00030
READ of size 8 at 0x7f83a1c00030 thread T0
```

**Inside a single statement — a `sort` call on the next line — `[&]` is safe and correct. If the
lambda outlives the scope, capture by value.**

---

## 8. In the interview

### How it gets asked

- *"What's the difference between `lower_bound` and `upper_bound`?"* — the direct version, and one
  of the most common C++ questions there is.
- *"Count how many times x appears in this sorted array, faster than O(n)."* — the applied
  version, where the answer is the two bounds and a subtraction.
- *"Sort these records by score descending, then name ascending."* — a live coding step, watching
  whether you write the comparator cleanly and with `const&`.
- *"Is `std::sort` stable? What is it actually implemented as?"* — the depth check.

### What to say out loud, in the first ninety seconds

1. **Define them together.** *"Both binary search a sorted range in O(log n). `lower_bound(x)`
   returns the first element not less than x; `upper_bound(x)` returns the first element strictly
   greater than x."*
2. **Say what happens with duplicates.** *"If x is absent they return the same position — the
   place x would be inserted. If x is present several times, `lower_bound` points at the first
   copy and `upper_bound` just past the last."*
3. **Name the technique.** *"So `upper_bound - lower_bound` is the number of copies of x, in
   O(log n) instead of the O(n) a `count` would take."*
4. **Give the range version.** *"And for a range, `lower_bound(lo)` to `upper_bound(hi)` gives me
   everything in `[lo, hi]` inclusive — that asymmetry is what makes both ends inclusive."*
5. **Name the precondition.** *"Both require the range to be sorted, and they give a wrong answer
   silently if it is not. If I sorted with a custom comparator, I have to pass the same one."*
6. **Add the container gotcha.** *"And on a `set` or `map` I use the member `lower_bound`, not
   `std::lower_bound` — the free one degrades to O(n) on a tree because the iterators cannot jump."*

Step 6 is worth real credit. It is a genuine bug that ships, and very few candidates raise it.

### The follow-ups

**"Is `std::sort` stable?"**
No. Equal elements can come out in any order. `std::stable_sort` is stable, and costs extra memory
— it is a merge sort that uses O(n) extra space when it can get it, and degrades to an in-place
merge that is O(n log² n) when it cannot. In practice I avoid needing stability by making the
comparator total: adding the original position as the last tie-break gives a deterministic order
and lets me keep the faster `sort`.

**"What is `std::sort` actually implemented as?"**
Introsort. It starts as quicksort with a median-of-three pivot, counts its recursion depth, and
switches to heapsort if it goes past about 2 log n — which is what removes quicksort's O(n²) worst
case. Below a threshold of around sixteen elements it stops recursing and finishes the whole array
with one insertion-sort pass, because insertion sort wins on small nearly-sorted data. So it is
three algorithms, and the guarantee is O(n log n) worst case with quicksort's constant factor most
of the time.

**"Why must the comparator be a strict weak ordering, and what happens if it is not?"**
Because `sort`'s partitioning loop uses the comparator itself as the bound on its scan — it walks
inward while `cmp(*i, pivot)` holds. That is only safe if no element compares less than itself. If
I write `<=`, then for two equal elements each compares "before" the other, the scan never
terminates at the pivot, and it runs off the end of the array. The result is a segmentation fault
or silent memory corruption, not a mis-sorted array. Compiling with `-D_GLIBCXX_DEBUG` turns it
into a clear message: "comparison doesn't meet irreflexive requirements".

**"When would you not sort, even though sorting would work?"**
When I only need part of the order. `nth_element` puts the k-th smallest in place in O(n) average,
and `partial_sort` sorts just the first k in O(n log k) — both beat a full sort for "top k" or
"the median". When the values are small bounded integers, counting sort is O(n) and beats O(n log
n) outright. When I need a running order as data arrives, a heap or a `multiset` maintains it
incrementally rather than re-sorting. And when the data is already nearly sorted, `stable_sort` on
almost-ordered input, or an insertion sort, can beat `sort` — though I would measure before
claiming it.

### A model answer

The interviewer asks for the count of a value in a sorted array, faster than linear.

> "I'd use the two bounds and subtract.
>
> `std::lower_bound` gives me an iterator to the first element not less than x, and
> `std::upper_bound` gives me the first element strictly greater than x. Both binary search, so
> both are O(log n) on a random-access range. If x appears three times, `lower_bound` points at
> the first of the three and `upper_bound` points one past the last — so the distance between them
> is exactly the count.
>
> ```cpp
> auto lo = std::lower_bound(v.begin(), v.end(), x);
> auto hi = std::upper_bound(v.begin(), v.end(), x);
> int count = hi - lo;
> ```
>
> That is O(log n) against `std::count`'s O(n). On a million elements it is about forty
> comparisons instead of a million.
>
> Two things I'd check before committing to it. The range has to be sorted — binary search gives a
> wrong answer silently on unsorted data, no error. And if it was sorted with a custom comparator,
> I have to pass the same comparator to both bounds, or I am searching by a different rule than
> the data is ordered by.
>
> The same pair generalises, which is really why I like it. `lower_bound(lo)` to `upper_bound(hi)`
> gives me every element in the closed range `[lo, hi]`, and the asymmetry between which function
> I use at which end is exactly what makes both ends inclusive. That answers 'how many values are
> between 20 and 60' in log n too.
>
> One caveat if this is on a `std::set` rather than a vector: I would call the member
> `s.lower_bound(x)`, not `std::lower_bound(s.begin(), s.end(), x)`. The free function needs to
> jump to the middle of the range, and a tree iterator can only step one node at a time, so it
> quietly degrades to O(n). It compiles and returns the right answer, which is what makes it
> dangerous."

That answer gives the technique, the code, the complexity with a concrete number, two
preconditions, a generalisation, and a real performance trap.

---

## 9. Recall card

1. **`lower_bound(x)` = first element ≥ x. `upper_bound(x)` = first element > x.** Both O(log n),
   both need sorted data, and both fail silently if it is not sorted.
2. **`upper_bound - lower_bound` = the count of x.** `lower_bound(lo)` to `upper_bound(hi)` = every
   element in `[lo, hi]` inclusive.
3. **Comparators use `<`, never `<=`.** `<=` is undefined behaviour and segfaults. Take arguments
   by `const&`, and use `std::tie` for multiple keys.
4. **`std::sort` is introsort: O(n log n) guaranteed, and not stable.** Sorting 10^6 ints costs
   about 0.1 s — the figure that settles "can I afford to sort".
5. **On a `set` or `map`, use the member `lower_bound`, not the free one** — the free one is O(n)
   on a tree. And `accumulate` needs `0LL`, or it sums into an `int` and overflows.

---

**Next in C++:** [day 068 — stack, queue, deque, and
priority_queue](../day-068-stacks/04-cpp-stack-queue-deque.md).
