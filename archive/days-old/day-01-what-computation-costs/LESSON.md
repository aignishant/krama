# Day 1 — What computation costs: the machine we pretend to have

> You are about to spend 230 days making claims like "this is O(n log n)". Today: what exactly
> is the thing being counted, and on what machine?

**Owns:** `CPX-01` · `CPX-02`  |  **Phase 1 — Computation and Cost**

---

## 1. The question of the day

Everyone can recite that binary search is O(log n). Far fewer can answer the two questions
underneath it: *log n of what*, and *counted on what machine*.

These are not philosophical questions. They decide real answers. Is multiplying two integers one
step? On a CPU with 64-bit registers and inputs under 2⁶³, yes. In Python, where integers grow
without bound and multiplying two 10,000-digit numbers is genuinely expensive, no — and any
complexity analysis that assumed it was constant is now wrong by a factor that grows with your
input. Is reading `a[i]` the same cost for every `i`? On paper yes; on hardware, an access that
hits L1 cache and one that misses to main memory differ by roughly two orders of magnitude.

So before any algorithm, this: the definition of the object being analysed, and the definition of
the machine it is analysed on. Both are fictions we agree to. Today you learn precisely which
fictions, and — more usefully — where each one leaks.

---

## 2. The map

Read in this order.

| Part | Title | The idea | ID |
|---|---|---|---|
| [1.1](parts/01-algorithm-and-specification/1.1-what-an-algorithm-actually-is.md) | What an algorithm actually is | A finite list of unambiguous steps an executor with no judgement can follow. | `CPX-01` |
| [1.2](parts/01-algorithm-and-specification/1.2-specification-versus-procedure.md) | Specification vs procedure | One specification admits many algorithms with wildly different costs; naming a result is not producing one. | `CPX-01` |
| [2.1](parts/02-model-of-computation/2.1-the-ram-model.md) | The RAM model | The imaginary machine — unit-cost operations, unbounded uniform memory — that every complexity claim is secretly about. | `CPX-02` |
| [2.2](parts/02-model-of-computation/2.2-defining-n.md) | Defining `n` | Input *size* is a choice, and the classic disasters come from counting the wrong thing. | `CPX-02` |
| [2.3](parts/02-model-of-computation/2.3-where-the-fiction-leaks.md) | Where the fiction leaks | Cache hierarchy, arbitrary-precision integers, and the constant factor that mugs you. | `CPX-02` |

**Section 1** is about the *object* — what kind of thing an algorithm is, and how it differs from
a statement of what you want. **Section 2** is about the *measuring instrument* — the model of
computation that makes "number of steps" a meaningful quantity at all.

---

## 3. What you already have

| ID | From | Why it is needed today |
|---|---|---|
| `FND-01` | Day 0 | Clause three — every cost is derived — is the reason this phase is eight days long. |
| `FND-03` | Day 0 | The reading protocol. Today is the day to actually do §5 on paper and §10 cold the next morning. |

Nothing else. This is the floor.

---

## 4. Setup

```bash
./k scaffold 1
```

---

## 5. The build brief

Implement in `days/day-01-what-computation-costs/lab/implement.py`:

```python
def max_and_comparisons(xs: list[int]) -> tuple[int, int]:
    """Return (maximum of xs, number of element-to-element comparisons performed).

    Pre:   xs is non-empty; on an empty list, raise ValueError.
    Post:  result[0] == the largest value in xs.
           result[1] == len(xs) - 1, exactly, whatever the values are.
    Time:  Theta(n), one pass.
    Space: Theta(1) auxiliary.
    """
```

**Forbidden today:** `max`, `min`, `sorted`, `list.sort`, `heapq`, `numpy`, `functools.reduce`.
Every one of them is a way of naming the result instead of producing one — which is what
[1.2](parts/01-algorithm-and-specification/1.2-specification-versus-procedure.md) is about.
The whole point is that you are the procedure.

The test suite does not take your word for the count. It hands your function elements that keep
their own tally of every ordering comparison they take part in, so `return sorted(xs)[-1],
len(xs) - 1` fails — right answer, wrong procedure. Read `lab/test_implement.py` before you start;
knowing what will be checked is not cheating, it is the contract.

Then answer the question the counter exists to ask: **run it on a hundred random lists of length
50 and look at the comparison counts.** They are all identical. Why? What does that tell you
about best case and worst case for this particular problem — and what would you have to change
about the procedure for the count to start varying?

Then the harder one, which Day 3 will formalise: can you write a procedure that finds the maximum
using *fewer* than `n - 1` comparisons? Try to. Failing to, and understanding *why* you failed,
is worth more than today's code.

Done when `uv run pytest days/day-01-what-computation-costs/lab -q` is green and
`bench.py`'s ratio column sits near 2.

---

## 6. The problem ladder

Selected from [`docs/PROBLEM_INDEX.md`](../../docs/PROBLEM_INDEX.md) — run `./k ladder CPX` to see
the catalogue. Phase 1 is a modelling phase, so every rung is written rather than judged: `own`
means paper, a REPL, or today's `lab/`. What is being graded is whether you can state something
precisely.

**Warm-up** — fire the mechanism once.
- *Specification or procedure? — twelve statements* (own) — testing: sorting statements into "says
  what must be true at the end" and "says what to do next".
- *Which of these is one operation?* (own) — testing: the rule that a step may be charged 1 only if
  its cost does not grow with `n`.

**Core** — solve from an empty file, without re-reading the lesson.
- *Second largest, tie policy stated first* (own) — testing: naming a result vs producing one;
  deciding `[7, 7]` and `[7]` before writing a line.
- *Count the model operations of a reversal* (own) — testing: charging every read, write and
  comparison, and reaching a closed form.
- *What is `n` here? — eight inputs* (own) — testing: choosing the size parameter for a grid, a
  graph, a string, and a single integer.

**Stretch** — today's ideas combined. Day 1 is the floor, so the only earlier IDs available are
Day 0's; the first entry combines today's two with each other, the second reaches back to `FND-02`.
- *Trial division, priced in digits* (own) — combines `CPX-02` with `CPX-01` — testing: polynomial
  in the value, exponential in the size.
- *The cache cliff, measured* (own) — combines `CPX-02` with `FND-02`, because you have to build
  and seed the harness yourself — testing: identical operation counts in two orders, and the size
  at which the ratio moves.

**Interview** — narrate aloud before you type.
- *One specification, three procedures* (own) — testing: producing three procedures for one
  specification and stating the cost gap out loud.

---

## 7. The gate

Say these out loud, without notes:

1. State the five properties of an algorithm, and give a procedure that has four of them.
2. What is the difference between a specification and an algorithm? Give an example where one
   specification has two procedures whose costs differ enormously.
3. Why can a specification be cheap to *check* and expensive to *satisfy*? Give the example from
   1.2 without using the word blood.
4. State the RAM model in three assumptions.
5. When may a step be charged as one operation? Then name three Python expressions that look like
   one operation and are not, and say what each really costs.
6. `n` for a graph problem: what is it, and why is that answer different from every other day this
   phase?
7. Trial division runs in `Θ(√m)`. Explain, to someone who thinks that sounds fast, why it is
   exponential.
8. Two procedures execute an identical number of operations on identical data, and one is
   thirteen times slower. Name the assumption that failed, and name the *size* at which it starts
   to fail on your own machine.
9. Your `max_and_comparisons` always reports the same count. Explain why in terms of the
   procedure's structure, not by re-reading its code. Then say what that property is called.

Then:

```bash
./k done 1
```

Tomorrow: `CPX-03` — loop invariants, and how to prove that a procedure does what you claim.
