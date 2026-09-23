# How a Krama day works

This is the format contract. Every one of the 360 lessons follows it.

---

## Who this is written for

Someone who has **never studied this before**. Not a computer science graduate.
Not someone brushing up. Someone who has to be told what a server is, and who will
be sitting in a product-company interview at the end of 180 days.

That single fact decides everything below.

---

## The prime directive

> **Every lesson answers one question an interviewer could actually ask,
> and leaves you able to answer it out loud, from memory, to a stranger.**

If a paragraph does not move you toward saying the answer out loud, it does not belong
in the file.

---

## The shape of a day

```
days/day-NNN-<topic>/
    README.md                       the hub — what today is, in one screen
    01-dsa-<topic>.md               the DSA lesson
    02-system-design-<topic>.md     the system design lesson
    03-practice.md                  problems to code, questions to say out loud
```

Four files. Nothing else. No `lab/`, no test harness, no benchmark script, no oracle.

Both tracks run in parallel from day 1 to day 180, so you are never doing only one of
them. The DSA track goes foundations → patterns → data structures → algorithms. The
system design track goes fundamentals → databases → object-oriented design → low-level
design → distributed systems → high-level design.

---

## The nine sections

Every lesson carries all nine, in this order. Both tracks share sections 1-4 and 8-9,
so you only ever learn one reading rhythm. Sections 5, 6 and 7 differ.

| # | DSA lesson | System design lesson |
|---:|---|---|
| 1 | What this is, and why they ask it | What this is, and why they ask it |
| 2 | The story | The story |
| 3 | The idea in plain English | The idea in plain English |
| 4 | The picture | The picture |
| 5 | The code, built step by step | How it actually works |
| 6 | What it costs | The numbers |
| 7 | The traps | The trade-offs |
| 8 | In the interview | In the interview |
| 9 | Recall card | Recall card |

### 1. What this is, and why they ask it

Three sentences saying what the idea is, then one short paragraph on why this shows up
in interviews. Name the companies or the round type if it is specific.

No build-up. The reader should know what they are learning by the end of the first line.

### 2. The story

A scene from ordinary life, 200-400 words, with a person in it, where this idea already
exists without anyone calling it by its technical name. Matching socks after the laundry.
A queue at a canteen counter. Laying tables before a wedding.

**Pick a scene almost anyone has lived.** Not a trade the reader has never seen. If the
scene only works for someone who has run a particular kind of shop, or kept a particular
kind of record, it is the wrong scene. The reader should recognise it in the first line.

**Simple words, and realistic detail.** Short sentences. The kind of vocabulary you would
use talking to a friend. Real numbers, real times of day, and the small true details that
make a scene rather than an example — what he is holding when he stops, what time the
shutters went up.

**No jargon. No code. No technical vocabulary at all.** Not one word.

**No paper props.** If the person in the story has to store something, they save it in
their phone. See the writing rules below.

The test: if you delete this section and lose nothing, it was decoration, not a story.

### 3. The idea in plain English

Take the story apart and map each piece onto the technical idea, one step at a time.
This is where the technical words are introduced — each one defined the first time it
appears, in a sentence a fifteen-year-old could read.

Concrete before abstract, always. A seven-element array before "an array of size n".
The number 5 before the variable `k`.

### 4. The picture

At least one diagram, captioned with what to notice in it.

- **ASCII boxes** for arrays, memory, pointers, bit patterns — anything where adjacency
  is the point. Indices above, values below, boundaries marked.
- **Mermaid** for trees, graphs, architectures, state machines, request flows.

### 5. The code, built step by step *(DSA)*

Small fragments, **ten lines or fewer**, each followed by prose explaining what it does
and why. Never a forty-line block with a comment on top.

Then the complete, working, copy-pasteable solution at the end of the section. Python
3.12+, type hints on the signature, comments on the lines that are not obvious.

**Show the whole solution.** This repository does not hide answers from you.

### 5. How it actually works *(system design)*

The mechanics. What the component really does, what it stores, what happens on failure,
and which real products work this way. Name them: Redis, Kafka, Postgres, S3, Cassandra.

### 6. What it costs *(DSA)*

Time and space, counted out from the loops in front of you. Show the counting:
"the outer loop runs n times, the inner loop runs n times for each of those, so n × n".

State the space separately, and say whether it is extra space or total space.

### 6. The numbers *(system design)*

The arithmetic, with the multiplication shown. Users → requests per second. Records →
bytes → storage per year. Fan-out multipliers. Replica counts.

"It will be a lot of data" is not an answer. `50M users × 20 posts × 2KB = 2TB` is.

### 7. The traps *(DSA)*

At least two:

- **The near-miss** — the version that looks correct, and the exact input that kills it.
- **The real error** — actual pasted output, never a paraphrase.
  `IndexError: list index out of range`, not "you get an index error".

### 7. The trade-offs *(system design)*

What you give up by choosing this. When you would choose something else instead. The
sentence that begins "I would not use this if..." is the one that separates candidates.

### 8. In the interview

The section the whole document exists for.

- **How it gets asked** — two or three real phrasings.
- **What to say out loud** — a script for the first ninety seconds.
- **The follow-ups** — the three questions that come next, with short answers.
- **A model answer** — what a strong candidate actually says, written out.

### 9. Recall card

Five lines, maximum. What survives if you forget everything else. This is what you
re-read the night before the interview.

---

## Writing rules

- **Second person, present tense.** "You keep two pointers." Never "we will now consider".
- **Short sentences, one idea each.** The subject is hard; the prose must not be.
- **Define every term the first time it appears.** No unearned vocabulary — if a word has
  not been defined in this lesson or an earlier day, define it here or do not use it.
- **No cheerleading.** No "Great!", no "Now for the fun part!", no emoji in the body.
- **Admit difficulty.** "This is the step people get wrong, and here is why it looks
  right" is worth more than confidence.
- **No study-time estimates.** No "≈45 minutes to read", no "quick". A day is a unit of
  subject. Timing a drill is different and is allowed — that is the interview clock.
- **Grammar and punctuation are part of the job.** Full sentences. Commas where the sense
  needs them, full stops at the end of them. A dropped comma makes a beginner re-read a
  line, and re-reading is the thing this course exists to prevent.
- **No paper, anywhere.** Never ask the reader to draw it on paper, write it on a blank
  page, or work it through with pen and paper. The compliant versions are "say it out loud
  from memory", "name the six beats in order without looking", or "draw it in any tool you
  like". This applies to lesson prose, to §9, and to every checklist in `03-practice.md`.
- **British/Indian-neutral English**, consistent within a file.

## When a lesson gets long

Depth over density. A long lesson is fine. If it genuinely will not fit in one file,
split it into a folder:

```
01-dsa-<topic>/
    1-<part>.md
    2-<part>.md
```

Do **not** compress. Compressing is how the material got too hard the first time.

---

## Generating and checking

```bash
python scripts/build_skeleton.py     # create any missing day folders and placeholders
./k status                           # how many lessons are written
./k check N                          # does day N follow the nine-section contract
```

The syllabus itself lives in [`scripts/curriculum.py`](../scripts/curriculum.py). To change
what a day teaches, edit that file and re-run the builder — never rename a folder by hand.
