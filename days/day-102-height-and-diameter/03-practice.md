---
day: 102
track: practice
title: "Practice — Height, depth, and diameter"
status: written
---

# Day 102 · Practice

**DSA topic:** Height, depth, and diameter
**System design topic:** Cache invalidation and eviction policies

---

## Code these, in this order

One rule for the whole set: **before writing the one-pass version, write the `O(n²)` one and say its cost
out loud.** Finding the improvement is what is being tested, and you cannot demonstrate finding it if you
start at the answer.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Maximum Depth of Binary Tree | LeetCode 104 (Easy) | The base case, and which convention you are using. |
| 2 | Balanced Binary Tree | LeetCode 110 (Easy) | Spotting the repeated `height` call, and the sentinel. |
| 3 | Diameter of Binary Tree | LeetCode 543 (Easy) | Return one thing, record another. |
| 4 | Longest Univalue Path | LeetCode 687 (Medium) | The same shape with a condition on each arm. |

### On problem 2, write the naive one and time it

Build a chain of 2,000 nodes and time both versions. Record the ratio. Then say why a chain is the worst
case for the naive version *and* for the recursion depth.

### On problem 3, break it three ways on purpose

Run each and record the output: assume the path goes through the root; return the bent path instead of
the height; omit `nonlocal`. Say which of the three raises and which two are silent.

### On problem 4, notice what changed

Compare it line by line with the diameter solution. Say exactly which lines differ, and say what stayed
the same.

### After all four, write the two-line summary

For each problem: what is returned to the parent, and what is recorded on the side. If you can fill that
table in from memory, you have the technique.

---

### The definition drill

1. Define diameter in one sentence.
2. Give the edge answer and the node answer for a five-node example.
3. Construct a tree whose diameter does not touch the root, and give both numbers.
4. State the two bounds relating height and diameter, and give a shape that achieves each.

### The key-observation drill

1. State the observation about every path having one highest node.
2. Say why that means evaluating every node considers every path exactly once.
3. Write the formula for the path bending at a node, in the edge convention.
4. Say why it is `+ 2` and what the formula becomes in the node convention.

### The naive-cost drill

1. Write the naive version.
2. Say why it is not `O(n)`, in terms of what `height` does.
3. Compute the total work for a balanced tree and for a chain.
4. Give the operation counts at n = 1,000, 10,000 and 100,000.
5. Say what else goes wrong on the same input that makes it quadratic.

### The return-versus-record drill

1. State the technique in one sentence.
2. For the diameter, say what is returned and what is recorded.
3. Say why the parent cannot use the recorded value.
4. Fill in the table for all five problems in the family.
5. Return the bent path instead and describe how the answer misbehaves.

### The `nonlocal` drill

1. Write the inner function without `nonlocal` and run it.
2. Quote the error, and say why Python produced it.
3. Say what happens if you only *read* the outer variable instead of assigning.
4. Name two alternatives to `nonlocal` and say which you prefer.

### The sentinel drill

1. Write the one-pass balanced check with a sentinel.
2. Say why `-2` is safe and `-1` is not, under the edge convention.
3. Say what the safe sentinel would be under the node convention.
4. Write the tuple version and say what it costs.
5. Say what "short-circuit" means here and where the saving comes from.

### The convention drill

1. Write the base case for both conventions.
2. Write the matching bending formula for each.
3. Mix them and compute the answer for a five-node tree; say by how much it is wrong.
4. Say why the mixed version is right on a single node.

### The break-it drill

Trigger each and record the exact output or error:

1. Assuming the diameter passes through the root, on an asymmetric tree.
2. Omitting `nonlocal`.
3. Returning `max(left, right, left + right + 2)`.
4. Base case `0` with the `+ 2` formula.
5. `-1` as the unbalanced sentinel.
6. A recursive diameter on a 10,000-node chain.

### The extension drill

1. Modify the solution to return the path, not the length.
2. Say what the space complexity becomes and why.
3. Describe the two-pass alternative that keeps `O(height)` space.
4. Say which you would offer first in an interview.

---

### The two-problems drill

1. Define invalidation and eviction, and say what each is about.
2. Give the cause and the fix for each.
3. Say what a failure of each one looks like to a user.
4. Say which one is a correctness bug and which is a performance bug.

### The mechanisms drill

1. Name the three invalidation mechanisms.
2. For each, give one advantage and one cost.
3. Say why a TTL belongs on every key even with perfect explicit invalidation.
4. Say what makes explicit invalidation hard, and give an example with five affected keys.

### The race drill

1. Draw the read-write race on a timeline, labelling both actors.
2. Say why nothing corrects it afterwards.
3. Compute the probability for a key read 100 times a second and a 2 ms window.
4. Name four mitigations in the order you would apply them.
5. Say which of them fully closes the race and which only bound it.

### The ordering drill

1. State both possible orders of the database write and the cache delete.
2. For each, describe the race and the size of its window.
3. Say which order you would use and why.
4. Say what still protects you when the chosen order loses the race anyway.

### The write-strategy drill

1. Name the three strategies and describe each in one line.
2. Give a use case for each, and the specific data type for write-back.
3. Compute the collapse ratio for a counter written 10,000 times a minute.
4. Say what a crash costs under write-back.
5. Say why you delete rather than set, in two reasons.

### The eviction drill

1. Name five eviction policies and what each throws away.
2. Say which is the default choice and why.
3. Name LRU's failure mode and describe the incident it causes, with numbers.
4. Name the fix, and the algorithm that implements it.
5. State Redis's default policy and say why that surprises people.

### The tuning drill

Fill in the two-by-two: for each combination of hit rate and eviction rate, say what it means and what
you would do.

1. Low hit rate, high eviction rate.
2. Low hit rate, low eviction rate.
3. High hit rate, high eviction rate.

Then compute the database load at 6,000 reads/second for hit rates of 90, 70 and 45 percent.

### The one-to-many drill

1. Say what makes "one write invalidates a hundred keys" hard.
2. Give the three answers and say when you would choose each.
3. Write the namespace-versioning keys and the single command that invalidates them.
4. Say what happens to the old entries afterwards.
5. Say how CDNs solve the same problem for static assets.

### The failure drill

For each, say what happens and what you would add:

1. A nightly export runs at 02:00.
2. Redis is deployed with no `maxmemory-policy`.
3. A user saves their profile and immediately reloads the page.
4. A reader caches a value it read before a concurrent write.
5. The same value is cached in the browser, the CDN and Redis with different TTLs.
6. The cache is emptied by a restart at peak traffic.

Two of the six are not fixed by changing the cache configuration. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the diameter of the binary tree in `O(n)`.*
   The definition with the convention declared, the not-through-the-root warning given before you can get
   it wrong, the every-path-has-one-highest-node observation, the naive version priced, then the
   return-versus-record sentence said precisely, and both complexities.

2. *How do you keep the cache consistent with the database?*
   Invalidation and eviction separated, write-around plus a TTL as the default, delete-not-update with the
   reason, the read-write race drawn with what happens afterwards, the write ordering, and the staleness
   budget per data type.

3. *The cache is full. What do you throw away?*
   LRU with `allkeys-lru`, Redis's surprising default, the approximate-LRU detail, the scan failure with
   its numbers, and admission control as the fix.

---

## Before you move on

- [ ] I can define diameter and give both conventions.
- [ ] I always say "it does not have to pass through the root" before writing code.
- [ ] I can state the every-path-has-one-highest-node observation.
- [ ] I can write the naive version and price it on a chain.
- [ ] I can say the return-versus-record sentence precisely.
- [ ] I know why the parent cannot use the recorded value.
- [ ] I can fill in the family table for all five problems.
- [ ] I know what `nonlocal` is for and what happens without it.
- [ ] I can write the one-pass balanced check and justify the sentinel value.
- [ ] I can give both bounds relating height and diameter, with achieving shapes.
- [ ] I know what returning the path costs, and the two-pass alternative.
- [ ] I can separate invalidation from eviction in one sentence each.
- [ ] I can name the three invalidation mechanisms and their costs.
- [ ] I can draw the read-write race and say why nothing fixes it.
- [ ] I know which order to write the database and the cache in, and why.
- [ ] I can name the three write strategies and the data type for write-back.
- [ ] I know Redis's default eviction policy and why it matters.
- [ ] I can describe the LRU scan incident with numbers and name the fix.
- [ ] I can invalidate a hundred keys with one command.
- [ ] I answered all three questions above out loud.
