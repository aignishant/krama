---
day: 133
track: practice
title: "Practice — Cycle detection in a directed graph"
status: written
---

# Day 133 · Practice

**DSA topic:** Cycle detection in a directed graph
**System design topic:** Object storage, S3-style

---

## Code these, in this order

One rule for the whole set: **your first test is the diamond** — `0→1`, `0→2`, `1→3`, `2→3` — and it must
return "no cycle". Write that assertion before the function. It is the only test that catches a two-state
implementation, and every trivial test passes without it.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Course Schedule | LeetCode 207 (Medium) | Three colours or Kahn's, and the outer loop. |
| 2 | Course Schedule II | LeetCode 210 (Medium) | The same pass, returning the order — why Kahn's wins. |
| 3 | Find Eventual Safe States | LeetCode 802 (Medium) | Colours again, but the answer is "not in or leading to a cycle". |
| 4 | Longest Cycle in a Graph | LeetCode 2360 (Hard) | Each vertex has one outgoing edge; the path index is the trick. |
| 5 | Minimum Height Trees | LeetCode 310 (Medium) | Kahn's on an **undirected** graph — peeling leaves, not sources. |

### On problem 1, write both algorithms and time them

Three-colour DFS and Kahn's, on the largest LeetCode input. Record both times and both line counts. Then say
which you would write in an interview and why — and the answer should mention problem 2.

### On problem 1, deliberately write the two-state version

Run it on the diamond. Record the answer. Then run the correct version on the same input. One sentence on what
"seen" failed to distinguish.

### On problem 3, notice the difference

"Safe" is not "not in a cycle" — it is "cannot reach a cycle". Write down what colour a safe vertex ends up
being, and why the black/grey distinction gives you the answer with no extra work.

### On problem 5, notice what changed

Kahn's here peels vertices of degree **one**, not in-degree zero, and the graph is undirected. Write one
sentence on why the same idea transfers and what had to change.

### Then the depth experiment

Build a directed chain of 100,000 vertices — `0→1→2→...` — and run:

1. Recursive three-colour DFS.
2. The same after `sys.setrecursionlimit(2_000_000)`.
3. The iterative version with stored iterators.
4. Kahn's.

Four results. Two are crashes and the difference between the crashes is the point.

### Then the unreachable-cycle experiment

Build `0→1` plus a triangle among 3, 4, 5. Run a version that starts only at vertex 0, and the version with
the outer loop. Two answers, and only one is right.

---

### The colours drill

1. Name the three states and say what each means, in one line.
2. Say which one is the cycle test and why.
3. Say where `BLACK` is assigned and what moving it before the loop does.
4. Give the two-set formulation and name the line people forget.
5. Walk the diamond out loud, step by step, saying the colours.

### The two-algorithms drill

1. Write the three-colour DFS from memory.
2. Write Kahn's from memory.
3. Say what `output != n` means, in words.
4. Give three reasons to prefer Kahn's and one reason to prefer DFS.
5. Say why Kahn's leftovers are not exactly "the vertices in a cycle".

### The undirected-comparison drill

1. Say why the parent check does nothing on a directed graph.
2. Give a two-vertex directed cycle and say what the parent check reports.
3. Say what the three-colour scheme reports on an undirected graph, and why.
4. State the one question each algorithm is really asking.

### The follow-ups drill

1. Return the cycle itself — say what structure you keep and how the slice works.
2. Say what it costs and how to make the lookup constant.
3. Say what you would use to find *all* the deadlocks precisely, and why Kahn's leftovers over-report.
4. Say how you would get a parallel build schedule out of Kahn's.

### The costs drill

1. Derive `O(V + E)` and say why it is `E` and not `2E` here.
2. Say what the worst case is and why an acyclic graph is the expensive one.
3. Give Python's usable recursion depth and the two failure modes past it.
4. Compare memory for a colour array against two Python sets at `V = 10^6`.

### The break-it drill

Trigger each and record the exact output or error:

1. Two states, on the diamond.
2. `on_path.remove` deleted.
3. `BLACK` assigned before the loop, on a triangle.
4. Starting only from vertex 0, with the cycle at 3–5.
5. The undirected parent check on `0→1`, `1→0`.
6. Recursion on a 100,000-vertex chain, before and after raising the limit.
7. Kahn's on a graph built from edges only, with an isolated vertex.

---

### The model drill

1. Say what an object, a key and a bucket are.
2. Say what `photos/2026/a.jpg` actually is, and what "rename the folder" costs.
3. Name the operations object storage supports and the four it does not.
4. Say why `GET` with a byte range exists when partial writes do not.
5. Say why the restrictions are what buy the durability.

### The numbers drill

1. Quote durability and availability separately and say what each means.
2. Give time-to-first-byte and compare with a database read and a cache read.
3. Give the four cost components and say which one dominates.
4. Compute storage and egress for 20M objects at 2 MB with 10M views a day.
5. Recompute origin egress at a 95% CDN hit rate.
6. Compare 40 TB in object storage against 40 TB on managed SSD.
7. Compute the request cost for a million 10 KB objects and compare it with a month of storage.

### The upload-path drill

1. Draw the bad upload path and say what it costs per worker.
2. Draw the presigned-URL path, all four steps.
3. Say why the completion signal should come from the store, not the client.
4. Give the three benefits of multipart upload.
5. Name the multipart trap and the lifecycle rule that fixes it.

### The consistency drill

1. Say what S3's consistency guarantee is today and what it was before 2020.
2. Say what is still not a snapshot.
3. Say what happens if the upload succeeds and the database write fails.
4. Give the three defences, in order.
5. Say which of the three is where the real correctness lives.

### The lifecycle drill

1. Name the storage classes and the price ratio between the cheapest and the most expensive.
2. Write a lifecycle policy for photos kept forever.
3. Give the two traps that make tiering small objects cost *more*.
4. Say what versioning protects against and what it costs.
5. Say what pairs with versioning, always.

### The access drill

1. Say how a presigned URL works and what it is, security-wise.
2. Give two things to get right about expiry and revocation.
3. Say why a presigned URL alone does not work behind a CDN, and what does.
4. Say what the alternative is and when you would accept its cost.

### The trade-offs drill

1. Say what you give up by choosing object storage — four things.
2. Say why 11 nines of durability is not a backup.
3. Say why small objects are inefficient and what to do instead.
4. Give the accurate statement about databases on object storage.
5. Name four cases where object storage is the wrong choice.

### The failure drill

For each, say what happens and what you would build:

1. The object uploads and the database write fails.
2. The browser closes immediately after a successful upload.
3. Versioning is on and there is no lifecycle rule on old versions.
4. A mobile app's video uploads fail 30% of the time, for a year.
5. A presigned download URL is pasted into a group chat.
6. A million 20 KB thumbnails are moved to Infrequent Access.
7. A user requests deletion and the derivative objects are missed.

Two of the seven produce a bill rather than an outage. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Does this directed graph contain a cycle?*
   Three colours with grey as the current path, the diamond as the case two states get wrong, the outer loop
   over all vertices, and Kahn's offered as the version that answers the follow-up too.

2. *Can all courses be finished? Now give me an order.*
   Kahn's in one pass, `output != n` as the cycle test, the emitted order as the schedule, and the level-by-
   level variant as a parallel build plan.

3. *Where do the uploaded images actually go?*
   Object store for bytes and database for the reference, presigned URLs so no bytes touch your servers,
   multipart for large files, a CDN in front — with the egress-versus-storage numbers as the reason.

---

## Before you move on

- [ ] My first test is the diamond, and it returns "no cycle".
- [ ] I can name the three colours and say what grey means.
- [ ] I know where `BLACK` is assigned and what moving it does.
- [ ] I know the missing line in the two-set formulation.
- [ ] I can walk the diamond aloud with the colours.
- [ ] I can write Kahn's from memory and explain `output != n`.
- [ ] I can give three reasons to prefer Kahn's.
- [ ] I know why Kahn's leftovers over-report the cycle.
- [ ] I can return the cycle itself using the path list.
- [ ] I know why the undirected parent check fails here, in both directions.
- [ ] I always loop over every vertex.
- [ ] I build from `range(n)`.
- [ ] I know the recursion limit and both failure modes past it.
- [ ] I can compare array and set memory at a million vertices.
- [ ] I know object storage has no folders and no partial writes.
- [ ] I know what "rename a folder" actually costs.
- [ ] I can quote durability and availability separately.
- [ ] I know first-byte latency and how it compares with a cache.
- [ ] I can compute storage and egress and say which dominates.
- [ ] I can draw the presigned-URL upload path.
- [ ] I know why the completion signal comes from the store.
- [ ] I know the three benefits of multipart and its billing trap.
- [ ] I know what to do when the upload succeeds and the database write fails.
- [ ] I know reconciliation is where the real correctness lives.
- [ ] I can write a lifecycle policy and name the small-object traps.
- [ ] I know what versioning protects against and what it must be paired with.
- [ ] I know why a presigned URL alone fails behind a CDN.
- [ ] I know why 11 nines is not a backup.
- [ ] I can name four cases where object storage is wrong.
- [ ] I answered all three questions above out loud.
