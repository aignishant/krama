# Day 3 — Growth: why we count shapes, not seconds

> Two programs, two machines, two stopwatches. What is the number you can write down that will
> still be true on a machine nobody has built yet?

**Owns:** `CPX-04` · `CPX-05`  |  **Phase 1 — Computation and Cost**

---

## 1. The question of the day

You can now count a procedure's operations (`CPX-02`) and prove that it does what you claim
(`CPX-03`). Today is the step that turns a count into a comparison.

The obstacle is that the obvious comparison — time it — measures the wrong thing. A stopwatch
reading is a fact about a processor, an interpreter, a cache, a moment, and one particular input.
Run the same code on the machine next to it and every digit changes. So the industry compares
something else: not how long a procedure takes, but **how its cost grows when the input grows**,
because that quantity survives multiplication by any constant and therefore survives changing the
machine.

Then comes the price of the abstraction, which is what most courses skip. Dropping the constant
deletes the number that decides how many servers you buy. Saying "grows faster" is a claim about
inputs larger than some threshold, and the threshold can be past anything you will ever run. By the
end of today you can state a bound formally, prove it by producing two numbers, disprove somebody
else's, and — the part that separates an engineer from a reciter — say precisely what your bound
does *not* tell you.

---

## 2. The map

Read in this order.

| Part | Title | The idea | ID |
|---|---|---|---|
| [1.1](parts/01-from-seconds-to-shapes/1.1-seconds-do-not-travel.md) | Seconds do not travel | A measurement describes a machine on a day; the ratio between doubled sizes describes the algorithm. | `CPX-04` |
| [1.2](parts/01-from-seconds-to-shapes/1.2-eventual-dominance.md) | Eventual dominance and the crossover | "Grows faster" is a claim about the tail, and the crossover is where it starts being true. | `CPX-04` |
| [1.3](parts/01-from-seconds-to-shapes/1.3-what-dropping-constants-destroys.md) | What dropping constants destroys | The growth class keeps the ranking and deletes the invoice. | `CPX-04` |
| [2.1](parts/02-asymptotic-notation/2.1-big-o-and-its-witness.md) | Big-O and its witness | `f = O(g)` is proved by exhibiting a multiplier and a threshold — a witness pair. | `CPX-05` |
| [2.2](parts/02-asymptotic-notation/2.2-omega-theta-and-the-abuse-of-o.md) | Omega, Theta, and the abuse of O | A ceiling is not a description; `O(n²)` is true of a linear loop, and `Θ` is the claim worth making. | `CPX-05` |

**Section 1** is the *argument*: why a shape is the portable part of a cost, what it costs you to
work in shapes, and where the abstraction lies to you. **Section 2** is the *notation*: the formal
definitions, how to prove and disprove a claim in them, and the four ways they are misused.

---

## 3. What you already have

| ID | From | Why it is needed today |
|---|---|---|
| `CPX-01` | [Day 1](../day-01-what-computation-costs/LESSON.md) | One specification, many procedures — today is how you compare those procedures without running them. |
| `CPX-02` | [Day 1](../day-01-what-computation-costs/LESSON.md) | The operation count, and what `n` is. Every bound today is a bound on that count, and every leak in the model is a leak in the bound. |
| `CPX-03` | [Day 2](../day-02-proving-a-loop-correct/LESSON.md) | A variant bounds the iteration count, which is where most of your `O` claims will come from — and 2.2 explains why it can never give you a `Θ`. |

---

## 4. Setup

The lab ships written, so `./k scaffold 3` will refuse rather than overwrite it. Go straight to:

```bash
uv run pytest days/day-03-counting-shapes-not-seconds/lab -q
```

Every test skips while `implement.py` is a stub. That is the starting state, and it is correct.

---

## 5. The build brief

Implement in `days/day-03-counting-shapes-not-seconds/lab/implement.py`:

```python
def dominates_from(f: list[int], g: list[int], c: int) -> int | None:
    """The smallest index from which f[n] <= c * g[n] holds for the whole tail.

    Pre:   len(f) == len(g); g[i] >= 0; c >= 0. On unequal lengths, raise
           ValueError("dominates_from() requires tables of equal length").
    Post:  None, or the smallest n0 with f[i] <= c*g[i] for every i >= n0.
           Empty tables return 0 -- the empty suffix holds vacuously.
    Time:  Theta(n), one pass.
    Space: Theta(1) auxiliary.
    """
```

This is the `n₀` of a witness pair from [2.1](parts/02-asymptotic-notation/2.1-big-o-and-its-witness.md),
computed on data rather than argued on paper.

**Forbidden today:** slicing (`f[i:]`, `f[::-1]`), `list`, `reversed`, `sorted`, `min`, `max`,
`sum`, `any`, `all`, `itertools`, `numpy`, `bisect`. The first group copies, and the contract is
`Θ(1)` auxiliary space; the second group names a scan instead of performing one, which hides the
only question that matters here — *suffix, or everything?* `test_forbidden_shapes.py` reads your
syntax tree.

The trap is in the specification and not in the code. "The smallest index where the inequality
holds" and "the smallest index from which it holds forever after" are different questions, and a
scan that stops at the first success answers the wrong one. Decide which direction to walk before
you type, write the invariant above the loop, and make sure it mentions the *suffix*.

Then do the experiment the day is really about:

1. Run `bench.py`. Your ratio column should sit near **2.00** and the oracle's near **4.00**.
2. Look at the third column — `oracle / yours`. It is not a constant. It doubles every row. Say out
   loud why that column, rather than either time column, is the thing
   [1.2](parts/01-from-seconds-to-shapes/1.2-eventual-dominance.md) is about.
3. Now find the crossover: shrink `n` until the oracle *wins*. It does, below some size. Write the
   size down. That number is the whole of Section 1 in one measurement.

Done when `uv run pytest days/day-03-counting-shapes-not-seconds/lab -q` is green and
`uv run python days/day-03-counting-shapes-not-seconds/lab/bench.py` shows those two ratio columns.

---

## 6. The problem ladder

Selected from [`docs/PROBLEM_INDEX.md`](../../docs/PROBLEM_INDEX.md) — run `./k ladder CPX-04` and
`./k ladder CPX-05`. Phase 1 is a modelling phase, so every rung is written rather than judged: `own`
means paper, a REPL, or today's `lab/`. What is graded is whether you can state something precisely.

**Warm-up** — fire the mechanism once.
- *The doubling table, read backwards* (own) — testing: naming the growth of six procedures from
  their ratio columns alone.
- *Exhibit the witness* (own) — testing: producing `c` and `n₀` for four O-claims, and the smallest
  `n₀` that works for one of them.

**Core** — solve from an empty file, without re-reading the lesson.
- *Rank eleven functions* (own) — testing: ordering by eventual dominance, and justifying two
  adjacent pairs with a ratio.
- *Find the crossover* (own) — testing: computing the `n` at which `100n` overtakes `n²`, then
  measuring it.
- *O, Omega, Theta — twelve statements* (own) — testing: true or false, including the true-but-useless
  ones such as a linear loop being `O(n³)`.
- *The tight bound they actually wanted* (own) — testing: answering "what is the complexity" with
  `Θ`, and saying when only `O` is honest.

**Stretch** — today's ideas combined with an earlier ID.
- *Two machines, one ranking* (own) — combines `CPX-04` with `CPX-02`, because the two timing tables
  only agree once you have decided what `n` is — testing: reading two timing tables that disagree on
  every second and agree on every shape.
- *Where the lower-order term is the whole cost* (own) — combines `CPX-04` with `CPX-03`, because the
  term you can ignore is decided by the iteration count the variant gave you — testing: the input
  range over which `n² + 10⁶n` is not usefully quadratic.
- *Disprove an O-claim* (own) — combines `CPX-05` with `CPX-04` — testing: showing no `(c, n₀)` can
  exist, by a ratio argument or by contradiction.

**Interview** — narrate aloud before you type.
- *The worst case of the best bound* (own) — testing: separating which case from which bound, and
  what each of the four combinations claims.
- *Same class, different job* (own) — testing: two linear procedures with a thirtyfold constant, and
  deciding which one ships.

---

## 7. The gate

Say these out loud, without notes:

1. Why is a measured time not a property of an algorithm? Name four things it *is* a property of.
2. What is invariant about a doubling table's ratio column, and why does that make it the
   instrument rather than the seconds?
3. Define "eventually dominates" with both quantifiers, and say which one people forget.
4. Give an example where the asymptotically worse algorithm is the correct choice, from a real
   standard library.
5. Name the two things a growth class discards, and give a case where each one is the entire cost.
6. State the definition of `f(n) = O(g(n))`. Then prove `3n² + 7n + 2 = O(n²)` in two lines.
7. Why can a benchmark refute an asymptotic claim but never establish one?
8. Is a linear loop `O(n²)`? Is it `Θ(n²)`? Explain why one answer is "yes and it is useless".
9. Give the two-sided witnesses for `n² + 100n = Θ(n²)`.
10. State a complexity in the three-slot form: `Θ(what)`, in which case, over which inputs — for
    linear search, and then for the lab function you wrote today.
11. Which of `O`, `Ω`, `Θ` does Day 2's termination measure hand you, and why can it not hand you
    the others?

Then:

```bash
./k done 3
```

Tomorrow: `CPX-06` — the zoo, felt. Constant to factorial, and the input size at which each of them
stops being usable.
