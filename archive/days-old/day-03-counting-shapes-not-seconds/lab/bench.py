"""Doubling benchmark. The ratio column is the proof; the wall clock is noise.

Run:  uv run python days/day-03-counting-shapes-not-seconds/lab/bench.py

This is the day's own instrument turned on the day's own lab. Two procedures
compute the same answer: yours, and the oracle that transcribes the definition
literally. Both are correct. Only one of them has a usable shape.

What to look for, in this order.

1. Your `ratio` column, which must settle near 2.00. That is part 1.1's
   invariant at work: doubling the input doubles the work, and the number is
   the same on any machine.
2. The oracle's `ratio` column, which settles near 4.00 -- the signature of a
   quadratic, since it re-checks a suffix for every candidate.
3. The `oracle / yours` column, which is not a constant. It doubles every row.
   That is the whole content of part 1.2: the gap between two shapes is not a
   factor, it is a factor that grows, and nothing you do to the constants of
   the slow one will close it.

The data is built so that the answer sits near the middle of the table, which
is the oracle's honest average rather than its worst case. Nothing floats: the
sizes are fixed, so this table is the same table tomorrow.
"""

import time

from implement import dominates_from
from reference import dominates_from as oracle_dominates_from

REPEATS = 3


def build(n: int) -> tuple[list[int], list[int]]:
    """Tables whose last violation is halfway along, so the answer is n // 2 + 1."""
    f = [1] * n
    g = [1] * n
    f[n // 2] = 99
    return f, g


def best(procedure, f: list[int], g: list[int]) -> float:
    out = None
    for _ in range(REPEATS):
        start = time.perf_counter()
        procedure(f, g, 1)
        elapsed = time.perf_counter() - start
        out = elapsed if out is None else min(out, elapsed)
    assert out is not None
    return out


def main() -> None:
    header = f"{'n':>8} {'yours (s)':>12} {'ratio':>7} {'oracle (s)':>12} {'ratio':>7}"
    print(f"{header} {'oracle/yours':>13}")
    previous_mine = previous_oracle = None
    n = 1_000
    for _ in range(5):
        f, g = build(n)
        mine = best(dominates_from, f, g)
        theirs = best(oracle_dominates_from, f, g)
        r_mine = f"{mine / previous_mine:7.2f}" if previous_mine else "      -"
        r_theirs = f"{theirs / previous_oracle:7.2f}" if previous_oracle else "      -"
        print(f"{n:>8} {mine:>12.6f} {r_mine} {theirs:>12.6f} {r_theirs} {theirs / mine:>12.1f}x")
        previous_mine, previous_oracle, n = mine, theirs, n * 2


if __name__ == "__main__":
    main()
