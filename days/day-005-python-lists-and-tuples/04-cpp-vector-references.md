---
day: 5
track: cpp
title: "vector, references, and the array you use for everything"
phase: "C++ and competitive programming"
status: written
---

# Day 005 · C++ — vector, references, and the array you use for everything

**After today you can:** You can use vector for every array problem in the course, and pass one to a function without copying four megabytes by accident.

**The interviewer asks it as:** *What is the difference between passing by value, by reference, and by pointer?*

---

> Fourth of the ten C++ days, and the twin of today's DSA lesson. You have just learned what a
> Python list costs. `std::vector` is the same structure with the same costs — and one extra
> question Python never asks you: who is holding the original, and who is holding a copy.

---

## 1. What this is, and why they ask it

`std::vector` is C++'s dynamic array. It is one continuous run of slots in memory that grows
when you push onto the end, exactly like the Python list you met today. Indexing is O(1),
`push_back` is O(1) amortised, inserting at the front is O(n). Every cost you learned this
morning transfers over unchanged.

What does not transfer is what happens when you hand one to a function. In Python, passing a
list passes the list — there is one list, and a change inside the function is visible outside.
In C++, passing a `vector` **copies it**. Every element. Every time. A `vector<int>` with a
million elements is four megabytes, and C++ will silently duplicate all four of them on every
call.

One character stops that. The ampersand, `&`, makes the parameter a **reference**: another name
for the caller's object rather than a copy of it.

Interviewers ask about this constantly, because the answer tells them whether you think about
memory at all. It is also the source of two entirely separate categories of bug that beginners
hit in their first week: functions that mysteriously do nothing, and functions that are
inexplicably slow.

---

## 2. The story

Meera goes to her sister in Hyderabad for eleven days in the middle of May. The flat in Kondhwa
is on the fourth floor and faces west, and the balcony has thirty-one plants on it, which she
has counted, because two of them are curry leaf plants her mother started from a cutting in 2016
and she is not casual about them.

Farid is next door. He has watered them before, in October, when it did not matter as much.

The night before she leaves she goes over the whole balcony with him on a video call from the
balcony itself, walking the phone slowly along the shelves. This one every day. This one every
third day, and less if it rains. The tulsi gets the morning sun so it drinks more. The big rubber
plant at the end has been dropping leaves and she thinks it needs repotting, and there is a bag
of soil under the sink.

Farid takes photographs as she talks. Thirty-one photographs, one per plant, so he will remember
which is which.

On the fourth day he is looking at the photographs on his phone over lunch, and it occurs to him
with a slight lurch that he has been doing this for four days and has not yet been into the
flat. He has the photos. He has looked at the rubber plant a dozen times. He knows exactly which
one needs repotting.

The photographs cannot be watered.

He has the spare key. It has been in the bowl by his door since Tuesday. He goes across after
lunch, unlocks the flat, and does the round properly — and now everything he does is to the
plants, not to pictures of them. He waters. He moves the tulsi eight inches left, out of the
afternoon glare. He repots the rubber plant.

He does not touch the two curry leaf plants beyond watering, because she had said, twice, in a
particular voice, not to move those.

Two kinds of access to the same thirty-one plants. One that took twenty minutes to make and
could change nothing. One that took no time to make, changed everything he touched, and came
with one thing he had promised not to do.

---

## 3. The idea in plain English

### `vector` is the Python list, with the same costs

Everything today's DSA lesson told you about a Python list is true of a `std::vector`. One
continuous block. Position `i` found by arithmetic. Cheap at the end, expensive at the front.

```cpp
#include <vector>

std::vector<int> v;          // empty
v.push_back(12);             // O(1) amortised   — Python's append
v.push_back(45);
int x = v[0];                // O(1)             — Python's v[0]
int n = v.size();            // O(1)             — Python's len(v)
v.pop_back();                // O(1)             — Python's pop()
```

The `<int>` in angle brackets is the element type, and it is fixed. A `vector<int>` holds `int`s
and nothing else. This is the first real difference from Python, where a list holds anything: C++
knows the element type when you compile, which is exactly why `v[i]` is a multiply-and-offset
with no lookup and no unwrapping.

The four ways to make one, all of which you will use:

```cpp
std::vector<int> a;                    // empty
std::vector<int> b(10);                // 10 elements, all 0
std::vector<int> c(10, -1);            // 10 elements, all -1
std::vector<int> d = {3, 1, 4, 1, 5};  // exactly these five
```

`vector<int> b(10)` **zero-fills**. That is worth knowing, because it means you can allocate a
counting table and start counting without initialising it yourself.

And the same asymmetry you learned this morning:

| Operation | Cost | Python equivalent |
|---|---|---|
| `v.push_back(x)` | O(1) amortised | `v.append(x)` |
| `v.pop_back()` | O(1) | `v.pop()` |
| `v[i]` | O(1) | `v[i]` |
| `v.size()`, `v.empty()` | O(1) | `len(v)` |
| `v.insert(v.begin(), x)` | **O(n)** | `v.insert(0, x)` |
| `v.erase(v.begin())` | **O(n)** | `v.pop(0)` |
| `v.back()`, `v.front()` | O(1) | `v[-1]`, `v[0]` |
| `v.clear()` | O(n) | `v.clear()` |

**The end is cheap, the front is expensive.** Same sentence, same reason: contiguity.

### Capacity, and why `push_back` is amortised

A `vector` keeps two numbers: its **size** — how many elements it holds — and its **capacity** —
how many it has room for. When `push_back` runs out of capacity, it allocates a bigger block,
copies everything across, and frees the old one. GCC's implementation doubles the capacity, so
the copies get rarer and rarer, and averaged over many pushes the cost per push is constant.
That is the same "amortised" you met this morning, with a growth factor of 2 rather than
Python's 1.125.

If you know how many elements are coming, say so:

```cpp
std::vector<int> v;
v.reserve(1000000);      // one allocation, then a million free push_backs
```

`reserve` sets the capacity without changing the size. On a million pushes it is worth a
measurable fraction of a second, because it removes about twenty reallocations and the copying
that goes with them.

### 2D vectors

The grid problems from [day 016](../day-016-2d-arrays/README.md) onwards need this shape:

```cpp
std::vector<std::vector<int>> grid(rows, std::vector<int>(cols, 0));
```

Read it inside out: `vector<int>(cols, 0)` is one row of `cols` zeros, and the outer one makes
`rows` copies of it. Then `grid[r][c]` is the cell.

Note that it makes genuine copies, so this does **not** have the `[[0]*3]*3` bug that today's
Python lesson warns about — each row is its own block. C++ is more verbose here and less
surprising.

### The three ways to hand a vector to a function

Farid's two options, plus the promise, are exactly C++'s three.

**By value** — the photographs. The function gets a copy. Changes to the copy do not affect the
original. Making the copy costs time proportional to the size.

```cpp
void f(std::vector<int> v);        // v is a COPY of the caller's vector
```

**By reference** — the key. The function gets another name for the caller's actual object. No
copy. Changes are visible outside.

```cpp
void f(std::vector<int>& v);       // v IS the caller's vector, under a second name
```

**By const reference** — the key, plus the promise about the curry leaf plants. No copy, and the
compiler refuses to compile any line inside the function that would modify it.

```cpp
void f(const std::vector<int>& v); // no copy, and modification is a compile error
```

**`const` is a promise checked when you compile, and enforced.** It is not a convention or a
comment. Try to assign through a `const` reference and the program does not build.

### The rule you will use for the rest of your life

> **Read only, and not tiny? `const T&`.**
> **Must modify? `T&`.**
> **Tiny and read-only — `int`, `double`, `char`, `bool`? Plain value.**

"Tiny" means it fits in a machine register — up to eight bytes or so. Copying an `int` is one
instruction and taking a reference to it costs the same, so a reference buys nothing and reads
worse. Copying a `vector`, a `string`, or a map is a real allocation and a real block copy, and
the reference buys everything.

That is the whole rule, and applying it mechanically will make your C++ both faster and more
correct than most beginners'.

### A reference is a second name, not a thing

```cpp
int score = 40;
int& alias = score;     // alias is another name for score
alias = 55;
// score is now 55
```

`alias` is not a variable that points at `score`. It **is** `score`, with a second label. There
is one number in memory and two names for it. Three consequences:

- A reference must be given something to refer to when it is created. `int& r;` does not compile.
- A reference can never be moved to name something else. `alias = other;` assigns *to score*.
- A reference cannot be null. There is no such thing as a reference to nothing.

[Day 078's C++ lesson](../day-078-nodes-and-links/README.md) covers pointers, which can do all
three of those things, and says when you want that.

### The loop, and the same trap again

```cpp
for (int x : v) { ... }          // "for each x in v" — Python's for x in v
```

In `for (int x : v)`, `x` is a **copy** of each element. For `int` that is free and correct. For
`std::string` it copies the whole string on every iteration.

```cpp
for (const auto& x : v)   // read-only, no copy    <- your default
for (auto& x : v)         // modify the elements in place
for (auto x : v)          // deliberate copy       <- say why
```

`auto` asks the compiler to work the type out from context. **`const auto&` is the default you
should type without thinking.** Reach for the other two only when you have a reason.

---

## 4. The picture

A `vector` in memory, with capacity drawn in — the same diagram as today's DSA lesson, because
it is the same structure:

```
  the vector object itself (24 bytes, on the stack)
  +----------+----------+----------+
  |  begin   |   end    | capacity |      three addresses
  +----------+----------+----------+
       |          |           |
       v          v           v
  +------+------+------+------+------+------+------+------+
  |  12  |  45  |   7  |  99  |  23  |      |      |      |   the heap block
  +------+------+------+------+------+------+------+------+
   index    0      1      2      3      4      5      6      7

  size = 5, capacity = 8

  push_back(31)  ->  goes straight into slot 5.  Nothing moves.  O(1)
```

**What to notice:** the `vector` variable is three addresses and nothing more. The elements live
somewhere else entirely, on the heap. That is why the next picture matters so much.

Now what a call does. First by value:

```
  caller:                         function f(vector<int> v):

  +---------------------+         +---------------------+
  | 1,000,000 ints      |         | 1,000,000 ints      |
  |         4 MB        | ---->   |         4 MB        |
  +---------------------+  COPY   +---------------------+
       the original                   a second 4 MB block,
                                      allocated and filled
                                      on every single call

  f writes v[0] = 99  ->  the copy changes.  The original does not.
```

Now by reference:

```
  caller:                         function f(vector<int>& v):

  +---------------------+
  | 1,000,000 ints      | <------  v
  |         4 MB        |          (a second name for the same object;
  +---------------------+           in practice, one 8-byte address)

  f writes v[0] = 99  ->  the original changes.  There is only one object.
```

**What to notice:** the by-value picture has two blocks and the by-reference picture has one.
Every difference — the speed, and whether changes are visible — comes from that.

And `const` on top:

```
  function f(const vector<int>& v):

  +---------------------+
  | 1,000,000 ints      | <------  v      reading v[0]: allowed
  +---------------------+                 v[0] = 99:      COMPILE ERROR
                                          v.push_back(1): COMPILE ERROR
```

**What to notice:** `const` adds no cost whatsoever while the program runs. The check happens
entirely in the compiler. It is a promise checked before your program exists, which makes it
free.

---

## 5. The code, built step by step

### The three parameter kinds, side by side

```cpp
void by_value(std::vector<int> v)        { v[0] = 99; }
void by_reference(std::vector<int>& v)   { v[0] = 99; }
void by_const_ref(const std::vector<int>& v) {
    // v[0] = 99;   // would not compile
    std::cout << v[0];
}
```

Call all three on the same vector and only the middle one changes it. The first one also
allocated and copied the entire vector to do nothing.

### Swap, which only works one way

```cpp
void swap_wrong(int a, int b) { int t = a; a = b; b = t; }
void swap_right(int& a, int& b) { int t = a; a = b; b = t; }
```

`swap_wrong` compiles, runs, swaps two copies, and has no effect. It is the photographs. Worth
typing both and watching the first one do nothing. In real code you write `std::swap(a, b)`,
which is exactly `swap_right`.

### The vector operations you will actually use

```cpp
std::vector<int> v = {5, 3, 8, 1};

v.push_back(9);              // {5,3,8,1,9}
v.pop_back();                // {5,3,8,1}
int last  = v.back();        // 1     — no bounds check, and empty is undefined
int first = v.front();       // 5
bool none = v.empty();       // false
v.clear();                   // size 0, capacity unchanged
```

Note `v.back()` on an empty vector is undefined behaviour, not an error. Check `!v.empty()`
first, always.

Removing by value needs two steps, and it is the one thing that reads worse than Python:

```cpp
v.erase(std::remove(v.begin(), v.end(), 8), v.end());   // remove every 8
```

`std::remove` shifts the survivors to the front and returns where the junk begins; `erase` cuts
the tail off. It is the **erase-remove idiom**, it is O(n) once rather than O(n) per element, and
it is exactly the write-pointer pattern from [day 015](../day-015-the-write-pointer/README.md).
C++20 adds `std::erase(v, 8)`, which does the same thing in one call.

### Where the cost actually is

```cpp
long long total_by_value(std::vector<int> v) {           // copies 4 MB per call
    long long s = 0;
    for (int x : v) s += x;
    return s;
}

long long total_by_const_ref(const std::vector<int>& v) { // copies nothing
    long long s = 0;
    for (int x : v) s += x;
    return s;
}
```

The bodies are identical. Call each a thousand times on a million-element vector and the first
has copied four gigabytes in total and the second has copied nothing.

### Returning is different

```cpp
std::vector<int> build(int n) {
    std::vector<int> result(n);
    for (int i = 0; i < n; i++) result[i] = i * i;
    return result;                    // NOT a copy, despite appearances
}
```

Returning a large object by value looks expensive and is not. Since C++17 the compiler is
*required* to construct `result` directly in the caller's storage — no copy and no move happens
at all.

**So: take parameters by `const&`, and return by value.** Do not try to be clever by returning a
reference; section 7 shows what that costs.

### The complete program

```cpp
// vectors.cpp — vector's costs, and what a copy costs.
//   g++ -std=c++20 -O2 -Wall -Wextra -o vectors vectors.cpp && ./vectors

#include <bits/stdc++.h>
using namespace std;

// Read-only and not tiny -> const reference. No copy, cannot modify.
long long total(const vector<int>& v) {
    long long s = 0;                  // long long: see day 002's C++ lesson
    for (int x : v) s += x;           // int is tiny, so a copy per element is right
    return s;
}

// Must modify the caller's object -> plain reference.
void double_all(vector<int>& v) {
    for (int& x : v) x *= 2;          // int& so the assignment reaches the original
}

// Deliberately by value, to measure what it costs.
long long total_copying(vector<int> v) {
    long long s = 0;
    for (int x : v) s += x;
    return s;
}

// A string is not tiny either. const string& even for one argument.
bool is_palindrome(const string& s) {
    int left = 0, right = (int)s.size() - 1;
    while (left < right) {
        if (s[left] != s[right]) return false;
        left++;
        right--;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // ---- the operations ----
    vector<int> v = {5, 3, 8, 1};
    v.push_back(9);
    cout << "v = ";
    for (int x : v) cout << x << ' ';
    cout << "| size " << v.size() << " | back " << v.back() << "\n";

    // ---- which one changes the caller's vector ----
    vector<int> small = {1, 2, 3};
    double_all(small);
    cout << "after double_all: ";
    for (int x : small) cout << x << ' ';       // 2 4 6
    cout << "\n";

    // ---- reserve, measured ----
    const int N = 1000000;
    auto t0 = chrono::steady_clock::now();
    vector<int> grow;
    for (int i = 0; i < N; i++) grow.push_back(i);
    auto t1 = chrono::steady_clock::now();
    vector<int> pre;
    pre.reserve(N);
    for (int i = 0; i < N; i++) pre.push_back(i);
    auto t2 = chrono::steady_clock::now();

    auto ms = [](auto a, auto b) {
        return chrono::duration_cast<chrono::milliseconds>(b - a).count();
    };
    cout << "1e6 push_back, no reserve : " << ms(t0, t1) << " ms\n";
    cout << "1e6 push_back, reserved   : " << ms(t1, t2) << " ms\n";

    // ---- the copy, measured ----
    vector<int> data(N, 1);
    auto t3 = chrono::steady_clock::now();
    long long acc = 0;
    for (int i = 0; i < 200; i++) acc += total(data);
    auto t4 = chrono::steady_clock::now();
    for (int i = 0; i < 200; i++) acc += total_copying(data);
    auto t5 = chrono::steady_clock::now();

    cout << "200 calls by const ref    : " << ms(t3, t4) << " ms\n";
    cout << "200 calls by value        : " << ms(t4, t5) << " ms\n";

    cout << is_palindrome("malayalam") << " " << acc << "\n";  // printed so nothing is deleted
    return 0;
}
```

Typical output:

```
v = 5 3 8 1 9 | size 5 | back 9
after double_all: 2 4 6
1e6 push_back, no reserve : 12 ms
1e6 push_back, reserved   : 4 ms
200 calls by const ref    : 168 ms
200 calls by value        : 402 ms
1 400000000
```

Same answer, same work, two and a half times the time — and all of the difference is one
ampersand. Note the last `cout`: without printing `acc`, `-O2` would notice the sums are unused
and delete both loops, and you would time nothing. That is a real and common measuring mistake.

---

## 6. What it costs

The copy is a block memory copy, so the arithmetic is straightforward:

```
  vector<int> with 10^6 elements
    = 10^6 x 4 bytes
    = 4 MB

  memory bandwidth on a normal machine: roughly 10 GB/s for a large copy
    4 MB / 10 GB/s = 0.4 milliseconds per copy

  in a loop calling the function 1,000 times:
    1,000 x 0.4 ms = 0.4 seconds
    of pure copying, doing nothing
```

Plus an **allocation** per call — the copy needs 4 MB of fresh memory, and giving it back
afterwards. Allocation is not free either; it is typically hundreds of nanoseconds and much worse
under contention.

For a `vector<string>` it is worse still, because copying the vector copies every string inside
it, each of which is its own allocation. A vector of 10^5 strings averaging 20 characters is
100,000 separate allocations per copy.

**Where a reference costs nothing:**

```
  a reference compiles to one 8-byte address, passed in a register.
  cost: identical to passing one int.
  const: costs zero while running. Checked entirely when you compile.
```

And the other direction, so the rule is not a superstition:

```
  passing an int by value:      the value goes in a register.  0 extra work.
  passing an int by const ref:  the ADDRESS goes in a register, and every read
                                has to follow it out to memory.
                                Possibly slower. Definitely uglier.
```

That is why the rule has a size threshold in it. **Under about 8-16 bytes, pass by value. Above
it, pass by `const&`.**

And the growth arithmetic, since `reserve` earned 8 milliseconds above:

```
  growing from 0 to 10^6 by doubling: capacities 1, 2, 4, ... 1,048,576
  total elements copied = 1 + 2 + 4 + ... + 524,288  =  1,048,575

  so an unreserved build copies about n extra elements in total,
  spread over ~20 reallocations.  reserve() removes all of it.
```

---

## 7. The traps

### The near-miss: the range loop that copies

```cpp
vector<string> words = read_dictionary();       // 100,000 words

int long_ones = 0;
for (string w : words)                          // copies EVERY string
    if (w.size() > 10) long_ones++;
```

That loop allocates and frees 100,000 strings to look at their lengths. It is correct and about
ten times slower than it needs to be. `-Wall` does not warn, because it is legal and occasionally
what you meant.

```cpp
for (const string& w : words)                   // the fix. One character of difference.
```

### The near-miss: the reference you forgot in the modifying loop

```cpp
for (int x : v) x *= 2;       // does nothing at all
for (int& x : v) x *= 2;      // doubles the vector
```

The first doubles a copy that is discarded at the end of each iteration. No warning, no error,
and the vector is unchanged. When a loop "does nothing", this is the first thing to check.

### The real error: `v[i]` does not check, and `.at(i)` does

```cpp
vector<int> v = {1, 2, 3};
cout << v[10];        // undefined behaviour. Often prints rubbish. No error.
cout << v.at(10);     // throws
```

`v[10]` reads memory past the end of the block. It is not a crash, usually — it prints whatever
happened to be there, which is why the bug survives your testing and dies on the judge. Under the
address sanitiser it reports itself precisely:

```
=================================================================
==18342==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000001c at pc 0x000000401329
READ of size 4 at 0x60200000001c thread T0
    #0 0x401328 in main vectors.cpp:9
```

`.at(10)` checks, and throws:

```
terminate called after throwing an instance of 'std::out_of_range'
  what():  vector::_M_range_check: __n (which is 10) >= this->size() (which is 3)
Aborted (core dumped)
```

**Use `[]` in contests** — `.at()` costs a comparison per access, which matters in a hot loop —
**and compile locally with `-fsanitize=address`**, which catches the same bug with no cost in the
submitted build.

### The real error: `push_back` invalidates references

This one is genuinely nasty, because the code reads as though it should be fine.

```cpp
vector<int> v = {1, 2, 3};
int& first = v[0];        // a reference into the vector's block
v.push_back(4);           // may reallocate: new block, old one freed
cout << first;            // first names memory that was freed
```

`push_back` can outgrow the capacity, allocate a bigger block, copy everything across, and free
the old one. Every reference, pointer and iterator into the old block now names freed memory. It
often prints the right value anyway, because the freed memory has not been reused yet, which is
the worst possible outcome — it means the bug ships.

```
==19104==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000000010 at pc 0x0000004013f7
READ of size 4 at 0x602000000010 thread T0
    #0 0x4013f6 in main vectors.cpp:11
```

**The rule: do not hold a reference or an iterator across anything that can grow the vector.**
Hold the index instead — an index survives reallocation, a reference does not.

### The real error: returning a reference to a local

```cpp
int& biggest(vector<int>& v) {
    int best = v[0];
    for (int x : v) best = max(best, x);
    return best;              // returning a reference to a local variable
}
```

`best` lives on the **stack frame** of `biggest` — the block of memory that exists for the
duration of the call. The instant the function returns, that frame is gone. g++ catches this
exact case:

```
main.cpp: In function 'int& biggest(std::vector<int>&)':
main.cpp:6:12: warning: reference to local variable 'best' returned [-Wreturn-local-addr]
    6 |     return best;
      |            ^~~~
main.cpp:3:9: note: declared here
    3 |     int best = v[0];
      |         ^~~~
```

**It is a warning, not an error.** The program builds and runs. This is why you compile with
`-Wall -Wextra` and treat warnings as things to fix. The fix is to return by value.

---

## 8. In the interview

### How it gets asked

- *"What's the difference between passing by value, by reference, and by pointer?"* — the single
  most-asked C++ question in existence.
- *"Why did you write `const std::vector<int>&` there?"* — asked live, while you are writing. It
  is checking whether the ampersand was a habit or a decision.
- *"What's the complexity of `push_back`, and why is it amortised?"* — the same question today's
  DSA lesson answers for Python, in C++ clothes.
- *"What invalidates a vector's iterators?"* — the deeper one, and the one that separates people.

### What to say out loud, in the first ninety seconds

1. **By value.** *"By value, the function gets a copy. Changes are invisible to the caller, and
   the copy costs time and memory proportional to the object's size — for a million-element
   `vector<int>` that is four megabytes and a heap allocation, per call."*
2. **By reference.** *"By reference, the parameter is another name for the caller's object. No
   copy, and changes are visible outside. A reference must be bound when it is created, can never
   be re-seated, and cannot be null."*
3. **By pointer.** *"By pointer, I pass an address. Same lack of copying, but a pointer can be
   null and can be reassigned, so the callee has to handle the null case."*
4. **Give the decision rule.** *"My default is `const T&` for anything read-only that is bigger
   than a register, plain value for `int` and `double`, and `T&` when I genuinely need to modify
   the caller's object."*
5. **Say when the pointer is right.** *"I use a pointer when 'nothing' is a legitimate argument —
   `T*` documents that the argument is optional in a way a reference cannot."*
6. **Add the free part.** *"`const` costs nothing while the program runs. It is checked entirely
   at compile time, so it is documentation the compiler enforces."*

Step 5 is the one most candidates miss. "Use references, they are safer" is a slogan. "Use a
pointer when null is meaningful" is a design rule.

### The follow-ups

**"Why is `push_back` O(1) amortised rather than O(1)?"**
Because a vector keeps spare capacity, and most pushes land in it and are genuinely one step. When
capacity runs out it allocates a bigger block — GCC doubles it — copies every element across, and
frees the old one, which is O(n) for that one push. Because the capacity doubles, those copies get
proportionally rarer: building a vector of n by pushing copies about n elements in total across
roughly log n reallocations, so the average per push is a constant. If I know the final size I
call `reserve(n)` first, which removes all of it — measurably, about three times faster on a
million pushes.

**"What invalidates iterators and references into a vector?"**
Anything that can reallocate the block, so `push_back`, `insert`, `resize`, `reserve`, and
`emplace_back` — they invalidate everything if the capacity changes. `erase` invalidates
everything from the erased position onwards, because the tail shifts. `clear` invalidates
everything. The practical rule I follow is not to hold a reference or an iterator across any
operation that can change the size: I hold the index instead, because an index survives
reallocation. It is a real bug class — it usually reads the right value in testing, because the
freed memory has not been reused yet, and then fails somewhere else.

**"When would you take a large parameter by value deliberately?"**
When the function needs its own copy anyway. If I am going to modify the vector and keep the
modified version, taking it by value lets the caller hand me a temporary and have it *moved* in
rather than copied — so `f(std::move(v))` costs nothing and `f(v)` costs one copy, which I was
going to make regardless. That is the sink-parameter idiom.

**"`vector` or a plain array?"**
`vector`, almost always. It knows its own size, it grows, it frees itself, and with `-O2` the
indexing compiles to the same instructions — there is no run-time penalty for `v[i]` over `a[i]`.
A plain C array or `std::array` is worth it when the size is a compile-time constant and I want
it on the stack with no allocation at all, which in competitive programming is occasionally a real
win for small fixed tables. But a raw `new int[n]` in modern C++ is a bug waiting to happen, and I
would not write one.

### A model answer

The interviewer asks the parameter-passing question cold.

> "There are three, and I choose between them by size and by whether I need to modify.
>
> By value, the parameter is a copy. Changes inside the function are invisible to the caller, and
> I have paid for the copy — for a `vector<int>` with a million elements, that is four megabytes
> copied plus a heap allocation, on every call.
>
> By reference — `T&` — the parameter is a second name for the caller's object. No copy is made,
> and modifications are visible outside. A reference has to be bound when it is created, it can
> never be re-seated to name something else, and there is no such thing as a null reference.
>
> By pointer — `T*` — I pass an address. It does not copy either, but a pointer is a real
> variable: it can be reassigned, and it can be null, so the function has to decide what to do
> about that.
>
> My working rule is `const T&` for anything read-only that is bigger than a register; plain value
> for `int`, `double`, `char` and other small types, because there a reference is an extra
> indirection for no benefit; and `T&` when the whole point of the function is to modify the
> argument. I reach for a raw pointer mainly when null is a meaningful value — a `T*` parameter
> documents 'this argument is optional' in a way a reference cannot.
>
> Two things I would add. `const` here is free — it is checked in the compiler and generates no
> extra instructions, so it is documentation with teeth. And the mirror image on the return side
> is that I return by value, not by reference. Returning a reference to a local is a dangling
> reference and undefined behaviour, and since C++17 returning a large object by value is not a
> copy anyway — the compiler is required to construct it directly in the caller's storage."

That answer covers all three, gives the mechanism, gives a decision rule with a threshold in it,
names when the least-fashionable option is right, and volunteers the return side unprompted.

---

## 9. Recall card

1. **`vector` is the Python list with the same costs.** `push_back` and `pop_back` O(1),
   `v[i]` O(1), inserting or erasing at the front O(n). `reserve(n)` if you know the size.
2. **Passing a vector copies it.** 10^6 ints is 4 MB and an allocation, per call. `const T&`
   makes that one 8-byte address instead.
3. **`const T&` read-only, `T&` to modify, plain value for `int` and friends.** That one rule
   covers almost every parameter you will ever write.
4. **`for (const auto& x : v)` is the default loop.** `for (auto& x : v)` to modify.
   `for (auto x : v)` copies every element, which is a real bug for strings.
5. **`push_back` invalidates every reference and iterator into the vector.** Hold the index, not
   the reference. And `v[i]` does not check bounds — compile locally with `-fsanitize=address`.

---

**Next in C++:** [day 006 — string, map, set, and
pair](../day-006-python-strings-dicts-sets/04-cpp-string-map-set.md).
