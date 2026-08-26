---
day: 7
track: practice
title: "Practice — Space complexity, and what in-place really means"
status: written
---

# Day 007 · Practice

**DSA topic:** Space complexity, and what in-place really means
**System design topic:** What a web server actually does

---

## Code these, in this order

Four problems that each have an easy `O(n)`-space solution and a harder `O(1)`-space one.
Write **both** versions of every one of them. The second version is the exercise.

For each problem:

1. Write the natural solution and state its extra space.
2. Then ask yourself the interviewer's question: *can I do this in `O(1)` extra space?*
3. Write that version, and state exactly what you kept: how many variables, and why none of
   them grow.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Reverse String | LeetCode 344 (Easy) | The problem statement explicitly demands `O(1)` extra space, which is why the input is a character list rather than a string. Two pointers and a swap. |
| 2 | Remove Duplicates from Sorted Array | LeetCode 26 (Easy) | The write pointer, in its purest form. The signature returns a length rather than a list, and that is the whole hint. |
| 3 | Move Zeroes | LeetCode 283 (Easy) | Same pattern, one step harder. Building a new list is trivial; doing it in place with one pass and one extra index is the point. |
| 4 | Majority Element | LeetCode 169 (Easy) | Three solutions with three different space costs: a `Counter` is `O(n)`, sorting is `O(1)` extra with an in-place sort, and Boyer-Moore is `O(1)` with one candidate and one count. |

### On problem 4, do this properly

Write all three. Then say out loud, for each one, the time and the extra space:

- `Counter(nums).most_common(1)` →
- `sorted(nums)[len(nums) // 2]` →
- Boyer-Moore voting →

Then answer the question that matters: **what did Boyer-Moore replace the whole count map
with?** If you can say that in one sentence, you have understood what "reformulate the state"
means, and it is the fourth of the four moves from §8 of the lesson.

### The measurement drill

Run the complete program from §5 at `N = 200_000`, then at `N = 400_000`.

The `O(n)` rows should double. The `O(1)` rows should stay at zero. Then add one line of your
own to the program — a function that solves any of today's problems by slicing — and confirm
it lands in the `O(n)` group even though it is one line long.

### The trap drill

Type this out and run it before you read the answer:

```python
def reverse(items):
    items = items[::-1]

nums = [1, 2, 3, 4]
reverse(nums)
print(nums)
```

Predict the output first. Then explain, out loud, in one sentence, why assigning to `items`
inside the function did nothing — and name the two ways to write it so that it does.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *Can you do that in O(1) extra space?*
   Use problem 3. Say what you would keep, why it does not grow, and what you gave up to get
   there.

2. *What happens inside the server between receiving a request and sending a response?*
   Four words for the loop, then the nine steps of handling, then the one-worker-one-request
   constraint.

3. *How many requests per second can one machine handle?*
   Do not guess. Pick a request duration, pick a worker count, do the division out loud, then
   state Little's Law and use it to turn a target into a worker count.

---

## Before you move on

- [ ] I say "O(1) **extra** space" and can explain what I am not counting.
- [ ] I can reverse an array in place with two pointers, from memory, first try.
- [ ] I know that `items.sort()` is in place and still `O(n)` auxiliary, and which sort is
      genuinely `O(1)`.
- [ ] I count recursion depth as space, every time.
- [ ] I can say the server loop in four words and name the three concurrency models with
      their memory costs.
