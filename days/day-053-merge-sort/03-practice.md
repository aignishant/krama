---
day: 53
track: practice
title: "Practice — Merge sort"
status: written
---

# Day 053 · Practice

**DSA topic:** Merge sort
**System design topic:** Writing clean, testable classes

---

## Code these, in this order

One rule for the whole set: **write `merge` on its own and test it before you write anything that
calls it.** Every bug in merge sort is a bug in the merge.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Merge Sorted Array | LeetCode 88 (Easy) | The merge step alone — and whether you spot that it must run backwards. |
| 2 | Merge Two Sorted Lists | LeetCode 21 (Easy) | The same merge on linked data, where relinking replaces copying. |
| 3 | Sort an Array | LeetCode 912 (Medium) | Whether you can produce the whole sort, base case included, under a time limit. |
| 4 | Sort List | LeetCode 148 (Medium) | Why merge sort is *the* answer for linked lists — no random access needed, O(1) extra space. |

### On problem 1, write the forward version first and break it

Write the forward merge that copies into `nums1` from the front. Run it on
`nums1 = [1, 2, 3, 0, 0, 0]`, `nums2 = [2, 5, 6]` and watch it pass. Then run it on
`nums1 = [4, 5, 6, 0, 0, 0]`, `nums2 = [1, 2, 3]` and read the output: `[1, 2, 3, 1, 2, 3]`. Say out
loud what was destroyed and why merging backwards fixes it. This is the whole reason the problem
exists.

### On problem 2, notice what disappears

Merging two linked lists needs no output list at all — you relink the nodes you already have. Say out
loud what the extra space is now (`O(1)`), and why the array version cannot do the same thing.

### On problem 3, get the base case right on purpose

Write it with `if len(nums) == 1` first. Run it on `[]`. Paste the `RecursionError`. Then fix it to
`<= 1` and say the general rule: the base case must cover every input that cannot shrink further.

Then submit the recursive version and the bottom-up version, and compare the runtimes. They are the
same complexity; note which is faster in Python and guess why before you look it up.

### On problem 4, connect it to yesterday

Sort List is where merge sort stops being an exercise. Say out loud, before coding, why quicksort is
the wrong choice here (no random access, so choosing and reaching a pivot is `O(n)` each time) and
why merge sort is right.

### The merge drill

Write `merge` from memory, then check each of these by running it:

1. `merge([1, 3, 5], [2, 4, 6])`
2. `merge([1, 2, 3], [])` — does your version keep the leftovers?
3. `merge([], [])`
4. `merge([5], [1])`
5. `merge([1, 1, 1], [1, 1])` — how many comparisons, and which side wins each tie?

Then add one assertion to your merge — `assert len(out) == len(left) + len(right)` — and say which of
the five cases it would have caught if you had forgotten the `extend` lines.

### The trace drill

Without running anything, write out every level of the split and every merge for
`[38, 27, 43, 3, 9, 82, 10]`. Then count:

1. How many levels?
2. How many values are merged at each level?
3. How many comparisons in total, at most?
4. What is the deepest the recursion goes?
5. How much extra memory exists at the widest moment?

### The complexity drill

Answer out loud, in under fifteen seconds each:

1. Why is merge sort `O(n log n)`? Give the two facts and multiply them.
2. Why is binary search `O(log n)` and not `O(n log n)`, when both halve?
3. What is merge sort's best case? Why is that answer unusual?
4. What is the extra space, and which half do you have to copy?
5. At `n = 100,000`, how many operations for insertion sort and for merge sort?

### The break-it drill

Introduce each bug, run it, and read what happens:

1. `len(nums) / 2` instead of `//`. Paste the error.
2. `if len(nums) == 1` instead of `<= 1`, called on `[]`. Paste the error.
3. Delete both `extend` lines. Run `merge([1, 2, 9], [3, 4])` and say what is missing.
4. Change `<=` to `<` in the merge. Sort `[("b", 1), ("a", 2), ("c", 1)]` by the number and say what
   moved.
5. Split as `nums[:middle]` and `nums[middle - 1:]`. Predict the failure before you run it.

### The follow-up drill

Count inversions — the number of pairs `(i, j)` with `i < j` and `nums[i] > nums[j]`:

1. Write the `O(n²)` double loop first. Check it on `[2, 4, 1, 3, 5]` (the answer is 3).
2. Now add the counting to your merge. The line is `crossing += len(left) - i`, and you should be
   able to say *why* that is the right number before you write it.
3. Check both versions agree on ten random lists.
4. Say what the answer is for a reversed list of `n` elements, and why.

### The testability drill

Take this class and make it testable, then write the two tests:

```python
class ReminderService:
    def __init__(self) -> None:
        self.db = PostgresConnection(os.environ["DATABASE_URL"])
        self.sms = TwilioClient(os.environ["TWILIO_KEY"])

    def send_due_reminders(self) -> int:
        due = self.db.query("SELECT * FROM reminders WHERE due_on <= %s", date.today())
        for row in due:
            self.sms.send(row["phone"], row["message"])
        return len(due)
```

1. Name every dependency, and say which are hidden.
2. Rewrite the constructor. Say what type each parameter has and why it is a `Protocol` rather than a
   concrete class.
3. Write the in-memory fake repository. Fifteen lines, no more.
4. Write the recording double for the SMS client, and say why it is a mock rather than a fake.
5. Deal with `date.today()`. Say whether you inject it per call or per object, and why.
6. Write the test for "a reminder due tomorrow is not sent today".
7. Write the test for "if the SMS client raises, the remaining reminders are still attempted" — or
   argue that they should not be, and test that instead.
8. Write the composition root, and give the `grep` command that proves the driver is swappable.

### The vocabulary drill

Define each in one sentence, then give an example from the `ReminderService` above:

1. Dependency injection — and whether it needs a framework.
2. Seam.
3. Dummy, stub, fake, mock — all four, and which you would use for the SMS client.
4. Composition root.
5. Contract test — and why a fake needs one.
6. The test pyramid — with the rough counts and times at each layer.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Write merge sort. Why is it O(n log n)?*
   The merge first, the two `extend` lines and the `<=` explained, then the two facts — n per level,
   log n levels — and why "it halves" is not the answer on its own.

2. *How would you unit test this class?*
   Name the blocker, change the constructor, name the doubles precisely, and give the reachability
   argument rather than the speed one. Then concede what still needs a real database.

3. *Merge sort or quicksort?*
   The guarantee, stability, memory, and the three situations where merge sort is the only answer —
   adversarial input, multi-key sorting, and data that does not fit in memory.

---

## Before you move on

- [ ] I wrote `merge` from memory and it handles empty lists and leftovers correctly.
- [ ] I broke LeetCode 88 with the forward merge and can say exactly which value got destroyed.
- [ ] I can give the two facts behind `O(n log n)` and say why binary search is different.
- [ ] I triggered the `RecursionError` from `== 1` and can state the general base-case rule.
- [ ] I can say where the `O(n)` extra space goes, and which half does not need copying.
- [ ] I made `ReminderService` testable and wrote both tests without a database running.
- [ ] I can name all four test doubles and say when a mock is the right choice.
- [ ] I answered all three questions above out loud.
