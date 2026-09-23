# Day 3 — Checklist

`./k done 3` refuses to commit until every box is ticked.

## Read
- [ ] 1.1 Seconds do not travel
- [ ] 1.2 Eventual dominance and the crossover
- [ ] 1.3 What dropping constants destroys
- [ ] 2.1 Big-O and its witness
- [ ] 2.2 Omega, Theta, and the abuse of O
- [ ] Built the doubling harness from §6 of 1.1 myself, and ran it on two procedures
- [ ] Reproduced the small-`n` nonsense from §8 of 1.1 — a ratio below 1 on my own machine
- [ ] Reproduced the near-miss of 1.1: input generation inside the timed region, and watched a
      logarithmic procedure report a ratio of 2.00
- [ ] Measured a crossover myself, on any two procedures, and predicted it first from the constants
      the way §7 of 1.2 does
- [ ] Ran the four spellings of the sum from §5 of 1.3 and recorded my own machine's spread
- [ ] Reproduced the growing "smallest c" table from §6 of 2.1, and can say why a growing constant
      is a disproof rather than a fit
- [ ] Measured the best case and the worst case of `target in xs` from §5 of 2.2 and saw the gap

## Build
- [ ] `lab/implement.py` written from an empty file, not copied from any §6
- [ ] The invariant written above the loop, mentioning the **suffix**, before any code
- [ ] `uv run pytest days/day-03-counting-shapes-not-seconds/lab -q` green, Hypothesis included
- [ ] `test_forbidden_shapes.py` green — no slice, no `reversed`, no aggregate call
- [ ] The read-counting test passes: one pass, not a re-check of every suffix
- [ ] `uv run python days/day-03-counting-shapes-not-seconds/lab/bench.py` run; my ratio column near
      2.00, the oracle's near 4.00
- [ ] Found the size below which the oracle *wins*, and wrote the number down
- [ ] Can say why the `oracle / yours` column is the one that settles the argument

## Ladder
- [ ] Warm-up: The doubling table, read backwards
- [ ] Warm-up: Exhibit the witness
- [ ] Core: Rank eleven functions
- [ ] Core: Find the crossover — predicted, then measured
- [ ] Core: O, Omega, Theta — twelve statements
- [ ] Core: The tight bound they actually wanted
- [ ] Stretch: Two machines, one ranking (`CPX-04` + `CPX-02`)
- [ ] Stretch: Where the lower-order term is the whole cost (`CPX-04` + `CPX-03`)
- [ ] Stretch: Disprove an O-claim (`CPX-05` + `CPX-04`)
- [ ] Interview: The worst case of the best bound — narrated aloud
- [ ] Interview: Same class, different job — narrated aloud

## Gate
- [ ] All eleven gate questions answered out loud without notes
- [ ] Anything I got wrong logged with `./k miss <ID>`
