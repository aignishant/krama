"""Doubling benchmark. The ratio column is the proof; the wall clock is noise.

Run:  uv run python days/day-01-what-computation-costs/lab/bench.py

What to look for, in this order.

1. The `ratio` column, which is this row's time divided by the previous row's.
   Theta(n) predicts 2.00 -- twice the input, twice the work. Anything settling
   near 4 means the procedure is quadratic and section 7 of part 1.2 is
   describing what you wrote.
2. The `cmp/n` column. It must read 1.00 at every size, because the contract
   says the count is exactly n - 1. If it reads about 2, you are comparing
   twice per element; if it climbs with n, you are not doing a single pass.
3. The drift upwards in the ratio at the largest sizes, which is not your
   procedure getting worse. That is part 2.3, leak one, on your machine.

Nothing floats: the seed is fixed, so this table is the same table tomorrow.
"""

import random
import time

from implement import max_and_comparisons

REPEATS = 5


def best_of(xs: list[int]) -> tuple[float, int]:
    """Smallest of REPEATS runs -- the minimum is the least noisy statistic here."""
    best = None
    comparisons = 0
    for _ in range(REPEATS):
        start = time.perf_counter()
        _, comparisons = max_and_comparisons(xs)
        elapsed = time.perf_counter() - start
        best = elapsed if best is None else min(best, elapsed)
    assert best is not None
    return best, comparisons


def main() -> None:
    random.seed(20260823)
    print(f"{'n':>10} {'seconds':>12} {'ratio':>8} {'comparisons':>13} {'cmp/n':>7}")
    previous = None
    n = 50_000
    for _ in range(7):
        xs = [random.randint(-(10**6), 10**6) for _ in range(n)]
        elapsed, comparisons = best_of(xs)
        ratio = f"{elapsed / previous:8.2f}" if previous else "       -"
        print(f"{n:>10} {elapsed:>12.6f} {ratio} {comparisons:>13,} {comparisons / n:>7.2f}")
        previous, n = elapsed, n * 2


if __name__ == "__main__":
    main()
