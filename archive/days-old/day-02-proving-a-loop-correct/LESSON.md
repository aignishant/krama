# Day 2 — Correctness: loop invariants and termination

> Yesterday you learned to count what a procedure costs. Today: how do you know it is right — and
> how do you know it stops?

**Owns:** `CPX-03`  |  **Phase 1 — Computation and Cost**

---

## 1. The question of the day

Ask most people why their loop is correct and they will run it for you. "So `i` is zero, `total` is
zero, then we add four…" That is a trace of one input. It says nothing whatsoever about the input
you did not pick, and the inputs you do not pick are where the bugs live.

There is an argument that covers every input at once, it is four sentences long, and it is older
than every language you will ever write in. Three of the sentences say what the loop keeps true and
what that entitles you to conclude when it stops. The fourth says why it stops at all — a separate
claim, with a separate witness, that most people never make and cannot supply when asked.

By the end of today you can look at a loop you have never seen and say: here is what it keeps true,
here is why the first iteration starts it true, here is why the body preserves it, here is what the
guard going false adds, and here is the quantity that shrinks. You will also be able to tell the
two failure modes apart by symptom alone — because a program that returns a wrong answer and a
program that never returns are debugged in completely different ways, and the second one arrives on
your desk with no evidence at all.

---

## 2. The map

Read in this order.

| Part | Title | The idea | ID |
|---|---|---|---|
| [1.1](parts/01-invariants-and-induction/1.1-initialization-and-maintenance.md) | Initialization and maintenance | A claim you make true before the loop and that every iteration leaves true — induction over iterations. | `CPX-03` |
| [1.2](parts/01-invariants-and-induction/1.2-exit-and-negated-guard.md) | Exit, and the negated guard | The invariant alone proves nothing; the answer comes from the invariant *and* the reason the loop stopped. | `CPX-03` |
| [2.1](parts/02-termination-and-measure/2.1-measure-that-decreases.md) | The measure that decreases | A non-negative whole number that gets strictly smaller every pass is why the loop ends — and how long it runs. | `CPX-03` |
| [2.2](parts/02-termination-and-measure/2.2-partial-versus-total-correctness.md) | Partial versus total correctness | "Right if it stops" and "it stops" are two promises, and they fail with two different symptoms. | `CPX-03` |

**Section 1** is about what stays **true** — the invariant, its two proof obligations, and the exit
argument that turns it into an answer. **Section 2** is about what **shrinks** — the variant, and
what you are entitled to claim once you have one. The two sections are two different obligations on
the same loop, and the most common mistake in this day is to think the first one implies the second.

---

## 3. What you already have

| ID | From | Why it is needed today |
|---|---|---|
| `CPX-01` | [Day 1](../day-01-what-computation-costs/LESSON.md) | Finiteness was one of the five properties of an algorithm, and correctness was explicitly *not*. Today supplies both missing arguments. |
| `CPX-02` | [Day 1](../day-01-what-computation-costs/LESSON.md) | The variant bounds the iteration count, so every termination proof hands you a cost derivation — priced in the RAM model, with the same leaks. |

---

## 4. Setup

The lab ships written, so `./k scaffold 2` will refuse rather than overwrite it. Go straight to:

```bash
uv run pytest days/day-02-proving-a-loop-correct/lab -q
```

Every test skips while `implement.py` is a stub. That is the starting state, and it is correct.

---

## 5. The build brief

Implement in `days/day-02-proving-a-loop-correct/lab/implement.py`:

```python
def divide(a: int, b: int) -> tuple[int, int, int]:
    """Divide by repeated subtraction. Return (quotient, remainder, iterations).

    Pre:   a >= 0 and b >= 1; otherwise raise
           ValueError("divide() requires a >= 0 and b >= 1").
    Post:  quotient * b + remainder == a, and 0 <= remainder < b.
           iterations == the number of times the body ran.
    Time:  Theta(a / b) iterations.
    Space: Theta(1) auxiliary.
    """
```

**Forbidden today:** `//`, `%`, `/`, `divmod`, `math`, `round`, `pow`, `abs`. Every one names the
quotient instead of producing it, and with any of them present there is no loop, so there is nothing
to prove. `test_forbidden_shapes.py` reads your file's syntax tree and says so. You have `-`, `+`,
`<`, `>` and a `while`.

Before you type a line, write these two sentences on paper:

```
invariant: quotient * b + remainder == a, and remainder >= 0
variant:   remainder — a non-negative integer, strictly smaller after every pass
```

Then write the body so that each statement discharges one of them, and be able to point at which
line does which. That pointing is the day.

Then do the three experiments the tests are built around:

1. Put `assert quotient * b + remainder == a` at the **top** of the loop and watch it pass on every
   iteration. Move it to **between** the two statements of the body and watch it fail. Say out loud
   why the second placement proves nothing — [1.1](parts/01-invariants-and-induction/1.1-initialization-and-maintenance.md) §3.
2. Change the guard from `>=` to `>` and run the tests. Read that failure: the loop stopped and
   returned a remainder equal to the divisor. That is a **partial-correctness** failure, and it
   comes with an input, an expected value and a line number.
3. Change the guard to `!=` and call `divide(10, 3)`. That one hangs. Interrupt it, and compare the
   traceback with [2.1](parts/02-termination-and-measure/2.1-measure-that-decreases.md) §8 — the
   named line is a guard, not work, which is the signature you are learning to recognise.

Done when `uv run pytest days/day-02-proving-a-loop-correct/lab -q` is green and
`uv run python days/day-02-proving-a-loop-correct/lab/bench.py` shows the first table's ratio near
2.00 while the second table's iteration count does not move at all.

---

## 6. The problem ladder

Selected from [`docs/PROBLEM_INDEX.md`](../../docs/PROBLEM_INDEX.md) — run `./k ladder CPX-03` to see
the catalogue. Phase 1 is a modelling phase, so every rung is written rather than judged: `own`
means paper, a REPL, or today's `lab/`. What is graded is whether you can state something precisely.

**Warm-up** — fire the mechanism once.
- *Prove the maximum you wrote on Day 1* (own) — testing: writing initialization, maintenance and
  exit for a loop you already trust.
- *Invariant for a loop you did not write* (own) — testing: stating the invariant of three
  unfamiliar loops from the code alone, before running them.

**Core** — solve from an empty file, without re-reading the lesson.
- *Where the invariant first breaks* (own) — testing: naming the exact iteration at which a proposed
  invariant stops being preserved.
- *Exit condition, negated* (own) — testing: deriving the postcondition from invariant and the
  negated guard, and noticing when it does not follow.
- *Find the variant — five loops* (own) — testing: naming the decreasing measure for each, and
  identifying the one loop that has none.

**Stretch** — today's idea combined with an earlier ID.
- *The strongest true invariant* (own) — combines `CPX-03` with `CPX-01`, because "strong enough"
  means "implies the specification", and the specification is Day 1's word — testing: strengthening
  a preserved-but-useless claim until it implies the postcondition.
- *The loop that stops for the wrong reason* (own) — combines `CPX-03` with `CPX-02`, because the
  measure you trusted was priced in the wrong quantity — testing: termination resting on a value the
  invariant never mentions, and what breaks when the input changes.

**Interview** — narrate aloud before you type.
- *Partial, total, and the bug report* (own) — testing: telling a wrong-answer failure from a
  never-returns failure by symptom alone, out loud.

---

## 7. The gate

Say these out loud, without notes:

1. State the two obligations that make up an invariant proof, and say which one is usually skipped
   and why it looks like it is saying nothing.
2. Someone asserts your invariant in the middle of your loop body and it fails. Are they right? Give
   the answer and the reason in two sentences.
3. Write the loop-proof obligation in symbols, all three parts, and say which part turns a claim
   about the finished portion into a claim about the whole input.
4. A loop leaves by a `while` guard and by a `return` in the middle. How many things must you prove,
   and are they the same thing?
5. State the three requirements on a variant. Then give a quantity that strictly decreases forever
   and say which requirement it fails.
6. Where is the variant of `for i in range(len(xs)):`?
7. Your measure starts at `n` and falls by at least one per iteration. Is the loop linear? Now the
   measure starts at `n` and halves. Same question, and say what changed in the argument.
8. Define partial and total correctness in one sentence each, and say which one Section 1 of today
   proved.
9. A colleague reports "the build hangs sometimes". Before you look at anything, what class of bug
   is that, and what will the traceback point at if you interrupt it?
10. You cannot find a variant for a loop you have to ship. Name the two legitimate moves, and say
    what each one costs.

Then:

```bash
./k done 2
```

Tomorrow: `CPX-04` and `CPX-05` — growth, and why the answer to "how fast is it" is a shape rather
than a number.
