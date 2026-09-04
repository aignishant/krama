---
day: 143
track: cpp
title: "DP tables in C++, and the contest traps that are left"
phase: "C++ and competitive programming"
status: written
---

# Day 143 · C++ — DP tables in C++, and the contest traps that are left

**After today you can:** You can allocate a DP table of any shape, memoise with a sentinel, and name the five bugs that still cost you contests.

**The interviewer asks it as:** *How would you write a 2D DP table in C++, and what does it cost in memory?*

---

> The last of the ten C++ days. Today's DSA lesson tells you what dynamic programming is. This
> tells you how to hold the table in C++ without running out of memory, and closes the track with
> the bugs that are left after everything else in it has been learned.

---

## 1. What this is, and why they ask it

Dynamic programming is a table and the order you fill it in. In Python the table is a list of
lists and you do not think about it. In C++ you must decide three things before you write a line:
how big it is, what type the entries are, and how it gets reset.

Those three decisions are where DP solutions actually fail. A table of 10^4 by 10^4 `int`s is 400
megabytes and will not fit in a 256 megabyte limit. A table initialised to `INT_MAX` overflows the
moment you add a weight to it. And a table that is not cleared between test cases gives a right
answer on the first case and quiet nonsense on the rest — which is the single most common
"accepted on my machine" bug in competitive programming.

Interviewers ask about the memory because it is where a correct recurrence still fails, and
because the follow-up — "can you do it in O(n) space instead of O(n²)?" — is the standard way to
turn one DP question into two.

---

## 2. The story

Ravi has driven an auto in Indore since 2011, mostly from the stand outside the railway station,
and the question he is asked forty times a day is how much to somewhere.

For the first year he worked out every one from scratch. How far, which way, what the traffic is
doing at that hour, whether the flyover is shut. Thirty seconds of thinking, and the passenger
standing there watching him think, which never looks good.

What he noticed, some time in the second year, was that he was doing the same thinking again and
again. Almost every trip out of the station goes through one of four places — the Palasia
crossing, the Bhawarkuan crossing, the bus stand, or the bridge by the temple. He had worked out
the run from the station to Palasia several thousand times.

So he stopped. He worked out those four properly, once, sitting there on a slow Tuesday, and put
them in the notes on his phone. After that a fare was one saved number plus the short bit at the
end. Four seconds, not thirty.

He did the four in a particular order, which he says afterwards was the part that made it work. He
did the nearest one first, then the next nearest, and by the time he got to the far ones he was
not working them out from the station at all — he was working them out from a number he already
had. Each one needed only the one before it.

The trouble came in 2019, when they closed the Bhawarkuan underpass for eleven months and
everything through there took twice as long.

Ravi updated Bhawarkuan on his phone that first week. What he did not do was update the two
further-out places he had worked out *from* Bhawarkuan, because he had worked those out in 2012
and had genuinely forgotten they were built on it. So for about five months he quoted two
destinations at a price that had been correct before the underpass shut and was nonsense
afterwards.

He was not guessing. That is what he says about it. He had a number, he trusted the number, and
the number had been right. It was just built on something that had changed underneath it, and
nothing about looking at it told him so.

---

## 3. The idea in plain English

### The table

A one-dimensional table is a `vector`:

```cpp
std::vector<long long> dp(n + 1, 0);
```

`n + 1` because DP tables are almost always indexed 0 to n inclusive, and the off-by-one there is
worth being deliberate about. `0` is the initial value, and choosing it is a real decision, not a
formality.

Two dimensions:

```cpp
std::vector<std::vector<int>> dp(rows + 1, std::vector<int>(cols + 1, 0));
```

Read it inside out: `vector<int>(cols + 1, 0)` is one row, and the outer constructor makes
`rows + 1` copies of it. Then `dp[i][j]` is the cell.

Three dimensions, which the harder problems need:

```cpp
std::vector<std::vector<std::vector<int>>> dp(
    a, std::vector<std::vector<int>>(b, std::vector<int>(c, 0)));
```

At that point it is worth stopping to check the arithmetic, because `a × b × c` grows very fast
and section 6 shows where the cliff is.

### The initial value carries meaning

This is the decision people make carelessly and then debug for an hour.

| Filling with | Means | Use for |
|---|---|---|
| `0` | "zero ways", "zero profit" | counting, maximising a sum from nothing |
| `-1` | "not computed yet" | top-down memoisation |
| `INT_MAX` | "impossible / infinity" | minimising — **but see the trap** |
| `1e18` (in `long long`) | "impossible / infinity" | minimising, safely |
| `false` | "not reachable" | subset-sum style reachability |

`-1` as "not computed" only works when a real answer can never be −1. In a counting problem where
0 is a legitimate answer, that is exactly why you cannot use 0 as the sentinel.

### Top-down: recursion plus a memo

The shape that follows the recurrence directly.

```cpp
std::vector<int> memo;

int solve(int i) {
    if (i <= 1) return i;                  // base case
    if (memo[i] != -1) return memo[i];      // already worked out — Ravi's phone
    return memo[i] = solve(i - 1) + solve(i - 2);
}

// caller:
memo.assign(n + 1, -1);
int answer = solve(n);
```

`return memo[i] = ...` assigns and returns in one expression, which is idiomatic and worth
recognising.

Top-down is easier to write, because you write the recurrence and the memo is bookkeeping. It has
two costs. It carries recursion depth, so a chain of 10^5 states will overflow the 8 MB stack
exactly as
[day 125's DFS did](../day-125-what-a-graph-is/04-cpp-graphs-and-recursion.md). And every state
costs a function call, which is perhaps five to ten times more than a loop iteration.

### Bottom-up: fill it in order

Ravi doing the nearest junction first.

```cpp
std::vector<long long> dp(n + 1, 0);
dp[0] = 0;
dp[1] = 1;
for (int i = 2; i <= n; i++)
    dp[i] = dp[i - 1] + dp[i - 2];
```

No recursion, no call overhead, and no depth limit. The cost is that **you must work out the order
yourself** — every cell you read must already be filled. That is the whole skill, and it is what
[day 147](../day-147-finding-the-state/README.md) is about.

**Write top-down first if the recurrence is complicated, then convert if you need the speed or the
depth.** Both are the same table.

### Rolling: when each row needs only the one before

If `dp[i][j]` depends only on row `i - 1`, you do not need every row.

```cpp
// full:     dp[n][W]  — O(n x W) memory
// rolling:  two rows  — O(W) memory
std::vector<int> prev(W + 1, 0), cur(W + 1, 0);
for (int i = 1; i <= n; i++) {
    for (int j = 0; j <= W; j++)
        cur[j] = std::max(prev[j], prev[j - weight[i]] + value[i]);
    std::swap(prev, cur);          // O(1): swaps the internal pointers, not the data
}
```

`std::swap` on two vectors exchanges their internal pointers, so it is constant time regardless of
size. That is what makes the rolling trick free.

The 0/1 knapsack goes further — one row, filled **backwards**:

```cpp
std::vector<int> dp(W + 1, 0);
for (int i = 0; i < n; i++)
    for (int j = W; j >= weight[i]; j--)          // BACKWARDS
        dp[j] = std::max(dp[j], dp[j - weight[i]] + value[i]);
```

Backwards so that `dp[j - weight[i]]` is still the *previous* row's value. Loop forwards and it is
the current row's, which lets you use the same item twice — and that is the unbounded knapsack,
which is a different problem. **The direction of one loop is the entire difference between the two
problems.** [Day 148](../day-148-knapsack/README.md) and
[day 150](../day-150-coin-change/README.md) are that pair.

### The reset, which is Ravi's underpass

Most contest problems have multiple test cases, and this is where DP solutions die.

```cpp
int t;
std::cin >> t;
while (t--) {
    int n;
    std::cin >> n;
    std::vector<int> dp(n + 1, -1);      // declared INSIDE the loop: fresh every time
    // ...
}
```

Declaring the table inside the loop is the safe habit, because it cannot be forgotten. A global
table is faster — no reallocation per case — but then you must clear it yourself, and clearing
only the part you used is what people get wrong:

```cpp
const int MAXN = 100005;
int dp[MAXN];

while (t--) {
    int n;
    std::cin >> n;
    std::fill(dp, dp + n + 1, -1);       // clear only 0..n, not all of MAXN — much faster
    // ...
}
```

If you clear all of `MAXN` on every one of 10^5 test cases, that is 10^10 writes and you have
turned a fast solution into a timeout by being careful.

### `memset`, and its one rule

You will see this everywhere:

```cpp
std::memset(dp, -1, sizeof dp);      // works
std::memset(dp, 0, sizeof dp);       // works
std::memset(dp, 1, sizeof dp);       // does NOT do what you think
```

`memset` sets every **byte** to the value. For 0 and −1 that happens to give the whole integer 0
and −1, because their byte patterns are all-zeros and all-ones. For anything else it does not: byte
1 repeated four times is 0x01010101, which is **16,843,009**.

That is occasionally used deliberately as a large sentinel — `memset(dp, 0x3f, sizeof dp)` gives
1,061,109,567, about 10^9, which is a convenient infinity you can add to without overflowing. But
`memset(dp, 1, ...)` intending 1 is always a bug.

`memset` only works on plain arrays, not on `vector`. For a vector use `assign` or `fill`.

---

## 4. The picture

The table, and the order it gets filled:

```
  the 0/1 knapsack: dp[i][j] = best value using the first i items, capacity j

  fill order: row by row, left to right.  Each cell reads only the row above.

           j=0   1    2    3    4    5   <- capacity
        +-----+----+----+----+----+----+
  i=0   |  0  | 0  | 0  | 0  | 0  | 0  |   no items: nothing to take
        +-----+----+----+----+----+----+
  i=1   |  0  | 0  | 3  | 3  | 3  | 3  |   item 1: weight 2, value 3
        +-----+----+----+----+----+----+
  i=2   |  0  | 0  | 3  | 4  | 4  | 7  |   item 2: weight 3, value 4
        +--^--+----+--^-+----+----+--^-+
           |        |               |
           |        +---- dp[1][2]  +--- max( dp[1][5], dp[1][5-3] + 4 )
           |             (skip it)             = max( 3, 3 + 4 ) = 7
           base

  every cell reads dp[i-1][ something <= j ].  Never the current row.
  So only the previous row is ever needed  ->  the rolling trick.
```

**What to notice:** the whole table is 3 × 6 cells but only two rows are ever live. That
observation, and nothing cleverer, is what turns O(n × W) memory into O(W).

The one-row backwards fill, which is the bit that confuses everyone:

```
  one row, item of weight 2, value 3.  dp starts as the PREVIOUS row.

  FORWARDS (wrong for 0/1):
     j:   0    1    2    3    4
        [ 0 ][ 0 ][ 0 ][ 0 ][ 0 ]
  j=2:              ^ dp[2] = dp[0] + 3 = 3      (dp[0] is the old row: fine)
        [ 0 ][ 0 ][ 3 ][ 0 ][ 0 ]
  j=4:                        ^ dp[4] = dp[2] + 3 = 6
                                       ^^^^^
                              dp[2] was ALREADY UPDATED this row.
                              The item has been used twice.

  BACKWARDS (correct for 0/1):
     j:   4    3    2    1    0
  j=4:  ^ dp[4] = dp[2] + 3 = 3        (dp[2] is still the old row: correct)
  j=2:            ^ dp[2] = dp[0] + 3 = 3
                              every cell read is still from the previous row
```

**What to notice:** the loop direction decides whether the cell you read has already been touched
this round. That is the whole difference between "each item once" and "each item any number of
times".

---

## 5. The code, built step by step

### Allocating, and checking the arithmetic first

```cpp
int n = 5000, m = 5000;
std::vector<std::vector<int>> dp(n + 1, std::vector<int>(m + 1, 0));
```

Before typing that, do the sum: 5001 × 5001 × 4 bytes = **100 MB**. That fits in 256 MB, just. Make
it 10^4 × 10^4 and it is 400 MB and it does not. Section 6 has the table.

If the arithmetic is tight, three things to try, in order:

```cpp
std::vector<std::vector<short>> dp(...);       // 2 bytes if values fit in ±32,767
std::vector<std::vector<char>>  dp(...);       // 1 byte for booleans or tiny values
std::vector<std::bitset<10001>> dp(n + 1);     // 1 BIT per cell, for reachability
```

A `bitset` of 10,001 bits is 1,252 bytes, so 10^4 rows is 12.5 MB where `vector<vector<bool>>`
would be similar but far slower, and `vector<vector<int>>` would be 400 MB.

### Top-down, done properly

```cpp
std::vector<std::vector<int>> memo;
std::vector<int> weight, value;

int solve(int i, int cap) {
    if (i < 0 || cap == 0) return 0;               // base case
    int& best = memo[i][cap];                       // a reference: read and write one cell
    if (best != -1) return best;                    // already known
    best = solve(i - 1, cap);                       // skip this item
    if (weight[i] <= cap)
        best = std::max(best, solve(i - 1, cap - weight[i]) + value[i]);
    return best;
}
```

`int& best = memo[i][cap];` is the idiom worth stealing. It names the cell once, so you cannot
accidentally write to `memo[i][cap]` and read from `memo[i][cap-1]` — a real bug that is invisible
in a wall of subscripts.

### Bottom-up, and then rolled

```cpp
// full table: O(n x W) memory
int knapsack_2d(const std::vector<int>& w, const std::vector<int>& v, int W) {
    int n = w.size();
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(W + 1, 0));
    for (int i = 1; i <= n; i++)
        for (int j = 0; j <= W; j++) {
            dp[i][j] = dp[i - 1][j];                              // skip item i
            if (w[i - 1] <= j)
                dp[i][j] = std::max(dp[i][j], dp[i - 1][j - w[i - 1]] + v[i - 1]);
        }
    return dp[n][W];
}

// one row, backwards: O(W) memory, same answer
int knapsack_1d(const std::vector<int>& w, const std::vector<int>& v, int W) {
    std::vector<int> dp(W + 1, 0);
    for (size_t i = 0; i < w.size(); i++)
        for (int j = W; j >= w[i]; j--)                           // BACKWARDS
            dp[j] = std::max(dp[j], dp[j - w[i]] + v[i]);
    return dp[W];
}
```

Same answer, and the second uses 1/n of the memory. Note `j >= w[i]` in the loop condition, which
removes the need for a bounds check inside — a small thing that also makes it faster.

### The complete program

```cpp
// dp.cpp — DP tables in C++, and the five bugs that are left.
//   g++ -std=c++20 -O2 -Wall -Wextra -o dp dp.cpp && ./dp

#include <bits/stdc++.h>
using namespace std;

// ---------- top-down, with a sentinel ----------
vector<vector<int>> memo;
vector<int> W_, V_;

int solve(int i, int cap) {
    if (i < 0 || cap == 0) return 0;
    int& best = memo[i][cap];              // name the cell once
    if (best != -1) return best;
    best = solve(i - 1, cap);
    if (W_[i] <= cap) best = max(best, solve(i - 1, cap - W_[i]) + V_[i]);
    return best;
}

// ---------- bottom-up, full table ----------
int knapsack_2d(const vector<int>& w, const vector<int>& v, int W) {
    int n = (int)w.size();
    vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
    for (int i = 1; i <= n; i++)
        for (int j = 0; j <= W; j++) {
            dp[i][j] = dp[i - 1][j];
            if (w[i - 1] <= j)
                dp[i][j] = max(dp[i][j], dp[i - 1][j - w[i - 1]] + v[i - 1]);
        }
    return dp[n][W];
}

// ---------- bottom-up, one row, backwards ----------
int knapsack_1d(const vector<int>& w, const vector<int>& v, int W) {
    vector<int> dp(W + 1, 0);
    for (size_t i = 0; i < w.size(); i++)
        for (int j = W; j >= w[i]; j--)                 // backwards: each item once
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    return dp[W];
}

// ---------- the unbounded version: the SAME loop, forwards ----------
int unbounded(const vector<int>& w, const vector<int>& v, int W) {
    vector<int> dp(W + 1, 0);
    for (size_t i = 0; i < w.size(); i++)
        for (int j = w[i]; j <= W; j++)                 // forwards: each item any number
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    return dp[W];
}

// ---------- counting: long long, because counts explode ----------
long long ways_to_climb(int n) {
    vector<long long> dp(n + 1, 0);
    dp[0] = 1;
    for (int i = 1; i <= n; i++) {
        dp[i] = dp[i - 1];
        if (i >= 2) dp[i] += dp[i - 2];
    }
    return dp[n];
}

// ---------- minimising: 1e18, not INT_MAX ----------
long long min_coins(const vector<int>& coins, int target) {
    const long long INF = 1e18;                 // room to add without overflowing
    vector<long long> dp(target + 1, INF);
    dp[0] = 0;
    for (int j = 1; j <= target; j++)
        for (int c : coins)
            if (c <= j && dp[j - c] != INF)     // guard: never add to INF
                dp[j] = min(dp[j], dp[j - c] + 1);
    return dp[target] == INF ? -1 : dp[target];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<int> w = {2, 3, 4, 5};
    vector<int> v = {3, 4, 5, 6};
    int W = 5;

    W_ = w; V_ = v;
    memo.assign(w.size(), vector<int>(W + 1, -1));      // reset before EVERY run
    cout << "top-down    " << solve((int)w.size() - 1, W) << "\n";
    cout << "2D table    " << knapsack_2d(w, v, W) << "\n";
    cout << "1D backward " << knapsack_1d(w, v, W) << "\n";
    cout << "unbounded   " << unbounded(w, v, W) << "   (same loop, forwards)\n";

    cout << "ways to climb 50 stairs: " << ways_to_climb(50) << "\n";
    cout << "  in an int that would be: " << (int)ways_to_climb(50) << "   (overflowed)\n";

    cout << "min coins for 11 from {1,5,6,9}: "
         << min_coins({1, 5, 6, 9}, 11) << "\n";

    // ---- the memset trap, demonstrated ----
    int arr[4];
    memset(arr, 1, sizeof arr);
    cout << "memset(arr, 1, ...) gives arr[0] = " << arr[0] << "   (not 1)\n";
    memset(arr, -1, sizeof arr);
    cout << "memset(arr, -1, ...) gives arr[0] = " << arr[0] << "   (this one works)\n";
    memset(arr, 0x3f, sizeof arr);
    cout << "memset(arr, 0x3f, ...) gives arr[0] = " << arr[0] << "   (a safe infinity)\n";

    return 0;
}
```

Expected output:

```
top-down    7
2D table    7
1D backward 7
unbounded   7   (same loop, forwards)
ways to climb 50 stairs: 20365011074
  in an int that would be: -1109825534   (overflowed)
min coins for 11 from {1,5,6,9}: 2
memset(arr, 1, ...) gives arr[0] = 16843009   (not 1)
memset(arr, -1, ...) gives arr[0] = -1   (this one works)
memset(arr, 0x3f, ...) gives arr[0] = 1061109567   (a safe infinity)
```

Two lines there are the whole lesson. `ways to climb 50 stairs` is 2 × 10^10, which does not fit in
an `int` — counting problems overflow far earlier than people expect, and 50 is not a large input.
And `memset(arr, 1, ...)` giving 16,843,009 is the byte-fill rule made visible.

---

## 6. What it costs

### Memory: the table that does not fit

The arithmetic to do **before** writing the allocation:

```
  cells x bytes per cell = total

  int   4 bytes      long long  8 bytes
  short 2 bytes      char       1 byte       bitset  1 BIT

  common shapes, in int:

    1000 x 1000    =  10^6 cells  x 4  =    4 MB      fine
    5000 x 5000    = 2.5x10^7     x 4  =  100 MB      fits in 256 MB, just
    10^4 x 10^4    =  10^8        x 4  =  400 MB      DOES NOT FIT
    100 x 100 x 100 = 10^6        x 4  =    4 MB      fine
    100 x 1000 x 1000 = 10^8      x 4  =  400 MB      no
```

**10^8 cells is the wall.** Any table with more than about 6 × 10^7 `int` cells will not fit in a
256 MB limit, and that is the number to carry.

When it does not fit:

```
  same 10^4 x 10^4 table:

    as int      400 MB    no
    as short    200 MB    maybe, if values fit in +-32,767
    as char     100 MB    yes, for booleans or values under 128
    as bitset    12.5 MB  yes, for pure reachability (true/false)
    rolled to 2 rows,
      as int      80 KB   yes — and this is almost always the real answer
```

Rolling is worth two orders of magnitude more than shrinking the type. Look for it first.

### Time

```
  a DP with S states and T transitions per state = O(S x T) operations
  at ~10^8 simple operations per second:

    S = 10^6, T = 1     ->  10^6      ->  0.01 s
    S = 10^6, T = 100   ->  10^8      ->  1.0 s      tight
    S = 10^7, T = 10    ->  10^8      ->  1.0 s      tight
    S = 10^8, T = 1     ->  10^8      ->  1.0 s      and 400 MB. no.
```

**The state count is usually bounded by memory before it is bounded by time**, which is why the
memory sum comes first.

### Top-down versus bottom-up, measured

```
  the same DP, 10^7 states

  bottom-up, plain loops                  ~0.09 s
  top-down, recursion + memo              ~0.55 s     6x slower
  top-down with vector<vector<int>>       ~0.70 s     the nested indirection costs too
  bottom-up with a flat 1D array          ~0.06 s     index as i*cols + j
```

The gap comes from three places: a function call per state, the recursion's stack traffic, and
`vector<vector<int>>` being a vector of *pointers* to separate blocks, so `dp[i][j]` is two memory
lookups and the rows are scattered.

For a hot 2D table, flattening is a real and easy win:

```cpp
std::vector<int> dp((rows + 1) * (cols + 1), 0);
// dp[i * (cols + 1) + j]  instead of  dp[i][j]
```

One contiguous block, one lookup, and the prefetcher works. Uglier, and roughly 30% faster.

**But write it clearly first.** The clear version passes most of the time, and a wrong fast
solution scores nothing.

---

## 7. The traps

These five are the ones left after everything else in this track. They are the reason a correct
recurrence still fails.

### The one that costs the most: not resetting between test cases

```cpp
const int MAXN = 100005;
int dp[MAXN];

int main() {
    int t;
    cin >> t;
    memset(dp, -1, sizeof dp);      // cleared ONCE, outside the loop
    while (t--) {
        int n;
        cin >> n;
        cout << solve(n) << "\n";   // case 2 reads case 1's answers
    }
}
```

First test case: correct. Every one after it: built on numbers computed for different input. This
is Ravi's underpass — the values are not garbage, they are *stale*, which is exactly why nothing
looks wrong.

The symptom is unmistakable once you know it: **the first sample passes and the second does not,
but running the second alone also passes.** If you see that, you have a reset bug.

Two fixes. Declare the table inside the loop, so it cannot be forgotten. Or clear only the part you
used, at the top of each case:

```cpp
while (t--) {
    cin >> n;
    fill(dp, dp + n + 1, -1);       // only 0..n. Clearing all of MAXN each time is a timeout.
}
```

### The near-miss: `INT_MAX` plus anything

```cpp
vector<int> dp(target + 1, INT_MAX);
dp[j] = min(dp[j], dp[j - c] + 1);        // when dp[j-c] is INT_MAX, +1 overflows
```

`INT_MAX + 1` is undefined behaviour, and in practice wraps to `INT_MIN` — a large negative number.
`min` then picks it happily, and your minimisation returns a negative answer, or a wildly small one
that looks almost plausible.

Two fixes, both used:

```cpp
const long long INF = 1e18;                       // room to add without overflowing
if (dp[j - c] != INF) dp[j] = min(dp[j], dp[j - c] + 1);   // or just guard it
```

`1e18` in a `long long` leaves nine orders of magnitude of headroom. `0x3f3f3f3f` — about
1.06 × 10^9 — is the `int` equivalent, chosen precisely because you can add two of them without
overflowing.

### The near-miss: the counting DP that overflows

```cpp
vector<int> dp(n + 1, 0);       // counting ways, in an int
```

The program above shows it: fifty stairs gives 2 × 10^10 ways, and an `int` stops at 2 × 10^9. The
input was fifty. Counting problems produce enormous numbers from tiny inputs, which is precisely
why so many of them say "modulo 10^9 + 7".

**Counting DP tables are `long long`, or they are reduced modulo something.** No exceptions.

### The real error: the table that does not fit

```cpp
vector<vector<int>> dp(10001, vector<int>(10001, 0));
```

```
terminate called after throwing an instance of 'std::bad_alloc'
  what():  std::bad_alloc
Aborted (core dumped)
```

`std::bad_alloc` means the allocation was refused. On a judge it is a memory-limit verdict. Do the
multiplication before you write the line: 10001 × 10001 × 4 = 400 MB.

And the subtler version — the table fits but the *indices* are the wrong way round:

```cpp
vector<vector<int>> dp(n, vector<int>(m, 0));
dp[j][i] = ...;                              // j goes up to m, i up to n. Swapped.
```

If `m > n` this reads past the end. Silently.

```
=================================================================
==31402==ERROR: AddressSanitizer: container-overflow on address 0x619000000d10
WRITE of size 4 at 0x619000000d10 thread T0
    #0 0x4015b8 in main dp.cpp:31
```

### The real error: memoised recursion that goes too deep

A top-down DP over 10^6 states in a chain recurses 10^6 deep, and
[day 125](../day-125-what-a-graph-is/04-cpp-graphs-and-recursion.md) has the arithmetic: about
130,000 frames on an 8 MB stack.

```
AddressSanitizer:DEADLYSIGNAL
==31877==ERROR: AddressSanitizer: stack-overflow on address 0x7ffe3c1fdff8
    #0 0x4013a1 in solve(int, int) dp.cpp:14
    #1 0x4013f2 in solve(int, int) dp.cpp:17
    #2 0x4013f2 in solve(int, int) dp.cpp:17
```

The same repeating frame is the signature. **Convert to bottom-up.** For DP that is usually easy —
the recurrence is the same, you only have to work out the fill order — and it removes the call
overhead as well.

---

## 8. In the interview

### How it gets asked

- *"Write the knapsack."* — and then, always, *"can you do it in less space?"*
- *"How much memory does your DP use?"* — asked the moment you write a two-dimensional table.
- *"Top-down or bottom-up, and why?"* — where a good answer names a trade rather than a
  preference.
- *"Your solution passes sample 1 and fails sample 2."* — the diagnostic version, and the answer is
  the reset.

### What to say out loud, in the first ninety seconds

1. **State the table.** *"`vector<vector<int>> dp(n+1, vector<int>(W+1, 0))` — dp[i][j] is the best
   value using the first i items with capacity j."*
2. **Do the memory arithmetic out loud.** *"That is (n+1) × (W+1) × 4 bytes. With n and W at 10^4
   that is 400 MB, which will not fit a 256 MB limit — so I would want the rolled version."*
3. **Give the roll.** *"Each row only reads the row above, so I keep one row and iterate capacity
   downwards. That is O(W) memory instead of O(n × W)."*
4. **Say why backwards.** *"Backwards so that `dp[j - w]` is still the previous row's value.
   Forwards would let me use the same item twice — which is the unbounded knapsack, a different
   problem."*
5. **Name the type risks.** *"I would use `long long` if this were counting rather than maximising,
   because counts overflow an `int` very fast, and I would use 1e18 rather than INT_MAX as infinity
   so adding to it does not overflow."*
6. **Name the reset.** *"And with multiple test cases I declare the table inside the loop, or clear
   only the used prefix — a stale table gives a right first answer and quiet nonsense afterwards."*

Step 2 is the one that changes the interviewer's opinion of you. Doing the memory arithmetic before
being asked is what a person who has actually hit the limit does.

### The follow-ups

**"Top-down or bottom-up — which and why?"**
I usually write top-down first, because it follows the recurrence directly and I only have to get
the base cases and the memo right, not the fill order. Then I convert to bottom-up if I need the
speed or the depth. Bottom-up is roughly five times faster on a large table, because there is no
function call per state and no stack traffic, and it has no recursion depth at all — a top-down DP
over 10^6 chained states will blow the 8 MB stack and segfault with no message. Top-down does have
one real advantage: it only computes the states it actually reaches. If the reachable set is a
small fraction of the table, top-down can be dramatically faster despite the overhead, and that is
the case where I would keep it.

**"Your DP is correct but memory-limit exceeded. What do you do?"**
Look for the roll first, because it is worth the most. If each state only reads the previous row or
the previous k rows, I keep those and drop the rest — that turns O(n × W) into O(W), which is
usually two or three orders of magnitude. If I still need the full table, I shrink the cell:
`short` if values fit in ±32,767, `char` for small values, and `std::bitset` for pure reachability,
which is one bit per cell and turns 400 MB into 12 MB. If I need the actual chosen items and not
just the value, rolling destroys that — so I would either store a compact parent decision, or use
the divide-and-conquer reconstruction that recomputes halves, which is O(n log n) time for O(W)
space.

**"Why does the 0/1 knapsack loop backwards?"**
Because the one-row version is a compressed two-row version, and `dp[j]` before I write to it still
holds row i−1's value. When I read `dp[j - w]`, I need that to also still be row i−1 — meaning it
must not have been updated yet in this pass. Iterating j downwards guarantees that, because
`j - w` is smaller than `j` and I have not reached it. Iterating upwards means `dp[j - w]` was
already updated this round, so the item gets used a second time — which is exactly the unbounded
knapsack. So the same three lines solve two different problems and the loop direction is the only
difference, which is a nice thing to be able to say.

**"Sample 1 passes and sample 2 fails. Where would you look?"**
A stale table between test cases, first, before anything else. It is the classic signature: each
case alone is correct, and the second case in sequence is not. Either the memo was cleared once
outside the loop, or a global accumulator was not reset. The fix is to declare the state inside the
loop so it cannot be forgotten. The related mistake is clearing the whole `MAXN` array on every
case — correct, but if there are 10^5 cases and MAXN is 10^5, that is 10^10 writes and you have
turned a wrong answer into a timeout. Clear only the prefix you used.

### A model answer

The interviewer has the candidate's 2D knapsack on screen and asks about the space.

> "It is O(n × W). The table is (n+1) by (W+1) `int`s, so at n = 10^4 and W = 10^4 that is 10^8
> cells, four hundred megabytes. That will not fit a 256 MB limit, so this version is only right
> for small W.
>
> The fix is to roll it. Look at the recurrence — `dp[i][j]` reads `dp[i-1][j]` and
> `dp[i-1][j - w[i]]`, both from the row directly above and never from the current row. So I never
> need more than two rows alive at once, and in fact I can do it with one:
>
> ```cpp
> vector<int> dp(W + 1, 0);
> for (int i = 0; i < n; i++)
>     for (int j = W; j >= w[i]; j--)
>         dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
> ```
>
> That is O(W) memory — forty kilobytes instead of four hundred megabytes — and the time is
> unchanged at O(n × W).
>
> The capacity loop has to run backwards, and that is the part worth being explicit about. Before I
> write `dp[j]`, it still holds the previous row's value, and I need `dp[j - w[i]]` to still be the
> previous row's too. Going downwards, `j - w[i]` is a cell I have not reached yet this pass, so it
> is untouched. If I went upwards, `dp[j - w[i]]` would already have been updated with item i, and
> I would be allowed to use the same item twice — which is the unbounded knapsack. Same three
> lines, opposite loop direction, different problem.
>
> Two things I would flag. Rolling loses the ability to reconstruct *which* items were chosen,
> because the earlier rows are gone — if the problem asks for the set and not just the value, I
> would keep the full table if it fits, or use the divide-and-conquer reconstruction, which costs
> an extra log factor in time to keep the linear space.
>
> And if this were a counting problem rather than a maximising one, the cells would have to be
> `long long`. Counts get very large from small inputs — the number of ways to climb fifty stairs
> is already 2 × 10^10, past an `int` — which is why so many of these problems ask for the answer
> modulo 10^9 + 7."

That answer gives the complexity, does the arithmetic in real units, gives the optimisation and its
exact code, explains the non-obvious loop direction from first principles, connects it to a
neighbouring problem, and names two things the optimisation costs.

---

## 9. Recall card

1. **`vector<vector<int>> dp(rows+1, vector<int>(cols+1, init))`.** Do the arithmetic before you
   write it: **10^8 cells × 4 bytes = 400 MB and it will not fit.** 6 × 10^7 ints is the practical
   wall.
2. **The initial value carries meaning.** `0` for counting, `-1` for "not computed", `1e18` for
   infinity — never `INT_MAX`, because adding to it overflows.
3. **Roll the table when each row reads only the row above.** O(n × W) becomes O(W). For 0/1
   knapsack, one row filled **backwards**; forwards is the unbounded problem.
4. **Reset between test cases**, and clear only the prefix you used. First sample right, second
   wrong, but right when run alone — that is always a stale table.
5. **Counting DP is `long long`.** 50 stairs is already 2 × 10^10. And `memset` sets *bytes* — only
   0, −1 and 0x3f do what you want.

---

## Where this track ends

That is the tenth and last C++ day. You now have, across ten lessons:

- **[Day 001](../day-001-how-your-code-actually-runs/04-cpp-compiling-and-running.md)** — compiling
  and running.
- **[Day 002](../day-002-counting-steps/04-cpp-types-numbers.md)** — types and overflow.
- **[Day 003](../day-003-big-o-in-plain-english/04-cpp-input-output.md)** — fast I/O, the template,
  and the constraint-to-complexity table.
- **[Day 005](../day-005-python-lists-and-tuples/04-cpp-vector-references.md)** — `vector` and
  references.
- **[Day 006](../day-006-python-strings-dicts-sets/04-cpp-string-map-set.md)** — `string`, `map`,
  `set`, `pair`.
- **[Day 042](../day-042-binary-search-idea/04-cpp-sort-lambdas.md)** — `sort`, lambdas,
  `lower_bound`.
- **[Day 068](../day-068-stacks/04-cpp-stack-queue-deque.md)** — the four adapters and the heap.
- **[Day 078](../day-078-nodes-and-links/04-cpp-structs-pointers.md)** — structs, pointers,
  ownership.
- **[Day 125](../day-125-what-a-graph-is/04-cpp-graphs-and-recursion.md)** — graphs, DSU, recursion
  depth.
- **Day 143** — DP tables and the remaining traps.

That is enough C++ to solve any problem in this course and to compete. What it is not is enough C++
to pass a C++-specific design round — classes, RAII, virtual functions, smart pointer ownership and
the design patterns in C++ are a separate body of work, and the course teaches those ideas in the
system design track from [day 043](../day-043-binary-search-without-bugs/README.md) onwards, in
Python. If your interviews are in C++, translate those days as you go, the same way this track has
you translating the DSA days.

For contest practice: Codeforces Div. 3 and Div. 4 rounds first, then Div. 2 A and B. AtCoder
Beginner Contests are gentler and better written. Do them with the template from
[day 003](../day-003-big-o-in-plain-english/04-cpp-input-output.md), read the constraint before you
read the statement, and compile locally with `-fsanitize=address,undefined` every single time.
