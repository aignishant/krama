---
name: day-krama
description: Write a Krama day — the hub README, the DSA lesson, the system design lesson and the practice sheet, all under the nine-section format contract. Use this skill whenever the user asks to write, generate, draft, expand, rewrite, fix or review any day in days/, mentions a day number ("do day 37", "write the binary search day", "day 102 is thin"), asks for a lesson or a practice sheet, asks anything about the nine-section contract, or asks for a system design day or case study. Use it even when they phrase it casually as "next day please" or "continue the course".
---

# Writing a Krama day

You are producing the teaching material for one day of a 180-day course. The reader is a
**complete beginner** preparing for **DSA and system design interviews at product
companies**. They read only these documents. If an idea is not in them, they never meet it.

Every day carries **two lessons**: one DSA, one system design. You write both. Never one.

**Read first, every time:** [`docs/00_HOW_A_DAY_WORKS.md`](../../../docs/00_HOW_A_DAY_WORKS.md)
and [`CLAUDE.md`](../../../CLAUDE.md).

---

## The procedure

### Step 1 · Read the assignment

```bash
./k day <N>
```

That prints the hub, which already names both topics, both "after today you can" lines,
and both interviewer questions. Those four lines are your brief — the syllabus decided
them, not you. Do not change the topic. If it is genuinely wrong, stop and say so; the
fix is an edit to `scripts/curriculum.py` in its own commit.

Also open the two placeholder lesson files. They carry the nine headings already.

### Step 2 · Check what the reader already knows

Skim the hubs of the previous five days and the phase this day sits in
(`docs/CURRICULUM_INDEX.md`). You may use any term an earlier day defined — link to that
day when you do. You may **not** use a term nobody has defined yet. Define it or drop it.

This matters more than anything else in this file. The single most common failure is
writing for someone who already knows the subject.

### Step 3 · Write the DSA lesson

Nine sections, in order, no exceptions. Full guidance in
[`reference/lesson_contract.md`](reference/lesson_contract.md). The short version:

1. **What this is, and why they ask it** — three sentences, then why it appears in interviews.
2. **The story** — 200-400 words, a person, ordinary life, **zero technical words**.
3. **The idea in plain English** — map the story onto the technical idea, defining terms.
4. **The picture** — ASCII for arrays and memory, Mermaid for trees and graphs. Captioned.
5. **The code, built step by step** — fragments of ten lines or fewer, each explained,
   then the **complete working solution**. Show the answer. Rule 5.
6. **What it costs** — count the loops out loud. Time and space separately.
7. **The traps** — the near-miss that looks right plus the input that kills it, and
   **real pasted error text**.
8. **In the interview** — real phrasings, a ninety-second script, three follow-ups with
   answers, and a written-out model answer. This is why the document exists.
9. **Recall card** — five lines, maximum.

### Step 4 · Write the system design lesson

Same nine headings; sections 5, 6 and 7 differ:

5. **How it actually works** — the mechanics, and the real products that do it this way.
   Name them: Redis, Kafka, Postgres, S3, Cassandra.
6. **The numbers** — show the multiplication. `50M users × 20 posts × 2KB = 2TB`.
   Never "a lot of data".
7. **The trade-offs** — what you give up, and when you would pick something else.

For a **case study day** (design a parking lot, design Twitter), read
[`reference/case_study_day.md`](reference/case_study_day.md) before writing.

### Step 5 · Write the practice sheet

`03-practice.md`. Named problems only — title, source, and one line on what it is really
testing. Never paste a problem statement. Four problems, easiest first, and they must be
findable (LeetCode number, or the standard name).

Then three questions to answer out loud. Two are already in the file; write the third.

### Step 6 · Fill in the hub

The hub is generated and mostly correct already. Update only the "Read in this order"
filenames if you renamed a lesson file, and remove nothing.

### Step 7 · Check

```bash
./k check <N>
```

It verifies the nine sections are present and in order, that the story is long enough and
carries no jargon, and that the interview section is not thin. Fix what it reports. Then
read section 2 of both lessons out loud — if it does not sound like a story about a
person, rewrite it.

---

## Hard stops

- **Never create a `lab/` folder**, an `implement.py`, a `reference.py`, a test file or a
  benchmark script. Rule 10. That structure was removed on purpose.
- **Never write only one of the two lessons.** Rule 2.
- **Never leave `status: empty` in the front matter** of a file you have written.
- **Never hand-edit** `docs/CURRICULUM_INDEX.md` or `days/README.md`. They are generated.
- **Never compress to save space.** If it is too long, split it into a folder of numbered
  parts. Depth over density.
- **Never include formal proofs, potential functions, or language-internals detail** unless
  an interviewer would ask for it. Rule 14.

## Tone

Second person, present tense. Short sentences, one idea each. Concrete numbers before
variables. No cheerleading, no emoji in body text, no time estimates. Admit the hard step
instead of glossing it: "this is the part people get wrong, and here is why it looks right".
