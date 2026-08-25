# Case study days

Days where the system design lesson is "design X" — a parking lot, an elevator, Twitter,
Uber. Days 77-96 (low-level) and 145-170 (high-level).

Same nine sections. But sections 5, 6 and 7 carry a specific structure, because a case
study is a **performance**, not a topic. The reader has to be able to reproduce it under a
clock with someone watching.

---

## Low-level design days (77-96)

The output is **classes**. The interviewer wants to see whether you can turn requirements
into objects with the right responsibilities.

### §5 · How it actually works

Run the same five moves the reader will run in the interview, in this order:

1. **Clarify** — three or four questions you would ask, with the answers you will assume.
   Write them out. ("Multiple floors? Yes. Multiple vehicle sizes? Yes. Payment on exit.")
2. **The nouns** — pull the classes straight out of the requirements. List them with one
   line each on what each is responsible for.
3. **The class diagram** — Mermaid `classDiagram`. Show fields, key methods, and the
   relationships. This is the artefact the interviewer is waiting for.
4. **The interesting part** — every LLD prompt has one place where the design is actually
   decided. Spot allocation. Elevator scheduling. Fare calculation. Put an interface there
   and show two implementations, so the design survives a changed requirement.
5. **The code** — the two or three classes that carry the interesting part, written out
   properly. Not all of them; the ones that matter.

### §6 · The numbers

Lighter here, but not skipped. How many objects live in memory. What the concurrency
looks like — two people clicking the same seat, two cars at the same barrier. Name the
lock or the atomic operation.

### §7 · The trade-offs

Which requirement would break this design, and what you would change. Interviewers almost
always add a requirement at the end; this section is the rehearsal for that.

---

## High-level design days (145-170)

The output is **an architecture**. Boxes, arrows, a data model, and numbers.

### §5 · How it actually works

Six moves, in this order — the same order the reader will use in the interview:

1. **Functional requirements** — three or four, no more. Say out loud what you are
   deliberately leaving out.
2. **Non-functional requirements** — scale, latency target, consistency requirement,
   availability target. Each as a number or a named guarantee.
3. **The API** — three or four endpoints. Method, path, request, response.
4. **The data model** — the tables or collections, the key fields, and the shard key.
   Say why that shard key and not another.
5. **The architecture** — Mermaid `flowchart LR`. Client, load balancer, service, cache,
   database, queue, storage. Every box labelled, every arrow directed.
6. **The deep dive** — pick the one hard part and go all the way into it. Feed fan-out.
   Seat locking. Video transcoding. Driver-location updates. This is the part that decides
   the interview, and every prompt has exactly one.

### §6 · The numbers

Not optional and not vague. Show the multiplication for:

- daily active users → requests per second, average and peak
- records per day → bytes per record → storage per year
- read-to-write ratio, and what it implies about caching
- bandwidth, where media is involved

### §7 · The trade-offs

Where this design gives up consistency, and what the user sees when it does. What breaks
at ten times the scale. What you would build first if you had six weeks.

---

## §8 for both

The interview section on a case study day is a **timed script**:

- **Minutes 0-5** — requirements and scope.
- **Minutes 5-10** — estimation, out loud.
- **Minutes 10-15** — API and data model.
- **Minutes 15-30** — the architecture diagram, drawn while narrating.
- **Minutes 30-40** — the deep dive on the one hard part.
- **Minutes 40-45** — bottlenecks, failure modes, what you would do next.

Then the three follow-ups this specific prompt always gets. "What about a celebrity with
fifty million followers." "What if two users book the last seat at the same instant."
"How do you handle a region going down." Answer each in three or four sentences.

---

## The rule that matters most here

**Never present the finished design as if it appeared fully formed.** Show the first
version, name what breaks, then show the fix. The reader is learning a way of thinking,
not memorising a diagram — and an interviewer can tell the difference in one question.
