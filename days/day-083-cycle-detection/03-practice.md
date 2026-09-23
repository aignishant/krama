---
day: 83
track: practice
title: "Practice — Cycle detection, and why Floyd's algorithm works"
status: written
---

# Day 083 · Practice

**DSA topic:** Cycle detection, and why Floyd's algorithm works
**System design topic:** Design tic-tac-toe, and then chess

---

## Code these, in this order

One rule for the whole set: **say the hash-set solution out loud first, then improve on it.** Naming
the O(n)-space baseline before writing the clever one is worth more than jumping straight to Floyd's,
and it is what you should do in a real interview.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Linked List Cycle | LeetCode 141 (Easy) | The two runners, `is` versus `==`, and advancing before comparing. |
| 2 | Linked List Cycle II | LeetCode 142 (Medium) | Phase two, and whether you can prove it rather than recite it. |
| 3 | Happy Number | LeetCode 202 (Easy) | Recognising a cycle question that has no linked list in it. |
| 4 | Find the Duplicate Number | LeetCode 287 (Medium) | The hardest reframing: an array read as a function, with the duplicate as the cycle entrance. |

### On problem 2, do the arithmetic before you code

Write out `a`, `b` and `c`, derive `a = kc − b`, and say the sentence that turns it into an
instruction. Only then write the three lines. If you write the code first you will not be able to
defend it.

### On problem 3, find the cycle without a list

There are no nodes here — the "next" of a number is the sum of the squares of its digits. Write the
`next` function first, then run exactly the same two-runner loop on it. Say out loud why the walk must
eventually repeat.

### On problem 4, say why each obvious solution is banned

Sorting mutates. A set costs O(n) space. Marking with negatives mutates. Only then explain the
index-to-value mapping and why the duplicate is the entrance. If you cannot state all three
rejections, you do not yet know why the problem is stated the way it is.

---

### The why-they-meet drill

Say each answer out loud, five times:

1. Why can a faster runner only catch a slower one from behind on a route that loops?
2. What happens instead if the route ends?
3. What is the forward gap doing on every step once both are inside the loop?
4. Why can that gap not skip over zero?
5. What would break if the ratio were 3:1 instead of 2:1? Give a concrete cycle length.

### The proof drill

1. Define `a`, `b` and `c` in words.
2. Write the two distances walked when they meet.
3. Derive `a + b = kc` and then `a = kc − b`.
4. Turn the last line into an instruction about where to walk from the meeting point.
5. State the `k = 1` version in one sentence about distances.
6. Deliver the whole thing in thirty seconds, without notes.

### The break-it drill

Trigger each and record the exact output or error text:

1. Use `==` instead of `is`, on a `Node` class with `__eq__` defined on the value.
2. Compare before advancing. Run any non-empty list.
3. Return the meeting point as the cycle start. Run the six-node example, then run a list that is
   entirely one cycle, and say why the second one hides the bug.
4. Put the loop condition in the wrong order. Run an even-length list with no cycle.
5. Add a safety counter to phase two. Say what it means about your own proof.
6. Detect the cycle by marking nodes as visited. Say what you have destroyed.

### The edge-case drill

Build and run each shape:

1. An empty list.
2. A single node with `next = None`.
3. A single node pointing at itself.
4. A two-node list with no cycle.
5. A list where the entire thing is one cycle.
6. A long tail with a two-node cycle at the end.

For each, state `a`, `b` and `c`, and check that phase two returns what you expect. Two of the six are
where "return the meeting point" accidentally looks correct.

### The complexity drill

1. Bound phase one, in terms of `a` and `c`, and justify the `c` part.
2. Bound phase two exactly.
3. State the total in terms of `n`.
4. State the space, and the memory of the set version at a million nodes.
5. Say which of the three approaches — set, Floyd's, marking — fails which constraint.

### The reframing drill

For each, say whether Floyd's applies, and if so what plays the part of "next":

1. A linked list.
2. Replacing a number with the sum of the squares of its digits.
3. An array of n+1 values in 1..n, read as `i -> nums[i]`.
4. A directed graph where every node has exactly one outgoing edge.
5. A directed graph where nodes have several outgoing edges.
6. A random number generator's sequence of states.

One of the six does not work. Name it and say precisely why the algorithm needs what it lacks.

---

### The counter drill

1. State the observation that makes the O(1) win check possible, in one sentence.
2. Write the four updates for a move at `(row, col)`.
3. Say why `+1` and `−1` beats two separate counts per line.
4. Write the win test and say why `abs(count) == n` is unambiguous.
5. Compute the naive and counter costs at N = 3, N = 100 and N = 1000.
6. Compute the total operations over a full game at N = 1000, both ways.
7. State the memory overhead as a percentage of the board.

### The diagonal drill

1. Write both diagonal conditions.
2. Say which cells satisfy both on a 3×3, a 4×4 and a 5×5.
3. Change the second `if` to an `elif` and construct the game that now reports no winner.
4. Say why this bug survives most testing.

### The win-condition drill

1. Apply the interface gate to `WinCondition` and name the second implementation.
2. Say why k-in-a-row cannot use the counters.
3. Write the four directions it scans and say why four and not eight.
4. State its cost per move and say what it does *not* depend on.
5. Say what would have gone wrong if you had added k-in-a-row as a parameter to the counter version.

### The chess-responsibility drill

For each rule, say whether it belongs to `Piece`, `Board`, or `Game`, and why:

1. A knight moves in an L.
2. A rook cannot jump over a piece.
3. You may not leave your own king attacked.
4. White moves first.
5. Castling requires that neither piece has moved.
6. En passant is only available immediately after a two-square pawn advance.
7. A pawn reaching the last rank becomes another piece.
8. The game is a draw after fifty moves with no capture or pawn move.

Three of the eight cannot belong to any single piece. Name them and say what they have in common.

### The two-stage drill

1. Say why `pseudo_legal_moves` is a better method name than `can_move`.
2. Write the legality filter in nine lines.
3. Say what `apply` must return and why.
4. Compute the cost of copying the board instead, per position and at a million positions a second.
5. Name the bug that make-and-unmake makes possible, and the language feature that prevents it.

### The forgotten-state drill

1. List the five pieces of state beyond "which piece is on which square".
2. For each, name a rule that is unimplementable without it.
3. Say roughly how many bytes all five take.
4. Say which standard format forces you to have remembered all of them.

### The endgame drill

1. Write the test that distinguishes checkmate from stalemate.
2. Name the three draw conditions this design does not yet handle.
3. Say what data structure each one needs.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Detect a cycle in a linked list. Now find the node where it begins.*
   The hash-set baseline named first, the rho shape, the two runners with *why* a faster runner can
   only catch from behind, the shrinking-gap answer to "could it skip past", phase two, and the
   four-line proof delivered without notes.

2. *Design tic-tac-toe. Now make it work for an N by N board.*
   The naive O(N²) check costed with a number, the observation about lines through the played square,
   the ±1 counters with the two separate diagonal `if`s, the memory overhead as a percentage, and the
   win condition behind an interface with the honest note that k-in-a-row does not share the
   algorithm.

3. *Where does "you cannot move into check" live?*
   Not on the piece, and the three reasons a piece cannot decide legality; pseudo-legal generation
   plus the game's filter; make, test, unmake, with the copying number that justifies it.

---

## Before you move on

- [ ] I state the hash-set baseline before writing Floyd's.
- [ ] I can say why a faster runner can only catch a slower one from behind.
- [ ] I can answer "could the fast pointer skip past" with the shrinking-gap argument.
- [ ] I can say what breaks at a 3:1 ratio, with a concrete cycle length.
- [ ] I can derive `a = kc − b` and turn it into an instruction, in thirty seconds.
- [ ] I returned the meeting point on purpose and found the shape where it looks correct.
- [ ] I ran all six edge shapes and checked `a`, `b` and `c` for each.
- [ ] I solved Find the Duplicate Number and can state all three rejected approaches.
- [ ] I can state the observation behind the O(1) win check in one sentence.
- [ ] I computed naive versus counter cost at N = 1000, per move and per game.
- [ ] I turned the second diagonal `if` into an `elif` and built the game that breaks.
- [ ] I can say why k-in-a-row needs a different algorithm, not a parameter.
- [ ] I can sort eight chess rules into piece, board and game.
- [ ] I can name the three rules no single piece can own, and what they have in common.
- [ ] I can justify make-and-unmake with the copying arithmetic.
- [ ] I can list the five pieces of forgotten chess state and a rule that needs each.
- [ ] I answered all three questions above out loud.
