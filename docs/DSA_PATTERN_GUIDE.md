# DSA patterns: how to recognize and reason about them

Use the section matching your week during the ten-minute concept slot. These are mechanism
notes, not exercise solutions. Trace the mechanism before choosing it for a problem. Bounds below
use the standard unit-cost model; Python object allocation, copying and large integers can add costs.

## 1. Cost, invariants and arrays

An invariant is a statement true at a repeatable point in a loop. To prove a scan correct,
show it holds initially, survives an iteration and implies the answer at termination. For a
prefix accumulator, explicitly define whether the current item is included. Count operations
as input size grows: one scan is linear; scanning the entire input inside each iteration is
quadratic. A function can be linear even with two separate loops. Auxiliary space excludes the
required returned output, but includes temporary slices and copied lists.

## 2. Hashing and prefix sums

A hash map trades memory for lookup speed. Expected constant-time access is not a worst-case
guarantee. Use a set for membership, a map for associated information and a frequency map when
multiplicity matters. Prefix sums store cumulative totals: a range can be answered by subtracting
two boundaries. Prefix-sum matching works with negative values because it uses equality, not
monotone growth. The empty prefix is often a necessary base case.

## 3. Two pointers and windows

Two pointers work when moving a boundary safely eliminates possibilities. Explain why discarded
candidates cannot improve the result. A window represents a contiguous interval with maintained
state; insertion and removal must both update that state. Positive numbers make a sum grow when
expanding, so shrinking can be justified. Negative numbers break that reasoning. Although a
shrinking loop is nested inside a scanning loop, total work stays linear if each pointer advances
at most n times.

## 4. Binary search

Binary search requires an ordered answer space or a monotone true/false predicate. Maintain an
interval with a precise meaning, such as the first feasible position lying in [lo,hi]. Every
update must preserve that meaning and shrink the interval. Search-on-answer separates two
proofs: feasibility must be computed correctly and must remain true as the candidate increases
(or decrease monotonically in the chosen direction). Include the predicate's cost in the bound.

## 5. Sorting, intervals and selection

Sorting creates order that makes local decisions possible. For intervals, define whether
endpoints are open or closed before deciding whether touching intervals conflict. Merge sort
combines sorted halves; stability requires a consistent equality decision. Partition-based
selection only certifies which side contains a rank, so sorting both sides wastes work.
Randomized or balanced pivots improve typical behavior, but state the worst-case cost separately.

## 6. Linked lists

A node owns a value and a reference to another node. Rewiring changes reachability; overwriting
the only reference to the remaining chain loses it. Save links before changing them. A sentinel
node makes inserting or removing the first real node use the same logic as other nodes. Fast/slow
cursors encode a relationship between distances. A doubly linked list supports constant-time
removal only when the node is already known; a map can supply that lookup.

## 7. Stacks, queues and monotone state

A stack serves the most recent unfinished item; a queue serves the earliest. Monotone structures
discard dominated candidates: a candidate is removable only if a newer candidate is at least as
good and remains useful for at least as long. Store indices when expiry or distances matter.
Amortized analysis counts total pushes, transfers and pops across the whole sequence. One operation
may be expensive even when average cost per operation is constant.

## 8. Backtracking

Backtracking explores a tree of partial choices. A state must contain enough information to
decide which next choices are legal. Choose, recurse, then undo every state change. Copy a path
when saving an answer; storing the live mutable path makes earlier answers change. Pruning needs
a proof that the rejected branch cannot contain a valid answer. Exponential output imposes an
exponential lower bound even when the search overhead is efficient.

## 9. Trees

Tree recursion describes what a call returns about its subtree. Distinguish a value returned to
the parent from a best answer seen anywhere below: the parent may be allowed to extend only
one child branch. Breadth-first traversal groups nodes by distance from the root. A search-tree
ordering condition applies to entire subtrees, not just immediate children. A skewed tree can
have height n, so recursive call-stack space is not always logarithmic.

## 10. Heaps and tries

A heap exposes the smallest or largest candidate without fully sorting all candidates. For
top-k, the boundary among retained candidates determines whether a new value belongs. A trie
shares prefixes across keys: each edge consumes a symbol and a terminal marker records a full
word. Trie memory grows with stored prefixes and child representation. Reconstruction and codecs
must preserve shape, not only values; repeated traversals or missing null markers can lose information.

## 11. Graph traversal

An adjacency list represents outgoing neighbors. DFS explores a path deeply; BFS expands a
frontier by edge count, giving shortest paths only when edges have equal cost. Visited state
prevents revisiting indefinitely. Directed dependency order exists only without directed cycles.
Indegree counts unfinished prerequisites. Disconnected inputs need an outer loop over unvisited
vertices when the task concerns the whole graph. Grid traversal is graph traversal with implicit edges.

## 12. Weighted graphs and connectivity

Nonnegative edge weights allow a minimum-distance frontier to finalize a shortest distance.
Negative edges invalidate that proof and require a different relaxation strategy. A disjoint-set
structure answers whether vertices already share a component; it does not provide the actual
path. A minimum spanning tree minimizes total connection cost, which differs from shortest paths
from a source. Directed strong connectivity requires paths in both directions; ordinary reachability
in one direction is insufficient.

## 13. Greedy algorithms

A greedy algorithm commits to a local choice without undoing it. Support that choice with an
exchange argument or a staying-ahead invariant. An exchange argument transforms an optimal answer
to include the greedy choice without worsening it. A counterexample to one greedy rule does not
mean all greedy rules fail. Sort keys, tie rules and interval endpoint conventions are part of
the correctness proof, not implementation details to choose afterward.

## 14. Dynamic programming foundations

DP reuses answers to overlapping subproblems. Define each state in one sentence before writing
a recurrence. Specify base states, impossible states, transition choices and evaluation order.
Memoization evaluates reachable states on demand; tabulation visits states in dependency order.
Counting ways, testing feasibility and minimizing cost need different combination operators.
Space compression is safe only when overwritten states are no longer needed.

## 15. Grid and string DP

A two-dimensional state often describes two prefix lengths or a grid coordinate. Include empty
prefixes to make boundary cases explicit. Matching, replacing, inserting and deleting correspond
to different predecessor states. Substrings are contiguous; subsequences can skip positions.
An interval state depends on smaller intervals, so traversal order must respect interval length.
Returning an optimal value and reconstructing an optimal path are separate requirements.

## 16. Knapsack and richer states

Zero-one choices allow each item once; unbounded choices permit reuse. In compressed DP, iteration
direction determines whether the current item can feed its own later updates. Interval DP chooses
a split point. Subset DP records a visited set as a bitmask and often needs an endpoint too.
Exponential state counts limit viable input size even when every state transition is simple.
Count the states and transitions before estimating runtime.

## 17. Bits and range structures

Bit operations manipulate a compact set of yes/no flags; define behavior for signed integers
before transferring fixed-width assumptions into Python. Repeated squaring reduces exponentiation
to a logarithmic number of multiplications. A binary indexed tree stores carefully overlapping
prefix summaries. A segment tree combines summaries of disjoint ranges. The combine operation
must be associative, and its identity must work for an empty contribution.

## 18. String matching

A prefix function records how much of an earlier match can survive a mismatch. Reusing that
information avoids rescanning text from scratch. A rolling hash updates a fingerprint as the
window moves; collisions mean equal fingerprints still need verification for exact matching.
Choose whether text means bytes, Unicode code points or grapheme clusters. Normalization and
case conversion can change the meaning of equality and may change length.

## 19. Advanced graphs and trees

A DAG permits dynamic programming in topological order. Some path problems combine edge costs
with maximum rather than addition; the priority strategy needs a proof for that combination.
Tree rerooting reuses one root's result by describing how crossing an edge changes contributions
inside and outside a subtree. Matching improves a current pairing through alternating paths;
locally choosing an unused partner can miss a larger global pairing.

## 20. Data structure design

Start with operations and their required costs. Combine structures when each supplies a missing
capability: a map finds a key, a list maintains recency, buckets group frequency and a heap selects
an extremum. Write invariants spanning the structures; every operation must update all relevant
representations. Include ties, deletion and capacity boundaries. A fast operation is not useful
if maintaining its indexes makes another required operation too expensive.

## 21. Mixed selection I

Recognize constraints rather than memorized titles. Sorted inputs suggest order-based decisions;
contiguous ranges suggest prefixes or windows; repeated lookup suggests hashing; mutable input
may permit using positions as storage. For every chosen pattern, name the prerequisite that
makes it valid. Deliberately change that prerequisite and find a counterexample. This is how you
distinguish understanding from recognizing a familiar statement.

## 22. Mixed selection II

Many problems combine patterns: a heap with a sweep, a topological traversal with DP, or prefix
sums with a monotone deque. Identify the responsibility of each component before combining them.
State which component controls correctness and which controls efficiency. Derive a small baseline
first so a sophisticated implementation can be compared against an independent answer on tiny inputs.

## 23. Mock interviews

Speak in a useful order: clarify the contract, show a baseline, propose the invariant, trace it,
implement, test and analyze. Explain uncertainty instead of silently guessing. When stuck,
reduce the input or solve a restricted version. Record whether the bottleneck was recognition,
proof, implementation or testing; repeating more problems without that diagnosis may repeat the
same failure.

## 24. Capstone and retention

Real tasks expose query/update tradeoffs, repeated work and memory limits that single-shot puzzles
hide. Reuse earlier mechanisms while making those workload assumptions explicit. A retained skill
is one you can reconstruct after a gap with changed inputs. Final review should use cold problems
and failure explanations, not rereading finished code. Keep a short queue of unresolved patterns
for subsequent practice rather than restarting the whole course.
