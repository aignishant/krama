# Writing a Track II (system design) day — Days 231–308

Everything in `SKILL.md` still applies: plan the split first, one document per subtopic, the ten
sections, the hub last, `./k depth N` at the end. This file covers only what is *different*.

## What stays exactly the same

The ten sections, in order, with the same failure conditions. Especially §2 (the story — a scene,
no jargon) and §8 (the real failure, reproduced). Design content is where hand-waving is easiest
and the contract exists to prevent it.

## What changes, section by section

**§4 Where this actually shows up** — for design days this must name **the system and the
version or the incident**. Not "many databases use MVCC" but "PostgreSQL's MVCC keeps old row
versions in the heap, which is why `VACUUM` exists and why a long-running transaction can bloat a
table." Public postmortems are gold here.

**§6 Line by line** — often there is no algorithm to write. Replace the code fragments with one
of these, and say which you are using:
- a **configuration** read line by line (a replication config, a Kafka topic config, an index
  definition) with the same "why this value and not the obvious alternative" prose;
- a **protocol trace** — the actual message sequence, step by step;
- a **small runnable simulation** — a hundred lines that demonstrates the phenomenon (replication
  lag, a thundering herd, quorum arithmetic) and can be run.
The near-miss requirement still holds: show the configuration or the sequence that looks right and
is subtly wrong.

**§7 The cost, derived → the arithmetic, shown.** This is the biggest change and the most
important. Design days replace complexity derivation with capacity derivation, and it must be
*shown*, never asserted:

```
100M daily active users × 20 reads/day        = 2 × 10⁹ reads/day
2 × 10⁹ / 86,400                              ≈ 23,000 QPS average
peak factor 3×                                ≈ 70,000 QPS
per record: 200 B payload + 60 B overhead     = 260 B
2 × 10⁹ writes/year × 260 B                   ≈ 520 GB/year before replication
× 3 replicas                                  ≈ 1.6 TB/year
```

Every design document states: QPS (average and peak), bytes per record, storage per year, and the
read:write ratio. If the day's subject makes one of those meaningless, say so explicitly rather
than omitting it silently.

**§9 In production** — keep all three blocks. The reviewer quote becomes a **design-review**
quote, and the three interviewer probes become the three follow-ups a staff engineer asks in a
design round. Where a real public postmortem exists, cite it.

**§10 Check yourself** — the "break it" question becomes: *what fails first, and what does the
user see while it fails?*

## The drill ladder replaces the problem ladder

Track II hubs use four different rungs:

| Rung | What goes in it |
|---|---|
| **Recall** | The numbers and the vocabulary, from memory. Latency figures, isolation anomalies, quorum arithmetic, the delivery semantics. |
| **Read** | Exactly one primary source, with the specific section named — a paper, an engineering blog post, or the actual documentation. Never a listicle. |
| **Drill** | One design prompt from `docs/PROBLEM_INDEX.md`'s drill bank, timed, narrated aloud, requirements first. |
| **Critique** | Break a design — usually the learner's own, from an earlier day. Use one of the critique prompts at the end of the problem index. |

The critique rung is mandatory. It is the one people skip and the one that separates a design
engineer from someone who has memorised fifteen templates.

## The hinge days

Days 210–214 (`SYS`) taught LRU, B-trees, LSM trees, cache-obliviousness and consistent hashing as
**structures**. Track II revisits them as **components**. When writing Days 246, 247 and 278,
open the Track I day first and *build on it by ID* — do not re-teach the structure. The Track II
document's job is what changes when the structure is replicated, partitioned, and failing.

## Common failure modes specific to design days

| Failure | Fix |
|---|---|
| **The template** | "Requirements, then API, then database, then cache, then CDN" recited regardless of the problem. Make the day's structure follow the *problem's* pressure point. |
| **The unnamed tradeoff** | "We'll use Cassandra." Every technology choice states what is given up, in the same sentence. |
| **Numberless scale** | "This needs to handle a lot of traffic." §7 exists to make this impossible. |
| **The happy path only** | No design document is complete without the failure case and what the user sees during it. |
| **Buzzword depth** | Using "eventually consistent" without saying *how eventually*, and what a reader can observe in the window. |
