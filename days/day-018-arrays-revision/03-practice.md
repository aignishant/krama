---
day: 18
track: practice
title: "Practice — Arrays revision and mock round"
status: written
---

# Day 018 · Practice

**DSA topic:** Arrays revision and mock round
**System design topic:** Status codes, errors, and idempotency

---

## Code these, in this order

Today is different from the last nine days. These four are not new material — they are the array
toolkit, phrased in ways you have not seen. **Treat every one of them as a real round.** Set a
timer, say everything out loud, and do not look anything up until you have finished or the time is
gone.

The rule for today: **if you did not narrate it, it does not count.** Solving it silently is Sneha's
invisible mirror check.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Best Time to Buy and Sell Stock | LeetCode 121 (Easy) | The single-pass habit from [day 014](../day-014-single-pass-habit/README.md), and whether you ask what happens when prices only fall. |
| 2 | Merge Sorted Array | LeetCode 88 (Easy) | The write pointer from [day 015](../day-015-the-write-pointer/README.md), reversed. Filling from the back is the entire insight. |
| 3 | Find All Numbers Disappeared in an Array | LeetCode 448 (Easy) | Whether you can find the `O(1)`-space trick — using the array's own values as markers — after giving the `O(n)`-space answer first. |
| 4 | Set Matrix Zeroes | LeetCode 73 (Medium) | [Day 016](../day-016-2d-arrays/README.md) plus a genuine trap: marking as you go destroys the information you still need. The `O(1)` version uses the first row and column as the marker store. |

### Run each one as a timed round

Twenty minutes each, and follow the six beats:

```
0-3    restate it, ask the four questions
3-6    one example and its answer, out loud
6-9    the brute force and its cost — say it, do not code it
9-12   the better approach and its cost — then PAUSE as if waiting for a nod
12-17  code it, one sentence per block
17-20  walk your own code through your own example, then the edge cases
```

If you finish early, do not stop. Spend the remaining time answering *"can you do better?"* and
*"what would you test?"* out loud, because both are certain to be asked.

### The four questions, every time

Before any of the four problems, answer these in under forty seconds:

1. Can I modify the input?
2. Is it sorted?
3. Duplicates? Negatives? Empty?
4. Does the order of the output matter?

For problem 3, question 1 is the whole problem — you are *allowed* to modify the input, and that is
what makes the `O(1)` solution possible. For problem 4, question 1 is what makes it hard.

### The record-yourself drill

Do problem 2 once with your phone recording the audio. Then listen to it. Nobody enjoys this and
everybody learns something from it. Count:

- How many seconds of complete silence are there? Anything over fifteen is a problem.
- Did you state a cost before you started typing?
- Did you say *why* you were filling from the back, or only *that* you were?
- How many times did you say "um, so, basically"?

Do it once at the start of each revision day and once more at the end of the phase. The change over
nine weeks is the point.

### The narration drill

Take the finished `merge` solution and say one sentence for each of these lines, out loud, as if
somebody were watching:

```python
write = m + n - 1
i, j = m - 1, n - 1
while j >= 0:
    if i >= 0 and nums1[i] > nums2[j]:
```

The sentences you want are about *why*, not *what*. "`write` is the last slot" is a description.
"`write` starts at the last slot because the largest value must end up there, and that slot is
guaranteed empty" is narration.

### The cost drill

State the time and space cost of each, from memory, in under a minute total, and **count the loops
out loud** rather than naming a class:

1. Reversing an array in place.
2. Rotating an array by `k` with the three-reversal trick.
3. Moving all zeros to the end.
4. Removing duplicates from a sorted array.
5. Inserting at the front of a Python list.
6. Walking an `m × n` matrix by column.
7. Rotating an `n × n` matrix with transpose-then-reverse.
8. Printing a matrix in spiral order.

Anything you cannot count out loud goes on tomorrow's list.

### The status code drill

Give the code for each of these, and one sentence on why it is not the neighbouring code:

1. Fetching a post that does not exist.
2. Fetching the comments of a post that exists but has none.
3. Posting a comment while logged out.
4. Editing somebody else's comment.
5. Posting a comment on a locked post.
6. Posting a comment with an empty body.
7. Posting your two-hundredth comment this minute.
8. The payments service is up but the bank connection is down.
9. A load balancer waited thirty seconds for your backend and gave up.
10. Deleting a comment that was already deleted.

Then answer the one that catches people: **why is number 2 not a `404`?**

### The idempotency drill

Answer these out loud, in two minutes:

1. Which HTTP methods are idempotent, and why is `DELETE` idempotent even though the second call
   returns `404`?
2. Is `PATCH` idempotent? Give one patch body that is and one that is not.
3. Your payment request times out. Name the two things that could have happened, and say why you
   cannot tell them apart.
4. Where does the idempotency key come from, and at what moment is it generated?
5. Why can the server not simply deduplicate on a hash of the request body?
6. Two retries with the same key arrive at the same instant. What stops both of them charging?
7. The key store is unavailable. Do you fail the payment or process it? Defend your answer.

Number 5 is the one that separates people who have read about this from people who have thought
about it.

### The arithmetic drill

Produce these from memory, in under two minutes:

- 50,000 requests a second, 0.1% timing out — how many unknown-outcome requests per day?
- Of those, 1% retried unsafely against a successful original — how many double charges a day?
- A service at 10,000 requests a second fails; every client retries three times with no backoff.
  What is the new load, and what is it with backoff spread over 15 seconds?
- 50,000 requests a second, 10% of them writes, keys kept 24 hours at 300 bytes — how much key
  storage?

Then say the sentence those numbers buy you: *"backoff without jitter is how a blip becomes an
outage."*

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Two array problems, no hints, talk as you go.*
   Have somebody pick two from the table above without telling you which, or pick at random. The
   scoring is not whether you finished. It is: did you restate it, did you ask the four questions,
   did you state a cost before typing, and did you test with an edge case you named yourself.

2. *Your client retries a failed payment request. What could go wrong?*
   Three outcomes first, and the point that a timeout is indistinguishable from a lost response.
   Then why `POST` is not idempotent. Then the key: generated once by the client, claimed atomically
   by the server, stored response replayed. Then backoff with jitter. Ninety seconds.

3. *Walk me through how you'd approach an array problem you have never seen.*
   The six beats, then the decision table — sorted means two pointers or binary search, a few
   extreme values means trackers, a shorter version of the array means a write pointer, a pair or a
   window means two indices. Finish with the four questions and why each one has bitten you.

---

## Before you move on

- [ ] I can name the six beats of a technical round in order, without looking.
- [ ] I ask the four array questions before writing any code, every single time.
- [ ] I state the brute force and its cost before proposing anything better.
- [ ] I pause for agreement before I start typing.
- [ ] I test with edge cases I named myself, not with the example I was handed.
- [ ] I can count out loud, not merely name, the cost of every array operation from days 9 to 17.
- [ ] I can give the right status code for all ten cases in the drill, and say why not the neighbour.
- [ ] I can explain an idempotency key end to end, including why the claim must be atomic.
- [ ] I can redraw the three-outcomes diagram from memory, in whatever tool I like.
