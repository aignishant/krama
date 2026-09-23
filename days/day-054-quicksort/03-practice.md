---
day: 54
track: practice
title: "Practice — Quicksort and partitioning"
status: written
---

# Day 054 · Practice

**DSA topic:** Quicksort and partitioning
**System design topic:** Object-oriented design revision and interview questions

---

## Code these, in this order

One rule for the whole set: **write `partition` on its own and check the returned position before you
write the sort.** Every quicksort bug is a partition bug or a recursion-bounds bug.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Sort Colors | LeetCode 75 (Medium) | A three-way partition with the pivot value fixed at 1 — the Dutch flag, in its purest form. |
| 2 | Partition Array According to Given Pivot | LeetCode 2161 (Medium) | Three-way partitioning where *stability* is required, so the in-place swap version is wrong. |
| 3 | Sort an Array | LeetCode 912 (Medium) | Whether your quicksort survives sorted input and 50,000 duplicates. |
| 4 | Wiggle Sort II | LeetCode 324 (Medium) | Partitioning as a tool rather than a sort — find the median, then place around it. |

### On problem 1, write it as a partition, not as counting

The counting solution (count the 0s, 1s and 2s, then overwrite) is two passes and it is fine. Write
it, then write the one-pass three-region version, and say out loud which region each of `low`, `i`
and `high` bounds. Then answer: why does `i` not advance when you swap with `high`?

### On problem 2, discover why stability matters

Solve it with the in-place three-way swap first and check it against the expected output. It fails,
and the reason is that the problem requires the original relative order to be preserved inside each
group. Say out loud which of the sorts you know are stable, and why partitioning cannot be.

### On problem 3, break it deliberately, then fix it

1. Submit quicksort with a last-element pivot. Note the verdict on the sorted-input test case.
2. Add the two lines of random pivot selection. Submit again.
3. Now build a list of 50,000 identical values locally and run your version on it. If you used `<=`
   in the partition, paste the `RecursionError`.
4. Switch to the three-way partition and run the same input. Say the before-and-after operation
   counts.

### On problem 4, use the partition without sorting

Wiggle Sort II needs the median, and the median comes from quickselect — tomorrow's topic, built on
today's partition. Solve it with `sorted()` first to get the placement rule right, then say out loud
what you would replace the sort with and what the complexity becomes.

### The partition drill

Write `partition` from memory, then verify by hand:

1. `partition([7, 2, 9, 4, 1, 8, 3], 0, 6)` — what does it return, and what is the list afterwards?
2. `partition([1, 2, 3], 0, 2)` — where does the pivot land, and what does that mean for the
   recursion?
3. `partition([3, 2, 1], 0, 2)` — the same question in reverse.
4. `partition([5, 5, 5, 5], 0, 3)` — with `<` and then with `<=`. Compare the returned positions.
5. `partition([2], 0, 0)` — does it terminate?

For each, state the invariant that holds at the moment the loop ends.

### The worst-case drill

Run the comparison counter from §5 of the lesson and record the numbers:

1. 500 sorted values, first-element pivot.
2. 500 sorted values, random pivot.
3. 500 reversed values, first-element pivot.
4. 500 reversed values, median-of-three pivot.
5. 500 identical values, two-way partition with `<`.
6. 500 identical values, three-way partition.

Then say, without looking: which input is the surprising one, and why is it surprising?

### The break-it drill

Introduce each bug, run it, and read the failure:

1. `quicksort(nums, lo, p)` instead of `p - 1`. Paste the error and say which pivot placement causes
   it.
2. `<=` instead of `<` in the partition, on a list of 3,000 equal values. Paste the error.
3. Last-element pivot on `list(range(5000))`. Paste the error and say why an already sorted list is
   the worst case.
4. Use Hoare's partition but recurse with `p - 1` and `p + 1`. Find an input where the output is
   wrong.
5. In the three-way partition, advance `i` after swapping with `gt`. Find the input that breaks it.

### The complexity drill

Answer out loud, in under fifteen seconds each:

1. What is quicksort's worst case, and what input causes it?
2. Why does randomising the pivot fix it? What exactly does it change?
3. What is the expected number of comparisons, and how does that compare with merge sort's?
4. Why is quicksort faster in practice despite doing *more* comparisons?
5. What is the extra space, and what is the recursion depth — with and without the smaller-side
   trick?
6. Name the three pivot strategies and one weakness of each.

### The design drill

Set a timer for twenty minutes and run the five moves out loud on this prompt:

> *Design the classes for a cinema ticket booking system. A chain has several cinemas; each cinema
> has several screens; each screen shows several shows a day; each show has seats of two classes.
> Users search by film and city, pick seats, pay, and can cancel up to two hours before the show for
> a partial refund. Prices vary by day of week and seat class.*

1. **Minutes 0-5** — four clarifying questions and the assumptions you will proceed on. Name what you
   are leaving out.
2. **Minutes 5-10** — the nouns, one sentence each. Then the noun that is *not* in the paragraph, and
   what has nowhere to live without it.
3. **Minutes 10-15** — the class diagram, with a multiplicity on every line.
4. **Minutes 15-20** — the one flow that matters, coded: seat selection and payment.

Then answer the three questions you know are coming:

- *Two users select the same seat at the same instant. What happens?*
- *Where did you put an interface, and where did you deliberately not?*
- *Now add a "book the whole row" feature.*

### The missing-noun drill

For each prompt, name the class that is not in the sentence, and say what has nowhere to live without
it:

1. "A guest books a room."
2. "A user picks seats for a show."
3. "A car parks in a spot and pays on exit."
4. "A member borrows a book."
5. "A rider requests a ride to a destination."
6. "A customer orders food from a restaurant."

### The race-condition drill

For each, name the check-then-write gap, say what two users see when it goes wrong, and give the
atomic fix as a single operation:

1. The last hotel room.
2. The last cinema seat.
3. The last parking spot.
4. Two withdrawals from the same account balance.
5. Two users claiming the same username.
6. A stock counter reaching zero during a flash sale.

### The interface-justification drill

For each, say whether you would create an interface, and name the second implementation — or say
plainly that you cannot:

1. Pricing in a hotel booking system.
2. `IHotel`.
3. The cancellation policy.
4. The payment gateway.
5. `IRoom`.
6. The booking repository.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Write quicksort. What is its worst case, and when does it happen?*
   The partition with its invariant, the excluded pivot in the recursion, `O(n²)` on **sorted** input
   with a fixed pivot, and the two lines that fix it — plus what randomising actually changes.

2. *Design the classes for a hotel booking system.*
   The five moves on a clock, the missing noun, the two justified interfaces, and the
   check-then-write race named before you are asked.

3. *Quicksort or merge sort?*
   In place and fast against guaranteed and stable, with the numbers — and the three situations where
   merge sort is the only answer.

---

## Before you move on

- [ ] I wrote `partition` from memory and can state its invariant at the moment the loop ends.
- [ ] I crashed quicksort on an already sorted list and can explain why that input is the worst case.
- [ ] I crashed it again on 3,000 equal values with `<=` and can say what the one character changed.
- [ ] I can give the three pivot strategies and one weakness of each, unprompted.
- [ ] I ran the twenty-minute cinema design out loud, including the missing noun and the race.
- [ ] I can name the check-then-write gap in six different prompts and give the atomic fix for each.
- [ ] I can say which interfaces I would create and name the second implementation for each.
- [ ] I answered all three questions above out loud.
