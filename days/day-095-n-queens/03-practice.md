---
day: 95
track: practice
title: "Practice — N-Queens and constraint grids"
status: written
---

# Day 095 · Practice

**DSA topic:** N-Queens and constraint grids
**System design topic:** Design an online auction

---

## Code these, in this order

One rule for the whole set: **reduce out loud before writing.** Say how many candidates the obvious
framing has, then say how many yours has. On N-Queens that is four billion against forty thousand, and
the reduction is worth more than the code.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | N-Queens II | LeetCode 52 (Hard) | The three constraint sets, and counting without building boards. |
| 2 | N-Queens | LeetCode 51 (Hard) | The same tree, plus rendering only at a solution. |
| 3 | Sudoku Solver | LeetCode 37 (Hard) | Row, column and box sets, and the `(r//3)*3 + c//3` index. |
| 4 | Valid Sudoku | LeetCode 36 (Medium) | The same three sets with no search at all — do it last, as the check. |

### On problem 1, count the nodes both ways

Write it once with the conflict check before the recursive call and once with it at the leaf. Record
the node counts for n = 6 and n = 8. Then say the ratio out loud.

### On problem 2, time the rendering

Run n = 12 with the board strings built at every call, and again with them built only at a solution.
Record both times and say what fraction of the work the rendering was.

### On problem 3, pre-compute the blanks

Write it scanning for the next blank from `(0,0)` every call, then with a pre-computed list of blanks
indexed by depth. Record the call counts and the times for a hard puzzle.

### On problem 4, notice what is missing

There is no recursion here at all. Say in one sentence what problem 4 shares with problems 1 to 3, and
what it does not have.

---

### The reduction drill

1. State the four framings and their sizes for n = 8, in order.
2. Say which observation takes you from each one to the next.
3. Say what representation the "one per row" framing implies.
4. Say what conflict becomes unrepresentable, and why that is better than checking for it.

### The diagonal drill

1. Say what is constant along a `\` diagonal and along a `/` diagonal.
2. Draw both value grids for a 4 × 4 board.
3. Give the range of each expression for general `n`.
4. Say what offset a list-based version needs, and which of the two needs it.
5. Run the version without the offset and describe what you get — and why there is no error.

### The pruning drill

1. Say the one line that separates this from brute force.
2. Say exactly where it goes.
3. Record the node counts for n = 6 and n = 8, both ways.
4. Say why the number of *solutions* is unchanged.
5. Say what the undo has to do with whether the check is affordable.

### The undo drill

1. Count the changes before the recursive call, and the restores after.
2. Delete the anti-diagonal restore and run `total_n_queens(8)`. Record the answer.
3. Say why the answer is what it is, and why nothing was raised.
4. Say what makes four pieces of state harder than one.

### The edge-case drill

1. Give the solution counts for n = 1 through n = 10 from memory or by running it.
2. Say which two values of `n` have none.
3. Say what breaks in code that assumes a non-empty result.
4. Say whether there is a formula for the count.

### The bitmask drill

1. Write the bitmask version of the counter.
2. Say what `available & -available` does.
3. Say why `cols` does not shift but `diag` and `anti` do, and in which direction each.
4. Time it against the set version at n = 12 and record the ratio.
5. Say when you would write it in an interview and when you would only mention it.

### The Sudoku drill

1. Name the three constraint sets.
2. Write the box index expression and check it for `(4, 7)`.
3. Say what depth means here, versus in N-Queens.
4. Say why the search returns `True` up the stack instead of exploring everything.
5. Describe the most-constrained-cell heuristic and say when it pays for itself.

### The cost drill

1. State the upper bound and say honestly why it is loose.
2. Give the measured node counts and running times for n = 8, 12 and 14.
3. State the extra space and say what the representation saved you.
4. Compute the output size for n = 12 and say why the counting version is faster.
5. Say what the symmetry trick saves, and what it does not change.

---

### The proxy drill

1. Say what is stored when someone bids ₹1,200.
2. Work the Ibrahim example through: three bids, and the price after each.
3. Name the four cases in `resolve` and say which one people forget.
4. Say what a losing bid does to the price, and why.
5. Say where a leaked maximum could appear, and what it would let someone do.

### The race drill

1. Write the conditional `UPDATE` from memory.
2. Trace two simultaneous bids through it, both branches.
3. Write the version that is wrong, and name the failure.
4. Say what the loser does after a zero-row update.
5. Say why you would not use a distributed lock here.

### The deadline drill

1. Say what the authority for "is bidding open" is, and what it is not.
2. Say what goes wrong if a status column is the authority and the job runs late.
3. Say why `ENDED` and `SOLD` are separate states.
4. Compare scheduled close against lazy close on the "job is late" row.

### The anti-snipe drill

1. Write the extension rule in two lines.
2. Say what a live auctioneer does and why.
3. Name the two policy decisions it needs.
4. Say what the design gives up by extending, in terms of the product.

### The numbers drill

Compute each, showing the multiplication:

1. Bids per day and per second at 10M active auctions, 12 bids each, over 7 days.
2. Writes per second on a single row for a hot auction with 1,000 bids in 30 seconds.
3. The collision probability and expected attempts at a 2 ms window.
4. Bid storage per day and per year at 200 bytes a row.
5. The read:write ratio, and what it says about caching.

### The failure drill

For each, say what happens and what you would add:

1. Two bids read the same version and both write unconditionally.
2. A bidder's phone submits the same bid twice.
3. The closing job runs thirty seconds late.
4. The current price is served from a two-second cache on the bid path.
5. A seller's friend bids the item up and then withdraws.
6. The winner's payment declines after `SOLD`.

Two of the six are not concurrency problems. Name them and say what kind of problem they are.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Place n queens on an n by n board.*
   The reduction first with all four numbers, the list-of-columns representation, the two diagonal
   expressions with their justification, the check placed before the descent with the 2,057 against
   19,173,961, four changes and four restores, and an honest complexity that admits the bound is loose.

2. *Design an auction site. Two bids arrive in the same millisecond.*
   What is actually stored, the conditional update with the version and both branches traced, the lost
   update named as the thing you are avoiding, the end time as the authority, anti-sniping as policy,
   and the numbers that make it a contention problem rather than a throughput one.

3. *Now solve a Sudoku board.*
   The same three-set technique, the box index expression, the pre-computed blanks, and the one thing
   that differs — returning as soon as a solution is found.

---

## Before you move on

- [ ] I can give the four framings of N-Queens and their sizes for n = 8.
- [ ] I can say why there is exactly one queen per row without being told.
- [ ] I can justify both diagonal expressions in one sentence each.
- [ ] I know which one needs an offset in a list version, and what happens without it.
- [ ] I recorded the node counts for n = 6 and n = 8 both ways.
- [ ] I can count four changes and four restores before running.
- [ ] I deleted one restore and can explain the zero.
- [ ] I know that n = 2 and n = 3 have no solutions.
- [ ] I can explain the bitmask shifts, and which mask does not shift.
- [ ] I can write the Sudoku box index and check it on a cell.
- [ ] I can state the complexity honestly, including that the bound is loose.
- [ ] I can say what is stored when someone bids ₹1,200, and what is displayed.
- [ ] I can name the four proxy cases and the one people forget.
- [ ] I can write the conditional `UPDATE` and trace two simultaneous bids.
- [ ] I can name the lost update and say why it is worse than an error.
- [ ] I can say what the authority for "bidding is open" must be, and why.
- [ ] I can produce the 200 bids/second and 170 writes/second-on-one-row numbers.
- [ ] I answered all three questions above out loud.
