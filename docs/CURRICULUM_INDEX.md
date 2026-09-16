# Krama — the curriculum index

180 days. Each day teaches one DSA topic and one system design topic, side by side,
and one languages theme taught three times — in Python, in Go, and in C++.
This file is generated from `scripts/curriculum.py` — edit that, then run
`python scripts/build_skeleton.py`.

- **Days 1-96** build the foundations and the low-level design half.
- **Days 97-180** build distributed systems and the high-level design half.
- **The languages track** runs its own nine phases alongside, from the first
  program to an eight-day capstone; Go carries Protocol Buffers and gRPC.

---

## The DSA track, by phase

| Days | Phase |
|---|---|
| 1-8 | Foundations: how code costs |
| 9-18 | Arrays |
| 19-26 | Strings |
| 27-36 | Two pointers and sliding window |
| 37-41 | Prefix sums |
| 42-50 | Binary search |
| 51-59 | Sorting |
| 60-67 | Hashing: maps and sets |
| 68-77 | Stacks and queues |
| 78-86 | Linked lists |
| 87-97 | Recursion and backtracking |
| 98-112 | Trees and binary search trees |
| 113-119 | Heaps and priority queues |
| 120-124 | Tries |
| 125-142 | Graphs |
| 143-163 | Dynamic programming |
| 164-170 | Greedy and intervals |
| 171-176 | Bits and maths |
| 177-180 | Final mocks and revision |

## The system design track, by phase

| Days | Phase |
|---|---|
| 1-14 | How computers and the internet work |
| 15-24 | APIs: how services talk |
| 25-42 | Databases from zero |
| 43-54 | Object-oriented design |
| 55-62 | SOLID and design principles |
| 63-76 | Design patterns |
| 77-96 | Low-level design case studies |
| 97-112 | Scaling fundamentals |
| 113-128 | Distributed systems core |
| 129-144 | Building blocks of big systems |
| 145-170 | High-level design case studies |
| 171-180 | Reliability, security, and the interview itself |

## The languages track, by phase

| Days | Phase |
|---|---|
| 1-15 | Languages: every language, every basic |
| 16-45 | Languages: advanced features |
| 46-60 | Languages: networking, HTTP, and data |
| 61-75 | Languages: Protocol Buffers and gRPC |
| 76-90 | Languages: performance and systems programming |
| 91-105 | Languages: messaging, resilience, and deployment |
| 106-135 | Languages: idiomatic depth and design |
| 136-165 | Languages: six five-day builds |
| 166-180 | Languages: interview prep and the capstone |

### Languages projects

| Starts | Project |
|---|---|
| Day 015 | Mini project 1: a to-do CLI |
| Day 030 | Mini project 2: a text analyser |
| Day 045 | Mini project 3: a concurrent downloader |
| Day 060 | Mini project 4: a URL shortener API |
| Day 075 | Mini project 5: an inventory service over gRPC |
| Day 090 | Mini project 6: a log analytics pipeline |
| Day 105 | Mini project 7: orders, events, and notifications |
| Day 120 | Mini project 8: a rate-limiter library |
| Day 135 | Mini project 9: a key-value store with a wire protocol |
| Day 136 | Build A: a distributed cache (days 136-140) |
| Day 141 | Build B: a job queue (days 141-145) |
| Day 146 | Build C: a storage engine (days 146-150) |
| Day 151 | Build D: a chat system (days 151-155) |
| Day 156 | Build E: an observability toolkit (days 156-160) |
| Day 161 | Build F: a tiny language (days 161-165) |
| Day 171 | Capstone: an order platform (days 171-178) |

## The C++ contest track

Optional, and twelve days long. Each one sits on the day the DSA course first needs
that piece of C++. Five land in the first six days, which is enough to start solving
in C++; the rest are placed at the head of the phase that needs them. This is separate
from the languages track's C++ lesson, which every day carries.

| Day | C++ contest lesson |
|---:|---|
| [001](../days/day-001-how-your-code-actually-runs/README.md) | Compiling and running your first program |
| [002](../days/day-002-counting-steps/README.md) | Types, numbers, and the overflow that costs contests |
| [003](../days/day-003-big-o-in-plain-english/README.md) | Input, output, and the competitive template |
| [005](../days/day-005-python-lists-and-tuples/README.md) | vector, references, and the array you use for everything |
| [006](../days/day-006-python-strings-dicts-sets/README.md) | string, map, set, and pair: half of DSA in four containers |
| [042](../days/day-042-binary-search-idea/README.md) | sort, lambdas, and lower_bound: the algorithms header |
| [068](../days/day-068-stacks/README.md) | stack, queue, deque, and priority_queue |
| [078](../days/day-078-nodes-and-links/README.md) | structs, pointers, and building your own nodes |
| [125](../days/day-125-what-a-graph-is/README.md) | Graphs and recursion in C++: adjacency lists, depth, and DSU |
| [143](../days/day-143-what-dp-is/README.md) | DP tables in C++, and the contest traps that are left |
| [171](../days/day-171-binary-and-bits/README.md) | Shifts, builtins, and bitset |
| [178](../days/day-178-thinking-out-loud/README.md) | Stress testing, and reading a judge's verdict |

---

## Every day: DSA and system design

### Days 1-8 — Foundations: how code costs

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [001](../days/day-001-how-your-code-actually-runs/README.md) | How your code actually runs, and where the time goes | What happens when you type google.com and press Enter |
| [002](../days/day-002-counting-steps/README.md) | Counting steps: your first cost model | Client and server, explained properly |
| [003](../days/day-003-big-o-in-plain-english/README.md) | Big-O in plain English | IP addresses, ports, and DNS |
| [004](../days/day-004-the-growth-curves/README.md) | The growth curves you will meet again and again | TCP and UDP |
| [005](../days/day-005-python-lists-and-tuples/README.md) | Python for DSA I: lists, tuples, and slicing | HTTP: the request and the response |
| [006](../days/day-006-python-strings-dicts-sets/README.md) | Python for DSA II: strings, dictionaries, and sets | HTTPS and TLS, without the maths |
| [007](../days/day-007-space-complexity/README.md) | Space complexity, and what in-place really means | What a web server actually does |
| [008](../days/day-008-reading-a-problem/README.md) | Reading a problem like the interviewer wrote it | Processes, threads, and concurrency |

### Days 9-18 — Arrays

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [009](../days/day-009-what-an-array-is/README.md) | What an array really is in memory | CPU, RAM, and disk: the speed hierarchy |
| [010](../days/day-010-traversal-patterns/README.md) | Traversal: the loop patterns you will reuse forever | Latency numbers every engineer should know |
| [011](../days/day-011-insert-and-delete/README.md) | Insert, delete, and the cost of the middle | The operating system's job |
| [012](../days/day-012-linear-search/README.md) | Searching an array: linear search, done properly | How your code becomes a running service |
| [013](../days/day-013-reverse-and-rotate/README.md) | Reversing, rotating, and swapping in place | Containers and why everyone uses Docker |
| [014](../days/day-014-single-pass-habit/README.md) | Max, min, second largest: the single-pass habit | Fundamentals revision and interview questions |
| [015](../days/day-015-the-write-pointer/README.md) | Moving elements: zeros, duplicates, and the write pointer | What an API is |
| [016](../days/day-016-2d-arrays/README.md) | 2D arrays and matrix traversal | REST, properly |
| [017](../days/day-017-matrix-tricks/README.md) | Matrix tricks: rotate, spiral, transpose | Designing a good REST endpoint |
| [018](../days/day-018-arrays-revision/README.md) | Arrays revision and mock round | Status codes, errors, and idempotency |

### Days 19-26 — Strings

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [019](../days/day-019-what-a-string-is/README.md) | What a string is, and why it is immutable | Authentication and authorisation |
| [020](../days/day-020-building-strings/README.md) | Building strings without the quadratic trap | JWT, sessions, and OAuth |
| [021](../days/day-021-frequency-maps/README.md) | Character counting and frequency maps | GraphQL versus REST |
| [022](../days/day-022-anagrams/README.md) | Anagrams: the sorting versus counting choice | gRPC and when binary protocols win |
| [023](../days/day-023-palindromes/README.md) | Palindromes and the two-ends habit | Rate limiting and API gateways |
| [024](../days/day-024-substrings-vs-subsequences/README.md) | Substrings versus subsequences: the distinction they test | API revision and interview questions |
| [025](../days/day-025-pattern-matching/README.md) | Pattern matching, the simple way | What a database gives you that a file does not |
| [026](../days/day-026-strings-revision/README.md) | Strings revision and mock round | Tables, rows, and keys |

### Days 27-36 — Two pointers and sliding window

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [027](../days/day-027-two-pointers-idea/README.md) | Two pointers: the idea | SQL you must know for interviews |
| [028](../days/day-028-opposite-ends/README.md) | Opposite ends: pair sums on a sorted array | Joins, drawn |
| [029](../days/day-029-read-write-pointer/README.md) | Same direction: the read pointer and the write pointer | Normalisation and when to break it |
| [030](../days/day-030-fast-and-slow/README.md) | Fast and slow pointers | Indexes: how a database finds a row fast |
| [031](../days/day-031-fixed-window/README.md) | Fixed-size sliding window | B-trees and why indexes are shaped that way |
| [032](../days/day-032-variable-window/README.md) | Variable-size sliding window | Query plans and the slow query |
| [033](../days/day-033-window-with-a-map/README.md) | Window plus hash map: the longest-substring family | Transactions and ACID |
| [034](../days/day-034-at-most-k/README.md) | At-most-K, and the exactly-K trick | Isolation levels and the anomalies they allow |
| [035](../days/day-035-choosing-the-pattern/README.md) | Choosing between two pointers and a window, under pressure | Locking and deadlocks |
| [036](../days/day-036-two-pointers-revision/README.md) | Two pointers revision and mock round | NoSQL: what it actually means |

### Days 37-41 — Prefix sums

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [037](../days/day-037-prefix-sums/README.md) | Prefix sums: answering range queries instantly | Key-value stores |
| [038](../days/day-038-subarray-sum-k/README.md) | Subarray sum equals K: prefix plus hash map | Document databases |
| [039](../days/day-039-difference-arrays/README.md) | Difference arrays: range updates, cheaply | Wide-column and time-series stores |
| [040](../days/day-040-2d-prefix-sums/README.md) | 2D prefix sums and inclusion-exclusion | Choosing SQL or NoSQL in an interview |
| [041](../days/day-041-prefix-revision/README.md) | Prefix sums revision and mock round | Connection pools, ORMs, and the N+1 query |

### Days 42-50 — Binary search

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [042](../days/day-042-binary-search-idea/README.md) | Binary search: the idea and the invariant | Database revision and interview questions |
| [043](../days/day-043-binary-search-without-bugs/README.md) | Writing binary search without off-by-one bugs | Why interviews ask object-oriented design at all |
| [044](../days/day-044-first-and-last-occurrence/README.md) | First and last occurrence | Classes and objects |
| [045](../days/day-045-rotated-array-search/README.md) | Search in a rotated sorted array | Encapsulation |
| [046](../days/day-046-binary-search-on-the-answer/README.md) | Binary search on the answer | Inheritance and its costs |
| [047](../days/day-047-minimise-the-maximum/README.md) | Minimise the maximum: the capacity family | Polymorphism |
| [048](../days/day-048-binary-search-on-floats/README.md) | Binary search on floats, and the epsilon question | Abstraction and interfaces |
| [049](../days/day-049-peak-finding/README.md) | Peak finding, and searching data that is structured but not sorted | Composition over inheritance |
| [050](../days/day-050-binary-search-revision/README.md) | Binary search revision and mock round | Class diagrams and the UML you will actually draw |

### Days 51-59 — Sorting

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [051](../days/day-051-why-sorting-matters/README.md) | Why sorting matters more than any single sorting algorithm | Modelling a real domain |
| [052](../days/day-052-quadratic-sorts/README.md) | Bubble, selection and insertion sort, and what each one teaches | Common object-oriented interview questions |
| [053](../days/day-053-merge-sort/README.md) | Merge sort | Writing clean, testable classes |
| [054](../days/day-054-quicksort/README.md) | Quicksort and partitioning | Object-oriented design revision and interview questions |
| [055](../days/day-055-quickselect/README.md) | Quickselect: finding the Kth largest without sorting | Single responsibility |
| [056](../days/day-056-non-comparison-sorts/README.md) | Counting sort, radix sort, and bucket sort | Open for extension, closed for modification |
| [057](../days/day-057-stability-and-pythons-sort/README.md) | Stability, and what Python's sort actually does | Liskov substitution |
| [058](../days/day-058-custom-comparators/README.md) | Custom comparators and sorting by keys | Interface segregation |
| [059](../days/day-059-sorting-revision/README.md) | Sorting revision and mock round | Dependency inversion |

### Days 60-67 — Hashing: maps and sets

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [060](../days/day-060-hash-tables/README.md) | Hash tables: how a dictionary finds anything instantly | DRY, KISS, and YAGNI |
| [061](../days/day-061-collisions/README.md) | Collisions, and why a hash map can turn slow | Coupling, cohesion, and code smells |
| [062](../days/day-062-sets/README.md) | Sets: membership, deduplication, and the O(1) habit | Design principles revision and interview questions |
| [063](../days/day-063-counting-with-dicts/README.md) | Counting with dictionaries | What a design pattern actually is |
| [064](../days/day-064-grouping/README.md) | Grouping: the key-design skill | Singleton |
| [065](../days/day-065-hashing-custom-objects/README.md) | Hashing your own objects | Factory and abstract factory |
| [066](../days/day-066-when-hashing-is-wrong/README.md) | When a hash map is the wrong answer | Builder |
| [067](../days/day-067-hashing-revision/README.md) | Hashing revision and mock round | Prototype, and cloning objects |

### Days 68-77 — Stacks and queues

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [068](../days/day-068-stacks/README.md) | Stacks: last in, first out | Adapter |
| [069](../days/day-069-balanced-brackets/README.md) | Balanced brackets and the parsing family | Decorator |
| [070](../days/day-070-min-stack/README.md) | Min stack, and stacks that carry extra state | Facade and proxy |
| [071](../days/day-071-monotonic-stack/README.md) | Monotonic stack: the next greater element | Strategy |
| [072](../days/day-072-largest-rectangle/README.md) | Largest rectangle in a histogram | Observer |
| [073](../days/day-073-queues/README.md) | Queues: first in, first out | State |
| [074](../days/day-074-deques-and-window-max/README.md) | Deques and the sliding-window maximum | Command and chain of responsibility |
| [075](../days/day-075-queue-from-stacks/README.md) | A queue from two stacks, and a stack from queues | Template method and iterator |
| [076](../days/day-076-lru-cache/README.md) | LRU cache: the structure interviewers love | Design patterns revision and interview questions |
| [077](../days/day-077-stacks-queues-revision/README.md) | Stacks and queues revision and mock round | How to run a low-level design interview: the forty-minute script |

### Days 78-86 — Linked lists

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [078](../days/day-078-nodes-and-links/README.md) | Nodes and links: pointers without pointers | Design a parking lot |
| [079](../days/day-079-list-traversal/README.md) | Traversal, insertion, and deletion | Design an elevator system |
| [080](../days/day-080-dummy-head/README.md) | The dummy head trick | Design an ATM |
| [081](../days/day-081-reversing-a-list/README.md) | Reversing a linked list | Design a vending machine |
| [082](../days/day-082-runner-technique/README.md) | Finding the middle, and the runner technique | Design a library management system |
| [083](../days/day-083-cycle-detection/README.md) | Cycle detection, and why Floyd's algorithm works | Design tic-tac-toe, and then chess |
| [084](../days/day-084-merging-and-sorting-lists/README.md) | Merging and sorting linked lists | Design a deck of cards and a card game |
| [085](../days/day-085-doubly-and-circular/README.md) | Doubly and circular linked lists | Design Splitwise |
| [086](../days/day-086-linked-lists-revision/README.md) | Linked lists revision and mock round | Design BookMyShow |

### Days 87-97 — Recursion and backtracking

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [087](../days/day-087-recursion-leap-of-faith/README.md) | Recursion: the leap of faith | Design a food delivery order flow |
| [088](../days/day-088-the-call-stack/README.md) | The call stack, drawn | Design a ride-hailing booking flow |
| [089](../days/day-089-recursion-that-terminates/README.md) | Writing a recursive function that terminates | Design a rate limiter, at the object level |
| [090](../days/day-090-recursion-on-arrays/README.md) | Recursion on arrays and strings | Design an in-memory cache with eviction |
| [091](../days/day-091-subsets/README.md) | Subsets: the include-or-exclude tree | Design a logging framework |
| [092](../days/day-092-permutations/README.md) | Permutations | Design a notification service |
| [093](../days/day-093-combinations/README.md) | Combinations and combination sum | Design a file system |
| [094](../days/day-094-backtracking/README.md) | Backtracking: the undo step | Design snake and ladder |
| [095](../days/day-095-n-queens/README.md) | N-Queens and constraint grids | Design an online auction |
| [096](../days/day-096-grid-backtracking/README.md) | Sudoku, word search, and grid backtracking | Low-level design revision and full mock |
| [097](../days/day-097-recursion-revision/README.md) | Recursion and backtracking revision and mock round | What scale actually means, in numbers |

### Days 98-112 — Trees and binary search trees

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [098](../days/day-098-what-a-tree-is/README.md) | What a tree is, and the vocabulary you need | Vertical versus horizontal scaling |
| [099](../days/day-099-binary-trees-in-code/README.md) | Binary trees in code | Load balancers |
| [100](../days/day-100-dfs-traversals/README.md) | Depth-first traversal: preorder, inorder, postorder | Stateless services and why they scale |
| [101](../days/day-101-bfs-level-order/README.md) | Breadth-first traversal: level order | Caching: the single biggest win |
| [102](../days/day-102-height-and-diameter/README.md) | Height, depth, and diameter | Cache invalidation and eviction policies |
| [103](../days/day-103-tree-comparisons/README.md) | Same tree, symmetric tree, and subtree | Content delivery networks |
| [104](../days/day-104-tree-path-problems/README.md) | Path problems, and the return-value trick | Database replication |
| [105](../days/day-105-lowest-common-ancestor/README.md) | Lowest common ancestor | Read replicas and replication lag |
| [106](../days/day-106-bst-property/README.md) | Binary search trees: the ordering property | Sharding, part one: choosing the key |
| [107](../days/day-107-bst-operations/README.md) | BST insert, search, and delete | Sharding, part two: rebalancing and hot spots |
| [108](../days/day-108-validating-a-bst/README.md) | Validating a binary search tree | Consistent hashing |
| [109](../days/day-109-balanced-trees/README.md) | Balanced trees, and why balance matters | Back-of-the-envelope estimation |
| [110](../days/day-110-trees-from-traversals/README.md) | Building a tree from its traversals | Capacity planning: QPS, storage, bandwidth |
| [111](../days/day-111-serialise-a-tree/README.md) | Serialising and deserialising a tree | Single points of failure |
| [112](../days/day-112-trees-revision/README.md) | Trees revision and mock round | Scaling revision and interview questions |

### Days 113-119 — Heaps and priority queues

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [113](../days/day-113-the-heap/README.md) | The heap: a tree stored in an array | Why distributed systems are hard |
| [114](../days/day-114-heapify/README.md) | Push, pop, and heapify | The CAP theorem, honestly |
| [115](../days/day-115-heapq/README.md) | Python's heapq, and the min-heap-only problem | Consistency models |
| [116](../days/day-116-top-k/README.md) | Top K problems | Eventual consistency in practice |
| [117](../days/day-117-merge-k-sorted/README.md) | Merging K sorted lists | Quorums: why R plus W must exceed N |
| [118](../days/day-118-two-heaps/README.md) | Two heaps: the running median | Leader election |
| [119](../days/day-119-heaps-revision/README.md) | Heaps revision and mock round | Consensus, and Raft in plain English |

### Days 120-124 — Tries

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [120](../days/day-120-the-trie/README.md) | The trie: a tree of characters | Distributed transactions and two-phase commit |
| [121](../days/day-121-trie-operations/README.md) | Insert, search, and prefix search | The saga pattern |
| [122](../days/day-122-autocomplete/README.md) | Autocomplete and word dictionaries | Idempotency and exactly-once delivery |
| [123](../days/day-123-word-search-ii/README.md) | Tries in interviews: word search II | Clocks, ordering, and why time is a lie |
| [124](../days/day-124-tries-revision/README.md) | Tries revision and mock round | Failure detection, heartbeats, and timeouts |

### Days 125-142 — Graphs

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [125](../days/day-125-what-a-graph-is/README.md) | What a graph is, and where graphs hide | Retries, backoff, and thundering herds |
| [126](../days/day-126-graph-representation/README.md) | Representing a graph: adjacency matrix versus adjacency list | Circuit breakers and bulkheads |
| [127](../days/day-127-graph-bfs/README.md) | Breadth-first search on a graph | Distributed locks |
| [128](../days/day-128-graph-dfs/README.md) | Depth-first search on a graph | Distributed systems revision and interview questions |
| [129](../days/day-129-connected-components/README.md) | Connected components | Message queues: why async changes everything |
| [130](../days/day-130-grids-are-graphs/README.md) | Grids are graphs: islands and flood fill | Kafka, explained |
| [131](../days/day-131-unweighted-shortest-path/README.md) | Shortest path in an unweighted graph | Publish-subscribe versus point-to-point |
| [132](../days/day-132-undirected-cycles/README.md) | Cycle detection in an undirected graph | Stream processing basics |
| [133](../days/day-133-directed-cycles/README.md) | Cycle detection in a directed graph | Object storage, S3-style |
| [134](../days/day-134-topological-sort/README.md) | Topological sort | Blob storage versus storing files in the database |
| [135](../days/day-135-dependency-problems/README.md) | Course schedule and the dependency family | Search: how a search index actually works |
| [136](../days/day-136-dijkstra/README.md) | Dijkstra's algorithm | Elasticsearch in a design |
| [137](../days/day-137-bellman-ford/README.md) | Bellman-Ford, and what negative edges break | Time-series and metrics stores |
| [138](../days/day-138-union-find/README.md) | Union-Find: the disjoint set union | Data warehouses: OLAP versus OLTP |
| [139](../days/day-139-minimum-spanning-trees/README.md) | Minimum spanning trees: Kruskal and Prim | ETL, batch pipelines, and where data goes to be counted |
| [140](../days/day-140-bipartite-graphs/README.md) | Bipartite graphs and two-colouring | Websockets, long polling, and server-sent events |
| [141](../days/day-141-multi-source-bfs/README.md) | Multi-source BFS and 0-1 BFS | Push notifications, end to end |
| [142](../days/day-142-graphs-revision/README.md) | Graphs revision and mock round | Geospatial indexing: geohash and quadtrees |

### Days 143-163 — Dynamic programming

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [143](../days/day-143-what-dp-is/README.md) | What dynamic programming actually is | Bloom filters and probabilistic structures |
| [144](../days/day-144-fibonacci-dp/README.md) | Fibonacci: memoisation versus tabulation | Building blocks revision and interview questions |
| [145](../days/day-145-climbing-stairs/README.md) | Climbing stairs and the one-dimensional habit | How to run a high-level design interview: the forty-five-minute script |
| [146](../days/day-146-house-robber/README.md) | House robber and the choice at each step | Design a URL shortener |
| [147](../days/day-147-finding-the-state/README.md) | Finding the state: the hardest part of DP | Design a pastebin |
| [148](../days/day-148-knapsack/README.md) | The 0/1 knapsack | Design a rate limiter, at system scale |
| [149](../days/day-149-subset-sum/README.md) | Subset sum and partition problems | Design a distributed key-value store |
| [150](../days/day-150-coin-change/README.md) | Unbounded knapsack and coin change | Design a distributed unique ID generator |
| [151](../days/day-151-counting-ways/README.md) | Coin change II: counting the ways | Design a web crawler |
| [152](../days/day-152-longest-increasing-subsequence/README.md) | Longest increasing subsequence | Design a notification system at scale |
| [153](../days/day-153-longest-common-subsequence/README.md) | Longest common subsequence | Design a news feed |
| [154](../days/day-154-edit-distance/README.md) | Edit distance | Design Twitter |
| [155](../days/day-155-string-dp/README.md) | String DP: palindromic substrings and subsequences | Design Instagram |
| [156](../days/day-156-grid-dp/README.md) | Grid DP: unique paths and minimum path sum | Design WhatsApp |
| [157](../days/day-157-stock-dp/README.md) | DP on decisions: buy and sell stock | Design a chat system with presence |
| [158](../days/day-158-interval-dp/README.md) | Interval DP | Design YouTube |
| [159](../days/day-159-dp-on-trees/README.md) | DP on trees | Design Netflix |
| [160](../days/day-160-bitmask-dp/README.md) | Bitmask DP | Design Google Drive or Dropbox |
| [161](../days/day-161-dp-space-optimisation/README.md) | Space optimisation in DP | Design Uber |
| [162](../days/day-162-recognising-dp/README.md) | Recognising dynamic programming in an interview | Design Google Maps |
| [163](../days/day-163-dp-revision/README.md) | Dynamic programming revision and mock round | Design an e-commerce system |

### Days 164-170 — Greedy and intervals

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [164](../days/day-164-greedy-idea/README.md) | Greedy: when taking the best option now is safe | Design a payment system |
| [165](../days/day-165-proving-greedy/README.md) | Proving a greedy choice, simply | Design a ticket booking system at scale |
| [166](../days/day-166-interval-scheduling/README.md) | Interval scheduling | Design search autocomplete at scale |
| [167](../days/day-167-merging-intervals/README.md) | Merging intervals | Design a leaderboard |
| [168](../days/day-168-sweep-line/README.md) | Meeting rooms and the sweep line | Design an ad click aggregator |
| [169](../days/day-169-jump-game/README.md) | Jump game and reachability | Design a distributed job scheduler |
| [170](../days/day-170-greedy-revision/README.md) | Greedy and intervals revision and mock round | High-level design revision and full mock |

### Days 171-176 — Bits and maths

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [171](../days/day-171-binary-and-bits/README.md) | Binary, bits, and why they matter | Monitoring, metrics, and alerting |
| [172](../days/day-172-bit-tricks/README.md) | The bit tricks every interview uses | Logging and distributed tracing |
| [173](../days/day-173-xor/README.md) | XOR problems | SLAs, SLOs, and error budgets |
| [174](../days/day-174-number-theory/README.md) | Primes, GCD, and modular arithmetic | Deployments: blue-green, canary, and rollback |
| [175](../days/day-175-combinatorics/README.md) | The combinatorics you actually need | Security in a design interview |
| [176](../days/day-176-bits-maths-revision/README.md) | Bits and maths revision and mock round | Cost: the constraint nobody mentions |

### Days 177-180 — Final mocks and revision

| Day | DSA lesson | System design lesson |
|---:|---|---|
| [177](../days/day-177-the-patterns-on-one-page/README.md) | The twenty patterns, on one page | Microservices versus monolith, argued both ways |
| [178](../days/day-178-thinking-out-loud/README.md) | How to think out loud in a coding round | The system design interview framework, memorised |
| [179](../days/day-179-full-coding-mock/README.md) | Full mock: two problems, forty-five minutes | Full mock: one high-level design, one low-level design |
| [180](../days/day-180-final-revision/README.md) | Final revision, and the week before the interview | Final revision, and the week before the interview |

---

## Every day: the languages track

### Days 1-15 — Languages: every language, every basic

| Day | Theme | Python | Go | C++ | You can |
|---:|---|---|---|---|---|
| [001](../days/day-001-how-your-code-actually-runs/README.md) | Toolchain and the first program | python3, a file, and the interpreter | go run, go build, and the Go toolchain | g++, a file, and the compiler | You can install all three toolchains, run a program in each, and read the first error each one gives you. |
| [002](../days/day-002-counting-steps/README.md) | Variables, types, and numbers | Dynamic names, int without limits, float with them | Static types, int64, and := versus var | Fixed-width ints, overflow, and auto | You can declare a number in each language, say how wide it is, and predict what 2 000 000 000 + 2 000 000 000 prints. |
| [003](../days/day-003-big-o-in-plain-english/README.md) | Strings and text | Immutable str, f-strings, and slicing | Strings are bytes, runes are characters, fmt.Sprintf | std::string, string literals, and std::format | You can build, slice, search and format text in each language, and say why a Hindi word has a different length in each. |
| [004](../days/day-004-the-growth-curves/README.md) | Conditions and loops | if/elif/else, for-in, while, break and continue | if with init statements, the only loop is for, switch without fallthrough | if, for, while, do-while, range-for, switch with fallthrough | You can write every loop shape in each language and pick the one that reads cleanest for a given job. |
| [005](../days/day-005-python-lists-and-tuples/README.md) | Functions | def, default arguments, *args, **kwargs, and returning anything | func, multiple return values, named results, variadic | Declarations, definitions, overloading, default arguments | You can write a function with several inputs and outputs in each language and explain where each argument lives. |
| [006](../days/day-006-python-strings-dicts-sets/README.md) | Growable sequences | list: append, insert, pop, slicing, and the cost of each | slice: length, capacity, append, and the backing array | std::vector: push_back, size, capacity, and reallocation | You can grow, shrink, index and copy a sequence in each language and say when a copy really happens. |
| [007](../days/day-007-space-complexity/README.md) | Key-value and membership | dict and set: hashing, ordering, and the in operator | map: make, lookup with the comma-ok idiom, delete, and no order | std::unordered_map, std::map, std::set, and the choice between them | You can count, group and deduplicate with a map in each language and explain what happens on a missing key. |
| [008](../days/day-008-reading-a-problem/README.md) | Modelling a thing | class, __init__, methods, and dataclasses | struct, methods with receivers, and constructor functions | struct, class, constructors, and member functions | You can model a bank account in each language with data and behaviour together, and say what is public. |
| [009](../days/day-009-what-an-array-is/README.md) | Errors, three ways | Exceptions: try, except, raise, finally | Error values: if err != nil, errors.New, fmt.Errorf | Exceptions and std::expected: throw, catch, and returning failure | You can make a function fail in each language and make the caller handle it, and say which style each language prefers. |
| [010](../days/day-010-traversal-patterns/README.md) | Files and standard I/O | open, with, read/write, pathlib, and sys.stdin | os.Open, bufio.Scanner, io.Reader and io.Writer | std::ifstream, std::ofstream, std::cin, std::cout, and buffering | You can read a file line by line, write one, and read from standard input in each language. |
| [011](../days/day-011-insert-and-delete/README.md) | Splitting code across files | import, modules, packages, and the main guard | package, exported names, go.mod, and internal directories | Headers, translation units, #include, and namespaces | You can split a program into three files in each language and explain what is visible from where. |
| [012](../days/day-012-linear-search/README.md) | Pointers, references, and value semantics | Everything is a reference to an object; is versus == | Pointers with & and *, value receivers versus pointer receivers | Pointers, references, const, and passing by value | You can say, for each language, whether a function receives a copy or the original, and prove it with a print. |
| [013](../days/day-013-reverse-and-rotate/README.md) | Memory: who frees what | Reference counting and the garbage collector | The garbage collector, escape analysis, and stack versus heap | RAII, new/delete, and why you almost never write delete | You can say where a value lives, who frees it, and when, in each language. |
| [014](../days/day-014-single-pass-habit/README.md) | Formatters, linters, and a real project layout | uv, venv, pyproject.toml, ruff | go fmt, go vet, go mod tidy, and the standard layout | CMake, clang-format, and a src/include layout | You can start a new project in each language from an empty folder, with formatting and dependencies working. |
| [015](../days/day-015-the-write-pointer/README.md) | Mini project 1: a to-do CLI | A to-do CLI in Python, saved as JSON | A to-do CLI in Go, saved as JSON | A to-do CLI in C++, saved as JSON | You can build the same small tool in all three languages, run it, and say which one felt right for the job. |

### Days 16-45 — Languages: advanced features

| Day | Theme | Python | Go | C++ | You can |
|---:|---|---|---|---|---|
| [016](../days/day-016-2d-arrays/README.md) | Interfaces | Duck typing, abstract base classes, and Protocol | Interfaces are satisfied implicitly; the empty interface; io.Reader | Abstract classes, pure virtual functions, and vtables | You can define a behaviour without naming a type in each language, and say when the check happens. |
| [017](../days/day-017-matrix-tricks/README.md) | Composition versus inheritance | Inheritance, super(), and the MRO | Struct embedding, and why Go has no inheritance | Public inheritance, virtual, override, and object slicing | You can extend a type in each language and say why composition is the usual answer. |
| [018](../days/day-018-arrays-revision/README.md) | Generics | typing generics: TypeVar, Generic, and list[T] | Type parameters, constraints, and any versus comparable | Templates, template argument deduction, and instantiation | You can write one Stack that works for ints and strings in each language. |
| [019](../days/day-019-what-a-string-is/README.md) | Closures | Functions as values, lambda, and captured variables | Function literals, captured loop variables, and function types | Lambdas, capture lists by value and by reference, std::function | You can return a function from a function in each language and say what it captured. |
| [020](../days/day-020-building-strings/README.md) | Iterators and generators | __iter__, __next__, yield, and generator expressions | Range-over-func iterators (iter.Seq) and channels as iterators | Iterator categories, begin/end, and C++20 ranges | You can produce values lazily in each language without building the whole list first. |
| [021](../days/day-021-frequency-maps/README.md) | Wrapping behaviour | Decorators, functools.wraps, and decorators with arguments | Middleware: functions that take and return handlers | Function objects, higher-order functions, and wrapper classes | You can add logging around any function in each language without touching the function. |
| [022](../days/day-022-anagrams/README.md) | Enums and sum types | Enum, IntEnum, auto, and match on enums | iota, typed constants, and the Stringer pattern | enum class, std::variant, and std::visit | You can model one-of-three-states in each language and be told, at compile time or run time, when you miss one. |
| [023](../days/day-023-palindromes/README.md) | Nothing, safely | None, Optional[T], and the walrus operator | nil, zero values, and the nil-interface trap | std::optional, nullptr, and value_or | You can express 'maybe no value' in each language and say what happens when you forget to check. |
| [024](../days/day-024-substrings-vs-subsequences/README.md) | Pattern matching | match/case with structural patterns and guards | Type switches and switch on values | std::visit on variant, if constexpr, and structured bindings | You can branch on the shape of data in each language. |
| [025](../days/day-025-pattern-matching/README.md) | Making your type behave like a built-in | __eq__, __lt__, __add__, __repr__, __hash__ | No operator overloading: Stringer, sort.Slice, and cmp | operator==, operator<=>, operator<<, and the rule of least surprise | You can make a Money type compare, print and sort correctly in each language. |
| [026](../days/day-026-strings-revision/README.md) | Immutability | frozen dataclasses, tuple, frozenset, and Final | const for constants only; immutability by convention | const, constexpr, consteval, and const-correct methods | You can mark something unchangeable in each language and say who enforces it. |
| [027](../days/day-027-two-pointers-idea/README.md) | Error handling, properly | Exception hierarchies, exception chaining, and ExceptionGroup | errors.Is, errors.As, %w wrapping, and sentinel errors | Exception hierarchies, noexcept, and std::expected chains | You can wrap an error with context in each language and unwrap it three layers up. |
| [028](../days/day-028-opposite-ends/README.md) | Testing | pytest: fixtures, parametrize, and assert introspection | go test, table-driven tests, and t.Run subtests | GoogleTest and CTest: TEST, EXPECT_EQ, and fixtures | You can write a test file in each language and make it fail on purpose to see the report. |
| [029](../days/day-029-read-write-pointer/README.md) | Debugging | pdb, breakpoint(), and reading a traceback | delve, and reading a goroutine panic dump | gdb, sanitizers, and reading a segfault | You can set a breakpoint, step, and inspect a variable in each language. |
| [030](../days/day-030-fast-and-slow/README.md) | Mini project 2: a text analyser | Word frequency and log summariser in Python | Word frequency and log summariser in Go | Word frequency and log summariser in C++ | You can build a tool that reads a large file, counts and reports, in all three, with tests. |
| [031](../days/day-031-fixed-window/README.md) | Concurrency I: threads | threading.Thread, the GIL, and what it really blocks | goroutines, go func(), and sync.WaitGroup | std::thread, std::jthread, and join | You can start ten workers in each language and wait for all of them. |
| [032](../days/day-032-variable-window/README.md) | Concurrency II: passing messages | queue.Queue and producer-consumer | Channels: unbuffered, buffered, close, and range | std::condition_variable and a hand-built thread-safe queue | You can move work between threads safely in each language. |
| [033](../days/day-033-window-with-a-map/README.md) | Concurrency III: shared memory | threading.Lock, RLock, and a race you can reproduce | sync.Mutex, sync.RWMutex, atomic, and go test -race | std::mutex, std::lock_guard, std::atomic, and ThreadSanitizer | You can write a data race in each language, detect it with a tool, and fix it. |
| [034](../days/day-034-at-most-k/README.md) | Concurrency IV: async | asyncio, await, gather, and the event loop | select, and why Go does not need async/await | std::async, std::future, and C++20 coroutines in outline | You can make 100 network calls at once in each language and say where the waiting happens. |
| [035](../days/day-035-choosing-the-pattern/README.md) | Worker pools and pipelines | concurrent.futures: ThreadPoolExecutor and ProcessPoolExecutor | Worker pool with channels, fan-out and fan-in | A thread pool class with a task queue | You can run N jobs on K workers in each language and collect results in order. |
| [036](../days/day-036-two-pointers-revision/README.md) | Timeouts and cancellation | asyncio.timeout, Event, and cooperative cancellation | context.Context: WithTimeout, WithCancel, and Done() | std::stop_token, deadlines, and checking a flag | You can stop a long job cleanly from the outside in each language. |
| [037](../days/day-037-prefix-sums/README.md) | Memory model, deeper | Object headers, refcounts, cycles, and the gc module | Escape analysis, the GC pacer, and GOGC | Smart pointers: unique_ptr, shared_ptr, weak_ptr | You can say why a value moved to the heap in each language and what that costs. |
| [038](../days/day-038-subarray-sum-k/README.md) | Copies, shares, and moves | Shallow copy, deepcopy, and aliasing bugs | Slices share backing arrays; copy(); append aliasing | Copy constructors, std::move, and the rule of five | You can predict whether a change through one variable shows up in another, in each language. |
| [039](../days/day-039-difference-arrays/README.md) | Text versus bytes | str versus bytes, encode, decode, and UnicodeDecodeError | []byte, rune, the utf8 package, and strings.Builder | char, char8_t, std::string_view, and UTF-8 by hand | You can explain what a byte is, what a character is, and where each language draws the line. |
| [040](../days/day-040-2d-prefix-sums/README.md) | JSON in and out | json.loads, json.dumps, dataclasses, and pydantic | encoding/json, struct tags, and omitempty | nlohmann/json: parsing, serialising, and from_json | You can round-trip a struct through JSON in each language and handle a bad document. |
| [041](../days/day-041-prefix-revision/README.md) | Dates, times, and randomness | datetime, zoneinfo, time.monotonic, and random versus secrets | time.Time, Duration, time.Now, and math/rand versus crypto/rand | std::chrono, time zones, and <random> | You can measure elapsed time correctly and generate a secure random token in each language. |
| [042](../days/day-042-binary-search-idea/README.md) | Regular expressions | re: search, match, findall, groups, and compiled patterns | regexp: RE2 semantics and why there is no backtracking | std::regex, and why you reach for RE2 or ctre instead | You can extract dates and emails from text in each language and say when regex is the wrong tool. |
| [043](../days/day-043-binary-search-without-bugs/README.md) | Reflection and metaprogramming | getattr, setattr, __dict__, and metaclasses in outline | reflect: Type, Value, struct tags, and when to avoid it | Type traits, if constexpr, and templates as compile-time code | You can inspect a type at run time in each language and say what it costs. |
| [044](../days/day-044-first-and-last-occurrence/README.md) | Building and shipping | pyproject.toml, wheels, and PyInstaller | go build flags, -ldflags, cross-compiling, and a static binary | CMake targets, static versus dynamic linking, and Release builds | You can produce a distributable artifact of a program in each language. |
| [045](../days/day-045-rotated-array-search/README.md) | Mini project 3: a concurrent downloader | asyncio and httpx downloader with a progress report | Goroutine worker-pool downloader with context | Thread-pool downloader with libcurl | You can fetch 200 URLs with a bounded pool, timeouts, and retries, in all three. |

### Days 46-60 — Languages: networking, HTTP, and data

| Day | Theme | Python | Go | C++ | You can |
|---:|---|---|---|---|---|
| [046](../days/day-046-binary-search-on-the-answer/README.md) | TCP sockets: an echo server | socket, bind, listen, accept, and a threaded echo server | net.Listen, Accept, and one goroutine per connection | POSIX sockets, or Boost.Asio, and one thread per connection | You can write a server that accepts a connection and echoes bytes back, in each language, and test it with a client. |
| [047](../days/day-047-minimise-the-maximum/README.md) | HTTP clients | httpx and requests: GET, POST, headers, timeouts, sessions | net/http Client, requests, headers, and reusing the transport | libcurl through cpr: GET, POST, headers, timeouts | You can call a JSON API with a timeout in each language and handle a 500. |
| [048](../days/day-048-binary-search-on-floats/README.md) | HTTP servers | FastAPI: a route, a request model, a response model | net/http: ServeMux, handlers, and http.ListenAndServe | cpp-httplib: routes and handlers | You can serve a JSON endpoint on a port in each language and hit it with curl. |
| [049](../days/day-049-peak-finding/README.md) | Routing and middleware | Routers, path parameters, dependencies, and middleware in FastAPI | Method and path patterns in ServeMux, and a middleware chain | Route patterns, pre-routing handlers, and a logging wrapper | You can add authentication and logging to every route without repeating code, in each language. |
| [050](../days/day-050-binary-search-revision/README.md) | Designing a JSON API | Pydantic models, validation errors, and status codes | Decoding request bodies, validation, and writing error responses | Parsing request bodies, validation, and consistent error shapes | You can build a CRUD endpoint set with proper status codes and error bodies, in each language. |
| [051](../days/day-051-why-sorting-matters/README.md) | Configuration: flags, environment, files | argparse and typer, os.environ, and a settings class | flag, cobra, os.Getenv, and a Config struct | CLI11, getenv, and a Config struct | You can configure a program from flags, env vars and a file, with a clear precedence order, in each language. |
| [052](../days/day-052-quadratic-sorts/README.md) | Logging that helps at 3am | logging, structlog, levels, and JSON output | log/slog: structured, levelled, and with context | spdlog: sinks, levels, and formatting | You can emit structured logs with request IDs in each language and grep them. |
| [053](../days/day-053-merge-sort/README.md) | Databases I: SQLite | sqlite3: connect, execute, parameters, and transactions | database/sql with modernc sqlite, prepared statements, and Scan | SQLite C API and a thin RAII wrapper | You can create a table, insert, query and update from each language, safely with parameters. |
| [054](../days/day-054-quicksort/README.md) | Databases II: Postgres and connection pools | psycopg 3 and asyncpg, and a connection pool | pgx, pgxpool, and context-aware queries | libpqxx: connections, transactions, and prepared statements | You can talk to a real Postgres from each language and say why a pool exists. |
| [055](../days/day-055-quickselect/README.md) | Databases III: migrations and ORMs | SQLAlchemy 2.0 and Alembic | sqlc generated queries and golang-migrate | Raw SQL with a migration runner you write yourself | You can evolve a schema safely in each language and say what an ORM buys and costs. |
| [056](../days/day-056-non-comparison-sorts/README.md) | Caching with Redis | redis-py: GET, SET, EX, and cache-aside | go-redis: GET, SET, pipelines, and cache-aside | redis-plus-plus: GET, SET, and cache-aside | You can add a cache in front of a slow query in each language and measure the difference. |
| [057](../days/day-057-stability-and-pythons-sort/README.md) | Authentication: hashing and tokens | bcrypt/argon2, PyJWT, and a login flow | bcrypt, golang-jwt, and a login flow | Argon2 via libsodium, jwt-cpp, and a login flow | You can store a password correctly and issue a signed token in each language. |
| [058](../days/day-058-custom-comparators/README.md) | Testing a service | TestClient, fixtures for a test database, and mocking with respx | httptest, table tests for handlers, and interfaces for mocking | GoogleTest with an in-process server, and gMock | You can test an HTTP handler in each language without a network or a real database. |
| [059](../days/day-059-sorting-revision/README.md) | Docker for each language | A slim Python image with uv and a non-root user | A multi-stage build to a scratch image | A multi-stage CMake build to a distroless image | You can containerise a service in each language and say why the images are 1 GB, 10 MB, and 20 MB. |
| [060](../days/day-060-hash-tables/README.md) | Mini project 4: a URL shortener API | FastAPI plus Postgres plus Redis | net/http plus pgx plus go-redis | cpp-httplib plus libpqxx plus redis-plus-plus | You can build, test, containerise, and demo the same REST service in all three languages. |

### Days 61-75 — Languages: Protocol Buffers and gRPC

| Day | Theme | Python | Go | C++ | You can |
|---:|---|---|---|---|---|
| [061](../days/day-061-collisions/README.md) | Protocol Buffers: what and why | JSON versus protobuf: size and speed, measured | JSON versus protobuf: size and speed, measured | JSON versus protobuf: size and speed, measured | You can explain what a schema is, why binary beats text on the wire, and write your first .proto file. |
| [062](../days/day-062-sets/README.md) | protoc, buf, and code generation | Generating _pb2.py and using it | protoc-gen-go, buf generate, and the generated .pb.go | protoc --cpp_out and linking libprotobuf | You can turn one .proto file into working code in all three languages with one command. |
| [063](../days/day-063-counting-with-dicts/README.md) | Messages: scalars, repeated, maps, nested, oneof | Generated classes: repeated fields, map fields, and oneof in Python | Generated structs: slices, maps, and the oneof interface pattern | Generated classes: RepeatedField, Map, and oneof cases | You can model an order with line items, an address, and a payment method that is one of three, in .proto. |
| [064](../days/day-064-grouping/README.md) | Field numbers, defaults, and schema evolution | Reading old messages with a new schema in Python | Reading old messages with a new schema in Go | Reading old messages with a new schema in C++ | You can change a schema without breaking old clients, and name the four changes that will break them. |
| [065](../days/day-065-hashing-custom-objects/README.md) | Well-known types | Timestamp, Duration, Any, Empty, and wrappers from Python | timestamppb, durationpb, anypb, and emptypb | google/protobuf/timestamp.pb.h and friends | You can represent time, absence, and a payload of unknown type in a message, in each language. |
| [066](../days/day-066-when-hashing-is-wrong/README.md) | The Go protobuf API | Python protobuf API: SerializeToString, ParseFromString, MessageToJson | proto.Marshal, proto.Unmarshal, proto.Equal, protojson, and protoreflect | SerializeToString, ParseFromString, and util::MessageToJsonString | You can marshal, unmarshal, compare, and print messages, and say what the Go API does differently. |
| [067](../days/day-067-hashing-revision/README.md) | gRPC I: a unary server in Go | grpcio: a Python server for the same service | service in .proto, protoc-gen-go-grpc, and a Go server | grpc++: a C++ server for the same service | You can define a service in .proto and serve one RPC from Go, with Python and C++ servers as comparison. |
| [068](../days/day-068-stacks/README.md) | gRPC II: clients in three languages | grpcio client with a channel and a stub | grpc.NewClient, the generated client, and connection lifecycle | grpc::CreateChannel and the generated Stub | You can call the Go server from a Python client and a C++ client. |
| [069](../days/day-069-balanced-brackets/README.md) | gRPC III: streaming | Server streaming and bidirectional streaming from Python | Server, client, and bidirectional streaming in Go | Server and bidirectional streaming in C++ | You can stream a large result and a live feed over gRPC in each language. |
| [070](../days/day-070-min-stack/README.md) | gRPC IV: errors, deadlines, metadata | grpc.StatusCode, timeouts, and metadata in Python | status.Error, codes, context deadlines, and metadata.MD | grpc::Status, deadlines, and ClientContext metadata | You can return a proper error with a code, propagate a deadline, and pass a request ID, in each language. |
| [071](../days/day-071-monotonic-stack/README.md) | gRPC V: interceptors, auth, TLS | Interceptors in grpcio and token auth | Unary and stream interceptors, per-RPC credentials, TLS | Interceptors in grpc++ and TLS credentials | You can add logging and token auth to every RPC, and secure the connection, in each language. |
| [072](../days/day-072-largest-rectangle/README.md) | gRPC and REST together | Calling a gRPC service from a FastAPI gateway | grpc-gateway: JSON transcoding, and when to expose both | Calling a gRPC service from a C++ HTTP handler | You can expose one Go service as both gRPC and REST and say when to do that. |
| [073](../days/day-073-queues/README.md) | Schema hygiene: lint, breaking checks, versioning | Packaging generated Python code | buf lint, buf breaking, module publishing, and package versioning | Packaging generated C++ code with CMake | You can enforce style and compatibility in CI and version an API like a professional team. |
| [074](../days/day-074-deques-and-window-max/README.md) | The wire format, decoded by hand | Dumping bytes and decoding them with the Python library | protowire: reading tags and varints yourself | Decoding a message with CodedInputStream | You can look at 08 96 01 and say what field and what value it is. |
| [075](../days/day-075-queue-from-stacks/README.md) | Mini project 5: an inventory service over gRPC | Python client and CLI | Go server: protobuf API, Postgres, streaming stock updates | C++ client and a load generator | You can ship a Go gRPC service with schema, migrations, tests, and clients in the other two languages. |

### Days 76-90 — Languages: performance and systems programming

| Day | Theme | Python | Go | C++ | You can |
|---:|---|---|---|---|---|
| [076](../days/day-076-lru-cache/README.md) | Benchmarking | timeit, pytest-benchmark, and pyperf | testing.B, b.N, benchstat, and allocation counts | Google Benchmark and DoNotOptimize | You can measure a function honestly in each language and say what makes a benchmark lie. |
| [077](../days/day-077-stacks-queues-revision/README.md) | CPU profiling | cProfile, py-spy, and flame graphs | pprof CPU profiles and the flame graph | perf, and flame graphs from a Release build with symbols | You can find the hottest function in a real program in each language. |
| [078](../days/day-078-nodes-and-links/README.md) | Memory profiling and leaks | tracemalloc and objgraph | pprof heap profiles, allocs, and GC traces | AddressSanitizer, LeakSanitizer, and valgrind | You can find what is holding memory in each language. |
| [079](../days/day-079-list-traversal/README.md) | Cache-friendly data layout | Why lists of objects are slow, and arrays of numbers are fast | Slices of structs versus slices of pointers, measured | Struct of arrays, contiguous memory, and false sharing | You can explain, with a measurement, why the same loop is ten times faster with a different layout. |
| [080](../days/day-080-dummy-head/README.md) | Numbers: floats, decimals, and big integers | float pitfalls, decimal, fractions, and arbitrary ints | float64, math/big, and shopspring decimal | double, long double, integer overflow, and a big-int library | You can add money correctly and say why 0.1 + 0.2 is not 0.3, in each language. |
| [081](../days/day-081-reversing-a-list/README.md) | Binary data | struct.pack, memoryview, and reading a binary header | encoding/binary, byte order, and bytes.Buffer | Byte order, std::bit_cast, and reading a binary header | You can read and write a binary file format with a header in each language. |
| [082](../days/day-082-runner-technique/README.md) | Calling across languages | ctypes and pybind11: calling C++ from Python | cgo: calling C from Go, and the cost of the boundary | extern C, and exposing a C++ library to the other two | You can write a hot loop in C++ and call it from Python and Go. |
| [083](../days/day-083-cycle-detection/README.md) | Processes, subprocesses, and signals | subprocess.run, Popen, pipes, and signal handling | os/exec, pipes, and os/signal with graceful shutdown | fork/exec, popen, and sigaction | You can run another program, capture its output, and handle Ctrl-C cleanly, in each language. |
| [084](../days/day-084-merging-and-sorting-lists/README.md) | The filesystem | pathlib, os.walk, tempfile, permissions, and watching for changes | filepath.WalkDir, os.MkdirTemp, permissions, and fsnotify | std::filesystem: walking, temp files, permissions | You can walk a tree, write atomically, and react to changes in each language. |
| [085](../days/day-085-doubly-and-circular/README.md) | Timers, tickers, and scheduling | sched, asyncio.sleep, and a cron-like loop | time.Ticker, time.AfterFunc, and a scheduler goroutine | std::this_thread::sleep_until, and a timer wheel in outline | You can run a job every minute, reliably, in each language, and say what drift is. |
| [086](../days/day-086-linked-lists-revision/README.md) | Streaming large data | Generators, iterators over files, and chunked reads | io.Reader, io.Writer, io.Pipe, and composing readers | std::istream, iterators, and chunked reads | You can process a 50 GB file with constant memory in each language. |
| [087](../days/day-087-recursion-leap-of-faith/README.md) | Other data formats | csv, tomllib, and PyYAML | encoding/csv, BurntSushi/toml, and yaml.v3 | fast-cpp-csv-parser, toml++, and yaml-cpp | You can read the three most common config and data formats in each language. |
| [088](../days/day-088-the-call-stack/README.md) | Templates and code generation | Jinja2 for text, HTML, and generating code | text/template, html/template, and go generate | Generating C++ with a script, and CMake configure_file | You can render a report from data and generate source code from a table, in each language. |
| [089](../days/day-089-recursion-that-terminates/README.md) | Plugins | importlib, entry points, and a plugin registry | Interfaces plus registration, and why the plugin package is avoided | dlopen, shared libraries, and a C plugin ABI | You can let someone add behaviour to your program without recompiling it, in each language. |
| [090](../days/day-090-recursion-on-arrays/README.md) | Mini project 6: a log analytics pipeline | Ingest, parse, and aggregate with generators and multiprocessing | Ingest, parse, and aggregate with a channel pipeline | Ingest, parse, and aggregate with a thread pool and mmap | You can build the same pipeline in all three, benchmark them, and explain the numbers. |

### Days 91-105 — Languages: messaging, resilience, and deployment

| Day | Theme | Python | Go | C++ | You can |
|---:|---|---|---|---|---|
| [091](../days/day-091-subsets/README.md) | Message brokers: Kafka | confluent-kafka: produce, consume, commit | franz-go: produce, consume, commit | librdkafka: produce, consume, commit | You can publish and consume events with a consumer group in each language. |
| [092](../days/day-092-permutations/README.md) | Pub/sub patterns | Consumer groups, partitions, and ordering guarantees from Python | Consumer groups, partitions, and ordering guarantees from Go | Consumer groups, partitions, and ordering guarantees from C++ | You can explain at-least-once versus at-most-once and write an idempotent consumer in each language. |
| [093](../days/day-093-combinations/README.md) | Background jobs | Celery or arq: enqueue, retry, and schedule | asynq or a hand-built worker with Redis | A worker process pulling from Redis lists | You can move slow work out of the request path in each language. |
| [094](../days/day-094-backtracking/README.md) | WebSockets | websockets and FastAPI WebSocket routes | gorilla/websocket or nhooyr, and a broadcast hub | Boost.Beast or uWebSockets, and a broadcast hub | You can push live updates to a browser from each language. |
| [095](../days/day-095-n-queens/README.md) | Rate limiting and retries | A token bucket, and tenacity for retries with backoff | golang.org/x/time/rate, and retries with jitter | A token bucket class, and retries with jitter | You can protect a service from too many calls and retry safely, in each language. |
| [096](../days/day-096-grid-backtracking/README.md) | Circuit breakers and idempotency keys | A circuit breaker class and idempotency keys in a store | gobreaker, and idempotency keys in a store | A circuit breaker class and idempotency keys in a store | You can stop cascading failure and make a payment endpoint safe to retry, in each language. |
| [097](../days/day-097-recursion-revision/README.md) | Observability: metrics and traces | prometheus_client and OpenTelemetry | prometheus/client_golang and OpenTelemetry | prometheus-cpp and OpenTelemetry C++ | You can expose a metrics endpoint and a trace that crosses two services, in each language. |
| [098](../days/day-098-what-a-tree-is/README.md) | Health checks and graceful shutdown | Liveness and readiness routes, and shutdown hooks | Health endpoints, http.Server.Shutdown, and draining | Health endpoints, stopping the server, and draining | You can stop a service without dropping in-flight requests, in each language. |
| [099](../days/day-099-binary-trees-in-code/README.md) | Config, secrets, and feature flags | Secrets from the environment, a vault client, and a flag store | Secrets from the environment, a vault client, and a flag store | Secrets from the environment, a vault client, and a flag store | You can ship a feature dark and turn it on for 1% of users, in each language. |
| [100](../days/day-100-dfs-traversals/README.md) | Service-to-service: discovery and load balancing | gRPC client-side load balancing from Python | gRPC resolvers, round-robin, and DNS-based discovery | gRPC client-side load balancing from C++ | You can have three instances of a service and spread calls across them, from each language. |
| [101](../days/day-101-bfs-level-order/README.md) | Distributed locks and leader election | Redis locks and their limits | etcd leases, leader election, and the lock lease trap | Redis locks and their limits | You can ensure only one instance runs the nightly job, and say why that is hard. |
| [102](../days/day-102-height-and-diameter/README.md) | The outbox pattern and event sourcing | Outbox table plus relay in Python | Outbox table plus relay in Go | Outbox table plus relay in C++ | You can publish an event and write to the database atomically, in each language. |
| [103](../days/day-103-tree-comparisons/README.md) | Kubernetes for your service | Deployment, Service, probes, and resource limits | Deployment, Service, probes, and resource limits | Deployment, Service, probes, and resource limits | You can run each of your three services on a local cluster with probes and limits. |
| [104](../days/day-104-tree-path-problems/README.md) | CI for three languages | GitHub Actions: uv, ruff, mypy, pytest, and coverage | GitHub Actions: go vet, staticcheck, test -race, and coverage | GitHub Actions: CMake, sanitizers, and ctest | You can make every push run the tests for all three languages and block a bad merge. |
| [105](../days/day-105-lowest-common-ancestor/README.md) | Mini project 7: orders, events, and notifications | Python notification worker consuming Kafka | Go order service with gRPC, Postgres, and the outbox | C++ pricing service called over gRPC | You can ship three services that talk over gRPC and Kafka, with CI and health checks. |

### Days 106-135 — Languages: idiomatic depth and design

| Day | Theme | Python | Go | C++ | You can |
|---:|---|---|---|---|---|
| [106](../days/day-106-bst-property/README.md) | Data modelling idioms | dataclasses, attrs, pydantic, and when each | Struct tags, validation, and functional options | Aggregates, designated initialisers, and builder structs | You can model a config or a record idiomatically in each language, with validation. |
| [107](../days/day-107-bst-operations/README.md) | Cleanup: context managers, defer, RAII | with, __enter__/__exit__, and contextlib | defer, its evaluation order, and the loop trap | RAII, scope guards, and destructors that never throw | You can guarantee a file closes or a lock releases on every path, in each language. |
| [108](../days/day-108-validating-a-bst/README.md) | Encapsulation | @property, __slots__, name mangling, and descriptors | Unexported fields, getters by convention, and method values | private, const methods, static members, and friend | You can hide a field and expose a computed one in each language. |
| [109](../days/day-109-balanced-trees/README.md) | Static typing, deep | mypy strict, Protocol, TypeVar bounds, and overload | Generic constraints, type sets, and interface embedding | Concepts, requires clauses, and constrained auto | You can express 'any type with a Len method' in each language and get a compile-time error when it is wrong. |
| [110](../days/day-110-trees-from-traversals/README.md) | Async, deep | TaskGroup, semaphores, cancellation, and aiohttp | errgroup, sync.Once, semaphores, and singleflight | Futures, promises, and a coroutine task type | You can run bounded concurrent work with error propagation in each language. |
| [111](../days/day-111-serialise-a-tree/README.md) | Parallelism and the scheduler | multiprocessing, the GIL, and free-threaded Python | GOMAXPROCS, the M:P:G scheduler, and preemption | std::execution policies and hardware_concurrency | You can use every core in each language and say what stops you from doing so. |
| [112](../days/day-112-trees-revision/README.md) | Standard library tour I: algorithms | itertools, functools, bisect, and heapq | slices, maps, sort, and container/heap | <algorithm>, <ranges>, <numeric> | You can reach for the standard function instead of writing the loop, in each language. |
| [113](../days/day-113-the-heap/README.md) | Standard library tour II: containers | collections: deque, Counter, defaultdict, OrderedDict | container/list, container/ring, and why maps and slices win | deque, list, set, priority_queue, and unordered containers | You can choose the right container by the operation you need, in each language. |
| [114](../days/day-114-heapify/README.md) | Standard library tour III: text | str methods, textwrap, string.Template, and difflib | strings, strconv, unicode, and text/tabwriter | std::string, std::string_view, std::format, and <charconv> | You can parse, transform, and format text without a third-party library, in each language. |
| [115](../days/day-115-heapq/README.md) | Publishing a library | PyPI, versioning, and a clean public API | Module proxy, semantic import versioning, and v2 paths | vcpkg or Conan, a CMake package config, and an install target | You can publish a library someone else can install, in each language. |
| [116](../days/day-116-top-k/README.md) | Documentation | Docstrings, Sphinx or mkdocs, and doctest | godoc conventions, examples that run as tests | Doxygen and a README that builds | You can document a package so a stranger can use it, in each language. |
| [117](../days/day-117-merge-k-sorted/README.md) | Linting and static analysis | ruff, mypy, and pre-commit | vet, staticcheck, golangci-lint | clang-tidy, cppcheck, and warnings as errors | You can make the tools catch a real bug before a human reads the code, in each language. |
| [118](../days/day-118-two-heaps/README.md) | Fuzz testing | hypothesis for property-based tests | go test -fuzz and the corpus | libFuzzer with sanitizers | You can let the computer find the input that breaks your parser, in each language. |
| [119](../days/day-119-heaps-revision/README.md) | Test strategy | Unit, integration, and end-to-end with pytest markers | Unit, integration with build tags, and end-to-end | Unit, integration, and end-to-end with CTest labels | You can say what to test at which level, and keep the suite fast, in each language. |
| [120](../days/day-120-the-trie/README.md) | Mini project 8: a rate-limiter library | A published Python package with docs and tests | A published Go module with docs and tests | A C++ library with a CMake package and tests | You can ship a small, correct, documented library in all three languages. |
| [121](../days/day-121-trie-operations/README.md) | Design patterns I: strategy, factory, builder | Strategy as functions, factories as classmethods, builders as kwargs | Strategy as interfaces, factory functions, functional options | Strategy with virtual or templates, factories, fluent builders | You can implement the three most-asked creational patterns idiomatically in each language. |
| [122](../days/day-122-autocomplete/README.md) | Design patterns II: observer, decorator, adapter | Observer with callbacks, decorator as wrapper, adapter as class | Observer with channels, decorator as wrapping interface, adapter | Observer with std::function, decorator, adapter | You can implement the three most-asked structural patterns idiomatically in each language. |
| [123](../days/day-123-word-search-ii/README.md) | Design patterns III: singleton, state, command | Module-level singletons, state as enum plus match, command as callable | sync.Once, state as interface, command as func | Meyers singleton, state as variant, command as std::function | You can implement the three most-asked behavioural patterns and say when a singleton is a mistake. |
| [124](../days/day-124-tries-revision/README.md) | Functional style | map, filter, reduce, comprehensions, and pure functions | Higher-order functions, and why Go keeps it plain | Ranges, views, and pure functions | You can write a data transformation as a pipeline of pure functions in each language. |
| [125](../days/day-125-what-a-graph-is/README.md) | Dependency injection | Constructor injection with Protocols, and pytest fixtures | Constructor injection with interfaces, and wire in outline | Constructor injection with interfaces, and templates | You can swap a real database for a fake in a test without a framework, in each language. |
| [126](../days/day-126-graph-representation/README.md) | Clean architecture | Domain, application, infrastructure layers in a Python service | Domain, application, infrastructure layers in a Go service | Domain, application, infrastructure layers in a C++ service | You can lay out a service so the business rules never import the database, in each language. |
| [127](../days/day-127-graph-bfs/README.md) | Error architecture | A domain exception hierarchy mapped to HTTP codes | Typed errors, sentinel errors, and mapping to gRPC codes | std::expected with a domain error enum, mapped to codes | You can design how errors flow from the database to the user, in each language. |
| [128](../days/day-128-graph-dfs/README.md) | Twelve-factor services | Config, logs to stdout, stateless processes, in Python | Config, logs to stdout, stateless processes, in Go | Config, logs to stdout, stateless processes, in C++ | You can name the twelve factors and point at where each of your services obeys them. |
| [129](../days/day-129-connected-components/README.md) | Security basics | Input validation, injection, secrets, and pickle | Input validation, injection, secrets, and the crypto packages | Bounds checking, undefined behaviour, and the sanitizers | You can name the top five ways each language gets exploited and how you prevent each. |
| [130](../days/day-130-grids-are-graphs/README.md) | Reading idiomatic code | A tour of a well-written Python package | A tour of a well-written Go package from the standard library | A tour of a well-written C++ library | You can read a real codebase in each language and say what is idiomatic and what is not. |
| [131](../days/day-131-unweighted-shortest-path/README.md) | Go, deep: channel patterns | The same patterns with asyncio queues | Done channels, fan-in, fan-out, select with default, and time.After | The same patterns with condition variables | You can write the five classic Go concurrency patterns from memory and explain each with a diagram. |
| [132](../days/day-132-undirected-cycles/README.md) | C++, deep: templates and constexpr | The nearest Python idea: generics and runtime dispatch | The nearest Go idea: generics and code generation | Templates, CRTP, concepts, constexpr, and compile-time tables | You can write a compile-time lookup table and a CRTP base class, and say what each buys. |
| [133](../days/day-133-directed-cycles/README.md) | Python, deep: the object model | Descriptors, metaclasses, __new__, and the import system | The nearest Go idea: reflection and struct tags | The nearest C++ idea: templates and traits | You can explain how a dataclass or an ORM works underneath, and write a tiny one. |
| [134](../days/day-134-topological-sort/README.md) | One program, three languages, measured | A JSON log parser in Python, profiled | A JSON log parser in Go, profiled | A JSON log parser in C++, profiled | You can show the same task at three speeds and explain every gap with a profile. |
| [135](../days/day-135-dependency-problems/README.md) | Mini project 9: a key-value store with a wire protocol | A KV server and client in Python | A KV server and client in Go | A KV server and client in C++ | You can design a small binary protocol and ship a server and client for it in all three. |

### Days 136-165 — Languages: six five-day builds

| Day | Theme | Python | Go | C++ | You can |
|---:|---|---|---|---|---|
| [136](../days/day-136-dijkstra/README.md) | Build A, day 1: a distributed cache. Design | Requirements and the Python client interface | Requirements, the .proto API, and the Go server skeleton | Requirements and the C++ client interface | You can write the requirements and the protobuf API for a distributed cache. |
| [137](../days/day-137-bellman-ford/README.md) | Build A, day 2: the server core | Property tests against the server | Sharded maps, TTLs, eviction, and the gRPC service | A load generator | You can implement an LRU-with-TTL store behind a gRPC service in Go. |
| [138](../days/day-138-union-find/README.md) | Build A, day 3: clients | A Python client with connection pooling and retries | A Go client library | A C++ client with connection pooling and retries | You can write a client library in each language against the same protobuf API. |
| [139](../days/day-139-minimum-spanning-trees/README.md) | Build A, day 4: consistent hashing | Consistent hashing simulation in Python | A hash ring and node add/remove in Go | The hash ring in C++ | You can spread keys over N nodes so adding one moves only 1/N of them. |
| [140](../days/day-140-bipartite-graphs/README.md) | Build A, day 5: ship it | Docs and a demo notebook | Docker, metrics, and CI | Benchmarks | You can ship the cache with docs, metrics, containers, and a README a stranger could use. |
| [141](../days/day-141-multi-source-bfs/README.md) | Build B, day 1: a job queue. Design | Requirements and the FastAPI submit/status API | Requirements, the .proto job schema, and the Go worker skeleton | Requirements and the C++ compute worker skeleton | You can design a job system with a submit API, a queue, workers, and status. |
| [142](../days/day-142-graphs-revision/README.md) | Build B, day 2: the queue and the worker | Submit, poll, and cancel from Python | Redis Streams or Kafka, the worker loop, and acknowledgements | The C++ worker consuming protobuf jobs | You can implement at-least-once delivery with acknowledgements and visibility timeouts. |
| [143](../days/day-143-what-dp-is/README.md) | Build B, day 3: retries and dead letters | Retry policy in the API | Exponential backoff, dead-letter queue, and poison messages | Idempotent compute in C++ | You can retry failed jobs safely and quarantine the ones that will never succeed. |
| [144](../days/day-144-fibonacci-dp/README.md) | Build B, day 4: scheduling and priorities | Cron-style scheduling from Python | Priority queues, delayed jobs, and a scheduler loop | Priority handling in the C++ worker | You can schedule a job for later and run urgent ones first. |
| [145](../days/day-145-climbing-stairs/README.md) | Build B, day 5: ship it | A dashboard page | Metrics, graceful shutdown, and CI | Benchmarks | You can ship the job system with a dashboard, metrics, and CI. |
| [146](../days/day-146-house-robber/README.md) | Build C, day 1: a storage engine. Design | Python bindings plan | Go bindings plan | Requirements, the on-disk format, and the C++ engine skeleton | You can design a log-structured storage engine and its file format. |
| [147](../days/day-147-finding-the-state/README.md) | Build C, day 2: WAL and memtable | A pure-Python reference implementation for testing | A pure-Go reference implementation for testing | Write-ahead log, fsync, and a sorted in-memory table | You can make writes durable and explain what fsync guarantees. |
| [148](../days/day-148-knapsack/README.md) | Build C, day 3: SSTables and compaction | Reading SSTables from Python | Reading SSTables from Go | Flushing, sorted files, bloom filters, and compaction | You can flush the memtable to disk and merge files without losing data. |
| [149](../days/day-149-subset-sum/README.md) | Build C, day 4: bindings | pybind11 bindings and a Python API | cgo bindings and a Go API | extern C surface and a stable ABI | You can call the C++ engine from Python and Go. |
| [150](../days/day-150-coin-change/README.md) | Build C, day 5: ship it | Tests through the bindings | Tests through the bindings | Crash tests, benchmarks, and docs | You can prove the engine survives a crash and ship it with benchmarks. |
| [151](../days/day-151-counting-ways/README.md) | Build D, day 1: a chat system. Design | Requirements and the web client plan | Requirements, the .proto messages, and the Go hub | Requirements and the C++ presence service | You can design a chat system with rooms, presence, and history. |
| [152](../days/day-152-longest-increasing-subsequence/README.md) | Build D, day 2: gRPC bidirectional streams | A Python terminal client on the stream | The room hub with bidirectional streaming | A C++ terminal client on the stream | You can hold thousands of open streams and fan a message out to a room. |
| [153](../days/day-153-longest-common-subsequence/README.md) | Build D, day 3: WebSockets for the browser | A FastAPI WebSocket gateway to the gRPC hub | WebSocket to gRPC bridging | Presence updates over gRPC | You can bridge a browser to the gRPC hub. |
| [154](../days/day-154-edit-distance/README.md) | Build D, day 4: history and presence | History queries | Postgres history, cursor pagination, and Redis presence | The presence service with heartbeats | You can page through history and know who is online. |
| [155](../days/day-155-string-dp/README.md) | Build D, day 5: ship it | Load test with locust | Metrics, tracing, and CI | Benchmarks | You can ship the chat system and show a trace of one message end to end. |
| [156](../days/day-156-grid-dp/README.md) | Build E, day 1: an observability toolkit. Design | Requirements and the dashboard plan | Requirements, the .proto metrics schema, and the Go agent | Requirements and the C++ collector skeleton | You can design a metrics agent, a collector, and a dashboard. |
| [157](../days/day-157-stock-dp/README.md) | Build E, day 2: the agent | A Python client library for custom metrics | Collecting CPU, memory, and app metrics; shipping over gRPC | Receiving and buffering in C++ | You can collect and ship metrics from a host every ten seconds. |
| [158](../days/day-158-interval-dp/README.md) | Build E, day 3: time-series storage | Querying from Python | Batching and forwarding | A columnar time-series store with downsampling | You can store a million points a minute and query a day in milliseconds. |
| [159](../days/day-159-dp-on-trees/README.md) | Build E, day 4: the dashboard and alerts | A FastAPI dashboard and an alert evaluator | Alert rules and notification fan-out | Query API in C++ | You can draw a graph and fire an alert on a threshold. |
| [160](../days/day-160-bitmask-dp/README.md) | Build E, day 5: ship it | Docs and demo | CI and containers | Benchmarks | You can ship the toolkit and monitor your own earlier projects with it. |
| [161](../days/day-161-dp-space-optimisation/README.md) | Build F, day 1: a tiny language. The lexer | The lexer in Python | The lexer in Go | The lexer in C++ | You can turn source text into tokens in each language. |
| [162](../days/day-162-recognising-dp/README.md) | Build F, day 2: the parser | A recursive-descent parser in Python | A recursive-descent parser in Go | A recursive-descent parser in C++ | You can turn tokens into a tree with correct precedence, in each language. |
| [163](../days/day-163-dp-revision/README.md) | Build F, day 3: the evaluator | A tree-walking evaluator with environments | A tree-walking evaluator with environments | A tree-walking evaluator with std::variant values | You can run programs in your language, with variables, functions, and closures. |
| [164](../days/day-164-greedy-idea/README.md) | Build F, day 4: errors and tests | Error messages with line numbers, and a test suite | Error messages with line numbers, and a test suite | Error messages with line numbers, and a test suite | You can report a syntax error a human can act on, and prove the interpreter with tests. |
| [165](../days/day-165-proving-greedy/README.md) | Build F, day 5: ship it | A REPL and docs | A REPL and docs | A REPL, benchmarks, and docs | You can ship an interpreter in three languages and compare their speed. |

### Days 166-180 — Languages: interview prep and the capstone

| Day | Theme | Python | Go | C++ | You can |
|---:|---|---|---|---|---|
| [166](../days/day-166-interval-scheduling/README.md) | Python interview questions | The forty questions: GIL, memory, decorators, generators, typing | How Go answers the same questions | How C++ answers the same questions | You can answer the forty most-asked Python questions out loud. |
| [167](../days/day-167-merging-intervals/README.md) | Go interview questions | How Python answers the same questions | The forty questions: goroutines, channels, interfaces, nil, slices, GC | How C++ answers the same questions | You can answer the forty most-asked Go questions out loud. |
| [168](../days/day-168-sweep-line/README.md) | C++ interview questions | How Python answers the same questions | How Go answers the same questions | The forty questions: virtual, smart pointers, move, RAII, UB, templates | You can answer the forty most-asked C++ questions out loud. |
| [169](../days/day-169-jump-game/README.md) | Choosing a language | When Python: the honest case | When Go: the honest case | When C++: the honest case | You can pick a language for a given job and defend it in two minutes. |
| [170](../days/day-170-greedy-revision/README.md) | Reading production code | A guided read of a popular Python service codebase | A guided read of a popular Go service codebase | A guided read of a popular C++ library | You can open a large unfamiliar codebase in each language and find where a request is handled. |
| [171](../days/day-171-binary-and-bits/README.md) | Capstone, day 1: an order platform. Requirements and API | The FastAPI gateway contract | The protobuf APIs for orders, inventory, and payments | The C++ pricing engine contract | You can write the requirements and every API of the capstone before writing a line of logic. |
| [172](../days/day-172-bit-tricks/README.md) | Capstone, day 2: the gateway | FastAPI gateway: auth, validation, and gRPC calls | Gateway middleware for auth tokens | Nothing today; C++ waits for pricing | You can accept a request at the edge, validate it, and forward it over gRPC. |
| [173](../days/day-173-xor/README.md) | Capstone, day 3: the order service | Contract tests from Python | Order service: Postgres, transactions, and the outbox | Contract tests from C++ | You can create an order atomically with an event that will definitely be published. |
| [174](../days/day-174-number-theory/README.md) | Capstone, day 4: the pricing engine | Price rules loaded from Python tooling | Calling pricing over gRPC with deadlines | The C++ pricing engine: rules, discounts, and sub-millisecond latency | You can build a service that answers in under a millisecond and prove it. |
| [175](../days/day-175-combinatorics/README.md) | Capstone, day 5: events and workers | Notification and analytics workers on Kafka | Inventory worker with idempotent consumption | Nothing today; C++ is done | You can react to an order event in two services without double-processing. |
| [176](../days/day-176-bits-maths-revision/README.md) | Capstone, day 6: resilience | Timeouts, retries, and a circuit breaker in the gateway | Deadlines, retries, and idempotency keys across services | Load shedding in the pricing engine | You can kill any one service and show the platform degrade instead of fall over. |
| [177](../days/day-177-the-patterns-on-one-page/README.md) | Capstone, day 7: observe and deploy | Tracing through the gateway | Tracing across gRPC and Kafka; Kubernetes manifests | Metrics from the engine | You can deploy the whole platform to a local cluster and follow one order through a trace. |
| [178](../days/day-178-thinking-out-loud/README.md) | Capstone, day 8: load test and review | Load test with locust and a report | Profile under load and fix the top hotspot | Profile under load and fix the top hotspot | You can state the platform's throughput and latency and what you fixed to get there. |
| [179](../days/day-179-full-coding-mock/README.md) | Your portfolio | READMEs, demos, and the two-minute pitch for each project | READMEs, demos, and the two-minute pitch for each project | READMEs, demos, and the two-minute pitch for each project | You can present any of your ten projects in two minutes and answer questions for ten. |
| [180](../days/day-180-final-revision/README.md) | Final revision | The hundred questions, Python | The hundred questions, Go | The hundred questions, C++ | You can answer the hundred questions across the three languages out loud, from memory. |
