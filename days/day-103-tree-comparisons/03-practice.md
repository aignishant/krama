---
day: 103
track: practice
title: "Practice — Same tree, symmetric tree, and subtree"
status: written
---

# Day 103 · Practice

**DSA topic:** Same tree, symmetric tree, and subtree
**System design topic:** Content delivery networks

---

## Code these, in this order

One rule for the whole set: **write the two base-case lines before anything else, as a unit.** Both
`None` is `True`; exactly one `None` is `False`. Every crash in this topic is on the line that comes
after those two, when they are not both there.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Same Tree | LeetCode 100 (Easy) | The three base cases, and the `and` short-circuit. |
| 2 | Symmetric Tree | LeetCode 101 (Easy) | Crossed arguments — mirror, not identical. |
| 3 | Subtree of Another Tree | LeetCode 572 (Easy) | Different base cases, and what "subtree" strictly means. |
| 4 | Invert Binary Tree | LeetCode 226 (Easy) | Producing a mirror rather than testing for one. |

### On problem 1, delete the middle base case on purpose

Run it on two trees of different shapes and record the exact error and the line it happens on. Then say
in one sentence why the missing case is a crash rather than a wrong answer.

### On problem 2, write the wrong version first

Write `is_same(root.left, root.right)`, run it on `[1,2,2,null,3,null,3]`, and record what it says. Then
write the crossed version and say what "mirror" means as opposed to "identical".

### On problem 3, test the strictness

Run `is_subtree([1,2,3], [1,2])` and record the answer. Say why it is `False` and what would have to be
true for it to be `True`.

### On problem 4, then connect it back

After inverting, check that `is_symmetric(t)` equals `is_same(t, invert(copy(t)))`. Say why you would
still write `is_mirror` instead, in terms of allocation.

---

### The base-case drill

1. Write the three base cases from memory.
2. Say what each one means about the two trees.
3. Say what error the missing middle case produces, and on which expression.
4. Say why everything after those two lines can dereference safely.
5. Say what the `and` short-circuit buys you, and what complexity that gives.

### The mirror drill

1. Write `is_same` and then derive `is_mirror` from it by changing one thing.
2. Say the change in words.
3. Construct a tree where identical halves are not symmetric.
4. Cross only one of the two calls and find an input where it is wrong.
5. Write the entry point and say why an empty tree and a single node are both symmetric.

### The subtree drill

1. Write the base cases for `is_subtree` and say why they differ from `is_same`'s.
2. Swap them and say what the function now returns for everything.
3. Define "subtree" precisely, in terms of what may hang below.
4. Give an input where a partial match is not a subtree.
5. Say what question you would ask the interviewer if they meant partial matching.

### The complexity drill

1. State the time for same tree, and say why it is `min` rather than `max`.
2. State the naive subtree complexity and give the worst-case input that achieves it.
3. Say why it is usually much better than the bound in practice.
4. Give the operation counts for n = 10,000 and m = 1,000.

### The serialisation drill

1. Write `serialise` with both fixes.
2. Construct two different trees that collide without null markers.
3. Construct a false match that occurs without delimiters.
4. State the complexity, and say what you are trading for it.
5. Say how you would phrase the complexity honestly with respect to `str.find`.

### The break-it drill

Trigger each and record the exact output or error:

1. `is_same` without the "exactly one is None" case.
2. `is_same(root.left, root.right)` as a symmetry test.
3. One of the two mirror calls uncrossed.
4. `is_subtree` with the base cases swapped.
5. Serialisation without null markers, comparing a left-only and a right-only tree.
6. Serialisation without delimiters, searching for a tree containing 2 inside one containing 12.
7. A recursive comparison on two chains of 10,000 nodes.

### The iterative drill

1. Write `is_same` with an explicit stack of pairs.
2. Write `is_symmetric` with a queue of pairs.
3. Say what the crossed pushes look like in the iterative version.
4. Say when you would bother writing these.

---

### The why-it-exists drill

1. Compute the round trip from India to Virginia, showing the working.
2. Say why no server optimisation touches it.
3. Give the edge, same-continent and cross-world figures.
4. Say what a page with four sequential round trips costs, both ways.
5. Say why the TLS handshake saving is often bigger than the content saving.

### The byte-split drill

1. Give the byte breakdown of a typical 2 MB page.
2. State the percentage a CDN can serve, in bytes and in requests.
3. Compute origin bandwidth per hour at 100,000 page loads, both ways.
4. Compute the monthly cost difference, including the CDN's own bandwidth charge.
5. Say why this makes the CDN the biggest of the four cache layers.

### The distribution drill

1. Define origin pull and say what a cold miss is.
2. Compute the cold misses for one new object across 300 edges.
3. Describe an origin shield and recompute.
4. Say when you would use push instead, with two examples.
5. Name the company that ships hardware into ISPs and say why.

### The headers drill

1. Write the `Cache-Control` header for a fingerprinted asset.
2. Write one for a personalised page.
3. Write one that caches at the edge but not in the browser, and name the directive.
4. Explain `ETag` and what a 304 saves.
5. Say what `Vary: User-Agent` does to the cache.

### The limits drill

1. Name the two things a CDN cannot help with, and say why they are the same thing.
2. Describe the page-splitting design that works around the first.
3. Say what edge compute changes and what it does not.
4. Say which kinds of product are transformed and which are barely helped, with an example of each.

### The invalidation drill

1. Say how long a purge takes and what limits it.
2. Describe the renaming approach and what it makes possible.
3. Say what "old and new coexist safely" prevents.
4. Compute the work for a deploy changing 400 files, both ways.

### The hit-rate drill

1. Give the expected hit rates for five kinds of content.
2. Say what a shared link with `utm_source` does to the cache key.
3. Compute the hit rate for one image shared four ways.
4. Name the three things you would check first when the hit rate is 60 percent.

### The failure drill

For each, say what happens and what you would add:

1. A personalised page is served with `Cache-Control: public`.
2. A response carrying `Set-Cookie` is cached.
3. `app.js` is cached for a year with no fingerprint.
4. A launch happens with a completely cold cache.
5. The CDN has a regional outage.
6. The origin is not firewalled to CDN traffic only.

Two of the six are security problems rather than performance problems. Name them.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Are these two trees identical? Is this tree a subtree of that one?*
   The two-tree recursion named, the three base cases stated before writing, what the missing one costs,
   the short-circuit complexity, then the strict meaning of subtree with its different base cases and the
   `O(n × m)` bound with the serialisation alternative and both of its silent traps.

2. *Would a CDN help this system? What would it not help with?*
   Distance as physics with the 200 ms number, the 95 percent byte split, origin pull plus a shield with
   the 300× burst, then the two limits — personalisation and writes — the page-splitting fix, and renaming
   instead of purging.

3. *Is this tree symmetric?*
   The crossed arguments, the counter-example where identical halves are not symmetric, and why an empty
   tree and a single node both qualify.

---

## Before you move on

- [ ] I write the two base-case lines as a unit before anything else.
- [ ] I can say what error the missing middle case produces.
- [ ] I can derive `is_mirror` from `is_same` by naming one change.
- [ ] I have a tree where identical halves are not symmetric.
- [ ] I know why `is_subtree`'s base cases are the opposite way round.
- [ ] I can state what "subtree" strictly means and give a failing partial match.
- [ ] I can state the same-tree complexity and say why it is `min`.
- [ ] I know the adversarial input that makes the naive subtree quadratic.
- [ ] I can write `serialise` with both fixes and explain each.
- [ ] I can construct the collision and the false match that each fix prevents.
- [ ] I can write both iterative versions with pairs.
- [ ] I can compute the India–Virginia round trip from first principles.
- [ ] I can give the byte split and the offload arithmetic.
- [ ] I can explain a cold miss and why an origin shield matters, with the 300× number.
- [ ] I can write three different `Cache-Control` headers and say what each is for.
- [ ] I can name both CDN limits and the page-splitting fix.
- [ ] I can explain why renaming beats purging, including the coexistence benefit.
- [ ] I know the first three things to check when a hit rate is low.
- [ ] I answered all three questions above out loud.
