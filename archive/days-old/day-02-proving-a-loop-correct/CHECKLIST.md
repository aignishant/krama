# Day 2 — Checklist

`./k done 2` refuses to commit until every box is ticked.

## Read
- [ ] 1.1 Initialization and maintenance
- [ ] 1.2 Exit, and the negated guard
- [ ] 2.1 The measure that decreases
- [ ] 2.2 Partial versus total correctness
- [ ] Redrew the tape diagram of 1.1 by hand, with the invariant written under it
- [ ] Reproduced the `IndexError` from §8 of 1.1 by moving `i += 1` above the accumulation
- [ ] Reproduced the `total_of_seeded` near-miss and can say which of the two obligations it fails
- [ ] Reproduced `xs[index_of(xs, 99)]` from §8 of 1.2 returning a plausible element
- [ ] Reproduced the hang from §8 of 2.1 with `while n != 1` on `n = -3`, interrupted it, and read
      which line the traceback names
- [ ] Reproduced `expansion_of(3)` from 2.2 and killed it; then ran `expansion_capped(3)` and can
      say why the capped version is worse

## Build
- [ ] `lab/implement.py` written from an empty file, not copied from any §6
- [ ] The invariant and the variant written on paper **before** the first line of code
- [ ] `uv run pytest days/day-02-proving-a-loop-correct/lab -q` green, Hypothesis included
- [ ] `test_forbidden_shapes.py` green — no `//`, no `%`, no `divmod` in my file
- [ ] Experiment 1: the assertion passes at the top of the loop and fails between the two body
      statements; I can say why the second placement proves nothing
- [ ] Experiment 2: guard changed to `>`, failure read as a *partial-correctness* failure — input,
      expected, actual, line number
- [ ] Experiment 3: guard changed to `!=`, `divide(10, 3)` hung, interrupted, and the traceback
      pointed at the guard
- [ ] `uv run python days/day-02-proving-a-loop-correct/lab/bench.py` run; first table's ratio sits
      near 2.00, second table's iteration count does not move
- [ ] Can say why the second table is the one that identifies what `n` really is here

## Ladder
- [ ] Warm-up: Prove the maximum you wrote on Day 1
- [ ] Warm-up: Invariant for a loop you did not write
- [ ] Core: Where the invariant first breaks — named the exact iteration
- [ ] Core: Exit condition, negated — including the case where it does not follow
- [ ] Core: Find the variant — five loops, and identified the one with none
- [ ] Stretch: The strongest true invariant (`CPX-03` + `CPX-01`)
- [ ] Stretch: The loop that stops for the wrong reason (`CPX-03` + `CPX-02`)
- [ ] Interview: Partial, total, and the bug report — narrated aloud

## Gate
- [ ] All ten gate questions answered out loud without notes
- [ ] Anything I got wrong logged with `./k miss <ID>`
