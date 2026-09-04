---
day: 68
track: cpp
title: "stack, queue, deque, and priority_queue"
phase: "C++ and competitive programming"
status: written
---

# Day 068 · C++ — stack, queue, deque, and priority_queue

**After today you can:** You can reach for the right container adapter instantly, and build a min-heap in C++ without having to think about it.

**The interviewer asks it as:** *How do you make a min-heap with std::priority_queue?*

---

> Seventh of the twelve C++ days. Today's DSA lesson gives you the stack. This gives you all four
> of the containers that are really the same idea with different rules about which end you are
> allowed to touch — and the one whose default is the opposite of Python's.

---

## 1. What this is, and why they ask it

C++ ships four containers that differ only in which element you are permitted to take next.
`std::stack` gives you the one you put in most recently. `std::queue` gives you the one that has
been waiting longest. `std::deque` lets you push and pop at both ends. `std::priority_queue`
gives you the largest, whatever order things arrived in.

They are called **container adapters**, because none of them is a new structure — each is a thin
layer over a `vector` or a `deque` that hides the operations you are not supposed to use. That is
the point: a `stack` will not let you reach into the middle, so a reader knows at a glance what
your code does.

Two things about them catch people out, and both are asked in interviews. `pop()` does not return
the element it removed, which is a deliberate design decision with a good reason behind it. And
`priority_queue` is a **max-heap by default**, which is the exact opposite of Python's `heapq` —
so every Python programmer's first C++ heap comes out backwards. Knowing the incantation for a
min-heap, and being able to say why the default is a maximum, is a small question that comes up
constantly.

---

## 2. The story

Devi has worked the counter at a dosa place on Sarjapur Road for nine years, and she has a theory
that you can tell how a place is run by looking at its plates.

Theirs are steel, about two hundred of them, and they come back from the wash in a tall stack by
the serving hatch. The boy who washes puts each clean plate on the top. The cook takes each plate
he needs off the top. Nobody has ever discussed this; it is simply the only sensible thing to do
with a stack of plates.

Devi worked out one slow afternoon in 2019 that a plate washed at eleven o'clock would very often
be back on the stack by twenty past, and used again by half past. The same forty or fifty plates
go round and round all day. And the ones at the bottom of that stack — she checked once, out of
curiosity, and there was one down there with a dent in the rim that she remembered from before her
son was born. It had not been touched in years. It was not lost. It was just always underneath.

The customers are the other way round entirely. They stand in a line from the counter to the
door, and the person who has been standing longest gets served first, and if anybody tries it on,
four other people say something. Nobody has to enforce it. It enforces itself.

There is one exception and everybody accepts it. If a child is crying — actually crying, not just
restless — that order goes in next, wherever the parents happen to be standing. The owner started
that years ago and it has never caused an argument. It is not about who arrived when. It is about
who most needs to be dealt with now.

So there are three rules running at once in a room eleven feet wide. The plates: most recent
first, and the bottom one may wait forever. The line: longest wait first, no exceptions. The
crying child: most urgent first, regardless of arrival.

Devi says the plates are the only one people find strange when you point it out, and she is
right. Everybody thinks a queue is fair and a stack is odd, until they have to wash the plates.

---

## 3. The idea in plain English

### `std::stack` — last in, first out

```cpp
#include <stack>

std::stack<int> s;
s.push(3);           // put on top
s.push(7);
int top = s.top();   // 7 — LOOK at the top, do not remove
s.pop();             // remove the top. Returns NOTHING.
bool empty = s.empty();
int n = s.size();
```

That is the entire interface, and it is deliberately small. Every operation is O(1).

**`pop()` returns `void`.** This is the first thing that surprises everybody, and it is the
difference from Python's `list.pop()`, which hands the value back. You must read with `top()`
first, then remove:

```cpp
int x = s.top();     // read
s.pop();             // then remove
```

The reason is not laziness. If `pop()` returned the element **by value**, it would have to copy it
out — and if that copy threw an exception, the element would already have been removed from the
stack and the copy would have failed, so the value would be lost with no way to recover it. By
splitting into a `top()` that only reads and a `pop()` that cannot throw, neither operation can
lose data. It is called **exception safety**, and it is a real interview answer.

### `std::queue` — first in, first out

```cpp
#include <queue>

std::queue<int> q;
q.push(3);           // join the back of the line
q.push(7);
int front = q.front();   // 3 — the one who has waited longest
int back  = q.back();    // 7
q.pop();                 // remove from the front. Returns nothing.
```

`push` at the back, `front` and `pop` at the front. All O(1). This is what every breadth-first
search runs on, from [day 101](../day-101-bfs-level-order/README.md) onwards.

### `std::deque` — both ends

A **deque** — say "deck", short for double-ended queue — is a `vector` that is also cheap at the
front.

```cpp
#include <deque>

std::deque<int> d;
d.push_back(3);
d.push_front(1);     // O(1), which a vector cannot do
d.pop_back();
d.pop_front();
int x = d[0];        // yes, you can still index it. O(1).
```

Everything is O(1): both ends, and indexing. That looks like a free lunch and it is not — see
section 6. It is Python's `collections.deque`, with the addition that C++'s can be indexed.

You need it for exactly two things: a sliding window maximum
([day 074](../day-074-deques-and-window-max/README.md)), and 0-1 BFS
([day 141](../day-141-multi-source-bfs/README.md)). Otherwise prefer a `vector`.

### `std::priority_queue` — largest first

```cpp
#include <queue>

std::priority_queue<int> pq;     // a MAX-heap. The largest comes out first.
pq.push(3);
pq.push(9);
pq.push(5);
int biggest = pq.top();          // 9
pq.pop();                        // removes the 9
```

`push` and `pop` are **O(log n)**; `top` is O(1). It is a binary heap stored in an array, which
[day 113](../day-113-the-heap/README.md) draws properly.

**The default is a maximum, and Python's `heapq` default is a minimum.** This is the single most
common C++ mistake a Python programmer makes, and it does not produce an error — it produces
answers that are exactly backwards.

### Making a min-heap: the three ways

**One — the declaration you should memorise:**

```cpp
std::priority_queue<int, std::vector<int>, std::greater<int>> pq;
```

Three template arguments, and you cannot skip the middle one. **The second argument is the
underlying container, not the comparator.** Writing `priority_queue<int, greater<int>>` is the
classic error and section 7 shows what it prints.

Read it as: elements are `int`, stored in a `vector<int>`, ordered by `greater` — and `greater`
means "the *greatest* according to this comparator comes out first", so with `greater` the
smallest wins. That inversion is genuinely confusing; the practical answer is that
`greater` gives you a min-heap, and you should just know it.

**Two — negate everything.** Push `-x`, and negate again when you pop. It works, it is one line
shorter, and it is a real source of sign bugs. Fine for a contest, avoid in an interview.

**Three — a custom comparator, when the elements are not plain numbers:**

```cpp
struct Task { int priority; std::string name; };

auto cmp = [](const Task& a, const Task& b) {
    return a.priority > b.priority;      // '>' gives smallest-priority-first
};
std::priority_queue<Task, std::vector<Task>, decltype(cmp)> pq(cmp);
```

`decltype(cmp)` means "the type of `cmp`", which you need because a lambda's type has no name. In
C++20 the `(cmp)` at the end can be dropped for a capture-less lambda.

**The rule to hold on to: the comparator is backwards from `sort`.** In `sort`, `cmp(a,b)` true
means a comes first. In `priority_queue`, `cmp(a,b)` true means a comes **later**. Get it wrong
and your heap is inverted. When in doubt, push three values and print the first one.

For pairs — which is what Dijkstra needs — this is the idiom:

```cpp
// min-heap of (distance, node)
std::priority_queue<std::pair<int,int>,
                    std::vector<std::pair<int,int>>,
                    std::greater<std::pair<int,int>>> pq;
```

`pair` compares on `.first` then `.second`, so putting the distance first gives you the nearest
node. That is [day 136](../day-136-dijkstra/README.md) in one declaration.

### They are adapters, and you can choose the container

```cpp
std::stack<int>                     s1;   // wraps a deque (the default)
std::stack<int, std::vector<int>>   s2;   // wraps a vector — faster
```

`stack` and `queue` default to `deque` underneath; `priority_queue` defaults to `vector`. Using
`vector` for a stack is measurably faster because the memory is contiguous, and it is a free win
in a hot loop. A `queue` cannot use a `vector`, because a vector has no cheap `pop_front`.

**None of them can be iterated.** There is no `begin()`, no range-based `for`. That is the point
of the adapter. If you need to look through the elements, you wanted a `vector` or a `deque`.

---

## 4. The picture

The three access rules, side by side:

```
  STACK — last in, first out                QUEUE — first in, first out

        push          pop                     pop                    push
         |             ^                       ^                      |
         v             |                       |                      v
       +-----------------+                  +-----------------------------+
       |   7   | <- top  |                  | 3 | 5 | 7 |  <- back        |
       |   5   |         |                  +-----------------------------+
       |   3   |         |                    ^
       |   1   | <- the dented plate.         front
       +-------+          never reached.

  push and pop both touch the TOP           push at the BACK, pop at the FRONT


  DEQUE — both ends                         PRIORITY_QUEUE — largest first

  push_front           push_back                        +-----+
      |                    |                            |  9  |  <- top
      v                    v                            +-----+
    +---------------------------+                      /       \
    | 1 | 3 | 5 | 7 |           |                 +-----+     +-----+
    +---------------------------+                 |  5  |     |  8  |
      ^                    ^                      +-----+     +-----+
  pop_front            pop_back                    /
                                              +-----+
  and d[2] still works, O(1)                  |  3  |
                                              +-----+

                                    a heap: every parent >= its children.
                                    push and pop are O(log n) — the height.
                                    order among siblings means nothing.
```

**What to notice:** in the first three pictures, the element you get is decided by *position*. In
the fourth, it is decided by *value* — and that is why it costs log n instead of 1. You are
paying for the tree to reshuffle itself.

The min-heap confusion, drawn, because this is the bit people get wrong:

```
  priority_queue<int>                     the DEFAULT
  push 3, 9, 5   ->  top() is 9           largest first     (max-heap)

  priority_queue<int, vector<int>, greater<int>>
  push 3, 9, 5   ->  top() is 3           smallest first    (min-heap)
                     ^^^^^^^^^^^
                     "greater" gives you the SMALLEST.
                     Read it as: greater() is the comparator that
                     decides who sinks, so with greater, big things sink.
```

**What to notice:** the word `greater` produces the smaller answer. There is no way to make that
read naturally; memorise the declaration as one unit.

---

## 5. The code, built step by step

### Balanced brackets — the stack, in six lines

The [day 069](../day-069-balanced-brackets/README.md) problem, which is the standard use of a
stack.

```cpp
bool balanced(const std::string& s) {
    std::stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') st.push(c);
        else {
            if (st.empty()) return false;          // a closer with nothing open
            char open = st.top();
            st.pop();
            if ((c == ')' && open != '(') ||
                (c == ']' && open != '[') ||
                (c == '}' && open != '{')) return false;
        }
    }
    return st.empty();                             // anything left open?
}
```

Note the `st.empty()` check before `st.top()`. **`top()` on an empty stack is undefined
behaviour**, not an exception — it reads memory that is not yours and usually returns rubbish.
Every `top()` and `front()` needs a guard.

### The monotonic stack — [day 071](../day-071-monotonic-stack/README.md)

The pattern that answers "next greater element" for every position in one pass.

```cpp
std::vector<int> next_greater(const std::vector<int>& a) {
    int n = a.size();
    std::vector<int> ans(n, -1);
    std::stack<int> st;                  // holds POSITIONS, not values
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.top()] < a[i]) {
            ans[st.top()] = a[i];        // a[i] is the next greater for that position
            st.pop();
        }
        st.push(i);
    }
    return ans;
}
```

Storing positions rather than values is the trick — it lets you write the answer back into the
right slot. Every element is pushed once and popped at most once, so the whole thing is O(n)
despite the inner `while`.

### BFS — the queue

```cpp
std::queue<int> q;
std::vector<bool> seen(n, false);
q.push(start);
seen[start] = true;

while (!q.empty()) {
    int u = q.front();
    q.pop();                             // read first, then remove
    for (int v : adj[u]) {
        if (!seen[v]) {
            seen[v] = true;              // mark on PUSH, not on pop
            q.push(v);
        }
    }
}
```

Marking `seen` when you push, not when you pop, is what stops a node being queued twice. It is the
single most common BFS bug and it is worth having in your fingers now.

### Top K — the min-heap of size K

The idiom worth memorising, because it turns an O(n log n) sort into O(n log k).

```cpp
// the k largest values, using a MIN-heap of size k
std::priority_queue<int, std::vector<int>, std::greater<int>> pq;
for (int x : a) {
    pq.push(x);
    if ((int)pq.size() > k) pq.pop();    // drop the smallest, keep the k biggest
}
```

The counter-intuitive part: to keep the *largest* k, you use a *minimum* heap, so that the thing
you throw away is the smallest of the survivors. Say that out loud once and it sticks.

### The complete program

```cpp
// adapters.cpp — the four adapters, and how to invert a heap.
//   g++ -std=c++20 -O2 -Wall -Wextra -o adapters adapters.cpp && ./adapters

#include <bits/stdc++.h>
using namespace std;

bool balanced(const string& s) {
    stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') st.push(c);
        else {
            if (st.empty()) return false;
            char open = st.top();
            st.pop();
            if ((c == ')' && open != '(') || (c == ']' && open != '[') ||
                (c == '}' && open != '{')) return false;
        }
    }
    return st.empty();
}

vector<int> next_greater(const vector<int>& a) {
    int n = (int)a.size();
    vector<int> ans(n, -1);
    stack<int> st;                          // positions
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.top()] < a[i]) {
            ans[st.top()] = a[i];
            st.pop();
        }
        st.push(i);
    }
    return ans;
}

// The largest k values, with a min-heap of size k. O(n log k).
vector<int> top_k(const vector<int>& a, int k) {
    priority_queue<int, vector<int>, greater<int>> pq;
    for (int x : a) {
        pq.push(x);
        if ((int)pq.size() > k) pq.pop();   // throw away the smallest so far
    }
    vector<int> out;
    while (!pq.empty()) { out.push_back(pq.top()); pq.pop(); }
    return out;                             // ascending
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // ---- stack ----
    cout << "balanced(\"{[()]}\") = " << balanced("{[()]}") << "\n";
    cout << "balanced(\"{[(])}\") = " << balanced("{[(])}") << "\n";

    vector<int> a = {2, 1, 4, 3};
    cout << "next greater:";
    for (int x : next_greater(a)) cout << " " << x;      // 4 4 -1 -1
    cout << "\n";

    // ---- queue ----
    queue<int> q;
    for (int x : {3, 5, 7}) q.push(x);
    cout << "queue front " << q.front() << " back " << q.back() << " -> pop -> ";
    q.pop();
    cout << "front " << q.front() << "\n";

    // ---- deque: both ends, and still indexable ----
    deque<int> d;
    d.push_back(3);
    d.push_front(1);
    d.push_back(5);
    cout << "deque:";
    for (int x : d) cout << " " << x;                    // 1 3 5
    cout << " | d[1] = " << d[1] << "\n";

    // ---- priority_queue: the default is a MAXIMUM ----
    priority_queue<int> mx;
    for (int x : {3, 9, 5}) mx.push(x);
    cout << "max-heap top = " << mx.top() << "   (the default)\n";

    priority_queue<int, vector<int>, greater<int>> mn;
    for (int x : {3, 9, 5}) mn.push(x);
    cout << "min-heap top = " << mn.top() << "   (greater<int> inverts it)\n";

    // ---- a min-heap of pairs: (distance, node). Dijkstra's shape. ----
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
    pq.push({7, 100});
    pq.push({2, 200});
    pq.push({5, 300});
    auto [dist, node] = pq.top();
    cout << "nearest: node " << node << " at distance " << dist << "\n";

    // ---- top k with a min-heap of size k ----
    vector<int> big = {5, 1, 9, 3, 7, 8};
    cout << "top 3:";
    for (int x : top_k(big, 3)) cout << " " << x;        // 7 8 9
    cout << "\n";

    return 0;
}
```

Expected output:

```
balanced("{[()]}") = 1
balanced("{[(])}") = 0
next greater: 4 4 -1 -1
queue front 3 back 7 -> pop -> front 5
deque: 1 3 5 | d[1] = 3
max-heap top = 9   (the default)
min-heap top = 3   (greater<int> inverts it)
nearest: node 200 at distance 2
top 3: 7 8 9
```

---

## 6. What it costs

### Per operation

```
  stack           push  O(1) amortised     top O(1)    pop O(1)
  queue           push  O(1)               front O(1)  pop O(1)
  deque           push_front/back O(1)     d[i] O(1)   pop O(1)
  priority_queue  push  O(log n)           top O(1)    pop O(log n)
```

The priority queue is the only one that is not constant, and log n is small: for n = 10^6 it is
twenty comparisons plus twenty swaps.

Measured, per operation, on 10^6 elements:

```
  stack<int, vector<int>>  push/pop     ~2 ns
  stack<int>  (deque-backed)            ~4 ns
  queue<int>  (deque-backed)            ~4 ns
  priority_queue<int>  push             ~35 ns
  priority_queue<int>  pop              ~90 ns
```

The pop is more expensive than the push because sifting down compares two children at each level
and the memory access pattern jumps around; the push usually stops after one or two levels.

### Where a `deque` gets its "free" front

A `deque` is not one block. It is an array of pointers to fixed-size chunks — 512 bytes each in
libstdc++. Pushing at the front allocates a new chunk and points at it; nothing shifts. That is
where the O(1) comes from.

The price:

```
  vector<int>, 10^6 elements
    one 4 MB block, perfectly contiguous.
    scanning it: the prefetcher predicts everything.  ~0.3 ms

  deque<int>, 10^6 elements
    ~7,800 chunks of 512 bytes, plus a pointer array
    scanning it: a jump every 128 elements, plus one extra indirection per access
    ~2-3x slower to scan, and d[i] is two memory lookups instead of one
```

**So: use a `vector` unless you actually need `push_front`.** The default `stack` and `queue` sit
on a `deque`, which is why `stack<int, vector<int>>` is worth typing in a hot loop.

### The heap's height, and why top-k beats sorting

```
  a binary heap of n elements has height  log2(n)
    n = 10^6  ->  20 levels

  push: sift UP,   worst case 20 swaps, average about 1.6
  pop:  sift DOWN, worst case 20 swaps, and it really does go most of the way

  top-k of n elements with a size-k min-heap:
    n pushes and pops on a heap of size k  =  n log k

    n = 10^6, k = 100:   10^6 x 7  =  7 x 10^6      ->  ~0.05 s
    sorting instead:     10^6 x 20 =  2 x 10^7      ->  ~0.10 s
    and the heap uses 100 elements of memory, not 10^6
```

Twice as fast and ten thousand times less memory. That is why "find the top k of a stream" is a
heap question and not a sorting question.

---

## 7. The traps

### The real error: `pop()` does not return anything

Every Python programmer writes this once:

```cpp
std::stack<int> s;
s.push(5);
int x = s.pop();      // does not compile
```

```
main.cpp:8:17: error: void value not ignored as it ought to be
    8 |     int x = s.pop();
      |             ~~~~~^~
```

`void value not ignored as it ought to be` means "this expression has no value and you tried to
use one". The fix is two lines:

```cpp
int x = s.top();
s.pop();
```

Unlike most traps in this track, this one is caught at compile time and cannot ship. It is on the
list because the error message is opaque the first time you meet it.

### The real error: the min-heap declaration with two arguments

```cpp
std::priority_queue<int, std::greater<int>> pq;      // wrong
```

The second template argument is the **container**, not the comparator. GCC's message is long; the
line that tells you is:

```
In file included from /usr/include/c++/13/queue:66,
                 from main.cpp:1:
/usr/include/c++/13/bits/stl_queue.h:509:41: error: no type named 'value_type' in 'struct std::greater<int>'
  509 |       typedef typename _Sequence::value_type                 value_type;
      |                                             ^~~~~~~~~~
```

`_Sequence` is the library's name for the container parameter, and it is complaining that
`greater<int>` is not one. The fix is the three-argument form:

```cpp
std::priority_queue<int, std::vector<int>, std::greater<int>> pq;
```

### The near-miss: the default is a maximum

```cpp
std::priority_queue<int> pq;      // MAX-heap
for (int x : distances) pq.push(x);
int nearest = pq.top();           // this is the FARTHEST
```

It compiles. It runs. Every answer is inverted. If you have come from Python, where `heapq` is a
min-heap and there is no max-heap at all, this will happen to you, and Dijkstra with a max-heap
produces plausible-looking wrong distances rather than an obvious failure.

**Habit: after declaring a heap, push three values and print `top()` once.** Two seconds, and it
settles the question before you build anything on top of it.

### The near-miss: `top()` and `front()` on an empty container

```cpp
std::stack<int> s;
int x = s.top();      // undefined behaviour. No exception. No error.
```

It reads whatever is at that memory. Often it prints a plausible number, which is the worst
outcome, because the bug survives testing. There is no checked alternative — unlike `vector`,
which has `.at()`, the adapters offer nothing.

**Every `top()`, `front()` and `back()` needs `!empty()` in front of it**, and it must be in the
same condition:

```cpp
while (!st.empty() && a[st.top()] < a[i]) { ... }
//     ^^^^^^^^^^^^^^ first, and && short-circuits so top() is never reached when empty
```

`&&` evaluates left to right and stops at the first false, which is what makes that line safe.
Write the guard first, every time.

### The near-miss: comparators are backwards from `sort`

```cpp
// sort:            true means a comes FIRST
std::sort(v.begin(), v.end(), [](int a, int b) { return a < b; });   // ascending

// priority_queue:  true means a comes LAST
std::priority_queue<int, std::vector<int>, std::less<int>> pq;       // MAX-heap
```

Same word, opposite outcome. `less` gives a max-heap and `greater` gives a min-heap, which reads
backwards and is not a mistake in the library — the comparator defines which element sinks, not
which one surfaces. There is no trick for remembering it. Memorise the min-heap declaration as a
single unit and test it when you write it.

### The quiet one: you cannot look inside

```cpp
std::priority_queue<int> pq;
for (int x : pq) { ... }        // does not compile: no begin()
```

There is no iteration and no way to inspect anything but `top()`. To see the contents you must pop
everything, which destroys the heap — so you copy it first, and copying a heap of 10^6 elements is
a 4 MB copy. If you find yourself needing to look through it, you wanted a `multiset`, which is
sorted, iterable, and lets you erase from the middle.

---

## 8. In the interview

### How it gets asked

- *"How do you make a min-heap in C++?"* — the direct version, and a genuine memory test.
- *"Why doesn't `stack::pop()` return the element?"* — a design question, and a very good one.
- *"Find the k largest elements in a stream of a million numbers."* — the applied version, where
  the answer is a size-k min-heap.
- *"When would you use a `deque` over a `vector`?"* — checking whether you know what the "free"
  front costs.

### What to say out loud, in the first ninety seconds

1. **Name the default.** *"`std::priority_queue<int>` is a max-heap — `top()` gives the largest.
   That is the opposite of Python's `heapq`, which is a min-heap."*
2. **Give the declaration.** *"For a min-heap I write
   `priority_queue<int, vector<int>, greater<int>>`. Three template arguments, and the middle one
   is the underlying container, not the comparator — that is the usual mistake."*
3. **Explain the inversion.** *"`greater` gives the smallest because the comparator says which
   element sinks, not which surfaces. It reads backwards, so I test it with three pushes when I
   write it."*
4. **Give the costs.** *"`push` and `pop` are O(log n), `top` is O(1). It is a binary heap in an
   array, so there is no per-node allocation."*
5. **Name the alternative.** *"The other way is to push negated values into a max-heap, which is
   shorter and a real source of sign bugs. I would not do it in code anyone else reads."*
6. **Offer the use.** *"The pattern I actually reach for is a size-k min-heap for top-k — push
   everything, pop when the size exceeds k, so what falls out is the smallest. That is O(n log k)
   instead of O(n log n), and O(k) memory."*

Step 6 turns a syntax answer into a technique answer, which is what they are really listening for.

### The follow-ups

**"Why doesn't `pop()` return the element?"**
Exception safety. If `pop()` removed the element and returned it by value, it would have to copy
or move it into the caller's variable — and if that copy threw, the element would already be gone
from the container with no way to get it back. The value would be lost between two operations that
each individually looked fine. By splitting it into `top()`, which only reads and can be called
again, and `pop()`, which removes and is guaranteed not to throw, no operation can lose data.
Herb Sutter wrote this up in *Exceptional C++* and it is why the whole standard library is shaped
this way. C++17 added `std::optional` and better move guarantees, which is why newer designs can
sometimes get away with a returning pop, but the containers keep the old shape for compatibility.

**"What is a `deque` actually, and why is `push_front` O(1)?"**
It is not one contiguous block. libstdc++ implements it as an array of pointers to fixed-size
chunks — 512 bytes each. Pushing at the front allocates a new chunk and adds a pointer, so nothing
shifts, which is where the constant time comes from. The costs are that `d[i]` needs two memory
lookups instead of one, and that scanning it is two to three times slower than a vector because
you jump between chunks and lose the prefetcher. So it is the right choice when I genuinely need
both ends — a sliding-window maximum, or 0-1 BFS — and the wrong default otherwise. I would also
say that `stack` and `queue` sit on a `deque` by default, so `stack<int, vector<int>>` is a free
speedup in a hot loop.

**"How would you find the median of a stream?"**
Two heaps. A max-heap for the lower half and a min-heap for the upper half, kept balanced so their
sizes differ by at most one. The median is then either the top of the larger heap, or the average
of the two tops when the sizes are equal. Insert is O(log n) and reading the median is O(1). The
fiddly part is the rebalancing — you push onto one side, then move its top across if the sizes go
out of step by more than one. That is [day 118](../day-118-two-heaps/README.md).

**"Can you delete an arbitrary element from a `priority_queue`?"**
Not directly — there is no such operation, and you cannot even iterate it. Two standard ways
round. **Lazy deletion**: keep a separate set of things you have logically removed, and whenever
you `top()`, discard entries that are in that set before using one. That is what most Dijkstra
implementations do instead of decrease-key, and it is why you see `if (d > dist[u]) continue;` at
the top of the loop. Or use a `std::multiset`, which is sorted, gives you the smallest at
`begin()` and the largest at `rbegin()`, and supports erasing any element in O(log n) — at the
cost of per-node allocation and worse cache behaviour.

### A model answer

The interviewer asks for the k largest elements in a stream of a million numbers.

> "I'd use a min-heap of size k.
>
> The instinct is a max-heap, and that is the wrong way round. I want to keep the k largest, which
> means the element I throw away each time is the smallest of the ones I am keeping — so the thing
> that needs to be instantly available is the minimum. A min-heap of size k gives me that.
>
> In C++ that is `priority_queue<int, vector<int>, greater<int>>`. Three template arguments: the
> element type, the underlying container, and the comparator. The middle one catches people out —
> it is the container, not the comparator, so the two-argument version does not compile. And
> `greater` produces a minimum at the top, because the comparator defines which element sinks
> rather than which surfaces.
>
> The loop is: push each value, and if the size exceeds k, pop. At the end the heap holds exactly
> the k largest, and popping them gives them in ascending order.
>
> The cost is n pushes and pops on a heap that never exceeds k, so O(n log k) rather than the
> O(n log n) a full sort would cost. For a million elements and k of a hundred, that is about
> 7 × 10^6 operations against 2 × 10^7 — roughly twice as fast. More importantly the memory is
> O(k), a hundred elements rather than a million, which is what makes it work on a stream at all:
> I never need to hold the whole input.
>
> One thing I'd check before writing it: whether k is close to n. If k is most of n, the heap
> offers nothing and I would just sort. And if I needed to remove arbitrary elements as well as the
> minimum, I would use a `multiset` instead — it gives me both ends and O(log n) erase anywhere, at
> the cost of per-node allocation."

That answer explains the counter-intuitive choice, gives the exact declaration and the trap in it,
gives the complexity with real numbers, names the memory advantage that is the actual point, and
says when it would not use the technique.

---

## 9. Recall card

1. **`stack` last-in-first-out, `queue` first-in-first-out, `deque` both ends, `priority_queue`
   largest first.** All O(1) except the heap's push and pop, which are O(log n).
2. **`pop()` returns nothing.** Read with `top()` or `front()` first, then `pop()`. And both are
   undefined behaviour on an empty container — always guard with `!empty()` first, using `&&`.
3. **`priority_queue<int>` is a MAX-heap** — the opposite of Python's `heapq`. For a min-heap:
   `priority_queue<int, vector<int>, greater<int>>`. The middle argument is the container.
4. **Heap comparators are backwards from `sort`'s.** `less` gives a max-heap, `greater` gives a
   min-heap. Test with three pushes when you declare one.
5. **Top-k = a min-heap of size k.** Push everything, pop when size exceeds k. O(n log k) time and
   O(k) memory — the reason it works on a stream.

---

**Next in C++:** [day 078 — structs, pointers, and building your own
nodes](../day-078-nodes-and-links/04-cpp-structs-pointers.md).
