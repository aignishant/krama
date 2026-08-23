# Problem Index

The whole curriculum's problem set, in one place, organised by **concept ID prefix**. Day ladders
are *selected* from here, never invented at writing time — that is what stops one problem
appearing on four days and stops a concept from ending up with none.

```bash
./k ladder BSR      # every problem for the binary-search phase
./k ladder DPA-09   # every problem testing one concept
```

**Columns.** `Lv` is E/M/H. `ID` is the concept the problem primarily tests — the day that owns
that ID is the day whose ladder may use it. `Really testing` is the line that must appear beside
the problem in a day's ladder, so that failing it tells you which document to re-read.

**Sources.** `LC` = LeetCode number. `own` = you implement it from scratch, no judge; the lab
tests are the judge. A problem may be **cross-listed** — it appears under its primary ID and is
marked `↺` where a later phase reuses it. Reusing a problem on a later day is allowed and good;
what is not allowed is two days claiming it as *new*.

**Never paste a problem statement into a lesson.** Title, source, and the testing line only.

---

## Track I

### `CPX` — Computation and Cost · Days 1–8

Phase 1 is a *modelling* phase: there is no data structure yet and no technique to drill, so its
problems are written rather than judged. `own` here means paper, a REPL, or the day's `lab/` —
what is graded is whether you can **state** something precisely, not whether a site turns green.
Days 2–8 add their rows as they are written.

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Specification or procedure? — twelve statements | own | E | CPX-01 | sorting statements into "says what must be true at the end" and "says what to do next" |
| Second largest, tie policy stated first | own | E | CPX-01 | naming a result vs producing one; deciding `[7, 7]` and `[7]` before writing a line |
| One specification, three procedures | own | M | CPX-01 | producing three procedures for one specification and stating the cost gap out loud |
| The definition that does not terminate | own | M | CPX-01 | a recursive specification transcribed literally, and the `RecursionError` it earns |
| Maximum with a comparison counter | own | E | CPX-01 | why the count never varies with the data, and what that says about best vs worst case |
| Which of these is one operation? | own | E | CPX-02 | the rule that a step may be charged 1 only if its cost does not grow with `n` |
| Count the model operations of a reversal | own | E | CPX-02 | charging every read, write and comparison, and reaching a closed form |
| What is `n` here? — eight inputs | own | E | CPX-02 | choosing the size parameter for a grid, a graph, a string, and a single integer |
| Trial division, priced in digits | own | M | CPX-02 | polynomial in the value, exponential in the size |
| The cache cliff, measured | own | M | CPX-02 | identical operation counts in two orders, and the size at which the ratio moves |
| Invariant for a loop you did not write | own | E | CPX-03 | stating the invariant of three unfamiliar loops from the code alone, before running them |
| Where the invariant first breaks | own | E | CPX-03 | naming the exact iteration at which a proposed invariant stops being preserved |
| Exit condition, negated | own | E | CPX-03 | deriving the postcondition from invariant and the negated guard, and noticing when it does not follow |
| The strongest true invariant | own | M | CPX-03 | strengthening a preserved-but-useless claim until it implies the postcondition |
| Find the variant — five loops | own | M | CPX-03 | naming the decreasing measure for each, and identifying the one loop that has none |
| The loop that stops for the wrong reason | own | M | CPX-03 | termination resting on a value the invariant never mentions, and what breaks when the input changes |
| Prove the maximum you wrote on Day 1 | own | E | CPX-03 | writing initialization, maintenance and exit for a loop you already trust |
| Partial, total, and the bug report | own | M | CPX-03 | telling a wrong-answer failure from a never-returns failure by symptom alone, out loud |

### `ARR` — Arrays and Dynamic Arrays · Days 15–20

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Remove Duplicates from Sorted Array | LC 26 | E | ARR-06 | the write-pointer invariant on in-place compaction |
| Remove Element | LC 27 | E | ARR-06 | same invariant, different predicate |
| Move Zeroes | LC 283 | E | ARR-06 | stability of the surviving order |
| Merge Sorted Array | LC 88 | E | ARR-06 | filling backwards to avoid an O(n) shift per insert |
| Rotate Array | LC 189 | M | ARR-06 | the triple-reversal identity, and O(1) extra space |
| Plus One | LC 66 | E | ARR-01 | carry propagation and the all-nines resize |
| Product of Array Except Self | LC 238 | M | ARR-06 | two directional passes replacing division |
| First Missing Positive | LC 41 | H | ARR-06 | using the array itself as a hash table |
| Find All Numbers Disappeared | LC 448 | E | ARR-06 | using the sign bit of the array itself as the marker |
| Spiral Matrix | LC 54 | M | ARR-07 | four boundary variables and their invariants |
| Rotate Image | LC 48 | M | ARR-07 | transpose then reverse each row, with no second matrix |
| Set Matrix Zeroes | LC 73 | M | ARR-08 | O(1) space via first row/column as markers |
| Transpose Matrix | LC 867 | E | ARR-07 | row-major indexing, and why the output shape differs |
| Sparse Matrix Multiplication | LC 311 | M | ARR-07 | skipping zeros, and what "sparse" costs |
| `DynamicArray` from scratch | own | M | ARR-09 | growth factor, amortized append, the resize copy |

### `STR` — Strings and Text · Days 21–26

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Reverse String | LC 344 | E | STR-03 | in-place on a mutable sequence vs Python's immutability |
| Valid Palindrome | LC 125 | E | STR-04 | two pointers plus "what counts as a character" |
| Valid Palindrome II | LC 680 | E | STR-04 | one branch point, and resisting the O(n²) retry |
| Longest Common Prefix | LC 14 | E | STR-04 | vertical vs horizontal scanning, and early exit |
| Find the Index of First Occurrence | LC 28 | E | STR-04 | the naive matcher, before KMP exists ↺ TRI-04 |
| Valid Anagram | LC 242 | E | STR-06 | frequency vector vs sorting, and the Unicode caveat |
| Group Anagrams | LC 49 | M | STR-06 | choosing a canonical key ↺ HSH-01 |
| Ransom Note | LC 383 | E | STR-06 | counting, and the direction of the containment |
| Reverse Words in a String | LC 151 | M | STR-05 | in-place-ish word reversal and whitespace edge cases |
| String Compression | LC 443 | M | STR-05 | run-length with a write pointer, multi-digit counts |
| Add Strings | LC 415 | E | STR-01 | digit arithmetic without integer conversion |
| Multiply Strings | LC 43 | M | STR-01 | positional accumulation; the schoolbook algorithm |
| Zigzag Conversion | LC 6 | M | STR-05 | building with buckets instead of concatenation |
| Longest Palindromic Substring | LC 5 | M | STR-07 | expand-around-centre, and the even/odd split ↺ TRI-06 |
| Palindromic Substrings | LC 647 | M | STR-07 | counting centres rather than enumerating substrings |
| Text Justification | LC 68 | H | STR-05 | specification density; where the ambiguity actually is |

### `TWP` — Two Pointers and Sliding Window · Days 27–32

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Two Sum II — Input Array Is Sorted | LC 167 | M | TWP-01 | the converging invariant, and why sortedness licenses it |
| 3Sum | LC 15 | M | TWP-01 | fixing one index and reducing; duplicate skipping |
| 3Sum Closest | LC 16 | M | TWP-01 | tracking a best while converging |
| 4Sum | LC 18 | M | TWP-01 | generalising the reduction, and overflow-free comparison |
| Container With Most Water | LC 11 | M | TWP-01 | why moving the shorter side is provably safe |
| Trapping Rain Water | LC 42 | H | TWP-01 | the prefix-max invariant ↺ STQ-06 |
| Sort Colors | LC 75 | M | TWP-01 | Dutch national flag, three regions, one pass |
| Squares of a Sorted Array | LC 977 | E | TWP-01 | producing a procedure instead of naming `sorted()` |
| Linked List Cycle | LC 141 | E | TWP-02 | fast/slow, and why they must meet ↺ LNK-04 |
| Middle of the Linked List | LC 876 | E | TWP-02 | the off-by-one on even length |
| Happy Number | LC 202 | E | TWP-02 | cycle detection on an implicit sequence |
| Minimum Size Subarray Sum | LC 209 | M | TWP-04 | expand/contract, and why total work stays O(n) |
| Longest Substring Without Repeating | LC 3 | M | TWP-04 | window with a last-seen map; the jump vs step choice |
| Longest Repeating Character Replacement | LC 424 | M | TWP-04 | a window validated by max-count, not by rescanning |
| Max Consecutive Ones III | LC 1004 | M | TWP-04 | the non-shrinking window trick |
| Minimum Window Substring | LC 76 | H | TWP-04 | a "satisfied" counter instead of comparing maps |
| Permutation in String | LC 567 | M | TWP-03 | fixed window, incremental frequency update |
| Find All Anagrams in a String | LC 438 | M | TWP-03 | same window, all positions reported |
| Fruit Into Baskets | LC 904 | M | TWP-05 | at-most-K distinct, stated plainly |
| Subarrays with K Different Integers | LC 992 | H | TWP-06 | exactly(K) = atMost(K) − atMost(K−1) |

### `PFX` — Prefix Sums and Difference Arrays · Days 33–36

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Running Sum of 1d Array | LC 1480 | E | PFX-01 | the accumulator as invented state |
| Find Pivot Index | LC 724 | E | PFX-01 | total − prefix − self, in one pass |
| Range Sum Query — Immutable | LC 303 | E | PFX-01 | precompute-once, query-many as a cost trade |
| Range Sum Query 2D — Immutable | LC 304 | M | PFX-03 | inclusion–exclusion on four corners |
| Subarray Sum Equals K | LC 560 | M | PFX-04 | prefix + hash map; why sliding window fails on negatives |
| Continuous Subarray Sum | LC 523 | M | PFX-04 | prefix modulo, and the pigeonhole argument |
| Contiguous Array | LC 525 | M | PFX-04 | re-encoding 0 as −1 to turn a count into a sum |
| Maximum Size Subarray Sum Equals k | LC 325 | M | PFX-04 | first-occurrence storage, not last |
| Corporate Flight Bookings | LC 1109 | M | PFX-02 | difference array: range update, point query |
| Car Pooling | LC 1094 | M | PFX-02 | events on a timeline as a difference array |
| Number of Submatrices That Sum to Target | LC 1074 | H | PFX-03 | collapsing 2D to 1D, then PFX-04 |

### `BSR` — Binary Search · Days 37–43

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Binary Search | LC 704 | E | BSR-01 | the `[lo, hi]` invariant, stated aloud |
| Search Insert Position | LC 35 | E | BSR-03 | lower_bound, and what `lo` means at termination |
| First Bad Version | LC 278 | E | BSR-01 | a predicate you cannot see the array behind |
| Find First and Last Position | LC 34 | M | BSR-03 | two boundary searches, not one search plus a scan |
| Find K Closest Elements | LC 658 | M | BSR-03 | searching for a window start, not an element |
| Time Based Key-Value Store | LC 981 | M | BSR-03 | upper_bound on a sorted timestamp list |
| Search in Rotated Sorted Array | LC 33 | M | BSR-06 | structure without sortedness; which half is ordered |
| Search in Rotated Sorted Array II | LC 81 | M | BSR-06 | duplicates destroying the decision, and the O(n) worst case |
| Find Minimum in Rotated Sorted Array | LC 153 | M | BSR-06 | comparing to `hi`, not to `lo` |
| Find Peak Element | LC 162 | M | BSR-06 | binary search with no sorted order at all |
| Sqrt(x) | LC 69 | E | BSR-04 | search on the answer, integer domain |
| Koko Eating Bananas | LC 875 | M | BSR-04 | naming the monotone predicate before coding |
| Capacity To Ship Packages Within D Days | LC 1011 | M | BSR-04 | the lower bound of the search range is not zero |
| Split Array Largest Sum | LC 410 | H | BSR-04 | search-on-answer replacing a DP ↺ DPA-03 |
| Kth Smallest Element in a Sorted Matrix | LC 378 | M | BSR-04 | counting as the predicate ↺ HEP-06 |
| Median of Two Sorted Arrays | LC 4 | H | BSR-03 | partitioning both arrays; the empty-side sentinels |
| Minimize Max Distance to Gas Station | LC 774 | H | BSR-05 | float search, and choosing the epsilon honestly |

### `SRT` — Sorting · Days 44–51

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Sort an Array | LC 912 | M | SRT-02 | merge sort written out, and the merge step's invariant |
| Merge Intervals | LC 56 | M | SRT-02 | the sorting key deciding the whole algorithm |
| Insert Interval | LC 57 | M | SRT-02 | three phases, and where the ambiguity lives |
| Largest Number | LC 179 | M | SRT-03 | a custom comparator, and proving it is a valid ordering |
| Custom Sort String | LC 791 | M | SRT-08 | counting sort with an externally supplied order |
| Sort Characters By Frequency | LC 451 | M | SRT-08 | bucket by count instead of sorting by count |
| Relative Sort Array | LC 1122 | E | SRT-08 | counting sort where the alphabet is small and known |
| H-Index | LC 274 | M | SRT-08 | counting sort turning O(n log n) into O(n) |
| Kth Largest Element in an Array | LC 215 | M | SRT-06 | quickselect, and expected vs worst case ↺ RND-02 |
| Wiggle Sort II | LC 324 | M | SRT-06 | select plus three-way partition plus index mapping |
| Maximum Gap | LC 164 | H | SRT-09 | pigeonhole + bucket sort to beat the comparison bound |
| Merge Sort / Quicksort / Heapsort | own | M | SRT-02 | three sorts written from scratch, benchmarked against each other |
| Timsort run detection | own | H | SRT-11 | why `list.sort()` beats everything you wrote |

### `LNK` — Linked Lists · Days 52–58

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Reverse Linked List | LC 206 | E | LNK-03 | three pointers, and the order of the reassignments |
| Reverse Linked List II | LC 92 | M | LNK-03 | the dummy head earning its existence |
| Reverse Nodes in k-Group | LC 25 | H | LNK-03 | counting before reversing; the leftover tail |
| Merge Two Sorted Lists | LC 21 | E | LNK-07 | splicing two lists without allocating a single new node |
| Remove Nth Node From End | LC 19 | M | LNK-02 | the gap-of-n two-pointer, one pass |
| Remove Linked List Elements | LC 203 | E | LNK-02 | deleting the head without a special case |
| Linked List Cycle II | LC 142 | M | LNK-04 | Floyd's second phase, and the proof of where they meet |
| Intersection of Two Linked Lists | LC 160 | E | LNK-01 | length alignment, or the two-pass switch trick |
| Palindrome Linked List | LC 234 | E | LNK-03 | reverse the second half in place, then restore it |
| Odd Even Linked List | LC 328 | M | LNK-02 | two interleaved chains and one join |
| Partition List | LC 86 | M | LNK-07 | stability, and two dummy heads |
| Sort List | LC 148 | M | LNK-07 | merge sort where random access does not exist |
| Copy List with Random Pointer | LC 138 | M | LNK-01 | the interleave trick vs the hash map, and the space cost |
| Add Two Numbers | LC 2 | M | LNK-02 | carry across nodes; the final carry node |
| Flatten a Multilevel Doubly Linked List | LC 430 | M | LNK-05 | prev pointers surviving surgery |
| `DoublyLinkedList` with O(1) splice | own | M | LNK-05 | the operation LRU will need ↺ SYS-01 |

### `STQ` — Stacks, Queues, Monotonic Structures · Days 59–65

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Valid Parentheses | LC 20 | E | STQ-01 | LIFO as the shape of nesting |
| Min Stack | LC 155 | M | STQ-08 | auxiliary state maintained in lockstep; amortized O(1) |
| Evaluate Reverse Polish Notation | LC 150 | M | STQ-01 | the operand stack, and why postfix needs no precedence rules |
| Basic Calculator II | LC 227 | M | STQ-01 | precedence without a parser |
| Basic Calculator | LC 224 | H | STQ-01 | sign state across nesting |
| Decode String | LC 394 | M | STQ-01 | two stacks, or one stack of pairs |
| Simplify Path | LC 71 | M | STQ-01 | `..` as a pop, and the edge cases around it |
| Asteroid Collision | LC 735 | M | STQ-01 | a stack whose top is repeatedly re-examined |
| Implement Queue using Stacks | LC 232 | E | STQ-03 | amortized O(1) by the accounting method |
| Implement Stack using Queues | LC 225 | E | STQ-02 | which operation you choose to make expensive |
| Design Circular Queue | LC 622 | M | STQ-02 | the full/empty ambiguity, and the two fixes for it |
| Next Greater Element I | LC 496 | E | STQ-05 | the monotonic stack, derived rather than recalled |
| Next Greater Element II | LC 503 | M | STQ-05 | circularity via two passes |
| Daily Temperatures | LC 739 | M | STQ-05 | storing indices, not values |
| Largest Rectangle in Histogram | LC 84 | H | STQ-06 | the span family, and the sentinel bar |
| Maximal Rectangle | LC 85 | H | STQ-06 | reducing 2D to a histogram per row |
| Remove K Digits | LC 402 | M | STQ-06 | greedy justified by a monotonic stack ↺ GRD-02 |
| Sliding Window Maximum | LC 239 | H | STQ-07 | the monotonic deque, and why each index is pushed once |

### `HSH` — Hashing · Days 66–72

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Two Sum | LC 1 | E | HSH-01 | trading space for a scan; the one-pass version |
| Contains Duplicate | LC 217 | E | HSH-01 | set membership as the whole algorithm |
| Contains Duplicate II | LC 219 | E | HSH-01 | a map from value to last index |
| Isomorphic Strings | LC 205 | E | HSH-07 | bijection needs two maps, not one |
| Word Pattern | LC 290 | E | HSH-07 | the same bijection over a different alphabet |
| Longest Consecutive Sequence | LC 128 | M | HSH-05 | starting only at sequence heads; why it stays O(n) |
| 4Sum II | LC 454 | M | HSH-01 | meet in the middle, 4 → 2 + 2 |
| Insert Delete GetRandom O(1) | LC 380 | M | HSH-05 | array + index map, and swap-with-last deletion |
| Design HashSet | LC 705 | E | HSH-03 | separate chaining, written out |
| Design HashMap | LC 706 | E | HSH-04 | open addressing, probing, tombstones |
| `HashMap` with resizing | own | M | HSH-05 | load factor, rehash cost, amortized O(1) derived |
| Custom `__hash__`/`__eq__` types | own | M | HSH-07 | the contract, and what breaks when you violate it |

### `HEP` — Heaps and Priority Queues · Days 73–78

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Kth Largest Element in a Stream | LC 703 | E | HEP-01 | a size-k heap, and which extremum it keeps |
| Last Stone Weight | LC 1046 | E | HEP-02 | repeated extract-max, and the heap that makes it cheap |
| K Closest Points to Origin | LC 973 | M | HEP-06 | heap vs quickselect, and when each wins |
| Top K Frequent Elements | LC 347 | M | HEP-06 | counting then selecting; the bucket alternative |
| Top K Frequent Words | LC 692 | M | HEP-06 | a comparator with a tie-break, in a heap |
| Task Scheduler | LC 621 | M | HEP-06 | greedy scheduling via a heap ↺ GRD-04 |
| Reorganize String | LC 767 | M | HEP-06 | most-frequent-first, and the feasibility condition |
| Meeting Rooms II | LC 253 | M | HEP-06 | a heap of end times as a resource pool |
| Find Median from Data Stream | LC 295 | H | HEP-06 | two heaps, and the rebalancing invariant |
| Sliding Window Median | LC 480 | H | HEP-06 | lazy deletion, because heaps cannot remove |
| Merge k Sorted Lists | LC 23 | H | HEP-07 | k-way merge; heap vs pairwise merging |
| IPO | LC 502 | H | HEP-06 | two structures, one sorted and one heaped |
| Ugly Number II | LC 264 | M | HEP-07 | generation by repeated smallest-extract |
| `BinaryHeap` and `DAryHeap` | own | M | HEP-04 | sift-up/down, O(n) heapify, and the d that wins |

### `REC` — Recursion and Backtracking · Days 79–86

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Subsets | LC 78 | M | REC-04 | the binary-choice tree, and the two ways to walk it |
| Subsets II | LC 90 | M | REC-06 | duplicate skipping at the level, not the branch |
| Permutations | LC 46 | M | REC-05 | swap vs used-array, and what each costs |
| Permutations II | LC 47 | M | REC-05 | sorting to make duplicates adjacent |
| Combinations | LC 77 | M | REC-06 | the start index that prevents reordering |
| Combination Sum | LC 39 | M | REC-06 | reuse allowed, and where that changes the recursion |
| Combination Sum II | LC 40 | M | REC-06 | each element once, duplicates present |
| Letter Combinations of a Phone Number | LC 17 | M | REC-04 | branching factor and the size of the output |
| Generate Parentheses | LC 22 | M | REC-07 | pruning by a counting invariant, not by validating at the leaf |
| Palindrome Partitioning | LC 131 | M | REC-07 | precomputing validity to make pruning cheap |
| Word Search | LC 79 | M | REC-07 | marking and unmarking; the grid as an implicit graph |
| Restore IP Addresses | LC 93 | M | REC-08 | bounded depth, and pruning on impossible remainders |
| N-Queens | LC 51 | H | REC-07 | three constraint sets, O(1) checking |
| Sudoku Solver | LC 37 | H | REC-08 | choosing the most-constrained cell first |
| Word Break II | LC 140 | H | REC-03 | memoizing a backtracker; the exponential-output caveat |
| Beautiful Arrangement | LC 526 | M | REC-08 | pruning that provably preserves the answer set |

### `DNC` — Divide and Conquer · Days 87–91

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Pow(x, n) | LC 50 | M | DNC-01 | halving the exponent; the negative-n edge |
| Maximum Subarray (D&C form) | LC 53 | M | DNC-01 | the crossing case, and the recurrence it produces |
| Different Ways to Add Parentheses | LC 241 | M | DNC-01 | splitting at every operator |
| Construct Binary Tree from Preorder+Inorder | LC 105 | M | DNC-01 | index maps to avoid O(n²) |
| Search a 2D Matrix II | LC 240 | M | DNC-01 | staircase elimination vs quadrant recursion |
| Count of Smaller Numbers After Self | LC 315 | H | DNC-02 | counting inversions during the merge ↺ RNG-03 |
| Reverse Pairs | LC 493 | H | DNC-02 | a second counting pass inside merge sort |
| The Skyline Problem | LC 218 | H | DNC-01 | merging profiles ↺ GEO-06 |
| Karatsuba multiplication | own | H | DNC-03 | three multiplications instead of four; the Master case |

### `GRD` — Greedy · Days 92–97

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Assign Cookies | LC 455 | E | GRD-01 | the two things a greedy needs before you trust it |
| Best Time to Buy and Sell Stock II | LC 122 | M | GRD-01 | local decisions summing to a global optimum |
| Jump Game | LC 55 | M | GRD-01 | furthest-reach as the invariant |
| Jump Game II | LC 45 | M | GRD-02 | level-by-level reach; the BFS reading of it |
| Gas Station | LC 134 | M | GRD-02 | the exchange argument for the restart point |
| Candy | LC 135 | H | GRD-02 | two passes because one direction is not enough |
| Queue Reconstruction by Height | LC 406 | M | GRD-02 | insertion order chosen so later inserts cannot break earlier ones |
| Non-overlapping Intervals | LC 435 | M | GRD-03 | sort by end, and the proof that it is optimal |
| Minimum Number of Arrows to Burst Balloons | LC 452 | M | GRD-03 | the same key, a different objective |
| Partition Labels | LC 763 | M | GRD-03 | last-occurrence as the boundary |
| Minimum Cost to Hire K Workers | LC 857 | H | GRD-04 | greedy over a sorted ratio, with a heap |
| Huffman coding | own | M | GRD-04 | greedy on a heap, and the optimality proof |
| A greedy that fails | own | M | GRD-05 | constructing the counterexample yourself |

### `TRE` — Trees · Days 98–107

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Maximum Depth of Binary Tree | LC 104 | E | TRE-03 | recursion as a contract on the subtree |
| Same Tree / Symmetric Tree | LC 100/101 | E | TRE-03 | structural recursion over two trees at once |
| Invert Binary Tree | LC 226 | E | TRE-03 | the base case doing the real work |
| Binary Tree Inorder Traversal | LC 94 | E | TRE-04 | the explicit stack, and where the recursion state went |
| Binary Tree Level Order Traversal | LC 102 | M | TRE-05 | the level-size snapshot that separates one level from the next |
| Binary Tree Zigzag Level Order | LC 103 | M | TRE-05 | reversing per level without reversing the queue |
| Binary Tree Right Side View | LC 199 | M | TRE-05 | last-of-level, or first-of-level from the right |
| All Nodes Distance K in Binary Tree | LC 863 | M | TRE-05 | turning a tree into an undirected graph ↺ GRA-01 |
| Path Sum / Path Sum III | LC 112/437 | E/M | TRE-03 | root-to-leaf vs any-path, and prefix sums on a tree ↺ PFX-04 |
| Diameter of Binary Tree | LC 543 | E | TRE-12 | returning one thing while accumulating another |
| Binary Tree Maximum Path Sum | LC 124 | H | TRE-12 | the same pattern with a sign trap |
| Validate Binary Search Tree | LC 98 | M | TRE-06 | bounds passed down, not values compared locally |
| Kth Smallest Element in a BST | LC 230 | M | TRE-06 | inorder is sorted, and early exit |
| Lowest Common Ancestor of a BST | LC 235 | E | TRE-06 | the ordering invariant doing the search |
| Lowest Common Ancestor of a Binary Tree | LC 236 | M | TRE-12 | post-order returning "found what" |
| Delete Node in a BST | LC 450 | M | TRE-07 | the two-child case, and the successor swap |
| Convert Sorted Array to BST | LC 108 | E | TRE-08 | why balance is a property you must construct |
| Balanced Binary Tree | LC 110 | E | TRE-09 | height and balance computed in one pass |
| Serialize and Deserialize Binary Tree | LC 297 | H | TRE-04 | making structure explicit, null markers included |
| Flatten Binary Tree to Linked List | LC 114 | M | TRE-04 | in-place restructuring, reverse post-order |
| Count Complete Tree Nodes | LC 222 | E | TRE-02 | using completeness to beat O(n) |
| AVL tree with deletion | own | H | TRE-09 | four rotations, and why deletion is harder than insertion |

### `TRI` — Tries and String Algorithms · Days 108–114

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Implement Trie (Prefix Tree) | LC 208 | M | TRI-01 | prefix as path; the end-of-word flag |
| Design Add and Search Words Data Structure | LC 211 | M | TRI-01 | wildcards turning lookup into a search |
| Replace Words | LC 648 | M | TRI-02 | stopping at the first end-of-word marker on the path |
| Longest Word in Dictionary | LC 720 | M | TRI-01 | traversal order deciding the tie-break |
| Word Search II | LC 212 | H | TRI-01 | trie-guided backtracking, and pruning dead branches |
| Maximum XOR of Two Numbers in an Array | LC 421 | M | TRI-01 | a bit trie, greedy from the high bit |
| Repeated DNA Sequences | LC 187 | M | TRI-03 | rolling hash, and the collision question |
| Repeated String Match | LC 686 | M | TRI-04 | bounding how many copies can possibly be needed |
| Longest Happy Prefix | LC 1392 | H | TRI-04 | the failure function *is* the answer |
| Shortest Palindrome | LC 214 | H | TRI-04 | KMP on `s + sep + reverse(s)` |
| Stream of Characters | LC 1032 | H | TRI-07 | Aho–Corasick, or a reversed trie over a suffix |
| KMP failure function | own | H | TRI-04 | deriving it, not memorising it |

### `RNG` — Range Query Structures · Days 115–122

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Range Sum Query — Mutable | LC 307 | M | RNG-03 | Fenwick, and what `i & -i` actually indexes |
| Range Sum Query 2D — Mutable | LC 308 | H | RNG-04 | Fenwick in two dimensions |
| Count of Smaller Numbers After Self | LC 315 | H | RNG-03 | coordinate compression + BIT ↺ DNC-02 |
| Number of Longest Increasing Subsequence | LC 673 | M | RNG-03 | a BIT storing pairs ↺ DPA-09 |
| My Calendar I | LC 729 | M | RNG-05 | ordered intervals; segment tree vs a sorted list |
| My Calendar III | LC 732 | H | RNG-06 | lazy propagation on a dynamic segment tree |
| Falling Squares | LC 699 | H | RNG-06 | range-max assign with lazy |
| Range Module | LC 715 | H | RNG-06 | interval assignment, merge and split |
| Sparse table RMQ | own | M | RNG-02 | idempotence licensing overlapping blocks |
| Mo's algorithm on offline queries | own | H | RNG-08 | ordering queries to bound pointer movement |

### `DSU` — Disjoint Set Union · Days 123–126

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Number of Connected Components | LC 323 | M | DSU-01 | the forest, before any optimisation |
| Number of Provinces | LC 547 | M | DSU-01 | DSU vs DFS on the same input |
| Redundant Connection | LC 684 | M | DSU-02 | union failing as the signal |
| Accounts Merge | LC 721 | M | DSU-03 | union over a mapped key space |
| Most Stones Removed | LC 947 | M | DSU-03 | uniting rows and columns as nodes |
| Satisfiability of Equality Equations | LC 990 | M | DSU-02 | two passes: unite, then check |
| Number of Islands II | LC 305 | H | DSU-03 | incremental connectivity; why DFS cannot do this |
| Swim in Rising Water | LC 778 | H | DSU-04 | DSU over sorted edges ↺ GRB-02 |
| Evaluate Division | LC 399 | M | DSU-04 | weighted DSU, or a graph walk |
| DSU with rollback | own | H | DSU-04 | why path compression and rollback conflict |

### `GRA` — Graphs I: Modelling and Traversal · Days 127–135

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Flood Fill | LC 733 | E | GRA-07 | the grid as a graph, and the visited set |
| Number of Islands | LC 200 | M | GRA-07 | component counting; DFS vs BFS vs DSU |
| Max Area of Island | LC 695 | M | GRA-07 | accumulating a value during traversal, not after it |
| Surrounded Regions | LC 130 | M | GRA-07 | starting from the border instead of the interior |
| Pacific Atlantic Water Flow | LC 417 | M | GRA-05 | reversing the direction of the question |
| Rotting Oranges | LC 994 | M | GRA-04 | multi-source BFS, and the layer as a time step |
| 01 Matrix | LC 542 | M | GRA-04 | seeding the queue with every zero at once |
| Walls and Gates | LC 286 | M | GRA-04 | the same shape, stated differently |
| Shortest Path in Binary Matrix | LC 1091 | M | GRA-04 | BFS where the neighbour set is eight cells, not four |
| Word Ladder | LC 127 | H | GRA-04 | an implicit graph you must not materialise |
| Word Ladder II | LC 126 | H | GRA-04 | BFS for layers, DFS for paths |
| Open the Lock | LC 752 | M | GRA-03 | states as nodes; the deadend set |
| Clone Graph | LC 133 | M | GRA-05 | traversal plus a node map |
| Course Schedule | LC 207 | M | GRA-08 | cycle detection in a directed graph |
| Course Schedule II | LC 210 | M | GRA-09 | Kahn's algorithm and the in-degree invariant |
| Alien Dictionary | LC 269 | H | GRA-09 | building the graph is the hard part |
| Minimum Height Trees | LC 310 | M | GRA-09 | peeling leaves, and why at most two survive |
| Is Graph Bipartite? | LC 785 | M | GRA-10 | 2-colouring, and the odd cycle |
| Possible Bipartition | LC 886 | M | GRA-10 | the same, disguised as a seating problem |

### `GRB` — Graphs II: Shortest Paths · Days 136–142

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Network Delay Time | LC 743 | M | GRB-02 | Dijkstra, and the "max over all" reading |
| Path with Maximum Probability | LC 1514 | M | GRB-02 | Dijkstra on a multiplicative objective |
| Path With Minimum Effort | LC 1631 | M | GRB-02 | minimax path; relaxation redefined |
| Cheapest Flights Within K Stops | LC 787 | M | GRB-06 | why Dijkstra fails with a hop limit; Bellman-Ford layers |
| Minimum Cost to Make at Least One Valid Path | LC 1368 | H | GRB-05 | 0-1 BFS and the deque |
| Shortest Path in a Grid with Obstacle Elimination | LC 1293 | H | GRB-05 | state = position + budget |
| Find the City With the Smallest Number of Neighbors | LC 1334 | M | GRB-07 | Floyd–Warshall, and the loop order that matters |
| Number of Ways to Arrive at Destination | LC 1976 | M | GRB-02 | counting paths during relaxation |
| Sliding Puzzle | LC 773 | H | GRB-01 | state-space search; where a heuristic would help |
| Bellman–Ford with negative-cycle detection | own | M | GRB-06 | the nth relaxation as the test |

### `GRC` — Graphs III: MST, SCC, Connectivity · Days 143–150

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Min Cost to Connect All Points | LC 1584 | M | GRC-02 | Kruskal on a complete graph; when Prim is better |
| Connecting Cities With Minimum Cost | LC 1135 | M | GRC-03 | Prim with a heap |
| Optimize Water Distribution in a Village | LC 1168 | H | GRC-02 | the virtual node that turns two costs into one MST |
| Critical Connections in a Network | LC 1192 | H | GRC-07 | bridges via low-link, and the parent-edge exception |
| Reconstruct Itinerary | LC 332 | H | GRC-08 | Hierholzer, and why greedy-with-backtrack is wrong |
| Valid Arrangement of Pairs | LC 2097 | H | GRC-08 | Eulerian path conditions, stated before coding |
| Tarjan's SCC | own | H | GRC-06 | low-link explained aloud, not recited |
| 2-SAT via implication graph | own | H | GRC-09 | reduction from a logical formula to SCC |

### `FLW` — Flows and Matching · Days 151–157

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Maximum bipartite matching (Hungarian/Kuhn) | own | M | FLW-07 | augmenting paths, and why they terminate |
| Edmonds–Karp | own | M | FLW-04 | BFS augmentation and the O(VE²) argument |
| Dinic's algorithm | own | H | FLW-05 | level graphs and blocking flows |
| Minimum cut / project selection | own | H | FLW-06 | modelling profit and cost as a cut |
| Maximum Students Taking Exam | LC 1349 | H | FLW-07 | matching vs bitmask DP on the same input ↺ DPB-05 |
| Task assignment with costs | own | H | FLW-09 | min-cost max-flow as an assignment solver |

### `DPA` — Dynamic Programming I · Days 158–168

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Climbing Stairs | LC 70 | E | DPA-04 | overlapping subproblems, seen for the first time |
| Min Cost Climbing Stairs | LC 746 | E | DPA-04 | where the base case actually is |
| House Robber | LC 198 | M | DPA-04 | take-or-skip as a state transition |
| House Robber II | LC 213 | M | DPA-04 | a circular constraint handled by two runs |
| Decode Ways | LC 91 | M | DPA-04 | transitions guarded by validity |
| Maximum Subarray | LC 53 | M | DPA-04 | Kadane as DP with a one-variable state |
| Maximum Product Subarray | LC 152 | M | DPA-04 | when one value of state is not enough |
| Word Break | LC 139 | M | DPA-02 | memo vs table on the same recursion |
| Perfect Squares | LC 279 | M | DPA-07 | unbounded coin change in disguise |
| Coin Change | LC 322 | M | DPA-07 | minimisation, and the unreachable sentinel |
| Coin Change II | LC 518 | M | DPA-07 | counting, and why the loop order changes the answer |
| Partition Equal Subset Sum | LC 416 | M | DPA-08 | subset-sum as a boolean table |
| Target Sum | LC 494 | M | DPA-08 | reducing a ± problem to subset-sum |
| Longest Increasing Subsequence | LC 300 | M | DPA-09 | O(n²) first, then patience + binary search ↺ BSR-03 |
| Russian Doll Envelopes | LC 354 | H | DPA-09 | the sort key that makes LIS applicable |
| Longest Common Subsequence | LC 1143 | M | DPA-10 | the grid archetype, and the two-case transition |
| Edit Distance | LC 72 | M | DPA-11 | three operations, three predecessors |
| Distinct Subsequences | LC 115 | H | DPA-10 | counting instead of optimising |
| Longest Palindromic Subsequence | LC 516 | M | DPA-10 | LCS with the reverse, and why that works |
| Unique Paths | LC 62 | M | DPA-10 | the combinatorial identity behind the table ↺ MTH-09 |
| Triangle | LC 120 | M | DPA-12 | bottom-up beats top-down here, and rolling rows halve the space |
| Best Time to Buy and Sell Stock III | LC 123 | H | DPA-03 | state design when the answer needs four variables |
| Best Time to Buy and Sell Stock with Cooldown | LC 309 | M | DPA-03 | a state machine drawn before any code |
| Print the LCS itself | own | M | DPA-13 | reconstruction, and what rolling rows cost you |

### `DPB` — Dynamic Programming II · Days 169–180

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Unique Paths II | LC 63 | M | DPB-01 | obstacles as forced zeroes |
| Minimum Path Sum | LC 64 | M | DPB-01 | grid DP with a single direction of flow |
| Burst Balloons | LC 312 | H | DPB-02 | choosing *last*, not first, as the split |
| Minimum Cost to Cut a Stick | LC 1547 | H | DPB-02 | interval DP over cut positions |
| Matrix chain multiplication | own | M | DPB-02 | the interval archetype in its original form |
| Stone Game II / VII | LC 1140/1690 | M | DPB-09 | minimax as a DP over turns |
| House Robber III | LC 337 | M | DPB-03 | tree DP returning a pair |
| Binary Tree Cameras | LC 968 | H | DPB-03 | three states per node, chosen carefully |
| Sum of Distances in Tree | LC 834 | H | DPB-04 | rerooting: one pass down, one pass up |
| Partition to K Equal Sum Subsets | LC 698 | M | DPB-05 | bitmask over the *elements* |
| Shortest Path Visiting All Nodes | LC 847 | H | DPB-05 | BFS over (node, mask) — TSP's approachable cousin |
| Number of Ways to Wear Different Hats | LC 1434 | H | DPB-05 | choosing which side to bitmask |
| Count Numbers with Unique Digits | LC 357 | M | DPB-06 | digit DP without the tight bound |
| Numbers At Most N Given Digit Set | LC 902 | H | DPB-06 | the `tight` flag, stated as an invariant |
| Knight Probability in Chessboard | LC 688 | M | DPB-08 | probability DP; normalise once, at the end |
| New 21 Game | LC 837 | M | DPB-08 | expectation DP with a sliding-window sum |
| Longest path in a DAG | own | M | DPB-07 | topological order making DP legal |
| Jump Game VI | LC 1696 | M | DPB-10 | monotonic deque optimising a DP transition |
| Constrained Subsequence Sum | LC 1425 | H | DPB-10 | the same optimisation, harder to see |
| Convex hull trick | own | H | DPB-12 | when transitions are lines and the query is a minimum |

### `MTH` — Mathematics for Algorithms · Days 181–190

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Excel Sheet Column Number/Title | LC 171/168 | E | MTH-01 | base conversion with a 1-indexed alphabet |
| Fraction to Recurring Decimal | LC 166 | M | MTH-01 | remainders repeating; the map from remainder to position |
| GCD of Strings | LC 1071 | E | MTH-02 | Euclid's algorithm on a non-numeric monoid |
| Count Primes | LC 204 | M | MTH-05 | the sieve, and why it is not n·√n |
| Ugly Number | LC 263 | E | MTH-07 | trial division, and the termination condition |
| Super Pow | LC 372 | M | MTH-11 | modular exponentiation with a digit-array exponent |
| Unique Paths (as nCr) | LC 62 | M | MTH-09 | the closed form, and computing it without overflow |
| Random Pick with Weight | LC 528 | M | MTH-09 | prefix sums + binary search ↺ BSR-03 |
| Fibonacci by matrix exponentiation | own | M | MTH-12 | turning a linear recurrence into a power |
| Miller–Rabin + Pollard's rho | own | H | MTH-07 | probabilistic primality, and the witness idea |
| CRT solver | own | M | MTH-08 | combining congruences with extended Euclid |
| Nim Game | LC 292 | E | MTH-14 | the XOR invariant, and its proof |
| Stone Game IV | LC 1510 | H | MTH-14 | win/lose states as a DP over Grundy reasoning |
| Polynomial multiply via NTT | own | H | MTH-13 | why the modulus is chosen the way it is |

### `GEO` — Computational Geometry · Days 191–196

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Valid Boomerang | LC 1037 | E | GEO-03 | the cross product as a collinearity oracle |
| Max Points on a Line | LC 149 | H | GEO-01 | slope as a normalised fraction, never a float |
| Convex Polygon | LC 469 | M | GEO-03 | consistent orientation around a ring |
| Minimum Area Rectangle | LC 939 | M | GEO-04 | point sets and hashing coordinates |
| Erect the Fence | LC 587 | H | GEO-05 | monotone chain, and collinear points on the hull |
| Rectangle Area II | LC 850 | H | GEO-06 | sweep line with a segment tree ↺ RNG-06 |
| Closest pair of points | own | H | GEO-06 | divide and conquer with the strip argument ↺ DNC-01 |

### `RND` — Randomised, Approximate, Streaming · Days 197–203

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| Shuffle an Array | LC 384 | M | RND-04 | Fisher–Yates, and the off-by-one that biases it |
| Linked List Random Node | LC 382 | M | RND-03 | reservoir sampling with k = 1 |
| Random Pick Index | LC 398 | M | RND-03 | reservoir over a filtered stream |
| Implement Rand10() Using Rand7() | LC 470 | M | RND-01 | rejection sampling, and its expected number of calls |
| Design Skiplist | LC 1206 | H | RND-05 | randomised balance instead of rotations |
| Kth Largest by quickselect | LC 215 | M | RND-02 | expected linear time, derived |
| Bloom filter with measured FPR | own | M | RND-06 | the false-positive equation, then the experiment |
| Count-Min sketch / HyperLogLog | own | H | RND-07 | error bounds you can state before you measure |

### `SYS` — Structures That Run Systems · Days 210–214

| Problem | Src | Lv | ID | Really testing |
|---|---|:-:|---|---|
| LRU Cache | LC 146 | M | SYS-01 | hash map + doubly linked list ↺ LNK-05 |
| LFU Cache | LC 460 | H | SYS-02 | frequency buckets, and O(1) promotion |
| Design In-Memory File System | LC 588 | H | SYS-03 | a tree with directory semantics ↺ TRI-01 |
| Design Search Autocomplete System | LC 642 | H | TRI-01 | trie + ranking + partial input state |
| Design Hit Counter | LC 362 | M | SYS-07 | a circular buffer over time buckets |
| Logger Rate Limiter | LC 359 | E | SYS-07 | the naive version's memory leak |
| Design Underground System | LC 1396 | M | HSH-05 | two maps and a running average |
| Design Tic-Tac-Toe | LC 348 | M | SYS-01 | O(1) win checking via maintained counters |
| Consistent hashing ring | own | M | SYS-06 | virtual nodes, and the distribution measured ↺ SCL-03 |
| B-tree node split | own | H | SYS-03 | fanout chosen from page size ↺ STO-02 |

---

## Track II — the drill bank

Design days do not use judges. Phase 41 supplies twelve drills; this bank supplies the rest, for
the **drill** and **critique** rungs. Each is run timed, narrated aloud, requirements first.

| Drill | Primary ID | The thing it is really testing |
|---|---|---|
| URL shortener | DES-02 | key generation, read/write ratio, cache placement |
| Rate limiter service | DES-03 | distributed counters and the clock you cannot trust |
| News feed | DES-04 | fan-out on write vs read, and the celebrity key |
| Chat system | DES-05 | connection state, ordering, delivery receipts |
| Rideshare matching | DES-06 | geospatial indexing and write-heavy location updates |
| Object store | DES-07 | chunking, replication, metadata vs data planes |
| Payments ledger | DES-08 | idempotency, double-entry, exactly-once at the app layer |
| Video streaming | DES-09 | transcoding pipeline, CDN economics, adaptive bitrate |
| Search / typeahead | DES-10 | inverted index, ranking, index freshness ↺ TRI-01 |
| Notification / webhook system | DES-11 | retries, backoff, poison messages, at-least-once |
| Collaborative document editor | DES-05 | CRDTs vs OT, and conflict as a product decision |
| Distributed job scheduler | DES-03 | leader election, leases, missed-run semantics ↺ CNS-08 |
| Metrics / time-series store | DES-07 | write amplification, downsampling, retention |
| Ad click aggregation | DES-04 | streaming windows, late data, exactly-once counting |
| Multi-region key-value store | DES-07 | quorum arithmetic, conflict resolution, PACELC in practice |
| Stock exchange order matching | DES-08 | ordering guarantees, latency budgets, no cache allowed |

### Critique prompts

Run these against a design — ideally your own, from an earlier day.

1. One region disappears. What does the user see, and for how long?
2. Where is the hot key, and what happens the day one customer is 40% of traffic?
3. Which read in this design can return stale data, and what is the worst business consequence?
4. What is retried, and what happens when the retry succeeds after the original also succeeded?
5. Where is the unbounded queue? Every design has one.
6. What is the p99, and which component owns it?
7. What breaks first as traffic grows 10×, and how would you know before users do?
8. Which piece of this cannot be rolled back?
