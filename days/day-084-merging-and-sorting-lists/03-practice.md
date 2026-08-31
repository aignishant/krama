---
day: 84
track: practice
title: "Practice — Merging and sorting linked lists"
status: written
---

# Day 084 · Practice

**DSA topic:** Merging and sorting linked lists
**System design topic:** Design a deck of cards and a card game

---

## Code these, in this order

One rule for the whole set: **write the cut in the same keystroke as the split.** `second = slow.next`
and `slow.next = None` are one action, not two, and separating them is how this day's only fatal bug
gets in.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Merge Two Sorted Lists | LeetCode 21 (Easy) | The builder dummy, `<=` for stability, and attaching the remainder in one assignment. |
| 2 | Sort List | LeetCode 148 (Medium) | The first middle, the cut, and whether you can say why merge sort and not quicksort. |
| 3 | Merge k Sorted Lists | LeetCode 23 (Hard) | O(nk) versus O(n log k), the heap tie-breaker, and terminating the output. |
| 4 | Insertion Sort List | LeetCode 147 (Medium) | The O(n²) baseline, so you can say what merge sort bought you and at what n it matters. |

### On problem 1, delete the last line and see what happens

Replace `tail.next = a if a is not None else b` with a loop that moves the remainder node by node.
Confirm it still works. Then say, in one sentence, what the one-line version knows that the loop does
not.

### On problem 2, break the split twice on purpose

First use the second middle and run `[1, 2]`. Quote the error. Then restore the first middle, remove
the cut, and run `[1, 2, 3, 4]`. Quote that error too. They are the same error from two different
causes, and you should be able to tell them apart from the code alone.

### On problem 3, hit the TypeError

Write the heap version with `(node.value, node)` and no tie-breaker. Feed it two lists whose heads are
equal. Quote the exact error. Then fix it and say why the fix works.

### On problem 4, get the number

Time insertion sort and merge sort on 10,000 random nodes. Write both numbers down. Then say at what
size you would stop caring, and why an interviewer still asks for O(n log n) at n = 100.

---

### The merge drill

1. Say what the merge creates and what it copies.
2. Say what the dummy is for, in the builder sense.
3. Write the remainder line and say why one assignment is enough.
4. Say what `<=` buys over `<`, and construct an input where it is visible.
5. State the time and space, and say what the array version would need that this does not.

### The split drill

1. Write the first-middle loop and the cut.
2. Run the second-middle version on `[1, 2]` and describe the recursion.
3. Remove the cut and describe what the two "halves" actually are.
4. Say why both mistakes produce the same error message.
5. State the base case with both its conditions and say what each one covers.

### The why-merge-sort drill

Answer each in one sentence:

1. What does quicksort's partition need that a linked list does not have?
2. What does merging two arrays need that merging two lists does not?
3. Which sort is the array's worst case for space and the list's best?
4. Is your sort stable, and what one character decides it?
5. What is the recursion's space, and what would make it O(1)?

### The break-it drill

Trigger each and record the exact output or error text:

1. Split at the second middle. Run `[1, 2]`.
2. Omit the cut. Run `[1, 2, 3, 4]`.
3. Use `<` instead of `<=` and sort a list of records already ordered by a second key. Describe what
   moved.
4. Loop to attach the remainder instead of one assignment. Confirm it works, then say what it signals.
5. Heap merge with no tie-breaker, two equal heads. Quote the error.
6. Heap merge without `tail.next = None`. Print the result and describe the failure.
7. Base case with only `head is None`. Run a single-node list.

### The k-lists drill

1. Compute the cost of merging one at a time, for k lists of n/k nodes.
2. Compute it at k = 10,000 and n = 1,000,000.
3. Compute the O(n log k) cost for the same inputs and state the ratio.
4. Write the pairwise version and say why it needs no special case for an odd count.
5. Write the heap version and name its two traps.
6. Say which you would submit and why.

### The bottom-up drill

1. Describe the passes in one sentence.
2. Say how many passes there are for a million nodes.
3. State its time and space.
4. Write `_cut` and say exactly what it returns.
5. Say honestly what it costs you in code, and when you would write it.

### The composition drill

Write `sort` from scratch using only functions you already have, and then name, for each piece, the
day it came from:

1. The dummy in the merge.
2. The runner in the split.
3. The divide-and-conquer shape.
4. The stability argument.

---

### The value-object drill

1. Say why a card is a value object rather than an entity.
2. Name the three things `frozen=True` gives you, and which day introduced them.
3. Say why `Suit` and `Rank` are enums rather than strings.
4. Say why you would set `order=False`, and what bug that prevents.

### The no-value drill

1. Give the value of an ace in three different games.
2. Give the value of a king in two games where the answer differs in kind, not just in number.
3. Say what breaks the day you put `value` on `Card`.
4. Say what the return types of a blackjack evaluator and a poker evaluator are, and what that proves.
5. Name the day this same "who owns the rule" question was asked about something else.

### The shuffle drill

1. Write the naive shuffle.
2. Enumerate all 27 paths for three cards by hand or by code, and tabulate the six orderings.
3. State the counting argument for why uniformity is impossible.
4. Write Fisher–Yates and point at the one changed range.
5. Count its paths for three cards and say why that proves uniformity.
6. Say what Python function does this for you.

### The randomness drill

1. State 52! and roughly how many bits it takes to name one ordering.
2. State Mersenne Twister's state size and why that is not the problem.
3. Compute the fraction of shuffles reachable from a 32-bit seed.
4. Say what an adversary can do with 624 consecutive outputs.
5. Name the two Python facilities you would use instead, and one more reason to inject the RNG.

### The blackjack drill

1. Write the hand evaluator in the count-high-then-downgrade form.
2. Run it on `A A A A` and show the arithmetic.
3. Say why a per-card decision about an ace is impossible in principle.
4. Say what `soft` is and which rule needs it.
5. Say where the dealer's hit-or-stand rule lives, and why not on the evaluator.

### The shoe drill

1. Compute the cards in a six-deck shoe and the number dealt at 75 percent penetration.
2. Compute roughly how many rounds that is with four players.
3. State a counter's edge at full penetration and at three quarters.
4. Say what a continuous shuffling machine changes, and which class would become an interface.

### The extension drill

For each, say which classes change and how many:

1. Build poker instead of blackjack.
2. Add jokers.
3. Use a 32-card piquet deck.
4. Move to a real-money site.
5. Support a continuous shuffling machine.
6. Add an audit trail that can reproduce any past shuffle.

One of the six changes nothing but a function call. Name it, and say why that is the payoff for the
whole design.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Merge two sorted linked lists. Now sort an unsorted one.*
   What the merge does not do, the builder dummy, `<=` for stability, the remainder in one assignment,
   then split-sort-merge with both fatal split details, the quicksort comparison in two sentences, and
   the complexity with where the log comes from.

2. *Design a deck of cards. Now build blackjack on top of it.*
   Card as a frozen value object, the no-value decision with the ace in three games, the naive shuffle
   killed by the counting argument with the 27-over-6 numbers, Fisher–Yates and the one changed range,
   the seeding arithmetic if money is involved, and blackjack changing nothing but the evaluator.

3. *Why merge sort rather than quicksort, for a linked list?*
   No random access for the partition, and merging lists needs no scratch space where merging arrays
   does — so merge sort is the array's worst case for space and the list's best.

---

## Before you move on

- [ ] I write the cut in the same keystroke as the split.
- [ ] I can say what the merge creates and copies, and the answer is nothing.
- [ ] I can state what the one-line remainder attachment knows that a loop does not.
- [ ] I can name the character that makes the sort stable and construct a visible case.
- [ ] I broke the split both ways and can tell the two causes apart from the code.
- [ ] I can give the quicksort comparison in two sentences without hedging.
- [ ] I can say where the `log n` comes from and quote the level count at a million nodes.
- [ ] I computed O(nk) versus O(n log k) at k = 10,000 and quoted the ratio.
- [ ] I hit the heap `TypeError` on purpose and know the fix.
- [ ] I can describe bottom-up merge sort and say what it costs in code.
- [ ] I can say why a card is a value object and what `frozen=True` gives me.
- [ ] I can give the ace's value in three games and say what that proves.
- [ ] I enumerated the 27 paths and can quote 14.81 and 18.52 percent.
- [ ] I can state the counting argument for the bias in one sentence.
- [ ] I can compute the fraction of shuffles reachable from a 32-bit seed.
- [ ] I can score `A A A A` and explain why a per-card ace decision is impossible.
- [ ] I answered all three questions above out loud.
