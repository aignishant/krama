# The nine sections, in detail

What belongs in each, and what makes each one fail. Read this before writing a lesson,
not after.

---

## 1. What this is, and why they ask it

**Three sentences** naming the idea, then **one short paragraph** on why it appears in
interviews — which round, which kind of company, how often.

No build-up. The reader knows what they are learning by the end of line one.

> **Fails when:** it opens with "In this lesson we will explore..." or spends a paragraph
> motivating before saying the thing.

---

## 2. The story

200-400 words. A scene from ordinary life. A named person doing something normal, where
this idea already exists without anyone calling it by its technical name.

**Zero technical words.** Not one. No "array", no "server", no "queue" in the technical
sense, no "cache", no "algorithm". A queue at a bank counter is fine; calling it a queue
data structure is not.

Good story sources: a kitchen, a laundry basket, a canteen counter, a wedding hall, a
railway booking counter, a hospital reception, a hostel warden, traffic on a road.

**Choose a scene almost anyone has lived.** The reader should recognise it in the first
line. A scene that only works for someone who has run a chemist's shop, or kept a ledger of
suppliers, is the wrong scene — it teaches the idea to the few people who have already been
there. Sorting socks, queueing for lunch and laying tables work for everybody.

**Simple words. Realistic detail.** Talk the way you would to a friend. Give real numbers,
real times, and the small true details that make it a scene instead of an example — what he
is holding when he stops, what time the shutters went up, what he nearly did wrong.

**No paper props.** Rule 15 applies inside the story too. When the person needs to store
something for later, they save it in their phone. Not a diary, not a notebook, not a slip
kept in a drawer.

The story must contain the **mechanism**, not just the mood. If the idea is "two pointers
move toward each other", two people in the story must walk toward each other. An analogy
that merely feels similar is not a story.

> **Test:** delete the section. If nothing is lost, it was decoration. Rewrite it.

---

## 3. The idea in plain English

Take the story apart. Map each piece onto the technical idea, one step at a time.

This is where technical vocabulary enters — **each term defined the first time it appears**,
in a sentence a fifteen-year-old could read.

Concrete before abstract, always. A seven-element array before "an array of size n". The
number 5 before the variable `k`.

> **Fails when:** it uses a word the reader has not met, or jumps to the general case
> before showing a specific one.

---

## 4. The picture

At least one diagram. Captioned with **what to notice in it** — not "Figure 1: the array".

**ASCII** for arrays, memory layout, pointers, bit patterns — anything where adjacency is
the point:

```
 index   0    1    2    3    4    5    6
       +----+----+----+----+----+----+----+
 value |  2 |  3 |  5 |  8 | 13 | 21 | 34 |
       +----+----+----+----+----+----+----+
         ^                            ^
       left                         right
```

**Mermaid** for trees, graphs, architectures, state machines, request flows.

---

## 5a. The code, built step by step *(DSA lessons)*

Fragments of **ten lines or fewer**, each followed by prose saying what it does and what
stays true after it runs. Never a forty-line block with a comment on top.

Then the **complete, working, copy-pasteable solution** at the end of the section. Python
3.12+, type hints on the signature.

Show the whole answer. This repository does not hide solutions from the reader.

Where the day is *about* a structure, build it from scratch first, then say "in an
interview you would use this" and show the standard-library call.

---

## 5b. How it actually works *(system design lessons)*

The mechanics. What the component stores, what it does on a read, what it does on a write,
what happens when it fails or restarts.

**Name real products.** Redis, Memcached, Postgres, MySQL, Cassandra, DynamoDB, Kafka,
RabbitMQ, S3, Elasticsearch, nginx, Cloudflare. A design lesson with no product names in
it is a lesson about nothing.

---

## 6a. What it costs *(DSA lessons)*

Count it out from the loops in front of the reader:

> The outer loop runs `n` times. For each of those the inner loop runs `n` times. So the
> body runs `n × n = n²` times, and each run is constant work. That is **O(n²)**.

State space separately, and say whether you mean extra space or total space.

> **Fails when:** it names a complexity without counting anything.

---

## 6b. The numbers *(system design lessons)*

The arithmetic, with the multiplication shown:

> 50 million daily users × 20 reads each = 1 billion reads a day.
> 1 000 000 000 ÷ 86 400 ≈ **11 600 reads per second** average, call it 35 000 at peak.

Cover whichever apply: QPS, storage per year, bytes per record, bandwidth, fan-out
multiplier, replica count, cache hit ratio.

> **Fails when:** it says "that would be a lot of traffic".

---

## 7a. The traps *(DSA lessons)*

At least two, and both must be concrete:

- **The near-miss** — the version that looks correct. Show it, then show the exact input
  that breaks it, then show what it returns versus what it should return.
- **The real error** — actual pasted output. Run it if you can.
  `IndexError: list index out of range`, never "you get an index error".

---

## 7b. The trade-offs *(system design lessons)*

What you give up by choosing this. What you would choose instead, and when.

The sentence beginning **"I would not use this if..."** is the one that separates a
candidate who has read a blog post from one who has thought about it. Write it explicitly.

---

## 8. In the interview

The section the whole document exists for. Four parts, all four required:

**How it gets asked** — two or three real phrasings, the way an interviewer actually says
it, including the vague version.

**What to say out loud** — a script for the first ninety seconds. What you clarify, what
you state, what you write down before you start coding or drawing.

**The follow-ups** — the three questions that come next, each with a short answer. These
are where candidates fall over, and they are predictable.

**A model answer** — written out, in full, as a strong candidate would actually say it.
Not a summary of what to say. The words.

> **Fails when:** it is three bullet points of generic advice.

---

## 9. Recall card

Five lines, maximum. What survives if the reader forgets everything else. This is what
gets re-read the night before the interview.

Format it as a short list, no prose paragraphs.
