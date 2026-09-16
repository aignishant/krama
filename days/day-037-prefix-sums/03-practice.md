---
day: 37
track: practice
title: "Practice — Prefix sums: answering range queries instantly"
status: written
---

# Day 037 · Practice

**DSA topic:** Prefix sums: answering range queries instantly
**System design topic:** Key-value stores

**Theme:** Memory model, deeper

---

## Code these, in this order

Four problems on one idea. **Before each, say the formula as a sentence** — *after the end, minus
before the start* — and say where the sentinel is.

Before each one, ask:

1. One query or many? Is the precompute actually earning its keep here?
2. Do I need the stored array, or just a running total?
3. Both ends inclusive, or half-open?
4. Can the values be negative — and does anything in my plan care? (It should not.)

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Running Sum of 1d Array | LeetCode 1480 (Easy) | The build loop itself — `prefix[i + 1] = prefix[i] + nums[i]` with nothing else in the way. |
| 2 | Range Sum Query — Immutable | LeetCode 303 (Easy) | The sentinel and the formula as a set; the constructor/method split. |
| 3 | Find Pivot Index | LeetCode 724 (Easy) | The running-total form — no stored array, check before adding, empty left side at index 0. |
| 4 | Left and Right Sum Differences | LeetCode 2574 (Easy) | Two directions of the same idea; whether your boundaries stay honest when one runs backwards. |

### On problem 2, break it both ways

Build the prefix without `initial=0` and query `(0, 3)` using `prefix[j] - prefix[i - 1]`. You get a
silently wrong number — say which entry `prefix[-1]` actually read. Then keep the zero-less array
but use the lesson's formula on the last index, and collect the
`IndexError: list index out of range`. Finish the sentence: *the sentinel and the formula are...*

### On problem 3, honour the empty side

Run `[2, 1, -1]` and explain, out loud, why the answer is 0 — what is the sum of nothing, and why
does checking before adding get it right with no special case?

### On problem 2 again, the follow-up rehearsal

Say the two-minute answer to *"now the array can be updated between queries"*: the contract that
broke, the rebuild-if-rare option, and the two tree names with their O(log n) — without pretending
to implement them.

### The formula drill

For `nums = [4, 7, 3, 6, 2, 5, 1]`, `prefix = [0, 4, 11, 14, 20, 22, 27, 28]`, answer from the
readings alone, under five seconds each, out loud:

1. Sum of `nums[2..4]`.
2. Sum of `nums[0..6]`.
3. Sum of `nums[3..3]`.
4. Sum of `nums[0..2]`.
5. Which two readings answer "sum of the last three elements"?

### The tell drill

For each, say whether prefix sums are the right tool, and why in one sentence:

1. One range-sum query on a ten-element array.
2. A hundred thousand range-sum queries on a fixed array.
3. Range sums where the array takes an update every few queries.
4. Longest subarray with sum at most k, all values positive.
5. Count subarrays summing to exactly k, negatives allowed.

Number 4 is yesterday's tool; number 5 is tomorrow's. Saying which is which *is* the drill.

### The shelf-or-ledger drill

For each piece of data, say Redis, DynamoDB, or Postgres — and the one-line reason:

1. Session blobs, 30-day expiry, read on every request.
2. Order history, seven years, auditors visit.
3. A like counter at 5,000 increments a second.
4. Cart items at Amazon scale, fetched by cart id.
5. Product search by colour, size and price.

### The refusal drill

Answer each in one or two sentences, out loud:

1. Why does "find every session for user 7" not exist in a key-value store — and what do you write
   at write time to make it exist?
2. What can Redis lose in a crash at its default settings, and which day's Postgres setting is the
   same trade?
3. Why is a Redis `INCR` counter free of the hot-row queue that the same counter has in Postgres?
4. What makes DynamoDB's pricing punish a fifty-key page view?

### The arithmetic drill

From memory, in under two minutes:

- 100,000 queries × average stretch 50,000 by loop, against build-plus-subtract. The two totals and
  the ratio.
- 50 million sessions × 1 KB — where does it fit? 200 million items × 4 KB — where does that fit?
- A session check on every one of 20,000 requests/s — what does moving it to Redis take off
  Postgres?

---

## Build these, in all three languages

Complete each exercise in Python, Go, and C++. Use today's lessons as references, then explain the result without looking at them.

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Keep an object in a long-lived collection, remove every local name, and explain why it remains alive. | Reachability versus usefulness. |
| 2 | Create two objects referring to each other and explain how the language reclaims or retains them. | Cycles and ownership. |
| 3 | Replace an owning observation with a weak/non-owning reference where supported and explain the lifetime check. | Observation without extending lifetime. |

## Compare

- **Python** — CPython uses reference counts and a cyclic garbage collector. Reachable but unnecessary objects remain live, so garbage collection does not prevent every memory leak. After building, say what was easiest and hardest in this version.
- **Go** — Go’s tracing garbage collector reclaims unreachable heap objects. Escape analysis decides where values may be stored; source syntax alone does not decide stack versus heap. After building, say what was easiest and hardest in this version.
- **C++** — unique_ptr expresses exclusive ownership, shared_ptr expresses shared ownership, and weak_ptr observes a shared object without extending its lifetime. After building, say what was easiest and hardest in this version.

CPython combines reference counting with cycle collection, Go traces reachable objects, and C++ smart pointers express ownership. Long-lived reachable data can waste memory under any of these models.

For each implementation, state the expected output, the input that exposes a mistake, and the time and extra space used.

## Say these out loud

### DSA and system design

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Answer many range-sum queries on a fixed array.*
   The precompute trade named on both sides, the sentinel and why, the formula as a sentence, and
   the follow-up about updates handled with the two tree names.

2. *When would you use a key-value store instead of a relational database?*
   The one promise and the refusals, Redis against DynamoDB in one breath each, the four standard
   uses, and where it sits — beside the system of record, never instead of it.

3. *Why does the prefix array have one more entry than the array?*
   Boundaries, not elements. What `prefix[0]` means, which queries need it, and what Python does —
   silently — when it is missing and `i` is 0.

### Languages

1. What is a memory leak in a garbage-collected language?
2. Can a garbage-collected program leak memory? Compare the answer across all three languages.
3. Can forced GC reclaim a live map entry? Explain the corresponding design decision in Python and C++.

## Before you move on

- [ ] I can build the prefix array with the sentinel and say what each entry means.
- [ ] I say "after the end, minus before the start" instead of reciting indices.
- [ ] I know both failure modes of the missing sentinel — the silent one and the crash.
- [ ] I can name when the precompute loses: single queries, and updates between queries.
- [ ] I can say what Redis and DynamoDB each promise, and the questions neither can answer.
- [ ] I know which data may live only on the shelf, and which needs a ledger behind it.
- [ ] I answered the DSA, system design, and language questions out loud.
- [ ] I completed all three language exercises in Python, Go, and C++.
- [ ] I can predict the examples and explain the failure cases.
