---
day: 17
track: practice
title: "Practice — Matrix tricks: rotate, spiral, transpose"
status: written
---

# Day 017 · Practice

**DSA topic:** Matrix tricks: rotate, spiral, transpose
**System design topic:** Designing a good REST endpoint

---

## Code these, in this order

Four problems where the difficulty is entirely in the boundaries. None of them needs an idea you do
not already have. All of them punish a single wrong `+ 1`.

Before each one, say out loud:

1. Is it square, or `m × n`? Does that change whether I can work in place?
2. What are my loop bounds, stated as a range with the endpoint spelled out?
3. Which cells could be visited twice, and what stops that?
4. What are the two degenerate inputs — one row, one column — and does my code survive them?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Transpose Matrix | LeetCode 867 (Easy) | That the answer is `n × m` for an `m × n` input, so it cannot be done in place unless the matrix is square. Write both versions. |
| 2 | Rotate Image | LeetCode 48 (Medium) | Transpose then reverse each row, and the `range(r + 1, n)` that keeps each pair swapped once. The whole question is the words *in place*. |
| 3 | Spiral Matrix | LeetCode 54 (Medium) | Four boundaries and the two guards. It is rectangular on purpose. |
| 4 | Spiral Matrix II | LeetCode 59 (Medium) | The same four passes, writing instead of reading. If you built problem 3 cleanly this is a fifteen-line rewrite. |

### On problem 2, prove the direction to yourself

Before writing any code, take `[[1,2,3],[4,5,6],[7,8,9]]` and say out loud where the 7 has to end
up after a clockwise turn. Then say where the transpose sends it, then where reversing that row
sends it, and check the two agree. Five seconds, and it is the check that saves you from writing
the anticlockwise version by mistake.

Then write all four turns and verify each against the same input:

```
clockwise      -> [[7,4,1],[8,5,2],[9,6,3]]
anticlockwise  -> [[3,6,9],[2,5,8],[1,4,7]]
180 degrees    -> [[9,8,7],[6,5,4],[3,2,1]]
```

### On problem 2, run the broken version

```python
def rotate(matrix):
    n = len(matrix)
    for r in range(n):
        for c in range(n):            # the bug
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
    for row in matrix:
        row.reverse()
    return matrix

print(rotate([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
```

Predict the output first. Then explain, in one sentence, why there is no error message — and why
counting swaps (three for a `3 × 3`, not nine) is a faster check than staring at the output.

Then run the same correct function on `[[1, 2, 3], [4, 5, 6]]` and on `[[1, 2], [3, 4], [5, 6]]`.
One of them crashes and one of them silently returns nonsense. Say which is which before you run
them, and say why the silent one is worse.

### On problem 3, test these five inputs every time

```python
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]        # square
[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]   # wider than tall
[[1, 2, 3, 4]]                            # one row
[[1], [2], [3], [4]]                      # one column
[]                                        # and [[]]
```

The square case passes even when the guards are missing, which is exactly why it is useless as a
test. Write the version **without** the two `if` statements, run it on the one-row input, and look
at what comes back:

```
[1, 2, 3, 4, 3, 2, 1]
```

Seven values from a four-cell matrix. Then add the guards and watch it become `[1, 2, 3, 4]`. Do
this once by hand and you will never forget the guards again.

### The bounds drill

Answer these without running anything, then check:

1. In `range(right, left - 1, -1)`, which values does it produce when `right = 3` and `left = 1`?
2. Why is it `left - 1` and not `left`?
3. After the top pass and `top += 1`, why does the right-hand pass start at `top` rather than at
   `top - 1`?
4. On an `n × n` matrix, how many times does the outer `while` loop run?
5. In the transpose loop, how many swaps happen for `n = 5`?

### The stretch problem

**Rotate Image, one pass.** Rewrite problem 2 as ring-by-ring four-way swaps instead of
transpose-then-reverse: for each ring, walk `i` across it and rotate four cells at a time, using one
temporary. Same `O(n²)` time and `O(1)` space, about half the writes.

Get the four index expressions right before you write the loop: say each of the four cell positions
out loud in terms of `layer`, `i` and `n`, then check them against the corners of a `4 × 4`. This is
genuinely fiddly, which is the point — it is the version interviewers ask for when they want to
push.

### The endpoint design drill

Design the endpoints for **a notifications feature**, with no help and nothing to copy. Cover:
listing a user's notifications, filtering to unread, marking one as read, marking all as read,
deleting one, and the notification preferences a user can change.

Then check your own design against these seven questions:

1. Did you list the nouns before writing any path?
2. Is "mark all as read" a verb in a path? Should it be, and can you justify it in one sentence?
3. Where did "unread only" go — the path or the query string? Why?
4. Is `PATCH /notifications/{id}` with `{"read": true}` better or worse than
   `POST /notifications/{id}/read`? Argue both sides, then pick.
5. Is your list endpoint paginated? What is the default limit and the hard cap?
6. What comes back when the user has zero notifications?
7. Which of your endpoints are idempotent, and does "mark all as read" being called twice cause a
   problem?

### The critique drill

Say what is wrong with each of these in one sentence, out loud, naming the rule and not just the
symptom:

```
POST /api/getCommentsForPost          {"post_id": 17}
GET  /posts/17/comments/newest
GET  /posts/17/comments               → 404 when the post has no comments
GET  /posts/17/comments/91/replies/4/reactions
POST /comments/91/likes               (called twice on a double-tap)
GET  /posts/17/comments?page=5000&per_page=20
DELETE /comments/91                   → 200 OK, {"deleted": true, "count": 1}
```

### The numbers drill

From memory, in under two minutes, for a site with 10 million daily users where 2% comment 1.5
times a day and each user views 8 threads:

- Comments written per day, and writes per second at peak.
- Thread views per day, and reads per second at peak.
- The read-to-write ratio, and the one design conclusion it forces.
- Storage per year at 250 bytes a comment.
- The size of an unpaginated response for a 50,000-comment post, and how long that takes on a
  2 Mbps connection.

Then say the sentence those numbers earn you: *"this does not need sharding, and here is why."*

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Rotate the image ninety degrees clockwise, in place.*
   Ask whether it is square, and say why that matters. State the decomposition — transpose, then
   reverse each row — then check the direction on one corner out loud. Name the `r + 1` before you
   write it and say what goes wrong without it. Finish with `O(n²)` time, `O(1)` extra space, and
   the one-liner you are choosing not to use.

2. *Design the endpoints for a comments feature.*
   Scope first, nouns second, paths third. State the nesting rule as a rule. Mention pagination
   before anyone asks. Sketch one response body. Name the errors, including the empty-list-is-not-a-
   404 point. Flag your one action sub-resource and say why you are keeping the number small.

3. *Print the matrix in spiral order.*
   Four boundaries, four passes, shrink each as you finish it. Then the important sentence: the
   bottom and left passes need guards because the remaining block may be a single row or a single
   column, and the square test case will not catch it.

---

## Before you move on

- [ ] I ask "is it square?" before writing any in-place matrix code.
- [ ] I can state the two-flip rotation recipe and check the direction on one corner in five seconds.
- [ ] I write `range(r + 1, n)` in a transpose without having to think about it.
- [ ] I test spiral code on a single row and a single column, every time.
- [ ] I list the nouns before I write the first path.
- [ ] I paginate every collection endpoint I design, without being asked.
- [ ] I know that an empty collection is `200` with `[]`, and that `404` means the parent is missing.
- [ ] I can redraw the spiral-boundaries diagram from memory, in whatever tool I like.
