---
day: 93
track: practice
title: "Practice — Combinations and combination sum"
status: written
---

# Day 093 · Practice

**DSA topic:** Combinations and combination sum
**System design topic:** Design a file system

---

## Code these, in this order

One rule for the whole set: **before you type the recursive call, say out loud whether the same value
may be used again.** `i` if yes, `i + 1` if no. That one character is the difference between two
LeetCode problems, and it fails silently.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Combinations | LeetCode 77 (Medium) | The `start` index, and the size prune that is a `break`. |
| 2 | Combination Sum | LeetCode 39 (Medium) | `build(i, …)` for reuse, and the sorted `break` on too-big. |
| 3 | Combination Sum III | LeetCode 216 (Medium) | Two constraints at once: a fixed size *and* a target. |
| 4 | Combination Sum II | LeetCode 40 (Medium) | Two skips, two keywords — `break` for too big, `continue` for duplicate. |

### On problem 1, measure the prune

Write it without the "not enough elements left" check, then with it. Count the calls both ways for
choosing 18 from 20 and record both numbers. Then say why the check is a `break` and not a `continue`.

### On problem 2, change one character and run it again

Run it correctly, then change `build(i, …)` to `build(i + 1, …)` and run `[2,3,6,7]` with target 7.
Record both outputs. Then remove the `sort()` and run `[7,2,6,3]` with target 7, and say which answer
disappeared and why the `break` caused it.

### On problem 3, name both prunes

There is a target prune and a size prune. Write both, and say which one is a `break` and which one a
`return`.

### On problem 4, swap the two keywords deliberately

Run `[1,1,2,5,6,7,10]` with target 8 correctly — four answers. Then change the duplicate `continue` to
a `break` and record what you get. Then change the too-big `break` to a `continue` and say what changed
in the output versus what changed in the running time.

---

### The definition drill

1. Say the difference between a combination and a permutation in one sentence.
2. Say what `start` guarantees about the order every answer is generated in.
3. Say why that guarantee means you never have to de-duplicate the result.
4. Say what `set()` on a list of lists does, and quote the error.

### The sort drill

1. Give the reason for sorting that is *not* about tidy output.
2. Run `combination_sum([7,2,6,3], 7)` unsorted, with the break. Record the output.
3. Say which answer was lost and at which step.
4. Name the second thing in this lesson that also requires the sort.

### The one-character drill

1. Say which problem uses `build(i, …)` and which uses `build(i + 1, …)`, and why.
2. Run `combination_sum([2,3], 6)` and `combination_sum_ii([2,3], 6)`. Explain both outputs.
3. Use `i` in a version where elements may only be used once, on `[1,1,2]` with target 2, and describe
   what is wrong with the answer.
4. Say what happens to that version if a candidate is `1` and the target is large.

### The two-keywords drill

1. Write the too-big check and say why it is a `break`.
2. Write the duplicate check and say why it is a `continue`.
3. Say what "monotone" means here, and use it to decide which keyword any new prune should get.
4. Swap them both and record the two different kinds of damage.

### The duplicate-rule drill

1. Write the Combination Sum II skip from memory.
2. Say what `i > start` means about position in the tree.
3. Change it to `i > 0`, run `[1,1,6]` with target 8, and say which box disappears.
4. State the permutations version of this rule, and say in one sentence why the two differ.
5. Name the three problems so far where this rule has appeared in a different outfit.

### The termination drill

1. Name the measure that decreases in combination sum, and say why it must.
2. Put a `0` in the candidates and run it. Quote the error.
3. Say why every LeetCode statement guarantees positive candidates.
4. Run `combination_sum([1,2,5], 5000)` and quote the error.
5. Say what makes this problem's depth different from every other one in the phase.

### The cost drill

1. State the number of answers for choose-k, and the worst `k` for a given `n`.
2. Compute `C(20,10)`, `C(30,15)` and `C(40,20)`.
3. State the depth and branching factor for combination sum, and give the loose bound.
4. Say honestly what the real cost tracks, and why the bound is loose.
5. State the extra space and say what it depends on.

### The counting drill

1. Write the counting version with a one-dimensional array.
2. Say what `ways[0] = 1` means.
3. Say which loop must be on the outside to count combinations rather than orderings.
4. Compare the step count against enumerating, for `[1,2,5]` and target 500.
5. Say what word in a question should make you switch to this immediately.

---

### The model drill

1. Name the three classes and say which one is abstract.
2. Say why `Directory` holding `Entry` — rather than holding `File` and `Directory` separately — is the
   whole design.
3. Write `size()` for both concrete classes.
4. Say what code you avoid writing by having the shared type, and name a change it makes cheap.

### The resolve drill

1. Write `_split` and say what it does with `"/"`.
2. Write `_resolve` and name the four possible outcomes of a walk.
3. Say which outcome is not an error for `mkdir`.
4. Say what `ls` returns when the path names a file, and why.
5. Say how many lookups resolving `/a/b/c/d/e` costs.

### The dict-versus-list drill

1. State the lookup cost of each.
2. Compute the resolve time for a five-part path with 100,000 children per directory, both ways.
3. Say what the dict costs you, and on which operation.
4. Say which operation is hot and which is rare, and use that to justify the choice.
5. Name the real file system that made the same decision and what it uses on disk.

### The content drill

1. Say why file content is a list of chunks rather than one string.
2. Compute the total bytes copied by 10,000 appends of 100 bytes into one string.
3. Say when you would prefer the single string instead.
4. Say where the join happens and why it is lazy.

### The numbers drill

Compute each, showing the multiplication:

1. Metadata memory for a million files across fifty thousand directories.
2. `ls` cost on a directory of 100,000 children.
3. `du` cost on a subtree of a million entries.
4. `find` cost with and without a name→paths map, and the memory that map costs.
5. Say which real system's bottleneck is exactly number 1, and why.

### The failure drill

For each, say what happens and what you would add:

1. Two threads call `mkdir("/a/b")` at the same instant.
2. A thread reads a file while another appends to it.
3. `ls` is called on a directory with a million files.
4. Someone asks to rename a directory containing a million files — here, and in S3.
5. `addContentToFile` is called with a path whose parent is a file.
6. The process restarts.

Two of the six are not solvable inside this design as drawn. Name them and say what you would build.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find all combinations that sum to the target.*
   The definition of combination first, the `start` index and what it guarantees, the sort with the
   reason that is about the `break`, the one character that allows reuse, why it terminates, and an
   honest complexity with the depth-is-target caveat.

2. *Design an in-memory file system.*
   The shared `Entry` type and what it buys, "resolve then act" as the shape of every method, the dict
   with the 5 ms versus 250 ns number, `ls` on a file returning its own name, and the S3 contrast about
   renaming.

3. *Now each number may be used only once, and the input has duplicates.*
   `i + 1`, sort, and `i > start` — then the part that separates people: two skips in one loop with two
   different keywords, and what each wrong keyword costs.

---

## Before you move on

- [ ] I can define combination against permutation in one sentence.
- [ ] I can say what the `start` index guarantees about generation order.
- [ ] I can give the reason for sorting that is about the `break`.
- [ ] I ran the unsorted version and know which answer it loses.
- [ ] I can say which of `i` and `i + 1` allows reuse, without hesitating.
- [ ] I can write both skips in Combination Sum II with the right keyword each.
- [ ] I swapped the keywords and recorded both kinds of damage.
- [ ] I can state the duplicate rule in all three outfits and say which tree each belongs to.
- [ ] I can name the measure that terminates combination sum, and what a `0` candidate does.
- [ ] I can say why the depth here is not bounded by `n`, and quote the error it causes.
- [ ] I can write the counting version and say which loop goes on the outside.
- [ ] I can name the three file system classes and write `size()` for both concrete ones.
- [ ] I can say what "resolve then act" means and name the four outcomes of a walk.
- [ ] I can justify the dict with the 5 ms versus 250 ns numbers.
- [ ] I can say what `ls` returns for a file path.
- [ ] I can state the metadata memory for a million files and name the system it limits.
- [ ] I can explain the S3 renaming contrast in two sentences.
- [ ] I answered all three questions above out loud.
