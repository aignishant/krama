---
day: 94
track: practice
title: "Practice — Backtracking: the undo step"
status: written
---

# Day 094 · Practice

**DSA topic:** Backtracking: the undo step
**System design topic:** Design snake and ladder

---

## Code these, in this order

One rule for the whole set: **before you run anything, count the lines that change shared state before
the recursive call and the lines that change it back after.** They must match. Do the counting with your
finger on the screen; the missing undo is always silent.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Letter Combinations of a Phone Number | LeetCode 17 (Medium) | One piece of state, one undo — the template with nothing else in the way. |
| 2 | Palindrome Partitioning | LeetCode 131 (Medium) | The validity check placed *before* the recursive call, not at the leaf. |
| 3 | Generate Parentheses | LeetCode 22 (Medium) | Two counters as arguments, so there is nothing to undo at all. |
| 4 | Restore IP Addresses | LeetCode 93 (Medium) | Several prunes, and a partial answer that must be undone by exact length. |

### On problem 1, write both styles

Write it with `current.append(...)` plus a pop, then again with `explore(prefix + letter)`. Confirm the
same answers. Then say which one allocates more, and where.

### On problem 2, move the check and measure

Write it checking `is_palindrome` at the leaf, then checking it before recursing. Count the calls both
ways for a 16-character string of all the same letter. Record both numbers.

### On problem 3, notice there is no undo

Both counters are parameters. Say why that means nothing needs restoring, and name the one thing in the
function that still does.

### On problem 4, break the undo deliberately

Remove the undo and run `"25525511135"`. Record the output length. Then put the undo after the loop
instead of inside it and record what happens.

---

### The invariant drill

1. State the invariant in one sentence.
2. Say what is true of every sibling branch if the invariant holds at every node.
3. Say what happens to the siblings if it fails at exactly one node.
4. Say why the failure raises no error.

### The three-kinds-of-state drill

1. Name the three kinds of state that need undoing.
2. For permutations, name which of your lines belongs to which kind.
3. For N-Queens, list all four things that must be undone.
4. Say which kind is the one that does not look like state, and give an example.
5. Say what the rule is for whether something needs an undo at all.

### The arguments drill

1. Write a version of combination sum that mutates a running total, with its undo.
2. Write the version that passes `remaining` as a parameter.
3. Say why the second one has nothing to undo.
4. Name three types that are safe to pass this way, and say what they have in common.
5. Say what this technique buys you beyond correctness.

### The placement drill

1. Write the three-line block and say where exactly the undo goes.
2. Move it outside the loop, run subsets on `[1,2,3]`, record the output.
3. Say why the answers get longer and longer.
4. Quote the error that eventually appears.
5. Say why a "reset everything at the top of the function" version is worse than correct.

### The early-return drill

1. Write a grid search that returns `True` on success.
2. Say whether the undo runs on that path.
3. Say when that is harmless and when it is a bug.
4. Rewrite it so the undo always runs, and say how many extra lines that cost.
5. Describe the symptom of the bug in terms of a test suite.

### The two-styles drill

1. Write subsets both ways.
2. Say how many allocations each makes, in terms of nodes and leaves.
3. Compute both for permutations at n = 9.
4. Say what happens if you mix the styles, and quote the error.
5. Give the one-sentence justification you would say out loud for choosing the mutating version.

### The pruning drill

1. Say the single line that turns enumeration into backtracking.
2. Say where it must go, and where it must not.
3. Run the N-Queens counter for n = 6 and n = 8 and record all four numbers.
4. Say what the undo has to do with whether pruning is affordable.
5. Say why every undo in this phase is O(1), and what it would mean if yours were not.

### The break-it drill

Trigger each and record the exact output or error:

1. One of two undoes omitted, in permutations.
2. The undo placed after the loop.
3. `current.pop()` after passing `current + [x]` down.
4. `board[:]` used as a snapshot of a list of lists.
5. `available.remove(x)` inside `for x in available`.
6. The validity check moved to the leaf, timed rather than printed.

---

### The one-object drill

1. Say why a snake and a ladder are the same object, in one sentence.
2. Write the board lookup in one line, and say what the default argument does.
3. Say how `is_ladder` is obtained, and why it is not stored.
4. Say what having two classes would cost, concretely.

### The dice drill

1. Write the `Dice` interface and both implementations.
2. Write the test for "a player at 97 rolls a 5".
3. Say why that test is impossible without the interface.
4. Name the three things a design must always let you replace.
5. Give the production reason, separate from the testing reason, for server-side rolls.

### The rules drill

1. Name the four rules that vary between households.
2. Say where each one lives.
3. Add "you must roll a six to start" and say which files change.
4. Say what cap you would put on consecutive extra turns, and why.

### The chained-jump drill

1. State the two possible answers to "a ladder lands you on a snake".
2. Write the loop for the chaining version.
3. Construct a two-jump board that loops for ever.
4. Write the validation that rejects it, and say when it runs.
5. Say why load-time validation beats a runtime guard, and why you would still keep the guard.

### The turn drill

1. Say the five steps of a turn in order.
2. Say where the win check goes and give the input that proves it.
3. Say what `play_turn` returns and why it does not print.
4. Name three callers that would use the same `Game` unchanged.
5. Say why `play_until_won` needs a turn cap.

### The numbers drill

Compute each, showing the multiplication:

1. Memory for one live game, and for 100,000 of them with a shared board.
2. What the figure would be if each game copied the board.
3. Turns per second at 100,000 games, 4 players and 8 seconds a turn.
4. Servers needed for the WebSocket connections at 50,000 per server.
5. Wall-clock length of a four-player game.

### The failure drill

For each, say what happens and what you would add:

1. Two actions arrive for the same game in the same millisecond.
2. A player's phone retries the same roll.
3. A player closes the app mid-game and comes back an hour later.
4. A configuration file is edited to add a jump from square 100.
5. Someone asks for ludo instead.
6. A player rolls sixes twenty times in a row.

Two of the six are not code problems. Say which, and what the actual fix is.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Why did you pop that element after the recursive call?*
   The invariant stated first, "not cleanup" said explicitly, the sibling-branch explanation, the
   counting rule for chooses against undoes, what you moved into the arguments, and the specific silent
   wrong answer that appears without it.

2. *Design snake and ladder for n players.*
   Snakes and ladders collapsed into one map in the first fifteen seconds, `Dice` as an interface with
   the testing reason and the anti-cheat reason, the varying rules as data, the turn in one sentence
   with the win check after the jump, and `TurnResult` returned rather than printed.

3. *What is the difference between backtracking and brute force?*
   One line — the validity check before the recursive call — plus the N-Queens numbers, and the sentence
   about why the undo is what makes that check affordable.

---

## Before you move on

- [ ] I can state the invariant in one sentence, without saying "cleanup".
- [ ] I can name the three kinds of state and give an example of the one that hides.
- [ ] I can count chooses against undoes before running anything.
- [ ] I know why anything passed as an argument needs no undo.
- [ ] I ran the version with the undo outside the loop and can explain the growing answers.
- [ ] I can say when an early return past the undo is safe and when it is a bug.
- [ ] I wrote both styles and can say where each one allocates.
- [ ] I know what happens if I mix the styles, and can quote the error.
- [ ] I can name the one line that makes it backtracking, and where it must go.
- [ ] I have the N-Queens pruning numbers for n = 6 and n = 8.
- [ ] I can say why every undo must be O(1).
- [ ] I can collapse snakes and ladders into one object in one sentence.
- [ ] I can write the `Dice` interface and the three-line test it enables.
- [ ] I can name the four varying rules and say where they live.
- [ ] I can construct a board that loops, and write the validation that rejects it.
- [ ] I can say where the win check goes and why.
- [ ] I can give the 110 MB figure for 100,000 games and say what makes it that small.
- [ ] I answered all three questions above out loud.
