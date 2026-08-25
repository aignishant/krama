# Day 1 — Checklist

`./k done 1` refuses to commit until every box is ticked.

## Read
- [ ] 1.1 What an algorithm actually is
- [ ] 1.2 Specification versus procedure
- [ ] 2.1 The RAM model
- [ ] 2.2 Defining `n`
- [ ] 2.3 Where the fiction leaks
- [ ] Redrew the §5 flow diagram of 1.1 by hand
- [ ] Reproduced the `IndexError` from §8 of 1.1 in a REPL with my own eyes
- [ ] Reproduced the `s[-i]` near-miss returning `True` for `"ab"`
- [ ] Reproduced the `RecursionError` from §8 of 1.2, and can say why raising the limit is the
      wrong repair
- [ ] Reproduced the `OverflowError` from §8 of 2.2, and checked `int(m ** 0.5)` against `k` for
      `k = 2**60 + 1` myself
- [ ] Reproduced the `ValueError` from §8 of 2.3 with `int("1" * 5000)`

## Build
- [ ] `lab/implement.py` written from an empty file
- [ ] `uv run pytest days/day-01-what-computation-costs/lab -q` green, Hypothesis included
- [ ] The comparison-count test passes — my procedure performs `n - 1` comparisons, it does not
      merely report `n - 1`
- [ ] `uv run python days/day-01-what-computation-costs/lab/bench.py` run; the `ratio` column
      sits near 2 and `cmp/n` reads 1.00 at every size
- [ ] Ran it on a hundred random lists of length 50; explained why every comparison count is
      identical, and named the property
- [ ] Tried and failed to beat `n - 1` comparisons, and can say why it is impossible

## Ladder
- [ ] Warm-up: Specification or procedure? — twelve statements
- [ ] Warm-up: Which of these is one operation?
- [ ] Core: Second largest, tie policy stated first — from an empty file, tie decided before coding
- [ ] Core: Count the model operations of a reversal — reached a closed form and checked it against
      a run
- [ ] Core: What is `n` here? — eight inputs
- [ ] Stretch: Trial division, priced in digits (`CPX-02` + `CPX-01`)
- [ ] Stretch: The cache cliff, measured (`CPX-02` + `FND-02`) — and I found the size at which the
      ratio moves on my machine
- [ ] Interview: One specification, three procedures — narrated aloud before typing

## Gate
- [ ] All nine gate questions answered out loud without notes
- [ ] Anything I got wrong logged with `./k miss <ID>`
