---
day: 15
track: practice
title: "Practice — Moving elements: zeros, duplicates, and the write pointer"
status: written
---

# Day 015 · Practice

**DSA topic:** Moving elements: zeros, duplicates, and the write pointer
**System design topic:** What an API is

---

## Code these, in this order

Four problems that are the same five lines with a different `if`. Do them in order and the fourth
one will feel like a variation rather than a new problem. That is the point of doing them in
order.

Before each one, say out loud:

1. What am I keeping, and what am I throwing away?
2. Does the order of the survivors have to be preserved?
3. Am I filling the tail, or returning a count?
4. What does the write index equal when the loop ends?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Remove Element | LeetCode 27 (Easy) | The bare pattern, and whether you understand that **nothing is deleted** — you return a count and the grader ignores everything past it. |
| 2 | Move Zeroes | LeetCode 283 (Easy) | The same loop plus the second phase. The trap is stopping after the first loop and leaving the stale tail behind. |
| 3 | Remove Duplicates from Sorted Array | LeetCode 26 (Easy) | Comparing against `items[write - 1]` — what you *kept* — rather than `items[read - 1]`. Also the empty-input guard, since `write` starts at 1. |
| 4 | Remove Duplicates from Sorted Array II | LeetCode 80 (Medium) | `items[write - 2]`. If you built the habit in problem 3 this is a one-character change; if you compared against `read - 1` it is a rewrite. |

### On problem 1, do it twice

Write the order-preserving version first — the plain write pointer. Then write the version that
does **not** preserve order: swap the unwanted element with the last one and shrink the range,
without advancing the read index.

Then answer, out loud: on `[3, 2, 2, 3]` with target `3`, how many writes does each version do?
And on an array of a million elements with exactly two matches?

That second answer is why the non-order-preserving version exists.

### On problem 2, run the broken versions first

Type these in and predict the output of each before you run it. Being wrong here is the exercise.

```python
items = [0, 0, 1]
for x in items:
    if x == 0:
        items.remove(x)
print(items)
```

```python
nums = [1, 0, 0, 0]
for i in range(len(nums)):
    if nums[i] == 0:
        del nums[i]
print(nums)
```

```python
def move_zeroes(items):
    write = 0
    for read in range(len(items)):
        if items[read] != 0:
            items[write] = items[read]
            write += 1
    return items

print(move_zeroes([0, 1, 0, 3, 12]))
```

Then, in one sentence each: which one gives a wrong answer silently, which one crashes, and which
one is right in front and wrong at the back. The first is the dangerous one, and you should be
able to say why.

### On problems 3 and 4, generalise before you move on

Once problem 4 passes, replace the `2` with a parameter `k` and check it still passes for `k = 2`.
Then test it with `k = 1` and confirm it solves problem 3. One function, both problems — that is
the sign you have understood the pattern rather than memorised two of them.

### The tracing drill

Take `[0, 1, 0, 3, 12]` and, without running anything, say out loud the value of `read`, `write`
and the whole list after every single turn of the loop. Five turns. Then run it with a `print`
inside the loop and check yourself.

Do the same for `[1, 2, 3]` — where `write` and `read` never separate — and for `[0, 0, 0]`, where
they separate immediately and the first loop keeps nothing.

### The stretch problem

**Sort Colors** — LeetCode 75 (Medium). Three values, 0, 1 and 2, to be sorted in one pass. It is
the write pointer with *two* write indices, one coming from each end, and it is the classic next
step from today. Try it before you look anything up; you have everything you need.

### The API drill

Pick a real API and answer these five questions about it without opening the documentation. Use
GitHub's if you have no other — it needs no sign-up for public data.

1. What is one operation it offers, written out as a method and a path?
2. What must you send with the request, and where does it go — path, query string, headers, body?
3. What comes back on success, and what fields does it have?
4. What comes back when you get it wrong, and what when they are broken?
5. Where is the version, and what would happen to your code if they changed the meaning of an
   existing field?

Then do the thing that makes it real: make the call. In a terminal,
`curl https://api.github.com/users/torvalds` costs nothing and returns a JSON body you can read.
Look at the response headers too — `x-ratelimit-remaining` is right there, and it makes the rate
limit stop being an abstract idea.

### The explain-it-twice drill

Explain what an API is **twice**, out loud, timed.

- **Sixty seconds, to a non-engineer.** No status codes, no JSON, no HTTP. If they could not
  repeat it back, it did not work.
- **Sixty seconds, to an engineer.** Method, path, headers, body, status code, response shape,
  versioning, and one named example with a real path.

Most candidates can do neither cleanly on the first attempt. It is the same fact twice, and being
able to switch registers on demand is exactly what the question is checking.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Move all zeros to the end while keeping the order of the other elements.*
   Ask the two contract questions first — in place, and order preserved. Then name the two indices
   and state the rule that `write` never overtakes `read`. Write the loop, then the tail fill, then
   give `O(n)` time and `O(1)` extra space. Finish by saying why you are not deleting as you go.

2. *What is an API? Give me an example of one you have used.*
   One plain sentence, then a concrete path with a real host in it, then the reason it matters —
   either side can change behind the contract — then the price, which is that you cannot change
   what it means once people depend on it. Sixty seconds, then stop talking.

3. *This array is sorted. Remove the duplicates in place and return the new length. Now allow each
   value at most twice.*
   The point is the second half. Say why `items[write - 1]` becomes `items[write - 2]`, why the
   first two elements pass unconditionally, and why comparing against `read - 1` instead would
   have made this a rewrite rather than a one-character change.

---

## Before you move on

- [ ] I ask "in place?" and "order preserved?" before writing a line of this family.
- [ ] I can state the rule — `write <= read`, so overwriting is always safe — in one sentence.
- [ ] I always test the **whole** output list, not just the front of it.
- [ ] I never delete from a list while looping over it, and I can show what breaks.
- [ ] I can define an API in one plain sentence, with a real method and path as the example.
- [ ] I can say what an API costs you, not only what it buys you.
- [ ] I can redraw today's request-and-response diagram from memory, in whatever tool I like.
