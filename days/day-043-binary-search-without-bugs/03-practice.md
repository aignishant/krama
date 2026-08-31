---
day: 43
track: practice
title: "Practice — Writing binary search without off-by-one bugs"
status: written
---

# Day 043 · Practice

**DSA topic:** Writing binary search without off-by-one bugs
**System design topic:** Why interviews ask object-oriented design at all

---

## Code these, in this order

One rule today, and it is strict: **solve all four with the same six-line template.** If you find
yourself writing `- 1` anywhere, you have slipped back to yesterday's convention — stop and restart
the function.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Search Insert Position | LeetCode 35 (Easy) | The lower bound with nothing added — and that "one past the end" is a real answer. |
| 2 | First Bad Version | LeetCode 278 (Easy) | The template with no array at all; the question is an API call. |
| 3 | Find Smallest Letter Greater Than Target | LeetCode 744 (Easy) | The upper bound, plus a wrap-around that the template does not solve for you. |
| 4 | Find First and Last Position of Element in Sorted Array | LeetCode 34 (Medium) | Both bounds, and whether you resist the find-then-walk shortcut. |

### On problem 1, write the invariant as a comment first

Literally type the sentence — *below lo all False, from hi up all True* — as the first line of the
function, then write the six lines under it. Delete the comment afterwards if you like. Doing this
five times is what makes the template automatic.

### On problem 2, notice what changed and what did not

Nothing about the loop changes. The question becomes `isBadVersion(mid)`, the range becomes `1` to
`n + 1`, and the answer is still "the first True". Use `lo + (hi - lo) // 2` here — n reaches
2³¹ − 1 and this problem exists partly to make that point. Then say out loud what the cost is in
*calls*, not comparisons: `log₂(2³¹) = 31` calls to the API.

### On problem 3, the template gives you most of it

The upper bound over the letters gives the first letter strictly greater than the target. It returns
`len(letters)` when there is none — and this problem wants a wrap to `letters[0]` in that case. Write
the wrap as a separate line after the search, not as a special case inside the loop. Keeping the
template pure and handling the problem's quirk outside it is the habit worth building.

### On problem 4, do two searches, not one search and a walk

The tempting version finds any match and walks outward. Build the array `[8] * 200000` with target 8
and time both. The walk is O(n) and the two bounds stay at eighteen comparisons each. Then say the
answer for the empty case: both bounds are equal, and `[-1, -1]` falls out of `lo == hi` without a
separate branch.

### The convention drill

For each line below, say which convention it belongs to — closed `[lo, hi]` or half-open `[lo, hi)` —
and what happens if you use it in the other one:

1. `hi = len(nums)`
2. `while lo <= hi`
3. `hi = mid`
4. `hi = mid - 1`
5. `return lo`
6. `return -1`

Then say the one-sentence rule that generates all six.

### The termination drill

Answer out loud, in under a minute: why does `hi = mid` never hang in the half-open template, and why
*does* it hang in the closed one? The answer is a single inequality about `mid` and `hi`. If you
cannot produce it, re-read §6 — this is the question interviewers use to separate people who
memorised the template from people who own it.

### The one-character drill

Starting from your working `lower_bound`, produce each of these by changing one character or adding
one line, and say the answer before you run it on `[2, 4, 4, 4, 7, 9]`:

1. First index with value `> 4`.
2. Last index holding 4.
3. How many 4s there are.
4. Whether 5 is present.
5. Where 5 would be inserted.

### The OOD round drill

Set a timer for four minutes and speak, out loud, the opening of a *design a vending machine* round:

1. The plan sentence — how you will spend the forty-five minutes.
2. Four clarifying questions that would actually change the model.
3. The scope you are taking and the scope you are dropping, said explicitly.
4. Six to eight class names, each with the one thing it is responsible for.
5. The one interface you would introduce, and the second implementation that justifies it.

Then answer the extension you know is coming — *"now it accepts card payments as well as coins"* —
in terms of files added versus existing methods edited. If your answer edits more than one existing
method, the seams are in the wrong place; move them and say the new answer.

### The wrong-round drill

For each sentence, say which round it belongs to — DSA, OOD, or HLD — and what the right sentence
for an OOD round would be instead:

1. "I'd shard by user id."
2. "That's O(n log n) because of the sort."
3. "`orders` would have a foreign key to `customers`."
4. "I'd put a Redis cache in front of it."
5. "I'll use a Singleton for the inventory."

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Write binary search on the whiteboard. No compiler.*
   Convention first, then the invariant, then the six lines, then what the return value means and
   what a caller must check before using it.

2. *Design a class structure for this feature.*
   The plan sentence, the four clarifying questions, the scope you keep and drop, and the rule for
   where behaviour lives. Do not name a pattern.

3. *Your binary search loop hangs. Talk me through why.*
   The `mid < hi` inequality, the two conventions, and the exact pairing that breaks — `hi = mid`
   inside a `while lo <= hi` loop.

---

## Before you move on

- [ ] I solved all four problems with one template and wrote `- 1` nowhere.
- [ ] I can state the half-open invariant and say which line preserves it.
- [ ] I can explain termination with the `mid < hi` inequality, unprompted.
- [ ] I produced all five one-character variants without re-deriving the loop.
- [ ] I ran the four-minute vending machine opening, including the scope I dropped.
- [ ] I can sort the five wrong-round sentences and give the OOD replacement for each.
- [ ] I answered all three questions above out loud.
