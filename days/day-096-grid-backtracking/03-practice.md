---
day: 96
track: practice
title: "Practice — Sudoku, word search, and grid backtracking"
status: written
---

# Day 096 · Practice

**DSA topic:** Sudoku, word search, and grid backtracking
**System design topic:** Low-level design revision and full mock

---

## Code these, in this order

One rule for the whole set: **say "path" or "region" out loud before writing a single line.** Path
clears the marker on the way out; region never does. That one word decides whether your solution is
exponential or linear, and getting it backwards produces a wrong answer rather than a crash.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Number of Islands | LeetCode 200 (Medium) | The region version: mark and never restore. Do this first, as the contrast. |
| 2 | Word Search | LeetCode 79 (Medium) | The path version: mark, explore, restore — and bounds before the match. |
| 3 | Flood Fill | LeetCode 733 (Easy) | Region again, with the trap that the new colour may equal the old one. |
| 4 | Sudoku Solver | LeetCode 37 (Hard) | Three sets, pre-computed blanks, and the most-constrained cell. |

### On problem 1, break the marker deliberately

Write it so the cell is restored after the four recursive calls. Run it on a 2 × 2 grid of land and
record what happens. Then say why the same island gets counted more than once.

### On problem 2, remove the bounds check

Run `["AB", "CD"]` looking for `"ADA"` with and without the bounds check. Record both answers, and say
why the version without it raises nothing at all.

### On problem 3, run it where the new colour equals the old

Start at a cell whose colour already equals the target colour. Say what happens and what one line fixes
it. This is a region problem whose marker is the colour itself.

### On problem 4, time the heuristic

Solve an easy puzzle and a deliberately hard one, in-order and most-constrained. Record four numbers.
Say when the heuristic earns its keep and when it costs more than it saves.

---

### The classify drill

1. Say the one-sentence test for path versus region.
2. Put these into the two buckets: word search, islands, rat in a maze, flood fill, all paths, largest
   connected region.
3. Say what happens to a path problem if you do not clear the marker.
4. Say what happens to a region problem if you do clear it, including the error.
5. State the complexity of each kind and say which line causes the difference.

### The bounds drill

1. Write the direction tuple from memory.
2. Say why the bounds check must be first, and what Python does without it.
3. Give the input that finds a word that is not there.
4. Say what changes for an eight-direction problem.

### The marking drill

1. Write the mark-and-restore in four lines.
2. Say what the sentinel character assumes about the input.
3. Say what you would use instead if that assumption is not safe.
4. Write it with `any(...)` and say why that is safer than a loop with an early return.
5. Say what the in-place marking costs the caller.

### The prune drill

1. Write the character-count check.
2. Write the reverse-the-word check and say what quantity it reduces.
3. Construct a grid and word where reversing gives a 36× improvement.
4. Say what both prunes cost, and why that cost is always worth paying.
5. Say what you would do differently if you had to find a hundred words instead of one.

### The cost drill

1. State the complexity of word search and explain where the `3` comes from.
2. Compute the worst-case path count on a 6 × 6 grid for L = 4, 8, 12 and 16.
3. State the space, and say what dominates it in each of the two kinds of problem.
4. Say which one can raise `RecursionError`, on what input, and what you would do instead.

### The Sudoku drill

1. Name the three sets and write the box index expression.
2. Say why the blanks are pre-computed and what it saves.
3. Describe the most-constrained-cell rule in one sentence.
4. Say why it costs a scan per node and why that is still a win.
5. Count the changes and the restores in the inner loop.

### The break-it drill

Trigger each and record the exact output or error:

1. Word search with the restore removed.
2. Islands with a restore added.
3. Word search without bounds, on a two-row grid.
4. `board[:]` used as a copy of a grid.
5. Flood fill where the new colour equals the old.
6. Sudoku scanning for blanks from `(0,0)` every call, timed against the pre-computed version.

---

### The five-moves drill

1. Name the five moves and the minute each one ends.
2. Say what you say out loud at minutes 5, 10, 20, 30 and 38.
3. Say which move you are actually being marked on.
4. Say the question that finds the interesting part.

### The pattern-recall drill

For each prompt, name the interesting part and the interface that goes there, without looking:

1. Parking lot. 2. Elevator. 3. ATM. 4. Vending machine. 5. Splitwise. 6. BookMyShow.
7. Ride-hailing. 8. Rate limiter. 9. Cache. 10. Logging. 11. Notifications. 12. File system.
13. Snake and ladder. 14. Auction.

Then say how many of the fourteen are a strategy, and what that tells you to reach for first.

### The tells drill

1. Give the four phrases and the pattern each one names.
2. Give an example prompt for each.
3. Name the two structural rules that came up in nearly every case study.
4. Say what each of the five losing mistakes looks like in a transcript.

### The chess drill

1. State the four clarifying questions, with your assumed answers.
2. Say which of the four is the one that impresses, and why.
3. Name the classes and say which one is abstract.
4. Say what `SlidingPiece` exists for and which three pieces use it.
5. State the two layers of legality and give the example that proves they are different.
6. Write the apply-check-undo loop and say why `Move` must carry the captured piece.
7. Define checkmate and stalemate in one line each.
8. Say where castling attaches and name its four guards.

### The self-criticism drill

1. Name three things wrong with the chess design before anyone asks.
2. For each, say what you optimised for instead.
3. Say what you would change if this had to search millions of positions.
4. Say what you would say at minute 38 if castling were still unwritten.

### The numbers drill

Compute each, showing the multiplication:

1. Memory for one chess game, and for 100,000 concurrent games.
2. The same for snake and ladder, and say why the two answers lead to different architectures.
3. Board checks per `legal_moves()` call.
4. Say what that figure means for a human game and for an engine.

### The concurrency-map drill

For each, say the mechanism from memory:

1. Two bids on one auction.
2. Two people booking the same seat.
3. Two `mkdir` calls for the same directory.
4. Two players acting in one game.
5. Two threads writing to one cache.

Say which of the five is the "inherently serial" case and what that buys you at scale.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Solve the sudoku board. Now find the word in the grid.*
   Path or region named first, the three sets and the box index for Sudoku, bounds before match for the
   grid, mark-and-restore with the reason, the complexity with the `3` explained, and the two one-line
   prunes.

2. *Design a chess game. Forty minutes. Begin.*
   Scope and exclusions in one sentence, the history question asked at minute two, the class list with
   `SlidingPiece` justified, the two layers of legality with the pinned-knight example, apply-check-undo
   with the reason `Move` stores the capture, and checkmate and stalemate in two lines.

3. *What is the same in every low-level design prompt?*
   The five moves with their minutes, the question that finds the interesting part, the fact that most
   prompts resolve to a strategy, the four tells, and the two structural rules about replaceable
   dependencies and returned results.

---

## Before you move on

- [ ] I say "path" or "region" before writing any grid code.
- [ ] I can state what happens if I get that backwards, in both directions.
- [ ] I write the bounds check first, and know why its absence raises nothing.
- [ ] I can write mark-and-restore with `any(...)` and say why not a loop with an early return.
- [ ] I can name the assumption behind the sentinel character.
- [ ] I can write both one-line prunes and say what each one reduces.
- [ ] I can explain where the `3` in the complexity comes from.
- [ ] I know which kind of grid problem raises `RecursionError`, and on what input.
- [ ] I can write the Sudoku box index and describe the most-constrained rule.
- [ ] I can name the five moves and their minutes.
- [ ] I can name the interesting part for at least ten of the fourteen prompts.
- [ ] I can give the four tells and the pattern each names.
- [ ] I can state the two layers of chess legality with the pinned-knight example.
- [ ] I can define checkmate and stalemate in one line each.
- [ ] I can say why `Move` must carry the captured piece.
- [ ] I can name three faults in my own chess design.
- [ ] I answered all three questions above out loud.
