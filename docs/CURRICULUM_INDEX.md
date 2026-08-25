# Krama — the curriculum index

180 days. Each day teaches one DSA topic and one system design topic, side by side.
This file is generated from `scripts/curriculum.py` — edit that, then run
`python scripts/build_skeleton.py`.

- **Days 1-96** build the foundations and the low-level design half.
- **Days 97-180** build distributed systems and the high-level design half.

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

---

## Every day

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
