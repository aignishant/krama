---
day: 53
track: practice
title: "Practice — Merge sort"
status: written
---

# Day 053 · Practice

**DSA topic:** Merge sort
**System design topic:** Writing clean, testable classes

**Theme:** Databases I: SQLite

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

## Build these, in all three languages

*Three exercises, easiest first. Each one says what it is really testing. Every
exercise is done three times: once in Python, once in Go, once in C++.*

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | The attack, side by side | Whether you can demonstrate injection and its cure on the same file with the same input. |
| 2 | Safe to run twice | Handling the constraint failure, and reading a "not found" without treating it as a crash. |
| 3 | The rollback test | Proving the transaction undoes the first update when the second fails, in the language where you wrote the undo yourself. |

All three start from the lesson's program and the `users.db` it creates. Delete the file
between runs when an exercise says to start clean.

### 1. The attack, side by side

Write `find_unsafe(name)` next to the lesson's `find_by_name`, building the SQL text with an
f-string, `Sprintf`, or `+`. Run both with `Meera`, then both with `x' OR '1'='1`, and paste the
four results into a comment. Then try `x'; DROP TABLE users; --` against the unsafe version and
paste what happened in each language, including whichever driver refused to run two statements
and whichever did not. Delete `find_unsafe` afterwards. Done means the four results and the
DROP outcome pasted, per language, and no unsafe function left in the file.

### 2. Safe to run twice

Make the program idempotent: a second run must print the same six lines as the first, not a
`UNIQUE constraint failed`. Do it by looking up each user by name first and inserting only if
absent, which means handling "not found" correctly: `None`, `sql.ErrNoRows`, `step()` returning
`false`. Then, in Go, delete `defer rows.Close()` from `listUsers`, call it two hundred times in
a loop, and paste what happens; put it back. Done means two consecutive runs with identical
output in all three, and the Go leak observed.

### 3. The rollback test

Write a test, in whatever form each language makes easy, that calls `transfer` with an amount
larger than the balance, catches the refusal, and then reads both balances and asserts neither
changed. Then break the transaction on purpose, remove `with conn:`, the `defer tx.Rollback()`,
or the `Transaction` object, and run the test again; it must fail, with the first balance
reduced. In C++, also throw from between the two updates with the `Transaction` in place and
show the balances unchanged. Done means the test passes with the transaction and fails without
it, in all three languages, and the outputs are pasted.

## Say these out loud

### DSA and system design

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

### Languages

*Three questions from today. Answer each in two minutes, standing up, no notes.*

1. What is SQL injection, and how do parameters stop it?
   The one-sentence attack with the `OR '1'='1` example, the two-channel explanation, why it
   is a complete defence and escaping is not, and the one thing a parameter cannot be.
2. What is a transaction, and how does each language make it exception-safe?
   All or nothing, the transfer example, and then `with conn:`, `defer tx.Rollback()`, and the
   `Transaction` destructor; what happens to a half-done transfer if you forget each one.
3. What does `database is locked` mean, and what would you do about it?
   One writer at a time, the pool or the second process holding a transaction, the Go
   `rows.Close` leak, and the point at which the answer is Postgres.

## Before you move on

- [ ] I wrote `merge` from memory and it handles empty lists and leftovers correctly.
- [ ] I broke LeetCode 88 with the forward merge and can say exactly which value got destroyed.
- [ ] I can give the two facts behind `O(n log n)` and say why binary search is different.
- [ ] I triggered the `RecursionError` from `== 1` and can state the general base-case rule.
- [ ] I can say where the `O(n)` extra space goes, and which half does not need copying.
- [ ] I made `ReminderService` testable and wrote both tests without a database running.
- [ ] I can name all four test doubles and say when a mock is the right choice.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] The three lesson programs print the six lines, and `parameterised` finds nobody for the long name in all three.
- [ ] Exercise 1 shows every row from the unsafe version and none from the safe one, with the DROP outcome per language.
- [ ] Exercise 2 runs twice with identical output in all three, and I saw what the missing `rows.Close()` does.
- [ ] Exercise 3's test passes with the transaction and fails without it in all three languages.
- [ ] I can say the two-channel explanation of parameters in two sentences, and name the one thing they cannot bind.
- [ ] I can say which C API call each C++ wrapper's destructor makes, and why the deleter is on a `unique_ptr`.
