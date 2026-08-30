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

Read three small files. They are compiled from the finished lessons by `./k wiki`, so
they say what the reader has actually met, not what the syllabus planned.

```bash
cat wiki/00-STATE.md                    # which days are written, and their titles
cat wiki/vocab.md                       # every term the reader knows, and its day
cat wiki/recall/<phase>.md              # the recall cards for this day's two phases
```

`./k day <N>` names both phases; take the slugs from there. Read only those two recall
files — the others belong to phases the reader has not reached, or finished long ago.

You may use any term in `wiki/vocab.md`, and you should link to the day it arrived. You
may **not** use a term that is not there. Define it, or drop it. The ledger prefers
precision to completeness: if a term you need is missing, define it again rather than
assume.

Do **not** open `docs/CURRICULUM_INDEX.md` for this. It is the plan, not the state, and
it costs six thousand tokens to say what `./k day <N>` already told you.

This matters more than anything else in this file. The single most common failure is
writing for someone who already knows the subject.

### Step 3 · Write the DSA lesson

Nine sections, in order, no exceptions. Full guidance in
[`reference/lesson_contract.md`](reference/lesson_contract.md). The short version:

1. **What this is, and why they ask it** — three sentences, then why it appears in interviews.
2. **The story** — 200-400 words, a person, a scene almost anyone has lived, **zero
   technical words**. Simple vocabulary, realistic detail, no paper props.
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

### Step 6 · Leave the hub alone

`README.md` is generated from the syllabus on every build. Do not hand-edit it — your
changes will be overwritten. If it is wrong, the syllabus is wrong: fix
`scripts/curriculum.py` and run `./k build`.

Never rename a lesson file either. The filename is derived from the topic, and the hub
links to the derived name.

### Step 7 · Check

```bash
./k check <N>
./k wiki
```

`check` verifies the nine sections are present and in order, that the story is long enough
and carries no jargon, that the interview section is not thin, and that every link you
made points at a folder that exists. `wiki` folds your new lesson into the ledger the next
day will read. Fix what they report. Then
read section 2 of both lessons out loud — if it does not sound like a story about a
person, rewrite it.

---

## Hard stops

- **Never create a `lab/` folder**, an `implement.py`, a `reference.py`, a test file or a
  benchmark script. Rule 10. That structure was removed on purpose.
- **Never write only one of the two lessons.** Rule 2.
- **Never ask the reader to reach for paper.** Rule 15. No "draw this on paper", no "on a
  blank page", no "pen and paper" — in the lessons, in §9, or in the practice checklist.
  Say it out loud from memory, or draw it in any tool. Stories use a phone, not a diary.
- **Never leave `status: empty` in the front matter** of a file you have written.
- **Never hand-edit** `docs/CURRICULUM_INDEX.md`, `days/README.md`, or anything under
  `wiki/`. They are generated. `wiki/` is rebuilt by `./k wiki`; run it after writing a
  day so the next day sees your vocabulary.
- **Never compress to save space.** If it is too long, split it into a folder of numbered
  parts. Depth over density.
- **Never include formal proofs, potential functions, or language-internals detail** unless
  an interviewer would ask for it. Rule 14.

## Tone

Second person, present tense. Short sentences, one idea each. Concrete numbers before
variables. No cheerleading, no emoji in body text, no study-time estimates. Admit the hard step
instead of glossing it: "this is the part people get wrong, and here is why it looks right".

Write it as prose, not as notes. Full sentences, correct grammar, and the commas and full
stops actually in place. The reader is a beginner meeting the idea for the first time, and
a sentence they have to read twice is a sentence that failed.
