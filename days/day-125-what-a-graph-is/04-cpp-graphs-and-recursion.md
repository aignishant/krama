---
day: 125
track: cpp
title: "Graphs and recursion in C++: adjacency lists, depth, and DSU"
phase: "C++ and competitive programming"
status: written
---

# Day 125 · C++ — Graphs and recursion in C++: adjacency lists, depth, and DSU

**After today you can:** You can build an adjacency list, run BFS and DFS with the STL, and say why a deep recursion crashes in C++ where Python only raises.

**The interviewer asks it as:** *How do you represent a graph in C++, and what breaks when the recursion goes deep?*

---

> Ninth of the twelve C++ days. Everything from here to day 170 — graphs, trees revisited, shortest
> paths, dynamic programming on graphs — is built on the three lines in section 5. And this is the
> day you learn the one way C++ fails that Python does not.

---

## 1. What this is, and why they ask it

A graph in C++ is one line: `vector<vector<int>> adj(n)`. For each thing, the list of things it
connects to. Everything else — breadth-first search, depth-first search, shortest paths, cycle
detection, connected components — is a loop over that structure, and the container work is done by
`queue`, `priority_queue` and plain recursion, all of which you already have.

The part that is genuinely different from Python is depth. Python has a recursion limit of about a
thousand, and when you exceed it you get a `RecursionError` — a clean exception, with a traceback,
naming the problem. C++ has no limit at all. It just keeps pushing stack frames until the stack
runs out of memory, and then the program dies with `Segmentation fault` and no explanation
whatsoever. On a graph shaped like a long chain — which is a perfectly ordinary test case — a
recursive depth-first search on 10^5 vertices will do exactly that.

Interviewers ask about the representation because the choice between an adjacency list and a
matrix is a memory question with an obvious wrong answer at scale. They ask about depth because
knowing that C++ will crash rather than complain, and knowing the two fixes, is the difference
between a solution that passes and one that fails on test 30 with no diagnosis.

---

## 2. The story

Sushila is at a wedding in Nashik, in the courtyard, in the gap after lunch when nothing is
happening and the band has stopped for an hour. There is a man of about fifty standing near the
water pots whom she is certain she has met, and she cannot place him at all.

So she starts working it out, the way everybody does at a wedding.

She asks the woman next to her, who says he came with the bride's side, and that his wife is the
one in the green sari, and that the woman in the green sari is somebody's cousin. Sushila follows
it. Green sari's mother's younger brother married a woman from Manmad, and that woman's sister is
married to somebody Sushila's own father used to work with.

Around the sixth step she loses it.

Not the current step — she knows exactly who she is standing on. What she has lost is the way
back. She cannot remember whether the man from Manmad was on the mother's side or the father's
side, and she cannot remember it because she has been holding five other half-remembered links in
her head at the same time and one of them has fallen out. She has to go back to the woman next to
her and start again.

The second time she does it differently, and it works.

She asks everyone at her own table, all six of them, whether they know him. Two do, a little. She
asks those two who else would know, and gets four names, and she goes and asks those four. It is
more walking and more conversations. But at no point is she holding more than one question in her
head: who is this, and who might know.

It takes about eleven minutes and she gets it. He taught at her brother's school for two years in
the nineties and she met him twice at a sports day.

What she says to her sister afterwards is that the second way was not cleverer. It was that the
first way asked her to remember every step she had taken, and she is fifty-three and there was a
band. The second way asked her to remember nothing at all except who to ask next, and there was
always somebody standing there to ask.

---

## 3. The idea in plain English

### The adjacency list

```cpp
int n;                              // how many vertices
std::vector<std::vector<int>> adj(n);   // for each one, who it connects to
```

`adj[u]` is a `vector<int>` holding every vertex `u` connects to. That is it. That is a graph in
C++, and you will type that line more than any other for the next fifty days.

Reading it in, for an undirected graph:

```cpp
int m;                              // how many edges
std::cin >> n >> m;
std::vector<std::vector<int>> adj(n);
for (int i = 0; i < m; i++) {
    int u, v;
    std::cin >> u >> v;
    u--; v--;                       // judges usually number from 1; C++ counts from 0
    adj[u].push_back(v);
    adj[v].push_back(u);            // both directions. Omit this line if directed.
}
```

The `u--; v--;` is the small thing that costs people whole contests. Problems number vertices from
1, C++ counts from 0, and the mismatch shows up as an out-of-range read at the far end of the
program. Convert once, at the point of reading, and never think about it again.

With weights, the neighbour is a pair:

```cpp
std::vector<std::vector<std::pair<int,int>>> adj(n);   // (neighbour, weight)
adj[u].push_back({v, w});
```

### Why not a matrix

The other representation is a two-dimensional table where `mat[u][v]` is 1 if there is an edge.

```cpp
std::vector<std::vector<int>> mat(n, std::vector<int>(n, 0));
```

It answers "is there an edge from u to v" in O(1), which the list answers in O(degree). And it
costs O(V²) memory whether or not the edges exist.

```
  V = 1000:    10^6 ints  =  4 MB       fine
  V = 10^5:    10^10 ints =  40 GB      impossible
```

**Use the list.** Real graphs are sparse — a road network, a social network, a dependency graph
all have a few edges per vertex, not V of them. Use a matrix only when V is small, under about a
thousand, and you genuinely need the O(1) edge test — Floyd-Warshall being the standard case.

### BFS is Sushila's second attempt

Breadth-first search visits everything one step away, then everything two steps away, and so on.
It uses a `queue`, and it holds nothing in its head except who to ask next.

```cpp
std::vector<int> dist(n, -1);            // -1 means "not reached"
std::queue<int> q;
dist[start] = 0;
q.push(start);

while (!q.empty()) {
    int u = q.front();
    q.pop();
    for (int v : adj[u]) {
        if (dist[v] == -1) {             // not seen before
            dist[v] = dist[u] + 1;
            q.push(v);
        }
    }
}
```

Because it expands in rings, **the first time BFS reaches a vertex is by a shortest path**, when
every edge counts the same. That is the whole reason it exists.

Mark `dist[v]` at the moment you **push**, not when you pop. Marking on pop lets the same vertex
be queued several times before it is first popped, and the queue blows up. This is the most common
BFS bug there is.

### DFS is Sushila's first attempt, and it can fall over

Depth-first search follows one path as far as it goes, then backs up and tries the next branch.

```cpp
std::vector<bool> seen(n, false);

void dfs(int u) {
    seen[u] = true;
    for (int v : adj[u])
        if (!seen[v]) dfs(v);
}
```

Four lines, and it is beautiful, and on a large graph it can crash.

Each call to `dfs` puts a **stack frame** on the call stack — space for its parameters, its
locals, and the address to return to. The frames stack up as you go deeper, and they only come off
as you come back. Sushila holding five half-remembered links is five stack frames.

**The stack has a fixed size, and C++ does not check.** On Linux the default is 8 MB. A frame for
that `dfs` is perhaps 48 to 80 bytes with the loop's iterator in it, so:

```
  8 MB / 64 bytes per frame  ≈  130,000 frames
```

A graph that is one long chain of 10^5 vertices — a perfectly ordinary test — recurses 10^5 deep
and lands right on that boundary. A chain of 10^6 is far past it.

This is the difference from Python that matters. Python counts the frames and raises
`RecursionError: maximum recursion depth exceeded` — an exception you can see, catch and read.
C++ counts nothing. It writes past the end of the stack, the operating system notices the page
fault, and you get:

```
Segmentation fault (core dumped)
```

No line number. No mention of depth. On a judge, a runtime error verdict on test 30 and nothing
else.

### The two fixes

**One — raise the stack.** Locally:

```
ulimit -s unlimited        # then run your program in the same shell
```

Codeforces gives 256 MB of stack, equal to the memory limit, so deep recursion is safe there and
this is a non-issue. Many other judges give you the default 8 MB and it is not.

**Two — write it iteratively, with your own stack.** This always works and depends on nothing:

```cpp
void dfs_iterative(int start, const std::vector<std::vector<int>>& adj,
                   std::vector<bool>& seen) {
    std::stack<int> st;
    st.push(start);
    seen[start] = true;
    while (!st.empty()) {
        int u = st.top();
        st.pop();
        for (int v : adj[u])
            if (!seen[v]) { seen[v] = true; st.push(v); }
    }
}
```

The heap is limited by the memory limit — 256 MB — not by the 8 MB stack, so this handles a
million-deep chain without complaint. The cost is that it visits children in reverse order
compared with the recursive version, and that post-order work (doing something *after* the
children) becomes fiddly and needs a second pass or a state marker.

**The practical rule:** recursive DFS when the depth is bounded and small — a tree of depth 20, a
grid of 1000 × 1000 where you cannot recurse more than 10^6 but usually far less. Iterative when
the graph could be a long chain and the judge's stack is unknown.

### Disjoint Set Union, in fifteen lines

[Day 138](../day-138-union-find/README.md) explains why it works. This is the code, and it is
short enough to memorise:

```cpp
struct DSU {
    std::vector<int> parent, size;

    DSU(int n) : parent(n), size(n, 1) {
        for (int i = 0; i < n; i++) parent[i] = i;      // everyone is their own group
    }

    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);  // path compression
        return parent[x];
    }

    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;                       // already together
        if (size[a] < size[b]) std::swap(a, b);         // union by size
        parent[b] = a;
        size[a] += size[b];
        return true;
    }
};
```

Path compression plus union by size gives you **O(α(n))** per operation, where α is the inverse
Ackermann function and is less than 5 for any n you will ever meet. Treat it as constant.

Note that `find` is recursive. On 10^6 elements the recursion depth after compression is tiny, but
before any compression has happened a pathological chain could be deep — so if you are nervous,
the iterative version is four lines and is in the complete program below.

---

## 4. The picture

The adjacency list, drawn as it actually sits in memory:

```
  graph:   0 --- 1 --- 3
           |     |
           2     4

  adj  (a vector of 5 vectors)

  adj[0] -> [ 1, 2 ]
  adj[1] -> [ 0, 3, 4 ]
  adj[2] -> [ 0 ]
  adj[3] -> [ 1 ]
  adj[4] -> [ 1 ]

  memory:  5 vector objects (24 bytes each), each pointing at its own small block
           total edges stored = 2 x number of edges, because undirected

  the same graph as a matrix, for comparison:

        0  1  2  3  4
     0 [ 0  1  1  0  0 ]
     1 [ 1  0  0  1  1 ]        25 cells to store 4 edges.
     2 [ 1  0  0  0  0 ]        at V = 10^5 that is 10^10 cells.
     3 [ 0  1  0  0  0 ]
     4 [ 0  1  0  0  0 ]
```

**What to notice:** the list stores what exists. The matrix stores what might exist. That is the
whole argument, and it is why every competitive graph problem uses the list.

The two searches, on the same graph:

```
  BFS from 0                          DFS from 0

  ring 0:  0                          0
  ring 1:  1, 2                        \
  ring 2:  3, 4                         1
                                         \
  queue:   [0] [1,2] [2,3,4] [3,4] ...    3   <- goes all the way down first
                                          |
  holds a whole ring at once,             (back up)
  but nothing about how it got there      4
                                        2

                                      holds the PATH — every step back to 0
```

**What to notice:** BFS's memory is the width of the graph; DFS's is the depth. That is why a long
thin graph is fine for BFS and fatal for recursive DFS, and a wide flat graph is the other way
round.

And the stack overflow:

```
  the call stack, growing downwards

     +-------------------+  <- top of the stack region
     | main's frame      |
     +-------------------+
     | dfs(0)   ~64 B    |
     +-------------------+
     | dfs(1)   ~64 B    |
     +-------------------+
     | dfs(2)            |
     +-------------------+
              .
              .            8 MB / 64 B  ≈  130,000 frames
              .
     +-------------------+
     | dfs(129999)       |
     +-------------------+
     | dfs(130000)       |  <- writes past the end of the stack region
     +===================+
     |  NOT YOUR MEMORY  |     SIGSEGV.  "Segmentation fault (core dumped)"
     +-------------------+     No line number. No message about depth.
```

**What to notice:** nothing counted. There is no limit being enforced and no check being failed —
the program simply walked off the end of a region the operating system had given it. Python's
`RecursionError` exists precisely because a counter was kept; C++ keeps none.

---

## 5. The code, built step by step

### Grids are graphs

Every island, flood-fill and maze problem is a graph where the neighbours are computed rather than
stored. [Day 130](../day-130-grids-are-graphs/README.md) is the reasoning; this is the C++ idiom:

```cpp
const int dr[4] = {-1, 1, 0, 0};
const int dc[4] = {0, 0, -1, 1};

for (int k = 0; k < 4; k++) {
    int nr = r + dr[k];
    int nc = c + dc[k];
    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;   // off the edge
    // ... visit (nr, nc)
}
```

Two small arrays and one bounds check. For eight directions, extend both arrays to
`{-1,-1,-1,0,0,1,1,1}` and `{-1,0,1,-1,1,-1,0,1}`. **Write the bounds check first**, before you
touch `grid[nr][nc]`, because reading out of range is undefined behaviour and not an error.

### Dijkstra, with the heap from day 068

```cpp
std::vector<long long> dijkstra(int start, const std::vector<std::vector<std::pair<int,int>>>& adj) {
    const long long INF = 1e18;
    std::vector<long long> dist(adj.size(), INF);
    std::priority_queue<std::pair<long long,int>,
                        std::vector<std::pair<long long,int>>,
                        std::greater<>> pq;          // min-heap of (distance, vertex)
    dist[start] = 0;
    pq.push({0, start});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;                   // a stale entry — skip it
        for (auto [v, w] : adj[u]) {
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

Three things in there are load-bearing.

`long long` for the distances, because a path of 10^5 edges of weight 10^9 sums to 10^14 and an
`int` stops at 2 × 10^9 — this is [day 002's bug](../day-002-counting-steps/04-cpp-types-numbers.md)
in its most common disguise.

`std::greater<>` with empty angle brackets is C++14's "work the type out", which saves writing the
pair type a third time.

And `if (d > dist[u]) continue;` is **lazy deletion**. C++'s `priority_queue` cannot lower the key
of an entry already in it, so instead you push a second, better entry and ignore the old one when
it surfaces. Without that line the algorithm still gives the right answer but does far more work.
This is the standard C++ Dijkstra and the reason it looks different from the textbook version.

### The complete program

```cpp
// graphs.cpp — the adjacency list, both searches, DSU, and the depth problem.
//   g++ -std=c++20 -O2 -Wall -Wextra -o graphs graphs.cpp && ./graphs

#include <bits/stdc++.h>
using namespace std;

// ---------- breadth-first: shortest path in edges ----------
vector<int> bfs(int start, const vector<vector<int>>& adj) {
    vector<int> dist(adj.size(), -1);
    queue<int> q;
    dist[start] = 0;
    q.push(start);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : adj[u])
            if (dist[v] == -1) {          // mark on PUSH, never on pop
                dist[v] = dist[u] + 1;
                q.push(v);
            }
    }
    return dist;
}

// ---------- depth-first, recursive: fine when the depth is bounded ----------
void dfs_rec(int u, const vector<vector<int>>& adj, vector<char>& seen) {
    seen[u] = 1;
    for (int v : adj[u])
        if (!seen[v]) dfs_rec(v, adj, seen);
}

// ---------- depth-first, iterative: safe at any depth ----------
void dfs_iter(int start, const vector<vector<int>>& adj, vector<char>& seen) {
    stack<int> st;
    st.push(start);
    seen[start] = 1;
    while (!st.empty()) {
        int u = st.top();
        st.pop();
        for (int v : adj[u])
            if (!seen[v]) { seen[v] = 1; st.push(v); }
    }
}

// ---------- disjoint set union ----------
struct DSU {
    vector<int> parent, size;
    DSU(int n) : parent(n), size(n, 1) {
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    int find(int x) {                     // iterative: no depth to worry about
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];   // path halving
            x = parent[x];
        }
        return x;
    }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (size[a] < size[b]) swap(a, b);
        parent[b] = a;
        size[a] += size[b];
        return true;
    }
};

// ---------- dijkstra ----------
vector<long long> dijkstra(int start, const vector<vector<pair<int,int>>>& adj) {
    const long long INF = 1e18;
    vector<long long> dist(adj.size(), INF);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    dist[start] = 0;
    pq.push({0, start});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;        // stale entry: lazy deletion
        for (auto [v, w] : adj[u])
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
    }
    return dist;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    //   0 --- 1 --- 3
    //   |     |
    //   2     4
    int n = 5;
    vector<vector<int>> adj(n);
    auto edge = [&](int u, int v) { adj[u].push_back(v); adj[v].push_back(u); };
    edge(0, 1); edge(0, 2); edge(1, 3); edge(1, 4);

    vector<int> d = bfs(0, adj);
    cout << "bfs distances from 0:";
    for (int x : d) cout << " " << x;                 // 0 1 1 2 2
    cout << "\n";

    vector<char> seen(n, 0);
    dfs_rec(0, adj, seen);
    cout << "dfs reached: " << count(seen.begin(), seen.end(), 1) << " of " << n << "\n";

    vector<char> seen2(n, 0);
    dfs_iter(0, adj, seen2);
    cout << "iterative dfs agrees: " << (seen == seen2 ? "yes" : "no") << "\n";

    // ---- connected components with DSU ----
    DSU dsu(n);
    dsu.unite(0, 1); dsu.unite(0, 2); dsu.unite(1, 3); dsu.unite(1, 4);
    int components = 0;
    for (int i = 0; i < n; i++) if (dsu.find(i) == i) components++;
    cout << "components: " << components << "\n";

    // ---- dijkstra on a weighted version ----
    vector<vector<pair<int,int>>> w(n);
    auto wedge = [&](int u, int v, int c) {
        w[u].push_back({v, c}); w[v].push_back({u, c});
    };
    wedge(0, 1, 4); wedge(0, 2, 1); wedge(2, 1, 2); wedge(1, 3, 5);
    vector<long long> dd = dijkstra(0, w);
    cout << "dijkstra from 0: ";
    for (int i = 0; i < 4; i++) cout << dd[i] << " ";  // 0 3 1 8
    cout << "\n";

    // ---- the depth problem, in numbers ----
    cout << "\na chain of 10^5 vertices recurses 10^5 deep.\n";
    cout << "8 MB stack / ~64 bytes per frame = about 130,000 frames.\n";
    cout << "that is the boundary. use dfs_iter, or raise the stack.\n";

    return 0;
}
```

Expected output:

```
bfs distances from 0: 0 1 1 2 2
dfs reached: 5 of 5
iterative dfs agrees: yes
components: 1
dijkstra from 0: 0 3 1 8

a chain of 10^5 vertices recurses 10^5 deep.
8 MB stack / ~64 bytes per frame = about 130,000 frames.
that is the boundary. use dfs_iter, or raise the stack.
```

`dijkstra from 0: 0 3 1 8` — the distance to vertex 1 is 3, not 4, because the route through
vertex 2 costs 1 + 2. That is the whole point of the algorithm, visible in one line of output.

---

## 6. What it costs

### Memory: the representation

```
  V vertices, E edges

  adjacency list:  V vector objects (24 bytes each) + 2E ints (undirected)
  adjacency matrix: V^2 ints

  V = 10^5, E = 2 x 10^5   (a typical contest graph)

    list:    10^5 x 24  +  4 x 10^5 x 4   =  2.4 MB + 1.6 MB  =  4 MB      fits
    matrix:  10^10 x 4                    =  40 GB                          no
```

If you write the matrix version at V = 10^5, the allocation itself fails:

```
terminate called after throwing an instance of 'std::bad_alloc'
  what():  std::bad_alloc
Aborted (core dumped)
```

`std::bad_alloc` means "I asked the operating system for memory and it said no". On a judge it is
a runtime error or a memory-limit verdict.

### Time: the searches

```
  BFS and DFS both visit every vertex once and every edge twice (undirected):
    O(V + E)

  V = 10^5, E = 2 x 10^5  ->  5 x 10^5 operations  ->  ~0.005 s

  Dijkstra with a binary heap:
    O((V + E) log V)  =  (3 x 10^5) x 17  =  5 x 10^6   ->  ~0.05 s

  DSU with path compression and union by size:
    O(α(n)) per operation, α(n) < 5 for any n up to 2^65536.
    10^6 operations  ->  ~0.02 s.  Treat it as constant.
```

### The stack, precisely

This is the number worth carrying:

```
  Linux default stack:               8 MB   (check with: ulimit -s)
  Windows default (MSVC/MinGW):      1 MB   <- four times worse
  Codeforces:                      256 MB   (equal to the memory limit)

  a small dfs frame with a range-for iterator:  ~48-80 bytes

  8 MB   / 64 B  ≈   130,000 frames
  1 MB   / 64 B  ≈    16,000 frames        <- Windows, and it fails early
  256 MB / 64 B  ≈ 4,000,000 frames
```

**A grid flood-fill on 1000 × 1000 can recurse 10^6 deep** in the worst case — a spiral-shaped
region — and that is eight times past the Linux default. Grid problems are where this bites most
often, and it is why experienced competitors write flood fill with an explicit stack or a BFS
queue rather than recursion.

Compare the two searches' memory while running:

```
  BFS:  the queue holds at most one "ring".  On a wide graph that can be O(V).
  DFS:  the stack holds the current path.    On a deep graph that is O(V).

  neither is uniformly better; they fail on opposite shapes.
```

---

## 7. The traps

### The real error: recursing too deep

```cpp
void dfs(int u) {
    seen[u] = true;
    for (int v : adj[u]) if (!seen[v]) dfs(v);
}
// on a chain of 200,000 vertices:
```

```
Segmentation fault (core dumped)
```

That is the whole message. Compile with the address sanitiser and you get the diagnosis:

```
AddressSanitizer:DEADLYSIGNAL
=================================================================
==27431==ERROR: AddressSanitizer: stack-overflow on address 0x7ffc9e7fdff8 (pc 0x0000004012a5 bp 0x7ffc9e7fe030 sp 0x7ffc9e7fdfe0 T0)
    #0 0x4012a4 in dfs(int) graphs.cpp:12
    #1 0x4012e9 in dfs(int) graphs.cpp:14
    #2 0x4012e9 in dfs(int) graphs.cpp:14
    #3 0x4012e9 in dfs(int) graphs.cpp:14
```

The word is `stack-overflow`, and the same two lines repeat down the trace forever. That repetition
is the signature: when a backtrace is the same frame over and over, you have recursed too deep.

Three responses, in order: use the iterative version; raise the stack with `ulimit -s unlimited`
locally; or check whether the judge already gives you a large stack, as Codeforces does.

### The near-miss: `vector<bool>` is not a vector of bools

This is a genuine oddity in the standard library and it catches everybody once.

```cpp
std::vector<bool> seen(n, false);
bool& b = seen[0];              // does not compile
```

```
main.cpp:10:11: error: cannot bind non-const lvalue reference of type 'bool&' to an rvalue of type 'std::_Bit_reference'
   10 |     bool& b = seen[0];
      |               ~~~~~^
```

`vector<bool>` is specialised to store one **bit** per element, so `seen[i]` does not return a
`bool&` — it returns a proxy object. That saves memory (10^6 bools in 125 KB instead of 1 MB) and
costs you the ability to take a reference, plus some speed from the bit masking on every access.

For a visited array, **use `vector<char>`**. It is a real array of bytes, it is faster, and it
behaves the way you expect. Use `vector<bool>` deliberately when the memory saving matters — a
sieve of 10^8, say.

### The near-miss: marking visited on pop

```cpp
while (!q.empty()) {
    int u = q.front(); q.pop();
    if (seen[u]) continue;
    seen[u] = true;                 // marking here, not on push
    for (int v : adj[u]) if (!seen[v]) q.push(v);
}
```

This gives the right answer and can be catastrophically slow. A vertex with a hundred thousand
neighbours gets pushed a hundred thousand times before it is first popped, so the queue holds
O(E) entries rather than O(V), and on a dense graph it runs out of memory.

**Mark on push.** The version in section 3 does, and it is why `dist[v] = dist[u] + 1` sits inside
the `if`.

### The near-miss: `int` distances in Dijkstra

```cpp
std::vector<int> dist(n, INT_MAX);
// ...
if (d + w < dist[v])            // d + w overflows when d is INT_MAX
```

Two problems at once. Path lengths of 10^5 edges at weight 10^9 reach 10^14, which needs
`long long`. And `INT_MAX + w` overflows immediately, which is undefined behaviour and in practice
wraps negative — making unreachable vertices look extremely close and quietly corrupting
everything.

**Use `long long` and a sentinel of `1e18`,** which leaves room to add without overflowing.

### The quiet one: off by one on vertex numbering

```cpp
cin >> u >> v;
adj[u].push_back(v);      // the input numbers from 1. adj has size n.
```

With `n = 5` and an edge `5 3`, `adj[5]` is out of range on a vector of size 5. Sometimes it
crashes. Often it silently reads and writes past the end and corrupts the vector next to it, and
the failure appears somewhere unrelated.

```
=================================================================
==28190==ERROR: AddressSanitizer: container-overflow on address 0x602000000090
WRITE of size 8 at 0x602000000090 thread T0
    #0 0x401533 in main graphs.cpp:24
```

**Convert once, at the point of reading: `u--; v--;`.** Or size the vectors `n + 1` and use 1-based
numbering throughout. Pick one and be consistent for the whole file — mixing them is where the bug
actually comes from.

---

## 8. In the interview

### How it gets asked

- *"How would you represent a graph?"* — the opener, where the expected answer is the list and the
  reason is memory.
- *"Your DFS crashes on the large test but works on the samples. Why?"* — the applied version, and
  a very common one.
- *"BFS or DFS here, and why?"* — where the real answer is about shortest paths and about which
  shape the graph has.
- *"Implement union-find."* — asked directly, because it is fifteen lines and reveals whether you
  know path compression.

### What to say out loud, in the first ninety seconds

1. **Give the representation.** *"An adjacency list — `vector<vector<int>>`, where `adj[u]` holds
   u's neighbours. For weights, `vector<vector<pair<int,int>>>`."*
2. **Justify it with the number.** *"A matrix is O(V²) whether the edges exist or not. At V = 10^5
   that is 10^10 cells, about 40 GB. The list is O(V + E), which for a typical sparse graph is a
   few megabytes."*
3. **Say when the matrix is right.** *"I would use a matrix only for small dense graphs, under
   about a thousand vertices, where I need an O(1) edge test — Floyd-Warshall being the case."*
4. **Name the depth risk.** *"For traversal I would be careful with recursive DFS. C++ has no
   recursion limit — it just runs out of stack and segfaults with no message. The default stack is
   8 MB, which is about 130,000 frames."*
5. **Give the fix.** *"So on a graph that could be a long chain, or a large grid flood fill, I
   write DFS iteratively with an explicit `std::stack`. That runs on the heap, so the limit is the
   memory limit rather than 8 MB."*
6. **Contrast with Python.** *"Python raises `RecursionError` at about a thousand, which is
   annoying but visible. C++ gives you a segfault with no line number, which is why this is worth
   thinking about before it happens."*

Step 6 is a small thing that lands well, because it shows you know the failure mode rather than
just the rule.

### The follow-ups

**"BFS or DFS, and how do you decide?"**
BFS if I need shortest paths in an unweighted graph, because expanding in rings means the first
time I reach a vertex is by a minimum number of edges — DFS gives no such guarantee. DFS if I need
structure: cycle detection, topological order, bridges and articulation points, or anything where
the recursion's natural post-order does the work for me. There is also a shape argument: BFS's
memory is the width of the graph and DFS's is the depth, so they fail on opposite inputs. A long
chain is fine for BFS and blows the stack for recursive DFS; a very wide star is the reverse. If
the graph is a grid of a million cells I would use BFS with a queue for both reasons.

**"Why is union-find nearly constant time?"**
Two optimisations together. Union by size always attaches the smaller tree under the larger root,
which bounds the height at log n on its own. Path compression makes every node on a `find` path
point straight at the root, so the next `find` on any of them is one step. Applied together the
amortised cost per operation is O(α(n)), the inverse Ackermann function, which is below 5 for any n
that fits in the universe. Tarjan proved that bound and it is tight. In practice I treat it as
constant, and I write `find` iteratively with path halving so there is no recursion depth at all.

**"How does Dijkstra work with `std::priority_queue`, given it has no decrease-key?"**
Lazy deletion. The textbook version lowers a vertex's key in place, and C++'s `priority_queue`
cannot do that — you cannot even iterate it. So instead of updating an existing entry I push a new
`(distance, vertex)` pair with the better distance, leaving the old one in the heap. When a stale
entry surfaces I detect it with `if (d > dist[u]) continue;` and skip it. The heap can hold up to E
entries rather than V, so the complexity is O(E log E) rather than O(E log V) — but log E is at most
twice log V, so it is the same up to a constant, and it is far simpler and faster in practice than
maintaining an indexed heap.

**"What if the graph has negative edge weights?"**
Dijkstra is wrong, not just slow. It commits to a vertex's distance the moment it pops it,
assuming no later path can be shorter, and a negative edge breaks exactly that assumption. I would
use Bellman-Ford — O(V·E), relaxing every edge V−1 times, which also detects a negative cycle if a
V-th pass still improves something. For all pairs on a small dense graph, Floyd-Warshall at
O(V³). And if the weights are only 0 and 1, 0-1 BFS with a deque is O(V + E): push a 0-weight
neighbour to the front and a 1-weight one to the back.

### A model answer

The interviewer asks how the candidate would represent a graph and traverse it.

> "An adjacency list. In C++ that is `vector<vector<int>> adj(n)`, where `adj[u]` holds every
> vertex u connects to; with weights it becomes `vector<vector<pair<int,int>>>`.
>
> The reason is memory. An adjacency matrix is O(V²) regardless of how many edges there actually
> are — at 10^5 vertices that is 10^10 cells, around forty gigabytes, and the allocation itself
> throws `bad_alloc`. The list is O(V + E), so the same graph with 2 × 10^5 edges is about four
> megabytes. Real graphs are sparse, so the list is almost always right. I would use a matrix only
> for a small dense graph — under about a thousand vertices — where I need to test 'is there an edge
> from u to v' in constant time, which is really the Floyd-Warshall case.
>
> For traversal: BFS with a `std::queue` if I need shortest paths in an unweighted graph, because
> expanding in rings guarantees the first arrival is a minimum-edge path. DFS if I need structure —
> cycles, topological order, components.
>
> There is one thing I would be deliberate about, which is recursion depth. Recursive DFS is four
> lines and I like it, but C++ enforces no recursion limit. It pushes frames until the stack runs
> out and then the process dies with `Segmentation fault` and no line number — unlike Python, which
> counts frames and raises `RecursionError`. The default stack on Linux is 8 megabytes and a small
> DFS frame is around sixty-four bytes, so the ceiling is roughly a hundred and thirty thousand
> frames. A chain of 10^5 vertices sits right on that, and a flood fill on a 1000 × 1000 grid can
> recurse a million deep in the worst case.
>
> So my rule is: recursive DFS when the depth is provably small — a balanced tree, a bounded
> structure. Iterative, with an explicit `std::stack`, when the graph could be a long chain or a
> large grid. The iterative version runs on the heap, so it is bounded by the memory limit rather
> than the stack limit. The cost is that the children come out in reverse order and post-order work
> needs a second pass or an explicit state marker.
>
> One last thing on the input: judges number vertices from one and C++ from zero, so I decrement
> both endpoints at the point of reading. Getting that wrong writes past the end of the vector,
> which is undefined behaviour and usually shows up somewhere completely unrelated."

That answer gives the choice, justifies it with arithmetic, names when the other option is right,
raises a failure mode before being asked, gives the fix and its cost, and closes with the
practical detail that actually loses contests.

---

## 9. Recall card

1. **`vector<vector<int>> adj(n)` is a graph.** O(V + E) memory. A matrix is O(V²), which is 40 GB
   at V = 10^5 — use it only for dense graphs under about a thousand vertices.
2. **BFS with a `queue`, and mark `dist[v]` on PUSH, never on pop.** First arrival is a shortest
   path when every edge counts the same.
3. **C++ has no recursion limit — it segfaults with no message.** 8 MB stack ÷ ~64 bytes per frame
   ≈ 130,000 frames. Long chains and 1000 × 1000 grids exceed it. Write DFS iteratively, or raise
   the stack.
4. **Dijkstra: `long long` distances, a min-heap of `(dist, vertex)`, and `if (d > dist[u])
   continue;`** for lazy deletion, because `priority_queue` has no decrease-key.
5. **DSU is fifteen lines and effectively O(1)** with path compression and union by size. And use
   `vector<char>` for visited, not `vector<bool>` — that one stores bits and returns a proxy.

---

**Next in C++:** [day 143 — DP tables in C++, and the contest traps that are
left](../day-143-what-dp-is/04-cpp-dp-tables.md).
