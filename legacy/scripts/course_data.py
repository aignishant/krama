"""Authored assignments. Each week contains six new sessions and one review.

DSA fields: title ~ contract ~ JSON input ~ JSON output ~ target ~ hint.
All problems use solve(data). JSON is the portable exercise interface.
"""

DSA = [
('Cost, invariants and arrays', '''
Count target values~Return how many elements equal target. Do not mutate nums.~{"nums":[2,1,2,3],"target":2}~2~O(n) time; O(1) extra space~State what your count means after processing i elements.
Find the first maximum~Return the first index of the maximum; return -1 for an empty list.~{"nums":[3,7,7,2]}~1~O(n) time; O(1) space~What should happen on equality rather than a strictly larger value?
Stable compaction~Return nums with all zeroes moved to the end, preserving other values' order. Mutate the provided list and return it.~{"nums":[0,1,0,3,12]}~[1,3,12,0,0]~O(n) time; O(1) auxiliary space~Keep a boundary separating written values from unread values.
Reverse a segment~Reverse nums between inclusive indices left and right; return the modified list. Inputs satisfy 0 <= left <= right < n.~{"nums":[1,2,3,4,5],"left":1,"right":3}~[1,4,3,2,5]~O(right-left+1) time; O(1) space~Which pair of positions can be finalized together?
Merge sorted arrays~Return a new sorted list containing all values from sorted lists a and b, including duplicates.~{"a":[1,3,5],"b":[2,3]}~[1,2,3,3,5]~O(n+m) time; output space O(n+m)~Which unconsumed head is safe to emit?
Best single trade~Given daily prices, return the largest nonnegative profit from one buy followed by one sell; no trade returns 0.~{"prices":[7,1,5,3,6,4]}~5~O(n) time; O(1) space~Track the cheapest earlier price, not the global minimum without order.
'''),
('Hashing and prefix sums', '''
First repeated value~Return the first value whose second occurrence is encountered scanning left to right, or null.~{"nums":[4,2,3,2,4]}~2~Expected O(n) time; O(n) space~Membership and insertion answer different questions.
Frequency ranking~Return distinct integers sorted by descending frequency, breaking ties by smaller value.~{"nums":[3,1,3,2,2,2,1]}~[2,1,3]~O(n+k log k) time~Separate counting from ordering.
Pair sum indices~Return the lexicographically smallest index pair [i,j] with i < j and nums[i]+nums[j]=target; return [] if absent.~{"nums":[2,7,11,15],"target":9}~[0,1]~Expected O(n) time; O(n) space~Store earliest indices and compare candidate index pairs.
Group anagrams~Group lowercase strings by letters. Sort strings within each group and sort the groups lexicographically.~{"words":["eat","tea","tan","ate","nat"]}~[["ate","eat","tea"],["nat","tan"]]~Explain character-key construction plus output sorting costs~A key must represent multiplicities, not merely distinct letters.
Range sums~For each inclusive [left,right] query return the sum. Queries are valid for nums; an empty nums has no queries.~{"nums":[2,-1,4,3],"queries":[[0,2],[1,3]]}~[5,6]~O(n+q) time; O(n) space~Use a prefix array with an initial zero.
Count target subarrays~Count contiguous nonempty subarrays summing to k; values may be negative.~{"nums":[1,1,1],"k":2}~2~Expected O(n) time; O(n) space~Count earlier prefix sums equal to current minus k.
'''),
('Two pointers and sliding windows', '''
Sorted pair existence~Return whether two distinct indices in sorted nums sum to target.~{"nums":[1,2,4,6],"target":8}~true~O(n) time; O(1) space~Explain why moving one boundary discards only impossible pairs.
Unique triples~Return sorted unique triples summing to zero, each sorted internally. Input may be reordered.~{"nums":[-1,0,1,2,-1,-4]}~[[-1,-1,2],[-1,0,1]]~O(n^2) time excluding output~Fix one value and suppress duplicate choices.
Container capacity~For nonnegative heights return max min(h[i],h[j])*(j-i), or 0 if fewer than two heights.~{"heights":[1,8,6,2,5,4,8,3,7]}~49~O(n) time; O(1) space~Can moving the taller endpoint improve the limiting height?
Fixed window maximum sum~Return maximum sum of exactly k adjacent values; 1 <= k <= n.~{"nums":[2,1,5,1,3,2],"k":3}~9~O(n) time; O(1) space~Account for one entering and one leaving element.
Longest distinct substring~Return the length of the longest substring with no repeated Unicode code point.~{"text":"abcabcbb"}~3~Expected O(n) time; O(k) space~The left boundary must never move backward.
Minimum positive window~Return shortest nonempty subarray length with sum >= target, or 0. Values and target are positive integers.~{"nums":[2,3,1,2,4,3],"target":7}~2~O(n) time; O(1) space~Positive values make shrinking safe; construct a negative-value counterexample.
'''),
('Binary search and ordered answers', '''
Lower bound~Return first index with nums[i] >= target, or len(nums), for sorted nums.~{"nums":[1,2,2,4],"target":2}~1~O(log n) time; O(1) space~Use one consistent half-open interval.
Target range~Return first and last target indices in sorted nums, or [-1,-1].~{"nums":[1,2,2,2,4],"target":2}~[1,3]~O(log n) time~Derive boundaries without a linear scan through duplicates.
Rotated search~Return target index in a rotation of a strictly increasing array, or -1.~{"nums":[4,5,6,7,0,1,2],"target":0}~4~O(log n) time~At least one side of the midpoint is sorted.
Integer square root~Return floor(sqrt(n)) for nonnegative integer n, without square-root functions.~{"n":26}~5~O(log n) comparisons~Search for the last feasible integer.
Minimum shipping capacity~Return smallest daily capacity shipping positive weights in given order within days; weights nonempty and days >= 1.~{"weights":[1,2,3,4,5],"days":3}~6~O(n log sum(weights)) time~Prove feasibility is monotone before searching.
Median of two arrays~Return the numeric median of sorted a and b; total length is positive.~{"a":[1,3],"b":[2]}~2~O(log(min(n,m)+1)) time; stretch difficulty~Partition both arrays so left size is fixed and boundary order holds.
'''),
('Sorting, intervals and selection', '''
Stable record sorting~Return records sorted ascending by score while preserving original order on ties. Implement merge sort once.~{"records":[["a",2],["b",1],["c",2]]}~[["b",1],["a",2],["c",2]]~O(n log n) time; O(n) space~A stable merge chooses the left record on equality.
Merge overlapping intervals~Return sorted merged closed intervals; touching endpoints overlap.~{"intervals":[[1,3],[2,6],[8,10],[10,12]]}~[[1,6],[8,12]]~O(n log n) time~Sort by start and maintain one active interval.
Insert an interval~Insert new into sorted disjoint closed intervals and merge overlaps.~{"intervals":[[1,3],[6,9]],"new":[2,5]}~[[1,5],[6,9]]~O(n) time~Separate intervals before, overlapping, and after the new interval.
Minimum meeting rooms~For positive-length half-open intervals [start,end), return peak simultaneous meetings.~{"intervals":[[0,30],[5,10],[15,20]]}~2~O(n log n) time~At an equal timestamp an ending meeting releases its room first.
Kth smallest~Return kth smallest value, counting duplicates; k is one-based and valid. Implement partition-based selection.~{"nums":[3,2,1,5,6,4],"k":2}~2~Expected O(n), worst O(n^2); explain pivot choice~A partition certifies a pivot rank, not a sorted array.
Count inversions~Count index pairs i < j with nums[i] > nums[j].~{"nums":[2,4,1,3,5]}~3~O(n log n) time~How many left-side items remain when a right-side item wins a merge?
'''),
('Linked lists and pointer invariants', '''
Reverse a linked list~Build singly linked nodes from values, reverse links, serialize the resulting values. Do not solve by reversing the input list.~{"values":[1,2,3]}~[3,2,1]~O(n) time; O(1) reversal workspace, excluding adapter~Save the next link before overwriting it.
Middle node~Build singly linked nodes and return the second middle value for even length; null for empty.~{"values":[1,2,3,4]}~3~O(n) time; O(1) traversal space~Compare one-step and two-step cursors.
Cycle entry~Build nodes from values and link the tail to index pos, or no cycle for -1. Return entry index or -1. Nonempty when pos >= 0.~{"values":[3,2,0,-4],"pos":1}~1~O(n) time; O(1) detection space~After a meeting, compare distances from head and meeting point.
Merge linked lists~Build two sorted linked lists, merge by relinking their nodes, then serialize.~{"a":[1,2,4],"b":[1,3,4]}~[1,1,2,3,4,4]~O(n+m) time; O(1) merge workspace~A sentinel simplifies which list supplies the first node.
Remove from end~Build a linked list and remove its nth node from the end; 1 <= n <= length. Return serialized values.~{"values":[1,2,3,4,5],"n":2}~[1,2,3,5]~O(n) time; O(1) traversal space~Keep a fixed gap and include a sentinel for head deletion.
Least recently used cache~Process [put,key,value] and [get,key] operations with capacity >= 1. Return get results, using -1 for misses. Implement map plus doubly linked nodes.~{"capacity":2,"ops":[["put",1,1],["put",2,2],["get",1],["put",3,3],["get",2]]}~[1,-1]~Expected O(1) per operation; O(capacity) space~The map finds a node; the list changes its recency.
'''),
('Stacks, queues and monotone structures', '''
Balanced delimiters~Return whether a string containing only ()[]{} is properly nested; empty is valid.~{"text":"([]{})"}~true~O(n) time; O(n) space~A closing delimiter must match the most recent unmatched opener.
Queue from stacks~Process [push,x] and [pop] operations; pops are valid. Return popped values. Use two stacks.~{"ops":[["push",1],["push",2],["pop"],["push",3],["pop"]]}~[1,2]~Amortized O(1) per operation~Move elements only when the outgoing stack is empty.
Minimum stack~Process [push,x], [pop], and [min]; pop and min are valid. Return min results.~{"ops":[["push",3],["push",1],["push",1],["pop"],["min"]]}~[1]~O(1) per operation~Repeated minima must survive one removal.
Warmer days~For each temperature return days until a strictly warmer temperature, or 0.~{"temps":[73,74,75,71,69,72,76,73]}~[1,1,4,2,1,1,0,0]~O(n) time; O(n) space~Store unresolved indices in monotone order.
Largest histogram rectangle~Return the largest rectangle area in nonnegative bar heights of unit width.~{"heights":[2,1,5,6,2,3]}~10~O(n) time; O(n) space~Popping a bar discovers its first smaller boundary on the right.
Sliding window maxima~Return maximum of each length-k window; 1 <= k <= n.~{"nums":[1,3,-1,-3,5,3,6,7],"k":3}~[3,3,5,5,6,7]~O(n) time; O(k) space~Store indices so expiry and value dominance are separate rules.
'''),
('Recursion and backtracking', '''
Enumerate subsets~Return all subsets of distinct nums; sort each subset and sort the final list lexicographically.~{"nums":[1,2]}~[[],[1],[1,2],[2]]~O(n*2^n) including copied output~Each decision includes or excludes exactly one element.
Enumerate permutations~Return all permutations of distinct nums in lexicographic order.~{"nums":[1,2,3]}~[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]~O(n*n!) including output~Track choices used on the current path, then undo.
Combination sum~From distinct positive candidates return unique sorted combinations summing to target, reusing candidates. Sort final list lexicographically.~{"candidates":[2,3,6,7],"target":7}~[[2,2,3],[7]]~Output-sensitive exponential search~A nondecreasing candidate index prevents reordered duplicates.
Balanced parentheses~Return all strings of n balanced pairs, sorted lexicographically; n >= 0.~{"n":3}~["((()))","(()())","(())()","()(())","()()()"]~Output-sensitive; explain valid-prefix pruning~Never close more pairs than have been opened.
Word search~Return whether word can be formed by orthogonal steps in a rectangular character grid without reusing a cell. Empty word is true.~{"board":[["A","B"],["C","D"]],"word":"ABD"}~true~O(rows*cols*4^L) upper bound~Path-local visited state must be undone on return.
Nonattacking queens~Return the number of ways to place n queens on n*n board with no shared row, column or diagonal; n >= 1.~{"n":4}~2~Exponential search with pruning~Rows can be implicit in recursion; diagonals have constant differences or sums.
'''),
('Binary trees and search trees', '''
Tree depth~Trees use null or [value,left,right]. Return maximum number of nodes on a root-to-leaf path.~{"tree":[1,[2,null,null],[3,[4,null,null],null]]}~3~O(n) time; O(height) call stack~Give the empty subtree a value that makes the recurrence work.
Level order~Return one list of values per depth, left to right, for nested-list trees.~{"tree":[1,[2,null,null],[3,null,null]]}~[[1],[2,3]]~O(n) time; O(width) queue space~Snapshot the frontier length before processing a level.
Validate search tree~Return whether every left descendant is strictly smaller and every right descendant strictly larger. Duplicates invalid.~{"tree":[5,[1,null,null],[4,[3,null,null],[6,null,null]]]}~false~O(n) time~Parent-only comparisons miss ancestor constraints.
Kth tree value~For a strict binary search tree return kth smallest value; k is valid and one-based.~{"tree":[3,[1,null,[2,null,null]],[4,null,null]],"k":2}~2~O(height+k) time with iterative traversal~An inorder traversal exposes sorted values lazily.
Tree diameter~Return maximum edges on any path between two nodes; empty and singleton have diameter 0.~{"tree":[1,[2,[4,null,null],[5,null,null]],[3,null,null]]}~3~O(n) time~Return height upward while separately retaining the best path.
Lowest shared ancestor~Values are unique and both p and q exist. Return the value of their lowest common ancestor, possibly one node itself.~{"tree":[3,[5,[6,null,null],[2,null,null]],[1,null,null]],"p":6,"q":2}~5~O(n) time~What does finding one target on each side imply?
'''),
('Heaps, tries and tree construction', '''
K largest stream values~Return the k largest values of nums sorted descending; 0 <= k <= n.~{"nums":[3,1,5,12,2,11],"k":3}~[12,11,5]~O(n log(k+1)) plus output sorting~Keep only candidates that can still belong to the answer.
Merge sorted streams~Merge k sorted arrays into one sorted list, retaining duplicates.~{"arrays":[[1,4,5],[1,3,4],[2,6]]}~[1,1,2,3,4,4,5,6]~O(N log(k+1)) time~Only each stream's next item competes for the next output.
Running median~After each integer insertion return the current median as a number.~{"nums":[5,15,1,3]}~[5,10,5,4]~O(log n) per insertion~Balance two halves and maintain boundary order.
Prefix dictionary~Build a trie of words. For each prefix return how many inserted distinct words begin with it; empty prefix matches all.~{"words":["car","cat","dog","car"],"prefixes":["ca","c","z",""]}~[2,2,0,3]~O(total characters + query characters)~Terminal markers distinguish a word from a prefix.
Tree reconstruction~Given preorder and inorder traversals with distinct equal value sets, return the nested-list tree.~{"pre":[3,9,20,15,7],"ino":[9,3,15,20,7]}~[3,[9,null,null],[20,[15,null,null],[7,null,null]]]~O(n) time with index map~The first preorder value splits the inorder interval.
Tree codec round trip~Return preorder tokens with null child markers for a nested-list tree; implement an inverse decoder and assert round-trip equality internally.~{"tree":[1,[2,null,null],null]}~[1,2,null,null,null]~O(n) time and serialized space~Without null markers distinct shapes can share the same values.
'''),
('Graph traversal and dependencies', '''
Reachability~Given n vertices 0..n-1 and undirected edges, return whether src reaches dst.~{"n":4,"edges":[[0,1],[1,2]],"src":0,"dst":3}~false~O(V+E) time~Mark visited when scheduling, not after repeatedly enqueueing.
Unweighted distance~Return fewest edges from src to dst in an undirected graph, or -1.~{"n":4,"edges":[[0,1],[1,2],[0,3],[3,2]],"src":0,"dst":2}~2~O(V+E) time~A FIFO frontier processes increasing distances.
Island count~Count orthogonally connected components of 1s in a rectangular 0/1 grid; empty grid returns 0.~{"grid":[[1,1,0],[0,1,0],[1,0,1]]}~3~O(rows*cols) time~Every new unvisited land cell starts exactly one flood fill.
Dependency order~For directed prerequisite edges u->v, return lexicographically smallest topological order; return [] on a cycle.~{"n":4,"edges":[[0,2],[1,2],[2,3]]}~[0,1,2,3]~O((V+E) log(V+1)) with min-heap~Track remaining prerequisites and count emitted nodes.
Two-color graph~Return whether an undirected graph is bipartite; include disconnected components.~{"n":3,"edges":[[0,1],[1,2],[2,0]]}~false~O(V+E) time~Every edge must connect opposite colors.
Multi-source spread~Grid 0 is empty, 1 fresh, 2 active. Active cells spread orthogonally each step. Return steps to activate all fresh cells or -1.~{"grid":[[2,1,1],[1,1,0],[0,1,1]]}~4~O(rows*cols) time~All initial sources enter the same first frontier.
'''),
('Weighted graphs and connectivity', '''
Nonnegative shortest paths~Directed weighted edges [u,v,w], w >= 0. Return distances from src; null for unreachable.~{"n":4,"edges":[[0,1,4],[0,2,1],[2,1,2]],"src":0}~[0,3,1,null]~O((V+E) log(V+1)) with heap~Discard stale heap entries after a shorter route wins.
Negative edge paths~Return distances from src in directed weighted graph; return string negative-cycle if a negative cycle is reachable from src.~{"n":3,"edges":[[0,1,4],[0,2,5],[1,2,-2]],"src":0}~[0,4,2]~O(VE) time~One extra relaxation pass detects a still-improving reachable path.
Disjoint set queries~Process [union,a,b] and [same,a,b] on n isolated vertices. Return booleans for same queries.~{"n":4,"ops":[["union",0,1],["same",0,1],["same",0,2]]}~[true,false]~Near-constant amortized operations~Represent each component by a root; compress paths and union by size.
Minimum spanning cost~Undirected weighted graph: return minimum total spanning-tree weight, or -1 if disconnected; n >= 1.~{"n":3,"edges":[[0,1,1],[1,2,2],[0,2,4]]}~3~O(E log E) time~The cheapest safe edge connects separate components.
Strong components~For directed graph return strongly connected vertex groups, each sorted, with groups lexicographically sorted.~{"n":4,"edges":[[0,1],[1,0],[1,2],[2,3],[3,2]]}~[[0,1],[2,3]]~O(V+E) traversal plus output sorting~Finish order and reversed edges separate mutually reachable regions.
Critical edges~In a simple undirected graph return sorted bridges [min(u,v),max(u,v)], lexicographically sorted.~{"n":4,"edges":[[0,1],[1,2],[2,0],[1,3]]}~[[1,3]]~O(V+E) traversal plus sorting; stretch~A child subtree needs a back route to an ancestor to avoid a bridge.
'''),
('Greedy choices and exchange arguments', '''
Maximum compatible meetings~Return max number of nonoverlapping positive-length half-open intervals.~{"intervals":[[1,3],[2,4],[3,5],[0,6],[5,7]]}~3~O(n log n) time~Which finish time leaves the most room for future choices?
Reach the end~Nonnegative nums[i] is maximum forward jump. Return whether last index is reachable; empty returns false.~{"nums":[2,3,1,1,4]}~true~O(n) time; O(1) space~Maintain the farthest point reachable from the scanned prefix.
Minimum jumps~Return fewest jumps to final index, -1 if unreachable; nonempty nonnegative nums.~{"nums":[2,3,1,1,4]}~2~O(n) time; O(1) space~One greedy layer contains positions reachable with the same jump count.
Circular fuel route~Return smallest valid start index completing the circuit, or -1. gas and cost have equal positive length and nonnegative values.~{"gas":[1,2,3,4,5],"cost":[3,4,5,1,2]}~3~O(n) time~When a candidate fails, which intermediate starts are also impossible?
Task cooldown length~Uppercase tasks take one slot, same task occurrences need at least n intervening slots. Return minimum total slots including idle.~{"tasks":["A","A","A","B","B","B"],"n":2}~8~O(number of tasks + alphabet size)~Compare the most frequent task's frame against total work.
Optimal merge cost~Repeatedly merge any two nonnegative file sizes, paying their sum. Return minimum total cost.~{"sizes":[4,3,2,6]}~29~O(n log n) time~Can exchanging a larger early merge for a smaller one reduce future cost?
'''),
('Dynamic programming foundations', '''
Climbing steps~Return ways to climb n steps using 1 or 2 steps; n >= 0 and there is one empty route for n=0.~{"n":5}~8~O(n) time; O(1) state~Classify routes by their final step.
Nonadjacent loot~Return maximum sum of nonadjacent nonnegative values; empty returns 0.~{"nums":[2,7,9,3,1]}~12~O(n) time; O(1) state~The current decision either includes this value or excludes it.
Minimum coins~Given distinct positive coin values and amount >= 0, return minimum coins or -1; unlimited use.~{"coins":[1,2,5],"amount":11}~3~O(amount*coin_count) time~Distinguish unreachable states from the zero-coin base case.
Coin combinations~Return count of unordered combinations forming amount from distinct positive coins, unlimited use.~{"coins":[1,2,5],"amount":5}~4~O(amount*coin_count) time~Loop order determines whether you count permutations or combinations.
Increasing subsequence~Return length of longest strictly increasing subsequence. Implement quadratic DP before the faster extension.~{"nums":[10,9,2,5,3,7,101,18]}~4~O(n^2) core; O(n log n) optional~A state can mean best subsequence ending exactly at i.
Decode digits~Return number of decodings of a nonempty digit string using 1..26; leading zeroes cannot form letters.~{"text":"226"}~3~O(n) time~Check one-digit and two-digit suffix validity independently.
'''),
('Dynamic programming on grids and strings', '''
Grid path count~Return number of top-left to bottom-right routes using right/down, avoiding 1-valued obstacles. Empty grid returns 0.~{"grid":[[0,0,0],[0,1,0],[0,0,0]]}~2~O(rows*cols) time; O(cols) state~An obstacle resets the state to zero.
Minimum grid path~Return minimum sum along right/down path in a nonempty rectangular integer grid, including endpoints.~{"grid":[[1,3,1],[1,5,1],[4,2,1]]}~7~O(rows*cols) time~Boundary cells do not have both predecessors.
Common subsequence length~Return longest common subsequence length of strings a and b.~{"a":"abcde","b":"ace"}~3~O(nm) time; O(min(n,m)) optional space~Matching final characters and nonmatching final characters have different transitions.
Edit distance~Return minimum insertions, deletions and replacements to turn a into b, each cost 1.~{"a":"horse","b":"ros"}~3~O(nm) time~Define the state for prefixes including empty prefixes.
Longest palindrome length~Return length of longest contiguous palindromic substring; empty returns 0. Implement interval DP.~{"text":"babad"}~3~O(n^2) time~An interval depends on its inner interval and matching ends.
Word segmentation~Return whether text can be segmented into one or more dictionary words; empty text is true; words nonempty.~{"text":"leetcode","words":["leet","code"]}~true~Give a bound that includes substring creation~A reachable prefix can start the next dictionary word.
'''),
('Knapsack and advanced DP states', '''
Zero-one knapsack~Return max value fitting capacity; positive weights, nonnegative values, each item used at most once.~{"weights":[2,3,4],"values":[4,5,6],"capacity":5}~9~O(n*capacity) time~Backward capacity iteration prevents using the current item twice.
Equal partition~Return whether nonnegative nums can be split into two equal-sum subsets; empty is true.~{"nums":[1,5,11,5]}~true~O(n*sum(nums)) time upper bound~An odd total is immediately impossible.
Signed target count~Assign + or - to every nonnegative number and return ways to produce target. Zero choices count separately.~{"nums":[1,1,1,1,1],"target":3}~5~O(n*reachable_sum_range) time~Count paths to states rather than only recording reachability.
Weighted scheduling~Jobs [start,end,value] have positive length, are half-open, and nonnegative value. Return maximum compatible value.~{"jobs":[[1,3,50],[2,4,10],[3,5,40],[3,6,70]]}~120~O(n log n) time~Find the latest compatible predecessor with binary search.
Matrix chain cost~dims describes compatible matrices dims[i]*dims[i+1]. Return minimum scalar multiplications; at least two positive dims.~{"dims":[10,30,5,60]}~4500~O(n^3) time; O(n^2) space~The final multiplication splits a chain into two independent intervals.
Visit every city~Nonnegative square cost matrix; return minimum directed Hamiltonian tour starting/ending at 0. n >= 1; diagonal 0.~{"cost":[[0,10,15],[10,0,20],[15,20,0]]}~45~O(n^2*2^n) time; small n only~A state needs both visited subset and last city.
'''),
('Bits, arithmetic and range structures', '''
Single unmatched value~Every integer appears twice except one. Return that value.~{"nums":[4,1,2,1,2]}~4~O(n) time; O(1) space~Find an operation that cancels equal pairs.
Set bit counts~Return popcount for every integer from 0 through n, where n >= 0.~{"n":5}~[0,1,1,2,1,2]~O(n) time~Remove the lowest set bit or use a right-shift recurrence.
Modular power~Return (base**exp) modulo mod, with exp >= 0 and mod >= 1; do not call three-argument pow.~{"base":3,"exp":13,"mod":17}~12~O(log(exp+1)) multiplications~Repeated squaring follows the exponent's bits.
Primes below a bound~Return all primes strictly less than n for n >= 0.~{"n":12}~[2,3,5,7,11]~O(n log log n) sieve target~Earlier multiples are already marked before p*p.
Mutable range sums~Process [add,index,delta] and [sum,left,right] inclusive over nums; valid indices. Return sums. Use a binary indexed tree.~{"nums":[1,2,3],"ops":[["sum",0,2],["add",1,4],["sum",1,2]]}~[6,9]~O(log n) per operation~One-based indices encode partial-sum ranges in the lowest set bit.
Mutable range minima~Process [set,index,value] and [min,left,right] inclusive on nonempty nums; return minima. Use a segment tree.~{"nums":[5,2,7,3],"ops":[["min",0,3],["set",1,8],["min",0,2]]}~[2,5]~O(log n) per query/update~Store an associative summary for each interval.
'''),
('String algorithms and pattern matching', '''
Normalize text units~Return list of lowercase alphanumeric Unicode code points from text; use code points, not grapheme clusters.~{"text":"A-b 2!"}~["a","b","2"]~O(n) time plus output~State the text model before comparing strings.
Prefix border lengths~For each prefix of text return the length of its longest proper prefix that is also a suffix.~{"text":"ababa"}~[0,0,1,2,3]~O(n) time~A mismatch can fall back through an already-known shorter border.
Find all pattern matches~Return all starting indices where pattern occurs in text, including overlaps; empty pattern matches 0..len(text). Use prefix-function matching.~{"text":"aaaaa","pattern":"aa"}~[0,1,2,3]~O(n+m) time~After a full match retain the longest reusable border.
Rolling hash matching~Return first index of pattern in text or -1; empty pattern returns 0. Use rolling hash and verify equal hashes by direct comparison.~{"text":"abracadabra","pattern":"cada"}~4~Expected linear; explain worst-case collisions~A hash match is a candidate, never proof of equality.
Smallest covering window~Return shortest substring covering all pattern character multiplicities; tie by earliest start; absent or empty pattern returns empty string.~{"text":"ADOBECODEBANC","pattern":"ABC"}~"BANC"~Expected O(n+m) time~Count satisfied requirements rather than all present characters.
Dictionary wildcard search~For each query return whether a lowercase dictionary word matches; dot matches one letter. Use a trie.~{"words":["bad","dad","mad"],"queries":["pad","bad",".ad","b.."]}~[false,true,true,true]~Query may branch exponentially in wildcard count~A wildcard explores children but does not skip depth.
'''),
('Advanced graph and tree practice', '''
Longest DAG path~Return max edge count along any path in a directed acyclic graph; n >= 1.~{"n":4,"edges":[[0,1],[0,2],[1,2],[2,3]]}~3~O(V+E) time~Process states only after their predecessors.
Minimum effort grid route~Return minimum possible maximum absolute height difference on a top-left to bottom-right orthogonal path; nonempty grid.~{"heights":[[1,2,2],[3,8,2],[5,3,5]]}~2~O(RC log(RC)) time~The path-combination operation is max instead of sum.
Redundant undirected edge~A tree has one extra edge added. Return the first input edge whose insertion connects already-connected vertices.~{"edges":[[1,2],[1,3],[2,3]]}~[2,3]~Near-linear with disjoint sets~Connectivity before insertion tells whether a cycle would form.
Subtree sizes~Given tree edges on 0..n-1 rooted at 0, return subtree sizes by vertex index; n >= 1.~{"n":5,"edges":[[0,1],[0,2],[1,3],[1,4]]}~[5,3,1,1,1]~O(n) time~Postorder combines children after skipping the parent edge.
Tree distance sums~Return sum of distances from each vertex to all others in a tree rooted arbitrarily; n >= 1.~{"n":3,"edges":[[0,1],[1,2]]}~[3,2,3]~O(n) time; stretch~Moving root across an edge brings one subtree closer and all other nodes farther.
Bipartite matching~Left vertices 0..left-1, right 0..right-1, edges [l,r]. Return maximum number of disjoint pairs.~{"left":3,"right":3,"edges":[[0,0],[0,1],[1,0],[2,2]]}~3~O(VE) augmenting-path baseline~A used partner may be reassigned through an alternating path.
'''),
('Data structure design and tradeoffs', '''
Time-indexed values~Process [set,key,value,timestamp] with strictly increasing timestamps per key, and [get,key,timestamp]. Return latest value <= timestamp or null.~{"ops":[["set","a","x",1],["set","a","y",3],["get","a",2],["get","a",0]]}~["x",null]~O(log n) get; amortized O(1) append~Find a rightmost feasible timestamp.
Frequency stack~Process [push,value] and [pop]. Pop most frequent value, breaking ties by most recent push among current elements. Return popped values.~{"ops":[["push",5],["push",7],["push",5],["push",7],["push",4],["push",5],["pop"],["pop"]]}~[5,7]~Expected O(1) per operation~Maintain separate recency stacks for each attained frequency.
Least frequently used cache~Process put/get like the LRU exercise, capacity >= 1; evict lowest frequency, then least recently used within it. New keys start at frequency 1; get and updating put increment frequency.~{"capacity":2,"ops":[["put",1,1],["put",2,2],["get",1],["put",3,3],["get",2],["get",3]]}~[1,-1,3]~Expected O(1) operations; stretch~Track the minimum nonempty frequency bucket.
Order statistic stream~After each insertion return the kth largest so far, or null until k values exist; k >= 1.~{"nums":[4,5,8,2,10],"k":3}~[null,null,4,4,5]~O(log k) per insertion~The smallest among retained top-k values is the answer.
Expiring counter~Events are sorted nondecreasing integer timestamps; for each event return events in (t-window,t], including current and earlier equal-timestamp events; window > 0.~{"times":[1,2,3,8,8],"window":5}~[1,2,3,1,2]~O(n) total time~The boundary is open on the left; duplicate timestamps remain separate events.
Autocomplete ranking~Given unique [word,count] entries and prefix return at most k matches by descending count then lexicographic word; k >= 0.~{"entries":[["cat",4],["car",4],["cart",2],["dog",9]],"prefix":"ca","k":2}~["car","cat"]~Explain scan baseline and trie/top-k extension~Decide whether optimizing lookup or updates matters more.
'''),
('Mixed pattern selection I', '''
Product except self~Return product of all other values for each position; no division; empty returns [].~{"nums":[1,2,3,4]}~[24,12,8,6]~O(n) time; O(1) auxiliary excluding output~A position needs a summary of values before and after it.
Longest consecutive run~Return length of longest consecutive integer set sequence; duplicates do not extend it.~{"nums":[100,4,200,1,3,2]}~4~Expected O(n) time~Start counting only where a predecessor is absent.
Trapped rainwater~Return total trapped water above nonnegative unit-width bars.~{"heights":[0,1,0,2,1,0,1,3,2,1,2,1]}~6~O(n) time; O(1) auxiliary stretch~The smaller known boundary determines one side safely.
Top frequent words~Return top k distinct words by descending count then lexicographic order; 0 <= k <= distinct count.~{"words":["i","love","code","i","love","python"],"k":2}~["i","love"]~Count then O(u log u) baseline; heap extension~Tie-breaking belongs in the ordering key.
Rotated minimum with duplicates~Return minimum in a nonempty rotated sorted array allowing duplicates.~{"nums":[2,2,2,0,1]}~0~O(log n) typical; O(n) worst case~Equality can erase information about which side contains the rotation.
Find duplicate without mutation~Length n+1 nums contains values 1..n and exactly one distinct duplicated value, possibly repeated multiple times. Return it without modifying nums.~{"nums":[1,3,4,2,2]}~2~O(n) time; O(1) space~Values can be interpreted as links in a functional graph.
'''),
('Mixed pattern selection II', '''
Interleaved strings~Return whether c interleaves a and b while preserving each string's internal order.~{"a":"aabcc","b":"dbbca","c":"aadbbcbcac"}~true~O(len(a)*len(b)) time~A prefix state records how much of each source has been consumed.
Course completion time~DAG edges u->v and positive durations per node; unlimited parallel workers. Return minimum makespan; empty graph returns 0.~{"durations":[3,2,5],"edges":[[0,2],[1,2]]}~8~O(V+E) time~A node starts after its slowest prerequisite finishes.
Maximum path sum~For a nonempty integer binary tree return largest sum on a nonempty simple path; values may be negative.~{"tree":[-10,[9,null,null],[20,[15,null,null],[7,null,null]]]}~42~O(n) time~A returned branch and the best completed path are different states.
Smallest missing positive~Return smallest missing positive integer. You may mutate nums.~{"nums":[3,4,-1,1]}~2~O(n) time; O(1) extra space~Only values 1..n can occupy useful indexed positions.
Shortest subarray with negatives~Return shortest nonempty subarray length with sum >= k, or -1; k > 0 and nums may be negative.~{"nums":[2,-1,2],"k":3}~3~O(n) time~Prefix sums plus a monotone deque replace the positive-only window.
Minimum interval for queries~For each integer query return smallest inclusive interval length containing it, or -1.~{"intervals":[[1,4],[2,4],[3,6],[4,4]],"queries":[2,3,4,5]}~[3,3,1,4]~O((n+q) log(n+1)) time~Sort queries, add eligible starts, expire candidates by end.
'''),
('Mock interviews and weak-area repair', '''
Mock arrays~Return length of longest subarray containing at most k distinct integers; k >= 0.~{"nums":[1,2,1,2,3],"k":2}~4~Expected O(n) time~Choose the pattern before coding; only then inspect this hint: window frequencies.
Mock search~Return minimum integer eating speed finishing positive piles within h hours; h >= number of piles and piles nonempty.~{"piles":[3,6,7,11],"h":8}~4~O(n log(max(piles))) time~Use a monotone predicate with ceiling division.
Mock graph~Return number of shortest unweighted paths from src to dst in a simple undirected graph; src==dst has one empty path.~{"n":4,"edges":[[0,1],[0,2],[1,3],[2,3]],"src":0,"dst":3}~2~O(V+E) time~Equal shortest distances add counts; longer arrivals do not.
Mock DP~Return maximum sum from a nonempty circular array of nonnegative houses, with no adjacent selected houses; one house may be selected.~{"nums":[2,3,2]}~3~O(n) time; O(1) auxiliary~The first and last positions cannot both be selected.
Mock heap~Return minimum cost to connect all given 2D points using Manhattan-distance edges; empty returns 0.~{"points":[[0,0],[2,2],[3,10],[5,2],[7,0]]}~20~O(n^2) dense spanning-tree approach~Implicit complete graphs need not materialize every edge.
Mock backtracking~Return all palindrome partitions of text, each a list of substrings; sort outer list lexicographically.~{"text":"aab"}~[["a","a","b"],["aa","b"]]~Output-sensitive exponential; palindrome precomputation optional~Every cut leaves a smaller suffix subproblem.
'''),
('Capstone and retention', '''
Routing capstone~Directed nonnegative edges and multiple [src,dst] queries: return shortest distances, -1 for unreachable. Cache work per distinct source.~{"n":3,"edges":[[0,1,2],[1,2,3]],"queries":[[0,2],[0,1],[2,0]]}~[5,2,-1]~Explain preprocessing versus per-query cost~Repeated sources can share one shortest-path computation.
Scheduling capstone~Jobs [release,duration] run nonpreemptively on one worker. Whenever idle choose shortest available duration, then original index; jump to next release if none. Return execution indices.~{"jobs":[[1,2],[2,4],[3,2],[4,1]]}~[0,2,3,1]~O(n log n) time~Separate future arrivals from currently eligible jobs.
Search capstone~Given unique words, return all dictionary words present on an orthogonal grid path without cell reuse, sorted; words are nonempty.~{"board":[["a","b"],["c","d"]],"words":["ab","abd","ac","aba"]}~["ab","abd","ac"]~Trie-guided exponential search; state assumptions~Share dictionary prefixes and maintain path-local visited state.
Range capstone~Process inclusive range queries [left,right] returning number of distinct values in nums; indices valid.~{"nums":[1,2,1,3],"queries":[[0,2],[1,3],[2,2]]}~[2,3,1]~O((n+q) log n) offline target; stretch~Sort queries by right endpoint and keep only each value's latest occurrence.
Counterexample capstone~Return the maximum sum of a nonempty contiguous subarray; nums nonempty and may be all negative.~{"nums":[-2,1,-3,4,-1,2,1,-5,4]}~6~O(n) time; O(1) state~A zero default can accidentally allow an empty answer.
Final independent problem~Return maximum number of envelopes nested with strictly increasing width and height; equal dimensions cannot nest.~{"envelopes":[[5,4],[6,4],[6,7],[2,3]]}~3~O(n log n) time~Sorting one dimension requires a careful tie rule before applying an increasing subsequence.
'''),
]

# Every SD/Python row is a bounded deliverable, not a full implementation project.
SD = [
('Requirements and estimation', '''
Functional scope~For a link-shortening service, write three user actions, two exclusions, and one measurable success criterion.
Quality requirements~Define availability, latency percentile, durability and freshness targets for that service; mark every number as an assumption.
Traffic estimates~Assume 1 million daily users and 10 reads per user; calculate average QPS and a separately justified peak multiplier.
Storage estimates~Assume 100000 new links daily and 500 bytes per record; calculate one-year raw storage, then separate index and replication overhead.
Latency budgets~Allocate a hypothetical 200 ms end-to-end p95 budget across client, network, app and storage; explain why summing component p95 values is only a rough budget.
Single-node baseline~Draw browser -> service -> database and trace create and redirect; name the first bottleneck to measure.
'''),
('Networking and HTTP', '''
Request journey~Draw DNS lookup, connection establishment, TLS, request and response for a browser opening a shortened URL.
HTTP methods~Specify create and redirect routes with method, request fields, response codes and caching implications.
Idempotency semantics~Show two retries of the same create request; choose a client key and define replay versus conflict behavior.
Connection budgets~Given 200 concurrent requests per worker and 20 workers, estimate connection demand; identify which pools impose separate limits.
Timeout propagation~Draw a three-hop call with one overall deadline and smaller per-hop budgets; show what cancellation does downstream.
Pagination~Design cursor pagination for links ordered by creation time with a unique tie-breaker; show concurrent insertion between pages.
'''),
('Service boundaries and API design', '''
Domain model~Name link, owner and click-event entities and sketch their keys and relationships.
API contract~Write a compact request/response/error contract for creating an expiring link; include input validation.
Stateless workers~Move session and link state out of workers; trace a request landing on a different worker after restart.
Sync versus async~Choose which click analytics actions belong off the redirect path and state the lost-work risk.
Compatibility~Evolve a response with an optional expiration field and define old-client behavior.
Modular monolith~Draw internal modules for links and analytics; state an observable trigger for extracting a service.
'''),
('Relational storage and indexes', '''
Schema constraints~Write tables and unique/foreign-key constraints for links and owners; distinguish product rules from lookup needs.
Index selection~Choose an index for owner plus newest-first lookup; show why a different column order changes usefulness.
Query plans~Read the database guide on EXPLAIN and describe scan, filter and sort stages for one query; no measured plan is claimed without running it.
Transactions~Trace creating a link and updating an owner quota atomically; show a failure between statements.
Isolation anomalies~Write an interleaving where two transactions overspend the same quota; choose a remedy and its retry behavior.
Optimistic concurrency~Add a version field to link edits; specify compare-and-swap failure and a client retry decision.
'''),
('Storage engine tradeoffs', '''
Tree indexes~Sketch page lookup and a page split in an ordered index; identify read and write amplification.
Log structured storage~Sketch memory buffer, immutable files and compaction; compare write cost and read cost.
Access-pattern modeling~Model recent clicks for one link and aggregate clicks per owner; avoid choosing a database before the queries.
Hot partitions~Show why a single popular link can overload one partition even when total storage is balanced.
TTL and deletion~Specify logical expiration, physical cleanup and tombstone retention; explain what a delayed cleanup may expose.
Storage decision memo~Choose relational versus key-value storage for redirects using three access patterns and two failure requirements.
'''),
('Caching and content delivery', '''
Cache aside~Trace hit, miss, database failure and cache-fill failure for redirects; label the source of truth.
Invalidation race~Show an interleaving where an old read repopulates a deleted cache entry; propose versioning or bounded staleness.
TTL and eviction~Choose expiration separately from memory eviction; explain behavior when all popular keys expire together.
Stampede control~Compare single-flight loading, TTL jitter and stale-while-revalidate for a popular link.
Negative caching~Cache absent links briefly; define how newly created links avoid being hidden too long.
CDN behavior~Place a CDN in the request path and specify cache key, private-data exclusions and invalidation needs.
'''),
('Load balancing and partitioning', '''
Balancing policies~Compare round-robin and least-connections for a mix of short redirects and slow exports.
Health checks~Separate liveness from readiness; trace rollout behavior while dependencies are unavailable.
Horizontal scaling~Calculate worker count from assumed peak QPS, tested per-worker capacity and explicit headroom.
Partition keys~Choose a shard key for links; show a read lookup, a range query and a hotspot.
Consistent placement~Draw a hash ring with virtual nodes and a node addition; distinguish data movement from load balance.
Resharding~Outline copy, catch-up, cutover and rollback while writes continue; state how duplicate writes are handled.
'''),
('Replication and consistency', '''
Leader replication~Trace acknowledged writes with synchronous and asynchronous replicas; compare latency and loss windows.
Read-your-writes~Show a user creating a link then reading a lagging replica; design session routing or a version fence.
Consistency models~Write one history permitted by eventual consistency but forbidden by linearizability.
Quorum reasoning~For N=3 compare R=1/W=1 and R=2/W=2; explain why overlap alone does not establish linearizability.
Network partitions~Describe which requests continue during a partition and what guarantee is sacrificed for this operation.
Failover~Draw leader failure, detection, election and client retry; identify split-brain prevention.
'''),
('Queues and event processing', '''
Queue fundamentals~Separate work queues from event logs; assign click aggregation to one and explain why.
Delivery semantics~Trace lost acknowledgment causing duplicate delivery; separate delivery guarantees from business-effect guarantees.
Consumer idempotency~Design a deduplication record and atomic business update using an event identifier.
Ordering~Choose partition keys for per-link order; show why global ordering would constrain throughput.
Backpressure~Given arrival rate above processing rate, calculate backlog growth and compare buffering, shedding and throttling.
Poison messages~Specify bounded retries, dead-letter handling, replay and alerting without infinite retry loops.
'''),
('Reliability patterns', '''
Retry budgets~Draw an outage with three retrying layers; quantify amplification and move retries to a deliberate boundary.
Backoff and jitter~Sketch retry times for synchronized versus jittered clients and define a maximum attempt/deadline budget.
Circuit breakers~Specify closed/open/half-open transitions and what callers receive when the breaker opens.
Bulkheads~Allocate separate worker/connection pools to redirects and analytics so analytics cannot exhaust redirects.
Rate limiting~Compare token bucket and sliding-window counters; define burst allowance, identity and rejection response.
Graceful degradation~During analytics outage preserve redirects and document what becomes delayed or unavailable.
'''),
('Distributed coordination', '''
Logical ordering~Construct events on two workers with clock skew; distinguish wall-clock timestamps from causal order.
Consensus purpose~Explain which replicated metadata needs agreement; sketch leader and majority without claiming to implement consensus.
Leader terms~Draw a stale leader attempting a write after failover; specify a monotone term or fencing check.
Distributed locks~Show a paused worker resuming after its lease expires; explain why a lock alone cannot prevent stale writes.
Unique identifiers~Compare random IDs, database sequences and time-based IDs; discuss collision, ordering and coordination.
Cross-service transactions~Compare coordinated commit and compensating actions for a reservation plus charge workflow.
'''),
('Observability and operations', '''
SLIs and SLOs~Define good/total redirect requests and a latency histogram; distinguish user-visible success from process uptime.
Error budgets~For a hypothetical 99.9 percent success target over 1 million requests, calculate allowed failures and a release decision.
Logs metrics traces~Choose one example of each for a slow redirect; carry a correlation ID without logging sensitive data.
Tail latency~Explain why fan-out magnifies stragglers; sketch bounded parallelism and timeout behavior.
Capacity and cost~Estimate monthly storage and compute units symbolically; separate measured inputs from guessed unit prices.
Incident review~Write a short timeline, customer impact, contributing causes and two verifiable follow-up actions for cache failure.
'''),
('Security and tenancy', '''
Trust boundaries~Mark untrusted input and privileged calls on the link-service diagram; choose validation at each boundary.
Authentication and authorization~Separate proving identity from checking ownership when editing a link; show an object-level access test.
Abuse prevention~Design limits for anonymous link creation and suspicious redirects without treating IP as a perfect identity.
Secret handling~Specify storage, rotation, revocation and log redaction for service credentials; use no real secrets.
Tenant isolation~Compare shared rows, schemas and databases for tenants; show how a missing tenant filter is detected.
Retention and audit~Specify hypothetical product retention and deletion behavior, backups and an audit trail; this is a design exercise, not legal advice.
'''),
('URL shortener case study', '''
Shortener requirements~Set create/read ratio, alias policy, expiry and availability assumptions; identify the critical path.
Shortener API and data~Write API examples, schema and unique alias constraint; handle a collision explicitly.
Shortener capacity~Compute peak redirect QPS, new-record storage and cache working set using your assumptions.
Shortener architecture~Draw load balancer, stateless workers, cache and durable store with read/write arrows.
Shortener deep dive~Choose one: hot-key mitigation or alias generation; compare two alternatives and explain the choice.
Shortener failure review~Walk through cache loss, replica lag and database failover; record three weaknesses and one revised diagram.
'''),
('Feed case study', '''
Feed requirements~Choose chronological versus ranked feed, follow semantics and acceptable freshness.
Feed API and data~Model posts, follows and feed entries; define cursor pagination under concurrent posts.
Feed capacity~Estimate fan-out work from followers per author; isolate celebrity users from the average.
Feed architecture~Compare fan-out on write, read and hybrid; draw where candidate entries are stored.
Feed deep dive~Handle delete/block propagation and stale cached entries; state read-time checks.
Feed failure review~Trace queue backlog and celebrity bursts; preserve a usable fallback and a recovery plan.
'''),
('Chat case study', '''
Chat requirements~Define one-to-one scope, online delivery, offline history and multi-device semantics.
Chat API and data~Specify message IDs, conversation sequence and acknowledgment fields.
Chat connections~Estimate concurrent connections and heartbeat traffic; separate connection routing from message storage.
Chat architecture~Draw gateways, routing registry, message store and offline delivery path.
Chat deep dive~Trace retry, deduplication and per-conversation ordering across reconnects.
Chat failure review~Model gateway loss and reconnect storm; preserve replay position and avoid duplicate user-visible messages.
'''),
('Upload and media case study', '''
Upload requirements~Define file size distribution, privacy, upload resume and download latency assumptions.
Upload API and metadata~Separate file bytes from metadata; specify upload session and completion contract.
Upload capacity~Estimate bandwidth and storage; distinguish ingress, transcoding and egress workloads.
Upload architecture~Draw direct object upload, metadata commit, asynchronous processing and CDN delivery.
Upload deep dive~Handle chunk checksums, resumability and an upload completed after session expiry.
Upload failure review~Trace object-created but metadata-missing and metadata-created but object-missing cases; design reconciliation.
'''),
('Search and notifications case studies', '''
Search requirements~Define searchable fields, ranking scope and freshness targets for a document service.
Search indexing~Draw write -> event -> index flow and handling of document edits/deletions.
Search query path~Specify tokenization, candidate retrieval, ranking and pagination at a conceptual level.
Notification requirements~Define email/push channels, preference checks and urgency classes.
Notification architecture~Draw event intake, template rendering, per-channel queues and provider adapters.
Notification failure review~Trace provider timeout after possible send; define deduplication limits and user-visible retry policy.
'''),
('Payments and reservations case study', '''
Reservation invariants~State no-oversell and no-double-charge invariants for a hypothetical ticket service.
Reservation data~Model inventory, holds, expiration and reservation states with valid transitions.
Payment idempotency~Design durable idempotency records including in-progress, success, failure and conflicting payloads.
Transactional outbox~Trace database commit and event publication across a crash; specify deduplication on the consumer.
Compensation workflow~Draw reserve -> authorize -> confirm with timeouts and compensations; distinguish reversible and irreversible effects.
Reconciliation~Compare internal state with provider records; define how unknown outcomes are investigated and repaired.
'''),
('Analytics and stream processing', '''
Analytics requirements~Define event volume, freshness, exactness and top-k dashboard queries.
Event time~Show late and out-of-order events; distinguish event time, processing time and watermark assumptions.
Aggregation windows~Choose tumbling versus sliding windows; show a late event update and retention cutoff.
Partitioned aggregation~Separate local partial counts from merged totals; identify a hot aggregation key.
Approximate answers~Compare exact distinct counting with approximate summaries; state error and mergeability requirements without invented guarantees.
Replay and rebuild~Specify immutable input retention, versioned transforms and rebuilding a corrupted aggregate safely.
'''),
('Multi-region and advanced tradeoffs', '''
Regional topology~Compare active-passive and active-active for writes; state latency and conflict consequences.
Recovery objectives~Choose hypothetical RPO and RTO and show which backup/replication actions support them.
Conflict resolution~Construct concurrent edits in two regions; compare explicit conflict handling and last-write-wins under skew.
Data placement~Map tenant locality, failover and routing constraints without assuming any specific regulation.
Disaster recovery drill~Write a restore checklist and observable acceptance tests; distinguish backup existence from successful recovery.
Migration strategy~Plan dual reads/writes, backfill, consistency checks, cutover and rollback for a datastore migration.
'''),
('Low-level design and maintainability', '''
Responsibilities~Split an in-process rate limiter into clock, policy and storage interfaces; avoid an interface for every class.
State machines~Model a background job lifecycle with retry, cancellation and terminal states; list forbidden transitions.
Dependency inversion~Design a notification sender that tests without network access using an injected transport.
Concurrency contracts~Specify ownership and synchronization for a shared cache; identify the atomic operations.
Extensibility~Add a second pricing policy to a hypothetical parking service; compare composition and inheritance.
Design review~Review one earlier design for cohesion, coupling, testability and migration costs; write three actionable comments.
'''),
('Design interviews and critique', '''
Mock requirements round~Use a distributed job scheduler prompt; spend the session on requirements and capacity only.
Mock architecture round~Continue the scheduler with durable jobs, workers, leasing and result storage.
Mock deep dive~Handle a worker dying after executing a job but before acknowledging it; state side-effect deduplication requirements.
Mock alternative~Design a collaborative document service at the level of requirements and operation flow; compare central ordering with conflict-free approaches conceptually.
Critique round~Score your diagrams for clear critical path, quantified assumptions, failure behavior and rejected alternatives.
Repair round~Rewrite the weakest two sections and answer a changed requirement without replacing the whole architecture.
'''),
('Final design portfolio', '''
Capstone brief~Choose one service from the portfolio and freeze a one-page requirements and capacity brief.
Capstone architecture~Produce one readable component diagram with data ownership and synchronous/asynchronous arrows.
Capstone consistency~Write three invariants and the consistency or transaction boundary enforcing each.
Capstone resilience~Document five failure scenarios, detection signals, user impact and recovery steps.
Capstone tradeoffs~Write a decision record with two rejected alternatives and measurable triggers to revisit the choice.
Final defense~Record a concise design explanation; answer a 10x traffic change and a full-region outage using your existing design.
'''),
]

LANG = [
('Object semantics', '''
Identity and equality~Predict and verify aliasing of two names bound to the same list versus equal distinct lists; avoid relying on interning.
Shallow and deep copies~Copy a nested list both ways, mutate an inner list, and write assertions describing which copies change.
Mutable defaults~Reproduce state leaking across calls through a list default, then fix with an explicit None sentinel.
Hash and equality~Make a small value object usable as a dictionary key; explain why mutating hash-relevant fields is unsafe.
Truth and sentinels~Distinguish None, zero and empty values in an API using an identity-tested sentinel.
Mutation contracts~Write one function that mutates input and one that returns a new value; test ownership assumptions explicitly.
'''),
('Functions and scope', '''
Argument binding~Write a function with positional-only and keyword-only parameters and capture one invalid call's real exception.
Closure binding~Create callbacks in a loop, reproduce late binding and fix it with a captured value.
Nonlocal state~Build a closure counter and explain where the state lives; compare with a callable instance.
Decorator metadata~Write a tracing decorator with functools.wraps and inspect name, docstring and __wrapped__.
Decorator arguments~Write a configurable validation decorator without swallowing the wrapped exception.
Partial application~Use functools.partial to specialize a function; test binding conflicts and distinguish it from a closure.
'''),
('Iteration and generators', '''
Iterator protocol~Implement a finite countdown iterator and prove exhaustion remains exhausted.
Generator laziness~Build a generator with observable side effects and show creation versus first iteration behavior.
Generator cleanup~Use try/finally in a generator and explicitly close it after partial consumption.
Yield delegation~Use yield from with a subgenerator returning a value; capture the delegated result.
Iterator consumption~Show why membership or list() consumes a one-shot iterator; repair code that needs two passes.
Streaming pipeline~Compose two lazy transformations over generated records and avoid materializing the whole input.
'''),
('Data model protocols', '''
Representations~Implement __repr__ and __str__ for a small object; ensure debugging output avoids secrets.
Rich comparison~Return NotImplemented for unsupported comparison operands and demonstrate reflected dispatch or TypeError.
Container protocol~Implement __len__, __iter__ and __contains__ for a tiny immutable collection.
Indexing and slicing~Implement __getitem__ handling integer and slice inputs with explicit boundary behavior.
Callable instances~Write a stateful callable and compare its inspectability with a closure.
Context managers~Implement __enter__/__exit__ and test cleanup on success and exception without accidental suppression.
'''),
('Classes and descriptors', '''
Attribute lookup~Demonstrate instance versus class attributes and explain lookup after shadowing an instance name.
Properties~Replace a public field with a validating property while preserving its external usage.
Descriptors~Implement a validating data descriptor and compare its precedence with the instance dictionary.
Method binding~Inspect a bound method's __self__ and __func__; contrast staticmethod and classmethod.
Inheritance and super~Use a small diamond hierarchy to trace cooperative super calls and inspect the method resolution order.
Slots~Compare presence of __dict__ in slotted and ordinary instances; measure rather than invent a memory saving.
'''),
('Data classes and modeling', '''
Dataclass defaults~Use default_factory for a mutable field and prove instances do not share it.
Frozen models~Demonstrate that frozen prevents field assignment but does not deeply freeze contained mutable objects.
Ordering and hashing~Inspect generated equality, order and hash behavior under two dataclass configurations.
Enums~Model job states with Enum and validate transitions using values rather than magic strings.
Composition~Replace an inheritance-only configuration example with a composed policy object and test it in isolation.
Model boundary~Convert an untrusted mapping into a validated model without silently accepting missing required fields.
'''),
('Typing foundations for experienced developers', '''
Annotations at runtime~Annotate a function then deliberately pass the wrong type; show annotations alone do not enforce validation.
Optional and narrowing~Write a function accepting str or None with a clear narrowing branch and no unchecked dereference.
Typed dictionaries~Describe a JSON-like payload with TypedDict and required versus optional keys; distinguish schema description from runtime checks.
Protocols~Specify a small structural interface and write two implementations without a common base class.
Generics~Write a generic first-item helper that preserves element type; define empty-input behavior.
Overloads~Describe distinct return types with overload declarations plus one real implementation; explain which code runs.
'''),
('Advanced typing and API contracts', '''
Callable signatures~Annotate a higher-order function and preserve its arguments with ParamSpec where appropriate.
Variance reasoning~Explain why a read-only sequence can be more flexible than a mutable list; construct a mutation counterexample.
Literal states~Use Literal for a finite mode and exhaustive branching; keep runtime validation at the external boundary.
Type guards~Write and test a predicate narrowing an object after checking its real structure.
NewType~Separate two integer identifier domains using NewType; show that runtime representation remains unchanged.
Typing debt~Review one existing practice solution and replace Any only where it clarifies a real interface.
'''),
('Exceptions and resource lifetime', '''
Exception chaining~Catch a low-level error and raise a domain error with from; inspect both traceback and cause.
Exception boundaries~Replace a broad catch with specific exceptions and prove programmer bugs remain visible.
Finally behavior~Demonstrate why returning from finally can hide an exception; remove that behavior.
Contextlib~Write a contextmanager function that releases a resource when its body fails.
ExitStack~Manage a variable number of resources and confirm reverse-order cleanup with a local trace.
Exception groups~Create an ExceptionGroup and handle one subgroup with except* without losing the rest.
'''),
('Testing and debugging', '''
Unittest subtests~Write boundary cases using subTest and intentionally break one expectation to inspect failure output.
Test doubles~Inject a fake clock into timeout logic instead of sleeping in tests.
Mock boundaries~Patch a dependency where the consuming module looks it up and explain why the definition module can be the wrong target.
Property checks~Use seeded random small inputs to compare an optimized solution with a deliberately simple oracle.
Metamorphic tests~Choose an input transformation that preserves a known result and encode the relationship as a test.
Debugging workflow~Reproduce one failure, minimize its input, inspect state, then keep a regression test.
'''),
('Collections and algorithms in Python', '''
Deque behavior~Compare endpoint operations on deque with list front deletion using operation reasoning and a small measurement.
Counter algebra~Test Counter subtraction versus subtract, including zero and negative counts.
Default dictionaries~Show which access forms create a missing entry and which do not.
Heap ordering~Store priority, tie-breaker and payload tuples in heapq so equal priorities do not compare arbitrary objects.
Bisect contracts~Test bisect_left and bisect_right with duplicates; distinguish logarithmic search from linear list insertion.
Sorting keys~Demonstrate stable multi-key sorting and why a key function is preferable to repeated derived comparisons.
'''),
('Functional tools and caching', '''
Itertools grouping~Show groupby groups adjacent keys and compare behavior before and after sorting.
Iterator duplication~Inspect tee behavior with consumers progressing at different rates; explain buffered memory risk.
Bounded iteration~Use islice and batched where available in the pinned interpreter; test a final short batch.
Function caching~Use lru_cache on a pure function and inspect hits/misses; identify argument hashability requirements.
Cache invalidation~Create a cached function reading mutable external state, reproduce staleness and add an explicit invalidation policy.
Dispatch~Use singledispatch for two data types and explain first-argument runtime dispatch.
'''),
('Async fundamentals', '''
Coroutine lifecycle~Distinguish coroutine object creation from awaiting and task scheduling with a local trace.
Blocking the loop~Compare a cooperative sleep with a blocking call in an isolated demo; explain the observed scheduling.
Concurrent tasks~Run independent coroutines with TaskGroup and compare elapsed behavior without asserting fragile exact timing.
Cancellation~Cancel a task waiting on an event and ensure finally cleanup runs; propagate cancellation.
Timeout scopes~Use asyncio.timeout around a bounded local operation and inspect the resulting exception boundary.
Async context managers~Implement async setup and cleanup using asynccontextmanager and test failure in the body.
'''),
('Async reliability', '''
Bounded concurrency~Use a semaphore around simulated work and assert observed concurrency never exceeds the bound.
Async queues~Build a tiny producer/consumer example using a bounded queue and correct task_done/join pairing.
Task failure~Show one TaskGroup child failure canceling peers; inspect the actual exception group.
Context variables~Keep per-task request identifiers using contextvars and verify isolation across concurrent tasks.
Offloading blocking work~Use asyncio.to_thread for a small blocking function; explain why canceling the await does not forcibly stop the thread.
Async shutdown~Stop intake, finish or cancel workers, and verify no owned tasks remain pending.
'''),
('Threads and processes', '''
Thread ownership~Design shared-counter synchronization with a Lock; do not assume a race must reproduce on every run.
Condition signaling~Use an Event or Condition to coordinate a worker without arbitrary sleeps.
Thread pools~Collect results and exceptions through futures and define executor shutdown behavior.
Process pools~Run a top-level picklable function under an if __name__ guard; explain Windows spawn constraints.
Serialization cost~Measure transfer cost for a modest payload and explain when process parallelism loses to overhead.
GIL boundaries~Separate interpreter-specific threading behavior from language guarantees; check current documentation before discussing free-threaded builds.
'''),
('Profiling and memory', '''
Measurement design~Use timeit for two equivalent small functions with repeated measurements and recorded interpreter version.
CPU profiles~Profile a deliberately repeated operation with cProfile and distinguish cumulative from self time.
Allocation tracing~Use tracemalloc snapshots around retained objects and identify an allocation site.
Reference cycles~Create a cycle, inspect gc behavior and explain why prompt destruction is not portable semantics.
Weak references~Build a weak-reference lookup for objects and distinguish cache ownership from observation.
Optimization memo~Optimize one measured hotspot, keep behavior tests and record before/after measurements without universal speed claims.
'''),
('Files, text and data boundaries', '''
Path handling~Use pathlib with a temporary directory and explicit encoding; avoid dependence on the working directory.
Unicode normalization~Compare canonically equivalent strings before and after normalization; distinguish code points from displayed characters.
Binary interfaces~Use bytes, bytearray and memoryview to demonstrate immutable, mutable and view behavior.
JSON boundaries~Validate a parsed JSON object's shape before use; test malformed input and unexpected types.
Decimal arithmetic~Compare a decimal constructed from a string versus a float and explain the input representation effect.
Timezone handling~Create aware datetimes with zoneinfo and reason about ambiguous local times using documented behavior.
'''),
('Persistence and safe I/O', '''
SQLite transactions~Use a temporary sqlite3 database, parameterized statements and an explicit transaction; force a rollback.
CSV streaming~Read CSV using newline handling and explicit encoding; test quoted delimiters and embedded newlines.
Atomic replacement~Write a temporary sibling file then replace the target; explain filesystem and durability limits separately.
Subprocess contracts~Run the current interpreter with an argument list, capture output and check nonzero exit status without shell interpolation.
Untrusted serialization~Explain why pickle is inappropriate for untrusted input; implement a JSON-based boundary for a small model.
Resource limits~Read a stream in bounded chunks with a maximum total size and test rejection at the boundary.
'''),
('Modules, imports and packaging', '''
Import execution~Use two tiny temporary modules to show import-time execution and module caching.
Circular imports~Construct a minimal circular dependency, capture its actual failure and repair the responsibility split.
Entry points~Separate reusable functions from the __main__ entry point and test importing without side effects.
Package layout~Sketch a src-layout package, tests and pyproject.toml; explain runtime versus build dependencies.
Environment isolation~Record the active interpreter and environment paths and explain how to avoid installing into the wrong interpreter.
Dependency policy~Classify direct and transitive dependencies and define upgrade, compatibility and reproducibility checks.
'''),
('Production Python service code', '''
Structured logs~Emit a correlation field via logging without including credentials or full sensitive payloads.
Configuration~Parse environment-like input into typed settings with explicit missing/invalid errors and no real secrets.
Retry wrapper~Inject clock, sleep and operation dependencies into a bounded retry function; test without real delays.
Idempotent handler~Implement a small in-memory event handler with duplicate detection; state restart and concurrency limitations.
Shutdown hooks~Design explicit start/stop methods and a context-managed lifecycle for a worker object.
Error taxonomy~Map validation, transient dependency and internal errors to distinct domain exceptions without leaking low-level details.
'''),
('Internals and version-aware Python', '''
Bytecode inspection~Use dis on two small functions and separate observed implementation details from semantic guarantees.
Object sizes~Compare sys.getsizeof with retained graph size; demonstrate why shallow size omits referents.
Name resolution~Inspect locals, globals and closure variables for a function with nested scope.
Special method lookup~Demonstrate implicit special-method lookup on a type versus assigning a same-named instance attribute.
Version compatibility~Choose one feature newer than the local interpreter, read its official version note and design a fallback without pretending it ran locally.
Implementation portability~Review an optimization relying on CPython behavior and write the assumption plus a portable alternative.
'''),
('Code review and refactoring', '''
API simplification~Refactor a boolean-flag-heavy function into explicit operations while keeping behavior tests.
Hidden state~Remove one module-global mutable dependency by passing it explicitly.
Mutable ownership review~Audit a function returning internal collections and decide between copying, views and documented mutation.
Concurrency review~Review an async function for blocking calls, unbounded task creation and swallowed cancellation.
Typing review~Find where annotations obscure rather than clarify a small interface; simplify and document runtime validation.
Performance review~Reject an unmeasured optimization, design the benchmark, then make a decision from evidence.
'''),
('Python interview drills', '''
Semantics drill~Explain aliasing, equality, hashability and mutable defaults using four tiny executable counterexamples.
Protocol drill~Implement a small iterable context-managed resource and explain both protocols out loud.
Typing drill~Design a typed storage interface with two implementations and explain structural versus nominal typing.
Concurrency drill~Choose threads, processes or async for three workloads and justify using blocking behavior and data sharing.
Debugging drill~Take a previous bug, reproduce it from a fresh process and narrate hypothesis, evidence and repair.
Review drill~Review one DSA solution for clarity, complexity accounting, mutation, tests and Python-specific hidden costs.
'''),
('Python capstone and retention', '''
Capstone interface~Specify a tiny local job runner's typed inputs, outputs and failure contract; keep the scope small.
Capstone generator~Implement lazy job input and deterministic cleanup when consumption stops early.
Capstone execution~Add one bounded execution strategy and explain ownership of tasks or worker threads.
Capstone tests~Add fake-clock tests for timeout/retry decisions and a real failure-path test.
Capstone profile~Measure one representative workload and document the main cost without premature optimization.
Final explanation~Explain three design decisions, one bug caught by tests and one deferred improvement with a measurable trigger.
'''),
]


def weeks():
    assert len(DSA) == len(SD) == len(LANG) == 24
    result = []
    for i, (dsa, sd, lang) in enumerate(zip(DSA, SD, LANG), 1):
        parsed = []
        for title, raw in (dsa, sd, lang):
            rows = [line.split('~') for line in raw.strip().splitlines()]
            assert len(rows) == 6, (i, title, len(rows))
            parsed.append(rows)
        result.append({'week': i, 'themes': [dsa[0], sd[0], lang[0]],
                       'dsa': parsed[0], 'sd': parsed[1], 'lang': parsed[2]})
    return result
